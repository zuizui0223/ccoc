# Bounded-type feedback portability theorem — 2026-08-14

> **Status:** analytic positive portability theorem for a delimited endogenous-accessibility class. This is the positive counterpart to the scalable feedback-gate rank theorem. It is not a universal classification of arbitrary feedback networks and it is not a historical novelty claim.

## 1. Why this theorem is needed

`feedback_gate_rank.py` proves the negative scalable direction: if `r` latent interaction modes are individually addressable through the alternating ecological cycle

\[
\mathsf{spread}\to\mathsf{turnover}\to\mathsf{spread},
\]

then all `2^r` mode profiles can become future-response distinct even though the current accessibility graph and current abundance/reachability summaries are identical.

That still leaves the positive portability question:

> Can an arbitrarily large physical feedback system have one fixed exact macro-law when the number of **response-distinct interaction types** stays bounded?

For the class below, yes. The exact macro size depends on the number of interaction types, not the number of physical gate copies.

---

## 2. One interaction type with arbitrary replication

Fix one interaction type with replication count

\[
n\ge1.
\]

Each physical copy `k=1,...,n` has

- facilitator/accessibility state \(f_k\in\{0,1\}\);
- target occupancy \(t_k\in\{0,1\}\).

The whole type shares one latent interaction mode

\[
m\in\{0,1\}.
\]

Copy identities are **not individually addressable**. The declared ecological grammar acts synchronously at type level.

### Spread

\[
\mathsf{spread}:
\qquad
t_k\leftarrow t_k\lor f_k
\quad\forall k.
\]

### Turnover

Turnover clears every occupied target. In the fragile mode `m=1`, each occupied facilitator is also removed:

\[
\mathsf{turnover}:
\qquad
t_k\leftarrow0,
\]

and for copies that were occupied,

\[
f_k\leftarrow0
\quad\text{if }m=1.
\]

The response is whether at least one target copy is occupied:

\[
Y=\mathbb 1\{\exists k:t_k=1\}.
\]

---

## 3. Reachable domain

The theorem starts from arbitrary target-empty states

\[
t=(0,\ldots,0)
\]

with arbitrary facilitator subset `f` and either mode.

From these starts, every reachable state satisfies one of two forms:

\[
t=0
\qquad\text{or}\qquad
t=f.
\]

### Proof

Initially `t=0`. A spread step sets every target to the current facilitator vector, so `t=f`. Repeated spread preserves that equality. Turnover sets `t=0`; in the fragile mode it may also set facilitator coordinates to zero, but the resulting target vector is still zero. Induction gives the invariant. `□`

For each mode there are `2^n` target-empty facilitator configurations and `2^n-1` nonempty occupied configurations. Hence the exact reachable microstate count is

\[
\boxed{
|X_n|=2^{n+2}-2.
}
\]

This grows exponentially with physical replication.

---

## 4. The five feedback macrostates

Define the following labels.

1. `empty-unreachable`:
   \[
   f=0,\ t=0.
   \]
   The mode is omitted because no future action can make it response-relevant once every facilitator is absent.

2. `ready-resilient`:
   \[
   m=0,\ f\ne0,\ t=0.
   \]

3. `ready-fragile`:
   \[
   m=1,\ f\ne0,\ t=0.
   \]

4. `occupied-resilient`:
   \[
   m=0,\ f\ne0,\ t=f.
   \]

5. `occupied-no-recovery`:
   \[
   m=1,\ f\ne0,\ t=f.
   \]

These are exactly the five qualitative states already suggested by the original five-state feedback triage witness. The present theorem proves that the same five labels remain exact for **arbitrary physical replication `n`**.

---

## 5. Theorem — exact five-state quotient independent of replication

### Theorem 1

For every replication count `n>=1`, the five labels above are the canonical exact future-response quotient on the reachable domain:

\[
\boxed{|P_n|=5.}
\]

The induced macro transition table is

| macrostate | `spread` | `turnover` | output |
|---|---|---|---:|
| empty-unreachable | empty-unreachable | empty-unreachable | 0 |
| ready-resilient | occupied-resilient | ready-resilient | 0 |
| ready-fragile | occupied-no-recovery | ready-fragile | 0 |
| occupied-resilient | occupied-resilient | ready-resilient | 1 |
| occupied-no-recovery | occupied-no-recovery | empty-unreachable | 1 |

The table contains no `n`.

### Proof of exactness

Take two microstates with the same five-state label.

- Their current outputs agree because output depends only on whether the label is occupied.
- `spread` sends every state in one label to the same destination label shown in the table. The exact facilitator subset does not matter; a nonempty subset remains nonempty and target occupancy becomes equal to that subset.
- `turnover` likewise sends every state in one label to the same destination label. In resilient states the nonempty facilitator subset survives; in fragile occupied states all currently facilitated/occupied copies are removed, yielding the empty label.

Thus output and both action successors factor through the five-state label. It is an exact dynamic interface.

### Proof of minimality

Every one of the five labels is realizable for every `n>=1` by choosing one nonzero facilitator copy.

They are pairwise future-distinguishable:

- occupied versus unoccupied labels differ in current output;
- `empty-unreachable` versus either ready state is separated by `spread`;
- `ready-resilient` versus `ready-fragile` is separated by
  \[
  \mathsf{spread}\;\mathsf{turnover}\;\mathsf{spread};
  \]
- `occupied-resilient` versus `occupied-no-recovery` is separated by
  \[
  \mathsf{turnover}\;\mathsf{spread}.
  \]

