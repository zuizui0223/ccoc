# Scalable feedback-gate rank theorem — 2026-08-14

> **Status:** analytic all-rank theorem family plus finite regression. This promotes the five-state feedback-network triage mechanism to a scalable lower-bound/cycle-necessity result. It does **not** yet give a complete positive portability classification for arbitrary feedback networks, and it is not a historical novelty claim.

## 1. Question

The five-state benchmark in `experiments/feedback_network_nonreducibility.py` shows one hidden interaction mode that is invisible to current output, static reachability, occupancy count, and every response word through length two, but becomes necessary under

\[
\mathsf{spread}\;\mathsf{turnover}\;\mathsf{spread}.
\]

The scalable question is whether this is only a tiny counterexample or whether endogenous accessibility feedback can generate an arbitrarily large exact interface burden while the **current ecological graph and current visible summaries remain fixed**.

The answer is yes.

The additional structural point is that the burden exists only when both arrows of the ecological feedback cycle are present:

\[
\text{latent interaction mode}
\longrightarrow
\text{turnover-induced facilitator loss}
\longrightarrow
\text{future spread accessibility}.
\]

Cut either arrow and the entire hidden-mode memory collapses.

---

## 2. Family

Fix an integer

\[
r\ge1.
\]

There are `r` active ecological gates. Gate `i` has:

- an immutable binary interaction mode
  \(m_i\in\{0,1\}\);
- a facilitator/accessibility state
  \(f_i\in\{0,1\}\);
- a local target occupancy
  \(t_i\in\{0,1\}\).

The latent profile is

\[
m=(m_1,\ldots,m_r)\in\{0,1\}^r.
\]

The canonical comparison slice fixes

\[
f_i=1,
\qquad
t_i=0
\qquad\forall i,
\]

so every profile has exactly the same current effective accessibility graph: every gate is open and every target is empty.

### Fixed control alphabet

Let

\[
d=\lceil\log_2 r\rceil
\]

with `d=0` for `r=1`. Gate indices use fixed-length binary addresses of length `d`; unused binary codes when `r` is not a power of two are inert.

The primitive action alphabet is independent of `r`:

\[
\boxed{
A=\{0,1,\mathsf{spread},\mathsf{turnover}\}.
}
\]

The `0/1` controls move only the experimental selector. They do not contain `m_i`, facilitator state, or an `r`-valued gate label.

Once an active gate is selected, the ecological actions are

\[
\mathsf{spread}:
\qquad
t_i\leftarrow t_i\lor f_i,
\]

and, if `t_i=1`,

\[
\mathsf{turnover}:
\qquad
t_i\leftarrow0,
\qquad
f_i\leftarrow
\begin{cases}
0,&m_i=1,\\
f_i,&m_i=0.
\end{cases}
\]

The observable is the target occupancy at the currently selected active gate; before a valid gate is selected it is zero.

Thus the hidden mode does not alter the current graph. It acts only after colonization makes turnover biologically effective, and the resulting facilitator state changes later colonization accessibility.

---

## 3. Current visible summaries are identical

On the canonical initial slice, every profile has

\[
Y_0=0,
\qquad
\sum_i f_i=r,
\qquad
\sum_i t_i=0,
\qquad
\#\{i:f_i=1\}=r.
\]

Every active gate is currently reachable through its local facilitator edge, so current static gate distance is one for all profiles.

Therefore any summary constructed only from

- current focal output;
- current static reachability/distance;
- current facilitator count;
- current target occupancy count; or
- the current effective gate graph

is identical across all `2^r` latent profiles.

This is stronger than saying the profiles have the same number of states. They represent literally the same current occupancy/accessibility configuration and differ only in a mode that affects how that configuration changes after an alternating ecological future.

---

## 4. Lemma — one feedback query decodes one mode bit

Let `addr(i)` be the fixed binary address of gate `i`, and define

\[
w_i
=
\operatorname{addr}(i)
\;\mathsf{spread}\;
\mathsf{turnover}\;
\mathsf{spread}.
\]

Then

\[
|w_i|=d+3.
\]

### Lemma

Starting from the canonical initial state for profile `m`, the final output under `w_i` is

