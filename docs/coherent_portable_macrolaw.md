# Coherent portable macro-laws under nested composition

## The gap after boundedness

A common finite summary alphabet \(Q\) can bound the exact quotient size at each
composition stage. That alone does **not** prove that there is one portable
macro-law. Two stages may use labels from the same alphabet while assigning
different outputs, legal actions, or successor transitions to those labels.

This theorem adds the missing coherence requirement.

## Nested stages

Let finite grammar-aware controlled systems form a nested chain

\[
(M_1,\Gamma_1)
\xrightarrow{\iota_1}
(M_2,\Gamma_2)
\xrightarrow{\iota_2}
\cdots.
\]

Each embedding preserves old outputs and every trajectory legal at the old stage.
A later stage may have additional legal actions; it need not have the same full
grammar.

For every stage let

\[
q_m:S_m\times G_m\to Q.
\]

## Coherence premise

Require one finite macro system

\[
\mathcal A=(Q,\bar h,\overline{\mathrm{Legal}},\bar T)
\]

such that every stage satisfies

\[
h_m=\bar h\circ q_m,
\]

\[
\mathrm{Legal}_m(s,g)
=
\overline{\mathrm{Legal}}(q_m(s,g)),
\]

and, for every legal action,

\[
q_m(T_m(s,a),\delta_m(g,a))
=
\bar T(q_m(s,g),a).
\]

Finally, require embedding coherence:

\[
\boxed{
q_{m+1}(\iota_m(s,g))=q_m(s,g).
}
\]

This is stronger than a common cardinality bound. It says every old state keeps
the same macro meaning after new modules are added.

## Theorem — coherent portability

Under the coherence premise, every stage has the same exact macro dynamics
\(\mathcal A\). Consequently the nested union/direct-limit composition has one
finite portable macro-law on \(Q\).

\[
\boxed{
\text{common finite dynamics}
+
\text{trajectory-preserving embeddings}
+
\text{label coherence}
\Rightarrow
\text{one extension-portable macro-law.}
}
\]

### Proof

At each stage, output/legal-action/successor preservation makes \(q_m\) an exact
dynamic interface whose induced macro system is \(\mathcal A\). Embedding
coherence identifies every old macrostate with the same macrostate at the next
stage. By induction, every finite trajectory in an earlier stage has the same
macro trace in every later stage. Thus the compatible stage laws define one law
on the nested union. \(\square\)

The theorem is finite-stage executable. The direct-limit statement is the
mathematical consequence of compatibility of all finite stages; the code does
not pretend to enumerate an infinite union.

## Future-word obstruction

Suppose two old states are merged by a proposed summary and their embedded images
remain merged at a later stage. If a word newly legal at that later stage yields
different output traces from the two images, then no exact coherent portable
macro-law can pass through that proposed merge.

\[
\boxed{
q_m(x)=q_m(y),
\quad
q_n(\iota_{m,n}x)=q_n(\iota_{m,n}y),
\quad
\operatorname{Tr}(\iota_{m,n}x,w)
\ne
\operatorname{Tr}(\iota_{m,n}y,w)
}
\]

is a concrete obstruction.

This is stronger than saying a quotient size increased. It names the old pair,
the later legal word, and the future distinction that makes the proposed shared
macrostate invalid.

## Positive witness

The executable inert chain has \(2^m\) physical configurations at stage \(m\),
but all configurations share one output and identical transition behavior under
all actions. Every stage projects to the same one-state macro system:

\[
Q=\{0\},
\qquad
\bar h(0)=\text{inert-window},
\qquad
\bar T(0,a)=0.
\]

Embeddings retain the same label. This proves that a growing composition can
have not only bounded interface size but literally the same portable macro-law.

## Relation to other RACH results

- The uniform dynamic blanket criterion proves bounded stagewise memory.
- This theorem adds common macro dynamics and embedding coherence, yielding one
  law across stages.
- The extension–compression lower bound proves growth when new factors become
  independently future-addressable.
- The future-word obstruction detects one concrete failure of portability before
  a full product lower bound is available.

## Ecological reading

A macro-law can persist across species addition, removal, reconnection, or
habitat expansion only if old ecological states retain the same macro meaning and
all newly available trajectories still factor through one common response
machine. It is not enough that every stage needs, say, three summary labels.
Those labels must denote the same outputs and causal update rules across stages.

Conversely, a newly possible exposure that distinguishes two formerly merged old
conditions is an explicit reason that the old macro-law was not portable.

The theorem is conditional on declared nested finite systems and legal grammars.
It does not assert that real ecosystems automatically provide such embeddings or
that grammar states are biological variables.