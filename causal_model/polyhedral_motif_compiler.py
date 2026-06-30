"""Proof-carrying compilation of Boolean motifs over finite polyhedral unions.

The ordinary exact-linear backend verifies a user-supplied ``nonempty``,
``active``, and ``inactive`` system, but it cannot know whether the last two
really encode a Boolean motif and its complement.  This module removes that
manual gap for a restricted declared universe:

    Theta = union_{j=1}^J U_j,

where every ``U_j`` is a rational polyhedron with one Boolean tag for every
motif.  A motif is true on the union of true-tagged cells and false on the union
of false-tagged cells.  Any two cells that assign different values to a motif
must carry an exact Farkas proof that they do not overlap.  Therefore the tags
define an unambiguous Boolean predicate on the declared union.

For a retained polyhedron ``C``, the compiler generates only branch systems
``C ∩ U_j``.  It then aggregates exact branch SAT/UNSAT certificates:

* nonempty: union over every declared cell;
* active: union over cells tagged true for the motif; and
* inactive: union over cells tagged false for the motif.

Finite-union aggregation is exact: a union is empty iff every branch is UNSAT,
and is non-empty if any branch is SAT.  The compiler never accepts hand-written
active/inactive systems.  It supports rational, non-strict, conjunction-only
linear cells; a finite union is represented by a finite family of such queries,
not falsely collapsed into one conjunction.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Mapping

from .admissibility import CoverageMode
from .certificate_manifest import ArtifactReference, QueryRole, canonical_json, sha256_digest
from .linear_proof_verifier import (
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    RationalLinearSystem,
    verify_linear_query,
)
from .symbolic_candidate_sets import (
    FeasibilityCertificate,
    FeasibilityStatus,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    SymbolicMotifQueries,
)


POLYHEDRAL_MOTIF_PARTITION_FORMAT = "rach-polyhedral-motif-partition/v1"
POLYHEDRAL_MOTIF_QUERY_PLAN_FORMAT = "rach-polyhedral-motif-query-plan/v1"
POLYHEDRAL_MOTIF_COMPILER = "proof-carrying-polyhedral-motif-compiler"


def _require_nonempty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")


def _row_signature(inequality: LinearInequality) -> tuple[tuple[object, ...], object]:
    return inequality.coefficients, inequality.bound


def _same_linear_system(left: RationalLinearSystem, right: RationalLinearSystem) -> bool:
    return (
        left.variables == right.variables
        and Counter(_row_signature(row) for row in left.inequalities)
        == Counter(_row_signature(row) for row in right.inequalities)
    )


def conjoin_linear_systems(
    left: RationalLinearSystem,
    right: RationalLinearSystem,
    *,
    description: str = "",
) -> RationalLinearSystem:
    """Return the exact conjunction of two systems with one ordered vocabulary."""

    if left.variables != right.variables:
        raise ValueError("linear systems can be conjoined only with identical ordered variables")
    return RationalLinearSystem(
        variables=left.variables,
        inequalities=(*left.inequalities, *right.inequalities),
        description=description or f"({left.description}) AND ({right.description})",
    )


def _system_payload(system: RationalLinearSystem) -> dict[str, object]:
    """Canonical mathematical payload; prose labels/descriptions are intentionally omitted."""

    return {
        "variables": list(system.variables),
        "inequalities": [
            {
                "coefficients": [str(value) for value in inequality.coefficients],
                "bound": str(inequality.bound),
            }
            for inequality in system.inequalities
        ],
    }


def _proof_payload(proof: LinearFeasibilityProof) -> dict[str, object]:
    return {
        "status": proof.status.value,
        "evidence_reference": proof.evidence_reference,
        "producer": proof.producer,
        "witness": None if proof.witness is None else [str(value) for value in proof.witness.values],
        "farkas_multipliers": (
            None if proof.farkas is None else [str(value) for value in proof.farkas.multipliers]
        ),
    }


@dataclass(frozen=True)
class TaggedPolyhedralCell:
    """One rational polyhedral region with a declared Boolean value per motif."""

    cell_id: str
    system: RationalLinearSystem
    motif_values: Mapping[str, bool]
    description: str = ""

    def __post_init__(self) -> None:
        _require_nonempty(self.cell_id, "cell_id")
        if not self.motif_values:
            raise ValueError("a tagged polyhedral cell needs at least one motif value")
        if any(not isinstance(motif, str) or not motif for motif in self.motif_values):
            raise ValueError("motif value keys must be non-empty strings")
        if any(not isinstance(value, bool) for value in self.motif_values.values()):
            raise ValueError("every tagged polyhedral motif value must be Boolean")


@dataclass(frozen=True)
class ConflictingCellOverlapProof:
    """Exact UNSAT proof that two differently tagged cells have empty overlap."""

    left_cell_id: str
    right_cell_id: str
    overlap_query: LinearFeasibilityQuery

    def __post_init__(self) -> None:
        _require_nonempty(self.left_cell_id, "left_cell_id")
        _require_nonempty(self.right_cell_id, "right_cell_id")
        if self.left_cell_id >= self.right_cell_id:
            raise ValueError("conflicting overlap proof cell IDs must be stored in increasing order")


@dataclass(frozen=True)
class PolyhedralMotifPartition:
    """A finite union of tagged rational polyhedra defining the declared universe.

    Exhaustiveness is definitional: the candidate universe of this object is the
    union of its listed cells, rather than an unverified claim that the cells
    cover a larger ambient Euclidean space.  Exact conflict-separation proofs
    ensure the Boolean tags are single-valued on that declared union.
    """

    space: SymbolicCandidateSpace
    cells: tuple[TaggedPolyhedralCell, ...]
    conflicting_overlap_proofs: tuple[ConflictingCellOverlapProof, ...] = ()

    def __post_init__(self) -> None:
        if not self.cells:
            raise ValueError("a polyhedral motif partition needs at least one cell")
        cell_ids = tuple(cell.cell_id for cell in self.cells)
        if len(set(cell_ids)) != len(cell_ids):
            raise ValueError("polyhedral partition cell IDs must be unique")
        expected_motifs = set(self.space.motifs)
        variables = self.cells[0].system.variables
        for cell in self.cells:
            if set(cell.motif_values) != expected_motifs:
                raise ValueError("every polyhedral cell must tag exactly the declared motifs")
            if cell.system.variables != variables:
                raise ValueError("every polyhedral partition cell must use one ordered variable vocabulary")


@dataclass(frozen=True)
class VerifiedPolyhedralMotifPartition:
    """A partition whose tag conflicts have been eliminated by exact proofs."""

    partition: PolyhedralMotifPartition
    partition_digest: str
    verified_conflicting_pairs: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class CompiledLinearQueryTemplate:
    """One compiler-generated branch system with no caller-controlled constraints."""

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
                raise ValueError("a nonempty compiled template must not name one motif")
        elif not self.motif:
            raise ValueError("an active/inactive compiled template must name one motif")


@dataclass(frozen=True)
class CompiledPolyhedralMotifQueryPlan:
    """All branch templates generated from one verified partition and retained system."""

    verified_partition: VerifiedPolyhedralMotifPartition
    retained_system: RationalLinearSystem
    query_prefix: str
    nonempty_templates: tuple[CompiledLinearQueryTemplate, ...]
    active_templates: Mapping[str, tuple[CompiledLinearQueryTemplate, ...]]
    inactive_templates: Mapping[str, tuple[CompiledLinearQueryTemplate, ...]]
    plan_digest: str

    def __post_init__(self) -> None:
        _require_nonempty(self.query_prefix, "query_prefix")
        if self.retained_system.variables != self.verified_partition.partition.cells[0].system.variables:
            raise ValueError("retained system variables must match the verified partition vocabulary")
        motifs = set(self.verified_partition.partition.space.motifs)
        if set(self.active_templates) != motifs or set(self.inactive_templates) != motifs:
            raise ValueError("compiled plan must contain active and inactive branches for every motif")
        if not self.nonempty_templates:
            raise ValueError("compiled plan must contain one nonempty branch per partition cell")

    @property
    def templates(self) -> tuple[CompiledLinearQueryTemplate, ...]:
        ordered: list[CompiledLinearQueryTemplate] = list(self.nonempty_templates)
        for motif in self.verified_partition.partition.space.motifs:
            ordered.extend(self.active_templates[motif])
            ordered.extend(self.inactive_templates[motif])
        return tuple(ordered)


@dataclass(frozen=True)
class BoundCompiledPolyhedralMotifProofs:
    """Externally supplied exact proofs bound to compiler-generated templates."""

    plan: CompiledPolyhedralMotifQueryPlan
    queries_by_id: Mapping[str, LinearFeasibilityQuery]

    def __post_init__(self) -> None:
        expected = {template.query_id for template in self.plan.templates}
        if set(self.queries_by_id) != expected:
            raise ValueError("bound compiled proofs must contain exactly every compiler-generated query ID")
        templates = {template.query_id: template for template in self.plan.templates}
        for query_id, query in self.queries_by_id.items():
            template = templates[query_id]
            if query.query_id != query_id:
                raise ValueError("bound compiled proof query ID does not match its template")
            if not _same_linear_system(query.system, template.system):
                raise ValueError("bound compiled proof system does not match the compiler-generated system")


@dataclass(frozen=True)
class VerifiedCompiledPolyhedralMotifQueries:
    """Exact branch verification plus aggregate RACH queries for every motif."""

    bound_proofs: BoundCompiledPolyhedralMotifProofs
    branch_certificates: Mapping[str, FeasibilityCertificate]
    motif_queries: Mapping[str, SymbolicMotifQueries]



def _ordered_cells(partition: PolyhedralMotifPartition) -> tuple[TaggedPolyhedralCell, ...]:
    return tuple(sorted(partition.cells, key=lambda cell: cell.cell_id))


def _pair_key(left_cell_id: str, right_cell_id: str) -> tuple[str, str]:
    return (left_cell_id, right_cell_id) if left_cell_id < right_cell_id else (right_cell_id, left_cell_id)


def _conflicting_pairs(partition: PolyhedralMotifPartition) -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = []
    for left, right in combinations(_ordered_cells(partition), 2):
        if any(left.motif_values[motif] != right.motif_values[motif] for motif in partition.space.motifs):
            pairs.append((left.cell_id, right.cell_id))
    return tuple(pairs)


def _partition_payload(partition: PolyhedralMotifPartition) -> dict[str, object]:
    cells = _ordered_cells(partition)
    proofs = sorted(
        partition.conflicting_overlap_proofs,
        key=lambda proof: (proof.left_cell_id, proof.right_cell_id),
    )
    return {
        "format_version": POLYHEDRAL_MOTIF_PARTITION_FORMAT,
        "candidate_space_description": partition.space.space_description,
        "motifs": list(partition.space.motifs),
        "cells": [
            {
                "cell_id": cell.cell_id,
                "system": _system_payload(cell.system),
                "motif_values": {
                    motif: cell.motif_values[motif]
                    for motif in partition.space.motifs
                },
            }
            for cell in cells
        ],
        "conflicting_overlap_proofs": [
            {
                "left_cell_id": proof.left_cell_id,
                "right_cell_id": proof.right_cell_id,
                "query_id": proof.overlap_query.query_id,
                "system": _system_payload(proof.overlap_query.system),
                "proof": _proof_payload(proof.overlap_query.proof),
            }
            for proof in proofs
        ],
    }


def polyhedral_motif_partition_payload(
    verified_partition: VerifiedPolyhedralMotifPartition,
) -> bytes:
    """Return canonical bytes committing the tagged cells and separation proofs."""

    return canonical_json(_partition_payload(verified_partition.partition)).encode("utf-8")


def polyhedral_motif_partition_artifact(
    verified_partition: VerifiedPolyhedralMotifPartition,
    *,
    artifact_id: str = "polyhedral-motif-partition",
) -> ArtifactReference:
    """Create a content-addressed manifest artifact for verified motif semantics."""

    return ArtifactReference.from_payload(
        artifact_id,
        polyhedral_motif_partition_payload(verified_partition),
        media_type="application/json",
    )


def verify_polyhedral_motif_partition(
    partition: PolyhedralMotifPartition,
) -> VerifiedPolyhedralMotifPartition:
    """Verify that differently tagged cells cannot overlap under exact arithmetic.

    Because the candidate universe is the union of the listed cells, no separate
    ambient-space coverage proof is needed for Boolean totality.  The only
    nontrivial semantic condition is consistency on overlaps: any point that can
    lie in more than one listed cell must receive identical motif values.
    """

    cells_by_id = {cell.cell_id: cell for cell in partition.cells}
    expected_pairs = set(_conflicting_pairs(partition))
    provided_pairs = {
        _pair_key(proof.left_cell_id, proof.right_cell_id)
        for proof in partition.conflicting_overlap_proofs
    }
    if provided_pairs != expected_pairs:
        raise ValueError("partition needs exactly one overlap-UNSAT proof for every conflicting cell pair")
    if len(provided_pairs) != len(partition.conflicting_overlap_proofs):
        raise ValueError("partition overlap proofs must not duplicate a cell pair")

    for proof in partition.conflicting_overlap_proofs:
        left = cells_by_id.get(proof.left_cell_id)
        right = cells_by_id.get(proof.right_cell_id)
        if left is None or right is None:
            raise ValueError("partition overlap proof references an unknown cell")
        expected_system = conjoin_linear_systems(
            left.system,
            right.system,
            description=f"overlap of {left.cell_id} and {right.cell_id}",
        )
        if not _same_linear_system(proof.overlap_query.system, expected_system):
            raise ValueError("partition overlap proof system is not the conjunction of its two cells")
        certificate = verify_linear_query(proof.overlap_query)
        if certificate.status is not FeasibilityStatus.UNSAT:
            raise ValueError("partition overlap proof must be exact UNSAT")

    digest = sha256_digest(canonical_json(_partition_payload(partition)))
    return VerifiedPolyhedralMotifPartition(
        partition=partition,
        partition_digest=digest,
        verified_conflicting_pairs=tuple(sorted(expected_pairs)),
    )


def _template_id(
    prefix: str,
    role: QueryRole,
    motif: str | None,
    partition_cell_id: str,
) -> str:
    motif_part = "all" if motif is None else motif
    return f"{prefix}/{role.value}/{motif_part}/{partition_cell_id}"


def _plan_payload(
    verified_partition: VerifiedPolyhedralMotifPartition,
    retained_system: RationalLinearSystem,
    query_prefix: str,
    templates: Iterable[CompiledLinearQueryTemplate],
) -> dict[str, object]:
    return {
        "format_version": POLYHEDRAL_MOTIF_QUERY_PLAN_FORMAT,
        "partition_digest": verified_partition.partition_digest,
        "retained_system": _system_payload(retained_system),
        "query_prefix": query_prefix,
        "templates": [
            {
                "query_id": template.query_id,
                "role": template.role.value,
                "motif": template.motif,
                "partition_cell_id": template.partition_cell_id,
                "system": _system_payload(template.system),
            }
            for template in sorted(templates, key=lambda item: item.query_id)
        ],
    }


def compile_polyhedral_motif_query_plan(
    verified_partition: VerifiedPolyhedralMotifPartition,
    *,
    retained_system: RationalLinearSystem,
    query_prefix: str,
) -> CompiledPolyhedralMotifQueryPlan:
    """Compile exact nonempty/active/inactive branch systems from cell tags only."""

    _require_nonempty(query_prefix, "query_prefix")
    partition = verified_partition.partition
    cells = _ordered_cells(partition)
    if retained_system.variables != cells[0].system.variables:
        raise ValueError("retained system variables must match the partition vocabulary")

    nonempty_templates: list[CompiledLinearQueryTemplate] = []
    active_templates: dict[str, list[CompiledLinearQueryTemplate]] = {
        motif: [] for motif in partition.space.motifs
    }
    inactive_templates: dict[str, list[CompiledLinearQueryTemplate]] = {
        motif: [] for motif in partition.space.motifs
    }

    for cell in cells:
        branch_system = conjoin_linear_systems(
            retained_system,
            cell.system,
            description=f"retained system intersect partition cell {cell.cell_id}",
        )
        nonempty_templates.append(
            CompiledLinearQueryTemplate(
                query_id=_template_id(query_prefix, QueryRole.NONEMPTY, None, cell.cell_id),
                role=QueryRole.NONEMPTY,
                motif=None,
                partition_cell_id=cell.cell_id,
                system=branch_system,
            )
        )
        for motif in partition.space.motifs:
            role = QueryRole.ACTIVE if cell.motif_values[motif] else QueryRole.INACTIVE
            template = CompiledLinearQueryTemplate(
                query_id=_template_id(query_prefix, role, motif, cell.cell_id),
                role=role,
                motif=motif,
                partition_cell_id=cell.cell_id,
                system=branch_system,
            )
            (active_templates if role is QueryRole.ACTIVE else inactive_templates)[motif].append(template)

    flat_templates = (
        *nonempty_templates,
        *(template for motif in partition.space.motifs for template in active_templates[motif]),
        *(template for motif in partition.space.motifs for template in inactive_templates[motif]),
    )
    digest = sha256_digest(
        canonical_json(_plan_payload(verified_partition, retained_system, query_prefix, flat_templates))
    )
    return CompiledPolyhedralMotifQueryPlan(
        verified_partition=verified_partition,
        retained_system=retained_system,
        query_prefix=query_prefix,
        nonempty_templates=tuple(nonempty_templates),
        active_templates={motif: tuple(active_templates[motif]) for motif in partition.space.motifs},
        inactive_templates={motif: tuple(inactive_templates[motif]) for motif in partition.space.motifs},
        plan_digest=digest,
    )


def compiled_polyhedral_motif_plan_payload(plan: CompiledPolyhedralMotifQueryPlan) -> bytes:
    """Return canonical bytes for a manifest-bound compiler query-encoding artifact."""

    payload = _plan_payload(
        plan.verified_partition,
        plan.retained_system,
        plan.query_prefix,
        plan.templates,
    )
    return canonical_json(payload).encode("utf-8")


def compiled_polyhedral_motif_plan_artifact(
    plan: CompiledPolyhedralMotifQueryPlan,
    *,
    artifact_id: str = "compiled-polyhedral-motif-query-plan",
) -> ArtifactReference:
    """Create a content-addressed artifact binding every compiler-generated query."""

    return ArtifactReference.from_payload(
        artifact_id,
        compiled_polyhedral_motif_plan_payload(plan),
        media_type="application/json",
    )


def bind_compiled_polyhedral_motif_proofs(
    plan: CompiledPolyhedralMotifQueryPlan,
    *,
    proofs_by_query_id: Mapping[str, LinearFeasibilityProof],
) -> BoundCompiledPolyhedralMotifProofs:
    """Bind external proofs to immutable compiler templates without accepting systems.

    The caller supplies only one ``LinearFeasibilityProof`` per generated query
    ID.  The system and query ID are reconstructed from the plan, preventing an
    external backend from changing active/inactive semantics while attaching a
    mathematically valid proof to a different system.
    """

    templates = {template.query_id: template for template in plan.templates}
    if set(proofs_by_query_id) != set(templates):
        raise ValueError("proofs_by_query_id must contain exactly every compiler-generated query ID")
    queries = {
        query_id: LinearFeasibilityQuery(
            query_id=query_id,
            system=template.system,
            proof=proofs_by_query_id[query_id],
            assumptions=(
                "query system was generated by the proof-carrying polyhedral motif compiler",
                f"compiled plan digest: {plan.plan_digest}",
                f"verified partition digest: {plan.verified_partition.partition_digest}",
            ),
        )
        for query_id, template in templates.items()
    }
    return BoundCompiledPolyhedralMotifProofs(plan=plan, queries_by_id=queries)


def _aggregate_union_certificates(
    *,
    plan: CompiledPolyhedralMotifQueryPlan,
    role: QueryRole,
    motif: str | None,
    templates: tuple[CompiledLinearQueryTemplate, ...],
    branch_certificates: Mapping[str, FeasibilityCertificate],
) -> FeasibilityCertificate:
    """Aggregate exact branch results for one finite union of polyhedra."""

    motif_part = "all" if motif is None else motif
    description = f"{plan.query_prefix}/union/{role.value}/{motif_part}"
    common_assumptions = (
        "the declared candidate universe is the verified finite union of tagged polyhedral cells",
        "compiler branch systems are retained-system intersections with exactly those cells",
        f"compiled plan digest: {plan.plan_digest}",
        f"verified partition digest: {plan.verified_partition.partition_digest}",
    )
    if not templates:
        return FeasibilityCertificate(
            query_description=description,
            status=FeasibilityStatus.UNSAT,
            evidence_reference=f"compiler-empty-tag-family:{plan.verified_partition.partition_digest}",
            solver=POLYHEDRAL_MOTIF_COMPILER,
            assumptions=(
                *common_assumptions,
                "the finite union has no tagged branches and is empty by construction",
            ),
        )

    certificates = [branch_certificates[template.query_id] for template in templates]
    sat = next((certificate for certificate in certificates if certificate.status is FeasibilityStatus.SAT), None)
    if sat is not None:
        return FeasibilityCertificate(
            query_description=description,
            status=FeasibilityStatus.SAT,
            evidence_reference=sat.evidence_reference,
            solver=POLYHEDRAL_MOTIF_COMPILER,
            assumptions=(
                *common_assumptions,
                "a finite union is non-empty because one exact branch witness is feasible",
                *sat.assumptions,
            ),
        )
    if all(certificate.status is FeasibilityStatus.UNSAT for certificate in certificates):
        return FeasibilityCertificate(
            query_description=description,
            status=FeasibilityStatus.UNSAT,
            evidence_reference="; ".join(certificate.evidence_reference for certificate in certificates),
            solver=POLYHEDRAL_MOTIF_COMPILER,
            assumptions=(
                *common_assumptions,
                "a finite union is empty because every exact branch is infeasible",
                *(assumption for certificate in certificates for assumption in certificate.assumptions),
            ),
        )
    return FeasibilityCertificate(
        query_description=description,
        status=FeasibilityStatus.UNKNOWN,
        solver=POLYHEDRAL_MOTIF_COMPILER,
        assumptions=(
            *common_assumptions,
            "no branch witness exists and at least one branch remains unknown",
        ),
    )


def verify_compiled_polyhedral_motif_proofs(
    bound_proofs: BoundCompiledPolyhedralMotifProofs,
) -> VerifiedCompiledPolyhedralMotifQueries:
    """Verify all branch proofs and derive semantic Boolean motif query triples."""

    plan = bound_proofs.plan
    branch_certificates = {
        query_id: verify_linear_query(query)
        for query_id, query in bound_proofs.queries_by_id.items()
    }
    nonempty = _aggregate_union_certificates(
        plan=plan,
        role=QueryRole.NONEMPTY,
        motif=None,
        templates=plan.nonempty_templates,
        branch_certificates=branch_certificates,
    )
    motif_queries = {
        motif: SymbolicMotifQueries(
            nonempty=nonempty,
            active=_aggregate_union_certificates(
                plan=plan,
                role=QueryRole.ACTIVE,
                motif=motif,
                templates=plan.active_templates[motif],
                branch_certificates=branch_certificates,
            ),
            inactive=_aggregate_union_certificates(
                plan=plan,
                role=QueryRole.INACTIVE,
                motif=motif,
                templates=plan.inactive_templates[motif],
                branch_certificates=branch_certificates,
            ),
        )
        for motif in plan.verified_partition.partition.space.motifs
    }
    return VerifiedCompiledPolyhedralMotifQueries(
        bound_proofs=bound_proofs,
        branch_certificates=branch_certificates,
        motif_queries=motif_queries,
    )


def compiled_polyhedral_motif_symbolic_cell(
    verified_queries: VerifiedCompiledPolyhedralMotifQueries,
    *,
    cell_id: str,
    description: str,
    required: bool = True,
    coverage_mode: CoverageMode = CoverageMode.SOLVER_BACKED,
) -> SymbolicConfidenceSetCell:
    """Convert compiler-derived semantic queries into one ordinary RACH cell."""

    return SymbolicConfidenceSetCell(
        cell_id=cell_id,
        description=description,
        motif_queries=verified_queries.motif_queries,
        required=required,
        coverage_mode=coverage_mode,
    )


def _role_templates(
    plan: CompiledPolyhedralMotifQueryPlan,
    *,
    motif: str,
    role: QueryRole,
) -> tuple[CompiledLinearQueryTemplate, ...]:
    if motif not in plan.verified_partition.partition.space.motifs:
        raise ValueError("role proof bundle motif is absent from the compiled plan")
    if role is QueryRole.NONEMPTY:
        return plan.nonempty_templates
    if role is QueryRole.ACTIVE:
        return plan.active_templates[motif]
    if role is QueryRole.INACTIVE:
        return plan.inactive_templates[motif]
    raise ValueError("unsupported compiled motif query role")


def compiled_role_proof_bundle_payload(
    verified_queries: VerifiedCompiledPolyhedralMotifQueries,
    *,
    motif: str,
    role: QueryRole,
) -> bytes:
    """Canonical artifact bytes for all exact branch proofs used by one motif role.

    Existing manifest bindings have one ``(look, cell, motif, role)`` slot.  A
    compiler role may contain several union branches, so this payload binds the
    complete branch family inside that one existing manifest artifact slot.
    """

    bound = verified_queries.bound_proofs
    templates = _role_templates(bound.plan, motif=motif, role=role)
    payload = {
        "format_version": POLYHEDRAL_MOTIF_QUERY_PLAN_FORMAT,
        "plan_digest": bound.plan.plan_digest,
        "motif": motif,
        "role": role.value,
        "branches": [
            {
                "query_id": template.query_id,
                "partition_cell_id": template.partition_cell_id,
                "system": _system_payload(template.system),
                "proof": _proof_payload(bound.queries_by_id[template.query_id].proof),
            }
            for template in templates
        ],
    }
    return canonical_json(payload).encode("utf-8")


def compiled_role_proof_bundle_artifact(
    verified_queries: VerifiedCompiledPolyhedralMotifQueries,
    *,
    motif: str,
    role: QueryRole,
    artifact_id: str | None = None,
) -> ArtifactReference:
    """Create one manifest-bindable artifact for every compiled motif role family."""

    identifier = artifact_id or f"compiled-proof-bundle:{motif}:{role.value}"
    return ArtifactReference.from_payload(
        identifier,
        compiled_role_proof_bundle_payload(verified_queries, motif=motif, role=role),
        media_type="application/json",
    )
