# Paper-core reproducibility pin

> **Status:** publication provenance record. This file records the latest successful paper-core replay that covers the theorem-code surface. Documentation/manuscript-only commits after that replay do not invalidate the theorem-code anchor, but a final submission snapshot must record both the manuscript SHA and the theorem replay SHA.

## Canonical theorem replay anchor

- theorem-code commit: `305106d739de7cd188a5d67d0810155948704ae0`
- workflow: `Paper-core reproducibility`
- workflow run: `31475391886` (`run_number=32`)
- event: `push` on `main`
- conclusion: `success`
- artifact name: `paper-core-reproducibility`
- artifact id: `9095585378`
- artifact digest: `sha256:531d927238b225323c55f613b04c8ec953ef0358900989de74d485a60ce3a25c`
- artifact expiry reported by GitHub: `2026-11-09T08:55:42Z`

The workflow validates theorem-registry provenance, the allowlisted CORE regression suite, and `scripts/verify_paper_core.py`, then writes the machine-readable replay reports.

## Current use

CCOC manuscript work now lives inside the same repository under `manuscript/`. Therefore submission provenance has two layers:

1. **submission snapshot SHA** — exact CCOC commit containing the manuscript, claim controls, and current repository surface;
2. **theorem replay anchor** — most recent successful paper-core run covering the theorem-code state used by that snapshot.

If no paper-core theorem/test/script/registry file changed after the replay anchor, the historical successful replay remains valid for the theorem code while later documentation/manuscript commits are separately pinned by the submission snapshot SHA.

If any paper-core theorem/test/script/registry path changes, this replay pin becomes stale and a new successful run is required before submission.

## Final submission rule

Before submission:

```bash
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
pytest -q
```

Record the exact successful commit and preserve the generated replay reports with the submission/release materials. Never cite `main` or `latest` as proof provenance.

Because GitHub Actions artifacts expire, the final manuscript/release workflow should preserve the machine-readable reports in a durable release or supplement.

## Claim boundary

A successful replay demonstrates consistency of declared finite certificates, regressions, registry provenance, and synthetic witness instances. It does not:

- prove the general analytic theorems;
- identify the ecological future grammar from observations;
- validate a real ecosystem;
- establish historical priority;
- turn a bounded-local sharpness witness into a firstness claim.
