#!/usr/bin/env python3
"""Exhaustively model-check the finite causal-closure theorem regression domain.

This script is deliberately dependency-free.  It enumerates all labelled total
maps on 1..4 states (288 systems), invokes the exact certificate classifier, and
writes a deterministic JSON summary suitable for a GitHub Actions artifact.

It does not claim formal verification of arbitrary continuous, stochastic, or
infinite-state dynamics.  It is an executable finite-model regression check of
the precise theorem domain implemented by causal_closure_calculus.py.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.causal_closure_calculus import (
    ClosureKind,
    classify_closure,
    exhaustive_rule_systems,
    verify_global_closure_certificate,
    verify_multistability_certificate,
    verify_recurrent_cycle_certificate,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-state-count", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.max_state_count <= 6:
        raise SystemExit("--max-state-count must be in [1, 6]")

    summaries: dict[str, dict[str, int]] = {}
    total = 0
    for count in range(1, args.max_state_count + 1):
        counts = {kind.value: 0 for kind in ClosureKind}
        for rule in exhaustive_rule_systems(count):
            classification = classify_closure(rule)
            if classification.kind is ClosureKind.GLOBAL_CLOSURE:
                verify_global_closure_certificate(rule, classification.global_closure)
            elif classification.kind is ClosureKind.RECURRENT_NONCLOSURE:
                verify_recurrent_cycle_certificate(rule, classification.recurrent_cycle)
            else:
                verify_multistability_certificate(rule, classification.multistability)
            counts[classification.kind.value] += 1
            total += 1
        if sum(counts.values()) != count**count:
            raise AssertionError("classification is not exhaustive for a finite map domain")
        summaries[str(count)] = counts

    result = {
        "format_version": "rach-causal-closure-exhaustive-regression/v1",
        "max_state_count": args.max_state_count,
        "total_rule_systems_checked": total,
        "theorem_domain": "finite labelled total deterministic maps",
        "conclusions": [
            "A strict integer ranking certificate proves global convergence to one fixed point.",
            "A nontrivial cycle certificate proves failure of global one-point closure.",
            "Absent nontrivial cycles, multiple fixed points certify multistable non-closure.",
        ],
        "classification_counts": summaries,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
