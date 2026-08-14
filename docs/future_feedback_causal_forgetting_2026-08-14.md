# Future-context feedback and exact causal forgetting — 2026-08-14

> **Status:** analytic theorem package with finite regression. This follows the evolving master-type theorem by showing that even the global master signature can be overcomplete once some ecological contexts become permanently unreachable. It is not a novelty claim.

## 1. Question

The evolving master-type theorem uses the full signature

\[
\tau^*(m)=(\tau_c(m))_{c\in C}
\]

and is exact whenever a hidden interaction mode can matter differently in different ecological contexts.

But if context evolution is irreversible, distinctions that matter only in contexts that can never occur again should not remain in the exact interface forever.

The next question is therefore:

> Which parts of a hidden feedback mode may be forgotten exactly after ecological context changes?

---

## 2. Autonomous context evolution

Use the contextual feedback contract

\[
y=h(c,q),
\]

\[
q'=F(c,q,a,\tau_c(m)).
\]

Strengthen only the context update premise:

\[
\boxed{c'=D(c,a).}
\]

Thus the next ecological context depends on the current context and declared action, but not on hidden mode identity or the current ecological macrostate.

This premise is deliberately explicit. If hidden mode or ecological macrostate changes which contexts become reachable, the theorem below does not apply without augmenting the context state.

Let

\[
\operatorname{Reach}^+(c)
\]

be the contexts reachable from `c` under finite action words, including `c` itself.

For every transition

\[
c\xrightarrow{a}c',
\]

reachability is nested:

\[
\operatorname{Reach}^+(c')
\subseteq
\operatorname{Reach}^+(c).
\]

---

## 3. Future feedback signature

Define

\[
\boxed{
\tau_c^+(m)
=
\bigl(\tau_d(m)\bigr)_{d\in\operatorname{Reach}^+(c)}.
}
\]

The associated future feedback rank is

\[
\boxed{
R_c^+
=
\left|
\{\tau_c^+(m):m\in M\}
\right|.
}
\]

Unlike the global master signature, this keeps only distinctions that can still become transition-relevant from the present context.

---

## 4. Theorem — exact future-signature interface

### Theorem 1

Under autonomous context evolution, the state summary

\[
\boxed{
Z^+(c,q,m)
=
(c,q,\tau_c^+(m))
}
\]

is an exact dynamic interface.

### Proof

Take two microstates with equal summary:

\[
(c,q,\tau_c^+(m))
=
(c,q,\tau_c^+(m')).
\]

Because `c` belongs to its own future-reachable set,

\[
\tau_c(m)=\tau_c(m').
\]

Therefore current output and the next ecological macrostate agree under every action:

\[
F(c,q,a,\tau_c(m))
=
F(c,q,a,\tau_c(m')).
\]

The context successor is the same fixed value

\[
c'=D(c,a).
\]

Now

\[
\operatorname{Reach}^+(c')
\subseteq
\operatorname{Reach}^+(c).
\]

The two old future signatures agreed on every context in the larger set, so their restrictions to the smaller set also agree:

\[
\tau_{c'}^+(m)=\tau_{c'}^+(m').
\]

Hence equal summary states have equal output and equal successor summary under every action. The exact dynamic-interface criterion gives equality of all future response traces. `□`

---

## 5. Corollary — exact causal forgetting

A hidden distinction may be removed from the interface as soon as every context in which it changes the feedback type has become unreachable.

This is exact, not approximate:

\[
\boxed{
\tau_c^+(m)=\tau_c^+(m')
\Longrightarrow
m,m'\text{ are safely merged by }Z^+.
}
\]

The theorem therefore formalizes a causal version of forgetting:

> past interaction distinctions are disposable once there is no legal future path by which they can affect the declared response again.

---

## 6. Rank monotonicity

### Theorem 2

Along every legal context transition

\[
c\to c',
\]

the future feedback rank cannot increase:

\[
\boxed{R_{c'}^+\le R_c^+.}
\]

### Proof

Every signature at `c'` is the restriction of a signature at `c` from

\[
\operatorname{Reach}^+(c)
\]

to its subset

\[
\operatorname{Reach}^+(c').
\]

Restriction cannot create more distinct rows. `□`

Thus irreversible context loss can only preserve or reduce the exact hidden-feedback burden.

This statement concerns the declared autonomous context graph. Opening a new context edge changes the graph and therefore changes the theorem input; it can increase future rank.

---

## 7. Irreversible feedback chain

Fix

\[
r\ge1.
\]

There are `r` informative contexts

\[
0,1,\ldots,r-1
\]

and one terminal context `r`.

Hidden modes are profiles

\[
b=(b_0,\ldots,b_{r-1})\in\{0,1\}^r.
\]

Context-specific feedback type is

\[
\tau_c(b)=b_c
\quad(c<r),
\]

while the terminal context has one inert type.

The action set is fixed:

\[
A=\{\mathsf{spread},\mathsf{turnover},\mathsf{advance}\}.
\]

`advance` moves irreversibly

\[
c\mapsto\min(c+1,r)
\]

and resets the local facilitator/target gate to the ready state. `spread` and `turnover` leave context unchanged.

At informative context `c`, the gate dynamics are the same endogenous-accessibility mechanism used in the earlier feedback theorems:

1. `spread` colonizes when the facilitator is present;
2. `turnover` clears the target and removes the facilitator iff `b_c=1`;
3. another `spread` succeeds iff the facilitator survived.

Hence

\[
\mathsf{spread}\,\mathsf{turnover}\,\mathsf{spread}
\]

returns final target occupancy

\[
1-b_c.
\]

---

## 8. Exact future rank in the chain

From context `c`, the reachable context set is

\[
\{c,c+1,\ldots,r\}.
\]

Therefore the future signature contains exactly the suffix bits

\[
(b_c,b_{c+1},\ldots,b_{r-1}).
\]

### Theorem 3

For `c<r`,

\[
\boxed{R_c^+=2^{r-c}.}
\]

At the terminal context,

\[
\boxed{R_r^+=1.}
\]

Consequently the exact hidden-feedback memory represented by the future signature is

\[
\boxed{
\log_2R_c^+=r-c
}
\]

bits and reaches zero at the terminal context.

---

## 9. Canonical minimality on the ready slice

The upper bound from Theorem 1 is exact for the chain.

Take the ready local gate state at context `c`. For every future informative context `j>=c`, use

\[
w_{c,j}
=
\mathsf{advance}^{j-c}
\mathsf{spread}
\mathsf{turnover}
\mathsf{spread}.
\]

The final output is

\[
1-b_j.
\]

Thus every suffix bit is separately future-addressable from the ready slice.

### Theorem 4

The canonical exact response quotient on the ready slice at context `c` has

\[
\boxed{|P_c^{\rm ready}|=2^{r-c}}
\]

classes for `c<r`, and one class at `c=r`.

Therefore

\[
\boxed{
K_c^{\rm ready}=r-c
}
\]

bits.

The future-signature interface is not merely sufficient here; it is minimal on the declared ready slice.

---

## 10. Sharp one-bit forgetting per irreversible advance

For every informative context transition

\[
c\xrightarrow{\mathsf{advance}}c+1,
\]

\[
R_{c+1}^+
=
\frac12R_c^+.
\]

Equivalently,

\[
\boxed{
K_{c+1}^{\rm ready}
=
K_c^{\rm ready}-1.
}
\]

The bit `b_c` matters at context `c`, but after `advance` there is no legal path back to any context in which `b_c` can affect turnover or future accessibility. It is therefore deleted from the exact causal interface immediately and permanently.

This gives a constructive sequence

\[
\boxed{
r,r-1,\ldots,1,0}
\]

of exact hidden-feedback memory requirements.

---

## 11. Relation to the previous feedback results

### PR #204 — addressable feedback rank

Many currently latent feedback modes can be forced to remain necessary when legal futures can address them.

### PR #205 — fixed bounded-type portability

Physical copies can grow without increasing exact memory if they remain copy-anonymous members of a fixed response type.

### PR #207 — evolving master types

Small instantaneous type count does not imply portability; all future contexts must be considered through a master signature.

### This theorem — exact forgetting

Even the global master signature may retain too much once some contexts are permanently unreachable. Exact memory is controlled by the master signature restricted to the **future causal cone in context space**.

The resulting picture is:

\[
\boxed{
\text{exact feedback memory at time }t
\sim
\text{future-response-distinct interaction signatures still reachable from }t.
}
\]

---

## 12. Scope and non-claims

- The theorem requires autonomous context evolution `c'=D(c,a)`. If context reachability depends on hidden mode or ecological macrostate, the context state must be augmented or another theorem is required.
- Reachability-set restriction is elementary set theory; no novelty is claimed for that operation.
- The chain is a sharp finite construction, not a claim that ecological succession always removes exactly one independent interaction bit per phase.
- Contexts, actions, and hidden types are declared model objects and are not inferred from observational data here.
- The result is exact deterministic finite-state mathematics; stochastic approximate forgetting remains a separate problem.

---

## 13. Executable certificate

`causal_model/future_feedback_causal_forgetting.py` provides:

- exact detection of the autonomous-context premise;
- future-reachable context sets;
- future feedback signatures and ranks;
- `FutureFeedbackClosureCertificate` for exact dynamic closure and rank monotonicity;
- `irreversible_feedback_chain(r)`;
- direct future bit probes;
- `IrreversibleFeedbackForgettingCertificate` verifying the exact rank sequence, canonical ready-slice block counts, and one-bit forgetting per irreversible context advance.

Finite tests cover small ranks and fail closed when context evolution depends on ecological macrostate. The all-rank statements are the analytic results above.
