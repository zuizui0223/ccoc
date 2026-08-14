# Stochastic ecological portability under capped-state-driven colonization

> **Status:** exact controlled-Markov portability theorem for a finite stochastic guild-abundance model, with a quantitative stochastic depletion boundary. Markov lumpability, finite kernels, and total variation are classical substrate; the CCOC contribution is the grammar-sensitive ecological portability interpretation and its connection to the deterministic saturation results.

## 1. Stochastic colonization model

Let guild abundance be

\[
N=(N_1,\ldots,N_r),
\qquad
N_g\in\{0,\ldots,M_g\},
\]

with fixed saturation levels

\[
1\le L_g\le M_g.
\]

Define the capped ecological state

\[
Z_g=\min\{L_g,N_g\}.
\]

For each controlled colonization action `a`, assume a non-negative increment vector

\[
D=(D_1,\ldots,D_r),\qquad D_g\ge0,
\]

is drawn from a finite distribution

\[
Q_a(D\mid Z).
\]

The key ecological assumption is that the proposal law depends on the microstate only through the current capped state `Z`; hidden oversaturation above `L_g` does not alter colonization pressure on response-relevant coordinates.

The abundance update is

\[
N'_g=\min\{M_g,N_g+D_g\}.
\]

## 2. Theorem — exact stochastic saturation lumping

For every realization of `D`,

\[
\boxed{
Z'_g
=
\min\{L_g,Z_g+D_g\}.
}
\]

Therefore the induced macro transition kernel is

