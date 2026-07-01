"""Common-mode failure robustness for canonical distinguishing panels.

``robust_canonical_panels`` treats declared panel cells as independently
lossable.  This module replaces that assumption with an explicit finite family
of common-mode failure domains.  A mode may represent one camera, site, power
supply, observer, weather window, communication link, or seasonal opportunity
and can delete many nominally replicated cells together.

For a selected separator set ``S_P(b,b')`` and a mode family ``M``, define

    lambda_M(P;b,b')
      = min{|J| : S_P(b,b') subseteq union(M_j for j in J)}.

A panel survives every union of at most ``r`` declared modes exactly when every
blanket pair has mode-cover number at least ``r + 1``.  The construction gives a
concrete failure certificate whenever this condition is false.

Every panel cell must lie in at least one declared mode.  This is an intentional
contract: without it, a cell is outside the stated common-mode failure model and
mode-cover numbers would be undefined rather than evidence of real robustness.

Singleton modes recover the independent-cell theorem exactly.  Conversely, a
panel may have arbitrarily many separating cells and still have zero one-mode
robustness when all of them share one failure domain.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

from .canonical_boundary_blankets import FiniteBoundaryResponseTable, Response
from .robust_canonical_panels import (
    BlanketPair,
    CanonicalPanelProfile,
    CanonicalSeparationHypergraph,
    ObservationCell,
    analyze_canonical_panel,
    build_canonical_separation_hypergraph,
)


def _validate_mode_budget(mode_budget: int) -> None:
    if not isinstance(mode_budget, int) or isinstance(mode_budget, bool) or mode_budget < 0:
        raise ValueError("mode_budget must be a non-negative integer")


def _canonical_mode(mode: Iterable[ObservationCell], panel: tuple[ObservationCell, ...]) -> tuple[ObservationCell, ...]:
    panel_order = {cell: index for index, cell in enumerate(panel)}
    try:
        values = tuple(mode)
    except TypeError as error:
        raise ValueError("failure mode must be an iterable of panel cells") from error
    if not values:
        raise ValueError("failure modes must be nonempty")
    if any(cell not in panel_order for cell in values):
        raise ValueError("failure mode contains a cell outside the declared panel")
    canonical = tuple(sorted(values, key=panel_order.__getitem__))
    if len(set(canonical)) != len(canonical):
        raise ValueError("failure mode cells must be unique")
    return canonical


def _canonical_modes(
    modes: Iterable[Iterable[ObservationCell]],
    panel: tuple[ObservationCell, ...],
) -> tuple[tuple[ObservationCell, ...], ...]:
    try:
        raw = tuple(modes)
    except TypeError as error:
        raise ValueError("failure_modes must be an iterable of cell collections") from error
    if not raw:
        raise ValueError("at least one failure mode is required")
    normalized = tuple(_canonical_mode(mode, panel) for mode in raw)
    if len(set(normalized)) != len(normalized):
        raise ValueError("failure modes must be distinct")
    return normalized


def _all_subsets_of_size(mode_count: int, size: int) -> Iterable[tuple[int, ...]]:
    return combinations(range(mode_count), size)


@dataclass(frozen=True)
class FailureModeFamily:
    """Finite common-mode failure contract over a fixed canonical panel."""

    profile: CanonicalPanelProfile
    modes: tuple[tuple[ObservationCell, ...], ...]

    @property
    def mode_count(self) -> int:
        return len(self.modes)

    @property
    def panel_cell_coverage(self) -> tuple[int, ...]:
        return tuple(
            sum(cell in mode for mode in self.modes)
            for cell in self.profile.panel
        )

    def union_of_modes(self, mode_indices: Iterable[int]) -> tuple[ObservationCell, ...]:
        try:
            indices = tuple(mode_indices)
        except TypeError as error:
            raise ValueError("mode_indices must be iterable") from error
        if tuple(sorted(set(indices))) != indices:
            raise ValueError("mode_indices must be sorted and unique")
        if any(not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < self.mode_count for index in indices):
            raise ValueError("mode index is outside range")
        selected = set()
        for index in indices:
            selected.update(self.modes[index])
        return tuple(cell for cell in self.profile.panel if cell in selected)

    def selected_separators(self, pair: BlanketPair) -> tuple[ObservationCell, ...]:
        return tuple(
            cell
            for cell in self.profile.panel
            if cell in set(self.profile.hypergraph.separation_set(pair))
        )

    def mode_support(self, pair: BlanketPair) -> tuple[int, ...]:
        separators = set(self.selected_separators(pair))
        return tuple(index for index, mode in enumerate(self.modes) if separators.intersection(mode))

    def verify(self) -> bool:
        try:
            if not self.profile.verify():
                return False
            normalized = _canonical_modes(self.modes, self.profile.panel)
            if normalized != self.modes:
                return False
            # Every declared panel cell is governed by at least one possible mode.
            if any(count == 0 for count in self.panel_cell_coverage):
                return False
            return True
        except (TypeError, ValueError):
            return False


def build_failure_mode_family(
    profile: CanonicalPanelProfile,
    modes: Iterable[Iterable[ObservationCell]],
) -> FailureModeFamily:
    """Build a covered finite mode family over an exact or nonexact panel profile."""
    if not profile.verify():
        raise ValueError("panel profile must be valid")
    normalized = _canonical_modes(modes, profile.panel)
    family = FailureModeFamily(profile=profile, modes=normalized)
    if not family.verify():
        raise ValueError("every declared panel cell must belong to at least one failure mode")
    return family


@dataclass(frozen=True)
class ModeCoverCertificate:
    """A minimum common-mode cover of one pair's selected separators."""

    family: FailureModeFamily
    pair: BlanketPair
    selected_separators: tuple[ObservationCell, ...]
    cover_mode_indices: tuple[int, ...]
    mode_cover_number: int

    def verify(self) -> bool:
        try:
            if not self.family.verify():
                return False
            if self.pair not in self.family.profile.hypergraph.pairs:
                return False
            expected_separators = self.family.selected_separators(self.pair)
            if self.selected_separators != expected_separators or not self.selected_separators:
                return False
            if tuple(sorted(set(self.cover_mode_indices))) != self.cover_mode_indices:
                return False
            if self.mode_cover_number != len(self.cover_mode_indices):
                return False
            if self.mode_cover_number < 1 or self.mode_cover_number > self.family.mode_count:
                return False
            covered = set(self.family.union_of_modes(self.cover_mode_indices))
            if not set(self.selected_separators).issubset(covered):
                return False
            # Exhaustive subset check is certificate validation for the finite
            # declared mode contract, not the theorem proof.
            for size in range(self.mode_cover_number):
                for candidate in _all_subsets_of_size(self.family.mode_count, size):
                    if set(self.selected_separators).issubset(set(self.family.union_of_modes(candidate))):
                        return False
            return True
        except (TypeError, ValueError):
            return False


