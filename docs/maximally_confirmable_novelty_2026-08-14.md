# Maximally confirmable novelty audit — 2026-08-14

> **Purpose:** maximize what CCOC can safely claim now, without waiting for every H1–H4 primary source and without converting absence-of-hit into proof of historical firstness. This document separates (i) mathematical validity, (ii) audited classical substrate, (iii) currently distinct problem framing, (iv) residual conditional firstness, and (v) extensions that still need their own prior-art gate.

## 1. First correction: H1–H4 are not fully recovered

The H1–H4 compiler contract is still **partially unresolved**.

- **H1 — bounded locality:** unresolved for the strongest primary classical compiler candidates; Weiner–Hopcroft 1968 and Newborn–Arnold 1972 still require the construction body.
- **H2 — fixed context-independent controls/input distribution:** Ullman–Weiner 1969 gives primary partial support for fixed binary source input; exact distribution/encoding cost is unread.
- **H3 — two-way response-trace faithfulness:** Ullman–Weiner gives primary wording of “isomorphic realization”, but the formal output/isomorphism contract is unread.
- **H4 — bounded timing/output latency:** Ullman–Weiner gives primary partial evidence that required source-input spacing need not grow with network size; exact source-step/network-round/output semantics remain unread.

Therefore no statement below upgrades bounded-local realization to a historical firstness claim. Issue #122 remains the H1–H4 gate.

## 2. What the targeted primary audit already blocks as novelty

### 2.1 Exact quotient / bisimulation / causal-state machinery

Do **not** claim novelty for the existence of a coarsest exact predictive/behavioral partition, partition refinement, bisimulation minimization, or action-conditioned predictive state representation.

Primary/authoritative anchors include:

- Amy Zhang et al., *Learning Causal State Representations of Partially Observable Environments* (2019), which explicitly treats causal states as the coarsest partition of action-observation histories and connects them to bisimulation.
- Standard MDP homomorphism/state-abstraction work, including recent exact/approximate abstraction work in PMLR.
- Bisimulation minimization and DFA/NFA minimization literature.

CCOC may use this substrate, but `CORE-1` is a formalization/scope anchor rather than a firstness claim.

### 2.2 Changing/expanding action sets

Do **not** claim that “the action set changes” or “new actions become available” is itself new.

Direct primary adjacent work includes:

- Chandak et al. (AAAI 2020), *Lifelong Learning with a Changing Action Set* — explicitly studies sequential decision problems where the available action set changes over time.
- Jain, Szot & Lim (ICML 2020), *Generalization to New Actions in Reinforcement Learning* — studies zero-shot generalization to unseen/new actions.
- Drago, Mussi & Metelli (ICML 2025), *Sleeping Reinforcement Learning* — formalizes varying available action sets and derives learning-theoretic lower/upper bounds.
- Fecher & Huth (VMCAI 2008), *Model Checking for Action Abstraction* — studies transition systems with ordered actions and consistent extensions of action sets under an extended-bisimulation refinement semantics.

Thus **action-set extension, action refinement, or changing availability alone is classical/adjacent territory**.

### 2.3 State abstraction across tasks / transfer

Do **not** claim that one abstraction being reused across multiple tasks/contexts is new in isolation.

- Abel et al. (ICML 2018), *State Abstractions for Lifelong Reinforcement Learning*, develops abstractions designed for transfer over task families.
- MDP homomorphism and state-action abstraction work provides transfer/reuse machinery under structural assumptions.

CCOC must therefore distinguish **exact response-interface portability under legal-future expansion** from generic task-transfer abstraction.

### 2.4 Markov lumpability / stochastic aggregation

Do **not** assign firstness to exact stochastic lumpability, row-sum conditions, or state aggregation in biological stochastic systems.

Primary biological/model-reduction literature already applies ordinary/strong lumpability to molecular evolution, reaction networks, and stochastic state aggregation. For example, Cardelli et al. (Bioinformatics 2021), *Exact maximal reduction of stochastic reaction networks by species lumping*, explicitly characterizes exact reductions via ordinary lumpability.

The CCOC stochastic ecology modules are therefore **model-specific portability statements built on classical lumpability substrate**, not first lumpability theorems.

### 2.5 Other demoted substrate

Also do not spend novelty language on:

- Myhill–Nerode/right congruences;
- common refinement/join/cardinality accounting;
- incomplete-machine minimization or input restrictions as broad ideas;
- repeated identical modules, bounded fan-in/fan-out, or fixed modules with delay in isolation;
- generic causal-cone counting;
- Fano, entropy, channel-capacity, or deadline-scheduling inequalities;
- shortest paths, directed reachability, Poisson/binomial survival, Bernoulli TV calculations;
- threshold aggregation by itself.

## 3. Strongest claim that is already supportable without H1–H4

### 3.1 Distinct problem formulation: exact compression portability under a declared legal future

The strongest H1–H4-independent contribution is the **specific exact portability question**:

> For one fixed controlled plant, if a state summary is exact for every response permitted by a declared closed future grammar, when does that same summary remain exact after the legal future language is enlarged, and how much additional exact interface memory can the opening force?

