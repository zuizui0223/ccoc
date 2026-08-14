"""Exact master-type closure for context-dependent ecological feedback.

This module identifies the correct finite object when a hidden interaction mode
has a *different response type in different ecological contexts*.  A bound on
the number of types visible at one context is not enough: future contexts can
split a previously merged hidden-mode class.

For a finite contextual feedback system, mode ``m`` has one context-specific
type label ``tau_c(m)`` at each ecological context ``c``.  Its **master feedback
signature** is the whole row

    tau_*(m) = (tau_c(m))_c.

If current macro transitions depend on the hidden mode only through the current
context type, then ``(context, macrostate, master type)`` is an exact dynamic
interface.  Duplicating micro modes inside one master type therefore does not
change the induced macro law.

A rotating-bit family gives the negative companion: every instantaneous context
has only two response types, yet the common master partition has ``2**r``
classes and the exact initial interface needs ``r`` bits.  The last bit first
becomes visible at horizon ``4*r - 1``.

The common-refinement identity behind master signatures is elementary substrate.
The scientific use here is to separate bounded *instantaneous* feedback type
count from bounded *future-stable* feedback type rank.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log2
from typing import Hashable, Iterable

from .dynamic_boundary_blankets import (
    DynamicInterfaceCertificate,
    FiniteControlledOutputSystem,
)

Action = str
Context = int
MacroState = int
Mode = int
MicroState = tuple[Context, MacroState, Mode]
MasterRow = tuple[int, ...]
SummaryState = tuple[Context, MacroState, int]

STEP: Action = "step"

READY = 0
OCCUPIED = 1
POST_LIVE = 2
POST_DEAD = 3
REPROBE_LIVE = 4
REPROBE_DEAD = 5
ROTATING_MACRO_STATE_COUNT = 6


def _positive_int(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _canonical_labels(values: Iterable[Hashable]) -> tuple[int, ...]:
    labels: dict[Hashable, int] = {}
    result: list[int] = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


def _same_partition(left: tuple[Hashable, ...], right: tuple[Hashable, ...]) -> bool:
    if len(left) != len(right):
        return False
    return all(
        (left[i] == left[j]) == (right[i] == right[j])
        for i in range(len(left))
        for j in range(len(left))
    )


@dataclass(frozen=True)
class ContextualFeedbackSystem:
    """Finite feedback system with context-dependent hidden-mode types.

    Hidden mode identity is static.  At context ``c`` the local macro successor
    may depend on mode ``m`` only through ``type_rows[m][c]``.
    """

    actions: tuple[Action, ...]
    context_count: int
    macro_state_count: int
    type_counts: tuple[int, ...]
    type_rows: tuple[MasterRow, ...]
    output_table: tuple[tuple[Hashable, ...], ...]
    context_transition_table: tuple[tuple[tuple[int, ...], ...], ...]
    macro_transition_table: tuple[tuple[tuple[tuple[int, ...], ...], ...], ...]

    def __post_init__(self) -> None:
        _positive_int(self.context_count, "context_count")
        _positive_int(self.macro_state_count, "macro_state_count")
        if not isinstance(self.actions, tuple) or not self.actions:
            raise ValueError("actions must be a nonempty tuple")
        if len(set(self.actions)) != len(self.actions):
            raise ValueError("actions must be unique")
        if any(not isinstance(action, str) or not action for action in self.actions):
            raise ValueError("actions must be nonempty strings")
        if not isinstance(self.type_counts, tuple) or len(self.type_counts) != self.context_count:
            raise ValueError("type_counts must have one entry per context")
        for count in self.type_counts:
            _positive_int(count, "context type count")
        if not isinstance(self.type_rows, tuple) or not self.type_rows:
            raise ValueError("type_rows must contain at least one hidden mode")
        for row in self.type_rows:
            if not isinstance(row, tuple) or len(row) != self.context_count:
                raise ValueError("every type row must have one label per context")
            for context, label in enumerate(row):
                if not isinstance(label, int) or isinstance(label, bool) or not 0 <= label < self.type_counts[context]:
                    raise ValueError("context type label is outside its declared type count")

        if not isinstance(self.output_table, tuple) or len(self.output_table) != self.context_count:
            raise ValueError("output_table must have one row per context")
        for row in self.output_table:
            if not isinstance(row, tuple) or len(row) != self.macro_state_count:
                raise ValueError("every output row must match macro_state_count")

        action_count = len(self.actions)
        if not isinstance(self.context_transition_table, tuple) or len(self.context_transition_table) != self.context_count:
            raise ValueError("context_transition_table must have one block per context")
        if not isinstance(self.macro_transition_table, tuple) or len(self.macro_transition_table) != self.context_count:
            raise ValueError("macro_transition_table must have one block per context")

        for context in range(self.context_count):
            context_rows = self.context_transition_table[context]
            macro_rows = self.macro_transition_table[context]
            if len(context_rows) != self.macro_state_count or len(macro_rows) != self.macro_state_count:
                raise ValueError("transition tables must have one row per macro state")
            for macrostate in range(self.macro_state_count):
                c_row = context_rows[macrostate]
                m_row = macro_rows[macrostate]
                if not isinstance(c_row, tuple) or len(c_row) != action_count:
                    raise ValueError("context transition row must match action count")
                if not isinstance(m_row, tuple) or len(m_row) != action_count:
                    raise ValueError("macro transition row must match action count")
                for target_context in c_row:
                    if not isinstance(target_context, int) or isinstance(target_context, bool) or not 0 <= target_context < self.context_count:
                        raise ValueError("context successor is outside the context space")
                for action_entry in m_row:
                    if not isinstance(action_entry, tuple) or len(action_entry) != self.type_counts[context]:
                        raise ValueError("macro transition entry must contain one successor per current context type")
                    for target_macro in action_entry:
                        if not isinstance(target_macro, int) or isinstance(target_macro, bool) or not 0 <= target_macro < self.macro_state_count:
                            raise ValueError("macro successor is outside the macro state space")

    @property
    def mode_count(self) -> int:
        return len(self.type_rows)

    @property
    def contexts(self) -> tuple[int, ...]:
        return tuple(range(self.context_count))

    @property
    def macro_states(self) -> tuple[int, ...]:
        return tuple(range(self.macro_state_count))

    @property
    def modes(self) -> tuple[int, ...]:
        return tuple(range(self.mode_count))

    @property
    def master_rows(self) -> tuple[MasterRow, ...]:
        return tuple(sorted(set(self.type_rows)))

    @property
    def master_type_count(self) -> int:
        return len(self.master_rows)

    @property
    def instantaneous_type_counts(self) -> tuple[int, ...]:
        return tuple(len({row[c] for row in self.type_rows}) for c in self.contexts)

    def master_type(self, mode: Mode) -> int:
        self.validate_mode(mode)
        return self.master_rows.index(self.type_rows[mode])

    def validate_mode(self, mode: Mode) -> None:
        if not isinstance(mode, int) or isinstance(mode, bool) or not 0 <= mode < self.mode_count:
            raise ValueError("mode is outside the hidden-mode space")

    def micro_states(self) -> tuple[MicroState, ...]:
        return tuple(product(self.contexts, self.macro_states, self.modes))

    def state_index_map(self) -> dict[MicroState, int]:
        return {state: index for index, state in enumerate(self.micro_states())}

    def micro_transition(self, state: MicroState, action: Action) -> MicroState:
        context, macrostate, mode = state
        self.validate_mode(mode)
        if action not in self.actions:
            raise ValueError(f"unknown action: {action!r}")
        if not 0 <= context < self.context_count or not 0 <= macrostate < self.macro_state_count:
            raise ValueError("microstate is outside the declared product")
        action_index = self.actions.index(action)
        type_label = self.type_rows[mode][context]
        next_context = self.context_transition_table[context][macrostate][action_index]
        next_macro = self.macro_transition_table[context][macrostate][action_index][type_label]
        return next_context, next_macro, mode

    def micro_output(self, state: MicroState) -> Hashable:
        context, macrostate, mode = state
        self.validate_mode(mode)
        if not 0 <= context < self.context_count or not 0 <= macrostate < self.macro_state_count:
            raise ValueError("microstate is outside the declared product")
        return self.output_table[context][macrostate]

    def compile_system(self) -> FiniteControlledOutputSystem:
        states = self.micro_states()
        index = {state: i for i, state in enumerate(states)}
        transition_table = tuple(
            tuple(index[self.micro_transition(state, action)] for action in self.actions)
            for state in states
        )
        outputs = tuple(self.micro_output(state) for state in states)
        return FiniteControlledOutputSystem(
            actions=self.actions,
            transition_table=transition_table,
            outputs=outputs,
        )

    def master_summary_labels(self) -> tuple[SummaryState, ...]:
        return tuple(
            (context, macrostate, self.master_type(mode))
            for context, macrostate, mode in self.micro_states()
        )

    def master_macro_output(self, summary: SummaryState) -> Hashable:
        context, macrostate, master = summary
        self._validate_summary(summary)
        return self.output_table[context][macrostate]

    def master_macro_transition(self, summary: SummaryState, action: Action) -> SummaryState:
        context, macrostate, master = summary
        self._validate_summary(summary)
        if action not in self.actions:
            raise ValueError(f"unknown action: {action!r}")
        action_index = self.actions.index(action)
        row = self.master_rows[master]
        type_label = row[context]
        return (
            self.context_transition_table[context][macrostate][action_index],
            self.macro_transition_table[context][macrostate][action_index][type_label],
            master,
        )

    def _validate_summary(self, summary: SummaryState) -> None:
        if not isinstance(summary, tuple) or len(summary) != 3:
            raise ValueError("summary must be a (context, macrostate, master_type) triple")
        context, macrostate, master = summary
        if not isinstance(context, int) or isinstance(context, bool) or not 0 <= context < self.context_count:
            raise ValueError("summary context is invalid")
        if not isinstance(macrostate, int) or isinstance(macrostate, bool) or not 0 <= macrostate < self.macro_state_count:
            raise ValueError("summary macrostate is invalid")
        if not isinstance(master, int) or isinstance(master, bool) or not 0 <= master < self.master_type_count:
            raise ValueError("summary master type is invalid")

    def with_master_replications(self, replications: tuple[int, ...]) -> "ContextualFeedbackSystem":
        """Duplicate hidden-mode identities without changing master signatures."""
        if not isinstance(replications, tuple) or len(replications) != self.master_type_count:
            raise ValueError("replications must have one positive entry per master type")
        rows: list[MasterRow] = []
        for row, count in zip(self.master_rows, replications):
            _positive_int(count, "master replication")
            rows.extend([row] * count)
        return ContextualFeedbackSystem(
            actions=self.actions,
            context_count=self.context_count,
            macro_state_count=self.macro_state_count,
            type_counts=self.type_counts,
            type_rows=tuple(rows),
            output_table=self.output_table,
            context_transition_table=self.context_transition_table,
            macro_transition_table=self.macro_transition_table,
        )


@dataclass(frozen=True)
class MasterFeedbackTypeClosureCertificate:
    feedback_system: ContextualFeedbackSystem

    @property
    def master_type_count(self) -> int:
        return self.feedback_system.master_type_count

    @property
    def micro_mode_count(self) -> int:
        return self.feedback_system.mode_count

    @property
    def summary_block_count(self) -> int:
        return (
            self.feedback_system.context_count
            * self.feedback_system.macro_state_count
            * self.feedback_system.master_type_count
        )

    @property
    def micro_state_count(self) -> int:
        return (
            self.feedback_system.context_count
            * self.feedback_system.macro_state_count
            * self.feedback_system.mode_count
        )

    def verify(self) -> bool:
        try:
            system = self.feedback_system.compile_system()
            labels = self.feedback_system.master_summary_labels()
            if len(set(labels)) != self.summary_block_count:
                return False
            if not DynamicInterfaceCertificate(system, labels).verify():
                return False
            # Master equality is exactly equality of every context-specific type.
            for left in self.feedback_system.modes:
                for right in self.feedback_system.modes:
                    same_master = self.feedback_system.master_type(left) == self.feedback_system.master_type(right)
                    same_all_contexts = all(
                        self.feedback_system.type_rows[left][c] == self.feedback_system.type_rows[right][c]
                        for c in self.feedback_system.contexts
                    )
                    if same_master != same_all_contexts:
                        return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


@dataclass(frozen=True)
class MasterTypePortabilityCertificate:
    """Changing-domain portability under hidden-mode replication."""

    systems: tuple[ContextualFeedbackSystem, ...]

    def verify(self) -> bool:
        try:
            if not isinstance(self.systems, tuple) or not self.systems:
                return False
            base = self.systems[0]
            base_rows = base.master_rows
            for system in self.systems:
                if (
                    system.actions != base.actions
                    or system.context_count != base.context_count
                    or system.macro_state_count != base.macro_state_count
                    or system.type_counts != base.type_counts
                    or system.output_table != base.output_table
                    or system.context_transition_table != base.context_transition_table
                    or system.macro_transition_table != base.macro_transition_table
                    or system.master_rows != base_rows
                ):
                    return False
                if not MasterFeedbackTypeClosureCertificate(system).verify():
                    return False
            # The summary transition law is structural and therefore identical.
            for context in base.contexts:
                for macrostate in base.macro_states:
                    for master in range(base.master_type_count):
                        summary = (context, macrostate, master)
                        for action in base.actions:
                            target = base.master_macro_transition(summary, action)
                            if any(system.master_macro_transition(summary, action) != target for system in self.systems[1:]):
                                return False
                            output = base.master_macro_output(summary)
                            if any(system.master_macro_output(summary) != output for system in self.systems[1:]):
                                return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def rotating_feedback_system(rank: int) -> ContextualFeedbackSystem:
    """Build the rotating-context family with two instantaneous types per context."""
    _positive_int(rank, "rank")
    type_rows = tuple(tuple((profile >> c) & 1 for c in range(rank)) for profile in range(2**rank))
    type_counts = (2,) * rank
    output_row = (0, 1, 0, 0, 1, 0)
    output_table = tuple(output_row for _ in range(rank))

    context_transition: list[tuple[tuple[int, ...], ...]] = []
    macro_transition: list[tuple[tuple[tuple[int, ...], ...], ...]] = []
    for context in range(rank):
        next_context = (context + 1) % rank
        c_rows: list[tuple[int, ...]] = []
        m_rows: list[tuple[tuple[int, ...], ...]] = []
        for macrostate in range(ROTATING_MACRO_STATE_COUNT):
            c_target = next_context if macrostate in (REPROBE_LIVE, REPROBE_DEAD) else context
            c_rows.append((c_target,))
            if macrostate == READY:
                successors = (OCCUPIED, OCCUPIED)
            elif macrostate == OCCUPIED:
                successors = (POST_LIVE, POST_DEAD)
            elif macrostate == POST_LIVE:
                successors = (REPROBE_LIVE, REPROBE_LIVE)
            elif macrostate == POST_DEAD:
                successors = (REPROBE_DEAD, REPROBE_DEAD)
            elif macrostate in (REPROBE_LIVE, REPROBE_DEAD):
                successors = (READY, READY)
            else:  # pragma: no cover - validated range above
                raise AssertionError("unreachable macrostate")
            m_rows.append((successors,))
        context_transition.append(tuple(c_rows))
        macro_transition.append(tuple(m_rows))

    return ContextualFeedbackSystem(
        actions=(STEP,),
        context_count=rank,
        macro_state_count=ROTATING_MACRO_STATE_COUNT,
        type_counts=type_counts,
        type_rows=type_rows,
        output_table=output_table,
        context_transition_table=tuple(context_transition),
        macro_transition_table=tuple(macro_transition),
    )


def rotating_initial_state_indices(feedback_system: ContextualFeedbackSystem) -> tuple[int, ...]:
    """Indices of ``(context=0, READY, profile)`` in the compiled system."""
    states = feedback_system.micro_states()
    index = {state: i for i, state in enumerate(states)}
    return tuple(index[(0, READY, mode)] for mode in feedback_system.modes)


def rotating_profile_trace(rank: int, profile: int, horizon: int) -> tuple[Hashable, ...]:
    _positive_int(rank, "rank")
    if not isinstance(profile, int) or isinstance(profile, bool) or not 0 <= profile < 2**rank:
        raise ValueError("profile is outside the rotating family")
    if not isinstance(horizon, int) or isinstance(horizon, bool) or horizon < 0:
        raise ValueError("horizon must be a non-negative integer")
    feedback = rotating_feedback_system(rank)
    system = feedback.compile_system()
    states = feedback.micro_states()
    index = {state: i for i, state in enumerate(states)}
    state = index[(0, READY, profile)]
    return system.output_trace(state, (STEP,) * horizon)


@dataclass(frozen=True)
class RotatingFeedbackTypeCertificate:
    rank: int
    instantaneous_type_counts: tuple[int, ...]
    master_type_count: int
    initial_block_count_at_target_horizon: int
    target_horizon: int
    pre_target_last_bit_collision: bool
    bit_decoder_correct: bool
    master_interface_exact: bool

    @property
    def exact_initial_memory_bits(self) -> float:
        return log2(self.master_type_count)

    def verify(self) -> bool:
        return (
            self.rank >= 1
            and self.instantaneous_type_counts == (2,) * self.rank
            and self.master_type_count == 2**self.rank
            and self.initial_block_count_at_target_horizon == 2**self.rank
            and self.target_horizon == 4 * self.rank - 1
            and self.pre_target_last_bit_collision
            and self.bit_decoder_correct
            and self.master_interface_exact
            and self.exact_initial_memory_bits == float(self.rank)
        )


def certify_rotating_feedback_type_rank(rank: int) -> RotatingFeedbackTypeCertificate:
    feedback = rotating_feedback_system(rank)
    system = feedback.compile_system()
    slice_indices = rotating_initial_state_indices(feedback)
    target_horizon = 4 * rank - 1
    labels = system.horizon_labels(target_horizon)
    initial_labels = tuple(labels[index] for index in slice_indices)

    if rank == 1:
        left, right = 0, 1
    else:
        left = 0
        right = 1 << (rank - 1)
    pre_horizon = target_horizon - 1
    pre_collision = (
        rotating_profile_trace(rank, left, pre_horizon)
        == rotating_profile_trace(rank, right, pre_horizon)
    )

    decoder_ok = True
    for profile in range(2**rank):
        trace = rotating_profile_trace(rank, profile, target_horizon)
        for context in range(rank):
            reveal_time = 4 * context + 3
            expected = 1 - ((profile >> context) & 1)
            if trace[reveal_time] != expected:
                decoder_ok = False
                break
        if not decoder_ok:
            break

    certificate = RotatingFeedbackTypeCertificate(
        rank=rank,
        instantaneous_type_counts=feedback.instantaneous_type_counts,
        master_type_count=feedback.master_type_count,
        initial_block_count_at_target_horizon=len(set(initial_labels)),
        target_horizon=target_horizon,
        pre_target_last_bit_collision=pre_collision,
        bit_decoder_correct=decoder_ok,
        master_interface_exact=MasterFeedbackTypeClosureCertificate(feedback).verify(),
    )
    if not certificate.verify():
        raise AssertionError(f"rotating feedback certificate failed: {certificate!r}")
    return certificate


def certify_rotating_master_replication_portability(rank: int, multiplicities: tuple[tuple[int, ...], ...]) -> MasterTypePortabilityCertificate:
    base = rotating_feedback_system(rank)
    systems = tuple(base.with_master_replications(replications) for replications in multiplicities)
    certificate = MasterTypePortabilityCertificate(systems)
    if not certificate.verify():
        raise AssertionError("rotating master-type portability certificate failed")
    return certificate
