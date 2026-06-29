import pytest

from causal_model.admissibility import CoverageMode, MotifStatus
from causal_model.anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
    SequentialSymbolicConfidenceSetSnapshot,
)
from causal_model.certificate_decision_audit import (
    CertificateAuditReason,
    audit_symbolic_snapshot_decisions,
    bind_certificate_to_manifest,
    verify_and_audit_anytime_symbolic_decisions,
)
from causal_model.certificate_manifest import (
    ExternalAssertionBinding,
    ManifestTarget,
    QueryRole,
    SolverQueryProofBinding,
    build_anytime_symbolic_manifest,
)
from causal_model.symbolic_candidate_sets import (
    FeasibilityCertificate,
    FeasibilityStatus,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    SymbolicMotifQueries,
)

SPACE = SymbolicCandidateSpace("symbolic test space", ("focal",))


def unbound(status):
    return FeasibilityCertificate(
        query_description="unbound-query",
        status=status,
        evidence_reference="unbound-proof" if status is not FeasibilityStatus.UNKNOWN else "",
        solver="unbound-verifier",
    )


def binding(role, status):
    return SolverQueryProofBinding.from_payloads(
        look=1,
        cell_id="primary",
        motif="focal",
        role=role,
        status=status,
        query_encoding_payload=f"query:{role.value}:{status.value}",
        proof_payload=f"proof:{role.value}:{status.value}",
        verifier_id="backend/v1",
        query_artifact_id=f"query-{role.value}",
        proof_artifact_id=f"proof-{role.value}",
    )


def setup(bindings):
    coverage = AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="coverage method",
        certified_looks=(1,),
    )
    solver = AnytimeSolverSemanticValidityCertificate(
        required_cell_ids=("primary",),
        motifs=("focal",),
        lower_bound=1.0,
        method="solver method",
        certified_looks=(1,),
    )
    target = ManifestTarget.from_payloads(
        SPACE,
        candidate_space_payload="space",
        motif_definition_payloads={"focal": "motif"},
        required_cell_ids=("primary",),
        certified_looks=(1,),
    )
    payloads = {
        "candidate-space": "space",
        "motif:focal": "motif",
        "coverage": "coverage artifact",
        "solver": "solver artifact",
    }
    for item in bindings:
        payloads[item.query_encoding_artifact.artifact_id] = f"query:{item.role.value}:{item.status.value}"
        payloads[item.proof_artifact.artifact_id] = f"proof:{item.role.value}:{item.status.value}"
    manifest = build_anytime_symbolic_manifest(
        target=target,
        coverage_certificate=coverage,
        solver_certificate=solver,
        coverage_assertion=ExternalAssertionBinding.from_payload(
            kind="time-uniform-statistical-coverage",
            lower_bound=coverage.lower_bound,
            method=coverage.method,
            assumptions=coverage.assumptions,
            evidence_artifact_id="coverage",
            evidence_payload=payloads["coverage"],
        ),
        solver_assertion=ExternalAssertionBinding.from_payload(
            kind="time-uniform-solver-semantic-validity",
            lower_bound=solver.lower_bound,
            method=solver.method,
            assumptions=solver.assumptions,
            evidence_artifact_id="solver",
            evidence_payload=payloads["solver"],
        ),
        solver_query_proofs=bindings,
    )
    return manifest, payloads, coverage, solver


def snapshot(nonempty, active, inactive):
    return SequentialSymbolicConfidenceSetSnapshot(
        look=1,
        cells=(
            SymbolicConfidenceSetCell(
                cell_id="primary",
                description="test cell",
                motif_queries={"focal": SymbolicMotifQueries(nonempty, active, inactive)},
                coverage_mode=CoverageMode.SOLVER_BACKED,
            ),
        ),
    )


