"""Finite qualitative ecological programs with noisy observations and exact panels.

This module broadens the OR-only theorem core without silently extending its
proof. A ``QualitativeProgram`` declares Boolean trait rules over a finite
mechanism state space. It may represent conjunction, alternative pathways and
inhibition snapshots. Exact state enumeration, likelihood scoring and minimum
observation panels are all conditional on that declared program and candidate
observation library.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import comb, isfinite, log
from typing import Iterable, Mapping

from .admissibility import (
    AdmissibilityReport,
    CoverageMode,
    ProgramRun,
    RobustnessCell,
    classify_motifs,
)

State = tuple[int, ...]


class Formula:
    """Boolean trait-rule expression over binary mechanism switches."""

    def evaluate(self, state: State) -> bool:
        raise NotImplementedError

    def mechanism_indices(self) -> frozenset[int]:
        raise NotImplementedError


@dataclass(frozen=True)
class Mechanism(Formula):
    """A single mechanism switch in a qualitative trait rule."""

    index: int

    def evaluate(self, state: State) -> bool:
        return bool(state[self.index])

    def mechanism_indices(self) -> frozenset[int]:
        return frozenset({self.index})


@dataclass(frozen=True)
class AllOf(Formula):
    """A conjunction of ecological requirements."""

    terms: tuple[Formula, ...]

    def __post_init__(self) -> None:
        if not self.terms:
            raise ValueError("AllOf requires at least one term")

    def evaluate(self, state: State) -> bool:
        return all(term.evaluate(state) for term in self.terms)

    def mechanism_indices(self) -> frozenset[int]:
        return frozenset().union(*(term.mechanism_indices() for term in self.terms))


@dataclass(frozen=True)
class AnyOf(Formula):
    """Alternative qualitative pathways to one trait."""

    terms: tuple[Formula, ...]

    def __post_init__(self) -> None:
        if not self.terms:
            raise ValueError("AnyOf requires at least one term")

    def evaluate(self, state: State) -> bool:
        return any(term.evaluate(state) for term in self.terms)

    def mechanism_indices(self) -> frozenset[int]:
        return frozenset().union(*(term.mechanism_indices() for term in self.terms))


@dataclass(frozen=True)
class Not(Formula):
    """A qualitative inhibitory condition."""

    term: Formula

    def evaluate(self, state: State) -> bool:
        return not self.term.evaluate(state)

    def mechanism_indices(self) -> frozenset[int]:
        return self.term.mechanism_indices()


@dataclass(frozen=True)
class QualitativeProgram:
    """Declared finite grammar for ecological mechanism-to-trait predictions.

    ``feasible_states`` is optional. Supplying it makes background compatibility,
    resource, or life-history restrictions explicit rather than assuming the full
    Boolean cube. State enumeration remains exact only for the declared finite
    state set.
    """

    mechanism_count: int
    trait_rules: Mapping[str, Formula]
    feasible_states: frozenset[State] | None = None

    def __post_init__(self) -> None:
        if self.mechanism_count < 1:
            raise ValueError("mechanism_count must be positive")
        if not self.trait_rules:
            raise ValueError("trait_rules must not be empty")
        all_states = frozenset(product((0, 1), repeat=self.mechanism_count))
        if self.feasible_states is not None:
            if not self.feasible_states:
                raise ValueError("feasible_states must not be empty")
            if not set(self.feasible_states) <= all_states:
                raise ValueError("feasible_states contains an invalid Boolean state")
        for trait, rule in self.trait_rules.items():
            if not trait:
                raise ValueError("trait names must be non-empty")
            if not isinstance(rule, Formula):
                raise ValueError("trait rules must be Formula objects")
            invalid = set(rule.mechanism_indices()) - set(range(self.mechanism_count))
            if invalid:
                raise ValueError(
                    f"rule for {trait!r} contains invalid mechanism indices: {sorted(invalid)}"
                )

    @property
    def states(self) -> tuple[State, ...]:
        if self.feasible_states is not None:
            return tuple(sorted(self.feasible_states))
        return tuple(product((0, 1), repeat=self.mechanism_count))

    def trait_is_present(self, trait: str, state: State) -> bool:
        if trait not in self.trait_rules:
            raise ValueError(f"unknown program trait: {trait!r}")
        if state not in self.states:
            raise ValueError("state is not feasible in this qualitative program")
        return self.trait_rules[trait].evaluate(state)


@dataclass(frozen=True)
class HardTraitObservation:
    """Exact trait requirements, used only when presence or NULL is trustworthy."""

    present: tuple[str, ...] = ()
    null: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if set(self.present) & set(self.null):
            raise ValueError("a trait cannot be both present and null")
        if len(set(self.present)) != len(self.present) or len(set(self.null)) != len(self.null):
            raise ValueError("hard-observation trait names must be unique")


def _validate_hard_observation(program: QualitativeProgram, observation: HardTraitObservation) -> None:
    unknown = (set(observation.present) | set(observation.null)) - set(program.trait_rules)
    if unknown:
        raise ValueError(f"observation refers to unknown traits: {sorted(unknown)}")


def admissible_states(
    program: QualitativeProgram,
    observation: HardTraitObservation,
) -> tuple[State, ...]:
    """Return declared states exactly compatible with trusted binary observations."""
    _validate_hard_observation(program, observation)
    return tuple(
        state
        for state in program.states
        if all(program.trait_is_present(trait, state) for trait in observation.present)
        and all(not program.trait_is_present(trait, state) for trait in observation.null)
    )


def mechanism_forced_on(states: Iterable[State], mechanism: int) -> bool:
    """Whether one switch is ON in every state of a non-empty declared region."""
    states_tuple = tuple(states)
    if not states_tuple:
        return False
    if mechanism not in range(len(states_tuple[0])):
        raise ValueError("mechanism index is out of range")
    return all(state[mechanism] == 1 for state in states_tuple)


@dataclass(frozen=True)
class TraitDetection:
    """Repeated binary detections for one trait with a declared observation channel.

    ``sensitivity`` is P(report present | trait truly present); ``false_positive``
    is P(report present | trait truly absent). NULL observations remain
    probabilistic unless sensitivity=1 and false_positive=0.
    """

    trait: str
    detections: int
    trials: int
    sensitivity: float = 1.0
    false_positive: float = 0.0

    def __post_init__(self) -> None:
        if not self.trait:
            raise ValueError("trait must be non-empty")
        if self.trials < 1:
            raise ValueError("trials must be at least one")
        if not 0 <= self.detections <= self.trials:
            raise ValueError("detections must lie between zero and trials")
        if not 0.0 <= self.sensitivity <= 1.0:
            raise ValueError("sensitivity must lie between zero and one")
        if not 0.0 <= self.false_positive <= 1.0:
            raise ValueError("false_positive must lie between zero and one")

    def likelihood(self, true_present: bool) -> float:
        probability_present = self.sensitivity if true_present else self.false_positive
        return comb(self.trials, self.detections) * probability_present**self.detections * (
            1.0 - probability_present
        ) ** (self.trials - self.detections)

    def log_likelihood(self, true_present: bool) -> float:
        value = self.likelihood(true_present)
        return float("-inf") if value == 0.0 else log(value)


@dataclass(frozen=True)
class NoisyObservationPanel:
    """Independent repeated trait detections for a declared observation context."""

    detections: tuple[TraitDetection, ...]

    def __post_init__(self) -> None:
        if not self.detections:
            raise ValueError("at least one trait detection is required")
        traits = [detection.trait for detection in self.detections]
        if len(set(traits)) != len(traits):
            raise ValueError("one noisy observation panel may contain each trait once")


def _validate_noisy_panel(program: QualitativeProgram, panel: NoisyObservationPanel) -> None:
    unknown = {detection.trait for detection in panel.detections} - set(program.trait_rules)
    if unknown:
        raise ValueError(f"noisy panel refers to unknown traits: {sorted(unknown)}")


@dataclass(frozen=True)
class ProgramFit:
    """Exact finite likelihood evaluation over all declared feasible states."""

    best_log_likelihood: float
    best_states: tuple[State, ...]
    state_log_likelihoods: Mapping[State, float]


def fit_program(program: QualitativeProgram, panel: NoisyObservationPanel) -> ProgramFit:
    """Score a program by enumerating its declared states under noisy observations."""
    _validate_noisy_panel(program, panel)
    scores: dict[State, float] = {}
    for state in program.states:
        score = sum(
            detection.log_likelihood(program.trait_is_present(detection.trait, state))
            for detection in panel.detections
        )
        scores[state] = score
    best = max(scores.values())
    return ProgramFit(
        best_log_likelihood=best,
        best_states=tuple(state for state in program.states if scores[state] == best),
        state_log_likelihoods=scores,
    )


@dataclass(frozen=True)
class QualitativeProgramCandidate:
    """One candidate ecological program and the motifs it asserts are active."""

    candidate_id: str
    active_motifs: frozenset[str]
    program: QualitativeProgram

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate_id must be non-empty")


@dataclass(frozen=True)
class NoisyRobustnessCell:
    """One observation/threshold context for program-family robust admissibility.

    The threshold is deliberately supplied by the analyst. It can encode a
    likelihood rule, a posterior-predictive check, a calibrated distance cutoff,
    or an externally generated acceptance decision translated to this finite
    interface.
    """

    cell_id: str
    description: str
    observations: NoisyObservationPanel
    acceptance_log_likelihood: float
    required: bool = True
    coverage_mode: CoverageMode = CoverageMode.SAMPLED

    def __post_init__(self) -> None:
        if not self.cell_id:
            raise ValueError("cell_id must be non-empty")
        if not isfinite(self.acceptance_log_likelihood):
            raise ValueError("acceptance_log_likelihood must be finite")


@dataclass(frozen=True)
class CandidateEvaluation:
    """One candidate's best finite fit in one robustness cell."""

    candidate_id: str
    cell_id: str
    accepted: bool
    best_log_likelihood: float
    best_states: tuple[State, ...]


