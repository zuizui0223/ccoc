from __future__ import annotations

from causal_model.evolving_feedback_master_types import ContextualFeedbackSystem
from causal_model.future_feedback_causal_forgetting import (
    ADVANCE,
    READY,
    FutureFeedbackClosureCertificate,
    autonomous_context_transition_table,
    certify_irreversible_feedback_forgetting,
    chain_bit_probe_word,
    future_feedback_rank,
    future_feedback_signature,
    future_reachable_contexts,
    irreversible_feedback_chain,
    ready_slice_canonical_block_count,
)


def test_irreversible_chain_forgets_one_exact_bit_per_context() -> None:
    for rank in range(1, 5):
        certificate = certify_irreversible_feedback_forgetting(rank)
        assert certificate.verify()
        assert certificate.future_ranks == tuple(2 ** (rank - c) for c in range(rank)) + (1,)
        assert certificate.exact_memory_bits == tuple(float(rank - c) for c in range(rank)) + (0.0,)


def test_future_reachable_context_sets_shrink_along_chain() -> None:
    feedback = irreversible_feedback_chain(4)
    assert future_reachable_contexts(feedback, 0) == (0, 1, 2, 3, 4)
    assert future_reachable_contexts(feedback, 2) == (2, 3, 4)
    assert future_reachable_contexts(feedback, 4) == (4,)


def test_future_feedback_rank_matches_suffix_profile_count() -> None:
    feedback = irreversible_feedback_chain(4)
    assert tuple(future_feedback_rank(feedback, c) for c in feedback.contexts) == (16, 8, 4, 2, 1)


def test_past_only_mode_difference_is_forgotten_exactly() -> None:
    feedback = irreversible_feedback_chain(4)
    # Profiles 0000 and 0001 differ only in context-0 type.  From context 1 onward
    # their future feedback signatures are exactly equal.
    assert future_feedback_signature(feedback, 0, 0) != future_feedback_signature(feedback, 0, 1)
    assert future_feedback_signature(feedback, 1, 0) == future_feedback_signature(feedback, 1, 1)


def test_ready_slice_canonical_quotient_has_exact_suffix_rank() -> None:
    rank = 4
    feedback = irreversible_feedback_chain(rank)
    for context in range(rank):
        horizon = (rank - 1 - context) + 3
        assert ready_slice_canonical_block_count(feedback, context, horizon) == 2 ** (rank - context)
    assert ready_slice_canonical_block_count(feedback, rank, 0) == 1


def test_direct_future_probe_decodes_target_context_bit() -> None:
    rank = 4
    feedback = irreversible_feedback_chain(rank)
    system = feedback.compile_system()
    states = feedback.micro_states()
    index = {state: i for i, state in enumerate(states)}
    current_context = 1
    target_context = 3
    word = chain_bit_probe_word(current_context, target_context)
    assert word == (ADVANCE, ADVANCE, "spread", "turnover", "spread")
    for profile in range(2**rank):
        trace = system.output_trace(index[(current_context, READY, profile)], word)
        assert trace[-1] == 1 - ((profile >> target_context) & 1)


def test_future_signature_summary_is_exact_dynamic_interface() -> None:
    feedback = irreversible_feedback_chain(3)
    certificate = FutureFeedbackClosureCertificate(feedback)
    assert certificate.verify()
    assert certificate.future_ranks == (8, 4, 2, 1)


def test_context_dynamics_are_macrostate_independent_in_chain() -> None:
    feedback = irreversible_feedback_chain(3)
    transitions = autonomous_context_transition_table(feedback)
    for context in range(3):
        assert transitions[context] == (context, context, context + 1)
    assert transitions[3] == (3, 3, 3)


def test_future_closure_rejects_macrostate_dependent_context_motion() -> None:
    base = irreversible_feedback_chain(2)
    context_table = [list(rows) for rows in base.context_transition_table]
    # At context 0, make SPREAD from macrostate 0 jump to context 1 while the
    # other macrostates stay in context 0.  This violates the autonomous-context
    # premise used by the future-signature theorem.
    row = list(context_table[0][0])
    row[0] = 1
    context_table[0][0] = tuple(row)
    broken = ContextualFeedbackSystem(
        actions=base.actions,
        context_count=base.context_count,
        macro_state_count=base.macro_state_count,
        type_counts=base.type_counts,
        type_rows=base.type_rows,
        output_table=base.output_table,
        context_transition_table=tuple(tuple(rows) for rows in context_table),
        macro_transition_table=base.macro_transition_table,
    )
    assert not FutureFeedbackClosureCertificate(broken).verify()
