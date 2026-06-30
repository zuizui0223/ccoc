"""End-to-end all-look admission for exact polyhedral RACH extensions.

PR #18 supplies an all-look, gamma-zero inclusion schema when every admitted
inner polyhedron retains a verified base system and every outer polyhedron is
fixed. This module supplies the matching beta-zero solver side.

At each admitted look, both inner and outer symbolic tiers are built only from
exact rational linear proof bundles. Every decisive SAT witness and UNSAT Farkas
certificate is checked by the existing exact verifier. For each cell, all motif
bundles must share one identical ``nonempty`` retained-set system; this prevents
motif-specific substitution of a different candidate set.

The resulting paired sequential snapshot is tied to the PR #18 inclusion gate:

    current inner retained polyhedron
        subseteq verified base inner polyhedron
        subseteq fixed outer retained polyhedron
        == nonempty retained system used by every outer motif bundle.

Thus, for every look admitted through this combined gate, the outer solver
semantic certificate and the inner-to-outer inclusion certificate both have
lower bound one. The construction is still conditional on exact parser/verifier
trust, the declared linear query encodings, and use of the admission gate for
every claimed look.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Mapping

from .admissibility import CoverageMode
from .anytime_symbolic_extension_stability import (
    AnytimeSymbolicExtensionTarget,
    SequentialSymbolicUniverseExtensionSnapshot,
)
from .anytime_symbolic_lifting import AnytimeSolverSemanticValidityCertificate
from .linear_proof_verifier import (
    LinearMotifQueryBundle,
    RationalLinearSystem,
    RationalWitness,
    linear_bundles_to_symbolic_cell,
)
from .online_polyhedral_inclusion_schema import (
    EXACT_MONOTONE_POLYHEDRAL_INCLUSION_SCHEMA_VERIFIER,
    MonotonePolyhedralInclusionLook,
    MonotonePolyhedralInclusionSchema,
    VerifiedMonotonePolyhedralInclusionLook,
    VerifiedMonotonePolyhedralInclusionSchema,
    verify_monotone_polyhedral_inclusion_look,
    verify_monotone_polyhedral_inclusion_schema,
)
from .symbolic_candidate_sets import (
    FeasibilityStatus,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
)
from .symbolic_universe_extension import SymbolicUniverseTier


EXACT_POLYHEDRAL_EXTENSION_ADMISSION_VERIFIER = (
    "exact-polyhedral-extension-admission-verifier"
)


@dataclass(frozen=True)
class ExactLinearProofCell:
    """Exact linear query bundles for every motif in one retained-set cell.

    Every motif bundle must use the same nonempty retained-set system. Its active
    and inactive systems may add different declared motif restrictions, but the
    base retained set cannot change across motifs.
    """

    description: str
    motif_bundles: Mapping[str, LinearMotifQueryBundle]
    required: bool = True

    def __post_init__(self) -> None:
        if not self.description:
            raise ValueError("exact linear proof cell description must be non-empty")
        if not self.motif_bundles:
            raise ValueError("exact linear proof cell needs motif bundles")


@dataclass(frozen=True)
class ExactPolyhedralExtensionLook:
    """Proposed inner and outer exact-proof tiers at one sequential look."""

    look: int
    inner_cells_by_id: Mapping[str, ExactLinearProofCell]
    outer_cells_by_id: Mapping[str, ExactLinearProofCell]
    evidence_reference: str

    def __post_init__(self) -> None:
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("look must be a positive integer")
        if not self.evidence_reference:
            raise ValueError("an exact polyhedral extension look needs an evidence_reference")


@dataclass(frozen=True)
class ExactPolyhedralExtensionAdmissionSchema:
    """Fixed target for all admitted exact polyhedral extension looks."""

    space: SymbolicCandidateSpace
    required_cell_ids: tuple[str, ...]
    inclusion_schema: MonotonePolyhedralInclusionSchema
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.required_cell_ids:
            raise ValueError("required_cell_ids must not be empty")
        if len(set(self.required_cell_ids)) != len(self.required_cell_ids):
            raise ValueError("required_cell_ids must be unique")

    @property
    def target(self) -> AnytimeSymbolicExtensionTarget:
        return AnytimeSymbolicExtensionTarget(
            inner_tier_id=self.inclusion_schema.inner_tier_id,
            outer_tier_id=self.inclusion_schema.outer_tier_id,
            space=self.space,
            required_cell_ids=self.required_cell_ids,
        )


@dataclass(frozen=True)
class VerifiedExactPolyhedralExtensionAdmissionSchema:
    """Verified all-look beta-zero and gamma-zero admission target."""

    schema: ExactPolyhedralExtensionAdmissionSchema
    verified_inclusion_schema: VerifiedMonotonePolyhedralInclusionSchema
    all_look_solver_certificate: AnytimeSolverSemanticValidityCertificate

    @property
    def target(self) -> AnytimeSymbolicExtensionTarget:
        return self.schema.target

    @property
    def all_look_inclusion_certificate(self):
        return self.verified_inclusion_schema.all_look_inclusion_certificate


@dataclass(frozen=True)
class VerifiedExactPolyhedralExtensionLook:
    """One paired inner/outer snapshot admitted by both exact proof gates."""

    look: int
    snapshot: SequentialSymbolicUniverseExtensionSnapshot
    verified_inclusion_look: VerifiedMonotonePolyhedralInclusionLook
    evidence_reference: str
    verifier: str
    assumptions: tuple[str, ...]


def _row_counter(system: RationalLinearSystem) -> Counter[tuple[tuple[object, ...], object]]:
    return Counter(
        (inequality.coefficients, inequality.bound)
        for inequality in system.inequalities
    )


def _same_system(left: RationalLinearSystem, right: RationalLinearSystem) -> bool:
    return left.variables == right.variables and _row_counter(left) == _row_counter(right)


def _validate_exact_cell_ids(
    mapping: Mapping[str, object],
    required_cell_ids: tuple[str, ...],
    name: str,
) -> None:
    if tuple(mapping) != required_cell_ids:
        raise ValueError(f"{name} must exactly match required_cell_ids in order")


def _common_nonempty_system_and_witness(
    *,
    cell_id: str,
    proof_cell: ExactLinearProofCell,
    space: SymbolicCandidateSpace,
) -> tuple[RationalLinearSystem, RationalWitness]:
    if set(proof_cell.motif_bundles) != set(space.motifs):
        raise ValueError(f"cell {cell_id!r} must contain exactly the declared motif bundles")
    ordered_bundles = tuple(proof_cell.motif_bundles[motif] for motif in space.motifs)
    first_query = ordered_bundles[0].nonempty
    system = first_query.system
    witness: RationalWitness | None = None
    for motif, bundle in zip(space.motifs, ordered_bundles):
        query = bundle.nonempty
        if not _same_system(system, query.system):
            raise ValueError(
                f"cell {cell_id!r} motif bundles must share one identical nonempty retained-set system"
            )
        if query.proof.status is not FeasibilityStatus.SAT or query.proof.witness is None:
            raise ValueError(
                f"cell {cell_id!r} motif {motif!r} needs an exact SAT nonempty proof for all-look admission"
            )
        if witness is None:
            witness = query.proof.witness
    assert witness is not None
    return system, witness


def _verified_symbolic_cell(
    *,
    cell_id: str,
    proof_cell: ExactLinearProofCell,
    space: SymbolicCandidateSpace,
) -> tuple[SymbolicConfidenceSetCell, RationalLinearSystem, RationalWitness]:
    retained_system, witness = _common_nonempty_system_and_witness(
        cell_id=cell_id,
        proof_cell=proof_cell,
        space=space,
    )
    cell = linear_bundles_to_symbolic_cell(
        cell_id=cell_id,
        description=proof_cell.description,
        motif_bundles=proof_cell.motif_bundles,
        required=proof_cell.required,
        coverage_mode=CoverageMode.SOLVER_BACKED,
    )
    return cell, retained_system, witness


def verify_exact_polyhedral_extension_admission_schema(
    schema: ExactPolyhedralExtensionAdmissionSchema,
) -> VerifiedExactPolyhedralExtensionAdmissionSchema:
    """Verify the base inclusion and create all-look beta/gamma-zero certificates.

    The beta-zero certificate covers only outer decisive results from looks
    admitted by `admit_exact_polyhedral_extension_look`. The gamma-zero
    certificate is inherited from the verified PR #18 monotone inclusion schema.
    """

    verified_inclusion = verify_monotone_polyhedral_inclusion_schema(
        schema.inclusion_schema,
        required_cell_ids=schema.required_cell_ids,
    )
    solver_certificate = AnytimeSolverSemanticValidityCertificate(
        required_cell_ids=schema.required_cell_ids,
        motifs=schema.space.motifs,
        lower_bound=1.0,
        method=EXACT_POLYHEDRAL_EXTENSION_ADMISSION_VERIFIER,
        assumptions=(
            "every claimed outer look is built by exact rational linear proof-bundle admission",
            "every decisive outer SAT/UNSAT result is checked by the exact rational linear verifier",
            "every motif bundle in a cell shares the same verified nonempty retained-set system",
            "all claimed extension looks pass the paired exact inclusion admission gate",
            *schema.assumptions,
            *verified_inclusion.all_look_inclusion_certificate.assumptions,
        ),
        certified_looks=None,
    )
    return VerifiedExactPolyhedralExtensionAdmissionSchema(
        schema=schema,
        verified_inclusion_schema=verified_inclusion,
        all_look_solver_certificate=solver_certificate,
    )


def admit_exact_polyhedral_extension_look(
    verified_schema: VerifiedExactPolyhedralExtensionAdmissionSchema,
    proposed_look: ExactPolyhedralExtensionLook,
) -> VerifiedExactPolyhedralExtensionLook:
    """Verify both symbolic tiers and the exact inner-to-outer inclusion at one look.

    The returned snapshot is the intended object for the anytime outer-envelope
    audit. It is constructed only after every linear query proof has verified and
    after the nonempty retained systems have been bound to the PR #18 monotone
    inclusion gate.
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

    for cell_id in required:
        inner_cell, inner_system, inner_witness = _verified_symbolic_cell(
            cell_id=cell_id,
            proof_cell=proposed_look.inner_cells_by_id[cell_id],
            space=schema.space,
        )
        outer_cell, outer_system, _ = _verified_symbolic_cell(
            cell_id=cell_id,
            proof_cell=proposed_look.outer_cells_by_id[cell_id],
            space=schema.space,
        )
        if not inner_cell.required or not outer_cell.required:
            raise ValueError("all exact extension admission cells must be required")
        inner_cells.append(inner_cell)
        outer_cells.append(outer_cell)
        inner_systems[cell_id] = inner_system
        outer_systems[cell_id] = outer_system
        inner_witnesses[cell_id] = inner_witness

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
            description=f"exact admitted inner tier at look {proposed_look.look}",
        ),
        outer=SymbolicUniverseTier(
            tier_id=schema.inclusion_schema.outer_tier_id,
            space=schema.space,
            cells=tuple(outer_cells),
            description=f"exact admitted outer tier at look {proposed_look.look}",
        ),
    )
    return VerifiedExactPolyhedralExtensionLook(
        look=proposed_look.look,
        snapshot=snapshot,
        verified_inclusion_look=inclusion_look,
        evidence_reference=proposed_look.evidence_reference,
        verifier=EXACT_POLYHEDRAL_EXTENSION_ADMISSION_VERIFIER,
        assumptions=(
            "all inner and outer linear motif queries were exactly verified",
            "outer nonempty retained systems match the fixed inclusion-envelope systems",
            "inner nonempty retained systems passed monotone inclusion admission",
            *verified_schema.all_look_solver_certificate.assumptions,
        ),
    )
