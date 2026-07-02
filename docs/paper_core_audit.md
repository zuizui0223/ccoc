# Paper-core mathematical robustness audit

## Audit question

This audit asks two separate questions.

1. Is the mathematical statement used by the open-composition manuscript valid
   under its written assumptions?
2. Does the repository replay the finite witnesses and boundary cases without
   silently turning those replays into a proof about arbitrary systems?

The answer is **yes for the conditional theorem package**, with the scope
corrections recorded below. The proof burden and replay burden are intentionally
distinct.

## Verdict by theorem asset

| Asset | Mathematical status | Executable evidence | Audit verdict |
|---|---|---|---|
| `CORE-1` exact grammar-aware interface | Exact finite theorem. Equal macro labels preserve output, legal-action rows, and enabled-action successors on system state × grammar state. | Canonical quotient, refinement, and counterexample regressions. | Robust for declared finite deterministic systems and grammars. |
| `CORE-2` addressability lower bound | Conditional injection theorem. Uniform coordinate decoders distinguish every pair in a declared product-indexed state subset. | Arithmetic replay plus a literal controlled readout witness with concrete trace decoders. | Robust once the decoder-word and product-subset assumptions are stated explicitly. |
| closed/open gap | Corollary from the open injection lower bound and a supplied closed exact factorization. | Finite declared closed word families are replayed for the literal readout witness. | Robust as an **upper-bound** comparison; closed equality needs extra decoder conditions and is not inferred from factorization alone. |
| `CORE-3` relay sharpness | Explicit binary equality family. | Exhaustive finite protocol and macro-time conjugacy checks for growing finite instances. | Robust as a sharpness construction, not as a theorem about all bounded-degree networks. |
| `CORE-4` conservative schema | Sufficient finite-chain criterion. | Positive legal-action expansion witness and exact stage-interface checks. | Robust as sufficient, not necessary; do not extend its conclusion to arbitrary infinite chains. |
| `CORE-5` fiber split | Local refutation of a proposed merge. | Future-word and newly legal action counterexamples. | Robust locally; it does not establish a global lower bound or rule out every alternative macro-law. |

## Formal proof versus finite replay

### What is proved symbolically

The addressability lower bound is an injection argument. Let

\[
Z^*\cong I\times E_1\times\cdots\times E_q
\]

be a declared product-indexed subset of states. If a legal word \(r_0\) decodes
\(I\), and each legal word \(r_j\) decodes \(E_j\) uniformly over all values of
the other coordinates, then any two distinct states in \(Z^*\) differ in a
coordinate exposed by one of these words. They cannot occupy the same exact
open-interface block. Hence

\[
K_{\mathrm{open}}
\ge
\log_2|I|+\sum_{j=1}^{q}\log_2|E_j|.
\]

The noncommutation inequality then combines this open lower bound with closed
**upper bounds** supplied by exact factorization through \((I,E_j)\).

### What the repository replays

The executable witnesses verify finite instances of the assumptions and
conclusions:

- a finite controlled system whose literal read words recover each coordinate;
- a finite closed grammar family whose complete declared words factor through
  \((I,E_j)\);
- binary relay trees with pairwise pulse propagation, degree at most three, and
  macro-time agreement with the coordinate witness; and
- finite conservative schema and fiber-split examples.

Passing these replays does not prove the general injection theorem, infer a
boundary grammar from data, prove reachability from an initial condition, or
validate a real ecosystem.

## Scope corrections fixed by this audit

### 1. Product subset, not transition-closed subsystem

The lower bound needs a declared product-indexed set of states on which decoder
words are defined. It does **not** require that set to be closed under the
controlled transition map. Indeed, the literal readout witness leaves the idle
product set after a read action. The active documentation therefore uses
“product subset” rather than “reachable product subsystem.”

If a later application needs reachability from a specified initial state, it must
supply an additional initial-state and reachability contract. The current theorem
neither assumes nor certifies it.

### 2. Closed equality needs more than factorization

If all closed responses factor through \((I,E_j)\), then

\[
K_{\mathrm{closed},j}
\le
\log_2|I|+\log_2|E_j|.
\]

Equality additionally requires that the closed grammar retain words that decode
both \(I\) and \(E_j\). The binary coordinate/relay witness has this property.
The general noncommutation corollary needs only the upper bound.

### 3. Local grammar is not a fixed global port alphabet

The relay family keeps its node state alphabet, message alphabet, pairwise update
rule, and degree bound fixed. The number of selectable ports grows with the
family. The paper must retain this distinction.

### 4. Positive portability is finite and sufficient

The conservative-schema certificate is an exact statement for a declared finite
chain with one fixed finite action alphabet. It does not characterize all
portable laws, stochastic systems, continuous systems, simultaneous-action
systems, or arbitrary infinite composition processes.

## GitHub Actions reproducibility contract

The `Paper-core reproducibility` workflow runs:

1. theorem-registry provenance validation;
2. an explicit allowlisted test suite for `CORE-1`--`CORE-5`; and
3. `scripts/verify_paper_core.py`, which writes a machine-readable finite replay
   report with the source commit SHA.

The workflow artifact records the exact finite claims that were replayed. It is a
reproducibility artifact, not an automated proof checker for the manuscript.

## Submission decision

The paper-core mathematics is ready to support a theorem-first submission once
its LaTeX manuscript repeats the definitions and proofs independently, preserves
the four scope corrections above, and pins a permanent RACH release commit.