def certify_mode_cover(family: FailureModeFamily, pair: BlanketPair) -> ModeCoverCertificate:
    """Find and verify the minimum mode cover of one selected separation set."""
    if not family.verify():
        raise ValueError("failure mode family must be valid")
    if pair not in family.profile.hypergraph.pairs:
        raise ValueError("pair is outside the canonical separation hypergraph")
    separators = family.selected_separators(pair)
    if not separators:
        raise ValueError("panel has no selected separator for this blanket pair")
    cover: tuple[int, ...] | None = None
    for size in range(1, family.mode_count + 1):
        for candidate in _all_subsets_of_size(family.mode_count, size):
            if set(separators).issubset(set(family.union_of_modes(candidate))):
                cover = candidate
                break
        if cover is not None:
            break
    if cover is None:
        raise AssertionError("mode family claimed to cover every panel cell but did not cover separators")
    certificate = ModeCoverCertificate(
        family=family,
        pair=pair,
        selected_separators=separators,
        cover_mode_indices=cover,
        mode_cover_number=len(cover),
    )
    if not certificate.verify():
        raise AssertionError("mode cover certificate did not verify")
    return certificate


@dataclass(frozen=True)
class CommonModePanelProfile:
    """Exact common-mode tolerance of a panel under one declared failure family."""

    family: FailureModeFamily
    pairwise_mode_covers: tuple[ModeCoverCertificate, ...]
    minimum_mode_cover_number: int

    @property
    def is_exact(self) -> bool:
        return self.family.profile.is_exact

    @property
    def mode_tolerance(self) -> int:
        """Largest r for which arbitrary union of r declared modes preserves exactness."""
        return self.minimum_mode_cover_number - 1

    def cover_for(self, pair: BlanketPair) -> ModeCoverCertificate:
        for cover in self.pairwise_mode_covers:
            if cover.pair == pair:
                return cover
        raise AssertionError("canonical blanket pair missing from common-mode profile")

    def survives_mode_loss(self, mode_budget: int) -> bool:
        _validate_mode_budget(mode_budget)
        return self.is_exact and self.minimum_mode_cover_number >= mode_budget + 1

    def verify(self) -> bool:
        try:
            if not self.family.verify() or not self.family.profile.is_exact:
                return False
            expected_pairs = self.family.profile.hypergraph.pairs
            if tuple(cover.pair for cover in self.pairwise_mode_covers) != expected_pairs:
                return False
            if any(not cover.verify() or cover.family != self.family for cover in self.pairwise_mode_covers):
                return False
            expected_minimum = min(cover.mode_cover_number for cover in self.pairwise_mode_covers)
            return self.minimum_mode_cover_number == expected_minimum
        except (AssertionError, TypeError, ValueError):
            return False


