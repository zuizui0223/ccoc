from itertools import product

import pytest

from causal_model.delayed_addressability import (
    FIRE,
    WAIT,
    DelayedOpenFamily,
    DelayedReaderGrammar,
    FinitePrefixGrammar,
    GrammarAwareControlledSystem,
    certify_delayed_addressability,
    certify_delayed_closure_nonidentifiability,
    certify_delayed_relay_attachment,
    certify_grammar_horizon_stabilization,
    delayed_separating_word_certificate,
)
from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem


def _explicit_initial_partition(constrained: GrammarAwareControlledSystem, horizon: int):
    grammar = constrained.grammar
    words = grammar.legal_words_through(horizon)
    buckets = {}
    for state in constrained.system.states:
        signature = tuple(constrained.system.output_trace(state, word) for word in words)
        buckets.setdefault(signature, []).append(state)
    return tuple(sorted((tuple(block) for block in buckets.values()), key=lambda block: block[0]))


def test_delayed_grammar_has_constant_local_alphabet_and_blocks_fire_until_ready():
    grammar = DelayedReaderGrammar(3)
    assert grammar.verify()
    assert grammar.as_prefix_grammar().actions == (WAIT, FIRE)
    assert grammar.legal_words_through(3) == ((), (WAIT,), (WAIT, WAIT), (WAIT, WAIT, WAIT))
    assert grammar.revealing_word == (WAIT, WAIT, WAIT, FIRE)
    assert FIRE not in sum((list(word) for word in grammar.legal_words_through(3)), [])


def test_delayed_addressability_has_independent_memory_and_horizon_axes():
    certificate = certify_delayed_addressability(module_count=4, delay=3)
    assert certificate.verify()
    assert certificate.pre_reveal_open_block_count == 2
    assert certificate.open_block_count == 32
    assert certificate.closed_block_counts == (4, 4, 4, 4)
    assert certificate.open_interface_bits == 5.0
    assert certificate.closed_interface_bits == (2.0, 2.0, 2.0, 2.0)
    assert certificate.counterfactual_delay == 4


def test_all_pre_fire_grammar_aware_partitions_are_completion_blind():
    family = DelayedOpenFamily(module_count=3, delay=4, reveals_exterior=True)
    for horizon in range(5):
        assert family.robust_block_count(horizon) == 2
        for port in family.ports:
            assert len(family.context(port).horizon_partition(horizon)) == 2
    assert family.robust_block_count(5) == 16
    assert all(len(block) == 1 for block in family.robust_partition(5))


def test_each_exterior_coordinate_has_one_delayed_concrete_separating_word():
    for port in range(5):
        certificate = delayed_separating_word_certificate(5, delay=2, port=port, focal_bit=1)
        assert certificate.verify()
        assert certificate.word == (WAIT, WAIT, FIRE)
        assert certificate.left_trace[:-1] == certificate.right_trace[:-1]
        assert certificate.left_trace[-1] != certificate.right_trace[-1]


def test_closed_open_models_agree_through_delay_and_diverge_at_the_next_legal_word():
    certificate = certify_delayed_closure_nonidentifiability(module_count=3, delay=5, port=2)
    assert certificate.verify()
    assert certificate.shared_horizon == 5
    assert certificate.separating_word == (WAIT, WAIT, WAIT, WAIT, WAIT, FIRE)
    assert certificate.closed_trace[-1] == 0
    assert certificate.open_trace[-1] == 1


def test_grammar_aware_refinement_matches_explicit_legal_word_traces():
    context = DelayedOpenFamily(module_count=2, delay=2).context(0)
    constrained = context.constrained_system()
    for horizon in range(5):
        assert constrained.initial_partition(horizon) == _explicit_initial_partition(constrained, horizon)


def test_general_prefix_grammar_product_stabilizes_by_product_state_bound():
    system = FiniteControlledOutputSystem(
        actions=("a", "b"),
        transition_table=((1, 0), (1, 0)),
        outputs=(0, 1),
    )
    grammar = FinitePrefixGrammar(
        actions=("a", "b"),
        transition_table=((1, None), (None, 2), (None, None)),
    )
    certificate = certify_grammar_horizon_stabilization(GrammarAwareControlledSystem(system, grammar))
    assert certificate.verify()
    assert certificate.stabilization_horizon <= certificate.product_state_bound


def test_relay_realization_keeps_attachment_structural_and_degree_bounded():
    # Port 2 means the third memory leaf, whose bit is 1 in this fixture.
    state = (0, 0, 0, 1, 0)
    certificate = certify_delayed_relay_attachment(module_count=4, delay=5, port=2, initial_state=state)
    assert certificate.verify()
    assert len(certificate.wait_configurations) == 6
    assert certificate.final_configuration.focal_output == 1


@pytest.mark.parametrize(
    "bad_grammar",
    [
        FinitePrefixGrammar(actions=("a",), transition_table=((None,),)),
    ],
)
def test_terminal_only_grammar_is_still_well_formed(bad_grammar):
    assert bad_grammar.legal_words_through(4) == ((),)


@pytest.mark.parametrize("bad_delay", [-1, True, 1.5, "2"])
def test_invalid_delays_fail_closed(bad_delay):
    with pytest.raises(ValueError):
        DelayedReaderGrammar(bad_delay)


@pytest.mark.parametrize("bad_port", [-1, 2, True, "0"])
def test_invalid_ports_fail_closed(bad_port):
    with pytest.raises(ValueError):
        delayed_separating_word_certificate(2, delay=1, port=bad_port)
