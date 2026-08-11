"""Constant-global-alphabet compilation of the CCOC relay sharpness witness.

The historical relay witness uses one externally selectable reader port per
exterior module.  Its local node/message grammar and degree are constant, but the
set of globally selectable ports grows with the module count.

This module removes that caveat for the power-of-two subfamily.  A single
selector token starts at the root of the binary relay body.  Global actions
``0`` and ``1`` move that token to the left or right child, ``fire`` asks the
selected leaf to emit its permanent memory bit, and ``tick`` propagates the
one-token pulse upward through the existing relay dynamics.

Thus the *global* action alphabet is the constant four-symbol set

    {"0", "1", "fire", "tick"}.

For ``m = 2**d`` leaves, the word that probes one leaf has exactly
``2*d + 2`` actions: ``d`` address bits followed by one fire and ``d + 1``
additional propagation ticks.  The output trace depends only on the initial
focal bit and the addressed memory bit.  Across all addressed words, every
binary memory coordinate remains independently observable.

The finite certificates below replay explicit instances.  The all-size theorem
is the symbolic address-routing plus relay-conjugacy argument documented in
``docs/constant_alphabet_relay.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log2
from typing import Iterable

from .relay_tree_compilation import (
    Node,
    RelayTreeConfiguration,
    RelayTreeTopology,
    coordinate_state,
    is_quiescent,
    micro_step,
    quiescent_configuration,
)

ADDRESS_ZERO = "0"
ADDRESS_ONE = "1"
FIRE = "fire"
TICK = "tick"
GLOBAL_ACTION_ALPHABET = (ADDRESS_ZERO, ADDRESS_ONE, FIRE, TICK)


def _validate_power_of_two_module_count(module_count: int) -> int:
    if not isinstance(module_count, int) or isinstance(module_count, bool) or module_count < 2:
        raise ValueError("module_count must be a power of two of at least two")
    if module_count & (module_count - 1):
        raise ValueError("module_count must be a power of two of at least two")
    return module_count.bit_length() - 1


def _validate_binary_state(module_count: int, state: Iterable[int]) -> tuple[int, ...]:
    normalized = tuple(state)
    if len(normalized) != module_count + 1:
        raise ValueError("state must contain one focal bit and one bit per module")
    if any(bit not in (0, 1) for bit in normalized):
        raise ValueError("state coordinates must be binary")
    return normalized


def _leaf_port(topology: RelayTreeTopology, leaf: Node) -> int:
    try:
        return topology.leaves.index(leaf)
    except ValueError as error:
        raise ValueError("selector is not at a memory leaf") from error


@dataclass(frozen=True)
class AddressedRelayConfiguration:
    """Relay microstate plus one local selector token."""

    relay: RelayTreeConfiguration
    selector_node: Node


def addressed_quiescent_configuration(
    topology: RelayTreeTopology,
    focal_output: int,
    memory_bits: tuple[int, ...],
) -> AddressedRelayConfiguration:
    """Embed a macrostate with the selector token at the binary-tree body root."""
    relay = quiescent_configuration(topology, focal_output, memory_bits)
    configuration = AddressedRelayConfiguration(relay=relay, selector_node=topology.body_root)
    validate_addressed_configuration(topology, configuration)
    return configuration


def validate_addressed_configuration(
    topology: RelayTreeTopology,
    configuration: AddressedRelayConfiguration,
) -> None:
    if not topology.verify():
        raise ValueError("topology must verify")
    if configuration.selector_node not in topology.leaves + topology.relays:
        raise ValueError("selector token must occupy one relay-body node or leaf")
    # coordinate_state validates the underlying relay configuration through the
    # relay module's public validation path.
    coordinate_state(configuration.relay)


def selector_depth(topology: RelayTreeTopology, selector_node: Node) -> int:
    """Distance of the selector below ``body_root`` in a perfect binary tree."""
    if selector_node not in topology.leaves + topology.relays:
        raise ValueError("selector node is outside the relay body")
    depth = 0
    current = selector_node
    while current != topology.body_root:
        current = topology.parent_by_node[current]
        if current == "root-output":
            raise ValueError("selector path left the relay body")
        depth += 1
    return depth


def apply_global_action(
    topology: RelayTreeTopology,
    configuration: AddressedRelayConfiguration,
    action: str,
) -> AddressedRelayConfiguration:
    """Apply one symbol from the constant global action alphabet.

    Address symbols move the unique selector token through one parent-child edge
    and are legal only while the relay pulse system is quiescent. ``fire`` is
    legal only at a selected leaf and performs the first relay microtick.
    ``tick`` advances the existing pairwise upward relay dynamics by one tick.
    """
    validate_addressed_configuration(topology, configuration)
    if action not in GLOBAL_ACTION_ALPHABET:
        raise ValueError("unknown constant-alphabet relay action")

    if action in (ADDRESS_ZERO, ADDRESS_ONE):
        if not is_quiescent(topology, configuration.relay):
            raise ValueError("address routing is legal only while relay pulses are quiescent")
        children = topology.children_by_node[configuration.selector_node]
        if len(children) != 2:
            raise ValueError("address action requires the selector to be at a binary relay")
        child_index = 0 if action == ADDRESS_ZERO else 1
        result = AddressedRelayConfiguration(
            relay=configuration.relay,
            selector_node=children[child_index],
        )
        validate_addressed_configuration(topology, result)
        return result

    if action == FIRE:
        if not is_quiescent(topology, configuration.relay):
            raise ValueError("fire is legal only from a quiescent relay state")
        port = _leaf_port(topology, configuration.selector_node)
        result = AddressedRelayConfiguration(
            relay=micro_step(topology, configuration.relay, fired_port=port),
            selector_node=configuration.selector_node,
        )
        validate_addressed_configuration(topology, result)
        return result

    result = AddressedRelayConfiguration(
        relay=micro_step(topology, configuration.relay, fired_port=None),
        selector_node=configuration.selector_node,
    )
    validate_addressed_configuration(topology, result)
    return result


def address_bits_for_port(module_count: int, port: int) -> tuple[str, ...]:
    """Binary root-to-leaf address in the balanced power-of-two topology."""
    depth = _validate_power_of_two_module_count(module_count)
    if not isinstance(port, int) or isinstance(port, bool) or not 0 <= port < module_count:
        raise ValueError("port is outside the addressed relay family")
    return tuple(ADDRESS_ONE if bit == "1" else ADDRESS_ZERO for bit in f"{port:0{depth}b}")


def addressed_probe_word(module_count: int, port: int) -> tuple[str, ...]:
    """The constant-alphabet word that reads one memory leaf."""
    depth = _validate_power_of_two_module_count(module_count)
    topology = RelayTreeTopology.balanced(module_count)
    if topology.settling_ticks != depth + 2:
        raise AssertionError("perfect binary relay settling depth does not match the symbolic bound")
    return address_bits_for_port(module_count, port) + (FIRE,) + (TICK,) * (topology.settling_ticks - 1)


def addressed_word_trajectory(
    topology: RelayTreeTopology,
    initial: AddressedRelayConfiguration,
    word: Iterable[str],
) -> tuple[AddressedRelayConfiguration, ...]:
    """Replay one declared constant-alphabet control word."""
    validate_addressed_configuration(topology, initial)
    trajectory = [initial]
    current = initial
    for action in tuple(word):
        current = apply_global_action(topology, current, action)
        trajectory.append(current)
    return tuple(trajectory)


def addressed_output_trace(
    topology: RelayTreeTopology,
    initial: AddressedRelayConfiguration,
    word: Iterable[str],
) -> tuple[int, ...]:
    """Observable focal-output trace for one addressed word."""
    return tuple(configuration.relay.focal_output for configuration in addressed_word_trajectory(topology, initial, word))


def run_addressed_probe(
    topology: RelayTreeTopology,
    initial: AddressedRelayConfiguration,
    port: int,
) -> AddressedRelayConfiguration:
    """Run the canonical binary-address word for ``port``."""
    if topology.module_count < 2:
        raise ValueError("constant-alphabet addressed family starts at two leaves")
    word = addressed_probe_word(topology.module_count, port)
    final = addressed_word_trajectory(topology, initial, word)[-1]
    if not is_quiescent(topology, final.relay):
        raise AssertionError("addressed relay probe did not settle")
    return final


def all_binary_coordinate_states(module_count: int) -> tuple[tuple[int, ...], ...]:
    _validate_power_of_two_module_count(module_count)
    return tuple(product((0, 1), repeat=module_count + 1))


def _open_signature(
    topology: RelayTreeTopology,
    state: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    initial = addressed_quiescent_configuration(topology, state[0], state[1:])
    return (addressed_output_trace(topology, initial, ()),) + tuple(
        addressed_output_trace(topology, initial, addressed_probe_word(topology.module_count, port))
        for port in range(topology.module_count)
    )


def _closed_signature(
    topology: RelayTreeTopology,
    state: tuple[int, ...],
    port: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    initial = addressed_quiescent_configuration(topology, state[0], state[1:])
    return (
        addressed_output_trace(topology, initial, ()),
        addressed_output_trace(topology, initial, addressed_probe_word(topology.module_count, port)),
    )


@dataclass(frozen=True)
class ConstantAlphabetRelaySharpnessCertificate:
    """Finite replay of constant-global-alphabet extension/compression sharpness."""

    module_count: int
    topology: RelayTreeTopology
    checked_state_port_pairs: int

    @property
    def address_depth(self) -> int:
        return _validate_power_of_two_module_count(self.module_count)

    @property
    def global_action_alphabet(self) -> tuple[str, ...]:
        return GLOBAL_ACTION_ALPHABET

    @property
    def global_action_alphabet_size(self) -> int:
        return len(self.global_action_alphabet)

    @property
    def probe_word_length(self) -> int:
        return 2 * self.address_depth + 2

    @property
    def open_interface_state_count(self) -> int:
        return 2 ** (self.module_count + 1)

    @property
    def open_interface_bits(self) -> int:
        return self.module_count + 1

    @property
    def closed_interface_state_counts(self) -> tuple[int, ...]:
        return (4,) * self.module_count

    @property
    def closed_interface_bits(self) -> tuple[int, ...]:
        return (2,) * self.module_count

    @property
    def noncommutation_gap_bits(self) -> int:
        return self.module_count - 1

    @property
    def maximum_degree(self) -> int:
        return max(self.topology.core_degree(node) for node in self.topology.nodes)

    @property
    def selector_augmented_relay_state_count(self) -> int:
        # Existing relay pulse state in {empty,0,1} times selected/unselected.
        return 6

    @property
    def selector_augmented_leaf_state_count(self) -> int:
        # Existing leaf state: permanent bit x pulse in {empty,0,1}; times selector marker.
        return 12

    def verify(self) -> bool:
        try:
            depth = _validate_power_of_two_module_count(self.module_count)
            if self.topology != RelayTreeTopology.balanced(self.module_count):
                return False
            if not self.topology.verify():
                return False
            if self.global_action_alphabet != ("0", "1", "fire", "tick"):
                return False
            if self.global_action_alphabet_size != 4:
                return False
            if self.maximum_degree > 3:
                return False
            if self.topology.settling_ticks != depth + 2:
                return False
            if self.probe_word_length != 2 * depth + 2:
                return False

            states = all_binary_coordinate_states(self.module_count)
            if self.checked_state_port_pairs != len(states) * self.module_count:
                return False

            open_signatures: set[tuple[tuple[int, ...], ...]] = set()
            closed_signatures = [set() for _ in range(self.module_count)]

            for state in states:
                initial = addressed_quiescent_configuration(self.topology, state[0], state[1:])
                if initial.selector_node != self.topology.body_root or not is_quiescent(self.topology, initial.relay):
                    return False
                open_signatures.add(_open_signature(self.topology, state))

                for port in range(self.module_count):
                    address = address_bits_for_port(self.module_count, port)
                    selected = addressed_word_trajectory(self.topology, initial, address)[-1]
                    if selected.selector_node != self.topology.leaf_for_port(port):
                        return False
                    final = run_addressed_probe(self.topology, initial, port)
                    if final.relay.focal_output != state[port + 1]:
                        return False
                    if final.relay.memory_bits != state[1:]:
                        return False
                    closed_signatures[port].add(_closed_signature(self.topology, state, port))

            if len(open_signatures) != self.open_interface_state_count:
                return False
            if tuple(len(signatures) for signatures in closed_signatures) != self.closed_interface_state_counts:
                return False
            return True
        except (AssertionError, KeyError, TypeError, ValueError):
            return False


def certify_constant_alphabet_relay_sharpness(
    module_count: int,
) -> ConstantAlphabetRelaySharpnessCertificate:
    """Certify the constant-global-alphabet family at one finite power-of-two size."""
    _validate_power_of_two_module_count(module_count)
    states = all_binary_coordinate_states(module_count)
    certificate = ConstantAlphabetRelaySharpnessCertificate(
        module_count=module_count,
        topology=RelayTreeTopology.balanced(module_count),
        checked_state_port_pairs=len(states) * module_count,
    )
    if not certificate.verify():
        raise AssertionError("constant-alphabet relay sharpness certificate did not verify")
    return certificate


__all__ = [
    "ADDRESS_ZERO",
    "ADDRESS_ONE",
    "FIRE",
    "TICK",
    "GLOBAL_ACTION_ALPHABET",
    "AddressedRelayConfiguration",
    "addressed_quiescent_configuration",
    "validate_addressed_configuration",
    "selector_depth",
    "apply_global_action",
    "address_bits_for_port",
    "addressed_probe_word",
    "addressed_word_trajectory",
    "addressed_output_trace",
    "run_addressed_probe",
    "all_binary_coordinate_states",
    "ConstantAlphabetRelaySharpnessCertificate",
    "certify_constant_alphabet_relay_sharpness",
]
