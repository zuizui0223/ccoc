from math import isclose

import pytest

from causal_model.admissibility import CoverageMode, MotifStatus
from causal_model.anytime_symbolic_extension_stability import (
    AnytimeJointSymbolicInclusionCertificate,
    AnytimeSymbolicExtensionTarget,
    SequentialSymbolicUniverseExtensionSnapshot,
    anytime_symbolic_extension_stability_guarantee,
    audit_anytime_symbolic_universe_extension,
    deterministic_anytime_symbolic_extension_stability_witness,
)
from causal_model.anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
)
from causal_model.symbolic_candidate_sets import (
    FeasibilityCertificate,
    FeasibilityStatus,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    SymbolicMotifQueries,
)
from causal_model.symbolic_universe_extension import (
    ExtensionStatus,
    SymbolicUniverseTier,
)


SPACE = SymbolicCandidateSpace("arbitrary continuous candidate space", ("focal",))


def certificate(label: str, status: FeasibilityStatus) -> FeasibilityCertificate:
    return FeasibilityCertificate(
        query_description=label,
        status=status,
        evidence_reference=f"proof://{label}" if status is not FeasibilityStatus.UNKNOWN else "",
        solver="illustrative backend",
    )


def tier(tier_id: str, look: int, active: FeasibilityStatus, inactive: FeasibilityStatus) -> SymbolicUniverseTier:
    return SymbolicUniverseTier(
        tier_id=tier_id,
        space=SPACE,
        cells=(
            SymbolicConfidenceSetCell(
                cell_id="primary",
                description=f"{tier_id} at look {look}",
                motif_queries={
                    "focal": SymbolicMotifQueries(
                        nonempty=certificate(f"{tier_id}/{look}/nonempty", FeasibilityStatus.SAT),
                        active=certificate(f"{tier_id}/{look}/active", active),
                        inactive=certificate(f"{tier_id}/{look}/inactive", inactive),
                    )
                },
                coverage_mode=CoverageMode.SOLVER_BACKED,
            ),
        ),
    )


def snapshot(look: int, inner_inactive: FeasibilityStatus, outer_active: FeasibilityStatus, outer_inactive: FeasibilityStatus) -> SequentialSymbolicUniverseExtensionSnapshot:
    return SequentialSymbolicUniverseExtensionSnapshot(
        look=look,
        inner=tier("inner", look, FeasibilityStatus.SAT, inner_inactive),
        outer=tier("outer", look, outer_active, outer_inactive),
    )


def certificates(*, coverage=0.95, solver=0.98, inclusion=0.97, coverage_looks=None, solver_looks=None, inclusion_looks=None):
    return (
        AnytimeSymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("primary",),
            lower_bound=coverage,
            method="external confidence sequence",
            certified_looks=coverage_looks,
        ),
        AnytimeSolverSemanticValidityCertificate(
            required_cell_ids=("primary",),
            motifs=("focal",),
            lower_bound=solver,
            method="external all-look solver audit",
            certified_looks=solver_looks,
        ),
        AnytimeJointSymbolicInclusionCertificate(
            inner_tier_id="inner",
            outer_tier_id="outer",
            required_cell_ids=("primary",),
            lower_bound=inclusion,
            method="external all-look inclusion proof",
            evidence_reference="proof://inner-subset-outer",
            certified_looks=inclusion_looks,
        ),
    )


def target() -> AnytimeSymbolicExtensionTarget:
    return AnytimeSymbolicExtensionTarget(
        inner_tier_id="inner",
        outer_tier_id="outer",
        space=SPACE,
        required_cell_ids=("primary",),
    )


def test_anytime_bound_combines_alpha_beta_gamma_without_independence():
    coverage, solver, inclusion = certificates()
    guarantee = anytime_symbolic_extension_stability_guarantee(
        target=target(),
        coverage_certificate=coverage,
        solver_certificate=solver,
        inclusion_certificate=inclusion,
    )

    assert guarantee.certified_looks is None
    assert isclose(guarantee.statistical_miscoverage_upper_bound, 0.05)
    assert isclose(guarantee.solver_semantic_failure_upper_bound, 0.02)
    assert isclose(guarantee.inclusion_failure_upper_bound, 0.03)
    assert isclose(guarantee.time_uniform_false_decisive_or_invalid_stability_upper_bound, 0.10)
    assert isclose(guarantee.stopping_time_false_decisive_or_invalid_stability_upper_bound, 0.10)


