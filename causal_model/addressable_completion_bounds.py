"""Operational product lower bounds for exterior completion interfaces.

This module formalizes a reusable exact theorem schema. A finite window state
factorizes into one visible inside coordinate and independently addressable
exterior completion coordinates. Each coordinate comes with a declared response
word whose response decodes that coordinate.

The mathematical lower bound is not obtained by merely counting a partition:
for every pair of distinct product states, a concrete permitted response word
is supplied that separates them. The resulting injection gives

    K_open >= log2 |I| + sum_j log2 |E_j|.

The canonical finite response family realizes equality, provides exact
closed-versus-open gaps, and supplies an observational nonidentifiability pair:
a closed model and an open model share all passive traces but have different
counterfactual interface complexity.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import log2, prod
from typing import Iterable

ProductState = tuple[int, ...]
Word = str
Response = tuple[int, ...]
OBSERVE: Word = "observe"


def _normalize_factor_cardinalities(factor_cardinalities: Iterable[int]) -> tuple[int, ...]:
    try:
        values = tuple(factor_cardinalities)
    except TypeError as error:
        raise ValueError("factor_cardinalities must be an iterable of positive integers") from error
    if len(values) < 2:
        raise ValueError("a product witness requires one inside factor and at least one exterior factor")
    for index, value in enumerate(values):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError("every factor cardinality must be a positive integer")
        if index > 0 and value < 2:
            raise ValueError("every exterior factor must have at least two distinguishable values")
    return values


def _normalize_active_indices(
    factor_cardinalities: tuple[int, ...],
    active_exterior_indices: Iterable[int],
) -> tuple[int, ...]:
    try:
        indices = tuple(active_exterior_indices)
    except TypeError as error:
        raise ValueError("active_exterior_indices must be an iterable of exterior indices") from error
    if any(not isinstance(index, int) or isinstance(index, bool) for index in indices):
        raise ValueError("active exterior indices must be integers")
    if tuple(sorted(set(indices))) != indices:
        raise ValueError("active exterior indices must be unique and sorted")
    if any(index < 1 or index >= len(factor_cardinalities) for index in indices):
        raise ValueError("active exterior index is outside the exterior factor range")
    return indices


def read_word(exterior_index: int) -> Word:
    if not isinstance(exterior_index, int) or isinstance(exterior_index, bool) or exterior_index < 1:
        raise ValueError("exterior_index must be a positive integer")
    return f"read:{exterior_index}"


def _parse_read_word(factor_cardinalities: tuple[int, ...], word: Word) -> int:
    if not isinstance(word, str) or not word.startswith("read:"):
        raise ValueError(f"unknown response word: {word!r}")
    suffix = word.split(":", 1)[1]
    try:
        index = int(suffix)
    except ValueError as error:
        raise ValueError(f"invalid read word: {word!r}") from error
    if not 1 <= index < len(factor_cardinalities):
        raise ValueError("read word references an unavailable exterior factor")
    return index


@dataclass(frozen=True)
class CanonicalAddressableProduct:
    """Finite controlled response system realizing the addressability hypotheses.

    Factor 0 is the visible inside coordinate I. Factors 1..q are exterior
    completion coordinates E_j. ``observe`` decodes I; ``read:j`` decodes E_j.
    The response additionally carries the inside value, but the designated
    coordinate decoder reads the appropriate component exactly.
    """

    factor_cardinalities: tuple[int, ...]

    def __post_init__(self) -> None:
        normalized = _normalize_factor_cardinalities(self.factor_cardinalities)
        object.__setattr__(self, "factor_cardinalities", normalized)

    @property
    def inside_cardinality(self) -> int:
        return self.factor_cardinalities[0]

    @property
    def exterior_indices(self) -> tuple[int, ...]:
        return tuple(range(1, len(self.factor_cardinalities)))

    @property
    def exterior_cardinalities(self) -> tuple[int, ...]:
        return self.factor_cardinalities[1:]

    @property
    def state_count(self) -> int:
        return prod(self.factor_cardinalities)

    @property
    def passive_words(self) -> tuple[Word, ...]:
        return (OBSERVE,)

    @property
    def open_words(self) -> tuple[Word, ...]:
        return (OBSERVE,) + tuple(read_word(index) for index in self.exterior_indices)

    @property
    def states(self) -> tuple[ProductState, ...]:
        return tuple(product(*(range(cardinality) for cardinality in self.factor_cardinalities)))

    def validate_state(self, state: ProductState) -> None:
        if not isinstance(state, tuple) or len(state) != len(self.factor_cardinalities):
            raise ValueError("state must have one coordinate per product factor")
        for index, (value, cardinality) in enumerate(zip(state, self.factor_cardinalities)):
            if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value < cardinality:
                raise ValueError(f"state coordinate {index} is outside its factor range")

    def validate_word(self, word: Word) -> None:
        if word == OBSERVE:
            return
        _parse_read_word(self.factor_cardinalities, word)

    def response(self, state: ProductState, word: Word) -> Response:
        """Deterministic response to one permitted controlled query word."""
        self.validate_state(state)
        self.validate_word(word)
        if word == OBSERVE:
            return (state[0],)
        index = _parse_read_word(self.factor_cardinalities, word)
        return (state[0], state[index])

    def coordinate_word(self, coordinate_index: int) -> Word:
        if not isinstance(coordinate_index, int) or isinstance(coordinate_index, bool):
            raise ValueError("coordinate_index must be an integer")
        if coordinate_index == 0:
            return OBSERVE
        if coordinate_index not in self.exterior_indices:
            raise ValueError("coordinate index is outside the product factors")
        return read_word(coordinate_index)

    def decode_coordinate(self, coordinate_index: int, response: Response) -> int:
        if coordinate_index == 0:
            if len(response) != 1:
                raise ValueError("inside observation response must have one component")
            return response[0]
        if coordinate_index not in self.exterior_indices:
            raise ValueError("coordinate index is outside the product factors")
        if len(response) != 2:
            raise ValueError("exterior read response must have two components")
        return response[1]

    def response_signature(self, state: ProductState, words: Iterable[Word]) -> tuple[Response, ...]:
        normalized = tuple(words)
        if not normalized:
            raise ValueError("a response grammar must contain at least one word")
        return tuple(self.response(state, word) for word in normalized)

    def partition(self, words: Iterable[Word]) -> tuple[tuple[ProductState, ...], ...]:
        normalized = tuple(words)
        buckets: dict[tuple[Response, ...], list[ProductState]] = {}
        for state in self.states:
            buckets.setdefault(self.response_signature(state, normalized), []).append(state)
        return tuple(sorted((tuple(block) for block in buckets.values()), key=lambda block: block[0]))

    def passive_partition(self) -> tuple[tuple[ProductState, ...], ...]:
        return self.partition(self.passive_words)

    def closed_words(self, exterior_index: int) -> tuple[Word, Word]:
        if exterior_index not in self.exterior_indices:
            raise ValueError("closed context must choose an exterior factor")
        return (OBSERVE, read_word(exterior_index))

    def closed_partition(self, exterior_index: int) -> tuple[tuple[ProductState, ...], ...]:
        return self.partition(self.closed_words(exterior_index))

    def open_partition(self) -> tuple[tuple[ProductState, ...], ...]:
        return self.partition(self.open_words)

    def boundary_blanket_words(self, active_exterior_indices: Iterable[int]) -> tuple[Word, ...]:
        indices = _normalize_active_indices(self.factor_cardinalities, active_exterior_indices)
        return (OBSERVE,) + tuple(read_word(index) for index in indices)

    def boundary_blanket_partition(self, active_exterior_indices: Iterable[int]) -> tuple[tuple[ProductState, ...], ...]:
        return self.partition(self.boundary_blanket_words(active_exterior_indices))


@dataclass(frozen=True)
class SeparatingWordCertificate:
    """Concrete permitted response word separating two product states."""

    factor_cardinalities: tuple[int, ...]
    left: ProductState
    right: ProductState
    word: Word
    left_response: Response
    right_response: Response

    def verify(self) -> bool:
        try:
            system = CanonicalAddressableProduct(self.factor_cardinalities)
            system.validate_state(self.left)
            system.validate_state(self.right)
            if self.left == self.right:
                return False
            system.validate_word(self.word)
            if self.left_response != system.response(self.left, self.word):
                return False
            if self.right_response != system.response(self.right, self.word):
                return False
            return self.left_response != self.right_response
        except ValueError:
            return False


def separating_word_certificate(
    factor_cardinalities: Iterable[int],
    left: ProductState,
    right: ProductState,
) -> SeparatingWordCertificate:
    """Return the coordinate readout word that separates any unequal product states."""
    system = CanonicalAddressableProduct(tuple(factor_cardinalities))
    system.validate_state(left)
    system.validate_state(right)
    if left == right:
        raise ValueError("a separating certificate requires distinct states")
    coordinate = next(index for index, (a, b) in enumerate(zip(left, right)) if a != b)
    word = system.coordinate_word(coordinate)
    certificate = SeparatingWordCertificate(
        factor_cardinalities=system.factor_cardinalities,
        left=left,
        right=right,
        word=word,
        left_response=system.response(left, word),
        right_response=system.response(right, word),
    )
    if not certificate.verify():
        raise AssertionError("constructed separating-word certificate did not verify")
    return certificate


@dataclass(frozen=True)
class AddressableCompletionProductCertificate:
    """Exact product lower bound and closed/open gap for a canonical response family.

    The certificate operationally verifies that every coordinate has a response
    word that decodes it. Pairwise separation then injects the whole product
    state space into the open trace quotient.
    """

    factor_cardinalities: tuple[int, ...]
    passive_block_count: int
    closed_block_counts: tuple[int, ...]
    open_block_count: int
    checked_separating_pairs: int

    @property
    def inside_cardinality(self) -> int:
        return self.factor_cardinalities[0]

    @property
    def exterior_cardinalities(self) -> tuple[int, ...]:
        return self.factor_cardinalities[1:]

    @property
    def product_state_count(self) -> int:
        return prod(self.factor_cardinalities)

    @property
    def passive_interface_bits(self) -> float:
        return log2(self.passive_block_count)

    @property
    def closed_interface_bits(self) -> tuple[float, ...]:
        return tuple(log2(count) for count in self.closed_block_counts)

    @property
    def open_interface_bits(self) -> float:
        return log2(self.open_block_count)

    @property
    def product_lower_bound_bits(self) -> float:
        return sum(log2(cardinality) for cardinality in self.factor_cardinalities)

    @property
    def extension_compression_gap_bits(self) -> float:
        return self.open_interface_bits - max(self.closed_interface_bits)

    @property
    def gap_lower_bound_bits(self) -> float:
        return sum(log2(cardinality) for cardinality in self.exterior_cardinalities) - max(
            log2(cardinality) for cardinality in self.exterior_cardinalities
        )

    @property
    def expected_pair_count(self) -> int:
        return self.product_state_count * (self.product_state_count - 1) // 2

    def verify(self) -> bool:
        try:
            system = CanonicalAddressableProduct(self.factor_cardinalities)
            if self.passive_block_count != system.inside_cardinality:
                return False
            expected_closed = tuple(
                system.inside_cardinality * cardinality
                for cardinality in system.exterior_cardinalities
            )
            if self.closed_block_counts != expected_closed:
                return False
            if self.open_block_count != system.state_count:
                return False
            if self.checked_separating_pairs != self.expected_pair_count:
                return False
            if len(system.passive_partition()) != self.passive_block_count:
                return False
            if tuple(
                len(system.closed_partition(index)) for index in system.exterior_indices
            ) != self.closed_block_counts:
                return False
            if len(system.open_partition()) != self.open_block_count:
                return False
            if any(len(block) != 1 for block in system.open_partition()):
                return False
            for state in system.states:
                for index in range(len(system.factor_cardinalities)):
                    word = system.coordinate_word(index)
                    decoded = system.decode_coordinate(index, system.response(state, word))
                    if decoded != state[index]:
                        return False
            for left, right in combinations(system.states, 2):
                if not separating_word_certificate(system.factor_cardinalities, left, right).verify():
                    return False
            tolerance = 1e-12
            if abs(self.open_interface_bits - self.product_lower_bound_bits) > tolerance:
                return False
            if abs(self.extension_compression_gap_bits - self.gap_lower_bound_bits) > tolerance:
                return False
            return True
        except (AssertionError, ValueError):
            return False


def certify_addressable_completion_product(
    factor_cardinalities: Iterable[int],
) -> AddressableCompletionProductCertificate:
    """Construct the exact product lower-bound certificate.

    Factor 0 is the inside state I and factors 1..q are independently
    addressable exterior completion coordinates E_j.
    """
    system = CanonicalAddressableProduct(tuple(factor_cardinalities))
    certificate = AddressableCompletionProductCertificate(
        factor_cardinalities=system.factor_cardinalities,
        passive_block_count=len(system.passive_partition()),
        closed_block_counts=tuple(
            len(system.closed_partition(index)) for index in system.exterior_indices
        ),
        open_block_count=len(system.open_partition()),
        checked_separating_pairs=system.state_count * (system.state_count - 1) // 2,
    )
    if not certificate.verify():
        raise AssertionError("addressable-completion product certificate did not verify")
    return certificate


@dataclass(frozen=True)
class FiniteBoundaryBlanketCertificate:
    """Exact finite factorization through a declared inside-plus-boundary summary."""

    factor_cardinalities: tuple[int, ...]
    active_exterior_indices: tuple[int, ...]
    boundary_block_count: int

    @property
    def inside_cardinality(self) -> int:
        return self.factor_cardinalities[0]

    @property
    def boundary_cardinality(self) -> int:
        return prod(self.factor_cardinalities[index] for index in self.active_exterior_indices)

    @property
    def upper_bound_bits(self) -> float:
        return log2(self.inside_cardinality) + log2(self.boundary_cardinality)

    @property
    def realized_interface_bits(self) -> float:
        return log2(self.boundary_block_count)

    def verify(self) -> bool:
        try:
            system = CanonicalAddressableProduct(self.factor_cardinalities)
            indices = _normalize_active_indices(system.factor_cardinalities, self.active_exterior_indices)
            expected_block_count = system.inside_cardinality * prod(
                system.factor_cardinalities[index] for index in indices
            )
            if self.boundary_block_count != expected_block_count:
                return False
            words = system.boundary_blanket_words(indices)
            if len(system.boundary_blanket_partition(indices)) != self.boundary_block_count:
                return False
            for left, right in combinations(system.states, 2):
                same_summary = (
                    left[0] == right[0]
                    and all(left[index] == right[index] for index in indices)
                )
                same_responses = system.response_signature(left, words) == system.response_signature(right, words)
                if same_summary != same_responses:
                    return False
            return abs(self.upper_bound_bits - self.realized_interface_bits) <= 1e-12
        except ValueError:
            return False


def certify_finite_boundary_blanket(
    factor_cardinalities: Iterable[int],
    active_exterior_indices: Iterable[int],
) -> FiniteBoundaryBlanketCertificate:
    """Certify a finite sufficient blanket in the canonical response family."""
    system = CanonicalAddressableProduct(tuple(factor_cardinalities))
    indices = _normalize_active_indices(system.factor_cardinalities, active_exterior_indices)
    certificate = FiniteBoundaryBlanketCertificate(
        factor_cardinalities=system.factor_cardinalities,
        active_exterior_indices=indices,
        boundary_block_count=len(system.boundary_blanket_partition(indices)),
    )
    if not certificate.verify():
        raise AssertionError("finite boundary blanket certificate did not verify")
    return certificate


@dataclass(frozen=True)
class PassiveClosureNonidentifiabilityCertificate:
    """A closed/open model pair with identical passive responses but distinct open quotients."""

    factor_cardinalities: tuple[int, ...]
    passive_block_count: int
    closed_model_open_block_count: int
    open_model_open_block_count: int
    separating_state: ProductState
    separating_word: Word
    closed_response: Response
    open_response: Response

    @property
    def inside_interface_bits(self) -> float:
        return log2(self.passive_block_count)

    @property
    def closed_model_open_bits(self) -> float:
        return log2(self.closed_model_open_block_count)

    @property
    def open_model_open_bits(self) -> float:
        return log2(self.open_model_open_block_count)

    def verify(self) -> bool:
        try:
            system = CanonicalAddressableProduct(self.factor_cardinalities)
            system.validate_state(self.separating_state)
            if self.separating_word not in system.open_words or self.separating_word == OBSERVE:
                return False
            if self.passive_block_count != system.inside_cardinality:
                return False
            if self.closed_model_open_block_count != system.inside_cardinality:
                return False
            if self.open_model_open_block_count != system.state_count:
                return False
            for state in system.states:
                if (state[0],) != system.response(state, OBSERVE):
                    return False
            if self.closed_response != (self.separating_state[0],):
                return False
            if self.open_response != system.response(self.separating_state, self.separating_word):
                return False
            if self.closed_response == self.open_response:
                return False
            return self.open_model_open_bits > self.closed_model_open_bits
        except ValueError:
            return False


def certify_passive_closure_nonidentifiability(
    factor_cardinalities: Iterable[int],
) -> PassiveClosureNonidentifiabilityCertificate:
    """Construct a passive-indistinguishable closed/open model pair.

    The closed comparator answers every read with the visible inside coordinate.
    The open model is the addressable product system. They agree on all passive
    words (repeated ``observe``), but differ on a permitted exterior read.
    """
    system = CanonicalAddressableProduct(tuple(factor_cardinalities))
    port = system.exterior_indices[0]
    state_values = [0] * len(system.factor_cardinalities)
    state_values[port] = 1
    state = tuple(state_values)
    word = read_word(port)
    certificate = PassiveClosureNonidentifiabilityCertificate(
        factor_cardinalities=system.factor_cardinalities,
        passive_block_count=system.inside_cardinality,
        closed_model_open_block_count=system.inside_cardinality,
        open_model_open_block_count=system.state_count,
        separating_state=state,
        separating_word=word,
        closed_response=(state[0],),
        open_response=system.response(state, word),
    )
    if not certificate.verify():
        raise AssertionError("passive closure nonidentifiability certificate did not verify")
    return certificate
