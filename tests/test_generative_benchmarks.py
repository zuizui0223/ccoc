import pytest

from causal_model.generative_benchmarks import (
    TwoDriverFamilyParameters,
    evaluate_two_driver_family,
    phase_table_markdown,
    sweep_two_driver_family,
)


def test_baseline_declared_or_world_has_zero_false_necessity_risk() -> None:
    point = evaluate_two_driver_family(TwoDriverFamilyParameters())
    assert point.declared_forced_on
    assert point.reported_observation_probability == pytest.approx(0.25)
    assert point.false_necessity_risk == 0.0
    assert point.perfect_measurement_focal_off_probability == 0.0


def test_latent_route_prevalence_one_has_one_third_exact_risk() -> None:
    point = evaluate_two_driver_family(
        TwoDriverFamilyParameters(latent_driver_prevalence=1.0)
    )
    assert point.reported_observation_probability == pytest.approx(0.375)
    assert point.false_necessity_risk == pytest.approx(1.0 / 3.0)
    assert point.perfect_measurement_focal_off_probability == pytest.approx(1.0 / 3.0)


def test_ninety_percent_witness_sensitivity_has_one_twelfth_exact_risk() -> None:
    point = evaluate_two_driver_family(
        TwoDriverFamilyParameters(witness_sensitivity=0.9)
    )
    assert point.reported_observation_probability == pytest.approx(0.3)
    assert point.false_necessity_risk == pytest.approx(1.0 / 12.0)
    assert point.perfect_measurement_focal_off_probability == 0.0


def test_full_inhibition_has_one_third_exact_risk_even_with_perfect_detection() -> None:
    point = evaluate_two_driver_family(
        TwoDriverFamilyParameters(inhibition_prevalence=1.0)
    )
    assert point.reported_observation_probability == pytest.approx(0.75)
    assert point.false_necessity_risk == pytest.approx(1.0 / 3.0)
    assert point.perfect_measurement_focal_off_probability == pytest.approx(1.0 / 3.0)


def test_pure_conjunction_marks_the_report_impossible_under_perfect_measurement() -> None:
    point = evaluate_two_driver_family(
        TwoDriverFamilyParameters(conjunction_prevalence=1.0)
    )
    assert point.report_is_impossible
    assert point.false_necessity_risk is None
    assert point.perfect_measurement_focal_off_probability is None


def test_compatibility_constraint_can_remove_competitor_only_false_necessity_states() -> None:
    point = evaluate_two_driver_family(
        TwoDriverFamilyParameters(compatibility_constraint_prevalence=1.0)
    )
    assert point.reported_observation_probability == pytest.approx(0.25)
    assert point.false_necessity_risk == 0.0


def test_sweep_is_cartesian_exact_and_phase_table_is_renderable() -> None:
    points = sweep_two_driver_family(
        {
            "latent_driver_prevalence": (0.0, 1.0),
            "witness_sensitivity": (1.0, 0.9),
        }
    )
    assert len(points) == 4
    assert points[0].parameters.latent_driver_prevalence == 0.0
    assert points[0].parameters.witness_sensitivity == 1.0
    table = phase_table_markdown(points, digits=3)
    assert "false_necessity_risk" in table
    assert table.count("\n") == len(points) + 1


def test_invalid_grid_and_probability_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="between zero and one"):
        TwoDriverFamilyParameters(inhibition_prevalence=1.1)
    with pytest.raises(ValueError, match="unknown family parameters"):
        sweep_two_driver_family({"unknown": (0.0,)})
    with pytest.raises(ValueError, match="at least one value"):
        sweep_two_driver_family({"witness_sensitivity": ()})
    with pytest.raises(ValueError, match="non-negative"):
        phase_table_markdown((), digits=-1)
