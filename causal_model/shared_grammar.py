"""Shared finite prefix-grammar primitives for the current paper core.

These classes describe a declared finite action contract and a finite controlled
output system constrained by that contract. They carry no claim about delayed
exposure, identifiability, or portability by themselves.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable

from .dynamic_boundary_blankets import FiniteControlledOutputSystem

Action = str
GrammarState = int
ProductState = tuple[int, int]
Partition = tuple[tuple[int, ...], ...]


def _validate_nonnegative_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")


def _canonical_labels(values: Iterable[Hashable]) -> tuple[int, ...]:
    labels: dict[Hashable, int] = {}
    result: list[int] = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


def _partition_from_labels(labels: tuple[int, ...]) -> Partition:
    blocks: dict[int, list[int]] = {}
    for state, label in enumerate(labels):
        blocks.setdefault(label, []).append(state)
    return tuple(tuple(blocks[label]) for label in sorted(blocks))


@dataclass(frozen=True)
class FinitePrefixGrammar:
    """A deterministic finite prefix-closed action grammar."""

    actions: tuple[Action, ...]
    transition_table: tuple[tuple[int | None, ...], ...]
    initial_state: GrammarState = 0

    def __post_init__(self) -> None:
        if not isinstance(self.actions, tuple) or not self.actions:
            raise ValueError("actions must be a nonempty tuple")
        if any(not isinstance(action, str) or not action for action in self.actions):
            raise ValueError("actions must be nonempty strings")
        if len(set(self.actions)) != len(self.actions):
            raise ValueError("actions must be unique")
        if not isinstance(self.transition_table, tuple) or not self.transition_table:
            raise ValueError("transition_table must be a nonempty tuple")
        state_count = len(self.transition_table)
        if (
            not isinstance(self.initial_state, int)
            or isinstance(self.initial_state, bool)
            or not 0 <= self.initial_state < state_count
        ):
            raise ValueError("initial_state is outside the grammar state space")
        for row in self.transition_table:
            if not isinstance(row, tuple) or len(row) != len(self.actions):
                raise ValueError("every grammar transition row must match the action count")
            for target in row:
                if target is None:
                    continue
                if (
                    not isinstance(target, int)
                    or isinstance(target, bool)
                    or not 0 <= target < state_count
                ):
                    raise ValueError("grammar transition targets must be valid states or None")

    @property
    def state_count(self) -> int:
        return len(self.transition_table)

    @property
    def states(self) -> tuple[GrammarState, ...]:
        return tuple(range(self.state_count))

    def action_index(self, action: Action) -> int:
        try:
            return self.actions.index(action)
        except ValueError as error:
            raise ValueError(f"unknown grammar action: {action!r}") from error

    def legal_actions(self, grammar_state: GrammarState) -> tuple[Action, ...]:
        self.validate_state(grammar_state)
        return tuple(
            action
            for action, target in zip(self.actions, self.transition_table[grammar_state])
            if target is not None
        )

    def transition(self, grammar_state: GrammarState, action: Action) -> GrammarState:
        self.validate_state(grammar_state)
        index = self.action_index(action)
        target = self.transition_table[grammar_state][index]
        if target is None:
            raise ValueError(f"action {action!r} is illegal at grammar state {grammar_state}")
        return target

    def validate_state(self, grammar_state: GrammarState) -> None:
        if (
            not isinstance(grammar_state, int)
            or isinstance(grammar_state, bool)
            or not 0 <= grammar_state < self.state_count
        ):
            raise ValueError("grammar state is outside the finite grammar")

    def normalize_legal_word(
        self,
        word: Iterable[Action],
        start_state: GrammarState | None = None,
    ) -> tuple[Action, ...]:
        try:
            normalized = tuple(word)
        except TypeError as error:
            raise ValueError("word must be an iterable of actions") from error
        current = self.initial_state if start_state is None else start_state
        self.validate_state(current)
        for action in normalized:
            current = self.transition(current, action)
        return normalized

    def legal_words_through(
        self,
        horizon: int,
        start_state: GrammarState | None = None,
    ) -> tuple[tuple[Action, ...], ...]:
        _validate_nonnegative_integer(horizon, "horizon")
        initial = self.initial_state if start_state is None else start_state
        self.validate_state(initial)
        words: list[tuple[Action, ...]] = [()]
        frontier: list[tuple[GrammarState, tuple[Action, ...]]] = [(initial, ())]
        for _ in range(horizon):
            next_frontier: list[tuple[GrammarState, tuple[Action, ...]]] = []
            for state, prefix in frontier:
                for action in self.legal_actions(state):
                    next_state = self.transition(state, action)
                    word = prefix + (action,)
                    words.append(word)
                    next_frontier.append((next_state, word))
            frontier = next_frontier
        return tuple(words)


@dataclass(frozen=True)
class GrammarAwareControlledSystem:
    """Finite deterministic output system constrained by a prefix grammar."""

    system: FiniteControlledOutputSystem
    grammar: FinitePrefixGrammar

    def __post_init__(self) -> None:
        if self.system.actions != self.grammar.actions:
            raise ValueError("system and grammar must use the same ordered action alphabet")

    @property
    def product_states(self) -> tuple[ProductState, ...]:
        return tuple(
            (system_state, grammar_state)
            for system_state in self.system.states
            for grammar_state in self.grammar.states
        )

    @property
    def product_state_count(self) -> int:
        return self.system.state_count * self.grammar.state_count

    def product_index(self, pair: ProductState) -> int:
        system_state, grammar_state = pair
        self.system.validate_state(system_state)
        self.grammar.validate_state(grammar_state)
        return system_state * self.grammar.state_count + grammar_state

    def horizon_labels(self, horizon: int) -> tuple[int, ...]:
        _validate_nonnegative_integer(horizon, "horizon")
        pairs = self.product_states
        labels = _canonical_labels(self.system.output(system_state) for system_state, _ in pairs)
        for _ in range(horizon):
            labels = _canonical_labels(
                (
                    self.system.output(system_state),
                    tuple(
                        (
                            action,
                            labels[
                                self.product_index(
                                    (
                                        self.system.transition(system_state, action),
                                        self.grammar.transition(grammar_state, action),
                                    )
                                )
                            ],
                        )
                        for action in self.grammar.legal_actions(grammar_state)
                    ),
                )
                for system_state, grammar_state in pairs
            )
        return labels

    def product_partition(self, horizon: int) -> Partition:
        return _partition_from_labels(self.horizon_labels(horizon))

    def initial_labels(self, horizon: int) -> tuple[int, ...]:
        labels = self.horizon_labels(horizon)
        return tuple(labels[self.product_index((state, self.grammar.initial_state))] for state in self.system.states)

    def initial_partition(self, horizon: int) -> Partition:
        return _partition_from_labels(self.initial_labels(horizon))

    def first_product_stabilizing_horizon(self) -> int:
        for horizon in range(self.product_state_count):
            if self.horizon_labels(horizon) == self.horizon_labels(horizon + 1):
                return horizon
        raise AssertionError("grammar-aware partition refinement did not stabilize by the product-state bound")


@dataclass(frozen=True)
class GrammarHorizonStabilizationCertificate:
    """Exact finite stabilization certificate for a grammar-aware product quotient."""

    constrained_system: GrammarAwareControlledSystem
    stabilization_horizon: int
    product_block_counts: tuple[int, ...]
    canonical_product_block_count: int

    @property
    def product_state_bound(self) -> int:
        return self.constrained_system.product_state_count - 1

    def verify(self) -> bool:
        try:
            _validate_nonnegative_integer(self.stabilization_horizon, "stabilization_horizon")
            if self.stabilization_horizon > self.product_state_bound:
                return False
            expected_counts = tuple(
                len(self.constrained_system.product_partition(horizon))
                for horizon in range(self.stabilization_horizon + 2)
            )
            if self.product_block_counts != expected_counts:
                return False
            if self.product_block_counts[-1] != self.product_block_counts[-2]:
                return False
            if any(
                self.constrained_system.product_partition(horizon)
                == self.constrained_system.product_partition(horizon + 1)
                for horizon in range(self.stabilization_horizon)
            ):
                return False
            if self.canonical_product_block_count != self.product_block_counts[-2]:
                return False
            return self.constrained_system.horizon_labels(
                self.stabilization_horizon
            ) == self.constrained_system.horizon_labels(self.stabilization_horizon + 1)
        except (AssertionError, ValueError):
            return False


def certify_grammar_horizon_stabilization(
    constrained_system: GrammarAwareControlledSystem,
) -> GrammarHorizonStabilizationCertificate:
    horizon = constrained_system.first_product_stabilizing_horizon()
    certificate = GrammarHorizonStabilizationCertificate(
        constrained_system=constrained_system,
        stabilization_horizon=horizon,
        product_block_counts=tuple(
            len(constrained_system.product_partition(step)) for step in range(horizon + 2)
        ),
        canonical_product_block_count=len(constrained_system.product_partition(horizon)),
    )
    if not certificate.verify():
        raise AssertionError("grammar-horizon stabilization certificate did not verify")
    return certificate


__all__ = [
    "Action",
    "GrammarState",
    "ProductState",
    "Partition",
    "FinitePrefixGrammar",
    "GrammarAwareControlledSystem",
    "GrammarHorizonStabilizationCertificate",
    "certify_grammar_horizon_stabilization",
]
