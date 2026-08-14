# Hidden cross-guild coupling controls exact and approximate portability

> **Status:** two-guild stochastic ecological portability theorem. The model is deliberately minimal: hidden abundance in guild A modulates recruitment of guild B. The result isolates the first cross-guild mechanism that can invalidate the capped-state stochastic macro even when each guild is individually thresholded. Bernoulli total variation and maximal coupling are classical substrate; the CCOC-specific content is the exact/approximate cross-grammar portability boundary.

## 1. Model

Let

\[
A\in\{0,\ldots,M_A\},
\qquad
B\in\{0,\ldots,M_B\},
\]

with response thresholds

\[
1\le L_A\le M_A,
\qquad
1\le L_B\le M_B.
\]

The proposed ecological macrostate is

\[
Z_A=\min(L_A,A),
\qquad
Z_B=\min(L_B,B).
\]

Consider one controlled recruitment action for guild B. Guild A does not change during this action. Conditional on the hidden abundance `A=a`, one B individual recruits with probability

\[
p(a),
\]

and otherwise B is unchanged:

\[
B'=
\begin{cases}
\min(M_B,B+1),&\text{with probability }p(A),\\
B,&\text{with probability }1-p(A).
\end{cases}
\]

This is the simplest model in which a response-saturated guild can still alter the future dynamics of another guild.

Below `L_A`, the macrostate identifies `A` exactly. The only hidden variation is therefore the saturated tail

\[
A\ge L_A.
\]

Define its hazard diameter

\[
\boxed{
\delta
=
\max_{a\ge L_A}p(a)
-
\min_{a\ge L_A}p(a).
}
\]

## 2. Exact theorem — capped-state portability iff hidden coupling disappears on the fiber

### Theorem

The capped state `(Z_A,Z_B)` is an exact controlled Markov lumping for the B-recruitment action if and only if

\[
\boxed{\delta=0.}
\]

Equivalently, the B-recruitment hazard must be constant on the saturated A fiber.

### Proof

For `Z_A<L_A`, the value of `A` is known exactly, so `p(A)` is a function of the macrostate.

For `Z_A=L_A`, all microstates `A>=L_A` are merged. If `p(A)` is constant on that tail, then every such microstate induces the same probability of the only response-relevant transition of B, so the next capped-state distribution depends only on `(Z_A,Z_B)`.

Conversely, suppose two saturated abundances `a_1,a_2>=L_A` have

\[
p(a_1)\ne p(a_2).
\]

Choose

\[
B=L_B-1.
\]

The next macrostate reaches `Z_B=L_B` with probability `p(a_i)`. The two microstates have the same current capped state `(L_A,L_B-1)` but different next-macro distributions. Exact lumpability therefore fails.

Thus exact descent of the capped macro transition is equivalent to `delta=0`. `□`

This makes the ecological condition explicit: **response saturation of A is not enough if hidden A abundance still changes response-relevant dynamics of B.**

## 3. Sharp one-step approximate theorem

Suppose `delta>0`. Let

\[
p_{\min}=\min_{a\ge L_A}p(a),
\qquad
p_{\max}=\max_{a\ge L_A}p(a).
\]

Any single macro hazard `r` used for the saturated A macrostate incurs worst-case Bernoulli total-variation error

\[
\max\{|r-p_{\min}|,|r-p_{\max}|\}.
\]

The minimax choice is the midpoint

\[
\boxed{
r^*=\frac{p_{\min}+p_{\max}}{2}}
\]

with sharp error

\[
\boxed{
\varepsilon_1^*=\frac{\delta}{2}.
}
\]

The lower bound follows because a single `r` cannot lie within less than `delta/2` of both endpoints. The midpoint attains the bound.

When `Z_B=L_B`, recruitment is invisible to the capped response and the macro row is a self-loop, so the error is zero. The worst case occurs while B is still below saturation, for example at `Z_B=L_B-1`.

Thus hidden cross-guild heterogeneity has a direct causal meaning:

\[
\boxed{
\text{intra-fiber hazard diameter}
\longleftrightarrow
2\times\text{minimum one-step macro error}.
}
\]

## 4. Finite-horizon path bound

Use the midpoint hazard for every saturated-A macrostate. At every step, whenever the true capped process and approximate macro process are still coupled, their next-step kernel TV distance is at most

\[
\varepsilon_1^*=\delta/2.
\]

