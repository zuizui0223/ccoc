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
from causal_model.online_polyhedral_inclusion_schema import (
    EXACT_MONOTONE_POLYHEDRAL_INCLUSION_SCHEMA_VERIFIER,
    MonotonePolyhedralInclusionLook,
    MonotonePolyhedralInclusionSchema,
    verify_monotone_polyhedral_inclusion_look,
    verify_monotone_polyhedral_inclusion_schema,
)
from causal_model.rational_polyhedral_inclusion import (
    FarkasRowImplicationCertificate,
    RationalPolyhedralInclusionProof,
    RationalPolyhedralInclusionQuery,
)
from causal_model.symbolic_candidate_sets import SymbolicCandidateSpace


def row(coefficients, bound, label=""):
    return LinearInequality(tuple(coefficients), bound, label)


def system(*rows, description=""):
    return RationalLinearSystem(("x",), tuple(rows), description)


def base_inner():
    return system(
        row((-1,), "-1/5", "x >= 1/5"),
        row((1,), 1, "x <= 1"),
        description="base inner",
    )


def fixed_outer():
    return system(
        row((-1,), 0, "x >= 0"),
        row((1,), 2, "x <= 2"),
        description="fixed outer",
    )


def base_query():
    return RationalPolyhedralInclusionQuery(
        query_id="base-in-outer",
        inner_system=base_inner(),
        outer_system=fixed_outer(),
        proof=RationalPolyhedralInclusionProof(
            inner_witness=RationalWitness(("1/5",)),
            row_certificates=(
                FarkasRowImplicationCertificate(0, (1, 0)),
                FarkasRowImplicationCertificate(1, (0, 1)),
            ),
            evidence_reference="proof://base-in-outer",
        ),
    )


def verified_schema():
    return verify_monotone_polyhedral_inclusion_schema(
        MonotonePolyhedralInclusionSchema(
            inner_tier_id="inner",
            outer_tier_id="outer",
            base_queries_by_cell={"primary": base_query()},
        ),
        required_cell_ids=("primary",),
    )


def strengthened_inner():
    return system(
        row((-1,), "-1/5", "renamed lower row"),
        row((1,), 1, "renamed upper row"),
        row((1,), "3/4", "new accumulated constraint"),
        description="later inner",
    )


def admitted_look(look=1):
    return MonotonePolyhedralInclusionLook(
        look=look,
        inner_systems_by_cell={"primary": strengthened_inner()},
        outer_systems_by_cell={"primary": fixed_outer()},
        inner_witnesses_by_cell={"primary": RationalWitness(("1/5",))},
        evidence_reference=f"proof://look-{look}-admission",
    )


def test_verified_schema_yields_all_look_gamma_zero_certificate():
    schema = verified_schema()

    certificate = schema.all_look_inclusion_certificate
    assert certificate.lower_bound == 1.0
    assert certificate.inclusion_failure_upper_bound == 0.0
    assert certificate.certified_looks is None
    assert certificate.method == EXACT_MONOTONE_POLYHEDRAL_INCLUSION_SCHEMA_VERIFIER


def test_admits_arbitrarily_late_strengthened_look_with_nonvacuous_witness():
    schema = verified_schema()
    first = verify_monotone_polyhedral_inclusion_look(schema, admitted_look(1))
    later = verify_monotone_polyhedral_inclusion_look(schema, admitted_look(10000))

    assert first.look == 1
    assert later.look == 10000
    assert later.verifier == EXACT_MONOTONE_POLYHEDRAL_INCLUSION_SCHEMA_VERIFIER


def test_rejects_current_inner_that_omits_a_base_constraint():
    schema = verified_schema()
    weakened = MonotonePolyhedralInclusionLook(
        look=1,
        inner_systems_by_cell={"primary": system(row((1,), "3/4", "only later row"))},
        outer_systems_by_cell={"primary": fixed_outer()},
        inner_witnesses_by_cell={"primary": RationalWitness((0,))},
        evidence_reference="proof://weakened",
    )

    with pytest.raises(ValueError, match="retain every base inequality"):
        verify_monotone_polyhedral_inclusion_look(schema, weakened)


def test_rejects_changed_outer_or_invalid_current_inner_witness():
    schema = verified_schema()
    changed_outer = MonotonePolyhedralInclusionLook(
        look=1,
        inner_systems_by_cell={"primary": strengthened_inner()},
        outer_systems_by_cell={
            "primary": system(
                row((-1,), 0, "x >= 0"),
                row((1,), 3, "x <= 3"),
            )
        },
        inner_witnesses_by_cell={"primary": RationalWitness(("1/5",))},
        evidence_reference="proof://changed-outer",
    )
    with pytest.raises(ValueError, match="fixed outer"):
        verify_monotone_polyhedral_inclusion_look(schema, changed_outer)

    invalid_witness = MonotonePolyhedralInclusionLook(
        look=1,
        inner_systems_by_cell={"primary": strengthened_inner()},
        outer_systems_by_cell={"primary": fixed_outer()},
        inner_witnesses_by_cell={"primary": RationalWitness((0,))},
        evidence_reference="proof://invalid-witness",
    )
    with pytest.raises(ValueError, match="inner witness"):
        verify_monotone_polyhedral_inclusion_look(schema, invalid_witness)


def test_all_look_schema_recovers_alpha_when_outer_solver_is_proof_carrying():
    schema = verified_schema()
    guarantee = anytime_symbolic_extension_stability_guarantee(
        target=AnytimeSymbolicExtensionTarget(
            inner_tier_id="inner",
            outer_tier_id="outer",
            space=SymbolicCandidateSpace("online polyhedral space", ("focal",)),
            required_cell_ids=("primary",),
        ),
        coverage_certificate=AnytimeSymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("primary",),
            lower_bound=0.95,
            method="external all-look confidence sequence",
        ),
        solver_certificate=AnytimeSolverSemanticValidityCertificate(
            required_cell_ids=("primary",),
            motifs=("focal",),
            lower_bound=1.0,
            method="proof-carrying outer solver verifier",
        ),
        inclusion_certificate=schema.all_look_inclusion_certificate,
    )

    assert guarantee.certified_looks is None
    assert isclose(guarantee.inclusion_failure_upper_bound, 0.0)
    assert isclose(guarantee.time_uniform_false_decisive_or_invalid_stability_upper_bound, 0.05)
