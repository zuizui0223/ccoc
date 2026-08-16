# CCOC current-tree cleanup manifest

> **Updated 2026-08-16.** The cleanup goal is to preserve scientific conclusions and reproducibility while removing duplicate active surfaces. Git history is the archive; the current tree is not required to contain every historical implementation.

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

Preserve theorem registry, paper-core replay, claim-status controls, source audits, and exact source pins.

## 2. KEEP — distinct follow-up surfaces

Keep a follow-up module only when it contributes a structurally distinct result rather than another spelling of fixed-grammar minimization.

Current examples include:

- exact converse/reuse modules;
- resource/installation-time distinctions;
- genuinely distinct stochastic, cross-guild, and spatial structural results;
- two representative deterministic feedback examples described below.

## 3. FEEDBACK CLEANUP — executed

### Active feedback code retained

- `causal_model/feedback_gate_rank.py` — strongest mechanism-specific negative witness with causal-arrow ablation;
- `causal_model/feedback_type_portability.py` — strongest positive closed-form example with replication-independent five-state quotient.

Their focused tests remain.

### Retired feedback implementations

Removed from the current tree because they are progressively more general/specialized versions of the same classical future-response refinement substrate:

- `causal_model/evolving_feedback_master_types.py`
- `causal_model/future_feedback_causal_forgetting.py`
- `causal_model/state_dependent_feedback_closure.py`

Their three dedicated test files were removed with them.

### Retired exploratory surface

The initial feedback-network nonreducibility experiment was superseded by the scalable feedback-gate rank construction, so the following were removed:

- `experiments/feedback_network_nonreducibility.py`
- `tests/test_feedback_network_triage.py`
- `docs/feedback_network_candidate_triage_2026-08-14.md`

### Retired duplicate feedback proof notes

The five per-PR detailed feedback documents were removed after their durable scientific conclusions were compressed into:

- `docs/feedback_portability_theorem_family_2026-08-15.md`
- `docs/feedback_novelty_audit_2026-08-16.md`

The complete pre-cleanup code and proof notes remain recoverable at:

`4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`.

## 4. COMPATIBILITY CLEANUP — started

### `current_theory.py` — retired

The deprecated `causal_model/current_theory.py` aggregate had no active in-repository import consumer. Its references were limited to its own compatibility test and historical documentation.

Removed:

- `causal_model/current_theory.py`
- `tests/test_current_theory.py`

The aggregate remains recoverable from the pre-cleanup Git pin.

### Package root — still active compatibility surface

`causal_model/__init__.py` exposes a large pre-CCOC qualitative/panel API. Current examples/scripts still import names from the package root, so it is not yet removable.

Do not add exports. Next pass should audit the root-import consumer families and either migrate or retire them, then shrink the facade.

### Candidate/panel/benchmark family — next target

Observation design, candidate uncertainty, panel selection, confidence lifting, and benchmark modules predate the narrow open-composition theorem spine. Audit them as a family rather than retaining them automatically because they have tests.

## 5. WORKFLOW CLEANUP — executed where stale behavior was exposed

`tests.yml` is the generic Python 3.10/3.11/3.12 gate. `theorem-registry.yml` is a distinct provenance gate.

`tests/conftest.py` marks every non-paper-core test as `legacy`, while `pyproject.toml` globally runs `pytest -m 'not legacy'`. Several old theorem-specific workflows nevertheless invoked a single legacy test file without overriding that marker. After `current_theory.py` was removed, those workflows were triggered by the deleted compatibility-test path and failed with pytest exit code 5 because zero tests were collected.

Those workflows were stale rather than evidence of a broken current core, so the following were removed instead of restoring the retired facade:

- `.github/workflows/delayed-addressability.yml`
- `.github/workflows/candidate-safe-laws.yml`
- `.github/workflows/joint-open-candidate-laws.yml`
- `.github/workflows/delayed-joint-nonidentifiability.yml`
- `.github/workflows/binary-joint-relay.yml`

A specialized workflow now survives only if it provides at least one of:

1. a correctly configured legacy gate that explicitly runs legacy tests;
2. a deterministic artifact/replay not produced elsewhere;
3. a frozen release/manuscript contract.

Do not retain theorem-named workflows solely because the corresponding historical theorem once had a dedicated module.

## 6. Cleanup safety rules

Before deleting a source file:

1. search in-repository imports and direct path references;
2. identify the scientific conclusion that must survive;
3. place that conclusion in a canonical current document if it is still relevant;
4. record a recoverable Git pin for full historical code/proof;
5. remove dedicated tests/docs/workflows that have no remaining active source.

Green CI validates the current executable surface; Git history supplies archival reversibility.

## 7. Next pass

Audit the old package-root / candidate-panel / benchmark surface.

Goal:

- reduce the broad `causal_model/__init__.py` facade;
- identify duplicate candidate/panel implementations;
- keep one canonical compatibility route where still necessary;
- retire source/test/doc/workflow bundles that no longer serve the publication core, a distinct extension, or a live compatibility consumer.