A maximal coupling can therefore keep the next capped states equal with probability at least

\[
1-\delta/2.
\]

Repeating for `H` controlled B-recruitment steps gives

\[
\boxed{
\operatorname{TV}(\text{true capped path law},\text{approximate macro path law})
\le
1-(1-\delta/2)^H.
}
\]

In particular,

\[
\boxed{
1-(1-\delta/2)^H
\le
H\delta/2.
}
\]

This is an upper bound, not a claim that every system attains equality at every horizon. Saturation of B can make later recruitment differences irrelevant and reduce the actual error.

## 5. Changing-capacity family theorem

Now allow a family of systems with different

\[
(M_A^{(q)},M_B^{(q)}),
\]

while keeping `L_A,L_B` fixed.

For a single common macro law, require the hazards below threshold

\[
p^{(q)}(a),\qquad a<L_A,
\]

to agree across systems, because those abundances are explicit macro states.

Across all saturated tails of all systems, define the global range

\[
p_-=\inf_{q,a\ge L_A}p^{(q)}(a),
\qquad
p_+=\sup_{q,a\ge L_A}p^{(q)}(a),
\]

and

\[
\boxed{\delta_{\rm family}=p_+-p_-.}
\]

Using the common saturated macro hazard

\[
r_{\rm family}=\frac{p_-+p_+}{2}
\]

gives one macro transition law on the fixed state space

\[
\{0,\ldots,L_A\}\times\{0,\ldots,L_B\}
\]

with uniform one-step error

\[
\boxed{\delta_{\rm family}/2}
\]

and `H`-step path error at most

\[
\boxed{1-(1-\delta_{\rm family}/2)^H.}
\]

Both the macro state count

\[
\boxed{(L_A+1)(L_B+1)}
\]

and the error bound are independent of the abundance capacities.

If `delta_family=0`, the same construction becomes an exact stochastic macro law across changing domains. If it is positive but uniformly small, exact portability fails while approximate portability remains capacity-independent.

## 6. Why this is a substantive extension of the saturation theorem

The earlier stochastic saturation theorem assumed the increment law had the form

\[
Q(D\mid Z).
\]

That assumption deliberately removed hidden-state effects on response-relevant dynamics.

The present theorem relaxes that assumption in one explicit direction: hidden oversaturation in A may modulate B recruitment. It then quantifies exactly what is lost.

- `delta=0`: the hidden coupling descends perfectly and exact capped portability survives.
- `delta>0`: exact capped lumpability fails.
- bounded `delta`: a fixed approximate macro survives with an explicit finite-horizon error.

Thus the stochastic lumpability condition is no longer merely assumed; its violation is parameterized by an ecological interaction strength and translated into a portability error budget.

## 7. Ecological interpretation

Examples of the hidden coupling represented by `p(A)` include:

- a saturated pollinator guild whose true abundance still changes recruitment of a plant guild;
- a saturated host guild whose hidden density changes colonization probability of a parasite;
- a consumer guild whose observed functional response has saturated but whose density still changes propagule transfer for another taxon;
- facilitation or inhibition whose driver abundance is hidden by a thresholded summary.

The theorem says that thresholding A is causally safe only if those downstream effects also saturate on the same fiber. If downstream interaction strength continues to vary above the response threshold, the hidden abundance remains dynamically relevant even though A's own observed response has saturated.

For approximate modeling, the relevant quantity is not hidden abundance range by itself but the induced **within-fiber range of the downstream transition hazard**.

## 8. Relation to CCOC

The result fits the established CCOC pattern:

\[
\text{current-response compression}
+
\text{future grammar/dynamics}
\longrightarrow
\text{which hidden distinctions must remain causal state}.
\]

Here the current capped output merges all `A>=L_A`. Cross-guild recruitment provides a future experiment that can reveal differences inside that merge. Exact portability is precisely descent of the stochastic transition row; approximate portability is controlled by the row diameter.

This is different from adding another one-guild mortality variant because the newly exposed information is transmitted **between ecological components**.

## 9. Claim discipline

Bernoulli kernels, total variation, interval midpoints, and maximal coupling are classical. Do not claim those ingredients as new. The CCOC-specific contribution is the model-class boundary: hidden cross-guild dependence above a response threshold is converted into an exact lumpability criterion and a sharp one-step / controlled finite-horizon approximate portability bound that remains uniform across changing ecological capacities.
