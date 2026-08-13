# Ecological saturation blanket under monotone guild colonization

> **Status:** exact ecological structural theorem in a finite deterministic abundance model. The theorem derives a system-size-independent causal blanket from guild structure, monotone colonization, and response saturation. Exchangeability/lumpability and threshold response models are classical substrate; the CCOC-specific role is to identify when those ecological assumptions do and do not protect compression under a later grammar opening.

## 1. Ecological state class

Consider `r` ecological guilds. Guild `g` has abundance

\[
N_g\in\{0,1,\ldots,M_g\}.
\]

The vector

\[
N=(N_1,\ldots,N_r)
\]

is the semantic exterior state. This abundance representation is appropriate when identities inside one guild are ecologically exchangeable for the declared response and actions; the theorem starts from that guild-abundance quotient rather than claiming that arbitrary identity-level dynamics are exchangeable.

Fix saturation thresholds

\[
1\le L_g\le M_g
\]

and define the capped guild summary

\[
Z_g=\min\{L_g,N_g\}.
\]

Assume the focal response depends on exterior abundance only through `Z`.

Every declared closed ecological action `a` is a monotone colonization event with non-negative guild increments

\[
d(a)=(d_1(a),\ldots,d_r(a)),
\qquad d_g(a)\ge0,
\]

and abundance update

\[
N'_g=\min\{M_g,N_g+d_g(a)\}.
\]

All such actions are legal at every closed grammar state; equivalently the future grammar is the free monoid over the declared colonization actions.

## 2. Theorem — capped guild counts are an exact dynamic blanket

For every guild and every colonization action,

\[
\boxed{
Z'_g
=
\min\{L_g,Z_g+d_g(a)\}.
}
\]

Therefore the vector `Z` is an exact dynamic interface for every legal colonization future.

### Proof

Since \(L_g\le M_g\),

