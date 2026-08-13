"""Information tradeoff between closed retention and reopening adaptation.

Let E=(E_1,...,E_m) be a uniformly distributed binary exterior state.  A closed
representation C may retain some information about E before composition opens.
After opening, an update message U may be added.  If every exterior coordinate is
decodable from (C,U) with error eps_j, then

    I(E;C) + H(U|C) >= m - sum_j h2(eps_j).

For a common error tolerance eps<=1/2 this becomes

    I(E;C) + H(U|C) >= m * (1 - h2(eps)).

The proof is Fano plus the chain rule.  Neither ingredient is a novelty claim.
The CCOC role is a portability resource allocation: exterior information discarded
by a closed compression must either have been retained already or be supplied by
a reopening update if the expanded grammar later makes those coordinates
approximately addressable.

The finite certificate below treats deterministic C and U on the full uniform
binary exterior product.  In that case I(E;C)=H(C), and it computes H(U|C)
exactly from finite frequencies.  The exact-error frontier is sharp: retaining k
prefix bits and updating the remaining m-k bits attains equality for every k.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product
from math import ceil, isfinite, log2
from typing import Callable, Hashable, Iterable

from .approximate_addressability import binary_entropy

ExteriorState = tuple[int, ...]
RepresentationLabel = Hashable
AdaptationDecoder = Callable[[tuple[RepresentationLabel, RepresentationLabel]], int]

_NUMERIC_TOLERANCE = 1e-12


def full_binary_exterior_states(exterior_count: int) -> tuple[ExteriorState, ...]:
    if (
        not isinstance(exterior_count, int)
        or isinstance(exterior_count, bool)
        or exterior_count < 1
    ):
        raise ValueError("exterior_count must be a positive integer")
    return tuple(product((0, 1), repeat=exterior_count))


def _normalize_full_binary_states(
    states: Iterable[Iterable[int]],
) -> tuple[ExteriorState, ...]:
    try:
        normalized = tuple(tuple(state) for state in states)
    except TypeError as error:
        raise ValueError("exterior_states must be iterable") from error
    if not normalized:
        raise ValueError("exterior_states must be nonempty")
    exterior_count = len(normalized[0])
    if exterior_count < 1:
        raise ValueError("each exterior state must contain at least one bit")
    if any(len(state) != exterior_count for state in normalized):
        raise ValueError("all exterior states must have the same length")
    if any(bit not in (0, 1) for state in normalized for bit in state):
        raise ValueError("exterior states must be binary")
    expected = set(full_binary_exterior_states(exterior_count))
    if len(normalized) != len(expected) or set(normalized) != expected:
        raise ValueError("exterior_states must contain the complete binary product exactly once")
    return normalized


def _entropy_bits(labels: tuple[Hashable, ...]) -> float:
    if not labels:
        raise ValueError("entropy labels must be nonempty")
    counts = Counter(labels)
    total = len(labels)
    entropy = 0.0
    for count in counts.values():
        probability = count / total
        entropy -= probability * log2(probability)
    return entropy


def _normalize_tolerances(
    tolerances: Iterable[float],
    coordinate_count: int,
) -> tuple[float, ...]:
    try:
        normalized = tuple(float(value) for value in tolerances)
    except (TypeError, ValueError) as error:
        raise ValueError("error_tolerances must be real probabilities") from error
    if len(normalized) != coordinate_count:
        raise ValueError("one error tolerance is required per exterior coordinate")
    for index, error in enumerate(normalized):
        if not isfinite(error) or not 0.0 <= error <= 0.5:
            raise ValueError(
                f"error_tolerances[{index}] must lie in [0, 0.5] for a binary coordinate"
            )
    return normalized


def binary_portability_information_lower_bound(
    error_tolerances: Iterable[float],
) -> float:
    """Return m - sum h2(eps_j) for independent uniform binary coordinates."""
    tolerances = tuple(float(value) for value in error_tolerances)
    if not tolerances:
        raise ValueError("at least one error tolerance is required")
    normalized = _normalize_tolerances(tolerances, len(tolerances))
    return max(0.0, len(normalized) - sum(binary_entropy(error) for error in normalized))


@dataclass(frozen=True)
class PortabilityAdaptationTradeoffCertificate:
    """Finite deterministic retention/update certificate on a uniform binary product."""

    exterior_states: tuple[ExteriorState, ...]
    closed_labels: tuple[RepresentationLabel, ...]
    update_labels: tuple[RepresentationLabel, ...]
    coordinate_decoders: tuple[AdaptationDecoder, ...]
    error_tolerances: tuple[float, ...]

    @property
    def exterior_count(self) -> int:
        return len(self.exterior_states[0])

    @property
    def state_count(self) -> int:
        return len(self.exterior_states)

    @property
    def closed_state_count(self) -> int:
        return len(set(self.closed_labels))

    @property
    def update_state_count(self) -> int:
        return len(set(self.update_labels))

    @property
    def joint_state_count(self) -> int:
        return len(set(zip(self.closed_labels, self.update_labels)))

    @property
    def retained_exterior_information_bits(self) -> float:
        # C is a deterministic function of uniform E, so I(E;C)=H(C).
        return _entropy_bits(self.closed_labels)

    @property
    def joint_exterior_information_bits(self) -> float:
        # (C,U) is deterministic, so I(E;C,U)=H(C,U).
        return _entropy_bits(tuple(zip(self.closed_labels, self.update_labels)))

    @property
    def update_conditional_entropy_bits(self) -> float:
        return self.joint_exterior_information_bits - self.retained_exterior_information_bits

    @property
    def closed_state_capacity_bits(self) -> float:
        return log2(self.closed_state_count)

    @property
    def update_state_capacity_bits(self) -> float:
        return log2(self.update_state_count)

    @property
    def empirical_coordinate_errors(self) -> tuple[float, ...]:
        errors: list[float] = []
        for coordinate, decoder in enumerate(self.coordinate_decoders):
            mistakes = 0
            for state, closed_label, update_label in zip(
                self.exterior_states,
                self.closed_labels,
                self.update_labels,
            ):
                try:
                    decoded = decoder((closed_label, update_label))
                except Exception as error:  # pragma: no cover - normalized by verify
                    raise ValueError(
                        f"coordinate decoder {coordinate} raised an exception"
                    ) from error
                if decoded not in (0, 1):
                    raise ValueError("coordinate decoders must return binary values")
                if decoded != state[coordinate]:
                    mistakes += 1
            errors.append(mistakes / self.state_count)
        return tuple(errors)

    @property
    def empirical_required_information_bits(self) -> float:
        return binary_portability_information_lower_bound(self.empirical_coordinate_errors)

    @property
    def contract_required_information_bits(self) -> float:
        return binary_portability_information_lower_bound(self.error_tolerances)

    @property
    def minimum_update_entropy_from_contract_bits(self) -> float:
        return max(
            0.0,
            self.contract_required_information_bits
            - self.retained_exterior_information_bits,
        )

    @property
    def minimum_update_state_count_from_contract(self) -> int:
        return max(
            1,
            ceil(
                2.0 ** self.minimum_update_entropy_from_contract_bits
                - _NUMERIC_TOLERANCE
            ),
        )

    @property
    def empirical_tradeoff_slack_bits(self) -> float:
        return (
            self.retained_exterior_information_bits
            + self.update_conditional_entropy_bits
            - self.empirical_required_information_bits
        )

    def verify(self) -> bool:
        try:
            normalized_states = _normalize_full_binary_states(self.exterior_states)
            if normalized_states != self.exterior_states:
                return False
            if len(self.closed_labels) != self.state_count:
                return False
            if len(self.update_labels) != self.state_count:
                return False
            try:
                for label in self.closed_labels + self.update_labels:
                    hash(label)
            except TypeError:
                return False
            if len(self.coordinate_decoders) != self.exterior_count:
                return False
            if any(not callable(decoder) for decoder in self.coordinate_decoders):
                return False
            tolerances = _normalize_tolerances(
                self.error_tolerances,
                self.exterior_count,
            )
            if tolerances != self.error_tolerances:
                return False

            actual_errors = self.empirical_coordinate_errors
            if any(
                actual > allowed + _NUMERIC_TOLERANCE
                for actual, allowed in zip(actual_errors, self.error_tolerances)
            ):
                return False

            if (
                self.retained_exterior_information_bits
                > self.closed_state_capacity_bits + _NUMERIC_TOLERANCE
            ):
                return False
            if (
                self.update_conditional_entropy_bits
                > self.update_state_capacity_bits + _NUMERIC_TOLERANCE
            ):
                return False
            if (
                self.retained_exterior_information_bits
                + self.update_conditional_entropy_bits
                + _NUMERIC_TOLERANCE
                < self.empirical_required_information_bits
            ):
                return False
            if (
                self.empirical_required_information_bits + _NUMERIC_TOLERANCE
                < self.contract_required_information_bits
            ):
                return False
            return True
        except (TypeError, ValueError, ZeroDivisionError):
            return False


def certify_portability_adaptation_tradeoff(
    exterior_states: Iterable[Iterable[int]],
    closed_labels: Iterable[RepresentationLabel],
    update_labels: Iterable[RepresentationLabel],
    coordinate_decoders: Iterable[AdaptationDecoder],
    error_tolerances: Iterable[float],
) -> PortabilityAdaptationTradeoffCertificate:
    normalized_states = _normalize_full_binary_states(exterior_states)
    certificate = PortabilityAdaptationTradeoffCertificate(
        exterior_states=normalized_states,
        closed_labels=tuple(closed_labels),
        update_labels=tuple(update_labels),
        coordinate_decoders=tuple(coordinate_decoders),
        error_tolerances=_normalize_tolerances(
            error_tolerances,
            len(normalized_states[0]),
        ),
    )
    if not certificate.verify():
        raise ValueError("retention/update adaptation witness does not verify")
    return certificate


def exact_retention_update_frontier(
    exterior_count: int,
    retained_bits: int,
) -> PortabilityAdaptationTradeoffCertificate:
    """Sharp exact witness: retain k prefix bits, update the remaining m-k bits."""
    states = full_binary_exterior_states(exterior_count)
    if (
        not isinstance(retained_bits, int)
        or isinstance(retained_bits, bool)
        or not 0 <= retained_bits <= exterior_count
    ):
        raise ValueError("retained_bits must lie in [0, exterior_count]")

    closed_labels = tuple(state[:retained_bits] for state in states)
    update_labels = tuple(state[retained_bits:] for state in states)

    decoders: list[AdaptationDecoder] = []
    for coordinate in range(exterior_count):
        if coordinate < retained_bits:
            decoders.append(
                lambda pair, coordinate=coordinate: pair[0][coordinate]
            )
        else:
            update_coordinate = coordinate - retained_bits
            decoders.append(
                lambda pair, update_coordinate=update_coordinate: pair[1][update_coordinate]
            )

    certificate = certify_portability_adaptation_tradeoff(
        states,
        closed_labels,
        update_labels,
        tuple(decoders),
        (0.0,) * exterior_count,
    )
    if abs(certificate.retained_exterior_information_bits - retained_bits) > _NUMERIC_TOLERANCE:
        raise AssertionError("exact frontier retained information did not match k")
    if abs(
        certificate.update_conditional_entropy_bits - (exterior_count - retained_bits)
    ) > _NUMERIC_TOLERANCE:
        raise AssertionError("exact frontier update information did not match m-k")
    if abs(certificate.empirical_tradeoff_slack_bits) > _NUMERIC_TOLERANCE:
        raise AssertionError("exact frontier did not saturate the tradeoff")
    return certificate


__all__ = [
    "ExteriorState",
    "RepresentationLabel",
    "AdaptationDecoder",
    "full_binary_exterior_states",
    "binary_portability_information_lower_bound",
    "PortabilityAdaptationTradeoffCertificate",
    "certify_portability_adaptation_tradeoff",
    "exact_retention_update_frontier",
]
