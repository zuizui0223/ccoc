# Research priorities — 2026-08-13 consolidated decision

> **Status:** canonical active agenda after the fixed-regular extremal theorem, the exact converse pass, and the correction of the multi-state grammar-expansion scope.

## 1. Governing decision

CCOC/RACH remains active, but the exact finite same-domain theory is now sufficiently closed that another nearby quotient theorem is not the main bottleneck.

The paper spine is

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

The remaining first-paper uncertainty is historical: whether classical uniform sequential-machine compilation already supplies the complete bounded-local realization package. Theorem validity and historical novelty remain separate questions.

## 2. Established mathematics

### 2.1 Exact grammar-aware interface

For one declared finite controlled system and one declared finite prefix grammar, the exact response interface is the coarsest labeling preserving current output, enabled-action rows, and enabled successors. Equivalently, fixed-contract response equivalence is the intersection of the kernels of all legal response maps.

This is formal substrate, not a firstness claim.

**Important scope correction:** changing the grammar automaton is not automatically monotone on the canonical product-state quotient. If an old partially available action is completed at additional grammar states, an earlier enabled-row distinction can disappear and the open canonical quotient can become coarser. Therefore the repository no longer uses an unconditional slogan that “grammar enlargement refines the quotient.”

### 2.2 Exact converse hierarchy

Three increasingly broad results are now separated.

1. **One-state action-language expansion** — `action_grammar_closure.py`.
   For `A_C* subseteq A_O*` on one fixed plant, stable open-action refinement of the canonical closed quotient equals the canonical open quotient. Zero inflation holds iff every newly legal action descends to the closed quotient.

2. **Finite grammar-state, globally-new-symbol expansion** — `grammar_expansion_closure.py`.
   Every old action symbol keeps its complete grammar transition column. Only a symbol illegal at every closed grammar state may be enabled after opening, possibly state-dependently. In this class every closed distinction persists, the open quotient refines the closed quotient, stable open-row closure equals the canonical open quotient, and zero inflation is iff open legality/successor rows descend on the closed quotient.

3. **Arbitrary same-domain grammar change** — `grammar_interface_reuse.py`.
   Canonical closed/open quotients may be equal, open-finer, open-coarser, or incomparable. The correct general question is interface reuse: the canonical closed labeling remains an exact open interface iff open enabled rows and successors descend on every closed fiber. Reuse and minimal-quotient monotonicity are distinct.

The explicit coarsening counterexample and exhaustive small-grammar regressions are retained to prevent the broader false monotonicity claim from returning.

### 2.3 Fixed-regular extremal theorem

For every integer `m>=1`, the same finite construction has

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

under the fixed primitive alphabet

\[
\{0,1,\mathsf{fire},\mathsf{tick}\}.
\]

Closed and open grammars are one-state and independent of `m`; opening adds only `fire`. The same family simultaneously has bounded local state/message alphabets, pairwise radius-one dynamics, maximum degree three, tree topology, focal/exterior cut one, and exact worst canonical access

\[
2\lceil\log_2m\rceil+2.
\]

The innovation saturates the finite-domain maximum. Fixed static/local resource constants therefore do not give a system-size-independent upper bound on exact interface inflation. General bounded-local causal-cone reasoning gives `Omega(log m)` access, so the explicit relay is order-optimal in scale.

### 2.4 Positive and companion results

- conservative finite macro-schema portability remains a constructive sufficient boundary;
- the exact reuse/converse results above explain when the canonical closed interface survives and when refinement is forced;
- adaptive finite-evidence closure no-go remains an identifiability companion;
- the Fano approximate-addressability result shows the obstruction is not purely a zero-error artifact.

## 3. Novelty boundary

Do not spend novelty budget on fixed-grammar minimization, Myhill--Nerode/right-congruence machinery, incomplete-machine reduction, promise-domain descriptional advantage, common refinement/natural-join accounting, elementary centralized one-action blow-up, generic partition-refinement algorithms, regular-language restriction, or generic causal-cone/locality lemmas.

The only live first-paper candidate remains the **simultaneous constrained extremal realization**: maximal same-plant cross-grammar response-interface separation together with fixed grammar, one newly legal primitive action, bounded local resources, degree three, and logarithmic causal access. Historical firstness remains conditional on the compiler audit.

## 4. Priority 1 — finish the H1–H4 primary compiler gate

Issue #122 remains the main historical gate. A classical full-language compiler is decisive only if it jointly supplies:

- **H1:** bounded local state/connectivity independent of source state count;
- **H2:** fixed context-independent source controls/input distribution;
- **H3:** two-way response-trace faithfulness without spurious closed distinctions;
- **H4:** bounded source-step/network/output latency.

If all four hold with comparable overhead, bounded-local realization **existence** is demoted as a novelty claim. The explicit CCOC relay remains a transparent extremal equality witness.

Primary acquisition routes are already fixed in the dedicated source-handoff documents. Do not restart generic web searching or infer H1–H4 from abstracts, titles, or holdings metadata.

## 5. Priority 2 — manuscript transfer

The manuscript must distinguish:

- formalism used;
- exact theorem statements;
- classical ancestry;
- the conditional simultaneous-realization novelty candidate;
- the fallback interpretation if the H1–H4 gate subsumes realization existence.

At transfer time record exact CCOC SHAs and replay provenance rather than citing “latest.”

## 6. Priority 3 — genuinely new mathematics beyond the closed exact same-domain boundary

### 6.1 Coupled resource tradeoff

Seek a sharp lower bound coupling response memory to control complexity, communication/local state, or latency that is not inherited from generic coding or causal-cone counting alone.

### 6.2 Approximate/stochastic portability

Move from approximate addressability to portability: characterize when one finite approximate/stochastic macro schema survives grammar/composition expansion, or derive a nontrivial memory/error/grammar tradeoff. Generic contraction or small-gain abstraction by itself is not a CCOC target.

### 6.3 Ecological structural theorem

Start from an explicit ecological composition class—colonization, dispersal, interaction-network, or boundary-coupling restrictions—and derive addressability lower bounds or finite-blanket upper bounds. Small cut width, low degree, acyclicity, and low treewidth alone are already ruled out as closure certificates by the relay.

### 6.4 Beyond same-domain exact converse

Further converse work is justified only if it changes the model class materially: changing semantic domains, embeddings between stages, resource-bounded portability across a chain, or approximate/stochastic contracts. Another fixed finite partition-refinement reformulation is not enough.

## 7. Explicit non-priorities

Do not prioritize another codebook family, another defect/accounting identity, more panel/reset variants, another toy adaptive no-go, generic contraction/small-gain abstraction, generic source searching, replacement/rewiring transport inside CCOC, or empirical ecological inference in this theorem repository.

## 8. Promotion rule

New active theorem work must be a strict assumption weakening, stronger conclusion, genuine new model class, sharp coupled-resource result, or substantive approximate/stochastic/ecological theorem. A nearby special case is not sufficient reason to enlarge the theorem registry.