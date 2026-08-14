from itertools import product

import pytest

from causal_model.dynamic_boundary_blankets import (
    DynamicInterfaceCertificate,
    FiniteControlledOutputSystem,
    certify_finite_horizon_stabilization,
)
from causal_model.feedback_type_portability import (
    EMPTY,
    OCCUPIED_NO_RECOVERY,
    OCCUPIED_RESILIENT,
    READY_FRAGILE,
    READY_RESILIENT,
    TYPE_ACTIONS,
    TYPE_MACRO_STATES,
    FeedbackTypeState,
    certify_feedback_type_portability,
    product_action_alphabet,
    product_macro_label,
    product_macro_state_count,
    product_macro_step,
    product_output,
    product_reachable_state_count,
    product_step,
    reachable_type_state_count,
    reachable_type_states,
    type_macro_distinguishing_word,
    type_macro_label,
    type_macro_output,
    type_macro_step,
    type_output,
    type_step,
)


def _same_partition(left, right):
    return all(
        (left[i] == left[j]) == (right[i] == right[j])
        for i in range(len(left))
        for j in range(len(left))
    )


def _build_single_type_system(replication):
    states = reachable_type_states(replication)
    index = {state: i for i, state in enumerate(states)}
    transition_table = tuple(
        tuple(index[type_step(state, action)] for action in TYPE_ACTIONS)
        for state in states
    )
    outputs = tuple(type_output(state) for state in states)
    return states, FiniteControlledOutputSystem(
        actions=TYPE_ACTIONS,
        transition_table=transition_table,
        outputs=outputs,
    )


def test_one_type_reachable_domain_has_closed_form_size():
    for replication in range(1, 7):
        states = reachable_type_states(replication)
        assert len(states) == reachable_type_state_count(replication)
        assert len(states) == 2 ** (replication + 2) - 2


def test_five_state_summary_is_exact_and_canonical_for_each_replication():
    for replication in range(1, 6):
        states, system = _build_single_type_system(replication)
        labels = tuple(type_macro_label(state) for state in states)
        assert set(labels) == set(TYPE_MACRO_STATES)
        assert DynamicInterfaceCertificate(system, labels).verify()
        stabilization = certify_finite_horizon_stabilization(system)
        canonical = system.horizon_labels(stabilization.stabilization_horizon)
        assert stabilization.canonical_block_count == 5
        assert _same_partition(labels, canonical)


def test_five_state_macro_transition_table_is_capacity_free():
    expected = {
        (EMPTY, "spread"): EMPTY,
        (EMPTY, "turnover"): EMPTY,
        (READY_RESILIENT, "spread"): OCCUPIED_RESILIENT,
        (READY_RESILIENT, "turnover"): READY_RESILIENT,
        (READY_FRAGILE, "spread"): OCCUPIED_NO_RECOVERY,
        (READY_FRAGILE, "turnover"): READY_FRAGILE,
        (OCCUPIED_RESILIENT, "spread"): OCCUPIED_RESILIENT,
        (OCCUPIED_RESILIENT, "turnover"): READY_RESILIENT,
        (OCCUPIED_NO_RECOVERY, "spread"): OCCUPIED_NO_RECOVERY,
        (OCCUPIED_NO_RECOVERY, "turnover"): EMPTY,
    }
    for key, target in expected.items():
        assert type_macro_step(*key) == target
    assert type_macro_output(EMPTY) == 0
    assert type_macro_output(READY_RESILIENT) == 0
    assert type_macro_output(READY_FRAGILE) == 0
    assert type_macro_output(OCCUPIED_RESILIENT) == 1
    assert type_macro_output(OCCUPIED_NO_RECOVERY) == 1


def test_five_macro_states_are_pairwise_future_distinguishable():
    for left in TYPE_MACRO_STATES:
        for right in TYPE_MACRO_STATES:
            if left == right:
                continue
            word = type_macro_distinguishing_word(left, right)
            a, b = left, right
            trace_a = [type_macro_output(a)]
            trace_b = [type_macro_output(b)]
            for action in word:
                a = type_macro_step(a, action)
                b = type_macro_step(b, action)
                trace_a.append(type_macro_output(a))
                trace_b.append(type_macro_output(b))
            assert tuple(trace_a) != tuple(trace_b)


def test_empty_mode_bit_is_exactly_redundant():
    for replication in range(1, 6):
        zero = (0,) * replication
        left = FeedbackTypeState(mode=0, facilitators=zero, targets=zero)
        right = FeedbackTypeState(mode=1, facilitators=zero, targets=zero)
        assert type_macro_label(left) == EMPTY
        assert type_macro_label(right) == EMPTY
        for word in product(TYPE_ACTIONS, repeat=4):
            l, r = left, right
            trace_l = [type_output(l)]
            trace_r = [type_output(r)]
            for action in word:
                l = type_step(l, action)
                r = type_step(r, action)
                trace_l.append(type_output(l))
                trace_r.append(type_output(r))
            assert trace_l == trace_r


def test_fixed_type_count_has_one_macro_law_across_replication_domains():
    vectors = ((1, 1), (2, 5), (7, 3), (10, 10))
    certificate = certify_feedback_type_portability(vectors)
    assert certificate.verify()
    assert certificate.type_count == 2
    assert certificate.macro_state_count == 25
    assert certificate.action_alphabet_size == 4
    assert certificate.physical_state_counts == tuple(
        product_reachable_state_count(vector) for vector in vectors
    )
    assert len(set(certificate.physical_state_counts)) == len(vectors)


def test_product_macro_transition_closes_coordinatewise():
    # Exhaust all physical states for the smallest two-type domain.
    type_states = reachable_type_states(1)
    actions = product_action_alphabet(2)
    for left in type_states:
        for right in type_states:
            state = (left, right)
            label = product_macro_label(state)
            assert product_output(state) == tuple(type_macro_output(x) for x in label)
            for action in actions:
                successor = product_step(state, action)
                assert product_macro_label(successor) == product_macro_step(label, action)


def test_product_macro_count_and_physical_growth_separate():
    assert product_macro_state_count(1) == 5
    assert product_macro_state_count(3) == 125
    small = product_reachable_state_count((1, 1, 1))
    large = product_reachable_state_count((8, 9, 10))
    assert large > small
    assert product_macro_state_count(3) == 125


def test_invalid_domains_fail_closed():
    with pytest.raises(ValueError):
        reachable_type_states(0)
    with pytest.raises(ValueError):
        certify_feedback_type_portability(())
    with pytest.raises(ValueError):
        certify_feedback_type_portability(((1, 2), (3,)))
    with pytest.raises(ValueError):
        product_action_alphabet(0)
