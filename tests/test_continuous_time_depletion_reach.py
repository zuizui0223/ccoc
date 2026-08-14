from math import e

import pytest

from causal_model.continuous_time_depletion_reach import (
    certify_continuous_time_depletion_reach,
    poisson_mass_interval,
)


def test_zero_rate_preserves_saturation_compression() -> None:
    certificate = certify_continuous_time_depletion_reach(8, 2, 0.0)
    assert certificate.verify()
    assert certificate.closed_class_count == 3
    assert certificate.open_exact_class_count == 3
    assert certificate.threshold_pair_event_gap(10.0) == 0.0
    assert certificate.threshold_gap_maximizing_horizon is None


def test_any_positive_rate_restores_full_exact_abundance_classes() -> None:
    certificate = certify_continuous_time_depletion_reach(8, 2, 0.2)
    assert certificate.verify()
    assert certificate.open_exact_class_count == 9
    assert certificate.threshold_gap_maximizing_horizon == 5.0
    assert abs(certificate.threshold_pair_event_gap(5.0) - 1.0 / e) < 1e-12
    assert abs(
        certificate.minimum_common_final_output_tv_error_lower_bound(5.0)
        - 1.0 / (2.0 * e)
    ) < 1e-12


def test_rare_rate_is_compensated_by_inverse_rate_horizon() -> None:
    rare = certify_continuous_time_depletion_reach(6, 2, 0.01)
    fast = certify_continuous_time_depletion_reach(6, 2, 2.0)
    assert abs(rare.threshold_pair_event_gap(100.0) - 1.0 / e) < 1e-12
    assert abs(fast.threshold_pair_event_gap(0.5) - 1.0 / e) < 1e-12


def test_all_saturated_pairs_have_positive_finite_horizon_witness() -> None:
    certificate = certify_continuous_time_depletion_reach(7, 2, 0.5)
    horizon = 2.0
    for lower in range(2, 7):
        for upper in range(lower + 1, 8):
            assert certificate.pair_event_gap(lower, upper, horizon) > 0.0


def test_poisson_interval_matches_threshold_formula() -> None:
    assert abs(poisson_mass_interval(1.0, 1, 2) - 1.0 / e) < 1e-12
    assert poisson_mass_interval(0.0, 1, 2) == 0.0


def test_invalid_continuous_time_depletion_contracts_are_rejected() -> None:
    with pytest.raises(ValueError):
        certify_continuous_time_depletion_reach(3, 3, 0.1)
    with pytest.raises(ValueError):
        certify_continuous_time_depletion_reach(5, 2, -0.1)
