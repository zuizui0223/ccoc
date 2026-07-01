"""Write a deterministic certificate-replay report for delayed joint reset panels."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.delayed_joint_reset_panels import (
    certify_delayed_joint_reset_panel_complexity,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exterior-port-count", type=int, default=4)
    parser.add_argument("--max-delay", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_exterior_port_count < 1:
        raise ValueError("max-exterior-port-count must be positive")
    if args.max_delay < 0:
        raise ValueError("max-delay must be non-negative")

    rows = []
    for exterior_port_count in range(1, args.max_exterior_port_count + 1):
        for delay in range(args.max_delay + 1):
            certificate = certify_delayed_joint_reset_panel_complexity(exterior_port_count, delay)
            rows.append(
                {
                    "exterior_port_count": exterior_port_count,
                    "delay": delay,
                    "state_count": certificate.family.state_count,
                    "minimum_trial_count": certificate.minimum_trial_count,
                    "minimum_maximum_trial_horizon": certificate.minimum_maximum_trial_horizon,
                    "minimum_total_action_count": certificate.minimum_total_action_count,
                    "parallel_wall_clock_lower_bound": certificate.parallel_wall_clock_lower_bound,
                    "required_probe_count": len(certificate.necessity_certificates),
                    "exact_panel_signature_count": certificate.exactness.signature_count,
                    "verified": certificate.verify(),
                }
            )

    report = {
        "theorem_domain": "finite deterministic binary delayed joint families with fresh resettable replicas",
        "claims": [
            "the canonical delayed read/intervene panel exactly identifies every initial joint state",
            "each exterior read and the intervention word are individually necessary",
            "minimum trials equal m+1",
            "minimum maximum trial depth equals H+1",
            "minimum total sequential action count equals (m+1)(H+1)",
        ],
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
