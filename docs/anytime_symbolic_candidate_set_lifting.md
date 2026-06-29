# Anytime symbolic candidate-set lifting

## Aim

This theorem joins the two broadest RACH layers:

1. **anytime confidence-set lifting** for arbitrary sequential random data; and
2. **symbolic candidate-set lifting** for candidate spaces that may be continuous,
   mixed, countably infinite, or uncountable.

It permits repeated inspection of solver-backed retained candidate sets and a
data-dependent stopping time, without requiring RACH to enumerate candidates,
read raw data, assume i.i.d. sampling, or trust an unverified solver result.

The central claim is conservative:

> An arbitrary-space, solver-backed RACH conclusion is optional-stopping safe
> only when both the statistical retained-set coverage and the semantic validity
> of decisive solver certificates hold uniformly over the certified look scope.

## Setup

Let:

- \(\Theta\) be any candidate space;
- \(m:\Theta\to\{0,1\}\) be each declared motif predicate;
- \(Z_1,Z_2,\ldots\) be an arbitrary evolving random data object;
- \(\mathcal R\) be a fixed set of required robustness cells;
- \(\mathcal T\) be either a fixed finite set of looks or all positive integer
  looks; and
- \(C_{r,t}(Z_{1:t})\subseteq\Theta\) be a symbolic retained set at cell \(r\)
  and look \(t\).

At each look, an external solver provides feasibility statements for

\[
C_{r,t},\qquad C_{r,t}\cap\{m=1\},\qquad C_{r,t}\cap\{m=0\}.
\]

RACH uses only solver-backed statements with the following meaning:

```text
non-empty + inactive subset UNSAT  -> INVARIANT
non-empty + active subset UNSAT    -> EXCLUDED
active and inactive subsets SAT    -> UNRESOLVED
needed query UNKNOWN               -> UNSUPPORTED
```

`UNKNOWN` is not disagreement. It means that the backend did not establish the
feasibility fact needed for a sound decisive conclusion.

## Two all-look obligations

The theorem requires two external statements over the same required-cell and
look target.

### Statistical coverage

For the true candidate \(\theta^\star\), an external set-valued procedure
establishes

\[
\Pr\left[
\forall t\in\mathcal T,\;
\theta^\star\in\bigcap_{r\in\mathcal R}C_{r,t}
\right]\ge1-\alpha.
\]

This may come from a confidence sequence, a jointly valid finite-look design,
an alpha-spending construction, or another method whose assumptions are stated
outside RACH.

### Solver semantic validity

An external proof or audit establishes that every decisive SAT/UNSAT certificate
used across all \(r\in\mathcal R\), all \(m\), and all \(t\in\mathcal T\) has
its advertised semantic meaning with probability at least \(1-\beta\).

A deterministic proof-carrying verifier, such as the exact rational linear
witness/Farkas verifier, may use \(\beta=0\), conditional on its trusted parser,
verifier, and constraint encoding. An approximate numerical solver, randomized
backend, or uncertified imported result must either supply an explicit nonzero
\(\beta\) or remain `UNKNOWN` for decisive purposes.

## Theorem

Assume both all-look statements above. Then

\[
\Pr\left[
\exists t\in\mathcal T,\exists m:
\begin{array}{l}
 m(\theta^\star)=0\ \text{and }\mathrm{RACH}_t(m)=\mathrm{INVARIANT},\\
 \text{or}\\
 m(\theta^\star)=1\ \text{and }\mathrm{RACH}_t(m)=\mathrm{EXCLUDED}
\end{array}
\right]
\le \min(1,\alpha+\beta).
\]

Consequently, for any data-dependent stopping time \(\tau\) that takes values
in \(\mathcal T\),

\[
\Pr\left[
\exists m:\ \mathrm{RACH}_{\tau}(m)\ \text{is false decisive}
\right]
\le \min(1,\alpha+\beta).
\]

No independence between the coverage event and solver-validity event is
required.

## Proof

Let

\[
E=\left\{
\forall t\in\mathcal T,\;
\theta^\star\in\bigcap_{r\in\mathcal R}C_{r,t}
\right\}
\]

be the all-look statistical retention event, and let \(S\) be the event that
all decisive solver certificates used over the same scope are semantically
valid.

On \(E\cap S\), fix a look \(t\). If RACH reports `INVARIANT` for a motif
absent from \(\theta^\star\), then the retained true point witnesses the
motif-inactive subset in every required cell. A semantically valid `UNSAT`
certificate for that subset is therefore impossible. The `EXCLUDED` case is
symmetric.

Thus, at every look,

\[
\{\text{false decisive result at }t\}\subseteq E^c\cup S^c.
\]

Taking a union over all looks and motifs changes nothing because both \(E\) and
\(S\) are already all-look, all-required-cell, and all-motif events:

\[
\{\text{any false decisive result at any certified look}\}
\subseteq E^c\cup S^c.
\]

By the union bound,

\[
\Pr(E^c\cup S^c)\le\alpha+\beta.
\]

The stopping-time result follows because a false decisive result at the selected
look is a subset of the union over all certified looks.

## Scope discipline

The theorem fixes three targets before sequential inspection:

1. the candidate-space and motif vocabulary;
2. the required cell IDs; and
3. the certified look scope.

RACH rejects a sequential trajectory that changes required cell IDs midstream or
uses a look outside either certificate's finite scope. When one certificate is
all-look and the other is finite, the resulting theorem applies only to the
finite scope. When both scopes are finite, they must match exactly.

Changing a motif definition, candidate encoding, required cell, or look scope
after observing results is not covered by the original certificate and requires
a new theorem target with new all-look guarantees.

## Relation to prior RACH theorems

| Layer | Candidate space | Time scope | Solver semantic risk |
|---|---|---|---|
| Confidence-set lifting | finite IDs | one analysis point | none | 
| Anytime confidence-set lifting | finite IDs | finite or all looks | none |
| Symbolic candidate-set lifting | arbitrary \(\Theta\) | one analysis point | \(\beta\) |
| **Anytime symbolic lifting** | arbitrary \(\Theta\) | finite or all looks | \(\beta\) |

With a finite candidate universe and \(\beta=0\), the theorem reduces to the
existing anytime confidence-set result. With one look, it reduces to symbolic
candidate-set lifting. With the exact rational linear proof verifier, every
verified linear SAT/UNSAT artifact can use \(\beta=0\) under its explicit trust
boundary.

## What remains outside RACH

This theorem does not construct a confidence sequence, prove that an arbitrary
solver's output is valid, infer motif predicates from a scientific narrative, or
ensure the true mechanism belongs to the declared candidate space. It controls
false decisiveness only conditional on all of those external obligations.

The implementation records those obligations through
`AnytimeSymbolicJointCoverageCertificate` and
`AnytimeSolverSemanticValidityCertificate`, then audits the deterministic
set-inclusion relation with `deterministic_anytime_symbolic_lifting_witness`.
