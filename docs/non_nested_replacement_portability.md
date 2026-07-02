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

## Layer N1 — edge preservation with supplied stage projections

Every stage has an exact projection into one common finite macro dynamics
\(\mathcal Q\). Each declared replacement edge supplies a transport relation

\[
R_{u,v}\subseteq S_u\times S_v
\]

that is total, label-preserving, output-preserving, legal-action preserving, and
successor-closed. If the declared replacement graph is connected, one exact
macro-law is shared across the family.

This transport need not be injective: several old microstates may map to one new
microstate while preserving the macro label and legal successor structure.

## Layer N2 — transported target factorization

The stronger edge theorem does **not** take target labels as an input.

Let \(q_S:S\to Q\) be an exact grammar-aware source projection. Let

\[
R\subseteq S\times T
\]

cover every declared source and target product state. Assume:

1. source and target share one finite action alphabet;
2. related states have equal current output and equal legal-action rows;
3. \(R\) is successor-closed under every related legal action; and
4. each target fiber has one source label:

   \[
   (s,t),(s',t)\in R
   \Longrightarrow
   q_S(s)=q_S(s').
   \]

Then

\[
q_T(t)=q_S(s)\qquad ((s,t)\in R)
\]

is well-defined, is an exact grammar-aware target interface, and induces the
same macro dynamics as \(q_S\).

The theorem is operationalized by
`TransportedTargetProjectionCertificate`. It constructs `target_labels` and the
exact `StageMacroProjection` only from the source projection, raw target system,
and relation.

### Finite proof

Target-fiber label consistency makes \(q_T\) well-defined. Now take two target
states \(t,t'\) with \(q_T(t)=q_T(t')\), and choose related source states
\((s,t),(s',t')\in R\). By definition, \(q_S(s)=q_S(s')\). Exactness of
\(q_S\) gives equal source outputs, equal source legal-action rows, and equal
source successor labels for every legal action.

Output and legal-row preservation along \(R\) transfer the first two equalities
to \(t,t'\). For a common legal action \(a\), successor closure gives

\[
(T_S(s,a),T_T(t,a))\in R,
\qquad
(T_S(s',a),T_T(t',a))\in R.
\]

The source successors have equal \(q_S\)-labels, so the target successors have
equal \(q_T\)-labels. Thus \(q_T\) satisfies the exact grammar-aware interface
conditions. Finally, total source coverage ensures every source macro label is
realized in the target; total target coverage and the same argument show output,
legal rows, and successors match label by label. Hence the induced macro dynamics
are identical.

### Why each premise matters

- Without target-fiber label consistency, one target state receives incompatible
  source macro labels.
- Without successor closure, source and target successors do not remain related,
  so target macro successors need not be well-defined.
- A newly legal target action violates equal legal-action preservation; this is
  precisely where a carried source merge may split.

## Positive witness

`transported_target_projection_witness()` uses a three-state source and a
two-state target. The many-to-one relation

\[
(0,0),\ (1,0),\ (2,1)
\]

constructs target labels \((0,1)\) without supplying them to the constructor.
No source-to-target injection exists, yet the derived target macro dynamics equal
the source macro dynamics.

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
| Transport-coherent portable macro-law with supplied projections | Sufficient finite-domain criterion |
| Source-to-target transported exact factorization | Sufficient finite-domain theorem |
| Newly legal replacement word separates a carried merge | Local obstruction to that merge |
| No valid transport certificate | `UNRESOLVED`, not an automatic memory-growth result |

## Verification contract

The extension is checked only inside its declared finite domain:

- `tests/test_non_nested_portability.py` checks target construction, target-fiber
  label inconsistency, successor-closure failure, newly legal actions, family
  connectedness, and facade exports.
- `scripts/verify_non_nested_replacement_portability.py` writes a deterministic
  JSON replay report with the supplied relation, source macro dynamics, derived
  target labels, and the rewiring obstruction.
- `.github/workflows/non-nested-replacement-portability.yml` runs those focused
  regressions and uploads the replay report for relevant changes.

A passing replay verifies the supplied certificates. It does not infer a
replacement grammar, test an empirical ecosystem, or exhaust arbitrary future
compositions.

## Do not claim

- A declared replacement relation is not inferred from empirical data.
- Failure to find a transport certificate does not prove cumulative addressability,
  unbounded interface memory, or absence of every alternative macro-law.
- The theorem does not cover transports with target-only legal actions; those
  require an additional conservative-extension contract or can trigger a fiber
  split.
- The result does not cover stochastic, approximate, or candidate-uncertain
  composition changes.
- It does not establish a macro-law for arbitrary ecosystem replacement without a
  declared finite state space and composition grammar.
