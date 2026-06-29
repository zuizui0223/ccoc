"""A symbolic continuous-space RACH example without enumerating candidates.

The candidate space is theta in R and the focal motif is theta > 0. An external
solver is represented only by its feasibility certificates for the retained
interval. The example does not call a solver or read data.

Run:
    python examples/symbolic_candidate_set_lifting.py
"""

from causal_model import (
    FeasibilityCertificate,
    FeasibilityStatus,
    SolverSemanticValidityCertificate,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    SymbolicJointCoverageCertificate,
    SymbolicMotifQueries,
    classify_symbolic_candidate_sets,
    symbolic_soundness_guarantee,
)


SPACE = SymbolicCandidateSpace(
    space_description="theta in the real line",
    motifs=("positive",),
)


def certificate(query: str, status: FeasibilityStatus) -> FeasibilityCertificate:
    return FeasibilityCertificate(
        query_description=query,
        status=status,
        evidence_reference=f"proof://interval/{query}" if status is not FeasibilityStatus.UNKNOWN else "",
        solver="external interval proof backend",
    )


def main() -> None:
    # Retained set: theta in [0.2, 1]. The active subset is feasible and the
    # inactive subset theta <= 0 is certified empty.
    interval = SymbolicConfidenceSetCell(
        cell_id="primary",
        description="retained interval theta in [0.2, 1]",
        motif_queries={
            "positive": SymbolicMotifQueries(
                nonempty=certificate("theta in [0.2, 1]", FeasibilityStatus.SAT),
                active=certificate("theta in [0.2, 1] and theta > 0", FeasibilityStatus.SAT),
                inactive=certificate("theta in [0.2, 1] and theta <= 0", FeasibilityStatus.UNSAT),
            )
        },
    )
    report = classify_symbolic_candidate_sets(SPACE, (interval,))
    guarantee = symbolic_soundness_guarantee(
        SPACE,
        SymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("primary",),
            lower_bound=0.95,
            method="external arbitrary-data confidence region",
        ),
        SolverSemanticValidityCertificate(
            required_cell_ids=("primary",),
            motifs=("positive",),
            lower_bound=1.0,
            method="proof-carrying interval backend with trusted verifier",
        ),
    )

    print("symbolic status:", report.classifications["positive"].status.value)
    print("false-decisive upper bound:", guarantee.family_wise_false_decisive_upper_bound)


if __name__ == "__main__":
    main()
