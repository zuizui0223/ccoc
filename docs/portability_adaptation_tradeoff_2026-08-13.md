# Retention–update tradeoff for approximate open portability — 2026-08-13

> **Status:** information-theoretic coupled-resource theorem for reopening/adaptation. The strongest form is a mutual-information statement and therefore already allows stochastic updates. Fano and information chain rules are classical substrate.

## 1. Setting

Let

\[
E=(E_1,\ldots,E_m)
\]

be `m` independent uniform binary exterior coordinates. Before opening, retain a random representation `C`. After opening, obtain an additional random update/observation `U`. No determinism or independence between `C`, `U`, and `E` is assumed.

Suppose each coordinate is decoded from `(C,U)` with

\[
\Pr[\widehat E_j\ne E_j]\le\varepsilon_j,
\qquad 0\le\varepsilon_j\le\tfrac12.
\]

## 2. Strong theorem — retained information plus acquired information

Every such representation satisfies

\[
\boxed{
I(E;C)+I(E;U\mid C)
\ge
m-\sum_{j=1}^m h_2(\varepsilon_j).
}
\]

Equivalently,

\[
\boxed{
I(E;C,U)
\ge
m-\sum_j h_2(\varepsilon_j).
}
\]

### Proof

Coordinate-wise Fano gives

\[
H(E_j\mid C,U)\le h_2(\varepsilon_j).
\]

Conditional entropy is subadditive, so

\[
H(E\mid C,U)
\le\sum_j h_2(\varepsilon_j).
\]

Because `E` is a uniform binary product, `H(E)=m`. Therefore

\[
I(E;C,U)
=H(E)-H(E\mid C,U)
\ge m-\sum_j h_2(\varepsilon_j).
\]

The mutual-information chain rule gives

\[
I(E;C,U)=I(E;C)+I(E;U\mid C),
\]

which proves the theorem. \(\square\)

This is stronger than the previously emphasized entropy form because

\[
I(E;U\mid C)\le H(U\mid C).
\]

Hence

\[
\boxed{
I(E;C)+H(U\mid C)
\ge
m-\sum_jh_2(\varepsilon_j)
}
\]

remains as a direct corollary.

For one common error ceiling `eps<=1/2`, both forms imply

\[
I(E;C)+I(E;U\mid C)
\ge m(1-h_2(\varepsilon)).
\]

## 3. Stochastic information-flow budget

The strong form immediately handles noisy or randomized adaptation. Suppose a declared post-opening mechanism guarantees only that the new observation can carry at most

\[
I(E;U\mid C)\le B
\]

bits of exterior information beyond what was already retained. Then necessarily

\[
\boxed{
I(E;C)+B
\ge
m-\sum_jh_2(\varepsilon_j).
}
\]

If the closed representation has at most `2^k` states, then `I(E;C)<=H(C)<=k`, so

\[
\boxed{
k+B\ge m(1-h_2(\varepsilon)).}
\]

No finite-alphabet, deterministic-update, or noiseless-channel assumption is needed for this formulation. `B` is simply an upper bound on **new exterior information acquired after opening**.

## 4. Sequential stochastic updates

Let reopening information arrive in stages

\[
U_1,U_2,\ldots,U_T.
\]

The chain rule gives

\[
I(E;U_1,\ldots,U_T\mid C)
=
\sum_{t=1}^{T}
I(E;U_t\mid C,U_1,\ldots,U_{t-1}).
\]

Therefore if each stage has a declared information-flow budget

\[
I(E;U_t\mid C,U_{<t})\le B_t,
\]

then approximate full materialization requires

\[
\boxed{
I(E;C)+\sum_{t=1}^{T}B_t
\ge
m-\sum_jh_2(\varepsilon_j).
}
\]

This is the stochastic information-flow version of the later finite-boundary theorem. A deterministic boundary with `c` locations, `s` symbols per location, and `T` synchronous rounds is recovered by using the crude capacity bound `sum B_t <= cT log2(s)`.

## 5. Exact case and sharp retention/update frontier

At zero error,

\[
\boxed{I(E;C)+I(E;U\mid C)\ge m.}
\]

For deterministic `C` and `U`, the bound is sharp at every integer split. Fix `0<=k<=m`, retain

\[
C=(E_1,\ldots,E_k),
\]

and use

\[
U=(E_{k+1},\ldots,E_m).
\]

Then

\[
I(E;C)=k,
\qquad
I(E;U\mid C)=H(U\mid C)=m-k,
\]

so equality holds. The exact frontier

\[
\boxed{(k,m-k),\qquad k=0,\ldots,m}
\]

is therefore fully achievable.

## 6. Approximate equality example

For two exterior bits, take `C` constant and `U=E_1`. Decode `E_1` exactly and always guess zero for `E_2`. Then

\[
(\varepsilon_1,\varepsilon_2)=(0,1/2),
\]

and the required-information bound is one bit. Meanwhile

\[
I(E;C)=0,
\qquad
I(E;U\mid C)=1,
\]

so the strong information-flow inequality is attained exactly.

## 7. Fixed-regular relay corollary

For the exterior coordinates of the fixed-regular extremal relay, the canonical closed interface retains no exterior information:

\[
I(E;C)=0.
\]

Thus any post-opening observation/update that makes every exterior bit approximately recoverable must supply

\[
\boxed{
I(E;U\mid C)
\ge
m(1-h_2(\varepsilon)).
}
\]

bits of **new exterior information**. At zero error,

\[
\boxed{I(E;U\mid C)\ge m.}
\]

The earlier entropy statement `H(U|C)>=m` follows immediately. The mutual-information form is conceptually cleaner: the adaptation debt is not message length per se, but how much exterior information the reopened system must newly acquire.

`docs/retention_boundary_time_tradeoff_2026-08-14.md` then converts this information debt into a boundary-time lower bound when a concrete finite synchronous boundary is imposed.

## 8. Relation to the executable finite certificate

`causal_model.portability_adaptation_tradeoff` treats deterministic `C` and `U` over the full uniform binary exterior product. In that finite subclass,

\[
I(E;C)=H(C),
\qquad
I(E;U\mid C)=H(U\mid C),
\]

so the existing certificate already measures the strong theorem exactly even though its public property names use entropy language.

`exact_retention_update_frontier(m,k)` realizes every exact equality point.

## 9. Claim discipline

Do not claim novelty for Fano, entropy subadditivity, mutual-information chain rules, channel-capacity reasoning, or the elementary exact bit split. The CCOC-specific content is the portability allocation: **information discarded under a closed future contract becomes an information-acquisition debt after the grammar opens.**

The strong mutual-information form supplies the correct interface to stochastic/noisy adaptation models; separate model-specific work is still required to upper-bound the information flow `B` generated by any particular stochastic ecological or communication mechanism.
