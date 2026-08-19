# Manuscript provenance

## Current development snapshot

- repository: `zuizui0223/ccoc`
- manuscript location: `manuscript/`
- submission-cleanup baseline before this provenance refresh: `421e6999f20083a4749815301b633a6f77c8ad87`
- theorem-code merge anchor: `b4cdb994a0fb0eb7d1d5be410a267ea983287281`
- validated theorem-code PR head: `1dae2af844251c994ab528b6b9e8d092c79169da`

The compare from the theorem-code merge anchor to the submission-cleanup baseline contains no changes under `causal_model/`, `tests/`, `scripts/`, or active workflow code.

## Validation

On the validated theorem-code PR head:

- theorem registry integrity: success (`32013744855`);
- grammar interface replay: success (`32013744852`);
- paper-core reproducibility: success (`32013744906`);
- full tests: success (`32013744974`) on Python 3.10, 3.11, and 3.12.

Paper-core artifact: `9282749044`, digest `sha256:e93e8ebcf924e5680fc02952c2fa300d8fab0a36dedb1f7f2f37d07902a0c140`.

## Claim control

The manuscript does not claim historical firstness for contextual minimization, generic quotient refinement, generic reduction/composition noncommutation, pair-separation/cardinality bounds, or bounded-local compilation in isolation.

The bounded-local relay is used as an explicit constrained extremal/sharpness realization.

## Submission snapshot rule

This file is a development record, not the final submission pin. Immediately before submission, replace the development snapshot with the exact final CCOC SHA and record a successful run of:

```bash
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
pytest -q
```
