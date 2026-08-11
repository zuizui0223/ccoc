# Freeze and reopening record: open-composition theorem repository

## Current status

**Development reopened on 2026-08-11.**

The July 2026 freeze is retained as a stable reproducibility checkpoint for the
first theorem-first manuscript **Causal Compression under Open Composition**. It
no longer prohibits new theorem development in this repository.

The historical frozen paper core was:

1. `CORE-1` — exact grammar-aware interfaces;
2. `CORE-2` — operational addressability and extension--compression
   noncommutation;
3. `CORE-3` — bounded-degree relay sharpness;
4. `CORE-4` — conservative macro-schema portability; and
5. `CORE-5` — local future-word / new-action fiber-split obstruction.

These identifiers and their deterministic replay remain provenance anchors for
v1. New work may strengthen, weaken assumptions of, replace, or supersede a
canonical claim, but it must say explicitly how it relates to this baseline.

## Historical freeze point

On 2026-07-02 the repository was frozen to stabilize the first open-composition
manuscript and its reproducibility surface. During that period, changes were
restricted to claim-narrowing corrections, deterministic replay repairs,
security/dependency maintenance, and archival metadata.

That policy is now historical. The freeze commit remains useful because it gives
a fixed reference against which post-freeze theorem changes can be compared.

## Reopened development rule

New mathematics is permitted again, subject to the following discipline:

- do not develop directly on `main`; use a branch and pull request;
- identify the exact canonical assumption or conclusion being changed;
- keep proof statements separate from finite computational replay;
- provide counterexamples or fail-closed tests for weakened assumptions where
  feasible;
- preserve a reproducible route to the July 2026 v1 theorem package; and
- do not infer empirical ecological validity from the abstract finite model.

The immediate reopened priority is the `CORE-2`/`CORE-3` novelty spine:

> determine whether the full product-indexed subset and joint-realisability
> assumptions can be weakened while retaining a quantitative
> extension--compression lower bound, and determine whether bounded-degree,
> pairwise, constant-local-grammar constructions remain sharp under the weaker
> hypothesis.

A new special case is not sufficient reason to add a theorem. Priority goes to
strict assumption weakening, stronger lower bounds, sharper necessity/sufficiency
boundaries, or genuinely stronger sharpness constructions.

## Scope separation retained after reopening

- Non-nested replacement, extinction, recolonization, and rewiring transport is
  developed in `zuizui0223/mltr` unless a result directly strengthens the
  open-composition theorem.
- Delayed exposure, finite-evidence limits, candidate mechanism uncertainty, and
  panel-design results remain companion directions rather than automatic parts
  of the CCOC theorem spine.
- Stochastic, approximate, continuous-state, simultaneous-action, and empirical
  extensions may now be proposed, but should not be mixed into the core without
  a separate scope decision.

## Reproducibility checkpoint

The historical v1 replay remains:

```bash
python -m pip install -e '.[dev]'
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
```

A successful replay validates the declared finite witnesses and provenance paths
of the v1 package; it is not an automated proof of the all-system theorems and
does not validate an observed ecosystem.

## Stable historical reference

The July 2026 freeze commit remains the stable historical reference for the first
paper core. Post-reopening releases should use new immutable tags rather than
moving or rewriting that checkpoint.

## Development locations

| Research direction | Repository |
|---|---|
| Open-composition theorem strengthening and sharpness | `zuizui0223/ccoc` |
| Open-composition manuscript prose, bibliography, figures, and submission files | `rach-open-composition-paper` |
| Exact macro-law transport through replacement and rewiring | `zuizui0223/mltr` |
| Other extensions | `zuizui0223/ccoc` only after an explicit theorem-scope decision, otherwise a dedicated repository |
