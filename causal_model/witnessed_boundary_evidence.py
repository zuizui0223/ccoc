"""Witnessed lower bounds for boundary blankets and completion-coverage no-go.

This module connects the canonical boundary blanket to finite evidence.  For a
finite sampled set of exterior completions and a finite tested panel of
inside-state / boundary-word cells, observed response signatures can certify a
*lower* bound on the number of exact exterior response classes.  The lower bound
is witnessed: every pair of observed classes carries a concrete separating
inside-state/word response.

The converse requires an explicit coverage contract.  A finite collection of
sampled completions proves the exact canonical blanket size only when it is
certified to meet every canonical response class and the panel covers the whole
declared inside/grammar product.

Without that completion-and-grammar coverage contract, finite transcript data do
not provide a universal upper bound over an extension-closed model class.  The
free-completion construction adds any chosen number of new exterior completions
which agree with a baseline on all tested cells, while fresh legal words separate
them pairwise.

All results are finite deterministic response-table statements.  They are not
statistical confidence intervals, claims about noisy field data, or claims that
an empirical sample exhausts a biological completion class.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import log2
from typing import Iterable

from .canonical_boundary_blankets import (
    ExteriorLabels,
    ExteriorState,
    FiniteBoundaryResponseTable,
    InsideState,
    Response,
    Word,
    _canonical_labels,
)

ObservationCell = tuple[InsideState, Word]


def _normalize_sample(
    system: FiniteBoundaryResponseTable,
    sampled_exteriors: Iterable[ExteriorState],
) -> tuple[ExteriorState, ...]:
    try:
        values = tuple(sampled_exteriors)
    except TypeError as error:
        raise ValueError("sampled_exteriors must be an iterable of exterior states") from error
    if not values:
        raise ValueError("sampled_exteriors must be nonempty")
    if tuple(sorted(set(values))) != values:
        raise ValueError("sampled_exteriors must be sorted, unique, and canonical")
    for exterior in values:
        system.validate_exterior(exterior)
    return values


def _normalize_cells(
    system: FiniteBoundaryResponseTable,
    grammar: tuple[Word, ...],
    cells: Iterable[ObservationCell],
) -> tuple[ObservationCell, ...]:
    try:
        values = tuple(cells)
    except TypeError as error:
        raise ValueError("observed_cells must be an iterable of (inside, word) cells") from error
    grammar_set = set(grammar)
    normalized: list[ObservationCell] = []
    for cell in values:
        if not isinstance(cell, tuple) or len(cell) != 2:
            raise ValueError("each observed cell must be a pair (inside, word)")
        inside, word = cell
        system.validate_inside(inside)
        if not isinstance(word, str) or word not in grammar_set:
            raise ValueError("observed cell word must belong to the declared grammar")
        normalized.append((inside, word))
    word_position = {word: index for index, word in enumerate(system.words)}
    canonical = tuple(sorted(normalized, key=lambda cell: (cell[0], word_position[cell[1]])))
    if len(set(canonical)) != len(canonical):
        raise ValueError("observed cells must be unique")
    return canonical


def _full_cells(system: FiniteBoundaryResponseTable, grammar: tuple[Word, ...]) -> tuple[ObservationCell, ...]:
    return tuple((inside, word) for inside in system.inside_states for word in grammar)


def observed_signature(
    system: FiniteBoundaryResponseTable,
    exterior: ExteriorState,
    observed_cells: Iterable[ObservationCell],
) -> tuple[Response, ...]:
    system.validate_exterior(exterior)
    return tuple(system.response(inside, exterior, word) for inside, word in observed_cells)


def _observed_labels(
    system: FiniteBoundaryResponseTable,
    sample: tuple[ExteriorState, ...],
    cells: tuple[ObservationCell, ...],
) -> ExteriorLabels:
    return _canonical_labels(observed_signature(system, exterior, cells) for exterior in sample)


@dataclass(frozen=True)
class ObservedClassSeparationWitness:
    """One tested cell that separates two observed signature classes."""

    left_sample_position: int
    right_sample_position: int
    inside: InsideState
    word: Word
    left_response: Response
    right_response: Response

    def verify(
        self,
        system: FiniteBoundaryResponseTable,
        sample: tuple[ExteriorState, ...],
        observed_cells: tuple[ObservationCell, ...],
        labels: ExteriorLabels,
    ) -> bool:
        try:
            if not 0 <= self.left_sample_position < len(sample) or not 0 <= self.right_sample_position < len(sample):
                return False
            if self.left_sample_position >= self.right_sample_position:
                return False
            if labels[self.left_sample_position] == labels[self.right_sample_position]:
                return False
            if (self.inside, self.word) not in observed_cells:
                return False
            left = sample[self.left_sample_position]
            right = sample[self.right_sample_position]
            if self.left_response != system.response(self.inside, left, self.word):
                return False
            if self.right_response != system.response(self.inside, right, self.word):
                return False
            return self.left_response != self.right_response
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class WitnessedBoundaryLowerBoundCertificate:
    """Observed exterior response classes give a witnessed lower blanket bound."""

    system: FiniteBoundaryResponseTable
    grammar: tuple[Word, ...]
    sampled_exteriors: tuple[ExteriorState, ...]
    observed_cells: tuple[ObservationCell, ...]
    observed_labels: ExteriorLabels
    observed_class_count: int
    canonical_blanket_count: int
    separation_witnesses: tuple[ObservedClassSeparationWitness, ...]

    @property
    def lower_bound_bits(self) -> float:
        return log2(self.observed_class_count)

    @property
    def canonical_blanket_bits(self) -> float:
        return log2(self.canonical_blanket_count)

    @property
    def expected_witness_count(self) -> int:
        return self.observed_class_count * (self.observed_class_count - 1) // 2

    def verify(self) -> bool:
        try:
            if not self.system.verify():
                return False
            grammar = self.system.normalize_grammar(self.grammar)
            if grammar != self.grammar:
                return False
            sample = _normalize_sample(self.system, self.sampled_exteriors)
            cells = _normalize_cells(self.system, grammar, self.observed_cells)
            if sample != self.sampled_exteriors or cells != self.observed_cells:
                return False
            labels = _observed_labels(self.system, sample, cells)
            if labels != self.observed_labels:
                return False
            if self.observed_class_count != len(set(labels)):
                return False
            canonical_labels = self.system.exterior_labels(grammar)
            if self.canonical_blanket_count != len(set(canonical_labels)):
                return False
            # Equality on all canonical responses implies equality on the observed subpanel.
            for left, right in combinations(range(len(sample)), 2):
                if canonical_labels[sample[left]] == canonical_labels[sample[right]] and labels[left] != labels[right]:
                    return False
            if self.observed_class_count > self.canonical_blanket_count:
                return False
            # One representative pair and one concrete separating observed cell per observed class pair.
            class_representatives: dict[int, int] = {}
            for position, label in enumerate(labels):
                class_representatives.setdefault(label, position)
            expected_class_pairs = {
                tuple(sorted((left_label, right_label)))
                for left_label, right_label in combinations(sorted(class_representatives), 2)
            }
            found_pairs: set[tuple[int, int]] = set()
            for witness in self.separation_witnesses:
                if not witness.verify(self.system, sample, cells, labels):
                    return False
                pair = tuple(sorted((labels[witness.left_sample_position], labels[witness.right_sample_position])))
                if pair in found_pairs:
                    return False
                found_pairs.add(pair)
            return len(self.separation_witnesses) == self.expected_witness_count and found_pairs == expected_class_pairs
        except (TypeError, ValueError):
            return False


def certify_witnessed_boundary_lower_bound(
    system: FiniteBoundaryResponseTable,
    grammar: Iterable[Word],
    sampled_exteriors: Iterable[ExteriorState],
    observed_cells: Iterable[ObservationCell],
) -> WitnessedBoundaryLowerBoundCertificate:
    """Certify a lower blanket bound from sampled completions and tested cells."""
    if not system.verify():
        raise ValueError("system must be a valid finite response table")
    normalized_grammar = system.normalize_grammar(grammar)
    sample = _normalize_sample(system, sampled_exteriors)
    cells = _normalize_cells(system, normalized_grammar, observed_cells)
    labels = _observed_labels(system, sample, cells)
    representatives: dict[int, int] = {}
    for position, label in enumerate(labels):
        representatives.setdefault(label, position)
    witnesses: list[ObservedClassSeparationWitness] = []
    for left_label, right_label in combinations(sorted(representatives), 2):
        left_position = representatives[left_label]
        right_position = representatives[right_label]
        left = sample[left_position]
        right = sample[right_position]
        separating_cell = next(
            (inside, word)
            for inside, word in cells
            if system.response(inside, left, word) != system.response(inside, right, word)
        )
        inside, word = separating_cell
        witnesses.append(
            ObservedClassSeparationWitness(
                left_sample_position=left_position,
                right_sample_position=right_position,
                inside=inside,
                word=word,
                left_response=system.response(inside, left, word),
                right_response=system.response(inside, right, word),
            )
        )
    certificate = WitnessedBoundaryLowerBoundCertificate(
        system=system,
        grammar=normalized_grammar,
        sampled_exteriors=sample,
        observed_cells=cells,
        observed_labels=labels,
        observed_class_count=len(set(labels)),
        canonical_blanket_count=system.exterior_block_count(normalized_grammar),
        separation_witnesses=tuple(witnesses),
    )
    if not certificate.verify():
        raise AssertionError("witnessed boundary lower-bound certificate did not verify")
    return certificate


@dataclass(frozen=True)
class EvidenceChainCertificate:
    """Monotone witnessed lower bounds over nested samples and tested panels."""

    system: FiniteBoundaryResponseTable
    grammar: tuple[Word, ...]
    sample_levels: tuple[tuple[ExteriorState, ...], ...]
    panel_levels: tuple[tuple[ObservationCell, ...], ...]
    lower_bound_counts: tuple[int, ...]

    def verify(self) -> bool:
        try:
            if not self.system.verify() or not self.sample_levels:
                return False
            grammar = self.system.normalize_grammar(self.grammar)
            if grammar != self.grammar or len(self.panel_levels) != len(self.sample_levels):
                return False
            if len(self.lower_bound_counts) != len(self.sample_levels):
                return False
            previous_sample: set[int] = set()
            previous_panel: set[ObservationCell] = set()
            previous_count = 0
            for sample, panel, count in zip(self.sample_levels, self.panel_levels, self.lower_bound_counts):
                normalized_sample = _normalize_sample(self.system, sample)
                normalized_panel = _normalize_cells(self.system, grammar, panel)
                if normalized_sample != sample or normalized_panel != panel:
                    return False
                if not previous_sample.issubset(sample) or not previous_panel.issubset(panel):
                    return False
                certificate = certify_witnessed_boundary_lower_bound(
                    self.system,
                    grammar,
                    sample,
                    panel,
                )
                if count != certificate.observed_class_count or count < previous_count:
                    return False
                previous_sample = set(sample)
                previous_panel = set(panel)
                previous_count = count
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_evidence_chain(
    system: FiniteBoundaryResponseTable,
    grammar: Iterable[Word],
    levels: Iterable[tuple[Iterable[ExteriorState], Iterable[ObservationCell]]],
) -> EvidenceChainCertificate:
    """Certify monotone growth of witnessed lower bounds for nested evidence."""
    normalized_grammar = system.normalize_grammar(grammar)
    try:
        raw_levels = tuple(levels)
    except TypeError as error:
        raise ValueError("levels must be an iterable of (sample, panel) pairs") from error
    if not raw_levels:
        raise ValueError("an evidence chain must contain at least one level")
    samples: list[tuple[ExteriorState, ...]] = []
    panels: list[tuple[ObservationCell, ...]] = []
    counts: list[int] = []
    for level in raw_levels:
        if not isinstance(level, tuple) or len(level) != 2:
            raise ValueError("each evidence level must be a pair (sample, panel)")
        sample = _normalize_sample(system, level[0])
        panel = _normalize_cells(system, normalized_grammar, level[1])
        certificate = certify_witnessed_boundary_lower_bound(system, normalized_grammar, sample, panel)
        samples.append(sample)
        panels.append(panel)
        counts.append(certificate.observed_class_count)
    certificate = EvidenceChainCertificate(
        system=system,
        grammar=normalized_grammar,
        sample_levels=tuple(samples),
        panel_levels=tuple(panels),
        lower_bound_counts=tuple(counts),
    )
    if not certificate.verify():
        raise AssertionError("evidence-chain certificate did not verify")
    return certificate


@dataclass(frozen=True)
class CompletionCoverageCertificate:
    """A formal contract turning sampled lower evidence into exact blanket size.

    The certificate is not derived from sample size.  It explicitly checks that
    the supplied sampled exteriors meet every canonical exterior response class,
    and that every inside/word cell of the declared grammar is tested.
    """

    system: FiniteBoundaryResponseTable
    grammar: tuple[Word, ...]
    sampled_exteriors: tuple[ExteriorState, ...]
    observed_cells: tuple[ObservationCell, ...]
    sampled_canonical_labels: tuple[int, ...]
    canonical_blanket_count: int
    exact_observed_class_count: int

    def verify(self) -> bool:
        try:
            if not self.system.verify():
                return False
            grammar = self.system.normalize_grammar(self.grammar)
            if grammar != self.grammar:
                return False
            sample = _normalize_sample(self.system, self.sampled_exteriors)
            cells = _normalize_cells(self.system, grammar, self.observed_cells)
            if sample != self.sampled_exteriors or cells != self.observed_cells:
                return False
            if cells != _full_cells(self.system, grammar):
                return False
            canonical = self.system.exterior_labels(grammar)
            sampled_labels = tuple(canonical[exterior] for exterior in sample)
            if self.sampled_canonical_labels != sampled_labels:
                return False
            if self.canonical_blanket_count != len(set(canonical)):
                return False
            if set(sampled_labels) != set(canonical):
                return False
            observed = _observed_labels(self.system, sample, cells)
            if self.exact_observed_class_count != len(set(observed)):
                return False
            return self.exact_observed_class_count == self.canonical_blanket_count
        except (TypeError, ValueError):
            return False


def certify_completion_coverage(
    system: FiniteBoundaryResponseTable,
    grammar: Iterable[Word],
    sampled_exteriors: Iterable[ExteriorState],
) -> CompletionCoverageCertificate:
    """Construct an exactness certificate under explicit canonical-class coverage."""
    normalized_grammar = system.normalize_grammar(grammar)
    sample = _normalize_sample(system, sampled_exteriors)
    cells = _full_cells(system, normalized_grammar)
    canonical = system.exterior_labels(normalized_grammar)
    if set(canonical[exterior] for exterior in sample) != set(canonical):
        raise ValueError("sampled exteriors do not cover every canonical response class")
    observed = _observed_labels(system, sample, cells)
    certificate = CompletionCoverageCertificate(
        system=system,
        grammar=normalized_grammar,
        sampled_exteriors=sample,
        observed_cells=cells,
        sampled_canonical_labels=tuple(canonical[exterior] for exterior in sample),
        canonical_blanket_count=len(set(canonical)),
        exact_observed_class_count=len(set(observed)),
    )
    if not certificate.verify():
        raise AssertionError("completion-coverage certificate did not verify")
    return certificate


def _fresh_words(system: FiniteBoundaryResponseTable, count: int) -> tuple[Word, ...]:
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise ValueError("fresh_completion_count must be a positive integer")
    words: list[Word] = []
    used = set(system.words)
    candidate_index = 0
    while len(words) < count:
        candidate = f"__fresh_completion_separator__:{candidate_index}"
        candidate_index += 1
        if candidate not in used:
            words.append(candidate)
            used.add(candidate)
    return tuple(words)


def _extended_with_free_completions(
    system: FiniteBoundaryResponseTable,
    baseline_exterior: ExteriorState,
    fresh_completion_count: int,
) -> tuple[FiniteBoundaryResponseTable, tuple[Word, ...], tuple[ExteriorState, ...]]:
    system.validate_exterior(baseline_exterior)
    fresh_words = _fresh_words(system, fresh_completion_count)
    extended_words = system.words + fresh_words
    rows: list[tuple[tuple[int, ...], ...]] = []
    for inside in system.inside_states:
        exterior_rows: list[tuple[int, ...]] = []
        for exterior in system.exterior_states:
            old = tuple(system.response(inside, exterior, word) for word in system.words)
            exterior_rows.append(old + (0,) * fresh_completion_count)
        baseline_old = tuple(system.response(inside, baseline_exterior, word) for word in system.words)
        for fresh_index in range(fresh_completion_count):
            special = tuple(1 if index == fresh_index else 0 for index in range(fresh_completion_count))
            exterior_rows.append(baseline_old + special)
        rows.append(tuple(exterior_rows))
    extended = FiniteBoundaryResponseTable(
        inside_count=system.inside_count,
        exterior_count=system.exterior_count + fresh_completion_count,
        words=extended_words,
        responses=tuple(rows),
    )
    new_exteriors = tuple(range(system.exterior_count, extended.exterior_count))
    return extended, fresh_words, new_exteriors


@dataclass(frozen=True)
class FreeCompletionExtensionCertificate:
    """Finite data are preserved while arbitrarily many new response types appear."""

    original_system: FiniteBoundaryResponseTable
    sampled_exteriors: tuple[ExteriorState, ...]
    observed_cells: tuple[ObservationCell, ...]
    baseline_exterior: ExteriorState
    fresh_completion_count: int
    extended_system: FiniteBoundaryResponseTable
    fresh_words: tuple[Word, ...]
    new_exteriors: tuple[ExteriorState, ...]
    original_blanket_count: int
    extended_blanket_count: int

    @property
    def expected_extended_blanket_count(self) -> int:
        return self.original_blanket_count + self.fresh_completion_count

    def verify(self) -> bool:
        try:
            if not self.original_system.verify() or not self.extended_system.verify():
                return False
            sample = _normalize_sample(self.original_system, self.sampled_exteriors)
            cells = _normalize_cells(self.original_system, self.original_system.words, self.observed_cells)
            if sample != self.sampled_exteriors or cells != self.observed_cells:
                return False
            self.original_system.validate_exterior(self.baseline_exterior)
            expected_extended, fresh_words, new_exteriors = _extended_with_free_completions(
                self.original_system,
                self.baseline_exterior,
                self.fresh_completion_count,
            )
            if self.extended_system != expected_extended or self.fresh_words != fresh_words or self.new_exteriors != new_exteriors:
                return False
            original_labels = self.original_system.exterior_labels(self.original_system.words)
            extended_labels = self.extended_system.exterior_labels(self.extended_system.words)
            if self.original_blanket_count != len(set(original_labels)):
                return False
            if self.extended_blanket_count != len(set(extended_labels)):
                return False
            # Original transcript and all original response distinctions are unchanged.
            for inside in self.original_system.inside_states:
                for exterior in self.original_system.exterior_states:
                    for word in self.original_system.words:
                        if self.extended_system.response(inside, exterior, word) != self.original_system.response(inside, exterior, word):
                            return False
            # New completions agree with the baseline on every tested old cell.
            for exterior in self.new_exteriors:
                for inside, word in cells:
                    if self.extended_system.response(inside, exterior, word) != self.original_system.response(inside, self.baseline_exterior, word):
                        return False
            # Fresh binary words make each new completion a new canonical class.
            for left, right in combinations(self.new_exteriors, 2):
                if not any(
                    self.extended_system.response(0, left, word) != self.extended_system.response(0, right, word)
                    for word in self.fresh_words
                ):
                    return False
            for exterior in self.new_exteriors:
                if not any(
                    self.extended_system.response(0, exterior, word)
                    != self.extended_system.response(0, self.baseline_exterior, word)
                    for word in self.fresh_words
                ):
                    return False
            return self.extended_blanket_count == self.expected_extended_blanket_count
        except (TypeError, ValueError):
            return False


def certify_free_completion_extension(
    system: FiniteBoundaryResponseTable,
    sampled_exteriors: Iterable[ExteriorState],
    observed_cells: Iterable[ObservationCell],
    baseline_exterior: ExteriorState,
    fresh_completion_count: int,
) -> FreeCompletionExtensionCertificate:
    """Construct an arbitrary-size unseen-completion extension preserving a transcript."""
    sample = _normalize_sample(system, sampled_exteriors)
    if baseline_exterior not in sample:
        raise ValueError("baseline_exterior must be among sampled_exteriors")
    cells = _normalize_cells(system, system.words, observed_cells)
    extended, fresh_words, new_exteriors = _extended_with_free_completions(system, baseline_exterior, fresh_completion_count)
    certificate = FreeCompletionExtensionCertificate(
        original_system=system,
        sampled_exteriors=sample,
        observed_cells=cells,
        baseline_exterior=baseline_exterior,
        fresh_completion_count=fresh_completion_count,
        extended_system=extended,
        fresh_words=fresh_words,
        new_exteriors=new_exteriors,
        original_blanket_count=system.exterior_block_count(system.words),
        extended_blanket_count=extended.exterior_block_count(extended.words),
    )
    if not certificate.verify():
        raise AssertionError("free-completion extension certificate did not verify")
    return certificate
