"""Write a deterministic certificate-replay report for delayed addressability."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.delayed_addressability import (
    certify_delayed_addressability,
    certify_delayed_closure_nonidentifiability,
    certify_delayed_relay_attachment,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-module-count", type=int, default=5)
    parser.add_argument("--max-delay", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_module_count < 1:
        raise ValueError("max-module-count must be positive")
    if args.max_delay < 0:
        raise ValueError("max-delay must be non-negative")

    rows = []
    for module_count in range(1, args.max_module_count + 1):
        for delay in range(args.max_delay + 1):
            delayed = certify_delayed_addressability(module_count, delay)
            no_go = certify_delayed_closure_nonidentifiability(module_count, delay, port=module_count - 1)
            relay = certify_delayed_relay_attachment(
                module_count,
                delay,
                port=module_count - 1,
                initial_state=(0,) + tuple(1 if index == module_count - 1 else 0 for index in range(module_count)),
            )
            rows.append(
                {
                    "module_count": module_count,
                    "delay": delay,
                    "revealing_horizon": delayed.revealing_horizon,
                    "closed_block_counts": list(delayed.closed_block_counts),
                    "open_block_count": delayed.open_block_count,
                    "open_interface_bits": delayed.open_interface_bits,
                    "closed_interface_bits": list(delayed.closed_interface_bits),
                    "pre_reveal_open_block_count": delayed.pre_reveal_open_block_count,
                    "no_go_verified": no_go.verify(),
                    "relay_verified": relay.verify(),
                    "verified": delayed.verify(),
                }
            )

    report = {
        "theorem_domain": "finite deterministic coordinate systems under a prefix-closed delayed boundary grammar",
        "claims": [
            "for every fixed delayed context, the exact open quotient stabilizes at the declared revealing horizon",
            "the robust open interface has m+1 bits while each fixed structural attachment has two bits",
            "closed and open families agree through the delay but diverge on the next legal boundary event",
        ],
        "max_module_count": args.max_module_count,
        "max_delay": args.max_delay,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
