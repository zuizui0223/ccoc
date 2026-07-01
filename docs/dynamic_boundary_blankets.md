# Dynamic boundary blankets and finite counterfactual horizons

## The question after the lower bound

The addressable-completion product theorem gives a lower bound: independently
readable exterior completions force open-interface memory. The complementary
question is positive and structural:

> When can the outside be compressed into a finite summary that remains valid
> after every allowed future boundary action?

A static covariate list is insufficient. A summary must be **dynamically
closed**: states with the same summary must have the same current output and
must update to the same next summary under every permitted action.

This document gives an exact answer in deterministic controlled systems. The
result is a standard quotient principle stated here as the positive side of the
RACH inside/outside program; no claim of novelty for the automata-theoretic core
is made.

## Controlled output systems

Let

\[
\mathcal M=(S,A,T,h)
\]

be a deterministic controlled output system, with state space \(S\), action
alphabet \(A\), transition map

\[
T:S\times A\to S,
\]

and observation-window output \(h:S\to Y\). For a finite action word
\(w=a_1\cdots a_t\), write

\[
\operatorname{Tr}(s,w)
=
\bigl(h(s),h(T(s,a_1)),\ldots,h(T^w(s))\bigr).
\]

The action alphabet is the declared counterfactual boundary grammar. It may
contain passive actions, external arrivals, reconnections, disturbances, or any
other intervention explicitly admitted by the theorem domain.

For horizon \(t\ge0\), define

