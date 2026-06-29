# RACH Causal Invariants

A theorem-first framework for conditional, set-valued causal reasoning: **which causal motifs are indispensable within a declared qualitative candidate class, and when can random data support that conclusion without false certainty?**

RACH is a methods repository. It contains no empirical data set and makes no domain-specific causal claim.

## Core question

Given a causal-program grammar, a declared candidate universe, and retained candidate sets produced by an observation or statistical procedure, distinguish:

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
9. **Multi-competitor panel benchmarks.** Exact joint-panel design is compared against strict one-step greedy selection under multiple competitors, latent routes, and correlated contexts. See [the panel benchmark guide](docs/multi_competitor_panel_phase_benchmarks.md).
10. **Risk-robust panel design.** Cost-first, coverage-greedy, minimax-risk, and weighted-mean-risk panel selection can be compared over explicit finite true-model scenarios, including shared witnesses and measurement channels. See [the robust-panel guide](docs/robust_panel_design.md).
11. **Reproducible benchmark suite.** A dependency-free runner regenerates paper-facing finite-enumeration CSV tables for phase risks, joint-panel synergy, and budgeted robust design. See [the experiment guide](experiments/README.md).
12. **Finite qualitative-program layer.** A separate Boolean program API represents conjunction, alternative pathways, inhibition snapshots, and explicit feasible-state constraints without silently extending the OR theorem. See [the ecological-program guide](docs/ecological_program_inference.md).
13. **Finite noisy-observation special case.** Repeated binary detections have declared sensitivity and false-positive rates, allowing exact finite-state likelihood and panel calculations under their stated assumptions.
14. **Exact observation-channel envelopes.** A known finite generator can be passed through all possible repeated-detection outcomes to quantify exact invariant, excluded, unresolved, unsupported, false-invariant, and false-excluded probabilities. See [the envelope guide](docs/exact_observation_envelopes.md).
15. **Confidence-set lifting theorem.** Any external procedure that returns simultaneously valid candidate confidence sets from arbitrary random data can be lifted into a finite-sample RACH family-wise false-decisive bound. See [the theorem](docs/confidence_set_lifting_theorem.md).
16. **Anytime confidence-set lifting theorem.** An externally valid time-uniform candidate confidence sequence controls false decisive conclusions across every certified look and every data-dependent stopping rule. See [the anytime theorem](docs/anytime_confidence_set_lifting.md).
17. **Symbolic candidate-set lifting.** A solver-backed feasible set over an arbitrary, including continuous or uncountable, candidate space can support RACH classification from SAT/UNSAT certificates; solver semantic risk is added explicitly to statistical miscoverage. See [the symbolic theorem](docs/symbolic_candidate_set_lifting.md).

## Reproduce benchmark tables

```bash
python experiments/run_all_benchmarks.py --output results
```

The generated tables are exact finite weighted enumerations under their declared benchmark families. They are not empirical estimates and contain no Monte Carlo uncertainty.

## Distribution-agnostic random-data layer

The central general theorem does not prescribe a data type, likelihood, sample size, or sampling scheme. Let an external method map arbitrary random data to a retained set of candidates in each required robustness cell. If it establishes the simultaneous coverage statement

```text
P(true candidate is retained in every required cell) >= 1 - alpha,
```

then RACH guarantees

```text
P(any false INVARIANT or false EXCLUDED conclusion across all motifs) <= alpha.
```

The implication is pointwise and therefore does not require RACH to assume i.i.d. observations, normality, discreteness, continuity, or a particular data dimension. The external method must establish its own coverage conditions; RACH only preserves and lifts that guarantee. Observationally indistinguishable candidates necessarily remain unresolved with high probability under any honest low-error procedure.

## Sequential / anytime layer

At each interim look, a fixed-time candidate confidence set is not enough to justify repeated peeking. For a certified look scope \(\mathcal T\), the external method must establish

```text
P(true candidate is retained in every required cell at every t in T) >= 1 - alpha.
```

Only then does RACH guarantee

```text
P(any false INVARIANT or false EXCLUDED conclusion
  at any certified look, across all motifs) <= alpha.
```

Therefore a data-dependent stopping rule is safe only when its selected look lies inside the all-look certificate scope. RACH does not turn separately valid fixed-time intervals into an anytime guarantee; it requires an external confidence sequence, a jointly valid finite-look construction, or another documented time-uniform coverage method.

