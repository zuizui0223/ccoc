"""Information-theoretic robustness bounds for approximate addressability.

The exact addressable-codebook theorem requires every declared coordinate to be
recovered without error. This companion module asks a weaker question: how much
summary memory is still necessary if coordinate-specific future probes only need
to be decoded with bounded average error on a uniformly sampled finite codebook?

The proof is a direct Fano/information argument. It is not a claim that Fano's
inequality, rate-distortion theory, or approximate state abstraction is new.
The CCOC-specific use is only a robustness statement: the exact open-interface
inflation does not disappear immediately when a fixed decoding error is allowed.

For a uniform codeword X in C, a deterministic summary Z = phi(X), and
coordinate decoders with error probabilities eps_j,

    log2 |im(phi)|
      >= log2 |C|
         - sum_j [h2(eps_j) + eps_j log2(|A_j| - 1)],

where A_j is the set of values realized by coordinate j on C. The declared
error-tolerance version uses eps_j no larger than the random-guess error ceiling
1 - 1/|A_j| so that the Fano penalty is monotone in the permitted error.

Finite certificates below exhaustively measure the actual decoder errors on the
declared codebook. They do not infer a codebook, future probe, summary, noise
model, ecological grammar, or sampling distribution from data.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, isfinite, log2
from typing import Callable, Hashable, Iterable

Codeword = tuple[Hashable, ...]
SummaryLabel = Hashable
SummaryDecoder = Callable[[SummaryLabel], Hashable]

_NUMERIC_TOLERANCE = 1e-12


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


def _coordinate_value_counts(codebook: tuple[Codeword, ...]) -> tuple[int, ...]:
    return tuple(len({word[index] for word in codebook}) for index in range(len(codebook[0])))


def binary_entropy(error: float) -> float:
    """Return binary entropy h2(error) in bits."""
    if isinstance(error, bool):
        raise ValueError("error must be a real probability")
    try:
        probability = float(error)
    except (TypeError, ValueError) as exc:
        raise ValueError("error must be a real probability") from exc
    if not isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("error must lie in [0, 1]")
    if probability == 0.0 or probability == 1.0:
        return 0.0
    return -probability * log2(probability) - (1.0 - probability) * log2(1.0 - probability)


def fano_coordinate_penalty(error: float, alphabet_size: int) -> float:
    """Return h2(error) + error log2(alphabet_size - 1)."""
    if not isinstance(alphabet_size, int) or isinstance(alphabet_size, bool) or alphabet_size < 1:
        raise ValueError("alphabet_size must be a positive integer")
    probability = float(error)
    entropy = binary_entropy(probability)
    if alphabet_size == 1:
        return 0.0
    return entropy + probability * log2(alphabet_size - 1)


def _normalize_error_tolerances(
    error_tolerances: Iterable[float],
    coordinate_value_counts: tuple[int, ...],
) -> tuple[float, ...]:
    try:
        tolerances = tuple(float(value) for value in error_tolerances)
    except (TypeError, ValueError) as exc:
        raise ValueError("error_tolerances must be real probabilities") from exc
    if len(tolerances) != len(coordinate_value_counts):
        raise ValueError("one error tolerance is required per codebook coordinate")
    for coordinate, (error, value_count) in enumerate(zip(tolerances, coordinate_value_counts)):
        if not isfinite(error) or not 0.0 <= error <= 1.0:
            raise ValueError(f"error_tolerances[{coordinate}] must lie in [0, 1]")
        if value_count == 1:
            if error > _NUMERIC_TOLERANCE:
                raise ValueError(
                    f"error_tolerances[{coordinate}] must be zero for a constant coordinate"
                )
            continue
        monotone_ceiling = 1.0 - 1.0 / value_count
        if error > monotone_ceiling + _NUMERIC_TOLERANCE:
            raise ValueError(
                f"error_tolerances[{coordinate}] exceeds the monotone Fano ceiling "
                f"{monotone_ceiling}"
            )
    return tolerances


def fano_codebook_lower_bound(
    codebook: Iterable[Iterable[Hashable]],
    error_tolerances: Iterable[float],
) -> float:
    """Lower-bound deterministic summary memory for a uniform finite codebook."""
    normalized = _normalize_codebook(codebook)
    value_counts = _coordinate_value_counts(normalized)
    tolerances = _normalize_error_tolerances(error_tolerances, value_counts)
    penalty = sum(
        fano_coordinate_penalty(error, value_count)
        for error, value_count in zip(tolerances, value_counts)
    )
    return max(0.0, log2(len(normalized)) - penalty)


def full_binary_product_fano_lower_bound(
    exterior_count: int,
    exterior_error: float,
    *,
    inside_error: float = 0.0,
) -> float:
    """Return the Fano lower bound for one inside bit and m exterior bits."""
    if (
        not isinstance(exterior_count, int)
        or isinstance(exterior_count, bool)
        or exterior_count < 1
    ):
        raise ValueError("exterior_count must be a positive integer")
    for name, error in (("inside_error", inside_error), ("exterior_error", exterior_error)):
        if isinstance(error, bool):
            raise ValueError(f"{name} must be a real probability")
        probability = float(error)
        if not isfinite(probability) or not 0.0 <= probability <= 0.5:
            raise ValueError(f"{name} must lie in [0, 0.5] for a binary coordinate")
    return max(
        0.0,
        exterior_count
        + 1.0
        - binary_entropy(float(inside_error))
        - exterior_count * binary_entropy(float(exterior_error)),
    )


@dataclass(frozen=True)
class ApproximateAddressableCodebookCertificate:
    """Verify one deterministic approximate summary on a uniform finite codebook."""

    codebook: tuple[Codeword, ...]
    summary_labels: tuple[SummaryLabel, ...]
    coordinate_decoders: tuple[SummaryDecoder, ...]
    error_tolerances: tuple[float, ...]

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
    def coordinate_value_counts(self) -> tuple[int, ...]:
        return _coordinate_value_counts(self.codebook)

    @property
    def summary_state_count(self) -> int:
        return len(set(self.summary_labels))

    @property
    def summary_bits(self) -> float:
        return log2(self.summary_state_count)

    @property
    def empirical_coordinate_errors(self) -> tuple[float, ...]:
        errors: list[float] = []
        for coordinate, decoder in enumerate(self.coordinate_decoders):
            mistakes = 0
            for codeword, label in zip(self.codebook, self.summary_labels):
                try:
                    decoded = decoder(label)
                except Exception as exc:  # pragma: no cover - normalized by verify/certify
                    raise ValueError(f"coordinate decoder {coordinate} raised an exception") from exc
                if decoded != codeword[coordinate]:
                    mistakes += 1
            errors.append(mistakes / self.codeword_count)
        return tuple(errors)

    @property
    def empirical_fano_penalty_bits(self) -> float:
        return sum(
            fano_coordinate_penalty(error, value_count)
            for error, value_count in zip(
                self.empirical_coordinate_errors,
                self.coordinate_value_counts,
            )
        )

    @property
    def contract_fano_penalty_bits(self) -> float:
        return sum(
            fano_coordinate_penalty(error, value_count)
            for error, value_count in zip(
                self.error_tolerances,
                self.coordinate_value_counts,
            )
        )

    @property
    def empirical_open_bits_lower_bound(self) -> float:
        return max(0.0, log2(self.codeword_count) - self.empirical_fano_penalty_bits)

    @property
    def contract_open_bits_lower_bound(self) -> float:
        return max(0.0, log2(self.codeword_count) - self.contract_fano_penalty_bits)

    @property
    def minimum_summary_state_count_from_contract(self) -> int:
        return max(1, ceil(2.0 ** self.contract_open_bits_lower_bound - _NUMERIC_TOLERANCE))

    @property
    def information_slack_bits(self) -> float:
        return self.summary_bits - self.empirical_open_bits_lower_bound

    def verify(self) -> bool:
        try:
            normalized = _normalize_codebook(self.codebook)
            if normalized != self.codebook:
                return False
            if len(self.summary_labels) != self.codeword_count:
                return False
            try:
                for label in self.summary_labels:
                    hash(label)
            except TypeError:
                return False
            if len(self.coordinate_decoders) != self.coordinate_count:
                return False
            if any(not callable(decoder) for decoder in self.coordinate_decoders):
                return False
            tolerances = _normalize_error_tolerances(
                self.error_tolerances,
                self.coordinate_value_counts,
            )
            if tolerances != self.error_tolerances:
                return False
            empirical_errors = self.empirical_coordinate_errors
            if any(
                actual > allowed + _NUMERIC_TOLERANCE
                for actual, allowed in zip(empirical_errors, self.error_tolerances)
            ):
                return False
            if self.summary_bits + _NUMERIC_TOLERANCE < self.empirical_open_bits_lower_bound:
                return False
            if (
                self.empirical_open_bits_lower_bound + _NUMERIC_TOLERANCE
                < self.contract_open_bits_lower_bound
            ):
                return False
            return True
        except (TypeError, ValueError, ZeroDivisionError):
            return False


def certify_approximate_addressable_codebook(
    codebook: Iterable[Iterable[Hashable]],
    summary_labels: Iterable[SummaryLabel],
    coordinate_decoders: Iterable[SummaryDecoder],
    error_tolerances: Iterable[float],
) -> ApproximateAddressableCodebookCertificate:
    """Certify a finite approximate codebook summary and its Fano lower bound."""
    normalized_codebook = _normalize_codebook(codebook)
    value_counts = _coordinate_value_counts(normalized_codebook)
    certificate = ApproximateAddressableCodebookCertificate(
        codebook=normalized_codebook,
        summary_labels=tuple(summary_labels),
        coordinate_decoders=tuple(coordinate_decoders),
        error_tolerances=_normalize_error_tolerances(error_tolerances, value_counts),
    )
    if not certificate.verify():
        raise ValueError("declared approximate addressability witness does not verify")
    return certificate


__all__ = [
    "Codeword",
    "SummaryLabel",
    "SummaryDecoder",
    "binary_entropy",
    "fano_coordinate_penalty",
    "fano_codebook_lower_bound",
    "full_binary_product_fano_lower_bound",
    "ApproximateAddressableCodebookCertificate",
    "certify_approximate_addressable_codebook",
]
