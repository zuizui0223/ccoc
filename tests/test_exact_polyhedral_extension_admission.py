from math import isclose

import pytest

from causal_model.anytime_symbolic_extension_stability import (
    anytime_symbolic_extension_stability_guarantee,
    audit_anytime_symbolic_universe_extension,
)
from causal_model.anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from causal_model.exact_polyhedral_extension_admission import (
    EXACT_POLYHEDRAL_EXTENSION_ADMISSION_VERIFIER,
    ExactLinearProofCell,
    ExactPolyhedralExtensionAdmissionSchema,
    ExactPolyhedralExtensionLook,
    admit_exact_polyhedral_extension_look,
    verify_exact_polyhedral_extension_admission_schema,
)
from causal_model.linear_proof_verifier import (
    FarkasInfeasibilityCertificate,
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    LinearMotifQueryBundle,
    RationalLinearSystem,
    RationalWitness,
)
from causal_model.online_polyhedral_inclusion_schema import MonotonePolyhedralInclusionSchema
from causal_model.rational_polyhedral_inclusion import (
    FarkasRowImplicationCertificate,
    RationalPolyhedralInclusionProof,
    RationalPolyhedralInclusionQuery,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace
from causal_model.symbolic_universe_extension import ExtensionStatus


SPACE = SymbolicCandidateSpace("exact online polyhedral candidate space", ("focal",))


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


def later_inner():
    return system(
        row((-1,), "-1/5", "x >= 1/5"),
        row((1,), 1, "x <= 1"),
        row((1,), "3/4", "x <= 3/4"),
        description="later inner",
    )


def sat_query(query_id, linear_system, witness="1/5"):
    return LinearFeasibilityQuery(
        query_id=query_id,
        system=linear_system,
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.SAT,
            witness=RationalWitness((witness,)),
            evidence_reference=f"proof://{query_id}",
        ),
    )


def unsat_query(query_id, linear_system, multipliers):
    return LinearFeasibilityQuery(
        query_id=query_id,
        system=linear_system,
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.UNSAT,
            farkas=FarkasInfeasibilityCertificate(tuple(multipliers)),
            evidence_reference=f"proof://{query_id}",
        ),
    )


def invariant_bundle(prefix, retained, *, inner):
    if inner:
        inactive = system(
            *retained.inequalities,
            row((1,), 0, "x <= 0"),
            description=f"{prefix} inactive",
        )
        inactive_multipliers = (1, 0, 0, 1)
        witness = "1/5"
    else:
        inactive = system(
            *retained.inequalities,
            row((1,), -1, "x <= -1"),
            description=f"{prefix} inactive",
        )
        inactive_multipliers = (1, 0, 1)
        witness = 0
    return LinearMotifQueryBundle(
        nonempty=sat_query(f"{prefix}/nonempty", retained, witness),
        active=sat_query(f"{prefix}/active", retained, witness),
        inactive=unsat_query(f"{prefix}/inactive", inactive, inactive_multipliers),
    )


