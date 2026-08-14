# CCOC hypothesis recovery source-coverage manifest — 2026-08-14

> **Purpose:** document the actual reverse-recovery work used to decide whether the hypothesis inventory is ready for novelty adjudication. This is not a novelty audit and does not claim that a repository search can prove historical scientific completeness outside the repository.

## 1. Recovery target

Recover every materially distinct **scientific/evidential hypothesis posed inside `zuizui0223/ccoc`** through the current pre-novelty recovery phase, including:

- statements later proved;
- broad statements later refuted or corrected;
- sufficient criteria that never became converses;
- explicit open candidates;
- deliberately deferred/not-pursued questions;
- unmerged experimental hypotheses;
- historical H1–H4 comparison hypotheses;
- early methods/evidence hypotheses later archived from the first-paper narrative.

Pure CI, packaging, serialization, signature, branch-retry, manuscript logistics, and source-acquisition mechanics are not separate scientific hypotheses unless they changed an inference/proof-validity assumption.

## 2. Source classes actually inspected

### A. Canonical theorem/status surfaces — complete pass

Read and cross-reconciled:

- `docs/theorem_registry.md` / machine-readable registry role;
- `docs/claim_status_audit.md`;
- `docs/current_architecture.md`;
- `docs/theorem_spine.md`;
- `docs/research_priorities.md`;
- `legacy/manifest.md` and `legacy/README.md`;
- `docs/promotion_calculus.md`;
- `docs/repository_asset_map.md`.

This established the July `CORE/EXT/ID/LEGACY` inventory and the August post-v1 theorem surfaces.

### B. GitHub issues — complete repository issue-set pass

The connector was used to search both the **closed issue set** and the current open issue set. Scientific/theorem issues are mapped in:

`docs/hypothesis_issue_recovery_index_2026-08-14.md`.

