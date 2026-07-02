"""Regression tests for the shared finite grammar contract surface."""

from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.grammar_aware_blankets import certify_grammar_aware_canonical_interface
from causal_model.portability_core import FinitePrefixGrammar as CoreGrammar
from causal_model.portability_core import GrammarAwareControlledSystem as CoreConstrainedSystem
from causal_model.shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem


def test_portability_core_uses_the_shared_grammar_primitives():
    assert CoreGrammar is FinitePrefixGrammar
    assert CoreConstrainedSystem is GrammarAwareControlledSystem


def test_shared_grammar_supports_the_core_grammar_aware_interface():
    system = FiniteControlledOutputSystem(
        actions=("step",),
        transition_table=((1,), (0,)),
        outputs=(0, 1),
    )
    grammar = FinitePrefixGrammar(
        actions=("step",),
        transition_table=((0,),),
    )
    constrained = GrammarAwareControlledSystem(system=system, grammar=grammar)

    certificate = certify_grammar_aware_canonical_interface(constrained)

    assert certificate.verify()
    assert certificate.canonical_block_count == 2
