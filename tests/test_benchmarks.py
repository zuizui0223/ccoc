import pytest

from causal_model.admissibility import ClaimCoverage, MotifStatus, ProgramRun
from causal_model.benchmarks import (
    CalibrationOutcome,
    FiniteBenchmarkCell,
    calibrate_single_cell_exhaustively,
    compare_sample_to_known_truth,
)


def _cell() -> FiniteBenchmarkCell:
    return FiniteBenchmarkCell(
        cell_id="truth",
        description="known finite universe",
        full_runs=(
            ProgramRun("r0", "truth", frozenset({"a"}), True),
            ProgramRun("r1", "truth", frozenset({"a", "b"}), True),
            ProgramRun("r2", "truth", frozenset(), True),
            ProgramRun("r3", "truth", frozenset({"a", "b"}), False),
        ),
    )


def test_comparison_flags_false_invariant_and_false_exclusion() -> None:
    comparison = compare_sample_to_known_truth(
        ("a", "b", "c"),
        (_cell(),),
        {"truth": (0,)},
    )
    assert comparison.truth.classifications["a"].status is MotifStatus.UNRESOLVED
    assert comparison.truth.classifications["b"].status is MotifStatus.UNRESOLVED
    assert comparison.truth.classifications["c"].status is MotifStatus.EXCLUDED
    assert comparison.truth.classifications["a"].claim_coverage is ClaimCoverage.COMPLETE
    assert comparison.sampled.classifications["a"].claim_coverage is ClaimCoverage.SAMPLED
    assert comparison.outcomes["a"] is CalibrationOutcome.FALSE_INVARIANT
    assert comparison.outcomes["b"] is CalibrationOutcome.FALSE_EXCLUDED
    assert comparison.outcomes["c"] is CalibrationOutcome.MATCH


def test_exact_single_cell_calibration_counts_all_equal_size_panels() -> None:
    summary = calibrate_single_cell_exhaustively(("a", "b", "c"), _cell(), sample_size=1)
    assert summary.total_panels == 4
    assert summary.outcome_counts["a"][CalibrationOutcome.FALSE_INVARIANT] == 2
    assert summary.outcome_counts["a"][CalibrationOutcome.FALSE_EXCLUDED] == 1
    assert summary.outcome_counts["a"][CalibrationOutcome.UNSUPPORTED] == 1
    assert summary.rate("a", CalibrationOutcome.FALSE_INVARIANT) == 0.5


def test_benchmark_sample_mapping_must_cover_exactly_the_declared_cells() -> None:
    with pytest.raises(ValueError, match="exactly"):
        compare_sample_to_known_truth(("a",), (_cell(),), {})


def test_calibration_rejects_unmanageable_or_invalid_panel_sizes() -> None:
    with pytest.raises(ValueError, match="between"):
        calibrate_single_cell_exhaustively(("a",), _cell(), sample_size=0)
    with pytest.raises(ValueError, match="max_panels"):
        calibrate_single_cell_exhaustively(("a",), _cell(), sample_size=2, max_panels=1)
