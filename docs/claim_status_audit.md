# CCOC current claim and proof-status audit — 2026-08-17

> **Status:** current control document. Historical theorem families and removed executable branches remain recoverable in Git history and `docs/historical_theorem_archive.md`; they are not current CCOC claims.

## Proof-status vocabulary

- **Analytic + executable** — quantified proof is written and finite replay/tests check the implementation.
- **Analytic only** — proof is written; a dedicated replay is not required or not linked.
- **Executable only** — finite code/oracle exists but is not a substitute for a quantified proof.
- **Supporting boundary** — valid theorem/obstruction that is not a headline CCOC novelty claim.

A passing certificate does not establish historical novelty and does not validate a real ecosystem.

## CORE-1 — exact grammar-aware dynamic interface

- **Registry tier:** headline foundation.
- **Status:** analytic + executable.
- **Claim:** for a declared finite deterministic controlled system and grammar, the legal-word response quotient is the coarsest exact deterministic interface preserving output and legal successors.
- **Analytic proof:** `docs/dynamic_boundary_blankets.md`, especially finite-horizon stabilization and dynamic-interface completeness.
- **Executable modules:** `causal_model/dynamic_boundary_blankets.py`, `causal_model/grammar_aware_blankets.py`, `causal_model/shared_grammar.py`.
- **Tests:** `tests/test_dynamic_boundary_blankets.py`, `tests/test_grammar_aware_blankets.py`, `tests/test_shared_grammar.py`.
- **Do not claim:** fixed-grammar minimization or right-congruence refinement is historically new, or the supplied grammar is automatically the correct ecological contract.

## CORE-2 — addressable-completion lower bound / extension–compression noncommutation

- **Registry tier:** headline theorem.
- **Status:** analytic + executable.
- **Claim:** joint realizability plus concrete legal decoder words force an injective open interface on the declared comparison family; supplied closed-context factorizations then yield the cross-grammar gap.
- **Analytic proof:** `docs/extension_compression_noncommutation.md`; canonical framing in `docs/portability_core_v1.md`.
- **Executable modules:** `causal_model/extension_compression_noncommutation.py`, `causal_model/operational_addressability.py`.
- **Tests:** `tests/test_extension_compression.py`, `tests/test_operational_addressability.py`.
- **Proof core:** two product states differing in any coordinate are separated by the declared future word decoding that coordinate; therefore no exact open interface can merge them.
- **Do not claim:** exterior memory adds without joint realizability and operational separation, or this is a source-relative repair theorem for one inherited partition.

## CORE-3 — bounded-local extremal sharpness

- **Registry tier:** headline sharpness support.
- **Status:** analytic all-`m` proof + executable finite-`m` replay.
- **Claim:** the explicit fixed-regular relay family realizes the closed/open gap with one fixed four-symbol primitive alphabet, one newly legal primitive action, pairwise local messages, degree at most three, and bounded local alphabets.
- **Analytic proof:** `docs/fixed_regular_extremal_theorem_2026-08-13.md`, Steps 1–7.
- **Executable modules:** `causal_model/fixed_regular_grammar_relay.py`, `causal_model/extremal_open_composition.py`, `causal_model/relay_tree_compilation.py`, `causal_model/constant_alphabet_relay.py`.
- **Important boundary:** a finite certificate for supplied `m` is not the proof of the all-`m` theorem; the construction/induction in the theorem document is.
- **Do not claim:** bounded degree alone forces inflation or the generic automata/routing substrate is historically novel.

## CORE-4 — conservative exact portability boundary

- **Registry tier:** supporting boundary.
- **Status:** analytic + executable sufficient criterion.
- **Claims:**
  - common macro output/action/transition dynamics plus label-coherent embeddings give one exact law across declared nested stages;
  - monotone legal-action expansion with unchanged old meanings and label-deterministic new actions gives one conservative finite macro schema.
- **Analytic proofs:** `docs/coherent_portable_macrolaw.md`, `docs/conservative_macro_schema.md`.
- **Executable modules/tests:** `causal_model/coherent_portable_macrolaw.py`, `causal_model/conservative_macro_schema.py` and their dedicated tests.
- **Do not claim:** these conditions are necessary for every portable law or they construct the unique minimal repair of an inherited source law. The latter belongs to MLTR.

## CORE-5 — future-word / new-action fiber split

- **Registry tier:** supporting boundary.
- **Status:** analytic + executable local obstruction.
- **Claim:** if a legal future word or newly legal action produces different traces or successor labels from two states inside one proposed macro fiber, that proposed merge is invalid.
- **Proof:** direct contradiction with exact deterministic factorization; documented with CORE-4.
- **Do not claim:** one split rules out every alternative macro-law or proves a global interface lower bound.

## Retained strengthenings outside the CORE-1–5 headline registry

Two current quantitative strengthenings are intentionally not promoted to additional headline theorems:

1. **Constrained codebooks** — `addressable_codebooks.py`, `codebook_families.py`; weakens the full Cartesian-product premise while retaining an operational code-size lower bound.
2. **Approximate addressability** — `approximate_addressability.py`; bounded decoding error retains an information lower bound via standard Fano/information machinery.

They are meaningful extensions of CORE-2, not separate CREST axes.

## Current ownership firewall

- open-future minimum-interface complexity → **CCOC**;
- fixed inherited-law transport / unique coarsest source-relative repair / defect / history → **MLTR**;
- retained mechanism disagreement and candidate-safe state → **MRM**;
- finite/noisy evidence, failure architecture, calibration, and risk-limited reportability → **CED**.

Removed feedback, evidence/panel, proof-carrying admission, ecological-special-case, generic converse, and other historical branches are not current proof obligations merely because their conclusions remain valid in Git history.

## Review rule

Any manuscript statement stronger than the proof source listed above must be weakened or supplied with a new proof before use. CI success alone cannot promote an executable witness into a quantified theorem.
