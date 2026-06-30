"""Tier-aware certificate manifests for compiler-admitted RACH evidence.

Manifest v1 binds solver proof artifacts by ``(look, cell, motif, role)``.  That
key is sufficient for one retained set, but it cannot distinguish the inner and
outer compiler-generated query families used by an outer-envelope stability
audit.  This module defines a separate, non-breaking v2 contract:

    (tier, look, cell, motif, role)

where ``tier`` is ``inner`` or ``outer``.  A v2 manifest also binds one compiled
query-plan artifact per ``(tier, look, cell)`` and one fixed semantic-partition
artifact.  Every proof binding must point to the exact plan artifact for its
tier/look/cell; this prevents a valid proof family from being transplanted to a
plan for another tier.

The v1 dataclasses and canonical byte format remain unchanged.  A migration API
exists only for an explicitly chosen *single* tier, because a tierless v1 proof
cannot truthfully be inferred to describe both inner and outer query families.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping

from .anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
)
from .certificate_manifest import (
    ArtifactReference,
    CertificateManifest,
    ExternalAssertionBinding,
    ManifestTarget,
    QueryRole,
    _common_scope,
    canonical_json,
    sha256_digest,
)
from .symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace


TIERED_MANIFEST_FORMAT = "rach-certificate-manifest/v2"


class QueryTier(str, Enum):
    """The two retained-set tiers used in exact outer-envelope audits."""

    INNER = "inner"
    OUTER = "outer"


def _require_nonempty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be non-empty")


def _validate_target_and_assertions(
    *,
    target: ManifestTarget,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
    coverage_assertion: ExternalAssertionBinding,
    solver_assertion: ExternalAssertionBinding,
) -> None:
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


@dataclass(frozen=True)
class TieredQueryPlanBinding:
    """One compiler query plan for a fixed tier, look, and required cell."""

    tier: QueryTier
    look: int
    cell_id: str
    query_plan_artifact: ArtifactReference

    def __post_init__(self) -> None:
        if not isinstance(self.tier, QueryTier):
            raise ValueError("query plan tier must be a QueryTier")
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("query plan look must be a positive integer")
        _require_nonempty(self.cell_id, "query plan cell_id")

    @property
    def plan_key(self) -> tuple[QueryTier, int, str]:
        return (self.tier, self.look, self.cell_id)


@dataclass(frozen=True)
class TieredSolverQueryProofBinding:
    """One decisive role-family proof bound to a tier-specific compiled plan."""

    tier: QueryTier
    look: int
    cell_id: str
    motif: str
    role: QueryRole
    status: FeasibilityStatus
    query_plan_artifact: ArtifactReference
    proof_artifact: ArtifactReference
    verifier_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.tier, QueryTier):
            raise ValueError("tiered proof binding tier must be a QueryTier")
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("tiered proof binding look must be a positive integer")
        _require_nonempty(self.cell_id, "tiered proof binding cell_id")
        _require_nonempty(self.motif, "tiered proof binding motif")
        if not isinstance(self.role, QueryRole):
            raise ValueError("tiered proof binding role must be a QueryRole")
        if self.status not in (FeasibilityStatus.SAT, FeasibilityStatus.UNSAT):
            raise ValueError("tiered proof bindings may contain only decisive SAT or UNSAT statuses")
        _require_nonempty(self.verifier_id, "tiered proof binding verifier_id")

    @property
    def query_key(self) -> tuple[QueryTier, int, str, str, QueryRole]:
        return (self.tier, self.look, self.cell_id, self.motif, self.role)

    @property
    def plan_key(self) -> tuple[QueryTier, int, str]:
        return (self.tier, self.look, self.cell_id)


@dataclass(frozen=True)
class TieredCertificateManifest:
    """Manifest v2: target, assertions, partition, tiered plans, and tiered proofs."""

    target: ManifestTarget
    coverage_assertion: ExternalAssertionBinding
    solver_assertion: ExternalAssertionBinding
    semantic_partition_artifact: ArtifactReference
    tiered_query_plans: tuple[TieredQueryPlanBinding, ...] = ()
    solver_query_proofs: tuple[TieredSolverQueryProofBinding, ...] = ()
    format_version: str = TIERED_MANIFEST_FORMAT

    def __post_init__(self) -> None:
        if self.format_version != TIERED_MANIFEST_FORMAT:
            raise ValueError(f"unsupported tiered manifest format: {self.format_version!r}")
        if self.coverage_assertion.kind != "time-uniform-statistical-coverage":
            raise ValueError("coverage_assertion kind must be time-uniform-statistical-coverage")
        if self.solver_assertion.kind != "time-uniform-solver-semantic-validity":
            raise ValueError("solver_assertion kind must be time-uniform-solver-semantic-validity")
        plan_keys = [binding.plan_key for binding in self.tiered_query_plans]
        if len(set(plan_keys)) != len(plan_keys):
            raise ValueError("tiered query plans must be unique per tier/look/cell")
        plans_by_key = {binding.plan_key: binding for binding in self.tiered_query_plans}
        proof_keys = [binding.query_key for binding in self.solver_query_proofs]
        if len(set(proof_keys)) != len(proof_keys):
            raise ValueError("tiered proof bindings must be unique per tier/look/cell/motif/role")
        for plan in self.tiered_query_plans:
            if not self.target.covers_look(plan.look):
                raise ValueError("tiered query plan look lies outside the manifest target scope")
            if plan.cell_id not in self.target.required_cell_ids:
                raise ValueError("tiered query plan cell_id is absent from the manifest target")
        for binding in self.solver_query_proofs:
            if not self.target.covers_look(binding.look):
                raise ValueError("tiered proof binding look lies outside the manifest target scope")
            if binding.cell_id not in self.target.required_cell_ids:
                raise ValueError("tiered proof binding cell_id is absent from the manifest target")
            if binding.motif not in self.target.motifs:
                raise ValueError("tiered proof binding motif is absent from the manifest target")
            matching_plan = plans_by_key.get(binding.plan_key)
            if matching_plan is None:
                raise ValueError("tiered proof binding needs a matching tiered query plan")
            if matching_plan.query_plan_artifact != binding.query_plan_artifact:
                raise ValueError("tiered proof binding query-plan artifact differs from its matching plan")

    @property
    def manifest_digest(self) -> str:
        return sha256_digest(canonical_json(self))

    @property
    def tiered_target_digest(self) -> str:
        """Bind the v1 target plus the fixed semantic partition artifact."""

        return sha256_digest(
            canonical_json(
                {
                    "format_version": self.format_version,
                    "target_digest": self.target.target_digest,
                    "semantic_partition_artifact": self.semantic_partition_artifact,
                }
            )
        )

    def referenced_artifacts(self) -> Mapping[str, ArtifactReference]:
        """Return the complete content-addressed registry, rejecting ID conflicts."""

        artifacts: dict[str, ArtifactReference] = {}
        for artifact in (
            self.target.candidate_space_artifact,
            *self.target.motif_definition_artifacts.values(),
            self.coverage_assertion.evidence_artifact,
            self.solver_assertion.evidence_artifact,
            self.semantic_partition_artifact,
            *(binding.query_plan_artifact for binding in self.tiered_query_plans),
            *(binding.query_plan_artifact for binding in self.solver_query_proofs),
            *(binding.proof_artifact for binding in self.solver_query_proofs),
        ):
            previous = artifacts.get(artifact.artifact_id)
            if previous is not None and previous != artifact:
                raise ValueError("one artifact_id cannot name different digest or media-type commitments")
            artifacts[artifact.artifact_id] = artifact
        return artifacts


@dataclass(frozen=True)
class TieredManifestVerificationReport:
    """Successful v2 theorem-target and artifact-content verification result."""

    manifest_digest: str
    target_digest: str
    tiered_target_digest: str
    verified_artifact_ids: tuple[str, ...]


def build_anytime_tiered_symbolic_manifest(
    *,
    target: ManifestTarget,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
    coverage_assertion: ExternalAssertionBinding,
    solver_assertion: ExternalAssertionBinding,
    semantic_partition_artifact: ArtifactReference,
    tiered_query_plans: Iterable[TieredQueryPlanBinding] = (),
    solver_query_proofs: Iterable[TieredSolverQueryProofBinding] = (),
) -> TieredCertificateManifest:
    """Build a v2 manifest only when target and theorem certificates agree exactly."""

    _validate_target_and_assertions(
        target=target,
        coverage_certificate=coverage_certificate,
        solver_certificate=solver_certificate,
        coverage_assertion=coverage_assertion,
        solver_assertion=solver_assertion,
    )
    return TieredCertificateManifest(
        target=target,
        coverage_assertion=coverage_assertion,
        solver_assertion=solver_assertion,
        semantic_partition_artifact=semantic_partition_artifact,
        tiered_query_plans=tuple(tiered_query_plans),
        solver_query_proofs=tuple(solver_query_proofs),
    )


def verify_tiered_manifest_context(
    manifest: TieredCertificateManifest,
    *,
    space: SymbolicCandidateSpace,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
) -> None:
    """Reject a v2 manifest whose target or theorem assertions differ from live inputs."""

    expected_scope = _common_scope(coverage_certificate, solver_certificate)
    if manifest.target.candidate_space_description != space.space_description:
        raise ValueError("tiered manifest candidate-space description does not match the declared space")
    if set(manifest.target.motifs) != set(space.motifs):
        raise ValueError("tiered manifest motif vocabulary does not match the declared space")
    if manifest.target.required_cell_ids != coverage_certificate.required_cell_ids:
        raise ValueError("tiered manifest required cells do not match the coverage certificate")
    if set(manifest.target.required_cell_ids) != set(solver_certificate.required_cell_ids):
        raise ValueError("tiered manifest required cells do not match the solver certificate")
    if manifest.target.certified_looks != expected_scope:
        raise ValueError("tiered manifest look scope does not match the common certificate scope")
    if manifest.coverage_assertion.lower_bound != coverage_certificate.lower_bound:
        raise ValueError("tiered manifest coverage bound does not match the coverage certificate")
    if manifest.coverage_assertion.method != coverage_certificate.method:
        raise ValueError("tiered manifest coverage method does not match the coverage certificate")
    if manifest.coverage_assertion.assumptions != coverage_certificate.assumptions:
        raise ValueError("tiered manifest coverage assumptions do not match the coverage certificate")
    if manifest.solver_assertion.lower_bound != solver_certificate.lower_bound:
        raise ValueError("tiered manifest solver bound does not match the solver certificate")
    if manifest.solver_assertion.method != solver_certificate.method:
        raise ValueError("tiered manifest solver method does not match the solver certificate")
    if manifest.solver_assertion.assumptions != solver_certificate.assumptions:
        raise ValueError("tiered manifest solver assumptions do not match the solver certificate")


def verify_tiered_manifest_artifacts(
    manifest: TieredCertificateManifest,
    payloads: Mapping[str, str | bytes],
) -> TieredManifestVerificationReport:
    """Verify every content-addressed artifact referenced by one v2 manifest."""

    artifacts = manifest.referenced_artifacts()
    missing = set(artifacts) - set(payloads)
    if missing:
        raise ValueError(f"missing payloads for tiered manifest artifacts: {sorted(missing)}")
    unexpected = set(payloads) - set(artifacts)
    if unexpected:
        raise ValueError(f"payloads include artifact IDs absent from the tiered manifest: {sorted(unexpected)}")
    for artifact_id, artifact in artifacts.items():
        if sha256_digest(payloads[artifact_id]) != artifact.sha256:
            raise ValueError(f"artifact digest mismatch for {artifact_id!r}")
    return TieredManifestVerificationReport(
        manifest_digest=manifest.manifest_digest,
        target_digest=manifest.target.target_digest,
        tiered_target_digest=manifest.tiered_target_digest,
        verified_artifact_ids=tuple(sorted(artifacts)),
    )


def verify_anytime_tiered_symbolic_manifest(
    manifest: TieredCertificateManifest,
    *,
    space: SymbolicCandidateSpace,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
    payloads: Mapping[str, str | bytes],
) -> TieredManifestVerificationReport:
    """Verify v2 theorem context and all v2 artifact content commitments."""

    verify_tiered_manifest_context(
        manifest,
        space=space,
        coverage_certificate=coverage_certificate,
        solver_certificate=solver_certificate,
    )
    return verify_tiered_manifest_artifacts(manifest, payloads)


def migrate_v1_manifest_to_explicit_single_tier_v2(
    manifest: CertificateManifest,
    *,
    tier: QueryTier,
    semantic_partition_artifact: ArtifactReference,
    tiered_query_plans: Iterable[TieredQueryPlanBinding],
) -> TieredCertificateManifest:
    """Promote a v1 manifest only to one explicitly declared tier.

    This function deliberately cannot manufacture inner *and* outer bindings
    from a tierless v1 manifest.  The caller supplies the chosen tier and the
    new partition/plan commitments.  Every v1 proof is linked to the exact
    supplied v2 plan with matching look and cell.
    """

    if not isinstance(manifest, CertificateManifest):
        raise TypeError("manifest must be a CertificateManifest")
    if not isinstance(tier, QueryTier):
        raise ValueError("migration tier must be a QueryTier")
    plans = tuple(tiered_query_plans)
    plans_by_look_cell = {
        (plan.look, plan.cell_id): plan
        for plan in plans
        if plan.tier is tier
    }
    if len(plans_by_look_cell) != len(plans):
        raise ValueError("single-tier migration plans must be unique and all use the requested tier")
    migrated_proofs: list[TieredSolverQueryProofBinding] = []
    for binding in manifest.solver_query_proofs:
        plan = plans_by_look_cell.get((binding.look, binding.cell_id))
        if plan is None:
            raise ValueError("single-tier migration needs one explicit v2 plan for every v1 proof look/cell")
        migrated_proofs.append(
            TieredSolverQueryProofBinding(
                tier=tier,
                look=binding.look,
                cell_id=binding.cell_id,
                motif=binding.motif,
                role=binding.role,
                status=binding.status,
                query_plan_artifact=plan.query_plan_artifact,
                proof_artifact=binding.proof_artifact,
                verifier_id=binding.verifier_id,
            )
        )
    return TieredCertificateManifest(
        target=manifest.target,
        coverage_assertion=manifest.coverage_assertion,
        solver_assertion=manifest.solver_assertion,
        semantic_partition_artifact=semantic_partition_artifact,
        tiered_query_plans=plans,
        solver_query_proofs=tuple(migrated_proofs),
    )
