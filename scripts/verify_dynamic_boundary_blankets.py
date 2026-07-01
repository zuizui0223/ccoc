"""Write a deterministic certificate-replay report for dynamic boundary blankets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.dynamic_boundary_blankets import (
    certify_dynamic_boundary_blanket,
    certify_finite_horizon_stabilization,
    certify_uniform_blanket_obstruction,
    delay_chain_system,
    redundant_boundary_system,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-delay-chain-states", type=int, default=8)
    parser.add_argument("--max-binary-exterior-count", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_delay_chain_states < 2:
        raise ValueError("max-delay-chain-states must be at least two")
    if args.max_binary_exterior_count < 1:
        raise ValueError("max-binary-exterior-count must be positive")

    delay_rows = []
    for state_count in range(2, args.max_delay_chain_states + 1):
        certificate = certify_finite_horizon_stabilization(delay_chain_system(state_count))
        delay_rows.append(
            {
                "state_count": state_count,
                "stabilization_horizon": certificate.stabilization_horizon,
                "state_count_bound": certificate.state_count_bound,
                "canonical_block_count": certificate.canonical_block_count,
                "partition_block_counts": list(certificate.partition_block_counts),
                "verified": certificate.verify(),
            }
        )

    redundant_system, inside_labels, boundary_labels = redundant_boundary_system()
    redundant_certificate = certify_dynamic_boundary_blanket(
        redundant_system,
        inside_labels,
        boundary_labels,
    )

    obstruction_rows = []
    for exterior_count in range(1, args.max_binary_exterior_count + 1):
        factors = (2,) * (exterior_count + 1)
        certificate = certify_uniform_blanket_obstruction(factors)
        obstruction_rows.append(
            {
                "exterior_count": exterior_count,
                "factor_cardinalities": list(factors),
                "required_boundary_state_count": certificate.required_boundary_state_count,
                "required_boundary_bits": certificate.required_boundary_bits,
                "open_block_count": certificate.open_block_count,
                "verified": certificate.verify(),
            }
        )

    report = {
        "theorem_domain": "finite deterministic controlled output systems with declared action grammars",
        "claims": [
            "finite all-word trace quotients stabilize by the state-count bound",
            "dynamic inside-plus-boundary summaries are exact only when action updates factor through them",
            "addressable exterior products obstruct a uniformly bounded blanket",
        ],
        "delay_chain_rows": delay_rows,
        "redundant_boundary_blanket": {
            "inside_cardinality": redundant_certificate.inside_cardinality,
            "boundary_cardinality": redundant_certificate.boundary_cardinality,
            "realized_pair_cardinality": redundant_certificate.realized_pair_cardinality,
            "canonical_block_count": redundant_certificate.canonical_block_count,
            "stabilization_horizon": redundant_certificate.stabilization_horizon,
            "realized_horizon_bound": redundant_certificate.realized_horizon_bound,
            "verified": redundant_certificate.verify(),
        },
        "uniform_blanket_obstruction_rows": obstruction_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
