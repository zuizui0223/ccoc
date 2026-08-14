# Research priorities — 2026-08-14 post-feedback-forgetting decision

> **Status:** canonical agenda after hypothesis recovery was pinned and the feedback program advanced through scalable rank, bounded-type portability, evolving master types, and exact future-context forgetting.

## Ordering rules

The repository-bounded hypothesis recovery remains pinned by
`docs/hypothesis_recovery_pin_2026-08-14.md`. Later theorem progress does not rewrite that historical recovery source SHA.

Novelty may be adjudicated row by row, but no global novelty slogan is admissible before publication-relevant rows and the H1–H4 historical compiler gate are reconciled.

The first-paper theorem spine remains unchanged:

\[
\text{exact response interface}
+
\text{cross-grammar obstruction}
+
\text{one-action extremal witness}
+
\text{bounded-local realization}
+
\text{positive/reuse boundary}.
\]

Feedback mathematics remains follow-up material unless an explicit editorial decision changes the paper dependency graph.

## Established mathematical packages

### 1. Exact converse and reuse

- `action_grammar_closure.py`: exact one-state action-language expansion converse.
- `grammar_expansion_closure.py`: corrected globally-new-symbol multi-state expansion theorem.
- `grammar_interface_reuse.py`: arbitrary same-domain grammar change; reuse iff open rows descend on closed fibers.
- `terminal_grammar_portability.py`: terminal quotient is the minimum one-labeling exact across a valid expansion chain.

The #163 coarsening counterexample permanently blocks unconditional quotient-monotonicity claims for arbitrary grammar completion.

### 2. Fixed-regular extremal open composition

For every `m>=1`, one fixed four-symbol grammar family has

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

with one newly legal primitive action, degree at most three, radius-one bounded-local dynamics, focal/exterior cut one, and selected-coordinate access

\[
2\lceil\log_2m\rceil+2.
\]

### 3. Portability resource theorems

The retention/update, finite-boundary time, and staged-prefix results separate retained information, post-opening update information, full-interface materialization time, selected-query latency, and exposure deadlines.

### 4. Deterministic ecological structure

`ecological_saturation_blanket.py`, `ecological_capacity_portability.py`, and `budgeted_depletion_blanket.py` establish exact compression from forward-invariant saturation fibers and bounded future downward reach.

### 5. Stochastic ecological portability

`stochastic_ecological_portability.py`, `continuous_time_depletion_reach.py`, `per_capita_mortality_reach.py`, and `finite_horizon_stochastic_saturation.py` separate exact stochastic non-portability from capacity-independent finite-horizon approximate portability.

### 6. Hidden cross-guild coupling

`cross_guild_stochastic_coupling.py` shows that hidden saturated abundance remains relevant only through the downstream kernel it induces. The saturated-tail hazard diameter gives the sharp one-step minimax common-macro TV error `delta/2`.

### 7. Spatial reachability

`spatial_dispersal_reachability.py` reduces arbitrary occupied-patch subsets to directed target distance. With at most `H` future spread actions, the initial exact quotient has `min(D,H)+2` states; unlimited futures restore dependence on full reachability depth.

## Feedback-network program — now four established layers

### 8. Addressable endogenous feedback rank — PR #204

`feedback_gate_rank.py` proves that an explicit feedback cycle

\[
\text{mode}
\to
\text{turnover-induced facilitator loss}
\to
\text{future spread accessibility}
\]

can make `r` latent modes require exactly `r` bits even when all profiles share the same current graph, output, facilitator count, and target count.

The fixed-alphabet query for one mode is

\[
\operatorname{addr}(i)
\;\mathsf{spread}\;
\mathsf{turnover}\;
\mathsf{spread}.
\]

Deleting either causal arrow collapses the hidden-mode burden from `r` bits to zero.

### 9. Bounded copy-anonymous type portability — PR #205

`feedback_type_portability.py` proves that one interaction type has a canonical exact five-state quotient independent of physical replication `n`, despite reachable microstate count `2^(n+2)-2`.

For fixed `q` types and arbitrary replication vector,

\[
\boxed{|Q_{\rm macro}|=5^q}
\]

