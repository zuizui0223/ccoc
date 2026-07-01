import math

import pytest

from causal_model.binary_joint_relay_compilation import (
    COPY_0,
    COPY_1,
    XOR_0,
    XOR_1,
    BinaryJointMacroAction,
    BinaryJointRelayConfiguration,
    BinaryJointRelayTopology,
    all_binary_joint_states,
    binary_joint_product,
    binary_joint_relay_grammar,
    certify_binary_joint_relay_compilation,
    certify_binary_joint_relay_protocol,
    configuration_from_macro_state,
    directed_edge_tokens,
    exhaustive_binary_joint_compilation_summary,
    expected_macro_successor,
    is_quiescent,
    macro_state,
    micro_step,
    protocol_trajectory,
    quiescent_configuration,
    run_macro_action,
    token_bit,
    token_kind,
)


def test_fixed_binary_joint_token_grammar_is_independent_of_port_count():
    grammar = binary_joint_relay_grammar()
    assert grammar.verify()
    assert grammar.token_alphabet == (None, COPY_0, COPY_1, XOR_0, XOR_1)
    assert grammar.maximum_degree == 3
    assert grammar.relay_state_count == 5

    one = BinaryJointRelayTopology.balanced(1)
    five = BinaryJointRelayTopology.balanced(5)
    assert one.verify() and five.verify()
    assert one.maximum_degree_for_read(0) <= 3
    assert five.maximum_degree_for_read(4) <= 3
    assert one.maximum_degree_for_intervene <= 3
    assert five.maximum_degree_for_intervene <= 3


def test_read_uses_structural_port_and_copies_only_the_selected_exterior_bit():
    topology = BinaryJointRelayTopology.balanced(3)
    state = (1, 0, 1, 0, 1)
    initial = configuration_from_macro_state(topology, state)

    final = run_macro_action(topology, initial, BinaryJointMacroAction.read(1))
    assert is_quiescent(topology, final)
    assert macro_state(final) == (1, 0, 1, 0, 1)

    final = run_macro_action(topology, initial, BinaryJointMacroAction.read(0))
    assert macro_state(final) == (0, 0, 1, 0, 1)
    assert final.exterior_bits == (0, 1, 0)
    assert final.response_type == 1


def test_intervene_compiles_binary_response_type_as_xor_not_as_action_label():
    topology = BinaryJointRelayTopology.balanced(2)
    one = configuration_from_macro_state(topology, (1, 0, 1, 1))
    zero = configuration_from_macro_state(topology, (1, 0, 1, 0))

    flipped = run_macro_action(topology, one, BinaryJointMacroAction.intervene())
    unchanged = run_macro_action(topology, zero, BinaryJointMacroAction.intervene())
    assert macro_state(flipped) == (0, 0, 1, 1)
    assert macro_state(unchanged) == (1, 0, 1, 0)

    trajectory = protocol_trajectory(topology, one, BinaryJointMacroAction.intervene())
    assert token_kind(trajectory[1].leaf_tokens[topology.response_leaf_index]) == "xor"
    assert token_bit(trajectory[1].leaf_tokens[topology.response_leaf_index]) == 1


def test_observe_is_exact_quiescent_macro_noop():
    topology = BinaryJointRelayTopology.balanced(2)
    initial = configuration_from_macro_state(topology, (1, 0, 1, 0))
    certificate = certify_binary_joint_relay_protocol(topology, macro_state(initial), BinaryJointMacroAction.observe())
    assert certificate.verify()
    assert certificate.trajectory == (initial,)
    assert run_macro_action(topology, initial, BinaryJointMacroAction.observe()) == initial


