from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.extension_compression_noncommutation import (
    certify_closed_context_factorization,
    certify_relay_tree_sharpness,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-module-count", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_module_count < 1:
        raise ValueError("max-module-count must be positive")

    generic = certify_closed_context_factorization(3, (2, 4, 8))
    sharp = []
    for module_count in range(1, args.max_module_count + 1):
        certificate = certify_relay_tree_sharpness(module_count)
        sharp.append(
            {
                "module_count": module_count,
                "closed_interface_bits": certificate.closed_bits,
                "open_interface_bits": certificate.open_bits,
                "gap_bits": certificate.gap_bits,
                "maximum_degree": certificate.relay_compilation.grammar.maximum_degree,
                "verified": certificate.verify(),
            }
        )

    report = {
        "theorem_domain": "finite deterministic addressable product systems and the binary bounded-degree relay-tree realization",
        "generic_product": {
            "inside_cardinality": generic.inside_cardinality,
            "exterior_cardinalities": generic.exterior_cardinalities,
            "open_state_lower_bound": generic.product_certificate.open_state_lower_bound,
            "closed_context_state_counts": generic.closed_context_state_counts,
            "gap_lower_bound_bits": generic.noncommutation_gap_lower_bound,
            "verified": generic.verify(),
        },
        "binary_relay_sharpness": sharp,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
