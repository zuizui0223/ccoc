from itertools import combinations, product
from math import isclose

import pytest

from causal_model import (
    AnytimeJointCoverageCertificate,
    CandidateAcceptanceSet,
    CandidateMotifUniverse,
    ConfidenceSetCell,
    CoverageMode,
    SequentialConfidenceSetSnapshot,
    anytime_soundness_guarantee_from_coverage,
    deterministic_anytime_lifting_witness,
)


UNIVERSE = CandidateMotifUniverse(
    candidate_motifs={
        "active": frozenset({"focal"}),
        "inactive": frozenset(),
    },
    motifs=("focal",),
)


def all_subsets(items: frozenset[str]) -> tuple[frozenset[str], ...]:
    ordered = tuple(sorted(items))
    return tuple(
        frozenset(selection)
        for size in range(len(ordered) + 1)
        for selection in combinations(ordered, size)
    )


def snapshot(
    look: int,
    left: frozenset[str],
    right: frozenset[str],
) -> SequentialConfidenceSetSnapshot:
    return SequentialConfidenceSetSnapshot(
        look=look,
        cells=(
            ConfidenceSetCell(
                "left",
                CandidateAcceptanceSet(left),
                coverage_mode=CoverageMode.EXHAUSTIVE,
            ),
            ConfidenceSetCell(
                "right",
                CandidateAcceptanceSet(right),
                coverage_mode=CoverageMode.EXHAUSTIVE,
            ),
        ),
    )


def test_anytime_implication_holds_for_every_two_look_acceptance_trajectory() -> None:
    """Exhaustively check all 4^4 retained-set paths over two looks and two cells."""

    subsets = all_subsets(UNIVERSE.candidate_ids)
    for left_1, right_1, left_2, right_2 in product(subsets, repeat=4):
        witness = deterministic_anytime_lifting_witness(
            UNIVERSE,
            (
                snapshot(1, left_1, right_1),
                snapshot(2, left_2, right_2),
            ),
            true_candidate_id="inactive",
        )
        assert witness.implication_holds
        if witness.joint_retention_at_all_looks:
            assert witness.false_decisive_looks == ()


def test_time_uniform_certificate_controls_all_looks_and_any_stopping_time() -> None:
    guarantee = anytime_soundness_guarantee_from_coverage(
        UNIVERSE,
        AnytimeJointCoverageCertificate(
            true_candidate_id="inactive",
            required_cell_ids=("left", "right"),
            lower_bound=0.95,
            method="externally validated confidence sequence",
            assumptions=("simultaneous coverage over every positive integer look",),
        ),
    )

    assert guarantee.certified_looks is None
    assert isclose(guarantee.time_uniform_family_wise_false_decisive_upper_bound, 0.05)
    assert isclose(guarantee.stopping_time_false_decisive_upper_bound, 0.05)
    assert isclose(guarantee.false_invariant_upper_bounds["focal"], 0.05)
    assert guarantee.false_excluded_upper_bounds["focal"] == 0.0


def test_finite_certificate_scope_rejects_an_uncertified_interim_look() -> None:
    certificate = AnytimeJointCoverageCertificate(
        true_candidate_id="inactive",
        required_cell_ids=("left", "right"),
        lower_bound=0.9,
        method="predeclared two-look simultaneous confidence set",
        certified_looks=(1, 2),
    )
    with pytest.raises(ValueError, match="outside the certificate's declared coverage scope"):
        deterministic_anytime_lifting_witness(
            UNIVERSE,
            (
                snapshot(1, frozenset({"inactive"}), frozenset({"inactive"})),
                snapshot(3, frozenset({"inactive"}), frozenset({"inactive"})),
            ),
            true_candidate_id="inactive",
            certificate=certificate,
        )


def test_certificate_rejects_changing_required_cell_sets_between_looks() -> None:
    certificate = AnytimeJointCoverageCertificate(
        true_candidate_id="inactive",
        required_cell_ids=("left", "right"),
        lower_bound=0.95,
        method="externally validated confidence sequence",
    )
    changed_snapshot = SequentialConfidenceSetSnapshot(
        look=2,
        cells=(
            ConfidenceSetCell("left", CandidateAcceptanceSet(frozenset({"inactive"}))),
            ConfidenceSetCell("other", CandidateAcceptanceSet(frozenset({"inactive"}))),
        ),
    )
    with pytest.raises(ValueError, match="same required cell IDs"):
        deterministic_anytime_lifting_witness(
            UNIVERSE,
            (
                snapshot(1, frozenset({"inactive"}), frozenset({"inactive"})),
                changed_snapshot,
            ),
            true_candidate_id="inactive",
            certificate=certificate,
        )


def test_true_retention_at_every_look_allows_correct_late_exclusion() -> None:
    witness = deterministic_anytime_lifting_witness(
        UNIVERSE,
        (
            snapshot(1, frozenset({"active", "inactive"}), frozenset({"active", "inactive"})),
            snapshot(2, frozenset({"inactive"}), frozenset({"inactive"})),
        ),
        true_candidate_id="inactive",
    )

    assert witness.joint_retention_at_all_looks
    assert witness.false_decisive_looks == ()
    assert witness.false_decisive_motifs_by_look[1] == ()
    assert witness.false_decisive_motifs_by_look[2] == ()
