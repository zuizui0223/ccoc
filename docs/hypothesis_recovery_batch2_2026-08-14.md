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
| `REC-18` | Do local contraction / small-gain assumptions yield an approximate finite-radius causal blanket or bounded truncation error? | **DEFERRED / NOT PURSUED AS A CCOC THEOREM.** | unmerged PR #158 `next_math_candidate_triage_2026-08-13.md` | The mathematical direction was judged sensible but left outside the CCOC theorem program; later stochastic portability does not prove this generic contraction statement. |
| `REC-19` | Can data or solver output be converted end-to-end into a retained completion/mechanism family and then into a candidate-safe open-law verdict under explicit coverage assumptions? | **PARTIALLY PREPARED, NOT IMPLEMENTED END-TO-END.** | `docs/promotion_calculus.md` “Evidence bridge” target; later `mechanism_to_data_bridge_2026-08-14.md` | The later bridge specifies observable/falsification contracts but intentionally does not infer grammar/completion families from empirical data. Operationally this now sits under `HYP-J01`. |
| `REC-20` | Do biologically structured non-product composition constraints beyond fixed richness—e.g. forbidden guild combinations, trophic feasibility, occupancy matroids, or spatial compatibility—produce genuinely new sharp inflation families? | **DEFERRED / NOT PURSUED.** | `docs/composition_code_rate.md` open question | Current policy stops proliferation of new codebook families unless they change the theorem, not merely instantiate the same rate corollary. |
| `REC-21` | Can the cheapest NULL-observation panel that makes a focal mechanism the last surviving driver be solved exactly rather than greedily? | **PROVED / LEGACY DESIGN.** Dynamic programming over cumulative eliminated-mechanism sets gives the exact minimum-cost panel under the monotone-OR contract. | `docs/minimum_discriminating_panels.md`; `observation_design.py` | Conditional design theorem after the candidate grammar and faithful NULL semantics are declared. |
| `REC-22` | Does the minimum-cost / coverage-greedy structurally resolving panel remain optimal when misspecification and observation risk are considered? | **REFUTED AS A UNIVERSAL DESIGN RULE; finite robust alternatives IMPLEMENTED.** Exact finite scenario enumeration supports minimax and weighted-mean risk objectives, and budget can change the recommended panel. | `docs/robust_panel_design.md`; `robust_panel_design.py` | Robustness is only against the declared scenario family and weights; not unknown-unknown protection. |
| `REC-23` | Can the two-driver misspecification benchmark be generalized to multiple competitors, latent routes, correlated environments, shared/imperfect witnesses, costs, and robust panel objectives? | **SUBSTANTIALLY RECOVERED ACROSS SUCCESSIVE LEGACY MODULES.** Multi-competitor/correlated-environment benchmarking was implemented, then shared/imperfect/cost-sensitive design was covered by robust-panel machinery. | `generative_misspecification_benchmarks.md`; `multi_competitor_panel_phase_benchmarks.md`; `robust_panel_design.md` | Methods/benchmark lineage, not the open-composition theorem. |
| `REC-24` | Can an ecological rule observed in a plot/island/survey window be reported explicitly as grammar-certified versus merely observation-window-conditioned? | **FORMALIZED AS AN INTERPRETATION CONTRACT; EMPIRICAL INSTANTIATION UNRESOLVED.** | `docs/observation_window_completion.md` H5; later mechanism-to-data bridge | Conceptual ancestor of `HYP-J01/J02`; the theorem does not infer the correct completion grammar from data. |
| `REC-25` | Can the finite closure certificate language be generalized to rational stochastic systems that distinguish convergence to a stationary distribution from deterministic recurrence and stochastic recurrent sign reversal? | **DEFERRED / NOT PURSUED.** | `docs/causal_closure_calculus.md` “Next mathematical extension” | Later stochastic ecology addresses a different portability question and does not solve this general stochastic closure-classification problem. |

## What these recoveries change

They change the **completeness of the hypothesis history**, not theorem truth and not novelty.

In particular:

- `REC-01`, `REC-04`, `REC-05`, `REC-06`, `REC-08`, `REC-14`–`REC-17`, `REC-21`, and much of `REC-23` are decided results that were previously bundled too coarsely.
- `REC-02`, `REC-09`, `REC-10`, and `REC-22` preserve hypotheses that were false or never established in their original broad form.
- `REC-07`, `REC-12`, `REC-18`, `REC-20`, and `REC-25` are deliberately **deferred/not-pursued**, not active scientific gaps.
- `REC-11`, `REC-13`, `REC-19`, `REC-23`, and `REC-24` were partially or substantially absorbed by later theorem/application-control families rather than solved under their original broad wording.

## Unmerged-PR recovery check

The repository has only three closed unmerged PRs in the current history search:

- PR #31 — scientific e-process hypotheses recovered already as `HYP-A09`;
- PR #158 — primary-source handoff was rescued to main, while its discarded next-math triage yielded `REC-18` plus four candidate classes that were later actually pursued (converse, resource tradeoff, stochastic portability, ecological structural theorem);
- PR #165 — identical theorem head superseded by merged PR #166; no lost hypothesis.

Thus there is no additional unmerged scientific branch currently hidden from the recovery record.

## Active-open status after this batch

This batch does **not** add a new active theorem target. The active scientific open set remains:

1. scalable feedback-memory / feedback-portability beyond the five-state benchmark;
2. one real application with the transition/recruitment/movement layer needed to identify a CCOC structural mechanism.

`REC-19` and `REC-24` are methodological/interpretive forms of the second item, not independent active programs. Historical H1–H4 remain literature-comparison hypotheses, not mathematical gaps.

## Next recovery pass

Continue reverse indexing through:

1. explicit false starts recorded only in PR comments or review corrections;
2. scientific module/doc “future work”, “open question”, “not proved”, and “non-claim” clauses not already covered here;
3. early benchmark/design modules that were never given a theorem-candidate issue.

Only after these sources map cleanly to the canonical ledger should novelty adjudication resume.