def analyze_common_mode_panel(family: FailureModeFamily) -> CommonModePanelProfile:
    """Compute the exact common-mode loss tolerance of an exact panel."""
    if not family.verify():
        raise ValueError("failure mode family must be valid")
    if not family.profile.is_exact:
        raise ValueError("common-mode tolerance is defined only after the panel is exact before failure")
    covers = tuple(certify_mode_cover(family, pair) for pair in family.profile.hypergraph.pairs)
    profile = CommonModePanelProfile(
        family=family,
        pairwise_mode_covers=covers,
        minimum_mode_cover_number=min(cover.mode_cover_number for cover in covers),
    )
    if not profile.verify():
        raise AssertionError("common-mode panel profile did not verify")
    return profile


@dataclass(frozen=True)
class CommonModeRobustnessCertificate:
    """Certificate of exactness after arbitrary loss of up to r modes."""

    profile: CommonModePanelProfile
    mode_budget: int

    @property
    def required_mode_cover_number(self) -> int:
        return self.mode_budget + 1

    def verify(self) -> bool:
        try:
            _validate_mode_budget(self.mode_budget)
            return self.profile.verify() and self.profile.survives_mode_loss(self.mode_budget)
        except (TypeError, ValueError):
            return False


def certify_common_mode_robustness(
    family: FailureModeFamily,
    mode_budget: int,
) -> CommonModeRobustnessCertificate:
    _validate_mode_budget(mode_budget)
    profile = analyze_common_mode_panel(family)
    certificate = CommonModeRobustnessCertificate(profile=profile, mode_budget=mode_budget)
    if not certificate.verify():
        raise ValueError("panel does not remain exact after the declared common-mode failure budget")
    return certificate


