# Grammar-aware dynamic blankets

## The missing positive theorem after delayed addressability

A finite prefix grammar specifies which counterfactual actions are legal from
the current boundary-contract state. Delayed addressability already shows that a
family can postpone an exterior distinction beyond any proposed common horizon.
What it does not by itself provide is a positive criterion for a fixed grammar:

> When may a finite summary certify every future trace that is legal under that
> grammar?

The answer is not just output agreement and not just physical-state update
agreement. A valid summary must also preserve the set of legal next actions.

\[
\boxed{
\text{grammar-aware closure requires output, enabled-action, and successor agreement.}
}
\]

## Product semantic state

Let

\[
M=(S,A,T,h)
\]

be a finite deterministic controlled output system, and let

\[
\mathcal G=(V,v_0,\delta)
\]

be a finite deterministic prefix-closed grammar over the same action alphabet.
A missing transition in \(\delta\) means that the corresponding action is not
legal at that grammar state.

The semantic state is the product

\[
(s,v)\in S\times V.
\]

The grammar state is not asserted to be a new physical ecological variable. It
records the declared boundary contract: which exterior events, interventions, or
protocol steps remain legal from the present situation.

For a word \(w\) legal from \(v\), write

\[
\operatorname{Tr}_{\mathcal G}(s,v;w)
\]

for the output trace produced by applying \(w\) to the system while advancing
both system and grammar state.

## Theorem 1 — Grammar-aware dynamic interface criterion

Let

\[
q:S\times V\to Q
\]

be a finite proposed summary. It is an exact deterministic macro-interface for
all legal future words if the following hold whenever

\[
q(s,v)=q(s',v'):
\]

