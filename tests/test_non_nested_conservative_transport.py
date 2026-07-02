"""Regression tests for conservative non-nested replacement transport."""

import pytest

import causal_model.portability_core as portability
from causal_model.coherent_portable_macrolaw import StageMacroProjection
from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.non_nested_conservative_transport import (
    ConservativeTransportedSchemaCertificate,
    certify_conservative_transported_schema,
    conservative_non_nested_replacement_witness,
)
from causal_model.shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem


def test_many_to_one_transport_constructs_a_schema_with_target_only_reveal():
    certificate = conservative_non_nested_replacement_witness()

    assert certificate.verify()
    assert certificate.target_labels == (0, 1)
    assert certificate.source_stage.stage_rows() == ((1, None), (0, None))
    assert certificate.target_stage.stage_rows() == ((1, 1), (0, 1))
    assert certificate.schema.transition_rows == ((1, 1), (0, 1))
    assert certificate.target_projection.verify()


def test_rejects_missing_successor_closure_for_an_old_legal_action():
    actions = ("flip", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((2, 0), (2, 1), (0, 2)), ("low", "low", "high")),
            FinitePrefixGrammar(actions=actions, transition_table=((0, None),)),
        ),
        (0, 0, 1),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, ((1, 1), (0, 1)), ("low", "high")),
        FinitePrefixGrammar(actions=actions, transition_table=((0, 0),)),
    )
    certificate = ConservativeTransportedSchemaCertificate(source, target, ((0, 0), (1, 0), (2, 0)))

    assert not certificate.verify()
    with pytest.raises(ValueError, match="successor-closed"):
        _ = certificate.target_labels


def test_rejects_target_only_action_with_nonuniform_macro_successor():
    actions = ("stay", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(
                actions,
                ((0, 0), (1, 1), (2, 2)),
                ("same", "same", "same"),
            ),
            FinitePrefixGrammar(actions=actions, transition_table=((0, None),)),
        ),
        (0, 0, 1),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(
            actions,
            ((0, 0), (1, 2), (2, 2)),
            ("same", "same", "same"),
        ),
        FinitePrefixGrammar(actions=actions, transition_table=((0, 0),)),
    )
    certificate = ConservativeTransportedSchemaCertificate(source, target, ((0, 0), (1, 1), (2, 2)))

    assert source.verify()
    assert not certificate.verify()
    with pytest.raises(ValueError, match="label-deterministic"):
        _ = certificate.schema


def test_rejects_nonuniform_target_only_action_availability():
    actions = ("stay", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((0, 0), (1, 1)), ("same", "same")),
            FinitePrefixGrammar(actions=actions, transition_table=((0, None),)),
        ),
        (0, 0),
    )
    target_system = FiniteControlledOutputSystem(actions, ((0, 0), (1, 1)), ("same", "same"))
    target_grammar = FinitePrefixGrammar(
        actions=actions,
        transition_table=((0, None), (1, 1)),
    )
    target = GrammarAwareControlledSystem(target_system, target_grammar)
    certificate = ConservativeTransportedSchemaCertificate(source, target, ((0, 0), (1, 1)))

    assert source.verify()
    assert not certificate.verify()
    with pytest.raises(ValueError, match="availability"):
        _ = certificate.schema


def test_constructor_rejects_a_nonconservative_transport():
    actions = ("stay", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((0, 0), (1, 1), (2, 2)), ("same", "same", "same")),
            FinitePrefixGrammar(actions=actions, transition_table=((0, None),)),
        ),
        (0, 0, 1),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, ((0, 0), (1, 2), (2, 2)), ("same", "same", "same")),
        FinitePrefixGrammar(actions=actions, transition_table=((0, 0),)),
    )

    with pytest.raises(ValueError, match="conservative target schema"):
        certify_conservative_transported_schema(source, target, ((0, 0), (1, 1), (2, 2)))


def test_certificate_is_exported_from_the_portability_facade():
    assert portability.conservative_non_nested_replacement_witness is conservative_non_nested_replacement_witness
    assert "ConservativeTransportedSchemaCertificate" in portability.__all__
    assert "certify_conservative_transported_schema" in portability.__all__
