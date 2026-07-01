"""Write a deterministic replay report for witnessed boundary evidence bounds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.canonical_boundary_blankets import redundant_exterior_response_table
from causal_model.witnessed_boundary_evidence import (
    certify_completion_coverage,
    certify_evidence_chain,
    certify_free_completion_extension,
    certify_witnessed_boundary_lower_bound,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-fresh-completions", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_fresh_completions < 1:
        raise ValueError("max-fresh-completions must be positive")

    system = redundant_exterior_response_table()
    grammar = ("observe", "read")
    partial = certify_witnessed_boundary_lower_bound(
        system,
        grammar,
        (0, 2),
        ((0, "observe"),),
    )
    witnessed = certify_witnessed_boundary_lower_bound(
        system,
        grammar,
        (0, 2),
        ((0, "read"),),
    )
    chain = certify_evidence_chain(
        system,
        grammar,
        (
            ((0,), ((0, "observe"),)),
            ((0, 2), ((0, "observe"),)),
            ((0, 2), ((0, "observe"), (0, "read"))),
            ((0, 1, 2, 3), ((0, "observe"), (0, "read"))),
        ),
    )
    coverage = certify_completion_coverage(system, grammar, (0, 2))

    extensions = []
    for fresh_count in range(1, args.max_fresh_completions + 1):
        certificate = certify_free_completion_extension(
            system,
            sampled_exteriors=(0, 2),
            observed_cells=((0, "observe"), (0, "read")),
            baseline_exterior=0,
            fresh_completion_count=fresh_count,
        )
        extensions.append(
            {
                "fresh_completion_count": fresh_count,
                "original_blanket_count": certificate.original_blanket_count,
                "extended_blanket_count": certificate.extended_blanket_count,
                "fresh_word_count": len(certificate.fresh_words),
                "verified": certificate.verify(),
            }
        )

    report = {
        "theorem_domain": "finite deterministic exterior response tables with sampled completions and tested boundary cells",
        "claims": [
            "observed response-signature classes certify lower bounds on canonical blanket cardinality",
            "every observed class-pair lower-bound distinction has a concrete tested-cell witness",
            "exact blanket cardinality needs declared canonical-class and full-grammar coverage",
            "without such coverage, finite transcripts admit arbitrary finite free-completion extensions",
        ],
        "partial_lower_bound": {
            "observed_class_count": partial.observed_class_count,
            "canonical_blanket_count": partial.canonical_blanket_count,
            "witness_count": len(partial.separation_witnesses),
            "verified": partial.verify(),
        },
        "witnessed_lower_bound": {
            "observed_class_count": witnessed.observed_class_count,
            "canonical_blanket_count": witnessed.canonical_blanket_count,
            "witness_count": len(witnessed.separation_witnesses),
            "verified": witnessed.verify(),
        },
        "evidence_chain": {
            "lower_bound_counts": chain.lower_bound_counts,
            "verified": chain.verify(),
        },
        "completion_coverage": {
            "canonical_blanket_count": coverage.canonical_blanket_count,
            "exact_observed_class_count": coverage.exact_observed_class_count,
            "verified": coverage.verify(),
        },
        "free_completion_extensions": extensions,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
