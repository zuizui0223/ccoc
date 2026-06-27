# Robust-admissibility roadmap

The active next layer is implemented in this repository; no additional repository is needed.

## Target

Given a declared qualitative program grammar, a finite or sampled parameter domain, a deterministic acceptance rule, and robustness cells that vary allowed analysis choices, classify each candidate motif as:

- **invariant**: active in every accepted run of every nonempty robustness cell;
- **excluded**: inactive in every accepted run of every nonempty robustness cell;
- **unresolved**: neither condition holds;
- **unsupported**: at least one required robustness cell has no accepted run, so the requested universal claim is not evaluated.

All labels are conditional on the declared grammar, parameter domain, observation encoding, acceptance rule, and robustness-cell specification.

## Migration slices

1. generic admissibility data model and exact cross-cell motif classifier;
2. known-truth benchmark and error metrics;
3. budgeted joint observation-panel optimizer;
4. two controlled, mechanically distinct backend adapters;
5. calibration report for tolerance, prior, finite-run, and endpoint sensitivity.

## Deliberately excluded

The repository does not import generic demos, UI, Campanula-specific code, or unscoped ABM families from `microdonta`.
