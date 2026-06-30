"""Proof-carrying interface for external all-look retained-set coverage.

RACH's lifting theorem is deliberately distribution agnostic: it consumes an
external certificate asserting simultaneous retention of the true candidate at
every required cell and every certified look.  A scalar lower bound alone is not
an auditable scientific object.  This module turns that assertion into a
content-addressed contract that binds:

* the declared candidate-universe target;
* the observation-channel and retained-set encoder definitions;
* the all-look coverage theorem/proof artifact; and
* the exact confidence, cell, look, method, and assumption declarations.

No universal verifier for arbitrary statistical proofs exists here.  Instead, a
method-specific ``CoverageProofVerifier`` receives exact contract and artifact
bytes and returns a checked receipt.  The chosen verifier is explicitly part of
the trusted computing base.  RACH verifies the surrounding identity/scope
bindings and never treats an opaque artifact hash as a statistical proof by
itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol, runtime_checkable

from .anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from .certificate_manifest import ArtifactReference, ManifestTarget, canonical_json, sha256_digest


ALL_LOOK_COVERAGE_CONTRACT_FORMAT = "rach-all-look-coverage-contract/v1"
ALL_LOOK_COVERAGE_CONTRACT_ARTIFACT_PREFIX = "all-look-coverage-contract"


def _require_nonempty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")


def _require_digest(value: str, name: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256 hexadecimal digest")


def _artifact_object(artifact: ArtifactReference) -> dict[str, str]:
    return {
        "artifact_id": artifact.artifact_id,
        "media_type": artifact.media_type,
        "sha256": artifact.sha256,
    }


@dataclass(frozen=True)
class AllLookCoverageContract:
    """One external all-look retained-set coverage claim with replayable inputs.

    The asserted event is fixed by this format:

    ``P(for all certified looks t, theta_star belongs to every required C[r,t])
    >= lower_bound``.

    ``retained_set_encoder_artifact`` identifies the data-prefix-to-retained-set
    construction; ``coverage_proof_artifact`` identifies the method-specific
    theorem, derivation, certificate, or proof program that establishes the
    event.  The actual proof semantics are checked only by a named external
    verifier supplied to ``verify_all_look_coverage_contract``.
    """

    contract_id: str
    target_digest: str
    candidate_space_artifact: ArtifactReference
    observation_channel_artifact: ArtifactReference
    retained_set_encoder_artifact: ArtifactReference
    coverage_proof_artifact: ArtifactReference
    true_candidate_label: str
    required_cell_ids: tuple[str, ...]
    certified_looks: tuple[int, ...] | None
    lower_bound: float
    method: str
    assumptions: tuple[str, ...]
    coverage_verifier_id: str
    format_version: str = ALL_LOOK_COVERAGE_CONTRACT_FORMAT

    def __post_init__(self) -> None:
        if self.format_version != ALL_LOOK_COVERAGE_CONTRACT_FORMAT:
            raise ValueError(f"unsupported all-look coverage contract format: {self.format_version!r}")
        _require_nonempty(self.contract_id, "contract_id")
        _require_digest(self.target_digest, "target_digest")
        _require_nonempty(self.true_candidate_label, "true_candidate_label")
        if not self.required_cell_ids or len(set(self.required_cell_ids)) != len(self.required_cell_ids):
            raise ValueError("required_cell_ids must be non-empty and unique")
        if any(not cell_id for cell_id in self.required_cell_ids):
            raise ValueError("required_cell_ids must be non-empty strings")
        if not 0.0 <= self.lower_bound <= 1.0:
            raise ValueError("lower_bound must lie in [0, 1]")
        _require_nonempty(self.method, "method")
        _require_nonempty(self.coverage_verifier_id, "coverage_verifier_id")
        if self.certified_looks is not None:
            if not self.certified_looks:
                raise ValueError("certified_looks must be non-empty when finite")
            if any(not isinstance(look, int) or look < 1 for look in self.certified_looks):
                raise ValueError("certified_looks must contain positive integers")
            if len(set(self.certified_looks)) != len(self.certified_looks):
                raise ValueError("certified_looks must be unique")

    @property
    def miscoverage_upper_bound(self) -> float:
        return 1.0 - self.lower_bound

    def covers_look(self, look: int) -> bool:
        return self.certified_looks is None or look in self.certified_looks

    @property
    def contract_payload(self) -> bytes:
        return canonical_json(
            {
                "format_version": self.format_version,
                "contract_id": self.contract_id,
                "target_digest": self.target_digest,
                "candidate_space_artifact": _artifact_object(self.candidate_space_artifact),
                "observation_channel_artifact": _artifact_object(self.observation_channel_artifact),
                "retained_set_encoder_artifact": _artifact_object(self.retained_set_encoder_artifact),
                "coverage_proof_artifact": _artifact_object(self.coverage_proof_artifact),
                "true_candidate_label": self.true_candidate_label,
                "required_cell_ids": list(self.required_cell_ids),
                "certified_looks": (
                    None if self.certified_looks is None else list(self.certified_looks)
                ),
                "lower_bound": self.lower_bound,
                "method": self.method,
                "assumptions": list(self.assumptions),
                "coverage_verifier_id": self.coverage_verifier_id,
            }
        ).encode("utf-8")

    @property
    def contract_digest(self) -> str:
        return sha256_digest(self.contract_payload)

    def referenced_artifacts(self) -> Mapping[str, ArtifactReference]:
        """Return all contract artifacts, rejecting ambiguous repeated IDs."""

        artifacts: dict[str, ArtifactReference] = {}
        for artifact in (
            self.candidate_space_artifact,
            self.observation_channel_artifact,
            self.retained_set_encoder_artifact,
            self.coverage_proof_artifact,
        ):
            previous = artifacts.get(artifact.artifact_id)
            if previous is not None and previous != artifact:
                raise ValueError("one coverage-contract artifact ID cannot name different commitments")
            artifacts[artifact.artifact_id] = artifact
        return artifacts


@dataclass(frozen=True)
class CoverageProofVerificationReceipt:
    """Successful output from a method-specific all-look coverage proof verifier."""

    contract_digest: str
    verifier_id: str
    coverage_proof_artifact_sha256: str
    retained_set_encoder_artifact_sha256: str
    observation_channel_artifact_sha256: str
    result: str = "valid"

    def __post_init__(self) -> None:
        _require_digest(self.contract_digest, "contract_digest")
        _require_nonempty(self.verifier_id, "verifier_id")
        _require_digest(self.coverage_proof_artifact_sha256, "coverage_proof_artifact_sha256")
        _require_digest(self.retained_set_encoder_artifact_sha256, "retained_set_encoder_artifact_sha256")
        _require_digest(self.observation_channel_artifact_sha256, "observation_channel_artifact_sha256")
        if self.result != "valid":
            raise ValueError("coverage proof verification receipt result must be 'valid'")


@runtime_checkable
class CoverageProofVerifier(Protocol):
    """Method-specific verifier for exact all-look coverage proof artifacts."""

    verifier_id: str

    def verify_all_look_coverage(
        self,
        contract: AllLookCoverageContract,
        artifact_payloads: Mapping[str, str | bytes],
    ) -> CoverageProofVerificationReceipt:
        """Check the coverage artifact against exact contract and artifact bytes."""


def coverage_contract_from_certificate(
    *,
    contract_id: str,
    target: ManifestTarget,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    observation_channel_artifact: ArtifactReference,
    retained_set_encoder_artifact: ArtifactReference,
    coverage_proof_artifact: ArtifactReference,
    coverage_verifier_id: str,
) -> AllLookCoverageContract:
    """Construct an all-look coverage contract from one existing theorem certificate."""

    contract = AllLookCoverageContract(
        contract_id=contract_id,
        target_digest=target.target_digest,
        candidate_space_artifact=target.candidate_space_artifact,
        observation_channel_artifact=observation_channel_artifact,
        retained_set_encoder_artifact=retained_set_encoder_artifact,
        coverage_proof_artifact=coverage_proof_artifact,
        true_candidate_label=coverage_certificate.true_candidate_label,
        required_cell_ids=coverage_certificate.required_cell_ids,
        certified_looks=coverage_certificate.certified_looks,
        lower_bound=coverage_certificate.lower_bound,
        method=coverage_certificate.method,
        assumptions=coverage_certificate.assumptions,
        coverage_verifier_id=coverage_verifier_id,
    )
    verify_all_look_coverage_contract_context(
        contract,
        target=target,
        coverage_certificate=coverage_certificate,
    )
    return contract


def verify_all_look_coverage_contract_context(
    contract: AllLookCoverageContract,
    *,
    target: ManifestTarget,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> None:
    """Verify that a coverage contract and a live RACH target assert one event."""

    if contract.target_digest != target.target_digest:
        raise ValueError("coverage contract target digest does not match the manifest target")
    if contract.candidate_space_artifact != target.candidate_space_artifact:
        raise ValueError("coverage contract candidate-space artifact does not match the manifest target")
    if contract.required_cell_ids != coverage_certificate.required_cell_ids:
        raise ValueError("coverage contract required cells do not match the coverage certificate")
    if contract.certified_looks != coverage_certificate.certified_looks:
        raise ValueError("coverage contract look scope does not match the coverage certificate")
    if contract.true_candidate_label != coverage_certificate.true_candidate_label:
        raise ValueError("coverage contract true candidate label does not match the coverage certificate")
    if contract.lower_bound != coverage_certificate.lower_bound:
        raise ValueError("coverage contract lower bound does not match the coverage certificate")
    if contract.method != coverage_certificate.method:
        raise ValueError("coverage contract method does not match the coverage certificate")
    if contract.assumptions != coverage_certificate.assumptions:
        raise ValueError("coverage contract assumptions do not match the coverage certificate")


def coverage_contract_artifact(
    contract: AllLookCoverageContract,
    *,
    artifact_id: str | None = None,
) -> ArtifactReference:
    """Return canonical contract bytes as a manifest/transcript-bindable artifact."""

    return ArtifactReference.from_payload(
        artifact_id or f"{ALL_LOOK_COVERAGE_CONTRACT_ARTIFACT_PREFIX}:{contract.contract_id}",
        contract.contract_payload,
        media_type="application/json",
    )


def verify_all_look_coverage_contract_artifacts(
    contract: AllLookCoverageContract,
    artifact_payloads: Mapping[str, str | bytes],
) -> None:
    """Verify hashes of every external object the contract names."""

    artifacts = contract.referenced_artifacts()
    missing = set(artifacts) - set(artifact_payloads)
    if missing:
        raise ValueError(f"missing payloads for all-look coverage artifacts: {sorted(missing)}")
    unexpected = set(artifact_payloads) - set(artifacts)
    if unexpected:
        raise ValueError(f"unexpected payloads for all-look coverage artifacts: {sorted(unexpected)}")
    for artifact_id, artifact in artifacts.items():
        if sha256_digest(artifact_payloads[artifact_id]) != artifact.sha256:
            raise ValueError(f"all-look coverage artifact digest mismatch for {artifact_id!r}")


def verify_all_look_coverage_contract(
    contract: AllLookCoverageContract,
    *,
    target: ManifestTarget,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    artifact_payloads: Mapping[str, str | bytes],
    verifier: CoverageProofVerifier,
) -> CoverageProofVerificationReceipt:
    """Run a method-specific verifier after RACH checks scope and content identity.

    A receipt is accepted only when it names the exact canonical contract digest,
    named verifier, coverage proof, retained-set encoder, and observation channel.
    The verifier's mathematical correctness remains an explicit external trust
    assumption, as is unavoidable for arbitrary coverage constructions.
    """

    verify_all_look_coverage_contract_context(
        contract,
        target=target,
        coverage_certificate=coverage_certificate,
    )
    verify_all_look_coverage_contract_artifacts(contract, artifact_payloads)
    if not isinstance(verifier, CoverageProofVerifier):
        raise TypeError("verifier must implement CoverageProofVerifier")
    if verifier.verifier_id != contract.coverage_verifier_id:
        raise ValueError("coverage proof verifier ID does not match the contract")
    receipt = verifier.verify_all_look_coverage(contract, artifact_payloads)
    if receipt.contract_digest != contract.contract_digest:
        raise ValueError("coverage proof receipt does not name the exact contract digest")
    if receipt.verifier_id != contract.coverage_verifier_id:
        raise ValueError("coverage proof receipt verifier ID does not match the contract")
    if receipt.coverage_proof_artifact_sha256 != contract.coverage_proof_artifact.sha256:
        raise ValueError("coverage proof receipt does not bind the exact proof artifact")
    if receipt.retained_set_encoder_artifact_sha256 != contract.retained_set_encoder_artifact.sha256:
        raise ValueError("coverage proof receipt does not bind the exact retained-set encoder")
    if receipt.observation_channel_artifact_sha256 != contract.observation_channel_artifact.sha256:
        raise ValueError("coverage proof receipt does not bind the exact observation channel")
    return receipt
