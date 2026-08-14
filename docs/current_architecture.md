# Current RACH/CCOC architecture — 2026-08-14

## Purpose

CCOC now separates eight questions:

1. what is the exact response interface for one declared future grammar;
2. when does opening force refinement;
3. when can a chosen closed interface still be reused;
4. what memory/update/boundary-time resources are required across openings;
5. when can one exact macro-law survive changing semantic domains;
6. which ecological structures create or destroy finite blankets;
7. when exact stochastic non-portability still admits a finite-horizon approximate portable macro;
8. how hidden cross-component coupling and directed spatial reachability expose otherwise compressed ecological distinctions.

The July v1 theorem IDs remain reproducibility anchors. Post-reopening results strengthen the research surface without rewriting those historical IDs.

## 1. Structural portability core

Preferred historical entrance:

```python
import causal_model.portability_core as rach
```

The v1 spine remains exact grammar-aware interfaces, cross-grammar obstruction, bounded-local relay sharpness, and conservative positive portability. Newer converse, resource, ecological, and stochastic modules remain explicit theorem surfaces rather than automatically expanding this already broad facade.

## 2. Exact converse and reuse layers

`action_grammar_closure.py` handles one-state action-language expansion. `grammar_expansion_closure.py` handles finite grammar-state **globally-new-symbol** expansion, where old action columns are frozen and the open canonical quotient genuinely refines the closed quotient. `grammar_interface_reuse.py` handles arbitrary same-domain grammar change, where canonical quotients may instead be equal, finer, coarser, or incomparable.

The correct broad statement is

\[
P_C\text{ reusable as an exact open interface}
\iff
\text{open enabled/successor rows descend on }P_C.
\]

The #163 coarsening counterexample is a permanent scope guard.

## 3. Integrated extremal family

`fixed_regular_grammar_relay.py` and `extremal_open_composition.py` realize, for every `m>=1`,

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

`terminal_grammar_portability.py` proves that for valid globally-new-symbol grammar chains,

\[
K_{\rm uniform}=\log_2|P_{\rm terminal}|.
\]

The same terminal labels realize one `ConservativeMacroSchema` at every stage.

`portability_adaptation_tradeoff.py` gives

\[
I(E;C)+I(E;U\mid C)
\ge
m-\sum_jh_2(\varepsilon_j).
\]

`retention_boundary_time_tradeoff_2026-08-14.md` turns update information into finite-boundary time. In the fixed-regular relay, one selected query is `Theta(log m)` while exact full-interface installation across the focal cut is `Omega(m)`.

`staged_materialization_prefix_2026-08-14.md` adds exposure deadlines. In the exact binary/power-of-two subclass the prefix inequalities are necessary and sufficient, so eventual shared memory and online installation schedule are distinct resources.

## 5. Deterministic ecological structural package

`ecological_saturation_blanket.py` derives

\[
Z_g=\min(L_g,N_g)
\]

as an exact dynamic blanket under non-negative guild colonization. Its state count `prod_g(L_g+1)` is independent of abundance capacities because saturated response fibers are forward-invariant.

`ecological_capacity_portability.py` shows that distinct abundance domains with different capacity vectors factor to one common capped macro-domain and the same capacity-free transition law.

`budgeted_depletion_blanket.py` shows that if at most `D` future depletion events remain legal,

\[
|P_{\rm initial}|=L+D+1,
\]

so the needed exact abundance cap is response threshold plus maximum legal future downward reach.

## 6. Stochastic ecological package

`stochastic_ecological_portability.py` proves exact controlled-Markov saturation portability when action-specific non-negative increment laws have the form

\[
Q_a(D\mid Z).
\]

The induced stochastic macro kernel is independent of hidden oversaturation and capacity. Positive-probability depletion breaks exact saturation lumping and can restore all `M+1` abundance classes.

`continuous_time_depletion_reach.py` and `per_capita_mortality_reach.py` show that every positive downward rate restores full exact abundance distinguishability while finite-horizon detectability is governed by a rate-adapted time scale.