1. **Output agreement**

   \[
   h(s)=h(s').
   \]

2. **Enabled-action agreement**

   \[
   \operatorname{Legal}(v)=\operatorname{Legal}(v').
   \]

3. **Enabled-successor agreement**: for every
   \(a\in\operatorname{Legal}(v)\),

   \[
   q(T(s,a),\delta(v,a))
   =
   q(T(s',a),\delta(v',a)).
   \]

Under these conditions define the partial macro system by choosing any
representative \((s,v)\) of a summary block:

\[
\bar h(q(s,v))=h(s),
\]

\[
\overline{\operatorname{Legal}}(q(s,v))=\operatorname{Legal}(v),
\]

and, for each enabled action,

\[
\bar T_a(q(s,v))=q(T(s,a),\delta(v,a)).
\]

The three conditions make these definitions representative independent.

### Proof

Proceed by induction on legal word length. The empty word has the same current
output by condition 1. Suppose the statement holds for all words of length at
most \(t\). If \(aw\) is legal from \(v\), condition 2 makes \(a\) legal from
\(v'\) as well, and condition 3 puts both successors in one summary block. The
induction hypothesis applies to the remaining legal suffix \(w\). Thus

\[
\operatorname{Tr}_{\mathcal G}(s,v;w)
=
\operatorname{Tr}_{\mathcal G}(s',v';w)
\]

for every legal future word. \(\square\)

Enabled-action agreement is essential. A summary that predicts the same current
output and the same successors for actions that happen to be shared is still not
an exact macro-law when it incorrectly claims that one state permits an action
which the other forbids.

## Theorem 2 — Coarsest grammar-aware interface

Define grammar-aware trace equivalence on product states by

\[
(s,v)\sim_{\mathcal G}(s',v')
\]

when the states have the same legal future grammar and identical traces for every
word legal from their respective current grammar state.

Then \(\sim_{\mathcal G}\) is the coarsest exact grammar-aware dynamic interface.
Equivalently, every valid summary \(q\) refines this quotient:

\[
q(s,v)=q(s',v')
\quad\Longrightarrow\quad
(s,v)\sim_{\mathcal G}(s',v').
\]

### Proof

The stable refinement begins with current output and repeatedly records the
ordered enabled-action successor labels. At a fixed point it satisfies the three
conditions of Theorem 1. Conversely, Theorem 1 and induction imply that any
valid summary block has identical trace signatures at every finite horizon, and
hence lies in one stable quotient block. \(\square\)

For a product with \(|S||V|\) states, refinement stabilizes by

\[
\boxed{|S||V|-1.}
\]

This is a finite-domain bound for one declared grammar. It does not contradict
the delayed-family theorem: grammar size and the revealing horizon can grow
without a uniform bound across a family.

## Corollary — Finite grammar-aware blanket upper bound

Let \(q:S\times V\to Q\) satisfy Theorem 1. Then the canonical legal-word
interface has at most \(|Q|\) blocks:

\[
\boxed{
K_{\mathcal G,\mathrm{canonical}}
\le
\log_2|Q|.
}
\]

Moreover, its first stable refinement horizon satisfies

\[
\boxed{
H_\star\le |Q|-1.
}
\]

The point is not that a grammar-aware blanket is always small. The point is that
when a valid finite summary exists, it gives a checkable upper bound on both
portable-interface memory and the legal counterfactual horizon for that fixed
system.

## Theorem 3 — Grammar-state necessity witness

For every delay \(H\ge1\), take one physical system state with one constant
window output, and a prefix grammar with legal words

\[
\epsilon,
\mathrm{wait},
\ldots,
\mathrm{wait}^{H},
\mathrm{wait}^{H}\mathrm{fire}.
\]

The physical state never changes, so a summary that remembers only physical
state has one block. Yet the initial grammar state permits `wait`, while the
ready state permits `fire`:

\[
\operatorname{Legal}(v_0)=\{\mathrm{wait}\},
\qquad
\operatorname{Legal}(v_H)=\{\mathrm{fire}\}.
\]

Thus these two product states cannot be merged by Theorem 1, despite having the
same physical state and the same present and future physical output.

\[
\boxed{
\text{physical-state sufficiency}
\not\Rightarrow
\text{grammar-aware sufficiency}.}
\]

The stable quotient has one block per grammar state in this witness. The
obstruction is an explicit enabled-action mismatch certificate, not an informal
claim that time alone is hidden state.

## Relation to the delayed no-go theorem

The two statements have different quantifiers:

\[
\text{fixed finite }(M,\mathcal G)
\Rightarrow
\text{finite exact grammar-aware interface and horizon},
\]

while

\[
\text{growing delayed family }\{(M_H,\mathcal G_H):H\ge0\}
\not\Rightarrow
\text{one uniform finite horizon}.
\]

The first is a positive factorization theorem. The second is a family-level
nonidentifiability obstruction. Both are needed to say exactly what a declared
observation window can and cannot certify.

## Executable certificates

`causal_model.grammar_aware_blankets` provides:

- `GrammarAwareDynamicInterfaceCertificate` for the three local conditions;
- `GrammarAwareCanonicalInterfaceCertificate` for the stable coarsest quotient;
- `GrammarAwareRefinementCertificate` showing that any valid summary refines the
  canonical interface;
- `GrammarAwareDynamicBlanketCertificate` for the memory and horizon upper
  bounds;
- `EnabledActionMismatchCertificate` for one illegal proposed merge; and
- `GrammarStateNecessityCertificate` for the constant-physical-state delayed
  witness.

The workflow cross-checks the recursive quotient against explicit legal-word
trace signatures over finite horizons. It is certificate replay, not simulation
evidence.

## Ecological projection

A phenological gate, seasonal corridor, monitoring protocol, or disturbance
window can change which future boundary events are declared possible. A portable
macro-law must retain the relevant contract state whenever it changes the legal
counterfactual continuation set.

This does not reify a protocol or seasonal gate as an unmeasured organismal
variable. It says that an ecological claim of the form “under these allowed
future connections and perturbations, the window follows this law” must retain
whatever contract information makes those allowed futures well-defined.

## Scope boundary

The theorem is for finite deterministic controlled systems and finite
deterministic prefix-closed grammars. It does not establish corresponding
results for arbitrary stochastic, continuous, partially observed, simultaneous,
or empirical ecosystems.