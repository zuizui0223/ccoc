"""Exact finite benchmark families for causal-invariant misspecification risk.

The family in this module fixes the declared two-driver OR model:

    target = focal OR competitor
    witness = competitor

and conditions on the reported observation ``target PRESENT, witness NULL``.
Under that declared model the focal mechanism is forced ON. The true generator
then varies latent target routes, witness inhibition, detection error,
conjunctive target contexts, and compatibility restrictions. All quantities are
computed by finite weighted enumeration, never Monte Carlo sampling.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import prod
from typing import Iterable, Mapping


@dataclass(frozen=True)
class TwoDriverFamilyParameters:
    """Parameters for the finite misspecification benchmark family.

    The focal and declared competitor switches have independent Bernoulli(0.5)
    priors before any compatibility constraint. A latent route is enabled with
    ``latent_driver_prevalence`` and, when enabled, has an independent
    Bernoulli(0.5) switch. ``inhibition_prevalence`` is the probability that an
    active competitor's witness is suppressed. ``conjunction_prevalence`` is the
    probability that the declared OR core is replaced by a focal-AND-competitor
    core in that context. ``compatibility_constraint_prevalence`` is the
    probability of a context in which the competitor cannot be ON while focal is
    OFF. Witness sensitivity and false-positive rate govern observation of the
    true witness state.
    """

    latent_driver_prevalence: float = 0.0
    witness_sensitivity: float = 1.0
    witness_false_positive_rate: float = 0.0
    inhibition_prevalence: float = 0.0
    conjunction_prevalence: float = 0.0
    compatibility_constraint_prevalence: float = 0.0

    def __post_init__(self) -> None:
        values = {
            "latent_driver_prevalence": self.latent_driver_prevalence,
            "witness_sensitivity": self.witness_sensitivity,
            "witness_false_positive_rate": self.witness_false_positive_rate,
            "inhibition_prevalence": self.inhibition_prevalence,
            "conjunction_prevalence": self.conjunction_prevalence,
            "compatibility_constraint_prevalence": self.compatibility_constraint_prevalence,
        }
        for name, value in values.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must lie between zero and one")


@dataclass(frozen=True)
class TwoDriverSweepPoint:
    """One exact conditional-risk result for a parameter setting."""

    parameters: TwoDriverFamilyParameters
    reported_observation_probability: float
    posterior_focal_off_probability: float | None
    perfect_measurement_focal_off_probability: float | None
    declared_forced_on: bool = True

    @property
    def false_necessity_risk(self) -> float | None:
        """Alias for posterior focal-OFF probability after the reported panel."""
        return self.posterior_focal_off_probability if self.declared_forced_on else None

    @property
    def report_is_impossible(self) -> bool:
        """Whether the reported panel has zero probability under the true generator."""
        return self.reported_observation_probability == 0.0


# State: (focal, competitor, latent_enabled, latent_active, inhibited,
#         conjunctive_context, compatibility_context)
FamilyState = tuple[int, int, int, int, int, int, int]


def _bernoulli_prob(value: int, probability_one: float) -> float:
    return probability_one if value else 1.0 - probability_one


def _family_state_weights(parameters: TwoDriverFamilyParameters) -> dict[FamilyState, float]:
    """Return an exactly normalized finite state distribution for the family."""
    weights: dict[FamilyState, float] = {}
    for focal, latent_enabled, latent_active, inhibited, conjunctive, compatibility in product(
        (0, 1), repeat=6
    ):
        base = prod(
            (
                0.5,
                _bernoulli_prob(latent_enabled, parameters.latent_driver_prevalence),
                0.5 if latent_enabled else (1.0 if latent_active == 0 else 0.0),
                _bernoulli_prob(inhibited, parameters.inhibition_prevalence),
                _bernoulli_prob(conjunctive, parameters.conjunction_prevalence),
                _bernoulli_prob(compatibility, parameters.compatibility_constraint_prevalence),
            )
        )
        if base == 0.0:
            continue
        for competitor in (0, 1):
            # In compatibility contexts, competitor requires focal to be ON.
            if compatibility and competitor and not focal:
                continue
            competitor_probability = 0.5 if not (compatibility and not focal) else 1.0
            state = (
                focal,
                competitor,
                latent_enabled,
                latent_active,
                inhibited,
                conjunctive,
                compatibility,
            )
            weights[state] = base * competitor_probability
    total = sum(weights.values())
    if total == 0.0:
        raise RuntimeError("benchmark generator produced zero total state mass")
    return {state: weight / total for state, weight in weights.items()}


def _target_present(state: FamilyState) -> bool:
    focal, competitor, latent_enabled, latent_active, _, conjunctive, _ = state
    declared_core = focal and competitor if conjunctive else focal or competitor
    latent_route = bool(latent_enabled and latent_active)
    return bool(declared_core or latent_route)


def _witness_present(state: FamilyState) -> bool:
    _, competitor, _, _, inhibited, _, _ = state
    return bool(competitor and not inhibited)


def _reported_null_likelihood(true_witness_present: bool, parameters: TwoDriverFamilyParameters) -> float:
    if true_witness_present:
        return 1.0 - parameters.witness_sensitivity
    return 1.0 - parameters.witness_false_positive_rate


def evaluate_two_driver_family(parameters: TwoDriverFamilyParameters) -> TwoDriverSweepPoint:
    """Compute exact false-necessity risk for one misspecification setting.

    The observation is target PRESENT plus a reported NULL competitor witness. The
    declared two-driver OR model makes focal forced ON. The returned posterior is
    evaluated under the true finite generator and the stated observation channel.
    """
    weights = _family_state_weights(parameters)
    reported_total = 0.0
    reported_focal_off = 0.0
    perfect_total = 0.0
    perfect_focal_off = 0.0

    for state, prior_weight in weights.items():
        if not _target_present(state):
            continue
        witness_present = _witness_present(state)
        likelihood_reported_null = _reported_null_likelihood(witness_present, parameters)
        reported_mass = prior_weight * likelihood_reported_null
        reported_total += reported_mass
        if state[0] == 0:
            reported_focal_off += reported_mass

        if not witness_present:
            perfect_total += prior_weight
            if state[0] == 0:
                perfect_focal_off += prior_weight

    return TwoDriverSweepPoint(
        parameters=parameters,
        reported_observation_probability=reported_total,
        posterior_focal_off_probability=(
            None if reported_total == 0.0 else reported_focal_off / reported_total
        ),
        perfect_measurement_focal_off_probability=(
            None if perfect_total == 0.0 else perfect_focal_off / perfect_total
        ),
    )


def sweep_two_driver_family(
    parameter_grid: Mapping[str, Iterable[float]],
) -> tuple[TwoDriverSweepPoint, ...]:
    """Evaluate the exact family over a Cartesian product of parameter values.

    Unspecified parameters retain their default values. Grid keys must correspond
    to fields of :class:`TwoDriverFamilyParameters`. Output order follows sorted
    parameter names and the input order of each value iterable.
    """
    allowed = set(TwoDriverFamilyParameters.__dataclass_fields__)
    unknown = set(parameter_grid) - allowed
    if unknown:
        raise ValueError(f"unknown family parameters: {sorted(unknown)}")
    names = tuple(sorted(parameter_grid))
    values = tuple(tuple(parameter_grid[name]) for name in names)
    if any(not value_set for value_set in values):
        raise ValueError("every parameter grid entry must contain at least one value")

    points: list[TwoDriverSweepPoint] = []
    for combination in product(*values):
        overrides = dict(zip(names, combination))
        points.append(evaluate_two_driver_family(TwoDriverFamilyParameters(**overrides)))
    return tuple(points)


def phase_table_markdown(points: Iterable[TwoDriverSweepPoint], *, digits: int = 4) -> str:
    """Render an exact sweep as a compact Markdown table without extra packages."""
    if digits < 0:
        raise ValueError("digits must be non-negative")
    point_tuple = tuple(points)
    parameter_names = tuple(TwoDriverFamilyParameters.__dataclass_fields__)
    headers = (*parameter_names, "report_probability", "false_necessity_risk", "perfect_measurement_risk")
    rows = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for point in point_tuple:
        values = [
            f"{getattr(point.parameters, name):.{digits}f}"
            for name in parameter_names
        ]
        values.extend(
            (
                f"{point.reported_observation_probability:.{digits}f}",
                "impossible" if point.false_necessity_risk is None else f"{point.false_necessity_risk:.{digits}f}",
                "impossible"
                if point.perfect_measurement_focal_off_probability is None
                else f"{point.perfect_measurement_focal_off_probability:.{digits}f}",
            )
        )
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join(rows)
