"""Write a deterministic finite report for observation-window completion certificates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.observation_window_completion import exhaustive_observation_window_summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-module-count", type=int, default=6)
    parser.add_argument("--passive-horizon", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    certificates = exhaustive_observation_window_summary(
        max_module_count=args.max_module_count,
        passive_horizon_checked=args.passive_horizon,
    )
    report = {
        "theorem_domain": (
            "finite deterministic observation windows with a declared passive action grammar "
            "and sequential boundary probes"
        ),
        "claim": (
            "passive observations do not certify closure in the witness family: "
            "K_passive=1 while K_open=m+1"
        ),
        "max_module_count": args.max_module_count,
        "passive_horizon": args.passive_horizon,
        "rows": [
            {
                "module_count": certificate.module_count,
                "passive_block_count": certificate.passive_block_count,
                "passive_interface_bits": certificate.passive_interface_bits,
                "hidden_completion_count_per_window_value": certificate.hidden_completion_count_per_window_value,
                "open_block_count": certificate.open_block_count,
                "open_interface_bits": certificate.open_interface_bits,
                "counterfactual_inflation_bits": certificate.counterfactual_inflation_bits,
                "checked_counterfactual_certificates": certificate.checked_counterfactual_certificates,
                "verified": certificate.verify(),
            }
            for certificate in certificates
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
