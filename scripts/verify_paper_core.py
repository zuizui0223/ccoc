"""Replay the finite theorem witnesses used by the open-composition paper.

This script is intentionally narrower than the full historical repository.  It
replays one finite instance for exact-interface semantics and operational
addressability, then checks the binary sharpness family and the positive/local
negative conservative-schema boundary.  It is reproducibility evidence for the
declared finite objects; it is not a substitute for the symbolic proofs in the
manuscript.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
from pathlib import Path
from typing import Any

from causal_model.coherent_portable_macrolaw import inert_portable_chain, newly_legal_word_obstruction
from causal_model.conservative_macro_schema import conservative_reveal_chain, newly_legal_action_merge_obstruction
from causal_model.extension_compression_noncommutation import exhaustive_noncommutation_summary
from causal_model.grammar_aware_blankets import (
    certify_grammar_aware_canonical_interface,
    certify_grammar_aware_refinement,
)
from causal_model.operational_addressability import (
    certify_canonical_operational_product,
    certify_operational_closed_context_factorization,
    standard_closed_projection,
)
from causal_model.relay_tree_compilation import exhaustive_compilation_summary


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "artifacts" / "paper_core_reproducibility_report.json"


def _assert_verified(value: Any, name: str) -> None:
    verifier = getattr(value, "verify", None)
    if not callable(verifier) or not verifier():
        raise AssertionError(f"{name} did not verify")


def build_report() -> dict[str, Any]:
    """Replay every finite witness that the manuscript cites as executable evidence."""
    # CORE-4 gives a two-stage grammar-aware controlled system.  Its second stage
    # is a compact concrete instance for CORE-1's canonical-interface theorem.
    conservative_chain = conservative_reveal_chain()
    _assert_verified(conservative_chain, "conservative reveal chain")
    exact_stage = conservative_chain.stages[-1]
    canonical_interface = certify_grammar_aware_canonical_interface(exact_stage.constrained_system)
    refinement = certify_grammar_aware_refinement(
        exact_stage.constrained_system,
        exact_stage.summary_labels,
    )
    _assert_verified(canonical_interface, "canonical exact interface")
    _assert_verified(refinement, "exact-interface refinement")

    # CORE-2: actual controlled finite system with decoders that recover each
    # coordinate independently of every other coordinate setting.
    operational = certify_canonical_operational_product(
        inside_cardinality=2,
        exterior_cardinalities=(2, 3),
    )
    _assert_verified(operational, "operational addressable product")
    closed = certify_operational_closed_context_factorization(
        open_certificate=operational,
        closed_words=(
            ((), operational.inside_word, operational.exterior_words[0]),
            ((), operational.inside_word, operational.exterior_words[1]),
        ),
        closed_factor_maps=(
            standard_closed_projection(0),
            standard_closed_projection(1),
        ),
    )
    _assert_verified(closed, "declared finite closed-context factorization")

    # CORE-3: the theorem-schema and relay implementation agree for the first six
    # binary family members.  This is an exhaustive finite replay of each member,
    # not a proof of the all-m theorem.
    noncommutation_family = exhaustive_noncommutation_summary(6)
    relay_family = exhaustive_compilation_summary(6)
    for certificate in noncommutation_family:
        _assert_verified(certificate, f"noncommutation family m={certificate.module_count}")
    for certificate in relay_family:
        _assert_verified(certificate, f"relay family m={certificate.module_count}")

    # CORE-4/5: one finite positive conservative expansion and two local negative
    # certificates (a future word and a newly legal action) establish the paper's
    # constructive boundary without claiming necessity.
    inert_chain = inert_portable_chain(4)
    future_word_obstruction = newly_legal_word_obstruction()
    new_action_obstruction = newly_legal_action_merge_obstruction()
    _assert_verified(inert_chain, "coherent inert chain")
    _assert_verified(future_word_obstruction, "future-word obstruction")
    _assert_verified(new_action_obstruction, "new-action obstruction")

    return {
        "schema_version": 1,
        "source": {
            "git_sha": os.environ.get("GITHUB_SHA", "local-unpinned"),
            "python": platform.python_version(),
        },
        "scope": {
            "model_class": "declared finite deterministic controlled systems",
            "proof_status": "finite replay and regression evidence; symbolic theorem proofs remain manuscript obligations",
            "product_object": "declared product-indexed subset of states; this replay does not infer reachability from an initial condition",
            "closed_contract": "the operational closed-context witness enumerates its complete declared finite word family",
        },
        "core_1_exact_interface": {
            "canonical_blocks": canonical_interface.canonical_block_count,
            "stabilization_horizon": canonical_interface.stabilization_horizon,
            "refinement_verified": refinement.verify(),
        },
        "core_2_operational_addressability": {
            "inside_cardinality": operational.inside_cardinality,
            "exterior_cardinalities": list(operational.exterior_cardinalities),
            "product_state_count": operational.product_state_count,
            "open_bits_lower_bound": operational.open_bits_lower_bound,
            "checked_distinct_pairs": operational.checked_distinct_pairs,
            "closed_factor_label_counts": list(closed.factor_label_counts),
            "closed_upper_bits": list(closed.closed_interface_upper_bits),
            "gap_lower_bound": closed.noncommutation_gap_lower_bound,
        },
        "core_3_binary_sharpness": [
            {
                "module_count": certificate.module_count,
                "closed_bits": certificate.closed_bits,
                "open_bits": certificate.open_bits,
                "gap_bits": certificate.gap_bits,
                "maximum_degree": certificate.relay_compilation.grammar.maximum_degree,
            }
            for certificate in noncommutation_family
        ],
        "core_3_relay_replay": [
            {
                "module_count": certificate.module_count,
                "open_interface_bits": certificate.open_interface_bits,
                "closed_interface_bits": list(certificate.closed_interface_bits),
                "maximum_degree": certificate.grammar.maximum_degree,
            }
            for certificate in relay_family
        ],
        "core_4_5_portability_boundary": {
            "inert_chain_stage_count": len(inert_chain.stages),
            "conservative_schema_state_count": conservative_chain.schema.state_count,
            "future_word_obstruction_verified": future_word_obstruction.verify(),
            "new_action_obstruction_verified": new_action_obstruction.verify(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true", help="write the deterministic JSON report under artifacts/")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
