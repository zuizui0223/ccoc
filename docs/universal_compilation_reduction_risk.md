# Universal-compilation reduction risk for the residual CCOC witness

> **Status:** conditional novelty-audit lemma. This document does **not** assert
> that Weiner–Hopcroft (1968), Hsieh–Tan–Newborn (1968), Ullman–Weiner (1969),
> Newborn–Arnold (1972), or Williams (1975) satisfy the compiler contract below.
> It states the properties that would be sufficient to subsume the bounded-local
> existence claim and corrects an earlier one-way-simulation gap in that reduction.

## 1. Why this matters

A centralized finite-state witness already gives maximal one-action innovation:
closed operation can route among dormant memory coordinates while withholding one
reveal action; adding that one action makes every dormant coordinate observable.
Thus

\[
|P_U|=2,
\qquad
|P_O|=2^{m+1},
\qquad
\iota_{\rm new}=m.
\]

The remaining CCOC realization question is whether this extremal response
separation can be implemented under bounded local resources without paying a
large control/timing cost.

Classical uniform-decomposition work is close enough that a sufficiently faithful
compiler could make local existence generic. The compiler reduction therefore has
to preserve **both distinctions and equivalences** of the source response
quotient, not merely permit reconstruction of source outputs from a richer
compiled trace.

## 2. Corrected compiler contract

Let `M` be a finite synchronous controlled machine over primitive input alphabet
`A`, with declared source observable trace `Tr_M`. Let `D` be the comparison-domain
embedding used by the CCOC witness.

A compiler `Comp` produces one synchronous network

\[
N=\operatorname{Comp}(M)
\]

with state embedding `e` and a context-independent input-word encoding `c`.

### C1. Constant local state

There exists `q` independent of `|M|` such that every component of `N` has at
most `q` local states.

### C2. Bounded local connectivity

There exists `Delta` independent of `|M|` bounding component fan-in/fan-out or
network degree.

### C3. Fixed, context-independent external control encoding

The same source word `w` is represented by the same compiled word `c(w)`
regardless of which closed/open sublanguage is later being studied. The compiled
primitive alphabet is either the original `A` or a fixed-size alphabet independent
of `|M|`, and the cost of `c` is explicitly bounded.

The important point is **context independence**. A construction that invents a
new codebook or recompiles the network separately for every restricted language
does not satisfy this contract.

### C4. Exact response-trace faithfulness on the embedded domain

For every source word `w` in the full source control language and all embedded
source states `s,s' in D`,

