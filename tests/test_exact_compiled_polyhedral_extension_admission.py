from dataclasses import replace
from math import isclose

import pytest

from causal_model.admissibility import MotifStatus
from causal_model.anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from causal_model.exact_compiled_polyhedral_extension_admission import (
    ExactCompiledPolyhedralExtensionAdmissionSchema,
    ExactCompiledPolyhedralExtensionLook,
    ExactCompiledPolyhedralProofCell,
    admit_exact_compiled_polyhedral_extension_look,
    audit_exact_compiled_polyhedral_extension_looks,
    compiled_query_plan_for_admission,
    exact_compiled_polyhedral_extension_guarantee,
    verify_exact_compiled_polyhedral_extension_admission_schema,
)
from causal_model.linear_proof_verifier import (
    FarkasInfeasibilityCertificate,
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    RationalLinearSystem,
    RationalWitness,
)
from causal_model.online_polyhedral_inclusion_schema import MonotonePolyhedralInclusionSchema
from causal_model.polyhedral_motif_compiler import (
    ConflictingCellOverlapProof,
    PolyhedralMotifPartition,
    TaggedPolyhedralCell,
    conjoin_linear_systems,
    verify_polyhedral_motif_partition,
)
from causal_model.rational_polyhedral_inclusion import (
    FarkasRowImplicationCertificate,
    RationalPolyhedralInclusionProof,
    RationalPolyhedralInclusionQuery,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace
from causal_model.symbolic_universe_extension import ExtensionStatus


SPACE = SymbolicCandidateSpace("fixed tagged union for all-look compiler admission", ("focal",))


def row(coefficients, bound, label=""):
    return LinearInequality(tuple(coefficients), bound, label)


def system(*rows, description=""):
    return RationalLinearSystem(("x",), tuple(rows), description)


def true_cell_system():
    return system(row((-1,), 0, "x >= 0"), description="true tagged cell")


def false_cell_system():
    return system(row((1,), -1, "x <= -1"), description="false tagged cell")


def base_inner_system():
    return system(
        row((-1,), 0, "x >= 0"),
        row((1,), 1, "x <= 1"),
        description="base retained inner",
    )


def later_inner_system():
    return system(
        row((-1,), 0, "x >= 0"),
        row((1,), 1, "x <= 1"),
        row((1,), "3/4", "x <= 3/4"),
        description="later retained inner",
    )


def fixed_outer_system():
    return system(
        row((-1,), 0, "x >= 0"),
        row((1,), 2, "x <= 2"),
        description="fixed retained outer",
    )


def verified_partition():
    false = TaggedPolyhedralCell(
        cell_id="false",
        system=false_cell_system(),
        motif_values={"focal": False},
    )
    true = TaggedPolyhedralCell(
        cell_id="true",
        system=true_cell_system(),
        motif_values={"focal": True},
    )
    overlap = LinearFeasibilityQuery(
        query_id="partition/false-true-overlap",
        system=conjoin_linear_systems(false.system, true.system),
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.UNSAT,
            farkas=FarkasInfeasibilityCertificate((1, 1)),
            evidence_reference="proof://partition/false-true-overlap",
        ),
    )
    return verify_polyhedral_motif_partition(
        PolyhedralMotifPartition(
            space=SPACE,
            cells=(false, true),
            conflicting_overlap_proofs=(ConflictingCellOverlapProof("false", "true", overlap),),
        )
    )


def base_inclusion_query():
    return RationalPolyhedralInclusionQuery(
        query_id="base-inner-in-fixed-outer",
        inner_system=base_inner_system(),
        outer_system=fixed_outer_system(),
        proof=RationalPolyhedralInclusionProof(
            inner_witness=RationalWitness((0,)),
            row_certificates=(
                FarkasRowImplicationCertificate(0, (1, 0)),
                FarkasRowImplicationCertificate(1, (0, 1)),
            ),
            evidence_reference="proof://base-inner-in-fixed-outer",
        ),
    )


def verified_schema():
    return verify_exact_compiled_polyhedral_extension_admission_schema(
        ExactCompiledPolyhedralExtensionAdmissionSchema(
            space=SPACE,
            required_cell_ids=("primary",),
            inclusion_schema=MonotonePolyhedralInclusionSchema(
                inner_tier_id="inner",
                outer_tier_id="outer",
                base_queries_by_cell={"primary": base_inclusion_query()},
            ),
            motif_partition=verified_partition(),
        )
    )


def proof_cell(verified, *, look, tier, retained, false_branch="unsat"):
    plan = compiled_query_plan_for_admission(
        verified,
        look=look,
        tier=tier,
        cell_id="primary",
        retained_system=retained,
    )
    proofs = {}
    for template in plan.templates:
        if template.partition_cell_id == "true":
            proofs[template.query_id] = LinearFeasibilityProof(
                status=FeasibilityStatus.SAT,
                witness=RationalWitness((0,)),
                evidence_reference=f"proof://{template.query_id}",
            )
        elif false_branch == "unknown":
            proofs[template.query_id] = LinearFeasibilityProof(status=FeasibilityStatus.UNKNOWN)
        else:
            # Every false branch is [retained rows..., x <= -1]. The first retained
            # row is -x <= 0, so multipliers on it and the final row derive 0 <= -1.
            multipliers = (1, *(0 for _ in range(len(template.system.inequalities) - 2)), 1)
            proofs[template.query_id] = LinearFeasibilityProof(
                status=FeasibilityStatus.UNSAT,
                farkas=FarkasInfeasibilityCertificate(multipliers),
                evidence_reference=f"proof://{template.query_id}",
            )
    return ExactCompiledPolyhedralProofCell(
        description=f"{tier} compiler proof cell at look {look}",
        retained_system=retained,
        proofs_by_query_id=proofs,
    )


