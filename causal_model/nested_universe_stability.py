"""Nested candidate-universe stability audits for RACH.

RACH conclusions are conditional on a declared candidate universe. This module
does not pretend to prove that the universe contains nature. It instead makes
scope sensitivity explicit: analysts predeclare nested finite candidate universes
whose retained sets grow by inclusion, then keep only motif conclusions that
survive the outer envelope.

For non-empty nested retained sets, candidate-set expansion is monotone:

* an outer `INVARIANT` implies an inner `INVARIANT`;
* an outer `EXCLUDED` implies an inner `EXCLUDED`; and
* an inner `UNRESOLVED` implies an outer `UNRESOLVED`.

An inner decisive conclusion lost after expansion is scope-fragile, not thereby
proven false. The implementation is exact for explicit finite tiers; arbitrary
symbolic extensions need an external inclusion certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .admissibility import MotifStatus


@dataclass(frozen=True)
class FiniteUniverseTier:
    """One explicit, supported candidate universe across required cells.

    Candidate IDs shared by nested tiers denote the same candidate and must retain
    the same motif assignment. Every required retained set must be non-empty.
    Empty retained sets are ordinary RACH `UNSUPPORTED` cases and are deliberately
    outside this monotonicity theorem, avoiding vacuous universal statements.
    """

    tier_id: str
    motifs: tuple[str, ...]
    required_cell_ids: tuple[str, ...]
    candidate_motifs: Mapping[str, frozenset[str]]
    retained_by_cell: Mapping[str, frozenset[str]]
    description: str = ""

    def __post_init__(self) -> None:
        if not self.tier_id:
            raise ValueError("tier_id must be non-empty")
        if not self.motifs or len(set(self.motifs)) != len(self.motifs):
            raise ValueError("motifs must be a non-empty tuple of unique names")
        if any(not motif for motif in self.motifs):
            raise ValueError("motif names must be non-empty")
        if not self.required_cell_ids or len(set(self.required_cell_ids)) != len(self.required_cell_ids):
            raise ValueError("required_cell_ids must be non-empty and unique")
        if any(not cell for cell in self.required_cell_ids):
            raise ValueError("required cell IDs must be non-empty")
        if not self.candidate_motifs:
            raise ValueError("candidate_motifs must not be empty")
        motif_set = set(self.motifs)
        for candidate_id, active_motifs in self.candidate_motifs.items():
            if not candidate_id:
                raise ValueError("candidate IDs must be non-empty")
            if not set(active_motifs) <= motif_set:
                raise ValueError("candidate motif sets must use only declared motifs")
        if set(self.retained_by_cell) != set(self.required_cell_ids):
            raise ValueError("retained_by_cell must contain exactly the required cell IDs")
        candidates = set(self.candidate_motifs)
        for cell_id, retained in self.retained_by_cell.items():
            if not retained:
                raise ValueError("nested-universe stability requires non-empty retained sets")
            if not set(retained) <= candidates:
                raise ValueError(f"retained set for {cell_id!r} contains undeclared candidates")

    def cell_status(self, cell_id: str, motif: str) -> MotifStatus:
        if cell_id not in self.retained_by_cell:
            raise ValueError(f"unknown required cell: {cell_id!r}")
        if motif not in self.motifs:
            raise ValueError(f"unknown motif: {motif!r}")
        retained = self.retained_by_cell[cell_id]
        active = {candidate_id for candidate_id in retained if motif in self.candidate_motifs[candidate_id]}
        if len(active) == len(retained):
            return MotifStatus.INVARIANT
        if not active:
            return MotifStatus.EXCLUDED
        return MotifStatus.UNRESOLVED

    def motif_status(self, motif: str) -> MotifStatus:
        statuses = tuple(self.cell_status(cell_id, motif) for cell_id in self.required_cell_ids)
        if all(status is MotifStatus.INVARIANT for status in statuses):
            return MotifStatus.INVARIANT
        if all(status is MotifStatus.EXCLUDED for status in statuses):
            return MotifStatus.EXCLUDED
        return MotifStatus.UNRESOLVED

    @property
    def statuses(self) -> Mapping[str, MotifStatus]:
        return {motif: self.motif_status(motif) for motif in self.motifs}


@dataclass(frozen=True)
class UniverseExtensionTransition:
    """One validated nested-universe transition and its motif-wise statuses."""

    inner_tier_id: str
    outer_tier_id: str
    inner_statuses: Mapping[str, MotifStatus]
    outer_statuses: Mapping[str, MotifStatus]

    def preserves_decisive_outer_claim(self, motif: str) -> bool:
        """Whether a decisive outer claim has the same status in the inner tier."""

        outer = self.outer_statuses[motif]
        return outer in (MotifStatus.INVARIANT, MotifStatus.EXCLUDED) and self.inner_statuses[motif] is outer

    def inner_decision_is_fragile(self, motif: str) -> bool:
        """Whether an inner decisive claim fails to survive this declared expansion."""

        inner = self.inner_statuses[motif]
        return inner in (MotifStatus.INVARIANT, MotifStatus.EXCLUDED) and self.outer_statuses[motif] is not inner


@dataclass(frozen=True)
class NestedUniverseStabilityReport:
    """Classification trace over a validated nested chain of finite universes."""

    tier_statuses: Mapping[str, Mapping[str, MotifStatus]]
    transitions: tuple[UniverseExtensionTransition, ...]
    outermost_tier_id: str
    outermost_statuses: Mapping[str, MotifStatus]
    extension_stable_motifs: tuple[str, ...]
    scope_fragile_motifs: tuple[str, ...]


def _validate_extension(inner: FiniteUniverseTier, outer: FiniteUniverseTier) -> None:
    if inner.motifs != outer.motifs:
        raise ValueError("nested tiers must use identical ordered motif vocabularies")
    if inner.required_cell_ids != outer.required_cell_ids:
        raise ValueError("nested tiers must use identical ordered required cell IDs")
    if not set(inner.candidate_motifs) <= set(outer.candidate_motifs):
        raise ValueError("outer candidate universe must contain every inner candidate ID")
    for candidate_id, inner_motifs in inner.candidate_motifs.items():
        if outer.candidate_motifs[candidate_id] != inner_motifs:
            raise ValueError("shared candidate IDs must preserve their declared motif sets across tiers")
    for cell_id in inner.required_cell_ids:
        if not set(inner.retained_by_cell[cell_id]) <= set(outer.retained_by_cell[cell_id]):
            raise ValueError("outer retained sets must contain the corresponding inner retained sets")


def _assert_monotonicity(inner: FiniteUniverseTier, outer: FiniteUniverseTier) -> UniverseExtensionTransition:
    """Construct a transition and fail only if the deterministic theorem is violated."""

    _validate_extension(inner, outer)
    inner_statuses = inner.statuses
    outer_statuses = outer.statuses
    for motif in inner.motifs:
        if outer_statuses[motif] is MotifStatus.INVARIANT and inner_statuses[motif] is not MotifStatus.INVARIANT:
            raise RuntimeError("outer invariant failed nested-universe monotonicity")
        if outer_statuses[motif] is MotifStatus.EXCLUDED and inner_statuses[motif] is not MotifStatus.EXCLUDED:
            raise RuntimeError("outer excluded failed nested-universe monotonicity")
        if inner_statuses[motif] is MotifStatus.UNRESOLVED and outer_statuses[motif] is not MotifStatus.UNRESOLVED:
            raise RuntimeError("inner unresolved failed nested-universe monotonicity")
    return UniverseExtensionTransition(
        inner_tier_id=inner.tier_id,
        outer_tier_id=outer.tier_id,
        inner_statuses=inner_statuses,
        outer_statuses=outer_statuses,
    )


def audit_nested_universe_stability(
    tiers: Iterable[FiniteUniverseTier],
) -> NestedUniverseStabilityReport:
    """Classify a nested chain and retain only outer-envelope decisive conclusions.

    The first tier is the narrowest declared universe and the last is the widest
    declared outer envelope. A motif is extension-stable exactly when the
    outermost tier reports `INVARIANT` or `EXCLUDED`; the monotonicity theorem then
    guarantees the same status at every inner tier.

    A motif is scope-fragile when some narrower tier is decisive but the outermost
    envelope does not preserve that same status. This diagnoses declared-model
    sensitivity without treating the narrower model as falsified.
    """

    tier_tuple = tuple(tiers)
    if len(tier_tuple) < 2:
        raise ValueError("nested-universe stability requires at least two tiers")
    if len({tier.tier_id for tier in tier_tuple}) != len(tier_tuple):
        raise ValueError("nested universe tier IDs must be unique")
    transitions = tuple(
        _assert_monotonicity(inner, outer)
        for inner, outer in zip(tier_tuple, tier_tuple[1:])
    )
    outer = tier_tuple[-1]
    outer_statuses = outer.statuses
    stable = tuple(
        motif
        for motif, status in outer_statuses.items()
        if status in (MotifStatus.INVARIANT, MotifStatus.EXCLUDED)
    )
    fragile = tuple(
        motif
        for motif in outer.motifs
        if any(
            tier.statuses[motif] in (MotifStatus.INVARIANT, MotifStatus.EXCLUDED)
            and tier.statuses[motif] is not outer_statuses[motif]
            for tier in tier_tuple[:-1]
        )
    )
    return NestedUniverseStabilityReport(
        tier_statuses={tier.tier_id: tier.statuses for tier in tier_tuple},
        transitions=transitions,
        outermost_tier_id=outer.tier_id,
        outermost_statuses=outer_statuses,
        extension_stable_motifs=stable,
        scope_fragile_motifs=fragile,
    )
