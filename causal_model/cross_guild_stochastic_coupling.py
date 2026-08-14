"""Hidden cross-guild coupling as an exact/approximate portability boundary.

Two guild abundances A and B are capped at response thresholds L_A and L_B.  A
controlled B-recruitment action leaves A unchanged and increments B by one with a
probability p(A).  Below L_A the capped state identifies A exactly.  Above L_A,
all abundances share one capped A label, so exact capped-state lumpability holds
iff p(A) is constant on the saturated A tail.

If the saturated hazard range has diameter delta, the midpoint hazard gives the
minimax common Bernoulli transition for that capped fiber.  Its worst one-step TV
error is exactly delta/2.  Repeated-action path TV is at most
1-(1-delta/2)^H by stepwise maximal coupling.  Across changing capacities, the
same statement holds with delta equal to the global saturated-tail hazard range,
provided the below-threshold hazards agree across systems.

The Bernoulli/TV minimax calculation and coupling bound are classical substrate.
The CCOC contribution is the ecological portability interpretation: hidden
oversaturation is harmless exactly when it cannot modulate response-relevant
cross-guild dynamics, and bounded hidden modulation yields a capacity-independent
approximate macro law.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Iterable

MacroState = tuple[int, int]
MicroState = tuple[int, int]
KernelRow = tuple[Fraction, ...]


def _positive_integer(value: int, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _probability(value: object, name: str = "probability") -> Fraction:
    try:
        probability = Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{name} must be rational-like") from error
    if not Fraction(0, 1) <= probability <= Fraction(1, 1):
        raise ValueError(f"{name} must lie in [0,1]")
    return probability


def _hazard_vector(values: Iterable[object], capacity_a: int) -> tuple[Fraction, ...]:
    hazards = tuple(_probability(value, "hazard") for value in values)
    if len(hazards) != capacity_a + 1:
        raise ValueError("hazard vector must contain one probability for every A abundance")
    return hazards


def _tv(left: KernelRow, right: KernelRow) -> Fraction:
    if len(left) != len(right):
        raise ValueError("kernel rows must have the same finite domain")
    return sum((abs(a - b) for a, b in zip(left, right)), Fraction(0, 1)) / 2


@dataclass(frozen=True)
class CrossGuildCouplingCertificate:
    """One two-guild capacity domain with hidden A -> B recruitment coupling."""

    capacity_a: int
    capacity_b: int
    threshold_a: int
    threshold_b: int
    recruitment_hazards_by_a: tuple[Fraction, ...]

    @property
    def macro_states(self) -> tuple[MacroState, ...]:
        return tuple(product(range(self.threshold_a + 1), range(self.threshold_b + 1)))

    @property
    def micro_states(self) -> tuple[MicroState, ...]:
        return tuple(product(range(self.capacity_a + 1), range(self.capacity_b + 1)))

    @property
    def macro_state_count(self) -> int:
        return (self.threshold_a + 1) * (self.threshold_b + 1)

    def capped_state(self, micro_state: MicroState) -> MacroState:
        a, b = micro_state
        if not 0 <= a <= self.capacity_a or not 0 <= b <= self.capacity_b:
            raise ValueError("micro_state is outside the abundance domain")
        return min(self.threshold_a, a), min(self.threshold_b, b)

    @property
    def saturated_hazards(self) -> tuple[Fraction, ...]:
        return self.recruitment_hazards_by_a[self.threshold_a :]

    @property
    def saturated_hazard_min(self) -> Fraction:
        return min(self.saturated_hazards)

    @property
    def saturated_hazard_max(self) -> Fraction:
        return max(self.saturated_hazards)

    @property
    def saturated_hazard_diameter(self) -> Fraction:
        return self.saturated_hazard_max - self.saturated_hazard_min

    @property
    def minimax_saturated_hazard(self) -> Fraction:
        return (self.saturated_hazard_min + self.saturated_hazard_max) / 2

    @property
    def exact_capped_lumpable(self) -> bool:
        return self.saturated_hazard_diameter == 0

    @property
    def minimax_one_step_tv_error(self) -> Fraction:
        return self.saturated_hazard_diameter / 2

    def micro_kernel_row(self, micro_state: MicroState) -> KernelRow:
        a, b = micro_state
        macro = self.capped_state(micro_state)
        hazard = self.recruitment_hazards_by_a[a]
        no_recruit = macro
        recruited_micro = (a, min(self.capacity_b, b + 1))
        recruit = self.capped_state(recruited_micro)
        masses: dict[MacroState, Fraction] = defaultdict(Fraction)
        masses[no_recruit] += 1 - hazard
        masses[recruit] += hazard
        return tuple(masses[state] for state in self.macro_states)

    def macro_hazard(self, macro_state: MacroState) -> Fraction:
        a_cap, b_cap = macro_state
        if macro_state not in self.macro_states:
            raise ValueError("macro_state is outside capped domain")
        if b_cap == self.threshold_b:
            # The macro transition is a self-loop regardless of the hidden hazard.
            return Fraction(0, 1)
        if a_cap < self.threshold_a:
            return self.recruitment_hazards_by_a[a_cap]
        return self.minimax_saturated_hazard

    def approximate_macro_row(self, macro_state: MacroState) -> KernelRow:
        if macro_state not in self.macro_states:
            raise ValueError("macro_state is outside capped domain")
        a_cap, b_cap = macro_state
        hazard = self.macro_hazard(macro_state)
        masses: dict[MacroState, Fraction] = defaultdict(Fraction)
        masses[macro_state] += 1 - hazard
        successor = (a_cap, min(self.threshold_b, b_cap + 1))
        masses[successor] += hazard
        return tuple(masses[state] for state in self.macro_states)

    def micro_to_approximate_one_step_tv(self, micro_state: MicroState) -> Fraction:
        macro = self.capped_state(micro_state)
        return _tv(self.micro_kernel_row(micro_state), self.approximate_macro_row(macro))

    def exact_obstruction_pair(self) -> tuple[MicroState, MicroState] | None:
        if self.exact_capped_lumpable:
            return None
        min_a = next(
            a
            for a in range(self.threshold_a, self.capacity_a + 1)
            if self.recruitment_hazards_by_a[a] == self.saturated_hazard_min
        )
        max_a = next(
            a
            for a in range(self.threshold_a, self.capacity_a + 1)
            if self.recruitment_hazards_by_a[a] == self.saturated_hazard_max
        )
        b = self.threshold_b - 1
        return (min_a, b), (max_a, b)

    @property
    def obstruction_one_step_tv(self) -> Fraction:
        pair = self.exact_obstruction_pair()
        if pair is None:
            return Fraction(0, 1)
        return _tv(self.micro_kernel_row(pair[0]), self.micro_kernel_row(pair[1]))

    def horizon_path_tv_upper_bound(self, steps: int) -> Fraction:
        if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
            raise ValueError("steps must be a non-negative integer")
        epsilon = self.minimax_one_step_tv_error
        return 1 - (1 - epsilon) ** steps

    def verify(self) -> bool:
        try:
            _positive_integer(self.capacity_a, "capacity_a")
            _positive_integer(self.capacity_b, "capacity_b")
            _positive_integer(self.threshold_a, "threshold_a")
            _positive_integer(self.threshold_b, "threshold_b")
            if self.threshold_a > self.capacity_a or self.threshold_b > self.capacity_b:
                return False
            if _hazard_vector(self.recruitment_hazards_by_a, self.capacity_a) != self.recruitment_hazards_by_a:
                return False
            if len(self.macro_states) != self.macro_state_count:
                return False

            actual_worst = max(
                self.micro_to_approximate_one_step_tv(state)
                for state in self.micro_states
            )
            if actual_worst != self.minimax_one_step_tv_error:
                return False

            # Exact lumpability is equivalent to zero hidden-tail diameter.
            rows_by_macro: dict[MacroState, set[KernelRow]] = defaultdict(set)
            for state in self.micro_states:
                rows_by_macro[self.capped_state(state)].add(self.micro_kernel_row(state))
            actual_exact = all(len(rows) == 1 for rows in rows_by_macro.values())
            if actual_exact != self.exact_capped_lumpable:
                return False

            if self.obstruction_one_step_tv != self.saturated_hazard_diameter:
                return False
            if self.horizon_path_tv_upper_bound(0) != 0:
                return False
            if self.horizon_path_tv_upper_bound(1) != self.minimax_one_step_tv_error:
                return False
            return True
        except (AssertionError, TypeError, ValueError, ZeroDivisionError):
            return False


def certify_cross_guild_coupling(
    capacity_a: int,
    capacity_b: int,
    threshold_a: int,
    threshold_b: int,
    recruitment_hazards_by_a: Iterable[object],
) -> CrossGuildCouplingCertificate:
    certificate = CrossGuildCouplingCertificate(
        capacity_a=_positive_integer(capacity_a, "capacity_a"),
        capacity_b=_positive_integer(capacity_b, "capacity_b"),
        threshold_a=_positive_integer(threshold_a, "threshold_a"),
        threshold_b=_positive_integer(threshold_b, "threshold_b"),
        recruitment_hazards_by_a=_hazard_vector(recruitment_hazards_by_a, capacity_a),
    )
    if not certificate.verify():
        raise ValueError("cross-guild coupling certificate did not verify")
    return certificate


@dataclass(frozen=True)
class CrossGuildCapacityFamilyCertificate:
    """One approximate cross-guild macro law shared across changing capacities."""

    stages: tuple[CrossGuildCouplingCertificate, ...]

    @property
    def threshold_a(self) -> int:
        return self.stages[0].threshold_a

    @property
    def threshold_b(self) -> int:
        return self.stages[0].threshold_b

    @property
    def macro_state_count(self) -> int:
        return self.stages[0].macro_state_count

    @property
    def common_below_threshold_hazards(self) -> tuple[Fraction, ...]:
        return self.stages[0].recruitment_hazards_by_a[: self.threshold_a]

    @property
    def global_saturated_hazard_min(self) -> Fraction:
        return min(stage.saturated_hazard_min for stage in self.stages)

    @property
    def global_saturated_hazard_max(self) -> Fraction:
        return max(stage.saturated_hazard_max for stage in self.stages)

    @property
    def global_saturated_hazard_diameter(self) -> Fraction:
        return self.global_saturated_hazard_max - self.global_saturated_hazard_min

    @property
    def common_saturated_hazard(self) -> Fraction:
        return (self.global_saturated_hazard_min + self.global_saturated_hazard_max) / 2

    @property
    def minimax_one_step_tv_error(self) -> Fraction:
        return self.global_saturated_hazard_diameter / 2

    @property
    def exact_common_macro_exists(self) -> bool:
        return self.global_saturated_hazard_diameter == 0

    def common_macro_hazard(self, macro_state: MacroState) -> Fraction:
        a_cap, b_cap = macro_state
        if macro_state not in self.stages[0].macro_states:
            raise ValueError("macro_state outside common capped domain")
        if b_cap == self.threshold_b:
            return Fraction(0, 1)
        if a_cap < self.threshold_a:
            return self.common_below_threshold_hazards[a_cap]
        return self.common_saturated_hazard

    def common_macro_row(self, macro_state: MacroState) -> KernelRow:
        states = self.stages[0].macro_states
        a_cap, b_cap = macro_state
        hazard = self.common_macro_hazard(macro_state)
        masses: dict[MacroState, Fraction] = defaultdict(Fraction)
        masses[macro_state] += 1 - hazard
        masses[(a_cap, min(self.threshold_b, b_cap + 1))] += hazard
        return tuple(masses[state] for state in states)

    def stage_micro_tv(self, stage_index: int, micro_state: MicroState) -> Fraction:
        stage = self.stages[stage_index]
        macro = stage.capped_state(micro_state)
        return _tv(stage.micro_kernel_row(micro_state), self.common_macro_row(macro))

    def horizon_path_tv_upper_bound(self, steps: int) -> Fraction:
        if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
            raise ValueError("steps must be a non-negative integer")
        epsilon = self.minimax_one_step_tv_error
        return 1 - (1 - epsilon) ** steps

    def verify(self) -> bool:
        try:
            if not self.stages or any(not stage.verify() for stage in self.stages):
                return False
            first = self.stages[0]
            for stage in self.stages[1:]:
                if stage.threshold_a != first.threshold_a or stage.threshold_b != first.threshold_b:
                    return False
                if stage.recruitment_hazards_by_a[: self.threshold_a] != self.common_below_threshold_hazards:
                    return False
                if stage.macro_states != first.macro_states:
                    return False

            actual_worst = max(
                self.stage_micro_tv(stage_index, micro_state)
                for stage_index, stage in enumerate(self.stages)
                for micro_state in stage.micro_states
            )
            if actual_worst != self.minimax_one_step_tv_error:
                return False
            if self.horizon_path_tv_upper_bound(1) != self.minimax_one_step_tv_error:
                return False
            return True
        except (AssertionError, IndexError, TypeError, ValueError, ZeroDivisionError):
            return False


def certify_cross_guild_capacity_family(
    capacities_by_stage: Iterable[tuple[int, int]],
    threshold_a: int,
    threshold_b: int,
    hazards_by_stage: Iterable[Iterable[object]],
) -> CrossGuildCapacityFamilyCertificate:
    capacities = tuple(tuple(pair) for pair in capacities_by_stage)
    hazards = tuple(tuple(row) for row in hazards_by_stage)
    if not capacities or len(capacities) != len(hazards):
        raise ValueError("one hazard vector is required per capacity stage")
    if any(len(pair) != 2 for pair in capacities):
        raise ValueError("each capacity stage must contain (capacity_a, capacity_b)")
    stages = tuple(
        certify_cross_guild_coupling(
            capacity_a=pair[0],
            capacity_b=pair[1],
            threshold_a=threshold_a,
            threshold_b=threshold_b,
            recruitment_hazards_by_a=row,
        )
        for pair, row in zip(capacities, hazards)
    )
    certificate = CrossGuildCapacityFamilyCertificate(stages)
    if not certificate.verify():
        raise ValueError("cross-guild capacity family does not share one approximate macro contract")
    return certificate


__all__ = [
    "CrossGuildCouplingCertificate",
    "CrossGuildCapacityFamilyCertificate",
    "certify_cross_guild_coupling",
    "certify_cross_guild_capacity_family",
]
