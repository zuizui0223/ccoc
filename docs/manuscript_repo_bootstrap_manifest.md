# `rach-open-composition-paper` bootstrap manifest

> **Purpose.** This is a transfer manifest, not manuscript prose. It defines the
> minimal publication workspace to create once `zuizui0223/rach-open-composition-paper`
> exists. It prevents theorem/code history, novelty-control notes, and manuscript
> text from being mixed back into the CCOC theorem archive.

## 1. Source snapshot represented by this manifest

This manifest was prepared from CCOC `main` after the August 2026 novelty-control
cleanup, including:

- manuscript theorem traceability record;
- paper-core replay pin;
- residual novelty go/no-go decision;
- fixed-input/unit-delay compiler prior-art audit;
- corrected universal-compiler faithfulness contract;
- H1–H4 compiler source audit;
- Tier A same-system/nested-grammar quantitative prior-art boundary;
- approximate-addressability companion theorem, explicitly outside the exact
  first-paper CORE facade.

**Do not treat this file as the final submission pin.** At transfer time, resolve
and record the then-current CCOC `main` SHA and the latest successful exact
paper-core replay separately.

## 2. Target repository

Repository:

`zuizui0223/rach-open-composition-paper`

Recommended initial state:

- private while drafting;
- default branch `main`;
- initialized with README;
- no copied `causal_model/` package;
- theorem code remains authoritative in `ccoc`.

Manual repository creation is tracked by issue #141 because the current connected
GitHub tool surface cannot create repositories.

## 3. Initial directory contract

Create only this publication-facing structure initially:

```text
rach-open-composition-paper/
  README.md
  manuscript/
    main.tex
    sections/
      01_introduction.tex
      02_formal_setup.tex
      03_noncommutation_theorem.tex
      04_codebook_strengthening.tex
      05_sharpness_relay.tex
      06_positive_portability.tex
      07_ecological_interpretation.tex
      08_discussion.tex
    references.bib
  supplement/
    theorem_proofs.tex
    reproducibility.tex
    related_work_audit.tex
  figures/
    README.md
  traceability/
    CCOC_PIN.md
    THEOREM_MAP.md
    CLAIM_BOUNDARY.md
    REPLAY_PIN.md
  submission/
    cover_letter.tex
    reviewer_candidates.md
```

This is a file-location contract only. Manuscript prose should be drafted in the
new repository after creation, not copied into this theorem archive.

## 4. Main-paper theorem spine to transfer

The first manuscript must remain narrow.

### Formal substrate

- finite deterministic controlled system;
- declared legal future-word grammar;
- exact grammar-aware response quotient / exact interface.

This is **substrate**, not a novelty claim.

### Main theorem — Tier A

Cross-grammar extension–compression noncommutation on one fixed deterministic
plant:

- source state space / transition table / output map fixed;
- closed and open legal-future grammars compared on that same plant;
- operationally addressable codebook/product coordinates force a large exact open
  response quotient;
- fixed closed contexts admit small exact factorizations.

The novelty candidate is the **same-system nested-grammar response-interface lower
bound under explicit operational decoder assumptions**.

Do not market contextual minimization, input restrictions, state blow-up, or
observer-relative equivalence separately as new.

### Quantitative strengthening

- arbitrary finite addressable codebooks, not only full Cartesian products;
- parity / fixed-richness examples as robustness to compositional constraints;
- one-new-action maximal finite-domain innovation as a clean sharpness statement.

The algebraic common-refinement/product-capacity accounting is supporting
substrate, not the headline.

### Sharpness witness

Use the degree-three/fixed-control relay to show the lower bound does not require a
centralized lookup table or growing local interaction grammar.

The relay is **supporting/constrained sharpness**, not a historical firstness claim
while issue #122 remains open.

### Positive boundary

Use the conservative finite portability criterion as the constructive counterpart:
when outputs, legal-action rows, and successors remain factorable through one
finite coherent schema, an exact portable macro-law survives the declared
composition/action growth.

Treat it as sufficient, not a complete converse.

## 5. Material explicitly outside the first paper

Do not migrate these into `manuscript/` except perhaps one sentence in limitations
or future work:

- delayed/adaptive closure-identifiability no-go branch;
- candidate-mechanism uncertainty and joint candidate/exterior laws;
- budgeted/reset/robust experimental panel theory;
- legacy closure-calculus utilities;
- non-nested replacement/transport-defect program;
- approximate-addressability Fano theorem.

The approximate theorem may be mentioned later as evidence that the exact gap is
not purely a zero-error artifact, but it is not part of CORE-1–CORE-5 and must not
expand the first-paper theorem spine unless a manuscript decision explicitly
changes.

## 6. `traceability/CCOC_PIN.md` contents at transfer time

Record exactly:

- CCOC repository URL;
- final source `main` SHA used by manuscript;
- theorem registry version / IDs;
- exact files used for each manuscript theorem;
- whether any later CCOC commit changes theorem semantics or only documentation;
- status of open historical-novelty issues (#122 and any source-acquisition
  blockers).

Never write “latest” without a SHA.

## 7. `traceability/REPLAY_PIN.md` contents

Carry forward the permanent logic from `docs/paper_core_replay_pin.md`:

- exact theorem-code SHA corresponding to the successful paper-core replay;
- workflow run ID and conclusion;
- artifact/report identifiers if still available;
- comparison showing whether later source-head changes touched theorem/test/script
  files;
- replacement run if theorem-code paths changed after the existing pin.

The replay is a finite certificate/provenance surface, not the analytic proof.

## 8. `traceability/THEOREM_MAP.md`

Map manuscript labels to CCOC provenance rather than copying Python into the paper
repo.

Recommended manuscript labels:

- **Definition 1:** grammar-aware exact response interface;
- **Lemma 1:** grammar monotonicity / response refinement;
- **Theorem 1:** addressable-completion/codebook lower bound;
- **Corollary 1:** extension–compression noncommutation gap;
- **Proposition 1:** constrained codebook families;
- **Theorem 2:** explicit bounded-local sharpness realization;
- **Theorem 3:** conservative finite portability criterion.

`CORE-1`–`CORE-5` remain provenance IDs, not necessarily manuscript theorem
numbers.

## 9. `traceability/CLAIM_BOUNDARY.md`

Start with three bins.

### Allowed headline candidate

> Compression under each fixed closed response grammar need not commute with
> opening the admissible response grammar on the same deterministic system; under
> explicit operational addressability assumptions the exact open interface can be
> forced to retain substantially more response information.

### Allowed supporting statement

> The separation has an explicit fixed-control, degree-three local sharpness
> realization and persists under constrained codebooks.

Do not attach historical firstness to the relay while #122 is unresolved.

### Disallowed novelty slogans

Do not claim novelty for:

- Myhill–Nerode-like quotient/minimization;
- input-restricted/contextual state minimization;
- common refinement/product-capacity algebra;
- exponential state blow-up by itself;
- one new action/word splitting a state class by itself;
- repeated identical modules;
- fixed-input modular synthesis;
- delayed fixed-module realization;
- bounded fan-in/fan-out realization as a broad idea;
- generic causal-cone/locality bounds;
- Fano/rate-distortion or approximate abstraction.

## 10. Related-work transfer checklist

The new repository's `supplement/related_work_audit.tex` should distinguish at
least four neighborhoods.

1. **Fixed-grammar/state-minimization substrate:** Myhill–Nerode, deterministic
   transducers, bisimulation/state abstraction, predictive state ideas.
2. **Context/input-restricted minimization:** Kim–Newborn lineage, interacting-FSM
   don't-cares, Tail Minimization, conformance testing under input restrictions.
3. **Descriptional/state-complexity blow-up:** partial/incompletely specified
   automata and related succinctness/state-complexity results; these prevent
   “exponential blow-up itself is new” wording.
4. **Uniform/local sequential-machine realization:** Hsieh–Tan–Newborn,
   Weiner–Hopcroft, Ullman–Weiner, Arnold–Tan–Newborn, Newborn–Arnold, Williams,
   and later decomposition theory.

Issue #122 controls the unresolved historical compiler comparison. The corrected
compiler audit asks for H1–H4:

- bounded local resources;
- fixed context-independent controls;
- two-way response-trace faithfulness;
- bounded timing/output latency.

Under the latter two semantic/control conditions, same-hardware sublanguage
restriction is derived rather than an independent compiler clause.

## 11. Figure contract

Prepare four figures only unless the manuscript clearly needs fewer.

1. **Closed versus open grammar:** same plant, different allowed future response
   words, quotient refinement.
2. **Addressable codebook / lower-bound mechanism:** distinct dormant coordinates
   exposed by declared future probes.
3. **Local sharpness witness:** binary selector + relay/pulse return, with degree
   and fixed-control constraints visible.
4. **Positive portability boundary:** finite macro schema that remains coherent as
   composition/actions expand.

Figures must explain the mathematics, not advertise repository architecture.

## 12. Proof-writing contract

The LaTeX supplement must prove the main analytic statements independently of
Python replay.

At minimum write out:

- exact response-equivalence definition;
- pair-separation injection proof for the codebook theorem;
- derivation of the closed/open memory gap using closed **upper bounds**;
- conditions for equality in the sharp witness;
- explicit local relay realization and its locality/control bounds;
- finite portability factorization proof.

Do not cite passing unit tests as the proof.

## 13. Migration sequence after repository creation

1. Re-read CCOC `main` and record the exact transfer SHA.
2. Re-check #122 and allowed novelty wording.
3. Re-check the latest exact paper-core workflow run; refresh it only if theorem-
   code paths changed.
4. Create the target directory structure from section 3.
5. Populate the four traceability files before writing Introduction/Discussion.
6. Create a compile-minimal LaTeX skeleton.
7. Draft theorem statements/proofs first.
8. Draft Introduction and ecological interpretation only after theorem wording and
   related-work boundary are stable.
9. Add figures, abstract, cover letter, and reviewer candidates last.

## 14. Definition of done for the bootstrap

The manuscript repository is ready for substantive drafting when:

- it exists and is writable through the connector;
- the exact CCOC source SHA is pinned;
- theorem/replay/claim-boundary traceability files exist;
- the LaTeX skeleton compiles;
- no theorem code has been copied into the manuscript repo;
- issue #122 status is visible in the claim-boundary file;
- theorem-first section order is established.

Until then, `ccoc` remains the theorem/certificate archive and issue #99 remains the
publication tracker.