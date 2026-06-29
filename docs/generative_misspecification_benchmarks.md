# Exact generative misspecification benchmarks

## Aim

The failure-mode audits establish that a single omitted route, false NULL, inhibitor, conjunction, or compatibility constraint can invalidate a last-driver conclusion. This benchmark family turns those counterexamples into **continuous, exact sensitivity analyses**.

The declared inference model is deliberately fixed:

\[
\text{target}=j\lor c,
\qquad
\text{witness}=c,
\]

and the reported observation is

\[
\text{target PRESENT},\qquad \text{witness NULL}.
\]

The declared model therefore always calls focal driver \(j\) forced ON. The benchmark asks a sharper question:

\[
R=\Pr(j=0\mid \text{target PRESENT, witness reported NULL};\;\theta),
\]

where \(\theta\) controls structured departures of the true generator from the declared model. `R` is the exact posterior false-necessity risk, calculated by weighted enumeration of a finite state space rather than simulation.

## Parameters

| Parameter | Meaning |
|---|---|
| `latent_driver_prevalence` | Probability that an unmodelled latent target route is available. When available, its switch is Bernoulli(0.5). |
| `witness_sensitivity` | Probability of reporting witness PRESENT when the true witness is present. A false NULL occurs with probability \(1-\text{sensitivity}\). |
| `witness_false_positive_rate` | Probability of reporting witness PRESENT when the true witness is absent. |
| `inhibition_prevalence` | Probability that an active competitor's witness is suppressed. |
| `conjunction_prevalence` | Probability that the true declared core changes from \(j\lor c\) to \(j\land c\). A latent route, if enabled, may still independently generate the target. |
| `compatibility_constraint_prevalence` | Probability of a context where \(c=1\) requires \(j=1\). |

The focal and declared competitor have Bernoulli(0.5) priors before the compatibility rule. These probabilities are benchmark inputs, not biological defaults.

## Anchor checks

The test suite pins the following exact limiting cases.

| Setting | Report probability | False-necessity risk \(R\) | Interpretation |
|---|---:|---:|---|
| All misspecification parameters zero, sensitivity 1 | \(1/4\) | 0 | The declared model is correct. |
| Latent route prevalence 1 | \(3/8\) | \(1/3\) | One hidden alternative route is enough to make the focal non-necessary in one third of reported cases. |
| Sensitivity 0.9 only | \(0.3\) | \(1/12\) | A 10% false-NULL rate yields 8.3% posterior false necessity. |
| Inhibition prevalence 1 | \(3/4\) | \(1/3\) | NULL no longer certifies competitor OFF. |
| Conjunction prevalence 1, perfect measurement | 0 | impossible | The report is incompatible with the true model; do not compute a necessity claim. |
| Compatibility prevalence 1 | \(1/4\) | 0 | The constraint removes competitor-only explanations in this specific panel. |

## Running a sweep

```python
from causal_model import phase_table_markdown, sweep_two_driver_family

points = sweep_two_driver_family({
    "latent_driver_prevalence": (0.0, 0.25, 0.5, 1.0),
    "witness_sensitivity": (1.0, 0.95, 0.9),
    "inhibition_prevalence": (0.0, 0.25, 0.5),
})
print(phase_table_markdown(points))
```

The output is a Markdown table that can be saved directly with a manuscript analysis. For a figure, use the returned `TwoDriverSweepPoint` objects to plot `false_necessity_risk` against any two axes while fixing the remaining parameters.

## Interpretation rules

1. A high \(R\) does not disprove the Boolean theorem; it says the theorem's declared model is too fragile under the specified true-generator departures.
2. A zero \(R\) under one benchmark setting does not validate the ecological grammar. It only shows no focal-OFF explanation exists in that finite family at that parameter point.
3. `report_is_impossible` takes priority over a numeric risk. Under a conjunction-dominated generator, target PRESENT plus witness NULL may indicate model contradiction, not evidence for focal necessity.
4. The family separates *noise-induced* risk from *structural misspecification* risk by reporting both risk after the noisy observation and risk under perfect witness measurement.

## Next extension

This two-driver family is intentionally interpretable. The next extension should generalize to multiple observed competitors, multiple latent routes, heterogeneous priors, correlated environmental contexts, and observation panels selected by `minimum_discriminating_panel`. At that point the benchmark can compare greedy and exact panel selection under the same misspecification surfaces.
