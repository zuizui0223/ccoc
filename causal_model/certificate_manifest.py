"""Hash-bound certificate manifests for auditable RACH theorem targets.

The lifting theorems distinguish several external obligations: a candidate-space
encoding, motif predicates, a time-uniform retained-set coverage statement,
solver-semantic validity, and individual query/proof artifacts.  A bare file
path or prose label is not enough to prove that those obligations concern the
same target.

This module defines a small deterministic manifest contract.  It does *not*
validate a statistical theorem or parse a solver proof.  Instead it binds each
external artifact to a canonical target through SHA-256 digests and rejects
mismatched candidate spaces, motif vocabularies, required cells, look scopes,
query roles, or artifact contents.

Cryptographic hashes provide integrity binding under the usual collision-
resistance assumption.  They do not provide authorship, signatures, trusted
provenance, or semantic correctness of the hashed artifacts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields, is_dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

from .anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
)
from .symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace


MANIFEST_FORMAT = "rach-certificate-manifest/v1"
_HEX_DIGEST_LENGTH = 64


class QueryRole(str, Enum):
    """The three solver queries used for one symbolic RACH motif decision."""

    NONEMPTY = "nonempty"
    ACTIVE = "active"
    INACTIVE = "inactive"


def _require_digest(value: str, name: str) -> None:
    if len(value) != _HEX_DIGEST_LENGTH or any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{name} must be a lowercase SHA-256 hexadecimal digest")


def _require_nonempty(value: str, name: str) -> None:
    if not value:
        raise ValueError(f"{name} must be non-empty")


def _validate_unit_interval(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")


def sha256_digest(payload: str | bytes) -> str:
    """Hash exact UTF-8 text or bytes for a manifest artifact reference."""

    raw = payload.encode("utf-8") if isinstance(payload, str) else payload
    if not isinstance(raw, bytes):
        raise TypeError("payload must be str or bytes")
    return sha256(raw).hexdigest()


def _canonicalize(value: Any) -> Any:
    """Convert supported manifest values into deterministic JSON-safe objects."""

    if isinstance(value, Enum):
        return value.value
    if isinstance(value, float):
        # Hex preserves the exact binary value used by the source certificate.
        return {"__float_hex__": value.hex()}
    if is_dataclass(value):
        return {
            field.name: _canonicalize(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, Mapping):
        return {
            str(key): _canonicalize(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [_canonicalize(item) for item in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    raise TypeError(f"unsupported manifest value: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    """Return deterministic JSON used for manifest and target fingerprints."""

    return json.dumps(
        _canonicalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


@dataclass(frozen=True)
class ArtifactReference:
    """A content-addressed external artifact reference.

    `artifact_id` is a human-readable locator within one manifest. The SHA-256
    digest is the actual integrity commitment. The manifest can reuse one
    artifact across multiple bindings when the identifier and digest agree.
    """

    artifact_id: str
    sha256: str
    media_type: str = "application/octet-stream"

    @classmethod
    def from_payload(
        cls,
        artifact_id: str,
        payload: str | bytes,
        *,
        media_type: str = "application/octet-stream",
    ) -> "ArtifactReference":
        return cls(artifact_id=artifact_id, sha256=sha256_digest(payload), media_type=media_type)

    def __post_init__(self) -> None:
        _require_nonempty(self.artifact_id, "artifact_id")
        _require_digest(self.sha256, "artifact SHA-256")
        _require_nonempty(self.media_type, "media_type")


@dataclass(frozen=True)
class ManifestTarget:
    """The fixed scientific/formal target to which external artifacts are bound.

    `candidate_space_artifact` must hash a formal candidate-space encoding, not
    merely an informal title. `motif_definition_artifacts` must contain exactly
    one content-addressed definition for every declared motif.
    """

    candidate_space_description: str
    candidate_space_artifact: ArtifactReference
    motif_definition_artifacts: Mapping[str, ArtifactReference]
    required_cell_ids: tuple[str, ...]
    certified_looks: tuple[int, ...] | None

    @classmethod
    def from_payloads(
        cls,
        space: SymbolicCandidateSpace,
        *,
        candidate_space_payload: str | bytes,
        motif_definition_payloads: Mapping[str, str | bytes],
        required_cell_ids: Iterable[str],
        certified_looks: tuple[int, ...] | None,
        candidate_space_artifact_id: str = "candidate-space",
    ) -> "ManifestTarget":
        motif_keys = set(motif_definition_payloads)
        if motif_keys != set(space.motifs):
            raise ValueError("motif_definition_payloads must contain exactly the declared motifs")
        return cls(
            candidate_space_description=space.space_description,
            candidate_space_artifact=ArtifactReference.from_payload(
                candidate_space_artifact_id,
                candidate_space_payload,
                media_type="application/json",
            ),
            motif_definition_artifacts={
                motif: ArtifactReference.from_payload(
                    f"motif:{motif}",
                    motif_definition_payloads[motif],
                    media_type="application/json",
                )
                for motif in space.motifs
            },
            required_cell_ids=tuple(required_cell_ids),
            certified_looks=certified_looks,
        )

    def __post_init__(self) -> None:
        _require_nonempty(self.candidate_space_description, "candidate_space_description")
        if not self.motif_definition_artifacts:
            raise ValueError("at least one motif definition artifact is required")
        if any(not motif for motif in self.motif_definition_artifacts):
            raise ValueError("motif names must be non-empty")
        if len(set(self.motif_definition_artifacts)) != len(self.motif_definition_artifacts):
            raise ValueError("motif names must be unique")
        if not self.required_cell_ids:
            raise ValueError("required_cell_ids must not be empty")
        if len(set(self.required_cell_ids)) != len(self.required_cell_ids) or any(not cell for cell in self.required_cell_ids):
            raise ValueError("required_cell_ids must be unique non-empty names")
        if self.certified_looks is not None:
            if not self.certified_looks:
                raise ValueError("certified_looks must be non-empty when provided")
            if any(not isinstance(look, int) or look < 1 for look in self.certified_looks):
                raise ValueError("certified_looks must contain positive integers")
            if len(set(self.certified_looks)) != len(self.certified_looks):
                raise ValueError("certified_looks must be unique")

    @property
    def motifs(self) -> tuple[str, ...]:
        return tuple(self.motif_definition_artifacts)

    @property
    def target_digest(self) -> str:
        return sha256_digest(canonical_json(self))

    def covers_look(self, look: int) -> bool:
        return self.certified_looks is None or look in self.certified_looks


@dataclass(frozen=True)
class ExternalAssertionBinding:
    """A coverage or solver-validity assertion tied to an evidence artifact."""

    kind: str
    lower_bound: float
    method: str
    assumptions: tuple[str, ...]
    evidence_artifact: ArtifactReference

    @classmethod
    def from_payload(
        cls,
        *,
        kind: str,
        lower_bound: float,
        method: str,
        assumptions: tuple[str, ...],
        evidence_artifact_id: str,
        evidence_payload: str | bytes,
    ) -> "ExternalAssertionBinding":
        return cls(
            kind=kind,
            lower_bound=lower_bound,
            method=method,
            assumptions=assumptions,
            evidence_artifact=ArtifactReference.from_payload(
                evidence_artifact_id,
                evidence_payload,
                media_type="application/json",
            ),
        )

    def __post_init__(self) -> None:
        _require_nonempty(self.kind, "assertion kind")
        _validate_unit_interval(self.lower_bound, "assertion lower_bound")
        _require_nonempty(self.method, "assertion method")


@dataclass(frozen=True)
class SolverQueryProofBinding:
    """Bind one decisive solver result to its exact target and query encoding."""

    look: int
    cell_id: str
    motif: str
    role: QueryRole
    status: FeasibilityStatus
    query_encoding_artifact: ArtifactReference
    proof_artifact: ArtifactReference
    verifier_id: str

    @classmethod
    def from_payloads(
        cls,
        *,
        look: int,
        cell_id: str,
        motif: str,
        role: QueryRole,
        status: FeasibilityStatus,
        query_encoding_payload: str | bytes,
        proof_payload: str | bytes,
        verifier_id: str,
        query_artifact_id: str | None = None,
        proof_artifact_id: str | None = None,
    ) -> "SolverQueryProofBinding":
        stem = f"look:{look}/cell:{cell_id}/motif:{motif}/role:{role.value}"
        return cls(
            look=look,
            cell_id=cell_id,
            motif=motif,
            role=role,
            status=status,
            query_encoding_artifact=ArtifactReference.from_payload(
                query_artifact_id or f"query:{stem}",
                query_encoding_payload,
                media_type="application/json",
            ),
            proof_artifact=ArtifactReference.from_payload(
                proof_artifact_id or f"proof:{stem}",
                proof_payload,
                media_type="application/json",
            ),
            verifier_id=verifier_id,
        )

    def __post_init__(self) -> None:
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("proof binding look must be a positive integer")
        _require_nonempty(self.cell_id, "proof binding cell_id")
        _require_nonempty(self.motif, "proof binding motif")
        if not isinstance(self.role, QueryRole):
            raise ValueError("proof binding role must be a QueryRole")
        if self.status not in (FeasibilityStatus.SAT, FeasibilityStatus.UNSAT):
            raise ValueError("proof bindings may contain only decisive SAT or UNSAT statuses")
        _require_nonempty(self.verifier_id, "proof binding verifier_id")

    @property
    def query_key(self) -> tuple[int, str, str, QueryRole]:
        return (self.look, self.cell_id, self.motif, self.role)


@dataclass(frozen=True)
class CertificateManifest:
    """A deterministic contract joining theorem target, assertions, and proofs."""

    target: ManifestTarget
    coverage_assertion: ExternalAssertionBinding
    solver_assertion: ExternalAssertionBinding
    solver_query_proofs: tuple[SolverQueryProofBinding, ...] = ()
    format_version: str = MANIFEST_FORMAT

    def __post_init__(self) -> None:
        if self.format_version != MANIFEST_FORMAT:
            raise ValueError(f"unsupported manifest format: {self.format_version!r}")
        if self.coverage_assertion.kind != "time-uniform-statistical-coverage":
            raise ValueError("coverage_assertion kind must be time-uniform-statistical-coverage")
        if self.solver_assertion.kind != "time-uniform-solver-semantic-validity":
            raise ValueError("solver_assertion kind must be time-uniform-solver-semantic-validity")
        keys = [binding.query_key for binding in self.solver_query_proofs]
        if len(set(keys)) != len(keys):
            raise ValueError("solver query proof bindings must be unique per look/cell/motif/role")
        for binding in self.solver_query_proofs:
            if not self.target.covers_look(binding.look):
                raise ValueError("proof binding look lies outside the manifest target scope")
            if binding.cell_id not in self.target.required_cell_ids:
                raise ValueError("proof binding cell_id is absent from the manifest target")
            if binding.motif not in self.target.motifs:
                raise ValueError("proof binding motif is absent from the manifest target")

    @property
    def manifest_digest(self) -> str:
        return sha256_digest(canonical_json(self))

    def referenced_artifacts(self) -> Mapping[str, ArtifactReference]:
        """Return the unique artifact registry, rejecting conflicting identifier reuse."""

        artifacts: dict[str, ArtifactReference] = {}
        for artifact in (
            self.target.candidate_space_artifact,
            *self.target.motif_definition_artifacts.values(),
            self.coverage_assertion.evidence_artifact,
            self.solver_assertion.evidence_artifact,
            *(binding.query_encoding_artifact for binding in self.solver_query_proofs),
            *(binding.proof_artifact for binding in self.solver_query_proofs),
        ):
            previous = artifacts.get(artifact.artifact_id)
            if previous is not None and previous != artifact:
                raise ValueError("one artifact_id cannot name different digest or media-type commitments")
            artifacts[artifact.artifact_id] = artifact
        return artifacts


@dataclass(frozen=True)
class ManifestVerificationReport:
    """Successful manifest context and artifact-content verification result."""

    manifest_digest: str
    target_digest: str
    verified_artifact_ids: tuple[str, ...]


def _common_scope(
    coverage: AnytimeSymbolicJointCoverageCertificate,
    solver: AnytimeSolverSemanticValidityCertificate,
) -> tuple[int, ...] | None:
    coverage_scope = coverage.certified_looks
    solver_scope = solver.certified_looks
    if coverage_scope is None and solver_scope is None:
        return None
    if coverage_scope is None:
        return tuple(sorted(solver_scope or ()))
    if solver_scope is None:
        return tuple(sorted(coverage_scope))
    if set(coverage_scope) != set(solver_scope):
        raise ValueError("coverage and solver certificates must cover the same finite look scope")
    return tuple(sorted(coverage_scope))


def build_anytime_symbolic_manifest(
    *,
    target: ManifestTarget,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
    coverage_assertion: ExternalAssertionBinding,
    solver_assertion: ExternalAssertionBinding,
    solver_query_proofs: Iterable[SolverQueryProofBinding] = (),
) -> CertificateManifest:
    """Build a manifest only when its target exactly matches the theorem inputs."""

    scope = _common_scope(coverage_certificate, solver_certificate)
    if target.required_cell_ids != coverage_certificate.required_cell_ids:
        raise ValueError("manifest target and coverage certificate required cell IDs must match exactly")
    if set(target.required_cell_ids) != set(solver_certificate.required_cell_ids):
        raise ValueError("manifest target and solver certificate required cell IDs must match")
    if target.certified_looks != scope:
        raise ValueError("manifest target look scope must equal the common certificate scope")
    if set(target.motifs) != set(solver_certificate.motifs):
        raise ValueError("manifest target motifs must match the solver certificate")
    if coverage_assertion.lower_bound != coverage_certificate.lower_bound:
        raise ValueError("coverage assertion lower bound must match the coverage certificate")
    if coverage_assertion.method != coverage_certificate.method:
        raise ValueError("coverage assertion method must match the coverage certificate")
    if coverage_assertion.assumptions != coverage_certificate.assumptions:
        raise ValueError("coverage assertion assumptions must match the coverage certificate")
    if solver_assertion.lower_bound != solver_certificate.lower_bound:
        raise ValueError("solver assertion lower bound must match the solver certificate")
    if solver_assertion.method != solver_certificate.method:
        raise ValueError("solver assertion method must match the solver certificate")
    if solver_assertion.assumptions != solver_certificate.assumptions:
        raise ValueError("solver assertion assumptions must match the solver certificate")
    return CertificateManifest(
        target=target,
        coverage_assertion=coverage_assertion,
        solver_assertion=solver_assertion,
        solver_query_proofs=tuple(solver_query_proofs),
    )


def verify_manifest_context(
    manifest: CertificateManifest,
    *,
    space: SymbolicCandidateSpace,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
) -> None:
    """Reject a manifest whose fixed target differs from live theorem inputs."""

    expected_scope = _common_scope(coverage_certificate, solver_certificate)
    if manifest.target.candidate_space_description != space.space_description:
        raise ValueError("manifest candidate-space description does not match the declared space")
    if set(manifest.target.motifs) != set(space.motifs):
        raise ValueError("manifest motif vocabulary does not match the declared space")
    if manifest.target.required_cell_ids != coverage_certificate.required_cell_ids:
        raise ValueError("manifest required cells do not match the coverage certificate")
    if set(manifest.target.required_cell_ids) != set(solver_certificate.required_cell_ids):
        raise ValueError("manifest required cells do not match the solver certificate")
    if manifest.target.certified_looks != expected_scope:
        raise ValueError("manifest look scope does not match the common certificate scope")
    if manifest.coverage_assertion.lower_bound != coverage_certificate.lower_bound:
        raise ValueError("manifest coverage bound does not match the coverage certificate")
    if manifest.coverage_assertion.method != coverage_certificate.method:
        raise ValueError("manifest coverage method does not match the coverage certificate")
    if manifest.coverage_assertion.assumptions != coverage_certificate.assumptions:
        raise ValueError("manifest coverage assumptions do not match the coverage certificate")
    if manifest.solver_assertion.lower_bound != solver_certificate.lower_bound:
        raise ValueError("manifest solver bound does not match the solver certificate")
    if manifest.solver_assertion.method != solver_certificate.method:
        raise ValueError("manifest solver method does not match the solver certificate")
    if manifest.solver_assertion.assumptions != solver_certificate.assumptions:
        raise ValueError("manifest solver assumptions do not match the solver certificate")


def verify_manifest_artifacts(
    manifest: CertificateManifest,
    payloads: Mapping[str, str | bytes],
) -> ManifestVerificationReport:
    """Verify supplied artifact contents against every manifest digest commitment."""

    artifacts = manifest.referenced_artifacts()
    missing = set(artifacts) - set(payloads)
    if missing:
        raise ValueError(f"missing payloads for manifest artifacts: {sorted(missing)}")
    unexpected = set(payloads) - set(artifacts)
    if unexpected:
        raise ValueError(f"payloads include artifact IDs absent from the manifest: {sorted(unexpected)}")
    for artifact_id, artifact in artifacts.items():
        observed = sha256_digest(payloads[artifact_id])
        if observed != artifact.sha256:
            raise ValueError(f"artifact digest mismatch for {artifact_id!r}")
    return ManifestVerificationReport(
        manifest_digest=manifest.manifest_digest,
        target_digest=manifest.target.target_digest,
        verified_artifact_ids=tuple(sorted(artifacts)),
    )


def verify_anytime_symbolic_manifest(
    manifest: CertificateManifest,
    *,
    space: SymbolicCandidateSpace,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
    payloads: Mapping[str, str | bytes],
) -> ManifestVerificationReport:
    """Verify both theorem-target context and exact artifact-content bindings."""

    verify_manifest_context(
        manifest,
        space=space,
        coverage_certificate=coverage_certificate,
        solver_certificate=solver_certificate,
    )
    return verify_manifest_artifacts(manifest, payloads)