\[
\operatorname{Tr}_M(s,w)=\operatorname{Tr}_M(s',w)
\quad\Longleftrightarrow\quad
\operatorname{Obs}_N(e(s),c(w))=\operatorname{Obs}_N(e(s'),c(w)).
\]

Equivalent formulations are allowed, for example a decoded compiled observable
that is exactly the source trace and contains no state-dependent side channel on
the comparison domain.

This two-way condition is stronger than merely requiring that the compiled trace
**determines** the source trace. One-way decodability preserves source
distinctions but can introduce spurious compiled distinctions, which would destroy
the small closed quotient and is therefore insufficient for the CCOC reduction.

### C5. Bounded time overhead

There is an explicit overhead function `tau` such that an original control word of
length `L` is represented within

\[
|c(w)|\le \tau(|M|,L),
\]

or an equivalent source-step to compiled-network-round/output-latency guarantee.
The important cases are constant slowdown or comparable polylogarithmic overhead.

## 3. Restriction compatibility is largely derived, not independent

Earlier versions of this audit listed a separate condition C6 requiring the same
compiled hardware to support restricted and open input grammars. Under C3 and C4
above, that property follows immediately for ordinary sublanguage restriction.

### Restriction-compatibility lemma

Let `L_C` be any source sublanguage of the full source language `L_O`. Keep the
single compiled network `N=Comp(M)` fixed and define the corresponding compiled
control grammars

\[
c(L_C)=\{c(w):w\in L_C\},
\qquad
c(L_O)=\{c(w):w\in L_O\}.
\]

Then for embedded source states `s,s'`,

\[
s\equiv_{L_C}^{M}s'
\quad\Longleftrightarrow\quad
 e(s)\equiv_{c(L_C)}^{N}e(s'),
\]

and likewise for `L_O`.

### Proof

The source equivalence is equality of source traces for every word in `L_C`.
Apply C4 word by word. Because C3 uses one context-independent encoding and one
fixed compiled network, restricting from `L_O` to `L_C` changes only the set of
compiled words being quantified over. No recompilation is needed. `square`

### Consequence

A historical compiler theorem that already gives one fixed full-language
realization with context-independent controls and exact response-trace faithfulness
does **not** need a separate theorem about every restricted language. Same-hardware
restriction is automatic.

A separate C6-type audit remains relevant only when:

- the historical construction is synthesized from an incompletely specified
  machine rather than from one full machine;
- the input encoding itself depends on the allowed language/context;
- the compiler exposes additional observables that make C4 fail;
- or the hardware/wiring is changed when the specification is restricted.

## 4. Corrected conditional reduction theorem

### Proposition

Assume C1–C5 above. Let `M_m` be a centralized single-action innovation witness on
comparison domain `D_m` with

\[
|P_U(M_m)|=2,
\qquad
|P_O(M_m)|=2^{m+1}.
\]

Then the **same** compiled network

\[
N_m=\operatorname{Comp}(M_m)
\]

has, on the embedded domain `e(D_m)`, exactly the corresponding closed and open
response quotients under `c(L_U)` and `c(L_O)`:

\[
|P_U(N_m)|=2,
\qquad
|P_O(N_m)|=2^{m+1},
\qquad
\iota_{\rm new}(N_m)=m.
\]

C1–C2 supply constant local state and bounded connectivity; C5 transfers the
control/query latency through the encoding overhead.

### Proof

For each grammar separately, source response equivalence is equality of traces for
all words in that grammar. By the restriction-compatibility lemma, C3–C4 preserve
that equivalence **in both directions** on the embedded domain. Therefore the
closed and open quotient partitions are isomorphic to the source partitions.
Their class counts and innovation difference are unchanged. `square`

## 5. Why the correction matters

The previous proof sketch used one-way behavioral simulation to say that states
merged by the source closed grammar remain merged after compilation. That inference
was not valid: a simulator may preserve all source outputs while leaking extra
state-dependent information in its compiled observable.

The corrected audit therefore distinguishes two levels:

1. **one-way simulation / source-trace decoding** — enough to preserve open
   distinctions and give a lower bound on compiled open complexity;
2. **two-way response-trace faithfulness** — required to preserve the small closed
   quotient and hence the complete restricted→open separation.

This makes the novelty gate more precise. It also makes the historical risk
potentially stronger: once a classical compiler has full-language two-way
faithfulness with a fixed encoding, same-hardware grammar restriction is no longer
an additional escape hatch.

## 6. Strong centralized seed and timing

The centralized seed can maintain a hidden finite controller that reads a binary
address over primitive controls `0/1`, followed by the newly legal `fire`.
For `m=2^d` dormant memories, source query words have

\[
O(\log m)
\]

length before compilation.

Thus a classical compiler with constant source-step slowdown would already yield a
bounded-local maximal-innovation family with logarithmic query latency. C5 remains
a decisive quantitative historical question.

## 7. Revised historical extraction checklist

The primary-source audit should now prioritize four independent resources rather
than treating old C6 as a fully separate clause:

### H1 — local resource bounds

- module state count;
- fan-in/fan-out or graph degree;
- number of modules and depth/diameter.

### H2 — input encoding

- source input convention;
- direct versus encoded/distributed controls;
- whether the encoding is fixed for the full source machine and independent of
  later language restriction;
- code length / distribution overhead.

### H3 — response-trace faithfulness

- what source output is reproduced;
- whether compiled observables contain extra state-dependent information;
- whether source trace equality implies equality of the declared compiled
  observable trace, not only the reverse implication;
- output decoding location and delay.

### H4 — timing

- one source step versus number of network rounds;
- delay semantics;
- output latency;
- asymptotic slowdown.

For Williams-style incomplete-specification synthesis, additionally ask whether a
new network is synthesized for each incomplete specification. That question is
still relevant because such a method may not begin with one fixed full-language
compiler at all.

## 8. Decision tree for CCOC realization novelty

### Case A — classical compiler satisfies H1–H4 with constant/comparable overhead

Then bounded-local existence and same-hardware restricted/open realization are
largely generic consequences of classical compilation. The explicit CCOC relay is
a clean constrained witness, not the main novelty.

### Case B — one-way simulation only

Then classical compilation preserves the source open distinctions but may add
spurious closed distinctions. It does not directly subsume the complete CCOC
closed/open quotient package.

### Case C — bounded local modules but expensive input or timing resources

Then CCOC may retain a quantitative realization distinction through its fixed
four-symbol controls, degree-three radius-one dynamics, constant local grammar,
and `Theta(log m)` addressed access.

### Case D — specification-dependent resynthesis

If incomplete/restricted machines are decomposed into different hardware rather
than obtained by restricting one full-machine realization, that literature is
strong ancestry for contextual decomposition but does not by itself provide the
same-hardware CCOC comparison.

## 9. Current safe description

Until the primary historical constructions are extracted:

> **CCOC gives an explicit extremal bounded-local realization. A classical
> full-language compiler would subsume that realization if it simultaneously has
> bounded local resources, context-independent external controls, two-way
> response-trace faithfulness, and comparable timing overhead. Under those
> conditions, same-hardware restriction to closed grammars follows automatically.**

This is a novelty-control statement, not a priority claim.