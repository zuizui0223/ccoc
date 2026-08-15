# State-dependent feedback continuation closure — 2026-08-15

> **Status:** analytic deterministic theorem package plus executable finite certificates. This addresses the remaining feedback boundary after PRs #204–#208: hidden interaction state may now change the successor ecological context itself. It is not a novelty claim and it is not part of the first-paper dependency graph.

## 1. Problem left by exact future-context forgetting

The future-context forgetting theorem assumes autonomous context motion

\[
c' = D(c,a).
\]

That premise makes future context cones common to all hidden modes. Once a context becomes unreachable, any feedback distinction used only there can be forgotten exactly.

The harder case is

\[
\boxed{
c' = D(c,q,m,a),
}
\]

or an equivalent rule in which hidden interaction mode changes which ecological context is reached next. Then two states with the same present context can have different future context cones.

A static set such as \(\operatorname{Reach}^+(c)\) is no longer shared across the whole current fiber, so PR #208's simple restriction proof does not apply.

The question here is:

> if ecological context \(c\) and ecological macrostate \(q\) remain explicit, what is the **minimum additional hidden-mode state** required for exact future-response closure when feedback rewrites context reachability?

---

## 2. Finite state-dependent feedback contract

Let

- \(C\) be a finite ecological context set;
- \(Q\) a finite ecological macrostate set;
- \(M\) a finite persistent hidden interaction-mode set;
- \(A\) a finite action alphabet.

Current output is

\[
y=h(c,q),
\]

so hidden mode is not directly observed at fixed \((c,q)\).

A declared current feedback typing is

\[
\tau_c:M\to T_c.
\]

The actual controlled successor is

\[
(c,q,m)\xrightarrow{a}
\bigl(D(c,q,m,a),F(c,q,m,a),m\bigr).
\]

The implementation accepts the full finite transition table. It does not assume that a supplied type label is automatically sufficient; that claim is itself tested by the first theorem below.

Hidden mode is persistent here. Mode-changing systems are a later model class.

---

## 3. Theorem 1 — exact current-type criterion

Consider the interpretable summary

\[
Z_\tau(c,q,m)=(c,q,\tau_c(m)).
\]

### Theorem