## Symbolic continuous / infinite candidate-set layer

The general lifting argument also does not require a finite candidate universe. For an arbitrary retained set \(C_r\subseteq\Theta\), RACH asks an external solver whether the set is non-empty and whether it contains candidates with and without each motif.

```text
non-empty + motif-inactive UNSAT  -> INVARIANT
non-empty + motif-active UNSAT    -> EXCLUDED
both motif values SAT             -> UNRESOLVED
any required query UNKNOWN        -> UNSUPPORTED
```

If statistical retained-set coverage fails with probability at most \(\alpha\), and the solver's decisive SAT/UNSAT certificates are semantically invalid with probability at most \(\beta\), then

```text
P(any false INVARIANT or false EXCLUDED conclusion) <= min(1, alpha + beta).
```

No independence between the two failure sources is needed. With a deterministic proof-carrying solver and trusted verifier, \(\beta=0\). RACH still does not implement a solver or convert a timeout into evidence.

## Ecological-program inference

The original disjunctive theorem remains exact only for its declared monotone OR assumptions. The ecological-program layer is a separate finite-state inference workflow: candidate programs are evaluated against repeated noisy observations, then passed to the existing robust-admissibility classifier across required analysis cells. It supports exact joint observation-panel design over a finite library, but its exhaustive search is deliberately limited to small, auditable candidate sets.

The analyst must predeclare the candidate program universe, feasible-state constraints, observation channels, acceptance thresholds, and search coverage. A `sampled` candidate universe must not be reported as complete merely because the state space within each sampled program was enumerated exactly.

## Exactness boundary

The Boolean theorems are exact only when the declared model permits every switch assignment compatible with the observation clauses. They do not cover hidden mutual exclusions, resource budgets, inhibitory effects, conjunctions, thresholds, feedbacks, or latent mechanisms folded into coarse labels. See [the theorem assumptions](docs/replaceability_theorems.md#exactness-assumptions) and [scope-failure audits](docs/failure_mode_audits.md).

The ecological-program module can represent a finite subset of those features, but it does not turn a candidate grammar into a universal model of nature. Its results remain conditional on the declared rules, feasible states, observation error model, acceptance rule, and candidate-program coverage.

The confidence-set lifting theorem controls false decisive conclusions only when the external procedure's simultaneous statistical coverage claim is valid and the true mechanism belongs to the declared candidate universe. The anytime theorem additionally requires coverage to hold across every certified look. The symbolic theorem additionally needs valid decisive solver certificates. None of these results can create power from data that do not distinguish candidates, repair an omitted mechanism, or certify their own assumptions.

## Relationship to domain models

RACH is deliberately **not** a floral-trait, pollination, fitness, population-genetic, site-level, or field-protocol model. It stores generic qualitative programs, candidate confidence sets, acceptance rules, coverage labels, and exact self-calibration benchmarks. It answers whether a motif would be classified as indispensable or excluded within those declared abstractions.

[`campanula-channel-identification`](https://github.com/zuizui0223/campanula-channel-identification) is a separate domain repository. It specifies a Campanula / island-floral-trait life cycle, including local reproduction versus establishment, nectar-guide routes, handling and pollen placement, selfing, recruitment, spatial structure, and prospective field measurements. It can translate a small predeclared set of its scenarios into a RACH candidate universe for a logical audit, but RACH contains neither those biological equations nor their empirical data and must not be presented as evidence for a Campanula mechanism.

## Scope boundary

This repository is the active methods home for RACH causal invariants. It contains no empirical data, field protocol, or domain-specific case-study contract. Every conclusion is conditional on the declared candidate mechanisms, observation or confidence-set validity, program grammar, and—for sampled program families—search coverage.

The initial theorem core is a clean extraction from earlier exploratory work. Generic theorem examples and finite benchmark families are retained; field-case code, UI prototypes, historical ABMs, and domain-specific data contracts are intentionally excluded.

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
-> distribution-agnostic confidence-set lifting with finite-sample error control
-> anytime confidence-set lifting with optional-stopping-safe error control
-> symbolic continuous / infinite candidate sets with solver-backed feasibility
-> real solver adapters with proof/error certificates and scalable robust design
```
