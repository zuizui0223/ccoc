# CCOC package boundary — current tree versus history

## Governing rule

The repository has three code layers:

1. **publication core** — dependencies of the narrow open-composition paper;
2. **distinct active extensions** — results that change the mathematical/ecological premise materially;
3. **compatibility shelf** — old APIs still used by repository consumers.

Everything else belongs in Git history rather than remaining an active source surface by default.

## 1. Publication core

Preferred entrance:

```python
import causal_model.portability_core as rach
```

Historical registry anchors remain CORE-1 through CORE-5. The fixed-regular extremal strengthening remains active through:

- `causal_model/fixed_regular_grammar_relay.py`
- `causal_model/extremal_open_composition.py`

Do not expand this package to expose every follow-up theorem.

## 2. Active extensions

A module qualifies as an active extension only when it contributes a distinct structural result, not merely another exact quotient/refinement of a finite deterministic system.

Active families currently include exact converse/reuse, selected resource tradeoffs, and delimited ecological/stochastic/spatial results.

Deterministic feedback has been reduced to two executable examples:

- `feedback_gate_rank.py`
- `feedback_type_portability.py`

The former PR #207/#208/#210 implementations are historical and recoverable at pre-cleanup pin `4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`.

## 3. Compatibility shelf

The package root `causal_model/__init__.py` remains a compatibility facade only because current examples/scripts still import older qualitative/panel names from it.

Rules:

- no new exports;
- migrate or retire in-repository root-import consumers;
- shrink `__init__.py` after each consumer family is removed;
- use immutable Git history for long-term historical recovery rather than preserving unused aggregate APIs forever.

The deprecated `causal_model/current_theory.py` aggregate was removed because no active repository code imported it. Its dedicated compatibility test was removed with it.

Candidate-uncertainty, observation-panel, benchmark, and experimental-design code is the next compatibility family to audit.

## 4. Documentation boundary

Each active theorem family should have at most:

- one canonical mathematical/scientific entrance document;
- one claim-control/prior-art document when necessary.

Do not keep a separate long proof note for every merged PR after the family has been consolidated. Historical details remain in Git history.

## 5. Test boundary

Keep tests for active sources and for explicit compatibility contracts.

Delete a dedicated test file when its only source was retired and no frozen replay contract still calls it.

A historical theorem does not need a permanent standalone current-tree regression if its conclusion is no longer represented by active code.

## 6. Workflow boundary

Keep one generic full-suite matrix (`tests.yml`) and distinct provenance/replay workflows only where they add a real gate or artifact.

Theorem-named workflow count should decrease as theorem-specific active surfaces are retired.

## 7. Source-of-truth rule

Current architecture is documented in `docs/current_architecture.md`.

Executed deletion decisions are recorded in `docs/core_surface_cleanup_manifest_2026-08-14.md`.

Historical results that are removed from the current tree remain recoverable from immutable commits/merged PRs; deletion from `main` is not deletion from scientific provenance.
