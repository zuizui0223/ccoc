from math import isclose

import pytest

from causal_model import (
    ClaimCoverage,
    CoverageMode,
    FeasibilityCertificate,
    FeasibilityStatus,
    MotifStatus,
    SolverSemanticValidityCertificate,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    SymbolicJointCoverageCertificate,
    SymbolicMotifQueries,
    classify_symbolic_candidate_sets,
    symbolic_soundness_guarantee,
)


SPACE = SymbolicCandidateSpace(
    space_description="real-valued theta with no finite enumeration",
    motifs=("positive",),
)


def query(label: str, status: FeasibilityStatus) -> FeasibilityCertificate:
    return FeasibilityCertificate(
        query_description=label,
        status=status,
        evidence_reference="artifact://" + label if status is not FeasibilityStatus.UNKNOWN else "",
        solver="illustrative constraint solver",
    )


def bundle(
    nonempty: FeasibilityStatus,
    active: FeasibilityStatus,
    inactive: FeasibilityStatus,
) -> SymbolicMotifQueries:
    return SymbolicMotifQueries(
        nonempty=query("retained", nonempty),
        active=query("retained_and_positive", active),
        inactive=query("retained_and_not_positive", inactive),
    )


def cell(
    cell_id: str,
    queries: SymbolicMotifQueries,
    *,
    coverage_mode: CoverageMode = CoverageMode.SOLVER_BACKED,
) -> SymbolicConfidenceSetCell:
    return SymbolicConfidenceSetCell(
        cell_id=cell_id,
        description=f"symbolic retained set for {cell_id}",
        motif_queries={"positive": queries},
        coverage_mode=coverage_mode,
    )


def test_solver_certified_unsat_classifies_an_invariant_without_enumeration() -> None:
    report = classify_symbolic_candidate_sets(
        SPACE,
        (
            cell(
                "interval",
                bundle(
                    FeasibilityStatus.SAT,
                    FeasibilityStatus.SAT,
                    FeasibilityStatus.UNSAT,
                ),
            ),
        ),
    )

    classification = report.classifications["positive"]
    assert classification.status is MotifStatus.INVARIANT
    assert classification.claim_coverage is ClaimCoverage.COMPLETE


def test_solver_certified_active_and_inactive_witnesses_are_unresolved() -> None:
    report = classify_symbolic_candidate_sets(
        SPACE,
        (
            cell(
                "straddling_interval",
                bundle(
                    FeasibilityStatus.SAT,
                    FeasibilityStatus.SAT,
                    FeasibilityStatus.SAT,
                ),
            ),
        ),
    )

    assert report.classifications["positive"].status is MotifStatus.UNRESOLVED


def test_unknown_solver_answer_is_unsupported_not_unresolved() -> None:
    report = classify_symbolic_candidate_sets(
        SPACE,
        (
            cell(
                "solver_timeout",
                bundle(
                    FeasibilityStatus.SAT,
                    FeasibilityStatus.SAT,
                    FeasibilityStatus.UNKNOWN,
                ),
            ),
        ),
    )

    classification = report.classifications["positive"]
    assert classification.status is MotifStatus.UNSUPPORTED
    assert classification.unsupported_required_cells == ("solver_timeout",)


def test_sampled_symbolic_cell_keeps_claim_coverage_sampled() -> None:
    report = classify_symbolic_candidate_sets(
        SPACE,
        (
            cell(
                "sampled_constraint_family",
                bundle(
                    FeasibilityStatus.SAT,
                    FeasibilityStatus.SAT,
                    FeasibilityStatus.UNSAT,
                ),
                coverage_mode=CoverageMode.SAMPLED,
            ),
        ),
    )

    assert report.classifications["positive"].claim_coverage is ClaimCoverage.SAMPLED


def test_combined_statistical_and_solver_error_needs_no_independence() -> None:
    guarantee = symbolic_soundness_guarantee(
        SPACE,
        SymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("interval",),
            lower_bound=0.95,
            method="external arbitrary-data confidence region",
        ),
        SolverSemanticValidityCertificate(
            required_cell_ids=("interval",),
            motifs=("positive",),
            lower_bound=0.98,
            method="externally audited randomized solver",
        ),
    )

    assert isclose(guarantee.statistical_miscoverage_upper_bound, 0.05)
    assert isclose(guarantee.solver_semantic_failure_upper_bound, 0.02)
    assert isclose(guarantee.family_wise_false_decisive_upper_bound, 0.07)


def test_proof_carrying_solver_recovers_ordinary_coverage_bound() -> None:
    guarantee = symbolic_soundness_guarantee(
        SPACE,
        SymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("interval",),
            lower_bound=0.95,
            method="external confidence region",
        ),
        SolverSemanticValidityCertificate(
            required_cell_ids=("interval",),
            motifs=("positive",),
            lower_bound=1.0,
            method="proof-carrying solver with trusted verifier",
        ),
    )

    assert isclose(guarantee.family_wise_false_decisive_upper_bound, 0.05)


def test_inconsistent_nonempty_and_motif_answers_are_rejected() -> None:
    with pytest.raises(ValueError, match="cannot exclude both motif values"):
        bundle(
            FeasibilityStatus.SAT,
            FeasibilityStatus.UNSAT,
            FeasibilityStatus.UNSAT,
        )


def test_mismatched_solver_certificate_target_is_rejected() -> None:
    with pytest.raises(ValueError, match="same required cell IDs"):
        symbolic_soundness_guarantee(
            SPACE,
            SymbolicJointCoverageCertificate(
                true_candidate_label="theta_star",
                required_cell_ids=("left",),
                lower_bound=0.95,
                method="external confidence region",
            ),
            SolverSemanticValidityCertificate(
                required_cell_ids=("right",),
                motifs=("positive",),
                lower_bound=1.0,
                method="proof-carrying solver",
            ),
        )
