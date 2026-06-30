from dataclasses import replace

import pytest

from causal_model.all_look_coverage_contract import (
    CoverageProofVerificationReceipt,
    coverage_contract_artifact,
    coverage_contract_from_certificate,
    verify_all_look_coverage_contract,
)
from causal_model.anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
)
from causal_model.certificate_manifest import (
    ArtifactReference,
    ExternalAssertionBinding,
    ManifestTarget,
)
from causal_model.coverage_bound_native_tiered_transcript import (
    CoverageBoundTieredManifest,
    coverage_bound_schema_artifact,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace
from causal_model.tiered_certificate_manifest import (
    QueryTier,
    TieredQueryPlanBinding,
    TieredSolverQueryProofBinding,
    build_anytime_tiered_symbolic_manifest,
)
from causal_model.certificate_manifest import QueryRole


SPACE = SymbolicCandidateSpace("coverage contract candidate space", ("focal",))


def artifact(identifier, payload):
    return ArtifactReference.from_payload(identifier, payload, media_type="application/json")


def target_and_certificates():
    coverage = AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external confidence sequence",
        assumptions=("all positive looks", "declared retained encoder"),
    )
    solver = AnytimeSolverSemanticValidityCertificate(
        required_cell_ids=("primary",),
        motifs=("focal",),
        lower_bound=1.0,
        method="exact compiler verifier",
        assumptions=("exact branch proofs",),
    )
    target = ManifestTarget.from_payloads(
        SPACE,
        candidate_space_payload=b'{"variables":["x"]}',
        motif_definition_payloads={"focal": b'{"motif":"focal"}'},
        required_cell_ids=("primary",),
        certified_looks=None,
    )
    return target, coverage, solver


def contract_fixture():
    target, coverage, solver = target_and_certificates()
    observation = artifact("observation-channel", b'{"channel":"arbitrary-stream"}')
    encoder = artifact("retained-encoder", b'{"encoder":"time-uniform-cs"}')
    proof = artifact("coverage-proof", b'{"theorem":"all-look-coverage"}')
    contract = coverage_contract_from_certificate(
        contract_id="coverage-run-1",
        target=target,
        coverage_certificate=coverage,
        observation_channel_artifact=observation,
        retained_set_encoder_artifact=encoder,
        coverage_proof_artifact=proof,
        coverage_verifier_id="toy-coverage-proof-verifier",
    )
    payloads = {
        target.candidate_space_artifact.artifact_id: b'{"variables":["x"]}',
        observation.artifact_id: b'{"channel":"arbitrary-stream"}',
        encoder.artifact_id: b'{"encoder":"time-uniform-cs"}',
        proof.artifact_id: b'{"theorem":"all-look-coverage"}',
    }
    return target, coverage, solver, contract, payloads


class ToyCoverageVerifier:
    verifier_id = "toy-coverage-proof-verifier"

    def verify_all_look_coverage(self, contract, artifact_payloads):
        # This toy backend represents a method-specific theorem checker.  It is
        # intentionally narrow: it only accepts the exact committed proof bytes.
        if artifact_payloads[contract.coverage_proof_artifact.artifact_id] != b'{"theorem":"all-look-coverage"}':
            raise ValueError("toy theorem proof does not verify")
        return CoverageProofVerificationReceipt(
            contract_digest=contract.contract_digest,
            verifier_id=self.verifier_id,
            coverage_proof_artifact_sha256=contract.coverage_proof_artifact.sha256,
            retained_set_encoder_artifact_sha256=contract.retained_set_encoder_artifact.sha256,
            observation_channel_artifact_sha256=contract.observation_channel_artifact.sha256,
        )


