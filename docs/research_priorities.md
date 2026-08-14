# Research priorities — 2026-08-14 post-spatial decision

> **Status:** canonical agenda after the exact converse/reuse, chain/resource, deterministic ecological, stochastic ecological, hidden cross-guild, and spatial reachability theorem passes.

## Governing decision

The active theorem package is now broad enough that another nearby quotient, cap, mortality/depletion variant, generic information inequality, or elementary reachability variant is not a priority.

The first-paper spine remains

\[
\text{response-interface formalism}
+
\text{cross-grammar obstruction}
+
\text{extremal one-action witness}
+
\text{bounded-local realization}
+
\text{positive/reuse boundary}.
\]

The main first-paper uncertainty is historical: whether classical uniform sequential-machine compilation already supplies the complete bounded-local realization package. Theorem validity and historical firstness remain separate.

## Established mathematics

### 1. Exact converse and reuse

- `action_grammar_closure.py`: one-state action-language expansion; stable closure equals the canonical open quotient; zero inflation iff newly legal actions descend.
- `grammar_expansion_closure.py`: globally-new-symbol finite grammar expansion; old action columns are frozen and stable open-row closure computes the canonical open quotient.
- `grammar_interface_reuse.py`: arbitrary same-domain grammar change; canonical quotients may be equal, finer, coarser, or incomparable; reuse of the closed labeling is iff open rows descend on closed fibers.

The #163 coarsening counterexample permanently rules out an unconditional claim that grammar mutation refines the canonical quotient.

### 2. Fixed-regular extremal family

For every `m>=1`, the fixed four-symbol relay family has

\[
|P_C|=2,
\qquad |P_O|=2^{m+1},
\qquad K_O-K_C=m,
\]

with one newly legal primitive action, bounded local state/message alphabets, radius-one dynamics, degree at most three, tree topology, focal/exterior cut one, and selected-coordinate access

\[
2\lceil\log_2m\rceil+2.
\]

The memory gap saturates finite-domain capacity. Constant cut width, degree, local alphabets, and grammar-edit count do not imply a system-size-independent exact interface bound.

### 3. Chain and coupled-resource portability

`terminal_grammar_portability.py` gives

\[
K_{\rm uniform}=\log_2|P_{\rm terminal}|,
\]

and terminal labels construct one `ConservativeMacroSchema` across a valid globally-new-symbol chain.

`portability_adaptation_tradeoff.py` gives

\[
I(E;C)+I(E;U\mid C)
\ge
m-\sum_jh_2(\varepsilon_j).
\]

`retention_boundary_time_tradeoff_2026-08-14.md` turns adaptation debt into boundary time; in the fixed-regular relay, exact full-interface installation is `Omega(m)` while one selected query is `Theta(log m)`.

`staged_materialization_prefix_2026-08-14.md` gives exact prefix deadlines in the binary/power-of-two subclass:

\[
k+\sum_{q\le t}L_q\ge m_t\quad\forall t
\]

is necessary and sufficient. Terminal shared memory can be path-independent while online installation is deadline-sensitive.

### 4. Deterministic ecological structural package

`ecological_saturation_blanket.py` gives the exact capped-guild blanket

\[
Z_g=\min(L_g,N_g),
\qquad
Z'_g=\min(L_g,Z_g+d_g)
\]

under non-negative colonization. The state count `prod_g(L_g+1)` is independent of abundance capacities because saturated response fibers are forward-invariant.

`ecological_capacity_portability.py` extends this to changing semantic domains: different capacity vectors factor to the same capped macro-domain and capacity-free macro transition law.

`budgeted_depletion_blanket.py` quantifies future downward reach. If at most `D` future depletion events remain legal,

\[
|P_{\rm initial}|=L+D+1,
\]

so the needed exact abundance cap is response threshold plus maximum legal future downward reach.

### 5. Stochastic ecological portability package

`stochastic_ecological_portability.py` gives an exact controlled-Markov positive theorem. If non-negative colonization increments are generated from `Q_a(D|Z)`, then the capped process induces one stochastic macro kernel independent of hidden oversaturation and abundance capacity.

A positive-probability depletion action breaks exact saturation lumping; `N=L` and `L+1` have one-step response rows at TV distance `p`, and repeated attempts restore all `M+1` exact abundance classes.

`continuous_time_depletion_reach.py` and `per_capita_mortality_reach.py` show that every positive downward rate restores full exact abundance distinguishability while finite-horizon detectability is governed by a rate-adapted time scale.

`finite_horizon_stochastic_saturation.py` supplies the positive approximate counterpart. Across unbounded capacities, the `L+1`-state saturated macro has worst saturated path-TV error

\[
1-e^{-\mu T}
\]

for a constant total depletion clock and

