# Addressable-completion product bounds

## Why this theorem is needed

The observation-window no-go witness shows that passive observations can leave
future-relevant exterior completions unresolved. By itself, however, a binary
copy-bit family could be dismissed as a coordinate trick.

This document states the reusable mathematical reason that an exterior forces
interface memory: **each exterior coordinate must be operationally readable by a
concrete allowed boundary word.** The lower bound follows from those separating
words, not from declaring a partition large in advance.

## Controlled response quotient

Let a finite deterministic controlled response system have state space \(S\), a
set of permitted words \(\mathcal L\), and a window response

\[
R:S\times\mathcal L\to\mathcal Y.
\]

The response may be a full output trace; the theorem needs only equality or
inequality of responses.

For a grammar \(\mathcal L\), define controlled trace equivalence

\[
s\equiv_{\mathcal L}s'
\iff
\forall w\in\mathcal L,
\quad R(s,w)=R(s',w).
\]

The exact causal-interface memory is

\[
K_{\mathcal L}
=
\log_2\left|S/\equiv_{\mathcal L}\right|.
\]

An interface is sound only when equal interface values imply this equivalence.
Thus any injection into the quotient is an information-theoretic lower bound on
all sound interfaces.

## Operational addressability

Assume a distinguished product subset of global states

\[
S^\star
\cong
I\times E_1\times\cdots\times E_q.
\]

Here \(I\) is the window-side state and \(E_j\) is an exterior completion
coordinate. The factors need not be binary.

The coordinates are **operationally addressable** under \(\mathcal L\) when
there exist words

\[
r_0,r_1,\ldots,r_q\in\mathcal L
\]

and decoders \(d_j\) such that, for every

\[
s=(i,e_1,\ldots,e_q)\in S^\star,
\]

\[
d_0(R(s,r_0))=i,
\qquad
d_j(R(s,r_j))=e_j\quad (1\le j\le q).
\]

This condition is deliberately counterfactual and operational. It says that a
permitted future boundary word can expose the value of exterior coordinate
\(j\), regardless of the values held by all other coordinates. It is not a
restatement that some already-computed quotient happened to have many blocks.

## Theorem 1 — Addressable-completion product lower bound

Under operational addressability,

\[
\boxed{
K_{\mathcal L}
\ge
\log_2|I|
+
\sum_{j=1}^{q}\log_2|E_j|.
}
\]

### Proof

Take two distinct states

\[
s=(i,e_1,\ldots,e_q),
\qquad
s'=(i',e_1',\ldots,e_q').
\]

