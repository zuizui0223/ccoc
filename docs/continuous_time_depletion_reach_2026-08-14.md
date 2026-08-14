# Continuous-time rare-disturbance reach under saturated response

> **Status:** continuous-time corollary of the stochastic ecological portability boundary. The Poisson-process calculation is classical; the CCOC role is to separate exact causal relevance from finite-horizon approximate detectability when depletion is rare.

## 1. Setting

Take one guild with abundance

\[
N\in\{0,\ldots,M\},
\qquad 1\le L<M,
\]

and response

\[
Y(N)=\min\{L,N\}.
\]

Closed dynamics preserve the saturated fiber. After opening, admit a one-unit pure-depletion mechanism with rate

\[
\mu\ge0.
\]

While abundance is positive, depletion events arrive according to a rate-`mu` clock. Let `D_t` denote the number of potential depletion events by time `t`; before the relevant threshold is crossed its count law is Poisson with mean

\[
\lambda=\mu t.
\]

## 2. Exact class-count discontinuity at zero rate

If `mu=0`, the newly admitted depletion mechanism never fires. Hidden oversaturation remains unreachable, so the exact abundance interface remains the saturated one:

\[
\boxed{|P_{\mu=0}|=L+1.}
\]

For every `mu>0`, take two saturated initial states

\[
L\le n_1<n_2\le M.
\]

The response falls below `L` once at least

\[
k_i=n_i-L+1
\]

depletion events have occurred. Hence at any horizon `t>0`,

\[
\Pr_{n_1}(Y_t<L)-\Pr_{n_2}(Y_t<L)
=
\Pr(k_1\le D_t<k_2).
\]

For `mu>0` and `t>0`, every finite Poisson count has positive probability, so

\[
\Pr(k_1\le D_t<k_2)>0.
\]

Thus every pair of saturated abundance states has different finite-time response laws. States below `L` already differ at time zero. Therefore

\[
\boxed{|P_{\mu>0}|=M+1.}
\]

The exact interface complexity is discontinuous at zero disturbance rate:

\[
\boxed{
K_{\rm exact}(\mu)=
\begin{cases}
\log_2(L+1), & \mu=0,\\
\log_2(M+1), & \mu>0.
\end{cases}}
\]

This is the continuous-time analogue of the discrete stochastic result that every depletion probability `p>0` restores full exact abundance distinguishability.

## 3. Threshold pair and finite-horizon approximate separation

For the nearest hidden pair `N=L` and `N=L+1`, the relevant event-count thresholds are one and two. Therefore

\[
\Pr_L(Y_t<L)-\Pr_{L+1}(Y_t<L)
=
\Pr(D_t=1)
=
\boxed{\lambda e^{-\lambda}},
\qquad \lambda=\mu t.
\]

This event-probability difference is a lower bound on the total-variation distance between the full final-output laws.

Any one approximate final-output law used to represent both initial states must therefore incur worst-case TV error at least

\[
\boxed{\frac12\lambda e^{-\lambda}}.
\]

The function `lambda exp(-lambda)` is maximized at

\[
\lambda=1,
\]

so the maximizing horizon is

\[
\boxed{t^*=1/\mu}
\]

and the event gap is

\[
\boxed{1/e}.
\]

Thus a rare disturbance rate does not remove approximate distinguishability; it shifts the informative observation horizon. If `mu` is divided by a factor `a`, the same dimensionless separation is recovered by multiplying the horizon by `a`.

## 4. Exact versus approximate interpretation

The result exposes two different limits.

### Exact interface

Any `mu>0`, however small, makes hidden oversaturation future-relevant because some finite-horizon response event has different probability. Exact state complexity therefore jumps immediately from `L+1` to `M+1`.

### Fixed observation horizon

For fixed `t` and small `mu`,

\[
\mu t e^{-\mu t}\sim \mu t,
\]

so the immediate statistical separation is small.

### Rate-adapted horizon

At `t=1/mu`, the same threshold pair has event gap `1/e`, independent of how small `mu` is.

Hence exact causal relevance, fixed-horizon detectability, and rate-adapted detectability are distinct quantities. CCOC should not use one as a proxy for the others.

## 5. Ecological reading

If extinction, mortality, harvest, disturbance, or emigration is genuinely impossible, oversaturation beyond the response threshold can remain causally irrelevant under the saturation theorem.

If such downward events occur at any positive rate, exact future response laws retain information about how far above threshold abundance lies. But whether that information is practically detectable depends on the observation horizon relative to the disturbance time scale.

This gives a concrete stochastic refinement of the deterministic disturbance-budget theorem:

- deterministic budget controls the **maximum downward reach**;
- stochastic rate controls the **time scale on which downward reach becomes observable**;
- exact interface complexity responds to whether the reach has positive probability at all.

## 6. Claim discipline

Poisson event counts, pure-death processes, and total-variation lower bounds are classical. The CCOC-specific value is the portability interpretation: a disturbance mechanism can be arbitrarily rare and still be structurally decisive for exact causal compression, while approximate distinguishability scales with the dimensionless horizon `mu*t`.
