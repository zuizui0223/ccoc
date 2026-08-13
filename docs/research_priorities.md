# Research priorities: final 2026-08-13 decision

> **Status date:** 2026-08-13. This is the canonical active agenda after the
> post-reopening theorem strengthening, historical novelty audit, and primary-source
> acquisition pass.

## 1. Governing research decision

CCOC/RACH remains an active theorem repository, but the current bottleneck is **not
another local theorem**. The finite deterministic theorem package is mature enough
for a paper. The remaining scientific uncertainty is whether the explicit
bounded-local extremal realization is historically distinctive once classical
uniform sequential-machine compilation is read at the construction level.

The mathematical paper spine remains:

\[
\text{response-interface formalism}
+
\text{cross-grammar lower bound}
+
\text{extremal one-action family}
+
\text{bounded-local realization}
+
\text{positive portability criterion}.
\]

But **theorem role and novelty role are separate**.

## 2. What is established

### 2.1 Formal interface machinery

For a supplied finite deterministic controlled system and declared legal future
grammar, the exact interface is the coarsest response quotient preserving current
output, legal-action rows, and successors.

For response maps `R_w`,

\[
\sim_L=\bigcap_{w\in L}\ker R_w.
\]

Thus grammar enlargement refines the response quotient, and a pair-separating
future family makes a finite codebook discrete. The arbitrary addressable-codebook
strengthening, constrained codebooks, and closed-factorization comparison bounds
are implemented and tested.

**Status:** useful formalism/substrate, not a firstness claim.

### 2.2 Static/dynamic inflation accounting

For the closed-union grammar, common refinement and join-realizability accounting
separate static closed-view capacity from genuinely open-only future innovation.
For the full open grammar,

\[
\iota_{\rm new}=\log_2|P_O|-\log_2|P_U|.
\]

Common refinement, product capacity, natural-join ancestry, and the generic fact
that extra future tests split a quotient are not novelty claims.

### 2.3 Extremal one-action family

The strengthened family has

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
\iota_{\rm new}=m,
\]

and `iota_new=m` saturates the finite-domain upper bound.

The strongest construction now uses the **same one-state finite prefix grammar for
every system size**:

\[
L_C=\{0,1,\mathsf{tick}\}^{*},
\qquad
L_O=\{0,1,\mathsf{fire},\mathsf{tick}\}^{*}.
\]

Both grammars use the common four-symbol action alphabet and one grammar state;
opening adds exactly the `fire` transition. The construction works for every
integer `m>=1`, not only powers of two. The closed result is proved for the entire
infinite regular language by a pulse-free invariant rather than finite word-list
enumeration.

A centralized unlock construction with this qualitative effect remains elementary
and is **not** firstness-bearing by itself.

### 2.4 Bounded-local relay

The explicit relay simultaneously has:

- primitive alphabet `{0,1,fire,tick}`;
- one-state closed and open grammar schemas independent of `m`;
- no `m`-dependent legal future-word list in the theorem statement;
- arbitrary positive `m`;
- bounded local state/message alphabets;
- pairwise radius-one dynamics;
- maximum degree three;
- tree interaction topology;
- exact worst canonical query length
  `2 ceil(log2(m)) + 2` in the balanced arbitrary-size selector-plus-return
  construction;
- order-optimal logarithmic access in the broader bounded-local causal-cone class.

For old power-of-two canonical probes, the fixed-grammar totalization is checked
against the historical addressed relay and preserves its trace/final
microconfiguration. Historical CORE replay semantics are unchanged.

**Status:** the only remaining conditional firstness candidate is this simultaneous
extremal/local resource package. The fixed-grammar strengthening removes hidden
construction caveats; it does not create a new automata-theory novelty claim.

### 2.5 Positive and companion results

- conservative finite macro-schema portability is a sufficient constructive
  boundary;
- adaptive finite-evidence closure no-go is already complete as an identifiability
  companion;
- the Fano approximate-addressability theorem shows the exact gap is not purely a
  zero-error artifact.

These do not need further special-case proliferation for the first paper.

## 3. What is explicitly prior art / substrate

Do not spend novelty budget on:

1. Myhill--Nerode/bisimulation-style fixed-grammar minimization;
2. context/input/environment-dependent sequential-machine reduction;
3. incomplete-machine reduction;
4. promise/restricted-domain descriptional advantage or exponential gap by itself;
5. broad state-reduction/realization noncommutation;
6. pair-separating/codebook cardinality lower bounds;
7. common-refinement/product-capacity/natural-join accounting;
8. elementary one-new-action centralized blow-up;
9. repeated fixed modules or uniform modular synthesis;
10. fixed-input synthesis, bounded fanout, or delayed universal modules in
    isolation;
11. regular-language/input restriction or one-state grammar descriptions;
12. generic finite-speed/local causal-cone bounds.

Hartmanis--Stearns is direct ancestry for broad reduction/realization
noncommutation. Kim--Newborn and the interacting-FSM literature establish
contextual minimization. Larrauri--Bloem's tail-minimization “exponential
improvement” is algorithmic/representation improvement, not an exponential
restricted/open minimum-state ratio; their exponential solution-size theorem is
for the distinct tail-synthesis problem.

