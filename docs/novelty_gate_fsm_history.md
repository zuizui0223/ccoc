# Historical FSM novelty gate for CCOC

> **Status:** manuscript novelty audit after the 2026-08-11 theorem restart.
> This document **supersedes the earlier working assumption that the mere
> closed-to-open compression separation is itself the novelty claim**.  The
> mathematics implemented in CCOC remains valid under its declared contracts;
> this audit concerns priority and positioning, not correctness.

## 1. Revised verdict

The following broad claim is no longer defensible as a novelty statement:

> a finite-state component can admit a smaller exact description under a
> restricted/context-dependent set of inputs, while a richer input or
> interaction environment forces more behavioral distinctions.

That problem has direct sequential-machine and interacting-FSM ancestry going
back at least to Kim & Newborn (1972), and it was developed extensively in the
1990s in work on sequential don't-cares, permissible component behavior, and
minimization of interacting FSM networks.

Likewise, the following are established mathematical/testing substrate rather
than CCOC novelty:

- minimal behavioral quotients for a fixed future/test language;
- state minimization of incompletely specified machines;
- component minimization under context-imposed input restrictions;
- using information from neighboring/interacting components as sequential
  don't-cares;
- sets of test sequences that jointly distinguish states;
- common refinements/intersections of behavioral equivalence relations;
- natural-join/product reconstruction of multiple restricted views;
- the fact that making a new input/test/intervention legal can split previously
  compatible states;
- prefix-code and finite-speed locality lower bounds used in the relay proof.

The **remaining novelty candidate** is much narrower and must still pass a full
priority search:

> an extremal quantitative family in which every one of `m` fixed closed
> compositions has a one-bit exact future-response interface, their entire
> closed-grammar union and static join/refinement capacity are still one bit,
> real routing dynamics are already legal in the closed regimes, and legalizing
> exactly one primitive action makes the open quotient discrete on
> `2^(m+1)` states—thereby attaining the absolute maximum `m` bits of new exact
> causal memory—while simultaneously retaining a four-symbol global action
> alphabet, pairwise local updates, maximum degree three, constant local grammar,
> and zero latency slack under the explicitly declared selector-plus-pulse local
> architecture.

Even this should presently be called a **novelty candidate / sharp construction**,
not a firstness claim.

---

## 2. Kim–Newborn ancestry: restricted inputs and exact minimization

### Primary bibliographic anchor

Joonki Kim and Monroe M. Newborn, **“The Simplification of Sequential Machines
with Input Restrictions,”** *IEEE Transactions on Computers* 21(12),
1440–1443, 1972.

The original full text was not available through the sources used in this audit,
so we do not infer details beyond what later primary work explicitly attributes
to it.  The bibliographic existence and citation details are independently
indexed by DBLP / IEEE metadata.

### What later primary work says Kim–Newborn solved

Larrauri & Bloem (2021), *Minimization and Synthesis of the Tail in Sequential
Compositions of Mealy Machines* (arXiv:2105.10292), gives a particularly direct
modern statement of the lineage:

- optimization of completely and incompletely specified FSMs is classical;
- decomposed systems may admit more optimization when components are considered
  in context;
- two machines can be non-equivalent in isolation yet interchangeable in the
  context of another component;
- the **first exact solution** to their Tail Minimization Problem was given by
  Kim and Newborn;
- the Kim–Newborn method obtains the smallest replacement by minimizing an
  incompletely specified Mealy machine induced by the context;
- for a cascade `T ∘ H`, a candidate replacement `T'` is valid exactly when its
  output agrees with `T` on every sequence in `Out(H)`—i.e. only on the input
  language the head can actually generate.

In Larrauri & Bloem's notation, their Tail Minimization Problem is explicitly:
find a replacement for component `T` with the **minimum number of states** while
preserving the behavior of the composition `T ∘ H`.

### CCOC consequence

This is extremely close to the broad intuition behind closed-context causal
compression.  Therefore CCOC must **not** claim:

- first state compression induced by input restrictions;
- first exact minimal state abstraction valid only inside a context;
- first demonstration that a component can be smaller in context than in
  isolation;
- first treatment of a neighboring component as a grammar/input restriction.

The CCOC distinction, if any, must be quantitative and structural beyond this
classical problem statement.

---

## 3. Interacting FSM networks: context information and sequential don't-cares

### Wang & Brayton (1993)

H.-Y. Wang and Robert K. Brayton, **“Input Don't Care Sequences in FSM
Networks,”** UCB/ERL M93/64, 1993.

The Berkeley report states that it computes input don't-care sequences for a
component in an FSM network with **arbitrary topology**.  It also states that for
a cascade network the Kim–Newborn procedure exactly computes all input don't-care
sequences for the driven machine, and then develops reductions / approximations
for more general networks.

### Devadas (1991)

Srinivas Devadas, **“Optimizing Interacting Finite State Machines Using
Sequential Don't Cares,”** *IEEE Transactions on Computer-Aided Design of
Integrated Circuits and Systems* 10(12), 1473–1484, 1991.

