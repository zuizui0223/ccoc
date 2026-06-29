"""Anytime outer-envelope stability for symbolic RACH candidate spaces.

This module combines three RACH layers:

* anytime symbolic confidence-set lifting for arbitrary sequential data;
* symbolic outer-envelope stability over continuous or uncountable candidate
  spaces; and
* joint inner-to-outer inclusion certificates.

At each certified look, an inner and outer symbolic retained set are classified.
An extension-stable conclusion is allowed only when the outer decisive status
matches the inner status under a certificate that every required inner retained
set is contained in the corresponding outer retained set. The theorem controls
false decisive *outer* conclusions and invalid extension-stability claims across
all certified looks and any data-dependent stopping time.

RACH does not read raw data, search for inclusion proofs, or infer the true
candidate. All coverage, solver-validity, and inclusion-validity statements are
external obligations recorded explicitly here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .admissibility import MotifStatus
from .anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
)
from .symbolic_candidate_sets import SymbolicCandidateSpace
from .symbolic_universe_extension import (
    ExtensionStatus,
    JointSymbolicInclusionCertificate,
    SymbolicUniverseExtensionReport,
    SymbolicUniverseTier,
    audit_symbolic_universe_extension,
)


def _unit_interval(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")


def _validate_look_scope(looks: tuple[int, ...] | None, name: str) -> None:
    if looks is None:
        return
    if not looks:
        raise ValueError(f"{name} must be non-empty when provided")
    if any(not isinstance(look, int) or look < 1 for look in looks):
        raise ValueError(f"{name} must contain positive integers")
    if len(set(looks)) != len(looks):
        raise ValueError(f"{name} must be unique")


@dataclass(frozen=True)
class AnytimeSymbolicExtensionTarget:
    """The fixed inner/outer target shared by every sequential extension look."""

    inner_tier_id: str
    outer_tier_id: str
    space: SymbolicCandidateSpace
    required_cell_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.inner_tier_id or not self.outer_tier_id:
            raise ValueError("inner_tier_id and outer_tier_id must be non-empty")
        if self.inner_tier_id == self.outer_tier_id:
            raise ValueError("inner and outer tier IDs must differ")
        if not self.required_cell_ids:
            raise ValueError("required_cell_ids must not be empty")
        if len(set(self.required_cell_ids)) != len(self.required_cell_ids):
            raise ValueError("required_cell_ids must be unique")


@dataclass(frozen=True)
class SequentialSymbolicUniverseExtensionSnapshot:
    """Inner and outer symbolic retained tiers at one positive integer look."""

    look: int
    inner: SymbolicUniverseTier
    outer: SymbolicUniverseTier

    def __post_init__(self) -> None:
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("look must be a positive integer")

    @property
    def target(self) -> AnytimeSymbolicExtensionTarget:
        if self.inner.space != self.outer.space:
            raise ValueError("inner and outer tiers must use the same symbolic candidate space")
        if self.inner.required_cell_ids != self.outer.required_cell_ids:
            raise ValueError("inner and outer tiers must use identical required cell IDs")
        return AnytimeSymbolicExtensionTarget(
            inner_tier_id=self.inner.tier_id,
            outer_tier_id=self.outer.tier_id,
            space=self.inner.space,
            required_cell_ids=self.inner.required_cell_ids,
        )


@dataclass(frozen=True)
class AnytimeJointSymbolicInclusionCertificate:
    """External all-look inclusion statement for a fixed inner/outer target.

    The certificate asserts

    ``P(for every certified look t and required cell r, C_inner,r,t subseteq C_outer,r,t) >= lower_bound``.

    With ``certified_looks=None``, it covers every positive integer look.
    A proof-carrying inclusion verifier may use ``lower_bound=1.0``. An
    approximate or randomized backend must expose its nonzero inclusion error
    as ``gamma = 1 - lower_bound``.
    """

    inner_tier_id: str
    outer_tier_id: str
    required_cell_ids: tuple[str, ...]
    lower_bound: float
    method: str
    assumptions: tuple[str, ...] = ()
    evidence_reference: str = ""
    certified_looks: tuple[int, ...] | None = None

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
        _validate_look_scope(self.certified_looks, "certified_looks")

    @property
    def inclusion_failure_upper_bound(self) -> float:
        return 1.0 - self.lower_bound

    def covers_look(self, look: int) -> bool:
        return self.certified_looks is None or look in self.certified_looks


@dataclass(frozen=True)
class AnytimeSymbolicExtensionStabilityReport:
    """Per-look extension audits over a shared sequential target."""

    target: AnytimeSymbolicExtensionTarget
    certified_looks: tuple[int, ...] | None
    reports_by_look: Mapping[int, SymbolicUniverseExtensionReport]

    @property
    def extension_stable_motifs_by_look(self) -> Mapping[int, tuple[str, ...]]:
        return {
            look: report.extension_stable_motifs
            for look, report in self.reports_by_look.items()
        }

    @property
    def scope_fragile_motifs_by_look(self) -> Mapping[int, tuple[str, ...]]:
        return {
            look: report.scope_fragile_motifs
            for look, report in self.reports_by_look.items()
        }


@dataclass(frozen=True)
class AnytimeSymbolicExtensionStabilityWitness:
    """Pointwise audit witness for the all-look outer-envelope theorem.

    The Boolean maps are ground-truth metadata supplied only for finite theorem
    checks and regression tests. RACH cannot infer them from data. The three maps
    correspond respectively to the all-look coverage event, decisive outer solver
    semantic-validity event, and all-look inclusion-validity event.
    """

    true_active_motifs: frozenset[str]
    outer_true_retained_by_look: Mapping[int, bool]
    outer_solver_semantics_valid_by_look: Mapping[int, bool]
    inclusion_valid_by_look: Mapping[int, bool]
    false_decisive_outer_motifs_by_look: Mapping[int, tuple[str, ...]]
    invalid_extension_stability_motifs_by_look: Mapping[int, tuple[str, ...]]

    @property
    def joint_good_event_at_all_looks(self) -> bool:
        return all(
            self.outer_true_retained_by_look[look]
            and self.outer_solver_semantics_valid_by_look[look]
            and self.inclusion_valid_by_look[look]
            for look in self.outer_true_retained_by_look
        )

    @property
    def false_or_invalid_looks(self) -> tuple[int, ...]:
        return tuple(
            look
            for look in self.outer_true_retained_by_look
            if self.false_decisive_outer_motifs_by_look[look]
            or self.invalid_extension_stability_motifs_by_look[look]
        )

    @property
    def implication_holds(self) -> bool:
        """False/invalid claims require failure of coverage, solver, or inclusion."""

        return not self.false_or_invalid_looks or not self.joint_good_event_at_all_looks


@dataclass(frozen=True)
class AnytimeSymbolicExtensionStabilityGuarantee:
    """All-look, optional-stopping-safe outer-envelope stability bound."""

    true_candidate_label: str
    target: AnytimeSymbolicExtensionTarget
    statistical_time_uniform_coverage_lower_bound: float
    solver_time_uniform_validity_lower_bound: float
    inclusion_time_uniform_validity_lower_bound: float
    statistical_miscoverage_upper_bound: float
    solver_semantic_failure_upper_bound: float
    inclusion_failure_upper_bound: float
    time_uniform_false_decisive_or_invalid_stability_upper_bound: float
    stopping_time_false_decisive_or_invalid_stability_upper_bound: float
    certified_looks: tuple[int, ...] | None
    coverage_method: str
    solver_method: str
    inclusion_method: str
    assumptions: tuple[str, ...]


def _common_scope(
    coverage: AnytimeSymbolicJointCoverageCertificate,
    solver: AnytimeSolverSemanticValidityCertificate,
    inclusion: AnytimeJointSymbolicInclusionCertificate,
) -> tuple[int, ...] | None:
    finite_scopes = [
        set(certificate.certified_looks)
        for certificate in (coverage, solver, inclusion)
        if certificate.certified_looks is not None
    ]
    if not finite_scopes:
        return None
    first = finite_scopes[0]
    if any(scope != first for scope in finite_scopes[1:]):
        raise ValueError("coverage, solver, and inclusion certificates must cover the same finite look scope")
    return tuple(sorted(first))


def _validate_target_certificates(
    target: AnytimeSymbolicExtensionTarget,
    coverage: AnytimeSymbolicJointCoverageCertificate,
    solver: AnytimeSolverSemanticValidityCertificate,
    inclusion: AnytimeJointSymbolicInclusionCertificate,
) -> tuple[int, ...] | None:
    if coverage.required_cell_ids != target.required_cell_ids:
        raise ValueError("coverage certificate required cell IDs do not match the extension target")
    if set(solver.required_cell_ids) != set(target.required_cell_ids):
        raise ValueError("solver certificate required cell IDs do not match the extension target")
    if set(solver.motifs) != set(target.space.motifs):
        raise ValueError("solver certificate motifs do not match the extension target")
    if inclusion.inner_tier_id != target.inner_tier_id:
        raise ValueError("inclusion certificate inner tier ID does not match the extension target")
    if inclusion.outer_tier_id != target.outer_tier_id:
        raise ValueError("inclusion certificate outer tier ID does not match the extension target")
    if inclusion.required_cell_ids != target.required_cell_ids:
        raise ValueError("inclusion certificate required cell IDs do not match the extension target")
    return _common_scope(coverage, solver, inclusion)


def _validate_snapshots(
    snapshots: Iterable[SequentialSymbolicUniverseExtensionSnapshot],
    *,
    target: AnytimeSymbolicExtensionTarget | None = None,
    coverage: AnytimeSymbolicJointCoverageCertificate | None = None,
    solver: AnytimeSolverSemanticValidityCertificate | None = None,
    inclusion: AnytimeJointSymbolicInclusionCertificate | None = None,
) -> tuple[SequentialSymbolicUniverseExtensionSnapshot, ...]:
    snapshot_tuple = tuple(snapshots)
    if not snapshot_tuple:
        raise ValueError("at least one sequential symbolic extension snapshot is required")
    looks = tuple(snapshot.look for snapshot in snapshot_tuple)
    if len(set(looks)) != len(looks) or looks != tuple(sorted(looks)):
        raise ValueError("extension snapshots must have unique increasing look indices")
    expected_target = target or snapshot_tuple[0].target
    for snapshot in snapshot_tuple:
        if snapshot.target != expected_target:
            raise ValueError("every extension snapshot must share the same inner/outer target")
        if coverage is not None and not coverage.covers_look(snapshot.look):
            raise ValueError(f"look {snapshot.look} is outside the coverage certificate's declared scope")
        if solver is not None and not solver.covers_look(snapshot.look):
            raise ValueError(f"look {snapshot.look} is outside the solver certificate's declared scope")
        if inclusion is not None and not inclusion.covers_look(snapshot.look):
            raise ValueError(f"look {snapshot.look} is outside the inclusion certificate's declared scope")
    return snapshot_tuple


def _single_look_inclusion_certificate(
    certificate: AnytimeJointSymbolicInclusionCertificate,
) -> JointSymbolicInclusionCertificate:
    return JointSymbolicInclusionCertificate(
        inner_tier_id=certificate.inner_tier_id,
        outer_tier_id=certificate.outer_tier_id,
        required_cell_ids=certificate.required_cell_ids,
        lower_bound=certificate.lower_bound,
        method=certificate.method,
        assumptions=certificate.assumptions,
        evidence_reference=certificate.evidence_reference,
    )


def audit_anytime_symbolic_universe_extension(
    snapshots: Iterable[SequentialSymbolicUniverseExtensionSnapshot],
    *,
    inclusion_certificate: AnytimeJointSymbolicInclusionCertificate | None,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate | None = None,
    solver_certificate: AnytimeSolverSemanticValidityCertificate | None = None,
) -> AnytimeSymbolicExtensionStabilityReport:
    """Audit outer-envelope stability at every certified sequential look.

    A missing inclusion certificate preserves the ordinary outer statuses inside
    each static tier, but produces `UNSUPPORTED` extension-stability labels at
    every look. If certificates are supplied, their target and scope are checked
    before any per-look audit runs.
    """

    first_pass = _validate_snapshots(snapshots)
    target = first_pass[0].target
    if inclusion_certificate is not None:
        if coverage_certificate is not None and solver_certificate is not None:
            scope = _validate_target_certificates(
                target,
                coverage_certificate,
                solver_certificate,
                inclusion_certificate,
            )
        else:
            if inclusion_certificate.inner_tier_id != target.inner_tier_id:
                raise ValueError("inclusion certificate inner tier ID does not match the extension target")
            if inclusion_certificate.outer_tier_id != target.outer_tier_id:
                raise ValueError("inclusion certificate outer tier ID does not match the extension target")
            if inclusion_certificate.required_cell_ids != target.required_cell_ids:
                raise ValueError("inclusion certificate required cell IDs do not match the extension target")
            scope = inclusion_certificate.certified_looks
    else:
        scope = None
    snapshot_tuple = _validate_snapshots(
        first_pass,
        target=target,
        coverage=coverage_certificate,
        solver=solver_certificate,
        inclusion=inclusion_certificate,
    )
    static_certificate = (
        _single_look_inclusion_certificate(inclusion_certificate)
        if inclusion_certificate is not None
        else None
    )
    return AnytimeSymbolicExtensionStabilityReport(
        target=target,
        certified_looks=scope,
        reports_by_look={
            snapshot.look: audit_symbolic_universe_extension(
                snapshot.inner,
                snapshot.outer,
                static_certificate,
            )
            for snapshot in snapshot_tuple
        },
    )


def _false_decisive_outer_motifs(
    statuses: Mapping[str, MotifStatus],
    true_active_motifs: frozenset[str],
) -> tuple[str, ...]:
    return tuple(
        motif
        for motif, status in statuses.items()
        if (status is MotifStatus.INVARIANT and motif not in true_active_motifs)
        or (status is MotifStatus.EXCLUDED and motif in true_active_motifs)
    )


def deterministic_anytime_symbolic_extension_stability_witness(
    snapshots: Iterable[SequentialSymbolicUniverseExtensionSnapshot],
    *,
    inclusion_certificate: AnytimeJointSymbolicInclusionCertificate,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
    true_active_motifs: frozenset[str],
    outer_true_retained_by_look: Mapping[int, bool],
    outer_solver_semantics_valid_by_look: Mapping[int, bool],
    inclusion_valid_by_look: Mapping[int, bool],
) -> AnytimeSymbolicExtensionStabilityWitness:
    """Check the pointwise all-look outer-stability implication.

    On the joint event that the true candidate is retained in every outer set,
    decisive outer solver semantics are valid, and every inner-to-outer inclusion
    relation is valid, neither a false decisive outer result nor an invalid
    extension-stability label can occur. The Boolean maps encode those external
    ground-truth events for exhaustive finite regression tests.
    """

    report = audit_anytime_symbolic_universe_extension(
        snapshots,
        inclusion_certificate=inclusion_certificate,
        coverage_certificate=coverage_certificate,
        solver_certificate=solver_certificate,
    )
    if not true_active_motifs <= set(report.target.space.motifs):
        raise ValueError("true_active_motifs must be a subset of the target motif vocabulary")
    looks = tuple(report.reports_by_look)
    for mapping, name in (
        (outer_true_retained_by_look, "outer_true_retained_by_look"),
        (outer_solver_semantics_valid_by_look, "outer_solver_semantics_valid_by_look"),
        (inclusion_valid_by_look, "inclusion_valid_by_look"),
    ):
        if set(mapping) != set(looks):
            raise ValueError(f"{name} must contain exactly the shown look indices")

    false_decisive = {
        look: _false_decisive_outer_motifs(
            extension_report.motifs and {
                motif: audit.outer_status
                for motif, audit in extension_report.motifs.items()
            },
            true_active_motifs,
        )
        for look, extension_report in report.reports_by_look.items()
    }
    invalid_stability = {
        look: (
            extension_report.extension_stable_motifs
            if not inclusion_valid_by_look[look]
            else ()
        )
        for look, extension_report in report.reports_by_look.items()
    }
    witness = AnytimeSymbolicExtensionStabilityWitness(
        true_active_motifs=true_active_motifs,
        outer_true_retained_by_look=outer_true_retained_by_look,
        outer_solver_semantics_valid_by_look=outer_solver_semantics_valid_by_look,
        inclusion_valid_by_look=inclusion_valid_by_look,
        false_decisive_outer_motifs_by_look=false_decisive,
        invalid_extension_stability_motifs_by_look=invalid_stability,
    )
    if not witness.implication_holds:
        raise RuntimeError("anytime symbolic extension-stability implication was violated")
    return witness


def anytime_symbolic_extension_stability_guarantee(
    *,
    target: AnytimeSymbolicExtensionTarget,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
    inclusion_certificate: AnytimeJointSymbolicInclusionCertificate,
) -> AnytimeSymbolicExtensionStabilityGuarantee:
    """Lift all-look outer soundness and inclusion validity to arbitrary stopping.

    Let the all-look outer statistical coverage event fail with probability at
    most ``alpha``, all decisive outer solver semantics fail with probability at
    most ``beta``, and all inner-to-outer inclusion statements fail with
    probability at most ``gamma``. Then, without any independence assumption,

    ``P(any false decisive outer conclusion OR invalid extension-stability claim at any certified look) <= min(1, alpha + beta + gamma)``.

    The same bound holds after every data-dependent stopping time whose selected
    look lies in the common certificate scope. The proof is a union bound over
    the three all-look failure events.
    """

    scope = _validate_target_certificates(
        target,
        coverage_certificate,
        solver_certificate,
        inclusion_certificate,
    )
    alpha = coverage_certificate.miscoverage_upper_bound
    beta = solver_certificate.semantic_failure_upper_bound
    gamma = inclusion_certificate.inclusion_failure_upper_bound
    bound = min(1.0, alpha + beta + gamma)
    return AnytimeSymbolicExtensionStabilityGuarantee(
        true_candidate_label=coverage_certificate.true_candidate_label,
        target=target,
        statistical_time_uniform_coverage_lower_bound=coverage_certificate.lower_bound,
        solver_time_uniform_validity_lower_bound=solver_certificate.lower_bound,
        inclusion_time_uniform_validity_lower_bound=inclusion_certificate.lower_bound,
        statistical_miscoverage_upper_bound=alpha,
        solver_semantic_failure_upper_bound=beta,
        inclusion_failure_upper_bound=gamma,
        time_uniform_false_decisive_or_invalid_stability_upper_bound=bound,
        stopping_time_false_decisive_or_invalid_stability_upper_bound=bound,
        certified_looks=scope,
        coverage_method=coverage_certificate.method,
        solver_method=solver_certificate.method,
        inclusion_method=inclusion_certificate.method,
        assumptions=(
            *coverage_certificate.assumptions,
            *solver_certificate.assumptions,
            *inclusion_certificate.assumptions,
        ),
    )
