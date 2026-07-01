import math

import pytest

from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.joint_open_candidate_laws import (
    INTERVENE,
    OBSERVE,
    READ,
    LOCAL_ACTIONS,
    JointOpenCandidateProduct,
    OpenLawCandidate,
    OpenLawFamily,
    OpenLawReportKind,
    StructuralQuery,
    agreeing_open_law_family,
    certify_candidate_safe_open_law,
    certify_joint_exterior_mechanism_product,
    certify_set_valued_open_law,
    certify_universal_open_law,
    classify_open_law_family,
    conflicting_open_law_family,
    joint_open_law_obstruction_certificate,
    joint_structural_separator_certificate,
    universal_open_law_obstruction_certificate,
)


def test_common_dynamic_interfaces_with_same_induced_map_give_a_universal_open_law():
    family = agreeing_open_law_family()
    assert family.verify_candidate_interfaces()
    assert family.response_type_count == 1
    assert family.has_universal_open_law

    certificate = certify_universal_open_law(family)
    assert certificate.verify()
    assert certificate.universal_transition_table == ((1,), (0,))

    verdict = classify_open_law_family(family, retain_response_type=False)
    assert verdict.verify()
    assert verdict.kind is OpenLawReportKind.UNIVERSAL_DETERMINISTIC


def test_dynamic_blankets_without_common_maps_do_not_give_a_universal_open_law():
    family = conflicting_open_law_family()
    assert family.verify_candidate_interfaces()
    assert family.response_type_count == 2
    assert not family.has_universal_open_law

    obstruction = universal_open_law_obstruction_certificate(family)
    assert obstruction.verify()
    assert obstruction.action == "step"
    assert obstruction.left_successor != obstruction.right_successor


def test_typed_trichotomy_distinguishes_candidate_safe_and_set_valued_outputs():
    family = conflicting_open_law_family()

    candidate_safe = classify_open_law_family(family, retain_response_type=True)
    assert candidate_safe.verify()
    assert candidate_safe.kind is OpenLawReportKind.CANDIDATE_SAFE_DETERMINISTIC

    candidate_safe_construction = certify_candidate_safe_open_law(family)
    assert candidate_safe_construction.verify()
    assert candidate_safe_construction.candidate_safe_state_count == 4
    assert candidate_safe_construction.explicit_response_type_bits == 1.0

    set_valued = classify_open_law_family(family, retain_response_type=False)
    assert set_valued.verify()
    assert set_valued.kind is OpenLawReportKind.SET_VALUED

    relation = certify_set_valued_open_law(family)
    assert relation.verify()
    assert not relation.is_deterministic
    assert relation.successor_sets == ((frozenset({0, 1}),), (frozenset({0, 1}),))


def test_joint_product_uses_constant_local_actions_and_structural_ports():
    family = JointOpenCandidateProduct(
        inside_cardinality=3,
        exterior_cardinalities=(2, 3),
        response_type_count=2,
    )
    assert family.local_actions == LOCAL_ACTIONS == (OBSERVE, READ, INTERVENE)
    assert family.ports == (0, 1)
    assert all(query.action in LOCAL_ACTIONS for query in family.structural_queries)
    assert all(":" not in query.action for query in family.structural_queries)

    state = (1, 0, 2, 1)
    assert family.trace(state, StructuralQuery(1, READ)) == (1, 2)
    assert family.trace(state, StructuralQuery(0, INTERVENE)) == (1, 2)


def test_joint_product_has_exact_additive_exterior_and_response_type_bound():
    certificate = certify_joint_exterior_mechanism_product(
        inside_cardinality=3,
        exterior_cardinalities=(2, 3),
        response_type_count=2,
    )
    assert certificate.verify()
    assert certificate.candidate_macrostate_count == 18
    assert certificate.fixed_candidate_block_counts == (18, 18)
    assert certificate.joint_state_count == 36
    assert certificate.joint_block_count == 36
    assert certificate.response_type_inflation_bits == 1.0
    assert certificate.joint_safe_interface_bits == math.log2(36)
    assert certificate.joint_product_lower_bound_bits == math.log2(36)


def test_every_joint_state_pair_has_a_concrete_structural_separator():
    family = JointOpenCandidateProduct(
        inside_cardinality=3,
        exterior_cardinalities=(2, 3),
        response_type_count=2,
    )
    inside_change = joint_structural_separator_certificate(family, (0, 0, 0, 0), (1, 0, 0, 0))
    assert inside_change.verify()
    assert inside_change.query == StructuralQuery(0, OBSERVE)

    exterior_change = joint_structural_separator_certificate(family, (0, 0, 0, 0), (0, 0, 1, 0))
    assert exterior_change.verify()
    assert exterior_change.query == StructuralQuery(1, READ)

    mechanism_change = joint_structural_separator_certificate(family, (0, 0, 0, 0), (0, 0, 0, 1))
    assert mechanism_change.verify()
    assert mechanism_change.query == StructuralQuery(0, INTERVENE)
    assert mechanism_change.left_trace != mechanism_change.right_trace


def test_joint_witness_exhibits_a_macro_transition_obstruction_when_response_types_differ():
    family = JointOpenCandidateProduct(
        inside_cardinality=3,
        exterior_cardinalities=(2,),
        response_type_count=2,
    )
    obstruction = joint_open_law_obstruction_certificate(family)
    assert obstruction.verify()
    assert obstruction.query == StructuralQuery(0, INTERVENE)
    assert obstruction.left_successor != obstruction.right_successor


def test_one_response_type_recovers_a_universal_open_law_in_the_joint_family():
    certificate = certify_joint_exterior_mechanism_product(
        inside_cardinality=2,
        exterior_cardinalities=(2,),
        response_type_count=1,
    )
    assert certificate.verify()
    assert certificate.response_type_inflation_bits == 0.0
    assert certificate.product_family.has_universal_open_law


def test_invalid_common_interface_is_rejected_before_any_universal_claim():
    invalid = OpenLawCandidate(
        candidate_id="not-update-closed",
        system=FiniteControlledOutputSystem(
            actions=("step",),
            transition_table=((0,), (2,), (2,)),
            outputs=(0, 0, 1),
        ),
        macro_labels=(0, 0, 1),
        macro_outputs=(0, 1),
    )
    family = OpenLawFamily((invalid,))
    assert not family.verify_candidate_interfaces()
    with pytest.raises(ValueError, match="dynamic interfaces"):
        classify_open_law_family(family, retain_response_type=True)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"inside_cardinality": 1, "exterior_cardinalities": (2,), "response_type_count": 1},
        {"inside_cardinality": 2, "exterior_cardinalities": (), "response_type_count": 1},
        {"inside_cardinality": 2, "exterior_cardinalities": (1,), "response_type_count": 1},
        {"inside_cardinality": 2, "exterior_cardinalities": (3,), "response_type_count": 1},
        {"inside_cardinality": 2, "exterior_cardinalities": (2,), "response_type_count": 3},
    ],
)
def test_joint_product_cardinality_conditions_fail_closed(kwargs):
    with pytest.raises(ValueError):
        JointOpenCandidateProduct(**kwargs)


def test_invalid_structural_query_fails_closed():
    family = JointOpenCandidateProduct(inside_cardinality=2, exterior_cardinalities=(2,), response_type_count=2)
    with pytest.raises(ValueError):
        family.successor((0, 0, 0), StructuralQuery(1, READ))
    with pytest.raises(ValueError):
        family.successor((0, 0, 0), StructuralQuery(0, "read:0"))