\[
\boxed{
\bar K_a(z,z')
=
\sum_{d:\,\min(L,z+d)=z'}Q_a(d\mid z).
}
\]

It depends only on the current capped state `z`, the action, the saturation thresholds, and the proposal law. It does **not** depend on the hidden abundance above threshold and does not depend on the carrying-capacity vector `M` as long as `M_g\ge L_g`.

Hence `Z` is an exact controlled Markov lumping of the stochastic abundance dynamics.

### Proof

Because `L_g <= M_g`,

\[
\min\{L_g,N'_g\}
=
\min\{L_g,\min(M_g,N_g+D_g)\}
=
\min\{L_g,N_g+D_g\}.
\]

If `N_g<L_g`, then `Z_g=N_g`. If `N_g>=L_g`, then `Z_g=L_g`, and adding a non-negative increment leaves the coordinate saturated. In either case

\[
\min\{L_g,N_g+D_g\}
=
\min\{L_g,Z_g+D_g\}.
\]

The conditional law of `D` is `Q_a(.|Z)`, so the law of the next capped state is the stated kernel `Kbar_a(Z,.)`. Thus all microstates in one capped fiber have the same macro output and the same next-macro distribution under every controlled action. Iteration gives equality of all finite controlled macro-response laws. `□`

## 3. Changing-capacity stochastic portability

Consider any family of capacity vectors

\[
M^{(q)}_g\ge L_g.
\]

The microstate domains

\[
\mathcal X_q=\prod_g\{0,\ldots,M^{(q)}_g\}
\]

may have different sizes. If the same capped-state-driven proposal laws `Q_a(.|z)` are used, every member of the family induces the same stochastic macro domain

\[
\mathcal Z=\prod_g\{0,\ldots,L_g\}
\]

and the same macro kernel `Kbar_a`.

Therefore one exact stochastic macro law is portable across changing abundance capacities. This is the stochastic analogue of the deterministic capacity-family theorem, and it again goes beyond same-domain partition reuse.

The executable `StochasticGuildCapacityFamilyCertificate` verifies the common macro kernel across multiple distinct abundance domains.

## 4. Why the capped-state dependence assumption matters

Monotone increments alone are not sufficient in a multi-guild model. Hidden oversaturation in one saturated guild could, in principle, change the colonization distribution of another guild that is still below threshold. Then two microstates with the same `Z` could induce different next-`Z` distributions.

The theorem therefore uses a mechanistic condition rather than merely assuming the conclusion: the arrival/proposal kernel is generated from `Q_a(D|Z)`. Once this generative contract is specified, exact lumpability follows algebraically.

## 5. Stochastic depletion opening

Now take one guild with abundance

\[
N\in\{0,\ldots,M\},
\qquad 1\le L<M,
\]

and capped response

\[
Y(N)=\min\{L,N\}.
\]

The closed contract contains only monotone colonization. Open the grammar by admitting a stochastic one-unit depletion action:

- if `N>0`, remove one unit with probability `p`;
- otherwise, or with probability `1-p`, leave abundance unchanged;
- assume

\[
0<p\le1.
\]

### Immediate threshold split

Compare the closed-equivalent states `N=L` and `N=L+1`.

From `N=L`, after one depletion action,

\[
Y'=L-1\quad\text{with probability }p,
\]

and `Y'=L` otherwise.

From `N=L+1`, both a successful one-unit depletion and a failed depletion leave the capped response at `L`. Hence its next capped response is `L` with probability one.

The total-variation distance between these two one-step response laws is exactly

\[
\boxed{\operatorname{TV}=p.}
\]

Thus every positive depletion probability destroys exact lumpability of the saturated closed fiber.

Moreover, any single approximate macro transition law used to represent both states must incur worst-case one-step TV error at least

\[
\boxed{p/2},
\]

by the triangle inequality.

## 6. Every saturated abundance remains exactly distinguishable

Take any

\[
L\le n_1<n_2\le M.
\]

Apply the depletion action

\[
t=n_1-L+1
\]

times.

Starting from `n_1`, the event that all `t` attempts deplete has probability

\[
\boxed{p^t>0}
\]

and sends abundance to `L-1`, producing a response below saturation.

Starting from `n_2`, even if every one of the same `t` depletion attempts succeeds,

\[
n_2-t\ge L,
\]

so the response cannot fall below saturation. Therefore the probability of the event `Y_t<L` is zero from `n_2` but positive from `n_1`.

Hence every pair of saturated abundance states has different finite-horizon open response laws. States below `L` were already separated by their current output. Consequently the exact open stochastic response partition is discrete:

\[
\boxed{|P_O|=M+1.}
\]

The closed colonization-only partition still has

\[
\boxed{|P_C|=L+1.}
\]

Thus a stochastic depletion action with **any** positive probability recovers the same exact worst-case state complexity as deterministic depletion.

The limit `p=1` is exactly the deterministic depletion theorem already in the repository.

## 7. Exact versus approximate boundary

The stochastic result gives a clean distinction.

- **Exact portability:** any `p>0` is enough to destroy the saturated merge, because a positive-probability response event is part of the exact future law.
- **Approximate one-step portability:** the threshold pair cannot be represented by one transition row with TV error below `p/2`.
- **Small `p`:** exact memory can still jump from `L+1` to `M+1` even though the immediate statistical separation is arbitrarily weak.

This is useful for CCOC because it separates exact causal-interface complexity from detectability at finite noise/error tolerance. A rare admissible disturbance can be structurally decisive for exact composition even when its one-step observational signature is small.

## 8. Relation to the information-flow companion

The retention/update theorem bounds how much information an adapted representation must eventually carry. The present ecological theorem supplies a concrete stochastic mechanism that determines whether hidden oversaturation is future-relevant in the first place.

Under capped-state-driven upward colonization, hidden oversaturation never changes the macro kernel, so no extra abundance information is required.

Once positive-probability depletion is legal, hidden oversaturation affects future response distributions. Exact portability then requires resolving abundance distinctions up to `M`; approximate portability can trade those distinctions against an explicit TV tolerance.

Thus the two layers are complementary:

\[
\text{ecological stochastic mechanism}
\longrightarrow
\text{which distinctions are future-relevant}
\longrightarrow
\text{information/resource cost of retaining or installing them}.
\]

## 9. Claim discipline

Do not claim novelty for Markov lumpability, thresholded birth processes, total variation, or finite stochastic kernels. The CCOC-specific content is the cross-grammar structural boundary on one ecological model class: a capped-state-driven monotone stochastic colonization mechanism yields one capacity-independent exact macro kernel, while admitting even a rare depletion action makes hidden oversaturation future-addressable and can restore full exact abundance memory.
