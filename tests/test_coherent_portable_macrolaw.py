import pytest

from causal_model.coherent_portable_macrolaw import (
    CoherentPortableMacroLawCertificate,
    PortableMacroDynamics,
    StageEmbedding,
    StageMacroProjection,
    certify_coherent_portable_macro_law,
    inert_portable_chain,
    newly_legal_word_obstruction,
)
from causal_model.delayed_addressability import FinitePrefixGrammar, GrammarAwareControlledSystem
from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem


@pytest.mark.parametrize("maximum_module_count", [1, 2, 3, 5])
def test_growing_inert_composition_has_one_unchanged_portable_macro_law(maximum_module_count):
    certificate = inert_portable_chain(maximum_module_count)
    assert certificate.verify()
    assert certificate.macro.state_count == 1
    assert certificate.macro.outputs == ("inert-window",)
    assert [stage.constrained_system.system.state_count for stage in certificate.stages] == [
        2**m for m in range(1, maximum_module_count + 1)
    ]
    assert len(certificate.embeddings) == maximum_module_count - 1


def test_embeddings_preserve_both_old_trajectories_and_macro_labels():
    certificate = inert_portable_chain(3)
    assert certificate.verify()
    for embedding in certificate.embeddings:
        assert embedding.verify()
        for source_index, target_index in enumerate(embedding.target_indices):
            assert embedding.source.summary_labels[source_index] == embedding.target.summary_labels[target_index]


def test_newly_legal_word_gives_a_concrete_obstruction_to_a_proposed_portable_merge():
    certificate = newly_legal_word_obstruction()
    assert certificate.verify()
    assert certificate.future_word == ("reveal",)
    assert certificate.source_labels[certificate.left_source_index] == certificate.source_labels[certificate.right_source_index]
    left_target = certificate.trajectory_embedding.target_indices[certificate.left_source_index]
    right_target = certificate.trajectory_embedding.target_indices[certificate.right_source_index]
    assert certificate.target_labels[left_target] == certificate.target_labels[right_target]


def test_same_summary_alphabet_without_common_macro_transition_is_rejected():
    actions = ("a",)
    grammar = FinitePrefixGrammar(actions, ((0,),))
    system = FiniteControlledOutputSystem(actions, ((0,),), ("x",))
    stage = StageMacroProjection(GrammarAwareControlledSystem(system, grammar), (0,))
    wrong_macro = PortableMacroDynamics(actions, ("other",), (("a",),), ((0,),))
    with pytest.raises(ValueError, match="coherent portable"):
        certify_coherent_portable_macro_law(wrong_macro, (stage,), ())


def test_noncoherent_embedding_is_rejected_even_when_each_stage_is_exact():
    actions = ("a",)
    grammar = FinitePrefixGrammar(actions, ((0,),))
    source_system = FiniteControlledOutputSystem(actions, ((0,),), (0,))
    target_system = FiniteControlledOutputSystem(actions, ((1,), (1,)), (0, 0))
    source = StageMacroProjection(GrammarAwareControlledSystem(source_system, grammar), (0,))
    target = StageMacroProjection(GrammarAwareControlledSystem(target_system, grammar), (0, 0))
    macro = source.induced_macro()
    bad_embedding = StageEmbedding(source, target, (0,))
    assert not bad_embedding.verify()
    certificate = CoherentPortableMacroLawCertificate(macro, (source, target), (bad_embedding,))
    assert not certificate.verify()


def test_invalid_chain_input_fails_closed():
    with pytest.raises(ValueError, match="positive"):
        inert_portable_chain(0)
