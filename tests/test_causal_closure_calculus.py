from itertools import product

import pytest

from causal_model.causal_closure_calculus import (
    ClosureKind,
    FiniteDeterministicRuleSystem,
    GlobalClosureCertificate,
    RecurrentCycleCertificate,
    classify_closure,
    exhaustive_classification_summary,
    exhaustive_rule_systems,
    find_recurrent_cycle_certificate,
    orbit_until_repeat,
    verify_global_closure_certificate,
    verify_recurrent_cycle_certificate,
)


def system(states, successors):
    return FiniteDeterministicRuleSystem(tuple(states), dict(successors), "test-rule")


def direct_kind(rule):
    """Independent orbit-level classification used only by theorem regression tests."""
    cycles = set()
    for start in rule.states:
        _, cycle = orbit_until_repeat(rule, start)
        rotations = tuple(cycle[offset:] + cycle[:offset] for offset in range(len(cycle)))
        cycles.add(min(rotations))
    if len(cycles) == 1 and len(next(iter(cycles))) == 1:
        return ClosureKind.GLOBAL_CLOSURE
    if any(len(cycle) >= 2 for cycle in cycles):
        return ClosureKind.RECURRENT_NONCLOSURE
    return ClosureKind.MULTISTABLE_NONCLOSURE


def test_ranking_certificate_proves_global_closure_with_finite_time_bound():
    rule = system(
        ("a", "b", "c", "root"),
        (("a", "b"), ("b", "c"), ("c", "root"), ("root", "root")),
    )
    certificate = GlobalClosureCertificate(
        attractor_state="root",
        rank_by_state={"a": 3, "b": 2, "c": 1, "root": 0},
    )
    verify_global_closure_certificate(rule, certificate)

    for state, rank in certificate.rank_by_state.items():
        assert rule.iterate(state, rank) == "root"
        assert rule.iterate(state, rank + 5) == "root"
    assert classify_closure(rule).kind is ClosureKind.GLOBAL_CLOSURE


def test_period_two_certificate_proves_local_transition_rules_do_not_globally_close():
    rule = system(
        ("left", "right", "tail"),
        (("left", "right"), ("right", "left"), ("tail", "left")),
    )
    certificate = RecurrentCycleCertificate(("left", "right"))
    verify_recurrent_cycle_certificate(rule, certificate)
    classification = classify_closure(rule)

    assert classification.kind is ClosureKind.RECURRENT_NONCLOSURE
    assert classification.recurrent_cycle == certificate
    assert rule.iterate("left", 2) == "left"
    assert rule.iterate("right", 2) == "right"


def test_multiple_fixed_points_are_not_confused_with_recurrent_cycles():
    rule = system(
        ("a", "b", "c", "d"),
        (("a", "a"), ("b", "b"), ("c", "a"), ("d", "b")),
    )
    classification = classify_closure(rule)

    assert classification.kind is ClosureKind.MULTISTABLE_NONCLOSURE
    assert classification.multistability.fixed_points == ("a", "b")
    assert find_recurrent_cycle_certificate(rule) is None


def test_invalid_certificates_fail_closed():
    rule = system(
        ("a", "b", "root"),
        (("a", "b"), ("b", "root"), ("root", "root")),
    )
    invalid_rank = GlobalClosureCertificate(
        attractor_state="root",
        rank_by_state={"a": 1, "b": 2, "root": 0},
    )
    with pytest.raises(ValueError, match="strictly decrease"):
        verify_global_closure_certificate(rule, invalid_rank)

    invalid_cycle = RecurrentCycleCertificate(("a", "b"))
    with pytest.raises(ValueError, match="does not match"):
        verify_recurrent_cycle_certificate(rule, invalid_cycle)


def test_exhaustive_small_finite_theorem_regression_matches_direct_orbit_analysis():
    # 1^1 + 2^2 + 3^3 + 4^4 = 288 labelled deterministic systems.
    total = 0
    for state_count in range(1, 5):
        for rule in exhaustive_rule_systems(state_count):
            total += 1
            classification = classify_closure(rule)
            assert classification.kind is direct_kind(rule)
            if classification.kind is ClosureKind.GLOBAL_CLOSURE:
                verify_global_closure_certificate(rule, classification.global_closure)
            elif classification.kind is ClosureKind.RECURRENT_NONCLOSURE:
                verify_recurrent_cycle_certificate(rule, classification.recurrent_cycle)
            else:
                assert len(classification.multistability.fixed_points) >= 2
    assert total == 288


def test_exhaustive_summary_is_complete_and_has_each_nontrivial_regime_by_four_states():
    summary = exhaustive_classification_summary(4)
    for state_count, counts in summary.items():
        assert sum(counts.values()) == state_count**state_count
    assert summary[4][ClosureKind.GLOBAL_CLOSURE] > 0
    assert summary[4][ClosureKind.RECURRENT_NONCLOSURE] > 0
    assert summary[4][ClosureKind.MULTISTABLE_NONCLOSURE] > 0