@dataclass(frozen=True)
class CommonModeAmbiguityCertificate:
    """Concrete union of at-most-r modes that makes one blanket pair collide."""

    profile: CommonModePanelProfile
    mode_budget: int
    ambiguous_pair: BlanketPair
    removed_mode_indices: tuple[int, ...]
    removed_cells: tuple[ObservationCell, ...]
    retained_panel: tuple[ObservationCell, ...]

    def verify(self) -> bool:
        try:
            _validate_mode_budget(self.mode_budget)
            if not self.profile.verify() or self.profile.survives_mode_loss(self.mode_budget):
                return False
            cover = self.profile.cover_for(self.ambiguous_pair)
            if self.removed_mode_indices != cover.cover_mode_indices or len(self.removed_mode_indices) > self.mode_budget:
                return False
            expected_removed = self.profile.family.union_of_modes(self.removed_mode_indices)
            if self.removed_cells != expected_removed:
                return False
            expected_retained = tuple(cell for cell in self.profile.family.profile.panel if cell not in set(expected_removed))
            if self.retained_panel != expected_retained:
                return False
            left = self.profile.family.profile.hypergraph.class_representatives[self.ambiguous_pair[0]]
            right = self.profile.family.profile.hypergraph.class_representatives[self.ambiguous_pair[1]]
            return all(
                self.profile.family.profile.hypergraph.system.response(inside, left, word)
                == self.profile.family.profile.hypergraph.system.response(inside, right, word)
                for inside, word in self.retained_panel
            )
        except (AssertionError, TypeError, ValueError):
            return False


def certify_common_mode_ambiguity(
    profile: CommonModePanelProfile,
    mode_budget: int,
) -> CommonModeAmbiguityCertificate:
    """Return a minimum-mode destructive witness when r-mode robustness fails."""
    _validate_mode_budget(mode_budget)
    if not profile.verify():
        raise ValueError("common-mode profile must be valid")
    failing = next(cover for cover in profile.pairwise_mode_covers if cover.mode_cover_number <= mode_budget)
    removed = profile.family.union_of_modes(failing.cover_mode_indices)
    certificate = CommonModeAmbiguityCertificate(
        profile=profile,
        mode_budget=mode_budget,
        ambiguous_pair=failing.pair,
        removed_mode_indices=failing.cover_mode_indices,
        removed_cells=removed,
        retained_panel=tuple(cell for cell in profile.family.profile.panel if cell not in set(removed)),
    )
    if not certificate.verify():
        raise AssertionError("common-mode ambiguity certificate did not verify")
    return certificate


@dataclass(frozen=True)
class SingletonModeReductionCertificate:
    """Exact reduction of common-mode robustness to #70 for singleton modes."""

    independent_profile: CanonicalPanelProfile
    singleton_family: FailureModeFamily
    common_mode_profile: CommonModePanelProfile

    def verify(self) -> bool:
        try:
            if not self.independent_profile.verify() or not self.singleton_family.verify() or not self.common_mode_profile.verify():
                return False
            if self.singleton_family.profile != self.independent_profile or self.common_mode_profile.family != self.singleton_family:
                return False
            expected_modes = tuple((cell,) for cell in self.independent_profile.panel)
            if self.singleton_family.modes != expected_modes:
                return False
            return (
                self.common_mode_profile.mode_tolerance == self.independent_profile.loss_tolerance
                and all(
                    self.common_mode_profile.cover_for(pair).mode_cover_number
                    == self.independent_profile.count_for(pair)
                    for pair in self.independent_profile.hypergraph.pairs
                )
            )
        except (AssertionError, TypeError, ValueError):
            return False


def certify_singleton_mode_reduction(profile: CanonicalPanelProfile) -> SingletonModeReductionCertificate:
    if not profile.verify() or not profile.is_exact:
        raise ValueError("singleton reduction requires an exact canonical panel")
    family = build_failure_mode_family(profile, tuple((cell,) for cell in profile.panel))
    common = analyze_common_mode_panel(family)
    certificate = SingletonModeReductionCertificate(
        independent_profile=profile,
        singleton_family=family,
        common_mode_profile=common,
    )
    if not certificate.verify():
        raise AssertionError("singleton reduction certificate did not verify")
    return certificate


