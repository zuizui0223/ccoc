# Approximate addressability: a Fano robustness bound

> **Status:** post-reopening companion theorem. This is deliberately **not** part of
> the frozen `CORE-1`–`CORE-5` paper facade. Its purpose is to test whether the exact
> extension–compression gap is brittle to small decoding errors. The information-
> theoretic ingredients are classical; no novelty claim is made for Fano's
> inequality, rate-distortion theory, predictive information bottlenecks, or
> approximate state abstraction.

## 1. Question

The exact addressable-codebook theorem says that if every relevant coordinate of a
finite jointly realizable codebook can be recovered by a declared future probe,
then an exact open interface must retain enough states to distinguish every
codeword.

A natural objection is that ecology, control, and learned macrostate models rarely
need **zero** error. If a summary is allowed to misdecode a probe response with a
small probability, can the open-interface memory collapse to `O(1)`?

For a uniform finite codebook, the answer is no when a positive rate of independent
coordinate information remains decodable.

## 2. Approximate summary contract

Let

\[
C\subseteq A_0\times A_1\times\cdots\times A_q
\]

be a finite codebook, and let

\[
X=(X_0,\ldots,X_q)\sim\operatorname{Unif}(C).
\]

A deterministic summary is

\[
Z=\phi(X)
\]

with finite image. For every coordinate `j`, assume there is a decoder

\[
\widehat X_j=d_j(Z)
\]

whose average error satisfies

\[
\Pr[\widehat X_j\neq X_j]\le \varepsilon_j.
\]

Let

\[
k_j=|\{x_j:(x_0,\ldots,x_q)\in C\}|
\]

be the number of values actually realized in coordinate `j` on the codebook.

For the declared tolerance form we restrict

\[
0\le \varepsilon_j\le 1-\frac1{k_j}
\]

when `k_j>1`, so the standard Fano penalty is monotone in the permitted error.
Constant coordinates have zero information cost and use zero declared tolerance in
the finite certificate.

## 3. Theorem: approximate addressability lower bound

Under the contract above,

\[
\boxed{
\log_2|\operatorname{im}\phi|
\ge
\log_2|C|
-
\sum_{j=0}^{q}
\left[
 h_2(\varepsilon_j)
 +
 \varepsilon_j\log_2(k_j-1)
\right]
}
\]

where the second term is interpreted as zero when `k_j=1`, and

\[
h_2(p)=-p\log_2p-(1-p)\log_2(1-p)
\]

is the binary entropy.

If the right-hand side is negative, the effective memory lower bound is simply
zero bits.

### Proof

For each coordinate, Fano's inequality gives

\[
H(X_j\mid Z)
\le
h_2(\varepsilon_j)
+
\varepsilon_j\log_2(k_j-1).
\]

The codeword is determined by its coordinates, so conditional subadditivity gives

\[
H(X\mid Z)
\le
\sum_j H(X_j\mid Z).
\]

Because `X` is uniform on `C`,

\[
H(X)=\log_2|C|.
\]

Because `Z=\phi(X)` is a deterministic summary,

\[
I(X;Z)=H(Z).
\]

Therefore

\[
H(Z)
=
H(X)-H(X\mid Z)
\]

is at least the stated codebook entropy minus the sum of coordinate Fano penalties.
Finally,

\[
H(Z)\le \log_2|\operatorname{im}\phi|,
\]

which proves the claim.

The proof is an information-theoretic robustness argument. It is not a new
minimization principle.

## 4. Binary full-product corollary

Take one binary inside coordinate and `m` binary exterior coordinates:

\[
C=\{0,1\}^{m+1}.
\]

Suppose the inside coordinate is recovered exactly and each exterior coordinate is
recovered with average error at most

\[
0\le\varepsilon\le\frac12.
\]

Then

\[
\boxed{
K_{\mathrm{open}}^{(\varepsilon)}
\ge
1+m\bigl(1-h_2(\varepsilon)\bigr)
}.
\]

For every fixed

\[
\varepsilon<\frac12,
\]

