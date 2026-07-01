import math

import pytest

from causal_model.candidate_safe_laws import (
    CandidateInducedLaw,
    CandidateLawFamily,
    binary_agreement_family,
    binary_identity_flip_family,
    certify_candidate_safe_product,
    certify_delayed_candidate_discrimination,
    certify_set_valued_macro_law,
    certify_universal_macro_law,
    find_candidate_response_separator,
    universal_law_obstruction_certificate,
)


def test_small_instance_laws_need_not_share_a_universal_deterministic_law():
    family = binary_identity_flip_family()
    assert family.macrostate_count == 2
    assert family.candidate_count == 2
    assert family.response_type_count == 2
    assert not family.has_universal_deterministic_law

    obstruction = universal_law_obstruction_certificate(family)
    assert obstruction.verify()
    assert obstruction.action == "intervene"
    assert obstruction.left_successor != obstruction.right_successor


def test_candidate_safe_product_retains_macrostate_and_response_type():
    family = binary_identity_flip_family()
    certificate = certify_candidate_safe_product(family)
    assert certificate.verify()
    assert certificate.macrostate_count == 2
    assert certificate.response_type_count == 2
    assert certificate.candidate_safe_block_count == 4
    assert certificate.instance_interface_bits == 1.0
    assert certificate.candidate_safe_interface_bits == 2.0
    assert certificate.response_type_inflation_bits == 1.0
    assert certificate.product_lower_bound_bits == 2.0
    assert certificate.checked_type_state_separators == 2


def test_each_response_type_pair_has_concrete_separating_words_at_every_macrostate():
    family = binary_identity_flip_family()
    for macrostate in family.macrostates:
        certificate = find_candidate_response_separator(family, 0, 1, macrostate)
        assert certificate is not None
        assert certificate.verify()
        assert certificate.word == ("intervene",)
        assert certificate.left_trace != certificate.right_trace


def test_duplicate_candidates_collapse_to_one_response_type_and_yield_a_universal_law():
    family = binary_agreement_family()
    assert family.candidate_count == 2
    assert family.response_type_count == 1
    assert family.has_universal_deterministic_law

    universal = certify_universal_macro_law(family)
    assert universal.verify()
    assert universal.universal_transition_table == ((0, 0), (1, 1))

    product = certify_candidate_safe_product(family)
    assert product.verify()
    assert product.candidate_safe_block_count == 2
    assert product.response_type_inflation_bits == 0.0


def test_set_valued_law_is_the_exact_candidate_forgetting_prediction():
    family = binary_identity_flip_family()
    certificate = certify_set_valued_macro_law(family)
    assert certificate.verify()
    assert not certificate.is_deterministic
    assert certificate.successor_sets[0] == (frozenset({0}), frozenset({0, 1}))
    assert certificate.successor_sets[1] == (frozenset({1}), frozenset({0, 1}))

    agreeing = certify_set_valued_macro_law(binary_agreement_family())
    assert agreeing.verify()
    assert agreeing.is_deterministic


def test_delayed_candidate_types_are_indistinguishable_until_the_legal_revealing_word():
    certificate = certify_delayed_candidate_discrimination(delay=5)
    assert certificate.verify()
    assert certificate.shared_horizon == 5
    assert certificate.revealing_horizon == 6
    assert certificate.revealing_word == ("wait", "wait", "wait", "wait", "wait", "fire")
    assert certificate.left_trace == (0, 0, 0, 0, 0, 0, 0)
    assert certificate.right_trace == (0, 0, 0, 0, 0, 0, 1)


def test_response_type_is_mechanistic_response_not_candidate_name():
    identity = binary_agreement_family().candidates[0]
    duplicate = CandidateInducedLaw(
        candidate_id="same-dynamics-new-name",
        actions=identity.actions,
        transition_table=identity.transition_table,
        macro_outputs=identity.macro_outputs,
    )
    family = CandidateLawFamily((identity, duplicate))
    assert family.candidate_count == 2
    assert family.response_type_count == 1


@pytest.mark.parametrize(
    "bad_law",
    [
        lambda: CandidateInducedLaw("", ("a",), ((0,),), (0,)),
        lambda: CandidateInducedLaw("x", ("a", "a"), ((0, 0),), (0,)),
        lambda: CandidateInducedLaw("x", ("a",), ((1,),), (0,)),
        lambda: CandidateInducedLaw("x", ("a",), ((0,),), (0, 0)),
    ],
)
def test_invalid_candidate_laws_fail_closed(bad_law):
    with pytest.raises(ValueError):
        bad_law()


def test_incompatible_shared_macrospace_fails_closed():
    left = CandidateInducedLaw("left", ("a",), ((0,),), (0,))
    right = CandidateInducedLaw("right", ("a",), ((0,), (0,)), (0, 1))
    with pytest.raises(ValueError, match="macrostate space"):
        CandidateLawFamily((left, right))


@pytest.mark.parametrize("bad_delay", [-1, True, 1.5, "4"])
def test_invalid_delayed_candidate_horizon_fails_closed(bad_delay):
    with pytest.raises(ValueError):
        certify_delayed_candidate_discrimination(bad_delay)
