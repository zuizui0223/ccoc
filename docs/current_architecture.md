# Current RACH/CCOC architecture — 2026-08-14 post-feedback theorem pair

## Purpose

CCOC now separates nine mathematical/ecological questions:

1. what is the exact response interface for one declared future grammar;
2. when does opening force refinement;
3. when can a chosen closed interface still be reused;
4. what retained/update/boundary-time resources are required across openings;
5. when can one exact macro-law survive changing semantic domains;
6. which deterministic ecological structures create or destroy finite blankets;
7. when exact stochastic non-portability still admits a finite-horizon approximate portable macro;
8. how hidden cross-component coupling and directed spatial reachability expose otherwise compressed distinctions;
9. when **endogenous accessibility feedback** creates unbounded hidden-mode memory and when bounded feedback types instead admit one portable exact macro.

The July v1 theorem IDs remain reproducibility anchors. Post-reopening results are explicit theorem surfaces and do not silently rewrite the historical paper core.

## 1. Structural portability core

Preferred historical entrance:

```python
import causal_model.portability_core as rach
```

The first-paper spine remains exact grammar-aware interfaces, cross-grammar obstruction, bounded-local relay sharpness, conservative portability, and the future-word fiber-split boundary.

## 2. Exact converse and reuse

`action_grammar_closure.py` gives the exact one-state action-language expansion converse. `grammar_expansion_closure.py` gives the corrected globally-new-symbol multi-state result. `grammar_interface_reuse.py` handles arbitrary same-domain grammar change, where canonical quotients may be equal, finer, coarser, or incomparable.

The broad reuse statement is

\[
P_C\text{ reusable exactly}
\iff
\text{open enabled/successor rows descend on }P_C.
\]

`terminal_grammar_portability.py` then identifies the terminal quotient as the minimum one-labeling exact across a valid globally-new-symbol expansion chain.

The #163 coarsening counterexample remains the permanent guard against restoring arbitrary grammar-completion monotonicity.

## 3. Integrated fixed-regular extremal family

`fixed_regular_grammar_relay.py` and `extremal_open_composition.py` realize for every `m>=1`

\[
|P_C|=2,
\qquad |P_O|=2^{m+1},
\qquad K_O-K_C=m,
\]

under one fixed four-symbol alphabet and one newly legal primitive action. Local state/message alphabets are bounded, dynamics are radius-one, maximum degree is three, topology is a tree, focal/exterior cut is one, and selected-coordinate access is

\[
2\lceil\log_2m\rceil+2.
\]

## 4. Chain and resource portability

`portability_adaptation_tradeoff.py` gives the retained/update information lower bound

\[
I(E;C)+I(E;U\mid C)
\ge
m-\sum_jh_2(\varepsilon_j).
\]

The boundary-time result converts update debt into full-interface installation time, while the staged-prefix theorem adds exposure deadlines. These distinguish eventual shared memory, selected-query latency, cumulative update throughput, and deadline-feasible installation.

## 5. Deterministic ecological structure

`ecological_saturation_blanket.py` derives

\[
Z_g=\min(L_g,N_g)
\]

as an exact dynamic blanket under monotone guild colonization. `ecological_capacity_portability.py` shows that different abundance-capacity domains factor to the same capped macro-law. `budgeted_depletion_blanket.py` sharpens the cap to response threshold plus maximum legal future downward reach.

The structural principle is forward-invariant response fibers: saturation is compressible only while legal futures cannot drive a hidden oversaturated state back across a response boundary.

## 6. Stochastic ecological portability

`stochastic_ecological_portability.py` gives exact stochastic saturation portability when action kernels factor through the capped state. Positive depletion can restore full exact abundance distinguishability.

`continuous_time_depletion_reach.py`, `per_capita_mortality_reach.py`, and `finite_horizon_stochastic_saturation.py` then separate exact non-portability from capacity-independent finite-horizon approximate macros with explicit path-TV error.

## 7. Hidden cross-guild coupling

`cross_guild_stochastic_coupling.py` shows that hidden saturated abundance remains relevant when it changes a downstream guild kernel. The saturated-tail hazard diameter

\[
\delta
=
\max_{A\ge L_A}p(A)-\min_{A\ge L_A}p(A)
\]

is zero exactly when the capped two-guild macro is exact; otherwise the sharp one-step minimax common-macro TV error is `delta/2`.

This package is one-way coupling: hidden state changes a downstream transition, but the downstream ecological transition does not rewrite the future accessibility structure that exposed the hidden state.

## 8. Spatial dispersal and reachability

`spatial_dispersal_reachability.py` treats spread on a fixed directed patch graph. Unlimited exact response equivalence is directed target distance plus one unreachable class. Under a prefix grammar with at most `H` future spreads,

\[
|P_H|=\min(D,H)+2.
\]

Thus finite future horizon gives a graph-size-independent exact macro even when raw occupancy state space grows exponentially. The graph itself is fixed in this package.

## 9. Endogenous-accessibility feedback package

The former five-state triage candidate is now a two-sided scalable theorem program.

### 9.1 Scalable feedback rank — `feedback_gate_rank.py`, PR #204

