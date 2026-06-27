"""RACH causal-invariant theorem and robust-admissibility modules."""

from .admissibility import (
    AdmissibilityReport,
    MotifClassification,
    MotifStatus,
    ProgramRun,
    RobustnessCell,
    classify_motifs,
)
from .observation_design import (
    MinimumPanel,
    NullObservationCandidate,
    minimum_discriminating_panel,
)
from .replaceability import (
    Observation,
    StructuralModel,
    admissible_configurations,
    forced_on_by_theorem,
    is_last_driver_standing,
    null_eliminated_mechanisms,
    observation_is_admissible,
    structural_crc,
    theorem_a_certificate,
)

__all__ = [
    "AdmissibilityReport",
    "MotifClassification",
    "MotifStatus",
    "ProgramRun",
    "RobustnessCell",
    "classify_motifs",
    "MinimumPanel",
    "NullObservationCandidate",
    "minimum_discriminating_panel",
    "Observation",
    "StructuralModel",
    "admissible_configurations",
    "forced_on_by_theorem",
    "is_last_driver_standing",
    "null_eliminated_mechanisms",
    "observation_is_admissible",
    "structural_crc",
    "theorem_a_certificate",
]
