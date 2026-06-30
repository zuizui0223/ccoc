"""All-look exact admission with compiler-generated polyhedral motif complements.

The single-polyhedron all-look admission path proves exact solver semantics for
hand-assembled active/inactive motif queries. The proof-carrying polyhedral motif
compiler removes the remaining query-encoding gap, but initially only for static
symbolic cells. This module joins the two layers.

A fixed verified tagged polyhedral union defines the candidate universe
``Theta``. At each admitted look and required robustness cell, the caller
supplies only:

* an inner retained polyhedron ``C_inner,t`` and exact branch proofs; and
* an outer retained polyhedron ``C_outer`` and exact branch proofs.

The compiler constructs every query system ``C ∩ U_j``. It derives active and
inactive query families from the fixed cell tags, then exact-verifies every
branch witness / Farkas proof. In parallel, the existing monotone inclusion gate
checks

    C_inner,t subseteq C_base subseteq C_outer.

Because the tagged universe is fixed,

    C_inner,t ∩ Theta subseteq C_outer ∩ Theta.

Thus the compiler-generated symbolic tiers inherit all-look gamma-zero inclusion
and all-look beta-zero decisive solver semantics. With valid all-look outer
coverage, the usual optional-stopping outer-envelope bound reduces to alpha for
looks admitted through this combined gate.

This module is deliberately limited to one fixed finite tagged rational
polyhedral union and conjunction-only retained systems. It is not an arbitrary
Boolean or nonlinear compiler, and it does not prove coverage of the declared
union by nature.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .admissibility import CoverageMode
from .anytime_symbolic_extension_stability import (
    AnytimeSymbolicExtensionStabilityGuarantee,
    AnytimeSymbolicExtensionStabilityReport,
    AnytimeSymbolicExtensionTarget,
    SequentialSymbolicUniverseExtensionSnapshot,
    anytime_symbolic_extension_stability_guarantee,
    audit_anytime_symbolic_universe_extension,
)
from .anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
)
from .linear_proof_verifier import (
    LinearFeasibilityProof,
    RationalLinearSystem,
    RationalWitness,
)
from .online_polyhedral_inclusion_schema import (
    MonotonePolyhedralInclusionLook,
    MonotonePolyhedralInclusionSchema,
    VerifiedMonotonePolyhedralInclusionLook,
    VerifiedMonotonePolyhedralInclusionSchema,
    verify_monotone_polyhedral_inclusion_look,
    verify_monotone_polyhedral_inclusion_schema,
)
from .polyhedral_motif_compiler import (
    BoundCompiledPolyhedralMotifProofs,
    CompiledPolyhedralMotifQueryPlan,
    PolyhedralMotifPartition,
    VerifiedCompiledPolyhedralMotifQueries,
    VerifiedPolyhedralMotifPartition,
    bind_compiled_polyhedral_motif_proofs,
    compile_polyhedral_motif_query_plan,
    compiled_polyhedral_motif_symbolic_cell,
    verify_compiled_polyhedral_motif_proofs,
    verify_polyhedral_motif_partition,
)
from .symbolic_candidate_sets import (
    FeasibilityStatus,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
)
from .symbolic_universe_extension import (
    SymbolicUniverseTier,
)
from .symbolic_universe_extension import JointSymbolicInclusionCertificate
from .anytime_symbolic_extension_stability import AnytimeJointSymbolicInclusionCertificate


EXACT_COMPILED_POLYHEDRAL_EXTENSION_ADMISSION_VERIFIER = (
    "exact-compiled-polyhedral-extension-admission-verifier"
)


def _require_nonempty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")


def _validate_exact_cell_ids(
    mapping: Mapping[str, object],
    required_cell_ids: tuple[str, ...],
    name: str,
) -> None:
    if tuple(mapping) != required_cell_ids:
        raise ValueError(f"{name} must exactly match required_cell_ids in order")


@dataclass(frozen=True)
class ExactCompiledPolyhedralProofCell:
    """One retained polyhedron plus proofs for compiler-generated branch IDs only."""

    description: str
    retained_system: RationalLinearSystem
    proofs_by_query_id: Mapping[str, LinearFeasibilityProof]
    required: bool = True

    def __post_init__(self) -> None:
        _require_nonempty(self.description, "compiled proof cell description")
        if not self.proofs_by_query_id:
            raise ValueError("compiled proof cell needs at least one branch proof")


@dataclass(frozen=True)
class ExactCompiledPolyhedralExtensionLook:
    """One proposed paired retained-system state at a sequential look."""

    look: int
    inner_cells_by_id: Mapping[str, ExactCompiledPolyhedralProofCell]
    outer_cells_by_id: Mapping[str, ExactCompiledPolyhedralProofCell]
    evidence_reference: str

    def __post_init__(self) -> None:
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("look must be a positive integer")
        _require_nonempty(self.evidence_reference, "compiled extension look evidence_reference")


@dataclass(frozen=True)
class ExactCompiledPolyhedralExtensionAdmissionSchema:
    """Fixed all-look target with one verified tagged polyhedral candidate union."""

    space: SymbolicCandidateSpace
    required_cell_ids: tuple[str, ...]
    inclusion_schema: MonotonePolyhedralInclusionSchema
    motif_partition: VerifiedPolyhedralMotifPartition
    query_namespace: str = "compiled-polyhedral-admission"
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.required_cell_ids:
            raise ValueError("required_cell_ids must not be empty")
        if len(set(self.required_cell_ids)) != len(self.required_cell_ids):
            raise ValueError("required_cell_ids must be unique")
        _require_nonempty(self.query_namespace, "query_namespace")

    @property
    def target(self) -> AnytimeSymbolicExtensionTarget:
        return AnytimeSymbolicExtensionTarget(
            inner_tier_id=self.inclusion_schema.inner_tier_id,
            outer_tier_id=self.inclusion_schema.outer_tier_id,
            space=self.space,
            required_cell_ids=self.required_cell_ids,
        )


@dataclass(frozen=True)
class VerifiedExactCompiledPolyhedralExtensionAdmissionSchema:
    """Reverified partition plus all-look beta/gamma-zero certificates."""

    schema: ExactCompiledPolyhedralExtensionAdmissionSchema
    verified_partition: VerifiedPolyhedralMotifPartition
    verified_inclusion_schema: VerifiedMonotonePolyhedralInclusionSchema
    all_look_solver_certificate: AnytimeSolverSemanticValidityCertificate
    all_look_inclusion_certificate: AnytimeJointSymbolicInclusionCertificate

    @property
    def target(self) -> AnytimeSymbolicExtensionTarget:
        return self.schema.target


@dataclass(frozen=True)
class VerifiedExactCompiledPolyhedralExtensionLook:
    """One exact-admitted paired snapshot with compiler-derived motif semantics."""

    look: int
    snapshot: SequentialSymbolicUniverseExtensionSnapshot
    verified_inclusion_look: VerifiedMonotonePolyhedralInclusionLook
    inner_queries_by_cell: Mapping[str, VerifiedCompiledPolyhedralMotifQueries]
    outer_queries_by_cell: Mapping[str, VerifiedCompiledPolyhedralMotifQueries]
    evidence_reference: str
    verifier: str
    assumptions: tuple[str, ...]


def _reverify_partition(
    proposed: VerifiedPolyhedralMotifPartition,
) -> VerifiedPolyhedralMotifPartition:
    """Reject hand-assembled or stale verified wrappers at the public boundary."""

    recomputed = verify_polyhedral_motif_partition(proposed.partition)
    if (
        proposed.partition_digest != recomputed.partition_digest
        or proposed.verified_conflicting_pairs != recomputed.verified_conflicting_pairs
    ):
        raise ValueError("supplied verified motif partition does not match exact re-verification")
    return recomputed


def _validate_schema_partition_compatibility(
    schema: ExactCompiledPolyhedralExtensionAdmissionSchema,
    verified_partition: VerifiedPolyhedralMotifPartition,
) -> None:
    partition = verified_partition.partition
    if partition.space != schema.space:
        raise ValueError("compiled motif partition candidate space must equal the admission schema space")
    _validate_exact_cell_ids(
        schema.inclusion_schema.base_queries_by_cell,
        schema.required_cell_ids,
        "inclusion_schema.base_queries_by_cell",
    )
    variables = partition.cells[0].system.variables
    for cell_id in schema.required_cell_ids:
        base_query = schema.inclusion_schema.base_queries_by_cell[cell_id]
        if base_query.inner_system.variables != variables or base_query.outer_system.variables != variables:
            raise ValueError("inclusion base systems must use the fixed partition variable vocabulary")


def verify_exact_compiled_polyhedral_extension_admission_schema(
    schema: ExactCompiledPolyhedralExtensionAdmissionSchema,
) -> VerifiedExactCompiledPolyhedralExtensionAdmissionSchema:
    """Create all-look beta/gamma-zero certificates for compiler-admitted tiers."""

    verified_partition = _reverify_partition(schema.motif_partition)
    _validate_schema_partition_compatibility(schema, verified_partition)
    verified_inclusion = verify_monotone_polyhedral_inclusion_schema(
        schema.inclusion_schema,
        required_cell_ids=schema.required_cell_ids,
    )
    inherited = verified_inclusion.all_look_inclusion_certificate
    inclusion_certificate = AnytimeJointSymbolicInclusionCertificate(
        inner_tier_id=inherited.inner_tier_id,
        outer_tier_id=inherited.outer_tier_id,
        required_cell_ids=inherited.required_cell_ids,
        lower_bound=1.0,
        method=EXACT_COMPILED_POLYHEDRAL_EXTENSION_ADMISSION_VERIFIER,
        assumptions=(
            "the candidate universe is one fixed exact-verified finite tagged polyhedral union",
            "each admitted symbolic retained set is the retained polyhedron intersected with that fixed union",
            "ambient retained-polyhedron inclusion implies inclusion after intersection with the fixed union",
            "all claimed extension looks pass exact monotone retained-polyhedron admission",
            f"verified tagged partition digest: {verified_partition.partition_digest}",
            *schema.assumptions,
            *inherited.assumptions,
        ),
        evidence_reference=inherited.evidence_reference,
        certified_looks=None,
    )
    solver_certificate = AnytimeSolverSemanticValidityCertificate(
        required_cell_ids=schema.required_cell_ids,
        motifs=schema.space.motifs,
        lower_bound=1.0,
        method=EXACT_COMPILED_POLYHEDRAL_EXTENSION_ADMISSION_VERIFIER,
        assumptions=(
            "every claimed look derives active/inactive query families solely from the fixed verified tagged partition",
            "every compiler-generated rational branch query is checked by an exact witness or Farkas certificate",
            "finite-union SAT/UNSAT aggregation is exact and UNKNOWN remains non-decisive",
            "all claimed extension looks pass paired compiler and exact inclusion admission",
            f"verified tagged partition digest: {verified_partition.partition_digest}",
            *schema.assumptions,
            *inherited.assumptions,
        ),
        certified_looks=None,
    )
    return VerifiedExactCompiledPolyhedralExtensionAdmissionSchema(
        schema=schema,
        verified_partition=verified_partition,
        verified_inclusion_schema=verified_inclusion,
        all_look_solver_certificate=solver_certificate,
        all_look_inclusion_certificate=inclusion_certificate,
    )


def compiled_query_plan_for_admission(
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    *,
    look: int,
    tier: str,
    cell_id: str,
    retained_system: RationalLinearSystem,
) -> CompiledPolyhedralMotifQueryPlan:
    """Return the only branch query plan accepted by the all-look compiler gate."""

    if not isinstance(look, int) or look < 1:
        raise ValueError("look must be a positive integer")
    if tier not in ("inner", "outer"):
        raise ValueError("tier must be 'inner' or 'outer'")
    if cell_id not in verified_schema.schema.required_cell_ids:
        raise ValueError("cell_id must be a required admission-schema cell")
    prefix = f"{verified_schema.schema.query_namespace}/{tier}/look-{look}/cell-{cell_id}"
    return compile_polyhedral_motif_query_plan(
        verified_schema.verified_partition,
        retained_system=retained_system,
        query_prefix=prefix,
    )


def _nonempty_retained_witness(
    verified_queries: VerifiedCompiledPolyhedralMotifQueries,
) -> RationalWitness:
    """Extract a branch witness proving both C∩Theta and ambient C are non-empty."""

    plan = verified_queries.bound_proofs.plan
    first_motif = plan.verified_partition.partition.space.motifs[0]
    if verified_queries.motif_queries[first_motif].nonempty.status is not FeasibilityStatus.SAT:
        raise ValueError("all-look compiled admission requires exact SAT retained-set nonemptiness")
    for template in plan.nonempty_templates:
        query = verified_queries.bound_proofs.queries_by_id[template.query_id]
        if query.proof.status is FeasibilityStatus.SAT:
            assert query.proof.witness is not None
            return query.proof.witness
    raise RuntimeError("compiled nonempty aggregate is SAT without an exact SAT branch witness")


def _compile_verify_cell(
    *,
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    look: int,
    tier: str,
    cell_id: str,
    proposed: ExactCompiledPolyhedralProofCell,
) -> tuple[SymbolicConfidenceSetCell, VerifiedCompiledPolyhedralMotifQueries, RationalWitness]:
    if not proposed.required:
        raise ValueError("all exact compiled extension admission cells must be required")
    plan = compiled_query_plan_for_admission(
        verified_schema,
        look=look,
        tier=tier,
        cell_id=cell_id,
        retained_system=proposed.retained_system,
    )
    bound: BoundCompiledPolyhedralMotifProofs = bind_compiled_polyhedral_motif_proofs(
        plan,
        proofs_by_query_id=proposed.proofs_by_query_id,
    )
    verified_queries = verify_compiled_polyhedral_motif_proofs(bound)
    witness = _nonempty_retained_witness(verified_queries)
    symbolic_cell = compiled_polyhedral_motif_symbolic_cell(
        verified_queries,
        cell_id=cell_id,
        description=proposed.description,
        required=True,
        coverage_mode=CoverageMode.SOLVER_BACKED,
    )
    return symbolic_cell, verified_queries, witness


def admit_exact_compiled_polyhedral_extension_look(
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    proposed_look: ExactCompiledPolyhedralExtensionLook,
) -> VerifiedExactCompiledPolyhedralExtensionLook:
    """Admit one look only after exact compiler and inclusion verification.

    Active/inactive systems are never supplied by the caller. They are produced
    branchwise from the fixed tagged partition, and all decisive branches receive
    exact rational proof verification before a normal symbolic RACH snapshot is
    constructed.
    """

    schema = verified_schema.schema
    required = schema.required_cell_ids
    _validate_exact_cell_ids(proposed_look.inner_cells_by_id, required, "inner_cells_by_id")
    _validate_exact_cell_ids(proposed_look.outer_cells_by_id, required, "outer_cells_by_id")

    inner_cells: list[SymbolicConfidenceSetCell] = []
    outer_cells: list[SymbolicConfidenceSetCell] = []
    inner_systems: dict[str, RationalLinearSystem] = {}
    outer_systems: dict[str, RationalLinearSystem] = {}
    inner_witnesses: dict[str, RationalWitness] = {}
    inner_queries_by_cell: dict[str, VerifiedCompiledPolyhedralMotifQueries] = {}
    outer_queries_by_cell: dict[str, VerifiedCompiledPolyhedralMotifQueries] = {}

    for cell_id in required:
        inner_proposed = proposed_look.inner_cells_by_id[cell_id]
        outer_proposed = proposed_look.outer_cells_by_id[cell_id]
        inner_cell, inner_queries, inner_witness = _compile_verify_cell(
            verified_schema=verified_schema,
            look=proposed_look.look,
            tier="inner",
            cell_id=cell_id,
            proposed=inner_proposed,
        )
        outer_cell, outer_queries, _ = _compile_verify_cell(
            verified_schema=verified_schema,
            look=proposed_look.look,
            tier="outer",
            cell_id=cell_id,
            proposed=outer_proposed,
        )
        inner_cells.append(inner_cell)
        outer_cells.append(outer_cell)
        inner_systems[cell_id] = inner_proposed.retained_system
        outer_systems[cell_id] = outer_proposed.retained_system
        inner_witnesses[cell_id] = inner_witness
        inner_queries_by_cell[cell_id] = inner_queries
        outer_queries_by_cell[cell_id] = outer_queries

    inclusion_look = verify_monotone_polyhedral_inclusion_look(
        verified_schema.verified_inclusion_schema,
        MonotonePolyhedralInclusionLook(
            look=proposed_look.look,
            inner_systems_by_cell=inner_systems,
            outer_systems_by_cell=outer_systems,
            inner_witnesses_by_cell=inner_witnesses,
            evidence_reference=proposed_look.evidence_reference,
        ),
    )
    snapshot = SequentialSymbolicUniverseExtensionSnapshot(
        look=proposed_look.look,
        inner=SymbolicUniverseTier(
            tier_id=schema.inclusion_schema.inner_tier_id,
            space=schema.space,
            cells=tuple(inner_cells),
            description=f"compiler-admitted inner tier at look {proposed_look.look}",
        ),
        outer=SymbolicUniverseTier(
            tier_id=schema.inclusion_schema.outer_tier_id,
            space=schema.space,
            cells=tuple(outer_cells),
            description=f"compiler-admitted outer tier at look {proposed_look.look}",
        ),
    )
    return VerifiedExactCompiledPolyhedralExtensionLook(
        look=proposed_look.look,
        snapshot=snapshot,
        verified_inclusion_look=inclusion_look,
        inner_queries_by_cell=inner_queries_by_cell,
        outer_queries_by_cell=outer_queries_by_cell,
        evidence_reference=proposed_look.evidence_reference,
        verifier=EXACT_COMPILED_POLYHEDRAL_EXTENSION_ADMISSION_VERIFIER,
        assumptions=(
            "all inner and outer motif query families were generated from the fixed verified tagged partition",
            "all decisive compiler branches were exactly rational-proof verified",
            "outer retained polyhedra match the fixed inclusion-envelope systems",
            "inner retained polyhedra passed monotone exact inclusion admission",
            "intersection with the fixed declared tagged union preserves the verified inclusion relation",
            *verified_schema.all_look_solver_certificate.assumptions,
        ),
    )


def audit_exact_compiled_polyhedral_extension_looks(
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    admitted_looks: Iterable[VerifiedExactCompiledPolyhedralExtensionLook],
    *,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> AnytimeSymbolicExtensionStabilityReport:
    """Audit compiler-admitted snapshots with their paired all-look certificates."""

    snapshots = tuple(admitted.snapshot for admitted in admitted_looks)
    if not snapshots:
        raise ValueError("at least one compiler-admitted look is required for an audit")
    return audit_anytime_symbolic_universe_extension(
        snapshots,
        inclusion_certificate=verified_schema.all_look_inclusion_certificate,
        coverage_certificate=coverage_certificate,
        solver_certificate=verified_schema.all_look_solver_certificate,
    )


def exact_compiled_polyhedral_extension_guarantee(
    verified_schema: VerifiedExactCompiledPolyhedralExtensionAdmissionSchema,
    *,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
) -> AnytimeSymbolicExtensionStabilityGuarantee:
    """Return the all-look optional-stopping guarantee for compiler-admitted tiers."""

    return anytime_symbolic_extension_stability_guarantee(
        target=verified_schema.target,
        coverage_certificate=coverage_certificate,
        solver_certificate=verified_schema.all_look_solver_certificate,
        inclusion_certificate=verified_schema.all_look_inclusion_certificate,
    )
