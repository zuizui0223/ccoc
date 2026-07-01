"""Write a deterministic certificate-replay report for product completion bounds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.addressable_completion_bounds import (
    certify_addressable_completion_product,
    certify_finite_boundary_blanket,
    certify_passive_closure_nonidentifiability,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exterior-count", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_exterior_count < 1:
        raise ValueError("max-exterior-count must be positive")

    binary_rows = []
    for exterior_count in range(1, args.max_exterior_count + 1):
        factors = (2,) * (exterior_count + 1)
        product_certificate = certify_addressable_completion_product(factors)
        no_go_certificate = certify_passive_closure_nonidentifiability(factors)
        active_indices = tuple(range(1, exterior_count + 1, 2))
        blanket_certificate = certify_finite_boundary_blanket(factors, active_indices)
        binary_rows.append(
            {
                "factor_cardinalities": list(factors),
                "exterior_count": exterior_count,
                "passive_block_count": product_certificate.passive_block_count,
                "closed_block_counts": list(product_certificate.closed_block_counts),
                "open_block_count": product_certificate.open_block_count,
                "open_interface_bits": product_certificate.open_interface_bits,
                "product_lower_bound_bits": product_certificate.product_lower_bound_bits,
                "extension_compression_gap_bits": product_certificate.extension_compression_gap_bits,
                "gap_lower_bound_bits": product_certificate.gap_lower_bound_bits,
                "checked_separating_pairs": product_certificate.checked_separating_pairs,
                "passive_nonidentifiability_verified": no_go_certificate.verify(),
                "blanket_active_indices": list(active_indices),
                "blanket_interface_bits": blanket_certificate.realized_interface_bits,
                "blanket_verified": blanket_certificate.verify(),
                "verified": product_certificate.verify(),
            }
        )

    nonbinary_factors = (3, 2, 5)
    nonbinary_certificate = certify_addressable_completion_product(nonbinary_factors)
    report = {
        "theorem_domain": "finite deterministic controlled response systems with operationally addressable exterior product coordinates",
        "claim": "concrete separating words force the product lower bound and the closed/open extension-compression gap",
        "max_exterior_count": args.max_exterior_count,
        "binary_rows": binary_rows,
        "nonbinary_exact_case": {
            "factor_cardinalities": list(nonbinary_factors),
            "closed_block_counts": list(nonbinary_certificate.closed_block_counts),
            "open_block_count": nonbinary_certificate.open_block_count,
            "open_interface_bits": nonbinary_certificate.open_interface_bits,
            "extension_compression_gap_bits": nonbinary_certificate.extension_compression_gap_bits,
            "gap_lower_bound_bits": nonbinary_certificate.gap_lower_bound_bits,
            "verified": nonbinary_certificate.verify(),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
