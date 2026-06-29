from itertools import product

import pytest

from causal_model.failure_modes import BinaryObservationChannel, TruthTableModel
from causal_model.observation_design import NullObservationCandidate
from causal_model.replaceability import StructuralModel
from causal_model.robust_panel_design import (
    FinitePanelScenario,
    RobustObjective,
    choose_coverage_greedy_panel,
    choose_minimum_cost_panel,
    choose_robust_panel,
    compare_panel_selection_strategies,
    evaluate_resolving_panel,
)


def _declared_model() -> StructuralModel:
    # Mechanism 3 is an unmodelled inhibitor in the declared target grammar.
    return StructuralModel(
        mechanism_count=4,
        driver_sets={
            "target": frozenset({0, 1, 2}),
            "shared": frozenset({1, 2}),
            "witness_1": frozenset({1}),
            "witness_2": frozenset({2}),
        },
    )


def _truth_model(*, shared_inhibited: bool) -> TruthTableModel:
    states = tuple(product((0, 1), repeat=4))
    return TruthTableModel(
        mechanism_count=4,
        trait_true_states={
            "target": frozenset(state for state in states if state[0] or state[1] or state[2]),
            "shared": frozenset(
                state
                for state in states
                if (state[1] or state[2]) and (not shared_inhibited or not state[3])
            ),
            "witness_1": frozenset(state for state in states if state[1]),
            "witness_2": frozenset(state for state in states if state[2]),
        },
    )


def _candidates() -> tuple[NullObservationCandidate, ...]:
    return (
        NullObservationCandidate("shared", cost=0.5),
        NullObservationCandidate("witness_1", cost=1.0),
        NullObservationCandidate("witness_2", cost=1.0),
    )


def _scenarios() -> tuple[FinitePanelScenario, ...]:
    # The frequent scenario makes private witnesses noisy but leaves the shared
    # witness reliable. The rarer scenario makes the shared witness suppressible
    # while private witnesses remain reliable.
    return (
        FinitePanelScenario(
            "frequent_private_noise",
            _truth_model(shared_inhibited=False),
            weight=10.0,
            channels={
                "witness_1": BinaryObservationChannel(present_if_true_present=0.9),
                "witness_2": BinaryObservationChannel(present_if_true_present=0.9),
            },
        ),
        FinitePanelScenario(
            "rare_shared_inhibition",
            _truth_model(shared_inhibited=True),
            weight=1.0,
        ),
    )


def test_shared_witness_is_cheapest_and_coverage_greedy_choice() -> None:
    comparison = compare_panel_selection_strategies(
        _declared_model(),
        focal_mechanism=0,
        target_trait="target",
        candidates=_candidates(),
        scenarios=_scenarios(),
        max_cost=0.5,
    )
    assert comparison.minimum_cost is not None
    assert comparison.coverage_greedy is not None
    assert comparison.minimum_cost.selected_null_traits == ("shared",)
    assert comparison.coverage_greedy.selected_null_traits == ("shared",)
    assert comparison.minimum_cost.total_cost == 0.5
    assert comparison.minimum_cost.worst_case_risk == pytest.approx(3.0 / 8.0)


def test_minimax_prefers_redundant_private_witnesses_over_cheap_fragile_shared_witness() -> None:
    # The all-three-witness panel would be safer still, but costs 2.5 and is
    # unavailable under this budget.
    result = choose_robust_panel(
        _declared_model(),
        focal_mechanism=0,
        target_trait="target",
        candidates=_candidates(),
        scenarios=_scenarios(),
        objective=RobustObjective.MINIMAX,
        max_cost=2.0,
    )
    assert result is not None
    assert result.selected_null_traits == ("witness_1", "witness_2")
    assert result.total_cost == 2.0
    assert result.worst_case_risk == pytest.approx(21.0 / 142.0)
    assert result.weighted_mean_risk == pytest.approx(105.0 / 781.0)