def tiered_manifest(target, coverage, solver):
    coverage_assertion = ExternalAssertionBinding.from_payload(
        kind="time-uniform-statistical-coverage",
        lower_bound=coverage.lower_bound,
        method=coverage.method,
        assumptions=coverage.assumptions,
        evidence_artifact_id="coverage-assertion",
        evidence_payload=b'{"coverage":"all-look"}',
    )
    solver_assertion = ExternalAssertionBinding.from_payload(
        kind="time-uniform-solver-semantic-validity",
        lower_bound=solver.lower_bound,
        method=solver.method,
        assumptions=solver.assumptions,
        evidence_artifact_id="solver-assertion",
        evidence_payload=b'{"solver":"exact"}',
    )
    partition = artifact("partition", b'{"cells":["true","false"]}')
    plan = TieredQueryPlanBinding(
        tier=QueryTier.OUTER,
        look=1,
        cell_id="primary",
        query_plan_artifact=artifact("plan:outer", b'{"tier":"outer"}'),
    )
    proof = TieredSolverQueryProofBinding(
        tier=QueryTier.OUTER,
        look=1,
        cell_id="primary",
        motif="focal",
        role=QueryRole.INACTIVE,
        status=FeasibilityStatus.UNSAT,
        query_plan_artifact=plan.query_plan_artifact,
        proof_artifact=artifact("proof:outer", b'{"farkas":["1"]}'),
        verifier_id="exact compiler verifier",
    )
    return build_anytime_tiered_symbolic_manifest(
        target=target,
        coverage_certificate=coverage,
        solver_certificate=solver,
        coverage_assertion=coverage_assertion,
        solver_assertion=solver_assertion,
        semantic_partition_artifact=partition,
        tiered_query_plans=(plan,),
        solver_query_proofs=(proof,),
    )


def test_contract_binds_target_encoder_observation_and_proof_to_exact_all_look_event():
    target, coverage, _, contract, payloads = contract_fixture()

    receipt = verify_all_look_coverage_contract(
        contract,
        target=target,
        coverage_certificate=coverage,
        artifact_payloads=payloads,
        verifier=ToyCoverageVerifier(),
    )
    assert receipt.contract_digest == contract.contract_digest
    assert contract.miscoverage_upper_bound == pytest.approx(0.05)
    assert coverage_contract_artifact(contract).sha256 == contract.contract_digest

    tampered = dict(payloads)
    tampered["retained-encoder"] = b'{"encoder":"other"}'
    with pytest.raises(ValueError, match="artifact digest mismatch"):
        verify_all_look_coverage_contract(
            contract,
            target=target,
            coverage_certificate=coverage,
            artifact_payloads=tampered,
            verifier=ToyCoverageVerifier(),
        )


def test_contract_rejects_coverage_scope_or_true_label_drift_before_external_verification():
    target, coverage, _, contract, payloads = contract_fixture()
    wrong_label = replace(coverage, true_candidate_label="another_theta")
    with pytest.raises(ValueError, match="true candidate label"):
        verify_all_look_coverage_contract(
            contract,
            target=target,
            coverage_certificate=wrong_label,
            artifact_payloads=payloads,
            verifier=ToyCoverageVerifier(),
        )

    wrong_scope = replace(coverage, certified_looks=(1, 2))
    with pytest.raises(ValueError, match="look scope"):
        verify_all_look_coverage_contract(
            contract,
            target=target,
            coverage_certificate=wrong_scope,
            artifact_payloads=payloads,
            verifier=ToyCoverageVerifier(),
        )


def test_coverage_bound_v2_manifest_and_schema_artifact_cannot_mix_coverage_claims():
    target, coverage, solver, contract, _ = contract_fixture()
    manifest = tiered_manifest(target, coverage, solver)
    contract_artifact = coverage_contract_artifact(contract)
    bound = CoverageBoundTieredManifest(
        tiered_manifest=manifest,
        coverage_contract=contract,
        coverage_contract_artifact=contract_artifact,
    )
    assert contract.contract_digest.encode("utf-8") in bound.payload

    changed_contract = replace(contract, method="different coverage method")
    with pytest.raises(ValueError, match="method"):
        CoverageBoundTieredManifest(
            tiered_manifest=manifest,
            coverage_contract=changed_contract,
            coverage_contract_artifact=coverage_contract_artifact(changed_contract),
        )

    base_schema = artifact("base-admission-schema", b'{"schema":"exact"}')
    first = coverage_bound_schema_artifact(
        base_admission_schema_artifact=base_schema,
        coverage_contract=contract,
    )
    second = coverage_bound_schema_artifact(
        base_admission_schema_artifact=base_schema,
        coverage_contract=replace(contract, contract_id="coverage-run-2"),
    )
    assert first.sha256 != second.sha256
