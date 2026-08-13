from itertools import product

import pytest

from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.grammar_expansion_closure import certify_grammar_expansion_closure, find_grammar_expansion_obstruction, newly_enabled_transitions
from causal_model.shared_grammar import FinitePrefixGrammar


def _one_state_plant(actions: tuple[str, ...]) -> FiniteControlledOutputSystem:
    return FiniteControlledOutputSystem(actions, (tuple(0 for _ in actions),), (0,))


def test_uniform_new_legality_and_successors_give_zero_inflation() -> None:
    actions = ("stay", "reveal")
    plant = _one_state_plant(actions)
    closed = FinitePrefixGrammar(actions, ((0, None), (1, None)))
    opened = FinitePrefixGrammar(actions, ((0, 0), (1, 1)))
    certificate = certify_grammar_expansion_closure(plant, closed, opened)
    assert certificate.verify()
    assert certificate.closed_block_count == 1
    assert certificate.open_block_count == 1
    assert certificate.zero_inflation
    assert certificate.newly_enabled_transition_count == 2
    assert find_grammar_expansion_obstruction(plant, closed, opened) is None


def test_state_dependent_new_legality_forces_inflation() -> None:
    actions = ("stay", "reveal")
    plant = _one_state_plant(actions)
    closed = FinitePrefixGrammar(actions, ((0, None), (1, None)))
    opened = FinitePrefixGrammar(actions, ((0, 0), (1, None)))
    certificate = certify_grammar_expansion_closure(plant, closed, opened)
    obstruction = find_grammar_expansion_obstruction(plant, closed, opened)
    assert certificate.verify() and not certificate.zero_inflation
    assert certificate.open_block_count == 2
    assert obstruction is not None and obstruction.verify()
    assert obstruction.kind == "legality" and obstruction.action == "reveal"


def test_uniform_new_legality_can_fail_successor_descent() -> None:
    actions = ("stay", "probe", "reveal")
    plant = _one_state_plant(actions)
    closed = FinitePrefixGrammar(actions, ((0, None, None), (1, None, None), (2, 2, None)))
    opened = FinitePrefixGrammar(actions, ((0, None, 0), (1, None, 2), (2, 2, None)))
    certificate = certify_grammar_expansion_closure(plant, closed, opened)
    obstruction = find_grammar_expansion_obstruction(plant, closed, opened)
    assert certificate.verify() and not certificate.zero_inflation
    assert certificate.closed_block_count == 2 and certificate.open_block_count == 3
    assert obstruction is not None and obstruction.verify()
    assert obstruction.kind == "successor" and obstruction.action == "reveal"


def test_changed_old_transition_is_rejected() -> None:
    actions = ("a", "b")
    plant = _one_state_plant(actions)
    closed = FinitePrefixGrammar(actions, ((0, None), (1, None)))
    invalid = FinitePrefixGrammar(actions, ((1, None), (1, None)))
    with pytest.raises(ValueError):
        certify_grammar_expansion_closure(plant, closed, invalid)


def test_all_two_state_two_action_monotone_grammar_expansions() -> None:
    actions = ("a", "b")
    plant = _one_state_plant(actions)
    cell_pairs = ((None, None), (None, 0), (None, 1), (0, 0), (1, 1))
    checked = 0
    for cells in product(cell_pairs, repeat=4):
        c = tuple(pair[0] for pair in cells)
        o = tuple(pair[1] for pair in cells)
        closed = FinitePrefixGrammar(actions, (c[:2], c[2:]))
        opened = FinitePrefixGrammar(actions, (o[:2], o[2:]))
        certificate = certify_grammar_expansion_closure(plant, closed, opened)
        obstruction = find_grammar_expansion_obstruction(plant, closed, opened)
        assert certificate.verify()
        assert certificate.stable_labels == certificate.open_labels
        assert certificate.zero_inflation == (obstruction is None)
        assert certificate.strict_refinement_rounds <= certificate.refinement_round_bound
        checked += 1
    assert checked == 625


def test_new_transition_inventory_is_exact() -> None:
    actions = ("a", "b")
    closed = FinitePrefixGrammar(actions, ((0, None), (1, None)))
    opened = FinitePrefixGrammar(actions, ((0, 1), (1, 0)))
    assert newly_enabled_transitions(closed, opened) == ((0, "b", 1), (1, "b", 0))
