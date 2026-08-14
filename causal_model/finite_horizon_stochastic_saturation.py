"""Finite-horizon approximate saturation blankets for stochastic depletion.

Exact stochastic response equivalence can require all M+1 abundance states as soon
as a downward mechanism has positive rate.  Over a fixed finite horizon, however,
a capacity-independent L+1-state macro can remain accurate: keep the unsaturated
states 0,...,L-1 exactly and approximate every saturated state by a macrostate that
stays saturated throughout the window.

For a constant total one-unit depletion clock of rate mu, the worst saturated
state is N=L and the path leaves saturation by time T with probability
1-exp(-mu*T).  For independent per-capita mortality, the worst saturated state is
again N=L and the path leaves saturation with probability 1-exp(-mu*L*T).
These are exact path-TV errors against the constant saturated macro path for the
worst saturated initial state and are independent of carrying capacity M.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, inf, isfinite, log
from typing import Iterable, Literal

Mechanism = Literal["constant_rate", "per_capita"]


def _normalize_mechanism(value: str) -> Mechanism:
    if value not in ("constant_rate", "per_capita"):
        raise ValueError("mechanism must be 'constant_rate' or 'per_capita'")
    return value  # type: ignore[return-value]


def _nonnegative_rate(value: float) -> float:
    if isinstance(value, bool):
        raise ValueError("rate must be a non-negative real number")
    rate = float(value)
    if not isfinite(rate) or rate < 0:
        raise ValueError("rate must be non-negative and finite")
    return rate


def _positive_horizon(value: float) -> float:
    if isinstance(value, bool):
        raise ValueError("horizon must be positive")
    horizon = float(value)
    if not isfinite(horizon) or horizon <= 0:
        raise ValueError("horizon must be positive and finite")
    return horizon


def finite_horizon_saturation_error(
    saturation_level: int,
    rate: float,
    horizon: float,
    mechanism: Mechanism,
) -> float:
    if not isinstance(saturation_level, int) or isinstance(saturation_level, bool) or saturation_level < 1:
        raise ValueError("saturation_level must be a positive integer")
    mu = _nonnegative_rate(rate)
    t = _positive_horizon(horizon)
    normalized = _normalize_mechanism(mechanism)
    exposure = mu * t if normalized == "constant_rate" else mu * saturation_level * t
    return 1.0 - exp(-exposure)


@dataclass(frozen=True)
class FiniteHorizonSaturationApproximationCertificate:
    """One capacity domain with an L+1-state finite-horizon approximate macro."""

    capacity: int
    saturation_level: int
    rate: float
    horizon: float
    mechanism: Mechanism

    @property
    def approximate_macro_state_count(self) -> int:
        return self.saturation_level + 1

    @property
    def exact_response_state_count(self) -> int:
        return self.approximate_macro_state_count if self.rate == 0 else self.capacity + 1

    @property
    def saturated_path_tv_error(self) -> float:
        return finite_horizon_saturation_error(
            self.saturation_level,
            self.rate,
            self.horizon,
            self.mechanism,
        )

    @property
    def compression_ratio(self) -> float:
        return self.exact_response_state_count / self.approximate_macro_state_count

    def meets_tolerance(self, tolerance: float) -> bool:
        if isinstance(tolerance, bool):
            raise ValueError("tolerance must be a probability")
        error = float(tolerance)
        if not isfinite(error) or not 0.0 <= error < 1.0:
            raise ValueError("tolerance must lie in [0,1)")
        return self.saturated_path_tv_error <= error + 1e-12

    def maximum_horizon_for_tolerance(self, tolerance: float) -> float:
        if isinstance(tolerance, bool):
            raise ValueError("tolerance must be a probability")
        error = float(tolerance)
        if not isfinite(error) or not 0.0 <= error < 1.0:
            raise ValueError("tolerance must lie in [0,1)")
        if self.rate == 0:
            return inf
        multiplier = 1 if self.mechanism == "constant_rate" else self.saturation_level
        return -log(1.0 - error) / (self.rate * multiplier)

    def verify(self) -> bool:
        try:
            if not isinstance(self.capacity, int) or isinstance(self.capacity, bool):
                return False
            if not isinstance(self.saturation_level, int) or isinstance(self.saturation_level, bool):
                return False
            if self.saturation_level < 1 or self.capacity < self.saturation_level:
                return False
            if _nonnegative_rate(self.rate) != self.rate:
                return False
            if _positive_horizon(self.horizon) != self.horizon:
                return False
            if _normalize_mechanism(self.mechanism) != self.mechanism:
                return False
            error = self.saturated_path_tv_error
            if not 0.0 <= error < 1.0:
                return False
            if self.rate == 0:
                if error != 0.0 or self.exact_response_state_count != self.approximate_macro_state_count:
                    return False
            elif self.exact_response_state_count != self.capacity + 1:
                return False
            if self.approximate_macro_state_count != self.saturation_level + 1:
                return False
            if abs(
                finite_horizon_saturation_error(
                    self.saturation_level, self.rate, self.horizon, self.mechanism
                )
                - error
            ) > 1e-12:
                return False
            return True
        except (OverflowError, TypeError, ValueError, ZeroDivisionError):
            return False


def certify_finite_horizon_saturation_approximation(
    capacity: int,
    saturation_level: int,
    rate: float,
    horizon: float,
    mechanism: Mechanism,
) -> FiniteHorizonSaturationApproximationCertificate:
    certificate = FiniteHorizonSaturationApproximationCertificate(
        capacity=capacity,
        saturation_level=saturation_level,
        rate=_nonnegative_rate(rate),
        horizon=_positive_horizon(horizon),
        mechanism=_normalize_mechanism(mechanism),
    )
    if not certificate.verify():
        raise ValueError("finite-horizon saturation approximation did not verify")
    return certificate


@dataclass(frozen=True)
class FiniteHorizonSaturationFamilyCertificate:
    """One approximate saturation macro/error contract across changing capacities."""

    stages: tuple[FiniteHorizonSaturationApproximationCertificate, ...]

    @property
    def approximate_macro_state_count(self) -> int:
        return self.stages[0].approximate_macro_state_count

    @property
    def saturated_path_tv_error(self) -> float:
        return self.stages[0].saturated_path_tv_error

    @property
    def capacities(self) -> tuple[int, ...]:
        return tuple(stage.capacity for stage in self.stages)

    def verify(self) -> bool:
        try:
            if not self.stages or any(not stage.verify() for stage in self.stages):
                return False
            first = self.stages[0]
            for stage in self.stages[1:]:
                if stage.saturation_level != first.saturation_level:
                    return False
                if stage.rate != first.rate or stage.horizon != first.horizon:
                    return False
                if stage.mechanism != first.mechanism:
                    return False
                if stage.approximate_macro_state_count != first.approximate_macro_state_count:
                    return False
                if abs(stage.saturated_path_tv_error - first.saturated_path_tv_error) > 1e-12:
                    return False
            return True
        except (TypeError, ValueError):
            return False


def certify_finite_horizon_saturation_family(
    capacities: Iterable[int],
    saturation_level: int,
    rate: float,
    horizon: float,
    mechanism: Mechanism,
) -> FiniteHorizonSaturationFamilyCertificate:
    capacity_tuple = tuple(capacities)
    if not capacity_tuple:
        raise ValueError("at least one capacity is required")
    stages = tuple(
        certify_finite_horizon_saturation_approximation(
            capacity,
            saturation_level,
            rate,
            horizon,
            mechanism,
        )
        for capacity in capacity_tuple
    )
    certificate = FiniteHorizonSaturationFamilyCertificate(stages)
    if not certificate.verify():
        raise AssertionError("finite-horizon capacity family did not share one approximate contract")
    return certificate


__all__ = [
    "Mechanism",
    "FiniteHorizonSaturationApproximationCertificate",
    "FiniteHorizonSaturationFamilyCertificate",
    "finite_horizon_saturation_error",
    "certify_finite_horizon_saturation_approximation",
    "certify_finite_horizon_saturation_family",
]
