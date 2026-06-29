# Symbolic candidate-set lifting over continuous and infinite spaces

## Aim

The finite RACH API enumerates a declared candidate universe. That is useful for
small auditable model classes, but neither the confidence-set lifting proof nor
the anytime extension fundamentally requires a finite candidate space.

This module extends RACH to an arbitrary candidate space \(\Theta\), including:

- a continuous parameter region such as \(\Theta\subseteq\mathbb R^d\);
- a countably infinite grammar or program family;
- a mixed discrete/continuous domain;
- a SAT/SMT/constraint-programming feasible set; or
- any implicit domain for which an external backend can answer feasibility
  queries.

RACH never enumerates \(\Theta\). It asks only whether a retained candidate set
contains an active or inactive witness for each declared motif.

## Symbolic retained sets

For a robustness cell \(r\), let \(C_r(Z)\subseteq\Theta\) be the retained
candidate set supplied by an external statistical procedure. For a Boolean motif
predicate \(m:\Theta\to\{0,1\}\), RACH requires three feasibility queries:

\[
\begin{aligned}
Q^0_r &: \exists\theta\in C_r(Z),\\
Q^+_{r,m} &: \exists\theta\in C_r(Z): m(\theta)=1,\\
Q^-_{r,m} &: \exists\theta\in C_r(Z): m(\theta)=0.
\end{aligned}
\]

A solver may report:

```text
SAT      a witness/model/feasible point exists
UNSAT    the queried set is empty, supported by a proof or certificate
UNKNOWN  the backend did not establish either statement
```

The classification rule is deliberately one-sided and conservative.

| Solver facts in a non-empty cell | RACH cell status |
|---|---|
| \(Q^-_{r,m}\) is certified `UNSAT` | `INVARIANT` |
| \(Q^+_{r,m}\) is certified `UNSAT` | `EXCLUDED` |
| both \(Q^+_{r,m}\) and \(Q^-_{r,m}\) are certified `SAT` | `UNRESOLVED` |
| any required feasibility fact is `UNKNOWN`, or the retained set is not certified non-empty | `UNSUPPORTED` |

A solver timeout is not empirical disagreement. It must not be silently
relabelled `UNRESOLVED`, because that would hide the difference between
"both motif values are feasible" and "we did not establish which values are
feasible."

## Continuous example

Let \(\Theta=\mathbb R\), and let the motif be

\[
m(\theta)=\mathbb 1\{\theta>0\}.
\]

For a retained interval \(C=[0.2,1]\):

```text
C is non-empty                         SAT
C ∩ {theta > 0} is non-empty           SAT
C ∩ {theta <= 0} is empty              UNSAT
```

RACH reports `INVARIANT` for `positive` without ever enumerating real numbers.
For \(C=[-1,1]\), both motif-restricted sets are `SAT`, so RACH reports
`UNRESOLVED`. If the backend cannot decide whether \(C\cap\{\theta\le0\}\)
is empty, the result is `UNSUPPORTED`, not an overconfident invariant.

## Theorem: symbolic candidate-set lifting

Let \(\theta^\star\in\Theta\) be the true candidate, with \(\Theta\) any
set; no finiteness, countability, topology, or probability distribution on
\(\Theta\) is required by the lifting step.

Assume the external statistical procedure gives

\[
\Pr\left[
  \theta^\star\in\bigcap_{r\in\mathcal R}C_r(Z)
\right]\ge 1-\alpha.
\]

Also assume the solver's decisive `SAT`/`UNSAT` statements used by RACH are
semantically valid jointly with probability at least \(1-\beta\). The two
failure events may be arbitrarily dependent.

Then

\[
\Pr\left[
  \text{any false RACH INVARIANT or EXCLUDED conclusion}
\right]
\le \min(1,\alpha+\beta).
\]

### Proof

Let \(E\) be the event that the true candidate belongs to every required
retained set, and \(S\) the event that every decisive solver certificate has its
advertised semantics.

On \(E\cap S\), a false `INVARIANT` for a motif absent from
\(\theta^\star\) is impossible: \(\theta^\star\in C_r\) witnesses the
motif-inactive query in every required cell, contradicting a sound `UNSAT`
certificate for that query. The argument for a false `EXCLUDED` is symmetric.
Thus

\[
\{\text{any false decisive RACH conclusion}\}\subseteq E^c\cup S^c.
\]

The union bound gives

\[
\Pr(E^c\cup S^c)\le\alpha+\beta.
\]

No independence assumption is used. If solver certificates are deterministic
and proof-carrying under a trusted verifier, set \(\beta=0\), recovering the
ordinary confidence-set lifting guarantee.

## What this theorem does not solve

The theorem does not show that a chosen solver is correct, that a candidate
encoding represents nature, or that a continuous feasible region can be solved
in finite time. It separates three obligations that are often conflated:

1. **Statistical coverage:** does the external procedure retain the true
   candidate with the claimed probability?
2. **Solver semantic validity:** are the decisive `SAT`/`UNSAT` answers valid
   for the encoded constraints?
3. **Candidate-universe coverage:** does \(\Theta\) contain a faithful
   representation of the true mechanism at all?

RACH lifts the first two into a false-decisive bound, conditional on the third.
It cannot repair an omitted mechanism or turn `UNKNOWN` into information.

## Relation to existing RACH layers

| Layer | Candidate representation | Observation / solver assumptions |
|---|---|---|
| Finite Boolean theorem | explicit switch assignments | hard observations |
| Finite noisy-program layer | enumerated finite programs and states | declared binary likelihood |
| Confidence-set lifting | finite candidate IDs | external set coverage |
| Anytime lifting | finite candidate IDs across looks | external all-look coverage |
| **Symbolic candidate-set lifting** | arbitrary implicit \(\Theta\) | external retained-set coverage plus solver validity |

The new layer is not a raw-data adapter. A future SMT, interval, semialgebraic,
or optimization backend must produce `FeasibilityCertificate` objects and state
its own proof or error guarantees.

## Code mapping

| Mathematical object | API |
|---|---|
| Arbitrary \(\Theta\) and motif vocabulary | `SymbolicCandidateSpace` |
| `SAT` / `UNSAT` / `UNKNOWN` feasibility answer | `FeasibilityCertificate` |
| \(Q^0_r,Q^+_{r,m},Q^-_{r,m}\) | `SymbolicMotifQueries` |
| Symbolic retained set \(C_r\) | `SymbolicConfidenceSetCell` |
| Symbolic RACH classification | `classify_symbolic_candidate_sets` |
| Statistical coverage event | `SymbolicJointCoverageCertificate` |
| Solver semantic validity event | `SolverSemanticValidityCertificate` |
| Combined \(\alpha+\beta\) guarantee | `symbolic_soundness_guarantee` |
