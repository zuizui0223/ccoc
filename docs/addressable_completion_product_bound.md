# Addressable-completion product bounds

> **Archive status.** This note is retained as a mathematical companion record.
> The manuscript source statement is [Portability core v1](portability_core_v1.md)
> and the proof/replay distinction is fixed in the
> [paper-core audit](paper_core_audit.md).

## Controlled response quotient

Let a finite deterministic controlled response system have state space \(S\), a
**declared** set of permitted words \(\mathcal L\), and response map

\[
R:S\times\mathcal L\to\mathcal Y.
\]

The response may be a full output trace. Define

\[
s\equiv_{\mathcal L}s'
\iff
\forall w\in\mathcal L,\quad R(s,w)=R(s',w),
\]

and

\[
K_{\mathcal L}=
\log_2\left|S/\equiv_{\mathcal L}\right|.
\]

A sound exact interface may merge states only inside one
\(\equiv_{\mathcal L}\)-class. Thus an injection into this quotient is a lower
bound for every sound interface.

## Operational addressability

Assume a declared **product-indexed subset** of states

\[
S^*\cong I\times E_1\times\cdots\times E_q.
\]

This set need not be transition-closed or reachable from an unspecified initial
state. For each coordinate, suppose a legal word and decoder exist such that for
every

\[
s=(i,e_1,\ldots,e_q)\in S^*,
\]

\[
d_0(R(s,r_0))=i,
\qquad
d_j(R(s,r_j))=e_j\quad(1\le j\le q).
\]

The same \(r_j\) and \(d_j\) must work uniformly over all values of the other
coordinates.

## Theorem 1 — Addressable-product lower bound

Under operational addressability,

\[
\boxed{
K_{\mathcal L}
\ge
\log_2|I|+
\sum_{j=1}^{q}\log_2|E_j|.
}
\]

### Proof

Take distinct \(s,s'\in S^*\). They differ in at least one coordinate. If the
inside coordinate differs, \(d_0\) gives distinct values on responses to
\(r_0\). Otherwise some exterior coordinate \(E_j\) differs, and \(d_j\) gives
distinct values on responses to \(r_j\). Hence no two distinct states in
\(S^*\) belong to the same \(\equiv_{\mathcal L}\)-class. There are
\(|I|\prod_j|E_j|\) such states. Taking base-two logarithms proves the
claim. \(\square\)

This is an injection proof driven by declared separating words; it is not a
state-counting assertion made without operational semantics.

## Theorem 2 — Closed/open extension--compression inequality

For each fixed closed context \(c\), suppose every permitted closed response
factors through \((i,e_c)\):

\[
R_c((i,e_1,\ldots,e_q),w)=F_{c,w}(i,e_c)
\qquad
\forall w\in\mathcal L_c.
\]

Then the projection

\[
(i,e_1,\ldots,e_q)\mapsto(i,e_c)
\]

is sound for the declared closed contract, so

\[
K_{\mathcal L_c}
\le
\log_2|I|+\log_2|E_c|.
\]

Combining these closed upper bounds with Theorem 1 yields

\[
\boxed{
K_{\mathrm{open}}-
\max_cK_{\mathcal L_c}
\ge
\sum_{j=1}^{q}\log_2|E_j|-
\max_c\log_2|E_c|.
}
\]

### When closed equality holds

The upper bound becomes equality only with an extra premise: the closed grammar
must contain words whose **closed responses** decode both \(I\) and \(E_c\).
Merely declaring that the open-system words \(r_0,r_c\) are syntactically allowed
is not enough when one has changed the response contract. The binary
coordinate/relay witness satisfies the stronger decoder premise and therefore
has

\[
K_{\mathcal L_c}=\log_2|I|+\log_2|E_c|.
\]

## Binary sharpness consequence

For \(|I|=2\) and \(|E_j|=2\) for all \(j\), the explicit relay-tree witness
has

\[
K_{\mathrm{closed}}=2,
\qquad
K_{\mathrm{open}}=q+1,
\qquad
K_{\mathrm{open}}-
\max_cK_{\mathcal L_c}=q-1.
\]

The witness keeps local node states, pulse alphabet, pairwise update rule, and
maximum degree bounded. The number of selectable ports grows with \(q\), so this
is not a constant-size global port alphabet claim.

## Grammar refinement monotonicity

For \(\mathcal L_1\subseteq\mathcal L_2\),

\[
\boxed{K_{\mathcal L_1}\le K_{\mathcal L_2}.}
\]

Indeed, equality of responses for every word in \(\mathcal L_2\) implies equality
for every word in its subset \(\mathcal L_1\). The larger grammar therefore
refines, rather than coarsens, the exact quotient.

## Finite replay boundary

`causal_model.operational_addressability` checks a literal controlled readout
witness: an injective product embedding, legal decoder words, concrete decoders,
and a **complete declared finite** word family for each closed context. It does
not infer the word family, the product representation, reachability, or an
ecological interpretation from data.

The finite replays substantiate the supplied witness. The all-cardinality theorem
is established by the symbolic injection proof above.

## Ecological reading

Potential exterior coordinates may be interpreted as sources, mutualists,
pathogen reservoirs, nutrient regimes, or neighbouring communities only after a
separate finite model contract declares state variables and legal future actions.
An exterior contributes to the lower bound only when a declared future boundary
word independently exposes its value. The theorem therefore does not say that
all external ecological variation must be retained, nor that any observed system
satisfies the model.
