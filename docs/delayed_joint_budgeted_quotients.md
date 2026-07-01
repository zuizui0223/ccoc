# Budgeted quotient ladder for delayed joint reset panels

## What this theorem adds

There are two established endpoints for the delayed joint family:

- over an expanding family of delays, finite passive stability does not certify
  open closure; and
- for one fixed family, enough fresh resettable trials identify every joint
  coordinate.

Most experimental designs lie between them. They determine neither the full
state nor nothing at all: they determine an exact **partial quotient**.

\[
\boxed{
\text{partial terminal-probe coverage}
\Longleftrightarrow
\text{a precise partial open-state quotient}.
}
\]

## Observation contract and reset panel

Fix

\[
x=(y,b_1,\ldots,b_m,r)\in\{0,1\}^{m+2}
\]

and delay \(H\). The contract contains one **zero-action baseline observation**

\[
\operatorname{base}(x)=y.
\]

This baseline is available before any resettable trial and does **not** consume a
trial or action budget.

Every later trial begins from a fresh copy of the same unknown initial state. A
legal information-bearing terminal word is one of

\[
\mathrm{wait}^{H}\mathrm{read}_i,
\qquad i=1,\ldots,m,
\]

or

\[
\mathrm{wait}^{H}\mathrm{intervene}.
\]

A panel \(P=(w_1,\ldots,w_N)\) may additionally contain wait-only words or
duplicate probes. Its full observed record is

\[
\Sigma_P(x)=
\left(
 y,
 \operatorname{Tr}(x,w_1),
 \ldots,
 \operatorname{Tr}(x,w_N)
\right).
\]

Define canonical terminal-probe coverage by

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

The order and multiplicity of trials do not enter this coverage definition.

## Theorem 1 — Exact panel quotient formula

For every legal reset panel \(P\), two initial states have the same record
\(\Sigma_P\) exactly when they agree on

\[
y,
\qquad
\{b_i:i\in R(P)\},
\qquad
r\ \text{when}\ J(P)=1.
\]

Consequently,

\[
\boxed{
|X/\!\sim_P|=2^{1+|R(P)|+J(P)}
}
\]

and every signature block has uniform residual cardinality

\[
\boxed{
|[x]_P|=2^{m+1-|R(P)|-J(P)}.
}
\]

Thus exact retained interface complexity is

\[
\boxed{
K(P)=1+|R(P)|+J(P).
}
\]

### Proof

The baseline records \(y\) even when \(P\) is empty. A wait-only trial leaves
all coordinates unchanged and adds no coordinate beyond this baseline. A covered
read at port \(i\) exposes \(b_i\). A covered intervention exposes
\(y\oplus r\), and the already recorded \(y\) therefore determines \(r\).

Hence agreement on the displayed coordinates is sufficient for identical panel
records. It is necessary because every covered terminal probe exposes its stated
coordinate. All uncovered exterior bits and, when \(J(P)=0\), the response bit
remain free. Counting retained and free binary coordinates proves both formulas.
\(\square\)

In particular, the empty panel has

\[
K(\varnothing)=1,
\]

not zero: it knows the focal baseline and nothing else.

## Theorem 2 — Sharp trial-budget frontier

With at most \(N\) fresh resettable trials,

\[
\boxed{
K_N^{\max}=1+\min\{N,m+1\}.
}
\]

Any \(\min\{N,m+1\}\) distinct terminal probes attain this bound. Every legal
trial has at most one terminal event before the grammar terminates, so no trial
can cover two independently addressable non-focal coordinates.

The frontier residual cardinality is

\[
2^{m+2-K_N^{\max}}.
\]

## Theorem 3 — Sharp total-action frontier

With total trial-action budget \(A\), every information-bearing terminal probe
costs exactly \(H+1\) actions. Therefore

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

Thus total effort and replica count are not interchangeable: one long trial
cannot replace several distinct terminal probes, because a trial terminates after
its first boundary event.

## Theorem 4 — Depth gate

With unlimited fresh copies but maximum trial depth \(D\),

\[
\boxed{
K_D^{\max}=
\begin{cases}
1, & D<H+1,\\[4pt]
m+2, & D\ge H+1.
\end{cases}
}
\]

No number of shallow trials crosses the delayed boundary. Once depth reaches
\(H+1\), unlimited replicas can cover every terminal probe.

\[
\boxed{
\text{replicate count},\quad
\text{total action effort},\quad
\text{and per-trial temporal depth}
\text{ are distinct resources.}
}
\]

## Theorem 5 — Marginal value and saturation

Adding one legal trial has only two possible exact effects:

\[
\Delta K=
\begin{cases}
1, & \text{it covers a previously uncovered terminal probe},\\
0, & \text{it is wait-only or duplicates an existing probe}.
\end{cases}
\]

When \(\Delta K=1\), residual ambiguity is halved:

\[
|[x]_{P\cup\{w\}}|=\frac12|[x]_P|.
\]

When \(\Delta K=0\), it is unchanged. Once all \(m+1\) terminal probes are
covered, the panel is exact and every further trial has zero marginal exact
value.

## Ecological projection and scope

Under a declared finite deterministic reset model, each independently targeted
boundary exposure resolves one named exterior or mechanism ambiguity factor. A
partial panel can therefore support an honest conditional law that retains
exactly the uncovered coordinates; it cannot justify silently discarding them or
claiming universal closure.

The theorem does **not** say field systems are resettable, binary, noise-free, or
governed by this prefix grammar. It also does not treat the zero-action baseline
as free empirical measurement in every application; whether it is observable is
part of the stated boundary contract. The result is an exact theorem conditional
on that contract.

## Executable certificates

`causal_model.delayed_joint_budgeted_quotients` provides:

- `TerminalProbeCoverage`, a canonical coverage summary;
- `PanelQuotientCertificate`, equality of the full baseline-plus-panel partition
  and the covered-coordinate projection;
- trial-, action-, and depth-budget frontier certificates; and
- `MarginalProbeValueCertificate`, one-bit-or-zero incremental value.

The Action workflow replays finite certificates and writes a deterministic
report. It is theorem regression, not stochastic power analysis.