def test_protocol_has_one_token_and_restores_quiescence_after_settling():
    topology = BinaryJointRelayTopology.balanced(4)
    initial = quiescent_configuration(topology, 1, (0, 1, 0, 1), 1)
    trajectory = protocol_trajectory(topology, initial, BinaryJointMacroAction.read(3))
    assert len(trajectory) == topology.settling_ticks + 1
    assert is_quiescent(topology, trajectory[0])
    assert is_quiescent(topology, trajectory[-1])
    assert sum(token is not None for token in trajectory[1].leaf_tokens) == 1
    assert all(
        sum(token is not None for token in configuration.leaf_tokens)
        + sum(token is not None for token in configuration.relay_tokens)
        <= 1
        for configuration in trajectory
    )


def test_compiled_macro_actions_match_the_existing_binary_joint_product():
    topology = BinaryJointRelayTopology.balanced(2)
    family = binary_joint_product(2)
    for state in all_binary_joint_states(2):
        for action in (BinaryJointMacroAction.observe(), BinaryJointMacroAction.read(0), BinaryJointMacroAction.read(1), BinaryJointMacroAction.intervene()):
            compiled = run_macro_action(topology, configuration_from_macro_state(topology, state), action)
            assert macro_state(compiled) == expected_macro_successor(topology, state, action)
            assert macro_state(compiled) in family.states


def test_exhaustive_binary_joint_compilation_certificate_attains_the_binary_product_size():
    certificate = certify_binary_joint_relay_compilation(3)
    assert certificate.verify()
    assert certificate.checked_macro_state_count == 2**5
    assert certificate.checked_read_protocols == 3 * 2**5
    assert certificate.checked_intervene_protocols == 2**5
    assert certificate.maximum_degree <= 3
    assert certificate.joint_safe_interface_bits == 5.0


def test_small_exhaustive_family_replay():
    certificates = exhaustive_binary_joint_compilation_summary(4)
    assert [certificate.topology.exterior_port_count for certificate in certificates] == [1, 2, 3, 4]
    assert all(certificate.verify() for certificate in certificates)


def test_directed_messages_are_pairwise_child_to_parent_tokens():
    topology = BinaryJointRelayTopology.balanced(2)
    initial = configuration_from_macro_state(topology, (0, 1, 0, 1))
    after_start = micro_step(topology, initial, BinaryJointMacroAction.read(0))
    messages = directed_edge_tokens(topology, after_start)
    assert all(child in topology.tree.nodes and parent in topology.tree.nodes for child, parent in messages)
    assert messages[(topology.exterior_leaves[0], topology.tree.parent_by_node[topology.exterior_leaves[0]])] == COPY_1


@pytest.mark.parametrize(
    "action",
    [
        BinaryJointMacroAction("read"),
        BinaryJointMacroAction("read", -1),
        BinaryJointMacroAction("read", 99),
        BinaryJointMacroAction("intervene", 0),
        BinaryJointMacroAction("observe", 0),
        BinaryJointMacroAction("unknown"),
    ],
)
def test_invalid_macro_action_contexts_fail_closed(action):
    topology = BinaryJointRelayTopology.balanced(2)
    with pytest.raises(ValueError):
        action.validate(topology)


def test_new_token_may_not_start_before_prior_protocol_returns_to_quiescence():
    topology = BinaryJointRelayTopology.balanced(2)
    initial = configuration_from_macro_state(topology, (0, 1, 0, 1))
    active = micro_step(topology, initial, BinaryJointMacroAction.read(0))
    with pytest.raises(ValueError, match="quiescence"):
        micro_step(topology, active, BinaryJointMacroAction.intervene())


def test_invalid_configurations_fail_closed():
    topology = BinaryJointRelayTopology.balanced(1)
    with pytest.raises(ValueError):
        quiescent_configuration(topology, 2, (0,), 0)
    with pytest.raises(ValueError):
        quiescent_configuration(topology, 0, (0, 1), 0)
    invalid = BinaryJointRelayConfiguration(
        focal_output=0,
        exterior_bits=(0,),
        response_type=0,
        leaf_tokens=("not-a-token", None),
        relay_tokens=(None,),
    )
    with pytest.raises(ValueError):
        micro_step(topology, invalid)
