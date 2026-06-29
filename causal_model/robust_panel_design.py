"""Cost-aware observation-panel design under finite misspecification scenarios.

The structural theorem answers whether a NULL panel forces a focal mechanism ON
inside a declared monotone-OR grammar. This module adds a second layer: among
all such panels, choose one with low posterior false-necessity risk across an
explicit finite family of true-model and observation-channel scenarios.

The implementation is exact by subset enumeration and finite-state weighted
summation. It is intended for modest candidate panels, where auditability matters
more than asymptotic optimization.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from math import isfinite
from typing import Iterable, Mapping

from .failure_modes import BinaryObservationChannel, TruthTableModel
from .observation_design import NullObservationCandidate
from .replaceability import Observation, StructuralModel, forced_on_by_theorem


class RobustObjective(str, Enum):
    """How risk is aggregated across declared true-model scenarios."""

    MINIMAX = "minimax"
    WEIGHTED_MEAN = "weighted_mean"


@dataclass(frozen=True)
class FinitePanelScenario:
    """A weighted finite true model for evaluating a proposed observation panel."""

    scenario_id: str
    truth_model: TruthTableModel
    weight: float = 1.0
    channels: Mapping[str, BinaryObservationChannel] | None = None
    prior_weights: Mapping[tuple[int, ...], float] | None = None

    def __post_init__(self) -> None:
        if not self.scenario_id:
            raise ValueError("scenario_id must be non-empty")
        if not isfinite(self.weight) or self.weight <= 0.0:
            raise ValueError("scenario weight must be finite and positive")
        channel_map = dict(self.channels or {})
        unknown_channels = set(channel_map) - set(self.truth_model.trait_true_states)
        if unknown_channels:
            raise ValueError(f"channels refer to unknown truth-table traits: {sorted(unknown_channels)}")
        if self.prior_weights is not None:
            if set(self.prior_weights) != set(self.truth_model.states):
                raise ValueError("prior_weights must contain exactly the feasible truth states")
            if any(weight < 0.0 or not isfinite(weight) for weight in self.prior_weights.values()):
                raise ValueError("prior weights must be finite and non-negative")
            if sum(self.prior_weights.values()) <= 0.0:
                raise ValueError("prior weights must have positive total mass")


@dataclass(frozen=True)
class ScenarioPanelRisk:
    """One panel's exact observation probability and focal-OFF posterior in one scenario."""

    scenario_id: str
    report_probability: float
    focal_off_probability: float | None


@dataclass(frozen=True)
class RobustPanelResult:
    """A structurally resolving panel together with finite-scenario risk summaries."""

    objective: RobustObjective
    focal_mechanism: int
    target_trait: str
    selected_null_traits: tuple[str, ...]
    total_cost: float
    scenario_risks: tuple[ScenarioPanelRisk, ...]
    worst_case_risk: float
    weighted_mean_risk: float


@dataclass(frozen=True)
class PanelStrategyComparison:
    """Minimum-cost, coverage-greedy, minimax, and mean-risk panel selections."""

    minimum_cost: RobustPanelResult | None
    coverage_greedy: RobustPanelResult | None
    minimax: RobustPanelResult | None
    weighted_mean: RobustPanelResult | None


