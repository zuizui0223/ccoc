"""Minimal hash-bound RACH certificate manifest example.

The payloads below stand in for a formal candidate-space encoding, a motif
predicate, all-look coverage evidence, solver-validity evidence, one query
encoding, and one proof artifact. No raw data and no solver search are used.

Run:
    python examples/certificate_manifest.py
"""

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
    verify_anytime_symbolic_manifest,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace


def main() -> None:
    payloads = {
        "candidate-space": '{"variables":["x"],"retained":"x>=1/5"}',
        "motif:nonnegative": '{"name":"nonnegative","predicate":"x>=0"}',
        "coverage-proof": '{"method":"confidence-sequence","alpha":0.05}',
        "solver-audit": '{"verifier":"exact-rational-linear","beta":0.0}',
        "query": '{"look":1,"cell":"primary","query":"x>=1/5 and x<=0"}',
        "proof": '{"certificate":["1","1"]}',
    }
    space = SymbolicCandidateSpace("rational polyhedral candidate space", ("nonnegative",))
    coverage = AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external confidence sequence",
        certified_looks=(1, 2),
    )
    solver = AnytimeSolverSemanticValidityCertificate(
        required_cell_ids=("primary",),
        motifs=("nonnegative",),
        lower_bound=1.0,
        method="exact rational proof verifier",
        certified_looks=(1, 2),
    )
    target = ManifestTarget.from_payloads(
        space,
        candidate_space_payload=payloads["candidate-space"],
        motif_definition_payloads={"nonnegative": payloads["motif:nonnegative"]},
        required_cell_ids=("primary",),
        certified_looks=(1, 2),
    )
    manifest = build_anytime_symbolic_manifest(
        target=target,
        coverage_certificate=coverage,
        solver_certificate=solver,
        coverage_assertion=ExternalAssertionBinding.from_payload(
            kind="time-uniform-statistical-coverage",
            lower_bound=coverage.lower_bound,
            method=coverage.method,
            assumptions=coverage.assumptions,
            evidence_artifact_id="coverage-proof",
            evidence_payload=payloads["coverage-proof"],
        ),
        solver_assertion=ExternalAssertionBinding.from_payload(
            kind="time-uniform-solver-semantic-validity",
            lower_bound=solver.lower_bound,
            method=solver.method,
            assumptions=solver.assumptions,
            evidence_artifact_id="solver-audit",
            evidence_payload=payloads["solver-audit"],
        ),
        solver_query_proofs=(
            SolverQueryProofBinding.from_payloads(
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
            ),
        ),
    )
    report = verify_anytime_symbolic_manifest(
        manifest,
        space=space,
        coverage_certificate=coverage,
        solver_certificate=solver,
        payloads=payloads,
    )
    print("target digest:", report.target_digest)
    print("manifest digest:", report.manifest_digest)
    print("verified artifacts:", ", ".join(report.verified_artifact_ids))


if __name__ == "__main__":
    main()
