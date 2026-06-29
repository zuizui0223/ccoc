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
10. **Risk-robust panel design.** Cost-first, coverage-greedy, minimax-risk, and weighted-mean-risk panel selection can be compared over explicit finite true-model scenarios, including shared witnesses and measurement channels. See [the robust-panel guide](docs/robust_panel_design.md).
11. **Reproducible benchmark suite.** A dependency-free runner regenerates the paper-facing finite-enumeration CSV tables for phase risks, joint-panel synergy, and budgeted robust design. See [the experiment guide](experiments/README.md).
12. **Finite ecological-program layer.** A separate Boolean program API represents conjunction, alternative pathways, inhibition snapshots, and explicit feasible-state constraints without silently extending the OR theorem. See [the ecological-program guide](docs/ecological_program_inference.md).
13. **Noisy repeated observations and empirical protocol.** Repeated detections have declared sensitivity and false-positive rates; an island flower-colour data contract provides a pre-analysis route for field, common-garden, pollinator, and genomic evidence. See [the empirical template](examples/island_flower_colour/README.md).
14. **Exact observation-channel envelopes.** A known finite generator can be passed through all possible repeated-detection outcomes to quantify exact invariant, excluded, unresolved, unsupported, false-invariant, and false-excluded probabilities. See [the envelope guide](docs/exact_observation_envelopes.md).

## Reproduce benchmark tables

```bash
python experiments/run_all_benchmarks.py --output results
```

The generated tables are exact finite weighted enumerations under their declared benchmark families. They are not empirical estimates and contain no Monte Carlo uncertainty.

## Ecological-program inference

The original disjunctive theorem remains exact only for its declared monotone OR
assumptions. The ecological-program layer is a separate finite-state inference
workflow: candidate programs are evaluated against repeated noisy observations,
then passed to the existing robust-admissibility classifier across required
analysis cells. It supports exact joint observation-panel design over a finite
library, but its exhaustive search is deliberately limited to small, auditable
candidate sets.

The analyst must predeclare the candidate program universe, feasible-state
constraints, observation channels, acceptance thresholds, and search coverage.
A `sampled` candidate universe must not be reported as complete merely because
the state space within each sampled program was enumerated exactly.

## Exactness boundary

The Boolean theorems are exact only when the declared model permits every switch assignment compatible with the observation clauses. They do not cover hidden mutual exclusions, resource budgets, inhibitory effects, conjunctions, thresholds, feedbacks, or latent mechanisms folded into coarse labels. See [the theorem assumptions](docs/replaceability_theorems.md#exactness-assumptions) and [scope-failure audits](docs/failure_mode_audits.md).

The ecological-program module can represent a finite subset of those features,
but it does not turn a candidate grammar into a universal model of nature. Its
results remain conditional on the declared rules, feasible states, observation
error model, acceptance rule, and candidate-program coverage.

## Relationship to domain models

RACH is deliberately **not** a floral-trait, pollination, fitness, population-genetic,
or site-level model. It stores generic qualitative programs, binary observation
channels, acceptance rules, coverage labels, and exact self-calibration
benchmarks. It answers whether a motif would be classified as indispensable or
excluded within those declared abstractions.

[`campanula-channel-identification`](https://github.com/zuizui0223/campanula-channel-identification)
is a separate domain repository. It specifies a Campanula / island-floral-trait
life cycle, including local reproduction versus establishment, nectar-guide
routes, handling and pollen placement, selfing, recruitment, spatial structure,
and prospective field measurements. It can translate a small predeclared set of
its scenarios into a RACH candidate universe for an audit, but RACH does not
contain those biological equations and must not be presented as evidence for a
Campanula mechanism.

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
-> cost-aware minimax and weighted-risk robust panel optimization
-> reproducible paper-facing exact benchmark tables
-> finite ecological-program grammar + repeated-observation likelihoods
-> exact observation-channel risk envelopes over finite candidate universes
-> empirical scenario calibration with predeclared field/genetic/pollination data
-> scalable solver-backed robust design and broader qualitative program families
```