@dataclass(frozen=True)
class ModeDisjointPackingCertificate:
    """Mode-diversity lower bound from pairs with disjoint mode supports."""

    family: FailureModeFamily
    mode_budget: int
    packed_pairs: tuple[BlanketPair, ...]
    mode_supports: tuple[tuple[BlanketPair, tuple[int, ...]], ...]

    @property
    def required_mode_diversity_lower_bound(self) -> int:
        return (self.mode_budget + 1) * len(self.packed_pairs)

    def verify(self) -> bool:
        try:
            if not self.family.verify() or not self.family.profile.is_exact:
                return False
            _validate_mode_budget(self.mode_budget)
            if tuple(sorted(set(self.packed_pairs))) != self.packed_pairs or not self.packed_pairs:
                return False
            if tuple(pair for pair, _ in self.mode_supports) != self.packed_pairs:
                return False
            used: set[int] = set()
            for pair, support in self.mode_supports:
                if pair not in self.family.profile.hypergraph.pairs:
                    return False
                expected = self.family.mode_support(pair)
                if support != expected or not support:
                    return False
                if used.intersection(support):
                    return False
                used.update(support)
                # Any r-mode robust panel must have a cover number at least r+1.
                # This certificate records the necessary mode diversity for the
                # already selected separator family; it does not claim raw-cell
                # optimality for arbitrary overlapping designs.
                cover = certify_mode_cover(self.family, pair)
                if cover.mode_cover_number < self.mode_budget + 1:
                    return False
            return len(used) >= self.required_mode_diversity_lower_bound
        except (AssertionError, TypeError, ValueError):
            return False


def certify_mode_disjoint_packing(
    family: FailureModeFamily,
    mode_budget: int,
    packed_pairs: Iterable[BlanketPair],
) -> ModeDisjointPackingCertificate:
    _validate_mode_budget(mode_budget)
    if not family.verify() or not family.profile.is_exact:
        raise ValueError("mode-disjoint packing requires an exact panel and valid failure family")
    try:
        pairs = tuple(sorted(set(tuple(pair) for pair in packed_pairs)))
    except TypeError as error:
        raise ValueError("packed_pairs must be iterable blanket pairs") from error
    supports = tuple((pair, family.mode_support(pair)) for pair in pairs)
    certificate = ModeDisjointPackingCertificate(
        family=family,
        mode_budget=mode_budget,
        packed_pairs=pairs,
        mode_supports=supports,
    )
    if not certificate.verify():
        raise ValueError("pairs do not provide a valid mode-disjoint robustness packing")
    return certificate


def replicated_two_class_response_table(replication: int) -> FiniteBoundaryResponseTable:
    """Two classes with ``replication`` nominally redundant separating cells."""
    if not isinstance(replication, int) or isinstance(replication, bool) or replication < 1:
        raise ValueError("replication must be a positive integer")
    words = tuple(f"replicate:{index}" for index in range(replication))
    return FiniteBoundaryResponseTable(
        inside_count=1,
        exterior_count=2,
        words=words,
        responses=((tuple((0,) * replication), tuple((1,) * replication)),),
    )


@dataclass(frozen=True)
class CommonModeCollapseCertificate:
    """Arbitrarily many cells in one mode give no positive one-mode resilience."""

    replication: int
    hypergraph: CanonicalSeparationHypergraph
    independent_profile: CanonicalPanelProfile
    one_mode_family: FailureModeFamily
    common_profile: CommonModePanelProfile
    one_mode_failure: CommonModeAmbiguityCertificate

    def verify(self) -> bool:
        try:
            system = replicated_two_class_response_table(self.replication)
            return (
                self.hypergraph.verify()
                and self.hypergraph.system == system
                and self.independent_profile.verify()
                and self.independent_profile.hypergraph == self.hypergraph
                and self.independent_profile.loss_tolerance == self.replication - 1
                and self.one_mode_family.verify()
                and self.one_mode_family.modes == (self.independent_profile.panel,)
                and self.common_profile.verify()
                and self.common_profile.mode_tolerance == 0
                and self.one_mode_failure.verify()
                and self.one_mode_failure.mode_budget == 1
                and self.one_mode_failure.removed_mode_indices == (0,)
            )
        except (TypeError, ValueError):
            return False