The targeted primary audit found several neighboring traditions:

- action-conditioned exact abstractions / causal states;
- abstractions across task families;
- changing or newly available action sets;
- action refinement and action-set extension in formal methods;

but **no inspected primary source directly characterizes the change in the coarsest exact response-interface cardinality caused solely by enlarging the legal future language of the same plant**, nor a matching “closed exact compression versus open exact interface” memory quantity.

This is **not proof of historical absence**. It is enough for manuscript-safe wording such as:

> “We study exact macro-interface portability under changes in the legal future action grammar.”

or, more cautiously,

> “We formulate the closed-to-open exact interface problem for a fixed controlled plant and quantify the memory exposed by legal-future expansion.”

Do not write “first” solely from this audit.

### 3.2 The exact noncommutation phenomenon is mathematically real, but the elementary centralized blow-up is not a novelty anchor

CCOC proves exact closed/open separation and an extension–compression obstruction. However, an elementary centralized family in which a newly legal action reveals hidden coordinates is too simple to carry historical novelty by itself.

Therefore the paper should **not** sell

\[
|P_C|\ll |P_O|
\]

alone as a new phenomenon. Its role is to make the exact portability failure explicit and auditable.

## 4. Strongest residual first-paper novelty candidate

The live candidate remains the **simultaneous constrained extremal/local realization package**.

For every `m>=1`, one fixed plant family and one fixed primitive alphabet

\[
\{0,1,\mathsf{fire},\mathsf{tick}\}
\]

have:

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

with the open quotient discrete on the finite semantic domain, hence zero capacity slack.

At the same time the explicit realization has:

- one newly legal primitive action / one grammar-transition edit;
- one-state closed/open regular grammar schemas independent of `m`;
- pairwise radius-one dynamics;
- bounded local state/message alphabets independent of `m`;
- tree topology;
- maximum degree three;
- focal/exterior cut width one;
- arbitrary `m`, not only powers of two;
- exact selected-coordinate access length

\[
2\lceil\log_2 m\rceil+2.
\]

### 4.1 What is already safe to claim

It is safe to claim the **mathematical conjunction** and its exact constants because CCOC proves them.

It is also safe to say that the targeted audit has found no direct primary antecedent that simultaneously presents this exact package as a closed/open response-interface extremal construction.

### 4.2 What remains conditional

Historical firstness for the **bounded-local realization existence** remains conditional on H1–H4.

If a classical uniform compiler satisfies H1–H4 with comparable overhead, then compiling the elementary centralized seed may already imply bounded-local existence. In that outcome CCOC should demote “first bounded-local realization” and retain:

- the explicit degree-three / cut-one architecture;
- the exact maximal equality case;
- the fixed four-symbol grammar and one-action opening;
- transparent selected-query length and constants;
- ecological/compositional interpretation.

### 4.3 What could survive even if H1–H4 all hold

Even if classical compilation subsumes **existence**, it does not automatically establish that an earlier source gives the same simultaneous **sharp extremal equality with the same explicit structural constants**.

Thus the residual claim ladder is:

1. **Existence of some bounded-local realization** — H1–H4 controlled and potentially classical.
2. **This explicit constrained equality witness** — likely survives as a construction contribution unless a primary source is found with comparable simultaneous constraints and sharpness.
3. **Historical “first such witness” wording** — still requires a dedicated direct-prior check and should not be asserted from absence of a hit.

## 5. Exact converse/reuse package: useful mathematics, weak historical-firstness target

The one-state action-closure theorem, globally-new-symbol closure theorem, arbitrary-grammar reuse iff criterion, and terminal-chain theorem are useful structural results.

However their proof mechanisms are close to classical right-congruence, bisimulation/homomorphism, partition-refinement, and factor-map conditions. Therefore:

- keep them as **CCOC scope-clarifying theorems**;
- do not spend first-paper novelty budget on “stable closure equals the open quotient” or row-descent conditions in isolation;
- use the #163 coarsening counterexample to prevent a false monotonicity slogan rather than to make a firstness claim.

## 6. Coupled resource package: substantive consequence, but novelty should be phrased as a CCOC-specific coupling

The retention/update/boundary-time/staged-deadline results are mathematically useful because they separate:

- information retained before opening;
- information communicated after opening;
- full-interface installation time;
- selected-query latency;
- stage-specific deadlines.

But the lower-bound substrate is classical information theory, finite-channel capacity, and scheduling. The strongest safe wording is therefore:

> “For the CCOC portability problem, these classical resources combine into a sharp retention–adaptation–installation tradeoff.”

Do not claim a new Fano/channel-capacity theorem.

## 7. Ecological/stochastic/spatial package: genuine CCOC extensions, historical novelty not yet audited

### 7.1 Deterministic saturation / changing capacity / bounded downward reach

The model-specific structural statement

\[
\text{required abundance cap}
=
\text{response threshold}
+
\text{maximum legal future downward reach}
\]

is a useful CCOC ecological result. It is stronger than simply saying “threshold aggregation is possible,” because the exact memory is tied to the declared future dynamics/grammar.

