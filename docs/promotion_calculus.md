# RACH promotion calculus

## One question behind the repository

RACH should not be read as a collection of unrelated causal, statistical,
solver, and audit modules. Its narrow question is:

> **When may a local or conditional causal statement be promoted to a portable
> macro-law, and which certificate is needed for that promotion?**

A local rule can be correct while its promotion fails along more than one axis.
The repository's active theorem modules are organized around those failures.

## Four promotion axes

| Axis | Invalid automatic promotion | RACH object that blocks it | Current finite certificate |
|---|---|---|---|
| **Time** | specified local update \(\Rightarrow\) one world-level endpoint | finite closure calculus | ranking descent, recurrent cycle, or multistability witness |
| **Regime** | law in a natural regime \(\Rightarrow\) law under observer coupling | paired-regime comparison | two declared maps with exact closure verdicts |
| **Composition** | small law in every fixed closed context \(\Rightarrow\) small law for an open system | extension--compression witness | open trace-separation partition and bounded-degree relay compilation |
| **Knowledge** | one convenient candidate \(\Rightarrow\) justified conclusion | candidate consensus | unanimity over the retained candidate family; otherwise `UNRESOLVED` |

The first three are ontic / structural axes: they ask whether a proposed law is
preserved across time, regime, or allowed composition. The fourth is epistemic:
it asks whether the available candidate family permits reporting that structural
claim.

## Active theorem spine

```text
local transition rules
       |
       +-- time promotion ------> closure / recurrence certificates
       |
       +-- regime promotion ----> natural vs observer-coupled certificates
       |
       +-- composition promotion -> open-safe interface / relay-tree certificates
       |
retained candidate family
       |
       +-- knowledge promotion --> consensus or UNRESOLVED
```

The headline result currently under development is the composition branch:

\[
\text{small causal interface in every fixed closed extension}
\not\Rightarrow
\text{small interface for the declared open composition}.
\]

For the explicit family,

\[
\max_i \kappa(M_m\parallel E_i)=2,
\qquad
\kappa_{\mathrm{open}}(M_m;\mathcal E_m)=m+1.
\]

The relay-tree compilation preserves this separation with one fixed finite local
grammar, edge-local pairwise messages, maximum degree three, and sequential
quiescent macro-time.

## How candidate uncertainty fits now

Mechanistic uncertainty is not the headline theorem. It is the **epistemic
shadow** of a structural composition question.

A retained candidate may specify a different admissible future attachment,
context, or mechanism. A candidate-safe macro-interface must preserve every
allowed future response that remains live in the retained family. Thus candidate
consensus and open-interface complexity meet only after both objects have been
made explicit:

\[
\text{retained family of composition grammars}
\longrightarrow
\text{candidate-safe open interface}
\longrightarrow
\text{shared law, set-valued law, or UNRESOLVED}.
\]

The current repository does not yet implement this general bridge. It should not
be simulated by relabelling the existing motif-specific admissibility code.

## What counts as a successful next theorem

The next theorem should not merely make another witness larger. It should state
a structural criterion or sharp lower-bound schema for one of these questions:

1. Which classes of admissible extension grammars preserve a bounded open-safe
   quotient?
2. When does an open-safe interface also admit one candidate-independent
   deterministic macro transition rather than only candidate-indexed dynamics?
3. Which local communication or topology restrictions are insufficient to
   prevent interface inflation?

A theorem that cannot be placed on one of the four promotion axes is probably a
supporting tool, not a new RACH core claim.

## Boundary

RACH does not thereby claim that every ecosystem has a finite-state relay-tree
representation, that observers always alter the system, or that every candidate
family has a meaningful exact probability model. Every promotion certificate is
conditional on its declared state space, action grammar, candidate family, and
scope.
