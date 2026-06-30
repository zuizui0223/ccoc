import json

import pytest

from causal_model.anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
)
from causal_model.canonical_tiered_manifest_json import (
    CANONICAL_TIERED_MANIFEST_JSON_FORMAT,
    canonical_tiered_manifest_bytes,
    canonical_tiered_manifest_digest,
    canonical_tiered_manifest_json,
    parse_canonical_tiered_manifest,
    verify_canonical_tiered_manifest,
)
from causal_model.certificate_manifest import (
    ArtifactReference,
    ExternalAssertionBinding,
    ManifestTarget,
    QueryRole,
    SolverQueryProofBinding,
    build_anytime_symbolic_manifest,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace
from causal_model.tiered_certificate_manifest import (
    QueryTier,
    TieredQueryPlanBinding,
    TieredSolverQueryProofBinding,
    build_anytime_tiered_symbolic_manifest,
    migrate_v1_manifest_to_explicit_single_tier_v2,
    verify_anytime_tiered_symbolic_manifest,
)


SPACE = SymbolicCandidateSpace("tier-aware candidate space", ("focal",))


def artifact(identifier, payload):
    return ArtifactReference.from_payload(identifier, payload, media_type="application/json")


def certificates():
    coverage = AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external confidence sequence",
        assumptions=("all looks covered",),
    )
    solver = AnytimeSolverSemanticValidityCertificate(
        required_cell_ids=("primary",),
        motifs=("focal",),
        lower_bound=1.0,
        method="exact compiler verifier",
        assumptions=("tier-aware exact branch proofs",),
    )
    return coverage, solver


def common_parts():
    coverage, solver = certificates()
    target = ManifestTarget.from_payloads(
        SPACE,
        candidate_space_payload=b'{"variables":["x"]}',
        motif_definition_payloads={"focal": b'{"tagged_cells":["true","false"]}'},
        required_cell_ids=("primary",),
        certified_looks=None,
    )
    coverage_assertion = ExternalAssertionBinding.from_payload(
        kind="time-uniform-statistical-coverage",
        lower_bound=coverage.lower_bound,
        method=coverage.method,
        assumptions=coverage.assumptions,
        evidence_artifact_id="coverage",
        evidence_payload=b'{"coverage":"all-look"}',
    )
    solver_assertion = ExternalAssertionBinding.from_payload(
        kind="time-uniform-solver-semantic-validity",
        lower_bound=solver.lower_bound,
        method=solver.method,
        assumptions=solver.assumptions,
        evidence_artifact_id="solver",
        evidence_payload=b'{"solver":"exact"}',
    )
    partition = artifact("partition", b'{"cells":["true","false"]}')
    return coverage, solver, target, coverage_assertion, solver_assertion, partition


def tiered_manifest(reverse=False):
    coverage, solver, target, coverage_assertion, solver_assertion, partition = common_parts()
    inner_plan = TieredQueryPlanBinding(
        tier=QueryTier.INNER,
        look=1,
        cell_id="primary",
        query_plan_artifact=artifact("plan:inner", b'{"tier":"inner","look":1}'),
    )
    outer_plan = TieredQueryPlanBinding(
        tier=QueryTier.OUTER,
        look=1,
        cell_id="primary",
        query_plan_artifact=artifact("plan:outer", b'{"tier":"outer","look":1}'),
    )
    inner_proof = TieredSolverQueryProofBinding(
        tier=QueryTier.INNER,
        look=1,
        cell_id="primary",
        motif="focal",
        role=QueryRole.INACTIVE,
        status=FeasibilityStatus.UNSAT,
        query_plan_artifact=inner_plan.query_plan_artifact,
        proof_artifact=artifact("proof:inner:inactive", b'{"farkas":["1","1"]}'),
        verifier_id="exact-rational-linear-proof-verifier",
    )
    outer_proof = TieredSolverQueryProofBinding(
        tier=QueryTier.OUTER,
        look=1,
        cell_id="primary",
        motif="focal",
        role=QueryRole.INACTIVE,
        status=FeasibilityStatus.UNSAT,
        query_plan_artifact=outer_plan.query_plan_artifact,
        proof_artifact=artifact("proof:outer:inactive", b'{"farkas":["2","1"]}'),
        verifier_id="exact-rational-linear-proof-verifier",
    )
    plans = (outer_plan, inner_plan) if reverse else (inner_plan, outer_plan)
    proofs = (outer_proof, inner_proof) if reverse else (inner_proof, outer_proof)
    return build_anytime_tiered_symbolic_manifest(
        target=target,
        coverage_certificate=coverage,
        solver_certificate=solver,
        coverage_assertion=coverage_assertion,
        solver_assertion=solver_assertion,
        semantic_partition_artifact=partition,
        tiered_query_plans=plans,
        solver_query_proofs=proofs,
    )