def test_complete_invariant_is_retained():
    nonempty = binding(QueryRole.NONEMPTY, FeasibilityStatus.SAT)
    inactive = binding(QueryRole.INACTIVE, FeasibilityStatus.UNSAT)
    manifest, _, _, _ = setup((nonempty, inactive))
    result = audit_symbolic_snapshot_decisions(
        SPACE,
        snapshot(
            bind_certificate_to_manifest(unbound(FeasibilityStatus.SAT), nonempty),
            unbound(FeasibilityStatus.SAT),
            bind_certificate_to_manifest(unbound(FeasibilityStatus.UNSAT), inactive),
        ),
        manifest,
    ).motifs["focal"]
    assert result.source_status is MotifStatus.INVARIANT
    assert result.audited_status is MotifStatus.INVARIANT


def test_missing_proof_downgrades_invariant_to_unsupported():
    nonempty = binding(QueryRole.NONEMPTY, FeasibilityStatus.SAT)
    manifest, _, _, _ = setup((nonempty,))
    result = audit_symbolic_snapshot_decisions(
        SPACE,
        snapshot(
            bind_certificate_to_manifest(unbound(FeasibilityStatus.SAT), nonempty),
            unbound(FeasibilityStatus.SAT),
            unbound(FeasibilityStatus.UNSAT),
        ),
        manifest,
    ).motifs["focal"]
    assert result.audited_status is MotifStatus.UNSUPPORTED
    assert CertificateAuditReason.MISSING_BINDING in result.reasons


def test_unresolved_needs_both_bound_witnesses():
    active = binding(QueryRole.ACTIVE, FeasibilityStatus.SAT)
    inactive = binding(QueryRole.INACTIVE, FeasibilityStatus.SAT)
    manifest, _, _, _ = setup((active, inactive))
    complete = audit_symbolic_snapshot_decisions(
        SPACE,
        snapshot(
            unbound(FeasibilityStatus.SAT),
            bind_certificate_to_manifest(unbound(FeasibilityStatus.SAT), active),
            bind_certificate_to_manifest(unbound(FeasibilityStatus.SAT), inactive),
        ),
        manifest,
    ).motifs["focal"]
    assert complete.audited_status is MotifStatus.UNRESOLVED

    incomplete_manifest, _, _, _ = setup((active,))
    incomplete = audit_symbolic_snapshot_decisions(
        SPACE,
        snapshot(
            unbound(FeasibilityStatus.SAT),
            bind_certificate_to_manifest(unbound(FeasibilityStatus.SAT), active),
            unbound(FeasibilityStatus.SAT),
        ),
        incomplete_manifest,
    ).motifs["focal"]
    assert incomplete.audited_status is MotifStatus.UNSUPPORTED
    assert CertificateAuditReason.MISSING_INACTIVE_WITNESS in incomplete.reasons


def test_end_to_end_gate_checks_manifest_payloads_first():
    nonempty = binding(QueryRole.NONEMPTY, FeasibilityStatus.SAT)
    inactive = binding(QueryRole.INACTIVE, FeasibilityStatus.UNSAT)
    manifest, payloads, coverage, solver = setup((nonempty, inactive))
    audited = verify_and_audit_anytime_symbolic_decisions(
        manifest=manifest,
        space=SPACE,
        coverage_certificate=coverage,
        solver_certificate=solver,
        payloads=payloads,
        snapshots=(
            snapshot(
                bind_certificate_to_manifest(unbound(FeasibilityStatus.SAT), nonempty),
                unbound(FeasibilityStatus.SAT),
                bind_certificate_to_manifest(unbound(FeasibilityStatus.UNSAT), inactive),
            ),
        ),
    )
    assert not audited.any_downgraded_decision

    payloads[inactive.proof_artifact.artifact_id] = "changed"
    with pytest.raises(ValueError, match="digest mismatch"):
        verify_and_audit_anytime_symbolic_decisions(
            manifest=manifest,
            space=SPACE,
            coverage_certificate=coverage,
            solver_certificate=solver,
            payloads=payloads,
            snapshots=(
                snapshot(
                    bind_certificate_to_manifest(unbound(FeasibilityStatus.SAT), nonempty),
                    unbound(FeasibilityStatus.SAT),
                    bind_certificate_to_manifest(unbound(FeasibilityStatus.UNSAT), inactive),
                ),
            ),
        )
