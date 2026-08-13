# Retention–update tradeoff for approximate open portability — 2026-08-13

> **Status:** information-theoretic coupled-resource theorem for reopening/adaptation. The proof uses standard Fano and entropy chain-rule inequalities; those ingredients are not novelty claims. The CCOC-specific role is to split the information required by a later open grammar between what a closed representation retained in advance and what must be supplied after opening.

## 1. Setting

Let

\[
E=(E_1,\ldots,E_m)
\]

be `m` independent uniform binary exterior coordinates.

A representation is formed in two stages.

1. **Closed retention:** before the expanded open grammar is available, retain a random representation `C` of the microstate.
2. **Reopening update:** after opening, supply an additional random update `U`.

No independence between `C`, `U`, and `E` is assumed. The update may depend on the exterior state and on the retained representation.

Suppose that from `(C,U)` there is, for each coordinate `j`, a decoder

\[
\widehat E_j=g_j(C,U)
\]

with error probability

\[
\Pr[\widehat E_j\ne E_j]\le\varepsilon_j,
\qquad
0\le\varepsilon_j\le\tfrac12.
\]

This is the information contract induced when the later open grammar makes the exterior coordinates approximately addressable.

## 2. Theorem — retained information plus update information

### Theorem

Every such representation satisfies

\[
\boxed{
I(E;C)+H(U\mid C)
\ge
m-\sum_{j=1}^m h_2(\varepsilon_j).
}
\]

If all coordinate errors are bounded by one common `eps<=1/2`, then

\[
\boxed{
I(E;C)+H(U\mid C)
\ge
m\bigl(1-h_2(\varepsilon)\bigr).
}
\]

### Proof

For each binary coordinate, Fano's inequality gives

\[
H(E_j\mid C,U)
\le
h_2(\varepsilon_j).
\]

Conditional entropy is subadditive, so

\[
H(E\mid C,U)
\le
\sum_{j=1}^m H(E_j\mid C,U)
\le
\sum_{j=1}^m h_2(\varepsilon_j).
\]

Because `E` is the uniform binary product,

\[
H(E)=m.
\]

Therefore

\[
I(E;C,U)
=H(E)-H(E\mid C,U)
\ge
m-\sum_j h_2(\varepsilon_j).
\]

By the mutual-information chain rule,

\[
I(E;C,U)
=I(E;C)+I(E;U\mid C).
\]

Finally,

\[
I(E;U\mid C)\le H(U\mid C),
\]

which proves the first inequality.

For a common error ceiling, `h2` is monotone on `[0,1/2]`, so

\[
\sum_j h_2(\varepsilon_j)
\le
m h_2(\varepsilon).
\]

This proves the uniform-error form. `□`

## 3. Update lower bound after a bounded closed representation

Rearranging gives the direct adaptation cost

\[
\boxed{
H(U\mid C)
\ge
m-\sum_j h_2(\varepsilon_j)-I(E;C).
}
\]

Since entropy is nonnegative, the operational statement is

\[
H(U\mid C)
\ge
\max\left\{0,
 m-\sum_j h_2(\varepsilon_j)-I(E;C)
\right\}.
\]

If the closed representation has at most `2^k` states, then

\[
I(E;C)\le H(C)\le k,
\]

and hence

\[
\boxed{
H(U\mid C)
\ge
\max\left\{0,
 m-\sum_j h_2(\varepsilon_j)-k
\right\}.
}
\]

For a common error tolerance,

\[
\boxed{
H(U\mid C)
\ge
\max\{0,
 m(1-h_2(\varepsilon))-k
\}.
}
\]

If the update itself has at most `2^b` possible messages, then

\[
H(U\mid C)\le H(U)\le b,
\]

so a simple state-capacity corollary is

\[
\boxed{
k+b\ge m(1-h_2(\varepsilon)).}
\]

This is a portability allocation rule: one can pay in advance by retaining exterior information, or later by transmitting/admitting an update, but the combined information budget cannot fall below the addressability requirement.

## 4. Exact case and sharp Pareto frontier

At zero error,

\[
h_2(0)=0,
\]

so

