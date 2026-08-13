# Current RACH/CCOC architecture — 2026-08-14

## Purpose

CCOC now separates six questions:

1. what is the exact response interface for one declared future grammar;
2. when does opening force refinement;
3. when can a chosen closed interface still be reused;
4. what memory/update/boundary-time resources are required across openings;
5. when can one exact macro-law survive changing semantic domains;
6. which explicit ecological structures create or destroy such finite blankets.

The July v1 theorem IDs remain reproducibility anchors. Post-reopening results strengthen the research surface without rewriting those historical IDs.

## 1. Structural portability core

Preferred historical entrance:

```python
import causal_model.portability_core as rach
```

The v1 spine remains exact grammar-aware interfaces, cross-grammar obstruction, bounded-local relay sharpness, and conservative positive portability.

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

`portability_adaptation_tradeoff.py` uses the strong form

\[
I(E;C)+I(E;U\mid C)
\ge
m-\sum_jh_2(\varepsilon_j).
\]

This already allows randomized/noisy updates. A model-specific mechanism enters by proving an upper bound on `I(E;U|C)`.

### Boundary time and staged deadlines

`retention_boundary_time_tradeoff_2026-08-14.md` converts update information into a finite-boundary time lower bound. In the fixed-regular relay, one selected query is `Theta(log m)` while exact full-interface installation across the focal cut is `Omega(m)`.

`staged_materialization_prefix_2026-08-14.md` adds exposure deadlines. In the exact binary/power-of-two subclass the prefix inequalities are necessary and sufficient, so eventual shared memory and online installation schedule are distinct resources.

## 5. Ecological structural package

These modules are explicit theorem surfaces rather than imports added to the already broad `portability_core` facade.

### Saturation blanket

`ecological_saturation_blanket.py`

For guild abundance `N_g`, response threshold `L_g`, and non-negative colonization increments,

\[
Z_g=\min(L_g,N_g)
\]

forms an exact dynamic blanket with

\[
|Z|=\prod_g(L_g+1)
\]

states independent of abundance capacities. The key structural property is that saturated response fibers are forward-invariant under the legal colonization grammar.

Opening one depletion action breaks fiber descent and can restore all hidden abundance states.

### Changing-domain capacity portability

`ecological_capacity_portability.py`

Different abundance domains with different capacity vectors `M` factor to the same capped macro-domain and the same transition

\[
Z'_g=\min(L_g,Z_g+d_g).
\]

This is a changing-domain factor-map theorem, not a same-domain partition reuse theorem.

### Bounded disturbance grammar

`budgeted_depletion_blanket.py`

With threshold `L` and at most `D` future depletion events, the exact initial interface has

\[
|P_{\rm initial}|=L+D+1.
\]

Thus the exact abundance cap equals the response threshold plus maximum legal future downward reach. `D=0` gives irreversible saturation; `D=M-L` gives the full abundance state.

## 6. Companion and legacy packages

`identifiability_companion` remains the epistemic package for delayed exposure, adaptive finite-evidence no-go, and candidate-mechanism uncertainty.

`approximate_addressability.py` remains the finite Fano robustness substrate. The newer stochastic information-flow statement belongs to the portability resource layer above; a model-specific stochastic ecological mechanism is still future work.

`current_theory.py` remains a compatibility aggregate, not the preferred research entrance. Experimental-design branches remain legacy. Non-nested replacement/rewiring remains centered in `zuizui0223/mltr`.

## 7. Workflow discipline

Analytic proofs and finite certificates remain separate evidence layers. A green workflow does not rescue an over-broad theorem statement; #163 remains the canonical example. New work must state its semantic domain, grammar, resource contract, and scope boundary explicitly and preserve the July replay.

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
- `research_priorities.md`
- `theorem_registry.md`
