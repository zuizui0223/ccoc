# Causal closure calculus: local rules need not close worlds

## Question

A complex system may have a perfectly specified local update rule

\[
x_{t+1}=F(x_t)
\]

while failing to converge to one stable world-level outcome. This module makes
that distinction exact for finite deterministic systems.

The target is not whether a local transition is valid. The target is whether
repeated application of the transition **closes**:

\[
\forall x\in S,\quad F^t(x)\to x^\star.
\]

## Finite theorem domain

Let \(S\) be a non-empty finite set and let \(F:S\to S\) be a total
 deterministic map. Every orbit eventually enters a directed cycle. Therefore
exactly one of the following holds:

1. **Global closure.** There is one singleton cycle \(\{x^\star\}\), and every
   state reaches it.
2. **Recurrent non-closure.** At least one directed cycle has period \(p\ge2\).
3. **Multistable non-closure.** There are at least two singleton cycles and no
   nontrivial cycle.

The three classes are mutually exclusive and exhaustive in this finite domain.

## Global closure certificate

A `GlobalClosureCertificate` contains a candidate attractor \(x^\star\) and an
integer ranking

\[
V:S\to\{0,1,2,\ldots\}
\]

such that

\[
F(x^\star)=x^\star,\qquad V(x^\star)=0,
\]

and for every \(x\ne x^\star\),

\[
V(F(x))<V(x).
\]

### Theorem

If this certificate verifies, every trajectory reaches \(x^\star\) in at most
\(V(x)\) steps.

### Proof

For a trajectory beginning at \(x\ne x^\star\), the non-negative integer
\(V(x_t)\) strictly decreases at each step until the trajectory reaches
\(x^\star\). An infinite strict descent in non-negative integers is impossible.
Therefore it reaches the unique rank-zero state in finitely many steps. Since
that state is fixed, it remains there forever. \(\square\)

The certificate is a finite discrete Lyapunov function. It proves closure; it
does not merely observe a long simulation that appears to settle.

## Recurrent non-closure certificate

A `RecurrentCycleCertificate` contains pairwise distinct states

\[
x_0,\ldots,x_{p-1},\qquad p\ge2,
\]

with

\[
F(x_i)=x_{(i+1)\bmod p}.
\]

### Theorem

If this certificate verifies, no globally attracting singleton fixed point
exists for the full state space.

### Proof

The trajectory starting at \(x_0\) visits the distinct period-\(p\) orbit
forever. It cannot converge to a singleton fixed point. \(\square\)

This is the formal version of **local truth / global non-closure**: every edge
of the local rule is correct, but the rule system does not produce one stable
world-level outcome.

## Multistability certificate

Two distinct fixed points \(x\ne y\) with

\[
F(x)=x,\qquad F(y)=y
\]

certify failure of one-point global closure. Unlike recurrent non-closure, this
case has no periodic oscillation: the long-run result depends on the initial
basin.

## Why the distinction matters

A statement that a local mechanism holds is weaker than a statement that the
same mechanism yields a stable, transferable macroscopic rule. The finite
calculus separates:

| Exact result | What it does establish | What it does not establish |
|---|---|---|
| Global closure | every declared state reaches one attractor | robustness to unmodelled states or stochastic forcing |
| Recurrent non-closure | a genuine repeatable cycle prevents one-point closure | chaos, random noise, or all possible cycles |
| Multistability | initial conditions can select different fixed outcomes | a nontrivial cycle |

## GitHub Actions theorem regression

`.github/workflows/causal-closure-theorem.yml` runs two checks on every relevant
pull request and on `main`:

1. targeted certificate tests; and
2. exhaustive enumeration of every labelled total deterministic map on one to
   four states:

\[
1^1+2^2+3^3+4^4=288.
\]

For each map, the workflow constructs and verifies its certificate, records the
classification, and uploads a JSON report. This is an executable finite-model
check of the stated theorem domain. It is not a substitute for a proof assistant
or a proof for arbitrary continuous, infinite-state, or stochastic systems.

## Next mathematical extension

The next nontrivial question is not to add more simulation. It is to extend the
certificate language to a restricted class of rational stochastic systems and
distinguish:

\[
\text{contraction to a stationary distribution},
\quad
\text{deterministic recurrence},
\quad
\text{and stochastic recurrent sign reversal}.
\]

That extension needs a new theorem and explicit assumptions; it should not be
inferred from the finite deterministic result here.
