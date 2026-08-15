# Deterministic feedback portability theorem family — 2026-08-15

> **Status:** consolidation of merged PRs #204, #205, #207, #208, and #210. This document reduces theorem sprawl: the five modules are not five unrelated headline theories. They are one deterministic feedback-portability family with a general relative closure theorem, closed-form positive subclasses, and sharp obstruction families. No novelty conclusion is made here.

## 1. One question

The common problem is:

> when hidden ecological interaction state changes later turnover, accessibility, or even the future context path, which hidden distinctions must an exact macro-interface retain?

Raw hidden-state count, raw network size, current abundance, and instantaneous interaction-type count are not the right answer.

Within the finite deterministic persistent-mode class, the controlling object is the **minimum hidden-mode partition that is closed under every legal future continuation while the chosen ecological context and macrostate coordinates remain explicit**.

## 2. General theorem — continuation-stable hidden repair

PR #210 supplies the general structural result in this deterministic class.

For explicit ecological context `c`, ecological macrostate `q`, persistent hidden mode `m`, and action `a`, allow the full successor

\[
(c,q,m)\xrightarrow{a}
(D(c,q,m,a),F(c,q,m,a),m).
\]

Start with one hidden-mode block in each `(c,q)` fiber and repeatedly split a block whenever two modes send some legal action to different explicit successor `(c',q')` values or to different hidden blocks at that successor.

The monotone refinement reaches a finite fixed point `P*` with bound

\[
N_{\rm refine}\le |C||Q|(|M|-1).
\]

Then

\[
\boxed{Z^*(c,q,m)=(c,q,[m]_{P^*_{c,q}})}
\]

is exact.

More strongly, among every exact interface that deliberately retains `c` and `q` explicitly,

\[
(c,q,\rho_{c,q}(m)),
\]

its hidden partition must refine `P*`. Thus `P*` is the unique coarsest/minimum hidden-mode repair relative to those ecological coordinates.

This is the family-level headline. The earlier feedback theorems identify interpretable cases where `P*` has a closed form or a sharp lower bound.

## 3. Closed-form positive subclasses

### A. Current type already closed

PR #210 also gives the one-step iff criterion for a proposed current type `tau_c(m)`.

`(c,q,tau_c(m))` is exact iff equal current types have, under every action:

1. equal successor context;
2. equal successor macrostate; and
3. equal successor current type.

So a current ecological type is portable exactly when it evolves as a deterministic macro type under the declared feedback dynamics.

### B. Fixed copy-anonymous interaction types

PR #205 is a concrete closed-form subclass. Physical copies within one interaction type are not individually addressable. Arbitrary replication `n` has a canonical exact five-state quotient independent of `n`, and fixed `q` types give

\[
|Q_{\rm macro}|=5^q.
\]

This is not a separate theory; it is a structured case where continuation closure collapses all copy identity.

### C. Mode-independent context motion — master types

PR #207 assumes hidden mode changes transition response by context but not the context successor itself. The stable hidden object has the closed form

\[
\tau^*(m)=(\tau_c(m))_{c\in C}.
\]

The master feedback signature is therefore an explicit representation of the general continuation partition for that subclass.

### D. Autonomous irreversible context motion — exact forgetting

PR #208 strengthens context motion to

\[
c'=D(c,a).
\]

The full master signature can then be restricted to still-reachable contexts:

\[
\tau_c^+(m)
=(\tau_d(m))_{d\in \operatorname{Reach}^+(c)}.
\]

Future rank cannot increase along a context edge. An irreversible chain attains exact hidden memory

\[
r,r-1,\ldots,1,0.
\]

This is the exact causal-forgetting special case of continuation closure: a hidden distinction disappears when no legal future continuation can make it relevant again.

## 4. Negative / sharpness side

### A. Feedback cycle creates memory — PR #204

An explicit mode → turnover-induced facilitator loss → future accessibility cycle converts `r` hidden modes into `r` exact response bits even though the current graph/output/count summaries are identical.

Deleting either causal arrow collapses the burden to zero. Thus hidden cardinality alone is not the source of the lower bound.

### B. Small instantaneous type count is insufficient — PR #207

A rotating family has only two current types in every context but `2^r` master types. The full profile first becomes recoverable at horizon `4r-1`.

### C. Hidden mode rewrites the future context path — PR #210

A two-action family with one ecological macrostate and only `3r+1` contexts has at most two current feedback types at every context, but the initial continuation partition has

\[
|P^*|=2^r,
\qquad K=r.
\]

The last hidden routing bit first becomes exposable at horizon

\[
2r-1,
\]

and the continuation refinement stabilizes at the same depth.

This closes the mode-dependent context-reachability boundary left open by PR #208.

## 5. What is actually established

For finite deterministic systems with:

- finite `C,Q,M,A`;
- persistent hidden interaction mode;
- current output represented through explicit ecological coordinates `c,q`;
- arbitrary hidden-mode dependence of ecological macro and context successors;

there is no remaining existence question about the **minimum extra hidden-mode memory conditional on retaining `c,q`**. PR #210 gives it as a finite continuation fixed point.

The simpler theorems answer when that fixed point collapses to an interpretable low-dimensional object and when it must be large.

The resulting principle is

\[
\boxed{
\text{exact hidden feedback memory}
=
\text{future-continuation distinctions not already represented by the chosen ecological coordinates}.
}
\]

## 6. Stop rule

Do not create another deterministic persistent-mode feedback theorem merely by changing the graph, adding another gate, changing the number of types, or choosing another finite context progression.

A new feedback theorem is justified only if it changes a model premise that PR #210 does not cover, for example:

- hidden interaction mode itself changes/evolves;
- stochastic feedback kernels;
- partial observation / uncertain context state;
- continuous or unbounded state with a nontrivial finite structural bound;
- a quantitative approximation/resource theorem not reducible to existing exact closure or generic information inequalities.

Until such a genuinely new premise is selected, deterministic feedback mathematics is **STOPPED / CONSOLIDATED**.

## 7. Publication placement

These feedback results remain follow-up mathematics, not part of the first open-composition paper proof dependency graph.

If later published as one unit, use one theorem-family narrative:

1. continuation-stable hidden repair — general structural theorem;
2. bounded-type/master/future-signature closed forms — positive subclasses;
3. cycle/rotating/routed families — sharp obstructions;
4. exact forgetting — causal interpretation of disappearing future distinctions.

Do not present every module as an independent headline theorem.

## 8. Source map

- `causal_model/feedback_gate_rank.py` — PR #204
- `causal_model/feedback_type_portability.py` — PR #205
- `causal_model/evolving_feedback_master_types.py` — PR #207
- `causal_model/future_feedback_causal_forgetting.py` — PR #208
- `causal_model/state_dependent_feedback_closure.py` — PR #210
- `docs/state_dependent_feedback_closure_2026-08-15.md` — general proof and routed-context equality family
