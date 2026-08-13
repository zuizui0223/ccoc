# Research priorities — 2026-08-14 consolidated decision

> **Status:** canonical agenda after the fixed-regular extremal theorem, exact converse/reuse pass, terminal-chain portability theorem, and retention/update/boundary-time resource results.

## 1. Governing decision

CCOC/RACH now has a mature exact finite core. Another nearby partition-refinement theorem is not the main bottleneck.

The first-paper spine is

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

The remaining first-paper uncertainty is historical: whether classical uniform sequential-machine compilation already supplies the complete bounded-local realization package. Theorem validity and historical novelty remain separate.

## 2. Established mathematics

### 2.1 Exact interface and converse hierarchy

For one finite controlled system and one finite prefix grammar, the exact response interface is the coarsest labeling preserving current output, enabled-action rows, and enabled successors.

Three cross-grammar levels are separated.

1. **One-state action-language expansion** — `action_grammar_closure.py`: stable open-action refinement of the canonical closed quotient equals the canonical open quotient; zero inflation is iff newly legal actions descend on the closed quotient.
2. **Finite grammar-state, globally-new-symbol expansion** — `grammar_expansion_closure.py`: old action columns are frozen and only globally absent symbols may be introduced. Closed distinctions persist, stable open-row closure computes the canonical open quotient, and zero inflation is iff open rows descend.
3. **Arbitrary same-domain grammar change** — `grammar_interface_reuse.py`: canonical closed/open quotients may be equal, finer, coarser, or incomparable. The exact general question is reuse: the canonical closed labeling remains an exact open interface iff open enabled rows and successors descend on each closed fiber.

The explicit coarsening counterexample remains a regression guard. Do not restore an unconditional claim that changing the grammar automaton must refine the canonical product-state quotient.

### 2.2 Fixed-regular extremal theorem

For every integer `m>=1`, the same family has

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

under one fixed four-symbol primitive alphabet and one-state closed/open grammar schemas. Opening adds only `fire`. The same family simultaneously has bounded local state/message alphabets, radius-one dynamics, maximum degree three, tree topology, focal/exterior cut one, and exact worst selected-coordinate access

\[
2\lceil\log_2m\rceil+2.
\]

The interface innovation saturates the finite-domain maximum. Constant cut width, degree, local alphabets, and grammar-edit count therefore do not give a system-size-independent exact-memory bound.

### 2.3 Terminal-stage exact portability for grammar chains

`terminal_grammar_portability.py` closes the uniform exact-memory question for chains of valid globally-new-symbol expansions. The terminal canonical quotient is an exact interface at every earlier stage and is the smallest single labeling that works for the whole chain:

\[
\boxed{K_{\rm uniform}=\log_2|P_{\rm terminal}|.}
\]

The same terminal labels construct one existing `ConservativeMacroSchema` across the chain. If two valid chains reach the same terminal grammar, their minimal uniform exact-memory budget is the same even if intermediate quotients differ.

### 2.4 Retention–update adaptation tradeoff

`portability_adaptation_tradeoff.py` separates information retained before opening from information supplied after opening. For `m` independent binary exterior coordinates,

\[
\boxed{
I(E;C)+H(U\mid C)
\ge
m-\sum_j h_2(\varepsilon_j).
}
\]

At zero error the bound is sharp for every split: retaining `k` exterior bits and supplying the remaining `m-k` bits attains equality. In the fixed-regular relay the canonical closed interface retains no exterior information, so exact full adaptation carries an `m`-bit information debt.

### 2.5 Boundary-time materialization tradeoff

`docs/retention_boundary_time_tradeoff_2026-08-14.md` converts the adaptation debt into a time/resource bound. If the inward boundary has width `c`, alphabet size `s`, and `T` synchronous update rounds,

\[
\boxed{
I(E;C)+cT\log_2s
\ge
m-\sum_j h_2(\varepsilon_j).
}
\]

For a closed representation with at most `2^k` states and common error `eps`,

\[
\boxed{k+cT\log_2s\ge m(1-h_2(\varepsilon)).}
\]

