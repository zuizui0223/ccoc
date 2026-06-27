# Robust admissibility

## Inputs

The classifier accepts a predeclared motif vocabulary and one or more **robustness cells**. A cell is an analysis context such as a prior family, tolerance value, endpoint convention, or sampling plan. It contains evaluated program runs with an externally determined acceptance flag.

At least one cell must be marked `required`. Optional cells are retained for reporting but cannot, by themselves, support a cross-cell universal claim. This rejects the vacuous case in which every supplied cell is optional and `all(...)` would otherwise classify every motif as invariant.

Each required cell also declares its `coverage_mode`:

- `sampled`: evaluated runs are only a finite sample of the candidate-program space;
- `exhaustive`: every program in the declared finite cell has been evaluated; or
- `solver_backed`: an external complete satisfiability/model-checking procedure has certified the cell result.

The module does not decide whether a run should be accepted or whether a coverage declaration is credible. Those decisions belong to the program-specific pattern distance, constraint predicate, tolerance rule, and search procedure.

## Cell-level definitions

For a motif \(m\) and one cell \(c\), let \(A_c\) be its accepted runs.

\[
m\text{ invariant in }c \iff \forall r\in A_c,\;m\in r,
\]

\[
m\text{ excluded in }c \iff \forall r\in A_c,\;m\notin r.
\]

A mixed accepted set is unresolved in that cell.

## Cross-cell definition

For a declared required cell collection \(\mathcal C\), a motif is:

\[
\text{robustly invariant}
\iff
\forall c\in\mathcal C\;\forall r\in A_c,\;m\in r,
\]

\[
\text{robustly excluded}
\iff
\forall c\in\mathcal C\;\forall r\in A_c,\;m\notin r.
\]

If any required cell has \(A_c=\varnothing\), both universal claims are marked **unsupported**. This prevents a conclusion based only on convenient analysis settings that happened to yield accepted programs.

## Claim coverage

Every `MotifClassification` now carries a separate `claim_coverage` value:

| Value | Meaning |
|---|---|
| `sampled` | The reported status applies to all evaluated accepted runs, but at least one required cell was sampled rather than complete. |
| `complete` | Every required cell was declared `exhaustive` or `solver_backed`; the reported status is complete within the declared grammar and acceptance rule. |
| `unsupported` | At least one required cell had no accepted run, so no cross-cell conclusion is supported. |

The `required_cell_coverage` mapping is retained in both the report and each motif classification, so a reader can see which cell kept a conclusion at sampled strength.

## What the label means

An `invariant + sampled` result means only:

```text
Within the declared grammar, parameter domain, acceptance rule,
required robustness cells, and evaluated accepted runs, every accepted run includes m.
```

An `invariant + complete` result is stronger, but remains conditional on the declared grammar, parameter domain, acceptance rule, and correctness of the exhaustive or solver-backed coverage claim. Neither label is a posterior probability nor a universal statement about nature.

## Relation to the exact replaceability core

The exact disjunctive theorem core answers when a mechanism is structurally forced ON in a finite Boolean model. Robust admissibility is broader: it aggregates accepted program runs across explicitly declared analysis cells. The two can be combined later, but neither silently substitutes for the other.
