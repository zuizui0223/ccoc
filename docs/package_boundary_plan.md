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

Registry anchors remain CORE-1 through CORE-5. Fixed-regular extremal strengthening remains active through its explicit modules.

Do not expand the publication package to expose every follow-up theorem.

## 2. Active extensions

A module qualifies only when it contributes a distinct structural open-future result rather than another finite quotient/refinement, evidence layer, candidate-inference layer, proof-admission layer, or companion-repository theorem.

Current examples include exact converse/reuse, selected resource tradeoffs, and delimited ecological/stochastic/spatial results pending their own audit.

## 3. Package root

`causal_model/__init__.py` is a minimal package marker.

Rules:

- publication users import `causal_model.portability_core`;
- historical qualitative/panel/evidence/certificate APIs are not re-exported;
- surviving extensions are imported explicitly by module;
- hypothetical external imports and legacy tests in Git history do not justify current compatibility code;
- Git history is the recovery mechanism for historical APIs.

## 4. CREST routing boundary

Before adding or retaining a family:

- open-future interface noncommutation / lower bound → CCOC;
- fixed inherited-law repair → MLTR;
- retained mechanism disagreement → MRM;
- finite/noisy evidence certification, observation design, monitoring risk, or proof-carrying evidence admission → CED.

Shared words such as `state`, `quotient`, `refinement`, `candidate`, `certificate`, or `uncertainty` do not override this ownership rule.

## 5. Current provenance path

Current release/provenance is intentionally small:

- theorem registry + integrity verifier;
- paper-core replay;
- current structural workflows;
- immutable Git pins/history.

The former symbolic confidence/certificate/admission/polyhedral stack is historical. It had no current script/workflow/registry dependency and therefore is not a compatibility layer.

## 6. Documentation boundary

Each active theorem family should have at most one canonical scientific entrance document plus a claim-control/prior-art document when necessary. Historical details remain in Git history rather than separate current proof notes.

## 7. Test boundary

Keep tests for active sources and explicit current provenance contracts. Delete dedicated tests when their source bundle is retired; a deselected legacy test is not itself a retention reason.

## 8. Workflow boundary

Keep one generic full-suite matrix and specialized workflows only where they add a distinct current structural replay or provenance artifact. Theorem-named workflow count should fall as active surfaces are retired.

## 9. Sources of truth

- `docs/current_architecture.md` — current architecture;
- `docs/core_surface_cleanup_manifest_2026-08-14.md` — executed deletion decisions;
- theorem and historical registries — executable versus archived theorem status.

Deletion from `main` is not deletion from scientific provenance.
