# CCOC current-tree cleanup manifest

> **Updated 2026-08-16.** Preserve scientific conclusions and reproducibility while removing duplicate active surfaces. Git history is the archive; the current tree does not need every historical implementation.

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

A follow-up module stays only when it contributes a structurally distinct result rather than another spelling of fixed-grammar minimization. Current examples include exact converse/reuse, selected resource tradeoffs, delimited stochastic/cross-guild/spatial results, and the two representative feedback examples below.

## 3. FEEDBACK CLEANUP — executed

### Active code retained

- `causal_model/feedback_gate_rank.py` — mechanism-specific negative witness with causal-arrow ablation;
- `causal_model/feedback_type_portability.py` — replication-independent five-state positive example.

### Retired implementations/tests

- `causal_model/evolving_feedback_master_types.py`
- `causal_model/future_feedback_causal_forgetting.py`
- `causal_model/state_dependent_feedback_closure.py`
- their three dedicated tests.

### Retired exploratory surface

- `experiments/feedback_network_nonreducibility.py`
- `tests/test_feedback_network_triage.py`
- `docs/feedback_network_candidate_triage_2026-08-14.md`

### Retired duplicate proof notes

Five per-PR feedback proof documents were replaced by:

- `docs/feedback_portability_theorem_family_2026-08-15.md`
- `docs/feedback_novelty_audit_2026-08-16.md`

Full pre-cleanup recovery pin:

`4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`.

## 4. COMPATIBILITY CLEANUP — executed / continuing

### Retired aggregate facades

No active repository code consumed these aggregates, so they were removed rather than kept indefinitely for hypothetical external imports:

- `causal_model/current_theory.py`
- `tests/test_current_theory.py`
- `causal_model/identifiability_companion.py`

Underlying ID-1–3 modules remain temporarily because the current theorem-registry verifier requires every registered source/test/document path to exist.

### Package root still active

`causal_model/__init__.py` still serves old examples/scripts that import qualitative/panel APIs from the package root. Do not add exports. The next large pass audits those consumer families, then shrinks the facade.

## 5. WORKFLOW CLEANUP — executed where stale behavior was exposed

`tests/conftest.py` marks non-paper-core tests as `legacy`, and `pyproject.toml` excludes them from default pytest. Several old theorem workflows nevertheless invoked one legacy test file without `-m legacy`; after deletion of `test_current_theory.py`, they failed with exit code 5 because zero tests were collected.

Removed stale workflows:

- `.github/workflows/delayed-addressability.yml`
- `.github/workflows/candidate-safe-laws.yml`
- `.github/workflows/joint-open-candidate-laws.yml`
- `.github/workflows/delayed-joint-nonidentifiability.yml`
- `.github/workflows/binary-joint-relay.yml`

Obsolete `test_current_theory.py` path triggers were also removed from the surviving dynamic-blanket and grammar-interface replay workflows.

A specialized workflow now survives only if it correctly supplies a distinct legacy replay, deterministic artifact, or frozen release/manuscript contract.

## 6. DOCUMENTATION DEDUPLICATION — executed

Current navigation is now centered on `README.md`, `docs/current_architecture.md`, the cleanup manifest, and theorem/legacy registries.

Removed duplicate or superseded navigation documents:

- `legacy/README.md` — duplicated the legacy manifest and obsolete deferred-move policy;
- `docs/repository_asset_map.md` — duplicated architecture/package-boundary state and still advertised retired facades.

`docs/legacy/README.md` remains only as the documentation path required by the current `LEGACY-1` registry entry and has been reduced to a compatibility note.

## 7. Cleanup safety rules

Before deleting a source bundle:

1. search active imports and direct path references;
2. preserve any still-useful scientific conclusion in a canonical current record;
3. record an immutable recovery pin;
4. remove dedicated tests/docs/workflows with no independent current role;
5. run current-core/provenance validation.

## 8. Next pass

Audit the package-root / candidate-panel / benchmark surface.

Goal:

- reduce `causal_model/__init__.py`;
- identify duplicate candidate/panel implementations and examples;
- keep compatibility only for live current-tree consumers;
- prepare a separate registry-aware migration for `CORE-0`, `EXT-*`, `ID-*`, and `LEGACY-1` rather than mixing registry redesign into this PR.
