# Research priorities — 2026-08-14 post-stochastic decision

> **Status:** canonical agenda after the exact converse/reuse, chain/resource, deterministic ecological, and stochastic ecological portability passes.

## Governing decision

The finite exact core and the first stochastic ecological extension are mature enough that another nearby quotient, cap, mortality variant, codebook, or generic information inequality is not a priority.

The first-paper spine remains:

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

The main first-paper uncertainty is still historical: whether classical uniform sequential-machine compilation already supplies the complete bounded-local realization package. Theorem validity and historical firstness are separate.

## Established mathematics

### 1. Exact converse and reuse

- `action_grammar_closure.py`: one-state action-language expansion; stable closure equals the canonical open quotient; zero inflation iff newly legal actions descend.
- `grammar_expansion_closure.py`: finite grammar-state globally-new-symbol expansion; old action columns are frozen; stable open-row closure computes the canonical open quotient.
- `grammar_interface_reuse.py`: arbitrary same-domain grammar change; canonical quotients may be equal, finer, coarser, or incomparable; the closed labeling is reusable iff open enabled/successor rows descend on its fibers.

The #163 coarsening counterexample permanently rules out the slogan that every grammar mutation refines the canonical product-state quotient.

### 2. Fixed-regular extremal family

For every `m>=1`, the fixed four-symbol relay family has

\[
|P_C|=2,
\qquad |P_O|=2^{m+1},
\qquad K_O-K_C=m,
\]

with one newly legal primitive action, bounded local state/message alphabets, radius-one dynamics, degree at most three, tree topology, focal/exterior cut one, and exact selected-coordinate access

\[
2\lceil\log_2m\rceil+2.
\]

The memory gap saturates finite-domain capacity. Constant cut width, degree, local alphabets, and grammar-edit count therefore do not imply a system-size-independent exact interface bound.

### 3. Chain and coupled-resource portability

`terminal_grammar_portability.py` gives

\[
K_{\rm uniform}=\log_2|P_{\rm terminal}|,
\]

and terminal labels construct one `ConservativeMacroSchema` across a valid globally-new-symbol chain.

`portability_adaptation_tradeoff.py` gives the stochastic information-flow form

\[
I(E;C)+I(E;U\mid C)
\ge
m-\sum_j h_2(\varepsilon_j).
\]

`retention_boundary_time_tradeoff_2026-08-14.md` converts adaptation debt into boundary time. In the fixed-regular relay, exact full-interface installation is `Omega(m)` while one selected query is `Theta(log m)`.

`staged_materialization_prefix_2026-08-14.md` gives prefix installation constraints. In the exact binary/power-of-two subclass,

\[
k+\sum_{q\le t}L_q\ge m_t\quad\forall t
\]

is necessary and sufficient. Terminal shared memory can be path-independent while online installation is deadline-sensitive.

### 4. Deterministic ecological structural package

`ecological_saturation_blanket.py` derives a system-size-independent exact blanket. For guild abundance `N_g`, saturation threshold `L_g`, and non-negative colonization increments,

\[
Z_g=\min(L_g,N_g),
\qquad
Z'_g=\min(L_g,Z_g+d_g).
\]

The exact blanket has `prod_g(L_g+1)` states independent of capacity `M_g`. The structural reason is forward invariance of saturated response fibers.

`ecological_capacity_portability.py` strengthens this to changing semantic domains: distinct capacity vectors realize the same capped macro-domain and the same capacity-free macro transition law.

`budgeted_depletion_blanket.py` quantifies future downward reach. If at most `D` depletion events remain legal,

\[
|P_{\rm initial}|=L+D+1,
\]

so

\[
\boxed{\text{needed abundance cap}=\text{response threshold}+\text{maximum legal future downward reach}.}
\]

`D=0` recovers saturation and `D=M-L` recovers full abundance.

### 5. Stochastic ecological portability package

`stochastic_ecological_portability.py` gives an exact controlled-Markov positive theorem. If non-negative colonization increments are drawn from laws

\[
Q_a(D\mid Z)
\]

that depend only on capped guild state `Z`, then

\[
Z' = \min(L,Z+D)
\]

