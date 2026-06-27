# RACH Causal Invariants

A theorem-first framework for reasoning about **which causal motifs are indispensable within a declared qualitative model class**, and about why the observations needed to establish that fact may be synergistic.

## Core question

Given a causal-program grammar, a set of biological constraints, and an observation set, distinguish:

```text
possible explanation
≠
robustly admissible explanation
```

The immediate theorem core works under a finite disjunctive structural model:

```text
cline(t)  <=>  at least one driver of trait t is active.
```

It proves, within that declared candidate set:

1. **Null-only elimination.** Positive observations cannot force a mechanism off; NULL observations eliminate the mechanisms that generate the null trait.
2. **Last-driver criterion.** A mechanism is indispensable exactly when it is the only surviving driver of at least one required-present trait.
3. **Synergistic observation design.** A set of individually uninformative competitor-witness observations can jointly make a mechanism indispensable. Therefore greedy one-step observation selection has no general guarantee.
4. **Minimum discriminating panels.** Given feasible NULL observations and their costs, an exact dynamic program finds the cheapest panel that makes a focal mechanism indispensable while preserving all required-present observations.
5. **Coverage-aware robustness reports.** Robust-admissibility results distinguish unanimity in sampled runs from complete claims backed by exhaustive enumeration or an external solver certificate.
6. **Known-truth calibration.** Small fully enumerated program universes can quantify false-invariant and false-excluded rates caused by finite sampling.
7. **Failure-mode audits.** Truth-table benchmarks show how omitted drivers, noisy NULLs, inhibition, conjunctions, and hidden compatibility constraints can produce false necessity, missed necessity, or an outright model contradiction.
8. **Exact misspecification phase benchmarks.** A finite generative family sweeps latent routes, witness sensitivity, inhibition, conjunctions, and compatibility constraints to calculate posterior false-necessity risk without Monte Carlo error. See [the benchmark guide](docs/generative_misspecification_benchmarks.md).
9. **Multi-competitor panel benchmarks.** Exact joint-panel design is compared against strict one-step greedy selection under multiple competitors, latent routes, and correlated environmental contexts. See [the panel benchmark guide](docs/multi_competitor_panel_phase_benchmarks.md).

## Exactness boundary

The Boolean theorems are exact only when the declared model permits every switch assignment compatible with the observation clauses. They do not cover hidden mutual exclusions, resource budgets, inhibitory effects, conjunctions, thresholds, feedbacks, or latent mechanisms folded into coarse labels. See [the theorem assumptions](docs/replaceability_theorems.md#exactness-assumptions) and [scope-failure audits](docs/failure_mode_audits.md).

## Scope boundary

This repository is the active methods home for RACH causal invariants. It does **not** claim that an inferred motif is universally true in nature. Every conclusion is conditional on the declared candidate mechanisms, observation fidelity, program grammar, and—for sampled program families—search coverage.

The initial theorem core is a clean extraction from the earlier `microdonta` work. Generic demos, field-case code, UI prototypes, and historical ABMs are intentionally not copied here.

## Development roadmap

```text
exact disjunctive theorem core + exhaustive small-model checks
-> exact minimum discriminating observation / intervention panels
-> coverage-aware robust-admissibility reports
-> known-truth finite benchmarks and sampling-error calibration
-> audited omitted-driver / noisy-NULL / non-OR failure modes
-> exact generative phase benchmarks for misspecification and noise
-> multi-driver correlated-context comparisons: exact panel versus strict greedy
-> cost-aware and risk-robust panel optimization across misspecification grids
-> broader qualitative program families
```