\[
Z'_g
=
\min\{L_g,N'_g\}
=
\min\{L_g,N_g+d_g(a)\}.
\]

If \(N_g<L_g\), then \(Z_g=N_g\), so

\[
Z'_g=\min\{L_g,Z_g+d_g(a)\}.
\]

If \(N_g\ge L_g\), then \(Z_g=L_g\). Non-negative colonization cannot move the guild below threshold, hence both sides equal \(L_g\).

Thus the next summary is a deterministic function of the current summary and action. States with equal `Z` have equal current response and equal successor `Z` under every legal action. By induction on legal word length, equal `Z` implies equal response trace for every future colonization word. Hence `Z` is an exact dynamic blanket. \(\square\)

## 3. System-size-independent bound

Every component has

\[
Z_g\in\{0,1,\ldots,L_g\},
\]

so the blanket has at most

\[
\boxed{
|\mathcal Z|=\prod_{g=1}^{r}(L_g+1)
}
\]

states and therefore memory

\[
\boxed{
K_Z\le\sum_{g=1}^{r}\log_2(L_g+1).
}
\]

For fixed guild count `r` and fixed ecological saturation thresholds `L_g`, this bound is independent of the carrying capacities `M_g`. The uncapped abundance state space has

\[
\prod_g(M_g+1)
\]

states and can grow without bound while the exact blanket remains fixed.

The executable certificate uses `Z` itself as the observable output. In that sharp realization, different capped summaries are already distinguished at the current time, so the canonical exact quotient has exactly

\[
\prod_g(L_g+1)
\]

blocks. The bound is therefore attainable, not merely an upper bound.

## 4. Why monotonicity matters

Saturation by itself does **not** make hidden oversaturation causally irrelevant. The proof used a specific ecological property: once a guild is at or above threshold, every allowed action keeps it at or above threshold.

A depleting action can reveal how far above threshold the hidden abundance actually was.

## 5. One-guild depletion opening — exact obstruction

Take one guild with

\[
N\in\{0,1,\ldots,M\},
\qquad 1\le L<M,
\]

and observable response

\[
Z=\min\{L,N\}.
\]

The plant has two primitive actions:

\[
\mathsf{colonize}:N\mapsto\min\{M,N+1\},
\]

and

\[
\mathsf{deplete}:N\mapsto\max\{0,N-1\}.
\]

In the **closed** grammar only `colonize` is legal. In the **open** grammar `deplete` becomes legal as one newly admitted primitive action.

### Closed quotient

Under colonization-only futures, all states \(N\ge L\) remain saturated forever, while states below `L` have distinct current outputs. Therefore

\[
\boxed{|P_C|=L+1.}
\]

The capped abundance `Z` is exactly the canonical closed quotient.

### First open split

The closed-equivalent states

\[
N=L,
\qquad
N=L+1
\]

have the same capped summary `L`. But one depletion gives

\[
L\mapsto L-1,
\qquad
L+1\mapsto L,
\]

whose outputs differ. Hence `deplete` does not descend to the capped closed quotient. This is exactly the one-state action-descent obstruction from the CCOC converse theorem.

### Open quotient is discrete

Take any \(N_1<N_2\). If their current capped outputs differ, they are already distinguished. Otherwise both are at least `L`. Apply

\[
\mathsf{deplete}^{N_1-L+1}.
\]

The first state reaches `L-1`, while the second remains at least `L`, so their outputs differ. Therefore every pair of abundance states is open-distinguishable and

\[
\boxed{|P_O|=M+1.}
\]

Thus

\[
\boxed{
K_O-K_C
=
\log_2\frac{M+1}{L+1}.
}
\]

For fixed saturation threshold `L`, this diverges as \(M\to\infty\).

So a fixed saturation blanket can be perfectly exact for all closed colonization futures yet fail arbitrarily badly after opening only **one depletion action**.

## 6. Ecological interpretation

The positive theorem identifies a genuine structural route to a small causal boundary:

- guild-level exchangeability removes identity dependence;
- response saturation removes abundance distinctions above ecological thresholds;
- monotone colonization ensures those hidden oversaturation distinctions can never return to the response-relevant range.

All three pieces matter. The relay theorem already showed that narrow physical cuts, sparse topology, and low treewidth alone do not guarantee a small causal interface. The present theorem supplies a different positive mechanism: **order-preserving ecological dynamics plus saturation create forward-invariant response fibers.**

The depletion counterexample then gives the portability boundary. If the open grammar admits an action that can drive a saturated guild back through its response threshold, hidden oversaturation becomes future-addressable and the old capped blanket may need refinement.

This has a direct ecological reading: a thresholded occupancy/abundance summary can be exact under irreversible accumulation but cease to be exact when extinction, harvest, disturbance, or other abundance-reducing interventions become admissible.

## 7. Relation to exact reuse/converse results

The theorem does not introduce a separate notion of portability.

- The positive colonization result constructs a `GrammarAwareDynamicInterfaceCertificate` for capped guild counts.
- The depletion opening is a one-state grammar expansion.
- Its failure is witnessed by the existing `ActionDescentObstructionCertificate`.

Therefore the ecological theorem plugs directly into the current CCOC hierarchy:

\[
\boxed{
\text{forward-invariant saturation fibers}
\Rightarrow
\text{small exact blanket}
}
\]

while

\[
\boxed{
\text{new depletion action breaks fiber descent}
\Rightarrow
\text{forced open refinement}.
}
\]

## 8. Scope and claim discipline

This is a finite deterministic abundance theorem, not an empirical claim that real guilds are perfectly exchangeable, that ecological responses truly saturate at known thresholds, or that colonization is irreversible in nature. Those assumptions would have to be justified for an application.

Do not claim novelty for lumpability, permutation symmetry, threshold aggregation, monotone systems, or deterministic finite-state minimization. The CCOC-specific contribution is the structural positive/negative boundary: explicit ecological assumptions derive a finite blanket, and relaxing the monotone future grammar by one biologically interpretable action exposes exactly why that blanket can fail.
