# Paper-core reproducibility pin

> **Status:** publication provenance record, refreshed 2026-08-19. This file records the latest successful replay known to cover the theorem-code surface currently carried by CCOC. Later changes through the current submission-cleanup main are documentation/manuscript only.

## Canonical theorem-code merge anchor

- current theorem-code merge commit: `b4cdb994a0fb0eb7d1d5be410a267ea983287281`
- source PR: #218, *Reduce non-core structural side branches*
- validated PR head: `1dae2af844251c994ab528b6b9e8d092c79169da`

A repository compare from the squash-merge commit `b4cdb994...` to submission-cleanup main `421e6999f20083a4749815301b633a6f77c8ad87` shows only README, documentation, claim-control, and `manuscript/` changes. No `causal_model/`, `tests/`, `scripts/`, or active workflow code changed after that theorem-code merge.

## Successful validation on the PR head

All relevant runs completed successfully on `1dae2af844251c994ab528b6b9e8d092c79169da`:

- **Theorem registry integrity** — run `32013744855`, run number 400 — success;
- **Grammar interface certificate replay** — run `32013744852`, run number 34 — success;
- **Paper-core reproducibility** — run `32013744906`, run number 130 — success;
- **tests** — run `32013744974`, run number 1125 — success.

The full test matrix passed on Python **3.10, 3.11, and 3.12**.

### Paper-core artifact

- artifact name: `paper-core-reproducibility`
- artifact id: `9282749044`
- digest: `sha256:e93e8ebcf924e5680fc02952c2fa300d8fab0a36dedb1f7f2f37d07902a0c140`
- created: `2026-08-17T09:10:33Z`
- reported expiry: `2026-11-15T09:08:53Z`

## Submission provenance model

CCOC manuscript work lives inside the same repository under `manuscript/`. Submission provenance therefore has two layers:

1. **submission snapshot SHA** — the exact CCOC commit containing the manuscript, claim controls, and repository surface submitted to the journal;
2. **theorem replay anchor** — the successful theorem-code validation above, or a later successful replay if any theorem/test/script/registry/workflow path changes.

Documentation/manuscript-only commits do not invalidate the theorem-code replay. Any change to the paper-core theorem/test/script/registry/workflow surface does.

## Final submission rule

Immediately before submission, run on the intended submission snapshot:

```bash
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
pytest -q
```

Record the exact successful SHA and preserve the generated replay reports with durable submission/release materials. Never cite `main` or `latest` as proof provenance.

Because GitHub Actions artifacts expire, preserve final machine-readable reports in a durable release or supplement.

## Claim boundary

A successful replay establishes consistency of declared finite certificates, regressions, registry provenance, and synthetic witness instances. It does not:

- prove the general analytic theorems;
- infer the ecological future grammar from observations;
- validate a real ecosystem;
- establish historical priority;
- turn the bounded-local relay into a firstness claim.
