from itertools import product

from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.grammar_interface_reuse import certify_closed_interface_reuse, find_closed_interface_reuse_obstruction
from causal_model.shared_grammar import FinitePrefixGrammar


def _plant(actions):
    return FiniteControlledOutputSystem(actions, (tuple(0 for _ in actions),), (0,))


def test_equal_and_reusable():
    actions=("a","b"); plant=_plant(actions); grammar=FinitePrefixGrammar(actions,((0,None),(1,None)))
    cert=certify_closed_interface_reuse(plant,grammar,grammar)
    assert cert.verify() and cert.reusable and cert.relation=="equal"


def test_open_coarser_but_closed_reusable():
    actions=("a","b"); plant=_plant(actions)
    closed=FinitePrefixGrammar(actions,((0,None),(1,1))); opened=FinitePrefixGrammar(actions,((0,0),(1,1)))
    cert=certify_closed_interface_reuse(plant,closed,opened)
    assert cert.verify() and cert.reusable and cert.relation=="closed_refines_open"
    assert (cert.closed_block_count,cert.open_block_count,cert.minimal_block_delta)==(2,1,-1)


def test_open_finer_and_reuse_fails():
    actions=("a","b"); plant=_plant(actions)
    closed=FinitePrefixGrammar(actions,((0,None),(1,None))); opened=FinitePrefixGrammar(actions,((0,0),(1,None)))
    cert=certify_closed_interface_reuse(plant,closed,opened); obstruction=find_closed_interface_reuse_obstruction(plant,closed,opened)
    assert cert.verify() and not cert.reusable and cert.relation=="open_refines_closed"
    assert obstruction is not None and obstruction.verify() and obstruction.kind=="legality"


def test_canonical_quotients_can_be_incomparable():
    actions=("a","b"); plant=_plant(actions)
    closed=FinitePrefixGrammar(actions,((None,None),(None,None),(None,0)))
    opened=FinitePrefixGrammar(actions,((None,None),(None,0),(None,0)))
    cert=certify_closed_interface_reuse(plant,closed,opened); obstruction=find_closed_interface_reuse_obstruction(plant,closed,opened)
    assert cert.verify() and not cert.reusable and cert.relation=="incomparable"
    assert (cert.closed_block_count,cert.open_block_count)==(2,2)
    assert obstruction is not None and obstruction.verify() and obstruction.kind=="legality"


def test_successor_obstruction_is_distinct():
    actions=("stay","probe","reveal"); plant=_plant(actions)
    closed=FinitePrefixGrammar(actions,((0,None,None),(1,None,None),(2,2,None)))
    opened=FinitePrefixGrammar(actions,((0,None,0),(1,None,2),(2,2,None)))
    cert=certify_closed_interface_reuse(plant,closed,opened); obstruction=find_closed_interface_reuse_obstruction(plant,closed,opened)
    assert cert.verify() and not cert.reusable
    assert obstruction is not None and obstruction.verify() and obstruction.kind=="successor"


def test_all_625_cellwise_monotone_changes_have_exact_reuse_decision():
    actions=("a","b"); plant=_plant(actions)
    cell_pairs=((None,None),(None,0),(None,1),(0,0),(1,1)); checked=0
    for cells in product(cell_pairs,repeat=4):
        c=tuple(pair[0] for pair in cells); o=tuple(pair[1] for pair in cells)
        closed=FinitePrefixGrammar(actions,(c[:2],c[2:])); opened=FinitePrefixGrammar(actions,(o[:2],o[2:]))
        cert=certify_closed_interface_reuse(plant,closed,opened)
        obstruction=find_closed_interface_reuse_obstruction(plant,closed,opened)
        assert cert.verify() and cert.reusable==(obstruction is None)
        checked+=1
    assert checked==625
