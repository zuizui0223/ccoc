# Manuscript readiness audit: open-composition causal compression

## Decision

RACH is now the **frozen theorem and certificate archive** for the finite deterministic result package. It is not the manuscript workspace and it is not the home for the next mathematics branch.

A submission-oriented manuscript may use the theorem package below, but must restate all definitions, lemmas, and proofs independently in LaTeX. Passing Python certificates are reproducibility evidence for declared finite instances; they are not a substitute for a general proof.

The intended main claim is:

\[
\text{exact compression in each fixed closed composition}
\not\Rightarrow
\text{one small exact interface for the declared open composition grammar}.
\]

The relevant lower bound is conditional on operational addressability, not on system size alone.

## Manuscript package

| Manuscript role | RACH asset | What can be used | What must not be claimed |
|---|---|---|---|
| Formal setup | `CORE-1`, `grammar_aware_blankets.py` | Exact interface means preservation of output, legal actions, and successor summary on `system state × grammar state`. | This quotient is not claimed to be novel relative to fixed-grammar quotient or bisimulation theory. |
| Main negative theorem | `CORE-2`, `extension_compression_noncommutation.py` | Under joint realization and uniform decoder-word premises, distinct product-indexed states require distinct open interface labels. | The certificate does not infer product structure, decoder words, reachability, or the ecological grammar from data. |
| Sharpness construction | `CORE-3`, `extension_compression.py`, `relay_tree_compilation.py` | Binary family with closed memory 2 bits, open memory `m + 1` bits, pairwise messages, maximum degree 3, and a size-independent local node/message grammar. | Do not call the global port-labelled action alphabet constant-size. Do not generalize from the witness to arbitrary local networks. |
| Positive boundary | `CORE-4`, `coherent_portable_macrolaw.py`, `conservative_macro_schema.py` | A finite update-consistent common summary gives a sufficient portability criterion for a declared finite chain. | The criterion is sufficient, not a necessary characterization or theorem about arbitrary infinite/stochastic composition. |
| Replacement/ecological corollary | `EXT-1`--`EXT-4`, `non_nested_*` modules | Declared replacement, extinction, and rewiring relations can transport a law under stated relation and fiber-uniformity conditions. | Failure of a transport certificate is not a lower bound and not absence of every macro-law. |
| Scope and interpretation | `docs/nonempirical_scope.md` | A focal patch plus dormant external modules can be a synthetic ecological reading. | No field validation, fitted parameters, or claim about any observed ecosystem. |

## The precise theorem spine for a paper

### Definition: exact grammar-aware interface

For a declared finite deterministic controlled system with a declared finite action grammar, an exact interface is a summary of the product state `(system state, grammar state)` that preserves:

1. current output;
2. the enabled legal-action row; and
3. the successor summary for every enabled action.

This is the object to which all memory statements refer.

### Theorem A: addressable-product lower bound

Let a declared product-indexed subset of system states be

\[
S^* \cong I\times E_1\times\cdots\times E_q.
\]

No transition closure or reachability from an unspecified initial state is needed
for this theorem. Assume that one legal future word uniformly decodes the inside
coordinate and that, for each exterior factor, one legal future word uniformly
decodes that factor over every setting of the remaining coordinates. Then every
exact open interface is injective on `S*`, hence

\[
K_{\mathrm{open}}
\ge
\log_2 |I|+\sum_{j=1}^{q}\log_2|E_j|.
\]

The proof is an injection argument: any two distinct product states differ in
some coordinate, and the declared decoder for that coordinate produces different
legal future behaviour.

### Corollary: extension--compression noncommutation

For each closed context `j`, assume a supplied exact interface factors through
`(I, E_j)`. This yields the **upper bound**

\[
K_{\mathrm{closed},j}\le \log_2|I|+\log_2|E_j|.
\]

Combining the open lower bound with the largest of these closed upper bounds gives

\[
K_{\mathrm{open}}-
\max_jK_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-
\max_j\log_2|E_j|.
\]

The word “upper bound” is essential. A factorization through `(I, E_j)` alone does
**not** imply that the closed minimal interface has exactly `|I||E_j|` states; it
can be smaller. Equality is established only for the explicit binary witness,
where the closed grammar also has decoders for both retained coordinates.

### Theorem B: conservative portability criterion

A common finite summary schema remains exact across a declared finite nested
composition chain when old macro meanings are preserved and each newly legal
action has one availability status and one macro successor inside every proposed
macro fiber. This is a sufficient constructive result, not a universal dichotomy.

## Robustness assessment

### What is robust now

- The exact-interface semantics explicitly checks current output, legal-action rows, and successor labels; the regression suite includes output, legality, and successor counterexamples.
- The operational addressability witness checks explicit decoder traces uniformly across all product-coordinate settings, not merely a cardinality table.
- The relay construction verifies macro-time conjugacy to the coordinate witness while keeping node states, message alphabet, pairwise communication, and maximum degree bounded.
- The conservative schema checks both a positive finite expansion witness and local failure modes: changed old-action meaning, nonuniform availability, and nonuniform successor labels.
- The dedicated paper-core replay records theorem provenance, selected finite witnesses, and scope limits in a machine-readable artifact.

