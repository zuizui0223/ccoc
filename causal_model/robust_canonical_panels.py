"""Robust distinguishing panels for finite canonical boundary blankets.

For a finite deterministic response table and a declared grammar, canonical
exterior response classes form the boundary blanket ``B``.  Each potential
observation/intervention cell ``(inside, word)`` distinguishes some pairs of
blanket classes.  The pairwise separation hypergraph has one hyperedge

    D_{b,b'} = {(i,w): Rbar(i,b,w) != Rbar(i,b',w)}

for every distinct blanket-class pair.

A panel is exact iff it hits every hyperedge.  It remains exact after arbitrary
loss of up to ``f`` independently lossable panel cells iff it hits every edge at
least ``f+1`` times.  Thus exact panels are transversals and loss-robust panels
are multicovers of the same hypergraph.

The module provides constructive failure certificates: when a panel is not
``f``-robust, it returns a concrete ambiguous class pair and the at-most-``f``
separating cells whose loss makes that pair collide.  It also provides a
disjoint-edge packing lower bound.  A robust candidate panel meeting that lower
bound is certified minimum without treating finite enumeration as the theorem
proof.

Distinct cells represent independently lossable declared observations or
interventions.  Repeated measurements are independent only when represented as
distinct cells in the response contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

from .canonical_boundary_blankets import (
    ExteriorLabels,
    FiniteBoundaryResponseTable,
    InsideState,
    Response,
    Word,
)

ObservationCell = tuple[InsideState, Word]
BlanketPair = tuple[int, int]


def _canonical_cells(
    system: FiniteBoundaryResponseTable,
    grammar: tuple[Word, ...],
    cells: Iterable[ObservationCell],
) -> tuple[ObservationCell, ...]:
    try:
        raw = tuple(cells)
    except TypeError as error:
        raise ValueError("panel cells must be an iterable of (inside, word) pairs") from error
    grammar_set = set(grammar)
    word_order = {word: index for index, word in enumerate(system.words)}
    normalized: list[ObservationCell] = []
    for cell in raw:
        if not isinstance(cell, tuple) or len(cell) != 2:
            raise ValueError("every panel cell must be a pair (inside, word)")
        inside, word = cell
        system.validate_inside(inside)
        if not isinstance(word, str) or word not in grammar_set:
            raise ValueError("panel cell word must belong to the declared grammar")
        normalized.append((inside, word))
    canonical = tuple(sorted(normalized, key=lambda cell: (cell[0], word_order[cell[1]])))
    if len(set(canonical)) != len(canonical):
        raise ValueError("panel cells must be unique")
    return canonical


def _full_cells(system: FiniteBoundaryResponseTable, grammar: tuple[Word, ...]) -> tuple[ObservationCell, ...]:
    return tuple((inside, word) for inside in system.inside_states for word in grammar)


def _validate_loss_budget(loss_budget: int) -> None:
    if not isinstance(loss_budget, int) or isinstance(loss_budget, bool) or loss_budget < 0:
        raise ValueError("loss_budget must be a non-negative integer")


def _validate_blanket_pair(pair: BlanketPair, class_count: int) -> None:
    if not isinstance(pair, tuple) or len(pair) != 2:
        raise ValueError("blanket pair must be a two-element tuple")
    left, right = pair
    if not isinstance(left, int) or isinstance(left, bool) or not isinstance(right, int) or isinstance(right, bool):
        raise ValueError("blanket pair labels must be integers")
    if not 0 <= left < class_count or not 0 <= right < class_count or left >= right:
        raise ValueError("blanket pair must contain ordered distinct valid labels")


@dataclass(frozen=True)
class CanonicalSeparationHypergraph:
    """Pairwise boundary-class separation sets over the full declared cell universe."""

    system: FiniteBoundaryResponseTable
    grammar: tuple[Word, ...]
    canonical_labels: ExteriorLabels
    class_representatives: tuple[int, ...]
    full_cells: tuple[ObservationCell, ...]
    separation_sets: tuple[tuple[BlanketPair, tuple[ObservationCell, ...]], ...]

    @property
    def class_count(self) -> int:
        return len(self.class_representatives)

    @property
    def pairs(self) -> tuple[BlanketPair, ...]:
        return tuple(pair for pair, _ in self.separation_sets)

    def separation_set(self, pair: BlanketPair) -> tuple[ObservationCell, ...]:
        _validate_blanket_pair(pair, self.class_count)
        for known_pair, cells in self.separation_sets:
            if known_pair == pair:
                return cells
        raise AssertionError("canonical pair is missing from separation hypergraph")

    def separation_count(self, panel: tuple[ObservationCell, ...], pair: BlanketPair) -> int:
        panel_set = set(panel)
        return len(panel_set.intersection(self.separation_set(pair)))

    def verify(self) -> bool:
        try:
            if not self.system.verify():
                return False
            grammar = self.system.normalize_grammar(self.grammar)
            if grammar != self.grammar:
                return False
            labels = self.system.exterior_labels(grammar)
            if labels != self.canonical_labels:
                return False
            class_count = len(set(labels))
            if class_count < 2:
                return False
            representatives: list[int] = []
            for label in range(class_count):
                matching = [exterior for exterior, observed_label in enumerate(labels) if observed_label == label]
                if not matching:
                    return False
                representatives.append(matching[0])
            if tuple(representatives) != self.class_representatives:
                return False
            full_cells = _full_cells(self.system, grammar)
            if full_cells != self.full_cells:
                return False
            expected_pairs = tuple(combinations(range(class_count), 2))
            if tuple(pair for pair, _ in self.separation_sets) != expected_pairs:
                return False
            for pair, cells in self.separation_sets:
                _validate_blanket_pair(pair, class_count)
                normalized = _canonical_cells(self.system, grammar, cells)
                if normalized != cells:
                    return False
                left_exterior = self.class_representatives[pair[0]]
                right_exterior = self.class_representatives[pair[1]]
                expected = tuple(
                    cell
                    for cell in full_cells
                    if self.system.response(cell[0], left_exterior, cell[1])
                    != self.system.response(cell[0], right_exterior, cell[1])
                )
                if cells != expected or not cells:
                    return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def build_canonical_separation_hypergraph(
    system: FiniteBoundaryResponseTable,
    grammar: Iterable[Word],
) -> CanonicalSeparationHypergraph:
    """Build the exact pairwise separation hypergraph of a nontrivial blanket."""
    if not system.verify():
        raise ValueError("system must be a valid finite response table")
    normalized_grammar = system.normalize_grammar(grammar)
    labels = system.exterior_labels(normalized_grammar)
    class_count = len(set(labels))
    if class_count < 2:
        raise ValueError("robust distinguishing panels require at least two canonical boundary classes")
    representatives = tuple(next(exterior for exterior, label in enumerate(labels) if label == target) for target in range(class_count))
    full_cells = _full_cells(system, normalized_grammar)
    separation_sets: list[tuple[BlanketPair, tuple[ObservationCell, ...]]] = []
    for pair in combinations(range(class_count), 2):
        left, right = representatives[pair[0]], representatives[pair[1]]
        cells = tuple(
            cell
            for cell in full_cells
            if system.response(cell[0], left, cell[1]) != system.response(cell[0], right, cell[1])
        )
        separation_sets.append((pair, cells))
    hypergraph = CanonicalSeparationHypergraph(
        system=system,
        grammar=normalized_grammar,
        canonical_labels=labels,
        class_representatives=representatives,
        full_cells=full_cells,
        separation_sets=tuple(separation_sets),
    )
    if not hypergraph.verify():
        raise AssertionError("canonical separation hypergraph did not verify")
    return hypergraph


@dataclass(frozen=True)
class CanonicalPanelProfile:
    """Exactness and failure tolerance of one declared panel."""

    hypergraph: CanonicalSeparationHypergraph
    panel: tuple[ObservationCell, ...]
    pairwise_separation_counts: tuple[tuple[BlanketPair, int], ...]
    minimum_pairwise_separation: int

    @property
    def is_exact(self) -> bool:
        return self.minimum_pairwise_separation >= 1

    @property
    def loss_tolerance(self) -> int:
        """Largest f for which this panel survives arbitrary loss of f cells.

        A value of -1 means that the panel is not exact before any loss.
        """
        return self.minimum_pairwise_separation - 1

    def count_for(self, pair: BlanketPair) -> int:
        _validate_blanket_pair(pair, self.hypergraph.class_count)
        for known_pair, count in self.pairwise_separation_counts:
            if pair == known_pair:
                return count
        raise AssertionError("canonical pair missing from panel profile")

    def survives_loss(self, loss_budget: int) -> bool:
        _validate_loss_budget(loss_budget)
        return self.minimum_pairwise_separation >= loss_budget + 1

    def verify(self) -> bool:
        try:
            if not self.hypergraph.verify():
                return False
            panel = _canonical_cells(self.hypergraph.system, self.hypergraph.grammar, self.panel)
            if panel != self.panel:
                return False
            expected = tuple(
                (pair, self.hypergraph.separation_count(panel, pair))
                for pair in self.hypergraph.pairs
            )
            if self.pairwise_separation_counts != expected:
                return False
            if self.minimum_pairwise_separation != min(count for _, count in expected):
                return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def analyze_canonical_panel(
    hypergraph: CanonicalSeparationHypergraph,
    panel: Iterable[ObservationCell],
) -> CanonicalPanelProfile:
    """Analyze exactness and the exact arbitrary-cell-loss tolerance of a panel."""
    if not hypergraph.verify():
        raise ValueError("hypergraph must be valid")
    normalized_panel = _canonical_cells(hypergraph.system, hypergraph.grammar, panel)
    counts = tuple(
        (pair, hypergraph.separation_count(normalized_panel, pair))
        for pair in hypergraph.pairs
    )
    profile = CanonicalPanelProfile(
        hypergraph=hypergraph,
        panel=normalized_panel,
        pairwise_separation_counts=counts,
        minimum_pairwise_separation=min(count for _, count in counts),
    )
    if not profile.verify():
        raise AssertionError("canonical panel profile did not verify")
    return profile


@dataclass(frozen=True)
class RobustCanonicalPanelCertificate:
    """Certificate that a panel remains exact after arbitrary loss of f cells."""

    profile: CanonicalPanelProfile
    loss_budget: int

    @property
    def required_separation_multiplicity(self) -> int:
        return self.loss_budget + 1

    def verify(self) -> bool:
        try:
            _validate_loss_budget(self.loss_budget)
            return self.profile.verify() and self.profile.survives_loss(self.loss_budget)
        except (TypeError, ValueError):
            return False


def certify_robust_canonical_panel(
    hypergraph: CanonicalSeparationHypergraph,
    panel: Iterable[ObservationCell],
    loss_budget: int,
) -> RobustCanonicalPanelCertificate:
    _validate_loss_budget(loss_budget)
    profile = analyze_canonical_panel(hypergraph, panel)
    certificate = RobustCanonicalPanelCertificate(profile=profile, loss_budget=loss_budget)
    if not certificate.verify():
        raise ValueError("panel does not distinguish every canonical class after the declared cell-loss budget")
    return certificate


@dataclass(frozen=True)
class DropoutAmbiguityCertificate:
    """Concrete at-most-f cell deletion producing a boundary-class collision."""

    profile: CanonicalPanelProfile
    loss_budget: int
    ambiguous_pair: BlanketPair
    removed_cells: tuple[ObservationCell, ...]
    retained_panel: tuple[ObservationCell, ...]

    def verify(self) -> bool:
        try:
            _validate_loss_budget(self.loss_budget)
            if not self.profile.verify() or self.profile.survives_loss(self.loss_budget):
                return False
            _validate_blanket_pair(self.ambiguous_pair, self.profile.hypergraph.class_count)
            expected_removed = tuple(
                cell
                for cell in self.profile.panel
                if cell in set(self.profile.hypergraph.separation_set(self.ambiguous_pair))
            )
            if self.removed_cells != expected_removed or len(self.removed_cells) > self.loss_budget:
                return False
            expected_retained = tuple(cell for cell in self.profile.panel if cell not in set(self.removed_cells))
            if self.retained_panel != expected_retained:
                return False
            left = self.profile.hypergraph.class_representatives[self.ambiguous_pair[0]]
            right = self.profile.hypergraph.class_representatives[self.ambiguous_pair[1]]
            return all(
                self.profile.hypergraph.system.response(inside, left, word)
                == self.profile.hypergraph.system.response(inside, right, word)
                for inside, word in self.retained_panel
            )
        except (AssertionError, TypeError, ValueError):
            return False


def certify_dropout_ambiguity(
    profile: CanonicalPanelProfile,
    loss_budget: int,
) -> DropoutAmbiguityCertificate:
    """Expose an explicit class collision when a panel lacks f-loss robustness."""
    _validate_loss_budget(loss_budget)
    if not profile.verify():
        raise ValueError("panel profile must be valid")
    failing_pair = next(pair for pair, count in profile.pairwise_separation_counts if count <= loss_budget)
    removed = tuple(cell for cell in profile.panel if cell in set(profile.hypergraph.separation_set(failing_pair)))
    certificate = DropoutAmbiguityCertificate(
        profile=profile,
        loss_budget=loss_budget,
        ambiguous_pair=failing_pair,
        removed_cells=removed,
        retained_panel=tuple(cell for cell in profile.panel if cell not in set(removed)),
    )
    if not certificate.verify():
        raise AssertionError("dropout ambiguity certificate did not verify")
    return certificate


@dataclass(frozen=True)
class DisjointSeparationPackingCertificate:
    """A disjoint hyperedge packing giving a robust-panel cardinality lower bound."""

    hypergraph: CanonicalSeparationHypergraph
    loss_budget: int
    packed_pairs: tuple[BlanketPair, ...]

    @property
    def lower_bound(self) -> int:
        return (self.loss_budget + 1) * len(self.packed_pairs)

    def verify(self) -> bool:
        try:
            if not self.hypergraph.verify():
                return False
            _validate_loss_budget(self.loss_budget)
            if tuple(sorted(set(self.packed_pairs))) != self.packed_pairs or not self.packed_pairs:
                return False
            seen_cells: set[ObservationCell] = set()
            for pair in self.packed_pairs:
                _validate_blanket_pair(pair, self.hypergraph.class_count)
                difference = set(self.hypergraph.separation_set(pair))
                if seen_cells.intersection(difference):
                    return False
                seen_cells.update(difference)
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_disjoint_separation_packing(
    hypergraph: CanonicalSeparationHypergraph,
    loss_budget: int,
    packed_pairs: Iterable[BlanketPair],
) -> DisjointSeparationPackingCertificate:
    _validate_loss_budget(loss_budget)
    try:
        pairs = tuple(packed_pairs)
    except TypeError as error:
        raise ValueError("packed_pairs must be an iterable of blanket pairs") from error
    certificate = DisjointSeparationPackingCertificate(
        hypergraph=hypergraph,
        loss_budget=loss_budget,
        packed_pairs=tuple(sorted(pairs)),
    )
    if not certificate.verify():
        raise ValueError("pairs are not a nonempty disjoint separation packing")
    return certificate


@dataclass(frozen=True)
class OptimalRobustPanelCertificate:
    """A matching robust upper and disjoint-packing lower bound proves optimality."""

    robust_panel: RobustCanonicalPanelCertificate
    packing: DisjointSeparationPackingCertificate

    @property
    def panel_size(self) -> int:
        return len(self.robust_panel.profile.panel)

    @property
    def optimum_size(self) -> int:
        return self.packing.lower_bound

    def verify(self) -> bool:
        try:
            return (
                self.robust_panel.verify()
                and self.packing.verify()
                and self.robust_panel.profile.hypergraph == self.packing.hypergraph
                and self.robust_panel.loss_budget == self.packing.loss_budget
                and self.panel_size == self.optimum_size
            )
        except (TypeError, ValueError):
            return False


def certify_optimal_robust_panel(
    robust_panel: RobustCanonicalPanelCertificate,
    packing: DisjointSeparationPackingCertificate,
) -> OptimalRobustPanelCertificate:
    certificate = OptimalRobustPanelCertificate(robust_panel=robust_panel, packing=packing)
    if not certificate.verify():
        raise ValueError("robust panel does not meet the disjoint-packing lower bound")
    return certificate


def private_bundle_response_table(replication: int) -> FiniteBoundaryResponseTable:
    """Four classes with three disjoint private separation bundles.

    For each replicate index j, words ``group:j``, ``left:j``, and ``right:j``
    distinguish respectively the pairs (0,2), (0,1), and (2,3).  The three
    selected pair separation sets are disjoint.  With r replicas, the full panel
    is optimally robust to r-1 arbitrary cell losses and needs exactly 3r cells.
    """
    if not isinstance(replication, int) or isinstance(replication, bool) or replication < 1:
        raise ValueError("replication must be a positive integer")
    words = (
        tuple(f"group:{index}" for index in range(replication))
        + tuple(f"left:{index}" for index in range(replication))
        + tuple(f"right:{index}" for index in range(replication))
    )
    response_patterns = (
        (0, 0, 0),  # exterior class 0
        (0, 1, 0),  # exterior class 1
        (1, 0, 0),  # exterior class 2
        (1, 0, 1),  # exterior class 3
    )
    exterior_rows: list[tuple[Response, ...]] = []
    for group_value, left_value, right_value in response_patterns:
        exterior_rows.append(
            (group_value,) * replication
            + (left_value,) * replication
            + (right_value,) * replication
        )
    return FiniteBoundaryResponseTable(
        inside_count=1,
        exterior_count=4,
        words=words,
        responses=(tuple(exterior_rows),),
    )


@dataclass(frozen=True)
class PrivateBundleOptimalityCertificate:
    """Closed-form optimal robust panel family with matching disjoint packing."""

    replication: int
    hypergraph: CanonicalSeparationHypergraph
    robust_panel: RobustCanonicalPanelCertificate
    packing: DisjointSeparationPackingCertificate
    optimality: OptimalRobustPanelCertificate

    @property
    def expected_panel_size(self) -> int:
        return 3 * self.replication

    @property
    def expected_loss_tolerance(self) -> int:
        return self.replication - 1

    def verify(self) -> bool:
        try:
            system = private_bundle_response_table(self.replication)
            return (
                self.hypergraph.verify()
                and self.hypergraph.system == system
                and self.robust_panel.verify()
                and self.packing.verify()
                and self.optimality.verify()
                and self.robust_panel.loss_budget == self.expected_loss_tolerance
                and self.robust_panel.profile.panel == self.hypergraph.full_cells
                and self.packing.packed_pairs == ((0, 1), (0, 2), (2, 3))
                and self.optimality.panel_size == self.expected_panel_size
                and self.optimality.optimum_size == self.expected_panel_size
            )
        except (TypeError, ValueError):
            return False


def certify_private_bundle_optimality(replication: int) -> PrivateBundleOptimalityCertificate:
    system = private_bundle_response_table(replication)
    hypergraph = build_canonical_separation_hypergraph(system, system.words)
    robust = certify_robust_canonical_panel(hypergraph, hypergraph.full_cells, replication - 1)
    packing = certify_disjoint_separation_packing(hypergraph, replication - 1, ((0, 1), (0, 2), (2, 3)))
    optimality = certify_optimal_robust_panel(robust, packing)
    certificate = PrivateBundleOptimalityCertificate(
        replication=replication,
        hypergraph=hypergraph,
        robust_panel=robust,
        packing=packing,
        optimality=optimality,
    )
    if not certificate.verify():
        raise AssertionError("private-bundle optimality certificate did not verify")
    return certificate