The work is explicitly about optimization of interconnected finite-state-machine
descriptions using sequential don't-care information.  This makes “interacting
components permit additional minimization because some sequential behavior is
irrelevant/impossible in context” a mature synthesis problem, not a new CCOC
idea.

### Aziz, Singhal, Swamy & Brayton (1993/1994)

**“Minimizing Interacting Finite State Machines,”** UCB/ERL M93/68, 1993
(and later conference version).

The report explicitly addresses minimizing **collections of interacting FSMs**.
It says redundancies relative to the verified system behavior can be captured by
series of equivalence relations, while direct minimization of the complete
product can be prohibitively large.  It therefore develops hierarchical
minimization procedures.

### CCOC consequence

The phrase “composition changes what can safely be forgotten” is not enough to
distinguish CCOC from prior FSM synthesis/verification.  Nor is the contrast
between small components and a large product/composite machine by itself novel.

---

## 4. Permissible behavior / unknown-component ancestry

Y. Watanabe and Robert K. Brayton, **“The Maximum Set of Permissible Behaviors
for FSM Networks,”** UCB/ERL M93/61, 1993.

This report considers interacting FSMs and asks for the complete set of
sequential functionalities that can replace a component **while preserving the
behavior of the total system**.  It represents that complete flexibility by an
E-machine.

Larrauri & Bloem (2021) explicitly places this E-machine approach in the lineage
of the unknown-component / tail-synthesis problem.

### CCOC consequence

CCOC's positive “what alternative local behavior remains compatible with a
larger composition?” side is adjacent to a substantial permissible-behavior and
component-synthesis literature.  The manuscript should not frame finite
conservative portability or permissible replacement as an unprecedented general
concept.

---

## 5. Modern input-restriction testing makes the composition link explicit

Alberto Larrauri and Roderick Bloem, **“Conformance Testing of Mealy Machines
Under Input Restrictions,”** arXiv:2206.07441 (2022).

Its abstract explicitly studies **networks of interconnected Mealy machines** in
which the component under test is observable but its **inputs are under the
control of other white-box components**.

### CCOC consequence

Environment/component-induced restriction of the admissible input grammar is not
merely an old circuit-synthesis trick; it is an explicit modern formal-testing
model.  CCOC must distinguish itself from this literature by the quantity being
bounded and by its sharp construction, not by saying that composition determines
which interventions/inputs are legal.

---

## 6. State-identification testing: families of future probes jointly refine state

FSM testing has a long state-identification tradition: distinguishing sequences,
UIO sequences, characterizing sets/W-sets, harmonized identifiers, and adaptive
state-identification procedures.

Relevant modern anchors include:

- Hierons & Türker's work on distinguishing sequences and characterizing/state
  identifier sets;
- van den Bos & Vaandrager, **“State Identification for Labeled Transition
  Systems with Inputs and Outputs”** (arXiv:1907.11034), which generalizes state
  identification beyond classical deterministic FSMs and explicitly discusses
  compatible states that cannot be distinguished by available tests.

A characterizing set is, in effect, a family of input sequences whose responses
jointly separate state pairs.  Thus the CCOC statement that several legal future
word families together induce the common refinement of their individual response
partitions is testing-theory substrate, not a novelty claim.

### CCOC consequence

Do not sell the `union_grammar_refinement` theorem as a new state-identification
principle.  Its value inside CCOC is bookkeeping: it separates the portion of
interface inflation already encoded by the union of closed future tests from the
additional inflation caused by genuinely open-only future words.

---

## 7. Static join/refinement and local-latency ancestry remain non-novel

Separate audits already identified:

- relational database natural-join / lossless-decomposition ancestry for the
  static shared-base refinement capacity and realizability defect;
- regular-language / automata product-state complexity ancestry for
  multiplicative refinement blow-ups;
- Kraft/McMillan coding ancestry for prefix-free address depth;
- local/distributed-computation ancestry for finite-radius / one-edge-per-round
  information propagation.

Those facts remain useful because the CCOC construction **saturates** the
corresponding bounds, not because the bounds themselves are new.

---

## 8. Revised novelty matrix

| CCOC element | Closest established ancestry | Current novelty status |
|---|---|---|
| Fixed-grammar exact quotient | Myhill–Nerode, FSM minimization, bisimulation | **Not novel** |
| Compression under restricted inputs | Kim–Newborn 1972; incomplete-FSM minimization | **Not novel** |
| Component becomes smaller in a context | Kim–Newborn; Larrauri–Bloem tail minimization | **Not novel** |
| Restrictions generated by interconnected components | Wang–Brayton; Larrauri–Bloem 2022 | **Not novel** |
| Optimization/minimization of interacting FSM networks | Devadas; Aziz et al.; Brayton school | **Not novel** |
| Complete permissible replacement behavior | Watanabe–Brayton E-machine / unknown component | **Not novel** |
| Several tests jointly distinguish more states | FSM characterizing-set / state-identification theory | **Not novel** |
| Common-refinement / union-grammar identity | Equivalence intersection; state-identification substrate | **Not novel** |
| Static fibered capacity / missing combinations | natural join / lossless decomposition | **Not novel** |
| New test/action can split an old state class | classical distinguishability / partial-FSM testing | **Not novel** |
| Degree-3 binary routing | standard network / coding construction | **Not novel alone** |
| `O(log m)` local query latency lower bound | Kraft + finite-speed locality | **Not novel alone** |
| Full-product / parity / fixed-richness counting formulas | combinatorial constructions on the above substrate | **Not sufficient for priority** |
| `m` one-bit closed contexts + one-bit closed union/join + one newly legal primitive action + discrete `2^(m+1)` open quotient | no exact match found in this audit | **Residual candidate** |
| Same family also uses alphabet size 4, degree 3, pairwise local rules, constant local grammar, absolute memory saturation, and exact declared-locality latency saturation | no exact simultaneous match found in this audit | **Strongest residual candidate; priority unproven** |

