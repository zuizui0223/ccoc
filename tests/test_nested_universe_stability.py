from itertools import combinations

import pytest

from causal_model.admissibility import MotifStatus
from causal_model.nested_universe_stability import (
    FiniteUniverseTier,
    audit_nested_universe_stability,
)


def tier(tier_id, candidates, retained):
    return FiniteUniverseTier(
        tier_id=tier_id,
        motifs=("focal",),
        required_cell_ids=("primary",),
        candidate_motifs=candidates,
        retained_by_cell={"primary": frozenset(retained)},
    )


def nonempty_subsets(items):
    ordered = tuple(items)
    return tuple(
        frozenset(choice)
        for size in range(1, len(ordered) + 1)
        for choice in combinations(ordered, size)
    )


def test_nested_status_monotonicity_exhaustively_holds_over_small_candidate_sets():
    inner_candidates = {"a": frozenset({"focal"}), "b": frozenset()}
    outer_candidates = {**inner_candidates, "c": frozenset({"focal"})}
    for inner_retained in nonempty_subsets(inner_candidates):
        for outer_retained in nonempty_subsets(outer_candidates):
            if not inner_retained <= outer_retained:
                continue
            report = audit_nested_universe_stability(
                (
                    tier("inner", inner_candidates, inner_retained),
                    tier("outer", outer_candidates, outer_retained),
                )
            )
            inner_status = report.tier_statuses["inner"]["focal"]
            outer_status = report.tier_statuses["outer"]["focal"]
            if outer_status is MotifStatus.INVARIANT:
                assert inner_status is MotifStatus.INVARIANT
            if outer_status is MotifStatus.EXCLUDED:
                assert inner_status is MotifStatus.EXCLUDED
            if inner_status is MotifStatus.UNRESOLVED:
                assert outer_status is MotifStatus.UNRESOLVED


def test_inner_invariant_becomes_scope_fragile_after_competitor_expansion():
    report = audit_nested_universe_stability(
        (
            tier("narrow", {"active": frozenset({"focal"})}, {"active"}),
            tier(
                "outer",
                {"active": frozenset({"focal"}), "new_competitor": frozenset()},
                {"active", "new_competitor"},
            ),
        )
    )
    assert report.tier_statuses["narrow"]["focal"] is MotifStatus.INVARIANT
    assert report.outermost_statuses["focal"] is MotifStatus.UNRESOLVED
    assert report.extension_stable_motifs == ()
    assert report.scope_fragile_motifs == ("focal",)


def test_outer_decisive_status_is_extension_stable():
    report = audit_nested_universe_stability(
        (
            tier("narrow", {"a": frozenset({"focal"})}, {"a"}),
            tier(
                "outer",
                {"a": frozenset({"focal"}), "b": frozenset({"focal"})},
                {"a", "b"},
            ),
        )
    )
    assert report.outermost_statuses["focal"] is MotifStatus.INVARIANT
    assert report.extension_stable_motifs == ("focal",)
    assert report.scope_fragile_motifs == ()


def test_extension_rejects_candidate_identity_reassignment():
    with pytest.raises(ValueError, match="preserve their declared motif sets"):
        audit_nested_universe_stability(
            (
                tier("inner", {"a": frozenset({"focal"})}, {"a"}),
                tier("outer", {"a": frozenset()}, {"a"}),
            )
        )


def test_extension_rejects_retained_set_contraction():
    with pytest.raises(ValueError, match="contain the corresponding inner retained sets"):
        audit_nested_universe_stability(
            (
                tier("inner", {"a": frozenset({"focal"}), "b": frozenset()}, {"a", "b"}),
                tier(
                    "outer",
                    {"a": frozenset({"focal"}), "b": frozenset(), "c": frozenset({"focal"})},
                    {"a", "c"},
                ),
            )
        )


def test_empty_retained_set_is_outside_supported_extension_theorem():
    with pytest.raises(ValueError, match="non-empty retained"):
        tier("unsupported", {"a": frozenset({"focal"})}, set())
