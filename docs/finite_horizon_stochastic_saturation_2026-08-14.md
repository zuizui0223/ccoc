# Finite-horizon approximate portability under stochastic depletion

> **Status:** positive approximate/stochastic ecological portability theorem. Exact response complexity can grow with abundance capacity as soon as downward events have positive rate, yet one capacity-independent saturated macro remains accurate over a finite horizon. The probability calculations are classical; the CCOC contribution is the portability interpretation across changing capacities and the explicit exact/approximate separation.

## 1. Approximate macro contract

Take one guild with abundance

\[
N\in\{0,\ldots,M\},
\qquad 1\le L\le M,
\]

and capped response

\[
Y(N)=\min\{L,N\}.
\]

Use the `L+1` macro states

\[
0,1,\ldots,L-1,\mathsf{sat}.
\]

Below threshold, retain abundance exactly. For every saturated microstate `N>=L`, approximate its response path over the finite window `[0,T]` by the constant path that stays at `L`.

For a point-mass approximate path, total variation from the true path law is exactly the probability that the true capped response ever leaves saturation during the window. Therefore a uniform bound on threshold-crossing probability is a finite-horizon approximate portability certificate.

## 2. Constant total depletion clock

Suppose one-unit depletion events arrive according to a constant total rate `mu`, independent of abundance while positive.

Starting from the least saturated state `N=L`, the capped response leaves saturation at the first depletion event. Hence

\[
\Pr_L(\text{leave saturation by }T)
=1-e^{-\mu T}.
\]

Starting from any `N>L`, at least two or more depletion events are required, so the crossing probability is no larger. Thus the worst-case saturated-path TV error is

\[
\boxed{
\varepsilon_T^{\rm const}
=1-e^{-\mu T}.
}
\]

This bound contains no `M`.

## 3. Independent per-capita mortality

Now suppose each individual dies independently at per-capita rate `mu`.

Starting from `N=L`, the response remains saturated throughout `[0,T]` iff all `L` individuals survive to time `T`. Each survives with probability `exp(-mu T)`, so

\[
\Pr_L(\text{stay saturated through }T)
=e^{-\mu LT}.
\]

Therefore

\[
\boxed{
\varepsilon_T^{\rm pc}
=1-e^{-\mu LT}.
}
\]

For `N>L`, the number of survivors at every fixed time is stochastically larger than for `N=L`, and the first threshold-crossing time is stochastically later. Hence the least saturated state is again the worst member of the saturated fiber.

This error bound also contains no carrying capacity `M`.

## 4. Changing-capacity approximate portability

Fix `L`, `mu`, `T`, and one of the two mortality mechanisms. Allow

\[
M^{(q)}\ge L
\]

to vary without bound.

Every system has the same `L+1`-state approximate macro and the same worst-case saturated-path error:

\[
\boxed{
|\mathcal Z_{\rm approx}|=L+1
}
\]

with either

\[
\boxed{\varepsilon_T=1-e^{-\mu T}}
\]

or

\[
\boxed{\varepsilon_T=1-e^{-\mu LT}}.
\]

Thus finite-horizon approximate portability survives across unbounded abundance capacities even though exact stochastic response complexity is

\[
|P_{\rm exact}|=M+1
\]

for every positive mortality/depletion rate in the corresponding exact theorem.

This gives the desired exact/approximate separation:

\[
\boxed{
M+1\ \text{exact states can diverge while}\ L+1\ \text{approximate states and }\varepsilon_T\text{ stay fixed}.}
\]

## 5. Error-tolerance horizon

For a target path-TV tolerance

\[
0\le\varepsilon<1,
\]

the constant-rate mechanism satisfies the target whenever

\[
1-e^{-\mu T}\le\varepsilon,
\]

equivalently

\[
\boxed{
T\le\frac{-\log(1-\varepsilon)}{\mu}.
}
\]

For per-capita mortality,

\[
\boxed{
T\le\frac{-\log(1-\varepsilon)}{\mu L}.
}
\]

At small exposure,

\[
1-e^{-x}\sim x,
\]

so

\[
\varepsilon_T^{\rm const}\sim\mu T,
\qquad
\varepsilon_T^{\rm pc}\sim\mu LT.
\]

The relevant approximation parameter is therefore not mortality rate alone but mortality exposure over the declared future horizon.

## 6. Relation to exact stochastic reach

The exact stochastic theorems ask whether two microstates have **identical** response laws for every legal future. Any positive-probability threshold crossing eventually makes hidden oversaturation relevant, giving `M+1` exact response classes.

The present theorem asks a different question: over one finite horizon, how close is a capacity-independent saturated macro to the true response path?

The answer can remain uniformly good for all `M` whenever the downward exposure is small enough. Therefore

\[
\boxed{
\text{exact non-portability does not imply finite-horizon approximate non-portability}.}
\]

This is the stochastic ecological analogue of the broader CCOC distinction between exact causal structure and finite-evidence identifiability.

## 7. Ecological interpretation

For island/community applications, `M` may represent a maximum guild abundance or number of exchangeable sites, while `L` is a response saturation level. If extinction or mortality is possible but sufficiently rare on the forecasting/decision horizon, exact abundance remains mechanistically relevant but the capped guild macro can still be an accurate finite-horizon predictive interface.

The theorem therefore provides a concrete way to choose the coarse-graining regime from a biological time scale:

- long horizons relative to depletion/mortality time scale demand more exact abundance information;
- short horizons can justify a capacity-independent saturated summary;
- increasing hidden carrying capacity above `L` does not itself worsen the finite-horizon approximation bound.

## 8. Claim discipline

Exponential waiting times, independent survival, coupling/stochastic ordering, and total variation to a point mass are classical. Do not claim novelty for those facts. The CCOC-specific result is the positive portability statement: a fixed finite stochastic macro with an explicit error guarantee can survive across changing ecological system sizes even when exact causal-interface size diverges.
