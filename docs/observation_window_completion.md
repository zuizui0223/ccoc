# Observation-window completion and counterfactual interface inflation

## The object is a window, not a patch

The mathematical object is a finite **observation window**: a declared set of
visible variables, spatial extent, temporal horizon, and allowed observation
actions. A habitat patch, field plot, camera view, island survey, or monitoring
range can instantiate a window, but none of those is the definition.

The complement of the window is represented by a declared **completion grammar**:
which hidden external modules, boundary inputs, attachments, or future actions
are allowed to influence the window.

A system is therefore not called closed merely because no external effect was
seen. It is closed only relative to a declared completion grammar when changing
an admissible exterior completion cannot change the future window trace.

## Finite witness domain

For each \(m\ge1\), the global state is

\[
x=(y,b_1,\ldots,b_m)\in\{0,1\}^{m+1}.
\]

The observation window sees only the focal output

\[
Y_W(x)=y.
\]

The bits \(b_i\) are exterior completion memory: they are not visible under the
passive observation grammar

\[
\mathcal P=\{\mathrm{observe},\mathrm{idle}\}.
\]

Both passive actions leave the global state unchanged. The declared open
counterfactual grammar adds one sequential boundary action per exterior module,

\[
\mathcal G_m
=
\mathcal P\cup
\{\mathrm{probe}:1,\ldots,\mathrm{probe}:m\},
\]

where

\[
(y,b_1,\ldots,b_m)
\xrightarrow{\mathrm{probe}:i}
(b_i,b_1,\ldots,b_m).
\]

This is a finite deterministic theorem domain, not a generic empirical
assumption about ecosystems.

## Controlled trace equivalence

For an action grammar \(\mathcal A\), define

