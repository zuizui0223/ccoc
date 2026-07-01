import math

import pytest

from causal_model.delayed_addressability import FinitePrefixGrammar, GrammarAwareControlledSystem
from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.grammar_aware_blankets import (
    FIRE,
    WAIT,
    GrammarAwareDynamicInterfaceCertificate,
    certify_grammar_aware_canonical_interface,
    certify_grammar_aware_dynamic_blanket,
    certify_grammar_aware_refinement,
    certify_grammar_state_necessity,
    constant_output_delayed_system,
    explicit_grammar_aware_partition,
    find_enabled_action_mismatch,
    grammar_aware_output_trace,
)


def _full_action_grammar(actions: tuple[str, ...]) -> FinitePrefixGrammar:
    return FinitePrefixGrammar(actions=actions, transition_table=(tuple(0 for _ in actions),))


def test_canonical_grammar_aware_partition_matches_explicit_legal_word_traces():
    constrained = constant_output_delayed_system(delay=3)
    for horizon in range(6):
        assert constrained.product_partition(horizon) == explicit_grammar_aware_partition(constrained, horizon)


def test_grammar_state_is_required_even_when_physical_state_and_output_are_constant():
    certificate = certify_grammar_state_necessity(delay=3)
    assert certificate.verify()
    assert certificate.constrained_system.system.state_count == 1
    assert certificate.canonical.canonical_block_count == 5
    assert certificate.canonical.initial_slice_block_count == 1
    assert certificate.enabled_action_obstruction.left == (0, 0)
    assert certificate.enabled_action_obstruction.right == (0, 3)
    assert certificate.enabled_action_obstruction.left_enabled_actions == (WAIT,)
    assert certificate.enabled_action_obstruction.right_enabled_actions == (FIRE,)


def test_grammar_state_summary_constructs_an_exact_partial_macro_law():
    constrained = constant_output_delayed_system(delay=2)
    summary = tuple(grammar_state for _, grammar_state in constrained.product_states)
    interface = GrammarAwareDynamicInterfaceCertificate(constrained, summary)
    assert interface.verify()
    assert interface.summary_block_count == 4
    assert interface.macro_output(0) == "constant-window-output"
    assert interface.macro_legal_actions(0) == (WAIT,)
    assert interface.macro_legal_actions(2) == (FIRE,)
    assert interface.macro_transition(0, WAIT) == 1
    assert interface.macro_transition(2, FIRE) == 3
    with pytest.raises(ValueError, match="illegal"):
        interface.macro_transition(0, FIRE)


def test_grammar_aware_blanket_bounds_canonical_memory_and_horizon():
    constrained = constant_output_delayed_system(delay=4)
    summary = tuple(grammar_state for _, grammar_state in constrained.product_states)
    certificate = certify_grammar_aware_dynamic_blanket(constrained, summary)
    assert certificate.verify()
    assert certificate.summary_block_count == 6
    assert certificate.canonical_block_count == 6
    assert certificate.canonical_interface_bits == math.log2(6)
    assert certificate.blanket_upper_bound_bits == math.log2(6)
    assert certificate.stabilization_horizon <= certificate.summary_horizon_bound


def test_any_valid_dynamic_summary_refines_the_canonical_legal_word_quotient():
    constrained = constant_output_delayed_system(delay=3)
    identity_summary = tuple(constrained.product_states)
    refinement = certify_grammar_aware_refinement(constrained, identity_summary)
    assert refinement.verify()
    assert refinement.interface.summary_block_count == constrained.product_state_count
    assert refinement.canonical.canonical_block_count == constrained.grammar.state_count


def test_enabled_action_mismatch_is_an_explicit_obstruction_to_omitting_grammar_state():
    constrained = constant_output_delayed_system(delay=2)
    omitted = ("same",) * constrained.product_state_count
    mismatch = find_enabled_action_mismatch(constrained, omitted)
    assert mismatch is not None
    assert mismatch.verify()
    assert not GrammarAwareDynamicInterfaceCertificate(constrained, omitted).verify()


def test_successor_mismatch_fails_even_when_outputs_and_enabled_actions_match():
    system = FiniteControlledOutputSystem(
        actions=("step",),
        transition_table=((0,), (2,), (2,)),
        outputs=(0, 0, 1),
    )
    constrained = GrammarAwareControlledSystem(system=system, grammar=_full_action_grammar(("step",)))
    invalid_summary = ("same", "same", "different")
    assert find_enabled_action_mismatch(constrained, invalid_summary) is None
    assert not GrammarAwareDynamicInterfaceCertificate(constrained, invalid_summary).verify()
    with pytest.raises(ValueError, match="not a grammar-aware dynamic interface"):
        certify_grammar_aware_refinement(constrained, invalid_summary)


def test_one_state_full_grammar_reduces_to_the_ordinary_dynamic_interface_case():
    system = FiniteControlledOutputSystem(
        actions=("step",),
        transition_table=((1,), (0,)),
        outputs=(0, 1),
    )
    constrained = GrammarAwareControlledSystem(system=system, grammar=_full_action_grammar(("step",)))
    canonical = certify_grammar_aware_canonical_interface(constrained)
    assert canonical.verify()
    assert canonical.canonical_block_count == 2
    assert canonical.initial_slice_block_count == 2


def test_legal_trace_requires_the_declared_grammar_contract():
    constrained = constant_output_delayed_system(delay=1)
    assert grammar_aware_output_trace(constrained, (0, 0), (WAIT, FIRE)) == (
        "constant-window-output",
        "constant-window-output",
        "constant-window-output",
    )
    with pytest.raises(ValueError, match="illegal"):
        grammar_aware_output_trace(constrained, (0, 0), (FIRE,))


@pytest.mark.parametrize(
    "bad_delay",
    [-1, True, 1.5, "2"],
)
def test_invalid_necessity_delays_fail_closed(bad_delay):
    with pytest.raises(ValueError):
        constant_output_delayed_system(bad_delay)


@pytest.mark.parametrize(
    "bad_labels",
    [
        (),
        ("only",),
        ([],) * 3,
    ],
)
def test_invalid_summary_shapes_or_labels_fail_closed(bad_labels):
    constrained = constant_output_delayed_system(delay=1)
    assert not GrammarAwareDynamicInterfaceCertificate(constrained, bad_labels).verify()


def test_invalid_product_state_is_rejected_in_trace_query():
    constrained = constant_output_delayed_system(delay=1)
    with pytest.raises(ValueError):
        grammar_aware_output_trace(constrained, (1, 0), ())
    with pytest.raises(ValueError):
        grammar_aware_output_trace(constrained, (0, 9), ())
