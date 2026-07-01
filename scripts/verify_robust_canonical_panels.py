"""Write a deterministic replay report for robust canonical distinguishing panels."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.canonical_boundary_blankets import redundant_exterior_response_table
from causal_model.robust_canonical_panels import (
    analyze_canonical_panel,
    build_canonical_separation_hypergraph,
    certify_dropout_ambiguity,
    certify_private_bundle_optimality,
    certify_robust_canonical_panel,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-replication", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_replication < 1:
        raise ValueError("max-replication must be positive")

    baseline_system = redundant_exterior_response_table()
    baseline_hypergraph = build_canonical_separation_hypergraph(baseline_system, ("observe", "read"))
    exact_one = certify_robust_canonical_panel(baseline_hypergraph, ((0, "read"),), 0)
    robust_one = certify_robust_canonical_panel(
        baseline_hypergraph,
        ((0, "read"), (1, "read")),
        1,
    )
    failure_profile = analyze_canonical_panel(baseline_hypergraph, ((0, "read"),))
    failure = certify_dropout_ambiguity(failure_profile, 1)

    rows = []
    for replication in range(1, args.max_replication + 1):
        certificate = certify_private_bundle_optimality(replication)
        rows.append(
            {
                "replication": replication,
                "loss_budget": certificate.robust_panel.loss_budget,
                "class_count": certificate.hypergraph.class_count,
                "panel_size": certificate.optimality.panel_size,
                "packing_lower_bound": certificate.packing.lower_bound,
                "verified": certificate.verify(),
            }
        )

    report = {
        "theorem_domain": "finite canonical boundary blankets with independently lossable declared observation/intervention cells",
        "claims": [
            "exact panels are transversals of pairwise canonical-class separation sets",
            "f-loss robust panels are (f+1)-fold transversals",
            "failure produces a concrete ambiguous pair and at-most-f cell dropout set",
            "disjoint separation packings provide analytical robust-panel lower bounds",
        ],
        "two_class_baseline": {
            "single_separator_exact": exact_one.verify(),
            "two_separator_one_loss_robust": robust_one.verify(),
            "one_loss_failure_pair": failure.ambiguous_pair,
            "one_loss_removed_cells": failure.removed_cells,
            "failure_verified": failure.verify(),
        },
        "private_bundle_optimality": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
