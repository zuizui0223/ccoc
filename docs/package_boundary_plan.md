# RACH package-boundary implementation plan

## Purpose

This document turns the existing logical split into a concrete repository rule.
It does not add a theorem. It fixes where future code, certificates, tests, and
public imports belong while preserving historical replay paths.

## The only active structural question

> When does an exact finite causal macro-law remain portable as the declared
> outside of a focal window expands?

The active theorem spine is:

1. **Exact dynamic factorization.** A finite update-consistent boundary summary
   yields an exact interface for a declared finite controlled system and grammar.
2. **Extension--compression obstruction.** A jointly realizable, independently
   decoded exterior product forces the addressable-product lower bound and, under
   closed-context factorization, the noncommutation gap.
3. **Conservative portability ladder.** Uniform boundedness, coherent law
   identity, and conservative legal-action expansion are nested sufficient
   criteria, not independent headline theories.

The relay tree is retained only as a sharpness realization of item 2.

## Package ownership

| Package | Public facade | Owns | Does not own |
|---|---|---|---|
| `portability` | `causal_model.portability_core` | dynamic blankets, grammar-aware exact quotient, addressability obstruction, noncommutation, conservative portability, sharpness witnesses | finite-evidence limitations, candidate uncertainty, measurement design |
| `identifiability` | `causal_model.identifiability_companion` | delayed exposure, adaptive finite-evidence no-go, candidate-safe and joint exterior--mechanism laws | the portability core lower bound or its positive factorization criterion |
| `legacy.experimental_design` | no new public facade | reset panels, evidence coverage, cell-loss and common-mode robustness, narrow observation protocols | closure or portability claims |
| `shared` | no direct theorem claim | finite controlled-system and prefix-grammar primitives used by more than one package | theorem-specific certificates or witnesses |

## Source-of-truth rule

- `extension_compression_noncommutation.py` is the canonical source for the
  addressable-product theorem and the Extension--Compression Noncommutation
  Inequality.
- `extension_compression.py` and `relay_tree_compilation.py` are sharpness
  witnesses only.
- `addressable_completion_bounds.py` remains a canonical finite product helper
  and passive-example compatibility module. It must not create a second public
  formulation of the main lower bound.
- `observation_window_completion.py` is a passive-evidence example and belongs
  under the identifiability narrative, not the portability narrative.

## Compatibility rule

Existing module paths remain importable until a dedicated compatibility-release
removes them. New code must import through one of the two facades:

```python
import causal_model.portability_core as rach
import causal_model.identifiability_companion as rach_id
```

`causal_model.current_theory` is historical compatibility only. It must not be
used in new theorem examples, README snippets, or new tests.

## Next implementation steps

1. Move `FinitePrefixGrammar` and `GrammarAwareControlledSystem` from the
   delayed-addressability module into a shared primitive module, retaining
   re-exports for compatibility.
2. Change `portability_core.py` to import those primitives from `shared` rather
   than from an identifiability module.
3. Mark `current_theory.py` as deprecated compatibility and replace its
   "active core" narrative with a neutral import-compatibility notice.
4. Add one operational witness API for the product theorem: it must receive an
   actual controlled system, product embedding, legal decoder words, decoders,
   and closed-context factorization map rather than merely replay cardinality
   arithmetic.
5. Keep the old arithmetic certificate as a theorem-schema replay and witness
   helper.

## Non-goals

- No new local grammar theorem.
- No new panel, robustness, coverage, or field-protocol abstraction.
- No physical repository split before shared primitives and compatibility
  imports stabilize.
