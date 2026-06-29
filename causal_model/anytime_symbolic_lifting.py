"""Anytime symbolic candidate-set lifting for arbitrary spaces.

This module unifies RACH's two general extensions:

* time-uniform confidence-set lifting for arbitrary sequential random data; and
* symbolic candidate-set lifting over potentially continuous or uncountable
  candidate spaces represented by solver feasibility certificates.

At each analysis look, an external procedure supplies a symbolic retained set
for every required cell.  The procedure separately certifies (i) time-uniform
statistical retention of the true candidate and (ii) time-uniform semantic
validity of every decisive solver certificate used by RACH.  RACH then controls
false `INVARIANT` / `EXCLUDED` conclusions across all certified looks, all
motifs, and any data-dependent stopping time in scope.

No raw data, solver search, independence assumption, or candidate enumeration is
implemented here.  The module is a theorem-level lifting and audit layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .admissibility import MotifStatus
from .symbolic_candidate_sets import (
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    classify_symbolic_candidate_sets,
)


def _unit_interval(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")


def _validate_look_scope(looks: tuple[int, ...] | None, name: str) -> None:
    if looks is None:
        return
    if not looks:
        raise ValueError(f"{name} must be non-empty when provided")
    if any(not isinstance(look, int) or look < 1 for look in looks):
        raise ValueError(f"{name} must contain positive integers")
    if len(set(looks)) != len(looks):
        raise ValueError(f"{name} must be unique")


@dataclass(frozen=True)
class SequentialSymbolicConfidenceSetSnapshot:
    """Solver-backed retained sets at one positive integer analysis look."""

    look: int
    cells: tuple[SymbolicConfidenceSetCell, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("look must be a positive integer")
        if not self.cells:
            raise ValueError("each symbolic sequential snapshot needs at least one cell")


@dataclass(frozen=True)
class AnytimeSymbolicJointCoverageCertificate:
    """External all-look statistical coverage for symbolic retained sets.

    The certificate asserts

    ``P(for every certified look t, theta_star belongs to every required C_{r,t}) >= lower_bound``.

    It does not require a finite, countable, or explicitly enumerated candidate
    space.  With ``certified_looks=None``, the assertion covers every positive
    integer look; otherwise it covers exactly the declared finite look scope.
    """

    true_candidate_label: str
    required_cell_ids: tuple[str, ...]
    lower_bound: float
    method: str
    assumptions: tuple[str, ...] = ()
    certified_looks: tuple[int, ...] | None = None

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
        _validate_look_scope(self.certified_looks, "certified_looks")

    @property
    def miscoverage_upper_bound(self) -> float:
        return 1.0 - self.lower_bound

    def covers_look(self, look: int) -> bool:
        return self.certified_looks is None or look in self.certified_looks


@dataclass(frozen=True)
class AnytimeSolverSemanticValidityCertificate:
    """External all-look validity guarantee for decisive symbolic solver answers.

    The certificate asserts that every SAT/UNSAT statement used to issue a
    decisive RACH status is semantically valid over every required cell, every
    declared motif, and every certified look with probability at least
    ``lower_bound``.  A deterministic proof-carrying verifier may use 1.0.

    This is distinct from statistical retained-set coverage and may be dependent
    on it.  The theorem uses a union bound and assumes no independence.
    """

    required_cell_ids: tuple[str, ...]
    motifs: tuple[str, ...]
    lower_bound: float
    method: str
    assumptions: tuple[str, ...] = ()
    certified_looks: tuple[int, ...] | None = None

    def __post_init__(self) -> None:
        if not self.required_cell_ids:
            raise ValueError("required_cell_ids must not be empty")
        if len(set(self.required_cell_ids)) != len(self.required_cell_ids):
            raise ValueError("required_cell_ids must be unique")
        if not self.motifs:
            raise ValueError("motifs must not be empty")
        if len(set(self.motifs)) != len(self.motifs) or any(not motif for motif in self.motifs):
            raise ValueError("motifs must be unique non-empty names")
        _unit_interval(self.lower_bound, "lower_bound")
        if not self.method:
            raise ValueError("method must be non-empty")
        _validate_look_scope(self.certified_looks, "certified_looks")

    @property
    def semantic_failure_upper_bound(self) -> float:
        return 1.0 - self.lower_bound

    def covers_look(self, look: int) -> bool:
        return self.certified_looks is None or look in self.certified_looks


@dataclass(frozen=True)
class AnytimeSymbolicLiftingWitness:
    """One realized symbolic trajectory audited against declared truth metadata.

    This is a deterministic theorem witness, not a statistical estimator.  The
    caller supplies whether the true point was retained and whether decisive solver
    semantics were valid at each realized look.  Those facts would be guaranteed
    probabilistically by the two external certificates in a genuine application.
    """

    true_candidate_label: str
    true_active_motifs: frozenset[str]
    true_retained_by_look: Mapping[int, bool]
    decisive_solver_semantics_valid_by_look: Mapping[int, bool]
    false_decisive_motifs_by_look: Mapping[int, tuple[str, ...]]

    @property
    def joint_good_event_at_all_looks(self) -> bool:
        return all(
            self.true_retained_by_look[look]
            and self.decisive_solver_semantics_valid_by_look[look]
            for look in self.true_retained_by_look
        )

    @property
    def false_decisive_looks(self) -> tuple[int, ...]:
        return tuple(
            look
            for look, motifs in self.false_decisive_motifs_by_look.items()
            if motifs
        )

    @property
    def any_false_decisive_claim(self) -> bool:
        return bool(self.false_decisive_looks)

    @property
    def implication_holds(self) -> bool:
        """Whether false decisiveness implies failure of retention or solver validity."""

        return not self.any_false_decisive_claim or not self.joint_good_event_at_all_looks


@dataclass(frozen=True)
class AnytimeSymbolicRACHSoundnessGuarantee:
    """Time-uniform soundness bound for arbitrary symbolic candidate spaces."""

    true_candidate_label: str
    statistical_time_uniform_coverage_lower_bound: float
    solver_time_uniform_validity_lower_bound: float
    statistical_miscoverage_upper_bound: float
    solver_semantic_failure_upper_bound: float
    time_uniform_family_wise_false_decisive_upper_bound: float
    stopping_time_false_decisive_upper_bound: float
    required_cell_ids: tuple[str, ...]
    motifs: tuple[str, ...]
    certified_looks: tuple[int, ...] | None
    coverage_method: str
    solver_method: str
    assumptions: tuple[str, ...]


def _required_cell_ids(snapshot: SequentialSymbolicConfidenceSetSnapshot) -> tuple[str, ...]:
    return tuple(cell.cell_id for cell in snapshot.cells if cell.required)


def _combined_scope(
    coverage: AnytimeSymbolicJointCoverageCertificate,
    solver: AnytimeSolverSemanticValidityCertificate,
) -> tuple[int, ...] | None:
    """Return the exact common scope, allowing one certificate to be all-look."""

    coverage_scope = coverage.certified_looks
    solver_scope = solver.certified_looks
    if coverage_scope is None and solver_scope is None:
        return None
    if coverage_scope is None:
        return tuple(sorted(solver_scope or ()))
    if solver_scope is None:
        return tuple(sorted(coverage_scope))
    if set(coverage_scope) != set(solver_scope):
        raise ValueError("coverage and solver certificates must cover the same finite look scope")
    return tuple(sorted(coverage_scope))


def _validate_snapshots(
    space: SymbolicCandidateSpace,
    snapshots: Iterable[SequentialSymbolicConfidenceSetSnapshot],
    *,
    expected_required_cell_ids: tuple[str, ...] | None = None,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate | None = None,
    solver_certificate: AnytimeSolverSemanticValidityCertificate | None = None,
) -> tuple[SequentialSymbolicConfidenceSetSnapshot, ...]:
    snapshot_tuple = tuple(snapshots)
    if not snapshot_tuple:
        raise ValueError("at least one symbolic sequential snapshot is required")
    looks = tuple(snapshot.look for snapshot in snapshot_tuple)
    if len(set(looks)) != len(looks):
        raise ValueError("symbolic sequential look indices must be unique")
    if looks != tuple(sorted(looks)):
        raise ValueError("symbolic sequential snapshots must be sorted by increasing look")

    first_required = _required_cell_ids(snapshot_tuple[0])
    if not first_required:
        raise ValueError("each symbolic sequential snapshot needs a required cell")
    expected = expected_required_cell_ids or first_required
    expected_set = set(expected)
    if not expected_set:
        raise ValueError("expected required cell IDs must not be empty")

    for snapshot in snapshot_tuple:
        classify_symbolic_candidate_sets(space, snapshot.cells)
        if set(_required_cell_ids(snapshot)) != expected_set:
            raise ValueError("every symbolic sequential snapshot must use the same required cell IDs")
        if coverage_certificate is not None and not coverage_certificate.covers_look(snapshot.look):
            raise ValueError(
                f"look {snapshot.look} is outside the coverage certificate's declared scope"
            )
        if solver_certificate is not None and not solver_certificate.covers_look(snapshot.look):
            raise ValueError(
                f"look {snapshot.look} is outside the solver certificate's declared scope"
            )
    return snapshot_tuple


def _false_decisive_motifs(
    space: SymbolicCandidateSpace,
    *,
    classifications: Mapping[str, MotifStatus],
    true_active_motifs: frozenset[str],
) -> tuple[str, ...]:
    errors: list[str] = []
    for motif in space.motifs:
        status = classifications[motif]
        if status is MotifStatus.INVARIANT and motif not in true_active_motifs:
            errors.append(motif)
        elif status is MotifStatus.EXCLUDED and motif in true_active_motifs:
            errors.append(motif)
    return tuple(errors)


def deterministic_anytime_symbolic_lifting_witness(
    space: SymbolicCandidateSpace,
    snapshots: Iterable[SequentialSymbolicConfidenceSetSnapshot],
    *,
    true_candidate_label: str,
    true_active_motifs: frozenset[str],
    true_retained_by_look: Mapping[int, bool],
    decisive_solver_semantics_valid_by_look: Mapping[int, bool],
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate | None = None,
    solver_certificate: AnytimeSolverSemanticValidityCertificate | None = None,
) -> AnytimeSymbolicLiftingWitness:
    """Audit the pointwise all-look symbolic lifting implication.

    At one look, a false decisive status is impossible whenever the true candidate
    belongs to every required retained set and the decisive solver certificates
    have their advertised semantics.  Taking the union over looks establishes the
    sequential implication.  The supplied Boolean maps make this relation
    executable in tests without pretending that RACH can infer the true point.
    """

    if not true_candidate_label:
        raise ValueError("true_candidate_label must be non-empty")
    if not true_active_motifs <= set(space.motifs):
        raise ValueError("true_active_motifs must be a subset of the declared motif vocabulary")
    if coverage_certificate is not None:
        if coverage_certificate.true_candidate_label != true_candidate_label:
            raise ValueError("coverage certificate and requested true candidate must agree")
        expected_required = coverage_certificate.required_cell_ids
    else:
        expected_required = None
    if solver_certificate is not None:
        if set(solver_certificate.motifs) != set(space.motifs):
            raise ValueError("solver certificate motifs must match the symbolic candidate space")
        if expected_required is None:
            expected_required = solver_certificate.required_cell_ids
        elif set(expected_required) != set(solver_certificate.required_cell_ids):
            raise ValueError("coverage and solver certificates must name the same required cell IDs")
        if coverage_certificate is not None:
            _combined_scope(coverage_certificate, solver_certificate)

    snapshot_tuple = _validate_snapshots(
        space,
        snapshots,
        expected_required_cell_ids=expected_required,
        coverage_certificate=coverage_certificate,
        solver_certificate=solver_certificate,
    )
    looks = tuple(snapshot.look for snapshot in snapshot_tuple)
    if set(true_retained_by_look) != set(looks):
        raise ValueError("true_retained_by_look must contain exactly the shown look indices")
    if set(decisive_solver_semantics_valid_by_look) != set(looks):
        raise ValueError("decisive_solver_semantics_valid_by_look must contain exactly the shown look indices")

    errors: dict[int, tuple[str, ...]] = {}
    for snapshot in snapshot_tuple:
        report = classify_symbolic_candidate_sets(space, snapshot.cells)
        errors[snapshot.look] = _false_decisive_motifs(
            space,
            classifications={
                motif: report.classifications[motif].status
                for motif in space.motifs
            },
            true_active_motifs=true_active_motifs,
        )
    witness = AnytimeSymbolicLiftingWitness(
        true_candidate_label=true_candidate_label,
        true_active_motifs=true_active_motifs,
        true_retained_by_look=true_retained_by_look,
        decisive_solver_semantics_valid_by_look=decisive_solver_semantics_valid_by_look,
        false_decisive_motifs_by_look=errors,
    )
    if not witness.implication_holds:
        raise RuntimeError("anytime symbolic lifting implication was violated")
    return witness


def anytime_symbolic_soundness_guarantee(
    space: SymbolicCandidateSpace,
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate,
    solver_certificate: AnytimeSolverSemanticValidityCertificate,
) -> AnytimeSymbolicRACHSoundnessGuarantee:
    """Lift all-look symbolic coverage and solver validity into optional-stopping control.

    **Anytime symbolic candidate-set lifting theorem.** Let ``Theta`` be any
    candidate space and let ``C_{r,t}(Z)`` be arbitrary solver-represented
    retained sets. Suppose

    ``P(for every t in T, theta_star belongs to intersection_r C_{r,t}) >= 1 - alpha``

    and every decisive SAT/UNSAT certificate used across all motifs, required
    cells, and looks in ``T`` is semantically valid with probability at least
    ``1 - beta``. Then

    ``P(exists t in T, any false RACH INVARIANT or EXCLUDED conclusion at t) <= min(1, alpha + beta)``.

    The same bound applies to a conclusion at any data-dependent stopping time
    whose selected look lies in ``T``. The proof is a union bound over the two
    global failure events; they need not be independent.
    """

    if set(coverage_certificate.required_cell_ids) != set(solver_certificate.required_cell_ids):
        raise ValueError("coverage and solver certificates must name the same required cell IDs")
    if set(space.motifs) != set(solver_certificate.motifs):
        raise ValueError("solver certificate motifs must match the symbolic candidate space")
    scope = _combined_scope(coverage_certificate, solver_certificate)
    alpha = coverage_certificate.miscoverage_upper_bound
    beta = solver_certificate.semantic_failure_upper_bound
    bound = min(1.0, alpha + beta)
    return AnytimeSymbolicRACHSoundnessGuarantee(
        true_candidate_label=coverage_certificate.true_candidate_label,
        statistical_time_uniform_coverage_lower_bound=coverage_certificate.lower_bound,
        solver_time_uniform_validity_lower_bound=solver_certificate.lower_bound,
        statistical_miscoverage_upper_bound=alpha,
        solver_semantic_failure_upper_bound=beta,
        time_uniform_family_wise_false_decisive_upper_bound=bound,
        stopping_time_false_decisive_upper_bound=bound,
        required_cell_ids=coverage_certificate.required_cell_ids,
        motifs=space.motifs,
        certified_looks=scope,
        coverage_method=coverage_certificate.method,
        solver_method=solver_certificate.method,
        assumptions=coverage_certificate.assumptions + solver_certificate.assumptions,
    )
