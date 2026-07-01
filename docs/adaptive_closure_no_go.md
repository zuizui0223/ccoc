# Adaptive finite-experiment no-go for exterior closure

## The question

A fixed observation panel can fail to reveal a delayed exterior influence. That
alone does not settle the stronger objection:

> What if the investigator chooses every next action adaptively, after seeing
> all previous measurements?

This theorem answers that question for every **finite** adaptive experiment.

\[
\boxed{
\text{No finite adaptive experiment certifies exterior irrelevance}
}
\]

over a family in which admissible exterior effects can be delayed beyond the
experiment and can have unbounded future-addressable response complexity.

The target property is exterior closure

\[
|B_\Gamma|=1,
\]

not merely existence of some finite boundary blanket. Every fixed open witness
below has a finite blanket; it is nevertheless not exterior-closed.

## Finite adaptive policy

Fix a constant action alphabet

\[
A=\{\mathrm{tick},\mathrm{bit0},\mathrm{bit1},\mathrm{fire}\}.
\]

A deterministic finite adaptive policy \(\Pi\) is a finite decision tree. At
step \(t\), it selects an action as a function of the output history observed
through that step. Its maximum depth is \(D\).

There is no action such as \(\mathrm{probe}:i\). A future exterior coordinate
is addressed using a binary sequence over `bit0` and `bit1`, followed by `fire`.
Thus the action alphabet remains constant as the number of addressable exterior
coordinates grows.

## Lemma — Policy lifting

Suppose two controlled systems satisfy

\[
\operatorname{Tr}_{M}(w)=\operatorname{Tr}_{M'}(w)
\qquad
\forall w\in A^{\le D}.
\]

Then every adaptive policy of depth at most \(D\) produces the same complete
interaction transcript on both systems.

### Proof

Initially the outputs agree. Assume the two policy runs have the same output
history through step \(t<D\). Because the policy is deterministic, it chooses
the same next action on both systems. The corresponding action word has length
at most \(D\), so its next output agrees by hypothesis. Induction proves that
the whole action/output transcript agrees. \(\square\)

The key point is that adaptivity provides no escape from a uniform all-word
indistinguishability statement through the policy horizon.

## Delayed closed/open pair

Fix a delay \(H\) and an address length \(\ell\). Let

\[
m=2^\ell.
\]

The initial focal output is \(y=0\). In the open system, an exterior completion
is a binary vector

\[
e=(e_0,\ldots,e_{m-1})\in\{0,1\}^{m}.
\]

For the first \(H\) actions, **every** action in \(A\) merely advances a known
protocol phase and leaves output unchanged. It does not matter whether the
policy tries `fire`, an address bit, or anything else.

After the gate opens, the word

\[
u_i=
\mathrm{tick}^{H}
\operatorname{address}(i)
\mathrm{fire}
\]

returns exterior coordinate \(e_i\) in the open system. The closed comparator
uses the same action alphabet and delay protocol, but its response is independent
of every exterior coordinate.

The phase counter is known protocol state. Complexity is evaluated on the
declared initial phase slice, so the theorem does not disguise a clock as unknown
window memory.

## Lemma — Canonical blanket sizes

For the closed comparator,

\[
|B_\Gamma^{\mathrm{closed}}|=1.
\]

For the delayed open system,

\[
\boxed{
|B_\Gamma^{\mathrm{open}}|=2^{m}=2^{2^\ell}.
}
\]

### Proof

The closed comparator ignores \(e\), so all exterior completions have identical
responses. In the open system, any distinct vectors \(e,e'\) differ at some
coordinate \(i\). The legal word \(u_i\) returns different outputs, so every
distinct exterior vector occupies a separate canonical response class.
\(\square\)

## Theorem — Adaptive closure no-go

For every finite adaptive policy \(\Pi\) of depth \(D\) and every address length
\(\ell\), choose

\[
H>D.
\]

Then there is a closed/open delayed pair such that

\[
\boxed{
\operatorname{Transcript}_\Pi(M_{\mathrm{closed}})
=
\operatorname{Transcript}_\Pi(M_{\mathrm{open}}),
}
\]

while

\[
\boxed{
|B_\Gamma(M_{\mathrm{closed}})|=1,
\qquad
|B_\Gamma(M_{\mathrm{open}})|=2^{2^\ell}.
}
\]

### Proof

Every action word with length at most \(D\) ends before the gate opens. Both
systems therefore return the unchanged focal output at every step, for every
such word. The policy-lifting lemma gives identical adaptive transcripts.

Afterwards, choose the open completion with \(e_0=1\). The future word

\[
\mathrm{tick}^{H}\mathrm{bit0}^{\ell}\mathrm{fire}
\]

returns zero in the closed comparator and one in the open system. The blanket
cardinality lemma gives the closure gap. \(\square\)

Therefore no finite-depth transcript-only rule can be both sound and complete
for the predicate \(|B_\Gamma|=1\) over this delayed family.

## Corollary — No finite transcript-only upper certificate

Let an adaptive policy have finite depth \(D\), and suppose a transcript-only
procedure proposes a finite blanket upper bound \(U\). Choose \(\ell\) such
that

\[
2^{2^\ell}>U,
\]

and then choose \(H>D\). The delayed open model has the same transcript as its
closed comparator under the policy, but its canonical blanket exceeds \(U\).

\[
\boxed{
\text{Without an independent uniform contract, a finite transcript cannot
soundly certify any finite global blanket upper bound.}
}
\]

The sound output in this model class is `UNRESOLVED`, unless additional bounds
are supplied.

## What would make finite certification possible

The theorem identifies the missing assumptions. A finite exhaustive procedure is
possible only after the model contract supplies, independently of the observed
transcript:

\[
\text{uniform delay bound}
+
\text{finite address/grammar bound}
+
\text{completion coverage}.
\]

With those bounds, the relevant response table is finite and the canonical
blanket can be enumerated or proven by a finite quotient certificate. The no-go
does not deny this; it denies obtaining those uniform bounds from a finite
adaptive transcript alone.

## Ecological projection

An investigator can adaptively choose a next plot, sampling time, camera
configuration, assay, or perturbation after every prior outcome. That power is
real, but it is still a finite adaptive policy when the campaign has a finite
endpoint.

If a delayed dispersal source, rare colonist, seasonal mutualist, external
climate pathway, or unmeasured response type may become admissible only after an
unbounded delay, then no finite adaptive campaign proves that the observation
window is exterior-closed. The appropriate conclusion is not a false declaration
of closure, but

\[
\boxed{\mathrm{UNRESOLVED}}
\]

until a biological or physical argument supplies a uniform horizon and a finite
outside-response contract.

## Scope

Finite deterministic binary-output witnesses; one constant action alphabet; and
known delay phase at the initial slice. The theorem does not claim that real
ecosystems are binary or deterministic, nor that field researchers can enumerate
all completions. It is a logical obstruction to promotion from finite adaptive
evidence to a universal exterior-closure claim.