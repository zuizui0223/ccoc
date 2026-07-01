import pytest

from causal_model.conservative_macro_schema import (
    ConservativeMacroSchema,
    ConservativeSchemaChainCertificate,
    ConservativeStageProjection,
    certify_conservative_macro_schema,
    conservative_reveal_chain,
    newly_legal_action_merge_obstruction,
)
from causal_model.coherent_portable_macrolaw import TrajectoryEmbedding
from causal_model.delayed_addressability import FinitePrefixGrammar, GrammarAwareControlledSystem
from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem


def test_newly_legal_action_can_be_added_conservatively_without_changing_old_macro_meaning():
    certificate = conservative_reveal_chain()
    assert certificate.verify()
    assert certificate.schema.state_count == 2
    old_rows = certificate.stages[0].stage_rows()
    new_rows = certificate.stages[1].stage_rows()
    assert old_rows == ((0, None), (1, None))
    assert new_rows == ((0, 1), (1, 1))
    assert certificate.schema.transition_rows == ((0, 1), (1, 1))
    assert certificate.embeddings[0].verify(equal_legal_actions=False)


def test_old_action_meanings_cannot_change_after_grammar_expansion():
    actions = ("stay", "reveal")
    schema = ConservativeMacroSchema(actions, (0, 1), ((0, 1), (1, 1)))
    old_system = FiniteControlledOutputSystem(actions, ((0, 1), (1, 1)), (0, 1))
    old_grammar = FinitePrefixGrammar(actions, ((0, None),))
    old = ConservativeStageProjection(GrammarAwareControlledSystem(old_system, old_grammar), (0, 1))
    changed_system = FiniteControlledOutputSystem(actions, ((1, 1), (1, 1)), (0, 1))
    new_grammar = FinitePrefixGrammar(actions, ((0, 0),))
    changed = ConservativeStageProjection(GrammarAwareControlledSystem(changed_system, new_grammar), (0, 1))
    embedding = TrajectoryEmbedding(old.constrained_system, changed.constrained_system, (0, 1))
    assert not embedding.verify(equal_legal_actions=False)
    with pytest.raises(ValueError, match="conservative portable"):
        certify_conservative_macro_schema(schema, (old, changed), (embedding,))


def test_newly_legal_action_that_splits_one_proposed_fiber_is_a_concrete_obstruction():
    certificate = newly_legal_action_merge_obstruction()
    assert certificate.verify()
    assert certificate.newly_legal_action == "reveal"
    assert certificate.proposed_labels[certificate.left_index] == certificate.proposed_labels[certificate.right_index]


def test_stage_must_realize_the_schema_successor_when_an_action_is_legal():
    actions = ("a",)
    schema = ConservativeMacroSchema(actions, (0, 1), ((1,), (1,)))
    system = FiniteControlledOutputSystem(actions, ((0,), (1,)), (0, 1))
    grammar = FinitePrefixGrammar(actions, ((0,),))
    stage = ConservativeStageProjection(GrammarAwareControlledSystem(system, grammar), (0, 1))
    with pytest.raises(ValueError, match="conservative portable"):
        certify_conservative_macro_schema(schema, (stage,), ())


def test_schema_and_labels_fail_closed_on_invalid_inputs():
    assert not ConservativeMacroSchema(("a",), (0,), ((2,),)).verify()
    with pytest.raises(ValueError, match="labels"):
        ConservativeStageProjection(
            GrammarAwareControlledSystem(
                FiniteControlledOutputSystem(("a",), ((0,),), (0,)),
                FinitePrefixGrammar(("a",), ((0,),)),
            ),
            (),
        ).verify()
    assert not ConservativeSchemaChainCertificate(
        ConservativeMacroSchema(("a",), (0,), ((0,),)), (), ()
    ).verify()
