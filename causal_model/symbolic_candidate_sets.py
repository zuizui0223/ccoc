"""Solver-backed RACH classification over arbitrary candidate spaces.

The finite candidate-enumeration APIs are useful for small auditable universes,
but the confidence-set lifting proof itself does not require a finite or
countable parameter space.  This module represents a retained candidate set
symbolically through feasibility queries:

* Is the retained set non-empty?
* Does it contain a candidate with a motif?
* Does it contain a candidate without that motif?

A SAT/SMT/constraint/interval/quantifier-elimination backend, or any other
external solver, may answer those queries as SAT, UNSAT, or UNKNOWN.  RACH uses
only declared SAT/UNSAT certificates; UNKNOWN is preserved as unsupported
rather than silently turned into a causal conclusion.

No solver is bundled and no raw data are accepted.  The module records and
combines externally established candidate-set coverage and solver-semantic
validity certificates.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping

from .admissibility import ClaimCoverage, CoverageMode, MotifStatus


def _unit_interval(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")


class FeasibilityStatus(str, Enum):
    """A solver answer to an existential feasibility query."""

    SAT = "sat"
    UNSAT = "unsat"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class FeasibilityCertificate:
    """One auditable SAT/UNSAT/UNKNOWN answer for a symbolic feasibility query.

    For `SAT`, ``evidence_reference`` should identify a witness, model, interval
    enclosure, or externally inspectable result.  For `UNSAT`, it should identify
    a proof, certificate, or solver artifact.  `UNKNOWN` intentionally carries no
    decisive semantic claim and therefore does not require such evidence.
    """

    query_description: str
    status: FeasibilityStatus
    evidence_reference: str = ""
    solver: str = ""
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.query_description:
            raise ValueError("query_description must be non-empty")
        if not isinstance(self.status, FeasibilityStatus):
            raise ValueError("status must be a FeasibilityStatus")
        if self.status is not FeasibilityStatus.UNKNOWN and not self.evidence_reference:
            raise ValueError("SAT and UNSAT certificates require an evidence_reference")


@dataclass(frozen=True)
class SymbolicMotifQueries:
    """Feasibility queries defining one motif's status in one retained set.

    Semantically, for retained set ``C`` and motif predicate ``m``:

    * ``nonempty`` asks whether ``C`` is non-empty;
    * ``active`` asks whether ``C ∩ {theta : m(theta)}`` is non-empty; and
    * ``inactive`` asks whether ``C ∩ {theta : not m(theta)}`` is non-empty.

    The data structure does not evaluate these queries; it checks only elementary
    logical consistency among the reported solver answers.
    """

    nonempty: FeasibilityCertificate
    active: FeasibilityCertificate
    inactive: FeasibilityCertificate

    def __post_init__(self) -> None:
        if self.nonempty.status is FeasibilityStatus.UNSAT:
            if self.active.status is FeasibilityStatus.SAT or self.inactive.status is FeasibilityStatus.SAT:
                raise ValueError("an empty retained set cannot have an active or inactive witness")
        if self.nonempty.status is FeasibilityStatus.UNKNOWN:
            if self.active.status is FeasibilityStatus.SAT or self.inactive.status is FeasibilityStatus.SAT:
                raise ValueError("an active or inactive witness also proves retained-set non-emptiness")
        if self.nonempty.status is FeasibilityStatus.SAT:
            if self.active.status is FeasibilityStatus.UNSAT and self.inactive.status is FeasibilityStatus.UNSAT:
                raise ValueError("a non-empty retained set cannot exclude both motif values")


@dataclass(frozen=True)
class SymbolicCandidateSpace:
    """A possibly infinite candidate space with a finite declared motif vocabulary.

    The candidate space is intentionally descriptive rather than enumerable. It
    may be continuous, countably infinite, mixed discrete/continuous, or an
    implicit solver-defined domain. Each motif is a Boolean predicate over that
    space, specified externally in the solver query descriptions.
    """

    space_description: str
    motifs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.space_description:
            raise ValueError("space_description must be non-empty")
        if not self.motifs:
            raise ValueError("at least one motif is required")
        if len(set(self.motifs)) != len(self.motifs) or any(not motif for motif in self.motifs):
            raise ValueError("motifs must be unique non-empty names")


@dataclass(frozen=True)
class SymbolicConfidenceSetCell:
    """One solver-represented retained candidate set in a robustness cell."""

    cell_id: str
    description: str
    motif_queries: Mapping[str, SymbolicMotifQueries]
    required: bool = True
    coverage_mode: CoverageMode = CoverageMode.SOLVER_BACKED

    def __post_init__(self) -> None:
        if not self.cell_id:
            raise ValueError("cell_id must be non-empty")
        if not self.description:
            raise ValueError("description must be non-empty")
        if not isinstance(self.coverage_mode, CoverageMode):
            raise ValueError("coverage_mode must be a CoverageMode")


@dataclass(frozen=True)
class SymbolicMotifClassification:
    """One motif's symbolic RACH status plus per-cell solver status."""

    motif: str
    status: MotifStatus
    cell_statuses: Mapping[str, MotifStatus]
    unsupported_required_cells: tuple[str, ...]
    claim_coverage: ClaimCoverage
    required_cell_coverage: Mapping[str, CoverageMode]


