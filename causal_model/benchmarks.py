"""Known-truth finite benchmarks for robust-admissibility error calibration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from math import comb
from typing import Iterable, Mapping

from .admissibility import (
    AdmissibilityReport,
    CoverageMode,
    MotifStatus,
    ProgramRun,
    RobustnessCell,
    classify_motifs,
)


class CalibrationOutcome(str, Enum):
    """Comparison of a sampled classification with a complete finite truth."""

    MATCH = "match"
    FALSE_INVARIANT = "false_invariant"
    FALSE_EXCLUDED = "false_excluded"
    CONSERVATIVE_UNRESOLVED = "conservative_unresolved"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class FiniteBenchmarkCell:
    """A finite, fully enumerated program universe with known acceptance labels."""

    cell_id: str
    description: str
    full_runs: tuple[ProgramRun, ...]
    required: bool = True

    def __post_init__(self) -> None:
        if not self.cell_id:
            raise ValueError("cell_id must be non-empty")
        if not self.full_runs:
            raise ValueError("a finite benchmark cell must contain at least one run")
        if any(run.cell_id != self.cell_id for run in self.full_runs):
            raise ValueError("every full run must carry the benchmark cell_id")
        run_ids = [run.run_id for run in self.full_runs]
        if len(set(run_ids)) != len(run_ids):
            raise ValueError("full-run IDs must be unique within a benchmark cell")

    def exhaustive_cell(self) -> RobustnessCell:
        """Return the complete analysis cell used as finite known truth."""
        return RobustnessCell(
            cell_id=self.cell_id,
            description=self.description,
            runs=self.full_runs,
            required=self.required,
            coverage_mode=CoverageMode.EXHAUSTIVE,
        )

    def sampled_cell(self, run_indices: Iterable[int]) -> RobustnessCell:
        """Return a sampled analysis cell using explicit indices into ``full_runs``."""
        indices = tuple(run_indices)
        if len(set(indices)) != len(indices):
            raise ValueError("sampled run indices must be unique")
        if any(index < 0 or index >= len(self.full_runs) for index in indices):
            raise ValueError("sampled run index is out of range")
        return RobustnessCell(
            cell_id=self.cell_id,
            description=self.description,
            runs=tuple(self.full_runs[index] for index in indices),
            required=self.required,
            coverage_mode=CoverageMode.SAMPLED,
        )


@dataclass(frozen=True)
class BenchmarkComparison:
    """Complete finite truth, one sampled estimate, and motif-wise outcomes."""

    truth: AdmissibilityReport
    sampled: AdmissibilityReport
    outcomes: Mapping[str, CalibrationOutcome]


@dataclass(frozen=True)
class ExactCalibrationSummary:
    """Outcome counts over every equal-size sample from one finite benchmark cell."""

    sample_size: int
    total_panels: int
    truth: AdmissibilityReport
    outcome_counts: Mapping[str, Mapping[CalibrationOutcome, int]]

    def rate(self, motif: str, outcome: CalibrationOutcome) -> float:
        """Return the exact fraction of panels with one motif-wise outcome."""
        return self.outcome_counts[motif].get(outcome, 0) / self.total_panels


def _outcome(sampled: MotifStatus, truth: MotifStatus) -> CalibrationOutcome:
    if sampled is MotifStatus.UNSUPPORTED:
        return CalibrationOutcome.UNSUPPORTED
    if sampled is truth:
        return CalibrationOutcome.MATCH
    if sampled is MotifStatus.INVARIANT:
        return CalibrationOutcome.FALSE_INVARIANT
    if sampled is MotifStatus.EXCLUDED:
        return CalibrationOutcome.FALSE_EXCLUDED
    return CalibrationOutcome.CONSERVATIVE_UNRESOLVED


def compare_sample_to_known_truth(
    motifs: Iterable[str],
    benchmark_cells: Iterable[FiniteBenchmarkCell],
    sampled_indices: Mapping[str, Iterable[int]],
) -> BenchmarkComparison:
    """Classify selected samples and compare them with complete finite truth.

    Every declared benchmark cell must have an entry in ``sampled_indices``. The
    complete report uses the full finite universe with `EXHAUSTIVE` coverage; the
    sampled report deliberately uses `SAMPLED` coverage.
    """
    motif_tuple = tuple(motifs)
    cells = tuple(benchmark_cells)
    if not cells:
        raise ValueError("at least one finite benchmark cell is required")
    ids = [cell.cell_id for cell in cells]
    if len(set(ids)) != len(ids):
        raise ValueError("benchmark cell IDs must be unique")
    if set(sampled_indices) != set(ids):
        raise ValueError("sampled_indices must contain exactly the benchmark cell IDs")

    truth = classify_motifs(motif_tuple, (cell.exhaustive_cell() for cell in cells))
    sampled = classify_motifs(
        motif_tuple,
        (cell.sampled_cell(sampled_indices[cell.cell_id]) for cell in cells),
    )
    outcomes = {
        motif: _outcome(
            sampled.classifications[motif].status,
            truth.classifications[motif].status,
        )
        for motif in motif_tuple
    }
    return BenchmarkComparison(truth=truth, sampled=sampled, outcomes=outcomes)


def calibrate_single_cell_exhaustively(
    motifs: Iterable[str],
    benchmark_cell: FiniteBenchmarkCell,
    *,
    sample_size: int,
    max_panels: int = 100_000,
) -> ExactCalibrationSummary:
    """Enumerate all equal-size samples and count classification error outcomes.

    This is an exact finite calibration tool for deliberately small known-truth
    benchmarks. `max_panels` prevents accidental combinatorial explosion.
    """
    motif_tuple = tuple(motifs)
    total_runs = len(benchmark_cell.full_runs)
    if not 1 <= sample_size <= total_runs:
        raise ValueError("sample_size must lie between one and the number of full runs")
    total_panels = comb(total_runs, sample_size)
    if total_panels > max_panels:
        raise ValueError("number of sample panels exceeds max_panels")

    truth = classify_motifs(motif_tuple, (benchmark_cell.exhaustive_cell(),))
    counts = {
        motif: {outcome: 0 for outcome in CalibrationOutcome}
        for motif in motif_tuple
    }
    for indices in combinations(range(total_runs), sample_size):
        sampled = classify_motifs(motif_tuple, (benchmark_cell.sampled_cell(indices),))
        for motif in motif_tuple:
            outcome = _outcome(
                sampled.classifications[motif].status,
                truth.classifications[motif].status,
            )
            counts[motif][outcome] += 1

    return ExactCalibrationSummary(
        sample_size=sample_size,
        total_panels=total_panels,
        truth=truth,
        outcome_counts=counts,
    )
