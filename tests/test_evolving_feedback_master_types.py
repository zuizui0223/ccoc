from __future__ import annotations

import pytest

from causal_model.evolving_feedback_master_types import (
    MasterFeedbackTypeClosureCertificate,
    MasterTypePortabilityCertificate,
    READY,
    ROTATING_MACRO_STATE_COUNT,
    certify_rotating_feedback_type_rank,
    certify_rotating_master_replication_portability,
    rotating_feedback_system,
    rotating_initial_state_indices,
    rotating_profile_trace,
)


def test_rotating_feedback_rank_is_exact_for_small_families() -> None:
    for rank in range(1, 5):
        certificate = certify_rotating_feedback_type_rank(rank)
        assert certificate.verify()
        assert certificate.instantaneous_type_counts == (2,) * rank
        assert certificate.master_type_count == 2**rank
        assert certificate.exact_initial_memory_bits == float(rank)
        assert certificate.target_horizon == 4 * rank - 1


def test_each_context_has_only_two_types_but_master_partition_is_exponential() -> None:
    feedback = rotating_feedback_system(4)
    assert feedback.instantaneous_type_counts == (2, 2, 2, 2)
    assert feedback.master_type_count == 16
    assert len(feedback.master_rows) == 16


def test_reveal_times_decode_each_profile_bit() -> None:
    rank = 4
    horizon = 4 * rank - 1
    for profile in range(2**rank):
        trace = rotating_profile_trace(rank, profile, horizon)
        for context in range(rank):
            reveal_time = 4 * context + 3
            assert trace[reveal_time] == 1 - ((profile >> context) & 1)


def test_last_bit_pair_is_identical_until_the_sharp_horizon() -> None:
    rank = 4
    left = 0
    right = 1 << (rank - 1)
    assert rotating_profile_trace(rank, left, 4 * rank - 2) == rotating_profile_trace(rank, right, 4 * rank - 2)
    assert rotating_profile_trace(rank, left, 4 * rank - 1) != rotating_profile_trace(rank, right, 4 * rank - 1)


def test_master_summary_is_an_exact_dynamic_interface() -> None:
    feedback = rotating_feedback_system(3)
    certificate = MasterFeedbackTypeClosureCertificate(feedback)
    assert certificate.verify()
    assert certificate.master_type_count == 8
    assert certificate.summary_block_count == 3 * ROTATING_MACRO_STATE_COUNT * 8
    assert certificate.micro_state_count == certificate.summary_block_count


def test_hidden_mode_replication_preserves_one_master_macro_law() -> None:
    rank = 2
    master_count = 2**rank
    multiplicities = (
        (1,) * master_count,
        (2,) * master_count,
        (1, 3, 2, 5),
    )
    certificate = certify_rotating_master_replication_portability(rank, multiplicities)
    assert certificate.verify()
    assert tuple(system.mode_count for system in certificate.systems) == (4, 8, 11)
    assert all(system.master_type_count == master_count for system in certificate.systems)
    assert all(
        MasterFeedbackTypeClosureCertificate(system).summary_block_count
        == rank * ROTATING_MACRO_STATE_COUNT * master_count
        for system in certificate.systems
    )


def test_master_replication_really_compresses_duplicate_mode_identities() -> None:
    base = rotating_feedback_system(2)
    replicated = base.with_master_replications((5, 4, 3, 2))
    certificate = MasterFeedbackTypeClosureCertificate(replicated)
    assert certificate.verify()
    assert certificate.micro_mode_count == 14
    assert certificate.master_type_count == 4
    assert certificate.micro_state_count == 2 * ROTATING_MACRO_STATE_COUNT * 14
    assert certificate.summary_block_count == 2 * ROTATING_MACRO_STATE_COUNT * 4


def test_compiled_canonical_initial_slice_is_discrete_at_target_horizon() -> None:
    rank = 3
    feedback = rotating_feedback_system(rank)
    system = feedback.compile_system()
    indices = rotating_initial_state_indices(feedback)
    labels = system.horizon_labels(4 * rank - 1)
    assert len({labels[index] for index in indices}) == 2**rank


def test_invalid_master_replications_fail_closed() -> None:
    feedback = rotating_feedback_system(2)
    with pytest.raises(ValueError):
        feedback.with_master_replications((1, 1))
    with pytest.raises(ValueError):
        feedback.with_master_replications((1, 1, 1, 0))


def test_portability_certificate_rejects_mismatched_master_row_set() -> None:
    left = rotating_feedback_system(2)
    right = rotating_feedback_system(1)
    assert not MasterTypePortabilityCertificate((left, right)).verify()


def test_ready_initial_microstates_have_identical_current_output() -> None:
    rank = 3
    feedback = rotating_feedback_system(rank)
    system = feedback.compile_system()
    states = feedback.micro_states()
    index = {state: i for i, state in enumerate(states)}
    assert {
        system.output(index[(0, READY, mode)])
        for mode in feedback.modes
    } == {0}
