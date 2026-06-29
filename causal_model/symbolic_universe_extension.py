"""Outer-envelope stability for symbolic and continuous RACH candidate spaces.

The finite nested-universe audit checks explicit set inclusion.  This module
extends the same logic to solver-defined candidate spaces, where retained sets
may be continuous, mixed, countably infinite, or uncountable.  Inclusion is not
assumed from names or descriptions: an external joint inclusion certificate must
cover every required cell.

For retained sets ``C_inner,r`` and ``C_outer,r`` with
``C_inner,r subseteq C_outer,r`` in every required cell, ordinary symbolic RACH
classification is monotone:

* outer INVARIANT implies inner INVARIANT;
* outer EXCLUDED implies inner EXCLUDED; and
* inner UNRESOLVED implies outer UNRESOLVED.

The module records whether an outer decisive conclusion is extension-stable,
scope-fragile under a declared expansion, non-decisive, or unsupported because
inclusion or symbolic classification is not certified.  It does not prove that
the outer envelope contains nature.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from .admissibility import MotifStatus
from .symbolic_candidate_sets import (
    SymbolicAdmissibilityReport,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    SymbolicJointCoverageCertificate,
    SolverSemanticValidityCertificate,
    classify_symbolic_candidate_sets,
)


def _unit_interval(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")


class ExtensionStatus(str, Enum):
    """Scope-robustness label for one motif across an inner/outer expansion."""

    EXTENSION_STABLE = "extension-stable"
    SCOPE_FRAGILE = "scope-fragile"
    NONDECISIVE = "nondecisive"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class SymbolicUniverseTier:
    """One symbolic retained-set tier for a common candidate space.

    The tier itself does not assert inclusion.  It supplies the same declared
    candidate space and a set of symbolic retained cells to an external
    inclusion-certificate layer.
    """

    tier_id: str
    space: SymbolicCandidateSpace
    cells: tuple[SymbolicConfidenceSetCell, ...]
    description: str = ""

    def __post_init__(self) -> None:
        if not self.tier_id:
            raise ValueError("tier_id must be non-empty")
        if not self.cells:
            raise ValueError("a symbolic universe tier needs at least one cell")
        cell_ids = [cell.cell_id for cell in self.cells]
        if len(set(cell_ids)) != len(cell_ids):
            raise ValueError("symbolic universe tier cell IDs must be unique")
        if not any(cell.required for cell in self.cells):
            raise ValueError("a symbolic universe tier needs at least one required cell")
        classify_symbolic_candidate_sets(self.space, self.cells)

    @property
    def required_cell_ids(self) -> tuple[str, ...]:
        return tuple(cell.cell_id for cell in self.cells if cell.required)

    @property
    def report(self) -> SymbolicAdmissibilityReport:
        return classify_symbolic_candidate_sets(self.space, self.cells)

    @property
    def statuses(self) -> Mapping[str, MotifStatus]:
        return {
            motif: self.report.classifications[motif].status
            for motif in self.space.motifs
        }


@dataclass(frozen=True)
class JointSymbolicInclusionCertificate:
    """External joint certificate that inner retained sets lie in outer sets.

    The intended event is

    ``for every required cell r, C_inner,r is a subset of C_outer,r``.

    The certificate's lower bound is a semantic-validity guarantee for that
    entire joint inclusion claim.  A deterministic proof-carrying verifier can
    use ``lower_bound=1.0``.  An approximate or randomized inclusion backend
    must state a lower value, introducing ``gamma = 1 - lower_bound`` into the
    extension-stability error bound.
    """

    inner_tier_id: str
    outer_tier_id: str
    required_cell_ids: tuple[str, ...]
    lower_bound: float
    method: str
    assumptions: tuple[str, ...] = ()
    evidence_reference: str = ""

    def __post_init__(self) -> None:
        if not self.inner_tier_id or not self.outer_tier_id:
            raise ValueError("inner_tier_id and outer_tier_id must be non-empty")
        if self.inner_tier_id == self.outer_tier_id:
            raise ValueError("inner and outer tier IDs must differ")
        if not self.required_cell_ids:
            raise ValueError("required_cell_ids must not be empty")
        if len(set(self.required_cell_ids)) != len(self.required_cell_ids):
            raise ValueError("required_cell_ids must be unique")
        _unit_interval(self.lower_bound, "lower_bound")
        if not self.method:
            raise ValueError("method must be non-empty")
        if self.lower_bound > 0.0 and not self.evidence_reference:
            raise ValueError("a nonzero inclusion guarantee needs an evidence_reference")

    @property
    def inclusion_failure_upper_bound(self) -> float:
        return 1.0 - self.lower_bound


@dataclass(frozen=True)
class SymbolicExtensionMotifAudit:
    """Inner/outer status and extension result for one motif."""

    motif: str
    inner_status: MotifStatus
    outer_status: MotifStatus
    extension_status: ExtensionStatus
    reason: str = ""


@dataclass(frozen=True)
class SymbolicUniverseExtensionReport:
    """Result of one solver-certified or unsupported symbolic expansion audit."""

    inner_tier_id: str
    outer_tier_id: str
    inclusion_certified: bool
    inclusion_failure_upper_bound: float | None
    motifs: Mapping[str, SymbolicExtensionMotifAudit]

    @property
    def extension_stable_motifs(self) -> tuple[str, ...]:
        return tuple(
            motif
            for motif, audit in self.motifs.items()
            if audit.extension_status is ExtensionStatus.EXTENSION_STABLE
        )

    @property
    def scope_fragile_motifs(self) -> tuple[str, ...]:
        return tuple(
            motif
            for motif, audit in self.motifs.items()
            if audit.extension_status is ExtensionStatus.SCOPE_FRAGILE
        )

    @property
    def unsupported_stability_motifs(self) -> tuple[str, ...]:
        return tuple(
            motif
            for motif, audit in self.motifs.items()
            if audit.extension_status is ExtensionStatus.UNSUPPORTED
        )


@dataclass(frozen=True)
class SymbolicExtensionStabilityGuarantee:
    """False-decisive-or-false-stability bound for an outer symbolic envelope."""

    outer_tier_id: str
    statistical_coverage_lower_bound: float
    solver_semantic_validity_lower_bound: float
    inclusion_validity_lower_bound: float
    statistical_miscoverage_upper_bound: float
    solver_semantic_failure_upper_bound: float
    inclusion_failure_upper_bound: float
    false_decisive_or_false_stability_upper_bound: float
    required_cell_ids: tuple[str, ...]
    motifs: tuple[str, ...]
    coverage_method: str
    solver_method: str
    inclusion_method: str
    assumptions: tuple[str, ...]


def _validate_same_target(inner: SymbolicUniverseTier, outer: SymbolicUniverseTier) -> None:
    if inner.space != outer.space:
        raise ValueError("inner and outer tiers must use the same symbolic candidate space")
    if inner.required_cell_ids != outer.required_cell_ids:
        raise ValueError("inner and outer tiers must use identical ordered required cell IDs")


def _validate_inclusion_certificate(
    inner: SymbolicUniverseTier,
    outer: SymbolicUniverseTier,
    certificate: JointSymbolicInclusionCertificate,
) -> None:
    _validate_same_target(inner, outer)
    if certificate.inner_tier_id != inner.tier_id:
        raise ValueError("inclusion certificate inner tier ID does not match")
    if certificate.outer_tier_id != outer.tier_id:
        raise ValueError("inclusion certificate outer tier ID does not match")
    if certificate.required_cell_ids != inner.required_cell_ids:
        raise ValueError("inclusion certificate required cell IDs do not match the tiers")


def _audit_motif(
    motif: str,
    inner_status: MotifStatus,
    outer_status: MotifStatus,
    *,
    inclusion_certified: bool,
) -> SymbolicExtensionMotifAudit:
    if not inclusion_certified:
        return SymbolicExtensionMotifAudit(
            motif,
            inner_status,
            outer_status,
            ExtensionStatus.UNSUPPORTED,
            "no joint inclusion certificate for this expansion",
        )
    if inner_status is MotifStatus.UNSUPPORTED or outer_status is MotifStatus.UNSUPPORTED:
        return SymbolicExtensionMotifAudit(
            motif,
            inner_status,
            outer_status,
            ExtensionStatus.UNSUPPORTED,
            "at least one tier has unsupported symbolic classification",
        )
    if outer_status in (MotifStatus.INVARIANT, MotifStatus.EXCLUDED):
        if inner_status is outer_status:
            return SymbolicExtensionMotifAudit(
                motif,
                inner_status,
                outer_status,
                ExtensionStatus.EXTENSION_STABLE,
            )
        return SymbolicExtensionMotifAudit(
            motif,
            inner_status,
            outer_status,
            ExtensionStatus.UNSUPPORTED,
            "outer decisive result conflicts with inner status under claimed inclusion",
        )
    if inner_status in (MotifStatus.INVARIANT, MotifStatus.EXCLUDED):
        return SymbolicExtensionMotifAudit(
            motif,
            inner_status,
            outer_status,
            ExtensionStatus.SCOPE_FRAGILE,
            "inner decisive result does not survive the declared outer envelope",
        )
    return SymbolicExtensionMotifAudit(
        motif,
        inner_status,
        outer_status,
        ExtensionStatus.NONDECISIVE,
    )


def audit_symbolic_universe_extension(
    inner: SymbolicUniverseTier,
    outer: SymbolicUniverseTier,
    inclusion_certificate: JointSymbolicInclusionCertificate | None,
) -> SymbolicUniverseExtensionReport:
    """Audit whether symbolic conclusions survive one outer-envelope expansion.

    Passing ``None`` deliberately produces `UNSUPPORTED` stability labels rather
    than assuming inclusion from tier names. With a certificate, the function
    validates only target identity and certificate scope; proof semantics belong
    to the external method named by the certificate.
    """

    _validate_same_target(inner, outer)
    if inclusion_certificate is not None:
        _validate_inclusion_certificate(inner, outer, inclusion_certificate)
    inner_statuses = inner.statuses
    outer_statuses = outer.statuses
    certified = inclusion_certificate is not None
    return SymbolicUniverseExtensionReport(
        inner_tier_id=inner.tier_id,
        outer_tier_id=outer.tier_id,
        inclusion_certified=certified,
        inclusion_failure_upper_bound=(
            inclusion_certificate.inclusion_failure_upper_bound
            if inclusion_certificate is not None
            else None
        ),
        motifs={
            motif: _audit_motif(
                motif,
                inner_statuses[motif],
                outer_statuses[motif],
                inclusion_certified=certified,
            )
            for motif in inner.space.motifs
        },
    )


def symbolic_extension_stability_guarantee(
    *,
    outer: SymbolicUniverseTier,
    outer_coverage_certificate: SymbolicJointCoverageCertificate,
    outer_solver_certificate: SolverSemanticValidityCertificate,
    inclusion_certificate: JointSymbolicInclusionCertificate,
) -> SymbolicExtensionStabilityGuarantee:
    """Combine outer soundness and inclusion validity into a stability bound.

    Let outer retained-set coverage fail with probability at most ``alpha``,
    decisive outer solver semantics fail with probability at most ``beta``, and
    the joint inner-to-outer inclusion certificate fail with probability at most
    ``gamma``. Then, without independence,

    ``P(any false decisive outer conclusion OR false extension-stability claim) <= min(1, alpha + beta + gamma)``.

    The stability part is conditional on a motif being called extension-stable by
    `audit_symbolic_universe_extension`; a missing inclusion certificate is not
    eligible for this guarantee.
    """

    if outer_coverage_certificate.required_cell_ids != outer.required_cell_ids:
        raise ValueError("outer coverage certificate required cell IDs do not match the outer tier")
    if set(outer_solver_certificate.required_cell_ids) != set(outer.required_cell_ids):
        raise ValueError("outer solver certificate required cell IDs do not match the outer tier")
    if set(outer_solver_certificate.motifs) != set(outer.space.motifs):
        raise ValueError("outer solver certificate motifs do not match the outer tier")
    if inclusion_certificate.outer_tier_id != outer.tier_id:
        raise ValueError("inclusion certificate outer tier ID does not match the outer tier")
    if inclusion_certificate.required_cell_ids != outer.required_cell_ids:
        raise ValueError("inclusion certificate required cells do not match the outer tier")

    alpha = outer_coverage_certificate.miscoverage_upper_bound
    beta = outer_solver_certificate.semantic_failure_upper_bound
    gamma = inclusion_certificate.inclusion_failure_upper_bound
    return SymbolicExtensionStabilityGuarantee(
        outer_tier_id=outer.tier_id,
        statistical_coverage_lower_bound=outer_coverage_certificate.lower_bound,
        solver_semantic_validity_lower_bound=outer_solver_certificate.lower_bound,
        inclusion_validity_lower_bound=inclusion_certificate.lower_bound,
        statistical_miscoverage_upper_bound=alpha,
        solver_semantic_failure_upper_bound=beta,
        inclusion_failure_upper_bound=gamma,
        false_decisive_or_false_stability_upper_bound=min(1.0, alpha + beta + gamma),
        required_cell_ids=outer.required_cell_ids,
        motifs=outer.space.motifs,
        coverage_method=outer_coverage_certificate.method,
        solver_method=outer_solver_certificate.method,
        inclusion_method=inclusion_certificate.method,
        assumptions=(
            *outer_coverage_certificate.assumptions,
            *outer_solver_certificate.assumptions,
            *inclusion_certificate.assumptions,
        ),
    )
