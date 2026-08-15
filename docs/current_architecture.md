# Current RACH/CCOC architecture — 2026-08-15

## Purpose

CCOC has one stable first-paper portability core and several explicit follow-up packages. Later theorem work does not silently expand the first-paper dependency graph.

## 1. First-paper structural core

The manuscript spine remains:

\[
\text{exact grammar-aware interface}
+
\text{extension/compression obstruction}
+
\text{bounded-local extremal witness}
+
\text{conservative portability}
+
\text{future-word fiber-split boundary}.
\]

Key modules remain `grammar_aware_blankets.py`, `extension_compression_noncommutation.py`, `relay_tree_compilation.py`, `coherent_portable_macrolaw.py`, and `conservative_macro_schema.py`, with the fixed-regular extremal strengthening in `fixed_regular_grammar_relay.py` / `extremal_open_composition.py`.

For every `m>=1`, the extremal family has

\[
|P_C|=2,
\qquad |P_O|=2^{m+1},
\qquad K_O-K_C=m,
\]

under one fixed four-symbol alphabet, one newly legal primitive action, degree at most three, cut one, and selected-coordinate access `2 ceil(log2 m)+2`.

## 2. Exact converse and reuse

- `action_grammar_closure.py`: exact one-state expansion converse;
- `grammar_expansion_closure.py`: corrected globally-new-symbol multi-state expansion;
- `grammar_interface_reuse.py`: arbitrary same-domain reuse iff open rows descend on closed fibers;
- `terminal_grammar_portability.py`: terminal quotient is the minimum labeling exact across a valid expansion chain.

The #163 coarsening counterexample permanently blocks arbitrary grammar-completion monotonicity.

## 3. Resource layer

`portability_adaptation_tradeoff.py` plus finite-boundary and staged-prefix results separate retained information, reopening update information, installation time, selected-query latency, and exposure deadlines.

## 4. Ecological structural layers

### Deterministic abundance

Saturation and depletion results show that exact finite blankets arise from forward-invariant response fibers and bounded future downward reach.

### Stochastic abundance

Stochastic saturation, continuous/per-capita depletion, and finite-horizon approximation separate exact stochastic relevance from approximate portable macros.

### Cross-guild coupling

Hidden saturated abundance remains relevant when it changes a downstream kernel; the saturated-tail hazard diameter controls exactness and sharp one-step minimax error.

### Spatial reachability

On a fixed directed graph, finite future horizon gives an exact distance-based macro with `min(D,H)+2` initial classes.

## 5. Deterministic feedback portability — one consolidated theorem family

Use `docs/feedback_portability_theorem_family_2026-08-15.md` as the entrance.

The family now has one general relative closure theorem and several interpretable special cases / sharpness constructions.

### General relative closure — PR #210

For finite context `C`, macrostate `Q`, persistent hidden mode `M`, and arbitrary hidden-mode dependence of successor context and macrostate, keep `(c,q)` explicit and refine hidden modes only when a legal future continuation forces a split.

The monotone continuation refinement reaches a fixed point `P*` after at most

\[
|C||Q|(|M|-1)
\]

strict split rounds.

Then

\[
\boxed{Z^*(c,q,m)=(c,q,[m]_{P^*_{c,q}})}
\]

is exact and is the unique coarsest/minimum hidden-mode repair among exact interfaces that retain `c,q` explicitly.

A proposed current type `tau_c(m)` is already exact iff equal current types have equal successor context, equal successor macrostate, and equal successor type under every action.

### Closed-form / sharp subclasses

- PR #204: an endogenous accessibility cycle generates exactly `r` feedback bits; cutting either causal arrow collapses the burden to zero.
- PR #205: copy-anonymous fixed interaction types give a replication-independent five-state quotient per type and `5^q` states for fixed `q` types.
- PR #207: mode-independent context motion with context-dependent types closes through the master signature; two instantaneous types per context can still generate `2^r` master classes.
- PR #208: autonomous irreversible context loss permits exact causal forgetting with sharp memory `r,r-1,...,0`.
- PR #210 routed-context family: hidden mode rewrites successor context itself; at most two instantaneous types and only `3r+1` contexts still require `2^r` initial continuation classes, with sharp exposure/stabilization depth `2r-1`.

### Deterministic feedback stop condition

For finite deterministic persistent hidden mode with explicit ecological `(c,q)`, the existence/minimum-hidden-repair question is closed by PR #210. Do not create more graph/type/context variants inside the same model class.

A new feedback theorem must change a premise materially: hidden-mode evolution, stochasticity, partial observation, continuous/unbounded state with a nontrivial bound, or a genuinely new approximation/resource question.

## 6. Mechanism-to-data bridge

`docs/mechanism_to_data_bridge_2026-08-14.md` remains the application-control layer. `UNIDENTIFIED` is not evidence for exact compression. A feedback application specifically needs longitudinal or experimental information resolving interaction → turnover/persistence → accessibility/movement → later response.

## 7. Historical, manuscript, and novelty gates

- H1–H4 in issue #122/#185 remain historical literature gates for bounded-local realization wording; primary construction pages are required.
- The hypothesis-recovery snapshot remains pinned separately.
- Manuscript transfer remains controlled by `docs/manuscript_transfer_manifest_2026-08-14.md` and issue #192.
- Novelty may now be adjudicated row by row from the recovered/fixed theorem scopes, but no global novelty slogan is allowed before publication-relevant comparisons are complete.

## 8. Workflow discipline

Analytic proof and finite replay remain separate. Green CI cannot rescue an over-broad theorem statement. Specialized workflows remain only where they supply distinct replay/artifact value.

## Navigation

- `fixed_regular_extremal_theorem_2026-08-13.md`
- `grammar_interface_reuse_2026-08-13.md`
- `terminal_grammar_portability_2026-08-13.md`
- `ecological_saturation_blanket_2026-08-14.md`
- `stochastic_ecological_portability_2026-08-14.md`
- `spatial_dispersal_reachability_2026-08-14.md`
- `feedback_portability_theorem_family_2026-08-15.md`
- `state_dependent_feedback_closure_2026-08-15.md`
- `mechanism_to_data_bridge_2026-08-14.md`
- `hypothesis_recovery_canonical_index_2026-08-14.md`
- `research_priorities.md`