@dataclass(frozen=True)
class CandidateUniverseReport:
    """Bridge from noisy qualitative programs to existing robust classifications."""

    robustness_cells: tuple[RobustnessCell, ...]
    evaluations: tuple[CandidateEvaluation, ...]

    def classify(self, motifs: Iterable[str]) -> AdmissibilityReport:
        return classify_motifs(motifs, self.robustness_cells)


def evaluate_candidate_universe(
    candidates: Iterable[QualitativeProgramCandidate],
    cells: Iterable[NoisyRobustnessCell],
) -> CandidateUniverseReport:
    """Evaluate a declared candidate-program universe in each noisy robustness cell.

    Each candidate is accepted in a cell only if some *declared feasible state*
    reaches the cell's predeclared likelihood threshold. No result is a causal
    conclusion outside the candidate universe, observation channel and threshold.
    """
    candidate_tuple = tuple(candidates)
    cell_tuple = tuple(cells)
    if not candidate_tuple:
        raise ValueError("at least one program candidate is required")
    if not cell_tuple:
        raise ValueError("at least one noisy robustness cell is required")
    candidate_ids = [candidate.candidate_id for candidate in candidate_tuple]
    if len(set(candidate_ids)) != len(candidate_ids):
        raise ValueError("candidate IDs must be unique")
    cell_ids = [cell.cell_id for cell in cell_tuple]
    if len(set(cell_ids)) != len(cell_ids):
        raise ValueError("robustness cell IDs must be unique")

    all_evaluations: list[CandidateEvaluation] = []
    robust_cells: list[RobustnessCell] = []
    for cell in cell_tuple:
        runs: list[ProgramRun] = []
        for candidate in candidate_tuple:
            fit = fit_program(candidate.program, cell.observations)
            accepted = fit.best_log_likelihood >= cell.acceptance_log_likelihood
            all_evaluations.append(
                CandidateEvaluation(
                    candidate_id=candidate.candidate_id,
                    cell_id=cell.cell_id,
                    accepted=accepted,
                    best_log_likelihood=fit.best_log_likelihood,
                    best_states=fit.best_states,
                )
            )
            runs.append(
                ProgramRun(
                    run_id=candidate.candidate_id,
                    cell_id=cell.cell_id,
                    active_motifs=candidate.active_motifs,
                    accepted=accepted,
                )
            )
        robust_cells.append(
            RobustnessCell(
                cell_id=cell.cell_id,
                description=cell.description,
                runs=tuple(runs),
                required=cell.required,
                coverage_mode=cell.coverage_mode,
            )
        )
    return CandidateUniverseReport(tuple(robust_cells), tuple(all_evaluations))


