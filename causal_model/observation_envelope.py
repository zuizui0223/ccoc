"""Exact observation-channel robustness envelopes for finite RACH universes.

This module evaluates *the classifier itself* under a known finite candidate
universe.  A user declares one candidate program and one feasible state per
robustness cell as the known generator, then enumerates every possible vector of
repeated binary detections exactly.  For each observation outcome it runs the
ordinary noisy-program / robust-admissibility pipeline and aggregates the
probability of invariant, excluded, unresolved, and unsupported conclusions.

It is deliberately domain-agnostic: no fitness function, species, trait unit,
or ecological mechanism is built into this module.  Results are conditional on
the declared program universe, true generator, state(s), observation channels,
acceptance thresholds, and coverage labels.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import comb, isclose, isfinite, prod
from typing import Iterable, Mapping

from .admissibility import CoverageMode, MotifStatus
from .ecological_program import (
    NoisyObservationPanel,
    NoisyRobustnessCell,
    QualitativeProgramCandidate,
    State,
    TraitDetection,
    evaluate_candidate_universe,
)


def _unit_interval(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")


@dataclass(frozen=True)
class DetectionChannelDesign:
    """One repeated binary detection channel before observations are collected.

    The channel is intentionally generic.  ``trait`` may be any declared binary
    observable in a qualitative program; it is not assumed to be a pollinator,
    genetic, phenotypic, or fitness measurement.
    """

    trait: str
    trials: int
    sensitivity: float = 1.0
    false_positive: float = 0.0

    def __post_init__(self) -> None:
        if not self.trait:
            raise ValueError("trait must be non-empty")
        if self.trials < 1:
            raise ValueError("trials must be at least one")
        _unit_interval(self.sensitivity, "sensitivity")
        _unit_interval(self.false_positive, "false_positive")

    def probability(self, detections: int, true_present: bool) -> float:
        """Exact binomial mass for one possible reported detection count."""

        if not 0 <= detections <= self.trials:
            raise ValueError("detections must lie between zero and trials")
        probability_present = self.sensitivity if true_present else self.false_positive
        return comb(self.trials, detections) * probability_present**detections * (
            1.0 - probability_present
        ) ** (self.trials - detections)


@dataclass(frozen=True)
class ObservationEnvelopeCell:
    """A pre-data observation-cell design used in exact envelope enumeration.

    ``coverage_mode`` describes the completeness of the *candidate-program
    search* in this cell.  It must not be upgraded merely because observation
    outcomes were enumerated exactly.
    """

    cell_id: str
    description: str
    channels: tuple[DetectionChannelDesign, ...]
    acceptance_log_likelihood: float
    required: bool = True
    coverage_mode: CoverageMode = CoverageMode.SAMPLED

    def __post_init__(self) -> None:
        if not self.cell_id:
            raise ValueError("cell_id must be non-empty")
        if not self.channels:
            raise ValueError("at least one detection channel is required")
        if not isfinite(self.acceptance_log_likelihood):
            raise ValueError("acceptance_log_likelihood must be finite")
        if not isinstance(self.coverage_mode, CoverageMode):
            raise ValueError("coverage_mode must be a CoverageMode")
        traits = [channel.trait for channel in self.channels]
        if len(set(traits)) != len(traits):
            raise ValueError("one envelope cell may contain each trait once")

    @property
    def outcome_count(self) -> int:
        """Number of all possible joint detection-count outcomes in this cell."""

        return prod(channel.trials + 1 for channel in self.channels)


@dataclass(frozen=True)
class MotifEnvelopeProfile:
    """Exact conclusion probabilities for one motif under a known generator."""

    motif: str
    true_active: bool
    invariant_probability: float
    excluded_probability: float
    unresolved_probability: float
    unsupported_probability: float
    false_invariant_probability: float
    false_excluded_probability: float
    correct_invariant_probability: float
    correct_excluded_probability: float

    @property
    def decisive_error_probability(self) -> float:
        """Probability of a wrong invariant or wrong excluded conclusion."""

        return self.false_invariant_probability + self.false_excluded_probability

    @property
    def decisive_correct_probability(self) -> float:
        """Probability of a correct invariant or correct excluded conclusion."""

        return self.correct_invariant_probability + self.correct_excluded_probability


@dataclass(frozen=True)
class ExactObservationEnvelope:
    """An exact self-calibration result for one known finite observation design."""

    true_candidate_id: str
    total_outcome_count: int
    total_probability: float
    profiles: Mapping[str, MotifEnvelopeProfile]


@dataclass(frozen=True)
class ObservationEnvelopeSweepPoint:
    """One named observation design and its exact envelope result."""

    label: str
    envelope: ExactObservationEnvelope


def _validate_universe(
    candidates: Iterable[QualitativeProgramCandidate],
    motifs: Iterable[str],
    cells: Iterable[ObservationEnvelopeCell],
    true_candidate_id: str,
    true_states: Mapping[str, State],
) -> tuple[
    tuple[QualitativeProgramCandidate, ...],
    tuple[str, ...],
    tuple[ObservationEnvelopeCell, ...],
    QualitativeProgramCandidate,
]:
    candidate_tuple = tuple(candidates)
    if not candidate_tuple:
        raise ValueError("at least one candidate program is required")
    candidate_ids = [candidate.candidate_id for candidate in candidate_tuple]
    if len(set(candidate_ids)) != len(candidate_ids):
        raise ValueError("candidate IDs must be unique")
    try:
        true_candidate = next(
            candidate for candidate in candidate_tuple if candidate.candidate_id == true_candidate_id
        )
    except StopIteration as error:
        raise ValueError("true_candidate_id must identify one declared candidate") from error

    motif_tuple = tuple(motifs)
    if not motif_tuple:
        raise ValueError("at least one motif is required")
    if len(set(motif_tuple)) != len(motif_tuple) or any(not motif for motif in motif_tuple):
        raise ValueError("motifs must be unique non-empty names")
    unknown_active = set().union(*(candidate.active_motifs for candidate in candidate_tuple)) - set(motif_tuple)
    if unknown_active:
        raise ValueError(f"candidate motifs are missing from motif vocabulary: {sorted(unknown_active)}")

    cell_tuple = tuple(cells)
    if not cell_tuple:
        raise ValueError("at least one observation envelope cell is required")
    cell_ids = [cell.cell_id for cell in cell_tuple]
    if len(set(cell_ids)) != len(cell_ids):
        raise ValueError("observation envelope cell IDs must be unique")
    if not any(cell.required for cell in cell_tuple):
        raise ValueError("at least one observation envelope cell must be required")
    if set(true_states) != set(cell_ids):
        raise ValueError("true_states must contain exactly one state for every envelope cell")

    for cell in cell_tuple:
        state = true_states[cell.cell_id]
        if state not in true_candidate.program.states:
            raise ValueError(f"true state for cell {cell.cell_id!r} is infeasible in the true program")
        traits = {channel.trait for channel in cell.channels}
        for candidate in candidate_tuple:
            missing = traits - set(candidate.program.trait_rules)
            if missing:
                raise ValueError(
                    f"candidate {candidate.candidate_id!r} lacks cell traits: {sorted(missing)}"
                )
    return candidate_tuple, motif_tuple, cell_tuple, true_candidate


def _enumerate_cell_outcomes(
    cell: ObservationEnvelopeCell,
    true_candidate: QualitativeProgramCandidate,
    true_state: State,
) -> tuple[tuple[float, NoisyRobustnessCell], ...]:
    """Enumerate every cell-level detection-count outcome and its exact mass."""

    detection_ranges = tuple(range(channel.trials + 1) for channel in cell.channels)
    outcomes: list[tuple[float, NoisyRobustnessCell]] = []
    for counts in product(*detection_ranges):
        detections: list[TraitDetection] = []
        probability = 1.0
        for channel, count in zip(cell.channels, counts):
            true_present = true_candidate.program.trait_is_present(channel.trait, true_state)
            probability *= channel.probability(count, true_present)
            detections.append(
                TraitDetection(
                    trait=channel.trait,
                    detections=count,
                    trials=channel.trials,
                    sensitivity=channel.sensitivity,
                    false_positive=channel.false_positive,
                )
            )
        if probability == 0.0:
            continue
        outcomes.append(
            (
                probability,
                NoisyRobustnessCell(
                    cell_id=cell.cell_id,
                    description=cell.description,
                    observations=NoisyObservationPanel(tuple(detections)),
                    acceptance_log_likelihood=cell.acceptance_log_likelihood,
                    required=cell.required,
                    coverage_mode=cell.coverage_mode,
                ),
            )
        )
    return tuple(outcomes)


def evaluate_exact_observation_envelope(
    candidates: Iterable[QualitativeProgramCandidate],
    motifs: Iterable[str],
    cells: Iterable[ObservationEnvelopeCell],
    *,
    true_candidate_id: str,
    true_states: Mapping[str, State],
    max_outcomes: int = 100_000,
) -> ExactObservationEnvelope:
    """Enumerate exact classification risk for all repeated-detection outcomes.

    The known generator is one candidate program and one declared feasible state
    in each cell.  This produces a *self-calibration* result within the finite
    candidate universe.  It does not validate a candidate grammar against nature
    or confer complete coverage on a sampled candidate family.
    """

    if max_outcomes < 1:
        raise ValueError("max_outcomes must be at least one")
    candidate_tuple, motif_tuple, cell_tuple, true_candidate = _validate_universe(
        candidates, motifs, cells, true_candidate_id, true_states
    )
    total_outcome_count = prod(cell.outcome_count for cell in cell_tuple)
    if total_outcome_count > max_outcomes:
        raise ValueError(
            f"exact envelope has {total_outcome_count} outcomes, above max_outcomes={max_outcomes}"
        )

    cell_outcomes = tuple(
        _enumerate_cell_outcomes(cell, true_candidate, true_states[cell.cell_id])
        for cell in cell_tuple
    )
    if any(not outcomes for outcomes in cell_outcomes):
        raise RuntimeError("an observation cell had no positive-probability outcomes")

    status_mass = {
        motif: {status: 0.0 for status in MotifStatus}
        for motif in motif_tuple
    }
    total_probability = 0.0
    for joint_outcome in product(*cell_outcomes):
        probability = prod(item[0] for item in joint_outcome)
        report = evaluate_candidate_universe(
            candidate_tuple,
            tuple(item[1] for item in joint_outcome),
        ).classify(motif_tuple)
        total_probability += probability
        for motif in motif_tuple:
            status = report.classifications[motif].status
            status_mass[motif][status] += probability

    if not isclose(total_probability, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise RuntimeError(f"outcome probabilities should sum to one, got {total_probability}")

    profiles: dict[str, MotifEnvelopeProfile] = {}
    true_motifs = true_candidate.active_motifs
    for motif in motif_tuple:
        masses = status_mass[motif]
        true_active = motif in true_motifs
        invariant_probability = masses[MotifStatus.INVARIANT]
        excluded_probability = masses[MotifStatus.EXCLUDED]
        profiles[motif] = MotifEnvelopeProfile(
            motif=motif,
            true_active=true_active,
            invariant_probability=invariant_probability,
            excluded_probability=excluded_probability,
            unresolved_probability=masses[MotifStatus.UNRESOLVED],
            unsupported_probability=masses[MotifStatus.UNSUPPORTED],
            false_invariant_probability=0.0 if true_active else invariant_probability,
            false_excluded_probability=excluded_probability if true_active else 0.0,
            correct_invariant_probability=invariant_probability if true_active else 0.0,
            correct_excluded_probability=0.0 if true_active else excluded_probability,
        )
    return ExactObservationEnvelope(
        true_candidate_id=true_candidate_id,
        total_outcome_count=total_outcome_count,
        total_probability=total_probability,
        profiles=profiles,
    )


def sweep_exact_observation_envelopes(
    candidates: Iterable[QualitativeProgramCandidate],
    motifs: Iterable[str],
    cell_designs_by_label: Mapping[str, Iterable[ObservationEnvelopeCell]],
    *,
    true_candidate_id: str,
    true_states: Mapping[str, State],
    max_outcomes: int = 100_000,
) -> tuple[ObservationEnvelopeSweepPoint, ...]:
    """Evaluate several named observation-channel designs against one known truth."""

    if not cell_designs_by_label:
        raise ValueError("at least one labelled observation design is required")
    points: list[ObservationEnvelopeSweepPoint] = []
    for label, cells in cell_designs_by_label.items():
        if not label:
            raise ValueError("observation-design labels must be non-empty")
        points.append(
            ObservationEnvelopeSweepPoint(
                label=label,
                envelope=evaluate_exact_observation_envelope(
                    candidates,
                    motifs,
                    tuple(cells),
                    true_candidate_id=true_candidate_id,
                    true_states=true_states,
                    max_outcomes=max_outcomes,
                ),
            )
        )
    return tuple(points)


def observation_envelope_table_markdown(
    points: Iterable[ObservationEnvelopeSweepPoint],
    motif: str,
    *,
    digits: int = 4,
) -> str:
    """Render exact motif-level envelope results as a compact Markdown table."""

    if digits < 0:
        raise ValueError("digits must be non-negative")
    point_tuple = tuple(points)
    if not point_tuple:
        raise ValueError("at least one sweep point is required")
    rows = [
        "| design | outcomes | true active | invariant | excluded | unresolved | unsupported | false decisive |",
        "|---|---:|---|---:|---:|---:|---:|---:|",
    ]
    for point in point_tuple:
        try:
            profile = point.envelope.profiles[motif]
        except KeyError as error:
            raise ValueError(f"motif {motif!r} is absent from one or more envelopes") from error
        rows.append(
            "| "
            + " | ".join(
                (
                    point.label,
                    str(point.envelope.total_outcome_count),
                    "yes" if profile.true_active else "no",
                    f"{profile.invariant_probability:.{digits}f}",
                    f"{profile.excluded_probability:.{digits}f}",
                    f"{profile.unresolved_probability:.{digits}f}",
                    f"{profile.unsupported_probability:.{digits}f}",
                    f"{profile.decisive_error_probability:.{digits}f}",
                )
            )
            + " |"
        )
    return "\n".join(rows)
