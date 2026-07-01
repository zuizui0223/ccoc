"""Write a deterministic certificate-replay report for joint open/candidate laws."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.joint_open_candidate_laws import (
    agreeing_open_law_family,
    certify_candidate_safe_open_law,
    certify_joint_exterior_mechanism_product,
    certify_set_valued_open_law,
    certify_universal_open_law,
    classify_open_law_family,
    conflicting_open_law_family,
    joint_open_law_obstruction_certificate,
    universal_open_law_obstruction_certificate,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-inside-cardinality", type=int, default=4)
    parser.add_argument("--max-port-count", type=int, default=2)
    parser.add_argument("--max-response-types", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_inside_cardinality < 2:
        raise ValueError("max-inside-cardinality must be at least two")
    if args.max_port_count < 1:
        raise ValueError("max-port-count must be positive")
    if args.max_response_types < 1:
        raise ValueError("max-response-types must be positive")

    agreeing = agreeing_open_law_family()
    agreement_certificate = certify_universal_open_law(agreeing)
    agreement_verdict = classify_open_law_family(agreeing, retain_response_type=False)

    conflicting = conflicting_open_law_family()
    conflict_obstruction = universal_open_law_obstruction_certificate(conflicting)
    conflict_candidate_safe = certify_candidate_safe_open_law(conflicting)
    conflict_set_valued = certify_set_valued_open_law(conflicting)
    conflict_candidate_safe_verdict = classify_open_law_family(conflicting, retain_response_type=True)
    conflict_set_valued_verdict = classify_open_law_family(conflicting, retain_response_type=False)

    rows = []
    for port_count in range(1, args.max_port_count + 1):
        exterior_cardinalities = tuple(2 for _ in range(port_count))
        for response_type_count in range(1, args.max_response_types + 1):
            for inside_cardinality in range(max(2, response_type_count), args.max_inside_cardinality + 1):
                certificate = certify_joint_exterior_mechanism_product(
                    inside_cardinality=inside_cardinality,
                    exterior_cardinalities=exterior_cardinalities,
                    response_type_count=response_type_count,
                )
                obstruction_verified = (
                    True
                    if response_type_count == 1
                    else joint_open_law_obstruction_certificate(certificate.product_family).verify()
                )
                rows.append(
                    {
                        "inside_cardinality": inside_cardinality,
                        "exterior_cardinalities": list(exterior_cardinalities),
                        "response_type_count": response_type_count,
                        "fixed_candidate_block_counts": list(certificate.fixed_candidate_block_counts),
                        "joint_block_count": certificate.joint_block_count,
                        "joint_state_count": certificate.joint_state_count,
                        "joint_safe_interface_bits": certificate.joint_safe_interface_bits,
                        "joint_product_lower_bound_bits": certificate.joint_product_lower_bound_bits,
                        "universal_open_law": certificate.product_family.has_universal_open_law,
                        "obstruction_verified": obstruction_verified,
                        "verified": certificate.verify(),
                    }
                )

    report = {
        "theorem_domain": "finite deterministic candidate families with declared dynamic interfaces, plus a structural-port joint product witness",
        "claims": [
            "a universal deterministic open law exists exactly when dynamic candidate interfaces induce the same macro maps",
            "candidate-safe and set-valued outputs are distinct exact reports when maps disagree",
            "the canonical jointly realizable product family attains additive exterior-memory plus response-type information under concrete structural separators",
        ],
        "agreement_case": {
            "universal_verified": agreement_certificate.verify(),
            "verdict": agreement_verdict.kind.value,
        },
        "conflict_case": {
            "obstruction_verified": conflict_obstruction.verify(),
            "candidate_safe_verified": conflict_candidate_safe.verify(),
            "candidate_safe_verdict": conflict_candidate_safe_verdict.kind.value,
            "set_valued_verified": conflict_set_valued.verify(),
            "set_valued_is_deterministic": conflict_set_valued.is_deterministic,
            "set_valued_verdict": conflict_set_valued_verdict.kind.value,
        },
        "joint_product_rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