### What must be preserved before submission

1. **Proof versus replay.** The analytic injection theorem must appear as a self-contained LaTeX proof. Certificates replay declared finite instances and do not discover an ecological grammar or decoder word.
2. **Product subset wording.** The theorem uses a declared product-indexed subset. Do not add transition closure or reachability claims unless an application separately supplies them.
3. **Closed-context wording.** Treat factorization through `(I, E_j)` as a closed upper bound. Claim equality only when the closed grammar itself decodes both retained coordinates.
4. **Local versus global grammar.** The relay construction has a constant local node/message grammar and degree bound, while the family still has port-specific choices whose number grows with `m`.
5. **Finite deterministic domain.** The results do not cover noise, stochastic transitions, continuous states, simultaneous reader firings, hidden-state learning, grammar discovery, or arbitrary infinite composition processes.
6. **Novelty boundary.** Fixed-grammar exact quotients are adjacent to standard automata/bisimulation and state-abstraction ideas. The paper must claim novelty only for the extension-grammar lower bound, its operational-addressability proof route, and the matching bounded-locality witness.

See [paper-core mathematical audit](paper_core_audit.md) for the complete
proof-versus-replay record and GitHub Actions contract.

### Robustness verdict

The central theorem family is mathematically viable for a theorem-first paper.
There is no contradiction in the conditional injection argument, finite relay
witness, or conservative-schema boundary. The principal risk is overstatement of
assumptions or treating finite replay as a general proof; both are now explicit
scope restrictions rather than hidden gaps.

## Figures and reusable material

1. **Closed versus open composition figure.** Draw one focal node with `m` dormant exterior modules. A closed context opens one port; the open grammar permits any future port. Caption the memory contrast `2` versus `m + 1` bits in the binary witness.
2. **Proof figure.** Show two product states differing in coordinate `j`, followed by the corresponding decoder word and a distinct output trace. This visualizes the injection proof rather than a generic state-space explosion.
3. **Relay sharpness figure.** Use a balanced binary relay tree with a one-token reader event. Label only local states/messages and maximum degree 3; do not imply a fixed global port alphabet.
4. **Positive-boundary figure.** Show one macro fiber that remains valid when a new action is uniform, versus one that splits when availability or successor differs.
5. **Optional ecological reading.** A focal patch, dormant sources, and one future connection event. Label this as a synthetic model contract, not a data example.

## Repository partition and migration policy

### This repository: `rach-causal-invariants`

Keep only:

- the frozen finite deterministic theorem package;
- proof-oriented documentation, certificates, deterministic replays, and CI;
- corrections that narrow claims, improve reproducibility, or repair regressions;
- release tags and a permanent theorem-to-manuscript traceability record.

Do not add manuscript prose, bibliography churn, exploratory simulations, empirical data, fitted models, approximate/stochastic extensions, or a new theorem family here.

### New manuscript repository: `rach-open-composition-paper`

Create this as the active submission workspace. It should contain:

- `manuscript/` for LaTeX, bibliography, journal style files, and cover letter;
- `figures/` for publication figures generated only from declared synthetic models;
- `literature/` for the novelty matrix and reading notes;
- `supplement/` for theorem proofs, reproducibility note, and a pinned RACH commit hash;
- `traceability/` mapping every manuscript theorem/figure to a RACH theorem ID and test/replay route.

The paper repository may quote a fixed RACH release but must not mutate RACH theory to make prose easier.

### New future-work repository: `rach-open-composition-next`

Move all non-submission research here after the manuscript scope is frozen:

- approximate, stochastic, continuous, simultaneous-action, or hidden-state domains;
- grammar discovery and learning from observations;
- candidate-mechanism uncertainty beyond the companion package;
- empirical ecological contracts, data ingestion, and case studies;
- additional transport variants, panel designs, robustness questions, or new witnesses.

Every issue moved there must begin by naming whether it changes a theorem assumption, a conclusion, or only an application domain. It must not be backported into RACH without a new canonical-claim decision.

## Immediate migration checklist

- [ ] Create a release tag for the frozen RACH theorem package after the audit PR is merged.
- [ ] Create `rach-open-composition-paper` and transfer Issue #99 there as the manuscript project tracker.
- [x] Open the literature novelty matrix in the paper workspace before drafting the Introduction.
- [x] Convert Theorem A, its injection proof, and the relay sharpness construction into self-contained LaTeX.
- [x] Keep `EXT-1`--`EXT-4` outside the manuscript theorem package.
- [x] Close historical RACH issues #39 and #41 as superseded by the frozen registry; retain links to their recovered theorem IDs.
