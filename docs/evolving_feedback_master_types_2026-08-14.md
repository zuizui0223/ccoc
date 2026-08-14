# Evolving feedback master-type closure — 2026-08-14

> **Status:** analytic theorem package with executable finite certificates. This extends the fixed-type feedback results of PRs #204–#205 to context-dependent interaction types. It is not a historical novelty claim.

## 1. Problem

The bounded-type feedback theorem proves that physical replication is harmless when copies remain response-equivalent members of one fixed interaction type. The next question is harder:

> What if the interaction-type partition itself changes as ecological context changes?

A system can look simple at every instant and still require large portable memory. The number of response types visible **now** is not the quantity that controls exact future portability when later ecological phases split those current types differently.

The correct finite object is the response type that remains stable across **all reachable future contexts**.

---

## 2. Context-specific feedback types

Let

- `C` be a finite set of ecological contexts;
- `Q` a finite ecological macrostate set;
- `M` a finite hidden interaction-mode set;
- `A` a finite action alphabet.

For every context `c`, hidden mode `m` has a context-specific feedback type

\[
\tau_c(m)\in T_c.
\]

The output depends only on current ecological context and macrostate:

\[
y=h(c,q).
\]

For action `a`, assume

\[
c' = D(c,q,a)
\]

and

\[
q' = F(c,q,a,\tau_c(m)).
\]

The hidden mode itself is persistent. Thus mode identity may influence the next ecological state, but only through the type relevant in the **current** context.

This is a finite deterministic contextual-feedback contract. It does not assert that an empirical ecological system is literally finite or that the relevant contexts/types can be inferred without data.

---

## 3. Master feedback signature

Define

\[
\boxed{
\tau^*(m)
=
\bigl(\tau_c(m)\bigr)_{c\in C}.
}
\]

Two hidden modes have the same master type iff they have the same feedback type in every context:

