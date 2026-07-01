from itertools import product

import pytest

from causal_model.extension_compression import all_states, probe_action, transition
from causal_model.relay_tree_compilation import (
    ROOT,
    RelayTreeTopology,
    certify_bounded_degree_compilation,
    certify_relay_protocol,
    coordinate_state,
    directed_edge_messages,
    exhaustive_compilation_summary,
    is_quiescent,
    micro_step,
    one_token_relay_grammar,
    protocol_trajectory,
    quiescent_configuration,
    run_macro_probe,
)


def test_fixed_grammar_and_degree_bound_hold_at_every_tree_size():
    grammar = one_token_relay_grammar()
    assert grammar.verify()
    for module_count in range(1, 9):
        topology = RelayTreeTopology.balanced(module_count)
        assert topology.verify()
        assert topology.relay_count == module_count - 1
        assert topology.core_degree(ROOT) == 1
        assert all(topology.maximum_degree_with_reader(port) <= 3 for port in range(module_count))
        assert all(topology.reader_attachment_edge(port)[1] == topology.leaf_for_port(port) for port in range(module_count))


def test_pairwise_messages_and_protocol_settling_are_explicit():
    topology = RelayTreeTopology.balanced(4)
    initial = quiescent_configuration(topology, 0, (1, 0, 1, 1))
    first = micro_step(topology, initial, fired_port=2)
    messages_before_fire = directed_edge_messages(topology, initial)

    assert all(value is None for value in messages_before_fire.values())
    assert first.leaf_pulses == (None, None, 1, None)
    assert first.relay_pulses == (None, None, None)

    trajectory = protocol_trajectory(topology, initial, 2)
    assert len(trajectory) == topology.settling_ticks + 1
    assert is_quiescent(topology, trajectory[-1])
    assert trajectory[-1].focal_output == 1
    assert trajectory[-1].memory_bits == initial.memory_bits


def test_every_macro_probe_equals_the_coordinate_witness_transition():
    for module_count in range(1, 6):
        topology = RelayTreeTopology.balanced(module_count)
        for state in all_states(module_count):
            initial = quiescent_configuration(topology, state[0], state[1:])
            for port in range(module_count):
                protocol = certify_relay_protocol(topology, initial, port)
                assert protocol.verify()
                assert coordinate_state(protocol.final) == transition(module_count, state, probe_action(port))
                assert run_macro_probe(topology, initial, port) == protocol.final


def test_macro_conjugacy_extends_to_every_finite_sequential_probe_word():
    module_count = 3
    topology = RelayTreeTopology.balanced(module_count)
    for initial_coordinate_state in all_states(module_count):
        for probe_word in product(range(module_count), repeat=3):
            tree_state = quiescent_configuration(
                topology,
                initial_coordinate_state[0],
                initial_coordinate_state[1:],
            )
            coordinate = initial_coordinate_state
            for port in probe_word:
                tree_state = run_macro_probe(topology, tree_state, port)
                coordinate = transition(module_count, coordinate, probe_action(port))
                assert is_quiescent(topology, tree_state)
                assert coordinate_state(tree_state) == coordinate


def test_compilation_certificate_preserves_two_vs_m_plus_one_separation():
    certificate = certify_bounded_degree_compilation(6)
    assert certificate.verify()
    assert certificate.closed_interface_bits == (2, 2, 2, 2, 2, 2)
    assert certificate.open_interface_bits == 7
    assert certificate.open_interface_state_count == 128
    assert certificate.topology.maximum_degree_with_reader(0) <= 3


def test_exhaustive_compilation_family_verifies_through_six_ports():
    certificates = exhaustive_compilation_summary(6)
    assert [certificate.module_count for certificate in certificates] == [1, 2, 3, 4, 5, 6]
    assert [certificate.open_interface_bits for certificate in certificates] == [2, 3, 4, 5, 6, 7]
    assert all(certificate.topology.relay_count == certificate.module_count - 1 for certificate in certificates)


@pytest.mark.parametrize("bad_count", [0, -1, True, 1.5, "4"])
def test_invalid_tree_sizes_fail_closed(bad_count):
    with pytest.raises(ValueError, match="positive integer"):
        RelayTreeTopology.balanced(bad_count)


def test_reader_cannot_fire_during_a_nonquiescent_protocol():
    topology = RelayTreeTopology.balanced(3)
    initial = quiescent_configuration(topology, 0, (0, 1, 1))
    in_flight = micro_step(topology, initial, fired_port=1)
    with pytest.raises(ValueError, match="quiescent"):
        micro_step(topology, in_flight, fired_port=2)
