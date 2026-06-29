from math import isclose

import pytest

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


SPACE = SymbolicCandidateSpace(
    space_description="arbitrary possibly uncountable candidate space",
    motifs=("focal",),
)


def certificate(label: str, status: FeasibilityStatus) -> FeasibilityCertificate:
    return FeasibilityCertificate(
        query_description=label,
        status=status,
        evidence_reference=f"proof://{label}" if status is not FeasibilityStatus.UNKNOWN else "",
        solver="illustrative proof backend",
    )


def cell(cell_id: str, active: FeasibilityStatus, inactive: FeasibilityStatus) -> SymbolicConfidenceSetCell:
    return SymbolicConfidenceSetCell(
        cell_id=cell_id,
        description=f"symbolic cell {cell_id}",
        motif_queries={
            "focal": SymbolicMotifQueries(
                nonempty=certificate(f"{cell_id}/nonempty", FeasibilityStatus.SAT),
                active=certificate(f"{cell_id}/active", active),
                inactive=certificate(f"{cell_id}/inactive", inactive),
            )
        },
        coverage_mode=CoverageMode.SOLVER_BACKED,
    )


def snapshot(look: int, active: FeasibilityStatus, inactive: FeasibilityStatus) -> SequentialSymbolicConfidenceSetSnapshot:
    return SequentialSymbolicConfidenceSetSnapshot(
        look=look,
        cells=(cell("primary", active, inactive),),
    )


def certificates(
    *,
    coverage: float = 0.95,
    solver: float = 0.98,
    coverage_looks=None,
    solver_looks=None,
):
    return (
        AnytimeSymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("primary",),
            lower_bound=coverage,
            method="external time-uniform arbitrary-data confidence region",
            certified_looks=coverage_looks,
        ),
        AnytimeSolverSemanticValidityCertificate(
            required_cell_ids=("primary",),
            motifs=("focal",),
            lower_bound=solver,
            method="external time-uniform solver certificate audit",
            certified_looks=solver_looks,
        ),
    )


def test_time_uniform_symbolic_guarantee_combines_alpha_and_beta_without_independence() -> None:
    coverage_certificate, solver_certificate = certificates()
    guarantee = anytime_symbolic_soundness_guarantee(
        SPACE,
        coverage_certificate,
        solver_certificate,
    )

    assert guarantee.certified_looks is None
    assert isclose(guarantee.statistical_miscoverage_upper_bound, 0.05)
    assert isclose(guarantee.solver_semantic_failure_upper_bound, 0.02)
    assert isclose(guarantee.time_uniform_family_wise_false_decisive_upper_bound, 0.07)
    assert isclose(guarantee.stopping_time_false_decisive_upper_bound, 0.07)


def test_all_look_good_event_allows_unresolved_then_correct_invariant() -> None:
    coverage_certificate, solver_certificate = certificates()
    witness = deterministic_anytime_symbolic_lifting_witness(
        SPACE,
        (
            snapshot(1, FeasibilityStatus.SAT, FeasibilityStatus.SAT),
            snapshot(2, FeasibilityStatus.SAT, FeasibilityStatus.UNSAT),
        ),
        true_candidate_label="theta_star",
        true_active_motifs=frozenset({"focal"}),
        true_retained_by_look={1: True, 2: True},
        decisive_solver_semantics_valid_by_look={1: True, 2: True},
        coverage_certificate=coverage_certificate,
        solver_certificate=solver_certificate,
    )

    assert witness.joint_good_event_at_all_looks
    assert witness.false_decisive_looks == ()


def test_false_exclusion_requires_loss_of_retention_or_solver_semantics() -> None:
    coverage_certificate, solver_certificate = certificates()
    witness = deterministic_anytime_symbolic_lifting_witness(
        SPACE,
        (
            snapshot(1, FeasibilityStatus.SAT, FeasibilityStatus.SAT),
            snapshot(2, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT),
        ),
        true_candidate_label="theta_star",
        true_active_motifs=frozenset({"focal"}),
        true_retained_by_look={1: True, 2: False},
        decisive_solver_semantics_valid_by_look={1: True, 2: True},
        coverage_certificate=coverage_certificate,
        solver_certificate=solver_certificate,
    )

    assert witness.false_decisive_looks == (2,)
    assert witness.implication_holds


def test_false_exclusion_under_the_all_look_good_event_is_rejected_as_contradictory() -> None:
    coverage_certificate, solver_certificate = certificates()
    with pytest.raises(RuntimeError, match="implication was violated"):
        deterministic_anytime_symbolic_lifting_witness(
            SPACE,
            (
                snapshot(1, FeasibilityStatus.SAT, FeasibilityStatus.SAT),
                snapshot(2, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT),
            ),
            true_candidate_label="theta_star",
            true_active_motifs=frozenset({"focal"}),
            true_retained_by_look={1: True, 2: True},
            decisive_solver_semantics_valid_by_look={1: True, 2: True},
            coverage_certificate=coverage_certificate,
            solver_certificate=solver_certificate,
        )


def test_all_look_coverage_combines_with_a_finite_solver_scope() -> None:
    coverage_certificate, solver_certificate = certificates(solver_looks=(1, 2))
    guarantee = anytime_symbolic_soundness_guarantee(
        SPACE,
        coverage_certificate,
        solver_certificate,
    )

    assert guarantee.certified_looks == (1, 2)


def test_snapshot_outside_finite_solver_scope_is_rejected() -> None:
    coverage_certificate, solver_certificate = certificates(solver_looks=(1, 2))
    with pytest.raises(ValueError, match="outside the solver certificate's declared scope"):
        deterministic_anytime_symbolic_lifting_witness(
            SPACE,
            (
                snapshot(1, FeasibilityStatus.SAT, FeasibilityStatus.SAT),
                snapshot(3, FeasibilityStatus.SAT, FeasibilityStatus.UNSAT),
            ),
            true_candidate_label="theta_star",
            true_active_motifs=frozenset({"focal"}),
            true_retained_by_look={1: True, 3: True},
            decisive_solver_semantics_valid_by_look={1: True, 3: True},
            coverage_certificate=coverage_certificate,
            solver_certificate=solver_certificate,
        )


def test_mismatched_finite_certificate_scopes_are_rejected() -> None:
    coverage_certificate, solver_certificate = certificates(coverage_looks=(1, 2), solver_looks=(1, 3))
    with pytest.raises(ValueError, match="same finite look scope"):
        anytime_symbolic_soundness_guarantee(
            SPACE,
            coverage_certificate,
            solver_certificate,
        )


def test_proof_carrying_solver_recovers_the_anytime_coverage_bound() -> None:
    coverage_certificate, solver_certificate = certificates(solver=1.0)
    guarantee = anytime_symbolic_soundness_guarantee(
        SPACE,
        coverage_certificate,
        solver_certificate,
    )

    assert isclose(guarantee.time_uniform_family_wise_false_decisive_upper_bound, 0.05)