def certify_common_mode_collapse(replication: int) -> CommonModeCollapseCertificate:
    system = replicated_two_class_response_table(replication)
    hypergraph = build_canonical_separation_hypergraph(system, system.words)
    independent = analyze_canonical_panel(hypergraph, hypergraph.full_cells)
    family = build_failure_mode_family(independent, (independent.panel,))
    common = analyze_common_mode_panel(family)
    failure = certify_common_mode_ambiguity(common, 1)
    certificate = CommonModeCollapseCertificate(
        replication=replication,
        hypergraph=hypergraph,
        independent_profile=independent,
        one_mode_family=family,
        common_profile=common,
        one_mode_failure=failure,
    )
    if not certificate.verify():
        raise AssertionError("common-mode collapse certificate did not verify")
    return certificate


def site_bundle_mode_family(
    site_count: int,
    replicates_per_site: int,
) -> tuple[CanonicalPanelProfile, FailureModeFamily]:
    """Two classes observed through sites, each with within-site repetitions.

    Every cell separates the two classes.  One mode corresponds to loss of one
    whole site, so robustness depends on site count rather than raw repetitions.
    """
    if not isinstance(site_count, int) or isinstance(site_count, bool) or site_count < 1:
        raise ValueError("site_count must be a positive integer")
    if not isinstance(replicates_per_site, int) or isinstance(replicates_per_site, bool) or replicates_per_site < 1:
        raise ValueError("replicates_per_site must be a positive integer")
    words = tuple(
        f"site:{site}:replicate:{replicate}"
        for site in range(site_count)
        for replicate in range(replicates_per_site)
    )
    system = FiniteBoundaryResponseTable(
        inside_count=1,
        exterior_count=2,
        words=words,
        responses=((tuple((0,) * len(words)), tuple((1,) * len(words))),),
    )
    hypergraph = build_canonical_separation_hypergraph(system, words)
    profile = analyze_canonical_panel(hypergraph, hypergraph.full_cells)
    modes = tuple(
        tuple((0, f"site:{site}:replicate:{replicate}") for replicate in range(replicates_per_site))
        for site in range(site_count)
    )
    family = build_failure_mode_family(profile, modes)
    return profile, family


@dataclass(frozen=True)
class SiteBundleResilienceCertificate:
    """Within-site repetition vs independent-site common-mode resilience."""

    site_count: int
    replicates_per_site: int
    independent_profile: CanonicalPanelProfile
    site_family: FailureModeFamily
    common_profile: CommonModePanelProfile

    @property
    def expected_independent_cell_tolerance(self) -> int:
        return self.site_count * self.replicates_per_site - 1

    @property
    def expected_site_mode_tolerance(self) -> int:
        return self.site_count - 1

    def verify(self) -> bool:
        try:
            expected_profile, expected_family = site_bundle_mode_family(self.site_count, self.replicates_per_site)
            return (
                self.independent_profile == expected_profile
                and self.site_family == expected_family
                and self.common_profile.verify()
                and self.common_profile.family == self.site_family
                and self.independent_profile.loss_tolerance == self.expected_independent_cell_tolerance
                and self.common_profile.mode_tolerance == self.expected_site_mode_tolerance
            )
        except (TypeError, ValueError):
            return False


def certify_site_bundle_resilience(site_count: int, replicates_per_site: int) -> SiteBundleResilienceCertificate:
    profile, family = site_bundle_mode_family(site_count, replicates_per_site)
    common = analyze_common_mode_panel(family)
    certificate = SiteBundleResilienceCertificate(
        site_count=site_count,
        replicates_per_site=replicates_per_site,
        independent_profile=profile,
        site_family=family,
        common_profile=common,
    )
    if not certificate.verify():
        raise AssertionError("site-bundle resilience certificate did not verify")
    return certificate