\[
s\equiv_t s'
\iff
\forall w\in A^{\le t},
\quad
\operatorname{Tr}(s,w)=\operatorname{Tr}(s',w).
\]

Let \(P_t=S/\equiv_t\). The all-counterfactual equivalence is

\[
s\equiv_\infty s'
\iff
\forall w\in A^*,
\quad
\operatorname{Tr}(s,w)=\operatorname{Tr}(s',w),
\]

and its exact interface memory is

\[
K_{\mathrm{open}}
=
\log_2|S/\equiv_\infty|.
\]

## Theorem 1 — Finite counterfactual-horizon stabilization

If \(|S|=N<\infty\), then

\[
\boxed{
P_{N-1}=P_\infty.
}
\]

Equivalently, every exact open distinction in a finite controlled system is
witnessed by an action word of length at most \(N-1\).

### Proof

The horizon partitions refine monotonically:

\[
P_0\preceq P_1\preceq P_2\preceq\cdots.
\]

They obey the recurrence

\[
s\equiv_{t+1}s'
\iff
h(s)=h(s')
\quad\text{and}\quad
T(s,a)\equiv_tT(s',a)
\ \forall a\in A.
\]

If \(P_t=P_{t+1}\), the recurrence implies \(P_{t+1}=P_{t+2}\), and induction
makes the partition stable forever. Before stabilization, every refinement
strictly increases the number of blocks. Starting with at least one and ending
with at most \(N\), there can be at most \(N-1\) strict refinements. Thus
\(P_{N-1}=P_N\), hence \(P_{N-1}=P_\infty\). \(\square\)

This is a finite-grammar result. It does **not** say that an unbounded ecosystem
outside can be enumerated by observing for \(N-1\) time steps; it applies after a
finite controlled state space and action grammar have been declared.

## Theorem 2 — Dynamic-interface completeness

Call a map

\[
q:S\to Q
\]

an exact extension-stable deterministic interface when there are maps

\[
\bar h:Q\to Y,
\qquad
\bar T_a:Q\to Q\quad(a\in A)
\]

such that

\[
h=\bar h\circ q,
\qquad
q(T(s,a))=\bar T_a(q(s))
\quad\forall s\in S,\;a\in A.
\]

Equivalently, whenever \(q(s)=q(s')\),

\[
h(s)=h(s')
\]

and

\[
q(T(s,a))=q(T(s',a))
\quad\forall a\in A.
\]

Then:

\[
\boxed{
S/\equiv_\infty
\text{ is the coarsest exact extension-stable deterministic interface.}
}
\]

For arbitrary (possibly infinite) \(S\), a finite exact open macro-law exists
if and only if \(\equiv_\infty\) has finite index.

### Proof

The equivalence \(\equiv_\infty\) respects current outputs and is a right
congruence: if states agree on all finite words, their successors after any one
action agree on all remaining finite words. Therefore its quotient carries
well-defined output and transition maps.

Conversely, if \(q(s)=q(s')\), the two factorization equations imply by induction
on word length that \(\operatorname{Tr}(s,w)=\operatorname{Tr}(s',w)\) for every
\(w\in A^*\). Thus each fiber of \(q\) lies inside an
\(\equiv_\infty\)-class. Every exact interface therefore refines the canonical
quotient and has at least as many states. \(\square\)

The condition is deliberately dynamic. Matching today's output alone, or
matching one-step average responses, does not make a summary an exact open
macro-law.

## Theorem 3 — Dynamic boundary-blanket upper bound

Let

\[
\alpha:S\to I
\]

be an inside summary and

\[
\beta:S\to B
\]

be a boundary summary. Put \(q=(\alpha,\beta)\). Suppose \(q\) is an exact
dynamic interface in the sense of Theorem 2. Then

\[
\boxed{
K_{\mathrm{open}}
\le
\log_2|\operatorname{im}q|
\le
\log_2|I|+\log_2|B|.
}
\]

If \(S\) is finite, the exact open quotient stabilizes by

\[
\boxed{
H_\star
\le
|\operatorname{im}q|-1
\le
|I||B|-1.
}
\]

### Proof

Theorem 2 says that the canonical quotient is no finer than any dynamic
interface. Hence

\[
|S/\equiv_\infty|
\le
|\operatorname{im}q|
\le |I||B|.
\]

The same cardinality bound limits how many strict horizon refinements can occur:
every \(P_t\) is no finer than the sound interface \(q\), so there can be at
most \(|\operatorname{im}q|-1\) strict refinements before stabilization.
\(\square\)

This gives the rigorous version of “the outside has a finite causal blanket.”
The blanket is not merely a list of external measurements. It is a state summary
whose action-conditioned update is sufficient for all permitted future window
traces.

## Theorem 4 — Uniform blanket obstruction

Suppose the addressable-completion product lower bound contains

\[
I\times E_1\times\cdots\times E_q
\]

and the inside coordinate has \(|I|\) values. Any dynamic blanket \(B\) used
alongside that inside coordinate must satisfy

\[
|I||B|
\ge
|I|\prod_{j=1}^q|E_j|.
\]

Therefore

\[
\boxed{
|B|
\ge
\prod_{j=1}^q|E_j|,
\qquad
\log_2|B|
\ge
\sum_{j=1}^q\log_2|E_j|.
}
\]

### Binary consequence

For \(|E_j|=2\),

\[
\boxed{
\log_2|B|\ge q.
}
\]

Thus the relay-tree / addressable-completion family admits no boundary blanket
of size bounded independently of \(q\). A finite blanket may exist for every
fixed \(q\), but its required memory grows at least linearly in bits and
exponentially in states.

This is the positive theorem turned into a no-go corollary:

\[
\text{finite blanket for each fixed closed scale}
\not\Rightarrow
\text{one uniformly finite blanket across open extension scales}.
\]

## Executable certificates

`causal_model.dynamic_boundary_blankets` provides:

- `FiniteHorizonStabilizationCertificate`, which checks the refinement sequence
  through its first stable horizon;
- `DynamicInterfaceCertificate`, which checks output preservation and
  action-by-action summary closure;
- `DynamicBoundaryBlanketCertificate`, which establishes the memory and horizon
  upper bounds for an inside-plus-boundary pair; and
- `UniformBlanketObstructionCertificate`, which combines the product lower bound
  with the blanket upper bound.

Two canonical finite systems make the boundaries visible.

### Delay chain

A one-action chain with \(N\) states has a terminal output signal. Its exact
counterfactual horizon is \(N-2\), showing that the \(O(N)\) horizon bound is
not a cosmetic artifact.

### Redundant-boundary system

An eight-state system consists of an inside bit, a boundary bit, and a redundant
bit. The pair \((\text{inside},\text{boundary})\) is a four-state dynamic
blanket, whereas the inside bit alone is rejected because a boundary-reading
action sends equal-inside states to different future inside values.

## Ecological projection

An observation plot may have a small exact open law only if the exterior's
future influence can be stored in a finite summary that updates correctly under
all declared events: dispersal, reconnection, seasonal change, disturbance, or
species addition.

The theorem does not state that such a summary exists in a real ecosystem. It
separates two logically different claims:

1. an external variable set predicts current observations; and
2. an external boundary state is dynamically sufficient for all allowed future
   counterfactual responses.

Only the second is a closure certificate for an open ecological law. The
addressable-completion lower bound then says when no **uniformly bounded** such
certificate can survive an expanding family of possible exterior connections.
