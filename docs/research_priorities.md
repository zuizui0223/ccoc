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

The v1 lower bound assumes a full product-indexed comparison set

\[
S^*\cong I\times E_1\times\cdots\times E_q.
\]

That assumption is sufficient but stronger than the injection proof actually
needs. The immediate strengthening is an **addressable codebook theorem**.

Let

\[
C\subseteq I\times E_1\times\cdots\times E_q
\]

be any finite jointly realizable codebook, injectively embedded as a declared
comparison domain `D_C` in a controlled state space. Assume one legal decoder
word per coordinate recovers that coordinate uniformly on `C`. Then the open
response quotient restricted to `D_C` is discrete:

\[
\boxed{K_{\mathrm{open}}(D_C)=\log_2|C|.}
\]

Consequently the full open system satisfies

\[
K_{\mathrm{open}}(S)\ge\log_2|C|.
\]

For closed context `j`, if every declared closed response on the **same comparison
domain** factors through

\[
\pi_j(i,e_1,\ldots,e_q)=(i,e_j),
\]

then

\[
K_{\mathrm{closed},j}(D_C)
\le
\log_2|\pi_j(C)|.
\]

Therefore

\[
\boxed{
K_{\mathrm{open}}(D_C)-
\max_jK_{\mathrm{closed},j}(D_C)
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

A codebook-only closed factorization does **not** upper-bound a larger full closed
state space outside `D_C`. A full-system gap claim needs an additional full
closed-domain factorization or other explicit upper-bound contract.

### Completed proof obligations in PR #107

1. State the codebook theorem without pretending that coordinate cardinalities
   alone imply the lower bound.
2. Prove the open codebook quotient is discrete by explicit pair separation.
3. Separate the full-open lower bound from the restricted closed/open comparison.
4. Prove the closed upper bound only from a declared response factorization on
   the same domain.
5. Record the equality caveat: factorization alone gives an upper bound.
6. Add executable operational codebook and closed-factorization certificates.

### Remaining obligations

1. Complete the closest-literature check before promoting the codebook statement
   itself as novel.
2. Decide whether coordinate decoders are unnecessarily strong and can be
   replaced by a general pair-separating future-word family.
3. Determine whether a converse can identify a sharp combinatorial invariant in
   a delimited model class.

## Priority 2 — constrained sharpness and composition code rate

The next question is not merely whether a non-product example exists. It is
whether linear inflation survives **strong global constraints** on admissible
compositions.

### Parity code

The smallest strict weakening is

\[
C_m=\{x\in\{0,1\}^{m+1}:x_0\oplus x_1\oplus\cdots\oplus x_m=0\}.
\]

Then `|C_m|=2^m`, while every two-coordinate projection `(x_0,x_j)` contains all
four pairs for `m>=2`. Therefore

\[
K_{\mathrm{open}}(D_{C_m})=m,
\qquad
K_{\mathrm{closed},j}(D_{C_m})\le2,
\]

and

\[
\boxed{
K_{\mathrm{open}}-
\max_jK_{\mathrm{closed},j}
\ge m-2
}
\]

on the declared parity-code domain.

### Fixed-richness / fixed-Hamming-weight code

A stronger witness fixes the number of active exterior modules exactly. Let

\[
C_{m,k}
=
\{(y,b_1,\ldots,b_m):y\in\{0,1\},\ b_j\in\{0,1\},\ \sum_jb_j=k\}.
\]

For `1<=k<=m-1`,

\[
|C_{m,k}|=2\binom{m}{k},
\qquad
|\pi_j(C_{m,k})|=4.
\]

With open coordinate decoders and closed decoders for `(y,b_j)`, the restricted
quotients satisfy exactly

\[
K_{\mathrm{open}}(D_{C_{m,k}})
=
1+\log_2\binom{m}{k},
\]

\[
K_{\mathrm{closed},j}(D_{C_{m,k}})=2,
\]

so

\[
\boxed{
\Delta_{m,k}
=
\log_2\binom{m}{k}-1.
}
\]

For `k=floor(rho m)` with fixed `0<rho<1`,

\[
\Delta_{m,k}
=
m h_2(\rho)-\frac12\log_2m+O(1).
\]

At half occupancy the slope approaches one:

\[
\Delta_{m,\lfloor m/2\rfloor}
=
m-\frac12\log_2m+O(1).
\]

Thus almost the full Cartesian linear gap survives under an exact fixed-richness
constraint.

### Bounded-degree inheritance

The existing degree-three relay tree realizes every binary coordinate macrostate
with the same constant local node/message grammar. Restricting the admissible
quiescent macrostates to the fixed-weight codebook changes neither topology nor
local dynamics. Each sequential port read still exposes its memory bit and
preserves the exterior memory vector.

The constrained codebook therefore inherits the bounded-degree locality witness.
The number of selectable ports still grows with `m`.

## Priority 3 — identify the true combinatorial quantity

The codebook theorem suggests that raw module count and full independence are not
fundamental. A natural zero-order quantity is

\[
\Delta_0(C)
=
\log_2|C|-\max_j\log_2|\pi_j(C)|.
\]

For a family `C_m`, define the code rate

\[
R_0
=
\liminf_{m\to\infty}\frac{1}{m}\log_2|C_m|.
\]

If the largest closed factor alphabet has subexponential size,

\[
\log_2 B_m=o(m),
\]

then the codebook corollary gives

\[
\liminf_{m\to\infty}\frac{\Delta_m}{m}\ge R_0.
\]

This supports the interpretation that **positive combinatorial rate of
future-distinguishable composition identities is sufficient for linear interface
inflation**.

Do not yet claim that `Delta_0` or `R_0` is necessary. The next mathematical
question is whether an explicitly delimited grammar class admits a converse.

## Priority 4 — novelty gate for the strengthened theorem

Before the strengthened theorem becomes a headline claim, compare it with:

1. Myhill--Nerode and finite-state distinguishability lower bounds;
2. fooling sets and separating families;
3. communication-complexity rectangle/fooling-set methods;
4. coding-theoretic constrained code families;
5. interface automata and compositional control abstraction; and
6. causal/compositional abstraction.

The likely novelty, if it survives, is **not** pairwise distinguishability of a
state set by itself. The defensible target remains the cross-grammar statement:
small exact quotients in every declared closed context can coexist with a large
open quotient, and this separation persists under bounded locality and strong
composition constraints.

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
