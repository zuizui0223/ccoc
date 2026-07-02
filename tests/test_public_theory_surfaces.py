"""Regression tests for the publication-core public surface."""

import causal_model.portability_core as portability

from causal_model.conservative_macro_schema import certify_conservative_macro_schema
from causal_model.dynamic_boundary_blankets import certify_dynamic_boundary_blanket
from causal_model.extension_compression_noncommutation import certify_addressable_product_lower_bound


def test_portability_core_exports_only_the_manuscript_theorem_package():
    assert portability.certify_dynamic_boundary_blanket is certify_dynamic_boundary_blanket
    assert portability.certify_addressable_product_lower_bound is certify_addressable_product_lower_bound
    assert portability.certify_conservative_macro_schema is certify_conservative_macro_schema

    required = {
        # Exact interface.
        "certify_dynamic_boundary_blanket",
        "certify_grammar_aware_canonical_interface",
        "certify_grammar_aware_dynamic_blanket",
        # Main lower bound and concrete finite contract.
        "certify_addressable_product_lower_bound",
        "certify_closed_context_factorization",
        "certify_operational_addressable_product",
        "certify_operational_closed_context_factorization",
        # Sharpness witness.
        "certify_relay_tree_sharpness",
        "certify_bounded_degree_compilation",
        # Positive boundary and its local obstruction.
        "certify_coherent_portable_macro_law",
        "certify_conservative_macro_schema",
        "newly_legal_action_merge_obstruction",
    }
    assert required.issubset(portability.__all__)


def test_portability_core_excludes_archived_theorem_branches():
    archived = {
        # Finite closure prerequisite.
        "classify_closure",
        # Compositional variants not used by the paper.
        "certify_uniform_dynamic_blanket_chain",
        "certify_cumulative_addressability_chain",
        "certify_binary_relay_growth",
        # Non-nested replacement / rewiring.
        "certify_transport_coherent_portable_macro_law",
        "certify_transported_target_projection",
        "certify_conservative_transported_schema",
        "non_nested_replacement_witness",
        # Finite-evidence and candidate-law companions.
        "certify_adaptive_closure_no_go",
        "certify_candidate_safe_product",
        "certify_joint_exterior_mechanism_product",
        # Experimental design shelf.
        "BudgetedResetPanel",
        "RobustCanonicalPanel",
        "CommonModeCanonicalPanel",
    }
    assert archived.isdisjoint(portability.__all__)
