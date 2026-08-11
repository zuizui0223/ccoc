"""Tests for the constant-global-alphabet bounded-degree relay family."""

from math import log2

import pytest

import causal_model.portability_core as portability
from causal_model.codebook_families import fixed_weight_binary_codebook
from causal_model.constant_alphabet_relay import (
    GLOBAL_ACTION_ALPHABET,
    address_bits_for_port,
    addressed_output_trace,
    addressed_probe_word,
    addressed_quiescent_configuration,
    addressed_word_trajectory,
    certify_constant_alphabet_relay_sharpness,
    run_addressed_probe,
)
from causal_model.relay_tree_compilation import RelayTreeTopology, is_quiescent


def test_global_action_alphabet_is_constant_across_sizes():
    assert GLOBAL_ACTION_ALPHABET == ("0", "1", "fire", "tick")
    for module_count in (2, 4, 8):
        certificate = certify_constant_alphabet_relay_sharpness(module_count)
        assert certificate.verify()
        assert certificate.global_action_alphabet == GLOBAL_ACTION_ALPHABET
        assert certificate.global_action_alphabet_size == 4
        assert certificate.maximum_degree <= 3


def test_binary_addresses_reach_exactly_the_requested_leaf():
    module_count = 8
    topology = RelayTreeTopology.balanced(module_count)
    initial = addressed_quiescent_configuration(topology, 0, (0,) * module_count)

    for port in range(module_count):
        address = address_bits_for_port(module_count, port)
        trajectory = addressed_word_trajectory(topology, initial, address)
        assert len(address) == 3
        assert trajectory[-1].selector_node == topology.leaf_for_port(port)
        assert is_quiescent(topology, trajectory[-1].relay)
        for before, after in zip(trajectory, trajectory[1:]):
            assert topology.parent_by_node[after.selector_node] == before.selector_node


def test_probe_word_length_is_two_log_m_plus_two():
    for module_count in (2, 4, 8, 16):
        expected = 2 * int(log2(module_count)) + 2
        lengths = {len(addressed_probe_word(module_count, port)) for port in range(module_count)}
        assert lengths == {expected}


def test_addressed_probe_reads_only_the_addressed_memory_bit():
    topology = RelayTreeTopology.balanced(4)
    state = (1, 0, 1, 1, 0)
    initial = addressed_quiescent_configuration(topology, state[0], state[1:])

    for port in range(topology.module_count):
        word = addressed_probe_word(topology.module_count, port)
        trace = addressed_output_trace(topology, initial, word)
        final = run_addressed_probe(topology, initial, port)
        assert trace[0] == state[0]
        assert trace[-1] == state[port + 1]
        assert final.relay.focal_output == state[port + 1]
        assert final.relay.memory_bits == state[1:]
        assert is_quiescent(topology, final.relay)


def test_sharpness_certificate_has_four_state_closed_views_and_full_open_quotient():
    certificate = certify_constant_alphabet_relay_sharpness(4)
    assert certificate.open_interface_state_count == 32
    assert certificate.open_interface_bits == 5
    assert certificate.closed_interface_state_counts == (4, 4, 4, 4)
    assert certificate.closed_interface_bits == (2, 2, 2, 2)
    assert certificate.noncommutation_gap_bits == 3
    assert certificate.probe_word_length == 6
    assert certificate.selector_augmented_relay_state_count == 6
    assert certificate.selector_augmented_leaf_state_count == 12


def test_fixed_richness_codebook_is_read_by_the_same_four_symbol_protocol():
    module_count = 4
    topology = RelayTreeTopology.balanced(module_count)
    for state in fixed_weight_binary_codebook(module_count, 2):
        initial = addressed_quiescent_configuration(topology, state[0], state[1:])
        for port in range(module_count):
            final = run_addressed_probe(topology, initial, port)
            assert final.relay.focal_output == state[port + 1]
            assert final.relay.memory_bits == state[1:]


@pytest.mark.parametrize("bad_count", [0, 1, 3, 6, -2, True, 4.0])
def test_non_power_of_two_sizes_fail_closed(bad_count):
    with pytest.raises(ValueError, match="power of two"):
        certify_constant_alphabet_relay_sharpness(bad_count)