the retained memory remains linear in `m`.

Thus the exact result

\[
K_{\mathrm{open}}=m+1
\]

does not collapse discontinuously as soon as a small fixed decoding error is
allowed.

If each fixed closed context still has a supplied exact two-bit interface, the
corresponding open-versus-closed lower bound is

\[
\boxed{
K_{\mathrm{open}}^{(\varepsilon)}
-
\max_i K_{\mathrm{closed},i}
\ge
m\bigl(1-h_2(\varepsilon)\bigr)-1.
}
\]

This is a robustness corollary, not a replacement for the exact main theorem.

## 5. Equality replay: dropping one binary coordinate

The finite test suite includes a simple equality witness.

Start from the four-bit full codebook

\[
C=\{0,1\}^{4}.
\]

Let the summary retain only the first three coordinates. The first three decoders
are exact; the fourth decoder always returns zero. Under the uniform codebook its
fourth-coordinate error is exactly `1/2`.

The summary has

\[
2^3
\]

states, hence three bits. Fano charges one full bit for the discarded binary
coordinate:

\[
h_2(1/2)=1.
\]

Therefore the lower bound is also exactly three bits. This gives a finite equality
check rather than only evaluating an inequality numerically.

## 6. Constrained codebooks

The theorem does not require a Cartesian product. It only uses the entropy of the
uniform codeword and the realized alphabet size of each coordinate.

For a constrained codebook `C`, the lower bound is

\[
\log_2|C|-\sum_j \text{FanoPenalty}_j.
\]

This makes the approximate theorem compatible with the existing parity and
fixed-richness codebook strengthenings: structural dependence among exterior
coordinates reduces `\log_2|C|`, but a fixed nontrivial coordinate-decoding rate
still forces retained information.

The theorem does **not** assume coordinate independence.

## 7. What the finite certificate verifies

`causal_model/approximate_addressability.py` provides
`ApproximateAddressableCodebookCertificate`.

A certificate receives:

- the complete finite codebook;
- one deterministic summary label for each codeword;
- one decoder for each coordinate;
- one declared average-error tolerance per coordinate.

It exhaustively computes the actual decoder error on the uniform finite codebook,
checks the declared tolerance, evaluates both the empirical and contract Fano
bounds, and verifies that the concrete summary image is large enough to satisfy the
information lower bound.

The certificate does **not** infer:

- a future action grammar;
- a codebook from data;
- which probe should decode which ecological variable;
- a noise distribution beyond the declared uniform codebook replay;
- a stochastic transition model;
- a real-world error rate.

Connecting this theorem to a controlled system requires a separate operational
argument that the approximate summary can decode the responses associated with the
declared future probes.

## 8. Scope and novelty boundary

Approximate state abstraction, predictive compression, information bottlenecks,
and rate-distortion theory are mature areas. Representative adjacent work includes:

- Abel, Hershkowitz & Littman (2016), *Near Optimal Behavior via Approximate State
  Abstraction*;
- Marzen & Crutchfield (2014/2016), causal/predictive rate-distortion analysis;
- predictive information-bottleneck and compressed predictive-state approaches.

Accordingly, manuscript-safe language is:

> The exact CCOC addressability gap has a simple information-theoretic robustness
> extension: if coordinate-specific open responses remain decodable with bounded
> average error, Fano's inequality forces a correspondingly large approximate
> summary. In the binary full-product family, any fixed error below one half leaves
> a linear-in-`m` memory requirement.

Unsafe language includes:

- “we introduce approximate state abstraction”;
- “we derive a new rate-distortion theorem”;
- “Fano's inequality is a CCOC novelty”;
- “this characterizes optimal approximate ecological macrostates.”

## 9. Role in the research program

This result is useful only if it answers a robustness objection to the exact paper:

\[
\boxed{
\text{the open-interface gap is not purely a zero-error artifact.}
}
\]

It should remain a companion strengthening or supplement unless a genuinely new
approximate-composition theorem is later proved. The exact cross-grammar theorem
remains the conceptual spine of the first paper.