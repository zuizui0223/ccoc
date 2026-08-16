# Deterministic feedback novelty audit — 2026-08-16

> **Decision:** the deterministic feedback family is mathematically valid, but its general continuation-refinement headline is classical minimization / coarsest-stable-refinement substrate. Keep the executable modules and ecological witness families as follow-up examples; do not spend novelty language on the existence, fixed-point, unique-coarsest, or finite-stabilization statements.

## 1. Repository snapshot used for this audit

Audit pin before this branch:

`4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`

At that pin:

- no pull request is open;
- the most recent generic `tests` workflow on `main` succeeded;
- PR #211 already consolidated PRs #204/#205/#207/#208/#210 and stopped additional same-premise deterministic feedback expansion;
- the 2026-08-11 `FREEZE.md` reopening means that adding mathematics after July was not itself a freeze violation;
- however, the 2026-08-12 residual-novelty memo had already declared fixed-grammar exact quotient/minimization and ordinary partition refinement non-novel substrate and had instructed the project not to proliferate new special-case theorem families without a materially new premise.

Therefore the governance failure was **not** “new mathematics was forbidden by FREEZE.md.” The real failure was that the stronger novelty gate was not applied to the feedback family before theorem-family promotion.

## 2. Primary prior-art comparison

The general PR #210 construction starts from a supplied partition of finite states (here one hidden-mode block per explicit `(c,q)` fiber), repeatedly splits blocks until action successors are stable with respect to the current partition, and proves that the fixed point is exact and is the unique coarsest exact refinement relative to the retained explicit coordinates.

That mathematical pattern is established prior-art territory.

### Hopcroft 1971 — finite-automaton minimization

John E. Hopcroft, *An n log n Algorithm for Minimizing States in a Finite Automaton*, 1971, gives a partition-refinement algorithm for minimizing a finite automaton and determining state equivalence.

Primary publisher record:

- https://doi.org/10.1016/B978-0-12-417750-5.50022-1

### Paige–Tarjan 1987 — relational coarsest partition

Robert Paige and Robert E. Tarjan, *Three Partition Refinement Algorithms*, SIAM Journal on Computing 16(6), 1987, explicitly treats the **relational coarsest partition** problem via partition refinement.

Primary publisher record:

- https://doi.org/10.1137/0216062

### Dean–Givan 1997 / Givan–Dean–Greig 2003 — coarsest homogeneous refinement

Thomas Dean and Robert Givan, *Model Minimization in Markov Decision Processes*, AAAI 1997, defines homogeneous state-space partitions and gives an algorithm for the **coarsest homogeneous refinement of any partition**, explicitly describing it as an adaptation of known automata-minimization algorithms.

Primary conference record:

- https://s.aaai.org/Library/AAAI/1997/aaai97-017.php

The later full treatment is Robert Givan, Thomas Dean, Matthew Greig, *Equivalence notions and model minimization in Markov decision processes*, Artificial Intelligence 147 (2003), 163–223.

Primary publisher record:

- https://doi.org/10.1016/S0004-3702(02)00376-4

These sources are enough to remove novelty budget from the general “start from an initial partition, refine to the unique coarsest stable exact partition” claim. A future literature review may add closer deterministic/bisimulation references, but the adjudication does not depend on finding a word-for-word ecological formulation.

## 3. PR #210 adjudication

### Theorem 1 — current-type iff criterion

**Verdict: classical substrate / no standalone novelty.**

The condition that states merged by a proposed label must agree on current observables/legal transitions and map under every action to the same successor label is the standard congruence/stability condition for an exact quotient.

Keep it because it is a useful ecological contract and implementation check. Do not present it as a new mathematical theorem.

### Theorem 2 — finite continuation refinement

**Verdict: classical substrate / no standalone novelty.**

Monotone splitting to a stable fixed point is the standard partition-refinement pattern. The bound

\[
N_{\rm refine}\le |C||Q|(|M|-1)
\]

is the elementary finite block-count termination bound: every strict event adds at least one block and each fiber has at most `|M|` blocks.

Keep it as an algorithmic construction and reproducibility route, not as a novelty-bearing theorem.

### Theorem 3 — unique minimum repair relative to explicit `(c,q)`

**Verdict: classical substrate / no standalone novelty.**

This is the coarsest stable refinement of a declared initial partition, with the ecological coordinates deliberately kept explicit. The relative-coordinate formulation is useful for interpretation but does not create a new minimization theorem.

This statement should be removed from the family-level novelty headline rather than downgraded merely to the paper's positive-boundary Tier D.

### Theorem 4 — routed-context family

**Verdict: retain as a supporting sharpness witness; novelty unresolved.**

The useful concrete package is:

\[
\max_c |\tau_c(M)|=2,
\qquad |C|=3r+1,
\qquad |A|=2,
\qquad |P^*_{R_0}|=2^r.
\]

This shows that a uniformly tiny instantaneous ecological typing need not bound future-response rank when hidden mode routes the future context path.

The construction is worth keeping, but its proof is still a direct distinguishability construction over `2^r` hidden profiles. Treat it as an explicit constrained example until a targeted state-complexity / sequential-machine comparison establishes a stronger residual claim.

### Theorem 5 — exact exposure depth `2r-1`

**Verdict: proof/witness detail, not novelty headline.**

The sharp depth follows from the serial routed chain and inert off-phase actions. It is useful for explaining delayed exposure but belongs with the witness, not as a separate mathematical contribution.

## 4. Earlier feedback modules

### PR #204 — scalable feedback-gate rank

**Keep as the strongest mechanism-specific ecological witness, not a general minimization theorem.**

The useful result is the explicit causal ablation:

\[
K=r
\quad\text{with both arrows,}\qquad
K=0
\quad\text{after deleting either arrow.}
\]

This identifies one concrete mechanism that makes latent bits response-addressable. The injection/distinguishability argument itself is not novel. Any publication claim must be framed as a mechanism-specific construction or ecological corollary, not as a new state-minimization principle.

### PR #205 — bounded-type feedback portability

**Keep as a closed-form example; demote the theorem headline.**

The exact five-state quotient independent of physical replication is a clean symmetry/copy-anonymity example. The `5^q` multi-type product is ordinary product/common-refinement structure and should not carry novelty language.

### PR #207 — evolving feedback master types

**Mostly substrate plus a witness.**

The master signature

\[
\tau^*(m)=(\tau_c(m))_{c\in C}
\]

is a joint response profile/common refinement across contexts. The rotating family with only two instantaneous types but `2^r` master classes is useful as a witness, not a new minimization theorem.

### PR #208 — future-context causal forgetting

**Keep the causal interpretation; demote the general mathematics.**

Restricting a response signature to still-reachable future contexts gives a useful ecological language for when hidden distinctions can be forgotten. The reachability-conditioned quotient and monotone loss of future distinctions are not a defensible standalone novelty claim without a more specific structural theorem.

## 5. Revised feedback-family status

The deterministic feedback package should be described as:

> **Ecological instantiations and sharp examples of classical exact response minimization.** The general continuation-stable repair is the coarsest stable refinement relative to retained ecological coordinates. CCOC's useful added content is the explicit ecological mechanism/witness design: feedback cycles can create response-addressable memory, copy-anonymous replication can collapse to a fixed closed form, irreversible context loss can remove distinctions, and mode-routed contexts can hide exponentially many future classes behind binary instantaneous types.

This is a valid follow-up package, but it is **not** a new theorem family on the same novelty level as the first-paper cross-grammar separation candidate.

## 6. First-paper consequence

No first-paper proof dependency changes.

Retain the 2026-08-12 decision:

- **Tier A:** cross-grammar response-interface separation under a declared jointly realizable comparison family;
- **Tier B:** the quantitative one-action extremal separation / maximum open-only innovation;
- **Tier C:** bounded-local relay as constrained sharpness, with historical firstness gated by H1–H4;
- **Tier D:** conservative finite portability as the constructive positive boundary.

Do not move the PR #210 coarsest-refinement theorem into Tier D. It sits below the tier ladder as formal substrate.

## 7. Governance correction

Effective immediately for this repository:

1. `docs/residual_novelty_decision_2026-08-12.md` is the controlling novelty gate for finite deterministic fixed-grammar minimization claims.
2. `FREEZE.md` controls whether theorem development is procedurally allowed; it does **not** override the novelty gate.
3. A theorem may be mathematically valid and still be barred from headline status by prior-art classification.
4. Before a new theorem family is promoted, its own document must contain a short prior-art/status section mapping each headline claim to `substrate`, `supporting witness`, `residual candidate`, or `historically unresolved`.
5. No further deterministic persistent-mode feedback theorem should be added without changing a material model premise already listed in the 2026-08-15 stop rule.

## 8. Manuscript reality check

The absence of `.tex` files inside CCOC is **not itself a repository-policy failure**. Current policy explicitly assigns manuscript prose to the separate `rach-open-composition-paper` repository and tells CCOC not to duplicate prose.

The actual failure is operational: that manuscript repository still does not exist. Issue #141 records this as a manual blocker because the connected GitHub tool surface cannot create repositories. Issue #192 therefore cannot start manuscript-side transfer.

Once the manuscript repository exists, manuscript drafting should proceed from the narrow Tier A/B spine while H1–H4 wording remains conditional. Do not use the missing manuscript repository as a reason to generate another theorem family inside CCOC.
