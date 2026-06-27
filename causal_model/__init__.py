"""RACH causal-invariant theorem and robust-admissibility modules."""

from .admissibility import (
    AdmissibilityReport,
    MotifClassification,
    MotifStatus,
    ProgramRun,
    RobustnessCell,
    classify_motifs,
)
from .replaceability import (
    Observation,
    StructuralModel,
    admissible_configurations,
    is_last_driver_standing,
    null_eliminated_mechanisms,
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
    "Observation",
    "StructuralModel",
    "admissible_configurations",
    "is_last_driver_standing",
    "null_eliminated_mechanisms",
    "structural_crc",
    "theorem_a_certificate",
]
