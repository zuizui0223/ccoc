"""Distribution-agnostic confidence-set lifting for RACH conclusions.

The theorem in this module is intentionally upstream of any particular data
model. An external procedure may analyse arbitrary random data (including
continuous, discrete, structured, dependent, high-dimensional, or randomized
observations) and return a set of candidate explanations. RACH only needs a
coverage certificate for that set.

If the true candidate belongs to every required acceptance set with probability
at least ``1 - alpha``, then the probability that RACH makes *any* false decisive
claim (false ``INVARIANT`` or false ``EXCLUDED`` for any declared motif) is at
most ``alpha``. The module does not create the coverage certificate: its role is
to lift an externally valid confidence-set statement into a simultaneous RACH
soundness statement.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .admissibility import (
    AdmissibilityReport,
    CoverageMode,
    MotifStatus,
    ProgramRun,
    RobustnessCell,
    classify_motifs,
)


def _unit_interval(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")


@dataclass(frozen=True)
class CandidateMotifUniverse:
    """A finite qualitative candidate universe with an explicit motif vocabulary.

    This class deliberately contains no data values, likelihoods, or stochastic
    assumptions. A candidate can stand for a causal graph, a qualitative program,
    a scientific explanation, or any other predeclared member of a finite model
    class. A motif is a Boolean property of candidates.
    """

    candidate_motifs: Mapping[str, frozenset[str]]
    motifs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.candidate_motifs:
            raise ValueError("candidate_motifs must not be empty")
        candidate_ids = tuple(self.candidate_motifs)
        if any(not candidate_id for candidate_id in candidate_ids):
            raise ValueError("candidate IDs must be non-empty")
        if not self.motifs:
            raise ValueError("motifs must not be empty")
        if len(set(self.motifs)) != len(self.motifs) or any(not motif for motif in self.motifs):
            raise ValueError("motifs must be unique non-empty names")
        vocabulary = set(self.motifs)
        unknown = set().union(*(set(active) for active in self.candidate_motifs.values())) - vocabulary
        if unknown:
            raise ValueError(f"candidate motifs are absent from the declared vocabulary: {sorted(unknown)}")

    @property
    def candidate_ids(self) -> frozenset[str]:
        return frozenset(self.candidate_motifs)

    def active_motifs(self, candidate_id: str) -> frozenset[str]:
        try:
            return self.candidate_motifs[candidate_id]
        except KeyError as error:
            raise ValueError(f"unknown candidate ID: {candidate_id!r}") from error


@dataclass(frozen=True)
class CandidateAcceptanceSet:
    """The candidate set retained by an arbitrary external data procedure.

    The data procedure itself is intentionally outside RACH. It may be an exact
    test, confidence region, permutation method, conformal method under its own
    assumptions, a Bayesian set with separately justified frequentist coverage,
    or another valid set-valued rule.
    """

    candidate_ids: frozenset[str]


@dataclass(frozen=True)
class ConfidenceSetCell:
    """One RACH robustness cell expressed as a retained candidate confidence set.

    ``coverage_mode`` concerns completeness of the *candidate universe* search.
    It is distinct from statistical coverage of the acceptance set and is never
    upgraded by this module.
    """

    cell_id: str
    acceptance_set: CandidateAcceptanceSet
    description: str = ""
    required: bool = True
    coverage_mode: CoverageMode = CoverageMode.SAMPLED

    def __post_init__(self) -> None:
        if not self.cell_id:
            raise ValueError("cell_id must be non-empty")
        if not isinstance(self.coverage_mode, CoverageMode):
            raise ValueError("coverage_mode must be a CoverageMode")


@dataclass(frozen=True)
class JointCoverageCertificate:
    """An externally established lower bound for simultaneous required-cell coverage.

    The intended assertion is

    ``P(true_candidate is retained in every required cell) >= lower_bound``.

    RACH checks that the statement names its target candidate and its required
    cells, but cannot establish the statement from data by itself. The theorem is
    valid for any random-data distribution or randomized analysis procedure for
    which this certificate is genuinely valid.
    """

    true_candidate_id: str
    required_cell_ids: tuple[str, ...]
    lower_bound: float
    method: str
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.true_candidate_id:
            raise ValueError("true_candidate_id must be non-empty")
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
class DeterministicLiftingWitness:
    """One realized confidence-set outcome and the deterministic theorem relation."""

    true_candidate_id: str
    true_candidate_retained_in_all_required_cells: bool
    false_decisive_motifs: tuple[str, ...]

    @property
    def false_decisive_claim(self) -> bool:
        return bool(self.false_decisive_motifs)

    @property
    def implication_holds(self) -> bool:
        """Whether false decisiveness implies a failure of joint coverage."""

        return not self.false_decisive_claim or not self.true_candidate_retained_in_all_required_cells


@dataclass(frozen=True)
class RACHSoundnessGuarantee:
    """A finite-sample, simultaneous upper bound induced by a coverage certificate."""

    true_candidate_id: str
    joint_coverage_lower_bound: float
    family_wise_false_decisive_upper_bound: float
    false_invariant_upper_bounds: Mapping[str, float]
    false_excluded_upper_bounds: Mapping[str, float]
    certificate_method: str
    certificate_assumptions: tuple[str, ...]


def _validate_cells(
    universe: CandidateMotifUniverse,
    cells: Iterable[ConfidenceSetCell],
) -> tuple[ConfidenceSetCell, ...]:
    cell_tuple = tuple(cells)
    if not cell_tuple:
        raise ValueError("at least one confidence-set cell is required")
    ids = [cell.cell_id for cell in cell_tuple]
    if len(set(ids)) != len(ids):
        raise ValueError("confidence-set cell IDs must be unique")
    if not any(cell.required for cell in cell_tuple):
        raise ValueError("at least one confidence-set cell must be required")
    unknown = set().union(*(set(cell.acceptance_set.candidate_ids) for cell in cell_tuple)) - universe.candidate_ids
    if unknown:
        raise ValueError(f"acceptance sets contain unknown candidate IDs: {sorted(unknown)}")
    return cell_tuple


def classify_confidence_sets(
    universe: CandidateMotifUniverse,
    cells: Iterable[ConfidenceSetCell],
) -> AdmissibilityReport:
    """Run ordinary RACH classification on externally supplied acceptance sets.

    No probability model enters here. This is a deterministic map from retained
    candidate sets to RACH statuses.
    """

    cell_tuple = _validate_cells(universe, cells)
    robustness_cells = tuple(
        RobustnessCell(
            cell_id=cell.cell_id,
            description=cell.description or cell.cell_id,
            runs=tuple(
                ProgramRun(
                    run_id=candidate_id,
                    cell_id=cell.cell_id,
                    active_motifs=universe.active_motifs(candidate_id),
                    accepted=candidate_id in cell.acceptance_set.candidate_ids,
                )
                for candidate_id in sorted(universe.candidate_ids)
            ),
            required=cell.required,
            coverage_mode=cell.coverage_mode,
        )
        for cell in cell_tuple
    )
    return classify_motifs(universe.motifs, robustness_cells)


def joint_coverage_event(
    true_candidate_id: str,
    cells: Iterable[ConfidenceSetCell],
) -> bool:
    """Whether one realized outcome retains the true candidate in all required cells."""

    cell_tuple = tuple(cells)
    if not any(cell.required for cell in cell_tuple):
        raise ValueError("at least one required confidence-set cell is needed")
    return all(
        true_candidate_id in cell.acceptance_set.candidate_ids
        for cell in cell_tuple
        if cell.required
    )


def false_decisive_motifs(
    universe: CandidateMotifUniverse,
    report: AdmissibilityReport,
    *,
    true_candidate_id: str,
) -> tuple[str, ...]:
    """Return motifs falsely called invariant or excluded in one realized outcome."""

    true_motifs = universe.active_motifs(true_candidate_id)
    errors: list[str] = []
    for motif in universe.motifs:
        status = report.classifications[motif].status
        if status is MotifStatus.INVARIANT and motif not in true_motifs:
            errors.append(motif)
        elif status is MotifStatus.EXCLUDED and motif in true_motifs:
            errors.append(motif)
    return tuple(errors)


def deterministic_lifting_witness(
    universe: CandidateMotifUniverse,
    cells: Iterable[ConfidenceSetCell],
    *,
    true_candidate_id: str,
) -> DeterministicLiftingWitness:
    """Check the pointwise implication behind the confidence-set lifting theorem.

    For every realized data outcome, if the true candidate is retained in all
    required cells, no motif can be falsely called ``INVARIANT`` or ``EXCLUDED``.
    This is a deterministic statement; probability enters only through an
    external coverage certificate for the retention event.
    """

    if true_candidate_id not in universe.candidate_ids:
        raise ValueError("true_candidate_id must belong to the candidate universe")
    cell_tuple = _validate_cells(universe, cells)
    report = classify_confidence_sets(universe, cell_tuple)
    witness = DeterministicLiftingWitness(
        true_candidate_id=true_candidate_id,
        true_candidate_retained_in_all_required_cells=joint_coverage_event(
            true_candidate_id, cell_tuple
        ),
        false_decisive_motifs=false_decisive_motifs(
            universe, report, true_candidate_id=true_candidate_id
        ),
    )
    if not witness.implication_holds:
        raise RuntimeError("confidence-set lifting implication was violated")
    return witness


def soundness_guarantee_from_joint_coverage(
    universe: CandidateMotifUniverse,
    certificate: JointCoverageCertificate,
) -> RACHSoundnessGuarantee:
    """Lift a simultaneous confidence-set coverage claim into RACH error control.

    **Confidence-set lifting theorem.** Let ``C_r(X, U)`` be arbitrary (possibly
    randomized) retained candidate sets for required cells ``r`` and let ``theta``
    be the true candidate. If

    ``P(theta in intersection_r C_r(X, U)) >= 1 - alpha``,

    then, for the RACH classification based on those cells,

    ``P(any false INVARIANT or false EXCLUDED conclusion) <= alpha``.

    The proof is pointwise: every false decisive conclusion excludes ``theta``
    from at least one required acceptance set. Therefore the false-decisive event
    is a subset of the joint-miscoverage event. No distributional form, sample
    size, independence assumption, or data type is used by this implication.
    """

    if certificate.true_candidate_id not in universe.candidate_ids:
        raise ValueError("certificate true candidate must belong to the candidate universe")
    alpha = certificate.miscoverage_upper_bound
    true_motifs = universe.active_motifs(certificate.true_candidate_id)
    false_invariant = {
        motif: 0.0 if motif in true_motifs else alpha
        for motif in universe.motifs
    }
    false_excluded = {
        motif: alpha if motif in true_motifs else 0.0
        for motif in universe.motifs
    }
    return RACHSoundnessGuarantee(
        true_candidate_id=certificate.true_candidate_id,
        joint_coverage_lower_bound=certificate.lower_bound,
        family_wise_false_decisive_upper_bound=alpha,
        false_invariant_upper_bounds=false_invariant,
        false_excluded_upper_bounds=false_excluded,
        certificate_method=certificate.method,
        certificate_assumptions=certificate.assumptions,
    )


def indistinguishability_abstention_lower_bound(miscoverage_upper_bound: float) -> float:
    """Lower bound on non-decision for an observationally indistinguishable pair.

    If one candidate has a motif and another lacks it but both induce exactly the
    same data distribution, an honest procedure with coverage error at most
    ``alpha`` can call that motif invariant with probability at most ``alpha``
    under the inactive truth and excluded with probability at most ``alpha`` under
    the active truth. Thus, under their shared distribution, the probability of
    ``UNRESOLVED`` or ``UNSUPPORTED`` is at least ``max(0, 1 - 2*alpha)``.

    This is an impossibility boundary, not a model of data generation: RACH can
    be universally sound by abstaining, but cannot be universally decisive.
    """

    _unit_interval(miscoverage_upper_bound, "miscoverage_upper_bound")
    return max(0.0, 1.0 - 2.0 * miscoverage_upper_bound)
