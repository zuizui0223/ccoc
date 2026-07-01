"""Bounded-degree relay-tree compilation of the extension--compression witness.

The coordinate witness in :mod:`extension_compression` has one focal bit ``y``
and dormant bits ``b_i`` that can be read by ``probe:i``.  This module gives an
exact finite implementation using a fixed local grammar:

* a one-tick reader event at one attached leaf;
* memory leaves carrying a permanent bit and a transient pulse;
* relay nodes carrying one transient pulse in ``{empty, 0, 1}``;
* one focal root-output node; and
* directed child-to-parent pairwise messages on a binary tree.

Only quiescent configurations are macro states.  One macro probe is a sequential
one-token protocol: fire one reader once, then let the tree settle.  The module
verifies that this protocol is conjugate, at macro time, to

    (y, b_1, ..., b_m) -> (b_i, b_1, ..., b_m).

The action grammar deliberately excludes simultaneous reader firings.  The
result is therefore an exact bounded-degree witness for a declared sequential
open-port interface, not a claim about arbitrary simultaneous environments.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Mapping

from .extension_compression import all_states, certify_extension_compression, probe_action, transition

Node = str
Pulse = int | None
ROOT: Node = "root-output"


def _validate_module_count(module_count: int) -> None:
    if not isinstance(module_count, int) or isinstance(module_count, bool) or module_count < 1:
        raise ValueError("module_count must be a positive integer")


def _validate_bit(value: int, name: str) -> None:
    if value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1")


@dataclass(frozen=True)
class OneTokenRelayGrammar:
    """The fixed finite local grammar, independent of the number of leaves."""

    reader_states: tuple[str, str] = ("ready", "fire")
    pulse_alphabet: tuple[Pulse, int, int] = (None, 0, 1)
    leaf_state_count: int = 6  # permanent bit times transient pulse
    relay_state_count: int = 3
    root_state_count: int = 2
    maximum_degree: int = 3

    def verify(self) -> bool:
        return (
            self.reader_states == ("ready", "fire")
            and self.pulse_alphabet == (None, 0, 1)
            and self.leaf_state_count == 6
            and self.relay_state_count == 3
            and self.root_state_count == 2
            and self.maximum_degree == 3
        )


def one_token_relay_grammar() -> OneTokenRelayGrammar:
    """Return the one constant-size node and message grammar used at every size."""
    grammar = OneTokenRelayGrammar()
    if not grammar.verify():
        raise AssertionError("constant relay grammar did not verify")
    return grammar


@dataclass(frozen=True)
class RelayTreeTopology:
    """A rooted binary relay tree with one focal output node above the tree body.

    Leaves are memory modules.  Internal tree nodes are relays.  ``ROOT`` is a
    separate focal-output node, so even a one-leaf system has a reader-leaf-root
    path.  A reader is attached only when a declared context activates one leaf.
    """

    module_count: int
    leaves: tuple[Node, ...]
    relays: tuple[Node, ...]
    body_root: Node
    children_by_node: Mapping[Node, tuple[Node, ...]]
    parent_by_node: Mapping[Node, Node]

    @classmethod
    def balanced(cls, module_count: int) -> "RelayTreeTopology":
        """Build a deterministic balanced binary tree for any positive leaf count."""
        _validate_module_count(module_count)
        leaves = tuple(f"leaf:{index}" for index in range(module_count))
        children: dict[Node, tuple[Node, ...]] = {leaf: () for leaf in leaves}
        parents: dict[Node, Node] = {}
        relay_index = 0

        def build(subtree_leaves: tuple[Node, ...]) -> Node:
            nonlocal relay_index
            if len(subtree_leaves) == 1:
                return subtree_leaves[0]
            midpoint = len(subtree_leaves) // 2
            left = build(subtree_leaves[:midpoint])
            right = build(subtree_leaves[midpoint:])
            relay = f"relay:{relay_index}"
            relay_index += 1
            children[relay] = (left, right)
            parents[left] = relay
            parents[right] = relay
            return relay

        body_root = build(leaves)
        children[ROOT] = (body_root,)
        parents[body_root] = ROOT
        topology = cls(
            module_count=module_count,
            leaves=leaves,
            relays=tuple(f"relay:{index}" for index in range(relay_index)),
            body_root=body_root,
            children_by_node=children,
            parent_by_node=parents,
        )
        if not topology.verify():
            raise AssertionError("constructed relay topology did not verify")
        return topology

    @property
    def nodes(self) -> tuple[Node, ...]:
        return self.leaves + self.relays + (ROOT,)

    @property
    def message_edges(self) -> tuple[tuple[Node, Node], ...]:
        return tuple((node, self.parent_by_node[node]) for node in self.nodes if node != ROOT)

    @property
    def relay_count(self) -> int:
        return len(self.relays)

    def leaf_for_port(self, port: int) -> Node:
        self.validate_port(port)
        return self.leaves[port]

    def validate_port(self, port: int) -> None:
        if not isinstance(port, int) or isinstance(port, bool) or not 0 <= port < self.module_count:
            raise ValueError(f"port must be an integer in [0, {self.module_count - 1}]")

    def reader_attachment_edge(self, port: int) -> tuple[Node, Node]:
        """The one degree-one reader edge available in a declared port context."""
        return (f"reader:{port}", self.leaf_for_port(port))

    def distance_to_root(self, node: Node) -> int:
        if node not in self.nodes:
            raise ValueError("node is not in this topology")
        distance = 0
        current = node
        while current != ROOT:
            current = self.parent_by_node[current]
            distance += 1
        return distance

    @property
    def settling_ticks(self) -> int:
        """Ticks from a reader firing to quiescence for every possible leaf."""
        return max(self.distance_to_root(leaf) for leaf in self.leaves) + 1

    def core_degree(self, node: Node) -> int:
        if node not in self.nodes:
            raise ValueError("node is not in this topology")
        child_degree = len(self.children_by_node[node])
        parent_degree = 0 if node == ROOT else 1
        return child_degree + parent_degree

    def degree_with_reader(self, node: Node, port: int) -> int:
        self.validate_port(port)
        return self.core_degree(node) + int(node == self.leaf_for_port(port))

    def maximum_degree_with_reader(self, port: int) -> int:
        self.validate_port(port)
        return max(self.degree_with_reader(node, port) for node in self.nodes)

    def verify(self) -> bool:
        try:
            _validate_module_count(self.module_count)
            if self.leaves != tuple(f"leaf:{index}" for index in range(self.module_count)):
                return False
            if len(self.relays) != self.module_count - 1:
                return False
            if len(set(self.nodes)) != len(self.nodes):
                return False
            if set(self.children_by_node) != set(self.nodes):
                return False
            if ROOT not in self.children_by_node or self.children_by_node[ROOT] != (self.body_root,):
                return False
            for leaf in self.leaves:
                if self.children_by_node[leaf] != ():
                    return False
            for relay in self.relays:
                if len(self.children_by_node[relay]) != 2:
                    return False
            if self.body_root not in self.leaves + self.relays:
                return False
            if set(self.parent_by_node) != set(self.nodes) - {ROOT}:
                return False
            for child, parent in self.parent_by_node.items():
                if child not in self.children_by_node[parent]:
                    return False
            for node in self.nodes:
                if node == ROOT:
                    continue
                if self.distance_to_root(node) < 1:
                    return False
            if any(self.core_degree(node) > 3 for node in self.nodes):
                return False
            if any(self.maximum_degree_with_reader(port) > 3 for port in range(self.module_count)):
                return False
            return True
        except (KeyError, ValueError):
            return False


@dataclass(frozen=True)
class RelayTreeConfiguration:
    """Microstate of the compiled tree; only quiescent states are macro states."""

    focal_output: int
    memory_bits: tuple[int, ...]
    leaf_pulses: tuple[Pulse, ...]
    relay_pulses: tuple[Pulse, ...]


def validate_configuration(topology: RelayTreeTopology, configuration: RelayTreeConfiguration) -> None:
    if not topology.verify():
        raise ValueError("topology must verify before configurations can be used")
    _validate_bit(configuration.focal_output, "focal_output")
    if len(configuration.memory_bits) != topology.module_count:
        raise ValueError("memory_bits must contain one bit per leaf")
    if len(configuration.leaf_pulses) != topology.module_count:
        raise ValueError("leaf_pulses must contain one pulse per leaf")
    if len(configuration.relay_pulses) != topology.relay_count:
        raise ValueError("relay_pulses must contain one pulse per relay")
    for index, bit in enumerate(configuration.memory_bits):
        _validate_bit(bit, f"memory_bits[{index}]")
    for name, pulse in tuple((f"leaf_pulses[{index}]", value) for index, value in enumerate(configuration.leaf_pulses)) + tuple((f"relay_pulses[{index}]", value) for index, value in enumerate(configuration.relay_pulses)):
        if pulse not in one_token_relay_grammar().pulse_alphabet:
            raise ValueError(f"{name} must be empty, 0, or 1")


def quiescent_configuration(
    topology: RelayTreeTopology,
    focal_output: int,
    memory_bits: tuple[int, ...],
) -> RelayTreeConfiguration:
    """Embed a coordinate-witness state at a quiescent macro boundary."""
    configuration = RelayTreeConfiguration(
        focal_output=focal_output,
        memory_bits=tuple(memory_bits),
        leaf_pulses=(None,) * topology.module_count,
        relay_pulses=(None,) * topology.relay_count,
    )
    validate_configuration(topology, configuration)
    return configuration


def is_quiescent(topology: RelayTreeTopology, configuration: RelayTreeConfiguration) -> bool:
    validate_configuration(topology, configuration)
    return all(pulse is None for pulse in configuration.leaf_pulses) and all(
        pulse is None for pulse in configuration.relay_pulses
    )


def coordinate_state(configuration: RelayTreeConfiguration) -> tuple[int, ...]:
    """Read the coordinate-witness state represented by a quiescent configuration."""
    return (configuration.focal_output,) + configuration.memory_bits


def _pulse_at_node(
    topology: RelayTreeTopology,
    configuration: RelayTreeConfiguration,
    node: Node,
) -> Pulse:
    if node in topology.leaves:
        return configuration.leaf_pulses[topology.leaves.index(node)]
    if node in topology.relays:
        return configuration.relay_pulses[topology.relays.index(node)]
    if node == ROOT:
        return None
    raise ValueError("node is not in this topology")


def directed_edge_messages(
    topology: RelayTreeTopology,
    configuration: RelayTreeConfiguration,
) -> Mapping[tuple[Node, Node], Pulse]:
    """Messages on the fixed pairwise child-to-parent channels at one microtick."""
    validate_configuration(topology, configuration)
    return {
        (child, parent): _pulse_at_node(topology, configuration, child)
        for child, parent in topology.message_edges
    }


def _unique_nonempty(pulses: tuple[Pulse, ...]) -> Pulse:
    nonempty = tuple(pulse for pulse in pulses if pulse is not None)
    if len(nonempty) > 1:
        raise ValueError("the one-token action grammar forbids simultaneous incoming pulses")
    return nonempty[0] if nonempty else None


def micro_step(
    topology: RelayTreeTopology,
    configuration: RelayTreeConfiguration,
    fired_port: int | None = None,
) -> RelayTreeConfiguration:
    """Advance one synchronous local-update tick.

    A non-null ``fired_port`` is the one-tick output of an attached reader in
    its ``fire`` state.  It is legal only at quiescence.  Leaves read that local
    reader message; relays and the root read only pairwise child-to-parent edge
    messages.  The grammar therefore remains fixed as the number of leaves
    grows.
    """
    validate_configuration(topology, configuration)
    if fired_port is not None:
        topology.validate_port(fired_port)
        if not is_quiescent(topology, configuration):
            raise ValueError("a reader may fire only from a quiescent macro state")

    messages = directed_edge_messages(topology, configuration)
    next_leaf_pulses = tuple(
        configuration.memory_bits[index] if index == fired_port else None
        for index in range(topology.module_count)
    )
    next_relay_pulses: list[Pulse] = []
    for relay in topology.relays:
        incoming = tuple(messages[(child, relay)] for child in topology.children_by_node[relay])
        next_relay_pulses.append(_unique_nonempty(incoming))
    root_child = topology.children_by_node[ROOT][0]
    root_message = messages[(root_child, ROOT)]
    next_output = root_message if root_message is not None else configuration.focal_output
    result = RelayTreeConfiguration(
        focal_output=next_output,
        memory_bits=configuration.memory_bits,
        leaf_pulses=next_leaf_pulses,
        relay_pulses=tuple(next_relay_pulses),
    )
    validate_configuration(topology, result)
    return result


def protocol_trajectory(
    topology: RelayTreeTopology,
    initial: RelayTreeConfiguration,
    port: int,
) -> tuple[RelayTreeConfiguration, ...]:
    """Run one reader firing plus enough idle ticks to reach universal quiescence."""
    topology.validate_port(port)
    validate_configuration(topology, initial)
    if not is_quiescent(topology, initial):
        raise ValueError("a macro probe must begin at quiescence")
    trajectory = [initial]
    current = initial
    for tick in range(topology.settling_ticks):
        current = micro_step(topology, current, fired_port=port if tick == 0 else None)
        trajectory.append(current)
    return tuple(trajectory)


def run_macro_probe(
    topology: RelayTreeTopology,
    initial: RelayTreeConfiguration,
    port: int,
) -> RelayTreeConfiguration:
    """Return the quiescent macro state after a declared reader probes one leaf."""
    final = protocol_trajectory(topology, initial, port)[-1]
    if not is_quiescent(topology, final):
        raise AssertionError("the one-token relay protocol did not settle")
    return final


@dataclass(frozen=True)
class RelayProtocolCertificate:
    """A replayable proof object for one compiled macro probe."""

    topology: RelayTreeTopology
    port: int
    trajectory: tuple[RelayTreeConfiguration, ...]

    @property
    def initial(self) -> RelayTreeConfiguration:
        return self.trajectory[0]

    @property
    def final(self) -> RelayTreeConfiguration:
        return self.trajectory[-1]

    def verify(self) -> bool:
        try:
            if not self.topology.verify():
                return False
            self.topology.validate_port(self.port)
            if len(self.trajectory) != self.topology.settling_ticks + 1:
                return False
            if not is_quiescent(self.topology, self.initial):
                return False
            for tick, configuration in enumerate(self.trajectory[:-1]):
                expected = micro_step(
                    self.topology,
                    configuration,
                    fired_port=self.port if tick == 0 else None,
                )
                if expected != self.trajectory[tick + 1]:
                    return False
            if not is_quiescent(self.topology, self.final):
                return False
            if self.final.memory_bits != self.initial.memory_bits:
                return False
            return self.final.focal_output == self.initial.memory_bits[self.port]
        except (AssertionError, KeyError, ValueError):
            return False


def certify_relay_protocol(
    topology: RelayTreeTopology,
    initial: RelayTreeConfiguration,
    port: int,
) -> RelayProtocolCertificate:
    certificate = RelayProtocolCertificate(
        topology=topology,
        port=port,
        trajectory=protocol_trajectory(topology, initial, port),
    )
    if not certificate.verify():
        raise AssertionError("relay protocol certificate did not verify")
    return certificate


@dataclass(frozen=True)
class BoundedDegreeCompilationCertificate:
    """Certificate that the relay tree macro-dynamics equal the coordinate witness."""

    module_count: int
    topology: RelayTreeTopology
    grammar: OneTokenRelayGrammar
    checked_protocols: int

    @property
    def closed_interface_bits(self) -> tuple[int, ...]:
        return tuple(2 for _ in range(self.module_count))

    @property
    def open_interface_bits(self) -> int:
        return self.module_count + 1

    @property
    def open_interface_state_count(self) -> int:
        return 2 ** (self.module_count + 1)

    def verify(self) -> bool:
        try:
            _validate_module_count(self.module_count)
            if self.topology.module_count != self.module_count or not self.topology.verify():
                return False
            if not self.grammar.verify():
                return False
            if self.checked_protocols != self.module_count * (2 ** (self.module_count + 1)):
                return False
            if any(self.topology.maximum_degree_with_reader(port) > self.grammar.maximum_degree for port in range(self.module_count)):
                return False
            coordinate_certificate = certify_extension_compression(self.module_count)
            if not coordinate_certificate.verify():
                return False
            for state in all_states(self.module_count):
                initial = quiescent_configuration(self.topology, state[0], state[1:])
                for port in range(self.module_count):
                    protocol = certify_relay_protocol(self.topology, initial, port)
                    expected_coordinate_state = transition(self.module_count, state, probe_action(port))
                    if coordinate_state(protocol.final) != expected_coordinate_state:
                        return False
            return True
        except (AssertionError, KeyError, ValueError):
            return False


def certify_bounded_degree_compilation(module_count: int) -> BoundedDegreeCompilationCertificate:
    """Construct the exact constant-grammar, degree-three compilation certificate."""
    _validate_module_count(module_count)
    topology = RelayTreeTopology.balanced(module_count)
    certificate = BoundedDegreeCompilationCertificate(
        module_count=module_count,
        topology=topology,
        grammar=one_token_relay_grammar(),
        checked_protocols=module_count * (2 ** (module_count + 1)),
    )
    if not certificate.verify():
        raise AssertionError("bounded-degree relay-tree compilation did not verify")
    return certificate


def exhaustive_compilation_summary(max_module_count: int = 6) -> tuple[BoundedDegreeCompilationCertificate, ...]:
    """Verify the explicit compilation family through a declared finite leaf bound."""
    if not isinstance(max_module_count, int) or isinstance(max_module_count, bool) or max_module_count < 1:
        raise ValueError("max_module_count must be a positive integer")
    return tuple(certify_bounded_degree_compilation(module_count) for module_count in range(1, max_module_count + 1))
