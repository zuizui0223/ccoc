import pytest

from causal_model.admissibility import (
    MotifStatus,
    ProgramRun,
    RobustnessCell,
    classify_motifs,
)


def _cell(cell_id: str, rows: list[tuple[bool, set[str]]], *, required: bool = True) -> RobustnessCell:
    return RobustnessCell(
        cell_id=cell_id,
        description=cell_id,
        required=required,
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


def test_optional_empty_cell_does_not_block_supported_invariant() -> None:
    report = classify_motifs(
        ("m",),
        (
            _cell("required", [(True, {"m"})]),
            _cell("optional", [(False, {"m"})], required=False),
        ),
    )
    assert report.classifications["m"].status is MotifStatus.INVARIANT


def test_unknown_motif_in_run_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown motifs"):
        classify_motifs(
            ("declared",),
            (_cell("cell", [(True, {"undeclared"})]),),
        )


def test_empty_motif_vocabulary_is_rejected() -> None:
    with pytest.raises(ValueError, match="at least one declared motif"):
        classify_motifs((), (_cell("cell", [(True, set())]),))
