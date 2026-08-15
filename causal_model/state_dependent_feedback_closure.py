"""Exact closure for feedback that rewrites future context reachability.

This module addresses the deterministic feedback boundary left open after the
future-context forgetting theorem.  Hidden interaction mode may now change the
*context successor itself*, so two states with the same present ecological
context can have different future context cones.

The module keeps ecological context and ecological macrostate explicit and asks
only how much hidden-mode memory must additionally be retained.

Main results implemented here:

* the declared current feedback type ``tau_c(m)`` is an exact hidden summary iff
  equal current types have the same successor context, successor macrostate, and
  successor current type under every action;
* when that condition fails, iterative continuation refinement of hidden modes
  reaches a finite fixed point; ``(context, macrostate, continuation-class)`` is
  exact and is the coarsest exact interface among interfaces that retain context
  and macrostate explicitly;
* a fixed two-action routed-context family has at most two instantaneous feedback
  types in every context, one ecological macrostate, and only ``3r+1`` contexts,
  yet its initial continuation rank is ``2**r`` and the last profile bit is first
  exposable at horizon ``2r-1``.

The finite certificates replay these claims.  The proofs are structural finite
arguments, not empirical ecology claims and not novelty claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log2
from typing import Hashable, Iterable

Action = str
HiddenMode = int
Context = int
Macrostate = int
ContinuationLabels = tuple[tuple[tuple[int, ...], ...], ...]


def _validate_positive_integer(value: int, name: str) -> None:
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


@dataclass(frozen=True)
class ModeDependentContextFeedbackSystem:
    """Finite deterministic feedback system with persistent hidden mode.

    Shapes are

    ``outputs[context][macrostate]``;
    ``feedback_types[context][mode]``;
    ``context_transitions[context][macrostate][mode][action_index]``; and
    ``macro_transitions[context][macrostate][mode][action_index]``.

    Current output is mode-independent by design.  Hidden mode can affect both
    ecological macro dynamics and the successor context, so it can rewrite which
    future ecological worlds remain reachable.
    """

    actions: tuple[Action, ...]
    outputs: tuple[tuple[Hashable, ...], ...]
    feedback_types: tuple[tuple[Hashable, ...], ...]
    context_transitions: tuple[tuple[tuple[tuple[Context, ...], ...], ...], ...]
    macro_transitions: tuple[tuple[tuple[tuple[Macrostate, ...], ...], ...], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.actions, tuple) or not self.actions:
            raise ValueError("actions must be a nonempty tuple")
        if any(not isinstance(action, str) or not action for action in self.actions):
            raise ValueError("actions must be nonempty strings")
        if len(set(self.actions)) != len(self.actions):
            raise ValueError("actions must be unique")
        if not isinstance(self.outputs, tuple) or not self.outputs:
            raise ValueError("outputs must contain at least one context")
        macro_count = len(self.outputs[0])
        if macro_count < 1 or any(len(row) != macro_count for row in self.outputs):
            raise ValueError("every output context must use the same positive macrostate count")
        context_count = len(self.outputs)
        if not isinstance(self.feedback_types, tuple) or len(self.feedback_types) != context_count:
            raise ValueError("feedback_types must have one row per context")
        mode_count = len(self.feedback_types[0])
        if mode_count < 1 or any(len(row) != mode_count for row in self.feedback_types):
            raise ValueError("every feedback-type row must use the same positive mode count")
        if len(self.context_transitions) != context_count or len(self.macro_transitions) != context_count:
            raise ValueError("transition tables must have one outer row per context")
        for context in range(context_count):
            if len(self.context_transitions[context]) != macro_count or len(self.macro_transitions[context]) != macro_count:
                raise ValueError("transition tables must have one row per macrostate")
            for macrostate in range(macro_count):
                c_mode_rows = self.context_transitions[context][macrostate]
                q_mode_rows = self.macro_transitions[context][macrostate]
                if len(c_mode_rows) != mode_count or len(q_mode_rows) != mode_count:
                    raise ValueError("transition tables must have one row per hidden mode")
                for mode in range(mode_count):
                    c_row = c_mode_rows[mode]
                    q_row = q_mode_rows[mode]
                    if len(c_row) != len(self.actions) or len(q_row) != len(self.actions):
                        raise ValueError("every transition row must match the action count")
                    for target in c_row:
                        if not isinstance(target, int) or isinstance(target, bool) or not 0 <= target < context_count:
                            raise ValueError("context transition target is outside the context space")
                    for target in q_row:
                        if not isinstance(target, int) or isinstance(target, bool) or not 0 <= target < macro_count:
                            raise ValueError("macro transition target is outside the macrostate space")
        for row in self.feedback_types:
            for value in row:
                hash(value)
        for row in self.outputs:
            for value in row:
                hash(value)

    @property
    def context_count(self) -> int:
        return len(self.outputs)

    @property
    def macrostate_count(self) -> int:
        return len(self.outputs[0])

    @property
    def mode_count(self) -> int:
        return len(self.feedback_types[0])

    @property
    def modes(self) -> tuple[HiddenMode, ...]:
        return tuple(range(self.mode_count))

    def action_index(self, action: Action) -> int:
        try:
            return self.actions.index(action)
        except ValueError as error:
            raise ValueError(f"unknown action: {action!r}") from error

    def validate_state(self, context: Context, macrostate: Macrostate, mode: HiddenMode) -> None:
        if not isinstance(context, int) or isinstance(context, bool) or not 0 <= context < self.context_count:
            raise ValueError("context is outside the context space")
        if not isinstance(macrostate, int) or isinstance(macrostate, bool) or not 0 <= macrostate < self.macrostate_count:
            raise ValueError("macrostate is outside the macrostate space")
        if not isinstance(mode, int) or isinstance(mode, bool) or not 0 <= mode < self.mode_count:
            raise ValueError("hidden mode is outside the mode space")

    def output(self, context: Context, macrostate: Macrostate) -> Hashable:
        self.validate_state(context, macrostate, 0)
        return self.outputs[context][macrostate]

    def feedback_type(self, context: Context, mode: HiddenMode) -> Hashable:
        self.validate_state(context, 0, mode)
        return self.feedback_types[context][mode]

    def transition(
        self,
        context: Context,
        macrostate: Macrostate,
        mode: HiddenMode,
        action: Action,
    ) -> tuple[Context, Macrostate, HiddenMode]:
        self.validate_state(context, macrostate, mode)
        index = self.action_index(action)
        return (
            self.context_transitions[context][macrostate][mode][index],
            self.macro_transitions[context][macrostate][mode][index],
            mode,
        )

    def output_trace(
        self,
        context: Context,
        macrostate: Macrostate,
        mode: HiddenMode,
        word: Iterable[Action],
    ) -> tuple[Hashable, ...]:
        self.validate_state(context, macrostate, mode)
        current_context = context
        current_macrostate = macrostate
        trace = [self.output(current_context, current_macrostate)]
        for action in tuple(word):
            current_context, current_macrostate, _ = self.transition(
                current_context, current_macrostate, mode, action
            )
            trace.append(self.output(current_context, current_macrostate))
        return tuple(trace)


@dataclass(frozen=True)
class CurrentTypeObstruction:
    context: Context
    macrostate: Macrostate
    left_mode: HiddenMode
    right_mode: HiddenMode
    action: Action
    current_type: Hashable
    left_successor: tuple[Context, Macrostate]
    right_successor: tuple[Context, Macrostate]
    left_successor_type: Hashable
    right_successor_type: Hashable


def find_current_type_obstruction(
    system: ModeDependentContextFeedbackSystem,
) -> CurrentTypeObstruction | None:
    """Return the first obstruction to exactness of ``(c,q,tau_c(m))``.

    Because current output depends only on ``(c,q)``, the current-type summary is
    exact iff equal current types have the same successor context, successor
    macrostate, and successor current type after every action.
    """

    for context in range(system.context_count):
        for macrostate in range(system.macrostate_count):
            for left_mode in system.modes:
                for right_mode in system.modes[left_mode + 1 :]:
                    left_type = system.feedback_type(context, left_mode)
                    right_type = system.feedback_type(context, right_mode)
                    if left_type != right_type:
                        continue
                    for action in system.actions:
                        left_context, left_macrostate, _ = system.transition(
                            context, macrostate, left_mode, action
                        )
                        right_context, right_macrostate, _ = system.transition(
                            context, macrostate, right_mode, action
                        )
                        left_next_type = system.feedback_type(left_context, left_mode)
                        right_next_type = system.feedback_type(right_context, right_mode)
                        if (
                            left_context != right_context
                            or left_macrostate != right_macrostate
                            or left_next_type != right_next_type
                        ):
                            return CurrentTypeObstruction(
                                context=context,
                                macrostate=macrostate,
                                left_mode=left_mode,
                                right_mode=right_mode,
                                action=action,
                                current_type=left_type,
                                left_successor=(left_context, left_macrostate),
                                right_successor=(right_context, right_macrostate),
                                left_successor_type=left_next_type,
                                right_successor_type=right_next_type,
                            )
    return None


def current_type_interface_is_exact(system: ModeDependentContextFeedbackSystem) -> bool:
    return find_current_type_obstruction(system) is None


def _coarse_continuation_labels(system: ModeDependentContextFeedbackSystem) -> ContinuationLabels:
    return tuple(
        tuple(tuple(0 for _mode in system.modes) for _macrostate in range(system.macrostate_count))
        for _context in range(system.context_count)
    )


def continuation_refinement_step(
    system: ModeDependentContextFeedbackSystem,
    labels: ContinuationLabels,
) -> ContinuationLabels:
    """One relative refinement step for persistent hidden modes.

    Context and ecological macrostate are retained explicitly.  Hidden modes in
    one ``(c,q)`` fiber remain merged only when every action reaches the same
    explicit successor ``(c',q')`` and the successor hidden modes remain merged
    by the previous continuation partition there.
    """

    if len(labels) != system.context_count:
        raise ValueError("continuation labels have the wrong context count")
    refined: list[tuple[tuple[int, ...], ...]] = []
    for context in range(system.context_count):
        if len(labels[context]) != system.macrostate_count:
            raise ValueError("continuation labels have the wrong macrostate count")
        context_rows: list[tuple[int, ...]] = []
        for macrostate in range(system.macrostate_count):
            if len(labels[context][macrostate]) != system.mode_count:
                raise ValueError("continuation labels have the wrong mode count")
            signatures = []
            for mode in system.modes:
                successor_signature = []
                for action in system.actions:
                    next_context, next_macrostate, _ = system.transition(
                        context, macrostate, mode, action
                    )
                    successor_signature.append(
                        (
                            action,
                            next_context,
                            next_macrostate,
                            labels[next_context][next_macrostate][mode],
                        )
                    )
                signatures.append(tuple(successor_signature))
            context_rows.append(_canonical_labels(signatures))
        refined.append(tuple(context_rows))
    return tuple(refined)


def continuation_stabilization_bound(system: ModeDependentContextFeedbackSystem) -> int:
    """Maximum number of strict synchronous refinement rounds needed."""

    return system.context_count * system.macrostate_count * (system.mode_count - 1)


def continuation_closure(
    system: ModeDependentContextFeedbackSystem,
) -> tuple[int, ContinuationLabels]:
    labels = _coarse_continuation_labels(system)
    bound = continuation_stabilization_bound(system)
    for round_index in range(bound + 1):
        refined = continuation_refinement_step(system, labels)
        if refined == labels:
            return round_index, labels
        labels = refined
    raise AssertionError("continuation refinement exceeded the finite split bound")


def continuation_rank(
    labels: ContinuationLabels,
    context: Context,
    macrostate: Macrostate,
) -> int:
    return len(set(labels[context][macrostate]))


def _fixed_point_is_exact(
    system: ModeDependentContextFeedbackSystem,
    labels: ContinuationLabels,
) -> bool:
    if continuation_refinement_step(system, labels) != labels:
        return False
    for context in range(system.context_count):
        for macrostate in range(system.macrostate_count):
            row = labels[context][macrostate]
            for left_mode in system.modes:
                for right_mode in system.modes[left_mode + 1 :]:
                    if row[left_mode] != row[right_mode]:
                        continue
                    for action in system.actions:
                        left_context, left_macrostate, _ = system.transition(
                            context, macrostate, left_mode, action
                        )
                        right_context, right_macrostate, _ = system.transition(
                            context, macrostate, right_mode, action
                        )
                        if (left_context, left_macrostate) != (right_context, right_macrostate):
                            return False
                        if (
                            labels[left_context][left_macrostate][left_mode]
                            != labels[right_context][right_macrostate][right_mode]
                        ):
                            return False
    return True


@dataclass(frozen=True)
class ContinuationClosureCertificate:
    stabilization_round: int
    labels: ContinuationLabels
    total_structural_macrostate_count: int
    max_fiber_rank: int
    current_type_exact: bool

    def verify(self, system: ModeDependentContextFeedbackSystem) -> bool:
        expected_round, expected_labels = continuation_closure(system)
        expected_total = sum(
            continuation_rank(expected_labels, context, macrostate)
            for context in range(system.context_count)
            for macrostate in range(system.macrostate_count)
        )
        expected_max = max(
            continuation_rank(expected_labels, context, macrostate)
            for context in range(system.context_count)
            for macrostate in range(system.macrostate_count)
        )
        return (
            self.stabilization_round == expected_round
            and self.labels == expected_labels
            and self.total_structural_macrostate_count == expected_total
            and self.max_fiber_rank == expected_max
            and self.current_type_exact == current_type_interface_is_exact(system)
            and _fixed_point_is_exact(system, self.labels)
            and self.stabilization_round <= continuation_stabilization_bound(system)
        )


def certify_continuation_closure(
    system: ModeDependentContextFeedbackSystem,
) -> ContinuationClosureCertificate:
    round_index, labels = continuation_closure(system)
    certificate = ContinuationClosureCertificate(
        stabilization_round=round_index,
        labels=labels,
        total_structural_macrostate_count=sum(
            continuation_rank(labels, context, macrostate)
            for context in range(system.context_count)
            for macrostate in range(system.macrostate_count)
        ),
        max_fiber_rank=max(
            continuation_rank(labels, context, macrostate)
            for context in range(system.context_count)
            for macrostate in range(system.macrostate_count)
        ),
        current_type_exact=current_type_interface_is_exact(system),
    )
    if not certificate.verify(system):
        raise AssertionError(f"continuation closure certificate failed: {certificate!r}")
    return certificate


def _profile_bit(profile: int, bit_index: int) -> int:
    return (profile >> bit_index) & 1


def _root_context(bit_index: int) -> int:
    return 3 * bit_index


def _branch_context(bit_index: int, bit: int) -> int:
    return 3 * bit_index + 1 + bit


def build_mode_routed_context_family(rank: int) -> ModeDependentContextFeedbackSystem:
    """Two-action family where hidden profile chooses future context routes.

    At root context ``j``, ``route`` moves to branch context ``(j,b_j)`` and the
    branch output equals ``b_j``.  ``advance`` from that branch reaches the next
    root.  The full context space is only ``3r+1`` and each context has at most
    two declared feedback types, yet all ``2**r`` profiles are distinguishable
    from the first root.
    """

    _validate_positive_integer(rank, "rank")
    actions = ("route", "advance")
    context_count = 3 * rank + 1
    terminal = 3 * rank
    mode_count = 1 << rank
    outputs: list[tuple[int, ...]] = []
    feedback_types: list[tuple[int, ...]] = []
    context_transitions: list[tuple[tuple[tuple[Context, ...], ...], ...]] = []
    macro_transitions: list[tuple[tuple[tuple[Macrostate, ...], ...], ...]] = []

    for context in range(context_count):
        output_value = 0
        root_index: int | None = None
        branch_index: int | None = None
        branch_bit: int | None = None
        for bit_index in range(rank):
            if context == _root_context(bit_index):
                root_index = bit_index
                break
            if context == _branch_context(bit_index, 0):
                branch_index = bit_index
                branch_bit = 0
                break
            if context == _branch_context(bit_index, 1):
                branch_index = bit_index
                branch_bit = 1
                output_value = 1
                break
        outputs.append((output_value,))

        if root_index is not None:
            feedback_types.append(
                tuple(_profile_bit(profile, root_index) for profile in range(mode_count))
            )
        else:
            feedback_types.append(tuple(0 for _profile in range(mode_count)))

        mode_context_rows: list[tuple[Context, ...]] = []
        mode_macro_rows: list[tuple[Macrostate, ...]] = []
        for profile in range(mode_count):
            if root_index is not None:
                bit = _profile_bit(profile, root_index)
                c_row = (_branch_context(root_index, bit), context)
            elif branch_index is not None and branch_bit is not None:
                next_root = terminal if branch_index == rank - 1 else _root_context(branch_index + 1)
                c_row = (context, next_root)
            else:
                c_row = (terminal, terminal)
            mode_context_rows.append(c_row)
            mode_macro_rows.append((0, 0))
        context_transitions.append((tuple(mode_context_rows),))
        macro_transitions.append((tuple(mode_macro_rows),))

    return ModeDependentContextFeedbackSystem(
        actions=actions,
        outputs=tuple(outputs),
        feedback_types=tuple(feedback_types),
        context_transitions=tuple(context_transitions),
        macro_transitions=tuple(macro_transitions),
    )


def _words_through(actions: tuple[Action, ...], horizon: int) -> tuple[tuple[Action, ...], ...]:
    return tuple(
        word
        for length in range(horizon + 1)
        for word in product(actions, repeat=length)
    )


@dataclass(frozen=True)
class ModeRoutedContextRankCertificate:
    rank: int
    context_count: int
    action_count: int
    maximum_instantaneous_type_count: int
    initial_continuation_rank: int
    initial_hidden_memory_bits: float
    stabilization_round: int
    last_bit_first_separating_horizon: int
    last_bit_pair_agrees_before_horizon: bool
    current_type_exact: bool

    def verify(self) -> bool:
        return (
            self.rank >= 1
            and self.context_count == 3 * self.rank + 1
            and self.action_count == 2
            and self.maximum_instantaneous_type_count == 2
            and self.initial_continuation_rank == 1 << self.rank
            and self.initial_hidden_memory_bits == float(self.rank)
            and self.stabilization_round == 2 * self.rank - 1
            and self.last_bit_first_separating_horizon == 2 * self.rank - 1
            and self.last_bit_pair_agrees_before_horizon
            and not self.current_type_exact
        )


def certify_mode_routed_context_rank(rank: int) -> ModeRoutedContextRankCertificate:
    system = build_mode_routed_context_family(rank)
    closure = certify_continuation_closure(system)
    initial_context = _root_context(0)
    initial_rank = continuation_rank(closure.labels, initial_context, 0)
    left_profile = 0
    right_profile = 1 << (rank - 1)
    first_horizon = 2 * rank - 1
    agrees_before = all(
        system.output_trace(initial_context, 0, left_profile, word)
        == system.output_trace(initial_context, 0, right_profile, word)
        for word in _words_through(system.actions, first_horizon - 1)
    )
    separating_word = tuple(
        action
        for bit_index in range(rank)
        for action in (("route", "advance") if bit_index < rank - 1 else ("route",))
    )
    if len(separating_word) != first_horizon:
        raise AssertionError("internal routed-context word-length mismatch")
    if (
        system.output_trace(initial_context, 0, left_profile, separating_word)
        == system.output_trace(initial_context, 0, right_profile, separating_word)
    ):
        raise AssertionError("routed-context last-bit witness failed to separate")
    certificate = ModeRoutedContextRankCertificate(
        rank=rank,
        context_count=system.context_count,
        action_count=len(system.actions),
        maximum_instantaneous_type_count=max(
            len(set(system.feedback_types[context])) for context in range(system.context_count)
        ),
        initial_continuation_rank=initial_rank,
        initial_hidden_memory_bits=log2(initial_rank),
        stabilization_round=closure.stabilization_round,
        last_bit_first_separating_horizon=first_horizon,
        last_bit_pair_agrees_before_horizon=agrees_before,
        current_type_exact=closure.current_type_exact,
    )
    if not certificate.verify():
        raise AssertionError(f"mode-routed context rank certificate failed: {certificate!r}")
    return certificate


if __name__ == "__main__":
    for _rank in range(1, 5):
        print(certify_mode_routed_context_rank(_rank))
