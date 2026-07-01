# Joint exterior–mechanism separation and universal open laws

## Why a joint theorem is needed

RACH already establishes two distinct obstructions:

1. an open boundary may require memory for exterior completions; and
2. retained mechanisms may induce different macro transitions even when each has
   a compact exact instance law.

These statements do **not** automatically add. A candidate type may be
unobservable under the same words that expose an exterior coordinate; some
completion/type combinations may be unrealizable; or two sources of variation
may be encoded by one common summary.

This document states the condition under which the burdens genuinely combine.

\[
\boxed{
\text{exterior-memory lower bound}
+
\text{response-type lower bound}
\text{ is valid only with joint operational separation.}
}
\]

## Part I — General universal open-law criterion

Let \(C\) be a finite retained candidate family. Candidate \(\theta\) has a
finite deterministic controlled output system

\[
M_\theta=(S_\theta,A,T^\theta,h^\theta).
\]

Suppose it has a proposed interface

\[
q_\theta:S_\theta\to Q
\]

into one common finite macrostate space \(Q\). A candidate interface is
**dynamic** when there are maps \(\bar h:Q\to Y\) and

\[
G_a^\theta:Q\to Q
\]

such that for every microstate \(s\) and allowed action \(a\),

\[
h^\theta(s)=\bar h(q_\theta(s)),
\qquad
q_\theta(T^\theta(s,a))=G_a^\theta(q_\theta(s)).
\]

The first equality is output sufficiency; the second is update closure. A static
boundary covariate fit without the second condition is not an open macro-law.

## Theorem 1 — Universal open-law criterion

Assume every retained candidate has a dynamic interface into the same
macrostate space \(Q\), with the same macro output map \(\bar h\). Then one
candidate-independent deterministic open macro-law

\[
G_a:Q\to Q
\]

exists if and only if