def payloads_for(manifest):
    return {
        artifact_id: b"placeholder"
        for artifact_id in manifest.referenced_artifacts()
    }


def actual_payloads_for(manifest):
    payloads = {
        "candidate-space": b'{"variables":["x"]}',
        "motif:focal": b'{"tagged_cells":["true","false"]}',
        "coverage": b'{"coverage":"all-look"}',
        "solver": b'{"solver":"exact"}',
        "partition": b'{"cells":["true","false"]}',
        "plan:inner": b'{"tier":"inner","look":1}',
        "plan:outer": b'{"tier":"outer","look":1}',
        "proof:inner:inactive": b'{"farkas":["1","1"]}',
        "proof:outer:inactive": b'{"farkas":["2","1"]}',
    }
    assert set(payloads) == set(manifest.referenced_artifacts())
    return payloads


def test_v2_distinguishes_inner_and_outer_proofs_with_the_same_former_v1_key():
    manifest = tiered_manifest()

    assert len(manifest.tiered_query_plans) == 2
    assert len(manifest.solver_query_proofs) == 2
    assert manifest.solver_query_proofs[0].query_key != manifest.solver_query_proofs[1].query_key
    assert {proof.tier for proof in manifest.solver_query_proofs} == {QueryTier.INNER, QueryTier.OUTER}
    assert manifest.solver_query_proofs[0].query_key[1:] == manifest.solver_query_proofs[1].query_key[1:]


def test_v2_rejects_missing_or_cross_tier_query_plan_bindings():
    manifest = tiered_manifest()
    outer = next(proof for proof in manifest.solver_query_proofs if proof.tier is QueryTier.OUTER)
    inner_plan = next(plan for plan in manifest.tiered_query_plans if plan.tier is QueryTier.INNER)

    with pytest.raises(ValueError, match="query-plan artifact differs"):
        type(manifest)(
            target=manifest.target,
            coverage_assertion=manifest.coverage_assertion,
            solver_assertion=manifest.solver_assertion,
            semantic_partition_artifact=manifest.semantic_partition_artifact,
            tiered_query_plans=manifest.tiered_query_plans,
            solver_query_proofs=(
                manifest.solver_query_proofs[0],
                type(outer)(
                    tier=outer.tier,
                    look=outer.look,
                    cell_id=outer.cell_id,
                    motif=outer.motif,
                    role=outer.role,
                    status=outer.status,
                    query_plan_artifact=inner_plan.query_plan_artifact,
                    proof_artifact=outer.proof_artifact,
                    verifier_id=outer.verifier_id,
                ),
            ),
        )

    with pytest.raises(ValueError, match="needs a matching tiered query plan"):
        type(manifest)(
            target=manifest.target,
            coverage_assertion=manifest.coverage_assertion,
            solver_assertion=manifest.solver_assertion,
            semantic_partition_artifact=manifest.semantic_partition_artifact,
            tiered_query_plans=(inner_plan,),
            solver_query_proofs=manifest.solver_query_proofs,
        )


def test_v2_canonical_bytes_are_order_invariant_and_strict_round_trip():
    first = tiered_manifest()
    second = tiered_manifest(reverse=True)

    assert canonical_tiered_manifest_bytes(first) == canonical_tiered_manifest_bytes(second)
    assert canonical_tiered_manifest_digest(first) == canonical_tiered_manifest_digest(second)
    document = parse_canonical_tiered_manifest(canonical_tiered_manifest_bytes(first))
    assert document.manifest == first
    assert document.canonical_digest == canonical_tiered_manifest_digest(first)
    assert CANONICAL_TIERED_MANIFEST_JSON_FORMAT == "rach-canonical-tiered-manifest-json/v2"

    with pytest.raises(ValueError, match="not strict canonical"):
        parse_canonical_tiered_manifest(canonical_tiered_manifest_bytes(first) + b"\n")


