"""Exact minimum-cost NULL-observation panels for the disjunctive theorem core."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

from .replaceability import (
    Observation,
    StructuralModel,
    forced_on_by_theorem,
    is_last_driver_standing,
    null_eliminated_mechanisms,
    observation_is_admissible,
)


@dataclass(frozen=True)
class NullObservationCandidate:
    """A feasible NULL observation and its non-negative acquisition cost."""

    trait: str
    cost: float = 1.0

    def __post_init__(self) -> None:
        if not self.trait:
            raise ValueError("candidate trait must be non-empty")
        if not isfinite(self.cost) or self.cost < 0.0:
            raise ValueError("candidate cost must be finite and non-negative")


@dataclass(frozen=True)
class MinimumPanel:
    """An exact minimum-cost panel that makes one focal mechanism indispensable."""

    focal_mechanism: int
    target_trait: str
    selected_null_traits: tuple[str, ...]
    total_cost: float
    observation: Observation
    eliminated_mechanisms: frozenset[int]


def _ranking(cost: float, traits: tuple[str, ...]) -> tuple[float, int, tuple[str, ...]]:
    return (cost, len(traits), traits)


def minimum_discriminating_panel(
    model: StructuralModel,
    *,
    focal_mechanism: int,
    target_trait: str,
    candidates: Iterable[NullObservationCandidate],
    base_observation: Observation = Observation(),
) -> MinimumPanel | None:
    """Find the exact minimum-cost NULL panel that makes ``focal_mechanism`` forced ON.

    ``target_trait`` is required present in the returned observation. Candidate NULL
    observations eliminate the full driver set of their trait. The search is exact:
    dynamic-programming states are the total eliminated-mechanism sets, retaining
    the cheapest panel for each set. A returned solution also preserves feasibility
    of every required-present trait in ``base_observation``.

    ``None`` means no candidate panel can make the focal mechanism indispensable
    without contradicting the declared observation model.
    """
    if focal_mechanism not in range(model.mechanism_count):
        raise ValueError("focal mechanism index is out of range")
    if target_trait not in model.driver_sets:
        raise ValueError(f"unknown target trait: {target_trait!r}")
    if focal_mechanism not in model.driver_sets[target_trait]:
        raise ValueError("focal mechanism must drive the target trait")
    unknown_base = (set(base_observation.present) | set(base_observation.null)) - set(model.driver_sets)
    if unknown_base:
        raise ValueError(f"observation refers to unknown traits: {sorted(unknown_base)}")
    if target_trait in base_observation.null:
        raise ValueError("target trait cannot be both required-present and required-null")

    present = tuple(dict.fromkeys((*base_observation.present, target_trait)))
    baseline = Observation(present=present, null=base_observation.null)
    base_eliminated = null_eliminated_mechanisms(model, baseline)
    if focal_mechanism in base_eliminated or not observation_is_admissible(model, baseline):
        return None

    candidate_tuple = tuple(candidates)
    traits = [candidate.trait for candidate in candidate_tuple]
    if len(set(traits)) != len(traits):
        raise ValueError("candidate traits must be unique")

    usable: list[NullObservationCandidate] = []
    for candidate in candidate_tuple:
        if candidate.trait not in model.driver_sets:
            raise ValueError(f"candidate refers to unknown trait: {candidate.trait!r}")
        if candidate.trait in present:
            raise ValueError(
                f"candidate NULL observation conflicts with required-present trait: {candidate.trait!r}"
            )
        if candidate.trait in baseline.null:
            continue
        drivers = model.driver_sets[candidate.trait]
        if focal_mechanism in drivers or drivers <= base_eliminated:
            continue
        usable.append(candidate)

    usable.sort(key=lambda candidate: candidate.trait)
    states: dict[frozenset[int], tuple[float, tuple[str, ...]]] = {
        base_eliminated: (0.0, ())
    }
    for candidate in usable:
        prior_states = tuple(states.items())
        driver_set = model.driver_sets[candidate.trait]
        for eliminated, (cost, selected) in prior_states:
            next_eliminated = frozenset(set(eliminated) | set(driver_set))
            next_selected = tuple(sorted((*selected, candidate.trait)))
            proposed = (cost + candidate.cost, next_selected)
            incumbent = states.get(next_eliminated)
            if incumbent is None or _ranking(*proposed) < _ranking(*incumbent):
                states[next_eliminated] = proposed

    best: MinimumPanel | None = None
    for eliminated, (cost, selected) in states.items():
        if focal_mechanism in eliminated:
            continue
        observation = Observation(present=present, null=tuple((*baseline.null, *selected)))
        if not observation_is_admissible(model, observation):
            continue
        support = is_last_driver_standing(model, observation, focal_mechanism)
        if target_trait not in support or not forced_on_by_theorem(model, observation, focal_mechanism):
            continue
        candidate_solution = MinimumPanel(
            focal_mechanism=focal_mechanism,
            target_trait=target_trait,
            selected_null_traits=selected,
            total_cost=cost,
            observation=observation,
            eliminated_mechanisms=eliminated,
        )
        if best is None or _ranking(candidate_solution.total_cost, candidate_solution.selected_null_traits) < _ranking(
            best.total_cost, best.selected_null_traits
        ):
            best = candidate_solution
    return best
