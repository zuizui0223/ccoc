# Delayed addressability and no uniform closure horizon

## The question after dynamic blankets

A fixed finite controlled grammar has an exact finite counterfactual horizon:
its all-word quotient eventually stabilizes. That statement does **not** give a
single observation or intervention horizon that works uniformly across a family
whose outside becomes addressable only after later and later declared events.

This document makes the missing distinction exact:

\[
\boxed{
\text{finite certificate for every fixed system}
\not\Rightarrow
\text{one finite certificate for every system in an expanding outside family.}
}
\]

The construction has two independent parameters:

- \(m\), the number of independently addressable exterior binary completions;
  and
- \(H\), the number of legal protocol steps before an exterior completion can
  first affect the observation window.

Thus memory burden and counterfactual delay are separate axes.

## Prefix-closed boundary grammars

Let

\[
\mathcal M=(S,A,T,h)
\]

be a finite deterministic controlled output system and let

\[
\mathcal G=(G,g_0,\delta)
\]

be a deterministic **partial** automaton over the same action alphabet. A word
is legal exactly when every transition of \(\delta\) exists. Since every reached
grammar state remains legal, the language is prefix closed.

The grammar is part of the boundary contract. It does not inject an outside
value into the focal system; it says which interventions or boundary events are
currently permitted.

For an augmented state \((s,g)\), define grammar-aware finite-horizon
trace-equivalence by