@dataclass(frozen=True)
class HardObservationCandidate:
    """A feasible exact trait observation with its acquisition cost."""

    trait: str
    reported_present: bool
    cost: float = 1.0

    def __post_init__(self) -> None:
        if not self.trait:
            raise ValueError("candidate trait must be non-empty")
        if not isfinite(self.cost) or self.cost < 0.0:
            raise ValueError("candidate cost must be finite and non-negative")


@dataclass(frozen=True)
class MinimumBooleanPanel:
    """Exact minimum-cost panel making one mechanism forced ON in a Boolean program."""

    focal_mechanism: int
    selected_traits: tuple[str, ...]
    total_cost: float
    observation: HardTraitObservation
    admissible_state_count: int


def _panel_rank(cost: float, traits: tuple[str, ...]) -> tuple[float, int, tuple[str, ...]]:
    return cost, len(traits), traits


def _merge_hard_observation(
    base: HardTraitObservation,
    candidates: Iterable[HardObservationCandidate],
) -> HardTraitObservation:
    positive = [*base.present]
    null = [*base.null]
    for candidate in candidates:
        (positive if candidate.reported_present else null).append(candidate.trait)
    return HardTraitObservation(tuple(positive), tuple(null))


def minimum_boolean_panel(
    program: QualitativeProgram,
    *,
    focal_mechanism: int,
    candidates: Iterable[HardObservationCandidate],
    base_observation: HardTraitObservation = HardTraitObservation(),
) -> MinimumBooleanPanel | None:
    """Exhaustively find the cheapest candidate panel that forces one mechanism ON.

    This deliberately evaluates *joint* panels rather than using singleton gain.
    It supports AND, OR, NOT and explicit feasible-state restrictions through the
    declared program. Complexity is exponential in candidate count; use it for
    finite design libraries or replace it with a solver-backed implementation.
    """
    if focal_mechanism not in range(program.mechanism_count):
        raise ValueError("focal mechanism index is out of range")
    _validate_hard_observation(program, base_observation)
    candidate_tuple = tuple(candidates)
    traits = [candidate.trait for candidate in candidate_tuple]
    if len(set(traits)) != len(traits):
        raise ValueError("candidate traits must be unique")
    base_traits = set(base_observation.present) | set(base_observation.null)
    overlap = base_traits & set(traits)
    if overlap:
        raise ValueError(f"candidate traits duplicate base observations: {sorted(overlap)}")
    unknown = set(traits) - set(program.trait_rules)
    if unknown:
        raise ValueError(f"candidate traits are unknown to program: {sorted(unknown)}")

    best: MinimumBooleanPanel | None = None
    for size in range(len(candidate_tuple) + 1):
        for selected in combinations(candidate_tuple, size):
            selected_traits = tuple(sorted(candidate.trait for candidate in selected))
            cost = sum(candidate.cost for candidate in selected)
            if best is not None and _panel_rank(cost, selected_traits) >= _panel_rank(
                best.total_cost, best.selected_traits
            ):
                continue
            observation = _merge_hard_observation(base_observation, selected)
            states = admissible_states(program, observation)
            if not states or not mechanism_forced_on(states, focal_mechanism):
                continue
            best = MinimumBooleanPanel(
                focal_mechanism=focal_mechanism,
                selected_traits=selected_traits,
                total_cost=cost,
                observation=observation,
                admissible_state_count=len(states),
            )
    return best
