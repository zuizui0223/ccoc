# Per-capita mortality makes hidden oversaturation future-relevant

> **Status:** model-specific continuous-time ecological corollary. The independent-survival/binomial law is classical; the CCOC contribution is the exact/approximate portability interpretation for a saturated abundance interface.

## 1. Model

Take one guild with abundance

\[
N_0=n\in\{0,\ldots,M\},
\qquad
Y(n)=\min\{L,n\},
\qquad 1\le L<M.
\]

Suppose every individual dies independently at per-capita rate `mu`. At time `t`, each initial individual survives with probability

\[
q=e^{-\mu t},
\]

so

\[
N_t\mid N_0=n\sim\operatorname{Binomial}(n,q).
\]

This differs from the constant-rate disturbance clock: mortality intensity scales with abundance, making it a more familiar ecological birth-death mechanism.

## 2. Exact interface discontinuity

If `mu=0`, no death occurs and all abundances `n>=L` remain response-equivalent under the saturated output. Thus

\[
|P_{\mu=0}|=L+1.
\]

If `mu>0`, then for any finite `t>0`,

\[
0<q<1.
\]

The probability that all individuals have died by time `t` is

\[
\Pr_n(Y_t=0)=(1-q)^n.
\]

For distinct positive abundances `n_1<n_2`,

\[
(1-q)^{n_1}>(1-q)^{n_2}.
\]

Hence every distinct abundance produces a different finite-time response law. States below `L` were already separated by their current output, so

\[
\boxed{|P_{\mu>0}|=M+1.}
\]

Thus per-capita mortality has the same exact zero-rate discontinuity as the constant-rate disturbance model:

\[
\boxed{
K_{\rm exact}(\mu)=
\begin{cases}
\log_2(L+1),&\mu=0,\\
\log_2(M+1),&\mu>0.
\end{cases}}
\]

## 3. Threshold-pair finite-horizon gap

Now compare `N_0=L` and `N_0=L+1`. The response is below threshold at time `t` iff fewer than `L` individuals survive.

For `L` initial individuals,

\[
\Pr_L(Y_t<L)=1-q^L.
\]

For `L+1` initial individuals,

\[
\Pr_{L+1}(Y_t<L)
=1-(L+1)q^L(1-q)-q^{L+1}.
\]

Subtracting gives

\[
\boxed{
\Delta_L(q)
=Lq^L(1-q).
}
\]

This event-probability gap lower-bounds the total-variation distance between the two final-output laws. Therefore any one approximate output law representing both states incurs worst-case TV error at least

\[
\boxed{\frac12Lq^L(1-q).}
\]

## 4. Rate-adapted informative horizon

Maximize

\[
f(q)=Lq^L(1-q),\qquad 0<q<1.
\]

Differentiation gives

\[
f'(q)=Lq^{L-1}\bigl(L-(L+1)q\bigr),
\]

so the maximum occurs at

\[
\boxed{q^*=\frac{L}{L+1}.}
\]

Because `q=exp(-mu t)`, the maximizing horizon is

\[
\boxed{
t^*
=\frac{1}{\mu}\log\frac{L+1}{L}.
}
\]

The maximal threshold-pair event gap is

\[
\boxed{
\Delta_L^*
=\left(\frac{L}{L+1}\right)^{L+1}.
}
\]

As the saturation threshold increases,

\[
\Delta_L^*\longrightarrow e^{-1}.
\]

Thus a small mortality rate shifts the informative horizon by the factor `1/mu` but does not force the best achievable finite-horizon separation to vanish.

For large `L`,

\[
t^*\sim\frac{1}{\mu L},
\]

reflecting the faster total death hazard when many individuals are present.

## 5. Relation to the constant-rate disturbance corollary

The constant-rate pure-depletion model gives threshold gap

\[
\lambda e^{-\lambda},\qquad \lambda=\mu t,
\]

with maximum `1/e` at `t=1/mu`.

The per-capita model gives

\[
Lq^L(1-q)
\]

with maximum

\[
(L/(L+1))^{L+1},
\]

which tends to the same `1/e` scale as `L` grows.

The detailed time scale changes because the mortality mechanism changes, but the CCOC conclusion is stable:

- exact compression distinguishes `mu=0` from every `mu>0`;
- fixed-horizon approximate separation can be weak when rates are small;
- rate-adapted horizons recover order-one separation.

## 6. Ecological interpretation

The deterministic disturbance-budget theorem asked how far the future grammar can drive abundance downward. The stochastic rate theorems add a second axis: **how long it takes that reach to become statistically expressed**.

A saturated abundance summary is therefore protected only when downward reach is absent, not merely rare. If mortality/extinction has positive rate, hidden oversaturation remains part of the exact causal state, although finite observation windows may make those distinctions hard to detect.

This matters for ecological coarse-graining because exact mechanistic portability and practical finite-window identifiability are different questions.

## 7. Claim discipline

Independent exponential lifetimes, binomial survival, and threshold probabilities are classical. Do not present their derivation as novel. The CCOC-specific point is the structural mapping from an explicit ecological mortality mechanism to exact interface failure and a quantitative rate-dependent observation horizon.
