"""Write a deterministic finite replay report for canonical boundary blankets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.canonical_boundary_blankets import (
    binary_addressable_ladder,
    certify_addressable_ladder,
    certify_boundary_summary_factor,
    certify_canonical_boundary_blanket,
    certify_finite_grammar_chain,
    redundant_exterior_response_table,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-addressable-bits", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_addressable_bits < 1:
        raise ValueError("max-addressable-bits must be positive")

    redundant = redundant_exterior_response_table()
    grammar = ("observe", "read")
    blanket = certify_canonical_boundary_blanket(redundant, grammar)
    raw_summary = certify_boundary_summary_factor(redundant, grammar, (0, 1, 2, 3))
    minimal_summary = certify_boundary_summary_factor(redundant, grammar, (0, 0, 1, 1))
    finite_chain = certify_finite_grammar_chain(
        redundant,
        ((), ("observe",), grammar, grammar),
    )

    ladders = []
    for bit_count in range(1, args.max_addressable_bits + 1):
        certificate = certify_addressable_ladder(bit_count)
        system, levels = binary_addressable_ladder(bit_count)
        ladders.append(
            {
                "bit_count": bit_count,
                "grammar_level_count": len(levels),
                "block_counts": certificate.chain.block_counts,
                "terminal_block_count": certificate.chain.block_counts[-1],
                "expected_terminal_block_count": system.exterior_count,
                "verified": certificate.verify(),
            }
        )

    report = {
        "theorem_domain": "finite deterministic window/exterior response tables with declared finite grammars",
        "claims": [
            "the canonical exterior response quotient is a minimum-cardinality exact boundary blanket",
            "every sound supplied exterior summary factors through the canonical quotient",
            "joint interface complexity is upper-bounded by inside states times canonical blanket states",
            "grammar growth refines canonical exterior partitions",
            "finite addressable prefixes exhibit exact exponential blanket growth but do not certify an infinite grammar",
        ],
        "redundant_exterior": {
            "raw_exterior_count": redundant.exterior_count,
            "canonical_blanket_count": blanket.blanket_block_count,
            "joint_interface_block_count": blanket.joint_interface_block_count,
            "joint_observable": blanket.equality_holds,
            "raw_summary_count": raw_summary.summary_image_count,
            "minimal_summary_count": minimal_summary.summary_image_count,
            "finite_chain_block_counts": finite_chain.block_counts,
            "finite_chain_stable_from": finite_chain.first_terminal_stable_level,
            "verified": blanket.verify() and raw_summary.verify() and minimal_summary.verify() and finite_chain.verify(),
        },
        "addressable_ladders": ladders,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
