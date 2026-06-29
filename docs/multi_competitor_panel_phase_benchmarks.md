# Multi-competitor panel phase benchmarks

## Question

The exact theorem says that a focal mechanism becomes structurally indispensable when every competing driver of a required target has been eliminated. With private competitor witnesses, this requires a **joint** NULL panel. The earlier synergy theorem showed that a greedy policy can fail abstractly; this module measures that failure alongside misspecification risk under a shared environmental context.

The declared model is

\[
\text{target}=j\lor c_1\lor\cdots\lor c_n,
\qquad
\text{witness}_i=c_i.
\]

The candidate observations are NULL results for the private witnesses.

## Selection policies

### Exact panel

`compare_panel_strategies` calls `minimum_discriminating_panel` on the declared grammar. With unit-cost private witnesses, it selects

\[
\{\text{witness}_1,\ldots,\text{witness}_n\},
\]

so the declared model labels focal driver \(j\) forced ON.

### Strict greedy panel

`strict_greedy_panel_traits` implements a deliberately narrow greedy criterion: add a witness only if that single addition immediately makes \(j\) forced ON. For \(n\ge2\), every singleton still leaves another competitor, so its marginal resolution gain is zero and strict greedy returns the empty panel.

This is not a claim that every practical greedy heuristic fails. It is the exact no-lookahead rule ruled out by the synergy theorem, retained here as a transparent baseline.

## Correlated true generator

A binary environment \(E\) changes the conditional probabilities of all competitors, latent routes, and witness inhibitors. They are conditionally independent given \(E\), but correlated marginally. This permits, for example:

- a high-environment context where all competitors tend to be ON;
- a low-environment context where all competitors tend to be OFF;
- context-specific inhibition, so the same high environment can make all witnesses NULL despite active competitors; and
- latent routes whose prevalence covaries with competitor activity.

For a selected panel \(P\), the exact benchmark reports

\[
\Pr(j=0\mid \text{target PRESENT, all witnesses in }P\text{ reported NULL}).
\]

It also reports the corresponding risk under perfect witness measurement. The gap identifies the component attributable to observation error rather than structural misspecification.

## Anchor scenarios

For two competitors, no latent routes, no inhibition, and perfect observations, exact selects both witnesses and has risk zero. Strict greedy selects nothing and makes no necessity claim.

With one latent route that is ON with probability 0.5, exact still selects both observed competitor witnesses, but its false-necessity risk is

\[
\frac13.
\]

With a shared environment where competitors are all OFF in low context and all ON in high context, 90% witness sensitivity yields risk

\[
\frac1{102},
\]

rather than the much larger risk under independent competitors. The joint NULL panel is informative because it identifies the low environment.

If the same high context also suppresses every witness, the risk rises to

\[
\frac13,
\]

even with perfect measurement of the suppressed phenotype. This is structural, not ordinary detection error.

For a pure conjunction target, target PRESENT plus all competitor witnesses NULL is impossible under perfect measurement. The correct output is therefore a zero report probability, not a numeric necessity risk.

## Usage

```python
from causal_model import (
    MultiCompetitorFamilyParameters,
    compare_panel_strategies,
    panel_phase_table_markdown,
    sweep_panel_phase_family,
)

comparison = compare_panel_strategies(
    MultiCompetitorFamilyParameters(
        competitor_count=3,
        latent_route_count=1,
        latent_on_probability_low=0.1,
        latent_on_probability_high=0.6,
        competitor_on_probability_low=0.1,
        competitor_on_probability_high=0.9,
        inhibition_probability_low=0.0,
        inhibition_probability_high=0.4,
        witness_sensitivity=0.9,
    )
)

points = sweep_panel_phase_family({
    "competitor_count": (2, 3, 4),
    "latent_route_count": (0, 1, 2),
    "latent_on_probability_low": (0.0, 0.2),
    "latent_on_probability_high": (0.2, 0.6),
    "witness_sensitivity": (1.0, 0.95, 0.9),
})
print(panel_phase_table_markdown(points))
```

## Reading results

- `exact.declared_forced_on=True` means only that the selected panel resolves the **declared** OR grammar.
- `exact.false_necessity_risk` quantifies how often this declared necessity is false under the chosen true generator.
- `strict_greedy.declared_forced_on=False` is not an error label; it records that a no-lookahead policy refused to collect a jointly informative panel.
- A low exact risk can occur because the panel genuinely constrains the true state space, or because the benchmark parameterization makes focal-OFF states rare. Interpret both the risk and the report probability.
- A zero report probability means model contradiction under the finite truth generator; it should not be treated as strong evidence for the focal mechanism.

## Next extension

The present module keeps the observation candidates as private witnesses. The next implementation should permit shared and imperfect witnesses with costs, then compare:

1. strict greedy resolution gain;
2. coverage-style greedy elimination gain;
3. exact minimum-cost design; and
4. robust designs that optimize worst-case or average risk across a declared misspecification grid.
