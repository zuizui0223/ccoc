"""Finite research benchmark for feedback-network non-reducibility.

This is deliberately an ``experiments/`` object, not a theorem module.  It tests
whether a tiny endogenous-accessibility feedback mechanism already escapes the
existing static-distance/occupancy summaries strongly enough to justify a new
theorem program.

State ``(f, m, t)`` means:

* ``f``: a facilitator currently keeps a source-to-target colonization edge open;
* ``m``: a latent interaction mode.  If ``m=1``, turnover after target
  colonization removes the facilitator as well as the target;
* ``t``: focal target occupancy (the observed response).

Actions:

* ``spread``: an open facilitator colonizes the target;
* ``turnover``: if the target is occupied, clear it; in latent mode ``m=1``
  also remove the facilitator.

The pair ``(1,0,0)`` and ``(1,1,0)`` agrees on current response, current static
reachability, occupancy count, and every response trace through length two.
It is separated only by ``spread, turnover, spread``.  Thus movement first
changes the ecological state on which the latent interaction mode acts; that
interaction then rewrites later accessibility.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Hashable

from causal_model.dynamic_boundary_blankets import (
    DynamicInterfaceCertificate,
    FiniteControlledOutputSystem,
    certify_finite_horizon_stabilization,
)

MicroState = tuple[int, int, int]


STATES: tuple[MicroState, ...] = tuple(product((0, 1), repeat=3))
STATE_INDEX = {state: index for index, state in enumerate(STATES)}
ACTIONS = ("spread", "turnover")
WITNESS_LEFT: MicroState = (1, 0, 0)
WITNESS_RIGHT: MicroState = (1, 1, 0)
DISTINGUISHING_WORD = ("spread", "turnover", "spread")


def _step(state: MicroState, action: str) -> MicroState:
    facilitator, mode, target = state
    if action == "spread":
        return facilitator, mode, int(bool(target or facilitator))
    if action == "turnover":
        if not target:
            return state
        next_facilitator = 0 if mode else facilitator
        return next_facilitator, mode, 0
    raise ValueError(f"unknown action: {action!r}")


def build_system() -> FiniteControlledOutputSystem:
    transition_table = tuple(
        tuple(STATE_INDEX[_step(state, action)] for action in ACTIONS)
        for state in STATES
    )
    outputs = tuple(state[2] for state in STATES)
    return FiniteControlledOutputSystem(
        actions=ACTIONS,
        transition_table=transition_table,
        outputs=outputs,
    )


def static_distance(state: MicroState) -> int:
    """Current distance shell: 0=occupied, 1=open one-step corridor, 2=unreachable."""
    facilitator, _mode, target = state
    if target:
        return 0
    if facilitator:
        return 1
    return 2


def baseline_label(state: MicroState) -> tuple[int, int, int]:
    """Existing-style product: focal output, static distance, current occupancy count."""
    facilitator, _mode, target = state
    return target, static_distance(state), facilitator + target


def feedback_label(state: MicroState) -> str:
    """Five-state feedback-aware summary for this benchmark.

    The latent mode matters before colonization because it controls whether the
    facilitator survives the next turnover.  Once a fragile occupied state has
    been reached, its future is identical to an occupied state with no
    facilitator, so the macro does not retain the hidden bit unnecessarily.
    """
    facilitator, mode, target = state
    if not target:
        if not facilitator:
            return "empty-unreachable"
        return "ready-fragile" if mode else "ready-resilient"
    if facilitator and not mode:
        return "occupied-resilient"
    return "occupied-no-recovery"


def _same_partition(left: tuple[Hashable, ...], right: tuple[Hashable, ...]) -> bool:
    if len(left) != len(right):
        return False
    return all(
        (left[i] == left[j]) == (right[i] == right[j])
        for i in range(len(left))
        for j in range(len(left))
    )


def _words_through(max_length: int) -> tuple[tuple[str, ...], ...]:
    return tuple(
        word
        for length in range(max_length + 1)
        for word in product(ACTIONS, repeat=length)
    )


@dataclass(frozen=True)
class FeedbackNetworkTriageCertificate:
    canonical_block_count: int
    stabilization_horizon: int
    baseline_block_count: int
    feedback_block_count: int
    baseline_dynamic: bool
    feedback_dynamic: bool
    feedback_matches_canonical: bool
    witness_agrees_through_length_two: bool
    witness_distinguished_at_length_three: bool

    def verify(self) -> bool:
        return (
            self.canonical_block_count == 5
            and self.stabilization_horizon == 3
            and self.baseline_block_count == 4
            and self.feedback_block_count == 5
            and not self.baseline_dynamic
            and self.feedback_dynamic
            and self.feedback_matches_canonical
            and self.witness_agrees_through_length_two
            and self.witness_distinguished_at_length_three
        )


def certify_feedback_network_triage() -> FeedbackNetworkTriageCertificate:
    system = build_system()
    baseline_labels = tuple(baseline_label(state) for state in STATES)
    feedback_labels = tuple(feedback_label(state) for state in STATES)

    stabilization = certify_finite_horizon_stabilization(system)
    canonical_labels = system.horizon_labels(stabilization.stabilization_horizon)

    left = STATE_INDEX[WITNESS_LEFT]
    right = STATE_INDEX[WITNESS_RIGHT]
    agrees_through_two = all(
        system.output_trace(left, word) == system.output_trace(right, word)
        for word in _words_through(2)
    )
    distinguished_at_three = (
        system.output_trace(left, DISTINGUISHING_WORD)
        != system.output_trace(right, DISTINGUISHING_WORD)
    )

    certificate = FeedbackNetworkTriageCertificate(
        canonical_block_count=stabilization.canonical_block_count,
        stabilization_horizon=stabilization.stabilization_horizon,
        baseline_block_count=len(set(baseline_labels)),
        feedback_block_count=len(set(feedback_labels)),
        baseline_dynamic=DynamicInterfaceCertificate(system, baseline_labels).verify(),
        feedback_dynamic=DynamicInterfaceCertificate(system, feedback_labels).verify(),
        feedback_matches_canonical=_same_partition(feedback_labels, canonical_labels),
        witness_agrees_through_length_two=agrees_through_two,
        witness_distinguished_at_length_three=distinguished_at_three,
    )
    if not certificate.verify():
        raise AssertionError(f"feedback-network triage certificate failed: {certificate!r}")
    return certificate


if __name__ == "__main__":
    print(certify_feedback_network_triage())
