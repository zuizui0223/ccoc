# Known-truth finite benchmarks and error calibration

## Purpose

Robust-admissibility labels are only as trustworthy as the search coverage behind them. This module supplies small, fully enumerated program universes where the true classification is known exactly, then asks how often a sampled analysis would report a different result.

The benchmark is deliberately finite and explicit. It tests the inference layer; it does not claim to model ecological reality.

## Finite benchmark cell

A `FiniteBenchmarkCell` contains every evaluated program in a small declared universe, its active motif set, and its externally assigned acceptance flag. The full cell is converted to a `RobustnessCell` with `CoverageMode.EXHAUSTIVE`, producing the finite known-truth report.

A selected subset of the same runs is converted to a `CoverageMode.SAMPLED` cell. Comparing the two reports yields, for each motif:

| Outcome | Meaning |
|---|---|
| `match` | The sampled status equals the complete finite truth. |
| `false_invariant` | Sampling declared a motif invariant although finite truth did not. |
| `false_excluded` | Sampling declared a motif excluded although finite truth did not. |
| `conservative_unresolved` | Sampling remained unresolved even though finite truth was invariant or excluded. |
| `unsupported` | The selected sample contained no accepted run in a required cell. |

## Exact calibration curve for one cell

`calibrate_single_cell_exhaustively` enumerates every equal-size sample from a single finite benchmark cell and counts these outcomes. For example, the exact false-invariant rate at sample size \(n\) is

\[
\frac{\#\{P: |P|=n,\;\text{sampled classification is false invariant}\}}
{\binom{N}{n}},
\]

where \(N\) is the full number of evaluated runs.

The implementation has a `max_panels` safety limit because \(\binom{N}{n}\) grows quickly. It is intended for deliberately small known-truth grammars, not production-scale program families.

## Recommended benchmark families

A useful benchmark suite should vary at least:

1. motif prevalence among accepted programs;
2. the number of required robustness cells;
3. acceptance sparsity, including cells with few accepted runs;
4. latent or omitted motifs, to quantify candidate-set misspecification separately from finite sampling;
5. tolerance settings that change which programs are accepted; and
6. observation noise that can turn a true signal into a NULL result.

The current primitive covers exact calibration conditional on a finite declared universe. The next scientific step is to define those benchmark families from qualitative generative programs with known ground truth.
