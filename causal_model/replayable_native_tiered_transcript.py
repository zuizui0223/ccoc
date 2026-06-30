"""Native-v2 transcript histories with mandatory exact proof replay.

PR #27 binds tier-aware manifests and compiler proof-family hashes into an
append-only history. PR #29 makes exact rational branch proofs replayable. This
module creates a fresh transcript variant where every plan and role artifact is
emitted in strict replayable form, and transcript verification requires a
registry of their bytes.

For every entry, verification performs the following chain for *every* role,
including UNKNOWN roles:

    artifact digest -> strict plan parse -> strict branch-bundle parse
    -> exact witness/Farkas replay -> finite-union aggregation
    -> compiler-template identity -> native v2 manifest/status agreement.

The generic hash chain and signed checkpoint wire format remain unchanged. They
commit to replayable artifact references through the native entry commitment;
the external registry supplies the referenced bytes for actual replay.

This is forward-only. Historical native v2 entries keep their hash-only role
artifacts and are not silently upgraded to mandatory replay histories.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .admission_transcript import AdmissionTranscript, AdmissionTranscriptEntry
from .anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from .canonical_manifest_json import canonical_manifest_digest
from .canonical_tiered_manifest_json import canonical_tiered_manifest_bytes
from .certificate_manifest import ArtifactReference, CertificateManifest, QueryRole, sha256_digest
from .compiled_admission_transcript import (
    CompiledAdmissionEntryEvidence,
    CompiledPlanArtifactBinding,
    CompiledRoleProofArtifactBinding,
)
from .exact_compiled_polyhedral_extension_admission import (
    VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    VerifiedExactCompiledPolyhedralExtensionLook,
    audit_exact_compiled_polyhedral_extension_looks,
)
from .native_tiered_admission_transcript import (
    NATIVE_TIERED_MANIFEST_ARTIFACT_PREFIX,
    NativeTieredAdmissionEntryEvidence,
    NativeTieredAdmissionTranscript,
    NativeTieredAdmissionTranscriptEntry,
    NativeTieredAdmissionTranscriptVerificationReport,
    NativeTieredManifestBundle,
    NativeTieredRoleStatusBinding,
    create_native_tiered_admission_transcript,
    verify_native_tiered_admission_transcript,
)
from .replayable_compiled_plan_artifacts import (
    ReplayableCompiledPlanDocument,
    canonical_replayable_compiled_plan_bytes,
    parse_canonical_replayable_compiled_plan,
    replayable_compiled_plan_artifact,
    same_replayable_linear_system,
)
from .replayable_compiled_role_artifacts import (
    build_replayable_compiled_role_bundle,
    replayable_compiled_role_proof_bundle_artifact,
    replayable_compiled_role_proof_bundle_payload,
)
from .replayable_exact_linear_proofs import replay_exact_linear_bundle
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
    TieredQueryPlanBinding,
    TieredSolverQueryProofBinding,
    build_anytime_tiered_symbolic_manifest,
)


REPLAYABLE_NATIVE_TIERED_TRANSCRIPT_FORMAT = "rach-replayable-native-tiered-transcript/v1"


def _query_tier(value: str) -> QueryTier:
    try:
        return QueryTier(value)
    except ValueError as error:
        raise ValueError("replayable transcript tier must be 'inner' or 'outer'") from error


def _role_status(queries: object, motif: str, role: QueryRole) -> FeasibilityStatus:
    motif_queries = queries.motif_queries[motif]
    if role is QueryRole.NONEMPTY:
        return motif_queries.nonempty.status
    if role is QueryRole.ACTIVE:
        return motif_queries.active.status
    if role is QueryRole.INACTIVE:
        return motif_queries.inactive.status
    raise ValueError("unsupported replayable transcript query role")


@dataclass(frozen=True)
class ReplayableArtifactRegistry:
    """External byte registry for manifest-referenced replayable artifacts.

    Registry bytes are not trusted merely because they are present. ``resolve``
    checks the SHA-256 digest in the transcript's artifact reference before any
    strict parser or proof replayer sees them.
    """

    payloads: Mapping[str, bytes]

    def __post_init__(self) -> None:
        for artifact_id, payload in self.payloads.items():
            if not isinstance(artifact_id, str) or not artifact_id:
                raise ValueError("replayable artifact registry IDs must be non-empty strings")
            if not isinstance(payload, bytes):
                raise TypeError("replayable artifact registry payloads must be bytes")

    def resolve(self, artifact: ArtifactReference) -> bytes:
        try:
            payload = self.payloads[artifact.artifact_id]
        except KeyError as error:
            raise ValueError(f"replayable artifact registry is missing {artifact.artifact_id!r}") from error
        if sha256_digest(payload) != artifact.sha256:
            raise ValueError(f"replayable artifact registry digest mismatch for {artifact.artifact_id!r}")
        return payload

    def with_payloads(self, additions: Mapping[str, bytes]) -> "ReplayableArtifactRegistry":
        merged = dict(self.payloads)
        for artifact_id, payload in additions.items():
            previous = merged.get(artifact_id)
            if previous is not None and previous != payload:
                raise ValueError("one replayable registry artifact ID cannot be assigned different bytes")
            merged[artifact_id] = payload
        return ReplayableArtifactRegistry(payloads=merged)


@dataclass(frozen=True)
class ReplayableNativeTieredAdmissionTranscript:
    """Fresh native-v2 history with an external registry required for proof replay."""

    native_transcript: NativeTieredAdmissionTranscript
    registry: ReplayableArtifactRegistry

    @property
    def head_digest(self) -> str:
        return self.native_transcript.head_digest


@dataclass(frozen=True)
class ReplayableNativeTieredTranscriptVerificationReport:
    """Baseline native report plus a count of replayed plan/role proof artifacts."""

    native_report: NativeTieredAdmissionTranscriptVerificationReport
    replayed_plan_artifact_count: int
    replayed_role_artifact_count: int
    replayed_unknown_role_count: int


def _plan_artifacts_by_key(
    evidence: CompiledAdmissionEntryEvidence,
) -> Mapping[tuple[QueryTier, str], ArtifactReference]:
    return {
        (_query_tier(binding.tier), binding.cell_id): binding.artifact
        for binding in evidence.plan_artifacts
    }


def _role_artifacts_by_key(
    evidence: CompiledAdmissionEntryEvidence,
) -> Mapping[tuple[QueryTier, str, str, QueryRole], ArtifactReference]:
    return {
        (_query_tier(binding.tier), binding.cell_id, binding.motif, binding.role): binding.artifact
        for binding in evidence.role_proof_artifacts
    }


def _expected_role_keys(
    transcript: NativeTieredAdmissionTranscript,
) -> set[tuple[QueryTier, str, str, QueryRole]]:
    return {
        (tier, cell_id, motif, role)
        for tier in (QueryTier.INNER, QueryTier.OUTER)
        for cell_id in transcript.header.transcript_header.required_cell_ids
        for motif in transcript.header.transcript_header.motifs
        for role in (QueryRole.NONEMPTY, QueryRole.ACTIVE, QueryRole.INACTIVE)
    }


def _expected_plan_keys(
    transcript: NativeTieredAdmissionTranscript,
) -> set[tuple[QueryTier, str]]:
    return {
        (tier, cell_id)
        for tier in (QueryTier.INNER, QueryTier.OUTER)
        for cell_id in transcript.header.transcript_header.required_cell_ids
    }


def _templates_for_role(
    plan: ReplayableCompiledPlanDocument,
    *,
    motif: str,
    role: QueryRole,
):
    return plan.plan.templates_for(motif=motif, role=role)


def _replay_role_against_plan(
    *,
    role_payload: bytes,
    role_artifact: ArtifactReference,
    plan_document: ReplayableCompiledPlanDocument,
    partition_digest: str,
    motif: str,
    role: QueryRole,
    expected_status: FeasibilityStatus,
) -> None:
    replayed = replay_exact_linear_bundle(
        role_payload,
        expected_digest=role_artifact.sha256,
        expected_plan_digest=plan_document.plan.plan_digest,
        expected_partition_digest=partition_digest,
        expected_motif=motif,
        expected_role=role,
    )
    if replayed.replayed_aggregate_status is not expected_status:
        raise ValueError("replayed role aggregate status differs from native transcript status table")
    expected = {template.query_id: template for template in _templates_for_role(plan_document, motif=motif, role=role)}
    actual = {query.query_id: query for query in replayed.bundle.branches}
    if set(actual) != set(expected):
        raise ValueError("replayed role query IDs do not match the replayable compiler plan")
    for query_id, template in expected.items():
        if not same_replayable_linear_system(actual[query_id].system, template.system):
            raise ValueError("replayed role system differs from replayable compiler plan template")


def _replay_entry(
    transcript: NativeTieredAdmissionTranscript,
    entry: NativeTieredAdmissionTranscriptEntry,
    registry: ReplayableArtifactRegistry,
) -> tuple[int, int, int]:
    evidence = entry.evidence
    compiler = evidence.compiler_evidence
    manifest = evidence.tiered_bundle.manifest
    plan_refs = _plan_artifacts_by_key(compiler)
    role_refs = _role_artifacts_by_key(compiler)
    if set(plan_refs) != _expected_plan_keys(transcript):
        raise ValueError("replayable transcript plan artifact keys do not cover every tier/cell")
    if set(role_refs) != _expected_role_keys(transcript):
        raise ValueError("replayable transcript role artifact keys do not cover every tier/cell/motif/role")

    manifest_plans = {
        (binding.tier, binding.cell_id): binding
        for binding in manifest.tiered_query_plans
    }
    if len(manifest_plans) != len(manifest.tiered_query_plans):
        raise ValueError("native v2 manifest contains duplicate tiered plan bindings")
    if set(manifest_plans) != set(plan_refs):
        raise ValueError("native v2 manifest plan bindings do not match replayable transcript plans")

    plan_documents: dict[tuple[QueryTier, str], ReplayableCompiledPlanDocument] = {}
    for key, artifact in plan_refs.items():
        tier, cell_id = key
        binding = manifest_plans[key]
        if binding.look != entry.look or binding.query_plan_artifact != artifact:
            raise ValueError("native v2 manifest plan binding differs from replayable transcript evidence")
        plan_documents[key] = parse_canonical_replayable_compiled_plan(
            registry.resolve(artifact),
            expected_digest=artifact.sha256,
            expected_partition_digest=evidence.compiler_evidence.partition_artifact.sha256,
        )

    statuses = {binding.key: binding for binding in evidence.tiered_bundle.role_statuses}
    if len(statuses) != len(evidence.tiered_bundle.role_statuses) or set(statuses) != set(role_refs):
        raise ValueError("native v2 role status table does not match replayable role evidence")
    manifest_proofs = {binding.query_key: binding for binding in manifest.solver_query_proofs}
    if len(manifest_proofs) != len(manifest.solver_query_proofs):
        raise ValueError("native v2 manifest contains duplicate decisive proof bindings")

    replayed_unknown = 0
    for key, role_artifact in role_refs.items():
        tier, cell_id, motif, role = key
        status = statuses[key].status
        plan_binding = manifest_plans[(tier, cell_id)]
        _replay_role_against_plan(
            role_payload=registry.resolve(role_artifact),
            role_artifact=role_artifact,
            plan_document=plan_documents[(tier, cell_id)],
            partition_digest=evidence.compiler_evidence.partition_artifact.sha256,
            motif=motif,
            role=role,
            expected_status=status,
        )
        manifest_key = (tier, entry.look, cell_id, motif, role)
        manifest_binding = manifest_proofs.get(manifest_key)
        if status in (FeasibilityStatus.SAT, FeasibilityStatus.UNSAT):
            if manifest_binding is None:
                raise ValueError("decisive replayed role is absent from the native v2 manifest")
            if (
                manifest_binding.status is not status
                or manifest_binding.proof_artifact != role_artifact
                or manifest_binding.query_plan_artifact != plan_binding.query_plan_artifact
                or manifest_binding.verifier_id != compiler.admission_verifier
            ):
                raise ValueError("native v2 decisive proof binding differs from replayed role evidence")
        else:
            replayed_unknown += 1
            if manifest_binding is not None:
                raise ValueError("UNKNOWN replayed role must not appear as a decisive native v2 proof")

    expected_decisive_keys = {
        (tier, entry.look, cell_id, motif, role)
        for (tier, cell_id, motif, role), binding in statuses.items()
        if binding.status in (FeasibilityStatus.SAT, FeasibilityStatus.UNSAT)
    }
    if set(manifest_proofs) != expected_decisive_keys:
        raise ValueError("native v2 manifest decisive proof keys do not equal replayed decisive roles")
    return len(plan_documents), len(role_refs), replayed_unknown


def verify_replayable_native_tiered_admission_transcript(
    transcript: ReplayableNativeTieredAdmissionTranscript,
    *,
    expected_head_digest: str | None = None,
) -> ReplayableNativeTieredTranscriptVerificationReport:
    """Verify native hash history, then mandatory plan/proof replay for every entry."""

    native_report = verify_native_tiered_admission_transcript(
        transcript.native_transcript,
        expected_head_digest=expected_head_digest,
    )
    plans = 0
    roles = 0
    unknown = 0
    for entry in transcript.native_transcript.entries:
        count_plans, count_roles, count_unknown = _replay_entry(
            transcript.native_transcript,
            entry,
            transcript.registry,
        )
        plans += count_plans
        roles += count_roles
        unknown += count_unknown
    return ReplayableNativeTieredTranscriptVerificationReport(
        native_report=native_report,
        replayed_plan_artifact_count=plans,
        replayed_role_artifact_count=roles,
        replayed_unknown_role_count=unknown,
    )


def _build_replayable_native_entry_evidence(
    *,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    admitted_look: VerifiedExactCompiledPolyhedralExtensionLook,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> tuple[NativeTieredAdmissionEntryEvidence, Mapping[str, bytes]]:
    plan_bindings: list[CompiledPlanArtifactBinding] = []
    role_bindings: list[CompiledRoleProofArtifactBinding] = []
    role_statuses: list[NativeTieredRoleStatusBinding] = []
    payloads: dict[str, bytes] = {}

    for tier_name, tier, queries_by_cell in (
        ("inner", QueryTier.INNER, admitted_look.inner_queries_by_cell),
        ("outer", QueryTier.OUTER, admitted_look.outer_queries_by_cell),
    ):
        if tuple(queries_by_cell) != verified_schema.target.required_cell_ids:
            raise ValueError("admitted query cells must match required-cell order")
        for cell_id in verified_schema.target.required_cell_ids:
            queries = queries_by_cell[cell_id]
            plan = queries.bound_proofs.plan
            plan_artifact = replayable_compiled_plan_artifact(
                plan,
                artifact_id=f"replayable-plan:{tier_name}:look-{admitted_look.look}:cell-{cell_id}",
            )
            plan_bindings.append(
                CompiledPlanArtifactBinding(tier=tier_name, cell_id=cell_id, artifact=plan_artifact)
            )
            payloads[plan_artifact.artifact_id] = canonical_replayable_compiled_plan_bytes(plan)
            for motif in verified_schema.target.space.motifs:
                for role in (QueryRole.NONEMPTY, QueryRole.ACTIVE, QueryRole.INACTIVE):
                    role_artifact = replayable_compiled_role_proof_bundle_artifact(
                        queries,
                        motif=motif,
                        role=role,
                        artifact_id=(
                            f"replayable-role:{tier_name}:look-{admitted_look.look}:"
                            f"cell-{cell_id}:motif-{motif}:role-{role.value}"
                        ),
                    )
                    role_bindings.append(
                        CompiledRoleProofArtifactBinding(
                            tier=tier_name,
                            cell_id=cell_id,
                            motif=motif,
                            role=role,
                            artifact=role_artifact,
                        )
                    )
                    payloads[role_artifact.artifact_id] = replayable_compiled_role_proof_bundle_payload(
                        queries,
                        motif=motif,
                        role=role,
                    )
                    role_statuses.append(
                        NativeTieredRoleStatusBinding(
                            tier=tier,
                            cell_id=cell_id,
                            motif=motif,
                            role=role,
                            status=_role_status(queries, motif, role),
                        )
                    )

    compiler_evidence = CompiledAdmissionEntryEvidence(
        look=admitted_look.look,
        partition_artifact=ArtifactReference.from_payload(
            "verified-polyhedral-motif-partition",
            # The compiler's existing partition artifact payload is committed by
            # the native schema header; this reference must match that header.
            # Reconstructing it here avoids accepting a caller-supplied value.
            __import__("causal_model.polyhedral_motif_compiler", fromlist=["polyhedral_motif_partition_payload"])
            .polyhedral_motif_partition_payload(verified_schema.verified_partition),
            media_type="application/json",
        ),
        plan_artifacts=tuple(plan_bindings),
        role_proof_artifacts=tuple(role_bindings),
        original_admission_evidence_reference=admitted_look.evidence_reference,
        original_inclusion_evidence_reference=admitted_look.verified_inclusion_look.evidence_reference,
        admission_verifier=admitted_look.verifier,
    )
    plan_by_key = {
        (_query_tier(binding.tier), binding.cell_id): binding.artifact
        for binding in plan_bindings
    }
    role_by_key = {
        (_query_tier(binding.tier), binding.cell_id, binding.motif, binding.role): binding.artifact
        for binding in role_bindings
    }
    tiered_manifest = build_anytime_tiered_symbolic_manifest(
        target=source_v1_manifest.target,
        coverage_certificate=coverage_certificate,
        solver_certificate=verified_schema.all_look_solver_certificate,
        coverage_assertion=source_v1_manifest.coverage_assertion,
        solver_assertion=source_v1_manifest.solver_assertion,
        semantic_partition_artifact=compiler_evidence.partition_artifact,
        tiered_query_plans=tuple(
            TieredQueryPlanBinding(
                tier=tier,
                look=admitted_look.look,
                cell_id=cell_id,
                query_plan_artifact=artifact,
            )
            for (tier, cell_id), artifact in plan_by_key.items()
        ),
        solver_query_proofs=tuple(
            TieredSolverQueryProofBinding(
                tier=status.tier,
                look=admitted_look.look,
                cell_id=status.cell_id,
                motif=status.motif,
                role=status.role,
                status=status.status,
                query_plan_artifact=plan_by_key[(status.tier, status.cell_id)],
                proof_artifact=role_by_key[status.key],
                verifier_id=compiler_evidence.admission_verifier,
            )
            for status in role_statuses
            if status.status in (FeasibilityStatus.SAT, FeasibilityStatus.UNSAT)
        ),
    )
    manifest_artifact = ArtifactReference.from_payload(
        f"{NATIVE_TIERED_MANIFEST_ARTIFACT_PREFIX}:look-{admitted_look.look}",
        canonical_tiered_manifest_bytes(tiered_manifest),
        media_type="application/json",
    )
    evidence = NativeTieredAdmissionEntryEvidence(
        compiler_evidence=compiler_evidence,
        tiered_bundle=NativeTieredManifestBundle(
            source_v1_manifest_digest=canonical_manifest_digest(source_v1_manifest),
            manifest=tiered_manifest,
            manifest_artifact=manifest_artifact,
            role_statuses=tuple(role_statuses),
        ),
    )
    return evidence, payloads


def create_replayable_native_tiered_admission_transcript(
    *,
    transcript_id: str,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    base_admission_schema_artifact: ArtifactReference,
) -> ReplayableNativeTieredAdmissionTranscript:
    """Create a fresh empty native-v2 history requiring replayable future artifacts."""

    native = create_native_tiered_admission_transcript(
        transcript_id=transcript_id,
        verified_schema=verified_schema,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
        base_admission_schema_artifact=base_admission_schema_artifact,
    )
    return ReplayableNativeTieredAdmissionTranscript(
        native_transcript=native,
        registry=ReplayableArtifactRegistry(payloads={}),
    )


def _validate_live_header(
    transcript: ReplayableNativeTieredAdmissionTranscript,
    *,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> None:
    expected = create_native_tiered_admission_transcript(
        transcript_id=transcript.native_transcript.header.transcript_header.transcript_id,
        verified_schema=verified_schema,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
        base_admission_schema_artifact=transcript.native_transcript.header.schema_artifacts.base_admission_schema_artifact,
    )
    if expected.header != transcript.native_transcript.header or expected.chain.header != transcript.native_transcript.chain.header:
        raise ValueError("live compiler schema or source v1 manifest does not match replayable transcript header")


def append_replayable_native_tiered_admitted_look(
    transcript: ReplayableNativeTieredAdmissionTranscript,
    *,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    admitted_look: VerifiedExactCompiledPolyhedralExtensionLook,
    source_v1_manifest: CertificateManifest,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> ReplayableNativeTieredAdmissionTranscript:
    """Append one admitted look while generating all replayable plan/proof artifacts."""

    report = verify_replayable_native_tiered_admission_transcript(transcript)
    _validate_live_header(
        transcript,
        verified_schema=verified_schema,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
    )
    if admitted_look.look != admitted_look.snapshot.look:
        raise ValueError("admitted replayable look ID and snapshot look ID must match")
    if admitted_look.verified_inclusion_look.look != admitted_look.look:
        raise ValueError("admitted replayable look ID and inclusion look ID must match")
    if admitted_look.snapshot.target != verified_schema.target:
        raise ValueError("admitted replayable snapshot target does not match fixed schema")
    if not source_v1_manifest.target.covers_look(admitted_look.look):
        raise ValueError("admitted replayable look lies outside source manifest scope")
    if not coverage_certificate.covers_look(admitted_look.look):
        raise ValueError("admitted replayable look lies outside coverage scope")
    if transcript.native_transcript.entries and admitted_look.look <= transcript.native_transcript.entries[-1].look:
        raise ValueError("new replayable look must be strictly later than transcript head")

    audit = audit_exact_compiled_polyhedral_extension_looks(
        verified_schema,
        (admitted_look,),
        coverage_certificate=coverage_certificate,
    )
    static_report = audit.reports_by_look[admitted_look.look]
    evidence, new_payloads = _build_replayable_native_entry_evidence(
        verified_schema=verified_schema,
        admitted_look=admitted_look,
        source_v1_manifest=source_v1_manifest,
        coverage_certificate=coverage_certificate,
    )
    merged_registry = transcript.registry.with_payloads(new_payloads)
    base_entry = AdmissionTranscriptEntry(
        sequence=report.native_report.entry_count + 1,
        look=admitted_look.look,
        previous_entry_digest=report.native_report.head_digest,
        canonical_manifest_digest=canonical_manifest_digest(source_v1_manifest),
        schema_context_digest=transcript.native_transcript.header.transcript_header.schema_context_digest,
        admission_evidence_reference=evidence.commitment_reference,
        inclusion_evidence_reference=evidence.compiler_evidence.original_inclusion_evidence_reference,
        admission_verifier=evidence.compiler_evidence.admission_verifier,
        outer_statuses={
            motif: static_report.motifs[motif].outer_status.value
            for motif in transcript.native_transcript.header.transcript_header.motifs
        },
        extension_statuses={
            motif: static_report.motifs[motif].extension_status.value
            for motif in transcript.native_transcript.header.transcript_header.motifs
        },
    )
    native_entry = NativeTieredAdmissionTranscriptEntry(
        sequence=base_entry.sequence,
        evidence=evidence,
        base_entry_digest=base_entry.entry_digest,
    )
    native = NativeTieredAdmissionTranscript(
        header=transcript.native_transcript.header,
        chain=AdmissionTranscript(
            header=transcript.native_transcript.chain.header,
            entries=(*transcript.native_transcript.chain.entries, base_entry),
        ),
        entries=(*transcript.native_transcript.entries, native_entry),
    )
    return ReplayableNativeTieredAdmissionTranscript(native_transcript=native, registry=merged_registry)


def create_replayable_native_tiered_transcript_head_checkpoint(
    transcript: ReplayableNativeTieredAdmissionTranscript,
    *,
    checkpoint_sequence: int,
) -> TranscriptHeadCheckpoint:
    """Create a standard checkpoint only after replaying every stored proof artifact."""

    verify_replayable_native_tiered_admission_transcript(transcript)
    return create_transcript_head_checkpoint(
        transcript.native_transcript.chain,
        checkpoint_sequence=checkpoint_sequence,
    )


def verify_signed_replayable_native_tiered_transcript_checkpoint(
    transcript: ReplayableNativeTieredAdmissionTranscript,
    signed_checkpoint: SignedTranscriptCheckpoint,
    *,
    trusted_key: Ed25519VerifierKey,
) -> SignedCheckpointVerificationReport:
    """Replay all plan/proof artifacts before verifying the standard signed head."""

    verify_replayable_native_tiered_admission_transcript(transcript)
    return verify_signed_transcript_checkpoint(
        transcript.native_transcript.chain,
        signed_checkpoint,
        trusted_key=trusted_key,
    )