with one replication-independent transition table.

### 10. Evolving master feedback types — PR #207

`evolving_feedback_master_types.py` handles context-dependent response types

\[
\tau_c(m).
\]

The exact stable object is the master signature

\[
\boxed{\tau^*(m)=(\tau_c(m))_{c\in C}.}
\]

Under the declared contextual-feedback contract,

\[
(c,q,[m]_*)
\]

is an exact dynamic interface. Duplicating micro-mode identities within one master signature across changing semantic domains does not change the macro law.

The rotating family proves that bounded instantaneous type count is insufficient:

\[
|T_c|=2\quad\forall c,
\qquad
R_*=2^r,
\qquad
K_{\rm initial}=r.
\]

The sharp full-profile exposure horizon is

\[
4r-1.
\]

### 11. Exact future-context forgetting — PR #208

`future_feedback_causal_forgetting.py` sharpens the master signature when ecological context evolution is autonomous:

\[
c'=D(c,a).
\]

At current context `c`, retain only type distinctions in contexts still reachable from `c`:

\[
\boxed{
\tau_c^+(m)=
(\tau_d(m))_{d\in\operatorname{Reach}^+(c)}.
}
\]

Then

\[
(c,q,\tau_c^+(m))
\]

is an exact dynamic interface and future feedback rank is monotone non-increasing along every context edge.

An irreversible `r`-bit chain attains the sharp sequence

\[
\boxed{r,r-1,\ldots,1,0}
\]

of canonical ready-slice feedback-memory bits. Leaving context `c` makes bit `b_c` exactly forgettable because no legal future can return to a context where it affects turnover or accessibility.

### Feedback principle now established

Within the proved deterministic classes, exact feedback memory is controlled by

\[
\boxed{
\text{future-response-distinct interaction signatures that remain causally reachable}
}
\]

rather than raw network size, raw hidden-mode count, or instantaneous type count.

## Priority 1 — only the remaining genuinely harder feedback boundary

Do not add another fixed-type, rotating-bit, or irreversible-chain witness.

The remaining serious feedback case is where **context reachability itself depends on ecological macrostate and/or hidden interaction mode**. In that class the autonomous-context premise of PR #208 fails: two states with the same present context can have different future context cones because feedback changes which contexts become reachable.

A worthwhile next theorem would need one of:

- an exact state-dependent future-context closure operator with a finite fixed point;
- a structural sufficient condition under which mode-dependent context reachability can still be summarized by a bounded interface;
- or a lower-bound family showing that a small present context/type description generates unboundedly many future context cones.

Do not merely restate generic partition refinement, ordinary lumpability, or the canonical all-word quotient.

## Priority 2 — real application / falsification

Issue #199 remains the live empirical-identification problem. A useful feedback application must observe a causal cycle of the form

\[
\text{interaction/state}
\to
\text{turnover/persistence change}
\to
\text{accessibility/movement change}
\to
\text{later response}.
\]

Static occurrence/suitability data alone remain `UNIDENTIFIED` for this mechanism.

## Priority 3 — H1–H4 historical compiler gate

Issue #122/#185 remains the first-paper historical-realization gate. H1–H4 must be decided from primary construction pages, not abstracts, metadata, or failed retrieval.

## Priority 4 — manuscript transfer

Use `docs/manuscript_transfer_manifest_2026-08-14.md` and issue #192. Feedback theorems remain outside the first-paper dependency graph unless deliberately promoted later.

## Priority 5 — cleanup only when it removes real maintenance debt

Keep `tests.yml` as the generic non-legacy full-suite matrix. Specialized replay workflows may remain when they generate theorem-specific artifacts. Compatibility facades stay until in-repository consumers are migrated and the manuscript source pin is immutable.

## Explicit non-priorities

No new codebook families, panel/reset variants, capped-count special cases, one-guild mortality variants, elementary Bernoulli coupling variants, elementary shortest-path variants, generic Fano/channel lemmas, generic contraction/small-gain theorems, generic symmetry/lumpability reformulations, additional fixed-feedback witnesses, empirical fitting inside the theorem registry, or bulk deletion of historical replay workflows.
