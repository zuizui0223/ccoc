from math import isclose

import pytest

from causal_model.anytime_symbolic_extension_stability import (
    AnytimeSymbolicExtensionTarget,
    anytime_symbolic_extension_stability_guarantee,
)
from causal_model.anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
)
from causal_model.linear_proof_verifier import (
    LinearInequality,
    RationalLinearSystem,
    RationalWitness,
)
from causal_model.rational_polyhedral_inclusion import (
    EXACT_RATIONAL_POLYHEDRAL_INCLUSION_VERIFIER,
    ExactRationalFiniteLookInclusionProof,
    ExactRationalJointInclusionProof,
    FarkasRowImplicationCertificate,
    RationalPolyhedralInclusionProof,
    RationalPolyhedralInclusionQuery,
    verify_exact_rational_finite_look_inclusion,
    verify_exact_rational_joint_inclusion,
    verify_rational_polyhedral_inclusion,
)
from causal_model.symbolic_candidate_sets import SymbolicCandidateSpace


def system(*rows, description=""):
    return RationalLinearSystem(("x",), tuple(rows), description)


def row(coefficients, bound, label=""):
    return LinearInequality(tuple(coefficients), bound, label)


def inner_interval():
    # 1/5 <= x <= 1
    return system(
        row((-1,), "-1/5", "x >= 1/5"),
        row((1,), 1, "x <= 1"),
        description="inner interval [1/5, 1]",
    )


def outer_interval():
    # 0 <= x <= 2
    return system(
        row((-1,), 0, "x >= 0"),
        row((1,), 2, "x <= 2"),
        description="outer interval [0, 2]",
    )


def valid_query(query_id="inner-in-outer"):
    return RationalPolyhedralInclusionQuery(
        query_id=query_id,
        inner_system=inner_interval(),
        outer_system=outer_interval(),
        proof=RationalPolyhedralInclusionProof(
            inner_witness=RationalWitness(("1/5",)),
            row_certificates=(
                FarkasRowImplicationCertificate(0, (1, 0)),
                FarkasRowImplicationCertificate(1, (0, 1)),
            ),
            evidence_reference=f"proof://{query_id}",
        ),
    )


def test_exact_farkas_row_proofs_verify_nonvacuous_polyhedral_inclusion():
    verified = verify_rational_polyhedral_inclusion(valid_query())

    assert verified.query_id == "inner-in-outer"
    assert verified.verifier == EXACT_RATIONAL_POLYHEDRAL_INCLUSION_VERIFIER
    assert verified.evidence_reference == "proof://inner-in-outer"


def test_invalid_inner_witness_rejects_vacuous_or_malformed_inclusion_proof():
    query = valid_query()
    invalid = RationalPolyhedralInclusionQuery(
        query_id="bad-witness",
        inner_system=query.inner_system,
        outer_system=query.outer_system,
        proof=RationalPolyhedralInclusionProof(
            inner_witness=RationalWitness((0,)),
            row_certificates=query.proof.row_certificates,
            evidence_reference="proof://bad-witness",
        ),
    )

    with pytest.raises(ValueError, match="inner nonempty witness"):
        verify_rational_polyhedral_inclusion(invalid)


def test_missing_outer_row_proof_is_rejected():
    query = valid_query()
    incomplete = RationalPolyhedralInclusionQuery(
        query_id="missing-row",
        inner_system=query.inner_system,
        outer_system=query.outer_system,
        proof=RationalPolyhedralInclusionProof(
            inner_witness=RationalWitness(("1/5",)),
            row_certificates=(FarkasRowImplicationCertificate(0, (1, 0)),),
            evidence_reference="proof://missing-row",
        ),
    )

    with pytest.raises(ValueError, match="every outer inequality"):
        verify_rational_polyhedral_inclusion(incomplete)


