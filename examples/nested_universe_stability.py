"""Minimal nested-universe stability audit without raw data.

A narrow universe contains one retained focal-active candidate. The outer
universe adds a retained focal-inactive competitor, so the narrow invariant is
classified as scope-fragile rather than presented as an outer-envelope claim.

Run:
    python examples/nested_universe_stability.py
"""

from causal_model.nested_universe_stability import (
    FiniteUniverseTier,
    audit_nested_universe_stability,
)


def main() -> None:
    narrow = FiniteUniverseTier(
        tier_id="narrow",
        motifs=("focal",),
        required_cell_ids=("primary",),
        candidate_motifs={"route_a": frozenset({"focal"})},
        retained_by_cell={"primary": frozenset({"route_a"})},
    )
    outer = FiniteUniverseTier(
        tier_id="outer-envelope",
        motifs=("focal",),
        required_cell_ids=("primary",),
        candidate_motifs={
            "route_a": frozenset({"focal"}),
            "new_competitor": frozenset(),
        },
        retained_by_cell={"primary": frozenset({"route_a", "new_competitor"})},
    )
    report = audit_nested_universe_stability((narrow, outer))
    print("narrow:", report.tier_statuses["narrow"]["focal"].value)
    print("outer:", report.outermost_statuses["focal"].value)
    print("extension-stable:", report.extension_stable_motifs)
    print("scope-fragile:", report.scope_fragile_motifs)


if __name__ == "__main__":
    main()
