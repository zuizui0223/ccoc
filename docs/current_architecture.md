# Current RACH/CCOC architecture — 2026-08-14 post-feedback-forgetting

## Purpose

CCOC now has a stable first-paper portability core plus explicit follow-up packages for converse/reuse, resources, deterministic/stochastic ecology, cross-guild coupling, spatial reachability, and endogenous interaction-network feedback.

The July v1 theorem IDs remain reproducibility anchors. Later theorem modules do not silently rewrite the historical paper core.

## 1. Structural portability core

Preferred historical entrance:

```python
import causal_model.portability_core as rach
```

The first-paper spine remains:

\[
\text{exact grammar-aware interface}
+
\text{cross-grammar obstruction}
+
\text{bounded-local extremal witness}
+
\text{conservative portability}
+
\text{future-word fiber-split boundary}.
\]

## 2. Exact converse and reuse

`action_grammar_closure.py` gives the exact one-state action-language expansion converse. `grammar_expansion_closure.py` gives the corrected globally-new-symbol multi-state theorem. `grammar_interface_reuse.py` handles arbitrary same-domain grammar change, where canonical quotients may be equal, finer, coarser, or incomparable.

The broad reuse criterion is

\[
P_C\text{ reusable exactly}
\iff
\text{open enabled/successor rows descend on }P_C.
\]

`terminal_grammar_portability.py` gives the minimum one-labeling exact across a valid globally-new-symbol chain.

## 3. Fixed-regular extremal family

For every `m>=1`, `fixed_regular_grammar_relay.py` / `extremal_open_composition.py` realize

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

under one fixed four-symbol alphabet and one newly legal primitive action, with bounded local alphabets, radius-one dynamics, degree at most three, tree topology, focal/exterior cut one, and selected-coordinate access

\[
2\lceil\log_2m\rceil+2.
\]

## 4. Resource portability

`portability_adaptation_tradeoff.py` gives

\[
I(E;C)+I(E;U\mid C)
\ge
m-\sum_jh_2(\varepsilon_j).
\]

The finite-boundary and staged-prefix results separate retained information, reopening update information, full-interface installation time, selected-query latency, and exposure deadlines.

## 5. Deterministic ecological structure

`ecological_saturation_blanket.py`, `ecological_capacity_portability.py`, and `budgeted_depletion_blanket.py` identify exact finite blankets from forward-invariant response fibers and bounded future downward reach.

The one-guild rule is:

\[
\text{needed exact cap}
=
\text{response threshold}
+
\text{maximum legal future downward reach}.
\]

## 6. Stochastic ecological portability

`stochastic_ecological_portability.py` gives exact capped Markov portability under non-negative increment kernels that factor through the cap. Positive depletion can restore full exact abundance distinguishability.

`continuous_time_depletion_reach.py`, `per_capita_mortality_reach.py`, and `finite_horizon_stochastic_saturation.py` separate exact non-portability from capacity-independent finite-horizon approximate macros.

## 7. Hidden cross-guild coupling

`cross_guild_stochastic_coupling.py` shows that hidden saturated abundance remains relevant only through the downstream kernel it induces. The saturated-tail hazard diameter `delta` is zero exactly when the capped two-guild macro is exact; otherwise the sharp one-step minimax common-macro TV error is `delta/2`.

## 8. Spatial reachability

`spatial_dispersal_reachability.py` treats spread on a fixed directed graph. Unlimited exact response equivalence is target distance plus one unreachable class. With at most `H` future spreads,

\[
|P_H|=\min(D,H)+2.
\]

Thus a fixed future horizon gives a graph-size-independent exact macro even when raw occupancy state space grows exponentially.

## 9. Endogenous-accessibility feedback package

The feedback program now has four exact deterministic layers.

### 9.1 Addressable feedback rank — PR #204

`feedback_gate_rank.py` constructs `r` hidden interaction modes that are invisible to current output, current graph, facilitator count, target count, and static gate distance. Each mode is exposed only through

\[
\operatorname{addr}(i)
\;\mathsf{spread}\;
\mathsf{turnover}\;
\mathsf{spread}.
\]

Hence

\[
\boxed{K_{\rm feedback}=r.}
\]

Removing either the mode→turnover effect or the facilitator→future-accessibility effect collapses the burden to zero bits. The exact memory comes from the complete ecological feedback cycle.

### 9.2 Fixed copy-anonymous interaction types — PR #205

