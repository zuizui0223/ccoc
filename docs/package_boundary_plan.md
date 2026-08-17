# CCOC package boundary — current tree versus history

## Governing rule

The repository has three code layers:

1. **publication core** — dependencies of the narrow open-composition paper;
2. **distinct active extensions** — results that materially change the CCOC structural premise;
3. **compatibility** — only code required by a demonstrated live current-tree consumer.

Everything else belongs in Git history by default.

## 1. Publication core

Preferred entrance:

```python
import causal_model.portability_core as rach
```

Historical registry anchors remain CORE-1 through CORE-5. Fixed-regular extremal strengthening remains active through:

- `causal_model/fixed_regular_grammar_relay.py`
- `causal_model/extremal_open_composition.py`

Do not expand the publication package to expose every follow-up theorem.

## 2. Active extensions

A module qualifies only when it contributes a distinct structural open-future result rather than another finite quotient/refinement, evidence layer, candidate-inference layer, or companion-repository theorem.

Current examples include exact converse/reuse, selected resource tradeoffs, and delimited ecological/stochastic/spatial results.

Deterministic feedback is historical after the CREST gate. Qualitative candidate, observation-panel, and benchmark modules are also historical/routed.

## 3. Package root

`causal_model/__init__.py` is intentionally minimal and has no historical API facade.

Rules:

- no new root re-exports;
- publication users import `causal_model.portability_core`;
- surviving extensions are imported explicitly by module;
- hypothetical external imports do not justify permanent retention of obsolete current-tree code;
- Git history is the recovery mechanism for historical APIs.

The old root facade was removed after its qualitative/panel consumer bundle was routed to CED/MRM and retired.

## 4. CREST routing boundary

Before adding or retaining a family:

- open-future interface noncommutation / lower bound → CCOC;
- fixed inherited-law repair → MLTR;
- retained mechanism disagreement → MRM;
- finite/noisy evidence certification, observation design, monitoring risk → CED.

Shared words such as `state`, `quotient`, `refinement`, `candidate`, or `uncertainty` do not override this ownership rule.

## 5. Deferred symbolic/certificate cluster

Do not partially dismantle the current symbolic/certificate/admission/polyhedral stack. Proof-carrying manifests currently import symbolic candidate/lifting objects. Audit the whole dependency graph first, then retain only the part that serves a real CCOC provenance/release contract.

## 6. Documentation boundary

Each active theorem family should have at most one canonical scientific entrance document plus a claim-control/prior-art document when necessary. Historical details remain in Git history rather than separate current proof notes.

## 7. Test boundary

Keep tests for active sources and explicit live compatibility/provenance contracts. Delete a dedicated test when its source bundle is retired and no frozen replay calls it.

## 8. Workflow boundary

Keep one generic full-suite matrix and specialized workflows only where they add a distinct current replay or provenance artifact. Theorem-named workflow count should fall as active theorem surfaces are retired.

## 9. Sources of truth

- `docs/current_architecture.md` — current architecture;
- `docs/core_surface_cleanup_manifest_2026-08-14.md` — executed deletion decisions;
- theorem and historical registries — executable versus archived theorem status.

Deletion from `main` is not deletion from scientific provenance.
