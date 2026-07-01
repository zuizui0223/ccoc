"""Regression tests for the logical public-package boundary."""

import causal_model.identifiability_companion as identifiability
import causal_model.portability_core as portability

from causal_model.conservative_macro_schema import certify_conservative_macro_schema
from causal_model.dynamic_boundary_blankets import certify_dynamic_boundary_blanket
from causal_model.extension_compression_noncommutation import certify_addressable_product_lower_bound
from causal_model.adaptive_closure_no_go import certify_adaptive_closure_no_go
from causal_model.candidate_safe_laws import certify_candidate_safe_product


def test_portability_core_exports_the_structural_ladder():
    assert portability.certify_dynamic_boundary_blanket is certify_dynamic_boundary_blanket
    assert portability.certify_addressable_product_lower_bound is certify_addressable_product_lower_bound
    assert portability.certify_conservative_macro_schema is certify_conservative_macro_schema

    required = {
        "certify_dynamic_boundary_blanket",
        "certify_grammar_aware_dynamic_blanket",
        "certify_addressable_product_lower_bound",
        "certify_closed_context_factorization",
        "certify_relay_tree_sharpness",
        "certify_uniform_dynamic_blanket_chain",
        "certify_coherent_portable_macro_law",
        "certify_conservative_macro_schema",
        "newly_legal_action_merge_obstruction",
    }
    assert required.issubset(portability.__all__)


def test_portability_core_excludes_companion_and_legacy_subjects():
    forbidden = {
        "certify_adaptive_closure_no_go",
        "certify_candidate_safe_product",
        "certify_joint_exterior_mechanism_product",
        "BudgetedResetPanel",
        "RobustCanonicalPanel",
        "CommonModeCanonicalPanel",
    }
    assert forbidden.isdisjoint(portability.__all__)


def test_identifiability_companion_exports_evidence_and_mechanism_questions():
    assert identifiability.certify_adaptive_closure_no_go is certify_adaptive_closure_no_go
    assert identifiability.certify_candidate_safe_product is certify_candidate_safe_product

    required = {
        "FiniteAdaptivePolicy",
        "certify_adaptive_closure_no_go",
        "certify_delayed_addressability",
        "certify_candidate_safe_product",
        "certify_joint_exterior_mechanism_product",
    }
    assert required.issubset(identifiability.__all__)


def test_identifiability_companion_does_not_claim_the_portability_ladder():
    forbidden = {
        "certify_conservative_macro_schema",
        "certify_coherent_portable_macro_law",
        "certify_uniform_dynamic_blanket_chain",
    }
    assert forbidden.isdisjoint(identifiability.__all__)