\[
\boxed{
G_a^\theta=G_a^{\theta'}
\quad
\forall\theta,\theta'\in C,\ \forall a\in A.
}
\]

### Proof

If a universal law exists, then candidate independence gives

\[
G_a^\theta(q)=G_a(q)=G_a^{\theta'}(q)
\]

for every candidate pair, macrostate, and action. Conversely, if all induced
maps agree, define \(G_a\) to be their common map. Dynamic sufficiency of each
candidate interface then makes this common map an exact open macro-law in every
candidate. \(\square\)

The theorem keeps two obligations distinct:

\[
\underbrace{q_\theta\text{ is dynamic}}_{\text{boundary sufficiency}}
\qquad\text{and}\qquad
\underbrace{G_a^\theta\text{ agrees across }\theta}_{\text{mechanism invariance}}.
\]

Neither implies the other.

## Typed outputs when Theorem 1 fails

Let response types be equivalence classes of candidates with the same complete
induced transition maps. The exact candidate-forgetting successor relation is

\[
F_a(q)=\{G_a^\theta(q):\theta\in C\}.
\]

RACH reports the strongest valid object:

\[
\begin{array}{rcl}
\text{all }G_a^\theta\text{ agree}
&\Rightarrow&
\text{universal deterministic open law},\\[4pt]
\text{maps disagree and response type is retained}
&\Rightarrow&
\text{candidate-safe deterministic law on }Q\times R,\\[4pt]
\text{maps disagree and response type is omitted}
&\Rightarrow&
\text{set-valued open law }F\text{, or \texttt{UNRESOLVED} if a deterministic report is required.}
\end{array}
\]

The product \(Q\times R\) is always a deterministic construction after
candidate interfaces have been certified dynamic. It is not automatically a
minimal representation; its exact lower bound needs operational separation.

## Part II — Joint operational separation

Let

\[
I\times E_1\times\cdots\times E_q\times R
\]

be a family of jointly realizable candidate-safe states. Here

- \(I\) is the inside coordinate observed at the window;
- \(E_j\) are exterior completion coordinates; and
- \(R\) is response type.

A **joint operational separation certificate** supplies, for every two unequal
joint states \(z\ne z'\), one declared future query whose window traces differ.
The query must be legal under the declared grammar and every product state used
in the argument must actually be realizable.

The condition is stronger than separate exterior addressability and separate
response-type disagreement. It asks for an injection from the full joint product
into the trace quotient.

## Theorem 2 — Joint product lower bound

Under joint operational separation, every exact candidate-safe deterministic
open interface has at least

\[
\boxed{
|I|\prod_{j=1}^{q}|E_j|\,|R|
}

states. Equivalently,

\[
\boxed{
K_{\mathrm{joint\text{-}safe}}
\ge
\log_2|I|
+
\sum_{j=1}^{q}\log_2|E_j|
+
\log_2|R|.
}
\]

### Proof

Map each jointly realizable product state to its exact future-trace equivalence
class. Joint operational separation says unequal states have unequal trace
classes, so this map is injective. The quotient therefore has at least the
product cardinality. Taking base-two logarithms gives the bound. \(\square\)

The proof is deliberately an injection proof. It does not infer additivity from
two unrelated cardinality counts.

## Canonical structural witness

The executable witness has parameters

\[
I\ge\max\{R,|E_1|,\ldots,|E_q|\},
\qquad |E_j|\ge2.
\]

A joint state is

\[
(i,e_1,\ldots,e_q,r).
\]

The fixed local action alphabet is

\[
A_{\mathrm{local}}=
\{\mathrm{observe},\mathrm{read},\mathrm{intervene}\}.
\]

A structural context attaches a reader to port \(j\); port identity is not part
of the local action symbol. The local semantics are

\[
\begin{array}{rcl}
\mathrm{observe}&:& i\mapsto i,\\[3pt]
\mathrm{read}\text{ at port }j&:& i\mapsto e_j,\\[3pt]
\mathrm{intervene}&:& i\mapsto i+r\pmod{|I|}.
\end{array}
\]

Response type \(r\) is a property of the mechanism, not an action token.

For any unequal states:

- if their inside values differ, `observe` separates them immediately;
- if their first differing exterior coordinate is \(e_j\), `read` in the
  structural port-\(j\) context separates them; and
- if they agree in inside and exterior state but have distinct response types,
  `intervene` separates them because \(|I|\ge |R|\).

Thus every pair has a concrete joint separator. The witness attains equality:

\[
K_{\mathrm{fixed\ candidate}}
=
\log_2|I|+\sum_j\log_2|E_j|,
\]

and

\[
\boxed{
K_{\mathrm{joint\text{-}safe}}
=
\log_2|I|+\sum_j\log_2|E_j|+\log_2|R|.
}
\]

When \(|R|>1\), the same candidate macrostate has incompatible `intervene`
successors across response types, so no universal deterministic open law exists.
When \(|R|=1\), the canonical family has one universal open law.

## Scope of the structural realization

The structural **port choice** follows the same principle as the existing
relay-tree theorem: a reader attachment selects the exterior port while the
local action alphabet remains fixed. This module verifies the theorem at the
finite structural grammar level.

It does **not** yet provide a full degree-three micro-compilation of arbitrary
multi-valued `read` registers plus the response-type shift mechanism. The
existing binary relay compilation remains the degree-three realization of the
selected-port exterior witness. A full joint relay compiler is a strengthening,
not an assumption hidden in this theorem.

## Executable certificates

`causal_model.joint_open_candidate_laws` provides:

- `OpenLawCandidate` and `OpenLawFamily` for candidate-specific micro systems
  with common proposed macrostate space;
- `UniversalOpenLawCertificate` and
  `UniversalOpenLawObstructionCertificate` for Theorem 1;
- `CandidateSafeOpenLawCertificate`, `SetValuedOpenLawCertificate`, and
  `TypedOpenLawVerdictCertificate` for the report trichotomy;
- `JointStructuralSeparationCertificate` for a concrete separator of any two
  canonical joint states; and
- `JointExteriorMechanismProductCertificate` for Theorem 2 and exact equality
  in the canonical family.

The workflow replays finite families and checks every pairwise joint separator.
It is certificate replay, not simulation evidence.

## Ecological projection

A field plot can require both kinds of memory:

1. exterior completion state, such as an immigration source, dispersal corridor,
   pathogen reservoir, delayed propagule pool, or resource connection; and
2. mechanism response type, such as distinct retained hypotheses about how the
   same disturbance or reconnection changes the community.

The theorem does not say these always add. It says that when the declared
counterfactual grammar can separately expose every joint completion/mechanism
state, a portable deterministic law must retain their combined information.

The ecological law-reporting consequence is sharp:

- one common dynamic blanket plus common induced maps supports a universal open
  law;
- a common blanket with retained response type supports a candidate-safe law;
- forgetting response type yields a set-valued forecast; and
- an unbounded exterior-memory obstruction remains a separate reason no fixed
  finite blanket works across the declared family.
