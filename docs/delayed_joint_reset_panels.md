# Exact reset-panel complexity for delayed joint identification

## From no-go to an exact experimental requirement

The delayed joint nonidentifiability theorem says that no common finite
observation horizon certifies candidate-safe open closure over an expanding
family of delays. That result is intentionally negative.

This document gives its fixed-family positive counterpart. Once a specific
finite delayed joint grammar is declared, and once we explicitly assume access
to fresh resettable replicas of the same unknown initial state, we can state the
exact experiment required to identify the entire joint state.

The reset assumption is mathematical and operational:

- every trial begins from the same unknown initial macro state;
- terminal boundary events are not silently composed in one trajectory; and
- the panel record is the ordered tuple of traces from those independent trials.

It is not a claim that an ecological community, plot, or island can literally be
reset.

## Family and legal trials

Fix \(m\ge1\) exterior coordinates and delay \(H\ge0\). The unknown initial
state is

\[
(y,b_1,\ldots,b_m,r)\in\{0,1\}^{m+2}.
\]

A legal trial begins from the initial grammar state. For \(H\) steps the only
allowed action is `wait`. At the ready state the trial may end with exactly one
of

\[
\mathrm{read}_i,
\qquad i=1,\ldots,m,
\]

or

\[
\mathrm{intervene}.
\]

The terminal effects are

\[
\mathrm{read}_i:
\quad y\leftarrow b_i,
\]

\[
\mathrm{intervene}:
\quad y\leftarrow y\oplus r.
\]

A reset panel is an ordered finite list

\[
P=(w_1,\ldots,w_N)
\]

of such legal initial words. Its response signature is

\[
\Sigma_P(x)=
\left(
\operatorname{Tr}(x,w_1),
\ldots,
\operatorname{Tr}(x,w_N)
\right).
\]

The panel is **exact** when \(\Sigma_P\) is injective on every initial joint
state.

## Theorem — Sharp reset-panel complexity

For the delayed binary joint family, define the canonical panel

\[
P^\star=
\left(
\mathrm{wait}^{H}\mathrm{read}_1,
\ldots,
\mathrm{wait}^{H}\mathrm{read}_m,
\mathrm{wait}^{H}\mathrm{intervene}
\right).
\]

Then \(P^\star\) is exact, and it has the sharp resource vector

\[
\boxed{
N_{\min}=m+1,
\qquad
D_{\min}=H+1,
\qquad
A_{\min}=(m+1)(H+1).
}
\]

Here:

- \(N\) is the number of fresh resettable trials;
- \(D\) is the maximum action length of one trial; and
- \(A\) is the total sequential action count across all trials.

With \(m+1\) independent replicas run in parallel, elapsed wall-clock depth can
be \(H+1\). This does not reduce the required number of resettable experimental
units.

## Proof of sufficiency

Every trial trace contains its initial focal output, so \(y\) is observed.
For each \(i\), the final output of

\[
\mathrm{wait}^{H}\mathrm{read}_i
\]

is \(b_i\). The final output of

\[
\mathrm{wait}^{H}\mathrm{intervene}
\]

combined with the already recorded initial \(y\), determines \(r\) through

\[
r=y\oplus(y\oplus r).
\]

Thus the panel record reconstructs every coordinate

\[
(y,b_1,\ldots,b_m,r),
\]

so it is injective. Its counts are visibly

\[
N=m+1,
\qquad
D=H+1,
\qquad
A=(m+1)(H+1).
\]

## Proof of necessity

For each exterior coordinate \(b_i\), compare the two initial states

\[
x_0=(0,0,\ldots,0,0)
\]

and

\[
x_i=(0,0,\ldots,1_i,\ldots,0,0).
\]

Among all legal initial words, the only word whose output trace separates
\(x_0\) from \(x_i\) is

\[
\mathrm{wait}^{H}\mathrm{read}_i.
\]

Every other structural read addresses a coordinate that remains equal, and
`intervene` sees equal response type \(r=0\).

For response type, compare

\[
x_0=(0,0,\ldots,0,0)
\]

with

\[
x_r=(0,0,\ldots,0,1).
\]

The unique separating legal initial word is

\[
\mathrm{wait}^{H}\mathrm{intervene}.
\]

Therefore any exact panel must contain every one of the \(m+1\) distinct
terminal words. Each has length \(H+1\). Hence

\[
N\ge m+1,
\qquad
D\ge H+1,
\qquad
A\ge(m+1)(H+1).
\]

Together with sufficiency, all three bounds are sharp. \(\square\)

## What this adds to the promotion calculus

The theorem separates three resources that are easy to blur together:

\[
\boxed{
\text{time to a legal boundary event}
\neq
\text{number of independent intervention trials}
\neq
\text{total action effort}.
}
\]

The delayed no-go theorem says that waiting for a fixed horizon cannot certify
all members of an expanding family. The reset-panel theorem says that, once one
member is specified, exact identification is possible but needs a specific
combination of waiting time and independently targeted trials.

## Executable certificates

`causal_model.delayed_joint_reset_panels` provides:

- `ResettableTrialPanel` for explicit fresh-copy panel semantics;
- `ResetPanelExactnessCertificate` for injective panel records;
- `TerminalProbeNecessityCertificate` for one uniquely necessary probe per
  exterior coordinate and response type;
- `MissingTerminalProbeCertificate` for an explicit collision caused by an
  omitted probe; and
- `DelayedJointResetPanelComplexityCertificate` for the sharp resource vector.

The Action replay verifies finite parameter representatives and deterministic
JSON reports. It is certificate replay, not statistical power analysis or a
claim about unmodeled field systems.

## Ecological projection

Suppose a seasonal connection, rare disturbance, or controlled exposure becomes
possible only after a gate opens. Under the finite model here, distinguishing
\(m\) possible external sources plus one retained mechanism class needs at least
\(m+1\) independently resettable or independent exposure trials. More monitoring
of the same terminally altered unit cannot replace a missing targeted trial.

Parallel independent plots, mesocosms, or repeated controlled assays can reduce
elapsed time to the gate, but they do not erase the sample/replicate lower bound.
Whether a real field system meets the reset and common-initial-state assumptions
must be established separately.

## Scope boundary

This theorem concerns finite deterministic binary state families, a sequential
prefix grammar, and fresh resettable replicas. It does not establish a generic
optimal experimental design theorem for stochastic, continuous, non-resettable,
or partially observed ecological systems.