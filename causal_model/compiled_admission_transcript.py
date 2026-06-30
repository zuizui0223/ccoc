"""Append-only signed-history adapter for compiler-admitted polyhedral looks.

The generic admission transcript predates proof-carrying finite-union motif
compilation.  Its hash chain binds one admitted snapshot and its conclusion, but
it has no tier-aware place to record all compiler artifacts used to derive a
motif and its complement.

This module wraps that existing transcript without changing its wire format.  A
compiler transcript entry computes one domain-separated evidence commitment over

* the fixed verified tagged-partition artifact;
* one compiled query-plan artifact for every (inner/outer tier, required cell);
* one branch-proof-family artifact for every
  (tier, required cell, motif, nonempty/active/inactive role); and
* the original admission and inclusion evidence references.

The commitment digest is stored in the existing transcript entry's
``admission_evidence_reference`` using a reserved domain-separated spelling.
Consequently the pre-existing hash chain and Ed25519 signed-checkpoint APIs
already bind compiler evidence.  The wrapper verifies the detailed evidence
object against that committed digest, so a digest cannot be used as an opaque
label for unrelated plans or branch proofs.

The adapter does not claim that manifest v1 binds both inner and outer query
families: its proof key has no tier coordinate.  The transcript is deliberately
the tier-aware audit layer, while the manifest remains the global candidate-space
and coverage commitment.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .admission_transcript import (
    ADMISSION_TRANSCRIPT_FORMAT,
    AdmissionTranscript,
    AdmissionTranscriptEntry,
    AdmissionTranscriptHeader,
    AdmissionTranscriptVerificationReport,
    verify_admission_transcript,
)
from .admissibility import MotifStatus
from .canonical_manifest_json import canonical_manifest_digest
from .certificate_manifest import (
    ArtifactReference,
    CertificateManifest,
    QueryRole,
    canonical_json,
    sha256_digest,
    verify_manifest_context,
)
from .exact_compiled_polyhedral_extension_admission import (
    EXACT_COMPILED_POLYHEDRAL_EXTENSION_ADMISSION_VERIFIER,
    VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    VerifiedExactCompiledPolyhedralExtensionLook,
    audit_exact_compiled_polyhedral_extension_looks,
)
from .polyhedral_motif_compiler import (
    compiled_polyhedral_motif_plan_artifact,
    compiled_role_proof_bundle_artifact,
    polyhedral_motif_partition_artifact,
)
from .signed_transcript_checkpoint import (
    Ed25519VerifierKey,
    SignedCheckpointVerificationReport,
    SignedTranscriptCheckpoint,
    TranscriptHeadCheckpoint,
    create_transcript_head_checkpoint,
    verify_signed_transcript_checkpoint,
)
from .symbolic_universe_extension import ExtensionStatus
from .anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate


COMPILED_ADMISSION_TRANSCRIPT_FORMAT = "rach-compiled-admission-transcript/v1"
COMPILED_ADMISSION_SCHEMA_ARTIFACT_ID = "compiled-polyhedral-admission-schema"
COMPILED_ADMISSION_ENTRY_ARTIFACT_PREFIX = "compiler-admission-entry/v1:"
_HEX_DIGEST_LENGTH = 64


def _require_nonempty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")


def _require_digest(value: str, name: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != _HEX_DIGEST_LENGTH
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256 hexadecimal digest")


def _artifact_object(artifact: ArtifactReference) -> dict[str, str]:
    return {
        "artifact_id": artifact.artifact_id,
        "media_type": artifact.media_type,
        "sha256": artifact.sha256,
    }


def _certificate_context_object(certificate: object) -> dict[str, object]:
    return {
        "required_cell_ids": list(certificate.required_cell_ids),
        "lower_bound": certificate.lower_bound,
        "method": certificate.method,
        "assumptions": list(certificate.assumptions),
        "certified_looks": (
            None if certificate.certified_looks is None else list(certificate.certified_looks)
        ),
    }


def compiled_admission_schema_context_digest(
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
) -> str:
    """Hash the all-look theorem target plus fixed compiler semantics."""

    target = verified_schema.target
    partition = verified_schema.verified_partition
    inclusion = verified_schema.all_look_inclusion_certificate
    return sha256_digest(
        canonical_json(
            {
                "format": COMPILED_ADMISSION_TRANSCRIPT_FORMAT,
                "target": {
                    "inner_tier_id": target.inner_tier_id,
                    "outer_tier_id": target.outer_tier_id,
                    "candidate_space_description": target.space.space_description,
                    "motifs": list(target.space.motifs),
                    "required_cell_ids": list(target.required_cell_ids),
                },
                "query_namespace": verified_schema.schema.query_namespace,
                "verified_partition_digest": partition.partition_digest,
                "outer_solver_certificate": _certificate_context_object(
                    verified_schema.all_look_solver_certificate
                ),
                "inner_outer_inclusion_certificate": {
                    **_certificate_context_object(inclusion),
                    "inner_tier_id": inclusion.inner_tier_id,
                    "outer_tier_id": inclusion.outer_tier_id,
                },
            }
        )
    )


@dataclass(frozen=True)
class CompiledAdmissionSchemaArtifacts:
    """Artifacts that define the immutable compiler admission schema history."""

    base_admission_schema_artifact: ArtifactReference
    partition_artifact: ArtifactReference

    def aggregate_artifact(
        self,
        *,
        schema_context_digest: str,
        query_namespace: str,
    ) -> ArtifactReference:
        """Build the single artifact committed by the generic transcript header."""

        _require_digest(schema_context_digest, "schema_context_digest")
        _require_nonempty(query_namespace, "query_namespace")
        payload = canonical_json(
            {
                "format_version": COMPILED_ADMISSION_TRANSCRIPT_FORMAT,
                "schema_context_digest": schema_context_digest,
                "query_namespace": query_namespace,
                "base_admission_schema_artifact": _artifact_object(
                    self.base_admission_schema_artifact
                ),
                "partition_artifact": _artifact_object(self.partition_artifact),
            }
        ).encode("utf-8")
        return ArtifactReference.from_payload(
            COMPILED_ADMISSION_SCHEMA_ARTIFACT_ID,
            payload,
            media_type="application/json",
        )


@dataclass(frozen=True)
class CompiledAdmissionTranscriptHeader:
    """A generic transcript header plus compiler-specific fixed commitments."""

    transcript_header: AdmissionTranscriptHeader
    schema_artifacts: CompiledAdmissionSchemaArtifacts
    query_namespace: str

    def __post_init__(self) -> None:
        _require_nonempty(self.query_namespace, "query_namespace")


@dataclass(frozen=True)
class CompiledPlanArtifactBinding:
    """One plan artifact for an inner or outer required cell at one look."""

    tier: str
    cell_id: str
    artifact: ArtifactReference

    def __post_init__(self) -> None:
        if self.tier not in ("inner", "outer"):
            raise ValueError("compiled plan artifact tier must be 'inner' or 'outer'")
        _require_nonempty(self.cell_id, "compiled plan artifact cell_id")


@dataclass(frozen=True)
class CompiledRoleProofArtifactBinding:
    """One complete compiler branch-proof family for a semantic motif role."""

    tier: str
    cell_id: str
    motif: str
    role: QueryRole
    artifact: ArtifactReference

    def __post_init__(self) -> None:
        if self.tier not in ("inner", "outer"):
            raise ValueError("compiled role artifact tier must be 'inner' or 'outer'")
        _require_nonempty(self.cell_id, "compiled role artifact cell_id")
        _require_nonempty(self.motif, "compiled role artifact motif")


@dataclass(frozen=True)
class CompiledAdmissionEntryEvidence:
    """Tier-aware compiler evidence whose digest is anchored in one base entry."""

    look: int
    partition_artifact: ArtifactReference
    plan_artifacts: tuple[CompiledPlanArtifactBinding, ...]
    role_proof_artifacts: tuple[CompiledRoleProofArtifactBinding, ...]
    original_admission_evidence_reference: str
    original_inclusion_evidence_reference: str
    admission_verifier: str

    def __post_init__(self) -> None:
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("compiler entry evidence look must be a positive integer")
        _require_nonempty(
            self.original_admission_evidence_reference,
            "original_admission_evidence_reference",
        )
        _require_nonempty(
            self.original_inclusion_evidence_reference,
            "original_inclusion_evidence_reference",
        )
        _require_nonempty(self.admission_verifier, "admission_verifier")

    @property
    def commitment_payload(self) -> bytes:
        return canonical_json(
            {
                "format_version": COMPILED_ADMISSION_TRANSCRIPT_FORMAT,
                "look": self.look,
                "partition_artifact": _artifact_object(self.partition_artifact),
                "plan_artifacts": [
                    {
                        "tier": binding.tier,
                        "cell_id": binding.cell_id,
                        "artifact": _artifact_object(binding.artifact),
                    }
                    for binding in sorted(
                        self.plan_artifacts,
                        key=lambda item: (item.tier, item.cell_id),
                    )
                ],
                "role_proof_artifacts": [
                    {
                        "tier": binding.tier,
                        "cell_id": binding.cell_id,
                        "motif": binding.motif,
                        "role": binding.role.value,
                        "artifact": _artifact_object(binding.artifact),
                    }
                    for binding in sorted(
                        self.role_proof_artifacts,
                        key=lambda item: (item.tier, item.cell_id, item.motif, item.role.value),
                    )
                ],
                "original_admission_evidence_reference": self.original_admission_evidence_reference,
                "original_inclusion_evidence_reference": self.original_inclusion_evidence_reference,
                "admission_verifier": self.admission_verifier,
            }
        ).encode("utf-8")

    @property
    def commitment_artifact(self) -> ArtifactReference:
        return ArtifactReference.from_payload(
            f"compiled-admission-entry:look-{self.look}",
            self.commitment_payload,
            media_type="application/json",
        )

    @property
    def commitment_reference(self) -> str:
        return f"{COMPILED_ADMISSION_ENTRY_ARTIFACT_PREFIX}{self.commitment_artifact.sha256}"


@dataclass(frozen=True)
class CompiledAdmissionTranscriptEntry:
    """Detailed compiler evidence paired with one hashed generic transcript entry."""

    sequence: int
    evidence: CompiledAdmissionEntryEvidence
    base_entry_digest: str

    def __post_init__(self) -> None:
        if not isinstance(self.sequence, int) or self.sequence < 1:
            raise ValueError("compiled transcript entry sequence must be a positive integer")
        _require_digest(self.base_entry_digest, "base_entry_digest")

    @property
    def look(self) -> int:
        return self.evidence.look


@dataclass(frozen=True)
class CompiledAdmissionTranscript:
    """Compiler evidence plus a generic hash chain usable by existing signatures."""

    header: CompiledAdmissionTranscriptHeader
    chain: AdmissionTranscript
    entries: tuple[CompiledAdmissionTranscriptEntry, ...] = ()

    @property
    def head_digest(self) -> str:
        return self.chain.head_digest


@dataclass(frozen=True)
class CompiledAdmissionTranscriptVerificationReport:
    """Successful validation of detailed compiler evidence and the base hash chain."""

    transcript_id: str
    entry_count: int
    recorded_looks: tuple[int, ...]
    genesis_digest: str
    head_digest: str
    partition_artifact_digest: str


def _expected_plan_keys(header: CompiledAdmissionTranscriptHeader) -> set[tuple[str, str]]:
    return {
        (tier, cell_id)
        for tier in ("inner", "outer")
        for cell_id in header.transcript_header.required_cell_ids
    }


def _expected_role_keys(header: CompiledAdmissionTranscriptHeader) -> set[tuple[str, str, str, QueryRole]]:
    return {
        (tier, cell_id, motif, role)
        for tier in ("inner", "outer")
        for cell_id in header.transcript_header.required_cell_ids
        for motif in header.transcript_header.motifs
        for role in (QueryRole.NONEMPTY, QueryRole.ACTIVE, QueryRole.INACTIVE)
    }


def _validate_evidence_layout(
    header: CompiledAdmissionTranscriptHeader,
    evidence: CompiledAdmissionEntryEvidence,
) -> None:
    if evidence.partition_artifact != header.schema_artifacts.partition_artifact:
        raise ValueError("compiler entry partition artifact does not match the transcript header")
    plan_keys = {(binding.tier, binding.cell_id) for binding in evidence.plan_artifacts}
    if plan_keys != _expected_plan_keys(header) or len(plan_keys) != len(evidence.plan_artifacts):
        raise ValueError("compiler entry must contain exactly one plan artifact per tier and required cell")
    role_keys = {
        (binding.tier, binding.cell_id, binding.motif, binding.role)
        for binding in evidence.role_proof_artifacts
    }
    if role_keys != _expected_role_keys(header) or len(role_keys) != len(evidence.role_proof_artifacts):
        raise ValueError("compiler entry must contain exactly one role artifact per tier/cell/motif/role")


def _validate_header_against_live_inputs(
    header: CompiledAdmissionTranscriptHeader,
    *,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> None:
    verify_manifest_context(
        manifest,
        space=verified_schema.target.space,
        coverage_certificate=coverage_certificate,
        solver_certificate=verified_schema.all_look_solver_certificate,
    )
    base = header.transcript_header
    if base.target_digest != manifest.target.target_digest:
        raise ValueError("manifest target digest does not match the compiled transcript header")
    if base.motifs != verified_schema.target.space.motifs:
        raise ValueError("live motif vocabulary does not match the compiled transcript header")
    if base.required_cell_ids != verified_schema.target.required_cell_ids:
        raise ValueError("live required cell IDs do not match the compiled transcript header")
    if header.query_namespace != verified_schema.schema.query_namespace:
        raise ValueError("live compiler query namespace does not match the transcript header")
    context_digest = compiled_admission_schema_context_digest(verified_schema)
    if base.schema_context_digest != context_digest:
        raise ValueError("live compiler admission schema context does not match the transcript header")
    expected_partition = polyhedral_motif_partition_artifact(verified_schema.verified_partition)
    if header.schema_artifacts.partition_artifact.sha256 != expected_partition.sha256:
        raise ValueError("live verified partition artifact does not match the transcript header")
    expected_schema_artifact = header.schema_artifacts.aggregate_artifact(
        schema_context_digest=context_digest,
        query_namespace=header.query_namespace,
    )
    if base.admission_schema_artifact != expected_schema_artifact:
        raise ValueError("compiled transcript schema artifact does not match its declared commitments")


def create_compiled_admission_transcript(
    *,
    transcript_id: str,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    base_admission_schema_artifact: ArtifactReference,
) -> CompiledAdmissionTranscript:
    """Create an empty compiler-aware chain bound to one fixed partition/schema."""

    verify_manifest_context(
        manifest,
        space=verified_schema.target.space,
        coverage_certificate=coverage_certificate,
        solver_certificate=verified_schema.all_look_solver_certificate,
    )
    context_digest = compiled_admission_schema_context_digest(verified_schema)
    artifacts = CompiledAdmissionSchemaArtifacts(
        base_admission_schema_artifact=base_admission_schema_artifact,
        partition_artifact=polyhedral_motif_partition_artifact(verified_schema.verified_partition),
    )
    header = AdmissionTranscriptHeader(
        transcript_id=transcript_id,
        target_digest=manifest.target.target_digest,
        motifs=verified_schema.target.space.motifs,
        required_cell_ids=verified_schema.target.required_cell_ids,
        admission_schema_artifact=artifacts.aggregate_artifact(
            schema_context_digest=context_digest,
            query_namespace=verified_schema.schema.query_namespace,
        ),
        schema_context_digest=context_digest,
    )
    compiled_header = CompiledAdmissionTranscriptHeader(
        transcript_header=header,
        schema_artifacts=artifacts,
        query_namespace=verified_schema.schema.query_namespace,
    )
    return CompiledAdmissionTranscript(
        header=compiled_header,
        chain=AdmissionTranscript(header=header),
    )


def _build_entry_evidence(
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    admitted_look: VerifiedExactCompiledPolyhedralExtensionLook,
) -> CompiledAdmissionEntryEvidence:
    plan_bindings: list[CompiledPlanArtifactBinding] = []
    role_bindings: list[CompiledRoleProofArtifactBinding] = []
    for tier, queries_by_cell in (
        ("inner", admitted_look.inner_queries_by_cell),
        ("outer", admitted_look.outer_queries_by_cell),
    ):
        if tuple(queries_by_cell) != verified_schema.target.required_cell_ids:
            raise ValueError("admitted compiler query cells must match the fixed required-cell order")
        for cell_id in verified_schema.target.required_cell_ids:
            queries = queries_by_cell[cell_id]
            plan = queries.bound_proofs.plan
            plan_bindings.append(
                CompiledPlanArtifactBinding(
                    tier=tier,
                    cell_id=cell_id,
                    artifact=compiled_polyhedral_motif_plan_artifact(
                        plan,
                        artifact_id=f"compiled-plan:{tier}:look-{admitted_look.look}:cell-{cell_id}",
                    ),
                )
            )
            for motif in verified_schema.target.space.motifs:
                for role in (QueryRole.NONEMPTY, QueryRole.ACTIVE, QueryRole.INACTIVE):
                    role_bindings.append(
                        CompiledRoleProofArtifactBinding(
                            tier=tier,
                            cell_id=cell_id,
                            motif=motif,
                            role=role,
                            artifact=compiled_role_proof_bundle_artifact(
                                queries,
                                motif=motif,
                                role=role,
                                artifact_id=(
                                    f"compiled-role:{tier}:look-{admitted_look.look}:"
                                    f"cell-{cell_id}:motif-{motif}:role-{role.value}"
                                ),
                            ),
                        )
                    )
    return CompiledAdmissionEntryEvidence(
        look=admitted_look.look,
        partition_artifact=polyhedral_motif_partition_artifact(verified_schema.verified_partition),
        plan_artifacts=tuple(plan_bindings),
        role_proof_artifacts=tuple(role_bindings),
        original_admission_evidence_reference=admitted_look.evidence_reference,
        original_inclusion_evidence_reference=admitted_look.verified_inclusion_look.evidence_reference,
        admission_verifier=admitted_look.verifier,
    )


def verify_compiled_admission_transcript(
    transcript: CompiledAdmissionTranscript,
    *,
    expected_head_digest: str | None = None,
) -> CompiledAdmissionTranscriptVerificationReport:
    """Verify the generic chain and every compiler-evidence commitment it anchors."""

    if transcript.chain.header != transcript.header.transcript_header:
        raise ValueError("compiled transcript chain header does not match the compiled transcript header")
    base_report = verify_admission_transcript(
        transcript.chain,
        expected_head_digest=expected_head_digest,
    )
    if len(transcript.entries) != base_report.entry_count:
        raise ValueError("compiled transcript evidence count does not match the base chain")
    for expected_sequence, (entry, base_entry) in enumerate(
        zip(transcript.entries, transcript.chain.entries),
        start=1,
    ):
        if entry.sequence != expected_sequence:
            raise ValueError("compiled transcript entry sequences must be contiguous from one")
        if entry.look != base_entry.look:
            raise ValueError("compiled transcript entry look does not match the base chain")
        _validate_evidence_layout(transcript.header, entry.evidence)
        if base_entry.base_entry_digest if False else False:
            raise AssertionError("unreachable")
        if entry.base_entry_digest != base_entry.entry_digest:
            raise ValueError("compiled transcript entry does not name its exact base entry digest")
        if base_entry.admission_evidence_reference != entry.evidence.commitment_reference:
            raise ValueError("base transcript entry does not bind the compiler evidence commitment")
        if base_entry.inclusion_evidence_reference != entry.evidence.original_inclusion_evidence_reference:
            raise ValueError("base transcript inclusion evidence does not match compiler evidence")
        if base_entry.admission_verifier != entry.evidence.admission_verifier:
            raise ValueError("base transcript verifier does not match compiler evidence")
    return CompiledAdmissionTranscriptVerificationReport(
        transcript_id=base_report.transcript_id,
        entry_count=base_report.entry_count,
        recorded_looks=base_report.recorded_looks,
        genesis_digest=base_report.genesis_digest,
        head_digest=base_report.head_digest,
        partition_artifact_digest=transcript.header.schema_artifacts.partition_artifact.sha256,
    )


def append_compiled_admitted_look(
    transcript: CompiledAdmissionTranscript,
    *,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    admitted_look: VerifiedExactCompiledPolyhedralExtensionLook,
    manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> CompiledAdmissionTranscript:
    """Append one #24-admitted look and bind all tier-aware compiler artifacts."""

    report = verify_compiled_admission_transcript(transcript)
    _validate_header_against_live_inputs(
        transcript.header,
        verified_schema=verified_schema,
        manifest=manifest,
        coverage_certificate=coverage_certificate,
    )
    if admitted_look.look != admitted_look.snapshot.look:
        raise ValueError("admitted compiler look ID and snapshot look ID must match")
    if admitted_look.verified_inclusion_look.look != admitted_look.look:
        raise ValueError("admitted compiler look ID and inclusion look ID must match")
    if admitted_look.snapshot.target != verified_schema.target:
        raise ValueError("admitted compiler snapshot target does not match the fixed schema")
    if not manifest.target.covers_look(admitted_look.look):
        raise ValueError("admitted compiler look lies outside the manifest target scope")
    if not coverage_certificate.covers_look(admitted_look.look):
        raise ValueError("admitted compiler look lies outside the coverage certificate scope")
    if transcript.entries and admitted_look.look <= transcript.entries[-1].look:
        raise ValueError("a new compiler-admitted look must be strictly later than the transcript head")

    audit = audit_exact_compiled_polyhedral_extension_looks(
        verified_schema,
        (admitted_look,),
        coverage_certificate=coverage_certificate,
    )
    static_report = audit.reports_by_look[admitted_look.look]
    evidence = _build_entry_evidence(verified_schema, admitted_look)
    _validate_evidence_layout(transcript.header, evidence)
    base_entry = AdmissionTranscriptEntry(
        sequence=report.entry_count + 1,
        look=admitted_look.look,
        previous_entry_digest=report.head_digest,
        canonical_manifest_digest=canonical_manifest_digest(manifest),
        schema_context_digest=transcript.header.transcript_header.schema_context_digest,
        admission_evidence_reference=evidence.commitment_reference,
        inclusion_evidence_reference=evidence.original_inclusion_evidence_reference,
        admission_verifier=evidence.admission_verifier,
        outer_statuses={
            motif: static_report.motifs[motif].outer_status.value
            for motif in transcript.header.transcript_header.motifs
        },
        extension_statuses={
            motif: static_report.motifs[motif].extension_status.value
            for motif in transcript.header.transcript_header.motifs
        },
    )
    compiled_entry = CompiledAdmissionTranscriptEntry(
        sequence=base_entry.sequence,
        evidence=evidence,
        base_entry_digest=base_entry.entry_digest,
    )
    return CompiledAdmissionTranscript(
        header=transcript.header,
        chain=AdmissionTranscript(
            header=transcript.chain.header,
            entries=(*transcript.chain.entries, base_entry),
        ),
        entries=(*transcript.entries, compiled_entry),
    )


def create_compiled_transcript_head_checkpoint(
    transcript: CompiledAdmissionTranscript,
    *,
    checkpoint_sequence: int,
) -> TranscriptHeadCheckpoint:
    """Create an existing signed-checkpoint payload after compiler evidence validation."""

    verify_compiled_admission_transcript(transcript)
    return create_transcript_head_checkpoint(
        transcript.chain,
        checkpoint_sequence=checkpoint_sequence,
    )


def verify_signed_compiled_transcript_checkpoint(
    transcript: CompiledAdmissionTranscript,
    signed_checkpoint: SignedTranscriptCheckpoint,
    *,
    trusted_key: Ed25519VerifierKey,
) -> SignedCheckpointVerificationReport:
    """Verify compiler evidence first, then reuse the generic Ed25519 checkpoint verifier."""

    verify_compiled_admission_transcript(transcript)
    return verify_signed_transcript_checkpoint(
        transcript.chain,
        signed_checkpoint,
        trusted_key=trusted_key,
    )
