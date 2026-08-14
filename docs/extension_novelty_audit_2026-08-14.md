# Extension novelty audit — 2026-08-14

> **Purpose:** identify the strongest defensible novelty position for the post-core resource/ecological/stochastic/spatial/feedback packages. This is a targeted adjacency audit, not an exhaustive historical priority search. Absence of a direct hit does not justify “first” language.

## 1. Broad substrate already occupied

### Approximate state aggregation and finite-horizon error

Finite-horizon and approximate state representation are established topics in stochastic control and reinforcement learning. Primary modern examples include:

- Abel, Hershkowitz & Littman (ICML 2016), *Near Optimal Behavior via Approximate State Abstraction*, which gives performance guarantees for approximate state abstractions;
- Kao & Subramanian (AISTATS 2022), *Common Information based Approximate State Representations in Multi-Agent Reinforcement Learning*, which derives finite-horizon optimality gaps from approximation errors;
- broader finite-horizon aggregation/dynamic-programming literature predates these works.

Therefore CCOC should not claim novelty for “finite-horizon approximate abstraction” or horizon-dependent error bounds by themselves.

### Exact stochastic lumpability and population-count aggregation

Exact Markov/CTMC lumpability and count-based population aggregation are classical. Modern biological examples explicitly use strong/ordinary lumpability to derive Markovian count processes or exact reduced stochastic reaction systems.

General birth–death processes are also classical ecological/population models, and aggregation/averaging of heterogeneous birth–death populations is an established subject.

Therefore the CCOC stochastic ecology package is not a first lumpability, population-count, birth–death, or mortality theorem.

### Adaptive ecological/network feedback

Feedback between node/population state and network structure is established in adaptive-network theory. Primary examples include:

- Kozma & Barrat (Phys. Rev. E 2008), *Consensus formation on adaptive networks*;
- Marceau et al. (Phys. Rev. E 2010), *Adaptive networks: Coevolution of disease and topology*;
- ecological adaptive-network models that jointly represent abundance dynamics, interaction rewiring, and extinction resilience, including Maia et al. (Journal of Animal Ecology 2021).

Metapopulation extinction–colonization dynamics on networks and eco-evolutionary extinction/colonization feedback are also well established.

Therefore the exploratory CCOC feedback-network direction cannot claim novelty merely for coupling colonization/extinction, interactions, or dynamic topology.

## 2. Deterministic saturation / bounded downward reach

CCOC's model-specific exact statement is:

\[
Z=\min(L,N)
\]

under the declared monotone future, and with at most `D` future unit-depletion events the required exact initial cap becomes

\[
\boxed{L+D},
\]

so the initial canonical interface has `L+D+1` states when capacity is large enough.

### What the audit found

The targeted search found extensive threshold population modeling, birth–death processes, lumpability, quasi-lumpability, and exact/approximate stochastic aggregation. It did **not** surface a primary source expressing the same exact-interface law as

> response threshold + maximum *legal future downward reach*

or deriving the `L+D+1` canonical response-class count from a bounded future action grammar.

### Defensible novelty position

Use:

> “We derive an exact grammar-dependent memory law in which the abundance resolution required by a saturated response equals the response threshold plus the maximum legal future downward reach.”

This is a **model-specific residual novelty candidate**. Do not yet use “first” or “previously unknown” without a dedicated prior-art audit in stochastic population aggregation / controlled lumpability.

## 3. Changing-domain ecological portability

CCOC shows that systems with different abundance capacities can factor through the same capped macro-domain and macro transition law when the saturation/monotone contract is fixed.

Generic aggregation across differently sized Markov systems, scaling limits, population-process averaging, and effective reduced dynamics are established subjects. The targeted search did not locate a direct primary statement matching the CCOC **same finite exact macro law across changing capacity domains under a declared future grammar**.

Defensible wording:

> “Within this model family, the capped macro law is capacity-independent and therefore portable across changing semantic state spaces.”

Treat historical firstness as unverified.

## 4. Stochastic exact-versus-finite-horizon approximate separation

CCOC combines two facts in the same saturated abundance family:

1. every positive downward rate restores all `M+1` exact abundance response classes;
2. for fixed horizon `T`, an `L+1`-state saturated macro retains a capacity-independent path-distribution error bound.

Finite-horizon approximate abstraction and Markov aggregation error are already classical, so neither ingredient alone is a novelty anchor.

The targeted audit did **not** find a direct primary source presenting this particular asymptotic contrast:

\[
\text{exact macro size}\to\infty\text{ with capacity}
\qquad\text{while}\qquad
\text{fixed-horizon approximate macro size/error remain capacity-independent}.
\]

Defensible wording:

