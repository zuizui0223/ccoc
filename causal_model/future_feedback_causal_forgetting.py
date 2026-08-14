"""Exact causal forgetting for irreversible context-dependent feedback.

Given a contextual feedback system whose context transition depends only on the
current context and action (not on hidden mode or ecological macrostate), a
hidden-mode distinction matters at context ``c`` only through type labels in
contexts that remain reachable from ``c``.

The future signature

    tau_c^+(m) = (tau_d(m)) for d reachable from c

therefore gives an exact dynamic interface together with the current ecological
context and macrostate.  As the reachable context set shrinks, future-signature
rank cannot increase.

An irreversible-chain family realizes the sharp case: with ``r`` latent bits,
exact hidden-mode memory on the ready slice falls from ``r`` bits to ``r-1``, ...,
then to zero as successive contexts become permanently unreachable.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Hashable

from .dynamic_boundary_blankets import DynamicInterfaceCertificate
from .evolving_feedback_master_types import ContextualFeedbackSystem

SPREAD = "spread"
TURNOVER = "turnover"
ADVANCE = "advance"
CHAIN_ACTIONS = (SPREAD, TURNOVER, ADVANCE)

EMPTY = 0        # f=0,t=0
READY = 1        # f=1,t=0
TARGET_ONLY = 2  # f=0,t=1
OCCUPIED = 3     # f=1,t=1
CHAIN_MACRO_STATE_COUNT = 4


def _positive_int(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _decode_gate_state(macrostate: int) -> tuple[int, int]:
    if macrostate == EMPTY:
        return 0, 0
    if macrostate == READY:
        return 1, 0
    if macrostate == TARGET_ONLY:
        return 0, 1
    if macrostate == OCCUPIED:
        return 1, 1
    raise ValueError("unknown chain macrostate")


def _encode_gate_state(facilitator: int, target: int) -> int:
    pair = (int(bool(facilitator)), int(bool(target)))
    mapping = {(0, 0): EMPTY, (1, 0): READY, (0, 1): TARGET_ONLY, (1, 1): OCCUPIED}
    return mapping[pair]


def autonomous_context_transition_table(feedback: ContextualFeedbackSystem) -> tuple[tuple[int, ...], ...]:
    """Return D(c,a) if context evolution is macrostate-independent.

    Raises ``ValueError`` when two ecological macrostates at the same context
    send one action to different next contexts.
    """
    rows: list[tuple[int, ...]] = []
    for context in feedback.contexts:
        row: list[int] = []
        for action_index, _action in enumerate(feedback.actions):
            targets = {
                feedback.context_transition_table[context][macrostate][action_index]
                for macrostate in feedback.macro_states
            }
            if len(targets) != 1:
                raise ValueError("context transition depends on ecological macrostate")
            row.append(next(iter(targets)))
        rows.append(tuple(row))
    return tuple(rows)


def future_reachable_contexts(feedback: ContextualFeedbackSystem, start_context: int) -> tuple[int, ...]:
    if not isinstance(start_context, int) or isinstance(start_context, bool) or not 0 <= start_context < feedback.context_count:
        raise ValueError("start_context is outside the context space")
    transitions = autonomous_context_transition_table(feedback)
    seen = {start_context}
    frontier = [start_context]
    while frontier:
        context = frontier.pop()
        for target in transitions[context]:
            if target not in seen:
                seen.add(target)
                frontier.append(target)
    return tuple(sorted(seen))


def future_feedback_signature(feedback: ContextualFeedbackSystem, context: int, mode: int) -> tuple[tuple[int, int], ...]:
    feedback.validate_mode(mode)
    reachable = future_reachable_contexts(feedback, context)
    return tuple((target_context, feedback.type_rows[mode][target_context]) for target_context in reachable)


def future_feedback_rank(feedback: ContextualFeedbackSystem, context: int) -> int:
    return len({future_feedback_signature(feedback, context, mode) for mode in feedback.modes})


def future_feedback_summary_labels(feedback: ContextualFeedbackSystem) -> tuple[Hashable, ...]:
    return tuple(
        (context, macrostate, future_feedback_signature(feedback, context, mode))
        for context, macrostate, mode in feedback.micro_states()
    )


@dataclass(frozen=True)
class FutureFeedbackClosureCertificate:
    feedback_system: ContextualFeedbackSystem

    @property
    def future_ranks(self) -> tuple[int, ...]:
        return tuple(future_feedback_rank(self.feedback_system, context) for context in self.feedback_system.contexts)

    def verify(self) -> bool:
        try:
            transitions = autonomous_context_transition_table(self.feedback_system)
            labels = future_feedback_summary_labels(self.feedback_system)
            if not DynamicInterfaceCertificate(self.feedback_system.compile_system(), labels).verify():
                return False
            # Along every context edge, the future context set only shrinks, so
            # future signature rank cannot increase.
            for context in self.feedback_system.contexts:
                source_reach = set(future_reachable_contexts(self.feedback_system, context))
                source_rank = future_feedback_rank(self.feedback_system, context)
                for target in transitions[context]:
                    target_reach = set(future_reachable_contexts(self.feedback_system, target))
                    if not target_reach.issubset(source_reach):
                        return False
                    if future_feedback_rank(self.feedback_system, target) > source_rank:
                        return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def irreversible_feedback_chain(rank: int) -> ContextualFeedbackSystem:
    """Build ``r`` informative contexts followed by one terminal context.

    Hidden profile bit ``b_c`` matters only in informative context ``c``.  The
    action ``advance`` irreversibly moves to the next context and resets the
    local facilitator/target gate to ``READY``.
    """
    _positive_int(rank, "rank")
    context_count = rank + 1
    type_counts = (2,) * rank + (1,)
    type_rows = tuple(
        tuple((profile >> context) & 1 for context in range(rank)) + (0,)
        for profile in range(2**rank)
    )
    output_row = tuple(_decode_gate_state(macrostate)[1] for macrostate in range(CHAIN_MACRO_STATE_COUNT))
    output_table = tuple(output_row for _ in range(context_count))

    context_transition: list[tuple[tuple[int, ...], ...]] = []
    macro_transition: list[tuple[tuple[tuple[int, ...], ...], ...]] = []

    for context in range(context_count):
        next_context = min(context + 1, rank)
        c_rows: list[tuple[int, ...]] = []
        m_rows: list[tuple[tuple[int, ...], ...]] = []
        for macrostate in range(CHAIN_MACRO_STATE_COUNT):
            facilitator, target = _decode_gate_state(macrostate)
            c_rows.append((context, context, next_context))
            action_entries: list[tuple[int, ...]] = []
            for action in CHAIN_ACTIONS:
                successors: list[int] = []
                for type_label in range(type_counts[context]):
                    if action == SPREAD:
                        successor = _encode_gate_state(facilitator, int(bool(target or facilitator)))
                    elif action == TURNOVER:
                        if target:
                            next_facilitator = 0 if type_label == 1 else facilitator
                            successor = _encode_gate_state(next_facilitator, 0)
                        else:
                            successor = macrostate
                    elif action == ADVANCE:
                        successor = READY
                    else:  # pragma: no cover
                        raise AssertionError("unknown chain action")
                    successors.append(successor)
                action_entries.append(tuple(successors))
            m_rows.append(tuple(action_entries))
        context_transition.append(tuple(c_rows))
        macro_transition.append(tuple(m_rows))

    return ContextualFeedbackSystem(
        actions=CHAIN_ACTIONS,
        context_count=context_count,
        macro_state_count=CHAIN_MACRO_STATE_COUNT,
        type_counts=type_counts,
        type_rows=type_rows,
        output_table=output_table,
        context_transition_table=tuple(context_transition),
        macro_transition_table=tuple(macro_transition),
    )


def ready_slice_indices(feedback: ContextualFeedbackSystem, context: int) -> tuple[int, ...]:
    states = feedback.micro_states()
    index = {state: i for i, state in enumerate(states)}
    return tuple(index[(context, READY, mode)] for mode in feedback.modes)


def ready_slice_canonical_block_count(feedback: ContextualFeedbackSystem, context: int, horizon: int) -> int:
    system = feedback.compile_system()
    labels = system.horizon_labels(horizon)
    return len({labels[index] for index in ready_slice_indices(feedback, context)})


def chain_bit_probe_word(current_context: int, target_context: int) -> tuple[str, ...]:
    if not isinstance(current_context, int) or isinstance(current_context, bool) or current_context < 0:
        raise ValueError("current_context must be a non-negative integer")
    if not isinstance(target_context, int) or isinstance(target_context, bool) or target_context < current_context:
        raise ValueError("target_context must be an integer at or after current_context")
    return (ADVANCE,) * (target_context - current_context) + (SPREAD, TURNOVER, SPREAD)


@dataclass(frozen=True)
class IrreversibleFeedbackForgettingCertificate:
    rank: int
    future_ranks: tuple[int, ...]
    ready_slice_block_counts: tuple[int, ...]
    exact_memory_bits: tuple[float, ...]
    future_interface_exact: bool
    one_bit_forgotten_per_advance: bool
    probes_decode_all_future_bits: bool

    def verify(self) -> bool:
        expected_ranks = tuple(2 ** (self.rank - context) for context in range(self.rank)) + (1,)
        expected_bits = tuple(float(self.rank - context) for context in range(self.rank)) + (0.0,)
        return (
            self.rank >= 1
            and self.future_ranks == expected_ranks
            and self.ready_slice_block_counts == expected_ranks
            and self.exact_memory_bits == expected_bits
            and self.future_interface_exact
            and self.one_bit_forgotten_per_advance
            and self.probes_decode_all_future_bits
        )


def certify_irreversible_feedback_forgetting(rank: int) -> IrreversibleFeedbackForgettingCertificate:
    feedback = irreversible_feedback_chain(rank)
    closure = FutureFeedbackClosureCertificate(feedback)
    future_ranks = closure.future_ranks

    # From context c, the longest direct future bit probe uses (r-1-c) advances
    # plus spread-turnover-spread.  This horizon therefore exposes every suffix bit.
    block_counts: list[int] = []
    bits: list[float] = []
    probes_ok = True
    system = feedback.compile_system()
    states = feedback.micro_states()
    index = {state: i for i, state in enumerate(states)}

    for context in range(rank + 1):
        if context == rank:
            horizon = 0
        else:
            horizon = (rank - 1 - context) + 3
        count = ready_slice_canonical_block_count(feedback, context, horizon)
        block_counts.append(count)
        bits.append(log2(count))

        if context < rank:
            for profile in range(2**rank):
                for target_context in range(context, rank):
                    word = chain_bit_probe_word(context, target_context)
                    start = index[(context, READY, profile)]
                    trace = system.output_trace(start, word)
                    expected = 1 - ((profile >> target_context) & 1)
                    if trace[-1] != expected:
                        probes_ok = False
                        break
                if not probes_ok:
                    break
        if not probes_ok:
            break

    one_bit = all(future_ranks[c + 1] * 2 == future_ranks[c] for c in range(rank))
    certificate = IrreversibleFeedbackForgettingCertificate(
        rank=rank,
        future_ranks=future_ranks,
        ready_slice_block_counts=tuple(block_counts),
        exact_memory_bits=tuple(bits),
        future_interface_exact=closure.verify(),
        one_bit_forgotten_per_advance=one_bit,
        probes_decode_all_future_bits=probes_ok,
    )
    if not certificate.verify():
        raise AssertionError(f"irreversible feedback forgetting certificate failed: {certificate!r}")
    return certificate
