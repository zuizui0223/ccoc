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

## Exactness assumptions

The proofs use more than binary notation. They require all of the following.

1. **Full compatibility of uneliminated switches.** Every Boolean assignment that satisfies the declared present and NULL clauses is structurally feasible. There are no unmodelled mutual exclusions, budgets, or other compatibility restrictions among switches.
2. **Monotone OR effects.** A driver being ON can only help its declared trait satisfy the clause. There are no inhibitory effects, sign reversals, thresholds, or saturation.
3. **No conjunction requirement.** A trait is not contingent on an AND relation such as \(s_j\land s_k\), a temporal sequence, or feedback dynamics.
4. **Faithful NULL interpretation.** A NULL observation is treated as evidence that every declared driver of that trait is OFF, not merely undetected or below power.
5. **Declared candidate sufficiency.** The driver sets include every candidate route relevant to the scoped question.

If any condition fails, the last-driver statement is not automatically valid. The theorem must then be replaced by a model-specific satisfiability or causal-program analysis.

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

The implementation exposes this direct criterion as `forced_on_by_theorem`. It checks that the observation is nonempty and feasible before returning `True`, so a contradictory observation is never relabelled as a necessity claim.

The associated absolute OFF-state surprisal under an independent Bernoulli prior is

\[
\operatorname{CRC}_j=-\log_2\Pr(s_j=0\mid s\in A(O)).
\]

It is infinite precisely when the mechanism is forced ON. Because it is an absolute conditional surprisal, it is not yet a baseline-adjusted evidence measure; an unconstrained switch can have nonzero CRC solely because its prior permits OFF with probability less than one.

## Theorem C: observation synergy

Consider focal mechanism \(j\) and competitors \(c_1,\ldots,c_n\), all driving a shared present trait. Let each competitor have a distinct private witness. No one witness-null observation makes \(j\) indispensable, but the complete panel of witness-null observations does.

Therefore the resolution objective is not generally submodular. A greedy procedure that stops when every singleton has zero marginal gain can return no observation, even though a joint panel resolves the focal mechanism.

## Computational checks

The test suite exhaustively enumerates all one- and two-trait models with up to three mechanisms and all non-contradictory observation patterns. For each nonempty admissible region it checks both:

- the NULL-only elimination lemma against Boolean enumeration; and
- Theorem A's direct last-driver criterion against Boolean enumeration.

These tests are a regression guard, not a substitute for the proof or for the assumptions above.

## Limits

The theorem does not establish causal necessity in a real ecological system without all of the following:

1. a candidate set that is sufficiently complete for the stated question;
2. valid interpretation of a NULL result rather than an unmeasured or low-power signal;
3. mechanism labels that are not hiding unmeasured latent mediators.

The repository uses this exact core as a base layer for robust-admissibility and minimum discriminating-panel work; it does not silently upgrade a structural theorem into an empirical conclusion.
