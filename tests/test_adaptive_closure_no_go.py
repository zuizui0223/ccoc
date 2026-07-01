import pytest

from causal_model.adaptive_closure_no_go import (
    ACTIONS,
    BIT0,
    BIT1,
    FIRE,
    TICK,
    FiniteAdaptivePolicy,
    address_bits_exceeding_upper_bound,
    certify_adaptive_closure_no_go,
    certify_canonical_blanket_cardinality,
    certify_policy_lifting,
    certify_transcript_upper_bound_refutation,
    closed_open_delayed_pair,
    exhaustive_adaptive_no_go_summary,
)


def test_policy_table_is_a_real_adaptive_decision_tree():
    policy = FiniteAdaptivePolicy.from_rule(
        3,
        lambda history: BIT1 if history[-1] else FIRE,
    )
    assert policy.verify()
    assert policy.action_for((0,)) == FIRE
    assert policy.action_for((1,)) == BIT1
    assert policy.action_for((0, 1, 0)) == FIRE
    assert policy.action_for((1, 0, 1)) == BIT1


def test_policy_lifting_holds_for_every_action_history_before_the_delay_gate():
    policy = FiniteAdaptivePolicy.from_rule(
        3,
        lambda history: BIT0 if sum(history) % 2 == 0 else BIT1,
    )
    closed, open_system = closed_open_delayed_pair(delay=4, address_bits=2)
    certificate = certify_policy_lifting(policy, closed, open_system, common_prefix_depth=3)
    assert certificate.verify()
    assert certificate.left_transcript == certificate.right_transcript
    assert certificate.left_transcript.outputs == (0, 0, 0, 0)
    assert all(action in ACTIONS for action in certificate.left_transcript.actions)


@pytest.mark.parametrize("depth,address_bits", [(0, 0), (1, 0), (2, 1), (3, 2)])
def test_adaptive_no_go_has_same_finite_policy_transcript_but_different_closure(depth, address_bits):
    policy = FiniteAdaptivePolicy.from_rule(
        depth,
        lambda history: FIRE if history[-1] == 0 else BIT1,
    )
    certificate = certify_adaptive_closure_no_go(policy, address_bits)
    assert certificate.verify()
    assert certificate.delay == depth + 1
    assert certificate.policy_lifting.left_transcript == certificate.policy_lifting.right_transcript
    assert certificate.closed_blanket.claimed_blanket_count == 1
    assert certificate.open_blanket.claimed_blanket_count == 2 ** (2**address_bits)
    assert len(certificate.future_separator_word) > depth
    assert certificate.closed_system.trace(certificate.future_separator_word) != certificate.open_system.trace(
        certificate.future_separator_word
    )


def test_constant_action_alphabet_does_not_grow_with_addressable_exterior_dimension():
    closed, open_system = closed_open_delayed_pair(delay=2, address_bits=3)
    assert closed.verify() and open_system.verify()
    assert set(ACTIONS) == {TICK, BIT0, BIT1, FIRE}
    assert open_system.exterior_coordinate_count == 8
    assert open_system.canonical_blanket_count == 2**8
    for coordinate in range(open_system.exterior_coordinate_count):
        word = open_system.read_word(coordinate)
        assert set(word).issubset(set(ACTIONS))
        assert len(word) == 2 + 3 + 1


def test_closed_and_open_canonical_blanket_certificates_have_exact_cardinalities():
    closed, open_system = closed_open_delayed_pair(delay=1, address_bits=2)
    closed_certificate = certify_canonical_blanket_cardinality(closed)
    open_certificate = certify_canonical_blanket_cardinality(open_system)
    assert closed_certificate.verify()
    assert open_certificate.verify()
    assert closed_certificate.claimed_blanket_count == 1
    assert open_certificate.claimed_blanket_count == 16
    assert open_certificate.all_exterior_states_separated


def test_future_read_at_structurally_encoded_port_zero_separates_closed_and_open():
    policy = FiniteAdaptivePolicy.constant(depth=2, action=TICK)
    certificate = certify_adaptive_closure_no_go(policy, address_bits=1)
    word = certificate.future_separator_word
    assert word == (TICK, TICK, TICK, BIT0, FIRE)
    assert certificate.closed_system.trace(word)[-1] == 0
    assert certificate.open_system.trace(word)[-1] == 1


@pytest.mark.parametrize("upper_bound", [1, 2, 15, 16, 255])
def test_any_proposed_finite_blanket_upper_bound_has_a_same_transcript_delayed_refutation(upper_bound):
    policy = FiniteAdaptivePolicy.from_rule(2, lambda history: TICK if history[-1] == 0 else FIRE)
    certificate = certify_transcript_upper_bound_refutation(policy, upper_bound)
    assert certificate.verify()
    assert certificate.no_go.open_blanket_count > upper_bound
    assert certificate.no_go.policy_lifting.left_transcript == certificate.no_go.policy_lifting.right_transcript
    assert 2 ** (2 ** address_bits_exceeding_upper_bound(upper_bound)) > upper_bound


def test_no_go_is_not_an_infinite_state_artifact_each_witness_is_finite():
    policy = FiniteAdaptivePolicy.constant(depth=4, action=FIRE)
    certificate = certify_adaptive_closure_no_go(policy, address_bits=2)
    assert certificate.verify()
    assert certificate.open_system.exterior_coordinate_count == 4
    assert certificate.open_blanket.claimed_blanket_count == 16
    assert certificate.delay == 5


def test_exhaustive_small_certificate_replay():
    certificates = exhaustive_adaptive_no_go_summary(max_policy_depth=3, max_address_bits=2)
    assert len(certificates) == (3 + 1) * 2 * (2 + 1)
    assert all(certificate.verify() for certificate in certificates)


def test_invalid_policies_and_bounds_fail_closed():
    with pytest.raises(ValueError, match="canonical total"):
        FiniteAdaptivePolicy(depth=1, actions_by_history=(((0,), TICK),))
    with pytest.raises(ValueError, match="fixed alphabet"):
        FiniteAdaptivePolicy.from_rule(1, lambda _history: "probe:0")
    with pytest.raises(ValueError, match="positive"):
        address_bits_exceeding_upper_bound(0)
