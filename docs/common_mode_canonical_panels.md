# Common-mode robustness for canonical distinguishing panels

## Why independent-cell robustness is not enough

A panel can have many nominally redundant cells and still be fragile if those
cells fail together. Examples include multiple sampling windows on one camera,
several assays sharing one reagent batch, repeated observations at one site, or
multiple plots exposed to the same storm, access route, observer, or power
supply.

The independent-cell theorem treats every declared cell as separately lossable.
This document replaces that assumption by an explicit common-mode failure
contract.

\[
\boxed{
\text{raw replicate count is not failure diversity.}
}
\]

## Setup

Let \(P\) be an exact canonical distinguishing panel and let

\[
S_P(b,b')=P\cap D_{b,b'}
\]

be the selected separators for one pair of canonical boundary classes. A finite
family of failure modes is

\[
\mathcal M=\{M_1,\ldots,M_q\},
\qquad M_j\subseteq P.
\]

A mode may delete all cells assigned to one shared failure source. Every panel
cell must lie in at least one mode; otherwise that cell is outside the declared
failure contract and cannot be used as evidence of common-mode resilience.

A failure event with budget \(r\) may remove the union of any at most \(r\)
modes.

For each blanket pair define the **mode-cover number**

\[
\lambda_{\mathcal M}(P;b,b')
=
\min\left\{
|J|:
S_P(b,b')\subseteq\bigcup_{j\in J}M_j
\right\}.
\]

It is the smallest number of declared common-mode failures that can erase every
selected separator for that pair.

## Theorem 1 — Exact common-mode robustness criterion

For any \(r\ge0\), the following are equivalent:

\[
\boxed{
P\text{ remains exact after every union of at most }r\text{ failure modes}
}
\]

and

\[
\boxed{
\forall b\ne b',\quad
\lambda_{\mathcal M}(P;b,b')\ge r+1.
}
\]

Hence the exact common-mode tolerance of a panel is

\[
\boxed{
r_\star(P;\mathcal M)
=
\min_{b\ne b'}\lambda_{\mathcal M}(P;b,b')-1.
}
\]

### Proof

If every selected separator set needs at least \(r+1\) modes to cover it, then
deleting any at most \(r\) modes leaves at least one selected separator for
every pair. The panel remains injective by the canonical-panel theorem.

Conversely, if a pair has a mode cover of size at most \(r\), delete exactly
those modes. Every selected separator of that pair is removed, so the retained
panel signatures collide. \(\square\)

## Theorem 2 — Singleton reduction

Suppose every mode is a singleton cell:

\[
\mathcal M=\{\{c\}:c\in P\}.
\]

Then

\[
\lambda_{\mathcal M}(P;b,b')=|S_P(b,b')|,
\]

so Theorem 1 reduces exactly to independent-cell robustness:

\[
\boxed{
r_\star(P;\mathcal M)=f_\star(P).}
\]

Thus common-mode robustness is a strict extension of the earlier theorem, not a
competing definition.

## Theorem 3 — Common-mode collapse / no free replication

For every \(k\ge1\), there is a two-class panel with \(k\) distinct separating
cells such that all \(k\) lie in a single failure mode. Its independent-cell
tolerance is

\[
f_\star=k-1,
\]

but its common-mode tolerance is

\[
\boxed{r_\star=0.}
\]

### Proof

Each of the \(k\) cells separates the two classes, so losing fewer than \(k\)
individual cells leaves one separator. But one common mode contains all
separators; deleting it removes the entire separation set. \(\square\)

This is a sharp warning: collecting more repeated observations inside one shared
failure domain gives no positive guarantee against one failure of that domain.

## Theorem 4 — Site-bundle law

Suppose there are \(s\) independent sites and \(h\) repeated cells within each
site, with every cell separating the same two boundary classes. The raw panel has
\(sh\) cells, so independent-cell tolerance is

\[
f_\star=sh-1.
\]

If one failure mode is loss of one whole site, then the common-mode tolerance is

\[
\boxed{r_\star=s-1.}
\]

The number of repetitions within a site changes raw-cell tolerance but not
site-level common-mode tolerance.

## Theorem 5 — Mode-disjoint packing lower bound

Take a collection \(Q\) of class pairs whose selected separator sets have
disjoint mode supports. If a panel is required to survive \(r\) mode losses,
each pair in \(Q\) must involve at least \(r+1\) distinct modes. Therefore the
number of distinct failure modes used by the design is at least

\[
\boxed{(r+1)|Q|.}
\]

This is a lower bound on **failure diversity**, not merely raw observation count.
It does not claim that arbitrary common-mode robust panel optimization is easy.

## Constructive failure report

A failed robustness certificate returns:

- the ambiguous canonical blanket pair \((b,b')\);
- a minimum mode cover of its selected separators;
- the cells deleted by the union of those modes; and
- the retained panel on which the pair collides.

Thus a design can say not just “one-mode robustness fails,” but exactly which
site, power system, weather window, or observer group is a weakest link for
which regime distinction.

## Ecological and field interpretation

This theorem is the operational correction to treating outdoor measurements as
independent by default. Multiple cameras on one power source, repeated assays on
one sampling day, or observations within one inaccessible valley may carry many
cells but only one relevant failure mode.

A defensible report therefore has two pieces:

1. the canonical boundary distinctions that must be preserved; and
2. the declared failure-mode architecture of sites, devices, observers, weather
   windows, transport, and power.

\[
\boxed{
\text{Robustness comes from separator diversity across failure domains,}
\quad
\text{not from replicate count alone.}
}
\]

## Executable certificates

`causal_model.common_mode_canonical_panels` provides:

- `FailureModeFamily` and `ModeCoverCertificate`;
- `CommonModePanelProfile` and `CommonModeRobustnessCertificate`;
- `CommonModeAmbiguityCertificate`;
- `SingletonModeReductionCertificate`;
- `ModeDisjointPackingCertificate`; and
- common-mode collapse and site-bundle witness families.

The GitHub Action replays finite certificates for declared mode families. It does
not estimate real-world failure probabilities or assume that mode assignments
are empirically established without a separate field design argument.