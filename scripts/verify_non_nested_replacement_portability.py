from __future__ import annotations

import json
from pathlib import Path

from causal_model.non_nested_portability import (
    non_nested_replacement_witness,
    non_nested_rewiring_obstruction,
    transported_target_projection_witness,
)


def main() -> None:
    """Write a deterministic replay for declared finite replacement transport.

    This verifies only the supplied finite systems, grammar, source projection,
    and transport relation. It does not infer ecological replacement processes.
    """

    positive = non_nested_replacement_witness()
    transport = positive.transports[0]
    constructed = transported_target_projection_witness()
    negative = non_nested_rewiring_obstruction()

    report = {
        "theorem_domain": (
            "declared finite grammar-aware controlled systems, an exact source projection, "
            "and a total target-fiber-label-consistent, output/legal-action-preserving, "
            "successor-closed replacement transport"
        ),
        "claim_status": {
            "edge_preservation": "sufficient finite-domain transport-coherence criterion",
            "target_construction": (
                "sufficient finite-domain theorem constructing an exact target projection "
                "from source labels and a transport relation"
            ),
            "negative": "local obstruction to one carried merge",
            "non_claim": (
                "failure to supply a transport certificate does not establish cumulative "
                "addressability, unbounded memory, or failure of every alternative macro-law"
            ),
        },
        "positive_replacement_witness": {
            "verified": positive.verify(),
            "macro_outputs": list(positive.macro.outputs),
            "macro_transition_rows": [list(row) for row in positive.macro.transition_rows],
            "source_product_state_count": transport.source.constrained_system.product_state_count,
            "target_product_state_count": transport.target.constrained_system.product_state_count,
            "relation": [list(pair) for pair in transport.relation],
            "source_to_target_injective": transport.is_source_injective,
            "transport_verified": transport.verify(),
        },
        "constructed_target_projection": {
            "verified": constructed.verify(),
            "derived_target_labels": list(constructed.target_labels),
            "target_macro_equals_source_macro": (
                constructed.target_projection.induced_macro() == constructed.source.induced_macro()
            ),
            "target_labels_were_input": False,
        },
        "newly_legal_word_obstruction": {
            "verified": negative.verify(),
            "future_word": list(negative.future_word),
            "source_product_state_count": negative.source.constrained_system.product_state_count,
            "target_product_state_count": negative.target_system.product_state_count,
            "carried_pair": [negative.left_source_index, negative.right_source_index],
            "proposed_label": negative.proposed_target_labels[
                dict(negative.relation)[negative.left_source_index]
            ],
        },
    }

    output = Path("artifacts/non_nested_replacement_portability_report.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
