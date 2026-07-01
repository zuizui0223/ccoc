from __future__ import annotations

import json
from pathlib import Path

from causal_model.conservative_macro_schema import (
    conservative_reveal_chain,
    newly_legal_action_merge_obstruction,
)


def main() -> None:
    chain = conservative_reveal_chain()
    obstruction = newly_legal_action_merge_obstruction()
    report = {
        "theorem_domain": "nested finite grammar-aware systems with fixed finite action alphabet and monotone legal-action expansion",
        "claims": [
            "stage legal rows may expand while old macro successors remain fixed",
            "a newly legal action is portable only when label-deterministic",
            "a pair/action conflict is a concrete obstruction to conservative portability",
        ],
        "conservative_reveal_chain": {
            "schema_outputs": chain.schema.outputs,
            "schema_transition_rows": chain.schema.transition_rows,
            "stage_rows": [stage.stage_rows() for stage in chain.stages],
            "embedding_count": len(chain.embeddings),
            "verified": chain.verify(),
        },
        "new_action_obstruction": {
            "action": obstruction.newly_legal_action,
            "pair": [obstruction.left_index, obstruction.right_index],
            "proposed_label": obstruction.proposed_labels[obstruction.left_index],
            "verified": obstruction.verify(),
        },
    }
    output = Path("artifacts/conservative_macro_schema_report.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
