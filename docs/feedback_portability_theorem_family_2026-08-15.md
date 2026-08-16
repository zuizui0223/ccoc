# Deterministic feedback portability family — 2026-08-15

> **Status after 2026-08-16 novelty audit:** consolidation of merged PRs #204, #205, #207, #208, and #210. The mathematics is retained, but the general continuation-refinement / unique-coarsest-repair result is now classified as **classical fixed-grammar minimization / coarsest-stable-refinement substrate**, not as a novelty-bearing family headline. The publication-relevant residue is the collection of explicit ecological mechanisms, closed-form examples, and constrained sharpness witnesses. See `docs/feedback_novelty_audit_2026-08-16.md`.

## 1. One question

The common ecological question remains useful:

> when hidden ecological interaction state changes later turnover, accessibility, or even the future context path, which hidden distinctions must an exact macro-interface retain?

Raw hidden-state count, raw network size, current abundance, and instantaneous interaction-type count are not the right answer.

Within the finite deterministic persistent-mode class, the controlling mathematical object is the minimum hidden-mode partition that is closed under every legal future continuation while the chosen ecological context and macrostate coordinates remain explicit.

That object is useful here as a **formal substrate**. Its computation by stable partition refinement is not a CCOC novelty claim.

## 2. General structural construction — continuation-stable hidden repair

PR #210 gives the relative stable-refinement construction in CCOC notation.

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

Among every exact interface that deliberately retains `c` and `q` explicitly,

\[
(c,q,\rho_{c,q}(m)),
\]

its hidden partition must refine `P*`. Thus `P*` is the unique coarsest/minimum hidden-mode repair relative to those ecological coordinates.

### Novelty status

The statements in this section are **not** a CCOC headline contribution. They instantiate the classical pattern of partition refinement to the coarsest stable/exact refinement of a supplied initial partition. The termination bound is the elementary finite block-count bound.

Primary prior-art anchors are recorded in `docs/feedback_novelty_audit_2026-08-16.md`, including Hopcroft (1971), Paige–Tarjan (1987), and Dean–Givan (1997).

The role of this section is therefore to provide one canonical implementation and notation for the ecological examples below.

## 3. Closed-form ecological examples

### A. Current type already closed

PR #210 gives the one-step stability check for a proposed current type `tau_c(m)`.

`(c,q,tau_c(m))` is exact iff equal current types have, under every action:

1. equal successor context;
2. equal successor macrostate; and
3. equal successor current type.

This is a quotient-stability/congruence test in ecological coordinates. Keep it as a useful contract; do not present the iff structure itself as novel mathematics.

### B. Fixed copy-anonymous interaction types

PR #205 is a concrete closed-form example. Physical copies within one interaction type are not individually addressable. Arbitrary replication `n` has a canonical exact five-state quotient independent of `n`, and fixed `q` types give

\[
|Q_{\rm macro}|=5^q.
\]

The five-state collapse is a useful explicit ecological example. The `5^q` product is ordinary product/common-refinement structure and carries no standalone novelty claim.

### C. Mode-independent context motion — master types

PR #207 assumes hidden mode changes transition response by context but not the context successor itself. The stable hidden object has the closed form

\[
\tau^*(m)=(\tau_c(m))_{c\in C}.
\]

This master signature is an interpretable representation of the relative stable partition in that subclass. Its product/profile form is substrate; the value is explanatory rather than firstness-bearing.

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

Retain this as a causal interpretation of when a hidden distinction becomes permanently irrelevant. Do not treat reachability-conditioned quotienting by itself as a new minimization theorem.

## 4. Mechanism-specific / sharpness witnesses

### A. Feedback cycle creates memory — PR #204

An explicit mode → turnover-induced facilitator loss → future accessibility cycle converts `r` hidden modes into `r` exact response bits even though the current graph/output/count summaries are identical.

Deleting either causal arrow collapses the burden to zero. This is the strongest feedback-specific ecological witness in the package because it identifies a concrete mechanism that creates operational addressability. The response-quotient injection used to prove the rank is substrate.

### B. Small instantaneous type count is insufficient — PR #207

A rotating family has only two current types in every context but `2^r` master types. The full profile first becomes recoverable at horizon `4r-1`.

Keep this as a constrained witness. No historical firstness is assigned to the exponential response separation.

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

This is worth retaining as an explicit routed-context sharpness family. The `2r-1` depth is a witness property, not a separate novelty headline.

## 5. What is actually established

For finite deterministic systems with:

- finite `C,Q,M,A`;
- persistent hidden interaction mode;
- current output represented through explicit ecological coordinates `c,q`;
- arbitrary hidden-mode dependence of ecological macro and context successors;

there is no remaining computational/existence question about the minimum extra hidden-mode memory conditional on retaining `c,q`: the classical stable-refinement substrate computes it as a finite fixed point.

CCOC's follow-up contribution candidate is therefore **not** the existence or uniqueness of that fixed point. The useful package is the explicit ecological structure around it:

- a feedback cycle can create response-addressable hidden memory and ablation can remove it;
- copy-anonymous replication can collapse to a fixed five-state exact description;
- irreversible future-context loss can make hidden distinctions exactly forgettable; and
- mode-routed contexts can hide exponentially many future classes behind uniformly binary instantaneous typing.

These are retained as examples/witnesses unless and until a targeted prior-art audit promotes a narrower residual claim.

## 6. Stop rule

Do not create another deterministic persistent-mode feedback theorem merely by changing the graph, adding another gate, changing the number of types, or choosing another finite context progression.

A new feedback theorem is justified only if it changes a model premise that PR #210 does not cover, for example:

- hidden interaction mode itself changes/evolves;
- stochastic feedback kernels;
- partial observation / uncertain context state;
- continuous or unbounded state with a nontrivial finite structural bound;
- a quantitative approximation/resource theorem not reducible to existing exact closure or generic information inequalities.

Until such a genuinely new premise is selected, deterministic feedback mathematics is **STOPPED / CONSOLIDATED**.

The 2026-08-12 residual-novelty gate takes precedence over theorem-count momentum: mathematical correctness is not sufficient for headline promotion.

## 7. Publication placement

These feedback results remain follow-up mathematics, not part of the first open-composition paper proof dependency graph.

If later published as one unit, use the following hierarchy rather than five equal theorem headlines:

1. **formal substrate:** relative exact response minimization via stable partition refinement;
2. **closed-form examples:** copy-anonymous five-state collapse, master signatures, future-context forgetting;
3. **mechanism-specific witnesses:** feedback-cycle ablation, rotating/routed families;
4. **ecological interpretation:** hidden state matters exactly while some legal future can route it back to the declared observable.

Do not present partition refinement, the unique coarsest fixed point, product/common refinement, or the finite split bound as new mathematics.

## 8. Source map

- `causal_model/feedback_gate_rank.py` — PR #204
- `causal_model/feedback_type_portability.py` — PR #205
- `causal_model/evolving_feedback_master_types.py` — PR #207
- `causal_model/future_feedback_causal_forgetting.py` — PR #208
- `causal_model/state_dependent_feedback_closure.py` — PR #210
- `docs/state_dependent_feedback_closure_2026-08-15.md` — general proof and routed-context equality family
- `docs/feedback_novelty_audit_2026-08-16.md` — prior-art adjudication and claim-control decision