def _validate_inputs(
    declared_model: StructuralModel,
    *,
    focal_mechanism: int,
    target_trait: str,
    candidates: Iterable[NullObservationCandidate],
    scenarios: Iterable[FinitePanelScenario],
) -> tuple[tuple[NullObservationCandidate, ...], tuple[FinitePanelScenario, ...]]:
    if focal_mechanism not in range(declared_model.mechanism_count):
        raise ValueError("focal mechanism index is out of range")
    if target_trait not in declared_model.driver_sets:
        raise ValueError(f"unknown target trait: {target_trait!r}")
    if focal_mechanism not in declared_model.driver_sets[target_trait]:
        raise ValueError("focal mechanism must drive the target trait")
    candidate_tuple = tuple(candidates)
    names = [candidate.trait for candidate in candidate_tuple]
    if len(set(names)) != len(names):
        raise ValueError("candidate traits must be unique")
    unknown = set(names) - set(declared_model.driver_sets)
    if unknown:
        raise ValueError(f"unknown candidate traits: {sorted(unknown)}")
    if target_trait in names:
        raise ValueError("the target trait cannot be a NULL candidate")
    scenario_tuple = tuple(scenarios)
    if not scenario_tuple:
        raise ValueError("at least one finite panel scenario is required")
    ids = [scenario.scenario_id for scenario in scenario_tuple]
    if len(set(ids)) != len(ids):
        raise ValueError("scenario IDs must be unique")
    for scenario in scenario_tuple:
        if scenario.truth_model.mechanism_count != declared_model.mechanism_count:
            raise ValueError("every scenario truth model must match declared mechanism_count")
        required_traits = {target_trait, *names}
        missing = required_traits - set(scenario.truth_model.trait_true_states)
        if missing:
            raise ValueError(
                f"scenario {scenario.scenario_id!r} lacks truth tables for traits: {sorted(missing)}"
            )
    return candidate_tuple, scenario_tuple


def _scenario_risk(
    scenario: FinitePanelScenario,
    *,
    focal_mechanism: int,
    target_trait: str,
    null_traits: tuple[str, ...],
) -> ScenarioPanelRisk:
    truth = scenario.truth_model
    weights = (
        dict(scenario.prior_weights)
        if scenario.prior_weights is not None
        else {state: 1.0 for state in truth.states}
    )
    channels = dict(scenario.channels or {})
    denominator = 0.0
    focal_off = 0.0
    total_prior = sum(weights.values())
    for state in truth.states:
        if not truth.trait_is_present(target_trait, state):
            continue
        likelihood = 1.0
        for trait in null_traits:
            channel = channels.get(trait, BinaryObservationChannel())
            likelihood *= channel.likelihood(
                reported_present=False,
                true_present=truth.trait_is_present(trait, state),
            )
        mass = weights[state] * likelihood
        denominator += mass
        if state[focal_mechanism] == 0:
            focal_off += mass
    return ScenarioPanelRisk(
        scenario_id=scenario.scenario_id,
        report_probability=denominator / total_prior,
        focal_off_probability=None if denominator == 0.0 else focal_off / denominator,
    )


def evaluate_resolving_panel(
    declared_model: StructuralModel,
    *,
    focal_mechanism: int,
    target_trait: str,
    selected_candidates: Iterable[NullObservationCandidate],
    scenarios: Iterable[FinitePanelScenario],
    objective: RobustObjective = RobustObjective.MINIMAX,
) -> RobustPanelResult:
    """Evaluate one structurally resolving panel across finite true scenarios."""
    candidates, scenario_tuple = _validate_inputs(
        declared_model,
        focal_mechanism=focal_mechanism,
        target_trait=target_trait,
        candidates=selected_candidates,
        scenarios=scenarios,
    )
    selected_traits = tuple(candidate.trait for candidate in candidates)
    observation = Observation(present=(target_trait,), null=selected_traits)
    if not forced_on_by_theorem(declared_model, observation, focal_mechanism):
        raise ValueError("selected panel does not force the focal mechanism ON in the declared model")
    risks = tuple(
        _scenario_risk(
            scenario,
            focal_mechanism=focal_mechanism,
            target_trait=target_trait,
            null_traits=selected_traits,
        )
        for scenario in scenario_tuple
    )
    # A zero-probability report is a contradiction alarm, not zero risk. Rank it
    # as maximally unsafe so a robust selector cannot win by selecting impossible panels.
    numeric_risks = tuple(
        1.0 if risk.focal_off_probability is None else risk.focal_off_probability
        for risk in risks
    )
    total_weight = sum(scenario.weight for scenario in scenario_tuple)
    weighted_mean = sum(
        scenario.weight * risk
        for scenario, risk in zip(scenario_tuple, numeric_risks)
    ) / total_weight
    return RobustPanelResult(
        objective=objective,
        focal_mechanism=focal_mechanism,
        target_trait=target_trait,
        selected_null_traits=selected_traits,
        total_cost=sum(candidate.cost for candidate in candidates),
        scenario_risks=risks,
        worst_case_risk=max(numeric_risks),
        weighted_mean_risk=weighted_mean,
    )