def test_weighted_mean_can_prefer_a_hybrid_panel_when_rarer_fragility_is_downweighted() -> None:
    # At this budget the private pair and all-three panel are unavailable. The
    # weighted-mean objective keeps the cheap shared witness and adds one private
    # witness as insurance against the inhibited shared channel.
    result = choose_robust_panel(
        _declared_model(),
        focal_mechanism=0,
        target_trait="target",
        candidates=_candidates(),
        scenarios=_scenarios(),
        objective=RobustObjective.WEIGHTED_MEAN,
        max_cost=1.5,
    )
    assert result is not None
    assert result.selected_null_traits == ("shared", "witness_1")
    assert result.weighted_mean_risk == pytest.approx(1.0 / 44.0)
    assert result.worst_case_risk == pytest.approx(1.0 / 4.0)


def test_unconstrained_minimax_uses_all_redundant_witnesses_when_they_remove_every_declared_risk() -> None:
    result = choose_robust_panel(
        _declared_model(),
        focal_mechanism=0,
        target_trait="target",
        candidates=_candidates(),
        scenarios=_scenarios(),
        objective=RobustObjective.MINIMAX,
    )
    assert result is not None
    assert result.selected_null_traits == ("shared", "witness_1", "witness_2")
    assert result.total_cost == 2.5
    assert result.worst_case_risk == 0.0


def test_per_scenario_risks_separate_measurement_and_structural_fragility() -> None:
    shared = evaluate_resolving_panel(
        _declared_model(),
        focal_mechanism=0,
        target_trait="target",
        selected_candidates=(_candidates()[0],),
        scenarios=_scenarios(),
    )
    private = evaluate_resolving_panel(
        _declared_model(),
        focal_mechanism=0,
        target_trait="target",
        selected_candidates=_candidates()[1:],
        scenarios=_scenarios(),
    )
    assert shared.scenario_risks[0].focal_off_probability == 0.0
    assert shared.scenario_risks[1].focal_off_probability == pytest.approx(3.0 / 8.0)
    assert private.scenario_risks[0].focal_off_probability == pytest.approx(21.0 / 142.0)
    assert private.scenario_risks[1].focal_off_probability == 0.0


def test_budget_can_make_robust_private_design_unavailable() -> None:
    cost_only = choose_minimum_cost_panel(
        _declared_model(),
        focal_mechanism=0,
        target_trait="target",
        candidates=_candidates(),
        scenarios=_scenarios(),
        max_cost=0.5,
    )
    minimax = choose_robust_panel(
        _declared_model(),
        focal_mechanism=0,
        target_trait="target",
        candidates=_candidates(),
        scenarios=_scenarios(),
        max_cost=0.5,
    )
    greedy = choose_coverage_greedy_panel(
        _declared_model(),
        focal_mechanism=0,
        target_trait="target",
        candidates=_candidates(),
        scenarios=_scenarios(),
        max_cost=0.4,
    )
    assert cost_only is not None and cost_only.selected_null_traits == ("shared",)
    assert minimax is not None and minimax.selected_null_traits == ("shared",)
    assert greedy is None


def test_invalid_panels_and_scenarios_are_rejected() -> None:
    scenario = _scenarios()[0]
    with pytest.raises(ValueError, match="does not force"):
        evaluate_resolving_panel(
            _declared_model(),
            focal_mechanism=0,
            target_trait="target",
            selected_candidates=(_candidates()[1],),
            scenarios=(scenario,),
        )
    with pytest.raises(ValueError, match="at least one finite panel scenario"):
        choose_minimum_cost_panel(
            _declared_model(),
            focal_mechanism=0,
            target_trait="target",
            candidates=_candidates(),
            scenarios=(),
        )
    with pytest.raises(ValueError, match="finite and positive"):
        FinitePanelScenario("bad", _truth_model(shared_inhibited=False), weight=0.0)
