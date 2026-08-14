# Current RACH/CCOC architecture — 2026-08-14

## Purpose

CCOC now separates seven questions:

1. what is the exact response interface for one declared future grammar;
2. when does opening force refinement;
3. when can a chosen closed interface still be reused;
4. what memory/update/boundary-time resources are required across openings;
5. when can one exact macro-law survive changing semantic domains;
6. which ecological structures create or destroy finite blankets;
7. when exact stochastic non-portability can still admit a finite-horizon approximate portable macro.

The July v1 theorem IDs remain reproducibility anchors. Post-reopening results strengthen the research surface without rewriting those historical IDs.

## 1. Structural portability core

Preferred historical entrance:

```python
import causal_model.portability_core as rach
```

The v1 spine remains exact grammar-aware interfaces, cross-grammar obstruction, bounded-local relay sharpness, and conservative positive portability. Newer converse, resource, and ecological modules are explicit theorem surfaces rather than automatically expanding this already broad facade.

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

### Terminal exact memory

`terminal_grammar_portability.py` proves that for valid globally-new-symbol grammar chains,

\[
K_{\rm uniform}=\log_2|P_{\rm terminal}|.
\]

The same terminal labels realize one `ConservativeMacroSchema` at every stage.

### Retention and stochastic update information

`portability_adaptation_tradeoff.py` gives

\[
I(E;C)+I(E;U\mid C)
\ge
m-\sum_jh_2(\varepsilon_j).
\]

Randomized/noisy updates are therefore already covered at the information-flow level. A mechanism-specific theorem enters by bounding or constructing `I(E;U|C)`.

### Boundary time and staged deadlines

`retention_boundary_time_tradeoff_2026-08-14.md` converts update information into finite-boundary time. In the fixed-regular relay, one selected query is `Theta(log m)` while exact full-interface installation across the focal cut is `Omega(m)`.

`staged_materialization_prefix_2026-08-14.md` adds exposure deadlines. In the exact binary/power-of-two subclass the prefix inequalities are necessary and sufficient, so eventual shared memory and online installation schedule are distinct resources.

## 5. Deterministic ecological structural package

### Saturation blanket

`ecological_saturation_blanket.py` derives

\[
Z_g=\min(L_g,N_g)
\]

as an exact dynamic blanket under non-negative guild colonization. Its state count

\[
\prod_g(L_g+1)
\]

is independent of abundance capacities because saturated response fibers are forward-invariant.

### Changing-domain capacity portability

`ecological_capacity_portability.py` shows that distinct abundance domains with different capacity vectors factor to one common capped macro-domain and the same capacity-free transition law.

### Bounded disturbance grammar

`budgeted_depletion_blanket.py` shows that if at most `D` future depletion events remain legal, then

\[
|P_{\rm initial}|=L+D+1.
\]

The needed exact abundance cap is response threshold plus maximum legal future downward reach.

## 6. Stochastic ecological package

### Exact controlled-Markov saturation portability

`stochastic_ecological_portability.py`

If non-negative colonization increments are generated from action-specific laws

\[
Q_a(D\mid Z)
\]

that depend only on capped guild state, then

\[
Z'=\min(L,Z+D)
\]

induces one exact stochastic macro kernel independent of hidden oversaturation and independent of capacity. The same stochastic macro law is portable across changing abundance domains.

The same module gives the stochastic depletion boundary. Any depletion probability `p>0` breaks exact saturation lumping; `N=L` and `L+1` have one-step response rows at TV distance `p`, so any common one-step row incurs at least `p/2` worst-case TV error. Repeated attempts distinguish all abundances, restoring `M+1` exact open classes.

### Continuous-time rare disturbance

`continuous_time_depletion_reach.py`

For a constant total depletion rate `mu`, exact complexity is `L+1` at `mu=0` and `M+1` for every `mu>0`. The threshold-pair event gap is

\[
\mu t e^{-\mu t},
\]

maximized at `t=1/mu` with value `1/e`.

### Per-capita mortality

`per_capita_mortality_reach.py`

Under independent per-capita mortality, `N_t|N_0=n` is binomial with survival probability

\[
q=e^{-\mu t}.
\]

Every positive rate restores full exact abundance distinguishability. The threshold-pair gap

\[
Lq^L(1-q)
\]

is maximized at `q=L/(L+1)`, giving a rate-adapted informative horizon.

### Positive finite-horizon approximate portability

`finite_horizon_stochastic_saturation.py`

Exact non-portability does not force finite-horizon approximate non-portability. Across arbitrarily large capacities, one `L+1`-state saturation macro has worst saturated path-TV error

\[
1-e^{-\mu T}
\]

for the constant-rate depletion clock and

\[
1-e^{-\mu LT}
\]

for per-capita mortality. Exact response state count may grow as `M+1` while approximate macro size/error remain capacity-independent.

This is the first completed stochastic macro-dynamics package in CCOC. Additional one-guild mortality variants are not an active target.

## 7. Companion and legacy packages

`identifiability_companion` remains the epistemic package for delayed exposure, adaptive finite-evidence no-go, and candidate-mechanism uncertainty.

`approximate_addressability.py` remains the finite Fano substrate. Its role is now complemented by the constructed stochastic ecological macro above rather than standing as the only approximate result.

`current_theory.py` remains a compatibility aggregate, not the preferred research entrance. Experimental-design branches remain legacy. Non-nested replacement/rewiring remains centered in `zuizui0223/mltr`.

## 8. Historical novelty gate

Issue #122 remains the main first-paper historical gate. The concrete acquisition/extraction instructions are retained on `main` in

`docs/primary_source_request_handoff_2026-08-13.md`.

H1–H4 must be decided from primary construction pages, not titles or abstracts.

## 9. Workflow discipline

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
- `primary_source_request_handoff_2026-08-13.md`
- `research_priorities.md`
- `theorem_registry.md`