\[
x\equiv_{\mathcal A}x'
\iff
\forall w\in\mathcal A^*,
\quad
\operatorname{Tr}(x,w)=\operatorname{Tr}(x',w),
\]

where \(\operatorname{Tr}\) is the focal-output trace induced by the action
word. The minimal causal interface memory for the grammar is

\[
K_{\mathcal A}
=
\log_2\left|X_m/\equiv_{\mathcal A}\right|.
\]

The grammar is part of the theorem statement. Enlarging it asks a stronger
counterfactual question.

## Theorem 1: finite passive observation does not certify closure

For every \(m\ge1\), every finite passive word
\(p\in\mathcal P^*\), every focal value \(y\in\{0,1\}\), and every port
\(i\), there are two distinct global completions \(x,x'\) such that

\[
\operatorname{Tr}(x,p)=\operatorname{Tr}(x',p),
\]

but

\[
\operatorname{Tr}(x,\mathrm{probe}:i)
\ne
\operatorname{Tr}(x',\mathrm{probe}:i).
\]

### Proof

Take

\[
x=(y,0,\ldots,0),
\]

and let \(x'\) equal \(x\) except that \(b_i'=1\). Every action in
\(\mathcal P\) is state preserving, so both passive traces are the constant
trace \((y,\ldots,y)\), for any finite length. The `probe:i` action changes
the focal output to \(0\) in \(x\) and to \(1\) in \(x'\). \(\square\)

This proves an **existence no-go**: in a model class containing this fixed
finite grammar, passive window traces alone cannot rule out all exterior
completions relevant to a declared future boundary action. It does not claim
that no observation protocol can ever establish closure under stronger
assumptions.

## Theorem 2: strict counterfactual interface inflation

For the passive grammar,

\[
K_{\mathcal P}=1.
\]

For the open grammar,

\[
K_{\mathcal G_m}=m+1.
\]

Hence

\[
\boxed{
K_{\mathcal G_m}-K_{\mathcal P}=m.
}
\]

### Proof

Under \(\mathcal P\), all states with the same \(y\) have identical future
traces, while \(y=0\) and \(y=1\) are separated by current observation. The
passive quotient therefore has two blocks.

Under \(\mathcal G_m\), two states that differ in \(y\) are separated by
`observe`. If they have equal \(y\) but differ in any \(b_i\), `probe:i`
separates them. Thus every global state is a distinct open trace-equivalence
class. \(\square\)

The pre-existing extension--compression theorem is recovered by comparing the
open grammar with a fixed context that permits only one probe. The present
version instead compares a passive observation window with its external
counterfactual completions.

## Theorem 3: counterfactual refinement monotonicity

For any deterministic controlled system and grammars

\[
\mathcal A_1\subseteq\mathcal A_2,
\]

one has

\[
\boxed{
K_{\mathcal A_1}\le K_{\mathcal A_2}.
}
\]

### Proof

Equivalence under \(\mathcal A_2\) requires equality of traces for every word
allowed by \(\mathcal A_2\), including every word allowed by
\(\mathcal A_1\). Hence

\[
\equiv_{\mathcal A_2}\subseteq\equiv_{\mathcal A_1}.
\]

The \(\mathcal A_2\) quotient is therefore a refinement of the
\(\mathcal A_1\) quotient and cannot have fewer blocks. \(\square\)

This inequality is simple but useful: increasing the range of admissible
counterfactual ecosystem-outside events cannot make a safe causal interface
smaller.

## Bounded-degree realization

The coordinate witness is compiled by
[`relay_tree_compilation.py`](../causal_model/relay_tree_compilation.py) to a
network with:

- one fixed finite node/message grammar;
- edge-local pairwise child-to-parent messages;
- maximum degree three, including one attached reader; and
- sequential quiescent macro-time.

The root is the observation window. The memory leaves are exterior completion
modules. In the absence of reader firing, different leaf memories generate the
same root trace for arbitrarily many passive microticks. A reader firing at one
leaf produces a distinct future root output when that exterior bit differs.
Thus Theorems 1 and 2 do not rely on a direct high-degree read of all external
memory.

## Positive counterpart: the boundary-memory upper bound

A no-go theorem is not a claim that useful laws never exist. Let \(I\) be an
inside interface with \(|I|\) states and let \(B\) be a finite controlled
boundary summary with \(|B|\) states. Suppose that every admissible exterior
completion influences every future window trace only through the evolving state
of \(B\). Then the product interface \((I,B)\) is sufficient, giving

\[
\boxed{
K_{\mathrm{open}}
\le
\log_2|I|+\log_2|B|.
}
\]

This is a direct constructive factorization lemma: if the exterior has a finite
sufficient causal blanket, store that blanket together with the inside
interface. The important open research task is to identify nontrivial classes
where such a blanket can be proved to exist, rather than assumed.

## Research hypotheses

The following are deliberately separated by status.

### H1 — proved in this module

A finite passive observation window can remain compatible with distinct
completion worlds that diverge under an allowed future boundary action.

### H2 — proved generally

Expanding the counterfactual action grammar cannot decrease minimal safe
interface memory.

### H3 — next lower-bound schema

If a completion grammar contains \(q\) independently addressable exterior
modules with \(r_i\) distinguishable responses, then, under an explicit product
independence condition,

\[
K_{\mathrm{open}}
\ge
K_{\mathrm{passive}}+
\sum_{i=1}^{q}\log_2 r_i.
\]

The binary relay witness realizes the special case \(r_i=2\). A general theorem
needs a definition of independence that does not merely restate partition size.

### H4 — stabilization / blanket conjecture

For a nested family of completion grammars
\(\Gamma_1\subseteq\Gamma_2\subseteq\cdots\), determine conditions under
which \(K_{\Gamma_n}\) eventually stabilizes. A finite dynamically sufficient
boundary blanket is a natural sufficient condition; necessity needs careful
formulation.

### H5 — ecological projection

A plot, island, survey extent, or monitoring period is an observation window.
Dispersal sources, rare colonists, delayed mutualists, pathogens, nutrient
inflow, and adjacent communities are possible exterior completions. The theorem
would classify an observed ecological rule as either:

- a rule certified under a specified completion grammar; or
- an internal, observation-window-conditioned rule whose open validity remains
  unresolved.

Patch geometry, edge length, corridors, and fragmentation can later enter by
changing the completion grammar. They are not the definition of open or closed.

## Executable regression

`causal_model.observation_window_completion` provides:

- `CounterfactualCompletionCertificate` for passive-indistinguishable coordinate
  completions separated by one boundary probe;
- `RelayCompletionCertificate` for the bounded-degree realization; and
- `ObservationWindowCompletionCertificate` for the exact
  \(K_{\mathcal P}=1\), \(K_{\mathcal G_m}=m+1\) family.

The GitHub Actions regression enumerates all passive words through a declared
finite horizon, both focal states, all ports, and all sizes \(m=1,\ldots,6\).
The finite enumeration is a regression certificate; the proofs above establish
the corresponding all-finite-word statements.