\[
m\equiv_*m'
\iff
\tau_c(m)=\tau_c(m')
\quad\forall c\in C.
\]

Let

\[
T^* = M/{\equiv_*}
\]

and let

\[
R_* = |T^*|
\]

be the **master feedback-type rank**.

This is the common refinement of the context-specific type partitions. That set-theoretic refinement fact is elementary substrate; the theorem below identifies why this particular refinement is an exact causal-interface object for evolving ecological feedback.

---

## 4. Theorem — master-type exact closure

### Theorem 1

Under the contextual-feedback contract above, the summary

\[
\boxed{
Z(c,q,m)
=
\bigl(c,q,[m]_*\bigr)
}
\]

is an exact dynamic interface for every legal future action word.

Consequently

\[
\boxed{
|Z|
\le
|C|\,|Q|\,R_*.
}
\]

### Proof

Take two microstates with equal summary:

\[
(c,q,[m]_*)=(c',q',[m']_*).
\]

Then `c=c'`, `q=q'`, and

\[
\tau_d(m)=\tau_d(m')
\qquad\forall d\in C.
\]

In particular the current-context labels agree:

\[
\tau_c(m)=\tau_c(m').
\]

Current outputs therefore agree because both equal `h(c,q)`.

For any action `a`, the context successor is the same:

\[
D(c,q,a).
\]

The macro successor is also the same because

\[
F(c,q,a,\tau_c(m))
=
F(c,q,a,\tau_c(m')).
\]

The hidden modes remain `m,m'`, whose master classes are still equal. Hence the two successors again have the same `Z` value.

Thus output and every action successor factor through `Z`. By the exact dynamic-interface criterion, all future response traces factor through `Z`. `□`

The important point is that a current type label alone is generally insufficient. The master label remembers only the distinctions that can become transition-relevant in **some** reachable context.

---

## 5. Changing-domain portability under hidden-mode replication

Suppose several semantic domains have different hidden-mode sets

\[
M_1,M_2,\ldots
\]

but share:

- the same `C,Q,A`;
- the same output law `h`;
- the same context update `D`;
- the same context/type-conditioned macro transition law `F`; and
- the same finite set of master signatures `T^*`.

The domains may contain arbitrarily many distinct micro-mode identities inside one master type.

### Theorem 2

All such domains factor through the **same** exact macro system

\[
C\times Q\times T^*.
\]

The macro output and transition table do not depend on the number of micro-mode identities in any master class.

### Proof

Theorem 1 gives exactness in every domain. For a macrostate `(c,q,t^*)`, choose the master row represented by `t^*`. Its current context label is fixed, so

\[
(c,q,t^*)\xrightarrow{a}
\left(
D(c,q,a),
F(c,q,a,\tau_c(t^*)),
 t^*
\right)
\]

is identical in every domain. Duplicating micro modes within the same master signature therefore changes only fiber cardinality, not the macro law. `□`

This is the evolving-type analogue of copy-anonymous feedback portability: exact memory depends on the number of future-response-distinct master types, not raw hidden-mode multiplicity.

---

## 6. Why bounded instantaneous type count is insufficient

A tempting but false portability criterion is

\[
\sup_c |T_c|<\infty.
\]

The next family refutes it maximally: every context has only two instantaneous types, yet master rank is exponential.

---

## 7. Rotating feedback family

Fix

\[
r\ge1.
\]

Hidden modes are binary profiles

\[
b=(b_0,\ldots,b_{r-1})\in\{0,1\}^r.
\]

There are `r` ecological contexts. In context `c`, the current feedback type is only

\[
\boxed{\tau_c(b)=b_c.}
\]

Therefore

\[
|T_c|=2
\qquad\forall c.
\]

But the master signature is the whole binary vector:

\[
\tau^*(b)=b,
\]

so

\[
\boxed{R_*=2^r.}
\]

### Local feedback cycle

The ecological macro has six states:

1. `READY` — facilitator present, target empty;
2. `OCCUPIED` — first spread has colonized the target;
3. `POST_LIVE` — turnover occurred and facilitator survived;
4. `POST_DEAD` — turnover occurred and facilitator was lost;
5. `REPROBE_LIVE` — second spread recolonized the target;
6. `REPROBE_DEAD` — second spread failed because accessibility was lost.

One fixed primitive action `step` advances the cycle:

\[
\text{READY}
\to
\text{OCCUPIED}
\to
\text{POST}_{b_c}
\to
\text{REPROBE}_{b_c}
\to
\text{READY in context }c+1.
\]

At the turnover transition,

- `b_c=0` means the facilitator survives;
- `b_c=1` means it is lost.

The subsequent spread converts that difference into target occupancy. Thus after the third step of context `c`,

\[
\boxed{Y=1-b_c.}
\]

The fourth step resets the local gate and advances to context `c+1`.

This is the same ecological feedback logic as PR #204, but the relevant hidden distinction **rotates with context** rather than being selected by an address.

---

## 8. Theorem — exponential master rank from binary instantaneous partitions

### Theorem 3

On the canonical initial slice

\[
(c,q)=(0,\mathrm{READY}),
\]

all `2^r` hidden profiles have the same current output and the same current ecological macrostate. Nevertheless the exact all-future response quotient is discrete:

\[
\boxed{|P_{\rm initial}|=2^r,}
\qquad
\boxed{K_{\rm initial}=r.}
\]

### Proof

For profile `b`, after `4c+3` repeated `step` actions the output is

\[
1-b_c.
\]

Hence the response trace through

\[
4r-1
\]

steps decodes every coordinate `b_c`. Any two distinct profiles differ at some context and therefore have different future traces. The exact quotient on the `2^r` initial profiles is discrete. `□`

Thus

\[
\boxed{
\max_c \log_2 |T_c|=1
\quad\text{but}\quad
K_{\rm initial}=r.
}
\]

A uniformly one-bit instantaneous feedback description does **not** imply a uniformly one-bit portable interface.

---

## 9. Sharp exposure horizon

### Theorem 4

The first horizon at which all profile distinctions are simultaneously available from the canonical initial slice is

\[
\boxed{H_*=4r-1.}
\]

### Upper bound

At horizon `4r-1`, the trace has revealed

\[
1-b_0,1-b_1,\ldots,1-b_{r-1},
\]

so all profiles are separated.

### Lower bound

Take two profiles that differ only in the final bit `b_{r-1}`. Before the third step of the final context, that bit has not affected any ecological transition or output. Therefore their traces agree through horizon

\[
4r-2.
\]

They first differ at step `4r-1`. `□`

So the family separates two notions:

- instantaneous feedback type count: always 2;
- future-stable master rank/exposure: `2^r` classes revealed only after linear context depth.

---

## 10. Positive/negative boundary after PRs #204–#205

The feedback program now has three exact levels.

### Fixed copy-anonymous type

PR #205:

\[
|P|=5
\]

per fixed interaction type, independent of physical replication.

### Multiple fixed master types

Theorem 1–2 here:

\[
|P|\le |C||Q|R_*
\]

and hidden-mode duplication inside a master type is free.

### Evolving context partitions

The rotating family:

\[
|T_c|=2\quad\forall c,
\qquad
R_*=2^r,
\qquad
K_{\rm initial}=r.
\]

Therefore the natural structural boundary is not raw network size or instantaneous type count. It is the number of feedback distinctions that remain inequivalent after taking **all reachable future contexts** into account.

---

## 11. What this theorem does not claim

- The common-refinement operation itself is not new mathematics.
- This is not a universal characterization of stochastic/adaptive ecological networks.
- Contexts and type maps are declared model objects; the theorem does not infer them from field data.
- A bounded master rank is a sufficient exact portability condition in this contextual-feedback class, not evidence that an empirical system has such a bound.
- The rotating family is a sharp counterexample to an instantaneous-type criterion, not a claim that real ecological phases expose one independent bit each.

---

## 12. Executable certificate

`causal_model/evolving_feedback_master_types.py` provides:

- `ContextualFeedbackSystem` — finite contextual-feedback contract;
- `MasterFeedbackTypeClosureCertificate` — exact master-type interface check;
- `MasterTypePortabilityCertificate` — changing-domain hidden-mode replication portability;
- `rotating_feedback_system(r)` — binary instantaneous-type counterfamily;
- `RotatingFeedbackTypeCertificate` — exact `2^r` initial quotient, `r` bits, and sharp `4r-1` horizon;
- finite tests that compare profile traces, master partitions, dynamic closure, and changing-domain macro laws.

The analytic proofs above establish the all-rank statements. The finite tests are falsification/regression checks, not substitutes for those proofs.
