# Non-nested replacement portability

## Position

This is the selected **post-v1 structural extension**. It does not replace the portability-core-v1 theorem family.

Portability core v1 handles nested composition through label-coherent embeddings and conservative legal-action expansion. This extension treats declared finite replacement, extinction, and rewiring relations for which there is no inclusion map between raw stage state spaces.

## One question

For a declared finite family of controlled systems connected by replacement relations,

\[
M_u \rightsquigarrow M_v,
\]

when can one exact finite macro-law remain shared even though neither stage is a subsystem of the other?

## Layer N1 — edge preservation with supplied stage projections

Every stage has an exact projection into one common finite macro dynamics. Each declared replacement edge supplies a total, label-preserving, output-preserving, legal-action-preserving, successor-closed transport relation. If the declared replacement graph is connected, one exact macro-law is shared across the family.

## Layer N2 — transported target factorization

Let \(q_S:S\to Q\) be an exact grammar-aware source projection. A relation \(R\subseteq S\times T\) can construct target labels without taking them as input when it covers both product spaces, preserves output and equal legal-action rows, is successor-closed, and is label-consistent on each target fiber:

\[
(s,t),(s',t)\in R \Longrightarrow q_S(s)=q_S(s').
\]

Then

\[
q_T(t)=q_S(s)\qquad ((s,t)\in R)
\]

is well-defined, grammar-aware exact, and induces the same macro dynamics as \(q_S\). `TransportedTargetProjectionCertificate` checks this finite theorem.

## Layer N3 — conservative transport with target-only actions

Equal legal-action rows are stronger than necessary. A target can add an action while preserving one exact conservative macro schema.

Start with an exact source projection \(q_S:S\to Q\) and a relation \(R\subseteq S\times T\) covering both product spaces. Require:

1. source and target share one finite action alphabet;
2. each target fiber has one source label, so \(q_T(t)=q_S(s)\) is well-defined;
3. related states have equal current outputs;
4. every action legal at a related source state remains legal at the target;
5. the relation is successor-closed for every source-legal action; and
6. for every derived target macro fiber, every target-only action has uniform availability and one uniform target successor label.

For an old action, use the source macro successor. For a target-only action, use its uniform target successor. This defines one finite schema. `ConservativeTransportedSchemaCertificate` derives \(q_T\), constructs the `ConservativeMacroSchema`, and verifies that the source realizes a restriction of it while the target realizes its full action rows.

### Finite proof sketch

For old actions, source exactness plus successor closure transfers equal source successor labels to equal target successor labels, exactly as in N2. For each new action, premise 6 supplies a common legal status and one common target successor label for every state in a derived target fiber. Therefore each target fiber has one output, one legal row, and one successor label per legal action, hence \(q_T\) is exact. The source legal rows are restrictions of the schema because all old actions remain legal; target rows equal the schema because the new actions are uniform by premise 6.

### Positive witness

`conservative_non_nested_replacement_witness()` is a three-state-to-two-state many-to-one replacement. `flip` is legal at both stages; `reveal` is target-only. The transport derives target labels \((0,1)\). The source realizes rows `((1, None), (0, None))`; the target realizes the conservative schema rows `((1, 1), (0, 1))`. There is no source-to-target injection.

### Why the new premise is necessary

- If a target-only action is legal for some but not all states in one derived target fiber, that proposed macrostate has no single legal row.
- If it has different successor labels inside one derived target fiber, that proposed macrostate has no single macro successor.
- Either conflict refutes that proposed carried merge, not every possible macro-law.

## Local negative obstruction

`non_nested_rewiring_obstruction()` makes `reveal` newly legal and separates two carried states in one proposed target fiber. It is the negative boundary of N3: that relation cannot realize a conservative schema with the proposed merge.

## Claim status

| Result | Status |
|---|---|
| Transport-coherent law with supplied projections | Sufficient finite-domain criterion |
| Source-to-target transported exact factorization | Sufficient finite-domain theorem |
| Conservative non-nested transport with target-only actions | Sufficient finite-domain theorem |
| Newly legal replacement word separates a carried merge | Local obstruction to that merge |
| No valid transport certificate | `UNRESOLVED`, not an automatic memory-growth result |

## Verification contract

The extension is checked only inside its declared finite domain:

- `tests/test_non_nested_portability.py` covers N1, N2, and the original rewiring obstruction.
- `tests/test_non_nested_conservative_transport.py` covers N3, successor-closure failure, nonuniform new-action availability, and nonuniform new-action successor labels.
- `scripts/verify_non_nested_replacement_portability.py` writes a deterministic JSON replay report with supplied relations, derived target labels, schema, and obstruction.
- `.github/workflows/non-nested-replacement-portability.yml` runs both focused suites and uploads that report.

A passing replay verifies supplied finite certificates. It does not infer a replacement grammar, test an empirical ecosystem, or exhaust arbitrary future compositions.

## Do not claim

- A declared replacement relation or action grammar is not inferred from empirical data.
- Failure to find a transport certificate does not prove cumulative addressability, unbounded interface memory, or absence of every alternative macro-law.
- N3 does not cover new actions with nonuniform availability or nonuniform macro successor inside a target fiber.
- The result does not cover stochastic, approximate, or candidate-uncertain composition changes.
- It does not establish a macro-law for arbitrary ecosystem replacement without a declared finite state space and composition grammar.
