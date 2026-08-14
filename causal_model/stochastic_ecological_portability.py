"""Stochastic ecological portability from capped-state-driven colonization.

The positive theorem fixes guild saturation thresholds L and lets each controlled
colonization action draw a non-negative increment from a distribution that depends
only on the current capped guild state Z=min(L,N).  The abundance capacity M may
vary across systems.  Because

    min(L, min(M, N + D)) = min(L, Z + D),

the capped process is an exact controlled Markov lumping and its macro kernel is
independent of M.

The negative theorem adds a one-unit stochastic depletion action.  If depletion
occurs with probability p>0, abundance states L and L+1 have one-step capped-output
laws at total-variation distance p.  Repeated depletion attempts distinguish every
pair of saturated abundance states, so the exact open stochastic response classes
are all M+1 abundance states.

Markov lumpability, total variation, and finite stochastic kernels are classical
substrate.  The CCOC role is the grammar-sensitive ecological portability boundary.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import prod
from typing import Iterable

CountState = tuple[int, ...]
Increment = tuple[int, ...]
Event = tuple[Increment, Fraction]
Distribution = tuple[Event, ...]
MacroRow = tuple[Fraction, ...]


def _positive_int_tuple(values: Iterable[int], name: str) -> tuple[int, ...]:
    result = tuple(values)
    if not result:
        raise ValueError(f"{name} must be nonempty")
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 1 for value in result):
        raise ValueError(f"{name} must contain positive integers")
    return result


def _normalize_levels(values: Iterable[int], capacities: tuple[int, ...]) -> tuple[int, ...]:
    levels = _positive_int_tuple(values, "saturation_levels")
    if len(levels) != len(capacities):
        raise ValueError("one saturation level per guild is required")
    if any(level > capacity for level, capacity in zip(levels, capacities)):
        raise ValueError("saturation levels cannot exceed capacities")
    return levels


def _normalize_actions(values: Iterable[str]) -> tuple[str, ...]:
    actions = tuple(values)
    if not actions or any(not isinstance(action, str) or not action for action in actions):
        raise ValueError("actions must be nonempty strings")
    if len(set(actions)) != len(actions):
        raise ValueError("actions must be unique")
    return actions


def _normalize_distribution(values: Iterable[tuple[Iterable[int], object]], guild_count: int) -> Distribution:
    events: list[Event] = []
    for increment_like, probability_like in values:
        increment = tuple(increment_like)
        if len(increment) != guild_count:
            raise ValueError("increment dimension must match guild count")
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in increment):
            raise ValueError("stochastic colonization increments must be non-negative integers")
        try:
            probability = Fraction(probability_like)
        except (TypeError, ValueError, ZeroDivisionError) as error:
            raise ValueError("probabilities must be rational-like values") from error
        if probability < 0:
            raise ValueError("probabilities must be non-negative")
        if probability:
            events.append((increment, probability))
    if not events:
        raise ValueError("each proposal distribution must have positive mass")
    total = sum((probability for _, probability in events), Fraction(0, 1))
    if total != 1:
        raise ValueError("proposal probabilities must sum exactly to one")
    return tuple(events)


def capped_summary(state: CountState, levels: tuple[int, ...]) -> CountState:
    return tuple(min(level, abundance) for abundance, level in zip(state, levels))


@dataclass(frozen=True)
class StochasticGuildColonizationCertificate:
    """One finite abundance domain realizing a capacity-free stochastic macro law."""

    capacities: tuple[int, ...]
    saturation_levels: tuple[int, ...]
    actions: tuple[str, ...]
    proposal_table: tuple[tuple[Distribution, ...], ...]

    @property
    def guild_count(self) -> int:
        return len(self.capacities)

    @property
    def macro_states(self) -> tuple[CountState, ...]:
        return tuple(product(*(range(level + 1) for level in self.saturation_levels)))

    @property
    def micro_states(self) -> tuple[CountState, ...]:
        return tuple(product(*(range(capacity + 1) for capacity in self.capacities)))

    @property
    def macro_state_count(self) -> int:
        return prod(level + 1 for level in self.saturation_levels)

    @property
    def micro_state_count(self) -> int:
        return prod(capacity + 1 for capacity in self.capacities)

    def proposal_distribution(self, action_index: int, macro_state: CountState) -> Distribution:
        if not 0 <= action_index < len(self.actions):
            raise ValueError("action index outside action set")
        try:
            macro_index = self.macro_states.index(macro_state)
        except ValueError as error:
            raise ValueError("state outside capped macro domain") from error
        return self.proposal_table[action_index][macro_index]

    def macro_successor(self, macro_state: CountState, increment: Increment) -> CountState:
        return tuple(
            min(level, abundance + delta)
            for abundance, delta, level in zip(macro_state, increment, self.saturation_levels)
        )

    def macro_kernel_row(self, action_index: int, macro_state: CountState) -> MacroRow:
        masses: dict[CountState, Fraction] = defaultdict(Fraction)
        for increment, probability in self.proposal_distribution(action_index, macro_state):
            masses[self.macro_successor(macro_state, increment)] += probability
        return tuple(masses[state] for state in self.macro_states)

    def micro_induced_macro_row(self, action_index: int, micro_state: CountState) -> MacroRow:
        if micro_state not in self.micro_states:
            raise ValueError("state outside abundance domain")
        macro_state = capped_summary(micro_state, self.saturation_levels)
        masses: dict[CountState, Fraction] = defaultdict(Fraction)
        for increment, probability in self.proposal_distribution(action_index, macro_state):
            successor = tuple(
                min(capacity, abundance + delta)
                for abundance, delta, capacity in zip(micro_state, increment, self.capacities)
            )
            masses[capped_summary(successor, self.saturation_levels)] += probability
        return tuple(masses[state] for state in self.macro_states)

    @property
    def macro_kernel(self) -> tuple[tuple[MacroRow, ...], ...]:
        return tuple(
            tuple(self.macro_kernel_row(action_index, state) for state in self.macro_states)
            for action_index in range(len(self.actions))
        )

    def verify(self) -> bool:
        try:
            capacities = _positive_int_tuple(self.capacities, "capacities")
            if capacities != self.capacities:
                return False
            levels = _normalize_levels(self.saturation_levels, capacities)
            if levels != self.saturation_levels:
                return False
            actions = _normalize_actions(self.actions)
            if actions != self.actions:
                return False
            if len(self.proposal_table) != len(actions):
                return False
            if any(len(rows) != self.macro_state_count for rows in self.proposal_table):
                return False
            for rows in self.proposal_table:
                for distribution in rows:
                    if _normalize_distribution(distribution, self.guild_count) != distribution:
                        return False

            for action_index in range(len(actions)):
                for micro_state in self.micro_states:
                    if self.micro_induced_macro_row(action_index, micro_state) != self.macro_kernel_row(
                        action_index, capped_summary(micro_state, levels)
                    ):
                        return False
            return True
        except (TypeError, ValueError, ZeroDivisionError):
            return False


def certify_stochastic_guild_colonization(
    capacities: Iterable[int],
    saturation_levels: Iterable[int],
    actions: Iterable[str],
    proposal_table: Iterable[Iterable[Iterable[tuple[Iterable[int], object]]]],
) -> StochasticGuildColonizationCertificate:
    capacities_t = _positive_int_tuple(capacities, "capacities")
    levels_t = _normalize_levels(saturation_levels, capacities_t)
    actions_t = _normalize_actions(actions)
    macro_count = prod(level + 1 for level in levels_t)
    raw_actions = tuple(tuple(rows) for rows in proposal_table)
    if len(raw_actions) != len(actions_t):
        raise ValueError("proposal table needs one row-family per action")
    normalized: list[tuple[Distribution, ...]] = []
    for rows in raw_actions:
        if len(rows) != macro_count:
            raise ValueError("proposal table needs one distribution per capped macro state")
        normalized.append(tuple(_normalize_distribution(row, len(capacities_t)) for row in rows))
    certificate = StochasticGuildColonizationCertificate(
        capacities_t, levels_t, actions_t, tuple(normalized)
    )
    if not certificate.verify():
        raise AssertionError("stochastic guild-colonization certificate did not verify")
    return certificate


@dataclass(frozen=True)
class StochasticGuildCapacityFamilyCertificate:
    """Changing abundance domains sharing one exact stochastic macro kernel."""

    stages: tuple[StochasticGuildColonizationCertificate, ...]

    @property
    def macro_kernel(self) -> tuple[tuple[MacroRow, ...], ...]:
        return self.stages[0].macro_kernel

    @property
    def micro_state_counts(self) -> tuple[int, ...]:
        return tuple(stage.micro_state_count for stage in self.stages)

    @property
    def macro_state_count(self) -> int:
        return self.stages[0].macro_state_count

    def verify(self) -> bool:
        try:
            if not self.stages or any(not stage.verify() for stage in self.stages):
                return False
            first = self.stages[0]
            for stage in self.stages[1:]:
                if stage.saturation_levels != first.saturation_levels:
                    return False
                if stage.actions != first.actions:
                    return False
                if stage.proposal_table != first.proposal_table:
                    return False
                if stage.macro_kernel != first.macro_kernel:
                    return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_stochastic_capacity_family(
    capacities_by_stage: Iterable[Iterable[int]],
    saturation_levels: Iterable[int],
    actions: Iterable[str],
    proposal_table: Iterable[Iterable[Iterable[tuple[Iterable[int], object]]]],
) -> StochasticGuildCapacityFamilyCertificate:
    capacities_family = tuple(tuple(row) for row in capacities_by_stage)
    if not capacities_family:
        raise ValueError("at least one capacity stage is required")
    levels_t = tuple(saturation_levels)
    actions_t = tuple(actions)
    raw_table = tuple(tuple(tuple(event for event in distribution) for distribution in rows) for rows in proposal_table)
    stages = tuple(
        certify_stochastic_guild_colonization(capacities, levels_t, actions_t, raw_table)
        for capacities in capacities_family
    )
    certificate = StochasticGuildCapacityFamilyCertificate(stages)
    if not certificate.verify():
        raise AssertionError("stochastic capacity family did not share one macro kernel")
    return certificate


@dataclass(frozen=True)
class StochasticDepletionExposureCertificate:
    """A positive-probability depletion action reveals hidden oversaturation."""

    capacity: int
    saturation_level: int
    depletion_probability: Fraction

    @property
    def closed_class_count(self) -> int:
        return self.saturation_level + 1

    @property
    def open_exact_class_count(self) -> int:
        return self.capacity + 1

    @property
    def threshold_one_step_tv(self) -> Fraction:
        # N=L has mass p at L-1 and 1-p at L; N=L+1 is capped at L with certainty.
        return self.depletion_probability

    @property
    def minimum_common_one_step_tv_error(self) -> Fraction:
        # Any one macro transition law approximating both rows has max TV error >= TV/2.
        return self.threshold_one_step_tv / 2

    def saturated_pair_witness(self, lower: int, upper: int) -> tuple[int, Fraction, Fraction]:
        if not self.saturation_level <= lower < upper <= self.capacity:
            raise ValueError("pair must be distinct saturated abundance states")
        attempts = lower - self.saturation_level + 1
        lower_below_probability = self.depletion_probability ** attempts
        # Even if every attempt depletes, the higher state remains at least L.
        upper_below_probability = Fraction(0, 1)
        return attempts, lower_below_probability, upper_below_probability

    def verify(self) -> bool:
        try:
            if not isinstance(self.capacity, int) or isinstance(self.capacity, bool):
                return False
            if not isinstance(self.saturation_level, int) or isinstance(self.saturation_level, bool):
                return False
            if self.saturation_level < 1 or self.capacity < self.saturation_level + 1:
                return False
            probability = Fraction(self.depletion_probability)
            if probability != self.depletion_probability or not Fraction(0, 1) < probability <= Fraction(1, 1):
                return False
            if self.threshold_one_step_tv != probability:
                return False
            if self.minimum_common_one_step_tv_error != probability / 2:
                return False
            for lower in range(self.saturation_level, self.capacity):
                for upper in range(lower + 1, self.capacity + 1):
                    attempts, left, right = self.saturated_pair_witness(lower, upper)
                    if attempts < 1 or left <= 0 or right != 0:
                        return False
                    if upper - attempts < self.saturation_level:
                        return False
            return self.closed_class_count == self.saturation_level + 1 and self.open_exact_class_count == self.capacity + 1
        except (TypeError, ValueError, ZeroDivisionError):
            return False


def certify_stochastic_depletion_exposure(
    capacity: int,
    saturation_level: int,
    depletion_probability: object,
) -> StochasticDepletionExposureCertificate:
    certificate = StochasticDepletionExposureCertificate(
        capacity, saturation_level, Fraction(depletion_probability)
    )
    if not certificate.verify():
        raise ValueError("stochastic depletion exposure witness did not verify")
    return certificate


__all__ = [
    "CountState",
    "Increment",
    "Distribution",
    "StochasticGuildColonizationCertificate",
    "StochasticGuildCapacityFamilyCertificate",
    "StochasticDepletionExposureCertificate",
    "capped_summary",
    "certify_stochastic_guild_colonization",
    "certify_stochastic_capacity_family",
    "certify_stochastic_depletion_exposure",
]
