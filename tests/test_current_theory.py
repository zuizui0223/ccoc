"""Regression tests for the historical ``current_theory`` compatibility facade."""

import importlib
import sys

import pytest

from causal_model.addressable_completion_bounds import certify_addressable_completion_product
from causal_model.candidate_safe_laws import certify_candidate_safe_product
from causal_model.causal_closure_calculus import classify_closure
from causal_model.delayed_addressability import certify_delayed_addressability
from causal_model.dynamic_boundary_blankets import certify_dynamic_boundary_blanket
from causal_model.grammar_aware_blankets import certify_grammar_aware_dynamic_blanket
from causal_model.joint_open_candidate_laws import certify_joint_exterior_mechanism_product
from causal_model.observation_regime_closure import summarize_regime_candidates
from causal_model.observation_window_completion import certify_observation_window_completion


def _import_historical_facade():
    sys.modules.pop("causal_model.current_theory", None)
    with pytest.warns(DeprecationWarning, match="historical compatibility aggregate"):
        return importlib.import_module("causal_model.current_theory")


def test_current_theory_is_deprecated_but_preserves_historical_certificate_exports():
    current = _import_historical_facade()

    assert current.classify_closure is classify_closure
    assert current.summarize_regime_candidates is summarize_regime_candidates
    assert current.certify_observation_window_completion is certify_observation_window_completion
    assert current.certify_addressable_completion_product is certify_addressable_completion_product
    assert current.certify_dynamic_boundary_blanket is certify_dynamic_boundary_blanket
    assert current.certify_delayed_addressability is certify_delayed_addressability
    assert current.certify_candidate_safe_product is certify_candidate_safe_product
    assert current.certify_joint_exterior_mechanism_product is certify_joint_exterior_mechanism_product
    assert current.certify_grammar_aware_dynamic_blanket is certify_grammar_aware_dynamic_blanket

    historical_exports = {
        "FiniteDeterministicRuleSystem",
        "ObservationRegimeRulePair",
        "ObservationWindowCompletionCertificate",
        "AddressableCompletionProductCertificate",
        "DynamicBoundaryBlanketCertificate",
        "DelayedAddressabilityCertificate",
        "CandidateSafeProductCertificate",
        "JointExteriorMechanismProductCertificate",
        "GrammarAwareDynamicBlanketCertificate",
    }
    assert historical_exports.issubset(current.__all__)

    # It must not turn audit/provenance plumbing into a theorem-facing API.
    forbidden = {"SignedTranscriptCheckpoint", "AdmissionTranscript", "TieredCertificateManifest"}
    assert forbidden.isdisjoint(current.__all__)


def test_new_public_research_surfaces_are_the_two_narrow_facades():
    import causal_model.identifiability_companion as identifiability
    import causal_model.portability_core as portability

    assert "certify_operational_addressable_product" in portability.__all__
    assert "certify_adaptive_closure_no_go" in identifiability.__all__
    assert "certify_adaptive_closure_no_go" not in portability.__all__
    assert "certify_conservative_macro_schema" not in identifiability.__all__
