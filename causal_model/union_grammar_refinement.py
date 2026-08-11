"""Exact union-grammar refinement and fibered interface capacity.

This module separates two layers that were previously bundled into coordinate
addressability arguments.

1. A purely combinatorial layer: several exact closed partitions refine one
   shared base partition. Their common refinement has at most the fibered
   Cartesian capacity allowed by the closed partitions inside each base block.
2. An operational controlled-response layer: when the declared open word family
   is exactly the union of the compared closed word families on one common
   domain, the exact open response quotient is exactly that common refinement.

The partition identity and Cartesian counting bound are elementary substrate;
they are not claimed as new mathematics. Their role in CCOC is to expose an
exact decomposition of extension--compression inflation into (i) the maximum
fibered refinement capacity allowed by the closed laws and (ii) a non-negative
joint-realizability / correlation defect.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2, prod
from typing import Hashable, Iterable

from .dynamic_boundary_blankets import Action, FiniteControlledOutputSystem

Label = Hashable
Word = tuple[Action, ...]
Trace = tuple[Hashable, ...]
ResponseSignature = tuple[Trace, ...]


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


def _ordered_unique(values: Iterable[Label]) -> tuple[Label, ...]:
    seen: set[Label] = set()
    result: list[Label] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def _partition_refines(fine: tuple[Label, ...], coarse: tuple[Label, ...]) -> bool:
    """Return whether equality of ``fine`` labels always implies coarse equality."""
    coarse_by_fine: dict[Label, Label] = {}
    for fine_label, coarse_label in zip(fine, coarse):
        if fine_label in coarse_by_fine:
            if coarse_by_fine[fine_label] != coarse_label:
                return False
        else:
            coarse_by_fine[fine_label] = coarse_label
    return True


@dataclass(frozen=True)
class PartitionRefinementCapacityCertificate:
    """Exact capacity accounting for common refinements over a shared base.

    ``base_labels`` encode a common coarse partition ``P_0`` of one finite
    comparison domain. Every row of ``closed_labels`` encodes one exact closed
    partition ``P_j`` and must refine ``P_0``.

    The common refinement is represented by the tuple of all closed labels at
    each state. Its realized block count is exact. The fibered capacity is the
    number of blocks that would be possible if, inside each base block, every
    Cartesian combination of closed labels were jointly realized.
    """

    base_labels: tuple[Label, ...]
    closed_labels: tuple[tuple[Label, ...], ...]

    @property
    def domain_size(self) -> int:
        return len(self.base_labels)

    @property
    def context_count(self) -> int:
        return len(self.closed_labels)

    @property
    def base_block_labels(self) -> tuple[Label, ...]:
        return _ordered_unique(self.base_labels)

    @property
    def base_block_count(self) -> int:
        return len(self.base_block_labels)

    @property
    def closed_block_counts(self) -> tuple[int, ...]:
        return tuple(len(set(labels)) for labels in self.closed_labels)

    @property
    def common_refinement_labels(self) -> tuple[tuple[Label, ...], ...]:
        return tuple(
            tuple(labels[state_index] for labels in self.closed_labels)
            for state_index in range(self.domain_size)
        )

    @property
    def common_refinement_block_count(self) -> int:
        return len(set(self.common_refinement_labels))

    def states_in_base_block(self, base_label: Label) -> tuple[int, ...]:
        if base_label not in set(self.base_labels):
            raise ValueError("base_label is not realized")
        return tuple(
            index for index, label in enumerate(self.base_labels) if label == base_label
        )

    def refinement_counts_in_base_block(self, base_label: Label) -> tuple[int, ...]:
        indices = self.states_in_base_block(base_label)
        return tuple(
            len({labels[index] for index in indices})
            for labels in self.closed_labels
        )

    @property
    def fibered_capacity_state_count(self) -> int:
        return sum(
            prod(self.refinement_counts_in_base_block(base_label))
            for base_label in self.base_block_labels
        )

    @property
    def fibered_capacity_bits(self) -> float:
        return log2(self.fibered_capacity_state_count)

    @property
    def common_refinement_bits(self) -> float:
        return log2(self.common_refinement_block_count)

    @property
    def closed_bits(self) -> tuple[float, ...]:
        return tuple(log2(count) for count in self.closed_block_counts)

    @property
    def exact_noncommutation_gap_bits(self) -> float:
        return self.common_refinement_bits - max(self.closed_bits)

    @property
    def capacity_gap_bits(self) -> float:
        return self.fibered_capacity_bits - max(self.closed_bits)

    @property
    def correlation_defect_bits(self) -> float:
        return self.fibered_capacity_bits - self.common_refinement_bits

    @property
    def saturates_fibered_capacity(self) -> bool:
        return self.common_refinement_block_count == self.fibered_capacity_state_count

    def realized_joint_count_in_base_block(self, base_label: Label) -> int:
        indices = self.states_in_base_block(base_label)
        return len({self.common_refinement_labels[index] for index in indices})

    def base_block_saturates_capacity(self, base_label: Label) -> bool:
        return self.realized_joint_count_in_base_block(base_label) == prod(
            self.refinement_counts_in_base_block(base_label)
        )

    def verify(self) -> bool:
        try:
            base = _normalize_labels(self.base_labels, "base_labels")
            if base != self.base_labels:
                return False
            closed = _normalize_closed_labels(self.closed_labels, len(base))
            if closed != self.closed_labels:
                return False
            if any(not _partition_refines(labels, base) for labels in closed):
                return False
            if self.common_refinement_block_count > self.fibered_capacity_state_count:
                return False
            if self.correlation_defect_bits < -1e-12:
                return False
            if abs(
                self.exact_noncommutation_gap_bits
                - (self.capacity_gap_bits - self.correlation_defect_bits)
            ) > 1e-12:
                return False
            if self.saturates_fibered_capacity != all(
                self.base_block_saturates_capacity(base_label)
                for base_label in self.base_block_labels
            ):
                return False
            return True
        except (TypeError, ValueError):
            return False


def certify_partition_refinement_capacity(
    base_labels: Iterable[Label],
    closed_labels: Iterable[Iterable[Label]],
) -> PartitionRefinementCapacityCertificate:
    """Certify the exact common-refinement capacity decomposition."""
    base = _normalize_labels(base_labels, "base_labels")
    closed = _normalize_closed_labels(closed_labels, len(base))
    certificate = PartitionRefinementCapacityCertificate(base, closed)
    if not certificate.verify():
        raise ValueError(
            "declared closed partitions do not form a valid shared-base refinement family"
        )
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
    family: Iterable[Iterable[Action]],
    name: str,
) -> tuple[Word, ...]:
    try:
        words = tuple(tuple(word) for word in family)
    except TypeError as error:
        raise ValueError(f"{name} must be an iterable of words") from error
    if not words:
        raise ValueError(f"{name} must contain at least one word")
    normalized = tuple(system.normalize_word(word) for word in words)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{name} must not contain duplicate words")
    return normalized


def _stable_word_union(
    families: tuple[tuple[Word, ...], ...],
) -> tuple[Word, ...]:
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
class UnionGrammarRefinementCertificate:
    """Operational finite replay of the union-grammar common-refinement theorem."""

    system: FiniteControlledOutputSystem
    domain_states: tuple[int, ...]
    base_words: tuple[Word, ...]
    closed_word_families: tuple[tuple[Word, ...], ...]

    @property
    def context_count(self) -> int:
        return len(self.closed_word_families)

    @property
    def open_words(self) -> tuple[Word, ...]:
        return _stable_word_union(self.closed_word_families)

    @property
    def base_labels(self) -> tuple[ResponseSignature, ...]:
        return tuple(
            _signature(self.system, state, self.base_words)
            for state in self.domain_states
        )

    @property
    def closed_labels(self) -> tuple[tuple[ResponseSignature, ...], ...]:
        return tuple(
            tuple(_signature(self.system, state, words) for state in self.domain_states)
            for words in self.closed_word_families
        )

    @property
    def open_labels(self) -> tuple[ResponseSignature, ...]:
        return tuple(
            _signature(self.system, state, self.open_words)
            for state in self.domain_states
        )

    @property
    def joint_closed_labels(self) -> tuple[tuple[ResponseSignature, ...], ...]:
        return tuple(
            tuple(labels[index] for labels in self.closed_labels)
            for index in range(len(self.domain_states))
        )

    @property
    def refinement_capacity(self) -> PartitionRefinementCapacityCertificate:
        return certify_partition_refinement_capacity(self.base_labels, self.closed_labels)

    @property
    def open_block_count(self) -> int:
        return len(set(self.open_labels))

    @property
    def closed_block_counts(self) -> tuple[int, ...]:
        return self.refinement_capacity.closed_block_counts

    @property
    def correlation_defect_bits(self) -> float:
        return self.refinement_capacity.correlation_defect_bits

    @property
    def exact_noncommutation_gap_bits(self) -> float:
        return self.refinement_capacity.exact_noncommutation_gap_bits

    @property
    def fibered_capacity_state_count(self) -> int:
        return self.refinement_capacity.fibered_capacity_state_count

    def verify(self) -> bool:
        try:
            domain = _normalize_domain(self.system, self.domain_states)
            if domain != self.domain_states:
                return False
            base = _normalize_word_family(self.system, self.base_words, "base_words")
            if base != self.base_words:
                return False
            if not self.closed_word_families:
                return False
            normalized_closed = tuple(
                _normalize_word_family(
                    self.system,
                    family,
                    f"closed_word_families[{index}]",
                )
                for index, family in enumerate(self.closed_word_families)
            )
            if normalized_closed != self.closed_word_families:
                return False
            base_set = set(base)
            if any(not base_set.issubset(set(family)) for family in normalized_closed):
                return False

            # Exact union-grammar identity: equality under all words in the union
            # is equivalent to equality of every closed-context response signature.
            for left in range(len(domain)):
                for right in range(len(domain)):
                    if (self.open_labels[left] == self.open_labels[right]) != (
                        self.joint_closed_labels[left]
                        == self.joint_closed_labels[right]
                    ):
                        return False

            capacity = self.refinement_capacity
            if not capacity.verify():
                return False
            if self.open_block_count != capacity.common_refinement_block_count:
                return False
            return True
        except (TypeError, ValueError):
            return False


def certify_union_grammar_refinement(
    system: FiniteControlledOutputSystem,
    domain_states: Iterable[int],
    base_words: Iterable[Iterable[Action]],
    closed_word_families: Iterable[Iterable[Iterable[Action]]],
) -> UnionGrammarRefinementCertificate:
    """Certify one finite union-grammar refinement/capacity instance."""
    domain = _normalize_domain(system, domain_states)
    base = _normalize_word_family(system, base_words, "base_words")
    closed = tuple(
        _normalize_word_family(
            system,
            family,
            f"closed_word_families[{index}]",
        )
        for index, family in enumerate(closed_word_families)
    )
    certificate = UnionGrammarRefinementCertificate(system, domain, base, closed)
    if not certificate.verify():
        raise ValueError("declared union-grammar refinement contract does not verify")
    return certificate


__all__ = [
    "Label",
    "Word",
    "Trace",
    "ResponseSignature",
    "PartitionRefinementCapacityCertificate",
    "certify_partition_refinement_capacity",
    "UnionGrammarRefinementCertificate",
    "certify_union_grammar_refinement",
]
