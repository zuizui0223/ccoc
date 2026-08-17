# CCOC current-tree cleanup manifest

> **Updated 2026-08-17.** Preserve scientific conclusions and reproducibility while removing duplicate or misrouted active surfaces. Git history is the archive; the current tree does not need every historical implementation.

## 1. KEEP — publication core

Retain the first-paper source set and fixed-regular strengthening:

- `causal_model/dynamic_boundary_blankets.py`
- `causal_model/shared_grammar.py`
- `causal_model/grammar_aware_blankets.py`
- `causal_model/extension_compression_noncommutation.py`
- `causal_model/operational_addressability.py`
- `causal_model/extension_compression.py`
- `causal_model/relay_tree_compilation.py`
- `causal_model/coherent_portable_macrolaw.py`
- `causal_model/conservative_macro_schema.py`
- `causal_model/fixed_regular_grammar_relay.py`
- `causal_model/extremal_open_composition.py`

Preserve theorem-registry and paper-core replay gates, claim/source audits, and exact source pins.

## 2. KEEP — distinct follow-up surfaces

A follow-up module stays only when it contributes a structurally distinct result rather than another spelling of fixed-grammar minimization or a result owned by a companion repository.

Apply the routing boundary:

- open-future lower bound / noncommutation → CCOC;
- fixed inherited-law repair → MLTR;
- retained mechanism disagreement → MRM;
- finite/noisy evidence certification → CED.

## 3. FEEDBACK CLEANUP — CREST gate completed

### Final verdict

The deterministic feedback family is **HISTORICAL / ROUTED**.

The family-level continuation-stable hidden repair is a coarsest stable refinement of a supplied retained partition. Under CREST §11/§12 it is not a new CCOC theorem; any further repair development routes to MLTR.

### Retired on 2026-08-17

The two previously retained representative examples no longer justify dedicated current-tree executable surfaces:

- `causal_model/feedback_gate_rank.py`
- `tests/test_feedback_gate_rank.py`
- `causal_model/feedback_type_portability.py`
- `tests/test_feedback_type_portability.py`

PR #204 remains a historical mechanism-specific future-addressability/ablation example. PR #205 remains a historical copy-anonymous five-state quotient example.

### Earlier retired implementations/tests

- `causal_model/evolving_feedback_master_types.py`
- `causal_model/future_feedback_causal_forgetting.py`
- `causal_model/state_dependent_feedback_closure.py`
- their dedicated tests;
- `experiments/feedback_network_nonreducibility.py` and its test;
- superseded exploratory and per-PR proof notes.

Canonical surviving records:

- `docs/feedback_portability_theorem_family_2026-08-15.md`
- `docs/feedback_novelty_audit_2026-08-16.md`

Full pre-cleanup recovery pin:

`4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`.

The feedback pass now demonstrates that a governance gate can remove previously preserved executable examples rather than merely relabel them.

## 4. COMPATIBILITY CLEANUP — executed / continuing

### Retired aggregate facades

No active repository code consumed these aggregates, so they were removed rather than kept indefinitely for hypothetical external imports:

- `causal_model/current_theory.py`
- `tests/test_current_theory.py`
- `causal_model/identifiability_companion.py`

### Package root still active

`causal_model/__init__.py` still serves older examples/scripts that import qualitative/panel APIs from the package root. Do not add exports. The next large pass audits those consumer families, then shrinks the facade.

## 5. WORKFLOW CLEANUP — executed where stale behavior was exposed

`tests/conftest.py` marks non-paper-core tests as `legacy`, and `pyproject.toml` excludes them from default pytest. Specialized workflows survive only when they supply a distinct replay, deterministic artifact, or release/manuscript contract.

Previously removed stale workflows include delayed-addressability, candidate-safe, joint-open-candidate, delayed-joint, and binary-joint replay jobs whose active theorem ownership had already moved or been archived.

## 6. DOCUMENTATION DEDUPLICATION — executed

Current navigation is centered on `README.md`, `docs/current_architecture.md`, this cleanup manifest, and theorem/historical registries.

Historical documents may retain former paths as provenance. A historical path is not a promise that the source remains executable in the current tree.

## 7. Cleanup safety rules

Before deleting a source bundle:

1. inspect active imports and direct path references;
2. preserve still-useful scientific conclusions in a canonical record;
3. record an immutable recovery pin;
4. remove dedicated tests/docs/workflows with no independent current role;
5. run current-core/provenance validation.

A valid theorem, witness, or ecological example is not automatically a reason to keep a dedicated executable surface.

## 8. Next pass

Audit the package-root / candidate-panel / benchmark surface.

Goal:

- reduce `causal_model/__init__.py`;
- identify duplicate candidate/panel implementations and examples;
- keep compatibility only for live current-tree consumers;
- enforce CREST routing before preserving any additional theorem family.