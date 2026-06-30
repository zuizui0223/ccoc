# Exact rational polyhedral inclusion verifier

## Purpose

The symbolic outer-envelope theorems use an inclusion-validity risk
\(\gamma\) for the claim

\[
C^{\mathrm{inner}}_r \subseteq C^{\mathrm{outer}}_r.
\]

This module gives the first concrete proof-carrying route to \(\gamma=0\):
exact inclusion of non-empty rational polyhedra. It verifies certificates but
does not search for them.

## Representation

An inner retained set and outer envelope are finite conjunctions of non-strict
rational linear inequalities:

\[
P_{\mathrm{inner}}=\{x:Ax\le b\},
\qquad
P_{\mathrm{outer}}=\{x:Cx\le d\}.
\]

All values use exact `Fraction` arithmetic. Integers and strings such as
`"-1/5"` are accepted; binary floating point is rejected.

The inner and outer systems must use the identical ordered variable vocabulary.
Equalities require two inequalities. Strict inequalities, disjunctions,
integrality, nonlinear constraints, and solver search are outside this verifier.

## Non-vacuity

Set inclusion of an empty inner set is mathematically true, but it is not a
useful RACH extension-stability witness. Every proof therefore includes an exact
rational point \(x_0\in P_{\mathrm{inner}}\), checked directly against every
inner row.

## Farkas implication certificate

For every outer inequality

\[
c_j^\top x\le d_j,
\]

the proof provides non-negative multipliers \(\lambda_j\ge0\) over the inner
rows such that

\[
\lambda_j^\top A=c_j^\top,
\qquad
\lambda_j^\top b\le d_j.
\]

For every \(x\) satisfying \(Ax\le b\), non-negativity gives

\[
c_j^\top x
=\lambda_j^\top Ax
\le\lambda_j^\top b
\le d_j.
\]

Thus every outer row follows from the inner system, and
\(P_{\mathrm{inner}}\subseteq P_{\mathrm{outer}}\). The verifier checks every
multiplier sign, coefficient equality, and bound comparison exactly.

### One-dimensional example

For

\[
1/5\le x\le1
\]

inside

\[
0\le x\le2,
\]

the inner rows are \(-x\le-1/5\) and \(x\le1\). The outer row
\(-x\le0\) uses multipliers \((1,0)\), while \(x\le2\) uses \((0,1)\).
Both are non-negative exact certificates.

## Static and sequential adapters

`verify_exact_rational_joint_inclusion` verifies one proof per required cell and
returns a `JointSymbolicInclusionCertificate` with

\[
\gamma=0.
\]

`verify_exact_rational_finite_look_inclusion` verifies one such collection at
each predeclared finite look and returns an
`AnytimeJointSymbolicInclusionCertificate` with lower bound one and exactly that
finite look scope.

A finite bundle for looks \(1,\ldots,T\) does **not** certify all positive
integer looks. An all-look \(\gamma=0\) result needs a separate parametric proof
schema or a verified invariant that covers every future look.

## Link to RACH guarantees

With exact outer solver certificates and exact polyhedral inclusion certificates,

\[
\beta=\gamma=0.
\]

The static symbolic extension bound becomes

\[
P(\text{false decisive outer conclusion or invalid stability})\le\alpha,
\]

and the same reduction applies to the anytime outer-envelope theorem over its
certified finite scope.

## Trust boundary

The result is conditional on the trusted rational parser, verifier code, and the
claim that supplied linear systems correctly encode the intended candidate sets.
It does not establish statistical retained-set coverage, generate a Farkas
certificate, prove that the outer envelope contains nature, or validate a
scientific motif encoding.
