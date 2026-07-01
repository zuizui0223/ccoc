"""Write a deterministic replay report for budgeted delayed joint quotients."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.delayed_joint_budgeted_quotients import (
    certify_action_budget_frontier,
    certify_depth_budget_frontier,
    certify_trial_budget_frontier,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exterior-port-count", type=int, default=4)
    parser.add_argument("--max-delay", type=int, default=3)
    parser.add_argument("--max-budget", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_exterior_port_count < 1:
        raise ValueError("max-exterior-port-count must be positive")
    if args.max_delay < 0 or args.max_budget < 0:
        raise ValueError("max-delay and max-budget must be non-negative")

    rows = []
    for exterior_port_count in range(1, args.max_exterior_port_count + 1):
        for delay in range(args.max_delay + 1):
            for budget in range(args.max_budget + 1):
                trial = certify_trial_budget_frontier(exterior_port_count, delay, budget)
                action = certify_action_budget_frontier(exterior_port_count, delay, budget)
                depth = certify_depth_budget_frontier(exterior_port_count, delay, budget)
                rows.append(
                    {
                        "exterior_port_count": exterior_port_count,
                        "delay": delay,
                        "budget": budget,
                        "trial_budget_bits": trial.maximum_retained_interface_bits,
                        "trial_budget_residual_cardinality": trial.construction.expected_residual_block_cardinality,
                        "action_budget_bits": action.maximum_retained_interface_bits,
                        "action_budget_residual_cardinality": action.construction.expected_residual_block_cardinality,
                        "depth_budget_bits": depth.maximum_retained_interface_bits,
                        "depth_reaches_terminal_boundary": depth.can_reach_terminal_boundary,
                        "verified": trial.verify() and action.verify() and depth.verify(),
                    }
                )

    report = {
        "theorem_domain": "finite deterministic delayed binary joint families with fresh resettable panels",
        "claims": [
            "panel quotient depends only on covered terminal probes",
            "each newly covered terminal probe adds one exact bit and halves residual ambiguity",
            "duplicate and wait-only trials have zero marginal exact value",
            "trial, action, and depth budgets have sharp but distinct quotient frontiers",
        ],
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
