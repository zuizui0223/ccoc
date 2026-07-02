"""Regression tests for non-nested replacement portability."""

import pytest

import causal_model.portability_core as portability
from causal_model.coherent_portable_macrolaw import PortableMacroDynamics, StageMacroProjection
from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.non_nested_portability import (
    ReplacementTransport,
    TransportedTargetProjectionCertificate,
    certify_transport_coherent_portable_macro_law,
    certify_transported_target_projection,
    non_nested_replacement_witness,
    non_nested_rewiring_obstruction,
    transported_target_projection_witness,
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


def test_transport_constructs_target_projection_without_target_labels_as_input():
    certificate = transported_target_projection_witness()

    assert certificate.verify()
    assert certificate.target_labels == (0, 1)
    assert certificate.target_projection.verify()
    assert certificate.target_projection.induced_macro() == certificate.source.induced_macro()
    assert certificate.target_system.product_state_count == 2


def test_transport_rejects_a_relation_that_is_not_successor_closed():
    actions = ("flip",)
    grammar = FinitePrefixGrammar(actions=actions, transition_table=((0,),))
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((2,), (2,), (0,)), ("low", "low", "high")),
            grammar,
        ),
        (0, 0, 1),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, ((1,), (2,), (0,)), ("low", "low", "high")),
        grammar,
    )
    certificate = TransportedTargetProjectionCertificate(source, target, ((0, 0), (1, 1), (2, 2)))

    assert not certificate.verify()
    with pytest.raises(ValueError, match="successor-closed"):
        _ = certificate.target_labels


def test_transport_rejects_label_inconsistent_target_fiber():
    actions = ("stay",)
    grammar = FinitePrefixGrammar(actions=actions, transition_table=((0,),))
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((0,), (1,)), ("low", "low")),
            grammar,
        ),
        (0, 1),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, ((0,),), ("low",)),
        grammar,
    )
    certificate = TransportedTargetProjectionCertificate(source, target, ((0, 0), (1, 0)))

    assert source.verify()
    assert not certificate.verify()
    with pytest.raises(ValueError, match="label-consistent"):
        _ = certificate.target_labels


def test_newly_legal_reveal_is_not_an_equal_legality_transport_certificate():
    obstruction = non_nested_rewiring_obstruction()
    certificate = TransportedTargetProjectionCertificate(
        obstruction.source,
        obstruction.target_system,
        obstruction.relation,
    )

    assert obstruction.verify()
    assert not certificate.verify()
    with pytest.raises(ValueError):
        _ = certificate.target_labels


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


def test_constructor_rejects_invalid_transport():
    obstruction = non_nested_rewiring_obstruction()

    with pytest.raises(ValueError, match="do not construct"):
        certify_transported_target_projection(
            obstruction.source,
            obstruction.target_system,
            obstruction.relation,
        )


def test_non_nested_certificates_are_exported_from_the_portability_facade():
    assert portability.non_nested_replacement_witness is non_nested_replacement_witness
    assert portability.transported_target_projection_witness is transported_target_projection_witness
    assert "TransportCoherentPortableMacroLawCertificate" in portability.__all__
    assert "TransportedTargetProjectionCertificate" in portability.__all__
    assert "certify_transported_target_projection" in portability.__all__
