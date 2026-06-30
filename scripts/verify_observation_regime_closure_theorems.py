#!/usr/bin/env python3
"""Exhaustively model-check finite observation-regime closure verdicts.

For every ordered pair (F_natural, F_observed) of labelled total maps on up to
three states, this script verifies each individual closure certificate through
the imported classifier and checks that the pair-level verdict agrees with the
two exact closure kinds.  It writes a deterministic JSON report for GitHub
Actions.

This is finite-model checking for the theorem domain only. It does not establish
that empirical observation is invasive, nor does it prove a statement about
continuous or stochastic dynamics.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.observation_regime_closure import (
    ObservationRegimeVerdict,
    classify_observation_regime_pair,
    exhaustive_observation_regime_pairs,
    regime_verdict,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-state-count", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.max_state_count <= 3:
        raise SystemExit("--max-state-count must be in [1, 3]")

    summary: dict[str, dict[str, int]] = {}
    total_pairs = 0
    for state_count in range(1, args.max_state_count + 1):
        counts = {verdict.value: 0 for verdict in ObservationRegimeVerdict}
        for pair in exhaustive_observation_regime_pairs(state_count):
            classification = classify_observation_regime_pair(pair)
            expected = regime_verdict(
                classification.natural_classification.kind,
                classification.observed_classification.kind,
            )
            if classification.verdict is not expected:
                raise AssertionError("pair verdict diverges from exact regime-kind table")
            counts[classification.verdict.value] += 1
            total_pairs += 1
        expected_count = (state_count**state_count) ** 2
        if sum(counts.values()) != expected_count:
            raise AssertionError("regime-pair classification is not exhaustive")
        summary[str(state_count)] = counts

    result = {
        "format_version": "rach-observation-regime-closure-regression/v1",
        "max_state_count": args.max_state_count,
        "total_ordered_regime_pairs_checked": total_pairs,
        "theorem_domain": "ordered pairs of finite labelled total deterministic maps on one common state space",
        "conclusions": [
            "Regime verdicts are derived solely from independently certified closure kinds.",
            "A nonclosing natural map plus a globally closing observed map is observation-induced closure in this declared pair model.",
            "A globally closing natural map plus a recurrent observed map is observation-induced recurrence in this declared pair model.",
            "The regression does not infer whether observation is causally invasive in an empirical system.",
        ],
        "verdict_counts": summary,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