## 4. Priority 1 — finish the H1–H4 primary compiler gate

Issue #122 remains the main historical research gate.

A classical full-language compiler is decisive only if it jointly supplies:

- **H1:** bounded local state/connectivity independent of source state count;
- **H2:** fixed context-independent source controls/input distribution;
- **H3:** two-way response-trace faithfulness with no spurious closed distinctions;
- **H4:** bounded source-step/network/output latency.

If H1–H4 hold with comparable overhead, a bounded-local implementation of the
centralized CCOC seed can be obtained classically and the relay's **existence**
novelty is demoted. The explicit fixed-grammar arbitrary-size relay remains a
transparent extremal construction.

### Primary acquisition routes are already fixed

The broad web search is finished. The remaining work is reading primary
construction text.

- **Weiner--Hopcroft 1968 report no. 61:** University of Tokyo / Princeton
  physical-copy route.
- **Ullman--Weiner 1969:** primary abstract/introduction already read; issue #137
  tracks construction pages. The article-level 14-page VTDA PDF resolves, but the
  current page-render/download backend still fails on construction-page access.
- **Newborn--Arnold 1972 C-21(1):63--79:** Osaka Prefectural Central Library direct
  copy route; correct DOI `10.1109/T-C.1972.223433`.
- **Drilman--Weiner 1972 C-21(10):1124--1129:** same Osaka holding; key
  fixed-module/nondeterministic-machine intersection.
- **Williams + Le Van--van Houtte 1975 C-24(8):** Tokyo University of Technology
  physical reading/copy route.
- **Sureshchander 1978, Almaini 1978, Chen--Hurst 1982:** same Tokyo holding as
  follow-up/correction/comparison sources.

Do not infer H1–H4 from titles, secondary abstracts, or holding metadata.

## 5. Priority 2 — move to the manuscript workspace

Issue #99 is the manuscript tracker. Issue #141 is the only repository-bootstrap
blocker.

The manuscript repository must be:

`zuizui0223/rach-open-composition-paper`

The current connector exposes no create-repository action and the execution
environment has no `gh` CLI, so repository creation remains one manual action.
Once it exists with `main` and a README, the connector can bootstrap the complete
traceability/LaTeX structure.

The manuscript must distinguish:

- **formalism used:** response quotient, codebook lower bound, closed/open
  comparison;
- **classical ancestry:** contextual minimization, noncommutation, modular
  synthesis;
- **conditional candidate:** simultaneous extremal one-action + fixed-grammar
  bounded-local realization;
- **fallback:** relay as explanatory sharp construction if #122 subsumes its
  existence.

## 6. Priority 3 — genuinely new mathematics only after/beyond the gates

Do not create another defect, score, panel, or codebook special case. New theorem
work is justified only if it materially changes one of the following.

### 6.1 Genuine necessity/converse

Find a delimited cross-grammar class with a nontrivial necessary-and-sufficient
criterion for bounded/open response-interface growth that is not merely common
refinement or fixed-grammar minimization.

### 6.2 Coupled resource tradeoff

Prove a sharp simultaneous lower bound coupling response memory to control
complexity, communication/local state, or causal access in a way not inherited
from generic coding or locality lemmas.

### 6.3 Approximate/stochastic portability

Go beyond approximate addressability. Characterize when one finite
approximate/stochastic macro schema remains portable as the legal composition
grammar expands, or derive a nontrivial memory/error tradeoff for portability.
Generic contraction/small-gain approximate abstraction alone is not a CCOC novelty
target.

### 6.4 Ecological structural theorem

Start from a mathematically specified ecological composition class—colonization,
dispersal, interaction-network, or boundary-coupling constraints—and **derive**
addressability lower bounds or finite-blanket upper bounds. Merely renaming latent
bits as species or colonists is not enough. In particular, small physical cut
width, sparse topology, acyclicity, or low treewidth alone cannot imply a small
exact dynamic blanket: the relay already separates those notions.

## 7. Explicit non-priorities

Until #122/#137 or the manuscript blocker moves, do not prioritize:

- another codebook family;
- another partition defect/accounting identity;
- more reset/panel/robustness variants;
- another toy adaptive no-go;
- generic contraction/small-gain abstraction as a standalone CCOC theorem;
- generic literature/mirror searching for already located primary sources;
- replacement/rewiring transport inside CCOC;
- empirical ecological inference in this theorem repository.

## 8. Promotion rule

Any new active theorem must identify exactly which canonical question it changes:

\[
\text{exact interface},\quad
\text{response-interface obstruction},\quad
\text{portable composition},\quad
\text{resource tradeoff},\quad
\text{or finite-evidence identifiability}.
\]

It must be a strict assumption weakening, stronger conclusion, genuine
converse/necessity result, sharper coupled resource theorem, or new model class.
A nearby special case is not sufficient reason to expand the theorem registry.
