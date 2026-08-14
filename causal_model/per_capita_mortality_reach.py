"""Per-capita mortality reach for saturated ecological responses.

For independent per-capita mortality at rate mu, each of n initial individuals
survives to time t with probability q=exp(-mu*t), so N_t~Binomial(n,q).  A capped
response Y=min(L,N) therefore has different finite-horizon laws for every distinct
initial abundance whenever mu>0.  In particular, the threshold pair L and L+1 has
below-threshold event-probability gap L*q**L*(1-q), maximized at
q=L/(L+1).

The binomial survival model is classical.  The CCOC role is the ecological
portability consequence: any positive mortality rate restores hidden
oversaturation as exact future-relevant information, while the informative time
scale is set by rate and threshold.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import comb, exp, isfinite, log


def _nonnegative_rate(value: float) -> float:
    if isinstance(value, bool):
        raise ValueError("rate must be a non-negative real number")
    rate = float(value)
    if not isfinite(rate) or rate < 0:
        raise ValueError("rate must be a non-negative finite real number")
    return rate


def _positive_horizon(value: float) -> float:
    if isinstance(value, bool):
        raise ValueError("horizon must be positive")
    horizon = float(value)
    if not isfinite(horizon) or horizon <= 0:
        raise ValueError("horizon must be positive and finite")
    return horizon


def binomial_below_threshold_probability(initial: int, threshold: int, survival_probability: float) -> float:
    if not isinstance(initial, int) or isinstance(initial, bool) or initial < 0:
        raise ValueError("initial must be a non-negative integer")
    if not isinstance(threshold, int) or isinstance(threshold, bool) or threshold < 1:
        raise ValueError("threshold must be a positive integer")
    q = float(survival_probability)
    if not isfinite(q) or not 0.0 <= q <= 1.0:
        raise ValueError("survival_probability must lie in [0,1]")
    upper = min(threshold, initial + 1)
    return sum(
        comb(initial, survivors) * q**survivors * (1.0 - q) ** (initial - survivors)
        for survivors in range(upper)
    )


@dataclass(frozen=True)
class PerCapitaMortalityReachCertificate:
    capacity: int
    saturation_level: int
    mortality_rate: float

    @property
    def closed_class_count(self) -> int:
        return self.saturation_level + 1

    @property
    def open_exact_class_count(self) -> int:
        return self.closed_class_count if self.mortality_rate == 0 else self.capacity + 1

    def survival_probability(self, horizon: float) -> float:
        t = _positive_horizon(horizon)
        return exp(-self.mortality_rate * t)

    def below_threshold_probability(self, initial: int, horizon: float) -> float:
        if not 0 <= initial <= self.capacity:
            raise ValueError("initial abundance outside finite domain")
        return binomial_below_threshold_probability(
            initial,
            self.saturation_level,
            self.survival_probability(horizon),
        )

    def pair_event_gap(self, lower: int, upper: int, horizon: float) -> float:
        if not self.saturation_level <= lower < upper <= self.capacity:
            raise ValueError("pair must be distinct saturated abundances")
        return self.below_threshold_probability(lower, horizon) - self.below_threshold_probability(upper, horizon)

    def threshold_pair_event_gap(self, horizon: float) -> float:
        q = self.survival_probability(horizon)
        level = self.saturation_level
        return level * q**level * (1.0 - q)

    @property
    def threshold_gap_maximizing_survival_probability(self) -> float | None:
        if self.mortality_rate == 0:
            return None
        level = self.saturation_level
        return level / (level + 1.0)

    @property
    def threshold_gap_maximizing_horizon(self) -> float | None:
        if self.mortality_rate == 0:
            return None
        level = self.saturation_level
        return log((level + 1.0) / level) / self.mortality_rate

    @property
    def threshold_gap_at_maximizing_horizon(self) -> float:
        if self.mortality_rate == 0:
            return 0.0
        level = self.saturation_level
        return (level / (level + 1.0)) ** (level + 1)

    def zero_output_probability(self, initial: int, horizon: float) -> float:
        if not 0 <= initial <= self.capacity:
            raise ValueError("initial abundance outside finite domain")
        q = self.survival_probability(horizon)
        return (1.0 - q) ** initial

    def minimum_common_final_output_tv_error_lower_bound(self, horizon: float) -> float:
        return self.threshold_pair_event_gap(horizon) / 2.0

    def verify(self) -> bool:
        try:
            if not isinstance(self.capacity, int) or isinstance(self.capacity, bool):
                return False
            if not isinstance(self.saturation_level, int) or isinstance(self.saturation_level, bool):
                return False
            if self.saturation_level < 1 or self.capacity < self.saturation_level + 1:
                return False
            rate = _nonnegative_rate(self.mortality_rate)
            if rate != self.mortality_rate:
                return False
            if rate == 0:
                if self.open_exact_class_count != self.closed_class_count:
                    return False
                if self.threshold_pair_event_gap(1.0) != 0.0:
                    return False
                return self.threshold_gap_maximizing_horizon is None

            if self.open_exact_class_count != self.capacity + 1:
                return False
            horizon = self.threshold_gap_maximizing_horizon
            if horizon is None:
                return False
            expected = self.threshold_gap_at_maximizing_horizon
            if abs(self.threshold_pair_event_gap(horizon) - expected) > 1e-12:
                return False
            # Any two distinct positive abundances have different all-death
            # probabilities at any finite positive horizon, hence different output laws.
            for lower in range(self.saturation_level, self.capacity):
                for upper in range(lower + 1, self.capacity + 1):
                    if self.pair_event_gap(lower, upper, horizon) <= 0:
                        return False
                    if not self.zero_output_probability(lower, horizon) > self.zero_output_probability(upper, horizon):
                        return False
            return True
        except (OverflowError, TypeError, ValueError, ZeroDivisionError):
            return False


def certify_per_capita_mortality_reach(
    capacity: int,
    saturation_level: int,
    mortality_rate: float,
) -> PerCapitaMortalityReachCertificate:
    certificate = PerCapitaMortalityReachCertificate(
        capacity=capacity,
        saturation_level=saturation_level,
        mortality_rate=_nonnegative_rate(mortality_rate),
    )
    if not certificate.verify():
        raise ValueError("per-capita mortality reach witness did not verify")
    return certificate


__all__ = [
    "PerCapitaMortalityReachCertificate",
    "binomial_below_threshold_probability",
    "certify_per_capita_mortality_reach",
]
