# Budgeted depletion: disturbance budget determines exact abundance memory

> **Status:** exact grammar-aware ecological theorem interpolating between irreversible saturation and fully revealing abundance.

Take one guild with abundance \(N\in\{0,\ldots,M\}\), threshold response

\[
Y(N)=\min\{L,N\},
\]

colonization \(N\mapsto\min(M,N+1)\), and depletion \(N\mapsto\max(0,N-1)\). The future grammar permits at most \(D\) depletion actions and tracks how many have already been used. Assume \(M\ge L+D\).

## Exact grammar-adaptive cap

At grammar state `u`, let the remaining depletion budget be

\[
d=D-u.
\]

Define

\[
\boxed{Z_u(N)=\min\{L+d,N\}.}
\]

Then `(u,Z_u(N))` is an exact grammar-aware dynamic interface.

For colonization, the grammar state does not change and

\[
Z_u(N+1)=\min\{L+d,Z_u(N)+1\}.
\]

For depletion, the remaining budget decreases from `d` to `d-1`. If the old cap is unsaturated then it equals the actual abundance and can be decremented directly. If the old cap equals `L+d`, the actual abundance is at least `L+d`, so after one depletion the new cap is exactly `L+d-1`. Thus in both cases

\[
Z_{u+1}(N-1)
=
\min\{L+d-1,\max(0,Z_u(N)-1)\}.
\]

Equal `(u,Z)` labels therefore have equal current output, equal legal-action rows, and equal successor labels. The grammar-aware exact-interface theorem gives exactness for every legal future word.

## Sharp initial interface

At the initial grammar state \(u=0\), the cap is `L+D`, so there are at most

\[
L+D+1
\]

classes. This is exact. For any

\[
0\le n_1<n_2\le L+D,
\]

states with different current threshold outputs are already separated. Otherwise both are at least `L`; applying

\[
\mathsf{deplete}^{n_1-L+1}
\]

uses at most `D` depletions and sends the first state to `L-1` while the second remains at least `L`. Hence every pair inside `0,...,L+D` is future-distinguishable.

Therefore

\[
\boxed{|P_{\rm initial}|=L+D+1,}
\]

and

\[
\boxed{K_D=\log_2(L+D+1).}
\]

Relative to the irreversible `D=0` blanket,

\[
\boxed{
\Delta K_D
=
\log_2\frac{L+D+1}{L+1}.
}
\]

## Full product quotient

At grammar state `u`, the remaining budget is `D-u`, giving exactly

\[
L+D-u+1
\]

abundance classes. Different grammar states are future-distinct because they permit different remaining depletion depths. Thus

\[
\boxed{
|P_{X\times Q}|
=
\sum_{u=0}^{D}(L+D-u+1)
=
\sum_{d=0}^{D}(L+d+1).
}
\]

The executable certificate verifies both this count and the initial-slice count against the canonical grammar-aware quotient.

## Interpolation

The theorem gives a quantitative continuum:

\[
D=0
\quad\Rightarrow\quad
|P_{\rm initial}|=L+1,
\]

while every additional allowed future depletion adds exactly one initial abundance class,

\[
L+1,L+2,\ldots,L+D+1.
\]

If

\[
D=M-L,
\]

then

\[
L+D+1=M+1,
\]

so the initial exact interface is the full abundance state. Enough legal downward motion eliminates all saturation compression.

The ecological rule is therefore

\[
\boxed{
\text{needed abundance cap}
=
\text{response threshold}
+
\text{maximum future downward reach}.
}
\]

A threshold can hide excess abundance only to the extent that the declared future grammar cannot drive that excess back through the response-sensitive threshold.

## Capacity-family consequence

For fixed `L` and fixed disturbance budget `D`, the bound `L+D+1` is independent of carrying capacity for every `M>=L+D`. If `D` itself grows with `M`, for example `D=M-L`, the exact interface grows as `M+1` and system-size-independent portability disappears.

Thus changing habitat capacity is harmless to the saturated macro law only when future downward reach remains uniformly bounded.

## Claim discipline

Bounded-counter grammars, threshold distinguishability, and finite-state minimization are classical substrate. The CCOC-specific content is the ecological portability law: the declared future disturbance budget quantitatively controls how much hidden oversaturation must be retained in an exact causal boundary.
