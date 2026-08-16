# Legacy / historical source manifest

This manifest distinguishes the current paper core from theorem branches that are historical or companion material. The current cleanup policy uses immutable Git history as the long-term archive; a historical result does not automatically require its source, test, docs, and workflow to remain in the current tree.

Pre-cleanup recovery pin:

`4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`

## Active paper core

| ID / role | Canonical source | Verification focus |
|---|---|---|
| `CORE-1` exact interface | `causal_model/dynamic_boundary_blankets.py`, `causal_model/shared_grammar.py`, `causal_model/grammar_aware_blankets.py` | output, legal-action, successor preservation |
| `CORE-2` noncommutation | `causal_model/extension_compression_noncommutation.py`, `causal_model/operational_addressability.py` | operational separation, open lower bound, closed factorization |
| `CORE-3` sharpness | `causal_model/extension_compression.py`, `causal_model/relay_tree_compilation.py`, fixed-regular strengthening | bounded-local extremal realization |
| `CORE-4` positive boundary | `causal_model/coherent_portable_macrolaw.py`, `causal_model/conservative_macro_schema.py` | conservative macro schema |
| `CORE-5` local negative boundary | `causal_model/conservative_macro_schema.py` | future-word / new-action fiber split |

## Historical / companion families

| Registry group | Scientific status | Current-tree policy |
|---|---|---|
| `CORE-0` | finite closure prerequisite | historical substrate; retain only while a live provenance contract requires source |
| `EXT-1`–`EXT-4` | replacement/rewiring transport | active successor is the dedicated EXT repository; CCOC copies are provenance candidates for retirement |
| `ID-1` | delayed exposure / finite-evidence limits | companion/legacy; not part of paper core |
| `ID-2`, `ID-3` | candidate-safe and joint mechanism laws | companion/legacy; not part of paper core |
| `LEGACY-1` | panel, coverage, failure-mode, benchmark, experimental-design families | historical compatibility shelf; next large cleanup target |

## Retired compatibility facades

The following aggregate facades had no active in-repository code consumers and were removed from the current tree:

- `causal_model/current_theory.py`
- `causal_model/identifiability_companion.py`

Their former exports and exact implementations remain available at the pre-cleanup Git pin.

The package root `causal_model/__init__.py` still exists because current examples/scripts import older qualitative/panel names from it. It is the remaining compatibility facade to shrink.

## Deterministic feedback cleanup

The former PR #204/#205/#207/#208/#210 five-module family is no longer one active theorem surface.

Current executable representatives:

- `causal_model/feedback_gate_rank.py`
- `causal_model/feedback_type_portability.py`

PR #207/#208/#210 implementations and duplicate proof notes were retired after their scientific conclusions were consolidated in `docs/feedback_portability_theorem_family_2026-08-15.md`. The general continuation-refinement theorem is classical fixed-grammar minimization substrate.

## Workflow rule

Generic current-tree verification is provided by `tests.yml` plus theorem-registry/paper-core provenance gates.

A historical theorem-specific workflow remains only when it correctly provides a distinct legacy replay, deterministic artifact, or frozen release contract. Workflows that invoked legacy tests while the global pytest policy excluded them were retired rather than repaired solely to preserve historical CI surface.

## Cleanup rule

For a legacy family, remove its current-tree source bundle when all of the following hold:

1. no publication-core dependency exists;
2. no active in-repository consumer requires the API;
3. the surviving scientific conclusion is recorded in a canonical document/registry entry;
4. a Git pin gives exact recovery of the historical implementation;
5. associated tests/docs/workflows have no independent current role.

The next audit target is the candidate/panel/benchmark family and the remaining package-root exports.