def nondecisive_bundle(prefix, retained, witness):
    return LinearMotifQueryBundle(
        nonempty=sat_query(f"{prefix}/nonempty", retained, witness),
        active=sat_query(f"{prefix}/active", retained, witness),
        inactive=sat_query(f"{prefix}/inactive", retained, witness),
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
    return verify_exact_polyhedral_extension_admission_schema(
        ExactPolyhedralExtensionAdmissionSchema(
            space=SPACE,
            required_cell_ids=("primary",),
            inclusion_schema=MonotonePolyhedralInclusionSchema(
                inner_tier_id="inner",
                outer_tier_id="outer",
                base_queries_by_cell={"primary": base_query()},
            ),
        )
    )


def admitted_look(look, *, inner_retained=None, outer_retained=None):
    return ExactPolyhedralExtensionLook(
        look=look,
        inner_cells_by_id={
            "primary": ExactLinearProofCell(
                description=f"inner proof cell at look {look}",
                motif_bundles={"focal": invariant_bundle("inner", inner_retained or later_inner(), inner=True)},
            )
        },
        outer_cells_by_id={
            "primary": ExactLinearProofCell(
                description=f"outer proof cell at look {look}",
                motif_bundles={"focal": invariant_bundle("outer", outer_retained or fixed_outer(), inner=False)},
            )
        },
        evidence_reference=f"proof://extension-look-{look}",
    )


def test_schema_builds_all_look_beta_zero_and_gamma_zero_certificates():
    verified = verified_schema()

    assert verified.all_look_solver_certificate.lower_bound == 1.0
    assert verified.all_look_solver_certificate.certified_looks is None
    assert verified.all_look_solver_certificate.method == EXACT_POLYHEDRAL_EXTENSION_ADMISSION_VERIFIER
    assert verified.all_look_inclusion_certificate.lower_bound == 1.0
    assert verified.all_look_inclusion_certificate.certified_looks is None


def test_admitted_exact_snapshots_bind_outer_solver_and_inclusion_at_any_look():
    verified = verified_schema()
    first = admit_exact_polyhedral_extension_look(verified, admitted_look(1))
    later = admit_exact_polyhedral_extension_look(verified, admitted_look(10000))

    report = audit_anytime_symbolic_universe_extension(
        (first.snapshot, later.snapshot),
        inclusion_certificate=verified.all_look_inclusion_certificate,
        coverage_certificate=AnytimeSymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("primary",),
            lower_bound=0.95,
            method="external all-look coverage",
        ),
        solver_certificate=verified.all_look_solver_certificate,
    )

    assert report.reports_by_look[1].motifs["focal"].extension_status is ExtensionStatus.EXTENSION_STABLE
    assert report.reports_by_look[10000].motifs["focal"].extension_status is ExtensionStatus.EXTENSION_STABLE
    assert later.verified_inclusion_look.look == 10000


def test_rejects_inner_system_that_drops_a_base_row():
    verified = verified_schema()
    weakened_inner = system(row((1,), "3/4", "only new row"), description="weakened inner")
    proposed = ExactPolyhedralExtensionLook(
        look=1,
        inner_cells_by_id={
            "primary": ExactLinearProofCell(
                description="weakened inner cell",
                motif_bundles={"focal": nondecisive_bundle("weakened", weakened_inner, 0)},
            )
        },
        outer_cells_by_id=admitted_look(1).outer_cells_by_id,
        evidence_reference="proof://weakened-inner",
    )

    with pytest.raises(ValueError, match="retain every base inequality"):
        admit_exact_polyhedral_extension_look(verified, proposed)


def test_rejects_outer_retained_system_drift_before_stability_claim():
    verified = verified_schema()
    drifted_outer = system(
        row((-1,), 0, "x >= 0"),
        row((1,), 3, "x <= 3"),
        description="drifted outer",
    )

    with pytest.raises(ValueError, match="fixed outer"):
        admit_exact_polyhedral_extension_look(
            verified,
            admitted_look(1, outer_retained=drifted_outer),
        )


def test_malformed_outer_linear_proof_is_rejected_before_snapshot_construction():
    verified = verified_schema()
    bad_outer_bundle = LinearMotifQueryBundle(
        nonempty=sat_query("bad/nonempty", fixed_outer(), "5"),
        active=sat_query("bad/active", fixed_outer(), "5"),
        inactive=unsat_query(
            "bad/inactive",
            system(*fixed_outer().inequalities, row((1,), -1, "x <= -1")),
            (1, 0, 1),
        ),
    )
    proposed = ExactPolyhedralExtensionLook(
        look=1,
        inner_cells_by_id=admitted_look(1).inner_cells_by_id,
        outer_cells_by_id={
            "primary": ExactLinearProofCell(
                description="malformed outer",
                motif_bundles={"focal": bad_outer_bundle},
            )
        },
        evidence_reference="proof://bad-outer",
    )

    with pytest.raises(ValueError, match="SAT witness violates"):
        admit_exact_polyhedral_extension_look(verified, proposed)


def test_combined_exact_admission_recovers_alpha_for_anytime_stability():
    verified = verified_schema()
    guarantee = anytime_symbolic_extension_stability_guarantee(
        target=verified.target,
        coverage_certificate=AnytimeSymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("primary",),
            lower_bound=0.95,
            method="external all-look coverage",
        ),
        solver_certificate=verified.all_look_solver_certificate,
        inclusion_certificate=verified.all_look_inclusion_certificate,
    )

    assert guarantee.certified_looks is None
    assert isclose(guarantee.solver_semantic_failure_upper_bound, 0.0)
    assert isclose(guarantee.inclusion_failure_upper_bound, 0.0)
    assert isclose(guarantee.time_uniform_false_decisive_or_invalid_stability_upper_bound, 0.05)
