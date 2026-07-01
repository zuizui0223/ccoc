"""Write a deterministic certificate-replay report for candidate-safe macro-laws."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.candidate_safe_laws import (
    CandidateInducedLaw,
    CandidateLawFamily,
    binary_agreement_family,
    binary_identity_flip_family,
    certify_candidate_safe_product,
    certify_delayed_candidate_discrimination,
    certify_set_valued_macro_law,
    certify_universal_macro_law,
    universal_law_obstruction_certificate,
)


def cyclic_shift_family(size: int) -> CandidateLawFamily:
    if size < 2:
        raise ValueError("size must be at least two")
    return CandidateLawFamily(
        tuple(
            CandidateInducedLaw(
                candidate_id=f"shift-{shift}",
                actions=("advance",),
                transition_table=tuple(((state + shift) % size,) for state in range(size)),
                macro_outputs=tuple(range(size)),
            )
            for shift in range(size)
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cyclic-size", type=int, default=5)
    parser.add_argument("--max-delay", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_cyclic_size < 2:
        raise ValueError("max-cyclic-size must be at least two")
    if args.max_delay < 0:
        raise ValueError("max-delay must be non-negative")

    agreement = binary_agreement_family()
    agreement_universal = certify_universal_macro_law(agreement)
    agreement_product = certify_candidate_safe_product(agreement)

    separation = binary_identity_flip_family()
    separation_obstruction = universal_law_obstruction_certificate(separation)
    separation_product = certify_candidate_safe_product(separation)
    separation_set_valued = certify_set_valued_macro_law(separation)

    cyclic_rows = []
    for size in range(2, args.max_cyclic_size + 1):
        family = cyclic_shift_family(size)
        certificate = certify_candidate_safe_product(family)
        set_valued = certify_set_valued_macro_law(family)
        cyclic_rows.append(
            {
                "macrostate_count": size,
                "response_type_count": family.response_type_count,
                "candidate_safe_block_count": certificate.candidate_safe_block_count,
                "instance_interface_bits": certificate.instance_interface_bits,
                "candidate_safe_interface_bits": certificate.candidate_safe_interface_bits,
                "product_lower_bound_bits": certificate.product_lower_bound_bits,
                "set_valued_is_deterministic": set_valued.is_deterministic,
                "verified": certificate.verify() and set_valued.verify(),
            }
        )

    delayed_rows = []
    for delay in range(args.max_delay + 1):
        certificate = certify_delayed_candidate_discrimination(delay)
        delayed_rows.append(
            {
                "delay": delay,
                "revealing_horizon": certificate.revealing_horizon,
                "shared_horizon": certificate.shared_horizon,
                "revealing_word": list(certificate.revealing_word),
                "verified": certificate.verify(),
            }
        )

    report = {
        "theorem_domain": "finite retained candidate families sharing one injectively observable macrostate space and action grammar",
        "claims": [
            "a universal deterministic macro-law exists exactly when all induced candidate maps agree",
            "under uniform response separation, candidate-safe deterministic prediction requires macrostate times response-type memory",
            "candidate-forgetting prediction is set-valued whenever induced candidate maps disagree",
            "candidate response type can remain unresolved through an arbitrarily long delayed legal horizon",
        ],
        "agreement_case": {
            "response_type_count": agreement.response_type_count,
            "universal_verified": agreement_universal.verify(),
            "candidate_safe_block_count": agreement_product.candidate_safe_block_count,
            "candidate_safe_verified": agreement_product.verify(),
        },
        "separation_case": {
            "response_type_count": separation.response_type_count,
            "obstruction_action": separation_obstruction.action,
            "obstruction_verified": separation_obstruction.verify(),
            "candidate_safe_block_count": separation_product.candidate_safe_block_count,
            "set_valued_is_deterministic": separation_set_valued.is_deterministic,
            "verified": separation_product.verify() and separation_set_valued.verify(),
        },
        "cyclic_shift_rows": cyclic_rows,
        "delayed_discrimination_rows": delayed_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
