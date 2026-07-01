from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.compositional_boundedness import (
    certify_binary_relay_growth,
    certify_cumulative_addressability_chain,
    certify_inert_attachment_boundedness,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-module-count", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_module_count < 1:
        raise ValueError("max-module-count must be positive")

    bounded = certify_inert_attachment_boundedness(args.max_module_count)
    binary = certify_cumulative_addressability_chain(2, (2,) * args.max_module_count)
    relay = certify_binary_relay_growth(args.max_module_count)
    nonbinary = certify_cumulative_addressability_chain(3, (2, 4, 3))

    report = {
        "theorem_domain": "finite deterministic stage chains under explicit uniform-factorization or joint-addressability premises",
        "claims": [
            "a common finite grammar-aware summary codomain bounds every stage quotient",
            "jointly realizable independently decoded factors force cumulative product lower bounds",
            "the binary relay-tree family attains the cumulative lower bound",
            "families satisfying neither premise remain unresolved",
        ],
        "uniform_inert_chain": {
            "module_counts": list(range(1, args.max_module_count + 1)),
            "physical_state_counts": [stage.constrained_system.system.state_count for stage in bounded.stages],
            "canonical_block_counts": bounded.canonical_block_counts,
            "summary_state_bound": bounded.summary_state_bound,
            "verified": bounded.verify(),
        },
        "binary_addressability_chain": {
            "open_state_lower_bounds": binary.open_state_lower_bounds,
            "open_bits_lower_bounds": binary.open_bits_lower_bounds,
            "relay_exact_bits": [stage.open_bits for stage in relay.relay_stages],
            "verified": binary.verify() and relay.verify(),
        },
        "nonbinary_product": {
            "inside_cardinality": nonbinary.inside_cardinality,
            "exterior_cardinalities": nonbinary.exterior_cardinalities,
            "open_state_lower_bounds": nonbinary.open_state_lower_bounds,
            "verified": nonbinary.verify(),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
