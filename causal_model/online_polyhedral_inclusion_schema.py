"""All-look gamma-zero inclusion via an online monotone polyhedral schema.

A finite bundle of exact polyhedral inclusion proofs certifies only listed
analysis looks. This module provides a different, more structural route to an
all-look inclusion guarantee for a restricted sequential pattern.

For every required cell r, first verify exactly that a fixed non-empty base
polyhedron lies inside a fixed outer envelope:

    P_base,r subseteq P_outer,r.

At every later look t, admit an inner polyhedron only after checking that it
contains every base inequality as an exact row and that its supplied rational
witness is feasible. Hence

    P_inner,r,t subseteq P_base,r subseteq P_outer,r

at every admitted look. Because the same deterministic verifier checks each
look, this is a proof schema over all admitted positive integer looks, not a
finite prelisted panel. It can therefore supply an all-look symbolic inclusion
certificate with gamma = 0.

The construction is deliberately conservative: it requires a fixed outer
polyhedron and syntactic accumulation of base inequalities. It is a verifier,
not a solver, and it does not prove that a caller actually routes every future
look through the admission gate.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Mapping

from .anytime_symbolic_extension_stability import AnytimeJointSymbolicInclusionCertificate
from .linear_proof_verifier import RationalLinearSystem, RationalWitness
from .rational_polyhedral_inclusion import (
    EXACT_RATIONAL_POLYHEDRAL_INCLUSION_VERIFIER,
    ExactRationalJointInclusionProof,
    RationalPolyhedralInclusionQuery,
    verify_exact_rational_joint_inclusion,
)


EXACT_MONOTONE_POLYHEDRAL_INCLUSION_SCHEMA_VERIFIER = (
    "exact-monotone-polyhedral-inclusion-schema-verifier"
)


@dataclass(frozen=True)
class MonotonePolyhedralInclusionSchema:
    """A fixed base-to-outer proof target for every required robustness cell.

    Each base query proves ``P_base,r subseteq P_outer,r`` using the exact
    rational row-implication verifier. A later inner set is admitted only when it
    has the same ordered variables, retains every base row, and is non-empty at a
    supplied exact witness.
    """

    inner_tier_id: str
    outer_tier_id: str
    base_queries_by_cell: Mapping[str, RationalPolyhedralInclusionQuery]
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.inner_tier_id or not self.outer_tier_id:
            raise ValueError("inner_tier_id and outer_tier_id must be non-empty")
        if self.inner_tier_id == self.outer_tier_id:
            raise ValueError("inner and outer tier IDs must differ")
        if not self.base_queries_by_cell:
            raise ValueError("base_queries_by_cell must not be empty")
        if any(not cell_id for cell_id in self.base_queries_by_cell):
            raise ValueError("base query cell IDs must be non-empty")


@dataclass(frozen=True)
class MonotonePolyhedralInclusionLook:
    """One proposed sequential inner/outer polyhedral state for admission.

    `inner_systems_by_cell` may contain additional inequalities beyond the base
    system. `outer_systems_by_cell` must equal the fixed outer systems exactly,
    up to row ordering and inequality labels. The provided inner witnesses make
    every admitted inner set non-vacuously feasible.
    """

    look: int
    inner_systems_by_cell: Mapping[str, RationalLinearSystem]
    outer_systems_by_cell: Mapping[str, RationalLinearSystem]
    inner_witnesses_by_cell: Mapping[str, RationalWitness]
    evidence_reference: str

    def __post_init__(self) -> None:
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("look must be a positive integer")
        if not self.evidence_reference:
            raise ValueError("an admitted online look needs an evidence_reference")


@dataclass(frozen=True)
class VerifiedMonotonePolyhedralInclusionSchema:
    """A verified base proof plus its all-look gamma-zero certificate."""

    schema: MonotonePolyhedralInclusionSchema
    required_cell_ids: tuple[str, ...]
    all_look_inclusion_certificate: AnytimeJointSymbolicInclusionCertificate


@dataclass(frozen=True)
class VerifiedMonotonePolyhedralInclusionLook:
    """A successfully admitted non-vacuous inner/outer state at one look."""

    look: int
    required_cell_ids: tuple[str, ...]
    evidence_reference: str
    verifier: str
    assumptions: tuple[str, ...]


def _row_counter(system: RationalLinearSystem) -> Counter[tuple[tuple[object, ...], object]]:
    """Return a label-insensitive multiset of exact inequality rows."""

    return Counter(
        (inequality.coefficients, inequality.bound)
        for inequality in system.inequalities
    )


def _same_linear_system(left: RationalLinearSystem, right: RationalLinearSystem) -> bool:
    """Equality of variable order and constraint multiset, ignoring prose labels."""

    return left.variables == right.variables and _row_counter(left) == _row_counter(right)


def _is_constraint_strengthening(
    *,
    base: RationalLinearSystem,
    current: RationalLinearSystem,
) -> bool:
    """Whether every exact base row occurs in the current conjunction."""

    if base.variables != current.variables:
        return False
    base_rows = _row_counter(base)
    current_rows = _row_counter(current)
    return all(current_rows[row] >= multiplicity for row, multiplicity in base_rows.items())


def _validate_exact_cell_ids(
    mapping: Mapping[str, object],
    required_cell_ids: tuple[str, ...],
    name: str,
) -> None:
    if tuple(mapping) != required_cell_ids:
        raise ValueError(f"{name} must exactly match required_cell_ids in order")


def verify_monotone_polyhedral_inclusion_schema(
    schema: MonotonePolyhedralInclusionSchema,
    *,
    required_cell_ids: tuple[str, ...],
) -> VerifiedMonotonePolyhedralInclusionSchema:
    """Verify base inclusion once and create an all-look gamma-zero schema.

    The returned certificate is valid for every positive integer look *admitted
    through* `verify_monotone_polyhedral_inclusion_look`. It is not a claim that
    arbitrary unchecked future systems satisfy the schema.
    """

    _validate_exact_cell_ids(schema.base_queries_by_cell, required_cell_ids, "base_queries_by_cell")
    static_certificate = verify_exact_rational_joint_inclusion(
        ExactRationalJointInclusionProof(
            inner_tier_id=schema.inner_tier_id,
            outer_tier_id=schema.outer_tier_id,
            queries_by_cell=schema.base_queries_by_cell,
            assumptions=schema.assumptions,
        ),
        required_cell_ids=required_cell_ids,
    )
    all_look_certificate = AnytimeJointSymbolicInclusionCertificate(
        inner_tier_id=schema.inner_tier_id,
        outer_tier_id=schema.outer_tier_id,
        required_cell_ids=required_cell_ids,
        lower_bound=1.0,
        method=EXACT_MONOTONE_POLYHEDRAL_INCLUSION_SCHEMA_VERIFIER,
        assumptions=(
            "base rational polyhedral inclusion is exactly verified in every required cell",
            "every claimed future look is admitted by the exact monotone-polyhedral schema verifier",
            "outer systems remain fixed and each inner system retains every base inequality row",
            "each admitted inner system has an exact feasible witness",
            *schema.assumptions,
            *static_certificate.assumptions,
        ),
        evidence_reference=static_certificate.evidence_reference,
        certified_looks=None,
    )
    return VerifiedMonotonePolyhedralInclusionSchema(
        schema=schema,
        required_cell_ids=required_cell_ids,
        all_look_inclusion_certificate=all_look_certificate,
    )


def verify_monotone_polyhedral_inclusion_look(
    verified_schema: VerifiedMonotonePolyhedralInclusionSchema,
    proposed_look: MonotonePolyhedralInclusionLook,
) -> VerifiedMonotonePolyhedralInclusionLook:
    """Admit one look only when the inner system strengthens the verified base.

    This establishes non-vacuous

    ``P_inner,t subseteq P_base subseteq P_outer``

    separately for every required cell. A changed outer row, a removed base row,
    a variable-order change, or an infeasible submitted witness rejects the look.
    """

    required = verified_schema.required_cell_ids
    _validate_exact_cell_ids(proposed_look.inner_systems_by_cell, required, "inner_systems_by_cell")
    _validate_exact_cell_ids(proposed_look.outer_systems_by_cell, required, "outer_systems_by_cell")
    _validate_exact_cell_ids(proposed_look.inner_witnesses_by_cell, required, "inner_witnesses_by_cell")

    for cell_id in required:
        base_query = verified_schema.schema.base_queries_by_cell[cell_id]
        current_inner = proposed_look.inner_systems_by_cell[cell_id]
        current_outer = proposed_look.outer_systems_by_cell[cell_id]
        witness = proposed_look.inner_witnesses_by_cell[cell_id]
        if not _is_constraint_strengthening(base=base_query.inner_system, current=current_inner):
            raise ValueError("admitted inner system must retain every base inequality row")
        if not _same_linear_system(base_query.outer_system, current_outer):
            raise ValueError("admitted outer system must equal the verified fixed outer system")
        if not current_inner.holds_at(witness.values):
            raise ValueError("admitted inner witness violates a declared inner inequality")

    return VerifiedMonotonePolyhedralInclusionLook(
        look=proposed_look.look,
        required_cell_ids=required,
        evidence_reference=proposed_look.evidence_reference,
        verifier=EXACT_MONOTONE_POLYHEDRAL_INCLUSION_SCHEMA_VERIFIER,
        assumptions=(
            "this look was admitted by exact base-row accumulation and fixed-outer verification",
            "inner non-vacuity witness was verified exactly",
            *verified_schema.all_look_inclusion_certificate.assumptions,
        ),
    )
