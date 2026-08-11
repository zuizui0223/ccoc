# Composition code rate and conservation-constrained sharpness

> **Status:** post-reopening corollary/witness program built on the addressable
> codebook theorem. This note does not replace the historical v1 sharpness claim.

## Why code rate matters

The full-product witness can make it look as though linear interface inflation is
caused by statistically or combinatorially independent exterior modules. The
addressable-codebook theorem shows that independence is not the essential
quantity.

For a family of declared comparison domains `C_m`, define its zero-order or
Hartley code rate by

\[
R_0
=
\liminf_{m\to\infty}
\frac{1}{m}\log_2|C_m|.
\]

Let `B_m` upper-bound the largest number of closed factor labels realized on the
same domain:

\[
\max_j|f_{m,j}(C_m)|\le B_m.
\]

If the open grammar separates every codeword while each closed grammar factors
through its corresponding `f_{m,j}`, then the codebook theorem gives

\[
\Delta_m
:=
K_{\mathrm{open}}(C_m)
-
\max_jK_{\mathrm{closed},j}(C_m)
\ge
\log_2|C_m|-\log_2 B_m.
\]

Therefore, whenever

\[
R_0>0
\qquad\text{and}\qquad
\log_2 B_m=o(m),
\]

we obtain

\[
\boxed{
\liminf_{m\to\infty}\frac{\Delta_m}{m}\ge R_0.
}
\]

This is an immediate corollary, not a new quotient theorem. Its conceptual point
is that **positive combinatorial composition rate is sufficient for linear
interface inflation even when the admissible compositions are strongly
correlated**.

## Fixed-richness codebook

Take one focal inside bit `y` and `m` binary exterior modules. Impose a hard
conservation law: exactly `k` exterior modules are active.

\[
C_{m,k}
=
\left\{
(y,b_1,\ldots,b_m):
 y\in\{0,1\},\ b_j\in\{0,1\},\ \sum_{j=1}^{m}b_j=k
\right\}.
\]

Then

\[
|C_{m,k}|=2\binom{m}{k}.
\]

For every `j` and every `1<=k<=m-1`, all four pairs `(y,b_j)` occur. Hence the
standard closed projection has exactly four labels:

\[
|\pi_j(C_{m,k})|=4.
\]

If the open grammar contains uniform decoder words for `y,b_1,...,b_m`, the open
quotient on `C_{m,k}` is discrete:

\[
K_{\mathrm{open}}(C_{m,k})
=
1+\log_2\binom{m}{k}.
\]

If each closed context retains decoder words for `y` and its own `b_j`, then the
closed quotient is exactly four-state:

\[
K_{\mathrm{closed},j}(C_{m,k})=2.
\]

Therefore the exact restricted-domain gap is

\[
\boxed{
\Delta_{m,k}
=
\log_2\binom{m}{k}-1.
}
\]

This is already a strict non-product family: the allowed exterior configurations
occupy only one Hamming-weight layer of the binary cube.

## Fixed-density asymptotics

Let

\[
k_m=\lfloor\rho m\rfloor,
\qquad 0<\rho<1.
\]

Standard binomial-coefficient asymptotics give

\[
\log_2\binom{m}{k_m}
=
m h_2(\rho)
-\frac12\log_2 m
+O(1),
\]

where

\[
h_2(\rho)
=-\rho\log_2\rho-(1-\rho)\log_2(1-\rho)
\]

is binary entropy. Hence

\[
\boxed{
\Delta_{m,k_m}
=
m h_2(\rho)
-\frac12\log_2 m
+O(1).
}
\]

At half occupancy, `rho=1/2`,

\[
\Delta_{m,\lfloor m/2\rfloor}
=
m-\frac12\log_2 m+O(1).
\]

Thus almost the full linear slope of the Cartesian witness survives even though
the exterior composition obeys an exact fixed-richness constraint.

## Bounded-degree relay inheritance

The existing relay-tree compilation realizes every binary coordinate macrostate

\[
(y,b_1,\ldots,b_m)
\]

with a constant local node/message grammar, pairwise child-to-parent messages,
and maximum degree three. A macro probe of port `j` reads `b_j` into the focal
output while preserving the memory bits.

The fixed-richness family is simply a declared subset of those quiescent macro
states. Because the codebook theorem does not require the comparison domain to be
transition-closed, restricting admissible starting macrostates to
`C_{m,k}` does not change:

- the relay topology;
- the degree bound;
- the local state or message alphabet;
- the sequential probe grammar; or
- the correctness of any coordinate readout.

Consequently the same bounded-degree relay construction realizes the
fixed-richness addressable codebook. The locality claim is inherited; only the
admissible composition domain is restricted.

The number of selectable ports still grows with `m`. This remains a
constant-local-grammar result, not a constant-size global action-alphabet claim.

## Ecological reading

The fixed-richness family is useful because it rules out a simple objection to
the original witness. Linear inflation does not require every exterior species or
module to vary independently, nor does it require species richness to increase
with system size.

A composition family may keep exactly `k` exterior modules active at every time
and vary only *which* modules occupy those slots. If the number of admissible
identity combinations is exponential and future actions can distinguish those
identities, an exact portable interface still needs linear memory.

In that sense, the structural driver is not raw richness but the combinatorial
rate of future-distinguishable composition identity.

## What remains open

1. Determine whether a pair-separating word family, without coordinate decoders,
   is the natural weakest assumption.
2. Determine whether a code-rate quantity can be made necessary in a delimited
   class, rather than merely sufficient.
3. Compare the construction explicitly with Myhill--Nerode distinguishability,
   fooling sets, separating systems, coding theory, and communication-complexity
   lower bounds before promoting the code-rate language to a novelty claim.
4. Decide whether biologically motivated constraints beyond fixed richness
   (forbidden guild combinations, trophic feasibility, occupancy matroids, or
   spatial compatibility constraints) yield new sharp families rather than only
   applications of the same codebook corollary.
