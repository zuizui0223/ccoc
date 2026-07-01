# Candidate-safe laws, universal laws, and ensemble--instance separation

## The distinction that matters

A retained candidate family can support a small exact law **inside every
candidate** while failing to support one deterministic law after the candidate
mechanism is forgotten.

These are different mathematical objects:

1. an **instance law**, valid after a candidate is fixed;
2. a **universal deterministic law**, valid for every retained candidate without
   recording which one is active;
3. a **candidate-safe deterministic law**, valid after the response type is
   retained as part of state; and
4. a **set-valued law**, the exact prediction after candidate identity is
   forgotten when deterministic agreement is absent.

The point is not that uncertainty is vaguely inconvenient. It is that distinct
retained mechanisms can impose different future macro transitions at the same
observable macrostate.

## Candidate-induced macro-laws

Let \(C\) be a finite retained candidate family. Assume every candidate has
already been reduced to the same observable macrostate space \(Q\), with
injective macro output map \(o:Q\to Y\). Candidate \(\theta\) induces, for
each declared action \(a\in A\), a deterministic macro transition

\[
G_a^\theta:Q\to Q.
\]

The assumption that each candidate has an exact instance law is precisely that
these maps are well defined. The question here is whether the maps agree across
candidates.

Define response-type equivalence by

