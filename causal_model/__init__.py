"""CCOC package boundary.

Publication-core users should prefer::

    import causal_model.portability_core as rach

The package root intentionally does not re-export retired qualitative-program,
observation-panel, benchmark, failure-mode, or robust-panel APIs.

A small transitional compatibility surface remains for the deferred
symbolic/certificate/admission provenance cluster.  These re-exports are not a
research-surface claim and should disappear when that dependency graph is audited.
"""

from .admissibility import ClaimCoverage, CoverageMode, MotifStatus
from .anytime_confidence_lifting import (
    AnytimeJointCoverageCertificate,
    SequentialConfidenceSetSnapshot,
    anytime_soundness_guarantee_from_coverage,
    deterministic_anytime_lifting_witness,
)
from .confidence_lifting import (
    CandidateAcceptanceSet,
    CandidateMotifUniverse,
    ConfidenceSetCell,
    JointCoverageCertificate,
    deterministic_lifting_witness,
    indistinguishability_abstention_lower_bound,
    soundness_guarantee_from_joint_coverage,
)
from .symbolic_candidate_sets import (
    FeasibilityCertificate,
    FeasibilityStatus,
    SolverSemanticValidityCertificate,
    SymbolicCandidateSpace,
    SymbolicConfidenceSetCell,
    SymbolicJointCoverageCertificate,
    SymbolicMotifQueries,
    classify_symbolic_candidate_sets,
    symbolic_soundness_guarantee,
)

__all__ = [
    "ClaimCoverage",
    "CoverageMode",
    "MotifStatus",
    "AnytimeJointCoverageCertificate",
    "SequentialConfidenceSetSnapshot",
    "anytime_soundness_guarantee_from_coverage",
    "deterministic_anytime_lifting_witness",
    "CandidateAcceptanceSet",
    "CandidateMotifUniverse",
    "ConfidenceSetCell",
    "JointCoverageCertificate",
    "deterministic_lifting_witness",
    "indistinguishability_abstention_lower_bound",
    "soundness_guarantee_from_joint_coverage",
    "FeasibilityCertificate",
    "FeasibilityStatus",
    "SolverSemanticValidityCertificate",
    "SymbolicCandidateSpace",
    "SymbolicConfidenceSetCell",
    "SymbolicJointCoverageCertificate",
    "SymbolicMotifQueries",
    "classify_symbolic_candidate_sets",
    "symbolic_soundness_guarantee",
]
