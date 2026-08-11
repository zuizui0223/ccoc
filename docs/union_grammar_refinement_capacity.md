# Union-grammar refinement capacity and correlation defect

> **Status:** post-reopening `CORE-2` strengthening candidate. The common-refinement
> identity and Cartesian counting bound are elementary mathematical substrate,
> not novelty claims. The intended contribution is their use to give an exact
> open-vs-closed interface-inflation decomposition under one declared composition
> contract.

## 1. Why this replaces coordinate decoders in one delimited class

The addressable-product and addressable-codebook theorems certify a large open
quotient by exhibiting legal future words that decode coordinates. That is useful
when only a lower-bound witness is known.

There is a stronger conclusion when the comparison contract itself has the form

\[
\mathcal L_{\rm open}=\bigcup_{j=1}^m \mathcal L_j
\]

on one common finite comparison domain `D`, with the same response map used in
every context. Then no coordinate system is needed at all.

For context `j`, define

\[
s\sim_j t
\iff
R(s,w)=R(t,w)\quad\forall w\in\mathcal L_j.
\]

For the open union grammar define `~open` analogously.

## 2. Exact union-grammar refinement theorem

### Theorem

If

\[
\mathcal L_{\rm open}=\bigcup_j\mathcal L_j,
\]

then on `D`

\[
\boxed{
\sim_{\rm open}=\bigcap_j\sim_j.
}
\]

Therefore the exact open quotient is the common refinement of the exact closed
quotients.

### Proof

If `s ~open t`, their responses agree for every word in the union grammar, hence
for every word in every `Lj`; thus `s ~j t` for all `j`.

Conversely, if `s ~j t` for every `j`, then any open word belongs to at least one
`Lj`, and the two states agree on that word. Hence `s ~open t`. `square`

Let

\[
q_j:D\to Q_j
\]

be the exact quotient label for context `j`. The theorem is equivalently

\[
\boxed{
|Q_{\rm open}|
=
\left|\{(q_1(s),\ldots,q_m(s)):s\in D\}\right|.
}
\]

Thus, within the exact union-grammar subclass, open-interface complexity is not
merely lower-bounded by future-separable coordinates: it is **exactly the number
of jointly realized closed-response signature tuples**.

This is the desired converse/characterization, but only for the explicitly
stated union-grammar contract. An open grammar containing additional words can
refine this quotient further.

## 3. Shared base quotient

Suppose there is a common base grammar `L0` contained in every closed grammar,
or more generally a common base partition

\[
P_0
\]

that is coarser than every closed partition `Pj`.

For a base block `B in P0`, let

\[
r_j(B)
\]

be the number of `Pj` blocks contained in `B`.

Inside `B`, a block of the common refinement is identified by one closed label
from every context. Therefore at most

\[
\prod_j r_j(B)
\]

joint labels can occur inside `B`.

Summing over disjoint base blocks gives the **fibered refinement capacity**

\[
\boxed{
C(P_0;P_1,\ldots,P_m)
=
\sum_{B\in P_0}\prod_{j=1}^m r_j(B)
}
\]

and the universal upper bound

\[
\boxed{
|Q_{\rm open}|\le C(P_0;P_1,\ldots,P_m).
}
\]

### Equality condition

Equality holds exactly when, inside every base block `B`, **every Cartesian
combination of closed quotient labels is jointly realized by at least one state**.

This is the precise role played by the historical full-product witness. Full
Cartesian realizability was stronger than needed for a lower bound, but it is
exactly the condition that saturates the maximum refinement capacity permitted by
the closed laws and their shared base.

## 4. Correlation / joint-realizability defect

Define

\[
\boxed{
\delta_{\rm corr}
=
\log_2 C-
\log_2|Q_{\rm open}|
\ge0.
}
\]

This measures the amount of nominal closed-context combination capacity that is
lost because some combinations of closed response types are not jointly
realizable.

The exact noncommutation gap is

\[
\Delta
=
\log_2|Q_{\rm open}|
-
\max_j\log_2|Q_j|.
\]

Substituting the defect definition gives the exact decomposition

\[
\boxed{
\Delta
=
\underbrace{\left(\log_2C-\max_j\log_2|Q_j|\right)}_{\text{fibered inflation capacity}}
-
\underbrace{\delta_{\rm corr}}_{\text{missing joint response types}}.
}
\]

This is not an inequality. Under the union-grammar/shared-base contract it is an
identity.

## 5. Uniform-fiber form

