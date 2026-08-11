# FSM novelty gate addendum: environment abstraction and the nonlocal one-action baseline

> **Purpose.** This addendum narrows the residual CCOC novelty candidate further.
> It records two points found after the main historical FSM audit:
>
> 1. environment abstraction for interacting FSM networks is itself established
>    prior work; and
> 2. even **absolute-maximal interface innovation caused by one newly legal
>    primitive action** is elementary if spatial/locality constraints are removed.
>
> Therefore the remaining priority question is not “can one action unlock many
> behavioral distinctions?” but whether the **simultaneous local sharpness
> package** already appears in prior finite-state / circuit / distributed-system
> literature.

## 1. Environment abstraction is direct prior art

Richard Raimi, Ramin Hojati, and Kedar S. Namjoshi,
**“Environment modeling and language universality,”**
*ACM Transactions on Design Automation of Electronic Systems* 5(3):705–725,
2000, DOI 10.1145/348019.348572.

The published abstract describes the environment-modeling problem as **abstracting
component finite-state machines bordering an FSM of interest within a network of
interacting FSMs**, explicitly with automatic state reduction of large FSM
networks as the goal.  It studies safe removal of a component under trace
equivalence, language universality, input independence, and simulation-based
abstraction when complete removal is impossible.

### CCOC consequence

Do not claim novelty for any broad formulation such as:

> the surrounding network/environment determines which distinctions of a focal
> finite-state component can be abstracted away.

That idea is directly in the environment-modeling literature.  CCOC must remain
focused on its quantitative closed/open interface accounting and sharp witness.

---

## 2. Bounded-fanout sequential-circuit work is a locality watchlist

Monroe M. Newborn and Thomas F. Arnold,
**“Universal Modules for Bounded Signal Fan-Out Synchronous Sequential
Circuits,”** *IEEE Transactions on Computers* 21(1):63–79, 1972.

The bibliographic record is clear, but the full text was not obtained in the
current audit.  We therefore **do not infer its construction or theorem from the
title**.

It nevertheless belongs on the high-priority locality watchlist because the
current CCOC residual candidate uses:

- synchronous sequential dynamics;
- bounded network degree / fan-out-like restrictions;
- a repeated finite local grammar;
- a large family compiled into a bounded-local architecture.

Before claiming that the CCOC relay is the first relevant bounded-local
realization, the Newborn–Arnold paper and its “uniform modular realization”
lineage should be read in full.

---

## 3. One-action maximal innovation is elementary without locality

The single-action CCOC relay proves that one newly legal primitive action can
create the maximum possible `m` bits of open-only exact interface innovation.
That is a strong property of the **local relay construction**, but the same
state-count phenomenon is easy to realize in a centralized finite-state machine.

### Centralized unlock-and-scan witness

Fix `m` dormant binary values

\[
 b=(b_0,\ldots,b_{m-1})\in\{0,1\}^m
\]

and one currently visible bit `y`.

The declared comparison domain contains initial states

\[
 D_m=\{(y,b,p=0):y\in\{0,1\}, b\in\{0,1\}^m\}.
\]

The machine has two primitive controls:

\[
A_O=\{\mathsf{advance},\mathsf{fire}\}.
\]

Closed operation allows only `advance`.

- `advance` increments a hidden pointer `p` modulo `m` but leaves the visible
  output equal to `y`;
- `fire` enters a readout state whose output is the currently addressed `b_p`.

The pointer states and readout states are ordinary transient states outside the
comparison-domain slice `p=0`; exact interface memory is evaluated on the stated
comparison domain, just as in the CCOC codebook/domain results.

### Closed quotient

Every closed word is `advance^k`.  Its entire output trace is the repetition of
`y`, regardless of `b`.  Therefore

\[
|P_C(D_m)|=2.
\]

### Open quotient after adding one primitive action

Opening the grammar adds only the primitive symbol `fire`.
For each memory coordinate `j`, the word

\[
 w_j=\mathsf{advance}^{j}\mathsf{fire}
\]

has final output `b_j`.

Together with the current output `y`, the words `w_0,\ldots,w_{m-1}` distinguish
every element of `D_m`.  Hence

\[
|P_O(D_m)|=2^{m+1}.
\]

Thus

\[
\boxed{
\iota_{\rm new}=m
}
\]

and, because this makes the open quotient discrete, the construction also
saturates the absolute finite-domain innovation bound.

### What this eliminates as a novelty claim

Therefore CCOC must **not** claim novelty for any of the following by itself:

- one newly legal primitive input/action creating an arbitrarily large state
  distinction;
- one new primitive action creating the absolute maximum possible finite-domain
  innovation;
- routing/selection operations existing before the revealing action becomes
  legal, in the absence of a locality restriction.

A centralized pointer already gives all of these.

---

## 4. What remains genuinely unresolved

The nonlocal baseline removes almost all purely automata-theoretic drama from the
single-action statement.  The remaining candidate is the fact that the **same
extremal effect survives severe realization constraints simultaneously**.

For the CCOC relay family:

\[
|P_j|=2\quad\forall j,
\qquad
|P_U|=C=2,
\qquad
|P_O|=2^{m+1},
\]

while:

- only one primitive action is newly legal;
- open primitive alphabet size is four;
- address routing is already legal in the fixed closed contexts;
- selector and response signals move by pairwise adjacent-node updates;
- maximum degree is three;
- local state/message grammar is constant in `m`;
- open-only innovation reaches its absolute finite-domain maximum `m` bits;
- query latency reaches the lower bound of the explicitly declared
  selector-plus-return-path local architecture.

The novelty question is therefore now:

> **Has this type of maximal restricted-input → unrestricted-input behavioral
> blow-up already been realized/proved under comparable bounded-local sequential
> architecture constraints?**

That is substantially narrower than the original CCOC novelty claim.

---

## 5. Next literature targets

Search full texts for:

1. Newborn & Arnold (1972), bounded signal fan-out universal modules;
2. Newborn's earlier uniform modular realization of sequential machines;
3. Kim–Newborn descendants that quantify worst-case state-count increase when an
   admissible input language is enlarged;
4. Rho–Somenzi / Brayton-school sequential-don't-care papers for extremal
   examples under network restrictions;
5. pseudo-nondeterministic / incompletely specified FSM minimization for examples
   where specifying a small number of previously don't-care inputs forces a large
   state expansion;
6. LOCAL/distributed automata or network-query constructions combining bounded
   degree, fixed local rules, and state-identification / query access.

Until those searches are complete, use **“extremal local construction with no
direct match found in the current audit”**, not a priority claim.

## References / provenance

- Raimi, R., Hojati, R., & Namjoshi, K. S. (2000). *Environment modeling and
  language universality*. ACM TODAES 5(3):705–725.
- Newborn, M. M., & Arnold, T. F. (1972). *Universal Modules for Bounded Signal
  Fan-Out Synchronous Sequential Circuits*. IEEE Transactions on Computers
  21(1):63–79.

The environment-modeling description above is supported by the published
abstract.  The Newborn–Arnold entry is used only as a bibliographic/watchlist
anchor because its full text was not obtained in this audit.
