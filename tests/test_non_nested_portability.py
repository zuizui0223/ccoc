"""Regression tests for non-nested replacement portability."""

import pytest

from causal_model.coherent_portable_macrolaw import PortableMacroDynamics, StageMacroProjection
from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.non_nested_portability import (
    ReplacementTransport,
    certify_transport_coherent_portable_macro_law,
    non_nested_replacement_witness,
    non_nested_rewiring_obstruction,
)
from causal_model.shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem


def test_many_to_one_replacement_transport_preserves_one_exact_macro_law():
    certificate = non_nested_replacement_witness()

    assert certificate.verify()
    assert certificate.macro.outputs == ("low", "high")
    assert len(certificate.stages) == 2
    transport = certificate.transports[0]
    assert transport.verify()
    assert transport.source.constrained_system.product_state_count == 3
    assert transport.target.constrained_system.product_state_count == 2
    assert not transport.is_source_injective


def test_transport_rejects_a_relation_that_is_not_successor_closed():
    valid = non_nested_replacement_witness().transports[0]
    invalid = ReplacementTransport(
        source=valid.source,
        target=valid.target,
        relation=((0, 0), (1, 0), (2, 0)),
    )

    assert not invalid.verify()


def test_newly_legal_reveal_refutes_a_proposed_non_nested_carried_merge():
    obstruction = non_nested_rewiring_obstruction()

    assert obstruction.verify()
    assert obstruction.source.constrained_system.product_state_count == 4
    assert obstruction.target_system.product_state_count == 3
    assert obstruction.future_word == ("reveal",)


def test_transport_family_requires_connected_replacement_graph():
    actions = ("flip",)
    macro = PortableMacroDynamics(actions, ("low", "high"), (actions, actions), ((1,), (0,)))
    grammar = FinitePrefixGrammar(actions=actions, transition_table=((0,),))
    first = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((1,), (0,)), ("low", "high")),
            grammar,
        ),
        (0, 1),
    )
    second = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((1,), (0,)), ("low", "high")),
            grammar,
        ),
        (0, 1),
    )

    with pytest.raises(ValueError, match="replacement transports"):
        certify_transport_coherent_portable_macro_law(macro, (first, second), ())
