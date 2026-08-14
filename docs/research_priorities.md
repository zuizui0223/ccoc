# Research priorities — 2026-08-14 post-bridge/cleanup decision

> **Status:** canonical agenda after the exact converse/reuse, chain/resource, deterministic ecological, stochastic ecological, hidden cross-guild, spatial reachability, mechanism-to-data bridge, and first infrastructure-cleanup passes.

## Governing decision

CCOC no longer has one active task. It has a stable first-paper core, established follow-up mathematics, an application/falsification bridge, a historical novelty gate, manuscript-transfer work, and compatibility/cleanup debt.

The first-paper mathematical spine remains

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

Another nearby quotient, cap, mortality/depletion special case, generic information inequality, or elementary reachability variant is not a priority. New mathematics must add a genuinely richer mechanism or a qualitatively new portability constraint.

Historical firstness and theorem validity remain separate. H1--H4 controls the historical wording of the bounded-local realization, not the existence of the mathematical theorem package.

## Established mathematical packages

### 1. Exact converse and reuse

- `action_grammar_closure.py`: one-state action-language expansion; stable closure equals the canonical open quotient; zero inflation iff newly legal actions descend.
- `grammar_expansion_closure.py`: globally-new-symbol finite grammar expansion; old action columns are frozen and stable open-row closure computes the canonical open quotient.
- `grammar_interface_reuse.py`: arbitrary same-domain grammar change; canonical quotients may be equal, finer, coarser, or incomparable; reuse of the closed labeling is iff open rows descend on closed fibers.

The #163 coarsening counterexample permanently blocks an unconditional claim that grammar mutation always refines the canonical quotient.

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

`terminal_grammar_portability.py` gives terminal-stage control of a common exact interface. `portability_adaptation_tradeoff.py` gives

\[
I(E;C)+I(E;U\mid C)
\ge
m-\sum_j h_2(\varepsilon_j).
\]

The boundary-time and staged-prefix results separate retained information, reopening update information, full-interface installation time, selected-query latency, and exposure deadlines.

### 4. Deterministic ecological structure

`ecological_saturation_blanket.py`, `ecological_capacity_portability.py`, and `budgeted_depletion_blanket.py` show that finite blankets arise from forward-invariant response fibers and bounded future downward reach. In particular,

\[
Z_g=\min(L_g,N_g)
\]

is exact under the declared monotone contract, and a remaining downward-reach budget `D` raises the necessary exact cap to `L+D`.

### 5. Stochastic ecological portability

`stochastic_ecological_portability.py`, `continuous_time_depletion_reach.py`, `per_capita_mortality_reach.py`, and `finite_horizon_stochastic_saturation.py` separate exact stochastic causal relevance from finite-horizon approximate portability. Positive downward rate can restore full exact abundance distinguishability while a capacity-independent finite-horizon macro remains accurate.

### 6. Hidden cross-guild coupling

`cross_guild_stochastic_coupling.py` quantifies failure of a capped guild abstraction through the saturated-tail downstream hazard diameter

\[
\delta=\sup_{A\ge L_A}p(A)-\inf_{A\ge L_A}p(A).
\]

Exact capped portability holds iff `delta=0`; the sharp one-step minimax common-macro TV error is `delta/2`.

### 7. Spatial dispersal/reachability

`spatial_dispersal_reachability.py` reduces arbitrary occupied-patch subsets to directed reachability depth relative to the focal target. Unlimited exact response classes are `D+2`; with at most `H` legal spread steps the initial quotient has

\[
|P_H|=\min(D,H)+2.
\]

Thus a long finite corridor and a true barrier can be equivalent under a short future grammar but differ once the legal future horizon expands.

### 8. Mechanism-to-data bridge

`docs/mechanism_to_data_bridge_2026-08-14.md` is now established claim/application control.

It specifies observable and falsification contracts for:

- saturation threshold `L`;
- downward-reach budget `D`;
- mortality/depletion rate `mu`;
- hidden cross-guild hazard diameter `delta`;
- directed dispersal edges;
- future horizon `H`;
- within-guild exchangeability;
- information-flow quantities where semantic variables are observable.

