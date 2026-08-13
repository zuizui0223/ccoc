# Retention–boundary–time tradeoff for open-interface materialization

## Setting

Let \(E=(E_1,\ldots,E_m)\) be independent uniform binary exterior coordinates. Before the open contract is activated, an inside representation retains a random variable \(C\). After activation, information may enter the inside through a declared synchronous boundary.

Assume the boundary has width \(c\). In each of \(T\) rounds, every boundary location can contribute one symbol from an alphabet of size \(s\). Let \(U\) denote the complete inward boundary-symbol history. From \((C,U)\), coordinate \(E_j\) must be decoded with error at most \(\varepsilon_j\le 1/2\).

This is a **full materialization** contract: after the update, one retained state must support all declared coordinate decoders. It is not the latency of one coordinate-specific query.

## Theorem

The resources satisfy

\[
\boxed{
I(E;C)+cT\log_2 s
\ge
m-\sum_{j=1}^m h_2(\varepsilon_j).
}
\]

If all errors are at most one common \(\varepsilon\), then

\[
\boxed{
I(E;C)+cT\log_2 s
\ge
m\bigl(1-h_2(\varepsilon)\bigr).
}
\]

### Proof

The retention–update theorem already gives

\[
I(E;C)+H(U\mid C)
\ge
m-\sum_j h_2(\varepsilon_j).
\]

A length-\(T\) synchronous boundary history contains \(cT\) symbols, each with at most \(s\) values. Therefore, even if the symbols are chosen adaptively using all available history,

\[
H(U\mid C)\le H(U)\le \log_2 s^{cT}=cT\log_2s.
\]

Substitution proves the result. The common-error form follows from monotonicity of binary entropy on \([0,1/2]\). \(\square\)

## Bounded closed state corollary

If the closed representation has at most \(2^k\) possible states, then

\[
I(E;C)\le H(C)\le k,
\]

hence

\[
\boxed{k+cT\log_2s\ge m(1-h_2(\varepsilon)).}
\]

Thus

\[
\boxed{
T\ge
\left\lceil
\frac{\max\{0,m(1-h_2(\varepsilon))-k\}}
{c\log_2s}
\right\rceil.
}
\]

At zero error,

\[
\boxed{k+cT\log_2s\ge m.}
\]

## Average-error floor

The theorem also gives a direct accuracy limit when the retention and boundary-time budgets are fixed. Define the mean coordinate error

\[
\bar\varepsilon=\frac1m\sum_{j=1}^m\varepsilon_j.
\]

Binary entropy is concave, so Jensen's inequality gives

\[
\frac1m\sum_j h_2(\varepsilon_j)
\le h_2(\bar\varepsilon).
\]

Therefore a closed representation with at most \(2^k\) states must satisfy

\[
\boxed{
k+cT\log_2s\ge m\bigl(1-h_2(\bar\varepsilon)\bigr).}
\]

Let

\[
B=\frac{k+cT\log_2s}{m}.
\]

When \(B<1\), monotonicity of \(h_2\) on \([0,1/2]\) implies the error floor

\[
\boxed{
\bar\varepsilon
\ge
h_2^{-1}(1-B).
}
\]

When \(B\ge1\), this information bound alone imposes no positive error floor. This inversion is a resource feasibility statement; no finite-block claim of sharpness is made for the approximate case.

## Sharpness for power-of-two boundary alphabets

Let \(s=2^b\). For any \(0\le k\le m\), retain the first \(k\) exterior bits in \(C\). Send the remaining \(m-k\) bits across the \(c\) boundary locations, packing \(b\) bits into each symbol. This needs

\[
T=\left\lceil\frac{m-k}{cb}\right\rceil
\]

rounds. Padding unused slots in the final round does not change the carried information. Hence the integer round lower bound is attained for every retention split.

The exact information frontier and the exact round frontier are therefore both sharp for power-of-two symbol alphabets.

## Fixed-regular relay corollary

In the fixed-regular extremal relay, the canonical closed interface retains the focal bit but no information about the \(m\) exterior coordinates. For the exterior vector \(E\), therefore \(I(E;C)=0\).

The focal node is attached to the exterior relay body through one edge, so the focal/exterior cut width is \(c=1\). The relay pulse alphabet is \(\{\mathrm{empty},0,1\}\), of size \(s=3\). Any synchronous protocol using that same focal cut and symbol alphabet that **materializes an exact reusable focal representation of all \(m\) exterior coordinates** must therefore satisfy

\[
\boxed{
T_{\rm full}\ge\left\lceil\frac{m}{\log_2 3}\right\rceil.
}
\]

This does not contradict the existing addressed-query result. An addressed query asks for one selected coordinate and returns one bit. Full materialization requires enough boundary information to support all coordinate decoders simultaneously.

The fixed-regular construction has exact worst canonical selected-query length

\[
T_{\rm query}=2\lceil\log_2m\rceil+2.
\]

Consequently

\[
\boxed{
\frac{T_{\rm full}}{T_{\rm query}}
\ge
\frac{\lceil m/\log_2 3\rceil}
{2\lceil\log_2m\rceil+2}
=
\Omega\!\left(\frac{m}{\log m}\right).
}
\]

Thus the same bounded-degree, cut-one family exhibits a diverging separation between two operational tasks:

- selected-coordinate random access: \(\Theta(\log m)\);
- exact full-interface installation across the focal cut: \(\Omega(m)\).

A narrow boundary can therefore support fast targeted interrogation while still making wholesale installation of the open causal interface asymptotically much slower.

## Claim discipline

The entropy bound for a finite alphabet channel, Fano's inequality, Jensen's inequality, and the chain rule are classical substrate. The CCOC-specific contribution here is the coupled portability interpretation and its application to the same extremal family: information omitted by closed compression becomes a reopening debt, a narrow boundary turns that debt into an installation-time lower bound, and targeted random access can remain exponentially faster in state-space terms than full interface materialization.