If \(i\ne i'\), then decoding the response to \(r_0\) yields distinct values,
so \(R(s,r_0)\ne R(s',r_0)\). Otherwise there is some \(j\) with
\(e_j\ne e_j'\), and decoding the response to \(r_j\) yields distinct values,
so \(R(s,r_j)\ne R(s',r_j)\).

Therefore every distinct pair in \(S^\star\) belongs to different
\(\equiv_{\mathcal L}\)-classes. The quotient contains at least

\[
|I|\prod_{j=1}^{q}|E_j|
\]

classes. Taking base-two logarithms proves the claim. \(\square\)

The proof is an injection proof driven by concrete separating words.

## Theorem 2 — Closed/open extension--compression inequality

For a fixed closed context \(c\), suppose only exterior coordinate \(E_c\)
can be read, and suppose every permitted closed response factors through
\((i,e_c)\):

\[
R_c((i,e_1,\ldots,e_q),w)
=
F_{c,w}(i,e_c)
\qquad
\forall w\in\mathcal L_c.
\]

If \(r_0\) and \(r_c\) are allowed in \(\mathcal L_c\), then

\[
K_{\mathcal L_c}
=
\log_2|I|+\log_2|E_c|.
\]

Combining this equality with Theorem 1 gives

\[
\boxed{
K_{\mathrm{open}}
-
\max_c K_{\mathcal L_c}
\ge
\sum_{j=1}^{q}\log_2|E_j|
-
\max_c\log_2|E_c|.
}
\]

### Proof

The factorization makes the projection

\[
(i,e_1,\ldots,e_q)\mapsto(i,e_c)
\]

sound for the closed grammar, giving the upper bound. The words \(r_0\) and
\(r_c\) distinguish every two distinct \((i,e_c)\) pairs, giving the matching
lower bound. Substitute these closed values into Theorem 1. \(\square\)

### Binary consequence

When \(|I|=2\) and every \(|E_j|=2\),

\[
K_{\mathcal L_c}=2,
\qquad
K_{\mathrm{open}}\ge q+1,
\qquad
K_{\mathrm{open}}-\max_cK_{\mathcal L_c}\ge q-1.
\]

The relay-tree witness realizes equality:

\[
K_{\mathrm{open}}=q+1,
\qquad
\max_cK_{\mathcal L_c}=2.
\]

Thus a family can have a constant-size exact law in every fixed closed context
while requiring linearly growing memory for one interface safe under all declared
future exterior connections.

## Theorem 3 — Grammar refinement monotonicity

For grammars \(\mathcal L_1\subseteq\mathcal L_2\),

\[
\boxed{K_{\mathcal L_1}\le K_{\mathcal L_2}.}
\]

### Proof

Equivalence under \(\mathcal L_2\) requires equal response for every word in
\(\mathcal L_2\), and hence for every word in its subset \(\mathcal L_1\). So

\[
\equiv_{\mathcal L_2}\subseteq\equiv_{\mathcal L_1}.
\]

The quotient for the larger grammar is a refinement and cannot have fewer
classes. \(\square\)

This is the basic inequality behind the phrase “allowing more ecosystem-outside
counterfactuals cannot make a safe causal interface smaller.”

## Theorem 4 — Passive-only closure nonidentifiability

There exist a closed response system \(M^{\mathrm{cl}}\) and an open response
system \(M^{\mathrm{op}}\) on the same product state space such that:

1. all passive responses coincide;
2. the closed system's response to every boundary read depends only on \(i\);
3. the open system reads \(e_j\) through \(r_j\); and
4. their open interface memories differ.

For the canonical product family,

\[
K_{\mathrm{open}}(M^{\mathrm{cl}})=\log_2|I|,
\]

whereas

\[
K_{\mathrm{open}}(M^{\mathrm{op}})
=
\log_2|I|+
\sum_{j=1}^{q}\log_2|E_j|.
\]

### Proof

Let passive observation return only \(i\) in both models. In the closed model,
every boundary read also returns only \(i\). In the open model, \(r_j\) returns
the value of \(e_j\). Thus every finite passive word produces the same response
in both models, but any exterior factor with at least two values supplies a
boundary word and state at which the models differ.

Any decision procedure using passive traces alone receives identical input on
these two models, so it must return the same closure verdict for both. That
verdict is wrong for at least one model. \(\square\)

This is an identifiability theorem, not a claim that passive data are useless
under all stronger model assumptions.

## Theorem 5 — Finite boundary-blanket factorization

Let \(\alpha:S\to A\) be an inside summary and \(\beta:S\to B\) be a
boundary summary. If every permitted response factors through the pair:

\[
R(s,w)=F_w(\alpha(s),\beta(s))
\qquad
\forall s\in S,\;w\in\mathcal L,
\]

then \((\alpha,\beta)\) is a sound interface and

\[
\boxed{
K_{\mathcal L}
\le
\log_2|\operatorname{im}\alpha|
+
\log_2|\operatorname{im}\beta|.
}
\]

### Proof

Equal pairs \((\alpha(s),\beta(s))\) produce equal response for every allowed
word by the stated factorization. Hence the pair map is sound. Its image has at
most \(|\operatorname{im}\alpha||\operatorname{im}\beta|\) values. \(\square\)

This is the positive counterpart to the no-go theorem. A system is not closed
because the outside disappears; it is safely compressible when the outside's
future effect admits a finite sufficient boundary summary.

## Canonical certificate family

`causal_model.addressable_completion_bounds` implements a finite response family
with

\[
R((i,e_1,\ldots,e_q),\mathrm{observe})=(i),
\]

and

\[
R((i,e_1,\ldots,e_q),\mathrm{read}:j)=(i,e_j).
\]

It provides:

- `SeparatingWordCertificate`: a concrete read word for every unequal pair of
  product states;
- `AddressableCompletionProductCertificate`: exact passive, closed, and open
  quotient counts and the closed/open gap;
- `PassiveClosureNonidentifiabilityCertificate`: a passive-indistinguishable
  closed/open model pair; and
- `FiniteBoundaryBlanketCertificate`: a constructive finite blanket for a
  declared subset of active exterior coordinates.

The finite checks replay certificate definitions for selected finite factor
families. The proofs above establish the all-cardinality statements; enumeration
is not the reason the inequalities hold.

## Ecological projection

The theorem does **not** say that every external variable must be remembered.
An exterior process contributes to the lower bound only when a declared future
boundary event can operationally expose it independently.

In ecology, possible candidates for \(E_j\) include dispersal sources, delayed
mutualists, pathogen reservoirs, nutrient inflow regimes, or neighboring
communities. They count only if the admissible counterfactual grammar contains
an intervention, reconnection, or future event whose window response decodes
their distinct state.

The mathematical conclusion is therefore sharper than “ecosystems are complex”:

\[
\boxed{
\text{simple law in every fixed closed community}
\not\Rightarrow
\text{small shared law under open ecological composition}.
}
\]

The cause can be the independently addressable future exterior, even under a
constant local grammar, pairwise messages, and bounded degree.