def proposed_look(verified, look, *, outer_system=None, false_branch="unsat"):
    return ExactCompiledPolyhedralExtensionLook(
        look=look,
        inner_cells_by_id={
            "primary": proof_cell(
                verified,
                look=look,
                tier="inner",
                retained=later_inner_system(),
                false_branch=false_branch,
            )
        },
        outer_cells_by_id={
            "primary": proof_cell(
                verified,
                look=look,
                tier="outer",
                retained=outer_system or fixed_outer_system(),
                false_branch=false_branch,
            )
        },
        evidence_reference=f"proof://compiled-extension-look-{look}",
    )


def coverage():
    return AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external all-look coverage",
    )


def test_schema_builds_all_look_compiler_solver_and_intersection_inclusion_certificates():
    verified = verified_schema()

    assert verified.all_look_solver_certificate.lower_bound == 1.0
    assert verified.all_look_solver_certificate.certified_looks is None
    assert verified.all_look_inclusion_certificate.lower_bound == 1.0
    assert verified.all_look_inclusion_certificate.certified_looks is None
    assert any(
        verified.verified_partition.partition_digest in assumption
        for assumption in verified.all_look_solver_certificate.assumptions
    )


def test_compiler_admission_is_extension_stable_at_look_one_and_arbitrarily_late_look():
    verified = verified_schema()
    first = admit_exact_compiled_polyhedral_extension_look(verified, proposed_look(verified, 1))
    later = admit_exact_compiled_polyhedral_extension_look(verified, proposed_look(verified, 10000))

    report = audit_exact_compiled_polyhedral_extension_looks(
        verified,
        (first, later),
        coverage_certificate=coverage(),
    )
    assert report.reports_by_look[1].motifs["focal"].outer_status is MotifStatus.INVARIANT
    assert report.reports_by_look[1].motifs["focal"].extension_status is ExtensionStatus.EXTENSION_STABLE
    assert report.reports_by_look[10000].motifs["focal"].extension_status is ExtensionStatus.EXTENSION_STABLE
    assert first.inner_queries_by_cell["primary"].motif_queries["focal"].inactive.status is FeasibilityStatus.UNSAT


def test_outer_drift_and_missing_compiler_branch_proof_are_rejected():
    verified = verified_schema()
    drifted_outer = system(
        row((-1,), 0, "x >= 0"),
        row((1,), 3, "x <= 3"),
        description="drifted outer",
    )
    with pytest.raises(ValueError, match="fixed outer"):
        admit_exact_compiled_polyhedral_extension_look(
            verified,
            proposed_look(verified, 1, outer_system=drifted_outer),
        )

    malformed = proposed_look(verified, 1)
    inner = malformed.inner_cells_by_id["primary"]
    missing = dict(inner.proofs_by_query_id)
    missing.pop(next(iter(missing)))
    malformed_inner = replace(inner, proofs_by_query_id=missing)
    malformed = replace(malformed, inner_cells_by_id={"primary": malformed_inner})
    with pytest.raises(ValueError, match="exactly every compiler-generated query ID"):
        admit_exact_compiled_polyhedral_extension_look(verified, malformed)


def test_unknown_branch_remains_unsupported_and_never_becomes_extension_stable():
    verified = verified_schema()
    admitted = admit_exact_compiled_polyhedral_extension_look(
        verified,
        proposed_look(verified, 1, false_branch="unknown"),
    )
    report = audit_exact_compiled_polyhedral_extension_looks(
        verified,
        (admitted,),
        coverage_certificate=coverage(),
    )
    assert report.reports_by_look[1].motifs["focal"].outer_status is MotifStatus.UNSUPPORTED
    assert report.reports_by_look[1].motifs["focal"].extension_status is ExtensionStatus.UNSUPPORTED


def test_schema_rejects_forged_verified_partition_wrapper_and_recovers_alpha_bound():
    partition = verified_partition()
    forged = replace(partition, partition_digest="0" * 64)
    schema = ExactCompiledPolyhedralExtensionAdmissionSchema(
        space=SPACE,
        required_cell_ids=("primary",),
        inclusion_schema=MonotonePolyhedralInclusionSchema(
            inner_tier_id="inner",
            outer_tier_id="outer",
            base_queries_by_cell={"primary": base_inclusion_query()},
        ),
        motif_partition=forged,
    )
    with pytest.raises(ValueError, match="does not match exact re-verification"):
        verify_exact_compiled_polyhedral_extension_admission_schema(schema)

    guarantee = exact_compiled_polyhedral_extension_guarantee(
        verified_schema(),
        coverage_certificate=coverage(),
    )
    assert guarantee.certified_looks is None
    assert isclose(guarantee.solver_semantic_failure_upper_bound, 0.0)
    assert isclose(guarantee.inclusion_failure_upper_bound, 0.0)
    assert isclose(guarantee.time_uniform_false_decisive_or_invalid_stability_upper_bound, 0.05)
