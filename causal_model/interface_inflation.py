"""Exact decomposition of closed-to-open causal interface inflation.

The union of closed response grammars has a static common-refinement / natural-
join interpretation. An actual open grammar may contain additional future words
that split those union-grammar fibers further. This module separates the two
sources of interface complexity.

The algebraic decomposition itself is elementary bookkeeping over finite
partitions. Its role is to connect three existing CCOC ingredients without
claiming the partition identity as novel mathematics:

* CORE-2 closed/open refinement capacity;
* database-style joint-realizability loss among closed response views; and
* CORE-5 newly legal future-word fiber splits.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Hashable, Iterable

from .dynamic_boundary_blankets import Action, FiniteControlledOutputSystem
from .union_grammar_refinement import (
    PartitionRefinementCapacityCertificate,
    ResponseSignature,
    Word,
    certify_partition_refinement_capacity,
    certify_union_grammar_refinement,
)

Label = Hashable
Trace = tuple[Hashable, ...]


def _normalize_labels(labels: Iterable[Label], name: str) -> tuple[Label, ...]:
    try:
        normalized = tuple(labels)
    except TypeError as error:
        raise ValueError(f"{name} must be iterable") from error
    if not normalized:
        raise ValueError(f"{name} must be nonempty")
    try:
        for label in normalized:
            hash(label)
    except TypeError as error:
        raise ValueError(f"{name} must contain only hashable labels") from error
    return normalized


def _normalize_closed_labels(
    closed_labels: Iterable[Iterable[Label]],
    domain_size: int,
) -> tuple[tuple[Label, ...], ...]:
    try:
        normalized = tuple(
            _normalize_labels(labels, f"closed_labels[{index}]")
            for index, labels in enumerate(closed_labels)
        )
    except TypeError as error:
        raise ValueError("closed_labels must be iterable") from error
    if not normalized:
        raise ValueError("at least one closed partition is required")
    if any(len(labels) != domain_size for labels in normalized):
        raise ValueError("every closed label row must match the domain size")
    return normalized


def _partition_refines(fine: tuple[Label, ...], coarse: tuple[Label, ...]) -> bool:
    coarse_by_fine: dict[Label, Label] = {}
    for fine_label, coarse_label in zip(fine, coarse):
        if fine_label in coarse_by_fine:
            if coarse_by_fine[fine_label] != coarse_label:
                return False
        else:
            coarse_by_fine[fine_label] = coarse_label
    return True


@dataclass(frozen=True)
class InterfaceInflationDecompositionCertificate:
    """Partition-level exact decomposition of total open-interface inflation."""

    base_labels: tuple[Label, ...]
    closed_labels: tuple[tuple[Label, ...], ...]
    open_labels: tuple[Label, ...]

    @property
    def domain_size(self) -> int:
        return len(self.base_labels)

    @property
    def refinement_capacity(self) -> PartitionRefinementCapacityCertificate:
        return certify_partition_refinement_capacity(self.base_labels, self.closed_labels)

    @property
    def union_labels(self) -> tuple[tuple[Label, ...], ...]:
        return self.refinement_capacity.common_refinement_labels

    @property
    def union_block_count(self) -> int:
        return self.refinement_capacity.common_refinement_block_count

    @property
    def open_block_count(self) -> int:
        return len(set(self.open_labels))

    @property
    def closed_block_counts(self) -> tuple[int, ...]:
        return self.refinement_capacity.closed_block_counts

    @property
    def fibered_capacity_state_count(self) -> int:
        return self.refinement_capacity.fibered_capacity_state_count

    @property
    def capacity_gap_bits(self) -> float:
        return self.refinement_capacity.capacity_gap_bits

    @property
    def join_realizability_defect_bits(self) -> float:
        return self.refinement_capacity.fibered_capacity_bits - log2(self.union_block_count)

    @property
    def new_word_innovation_bits(self) -> float:
        return log2(self.open_block_count) - log2(self.union_block_count)

    @property
    def total_noncommutation_gap_bits(self) -> float:
        return log2(self.open_block_count) - max(
            log2(count) for count in self.closed_block_counts
        )

    @property
    def first_innovation_split_indices(self) -> tuple[int, int] | None:
        for left in range(self.domain_size):
            for right in range(left + 1, self.domain_size):
                if (
                    self.union_labels[left] == self.union_labels[right]
                    and self.open_labels[left] != self.open_labels[right]
                ):
                    return (left, right)
        return None

    @property
    def has_new_word_innovation(self) -> bool:
        return self.first_innovation_split_indices is not None

    def verify(self) -> bool:
        try:
            base = _normalize_labels(self.base_labels, "base_labels")
            if base != self.base_labels:
                return False
            closed = _normalize_closed_labels(self.closed_labels, len(base))
            if closed != self.closed_labels:
                return False
            open_labels = _normalize_labels(self.open_labels, "open_labels")
            if open_labels != self.open_labels or len(open_labels) != len(base):
                return False

            capacity = self.refinement_capacity
            if not capacity.verify():
                return False

            # The actual open grammar contains the closed-union grammar, so its
            # partition must refine the common closed refinement.
            if not _partition_refines(open_labels, self.union_labels):
                return False
            if self.open_block_count < self.union_block_count:
                return False
            if self.join_realizability_defect_bits < -1e-12:
                return False
            if self.new_word_innovation_bits < -1e-12:
                return False

            expected = (
                self.capacity_gap_bits
                - self.join_realizability_defect_bits
                + self.new_word_innovation_bits
            )
            if abs(self.total_noncommutation_gap_bits - expected) > 1e-12:
                return False
            if self.has_new_word_innovation != (self.open_block_count > self.union_block_count):
                return False
            return True
        except (TypeError, ValueError):
            return False


def certify_interface_inflation_decomposition(
    base_labels: Iterable[Label],
    closed_labels: Iterable[Iterable[Label]],
    open_labels: Iterable[Label],
) -> InterfaceInflationDecompositionCertificate:
    """Certify one finite partition-level inflation decomposition."""
    base = _normalize_labels(base_labels, "base_labels")
    closed = _normalize_closed_labels(closed_labels, len(base))
    open_normalized = _normalize_labels(open_labels, "open_labels")
    if len(open_normalized) != len(base):
        raise ValueError("open_labels must match the comparison-domain size")
    certificate = InterfaceInflationDecompositionCertificate(
        base_labels=base,
        closed_labels=closed,
        open_labels=open_normalized,
    )
    if not certificate.verify():
        raise ValueError("declared open partition does not refine the closed-union contract")
    return certificate


def _normalize_domain(
    system: FiniteControlledOutputSystem,
    domain_states: Iterable[int],
) -> tuple[int, ...]:
    try:
        domain = tuple(domain_states)
    except TypeError as error:
        raise ValueError("domain_states must be iterable") from error
    if not domain:
        raise ValueError("domain_states must be nonempty")
    if len(set(domain)) != len(domain):
        raise ValueError("domain_states must be unique")
    for state in domain:
        system.validate_state(state)
    return domain


def _normalize_word_family(
    system: FiniteControlledOutputSystem,
    words: Iterable[Iterable[Action]],
    name: str,
    *,
    allow_empty: bool,
) -> tuple[Word, ...]:
    try:
        normalized = tuple(system.normalize_word(tuple(word)) for word in words)
    except TypeError as error:
        raise ValueError(f"{name} must be an iterable of words") from error
    if not allow_empty and not normalized:
        raise ValueError(f"{name} must contain at least one word")
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{name} must not contain duplicate words")
    return normalized


def _stable_word_union(families: Iterable[Iterable[Word]]) -> tuple[Word, ...]:
    seen: set[Word] = set()
    result: list[Word] = []
    for family in families:
        for word in family:
            if word not in seen:
                seen.add(word)
                result.append(word)
    return tuple(result)


def _signature(
    system: FiniteControlledOutputSystem,
    state: int,
    words: tuple[Word, ...],
) -> ResponseSignature:
    return tuple(system.output_trace(state, word) for word in words)


@dataclass(frozen=True)
class OpenOnlyWordSplitWitness:
    """Concrete open-only word separating one closed-union quotient fiber."""

    left_state: int
    right_state: int
    separating_word: Word
    left_trace: Trace
    right_trace: Trace

    def verify(self, system: FiniteControlledOutputSystem) -> bool:
        try:
            system.validate_state(self.left_state)
            system.validate_state(self.right_state)
            if self.left_state == self.right_state:
                return False
            if system.normalize_word(self.separating_word) != self.separating_word:
                return False
            return (
                system.output_trace(self.left_state, self.separating_word) == self.left_trace
                and system.output_trace(self.right_state, self.separating_word) == self.right_trace
                and self.left_trace != self.right_trace
            )
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class OperationalInterfaceInflationCertificate:
    """Controlled-response realization of the capacity/defect/innovation identity."""

    system: FiniteControlledOutputSystem
    domain_states: tuple[int, ...]
    base_words: tuple[Word, ...]
    closed_word_families: tuple[tuple[Word, ...], ...]
    open_only_words: tuple[Word, ...]

    @property
    def union_certificate(self):
        return certify_union_grammar_refinement(
            self.system,
            self.domain_states,
            self.base_words,
            self.closed_word_families,
        )

    @property
    def union_words(self) -> tuple[Word, ...]:
        return self.union_certificate.open_words

    @property
    def open_words(self) -> tuple[Word, ...]:
        return _stable_word_union((self.union_words, self.open_only_words))

    @property
    def open_labels(self) -> tuple[ResponseSignature, ...]:
        return tuple(
            _signature(self.system, state, self.open_words)
            for state in self.domain_states
        )

    @property
    def decomposition(self) -> InterfaceInflationDecompositionCertificate:
        union = self.union_certificate
        return certify_interface_inflation_decomposition(
            union.base_labels,
            union.closed_labels,
            self.open_labels,
        )

    @property
    def join_realizability_defect_bits(self) -> float:
        return self.decomposition.join_realizability_defect_bits

    @property
    def new_word_innovation_bits(self) -> float:
        return self.decomposition.new_word_innovation_bits

    @property
    def total_noncommutation_gap_bits(self) -> float:
        return self.decomposition.total_noncommutation_gap_bits

    @property
    def first_open_only_split_witness(self) -> OpenOnlyWordSplitWitness | None:
        split = self.decomposition.first_innovation_split_indices
        if split is None:
            return None
        left_index, right_index = split
        left_state = self.domain_states[left_index]
        right_state = self.domain_states[right_index]
        for word in self.open_only_words:
            left_trace = self.system.output_trace(left_state, word)
            right_trace = self.system.output_trace(right_state, word)
            if left_trace != right_trace:
                return OpenOnlyWordSplitWitness(
                    left_state=left_state,
                    right_state=right_state,
                    separating_word=word,
                    left_trace=left_trace,
                    right_trace=right_trace,
                )
        raise AssertionError("open refinement split was not witnessed by an open-only word")

    def verify(self) -> bool:
        try:
            domain = _normalize_domain(self.system, self.domain_states)
            if domain != self.domain_states:
                return False
            base = _normalize_word_family(
                self.system,
                self.base_words,
                "base_words",
                allow_empty=False,
            )
            if base != self.base_words:
                return False
            if not self.closed_word_families:
                return False
            closed = tuple(
                _normalize_word_family(
                    self.system,
                    family,
                    f"closed_word_families[{index}]",
                    allow_empty=False,
                )
                for index, family in enumerate(self.closed_word_families)
            )
            if closed != self.closed_word_families:
                return False
            open_only = _normalize_word_family(
                self.system,
                self.open_only_words,
                "open_only_words",
                allow_empty=True,
            )
            if open_only != self.open_only_words:
                return False
            union_words = set(_stable_word_union(closed))
            if union_words.intersection(open_only):
                return False

            union = self.union_certificate
            if not union.verify():
                return False
            decomposition = self.decomposition
            if not decomposition.verify():
                return False

            witness = self.first_open_only_split_witness
            if decomposition.has_new_word_innovation:
                if witness is None or not witness.verify(self.system):
                    return False
                if witness.separating_word not in self.open_only_words:
                    return False
            elif witness is not None:
                return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_operational_interface_inflation(
    system: FiniteControlledOutputSystem,
    domain_states: Iterable[int],
    base_words: Iterable[Iterable[Action]],
    closed_word_families: Iterable[Iterable[Iterable[Action]]],
    open_only_words: Iterable[Iterable[Action]],
) -> OperationalInterfaceInflationCertificate:
    """Certify one controlled-response interface inflation decomposition."""
    domain = _normalize_domain(system, domain_states)
    base = _normalize_word_family(system, base_words, "base_words", allow_empty=False)
    closed = tuple(
        _normalize_word_family(
            system,
            family,
            f"closed_word_families[{index}]",
            allow_empty=False,
        )
        for index, family in enumerate(closed_word_families)
    )
    open_only = _normalize_word_family(
        system,
        open_only_words,
        "open_only_words",
        allow_empty=True,
    )
    certificate = OperationalInterfaceInflationCertificate(
        system=system,
        domain_states=domain,
        base_words=base,
        closed_word_families=closed,
        open_only_words=open_only,
    )
    if not certificate.verify():
        raise ValueError("declared controlled open-grammar inflation contract does not verify")
    return certificate


__all__ = [
    "InterfaceInflationDecompositionCertificate",
    "certify_interface_inflation_decomposition",
    "OpenOnlyWordSplitWitness",
    "OperationalInterfaceInflationCertificate",
    "certify_operational_interface_inflation",
]