If every base block has the same number `rj` of refinements in context `j`, then

\[
C=|Q_0|\prod_j r_j.
\]

If additionally

\[
|Q_j|=|Q_0|r_j,
\]

then the maximum possible gap compatible with these closed/base quotient sizes is

\[
\boxed{
\Delta_{\max}
=
\sum_j\log_2r_j-
\max_j\log_2r_j.
}
\]

The historical binary product family has `|Q0|=2` and `rj=2`; hence

\[
\Delta_{\max}=m-1.
\]

Its earlier lower bound therefore meets a universal upper bound in this class.
This explains the sharpness of the original construction more cleanly than the
coordinate-count statement alone.

## 6. Post-reopening codebooks as capacity-defect families

Take one binary inside/base state and `m` binary closed refinements. Then

\[
C=2^{m+1}.
\]

### Full product

All combinations occur:

\[
|Q_{\rm open}|=2^{m+1},
\qquad
\delta_{\rm corr}=0,
\qquad
\Delta=m-1.
\]

### Even parity

Exactly half of the binary combinations occur:

\[
|Q_{\rm open}|=2^m,
\qquad
\delta_{\rm corr}=1,
\qquad
\Delta=m-2.
\]

### Fixed richness / Hamming weight

For

\[
C_{m,k}
=
\{(y,b_1,\ldots,b_m):\sum_jb_j=k\},
\]

with `1 <= k <= m-1`, all four `(y,bj)` closed labels occur, while

\[
|Q_{\rm open}|=2\binom{m}{k}.
\]

Hence

\[
\boxed{
\delta_{\rm corr}
=m-\log_2\binom{m}{k}
}
\]

and

\[
\boxed{
\Delta
=\log_2\binom{m}{k}-1.
}
\]

At fixed density `k ~= rho m`, the defect is only sublinear around maximal
entropy density. In particular near `rho=1/2`,

\[
\delta_{\rm corr}=\tfrac12\log_2m+O(1),
\]

so the family retains almost all of the `m-1` bit inflation capacity despite an
exact fixed-richness constraint.

This gives a sharper interpretation of the earlier `composition code rate`: it
is the fraction of fibered response-combination capacity actually occupied by
admissible compositions.

## 7. Relation to addressability

The three levels now have distinct roles.

1. **General grammar, lower-bound witness:** operational decoder words or any
   pair-separating family can certify that some set of states must remain distinct.
2. **Exact union grammar:** no decoder coordinates are needed; the open quotient
   is exactly the common refinement of closed quotients.
3. **Shared-base union grammar:** the refinement has an exact maximum capacity and
   a measurable correlation defect.

Thus the addressable-codebook theorem remains useful outside the exact
union-grammar subclass. The refinement theorem does not replace it universally.

## 8. Novelty boundary and adjacent automata theory

The following pieces are **not** novelty claims:

- intersection of equivalence relations;
- common refinement of partitions;
- Cartesian-product upper bounds for combined state descriptions; and
- the fact that Boolean operations on regular languages can have multiplicative
  state/quotient complexity.

Regular-language state/quotient complexity explicitly studies tight state
blow-ups under operations. Relevant anchors include Brzozowski, *Quotient
Complexity of Regular Languages* (2009, arXiv:0907.4547), and Brzozowski,
*Unrestricted State Complexity of Binary Operations on Regular Languages* (2016,
arXiv:1602.01387), where intersection has the familiar multiplicative product
bound. These results are a reason **not** to present the product/refinement count
as new.

The CCOC claim should remain narrower:

> closed ecological/compositional grammars can each admit small exact causal
> interfaces while their declared open union grammar realizes a large common
> refinement; the inflation can approach its fibered maximum even under strong
> global composition constraints, and can be realized with bounded degree,
> pairwise locality, constant local grammar, and a constant global action
> alphabet.

The cross-grammar causal-composition interpretation and constrained/locality
sharpness remain the novelty target. A full manuscript literature gate is still
required before a priority claim.

## 9. Executable certificate

`causal_model.union_grammar_refinement` provides two layers:

- `PartitionRefinementCapacityCertificate`: exact common-refinement count,
  fibered capacity, equality test, and correlation-defect decomposition for
  supplied finite partitions;
- `UnionGrammarRefinementCertificate`: constructs the exact closed/open response
  signatures from one finite controlled system, common comparison domain, shared
  base word family, and closed word families whose union is the open grammar.

Finite replay checks supplied contracts; the all-cardinality identities are the
symbolic proofs above.
