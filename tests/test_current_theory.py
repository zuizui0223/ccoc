"""Regression tests for the deliberately small current-theory import surface."""

import causal_model.current_theory as current
from causal_model.addressable_completion_bounds import certify_addressable_completion_product
from causal_model.candidate_safe_laws import certify_candidate_safe_product
from causal_model.causal_closure_calculus import classify_closure
from causal_model.delayed_addressability import certify_delayed_addressability
from causal_model.dynamic_boundary_blankets import certify_dynamic_boundary_blanket
from causal_model.joint_open_candidate_laws import certify_joint_exterior_mechanism_product
from causal_model.observation_regime_closure import summarize_regime_candidates
from causal_model.observation_window_completion import certify_observation_window_completion


def test_current_theory_facade_reexports_the_active_certificate_core():
    assert current.classify_closure is classify_closure
    assert current.summarize_regime_candidates is summarize_regime_candidates
    assert current.certify_observation_window_completion is certify_observation_window_completion
    assert current.certify_addressable_completion_product is certify_addressable_completion_product
    assert current.certify_dynamic_boundary_blanket is certify_dynamic_boundary_blanket
    assert current.certify_delayed_addressability is certify_delayed_addressability
    assert current.certify_candidate_safe_product is certify_candidate_safe_product
    assert current.certify_joint_exterior_mechanism_product is certify_joint_exterior_mechanism_product
    assert "FiniteDeterministicRuleSystem" in current.__all__
    assert "ObservationRegimeRulePair" in current.__all__
    assert "ObservationWindowCompletionCertificate" in current.__all__
    assert "AddressableCompletionProductCertificate" in current.__all__
    assert "DynamicBoundaryBlanketCertificate" in current.__all__
    assert "DelayedAddressabilityCertificate" in current.__all__
    assert "CandidateSafeProductCertificate" in current.__all__
    assert "JointExteriorMechanismProductCertificate" in current.__all__

    # The facade should not turn audit/provenance plumbing into theory-core API.
    forbidden = {"SignedTranscriptCheckpoint", "AdmissionTranscript", "TieredCertificateManifest"}
    assert forbidden.isdisjoint(current.__all__)
