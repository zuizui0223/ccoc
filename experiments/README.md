# Reproducible exact benchmark suite

This directory turns the repository's finite benchmark families into paper-facing, reproducible tables.

## Run everything

From the repository root:

```bash
python experiments/run_all_benchmarks.py --output results
```

The runner has no third-party dependencies and produces only generated output. The default `results/` directory is intentionally not versioned: it should be regenerated from the current code and committed configuration whenever a manuscript figure is made.

## Outputs

| Output file | Benchmark family | Suggested manuscript role |
|---|---|---|
| `two_driver_phase_grid.csv` | Latent driver prevalence × witness sensitivity × inhibition × conjunction context | Main misspecification-risk surface; Figure on why NULL is powerful but conditional. |
| `multi_competitor_panel_grid.csv` | Exact joint panel versus strict greedy under multiple competitors and correlated environments | Main observation-synergy comparison; Figure on greedy failure. |
| `robust_panel_design_grid.csv` | Minimum-cost, coverage-greedy, minimax, and weighted-mean designs across budgets | Main cost–risk trade-off figure or table. |
| `canonical_anchors.csv` | Closed-form / canonical benchmark values | Text checks, supplement, and regression anchors. |
| `README.md` | Row counts and reproduction command | Generated audit record for the result directory. |

## Scientific interpretation

Every row is a **finite weighted enumeration under a declared benchmark generator**. These tables are not empirical data and should never be labelled as biological frequencies. They establish four narrower claims:

1. The Boolean theorem is exact inside its declared monotone-OR grammar.
2. Candidate omission, false NULLs, inhibition, conjunctions, and compatibility constraints have distinct failure signatures.
3. Joint observation panels can identify a focal mechanism when no singleton observation can.
4. Cheapest, declared-coverage-greedy, average-risk, and worst-case-risk plans can recommend different experiments.

## Figure workflow

Use the CSV files as inputs to a separate plotting script or notebook. Keep plotting separate from the enumerator: this preserves a clean provenance chain from model assumptions to numbers, then from numbers to a journal-specific visual design.

For each manuscript figure, record:

- commit SHA of the code used to generate the CSV;
- command line and output directory;
- selected columns, filters, and transformations; and
- the exact benchmark family and parameter grid shown.