def _resolving_subsets(
    declared_model: StructuralModel,
    *,
    focal_mechanism: int,
    target_trait: str,
    candidates: tuple[NullObservationCandidate, ...],
    max_cost: float | None,
) -> tuple[tuple[NullObservationCandidate, ...], ...]:
    if max_cost is not None and (not isfinite(max_cost) or max_cost < 0.0):
        raise ValueError("max_cost must be finite and non-negative")
    resolving: list[tuple[NullObservationCandidate, ...]] = []
    for size in range(len(candidates) + 1):
        for subset in combinations(candidates, size):
            cost = sum(candidate.cost for candidate in subset)
            if max_cost is not None and cost > max_cost:
                continue
            observation = Observation(present=(target_trait,), null=tuple(candidate.trait for candidate in subset))
            if forced_on_by_theorem(declared_model, observation, focal_mechanism):
                resolving.append(subset)
    return tuple(resolving)


def choose_robust_panel(
    declared_model: StructuralModel,
    *,
    focal_mechanism: int,
    target_trait: str,
    candidates: Iterable[NullObservationCandidate],
    scenarios: Iterable[FinitePanelScenario],
    objective: RobustObjective = RobustObjective.MINIMAX,
    max_cost: float | None = None,
) -> RobustPanelResult | None:
    """Choose an exact finite-scenario robust panel among all resolving subsets.

    Tie-breaking is deterministic: primary objective, secondary objective,
    total cost, panel cardinality, then lexical trait order. Contradictory
    zero-probability reports are treated as risk one for ranking.
    """
    candidate_tuple, scenario_tuple = _validate_inputs(
        declared_model,
        focal_mechanism=focal_mechanism,
        target_trait=target_trait,
        candidates=candidates,
        scenarios=scenarios,
    )
    results = [
        evaluate_resolving_panel(
            declared_model,
            focal_mechanism=focal_mechanism,
            target_trait=target_trait,
            selected_candidates=subset,
            scenarios=scenario_tuple,
            objective=objective,
        )
        for subset in _resolving_subsets(
            declared_model,
            focal_mechanism=focal_mechanism,
            target_trait=target_trait,
            candidates=candidate_tuple,
            max_cost=max_cost,
        )
    ]
    if not results:
        return None
    if objective is RobustObjective.MINIMAX:
        key = lambda result: (
            result.worst_case_risk,
            result.weighted_mean_risk,
            result.total_cost,
            len(result.selected_null_traits),
            result.selected_null_traits,
        )
    elif objective is RobustObjective.WEIGHTED_MEAN:
        key = lambda result: (
            result.weighted_mean_risk,
            result.worst_case_risk,
            result.total_cost,
            len(result.selected_null_traits),
            result.selected_null_traits,
        )
    else:
        raise ValueError("objective must be a RobustObjective")
    return min(results, key=key)


def choose_minimum_cost_panel(
    declared_model: StructuralModel,
    *,
    focal_mechanism: int,
    target_trait: str,
    candidates: Iterable[NullObservationCandidate],
    scenarios: Iterable[FinitePanelScenario],
    max_cost: float | None = None,
) -> RobustPanelResult | None:
    """Choose the cheapest structurally resolving panel, with risk as a tie-breaker."""
    candidate_tuple, scenario_tuple = _validate_inputs(
        declared_model,
        focal_mechanism=focal_mechanism,
        target_trait=target_trait,
        candidates=candidates,
        scenarios=scenarios,
    )
    results = [
        evaluate_resolving_panel(
            declared_model,
            focal_mechanism=focal_mechanism,
            target_trait=target_trait,
            selected_candidates=subset,
            scenarios=scenario_tuple,
            objective=RobustObjective.MINIMAX,
        )
        for subset in _resolving_subsets(
            declared_model,
            focal_mechanism=focal_mechanism,
            target_trait=target_trait,
            candidates=candidate_tuple,
            max_cost=max_cost,
        )
    ]
    if not results:
        return None
    return min(
        results,
        key=lambda result: (
            result.total_cost,
            result.worst_case_risk,
            result.weighted_mean_risk,
            len(result.selected_null_traits),
            result.selected_null_traits,
        ),
    )


