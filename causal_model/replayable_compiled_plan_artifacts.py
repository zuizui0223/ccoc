"""Strict replayable artifacts for compiler-generated polyhedral query plans.

A replayable exact branch proof establishes SAT/UNSAT for an encoded linear
system. To prevent a proof from being attached to another compiler plan, the
plan itself also needs a canonical, parseable artifact. This module serializes
the exact branch templates emitted by ``CompiledPolyhedralMotifQueryPlan``.

The artifact is deliberately a *template* record, not a second implementation
of the motif compiler. It binds the plan and partition digests claimed by the
compiler, then lists every generated query ID, role, motif, partition cell, and
exact rational system. Consumers can reconstruct the expected family for a
particular motif/role and compare replayed proof systems byte-independently.

The in-memory compiler remains responsible for generating the plan. The strict
artifact lets an auditor replay that plan's emitted branch systems after the
fact, provided the plan artifact was produced during an admitted run.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from .certificate_manifest import ArtifactReference, QueryRole
from .linear_proof_verifier import LinearInequality, RationalLinearSystem
from .polyhedral_motif_compiler import CompiledLinearQueryTemplate, CompiledPolyhedralMotifQueryPlan


REPLAYABLE_COMPILED_PLAN_ARTIFACT_FORMAT = "rach-replayable-compiled-polyhedral-plan/v1"
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


def _canonical_rational(value: object) -> str:
    if isinstance(value, float):
        raise TypeError("binary floating point is not allowed in replayable compiler plans")
    try:
        return str(Fraction(value))
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise TypeError(f"cannot encode exact rational {value!r}") from error


def _parse_rational(value: Any, name: str) -> Fraction:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty canonical rational string")
    try:
        rational = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{name} is not an exact rational string") from error
    if str(rational) != value:
        raise ValueError(f"{name} is not a canonical rational string")
    return rational


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
            raise ValueError("replayable compiler plan payload must be valid UTF-8") from error
        raw = payload
    elif isinstance(payload, str):
        text = payload
        raw = payload.encode("utf-8")
    else:
        raise TypeError("replayable compiler plan payload must be str or bytes")
    if text.startswith("\ufeff"):
        raise ValueError("replayable compiler plan payload must not contain a UTF-8 BOM")
    return text, raw


def _expect_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a JSON object")
    return value


def _expect_exact_keys(value: Any, expected: set[str], name: str) -> Mapping[str, Any]:
    mapping = _expect_mapping(value, name)
    missing = expected - set(mapping)
    unexpected = set(mapping) - expected
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


def _parse_role(value: Any, name: str) -> QueryRole:
    try:
        return QueryRole(_expect_string(value, name, nonempty=True))
    except ValueError as error:
        raise ValueError(f"{name} is not a supported query role") from error


def _system_object(system: RationalLinearSystem) -> dict[str, Any]:
    return {
        "variables": list(system.variables),
        "inequalities": [
            {
                "coefficients": [_canonical_rational(value) for value in inequality.coefficients],
                "bound": _canonical_rational(inequality.bound),
            }
            for inequality in system.inequalities
        ],
    }


def _parse_system(value: Any, name: str) -> RationalLinearSystem:
    mapping = _expect_exact_keys(value, {"variables", "inequalities"}, name)
    if not isinstance(mapping["variables"], list):
        raise ValueError(f"{name}.variables must be a JSON array")
    variables = tuple(
        _expect_string(item, f"{name}.variables[{index}]", nonempty=True)
        for index, item in enumerate(mapping["variables"])
    )
    if len(set(variables)) != len(variables):
        raise ValueError(f"{name}.variables must be unique")
    if not isinstance(mapping["inequalities"], list):
        raise ValueError(f"{name}.inequalities must be a JSON array")
    inequalities: list[LinearInequality] = []
    for index, raw_row in enumerate(mapping["inequalities"]):
        row_name = f"{name}.inequalities[{index}]"
        row = _expect_exact_keys(raw_row, {"coefficients", "bound"}, row_name)
        if not isinstance(row["coefficients"], list):
            raise ValueError(f"{row_name}.coefficients must be a JSON array")
        coefficients = tuple(
            _parse_rational(item, f"{row_name}.coefficients[{column}]")
            for column, item in enumerate(row["coefficients"])
        )
        bound = _parse_rational(row["bound"], f"{row_name}.bound")
        inequalities.append(LinearInequality(coefficients=coefficients, bound=bound))
    return RationalLinearSystem(variables=variables, inequalities=tuple(inequalities))


@dataclass(frozen=True)
class ReplayableCompiledPlanTemplate:
    """One compiler-emitted exact branch template recorded for independent comparison."""

    query_id: str
    role: QueryRole
    motif: str | None
    partition_cell_id: str
    system: RationalLinearSystem

    def __post_init__(self) -> None:
        _require_nonempty(self.query_id, "query_id")
        _require_nonempty(self.partition_cell_id, "partition_cell_id")
        if self.role is QueryRole.NONEMPTY:
            if self.motif is not None:
                raise ValueError("nonempty replayable plan templates must have motif=None")
        elif not isinstance(self.motif, str) or not self.motif:
            raise ValueError("active/inactive replayable plan templates need a non-empty motif")


@dataclass(frozen=True)
class ReplayableCompiledPolyhedralPlan:
    """Canonical record of all exact branch templates emitted by one compiler plan."""

    plan_digest: str
    partition_digest: str
    query_prefix: str
    templates: tuple[ReplayableCompiledPlanTemplate, ...]

    def __post_init__(self) -> None:
        _require_digest(self.plan_digest, "plan_digest")
        _require_digest(self.partition_digest, "partition_digest")
        _require_nonempty(self.query_prefix, "query_prefix")
        query_ids = tuple(template.query_id for template in self.templates)
        if len(set(query_ids)) != len(query_ids):
            raise ValueError("replayable compiler plan template query IDs must be unique")

    def templates_for(self, *, motif: str, role: QueryRole) -> tuple[ReplayableCompiledPlanTemplate, ...]:
        if role is QueryRole.NONEMPTY:
            return tuple(template for template in self.templates if template.role is QueryRole.NONEMPTY)
        return tuple(
            template
            for template in self.templates
            if template.role is role and template.motif == motif
        )


@dataclass(frozen=True)
class ReplayableCompiledPlanDocument:
    """Strict canonical bytes and a reconstructed compiler-template record."""

    plan: ReplayableCompiledPolyhedralPlan
    canonical_bytes: bytes
    canonical_digest: str


def _template_object(template: ReplayableCompiledPlanTemplate) -> dict[str, Any]:
    return {
        "motif": template.motif,
        "partition_cell_id": template.partition_cell_id,
        "query_id": template.query_id,
        "role": template.role.value,
        "system": _system_object(template.system),
    }


def _plan_object(plan: ReplayableCompiledPolyhedralPlan) -> dict[str, Any]:
    return {
        "format_version": REPLAYABLE_COMPILED_PLAN_ARTIFACT_FORMAT,
        "partition_digest": plan.partition_digest,
        "plan_digest": plan.plan_digest,
        "query_prefix": plan.query_prefix,
        "templates": [
            _template_object(template)
            for template in sorted(plan.templates, key=lambda item: item.query_id)
        ],
    }


def build_replayable_compiled_plan(
    plan: CompiledPolyhedralMotifQueryPlan,
) -> ReplayableCompiledPolyhedralPlan:
    """Capture all compiler-generated templates from one in-memory verified plan."""

    if not isinstance(plan, CompiledPolyhedralMotifQueryPlan):
        raise TypeError("plan must be a CompiledPolyhedralMotifQueryPlan")
    return ReplayableCompiledPolyhedralPlan(
        plan_digest=plan.plan_digest,
        partition_digest=plan.verified_partition.partition_digest,
        query_prefix=plan.query_prefix,
        templates=tuple(
            ReplayableCompiledPlanTemplate(
                query_id=template.query_id,
                role=template.role,
                motif=template.motif,
                partition_cell_id=template.partition_cell_id,
                system=template.system,
            )
            for template in plan.templates
        ),
    )


def canonical_replayable_compiled_plan_bytes(
    plan: CompiledPolyhedralMotifQueryPlan | ReplayableCompiledPolyhedralPlan,
) -> bytes:
    """Return unique compact UTF-8 bytes for a compiler-template record."""

    replayable = build_replayable_compiled_plan(plan) if isinstance(plan, CompiledPolyhedralMotifQueryPlan) else plan
    if not isinstance(replayable, ReplayableCompiledPolyhedralPlan):
        raise TypeError("plan must be a compiled plan or ReplayableCompiledPolyhedralPlan")
    return json.dumps(
        _plan_object(replayable),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def replayable_compiled_plan_artifact(
    plan: CompiledPolyhedralMotifQueryPlan,
    *,
    artifact_id: str | None = None,
) -> ArtifactReference:
    """Create a content-addressed strict plan artifact for future proof replay."""

    raw = canonical_replayable_compiled_plan_bytes(plan)
    return ArtifactReference.from_payload(
        artifact_id or f"replayable-compiled-plan:{plan.plan_digest}",
        raw,
        media_type="application/json",
    )


def _parse_template(value: Any, index: int) -> ReplayableCompiledPlanTemplate:
    name = f"templates[{index}]"
    mapping = _expect_exact_keys(
        value,
        {"motif", "partition_cell_id", "query_id", "role", "system"},
        name,
    )
    role = _parse_role(mapping["role"], f"{name}.role")
    motif_raw = mapping["motif"]
    motif = None if motif_raw is None else _expect_string(motif_raw, f"{name}.motif", nonempty=True)
    return ReplayableCompiledPlanTemplate(
        query_id=_expect_string(mapping["query_id"], f"{name}.query_id", nonempty=True),
        role=role,
        motif=motif,
        partition_cell_id=_expect_string(
            mapping["partition_cell_id"],
            f"{name}.partition_cell_id",
            nonempty=True,
        ),
        system=_parse_system(mapping["system"], f"{name}.system"),
    )


def parse_canonical_replayable_compiled_plan(
    payload: str | bytes,
    *,
    expected_digest: str | None = None,
    expected_plan_digest: str | None = None,
    expected_partition_digest: str | None = None,
) -> ReplayableCompiledPlanDocument:
    """Strictly parse one canonical compiler plan artifact and check its context."""

    text, raw = _decode_payload(payload)
    try:
        decoded = json.loads(
            text,
            object_pairs_hook=_duplicate_key_rejecting_object,
            parse_constant=_reject_nonfinite_json_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("replayable compiler plan payload is not valid JSON") from error
    root = _expect_exact_keys(
        decoded,
        {"format_version", "partition_digest", "plan_digest", "query_prefix", "templates"},
        "replayable_compiled_plan",
    )
    if _expect_string(root["format_version"], "format_version", nonempty=True) != REPLAYABLE_COMPILED_PLAN_ARTIFACT_FORMAT:
        raise ValueError("unsupported replayable compiled plan format")
    if not isinstance(root["templates"], list):
        raise ValueError("templates must be a JSON array")
    plan = ReplayableCompiledPolyhedralPlan(
        plan_digest=_expect_string(root["plan_digest"], "plan_digest", nonempty=True),
        partition_digest=_expect_string(root["partition_digest"], "partition_digest", nonempty=True),
        query_prefix=_expect_string(root["query_prefix"], "query_prefix", nonempty=True),
        templates=tuple(_parse_template(item, index) for index, item in enumerate(root["templates"])),
    )
    canonical = canonical_replayable_compiled_plan_bytes(plan)
    if raw != canonical:
        raise ValueError("replayable compiler plan JSON is valid but not strict canonical JSON")
    digest = sha256(canonical).hexdigest()
    if expected_digest is not None:
        _require_digest(expected_digest, "expected_digest")
        if digest != expected_digest:
            raise ValueError("replayable compiler plan digest does not match expected_digest")
    if expected_plan_digest is not None and plan.plan_digest != expected_plan_digest:
        raise ValueError("replayable compiler plan digest field does not match the expected plan")
    if expected_partition_digest is not None and plan.partition_digest != expected_partition_digest:
        raise ValueError("replayable compiler plan partition digest does not match the expected partition")
    return ReplayableCompiledPlanDocument(plan=plan, canonical_bytes=canonical, canonical_digest=digest)


def same_replayable_linear_system(left: RationalLinearSystem, right: RationalLinearSystem) -> bool:
    """Compare plan/query systems modulo non-semantic prose labels and row order."""

    def signature(inequality: LinearInequality) -> tuple[tuple[object, ...], object]:
        return inequality.coefficients, inequality.bound

    return (
        left.variables == right.variables
        and Counter(signature(row) for row in left.inequalities)
        == Counter(signature(row) for row in right.inequalities)
    )
