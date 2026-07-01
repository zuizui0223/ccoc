"""Public entrance for RACH identifiability companion results.

These theorems ask what finite evidence or retained mechanism families can
justify.  They are intentionally separate from :mod:`portability_core`, which
asks when a macro-law structurally survives declared composition changes.

The facade re-exports existing certificates only; it introduces no mathematics.
"""

from .adaptive_closure_no_go import (
    ACTIONS,
    AdaptiveClosureNoGoCertificate,
    AdaptiveTranscript,
    CanonicalBlanketCardinalityCertificate,
    DelayGatedExteriorSystem,
    FiniteAdaptivePolicy,
    PolicyLiftingCertificate,
    certify_adaptive_closure_no_go,
    certify_canonical_blanket_cardinality,
    certify_policy_lifting,
    closed_open_delayed_pair,
)
from .delayed_addressability import (
    DelayedAddressabilityCertificate,
    DelayedClosureNonidentifiabilityCertificate,
    GrammarHorizonStabilizationCertificate,
    certify_delayed_addressability,
    certify_delayed_closure_nonidentifiability,
    certify_grammar_horizon_stabilization,
)
from .candidate_safe_laws import (
    CandidateInducedLaw,
    CandidateLawFamily,
    CandidateResponseSeparationCertificate,
    CandidateSafeProductCertificate,
    SetValuedMacroLawCertificate,
    UniversalLawObstructionCertificate,
    UniversalMacroLawCertificate,
    certify_candidate_safe_product,
    certify_set_valued_macro_law,
    certify_universal_macro_law,
    universal_law_obstruction_certificate,
)
from .joint_open_candidate_laws import (
    CandidateSafeOpenLawCertificate,
    JointExteriorMechanismProductCertificate,
    JointOpenLawObstructionCertificate,
    SetValuedOpenLawCertificate,
    UniversalOpenLawCertificate,
    certify_candidate_safe_open_law,
    certify_joint_exterior_mechanism_product,
    certify_set_valued_open_law,
    certify_universal_open_law,
)

__all__ = [
    # finite-adaptive evidence limitation
    "ACTIONS",
    "FiniteAdaptivePolicy",
    "AdaptiveTranscript",
    "DelayGatedExteriorSystem",
    "CanonicalBlanketCardinalityCertificate",
    "PolicyLiftingCertificate",
    "AdaptiveClosureNoGoCertificate",
    "closed_open_delayed_pair",
    "certify_canonical_blanket_cardinality",
    "certify_policy_lifting",
    "certify_adaptive_closure_no_go",
    # delayed horizon family
    "DelayedAddressabilityCertificate",
    "DelayedClosureNonidentifiabilityCertificate",
    "GrammarHorizonStabilizationCertificate",
    "certify_delayed_addressability",
    "certify_delayed_closure_nonidentifiability",
    "certify_grammar_horizon_stabilization",
    # retained mechanism families
    "CandidateInducedLaw",
    "CandidateLawFamily",
    "CandidateResponseSeparationCertificate",
    "CandidateSafeProductCertificate",
    "SetValuedMacroLawCertificate",
    "UniversalLawObstructionCertificate",
    "UniversalMacroLawCertificate",
    "certify_candidate_safe_product",
    "certify_set_valued_macro_law",
    "certify_universal_macro_law",
    "universal_law_obstruction_certificate",
    # joint exterior--mechanism companion
    "CandidateSafeOpenLawCertificate",
    "JointExteriorMechanismProductCertificate",
    "JointOpenLawObstructionCertificate",
    "SetValuedOpenLawCertificate",
    "UniversalOpenLawCertificate",
    "certify_candidate_safe_open_law",
    "certify_joint_exterior_mechanism_product",
    "certify_set_valued_open_law",
    "certify_universal_open_law",
]