`feedback_type_portability.py` proves that one physical interaction type has a canonical exact five-state quotient independent of replication count `n`, although its reachable microstate count is `2^(n+2)-2`.

For fixed `q` types and arbitrary replication vector,

\[
\boxed{|Q|=5^q}
\]

with one shared transition table across changing physical domains.

### 9.3 Evolving context-dependent types — PR #207

`evolving_feedback_master_types.py` lets hidden mode `m` have a different response type

\[
\tau_c(m)
\]

in each ecological context `c`.

The stable object is the **master feedback signature**

\[
\boxed{
\tau^*(m)=(\tau_c(m))_{c\in C}.
}
\]

Under the declared contextual-feedback contract,

\[
(c,q,[m]_*)
\]

is an exact dynamic interface. Duplicating hidden micro-mode identities inside one master signature changes fiber size but not the macro law.

The rotating family shows why instantaneous type count is insufficient:

\[
|T_c|=2\quad\forall c,
\qquad
R_*=2^r,
\qquad
K_{\rm initial}=r.
\]

All `r` bits first become simultaneously recoverable at horizon

\[
\boxed{4r-1.}
\]

### 9.4 Future-context causal forgetting — PR #208

`future_feedback_causal_forgetting.py` handles the case where context evolution is autonomous:

\[
c'=D(c,a).
\]

At current context `c`, retain only interaction distinctions in contexts still reachable from `c`:

\[
\boxed{
\tau_c^+(m)
=
(\tau_d(m))_{d\in\operatorname{Reach}^+(c)}.
}
\]

Then

\[
(c,q,\tau_c^+(m))
\]

is exact, and future feedback rank cannot increase along a legal context edge.

An irreversible `r`-bit context chain has canonical ready-slice memory

\[
\boxed{r,r-1,\ldots,1,0}
\]

bits. Once context `c` becomes permanently unreachable, bit `b_c` has no future causal path to turnover/accessibility/response and can be forgotten exactly.

### 9.5 Feedback principle after the four theorems

Within these deterministic classes, the controlling object is

\[
\boxed{
\text{future-response-distinct interaction signatures still causally reachable}
}
\]

rather than raw network size, raw hidden-mode count, physical copy count, or instantaneous interaction-type count.

## 10. Remaining feedback boundary

The next genuinely harder class is where context reachability itself depends on ecological macrostate or hidden mode. Then the autonomous-context premise of PR #208 fails: feedback changes not only transition rows **within** a context but also which future contexts exist.

A future theorem must therefore derive a finite state-dependent future-context closure or a matching obstruction. Merely applying the generic all-word quotient, ordinary lumpability, or static reachability is not enough.

## 11. Mechanism-to-data bridge

`docs/mechanism_to_data_bridge_2026-08-14.md` remains the application-control layer. A feedback application needs longitudinal/experimental information resolving a cycle of

\[
\text{interaction/state}
\to
\text{turnover/persistence}
\to
\text{accessibility/movement}
\to
\text{later response}.
\]

Static occurrence/suitability data alone do not identify this mechanism.

## 12. Historical and manuscript gates

Issue #122/#185 remains the H1–H4 historical compiler gate controlling first-paper realization wording. Primary construction pages are required.

The hypothesis-recovery source snapshot remains pinned separately. Later theorem progress updates current status but does not rewrite that source pin.

Feedback modules remain outside the first-paper proof dependency graph unless explicitly promoted later.

## 13. Workflow discipline

Analytic proof and finite replay remain separate. A green workflow cannot rescue an over-broad theorem statement. New work must state semantic domain, legal grammar, exact/approximate contract, and explicit non-claims.

## Navigation

- `fixed_regular_extremal_theorem_2026-08-13.md`
- `grammar_interface_reuse_2026-08-13.md`
- `terminal_grammar_portability_2026-08-13.md`
- `retention_boundary_time_tradeoff_2026-08-14.md`
- `ecological_saturation_blanket_2026-08-14.md`
- `stochastic_ecological_portability_2026-08-14.md`
- `cross_guild_stochastic_coupling_2026-08-14.md`
- `spatial_dispersal_reachability_2026-08-14.md`
- `feedback_gate_rank_theorem_2026-08-14.md`
- `feedback_type_portability_2026-08-14.md`
- `evolving_feedback_master_types_2026-08-14.md`
- `future_feedback_causal_forgetting_2026-08-14.md`
- `mechanism_to_data_bridge_2026-08-14.md`
- `hypothesis_recovery_canonical_index_2026-08-14.md`
- `research_priorities.md`
