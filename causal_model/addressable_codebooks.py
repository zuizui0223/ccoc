"""Operational codebook witnesses for open-composition lower bounds.

This module strengthens the v1 addressable-product theorem by replacing the full
Cartesian product premise with an arbitrary finite jointly realizable codebook.
The analytic content is simple but important: if every coordinate of every
codeword can be recovered by a declared legal future word, then distinct
codewords are pairwise future-distinguishable and every exact open interface must
retain at least ``log2(len(codebook))`` bits.

Closed-context factorization is compared against the actual number of factor
labels realized on the same codebook. The v1 product theorem is recovered when
the codebook is the full Cartesian product and the closed factor maps are the
standard ``(inside, exterior_j)`` projections.

Finite certificates in this module replay a declared witness. They do not infer
a codebook, grammar, decoder, reachability claim, or ecological interpretation
from data.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import log2
from typing import Callable, Hashable, Iterable

from .dynamic_boundary_blankets import Action, FiniteControlledOutputSystem

Codeword = tuple[Hashable, ...]
Word = tuple[Action, ...]
Trace = tuple[Hashable, ...]
TraceDecoder = Callable[[Trace], Hashable]
ClosedFactorMap = Callable[[Codeword], Hashable]


def _normalize_codebook(codebook: Iterable[Iterable[Hashable]]) -> tuple[Codeword, ...]:
    try:
        normalized = tuple(tuple(word) for word in codebook)
    except TypeError as error:
        raise ValueError("codebook must be an iterable of iterable codewords") from error
    if not normalized:
        raise ValueError("codebook must contain at least one codeword")
    coordinate_count = len(normalized[0])
    if coordinate_count < 2:
        raise ValueError("codewords must contain one inside and at least one exterior coordinate")
    for index, word in enumerate(normalized):
        if len(word) != coordinate_count:
            raise ValueError("all codewords must have the same coordinate count")
        try:
            hash(word)
            for value in word:
                hash(value)
        except TypeError as error:
            raise ValueError(f"codeword {index} contains a non-hashable coordinate") from error
    if len(set(normalized)) != len(normalized):
        raise ValueError("codebook must not contain duplicate codewords")
    return normalized


def _normalize_word(system: FiniteControlledOutputSystem, word: Iterable[Action], name: str) -> Word:
    try:
        normalized = tuple(word)
    except TypeError as error:
        raise ValueError(f"{name} must be an iterable of actions") from error
    try:
        return system.normalize_word(normalized)
    except ValueError as error:
        raise ValueError(f"{name} is not legal for the declared controlled system") from error


def first_differing_codebook_coordinate(left: Codeword, right: Codeword) -> int:
    """Return the first coordinate at which two unequal codewords differ."""
    if len(left) != len(right):
        raise ValueError("codewords must have equal length")
    if left == right:
        raise ValueError("distinct codewords are required")
    for coordinate, (left_value, right_value) in enumerate(zip(left, right)):
        if left_value != right_value:
            return coordinate
    raise AssertionError("distinct equal-length tuples must differ")


def standard_codebook_closed_projection(module_index: int) -> ClosedFactorMap:
    """Return ``(inside, exterior_j)`` on an arbitrary codebook."""
    if not isinstance(module_index, int) or isinstance(module_index, bool) or module_index < 0:
        raise ValueError("module_index must be a non-negative integer")

    def projection(codeword: Codeword) -> tuple[Hashable, Hashable]:
        coordinate = module_index + 1
        if coordinate >= len(codeword):
            raise ValueError("codeword does not contain the requested exterior module")
        return (codeword[0], codeword[coordinate])

    return projection


@dataclass(frozen=True)
class OperationalAddressableCodebookCertificate:
    """Exhaustively verify coordinate addressability on a finite codebook."""

    system: FiniteControlledOutputSystem
    codebook: tuple[Codeword, ...]
    embedding: tuple[int, ...]
    coordinate_words: tuple[Word, ...]
    coordinate_decoders: tuple[TraceDecoder, ...]

    @property
    def coordinate_count(self) -> int:
        return len(self.codebook[0])

    @property
    def exterior_count(self) -> int:
        return self.coordinate_count - 1

    @property
    def codeword_count(self) -> int:
        return len(self.codebook)

    @property
    def open_state_lower_bound(self) -> int:
        return self.codeword_count

    @property
    def open_bits_lower_bound(self) -> float:
        return log2(self.open_state_lower_bound)

    @property
    def checked_distinct_pairs(self) -> int:
        return self.codeword_count * (self.codeword_count - 1) // 2

    @property
    def coordinate_value_counts(self) -> tuple[int, ...]:
        return tuple(len({codeword[index] for codeword in self.codebook}) for index in range(self.coordinate_count))

    @property
    def ambient_cartesian_count(self) -> int:
        count = 1
        for cardinality in self.coordinate_value_counts:
            count *= cardinality
        return count

    @property
    def is_full_cartesian_codebook(self) -> bool:
        return self.codeword_count == self.ambient_cartesian_count

    def embedded_system_state(self, codeword: Codeword) -> int:
        try:
            index = self.codebook.index(codeword)
        except ValueError as error:
            raise ValueError("codeword is outside the declared addressable codebook") from error
        return self.embedding[index]

    def trace(self, codeword: Codeword, word: Word) -> Trace:
        return self.system.output_trace(self.embedded_system_state(codeword), word)

    def decoder_for_coordinate(self, coordinate: int) -> tuple[Word, TraceDecoder]:
        if not isinstance(coordinate, int) or isinstance(coordinate, bool):
            raise ValueError("coordinate must be an integer")
        if not 0 <= coordinate < self.coordinate_count:
            raise ValueError("coordinate is outside the codeword")
        return self.coordinate_words[coordinate], self.coordinate_decoders[coordinate]

    def verify(self) -> bool:
        try:
            normalized_codebook = _normalize_codebook(self.codebook)
            if normalized_codebook != self.codebook:
                return False
            if len(self.embedding) != self.codeword_count or len(set(self.embedding)) != len(self.embedding):
                return False
            for system_state in self.embedding:
                self.system.validate_state(system_state)
            if len(self.coordinate_words) != self.coordinate_count:
                return False
            if len(self.coordinate_decoders) != self.coordinate_count:
                return False
            normalized_words = tuple(
                _normalize_word(self.system, word, f"coordinate_words[{index}]")
                for index, word in enumerate(self.coordinate_words)
            )
            if normalized_words != self.coordinate_words:
                return False
            if any(not callable(decoder) for decoder in self.coordinate_decoders):
                return False

            for codeword in self.codebook:
                for coordinate, decoder in enumerate(self.coordinate_decoders):
                    word = self.coordinate_words[coordinate]
                    if decoder(self.trace(codeword, word)) != codeword[coordinate]:
                        return False

            for left, right in combinations(self.codebook, 2):
                coordinate = first_differing_codebook_coordinate(left, right)
                word, decoder = self.decoder_for_coordinate(coordinate)
                if decoder(self.trace(left, word)) == decoder(self.trace(right, word)):
                    return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_operational_addressable_codebook(
    system: FiniteControlledOutputSystem,
    codebook: Iterable[Iterable[Hashable]],
    embedding: Iterable[int],
    coordinate_words: Iterable[Iterable[Action]],
    coordinate_decoders: Iterable[TraceDecoder],
) -> OperationalAddressableCodebookCertificate:
    """Certify one finite application of the addressable-codebook lower bound."""
    certificate = OperationalAddressableCodebookCertificate(
        system=system,
        codebook=_normalize_codebook(codebook),
        embedding=tuple(embedding),
        coordinate_words=tuple(tuple(word) for word in coordinate_words),
        coordinate_decoders=tuple(coordinate_decoders),
    )
    if not certificate.verify():
        raise ValueError("declared operational codebook witness does not verify")
    return certificate


@dataclass(frozen=True)
class OperationalCodebookClosedContextCertificate:
    """Verify closed response factorizations on one addressable codebook."""

    open_certificate: OperationalAddressableCodebookCertificate
    closed_words: tuple[tuple[Word, ...], ...]
    closed_factor_maps: tuple[ClosedFactorMap, ...]

    @property
    def context_count(self) -> int:
        return self.open_certificate.exterior_count

    @property
    def factor_label_counts(self) -> tuple[int, ...]:
        return tuple(
            len({factor_map(codeword) for codeword in self.open_certificate.codebook})
            for factor_map in self.closed_factor_maps
        )

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
            if len(self.closed_words) != self.context_count:
                return False
            if len(self.closed_factor_maps) != self.context_count:
                return False

            for context_index, (word_family, factor_map) in enumerate(zip(self.closed_words, self.closed_factor_maps)):
                if not callable(factor_map) or not word_family:
                    return False
                normalized_words = tuple(
                    _normalize_word(self.open_certificate.system, word, f"closed_words[{context_index}]")
                    for word in word_family
                )
                if normalized_words != word_family or len(set(word_family)) != len(word_family):
                    return False

                labels = tuple(factor_map(codeword) for codeword in self.open_certificate.codebook)
                try:
                    for label in labels:
                        hash(label)
                except TypeError:
                    return False

                for word in word_family:
                    traces_by_label: dict[Hashable, Trace] = {}
                    for codeword, label in zip(self.open_certificate.codebook, labels):
                        trace = self.open_certificate.trace(codeword, word)
                        previous = traces_by_label.get(label)
                        if previous is not None and previous != trace:
                            return False
                        traces_by_label[label] = trace
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_operational_codebook_closed_context_factorization(
    open_certificate: OperationalAddressableCodebookCertificate,
    closed_words: Iterable[Iterable[Iterable[Action]]],
    closed_factor_maps: Iterable[ClosedFactorMap],
) -> OperationalCodebookClosedContextCertificate:
    """Certify finite closed-context upper bounds on an addressable codebook."""
    certificate = OperationalCodebookClosedContextCertificate(
        open_certificate=open_certificate,
        closed_words=tuple(tuple(tuple(word) for word in family) for family in closed_words),
        closed_factor_maps=tuple(closed_factor_maps),
    )
    if not certificate.verify():
        raise ValueError("declared codebook closed-context factorization does not verify")
    return certificate


@dataclass(frozen=True)
class CanonicalOperationalCodebook:
    """Literal controlled readout realization of an arbitrary finite codebook."""

    codebook: tuple[Codeword, ...]
    system: FiniteControlledOutputSystem
    embedding: tuple[int, ...]
    coordinate_words: tuple[Word, ...]


def build_canonical_operational_codebook(
    codebook: Iterable[Iterable[Hashable]],
) -> CanonicalOperationalCodebook:
    """Build a controlled system whose query words read codebook coordinates."""
    normalized = _normalize_codebook(codebook)
    coordinate_count = len(normalized[0])
    actions = tuple(f"read:{coordinate}" for coordinate in range(coordinate_count))
    idle_count = len(normalized)

    readout_keys: list[tuple[int, Hashable]] = []
    for coordinate in range(coordinate_count):
        seen: set[Hashable] = set()
        for codeword in normalized:
            value = codeword[coordinate]
            if value not in seen:
                seen.add(value)
                readout_keys.append((coordinate, value))

    readout_index = {key: idle_count + index for index, key in enumerate(readout_keys)}
    outputs: list[Hashable] = [("idle",)] * idle_count
    outputs.extend(("read", coordinate, value) for coordinate, value in readout_keys)

    transition_rows: list[tuple[int, ...]] = []
    for codeword in normalized:
        transition_rows.append(
            tuple(readout_index[(coordinate, codeword[coordinate])] for coordinate in range(coordinate_count))
        )
    for coordinate, value in readout_keys:
        current = readout_index[(coordinate, value)]
        transition_rows.append(tuple(current for _ in actions))

    return CanonicalOperationalCodebook(
        codebook=normalized,
        system=FiniteControlledOutputSystem(
            actions=actions,
            transition_table=tuple(transition_rows),
            outputs=tuple(outputs),
        ),
        embedding=tuple(range(idle_count)),
        coordinate_words=tuple((action,) for action in actions),
    )


def readout_symbol(trace: Trace) -> Hashable:
    """Decode the symbol from one canonical one-step coordinate readout."""
    if len(trace) != 2:
        raise ValueError("trace is not a canonical one-step readout")
    output = trace[-1]
    if not isinstance(output, tuple) or len(output) != 3 or output[0] != "read":
        raise ValueError("trace is not a canonical one-step readout")
    return output[2]


def certify_canonical_operational_codebook(
    codebook: Iterable[Iterable[Hashable]],
) -> OperationalAddressableCodebookCertificate:
    """Return a verified canonical controlled-system codebook witness."""
    canonical = build_canonical_operational_codebook(codebook)
    return certify_operational_addressable_codebook(
        system=canonical.system,
        codebook=canonical.codebook,
        embedding=canonical.embedding,
        coordinate_words=canonical.coordinate_words,
        coordinate_decoders=(readout_symbol,) * len(canonical.coordinate_words),
    )


def even_parity_codebook(exterior_count: int) -> tuple[Codeword, ...]:
    """Return the binary even-parity code on one inside plus exterior coordinates."""
    if not isinstance(exterior_count, int) or isinstance(exterior_count, bool) or exterior_count < 1:
        raise ValueError("exterior_count must be a positive integer")
    coordinate_count = exterior_count + 1
    return tuple(bits for bits in product((0, 1), repeat=coordinate_count) if sum(bits) % 2 == 0)


__all__ = [
    "Codeword",
    "Word",
    "Trace",
    "TraceDecoder",
    "ClosedFactorMap",
    "first_differing_codebook_coordinate",
    "standard_codebook_closed_projection",
    "OperationalAddressableCodebookCertificate",
    "certify_operational_addressable_codebook",
    "OperationalCodebookClosedContextCertificate",
    "certify_operational_codebook_closed_context_factorization",
    "CanonicalOperationalCodebook",
    "build_canonical_operational_codebook",
    "readout_symbol",
    "certify_canonical_operational_codebook",
    "even_parity_codebook",
]
