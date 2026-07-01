import math

import pytest

from causal_model.delayed_joint_nonidentifiability import (
    INTERVENE,
    READ,
    WAIT,
    DelayedJointAction,
    DelayedJointFamily,
    DelayedJointGrammar,
    DelayedJointSeparatorCertificate,
    certify_delayed_joint_no_uniform_horizon,
    certify_delayed_joint_quotient_jump,
    exhaustive_delayed_joint_summary,
)


def test_delayed_joint_grammar_uses_fixed_action_kinds_and_structural_read_contexts():
    grammar = DelayedJointGrammar(delay=3, exterior_port_count=2)
    assert grammar.verify()
    assert grammar.legal_actions(0) == (DelayedJointAction.wait(),)
    assert grammar.legal_actions(2) == (DelayedJointAction.wait(),)
    assert grammar.legal_actions(3) == (
        DelayedJointAction.read(0),
        DelayedJointAction.read(1),
        DelayedJointAction.intervene(),
    )
    assert grammar.legal_actions(grammar.terminal_state) == ()
    assert tuple(action.kind for action in grammar.legal_actions(3)) == (READ, READ, INTERVENE)
    assert grammar.revealing_read_word(1) == (
        DelayedJointAction.wait(),
        DelayedJointAction.wait(),
        DelayedJointAction.wait(),
        DelayedJointAction.read(1),
    )
    assert grammar.revealing_intervene_word[-1].kind == INTERVENE


def test_all_early_legal_words_are_wait_prefixes_and_see_only_inside_output():
    family = DelayedJointFamily(exterior_port_count=3, delay=4)
    early_words = family.grammar.legal_words_through(family.early_horizon)
    assert early_words == tuple((DelayedJointAction.wait(),) * length for length in range(5))

    left = (0, 0, 0, 0, 0)
    right = (0, 1, 1, 1, 1)
    assert family.horizon_signature(left, 4) == family.horizon_signature(right, 4)
    assert family.horizon_signature(left, 4) == tuple(
        (word, (0,) * (len(word) + 1)) for word in early_words
    )


def test_delayed_joint_quotient_jump_is_exact_at_the_first_revealing_horizon():
    certificate = certify_delayed_joint_quotient_jump(exterior_port_count=3, delay=2)
    assert certificate.verify()
    assert certificate.early_block_count == 2
    assert certificate.full_block_count == 2**5
    assert certificate.first_revealing_horizon == 3
    assert certificate.family.early_interface_bits == 1.0
    assert certificate.family.full_interface_bits == 5.0
    assert len(certificate.family.horizon_partition(2)) == 2
    assert len(certificate.family.horizon_partition(3)) == 2**5


@pytest.mark.parametrize("delay", [0, 1, 2, 5])
def test_first_joint_separating_horizon_is_delay_plus_one(delay):
    certificate = certify_delayed_joint_quotient_jump(exterior_port_count=2, delay=delay)
    assert certificate.first_revealing_horizon == delay + 1
    assert certificate.early_block_count == 2
    assert certificate.full_block_count == 16


def test_exterior_and_response_have_distinct_concrete_delayed_separators():
    family = DelayedJointFamily(exterior_port_count=2, delay=3)
    left = (0, 0, 0, 0)
    exterior_right = (0, 0, 1, 0)
    response_right = (0, 0, 0, 1)

    exterior = family.separator_for_pair(left, exterior_right)
    response = family.separator_for_pair(left, response_right)
    assert exterior.verify() and response.verify()
    assert exterior.reason == "exterior"
    assert response.reason == "response"
    assert exterior.word == family.grammar.revealing_read_word(1)
    assert response.word == family.grammar.revealing_intervene_word
    assert exterior.left_trace[-1] == 0
    assert exterior.right_trace[-1] == 1
    assert response.left_trace[-1] == 0
    assert response.right_trace[-1] == 1


def test_one_joint_pair_can_be_early_indistinguishable_then_separated_by_both_late_queries():
    family = DelayedJointFamily(exterior_port_count=2, delay=2)
    left = (0, 0, 0, 0)
    right = (0, 1, 0, 1)
    exterior = DelayedJointSeparatorCertificate(
        family, left, right, "exterior", family.grammar.revealing_read_word(0)
    )
    response = DelayedJointSeparatorCertificate(
        family, left, right, "response", family.grammar.revealing_intervene_word
    )
    assert family.horizon_signature(left, 2) == family.horizon_signature(right, 2)
    assert exterior.verify() and response.verify()
    assert exterior.left_trace != exterior.right_trace
    assert response.left_trace != response.right_trace


@pytest.mark.parametrize("proposed_horizon", [0, 1, 3, 7])
def test_no_uniform_joint_horizon_certificate_uses_a_later_exterior_and_response_separator(proposed_horizon):
    certificate = certify_delayed_joint_no_uniform_horizon(
        exterior_port_count=2,
        proposed_horizon=proposed_horizon,
    )
    assert certificate.verify()
    assert certificate.family.delay == proposed_horizon
    assert certificate.family.horizon_signature(certificate.left, proposed_horizon) == certificate.family.horizon_signature(
        certificate.right, proposed_horizon
    )
    assert len(certificate.exterior_separator.word) == proposed_horizon + 1
    assert len(certificate.response_separator.word) == proposed_horizon + 1


def test_full_delayed_joint_quotient_has_the_expected_additive_binary_memory():
    family = DelayedJointFamily(exterior_port_count=4, delay=1)
    certificate = certify_delayed_joint_quotient_jump(4, 1)
    assert certificate.full_block_count == family.state_count == 2**6
    assert math.log2(certificate.full_block_count) == family.full_interface_bits == 6.0


def test_exhaustive_small_delayed_joint_family_replay():
    certificates = exhaustive_delayed_joint_summary(max_exterior_port_count=3, max_delay=3)
    assert len(certificates) == 12
    assert all(certificate.verify() for certificate in certificates)


@pytest.mark.parametrize(
    "action",
    [
        DelayedJointAction(WAIT, 0),
        DelayedJointAction(READ),
        DelayedJointAction(READ, -1),
        DelayedJointAction(INTERVENE, 0),
        DelayedJointAction("unknown"),
    ],
)
def test_invalid_actions_fail_closed(action):
    with pytest.raises(ValueError):
        action.validate(2)


def test_illegal_words_and_invalid_states_fail_closed():
    family = DelayedJointFamily(exterior_port_count=1, delay=1)
    with pytest.raises(ValueError, match="illegal"):
        family.trace((0, 0, 0), (DelayedJointAction.read(0),))
    with pytest.raises(ValueError):
        family.trace((0, 2, 0), ())
    with pytest.raises(ValueError):
        family.grammar.revealing_read_word(2)
