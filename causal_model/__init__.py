"""RACH causal-invariant theorem and robust-admissibility modules."""

from .admissibility import (
    AdmissibilityReport,
    ClaimCoverage,
    CoverageMode,
    MotifClassification,
    MotifStatus,
    ProgramRun,
    RobustnessCell,
    classify_motifs,
)
from .benchmarks import (
    BenchmarkComparison,
    CalibrationOutcome,
    ExactCalibrationSummary,
    FiniteBenchmarkCell,
    calibrate_single_cell_exhaustively,
    compare_sample_to_known_truth,
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
    "ClaimCoverage",
    "CoverageMode",
    "MotifClassification",
    "MotifStatus",
    "ProgramRun",
    "RobustnessCell",
    "classify_motifs",
    "BenchmarkComparison",
    "CalibrationOutcome",
    "ExactCalibrationSummary",
    "FiniteBenchmarkCell",
    "calibrate_single_cell_exhaustively",
    "compare_sample_to_known_truth",
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
