# Freeze and submission-mode record: open-composition theorem repository

## Current status

The July 2026 freeze remains a stable reproducibility checkpoint for the first theorem-first manuscript **Causal Compression under Open Composition**.

Development was reopened on 2026-08-11 to test and strengthen the theorem spine. That strengthening phase is now complete for the first paper. As of 2026-08-19, CCOC is in **submission-conversion mode**.

## Historical frozen paper core

1. `CORE-1` — exact grammar-aware interfaces;
2. `CORE-2` — operational addressability and extension–compression separation;
3. `CORE-3` — bounded-local relay sharpness;
4. `CORE-4` — conservative macro-schema portability;
5. `CORE-5` — local future-word / new-action fiber-split obstruction.

These identifiers remain provenance anchors. Later strengthenings may refine assumptions or sharpness, but the first-paper theorem count is frozen unless a concrete claim failure forces replacement mathematics.

## Current development rule

- do not develop directly on `main`; use branch/PR review;
- manuscript, documentation, and cleanup changes are allowed when they improve submission readiness;
- new mathematics is admitted only if it repairs a failed premise or materially strengthens the first-paper claim;
- do not add a special case merely to increase theorem count;
- keep analytic proof statements separate from finite computational replay;
- preserve reproducible access to historical checkpoints;
- do not infer empirical ecological validity from the abstract finite model.

## Current first-paper priority

The main task is no longer theorem expansion. It is:

1. complete the self-contained manuscript under `manuscript/`;
2. maintain the conservative novelty boundary;
3. finish theorem/source/claim traceability;
4. build the agreed figure set;
5. pin an immutable submission SHA and rerun theorem registry, paper core, and full tests;
6. perform journal-specific and final human submission review.

## Scope separation

- open-composition future-sufficiency mathematics → `zuizui0223/ccoc`;
- non-nested replacement/rewiring transport → `zuizui0223/mltr`;
- mechanism uncertainty → `zuizui0223/mrm`;
- evidence/reportability → `zuizui0223/ced`;
- cross-contract synthesis → `zuizui0223/crest`.

Approximate addressability remains a secondary CCOC strengthening. Evidence, mechanism, inherited-law repair, field-protocol, and other historical branches do not return to the first-paper spine without an explicit scope decision.

## Reproducibility checkpoint

The historical replay route remains:

```bash
python -m pip install -e '.[dev]'
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
pytest -q
```

A successful replay validates declared finite witnesses, regressions, and provenance paths. It does not prove the analytic theorem family, validate a real ecosystem, or establish historical novelty.

## Repository locations

| Research surface | Location |
|---|---|
| theorem code and tests | `causal_model/`, `tests/`, `scripts/` in CCOC |
| manuscript prose and submission structure | `manuscript/` in CCOC |
| proof/source/claim controls | `docs/` in CCOC |
| historical archive | immutable Git history and compact archive records |

There is no separate manuscript repository.
