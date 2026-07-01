"""Public entrance for RACH portability core v1.

This facade exposes only the structural theorem family:

1. exact finite grammar-aware dynamic factorization;
2. the addressable-completion / extension--compression lower bound; and
3. bounded, coherent, and conservative portability under nested composition.

Relay constructions are retained as sharpness witnesses.  Delayed evidence and
candidate-mechanism uncertainty live in :mod:`identifiability_companion`.
Legacy experiment-design APIs remain in their original modules.

The facade re-exports existing certificates only; it introduces no mathematics.
"""

from .causal_closure_calculus import (
    ClosureClassification,
    ClosureKind,
    FiniteDeterministicRuleSystem,
    GlobalClosureCertificate,
    MultistabilityCertificate,
    RecurrentCycleCertificate,
    classify_closure,
)
from .dynamic_boundary_blankets import (
    DynamicBoundaryBlanketCertificate,
    DynamicInterfaceCertificate,
    FiniteControlledOutputSystem,
    certify_dynamic_boundary_blanket,
)
from .delayed_addressability import FinitePrefixGrammar, GrammarAwareControlledSystem
from .grammar_aware_blankets import (
    GrammarAwareCanonicalInterfaceCertificate,
    GrammarAwareDynamicBlanketCertificate,
    GrammarAwareDynamicInterfaceCertificate,
    certify_grammar_aware_canonical_interface,
    certify_grammar_aware_dynamic_blanket,
)
from .extension_compression_noncommutation import (
    AddressableProductLowerBoundCertificate,
    ClosedContextFactorizationCertificate,
    RelayTreeSharpnessCertificate,
    certify_addressable_product_lower_bound,
    certify_closed_context_factorization,
    certify_relay_tree_sharpness,
)
from .relay_tree_compilation import (
    BoundedDegreeCompilationCertificate,
    RelayProtocolCertificate,
    RelayTreeTopology,
    certify_bounded_degree_compilation,
)
from .compositional_boundedness import (
    BinaryRelayGrowthCertificate,
    CumulativeAddressabilityChainCertificate,
    UniformDynamicBlanketChainCertificate,
    UniformFactorizationStage,
    certify_binary_relay_growth,
    certify_cumulative_addressability_chain,
    certify_inert_attachment_boundedness,
    certify_uniform_dynamic_blanket_chain,
)
from .coherent_portable_macrolaw import (
    CoherentPortableMacroLawCertificate,
    FutureWordObstructionCertificate,
    PortableMacroDynamics,
    StageEmbedding,
    StageMacroProjection,
    TrajectoryEmbedding,
    certify_coherent_portable_macro_law,
    inert_portable_chain,
    newly_legal_word_obstruction,
)
from .conservative_macro_schema import (
    ConservativeMacroSchema,
    ConservativeSchemaChainCertificate,
    ConservativeStageProjection,
    NewActionMergeObstructionCertificate,
    certify_conservative_macro_schema,
    conservative_reveal_chain,
    newly_legal_action_merge_obstruction,
)

__all__ = [
    # finite-model prerequisite
    "ClosureClassification",
    "ClosureKind",
    "FiniteDeterministicRuleSystem",
    "GlobalClosureCertificate",
    "MultistabilityCertificate",
    "RecurrentCycleCertificate",
    "classify_closure",
    # exact factorization
    "FiniteControlledOutputSystem",
    "FinitePrefixGrammar",
    "GrammarAwareControlledSystem",
    "DynamicBoundaryBlanketCertificate",
    "DynamicInterfaceCertificate",
    "GrammarAwareCanonicalInterfaceCertificate",
    "GrammarAwareDynamicBlanketCertificate",
    "GrammarAwareDynamicInterfaceCertificate",
    "certify_dynamic_boundary_blanket",
    "certify_grammar_aware_canonical_interface",
    "certify_grammar_aware_dynamic_blanket",
    # addressability obstruction and sharpness witness
    "AddressableProductLowerBoundCertificate",
    "ClosedContextFactorizationCertificate",
    "RelayTreeSharpnessCertificate",
    "certify_addressable_product_lower_bound",
    "certify_closed_context_factorization",
    "certify_relay_tree_sharpness",
    "BoundedDegreeCompilationCertificate",
    "RelayProtocolCertificate",
    "RelayTreeTopology",
    "certify_bounded_degree_compilation",
    # composition portability ladder
    "UniformFactorizationStage",
    "UniformDynamicBlanketChainCertificate",
    "CumulativeAddressabilityChainCertificate",
    "BinaryRelayGrowthCertificate",
    "certify_uniform_dynamic_blanket_chain",
    "certify_inert_attachment_boundedness",
    "certify_cumulative_addressability_chain",
    "certify_binary_relay_growth",
    "PortableMacroDynamics",
    "StageMacroProjection",
    "StageEmbedding",
    "TrajectoryEmbedding",
    "CoherentPortableMacroLawCertificate",
    "FutureWordObstructionCertificate",
    "certify_coherent_portable_macro_law",
    "inert_portable_chain",
    "newly_legal_word_obstruction",
    "ConservativeMacroSchema",
    "ConservativeStageProjection",
    "ConservativeSchemaChainCertificate",
    "NewActionMergeObstructionCertificate",
    "certify_conservative_macro_schema",
    "conservative_reveal_chain",
    "newly_legal_action_merge_obstruction",
]
