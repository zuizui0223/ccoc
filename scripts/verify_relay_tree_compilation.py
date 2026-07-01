"""Write a deterministic finite report for the bounded-degree relay-tree compilation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.relay_tree_compilation import exhaustive_compilation_summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-module-count", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    certificates = exhaustive_compilation_summary(args.max_module_count)
    report = {
        "theorem_domain": "quiescent macro-time of finite deterministic one-token relay trees",
        "claim": "the fixed local grammar and degree-three relay tree implement the extension-compression coordinate witness exactly",
        "max_module_count": args.max_module_count,
        "rows": [
            {
                "module_count": certificate.module_count,
                "relay_count": certificate.topology.relay_count,
                "settling_ticks": certificate.topology.settling_ticks,
                "maximum_degree_by_port": [
                    certificate.topology.maximum_degree_with_reader(port)
                    for port in range(certificate.module_count)
                ],
                "checked_protocols": certificate.checked_protocols,
                "closed_interface_bits": list(certificate.closed_interface_bits),
                "open_interface_bits": certificate.open_interface_bits,
                "open_interface_state_count": certificate.open_interface_state_count,
                "verified": certificate.verify(),
            }
            for certificate in certificates
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
