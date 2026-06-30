"""Exact proof-carrying inclusion for rational polyhedral RACH envelopes.

This module turns the abstract inclusion-risk term ``gamma`` in symbolic
outer-envelope stability into an exactly verified statement for a restricted but
useful class of candidate sets.  A retained set is represented as a finite
conjunction of non-strict rational inequalities:

    P = {x : A x <= b}.

To prove ``P_inner subseteq P_outer``, an external backend supplies:

* one exact rational point in ``P_inner`` (so inclusion is not used vacuously);
  and
* for every outer inequality ``c_j x <= d_j``, non-negative multipliers
  ``lambda_j`` with

      lambda_j^T A = c_j^T,
      lambda_j^T b <= d_j.

Every point satisfying the inner system then satisfies the outer row, so all
outer rows follow.  Verification uses only ``fractions.Fraction`` arithmetic;
the module is a verifier, not an LP solver or proof generator.

A verified finite collection of these proofs can create a static
``JointSymbolicInclusionCertificate`` or a finite-look
``AnytimeJointSymbolicInclusionCertificate`` with lower bound 1.0.  Thus,
conditional on the trusted parser, verifier, and constraint encodings, gamma is
zero for the included cells and looks.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Mapping

from .anytime_symbolic_extension_stability import (
    AnytimeJointSymbolicInclusionCertificate,
)
from .linear_proof_verifier import (
    RationalLike,
    RationalLinearSystem,
    RationalWitness,
)
from .symbolic_universe_extension import JointSymbolicInclusionCertificate


EXACT_RATIONAL_POLYHEDRAL_INCLUSION_VERIFIER = (
    "exact-rational-polyhedral-inclusion-verifier"
)


def _fraction(value: RationalLike) -> Fraction:
    """Coerce an exact rational literal while rejecting binary floating point."""

    if isinstance(value, float):
        raise TypeError("floating-point inputs are not exact; pass Fraction or a decimal string")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise TypeError(f"cannot coerce {value!r} to an exact rational") from error


@dataclass(frozen=True)
class FarkasRowImplicationCertificate:
    """Proof that one outer inequality follows from an inner linear system.

    For ``A x <= b`` and the selected outer row ``c x <= d``, multipliers must
    satisfy ``lambda >= 0``, ``lambda^T A = c`` and ``lambda^T b <= d``.
    """

    outer_inequality_index: int
    multipliers: tuple[RationalLike, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.outer_inequality_index, int) or self.outer_inequality_index < 0:
            raise ValueError("outer_inequality_index must be a non-negative integer")
        object.__setattr__(self, "multipliers", tuple(_fraction(value) for value in self.multipliers))


@dataclass(frozen=True)
class RationalPolyhedralInclusionProof:
    """One non-vacuous, proof-carrying inclusion artifact.

    ``inner_witness`` confirms the inner retained polyhedron is non-empty.  A
    row certificate is required exactly once for every outer inequality.  An
    outer system with no inequalities is allowed and needs no row certificates;
    it still needs a valid inner witness.
    """

    inner_witness: RationalWitness
    row_certificates: tuple[FarkasRowImplicationCertificate, ...]
    evidence_reference: str
    producer: str = "external rational polyhedral backend"

    def __post_init__(self) -> None:
        if not self.evidence_reference:
            raise ValueError("a rational polyhedral inclusion proof needs an evidence_reference")
        if not self.producer:
            raise ValueError("producer must be non-empty")


@dataclass(frozen=True)
class RationalPolyhedralInclusionQuery:
    """One named claim that a non-empty inner polyhedron lies in an outer one."""

    query_id: str
    inner_system: RationalLinearSystem
    outer_system: RationalLinearSystem
    proof: RationalPolyhedralInclusionProof
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.query_id:
            raise ValueError("query_id must be non-empty")
        if self.inner_system.variables != self.outer_system.variables:
            raise ValueError("inner and outer polyhedra must use identical ordered variables")


@dataclass(frozen=True)
class VerifiedRationalPolyhedralInclusion:
    """Result of an exact successful inclusion verification."""

    query_id: str
    inner_variables: tuple[str, ...]
    inner_description: str
    outer_description: str
    evidence_reference: str
    verifier: str
    assumptions: tuple[str, ...]


@dataclass(frozen=True)
class ExactRationalJointInclusionProof:
    """Exact proof bundle for all required cells of one static universe expansion."""

    inner_tier_id: str
    outer_tier_id: str
    queries_by_cell: Mapping[str, RationalPolyhedralInclusionQuery]
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.inner_tier_id or not self.outer_tier_id:
            raise ValueError("inner_tier_id and outer_tier_id must be non-empty")
        if self.inner_tier_id == self.outer_tier_id:
            raise ValueError("inner and outer tier IDs must differ")
        if not self.queries_by_cell:
            raise ValueError("queries_by_cell must not be empty")
        if any(not cell_id for cell_id in self.queries_by_cell):
            raise ValueError("cell IDs must be non-empty")


@dataclass(frozen=True)
class ExactRationalFiniteLookInclusionProof:
    """Exact proof bundle for a fixed finite collection of sequential looks.

    This object does not prove an all-positive-integer inclusion theorem.  It
    proves only the explicit look IDs in ``queries_by_look`` and consequently
    yields a finite-scope anytime certificate.
    """

    inner_tier_id: str
    outer_tier_id: str
    queries_by_look: Mapping[int, Mapping[str, RationalPolyhedralInclusionQuery]]
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.inner_tier_id or not self.outer_tier_id:
            raise ValueError("inner_tier_id and outer_tier_id must be non-empty")
        if self.inner_tier_id == self.outer_tier_id:
            raise ValueError("inner and outer tier IDs must differ")
        if not self.queries_by_look:
            raise ValueError("queries_by_look must not be empty")
        looks = tuple(self.queries_by_look)
        if any(not isinstance(look, int) or look < 1 for look in looks):
            raise ValueError("proof-bundle look IDs must be positive integers")
        if any(not queries for queries in self.queries_by_look.values()):
            raise ValueError("every finite look needs at least one cell query")


def _verify_row_implication(
    inner_system: RationalLinearSystem,
    outer_index: int,
    certificate: FarkasRowImplicationCertificate,
) -> None:
    if certificate.outer_inequality_index != outer_index:
        raise ValueError("row certificate is attached to the wrong outer inequality index")
    multipliers = certificate.multipliers
    if len(multipliers) != len(inner_system.inequalities):
        raise ValueError("implication multiplier count must equal the inner inequality count")
    if any(multiplier < 0 for multiplier in multipliers):
        raise ValueError("implication multipliers must be non-negative")


def _verify_row_implication_against_outer(
    inner_system: RationalLinearSystem,
    outer_system: RationalLinearSystem,
    certificate: FarkasRowImplicationCertificate,
) -> None:
    outer_index = certificate.outer_inequality_index
    if outer_index >= len(outer_system.inequalities):
        raise ValueError("row certificate outer inequality index is out of range")
    _verify_row_implication(inner_system, outer_index, certificate)
    outer = outer_system.inequalities[outer_index]
    multipliers = certificate.multipliers

    for column in range(len(inner_system.variables)):
        implied_coefficient = sum(
            (
                multiplier * inequality.coefficients[column]
                for multiplier, inequality in zip(multipliers, inner_system.inequalities)
            ),
            start=Fraction(0),
        )
        if implied_coefficient != outer.coefficients[column]:
            raise ValueError("implication certificate does not derive the outer row coefficients")

    implied_bound = sum(
        (
            multiplier * inequality.bound
            for multiplier, inequality in zip(multipliers, inner_system.inequalities)
        ),
        start=Fraction(0),
    )
    if implied_bound > outer.bound:
        raise ValueError("implication certificate derives a weaker bound than the outer row")


def verify_rational_polyhedral_inclusion(
    query: RationalPolyhedralInclusionQuery,
) -> VerifiedRationalPolyhedralInclusion:
    """Verify ``inner_system subseteq outer_system`` with exact rational arithmetic.

    The verifier rejects malformed purported proofs. It never turns an absent or
    invalid proof into a decisive inclusion claim. The theorem is conditional on
    the trusted rational parser, verifier implementation, and caller-supplied
    encoding of the intended inner and outer retained sets.
    """

    if not query.inner_system.holds_at(query.proof.inner_witness.values):
        raise ValueError("inner nonempty witness violates a declared inner inequality")

    certificates = query.proof.row_certificates
    expected_indices = set(range(len(query.outer_system.inequalities)))
    observed_indices = {certificate.outer_inequality_index for certificate in certificates}
    if len(observed_indices) != len(certificates):
        raise ValueError("outer inequality row certificates must be unique")
    if observed_indices != expected_indices:
        raise ValueError("one row implication certificate is required for every outer inequality")

    for certificate in certificates:
        _verify_row_implication_against_outer(
            query.inner_system,
            query.outer_system,
            certificate,
        )

    return VerifiedRationalPolyhedralInclusion(
        query_id=query.query_id,
        inner_variables=query.inner_system.variables,
        inner_description=query.inner_system.description,
        outer_description=query.outer_system.description,
        evidence_reference=query.proof.evidence_reference,
        verifier=EXACT_RATIONAL_POLYHEDRAL_INCLUSION_VERIFIER,
        assumptions=(
            "rational parser and polyhedral inclusion verifier are trusted",
            "inner and outer linear systems encode the declared retained sets",
            "inner nonempty witness was verified exactly",
            *query.assumptions,
        ),
    )


def verify_exact_rational_joint_inclusion(
    proof_bundle: ExactRationalJointInclusionProof,
    *,
    required_cell_ids: tuple[str, ...],
) -> JointSymbolicInclusionCertificate:
    """Verify every required static cell and return a gamma-zero certificate."""

    if tuple(proof_bundle.queries_by_cell) != required_cell_ids:
        raise ValueError("exact rational proof bundle cell IDs must exactly match required_cell_ids in order")
    verified = tuple(
        verify_rational_polyhedral_inclusion(proof_bundle.queries_by_cell[cell_id])
        for cell_id in required_cell_ids
    )
    return JointSymbolicInclusionCertificate(
        inner_tier_id=proof_bundle.inner_tier_id,
        outer_tier_id=proof_bundle.outer_tier_id,
        required_cell_ids=required_cell_ids,
        lower_bound=1.0,
        method=EXACT_RATIONAL_POLYHEDRAL_INCLUSION_VERIFIER,
        assumptions=(
            "every required cell has an exact non-vacuous rational polyhedral inclusion proof",
            *proof_bundle.assumptions,
            *(assumption for result in verified for assumption in result.assumptions),
        ),
        evidence_reference="; ".join(result.evidence_reference for result in verified),
    )


def verify_exact_rational_finite_look_inclusion(
    proof_bundle: ExactRationalFiniteLookInclusionProof,
    *,
    required_cell_ids: tuple[str, ...],
) -> AnytimeJointSymbolicInclusionCertificate:
    """Verify a finite schedule of cellwise proofs and return an anytime gamma-zero certificate.

    The returned certificate covers exactly the predeclared look IDs.  A finite
    proof bundle cannot certify unbounded sequential monitoring.
    """

    look_ids = tuple(proof_bundle.queries_by_look)
    if tuple(sorted(look_ids)) != look_ids:
        raise ValueError("finite-look proof bundle look IDs must be sorted increasingly")
    verified_by_look = {
        look: verify_exact_rational_joint_inclusion(
            ExactRationalJointInclusionProof(
                inner_tier_id=proof_bundle.inner_tier_id,
                outer_tier_id=proof_bundle.outer_tier_id,
                queries_by_cell=queries_by_cell,
                assumptions=proof_bundle.assumptions,
            ),
            required_cell_ids=required_cell_ids,
        )
        for look, queries_by_cell in proof_bundle.queries_by_look.items()
    }
    return AnytimeJointSymbolicInclusionCertificate(
        inner_tier_id=proof_bundle.inner_tier_id,
        outer_tier_id=proof_bundle.outer_tier_id,
        required_cell_ids=required_cell_ids,
        lower_bound=1.0,
        method=EXACT_RATIONAL_POLYHEDRAL_INCLUSION_VERIFIER,
        assumptions=(
            "every certified look has exact non-vacuous rational polyhedral inclusion proofs",
            *proof_bundle.assumptions,
            *(assumption for certificate in verified_by_look.values() for assumption in certificate.assumptions),
        ),
        evidence_reference=" | ".join(
            f"look {look}: {certificate.evidence_reference}"
            for look, certificate in verified_by_look.items()
        ),
        certified_looks=look_ids,
    )
