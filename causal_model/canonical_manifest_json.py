"""Strict canonical JSON v1 for hash-bound RACH certificate manifests.

``certificate_manifest`` already provides deterministic in-memory fingerprints,
but a later transcript or signature needs a byte-level interchange contract. This
module defines that contract for ``CertificateManifest`` itself:

* exact UTF-8 JSON bytes with no insignificant whitespace;
* sorted object keys;
* lower-bound probabilities encoded as canonical IEEE-754 hexadecimal wrappers;
* proof bindings sorted by their semantic query key; and
* a strict parser that rejects duplicate keys, unknown fields, malformed types,
  non-canonical float spellings, and syntactically valid but non-canonical bytes.

The existing ``CertificateManifest.manifest_digest`` is intentionally left
unchanged for backward compatibility. ``canonical_manifest_digest`` is the new
stable digest intended for append-only transcripts and future signatures.

This codec serializes the manifest contract, not arbitrary proof artifact
formats. Query encodings, Farkas proofs, and statistical evidence remain opaque
content-addressed artifacts whose bytes are committed by the manifest.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Mapping

from .certificate_manifest import (
    MANIFEST_FORMAT,
    ArtifactReference,
    CertificateManifest,
    ExternalAssertionBinding,
    ManifestTarget,
    QueryRole,
    SolverQueryProofBinding,
)
from .symbolic_candidate_sets import FeasibilityStatus


CANONICAL_MANIFEST_JSON_FORMAT = "rach-canonical-manifest-json/v1"
_FLOAT_KEY = "__float_hex__"
_HEX_DIGEST_LENGTH = 64


@dataclass(frozen=True)
class CanonicalManifestDocument:
    """A parsed or serialized manifest together with its canonical byte identity."""

    manifest: CertificateManifest
    canonical_bytes: bytes
    canonical_digest: str


def _require_manifest(manifest: CertificateManifest) -> None:
    if not isinstance(manifest, CertificateManifest):
        raise TypeError("manifest must be a CertificateManifest")


def _probability_object(value: float | int) -> dict[str, str]:
    """Encode a probability as one canonical finite IEEE-754 hexadecimal value."""

    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError("manifest probability must be finite")
    if not 0.0 <= numeric <= 1.0:
        raise ValueError("manifest probability must lie in [0, 1]")
    return {_FLOAT_KEY: numeric.hex()}


def _artifact_object(artifact: ArtifactReference) -> dict[str, str]:
    return {
        "artifact_id": artifact.artifact_id,
        "media_type": artifact.media_type,
        "sha256": artifact.sha256,
    }


def _target_object(target: ManifestTarget) -> dict[str, Any]:
    return {
        "candidate_space_artifact": _artifact_object(target.candidate_space_artifact),
        "candidate_space_description": target.candidate_space_description,
        "certified_looks": (
            None if target.certified_looks is None else list(sorted(target.certified_looks))
        ),
        "motif_definition_artifacts": {
            motif: _artifact_object(artifact)
            for motif, artifact in sorted(target.motif_definition_artifacts.items())
        },
        "required_cell_ids": list(target.required_cell_ids),
    }


def _assertion_object(assertion: ExternalAssertionBinding) -> dict[str, Any]:
    return {
        "assumptions": list(assertion.assumptions),
        "evidence_artifact": _artifact_object(assertion.evidence_artifact),
        "kind": assertion.kind,
        "lower_bound": _probability_object(assertion.lower_bound),
        "method": assertion.method,
    }


def _proof_sort_key(binding: SolverQueryProofBinding) -> tuple[int, str, str, str]:
    return (binding.look, binding.cell_id, binding.motif, binding.role.value)


def _proof_object(binding: SolverQueryProofBinding) -> dict[str, Any]:
    return {
        "cell_id": binding.cell_id,
        "look": binding.look,
        "motif": binding.motif,
        "proof_artifact": _artifact_object(binding.proof_artifact),
        "query_encoding_artifact": _artifact_object(binding.query_encoding_artifact),
        "role": binding.role.value,
        "status": binding.status.value,
        "verifier_id": binding.verifier_id,
    }


def canonical_manifest_object(manifest: CertificateManifest) -> dict[str, Any]:
    """Return the typed manifest as the canonical JSON-safe v1 object.

    Proof bindings form a semantically keyed set in the manifest contract, so
    their caller order is normalized. Required cells and assumptions remain
    ordered because the existing theorem APIs treat their tuple order as part of
    the declared target and assertion text.
    """

    _require_manifest(manifest)
    if manifest.format_version != MANIFEST_FORMAT:
        raise ValueError(f"unsupported manifest format: {manifest.format_version!r}")
    return {
        "coverage_assertion": _assertion_object(manifest.coverage_assertion),
        "format_version": manifest.format_version,
        "solver_assertion": _assertion_object(manifest.solver_assertion),
        "solver_query_proofs": [
            _proof_object(binding)
            for binding in sorted(manifest.solver_query_proofs, key=_proof_sort_key)
        ],
        "target": _target_object(manifest.target),
    }


def canonical_manifest_json(manifest: CertificateManifest) -> str:
    """Serialize one manifest to the exact canonical JSON v1 character sequence."""

    return json.dumps(
        canonical_manifest_object(manifest),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def canonical_manifest_bytes(manifest: CertificateManifest) -> bytes:
    """Return the exact UTF-8 bytes committed by canonical manifest digest/signature APIs."""

    return canonical_manifest_json(manifest).encode("utf-8")


def canonical_manifest_digest(manifest: CertificateManifest) -> str:
    """SHA-256 of strict canonical manifest bytes, independent of proof input order."""

    return sha256(canonical_manifest_bytes(manifest)).hexdigest()


def serialize_canonical_manifest(manifest: CertificateManifest) -> CanonicalManifestDocument:
    """Create a canonical document and its stable byte-level digest."""

    raw = canonical_manifest_bytes(manifest)
    return CanonicalManifestDocument(
        manifest=manifest,
        canonical_bytes=raw,
        canonical_digest=sha256(raw).hexdigest(),
    )


def _duplicate_key_rejecting_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _reject_nonfinite_json_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant is not permitted: {token}")


def _decode_payload(payload: str | bytes) -> tuple[str, bytes]:
    if isinstance(payload, str):
        raw = payload.encode("utf-8")
    elif isinstance(payload, bytes):
        raw = payload
    else:
        raise TypeError("canonical manifest payload must be str or bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("canonical manifest JSON must not include a UTF-8 byte-order mark")
    try:
        return raw.decode("utf-8"), raw
    except UnicodeDecodeError as error:
        raise ValueError("canonical manifest JSON must be valid UTF-8") from error


def _expect_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a JSON object")
    return value


def _expect_exact_keys(value: Any, expected: set[str], name: str) -> Mapping[str, Any]:
    mapping = _expect_mapping(value, name)
    observed = set(mapping)
    missing = expected - observed
    unknown = observed - expected
    if missing or unknown:
        details: list[str] = []
        if missing:
            details.append(f"missing={sorted(missing)}")
        if unknown:
            details.append(f"unknown={sorted(unknown)}")
        raise ValueError(f"{name} has invalid fields: {', '.join(details)}")
    return mapping


def _expect_string(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a JSON string")
    return value


def _expect_integer(value: Any, name: str, *, minimum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a JSON integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _expect_string_list(value: Any, name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{name} must be a JSON array of strings")
    return tuple(value)


def _expect_look_scope(value: Any, name: str) -> tuple[int, ...] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        raise ValueError(f"{name} must be null or a JSON array of positive integers")
    return tuple(_expect_integer(item, f"{name}[{index}]", minimum=1) for index, item in enumerate(value))


def _decode_probability(value: Any, name: str) -> float:
    mapping = _expect_exact_keys(value, {_FLOAT_KEY}, name)
    spelling = _expect_string(mapping[_FLOAT_KEY], f"{name}.{_FLOAT_KEY}")
    try:
        numeric = float.fromhex(spelling)
    except ValueError as error:
        raise ValueError(f"{name} has an invalid hexadecimal float spelling") from error
    if not isfinite(numeric) or numeric.hex() != spelling:
        raise ValueError(f"{name} must use a canonical finite hexadecimal float spelling")
    if not 0.0 <= numeric <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")
    return numeric


def _decode_artifact(value: Any, name: str) -> ArtifactReference:
    mapping = _expect_exact_keys(value, {"artifact_id", "media_type", "sha256"}, name)
    return ArtifactReference(
        artifact_id=_expect_string(mapping["artifact_id"], f"{name}.artifact_id"),
        media_type=_expect_string(mapping["media_type"], f"{name}.media_type"),
        sha256=_expect_string(mapping["sha256"], f"{name}.sha256"),
    )


def _decode_target(value: Any) -> ManifestTarget:
    mapping = _expect_exact_keys(
        value,
        {
            "candidate_space_artifact",
            "candidate_space_description",
            "certified_looks",
            "motif_definition_artifacts",
            "required_cell_ids",
        },
        "target",
    )
    motifs = _expect_mapping(mapping["motif_definition_artifacts"], "target.motif_definition_artifacts")
    if any(not isinstance(motif, str) for motif in motifs):
        raise ValueError("target.motif_definition_artifacts keys must be strings")
    return ManifestTarget(
        candidate_space_description=_expect_string(
            mapping["candidate_space_description"],
            "target.candidate_space_description",
        ),
        candidate_space_artifact=_decode_artifact(
            mapping["candidate_space_artifact"],
            "target.candidate_space_artifact",
        ),
        motif_definition_artifacts={
            motif: _decode_artifact(artifact, f"target.motif_definition_artifacts[{motif!r}]")
            for motif, artifact in motifs.items()
        },
        required_cell_ids=_expect_string_list(mapping["required_cell_ids"], "target.required_cell_ids"),
        certified_looks=_expect_look_scope(mapping["certified_looks"], "target.certified_looks"),
    )


def _decode_assertion(value: Any, name: str) -> ExternalAssertionBinding:
    mapping = _expect_exact_keys(
        value,
        {"assumptions", "evidence_artifact", "kind", "lower_bound", "method"},
        name,
    )
    return ExternalAssertionBinding(
        kind=_expect_string(mapping["kind"], f"{name}.kind"),
        lower_bound=_decode_probability(mapping["lower_bound"], f"{name}.lower_bound"),
        method=_expect_string(mapping["method"], f"{name}.method"),
        assumptions=_expect_string_list(mapping["assumptions"], f"{name}.assumptions"),
        evidence_artifact=_decode_artifact(mapping["evidence_artifact"], f"{name}.evidence_artifact"),
    )


def _decode_proof(value: Any, index: int) -> SolverQueryProofBinding:
    name = f"solver_query_proofs[{index}]"
    mapping = _expect_exact_keys(
        value,
        {
            "cell_id",
            "look",
            "motif",
            "proof_artifact",
            "query_encoding_artifact",
            "role",
            "status",
            "verifier_id",
        },
        name,
    )
    try:
        role = QueryRole(_expect_string(mapping["role"], f"{name}.role"))
    except ValueError as error:
        raise ValueError(f"{name}.role is not a supported query role") from error
    try:
        status = FeasibilityStatus(_expect_string(mapping["status"], f"{name}.status"))
    except ValueError as error:
        raise ValueError(f"{name}.status is not a supported feasibility status") from error
    return SolverQueryProofBinding(
        look=_expect_integer(mapping["look"], f"{name}.look", minimum=1),
        cell_id=_expect_string(mapping["cell_id"], f"{name}.cell_id"),
        motif=_expect_string(mapping["motif"], f"{name}.motif"),
        role=role,
        status=status,
        query_encoding_artifact=_decode_artifact(
            mapping["query_encoding_artifact"],
            f"{name}.query_encoding_artifact",
        ),
        proof_artifact=_decode_artifact(mapping["proof_artifact"], f"{name}.proof_artifact"),
        verifier_id=_expect_string(mapping["verifier_id"], f"{name}.verifier_id"),
    )


def _decode_manifest(value: Any) -> CertificateManifest:
    mapping = _expect_exact_keys(
        value,
        {
            "coverage_assertion",
            "format_version",
            "solver_assertion",
            "solver_query_proofs",
            "target",
        },
        "manifest",
    )
    proofs_raw = mapping["solver_query_proofs"]
    if not isinstance(proofs_raw, list):
        raise ValueError("manifest.solver_query_proofs must be a JSON array")
    return CertificateManifest(
        target=_decode_target(mapping["target"]),
        coverage_assertion=_decode_assertion(mapping["coverage_assertion"], "coverage_assertion"),
        solver_assertion=_decode_assertion(mapping["solver_assertion"], "solver_assertion"),
        solver_query_proofs=tuple(_decode_proof(item, index) for index, item in enumerate(proofs_raw)),
        format_version=_expect_string(mapping["format_version"], "format_version"),
    )


def parse_canonical_manifest(payload: str | bytes) -> CanonicalManifestDocument:
    """Strictly parse canonical manifest JSON and reject equivalent noncanonical bytes.

    This parser intentionally does *not* accept pretty-printed JSON, reordered
    keys, integer spellings for probabilities, or alternate Unicode escapes. A
    caller needing to migrate arbitrary JSON must first parse it in a separate
    migration tool and then explicitly serialize the returned manifest here.
    """

    text, raw = _decode_payload(payload)
    try:
        decoded = json.loads(
            text,
            object_pairs_hook=_duplicate_key_rejecting_object,
            parse_constant=_reject_nonfinite_json_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("canonical manifest payload is not valid JSON") from error
    manifest = _decode_manifest(decoded)
    canonical = canonical_manifest_bytes(manifest)
    if raw != canonical:
        raise ValueError("manifest JSON is valid but not strict canonical JSON v1")
    return CanonicalManifestDocument(
        manifest=manifest,
        canonical_bytes=canonical,
        canonical_digest=sha256(canonical).hexdigest(),
    )


def verify_canonical_manifest(
    payload: str | bytes,
    *,
    expected_digest: str | None = None,
) -> CanonicalManifestDocument:
    """Strictly parse a manifest and optionally verify its canonical SHA-256 digest."""

    document = parse_canonical_manifest(payload)
    if expected_digest is not None:
        if (
            not isinstance(expected_digest, str)
            or len(expected_digest) != _HEX_DIGEST_LENGTH
            or any(character not in "0123456789abcdef" for character in expected_digest)
        ):
            raise ValueError("expected_digest must be a lowercase SHA-256 hexadecimal digest")
        if document.canonical_digest != expected_digest:
            raise ValueError("canonical manifest digest does not match expected_digest")
    return document
