# CCOC cleanup and manuscript consolidation — 2026-08-19

## Decision

CCOC remains the single repository for theorem code, provenance, manuscript-facing documentation, and submission preparation. The previously proposed separate `rach-open-composition-paper` repository is abandoned.

The current tree should contain only:

1. the publication theorem core;
2. the constrained-codebook strengthening;
3. approximate addressability as a clearly secondary stronger-model extension;
4. manuscript/submission controls and reproducibility assets;
5. compact historical provenance records needed to explain removed branches.

Git history, not duplicate live workspaces, is the archive.

## Immediate cleanup

- delete the obsolete separate-repository bootstrap manifest;
- remove separate-repository creation as a manuscript blocker;
- keep H1–H4 compiler-history work as non-blocking Related Work provenance only;
- retain the tiny `delayed_addressability.py` forwarding shim only until all live imports are migrated to `shared_grammar.py`; it has no theorem status;
- do not add theorem families merely to justify retained files.

## Manuscript organization inside CCOC

Submission-facing work stays in this repository. The canonical path is:

```text
README.md
  -> docs/submission_conversion_decision_2026-08-19.md
  -> docs/manuscript_readiness_audit.md
  -> manuscript/
  -> theorem/proof documents and executable replay
```

The manuscript directory is publication prose only; theorem code stays under `causal_model/` and is referenced through immutable Git provenance.

## Retention rule

A current-tree artifact remains only if it is required by at least one of:

- the first-paper theorem/proof spine;
- a distinct strengthening explicitly used in the manuscript or supplement;
- reproducibility/CI of those claims;
- source/claim provenance that cannot be represented more compactly.

Everything else is historical and should be removed from the active tree once no live dependency remains.