> “The model exhibits a sharp exact/finite-horizon separation: exact causal resolution grows with capacity for every positive downward rate, while a fixed-size saturated macro remains uniformly accurate over a fixed horizon.”

This is a stronger residual candidate than the elementary mortality formulas themselves, but still needs a dedicated controlled-lumpability/approximation prior-art gate before firstness language.

## 5. Hidden cross-guild coupling

CCOC defines the saturated-tail downstream-hazard diameter

\[
\delta=\sup_{A\ge L_A}p(A)-\inf_{A\ge L_A}p(A),
\]

and obtains exact capped portability iff `delta=0`, with sharp one-step minimax common-macro TV error `delta/2` in the Bernoulli recruitment model.

The Bernoulli/TV calculation is elementary and quasi-lumpability literature already measures within-block variation of transition probabilities. Therefore `delta/2` by itself is not a strong historical novelty target.

The more distinctive interpretation is:

> hidden abundance is removable exactly when every response-relevant downstream transition kernel is invariant inside the proposed saturated fiber.

Use this as a mechanistic CCOC statement, not as a first quasi-lumpability theorem.

## 6. Spatial reachability

CCOC's `min(D,H)+2` response-class law is a clean grammar-aware specialization, but graph reachability, shortest paths, patch-occupancy models, and extinction–colonization network dynamics are classical.

The strongest safe role is explanatory:

> the exact causal boundary is determined by directed reachability depth relative to the *declared legal future horizon*, so a remote reachable state and a true barrier may be equivalent under one future grammar and inequivalent under another.

Do not spend historical novelty budget on shortest-path or occupancy-shell counting.

## 7. Feedback-network direction after the new finite benchmark

Adaptive networks already establish mutual feedback between state dynamics and topology. Ecological network models already combine population dynamics, extinction, interaction rewiring, and network resilience.

Therefore a publishable new feedback theorem must target a different object:

> **exact causal-interface closure when interaction state changes later movement/reachability and movement in turn exposes or modifies interaction state.**

The current finite benchmark is relevant because two states agree on current response, static reachability/occupancy summaries, and every response word through length two, yet `spread -> turnover -> spread` separates them.

This suggests a latent **feedback memory** that is not represented by a static distance shell or a one-step downstream hazard.

### Minimum novelty requirement for promotion to theorem

Do not promote the benchmark unless a scalable result does at least one of:

1. characterize a finite feedback-aware exact interface under explicit structural assumptions;
2. prove that a natural product of existing saturation/reachability/hazard summaries is insufficient;
3. derive a sharp lower bound from independently addressable feedback modes;
4. prove a portability condition whose failure is specifically caused by alternating movement–interaction feedback, not generic hidden state.

Only then run a dedicated adaptive-network / ecological-network / controlled-bisimulation prior-art audit.

## 8. Extension claim ladder

### E-A — unconditional model result

Safe now:

> “Within the declared models, we derive exact and approximate interface laws for saturation, depletion reach, cross-guild coupling, and directed dispersal.”

### E-B — targeted-audit residual distinction

Safe with qualifier:

> “The targeted audit did not identify direct antecedents for the grammar-dependent `L+D` exact memory law or for the same-model contrast between capacity-diverging exact resolution and capacity-independent fixed-horizon approximate portability.”

### E-C — historical firstness

Not yet safe. Requires dedicated domain-specific prior-art searches beyond the present adjacency audit.

## 9. Audit anchors

Targeted adjacency sources used here include:

- Abel, Hershkowitz & Littman (2016), *Near Optimal Behavior via Approximate State Abstraction*, PMLR 48;
- Kao & Subramanian (2022), *Common Information based Approximate State Representations in Multi-Agent Reinforcement Learning*, PMLR 151;
- Kemeny–Snell lumpability as represented in modern exact-lumpability literature;
- Cardelli et al. (2021), exact species lumping for stochastic reaction networks;
- Crawford et al. (2018), *Computational methods for birth-death processes*;
- Kaakai & El Karoui (2018), birth–death-swap aggregation/averaging;
- Kozma & Barrat (2008), adaptive-network feedback;
- Marceau et al. (2010), coevolution of process and topology on adaptive networks;
- Maia et al. (2021), ecological abundance/topology feedback and rewiring;
- network metapopulation extinction–colonization literature.

## 10. Decision

The strongest immediate historical-novelty effort remains the first-paper constrained extremal package. Among extensions, the most promising **directly auditable residual candidates** are:

1. the grammar-dependent exact memory law `L+D`;
2. the capacity-diverging exact versus capacity-independent finite-horizon approximate separation;
3. a future scalable feedback-memory theorem, if it can be shown non-reducible to existing aggregation/reachability/adaptive-network substrate.

Do not dilute these candidates by assigning novelty to their classical ingredients.