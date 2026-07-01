"""Write a deterministic certificate-replay report for grammar-aware blankets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.delayed_addressability import FinitePrefixGrammar, GrammarAwareControlledSystem
from causal_model.dynamic_boundary_blankets import FiniteControlledOutputSystem
from causal_model.grammar_aware_blankets import (
    GrammarAwareDynamicInterfaceCertificate,
    certify_grammar_aware_canonical_interface,
    certify_grammar_aware_dynamic_blanket,
    certify_grammar_state_necessity,
    constant_output_delayed_system,
    explicit_grammar_aware_partition,
)


def full_action_grammar(actions: tuple[str, ...]) -> FinitePrefixGrammar:
    return FinitePrefixGrammar(actions=actions, transition_table=(tuple(0 for _ in actions),))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-delay", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_delay < 1:
        raise ValueError("max-delay must be positive")

    delayed_rows = []
    for delay in range(1, args.max_delay + 1):
        constrained = constant_output_delayed_system(delay)
        summary = tuple(grammar_state for _, grammar_state in constrained.product_states)
        canonical = certify_grammar_aware_canonical_interface(constrained)
        blanket = certify_grammar_aware_dynamic_blanket(constrained, summary)
        necessity = certify_grammar_state_necessity(delay)
        explicit_match = all(
            constrained.product_partition(horizon) == explicit_grammar_aware_partition(constrained, horizon)
            for horizon in range(delay + 3)
        )
        delayed_rows.append(
            {
                "delay": delay,
                "grammar_state_count": constrained.grammar.state_count,
                "canonical_block_count": canonical.canonical_block_count,
                "initial_slice_block_count": canonical.initial_slice_block_count,
                "stabilization_horizon": canonical.stabilization_horizon,
                "summary_block_count": blanket.summary_block_count,
                "explicit_trace_partition_match": explicit_match,
                "necessity_verified": necessity.verify(),
                "blanket_verified": blanket.verify(),
            }
        )

    system = FiniteControlledOutputSystem(
        actions=("step",),
        transition_table=((1,), (0,)),
        outputs=(0, 1),
    )
    unconstrained = GrammarAwareControlledSystem(system, full_action_grammar(("step",)))
    unconstrained_canonical = certify_grammar_aware_canonical_interface(unconstrained)

    report = {
        "theorem_domain": "finite deterministic controlled output systems under finite deterministic prefix-closed grammars",
        "claims": [
            "output, enabled-action, and enabled-successor agreement define an exact grammar-aware dynamic interface",
            "the stable legal-word quotient is the coarsest such interface",
            "a finite grammar-aware blanket upper-bounds canonical interface memory and the refinement horizon",
            "grammar state can be necessary even with constant physical state and output",
        ],
        "delayed_constant_rows": delayed_rows,
        "one_state_full_grammar_case": {
            "canonical_block_count": unconstrained_canonical.canonical_block_count,
            "verified": unconstrained_canonical.verify(),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