@dataclass(frozen=True)
class SymbolicAdmissibilityReport:
    """RACH classifications derived without candidate enumeration."""

    space_description: str
    motifs: tuple[str, ...]
    classifications: Mapping[str, SymbolicMotifClassification]
    required_cells: tuple[str, ...]
    required_cell_coverage: Mapping[str, CoverageMode]

    def by_status(self, status: MotifStatus) -> tuple[str, ...]:
        return tuple(
            motif
            for motif in self.motifs
            if self.classifications[motif].status is status
        )


@dataclass(frozen=True)
class SymbolicJointCoverageCertificate:
    """External coverage statement for the true point in symbolic retained sets.

    The intended assertion is

    ``P(true candidate belongs to every required symbolic retained set) >= lower_bound``.

    This is the arbitrary-space analogue of a finite candidate confidence-set
    certificate. It can be supplied by any valid external statistical method.
    """

    true_candidate_label: str
    required_cell_ids: tuple[str, ...]
    lower_bound: float
    method: str
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.true_candidate_label:
            raise ValueError("true_candidate_label must be non-empty")
        if not self.required_cell_ids:
            raise ValueError("required_cell_ids must not be empty")
        if len(set(self.required_cell_ids)) != len(self.required_cell_ids):
            raise ValueError("required_cell_ids must be unique")
        _unit_interval(self.lower_bound, "lower_bound")
        if not self.method:
            raise ValueError("method must be non-empty")

    @property
    def miscoverage_upper_bound(self) -> float:
        return 1.0 - self.lower_bound


@dataclass(frozen=True)
class SolverSemanticValidityCertificate:
    """External validity statement for all decisive solver answers used by RACH.

    The intended assertion is that every `SAT`/`UNSAT` result used for the named
    motifs and required cells has its advertised semantic meaning with probability
    at least ``lower_bound``.  A deterministic proof-carrying solver and trusted
    verifier should use ``lower_bound=1.0``.  A randomized, approximate, or
    externally audited backend can state a lower lower bound.

    No independence from the statistical coverage event is assumed or required;
    the lifted guarantee uses a union bound.
    """

    required_cell_ids: tuple[str, ...]
    motifs: tuple[str, ...]
    lower_bound: float
    method: str
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.required_cell_ids:
            raise ValueError("required_cell_ids must not be empty")
        if len(set(self.required_cell_ids)) != len(self.required_cell_ids):
            raise ValueError("required_cell_ids must be unique")
        if not self.motifs:
            raise ValueError("motifs must not be empty")
        if len(set(self.motifs)) != len(self.motifs):
            raise ValueError("motifs must be unique")
        _unit_interval(self.lower_bound, "lower_bound")
        if not self.method:
            raise ValueError("method must be non-empty")

    @property
    def semantic_failure_upper_bound(self) -> float:
        return 1.0 - self.lower_bound


@dataclass(frozen=True)
class SymbolicRACHSoundnessGuarantee:
    """False-decisive bound for a potentially infinite symbolic candidate space."""

    true_candidate_label: str
    statistical_coverage_lower_bound: float
    solver_semantic_validity_lower_bound: float
    statistical_miscoverage_upper_bound: float
    solver_semantic_failure_upper_bound: float
    family_wise_false_decisive_upper_bound: float
    required_cell_ids: tuple[str, ...]
    motifs: tuple[str, ...]
    coverage_method: str
    solver_method: str
    assumptions: tuple[str, ...]


def _cell_motif_status(queries: SymbolicMotifQueries) -> MotifStatus:
    """Classify one motif in one symbolic retained set conservatively."""

    if queries.nonempty.status is not FeasibilityStatus.SAT:
        return MotifStatus.UNSUPPORTED
    if queries.inactive.status is FeasibilityStatus.UNSAT:
        return MotifStatus.INVARIANT
    if queries.active.status is FeasibilityStatus.UNSAT:
        return MotifStatus.EXCLUDED
    if (
        queries.active.status is FeasibilityStatus.SAT
        and queries.inactive.status is FeasibilityStatus.SAT
    ):
        return MotifStatus.UNRESOLVED
    return MotifStatus.UNSUPPORTED


def _validate_symbolic_cells(
    space: SymbolicCandidateSpace,
    cells: Iterable[SymbolicConfidenceSetCell],
) -> tuple[SymbolicConfidenceSetCell, ...]:
    cell_tuple = tuple(cells)
    if not cell_tuple:
        raise ValueError("at least one symbolic confidence-set cell is required")
    ids = [cell.cell_id for cell in cell_tuple]
    if len(set(ids)) != len(ids):
        raise ValueError("symbolic confidence-set cell IDs must be unique")
    if not any(cell.required for cell in cell_tuple):
        raise ValueError("at least one required symbolic confidence-set cell is required")
    motif_set = set(space.motifs)
    for cell in cell_tuple:
        if set(cell.motif_queries) != motif_set:
            raise ValueError(
                f"cell {cell.cell_id!r} must provide exactly one query bundle for every declared motif"
            )
    return cell_tuple