def test_v2_strict_parser_rejects_missing_tier_and_duplicate_field():
    manifest = tiered_manifest()
    object_value = json.loads(canonical_tiered_manifest_json(manifest))
    del object_value["solver_query_proofs"][0]["tier"]
    malformed = json.dumps(object_value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    with pytest.raises(ValueError, match="missing"):
        parse_canonical_tiered_manifest(malformed)

    raw = canonical_tiered_manifest_json(manifest)
    duplicate = raw.replace(
        '"tier":"inner"',
        '"tier":"inner","tier":"inner"',
        1,
    )
    with pytest.raises(ValueError, match="duplicate JSON object key"):
        parse_canonical_tiered_manifest(duplicate)


def test_v2_context_and_artifact_verification_cover_partition_plans_and_proofs():
    manifest = tiered_manifest()
    coverage, solver = certificates()
    report = verify_anytime_tiered_symbolic_manifest(
        manifest,
        space=SPACE,
        coverage_certificate=coverage,
        solver_certificate=solver,
        payloads=actual_payloads_for(manifest),
    )
    assert report.tiered_target_digest == manifest.tiered_target_digest
    assert "plan:inner" in report.verified_artifact_ids
    assert "proof:outer:inactive" in report.verified_artifact_ids

    tampered = actual_payloads_for(manifest)
    tampered["plan:outer"] = b'{"tier":"outer","look":999}'
    with pytest.raises(ValueError, match="artifact digest mismatch"):
        verify_anytime_tiered_symbolic_manifest(
            manifest,
            space=SPACE,
            coverage_certificate=coverage,
            solver_certificate=solver,
            payloads=tampered,
        )


def test_v1_migration_requires_an_explicit_single_tier_and_explicit_plan():
    coverage, solver, target, coverage_assertion, solver_assertion, partition = common_parts()
    v1_proof = SolverQueryProofBinding(
        look=1,
        cell_id="primary",
        motif="focal",
        role=QueryRole.INACTIVE,
        status=FeasibilityStatus.UNSAT,
        query_encoding_artifact=artifact("v1-query", b'{"legacy":true}'),
        proof_artifact=artifact("v1-proof", b'{"farkas":["1"]}'),
        verifier_id="legacy-verifier",
    )
    v1 = build_anytime_symbolic_manifest(
        target=target,
        coverage_certificate=coverage,
        solver_certificate=solver,
        coverage_assertion=coverage_assertion,
        solver_assertion=solver_assertion,
        solver_query_proofs=(v1_proof,),
    )
    outer_plan = TieredQueryPlanBinding(
        tier=QueryTier.OUTER,
        look=1,
        cell_id="primary",
        query_plan_artifact=artifact("outer-plan", b'{"tier":"outer"}'),
    )
    migrated = migrate_v1_manifest_to_explicit_single_tier_v2(
        v1,
        tier=QueryTier.OUTER,
        semantic_partition_artifact=partition,
        tiered_query_plans=(outer_plan,),
    )
    assert migrated.solver_query_proofs[0].tier is QueryTier.OUTER
    assert migrated.solver_query_proofs[0].proof_artifact == v1_proof.proof_artifact

    with pytest.raises(ValueError, match="needs one explicit v2 plan"):
        migrate_v1_manifest_to_explicit_single_tier_v2(
            v1,
            tier=QueryTier.INNER,
            semantic_partition_artifact=partition,
            tiered_query_plans=(),
        )

    with pytest.raises(ValueError, match="all use the requested tier"):
        migrate_v1_manifest_to_explicit_single_tier_v2(
            v1,
            tier=QueryTier.OUTER,
            semantic_partition_artifact=partition,
            tiered_query_plans=(
                TieredQueryPlanBinding(
                    tier=QueryTier.INNER,
                    look=1,
                    cell_id="primary",
                    query_plan_artifact=artifact("inner-plan", b'{"tier":"inner"}'),
                ),
            ),
        )


def test_v2_digest_verification_rejects_different_canonical_content():
    manifest = tiered_manifest()
    raw = canonical_tiered_manifest_bytes(manifest)
    with pytest.raises(ValueError, match="does not match expected_digest"):
        verify_canonical_tiered_manifest(raw, expected_digest="0" * 64)