\[
\boxed{Y_{\rm final}(w_i)=1-m_i.}
\]

### Proof

Addressing changes no ecological state, so the selected gate begins with

\[
(f_i,t_i)=(1,0).
\]

The first `spread` gives

\[
(1,0)\mapsto(1,1),
\]

independently of `m_i`.

`turnover` clears the target. If `m_i=0`, the facilitator survives:

\[
(1,1)\mapsto(1,0).
\]

If `m_i=1`, turnover removes it:

\[
(1,1)\mapsto(0,0).
\]

The second `spread` therefore yields target occupancy one in the first case and zero in the second:

\[
Y_{\rm final}=1-m_i.
\]

Hence the declared legal word itself supplies the decoder

\[
m_i=1-Y_{\rm final}(w_i).
\]

`□`

The latent bit is not a primitive readout. It becomes observable only because one ecological transition changes the state on which the hidden interaction acts, and that interaction changes later accessibility.

---

## 5. Theorem — exact scalable feedback-mode rank

Consider only the canonical initial comparison domain

\[
D_r=\{x(m):m\in\{0,1\}^r\},
\]

where all facilitator and target states are fixed as above.

### Theorem 1

Under the full feedback dynamics, the exact response quotient on `D_r` is discrete:

\[
\boxed{|P_{\rm fb}(D_r)|=2^r.}
\]

Equivalently,

\[
\boxed{K_{\rm fb}(D_r)=r.}
\]

### Proof

Take two distinct profiles `m != m'`. They differ at some gate `i`:

\[
m_i\ne m'_i.
\]

By the decoder lemma,

\[
Y_{\rm final}(x(m),w_i)=1-m_i
\ne
1-m'_i=Y_{\rm final}(x(m'),w_i).
\]

Thus every unequal pair of profiles has a legal future word with a different output trace. All `2^r` initial states are therefore in distinct exact response classes.

The quotient cannot have more than the `2^r` states in the declared comparison domain, so equality follows. `□`

### Consequence

The current visible summary has one value on `D_r`, while the exact future-response interface has `2^r` classes:

\[
\boxed{
K_{\rm exact}-K_{\rm current\ visible}=r.
}
\]

This is the scalable version of the five-state nonreducibility observation: present-time reachability and abundance can be identical while future accessibility feedback stores arbitrarily many exact causal bits.

---

## 6. Theorem — exact first separating horizon

### Theorem 2

The first horizon at which any two mode profiles can be distinguished is

\[
\boxed{
H_\star=d+3
=
\lceil\log_2r\rceil+3.
}
\]

### Proof

A hidden mode affects the transition only when all of the following have occurred:

1. `d` binary selector actions have reached an active gate;
2. `spread` has made that target occupied;
3. `turnover` has converted `m_i` into a possible facilitator-state difference; and
4. a later `spread` has converted that facilitator difference into an output difference.

Before step `d+3`, the output can depend on selector position and target occupancy, but every profile begins with the same selector, facilitator, and target state, and no mode-dependent facilitator difference has yet been converted back into target occupancy.

Therefore all profile traces agree through horizon `d+2`.

The word `w_i` has length `d+3` and distinguishes profiles differing at coordinate `i`, by Theorem 1. Hence the bound is exact. `□`

The logarithmic selector term is ordinary addressing substrate. The new ecological content is the irreducible three-action alternating cycle required to convert latent interaction mode into later accessibility.

---

## 7. Theorem — breaking either feedback arrow collapses the rank

The family admits two precise ablations.

### Ablation A — mode-blind turnover

Keep

\[
t_i\leftarrow0
\]

under turnover but never let `m_i` change `f_i`.

### Ablation B — accessibility-blind spread

Turnover may still make `f_i` depend on `m_i`, but define later spread by

\[
t_i\leftarrow1
\]

at the selected active gate, independent of `f_i`.

### Theorem 3 — cycle necessity

For every `r>=1`, if either ablation is applied, every latent profile has the same output trace under **every** action word. Hence

\[
\boxed{|P_{\rm ablated}(D_r)|=1,\qquad K_{\rm ablated}(D_r)=0.}
\]

