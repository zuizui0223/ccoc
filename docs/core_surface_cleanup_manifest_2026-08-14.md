# CCOC current-tree cleanup manifest

> **Updated 2026-08-17.** Preserve scientific conclusions and reproducibility while removing duplicate or misrouted active surfaces. Git history is the archive; the current tree does not need every historical implementation.

## 1. KEEP — publication core

Retain:

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

A follow-up stays only when it changes a structural open-future premise and is not owned by a companion repository.

Routing boundary:

- open-future lower bound / noncommutation → CCOC;
- fixed inherited-law repair → MLTR;
- retained mechanism disagreement → MRM;
- finite/noisy evidence certification / monitoring design → CED.

## 3. FEEDBACK CLEANUP — completed

Deterministic feedback is **HISTORICAL / ROUTED**. The family-level coarsest hidden repair routes to MLTR. PR #204/#205 remain historical examples only.

Retired current-tree executable surface:

- `causal_model/feedback_gate_rank.py`
- `tests/test_feedback_gate_rank.py`
- `causal_model/feedback_type_portability.py`
- `tests/test_feedback_type_portability.py`

Canonical records remain in the two feedback audit documents. Full pre-cleanup recovery pin: `4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`.

## 4. QUALITATIVE CANDIDATE / PANEL / BENCHMARK CLEANUP — completed

CREST routing classified this family as evidence/mechanism infrastructure rather than CCOC open-composition theory.

### Retired source modules

- `causal_model/admissibility.py`
- `causal_model/benchmarks.py`
- `causal_model/ecological_program.py`
- `causal_model/failure_modes.py`
- `causal_model/generative_benchmarks.py`
- `causal_model/observation_design.py`
- `causal_model/observation_envelope.py`
- `causal_model/panel_phase_benchmarks.py`
- `causal_model/replaceability.py`
- `causal_model/robust_panel_design.py`

Their dedicated regression tests, benchmark/observation experiments, example, and family-specific docs were retired with them.

### Routing

- admissibility, noisy observation, observation envelopes, panel selection, panel robustness, and benchmark/calibration logic → CED if revisited;
- retained mechanism/candidate uncertainty that changes future prediction → MRM if revisited.

No source was copied into CED or MRM because those repositories already contain their own active formulations. The exact CCOC-era bundle remains recoverable from pre-removal main commit `bbe84993a369213f1a9739dba02fbed5e780ad00`.

## 5. PACKAGE BOUNDARY — tightened

`causal_model/__init__.py` is now a minimal package marker. It does not re-export historical candidate/panel/evidence APIs.

Preferred publication API:

```python
import causal_model.portability_core as rach
```

Compatibility is retained only for a demonstrated live current-tree dependency, not hypothetical external consumers.

## 6. DEFERRED DEPENDENCY CLUSTER

The symbolic/certificate/admission/polyhedral cluster is **not** part of this cleanup wave. Current proof-carrying manifest code imports symbolic candidate/lifting objects, so this cluster must be audited as one dependency graph before removal.

Examples include:

- `symbolic_candidate_sets.py`
- `anytime_symbolic_lifting.py`
- `certificate_manifest.py`
- admission transcript / proof-carrying / polyhedral verification modules.

## 7. WORKFLOW / DOCUMENTATION BOUNDARY

Specialized workflows survive only if they supply a distinct current replay, deterministic artifact, or release/manuscript contract.

Current navigation is centered on `README.md`, `docs/current_architecture.md`, this manifest, and theorem/historical registries. Historical ledgers may name retired paths as provenance.

## 8. Cleanup safety rules

Before deleting a source bundle:

1. inspect active imports and direct path references;
2. preserve useful conclusions through existing canonical records or immutable Git history;
3. record a recovery pin;
4. retire dedicated tests/docs/examples/workflows with no independent current role;
5. run current-core/provenance validation.

A valid theorem, witness, benchmark, or ecological example is not automatically a reason to keep a current executable surface.

## 9. Next pass

Audit the symbolic/certificate/admission/polyhedral cluster and decide which parts are genuine CCOC release/provenance infrastructure versus CED-style evidence machinery.