induces one exact stochastic macro kernel independent of hidden oversaturation and independent of capacity `M`. The same kernel is portable across changing abundance domains.

The same module gives the stochastic depletion boundary. A one-unit depletion action with any probability `p>0` makes `N=L` and `L+1` differ at one step by TV distance `p`; any common one-step transition row incurs at least `p/2` worst-case TV error. Repeated depletion attempts distinguish every saturated abundance, so exact open state count is `M+1`.

`continuous_time_depletion_reach.py` gives the constant-rate continuous-time corollary. Exact complexity jumps from `L+1` at rate zero to `M+1` at every positive rate. For the threshold pair, a finite-time event gap is

\[
\mu t e^{-\mu t},
\]

maximized at `t=1/mu` with value `1/e`.

`per_capita_mortality_reach.py` gives the independent per-capita mortality mechanism. With

\[
q=e^{-\mu t},
\]

the threshold-pair gap is

\[
Lq^L(1-q),
\]

maximized at

\[
q=L/(L+1),
\qquad
t^*=\mu^{-1}\log((L+1)/L).
\]

Every positive mortality rate again restores full exact abundance distinguishability.

`finite_horizon_stochastic_saturation.py` supplies the positive approximate counterpart. Across arbitrarily large capacities, the `L+1`-state saturated macro has worst saturated path-TV error

\[
\boxed{1-e^{-\mu T}}
\]

for constant-rate depletion and

\[
\boxed{1-e^{-\mu LT}}
\]

for per-capita mortality. Thus exact state count can grow as `M+1` while finite-horizon approximate macro size and error remain capacity-independent.

This closes the first intended stochastic ecological pass: exact causal relevance, finite-horizon detectability, and approximate portability are now explicitly separated.

## Novelty discipline

Do not spend novelty budget on fixed-grammar minimization, right congruences, common refinement, generic partition algorithms, Fano, finite-alphabet entropy, deadline scheduling, threshold aggregation, lumpability, Poisson/binomial survival, or total variation by themselves.

The live first-paper firstness candidate remains the **simultaneous constrained extremal realization**. Historical firstness remains conditional on the H1–H4 compiler audit. The chain/resource and ecological packages are substantive CCOC extensions, but their classical ingredients are substrate unless separately audited.

## Priority 1 — H1–H4 compiler gate

Issue #122 remains the main historical gate:

- **H1:** bounded local state/connectivity independent of source state count;
- **H2:** fixed context-independent source controls/input distribution;
- **H3:** two-way response-trace faithfulness without spurious closed distinctions;
- **H4:** bounded source-step/network/output latency.

The concrete acquisition actions are now retained on `main` in `docs/primary_source_request_handoff_2026-08-13.md`. Do not restart generic source searching; read the primary construction pages when recovered.

## Priority 2 — manuscript transfer

Transfer the established spine with exact SHA/replay provenance. Separate exact theorem statements, classical ancestry, the conditional realization novelty candidate, and the fallback interpretation if H1–H4 subsumes realization existence.

The stochastic/ecological results should be presented as extensions unless a separate prior-art audit justifies stronger novelty language.

## Priority 3 — genuinely new mechanism classes only

1. **Spatial dispersal/reachability ecology.** Derive a blanket or lower bound from explicit colonization barriers, reachability, or network constraints rather than another threshold-count variant.
2. **Hidden cross-guild stochastic coupling.** The capped-state-driven kernel theorem is positive. A genuinely new result would quantify what happens when hidden oversaturation in one guild modulates another guild's colonization or extinction rates; merely restating lumpability is not enough.
3. **Mechanism-to-data bridge.** If an application is pursued, identify which rates, thresholds, or exchangeability assumptions could be estimated or falsified from ecological data. Empirical inference itself remains outside this theorem repository unless a dedicated application package is created.

## Explicit non-priorities

No new codebook families, partition-defect identities, panel/reset variants, same-domain quotient reformulations, capped-count special cases, additional one-guild mortality/depletion variants, generic Fano/channel lemmas, generic contraction/small-gain results, generic source searching, replacement/rewiring transport inside CCOC, or empirical fitting inside the theorem core.
