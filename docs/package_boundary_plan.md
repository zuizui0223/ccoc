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
- `operational_addressability.py` is the canonical finite **application** layer:
  it verifies a supplied controlled system, product embedding, decoder words,
  decoder functions, and finite closed-context factor maps.
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

`causal_model.current_theory` is a deprecated historical compatibility aggregate.
It may be used to replay old notebooks and certificates, but it must not be used
in new theorem examples, README snippets, or new tests.

## Implementation status

Completed:

1. `FinitePrefixGrammar` and `GrammarAwareControlledSystem` now live in
   `shared_grammar.py`; historical delayed-addressability imports remain intact.
2. `portability_core.py` now imports these neutral primitives from `shared` rather
   than from an identifiability module.
3. The operational product certificate now checks an actual finite controlled
   system, injective product embedding, legal decoder words, decoder functions,
   and explicit finite closed-context factor maps. The former cardinality-only
   certificate remains a theorem-schema replay and witness helper.
4. `current_theory.py` is now a warning-emitting historical aggregate. It retains
   prior theorem-facing symbols but no longer describes itself as an active core
   or a single theorem chain.

Still pending:

1. Add an optional reachability contract only when a chosen theorem application
   needs one. The present operational certificate verifies the supplied embedded
   subsystem; it does not infer reachability from an unstated initial condition.
2. Do not physically split repositories before shared primitives and compatibility
   imports stabilize.

## Non-goals

- No new local grammar theorem.
- No new panel, robustness, coverage, or field-protocol abstraction.
- No claim that an arbitrary empirical system satisfies a supplied product
  embedding, legal-word family, or boundary grammar.
