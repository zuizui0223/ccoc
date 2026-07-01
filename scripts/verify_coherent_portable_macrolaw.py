from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.coherent_portable_macrolaw import inert_portable_chain, newly_legal_word_obstruction


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-module-count", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_module_count < 1:
        raise ValueError("max-module-count must be positive")

    rows = []
    for maximum in range(1, args.max_module_count + 1):
        certificate = inert_portable_chain(maximum)
        rows.append(
            {
                "maximum_module_count": maximum,
                "physical_state_counts": [stage.constrained_system.system.state_count for stage in certificate.stages],
                "macro_state_count": certificate.macro.state_count,
                "embedding_count": len(certificate.embeddings),
                "verified": certificate.verify(),
            }
        )
    obstruction = newly_legal_word_obstruction()
    report = {
        "theorem_domain": "nested finite grammar-aware controlled systems with trajectory-preserving embeddings",
        "claims": [
            "one common output/legal-action/transition system plus label-coherent embeddings yields one portable macro-law",
            "a common label alphabet alone is insufficient",
            "a newly legal future word that separates a proposed merged old pair is a concrete portability obstruction",
        ],
        "coherent_inert_chains": rows,
        "future_word_obstruction": {
            "word": obstruction.future_word,
            "source_pair": [obstruction.left_source_index, obstruction.right_source_index],
            "verified": obstruction.verify(),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
