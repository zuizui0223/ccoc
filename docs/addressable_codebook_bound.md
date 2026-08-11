# Addressable-codebook extension--compression bound

> **Status:** post-reopening theorem-strengthening candidate. This note is not yet
> part of the historical July 2026 `CORE-1`--`CORE-5` replay. It strictly weakens
> the full-product premise of the v1 addressability theorem if the proof and
> finite certificate review pass.

## Motivation

The v1 theorem assumes a product-indexed subset

\[
S^*\cong I\times E_1\times\cdots\times E_q.
\]

The injection proof does not actually need every Cartesian combination to exist.
It only needs a sufficiently large set of jointly realizable states whose
coordinate labels can be recovered by declared legal future words.

That observation leads to a codebook formulation.

## Setup

Let a finite deterministic controlled response system have state space `S`, a
declared legal word family `L`, and response map

\[
R:S\times\mathcal L\to\mathcal Y.
\]

Define the exact response equivalence

\[
s\equiv_{\mathcal L}s'
\iff
\forall w\in\mathcal L,\quad R(s,w)=R(s',w),
\]

and exact interface memory

\[
K_{\mathcal L}=\log_2|S/\!\equiv_{\mathcal L}|.
\]

Let

\[
C\subseteq I\times E_1\times\cdots\times E_q
\]

be any finite set of distinct codewords, together with an injective embedding

\[
\eta:C\hookrightarrow S.
\]

No Cartesian closure assumption is made: `C` may contain arbitrary correlations,
constraints, forbidden combinations, or parity relations.

## Operational coordinate addressability

For every coordinate `k=0,...,q`, suppose there is one legal word `r_k` and one
decoder `d_k` such that

\[
d_k(R(\eta(c),r_k))=c_k
\qquad\forall c\in C.
\]

The same word and decoder must work uniformly over the entire codebook.

## Theorem — Addressable-codebook lower bound

Under the assumptions above,

\[
\boxed{K_{\mathrm{open}}\ge\log_2|C|.}
\]

### Proof

Take distinct `c,c' in C`. Because they are distinct finite tuples, some
coordinate `k` differs. The declared decoder returns

\[
d_k(R(\eta(c),r_k))=c_k\neq c'_k=d_k(R(\eta(c'),r_k)).
\]

Therefore the two responses to `r_k` cannot be equal, so

\[
\eta(c)\not\equiv_{\mathcal L}\eta(c').
\]

Thus the exact open quotient contains at least one class per codeword. Hence it
has at least `|C|` classes, and taking base-two logarithms gives the result.
`\square`

The proof is still an operational injection argument. It no longer derives the
bound from the ambient coordinate cardinalities.

## Closed-context upper bound

For each fixed context `j`, let

\[
\pi_j(c)=(c_0,c_j)
\]

where coordinate `0` is the inside coordinate and coordinate `j` is the relevant
exterior coordinate. Suppose every declared closed response factors through this
projection:

\[
R_j(\eta(c),w)=F_{j,w}(\pi_j(c))
\qquad\forall c\in C,\ \forall w\in\mathcal L_j.
\]

Then `\pi_j` is a sound closed interface on the codebook, giving

\[
\boxed{K_{\mathrm{closed},j}\le\log_2|\pi_j(C)|.}
\]

As in v1, equality needs extra closed decoder/separation assumptions; response
factorization alone gives an upper bound.

## Strengthened noncommutation inequality

Combining the open lower bound and closed upper bounds gives

\[
\boxed{
K_{\mathrm{open}}-
\max_jK_{\mathrm{closed},j}
\ge
\log_2|C|-
\max_j\log_2|\pi_j(C)|.
}
\]

Define the codebook separation quantity

\[
\Delta_0(C)
=
\log_2|C|-
\max_j\log_2|\pi_j(C)|.
\]

At present `\Delta_0(C)` is a proved lower-bound expression under the declared
operational and factorization premises. It is **not** claimed to be a necessary
or universally complete invariant.

## Recovery of the v1 product theorem

If

\[
C=I\times\prod_{j=1}^qE_j,
\]

then

\[
|C|=|I|\prod_j|E_j|
\]

and

\[
|\pi_j(C)|=|I||E_j|.
\]

Therefore the codebook inequality reduces exactly to

\[
K_{\mathrm{open}}-
\max_jK_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-
\max_j\log_2|E_j|,
\]

which is the v1 Extension--Compression Noncommutation Inequality.

## Non-product linear-gap family

For `m>=2`, take the binary even-parity code

\[
C_m
=
\left\{
(x_0,x_1,\ldots,x_m)\in\{0,1\}^{m+1}:
\bigoplus_{k=0}^{m}x_k=0
\right\}.
\]

This is not a Cartesian product because exactly half of the ambient bit strings
are absent. Its size is

\[
|C_m|=2^m.
\]

For every exterior coordinate `j`, every pair `(x_0,x_j)` is realized when
`m>=2`, so

\[
|\pi_j(C_m)|=4.
\]

Hence

\[
K_{\mathrm{open}}\ge m,
\qquad
K_{\mathrm{closed},j}\le2,
\]

and

\[
\boxed{
K_{\mathrm{open}}-
\max_jK_{\mathrm{closed},j}
\ge m-2.
}
\]

Thus a linearly growing extension--compression gap does not require a full
Cartesian product of independently variable exterior coordinates.

## What has and has not been weakened

The theorem removes **Cartesian closure** of the realizable state family. It does
not remove all joint-realizability requirements: the codewords in `C` must still
correspond to actual states in the declared model. Nor does it remove operational
addressability: each coordinate must still be uniformly recoverable by a legal
future word.

A further strengthening would replace coordinate-wise decoders with a more
general pair-separating family of future words. In that formulation, the truly
minimal premise may be a large set of states that is pairwise separated by the
open grammar while every closed grammar induces a small quotient. That direction
should be compared carefully with fooling sets, separating systems,
communication-complexity lower bounds, and automata minimization before a novelty
claim is expanded.

## Executable witness

`causal_model.addressable_codebooks` provides:

- `OperationalAddressableCodebookCertificate` for finite coordinate decoding;
- `OperationalCodebookClosedContextCertificate` for finite closed
  factorizations;
- a canonical readout realization for arbitrary finite codebooks; and
- `even_parity_codebook(m)` as the first non-product regression family.

These are finite witness replays. The all-cardinality theorem is the symbolic
pair-separation proof above.
