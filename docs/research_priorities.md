# Research priorities: reopened theorem development

## Governing rule

RACH/CCOC is again an **active theorem-development repository** as of 2026-08-11.
The July 2026 manuscript freeze remains a reproducibility checkpoint, not a ban
on new mathematics.

The first-paper spine remains the baseline:

\[
\text{exact grammar-aware interface}
\; + \;
\text{extension--compression noncommutation}
\; + \;
\text{relay sharpness}
\; + \;
\text{conservative portability boundary}.
\]

New work should strengthen a canonical claim rather than accumulate nearby
special cases. Development must occur on a branch and enter `main` by pull
request.

RACH remains a mathematical-ecology repository for finite formal models and
theorem certificates. It contains no empirical datasets, field inference, or
claims of ecological validation.

## Priority 1 — weaken the product assumption in CORE-2

The v1 lower bound assumes a full product-indexed subset

\[
S^*\cong I\times E_1\times\cdots\times E_q.
\]

That assumption is sufficient but stronger than the injection proof actually
needs. The immediate target is an **addressable codebook theorem**.

Let

\[
C\subseteq I\times E_1\times\cdots\times E_q
\]

be any finite jointly realizable codebook embedded in the controlled state space.
Assume one legal decoder word per coordinate recovers that coordinate uniformly
on `C`. Then distinct codewords are pairwise separated by a legal future word,
so

\[
\boxed{K_{\mathrm{open}}\ge \log_2|C|.}
\]

For closed context `j`, if every declared closed response factors through the
projection

\[
\pi_j(i,e_1,\ldots,e_q)=(i,e_j),
\]

then

\[
K_{\mathrm{closed},j}\le \log_2|\pi_j(C)|.
\]

Therefore the candidate strengthened noncommutation inequality is

\[
\boxed{
K_{\mathrm{open}}-\max_jK_{\mathrm{closed},j}
\ge
\log_2|C|-\max_j\log_2|\pi_j(C)|.
}
\]

The v1 product theorem is the special case

\[
C=I\times\prod_jE_j.
\]

This is a strict assumption weakening whenever `C` is correlated or constrained
and is not a Cartesian product.

### Required proof obligations

1. State the codebook theorem without pretending that coordinate cardinalities
   alone imply the lower bound.
2. Prove the open lower bound by explicit pair separation / injection.
3. Prove the closed upper bound only from a declared response factorization.
4. Record exactly when equality holds; factorization alone gives an upper bound.
5. Give a non-product family with an asymptotically growing gap.
6. Check whether the bounded-degree relay construction can realize or restrict to
   that family without enlarging local node/message grammar.
7. Compare the codebook formulation with combinatorial rectangle, fooling-set,
   communication-complexity, automata, and abstraction lower-bound literature
   before making a stronger novelty claim.

## Priority 2 — non-product sharpness family

The first target is a binary constrained codebook whose size is exponential but
which is not a full Cartesian product. A parity-constrained family is the
simplest candidate:

\[
C_m=\{x\in\{0,1\}^{m+1}: x_0\oplus x_1\oplus\cdots\oplus x_m=0\}.
\]

Then

\[
|C_m|=2^m,
\]

while every two-coordinate projection `(x_0,x_j)` is all of `\{0,1\}^2` for
`m\ge2`. Hence the codebook inequality gives

\[
K_{\mathrm{open}}\ge m,
\qquad
K_{\mathrm{closed},j}\le2,
\qquad
\boxed{K_{\mathrm{open}}-\max_jK_{\mathrm{closed},j}\ge m-2.}
\]

This witnesses a linear separation without a full product state subset. The next
question is whether a bounded-degree relay implementation can attain equality or
an asymptotically matching gap under the constrained global state set.

## Priority 3 — determine the true combinatorial invariant

The codebook size bound suggests that raw coordinate count is not fundamental.
The quantity controlling the separation may instead be the number of jointly
realisable, future-separable response types relative to the largest closed
projection. Candidate invariant:

\[
\Delta_0(C)
=
\log_2|C|-\max_j\log_2|\pi_j(C)|.
\]

The research question is whether `\Delta_0` is merely a sufficient counting
lower bound or the correct sharp invariant for an explicitly delimited class of
open/closed grammar pairs. Do not claim necessity until a converse is proved.

## Historical v1 publication core

| Asset | Role in first paper |
|---|---|
| `CORE-1` | definition of exact grammar-aware interface |
| `CORE-2` | product addressability / noncommutation lower bound |
| `CORE-3` | bounded-degree binary sharpness witness |
| `CORE-4` | sufficient conservative schema boundary |
| `CORE-5` | local fiber-split negative boundary |

The v1 default test gate continues to cover these assets. New theorem work must
not silently change what a historical v1 replay certifies.

## Companion directions

Delayed exposure, candidate-mechanism uncertainty, panel design, stochastic or
approximate extensions, and empirical case studies are no longer prohibited by a
freeze. They are nevertheless lower priority than strengthening the CORE-2/3
novelty spine and should be opened only through a separate scope decision.

Replacement, extinction, recolonization, and rewiring transport remain centered
in `zuizui0223/mltr`.

## Promotion rule

A new active result should name exactly which canonical claim it changes:

\[
\text{exact interface},\qquad
\text{addressability obstruction},\qquad
\text{portable composition},\qquad
\text{or finite-evidence identifiability}.
\]

It should also state whether the change is a strict assumption weakening, a
stronger conclusion, a converse/necessity result, a sharper construction, or a
new model class. A nearby special case alone remains insufficient reason to grow
the theorem registry.
