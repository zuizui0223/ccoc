# Paper-core reproducibility pin

> **Status:** publication provenance record, 2026-08-12. This file records the
> latest successful `Paper-core reproducibility` run that includes the current
> theorem-code surface. It is not a release tag and it is not a substitute for the
> manuscript proofs.

## Canonical replay anchor

- theorem-code commit: `305106d739de7cd188a5d67d0810155948704ae0`
- commit title: `Generalize relay latency with a bounded-local causal-cone bound`
- workflow: `Paper-core reproducibility`
- workflow run: `31475391886` (`run_number=32`)
- event: `push` on `main`
- conclusion: `success`
- artifact name: `paper-core-reproducibility`
- artifact id: `9095585378`
- artifact digest: `sha256:531d927238b225323c55f613b04c8ec953ef0358900989de74d485a60ce3a25c`
- artifact expiry reported by GitHub: `2026-11-09T08:55:42Z`

The workflow executes theorem-registry provenance validation, the allowlisted
`CORE-1`–`CORE-5` regression suite, and `scripts/verify_paper_core.py`, then uploads
`artifacts/paper_core_reproducibility_report.json` and
`artifacts/theorem_registry_report.json`.

## Why this remains the theorem replay anchor after later documentation commits

At the time this record was created, current `main` was

`892192ab730e0ef2f6995d3905d90a6aeb477e00`.

A repository compare from the successful replay SHA `305106d7...` to that main
head showed four later commits affecting only:

- `README.md`;
- `docs/manuscript_traceability.md`;
- `docs/quantitative_prior_art_matrix.md`;
- `docs/universal_compilation_reduction_risk.md`;
- `docs/universal_compilation_source_audit.md`;
- `docs/universal_compiler_acquisition_log_2026-08-12.md`.

No `causal_model/`, `tests/`, `scripts/`, theorem-registry, or paper-core workflow
file changed in that interval. Therefore run `31475391886` is the most recent
successful replay of the theorem-code state currently carried by the archive;
subsequent changes are claim-control/provenance documentation.

This statement is deliberately narrower than saying that every later commit was
executed by the workflow.

## Submission transfer rule

When `rach-open-composition-paper` is created, record both:

1. the final CCOC/RACH commit or release used by the manuscript; and
2. this successful theorem replay anchor, or a later successful replay if theorem
   code changes before submission.

If any file under the paper-core workflow's theorem/test/script path filter changes
later, this pin becomes stale and a newer successful run must replace it.

Because GitHub Actions artifacts expire, the manuscript/release workflow should
preserve the machine-readable replay reports in a permanent release or supplement
before the reported artifact expiry date. The artifact's current availability is
not itself a permanence guarantee.

## Claim boundary

A successful replay demonstrates consistency of the declared finite certificates,
regressions, registry provenance, and synthetic witness instances. It does not:

- prove the manuscript's general analytic theorems;
- identify an ecological grammar from observations;
- validate a real ecosystem;
- resolve historical priority or the universal-compilation novelty risk in issue
  #122.
