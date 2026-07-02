"""Public facade for the RACH open-composition manuscript core.

This module exposes only the finite theorem package used by the current paper:

1. exact grammar-aware dynamic interfaces;
2. the operational-addressability / extension--compression lower bound;
3. the bounded-degree relay sharpness construction; and
4. conservative macro schemas plus local fiber-split obstructions.

Finite closure classification, non-nested replacement transport, candidate
uncertainty, delayed-evidence limits, and experimental-design branches are
preserved in :mod:`legacy` as compatibility material. They are deliberately not
re-exported here, because they are not premises or conclusions of the manuscript.
"""

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
    GrammarAwareRefinementCertificate,
    certify_grammar_aware_canonical_interface,
    certify_grammar_aware_dynamic_blanket,
    certify_grammar_aware_refinement,
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
    # Exact grammar-aware interface.
    "FiniteControlledOutputSystem",
    "FinitePrefixGrammar",
    "GrammarAwareControlledSystem",
    "DynamicBoundaryBlanketCertificate",
    "DynamicInterfaceCertificate",
    "GrammarAwareCanonicalInterfaceCertificate",
    "GrammarAwareDynamicBlanketCertificate",
    "GrammarAwareDynamicInterfaceCertificate",
    "GrammarAwareRefinementCertificate",
    "certify_dynamic_boundary_blanket",
    "certify_grammar_aware_canonical_interface",
    "certify_grammar_aware_dynamic_blanket",
    "certify_grammar_aware_refinement",
    # Addressability obstruction and open/closed comparison.
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
    # Bounded-locality sharpness witness.
    "RelayTreeSharpnessCertificate",
    "certify_relay_tree_sharpness",
    "BoundedDegreeCompilationCertificate",
    "RelayProtocolCertificate",
    "RelayTreeTopology",
    "certify_bounded_degree_compilation",
    # Positive conservative boundary and local obstruction.
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
