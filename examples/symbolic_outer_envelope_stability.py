"""Minimal symbolic outer-envelope stability audit.

The inner retained set admits only focal-active candidates. The outer envelope
also admits a focal-inactive competitor. A joint inclusion certificate lets RACH
classify the narrow invariant as scope-fragile rather than extension-stable.

Run:
    python examples/symbolic_outer_envelope_stability.py
"""

from causal_model.admissibility import CoverageMode
from causal_model.symbolic_candidate_sets import (
    FeasibilityCertificate,
    FeasibilityStatus,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    SymbolicMotifQueries,
)
from causal_model.symbolic_universe_extension import (
    JointSymbolicInclusionCertificate,
    SymbolicUniverseTier,
    audit_symbolic_universe_extension,
)


def certificate(label: str, status: FeasibilityStatus) -> FeasibilityCertificate:
    return FeasibilityCertificate(
        query_description=label,
        status=status,
        evidence_reference=f"proof://{label}",
        solver="external symbolic backend",
    )


def tier(tier_id: str, inactive_status: FeasibilityStatus, space: SymbolicCandidateSpace) -> SymbolicUniverseTier:
    return SymbolicUniverseTier(
        tier_id=tier_id,
        space=space,
        cells=(
            SymbolicConfidenceSetCell(
                cell_id="primary",
                description=f"{tier_id} symbolic retained set",
                motif_queries={
                    "focal": SymbolicMotifQueries(
                        nonempty=certificate(f"{tier_id}/nonempty", FeasibilityStatus.SAT),
                        active=certificate(f"{tier_id}/active", FeasibilityStatus.SAT),
                        inactive=certificate(f"{tier_id}/inactive", inactive_status),
                    )
                },
                coverage_mode=CoverageMode.SOLVER_BACKED,
            ),
        ),
    )


def main() -> None:
    space = SymbolicCandidateSpace("theta in an arbitrary continuous space", ("focal",))
    inner = tier("inner", FeasibilityStatus.UNSAT, space)
    outer = tier("outer-envelope", FeasibilityStatus.SAT, space)
    report = audit_symbolic_universe_extension(
        inner,
        outer,
        JointSymbolicInclusionCertificate(
            inner_tier_id="inner",
            outer_tier_id="outer-envelope",
            required_cell_ids=("primary",),
            lower_bound=1.0,
            method="proof-carrying inclusion verifier",
            evidence_reference="proof://inner-subset-outer",
        ),
    )
    audit = report.motifs["focal"]
    print("inner:", audit.inner_status.value)
    print("outer:", audit.outer_status.value)
    print("extension status:", audit.extension_status.value)


if __name__ == "__main__":
    main()
