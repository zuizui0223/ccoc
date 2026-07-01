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
| **Window / outside** | rule inside a passive observation window \(\Rightarrow\) rule under every allowed exterior completion | completion lower bounds plus dynamic-blanket factorization | separating boundary word, canonical open quotient, or update-closed boundary summary |
| **Knowledge** | one convenient candidate \(\Rightarrow\) justified conclusion | candidate consensus | unanimity over the retained candidate family; otherwise `UNRESOLVED` |

The first two are structural. The third is epistemic: it controls when a
structural result may be reported despite incomplete model knowledge.

## Boundary grammars are the central object

Let \(W\) be a finite observation window. Its outside is not simply “everything
outside a geographic patch.” It is the declared grammar \(\Gamma\) of external
completions, boundary inputs, attachments, and future actions that may influence
\(W\).

A rule inside \(W\) becomes an open-system law only when exterior effects can be
omitted or stored in a finite dynamic boundary summary without changing every
future window trace:

\[
R_W(x,e,w)=R_W(x,e',w)
\]

for all allowed exterior completions \(e,e'\) and boundary words
\(w\in\Gamma^*\), after conditioning on that summary.

Thus closure means neither “the outside does not exist” nor “nothing entered
while we watched.” It means that, under the declared counterfactual grammar, the
outside can be represented by a summary whose update is itself well defined.

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
        |       +-- canonical all-word open quotient
        |       +-- lower bounds from distinguishable completions
        |       +-- dynamic blanket upper bounds
        |       +-- finite counterfactual horizon when a finite blanket exists
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

## The lower-bound side

The observation-window witness proves, for every \(m\ge1\),

\[
K_{\mathrm{passive}}=1,
\qquad
K_{\mathrm{open}}=m+1.
\]

The passive window sees only a focal bit. It is compatible with
\(2^m\) exterior completion states for each focal output. A single permitted
boundary probe can expose any one of the hidden completion bits.

The addressable-completion product theorem generalizes this. If

\[
I\times E_1\times\cdots\times E_q
\]

is operationally readable by concrete boundary words, then

\[
K_{\mathrm{open}}
\ge
\log_2|I|+
\sum_j\log_2|E_j|.
\]

The witness is compiled to one fixed local grammar with pairwise messages and
maximum degree three. It therefore does not rely on an unbounded local lookup
table or a high-degree focal node.

## The positive side: dynamic blanket completeness

A finite exterior summary is sufficient only when it is dynamically closed. If
\(q=(\alpha,\beta)\) stores inside and boundary states and both output and every
allowed action update factor through \(q\), then it is an exact open interface:

\[
K_{\mathrm{open}}
\le
\log_2|\operatorname{im}q|
\le
\log_2|I|+\log_2|B|.
\]

For a finite controlled system, the canonical all-word quotient stabilizes after
at most \(|\operatorname{im}q|-1\) counterfactual refinement rounds. Conversely,
the canonical quotient is the coarsest exact extension-stable deterministic
interface.

Combining both directions gives a sharp family-level conclusion. In the binary
addressable-completion family, any exact blanket has at least \(m\) bits:

\[
\log_2|B_m|\ge m.
\]

Hence there is no blanket of size bounded independently of the number of
possible future exterior attachments.

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

1. **Grammar-growth lower bound.** Specify extension grammars for which increasing
   reachable exterior structure forces a non-stabilizing family of blanket sizes.
2. **Regular-language completion theorem.** Extend finite-horizon certification
   from a free finite action alphabet to a declared regular boundary grammar.
3. **Uniform-law criterion.** Separate a safe interface from existence of one
   candidate-independent deterministic macro transition across a family.
4. **Candidate-family bridge.** Learn or retain completion grammars from data only
   after the structural theorem specifies the object that evidence must certify.

A larger coordinate table, an extra provenance format, or a generic statistical
backend is not a new core theorem by itself.

## Boundary

RACH does not claim that every ecosystem has a finite-state representation, that
passive data are useless, or that an arbitrary outside can be exhaustively
simulated. Every statement is conditional on a declared observation window,
action grammar, completion class, horizon, and candidate family.
