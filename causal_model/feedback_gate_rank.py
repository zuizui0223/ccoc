"""Scalable feedback-memory theorem for endogenous accessibility gates.

This module promotes the five-state feedback triage witness to an all-rank family.
The hidden interaction modes are not directly observable and do not alter the
current accessibility graph.  They become response-relevant only through the
alternating ecological cycle

    spread -> turnover -> spread

because target occupancy enables mode-dependent facilitator loss, and facilitator
loss changes later accessibility.

The family is deliberately finite and deterministic.  Its fixed primitive
control alphabet is ``{0, 1, spread, turnover}``; ``0``/``1`` address one gate
through a fixed-length binary selector and do not directly encode the hidden mode.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import ceil, log2
from typing import Iterable

ModeProfile = tuple[int, ...]
ActionWord = tuple[str, ...]

BIT0 = "0"
BIT1 = "1"
SPREAD = "spread"
TURNOVER = "turnover"
ACTIONS: tuple[str, ...] = (BIT0, BIT1, SPREAD, TURNOVER)


def _validate_rank(rank: int) -> None:
    if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
        raise ValueError("rank must be a positive integer")


def _validate_profile(profile: ModeProfile) -> None:
    if not isinstance(profile, tuple) or not profile:
        raise ValueError("mode profile must be a non-empty tuple")
    if any(bit not in (0, 1) for bit in profile):
        raise ValueError("every mode coordinate must be binary")


def selector_depth(rank: int) -> int:
    """Return the fixed binary address depth used for ``rank`` active gates."""
    _validate_rank(rank)
    if rank == 1:
        return 0
    return ceil(log2(rank))


def address_for(rank: int, index: int) -> ActionWord:
    """Return the fixed-length binary address for active gate ``index``."""
    _validate_rank(rank)
    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < rank:
        raise ValueError("index must identify an active gate")
    depth = selector_depth(rank)
    if depth == 0:
        return ()
    bits = format(index, f"0{depth}b")
    return tuple(BIT1 if bit == "1" else BIT0 for bit in bits)


def feedback_query_word(rank: int, index: int) -> ActionWord:
    """Address gate ``index`` and expose its mode through one feedback cycle."""
    return address_for(rank, index) + (SPREAD, TURNOVER, SPREAD)


@dataclass(frozen=True)
class FeedbackGateState:
    """Finite state of the addressed feedback-gate family.

    ``selector`` is the binary address prefix already supplied.  ``facilitators``
    are the current accessibility-gate states, ``targets`` are local target
    occupancies, and ``modes`` are immutable latent interaction modes.
    """

    selector: tuple[int, ...]
    facilitators: tuple[int, ...]
    targets: tuple[int, ...]
    modes: ModeProfile

    @property
    def rank(self) -> int:
        return len(self.modes)

    def validate(self) -> None:
        _validate_profile(self.modes)
        if len(self.facilitators) != self.rank or len(self.targets) != self.rank:
            raise ValueError("facilitator, target, and mode vectors must have equal length")
        if any(bit not in (0, 1) for bit in self.facilitators + self.targets):
            raise ValueError("ecological gate states must be binary")
        if any(bit not in (0, 1) for bit in self.selector):
            raise ValueError("selector prefix must be binary")
        if len(self.selector) > selector_depth(self.rank):
            raise ValueError("selector prefix is deeper than the declared address depth")


def initial_feedback_state(profile: ModeProfile) -> FeedbackGateState:
    """Canonical initial slice: every gate open, every target empty."""
    _validate_profile(profile)
    rank = len(profile)
    return FeedbackGateState(
        selector=(),
        facilitators=(1,) * rank,
        targets=(0,) * rank,
        modes=profile,
    )


def selected_gate(state: FeedbackGateState) -> int | None:
    """Return the selected active gate, or ``None`` before/after an unused code."""
    state.validate()
    depth = selector_depth(state.rank)
    if len(state.selector) != depth:
        return None
    if depth == 0:
        return 0
    index = 0
    for bit in state.selector:
        index = (index << 1) | bit
    return index if index < state.rank else None


def feedback_output(state: FeedbackGateState) -> int:
    """Observe occupancy at the currently selected gate; otherwise return zero."""
    gate = selected_gate(state)
    if gate is None:
        return 0
    return state.targets[gate]


def feedback_step(
    state: FeedbackGateState,
    action: str,
    *,
    mode_dependent_turnover: bool = True,
    accessibility_dependent_spread: bool = True,
) -> FeedbackGateState:
    """Apply one selector or ecological action.

    Two Boolean switches expose the exact feedback-cycle ablations used by the
    theorem.  If ``mode_dependent_turnover`` is false, turnover never converts
    the hidden mode into facilitator loss.  If ``accessibility_dependent_spread``
    is false, later spread ignores facilitator state, so facilitator loss cannot
    alter future accessibility.
    """
    state.validate()
    if action not in ACTIONS:
        raise ValueError(f"unknown action: {action!r}")

    depth = selector_depth(state.rank)
    if action in (BIT0, BIT1):
        if len(state.selector) >= depth:
            return state
        bit = 1 if action == BIT1 else 0
        return FeedbackGateState(
            selector=state.selector + (bit,),
            facilitators=state.facilitators,
            targets=state.targets,
            modes=state.modes,
        )

    gate = selected_gate(state)
    if gate is None:
        return state

    facilitators = list(state.facilitators)
    targets = list(state.targets)

    if action == SPREAD:
        if accessibility_dependent_spread:
            targets[gate] = int(bool(targets[gate] or facilitators[gate]))
        else:
            targets[gate] = 1
    elif action == TURNOVER and targets[gate]:
        targets[gate] = 0
        if mode_dependent_turnover and state.modes[gate]:
            facilitators[gate] = 0

    return FeedbackGateState(
        selector=state.selector,
        facilitators=tuple(facilitators),
        targets=tuple(targets),
        modes=state.modes,
    )


def feedback_trace(
    profile: ModeProfile,
    word: Iterable[str],
    *,
    mode_dependent_turnover: bool = True,
    accessibility_dependent_spread: bool = True,
) -> tuple[int, ...]:
    """Return the selected-target output trace from the canonical initial state."""
    state = initial_feedback_state(profile)
    trace = [feedback_output(state)]
    for action in word:
        state = feedback_step(
            state,
            action,
            mode_dependent_turnover=mode_dependent_turnover,
            accessibility_dependent_spread=accessibility_dependent_spread,
        )
        trace.append(feedback_output(state))
    return tuple(trace)


def decode_mode_from_query(trace: tuple[int, ...]) -> int:
    """Decode the queried binary mode from the final accessibility response."""
    if not trace or trace[-1] not in (0, 1):
        raise ValueError("query trace must end in a binary response")
    return 1 - trace[-1]


@dataclass(frozen=True)
class FeedbackVisibleSummary:
    """Current-time summaries shared by every latent profile in the theorem slice."""

    focal_output: int
    facilitator_count: int
    target_occupancy_count: int
    accessible_gate_count: int
    static_gate_distance: int


def visible_initial_summary(profile: ModeProfile) -> FeedbackVisibleSummary:
    """Return current output/reachability/count information before any feedback."""
    _validate_profile(profile)
    rank = len(profile)
    return FeedbackVisibleSummary(
        focal_output=0,
        facilitator_count=rank,
        target_occupancy_count=0,
        accessible_gate_count=rank,
        static_gate_distance=1,
    )


def all_mode_profiles(rank: int) -> tuple[ModeProfile, ...]:
    _validate_rank(rank)
    return tuple(tuple(bits) for bits in product((0, 1), repeat=rank))


def feedback_profile_signature(profile: ModeProfile) -> tuple[tuple[int, ...], ...]:
    """Canonical response signature using one feedback query for every gate."""
    _validate_profile(profile)
    rank = len(profile)
    return tuple(feedback_trace(profile, feedback_query_word(rank, i)) for i in range(rank))


def feedback_memory_bits(
    rank: int,
    *,
    mode_dependent_turnover: bool = True,
    accessibility_dependent_spread: bool = True,
) -> int:
    """Exact initial-slice mode memory for the declared feedback-cycle family.

    With both feedback arrows present, each hidden mode coordinate is decoded by
    its alternating query, so all ``2**rank`` profiles are response-distinct.
    If either arrow is removed, mode profiles are response-inert for every word:
    either the modes never change an ecological state, or the changed facilitator
    state never changes future target accessibility.
    """
    _validate_rank(rank)
    return rank if mode_dependent_turnover and accessibility_dependent_spread else 0


def first_feedback_separating_horizon(rank: int) -> int:
    """First possible profile-separating horizon on the canonical initial slice."""
    return selector_depth(rank) + 3


@dataclass(frozen=True)
class FeedbackGateRankCertificate:
    """Executable certificate for the all-rank feedback-memory theorem surface."""

    rank: int
    selector_depth_value: int
    primitive_alphabet_size: int
    query_length: int
    visible_summary_count: int
    full_feedback_memory_bits: int
    mode_blind_memory_bits: int
    accessibility_blind_memory_bits: int
    first_separating_horizon: int

    def verify(self) -> bool:
        try:
            _validate_rank(self.rank)
            depth = selector_depth(self.rank)
            if self.selector_depth_value != depth:
                return False
            if self.primitive_alphabet_size != len(ACTIONS):
                return False
            if self.query_length != depth + 3:
                return False
            if self.first_separating_horizon != depth + 3:
                return False
            if self.visible_summary_count != 1:
                return False
            if self.full_feedback_memory_bits != self.rank:
                return False
            if self.mode_blind_memory_bits != 0 or self.accessibility_blind_memory_bits != 0:
                return False

            addresses = tuple(address_for(self.rank, i) for i in range(self.rank))
            if len(set(addresses)) != self.rank:
                return False
            if any(len(address) != depth for address in addresses):
                return False

            baseline = (0,) * self.rank
            baseline_summary = visible_initial_summary(baseline)
            for i in range(self.rank):
                unit = tuple(1 if j == i else 0 for j in range(self.rank))
                if visible_initial_summary(unit) != baseline_summary:
                    return False
                base_trace = feedback_trace(baseline, feedback_query_word(self.rank, i))
                unit_trace = feedback_trace(unit, feedback_query_word(self.rank, i))
                if decode_mode_from_query(base_trace) != 0:
                    return False
                if decode_mode_from_query(unit_trace) != 1:
                    return False
                if base_trace[:-1] != unit_trace[:-1] or base_trace[-1] == unit_trace[-1]:
                    return False

                mode_blind_trace = feedback_trace(
                    unit,
                    feedback_query_word(self.rank, i),
                    mode_dependent_turnover=False,
                )
                accessibility_blind_trace = feedback_trace(
                    unit,
                    feedback_query_word(self.rank, i),
                    accessibility_dependent_spread=False,
                )
                if mode_blind_trace != base_trace:
                    return False
                if accessibility_blind_trace != base_trace:
                    return False
            return True
        except ValueError:
            return False


def certify_feedback_gate_rank(rank: int) -> FeedbackGateRankCertificate:
    """Build the exact scalable feedback-cycle rank certificate for ``rank`` modes."""
    _validate_rank(rank)
    certificate = FeedbackGateRankCertificate(
        rank=rank,
        selector_depth_value=selector_depth(rank),
        primitive_alphabet_size=len(ACTIONS),
        query_length=selector_depth(rank) + 3,
        visible_summary_count=1,
        full_feedback_memory_bits=feedback_memory_bits(rank),
        mode_blind_memory_bits=feedback_memory_bits(rank, mode_dependent_turnover=False),
        accessibility_blind_memory_bits=feedback_memory_bits(rank, accessibility_dependent_spread=False),
        first_separating_horizon=first_feedback_separating_horizon(rank),
    )
    if not certificate.verify():
        raise AssertionError(f"feedback gate rank certificate failed: {certificate!r}")
    return certificate
