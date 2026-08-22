# CCOC — causal compression under open composition

CCOC is a theorem-first mathematical-ecology repository for one finite question:

> When can exact compression valid under fixed closed future grammars fail to provide one comparably small exact interface after the legal future grammar is opened?

The current formal scope is finite and mostly deterministic. Passing certificates establish properties of declared finite models; they do not validate an observed ecosystem.

## Core result

The first-paper spine is deliberately narrow:

1. `CORE-1` — exact grammar-aware response interface as foundational substrate;
2. `CORE-2` — **cross-grammar extension/compression lower bound**, the headline theorem candidate;
3. `CORE-3` — bounded-local extremal realization showing sharpness under simple local structure.

`CORE-4` and `CORE-5` remain executable supporting boundaries only.

The strongest explicit family has

\[
|P_C|=2,\qquad |P_O|=2^{m+1},\qquad K_O-K_C=m.
\]

Two retained strengthenings support rather than expand the first-paper spine:

- **constrained codebooks:** large inflation does not require the full Cartesian product of exterior states;
- **approximate addressability:** bounded decoding error does not immediately erase the memory lower bound.

## Submission mode

The first paper is in **submission-conversion mode**, not theorem-expansion mode. Manuscript preparation stays inside this repository under [`manuscript/`](manuscript/); no separate manuscript repository is required.

Current operational documents:

- [`docs/submission_conversion_decision_2026-08-19.md`](docs/submission_conversion_decision_2026-08-19.md) — journal/claim strategy;
- [`docs/cleanup_consolidation_2026-08-19.md`](docs/cleanup_consolidation_2026-08-19.md) — single-repository retention rule;
- [`docs/manuscript_transfer_manifest_2026-08-14.md`](docs/manuscript_transfer_manifest_2026-08-14.md) — in-repository manuscript integration contract.

The bounded-local relay is used as a constrained extremal/sharpness realization **without historical-firstness language**. The H1–H4 classical compiler audit remains useful Related Work provenance but is non-blocking for manuscript drafting.

## Hypothesis recovery status

The repository-bounded reverse-recovery pass covers the complete issue set, PR history, closed-unmerged PRs, branch audit, scientific docs, theorem/status maps, and module inventory. The canonical recovery record preserves proved, refuted, corrected, deferred, abandoned, experimental, and historical hypotheses rather than only successful theorems.

The post-cleanup status is summarized in [`docs/hypothesis_recovery_post_cleanup_status_2026-08-20.md`](docs/hypothesis_recovery_post_cleanup_status_2026-08-20.md). In particular, deterministic feedback is no longer an active CCOC first-paper program; it remains recovered provenance and is routed to MLTR if revived. The current first-paper theorem selection is complete.

## CREST role: future insufficiency of a present-state merge

The dedicated synthesis lives at [zuizui0223/crest](https://github.com/zuizui0223/crest). The current program architecture is documented in [the trajectory-first CREST map](https://github.com/zuizui0223/crest/blob/main/docs/trajectory_first_program_architecture_2026-08-22.md).

CREST now starts from temporally extended ecological worlds and asks when a present snapshot can be compressed into an adequate scientific state. Within that hierarchy, CCOC is a **structural obstruction theory for future sufficiency**.

Let two ecological worlds share the same present snapshot or current macro-description. CCOC asks whether opening the declared future grammar can expose a response distinction that the present merge erased. Its program-level reading is therefore

\[
\boxed{
\text{same present description}
\not\Rightarrow
\text{same required state under an enlarged future grammar}.
}
\]

This is one reason a present snapshot can fail to be a sufficient CREST state. CCOC does not by itself decide whether an inherited category remains semantically coherent after replacement, whether retained mechanisms agree, or whether field evidence identifies the required distinction.

CCOC remains a separate theorem and provenance unit. CREST does not merge the companion theorem programs into one theorem.

Companion ownership remains:

- fixed inherited-law repair / transport defect / history → **MLTR**;
- retained mechanism disagreement → **MRM**;
- finite/noisy evidence, monitoring design, proof-carrying evidence admission → **CED**.

## Current code surface

Preferred entrance:

```python
import causal_model.portability_core as rach
```

The facade contains only the manuscript theorem spine plus codebook and bounded-local strengthenings. `approximate_addressability.py` remains an explicit stronger-model extension rather than part of the paper-core facade.

Historical converse/reuse, generic canonical-quotient, resource-accounting, observation-window, stochastic/ecological special-case, and other supporting branches remain recoverable from Git history but are no longer active CCOC APIs.

## Repository cleanup status

Files are classified as:

- **CURRENT** — publication core, manuscript surface, or genuinely distinct strengthening;
- **COMPATIBILITY** — a demonstrated temporary live dependency only;
- **HISTORICAL** — valid conclusion/provenance recoverable from Git history or compact archive records;
- **REMOVE** — duplicate, misrouted, or superseded current-tree surface.

A valid theorem or ecological example is not automatically a reason to keep a dedicated executable bundle.

## Reproducibility

```bash
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
pytest -q
```

Finite certificates and replay verify current implementations; quantified theorem proofs are indexed separately.

## Start here

- `manuscript/README.md` — first-paper manuscript workspace and section order
- `docs/submission_conversion_decision_2026-08-19.md` — current submission plan
- `docs/hypothesis_recovery_post_cleanup_status_2026-08-20.md` — recovered-hypothesis inventory synchronized with the current post-cleanup program
- `docs/cleanup_consolidation_2026-08-19.md` — current cleanup/retention rule
- `docs/theorem_spine.md` — CORE-1–5 proof dependency graph and analytic proof locations
- `docs/claim_status_audit.md` — proof status, executable surfaces, and non-claims
- `docs/current_architecture.md` — current code/theorem map
- `docs/core_surface_cleanup_manifest_2026-08-14.md` — executed cleanup decisions
- `docs/residual_novelty_decision_2026-08-13.md` — novelty boundary
- `docs/ccoc_mltr_claim_firewall_2026-08-16.md` — CCOC/MLTR boundary
- `docs/theorem_registry.md` — executable theorem registry
- `docs/nonempirical_scope.md` — nonempirical scope policy
- `docs/historical_theorem_archive.md` — historical theorem archive
- `FREEZE.md` — historical freeze/reopen policy

## Development rule

Do not add a theorem family unless it changes a material premise, survives prior-art classification, and passes CREST routing. New ecological relabelings, exact converse variants, or resource corollaries do not qualify by themselves.