There are `r` latent interaction modes. On the canonical initial slice, all profiles share the same current output, facilitator count, target count, currently open accessibility gates, and static gate distance.

A fixed primitive alphabet

\[
\{0,1,\mathsf{spread},\mathsf{turnover}\}
\]

addresses one gate and exposes its mode only through

\[
\operatorname{addr}(i)
\;\mathsf{spread}\;
\mathsf{turnover}\;
\mathsf{spread}.
\]

The final response is `1-m_i`, so all `2^r` latent profiles are exact-future distinguishable:

\[
\boxed{K_{\rm feedback}=r.}
\]

The first separating horizon is

\[
\boxed{\lceil\log_2 r\rceil+3.}
\]

The family also gives an exact cycle-necessity result. If mode no longer controls turnover-induced facilitator loss, or if later spread ignores facilitator/accessibility state, then every latent profile becomes response-equivalent under every future word:

\[
\boxed{K_{\rm ablated}=0.}
\]

The memory burden is therefore caused by the complete ecological feedback path, not by hidden-state cardinality alone.

### 9.2 Bounded-type changing-domain portability — `feedback_type_portability.py`, PR #205

For one copy-anonymous interaction type with arbitrary physical replication `n`, the reachable microstate count is

\[
2^{n+2}-2,
\]

but the canonical exact quotient is always the same five states:

1. empty-unreachable;
2. ready-resilient;
3. ready-fragile;
4. occupied-resilient;
5. occupied-no-recovery.

The five-state transition table is independent of `n`.

For a fixed number `q` of interaction types and arbitrary replication vector `(n_1,...,n_q)`, the product quotient is exactly

\[
\boxed{|Q|=5^q,\qquad K=q\log_2 5,}
\]

while the physical reachable state count is

\[
\prod_{j=1}^q\left(2^{n_j+2}-2\right).
\]

Thus different physical domains share one exact macro state space and one transition table without state-by-state micro correspondence.

### 9.3 Structural boundary now visible

The exact positive/negative pair shows that raw network size is not the controlling quantity in these classes. What matters is the number of **future-response-distinct feedback types/modes exposed by the grammar**.

- fixed copy-anonymous type rank ⇒ capacity-independent exact portability;
- independently addressable mode rank ⇒ linear exact memory growth.

This is stronger than the former five-state nonreducibility witness but still not a universal classification of arbitrary evolving feedback networks.

## 10. Mechanism-to-data bridge and application boundary

`docs/mechanism_to_data_bridge_2026-08-14.md` remains the generic application-control layer. A feedback application additionally needs observations or interventions on a causal cycle of the form

\[
\text{interaction/state}
\to
\text{turnover/persistence change}
\to
\text{accessibility/movement change}
\to
\text{later response}.
\]

Static occurrence/suitability associations alone cannot identify the new feedback mechanism.

## 11. Remaining feedback mathematics

Do not add another gate witness or a generic symmetry/lumpability reformulation.

The next serious feedback theorem must handle systems where response-equivalent feedback types themselves can **merge, split, or change membership over time**. A useful result would provide a structural invariant controlling whether that evolving feedback-type rank stays bounded, or a matching obstruction showing that legal feedback dynamics generate unboundedly many future-response-distinct types despite a small instantaneous description.

## 12. Companion, legacy, and historical gates

`identifiability_companion` remains the epistemic package for delayed exposure, adaptive finite-evidence no-go, and candidate-mechanism uncertainty. Experimental-design branches remain legacy. Non-nested replacement/rewiring stays centered in `zuizui0223/mltr`.

Issue #122/#185 remains the historical compiler gate for first-paper realization wording. H1–H4 require primary construction pages. The hypothesis-recovery snapshot remains pinned separately and is not rewritten by later theorem progress.

## 13. Workflow discipline

Analytic proof and finite replay remain separate. Green CI cannot rescue an over-broad claim. New theorem work must state semantic domain, legal grammar, exact/approximate resource contract, and explicit non-claims.

## Navigation

- `fixed_regular_extremal_theorem_2026-08-13.md`
- `action_grammar_closure_converse_2026-08-13.md`
- `grammar_expansion_closure_converse_2026-08-13.md`
- `grammar_interface_reuse_2026-08-13.md`
- `terminal_grammar_portability_2026-08-13.md`
- `retention_boundary_time_tradeoff_2026-08-14.md`
- `staged_materialization_prefix_2026-08-14.md`
- `ecological_saturation_blanket_2026-08-14.md`
- `ecological_capacity_portability_2026-08-14.md`
- `budgeted_depletion_blanket_2026-08-14.md`
- `stochastic_ecological_portability_2026-08-14.md`
- `finite_horizon_stochastic_saturation_2026-08-14.md`
- `cross_guild_stochastic_coupling_2026-08-14.md`
- `spatial_dispersal_reachability_2026-08-14.md`
- `feedback_gate_rank_theorem_2026-08-14.md`
- `feedback_type_portability_2026-08-14.md`
- `mechanism_to_data_bridge_2026-08-14.md`
- `hypothesis_recovery_canonical_index_2026-08-14.md`
- `research_priorities.md`
