from math import e, log

import pytest

from causal_model.per_capita_mortality_reach import (
    binomial_below_threshold_probability,
    certify_per_capita_mortality_reach,
)


def test_zero_mortality_preserves_saturation_compression() -> None:
    certificate = certify_per_capita_mortality_reach(8, 2, 0.0)
    assert certificate.verify()
    assert certificate.closed_class_count == 3
    assert certificate.open_exact_class_count == 3
    assert certificate.threshold_pair_event_gap(10.0) == 0.0


def test_positive_per_capita_mortality_restores_full_exact_classes() -> None:
    certificate = certify_per_capita_mortality_reach(8, 2, 0.1)
    assert certificate.verify()
    assert certificate.open_exact_class_count == 9
    expected_horizon = log(3.0 / 2.0) / 0.1
    assert abs(certificate.threshold_gap_maximizing_horizon - expected_horizon) < 1e-12
    assert abs(certificate.threshold_gap_at_maximizing_horizon - (2.0 / 3.0) ** 3) < 1e-12
    assert abs(
        certificate.threshold_pair_event_gap(expected_horizon) - (2.0 / 3.0) ** 3
    ) < 1e-12


def test_rate_rescaling_shifts_informative_horizon() -> None:
    slow = certify_per_capita_mortality_reach(6, 3, 0.01)
    fast = certify_per_capita_mortality_reach(6, 3, 2.0)
    assert abs(
        slow.threshold_pair_event_gap(slow.threshold_gap_maximizing_horizon)
        - fast.threshold_pair_event_gap(fast.threshold_gap_maximizing_horizon)
    ) < 1e-12
    assert abs(
        slow.threshold_gap_at_maximizing_horizon - (3.0 / 4.0) ** 4
    ) < 1e-12


def test_all_saturated_abundances_have_distinct_final_response_laws() -> None:
    certificate = certify_per_capita_mortality_reach(7, 2, 0.4)
    horizon = 1.3
    for lower in range(2, 7):
        for upper in range(lower + 1, 8):
            assert certificate.pair_event_gap(lower, upper, horizon) > 0.0
            assert certificate.zero_output_probability(lower, horizon) > certificate.zero_output_probability(upper, horizon)


def test_threshold_formula_matches_binomial_sum() -> None:
    certificate = certify_per_capita_mortality_reach(5, 2, 0.3)
    horizon = 2.0
    q = certificate.survival_probability(horizon)
    direct = (
        binomial_below_threshold_probability(2, 2, q)
        - binomial_below_threshold_probability(3, 2, q)
    )
    assert abs(direct - 2.0 * q**2 * (1.0 - q)) < 1e-12


def test_large_threshold_maximum_approaches_inverse_e() -> None:
    values = [(level / (level + 1.0)) ** (level + 1) for level in (5, 20, 100)]
    assert abs(values[-1] - 1.0 / e) < 0.01
    assert values[0] < values[1] < values[2]


def test_invalid_per_capita_contracts_are_rejected() -> None:
    with pytest.raises(ValueError):
        certify_per_capita_mortality_reach(2, 2, 0.1)
    with pytest.raises(ValueError):
        certify_per_capita_mortality_reach(5, 2, -0.1)
