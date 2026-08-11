# Database-join ancestry of the shared-base refinement capacity

## Why this note exists

The post-reopening union-grammar refinement calculation has a direct static
analogue in classical relational database theory. That connection is important
for novelty discipline: CCOC must not claim the natural-join combinatorics,
lossless reconstruction condition, or join-redundancy idea as new.

The useful contribution, if any, is the **controlled causal-response
interpretation**: each relation attribute below is itself an exact future-response
quotient induced by a declared closed counterfactual grammar, and the open system
asks what happens when those grammars become jointly legal.

## Static relation induced by closed causal quotients

Fix a finite comparison domain `D`, a shared base quotient

\[
q_0:D\to Q_0,
\]

and exact closed-context quotients

\[
q_j:D\to Q_j.
\]

Assume each `qj` refines the shared base. Inside a base block we may equivalently
write the context-specific refinement label as `u_j`.

The jointly realized causal response types form a finite relation

\[
R
=
\{(q_0(s),u_1(s),\ldots,u_m(s)):s\in D\}.
\]

Each closed context exposes only the projection

\[
R_j=\pi_{0j}(R).
\]

The natural join of these closed projections is

\[
J
=R_1\Join R_2\Join\cdots\Join R_m.
\]

Because all projections share the same base key, its cardinality is exactly

\[
\boxed{
|J|
=
\sum_{B\in Q_0}\prod_j r_j(B),
}
\]

where `r_j(B)` is the number of context-`j` refinement labels observed over base
block `B`.

This is exactly the `fibered_capacity_state_count` used by
`PartitionRefinementCapacityCertificate`.

## Lossless join equals capacity saturation

Always

\[
R\subseteq J.
\]

Equality

\[
R=J
\]

means that the family of closed projections reconstructs the realized joint
relation without introducing any spurious combination. In database language this
is a **lossless join** condition.

Therefore CCOC's condition

> every Cartesian combination of closed quotient labels is jointly realized in
> each shared-base block

is the same static combinatorial condition as lossless reconstruction of `R`
from the projections `R_j`.

The historical full-product witness satisfies this condition and hence saturates
the join/refinement capacity.

## Join-realizability defect

The current certificate records

\[
\delta
=
\log_2|J|-
\log_2|R|.
\]

This is best interpreted as a **support-level join-realizability defect**: the
logarithmic excess of combinations admitted by the natural join of closed
projections over combinations actually realized by the open causal state family.

It should not be advertised as a new database-theoretic loss measure. Classical
work studies lossless joins and join dependencies, and recent work explicitly
quantifies join-dependency loss using redundant tuples and information-theoretic
quantities.

The exact CCOC gap identity can therefore be written

\[
\boxed{
\Delta
=
\left(\log_2|J|-\max_j\log_2|Q_j|\right)
-
\log_2\frac{|J|}{|R|}.
}
\]

The first term is the nominal closed-projection join capacity relative to the
largest single closed interface. The second term is loss of realizable
combinations.

## Classical ancestry that must be cited

At minimum, the manuscript comparison should include:

- Ronald Fagin (1977), **Multivalued Dependencies and a New Normal Form for
  Relational Databases**, *ACM Transactions on Database Systems* 2(3):262--278.
  Multivalued dependencies are tied to decomposition into projections without
  loss of information.
- A. V. Aho, C. Beeri, and J. D. Ullman (1979), **The Theory of Joins in
  Relational Databases**, *ACM Transactions on Database Systems* 4(3):297--314.
  This develops lossless-join theory for decomposed relational schemes.
- Jorma Rissanen (1977), **Independent Components of Relations**, *ACM
  Transactions on Database Systems*. The paper explicitly studies projections
  that behave like Cartesian-product / independent components and reconstructs
  them by natural join.
- Batya Kenig and Nir Weinberger (2022), **Quantifying the Loss of Acyclic Join
  Dependencies**, arXiv:2210.14572. This is particularly relevant because it
  treats redundant tuples created by a lossy join and relates join loss to an
  information-theoretic measure.

These references mean that neither natural-join saturation nor a logarithmic
summary of missing combinations should be presented as an isolated new
combinatorial invention.

## What is still specifically CCOC

The database relation above is not the starting object in CCOC. Each label `q_j`
is itself defined by equality of **future controlled response traces under one
closed action grammar**. The open grammar changes which counterfactual futures
are jointly admissible.

The current CCOC novelty target is therefore narrower:

1. exact causal compression is small under every closed counterfactual grammar;
2. opening the grammar makes the joint future-response relation operationally
   relevant;
3. this forces interface inflation that can approach the full join capacity even
   under parity or fixed-richness constraints; and
4. the near/maximal inflation admits a pairwise, maximum-degree-three,
   constant-local-grammar, constant-global-action-alphabet dynamic realization.

That combination is what must be compared against causal abstraction,
compositional abstraction, automata state complexity, and database join theory.
The static join calculation alone is not the novelty claim.
