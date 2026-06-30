import pytest

from causal_model.causal_closure_calculus import ClosureKind, FiniteDeterministicRuleSystem
from causal_model.observation_regime_closure import (
    ObservationRegimeRulePair,
    ObservationRegimeVerdict,
    RegimeConsensusKind,
    classify_observation_regime_pair,
    exhaustive_observation_regime_pairs,
    exhaustive_regime_summary,
    regime_verdict,
    summarize_regime_candidates,
)


def rule(rule_id, successors):
    states = tuple(successors)
    return FiniteDeterministicRuleSystem(
        states=states,
        successor_by_state=successors,
        rule_id=rule_id,
    )


def closing_rule(rule_id="closing"):
    return rule(rule_id, {"a": "root", "b": "a", "root": "root"})


def cyclic_rule(rule_id="cyclic"):
    return rule(rule_id, {"a": "b", "b": "a", "root": "a"})


def multistable_rule(rule_id="multi"):
    return rule(rule_id, {"a": "a", "b": "b", "root": "a"})


def test_observation_induced_closure_is_exactly_a_nonclosing_to_closing_regime_change():
    pair = ObservationRegimeRulePair(
        candidate_id="induced-closure",
        natural_rule=cyclic_rule("natural"),
        observed_rule=closing_rule("observed"),
    )
    result = classify_observation_regime_pair(pair)

    assert result.natural_classification.kind is ClosureKind.RECURRENT_NONCLOSURE
    assert result.observed_classification.kind is ClosureKind.GLOBAL_CLOSURE
    assert result.verdict is ObservationRegimeVerdict.OBSERVATION_INDUCED_CLOSURE
    assert result.natural_classification.recurrent_cycle.cycle_states == ("a", "b")
    assert result.observed_classification.global_closure.attractor_state == "root"


def test_observation_induced_recurrence_is_not_confused_with_multistability():
    pair = ObservationRegimeRulePair(
        candidate_id="induced-cycle",
        natural_rule=closing_rule("natural"),
        observed_rule=cyclic_rule("observed"),
    )
    result = classify_observation_regime_pair(pair)
    assert result.verdict is ObservationRegimeVerdict.OBSERVATION_INDUCED_RECURRENCE

    assert regime_verdict(
        ClosureKind.GLOBAL_CLOSURE,
        ClosureKind.MULTISTABLE_NONCLOSURE,
    ) is ObservationRegimeVerdict.OBSERVATION_INDUCED_MULTISTABILITY


def test_shared_candidate_verdict_is_decisive_but_disagreement_is_unresolved():
    first = ObservationRegimeRulePair("one", cyclic_rule("n1"), closing_rule("o1"))
    second = ObservationRegimeRulePair("two", multistable_rule("n2"), closing_rule("o2"))
    decisive = summarize_regime_candidates((first, second))

    assert decisive.kind is RegimeConsensusKind.DECISIVE
    assert decisive.verdict is ObservationRegimeVerdict.OBSERVATION_INDUCED_CLOSURE

    conflicting = ObservationRegimeRulePair("three", closing_rule("n3"), cyclic_rule("o3"))
    unresolved = summarize_regime_candidates((first, conflicting))
    assert unresolved.kind is RegimeConsensusKind.UNRESOLVED
    assert unresolved.verdict is None


def test_regime_pair_rejects_state_space_drift_and_duplicate_candidate_ids():
    with pytest.raises(ValueError, match="identical ordered state spaces"):
        ObservationRegimeRulePair(
            "bad",
            FiniteDeterministicRuleSystem(("a",), {"a": "a"}),
            closing_rule(),
        )

    first = ObservationRegimeRulePair("same", cyclic_rule("n1"), closing_rule("o1"))
    second = ObservationRegimeRulePair("same", closing_rule("n2"), cyclic_rule("o2"))
    with pytest.raises(ValueError, match="candidate IDs must be unique"):
        summarize_regime_candidates((first, second))


def test_exhaustive_three_state_regime_pairs_are_complete_and_all_core_regimes_occur():
    # Three labelled states have 3^3=27 maps, hence 27^2=729 ordered regime pairs.
    pairs = tuple(exhaustive_observation_regime_pairs(3))
    assert len(pairs) == 729
    summary = exhaustive_regime_summary(3)
    assert sum(summary[3].values()) == 729
    assert summary[3][ObservationRegimeVerdict.OBSERVER_INDEPENDENT_CLOSURE] > 0
    assert summary[3][ObservationRegimeVerdict.OBSERVATION_INDUCED_CLOSURE] > 0
    assert summary[3][ObservationRegimeVerdict.OBSERVATION_INDUCED_RECURRENCE] > 0
    assert summary[3][ObservationRegimeVerdict.REGIME_DEPENDENT_NONCLOSURE] > 0
