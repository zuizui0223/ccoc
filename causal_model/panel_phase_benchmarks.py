"""Exact multi-competitor observation-panel benchmarks.

This module compares two declared-model selection strategies in a canonical
multi-competitor setting:

* ``exact`` uses :func:`minimum_discriminating_panel` and can select a joint
  NULL panel; and
* ``strict_greedy`` adds a witness only when that one step immediately makes the
  focal driver forced ON.

The true generator has a shared environmental context that induces correlation
among competitors, latent target routes, and witness inhibition. All posterior
risks are weighted finite sums, not Monte Carlo estimates.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product
from math import prod
from typing import Iterable, Mapping

from .observation_design import NullObservationCandidate, minimum_discriminating_panel
from .replaceability import Observation, StructuralModel, forced_on_by_theorem


class PanelStrategy(str, Enum):
    """Declared-model observation-panel selection policy."""

    EXACT = "exact"
    STRICT_GREEDY = "strict_greedy"


@dataclass(frozen=True)
class MultiCompetitorFamilyParameters:
    """Finite true-generator parameters for a focal driver and multiple competitors.

    Competitors and latent routes are independent conditional on one binary
    environment. Their conditional probabilities differ between low and high
    environment, which induces marginal correlation. Inhibition is likewise
    conditionally independent across witnesses.
    """

    competitor_count: int = 2
    latent_route_count: int = 0
    focal_on_probability: float = 0.5
    environment_high_probability: float = 0.5
    competitor_on_probability_low: float = 0.5
    competitor_on_probability_high: float = 0.5
    latent_on_probability_low: float = 0.0
    latent_on_probability_high: float = 0.0
    inhibition_probability_low: float = 0.0
    inhibition_probability_high: float = 0.0
    witness_sensitivity: float = 1.0
    witness_false_positive_rate: float = 0.0
    conjunction_context_prevalence: float = 0.0

    def __post_init__(self) -> None:
        if self.competitor_count < 2:
            raise ValueError("competitor_count must be at least two")
        if self.latent_route_count < 0:
            raise ValueError("latent_route_count must be non-negative")
        probabilities = {
            name: value
            for name, value in self.__dict__.items()
            if name not in {"competitor_count", "latent_route_count"}
        }
        for name, value in probabilities.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must lie between zero and one")


@dataclass(frozen=True)
class PanelStrategyResult:
    """Declared conclusion and true-generator risk for one selected panel."""

    strategy: PanelStrategy
    selected_null_traits: tuple[str, ...]
    declared_forced_on: bool
    reported_panel_probability: float
    posterior_focal_off_probability: float | None
    perfect_measurement_focal_off_probability: float | None

    @property
    def false_necessity_risk(self) -> float | None:
        """Risk is meaningful only when the declared strategy makes a necessity claim."""
        if not self.declared_forced_on:
            return None
        return self.posterior_focal_off_probability


@dataclass(frozen=True)
class MultiCompetitorPanelComparison:
    """Exact and strict-greedy panel results at one true-generator parameter point."""

    parameters: MultiCompetitorFamilyParameters
    exact: PanelStrategyResult
    strict_greedy: PanelStrategyResult

    @property
    def synergy_gap(self) -> int:
        """Number of observations exact uses beyond strict greedy."""
        return len(self.exact.selected_null_traits) - len(self.strict_greedy.selected_null_traits)


# State = focal, environment, competitors..., latent routes..., inhibition flags..., conjunction-context
MultiState = tuple[int, ...]


def _bernoulli(value: int, probability_one: float) -> float:
    return probability_one if value else 1.0 - probability_one


def declared_multi_competitor_model(competitor_count: int) -> StructuralModel:
    """Build the declared focal-plus-private-witness OR grammar."""
    if competitor_count < 2:
        raise ValueError("competitor_count must be at least two")
    drivers: dict[str, frozenset[int]] = {
        "target": frozenset(range(competitor_count + 1)),
    }
    for competitor in range(1, competitor_count + 1):
        drivers[f"witness_{competitor}"] = frozenset({competitor})
    return StructuralModel(mechanism_count=competitor_count + 1, driver_sets=drivers)


def _candidate_traits(parameters: MultiCompetitorFamilyParameters) -> tuple[str, ...]:
    return tuple(f"witness_{index}" for index in range(1, parameters.competitor_count + 1))


def _exact_panel_traits(parameters: MultiCompetitorFamilyParameters) -> tuple[str, ...]:
    model = declared_multi_competitor_model(parameters.competitor_count)
    result = minimum_discriminating_panel(
        model,
        focal_mechanism=0,
        target_trait="target",
        candidates=tuple(NullObservationCandidate(trait) for trait in _candidate_traits(parameters)),
    )
    if result is None:
        raise RuntimeError("canonical multi-competitor declared model must admit an exact panel")
    return result.selected_null_traits


def strict_greedy_panel_traits(parameters: MultiCompetitorFamilyParameters) -> tuple[str, ...]:
    """Use strict one-step resolution gain, intentionally exposing synergy failure.

    A candidate is selected only when adding it immediately changes the declared
    focal status from not-forced to forced ON. In the private-witness canonical
    family every singleton has zero gain, hence strict greedy stops before the
    jointly resolving panel.
    """
    model = declared_multi_competitor_model(parameters.competitor_count)
    selected: tuple[str, ...] = ()
    remaining = list(_candidate_traits(parameters))
    while remaining:
        baseline = Observation(present=("target",), null=selected)
        if forced_on_by_theorem(model, baseline, 0):
            break
        resolving = []
        for trait in remaining:
            proposal = Observation(present=("target",), null=tuple((*selected, trait)))
            if forced_on_by_theorem(model, proposal, 0):
                resolving.append(trait)
        if not resolving:
            break
        chosen = min(resolving)
        selected = tuple((*selected, chosen))
        remaining.remove(chosen)
    return selected


def _state_distribution(parameters: MultiCompetitorFamilyParameters) -> dict[MultiState, float]:
    """Return the normalized exact distribution over the finite correlated generator."""
    weights: dict[MultiState, float] = {}
    n = parameters.competitor_count
    m = parameters.latent_route_count
    for focal, environment, conjunctive in product((0, 1), repeat=3):
        environment_probability = _bernoulli(environment, parameters.environment_high_probability)
        core_probability = _bernoulli(focal, parameters.focal_on_probability)
        conjunction_probability = _bernoulli(conjunctive, parameters.conjunction_context_prevalence)
        competitor_probability = (
            parameters.competitor_on_probability_high
            if environment
            else parameters.competitor_on_probability_low
        )
        latent_probability = (
            parameters.latent_on_probability_high
            if environment
            else parameters.latent_on_probability_low
        )
        inhibition_probability = (
            parameters.inhibition_probability_high
            if environment
            else parameters.inhibition_probability_low
        )
        for competitors in product((0, 1), repeat=n):
            competitor_weight = prod(_bernoulli(value, competitor_probability) for value in competitors)
            for latent_routes in product((0, 1), repeat=m):
                latent_weight = prod(_bernoulli(value, latent_probability) for value in latent_routes)
                for inhibited in product((0, 1), repeat=n):
                    inhibition_weight = prod(_bernoulli(value, inhibition_probability) for value in inhibited)
                    state = (focal, environment, *competitors, *latent_routes, *inhibited, conjunctive)
                    weights[state] = (
                        environment_probability
                        * core_probability
                        * conjunction_probability
                        * competitor_weight
                        * latent_weight
                        * inhibition_weight
                    )
    total = sum(weights.values())
    if total == 0.0:
        raise RuntimeError("multi-competitor generator produced zero total mass")
    return {state: weight / total for state, weight in weights.items() if weight > 0.0}


def _decode(state: MultiState, parameters: MultiCompetitorFamilyParameters) -> tuple[int, tuple[int, ...], tuple[int, ...], tuple[int, ...], int]:
    n = parameters.competitor_count
    m = parameters.latent_route_count
    focal = state[0]
    competitors = state[2 : 2 + n]
    latent_start = 2 + n
    latent_routes = state[latent_start : latent_start + m]
    inhibition_start = latent_start + m
    inhibited = state[inhibition_start : inhibition_start + n]
    conjunctive = state[-1]
    return focal, competitors, latent_routes, inhibited, conjunctive


def _target_present(state: MultiState, parameters: MultiCompetitorFamilyParameters) -> bool:
    focal, competitors, latent_routes, _, conjunctive = _decode(state, parameters)
    competitor_any = any(competitors)
    declared_core = bool(focal and competitor_any) if conjunctive else bool(focal or competitor_any)
    return bool(declared_core or any(latent_routes))


def _true_witness_present(state: MultiState, parameters: MultiCompetitorFamilyParameters, competitor_index: int) -> bool:
    _, competitors, _, inhibited, _ = _decode(state, parameters)
    return bool(competitors[competitor_index] and not inhibited[competitor_index])


def _reported_null_likelihood(true_witness_present: bool, parameters: MultiCompetitorFamilyParameters) -> float:
    return (
        1.0 - parameters.witness_sensitivity
        if true_witness_present
        else 1.0 - parameters.witness_false_positive_rate
    )


def _evaluate_selected_panel(
    parameters: MultiCompetitorFamilyParameters,
    *,
    strategy: PanelStrategy,
    selected_null_traits: tuple[str, ...],
) -> PanelStrategyResult:
    model = declared_multi_competitor_model(parameters.competitor_count)
    observation = Observation(present=("target",), null=selected_null_traits)
    declared_forced = forced_on_by_theorem(model, observation, 0)
    indices = tuple(int(trait.removeprefix("witness_")) - 1 for trait in selected_null_traits)

    reported_total = 0.0
    reported_off = 0.0
    perfect_total = 0.0
    perfect_off = 0.0
    for state, prior_weight in _state_distribution(parameters).items():
        if not _target_present(state, parameters):
            continue
        likelihood = 1.0
        all_true_null = True
        for index in indices:
            witness_present = _true_witness_present(state, parameters, index)
            likelihood *= _reported_null_likelihood(witness_present, parameters)
            all_true_null = all_true_null and not witness_present
        reported_mass = prior_weight * likelihood
        reported_total += reported_mass
        if state[0] == 0:
            reported_off += reported_mass
        if all_true_null:
            perfect_total += prior_weight
            if state[0] == 0:
                perfect_off += prior_weight

    return PanelStrategyResult(
        strategy=strategy,
        selected_null_traits=selected_null_traits,
        declared_forced_on=declared_forced,
        reported_panel_probability=reported_total,
        posterior_focal_off_probability=(None if reported_total == 0.0 else reported_off / reported_total),
        perfect_measurement_focal_off_probability=(None if perfect_total == 0.0 else perfect_off / perfect_total),
    )


def compare_panel_strategies(parameters: MultiCompetitorFamilyParameters) -> MultiCompetitorPanelComparison:
    """Compare exact joint-panel selection with strict one-step greedy selection."""
    exact_traits = _exact_panel_traits(parameters)
    greedy_traits = strict_greedy_panel_traits(parameters)
    return MultiCompetitorPanelComparison(
        parameters=parameters,
        exact=_evaluate_selected_panel(
            parameters,
            strategy=PanelStrategy.EXACT,
            selected_null_traits=exact_traits,
        ),
        strict_greedy=_evaluate_selected_panel(
            parameters,
            strategy=PanelStrategy.STRICT_GREEDY,
            selected_null_traits=greedy_traits,
        ),
    )


def sweep_panel_phase_family(
    parameter_grid: Mapping[str, Iterable[float | int]],
) -> tuple[MultiCompetitorPanelComparison, ...]:
    """Evaluate exact-versus-greedy comparisons across a Cartesian parameter grid."""
    allowed = set(MultiCompetitorFamilyParameters.__dataclass_fields__)
    unknown = set(parameter_grid) - allowed
    if unknown:
        raise ValueError(f"unknown family parameters: {sorted(unknown)}")
    names = tuple(sorted(parameter_grid))
    value_sets = tuple(tuple(parameter_grid[name]) for name in names)
    if any(not values for values in value_sets):
        raise ValueError("every parameter grid entry must contain at least one value")
    return tuple(
        compare_panel_strategies(MultiCompetitorFamilyParameters(**dict(zip(names, values))))
        for values in product(*value_sets)
    )


def panel_phase_table_markdown(
    comparisons: Iterable[MultiCompetitorPanelComparison],
    *,
    digits: int = 4,
) -> str:
    """Render multi-competitor strategy comparisons as compact Markdown."""
    if digits < 0:
        raise ValueError("digits must be non-negative")
    rows = [
        "| competitors | latent routes | p(comp low) | p(comp high) | sensitivity | exact panel | greedy panel | exact claim | greedy claim | exact risk | greedy conditional off |",
        "|---:|---:|---:|---:|---:|---|---|---|---|---:|---:|",
    ]
    for comparison in comparisons:
        p = comparison.parameters
        exact = comparison.exact
        greedy = comparison.strict_greedy
        exact_risk = "impossible" if exact.false_necessity_risk is None else f"{exact.false_necessity_risk:.{digits}f}"
        greedy_off = (
            "impossible"
            if greedy.posterior_focal_off_probability is None
            else f"{greedy.posterior_focal_off_probability:.{digits}f}"
        )
        rows.append(
            "| "
            + " | ".join(
                (
                    str(p.competitor_count),
                    str(p.latent_route_count),
                    f"{p.competitor_on_probability_low:.{digits}f}",
                    f"{p.competitor_on_probability_high:.{digits}f}",
                    f"{p.witness_sensitivity:.{digits}f}",
                    ", ".join(exact.selected_null_traits) or "—",
                    ", ".join(greedy.selected_null_traits) or "—",
                    str(exact.declared_forced_on),
                    str(greedy.declared_forced_on),
                    exact_risk,
                    greedy_off,
                )
            )
            + " |"
        )
    return "\n".join(rows)
