# Witnessed boundary evidence: lower bounds, coverage, and the completion no-go

## Why this theorem is needed

The canonical boundary blanket gives the smallest exact summary of all exterior
completions under a declared response grammar. In an application, however, one
does not begin with all completions and all response cells in hand. One has a
finite collection of sampled exterior conditions and a finite collection of
tested interventions or observations.

That creates a fundamental asymmetry:

\[
\boxed{
\text{finite response evidence can force a lower bound on boundary complexity,}
}
\]

but, without an explicit coverage argument,

\[
\boxed{
\text{it cannot prove that no additional boundary response types remain.}
}
\]

This document makes both statements exact.

## Setup

Let \(I\) be window states, \(E\) exterior completions, \(\Gamma\) a declared
boundary-word grammar, and

\[
R(i,e,w)
\]

the deterministic window response. The canonical exterior response equivalence
is

\[
e\equiv_\Gamma e'
\quad\Longleftrightarrow\quad
\forall i\in I,\ \forall w\in\Gamma,
R(i,e,w)=R(i,e',w),
\]

and the canonical blanket is

\[
B_\Gamma=E/\!\equiv_\Gamma.
\]

Now let \(C\subseteq E\) be sampled exterior completions and let

\[
P\subseteq I\times\Gamma
\]

be a finite tested panel. The observed signature is

\[
\sigma_P(e)=\bigl(R(i,e,w)\bigr)_{(i,w)\in P}.
\]

Define the observed response-class count

\[
L_P(C)=\left|\{\sigma_P(e):e\in C\}\right|.
\]

## Theorem 1 — Witnessed lower bound

For every sampled completion set \(C\) and tested panel \(P\),

\[
\boxed{
L_P(C)\le |B_\Gamma|.
}
\]

Consequently,

\[
\boxed{
\log_2 L_P(C)
\le
\log_2|B_\Gamma|
}
\]

is an exact evidence-backed lower bound on exterior boundary complexity.

### Proof

If two sampled completions belong to the same canonical blanket class, then they
agree for every \(i\in I\) and \(w\in\Gamma\). In particular, they agree on the
restricted panel \(P\). Thus every observed-signature class is a union of
canonical classes restricted to the sample. A coarser partition cannot have more
blocks than the finer canonical partition, proving the inequality. \(\square\)

The certificate does not merely count blocks. For every pair of distinct observed
signature classes it stores a concrete cell

\[
(i,w)\in P
\]

where the representative responses differ. Therefore a reported lower bound can
be audited as a list of actual separating observations or interventions.

## Corollary — Evidence monotonicity

Suppose samples and tested cells grow monotonically:

\[
C_0\subseteq C_1\subseteq\cdots,
\qquad
P_0\subseteq P_1\subseteq\cdots.
\]

Then

\[
\boxed{
L_{P_0}(C_0)
\le L_{P_1}(C_1)
\le\cdots
\le |B_\Gamma|.
}
\]

No newly sampled completion or new tested response cell can invalidate an old
lower bound. It may leave the bound unchanged, or it may reveal a new response
type and increase it.

This is a statement about exact deterministic signatures. It is not a claim that
noisy observed class counts should be treated as exact without an error model.

## Theorem 2 — When finite evidence becomes exact

Finite evidence proves the exact canonical blanket cardinality only under two
separate contracts.

### Completion coverage

The sample contains at least one completion from every canonical class:

\[
\{[e]_\Gamma:e\in C\}=B_\Gamma.
\]

### Grammar coverage

The tested panel includes the entire declared response product:

\[
P=I\times\Gamma.
\]

Under both contracts,

\[
\boxed{
L_{I\times\Gamma}(C)=|B_\Gamma|.
}
\]

### Proof

Grammar coverage makes the observed signature identical to the canonical
response signature. Completion coverage makes the sample hit every canonical
class. Thus the observed signatures enumerate all and only the canonical classes.
\(\square\)

The important point is epistemic: a large sample is not automatically completion
coverage. Coverage is an additional biological, physical, or model-theoretic
claim that must itself be justified.

## Theorem 3 — Free-completion extension no-go

Let a finite transcript be defined by sampled completions \(C\), tested panel
\(P\), and a baseline completion \(e_0\in C\). For any integer \(r\ge1\), there
is a finite extension with:

- new completions \(e_1^\star,\ldots,e_r^\star\);
- fresh boundary words \(u_1,\ldots,u_r\); and
- binary responses on the fresh words,

such that

\[
R'(i,e_j^\star,w)=R(i,e_0,w)
\quad
\text{for every }(i,w)\in P,
\]

while

\[
R'(i_0,e_j^\star,u_j)=1,
\qquad
R'(i_0,e_k^\star,u_j)=0\quad(k\ne j),
\]

for one fixed inside state \(i_0\). All old transcript values remain unchanged.

The new completions are pairwise response-distinct and distinct from every old
completion. If the old blanket has size \(|B|\), the extended one has size

\[
\boxed{|B'|=|B|+r.}
\]

### Consequence

No rule that sees only the original finite transcript can provide a finite
universal upper bound on boundary complexity over a model class that admits this
kind of exterior-completion and grammar extension.

This is not a contradiction with the exactness theorem. The no-go applies when
completion/grammar coverage has **not** been declared. Once all admissible
completions and all admissible words are fixed and covered, the free extension is
outside the model class.

## The three report types

The theorem yields a clean reporting discipline.

### 1. Witnessed lower-bound report

> Under the tested panel \(P\), the sampled completions force at least \(k\)
> response-distinct exterior regimes.

Mathematically:

\[
|B_\Gamma|\ge k.
\]

This is the default honest conclusion from finite evidence.

### 2. Exact covered-blanket report

> Under the declared exhaustive completion and grammar coverage contract, the
> canonical blanket has exactly \(k\) regimes.

Mathematically:

\[
|B_\Gamma|=k.
\]

This needs an explicit coverage certificate.

### 3. Unresolved-open report

> The current transcript has lower bound \(k\), but no completion/grammar
> coverage contract; larger compatible open blankets remain possible.

This is not failure. It is the correct scientific state of knowledge.

## Ecological projection

A field survey, manipulative assay, camera protocol, or plot experiment can
support statements such as:

> Across the declared tested contexts, the observed source populations / delayed
> states / unmeasured interaction regimes already require at least \(k\)
> distinct boundary response types.

It cannot convert that sentence into “there are exactly \(k\) outside regimes”
merely by observing no novelty in the current finite sample. Exact closure needs
an independent contract that all relevant dispersal sources, seasonal delays,
rare interactions, and permitted future perturbations have been covered.

\[
\boxed{
\text{Evidence accumulates sound lower bounds.}
\quad
\text{Closure needs a coverage proof.}
}
\]

## Executable certificates

`causal_model.witnessed_boundary_evidence` provides:

- `WitnessedBoundaryLowerBoundCertificate` with a separating response witness
  for every observed class pair;
- `EvidenceChainCertificate` for nested samples/panels;
- `CompletionCoverageCertificate` for exactness under explicit coverage; and
- `FreeCompletionExtensionCertificate` for the finite transcript-preserving
  extension construction.

The GitHub Action performs deterministic finite certificate replay. It does not
turn finite replay into a proof about unlisted ecological possibilities or an
infinite grammar.