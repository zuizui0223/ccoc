"""Exact closure-class comparison across observer-independent and observer-coupled regimes.

This module does *not* claim that observation creates reality.  It formalizes a
narrow, testable alternative: the act of observing, tracking, measuring, or
managing may be part of the update mechanism, so that the system has distinct
maps under two declared regimes:

    F_natural : S -> S
    F_observed: S -> S.

Each map is classified by ``causal_closure_calculus`` using exact finite
certificates.  The pair is then assigned a regime verdict.  A candidate family
can be summarized RACH-style: only a verdict shared by every retained candidate
pair is decisive; disagreement is ``UNRESOLVED``.

The theorem domain is finite labelled total deterministic maps with one common
state space.  It does not infer whether an empirical measurement is causally
invasive; that must be supplied as a modelling assumption.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Iterable, Mapping

from .causal_closure_calculus import (
    ClosureClassification,
    ClosureKind,
    FiniteDeterministicRuleSystem,
    classify_closure,
    exhaustive_rule_systems,
)


class ObservationRegimeVerdict(str, Enum):
    """Exact pair-level closure statements for two declared observation regimes."""

    OBSERVER_INDEPENDENT_CLOSURE = "observer_independent_closure"
    OBSERVATION_INDUCED_CLOSURE = "observation_induced_closure"
    OBSERVATION_INDUCED_RECURRENCE = "observation_induced_recurrence"
    OBSERVATION_INDUCED_MULTISTABILITY = "observation_induced_multistability"
    OBSERVER_INDEPENDENT_RECURRENCE = "observer_independent_recurrence"
    OBSERVER_INDEPENDENT_MULTISTABILITY = "observer_independent_multistability"
    REGIME_DEPENDENT_NONCLOSURE = "regime_dependent_nonclosure"


class RegimeConsensusKind(str, Enum):
    """RACH-style verdict over a retained family of regime-pair candidates."""

    DECISIVE = "decisive"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class ObservationRegimeRulePair:
    """One candidate model with a natural and observer-coupled update map."""

    candidate_id: str
    natural_rule: FiniteDeterministicRuleSystem
    observed_rule: FiniteDeterministicRuleSystem

    def __post_init__(self) -> None:
        if not isinstance(self.candidate_id, str) or not self.candidate_id:
            raise ValueError("candidate_id must be a non-empty string")
        if self.natural_rule.states != self.observed_rule.states:
            raise ValueError("natural and observed rules must use identical ordered state spaces")


@dataclass(frozen=True)
class ObservationRegimeClassification:
    """Exact classifications for a pair and their derived regime verdict."""

    pair: ObservationRegimeRulePair
    natural_classification: ClosureClassification
    observed_classification: ClosureClassification
    verdict: ObservationRegimeVerdict


@dataclass(frozen=True)
class RegimeConsensus:
    """A decisive shared verdict or an explicit unresolved candidate disagreement."""

    kind: RegimeConsensusKind
    verdict: ObservationRegimeVerdict | None
    candidate_verdicts: Mapping[str, ObservationRegimeVerdict]

    def __post_init__(self) -> None:
        if not self.candidate_verdicts:
            raise ValueError("regime consensus requires at least one candidate verdict")
        if self.kind is RegimeConsensusKind.DECISIVE and self.verdict is None:
            raise ValueError("decisive regime consensus needs one shared verdict")
        if self.kind is RegimeConsensusKind.UNRESOLVED and self.verdict is not None:
            raise ValueError("unresolved regime consensus must not name one verdict")


def _same_nonclosure_kind(left: ClosureKind, right: ClosureKind) -> bool:
    return left is right and left in {
        ClosureKind.RECURRENT_NONCLOSURE,
        ClosureKind.MULTISTABLE_NONCLOSURE,
    }


def regime_verdict(
    natural: ClosureKind,
    observed: ClosureKind,
) -> ObservationRegimeVerdict:
    """Classify closure change without treating every regime dependence as one claim."""

    if natural is ClosureKind.GLOBAL_CLOSURE and observed is ClosureKind.GLOBAL_CLOSURE:
        return ObservationRegimeVerdict.OBSERVER_INDEPENDENT_CLOSURE
    if natural is not ClosureKind.GLOBAL_CLOSURE and observed is ClosureKind.GLOBAL_CLOSURE:
        return ObservationRegimeVerdict.OBSERVATION_INDUCED_CLOSURE
    if natural is ClosureKind.GLOBAL_CLOSURE and observed is ClosureKind.RECURRENT_NONCLOSURE:
        return ObservationRegimeVerdict.OBSERVATION_INDUCED_RECURRENCE
    if natural is ClosureKind.GLOBAL_CLOSURE and observed is ClosureKind.MULTISTABLE_NONCLOSURE:
        return ObservationRegimeVerdict.OBSERVATION_INDUCED_MULTISTABILITY
    if natural is ClosureKind.RECURRENT_NONCLOSURE and observed is ClosureKind.RECURRENT_NONCLOSURE:
        return ObservationRegimeVerdict.OBSERVER_INDEPENDENT_RECURRENCE
    if natural is ClosureKind.MULTISTABLE_NONCLOSURE and observed is ClosureKind.MULTISTABLE_NONCLOSURE:
        return ObservationRegimeVerdict.OBSERVER_INDEPENDENT_MULTISTABILITY
    return ObservationRegimeVerdict.REGIME_DEPENDENT_NONCLOSURE


def classify_observation_regime_pair(
    pair: ObservationRegimeRulePair,
) -> ObservationRegimeClassification:
    """Build exact certificates in each regime and derive the pair-level verdict."""

    natural = classify_closure(pair.natural_rule)
    observed = classify_closure(pair.observed_rule)
    return ObservationRegimeClassification(
        pair=pair,
        natural_classification=natural,
        observed_classification=observed,
        verdict=regime_verdict(natural.kind, observed.kind),
    )


def summarize_regime_candidates(
    pairs: Iterable[ObservationRegimeRulePair],
) -> RegimeConsensus:
    """Return a claim only when every retained candidate pair has the same verdict."""

    classifications = tuple(classify_observation_regime_pair(pair) for pair in pairs)
    candidate_ids = tuple(item.pair.candidate_id for item in classifications)
    if len(set(candidate_ids)) != len(candidate_ids):
        raise ValueError("candidate IDs must be unique")
    verdicts = {item.pair.candidate_id: item.verdict for item in classifications}
    unique = set(verdicts.values())
    if len(unique) == 1:
        return RegimeConsensus(
            kind=RegimeConsensusKind.DECISIVE,
            verdict=next(iter(unique)),
            candidate_verdicts=verdicts,
        )
    return RegimeConsensus(
        kind=RegimeConsensusKind.UNRESOLVED,
        verdict=None,
        candidate_verdicts=verdicts,
    )


def exhaustive_observation_regime_pairs(state_count: int) -> Iterable[ObservationRegimeRulePair]:
    """Enumerate every ordered natural/observed pair of labelled maps on n states."""

    rules = tuple(exhaustive_rule_systems(state_count))
    for natural_index, observed_index in product(range(len(rules)), repeat=2):
        natural = rules[natural_index]
        observed = rules[observed_index]
        yield ObservationRegimeRulePair(
            candidate_id=f"n{natural_index}-o{observed_index}",
            natural_rule=natural,
            observed_rule=observed,
        )


def exhaustive_regime_summary(max_state_count: int = 3) -> Mapping[int, Mapping[ObservationRegimeVerdict, int]]:
    """Exhaustively classify all ordered regime pairs up to a small finite state size."""

    if not isinstance(max_state_count, int) or not 1 <= max_state_count <= 4:
        raise ValueError("max_state_count must be an integer in [1, 4]")
    result: dict[int, Mapping[ObservationRegimeVerdict, int]] = {}
    for state_count in range(1, max_state_count + 1):
        counts = {verdict: 0 for verdict in ObservationRegimeVerdict}
        for pair in exhaustive_observation_regime_pairs(state_count):
            counts[classify_observation_regime_pair(pair).verdict] += 1
        result[state_count] = counts
    return result