It also distinguishes `SUPPORTED AT CURRENT RESOLUTION`, `APPROXIMATE`, `FALSIFIED`, and `UNIDENTIFIED`. `UNIDENTIFIED` is explicitly not evidence for exact compression.

Actual data fitting, uncertainty estimation, model selection, and case-study claims remain outside the theorem core.

## Novelty discipline

Do not spend novelty budget on fixed-grammar minimization, right congruences, common refinement, generic partition algorithms, Fano, finite-alphabet entropy, deadline scheduling, threshold aggregation, lumpability, Poisson/binomial survival, Bernoulli TV calculations, shortest paths, or graph reachability by themselves.

The live first-paper firstness candidate remains the **simultaneous constrained extremal realization**. Historical firstness remains conditional on the H1--H4 compiler audit. The resource/ecological packages are substantive extensions but need separate prior-art gates before stronger historical novelty language.

## Priority 1 — finish the H1--H4 historical compiler gate

Issue #122 remains the historical comparison gate, with execution in #185 and Ullman--Weiner construction pages in #137.

The current fastest H1 route is the original Weiner--Hopcroft 1968 two-page `Proceedings of the IEEE` item, with Tohoku local access first. Report no. 61 remains the main full H1--H4 construction source. The 1967 predecessor is a targeted H2/H3 semantics source.

Do not restart broad modular-synthesis searching and do not change H1--H4 from abstracts, metadata, or failed retrieval.

## Priority 2 — manuscript transfer

Use `docs/manuscript_transfer_manifest_2026-08-14.md` and issue #192.

The first-paper proof dependency graph is CORE-1 through CORE-5 plus the fixed-regular extremal strengthening. Converse/resource/ecological/stochastic/spatial packages are follow-up or appendix material unless an explicit editorial decision changes scope.

The remaining manual repository-creation blocker is issue #141. Transfer must pin one immutable CCOC SHA and replay theorem registry, paper-core verification, and full pytest on that pin.

## Priority 3 — choose the application path

The generic theorem-to-data bridge is complete. The next application step should therefore be a **dedicated application package/repository with one declared biological mechanism family**, not more generic prose inside CCOC.

Before creating such a package, choose an application that can actually observe or manipulate at least one of the theorem quantities (`L`, `D`, `mu`, `delta`, directed edges, `H`) and can distinguish `FALSIFIED` from `UNIDENTIFIED`.

Do not add fitted data or empirical constants to the CCOC theorem registry.

## Priority 4 — only genuinely richer new ecology mathematics

If new theory is pursued before/alongside an application, the target must add dynamics absent from the existing packages. A serious candidate is **bidirectional colonization/extinction coupled to nontrivial interaction-network feedback**, where the same interaction state changes both future reachability and downstream transition kernels.

A useful new theorem would have to show something not reducible to:

- another abundance cap;
- another one-way mortality/depletion clock;
- another Bernoulli tail-diameter calculation;
- another shortest-distance shell;
- or a direct product of already-proved bounds.

The target should expose a new closure/portability condition, a new failure mode, or a sharp tradeoff created specifically by feedback between movement, extinction, and interaction structure.

## Priority 5 — repository cleanup and compatibility migration

PR #194 removed the duplicate generic `ci.yml` and established `tests.yml` as the single generic non-legacy full-suite matrix. `docs/core_surface_cleanup_manifest_2026-08-14.md` records KEEP / REMOVE NOW / DEFER decisions.

Do not bulk-delete specialized workflows: generic pytest excludes `legacy` tests, and inspected theorem workflows also generate dedicated replay artifacts. Workflow deletion must be file-specific.

`causal_model/__init__.py` and `current_theory.py` remain compatibility surfaces because in-repository historical consumers still use them. The next high-value cleanup is consumer migration, not facade deletion. Physical relocation into a legacy namespace waits for an immutable manuscript source pin and preserved replay mapping.

## Explicit non-priorities

No new codebook families, partition-defect identities, panel/reset variants, same-domain quotient reformulations, capped-count special cases, additional one-guild mortality/depletion variants, elementary cross-guild Bernoulli variants, elementary shortest-path variants, generic Fano/channel lemmas, generic contraction/small-gain results, generic source searching, replacement/rewiring transport inside CCOC, empirical fitting inside the theorem core, or bulk deletion of historical replay workflows.