The exact integer round bound is sharp for power-of-two boundary alphabets.

For the fixed-regular relay, full exact installation across the cut-one three-symbol focal boundary needs

\[
T_{\rm full}=\Omega(m),
\]

while one selected coordinate has

\[
T_{\rm query}=\Theta(\log m).
\]

More precisely,

\[
\frac{T_{\rm full}}{T_{\rm query}}
=\Omega\!\left(\frac{m}{\log m}\right).
\]

Thus random-access latency and full-interface installation latency are different resources.

## 3. Novelty boundary

Do not spend novelty budget on fixed-grammar minimization, Myhill–Nerode/right-congruence machinery, common refinement/natural-join bookkeeping, elementary centralized unlocks, generic partition refinement, regular-language restriction, generic causal-cone counting, Fano, finite-alphabet channel entropy, or deadline scheduling by themselves.

The live first-paper candidate remains the **simultaneous constrained extremal realization**: maximal same-plant cross-grammar separation together with fixed grammar, one newly legal primitive action, bounded local resources, degree three, and logarithmic selected-query access. Historical firstness remains conditional on the compiler audit.

The newer retention/update and boundary-time results are useful coupled-resource consequences. Their information-theoretic ingredients are classical; do not present them as independent historical firstness claims without a separate prior-art gate.

## 4. Priority 1 — finish the H1–H4 primary compiler gate

Issue #122 remains the main historical gate. A classical full-language compiler is decisive only if it jointly supplies:

- **H1:** bounded local state/connectivity independent of source state count;
- **H2:** fixed context-independent source controls/input distribution;
- **H3:** two-way response-trace faithfulness without spurious closed distinctions;
- **H4:** bounded source-step/network/output latency.

If all four hold with comparable overhead, bounded-local realization **existence** is demoted as a novelty claim. The explicit CCOC relay remains a transparent extremal equality witness.

Primary acquisition routes are already fixed. Do not restart generic source searching or infer H1–H4 from titles, abstracts, or holding metadata.

## 5. Priority 2 — manuscript transfer

The manuscript must distinguish formalism, exact theorem statements, classical ancestry, the conditional simultaneous-realization novelty candidate, and the fallback interpretation if the H1–H4 gate subsumes realization existence. Record exact CCOC SHAs and replay provenance rather than citing “latest.”

## 6. Priority 3 — genuinely new mathematics beyond the completed exact core

### 6.1 Staged installation deadlines — active next target

Extend terminal-memory path independence with online resource deadlines. For nested stage requirements `S_t`, derive prefix bounds of the form

\[
k+\sum_{q\le t} c_qT_q\log_2s_q
\ge
|S_t|-\text{error penalty}.
\]

The exact binary/power-of-two subclass is promising because the prefix inequalities appear to be both necessary and sufficient. The scientific point is the contrast: terminal shared-memory capacity can depend only on the final grammar, while online installation feasibility depends on **when** distinctions become required.

### 6.2 Approximate/stochastic portability

Go beyond approximate addressability. Replace deterministic finite boundary-symbol capacity by a genuine noisy/stochastic information-flow contract, or characterize when one approximate/stochastic macro schema remains portable under grammar expansion. Generic contraction or small-gain abstraction alone is not a CCOC target.

### 6.3 Ecological structural theorem

Start from an explicit ecological composition class—colonization, dispersal, interaction-network, or boundary-coupling restrictions—and derive addressability lower bounds or finite-blanket upper bounds. Small cut width, low degree, acyclicity, and low treewidth alone are already insufficient by the relay.

## 7. Explicit non-priorities

Do not prioritize another codebook family, another partition defect/accounting identity, more panel/reset variants, another toy adaptive no-go, another same-domain quotient reformulation, generic contraction/small-gain abstraction, generic source searching, replacement/rewiring transport inside CCOC, or empirical ecological inference in this theorem repository.

## 8. Promotion rule

New active theorem work must materially change the model class or coupled resource statement: a strict assumption weakening, stronger conclusion, sharp staged-resource result, substantive approximate/stochastic theorem, or derived ecological theorem. A nearby special case is not enough.
