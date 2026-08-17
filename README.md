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

The current strengthening surface adds two things that materially change this core claim:

- **constrained codebooks:** the lower bound does not require the full Cartesian product of exterior states; large inflation can survive strong compositional constraints;
- **approximate addressability:** fixed decoding error does not immediately erase the memory lower bound.

## CREST role and claim firewall

At program level, CCOC is the **future-sufficiency audit** of Contract-Relative Ecological State Theory (CREST): it asks which distinctions a declared future grammar can make operationally necessary.

The canonical four-audit synthesis is maintained in MRM at [Contract-Relative Ecological State Theory (CREST)](https://github.com/zuizui0223/mrm/blob/main/docs/contract_relative_ecological_state_theory.md). CCOC remains a separate theorem and provenance unit; CREST does not merge the four quotient/refinement problems into one theorem.

CCOC owns independently optimized closed-vs-open interface complexity. Companion ownership remains:

- fixed inherited-law repair / transport defect / history → **MLTR**;
- retained mechanism disagreement → **MRM**;
- finite/noisy evidence, monitoring design, proof-carrying evidence admission → **CED**.

Passing the CCOC audit does not imply semantic coherence after replacement, robustness to retained mechanism uncertainty, or evidential licensing. CREST is the routing rule; shared vocabulary is not enough to keep a theorem family here.

## Current code surface

Preferred entrance:

```python
import causal_model.portability_core as rach
```

The facade contains only the manuscript theorem spine plus codebook and bounded-local strengthenings. `approximate_addressability.py` remains an explicit stronger-model extension rather than part of the paper-core facade.

Historical converse/reuse, generic canonical-quotient, resource-accounting, observation-window, stochastic/ecological special-case, and other supporting branches remain recoverable from Git history but are no longer active CCOC APIs.

## Repository cleanup status

Files are classified as:

- **CURRENT** — publication core or a genuinely distinct strengthening;
- **COMPATIBILITY** — required by a demonstrated live current-tree consumer;
- **HISTORICAL** — valid conclusion/provenance retained in Git history or canonical records;
- **REMOVE** — duplicate, misrouted, or superseded current-tree surface.

A valid theorem or ecological example is not automatically a reason to keep a dedicated executable bundle.

## Reproducibility

```bash
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
pytest -q
```

## Start here

- [CREST program synthesis](https://github.com/zuizui0223/mrm/blob/main/docs/contract_relative_ecological_state_theory.md) — canonical four-audit program map and cross-repository firewalls
- `docs/current_architecture.md` — current code/theorem map
- `docs/core_surface_cleanup_manifest_2026-08-14.md` — executed cleanup decisions
- `docs/residual_novelty_decision_2026-08-12.md` — novelty gate
- `docs/ccoc_mltr_claim_firewall_2026-08-16.md` — CCOC/MLTR boundary
- `docs/theorem_registry.md` — executable theorem registry / current theorem atlas
- `docs/nonempirical_scope.md` — nonempirical scope policy
- `docs/historical_theorem_archive.md` — historical theorem archive
- `docs/manuscript_transfer_manifest_2026-08-14.md` — manuscript handoff
- `FREEZE.md` — historical freeze/reopen policy

## Development rule

Do not add a theorem family unless it changes a material premise, survives prior-art classification, and passes CREST routing. New ecological relabelings, exact converse variants, or resource corollaries do not qualify by themselves.
