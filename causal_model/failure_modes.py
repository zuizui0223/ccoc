"""Finite known-truth audits for assumptions outside the exact OR theorem scope.

The exact replaceability theorem deliberately assumes a complete monotone-OR
candidate grammar. This module does not weaken that theorem. Instead, it supplies
small truth-table models that expose what happens when the declared grammar omits
a driver, NULL observations are noisy, or the true program contains inhibition,
conjunction, or state-compatibility constraints.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Iterable, Mapping

from .replaceability import (
    Observation,
    StructuralModel,
    forced_on_by_theorem,
    observation_is_admissible,
)

State = tuple[int, ...]


class TheoremAuditStatus(str, Enum):
    """Relationship between a declared OR theorem claim and finite known truth."""

    MATCH = "match"
    FALSE_NECESSITY = "false_necessity"
    MISSED_NECESSITY = "missed_necessity"
    TRUE_MODEL_CONTRADICTION = "true_model_contradiction"
    DECLARED_MODEL_CONTRADICTION = "declared_model_contradiction"
    BOTH_MODELS_CONTRADICT = "both_models_contradict"


@dataclass(frozen=True)
class TruthTableModel:
    """Finite qualitative truth model with arbitrary trait logic and feasible states.

    ``trait_true_states`` may encode OR, AND, inhibition, thresholds, feedback
    snapshots, or any other finite qualitative semantics. ``feasible_states``
    encodes background compatibility restrictions. This object is intentionally a
    truth benchmark, not an inference model.
    """

    mechanism_count: int
    trait_true_states: Mapping[str, frozenset[State]]
    feasible_states: frozenset[State] | None = None

    def __post_init__(self) -> None:
        if self.mechanism_count < 1:
            raise ValueError("mechanism_count must be positive")
        if not self.trait_true_states:
            raise ValueError("trait_true_states must not be empty")
        all_states = frozenset(product((0, 1), repeat=self.mechanism_count))
        if self.feasible_states is not None:
            if not self.feasible_states:
                raise ValueError("feasible_states must not be empty")
            if not set(self.feasible_states) <= all_states:
                raise ValueError("feasible_states contains an invalid Boolean state")
        for trait, states in self.trait_true_states.items():
            if not trait:
                raise ValueError("trait names must be non-empty")
            if not set(states) <= all_states:
                raise ValueError(f"truth table for {trait!r} contains an invalid Boolean state")

    @property
    def states(self) -> frozenset[State]:
        """All feasible true states, including a full Boolean cube by default."""
        if self.feasible_states is not None:
            return self.feasible_states
        return frozenset(product((0, 1), repeat=self.mechanism_count))

    def trait_is_present(self, trait: str, state: State) -> bool:
        """Return the true qualitative state of one observable trait."""
        if trait not in self.trait_true_states:
            raise ValueError(f"unknown truth-table trait: {trait!r}")
        if state not in self.states:
            raise ValueError("state is not feasible in this truth-table model")
        return state in self.trait_true_states[trait]


@dataclass(frozen=True)
class TheoremAudit:
    """Declared theorem conclusion compared with finite true-model behavior."""

    status: TheoremAuditStatus
    observation: Observation
    focal_mechanism: int
    declared_observation_admissible: bool
    true_admissible_states: tuple[State, ...]
    declared_forced_on: bool
    true_forced_on: bool


@dataclass(frozen=True)
class BinaryObservationChannel:
    """Probability model for a binary observed trait.

    ``present_if_true_present`` is sensitivity; ``present_if_true_null`` is the
    false-positive probability. A reported NULL therefore has likelihood
    ``1 - present_if_true_present`` when the trait is truly present.
    """

    present_if_true_present: float = 1.0
    present_if_true_null: float = 0.0

    def __post_init__(self) -> None:
        for probability in (self.present_if_true_present, self.present_if_true_null):
            if not 0.0 <= probability <= 1.0:
                raise ValueError("observation probabilities must lie between zero and one")

    def likelihood(self, *, reported_present: bool, true_present: bool) -> float:
        """Return the likelihood of one reported binary result."""
        probability_present = (
            self.present_if_true_present if true_present else self.present_if_true_null
        )
        return probability_present if reported_present else 1.0 - probability_present


@dataclass(frozen=True)
class NoisyObservationAudit:
    """Posterior risk that a declared forced-ON claim is false under measurement noise."""

    observation: Observation
    focal_mechanism: int
    declared_forced_on: bool
    report_probability: float
    posterior_focal_off_probability: float
    false_necessity_risk: float | None


def _validate_observation_against_truth(model: TruthTableModel, observation: Observation) -> None:
    overlap = set(observation.present) & set(observation.null)
    if overlap:
        raise ValueError(f"a trait cannot be both present and null: {sorted(overlap)}")
    unknown = (set(observation.present) | set(observation.null)) - set(model.trait_true_states)
    if unknown:
        raise ValueError(f"observation refers to unknown truth-table traits: {sorted(unknown)}")


def true_admissible_configurations(
    model: TruthTableModel,
    observation: Observation,
) -> tuple[State, ...]:
    """Enumerate true feasible states that generate the declared observation."""
    _validate_observation_against_truth(model, observation)
    return tuple(
        sorted(
            state
            for state in model.states
            if all(model.trait_is_present(trait, state) for trait in observation.present)
            and all(not model.trait_is_present(trait, state) for trait in observation.null)
        )
    )


def true_forced_on(
    configurations: Iterable[State],
    mechanism: int,
) -> bool:
    """Whether a mechanism is ON in every nonempty true admissible state."""
    configs = tuple(configurations)
    if not configs:
        return False
    if mechanism not in range(len(configs[0])):
        raise ValueError("mechanism index is out of range")
    return all(state[mechanism] == 1 for state in configs)


def audit_declared_theorem(
    declared_model: StructuralModel,
    truth_model: TruthTableModel,
    observation: Observation,
    *,
    focal_mechanism: int,
) -> TheoremAudit:
    """Compare a declared last-driver claim with arbitrary finite known truth."""
    if declared_model.mechanism_count != truth_model.mechanism_count:
        raise ValueError("declared and truth models must have the same mechanism_count")
    if focal_mechanism not in range(declared_model.mechanism_count):
        raise ValueError("focal mechanism index is out of range")
    _validate_observation_against_truth(truth_model, observation)

    declared_admissible = observation_is_admissible(declared_model, observation)
    declared_forced = forced_on_by_theorem(declared_model, observation, focal_mechanism)
    true_configs = true_admissible_configurations(truth_model, observation)
    actual_forced = true_forced_on(true_configs, focal_mechanism)

    if declared_admissible and not true_configs:
        status = TheoremAuditStatus.TRUE_MODEL_CONTRADICTION
    elif not declared_admissible and true_configs:
        status = TheoremAuditStatus.DECLARED_MODEL_CONTRADICTION
    elif not declared_admissible and not true_configs:
        status = TheoremAuditStatus.BOTH_MODELS_CONTRADICT
    elif declared_forced and not actual_forced:
        status = TheoremAuditStatus.FALSE_NECESSITY
    elif actual_forced and not declared_forced:
        status = TheoremAuditStatus.MISSED_NECESSITY
    else:
        status = TheoremAuditStatus.MATCH

    return TheoremAudit(
        status=status,
        observation=observation,
        focal_mechanism=focal_mechanism,
        declared_observation_admissible=declared_admissible,
        true_admissible_states=true_configs,
        declared_forced_on=declared_forced,
        true_forced_on=actual_forced,
    )


def noisy_observation_audit(
    declared_model: StructuralModel,
    truth_model: TruthTableModel,
    observation: Observation,
    *,
    focal_mechanism: int,
    channels: Mapping[str, BinaryObservationChannel] | None = None,
    prior_weights: Mapping[State, float] | None = None,
) -> NoisyObservationAudit:
    """Quantify posterior false-necessity risk under a binary observation channel.

    The declared theorem is evaluated on the reported observation. The true model
    supplies possible latent states. For each trait, missing channel entries use a
    perfect observation channel. Prior weights default to a uniform distribution
    over feasible true states. The risk is the posterior probability that the
    focal mechanism is OFF, conditional on the reported observation; it is only
    labelled ``false_necessity_risk`` when the declared model calls it forced ON.
    """
    if declared_model.mechanism_count != truth_model.mechanism_count:
        raise ValueError("declared and truth models must have the same mechanism_count")
    if focal_mechanism not in range(declared_model.mechanism_count):
        raise ValueError("focal mechanism index is out of range")
    _validate_observation_against_truth(truth_model, observation)
    channel_map = dict(channels or {})
    unknown_channels = set(channel_map) - set(truth_model.trait_true_states)
    if unknown_channels:
        raise ValueError(f"channels refer to unknown truth-table traits: {sorted(unknown_channels)}")

    states = tuple(sorted(truth_model.states))
    if prior_weights is None:
        weights = {state: 1.0 for state in states}
    else:
        if set(prior_weights) != set(states):
            raise ValueError("prior_weights must contain exactly the feasible truth states")
        weights = dict(prior_weights)
        if any(weight < 0.0 for weight in weights.values()):
            raise ValueError("prior weights must be non-negative")
    if sum(weights.values()) <= 0.0:
        raise ValueError("prior weights must have positive total mass")

    numerator_off = 0.0
    denominator = 0.0
    for state in states:
        likelihood = 1.0
        for trait in observation.present:
            channel = channel_map.get(trait, BinaryObservationChannel())
            likelihood *= channel.likelihood(
                reported_present=True,
                true_present=truth_model.trait_is_present(trait, state),
            )
        for trait in observation.null:
            channel = channel_map.get(trait, BinaryObservationChannel())
            likelihood *= channel.likelihood(
                reported_present=False,
                true_present=truth_model.trait_is_present(trait, state),
            )
        posterior_mass = weights[state] * likelihood
        denominator += posterior_mass
        if state[focal_mechanism] == 0:
            numerator_off += posterior_mass

    if denominator == 0.0:
        raise ValueError("reported observation has zero probability under the truth model and channels")
    posterior_off = numerator_off / denominator
    declared_forced = forced_on_by_theorem(declared_model, observation, focal_mechanism)
    return NoisyObservationAudit(
        observation=observation,
        focal_mechanism=focal_mechanism,
        declared_forced_on=declared_forced,
        report_probability=denominator / sum(weights.values()),
        posterior_focal_off_probability=posterior_off,
        false_necessity_risk=posterior_off if declared_forced else None,
    )


def latent_competitor_counterexample() -> tuple[StructuralModel, TruthTableModel, Observation]:
    """Return a false-necessity case caused by an omitted latent target driver."""
    declared = StructuralModel(
        mechanism_count=3,
        driver_sets={
            "shared": frozenset({0, 1}),
            "witness_1": frozenset({1}),
        },
    )
    states = tuple(product((0, 1), repeat=3))
    truth = TruthTableModel(
        mechanism_count=3,
        trait_true_states={
            "shared": frozenset(state for state in states if state[0] or state[1] or state[2]),
            "witness_1": frozenset(state for state in states if state[1]),
        },
    )
    return declared, truth, Observation(present=("shared",), null=("witness_1",))


def inhibitory_null_counterexample() -> tuple[StructuralModel, TruthTableModel, Observation]:
    """Return a false-necessity case where NULL does not imply driver OFF."""
    declared = StructuralModel(
        mechanism_count=3,
        driver_sets={
            "shared": frozenset({0, 1}),
            "witness_1": frozenset({1}),
        },
    )
    states = tuple(product((0, 1), repeat=3))
    truth = TruthTableModel(
        mechanism_count=3,
        trait_true_states={
            "shared": frozenset(state for state in states if state[0] or state[1]),
            "witness_1": frozenset(state for state in states if state[1] and not state[2]),
        },
    )
    return declared, truth, Observation(present=("shared",), null=("witness_1",))


def conjunction_contradiction_counterexample() -> tuple[StructuralModel, TruthTableModel, Observation]:
    """Return a case where OR semantics turns a true contradiction into a claim."""
    declared = StructuralModel(
        mechanism_count=2,
        driver_sets={
            "shared": frozenset({0, 1}),
            "witness_1": frozenset({1}),
        },
    )
    states = tuple(product((0, 1), repeat=2))
    truth = TruthTableModel(
        mechanism_count=2,
        trait_true_states={
            "shared": frozenset(state for state in states if state[0] and state[1]),
            "witness_1": frozenset(state for state in states if state[1]),
        },
    )
    return declared, truth, Observation(present=("shared",), null=("witness_1",))


def compatibility_missed_necessity_counterexample() -> tuple[StructuralModel, TruthTableModel, Observation]:
    """Return a case where a hidden prerequisite makes a mechanism truly necessary."""
    declared = StructuralModel(
        mechanism_count=2,
        driver_sets={"shared": frozenset({0, 1})},
    )
    states = tuple(product((0, 1), repeat=2))
    truth = TruthTableModel(
        mechanism_count=2,
        trait_true_states={
            "shared": frozenset(state for state in states if state[0] or state[1]),
        },
        feasible_states=frozenset({(0, 0), (1, 0), (1, 1)}),
    )
    return declared, truth, Observation(present=("shared",))
