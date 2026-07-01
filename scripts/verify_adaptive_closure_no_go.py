from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.adaptive_closure_no_go import (
    BIT1,
    FIRE,
    FiniteAdaptivePolicy,
    certify_adaptive_closure_no_go,
    certify_transcript_upper_bound_refutation,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--max-address-bits", type=int, default=2)
    parser.add_argument("--max-upper-bound", type=int, default=31)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if min(args.max_depth, args.max_address_bits, args.max_upper_bound) < 0:
        raise ValueError("all maxima must be non-negative")

    rows = []
    for depth in range(args.max_depth + 1):
        policy = FiniteAdaptivePolicy.from_rule(
            depth,
            lambda history: BIT1 if history[-1] else FIRE,
        )
        for address_bits in range(args.max_address_bits + 1):
            certificate = certify_adaptive_closure_no_go(policy, address_bits)
            rows.append(
                {
                    "policy_depth": depth,
                    "delay": certificate.delay,
                    "address_bits": address_bits,
                    "constant_action_alphabet": ["tick", "bit0", "bit1", "fire"],
                    "closed_blanket_count": certificate.closed_blanket.claimed_blanket_count,
                    "open_blanket_count": certificate.open_blanket_count,
                    "future_separator_length": len(certificate.future_separator_word),
                    "same_adaptive_transcript": certificate.policy_lifting.left_transcript == certificate.policy_lifting.right_transcript,
                    "verified": certificate.verify(),
                }
            )

    upper_rows = []
    policy = FiniteAdaptivePolicy.constant(depth=args.max_depth)
    for upper_bound in range(1, args.max_upper_bound + 1):
        certificate = certify_transcript_upper_bound_refutation(policy, upper_bound)
        upper_rows.append(
            {
                "proposed_upper_bound": upper_bound,
                "open_blanket_count": certificate.no_go.open_blanket_count,
                "address_bits": certificate.no_go.address_bits,
                "verified": certificate.verify(),
            }
        )

    report = {
        "theorem_domain": "finite deterministic delay-gated closed/open pairs under one constant action alphabet and finite adaptive policies",
        "claims": [
            "all action words through the policy horizon agree",
            "policy lifting gives identical adaptive transcripts",
            "the closed comparator has one exterior response class",
            "the delayed open witness has 2^(2^ell) exterior response classes",
            "every proposed finite transcript-only blanket upper bound has a same-transcript delayed refutation",
        ],
        "no_go_rows": rows,
        "upper_bound_refutations": upper_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
