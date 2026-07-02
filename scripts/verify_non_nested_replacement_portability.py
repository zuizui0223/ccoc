from __future__ import annotations

import json
from pathlib import Path

from causal_model.non_nested_conservative_transport import conservative_non_nested_replacement_witness
from causal_model.non_nested_portability import (
    non_nested_replacement_witness,
    non_nested_rewiring_obstruction,
    transported_target_projection_witness,
)


def main() -> None:
    """Write a deterministic replay for declared finite replacement transport.

    This verifies only supplied finite systems, grammar, source projections, and
    transport relations. It does not infer ecological replacement processes.
    """

    positive = non_nested_replacement_witness()
    transport = positive.transports[0]
    constructed = transported_target_projection_witness()
    conservative = conservative_non_nested_replacement_witness()
    negative = non_nested_rewiring_obstruction()

    report = {
        "theorem_domain": (
            "declared finite grammar-aware controlled systems, exact source projections, "
            "and total target-fiber-label-consistent replacement transports; target-only "
            "actions require uniform availability and macro-successor determinism"
        ),
        "claim_status": {
            "edge_preservation": "sufficient finite-domain transport-coherence criterion",
            "target_construction": (
                "sufficient finite-domain theorem constructing an exact target projection "
                "from source labels and an equal-legality transport relation"
            ),
            "conservative_target_construction": (
                "sufficient finite-domain theorem constructing one conservative macro schema "
                "when target-only actions are uniform and label-deterministic"
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
        "conservative_target_only_action": {
            "verified": conservative.verify(),
            "derived_target_labels": list(conservative.target_labels),
            "source_rows": [list(row) for row in conservative.source_stage.stage_rows()],
            "target_rows": [list(row) for row in conservative.target_stage.stage_rows()],
            "schema_transition_rows": [list(row) for row in conservative.schema.transition_rows],
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
