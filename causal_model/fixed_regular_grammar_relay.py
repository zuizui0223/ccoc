"""Fixed-regular-grammar totalization of the CCOC relay sharpness witness.

This module removes two construction caveats from the post-reopening one-action
relay without changing the historical theorem modules:

* the closed/open future grammar is one constant-size ``FinitePrefixGrammar`` for
  every system size rather than an ``m``-dependent finite word list; and
* the construction works for every positive number of memory leaves, not only
  powers of two.

The common primitive alphabet is ``{0,1,fire,tick}``. The closed grammar is the
one-state partial DFA with loops on ``0``, ``1``, and ``tick``. The open grammar
adds exactly the ``fire`` loop. Thus the languages are

    L_closed = {0,1,tick}*
    L_open   = {0,1,fire,tick}*.

To make those languages genuinely size-independent, all four system actions are
totalized locally. Address actions move a unique selector token down one child
edge when possible and stutter at a leaf. ``fire`` emits the permanent bit only
when the selected node is a memory leaf. Every action advances the pulse layer by
one radius-one synchronous step. Multiple incoming pulses are combined by the
fixed Boolean-OR rule; this makes the transition total on every declared
microstate. On the canonical one-leaf probe trajectories there is only one pulse
path, so the totalized semantics agrees exactly with the historical one-token
relay semantics.

Starting from quiescent comparison states with the selector at the relay-body
root, no closed action can create a pulse. Therefore every word in the infinite
closed regular language leaves the focal trace dependent only on the initial focal
bit. In the open grammar, the actual root-to-leaf path followed by ``fire`` and
enough ticks reads each memory bit. Hence the closed quotient has two classes and
the open quotient is discrete on ``2**(m+1)`` states for every ``m>=1``.

The grammar/automata facts and the local totalization are strengthening claims
about this explicit construction only. Regular-language restriction, partial
DFAs, local Boolean aggregation, and binary-tree addressing are classical
substrate and are not novelty claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from itertools import product
from typing import Iterable

from .constant_alphabet_relay import (
    ADDRESS_ONE,
    ADDRESS_ZERO,
    FIRE,
    GLOBAL_ACTION_ALPHABET,
    TICK,
    AddressedRelayConfiguration,
    addressed_output_trace,
    addressed_probe_word,
    addressed_quiescent_configuration,
    addressed_word_trajectory,
    selector_depth,
)
from .relay_tree_compilation import (
    ROOT,
    Node,
    Pulse,
    RelayTreeConfiguration,
    RelayTreeTopology,
    directed_edge_messages,
    is_quiescent,
    validate_configuration,
)
from .shared_grammar import FinitePrefixGrammar

CoordinateState = tuple[int, ...]
RelayWord = tuple[str, ...]
RelayTrace = tuple[int, ...]

CLOSED_REGULAR_ACTIONS = (ADDRESS_ZERO, ADDRESS_ONE, TICK)
OPEN_REGULAR_ACTIONS = GLOBAL_ACTION_ALPHABET
NEW_REGULAR_ACTIONS = (FIRE,)


def _validate_module_count(module_count: int) -> None:
    if not isinstance(module_count, int) or isinstance(module_count, bool) or module_count < 1:
        raise ValueError("module_count must be a positive integer")


def _validate_port(topology: RelayTreeTopology, port: int) -> None:
    topology.validate_port(port)


def _validate_coordinate_state(module_count: int, state: Iterable[int]) -> CoordinateState:
    _validate_module_count(module_count)
    normalized = tuple(state)
    if len(normalized) != module_count + 1:
        raise ValueError("state must contain one focal bit and one bit per module")
    if any(bit not in (0, 1) for bit in normalized):
        raise ValueError("all coordinate-state entries must be binary")
    return normalized


def all_regular_coordinate_states(module_count: int) -> tuple[CoordinateState, ...]:
    """Return the complete quiescent comparison domain ``{0,1}^{m+1}``."""
    _validate_module_count(module_count)
    return tuple(product((0, 1), repeat=module_count + 1))


def fixed_closed_regular_grammar() -> FinitePrefixGrammar:
    """One-state prefix grammar for ``{0,1,tick}*`` over the common alphabet."""
    grammar = FinitePrefixGrammar(
        actions=GLOBAL_ACTION_ALPHABET,
        transition_table=((0, 0, None, 0),),
    )
    if grammar.state_count != 1 or grammar.legal_actions(0) != CLOSED_REGULAR_ACTIONS:
        raise AssertionError("closed fixed regular grammar did not verify")
    return grammar


def fixed_open_regular_grammar() -> FinitePrefixGrammar:
    """One-state prefix grammar for the full four-symbol Kleene-star language."""
    grammar = FinitePrefixGrammar(
        actions=GLOBAL_ACTION_ALPHABET,
        transition_table=((0, 0, 0, 0),),
    )
    if grammar.state_count != 1 or grammar.legal_actions(0) != OPEN_REGULAR_ACTIONS:
        raise AssertionError("open fixed regular grammar did not verify")
    return grammar


def balanced_tree_max_selector_depth(module_count: int) -> int:
    """Exact maximum body-root-to-leaf depth of ``RelayTreeTopology.balanced``.

    For the midpoint-recursive balanced tree this is ``ceil(log2(m))``. The
    integer expression ``(m-1).bit_length()`` avoids floating-point arithmetic and
    handles ``m=1`` with depth zero.
    """
    _validate_module_count(module_count)
    return (module_count - 1).bit_length()


def tree_address_for_port(topology: RelayTreeTopology, port: int) -> RelayWord:
    """Return the actual left/right body-root-to-leaf address for any ``m``."""
    _validate_port(topology, port)
    leaf = topology.leaf_for_port(port)
    if leaf == topology.body_root:
        return ()

    reverse_bits: list[str] = []
    current = leaf
    while current != topology.body_root:
        parent = topology.parent_by_node[current]
        if parent == ROOT:
            raise AssertionError("leaf path reached focal root before relay body root")
        children = topology.children_by_node[parent]
        if len(children) != 2:
            raise AssertionError("non-root selector parent must be a binary relay")
        if current == children[0]:
            reverse_bits.append(ADDRESS_ZERO)
        elif current == children[1]:
            reverse_bits.append(ADDRESS_ONE)
        else:
            raise AssertionError("parent-child topology is inconsistent")
        current = parent
    return tuple(reversed(reverse_bits))


def fixed_regular_probe_word(topology: RelayTreeTopology, port: int) -> RelayWord:
    """Canonical open word that reads one leaf in an arbitrary-size balanced tree."""
    _validate_port(topology, port)
    address = tree_address_for_port(topology, port)
    leaf = topology.leaf_for_port(port)
    # One pulse is created by ``fire``; it then needs one local round per graph
    # edge from the leaf to the focal ROOT.
    return address + (FIRE,) + (TICK,) * topology.distance_to_root(leaf)


def _merge_pulses_or(pulses: tuple[Pulse, ...]) -> Pulse:
    """Total fixed local collision rule for the finite pulse alphabet."""
    nonempty = tuple(pulse for pulse in pulses if pulse is not None)
    if not nonempty:
        return None
    # Pulse values are binary. OR keeps the state alphabet {empty,0,1} fixed and
    # agrees with the historical one-token relay whenever <=1 input is nonempty.
    return 1 if any(pulse == 1 for pulse in nonempty) else 0


def _next_selector_node(topology: RelayTreeTopology, selector_node: Node, action: str) -> Node:
    """Local selector update: descend one edge on 0/1, stutter otherwise."""
    if action not in (ADDRESS_ZERO, ADDRESS_ONE):
        return selector_node
    children = topology.children_by_node[selector_node]
    if len(children) != 2:
        # The selector has reached a memory leaf. Further address symbols are a
        # local stutter, which makes the action total without a depth oracle.
        return selector_node
    return children[0 if action == ADDRESS_ZERO else 1]


def apply_fixed_regular_action(
    topology: RelayTreeTopology,
    configuration: AddressedRelayConfiguration,
    action: str,
) -> AddressedRelayConfiguration:
    """Apply one total radius-one action from the fixed four-symbol alphabet.

    No global quiescence predicate is consulted. Every action advances the pulse
    layer by one synchronous local round. A selected leaf emits its permanent bit
    exactly when the global action is ``fire``; firing at an internal selector
    position emits nothing.
    """
    if not topology.verify():
        raise ValueError("topology must verify")
    validate_configuration(topology, configuration.relay)
    if configuration.selector_node not in topology.leaves + topology.relays:
        raise ValueError("selector token must occupy one relay-body node or leaf")
    if action not in GLOBAL_ACTION_ALPHABET:
        raise ValueError("unknown fixed-regular-grammar action")

    messages = directed_edge_messages(topology, configuration.relay)

    fired_port: int | None = None
    if action == FIRE and configuration.selector_node in topology.leaves:
        fired_port = topology.leaves.index(configuration.selector_node)

    next_leaf_pulses = tuple(
        configuration.relay.memory_bits[index] if index == fired_port else None
        for index in range(topology.module_count)
    )

    next_relay_pulses = tuple(
        _merge_pulses_or(
            tuple(messages[(child, relay)] for child in topology.children_by_node[relay])
        )
        for relay in topology.relays
    )

    root_child = topology.children_by_node[ROOT][0]
    root_message = messages[(root_child, ROOT)]
    next_output = root_message if root_message is not None else configuration.relay.focal_output

    relay = RelayTreeConfiguration(
        focal_output=next_output,
        memory_bits=configuration.relay.memory_bits,
        leaf_pulses=next_leaf_pulses,
        relay_pulses=next_relay_pulses,
    )
    validate_configuration(topology, relay)

    result = AddressedRelayConfiguration(
        relay=relay,
        selector_node=_next_selector_node(topology, configuration.selector_node, action),
    )
    if result.selector_node not in topology.leaves + topology.relays:
        raise AssertionError("total selector update left relay body")
    return result


def fixed_regular_word_trajectory(
    topology: RelayTreeTopology,
    initial: AddressedRelayConfiguration,
    word: Iterable[str],
) -> tuple[AddressedRelayConfiguration, ...]:
    """Replay any word over the totalized fixed global alphabet."""
    validate_configuration(topology, initial.relay)
    if initial.selector_node not in topology.leaves + topology.relays:
        raise ValueError("selector token must occupy one relay-body node or leaf")
    trajectory = [initial]
    current = initial
    for action in tuple(word):
        current = apply_fixed_regular_action(topology, current, action)
        trajectory.append(current)
    return tuple(trajectory)


def fixed_regular_output_trace(
    topology: RelayTreeTopology,
    initial: AddressedRelayConfiguration,
    word: Iterable[str],
) -> RelayTrace:
    return tuple(
        configuration.relay.focal_output
        for configuration in fixed_regular_word_trajectory(topology, initial, word)
    )


def _initial_configuration(topology: RelayTreeTopology, state: CoordinateState) -> AddressedRelayConfiguration:
    normalized = _validate_coordinate_state(topology.module_count, state)
    return addressed_quiescent_configuration(topology, normalized[0], normalized[1:])


def _canonical_open_signature(topology: RelayTreeTopology, state: CoordinateState) -> tuple[RelayTrace, ...]:
    initial = _initial_configuration(topology, state)
    return (fixed_regular_output_trace(topology, initial, ()),) + tuple(
        fixed_regular_output_trace(topology, initial, fixed_regular_probe_word(topology, port))
        for port in range(topology.module_count)
    )


@dataclass(frozen=True)
class FixedRegularGrammarRelayCertificate:
    """Finite certificate for the arbitrary-``m`` fixed-grammar strengthening."""

    module_count: int
    topology: RelayTreeTopology
    checked_coordinate_states: int

    @cached_property
    def closed_grammar(self) -> FinitePrefixGrammar:
        return fixed_closed_regular_grammar()

    @cached_property
    def open_grammar(self) -> FinitePrefixGrammar:
        return fixed_open_regular_grammar()

    @cached_property
    def states(self) -> tuple[CoordinateState, ...]:
        return all_regular_coordinate_states(self.module_count)

    @property
    def maximum_leaf_depth(self) -> int:
        return max(selector_depth(self.topology, leaf) for leaf in self.topology.leaves)

    @property
    def expected_maximum_leaf_depth(self) -> int:
        return balanced_tree_max_selector_depth(self.module_count)

    @property
    def worst_canonical_query_length(self) -> int:
        return max(len(fixed_regular_probe_word(self.topology, port)) for port in range(self.module_count))

    @property
    def expected_worst_canonical_query_length(self) -> int:
        return 2 * self.expected_maximum_leaf_depth + 2

    @property
    def maximum_degree(self) -> int:
        return max(self.topology.core_degree(node) for node in self.topology.nodes)

    @property
    def closed_interface_state_count(self) -> int:
        return 2

    @property
    def open_interface_state_count(self) -> int:
        return 2 ** (self.module_count + 1)

    @property
    def closed_interface_bits(self) -> int:
        return 1

    @property
    def open_interface_bits(self) -> int:
        return self.module_count + 1

    @property
    def open_only_innovation_bits(self) -> int:
        return self.module_count

    @property
    def selector_augmented_relay_state_count(self) -> int:
        return 6

    @property
    def selector_augmented_leaf_state_count(self) -> int:
        return 12

    def _closed_one_step_invariant(self) -> bool:
        """Check the induction step proving blindness for every closed word."""
        for state in self.states:
            relay = _initial_configuration(self.topology, state).relay
            for selector_node in self.topology.leaves + self.topology.relays:
                configuration = AddressedRelayConfiguration(relay=relay, selector_node=selector_node)
                for action in CLOSED_REGULAR_ACTIONS:
                    result = apply_fixed_regular_action(self.topology, configuration, action)
                    if result.relay.focal_output != relay.focal_output:
                        return False
                    if result.relay.memory_bits != relay.memory_bits:
                        return False
                    if not is_quiescent(self.topology, result.relay):
                        return False
        return True

    def _power_of_two_compatibility(self) -> bool:
        """On old canonical words, agree exactly with the historical relay."""
        m = self.module_count
        if m < 2 or m & (m - 1):
            return True
        for state in self.states:
            initial = _initial_configuration(self.topology, state)
            for port in range(m):
                old_word = addressed_probe_word(m, port)
                new_word = fixed_regular_probe_word(self.topology, port)
                if new_word != old_word:
                    return False
                if fixed_regular_output_trace(self.topology, initial, new_word) != addressed_output_trace(
                    self.topology, initial, old_word
                ):
                    return False
                if fixed_regular_word_trajectory(self.topology, initial, new_word)[-1] != addressed_word_trajectory(
                    self.topology, initial, old_word
                )[-1]:
                    return False
        return True

    def verify(self) -> bool:
        try:
            _validate_module_count(self.module_count)
            if self.topology != RelayTreeTopology.balanced(self.module_count):
                return False
            if not self.topology.verify():
                return False
            if self.checked_coordinate_states != 2 ** (self.module_count + 1):
                return False
            if len(self.states) != self.checked_coordinate_states:
                return False

            if self.closed_grammar.state_count != 1 or self.open_grammar.state_count != 1:
                return False
            if self.closed_grammar.actions != GLOBAL_ACTION_ALPHABET:
                return False
            if self.open_grammar.actions != GLOBAL_ACTION_ALPHABET:
                return False
            if self.closed_grammar.legal_actions(0) != CLOSED_REGULAR_ACTIONS:
                return False
            if self.open_grammar.legal_actions(0) != OPEN_REGULAR_ACTIONS:
                return False
            if set(self.open_grammar.legal_actions(0)) - set(self.closed_grammar.legal_actions(0)) != {FIRE}:
                return False
            try:
                self.closed_grammar.normalize_legal_word((FIRE,))
                return False
            except ValueError:
                pass
            if self.open_grammar.normalize_legal_word((FIRE,)) != (FIRE,):
                return False

            if self.maximum_degree > 3:
                return False
            if self.maximum_leaf_depth != self.expected_maximum_leaf_depth:
                return False
            if self.worst_canonical_query_length != self.expected_worst_canonical_query_length:
                return False

            # The topology itself is a tree: one parent edge per non-root node.
            if len(self.topology.message_edges) != len(self.topology.nodes) - 1:
                return False

            # Every actual tree-path address selects exactly its intended leaf.
            zero_state = (0,) * (self.module_count + 1)
            initial_zero = _initial_configuration(self.topology, zero_state)
            addresses: list[RelayWord] = []
            for port in range(self.module_count):
                address = tree_address_for_port(self.topology, port)
                addresses.append(address)
                selected = fixed_regular_word_trajectory(self.topology, initial_zero, address)[-1]
                if selected.selector_node != self.topology.leaf_for_port(port):
                    return False
                if len(address) != selector_depth(self.topology, self.topology.leaf_for_port(port)):
                    return False
            for left_index, left in enumerate(addresses):
                for right_index, right in enumerate(addresses):
                    if left_index == right_index:
                        continue
                    if len(left) <= len(right) and right[: len(left)] == left:
                        return False

            if not self._closed_one_step_invariant():
                return False

            if self.closed_interface_state_count != 2 or self.closed_interface_bits != 1:
                return False

            open_signatures: set[tuple[RelayTrace, ...]] = set()
            for state in self.states:
                initial = _initial_configuration(self.topology, state)
                open_signatures.add(_canonical_open_signature(self.topology, state))
                for port in range(self.module_count):
                    word = fixed_regular_probe_word(self.topology, port)
                    final = fixed_regular_word_trajectory(self.topology, initial, word)[-1]
                    if not is_quiescent(self.topology, final.relay):
                        return False
                    if final.relay.memory_bits != state[1:]:
                        return False
                    if final.relay.focal_output != state[port + 1]:
                        return False

            if len(open_signatures) != self.open_interface_state_count:
                return False
            if self.open_interface_bits != self.module_count + 1:
                return False
            if self.open_only_innovation_bits != self.module_count:
                return False

            if not self._power_of_two_compatibility():
                return False
            return True
        except (AssertionError, KeyError, TypeError, ValueError):
            return False


def certify_fixed_regular_grammar_relay(module_count: int) -> FixedRegularGrammarRelayCertificate:
    """Certify the fixed-grammar arbitrary-size relay at one finite ``m``."""
    _validate_module_count(module_count)
    certificate = FixedRegularGrammarRelayCertificate(
        module_count=module_count,
        topology=RelayTreeTopology.balanced(module_count),
        checked_coordinate_states=2 ** (module_count + 1),
    )
    if not certificate.verify():
        raise AssertionError("fixed-regular-grammar relay certificate did not verify")
    return certificate


__all__ = [
    "CLOSED_REGULAR_ACTIONS",
    "OPEN_REGULAR_ACTIONS",
    "NEW_REGULAR_ACTIONS",
    "fixed_closed_regular_grammar",
    "fixed_open_regular_grammar",
    "balanced_tree_max_selector_depth",
    "tree_address_for_port",
    "fixed_regular_probe_word",
    "apply_fixed_regular_action",
    "fixed_regular_word_trajectory",
    "fixed_regular_output_trace",
    "all_regular_coordinate_states",
    "FixedRegularGrammarRelayCertificate",
    "certify_fixed_regular_grammar_relay",
]
