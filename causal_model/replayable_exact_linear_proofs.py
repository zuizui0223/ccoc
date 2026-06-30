"""Strict canonical artifacts and replay verification for exact linear proofs.

The exact rational linear backend already checks a ``LinearFeasibilityQuery`` in
memory.  Historical manifests and transcripts, however, previously bound only
opaque proof-artifact hashes.  This module defines a byte-level artifact format
from which an independent verifier can reconstruct the full query, witness, or
Farkas certificate and rerun exact verification.

Two formats are provided:

* one replayable SAT/UNSAT/UNKNOWN linear query; and
* one replayable finite branch family whose aggregate status is recomputed as
  an exact finite-union result.

All rationals are canonical strings produced by ``str(Fraction(...))``.  Binary
floating point, alternate fraction spellings, duplicate JSON keys, unknown
fields, and valid-but-noncanonical JSON bytes are rejected.  The artifact does
not prove that a query encodes the intended scientific predicate; the compiler
or another semantic layer must bind that query to a declared plan.  It does prove
that the bytes contain an exact replayable proof for the precise encoded system.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

from .certificate_manifest import ArtifactReference, QueryRole
from .linear_proof_verifier import (
    FarkasInfeasibilityCertificate,
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    RationalLinearSystem,
    RationalWitness,
    verify_linear_query,
)
from .symbolic_candidate_sets import FeasibilityCertificate, FeasibilityStatus


EXACT_LINEAR_QUERY_ARTIFACT_FORMAT = "rach-replayable-exact-linear-query/v1"
EXACT_LINEAR_BUNDLE_ARTIFACT_FORMAT = "rach-replayable-exact-linear-bundle/v1"
EXACT_LINEAR_PROOF_REPLAYER = "exact-rational-linear-proof-replayer"
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


def _canonical_rational(value: Fraction | int | str) -> str:
    if isinstance(value, float):
        raise TypeError("binary floating point is not allowed in replayable exact proof artifacts")
    try:
        return str(Fraction(value))
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise TypeError(f"cannot encode exact rational {value!r}") from error


def _parse_canonical_rational(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty canonical rational string")
    try:
        parsed = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{name} is not an exact rational string") from error
    if str(parsed) != value:
        raise ValueError(f"{name} is not a canonical rational string")
    return value


def _duplicate_key_rejecting_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _reject_nonfinite_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant is not allowed: {value}")


def _decode_payload(payload: str | bytes) -> tuple[str, bytes]:
    if isinstance(payload, bytes):
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("replayable exact proof payload must be valid UTF-8") from error
        raw = payload
    elif isinstance(payload, str):
        text = payload
        raw = payload.encode("utf-8")
    else:
        raise TypeError("replayable exact proof payload must be str or bytes")
    if text.startswith("\ufeff"):
        raise ValueError("replayable exact proof payload must not contain a UTF-8 BOM")
    return text, raw


def _expect_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a JSON object")
    return value


def _expect_exact_keys(value: Any, expected: set[str], name: str) -> Mapping[str, Any]:
    mapping = _expect_mapping(value, name)
    actual = set(mapping)
    missing = expected - actual
    unexpected = actual - expected
    if missing:
        raise ValueError(f"{name} is missing fields: {sorted(missing)}")
    if unexpected:
        raise ValueError(f"{name} has unknown fields: {sorted(unexpected)}")
    return mapping


def _expect_string(value: Any, name: str, *, nonempty: bool = False) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a JSON string")
    if nonempty and not value:
        raise ValueError(f"{name} must be non-empty")
    return value


def _expect_string_tuple(value: Any, name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a JSON array")
    return tuple(_expect_string(item, f"{name}[{index}]") for index, item in enumerate(value))


def _strict_json(payload: str | bytes) -> tuple[Any, bytes]:
    text, raw = _decode_payload(payload)
    try:
        decoded = json.loads(
            text,
            object_pairs_hook=_duplicate_key_rejecting_object,
            parse_constant=_reject_nonfinite_json_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("replayable exact proof payload is not valid JSON") from error
    return decoded, raw


def _inequality_object(inequality: LinearInequality) -> dict[str, Any]:
    return {
        "coefficients": [_canonical_rational(value) for value in inequality.coefficients],
        "bound": _canonical_rational(inequality.bound),
    }


def _system_object(system: RationalLinearSystem) -> dict[str, Any]:
    return {
        "inequalities": [_inequality_object(inequality) for inequality in system.inequalities],
        "variables": list(system.variables),
    }


def _proof_object(proof: LinearFeasibilityProof) -> dict[str, Any]:
    return {
        "evidence_reference": proof.evidence_reference,
        "farkas_multipliers": (
            None
            if proof.farkas is None
            else [_canonical_rational(value) for value in proof.farkas.multipliers]
        ),
        "producer": proof.producer,
        "status": proof.status.value,
        "witness": (
            None
            if proof.witness is None
            else [_canonical_rational(value) for value in proof.witness.values]
        ),
    }


def _query_object(query: LinearFeasibilityQuery) -> dict[str, Any]:
    return {
        "assumptions": list(query.assumptions),
        "proof": _proof_object(query.proof),
        "query_id": query.query_id,
        "system": _system_object(query.system),
    }


def _parse_system(value: Any, name: str) -> RationalLinearSystem:
    mapping = _expect_exact_keys(value, {"inequalities", "variables"}, name)
    variables = _expect_string_tuple(mapping["variables"], f"{name}.variables")
    if not isinstance(mapping["inequalities"], list):
        raise ValueError(f"{name}.inequalities must be a JSON array")
    inequalities: list[LinearInequality] = []
    for index, raw in enumerate(mapping["inequalities"]):
        row_name = f"{name}.inequalities[{index}]"
        row = _expect_exact_keys(raw, {"coefficients", "bound"}, row_name)
        if not isinstance(row["coefficients"], list):
            raise ValueError(f"{row_name}.coefficients must be a JSON array")
        coefficients = tuple(
            _parse_canonical_rational(item, f"{row_name}.coefficients[{column}]")
            for column, item in enumerate(row["coefficients"])
        )
        bound = _parse_canonical_rational(row["bound"], f"{row_name}.bound")
        inequalities.append(LinearInequality(coefficients=coefficients, bound=bound))
    return RationalLinearSystem(variables=variables, inequalities=tuple(inequalities))


def _parse_status(value: Any, name: str) -> FeasibilityStatus:
    try:
        return FeasibilityStatus(_expect_string(value, name, nonempty=True))
    except ValueError as error:
        raise ValueError(f"{name} is not a supported feasibility status") from error


def _parse_rational_vector(value: Any, name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a JSON array")
    return tuple(_parse_canonical_rational(item, f"{name}[{index}]") for index, item in enumerate(value))


def _parse_proof(value: Any, name: str) -> LinearFeasibilityProof:
    mapping = _expect_exact_keys(
        value,
        {"evidence_reference", "farkas_multipliers", "producer", "status", "witness"},
        name,
    )
    status = _parse_status(mapping["status"], f"{name}.status")
    evidence_reference = _expect_string(mapping["evidence_reference"], f"{name}.evidence_reference")
    producer = _expect_string(mapping["producer"], f"{name}.producer", nonempty=True)
    witness_raw = mapping["witness"]
    farkas_raw = mapping["farkas_multipliers"]
    witness = None if witness_raw is None else RationalWitness(_parse_rational_vector(witness_raw, f"{name}.witness"))
    farkas = (
        None
        if farkas_raw is None
        else FarkasInfeasibilityCertificate(
            _parse_rational_vector(farkas_raw, f"{name}.farkas_multipliers")
        )
    )
    return LinearFeasibilityProof(
        status=status,
        evidence_reference=evidence_reference,
        witness=witness,
        farkas=farkas,
        producer=producer,
    )


def _parse_query(value: Any, name: str) -> LinearFeasibilityQuery:
    mapping = _expect_exact_keys(value, {"assumptions", "proof", "query_id", "system"}, name)
    return LinearFeasibilityQuery(
        query_id=_expect_string(mapping["query_id"], f"{name}.query_id", nonempty=True),
        system=_parse_system(mapping["system"], f"{name}.system"),
        proof=_parse_proof(mapping["proof"], f"{name}.proof"),
        assumptions=_expect_string_tuple(mapping["assumptions"], f"{name}.assumptions"),
    )


@dataclass(frozen=True)
class ReplayableExactLinearQueryDocument:
    """One exact query plus strict canonical bytes and its replayed certificate."""

    query: LinearFeasibilityQuery
    canonical_bytes: bytes
    canonical_digest: str
    certificate: FeasibilityCertificate | None = None


def canonical_exact_linear_query_object(query: LinearFeasibilityQuery) -> dict[str, Any]:
    """Return canonical JSON-safe content for one exact rational feasibility query."""

    if not isinstance(query, LinearFeasibilityQuery):
        raise TypeError("query must be a LinearFeasibilityQuery")
    return {
        "format_version": EXACT_LINEAR_QUERY_ARTIFACT_FORMAT,
        "query": _query_object(query),
    }


def canonical_exact_linear_query_bytes(query: LinearFeasibilityQuery) -> bytes:
    """Serialize a query into its unique compact UTF-8 artifact bytes."""

    # A producer must not mint an allegedly replayable artifact that does not
    # verify at generation time. Parsing remains separate from replay.
    verify_linear_query(query)
    return json.dumps(
        canonical_exact_linear_query_object(query),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def exact_linear_query_artifact(
    query: LinearFeasibilityQuery,
    *,
    artifact_id: str | None = None,
) -> ArtifactReference:
    """Create a content-addressed artifact for an exactly replayable query proof."""

    raw = canonical_exact_linear_query_bytes(query)
    return ArtifactReference.from_payload(
        artifact_id or f"exact-linear-query:{query.query_id}",
        raw,
        media_type="application/json",
    )


def parse_canonical_exact_linear_query(payload: str | bytes) -> ReplayableExactLinearQueryDocument:
    """Strictly parse canonical query bytes without trusting their proof semantics."""

    decoded, raw = _strict_json(payload)
    root = _expect_exact_keys(decoded, {"format_version", "query"}, "exact_linear_query")
    if _expect_string(root["format_version"], "format_version", nonempty=True) != EXACT_LINEAR_QUERY_ARTIFACT_FORMAT:
        raise ValueError("unsupported replayable exact linear query format")
    query = _parse_query(root["query"], "query")
    canonical = json.dumps(
        canonical_exact_linear_query_object(query),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    if raw != canonical:
        raise ValueError("exact linear query JSON is valid but not strict canonical JSON")
    return ReplayableExactLinearQueryDocument(
        query=query,
        canonical_bytes=canonical,
        canonical_digest=sha256(canonical).hexdigest(),
    )


def replay_exact_linear_query(
    payload: str | bytes,
    *,
    expected_digest: str | None = None,
) -> ReplayableExactLinearQueryDocument:
    """Strictly parse and independently rerun exact SAT/UNSAT verification."""

    document = parse_canonical_exact_linear_query(payload)
    if expected_digest is not None:
        _require_digest(expected_digest, "expected_digest")
        if document.canonical_digest != expected_digest:
            raise ValueError("exact linear query digest does not match expected_digest")
    certificate = verify_linear_query(document.query)
    return ReplayableExactLinearQueryDocument(
        query=document.query,
        canonical_bytes=document.canonical_bytes,
        canonical_digest=document.canonical_digest,
        certificate=certificate,
    )


@dataclass(frozen=True)
class ExactLinearProofBundle:
    """Finite branch family used to prove one union feasibility status exactly."""

    bundle_id: str
    plan_digest: str
    partition_digest: str
    motif: str
    role: QueryRole
    branches: tuple[LinearFeasibilityQuery, ...]
    aggregate_status: FeasibilityStatus

    def __post_init__(self) -> None:
        _require_nonempty(self.bundle_id, "bundle_id")
        _require_digest(self.plan_digest, "plan_digest")
        _require_digest(self.partition_digest, "partition_digest")
        _require_nonempty(self.motif, "motif")
        if not isinstance(self.role, QueryRole):
            raise ValueError("bundle role must be a QueryRole")
        if not isinstance(self.aggregate_status, FeasibilityStatus):
            raise ValueError("bundle aggregate_status must be a FeasibilityStatus")
        query_ids = tuple(query.query_id for query in self.branches)
        if len(set(query_ids)) != len(query_ids):
            raise ValueError("replayable exact linear bundle branch query IDs must be unique")


@dataclass(frozen=True)
class ReplayableExactLinearBundleDocument:
    """One branch family with exact replay result for every branch and union status."""

    bundle: ExactLinearProofBundle
    canonical_bytes: bytes
    canonical_digest: str
    branch_certificates: Mapping[str, FeasibilityCertificate] | None = None
    replayed_aggregate_status: FeasibilityStatus | None = None


def _bundle_object(bundle: ExactLinearProofBundle) -> dict[str, Any]:
    return {
        "aggregate_status": bundle.aggregate_status.value,
        "branches": [
            _query_object(query)
            for query in sorted(bundle.branches, key=lambda item: item.query_id)
        ],
        "bundle_id": bundle.bundle_id,
        "format_version": EXACT_LINEAR_BUNDLE_ARTIFACT_FORMAT,
        "motif": bundle.motif,
        "partition_digest": bundle.partition_digest,
        "plan_digest": bundle.plan_digest,
        "role": bundle.role.value,
    }


def _aggregate_status(certificates: Iterable[FeasibilityCertificate]) -> FeasibilityStatus:
    statuses = tuple(certificate.status for certificate in certificates)
    if any(status is FeasibilityStatus.SAT for status in statuses):
        return FeasibilityStatus.SAT
    if all(status is FeasibilityStatus.UNSAT for status in statuses):
        # The empty union is empty, hence UNSAT. This is needed for a tag family
        # with no cells and matches finite-union semantics in the compiler.
        return FeasibilityStatus.UNSAT
    return FeasibilityStatus.UNKNOWN


def canonical_exact_linear_bundle_bytes(bundle: ExactLinearProofBundle) -> bytes:
    """Serialize a branch family only after exact replay validates every branch."""

    replay_exact_linear_bundle_object(bundle)
    return json.dumps(
        _bundle_object(bundle),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def exact_linear_bundle_artifact(
    bundle: ExactLinearProofBundle,
    *,
    artifact_id: str | None = None,
) -> ArtifactReference:
    """Create one replayable artifact for every exact finite branch family."""

    raw = canonical_exact_linear_bundle_bytes(bundle)
    return ArtifactReference.from_payload(
        artifact_id or f"exact-linear-bundle:{bundle.bundle_id}",
        raw,
        media_type="application/json",
    )


def _parse_bundle(decoded: Any) -> ExactLinearProofBundle:
    root = _expect_exact_keys(
        decoded,
        {
            "aggregate_status",
            "branches",
            "bundle_id",
            "format_version",
            "motif",
            "partition_digest",
            "plan_digest",
            "role",
        },
        "exact_linear_bundle",
    )
    if _expect_string(root["format_version"], "format_version", nonempty=True) != EXACT_LINEAR_BUNDLE_ARTIFACT_FORMAT:
        raise ValueError("unsupported replayable exact linear bundle format")
    if not isinstance(root["branches"], list):
        raise ValueError("branches must be a JSON array")
    try:
        role = QueryRole(_expect_string(root["role"], "role", nonempty=True))
    except ValueError as error:
        raise ValueError("role is not a supported query role") from error
    return ExactLinearProofBundle(
        bundle_id=_expect_string(root["bundle_id"], "bundle_id", nonempty=True),
        plan_digest=_expect_string(root["plan_digest"], "plan_digest", nonempty=True),
        partition_digest=_expect_string(root["partition_digest"], "partition_digest", nonempty=True),
        motif=_expect_string(root["motif"], "motif", nonempty=True),
        role=role,
        branches=tuple(_parse_query(item, f"branches[{index}]") for index, item in enumerate(root["branches"])),
        aggregate_status=_parse_status(root["aggregate_status"], "aggregate_status"),
    )


def parse_canonical_exact_linear_bundle(payload: str | bytes) -> ReplayableExactLinearBundleDocument:
    """Strictly parse one canonical branch-family artifact without trusting its proof."""

    decoded, raw = _strict_json(payload)
    bundle = _parse_bundle(decoded)
    canonical = json.dumps(
        _bundle_object(bundle),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    if raw != canonical:
        raise ValueError("exact linear bundle JSON is valid but not strict canonical JSON")
    return ReplayableExactLinearBundleDocument(
        bundle=bundle,
        canonical_bytes=canonical,
        canonical_digest=sha256(canonical).hexdigest(),
    )


def replay_exact_linear_bundle_object(bundle: ExactLinearProofBundle) -> ReplayableExactLinearBundleDocument:
    """Rerun every branch proof and recompute exact finite-union aggregation."""

    certificates = {
        query.query_id: verify_linear_query(query)
        for query in bundle.branches
    }
    replayed = _aggregate_status(certificates.values())
    if replayed is not bundle.aggregate_status:
        raise ValueError("exact linear bundle declared aggregate status disagrees with replay")
    canonical = json.dumps(
        _bundle_object(bundle),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return ReplayableExactLinearBundleDocument(
        bundle=bundle,
        canonical_bytes=canonical,
        canonical_digest=sha256(canonical).hexdigest(),
        branch_certificates=certificates,
        replayed_aggregate_status=replayed,
    )


def replay_exact_linear_bundle(
    payload: str | bytes,
    *,
    expected_digest: str | None = None,
    expected_plan_digest: str | None = None,
    expected_partition_digest: str | None = None,
    expected_motif: str | None = None,
    expected_role: QueryRole | None = None,
) -> ReplayableExactLinearBundleDocument:
    """Strictly parse, context-check, and replay an exact finite branch family."""

    document = parse_canonical_exact_linear_bundle(payload)
    if expected_digest is not None:
        _require_digest(expected_digest, "expected_digest")
        if document.canonical_digest != expected_digest:
            raise ValueError("exact linear bundle digest does not match expected_digest")
    bundle = document.bundle
    if expected_plan_digest is not None and bundle.plan_digest != expected_plan_digest:
        raise ValueError("exact linear bundle plan digest does not match the expected plan")
    if expected_partition_digest is not None and bundle.partition_digest != expected_partition_digest:
        raise ValueError("exact linear bundle partition digest does not match the expected partition")
    if expected_motif is not None and bundle.motif != expected_motif:
        raise ValueError("exact linear bundle motif does not match the expected motif")
    if expected_role is not None and bundle.role is not expected_role:
        raise ValueError("exact linear bundle role does not match the expected role")
    replayed = replay_exact_linear_bundle_object(bundle)
    return ReplayableExactLinearBundleDocument(
        bundle=replayed.bundle,
        canonical_bytes=document.canonical_bytes,
        canonical_digest=document.canonical_digest,
        branch_certificates=replayed.branch_certificates,
        replayed_aggregate_status=replayed.replayed_aggregate_status,
    )