However exact aggregation/lumpability and thresholded population summaries have broad ancestry. Until a dedicated prior-art audit is done, use **“we derive”**, not “first”.

### 7.2 Stochastic exact versus finite-horizon approximate portability

The CCOC package gives a clear model-specific separation:

- any positive downward rate can restore all exact abundance classes;
- finite-horizon approximate macro size/error can remain capacity-independent.

This exact/approximate contrast is scientifically interesting, but approximate abstraction and lumpability are classical. Treat it as a **new CCOC consequence/model result**, not yet a historically first theorem.

### 7.3 Hidden cross-guild coupling

The saturated-tail hazard diameter `delta` gives a compact mechanistic criterion and sharp `delta/2` one-step minimax TV error in the declared Bernoulli model.

The formula itself is elementary. The potentially distinctive contribution is the interpretation:

> hidden state matters precisely through the downstream transition kernel it changes inside a proposed macro fiber.

Keep the mechanism framing; do not claim novelty for the Bernoulli/TV calculation.

### 7.4 Spatial reachability

The `min(D,H)+2` result is a clean CCOC grammar-aware ecological statement, but shortest-path reachability is classical. Use it as an explanatory structural theorem, not a historical firstness anchor.

### 7.5 Feedback-network benchmark

The new `spread -> turnover -> spread` benchmark shows a latent interaction mode can rewrite later accessibility even when static distance, occupancy count, and all response words through length two agree.

This is currently **research triage**, not a public theorem. It is promising precisely because it may escape a direct product of existing reachability/depletion/cross-guild summaries. Do not assign novelty until it scales to a theorem and receives its own prior-art audit.

## 8. Claim ladder for the manuscript

### Level A — unconditional mathematical claim

Use freely:

> “We define exact response interfaces relative to a declared future grammar and prove closed/open separation, a fixed-grammar extremal family, and positive portability conditions.”

This is a statement about what the paper proves, not historical firstness.

### Level B — audited-distinct formulation claim

Currently supportable:

> “We study the portability of exact state compression when the legal future action language of a fixed system is enlarged.”

Targeted primary searching found adjacent work on causal-state/bisimulation abstraction, task-transfer abstraction, changing action sets, new-action generalization, and action-set refinement, but no direct antecedent matching the exact response-interface inflation problem.

### Level C — targeted-audit residual claim

Currently supportable with explicit qualifier:

> “To our knowledge, the inspected literature does not provide the same simultaneous fixed-grammar, one-action, maximal closed/open separation with the explicit bounded-local degree-three/cut-one realization.”

This is stronger than Level B but still not a proof of historical firstness.

### Level D — historical firstness claim

**Not yet supportable.** Reserve wording such as “first,” “previously unknown,” or “no prior construction” until the decisive H1–H4 primary construction pages and the direct constrained-witness comparison are complete.

## 9. Recommended novelty sentence now

A manuscript-safe high-information sentence is:

> We study exact macro-interface portability under legal-future expansion of a fixed controlled system. Although predictive/state abstraction, changing action sets, action refinement, and modular sequential-machine realization each have substantial prior literatures, we give a fixed four-symbol, one-action extremal family in which a two-class closed exact interface becomes the discrete open quotient, together with an explicit degree-three, cut-one local realization and matching logarithmic selected access; the historical firstness of the local-realization component remains subject to the H1–H4 compiler audit.

This sentence maximizes the confirmed contribution while isolating the one historical clause that is still unresolved.

## 10. Primary-source anchors used in the 2026-08-14 targeted audit

These are adjacency/claim-control anchors, not an exhaustive bibliography.

- Zhang et al. (2019), *Learning Causal State Representations of Partially Observable Environments*, arXiv:1906.10437.
- Abel et al. (2018), *State Abstractions for Lifelong Reinforcement Learning*, ICML / PMLR 80.
- Chandak et al. (2020), *Lifelong Learning with a Changing Action Set*, AAAI, DOI `10.1609/aaai.v34i04.5739`.
- Jain, Szot & Lim (2020), *Generalization to New Actions in Reinforcement Learning*, ICML / PMLR 119.
- Drago, Mussi & Metelli (2025), *Sleeping Reinforcement Learning*, ICML / PMLR 267.
- Fecher & Huth (2008), *Model Checking for Action Abstraction*, VMCAI, DOI `10.1007/978-3-540-78163-9_13`.
- De Santi et al. (2024), *Geometric Active Exploration in Markov Decision Processes: the Benefit of Abstraction*, ICML / PMLR 235, for modern MDP-homomorphism abstraction context.
- Cardelli et al. (2021), *Exact maximal reduction of stochastic reaction networks by species lumping*, Bioinformatics 37(15):2175–2185, for exact biological stochastic lumpability/model reduction.

## 11. Stop rule

Do not convert “no direct hit in this targeted audit” into an absolute firstness claim.

The correct strategy is:

1. maximize **unconditional mathematical contribution**;
2. maximize **audited distinctness of the problem/conjunction**;
3. isolate only the bounded-local historical existence clause behind H1–H4;
4. run separate prior-art gates before assigning firstness to ecological/resource follow-ups;
5. preserve strong non-claims for every classical substrate component.
