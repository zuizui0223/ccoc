# Conservative macro-schema extension under newly legal actions

## The gap

A fixed coherent portable macro-law is enough when every old embedded state keeps
exactly the same legal actions. But ecological composition can make an action,
connection, exposure, or route newly available at an already-existing state.

The fixed-legality theorem remains valid in its own domain. This theorem adds the
strictly broader monotone-grammar case without changing the established
extension–compression inequalities or fixed-legality certificates.

## Setup

Fix one finite global action alphabet \(A\). At stage \(m\), a finite
grammar-aware controlled system has an exact summary

\[
q_m:S_m\times G_m\to Q.
\]

Old trajectories embed into later stages. Legal actions may expand:

\[
\mathrm{Legal}_m(x)
\subseteq
\mathrm{Legal}_{m+1}(\iota_m x).
\]

The inclusion is deliberately not equality.

## Conservative macro schema

A conservative schema consists of a finite macro state set \(Q\), output map
\(\bar h\), and partial action transition table

\[
\bar T:Q\times A\to Q\cup\{\bot\}.
\]

The schema may already specify the meaning of an action before a particular
stage admits it. At each stage, the realized legal actions are a restriction of
this schema:

\[
q_m(T_m(x,a))=\bar T(q_m(x),a)
\]

whenever \(a\) is legal at \(x\) in stage \(m\).

For adjacent stages, legal macro rows may only expand. If \(a\) was already
legal, its macro successor cannot change:

\[
\bar T_m(q,a)\ne\bot
\Longrightarrow
\bar T_{m+1}(q,a)=\bar T_m(q,a).
\]

Embedding coherence remains

\[
q_{m+1}(\iota_m x)=q_m(x).
\]

## Theorem — conservative portability

Under the conservative schema premise, the union grammar has one exact finite
macro schema. Every action that becomes legal later receives the pre-specified,
label-deterministic macro successor; every previously legal action keeps its old
meaning.

\[
\boxed{
\text{monotone legal-action expansion}
+
\text{one finite conservative schema}
+
\text{label-coherent trajectory embeddings}
\Rightarrow
\text{portable macro schema on the union grammar.}
}
\]

### Proof

At each finite stage, exactness of \(q_m\) makes every currently legal action
constant on each summary fiber. The stage transition table is therefore a
restriction of \(\bar T\). Monotonicity prevents any earlier defined macro
transition from changing. Embedding coherence preserves the macro label of every
old trajectory. Thus all finite stage tables are compatible restrictions of one
partial table \(\bar T\), which is exact wherever an action is admitted in the
union grammar. \(\square\)

The result is stronger than bounded interface cardinality and weaker than
requiring fixed legal rows forever.

## Concrete obstruction

Let two target-stage states lie in one proposed macro fiber \(q\), and let a
newly legal action \(a\) be available at both. If either their one-step output
traces differ or their proposed successor labels differ, then no exact
conservative schema can assign one successor \(\bar T(q,a)\).

\[
\boxed{
q(x)=q(y),
\quad a\in\mathrm{Legal}(x)\cap\mathrm{Legal}(y),
\quad
\operatorname{Tr}(x,a)\ne\operatorname{Tr}(y,a)
\ \text{or}\ q(T(x,a))\ne q(T(y,a))
}
\]

is an explicit portability obstruction.

## Positive witness

The executable two-stage witness has macro states \(0,1\) and actions
`stay,reveal`.

At stage 0, `reveal` is unavailable at macrostate 0. At stage 1 it becomes legal
and sends macrostate 0 to macrostate 1:

\[
\bar T(0,\mathrm{stay})=0,
\qquad
\bar T(0,\mathrm{reveal})=1.
\]

The old `stay` dynamics are unchanged. Thus the extension is portable even
though the legal grammar has expanded.

## Ecological reading

A later-available dispersal corridor, experimental exposure, mutualist contact,
or habitat link need not invalidate a macro-law merely because it is new. It is
portable when the newly available connection has one well-defined effect for
every state already grouped into the same macrostate.

It invalidates the macro-law when the new connection reveals hidden variation
inside a previously merged class. The obstruction then identifies the class,
connection, and conflicting future outcomes.

The theorem applies only to declared finite deterministic systems and a fixed
finite action alphabet. It does not claim that all ecological additions can be
represented as such actions.