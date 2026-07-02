"""Sharp extension--compression noncommutation theorem.

The central statement is not that one particular coordinate table has many
states.  It is the following injection principle.

For an addressable product subsystem ``I x E_1 x ... x E_q``, suppose a legal
future word decodes the inside coordinate and, for each exterior module ``j``, a
legal future word decodes ``E_j`` independently of all other coordinates.  Then
no exact open-safe interface may merge two product states:

    K_open >= log2|I| + sum_j log2|E_j|.

If a fixed closed context ``j`` admits a supplied exact interface that factors
through ``(I, E_j)``, then that factorization gives the upper bound
``K_closed,j <= log2|I| + log2|E_j|``.  Hence extension and compression need not
commute:

    K_open - max_j K_closed,j
      >= sum_j log2|E_j| - max_j log2|E_j|.

The existing coordinate witness realizes equality for binary modules.  The
existing relay-tree compiler realizes the same sharp family with a constant-size
local node/message grammar, pairwise messages, and maximum degree three.  The
family still has a growing set of selectable ports, so this is not a claim of a
constant-size global action alphabet.  This module makes that theorem spine
explicit; it does not add a new ecosystem design language.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import log2, prod
from typing import Iterable

from .extension_compression import ExtensionCompressionCertificate, certify_extension_compression
from .relay_tree_compilation import BoundedDegreeCompilationCertificate, certify_bounded_degree_compilation

ProductState = tuple[int, ...]


def _positive_int(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _normalize_cardinalities(exterior_cardinalities: Iterable[int]) -> tuple[int, ...]:
    try:
        values = tuple(exterior_cardinalities)
    except TypeError as error:
        raise ValueError("exterior_cardinalities must be iterable") from error
    if not values:
        raise ValueError("at least one exterior module is required")
    for index, value in enumerate(values):
        _positive_int(value, f"exterior_cardinalities[{index}]")
    return values


def _product_states(inside_cardinality: int, exterior_cardinalities: tuple[int, ...]) -> tuple[ProductState, ...]:
    return tuple(product(range(inside_cardinality), *(range(size) for size in exterior_cardinalities)))


def decoder_coordinate(left: ProductState, right: ProductState) -> int:
    """Return 0 for the inside decoder, else the differing exterior decoder index.

    This is the finite combinatorial core of the injection proof: any distinct
    product states differ in some coordinate, and the corresponding declared
    future word separates them under the theorem's operational decoder premise.
    """
    if left == right:
        raise ValueError("decoder_coordinate requires distinct product states")
    for index, (left_value, right_value) in enumerate(zip(left, right)):
        if left_value != right_value:
            return index
    raise AssertionError("distinct equal-length tuples must differ in a coordinate")


@dataclass(frozen=True)
class AddressableProductLowerBoundCertificate:
    """Arithmetic/injection certificate for the decoder-based product theorem.

    The booleans represent the theorem hypotheses: a base decoder and one
    exterior decoder per module exist as declared legal future words.  The
    certificate enumerates only the finite product instance to replay that any
    unequal pair has a concrete decoder coordinate; the general proof is the
    coordinate injection in the documentation.
    """

    inside_cardinality: int
    exterior_cardinalities: tuple[int, ...]
    base_word_decodes_inside: bool
    module_words_decode_exteriors: tuple[bool, ...]
    checked_distinct_pairs: int

    @property
    def exterior_module_count(self) -> int:
        return len(self.exterior_cardinalities)

    @property
    def open_state_lower_bound(self) -> int:
        return self.inside_cardinality * prod(self.exterior_cardinalities)

    @property
    def open_bits_lower_bound(self) -> float:
        return log2(self.open_state_lower_bound)

    @property
    def expected_checked_pairs(self) -> int:
        return self.open_state_lower_bound * (self.open_state_lower_bound - 1) // 2

    def verify(self) -> bool:
        try:
            _positive_int(self.inside_cardinality, "inside_cardinality")
            cards = _normalize_cardinalities(self.exterior_cardinalities)
            if cards != self.exterior_cardinalities:
                return False
            if not self.base_word_decodes_inside:
                return False
            if self.module_words_decode_exteriors != (True,) * len(cards):
                return False
            states = _product_states(self.inside_cardinality, cards)
            if len(states) != self.open_state_lower_bound:
                return False
            if self.checked_distinct_pairs != self.expected_checked_pairs:
                return False
            # A separate decoder word is available for the first coordinate in
            # which any pair differs.  This is the explicit finite replay of the
            # injection hypothesis.
            for left, right in combinations(states, 2):
                coordinate = decoder_coordinate(left, right)
                if coordinate == 0 and not self.base_word_decodes_inside:
                    return False
                if coordinate > 0 and not self.module_words_decode_exteriors[coordinate - 1]:
                    return False
            return True
        except (TypeError, ValueError):
            return False


def certify_addressable_product_lower_bound(
    inside_cardinality: int,
    exterior_cardinalities: Iterable[int],
) -> AddressableProductLowerBoundCertificate:
    cards = _normalize_cardinalities(exterior_cardinalities)
    _positive_int(inside_cardinality, "inside_cardinality")
    state_count = inside_cardinality * prod(cards)
    certificate = AddressableProductLowerBoundCertificate(
        inside_cardinality=inside_cardinality,
        exterior_cardinalities=cards,
        base_word_decodes_inside=True,
        module_words_decode_exteriors=(True,) * len(cards),
        checked_distinct_pairs=state_count * (state_count - 1) // 2,
    )
    if not certificate.verify():
        raise AssertionError("addressable product lower-bound certificate did not verify")
    return certificate


@dataclass(frozen=True)
class ClosedContextFactorizationCertificate:
    """Closed-context interface upper bound under the declared factorization premise.

    ``closed_context_state_counts`` records the cardinality of the supplied
    factorized summaries, not a claim that these summaries are minimal for every
    possible closed system.  The resulting upper bound is exactly what the
    noncommutation inequality needs.
    """

    product_certificate: AddressableProductLowerBoundCertificate
    closed_context_state_counts: tuple[int, ...]

    @property
    def inside_cardinality(self) -> int:
        return self.product_certificate.inside_cardinality

    @property
    def exterior_cardinalities(self) -> tuple[int, ...]:
        return self.product_certificate.exterior_cardinalities

    @property
    def closed_bits(self) -> tuple[float, ...]:
        return tuple(log2(count) for count in self.closed_context_state_counts)

    @property
    def largest_closed_bits(self) -> float:
        return max(self.closed_bits)

    @property
    def noncommutation_gap_lower_bound(self) -> float:
        return self.product_certificate.open_bits_lower_bound - self.largest_closed_bits

    @property
    def expected_gap_lower_bound(self) -> float:
        return sum(log2(cardinality) for cardinality in self.exterior_cardinalities) - max(
            log2(cardinality) for cardinality in self.exterior_cardinalities
        )

    def verify(self) -> bool:
        try:
            if not self.product_certificate.verify():
                return False
            expected = tuple(
                self.inside_cardinality * cardinality
                for cardinality in self.exterior_cardinalities
            )
            if self.closed_context_state_counts != expected:
                return False
            return abs(self.noncommutation_gap_lower_bound - self.expected_gap_lower_bound) < 1e-12
        except (TypeError, ValueError):
            return False


def certify_closed_context_factorization(
    inside_cardinality: int,
    exterior_cardinalities: Iterable[int],
) -> ClosedContextFactorizationCertificate:
    product_certificate = certify_addressable_product_lower_bound(inside_cardinality, exterior_cardinalities)
    certificate = ClosedContextFactorizationCertificate(
        product_certificate=product_certificate,
        closed_context_state_counts=tuple(
            inside_cardinality * cardinality
            for cardinality in product_certificate.exterior_cardinalities
        ),
    )
    if not certificate.verify():
        raise AssertionError("closed-context factorization certificate did not verify")
    return certificate


@dataclass(frozen=True)
class RelayTreeSharpnessCertificate:
    """Sharp binary realization under a constant local grammar and degree bound."""

    module_count: int
    product_bound: AddressableProductLowerBoundCertificate
    closed_factorization: ClosedContextFactorizationCertificate
    coordinate_witness: ExtensionCompressionCertificate
    relay_compilation: BoundedDegreeCompilationCertificate

    @property
    def closed_bits(self) -> int:
        return 2

    @property
    def open_bits(self) -> int:
        return self.module_count + 1

    @property
    def gap_bits(self) -> int:
        return self.module_count - 1

    def verify(self) -> bool:
        try:
            _positive_int(self.module_count, "module_count")
            if not self.product_bound.verify() or not self.closed_factorization.verify():
                return False
            if self.product_bound.inside_cardinality != 2:
                return False
            if self.product_bound.exterior_cardinalities != (2,) * self.module_count:
                return False
            if self.coordinate_witness.module_count != self.module_count or not self.coordinate_witness.verify():
                return False
            if self.relay_compilation.module_count != self.module_count or not self.relay_compilation.verify():
                return False
            if self.closed_factorization.closed_context_state_counts != (4,) * self.module_count:
                return False
            if self.product_bound.open_state_lower_bound != 2 ** (self.module_count + 1):
                return False
            if self.coordinate_witness.open_interface_bits != self.open_bits:
                return False
            if self.coordinate_witness.closed_interface_bits != (self.closed_bits,) * self.module_count:
                return False
            if self.relay_compilation.open_interface_bits != self.open_bits:
                return False
            if self.relay_compilation.closed_interface_bits != (self.closed_bits,) * self.module_count:
                return False
            if self.relay_compilation.grammar.maximum_degree != 3:
                return False
            return self.gap_bits == self.module_count - 1
        except (TypeError, ValueError):
            return False


def certify_relay_tree_sharpness(module_count: int) -> RelayTreeSharpnessCertificate:
    _positive_int(module_count, "module_count")
    product_bound = certify_addressable_product_lower_bound(2, (2,) * module_count)
    factorization = certify_closed_context_factorization(2, (2,) * module_count)
    certificate = RelayTreeSharpnessCertificate(
        module_count=module_count,
        product_bound=product_bound,
        closed_factorization=factorization,
        coordinate_witness=certify_extension_compression(module_count),
        relay_compilation=certify_bounded_degree_compilation(module_count),
    )
    if not certificate.verify():
        raise AssertionError("relay-tree sharpness certificate did not verify")
    return certificate


def exhaustive_noncommutation_summary(max_module_count: int = 5) -> tuple[RelayTreeSharpnessCertificate, ...]:
    _positive_int(max_module_count, "max_module_count")
    return tuple(certify_relay_tree_sharpness(module_count) for module_count in range(1, max_module_count + 1))
