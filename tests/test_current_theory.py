"""Regression tests for the deliberately small current-theory import surface."""

import causal_model.current_theory as current
from causal_model.causal_closure_calculus import classify_closure
from causal_model.observation_regime_closure import summarize_regime_candidates


def test_current_theory_facade_reexports_only_closure_and_regime_core_symbols():
    assert current.classify_closure is classify_closure
    assert current.summarize_regime_candidates is summarize_regime_candidates
    assert "FiniteDeterministicRuleSystem" in current.__all__
    assert "ObservationRegimeRulePair" in current.__all__

    # The facade should not turn audit/provenance plumbing into theory-core API.
    forbidden = {"SignedTranscriptCheckpoint", "AdmissionTranscript", "TieredCertificateManifest"}
    assert forbidden.isdisjoint(current.__all__)
