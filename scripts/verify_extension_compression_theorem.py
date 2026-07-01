"""Write a deterministic finite-witness report for the extension-compression theorem."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.extension_compression import exhaustive_witness_summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-module-count", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    certificates = exhaustive_witness_summary(args.max_module_count)
    report = {
        "theorem_domain": "finite deterministic focal-bit systems with declared open probe ports",
        "claim": "every fixed closed port has a 4-state quotient; the open-port quotient is the full microstate partition",
        "max_module_count": args.max_module_count,
        "rows": [
            {
                "module_count": certificate.module_count,
                "closed_block_counts": list(certificate.closed_block_counts),
                "closed_interface_bits": list(certificate.closed_interface_bits),
                "open_block_count": certificate.open_block_count,
                "open_interface_bits": certificate.open_interface_bits,
                "microstate_count": certificate.microstate_count,
                "verified": certificate.verify(),
            }
            for certificate in certificates
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
