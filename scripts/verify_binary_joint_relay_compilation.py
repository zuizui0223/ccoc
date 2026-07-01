"""Write a deterministic replay report for the binary joint relay compiler."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.binary_joint_relay_compilation import (
    BinaryJointMacroAction,
    all_binary_joint_states,
    certify_binary_joint_relay_compilation,
    certify_binary_joint_relay_protocol,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exterior-port-count", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_exterior_port_count < 1:
        raise ValueError("max-exterior-port-count must be positive")

    rows = []
    for exterior_port_count in range(1, args.max_exterior_port_count + 1):
        certificate = certify_binary_joint_relay_compilation(exterior_port_count)
        topology = certificate.topology
        sample_state = all_binary_joint_states(exterior_port_count)[-1]
        read_sample = certify_binary_joint_relay_protocol(
            topology, sample_state, BinaryJointMacroAction.read(exterior_port_count - 1)
        )
        intervene_sample = certify_binary_joint_relay_protocol(
            topology, sample_state, BinaryJointMacroAction.intervene()
        )
        rows.append(
            {
                "exterior_port_count": exterior_port_count,
                "macro_state_count": certificate.checked_macro_state_count,
                "read_protocol_count": certificate.checked_read_protocols,
                "intervene_protocol_count": certificate.checked_intervene_protocols,
                "observe_protocol_count": certificate.checked_observe_protocols,
                "joint_safe_interface_bits": certificate.joint_safe_interface_bits,
                "maximum_degree": certificate.maximum_degree,
                "read_settling_ticks": len(read_sample.trajectory) - 1,
                "intervene_settling_ticks": len(intervene_sample.trajectory) - 1,
                "verified": certificate.verify(),
            }
        )

    report = {
        "theorem_domain": "binary joint exterior--mechanism family under a sequential one-token relay grammar",
        "claims": [
            "the fixed token alphabet is empty/copy-0/copy-1/xor-0/xor-1",
            "read ports are selected structurally rather than encoded in local action labels",
            "the response type is a permanent leaf bit and intervene realizes y <- y xor r",
            "every quiescent binary joint macro action is conjugate to a degree-three pairwise micro protocol",
        ],
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