def classify_symbolic_candidate_sets(
    space: SymbolicCandidateSpace,
    cells: Iterable[SymbolicConfidenceSetCell],
) -> SymbolicAdmissibilityReport:
    """Classify motifs from solver-backed feasible-set queries without enumeration.

    `INVARIANT` requires a non-empty certificate and an `UNSAT` certificate for
    the motif-inactive subset in every required cell. `EXCLUDED` is symmetric.
    `UNRESOLVED` requires witnessed active and inactive candidates in at least one
    required-cell pattern that prevents a universal conclusion. Any missing,
    unknown, or empty required query yields `UNSUPPORTED` rather than a decisive
    result.
    """

    cell_tuple = _validate_symbolic_cells(space, cells)
    required = tuple(cell for cell in cell_tuple if cell.required)
    required_coverage = {cell.cell_id: cell.coverage_mode for cell in required}

    classifications: dict[str, SymbolicMotifClassification] = {}
    for motif in space.motifs:
        cell_statuses = {
            cell.cell_id: _cell_motif_status(cell.motif_queries[motif])
            for cell in cell_tuple
        }
        unsupported_required = tuple(
            cell.cell_id
            for cell in required
            if cell_statuses[cell.cell_id] is MotifStatus.UNSUPPORTED
        )
        if unsupported_required:
            overall = MotifStatus.UNSUPPORTED
            coverage = ClaimCoverage.UNSUPPORTED
        else:
            required_statuses = [cell_statuses[cell.cell_id] for cell in required]
            if all(status is MotifStatus.INVARIANT for status in required_statuses):
                overall = MotifStatus.INVARIANT
            elif all(status is MotifStatus.EXCLUDED for status in required_statuses):
                overall = MotifStatus.EXCLUDED
            else:
                overall = MotifStatus.UNRESOLVED
            coverage = (
                ClaimCoverage.COMPLETE
                if all(cell.coverage_mode is not CoverageMode.SAMPLED for cell in required)
                else ClaimCoverage.SAMPLED
            )
        classifications[motif] = SymbolicMotifClassification(
            motif=motif,
            status=overall,
            cell_statuses=cell_statuses,
            unsupported_required_cells=unsupported_required,
            claim_coverage=coverage,
            required_cell_coverage=required_coverage,
        )
    return SymbolicAdmissibilityReport(
        space_description=space.space_description,
        motifs=space.motifs,
        classifications=classifications,
        required_cells=tuple(cell.cell_id for cell in required),
        required_cell_coverage=required_coverage,
    )


def symbolic_soundness_guarantee(
    space: SymbolicCandidateSpace,
    coverage_certificate: SymbolicJointCoverageCertificate,
    solver_certificate: SolverSemanticValidityCertificate,
) -> SymbolicRACHSoundnessGuarantee:
    """Combine symbolic-set coverage and solver validity into RACH soundness.

    **Symbolic candidate-set lifting theorem.** Let ``Theta`` be any candidate
    space, possibly uncountable, and let every required retained set ``C_r(Z)``
    be represented through sound feasibility queries. If the true candidate is in
    every required retained set with probability at least ``1 - alpha`` and every
    decisive solver answer is semantically valid with probability at least
    ``1 - beta``, then

    ``P(any false RACH INVARIANT or EXCLUDED conclusion) <= min(1, alpha + beta)``.

    No independence between data coverage and solver validity is needed. With a
    deterministic proof-carrying solver, ``beta = 0`` and this reduces to the
    ordinary confidence-set lifting bound.
    """

    required = tuple(space for space in coverage_certificate.required_cell_ids)
    if set(required) != set(solver_certificate.required_cell_ids):
        raise ValueError("coverage and solver certificates must name the same required cell IDs")
    if set(space.motifs) != set(solver_certificate.motifs):
        raise ValueError("solver certificate motifs must match the symbolic candidate space")
    alpha = coverage_certificate.miscoverage_upper_bound
    beta = solver_certificate.semantic_failure_upper_bound
    bound = min(1.0, alpha + beta)
    return SymbolicRACHSoundnessGuarantee(
        true_candidate_label=coverage_certificate.true_candidate_label,
        statistical_coverage_lower_bound=coverage_certificate.lower_bound,
        solver_semantic_validity_lower_bound=solver_certificate.lower_bound,
        statistical_miscoverage_upper_bound=alpha,
        solver_semantic_failure_upper_bound=beta,
        family_wise_false_decisive_upper_bound=bound,
        required_cell_ids=coverage_certificate.required_cell_ids,
        motifs=space.motifs,
        coverage_method=coverage_certificate.method,
        solver_method=solver_certificate.method,
        assumptions=coverage_certificate.assumptions + solver_certificate.assumptions,
    )
