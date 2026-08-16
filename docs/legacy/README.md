# Legacy registry compatibility note

The current research surface is defined by `docs/current_architecture.md`. Historical and companion theorem groups are tracked by `legacy/manifest.md` and the machine-readable `docs/theorem_registry.json`.

This file remains only because the current theorem registry still cites a documentation path under `docs/` for the `LEGACY-1` experimental-design entry.

## Current status

- `CORE-1` through `CORE-5` form the publication core.
- `CORE-0`, `EXT-1`–`EXT-4`, `ID-1`–`ID-3`, and `LEGACY-1` are historical/companion registry entries, not equal current research priorities.
- `causal_model.current_theory` and `causal_model.identifiability_companion` have been retired from the current tree because they had no active code consumers.
- several stale theorem-specific legacy workflows have also been removed.
- complete pre-cleanup recovery is available at Git pin `4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`.

## Why legacy source still exists

The current registry verifier requires every registered `modules`, `tests`, and `documents` path to exist. Therefore the underlying ID/EXT/LEGACY source bundles cannot be physically retired cleanly until the registry is split into a **current executable registry** and an **immutable historical archive record**.

That registry-aware migration is a later cleanup pass. It should not be confused with scientific promotion of these branches.

## Rule

Do not add new theorem variants, facades, workflows, or examples to the legacy groups. Maintenance is allowed only when needed to preserve the current registry contract until that contract is simplified.
