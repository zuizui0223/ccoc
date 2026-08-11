"""Public facade for the RACH/CCOC open-composition theorem core.

This module exposes the finite theorem package used by the first paper together
with post-reopening theorem strengthenings that directly modify the canonical
portability claims:

1. exact grammar-aware dynamic interfaces;
2. operational addressability / extension--compression lower bounds;
3. bounded-degree relay sharpness constructions; and
4. conservative macro schemas plus local fiber-split obstructions.

Finite closure classification, non-nested replacement transport, candidate
uncertainty, delayed-evidence limits, and experimental-design branches remain
separate compatibility or companion material.
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
from .addressable_codebooks import (
    CanonicalOperationalCodebook,
    OperationalAddressableCodebookCertificate,
    OperationalCodebookClosedContextCertificate,
    build_canonical_operational_codebook,
    certify_canonical_operational_codebook,
    certify_operational_addressable_codebook,
    certify_operational_codebook_closed_context_factorization,
    even_parity_codebook,
    first_differing_codebook_coordinate,
    readout_symbol,
    standard_codebook_closed_projection,
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
    # V1 product addressability obstruction and open/closed comparison.
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
    # Post-reopening arbitrary-codebook strengthening.
    "OperationalAddressableCodebookCertificate",
    "OperationalCodebookClosedContextCertificate",
    "certify_operational_addressable_codebook",
    "certify_operational_codebook_closed_context_factorization",
    "CanonicalOperationalCodebook",
    "build_canonical_operational_codebook",
    "certify_canonical_operational_codebook",
    "readout_symbol",
    "standard_codebook_closed_projection",
    "first_differing_codebook_coordinate",
    "even_parity_codebook",
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
