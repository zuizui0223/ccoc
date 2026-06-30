"""Replayable exact branch-family artifacts for compiled polyhedral motif roles.

``replayable_exact_linear_proofs`` can replay a finite family of exact rational
queries.  This adapter ties such a family back to the proof-carrying polyhedral
motif compiler: the replayed query IDs and systems must be exactly those emitted
by one fixed compiled plan for one ``(motif, role)`` pair.

The division of responsibility is intentional:

* exact proof replay verifies SAT witnesses / Farkas UNSAT certificates; and
* this adapter verifies that those replayed systems are the compiler's branch
  systems for the declared plan, partition, motif, and role.

Together they remove both opaque-proof and query-substitution gaps for new
compiler role artifacts.  Existing historical artifacts are not reinterpreted.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Mapping

from .certificate_manifest import ArtifactReference, QueryRole
from .linear_proof_verifier import LinearFeasibilityQuery, LinearInequality, RationalLinearSystem
from .polyhedral_motif_compiler import (
    CompiledLinearQueryTemplate,
    CompiledPolyhedralMotifQueryPlan,
    VerifiedCompiledPolyhedralMotifQueries,
)
from .replayable_exact_linear_proofs import (
    ExactLinearProofBundle,
    ReplayableExactLinearBundleDocument,
    exact_linear_bundle_artifact,
    canonical_exact_linear_bundle_bytes,
    replay_exact_linear_bundle,
)
from .symbolic_candidate_sets import FeasibilityStatus


REPLAYABLE_COMPILED_ROLE_ARTIFACT_FORMAT = "rach-replayable-compiled-role-proof/v1"


def _row_signature(inequality: LinearInequality) -> tuple[tuple[object, ...], object]:
    return inequality.coefficients, inequality.bound


def _same_linear_system(left: RationalLinearSystem, right: RationalLinearSystem) -> bool:
    return (
        left.variables == right.variables
        and Counter(_row_signature(row) for row in left.inequalities)
        == Counter(_row_signature(row) for row in right.inequalities)
    )


def _role_templates(
    plan: CompiledPolyhedralMotifQueryPlan,
    *,
    motif: str,
    role: QueryRole,
) -> tuple[CompiledLinearQueryTemplate, ...]:
    if motif not in plan.verified_partition.partition.space.motifs:
        raise ValueError("replayable compiled role motif is absent from the plan")
    if role is QueryRole.NONEMPTY:
        return plan.nonempty_templates
    if role is QueryRole.ACTIVE:
        return plan.active_templates[motif]
    if role is QueryRole.INACTIVE:
        return plan.inactive_templates[motif]
    raise ValueError("unsupported replayable compiled role")


def _aggregate_status(
    verified_queries: VerifiedCompiledPolyhedralMotifQueries,
    *,
    motif: str,
    role: QueryRole,
) -> FeasibilityStatus:
    queries = verified_queries.motif_queries[motif]
    if role is QueryRole.NONEMPTY:
        return queries.nonempty.status
    if role is QueryRole.ACTIVE:
        return queries.active.status
    if role is QueryRole.INACTIVE:
        return queries.inactive.status
    raise ValueError("unsupported replayable compiled role")


@dataclass(frozen=True)
class ReplayableCompiledRoleProof:
    """A replayed bundle proven to match one compiler plan/motif/role family."""

    document: ReplayableExactLinearBundleDocument
    plan_digest: str
    partition_digest: str
    motif: str
    role: QueryRole


def build_replayable_compiled_role_bundle(
    verified_queries: VerifiedCompiledPolyhedralMotifQueries,
    *,
    motif: str,
    role: QueryRole,
) -> ExactLinearProofBundle:
    """Build a replayable exact bundle directly from compiler-bound queries only."""

    bound = verified_queries.bound_proofs
    plan = bound.plan
    templates = _role_templates(plan, motif=motif, role=role)
    branches = tuple(bound.queries_by_id[template.query_id] for template in templates)
    return ExactLinearProofBundle(
        bundle_id=(
            f"compiled-role:{plan.plan_digest}:{plan.verified_partition.partition_digest}:"
            f"{motif}:{role.value}"
        ),
        plan_digest=plan.plan_digest,
        partition_digest=plan.verified_partition.partition_digest,
        motif=motif,
        role=role,
        branches=branches,
        aggregate_status=_aggregate_status(verified_queries, motif=motif, role=role),
    )


def replayable_compiled_role_proof_bundle_payload(
    verified_queries: VerifiedCompiledPolyhedralMotifQueries,
    *,
    motif: str,
    role: QueryRole,
) -> bytes:
    """Return strict canonical replayable bytes for one compiler-generated role family."""

    return canonical_exact_linear_bundle_bytes(
        build_replayable_compiled_role_bundle(verified_queries, motif=motif, role=role)
    )


def replayable_compiled_role_proof_bundle_artifact(
    verified_queries: VerifiedCompiledPolyhedralMotifQueries,
    *,
    motif: str,
    role: QueryRole,
    artifact_id: str | None = None,
) -> ArtifactReference:
    """Create a manifest-bindable proof artifact that can be independently replayed."""

    bundle = build_replayable_compiled_role_bundle(verified_queries, motif=motif, role=role)
    identifier = artifact_id or f"replayable-compiled-proof:{motif}:{role.value}"
    return exact_linear_bundle_artifact(bundle, artifact_id=identifier)


def replay_compiled_role_proof_bundle(
    payload: str | bytes,
    *,
    plan: CompiledPolyhedralMotifQueryPlan,
    motif: str,
    role: QueryRole,
    expected_digest: str | None = None,
) -> ReplayableCompiledRoleProof:
    """Replay exact proofs and prove the branch family matches the compiler templates."""

    document = replay_exact_linear_bundle(
        payload,
        expected_digest=expected_digest,
        expected_plan_digest=plan.plan_digest,
        expected_partition_digest=plan.verified_partition.partition_digest,
        expected_motif=motif,
        expected_role=role,
    )
    expected_templates = _role_templates(plan, motif=motif, role=role)
    expected_by_id: Mapping[str, CompiledLinearQueryTemplate] = {
        template.query_id: template for template in expected_templates
    }
    actual_by_id: Mapping[str, LinearFeasibilityQuery] = {
        query.query_id: query for query in document.bundle.branches
    }
    if set(actual_by_id) != set(expected_by_id):
        raise ValueError("replayed compiler role bundle query IDs do not match compiler templates")
    for query_id, template in expected_by_id.items():
        if not _same_linear_system(actual_by_id[query_id].system, template.system):
            raise ValueError("replayed compiler role bundle system differs from compiler template")
    return ReplayableCompiledRoleProof(
        document=document,
        plan_digest=plan.plan_digest,
        partition_digest=plan.verified_partition.partition_digest,
        motif=motif,
        role=role,
    )
