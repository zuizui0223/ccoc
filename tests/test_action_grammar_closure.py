from itertools import product

import pytest

from causal_model.action_grammar_closure import (
    ActionDescentObstructionCertificate,
    ActionGrammarClosureCertificate,
    action_grammar_refinement_trace,
    canonical_action_quotient_labels,
    certify_action_grammar_closure,
    find_action_descent_obstruction,
    newly_legal_actions_descend,
)
from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem


def zero_system() -> FiniteControlledOutputSystem:
    return FiniteControlledOutputSystem(("c", "n"), ((0, 2), (1, 2), (2, 2)), (0, 0, 1))


def split_system() -> FiniteControlledOutputSystem:
    return FiniteControlledOutputSystem(("c", "n"), ((0, 0), (1, 2), (2, 2)), (0, 0, 1))


def cascade_system(depth: int) -> FiniteControlledOutputSystem:
    if depth < 1:
        raise ValueError("depth must be positive")
    state_count = depth + 2
    z, x0 = 0, 1
    new_targets = [x0, x0]
    for j in range(1, depth + 1):
        state = x0 + j
        new_targets.append(z if j == 1 else state - 1)
    table = tuple((x0, new_targets[state]) for state in range(state_count))
    return FiniteControlledOutputSystem(("c", "n"), table, (1,) + (0,) * (state_count - 1))


def test_zero_inflation_iff_new_action_descends() -> None:
    system = zero_system()
    cert = certify_action_grammar_closure(system, ("c",), ("c", "n"))
    assert isinstance(cert, ActionGrammarClosureCertificate)
    assert cert.verify()
    assert cert.closed_block_count == cert.open_block_count == 2
    assert cert.zero_inflation
    assert newly_legal_actions_descend(system, ("c",), ("c", "n"))
    assert cert.descent_obstruction is None


def test_failed_descent_constructs_open_witness() -> None:
    system = split_system()
    cert = certify_action_grammar_closure(system, ("c",), ("c", "n"))
    assert cert.verify()
    assert cert.closed_block_count == 2
    assert cert.open_block_count == 3
    assert not cert.zero_inflation
    obstruction = cert.descent_obstruction
    assert isinstance(obstruction, ActionDescentObstructionCertificate)
    assert obstruction.verify()
    assert obstruction.open_witness_word == ("n",)


def test_obstruction_can_need_closed_suffix() -> None:
    system = FiniteControlledOutputSystem(
        ("c", "n"),
        ((0, 2), (1, 3), (4, 2), (3, 3), (4, 4)),
        (0, 0, 0, 0, 1),
    )
    obstruction = find_action_descent_obstruction(system, ("c",), ("c", "n"))
    assert obstruction is not None and obstruction.verify()
    assert obstruction.closed_distinguishing_suffix == ("c",)
    assert obstruction.open_witness_word == ("n", "c")


def test_cascade_attains_round_bound() -> None:
    for depth in range(1, 6):
        cert = certify_action_grammar_closure(cascade_system(depth), ("c",), ("c", "n"))
        assert cert.verify()
        assert cert.closed_block_count == 2
        assert cert.open_block_count == cert.system.state_count
        assert cert.refinement_rounds == cert.refinement_round_bound == depth
        assert tuple(len(set(labels)) for labels in cert.refinement_labels) == tuple(
            range(2, cert.system.state_count + 1)
        )


def test_stable_refinement_equals_direct_open_quotient() -> None:
    system = cascade_system(4)
    assert action_grammar_refinement_trace(system, ("c",), ("c", "n"))[-1] == canonical_action_quotient_labels(
        system, ("c", "n")
    )


def test_all_two_state_plants_satisfy_converse() -> None:
    transition_functions = tuple(product(range(2), repeat=2))
    checked = 0
    for closed_transition in transition_functions:
        for new_transition in transition_functions:
            table = tuple((closed_transition[s], new_transition[s]) for s in range(2))
            for outputs in product((0, 1), repeat=2):
                system = FiniteControlledOutputSystem(("c", "n"), table, outputs)
                cert = certify_action_grammar_closure(system, ("c",), ("c", "n"))
                assert cert.verify()
                assert cert.stable_open_labels == canonical_action_quotient_labels(system, ("c", "n"))
                assert cert.zero_inflation == newly_legal_actions_descend(system, ("c",), ("c", "n"))
                checked += 1
    assert checked == 64


def test_validation_fails_closed() -> None:
    system = zero_system()
    with pytest.raises(ValueError):
        certify_action_grammar_closure(system, ("n",), ("c",))
    with pytest.raises(ValueError):
        canonical_action_quotient_labels(system, ("bogus",))