def test_all_good_trajectory_can_be_fragile_then_extension_stable():
    coverage, solver, inclusion = certificates()
    trajectory = (
        snapshot(1, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT, FeasibilityStatus.SAT),
        snapshot(2, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT, FeasibilityStatus.UNSAT),
    )
    report = audit_anytime_symbolic_universe_extension(
        trajectory,
        inclusion_certificate=inclusion,
        coverage_certificate=coverage,
        solver_certificate=solver,
    )
    assert report.reports_by_look[1].motifs["focal"].extension_status is ExtensionStatus.SCOPE_FRAGILE
    assert report.reports_by_look[2].motifs["focal"].extension_status is ExtensionStatus.EXTENSION_STABLE

    witness = deterministic_anytime_symbolic_extension_stability_witness(
        trajectory,
        inclusion_certificate=inclusion,
        coverage_certificate=coverage,
        solver_certificate=solver,
        true_active_motifs=frozenset({"focal"}),
        outer_true_retained_by_look={1: True, 2: True},
        outer_solver_semantics_valid_by_look={1: True, 2: True},
        inclusion_valid_by_look={1: True, 2: True},
    )
    assert witness.joint_good_event_at_all_looks
    assert witness.false_or_invalid_looks == ()


def test_false_outer_exclusion_requires_failure_of_one_global_event():
    coverage, solver, inclusion = certificates()
    trajectory = (
        snapshot(1, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT, FeasibilityStatus.UNSAT),
        snapshot(2, FeasibilityStatus.UNSAT, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT),
    )
    witness = deterministic_anytime_symbolic_extension_stability_witness(
        trajectory,
        inclusion_certificate=inclusion,
        coverage_certificate=coverage,
        solver_certificate=solver,
        true_active_motifs=frozenset({"focal"}),
        outer_true_retained_by_look={1: True, 2: False},
        outer_solver_semantics_valid_by_look={1: True, 2: True},
        inclusion_valid_by_look={1: True, 2: True},
    )

    assert witness.false_decisive_outer_motifs_by_look[2] == ("focal",)
    assert witness.implication_holds


def test_false_outer_exclusion_under_all_good_events_is_rejected():
    coverage, solver, inclusion = certificates()
    with pytest.raises(RuntimeError, match="implication was violated"):
        deterministic_anytime_symbolic_extension_stability_witness(
            (
                snapshot(1, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT, FeasibilityStatus.UNSAT),
                snapshot(2, FeasibilityStatus.UNSAT, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT),
            ),
            inclusion_certificate=inclusion,
            coverage_certificate=coverage,
            solver_certificate=solver,
            true_active_motifs=frozenset({"focal"}),
            outer_true_retained_by_look={1: True, 2: True},
            outer_solver_semantics_valid_by_look={1: True, 2: True},
            inclusion_valid_by_look={1: True, 2: True},
        )


def test_inclusion_failure_invalidates_extension_stability_claim():
    coverage, solver, inclusion = certificates()
    trajectory = (
        snapshot(1, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT, FeasibilityStatus.UNSAT),
        snapshot(2, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT, FeasibilityStatus.UNSAT),
    )
    witness = deterministic_anytime_symbolic_extension_stability_witness(
        trajectory,
        inclusion_certificate=inclusion,
        coverage_certificate=coverage,
        solver_certificate=solver,
        true_active_motifs=frozenset({"focal"}),
        outer_true_retained_by_look={1: True, 2: True},
        outer_solver_semantics_valid_by_look={1: True, 2: True},
        inclusion_valid_by_look={1: True, 2: False},
    )

    assert witness.invalid_extension_stability_motifs_by_look[2] == ("focal",)
    assert witness.implication_holds


def test_finite_scope_cannot_be_silently_extended_by_optional_stopping():
    coverage, solver, inclusion = certificates(inclusion_looks=(1, 2))
    guarantee = anytime_symbolic_extension_stability_guarantee(
        target=target(),
        coverage_certificate=coverage,
        solver_certificate=solver,
        inclusion_certificate=inclusion,
    )
    assert guarantee.certified_looks == (1, 2)

    with pytest.raises(ValueError, match="outside the inclusion certificate's declared scope"):
        audit_anytime_symbolic_universe_extension(
            (
                snapshot(1, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT, FeasibilityStatus.UNSAT),
                snapshot(3, FeasibilityStatus.UNSAT, FeasibilityStatus.SAT, FeasibilityStatus.UNSAT),
            ),
            inclusion_certificate=inclusion,
            coverage_certificate=coverage,
            solver_certificate=solver,
        )


def test_mismatched_finite_look_scopes_are_rejected():
    coverage, solver, inclusion = certificates(coverage_looks=(1, 2), solver_looks=(1, 3), inclusion_looks=(1, 2))
    with pytest.raises(ValueError, match="same finite look scope"):
        anytime_symbolic_extension_stability_guarantee(
            target=target(),
            coverage_certificate=coverage,
            solver_certificate=solver,
            inclusion_certificate=inclusion,
        )


def test_proof_carrying_outer_and_inclusion_verifiers_recover_alpha():
    coverage, solver, inclusion = certificates(solver=1.0, inclusion=1.0)
    guarantee = anytime_symbolic_extension_stability_guarantee(
        target=target(),
        coverage_certificate=coverage,
        solver_certificate=solver,
        inclusion_certificate=inclusion,
    )
    assert isclose(guarantee.time_uniform_false_decisive_or_invalid_stability_upper_bound, 0.05)
