import pytest

from causal_model.extension_compression import (
    IDLE,
    OBSERVE,
    all_states,
    certify_extension_compression,
    closed_interface_signature,
    closed_partition,
    exhaustive_witness_summary,
    is_closed_partition_sound,
    open_partition,
    open_trace_signature,
    probe_action,
    separating_trace_certificate,
    transition,
)


def test_each_closed_context_has_an_exact_four_state_interface():
    module_count = 4
    for port in range(module_count):
        assert len(closed_partition(module_count, port)) == 4
        assert is_closed_partition_sound(module_count, port)

    state = (0, 1, 0, 1, 1)
    assert closed_interface_signature(module_count, 2, state) == (0, 1)
    assert transition(module_count, state, probe_action(2)) == (1, 1, 0, 1, 1)
    assert transition(module_count, state, IDLE) == state
    assert transition(module_count, state, OBSERVE) == state


def test_open_interface_is_the_discrete_microstate_partition():
    module_count = 5
    partition = open_partition(module_count)
    assert len(partition) == 2 ** (module_count + 1)
    assert all(len(block) == 1 for block in partition)
    assert len({open_trace_signature(module_count, state) for state in all_states(module_count)}) == len(all_states(module_count))


def test_every_distinct_pair_has_an_explicit_admissible_trace_separator():
    module_count = 5
    states = all_states(module_count)
    for index, left in enumerate(states):
        for right in states[index + 1 :]:
            certificate = separating_trace_certificate(module_count, left, right)
            assert certificate.verify()
            if left[0] != right[0]:
                assert certificate.action == OBSERVE
            else:
                assert certificate.action.startswith("probe:")


def test_exact_two_vs_m_plus_one_separation():
    certificate = certify_extension_compression(6)
    assert certificate.closed_interface_bits == (2, 2, 2, 2, 2, 2)
    assert certificate.open_interface_bits == 7
    assert certificate.open_block_count == 128
    assert certificate.verify()


def test_exhaustive_finite_witness_family_has_the_claimed_scaling():
    certificates = exhaustive_witness_summary(6)
    assert [certificate.module_count for certificate in certificates] == [1, 2, 3, 4, 5, 6]
    assert all(certificate.closed_interface_bits == tuple(2 for _ in range(certificate.module_count)) for certificate in certificates)
    assert [certificate.open_interface_bits for certificate in certificates] == [2, 3, 4, 5, 6, 7]


@pytest.mark.parametrize("bad_count", [0, -1, True, 1.5, "4"])
def test_invalid_module_counts_fail_closed(bad_count):
    with pytest.raises(ValueError, match="positive integer"):
        certify_extension_compression(bad_count)
