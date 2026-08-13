# Current RACH/CCOC architecture

## Purpose

CCOC separates four questions that must not be conflated:

1. what is the exact response interface for one declared future grammar;
2. when does opening force that interface to refine;
3. when can a chosen closed interface still be reused under a changed grammar;
4. what local/static resources are sufficient to bound or realize the required interface.

The July v1 theorem IDs remain reproducibility anchors. Post-reopening work strengthens and clarifies the paper spine without rewriting those historical IDs.

## 1. Portability core

Preferred structural entrance:

```python
import causal_model.portability_core as rach
```

Historical spine:

| Role | Canonical modules |
|---|---|
| exact grammar-aware interface | `dynamic_boundary_blankets.py`, `grammar_aware_blankets.py` |
| cross-grammar lower-bound obstruction | `extension_compression_noncommutation.py`, `operational_addressability.py` |
| bounded-local sharpness | relay/compilation modules |
| conservative positive boundary | `coherent_portable_macrolaw.py`, `conservative_macro_schema.py` |

## 2. Exact converse and reuse layers

These are now intentionally separated by scope.

### 2.1 One-state action expansion

`causal_model/action_grammar_closure.py`

For a fixed plant with

\[
A_C^*\subseteq A_O^*,
\]

stable refinement of the canonical closed quotient under open actions equals the canonical open quotient. Zero inflation is equivalent to every newly legal action descending to the closed quotient.

### 2.2 Multi-state globally-new-symbol expansion

`causal_model/grammar_expansion_closure.py`

Old action symbols keep their **entire** grammar transition columns. Only an action illegal at every closed grammar state may be enabled after opening, possibly state-dependently. This preserves every closed distinguishing future, so

\[
P_O\preceq P_C.
\]

Stable open-row refinement of `P_C` then equals `P_O`. Zero inflation is exactly uniform open legality plus successor descent inside every closed fiber.

The stronger symbol-level premise is necessary. Completing a partially available old action can erase an enabled-row distinction and make the open canonical quotient coarser.

### 2.3 Arbitrary same-domain grammar change

`causal_model/grammar_interface_reuse.py`

When the grammar transition table may change more broadly, canonical quotient monotonicity is not assumed. The exact statement is instead:

\[
\boxed{
P_C\text{ reusable as an exact open interface}
\iff
\text{open enabled/successor rows descend on }P_C.
}
\]

The minimal canonical partitions may be equal, open-finer, open-coarser, or incomparable. Reuse of a chosen interface and movement of the minimal quotient are therefore distinct questions.

## 3. Integrated extremal theorem

Canonical analytic proof:

`docs/fixed_regular_extremal_theorem_2026-08-13.md`

Executable aggregate:

`causal_model/extremal_open_composition.py`

For every `m>=1`, the same fixed four-symbol system/grammar family has

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

with one newly legal action, one-state grammar schemas independent of `m`, bounded local state/message alphabets, pairwise radius-one dynamics, degree at most three, tree topology, focal/exterior cut one, and worst canonical access

\[
2\lceil\log_2m\rceil+2.
\]

It saturates finite-domain response-memory capacity. Together with the generic bounded-local causal-cone lower bound, its access is order-optimal in `m`.

This construction lies inside both the one-state closure theorem and the corrected globally-new-symbol class.

## 4. What the current theory does **not** say

- arbitrary mutation of a grammar automaton does not necessarily refine its canonical grammar-aware quotient;
- a smaller canonical open quotient does not mean a closed interface is unusable—it may remain an exact but nonminimal refinement;
- bounded degree, sparse/tree topology, or cut width one does not imply a small dynamic causal blanket;
- passing finite replay does not prove a quantified analytic theorem or validate an observed ecosystem.

## 5. Companion packages

### Identifiability

```python
import causal_model.identifiability_companion as rach_id
```

Delayed exposure, adaptive finite-evidence no-go, candidate-family agreement, and related epistemic results remain separate from the first-paper structural spine.

### Approximate robustness

`approximate_addressability.py` gives the Fano lower bound companion. It is not yet an approximate/stochastic portability theorem.

### Compatibility aggregate

`current_theory.py` remains a backward-compatible import surface, not the research entrance for new work.

### Legacy / replacement

Experimental-design branches remain executable but outside the structural novelty spine. Non-nested replacement/rewiring is centered in `zuizui0223/mltr`.

## 6. Workflow discipline

Analytic proof documents and finite certificates serve different roles. Every active result must state its exact semantic domain and grammar assumptions, include fail-closed counterexamples where appropriate, and preserve the July v1 replay.

The #163 correction is the model: a green CI result does not rescue an over-broad theorem statement when a mathematical counterexample exists.

## Navigation

- [Fixed-regular extremal theorem](fixed_regular_extremal_theorem_2026-08-13.md)
- [One-state closure converse](action_grammar_closure_converse_2026-08-13.md)
- [Corrected multi-state closure converse](grammar_expansion_closure_converse_2026-08-13.md)
- [General interface reuse theorem](grammar_interface_reuse_2026-08-13.md)
- [Research priorities](research_priorities.md)
- [Theorem registry](theorem_registry.md)
- [Legacy shelf](../legacy/README.md)
