from itertools import product

import pytest

from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.grammar_aware_blankets import certify_grammar_aware_canonical_interface
from causal_model.grammar_expansion_closure import (
    certify_grammar_expansion_closure,
    find_grammar_expansion_obstruction,
    globally_new_action_symbols,
    newly_enabled_transitions,
)
from causal_model.shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem


def _plant(actions):
    return FiniteControlledOutputSystem(actions, (tuple(0 for _ in actions),), (0,))


def test_uniform_globally_new_action_gives_zero_inflation():
    actions = ("stay", "reveal")
    plant = _plant(actions)
    closed = FinitePrefixGrammar(actions, ((0, None), (1, None)))
    opened = FinitePrefixGrammar(actions, ((0, 0), (1, 1)))
    cert = certify_grammar_expansion_closure(plant, closed, opened)
    assert cert.verify() and cert.zero_inflation
    assert cert.closed_block_count == cert.open_block_count == 1
    assert cert.new_action_symbols == ("reveal",)
    assert find_grammar_expansion_obstruction(plant, closed, opened) is None


def test_state_dependent_legality_of_new_action_forces_inflation():
    actions = ("stay", "reveal")
    plant = _plant(actions)
    closed = FinitePrefixGrammar(actions, ((0, None), (1, None)))
    opened = FinitePrefixGrammar(actions, ((0, 0), (1, None)))
    cert = certify_grammar_expansion_closure(plant, closed, opened)
    obstruction = find_grammar_expansion_obstruction(plant, closed, opened)
    assert cert.verify() and not cert.zero_inflation and cert.open_block_count == 2
    assert obstruction is not None and obstruction.verify() and obstruction.kind == "legality"


def test_uniform_new_legality_can_fail_successor_descent():
    actions = ("stay", "probe", "reveal")
    plant = _plant(actions)
    closed = FinitePrefixGrammar(actions, ((0, None, None), (1, None, None), (2, 2, None)))
    opened = FinitePrefixGrammar(actions, ((0, None, 0), (1, None, 2), (2, 2, None)))
    cert = certify_grammar_expansion_closure(plant, closed, opened)
    obstruction = find_grammar_expansion_obstruction(plant, closed, opened)
    assert cert.verify() and cert.closed_block_count == 2 and cert.open_block_count == 3
    assert obstruction is not None and obstruction.verify() and obstruction.kind == "successor"


def test_partial_completion_of_old_symbol_can_coarsen_and_is_rejected():
    actions = ("a", "b")
    plant = _plant(actions)
    closed = FinitePrefixGrammar(actions, ((0, None), (1, 1)))
    opened = FinitePrefixGrammar(actions, ((0, 0), (1, 1)))
    closed_canonical = certify_grammar_aware_canonical_interface(GrammarAwareControlledSystem(plant, closed))
    open_canonical = certify_grammar_aware_canonical_interface(GrammarAwareControlledSystem(plant, opened))
    assert closed_canonical.canonical_block_count == 2
    assert open_canonical.canonical_block_count == 1
    with pytest.raises(ValueError):
        certify_grammar_expansion_closure(plant, closed, opened)


def test_changed_old_transition_is_rejected():
    actions = ("a", "b")
    plant = _plant(actions)
    closed = FinitePrefixGrammar(actions, ((0, None), (1, None)))
    invalid = FinitePrefixGrammar(actions, ((1, None), (1, None)))
    with pytest.raises(ValueError):
        certify_grammar_expansion_closure(plant, closed, invalid)


def _valid_symbol_expansion(closed_rows, open_rows):
    for action_index in range(len(closed_rows[0])):
        closed_column = tuple(row[action_index] for row in closed_rows)
        open_column = tuple(row[action_index] for row in open_rows)
        if closed_column != open_column and any(target is not None for target in closed_column):
            return False
    return True


def test_all_two_state_two_action_cellwise_expansions_are_classified():
    actions = ("a", "b")
    plant = _plant(actions)
    cell_pairs = ((None, None), (None, 0), (None, 1), (0, 0), (1, 1))
    accepted = rejected = 0
    for cells in product(cell_pairs, repeat=4):
        c = tuple(pair[0] for pair in cells)
        o = tuple(pair[1] for pair in cells)
        closed_rows = (c[:2], c[2:])
        open_rows = (o[:2], o[2:])
        closed = FinitePrefixGrammar(actions, closed_rows)
        opened = FinitePrefixGrammar(actions, open_rows)
        if _valid_symbol_expansion(closed_rows, open_rows):
            cert = certify_grammar_expansion_closure(plant, closed, opened)
            obstruction = find_grammar_expansion_obstruction(plant, closed, opened)
            assert cert.verify() and cert.stable_labels == cert.open_labels
            assert cert.zero_inflation == (obstruction is None)
            accepted += 1
        else:
            with pytest.raises(ValueError):
                certify_grammar_expansion_closure(plant, closed, opened)
            rejected += 1
    assert (accepted, rejected) == (289, 336)


def test_new_transition_and_symbol_inventory():
    actions = ("a", "b")
    closed = FinitePrefixGrammar(actions, ((0, None), (1, None)))
    opened = FinitePrefixGrammar(actions, ((0, 1), (1, 0)))
    assert globally_new_action_symbols(closed, opened) == ("b",)
    assert newly_enabled_transitions(closed, opened) == ((0, "b", 1), (1, "b", 0))
