# RACH promotion calculus

## One question behind the repository

RACH asks:

> **When may a rule discovered inside a finite observation window be promoted to a
> portable causal law, and which certificate is required for that promotion?**

A law can be exactly correct for the observed inside and still fail to export to
longer time scales, to counterfactual ecosystem-outsides, or to a retained family
of candidate worlds.

## Three structural axes and one epistemic gate

| Axis | Invalid automatic promotion | RACH object that blocks it | Current finite certificate |
|---|---|---|---|
| **Time** | specified local update \(\Rightarrow\) one world-level endpoint | finite closure calculus | ranking descent, recurrent cycle, or multistability witness |
| **Window / outside** | rule inside a passive observation window \(\Rightarrow\) rule under every allowed exterior completion | observation-window completion calculus | passive-indistinguishable completion pair, boundary probe, and open trace quotient |
| **Knowledge** | one convenient candidate \(\Rightarrow\) justified conclusion | candidate consensus | unanimity over the retained candidate family; otherwise `UNRESOLVED` |

The first two are structural. The third is epistemic: it controls when a
structural result may be reported despite incomplete model knowledge.

## Boundary grammars are the central object

Let \(W\) be a finite observation window. Its outside is not simply “everything
outside a geographic patch.” It is the declared grammar \(\Gamma\) of external
completions, boundary inputs, attachments, and future actions that may influence
\(W\).

A rule inside \(W\) becomes an open-system law only when it is invariant across
that completion grammar:

\[
R_W(x,e,w)=R_W(x,e',w)
\]

for all allowed exterior completions \(e,e'\) and boundary words
\(w\in\Gamma^*\), after whatever finite boundary summary the theorem declares.

Thus closure means neither “the outside does not exist” nor “nothing entered
while we watched.” It means that, under the declared counterfactual grammar, the
outside can be omitted or summarized without changing future traces in the
window.

## Active theorem spine

```text
finite observation window W
        |
        +-- passive inside traces
        |       |
        |       +-- completion no-go:
        |               same passive trace, different boundary counterfactual
        |
        +-- declared completion grammar Gamma
        |       |
        |       +-- minimal open-safe causal interface
        |       +-- lower bounds from distinguishable completions
        |       +-- upper bounds from finite boundary blankets
        |
local transition rules
        |
        +-- time promotion -> closure / recurrence certificates
        |
retained candidate family
        |
        +-- knowledge gate -> shared conclusion or UNRESOLVED
```

The extension--compression and relay-tree results are now interpreted as a
specific boundary-completion family. They show that every fixed closed context
can have a small exact interface while the interface safe for all declared future
attachments is exponentially larger.

## The current no-go result

The observation-window witness proves, for every \(m\ge1\),

\[
K_{\mathrm{passive}}=1,
\qquad
K_{\mathrm{open}}=m+1.
\]

The passive window sees only a focal bit. It is compatible with
\(2^m\) exterior completion states for each focal output. A single permitted
boundary probe can expose any one of the hidden completion bits.

The witness is compiled to one fixed local grammar with pairwise messages and
maximum degree three. It therefore does not rely on an unbounded local lookup
table or a high-degree focal node.

## Operational regime comparison is now a special case

`observation_regime_closure.py` remains valuable. It compares two declared action
or observation regimes on the same state space. In the promotion calculus it is
not the principal inside/outside axis; it is a special operational case of
changing the declared action grammar.

For example, an observer-coupled map may be one permitted boundary action in
\(\Gamma\). The module should be reused when that exact two-regime comparison is
the claim, not as a generic slogan that observation changes ecosystems.

## Candidate uncertainty fits as an epistemic shadow

Mechanistic uncertainty is not the headline theorem. A retained candidate family
may specify different allowed completions or different boundary grammar. A
candidate-safe interface must preserve every future response that remains live
in that family:

\[
\text{retained completion grammars}
\longrightarrow
\text{candidate-safe open interface}
\longrightarrow
\text{shared law, set-valued law, or UNRESOLVED}.
\]

The general bridge from data to retained completion grammars is not implemented
yet. It must not be faked by relabelling old motif-specific code.

## What counts as a successful next theorem

A new theorem should strengthen one of these claims:

1. **Completion lower bound.** Independently addressable external completions
   force additive open-interface memory.
2. **Boundary blanket upper bound.** A stated finite causal blanket suffices to
   export a window rule to a declared open grammar.
3. **Stabilization criterion.** Characterize when enlarging the completion
   grammar stops refining the open-safe interface.
4. **Uniform-law criterion.** Separate a safe interface from existence of one
   candidate-independent deterministic macro transition.

A larger coordinate table, an extra provenance format, or a generic statistical
backend is not a new core theorem by itself.

## Boundary

RACH does not claim that every ecosystem has a finite-state representation, that
passive data are useless, or that an arbitrary outside can be exhaustively
simulated. Every statement is conditional on a declared observation window,
action grammar, completion class, horizon, and candidate family.
