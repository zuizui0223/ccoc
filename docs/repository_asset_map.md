# RACH asset map: portability core, identifiability companion, and legacy shelf

Read [portability core v1](portability_core_v1.md) before extending any module.
Read [the package-boundary implementation plan](package_boundary_plan.md) before
moving an asset or changing a public import.

This map answers one practical question:

> **Which assets may receive active theorem work, and which assets are frozen?**

## Classification rule

An asset belongs to the portability core only when it changes one of the
canonical structural claims:

\[
\text{exact factorization},
\quad
\text{addressability obstruction},
\quad
\text{or conservative portability under composition}.
\]

An identifiability asset asks what finite evidence or retained mechanism families
can justify. A legacy asset is mathematically valid but begins only after a
structural contract has already been fixed.

## A. Portability core

Use the stable public facade:

```python
import causal_model.portability_core as rach
```

| Asset | Present role |
|---|---|
| `causal_closure_calculus.py` | finite-model prerequisite: closure / recurrence / multistability |
| `shared_grammar.py` | shared finite prefix-grammar and controlled-system contract primitives; no theorem claim by itself |
| `dynamic_boundary_blankets.py` | exact update-closed finite boundary summary |
| `grammar_aware_blankets.py` | exact factorization over physical state × declared grammar state |
| `extension_compression_noncommutation.py` | **canonical** operational addressability lower bound and noncommutation inequality |
| `extension_compression.py` | binary coordinate sharpness witness |
| `relay_tree_compilation.py` | constant-grammar, pairwise, degree-three sharpness realization |
| `compositional_boundedness.py` | boundedness versus cumulative growth criteria across nested stages |
| `coherent_portable_macrolaw.py` | same macro law under label-coherent nested embeddings |
| `conservative_macro_schema.py` | safe monotone legal-action expansion and fiber-split obstruction |
| `portability_core.py` | core-only public facade |

The composition modules are one portability ladder, not independent headline
theories:

\[
\text{bounded memory}
\subset
\text{coherent portable law}
\subset
\text{conservative grammar extension}.
\]

Relay trees are sharpness witnesses; they do not independently justify a new
structural research branch.

`addressable_completion_bounds.py` is retained as a finite product helper and
canonical coordinate example. It must not introduce a second public statement of
the core lower bound; that source of truth is
`extension_compression_noncommutation.py`.

## B. Identifiability companion

Use the separate public facade:

```python
import causal_model.identifiability_companion as rach_id
```

| Asset | Present role |
|---|---|
| `delayed_addressability.py` | no uniform horizon across expanding delayed families; historical re-export of shared grammar types during migration |
| `adaptive_closure_no_go.py` | finite adaptive transcript-only evidence cannot certify closure without an independent bound |
| `candidate_safe_laws.py` | universal versus candidate-safe versus set-valued macro laws |
| `joint_open_candidate_laws.py` | justified joint exterior–mechanism separation |
| `admissibility.py`, `confidence_lifting.py`, `anytime_confidence_lifting.py` | evidence-to-retained-candidate adapters |
| `symbolic_candidate_sets.py` | finite symbolic retained-family support |
| `observation_window_completion.py` | passive-evidence example; not a portability theorem target |
| `identifiability_companion.py` | companion-only public facade |

These modules are active only when the next selected research direction is
identifiability or mechanism uncertainty. They are not premises of the
portability core theorem family.

## C. Experimental-design legacy shelf

No new feature or theorem work without an explicit dependency from a selected
core or companion question.

| Branch | Why frozen |
|---|---|
| `delayed_joint_budgeted_quotients.py` | reset-budget identification is conditional design theory |
| `witnessed_boundary_evidence.py` | evidence lower bounds are not a closure theorem |
| `robust_canonical_panels.py` | robustness begins after quotient/panel selection |
| `common_mode_canonical_panels.py` | shared failure domains are field architecture |
| `observation_regime_closure.py` | narrow operational special case |

See [legacy/README.md](legacy/README.md).

## D. Frozen infrastructure

Certificate manifests, transcript registries, signed checkpoints, coverage
adapters, and tiered artifact formats preserve provenance. Keep them passing, but
add no audit feature unless a publication-grade certificate needs it.

## Public-import rule

New theorem code, examples, and tests must use exactly one of the two facades:

```python
import causal_model.portability_core as rach
import causal_model.identifiability_companion as rach_id
```

`causal_model.current_theory` remains a broad historical compatibility aggregate.
It is not a research entrance and must not receive new exports.

## Current priority order

1. **P1 proof hygiene:** use the public facades, remove duplicate public claims,
   and classify every statement as theorem, sufficient criterion, lower bound,
   witness, or unresolved region.
2. **P2 logical package boundary:** preserve the three public surfaces above;
   move shared primitives and compatibility shims before considering a physical
   repository split.
3. **P3 one research direction:** only after core v1 stop criteria are met,
   choose exactly one of non-nested rewiring, composition-dependent mechanisms,
   or approximate noisy portability.

## Anti-queue

Do not start another panel definition, budget ladder, audit wrapper,
domain-specific ecological toy model, action-alphabet special case, or larger
coordinate table merely because it supplies another edge case. It must first
change a canonical claim in [portability core v1](portability_core_v1.md) or a
selected identifiability claim.
