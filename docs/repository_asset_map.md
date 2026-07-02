# RACH asset map: core, selected extension, companion, and legacy shelf

Read [portability core v1](portability_core_v1.md) before extending the structural
core and [research priorities](research_priorities.md) before opening a new
branch.

## Classification rule

An asset belongs to the structural program only when it changes one canonical
claim:

\[
\text{exact factorization},
\quad
\text{addressability obstruction},
\quad
\text{or portable composition}.
\]

Identifiability assets ask what finite evidence or retained mechanisms can justify.
Legacy assets begin only after a structural contract is fixed.

## A. Portability core v1

Use the stable public facade:

```python
import causal_model.portability_core as rach
```

| Asset | Present role |
|---|---|
| `causal_closure_calculus.py` | finite-model prerequisite: closure / recurrence / multistability |
| `shared_grammar.py` | shared finite prefix-grammar and controlled-system primitives |
| `dynamic_boundary_blankets.py` | exact update-closed finite boundary summary |
| `grammar_aware_blankets.py` | exact factorization over physical state × declared grammar state |
| `extension_compression_noncommutation.py` | canonical operational addressability lower bound and noncommutation inequality |
| `operational_addressability.py` | system-specific decoder and closed-context factorization certificates |
| `extension_compression.py` | binary coordinate sharpness witness |
| `relay_tree_compilation.py` | constant-grammar, pairwise, degree-three sharpness realization |
| `compositional_boundedness.py` | boundedness versus cumulative growth across nested stages |
| `coherent_portable_macrolaw.py` | common law under label-coherent nested embeddings |
| `conservative_macro_schema.py` | safe legal-action expansion and fiber-split obstruction |
| `portability_core.py` | structural public facade |

The v1 composition modules form one ladder:

\[
\text{bounded memory}
\subset
\text{coherent portable law}
\subset
\text{conservative grammar extension}.
\]

Relay trees are sharpness witnesses. `addressable_completion_bounds.py` is a
finite product helper; the sole public lower-bound statement is in
`extension_compression_noncommutation.py`.

## B. Selected post-v1 structural extension: non-nested replacement

This is the only authorized post-v1 direction. It replaces nested embeddings by
declared total transports that may be many-to-one or one-to-many.

| Asset | Present role |
|---|---|
| `non_nested_portability.py` | edge preservation, **transported target exact factorization**, and newly legal-word obstruction |
| `tests/test_non_nested_portability.py` | target construction plus label-consistency, successor-closure, new-action, connectedness, and facade regressions |
| `scripts/verify_non_nested_replacement_portability.py` | deterministic replay of supplied relation, derived target labels, and obstruction |
| `.github/workflows/non-nested-replacement-portability.yml` | path-scoped test and replay CI |
| `docs/non_nested_replacement_portability.md` | theorem, domain, verification contract, and non-claims |

The current construction theorem takes an exact source projection and a total
transport that preserves output and equal legal rows, is successor-closed, and is
label-consistent on each target fiber. It derives target labels and verifies the
resulting exact target projection. It does **not** cover target-only legal actions,
which require a different conservative transport contract or can split a carried
macro fiber.

## C. Identifiability companion

Use the separate public facade:

```python
import causal_model.identifiability_companion as rach_id
```

| Asset | Present role |
|---|---|
| `delayed_addressability.py` | delayed-family nonidentifiability primitives |
| `adaptive_closure_no_go.py` | finite adaptive transcript-only closure no-go |
| `candidate_safe_laws.py` | universal versus candidate-safe versus set-valued macro laws |
| `joint_open_candidate_laws.py` | justified joint exterior–mechanism separation |
| `admissibility.py`, `confidence_lifting.py`, `anytime_confidence_lifting.py` | evidence-to-retained-candidate adapters |
| `symbolic_candidate_sets.py` | finite symbolic retained-family support |
| `observation_window_completion.py` | passive-evidence example, not a core theorem target |
| `identifiability_companion.py` | companion public facade |

## D. Experimental-design legacy shelf

No new feature or theorem work is allowed here without an explicit dependency
from the selected structural or companion question.

| Branch | Why frozen |
|---|---|
| `delayed_joint_budgeted_quotients.py` | reset-budget identification is conditional design theory |
| `witnessed_boundary_evidence.py` | evidence lower bounds are not a closure theorem |
| `robust_canonical_panels.py` | robustness begins after quotient/panel selection |
| `common_mode_canonical_panels.py` | shared failure domains are field architecture |
| `observation_regime_closure.py` | narrow operational special case |

## E. Frozen infrastructure and public-import rule

Certificate manifests, transcript registries, signed checkpoints, coverage
adapters, and tiered artifacts preserve provenance. Keep them passing, but add no
feature without a publication-grade need.

New theorem code, examples, and tests use exactly one of:

```python
import causal_model.portability_core as rach
import causal_model.identifiability_companion as rach_id
```

`causal_model.current_theory` is a historical compatibility aggregate and must
not receive new exports.

## Current priority order

1. Preserve the core/companion/legacy boundary.
2. Treat transported target factorization plus the newly legal-word obstruction as
   the current stop point of non-nested portability.
3. Do not start candidate-dependent, approximate, or target-only-action transport
   branches in parallel.
4. Add new mathematics only by changing a canonical claim, not by adding another
   special-case witness or panel.
