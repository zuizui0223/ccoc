import pytest

from causal_model.certificate_manifest import QueryRole
from causal_model.linear_proof_verifier import (
    FarkasInfeasibilityCertificate,
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    RationalLinearSystem,
    RationalWitness,
)
from causal_model.polyhedral_motif_compiler import (
    ConflictingCellOverlapProof,
    PolyhedralMotifPartition,
    TaggedPolyhedralCell,
    bind_compiled_polyhedral_motif_proofs,
    compile_polyhedral_motif_query_plan,
    conjoin_linear_systems,
    verify_compiled_polyhedral_motif_proofs,
    verify_polyhedral_motif_partition,
)
from causal_model.replayable_compiled_role_artifacts import (
    build_replayable_compiled_role_bundle,
    replay_compiled_role_proof_bundle,
    replayable_compiled_role_proof_bundle_artifact,
    replayable_compiled_role_proof_bundle_payload,
)
from causal_model.replayable_exact_linear_proofs import (
    ExactLinearProofBundle,
    canonical_exact_linear_bundle_bytes,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace


SPACE = SymbolicCandidateSpace("replayable compiled-role space", ("focal",))


def row(coefficients, bound, label=""):
    return LinearInequality(tuple(coefficients), bound, label)


def system(*rows, description=""):
    return RationalLinearSystem(("x",), tuple(rows), description)


def verified_partition():
    false = TaggedPolyhedralCell(
        cell_id="false",
        system=system(row((1,), "-1", "x <= -1"), description="false cell"),
        motif_values={"focal": False},
    )
    true = TaggedPolyhedralCell(
        cell_id="true",
        system=system(row((-1,), "0", "x >= 0"), description="true cell"),
        motif_values={"focal": True},
    )
    overlap = LinearFeasibilityQuery(
        query_id="partition/false-true-overlap",
        system=conjoin_linear_systems(false.system, true.system),
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.UNSAT,
            farkas=FarkasInfeasibilityCertificate(("1", "1")),
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


def verified_queries():
    partition = verified_partition()
    retained = system(row((-1,), "0", "retain x >= 0"), description="retained")
    plan = compile_polyhedral_motif_query_plan(
        partition,
        retained_system=retained,
        query_prefix="replay",
    )
    proofs = {}
    for template in plan.templates:
        if template.partition_cell_id == "true":
            proofs[template.query_id] = LinearFeasibilityProof(
                status=FeasibilityStatus.SAT,
                witness=RationalWitness(("0",)),
                evidence_reference=f"proof://{template.query_id}",
            )
        else:
            # retained x >= 0 plus false-cell x <= -1.
            proofs[template.query_id] = LinearFeasibilityProof(
                status=FeasibilityStatus.UNSAT,
                farkas=FarkasInfeasibilityCertificate(("1", "1")),
                evidence_reference=f"proof://{template.query_id}",
            )
    return verify_compiled_polyhedral_motif_proofs(
        bind_compiled_polyhedral_motif_proofs(plan, proofs_by_query_id=proofs)
    )


def test_replayable_role_artifact_replays_and_matches_the_exact_compiler_template_family():
    queries = verified_queries()
    plan = queries.bound_proofs.plan
    raw = replayable_compiled_role_proof_bundle_payload(
        queries,
        motif="focal",
        role=QueryRole.INACTIVE,
    )
    artifact = replayable_compiled_role_proof_bundle_artifact(
        queries,
        motif="focal",
        role=QueryRole.INACTIVE,
    )
    replayed = replay_compiled_role_proof_bundle(
        raw,
        plan=plan,
        motif="focal",
        role=QueryRole.INACTIVE,
        expected_digest=artifact.sha256,
    )

    assert replayed.document.replayed_aggregate_status is FeasibilityStatus.UNSAT
    assert replayed.plan_digest == plan.plan_digest
    assert replayed.partition_digest == plan.verified_partition.partition_digest


def test_replayable_role_adapter_rejects_a_different_but_mathematically_valid_unsat_query():
    queries = verified_queries()
    plan = queries.bound_proofs.plan
    original = build_replayable_compiled_role_bundle(
        queries,
        motif="focal",
        role=QueryRole.INACTIVE,
    )
    only_branch = original.branches[0]
    substituted = LinearFeasibilityQuery(
        query_id=only_branch.query_id,
        system=system(
            row((-1,), "0", "x >= 0"),
            row((1,), "-2", "x <= -2"),
        ),
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.UNSAT,
            farkas=FarkasInfeasibilityCertificate(("1", "1")),
            evidence_reference="proof://different-but-unsat",
        ),
    )
    forged = ExactLinearProofBundle(
        bundle_id=original.bundle_id,
        plan_digest=original.plan_digest,
        partition_digest=original.partition_digest,
        motif=original.motif,
        role=original.role,
        branches=(substituted,),
        aggregate_status=FeasibilityStatus.UNSAT,
    )
    raw = canonical_exact_linear_bundle_bytes(forged)
    with pytest.raises(ValueError, match="system differs from compiler template"):
        replay_compiled_role_proof_bundle(
            raw,
            plan=plan,
            motif="focal",
            role=QueryRole.INACTIVE,
        )


def test_role_adapter_rejects_context_cross_binding_before_query_replay():
    queries = verified_queries()
    plan = queries.bound_proofs.plan
    raw = replayable_compiled_role_proof_bundle_payload(
        queries,
        motif="focal",
        role=QueryRole.INACTIVE,
    )
    with pytest.raises(ValueError, match="expected role"):
        replay_compiled_role_proof_bundle(
            raw,
            plan=plan,
            motif="focal",
            role=QueryRole.ACTIVE,
        )
