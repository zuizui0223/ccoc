# Legacy migration manifest

This manifest is the compatibility-preserving migration record for manuscript
preparation. `active` means part of the open-composition paper's proof or
reproducibility package. `legacy` means retained but excluded from the paper's
main theorem package.

## Active paper core

| ID / role | Canonical source | Verification focus |
|---|---|---|
| `CORE-1` exact interface | `causal_model/dynamic_boundary_blankets.py`, `causal_model/shared_grammar.py`, `causal_model/grammar_aware_blankets.py` | output, legal-action, and successor preservation |
| `CORE-2` noncommutation | `causal_model/extension_compression_noncommutation.py`, `causal_model/operational_addressability.py` | uniform decoder words, product injection, closed-factorization upper bound |
| `CORE-3` sharpness | `causal_model/extension_compression.py`, `causal_model/relay_tree_compilation.py` | bounded degree, local grammar, macro-time conjugacy |
| `CORE-4` positive boundary | `causal_model/coherent_portable_macrolaw.py`, `causal_model/conservative_macro_schema.py` | conservative macro schema |
| `CORE-5` local negative boundary | `causal_model/coherent_portable_macrolaw.py`, `causal_model/conservative_macro_schema.py` | future-word / new-action fiber split |

## Legacy now

| Registry group | Source paths | Documentation / replay paths |
|---|---|---|
| `CORE-0` | `causal_model/causal_closure_calculus.py` | `tests/test_causal_closure_calculus.py`, `docs/claim_status_audit.md` |
| `EXT-1`--`EXT-4` | `causal_model/non_nested_portability.py`, `causal_model/non_nested_conservative_transport.py` | `tests/test_non_nested_portability.py`, `tests/test_non_nested_conservative_transport.py`, `docs/non_nested_replacement_portability.md`, `scripts/verify_non_nested_replacement_portability.py` |
| `ID-1` | `causal_model/delayed_addressability.py`, `causal_model/adaptive_closure_no_go.py`, `causal_model/observation_window_completion.py`, `causal_model/observation_regime_closure.py`, `causal_model/addressable_completion_bounds.py` | delayed / observation tests, docs, and replays |
| `ID-2`, `ID-3` | `causal_model/candidate_safe_laws.py`, `causal_model/joint_open_candidate_laws.py` | candidate / joint-law tests, docs, and replays |
| `LEGACY-1` | panel, coverage, failure-mode, and experimental-design families | `docs/legacy/README.md` and linked historical replays |
| historical facade | `causal_model/current_theory.py`, `causal_model/identifiability_companion.py` | retained only to keep old imports and notebooks replayable |

## Root-interface rule

- `README.md` and `causal_model.portability_core` expose only the active paper core.
- `causal_model.identifiability_companion` remains importable but is not a public
  entrance for this manuscript.
- `causal_model.current_theory` remains a deprecated compatibility aggregate.
- The complete registry is retained as provenance, not as a list of current paper
  claims.

## Later physical move

After a permanent RACH source tag is created for the paper, move legacy source
families to `causal_model/legacy/`, move their tests to `legacy/tests/`, move
replays to `legacy/scripts/`, and retain only deprecation shims at old paths.
That change is intentionally deferred so the pre-submission source tag does not
simultaneously alter theorem scope and external import semantics.