\[
\theta\sim_{\mathrm{resp}}\theta'
\iff
G_a^\theta=G_a^{\theta'}
\quad\forall a\in A.
\]

Let

\[
R=|C/\sim_{\mathrm{resp}}|
\]

be the number of distinct induced response types. Duplicate candidates with the
same induced macro dynamics count once; this is a response distinction, not a
model-name distinction.

## Theorem 1 — Universal deterministic macro-law criterion

A candidate-independent deterministic macro-law

\[
G_a:Q\to Q
\]

exists for every action \(a\in A\) if and only if

\[
\boxed{
G_a^\theta=G_a^{\theta'}
\quad
\forall\theta,\theta'\in C,\ \forall a\in A.
}
\]

Equivalently,

\[
\boxed{R=1.}
\]

### Proof

If a universal map \(G_a\) exists, its defining candidate-independence gives

\[
G_a^\theta(q)=G_a(q)=G_a^{\theta'}(q)
\]

for every \(q\), action, and candidate pair. Thus all induced maps agree.

Conversely, if all induced maps agree, define \(G_a\) to be their common map.
It is candidate independent by construction. \(\square\)

The criterion is stronger than equality of interface size. Two candidates may
both need only one macro bit yet assign different transitions to that same bit.

## Theorem 2 — Ensemble--instance separation

There is a two-candidate family with

\[
Q=\{0,1\},
\qquad
K_{\mathrm{instance}}(\theta)=1
\quad\forall\theta\in C,
\]

but no universal deterministic macro-law on \(Q\).

Take a passive action that preserves \(q\) in both candidates and an
intervention \(a\) with

\[
G_a^{(0)}(q)=q,
\qquad
G_a^{(1)}(q)=1-q.
\]

Both candidates have an exact one-bit instance law. Yet at either macrostate,

\[
G_a^{(0)}(q)\ne G_a^{(1)}(q).
\]

By Theorem 1, no candidate-forgetting deterministic law exists.

\[
\boxed{
\text{small exact law per candidate}
\not\Rightarrow
\text{universal deterministic law across candidates.}
}
\]

This obstruction is independent of the outside-memory lower bound. Here the
state requirement of every individual mechanism is already minimal; what fails
is agreement of the induced transition law.

## Set-valued law: the exact candidate-forgetting object

Without recording the response type, the exact one-step prediction is

\[
F_a(q)
=
\{G_a^\theta(q):\theta\in C\}.
\]

This is a set-valued macro-law. It is singleton-valued for every \(q,a\) if and
only if \(R=1\), equivalently if and only if a universal deterministic law
exists.

Thus RACH has a precise output rule:

\[
\begin{array}{rcl}
R=1
&\Longrightarrow&
\text{report a universal deterministic law},\\[4pt]
R>1\ \text{and type retained}
&\Longrightarrow&
\text{report a candidate-safe deterministic law},\\[4pt]
R>1\ \text{and type forgotten}
&\Longrightarrow&
\text{report a set-valued law or \texttt{UNRESOLVED}.}
\end{array}
\]

## Uniform response separation

The number \(R\) alone does not always force a full product lower bound. Two
response types may differ only from some macrostates and not others. The exact
multiplicative theorem requires the following operational condition.

For every pair of distinct response types \(r\ne r'\) and every macrostate
\(q\in Q\), there is a declared future action word \(w_{r,r',q}\in A^*\)
such that

\[
\operatorname{Tr}_r(q,w_{r,r',q})
\ne
\operatorname{Tr}_{r'}(q,w_{r,r',q}).
\]

Call this **uniform response separation**. The words may differ across pairs and
macrostates. What matters is that each candidate type is operationally
addressable from every shared macrostate.

## Theorem 3 — Candidate-safe product lower bound

Assume uniform response separation. Then any exact deterministic interface that
both retains the observable macrostate and predicts every declared future action
must have at least

\[
\boxed{
|Q|R
}
\]

states. Equivalently,

\[
\boxed{
K_{\mathrm{candidate\text{-}safe}}
\ge
\log_2|Q|+\log_2R.
}
\]

### Proof

Consider augmented states \((q,r)\in Q\times\{1,\ldots,R\}\).

- If \(q\ne q'\), the injective current macro output separates
  \((q,r)\) from \((q',r')\).
- If \(q=q'\) but \(r\ne r'\), the word \(w_{r,r',q}\) separates the two
  states by uniform response separation.

Therefore every distinct pair in \(Q\times\{1,\ldots,R\}\) has a concrete
future trace separator. The map into the exact candidate-safe trace quotient is
injective, so the quotient has at least \(|Q|R\) classes. Taking base-two
logarithms gives the result. \(\square\)

The candidate-safe deterministic construction attains this bound in the
canonical family: store the pair \((q,r)\), keep \(r\) fixed, and update

\[
(q,r)
\xrightarrow{a}
\bigl(G_a^r(q),r\bigr).
\]

## Delayed candidate discrimination

The preceding obstruction can remain hidden for an arbitrarily long legal
horizon. Let the boundary grammar allow only

\[
\epsilon,
\mathrm{wait},
\ldots,
\mathrm{wait}^{H},
\mathrm{wait}^{H}\mathrm{fire}.
\]

Use two candidates with

\[
G_{\mathrm{wait}}^{(0)}=G_{\mathrm{wait}}^{(1)}=\mathrm{id},
\]

and

\[
G_{\mathrm{fire}}^{(0)}=\mathrm{id},
\qquad
G_{\mathrm{fire}}^{(1)}=\mathrm{flip}.
\]

Then for every \(t\le H\), every legal word of length at most \(t\) has the
same trace in the two candidates. The legal word

\[
\mathrm{wait}^{H}\mathrm{fire}
\]

separates them.

\[
\boxed{
\text{No fixed finite-horizon procedure resolves candidate response type}
\text{ uniformly over the delayed family.}
}
\]

This is a different statement from the open/closed no-go in the delayed
addressability theorem. There, the unknown object is whether a completion can
affect the window. Here, every candidate has a small instance law, but the
unknown object is **which induced macro transition law is correct**.

## Executable certificates

`causal_model.candidate_safe_laws` supplies:

- `UniversalMacroLawCertificate`, proving all retained induced maps agree;
- `UniversalLawObstructionCertificate`, a one-step disagreement witness;
- `SetValuedMacroLawCertificate`, the exact candidate-forgetting prediction;
- `CandidateResponseSeparationCertificate`, a concrete future word separating
  two response types at one macrostate;
- `CandidateSafeProductCertificate`, which verifies the uniform-separation
  premise and exact \(|Q|R\) quotient in a finite family; and
- `DelayedCandidateDiscriminationCertificate`, which composes response-type
  disagreement with a delayed prefix grammar.

The certificate replay validates finite witnesses and implementation invariants.
The proofs above establish the stated theorem schemas; replay is not simulation
evidence.

## Ecological projection

Two retained ecological mechanisms may generate the same currently observed
community pattern and each may have a compact mechanism-specific model. They can
still disagree on the macro response to a disturbance, colonist arrival,
corridor opening, pathogen exposure, or phenological transition.

A universal ecological law requires both:

1. an adequate dynamic boundary blanket for each mechanism; and
2. candidate-invariant induced macro dynamics.

Without the second condition, the mathematically honest conclusion is not one
universal deterministic law. It is a candidate-safe law that retains mechanism
type, a set-valued forecast, or `UNRESOLVED`.
