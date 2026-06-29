from itertools import combinations
from math import isclose

import pytest

from causal_model import (
    CandidateAcceptanceSet,
    CandidateMotifUniverse,
    ConfidenceSetCell,
    CoverageMode,
    JointCoverageCertificate,
    deterministic_lifting_witness,
    indistinguishability_abstention_lower_bound,
    soundness_guarantee_from_joint_coverage,
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


def cells(left: frozenset[str], right: frozenset[str]) -> tuple[ConfidenceSetCell, ...]:
    return (
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
    )


def test_lifting_implication_holds_for_every_finite_acceptance_outcome() -> None:
    """Exhaustively check false decisive => true candidate omitted in some required cell."""

    for left in all_subsets(UNIVERSE.candidate_ids):
        for right in all_subsets(UNIVERSE.candidate_ids):
            witness = deterministic_lifting_witness(
                UNIVERSE,
                cells(left, right),
                true_candidate_id="inactive",
            )
            assert witness.implication_holds
            if witness.true_candidate_retained_in_all_required_cells:
                assert witness.false_decisive_motifs == ()


def test_joint_coverage_certificate_lifts_to_simultaneous_false_decisive_bound() -> None:
    guarantee = soundness_guarantee_from_joint_coverage(
        UNIVERSE,
        JointCoverageCertificate(
            true_candidate_id="inactive",
            required_cell_ids=("left", "right"),
            lower_bound=0.95,
            method="externally validated finite-sample confidence set",
            assumptions=("coverage is simultaneous over left and right",),
        ),
    )

    assert isclose(guarantee.family_wise_false_decisive_upper_bound, 0.05)
    assert isclose(guarantee.false_invariant_upper_bounds["focal"], 0.05)
    assert guarantee.false_excluded_upper_bounds["focal"] == 0.0
    assert guarantee.certificate_assumptions == ("coverage is simultaneous over left and right",)


def test_active_truth_has_only_false_exclusion_risk() -> None:
    guarantee = soundness_guarantee_from_joint_coverage(
        UNIVERSE,
        JointCoverageCertificate(
            true_candidate_id="active",
            required_cell_ids=("left",),
            lower_bound=0.9,
            method="any valid randomized confidence procedure",
        ),
    )

    assert guarantee.false_invariant_upper_bounds["focal"] == 0.0
    assert isclose(guarantee.false_excluded_upper_bounds["focal"], 0.1)


def test_unknown_retained_candidate_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown candidate IDs"):
        deterministic_lifting_witness(
            UNIVERSE,
            (
                ConfidenceSetCell(
                    "evidence",
                    CandidateAcceptanceSet(frozenset({"not_declared"})),
                ),
            ),
            true_candidate_id="inactive",
        )


def test_indistinguishable_pair_requires_abstention_at_small_error() -> None:
    assert isclose(indistinguishability_abstention_lower_bound(0.05), 0.9)
    assert indistinguishability_abstention_lower_bound(0.6) == 0.0