def choose_coverage_greedy_panel(
    declared_model: StructuralModel,
    *,
    focal_mechanism: int,
    target_trait: str,
    candidates: Iterable[NullObservationCandidate],
    scenarios: Iterable[FinitePanelScenario],
    max_cost: float | None = None,
) -> RobustPanelResult | None:
    """Select witnesses by declared competitor elimination gain per unit cost.

    This is a conventional coverage-style greedy baseline, unlike strict greedy:
    it can collect individually non-resolving observations. It knows only the
    declared driver sets and costs, not true-scenario risks.
    """
    candidate_tuple, scenario_tuple = _validate_inputs(
        declared_model,
        focal_mechanism=focal_mechanism,
        target_trait=target_trait,
        candidates=candidates,
        scenarios=scenarios,
    )
    if max_cost is not None and (not isfinite(max_cost) or max_cost < 0.0):
        raise ValueError("max_cost must be finite and non-negative")
    selected: list[NullObservationCandidate] = []
    remaining = list(candidate_tuple)
    survivors = set(declared_model.driver_sets[target_trait]) - {focal_mechanism}
    while survivors and remaining:
        options: list[tuple[float, int, float, str, NullObservationCandidate]] = []
        for candidate in remaining:
            if max_cost is not None and sum(item.cost for item in selected) + candidate.cost > max_cost:
                continue
            eliminated = survivors & set(declared_model.driver_sets[candidate.trait])
            gain = len(eliminated)
            if gain:
                options.append((-gain / candidate.cost, -gain, candidate.cost, candidate.trait, candidate))
        if not options:
            break
        _, _, _, _, chosen = min(options)
        selected.append(chosen)
        remaining.remove(chosen)
        survivors -= set(declared_model.driver_sets[chosen.trait])
    observation = Observation(present=(target_trait,), null=tuple(item.trait for item in selected))
    if not forced_on_by_theorem(declared_model, observation, focal_mechanism):
        return None
    return evaluate_resolving_panel(
        declared_model,
        focal_mechanism=focal_mechanism,
        target_trait=target_trait,
        selected_candidates=tuple(selected),
        scenarios=scenario_tuple,
        objective=RobustObjective.MINIMAX,
    )


def compare_panel_selection_strategies(
    declared_model: StructuralModel,
    *,
    focal_mechanism: int,
    target_trait: str,
    candidates: Iterable[NullObservationCandidate],
    scenarios: Iterable[FinitePanelScenario],
    max_cost: float | None = None,
) -> PanelStrategyComparison:
    """Return cost-first, coverage-greedy, minimax, and mean-risk selections."""
    candidate_tuple, scenario_tuple = _validate_inputs(
        declared_model,
        focal_mechanism=focal_mechanism,
        target_trait=target_trait,
        candidates=candidates,
        scenarios=scenarios,
    )
    return PanelStrategyComparison(
        minimum_cost=choose_minimum_cost_panel(
            declared_model,
            focal_mechanism=focal_mechanism,
            target_trait=target_trait,
            candidates=candidate_tuple,
            scenarios=scenario_tuple,
            max_cost=max_cost,
        ),
        coverage_greedy=choose_coverage_greedy_panel(
            declared_model,
            focal_mechanism=focal_mechanism,
            target_trait=target_trait,
            candidates=candidate_tuple,
            scenarios=scenario_tuple,
            max_cost=max_cost,
        ),
        minimax=choose_robust_panel(
            declared_model,
            focal_mechanism=focal_mechanism,
            target_trait=target_trait,
            candidates=candidate_tuple,
            scenarios=scenario_tuple,
            objective=RobustObjective.MINIMAX,
            max_cost=max_cost,
        ),
        weighted_mean=choose_robust_panel(
            declared_model,
            focal_mechanism=focal_mechanism,
            target_trait=target_trait,
            candidates=candidate_tuple,
            scenarios=scenario_tuple,
            objective=RobustObjective.WEIGHTED_MEAN,
            max_cost=max_cost,
        ),
    )