\(Z_\tau\) is an exact dynamic interface **iff**, for every fixed \((c,q)\), every pair \(m,m'\) with

\[
\tau_c(m)=\tau_c(m'),
\]

and every action \(a\), the following three quantities agree:

\[
D(c,q,m,a)=D(c,q,m',a),
\]

\[
F(c,q,m,a)=F(c,q,m',a),
\]

and, writing the common successor context as \(c'\),

\[
\tau_{c'}(m)=\tau_{c'}(m').
\]

### Proof — sufficiency

Equal \(Z_\tau\) values imply equal current \(c,q\), hence equal current output. The three displayed conditions imply that every action gives equal successor context, equal successor macrostate, and equal successor type. Thus equal summary states have equal successor summary under every action. Induction on action-word length gives equal output traces for every future word. `□`

### Proof — necessity

If any one of the three successor quantities differs for two states merged by \(Z_\tau\), then after action \(a\) their successor \(Z_\tau\) values differ. Therefore the proposed summary does not define a deterministic exact successor on that macro fiber. An exact interface of this declared form is impossible. `□`

This gives a one-step test for whether the **currently visible interaction type** is already stable under its own feedback-induced future.

It also explains why a small instantaneous type count is not enough: current types may split after they route the system into a new context.

---

## 4. Relative continuation refinement

When the current type is not closed, do not immediately retain full hidden-mode identity. Instead refine hidden modes only by the future distinctions that are forced while keeping \(c,q\) explicit.

For every \((c,q)\), start with the one-block partition

\[
P^{(0)}_{c,q}=\{M\}.
\]

Given all partitions at round \(n\), define \(P^{(n+1)}_{c,q}\) by declaring \(m,m'\) equivalent iff for every action \(a\):

1. their successor contexts agree;
2. their successor ecological macrostates agree; and
3. at that common successor \((c',q')\), the persistent modes \(m,m'\) lie in the same block of \(P^{(n)}_{c',q'}\).

Equivalently, each mode receives the structural continuation row

\[
\sigma^{(n+1)}_{c,q}(m)
=
\Bigl(
 a,
 D(c,q,m,a),
 F(c,q,m,a),
 [m]_{P^{(n)}_{D,F}}
\Bigr)_{a\in A},
\]

and equal rows remain merged.

This is not the unrestricted global trace quotient. It is a **relative repair problem**: ecological context and ecological macrostate are deliberately retained as interpretable coordinates, and only hidden-mode distinctions are optimized.

---

## 5. Theorem 2 — finite stabilization and exact closure

### Theorem

The simultaneous refinement family

\[
P^{(0)}\preceq P^{(1)}\preceq P^{(2)}\preceq\cdots
\]

stabilizes after finitely many strict rounds. If \(P^*_{c,q}\) denotes the fixed point, then

\[
\boxed{
Z^*(c,q,m)=(c,q,[m]_{P^*_{c,q}})
}
\]

is an exact dynamic interface.

A uniform split bound is

\[
\boxed{
N_{\rm refine}
\le
|C|\,|Q|\,(|M|-1).
}
\]

### Proof — monotonicity and finite stabilization

Every new row contains the previous-round successor block label. Hence once two modes are separated in a \((c,q)\) fiber they never merge again. Each of the \(|C||Q|\) mode partitions begins with one block and can gain at most \(|M|-1\) blocks. Therefore the total number of strict block-increase events is at most the displayed bound. If the global partition family is not yet stable, at least one such increase occurs. `□`

### Proof — exactness at the fixed point

Take two states with equal \(Z^*\). They have the same explicit \(c,q\) and the same fixed-point hidden class. By the fixed-point row definition, every action gives the same successor context \(c'\), the same successor macrostate \(q'\), and hidden modes that remain in the same fixed-point block \(P^*_{c',q'}\). Thus the two successors again have equal \(Z^*\). Current outputs agree because output depends only on \(c,q\). Induction gives equality of all future traces. `□`

---

## 6. Theorem 3 — unique minimum repair relative to explicit ecological coordinates

The fixed point is not merely one sound refinement.

Consider any exact interface that deliberately keeps the ecological coordinates explicit:

\[
\widetilde Z(c,q,m)
=
(c,q,\rho_{c,q}(m)).
\]

### Theorem

For every \((c,q)\), the partition induced by \(\rho_{c,q}\) must refine \(P^*_{c,q}\).

Therefore \(P^*\) is the **unique coarsest / minimum-cardinality hidden-mode repair** among exact interfaces that retain \(c,q\) explicitly.

### Proof

Use induction on refinement rounds.

At round zero the claim is trivial because \(P^{(0)}_{c,q}\) has one block.

Assume every \(\rho\)-partition refines every \(P^{(n)}_{c,q}\). Take modes \(m,m'\) with

\[
\rho_{c,q}(m)=\rho_{c,q}(m').
\]

Because \(\widetilde Z\) is exact and includes \(c,q\) explicitly, each action must send the two states to equal successor \(\widetilde Z\) values. Hence their successor contexts and macrostates are identical, and their persistent modes have equal \(\rho\)-labels in the common successor fiber. By the induction hypothesis those equal \(\rho\)-labels lie in the same \(P^{(n)}\) block there. Thus the two modes have equal round-\(n+1\) continuation rows and remain together in \(P^{(n+1)}_{c,q}\).

So every exact \(\rho\) refines every round and therefore the fixed point. `□`

This is the exact analogue of a **minimum repair**: retain no hidden distinction unless feedback-induced future routing forces it.

---

## 7. Mode-routed context family

A lower-bound family shows that this repair can still be arbitrarily large even when every instantaneous context looks simple.

Fix

\[
r\ge1.
\]

Hidden mode is a bit profile

\[
b=(b_0,\ldots,b_{r-1})\in\{0,1\}^r.
\]

There is one ecological macrostate. The fixed action alphabet is

\[
A=\{\mathsf{route},\mathsf{advance}\}.
\]

For each bit index \(j\) there are three contexts:

- root \(R_j\);
- branch \(B_{j,0}\);
- branch \(B_{j,1}\).

There is one terminal context, so the whole context set has only

\[
\boxed{3r+1}
\]

states.

At root \(R_j\), current feedback type is only the current bit

\[
\tau_{R_j}(b)=b_j,
\]

so every context has at most two instantaneous types.

The hidden bit controls **context routing**:

\[
R_j\xrightarrow{\mathsf{route}}B_{j,b_j}.
\]

Branch output is its branch bit:

\[
h(B_{j,0})=0,
\qquad
h(B_{j,1})=1.
\]

Then

\[
B_{j,b}\xrightarrow{\mathsf{advance}}R_{j+1}
\]

or to the terminal context after the last bit.

Other action uses are inert self-loops, so no shorter route can skip the required alternating exposure path.

This is precisely the class excluded from PR #208: hidden mode changes the future context path itself.

---

## 8. Theorem 4 — small instantaneous type count, exponentially large continuation rank

### Theorem

At the initial root \(R_0\), the continuation fixed point is discrete over all bit profiles:

\[
\boxed{
|P^*_{R_0}|=2^r,
\qquad
K_{R_0}=r.
}
\]

Yet

\[
\boxed{
\max_c |\tau_c(M)|=2,
}
\]

there is only one ecological macrostate, only two primitive actions, and only \(3r+1\) contexts.

### Proof

Apply

\[
\mathsf{route},\mathsf{advance},
\mathsf{route},\mathsf{advance},\ldots
\]

through the phase chain. Each \(\mathsf{route}\) moves into branch \(B_{j,b_j}\), whose output reveals \(b_j\). Therefore the trace of the full routed word recovers the entire profile. Distinct profiles have different traces, so no exact initial hidden-mode interface can merge them. The continuation closure is exact and has at most \(|M|=2^r\) blocks, hence equality. `□`

For \(r\ge2\), the declared current-type summary fails the one-step closure test somewhere in the context system: modes sharing a current type can later reach a root where their next feedback types differ. For \(r=1\), the current bit already uniquely identifies the hidden mode, so current type is exact as the trivial edge case.

The route-memory excess over the **initial instantaneous** type count is therefore

\[
\boxed{
r-1\text{ bits}
}
\]

for \(r\ge1\).

---

## 9. Theorem 5 — sharp exposure depth

Take two profiles that agree on

\[
b_0,\ldots,b_{r-2}
\]

and differ only in \(b_{r-1}\).

### Theorem

Every action word of length at most

\[
2r-2
\]

produces identical output traces from these two profiles at \(R_0\), while the word

\[
(\mathsf{route}\,\mathsf{advance})^{r-1}\mathsf{route}
\]

of length

\[
\boxed{2r-1}
\]

separates them.

Hence the last hidden routing bit has exact first separating horizon

\[
\boxed{H_*=2r-1.}
\]

### Proof

To expose bit \(j+1\), the system must first route through bit \(j\) and then advance to the next root. `advance` at a root is inert, and `route` at a branch is inert, so no legal action word can arrive at \(R_{r-1}\) and execute its informative `route` in fewer than \(2r-1\) steps. The two selected profiles agree on every earlier branch output. The displayed word reaches the last branch and reveals the unequal final bit. `□`

The executable closure itself stabilizes at the same depth:

\[
\boxed{N_{\rm refine}=2r-1}
\]

for this family.

---

## 10. What changed relative to the previous feedback theorems

The progression is now:

1. **PR #204:** hidden mode changes turnover, turnover changes later accessibility;
2. **PR #205:** fixed copy-anonymous interaction types give replication-independent exact portability;
3. **PR #207:** context-dependent feedback types require a stable master type when context motion is mode-independent;
4. **PR #208:** autonomous irreversible context loss permits exact causal forgetting;
5. **this theorem:** hidden mode can change the successor context itself; exact repair is the continuation fixed point, and a small instantaneous typing can conceal an exponentially larger future routing rank.

The new object is not a static reachability set. It is a **feedback continuation partition** over persistent hidden modes conditional on explicit ecological context and macrostate.

---

## 11. Scope and non-claims

This theorem is deliberately finite and deterministic.

It does **not** claim:

- that context/macro coordinates are always the scientifically optimal observables;
- that the relative continuation partition is the unrestricted global trace quotient if context or macrostate may themselves be merged;
- stochastic or partially observed closure;
- hidden-mode transitions or evolution;
- empirical identification of the relevant contexts, modes, or actions;
- historical novelty of partition refinement or fixed-point computation.

The common-refinement / right-congruence logic is substrate. The ecological content is the explicit structural boundary: **when feedback changes future context reachability, exact hidden memory is the minimum continuation-stable repair of the current ecological coordinates, and that repair can grow linearly in bits despite uniformly binary instantaneous feedback typing.**

## 12. Executable evidence

- theorem module: `causal_model/state_dependent_feedback_closure.py`
- regression: `tests/test_state_dependent_feedback_closure.py`
- finite routed-family checks: ranks `1..4`

The tests verify current-type positive/negative cases, exact continuation fixed points, the \(2^r\) initial rank, the \(2r-1\) stabilization/exposure horizon, and fail-closed input handling.
