"""Strict canonical JSON v2 for tier-aware RACH certificate manifests.

This module is intentionally separate from ``canonical_manifest_json``.  The
v1 byte contract is part of already signed transcript history and must not gain
a new ``tier`` field retroactively.  Manifest v2 has its own format identifier,
strict parser, canonical bytes, and digest.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

from .canonical_manifest_json import (
    _artifact_object,
    _assertion_object,
    _decode_artifact,
    _decode_assertion,
    _decode_payload,
    _decode_target,
    _duplicate_key_rejecting_object,
    _expect_exact_keys,
    _expect_integer,
    _expect_mapping,
    _expect_string,
    _reject_nonfinite_json_constant,
    _target_object,
)
from .certificate_manifest import QueryRole
from .symbolic_candidate_sets import FeasibilityStatus
from .tiered_certificate_manifest import (
    TIERED_MANIFEST_FORMAT,
    QueryTier,
    TieredCertificateManifest,
    TieredQueryPlanBinding,
    TieredSolverQueryProofBinding,
)


CANONICAL_TIERED_MANIFEST_JSON_FORMAT = "rach-canonical-tiered-manifest-json/v2"
_HEX_DIGEST_LENGTH = 64


@dataclass(frozen=True)
class CanonicalTieredManifestDocument:
    """A tiered v2 manifest together with its strict canonical byte identity."""

    manifest: TieredCertificateManifest
    canonical_bytes: bytes
    canonical_digest: str


def _require_manifest(manifest: TieredCertificateManifest) -> None:
    if not isinstance(manifest, TieredCertificateManifest):
        raise TypeError("manifest must be a TieredCertificateManifest")


def _plan_sort_key(binding: TieredQueryPlanBinding) -> tuple[str, int, str]:
    return (binding.tier.value, binding.look, binding.cell_id)


def _proof_sort_key(binding: TieredSolverQueryProofBinding) -> tuple[str, int, str, str, str]:
    return (binding.tier.value, binding.look, binding.cell_id, binding.motif, binding.role.value)


def _plan_object(binding: TieredQueryPlanBinding) -> dict[str, Any]:
    return {
        "cell_id": binding.cell_id,
        "look": binding.look,
        "query_plan_artifact": _artifact_object(binding.query_plan_artifact),
        "tier": binding.tier.value,
    }


def _proof_object(binding: TieredSolverQueryProofBinding) -> dict[str, Any]:
    return {
        "cell_id": binding.cell_id,
        "look": binding.look,
        "motif": binding.motif,
        "proof_artifact": _artifact_object(binding.proof_artifact),
        "query_plan_artifact": _artifact_object(binding.query_plan_artifact),
        "role": binding.role.value,
        "status": binding.status.value,
        "tier": binding.tier.value,
        "verifier_id": binding.verifier_id,
    }


def canonical_tiered_manifest_object(manifest: TieredCertificateManifest) -> dict[str, Any]:
    """Return one v2 manifest as its canonical JSON-safe object."""

    _require_manifest(manifest)
    if manifest.format_version != TIERED_MANIFEST_FORMAT:
        raise ValueError(f"unsupported tiered manifest format: {manifest.format_version!r}")
    return {
        "coverage_assertion": _assertion_object(manifest.coverage_assertion),
        "format_version": manifest.format_version,
        "semantic_partition_artifact": _artifact_object(manifest.semantic_partition_artifact),
        "solver_assertion": _assertion_object(manifest.solver_assertion),
        "solver_query_proofs": [
            _proof_object(binding)
            for binding in sorted(manifest.solver_query_proofs, key=_proof_sort_key)
        ],
        "target": _target_object(manifest.target),
        "tiered_query_plans": [
            _plan_object(binding)
            for binding in sorted(manifest.tiered_query_plans, key=_plan_sort_key)
        ],
    }


def canonical_tiered_manifest_json(manifest: TieredCertificateManifest) -> str:
    """Serialize one v2 manifest to its exact canonical JSON character sequence."""

    return json.dumps(
        canonical_tiered_manifest_object(manifest),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def canonical_tiered_manifest_bytes(manifest: TieredCertificateManifest) -> bytes:
    """Return exact UTF-8 bytes committed by v2 transcript/signature consumers."""

    return canonical_tiered_manifest_json(manifest).encode("utf-8")


def canonical_tiered_manifest_digest(manifest: TieredCertificateManifest) -> str:
    """SHA-256 of strict v2 bytes, independent of caller order for plan/proof sets."""

    return sha256(canonical_tiered_manifest_bytes(manifest)).hexdigest()


def serialize_canonical_tiered_manifest(
    manifest: TieredCertificateManifest,
) -> CanonicalTieredManifestDocument:
    raw = canonical_tiered_manifest_bytes(manifest)
    return CanonicalTieredManifestDocument(
        manifest=manifest,
        canonical_bytes=raw,
        canonical_digest=sha256(raw).hexdigest(),
    )


def _decode_tier(value: Any, name: str) -> QueryTier:
    try:
        return QueryTier(_expect_string(value, name))
    except ValueError as error:
        raise ValueError(f"{name} is not a supported query tier") from error


def _decode_role(value: Any, name: str) -> QueryRole:
    try:
        return QueryRole(_expect_string(value, name))
    except ValueError as error:
        raise ValueError(f"{name} is not a supported query role") from error


def _decode_status(value: Any, name: str) -> FeasibilityStatus:
    try:
        return FeasibilityStatus(_expect_string(value, name))
    except ValueError as error:
        raise ValueError(f"{name} is not a supported feasibility status") from error


def _decode_plan(value: Any, index: int) -> TieredQueryPlanBinding:
    name = f"tiered_query_plans[{index}]"
    mapping = _expect_exact_keys(
        value,
        {"cell_id", "look", "query_plan_artifact", "tier"},
        name,
    )
    return TieredQueryPlanBinding(
        tier=_decode_tier(mapping["tier"], f"{name}.tier"),
        look=_expect_integer(mapping["look"], f"{name}.look", minimum=1),
        cell_id=_expect_string(mapping["cell_id"], f"{name}.cell_id"),
        query_plan_artifact=_decode_artifact(
            mapping["query_plan_artifact"],
            f"{name}.query_plan_artifact",
        ),
    )


def _decode_proof(value: Any, index: int) -> TieredSolverQueryProofBinding:
    name = f"solver_query_proofs[{index}]"
    mapping = _expect_exact_keys(
        value,
        {
            "cell_id",
            "look",
            "motif",
            "proof_artifact",
            "query_plan_artifact",
            "role",
            "status",
            "tier",
            "verifier_id",
        },
        name,
    )
    return TieredSolverQueryProofBinding(
        tier=_decode_tier(mapping["tier"], f"{name}.tier"),
        look=_expect_integer(mapping["look"], f"{name}.look", minimum=1),
        cell_id=_expect_string(mapping["cell_id"], f"{name}.cell_id"),
        motif=_expect_string(mapping["motif"], f"{name}.motif"),
        role=_decode_role(mapping["role"], f"{name}.role"),
        status=_decode_status(mapping["status"], f"{name}.status"),
        query_plan_artifact=_decode_artifact(
            mapping["query_plan_artifact"],
            f"{name}.query_plan_artifact",
        ),
        proof_artifact=_decode_artifact(mapping["proof_artifact"], f"{name}.proof_artifact"),
        verifier_id=_expect_string(mapping["verifier_id"], f"{name}.verifier_id"),
    )


def _decode_manifest(value: Any) -> TieredCertificateManifest:
    mapping = _expect_exact_keys(
        value,
        {
            "coverage_assertion",
            "format_version",
            "semantic_partition_artifact",
            "solver_assertion",
            "solver_query_proofs",
            "target",
            "tiered_query_plans",
        },
        "tiered_manifest",
    )
    plans = mapping["tiered_query_plans"]
    proofs = mapping["solver_query_proofs"]
    if not isinstance(plans, list):
        raise ValueError("tiered_manifest.tiered_query_plans must be a JSON array")
    if not isinstance(proofs, list):
        raise ValueError("tiered_manifest.solver_query_proofs must be a JSON array")
    return TieredCertificateManifest(
        target=_decode_target(mapping["target"]),
        coverage_assertion=_decode_assertion(mapping["coverage_assertion"], "coverage_assertion"),
        solver_assertion=_decode_assertion(mapping["solver_assertion"], "solver_assertion"),
        semantic_partition_artifact=_decode_artifact(
            mapping["semantic_partition_artifact"],
            "semantic_partition_artifact",
        ),
        tiered_query_plans=tuple(_decode_plan(item, index) for index, item in enumerate(plans)),
        solver_query_proofs=tuple(_decode_proof(item, index) for index, item in enumerate(proofs)),
        format_version=_expect_string(mapping["format_version"], "format_version"),
    )


def parse_canonical_tiered_manifest(payload: str | bytes) -> CanonicalTieredManifestDocument:
    """Strictly parse v2 JSON and reject any equivalent noncanonical byte spelling."""

    text, raw = _decode_payload(payload)
    try:
        decoded = json.loads(
            text,
            object_pairs_hook=_duplicate_key_rejecting_object,
            parse_constant=_reject_nonfinite_json_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("canonical tiered manifest payload is not valid JSON") from error
    manifest = _decode_manifest(decoded)
    canonical = canonical_tiered_manifest_bytes(manifest)
    if raw != canonical:
        raise ValueError("tiered manifest JSON is valid but not strict canonical JSON v2")
    return CanonicalTieredManifestDocument(
        manifest=manifest,
        canonical_bytes=canonical,
        canonical_digest=sha256(canonical).hexdigest(),
    )


def verify_canonical_tiered_manifest(
    payload: str | bytes,
    *,
    expected_digest: str | None = None,
) -> CanonicalTieredManifestDocument:
    """Strictly parse v2 JSON and optionally verify a lowercase SHA-256 digest."""

    document = parse_canonical_tiered_manifest(payload)
    if expected_digest is not None:
        if (
            not isinstance(expected_digest, str)
            or len(expected_digest) != _HEX_DIGEST_LENGTH
            or any(character not in "0123456789abcdef" for character in expected_digest)
        ):
            raise ValueError("expected_digest must be a lowercase SHA-256 hexadecimal digest")
        if document.canonical_digest != expected_digest:
            raise ValueError("canonical tiered manifest digest does not match expected_digest")
    return document