---

## 9. What is mathematically strongest after this audit

The post-reopening package is still useful even after removing broad novelty
claims.  Its strongest theorem/construction statement is now:

### Exact accounting

On one finite comparison domain,

\[
\Delta_{\rm total}
=
\Delta_{\rm capacity}
-
\delta_{\rm join}
+
\iota_{\rm new},
\]

with `CORE-5`'s newly legal future-word split serving as the local witness for
`iota_new > 0`.

### Extremal dynamic witness

For `m=2^d` dormant binary memories:

\[
|P_j|=2\quad\forall j,
\qquad
|P_U|=C=2,
\]

while legalizing only the primitive action `fire` yields

\[
|P_O|=2^{m+1}.
\]

Hence

\[
\iota_{\rm new}=m.
\]

Because

\[
\iota_{\rm new}
\le
\log_2|D_m|-\log_2|P_U|=m,
\]

the witness attains the **absolute maximum possible open-only innovation** on its
finite domain.

The same family has:

- four primitive global actions in the open regime;
- only one newly legal primitive action;
- maximum graph degree three;
- pairwise selector and pulse updates;
- constant local state/message grammar;
- real routing dynamics already legal in each closed regime;
- query length `2 log2(m)+2`, equal to the lower bound in the explicitly declared
  one-edge selector/return-path architecture.

This simultaneous extremal package is currently the best remaining place to make
a novelty case.

---

## 10. Remaining high-priority literature questions

Before any firstness or “direct precedent absent” language, search specifically
for **quantitative worst-case separations**, not only problem formulations:

1. Kim–Newborn descendants: how large can the ratio/difference be between the
   minimal implementation under an input restriction and under the unrestricted
   input language?
2. Incomplete / partially specified Mealy machines: are there standard witness
   families where defining **one previously undefined input symbol/action** makes
   the minimal implementation jump from `O(1)` to `2^m` states or by `m` bits?
3. Sequential don't-care / interacting-FSM synthesis: are there bounded-degree or
   constant-alphabet worst-case constructions matching the CCOC relay?
4. FSM testing: are there constructions where one newly enabled primitive input,
   composed with previously available routing words, makes an exponentially
   larger set of states distinguishable?
5. Component minimization / unknown-component equations: is there a published
   extremal state-count theorem under changing admissible languages that already
   subsumes the CCOC single-action family?

Until those are answered, the correct manuscript wording is:

> **We give an extremal open-composition construction with no direct match found
> in our current literature audit.**

not:

> **We are the first to show that context-dependent input restrictions change
> state compression.**

---

## 11. Primary / authoritative references used in this gate

- Kim, J. & Newborn, M. M. (1972). *The Simplification of Sequential Machines
  with Input Restrictions*. IEEE Transactions on Computers 21(12):1440–1443.
- Devadas, S. (1991). *Optimizing Interacting Finite State Machines Using
  Sequential Don't Cares*. IEEE TCAD 10(12):1473–1484.
- Wang, H.-Y. & Brayton, R. K. (1993). *Input Don't Care Sequences in FSM
  Networks*. UCB/ERL M93/64.
- Watanabe, Y. & Brayton, R. K. (1993). *The Maximum Set of Permissible
  Behaviors for FSM Networks*. UCB/ERL M93/61.
- Aziz, A., Singhal, V., Swamy, G. M. & Brayton, R. K. (1993). *Minimizing
  Interacting Finite State Machines*. UCB/ERL M93/68.
- Larrauri, A. & Bloem, R. (2021). *Minimization and Synthesis of the Tail in
  Sequential Compositions of Mealy Machines*. arXiv:2105.10292.
- Larrauri, A. & Bloem, R. (2022). *Conformance Testing of Mealy Machines Under
  Input Restrictions*. arXiv:2206.07441.
- van den Bos, P. & Vaandrager, F. (2019/2021). *State Identification for Labeled
  Transition Systems with Inputs and Outputs*. arXiv:1907.11034 / later journal
  version.

The audit intentionally distinguishes these historical problem formulations from
the narrower unresolved question of whether the **simultaneous extremal CCOC
witness** already appears in the literature.
