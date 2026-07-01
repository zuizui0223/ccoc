"""Write a deterministic replay report for delayed joint nonidentifiability."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.delayed_joint_nonidentifiability import (
    certify_delayed_joint_no_uniform_horizon,
    certify_delayed_joint_quotient_jump,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exterior-port-count", type=int, default=3)
    parser.add_argument("--max-delay", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_exterior_port_count < 1:
        raise ValueError("max-exterior-port-count must be positive")
    if args.max_delay < 0:
        raise ValueError("max-delay must be non-negative")

    quotient_rows = []
    horizon_rows = []
    for exterior_port_count in range(1, args.max_exterior_port_count + 1):
        for delay in range(args.max_delay + 1):
            quotient = certify_delayed_joint_quotient_jump(exterior_port_count, delay)
            no_uniform = certify_delayed_joint_no_uniform_horizon(exterior_port_count, delay)
            quotient_rows.append(
                {
                    "exterior_port_count": exterior_port_count,
                    "delay": delay,
                    "early_block_count": quotient.early_block_count,
                    "full_block_count": quotient.full_block_count,
                    "first_revealing_horizon": quotient.first_revealing_horizon,
                    "early_interface_bits": quotient.family.early_interface_bits,
                    "full_interface_bits": quotient.family.full_interface_bits,
                    "pair_separator_count": quotient.all_pair_separator_count,
                    "verified": quotient.verify(),
                }
            )
            horizon_rows.append(
                {
                    "exterior_port_count": exterior_port_count,
                    "proposed_horizon": delay,
                    "later_exterior_word_length": len(no_uniform.exterior_separator.word),
                    "later_response_word_length": len(no_uniform.response_separator.word),
                    "verified": no_uniform.verify(),
                }
            )

    report = {
        "theorem_domain": "finite binary exterior-plus-response families under a fixed action-kind alphabet and delayed structural boundary grammar",
        "claims": [
            "all initial legal traces through delay H retain only the focal output bit",
            "the full initial-slice quotient at horizon H+1 has 2^(m+2) blocks",
            "late structural reads separate exterior coordinates and late intervention separates response type",
            "no finite horizon is uniform across the expanding delayed joint family",
        ],
        "quotient_rows": quotient_rows,
        "no_uniform_horizon_rows": horizon_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
