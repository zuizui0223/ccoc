# Budgeted quotient ladder for delayed joint reset panels

## Why a middle theorem is needed

There are now two endpoints for the delayed joint family:

- without a fixed contract-wide horizon over an expanding delay family, passive
  stability does not certify open closure; and
- for one fixed family member, enough fresh resettable trials exactly recover
  every coordinate.

Most finite observation designs sit between those endpoints. They neither prove
full closure nor yield no information. This theorem gives the exact quotient that
a limited reset panel identifies.

\[
\boxed{
\text{partial experimental coverage}
\Longleftrightarrow
\text{a precise partial open-state quotient}.
}
\]

## Delayed joint panel model

Fix

\[
x=(y,b_1,\ldots,b_m,r)\in\{0,1\}^{m+2}
\]

and delay \(H\). Every trial begins from a fresh copy of the same unknown initial
state. A legal terminal probe is one of

\[
\mathrm{wait}^{H}\mathrm{read}_i,
\qquad i=1,\ldots,m,
\]

or

\[
\mathrm{wait}^{H}\mathrm{intervene}.
\]

A panel \(P\) may also contain wait-only trials or duplicate terminal probes.
Define its canonical coverage by

\[
R(P)=\left\{i:
\mathrm{wait}^{H}\mathrm{read}_i\in P
\right\},
\]

and

\[
J(P)=
\mathbf 1\left\{
\mathrm{wait}^{H}\mathrm{intervene}\in P
\right\}.
\]

The order and multiplicity of trials are deliberately absent from this definition.

## Theorem 1 — Exact panel quotient formula

For every legal reset panel \(P\), two initial states have the same complete
panel record exactly when they agree on

\[
y,
\qquad
\{b_i:i\in R(P)\},
\qquad
r\ \text{when}\ J(P)=1.
\]

Equivalently,

\[
\boxed{
|X/\!\sim_P|=2^{1+|R(P)|+J(P)}.
}
\]

Every panel-signature block has the same residual cardinality

\[
\boxed{
|[x]_P|=2^{m+1-|R(P)|-J(P)}.
}
\]

Thus the exact retained interface complexity is

\[
\boxed{
K(P)=1+|R(P)|+J(P).
}
\]

### Proof

Every trial trace begins with \(y\). A wait-only word leaves the state unchanged,
so it provides no coordinate beyond \(y\). The terminal read at port \(i\)
returns \(b_i\), while terminal intervention returns \(y\oplus r\); combined
with the initial \(y\), this determines \(r\).

Therefore agreement on the displayed coordinates is sufficient for equal panel
records. It is necessary because every covered terminal probe explicitly reveals
its displayed coordinate. All uncovered \(b_i\) coordinates and, when
\(J(P)=0\), the response bit may vary freely within a panel-signature block.
There are exactly \(1+|R(P)|+J(P)\) retained binary coordinates and the stated
number of omitted binary coordinates. \(\square\)

## Theorem 2 — Sharp trial-budget frontier

Let at most \(N\) fresh resettable trials be allowed. Then

\[
\boxed{
K_N^{\max}=1+\min\{N,m+1\}.
}
\]

A panel consisting of any \(\min\{N,m+1\}\) distinct terminal probes attains
this value.

No panel with \(N\) trials can cover more than \(N\) terminal probes: every
legal trial reaches at most one terminal event before the grammar terminates.
Since each terminal probe adds only one of the \(m+1\) non-focal coordinates,
the bound is sharp.

The residual ambiguity at the frontier is

\[
2^{m+2-K_N^{\max}}.
\]

## Theorem 3 — Sharp total-action budget frontier

Let the total number of actions across all fresh trials be at most \(A\). Each
information-bearing terminal probe has length \(H+1\). Therefore

\[
\boxed{
K_A^{\max}
=
1+
\min\left\{
\left\lfloor\frac{A}{H+1}\right\rfloor,
 m+1
\right\}.
}
\]

This is attained by the corresponding number of distinct terminal probes.

This theorem distinguishes total effort from the number of experimental units:
three trials at depth four and one trial at depth twelve may have the same action
count, but only the former can cover three separately addressable terminal
coordinates under the declared grammar.

## Theorem 4 — Depth gate

Suppose fresh trials are unlimited but each trial may contain at most \(D\)
actions. Then

\[
\boxed{
K_D^{\max}=
\begin{cases}
1, & D<H+1,\\[4pt]
m+2, & D\ge H+1.
\end{cases}
}
\]

No number of shallow trials crosses the delayed boundary event. Once a trial can
reach it, unlimited resettable replicas can cover every terminal probe.

This makes the resource axes non-interchangeable:

\[
\boxed{
\text{trial count},\quad
\text{total action effort},\quad
\text{and per-trial temporal depth}
\text{ are distinct constraints.}
}
\]

## Theorem 5 — Exact marginal value and saturation

Adding one legal trial to a panel has only two possible exact effects:

\[
\Delta K=
\begin{cases}
1, & \text{the trial covers a previously uncovered terminal probe},\\
0, & \text{the trial is wait-only or duplicates a covered probe}.
\end{cases}
\]

When \(\Delta K=1\), residual ambiguity is halved:

\[
|[x]_{P\cup\{w\}}|=\frac12|[x]_P|.
\]

When \(\Delta K=0\), it is unchanged. After all \(m+1\) terminal probes are
covered, the panel is exact and every additional trial has zero marginal exact
value.

## What this does and does not mean ecologically

The theorem says that, **under a declared finite deterministic reset model**, every
independently targeted boundary exposure has a transparent value: it resolves one
explicitly named ambiguity factor, not a vague fraction of “complexity.”

Ecologically, this gives a disciplined language for partial resolution. A set of
replicated assays, plots, or controlled exposures may justify a conditional law
that retains only the still-uncovered exterior/mechanism coordinates. It does not
justify silently discarding them, and it does not turn partial coverage into a
claim of universal closure.

The theorem does not assume real ecosystems are resettable, binary, noise-free,
or governed by this one-prefix grammar. Testing whether a biological design
approximately meets those assumptions is a separate empirical task.

## Executable certificates

`causal_model.delayed_joint_budgeted_quotients` provides:

- `TerminalProbeCoverage`, which canonically reduces a panel to covered terminal
  probes;
- `PanelQuotientCertificate`, which verifies exact agreement between full panel
  signatures and the covered-coordinate projection;
- trial-, action-, and depth-budget frontier certificates; and
- `MarginalProbeValueCertificate`, which verifies one-bit-or-zero incremental
  value.

The replay workflow checks finite parameter instances and writes a deterministic
report. It is certificate replay for the stated theorem, not a stochastic power
calculation.