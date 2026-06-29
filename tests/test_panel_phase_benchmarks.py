import pytest

from causal_model.panel_phase_benchmarks import (
    MultiCompetitorFamilyParameters,
    PanelStrategy,
    compare_panel_strategies,
    declared_multi_competitor_model,
    panel_phase_table_markdown,
    strict_greedy_panel_traits,
    sweep_panel_phase_family,
)


def test_exact_joint_panel_resolves_canonical_synergy_but_strict_greedy_stops() -> None:
    comparison = compare_panel_strategies(MultiCompetitorFamilyParameters())
    assert comparison.exact.strategy is PanelStrategy.EXACT
    assert comparison.exact.selected_null_traits == ("witness_1", "witness_2")
    assert comparison.exact.declared_forced_on
    assert comparison.strict_greedy.strategy is PanelStrategy.STRICT_GREEDY
    assert comparison.strict_greedy.selected_null_traits == ()
    assert not comparison.strict_greedy.declared_forced_on
    assert comparison.synergy_gap == 2
    assert comparison.exact.reported_panel_probability == pytest.approx(0.125)
    assert comparison.exact.false_necessity_risk == 0.0
    assert comparison.strict_greedy.posterior_focal_off_probability == pytest.approx(3.0 / 7.0)
    assert comparison.strict_greedy.false_necessity_risk is None


def test_one_latent_route_creates_one_third_false_necessity_risk_for_exact_panel() -> None:
    comparison = compare_panel_strategies(
        MultiCompetitorFamilyParameters(
            latent_route_count=1,
            latent_on_probability_low=0.5,
            latent_on_probability_high=0.5,
        )
    )
    assert comparison.exact.reported_panel_probability == pytest.approx(3.0 / 16.0)
    assert comparison.exact.false_necessity_risk == pytest.approx(1.0 / 3.0)
    assert comparison.exact.perfect_measurement_focal_off_probability == pytest.approx(1.0 / 3.0)


def test_correlated_environment_can_make_joint_null_panel_more_informative() -> None:
    comparison = compare_panel_strategies(
        MultiCompetitorFamilyParameters(
            competitor_on_probability_low=0.0,
            competitor_on_probability_high=1.0,
            witness_sensitivity=0.9,
        )
    )
    assert comparison.exact.reported_panel_probability == pytest.approx(0.255)
    assert comparison.exact.false_necessity_risk == pytest.approx(1.0 / 102.0)


def test_context_correlated_inhibition_restores_false_necessity_risk() -> None:
    comparison = compare_panel_strategies(
        MultiCompetitorFamilyParameters(
            competitor_on_probability_low=0.0,
            competitor_on_probability_high=1.0,
            inhibition_probability_low=0.0,
            inhibition_probability_high=1.0,
        )
    )
    assert comparison.exact.reported_panel_probability == pytest.approx(0.75)
    assert comparison.exact.false_necessity_risk == pytest.approx(1.0 / 3.0)
    assert comparison.exact.perfect_measurement_focal_off_probability == pytest.approx(1.0 / 3.0)


def test_pure_conjunction_makes_exact_all_witness_null_panel_impossible() -> None:
    comparison = compare_panel_strategies(
        MultiCompetitorFamilyParameters(conjunction_context_prevalence=1.0)
    )
    assert comparison.exact.reported_panel_probability == 0.0
    assert comparison.exact.false_necessity_risk is None
    assert comparison.exact.perfect_measurement_focal_off_probability is None


def test_exact_panel_scales_to_three_competitors_and_greedy_still_has_no_singleton_gain() -> None:
    parameters = MultiCompetitorFamilyParameters(competitor_count=3)
    comparison = compare_panel_strategies(parameters)
    assert comparison.exact.selected_null_traits == ("witness_1", "witness_2", "witness_3")
    assert comparison.strict_greedy.selected_null_traits == ()
    assert comparison.synergy_gap == 3
    assert comparison.exact.reported_panel_probability == pytest.approx(1.0 / 16.0)
    assert comparison.exact.false_necessity_risk == 0.0


def test_declared_model_and_strict_greedy_input_validation() -> None:
    model = declared_multi_competitor_model(3)
    assert model.mechanism_count == 4
    assert model.driver_sets["target"] == frozenset({0, 1, 2, 3})
    assert strict_greedy_panel_traits(MultiCompetitorFamilyParameters(competitor_count=3)) == ()
    with pytest.raises(ValueError, match="at least two"):
        MultiCompetitorFamilyParameters(competitor_count=1)
    with pytest.raises(ValueError, match="non-negative"):
        MultiCompetitorFamilyParameters(latent_route_count=-1)
    with pytest.raises(ValueError, match="at least two"):
        declared_multi_competitor_model(1)


def test_phase_sweep_and_markdown_table_are_deterministic() -> None:
    comparisons = sweep_panel_phase_family(
        {
            "competitor_count": (2, 3),
            "latent_route_count": (0, 1),
            "latent_on_probability_low": (0.0,),
            "latent_on_probability_high": (0.0,),
        }
    )
    assert len(comparisons) == 4
    assert comparisons[0].parameters.competitor_count == 2
    table = panel_phase_table_markdown(comparisons, digits=3)
    assert "exact panel" in table
    assert table.count("\n") == len(comparisons) + 1
    with pytest.raises(ValueError, match="unknown family parameters"):
        sweep_panel_phase_family({"not_a_parameter": (0.0,)})
    with pytest.raises(ValueError, match="at least one value"):
        sweep_panel_phase_family({"competitor_count": ()})
    with pytest.raises(ValueError, match="non-negative"):
        panel_phase_table_markdown((), digits=-1)
