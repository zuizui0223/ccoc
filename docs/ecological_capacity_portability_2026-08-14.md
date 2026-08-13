# Ecological capacity-family portability under saturation

> **Status:** exact changing-domain portability theorem derived from the ecological saturation blanket. The underlying abundance-state domains may change with habitat/guild capacity, while one fixed capped-guild macro-law remains exact. This moves beyond the same-domain converse results.

## 1. Family of changing ecological domains

Fix:

- a guild count `r`;
- saturation thresholds \(L=(L_1,\ldots,L_r)\);
- a finite collection of monotone colonization actions with non-negative increments \(d(a)\).

Now allow the abundance capacities themselves to vary across systems or stages:

\[
M^{(q)}=(M^{(q)}_1,\ldots,M^{(q)}_r),
\qquad
M^{(q)}_g\ge L_g.
\]

System `q` has semantic state domain

\[
\mathcal X_q
=
\prod_{g=1}^{r}\{0,1,\ldots,M^{(q)}_g\}.
\]

These domains need not have the same size. They are not being identified state-by-state.

For every domain, define the same capped ecological summary

\[
Z_g=\min\{L_g,N_g\}.
\]

## 2. Theorem — one exact macro-law for every capacity vector

For every colonization action `a`, the capped successor is

\[
\boxed{
\tau_a(Z)_g
=
\min\{L_g,Z_g+d_g(a)\}.
}
\]

This transition contains no \(M^{(q)}_g\). Therefore every capacity system realizes the **same** finite macro-state space

\[
\mathcal Z
=
\prod_{g=1}^{r}\{0,1,\ldots,L_g\}
\]

and the same action-indexed macro transitions \(\tau_a\).

Consequently one exact macro-law is portable across the entire capacity family.

### Proof

For any capacity vector with \(M_g\ge L_g\), the ecological saturation theorem gives

\[
\min\{L_g,\min(M_g,N_g+d_g(a))\}
=
\min\{L_g,Z_g+d_g(a)\}.
\]

The right-hand side depends only on `Z`, `L`, and the fixed action increment. It is independent of the underlying capacity.

Thus two abundance states from the **same** capacity system with equal `Z` have equal current macro output and equal next `Z` under every legal action, so `Z` is exact within each domain. More strongly, the induced macro output/transition table is identical for every capacity vector. Hence all domains realize one common macro dynamics. \(\square\)

## 3. Uniform memory bound across changing system size

The shared macro-law has exactly

\[
\boxed{
|\mathcal Z|=\prod_g(L_g+1)
}

possible capped states and memory

\[
\boxed{
K_{\rm macro}=\sum_g\log_2(L_g+1).
}
\]

By contrast, capacity system `q` has

\[
|\mathcal X_q|=\prod_g(M^{(q)}_g+1)
\]

abundance states.

For fixed `r` and `L`, \(|\mathcal X_q|\) can grow without bound while `K_macro` is unchanged. The result is therefore a **system-size-independent exact portability theorem across changing semantic domains**, not only a small interface for one fixed finite system.

The executable `GuildCapacityFamilyPortabilityCertificate` takes several distinct capacity vectors, verifies each ecological saturation blanket, and verifies that every stage induces the same capacity-free macro transition table.

## 4. Relation to carrying capacity, habitat size, and island comparisons

Mathematically, the varying \(M_g\) are abundance ceilings. An ecological application could use them to represent different habitat capacities, different numbers of exchangeable sites, or different maximum guild abundances across islands or environments.

The theorem does **not** claim that real carrying capacity changes leave dynamics otherwise unchanged. The portable conclusion requires the declared guild thresholds and colonization increments to remain the same and requires response saturation to occur at the fixed \(L_g\).

Under those assumptions, however, increasing the amount of hidden ecological capacity above the response threshold does not create new causal interface states: all additional oversaturation lies inside one forward-invariant macro fiber.

## 5. Depletion destroys uniform capacity portability

The one-guild depletion opening from `ecological_saturation_blanket.py` gives the opposite result. For fixed threshold `L` and capacity `M`, colonization-only futures have

\[
|P_C|=L+1,
\]

but after one depletion action becomes legal,

\[
|P_O|=M+1.
\]

Therefore

\[
K_O=\log_2(M+1)
\]

is unbounded across a family with \(M\to\infty\). No fixed finite macro-state bound can represent the exact open abundance response for the whole capacity family.

This yields a clean changing-domain separation:

\[
\boxed{
\text{monotone colonization + fixed saturation}
\Rightarrow
\text{uniform finite macro-law across }M
}
\]

whereas

\[
\boxed{
\text{opening depletion}
\Rightarrow
\text{required exact state grows with }M.
}
\]

## 6. Why this is stronger than the same-domain theorem

The terminal grammar-chain theorem uses one common semantic domain and shows that a terminal quotient can be reused at earlier grammar stages.

Here the semantic domains themselves differ:

\[
\mathcal X_1,\mathcal X_2,\ldots
\]

may have different cardinalities and no bijective state correspondence. Portability comes instead from a shared **factor map** to one capacity-independent ecological macro system.

This is the kind of changing-domain positive result that the earlier exact-converse agenda left open.

## 7. Claim discipline

The construction is a deterministic finite-state form of familiar symmetry/saturation/lumpability ideas. Do not claim novelty for aggregation by counts, thresholding, or monotone systems alone.

The CCOC-specific contribution is the portability boundary: an explicit ecological structure yields one exact macro-law across changing system sizes, while a single biologically interpretable change in the legal future grammar—depletion—can destroy every system-size-independent exact bound.
