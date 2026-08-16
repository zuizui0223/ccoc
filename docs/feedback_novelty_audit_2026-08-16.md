# Deterministic feedback novelty audit — 2026-08-16

> **Decision:** the deterministic feedback program is mathematically valid, but its general continuation-refinement headline is classical minimization / coarsest-stable-refinement substrate. The current tree therefore keeps only two representative executable feedback examples; the remaining conclusions are retained in one consolidated record and Git history.

## 1. Audit pin and governance finding

Pre-cleanup pin:

`4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`

`FREEZE.md` had reopened theorem development on 2026-08-11, so adding mathematics was not itself a freeze violation.

The real control failure was different: `docs/residual_novelty_decision_2026-08-12.md` had already classified fixed-grammar exact quotient/minimization and partition-refinement machinery as non-novel substrate, but the feedback family was promoted before that gate was applied to its headline.

## 2. Prior-art anchors

PR #210 starts from a supplied finite partition, repeatedly splits blocks until action successors are stable, and proves that the fixed point is exact and the unique coarsest exact refinement relative to retained coordinates.

That pattern is established prior-art territory.

### Hopcroft 1971

John E. Hopcroft, *An n log n Algorithm for Minimizing States in a Finite Automaton*.

Primary publisher record:

- https://doi.org/10.1016/B978-0-12-417750-5.50022-1

### Paige–Tarjan 1987

Robert Paige and Robert E. Tarjan, *Three Partition Refinement Algorithms*, SIAM Journal on Computing 16(6), explicitly treats the relational coarsest partition problem.

- https://doi.org/10.1137/0216062

### Dean–Givan 1997 / Givan–Dean–Greig 2003

Dean and Givan define homogeneous state-space partitions and the coarsest homogeneous refinement of an arbitrary initial partition, explicitly adapting automata-minimization ideas.

- https://s.aaai.org/Library/AAAI/1997/aaai97-017.php
- https://doi.org/10.1016/S0004-3702(02)00376-4

These anchors are sufficient to remove novelty budget from the general “refine an initial partition to the unique coarsest stable exact partition” claim.

## 3. PR #210 adjudication

### Current-type stability criterion

**Classical substrate.** Equal proposed labels must have equal current observables/legal rows and action successors that remain in equal labels. Useful ecological contract, not new quotient theory.

### Finite continuation refinement

**Classical substrate.** Monotone splitting to a stable fixed point is standard partition refinement. The bound

\[
N_{\rm refine}\le |C||Q|(|M|-1)
\]

is the elementary finite block-count termination argument.

### Unique minimum repair relative to `(c,q)`

**Classical substrate.** This is the coarsest stable refinement of the initial partition defined by retaining the ecological coordinates explicitly. It sits below the Tier A–D novelty ladder.

### Routed-context construction

**Supporting witness; historical novelty unresolved.** The useful concrete package is

\[
\max_c |\tau_c(M)|=2,
\qquad |C|=3r+1,
\qquad |A|=2,
\qquad |P^*_{R_0}|=2^r,
\]

with last-bit exposure at depth `2r-1`.

The current tree preserves this conclusion in the consolidated feedback record rather than maintaining a separate general-refinement implementation.

## 4. Earlier feedback results

### PR #204 — feedback-cycle rank

**Strongest active negative/mechanistic example.** With both causal arrows the family stores `r` response bits; deleting either arrow collapses the burden to zero:

\[
K=r \quad\to\quad K=0.
\]

Keep executable module `causal_model/feedback_gate_rank.py` and its focused test.

### PR #205 — copy-anonymous five-state collapse

**Strongest active positive example.** Exact quotient size is five independent of physical replication. Keep executable module `causal_model/feedback_type_portability.py` and its focused test. The `5^q` product itself is ordinary product/common-refinement structure.

### PR #207 — master profiles

**Substrate plus witness.** The context profile

\[
\tau^*(m)=(\tau_c(m))_{c\in C}
\]

is a joint response profile/common refinement. The rotating `2`-instantaneous-type versus `2^r`-future-class construction remains a historical supporting witness. Dedicated current-tree implementation retired.

### PR #208 — future-context forgetting

**Useful causal interpretation, not standalone minimization novelty.** A hidden distinction can be forgotten when no still-reachable legal future can expose it. Dedicated current-tree implementation retired.

## 5. Current-tree decision

The feedback package now has only:

- `causal_model/feedback_gate_rank.py`
- `causal_model/feedback_type_portability.py`
- `docs/feedback_portability_theorem_family_2026-08-15.md`
- this novelty audit

as its active source/doc surface.

Retired from the current tree:

- PR #207/#208/#210 theorem modules and tests;
- the superseded initial feedback-network experiment and test;
- five per-PR feedback proof notes and the exploratory triage note.

The complete pre-cleanup implementation/proof surface remains recoverable at audit pin `4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`.

## 6. First-paper consequence

No first-paper proof dependency changes.

- **Tier A:** same-system cross-grammar response-interface separation;
- **Tier B:** one-action maximal open-only innovation;
- **Tier C:** bounded-local relay as constrained sharpness, historical firstness unresolved;
- **Tier D:** conservative finite portability boundary.

Fixed-grammar coarsest refinement is substrate below this ladder.

## 7. Stop rule

Do not add another deterministic persistent-mode feedback theorem by changing only graph, gate count, type count, or finite context progression.

A new branch requires a material premise change: evolving hidden mode, stochastic feedback, partial observation, continuous/unbounded state with a nontrivial bound, or a genuinely new approximation/resource theorem.

## 8. Current project direction

The current priority is **repository cleanup**, not new theorem development and not manuscript expansion inside CCOC.

Use this feedback pass as the template: retain a small number of representative executable results, preserve scientific conclusions in a canonical record, and let immutable Git history carry superseded implementations and detailed proof notes.
