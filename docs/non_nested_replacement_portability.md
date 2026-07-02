# Non-nested replacement portability

## Position

This is the selected **post-v1 structural extension**. It does not replace the
portability-core-v1 theorem family.

Portability core v1 handles nested composition through label-coherent embeddings
and conservative legal-action expansion. This extension treats declared finite
replacement, extinction, and rewiring relations for which there is no inclusion
map between raw stage state spaces.

## One question

For a declared finite family of controlled systems connected by replacement
relations,

\[
M_u \rightsquigarrow M_v,
\]

when can one exact finite macro-law remain shared even though neither stage is a
subsystem of the other?

## Positive sufficient criterion

Every stage has an exact projection into one common finite macro dynamics
\(\mathcal Q\). Each declared replacement edge supplies a transport relation

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
across the whole finite family. The transport need not be injective: several old
microstates may map to one new microstate while preserving the macro label and
its legal successor structure.

## Positive witness

`non_nested_replacement_witness()` has a three-state source stage and a two-state
target stage. No source-to-target injection exists, but the many-to-one transport

\[
(0,0),\ (1,0),\ (2,1)
\]

preserves the same two-state macro dynamics exactly. This distinguishes the
criterion from a bare restatement of nested embedding portability.

## Local negative obstruction

A replacement can admit a word that was previously illegal. If that word
separates two old states carried in one proposed macro fiber, the proposed merge
is invalid.

`non_nested_rewiring_obstruction()` has a four-state source stage and a
three-state target stage. `reveal` is illegal before replacement, legal after it,
and separates two carried states that a proposed target summary merges.

## Claim status

| Result | Status |
|---|---|
| Transport-coherent portable macro-law | Sufficient finite-domain criterion |
| Newly legal replacement word separates a carried merge | Local obstruction to that merge |
| No transport witness exists | `UNRESOLVED`, not an automatic memory-growth result |

## Verification contract

The extension is checked only inside its declared finite domain:

- `tests/test_non_nested_portability.py` checks the many-to-one positive witness,
  successor-closure rejection, the newly legal-word obstruction, connectedness,
  and facade exports.
- `scripts/verify_non_nested_replacement_portability.py` writes a deterministic
  JSON replay report with the transport relation, macro dynamics, and obstruction
  witness.
- `.github/workflows/non-nested-replacement-portability.yml` runs the focused
  regression tests and uploads that replay report for relevant changes.

A passing replay verifies the supplied certificates. It does not infer a
replacement grammar, test an empirical ecosystem, or exhaust arbitrary future
compositions.

## Proof-strength boundary

The current positive criterion assumes that **every stage already has an exact
projection into the common macro dynamics**. The transport then certifies that the
declared replacement edge preserves that shared meaning.

A stronger future theorem would start with an exact source projection and show
when a total, label-consistent, successor-closed transport *constructs* the
target projection. That construction is not claimed here.

## Do not claim

- A declared replacement relation is not inferred from empirical data.
- Failure to find a transport witness does not prove cumulative addressability,
  unbounded interface memory, or absence of every alternative macro-law.
- The result does not cover stochastic, approximate, or candidate-uncertain
  composition changes.
- It does not establish a macro-law for arbitrary ecosystem replacement without
  a declared finite state space and composition grammar.
