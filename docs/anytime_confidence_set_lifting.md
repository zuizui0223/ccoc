# Anytime confidence-set lifting theorem

## Aim

The ordinary confidence-set lifting theorem controls false decisive RACH
conclusions at a declared analysis point. This extension controls them when an
analyst may inspect results repeatedly and stop after seeing the evolving
candidate sets.

RACH still does not analyse raw data. An external sequential method produces
candidate sets at information times, and separately proves a simultaneous-over-
time coverage statement. RACH lifts that statement into a guarantee over:

- every certified analysis look;
- every declared causal motif; and
- every data-dependent stopping rule whose selected look lies in the certified
  scope.

## Setup

Let:

- \(\Theta\) be a finite predeclared candidate universe;
- \(M(\theta)\subseteq\mathcal M\) be the motifs active in candidate
  \(\theta\);
- \(Z_1,Z_2,\ldots\) be an arbitrary evolving random data object, with any
  dependence, dimension, sampling scheme, or randomisation allowed by the
  external procedure;
- \(\mathcal R\) be a fixed set of required robustness cells;
- \(\mathcal T\) be either a fixed finite schedule of looks or all positive
  integer looks; and
- \(C_{r,t}(Z_{1:t})\subseteq\Theta\) be a retained candidate set for required
  cell \(r\) at look \(t\).

RACH applies its ordinary within-look classification to
\(\{C_{r,t}:r\in\mathcal R\}\). For a motif \(m\), each look yields one of
`INVARIANT`, `EXCLUDED`, `UNRESOLVED`, or `UNSUPPORTED`.

The candidate universe, motif map, and required cell IDs are fixed across
looks. A changing set of required cells is not silently accepted: it requires a
new certificate covering the changed inferential target.

## Theorem: anytime confidence-set lifting

Assume \(\theta^\star\in\Theta\) is the true candidate and an external
sequential procedure establishes

\[
\Pr\left[
  \forall t\in\mathcal T,\;
  \theta^\star\in\bigcap_{r\in\mathcal R} C_{r,t}(Z_{1:t})
\right]\ge 1-\alpha.
\]

Then

\[
\Pr\left[
\exists t\in\mathcal T,\exists m\in\mathcal M:
\begin{array}{l}
 m\notin M(\theta^\star)\ \text{and RACH}_t(m)=\mathrm{INVARIANT},\\
 \text{or}\\
 m\in M(\theta^\star)\ \text{and RACH}_t(m)=\mathrm{EXCLUDED}
\end{array}
\right]\le\alpha.
\]

Consequently, for any stopping time \(\tau\) taking values in
\(\mathcal T\),

\[
\Pr\left[
\exists m\in\mathcal M:\ \text{RACH}_{\tau}(m)\ \text{is false decisive}
\right]\le\alpha.
\]

The last statement actually follows for any data-dependent selected look in the
certified scope, because its false-decisive event is contained in the union over
all certified looks. Calling \(\tau\) a stopping time is the usual sequential
interpretation; the RACH set-inclusion step itself adds no filtration or
independence assumption.

### Proof

For one realized trajectory, suppose the true candidate belongs to every
required set at every certified look. At a fixed look \(t\), an `INVARIANT`
claim for a motif absent from \(\theta^\star\) is impossible because
\(\theta^\star\) is a retained candidate without that motif. Similarly, an
`EXCLUDED` claim for a motif active in \(\theta^\star\) is impossible because
\(\theta^\star\) is retained with that motif.

Thus, at each look,

\[
\{\text{false decisive conclusion at }t\}
\subseteq
\left\{
\theta^\star\notin\bigcap_{r\in\mathcal R} C_{r,t}
\right\}.
\]

Taking a union over \(t\in\mathcal T\) gives

\[
\{\text{false decisive conclusion at any certified look}\}
\subseteq
\left\{
\exists t\in\mathcal T:\
\theta^\star\notin\bigcap_{r\in\mathcal R} C_{r,t}
\right\}.
\]

The asserted simultaneous coverage inequality bounds the probability of the
right-hand event by \(\alpha\). No condition on the form of the data process is
introduced in this proof.

## Why repeated fixed-time analyses are insufficient

A coverage statement valid only at each individual look,

\[
\Pr\left[\theta^\star\in\bigcap_r C_{r,t}\right]\ge1-\alpha
\quad\text{for each fixed }t,
\]

does **not** automatically imply the time-uniform theorem. Repeated peeking can
accumulate miscoverage across looks. The external procedure must instead give
one statement that simultaneously covers the entire schedule, for example:

```text
finite predeclared schedule: a jointly valid or alpha-spending construction
all positive integer looks: an anytime-valid confidence sequence / confidence set
```

RACH records that certificate; it does not convert fixed-time intervals into a
sequential guarantee on its own.

## Scope and limits

The theorem is conditional on three distinct ingredients:

1. **Statistical time-uniform coverage.** The external method genuinely covers
   the true candidate across every declared required cell and every certified
   look with probability at least \(1-\alpha\).
2. **Candidate-universe coverage.** The true mechanism is represented by a
   candidate in \(\Theta\). A time-uniform set cannot repair an omitted
   mechanism.
3. **Stable inferential target.** The motif vocabulary and required cell IDs do
   not change after inspecting the sequence. A changed target needs a certificate
   for the changed target.

The theorem guarantees soundness, not power. A weak external confidence sequence
may retain many candidates forever, producing `UNRESOLVED`. That outcome is the
correct response when the data have not separated the candidates.

## Relation to the non-sequential theorem

The non-sequential theorem is recovered by setting \(\mathcal T=\{t_0\}\).
The exact binary observation-envelope module is an even narrower finite special
case: it specifies a binomial observation model and enumerates all outcomes.

The anytime theorem is more general in data type but not stronger than its
external certificate. It does not provide an e-process, confidence sequence,
martingale proof, or raw-data adapter. Those are separate projects and must
state their own assumptions.

## Code mapping

| Mathematical object | API |
|---|---|
| Snapshot \(\{C_{r,t}\}_r\) | `SequentialConfidenceSetSnapshot` |
| External all-look coverage statement | `AnytimeJointCoverageCertificate` |
| Pointwise all-look inclusion check | `deterministic_anytime_lifting_witness` |
| Time-uniform and stopping-time error bound | `anytime_soundness_guarantee_from_coverage` |

The implementation rejects trajectories whose required cell IDs change across
looks or whose look index lies outside a finite certificate scope. It does not
accept raw data or pretend to validate an external coverage claim.
