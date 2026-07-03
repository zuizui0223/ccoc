# Freeze record: open-composition theorem archive

## Status

RACH is frozen as the reproducibility and provenance archive for the theorem-first
manuscript **Causal Compression under Open Composition**.

The repository's active claim is restricted to finite deterministic controlled
systems with declared finite action grammars. The frozen paper core is:

1. `CORE-1` — exact grammar-aware interfaces;
2. `CORE-2` — operational addressability and extension--compression
   noncommutation;
3. `CORE-3` — bounded-degree relay sharpness;
4. `CORE-4` — conservative macro-schema portability; and
5. `CORE-5` — local future-word / new-action fiber-split obstruction.

## Freeze rule

After this freeze point, do **not** add new theorem families, examples,
application domains, empirical data, or manuscript-driven changes to RACH.
Permitted maintenance is limited to:

- corrections that narrow an existing claim;
- repairs that restore a documented deterministic replay or CI check;
- security and dependency maintenance that leaves theorem behavior unchanged;
- permanent archival metadata, release records, and citation information.

A correction that changes an assumption or conclusion requires a new audit and a
new versioned freeze point.

## What is deliberately outside this archive

- Non-nested replacement, extinction, recolonization, and rewiring transport is
  now developed in `zuizui0223/mltr` (**MLTR**, formerly `EXT`). RACH retains the
  original `EXT-1`--`EXT-4` assets only as historical provenance.
- Delayed exposure, finite-evidence limits, candidate mechanism uncertainty, and
  panel-design results remain legacy companions and are not paper claims.
- Stochastic, approximate, continuous-state, simultaneous-action, and empirical
  extensions are future work, not implicit corollaries.

## Reproducibility command

```bash
python -m pip install -e '.[dev]'
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
```

The dedicated **Paper-core reproducibility** GitHub Actions workflow runs the
same finite theorem suite and uploads the paper-core JSON report. A successful
replay validates the declared finite witnesses and provenance paths; it is not an
automated proof of the all-system theorems and does not validate an observed
ecosystem.

## Stable citation target

The intended stable reference is the Git commit containing this file, followed by
a GitHub release tag and release record pointing to that commit. The release tag
must not be moved after creation.

## Next development locations

| Research direction | Repository |
|---|---|
| Open-composition manuscript prose, bibliography, figures, and submission files | `rach-open-composition-paper` |
| Exact macro-law transport through replacement and rewiring | `zuizui0223/mltr` (formerly `EXT`) |
| Other legacy extensions | new dedicated repository only after a separate theorem-scope decision |
