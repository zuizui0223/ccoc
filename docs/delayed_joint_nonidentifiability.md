# Delayed joint exterior–mechanism nonidentifiability

## What is added beyond the earlier theorems

The repository already had two separate results:

1. independently addressable exterior coordinates can force an open-interface
   memory lower bound; and
2. an exterior coordinate may be legally addressable only after an arbitrarily
   long declared delay.

It also had a response-type theorem: one deterministic candidate-independent law
is not licensed when retained mechanisms induce different responses.

The present theorem combines the outside and mechanism burdens **in time**. It
shows that a stable record over every legal word through the current horizon may
hide both an exterior difference and a response-type difference at once.

\[
\boxed{
\text{early legal stability}
\not\Rightarrow
\text{a universal open law is certified.}
}
\]

## Delayed binary joint family

Fix an exterior-port count \(m\ge1\) and a delay \(H\ge0\). The initial macro
state is

\[
(y,b_1,\ldots,b_m,r)\in\{0,1\}^{m+2},
\]

where:

- \(y\) is the current focal/window output;
- \(b_i\) is the \(i\)-th exterior completion coordinate; and
- \(r\) is retained response type.

The action **kinds** are fixed:

\[
\{\mathrm{wait},\mathrm{read},\mathrm{intervene}\}.
\]

A `read` port is selected by a structural attachment context, not by an expanding
alphabet item such as `read:i`. The response type is state/mechanism information,
not a command such as `intervene:r`.

The prefix grammar is:

\[
\underbrace{\mathrm{wait}\cdots\mathrm{wait}}_{H\text{ times}}
\quad\longrightarrow\quad
\begin{cases}
\mathrm{read}_i & \text{for one structural port }i,\\
\mathrm{intervene}. &
\end{cases}
\]

Before readiness, `wait` is the only legal action. After exactly \(H\) waits,
the grammar allows one terminal boundary event.

The macro transitions are

\[
\mathrm{wait}:
(y,\mathbf b,r)\mapsto(y,\mathbf b,r),
\]

\[
\mathrm{read}_i:
(y,\mathbf b,r)\mapsto(b_i,\mathbf b,r),
\]

\[
\mathrm{intervene}:
(y,\mathbf b,r)\mapsto(y\oplus r,\mathbf b,r).
\]

The final line is the binary restriction of the joint product's modular response
rule.

## Theorem 1 — Exact delayed joint quotient jump

Let \(\sim_{\le h}\) identify initial states with identical traces for all
legal words of length at most \(h\). Then

\[
\boxed{
\left|\{0,1\}^{m+2}/\!\sim_{\le H}\right|=2,
\qquad
\left|\{0,1\}^{m+2}/\!\sim_{\le H+1}\right|=2^{m+2}.
}
\]

Equivalently,

\[
\boxed{
K_{\le H}=1,
\qquad
K_{\mathrm{full}}=m+2,
qquad
H_\star=H+1.
}
\]

### Proof

Every word legal from the initial grammar state with length at most \(H\) is
\(\mathrm{wait}^t\) for some \(0\le t\le H\). `wait` does not change the
macro state, so its trace is simply

\[
(y,y,\ldots,y).
\]

Hence all states with the same \(y\) are early-equivalent, yielding exactly two
blocks.

For the full quotient, take distinct states \(x,x'\). If their focal bits
differ, the empty word separates them. Otherwise, if some exterior coordinate
\(b_i\) differs, the legal word

\[
\mathrm{wait}^{H}\mathrm{read}_i
\]

separates them. If all exterior coordinates agree but \(r\) differs, then

\[
\mathrm{wait}^{H}\mathrm{intervene}
\]

separates them. Thus every unequal pair has a legal separating word by horizon
\(H+1\), so the quotient has all \(2^{m+2}\) singleton blocks. The first
possible non-`wait` event has length \(H+1\), proving minimality. \(\square\)

## Theorem 2 — No uniform joint closure horizon

For every proposed finite horizon \(h\), choose the family member with
\(H=h\). Consider the two states

\[
x=(0,0,\ldots,0,0),
\]

\[
x'=(0,1,0,\ldots,0,1).
\]

They agree on all legal traces through \(h\): only `wait` is legal, and both
have focal output zero. Yet at horizon \(h+1\), both legal words

\[
\mathrm{wait}^{h}\mathrm{read}_1
\]

and

\[
\mathrm{wait}^{h}\mathrm{intervene}
\]

separate the same pair.

Therefore,

\[
\boxed{
\forall h<\infty\;\exists(M_h,\Gamma_h,x,x'):
\operatorname{Tr}_{\le h}(x)=\operatorname{Tr}_{\le h}(x')
\text{ but }
\operatorname{Tr}_{\le h+1}(x)\ne\operatorname{Tr}_{\le h+1}(x').
}
\]

No single finite legal-word horizon can certify candidate-safe open closure
uniformly over the expanding delayed joint family.

## Why this does not contradict the positive blanket theorem

For every fixed \((m,H)\), the state space and grammar are finite. Its
full grammar-aware quotient is finite and can be certified by a finite horizon.

The negative statement changes the quantifiers:

\[
\forall\text{ fixed member},\;\exists\text{ finite horizon}
\]

does not imply

\[
\exists\text{ one finite horizon},\;\forall\text{ members}.
\]

The grammar-aware dynamic blanket theorem remains the positive criterion for a
fixed declared contract. This theorem says that a family of contracts can delay
both kinds of missing information without bound.

## Certificates

`causal_model.delayed_joint_nonidentifiability` provides:

- `DelayedJointGrammar` for legal structural-read/intervention words;
- `DelayedJointSeparatorCertificate` for one concrete pairwise separator;
- `DelayedJointQuotientJumpCertificate` for the early/full quotient jump; and
- `DelayedJointNoUniformHorizonCertificate` for the family-level counterexample
  at any proposed horizon.

The replay checks finite representatives of the all-parameter proof. It is not
simulation evidence outside the declared finite grammar.

## Ecological projection

A delayed dispersal route, seasonal partner availability, rare disturbance
window, or a future intervention gate can postpone two independent failures of
promotion:

1. an exterior completion becomes relevant only later; and
2. retained mechanisms give different responses when that event finally occurs.

A time series or field observation that is stable through the currently available
contract horizon therefore cannot by itself justify the sentence “one universal
open law has been found.” It can still support a conditional law under the
current boundary contract, a candidate-safe law that retains response type, or
an honest `UNRESOLVED` verdict.

## Scope boundary

The theorem concerns finite deterministic binary macro systems, a sequential
prefix grammar, and structurally selected read ports. It does not claim that
real ecosystems are binary, deterministic, or subject to a single known
seasonal grammar. The construction is a sharp counterexample family for the
logical promotion step, not a literal ecological ontology.