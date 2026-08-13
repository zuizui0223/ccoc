"""Exact closure converse for monotone finite prefix-grammar expansion.

This module generalizes the one-state action-alphabet converse in
``action_grammar_closure`` to finite state-dependent prefix grammars.  The
physical controlled plant is fixed.  Closed and open grammars use the same action
alphabet, grammar-state set, and initial grammar state.  Opening may replace
``None`` transitions by concrete grammar-state targets, but it may not change an
already-defined closed transition.

Starting from the canonical exact closed grammar-aware quotient, repeatedly split
blocks by their open enabled-action row and by the current quotient labels of all
open successors.  The stable partition is exactly the canonical open quotient.
Hence the closed quotient is reusable without inflation iff, inside every closed
fiber, the open legality row is uniform and every open successor descends to a
well-defined closed quotient state.

The result is a finite theorem-boundary characterization.  It does not assign
novelty to deterministic automata, right congruences, or partition refinement.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Hashable, Iterable, Literal

from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .grammar_aware_blankets import certify_grammar_aware_canonical_interface
from .shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem

SummaryLabel = Hashable
ObstructionKind = Literal["legality", "successor"]


def _canonical_labels(values: Iterable[Hashable]) -> tuple[int, ...]:
    labels: dict[Hashable, int] = {}
    result: list[int] = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


def _validate_monotone_expansion(closed_grammar: FinitePrefixGrammar, open_grammar: FinitePrefixGrammar) -> None:
    if closed_grammar.actions != open_grammar.actions:
        raise ValueError("closed and open grammars must use the same ordered action alphabet")
    if closed_grammar.state_count != open_grammar.state_count:
        raise ValueError("closed and open grammars must use the same grammar-state set")
    if closed_grammar.initial_state != open_grammar.initial_state:
        raise ValueError("closed and open grammars must use the same initial grammar state")
    for closed_row, open_row in zip(closed_grammar.transition_table, open_grammar.transition_table):
        for closed_target, open_target in zip(closed_row, open_row):
            if closed_target is not None and open_target != closed_target:
                raise ValueError("opening may add transitions but cannot change a closed transition")


def newly_enabled_transitions(closed_grammar: FinitePrefixGrammar, open_grammar: FinitePrefixGrammar) -> tuple[tuple[int, str, int], ...]:
    _validate_monotone_expansion(closed_grammar, open_grammar)
    additions: list[tuple[int, str, int]] = []
    for grammar_state, (closed_row, open_row) in enumerate(zip(closed_grammar.transition_table, open_grammar.transition_table)):
        for action, closed_target, open_target in zip(closed_grammar.actions, closed_row, open_row):
            if closed_target is None and open_target is not None:
                additions.append((grammar_state, action, open_target))
    return tuple(additions)


def _open_successor_index(constrained_system: GrammarAwareControlledSystem, product_index: int, action: str) -> int:
    system_state, grammar_state = constrained_system.product_states[product_index]
    return constrained_system.product_index((constrained_system.system.transition(system_state, action), constrained_system.grammar.transition(grammar_state, action)))


def refine_by_open_grammar(open_system: GrammarAwareControlledSystem, current_labels: tuple[SummaryLabel, ...]) -> tuple[int, ...]:
    if len(current_labels) != open_system.product_state_count:
        raise ValueError("current_labels must provide one label per open product state")
    for label in current_labels:
        hash(label)
    signatures = []
    for index, (_, grammar_state) in enumerate(open_system.product_states):
        legal = open_system.grammar.legal_actions(grammar_state)
        successor_signature = tuple((action, current_labels[_open_successor_index(open_system, index, action)]) for action in legal)
        signatures.append((current_labels[index], successor_signature))
    return _canonical_labels(signatures)


def grammar_expansion_refinement_sequence(plant: FiniteControlledOutputSystem, closed_grammar: FinitePrefixGrammar, open_grammar: FinitePrefixGrammar) -> tuple[tuple[int, ...], ...]:
    _validate_monotone_expansion(closed_grammar, open_grammar)
    closed_system = GrammarAwareControlledSystem(plant, closed_grammar)
    open_system = GrammarAwareControlledSystem(plant, open_grammar)
    closed = certify_grammar_aware_canonical_interface(closed_system).canonical_labels
    sequence = [closed]
    current = closed
    for _ in range(open_system.product_state_count):
        refined = refine_by_open_grammar(open_system, current)
        if refined == current:
            return tuple(sequence)
        sequence.append(refined)
        current = refined
    raise AssertionError("finite grammar-expansion refinement did not stabilize")


@dataclass(frozen=True)
class GrammarExpansionObstructionCertificate:
    plant: FiniteControlledOutputSystem
    closed_grammar: FinitePrefixGrammar
    open_grammar: FinitePrefixGrammar
    closed_labels: tuple[int, ...]
    left_index: int
    right_index: int
    kind: ObstructionKind
    action: str

    def verify(self) -> bool:
        try:
            _validate_monotone_expansion(self.closed_grammar, self.open_grammar)
            closed_system = GrammarAwareControlledSystem(self.plant, self.closed_grammar)
            open_system = GrammarAwareControlledSystem(self.plant, self.open_grammar)
            expected = certify_grammar_aware_canonical_interface(closed_system).canonical_labels
            if self.closed_labels != expected or self.left_index == self.right_index:
                return False
            if not 0 <= self.left_index < open_system.product_state_count or not 0 <= self.right_index < open_system.product_state_count:
                return False
            if self.closed_labels[self.left_index] != self.closed_labels[self.right_index]:
                return False
            _, left_q = open_system.product_states[self.left_index]
            _, right_q = open_system.product_states[self.right_index]
            left_legal = open_system.grammar.legal_actions(left_q)
            right_legal = open_system.grammar.legal_actions(right_q)
            if self.kind == "legality":
                return (self.action in left_legal) != (self.action in right_legal)
            if self.kind != "successor" or self.action not in left_legal or self.action not in right_legal:
                return False
            left_successor = _open_successor_index(open_system, self.left_index, self.action)
            right_successor = _open_successor_index(open_system, self.right_index, self.action)
            return self.closed_labels[left_successor] != self.closed_labels[right_successor]
        except (AssertionError, TypeError, ValueError):
            return False


def find_grammar_expansion_obstruction(plant: FiniteControlledOutputSystem, closed_grammar: FinitePrefixGrammar, open_grammar: FinitePrefixGrammar) -> GrammarExpansionObstructionCertificate | None:
    _validate_monotone_expansion(closed_grammar, open_grammar)
    closed_system = GrammarAwareControlledSystem(plant, closed_grammar)
    open_system = GrammarAwareControlledSystem(plant, open_grammar)
    labels = certify_grammar_aware_canonical_interface(closed_system).canonical_labels
    for left_index in range(open_system.product_state_count):
        for right_index in range(left_index + 1, open_system.product_state_count):
            if labels[left_index] != labels[right_index]:
                continue
            _, left_q = open_system.product_states[left_index]
            _, right_q = open_system.product_states[right_index]
            left_legal = open_system.grammar.legal_actions(left_q)
            right_legal = open_system.grammar.legal_actions(right_q)
            if left_legal != right_legal:
                for action in open_system.system.actions:
                    if (action in left_legal) != (action in right_legal):
                        cert = GrammarExpansionObstructionCertificate(plant, closed_grammar, open_grammar, labels, left_index, right_index, "legality", action)
                        if not cert.verify():
                            raise AssertionError("legality obstruction failed verification")
                        return cert
            for action in left_legal:
                left_successor = _open_successor_index(open_system, left_index, action)
                right_successor = _open_successor_index(open_system, right_index, action)
                if labels[left_successor] != labels[right_successor]:
                    cert = GrammarExpansionObstructionCertificate(plant, closed_grammar, open_grammar, labels, left_index, right_index, "successor", action)
                    if not cert.verify():
                        raise AssertionError("successor obstruction failed verification")
                    return cert
    return None


@dataclass(frozen=True)
class GrammarExpansionClosureCertificate:
    plant: FiniteControlledOutputSystem
    closed_grammar: FinitePrefixGrammar
    open_grammar: FinitePrefixGrammar
    closed_labels: tuple[int, ...]
    open_labels: tuple[int, ...]
    refinement_sequence: tuple[tuple[int, ...], ...]

    @property
    def product_state_count(self) -> int:
        return self.plant.state_count * self.closed_grammar.state_count

    @property
    def closed_block_count(self) -> int:
        return len(set(self.closed_labels))

    @property
    def open_block_count(self) -> int:
        return len(set(self.open_labels))

    @property
    def stable_labels(self) -> tuple[int, ...]:
        return self.refinement_sequence[-1]

    @property
    def strict_refinement_rounds(self) -> int:
        return len(self.refinement_sequence) - 1

    @property
    def refinement_round_bound(self) -> int:
        return self.product_state_count - self.closed_block_count

    @property
    def zero_inflation(self) -> bool:
        return self.open_labels == self.closed_labels

    @property
    def inflation_bits(self) -> float:
        return log2(self.open_block_count) - log2(self.closed_block_count)

    @property
    def newly_enabled_transition_count(self) -> int:
        return len(newly_enabled_transitions(self.closed_grammar, self.open_grammar))

    def open_summary_exists_with_at_most(self, block_bound: int) -> bool:
        if not isinstance(block_bound, int) or isinstance(block_bound, bool) or block_bound < 1:
            raise ValueError("block_bound must be a positive integer")
        return self.open_block_count <= block_bound

    def verify(self) -> bool:
        try:
            _validate_monotone_expansion(self.closed_grammar, self.open_grammar)
            closed_system = GrammarAwareControlledSystem(self.plant, self.closed_grammar)
            open_system = GrammarAwareControlledSystem(self.plant, self.open_grammar)
            closed = certify_grammar_aware_canonical_interface(closed_system).canonical_labels
            opened = certify_grammar_aware_canonical_interface(open_system).canonical_labels
            if self.closed_labels != closed or self.open_labels != opened:
                return False
            if not self.refinement_sequence or self.refinement_sequence[0] != self.closed_labels or self.stable_labels != self.open_labels:
                return False
            for earlier, later in zip(self.refinement_sequence, self.refinement_sequence[1:]):
                if refine_by_open_grammar(open_system, earlier) != later:
                    return False
                if len(set(later)) <= len(set(earlier)):
                    return False
            if refine_by_open_grammar(open_system, self.stable_labels) != self.stable_labels:
                return False
            if self.strict_refinement_rounds > self.refinement_round_bound:
                return False
            obstruction = find_grammar_expansion_obstruction(self.plant, self.closed_grammar, self.open_grammar)
            if self.zero_inflation != (obstruction is None):
                return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_grammar_expansion_closure(plant: FiniteControlledOutputSystem, closed_grammar: FinitePrefixGrammar, open_grammar: FinitePrefixGrammar) -> GrammarExpansionClosureCertificate:
    _validate_monotone_expansion(closed_grammar, open_grammar)
    closed_system = GrammarAwareControlledSystem(plant, closed_grammar)
    open_system = GrammarAwareControlledSystem(plant, open_grammar)
    certificate = GrammarExpansionClosureCertificate(
        plant=plant,
        closed_grammar=closed_grammar,
        open_grammar=open_grammar,
        closed_labels=certify_grammar_aware_canonical_interface(closed_system).canonical_labels,
        open_labels=certify_grammar_aware_canonical_interface(open_system).canonical_labels,
        refinement_sequence=grammar_expansion_refinement_sequence(plant, closed_grammar, open_grammar),
    )
    if not certificate.verify():
        raise AssertionError("grammar-expansion closure certificate did not verify")
    return certificate


__all__ = [
    "GrammarExpansionObstructionCertificate",
    "GrammarExpansionClosureCertificate",
    "newly_enabled_transitions",
    "refine_by_open_grammar",
    "grammar_expansion_refinement_sequence",
    "find_grammar_expansion_obstruction",
    "certify_grammar_expansion_closure",
]
