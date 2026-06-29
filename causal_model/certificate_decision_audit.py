"""Certificate-completeness audit for symbolic RACH decisions.

A hash-bound manifest says which artifacts belong to a theorem target.  This
module adds the final decision gate: a live symbolic RACH classification is
allowed to remain `INVARIANT`, `EXCLUDED`, or `UNRESOLVED` only when the
manifest contains the proof bindings required for that particular conclusion and
the live certificates identify those bindings exactly.

The audit intentionally downgrades incomplete conclusions to `UNSUPPORTED`:

* `INVARIANT` needs a bound non-empty SAT witness and a bound inactive UNSAT
  proof in every required cell.
* `EXCLUDED` needs a bound non-empty SAT witness and a bound active UNSAT proof
  in every required cell.
* `UNRESOLVED` needs at least one bound active SAT witness and at least one
  bound inactive SAT witness across the required cells.

The module neither establishes statistical coverage nor proves solver semantics.
Those remain the responsibilities of the external certificates and proof
verifiers.  It verifies that the conclusions being surfaced are actually backed
by the target-bound artifacts that those other layers describe.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping

from .admissibility import MotifStatus
from .anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
    SequentialSymbolicConfidenceSetSnapshot,
)
from .certificate_manifest import (
    CertificateManifest,
    ManifestVerificationReport,
    QueryRole,
    SolverQueryProofBinding,
    verify_anytime_symbolic_manifest,
)
from .symbolic_candidate_sets import (
    FeasibilityCertificate,
    FeasibilityStatus,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    classify_symbolic_candidate_sets,
)


class CertificateAuditReason(str, Enum):
    """Why a source symbolic status could not be retained by the audit gate."""

    SOURCE_UNSUPPORTED = "source-unsupported"
    MISSING_BINDING = "missing-binding"
    STATUS_MISMATCH = "status-mismatch"
    QUERY_IDENTIFIER_MISMATCH = "query-identifier-mismatch"
    PROOF_IDENTIFIER_MISMATCH = "proof-identifier-mismatch"
    VERIFIER_IDENTIFIER_MISMATCH = "verifier-identifier-mismatch"
    MISSING_ACTIVE_WITNESS = "missing-active-witness"
    MISSING_INACTIVE_WITNESS = "missing-inactive-witness"


@dataclass(frozen=True)
class CertificateRequirement:
    """One live certificate that must be bound for a conclusion to be retained."""

    look: int
    cell_id: str
    motif: str
    role: QueryRole
    expected_status: FeasibilityStatus

    @property
    def key(self) -> tuple[int, str, str, QueryRole]:
        return (self.look, self.cell_id, self.motif, self.role)


@dataclass(frozen=True)
class CertificateRequirementAudit:
    """Audit result for one required live certificate."""

    requirement: CertificateRequirement
    satisfied: bool
    reason: CertificateAuditReason | None = None


@dataclass(frozen=True)
class CertificateCompleteMotifAudit:
    """Source versus certificate-complete status for one motif at one look."""

    look: int
    motif: str
    source_status: MotifStatus
    audited_status: MotifStatus
    requirement_audits: tuple[CertificateRequirementAudit, ...]
    reasons: tuple[CertificateAuditReason, ...]

    @property
    def certificate_complete(self) -> bool:
        return self.source_status is self.audited_status and self.audited_status is not MotifStatus.UNSUPPORTED


@dataclass(frozen=True)
class CertificateCompleteSnapshotAudit:
    """All motif audits at one certified sequential look."""

    look: int
    motifs: Mapping[str, CertificateCompleteMotifAudit]


@dataclass(frozen=True)
class CertificateCompleteDecisionAudit:
    """End-to-end manifest verification plus certificate-complete decisions."""

    manifest_verification: ManifestVerificationReport
    snapshots: tuple[CertificateCompleteSnapshotAudit, ...]

    @property
    def any_downgraded_decision(self) -> bool:
        return any(
            audit.source_status is not audit.audited_status
            for snapshot in self.snapshots
            for audit in snapshot.motifs.values()
        )


def bind_certificate_to_manifest(
    certificate: FeasibilityCertificate,
    binding: SolverQueryProofBinding,
) -> FeasibilityCertificate:
    """Return a certificate carrying the exact IDs of a verified manifest binding.

    Call this only after the underlying solver result has been independently
    verified (for example by the exact rational linear verifier).  The helper
    does not establish the result's semantics; it writes the query and proof
    artifact IDs required for an end-to-end manifest audit.
    """

    if certificate.status is not binding.status:
        raise ValueError("live certificate status must match its manifest binding status")
    return FeasibilityCertificate(
        query_description=binding.query_encoding_artifact.artifact_id,
        status=certificate.status,
        evidence_reference=binding.proof_artifact.artifact_id,
        solver=binding.verifier_id,
        assumptions=certificate.assumptions + ("bound-to-certificate-manifest",),
    )


def _binding_index(manifest: CertificateManifest) -> Mapping[tuple[int, str, str, QueryRole], SolverQueryProofBinding]:
    return {binding.query_key: binding for binding in manifest.solver_query_proofs}


def _certificate_for_role(
    cell: SymbolicConfidenceSetCell,
    motif: str,
    role: QueryRole,
) -> FeasibilityCertificate:
    queries = cell.motif_queries[motif]
    if role is QueryRole.NONEMPTY:
        return queries.nonempty
    if role is QueryRole.ACTIVE:
        return queries.active
    return queries.inactive


def _audit_requirement(
    requirement: CertificateRequirement,
    certificate: FeasibilityCertificate,
    bindings: Mapping[tuple[int, str, str, QueryRole], SolverQueryProofBinding],
) -> CertificateRequirementAudit:
    binding = bindings.get(requirement.key)
    if binding is None:
        return CertificateRequirementAudit(requirement, False, CertificateAuditReason.MISSING_BINDING)
    if certificate.status is not requirement.expected_status or binding.status is not requirement.expected_status:
        return CertificateRequirementAudit(requirement, False, CertificateAuditReason.STATUS_MISMATCH)
    if certificate.query_description != binding.query_encoding_artifact.artifact_id:
        return CertificateRequirementAudit(requirement, False, CertificateAuditReason.QUERY_IDENTIFIER_MISMATCH)
    if certificate.evidence_reference != binding.proof_artifact.artifact_id:
        return CertificateRequirementAudit(requirement, False, CertificateAuditReason.PROOF_IDENTIFIER_MISMATCH)
    if certificate.solver != binding.verifier_id:
        return CertificateRequirementAudit(requirement, False, CertificateAuditReason.VERIFIER_IDENTIFIER_MISMATCH)
    return CertificateRequirementAudit(requirement, True)


def _required_cells(snapshot: SequentialSymbolicConfidenceSetSnapshot) -> tuple[SymbolicConfidenceSetCell, ...]:
    return tuple(cell for cell in snapshot.cells if cell.required)


def _decisive_requirements(
    source_status: MotifStatus,
    *,
    look: int,
    motif: str,
    cells: tuple[SymbolicConfidenceSetCell, ...],
) -> tuple[CertificateRequirement, ...]:
    if source_status is MotifStatus.INVARIANT:
        return tuple(
            requirement
            for cell in cells
            for requirement in (
                CertificateRequirement(look, cell.cell_id, motif, QueryRole.NONEMPTY, FeasibilityStatus.SAT),
                CertificateRequirement(look, cell.cell_id, motif, QueryRole.INACTIVE, FeasibilityStatus.UNSAT),
            )
        )
    if source_status is MotifStatus.EXCLUDED:
        return tuple(
            requirement
            for cell in cells
            for requirement in (
                CertificateRequirement(look, cell.cell_id, motif, QueryRole.NONEMPTY, FeasibilityStatus.SAT),
                CertificateRequirement(look, cell.cell_id, motif, QueryRole.ACTIVE, FeasibilityStatus.UNSAT),
            )
        )
    return ()


def _unresolved_requirements(
    *,
    look: int,
    motif: str,
    cells: tuple[SymbolicConfidenceSetCell, ...],
) -> tuple[CertificateRequirement, ...]:
    """Return every available active/inactive witness candidate for later audit."""

    return tuple(
        CertificateRequirement(look, cell.cell_id, motif, role, FeasibilityStatus.SAT)
        for cell in cells
        for role in (QueryRole.ACTIVE, QueryRole.INACTIVE)
        if _certificate_for_role(cell, motif, role).status is FeasibilityStatus.SAT
    )


def _unique_reasons(audits: Iterable[CertificateRequirementAudit]) -> tuple[CertificateAuditReason, ...]:
    return tuple(dict.fromkeys(
        audit.reason for audit in audits if audit.reason is not None
    ))


def audit_symbolic_snapshot_decisions(
    space: SymbolicCandidateSpace,
    snapshot: SequentialSymbolicConfidenceSetSnapshot,
    manifest: CertificateManifest,
) -> CertificateCompleteSnapshotAudit:
    """Audit one symbolic sequential look against a verified manifest target.

    This function assumes artifact bytes and theorem context were checked already
    by `verify_anytime_symbolic_manifest`. It additionally checks that every
    conclusion's *live* certificates identify the corresponding manifest query,
    proof artifact, and verifier.
    """

    required_cells = _required_cells(snapshot)
    required_ids = tuple(cell.cell_id for cell in required_cells)
    if required_ids != manifest.target.required_cell_ids:
        raise ValueError("snapshot required cell IDs must exactly match the manifest target")
    if not manifest.target.covers_look(snapshot.look):
        raise ValueError("snapshot look lies outside the manifest target scope")

    report = classify_symbolic_candidate_sets(space, snapshot.cells)
    bindings = _binding_index(manifest)
    motif_audits: dict[str, CertificateCompleteMotifAudit] = {}

    for motif in space.motifs:
        source_status = report.classifications[motif].status
        if source_status is MotifStatus.UNSUPPORTED:
            motif_audits[motif] = CertificateCompleteMotifAudit(
                look=snapshot.look,
                motif=motif,
                source_status=source_status,
                audited_status=MotifStatus.UNSUPPORTED,
                requirement_audits=(),
                reasons=(CertificateAuditReason.SOURCE_UNSUPPORTED,),
            )
            continue

        if source_status in (MotifStatus.INVARIANT, MotifStatus.EXCLUDED):
            requirements = _decisive_requirements(
                source_status,
                look=snapshot.look,
                motif=motif,
                cells=required_cells,
            )
            audits = tuple(
                _audit_requirement(
                    requirement,
                    _certificate_for_role(
                        next(cell for cell in required_cells if cell.cell_id == requirement.cell_id),
                        motif,
                        requirement.role,
                    ),
                    bindings,
                )
                for requirement in requirements
            )
            complete = all(audit.satisfied for audit in audits)
            motif_audits[motif] = CertificateCompleteMotifAudit(
                look=snapshot.look,
                motif=motif,
                source_status=source_status,
                audited_status=source_status if complete else MotifStatus.UNSUPPORTED,
                requirement_audits=audits,
                reasons=_unique_reasons(audits),
            )
            continue

        # A globally unresolved classification is surfaced only after both motif
        # values have an independently manifest-bound SAT witness somewhere in
        # the required cells.
        candidates = _unresolved_requirements(
            look=snapshot.look,
            motif=motif,
            cells=required_cells,
        )
        audits = tuple(
            _audit_requirement(
                requirement,
                _certificate_for_role(
                    next(cell for cell in required_cells if cell.cell_id == requirement.cell_id),
                    motif,
                    requirement.role,
                ),
                bindings,
            )
            for requirement in candidates
        )
        active_complete = any(
            audit.satisfied and audit.requirement.role is QueryRole.ACTIVE
            for audit in audits
        )
        inactive_complete = any(
            audit.satisfied and audit.requirement.role is QueryRole.INACTIVE
            for audit in audits
        )
        reasons = list(_unique_reasons(audits))
        if not active_complete:
            reasons.append(CertificateAuditReason.MISSING_ACTIVE_WITNESS)
        if not inactive_complete:
            reasons.append(CertificateAuditReason.MISSING_INACTIVE_WITNESS)
        complete = active_complete and inactive_complete
        motif_audits[motif] = CertificateCompleteMotifAudit(
            look=snapshot.look,
            motif=motif,
            source_status=source_status,
            audited_status=MotifStatus.UNRESOLVED if complete else MotifStatus.UNSUPPORTED,
            requirement_audits=audits,
            reasons=tuple(dict.fromkeys(reasons)),
        )

    return CertificateCompleteSnapshotAudit(look=snapshot.look, motifs=motif_audits)


def verify_and_audit_anytime_symbolic_decisions(
    *,
    manifest: CertificateManifest,
    space: SymbolicCandidateSpace,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
    payloads: Mapping[str, str | bytes],
    snapshots: Iterable[SequentialSymbolicConfidenceSetSnapshot],
) -> CertificateCompleteDecisionAudit:
    """Run manifest verification followed by certificate-completeness decision audit."""

    manifest_report = verify_anytime_symbolic_manifest(
        manifest,
        space=space,
        coverage_certificate=coverage_certificate,
        solver_certificate=solver_certificate,
        payloads=payloads,
    )
    snapshot_tuple = tuple(snapshots)
    looks = tuple(snapshot.look for snapshot in snapshot_tuple)
    if not snapshot_tuple:
        raise ValueError("at least one symbolic snapshot is required")
    if looks != tuple(sorted(looks)) or len(set(looks)) != len(looks):
        raise ValueError("symbolic snapshots must have unique increasing look indices")
    return CertificateCompleteDecisionAudit(
        manifest_verification=manifest_report,
        snapshots=tuple(
            audit_symbolic_snapshot_decisions(space, snapshot, manifest)
            for snapshot in snapshot_tuple
        ),
    )
