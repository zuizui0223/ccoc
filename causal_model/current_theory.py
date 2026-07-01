"""Small public entrance to the current RACH theory core.

The repository contains older finite-program, observation-design, sequential,
and audit modules. They remain supported. The active mathematical core exposes
nine exact finite theorem families:

    finite candidate rule systems
    -> exact closure/recurrent certificates per candidate
    -> RACH-style consensus across retained candidates
    -> observer-independent / observer-coupled regime verdicts;

    fixed closed extension interfaces
    -> declared open-port interfaces
    -> exact extension--compression separation certificates;

    coordinate-level open-port witnesses
    -> constant-grammar, degree-three relay-tree protocols
    -> exact macro-time conjugacy certificates;

    finite passive observation windows
    -> exterior completion counterexamples
    -> counterfactual interface-inflation certificates;

    addressable exterior completion products
    -> separating-word lower bounds
    -> static finite boundary-blanket upper bounds;

    dynamic boundary blankets
    -> exact extension-stable macro interfaces
    -> finite counterfactual-horizon certificates;

    delayed addressability
    -> prefix-grammar constrained lower bounds
    -> no uniform closure horizon across expanding delayed families;

    candidate-safe universal laws
    -> ensemble--instance separation certificates
    -> deterministic universal, deterministic candidate-safe, or set-valued
       macro-law verdicts; and

    joint open-candidate laws
    -> common dynamic-interface and induced-map criterion
    -> joint exterior-memory plus response-type lower bounds under explicit
       structural separation.

This module intentionally re-exports only that core. It introduces no new
mathematics and does not replace the lower-level modules.
"""

from .addressable_completion_bounds import (
    AddressableCompletionProductCertificate,
    CanonicalAddressableProduct,
    FiniteBoundaryBlanketCertificate,
    PassiveClosureNonidentifiabilityCertificate,
    SeparatingWordCertificate,
    certify_addressable_completion_product,
    certify_finite_boundary_blanket,
    certify_passive_closure_nonidentifiability,
    separating_word_certificate,
)
from .candidate_safe_laws import (
    CandidateInducedLaw,
    CandidateLawFamily,
    CandidateResponseSeparationCertificate,
    CandidateSafeProductCertificate,
    DelayedCandidateDiscriminationCertificate,
    SetValuedMacroLawCertificate,
    UniversalLawObstructionCertificate,
    UniversalMacroLawCertificate,
    certify_candidate_safe_product,
    certify_delayed_candidate_discrimination,
    certify_set_valued_macro_law,
    certify_universal_macro_law,
    find_candidate_response_separator,
    universal_law_obstruction_certificate,
)
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
from .delayed_addressability import (
    DelayedAddressabilityCertificate,
    DelayedClosureNonidentifiabilityCertificate,
    DelayedReaderGrammar,
    DelayedRelayAttachmentCertificate,
    FinitePrefixGrammar,
    GrammarAwareControlledSystem,
    GrammarHorizonStabilizationCertificate,
    certify_delayed_addressability,
    certify_delayed_closure_nonidentifiability,
    certify_delayed_relay_attachment,
    certify_grammar_horizon_stabilization,
    delayed_separating_word_certificate,
)
from .dynamic_boundary_blankets import (
    DynamicBoundaryBlanketCertificate,
    DynamicInterfaceCertificate,
    FiniteControlledOutputSystem,
    FiniteHorizonStabilizationCertificate,
    UniformBlanketObstructionCertificate,
    certify_dynamic_boundary_blanket,
    certify_finite_horizon_stabilization,
    certify_uniform_blanket_obstruction,
)
from .extension_compression import (
    ExtensionCompressionCertificate,
    TraceSeparationCertificate,
    certify_extension_compression,
    exhaustive_witness_summary,
)
from .joint_open_candidate_laws import (
    CandidateSafeOpenLawCertificate,
    JointExteriorMechanismProductCertificate,
    JointOpenCandidateProduct,
    JointOpenLawObstructionCertificate,
    JointStructuralSeparationCertificate,
    OpenLawCandidate,
    OpenLawFamily,
    OpenLawReportKind,
    SetValuedOpenLawCertificate,
    StructuralQuery,
    TypedOpenLawVerdictCertificate,
    UniversalOpenLawCertificate,
    UniversalOpenLawObstructionCertificate,
    certify_candidate_safe_open_law,
    certify_joint_exterior_mechanism_product,
    certify_set_valued_open_law,
    certify_universal_open_law,
    classify_open_law_family,
    joint_open_law_obstruction_certificate,
    joint_structural_separator_certificate,
    universal_open_law_obstruction_certificate,
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
    "CandidateSafeOpenLawCertificate",
    "JointExteriorMechanismProductCertificate",
    "JointOpenCandidateProduct",
    "JointOpenLawObstructionCertificate",
    "JointStructuralSeparationCertificate",
    "OpenLawCandidate",
    "OpenLawFamily",
    "OpenLawReportKind",
    "SetValuedOpenLawCertificate",
    "StructuralQuery",
    "TypedOpenLawVerdictCertificate",
    "UniversalOpenLawCertificate",
    "UniversalOpenLawObstructionCertificate",
    "certify_candidate_safe_open_law",
    "certify_joint_exterior_mechanism_product",
    "certify_set_valued_open_law",
    "certify_universal_open_law",
    "classify_open_law_family",
    "joint_open_law_obstruction_certificate",
    "joint_structural_separator_certificate",
    "universal_open_law_obstruction_certificate",
    "CandidateInducedLaw",
    "CandidateLawFamily",
    "CandidateResponseSeparationCertificate",
    "CandidateSafeProductCertificate",
    "DelayedCandidateDiscriminationCertificate",
    "SetValuedMacroLawCertificate",
    "UniversalLawObstructionCertificate",
    "UniversalMacroLawCertificate",
    "certify_candidate_safe_product",
    "certify_delayed_candidate_discrimination",
    "certify_set_valued_macro_law",
    "certify_universal_macro_law",
    "find_candidate_response_separator",
    "universal_law_obstruction_certificate",
    "DelayedAddressabilityCertificate",
    "DelayedClosureNonidentifiabilityCertificate",
    "DelayedReaderGrammar",
    "DelayedRelayAttachmentCertificate",
    "FinitePrefixGrammar",
    "GrammarAwareControlledSystem",
    "GrammarHorizonStabilizationCertificate",
    "certify_delayed_addressability",
    "certify_delayed_closure_nonidentifiability",
    "certify_delayed_relay_attachment",
    "certify_grammar_horizon_stabilization",
    "delayed_separating_word_certificate",
    "DynamicBoundaryBlanketCertificate",
    "DynamicInterfaceCertificate",
    "FiniteControlledOutputSystem",
    "FiniteHorizonStabilizationCertificate",
    "UniformBlanketObstructionCertificate",
    "certify_dynamic_boundary_blanket",
    "certify_finite_horizon_stabilization",
    "certify_uniform_blanket_obstruction",
    "AddressableCompletionProductCertificate",
    "CanonicalAddressableProduct",
    "FiniteBoundaryBlanketCertificate",
    "PassiveClosureNonidentifiabilityCertificate",
    "SeparatingWordCertificate",
    "certify_addressable_completion_product",
    "certify_finite_boundary_blanket",
    "certify_passive_closure_nonidentifiability",
    "separating_word_certificate",
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
