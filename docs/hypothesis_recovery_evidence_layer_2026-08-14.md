# CCOC hypothesis recovery — early symbolic/evidence layer (2026-08-14)

> **Purpose:** de-bundle the early RACH evidence mathematics that PR #201 compressed into broad A03–A08 rows. These are retained as historical mathematical/evidential hypotheses, not first-paper novelty claims.

## Recovered evidence hypotheses

| Recovery ID | Question | Current status | Source | Scope |
|---|---|---|---|---|
| `REC-44` | Does confidence-set lifting fundamentally require a finite enumerated candidate universe, or can it operate on an arbitrary symbolic/continuous/mixed candidate space using feasibility queries? | **PROVED.** For arbitrary `Theta`, valid joint retained-set coverage plus jointly valid decisive solver semantics gives false-decisive risk `<= alpha+beta`. | PR #9/#11; `docs/symbolic_candidate_set_lifting.md` | Candidate-universe adequacy remains an external assumption; `UNKNOWN` solver status is `UNSUPPORTED`, not evidence of both motif values. |
| `REC-45` | If a declared retained candidate universe is enlarged by inclusion, which decisive conclusions are preserved and how should a narrow conclusion that disappears be reported? | **PROVED.** Outer `INVARIANT/EXCLUDED` implies the same inner status; inner `UNRESOLVED` remains unresolved outward. A narrow decisive result lost under expansion is `SCOPE_FRAGILE`, not automatically false. | PR #14; `docs/nested_universe_stability.md` | The outer envelope is declared, not proven to contain nature. |
| `REC-46` | Can symbolic inner-to-outer candidate-set inclusion be treated as true from descriptions or numerical failure to find a counterexample? | **REFUTED AS AN INFERENCE; exact certificate route PROVED.** A joint inclusion certificate is required; for rational conjunction-only polyhedra, exact rowwise Farkas implication plus a nonempty inner witness can set the inclusion error `gamma=0`. | PR #15/#17; symbolic outer-envelope and rational-inclusion docs | A numerical search failure is not an inclusion proof. |
| `REC-47` | Can a finite collection of exact inclusion checks certify inner⊆outer at every future sequential look? | **REFUTED AS AUTOMATIC; restricted all-look schema PROVED.** With fixed outer polyhedron, verified base inclusion, and inner updates that retain every base row while adding constraints, deterministic admission yields all-look `gamma=0`. | PR #18; `docs/online_monotone_polyhedral_inclusion.md` | Only admitted looks under the monotone rational-polyhedral update schema are covered. |
| `REC-48` | Does exact SAT/UNSAT verification of caller-supplied `active` and `inactive` systems guarantee those systems really encode a motif and its complement? | **REFUTED; compiler solution PROVED for a finite tagged rational-polyhedral union.** Differently tagged overlapping cells require exact separation proofs; compiler-generated branch systems then enforce the active/inactive semantics. | PR #23; `docs/proof_carrying_polyhedral_motif_compiler.md` | Tags and declared union semantics are still supplied; nonlinear/integer/general Boolean complement compilation is outside scope. |
| `REC-49` | Can the tagged finite-union motif compiler be integrated with the all-look inner/outer admission path while retaining exact solver/inclusion semantics and optional-stopping soundness? | **PROVED in the declared finite-union/rational setting.** Compiler-generated branch proofs plus fixed tagged union and monotone ambient inclusion yield all-look `beta=gamma=0`; with external all-look coverage, false decisive/stability risk is bounded by `alpha`. | PR #24; `docs/all_look_compiled_polyhedral_admission.md` | Does not establish statistical coverage, candidate-universe completeness, tag truth, or safety of bypassed manual-query looks. |
| `REC-51` | Before the finite-union compiler existed, could exact rational solver proofs and exact inner⊆outer admission be bound to the **same single-polyhedron sequential snapshot**, so solver-semantic and inclusion errors simultaneously satisfy `beta=gamma=0` at every admitted look? | **PROVED.** A shared nonempty retained system is enforced across motif queries in each cell; exact SAT/UNSAT proofs and the monotone inclusion gate are jointly checked before constructing the paired snapshot. | PR #19; `docs/exact_all_look_polyhedral_extension_admission.md` | Applies only to rational non-strict conjunction systems, fixed outer envelope, base-row-preserving inner updates, and looks routed through the admission gate. Motif active/inactive semantic encoding remained a separate assumption, later addressed by `REC-48/49`. |

## What remains engineering/provenance rather than a separate scientific hypothesis

The later canonical-JSON, hash-chain, signed-checkpoint, tiered-manifest, replayable-proof, and transcript-integration PRs strengthen artifact integrity and auditability. Their scientific content is already captured by the evidence-validity premise in the rows above and by `HYP-A08`; they are **not** each promoted to separate hypothesis rows merely because they introduced a new serialization/provenance format.

One substantive exception is the unmerged finite e-process coverage backend, already recovered as `HYP-A09`.

## Recovery consequence

The early evidence program had a real mathematical progression:

```text
finite retained sets
→ arbitrary symbolic candidate spaces
→ nested / outer-envelope scope stability
→ exact inclusion certificates
→ all-look inclusion schema
→ exact single-polyhedron solver+inclusion admission
→ semantics-safe motif query compiler
→ all-look compiler-admitted finite-union path
```

This progression is now explicit instead of being collapsed into a generic “proof/evidence binding” row.