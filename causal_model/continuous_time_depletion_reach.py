"""Continuous-time depletion reach for saturated ecological responses.

A one-guild abundance N has capped response Y=min(L,N).  Under a pure one-unit
depletion clock of rate mu, the number of depletion opportunities up to time t is
Poisson(mu*t) until absorption at zero.  For two saturated initial abundances
L<=n1<n2, the event Y_t<L requires at least n-L+1 depletions.  Therefore the gap
between the two event probabilities is a strictly positive finite Poisson mass for
every mu>0 and t>0.

This gives a continuous-time counterpart of stochastic depletion exposure: every
positive depletion rate restores full exact abundance distinguishability, while
finite-horizon approximate separation is controlled by the dimensionless product
mu*t.  The Poisson-process calculation is classical substrate.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import e, exp, factorial, isfinite


def _nonnegative_rate(value: float) -> float:
    if isinstance(value, bool):
        raise ValueError("rate must be a non-negative real number")
    rate = float(value)
    if not isfinite(rate) or rate < 0:
        raise ValueError("rate must be a non-negative finite real number")
    return rate


def _positive_horizon(value: float) -> float:
    if isinstance(value, bool):
        raise ValueError("horizon must be a positive real number")
    horizon = float(value)
    if not isfinite(horizon) or horizon <= 0:
        raise ValueError("horizon must be a positive finite real number")
    return horizon


def poisson_mass_interval(mean: float, start: int, stop: int) -> float:
    """Return P(start <= Pois(mean) < stop) for integers 0<=start<stop."""
    if isinstance(mean, bool):
        raise ValueError("mean must be a non-negative real number")
    lam = float(mean)
    if not isfinite(lam) or lam < 0:
        raise ValueError("mean must be non-negative and finite")
    if not isinstance(start, int) or isinstance(start, bool) or start < 0:
        raise ValueError("start must be a non-negative integer")
    if not isinstance(stop, int) or isinstance(stop, bool) or stop <= start:
        raise ValueError("stop must be an integer larger than start")
    if lam == 0:
        return 1.0 if start == 0 else 0.0
    return exp(-lam) * sum(lam**count / factorial(count) for count in range(start, stop))


@dataclass(frozen=True)
class ContinuousTimeDepletionReachCertificate:
    """Exact/approximate reach consequences of one continuous-time depletion clock."""

    capacity: int
    saturation_level: int
    depletion_rate: float

    @property
    def closed_class_count(self) -> int:
        return self.saturation_level + 1

    @property
    def open_exact_class_count(self) -> int:
        return self.closed_class_count if self.depletion_rate == 0 else self.capacity + 1

    @property
    def exact_complexity_jumps_at_zero_rate(self) -> bool:
        return self.capacity + 1 > self.closed_class_count

    def pair_event_gap(self, lower: int, upper: int, horizon: float) -> float:
        """Difference in P(Y_t<L) for two saturated initial abundances."""
        if not self.saturation_level <= lower < upper <= self.capacity:
            raise ValueError("pair must be distinct saturated abundance states")
        t = _positive_horizon(horizon)
        lower_threshold = lower - self.saturation_level + 1
        upper_threshold = upper - self.saturation_level + 1
        mean = self.depletion_rate * t
        return poisson_mass_interval(mean, lower_threshold, upper_threshold)

    def threshold_pair_event_gap(self, horizon: float) -> float:
        """Gap for initial abundances L and L+1: lambda exp(-lambda)."""
        return self.pair_event_gap(
            self.saturation_level,
            self.saturation_level + 1,
            horizon,
        )

    @property
    def threshold_gap_maximizing_horizon(self) -> float | None:
        if self.depletion_rate == 0:
            return None
        return 1.0 / self.depletion_rate

    @property
    def threshold_gap_at_maximizing_horizon(self) -> float:
        if self.depletion_rate == 0:
            return 0.0
        return 1.0 / e

    def minimum_common_final_output_tv_error_lower_bound(self, horizon: float) -> float:
        """Any common final-output law for L and L+1 incurs >= event-gap/2 TV error."""
        return self.threshold_pair_event_gap(horizon) / 2.0

    def verify(self) -> bool:
        try:
            if not isinstance(self.capacity, int) or isinstance(self.capacity, bool):
                return False
            if not isinstance(self.saturation_level, int) or isinstance(self.saturation_level, bool):
                return False
            if self.saturation_level < 1 or self.capacity < self.saturation_level + 1:
                return False
            rate = _nonnegative_rate(self.depletion_rate)
            if rate != self.depletion_rate:
                return False
            if self.closed_class_count != self.saturation_level + 1:
                return False
            if rate == 0:
                if self.open_exact_class_count != self.closed_class_count:
                    return False
                if self.threshold_pair_event_gap(1.0) != 0.0:
                    return False
                return self.threshold_gap_maximizing_horizon is None

            if self.open_exact_class_count != self.capacity + 1:
                return False
            diagnostic_horizon = 1.0 / rate
            if abs(self.threshold_pair_event_gap(diagnostic_horizon) - 1.0 / e) > 1e-12:
                return False
            if abs(self.threshold_gap_at_maximizing_horizon - 1.0 / e) > 1e-12:
                return False
            for lower in range(self.saturation_level, self.capacity):
                for upper in range(lower + 1, self.capacity + 1):
                    if self.pair_event_gap(lower, upper, diagnostic_horizon) <= 0:
                        return False
            return True
        except (OverflowError, TypeError, ValueError, ZeroDivisionError):
            return False


def certify_continuous_time_depletion_reach(
    capacity: int,
    saturation_level: int,
    depletion_rate: float,
) -> ContinuousTimeDepletionReachCertificate:
    certificate = ContinuousTimeDepletionReachCertificate(
        capacity=capacity,
        saturation_level=saturation_level,
        depletion_rate=_nonnegative_rate(depletion_rate),
    )
    if not certificate.verify():
        raise ValueError("continuous-time depletion reach witness did not verify")
    return certificate


__all__ = [
    "ContinuousTimeDepletionReachCertificate",
    "poisson_mass_interval",
    "certify_continuous_time_depletion_reach",
]
