"""Exact-rational proof verification for linear symbolic RACH queries.

This module is deliberately a *verifier*, not a linear-programming solver.  An
external backend may search for a feasible point or an infeasibility proof, but
RACH accepts a decisive linear feasibility result only after checking a compact
certificate with exact ``fractions.Fraction`` arithmetic:

* ``SAT``: a rational witness satisfies every declared inequality;
* ``UNSAT``: non-negative Farkas multipliers combine the inequalities into
  ``0 <= c`` with ``c < 0``; and
* ``UNKNOWN``: no decisive certificate is supplied.

The verifier then adapts those checked results into the generic symbolic
candidate-set layer.  This provides a concrete proof-carrying backend for
rational polyhedral candidate sets while keeping raw data, optimisation search,
and domain models outside RACH.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Mapping

from .admissibility import CoverageMode
from .symbolic_candidate_sets import (
    FeasibilityCertificate,
    FeasibilityStatus,
    SymbolicConfidenceSetCell,
    SymbolicMotifQueries,
)


RationalLike = Fraction | int | str


def _fraction(value: RationalLike) -> Fraction:
    """Coerce an exact rational literal while rejecting binary floating point."""

    if isinstance(value, float):
        raise TypeError("floating-point inputs are not exact; pass Fraction or a decimal string")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise TypeError(f"cannot coerce {value!r} to an exact rational") from error


@dataclass(frozen=True)
class LinearInequality:
    """One exact rational linear inequality ``coefficients · x <= bound``."""

    coefficients: tuple[RationalLike, ...]
    bound: RationalLike
    label: str = ""

    def __post_init__(self) -> None:
        coefficients = tuple(_fraction(value) for value in self.coefficients)
        if not coefficients:
            raise ValueError("a linear inequality needs at least one coefficient")
        object.__setattr__(self, "coefficients", coefficients)
        object.__setattr__(self, "bound", _fraction(self.bound))

    def left_hand_side(self, point: tuple[Fraction, ...]) -> Fraction:
        return sum(
            (coefficient * value for coefficient, value in zip(self.coefficients, point)),
            start=Fraction(0),
        )

    def holds_at(self, point: tuple[Fraction, ...]) -> bool:
        return self.left_hand_side(point) <= self.bound


@dataclass(frozen=True)
class RationalLinearSystem:
    """A finite conjunction of exact rational inequalities over named variables."""

    variables: tuple[str, ...]
    inequalities: tuple[LinearInequality, ...]
    description: str = ""

    def __post_init__(self) -> None:
        if not self.variables:
            raise ValueError("at least one linear variable is required")
        if len(set(self.variables)) != len(self.variables) or any(not name for name in self.variables):
            raise ValueError("linear variable names must be unique and non-empty")
        for inequality in self.inequalities:
            if len(inequality.coefficients) != len(self.variables):
                raise ValueError("every inequality must have one coefficient per variable")

    def coerce_point(self, point: Iterable[RationalLike]) -> tuple[Fraction, ...]:
        coerced = tuple(_fraction(value) for value in point)
        if len(coerced) != len(self.variables):
            raise ValueError("linear witness dimension does not match the system")
        return coerced

    def holds_at(self, point: Iterable[RationalLike]) -> bool:
        coerced = self.coerce_point(point)
        return all(inequality.holds_at(coerced) for inequality in self.inequalities)


@dataclass(frozen=True)
class RationalWitness:
    """A proposed exact feasible point for a rational linear system."""

    values: tuple[RationalLike, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", tuple(_fraction(value) for value in self.values))


@dataclass(frozen=True)
class FarkasInfeasibilityCertificate:
    """A non-negative Farkas multiplier vector for ``A x <= b`` infeasibility.

    The verifier checks ``lambda >= 0``, ``lambda^T A = 0``, and
    ``lambda^T b < 0``.  Combining the original inequalities then yields the
    contradiction ``0 <= lambda^T b < 0``.
    """

    multipliers: tuple[RationalLike, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "multipliers", tuple(_fraction(value) for value in self.multipliers))


@dataclass(frozen=True)
class LinearFeasibilityProof:
    """One proof-carrying linear feasibility result.

    ``SAT`` requires a ``RationalWitness``; ``UNSAT`` requires a
    ``FarkasInfeasibilityCertificate``; and ``UNKNOWN`` carries neither.  The
    proof object alone is not trusted: use ``verify_linear_query`` before
    converting it into a generic RACH feasibility certificate.
    """

    status: FeasibilityStatus
    evidence_reference: str = ""
    witness: RationalWitness | None = None
    farkas: FarkasInfeasibilityCertificate | None = None
    producer: str = "external linear backend"

    def __post_init__(self) -> None:
        if not isinstance(self.status, FeasibilityStatus):
            raise ValueError("status must be a FeasibilityStatus")
        if self.status is FeasibilityStatus.SAT:
            if self.witness is None or self.farkas is not None:
                raise ValueError("SAT proof requires exactly one rational witness")
        elif self.status is FeasibilityStatus.UNSAT:
            if self.farkas is None or self.witness is not None:
                raise ValueError("UNSAT proof requires exactly one Farkas certificate")
        else:
            if self.witness is not None or self.farkas is not None:
                raise ValueError("UNKNOWN proof must not carry a witness or Farkas certificate")
        if self.status is not FeasibilityStatus.UNKNOWN and not self.evidence_reference:
            raise ValueError("decisive linear proofs require an evidence_reference")


@dataclass(frozen=True)
class LinearFeasibilityQuery:
    """A named rational linear feasibility query and its externally supplied proof."""

    query_id: str
    system: RationalLinearSystem
    proof: LinearFeasibilityProof
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.query_id:
            raise ValueError("query_id must be non-empty")


@dataclass(frozen=True)
class LinearMotifQueryBundle:
    """Verified linear query inputs for one retained set and one Boolean motif.

    The three systems must use the same ordered variable vocabulary.  Their
    semantic relationship—base retained set, motif-active restriction, and
    motif-inactive restriction—must be declared by the caller and recorded in
    their query IDs.  The verifier proves each linear result, but it cannot infer
    an intended motif predicate from arbitrary inequalities.
    """

    nonempty: LinearFeasibilityQuery
    active: LinearFeasibilityQuery
    inactive: LinearFeasibilityQuery

    def __post_init__(self) -> None:
        variables = self.nonempty.system.variables
        if self.active.system.variables != variables or self.inactive.system.variables != variables:
            raise ValueError("nonempty, active, and inactive linear queries need identical variables")


def _verify_farkas(system: RationalLinearSystem, certificate: FarkasInfeasibilityCertificate) -> None:
    multipliers = certificate.multipliers
    if len(multipliers) != len(system.inequalities):
        raise ValueError("Farkas multiplier count must equal the number of inequalities")
    if any(multiplier < 0 for multiplier in multipliers):
        raise ValueError("Farkas multipliers must be non-negative")

    for column in range(len(system.variables)):
        coefficient_sum = sum(
            (
                multiplier * inequality.coefficients[column]
                for multiplier, inequality in zip(multipliers, system.inequalities)
            ),
            start=Fraction(0),
        )
        if coefficient_sum != 0:
            raise ValueError("Farkas certificate does not eliminate every variable")

    bound_sum = sum(
        (
            multiplier * inequality.bound
            for multiplier, inequality in zip(multipliers, system.inequalities)
        ),
        start=Fraction(0),
    )
    if bound_sum >= 0:
        raise ValueError("Farkas certificate must derive a strictly negative constant bound")


def verify_linear_query(query: LinearFeasibilityQuery) -> FeasibilityCertificate:
    """Verify an exact linear proof and return a generic symbolic certificate.

    A returned `SAT` or `UNSAT` object has been checked with exact rational
    arithmetic.  Treat it as proof-carrying only under the stated trust boundary:
    the verifier implementation, rational parser, and query encoding must be
    trusted.  Invalid proofs raise `ValueError`; they are not downgraded to
    `UNKNOWN` because the caller supplied a malformed purported certificate.
    """

    proof = query.proof
    if proof.status is FeasibilityStatus.SAT:
        assert proof.witness is not None
        if not query.system.holds_at(proof.witness.values):
            raise ValueError("rational SAT witness violates a declared inequality")
    elif proof.status is FeasibilityStatus.UNSAT:
        assert proof.farkas is not None
        _verify_farkas(query.system, proof.farkas)

    return FeasibilityCertificate(
        query_description=query.query_id,
        status=proof.status,
        evidence_reference=proof.evidence_reference,
        solver="exact-rational-linear-proof-verifier",
        assumptions=(
            "rational parser and proof verifier are trusted",
            "linear query encodes the declared retained-set predicate",
            *query.assumptions,
        ),
    )


def verify_linear_motif_queries(bundle: LinearMotifQueryBundle) -> SymbolicMotifQueries:
    """Verify a three-query bundle before passing it to symbolic RACH."""

    return SymbolicMotifQueries(
        nonempty=verify_linear_query(bundle.nonempty),
        active=verify_linear_query(bundle.active),
        inactive=verify_linear_query(bundle.inactive),
    )


def linear_bundles_to_symbolic_cell(
    *,
    cell_id: str,
    description: str,
    motif_bundles: Mapping[str, LinearMotifQueryBundle],
    required: bool = True,
    coverage_mode: CoverageMode = CoverageMode.SOLVER_BACKED,
) -> SymbolicConfidenceSetCell:
    """Build one symbolic RACH cell only from verified linear proof bundles."""

    if not motif_bundles:
        raise ValueError("at least one motif proof bundle is required")
    return SymbolicConfidenceSetCell(
        cell_id=cell_id,
        description=description,
        motif_queries={
            motif: verify_linear_motif_queries(bundle)
            for motif, bundle in motif_bundles.items()
        },
        required=required,
        coverage_mode=coverage_mode,
    )
