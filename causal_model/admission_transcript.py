"""Append-only hash transcripts for exact-admitted RACH sequential looks.

The exact polyhedral admission gate verifies one paired inner/outer snapshot at
a time. A valid all-look theorem still needs an audit trail that records which
admitted looks underlie a stopped conclusion. This module chains such records.

Every entry binds:

* one exact-admitted look from ``exact_polyhedral_extension_admission``;
* the strict canonical digest of its ``CertificateManifest``;
* a fixed external artifact commitment for the all-look admission schema;
* the previous entry digest; and
* outer and extension statuses recomputed from the admitted snapshot.

The resulting hash chain detects altered entries, reordered entries, cross-target
transplants, and deletion relative to a separately retained expected head. It
is not a signature scheme, timestamp authority, or proof that an external caller
recorded every look it ever inspected. In particular, fork/rollback detection
requires a previously published, signed, or otherwise trusted head digest.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .admissibility import MotifStatus
from .anytime_symbolic_extension_stability import audit_anytime_symbolic_universe_extension
from .anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from .canonical_manifest_json import canonical_manifest_digest
from .certificate_manifest import (
    ArtifactReference,
    CertificateManifest,
    canonical_json,
    sha256_digest,
    verify_manifest_context,
)
from .exact_polyhedral_extension_admission import (
    VerifiedExactPolyhedralExtensionAdmissionSchema,
    VerifiedExactPolyhedralExtensionLook,
)
from .symbolic_universe_extension import ExtensionStatus


ADMISSION_TRANSCRIPT_FORMAT = "rach-admission-transcript/v1"
_HEX_DIGEST_LENGTH = 64


def _require_digest(value: str, name: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != _HEX_DIGEST_LENGTH
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256 hexadecimal digest")


def _require_nonempty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")


def _certificate_context_object(certificate: object) -> dict[str, object]:
    """Return the theorem-relevant certificate fields without serializing proofs."""

    return {
        "required_cell_ids": list(certificate.required_cell_ids),
        "lower_bound": certificate.lower_bound,
        "method": certificate.method,
        "assumptions": list(certificate.assumptions),
        "certified_looks": (
            None if certificate.certified_looks is None else list(certificate.certified_looks)
        ),
    }


def admission_schema_context_digest(
    verified_schema: VerifiedExactPolyhedralExtensionAdmissionSchema,
) -> str:
    """Hash the fixed theorem context of a beta/gamma-zero admission schema.

    The separate ``admission_schema_artifact`` in a transcript header commits to
    serialized base systems and proof material. This digest binds the live
    in-memory theorem target and the two all-look certificate declarations.
    """

    target = verified_schema.target
    inclusion = verified_schema.all_look_inclusion_certificate
    return sha256_digest(
        canonical_json(
            {
                "format": ADMISSION_TRANSCRIPT_FORMAT,
                "target": {
                    "inner_tier_id": target.inner_tier_id,
                    "outer_tier_id": target.outer_tier_id,
                    "candidate_space_description": target.space.space_description,
                    "motifs": list(target.space.motifs),
                    "required_cell_ids": list(target.required_cell_ids),
                },
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
class AdmissionTranscriptHeader:
    """Immutable target commitment for one append-only admission history."""

    transcript_id: str
    target_digest: str
    motifs: tuple[str, ...]
    required_cell_ids: tuple[str, ...]
    admission_schema_artifact: ArtifactReference
    schema_context_digest: str
    format_version: str = ADMISSION_TRANSCRIPT_FORMAT

    def __post_init__(self) -> None:
        _require_nonempty(self.transcript_id, "transcript_id")
        if self.format_version != ADMISSION_TRANSCRIPT_FORMAT:
            raise ValueError(f"unsupported admission transcript format: {self.format_version!r}")
        _require_digest(self.target_digest, "target_digest")
        _require_digest(self.schema_context_digest, "schema_context_digest")
        if not self.motifs or len(set(self.motifs)) != len(self.motifs) or any(not motif for motif in self.motifs):
            raise ValueError("motifs must be unique non-empty names")
        if (
            not self.required_cell_ids
            or len(set(self.required_cell_ids)) != len(self.required_cell_ids)
            or any(not cell_id for cell_id in self.required_cell_ids)
        ):
            raise ValueError("required_cell_ids must be unique non-empty names")

    @property
    def genesis_digest(self) -> str:
        return sha256_digest(
            canonical_json(
                {
                    "format_version": self.format_version,
                    "transcript_id": self.transcript_id,
                    "target_digest": self.target_digest,
                    "motifs": list(self.motifs),
                    "required_cell_ids": list(self.required_cell_ids),
                    "admission_schema_artifact": self.admission_schema_artifact,
                    "schema_context_digest": self.schema_context_digest,
                }
            )
        )


@dataclass(frozen=True)
class AdmissionTranscriptEntry:
    """One chained exact-admission record for an increasing analysis look."""

    sequence: int
    look: int
    previous_entry_digest: str
    canonical_manifest_digest: str
    schema_context_digest: str
    admission_evidence_reference: str
    inclusion_evidence_reference: str
    admission_verifier: str
    outer_statuses: Mapping[str, str]
    extension_statuses: Mapping[str, str]

    def __post_init__(self) -> None:
        if not isinstance(self.sequence, int) or self.sequence < 1:
            raise ValueError("sequence must be a positive integer")
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("look must be a positive integer")
        _require_digest(self.previous_entry_digest, "previous_entry_digest")
        _require_digest(self.canonical_manifest_digest, "canonical_manifest_digest")
        _require_digest(self.schema_context_digest, "schema_context_digest")
        _require_nonempty(self.admission_evidence_reference, "admission_evidence_reference")
        _require_nonempty(self.inclusion_evidence_reference, "inclusion_evidence_reference")
        _require_nonempty(self.admission_verifier, "admission_verifier")
        if set(self.outer_statuses) != set(self.extension_statuses):
            raise ValueError("outer_statuses and extension_statuses must have identical motif keys")
        if not self.outer_statuses:
            raise ValueError("an admission transcript entry needs at least one motif status")
        for motif, status in self.outer_statuses.items():
            _require_nonempty(motif, "entry motif")
            try:
                MotifStatus(status)
            except ValueError as error:
                raise ValueError(f"unsupported outer status for motif {motif!r}") from error
        for motif, status in self.extension_statuses.items():
            try:
                extension = ExtensionStatus(status)
            except ValueError as error:
                raise ValueError(f"unsupported extension status for motif {motif!r}") from error
            outer = MotifStatus(self.outer_statuses[motif])
            if extension is ExtensionStatus.EXTENSION_STABLE and outer not in (
                MotifStatus.INVARIANT,
                MotifStatus.EXCLUDED,
            ):
                raise ValueError("extension-stable entry status requires a decisive outer status")
            if extension in (ExtensionStatus.SCOPE_FRAGILE, ExtensionStatus.NONDECISIVE) and outer is not MotifStatus.UNRESOLVED:
                raise ValueError("scope-fragile/nondecisive entry status requires an unresolved outer status")

    @property
    def entry_digest(self) -> str:
        return sha256_digest(
            canonical_json(
                {
                    "sequence": self.sequence,
                    "look": self.look,
                    "previous_entry_digest": self.previous_entry_digest,
                    "canonical_manifest_digest": self.canonical_manifest_digest,
                    "schema_context_digest": self.schema_context_digest,
                    "admission_evidence_reference": self.admission_evidence_reference,
                    "inclusion_evidence_reference": self.inclusion_evidence_reference,
                    "admission_verifier": self.admission_verifier,
                    "outer_statuses": dict(self.outer_statuses),
                    "extension_statuses": dict(self.extension_statuses),
                }
            )
        )


@dataclass(frozen=True)
class AdmissionTranscript:
    """One immutable append-only history represented as an ordered entry tuple."""

    header: AdmissionTranscriptHeader
    entries: tuple[AdmissionTranscriptEntry, ...] = ()

    @property
    def head_digest(self) -> str:
        return self.header.genesis_digest if not self.entries else self.entries[-1].entry_digest


@dataclass(frozen=True)
class AdmissionTranscriptVerificationReport:
    """Successful integrity verification result for one transcript prefix."""

    transcript_id: str
    entry_count: int
    recorded_looks: tuple[int, ...]
    genesis_digest: str
    head_digest: str


@dataclass(frozen=True)
class TranscriptDecisionAnchor:
    """A stable reference to one decisive extension-stable transcript prefix."""

    transcript_id: str
    sequence: int
    look: int
    motif: str
    outer_status: str
    extension_status: str
    canonical_manifest_digest: str
    entry_digest: str
    prefix_head_digest: str
    genesis_digest: str

    def __post_init__(self) -> None:
        _require_nonempty(self.transcript_id, "transcript_id")
        if not isinstance(self.sequence, int) or self.sequence < 1:
            raise ValueError("anchor sequence must be a positive integer")
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("anchor look must be a positive integer")
        _require_nonempty(self.motif, "anchor motif")
        outer = MotifStatus(self.outer_status)
        extension = ExtensionStatus(self.extension_status)
        if outer not in (MotifStatus.INVARIANT, MotifStatus.EXCLUDED):
            raise ValueError("a transcript decision anchor needs a decisive outer status")
        if extension is not ExtensionStatus.EXTENSION_STABLE:
            raise ValueError("a transcript decision anchor needs extension-stable status")
        for value, name in (
            (self.canonical_manifest_digest, "canonical_manifest_digest"),
            (self.entry_digest, "entry_digest"),
            (self.prefix_head_digest, "prefix_head_digest"),
            (self.genesis_digest, "genesis_digest"),
        ):
            _require_digest(value, name)


def create_admission_transcript_header(
    *,
    transcript_id: str,
    verified_schema: VerifiedExactPolyhedralExtensionAdmissionSchema,
    manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    admission_schema_artifact: ArtifactReference,
) -> AdmissionTranscriptHeader:
    """Bind one exact admission schema to a manifest target and coverage theorem.

    The provided artifact is an external content commitment to the serialized
    base systems and admission-schema proof material. This module does not invent
    that serialization; it records its SHA-256 alongside the live theorem context.
    """

    verify_manifest_context(
        manifest,
        space=verified_schema.target.space,
        coverage_certificate=coverage_certificate,
        solver_certificate=verified_schema.all_look_solver_certificate,
    )
    return AdmissionTranscriptHeader(
        transcript_id=transcript_id,
        target_digest=manifest.target.target_digest,
        motifs=verified_schema.target.space.motifs,
        required_cell_ids=verified_schema.target.required_cell_ids,
        admission_schema_artifact=admission_schema_artifact,
        schema_context_digest=admission_schema_context_digest(verified_schema),
    )


def _validate_header_against_live_inputs(
    header: AdmissionTranscriptHeader,
    *,
    verified_schema: VerifiedExactPolyhedralExtensionAdmissionSchema,
    manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> None:
    verify_manifest_context(
        manifest,
        space=verified_schema.target.space,
        coverage_certificate=coverage_certificate,
        solver_certificate=verified_schema.all_look_solver_certificate,
    )
    if header.target_digest != manifest.target.target_digest:
        raise ValueError("manifest target digest does not match the transcript header")
    if header.motifs != verified_schema.target.space.motifs:
        raise ValueError("live motif vocabulary does not match the transcript header")
    if header.required_cell_ids != verified_schema.target.required_cell_ids:
        raise ValueError("live required cell IDs do not match the transcript header")
    if header.schema_context_digest != admission_schema_context_digest(verified_schema):
        raise ValueError("live exact-admission schema context does not match the transcript header")


def verify_admission_transcript(
    transcript: AdmissionTranscript,
    *,
    expected_head_digest: str | None = None,
) -> AdmissionTranscriptVerificationReport:
    """Verify one transcript's hash chain and optional externally retained head.

    Supplying a known head digest detects suffix deletion / rollback. Without an
    external head, a shorter valid prefix remains internally valid by design.
    """

    header = transcript.header
    previous = header.genesis_digest
    previous_look = 0
    for expected_sequence, entry in enumerate(transcript.entries, start=1):
        if entry.sequence != expected_sequence:
            raise ValueError("transcript entry sequences must be contiguous from one")
        if entry.look <= previous_look:
            raise ValueError("transcript look IDs must be strictly increasing")
        if entry.previous_entry_digest != previous:
            raise ValueError("transcript previous-entry hash link is broken")
        if entry.schema_context_digest != header.schema_context_digest:
            raise ValueError("transcript entry schema context does not match the header")
        if set(entry.outer_statuses) != set(header.motifs):
            raise ValueError("transcript entry outer statuses do not match header motifs")
        if set(entry.extension_statuses) != set(header.motifs):
            raise ValueError("transcript entry extension statuses do not match header motifs")
        previous = entry.entry_digest
        previous_look = entry.look
    if expected_head_digest is not None:
        _require_digest(expected_head_digest, "expected_head_digest")
        if previous != expected_head_digest:
            raise ValueError("transcript head does not match expected_head_digest")
    return AdmissionTranscriptVerificationReport(
        transcript_id=header.transcript_id,
        entry_count=len(transcript.entries),
        recorded_looks=tuple(entry.look for entry in transcript.entries),
        genesis_digest=header.genesis_digest,
        head_digest=previous,
    )


def append_admitted_look(
    transcript: AdmissionTranscript,
    *,
    verified_schema: VerifiedExactPolyhedralExtensionAdmissionSchema,
    admitted_look: VerifiedExactPolyhedralExtensionLook,
    manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> AdmissionTranscript:
    """Append one exact-admitted paired snapshot after rechecking all bindings.

    This function does not accept raw statuses. It recomputes outer and extension
    statuses from the supplied exact-admitted snapshot and the live all-look
    certificates. Consequently a transcript entry cannot claim
    ``EXTENSION_STABLE`` unless the ordinary #16 audit returns that label.
    """

    report = verify_admission_transcript(transcript)
    _validate_header_against_live_inputs(
        transcript.header,
        verified_schema=verified_schema,
        manifest=manifest,
        coverage_certificate=coverage_certificate,
    )
    if admitted_look.look != admitted_look.snapshot.look:
        raise ValueError("admitted look ID and snapshot look ID must match")
    if admitted_look.verified_inclusion_look.look != admitted_look.look:
        raise ValueError("admitted look ID and inclusion-admission look ID must match")
    if admitted_look.snapshot.target != verified_schema.target:
        raise ValueError("admitted snapshot target does not match the exact-admission schema")
    if not manifest.target.covers_look(admitted_look.look):
        raise ValueError("admitted look lies outside the manifest target scope")
    if not coverage_certificate.covers_look(admitted_look.look):
        raise ValueError("admitted look lies outside the coverage certificate scope")
    if transcript.entries and admitted_look.look <= transcript.entries[-1].look:
        raise ValueError("a new admitted look must be strictly later than the transcript head")

    anytime_report = audit_anytime_symbolic_universe_extension(
        (admitted_look.snapshot,),
        inclusion_certificate=verified_schema.all_look_inclusion_certificate,
        coverage_certificate=coverage_certificate,
        solver_certificate=verified_schema.all_look_solver_certificate,
    )
    static_report = anytime_report.reports_by_look[admitted_look.look]
    entry = AdmissionTranscriptEntry(
        sequence=report.entry_count + 1,
        look=admitted_look.look,
        previous_entry_digest=report.head_digest,
        canonical_manifest_digest=canonical_manifest_digest(manifest),
        schema_context_digest=transcript.header.schema_context_digest,
        admission_evidence_reference=admitted_look.evidence_reference,
        inclusion_evidence_reference=admitted_look.verified_inclusion_look.evidence_reference,
        admission_verifier=admitted_look.verifier,
        outer_statuses={
            motif: static_report.motifs[motif].outer_status.value
            for motif in transcript.header.motifs
        },
        extension_statuses={
            motif: static_report.motifs[motif].extension_status.value
            for motif in transcript.header.motifs
        },
    )
    return AdmissionTranscript(header=transcript.header, entries=(*transcript.entries, entry))


def create_transcript_decision_anchor(
    transcript: AdmissionTranscript,
    *,
    look: int,
    motif: str,
) -> TranscriptDecisionAnchor:
    """Anchor one extension-stable decisive result to its transcript prefix.

    The anchor stays verifiable after later entries are appended because it names
    the historical entry digest, not merely the current transcript head.
    """

    report = verify_admission_transcript(transcript)
    if motif not in transcript.header.motifs:
        raise ValueError("anchor motif is absent from the transcript header")
    matches = [entry for entry in transcript.entries if entry.look == look]
    if len(matches) != 1:
        raise ValueError("anchor look must occur exactly once in the transcript")
    entry = matches[0]
    outer = entry.outer_statuses[motif]
    extension = entry.extension_statuses[motif]
    if ExtensionStatus(extension) is not ExtensionStatus.EXTENSION_STABLE:
        raise ValueError("only extension-stable transcript entries can anchor a decisive claim")
    if MotifStatus(outer) not in (MotifStatus.INVARIANT, MotifStatus.EXCLUDED):
        raise ValueError("only decisive outer transcript entries can anchor a decision")
    return TranscriptDecisionAnchor(
        transcript_id=transcript.header.transcript_id,
        sequence=entry.sequence,
        look=entry.look,
        motif=motif,
        outer_status=outer,
        extension_status=extension,
        canonical_manifest_digest=entry.canonical_manifest_digest,
        entry_digest=entry.entry_digest,
        prefix_head_digest=entry.entry_digest,
        genesis_digest=report.genesis_digest,
    )


def verify_transcript_decision_anchor(
    transcript: AdmissionTranscript,
    anchor: TranscriptDecisionAnchor,
) -> None:
    """Verify an anchored decision against the matching immutable transcript prefix."""

    report = verify_admission_transcript(transcript)
    if anchor.transcript_id != transcript.header.transcript_id:
        raise ValueError("decision anchor transcript ID does not match")
    if anchor.genesis_digest != report.genesis_digest:
        raise ValueError("decision anchor genesis digest does not match")
    if anchor.sequence > len(transcript.entries):
        raise ValueError("decision anchor sequence lies beyond the supplied transcript")
    entry = transcript.entries[anchor.sequence - 1]
    if (
        entry.look != anchor.look
        or entry.entry_digest != anchor.entry_digest
        or entry.entry_digest != anchor.prefix_head_digest
        or entry.canonical_manifest_digest != anchor.canonical_manifest_digest
        or entry.outer_statuses.get(anchor.motif) != anchor.outer_status
        or entry.extension_statuses.get(anchor.motif) != anchor.extension_status
    ):
        raise ValueError("decision anchor does not match the named transcript entry")
