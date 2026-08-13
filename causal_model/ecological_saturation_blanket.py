"""Exact ecological blankets from monotone guild colonization and saturation.

Exterior abundance is a finite guild-count vector n. Colonization actions add
non-negative guild increments. Responses saturate at thresholds L_g, giving the
candidate blanket z_g=min(L_g,n_g). Because colonization is monotone, the next
capped summary depends only on the current capped summary and the action. Thus
capped guild counts form an exact dynamic interface with prod(L_g+1) states,
independent of total guild capacities.

A one-guild opening of a depletion action marks the boundary: n=L and n=L+1 are
closed-equivalent under colonization but depletion separates them. Repeated
depletion makes all abundances 0,...,M distinguishable.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from math import log2, prod
from typing import Iterable
from .action_grammar_closure import (
    canonical_action_quotient_labels, find_action_descent_obstruction,
)
from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .grammar_aware_blankets import GrammarAwareDynamicInterfaceCertificate
from .shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem

CountState = tuple[int, ...]
Increment = tuple[int, ...]


def _capacities(values: Iterable[int]) -> tuple[int, ...]:
    out = tuple(values)
    if not out or any(not isinstance(x, int) or isinstance(x, bool) or x < 1 for x in out):
        raise ValueError("capacities must be positive integers")
    return out


def _levels(values: Iterable[int], capacities: tuple[int, ...]) -> tuple[int, ...]:
    out = tuple(values)
    if len(out) != len(capacities):
        raise ValueError("one saturation level per guild is required")
    if any(not isinstance(x, int) or isinstance(x, bool) or x < 1 for x in out):
        raise ValueError("saturation levels must be positive integers")
    if any(level > capacity for level, capacity in zip(out, capacities)):
        raise ValueError("saturation levels cannot exceed capacities")
    return out


def _increments(values: Iterable[Iterable[int]], guild_count: int) -> tuple[Increment, ...]:
    out = tuple(tuple(row) for row in values)
    if not out:
        raise ValueError("at least one colonization action is required")
    if any(len(row) != guild_count for row in out):
        raise ValueError("colonization increments must match guild count")
    if any(not isinstance(x, int) or isinstance(x, bool) or x < 0 for row in out for x in row):
        raise ValueError("colonization increments must be non-negative integers")
    if len(set(out)) != len(out):
        raise ValueError("colonization increments must be unique")
    return out


def capped_summary(state: CountState, levels: tuple[int, ...]) -> CountState:
    return tuple(min(level, abundance) for abundance, level in zip(state, levels))


@dataclass(frozen=True)
class GuildSaturationBlanketCertificate:
    capacities: tuple[int, ...]
    saturation_levels: tuple[int, ...]
    colonization_increments: tuple[Increment, ...]

    @property
    def count_states(self) -> tuple[CountState, ...]:
        return tuple(product(*(range(capacity + 1) for capacity in self.capacities)))

    @property
    def actions(self) -> tuple[str, ...]:
        return tuple(f"colonize:{i}" for i in range(len(self.colonization_increments)))

    @property
    def labels(self) -> tuple[CountState, ...]:
        return tuple(capped_summary(state, self.saturation_levels) for state in self.count_states)

    @property
    def blanket_state_count(self) -> int:
        return prod(level + 1 for level in self.saturation_levels)

    @property
    def blanket_memory_bits(self) -> float:
        return log2(self.blanket_state_count)

    @property
    def count_state_count(self) -> int:
        return prod(capacity + 1 for capacity in self.capacities)

    @property
    def system(self) -> FiniteControlledOutputSystem:
        states = self.count_states
        indices = {state: i for i, state in enumerate(states)}
        rows = []
        for state in states:
            row = []
            for increment in self.colonization_increments:
                successor = tuple(
                    min(capacity, abundance + delta)
                    for abundance, delta, capacity in zip(state, increment, self.capacities)
                )
                row.append(indices[successor])
            rows.append(tuple(row))
        return FiniteControlledOutputSystem(self.actions, tuple(rows), self.labels)

    @property
    def interface(self) -> GrammarAwareDynamicInterfaceCertificate:
        grammar = FinitePrefixGrammar(self.actions, (tuple(0 for _ in self.actions),))
        constrained = GrammarAwareControlledSystem(self.system, grammar)
        return GrammarAwareDynamicInterfaceCertificate(constrained, self.labels)

    def verify(self) -> bool:
        try:
            if _capacities(self.capacities) != self.capacities:
                return False
            if _levels(self.saturation_levels, self.capacities) != self.saturation_levels:
                return False
            if _increments(self.colonization_increments, len(self.capacities)) != self.colonization_increments:
                return False
            if len(set(self.labels)) != self.blanket_state_count:
                return False
            for state in self.count_states:
                z = capped_summary(state, self.saturation_levels)
                for delta in self.colonization_increments:
                    expected = tuple(min(level, capped + d) for capped, d, level in zip(z, delta, self.saturation_levels))
                    successor = tuple(min(capacity, abundance + d) for abundance, d, capacity in zip(state, delta, self.capacities))
                    if capped_summary(successor, self.saturation_levels) != expected:
                        return False
            return self.interface.verify()
        except (AssertionError, TypeError, ValueError):
            return False


def certify_guild_saturation_blanket(capacities: Iterable[int], saturation_levels: Iterable[int],
                                      colonization_increments: Iterable[Iterable[int]]) -> GuildSaturationBlanketCertificate:
    caps = _capacities(capacities)
    cert = GuildSaturationBlanketCertificate(
        caps, _levels(saturation_levels, caps), _increments(colonization_increments, len(caps)))
    if not cert.verify():
        raise AssertionError("guild saturation blanket did not verify")
    return cert


@dataclass(frozen=True)
class DepletionOpeningCertificate:
    capacity: int
    saturation_level: int

    @property
    def system(self) -> FiniteControlledOutputSystem:
        actions = ("colonize", "deplete")
        rows = tuple((min(self.capacity, n + 1), max(0, n - 1)) for n in range(self.capacity + 1))
        outputs = tuple(min(self.saturation_level, n) for n in range(self.capacity + 1))
        return FiniteControlledOutputSystem(actions, rows, outputs)

    @property
    def closed_labels(self) -> tuple[int, ...]:
        return canonical_action_quotient_labels(self.system, ("colonize",))

    @property
    def open_labels(self) -> tuple[int, ...]:
        return canonical_action_quotient_labels(self.system, ("colonize", "deplete"))

    @property
    def closed_block_count(self) -> int:
        return len(set(self.closed_labels))

    @property
    def open_block_count(self) -> int:
        return len(set(self.open_labels))

    @property
    def inflation_bits(self) -> float:
        return log2(self.open_block_count / self.closed_block_count)

    def verify(self) -> bool:
        try:
            if not isinstance(self.capacity, int) or isinstance(self.capacity, bool):
                return False
            if not isinstance(self.saturation_level, int) or isinstance(self.saturation_level, bool):
                return False
            if self.saturation_level < 1 or self.capacity < self.saturation_level + 1:
                return False
            if self.closed_block_count != self.saturation_level + 1:
                return False
            if self.open_block_count != self.capacity + 1:
                return False
            obstruction = find_action_descent_obstruction(
                self.system, ("colonize",), ("colonize", "deplete"))
            return obstruction is not None and obstruction.verify() and obstruction.newly_legal_action == "deplete"
        except (AssertionError, TypeError, ValueError):
            return False


def certify_depletion_opening(capacity: int, saturation_level: int) -> DepletionOpeningCertificate:
    cert = DepletionOpeningCertificate(capacity, saturation_level)
    if not cert.verify():
        raise ValueError("depletion opening witness does not verify")
    return cert


__all__ = ["CountState", "Increment", "GuildSaturationBlanketCertificate",
           "DepletionOpeningCertificate", "capped_summary",
           "certify_guild_saturation_blanket", "certify_depletion_opening"]
