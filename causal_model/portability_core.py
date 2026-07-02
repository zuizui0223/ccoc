"""Public entrance for RACH portability core.

This facade exposes only the structural theorem family:

1. exact finite grammar-aware dynamic factorization;
2. the addressable-completion / extension--compression lower bound; and
3. portable macro-laws under nested conservative growth or declared non-nested
   replacement transport.

Relay constructions are retained as sharpness witnesses. Delayed evidence and
candidate-mechanism uncertainty live in :mod:`identifiability_companion`.
Legacy experiment-design APIs remain in their original modules.

Shared grammar primitives are imported from :mod:`shared_grammar`, not from an
identifiability module. The facade re-exports existing certificates only; it
introduces no mathematics.
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
from .shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem
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
from .operational_addressability import (
    CanonicalOperationalProduct,
    OperationalAddressableProductCertificate,
    OperationalClosedContextFactorizationCertificate,
    build_canonical_operational_product,
    certify_canonical_operational_product,
    certify_operational_addressable_product,
    certify_operational_closed_context_factorization,
    readout_value,
    standard_closed_projection,
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
from .non_nested_portability import (
    ReplacementFiberSplitObstructionCertificate,
    ReplacementTransport,
    TransportCoherentPortableMacroLawCertificate,
    certify_transport_coherent_portable_macro_law,
    non_nested_replacement_witness,
    non_nested_rewiring_obstruction,
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
    # addressability obstruction: analytic theorem and operational applications
    "AddressableProductLowerBoundCertificate",
    "ClosedContextFactorizationCertificate",
    "certify_addressable_product_lower_bound",
    "certify_closed_context_factorization",
    "OperationalAddressableProductCertificate",
    "OperationalClosedContextFactorizationCertificate",
    "certify_operational_addressable_product",
    "certify_operational_closed_context_factorization",
    "CanonicalOperationalProduct",
    "build_canonical_operational_product",
    "certify_canonical_operational_product",
    "readout_value",
    "standard_closed_projection",
    # sharpness witness
    "RelayTreeSharpnessCertificate",
    "certify_relay_tree_sharpness",
    "BoundedDegreeCompilationCertificate",
    "RelayProtocolCertificate",
    "RelayTreeTopology",
    "certify_bounded_degree_compilation",
    # nested composition portability ladder
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
    # non-nested replacement and rewiring portability
    "ReplacementTransport",
    "TransportCoherentPortableMacroLawCertificate",
    "certify_transport_coherent_portable_macro_law",
    "non_nested_replacement_witness",
    "ReplacementFiberSplitObstructionCertificate",
    "non_nested_rewiring_obstruction",
    # conservative legal-action expansion
    "ConservativeMacroSchema",
    "ConservativeStageProjection",
    "ConservativeSchemaChainCertificate",
    "NewActionMergeObstructionCertificate",
    "certify_conservative_macro_schema",
    "conservative_reveal_chain",
    "newly_legal_action_merge_obstruction",
]
