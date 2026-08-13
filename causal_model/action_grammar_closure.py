"""Exact closure/converse for one-state action-grammar expansion.

This module treats a deliberately narrow cross-grammar subclass.  A finite
controlled plant is held fixed while a one-state partial grammar enlarges its
set of globally legal primitive actions.  The closed language is ``A_C*`` and
the open language is ``A_O*`` with ``A_C subseteq A_O``.

Starting from the canonical closed response quotient, repeatedly split states by
the current quotient labels of all open-action successors.  The stable refinement
is exactly the canonical open response quotient.  Consequently zero interface
inflation holds if and only if every newly legal action descends to a well-defined
transition on the closed quotient.

The result is a CCOC converse/closure statement, not a novelty claim for
Myhill--Nerode theory, right congruences, DFA minimization, or partition
refinement.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import log2
from typing import Hashable, Iterable

from .dynamic_boundary_blankets import FiniteControlledOutputSystem

Action = str
Labels = tuple[int, ...]


def _canonical_labels(values: Iterable[Hashable]) -> Labels:
    mapping: dict[Hashable, int] = {}
    result: list[int] = []
    for value in values:
        if value not in mapping:
            mapping[value] = len(mapping)
        result.append(mapping[value])
    return tuple(result)


def _normalize_actions(
    system: FiniteControlledOutputSystem,
    actions: Iterable[Action],
    name: str,
) -> tuple[Action, ...]:
    try:
        requested = tuple(actions)
    except TypeError as error:
        raise ValueError(f"{name} must be iterable") from error
    if len(requested) != len(set(requested)):
        raise ValueError(f"{name} must not contain duplicate actions")
    for action in requested:
        system.action_index(action)
    requested_set = set(requested)
    # Canonicalize subset order to the plant action order so the certificate does
    # not depend on how the caller happened to enumerate a set.
    return tuple(action for action in system.actions if action in requested_set)


def _block_count(labels: Labels) -> int:
    return len(set(labels))


def _refine_labels(
    system: FiniteControlledOutputSystem,
    labels: Labels,
    actions: tuple[Action, ...],
) -> Labels:
    if len(labels) != system.state_count:
        raise ValueError("labels must contain one entry per plant state")
    return _canonical_labels(
        (
            labels[state],
            tuple(labels[system.transition(state, action)] for action in actions),
        )
        for state in system.states
    )


def canonical_action_quotient_labels(
    system: FiniteControlledOutputSystem,
    actions: Iterable[Action],
) -> Labels:
    """Canonical exact response quotient for the one-state language ``actions*``."""
    normalized = _normalize_actions(system, actions, "actions")
    labels = _canonical_labels(system.outputs)
    for _ in range(system.state_count):
        refined = _refine_labels(system, labels, normalized)
        if refined == labels:
            return labels
        labels = refined
    raise AssertionError("finite action quotient did not stabilize")


def action_grammar_refinement_trace(
    system: FiniteControlledOutputSystem,
    closed_actions: Iterable[Action],
    open_actions: Iterable[Action],
) -> tuple[Labels, ...]:
    """Refine the closed quotient until it is a congruence for all open actions."""
    closed = _normalize_actions(system, closed_actions, "closed_actions")
    opened = _normalize_actions(system, open_actions, "open_actions")
    if not set(closed).issubset(opened):
        raise ValueError("closed_actions must be a subset of open_actions")

    labels = canonical_action_quotient_labels(system, closed)
    trace = [labels]
    for _ in range(system.state_count):
        refined = _refine_labels(system, labels, opened)
        if refined == labels:
            return tuple(trace)
        labels = refined
        trace.append(labels)
    raise AssertionError("open congruence closure did not stabilize")


def shortest_distinguishing_word(
    system: FiniteControlledOutputSystem,
    actions: Iterable[Action],
    left_state: int,
    right_state: int,
) -> tuple[Action, ...]:
    """Return a shortest word whose output traces distinguish two plant states."""
    normalized = _normalize_actions(system, actions, "actions")
    system.validate_state(left_state)
    system.validate_state(right_state)

    if system.output(left_state) != system.output(right_state):
        return ()

    queue: deque[tuple[int, int, tuple[Action, ...]]] = deque(
        [(left_state, right_state, ())]
    )
    visited = {(left_state, right_state)}
    while queue:
        left, right, prefix = queue.popleft()
        for action in normalized:
            next_left = system.transition(left, action)
            next_right = system.transition(right, action)
            word = prefix + (action,)
            if system.output(next_left) != system.output(next_right):
                return word
            pair = (next_left, next_right)
            if pair not in visited:
                visited.add(pair)
                queue.append((next_left, next_right, word))
    raise ValueError("the supplied states are equivalent under the declared actions")


def newly_legal_actions_descend(
    system: FiniteControlledOutputSystem,
    closed_actions: Iterable[Action],
    open_actions: Iterable[Action],
) -> bool:
    """Whether every newly legal action induces a map on the closed quotient."""
    closed = _normalize_actions(system, closed_actions, "closed_actions")
    opened = _normalize_actions(system, open_actions, "open_actions")
    if not set(closed).issubset(opened):
        raise ValueError("closed_actions must be a subset of open_actions")
    new_actions = tuple(action for action in opened if action not in closed)
    closed_labels = canonical_action_quotient_labels(system, closed)
    for action in new_actions:
        for left in system.states:
            for right in range(left + 1, system.state_count):
                if closed_labels[left] != closed_labels[right]:
                    continue
                left_successor = system.transition(left, action)
                right_successor = system.transition(right, action)
                if closed_labels[left_successor] != closed_labels[right_successor]:
                    return False
    return True


@dataclass(frozen=True)
class ActionDescentObstructionCertificate:
    """One newly legal action plus a closed suffix that refutes a closed merge."""

    system: FiniteControlledOutputSystem
    closed_actions: tuple[Action, ...]
    open_actions: tuple[Action, ...]
    closed_labels: Labels
    left_state: int
    right_state: int
    newly_legal_action: Action
    closed_distinguishing_suffix: tuple[Action, ...]

    @property
    def open_witness_word(self) -> tuple[Action, ...]:
        return (self.newly_legal_action,) + self.closed_distinguishing_suffix

    def verify(self) -> bool:
        try:
            closed = _normalize_actions(self.system, self.closed_actions, "closed_actions")
            opened = _normalize_actions(self.system, self.open_actions, "open_actions")
            if closed != self.closed_actions or opened != self.open_actions:
                return False
            if not set(closed).issubset(opened):
                return False
            if self.newly_legal_action not in opened or self.newly_legal_action in closed:
                return False
            expected_labels = canonical_action_quotient_labels(self.system, closed)
            if self.closed_labels != expected_labels:
                return False
            self.system.validate_state(self.left_state)
            self.system.validate_state(self.right_state)
            if self.left_state == self.right_state:
                return False
            if self.closed_labels[self.left_state] != self.closed_labels[self.right_state]:
                return False
            left_successor = self.system.transition(self.left_state, self.newly_legal_action)
            right_successor = self.system.transition(self.right_state, self.newly_legal_action)
            if self.closed_labels[left_successor] == self.closed_labels[right_successor]:
                return False
            if any(action not in closed for action in self.closed_distinguishing_suffix):
                return False
            if self.system.output_trace(
                left_successor, self.closed_distinguishing_suffix
            ) == self.system.output_trace(
                right_successor, self.closed_distinguishing_suffix
            ):
                return False
            return self.system.output_trace(
                self.left_state, self.open_witness_word
            ) != self.system.output_trace(
                self.right_state, self.open_witness_word
            )
        except (AssertionError, TypeError, ValueError):
            return False


def find_action_descent_obstruction(
    system: FiniteControlledOutputSystem,
    closed_actions: Iterable[Action],
    open_actions: Iterable[Action],
) -> ActionDescentObstructionCertificate | None:
    """Return the first concrete obstruction to zero interface inflation."""
    closed = _normalize_actions(system, closed_actions, "closed_actions")
    opened = _normalize_actions(system, open_actions, "open_actions")
    if not set(closed).issubset(opened):
        raise ValueError("closed_actions must be a subset of open_actions")
    new_actions = tuple(action for action in opened if action not in closed)
    closed_labels = canonical_action_quotient_labels(system, closed)

    for action in new_actions:
        for left in system.states:
            for right in range(left + 1, system.state_count):
                if closed_labels[left] != closed_labels[right]:
                    continue
                left_successor = system.transition(left, action)
                right_successor = system.transition(right, action)
                if closed_labels[left_successor] == closed_labels[right_successor]:
                    continue
                suffix = shortest_distinguishing_word(
                    system, closed, left_successor, right_successor
                )
                certificate = ActionDescentObstructionCertificate(
                    system=system,
                    closed_actions=closed,
                    open_actions=opened,
                    closed_labels=closed_labels,
                    left_state=left,
                    right_state=right,
                    newly_legal_action=action,
                    closed_distinguishing_suffix=suffix,
                )
                if not certificate.verify():
                    raise AssertionError("constructed action-descent obstruction did not verify")
                return certificate
    return None


@dataclass(frozen=True)
class ActionGrammarClosureCertificate:
    """Exact cross-grammar closure certificate for one-state action expansion."""

    system: FiniteControlledOutputSystem
    closed_actions: tuple[Action, ...]
    open_actions: tuple[Action, ...]
    refinement_labels: tuple[Labels, ...]
    direct_open_labels: Labels

    @property
    def closed_labels(self) -> Labels:
        return self.refinement_labels[0]

    @property
    def stable_open_labels(self) -> Labels:
        return self.refinement_labels[-1]

    @property
    def closed_block_count(self) -> int:
        return _block_count(self.closed_labels)

    @property
    def open_block_count(self) -> int:
        return _block_count(self.stable_open_labels)

    @property
    def refinement_rounds(self) -> int:
        return len(self.refinement_labels) - 1

    @property
    def new_actions(self) -> tuple[Action, ...]:
        return tuple(action for action in self.open_actions if action not in self.closed_actions)

    @property
    def zero_inflation(self) -> bool:
        return self.closed_labels == self.stable_open_labels

    @property
    def closed_interface_bits(self) -> float:
        return log2(self.closed_block_count)

    @property
    def open_interface_bits(self) -> float:
        return log2(self.open_block_count)

    @property
    def inflation_bits(self) -> float:
        return self.open_interface_bits - self.closed_interface_bits

    @property
    def refinement_round_bound(self) -> int:
        return self.system.state_count - self.closed_block_count

    @property
    def descent_obstruction(self) -> ActionDescentObstructionCertificate | None:
        return find_action_descent_obstruction(
            self.system, self.closed_actions, self.open_actions
        )

    def supports_open_block_bound(self, maximum_blocks: int) -> bool:
        if not isinstance(maximum_blocks, int) or isinstance(maximum_blocks, bool) or maximum_blocks < 1:
            raise ValueError("maximum_blocks must be a positive integer")
        return self.open_block_count <= maximum_blocks

    def verify(self) -> bool:
        try:
            closed = _normalize_actions(self.system, self.closed_actions, "closed_actions")
            opened = _normalize_actions(self.system, self.open_actions, "open_actions")
            if closed != self.closed_actions or opened != self.open_actions:
                return False
            if not set(closed).issubset(opened):
                return False

            expected_trace = action_grammar_refinement_trace(self.system, closed, opened)
            if self.refinement_labels != expected_trace or not self.refinement_labels:
                return False
            expected_open = canonical_action_quotient_labels(self.system, opened)
            if self.direct_open_labels != expected_open:
                return False
            if self.stable_open_labels != self.direct_open_labels:
                return False

            counts = tuple(_block_count(labels) for labels in self.refinement_labels)
            if any(later <= earlier for earlier, later in zip(counts, counts[1:])):
                return False
            if self.refinement_rounds > self.refinement_round_bound:
                return False

            descent = newly_legal_actions_descend(self.system, closed, opened)
            if self.zero_inflation != descent:
                return False
            obstruction = self.descent_obstruction
            if self.zero_inflation:
                if obstruction is not None:
                    return False
            else:
                if obstruction is None or not obstruction.verify():
                    return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_action_grammar_closure(
    system: FiniteControlledOutputSystem,
    closed_actions: Iterable[Action],
    open_actions: Iterable[Action],
) -> ActionGrammarClosureCertificate:
    closed = _normalize_actions(system, closed_actions, "closed_actions")
    opened = _normalize_actions(system, open_actions, "open_actions")
    if not set(closed).issubset(opened):
        raise ValueError("closed_actions must be a subset of open_actions")
    certificate = ActionGrammarClosureCertificate(
        system=system,
        closed_actions=closed,
        open_actions=opened,
        refinement_labels=action_grammar_refinement_trace(system, closed, opened),
        direct_open_labels=canonical_action_quotient_labels(system, opened),
    )
    if not certificate.verify():
        raise AssertionError("action-grammar closure certificate did not verify")
    return certificate


__all__ = [
    "ActionDescentObstructionCertificate",
    "ActionGrammarClosureCertificate",
    "canonical_action_quotient_labels",
    "action_grammar_refinement_trace",
    "shortest_distinguishing_word",
    "newly_legal_actions_descend",
    "find_action_descent_obstruction",
    "certify_action_grammar_closure",
]
