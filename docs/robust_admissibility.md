# Robust admissibility

## Inputs

The classifier accepts a predeclared motif vocabulary and one or more **robustness cells**. A cell is an analysis context such as a prior family, tolerance value, endpoint convention, or sampling plan. It contains evaluated program runs with an externally determined acceptance flag.

At least one cell must be marked `required`. Optional cells are retained for reporting but cannot, by themselves, support a cross-cell universal claim. This rejects the vacuous case in which every supplied cell is optional and `all(...)` would otherwise classify every motif as invariant.

The module does not decide whether a run should be accepted. That decision belongs to the program-specific pattern distance, constraint predicate, and tolerance rule.

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

## What the label means

A robust-invariant label currently means only:

```text
Within the declared grammar, parameter domain, acceptance rule,
required robustness cells, and evaluated accepted runs, every accepted run includes m.
```

It is not a posterior probability and not a universal statement about nature. More importantly, it is not yet proof over all programs in a cell: finite search can miss an admissible counterexample. The next implementation stage will add coverage metadata, such as `sampled`, `exhaustive`, or `solver-backed`, so reports cannot blur sampled unanimity with exhaustive necessity.

## Relation to the exact replaceability core

The exact disjunctive theorem core answers when a mechanism is structurally forced ON in a finite Boolean model. Robust admissibility is broader: it aggregates accepted program runs across explicitly declared analysis cells. The two can be combined later, but neither silently substitutes for the other.
