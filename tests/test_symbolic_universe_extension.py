from math import isclose

import pytest

from causal_model.admissibility import CoverageMode, MotifStatus
from causal_model.symbolic_candidate_sets import (
    FeasibilityCertificate,
    FeasibilityStatus,
    SolverSemanticValidityCertificate,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    SymbolicJointCoverageCertificate,
    SymbolicMotifQueries,
)
from causal_model.symbolic_universe_extension import (
    ExtensionStatus,
    JointSymbolicInclusionCertificate,
    SymbolicUniverseTier,
    audit_symbolic_universe_extension,
    symbolic_extension_stability_guarantee,
)


SPACE = SymbolicCandidateSpace("theta in an arbitrary continuous space", ("focal",))


def certificate(label, status):
    return FeasibilityCertificate(
        query_description=label,
        status=status,
        evidence_reference=f"proof://{label}" if status is not FeasibilityStatus.UNKNOWN else "",
        solver="illustrative solver",
    )


def tier(tier_id, *, active, inactive):
    return SymbolicUniverseTier(
        tier_id=tier_id,
        space=SPACE,
        cells=(
            SymbolicConfidenceSetCell(
                cell_id="primary",
                description=f"{tier_id} retained set",
                motif_queries={
                    "focal": SymbolicMotifQueries(
                        nonempty=certificate(f"{tier_id}/nonempty", FeasibilityStatus.SAT),
                        active=certificate(f"{tier_id}/active", active),
                        inactive=certificate(f"{tier_id}/inactive", inactive),
                    )
                },
                coverage_mode=CoverageMode.SOLVER_BACKED,
            ),
        ),
    )


def inclusion(inner, outer, *, lower_bound=1.0):
    return JointSymbolicInclusionCertificate(
        inner_tier_id=inner.tier_id,
        outer_tier_id=outer.tier_id,
        required_cell_ids=("primary",),
        lower_bound=lower_bound,
        method="external joint symbolic inclusion verifier",
        evidence_reference="proof://inner-subset-outer",
    )


def test_inner_invariant_becomes_scope_fragile_when_outer_adds_an_inactive_competitor():
    inner = tier("inner", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    outer = tier("outer", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.SAT)
    report = audit_symbolic_universe_extension(inner, outer, inclusion(inner, outer))

    audit = report.motifs["focal"]
    assert audit.inner_status is MotifStatus.INVARIANT
    assert audit.outer_status is MotifStatus.UNRESOLVED
    assert audit.extension_status is ExtensionStatus.SCOPE_FRAGILE
    assert report.scope_fragile_motifs == ("focal",)


def test_outer_decisive_result_is_extension_stable_when_inner_matches():
    inner = tier("inner", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    outer = tier("outer", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    report = audit_symbolic_universe_extension(inner, outer, inclusion(inner, outer))

    audit = report.motifs["focal"]
    assert audit.extension_status is ExtensionStatus.EXTENSION_STABLE
    assert report.extension_stable_motifs == ("focal",)


def test_missing_inclusion_certificate_makes_stability_unsupported():
    inner = tier("inner", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    outer = tier("outer", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    report = audit_symbolic_universe_extension(inner, outer, None)

    assert report.inclusion_certified is False
    assert report.motifs["focal"].extension_status is ExtensionStatus.UNSUPPORTED
    assert report.unsupported_stability_motifs == ("focal",)


def test_conflicting_outer_decisive_status_is_unsupported_under_claimed_inclusion():
    inner = tier("inner", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    outer = tier("outer", active=FeasibilityStatus.UNSAT, inactive=FeasibilityStatus.SAT)
    report = audit_symbolic_universe_extension(inner, outer, inclusion(inner, outer))

    assert report.motifs["focal"].extension_status is ExtensionStatus.UNSUPPORTED
    assert "conflicts" in report.motifs["focal"].reason


def test_inclusion_certificate_must_target_the_exact_tiers_and_cells():
    inner = tier("inner", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    outer = tier("outer", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    wrong = JointSymbolicInclusionCertificate(
        inner_tier_id="different",
        outer_tier_id="outer",
        required_cell_ids=("primary",),
        lower_bound=1.0,
        method="verifier",
        evidence_reference="proof://wrong",
    )
    with pytest.raises(ValueError, match="inner tier ID"):
        audit_symbolic_universe_extension(inner, outer, wrong)


def test_outer_soundness_and_inclusion_risk_combine_without_independence():
    inner = tier("inner", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    outer = tier("outer", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    guarantee = symbolic_extension_stability_guarantee(
        outer=outer,
        outer_coverage_certificate=SymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("primary",),
            lower_bound=0.95,
            method="external confidence region",
        ),
        outer_solver_certificate=SolverSemanticValidityCertificate(
            required_cell_ids=("primary",),
            motifs=("focal",),
            lower_bound=0.98,
            method="external solver audit",
        ),
        inclusion_certificate=inclusion(inner, outer, lower_bound=0.97),
    )

    assert isclose(guarantee.statistical_miscoverage_upper_bound, 0.05)
    assert isclose(guarantee.solver_semantic_failure_upper_bound, 0.02)
    assert isclose(guarantee.inclusion_failure_upper_bound, 0.03)
    assert isclose(guarantee.false_decisive_or_false_stability_upper_bound, 0.10)


def test_proof_carrying_inclusion_recovers_alpha_plus_beta_bound():
    inner = tier("inner", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    outer = tier("outer", active=FeasibilityStatus.SAT, inactive=FeasibilityStatus.UNSAT)
    guarantee = symbolic_extension_stability_guarantee(
        outer=outer,
        outer_coverage_certificate=SymbolicJointCoverageCertificate(
            true_candidate_label="theta_star",
            required_cell_ids=("primary",),
            lower_bound=0.95,
            method="external confidence region",
        ),
        outer_solver_certificate=SolverSemanticValidityCertificate(
            required_cell_ids=("primary",),
            motifs=("focal",),
            lower_bound=1.0,
            method="proof-carrying solver verifier",
        ),
        inclusion_certificate=inclusion(inner, outer, lower_bound=1.0),
    )

    assert isclose(guarantee.false_decisive_or_false_stability_upper_bound, 0.05)
