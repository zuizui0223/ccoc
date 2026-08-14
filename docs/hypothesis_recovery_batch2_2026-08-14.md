# CCOC hypothesis recovery — batch 2 issue/doc reverse pass (2026-08-14)

> **Purpose:** continue actual hypothesis recovery after PR #201. This file does not evaluate novelty. It records scientific questions that were posed in issues/docs but were compressed away or bundled too coarsely in the first recovery ledger.

## Recovery rule

A row is included when the repository history contains a materially distinct scientific/evidential question, even if it was later absorbed into another theorem, explicitly rejected, deferred, or archived. Pure CI/serialization/manuscript logistics are not hypotheses.

## Recovered omitted / over-bundled hypotheses

| Recovery ID | Original question | Recovered status | Primary repository source | Relation to current theory |
|---|---|---|---|---|
| `REC-01` | If small decoding error is allowed, can the open-interface memory gap collapse to `O(1)`? | **PROVED NO in the declared codebook contract.** For a uniform finite codebook, Fano gives `log2|im(phi)| >= log2|C| - sum_j penalty_j`; on the binary full product, fixed `eps<1/2` leaves `K_open^(eps) >= 1 + m(1-h2(eps))`. | PR #134; `causal_model/approximate_addressability.py`; `docs/approximate_addressability.md` | Separate companion robustness hypothesis; it should not be hidden inside the later retention/update tradeoff. |
| `REC-02` | Does response-type count alone force a `|Q|R` candidate-safe product interface? | **REFUTED as automatic; corrected theorem PROVED under uniform response separation.** | Issue #49; `candidate_safe_laws.py`; `docs/candidate_safe_universal_laws.md` | Distinct from the simpler universal-law iff in `HYP-B11`. |
| `REC-03` | Can candidate response type remain unresolved for an arbitrarily long legal prefix even when every candidate has a small exact instance law? | **PROVED.** Delayed identity/flip candidates agree through horizon `H` and split at `wait^H fire`. | Issue #49; PR #50; `candidate_safe_laws.py` | Mechanism-identifiability analogue of delayed exterior addressability. |
| `REC-04` | Is there a unique minimum exact **exterior-only** boundary blanket under a declared grammar, and when do nested-grammar blankets stabilize? | **PROVED.** `B_Gamma=E/~_Gamma` is the coarsest/minimum exact exterior summary; finite union blanket iff the nested quotient sizes are uniformly bounded, with eventual stabilization in the finite-index case. | Issue #65; PR #66; `canonical_boundary_blankets.py` | Scientifically distinct from the full system-state dynamic-interface quotient in `HYP-B06`. |
| `REC-05` | What can finite sampled completions / tested response cells establish about the canonical blanket? | **PROVED asymmetric evidence result.** Observed signature count is a monotone lower bound; exact blanket size requires explicit completion-class and grammar/panel coverage. Free completion extension prevents transcript-only universal upper bounds. | Issue #67; PR #68; `witnessed_boundary_evidence.py` | `HYP-B08` retained the no-go but not the positive witnessed-lower-bound / coverage-exactness half. |
| `REC-06` | Can the joint exterior + mechanism binary witness be compiled to the same degree-three one-token local architecture? | **SHARPNESS / CONSTRUCTION PROVED for the binary subfamily.** | Issue #57; PR #58; `binary_joint_relay_compilation.py` | Local anti-triviality strengthening of `ID-3`, outside current first-paper spine. |
| `REC-07` | Can the binary joint relay compiler be generalized to arbitrary multi-valued read registers and general modular response updates? | **DEFERRED / NOT PROVED.** Explicitly left outside PR #58 and never promoted later. | Issue #57; PR #58 scope boundary | Historical research branch, not an active current hypothesis unless deliberately reopened. |
| `REC-08` | Can exterior coordinates and retained mechanism type be jointly invisible for an arbitrarily long legal prefix and then become jointly necessary at one later horizon? | **PROVED.** Initial-slice quotient stays one bit through `H`, then full joint memory `m+2` is exposed at `H+1`; no uniform joint closure horizon. | Issue #59; PR #60; `delayed_joint_nonidentifiability.py` | More specific than the separate exterior-delay and candidate-delay rows. |
| `REC-09` | Can removing one small candidate from a candidate family cause an unbounded interface-memory cliff? | **REFUTED / RED-TEAM REJECTED.** Issue #35 explicitly forbids this claim; common-refinement/product accounting bounds the drop by the removed candidate's own interface contribution. | Issue #35 red-team constraint / proposed “no single-candidate cliff” lemma | Never became a headline theorem module; preserve as a rejected research hypothesis. |
| `REC-10` | Is `Delta_0(C)=log|C|-max_j log|pi_j(C)|` a necessary/sharp characterization of cross-grammar inflation for general codebooks? | **NOT PROVED IN THAT GENERAL FORM; SUPERSEDED IN A DELIMITED SUBCLASS.** | Issue #106 unchecked item; Issue #110 / PR #111 | Exact union-grammar subclass is characterized instead by common refinement plus fibered capacity / realizability defect. Do not retroactively claim general necessity for `Delta_0`. |
| `REC-11` | Can coordinate decoders be replaced by a completely general pair-separating future-word premise without changing the theory? | **PARTIALLY RECOVERED / SUBCLASS RESOLVED.** | Issue #106 unchecked item; PR #111 | In the exact union-grammar subclass no coordinate decoders are needed; outside that subclass, the general operational addressability theorem remains decoder/separator-contract based. Not an active priority. |
| `REC-12` | Should post-v1 work pursue composition-dependent candidate-mechanism families? | **DEFERRED / NOT SELECTED.** | Issue #84 P3 decision menu | Non-nested replacement was selected first; later resource/ecology work followed. No dedicated composition-dependent-candidate theorem family was opened. |
| `REC-13` | Should post-v1 work pursue noisy/approximate portability? | **PARTIALLY THEN SUBSTANTIALLY RECOVERED.** | Issue #84 P3; PR #134; PRs #177–#180 | Fano approximate addressability answered robustness of the lower bound; stochastic ecological work later constructed positive finite-horizon approximate portable macros. |
| `REC-14` | Is an exact canonical distinguishing panel exactly a hitting set, and is robustness to `f` independent cell losses exactly an `(f+1)`-multicover? | **PROVED / LEGACY DESIGN.** | Issue #69; PR #70; `robust_canonical_panels.py` | Separate from common-mode robustness in `HYP-B14`; retained as post-quotient design theory. |
| `REC-15` | Can observer-independent and observer-coupled finite dynamics be compared by exact closure-class transitions without claiming observation creates reality? | **PROVED / LEGACY.** | PR #33; `observation_regime_closure.py` | Regime-comparison theorem; distinct from candidate-family consensus. |
| `REC-16` | Can a finite declared mechanism library exhibit observation/intervention **synergy** such that a jointly discriminating panel succeeds while greedy singleton ranking fails? | **PROVED AS A FINITE LEGACY WITNESS.** | PR #1 / early replaceability theorem core | Early methods-layer hypothesis, later demoted from the open-composition paper. |
| `REC-17` | Can a known-truth finite observation channel be exactly self-calibrated for false-invariant / false-exclusion probability under declared sensitivity/false-positive rates? | **PROVED / LEGACY EVIDENCE DESIGN.** | PR #6 and associated observation-envelope modules | Conditional self-calibration, not empirical validation or candidate-universe coverage. |