def test_row_certificate_rejects_wrong_coefficients_or_weaker_bound():
    query = valid_query()
    wrong_coefficients = RationalPolyhedralInclusionQuery(
        query_id="wrong-coefficients",
        inner_system=query.inner_system,
        outer_system=query.outer_system,
        proof=RationalPolyhedralInclusionProof(
            inner_witness=RationalWitness(("1/5",)),
            row_certificates=(
                FarkasRowImplicationCertificate(0, (0, 1)),
                FarkasRowImplicationCertificate(1, (0, 1)),
            ),
            evidence_reference="proof://wrong-coefficients",
        ),
    )
    with pytest.raises(ValueError, match="coefficients"):
        verify_rational_polyhedral_inclusion(wrong_coefficients)

    too_small_outer = system(row((1,), "1/2", "x <= 1/2"), description="outer x <= 1/2")
    weak_bound = RationalPolyhedralInclusionQuery(
        query_id="weak-bound",
        inner_system=inner_interval(),
        outer_system=too_small_outer,
        proof=RationalPolyhedralInclusionProof(
            inner_witness=RationalWitness(("1/5",)),
            row_certificates=(FarkasRowImplicationCertificate(0, (0, 1)),),
            evidence_reference="proof://weak-bound",
        ),
    )
    with pytest.raises(ValueError, match="weaker bound"):
        verify_rational_polyhedral_inclusion(weak_bound)


def test_static_bundle_builds_gamma_zero_joint_inclusion_certificate():
    certificate = verify_exact_rational_joint_inclusion(
        ExactRationalJointInclusionProof(
            inner_tier_id="inner",
            outer_tier_id="outer",
            queries_by_cell={"primary": valid_query()},
        ),
        required_cell_ids=("primary",),
    )

    assert certificate.lower_bound == 1.0
    assert certificate.inclusion_failure_upper_bound == 0.0
    assert certificate.method == EXACT_RATIONAL_POLYHEDRAL_INCLUSION_VERIFIER


def test_finite_look_bundle_builds_gamma_zero_anytime_certificate():
    certificate = verify_exact_rational_finite_look_inclusion(
        ExactRationalFiniteLookInclusionProof(
            inner_tier_id="inner",
            outer_tier_id="outer",
            queries_by_look={
                1: {"primary": valid_query("look-1")},
                2: {"primary": valid_query("look-2")},
            },
        ),
        required_cell_ids=("primary",),
    )

    assert certificate.lower_bound == 1.0
    assert certificate.certified_looks == (1, 2)
    assert certificate.inclusion_failure_upper_bound == 0.0


def test_finite_proof_bundle_cannot_claim_all_positive_integer_looks():
    with pytest.raises(ValueError, match="sorted increasingly"):
        verify_exact_rational_finite_look_inclusion(
            ExactRationalFiniteLookInclusionProof(
                inner_tier_id="inner",
                outer_tier_id="outer",
                queries_by_look={
                    2: {"primary": valid_query("look-2")},
                    1: {"primary": valid_query("look-1")},
                },
            ),
            required_cell_ids=("primary",),
        )


def test_exact_polyhedral_inclusion_recovers_alpha_plus_beta_for_anytime_stability():
    inclusion = verify_exact_rational_finite_look_inclusion(
        ExactRationalFiniteLookInclusionProof(
            inner_tier_id="inner",
            outer_tier_id="outer",
            queries_by_look={
                1: {"primary": valid_query("look-1")},
                2: {"primary": valid_query("look-2")},
            },
        ),
        required_cell_ids=("primary",),
    )
    guarantee = anytime_symbolic_extension_stability_guarantee(
        target=AnytimeSymbolicExtensionTarget(
            inner_tier_id="inner",
            outer_tier_id="outer",
            space=SymbolicCandidateSpace("polyhedral candidate space", ("focal",)),
            required_cell_ids=("primary",),
        ),
        coverage_certificate=AnytimeSymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("primary",),
            lower_bound=0.95,
            method="external finite-look coverage",
            certified_looks=(1, 2),
        ),
        solver_certificate=AnytimeSolverSemanticValidityCertificate(
            required_cell_ids=("primary",),
            motifs=("focal",),
            lower_bound=1.0,
            method="proof-carrying outer solver verifier",
            certified_looks=(1, 2),
        ),
        inclusion_certificate=inclusion,
    )

    assert isclose(guarantee.inclusion_failure_upper_bound, 0.0)
    assert isclose(guarantee.time_uniform_false_decisive_or_invalid_stability_upper_bound, 0.05)
