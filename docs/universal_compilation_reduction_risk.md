# Universal-compilation reduction risk for the residual CCOC witness

> **Status:** conditional novelty-audit lemma. This document does **not** assert
> that Weiner–Hopcroft (1968), Williams (1975), or Newborn–Arnold (1972) satisfy
> the compiler contract below. It explains exactly which historical compiler
> properties would be sufficient to subsume the remaining bounded-local
> existence claim.

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

The remaining CCOC novelty candidate has therefore been the fact that the same
extremal effect has an explicit bounded-local realization.

But classical uniform-decomposition work is reported to compile arbitrary
synchronous sequential machines into networks of identical small modules with
bounded fan-in/fan-out. If such a compiler preserves external controls and timing
well enough, **local existence follows by compilation** and is not an independent
new phenomenon.

## 2. Input-preserving local compiler contract

Let `M` be a finite synchronous controlled machine over primitive input alphabet
`A`, with observable output `h`.

A compiler family `Comp` is sufficient for the reduction below if, for every
`M`, it produces a synchronous network `N=Comp(M)` satisfying:

### C1. Constant local state

There exists `q` independent of `|M|` such that every component of `N` has at
most `q` local states.

### C2. Bounded local connectivity

There exists `Delta` independent of `|M|` bounding component fan-in/fan-out or
network degree.

### C3. Fixed external control semantics

The compiled network is controlled by the same external alphabet `A`, or by a
fixed-size alphabet independent of `|M|` together with an input encoding whose
complexity is explicitly bounded.

### C4. Behavioral simulation

For every state in the declared comparison-domain embedding and every legal input
word `w`, the compiled focal/output trace determines the original trace of `M`.

### C5. Bounded time overhead

There is an explicit overhead function `tau` such that an original control word
of length `L` is simulated within at most

\[
T\le \tau(|M|,L).
\]

The important cases are constant slowdown, `O(L log |M|)`, or other polylogarithmic
overhead.

### C6. Restriction compatibility

If the original machine is studied under a restricted input language/grammar
`L_C`, the **same compiled network** can be studied by restricting its external
control language accordingly. The compiler must not require a completely
separate hardware network for every closed context.

This last condition is essential to the CCOC closed/open question.

## 3. Conditional reduction theorem

### Proposition

Assume a compiler satisfying C1–C6.
Let `M_m` be any centralized single-action innovation witness whose comparison
domain has

\[
|P_U(M_m)|=2,
\qquad
|P_O(M_m)|=2^{m+1}.
\]

Then the compiled network

\[
N_m=\operatorname{Comp}(M_m)
\]

has the same closed/open exact response separation on the embedded comparison
domain, up to the declared trace decoding. In particular,

\[
\iota_{\rm new}(N_m)\ge m,
\]

and if the compiled trace equivalence is faithful in both directions,

\[
\iota_{\rm new}(N_m)=m.
\]

Moreover C1–C2 give a constant-local-state, bounded-connectivity realization, and
C5 transfers the query-latency bound from the centralized witness through `tau`.

### Proof sketch

Every pair merged under the restricted centralized grammar produces identical
restricted traces. By C4 and C6, its compiled embeddings remain equivalent under
the corresponding restricted compiled grammar.

Every pair separated by an open centralized word has a compiled word whose trace
recovers the separating centralized trace. Hence all original open distinctions
survive compilation. The quotient-size statement follows on the embedded domain.
`C1`, `C2`, and `C5` provide the realization bounds. `square`

The proposition is elementary. Its role is novelty control: it shows why an old
**universal compiler theorem** can subsume a new-looking explicit local witness.

## 4. Stronger centralized seed with logarithmic query words

The centralized seed need not use a unary `advance^j` scan.
It can itself maintain a hidden finite controller that reads a binary address over
primitive controls `0/1`, followed by the newly legal `fire`.  With `m=2^d`
dormant memories, the centralized query words can have

\[
O(\log m)
\]

length before compilation.

Therefore, if a classical uniform decomposition preserves one original input
symbol per compiled synchronous step with constant slowdown, it would yield a
bounded-local maximal-innovation family with **logarithmic query latency** almost
immediately.

This is why the timing semantics of the old decomposition theorems are now a
decisive novelty question.

## 5. What current historical evidence does and does not show

### Weiner & Hopcroft (1968)

Available bibliographic and abstract evidence supports:

- arbitrary synchronous sequential machine as input;
- interconnection of identical two-state modules;
- fan-in/fan-out bound independent of the original state count.

The current audit has **not** verified from full text:

- exact external input encoding;
- original-clock versus slowed simulation;
- output decoding delay;
- module count and network diameter;
- restriction compatibility C6.

These are therefore `UNKNOWN`, not negative findings.

### Arnold–Tan–Newborn (1970)

The IBM abstract supports arbitrary synchronous flow-table realization by an array
of identical modules in a regular pattern. The same input/time/restriction details
remain unresolved from the abstract.

### Williams (1975)

Bibliographic evidence confirms uniform decomposition of incompletely specified
sequential machines. A secondary abstract-style copy says incomplete
specification can reduce the number of universal two-state components. Original
source verification and compiler-overhead details remain outstanding.

### Jóźwiak–Ślusarczyk (2004)

The accessible ScienceDirect text establishes a very broad theory of constrained
network decomposition for incompletely specified sequential machines. It does not,
in the passages reviewed so far, give the particular compiler constants needed
to settle C1–C6 for the CCOC extremal family.

## 6. Decision tree for CCOC novelty

### Case A — old compiler satisfies C1–C6 with constant or logarithmic overhead

Then bounded-local existence and logarithmic access are largely generic
consequences of classical sequential-machine compilation. The current relay may
remain useful as a clean explicit construction, but it should **not** carry the
main mathematical novelty claim.

### Case B — old compiler has bounded modules but large/nonlocal input distribution
or large time overhead

Then the explicit CCOC relay may retain a quantitative realization theorem:
small external alphabet, degree three, radius-one pairwise updates, and
`Theta(log m)` causal access simultaneously.

### Case C — old incomplete-specification decompositions require different hardware
for different restricted contexts

Then CCOC's “same hardware, grammar opens” contract remains a meaningful
structural distinction.

## 7. Immediate literature checklist

For the historical full texts, extract a literal table of:

- module state count;
- module fan-in;
- module fan-out;
- number of modules as a function of original state/input count;
- external input alphabet / distribution mechanism;
- one-clock versus multi-clock simulation;
- output decoding mechanism and latency;
- whether the same decomposed network supports different admissible input
  languages simply by restricting external inputs;
- whether incomplete-specification optimization changes only machine behavior or
  also changes the hardware decomposition.

Until this is resolved, the safe description is:

> **CCOC gives an explicit extremal bounded-local realization; whether its
> existence follows from classical universal sequential-machine decomposition
> with comparable overhead is an open historical-comparison question.**