## What these recoveries change

They change the **completeness of the hypothesis history**, not theorem truth and not novelty.

In particular:

- `REC-01`, `REC-04`, `REC-05`, `REC-06`, `REC-08`, `REC-14`, `REC-15`, `REC-16`, and `REC-17` are decided results that were previously bundled too coarsely.
- `REC-02`, `REC-09`, and `REC-10` preserve hypotheses that were false or never established in their original broad form.
- `REC-07` and `REC-12` are deliberately **deferred/not-pursued**, not active scientific gaps.
- `REC-11` and `REC-13` were partially or substantially absorbed by later theorem families rather than solved under their original broad wording.

## Active-open status after this batch

This batch does **not** add a new active theorem target. The active scientific open set remains:

1. scalable feedback-memory / feedback-portability beyond the five-state benchmark;
2. one real application with the transition/recruitment/movement layer needed to identify a CCOC structural mechanism.

Historical H1–H4 remain literature-comparison hypotheses, not mathematical gaps.

## Next recovery pass

Continue reverse indexing through:

1. all theorem-candidate issues and their closed comments;
2. `legacy/README.md`, `docs/promotion_calculus.md`, and old roadmap/freeze documents;
3. scientific module/doc “future work”, “open question”, “not proved”, and “non-claim” clauses;
4. unmerged branches/PRs that contained scientific hypotheses but never reached `main`.

Only after these sources map cleanly to the canonical ledger should novelty adjudication resume.