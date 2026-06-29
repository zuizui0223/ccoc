import pytest

from causal_model.anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
)
from causal_model.certificate_manifest import (
    ExternalAssertionBinding,
    ManifestTarget,
    QueryRole,
    SolverQueryProofBinding,
    build_anytime_symbolic_manifest,
    canonical_json,
    sha256_digest,
    verify_anytime_symbolic_manifest,
    verify_manifest_artifacts,
    verify_manifest_context,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace


SPACE = SymbolicCandidateSpace("rational polyhedral candidate space", ("nonnegative",))


def fixture_parts():
    payloads = {
        "candidate-space": '{"variables":["x"],"retained":"x>=1/5"}',
        "motif:nonnegative": '{"name":"nonnegative","predicate":"x>=0"}',
        "coverage-proof": '{"method":"confidence-sequence","alpha":0.05}',
        "solver-audit": '{"verifier":"exact-rational-linear","beta":0.0}',
        "query": '{"look":1,"cell":"primary","query":"x>=1/5 and x<=0"}',
        "proof": '{"certificate":["1","1"]}',
    }
    coverage = AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external confidence sequence",
        assumptions=("all looks are covered",),
        certified_looks=(1, 2),
    )
    solver = AnytimeSolverSemanticValidityCertificate(
        required_cell_ids=("primary",),
        motifs=("nonnegative",),
        lower_bound=1.0,
        method="exact rational proof verifier",
        assumptions=("parser and verifier are trusted",),
        certified_looks=(2, 1),
    )
    target = ManifestTarget.from_payloads(
        SPACE,
        candidate_space_payload=payloads["candidate-space"],
        motif_definition_payloads={"nonnegative": payloads["motif:nonnegative"]},
        required_cell_ids=("primary",),
        certified_looks=(1, 2),
    )
    coverage_binding = ExternalAssertionBinding.from_payload(
        kind="time-uniform-statistical-coverage",
        lower_bound=coverage.lower_bound,
        method=coverage.method,
        assumptions=coverage.assumptions,
        evidence_artifact_id="coverage-proof",
        evidence_payload=payloads["coverage-proof"],
    )
    solver_binding = ExternalAssertionBinding.from_payload(
        kind="time-uniform-solver-semantic-validity",
        lower_bound=solver.lower_bound,
        method=solver.method,
        assumptions=solver.assumptions,
        evidence_artifact_id="solver-audit",
        evidence_payload=payloads["solver-audit"],
    )
    query_proof = SolverQueryProofBinding.from_payloads(
        look=1,
        cell_id="primary",
        motif="nonnegative",
        role=QueryRole.INACTIVE,
        status=FeasibilityStatus.UNSAT,
        query_encoding_payload=payloads["query"],
        proof_payload=payloads["proof"],
        verifier_id="exact-rational-linear-proof-verifier/v1",
        query_artifact_id="query",
        proof_artifact_id="proof",
    )
    manifest = build_anytime_symbolic_manifest(
        target=target,
        coverage_certificate=coverage,
        solver_certificate=solver,
        coverage_assertion=coverage_binding,
        solver_assertion=solver_binding,
        solver_query_proofs=(query_proof,),
    )
    return payloads, coverage, solver, target, coverage_binding, solver_binding, query_proof, manifest


def test_canonical_json_hash_is_stable_under_mapping_order():
    assert canonical_json({"b": 2, "a": 1}) == canonical_json({"a": 1, "b": 2})
    assert sha256_digest(canonical_json({"b": 2, "a": 1})) == sha256_digest(canonical_json({"a": 1, "b": 2}))


def test_valid_manifest_binds_target_and_every_artifact():
    payloads, coverage, solver, target, _, _, _, manifest = fixture_parts()
    report = verify_anytime_symbolic_manifest(
        manifest,
        space=SPACE,
        coverage_certificate=coverage,
        solver_certificate=solver,
        payloads=payloads,
    )
    assert report.manifest_digest == manifest.manifest_digest
    assert report.target_digest == target.target_digest
    assert set(report.verified_artifact_ids) == set(payloads)


def test_proof_tampering_is_rejected_by_digest():
    payloads, _, _, _, _, _, _, manifest = fixture_parts()
    payloads["proof"] = '{"certificate":["1","2"]}'
    with pytest.raises(ValueError, match="digest mismatch"):
        verify_manifest_artifacts(manifest, payloads)


def test_context_rejects_changed_coverage_bound():
    _, coverage, solver, _, _, _, _, manifest = fixture_parts()
    changed = AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.9,
        method=coverage.method,
        assumptions=coverage.assumptions,
        certified_looks=(1, 2),
    )
    with pytest.raises(ValueError, match="coverage bound"):
        verify_manifest_context(
            manifest,
            space=SPACE,
            coverage_certificate=changed,
            solver_certificate=solver,
        )


def test_out_of_scope_and_duplicate_query_bindings_are_rejected():
    _, coverage, solver, target, coverage_binding, solver_binding, query_proof, _ = fixture_parts()
    out_of_scope = SolverQueryProofBinding.from_payloads(
        look=3,
        cell_id="primary",
        motif="nonnegative",
        role=QueryRole.INACTIVE,
        status=FeasibilityStatus.UNSAT,
        query_encoding_payload="later-query",
        proof_payload="later-proof",
        verifier_id="verifier",
    )
    with pytest.raises(ValueError, match="outside the manifest target scope"):
        build_anytime_symbolic_manifest(
            target=target,
            coverage_certificate=coverage,
            solver_certificate=solver,
            coverage_assertion=coverage_binding,
            solver_assertion=solver_binding,
            solver_query_proofs=(out_of_scope,),
        )
    with pytest.raises(ValueError, match="must be unique"):
        build_anytime_symbolic_manifest(
            target=target,
            coverage_certificate=coverage,
            solver_certificate=solver,
            coverage_assertion=coverage_binding,
            solver_assertion=solver_binding,
            solver_query_proofs=(query_proof, query_proof),
        )


def test_target_digest_changes_when_motif_definition_changes():
    payloads, _, _, target, _, _, _, _ = fixture_parts()
    changed = ManifestTarget.from_payloads(
        SPACE,
        candidate_space_payload=payloads["candidate-space"],
        motif_definition_payloads={"nonnegative": '{"name":"nonnegative","predicate":"x>0"}'},
        required_cell_ids=("primary",),
        certified_looks=(1, 2),
    )
    assert changed.target_digest != target.target_digest
