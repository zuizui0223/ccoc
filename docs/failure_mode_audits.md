# Theorem-scope failure-mode audits

## Purpose

The exact replaceability theorem is correct for its declared finite monotone-OR model. The important scientific question is not whether to stretch that theorem past its assumptions, but how badly a causal conclusion can fail when those assumptions are wrong.

`causal_model.failure_modes` provides finite truth-table audits. A declared `StructuralModel` is evaluated with the exact theorem, then compared with a separate `TruthTableModel` that can encode omitted drivers, inhibition, conjunctions, and background state-compatibility constraints.

## Audit labels

| Label | Meaning |
|---|---|
| `match` | The declared forced-ON conclusion matches finite true-model behavior. |
| `false_necessity` | The declared theorem calls the focal mechanism indispensable, but a true admissible state has it OFF. |
| `missed_necessity` | The focal mechanism is truly ON in every admissible true state, but the declared last-driver rule does not detect it. |
| `true_model_contradiction` | The declared OR model admits the observation, but the true model has no compatible state. |
| `declared_model_contradiction` | The declared model rejects an observation that the true model permits. |
| `both_models_contradict` | Neither model permits the stated observation. |

A contradiction label is not a causal claim. It is a model-checking alarm: the observation should not be used to infer necessity under the declared grammar.

## 1. Omitted latent competitor

The declared target has drivers \(\{j,c\}\), and a NULL private witness removes \(c\). The theorem therefore calls \(j\) the final surviving driver. In the true model, an omitted mechanism \(\ell\) can also generate the target but has no declared witness. The true state

\[
(s_j,s_c,s_\ell)=(0,0,1)
\]

matches target PRESENT and competitor witness NULL, so the declared conclusion is a `false_necessity`.

**Interpretation:** candidate-set completeness is not bookkeeping; it is an identifying assumption.

## 2. Noisy NULL results

For the simple two-driver model, let the focal driver be \(j\), the competitor be \(c\), and let a private witness perfectly reflect \(c\) before measurement error. The report is target PRESENT plus witness NULL. If the witness has sensitivity \(1-\varepsilon\), zero false-positive rate, and all four switch states have equal prior probability, then the declared theorem calls \(j\) forced ON but

\[
\Pr(s_j=0\mid \text{target PRESENT, witness reported NULL})
=
\frac{\varepsilon}{1+2\varepsilon}.
\]

At 90% sensitivity, \(\varepsilon=0.1\), so the false-necessity risk is

\[
\frac{0.1}{1.2}=\frac1{12}\approx 8.3\%.
\]

The implementation generalizes this calculation to arbitrary finite truth states, trait-specific binary observation channels, and user-specified prior state weights.

**Interpretation:** a NULL result needs an explicit measurement model or a defensible power threshold before it can act as deterministic elimination.

## 3. Inhibitory effects

Suppose a witness is truly expressed only when \(c=1\) and an inhibitor \(h=0\). A NULL witness therefore need not mean \(c=0\); it may mean \(h=1\). The state

\[
(s_j,s_c,s_h)=(0,1,1)
\]

can match target PRESENT and witness NULL, even though the declared OR model removes \(c\) and calls \(j\) necessary. This is another `false_necessity`.

**Interpretation:** sign-consistency and monotonicity are substantive assumptions. A NULL observation is not universally an OFF certificate.

## 4. Conjunctions

When a target truly requires \(j\land c\), observing the target PRESENT while a private witness says \(c\) is NULL has no true compatible state. An OR grammar instead treats the target as satisfiable by \(j\) alone and can call it necessary. The audit returns `true_model_contradiction`.

**Interpretation:** do not interpret an OR-theorem result when the observed phenotype could require joint action, sequence, or threshold crossing.

## 5. Compatibility constraints and missed necessity

Hidden prerequisites can create true necessity that is invisible to last-driver logic. In the supplied truth-table example, the competitor can only occur when the focal mechanism is also ON. The declared grammar sees two surviving target drivers and remains unresolved; the true state space makes the focal mechanism ON in every target-present state. The audit returns `missed_necessity`.

**Interpretation:** the OR theorem can be conservative as well as overconfident once free switch compatibility fails.

## Practical rule

Use the exact theorem only after documenting why the following hold for the scoped question:

1. all plausible target drivers are represented;
2. a reported NULL is sufficiently reliable to approximate deterministic elimination;
3. drivers act monotonically rather than through suppression or context-dependent reversal;
4. target expression is not contingent on unmodelled conjunctions, sequences, or thresholds; and
5. mechanisms are jointly feasible unless a richer constrained state model is used.

When any item is uncertain, report the theorem output as a **conditional design heuristic**, then run a truth-table or program-family audit rather than upgrading it to causal necessity.
