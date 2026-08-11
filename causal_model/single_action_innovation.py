"""One newly legal primitive action can force linear causal-interface innovation.

This module isolates the genuinely dynamic term in the post-reopening interface
inflation decomposition.  It reuses the existing constant-alphabet, degree-three
binary relay.

Closed operation already permits binary address routing and idle relay ticks, but
``fire`` is excluded.  Without ``fire`` no dormant memory bit can inject a pulse
into the focal channel, so every declared closed response trace factors through
the focal bit alone.  Opening the system legalizes exactly the one primitive
action ``fire``.  Together with the already available address and tick symbols,
this makes all addressed read words legal and separates every dormant memory
coordinate.

For m=2**d memory leaves, the closed quotient has two states while the open
quotient has 2**(m+1) states.  Thus the open-only innovation term is exactly m
bits, even though the open global action alphabet has size four, the new
primitive-action set has size one, local interactions are pairwise, and maximum
degree is three.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from itertools import product
from math import log2
from typing import Iterable

from .constant_alphabet_relay import (
    ADDRESS_ONE,
    ADDRESS_ZERO,
    FIRE,
    GLOBAL_ACTION_ALPHABET,
    TICK,
    address_bits_for_port,
    addressed_output_trace,
    addressed_probe_word,
    addressed_quiescent_configuration,
)
from .interface_inflation import (
    InterfaceInflationDecompositionCertificate,
    certify_interface_inflation_decomposition,
)
from .relay_tree_compilation import RelayTreeTopology

CoordinateState = tuple[int, ...]
RelayWord = tuple[str, ...]
RelayTrace = tuple[int, ...]

CLOSED_PRIMITIVE_ACTIONS = (ADDRESS_ZERO, ADDRESS_ONE, TICK)
OPEN_PRIMITIVE_ACTIONS = GLOBAL_ACTION_ALPHABET
NEWLY_LEGAL_PRIMITIVE_ACTIONS = (FIRE,)


def _validate_power_of_two_module_count(module_count: int) -> int:
    if not isinstance(module_count, int) or isinstance(module_count, bool) or module_count < 2:
        raise ValueError("module_count must be a power of two of at least two")
    if module_count & (module_count - 1):
        raise ValueError("module_count must be a power of two of at least two")
    return module_count.bit_length() - 1


def all_coordinate_states(module_count: int) -> tuple[CoordinateState, ...]:
    """All quiescent macro states ``(y,b_1,...,b_m)``."""
    _validate_power_of_two_module_count(module_count)
    return tuple(product((0, 1), repeat=module_count + 1))


def closed_fire_free_words(module_count: int) -> tuple[RelayWord, ...]:
    """Finite closed grammar with routing/ticks available but ``fire`` absent.

    The family contains every binary address prefix of length at most ``d`` and,
    after each prefix, between zero and ``d+1`` idle ticks.  Since the relay is
    quiescent and no pulse is ever injected, all of these words leave the focal
    output unchanged while still demonstrating that address routing and ticks are
    already legal on the closed side.
    """
    depth = _validate_power_of_two_module_count(module_count)
    prefixes: set[RelayWord] = {()}
    for port in range(module_count):
        address = address_bits_for_port(module_count, port)
        for length in range(1, depth + 1):
            prefixes.add(address[:length])

    words = {
        prefix + (TICK,) * tick_count
        for prefix in prefixes
        for tick_count in range(depth + 2)
    }
    return tuple(sorted(words, key=lambda word: (len(word), word)))


def open_addressed_probe_words(module_count: int) -> tuple[RelayWord, ...]:
    """One open probe word per dormant memory leaf."""
    _validate_power_of_two_module_count(module_count)
    return tuple(addressed_probe_word(module_count, port) for port in range(module_count))


def _initial_configuration(
    topology: RelayTreeTopology,
    state: CoordinateState,
):
    return addressed_quiescent_configuration(topology, state[0], state[1:])


def _trace(
    topology: RelayTreeTopology,
    state: CoordinateState,
    word: RelayWord,
) -> RelayTrace:
    return addressed_output_trace(topology, _initial_configuration(topology, state), word)


def closed_response_signature(
    topology: RelayTreeTopology,
    state: CoordinateState,
    closed_words: tuple[RelayWord, ...],
) -> tuple[RelayTrace, ...]:
    """Exact declared closed response signature for one macro state."""
    return tuple(_trace(topology, state, word) for word in closed_words)


def open_response_signature(
    topology: RelayTreeTopology,
    state: CoordinateState,
    closed_words: tuple[RelayWord, ...],
    probe_words: tuple[RelayWord, ...],
) -> tuple[RelayTrace, ...]:
    """Full open signature: old closed responses plus addressed memory reads."""
    return closed_response_signature(topology, state, closed_words) + tuple(
        _trace(topology, state, word) for word in probe_words
    )


@dataclass(frozen=True)
class RelayInnovationSplitWitness:
    """Concrete dormant-memory pair split only by an open probe containing fire."""

    left_state: CoordinateState
    right_state: CoordinateState
    separating_word: RelayWord
    left_trace: RelayTrace
    right_trace: RelayTrace

    def verify(self, topology: RelayTreeTopology, closed_words: tuple[RelayWord, ...]) -> bool:
        try:
            if self.left_state == self.right_state:
                return False
            if closed_response_signature(topology, self.left_state, closed_words) != closed_response_signature(
                topology, self.right_state, closed_words
            ):
                return False
            if FIRE not in self.separating_word:
                return False
            if self.left_trace != _trace(topology, self.left_state, self.separating_word):
                return False
            if self.right_trace != _trace(topology, self.right_state, self.separating_word):
                return False
            return self.left_trace != self.right_trace
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class SingleActionInnovationCertificate:
    """Finite exhaustive certificate for the one-action linear-innovation family."""

    module_count: int
    topology: RelayTreeTopology
    closed_words: tuple[RelayWord, ...]
    open_probe_words: tuple[RelayWord, ...]

    @property
    def address_depth(self) -> int:
        return _validate_power_of_two_module_count(self.module_count)

    @cached_property
    def states(self) -> tuple[CoordinateState, ...]:
        return all_coordinate_states(self.module_count)

    @property
    def closed_primitive_actions(self) -> tuple[str, ...]:
        return CLOSED_PRIMITIVE_ACTIONS

    @property
    def open_primitive_actions(self) -> tuple[str, ...]:
        return OPEN_PRIMITIVE_ACTIONS

    @property
    def newly_legal_primitive_actions(self) -> tuple[str, ...]:
        return NEWLY_LEGAL_PRIMITIVE_ACTIONS

    @cached_property
    def closed_labels(self) -> tuple[tuple[RelayTrace, ...], ...]:
        return tuple(
            closed_response_signature(self.topology, state, self.closed_words)
            for state in self.states
        )

    @cached_property
    def open_labels(self) -> tuple[tuple[RelayTrace, ...], ...]:
        return tuple(
            self.closed_labels[index]
            + tuple(_trace(self.topology, state, word) for word in self.open_probe_words)
            for index, state in enumerate(self.states)
        )

    @cached_property
    def base_labels(self) -> tuple[int, ...]:
        return tuple(state[0] for state in self.states)

    @property
    def closed_block_count(self) -> int:
        return len(set(self.closed_labels))

    @property
    def open_block_count(self) -> int:
        return len(set(self.open_labels))

    @property
    def closed_interface_bits(self) -> float:
        return log2(self.closed_block_count)

    @property
    def open_interface_bits(self) -> float:
        return log2(self.open_block_count)

    @cached_property
    def decomposition(self) -> InterfaceInflationDecompositionCertificate:
        return certify_interface_inflation_decomposition(
            self.base_labels,
            (self.closed_labels,),
            self.open_labels,
        )

    @property
    def join_realizability_defect_bits(self) -> float:
        return self.decomposition.join_realizability_defect_bits

    @property
    def open_only_innovation_bits(self) -> float:
        return self.decomposition.new_word_innovation_bits

    @property
    def total_gap_bits(self) -> float:
        return self.decomposition.total_noncommutation_gap_bits

    @property
    def maximum_degree(self) -> int:
        return max(self.topology.core_degree(node) for node in self.topology.nodes)

    @cached_property
    def first_split_witness(self) -> RelayInnovationSplitWitness | None:
        for left_index, left_state in enumerate(self.states):
            for right_index in range(left_index + 1, len(self.states)):
                right_state = self.states[right_index]
                if self.closed_labels[left_index] != self.closed_labels[right_index]:
                    continue
                left_probe_traces = self.open_labels[left_index][len(self.closed_words) :]
                right_probe_traces = self.open_labels[right_index][len(self.closed_words) :]
                for port, word in enumerate(self.open_probe_words):
                    if left_probe_traces[port] != right_probe_traces[port]:
                        return RelayInnovationSplitWitness(
                            left_state=left_state,
                            right_state=right_state,
                            separating_word=word,
                            left_trace=left_probe_traces[port],
                            right_trace=right_probe_traces[port],
                        )
        return None

    def verify(self) -> bool:
        try:
            depth = _validate_power_of_two_module_count(self.module_count)
            if self.topology != RelayTreeTopology.balanced(self.module_count):
                return False
            if not self.topology.verify() or self.maximum_degree > 3:
                return False
            if self.closed_words != closed_fire_free_words(self.module_count):
                return False
            if self.open_probe_words != open_addressed_probe_words(self.module_count):
                return False
            if FIRE in self.closed_primitive_actions:
                return False
            if set(self.open_primitive_actions) - set(self.closed_primitive_actions) != {FIRE}:
                return False
            if self.newly_legal_primitive_actions != (FIRE,):
                return False
            if any(FIRE in word for word in self.closed_words):
                return False
            if not any(ADDRESS_ZERO in word for word in self.closed_words):
                return False
            if not any(ADDRESS_ONE in word for word in self.closed_words):
                return False
            if not any(TICK in word for word in self.closed_words):
                return False
            if any(word.count(FIRE) != 1 for word in self.open_probe_words):
                return False
            if any(len(word) != 2 * depth + 2 for word in self.open_probe_words):
                return False

            # With fire excluded, every declared closed trace is a repetition of
            # the current focal bit. Thus closed memory is exactly one bit.
            for state, signature in zip(self.states, self.closed_labels):
                for trace in signature:
                    if set(trace) != {state[0]}:
                        return False

            if self.closed_block_count != 2:
                return False
            if self.open_block_count != 2 ** (self.module_count + 1):
                return False

            # Every addressed word ends by exposing its selected dormant bit.
            for state, signature in zip(self.states, self.open_labels):
                probe_traces = signature[len(self.closed_words) :]
                if len(probe_traces) != self.module_count:
                    return False
                for port, trace in enumerate(probe_traces):
                    if trace[-1] != state[port + 1]:
                        return False

            decomposition = self.decomposition
            if not decomposition.verify():
                return False
            if decomposition.fibered_capacity_state_count != 2:
                return False
            if abs(self.join_realizability_defect_bits) > 1e-12:
                return False
            if abs(self.open_only_innovation_bits - self.module_count) > 1e-12:
                return False
            if abs(self.total_gap_bits - self.module_count) > 1e-12:
                return False

            witness = self.first_split_witness
            if witness is None or not witness.verify(self.topology, self.closed_words):
                return False
            return True
        except (AssertionError, KeyError, TypeError, ValueError):
            return False


def certify_single_action_innovation(module_count: int) -> SingleActionInnovationCertificate:
    """Certify the one-new-primitive-action innovation family at ``m=2**d``."""
    _validate_power_of_two_module_count(module_count)
    certificate = SingleActionInnovationCertificate(
        module_count=module_count,
        topology=RelayTreeTopology.balanced(module_count),
        closed_words=closed_fire_free_words(module_count),
        open_probe_words=open_addressed_probe_words(module_count),
    )
    if not certificate.verify():
        raise AssertionError("single-action innovation certificate did not verify")
    return certificate


__all__ = [
    "CoordinateState",
    "RelayWord",
    "RelayTrace",
    "CLOSED_PRIMITIVE_ACTIONS",
    "OPEN_PRIMITIVE_ACTIONS",
    "NEWLY_LEGAL_PRIMITIVE_ACTIONS",
    "all_coordinate_states",
    "closed_fire_free_words",
    "open_addressed_probe_words",
    "closed_response_signature",
    "open_response_signature",
    "RelayInnovationSplitWitness",
    "SingleActionInnovationCertificate",
    "certify_single_action_innovation",
]
