# Risk-robust observation-panel design

## Why a second optimization layer is needed

`minimum_discriminating_panel` is exactly right for one question:

> What is the cheapest panel that forces a focal mechanism ON in the declared monotone-OR grammar?

That is not automatically the same as:

> What panel is least likely to yield a false necessity claim when the grammar, witness biology, or measurement process may be wrong?

`causal_model.robust_panel_design` makes that distinction explicit. It evaluates every structurally resolving candidate panel across a finite set of declared true-model scenarios, then chooses by cost, coverage-greedy elimination, worst-case risk, or weighted mean risk.

## Two layers

### Layer 1: declared structural resolution

For every candidate NULL panel \(P\), the module first requires

\[
\text{focal } j \text{ is forced ON under the declared model and } P.
\]

Panels that do not meet this condition are never ranked as causal-necessity designs.

### Layer 2: finite scenario risk

For each finite scenario \(s\), with a `TruthTableModel`, optional observation channels, and optional state priors, it computes

\[
R_s(P)=\Pr(j=0\mid \text{target PRESENT and all traits in }P\text{ reported NULL};s).
\]

A zero-probability reported panel is treated as a model contradiction. It is ranked as maximally unsafe during robust optimization rather than being mistaken for zero risk.

## Objectives

| Selector | Objective |
|---|---|
| `choose_minimum_cost_panel` | Cheapest structurally resolving panel; risk only breaks cost ties. |
| `choose_coverage_greedy_panel` | Declared competitor elimination gain per unit cost; no access to true-scenario risks. |
| `choose_robust_panel(..., MINIMAX)` | Minimize \(\max_s R_s(P)\). |
| `choose_robust_panel(..., WEIGHTED_MEAN)` | Minimize weighted average \(\sum_s w_s R_s(P)/\sum_s w_s\). |

The minimax and weighted-mean selectors are exact finite subset searches. Their difference is scientific rather than technical: minimax protects against a rare but severe scenario, whereas weighted mean treats scenario weights as an explicit frequency or decision-weight model.

## Canonical shared-witness example

Declared mechanisms are focal \(j\), competitors \(c_1,c_2\), and an unmodelled inhibitor \(h\). The declared model contains:

\[
\text{target}=j\lor c_1\lor c_2,
\qquad
\text{shared}=c_1\lor c_2,
\qquad
\text{witness}_i=c_i.
\]

Candidate costs are:

| Candidate | Cost | Declared elimination |
|---|---:|---|
| `shared` | 0.5 | \(c_1,c_2\) |
| `witness_1` | 1 | \(c_1\) |
| `witness_2` | 1 | \(c_2\) |

Thus minimum-cost and coverage-greedy selection choose `shared`.

The benchmark then evaluates two true scenarios:

1. **Frequent private-noise scenario** (weight 10): private witnesses have sensitivity 0.9, while `shared` is reliable.
2. **Rare shared-inhibition scenario** (weight 1): `shared` is absent whenever \(h=1\), even if a competitor is active; private witnesses remain reliable.

The exact results are:

| Panel | Cost | Worst-case risk | Weighted mean risk |
|---|---:|---:|---:|
| `shared` | 0.5 | \(3/8\) | \(3/88\) |
| `witness_1,witness_2` | 2 | \(21/142\) | \(105/781\) |

Consequently:

- minimum-cost and coverage-greedy choose `shared`;
- minimax chooses `witness_1,witness_2` because \(21/142 < 3/8\);
- weighted-mean risk chooses `shared` because the shared-inhibition scenario has low declared weight.

This is not an inconsistency. It exposes the decision commitment hidden in every observation plan.

## Example

```python
from causal_model import (
    FinitePanelScenario,
    NullObservationCandidate,
    RobustObjective,
    StructuralModel,
    TruthTableModel,
    choose_robust_panel,
)

# Build a declared model, candidates, and finite scenarios, then:
result = choose_robust_panel(
    declared_model,
    focal_mechanism=0,
    target_trait="target",
    candidates=candidates,
    scenarios=scenarios,
    objective=RobustObjective.MINIMAX,
    max_cost=5.0,
)
```

`result.scenario_risks` retains the individual scenario probabilities and focal-OFF posteriors, so a final recommendation can be audited rather than presented as a black-box score.

## Interpretation rules

1. A minimax panel is only as good as the scenario set. It protects against **declared** adverse cases, not unknown unknowns.
2. Weighted means require a documented rationale for scenario weights. They are not objective probabilities unless empirically calibrated.
3. Minimum cost and coverage greedy are useful baselines, but their structural knowledge alone cannot see inhibitor or measurement risk.
4. A budget can make the robust panel unavailable. This is a scientific result: the budget is insufficient for the requested robustness criterion.
5. The finite enumeration is intentionally exponential in candidate count. For large panels, use it to audit a reduced candidate set or extend the module with an integer-programming solver and certificate.
