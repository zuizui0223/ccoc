from itertools import product

import pytest

from causal_model.constant_alphabet_relay import FIRE, GLOBAL_ACTION_ALPHABET, addressed_quiescent_configuration
from causal_model.fixed_regular_grammar_relay import (
    CLOSED_REGULAR_ACTIONS,
    FixedRegularGrammarRelayCertificate,
    all_regular_coordinate_states,
    apply_fixed_regular_action,
    balanced_tree_max_selector_depth,
    certify_fixed_regular_grammar_relay,
    fixed_closed_regular_grammar,
    fixed_open_regular_grammar,
    fixed_regular_output_trace,
    fixed_regular_probe_word,
    fixed_regular_word_trajectory,
    tree_address_for_port,
)
from causal_model.relay_tree_compilation import RelayTreeTopology, is_quiescent


def test_fixed_regular_grammars_have_one_state_and_one_new_transition() -> None:
    closed = fixed_closed_regular_grammar()
    opened = fixed_open_regular_grammar()

    assert closed.state_count == 1
    assert opened.state_count == 1
    assert closed.actions == tuple(GLOBAL_ACTION_ALPHABET)
    assert opened.actions == tuple(GLOBAL_ACTION_ALPHABET)
    assert closed.legal_actions(0) == CLOSED_REGULAR_ACTIONS
    assert opened.legal_actions(0) == tuple(GLOBAL_ACTION_ALPHABET)
    assert closed.transition_table == ((0, 0, None, 0),)
    assert opened.transition_table == ((0, 0, 0, 0),)

    assert closed.normalize_legal_word(()) == ()
    assert closed.normalize_legal_word(("0", "1", "tick", "0")) == ("0", "1", "tick", "0")
    with pytest.raises(ValueError):
        closed.normalize_legal_word(("0", FIRE))
    assert opened.normalize_legal_word(tuple(GLOBAL_ACTION_ALPHABET) * 3) == tuple(GLOBAL_ACTION_ALPHABET) * 3


def test_balanced_arbitrary_m_addresses_are_prefix_free_and_hit_each_leaf() -> None:
    for module_count in range(1, 10):
        topology = RelayTreeTopology.balanced(module_count)
        state = (0,) * (module_count + 1)
        initial = addressed_quiescent_configuration(topology, state[0], state[1:])
        addresses = tuple(tree_address_for_port(topology, port) for port in range(module_count))

        assert max((len(address) for address in addresses), default=0) == balanced_tree_max_selector_depth(
            module_count
        )

        for port, address in enumerate(addresses):
            selected = fixed_regular_word_trajectory(topology, initial, address)[-1]
            assert selected.selector_node == topology.leaf_for_port(port)

        for left_index, left in enumerate(addresses):
            for right_index, right in enumerate(addresses):
                if left_index == right_index:
                    continue
                assert not (len(left) <= len(right) and right[: len(left)] == left)


def test_totalized_action_semantics_accepts_arbitrary_open_words() -> None:
    topology = RelayTreeTopology.balanced(3)
    initial = addressed_quiescent_configuration(topology, 0, (1, 0, 1))

    for length in range(5):
        for word in product(GLOBAL_ACTION_ALPHABET, repeat=length):
            trajectory = fixed_regular_word_trajectory(topology, initial, word)
            assert len(trajectory) == length + 1
            assert trajectory[-1].relay.memory_bits == initial.relay.memory_bits
            assert trajectory[-1].selector_node in topology.leaves + topology.relays


def test_closed_words_remain_blind_to_memory_on_non_power_of_two() -> None:
    topology = RelayTreeTopology.balanced(3)
    states = all_regular_coordinate_states(3)

    # Finite regression sample. The all-word theorem is the one-step pulse-free
    # invariant checked by FixedRegularGrammarRelayCertificate.
    for length in range(5):
        for word in product(CLOSED_REGULAR_ACTIONS, repeat=length):
            traces_by_y: dict[int, set[tuple[int, ...]]] = {0: set(), 1: set()}
            for state in states:
                initial = addressed_quiescent_configuration(topology, state[0], state[1:])
                trace = fixed_regular_output_trace(topology, initial, word)
                traces_by_y[state[0]].add(trace)
            assert len(traces_by_y[0]) == 1
            assert len(traces_by_y[1]) == 1
            assert next(iter(traces_by_y[0])) != next(iter(traces_by_y[1]))


def test_canonical_probe_reads_every_leaf_for_arbitrary_m() -> None:
    for module_count in (1, 3, 5):
        topology = RelayTreeTopology.balanced(module_count)
        for state in all_regular_coordinate_states(module_count):
            initial = addressed_quiescent_configuration(topology, state[0], state[1:])
            for port in range(module_count):
                word = fixed_regular_probe_word(topology, port)
                final = fixed_regular_word_trajectory(topology, initial, word)[-1]
                assert is_quiescent(topology, final.relay)
                assert final.relay.focal_output == state[port + 1]
                assert final.relay.memory_bits == state[1:]


def test_repeated_fire_is_total_even_while_a_pulse_is_active() -> None:
    topology = RelayTreeTopology.balanced(3)
    initial = addressed_quiescent_configuration(topology, 0, (0, 1, 0))
    address = tree_address_for_port(topology, 1)
    selected = fixed_regular_word_trajectory(topology, initial, address)[-1]

    first = apply_fixed_regular_action(topology, selected, FIRE)
    assert not is_quiescent(topology, first.relay)

    # Historical one-token semantics would reject this second fire while the
    # first pulse is active. The fixed-grammar totalization defines it locally.
    second = apply_fixed_regular_action(topology, first, FIRE)
    assert second.relay.memory_bits == initial.relay.memory_bits


def test_fixed_regular_grammar_certificate_includes_non_powers_of_two() -> None:
    for module_count in (1, 2, 3, 4, 5):
        certificate = certify_fixed_regular_grammar_relay(module_count)
        assert isinstance(certificate, FixedRegularGrammarRelayCertificate)
        assert certificate.verify()
        assert certificate.closed_grammar.state_count == 1
        assert certificate.open_grammar.state_count == 1
        assert certificate.closed_interface_state_count == 2
        assert certificate.open_interface_state_count == 2 ** (module_count + 1)
        assert certificate.open_only_innovation_bits == module_count
        assert certificate.maximum_degree <= 3
        assert certificate.maximum_leaf_depth == balanced_tree_max_selector_depth(module_count)
        assert certificate.worst_canonical_query_length == 2 * balanced_tree_max_selector_depth(module_count) + 2


def test_invalid_module_count_and_action_fail_closed() -> None:
    with pytest.raises(ValueError):
        certify_fixed_regular_grammar_relay(0)

    topology = RelayTreeTopology.balanced(2)
    initial = addressed_quiescent_configuration(topology, 0, (0, 1))
    with pytest.raises(ValueError):
        apply_fixed_regular_action(topology, initial, "bogus")
