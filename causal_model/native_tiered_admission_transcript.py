"""Native manifest-v2 transcripts for compiler-admitted RACH looks.

PR #25 commits tier-aware compiler plans and role-proof families in an
append-only transcript. PR #26 introduces a native tier-aware manifest whose
proof keys contain ``(tier, look, cell, motif, role)``. This module joins them
without changing historical v1 transcript records.

A native-v2 entry is constructed only from a #24 admitted look and a live v1
source manifest. The adapter deterministically derives:

* all inner/outer compiled plan artifacts;
* all role-family artifacts and their exact aggregate SAT/UNSAT/UNKNOWN status;
* a per-look ``TieredCertificateManifest`` containing every plan and every
  decisive role family; and
* an artifact whose bytes are the strict canonical v2 manifest bytes.

The native entry commitment includes the source v1 canonical digest and the v2
canonical digest. It becomes the generic transcript entry's
``admission_evidence_reference``. Hence an unchanged generic hash chain and
Ed25519 checkpoint now commit directly to the exact bytes of the native v2
manifest.

UNKNOWN role families are intentionally not converted into v2 decisive proof
bindings. They remain in the status table and compiler evidence commitment, so
absence from the v2 decisive-proof set cannot be misread as an omitted artifact.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .admission_transcript import (
    AdmissionTranscript,
    AdmissionTranscriptEntry,
    AdmissionTranscriptVerificationReport,
    verify_admission_transcript,
)
from .anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from .canonical_manifest_json import canonical_manifest_digest
from .canonical_tiered_manifest_json import (
    canonical_tiered_manifest_bytes,
    canonical_tiered_manifest_digest,
)
from .certificate_manifest import (
    ArtifactReference,
    CertificateManifest,
    QueryRole,
    canonical_json,
    sha256_digest,
)
from .compiled_admission_transcript import (
    COMPILED_ADMISSION_TRANSCRIPT_FORMAT,
    CompiledAdmissionEntryEvidence,
    CompiledAdmissionSchemaArtifacts,
    CompiledAdmissionTranscriptHeader,
    CompiledPlanArtifactBinding,
    CompiledRoleProofArtifactBinding,
    create_compiled_admission_transcript,
)
from .exact_compiled_polyhedral_extension_admission import (
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
from .symbolic_candidate_sets import FeasibilityStatus
from .tiered_certificate_manifest import (
    QueryTier,
    TieredCertificateManifest,
    TieredQueryPlanBinding,
    TieredSolverQueryProofBinding,
    build_anytime_tiered_symbolic_manifest,
)


NATIVE_TIERED_ADMISSION_TRANSCRIPT_FORMAT = "rach-native-tiered-admission-transcript/v1"
NATIVE_TIERED_ADMISSION_ENTRY_ARTIFACT_PREFIX = "native-tiered-admission-entry/v1:"
NATIVE_TIERED_MANIFEST_ARTIFACT_PREFIX = "native-tiered-manifest-v2"
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


def _query_tier(value: str) -> QueryTier:
    try:
        return QueryTier(value)
    except ValueError as error:
        raise ValueError("compiler evidence tier must be 'inner' or 'outer'") from error


def _role_certificate_status(queries: object, motif: str, role: QueryRole) -> FeasibilityStatus:
    motif_queries = queries.motif_queries[motif]
    if role is QueryRole.NONEMPTY:
        return motif_queries.nonempty.status
    if role is QueryRole.ACTIVE:
        return motif_queries.active.status
    if role is QueryRole.INACTIVE:
        return motif_queries.inactive.status
    raise ValueError("unsupported query role")


@dataclass(frozen=True)
class NativeTieredRoleStatusBinding:
    """One exact aggregate compiler role status, including UNKNOWN when present."""

    tier: QueryTier
    cell_id: str
    motif: str
    role: QueryRole
    status: FeasibilityStatus

    def __post_init__(self) -> None:
        if not isinstance(self.tier, QueryTier):
            raise ValueError("native role status tier must be a QueryTier")
        _require_nonempty(self.cell_id, "native role status cell_id")
        _require_nonempty(self.motif, "native role status motif")
        if not isinstance(self.role, QueryRole):
            raise ValueError("native role status role must be a QueryRole")
        if self.status not in (
            FeasibilityStatus.SAT,
            FeasibilityStatus.UNSAT,
            FeasibilityStatus.UNKNOWN,
        ):
            raise ValueError("native role status must be SAT, UNSAT, or UNKNOWN")

    @property
    def key(self) -> tuple[QueryTier, str, str, QueryRole]:
        return (self.tier, self.cell_id, self.motif, self.role)


@dataclass(frozen=True)
class NativeTieredManifestBundle:
    """Per-look v2 bytes and the status table needed to audit their completeness."""

    source_v1_manifest_digest: str
    manifest: TieredCertificateManifest
    manifest_artifact: ArtifactReference
    role_statuses: tuple[NativeTieredRoleStatusBinding, ...]

    def __post_init__(self) -> None:
        _require_digest(self.source_v1_manifest_digest, "source_v1_manifest_digest")
        expected = canonical_tiered_manifest_digest(self.manifest)
        if self.manifest_artifact.sha256 != expected:
            raise ValueError("native tiered manifest artifact does not hash the canonical v2 manifest")

    @property
    def canonical_digest(self) -> str:
        return canonical_tiered_manifest_digest(self.manifest)


@dataclass(frozen=True)
class NativeTieredAdmissionEntryEvidence:
    """Compiler evidence plus the direct canonical-v2 manifest commitment for one look."""

    compiler_evidence: CompiledAdmissionEntryEvidence
    tiered_bundle: NativeTieredManifestBundle

    def __post_init__(self) -> None:
        if self.compiler_evidence.look < 1:
            raise ValueError("native entry evidence needs a positive compiler look")

    @property
    def look(self) -> int:
        return self.compiler_evidence.look

    @property
    def commitment_payload(self) -> bytes:
        bundle = self.tiered_bundle
        return canonical_json(
            {
                "format_version": NATIVE_TIERED_ADMISSION_TRANSCRIPT_FORMAT,
                "look": self.look,
                "compiler_evidence_commitment": _artifact_object(
                    self.compiler_evidence.commitment_artifact
                ),
                "source_v1_manifest_digest": bundle.source_v1_manifest_digest,
                "tiered_manifest_artifact": _artifact_object(bundle.manifest_artifact),
                "tiered_manifest_canonical_digest": bundle.canonical_digest,
                "role_statuses": [
                    {
                        "tier": status.tier.value,
                        "cell_id": status.cell_id,
                        "motif": status.motif,
                        "role": status.role.value,
                        "status": status.status.value,
                    }
                    for status in sorted(
                        bundle.role_statuses,
                        key=lambda item: (
                            item.tier.value,
                            item.cell_id,
                            item.motif,
                            item.role.value,
                        ),
                    )
                ],
            }
        ).encode("utf-8")

    @property
    def commitment_artifact(self) -> ArtifactReference:
        return ArtifactReference.from_payload(
            f"native-tiered-admission-entry:look-{self.look}",
            self.commitment_payload,
            media_type="application/json",
        )

    @property
    def commitment_reference(self) -> str:
        return f"{NATIVE_TIERED_ADMISSION_ENTRY_ARTIFACT_PREFIX}{self.commitment_artifact.sha256}"


@dataclass(frozen=True)
class NativeTieredAdmissionTranscriptEntry:
    """One native-v2 evidence record paired with a generic chain entry."""

    sequence: int
    evidence: NativeTieredAdmissionEntryEvidence
    base_entry_digest: str

    def __post_init__(self) -> None:
        if not isinstance(self.sequence, int) or self.sequence < 1:
            raise ValueError("native tiered transcript entry sequence must be a positive integer")
        _require_digest(self.base_entry_digest, "base_entry_digest")

    @property
    def look(self) -> int:
        return self.evidence.look


@dataclass(frozen=True)
class NativeTieredAdmissionTranscript:
    """A fresh v2-native history using the stable generic chain and checkpoint wire format."""

    header: CompiledAdmissionTranscriptHeader
    chain: AdmissionTranscript
    entries: tuple[NativeTieredAdmissionTranscriptEntry, ...] = ()

    @property
    def head_digest(self) -> str:
        return self.chain.head_digest


@dataclass(frozen=True)
class NativeTieredAdmissionTranscriptVerificationReport:
    """Successful native-v2 evidence and generic-chain verification result."""

    transcript_id: str
    entry_count: int
    recorded_looks: tuple[int, ...]
    genesis_digest: str
    head_digest: str
    native_tiered_manifest_digests: tuple[str, ...]


def _expected_plan_keys(header: CompiledAdmissionTranscriptHeader) -> set[tuple[str, str]]:
    return {
        (tier, cell_id)
        for tier in ("inner", "outer")
        for cell_id in header.transcript_header.required_cell_ids
    }


def _expected_role_keys(header: CompiledAdmissionTranscriptHeader) -> set[tuple[QueryTier, str, str, QueryRole]]:
    return {
        (tier, cell_id, motif, role)
        for tier in (QueryTier.INNER, QueryTier.OUTER)
        for cell_id in header.transcript_header.required_cell_ids
        for motif in header.transcript_header.motifs
        for role in (QueryRole.NONEMPTY, QueryRole.ACTIVE, QueryRole.INACTIVE)
    }


def _validate_compiler_evidence_layout(
    header: CompiledAdmissionTranscriptHeader,
    evidence: CompiledAdmissionEntryEvidence,
) -> None:
    if evidence.partition_artifact != header.schema_artifacts.partition_artifact:
        raise ValueError("native entry partition artifact does not match the transcript header")
    plan_keys = {(binding.tier, binding.cell_id) for binding in evidence.plan_artifacts}
    if plan_keys != _expected_plan_keys(header) or len(plan_keys) != len(evidence.plan_artifacts):
        raise ValueError("native entry needs exactly one plan artifact per tier and required cell")
    role_keys = {
        (_query_tier(binding.tier), binding.cell_id, binding.motif, binding.role)
        for binding in evidence.role_proof_artifacts
    }
    if role_keys != _expected_role_keys(header) or len(role_keys) != len(evidence.role_proof_artifacts):
        raise ValueError("native entry needs exactly one role artifact per tier/cell/motif/role")


def _role_artifacts_by_key(
    evidence: CompiledAdmissionEntryEvidence,
) -> Mapping[tuple[QueryTier, str, str, QueryRole], ArtifactReference]:
    return {
        (_query_tier(binding.tier), binding.cell_id, binding.motif, binding.role): binding.artifact
        for binding in evidence.role_proof_artifacts
    }


def _plan_artifacts_by_key(
    evidence: CompiledAdmissionEntryEvidence,
) -> Mapping[tuple[QueryTier, str], ArtifactReference]:
    return {
        (_query_tier(binding.tier), binding.cell_id): binding.artifact
        for binding in evidence.plan_artifacts
    }


def _validate_native_bundle(
    header: CompiledAdmissionTranscriptHeader,
    evidence: NativeTieredAdmissionEntryEvidence,
) -> None:
    compiler = evidence.compiler_evidence
    bundle = evidence.tiered_bundle
    _validate_compiler_evidence_layout(header, compiler)
    if bundle.source_v1_manifest_digest == "":
        raise ValueError("native tiered bundle needs a source v1 manifest digest")
    manifest = bundle.manifest
    if manifest.target.target_digest != header.transcript_header.target_digest:
        raise ValueError("native tiered manifest target does not match the transcript header")
    if manifest.semantic_partition_artifact != compiler.partition_artifact:
        raise ValueError("native tiered manifest partition does not match compiler evidence")
    if bundle.manifest_artifact.artifact_id != f"{NATIVE_TIERED_MANIFEST_ARTIFACT_PREFIX}:look-{compiler.look}":
        raise ValueError("native tiered manifest artifact ID does not match its look")
    expected_plan_artifacts = _plan_artifacts_by_key(compiler)
    observed_plans = {
        (binding.tier, binding.cell_id): binding.query_plan_artifact
        for binding in manifest.tiered_query_plans
    }
    if len(observed_plans) != len(manifest.tiered_query_plans):
        raise ValueError("native tiered manifest plan bindings are duplicated")
    if set(observed_plans) != set(expected_plan_artifacts):
        raise ValueError("native tiered manifest plans do not match compiler evidence tiers/cells")
    if any(binding.look != compiler.look for binding in manifest.tiered_query_plans):
        raise ValueError("native tiered manifest plan look does not match compiler evidence look")
    if observed_plans != expected_plan_artifacts:
        raise ValueError("native tiered manifest plan artifacts do not match compiler evidence")

    statuses = {status.key: status for status in bundle.role_statuses}
    if len(statuses) != len(bundle.role_statuses) or set(statuses) != _expected_role_keys(header):
        raise ValueError("native tiered bundle needs exactly one aggregate status per tier/cell/motif/role")
    role_artifacts = _role_artifacts_by_key(compiler)
    expected_proofs: dict[tuple[QueryTier, int, str, str, QueryRole], tuple[FeasibilityStatus, ArtifactReference, ArtifactReference]] = {}
    for key, status_binding in statuses.items():
        tier, cell_id, motif, role = key
        if status_binding.status in (FeasibilityStatus.SAT, FeasibilityStatus.UNSAT):
            expected_proofs[(tier, compiler.look, cell_id, motif, role)] = (
                status_binding.status,
                expected_plan_artifacts[(tier, cell_id)],
                role_artifacts[key],
            )
    observed_proofs = {binding.query_key: binding for binding in manifest.solver_query_proofs}
    if len(observed_proofs) != len(manifest.solver_query_proofs):
        raise ValueError("native tiered manifest proof bindings are duplicated")
    if set(observed_proofs) != set(expected_proofs):
        raise ValueError("native tiered manifest decisive proof keys do not match role statuses")
    for key, (status, plan_artifact, proof_artifact) in expected_proofs.items():
        binding = observed_proofs[key]
        if (
            binding.status is not status
            or binding.query_plan_artifact != plan_artifact
            or binding.proof_artifact != proof_artifact
            or binding.verifier_id != compiler.admission_verifier
        ):
            raise ValueError("native tiered manifest decisive proof does not match compiler evidence")


def _build_compiler_evidence(
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    admitted_look: VerifiedExactCompiledPolyhedralExtensionLook,
) -> tuple[CompiledAdmissionEntryEvidence, Mapping[tuple[QueryTier, str, str, QueryRole], FeasibilityStatus]]:
    plan_bindings: list[CompiledPlanArtifactBinding] = []
    role_bindings: list[CompiledRoleProofArtifactBinding] = []
    statuses: dict[tuple[QueryTier, str, str, QueryRole], FeasibilityStatus] = {}
    for tier_name, tier, queries_by_cell in (
        ("inner", QueryTier.INNER, admitted_look.inner_queries_by_cell),
        ("outer", QueryTier.OUTER, admitted_look.outer_queries_by_cell),
    ):
        if tuple(queries_by_cell) != verified_schema.target.required_cell_ids:
            raise ValueError("admitted compiler query cells must match required-cell order")
        for cell_id in verified_schema.target.required_cell_ids:
            queries = queries_by_cell[cell_id]
            plan = queries.bound_proofs.plan
            plan_bindings.append(
                CompiledPlanArtifactBinding(
                    tier=tier_name,
                    cell_id=cell_id,
                    artifact=compiled_polyhedral_motif_plan_artifact(
                        plan,
                        artifact_id=f"compiled-plan:{tier_name}:look-{admitted_look.look}:cell-{cell_id}",
                    ),
                )
            )
            for motif in verified_schema.target.space.motifs:
                for role in (QueryRole.NONEMPTY, QueryRole.ACTIVE, QueryRole.INACTIVE):
                    role_bindings.append(
                        CompiledRoleProofArtifactBinding(
                            tier=tier_name,
                            cell_id=cell_id,
                            motif=motif,
                            role=role,
                            artifact=compiled_role_proof_bundle_artifact(
                                queries,
                                motif=motif,
                                role=role,
                                artifact_id=(
                                    f"compiled-role:{tier_name}:look-{admitted_look.look}:"
                                    f"cell-{cell_id}:motif-{motif}:role-{role.value}"
                                ),
                            ),
                        )
                    )
                    statuses[(tier, cell_id, motif, role)] = _role_certificate_status(
                        queries,
                        motif,
                        role,
                    )
    compiler_evidence = CompiledAdmissionEntryEvidence(
        look=admitted_look.look,
        partition_artifact=polyhedral_motif_partition_artifact(verified_schema.verified_partition),
        plan_artifacts=tuple(plan_bindings),
        role_proof_artifacts=tuple(role_bindings),
        original_admission_evidence_reference=admitted_look.evidence_reference,
        original_inclusion_evidence_reference=admitted_look.verified_inclusion_look.evidence_reference,
        admission_verifier=admitted_look.verifier,
    )
    return compiler_evidence, statuses


def build_native_tiered_manifest_for_admitted_look(
    *,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    admitted_look: VerifiedExactCompiledPolyhedralExtensionLook,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> NativeTieredAdmissionEntryEvidence:
    """Derive one exact per-look v2 manifest from a #24 admitted snapshot.

    No plan, role proof, or role status is accepted from the caller.  The
    compiler-admitted look determines all artifacts; the v1 manifest contributes
    the pre-existing target and theorem assertion declarations.
    """

    compiler_evidence, statuses = _build_compiler_evidence(verified_schema, admitted_look)
    _validate_compiler_evidence_layout(
        CompiledAdmissionTranscriptHeader(
            transcript_header=AdmissionTranscript(
                header=create_compiled_admission_transcript(
                    transcript_id="validation-only",
                    verified_schema=verified_schema,
                    manifest=source_v1_manifest,
                    coverage_certificate=coverage_certificate,
                    base_admission_schema_artifact=ArtifactReference.from_payload(
                        "validation-only",
                        b"validation-only",
                    ),
                ).chain.header,
            ).header,
            schema_artifacts=CompiledAdmissionSchemaArtifacts(
                base_admission_schema_artifact=ArtifactReference.from_payload(
                    "validation-only",
                    b"validation-only",
                ),
                partition_artifact=compiler_evidence.partition_artifact,
            ),
            query_namespace=verified_schema.schema.query_namespace,
        ),
        compiler_evidence,
    )
    plan_artifacts = _plan_artifacts_by_key(compiler_evidence)
    role_artifacts = _role_artifacts_by_key(compiler_evidence)
    plan_bindings = tuple(
        TieredQueryPlanBinding(
            tier=tier,
            look=admitted_look.look,
            cell_id=cell_id,
            query_plan_artifact=artifact,
        )
        for (tier, cell_id), artifact in plan_artifacts.items()
    )
    proof_bindings = tuple(
        TieredSolverQueryProofBinding(
            tier=tier,
            look=admitted_look.look,
            cell_id=cell_id,
            motif=motif,
            role=role,
            status=status,
            query_plan_artifact=plan_artifacts[(tier, cell_id)],
            proof_artifact=role_artifacts[(tier, cell_id, motif, role)],
            verifier_id=compiler_evidence.admission_verifier,
        )
        for (tier, cell_id, motif, role), status in statuses.items()
        if status in (FeasibilityStatus.SAT, FeasibilityStatus.UNSAT)
    )
    manifest = build_anytime_tiered_symbolic_manifest(
        target=source_v1_manifest.target,
        coverage_certificate=coverage_certificate,
        solver_certificate=verified_schema.all_look_solver_certificate,
        coverage_assertion=source_v1_manifest.coverage_assertion,
        solver_assertion=source_v1_manifest.solver_assertion,
        semantic_partition_artifact=compiler_evidence.partition_artifact,
        tiered_query_plans=plan_bindings,
        solver_query_proofs=proof_bindings,
    )
    raw = canonical_tiered_manifest_bytes(manifest)
    artifact = ArtifactReference.from_payload(
        f"{NATIVE_TIERED_MANIFEST_ARTIFACT_PREFIX}:look-{admitted_look.look}",
        raw,
        media_type="application/json",
    )
    return NativeTieredAdmissionEntryEvidence(
        compiler_evidence=compiler_evidence,
        tiered_bundle=NativeTieredManifestBundle(
            source_v1_manifest_digest=canonical_manifest_digest(source_v1_manifest),
            manifest=manifest,
            manifest_artifact=artifact,
            role_statuses=tuple(
                NativeTieredRoleStatusBinding(
                    tier=tier,
                    cell_id=cell_id,
                    motif=motif,
                    role=role,
                    status=status,
                )
                for (tier, cell_id, motif, role), status in statuses.items()
            ),
        ),
    )


def create_native_tiered_admission_transcript(
    *,
    transcript_id: str,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    base_admission_schema_artifact: ArtifactReference,
) -> NativeTieredAdmissionTranscript:
    """Create a fresh transcript whose future entries commit directly to v2 bytes."""

    base = create_compiled_admission_transcript(
        transcript_id=transcript_id,
        verified_schema=verified_schema,
        manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
        base_admission_schema_artifact=base_admission_schema_artifact,
    )
    return NativeTieredAdmissionTranscript(header=base.header, chain=base.chain)


def _validate_live_header(
    transcript: NativeTieredAdmissionTranscript,
    *,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> None:
    expected = create_compiled_admission_transcript(
        transcript_id=transcript.header.transcript_header.transcript_id,
        verified_schema=verified_schema,
        manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
        base_admission_schema_artifact=transcript.header.schema_artifacts.base_admission_schema_artifact,
    )
    if expected.header != transcript.header or expected.chain.header != transcript.chain.header:
        raise ValueError("live compiler schema or source v1 manifest does not match native transcript header")


def verify_native_tiered_admission_transcript(
    transcript: NativeTieredAdmissionTranscript,
    *,
    expected_head_digest: str | None = None,
) -> NativeTieredAdmissionTranscriptVerificationReport:
    """Verify generic chaining, exact v2 byte digests, and compiler/v2 consistency."""

    if transcript.chain.header != transcript.header.transcript_header:
        raise ValueError("native tiered transcript chain header does not match the compiled header")
    base_report: AdmissionTranscriptVerificationReport = verify_admission_transcript(
        transcript.chain,
        expected_head_digest=expected_head_digest,
    )
    if len(transcript.entries) != base_report.entry_count:
        raise ValueError("native tiered evidence count does not match the base chain")
    digests: list[str] = []
    for expected_sequence, (entry, base_entry) in enumerate(
        zip(transcript.entries, transcript.chain.entries),
        start=1,
    ):
        if entry.sequence != expected_sequence:
            raise ValueError("native tiered transcript entry sequences must be contiguous from one")
        if entry.look != base_entry.look:
            raise ValueError("native tiered transcript entry look does not match the base chain")
        if entry.base_entry_digest != base_entry.entry_digest:
            raise ValueError("native tiered transcript entry does not name its exact base entry digest")
        evidence = entry.evidence
        _validate_native_bundle(transcript.header, evidence)
        if evidence.tiered_bundle.source_v1_manifest_digest != base_entry.canonical_manifest_digest:
            raise ValueError("native tiered entry source v1 digest does not match the base transcript entry")
        if base_entry.admission_evidence_reference != evidence.commitment_reference:
            raise ValueError("base transcript entry does not bind the native tiered evidence commitment")
        if base_entry.inclusion_evidence_reference != evidence.compiler_evidence.original_inclusion_evidence_reference:
            raise ValueError("base transcript inclusion evidence does not match native compiler evidence")
        if base_entry.admission_verifier != evidence.compiler_evidence.admission_verifier:
            raise ValueError("base transcript verifier does not match native compiler evidence")
        digests.append(evidence.tiered_bundle.canonical_digest)
    return NativeTieredAdmissionTranscriptVerificationReport(
        transcript_id=base_report.transcript_id,
        entry_count=base_report.entry_count,
        recorded_looks=base_report.recorded_looks,
        genesis_digest=base_report.genesis_digest,
        head_digest=base_report.head_digest,
        native_tiered_manifest_digests=tuple(digests),
    )


def append_native_tiered_admitted_look(
    transcript: NativeTieredAdmissionTranscript,
    *,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    admitted_look: VerifiedExactCompiledPolyhedralExtensionLook,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> NativeTieredAdmissionTranscript:
    """Append one #24-admitted look with a direct strict-canonical v2 manifest binding."""

    report = verify_native_tiered_admission_transcript(transcript)
    _validate_live_header(
        transcript,
        verified_schema=verified_schema,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
    )
    if admitted_look.look != admitted_look.snapshot.look:
        raise ValueError("admitted native tiered look ID and snapshot look ID must match")
    if admitted_look.verified_inclusion_look.look != admitted_look.look:
        raise ValueError("admitted native tiered look ID and inclusion look ID must match")
    if admitted_look.snapshot.target != verified_schema.target:
        raise ValueError("admitted native tiered snapshot target does not match the fixed schema")
    if not source_v1_manifest.target.covers_look(admitted_look.look):
        raise ValueError("admitted native tiered look lies outside the source v1 manifest scope")
    if not coverage_certificate.covers_look(admitted_look.look):
        raise ValueError("admitted native tiered look lies outside the coverage certificate scope")
    if transcript.entries and admitted_look.look <= transcript.entries[-1].look:
        raise ValueError("a new native tiered look must be strictly later than the transcript head")

    audit = audit_exact_compiled_polyhedral_extension_looks(
        verified_schema,
        (admitted_look,),
        coverage_certificate=coverage_certificate,
    )
    static_report = audit.reports_by_look[admitted_look.look]
    evidence = build_native_tiered_manifest_for_admitted_look(
        verified_schema=verified_schema,
        admitted_look=admitted_look,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
    )
    _validate_native_bundle(transcript.header, evidence)
    base_entry = AdmissionTranscriptEntry(
        sequence=report.entry_count + 1,
        look=admitted_look.look,
        previous_entry_digest=report.head_digest,
        canonical_manifest_digest=canonical_manifest_digest(source_v1_manifest),
        schema_context_digest=transcript.header.transcript_header.schema_context_digest,
        admission_evidence_reference=evidence.commitment_reference,
        inclusion_evidence_reference=evidence.compiler_evidence.original_inclusion_evidence_reference,
        admission_verifier=evidence.compiler_evidence.admission_verifier,
        outer_statuses={
            motif: static_report.motifs[motif].outer_status.value
            for motif in transcript.header.transcript_header.motifs
        },
        extension_statuses={
            motif: static_report.motifs[motif].extension_status.value
            for motif in transcript.header.transcript_header.motifs
        },
    )
    native_entry = NativeTieredAdmissionTranscriptEntry(
        sequence=base_entry.sequence,
        evidence=evidence,
        base_entry_digest=base_entry.entry_digest,
    )
    return NativeTieredAdmissionTranscript(
        header=transcript.header,
        chain=AdmissionTranscript(
            header=transcript.chain.header,
            entries=(*transcript.chain.entries, base_entry),
        ),
        entries=(*transcript.entries, native_entry),
    )


def create_native_tiered_transcript_head_checkpoint(
    transcript: NativeTieredAdmissionTranscript,
    *,
    checkpoint_sequence: int,
) -> TranscriptHeadCheckpoint:
    """Create a standard checkpoint after verifying every direct v2 entry commitment."""

    verify_native_tiered_admission_transcript(transcript)
    return create_transcript_head_checkpoint(
        transcript.chain,
        checkpoint_sequence=checkpoint_sequence,
    )


def verify_signed_native_tiered_transcript_checkpoint(
    transcript: NativeTieredAdmissionTranscript,
    signed_checkpoint: SignedTranscriptCheckpoint,
    *,
    trusted_key: Ed25519VerifierKey,
) -> SignedCheckpointVerificationReport:
    """Verify native v2 evidence first, then reuse the established Ed25519 verifier."""

    verify_native_tiered_admission_transcript(transcript)
    return verify_signed_transcript_checkpoint(
        transcript.chain,
        signed_checkpoint,
        trusted_key=trusted_key,
    )