\[
1-e^{-\mu LT}
\]

for per-capita mortality. Exact state count may grow as `M+1` while finite-horizon approximate macro size/error remain capacity-independent.

### 6. Hidden cross-guild coupling

`cross_guild_stochastic_coupling.py` makes the stochastic lumpability boundary mechanistic rather than assumed.

Guild A is response-capped at `L_A`, while hidden A abundance modulates recruitment probability `p(A)` of guild B. Define the hidden saturated-tail hazard diameter

\[
\delta
=
\max_{A\ge L_A}p(A)-\min_{A\ge L_A}p(A).
\]

Then capped `(Z_A,Z_B)` is an exact stochastic macro iff

\[
\boxed{\delta=0.}
\]

If `delta>0`, the sharp one-step minimax TV error for any single saturated-A macro hazard is

\[
\boxed{\delta/2},
\]

attained by the midpoint hazard. Repeated controlled recruitment has path-TV bound

\[
\boxed{1-(1-\delta/2)^H\le H\delta/2.}
\]

Across changing capacity domains, the same fixed `(L_A+1)(L_B+1)`-state approximate macro works with the global saturated-tail hazard diameter. Thus hidden abundance matters precisely through the response-relevant downstream kernel it induces, not through abundance range by itself.

### 7. Spatial dispersal and reachability

`spatial_dispersal_reachability.py` treats an arbitrary occupied-patch subset on a directed graph. One `spread` action adds all outgoing neighbors, and the focal response records whether a target patch is occupied.

Although the occupancy microstate space has `2^|V|` states, unlimited future response equivalence is exactly minimum directed distance to the focal target plus one unreachable class. If `D` is maximum finite directed distance,

\[
\boxed{|P_\infty|=D+2.}
\]

If the declared future grammar allows at most `H` spread steps, the grammar-adaptive capped distance is exact and the initial canonical quotient has

\[
\boxed{|P_H|=\min(D,H)+2.}
\]

Hence fixed `H` gives a graph-size-independent bound `H+2` across changing spatial domains, while unlimited exact memory can grow with reachability depth. True directed barriers remain future-silent; a long but finite corridor is only invisible when it lies beyond the legal future horizon.

## Novelty discipline

Do not spend novelty budget on fixed-grammar minimization, right congruences, common refinement, generic partition algorithms, Fano, finite-alphabet entropy, deadline scheduling, threshold aggregation, lumpability, Poisson/binomial survival, Bernoulli TV calculations, shortest paths, or graph reachability by themselves.

The live first-paper firstness candidate remains the **simultaneous constrained extremal realization**. Historical firstness remains conditional on the H1–H4 compiler audit. The ecological/resource packages are substantive CCOC extensions but should not receive stronger firstness language without dedicated prior-art gates.

## Priority 1 — H1–H4 compiler gate

Issue #122 remains the main historical gate:

- **H1:** bounded local state/connectivity independent of source state count;
- **H2:** fixed context-independent source controls/input distribution;
- **H3:** two-way response-trace faithfulness without spurious closed distinctions;
- **H4:** bounded source-step/network/output latency.

The concrete acquisition actions are retained in `docs/primary_source_request_handoff_2026-08-13.md`. Do not restart generic source searching; read the primary construction pages when recovered.

## Priority 2 — manuscript transfer

Transfer the established spine with exact SHA/replay provenance. Separate exact theorem statements, classical ancestry, the conditional realization novelty candidate, and the fallback interpretation if H1–H4 subsumes realization existence.

The resource/stochastic/ecological results should be presented as extensions unless separate prior-art audits justify stronger novelty language.

## Priority 3 — bridge theory to testable mechanisms, not more theorem variants

1. **Mechanism-to-data bridge.** Identify which thresholds, mortality/depletion rates, cross-guild hazard diameters, directed dispersal edges, or future horizons could be estimated or falsified in an application. Empirical fitting itself should live outside the theorem core unless a dedicated application package is created.
2. **Only materially richer network mechanisms.** Further ecology theory is justified only if it adds genuinely new dynamics—e.g. bidirectional colonization/extinction with nontrivial interaction-network feedback—not another one-guild cap, mortality variant, or elementary distance shell.
3. **Historical and manuscript work take precedence.** New mathematics should not displace the H1–H4 gate or manuscript transfer merely because another nearby finite model can be solved.

## Explicit non-priorities

No new codebook families, partition-defect identities, panel/reset variants, same-domain quotient reformulations, capped-count special cases, additional one-guild mortality/depletion variants, elementary cross-guild Bernoulli variants, elementary shortest-path variants, generic Fano/channel lemmas, generic contraction/small-gain results, generic source searching, replacement/rewiring transport inside CCOC, or empirical fitting inside the theorem core.