Therefore no two labels can be merged in any exact response interface. The five-state interface is canonical. `□`

---

## 6. Why the hidden mode disappears in the empty state

The merge

\[
(m=0,f=0,t=0)
\sim
(m=1,f=0,t=0)
\]

is not an approximation. Once facilitator state is zero, `spread` can never create occupancy and `turnover` changes nothing. The mode has no path back to the observable under the declared grammar.

This is the positive analogue of the feedback-cycle necessity result: hidden state matters only while a causal path remains from that hidden state through future accessibility to the response.

---

## 7. Multiple bounded interaction types

Now fix a finite number

\[
q\ge1
\]

of interaction types. Type `j` has arbitrary replication count

\[
n_j\ge1.
\]

Actions are type-specific but copy-anonymous:

\[
\mathsf{spread}:j,
\qquad
\mathsf{turnover}:j.
\]

The action alphabet therefore has size `2q`, independent of the replication vector.

The output is the `q`-vector of type-level target occupancies.

### Theorem 2 — exact product quotient

For every replication vector

\[
(n_1,\ldots,n_q),
\]

the canonical exact quotient has

\[
\boxed{|P|=5^q}
\]

states and is the Cartesian product of the one-type five-state quotients.

### Proof

The product label is exact because every type-specific action changes one coordinate according to the same five-state transition table while leaving all other coordinates fixed; the output vector also factors coordinatewise.

For minimality, take two unequal product labels. They differ in at least one type coordinate `j`. The one-type theorem supplies a finite distinguishing word over `spread:j` and `turnover:j` for those two local labels. Applying that same word to the product system changes only coordinate `j`, so the full output vectors differ. Thus every unequal product label is response-distinct. `□`

Hence exact macro memory is

\[
\boxed{
K_{\rm macro}=q\log_2 5.
}
\]

---

## 8. Theorem — changing-domain feedback portability

The reachable physical state count for one type is

\[
2^{n_j+2}-2.
\]

Therefore for `q` types,

\[
|X_{n_1,\ldots,n_q}|
=
\prod_{j=1}^q\left(2^{n_j+2}-2\right),
\]

which can grow without bound as any replication count grows.

Yet Theorem 2 gives the same macro domain

\[
\mathcal Q=\{1,\ldots,5\}^q
\]

and the same macro transition table for every replication vector.

### Theorem 3

For fixed interaction-type count `q`, arbitrary growth in the number of exchangeable physical gate copies admits one common exact macro-law with

\[
\boxed{5^q}
\]

states, independent of all replication counts.

This is true changing-semantic-domain portability: no state-by-state identification of microstates across different replication vectors is required. Every domain factors to the same five-state-per-type causal machine.

---

## 9. Positive/negative structural boundary

The positive theorem and the scalable feedback-rank theorem now expose one clean boundary.

### Bounded type rank / anonymous copies

If physical copies fall into a fixed number `q` of response-equivalent feedback types, share one mode per type, and the grammar acts only at type level, then arbitrary physical replication costs no additional exact macro memory:

\[
K=q\log_2 5.
\]

### Individually addressable feedback modes

If instead `r` gate modes remain independently distinguishable by addressed alternating feedback words, the current graph can still be identical across all profiles, but exact future-response memory grows as

\[
K=r.
\]

Thus raw system size or raw gate count is not the relevant quantity. The controlling quantity in these two exact classes is the number of **future-response-distinct feedback types/modes that the grammar can address**.

This is not yet a universal necessity theorem for every feedback network, but it is an exact positive/negative theorem pair in a nontrivial state-dependent-accessibility class.

---

## 10. Relation to earlier ecological packages

This theorem is not the abundance-saturation cap in different notation.

- The physical microstate is a set of facilitator identities plus target identities, and the number of reachable microstates grows exponentially with replication.
- The exact five-state macro is created by **type exchangeability and feedback closure**, not by truncating an abundance at a response threshold.
- The latent mode is retained only while it can influence future accessibility and is exactly forgotten after causal extinction of all facilitators.

It is also not static reachability: turnover can destroy the facilitator state that future spread uses.

---

## 11. Executable certificate

`causal_model.feedback_type_portability` provides:

- exact reachable one-type microdomains;
- the closed-form physical state count `2^(n+2)-2`;
- the five-state macro labeling and capacity-free transition table;
- shortest pairwise distinguishing words for the five macro states;
- type-level product actions and product macro transitions;
- physical-state and macro-state count formulas for arbitrary replication vectors; and
- `FeedbackTypePortabilityCertificate` for changing-domain families.

The tests exhaustively compute the canonical future-response quotient for one type through replication five and verify that it is exactly the declared five-state partition. They also exhaust all states of the smallest two-type product and verify coordinatewise macro closure. Those finite checks support, but do not replace, the all-`n` and all-`q` proofs above.

---

## 12. Status of HYP-I04 after the pair of theorems

The feedback program now has both scalable directions:

1. **negative:** independently addressable hidden feedback modes force an exact `r`-bit burden while current graph/summaries remain fixed;
2. **positive:** a fixed number `q` of copy-anonymous feedback types has one exact `5^q`-state macro across unbounded physical replication.

This substantially closes the original five-state-only gap. What remains open is a broader characterization for arbitrary heterogeneous state-dependent graphs where feedback types may merge, split, or move between equivalence classes over time.

That broader classification should not be attempted by adding another witness. A next theorem would need a genuine structural invariant controlling when feedback-type rank itself stays bounded under network evolution.
