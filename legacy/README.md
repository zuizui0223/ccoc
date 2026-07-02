# Legacy shelf: non-publication RACH branches

## Purpose

This shelf preserves finite results that are **not part of the current
open-composition manuscript**. They are retained for historical replay,
comparison, and possible later promotion; they are not deleted and are not being
called false.

The active paper asks one question only:

> When does exact compression in each fixed closed composition fail to extend to one small exact interface for a declared open composition grammar?

The active source package is therefore limited to:

1. exact grammar-aware interfaces;
2. operational-addressability and extension--compression noncommutation;
3. the bounded-degree relay sharpness witness; and
4. conservative macro schemas and local fiber-split boundary.

## Compatibility-preserving migration

The original Python module paths remain temporarily importable so old notebooks,
certificate replays, and commit-pinned artifacts do not break during manuscript
preparation. Their **research status**, documentation entry point, public API
status, and active CI priority have moved here.

A physical module-path move is deferred until after a tagged manuscript source
release. At that point legacy modules can be placed under `causal_model.legacy`
with forwarding shims or a breaking compatibility release. This avoids changing
both proof scope and import semantics in the same pre-submission revision.

## Archived branches

| Archive group | Registry IDs | Source families retained | Why it is outside the paper |
|---|---|---|---|
| Finite closure prerequisite | `CORE-0` | `causal_closure_calculus.py` | Classifies a supplied finite update map; it is not needed for the open-composition theorem or its sharpness family. |
| Non-nested replacement and rewiring | `EXT-1`--`EXT-4` | `non_nested_portability.py`, `non_nested_conservative_transport.py` | A useful future extension, but adding replacement relations would create a second composition theorem in the current manuscript. |
| Finite-evidence and delayed-exposure companions | `ID-1` | `delayed_addressability.py`, `adaptive_closure_no_go.py`, observation-window modules | Asks what finite evidence can establish, rather than when a declared open grammar forces memory growth. |
| Candidate-mechanism companions | `ID-2`, `ID-3` | `candidate_safe_laws.py`, `joint_open_candidate_laws.py` | Adds mechanism uncertainty to exterior uncertainty; not a premise of the central lower bound. |
| Experimental-design shelf | `LEGACY-1` | reset panels, evidence coverage, cell-loss and common-mode branches | Conditional measurement/design questions after a structural quotient is already fixed. |
| Historical aggregates and examples | no active registry ID | `current_theory.py`, old examples, experiments, benchmark scripts | Retained only for reproducibility and development history. |

## Rules

1. Do not add features, theorem variants, examples, workflows, or README claims to
   this shelf during manuscript preparation.
2. A legacy result may be cited in the Supplement only as a scope boundary or a
   future-work pointer; it does not become a second headline theorem.
3. Re-promotion requires a concrete statement of which manuscript assumption or
   conclusion changes. A useful application story alone is not enough.
4. A failing legacy replay is recorded and repaired on a legacy branch; it does
   not expand the paper's mathematical claim.
5. The paper source must pin a RACH commit or release hash and identify exactly
   which `CORE-*` assets it relies on.

## Paper-core verification set

The active reproducibility gate comprises only these finite paths:

```text
causal_model/dynamic_boundary_blankets.py
causal_model/shared_grammar.py
causal_model/grammar_aware_blankets.py
causal_model/extension_compression_noncommutation.py
causal_model/operational_addressability.py
causal_model/extension_compression.py
causal_model/relay_tree_compilation.py
causal_model/coherent_portable_macrolaw.py
causal_model/conservative_macro_schema.py
```

The corresponding active theorem IDs are `CORE-1` through `CORE-5`, with
`CORE-4` restricted in the manuscript to the conservative-schema sufficient
criterion and `CORE-5` to the local new-action fiber-split boundary.
