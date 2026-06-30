"""Bind proof-carrying all-look coverage contracts into native v2 histories.

A native tiered transcript already commits each admitted look to exact compiler
plans, proof families, and a per-look tier-aware manifest.  This module binds
one fixed all-look coverage contract into the transcript *genesis* and checks
that every per-look v2 manifest carries the same target and coverage assertion.

The contract is all-look, so it belongs in the immutable header rather than
being redundantly copied into every entry.  The generic transcript genesis hash
therefore commits to the coverage-contract artifact; every later entry and every
Ed25519 signed checkpoint head inherits that commitment.

A coverage-bound v2 manifest wrapper additionally supplies a direct canonical
artifact combining the exact v2 manifest bytes with the exact coverage-contract
bytes.  It is derived during append/verification, never hand-authored by callers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .all_look_coverage_contract import (
    AllLookCoverageContract,
    CoverageProofVerifier,
    CoverageProofVerificationReceipt,
    coverage_contract_artifact,
    verify_all_look_coverage_contract,
    verify_all_look_coverage_contract_context,
)
from .anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from .canonical_tiered_manifest_json import canonical_tiered_manifest_bytes, canonical_tiered_manifest_digest
from .certificate_manifest import ArtifactReference, CertificateManifest, canonical_json
from .native_tiered_admission_transcript import (
    NATIVE_TIERED_ADMISSION_TRANSCRIPT_FORMAT,
    NativeTieredAdmissionTranscript,
    NativeTieredAdmissionTranscriptVerificationReport,
    append_native_tiered_admitted_look,
    build_native_tiered_manifest_for_admitted_look,
    create_native_tiered_admission_transcript,
    create_native_tiered_transcript_head_checkpoint,
    verify_native_tiered_admission_transcript,
    verify_signed_native_tiered_transcript_checkpoint,
)
from .exact_compiled_polyhedral_extension_admission import (
    VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    VerifiedExactCompiledPolyhedralExtensionLook,
)
from .signed_transcript_checkpoint import (
    Ed25519VerifierKey,
    SignedCheckpointVerificationReport,
    SignedTranscriptCheckpoint,
    TranscriptHeadCheckpoint,
)
from .tiered_certificate_manifest import TieredCertificateManifest


COVERAGE_BOUND_NATIVE_TRANSCRIPT_FORMAT = "rach-coverage-bound-native-tiered-transcript/v1"
COVERAGE_BOUND_SCHEMA_ARTIFACT_ID = "coverage-bound-native-admission-schema"
COVERAGE_BOUND_TIERED_MANIFEST_ARTIFACT_PREFIX = "coverage-bound-tiered-manifest"


def _artifact_object(artifact: ArtifactReference) -> dict[str, str]:
    return {
        "artifact_id": artifact.artifact_id,
        "media_type": artifact.media_type,
        "sha256": artifact.sha256,
    }


@dataclass(frozen=True)
class CoverageBoundTieredManifest:
    """One v2 manifest bound to the all-look contract that supplies its alpha."""

    tiered_manifest: TieredCertificateManifest
    coverage_contract: AllLookCoverageContract
    coverage_contract_artifact: ArtifactReference

    def __post_init__(self) -> None:
        if self.coverage_contract_artifact.sha256 != self.coverage_contract.contract_digest:
            raise ValueError("coverage contract artifact does not hash the canonical coverage contract")
        target = self.tiered_manifest.target
        assertion = self.tiered_manifest.coverage_assertion
        contract = self.coverage_contract
        if contract.target_digest != target.target_digest:
            raise ValueError("coverage contract target does not match the tiered manifest target")
        if contract.candidate_space_artifact != target.candidate_space_artifact:
            raise ValueError("coverage contract candidate space does not match the tiered manifest target")
        if contract.required_cell_ids != target.required_cell_ids:
            raise ValueError("coverage contract cells do not match the tiered manifest target")
        if contract.certified_looks != target.certified_looks:
            raise ValueError("coverage contract look scope does not match the tiered manifest target")
        if contract.lower_bound != assertion.lower_bound:
            raise ValueError("coverage contract lower bound does not match the tiered manifest assertion")
        if contract.method != assertion.method:
            raise ValueError("coverage contract method does not match the tiered manifest assertion")
        if contract.assumptions != assertion.assumptions:
            raise ValueError("coverage contract assumptions do not match the tiered manifest assertion")

    @property
    def payload(self) -> bytes:
        tiered_artifact = ArtifactReference.from_payload(
            "tiered-manifest-v2",
            canonical_tiered_manifest_bytes(self.tiered_manifest),
            media_type="application/json",
        )
        return canonical_json(
            {
                "format_version": COVERAGE_BOUND_NATIVE_TRANSCRIPT_FORMAT,
                "tiered_manifest_artifact": _artifact_object(tiered_artifact),
                "tiered_manifest_canonical_digest": canonical_tiered_manifest_digest(
                    self.tiered_manifest
                ),
                "coverage_contract_artifact": _artifact_object(self.coverage_contract_artifact),
                "coverage_contract_digest": self.coverage_contract.contract_digest,
            }
        ).encode("utf-8")

    @property
    def artifact(self) -> ArtifactReference:
        return ArtifactReference.from_payload(
            f"{COVERAGE_BOUND_TIERED_MANIFEST_ARTIFACT_PREFIX}:"
            f"{canonical_tiered_manifest_digest(self.tiered_manifest)}",
            self.payload,
            media_type="application/json",
        )


@dataclass(frozen=True)
class CoverageBoundNativeTieredAdmissionTranscript:
    """Fresh native-v2 history whose genesis commits to a verified coverage contract."""

    native_transcript: NativeTieredAdmissionTranscript
    coverage_contract: AllLookCoverageContract
    coverage_contract_artifact: ArtifactReference
    base_admission_schema_artifact: ArtifactReference

    @property
    def head_digest(self) -> str:
        return self.native_transcript.head_digest


@dataclass(frozen=True)
class CoverageBoundNativeTranscriptVerificationReport:
    """Successful native proof/history verification with fixed coverage identity."""

    native_report: NativeTieredAdmissionTranscriptVerificationReport
    coverage_contract_digest: str
    coverage_contract_artifact_sha256: str
    coverage_bound_tiered_manifest_digests: tuple[str, ...]
    coverage_proof_receipt: CoverageProofVerificationReceipt | None


def coverage_bound_schema_artifact(
    *,
    base_admission_schema_artifact: ArtifactReference,
    coverage_contract: AllLookCoverageContract,
    coverage_contract_reference: ArtifactReference | None = None,
) -> ArtifactReference:
    """Build the immutable genesis artifact joining exact admission and coverage proof."""

    contract_artifact = coverage_contract_reference or coverage_contract_artifact(coverage_contract)
    if contract_artifact.sha256 != coverage_contract.contract_digest:
        raise ValueError("coverage contract reference does not hash the canonical contract")
    payload = canonical_json(
        {
            "format_version": COVERAGE_BOUND_NATIVE_TRANSCRIPT_FORMAT,
            "base_admission_schema_artifact": _artifact_object(base_admission_schema_artifact),
            "coverage_contract_artifact": _artifact_object(contract_artifact),
            "coverage_contract_digest": coverage_contract.contract_digest,
            "native_transcript_format": NATIVE_TIERED_ADMISSION_TRANSCRIPT_FORMAT,
        }
    ).encode("utf-8")
    return ArtifactReference.from_payload(
        COVERAGE_BOUND_SCHEMA_ARTIFACT_ID,
        payload,
        media_type="application/json",
    )


def create_coverage_bound_native_tiered_admission_transcript(
    *,
    transcript_id: str,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    coverage_contract: AllLookCoverageContract,
    base_admission_schema_artifact: ArtifactReference,
) -> CoverageBoundNativeTieredAdmissionTranscript:
    """Create a fresh signed-history-ready path with a fixed all-look contract."""

    verify_all_look_coverage_contract_context(
        coverage_contract,
        target=source_v1_manifest.target,
        coverage_certificate=coverage_certificate,
    )
    contract_artifact = coverage_contract_artifact(coverage_contract)
    bound_schema = coverage_bound_schema_artifact(
        base_admission_schema_artifact=base_admission_schema_artifact,
        coverage_contract=coverage_contract,
        coverage_contract_reference=contract_artifact,
    )
    native = create_native_tiered_admission_transcript(
        transcript_id=transcript_id,
        verified_schema=verified_schema,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
        base_admission_schema_artifact=bound_schema,
    )
    return CoverageBoundNativeTieredAdmissionTranscript(
        native_transcript=native,
        coverage_contract=coverage_contract,
        coverage_contract_artifact=contract_artifact,
        base_admission_schema_artifact=base_admission_schema_artifact,
    )


def _verify_coverage_bound_header(
    transcript: CoverageBoundNativeTieredAdmissionTranscript,
    *,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> None:
    verify_all_look_coverage_contract_context(
        transcript.coverage_contract,
        target=source_v1_manifest.target,
        coverage_certificate=coverage_certificate,
    )
    if transcript.coverage_contract_artifact.sha256 != transcript.coverage_contract.contract_digest:
        raise ValueError("coverage-bound transcript contract artifact does not hash the contract")
    expected = coverage_bound_schema_artifact(
        base_admission_schema_artifact=transcript.base_admission_schema_artifact,
        coverage_contract=transcript.coverage_contract,
        coverage_contract_reference=transcript.coverage_contract_artifact,
    )
    actual = transcript.native_transcript.header.schema_artifacts.base_admission_schema_artifact
    if actual != expected:
        raise ValueError("native transcript genesis does not bind the declared coverage contract")


def verify_coverage_bound_native_tiered_admission_transcript(
    transcript: CoverageBoundNativeTieredAdmissionTranscript,
    *,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    expected_head_digest: str | None = None,
    coverage_artifact_payloads: Mapping[str, str | bytes] | None = None,
    coverage_verifier: CoverageProofVerifier | None = None,
) -> CoverageBoundNativeTranscriptVerificationReport:
    """Verify native history, all-look coverage identity, and optional proof replay.

    Passing both ``coverage_artifact_payloads`` and ``coverage_verifier`` invokes
    the method-specific proof verifier. Passing neither verifies the contract's
    static target/header binding only. Passing exactly one is rejected.
    """

    if (coverage_artifact_payloads is None) != (coverage_verifier is None):
        raise ValueError("coverage_artifact_payloads and coverage_verifier must be supplied together")
    _verify_coverage_bound_header(
        transcript,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
    )
    native_report = verify_native_tiered_admission_transcript(
        transcript.native_transcript,
        expected_head_digest=expected_head_digest,
    )
    bound_digests: list[str] = []
    for entry in transcript.native_transcript.entries:
        bound = CoverageBoundTieredManifest(
            tiered_manifest=entry.evidence.tiered_bundle.manifest,
            coverage_contract=transcript.coverage_contract,
            coverage_contract_artifact=transcript.coverage_contract_artifact,
        )
        bound_digests.append(bound.artifact.sha256)
    receipt = None
    if coverage_verifier is not None and coverage_artifact_payloads is not None:
        receipt = verify_all_look_coverage_contract(
            transcript.coverage_contract,
            target=source_v1_manifest.target,
            coverage_certificate=coverage_certificate,
            artifact_payloads=coverage_artifact_payloads,
            verifier=coverage_verifier,
        )
    return CoverageBoundNativeTranscriptVerificationReport(
        native_report=native_report,
        coverage_contract_digest=transcript.coverage_contract.contract_digest,
        coverage_contract_artifact_sha256=transcript.coverage_contract_artifact.sha256,
        coverage_bound_tiered_manifest_digests=tuple(bound_digests),
        coverage_proof_receipt=receipt,
    )


def append_coverage_bound_native_tiered_admitted_look(
    transcript: CoverageBoundNativeTieredAdmissionTranscript,
    *,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    admitted_look: VerifiedExactCompiledPolyhedralExtensionLook,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> CoverageBoundNativeTieredAdmissionTranscript:
    """Append only after coverage identity and per-look v2 compatibility are checked."""

    verify_coverage_bound_native_tiered_admission_transcript(
        transcript,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
    )
    proposed_evidence = build_native_tiered_manifest_for_admitted_look(
        verified_schema=verified_schema,
        admitted_look=admitted_look,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
    )
    CoverageBoundTieredManifest(
        tiered_manifest=proposed_evidence.tiered_bundle.manifest,
        coverage_contract=transcript.coverage_contract,
        coverage_contract_artifact=transcript.coverage_contract_artifact,
    )
    appended = append_native_tiered_admitted_look(
        transcript.native_transcript,
        verified_schema=verified_schema,
        admitted_look=admitted_look,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
    )
    return CoverageBoundNativeTieredAdmissionTranscript(
        native_transcript=appended,
        coverage_contract=transcript.coverage_contract,
        coverage_contract_artifact=transcript.coverage_contract_artifact,
        base_admission_schema_artifact=transcript.base_admission_schema_artifact,
    )


def create_coverage_bound_native_tiered_transcript_head_checkpoint(
    transcript: CoverageBoundNativeTieredAdmissionTranscript,
    *,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    checkpoint_sequence: int,
) -> TranscriptHeadCheckpoint:
    """Create a standard checkpoint only after coverage-bound native verification."""

    verify_coverage_bound_native_tiered_admission_transcript(
        transcript,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
    )
    return create_native_tiered_transcript_head_checkpoint(
        transcript.native_transcript,
        checkpoint_sequence=checkpoint_sequence,
    )


def verify_signed_coverage_bound_native_tiered_transcript_checkpoint(
    transcript: CoverageBoundNativeTieredAdmissionTranscript,
    signed_checkpoint: SignedTranscriptCheckpoint,
    *,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    trusted_key: Ed25519VerifierKey,
) -> SignedCheckpointVerificationReport:
    """Verify coverage header/native evidence first, then the established checkpoint."""

    verify_coverage_bound_native_tiered_admission_transcript(
        transcript,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
    )
    return verify_signed_native_tiered_transcript_checkpoint(
        transcript.native_transcript,
        signed_checkpoint,
        trusted_key=trusted_key,
    )
