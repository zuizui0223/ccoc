"""Exact causal-replaceability theorems for finite disjunctive models.

The module deliberately separates a mathematical claim from a claim about nature.
A :class:`StructuralModel` fixes a finite candidate set of mechanisms and the
observable traits each mechanism can produce. An observation declares traits to
be PRESENT or NULL. Under sign-consistent disjunctive semantics,

    cline(t) <=> OR_{k in D(t)} s_k,

where ``D(t)`` is the driver set of trait ``t`` and ``s_k`` is a binary mechanism
switch.

The exact theorem assumes that every switch assignment compatible with the
observation clauses is structurally feasible. In particular, the model contains
no hidden mutual exclusions, resource budgets, inhibitory effects, conjunctions,
or other cross-mechanism constraints.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log2, prod
from typing import Iterable, Mapping


@dataclass(frozen=True)
class StructuralModel:
    """Finite causal candidate set with a driver set for each observable trait."""

    mechanism_count: int
    driver_sets: Mapping[str, frozenset[int]]

    def __post_init__(self) -> None:
        if self.mechanism_count < 1:
            raise ValueError("mechanism_count must be positive")
        if not self.driver_sets:
            raise ValueError("driver_sets must not be empty")
        allowed = set(range(self.mechanism_count))
        for trait, drivers in self.driver_sets.items():
            if not trait:
                raise ValueError("trait names must be non-empty")
            if not drivers:
                raise ValueError(f"driver set for {trait!r} must not be empty")
            if not set(drivers) <= allowed:
                raise ValueError(f"driver set for {trait!r} contains invalid mechanism index")


@dataclass(frozen=True)
class Observation:
    """Required-present and required-null trait outcomes in a structural experiment."""

    present: tuple[str, ...] = ()
    null: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        overlap = set(self.present) & set(self.null)
        if overlap:
            raise ValueError(f"a trait cannot be both present and null: {sorted(overlap)}")


@dataclass(frozen=True)
class TheoremACertificate:
    """Exact certificate for whether one mechanism is structurally indispensable."""

    mechanism: int
    admissible_configuration_count: int
    forced_on: bool
    last_driver_standing: bool
    supporting_traits: tuple[str, ...]
    holds: bool


def _validate_observation(model: StructuralModel, observation: Observation) -> None:
    unknown = (set(observation.present) | set(observation.null)) - set(model.driver_sets)
    if unknown:
        raise ValueError(f"observation refers to unknown traits: {sorted(unknown)}")


def null_eliminated_mechanisms(model: StructuralModel, observation: Observation) -> frozenset[int]:
    """Return ``NullOff(O)``: switches forced OFF by declared NULL observations."""
    _validate_observation(model, observation)
    eliminated: set[int] = set()
    for trait in observation.null:
        eliminated.update(model.driver_sets[trait])
    return frozenset(eliminated)


def observation_is_admissible(model: StructuralModel, observation: Observation) -> bool:
    """Whether the observation has at least one compatible structural state.

    Under the declared unconstrained monotone-OR semantics, an observation is
    feasible exactly when every required-present trait retains at least one
    driver after the NULL observations have eliminated their driver sets.
    """
    _validate_observation(model, observation)
    eliminated = null_eliminated_mechanisms(model, observation)
    return all(model.driver_sets[trait] - eliminated for trait in observation.present)


def admissible_configurations(
    model: StructuralModel,
    observation: Observation,
) -> tuple[tuple[int, ...], ...]:
    """Enumerate the exact structural admissible region ``A(O)``.

    Enumeration is intentional: this is a finite theorem core for small candidate
    sets, not a surrogate for a continuous ecological model.
    """
    _validate_observation(model, observation)
    eliminated = null_eliminated_mechanisms(model, observation)
    configurations: list[tuple[int, ...]] = []
    for state in product((0, 1), repeat=model.mechanism_count):
        if any(state[k] for k in eliminated):
            continue
        if all(any(state[k] for k in model.driver_sets[trait]) for trait in observation.present):
            configurations.append(state)
    return tuple(configurations)


def forced_off(configurations: Iterable[tuple[int, ...]], mechanism: int) -> bool:
    """Whether a mechanism is OFF in every configuration of a non-empty region."""
    configs = tuple(configurations)
    return bool(configs) and all(state[mechanism] == 0 for state in configs)


def forced_on(configurations: Iterable[tuple[int, ...]], mechanism: int) -> bool:
    """Whether a mechanism is ON in every configuration of a non-empty region."""
    configs = tuple(configurations)
    return bool(configs) and all(state[mechanism] == 1 for state in configs)


def is_last_driver_standing(
    model: StructuralModel,
    observation: Observation,
    mechanism: int,
) -> tuple[str, ...]:
    """Return present traits for which ``mechanism`` is the sole uneliminated driver.

    This is a local driver-set relation. If the whole observation is infeasible,
    use :func:`forced_on_by_theorem`, which also checks admissibility.
    """
    if mechanism not in range(model.mechanism_count):
        raise ValueError("mechanism index is out of range")
    eliminated = null_eliminated_mechanisms(model, observation)
    support: list[str] = []
    for trait in observation.present:
        drivers = model.driver_sets[trait]
        if mechanism in drivers and (drivers - {mechanism}) <= eliminated:
            support.append(trait)
    return tuple(support)


def forced_on_by_theorem(
    model: StructuralModel,
    observation: Observation,
    mechanism: int,
) -> bool:
    """Apply Theorem A without enumerating all Boolean configurations.

    ``True`` means that the observation is feasible and the mechanism is the last
    surviving driver of at least one required-present trait. This is equivalent to
    :func:`forced_on` on ``admissible_configurations(model, observation)`` under
    the declared unconstrained monotone-OR semantics.
    """
    if mechanism not in range(model.mechanism_count):
        raise ValueError("mechanism index is out of range")
    if not observation_is_admissible(model, observation):
        return False
    return bool(is_last_driver_standing(model, observation, mechanism))


def structural_crc(
    mechanism: int,
    configurations: Iterable[tuple[int, ...]],
    prior_on_probability: float = 0.5,
) -> float:
    """Absolute OFF-state surprisal under an independent Bernoulli prior.

    The returned quantity is ``-log2 P(s_j = 0 | s in A(O))``. ``inf`` means
    that setting the mechanism OFF is impossible inside the structural admissible
    region. ``nan`` denotes an empty admissible region. This is an absolute
    conditional surprisal; it is not yet a baseline-adjusted evidence measure.
    """
    configs = tuple(configurations)
    if not configs:
        return float("nan")
    if not 0.0 < prior_on_probability < 1.0:
        raise ValueError("prior_on_probability must lie strictly between zero and one")
    if mechanism not in range(len(configs[0])):
        raise ValueError("mechanism index is out of range")

    def weight(state: tuple[int, ...]) -> float:
        p = prior_on_probability
        return prod(p if value else 1.0 - p for value in state)

    total = sum(weight(state) for state in configs)
    off = sum(weight(state) for state in configs if state[mechanism] == 0)
    if off == 0.0:
        return float("inf")
    return -log2(off / total)


def theorem_a_certificate(
    model: StructuralModel,
    observation: Observation,
    mechanism: int,
) -> TheoremACertificate:
    """Audit Theorem A by comparing its direct rule with exhaustive enumeration."""
    configs = admissible_configurations(model, observation)
    support = is_last_driver_standing(model, observation, mechanism)
    on = forced_on(configs, mechanism)
    by_theorem = forced_on_by_theorem(model, observation, mechanism)
    # For an empty region we do not label a contradiction as a necessity claim.
    holds = bool(configs) and (on == by_theorem)
    return TheoremACertificate(
        mechanism=mechanism,
        admissible_configuration_count=len(configs),
        forced_on=on,
        last_driver_standing=bool(support),
        supporting_traits=support,
        holds=holds,
    )


def canonical_synergy_model(competitor_count: int) -> tuple[StructuralModel, Observation, tuple[Observation, ...]]:
    """Construct the canonical greedy-failure family.

    Mechanism zero is focal. All mechanisms drive ``shared``. Each competitor
    additionally drives one private witness. Every singleton witness-null leaves
    at least one competitor, whereas the full panel leaves the focal mechanism as
    the only driver of ``shared``.
    """
    if competitor_count < 2:
        raise ValueError("competitor_count must be at least two")
    drivers: dict[str, frozenset[int]] = {
        "shared": frozenset(range(competitor_count + 1)),
    }
    singleton_panels: list[Observation] = []
    for competitor in range(1, competitor_count + 1):
        witness = f"witness_{competitor}"
        drivers[witness] = frozenset({competitor})
        singleton_panels.append(Observation(present=("shared",), null=(witness,)))
    return StructuralModel(competitor_count + 1, drivers), Observation(
        present=("shared",),
        null=tuple(f"witness_{i}" for i in range(1, competitor_count + 1)),
    ), tuple(singleton_panels)


def greedy_failure_witness(competitor_count: int) -> bool:
    """Return whether the canonical family has zero singleton but positive joint gain."""
    model, full_panel, singleton_panels = canonical_synergy_model(competitor_count)
    base = Observation(present=("shared",))
    base_forced = forced_on(admissible_configurations(model, base), 0)
    singleton_forced = [
        forced_on(admissible_configurations(model, panel), 0) for panel in singleton_panels
    ]
    joint_forced = forced_on(admissible_configurations(model, full_panel), 0)
    return (not base_forced) and (not any(singleton_forced)) and joint_forced