Together with Theorem 1,

\[
\boxed{
K(D_r)=
\begin{cases}
r,&\text{both feedback arrows present},\\
0,&\text{either arrow removed}.
\end{cases}
}
\]

### Proof for Ablation A

The immutable `m_i` coordinates no longer appear in any transition or output rule. Two canonical initial states differing only in `m` therefore have identical selector, facilitator, and target states at time zero and receive identical successors after every action by induction on word length. Their output traces are identical for every word. `□`

### Proof for Ablation B

Mode-dependent turnover may produce different hidden facilitator states, but target/selector evolution no longer depends on facilitator state: addressing is mode-independent, `turnover` clears occupied targets independently of the mode value, and every later `spread` sets the selected target to one regardless of `f_i`.

Thus the projection onto `(selector, target occupancies)` has identical dynamics for every latent profile and the output factors through that projection. Again all mode profiles have identical traces for every word. `□`

This exact `r -> 0` collapse is the key structural result of the family. The memory burden is not caused by merely carrying `r` hidden bits in the physical state. Those bits become causal interface information only when the two ecological arrows form a closed feedback path into the future observable.

---

## 8. Why this is not the existing static-reachability theorem

If the mode-dependent turnover arrow is removed, the accessibility gates remain permanently open. The system reduces to a fixed accessibility structure and the hidden modes disappear from all responses.

The full theorem therefore cannot be reproduced by current static directed distance alone: the relevant edge state is **rewritten by the ecological dynamics**.

Likewise, the first `spread` and `turnover` traces agree across mode profiles. A one-step downstream hazard/turnover label is not enough. The distinction is exposed only after the changed facilitator state is fed back into a later movement event.

---

## 9. Why this is not merely the earlier cross-guild hazard theorem

A hidden mode can change facilitator survival under turnover, but that alone does not create response memory: Ablation B leaves the mode-dependent facilitator change in place while making spread accessibility independent of the facilitator, and the exact mode memory still collapses to zero.

Thus the theorem requires the hazard/interactor effect to alter a state that is subsequently used by movement/accessibility. A one-way hidden-tail effect on one downstream transition is insufficient in this family.

---

## 10. Relation to generic addressability

The proof of Theorem 1 ends with an injection, as every exact lower bound ultimately must. We do **not** claim that pairwise decoding or response-quotient injection is new.

The strengthening relative to a bare addressability assumption is that the decoder words are **derived from one explicit ecological feedback mechanism** and disappear under either causal-arrow ablation:

\[
\text{mode}
\to
\text{turnover change}
\to
\text{accessibility change}
\to
\text{future occupancy response}.
\]

So the theorem identifies a structural source of addressability rather than assuming an arbitrary bank of readable hidden bits.

Historical novelty still requires a separate literature comparison and is not decided here.

---

## 11. Executable certificate

`causal_model.feedback_gate_rank` provides:

- fixed-length gate addresses and the constant primitive alphabet;
- exact feedback-gate microstate transitions;
- canonical query words `addr(i) + spread + turnover + spread`;
- query decoding of every hidden mode coordinate;
- current visible-summary equality across all profiles;
- the exact memory formula `r` with full feedback and `0` under either ablation;
- the exact first separating horizon `ceil(log2(r)) + 3`; and
- `FeedbackGateRankCertificate`.

The tests exhaustively replay all profiles through small ranks, brute-force all action words through the pre-separation horizon for ranks up to four, and brute-force both ablations over a longer finite horizon. Those finite replays are regression/falsification checks; the proofs above establish the all-`r`, all-word claims.

---

## 12. Scope and remaining active problem

This result closes the first half of `HYP-I04`: the five-state benchmark is not isolated. Endogenous accessibility feedback supports an arbitrarily large exact hidden-mode rank even when the current ecological graph and current visible summaries are identical.

It does **not** yet provide the desired complete portability theory for general feedback networks. In particular, still open is a positive structural theorem giving a system-size-independent interaction-closed macrostate under a nontrivial class of growing state-dependent graphs.

The next proof target should therefore be **positive feedback portability**, not a second lower-bound witness and not another special-case codebook.
