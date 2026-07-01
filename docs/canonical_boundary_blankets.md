# Canonical boundary blankets and grammar stabilization

## The question

A finite boundary blanket is not the assertion that an observed window has no
outside. It is the assertion that every admissible outside completion can be
replaced, for the purposes of the declared window response grammar, by one of
finitely many boundary response types.

The existing sufficient-factorization statement says:

\[
\text{inside state} + \text{a declared finite boundary summary}
\Longrightarrow
\text{a finite response-sufficient interface}.
\]

This document gives the converse canonical object: the smallest exact boundary
summary itself.

## Setup

Let

\[
I
\]

be window states, \(E\) exterior completions, \(\Gamma\) a grammar of allowed
boundary words, and

\[
R(i,e,w)
\]

the deterministic response observed in the window. No geometry is built into the
definition. Spatial exterior, delayed seasonal state, a rare immigrant source,
and an unmeasured variable inside the sampled area can all be part of \(E\).
Geometry and monitoring scope determine \(\Gamma\).

Define exterior response equivalence by

\[
e\equiv_\Gamma e'
\quad\Longleftrightarrow\quad
\forall i\in I,\ \forall w\in\Gamma,
\ R(i,e,w)=R(i,e',w).
\]

The **canonical boundary blanket** is

\[
B_\Gamma=E/\!\equiv_\Gamma,
\]

with quotient map \(q_\Gamma:E\to B_\Gamma\).

## Theorem 1 — Canonical minimal blanket

The map \(q_\Gamma\) is response-sound: there is a unique induced law

\[
\bar R(i,q_\Gamma(e),w)=R(i,e,w).
\]

Let \(\beta:E\to B\) be any other exact exterior summary, meaning that there
exists a response law \(\widetilde R\) such that

\[
R(i,e,w)=\widetilde R(i,\beta(e),w)
\]

for all \(i,e,w\). Then there is a unique map

\[
f:\operatorname{im}(\beta)\to B_\Gamma
\]

such that

\[
\boxed{
q_\Gamma=f\circ\beta.
}
\]

Consequently,

\[
\boxed{
|\operatorname{im}(\beta)|\ge |B_\Gamma|.
}
\]

So \(B_\Gamma\) is, up to relabelling, the unique coarsest and
minimum-cardinality exact exterior summary.

### Proof

If \(\beta(e)=\beta(e')\), exact factorization gives

\[
R(i,e,w)=\widetilde R(i,\beta(e),w)
=\widetilde R(i,\beta(e'),w)
=R(i,e',w)
\]

for every \(i,w\). Hence \(e\equiv_\Gamma e'\). Therefore the canonical class
of \(e\) depends only on \(\beta(e)\), which defines \(f\). Surjectivity of
\(q_\Gamma\) gives uniqueness. Since a map from \(\operatorname{im}(\beta)\)
onto \(B_\Gamma\) exists, the cardinality inequality follows. \(\square\)

This is a response-quotient theorem, analogous in logical form to a
Myhill–Nerode minimality argument. It is not a claim that the construction is
novel relative to automata minimization; the RACH contribution is its boundary
interpretation and use in open-system compression.

## Theorem 2 — Window interface bound

The map

\[
(i,e)\mapsto (i,q_\Gamma(e))
\]

is response-sufficient. Thus, for finite \(I\) and finite \(B_\Gamma\),

\[
\boxed{
K_\Gamma^{\mathrm{window}}
\le
\log_2|I|+\log_2|B_\Gamma|.
}
\]

Equality requires a separate **joint-observability** condition:

\[
\forall (i,b)\ne(i',b'),\ \exists w\in\Gamma
\quad
\bar R(i,b,w)\ne\bar R(i',b',w).
\]

Under that condition, every unequal inside-plus-blanket cell has a concrete
separating word, so

\[
\boxed{
K_\Gamma^{\mathrm{window}}
=
\log_2|I|+\log_2|B_\Gamma|.
}
\]

Without joint observability the displayed expression is only an upper bound.
This distinction matters: a finite blanket can be minimal for the exterior even
when some inside states are observationally redundant under the same grammar.

## Theorem 3 — Grammar refinement and stabilization

Let

\[
\Gamma_0\subseteq\Gamma_1\subseteq\cdots,
\qquad
\Gamma_\infty=\bigcup_{n\ge0}\Gamma_n.
\]

Then exterior equivalence can only refine:

\[
e\equiv_{\Gamma_{n+1}}e'
\Longrightarrow
 e\equiv_{\Gamma_n}e'.
\]

Hence canonical blanket sizes are monotone:

\[
|B_{\Gamma_0}|
\le |B_{\Gamma_1}|
\le\cdots
\le |B_{\Gamma_\infty}|.
\]

The exact criterion is

\[
\boxed{
B_{\Gamma_\infty}\text{ is finite}
\quad\Longleftrightarrow\quad
\sup_n |B_{\Gamma_n}|<\infty.
}
\]

When the equivalent conditions hold, there is an \(N\) such that

\[
\boxed{
\equiv_{\Gamma_n}=\equiv_{\Gamma_\infty}
\quad\text{for every } n\ge N.
}
\]

### Proof

A finite blanket for \(\Gamma_\infty\) bounds every earlier quotient, proving
one direction. Conversely, if the nondecreasing integer sequence
\(|B_{\Gamma_n}|\) is bounded, it is eventually constant. A proper refinement of
a finite partition strictly increases its block count, so the partitions
therefore become identical from some \(N\) onward. Every word in
\(\Gamma_\infty\) lies in some finite grammar level, so equivalence for the
stable partition is exactly equivalence for the union. \(\square\)

The result is semantic. Observing a finite run of stable empirical data does not
establish that the real admissible grammar has stabilized.

## Theorem 4 — Unbounded addressability prevents finite closure

Take

\[
E=\{0,1\}^{\mathbb N}
\]

and let \(\Gamma_n\) contain readouts of the first \(n\) binary exterior
coordinates. Then two completions are equivalent at level \(n\) exactly when
their first \(n\) coordinates agree, so

\[
\boxed{|B_{\Gamma_n}|=2^n.}
\]

The quotients are unbounded. By Theorem 3, no finite exact blanket exists for
\(\Gamma_\infty\).

This is the infinite counterpart to the finite addressable-completion product
lower bound. Each extra readable exterior coordinate is not merely another
variable: it forces a new independent boundary response distinction.

## Executable finite certificates

`causal_model.canonical_boundary_blankets` provides a finite deterministic
response-table abstraction and certificates for:

- the canonical exterior response quotient;
- factorization of a supplied sound summary through that quotient;
- joint observability, which distinguishes equality from upper-bound-only;
- monotone refinement across a declared finite grammar chain; and
- two contrasting examples.

The first example has four raw exterior completions but only two response types,
so its canonical blanket compresses \(4\to2\). The second is a finite binary
addressable ladder with exact counts

\[
1,2,4,\ldots,2^m.
\]

These finite checks are certificate replay. They demonstrate the finite cases of
the proofs; they do not prove an unlisted infinite continuation.

## Ecological projection

For a monitoring window, a finite portable open law exists only relative to a
declared family of admissible boundary interventions, dispersal channels, time
horizons, and hidden variables. It exists exactly when those exterior
possibilities collapse into finitely many response-equivalent boundary regimes.

\[
\boxed{
\text{Closure is not absence of outside.}
\quad
\text{It is finiteness of the minimal response-sufficient outside summary.}
}
\]

A growing list of newly addressable rare colonists, delayed mutualists, climate
modes, or source populations need not permit such a summary. Conversely, many
physical outside states may be safely collapsed when they induce the same window
responses under the stated grammar.