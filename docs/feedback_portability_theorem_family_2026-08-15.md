# Deterministic feedback portability — consolidated record

> **Current status (2026-08-16):** feedback mathematics is **STOPPED / CONSOLIDATED**. The general continuation-refinement result from PR #210 is classical fixed-grammar minimization / coarsest-stable-refinement substrate. The current tree keeps only two representative executable examples. The removed implementations and detailed proof notes remain permanently recoverable from audit pin `4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a` and their merged PRs.

## 1. Scientific question retained

When hidden ecological interaction state changes later turnover, accessibility, or the future context path, which hidden distinctions must an exact macro-interface retain?

The answer is governed by future response distinctions, not raw hidden-state count, present abundance, or instantaneous type count.

## 2. Formal substrate — not a novelty claim

For finite deterministic persistent hidden mode with explicit ecological coordinates `(c,q)`, start from one hidden-mode block in each `(c,q)` fiber and refine until every legal action has a uniform successor explicit state and successor block.

The fixed point is exact and is the coarsest stable refinement relative to the retained `(c,q)` coordinates. Finite termination follows from block-count growth.

This is standard partition-refinement/minimization structure. Do not headline:

- the existence of the fixed point;
- its unique-coarsest property;
- the one-step quotient-stability criterion; or
- the elementary finite split bound.

Prior-art adjudication is in `docs/feedback_novelty_audit_2026-08-16.md`.

## 3. Active executable feedback surface

### A. Mechanism-specific negative witness — PR #204

Active module:

`causal_model/feedback_gate_rank.py`

An explicit cycle

\[
\text{hidden interaction mode}
\to
\text{turnover-induced facilitator loss}
\to
\text{future accessibility}
\]

makes `r` latent mode bits exactly response-distinguishable while current graph/output/count summaries are identical.

The useful causal result is the ablation:

\[
K=r \quad\text{with both arrows},
\qquad
K=0 \quad\text{if either arrow is removed}.
\]

The distinguishability/injection proof itself is substrate; the retained value is the explicit ecological mechanism that creates addressability.

### B. Closed-form positive example — PR #205

Active module:

`causal_model/feedback_type_portability.py`

If physical copies are copy-anonymous and share one interaction type, arbitrary replication has a five-state exact response quotient independent of copy count. For fixed `q` independently controlled types the product has `5^q` states.

The five-state collapse is the useful ecological example. The product construction is ordinary product/common-refinement structure.

## 4. Historical conclusions retained without active modules

The following valid conclusions are preserved here and in Git history, but no longer justify separate source/test/doc families in the current tree.

### PR #207 — master response profiles

When context motion is mode-independent but response type depends on context, the stable hidden summary can be represented by the context profile

\[
\tau^*(m)=(\tau_c(m))_{c\in C}.
\]

A rotating construction can have only two instantaneous types per context while producing `2^r` full future-response classes. Treat this as a witness, not a new minimization principle.

### PR #208 — exact causal forgetting

Under autonomous irreversible context motion, hidden distinctions needed only in permanently unreachable future contexts can be forgotten exactly. A chain can realize hidden-memory sequence

\[
r,r-1,\ldots,1,0.
\]

Retain the ecological interpretation: a hidden distinction ceases to matter when no legal future can route it back to the declared observable.

### PR #210 — mode-routed future contexts

If hidden mode changes the successor context itself, a routed family with one ecological macrostate, two actions, `3r+1` contexts, and at most two instantaneous feedback types per context can still require

\[
|P^*|=2^r,
\qquad K=r,
\]

at the initial context. The last bit is first exposed at depth `2r-1`.

The routed family remains a useful sharp example. The general refinement theorem used to compute `P*` is classical substrate.

## 5. Why the old implementation family was retired

PRs #207, #208, and #210 formed a sequence of progressively more general deterministic refinements of the same future-response equivalence problem. After the 2026-08-16 novelty audit, keeping all three implementations, three tests, and separate proof notes imposed maintenance cost without preserving additional headline science.

Their current-tree retirement does **not** erase the results:

- merged PRs and commit history preserve the complete code/proofs;
- audit pin `4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a` reproduces the pre-cleanup family;
- this document preserves the scientific statements that remain worth citing.

## 6. Stop rule

Do not add another deterministic persistent-mode feedback theorem by changing only graph layout, gate count, type count, or finite context progression.

A new feedback branch is justified only by a material premise change such as:

- evolving hidden mode;
- stochastic feedback;
- partial observation;
- continuous/unbounded state with a nontrivial structural bound; or
- a quantitative approximation/resource result not reducible to exact minimization or generic information inequalities.

## 7. Current navigation

- scientific/novelty audit: `docs/feedback_novelty_audit_2026-08-16.md`
- active negative witness: `causal_model/feedback_gate_rank.py`
- active positive example: `causal_model/feedback_type_portability.py`
- historical full feedback family: Git commit `4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`
