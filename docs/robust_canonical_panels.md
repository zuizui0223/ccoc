# Robust canonical distinguishing panels

## Position in the RACH calculus

A canonical boundary blanket gives the smallest exact exterior response summary
under a declared grammar. A completion-coverage certificate then says when a
finite evidence set has actually enumerated that blanket. The next question is
not whether a panel is vaguely “robust,” but exactly which declared
observation/intervention cells are necessary to distinguish all blanket classes
and how many independently lost cells can be tolerated.

The answer is a pairwise separation hypergraph.

## Setup

Let \(B\) be a finite canonical blanket and let

\[
\bar R(i,b,w)
\]

be the induced response of inside state \(i\), blanket class \(b\), and allowed
word \(w\). The cell universe is

\[
U=I\times\Gamma.
\]

For each distinct pair \(b\ne b'\), define its separation set

\[
D_{b,b'}=
\left\{
(i,w)\in U:
\bar R(i,b,w)\ne\bar R(i,b',w)
\right\}.
\]

A panel is a finite subset \(P\subseteq U\). Its separation multiplicity for a
pair is

\[
s_P(b,b')=|P\cap D_{b,b'}|.
\]

A cell means one declared independently lossable observation or intervention.
Replicated camera deployments, repeated assays, or repeated plot measurements
count as independent only when their independence is made explicit in the
contract as distinct cells.

## Theorem 1 — Exact panel equivalence

\[
\boxed{
P\text{ identifies every blanket class exactly}
\quad\Longleftrightarrow\quad
\forall b\ne b',\ s_P(b,b')\ge1.
}
\]

Equivalently, \(P\) is a transversal of the separation hypergraph

\[
\mathcal D=\{D_{b,b'}:b\ne b'\}.
\]

Its minimum possible size is the transversal number

\[
\boxed{\tau(\mathcal D).}
\]

### Proof

The panel response signature of \(b\) is the tuple

\[
\left(\bar R(i,b,w)\right)_{(i,w)\in P}.
\]

Two classes have unequal signatures precisely when at least one selected cell
lies in \(D_{b,b'}\). Thus injectivity of the panel signature is exactly the
condition that every pairwise separation set is hit. \(\square\)

The theorem is a structural characterization. It does not claim that arbitrary
minimum-transversal instances are computationally easy.

## Theorem 2 — Exact arbitrary-loss robustness

For \(f\ge0\), the following are equivalent:

\[
\boxed{
P\text{ remains exact after deletion of every at-most-}f\text{ subset of cells}
}
\]

and

\[
\boxed{
\forall b\ne b',\ s_P(b,b')\ge f+1.
}
\]

Thus \(f\)-loss robust panels are precisely \((f+1)\)-fold transversals of
\(\mathcal D\), with minimum cardinality

\[
\boxed{\tau_{f+1}(\mathcal D).}
\]

The exact tolerance of a fixed panel is

\[
\boxed{
f_\star(P)=\min_{b\ne b'}s_P(b,b')-1.
}
\]

When \(f_\star(P)=-1\), the panel is not exact even before any loss.

### Proof

If every pair has at least \(f+1\) selected separators, deletion of at most
\(f\) cells leaves one separator for every pair, so Theorem 1 still applies.
Conversely, if some pair has at most \(f\) selected separators, delete exactly
those cells. The two classes then have identical retained-panel signatures.
\(\square\)

## Theorem 3 — Constructive dropout ambiguity

The converse proof is operational. Whenever a panel fails \(f\)-loss robustness,
the failure certificate returns:

- a concrete blanket pair \((b,b')\);
- the complete selected separator set \(P\cap D_{b,b'}\), of size at most \(f\);
  and
- the retained panel on which \(b\) and \(b'\) collide.

So a failed robustness claim is not a scalar warning. It names the ecological or
mechanistic ambiguity left after a particular possible observation loss.

## Theorem 4 — Disjoint-packing lower bound

Let \(Q\) be any collection of blanket pairs whose separation sets are pairwise
disjoint. Every \(f\)-loss robust panel obeys

\[
\boxed{
|P|\ge(f+1)|Q|.
}
\]

### Proof

For each pair in \(Q\), the panel needs at least \(f+1\) cells from its
separation set. Because those sets are disjoint, these requirements cannot share
cells. Summing gives the lower bound. \(\square\)

A candidate robust panel that meets this bound is therefore minimum-size. This
is an analytical optimality certificate, not a finite search result.

## Closed-form private-bundle witness

A four-class family uses three disjoint bundles of \(r\) cells:

- a group bundle separating \((0,2)\);
- a left bundle separating \((0,1)\); and
- a right bundle separating \((2,3)\).

The three named pairwise separation sets are disjoint. The full panel has
\(3r\) cells and remains exact after any \(r-1\) cell losses. The packing
lower bound gives

\[
|P|\ge r\times3=3r,
\]

so

\[
\boxed{
\tau_r(\mathcal D)=3r.
}
\]

This separates an actual minimum robust design theorem from a generic claim that
“more replicates are safer.”

## Ecological projection

Once the declared outside has been reduced to finitely many canonical response
regimes, an empirical design can make a precise statement such as:

> This panel distinguishes all declared boundary regimes even if any one camera,
> assay, weather window, or independently deployed plot cell is lost.

Or, if it fails:

> Loss of these specific cells makes regime \(b\) observationally indistinguishable
> from regime \(b'\).

This theorem is conditional on a finite coverage contract and independently
lossable cells. It does not claim that real missingness is independent, that
cells are noise-free, or that unmodeled exterior completions have been excluded.

## Executable certificates

`causal_model.robust_canonical_panels` provides:

- `CanonicalSeparationHypergraph`;
- `CanonicalPanelProfile` and `RobustCanonicalPanelCertificate`;
- `DropoutAmbiguityCertificate`;
- `DisjointSeparationPackingCertificate`; and
- `OptimalRobustPanelCertificate`.

Finite replay checks the certificates. The proofs above establish the general
equivalences; replay is not a simulation claim.