\[
(s,g)\equiv_t(s',g')
\iff
\forall w\in L_g\cap A^{\le t},
\quad
\operatorname{Tr}(s,w)=\operatorname{Tr}(s',w),
\]

with the usual recursive interpretation that the allowed continuations are
those accepted from the current grammar state. The initial-window quotient uses
\(g=g'=g_0\).

## Theorem 1 — Grammar-aware finite-horizon stabilization

For a finite system with \(|S|=N\) and a finite grammar with \(|G|=R\), the
all-word quotient on the augmented product stabilizes by

\[
\boxed{
P_{NR-1}=P_\infty.
}
\]

### Proof

The grammar-aware refinement recurrence is

\[
(s,g)\equiv_{t+1}(s',g')
\iff
h(s)=h(s')
\quad\text{and}\quad
\forall a\in\operatorname{Legal}(g),
\quad
\bigl(T(s,a),\delta(g,a)\bigr)
\equiv_t
\bigl(T(s',a),\delta(g',a)\bigr),
\]

with the enabled-action structure included in the comparison. The induced
partitions of \(S\times G\) refine monotonically. If two consecutive partitions
are equal, the recurrence forces every later partition to be equal. Before
stabilization, the number of blocks strictly increases. There are at most
\(NR\) product states, hence at most \(NR-1\) strict refinements. \(\square\)

This is a controlled finite-state quotient theorem. It is not a statement that
one can exhaust an arbitrary empirical outside.

## Delayed reader grammar

For any \(H\ge0\), take one constant local action alphabet

\[
A=\{\mathrm{wait},\mathrm{fire}\}.
\]

The grammar states are

\[
g_0,g_1,\ldots,g_H,g_\bot.
\]

The only legal transitions are

\[
g_r\xrightarrow{\mathrm{wait}}g_{r+1}
\quad(0\le r<H),
\]

and

\[
g_H\xrightarrow{\mathrm{fire}}g_\bot.
\]

Therefore the legal words from \(g_0\) are exactly

\[
\epsilon,
\mathrm{wait},
\ldots,
\mathrm{wait}^H,
\mathrm{wait}^H\mathrm{fire}.
\]

There is no legal `fire` before depth \(H\). The unique revealing word is

\[
r_H=\mathrm{wait}^H\mathrm{fire},
\qquad |r_H|=H+1.
\]

## Structural port contexts

The coordinate state is

\[
x=(y,b_1,\ldots,b_m)\in\{0,1\}^{m+1}.
\]

A fixed closed context \(E_i\) physically attaches its reader to leaf \(i\).
This attachment, not an action token, chooses the exterior module. The same
local grammar is used in every context:

\[
(y,b_1,\ldots,b_m)
\xrightarrow{\mathrm{wait}}
(y,b_1,\ldots,b_m),
\]

while the only permitted `fire` occurs after the delay and maps

\[
(y,b_1,\ldots,b_m)
\xrightarrow{\mathrm{fire}\text{ in }E_i}
(b_i,b_1,\ldots,b_m).
\]

The declared open family is the collection of all structural attachments

\[
\mathcal E_m=\{E_1,\ldots,E_m\}.
\]

Its safe interface is the common refinement of the exact interfaces in every
allowed attachment context.

## Theorem 2 — Delayed addressability rectangle

For every \(m\ge1\) and \(H\ge0\), the delayed family satisfies

\[
\boxed{
K_{\mathrm{open}}=m+1,
\qquad
\max_iK_{\mathrm{closed},i}=2,
\qquad
H_\star=H+1.
}
\]

Here \(H_\star\) is the first horizon at which the robust open quotient reaches
its final partition.

More explicitly, for every \(0\le t\le H\),

\[
|Q_{\mathrm{open},t}|=2,
\]

because every legal word through horizon \(t\) consists only of waits and hence
observes only \(y\). At horizon \(H+1\), the context \(E_i\) separates any two
states differing in \(b_i\), using \(r_H\). Taking the common refinement over
all \(i\) separates every coordinate state:

\[
|Q_{\mathrm{open},H+1}|=2^{m+1}.
\]

The fixed context \(E_i\) sees only \((y,b_i)\), so

\[
|Q_{E_i,H+1}|=4.
\]

Taking base-two logarithms gives the claimed interface memories. Since the
partition has two blocks at horizon \(H\), becomes discrete at \(H+1\), and the
grammar then has no continuations, the first stabilization horizon is exactly
\(H+1\). \(\square\)

This is a rectangle in two independent lower-bound directions:

\[
\text{open memory inflation}=m,
\qquad
\text{delayed distinguishability}=H+1.
\]

Neither parameter is a consequence of the other.

## Corollary — No uniform finite closure horizon

For every proposed finite horizon \(H\), there is a closed model family and an
open model family that agree on every legal trace through horizon \(H\), but
differ on the legal word

\[
\mathrm{wait}^H\mathrm{fire}.
\]

### Construction

Use the same state space and grammar in both models. In the open model,
`fire` in context \(E_i\) sets the focal output to \(b_i\). In the closed
comparator, `fire` leaves the focal output unchanged.

Every legal word through horizon \(H\) contains no `fire`, so the two models
have identical traces for every initial state. Choose a state with \(y=0\) and
\(b_i=1\). The legal word of length \(H+1\) yields focal output \(1\) in the
open model and \(0\) in the closed model.

Consequently, any rule that sees only all legal traces up to a fixed finite
horizon receives identical information from these two models and therefore must
make the same closure decision for both. It is wrong for at least one.

\[
\boxed{
\text{No fixed finite-horizon trace procedure certifies closure uniformly over}
\quad\{M_{m,H}:H\ge0\}.
}
\]

This does not contradict finite stabilization for each fixed family member. The
required horizon is finite for each \(H\), but unbounded over the union.

## Bounded-degree structural realization

The reader attachment is compiled using the existing relay-tree construction:

- the reader attaches to one leaf selected by the fixed context;
- each leaf-to-root path uses only pairwise child-to-parent messages;
- maximum degree remains three, including the reader; and
- the local node/message grammar is unchanged as \(m\) grows.

A `wait` is a quiescent microtick with no reader firing. After \(H\) waits, the
same one-token `fire` protocol already certified by the relay-tree module
propagates the attached leaf's permanent bit to the root.

This establishes that port selection is structural rather than a growing action
alphabet. The **delay gate itself** is represented here by the explicit boundary
grammar automaton. The present theorem does not claim an autonomous local-clock
implementation of every possible delay mechanism; that would be a separate
strengthening.

## Executable certificates

`causal_model.delayed_addressability` contains:

- `FinitePrefixGrammar` and `GrammarAwareControlledSystem` for exact
  grammar-constrained quotients;
- `GrammarHorizonStabilizationCertificate` for the \(|S||G|-1\) upper bound;
- `DelayedSeparatingWordCertificate` for the concrete delayed word exposing one
  exterior coordinate;
- `DelayedAddressabilityCertificate` for the exact
  \((K_{\mathrm{closed}},K_{\mathrm{open}},H_\star)=(2,m+1,H+1)\) family;
- `DelayedClosureNonidentifiabilityCertificate` for the closed/open prefix pair;
  and
- `DelayedRelayAttachmentCertificate` for the degree-three structural reader
  realization.

The certificate replay workflow checks these finite objects over a declared
finite range. The proofs above establish the all-\(m\), all-\(H\) statements.

## Ecological projection

The theorem does not assert that real ecosystems contain arbitrary hidden delayed
causes. It states what follows **if** the declared outside grammar permits a
later event but rules it out before a delay: a short observation window cannot
use its earlier irrelevance as a closure certificate.

Phenological gates, seasonal corridors, post-disturbance colonization, delayed
pathogen emergence, seed-bank recruitment, and return intervals are possible
ways an ecological grammar may delay an exterior interaction. The relevant
question is not whether the outside was visible before the delay, but whether it
is a legal future continuation of the system's stated boundary contract.