The index covers the early roadmap (#2), the open-composition theorem sequence (#35 onward), post-v1 strengthening issues (#106 onward), historical compiler issues (#122/#136/#137), and application issue #199.

Project-control issues are explicitly separated. Accidental #186/#187 contain no content.

**Issue-level recovery status:** closed. No scientifically meaningful issue remains unmapped.

### C. Pull requests — full history metadata pass plus targeted patch reads

Repository PR history through PR #200 was inspected through the connector. Recovery used PR bodies to identify:

- theorem questions that changed scope during implementation;
- explicit “outside this PR”, “next theorem”, and “not proved” clauses;
- proof corrections;
- abandoned or superseded research branches.

Targeted patch/body reads included the paper-core scope correction, compiler-faithfulness correction, binary joint compiler, codebook strengthening, and the discarded next-math triage.

### D. Closed unmerged PRs — complete pass

Only three closed-unmerged PRs were found:

1. #31 — e-process scientific hypothesis, recovered as `HYP-A09`;
2. #158 — source handoff + discarded math triage; contraction/small-gain target recovered as `REC-18`, while the other permitted directions were later pursued;
3. #165 — same theorem head superseded by merged #166; no lost hypothesis.

**Unmerged-PR recovery status:** closed.

### E. Branch-only work — complete branch-name pagination + suspicious-content check

All branch names returned by the connector were paginated; the follow-up page after the initial branch set was empty.

Because many `agent/*` branches were write-safety retries, branch names were not automatically counted as hypotheses. Scientifically suspicious branch families were checked against merged-ready branches.

The strongest suspicious case, `agent/cut-throughput-portability-v2`, contained no independent theorem: its unique `cut_throughput_portability.py` path is only a one-line module docstring, while the substantive theorem is the merged retention–boundary–time result.

Retry families for grammar converse, stochastic ecology, terminal portability, staged materialization, and manuscript/source-control work were classified as duplicate theorem/provenance lineages unless substantive content indicated otherwise.

**Branch-only recovery status:** no unrecovered active scientific hypothesis found.

### F. Scientific docs — broad keyword reverse pass + targeted reading

Repository search was run across multiple recovery phrases, including:

- `hypothesis`;
- `open question` / `open problem`;
- `future work` / `future theorem` / `future direction`;
- `next scientific step` / `Next extension`;
- `not proved` / `unproved` / `not yet`;
- `remains open` / `remains future` / `remains separate` / `remains unknown`;
- `separate strengthening` / `separate theorem` / `separate problem`;
- `conjecture`;
- `false` / correction-oriented terms;
- `TODO`;
- PR searches for `next theorem` and `outside this PR`.

Targeted documents read include, among others:

- dynamic/grammar-aware blankets and observation-window completion;
- delayed addressability and adaptive no-go;
- candidate-safe and joint exterior–mechanism laws;
- canonical/witnessed boundary blankets;
- delayed joint/reset-panel family;
- codebook/composition-code-rate and constant-alphabet relay;
- innovation capacity/local causal cone;
- binary joint relay compilation;
- early replaceability, failure-mode, known-truth, observation-envelope, minimum-panel, misspecification, multi-competitor, and robust-panel docs;
- symbolic candidate lifting, nested/outer envelope stability, rational inclusion, all-look monotone inclusion, exact all-look polyhedral admission, polyhedral motif compiler, and compiler-admitted all-look path;
- early closure calculus and roadmap/freeze documents.

These reads produced `REC-01`–`REC-51`, including rows that were missing from PR #201 because later architecture documents had bundled them too coarsely.

### G. Scientific module inventory — role reconciliation pass

The `causal_model/` directory was enumerated from the pinned main SHA and reconciled against:

- the theorem registry / legacy manifest;
- the current architecture;
- issue/PR recovery rows;
- early evidence/design recovery rows.

Verifier/serialization/audit modules that instantiate one recovered evidence premise are not multiplied into separate hypotheses solely because they are separate Python files.

## 3. Recovery amendments produced in batch 2

- `docs/hypothesis_recovery_batch2_2026-08-14.md` — omitted/over-bundled scientific questions (`REC-01` onward through early methods/failure/scope rows).
- `docs/hypothesis_recovery_corrections_2026-08-14.md` — false or over-broad proof inferences (`REC-34`–`REC-39`).
- `docs/hypothesis_recovery_deferred_and_branch_audit_2026-08-14.md` — deferred strengthening and branch-only checks (`REC-40`, `REC-41`, `REC-43`, `REC-50`).
- `docs/hypothesis_recovery_early_roadmap_2026-08-14.md` — abandoned controlled-generative validation plan (`REC-42`).
- `docs/hypothesis_recovery_evidence_layer_2026-08-14.md` — de-bundled symbolic/all-look evidence mathematics (`REC-44`–`REC-49`, `REC-51`).
- `docs/hypothesis_issue_recovery_index_2026-08-14.md` — issue-to-hypothesis provenance map.
- `docs/hypothesis_recovery_canonical_index_2026-08-14.md` — makes the base ledger plus these recovery appendices one canonical record.

The IDs intentionally preserve historical distinctions even when multiple rows now collapse to one current theorem family.

## 4. Important distinctions recovered

The recovery pass demonstrates why the first PR #201 ledger was not enough by itself. Examples newly restored include:

- approximate addressability as its own robustness hypothesis;
- canonical **exterior-only** blanket minimality versus full dynamic-interface minimality;
- witnessed lower-bound evidence versus blanket exactness;
- binary joint local compilation versus multi-valued/concurrent compiler questions;
- single-candidate-cliff rejection;
- general `Delta_0` necessity as unproved rather than silently solved;
- abandoned contraction/small-gain and stochastic-closure directions;
- early controlled-generative validation plan;
- separate search-coverage, observation-error, inhibition, conjunction, compatibility, and vacuity failure hypotheses;
- one-way simulation versus two-way response-faithfulness correction;
- local-grammar versus global-control-alphabet correction;
- four-symbol sufficiency versus unproved four-symbol minimality;
- early symbolic candidate-space / outer-envelope / exact-inclusion / all-look compiler progression;
- the exact single-polyhedron solver+inclusion admission theorem that preceded the finite-union compiler path.

## 5. Active, deferred, and historical are not synonyms

After actual recovery, the repository contains many **unproved/deferred** historical questions, but only two current active scientific programs are intentionally live:

1. scalable feedback-memory / feedback-portability beyond the five-state benchmark;
2. a real application whose data identify the required transition/recruitment/movement layer rather than only associations.

Examples such as autonomous local delay-gate compilation, arbitrary multi-valued/concurrent relay compilation, generic contraction blankets, general stochastic closure calculus, richer biological codebooks, and four-symbol minimality are recovered as deferred/non-priority questions. Their existence does not mean current priorities should reopen them automatically.

HIST-H1–H4 remain historical-literature gates, not CCOC mathematical gaps.

## 6. Consolidation status before novelty can resume

The canonical consolidation is now explicit in:

`docs/hypothesis_recovery_canonical_index_2026-08-14.md`.

That index declares the base PR #201 ledger plus all accepted `REC-*` appendices normative and separates active, deferred, abandoned, refuted/corrected, legacy/evidence, and historical categories.

The remaining procedural gate is therefore:

1. merge this recovery batch after the final CI head is green;
2. record the resulting immutable recovery SHA;
3. only then resume row-by-row novelty adjudication.

## 7. Completeness claim boundary

This manifest supports the statement:

> **Within the accessible `ccoc` repository history and connected GitHub records examined above, the scientific hypothesis inventory has undergone an issue/PR/branch/doc/module reverse-recovery pass with explicit provenance for recovered omissions.**

It does **not** prove that every scientific idea ever discussed outside the repository, in deleted local work, or in inaccessible external conversations has been recovered. Novelty adjudication must use this repository-bounded claim, not an absolute memory claim.