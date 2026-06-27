import pytest

from causal_model.admissibility import (
    ClaimCoverage,
    CoverageMode,
    MotifStatus,
    ProgramRun,
    RobustnessCell,
    classify_motifs,
)


def _cell(
    cell_id: str,
    rows: list[tuple[bool, set[str]]],
    *,
    required: bool = True,
    coverage_mode: CoverageMode = CoverageMode.SAMPLED,
) -> RobustnessCell:
    return RobustnessCell(
        cell_id=cell_id,
        description=cell_id,
        required=required,
        coverage_mode=coverage_mode,
        runs=tuple(
            ProgramRun(
                run_id=f"{cell_id}-{index}",
                cell_id=cell_id,
                accepted=accepted,
                active_motifs=frozenset(active),
            )
            for index, (accepted, active) in enumerate(rows)
        ),
    )


def test_invariant_and_excluded_require_agreement_across_cells() -> None:
    report = classify_motifs(
        ("fecundity", "survival", "noise"),
        (
            _cell("prior_a", [(True, {"fecundity"}), (True, {"fecundity"})]),
            _cell("prior_b", [(True, {"fecundity"}), (False, {"survival"})]),
        ),
    )
    assert report.classifications["fecundity"].status is MotifStatus.INVARIANT
    assert report.classifications["survival"].status is MotifStatus.EXCLUDED
    assert report.classifications["noise"].status is MotifStatus.EXCLUDED
    assert report.classifications["fecundity"].claim_coverage is ClaimCoverage.SAMPLED


def test_motif_is_unresolved_when_any_required_cell_mixes_states() -> None:
    report = classify_motifs(
        ("m",),
        (
            _cell("tolerance_low", [(True, {"m"}), (True, set())]),
            _cell("tolerance_high", [(True, {"m"})]),
        ),
    )
    result = report.classifications["m"]
    assert result.status is MotifStatus.UNRESOLVED
    assert result.active_accepted_count == 2
    assert result.inactive_accepted_count == 1


def test_required_empty_cell_blocks_universal_claim() -> None:
    report = classify_motifs(
        ("m",),
        (
            _cell("covered", [(True, {"m"})]),
            _cell("no_accepted_program", [(False, {"m"})]),
        ),
    )
    result = report.classifications["m"]
    assert result.status is MotifStatus.UNSUPPORTED
    assert result.empty_required_cells == ("no_accepted_program",)
    assert result.claim_coverage is ClaimCoverage.UNSUPPORTED


def test_optional_empty_cell_does_not_block_supported_invariant() -> None:
    report = classify_motifs(
        ("m",),
        (
            _cell("required", [(True, {"m"})]),
            _cell("optional", [(False, {"m"})], required=False),
        ),
    )
    assert report.classifications["m"].status is MotifStatus.INVARIANT


def test_all_optional_cells_are_rejected() -> None:
    with pytest.raises(ValueError, match="at least one required robustness cell"):
        classify_motifs(("m",), (_cell("optional", [(True, {"m"})], required=False),))


def test_unknown_motif_in_run_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown motifs"):
        classify_motifs(
            ("declared",),
            (_cell("cell", [(True, {"undeclared"})]),),
        )


def test_empty_motif_vocabulary_is_rejected() -> None:
    with pytest.raises(ValueError, match="at least one declared motif"):
        classify_motifs((), (_cell("cell", [(True, set())]),))


def test_complete_coverage_distinguishes_proof_from_sampled_unanimity() -> None:
    report = classify_motifs(
        ("m",),
        (
            _cell(
                "enumerated",
                [(True, {"m"})],
                coverage_mode=CoverageMode.EXHAUSTIVE,
            ),
            _cell(
                "solver_certificate",
                [(True, {"m"})],
                coverage_mode=CoverageMode.SOLVER_BACKED,
            ),
        ),
    )
    result = report.classifications["m"]
    assert result.status is MotifStatus.INVARIANT
    assert result.claim_coverage is ClaimCoverage.COMPLETE
    assert result.required_cell_coverage == {
        "enumerated": CoverageMode.EXHAUSTIVE,
        "solver_certificate": CoverageMode.SOLVER_BACKED,
    }
    assert report.required_cell_coverage == result.required_cell_coverage


def test_any_sampled_required_cell_keeps_claim_coverage_sampled() -> None:
    report = classify_motifs(
        ("m",),
        (
            _cell("enumerated", [(True, {"m"})], coverage_mode=CoverageMode.EXHAUSTIVE),
            _cell("sampled", [(True, {"m"})]),
        ),
    )
    assert report.classifications["m"].claim_coverage is ClaimCoverage.SAMPLED


def test_invalid_coverage_mode_is_rejected() -> None:
    with pytest.raises(ValueError, match="coverage_mode"):
        RobustnessCell("cell", "cell", (), coverage_mode="sampled")  # type: ignore[arg-type]
