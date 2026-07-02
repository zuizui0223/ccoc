"""Operational witnesses for the addressable-product theorem.

The central Extension--Compression theorem has two layers:

1. an analytic injection argument: independently decoded coordinates force an
   open-safe interface to distinguish every product state; and
2. a finite application: a declared controlled system actually contains such a
   reachable product subsystem, with concrete legal decoder words and concrete
   decoder functions.

Earlier arithmetic certificates replayed layer 1 for cardinalities. This module
implements layer 2. It checks an actual finite controlled output system,
injective product embedding, declared decoder words, and finite closed-context
factorization contracts. It never infers a biological grammar: every word family
is explicitly supplied by the caller.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import log2
from typing import Callable, Hashable, Iterable

from .dynamic_boundary_blankets import Action, FiniteControlledOutputSystem

ProductState = tuple[int, ...]
Word = tuple[Action, ...]
Trace = tuple[Hashable, ...]
TraceDecoder = Callable[[Trace], Hashable]
ClosedFactorMap = Callable[[ProductState], Hashable]


def _positive_int(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _normalize_cardinalities(exterior_cardinalities: Iterable[int]) -> tuple[int, ...]:
    try:
        cards = tuple(exterior_cardinalities)
    except TypeError as error:
        raise ValueError("exterior_cardinalities must be iterable") from error
    if not cards:
        raise ValueError("at least one exterior module is required")
    for index, cardinality in enumerate(cards):
        _positive_int(cardinality, f"exterior_cardinalities[{index}]")
    return cards


def _normalize_word(system: FiniteControlledOutputSystem, word: Iterable[Action], name: str) -> Word:
    try:
        normalized = tuple(word)
    except TypeError as error:
        raise ValueError(f"{name} must be an iterable of actions") from error
    try:
        return system.normalize_word(normalized)
    except ValueError as error:
        raise ValueError(f"{name} is not legal for the declared controlled system") from error


def _product_states(inside_cardinality: int, exterior_cardinalities: tuple[int, ...]) -> tuple[ProductState, ...]:
    return tuple(product(range(inside_cardinality), *(range(cardinality) for cardinality in exterior_cardinalities)))


def first_differing_coordinate(left: ProductState, right: ProductState) -> int:
    """Return the first coordinate at which two unequal product states differ."""
    if left == right:
        raise ValueError("first_differing_coordinate requires distinct product states")
    for coordinate, (left_value, right_value) in enumerate(zip(left, right)):
        if left_value != right_value:
            return coordinate
    raise AssertionError("distinct equal-length tuples must differ")


def standard_closed_projection(module_index: int) -> ClosedFactorMap:
    """Return the standard fixed-context map ``(i,e_1,...,e_q) -> (i,e_j)``."""
    if not isinstance(module_index, int) or isinstance(module_index, bool) or module_index < 0:
        raise ValueError("module_index must be a non-negative integer")

    def projection(state: ProductState) -> tuple[int, int]:
        if len(state) <= module_index + 1:
            raise ValueError("product state does not contain the requested exterior module")
        return (state[0], state[module_index + 1])

    return projection


@dataclass(frozen=True)
class OperationalAddressableProductCertificate:
    """Exhaustively verify the operational lower-bound premise on a finite system.

    ``embedding`` maps canonical product states to distinct actual system states.
    Decoder zero reads the inside coordinate; decoder ``j`` reads exterior
    coordinate ``j`` independently of every setting of all other coordinates.
    """

    system: FiniteControlledOutputSystem
    inside_cardinality: int
    exterior_cardinalities: tuple[int, ...]
    embedding: tuple[int, ...]
    inside_word: Word
    exterior_words: tuple[Word, ...]
    inside_decoder: TraceDecoder
    exterior_decoders: tuple[TraceDecoder, ...]

    @property
    def product_states(self) -> tuple[ProductState, ...]:
        return _product_states(self.inside_cardinality, self.exterior_cardinalities)

    @property
    def product_state_count(self) -> int:
        return len(self.product_states)

    @property
    def open_state_lower_bound(self) -> int:
        return self.product_state_count

    @property
    def open_bits_lower_bound(self) -> float:
        return log2(self.open_state_lower_bound)

    @property
    def checked_distinct_pairs(self) -> int:
        return self.product_state_count * (self.product_state_count - 1) // 2

    def embedded_system_state(self, product_state: ProductState) -> int:
        try:
            index = self.product_states.index(product_state)
        except ValueError as error:
            raise ValueError("product_state is outside the declared product subsystem") from error
        return self.embedding[index]

    def trace(self, product_state: ProductState, word: Word) -> Trace:
        return self.system.output_trace(self.embedded_system_state(product_state), word)

    def decoder_for_coordinate(self, coordinate: int) -> tuple[Word, TraceDecoder]:
        if coordinate == 0:
            return self.inside_word, self.inside_decoder
        if not 1 <= coordinate <= len(self.exterior_cardinalities):
            raise ValueError("coordinate is outside the product state")
        return self.exterior_words[coordinate - 1], self.exterior_decoders[coordinate - 1]

    def verify(self) -> bool:
        try:
            _positive_int(self.inside_cardinality, "inside_cardinality")
            cards = _normalize_cardinalities(self.exterior_cardinalities)
            if cards != self.exterior_cardinalities:
                return False
            states = self.product_states
            if len(self.embedding) != len(states) or len(set(self.embedding)) != len(self.embedding):
                return False
            for system_state in self.embedding:
                self.system.validate_state(system_state)
            if len(self.exterior_words) != len(cards) or len(self.exterior_decoders) != len(cards):
                return False
            if _normalize_word(self.system, self.inside_word, "inside_word") != self.inside_word:
                return False
            normalized_exterior_words = tuple(
                _normalize_word(self.system, word, f"exterior_words[{index}]")
                for index, word in enumerate(self.exterior_words)
            )
            if normalized_exterior_words != self.exterior_words:
                return False
            if not callable(self.inside_decoder) or any(not callable(decoder) for decoder in self.exterior_decoders):
                return False
            for state in states:
                if self.inside_decoder(self.trace(state, self.inside_word)) != state[0]:
                    return False
                for exterior_index, decoder in enumerate(self.exterior_decoders, start=1):
                    if decoder(self.trace(state, self.exterior_words[exterior_index - 1])) != state[exterior_index]:
                        return False
            for left, right in combinations(states, 2):
                coordinate = first_differing_coordinate(left, right)
                word, decoder = self.decoder_for_coordinate(coordinate)
                if decoder(self.trace(left, word)) == decoder(self.trace(right, word)):
                    return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_operational_addressable_product(
    system: FiniteControlledOutputSystem,
    inside_cardinality: int,
    exterior_cardinalities: Iterable[int],
    embedding: Iterable[int],
    inside_word: Iterable[Action],
    exterior_words: Iterable[Iterable[Action]],
    inside_decoder: TraceDecoder,
    exterior_decoders: Iterable[TraceDecoder],
) -> OperationalAddressableProductCertificate:
    """Certify one concrete finite application of the product lower bound."""
    certificate = OperationalAddressableProductCertificate(
        system=system,
        inside_cardinality=inside_cardinality,
        exterior_cardinalities=_normalize_cardinalities(exterior_cardinalities),
        embedding=tuple(embedding),
        inside_word=tuple(inside_word),
        exterior_words=tuple(tuple(word) for word in exterior_words),
        inside_decoder=inside_decoder,
        exterior_decoders=tuple(exterior_decoders),
    )
    if not certificate.verify():
        raise ValueError("declared operational decoder witness does not verify")
    return certificate


@dataclass(frozen=True)
class OperationalClosedContextFactorizationCertificate:
    """Verify declared finite closed-context trace factorizations.

    For context ``j``, words in ``closed_words[j]`` are the full declared finite
    counterfactual family and ``closed_factor_maps[j]`` is the proposed summary.
    Each map gives an upper bound on the exact closed interface for that contract.
    Standard maps ``(i,e_j)`` recover the usual noncommutation comparison.
    """

    open_certificate: OperationalAddressableProductCertificate
    closed_words: tuple[tuple[Word, ...], ...]
    closed_factor_maps: tuple[ClosedFactorMap, ...]

    @property
    def context_count(self) -> int:
        return len(self.open_certificate.exterior_cardinalities)

    @property
    def factor_label_counts(self) -> tuple[int, ...]:
        states = self.open_certificate.product_states
        return tuple(len({factor_map(state) for state in states}) for factor_map in self.closed_factor_maps)

    @property
    def closed_interface_upper_bits(self) -> tuple[float, ...]:
        return tuple(log2(count) for count in self.factor_label_counts)

    @property
    def noncommutation_gap_lower_bound(self) -> float:
        return self.open_certificate.open_bits_lower_bound - max(self.closed_interface_upper_bits)

    def verify(self) -> bool:
        try:
            if not self.open_certificate.verify():
                return False
            if len(self.closed_words) != self.context_count or len(self.closed_factor_maps) != self.context_count:
                return False
            states = self.open_certificate.product_states
            for context_index, (word_family, factor_map) in enumerate(zip(self.closed_words, self.closed_factor_maps)):
                if not callable(factor_map) or not word_family:
                    return False
                normalized_words = tuple(
                    _normalize_word(self.open_certificate.system, word, f"closed_words[{context_index}]")
                    for word in word_family
                )
                if normalized_words != word_family or len(set(word_family)) != len(word_family):
                    return False
                labels = tuple(factor_map(state) for state in states)
                try:
                    for label in labels:
                        hash(label)
                except TypeError:
                    return False
                for word in word_family:
                    traces_by_label: dict[Hashable, Trace] = {}
                    for state, label in zip(states, labels):
                        trace = self.open_certificate.trace(state, word)
                        previous = traces_by_label.get(label)
                        if previous is not None and previous != trace:
                            return False
                        traces_by_label[label] = trace
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_operational_closed_context_factorization(
    open_certificate: OperationalAddressableProductCertificate,
    closed_words: Iterable[Iterable[Iterable[Action]]],
    closed_factor_maps: Iterable[ClosedFactorMap],
) -> OperationalClosedContextFactorizationCertificate:
    """Certify declared finite closed-context trace factorizations."""
    certificate = OperationalClosedContextFactorizationCertificate(
        open_certificate=open_certificate,
        closed_words=tuple(tuple(tuple(word) for word in family) for family in closed_words),
        closed_factor_maps=tuple(closed_factor_maps),
    )
    if not certificate.verify():
        raise ValueError("declared closed-context factorization does not verify")
    return certificate


@dataclass(frozen=True)
class CanonicalOperationalProduct:
    """Literal finite readout realization used for regression and documentation."""

    inside_cardinality: int
    exterior_cardinalities: tuple[int, ...]
    system: FiniteControlledOutputSystem
    embedding: tuple[int, ...]
    inside_word: Word
    exterior_words: tuple[Word, ...]


def build_canonical_operational_product(
    inside_cardinality: int,
    exterior_cardinalities: Iterable[int],
) -> CanonicalOperationalProduct:
    """Build a controlled system whose query words read individual coordinates."""
    _positive_int(inside_cardinality, "inside_cardinality")
    cards = _normalize_cardinalities(exterior_cardinalities)
    product_states = _product_states(inside_cardinality, cards)
    actions = tuple(f"read:{coordinate}" for coordinate in range(len(cards) + 1))
    idle_count = len(product_states)
    readout_keys = tuple(
        (coordinate, value)
        for coordinate, cardinality in enumerate((inside_cardinality,) + cards)
        for value in range(cardinality)
    )
    readout_index = {key: idle_count + index for index, key in enumerate(readout_keys)}
    outputs: list[Hashable] = [("idle",)] * idle_count
    outputs.extend(("read", coordinate, value) for coordinate, value in readout_keys)
    transition_rows: list[tuple[int, ...]] = []
    for state in product_states:
        transition_rows.append(tuple(readout_index[(coordinate, state[coordinate])] for coordinate in range(len(actions))))
    for coordinate, value in readout_keys:
        current = readout_index[(coordinate, value)]
        transition_rows.append(tuple(current for _ in actions))
    return CanonicalOperationalProduct(
        inside_cardinality=inside_cardinality,
        exterior_cardinalities=cards,
        system=FiniteControlledOutputSystem(
            actions=actions,
            transition_table=tuple(transition_rows),
            outputs=tuple(outputs),
        ),
        embedding=tuple(range(idle_count)),
        inside_word=("read:0",),
        exterior_words=tuple((f"read:{coordinate}",) for coordinate in range(1, len(cards) + 1)),
    )


def readout_value(trace: Trace) -> int:
    """Decode a coordinate value from one canonical query trace."""
    if len(trace) != 2 or not isinstance(trace[-1], tuple) or len(trace[-1]) != 3 or trace[-1][0] != "read":
        raise ValueError("trace is not a canonical one-step readout")
    value = trace[-1][2]
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError("canonical readout value is not an integer")
    return value


def certify_canonical_operational_product(
    inside_cardinality: int,
    exterior_cardinalities: Iterable[int],
) -> OperationalAddressableProductCertificate:
    """Return a verified controlled-system witness for the product theorem."""
    canonical = build_canonical_operational_product(inside_cardinality, exterior_cardinalities)
    return certify_operational_addressable_product(
        system=canonical.system,
        inside_cardinality=canonical.inside_cardinality,
        exterior_cardinalities=canonical.exterior_cardinalities,
        embedding=canonical.embedding,
        inside_word=canonical.inside_word,
        exterior_words=canonical.exterior_words,
        inside_decoder=readout_value,
        exterior_decoders=(readout_value,) * len(canonical.exterior_cardinalities),
    )


__all__ = [
    "ProductState",
    "Word",
    "Trace",
    "TraceDecoder",
    "ClosedFactorMap",
    "first_differing_coordinate",
    "standard_closed_projection",
    "OperationalAddressableProductCertificate",
    "certify_operational_addressable_product",
    "OperationalClosedContextFactorizationCertificate",
    "certify_operational_closed_context_factorization",
    "CanonicalOperationalProduct",
    "build_canonical_operational_product",
    "readout_value",
    "certify_canonical_operational_product",
]
