# Non-nested replacement portability

## Position

This is the selected **post-v1 structural extension**. It does not replace the
portability-core-v1 theorem family.

Portability core v1 handles nested composition by label-coherent embeddings and
conservative legal-action expansion. This extension asks what remains true when
stages are connected by declared replacement, extinction, or rewiring relations
with no inclusion map between raw state spaces.

## One question

For a declared finite family of controlled systems connected by replacement
relations,

\[
M_u \rightsquigarrow M_v,
\]

when can one exact finite macro-law remain shared even though neither stage is a
subsystem of the other?

## Positive sufficient criterion

Every stage must have an exact projection into one common finite macro dynamics
\(\mathcal Q\). Each declared replacement edge must supply a transport relation

\[
R_{u,v}\subseteq S_u\times S_v
\]

that is:

1. total on the declared source and target product states;
2. label-preserving;
3. output-preserving;
4. legal-action preserving; and
5. successor-closed under every legal action.

If the declared replacement graph is connected, one exact macro-law is shared
across the whole finite family.

The transport need not be injective. In particular, several old microstates may
be replaced by one new microstate while preserving the common macro label and
its legal successor structure.

## Positive witness

`non_nested_replacement_witness()` gives a three-state source stage and a
two-state target stage. No source-to-target injection exists, but the many-to-one
transport

\[
(0,0),\ (1,0),\ (2,1)
\]

preserves the same two-state macro dynamics exactly.

This is why the result is not merely a restatement of nested embedding
portability.

## Local negative obstruction

A replacement can admit a word that was previously illegal. If that word
separates two old states carried in one proposed macro fiber, the proposed merge
is invalid.

`non_nested_rewiring_obstruction()` gives a four-state source stage and a
three-state target stage. The word `reveal` is illegal before replacement and
legal after it; it distinguishes two carried states that a proposed target
summary still merges.

## Claim status

| Result | Status |
|---|---|
| Transport-coherent portable macro-law | Sufficient finite-domain criterion |
| Newly legal replacement word separates a carried merge | Local obstruction to that proposed merge |
| No transport witness exists | `UNRESOLVED`, not an automatic memory-growth theorem |

## Do not claim

- A declared replacement relation is not inferred from empirical data.
- Failure to find a transport witness does not prove cumulative addressability,
  unbounded interface memory, or absence of every alternative macro-law.
- The result does not cover stochastic, approximate, or candidate-uncertain
  composition changes.
- It does not establish a macro-law for arbitrary ecosystem replacement without
  a declared finite state space and composition grammar.
