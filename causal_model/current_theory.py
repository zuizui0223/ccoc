"""Small public entrance to the current RACH theory core.

The repository contains older finite-program, observation-design, sequential,
and audit modules. They remain supported. The active mathematical core exposes
four exact finite theorem families:

    finite candidate rule systems
    -> exact closure/recurrent certificates per candidate
    -> RACH-style consensus across retained candidates
    -> observer-independent / observer-coupled regime verdicts;

    fixed closed extension interfaces
    -> declared open-port interfaces
    -> exact extension--compression separation certificates;

    coordinate-level open-port witnesses
    -> constant-grammar, degree-three relay-tree protocols
    -> exact macro-time conjugacy certificates; and

    finite passive observation windows
    -> exterior completion counterexamples
    -> counterfactual interface-inflation certificates.

This module intentionally re-exports only that core. It introduces no new
mathematics and does not replace the lower-level modules.
"""

from .causal_closure_calculus import (
    ClosureClassification,
    ClosureKind,
    FiniteDeterministicRuleSystem,
    GlobalClosureCertificate,
    MultistabilityCertificate,
    RecurrentCycleCertificate,
    classify_closure,
    verify_global_closure_certificate,
    verify_multistability_certificate,
    verify_recurrent_cycle_certificate,
)
from .extension_compression import (
    ExtensionCompressionCertificate,
    TraceSeparationCertificate,
    certify_extension_compression,
    exhaustive_witness_summary,
)
from .observation_regime_closure import (
    ObservationRegimeClassification,
    ObservationRegimeRulePair,
    ObservationRegimeVerdict,
    RegimeConsensus,
    RegimeConsensusKind,
    classify_observation_regime_pair,
    summarize_regime_candidates,
)
from .observation_window_completion import (
    CounterfactualCompletionCertificate,
    ObservationWindowCompletionCertificate,
    RelayCompletionCertificate,
    certify_observation_window_completion,
    completion_counterexample_certificate,
    exhaustive_observation_window_summary,
    relay_completion_certificate,
)
from .relay_tree_compilation import (
    BoundedDegreeCompilationCertificate,
    OneTokenRelayGrammar,
    RelayProtocolCertificate,
    RelayTreeTopology,
    certify_bounded_degree_compilation,
    certify_relay_protocol,
    exhaustive_compilation_summary,
)

__all__ = [
    "ClosureClassification",
    "ClosureKind",
    "FiniteDeterministicRuleSystem",
    "GlobalClosureCertificate",
    "MultistabilityCertificate",
    "RecurrentCycleCertificate",
    "classify_closure",
    "verify_global_closure_certificate",
    "verify_multistability_certificate",
    "verify_recurrent_cycle_certificate",
    "ExtensionCompressionCertificate",
    "TraceSeparationCertificate",
    "certify_extension_compression",
    "exhaustive_witness_summary",
    "BoundedDegreeCompilationCertificate",
    "OneTokenRelayGrammar",
    "RelayProtocolCertificate",
    "RelayTreeTopology",
    "certify_bounded_degree_compilation",
    "certify_relay_protocol",
    "exhaustive_compilation_summary",
    "CounterfactualCompletionCertificate",
    "ObservationWindowCompletionCertificate",
    "RelayCompletionCertificate",
    "certify_observation_window_completion",
    "completion_counterexample_certificate",
    "exhaustive_observation_window_summary",
    "relay_completion_certificate",
    "ObservationRegimeClassification",
    "ObservationRegimeRulePair",
    "ObservationRegimeVerdict",
    "RegimeConsensus",
    "RegimeConsensusKind",
    "classify_observation_regime_pair",
    "summarize_regime_candidates",
]