\[
\boxed{I(E;C)+H(U\mid C)\ge m.}
\]

This bound is sharp at **every** allocation point.

Fix any integer

\[
0\le k\le m.
\]

Let the closed representation retain exactly the first `k` exterior bits,

\[
C=(E_1,\ldots,E_k),
\]

and let the reopening update contain exactly the remaining bits,

\[
U=(E_{k+1},\ldots,E_m).
\]

Then

\[
I(E;C)=H(C)=k,
\]

and, because the exterior product is independent and uniform,

\[
H(U\mid C)=m-k.
\]

Every exterior coordinate is recovered exactly from `(C,U)`, and

\[
I(E;C)+H(U\mid C)=m.
\]

Thus the exact frontier

\[
\boxed{(k,m-k),\qquad k=0,\ldots,m}
\]

is fully achievable. There is no hidden slack in the inequality for exact recovery.

## 5. Approximate equality example

For two exterior bits, let `C` be constant. Let

\[
U=E_1.
\]

Decode `E_1` exactly and always guess zero for `E_2`. Then

\[
\varepsilon_1=0,
\qquad
\varepsilon_2=\tfrac12.
\]

The required-information lower bound is

\[
2-h_2(0)-h_2(1/2)=1.
\]

Meanwhile

\[
I(E;C)=0,
\qquad
H(U\mid C)=1.
\]

Hence this approximate point also attains equality.

## 6. CCOC relay corollary

In the fixed-regular extremal relay, conditional on the focal/inside bit, the canonical closed response interface retains **no information** about the `m` exterior memory bits: the closed all-word invariant makes every exterior vector response-equivalent.

Thus for the exterior coordinates

\[
I(E;C)=0.
\]

If one insists on using that closed representation and only repairs it after opening through an update `U`, while requiring every newly addressable exterior bit to be decoded with error at most `eps`, then

\[
\boxed{
H(U\mid C)
\ge
m(1-h_2(\varepsilon)).
}
\]

and at zero error

\[
\boxed{H(U\mid C)\ge m.}
\]

So the relay's `m`-bit interface inflation can be read equivalently as an **adaptation debt**: exact closed compression removed all dormant exterior information, and once `fire` makes those coordinates addressable, any post-opening repair must restore `m` bits of information somewhere.

This does not mean the relay literally transmits an `m`-bit update message during one physical action. `U` is an abstract adaptation resource describing information added to the retained representation. Local communication/latency constraints are separate and remain governed by the relay/causal-cone results.

## 7. Why this is different from the existing Fano companion

`approximate_addressability.py` lower-bounds the information required in the **final** summary once approximate coordinate recovery is demanded.

The present theorem decomposes that final information burden into two portability resources:

\[
\boxed{
\text{information retained before opening}
+
\text{information added after opening}.
}
\]

This answers a different question: how much can a deliberately over-informative closed representation buy down the cost of adapting to a later open grammar, and how much update is unavoidable if the closed compression discarded exterior distinctions?

The final Fano lower bound is an input to the argument, but the retention/update allocation and its sharp exact frontier are the portability statement.

## 8. Finite executable certificate

`causal_model.portability_adaptation_tradeoff` treats deterministic `C` and `U` over the full uniform binary exterior product. It computes exactly:

- `H(C)=I(E;C)`;
- `H(U|C)=H(C,U)-H(C)`;
- empirical coordinate decoder errors;
- empirical and contract Fano lower bounds;
- minimum update entropy implied by the declared error contract;
- the minimum update-state count implied by that entropy lower bound.

`exact_retention_update_frontier(m,k)` realizes the exact equality point `(k,m-k)` for every `k`.

## 9. Scope and novelty discipline

Do not claim novelty for Fano's inequality, entropy subadditivity, mutual-information chain rules, or the elementary exact bit split. The CCOC value is the coupled portability interpretation and its explicit connection to cross-grammar compression: **information discarded under a closed future contract becomes either pre-retention cost or reopening adaptation cost once future addressability expands.**

The theorem does not yet impose local communication topology, update latency, stochastic plant dynamics, or changing semantic domains. Those are separate possible strengthenings.