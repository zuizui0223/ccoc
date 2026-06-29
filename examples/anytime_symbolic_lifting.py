"""Minimal all-look symbolic RACH example without raw data or solver search.

At the first look, both focal values remain feasible and the status is
UNRESOLVED. At the second look, the inactive subset has a verified UNSAT
certificate and the status becomes INVARIANT. The theorem treats this conclusion
as optional-stopping safe only under external all-look coverage and all-look
solver-semantic-validity certificates.

Run:
    python examples/anytime_symbolic_lifting.py
"""

from causal_model.admissibility import CoverageMode
from causal_model.anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
    SequentialSymbolicConfidenceSetSnapshot,
    anytime_symbolic_soundness_guarantee,
    deterministic_anytime_symbolic_lifting_witness,
)
from causal_model.symbolic_candidate_sets import (
    FeasibilityCertificate,
    FeasibilityStatus,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    SymbolicMotifQueries,
)


def certificate(label: str, status: FeasibilityStatus) -> FeasibilityCertificate:
    return FeasibilityCertificate(
        query_description=label,
        status=status,
        evidence_reference=f"proof://{label}" if status is not FeasibilityStatus.UNKNOWN else "",
        solver="external proof backend",
    )


def snapshot(look: int, inactive: FeasibilityStatus) -> SequentialSymbolicConfidenceSetSnapshot:
    return SequentialSymbolicConfidenceSetSnapshot(
        look=look,
        cells=(
            SymbolicConfidenceSetCell(
                cell_id="primary",
                description="generic symbolic retained set",
                motif_queries={
                    "focal": SymbolicMotifQueries(
                        nonempty=certificate(f"{look}/nonempty", FeasibilityStatus.SAT),
                        active=certificate(f"{look}/active", FeasibilityStatus.SAT),
                        inactive=certificate(f"{look}/inactive", inactive),
                    )
                },
                coverage_mode=CoverageMode.SOLVER_BACKED,
            ),
        ),
    )


def main() -> None:
    space = SymbolicCandidateSpace("arbitrary candidate space", ("focal",))
    coverage = AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external arbitrary-data confidence sequence",
    )
    solver = AnytimeSolverSemanticValidityCertificate(
        required_cell_ids=("primary",),
        motifs=("focal",),
        lower_bound=1.0,
        method="proof-carrying solver verifier",
    )
    trajectory = (
        snapshot(1, FeasibilityStatus.SAT),
        snapshot(2, FeasibilityStatus.UNSAT),
    )
    witness = deterministic_anytime_symbolic_lifting_witness(
        space,
        trajectory,
        true_candidate_label="theta_star",
        true_active_motifs=frozenset({"focal"}),
        true_retained_by_look={1: True, 2: True},
        decisive_solver_semantics_valid_by_look={1: True, 2: True},
        coverage_certificate=coverage,
        solver_certificate=solver,
    )
    guarantee = anytime_symbolic_soundness_guarantee(space, coverage, solver)

    print("false-decisive looks:", witness.false_decisive_looks)
    print("anytime false-decisive upper bound:", guarantee.time_uniform_family_wise_false_decisive_upper_bound)


if __name__ == "__main__":
    main()
