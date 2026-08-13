import pytest

from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.terminal_grammar_portability import (
    TerminalGrammarPortabilityCertificate,
    certify_terminal_grammar_portability,
)
from causal_model.shared_grammar import FinitePrefixGrammar


def _constant_plant() -> FiniteControlledOutputSystem:
    actions = ("stay", "u", "v")
    return FiniteControlledOutputSystem(
        actions,
        ((0, 0, 0),),
        ("constant",),
    )


def _chain_u_then_v():
    actions = ("stay", "u", "v")
    g0 = FinitePrefixGrammar(
        actions,
        (
            (0, None, None),
            (1, None, None),
            (2, None, None),
        ),
    )
    g1 = FinitePrefixGrammar(
        actions,
        (
            (0, 0, None),
            (1, None, None),
            (2, None, None),
        ),
    )
    g2 = FinitePrefixGrammar(
        actions,
        (
            (0, 0, None),
            (1, None, 1),
            (2, None, None),
        ),
    )
    return (g0, g1, g2)


def _chain_v_then_u():
    actions = ("stay", "u", "v")
    g0 = FinitePrefixGrammar(
        actions,
        (
            (0, None, None),
            (1, None, None),
            (2, None, None),
        ),
    )
    g1 = FinitePrefixGrammar(
        actions,
        (
            (0, None, None),
            (1, None, 1),
            (2, None, None),
        ),
    )
    g2 = FinitePrefixGrammar(
        actions,
        (
            (0, 0, None),
            (1, None, 1),
            (2, None, None),
        ),
    )
    return (g0, g1, g2)


def test_terminal_labels_are_minimal_uniform_interface_for_chain() -> None:
    certificate = certify_terminal_grammar_portability(
        _constant_plant(), _chain_u_then_v()
    )

    assert isinstance(certificate, TerminalGrammarPortabilityCertificate)
    assert certificate.verify()
    assert certificate.stage_block_counts == (1, 2, 3)
    assert certificate.terminal_block_count == 3
    assert certificate.minimal_uniform_interface_block_count == 3
    assert certificate.introduced_symbols_by_step == (("u",), ("v",))
    assert not certificate.uniform_interface_exists_with_at_most(2)
    assert certificate.uniform_interface_exists_with_at_most(3)
    with pytest.raises(ValueError):
        certificate.uniform_interface_exists_with_at_most(0)


def test_terminal_labels_construct_one_conservative_schema() -> None:
    certificate = certify_terminal_grammar_portability(
        _constant_plant(), _chain_u_then_v()
    )
    conservative = certificate.conservative_schema_certificate

    assert conservative.verify()
    assert conservative.schema.state_count == 3
    assert len(conservative.stages) == 3
    assert len(conservative.embeddings) == 2


def test_addition_order_does_not_change_terminal_uniform_budget() -> None:
    plant = _constant_plant()
    left = certify_terminal_grammar_portability(plant, _chain_u_then_v())
    right = certify_terminal_grammar_portability(plant, _chain_v_then_u())

    assert left.verify() and right.verify()
    assert left.grammars[-1] == right.grammars[-1]
    assert left.terminal_labels == right.terminal_labels
    assert left.minimal_uniform_interface_block_count == 3
    assert right.minimal_uniform_interface_block_count == 3
    assert left.introduced_symbols_by_step == (("u",), ("v",))
    assert right.introduced_symbols_by_step == (("v",), ("u",))


def test_single_stage_chain_reduces_to_terminal_canonical_interface() -> None:
    plant = _constant_plant()
    final = _chain_u_then_v()[-1]
    certificate = certify_terminal_grammar_portability(plant, (final,))

    assert certificate.verify()
    assert certificate.stage_count == 1
    assert certificate.stage_block_counts == (3,)
    assert certificate.introduced_symbols_by_step == ()
    assert certificate.minimal_uniform_interface_block_count == 3


def test_partial_completion_of_old_symbol_is_rejected() -> None:
    actions = ("stay", "u", "v")
    plant = _constant_plant()
    source = FinitePrefixGrammar(
        actions,
        (
            (0, 0, None),
            (1, None, None),
            (2, None, None),
        ),
    )
    invalid_target = FinitePrefixGrammar(
        actions,
        (
            (0, 0, None),
            (1, 1, None),
            (2, None, None),
        ),
    )

    with pytest.raises(ValueError):
        certify_terminal_grammar_portability(plant, (source, invalid_target))
