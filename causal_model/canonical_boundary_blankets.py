"""Canonical minimal boundary blankets for finite deterministic response systems.

Let ``I`` be finite window states, ``E`` finite exterior completions, ``Gamma`` a
declared grammar of boundary words, and ``R(i, e, w)`` the deterministic window
response.  Exterior completions are response-equivalent when no allowed word,
from any inside state, distinguishes them:

    e ~_Gamma e' iff R(i,e,w)=R(i,e',w) for every i in I and w in Gamma.

The quotient ``B_Gamma = E / ~_Gamma`` is the canonical boundary blanket.  It is
sound by construction and is coarsest among all exact exterior summaries: any
summary through which responses factor must refine this quotient.

For nested grammars, exterior partitions only refine.  The accompanying proof
document establishes that a finite exact blanket over a union grammar exists iff
the finite-level quotient sizes are uniformly bounded; then the partitions
stabilize.  This module provides finite certificates and canonical witnesses. It
does not claim that a finite replay can certify an unbounded empirical grammar.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import log2
from typing import Iterable

Word = str
Response = int
InsideState = int
ExteriorState = int
ExteriorLabels = tuple[int, ...]


def _positive_int(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _canonical_labels(values: Iterable[object]) -> ExteriorLabels:
    labels: dict[object, int] = {}
    result: list[int] = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


def _same_partition(left: ExteriorLabels, right: ExteriorLabels) -> bool:
    if len(left) != len(right):
        return False
    return all(
        (left[i] == left[j]) == (right[i] == right[j])
        for i in range(len(left))
        for j in range(len(left))
    )


def _is_refinement(finer: ExteriorLabels, coarser: ExteriorLabels) -> bool:
    """Return whether every finer block lies inside one coarser block."""
    if len(finer) != len(coarser):
        return False
    return all(finer[i] != finer[j] or coarser[i] == coarser[j] for i in range(len(finer)) for j in range(len(finer)))


@dataclass(frozen=True)
class FiniteBoundaryResponseTable:
    """A finite deterministic response table with a declared word universe.

    ``responses[i][e][k]`` is the response label for inside state ``i``, exterior
    completion ``e``, and ``words[k]``.  Grammar arguments select finite subsets
    of ``words``; response labels need only be equality-comparable integers.
    """

    inside_count: int
    exterior_count: int
    words: tuple[Word, ...]
    responses: tuple[tuple[tuple[Response, ...], ...], ...]

    def __post_init__(self) -> None:
        _positive_int(self.inside_count, "inside_count")
        _positive_int(self.exterior_count, "exterior_count")
        if not isinstance(self.words, tuple) or any(not isinstance(word, str) or not word for word in self.words):
            raise ValueError("words must be a tuple of nonempty strings")
        if len(set(self.words)) != len(self.words):
            raise ValueError("words must be unique")
        if len(self.responses) != self.inside_count:
            raise ValueError("responses must have one row per inside state")
        for inside_row in self.responses:
            if len(inside_row) != self.exterior_count:
                raise ValueError("responses must have one row per exterior state")
            for exterior_row in inside_row:
                if len(exterior_row) != len(self.words):
                    raise ValueError("each response row must cover every declared word")
                if any(not isinstance(value, int) or isinstance(value, bool) for value in exterior_row):
                    raise ValueError("response labels must be integers")

    @property
    def inside_states(self) -> tuple[InsideState, ...]:
        return tuple(range(self.inside_count))

    @property
    def exterior_states(self) -> tuple[ExteriorState, ...]:
        return tuple(range(self.exterior_count))

    @property
    def joint_state_count(self) -> int:
        return self.inside_count * self.exterior_count

    def validate_inside(self, inside: InsideState) -> None:
        if not isinstance(inside, int) or isinstance(inside, bool) or not 0 <= inside < self.inside_count:
            raise ValueError("inside state is outside range")

    def validate_exterior(self, exterior: ExteriorState) -> None:
        if not isinstance(exterior, int) or isinstance(exterior, bool) or not 0 <= exterior < self.exterior_count:
            raise ValueError("exterior state is outside range")

    def normalize_grammar(self, grammar: Iterable[Word]) -> tuple[Word, ...]:
        try:
            requested = tuple(grammar)
        except TypeError as error:
            raise ValueError("grammar must be an iterable of declared words") from error
        if len(set(requested)) != len(requested):
            raise ValueError("grammar words must be unique")
        if any(word not in self.words for word in requested):
            raise ValueError("grammar contains a word outside the declared word universe")
        requested_set = set(requested)
        return tuple(word for word in self.words if word in requested_set)

    def response(self, inside: InsideState, exterior: ExteriorState, word: Word) -> Response:
        self.validate_inside(inside)
        self.validate_exterior(exterior)
        try:
            index = self.words.index(word)
        except ValueError as error:
            raise ValueError("word is outside the declared word universe") from error
        return self.responses[inside][exterior][index]

    def exterior_signature(self, exterior: ExteriorState, grammar: Iterable[Word]) -> tuple[tuple[Response, ...], ...]:
        self.validate_exterior(exterior)
        words = self.normalize_grammar(grammar)
        return tuple(tuple(self.response(inside, exterior, word) for word in words) for inside in self.inside_states)

    def exterior_labels(self, grammar: Iterable[Word]) -> ExteriorLabels:
        return _canonical_labels(self.exterior_signature(exterior, grammar) for exterior in self.exterior_states)

    def exterior_block_count(self, grammar: Iterable[Word]) -> int:
        return len(set(self.exterior_labels(grammar)))

    def joint_signature(self, inside: InsideState, exterior: ExteriorState, grammar: Iterable[Word]) -> tuple[Response, ...]:
        self.validate_inside(inside)
        self.validate_exterior(exterior)
        return tuple(self.response(inside, exterior, word) for word in self.normalize_grammar(grammar))

    def joint_labels(self, grammar: Iterable[Word]) -> tuple[int, ...]:
        return _canonical_labels(
            self.joint_signature(inside, exterior, grammar)
            for inside in self.inside_states
            for exterior in self.exterior_states
        )

    def joint_block_count(self, grammar: Iterable[Word]) -> int:
        return len(set(self.joint_labels(grammar)))

    def verify(self) -> bool:
        try:
            self.__post_init__()
            return True
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class BoundarySummaryFactorCertificate:
    """Certificate that a supplied summary is exact and refines the canonical blanket."""

    system: FiniteBoundaryResponseTable
    grammar: tuple[Word, ...]
    summary_labels: ExteriorLabels
    canonical_labels: ExteriorLabels
    summary_image_count: int
    canonical_block_count: int
    quotient_factor: tuple[int, ...]

    @property
    def is_minimal(self) -> bool:
        return self.summary_image_count == self.canonical_block_count

    def verify(self) -> bool:
        try:
            if not self.system.verify():
                return False
            grammar = self.system.normalize_grammar(self.grammar)
            if grammar != self.grammar or len(self.summary_labels) != self.system.exterior_count:
                return False
            if any(not isinstance(label, int) or isinstance(label, bool) or label < 0 for label in self.summary_labels):
                return False
            canonical = self.system.exterior_labels(grammar)
            if self.canonical_labels != canonical:
                return False
            summary_values = tuple(sorted(set(self.summary_labels)))
            if self.summary_image_count != len(summary_values):
                return False
            if self.canonical_block_count != len(set(canonical)):
                return False
            if len(self.quotient_factor) != self.summary_image_count:
                return False
            summary_to_dense = {label: index for index, label in enumerate(summary_values)}
            for left, right in combinations(self.system.exterior_states, 2):
                if self.summary_labels[left] == self.summary_labels[right]:
                    if self.system.exterior_signature(left, grammar) != self.system.exterior_signature(right, grammar):
                        return False
            for exterior in self.system.exterior_states:
                dense_summary = summary_to_dense[self.summary_labels[exterior]]
                if self.quotient_factor[dense_summary] != canonical[exterior]:
                    return False
            return self.summary_image_count >= self.canonical_block_count
        except (TypeError, ValueError):
            return False


def certify_boundary_summary_factor(
    system: FiniteBoundaryResponseTable,
    grammar: Iterable[Word],
    summary_labels: Iterable[int],
) -> BoundarySummaryFactorCertificate:
    if not system.verify():
        raise ValueError("system must be a valid finite response table")
    normalized_grammar = system.normalize_grammar(grammar)
    labels = tuple(summary_labels)
    if len(labels) != system.exterior_count:
        raise ValueError("summary_labels must contain one label per exterior completion")
    if any(not isinstance(label, int) or isinstance(label, bool) or label < 0 for label in labels):
        raise ValueError("summary labels must be non-negative integers")
    canonical = system.exterior_labels(normalized_grammar)
    summary_values = tuple(sorted(set(labels)))
    quotient_factor: list[int] = []
    for summary in summary_values:
        classes = {canonical[e] for e in system.exterior_states if labels[e] == summary}
        if len(classes) != 1:
            raise ValueError("summary is not response-sound under this grammar")
        quotient_factor.append(next(iter(classes)))
    certificate = BoundarySummaryFactorCertificate(
        system=system,
        grammar=normalized_grammar,
        summary_labels=labels,
        canonical_labels=canonical,
        summary_image_count=len(summary_values),
        canonical_block_count=len(set(canonical)),
        quotient_factor=tuple(quotient_factor),
    )
    if not certificate.verify():
        raise AssertionError("boundary summary factor certificate did not verify")
    return certificate


@dataclass(frozen=True)
class JointObservabilityCertificate:
    """Concrete all-pairs response separation of inside-plus-blanket cells."""

    system: FiniteBoundaryResponseTable
    grammar: tuple[Word, ...]
    canonical_labels: ExteriorLabels
    cell_count: int
    joint_block_count: int
    checked_distinct_cell_pairs: int
    separating_cell_pairs: int

    @property
    def is_joint_observable(self) -> bool:
        return self.joint_block_count == self.cell_count

    @property
    def expected_pair_count(self) -> int:
        return self.cell_count * (self.cell_count - 1) // 2

    def verify(self) -> bool:
        try:
            if not self.system.verify():
                return False
            grammar = self.system.normalize_grammar(self.grammar)
            if grammar != self.grammar:
                return False
            labels = self.system.exterior_labels(grammar)
            if self.canonical_labels != labels:
                return False
            representative: dict[int, int] = {}
            for exterior, label in enumerate(labels):
                representative.setdefault(label, exterior)
            cells = tuple((inside, label) for inside in self.system.inside_states for label in sorted(representative))
            if self.cell_count != len(cells):
                return False
            if self.joint_block_count != self.system.joint_block_count(grammar):
                return False
            separated = 0
            for (inside_a, label_a), (inside_b, label_b) in combinations(cells, 2):
                exterior_a = representative[label_a]
                exterior_b = representative[label_b]
                if any(
                    self.system.response(inside_a, exterior_a, word) != self.system.response(inside_b, exterior_b, word)
                    for word in grammar
                ):
                    separated += 1
            return (
                self.checked_distinct_cell_pairs == self.expected_pair_count
                and self.separating_cell_pairs == separated
                and (self.is_joint_observable == (separated == self.expected_pair_count))
            )
        except (TypeError, ValueError):
            return False


def certify_joint_observability(
    system: FiniteBoundaryResponseTable,
    grammar: Iterable[Word],
) -> JointObservabilityCertificate:
    normalized_grammar = system.normalize_grammar(grammar)
    labels = system.exterior_labels(normalized_grammar)
    block_count = len(set(labels))
    certificate = JointObservabilityCertificate(
        system=system,
        grammar=normalized_grammar,
        canonical_labels=labels,
        cell_count=system.inside_count * block_count,
        joint_block_count=system.joint_block_count(normalized_grammar),
        checked_distinct_cell_pairs=(system.inside_count * block_count) * (system.inside_count * block_count - 1) // 2,
        separating_cell_pairs=0,
    )
    # Rebuild once with the actual count so verification remains self-contained.
    representatives: dict[int, int] = {}
    for exterior, label in enumerate(labels):
        representatives.setdefault(label, exterior)
    cells = tuple((inside, label) for inside in system.inside_states for label in sorted(representatives))
    separated = sum(
        any(
            system.response(inside_a, representatives[label_a], word)
            != system.response(inside_b, representatives[label_b], word)
            for word in normalized_grammar
        )
        for (inside_a, label_a), (inside_b, label_b) in combinations(cells, 2)
    )
    certificate = JointObservabilityCertificate(
        system=system,
        grammar=normalized_grammar,
        canonical_labels=labels,
        cell_count=len(cells),
        joint_block_count=system.joint_block_count(normalized_grammar),
        checked_distinct_cell_pairs=len(cells) * (len(cells) - 1) // 2,
        separating_cell_pairs=separated,
    )
    if not certificate.verify():
        raise AssertionError("joint observability certificate did not verify")
    return certificate


@dataclass(frozen=True)
class CanonicalBoundaryBlanketCertificate:
    """Canonical quotient, induced response factorization, and interface bound."""

    system: FiniteBoundaryResponseTable
    grammar: tuple[Word, ...]
    canonical_labels: ExteriorLabels
    blanket_block_count: int
    joint_interface_block_count: int
    joint_observability: JointObservabilityCertificate

    @property
    def boundary_bits(self) -> float:
        return log2(self.blanket_block_count)

    @property
    def interface_upper_bound_bits(self) -> float:
        return log2(self.system.inside_count) + self.boundary_bits

    @property
    def realized_interface_bits(self) -> float:
        return log2(self.joint_interface_block_count)

    @property
    def equality_holds(self) -> bool:
        return self.joint_observability.is_joint_observable

    def verify(self) -> bool:
        try:
            if not self.system.verify() or not self.joint_observability.verify():
                return False
            grammar = self.system.normalize_grammar(self.grammar)
            if grammar != self.grammar:
                return False
            labels = self.system.exterior_labels(grammar)
            if self.canonical_labels != labels:
                return False
            if self.blanket_block_count != len(set(labels)):
                return False
            if self.joint_interface_block_count != self.system.joint_block_count(grammar):
                return False
            # Same inside + same blanket class must imply equal response for every word.
            for inside in self.system.inside_states:
                for left, right in combinations(self.system.exterior_states, 2):
                    if labels[left] == labels[right]:
                        if any(
                            self.system.response(inside, left, word) != self.system.response(inside, right, word)
                            for word in grammar
                        ):
                            return False
            cell_count = self.system.inside_count * self.blanket_block_count
            if self.joint_interface_block_count > cell_count:
                return False
            tolerance = 1e-12
            if self.equality_holds:
                return abs(self.realized_interface_bits - self.interface_upper_bound_bits) <= tolerance
            return self.realized_interface_bits < self.interface_upper_bound_bits + tolerance
        except (TypeError, ValueError):
            return False


def certify_canonical_boundary_blanket(
    system: FiniteBoundaryResponseTable,
    grammar: Iterable[Word],
) -> CanonicalBoundaryBlanketCertificate:
    normalized_grammar = system.normalize_grammar(grammar)
    labels = system.exterior_labels(normalized_grammar)
    observability = certify_joint_observability(system, normalized_grammar)
    certificate = CanonicalBoundaryBlanketCertificate(
        system=system,
        grammar=normalized_grammar,
        canonical_labels=labels,
        blanket_block_count=len(set(labels)),
        joint_interface_block_count=system.joint_block_count(normalized_grammar),
        joint_observability=observability,
    )
    if not certificate.verify():
        raise AssertionError("canonical boundary blanket certificate did not verify")
    return certificate


@dataclass(frozen=True)
class FiniteGrammarChainCertificate:
    """Finite declared-chain replay of monotone exterior quotient refinement.

    The certificate checks only the supplied finite chain.  It deliberately does
    not infer stabilization of an unlisted infinite continuation.
    """

    system: FiniteBoundaryResponseTable
    grammar_levels: tuple[tuple[Word, ...], ...]
    exterior_labels_by_level: tuple[ExteriorLabels, ...]
    block_counts: tuple[int, ...]
    first_terminal_stable_level: int

    def verify(self) -> bool:
        try:
            if not self.system.verify() or not self.grammar_levels:
                return False
            normalized = tuple(self.system.normalize_grammar(level) for level in self.grammar_levels)
            if normalized != self.grammar_levels:
                return False
            if len(self.exterior_labels_by_level) != len(normalized) or len(self.block_counts) != len(normalized):
                return False
            for index, grammar in enumerate(normalized):
                labels = self.system.exterior_labels(grammar)
                if self.exterior_labels_by_level[index] != labels or self.block_counts[index] != len(set(labels)):
                    return False
                if index:
                    if not set(normalized[index - 1]).issubset(grammar):
                        return False
                    if not _is_refinement(labels, self.exterior_labels_by_level[index - 1]):
                        return False
                    if self.block_counts[index] < self.block_counts[index - 1]:
                        return False
            stable = [
                index
                for index in range(len(normalized))
                if all(_same_partition(self.exterior_labels_by_level[index], later) for later in self.exterior_labels_by_level[index:])
            ]
            return bool(stable) and self.first_terminal_stable_level == stable[0]
        except (TypeError, ValueError):
            return False


def certify_finite_grammar_chain(
    system: FiniteBoundaryResponseTable,
    grammar_levels: Iterable[Iterable[Word]],
) -> FiniteGrammarChainCertificate:
    try:
        levels = tuple(system.normalize_grammar(level) for level in grammar_levels)
    except TypeError as error:
        raise ValueError("grammar_levels must be an iterable of grammar iterables") from error
    if not levels:
        raise ValueError("a finite grammar chain must contain at least one level")
    labels = tuple(system.exterior_labels(level) for level in levels)
    stable = next(
        index
        for index in range(len(levels))
        if all(_same_partition(labels[index], later) for later in labels[index:])
    )
    certificate = FiniteGrammarChainCertificate(
        system=system,
        grammar_levels=levels,
        exterior_labels_by_level=labels,
        block_counts=tuple(len(set(level)) for level in labels),
        first_terminal_stable_level=stable,
    )
    if not certificate.verify():
        raise AssertionError("finite grammar chain certificate did not verify")
    return certificate


def redundant_exterior_response_table() -> FiniteBoundaryResponseTable:
    """Two raw exterior response types duplicated into four physical completions.

    Exterior states 0/1 are response-equivalent and 2/3 are response-equivalent.
    The canonical blanket has two classes even though the raw exterior has four.
    """
    words = ("observe", "read")
    rows: list[tuple[tuple[int, ...], ...]] = []
    for inside in range(2):
        inside_rows: list[tuple[int, ...]] = []
        for exterior in range(4):
            response_type = exterior // 2
            inside_rows.append((inside, 2 * inside + response_type))
        rows.append(tuple(inside_rows))
    return FiniteBoundaryResponseTable(
        inside_count=2,
        exterior_count=4,
        words=words,
        responses=tuple(rows),
    )


def binary_addressable_ladder(exterior_bit_count: int) -> tuple[FiniteBoundaryResponseTable, tuple[tuple[Word, ...], ...]]:
    """Finite prefixes of an unbounded-addressability obstruction.

    The returned chain has level k able to read the first k of ``m`` binary
    exterior coordinates, giving exactly ``2^k`` canonical blanket classes.
    It is a finite replay witness; the countable extension belongs to the proof
    document, not to this finite object.
    """
    _positive_int(exterior_bit_count, "exterior_bit_count")
    words = tuple(f"read:{index}" for index in range(exterior_bit_count))
    exterior_count = 2 ** exterior_bit_count
    rows: list[tuple[tuple[int, ...], ...]] = []
    inside_rows: list[tuple[int, ...]] = []
    for exterior in range(exterior_count):
        inside_rows.append(tuple((exterior >> index) & 1 for index in range(exterior_bit_count)))
    rows.append(tuple(inside_rows))
    system = FiniteBoundaryResponseTable(
        inside_count=1,
        exterior_count=exterior_count,
        words=words,
        responses=tuple(rows),
    )
    levels = tuple(tuple(words[:count]) for count in range(exterior_bit_count + 1))
    return system, levels


@dataclass(frozen=True)
class AddressableLadderCertificate:
    """Exact finite-prefix growth of canonical blanket classes."""

    exterior_bit_count: int
    chain: FiniteGrammarChainCertificate

    @property
    def expected_block_counts(self) -> tuple[int, ...]:
        return tuple(2**count for count in range(self.exterior_bit_count + 1))

    def verify(self) -> bool:
        try:
            system, levels = binary_addressable_ladder(self.exterior_bit_count)
            return (
                self.chain.verify()
                and self.chain.system == system
                and self.chain.grammar_levels == levels
                and self.chain.block_counts == self.expected_block_counts
                and self.chain.first_terminal_stable_level == self.exterior_bit_count
            )
        except (TypeError, ValueError):
            return False


def certify_addressable_ladder(exterior_bit_count: int) -> AddressableLadderCertificate:
    system, levels = binary_addressable_ladder(exterior_bit_count)
    certificate = AddressableLadderCertificate(
        exterior_bit_count=exterior_bit_count,
        chain=certify_finite_grammar_chain(system, levels),
    )
    if not certificate.verify():
        raise AssertionError("addressable ladder certificate did not verify")
    return certificate
