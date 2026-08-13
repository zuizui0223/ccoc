"""One saturated guild macro-law shared across changing abundance capacities.

For fixed guild thresholds and fixed non-negative colonization increments, the
capped-summary transition z -> min(L,z+d) is independent of the underlying
capacity vector M as long as M_g>=L_g. Hence count-state systems with different
semantic domains share one exact macro-law and one fixed memory bound.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from math import log2, prod
from typing import Iterable
from .ecological_saturation_blanket import (
    CountState, GuildSaturationBlanketCertificate,
    certify_guild_saturation_blanket,
)


def _capacity_family(values: Iterable[Iterable[int]]) -> tuple[tuple[int, ...], ...]:
    family = tuple(tuple(row) for row in values)
    if not family:
        raise ValueError("at least one capacity vector is required")
    guild_count = len(family[0])
    if guild_count < 1 or any(len(row) != guild_count for row in family):
        raise ValueError("capacity vectors must have one common positive guild count")
    if any(not isinstance(x, int) or isinstance(x, bool) or x < 1 for row in family for x in row):
        raise ValueError("capacities must be positive integers")
    return family


@dataclass(frozen=True)
class GuildCapacityFamilyPortabilityCertificate:
    capacities_by_stage: tuple[tuple[int, ...], ...]
    saturation_levels: tuple[int, ...]
    colonization_increments: tuple[tuple[int, ...], ...]

    @property
    def guild_count(self) -> int:
        return len(self.saturation_levels)

    @property
    def macro_states(self) -> tuple[CountState, ...]:
        return tuple(product(*(range(level + 1) for level in self.saturation_levels)))

    @property
    def macro_state_count(self) -> int:
        return prod(level + 1 for level in self.saturation_levels)

    @property
    def macro_memory_bits(self) -> float:
        return log2(self.macro_state_count)

    @property
    def stage_certificates(self) -> tuple[GuildSaturationBlanketCertificate, ...]:
        return tuple(
            certify_guild_saturation_blanket(
                capacities, self.saturation_levels, self.colonization_increments)
            for capacities in self.capacities_by_stage
        )

    @property
    def stage_count_state_counts(self) -> tuple[int, ...]:
        return tuple(certificate.count_state_count for certificate in self.stage_certificates)

    def macro_successor(self, state: CountState, action_index: int) -> CountState:
        if state not in self.macro_states:
            raise ValueError("state is outside the shared capped macro-domain")
        if not isinstance(action_index, int) or isinstance(action_index, bool) or not 0 <= action_index < len(self.colonization_increments):
            raise ValueError("action_index is outside the colonization action set")
        increment = self.colonization_increments[action_index]
        return tuple(
            min(level, abundance + delta)
            for abundance, delta, level in zip(state, increment, self.saturation_levels)
        )

    def verify(self) -> bool:
        try:
            family = _capacity_family(self.capacities_by_stage)
            if family != self.capacities_by_stage:
                return False
            if len(self.saturation_levels) != len(family[0]):
                return False
            if any(not isinstance(level, int) or isinstance(level, bool) or level < 1 for level in self.saturation_levels):
                return False
            if any(
                capacity < level
                for capacities in family
                for capacity, level in zip(capacities, self.saturation_levels)
            ):
                return False
            if not self.colonization_increments:
                return False
            stages = self.stage_certificates
            if any(not stage.verify() for stage in stages):
                return False
            if any(stage.blanket_state_count != self.macro_state_count for stage in stages):
                return False
            if any(stage.blanket_memory_bits != self.macro_memory_bits for stage in stages):
                return False

            # The shared macro transition is capacity-free. Cache each finite
            # realization once, then compare all of its capped transitions with
            # the single shared macro law.
            for stage in stages:
                system = stage.system
                labels = stage.labels
                actions = stage.actions
                for state_index, label in enumerate(labels):
                    for action_index, action in enumerate(actions):
                        successor_index = system.transition(state_index, action)
                        successor_label = labels[successor_index]
                        if successor_label != self.macro_successor(label, action_index):
                            return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_guild_capacity_family_portability(
    capacities_by_stage: Iterable[Iterable[int]],
    saturation_levels: Iterable[int],
    colonization_increments: Iterable[Iterable[int]],
) -> GuildCapacityFamilyPortabilityCertificate:
    family = _capacity_family(capacities_by_stage)
    certificate = GuildCapacityFamilyPortabilityCertificate(
        capacities_by_stage=family,
        saturation_levels=tuple(saturation_levels),
        colonization_increments=tuple(tuple(row) for row in colonization_increments),
    )
    if not certificate.verify():
        raise ValueError("capacity family does not realize one saturated guild macro-law")
    return certificate


__all__ = [
    "GuildCapacityFamilyPortabilityCertificate",
    "certify_guild_capacity_family_portability",
]
