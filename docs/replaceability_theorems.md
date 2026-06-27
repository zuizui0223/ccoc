# Exact causal-replaceability theorem core

## Declared structural model

Let the candidate mechanisms be binary switches

\[
s=(s_1,\ldots,s_K)\in\{0,1\}^K.
\]

Each observable trait \(t\) has a nonempty driver set \(D(t)\). Under the declared sign-consistent disjunctive semantics,

\[
\operatorname{cline}(t)\iff\bigvee_{k\in D(t)}s_k.
\]

An observation contains required-present traits and required-null traits. The admissible structural region is

\[
A(O)=\{s: \text{every present clause holds and every null-driver is OFF}\}.
\]

This is a finite, exact theorem target. It is not a fitted ecological model.

## Lemma: elimination is null-only

Define

\[
\operatorname{NullOff}(O)=\bigcup_{t\in O_{\rm null}}D(t).
\]

For every nonempty admissible region,

\[
s_k=0\;\forall s\in A(O)
\iff
k\in\operatorname{NullOff}(O).
\]

Thus positive observations can satisfy a present disjunction, but cannot eliminate a candidate mechanism.

## Theorem A: last driver standing

A mechanism \(j\) is forced ON in every admissible configuration if and only if there is a required-present trait \(t\) such that

\[
j\in D(t),\qquad D(t)\setminus\{j\}\subseteq\operatorname{NullOff}(O).
\]

Equivalently, \(j\) is indispensable **within the declared candidate set** exactly when it is the last surviving driver of some required-present trait.

The associated structural causal replaceability cost is

\[
\operatorname{CRC}_j=-\log_2\Pr(s_j=0\mid s\in A(O)).
\]

It is infinite precisely when the mechanism is forced ON.

## Theorem C: observation synergy

Consider focal mechanism \(j\) and competitors \(c_1,\ldots,c_n\), all driving a shared present trait. Let each competitor have a distinct private witness. No one witness-null observation makes \(j\) indispensable, but the complete panel of witness-null observations does.

Therefore the resolution objective is not generally submodular. A greedy procedure that stops when every singleton has zero marginal gain can return no observation, even though a joint panel resolves the focal mechanism.

## Limits

The theorem does not establish causal necessity in a real ecological system without all of the following:

1. a candidate set that is sufficiently complete for the stated question;
2. valid interpretation of a NULL result rather than an unmeasured or low-power signal;
3. mechanism labels that are not hiding unmeasured latent mediators.

The repository will use this exact core as a base layer for robust-admissibility and minimum discriminating-panel work; it will not silently upgrade a structural theorem into an empirical conclusion.
