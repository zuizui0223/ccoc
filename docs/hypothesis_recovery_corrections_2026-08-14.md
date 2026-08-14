# CCOC hypothesis recovery — correction and proof-scope pass (2026-08-14)

> **Purpose:** recover hypotheses that were once stated or implicitly used too broadly and were later corrected. These are scientific/proof-scope records, not novelty decisions.

## Corrected hypotheses

| Recovery ID | Earlier hypothesis / inference | Correct status | Correction source | Permanent rule |
|---|---|---|---|---|
| `REC-34` | If a compiled observable trace determines the source trace, then a compiler automatically preserves the source closed/open response quotient separation. | **REFUTED AS A SUFFICIENT COMPILER CONTRACT.** One-way decodability preserves source distinctions but may add spurious compiled distinctions. Exact transfer of both the small closed quotient and large open quotient requires two-way response-trace faithfulness on the embedded comparison domain. | PR #139; `docs/universal_compilation_reduction_risk.md` | Never infer preservation of source equivalences from one-way simulation. This is the logical reason `HIST-H3` asks for two-way faithfulness. |
| `REC-35` | A product-indexed comparison domain used in the addressability theorem must be a reachable or transition-closed subsystem. | **REFUTED / SCOPE CORRECTED.** The lower bound only needs the declared jointly realizable comparison states and legal decoder words; the readout witness may leave the comparison set after the query. | PR #102 paper-core audit; later `portability_core_v1.md` | Do not silently strengthen theorem premises to reachability/transition closure, and do not claim either property from the certificate. |
| `REC-36` | A closed factorization through `(I,E_j)` proves the minimal closed exact interface has exactly `|I||E_j|` states. | **REFUTED / SCOPE CORRECTED.** Factorization supplies a closed-interface upper bound; equality requires explicit closed separation/decoder evidence and holds in the declared equality witnesses. | PR #100/#102 paper-core audit | Keep inequality direction explicit in every manuscript use. |
| `REC-37` | Finite exhaustive certificate replay for selected sizes proves an all-parameter theorem. | **REFUTED AS PROOF LOGIC.** Replay verifies declared finite objects; analytic arguments establish the quantified theorem. | PR #102 paper-core audit; current workflow discipline | Keep analytic proof and executable regression as distinct evidence layers. |
| `REC-38` | The historical CORE-3 relay already had a size-independent global action alphabet because its local node/message grammar was constant. | **REFUTED / TERMINOLOGY CORRECTED, THEN STRENGTHENED LATER.** Original port-labelled choices grew with `m`; fixed four-symbol global control was achieved only in the later addressed/fixed-regular constructions (`REC-32`). | PR #100 audit; PR #109; PR #160 | Distinguish local grammar complexity from external/global control alphabet complexity. |
| `REC-39` | Failure of an implementation-specific transport, conservative schema, or proposed merge is itself evidence that no exact macro-law exists. | **REFUTED AS A GENERAL INFERENCE.** Such failures only refute the supplied certificate/merge unless an independent canonical lower-bound/converse applies. | claim-status audit; CORE-5 and EXT scope corrections | Keep local obstruction, certificate failure, and global impossibility as separate statuses. |

## Relation to the main ledger

Several of these ideas appear in abbreviated form in the main ledger's permanent scope-correction list. They are repeated here deliberately because the **earlier false inference itself** is part of the recovered hypothesis history and should be visible before novelty adjudication.

`REC-34` is especially important: H1–H4 source recovery asks whether classical compilers satisfy the corrected contract, but the need for H3 is already a resolved CCOC proof-logic issue rather than a literature question.

## Result of correction pass

The main known proof-scope reversals are now accounted for:

- grammar completion monotonicity failure (#162 → #163/#164) is already `HYP-E03/E04/E05/E06`;
- degree-only latency is already `HYP-C13`;
- stagewise-small ⇒ coherent portability is already `HYP-C05`;
- comparison-domain ⇒ full-system bound is `REC-33`;
- one-way simulation ⇒ quotient faithfulness is `REC-34`;
- reachability/transition-closure over-strengthening is `REC-35`;
- factorization equality is `REC-36`;
- replay-as-proof is `REC-37`;
- local/global alphabet conflation is `REC-38`;
- local certificate failure ⇒ global impossibility is `REC-39`.

No novelty status is assigned here.