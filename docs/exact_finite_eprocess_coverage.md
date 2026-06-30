# Exact finite-alphabet e-process coverage

## The mathematical principle

This module is the first concrete backend for RACH's proof-carrying all-look
coverage contract. It turns a finite hypothesis universe into nested,
optional-stopping-safe retained sets.

Let \(\Theta\) be a finite candidate set. For every required cell \(r\), let
\(X_{r,1},X_{r,2},\ldots\) take values in a finite alphabet \(\mathcal X_r\).
Under candidate \(\theta\), the declared stationary channel law is

\[
p_{r,\theta}(x)>0,
\qquad
\sum_{x\in\mathcal X_r}p_{r,\theta}(x)=1.
\]

Before observing the stream, choose an alternative PMF \(q_r\) and a cellwise
error budget \(\alpha_r\). Define

\[
E_{r,\theta,t}
=
\prod_{i=1}^{t}
\frac{q_r(X_{r,i})}{p_{r,\theta}(X_{r,i})}.
\]

The local identity is exact:

\[
\mathbb E_\theta\left[
\frac{q_r(X_{r,t})}{p_{r,\theta}(X_{r,t})}
\middle|
\mathcal F_{t-1}
\right]
=
\sum_xp_{r,\theta}(x)\frac{q_r(x)}{p_{r,\theta}(x)
=1.
\]

Thus \(E_{r,\theta,t}\) is a nonnegative martingale under candidate
\(\theta\). Ville's inequality gives

\[
\Pr_\theta\left[
\sup_{t\ge1}E_{r,\theta,t}\ge \frac1{\alpha_r}
\right]
\le \alpha_r.
\]

## Candidate recovery rule

RACH needs retained sets, not a forced single winner. The backend retains
candidate \(\theta\) in cell \(r\) at look \(t\) exactly when

\[
\max_{s\le t}E_{r,\theta,s}<\frac1{\alpha_r}.
\]

Using the running maximum has two consequences:

1. retained candidate sets are nested decreasing over time; and
2. exclusion is irreversible and carries a precise crossing witness.

A retained candidate is **not confirmed**. It is only not yet contradicted by
its declared observation channel at the allocated error budget. Several
observationally indistinguishable candidates may remain retained indefinitely;
that is the correct `UNRESOLVED` behavior, not a defect.

## Why the budget is over cells, not hypotheses

Suppose \(\theta^\star\) is the one true candidate. For its false exclusion,
only the e-process indexed by \(\theta^\star\) matters. Therefore no Bonferroni
factor for \(|\Theta|\) is required to retain the true candidate.

To retain it simultaneously in every required cell, apply the union bound:

\[
\Pr_{\theta^\star}\left[
\exists r,\exists t:\;
\theta^\star\notin C_{r,t}
\right]
\le \sum_{r\in\mathcal R}\alpha_r.
\]

No cross-cell independence is needed for this final inequality. The backend
therefore supplies the all-look coverage lower bound

\[
1-\sum_r\alpha_r.
\]

This is the **single-truth principle**: the number of competing hypotheses
affects power and computation, but not the family-wise coverage budget needed
to avoid excluding the one true hypothesis.

## Exact proof-carrying artifacts

Three strict canonical artifacts are generated:

```text
rach-exact-finite-observation-model/v1
rach-exact-finite-eprocess-encoder/v1
rach-exact-finite-eprocess-ville-proof/v1
```

They bind, respectively:

- finite alphabets and every candidate PMF;
- predeclared alternatives and cellwise error budgets; and
- model/encoder digests, theorem identity, and exact lower bound.

The method-specific verifier parses each artifact, rechecks every PMF sum and
strict positivity condition, recomputes every local martingale identity,
recomputes the aggregate error budget, and verifies all links to the coverage
contract.

## Relation to the RACH stack

The backend produces a genuine
`AnytimeSymbolicJointCoverageCertificate` with `certified_looks=None`, hence it
covers every positive integer look. It can then be put into the existing chain:

\[
\text{finite hypothesis / channel specification}
\to
\text{exact e-process coverage contract}
\to
\text{compiler and inclusion admission}
\to
\text{manifest / transcript / checkpoint}.
\]

This is still a restricted backend, not a claim that all data are finite or
stationary. The distribution-agnostic lifting theorem remains more general:
other data types can use different valid coverage procedures. This module proves
that at least one nontrivial sequential procedure can discharge the external
coverage premise exactly and auditably.

## Limits

The module assumes:

- the true mechanism belongs to the declared finite candidate universe;
- each cell has the declared stationary conditional PMF under that candidate;
- all candidate PMFs have strictly positive support on the declared alphabet;
- alternatives and error budgets are fixed before data; and
- the coverage procedure is evaluated at every claimed look.

It does not establish candidate-universe adequacy, learn a good alternative
PMF, handle continuous observations, or prove causal motif semantics. Those are
separate layers. The next natural extension is a predictable, history-dependent
mixture alternative while retaining a proof-carrying e-process certificate.

## API

| Task | API |
|---|---|
| Declare one candidate PMF | `ExactCandidatePMF` |
| Declare cells / hypothesis universe | `ExactFiniteObservationModel` |
| Declare alternatives and budgets | `ExactFiniteEProcessEncoder` |
| Compute nested retained sets | `exact_finite_eprocess_snapshots` |
| Audit a finite horizon exactly | `exact_finite_false_exclusion_probability_up_to_horizon` |
| Build concrete coverage contract package | `build_exact_finite_eprocess_coverage_package` |
| Verify model/encoder/proof contract | `ExactFiniteEProcessCoverageVerifier` |
