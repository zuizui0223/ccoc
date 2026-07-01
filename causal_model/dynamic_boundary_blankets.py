"""Exact dynamic-boundary-blanket certificates for controlled open systems.

A static list of exterior covariates is not enough to support an open macro-law.
A boundary summary must also update consistently under every permitted action.
This module formalizes that requirement for finite deterministic controlled output
systems and proves three executable theorem families:

* the all-word controlled trace quotient stabilizes after a finite horizon;
* that quotient is the coarsest exact extension-stable deterministic interface;
* a dynamically closed inside-plus-boundary summary gives both memory and
  counterfactual-horizon upper bounds.

Combined with ``addressable_completion_bounds``, the module also records the
uniform-blanket obstruction: the binary exterior-completion family has no
boundary blanket of size bounded independently of the number of addressable
exterior modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, log2, prod
from typing import Hashable, Iterable

from .addressable_completion_bounds import (
    CanonicalAddressableProduct,
    certify_addressable_completion_product,
)

State = int
Action = str
SummaryLabel = Hashable
Partition = tuple[tuple[State, ...], ...]


def _validate_positive_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


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
    blocks: dict[int, list[State]] = {}
    for state, label in enumerate(labels):
        blocks.setdefault(label, []).append(state)
    return tuple(tuple(blocks[label]) for label in sorted(blocks))


@dataclass(frozen=True)
class FiniteControlledOutputSystem:
    """A finite deterministic controlled output system.

    ``transition_table[state][action_index]`` is the next state. ``outputs`` is
    the observation-window output at the current state.
    """

    actions: tuple[Action, ...]
    transition_table: tuple[tuple[State, ...], ...]
    outputs: tuple[Hashable, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.actions, tuple) or not self.actions:
            raise ValueError("actions must be a nonempty tuple")
        if any(not isinstance(action, str) or not action for action in self.actions):
            raise ValueError("actions must be nonempty strings")
        if len(set(self.actions)) != len(self.actions):
            raise ValueError("actions must be unique")
        if not isinstance(self.outputs, tuple) or not self.outputs:
            raise ValueError("outputs must be a nonempty tuple")
        state_count = len(self.outputs)
        if not isinstance(self.transition_table, tuple) or len(self.transition_table) != state_count:
            raise ValueError("transition_table must provide one row per state")
        for row in self.transition_table:
            if not isinstance(row, tuple) or len(row) != len(self.actions):
                raise ValueError("every transition row must match the action count")
            for target in row:
                if not isinstance(target, int) or isinstance(target, bool) or not 0 <= target < state_count:
                    raise ValueError("transition targets must be valid state indices")
        try:
            for output in self.outputs:
                hash(output)
        except TypeError as error:
            raise ValueError("outputs must be hashable") from error

    @property
    def state_count(self) -> int:
        return len(self.outputs)

    @property
    def states(self) -> tuple[State, ...]:
        return tuple(range(self.state_count))

    def action_index(self, action: Action) -> int:
        try:
            return self.actions.index(action)
        except ValueError as error:
            raise ValueError(f"unknown action: {action!r}") from error

    def transition(self, state: State, action: Action) -> State:
        self.validate_state(state)
        return self.transition_table[state][self.action_index(action)]

    def output(self, state: State) -> Hashable:
        self.validate_state(state)
        return self.outputs[state]

    def validate_state(self, state: State) -> None:
        if not isinstance(state, int) or isinstance(state, bool) or not 0 <= state < self.state_count:
            raise ValueError("state is outside the finite state space")

    def normalize_word(self, word: Iterable[Action]) -> tuple[Action, ...]:
        try:
            normalized = tuple(word)
        except TypeError as error:
            raise ValueError("word must be an iterable of actions") from error
        for action in normalized:
            self.action_index(action)
        return normalized

    def output_trace(self, state: State, word: Iterable[Action]) -> tuple[Hashable, ...]:
        current = state
        trace = [self.output(current)]
        for action in self.normalize_word(word):
            current = self.transition(current, action)
            trace.append(self.output(current))
        return tuple(trace)

    def horizon_labels(self, horizon: int) -> tuple[int, ...]:
        """Canonical labels for agreement on all action words of length <= horizon."""
        _validate_nonnegative_integer(horizon, "horizon")
        labels = _canonical_labels(self.outputs)
        for _ in range(horizon):
            labels = _canonical_labels(
                (self.outputs[state], tuple(labels[target] for target in self.transition_table[state]))
                for state in self.states
            )
        return labels

    def horizon_partition(self, horizon: int) -> Partition:
        return _partition_from_labels(self.horizon_labels(horizon))

    def first_stabilizing_horizon(self) -> int:
        """First t with P_t = P_{t+1}; finite systems guarantee t <= |S|-1."""
        for horizon in range(self.state_count):
            if self.horizon_labels(horizon) == self.horizon_labels(horizon + 1):
                return horizon
        raise AssertionError("finite partition refinement did not stabilize by the state-count bound")


def finite_horizon_partition(system: FiniteControlledOutputSystem, horizon: int) -> Partition:
    return system.horizon_partition(horizon)


@dataclass(frozen=True)
class FiniteHorizonStabilizationCertificate:
    """Certificate that finite counterfactual refinement has reached its exact quotient."""

    system: FiniteControlledOutputSystem
    stabilization_horizon: int
    partition_block_counts: tuple[int, ...]
    canonical_block_count: int

    @property
    def state_count_bound(self) -> int:
        return self.system.state_count - 1

    @property
    def open_interface_bits(self) -> float:
        return log2(self.canonical_block_count)

    def verify(self) -> bool:
        try:
            _validate_nonnegative_integer(self.stabilization_horizon, "stabilization_horizon")
            if self.stabilization_horizon > self.state_count_bound:
                return False
            expected_counts = tuple(
                len(self.system.horizon_partition(horizon))
                for horizon in range(self.stabilization_horizon + 2)
            )
            if self.partition_block_counts != expected_counts:
                return False
            if self.partition_block_counts[-1] != self.partition_block_counts[-2]:
                return False
            if any(
                self.system.horizon_partition(horizon) == self.system.horizon_partition(horizon + 1)
                for horizon in range(self.stabilization_horizon)
            ):
                return False
            final_partition = self.system.horizon_partition(self.stabilization_horizon)
            if self.canonical_block_count != len(final_partition):
                return False
            canonical_labels = self.system.horizon_labels(self.stabilization_horizon)
            next_labels = self.system.horizon_labels(self.stabilization_horizon + 1)
            if canonical_labels != next_labels:
                return False
            return DynamicInterfaceCertificate(self.system, canonical_labels).verify()
        except (AssertionError, ValueError):
            return False


def certify_finite_horizon_stabilization(
    system: FiniteControlledOutputSystem,
) -> FiniteHorizonStabilizationCertificate:
    horizon = system.first_stabilizing_horizon()
    certificate = FiniteHorizonStabilizationCertificate(
        system=system,
        stabilization_horizon=horizon,
        partition_block_counts=tuple(
            len(system.horizon_partition(step)) for step in range(horizon + 2)
        ),
        canonical_block_count=len(system.horizon_partition(horizon)),
    )
    if not certificate.verify():
        raise AssertionError("finite-horizon stabilization certificate did not verify")
    return certificate


@dataclass(frozen=True)
class DynamicInterfaceCertificate:
    """A summary that is output-respecting and update-closed under every action.

    Equal summary labels must imply equal current output and equal successor
    labels for each permitted action. This is the exact finite right-congruence
    condition required for a deterministic extension-stable macro-interface.
    """

    system: FiniteControlledOutputSystem
    summary_labels: tuple[SummaryLabel, ...]

    @property
    def summary_block_count(self) -> int:
        return len(set(self.summary_labels))

    def verify(self) -> bool:
        try:
            if not isinstance(self.summary_labels, tuple) or len(self.summary_labels) != self.system.state_count:
                return False
            for label in self.summary_labels:
                hash(label)
            for left in self.system.states:
                for right in self.system.states:
                    if self.summary_labels[left] != self.summary_labels[right]:
                        continue
                    if self.system.output(left) != self.system.output(right):
                        return False
                    for action in self.system.actions:
                        if self.summary_labels[self.system.transition(left, action)] != self.summary_labels[
                            self.system.transition(right, action)
                        ]:
                            return False
            final_labels = self.system.horizon_labels(self.system.first_stabilizing_horizon())
            for left in self.system.states:
                for right in self.system.states:
                    if self.summary_labels[left] == self.summary_labels[right] and final_labels[left] != final_labels[right]:
                        return False
            return True
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class DynamicBoundaryBlanketCertificate:
    """A dynamic inside-plus-boundary factorization certificate.

    The pair ``(inside_label, boundary_label)`` is required to satisfy the
    dynamic interface condition, not merely to fit current observations.
    """

    system: FiniteControlledOutputSystem
    inside_labels: tuple[SummaryLabel, ...]
    boundary_labels: tuple[SummaryLabel, ...]
    canonical_block_count: int
    stabilization_horizon: int

    @property
    def pair_labels(self) -> tuple[tuple[SummaryLabel, SummaryLabel], ...]:
        return tuple(zip(self.inside_labels, self.boundary_labels))

    @property
    def inside_cardinality(self) -> int:
        return len(set(self.inside_labels))

    @property
    def boundary_cardinality(self) -> int:
        return len(set(self.boundary_labels))

    @property
    def realized_pair_cardinality(self) -> int:
        return len(set(self.pair_labels))

    @property
    def open_interface_bits(self) -> float:
        return log2(self.canonical_block_count)

    @property
    def blanket_upper_bound_bits(self) -> float:
        return log2(self.inside_cardinality) + log2(self.boundary_cardinality)

    @property
    def realized_summary_upper_bound_bits(self) -> float:
        return log2(self.realized_pair_cardinality)

    @property
    def product_horizon_bound(self) -> int:
        return self.inside_cardinality * self.boundary_cardinality - 1

    @property
    def realized_horizon_bound(self) -> int:
        return self.realized_pair_cardinality - 1

    def verify(self) -> bool:
        try:
            if len(self.inside_labels) != self.system.state_count or len(self.boundary_labels) != self.system.state_count:
                return False
            if self.inside_cardinality < 1 or self.boundary_cardinality < 1:
                return False
            dynamic_interface = DynamicInterfaceCertificate(self.system, self.pair_labels)
            if not dynamic_interface.verify():
                return False
            stabilization = certify_finite_horizon_stabilization(self.system)
            if self.canonical_block_count != stabilization.canonical_block_count:
                return False
            if self.stabilization_horizon != stabilization.stabilization_horizon:
                return False
            if self.canonical_block_count > self.realized_pair_cardinality:
                return False
            if self.stabilization_horizon > self.realized_horizon_bound:
                return False
            if self.realized_horizon_bound > self.product_horizon_bound:
                return False
            if self.open_interface_bits > self.realized_summary_upper_bound_bits + 1e-12:
                return False
            if self.realized_summary_upper_bound_bits > self.blanket_upper_bound_bits + 1e-12:
                return False
            return True
        except (TypeError, ValueError):
            return False


def certify_dynamic_boundary_blanket(
    system: FiniteControlledOutputSystem,
    inside_labels: Iterable[SummaryLabel],
    boundary_labels: Iterable[SummaryLabel],
) -> DynamicBoundaryBlanketCertificate:
    try:
        inside = tuple(inside_labels)
        boundary = tuple(boundary_labels)
    except TypeError as error:
        raise ValueError("inside_labels and boundary_labels must be iterable") from error
    stabilization = certify_finite_horizon_stabilization(system)
    certificate = DynamicBoundaryBlanketCertificate(
        system=system,
        inside_labels=inside,
        boundary_labels=boundary,
        canonical_block_count=stabilization.canonical_block_count,
        stabilization_horizon=stabilization.stabilization_horizon,
    )
    if not certificate.verify():
        raise AssertionError("dynamic boundary blanket certificate did not verify")
    return certificate


@dataclass(frozen=True)
class UniformBlanketObstructionCertificate:
    """Lower bound on any boundary blanket for an addressable completion family."""

    factor_cardinalities: tuple[int, ...]
    required_boundary_state_count: int
    required_boundary_bits: float
    open_block_count: int

    @property
    def inside_cardinality(self) -> int:
        return self.factor_cardinalities[0]

    @property
    def exterior_cardinalities(self) -> tuple[int, ...]:
        return self.factor_cardinalities[1:]

    def verify(self) -> bool:
        try:
            product_system = CanonicalAddressableProduct(self.factor_cardinalities)
            product_certificate = certify_addressable_completion_product(self.factor_cardinalities)
            expected_boundary_states = prod(self.exterior_cardinalities)
            if self.required_boundary_state_count != expected_boundary_states:
                return False
            if abs(self.required_boundary_bits - log2(expected_boundary_states)) > 1e-12:
                return False
            if self.open_block_count != product_certificate.open_block_count:
                return False
            if self.open_block_count > self.inside_cardinality * self.required_boundary_state_count:
                return False
            if product_system.state_count != self.open_block_count:
                return False
            return True
        except (AssertionError, ValueError):
            return False


def certify_uniform_blanket_obstruction(
    factor_cardinalities: Iterable[int],
) -> UniformBlanketObstructionCertificate:
    product_system = CanonicalAddressableProduct(tuple(factor_cardinalities))
    boundary_states = prod(product_system.exterior_cardinalities)
    certificate = UniformBlanketObstructionCertificate(
        factor_cardinalities=product_system.factor_cardinalities,
        required_boundary_state_count=boundary_states,
        required_boundary_bits=log2(boundary_states),
        open_block_count=product_system.state_count,
    )
    if not certificate.verify():
        raise AssertionError("uniform blanket obstruction certificate did not verify")
    return certificate


def delay_chain_system(state_count: int) -> FiniteControlledOutputSystem:
    """One-action family whose exact counterfactual horizon grows linearly."""
    _validate_positive_integer(state_count, "state_count")
    if state_count < 2:
        raise ValueError("delay-chain state_count must be at least two")
    return FiniteControlledOutputSystem(
        actions=("advance",),
        transition_table=tuple((min(state + 1, state_count - 1),) for state in range(state_count)),
        outputs=tuple(1 if state == state_count - 1 else 0 for state in range(state_count)),
    )


def redundant_boundary_system() -> tuple[FiniteControlledOutputSystem, tuple[int, ...], tuple[int, ...]]:
    """Return a nontrivial four-state dynamic blanket with redundant microstate.

    States encode ``(inside, boundary, redundant)``. The redundant coordinate
    never affects output or transitions. The pair ``(inside, boundary)`` is a
    four-state exact dynamic blanket.
    """
    def encode(inside: int, boundary: int, redundant: int) -> int:
        return 4 * inside + 2 * boundary + redundant

    def decode(state: int) -> tuple[int, int, int]:
        return state // 4, (state // 2) % 2, state % 2

    rows: list[tuple[int, int]] = []
    outputs: list[int] = []
    inside_labels: list[int] = []
    boundary_labels: list[int] = []
    for state in range(8):
        inside, boundary, redundant = decode(state)
        rows.append(
            (
                encode(boundary, boundary, redundant),
                encode(inside, 1 - boundary, redundant),
            )
        )
        outputs.append(inside)
        inside_labels.append(inside)
        boundary_labels.append(boundary)
    system = FiniteControlledOutputSystem(
        actions=("read-boundary", "toggle-boundary"),
        transition_table=tuple(rows),
        outputs=tuple(outputs),
    )
    return system, tuple(inside_labels), tuple(boundary_labels)
