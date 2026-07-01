# Compositional boundedness criteria for open causal interfaces

## What this theorem does—and does not—say

The extension–compression inequality gives a lower bound when newly attachable
modules are independently addressable. Grammar-aware dynamic blankets give a
positive finite factorization for one declared contract. The missing family-level
question is:

\[
\text{When can a finite macro-interface survive growing future composition?}
\]

There is no unconditional two-way classification of arbitrary ecological or
controlled families. This document proves two **conditional structural criteria**:

1. a common finite dynamic blanket gives a uniform interface bound; and
2. cumulative relative addressability gives cumulative interface growth.

A family satisfying neither premise is deliberately left unresolved.

## Setup

Let \(\Gamma_1\subseteq\Gamma_2\subseteq\cdots\) denote increasingly permissive
future boundary grammars or, more generally, increasingly rich composition
stages. Let \(K_m\) be the memory of the exact causal trace quotient at stage
\(m\).

The stage state spaces may grow because new dormant modules become physically
available. The grammar state remains a declared boundary-contract state; it is
not automatically interpreted as a biological variable.

## Positive criterion — Uniform dynamic blanket

Suppose there is one finite summary alphabet

\[
Q,\qquad |Q|<\infty,
\]

and for every stage \(m\) a summary map

\[
q_m:S_m\times G_m\to Q
\]

such that equal summary values preserve:

\[
\text{current output},
\qquad
\text{enabled legal actions},
\qquad
\text{and successor summary under every enabled action}.
\]

Equivalently, each \(q_m\) is a grammar-aware dynamic interface with the same
finite codomain \(Q\).

Then the exact canonical quotient at every stage refines no further than this
summary:

\[
\boxed{
K_m\le\log_2|Q|
\quad\text{for every }m.
}
\]

Hence

\[
\boxed{
\sup_m K_m\le\log_2|Q|.
}
\]

### Proof

At stage \(m\), output/action/successor preservation makes \(q_m\) an exact
grammar-aware dynamic interface. The canonical quotient is coarser than every
exact interface, so it has at most \(|\operatorname{im}q_m|\le|Q|\) blocks.
Taking logarithms and then the supremum yields the claim. \(\square\)

The key is not that module count is bounded. The stage domains may grow without
bound. What matters is that every new module contributes no new future response
type beyond the fixed summary alphabet.

### Positive witness

The executable inert-attachment family has \(2^m\) physical configurations at
stage \(m\), but every action leaves every configuration unchanged and all
window outputs agree. One summary label is exact at every stage:

\[
|S_m|=2^m,
\qquad
K_m=0.
\]

This is intentionally simple. It proves that growing composition *alone* does
not force macro-interface growth.

## Negative criterion — Cumulative relative addressability

At stage \(m\), suppose a jointly realizable reachable subsystem has the form

\[
I\times E_1\times\cdots\times E_m.
\]

Assume a legal base word decodes the inside coordinate and, for each \(j\le m\),
a legal future boundary word decodes the value of \(E_j\) independently of the
other factors. These are **relative operational addressability** assumptions:
the new factor remains jointly realizable with all prior factors and is not
already collapsed by the old quotient.

Then the decoder injection gives

\[
\boxed{
K_m
\ge
\log_2|I|+
\sum_{j=1}^{m}\log_2|E_j|.
}
\]

### Proof

Any two distinct product states differ in the inside coordinate or in at least
one exterior factor. The corresponding legal decoder word separates that pair.
Therefore the trace quotient is discrete on the product subsystem, whose
cardinality is

\[
|I|\prod_{j=1}^{m}|E_j|.
\]

Taking the logarithm proves the lower bound. \(\square\)

For binary modules,

\[
|I|=2,
\qquad |E_j|=2,
\]

this becomes

\[
\boxed{K_m\ge m+1.}
\]

Thus an unbounded sequence of independently future-addressable binary modules
prevents any uniform finite interface bound.

## Sharp realization

The existing bounded-degree relay-tree family attains the binary lower bound at
every prefix stage:

\[
K_m=m+1.
\]

It uses one repeated finite local grammar, pairwise directed messages, and
maximum degree three. Therefore cumulative growth is not an artifact of
higher-order interaction or a growing local rule vocabulary.

## What sits between the criteria

The results are not a universal dichotomy. A family can fail to have a supplied
uniform blanket certificate and also fail the joint-addressability premise—for
example because new modules are partially redundant, only conditionally
realizable, or their legal boundary words do not separate independent factors.

The mathematically honest status in that middle region is

\[
\boxed{\mathrm{UNRESOLVED}}
\]

until a stronger factorization or a stronger decoder/product theorem is proved.

## Ecological reading

Potential source populations, reservoirs, mutualists, corridors, and neighboring
communities do not destroy a portable macro-law merely by existing. They destroy
portability only when each added module introduces a future response distinction
not already compressed by a stable dynamic boundary summary.

\[
\boxed{
\text{new attachment factors through the old blanket}
\Rightarrow
\text{bounded macro-interface},
}
\]

\[
\boxed{
\text{new attachment is independently future-addressable}
\Rightarrow
\text{cumulative interface memory}.
}
\]

This is conditional on a declared finite deterministic grammar. It does not
claim that arbitrary ecosystems satisfy either premise or that grammar state is
a latent ecological state.