`finite_horizon_stochastic_saturation.py` gives the positive approximate result: across arbitrarily large capacities, one `L+1`-state saturation macro has worst saturated path-TV error `1-exp(-mu*T)` for a constant total depletion clock and `1-exp(-mu*L*T)` for per-capita mortality.

## 7. Hidden cross-guild coupling

`cross_guild_stochastic_coupling.py` relaxes the positive `Q(D|Z)` premise in one explicit ecological direction.

Guild A is capped at `L_A`, but hidden A abundance changes recruitment probability `p(A)` of guild B. Define

\[
\delta
=
\max_{A\ge L_A}p(A)-\min_{A\ge L_A}p(A).
\]

Then the capped two-guild state is an exact stochastic macro iff

\[
\delta=0.
\]

If `delta>0`, a single saturated-A macro transition has sharp minimax one-step TV error

\[
\delta/2,
\]

attained by the midpoint hazard. Repeated controlled recruitment has path-TV bound

\[
1-(1-\delta/2)^H\le H\delta/2.
\]

Across changing capacity domains, one fixed `(L_A+1)(L_B+1)`-state approximate macro remains portable when below-threshold hazards agree and the global saturated-tail hazard diameter is uniformly bounded.

The key conceptual shift is that hidden abundance is relevant only through the response-relevant downstream kernel it induces. Saturation of A's own response does not justify forgetting A if its downstream ecological effects have not also saturated.

## 8. Spatial dispersal and reachability

`spatial_dispersal_reachability.py` treats a finite directed patch graph with arbitrary occupied-patch subsets. One `spread` action monotonically adds every outgoing neighbor; the focal response is occupancy of one target patch.

The microstate space has

\[
2^{|V|}
\]

occupancy states, but unlimited future-response equivalence is exactly minimum directed distance to the focal target plus one unreachable class. If `D` is maximum finite directed distance,

\[
|P_\infty|=D+2.
\]

For a prefix grammar allowing at most `H` future spread actions, the grammar-adaptive capped distance is an exact dynamic interface and the initial canonical quotient has

\[
\boxed{|P_H|=\min(D,H)+2.}
\]

Thus fixed `H` gives a graph-size-independent exact bound `H+2` across changing spatial domains even though the occupancy state spaces can grow exponentially. Removing the horizon bound restores dependence on directed reachability depth.

True directed barriers remain future-silent; long finite corridors are only indistinguishable from barriers when they lie beyond the declared future horizon. This is the spatial counterpart of the abundance disturbance-budget theorem.

## 9. Companion and legacy packages

`identifiability_companion` remains the epistemic package for delayed exposure, adaptive finite-evidence no-go, and candidate-mechanism uncertainty.

`approximate_addressability.py` remains the finite Fano substrate. Its role is complemented by the constructed approximate stochastic ecological macros above.

`current_theory.py` remains a compatibility aggregate, not the preferred research entrance. Experimental-design branches remain legacy. Non-nested replacement/rewiring remains centered in `zuizui0223/mltr`.

## 10. Historical novelty gate

Issue #122 remains the main first-paper historical gate. The concrete acquisition/extraction instructions are retained in

`docs/primary_source_request_handoff_2026-08-13.md`.

H1–H4 must be decided from primary construction pages, not titles or abstracts.

## 11. Workflow discipline

Analytic proofs and finite certificates remain separate evidence layers. A green workflow does not rescue an over-broad theorem statement; #163 remains the canonical example. New work must state semantic domain, grammar, resource/error contract, and scope boundary explicitly and preserve the July replay.

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
- `continuous_time_depletion_reach_2026-08-14.md`
- `per_capita_mortality_reach_2026-08-14.md`
- `finite_horizon_stochastic_saturation_2026-08-14.md`
- `cross_guild_stochastic_coupling_2026-08-14.md`
- `spatial_dispersal_reachability_2026-08-14.md`
- `primary_source_request_handoff_2026-08-13.md`
- `research_priorities.md`
- `theorem_registry.md`
