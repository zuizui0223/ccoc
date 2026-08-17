# CCOC — causal compression under open composition

CCOC is a theorem-first mathematical-ecology repository for one finite question:

> When can exact compression valid under fixed closed future grammars fail to provide one comparably small exact interface after the legal future grammar is opened?

The current formal scope is finite and mostly deterministic. Passing certificates establish properties of declared finite models; they do not validate an observed ecosystem.

## Core result

The first-paper spine is deliberately narrow:

1. `CORE-1` — exact grammar-aware response interface as foundational substrate;
2. `CORE-2` — **cross-grammar extension/compression lower bound**, the headline theorem candidate;
3. `CORE-3` — bounded-local extremal realization showing sharpness under simple local structure.

`CORE-4` and `CORE-5` remain executable supporting boundaries only. They are not independent novelty claims and must not grow into source-relative repair theory.

The strongest explicit family has, for every `m>=1`,

\[
|P_C|=2,\qquad |P_O|=2^{m+1},\qquad K_O-K_C=m,
\]

with one fixed four-symbol primitive alphabet, one newly legal primitive action, pairwise radius-one dynamics, maximum degree three, cut one, and logarithmic selected-coordinate access.

The safe headline is therefore a **same-system cross-grammar quantitative separation**, not the invention of finite-state minimization.

## Claim firewall

CCOC optimizes separately under each closed grammar and compares those minima with the minimum exact interface under a jointly open grammar:

\[
K_i^*=\min_{q\text{ exact under }\Gamma_i}\log_2|q|,
\qquad
K_O^*=\min_{q\text{ exact under }\Gamma_O}\log_2|q|.
\]

Its target separation is

\[
\max_i K_i^*=O(1),\qquad K_O^*=\Omega(m).
\]

No inherited source partition is fixed, and the closed optima may differ.

CREST routing keeps companion questions out of this repository's active theorem surface:

- fixed inherited-law repair, transport defect, route coherence, history completion → **MLTR**;
- retained mechanism disagreement and candidate-safe prediction → **MRM**;
- finite/noisy evidence, candidate-set certification, observation panels, detection failure, and monitoring risk → **CED**.

See `docs/ccoc_mltr_claim_firewall_2026-08-16.md` and the program-level CREST document in `zuizui0223/mrm`.

## Current code surface

Preferred structural entrance:

```python
import causal_model.portability_core as rach
```

`causal_model/__init__.py` is intentionally not a compatibility facade. Historical evidence/panel/candidate APIs are not re-exported from the package root.

Canonical first-paper modules and distinct surviving extensions are listed in `docs/current_architecture.md`.

### Historical / routed families

Deterministic feedback was routed under CREST on 2026-08-17; its executable surface was retired while conclusions remain in Git history and the consolidated feedback records.

The former qualitative-candidate / observation-panel / benchmark surface was also routed on 2026-08-17. Its central objects are evidence certification, retained candidate sets, observation design, failure modes, and benchmarked panel choice, so they belong to CED/MRM rather than the CCOC open-future theorem. The dedicated source/test/doc/example/experiment bundle is historical rather than current code.

## Repository cleanup status

Files are classified as:

- **CURRENT** — publication core or a genuinely distinct active extension;
- **COMPATIBILITY** — required by a live current-tree consumer;
- **HISTORICAL** — conclusion/provenance retained in records and Git history;
- **REMOVE** — duplicated, misrouted, or superseded current-tree surface.

A valid theorem, witness, or example is not automatically a reason to keep a dedicated executable bundle.

## Reproducibility

```bash
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
pytest -q
```

`tests.yml` is the generic Python 3.10/3.11/3.12 gate. Specialized workflows survive only when they provide a distinct current replay or provenance contract.

## Start here

- `docs/current_architecture.md` — current code/theorem map
- `docs/core_surface_cleanup_manifest_2026-08-14.md` — executed cleanup decisions
- `docs/residual_novelty_decision_2026-08-12.md` — novelty gate
- `docs/ccoc_mltr_claim_firewall_2026-08-16.md` — CCOC/MLTR boundary
- `docs/theorem_registry.md` — executable theorem registry
- `docs/historical_theorem_archive.md` — historical theorem archive
- `docs/manuscript_transfer_manifest_2026-08-14.md` — eventual manuscript handoff
- `FREEZE.md` — historical freeze/reopen policy

## Development rule

Do not add a theorem family while cleanup is active unless it changes a material model premise, survives prior-art classification, and passes CREST routing. The current task is to make the surviving CCOC result easier to see, not to increase theorem count.
