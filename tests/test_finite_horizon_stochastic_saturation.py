from math import exp, isinf

import pytest

from causal_model.finite_horizon_stochastic_saturation import (
    certify_finite_horizon_saturation_approximation,
    certify_finite_horizon_saturation_family,
)


def test_constant_rate_approximate_error_is_capacity_independent() -> None:
    family = certify_finite_horizon_saturation_family(
        capacities=(2, 10, 100),
        saturation_level=2,
        rate=0.1,
        horizon=3.0,
        mechanism="constant_rate",
    )
    expected = 1.0 - exp(-0.3)
    assert family.verify()
    assert family.approximate_macro_state_count == 3
    assert family.capacities == (2, 10, 100)
    assert abs(family.saturated_path_tv_error - expected) < 1e-12
    assert all(abs(stage.saturated_path_tv_error - expected) < 1e-12 for stage in family.stages)


def test_per_capita_error_depends_on_threshold_not_capacity() -> None:
    family = certify_finite_horizon_saturation_family(
        capacities=(3, 12, 80),
        saturation_level=3,
        rate=0.05,
        horizon=4.0,
        mechanism="per_capita",
    )
    expected = 1.0 - exp(-0.05 * 3 * 4.0)
    assert family.verify()
    assert family.approximate_macro_state_count == 4
    assert abs(family.saturated_path_tv_error - expected) < 1e-12
    assert family.stages[-1].exact_response_state_count == 81
    assert family.stages[-1].compression_ratio == 81 / 4


def test_exact_complexity_can_grow_while_approximate_error_stays_fixed() -> None:
    family = certify_finite_horizon_saturation_family(
        capacities=(2, 20, 200),
        saturation_level=2,
        rate=0.02,
        horizon=5.0,
        mechanism="constant_rate",
    )
    exact_counts = tuple(stage.exact_response_state_count for stage in family.stages)
    assert exact_counts == (3, 21, 201)
    assert len({stage.saturated_path_tv_error for stage in family.stages}) == 1


def test_tolerance_horizon_is_exact_inverse_of_error_bound() -> None:
    certificate = certify_finite_horizon_saturation_approximation(
        capacity=50,
        saturation_level=5,
        rate=0.2,
        horizon=1.0,
        mechanism="per_capita",
    )
    tolerance = 0.1
    max_horizon = certificate.maximum_horizon_for_tolerance(tolerance)
    boundary = certify_finite_horizon_saturation_approximation(
        capacity=50,
        saturation_level=5,
        rate=0.2,
        horizon=max_horizon,
        mechanism="per_capita",
    )
    assert abs(boundary.saturated_path_tv_error - tolerance) < 1e-12
    assert boundary.meets_tolerance(tolerance)


def test_zero_rate_makes_approximation_exact_for_every_horizon() -> None:
    certificate = certify_finite_horizon_saturation_approximation(
        capacity=100,
        saturation_level=3,
        rate=0.0,
        horizon=1000.0,
        mechanism="constant_rate",
    )
    assert certificate.verify()
    assert certificate.saturated_path_tv_error == 0.0
    assert certificate.exact_response_state_count == 4
    assert isinf(certificate.maximum_horizon_for_tolerance(0.0))


def test_invalid_finite_horizon_contracts_are_rejected() -> None:
    with pytest.raises(ValueError):
        certify_finite_horizon_saturation_approximation(10, 2, 0.1, 0.0, "constant_rate")
    with pytest.raises(ValueError):
        certify_finite_horizon_saturation_approximation(10, 2, 0.1, 1.0, "unknown")  # type: ignore[arg-type]
