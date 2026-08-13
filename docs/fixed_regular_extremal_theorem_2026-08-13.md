# Fixed-regular open-composition extremal theorem — 2026-08-13

> **Status:** analytic aggregation of the strongest existing CCOC relay results. This is not a new witness family and does not assign novelty to regular-language restriction, finite-state minimization, binary routing, bounded-degree compilation, or generic locality. It packages the current construction into one theorem with one proof spine.

## Theorem

For every integer

\[
m\ge 1,
\]

there exists a finite deterministic synchronous controlled network \(N_m\) with comparison domain

\[
D_m=\{0,1\}^{m+1}
=\{(y,b_1,\ldots,b_m)\},
\]

and common primitive action alphabet

\[
A=\{0,1,\mathsf{fire},\mathsf{tick}\},
\]

such that the following statements hold simultaneously.

1. The closed future grammar is

   \[
   L_C=\{0,1,\mathsf{tick}\}^{*},
   \]

   and the open future grammar is

   \[
   L_O=A^{*}.
   \]

   Both are represented by one-state partial DFAs independent of \(m\), and opening adds exactly one primitive transition, the loop labelled \(\mathsf{fire}\). The controlled network and its transition rule are otherwise unchanged; only the declared legal future grammar changes.

2. The exact closed response quotient on \(D_m\) has

   \[
   |P_C|=2,
   \qquad
   K_C=1.
   \]

3. The exact open response quotient on \(D_m\) is discrete:

   \[
   |P_O|=2^{m+1},
   \qquad
   K_O=m+1.
   \]

4. Consequently the open-only response innovation is

   \[
   \iota_{\rm new}=K_O-K_C=m,
   \]

   and this attains the absolute finite-domain upper bound.

5. The interaction graph is a tree, the focal node is separated from the entire exterior relay body by one edge, the maximum degree is at most three, and the local state/message alphabets are bounded independently of \(m\).

6. If the relay tree is midpoint-balanced, every exterior coordinate can be read by a canonical legal open word and the worst such word has exact length

   \[
   L_{\rm query}^{\rm worst}
   =2\lceil\log_2m\rceil+2.
   \]

Thus a single fixed four-symbol grammar schema and a one-edge focal/exterior physical cut coexist with an exact closed/open interface gap of \(m\) bits.

---

## Proof

### Step 1 — fixed grammar and total local dynamics

Use the midpoint-balanced binary relay topology with \(m\) terminal memory leaves. Add one focal node `ROOT` above the relay-body root. The selector state records one currently selected relay-body node. The permanent memory at leaf \(j\) is \(b_j\), and the focal output is \(y\).

The closed grammar has one state with loops on `0`, `1`, and `tick`; `fire` is undefined. The open grammar adds the single missing `fire` loop. Hence both grammar descriptions are constant size and independent of \(m\). The underlying controlled transition function is the same in the closed and open comparisons; grammar enlargement changes legality, not the plant.

The controlled dynamics are total on the common four-symbol alphabet. Address symbols move the selector down one local child edge when possible and stutter at a leaf. `fire` creates a pulse only at a selected memory leaf. Every global action advances the pulse layer by one radius-one synchronous round. At an internal relay, simultaneous child pulses are combined by a fixed Boolean-OR rule. None of these local rules uses \(m\), a global quiescence oracle, a depth counter, or an \(m\)-valued port identifier.

This establishes the fixed grammar and fixed local-rule part of the theorem.

### Step 2 — closed all-word invariant

Start from any comparison state \((y,b_1,\ldots,b_m)\in D_m\), embedded as a pulse-free relay configuration with the selector at the relay-body root.

We claim that after any closed action

\[
a\in\{0,1,\mathsf{tick}\},
\]

three properties are preserved:

1. every permanent memory bit \(b_j\);
2. the focal output \(y\);
3. the absence of every pulse.

No closed action is `fire`, so no memory leaf emits a pulse. If the current pulse layer is empty, every child-to-parent message is empty. Therefore each relay stores the empty pulse at the next round and `ROOT` receives no pulse, so its output remains unchanged. Address actions can change only the selector position.

This proves the one-step invariant. Induction on word length gives the invariant for every

\[
w\in L_C.
\]

Therefore every closed response trace depends only on \(y\), never on \((b_1,\ldots,b_m)\). Hence states with the same \(y\) are closed-equivalent. The empty word/current output distinguishes \(y=0\) from \(y=1\). Thus

\[
|P_C|=2,
\qquad
K_C=1.
\]

### Step 3 — every exterior coordinate is legally addressable after opening

Let leaf \(j\) have actual left/right address

\[
a_j\in\{0,1\}^{d_j},
\]

where \(d_j\) is its depth below the relay-body root. Because the memory sites are terminal leaves, these addresses are prefix-free.

Define

\[
w_j
= a_j\,\mathsf{fire}\,\mathsf{tick}^{d_j+1}.
\]

This word is legal in \(L_O=A^*\). The prefix \(a_j\) moves the selector to leaf \(j\). Before `fire`, the pulse layer is still empty by the same invariant argument. `fire` writes the permanent bit \(b_j\) into the selected leaf pulse. The following \(d_j+1\) ticks move that pulse one parent edge per round from the leaf to `ROOT`. Therefore

\[
\operatorname{finaloutput}(s,w_j)=b_j.
\]

The permanent memory vector is unchanged and the canonical probe returns the pulse layer to quiescence.

Thus every exterior coordinate has a legal future decoder word.

### Step 4 — the open quotient is discrete

Take two distinct states

\[
s=(y,b_1,\ldots,b_m),
\qquad
t=(y',b'_1,\ldots,b'_m).
\]

If \(y\ne y'\), the empty word/current output distinguishes them. Otherwise \(y=y'\), so because \(s\ne t\), some exterior coordinate satisfies \(b_j\ne b'_j\). The legal open word \(w_j\) returns different final focal outputs on the two states.

Hence every distinct pair of states in \(D_m\) is separated by an open legal word. Therefore the open response quotient is discrete:

\[
|P_O|=|D_m|=2^{m+1},
\qquad
K_O=m+1.
\]

### Step 5 — exact capacity sharpness

The innovation created by opening is

\[
\iota_{\rm new}=K_O-K_C=(m+1)-1=m.
\]

For any refinement of a two-class quotient on a domain of size \(2^{m+1}\), the additional exact response memory cannot exceed

\[
\log_2|D_m|-\log_2|P_C|
=(m+1)-1
=m.
\]

The relay attains this upper bound with equality. Therefore its open-only innovation has zero finite-domain memory slack.

Equivalently, if the focal bit \(y\) is supplied separately, any exact exterior response label valid on \(D_m\) must distinguish all \(2^m\) exterior bit vectors: otherwise two states with the same \(y\) and the same exterior label but different \(b_j\) would be separated by \(w_j\). Hence at least \(m\) exterior response bits are forced.

### Step 6 — bounded locality and one-edge physical cut

The relay body is a binary tree. Adding `ROOT` above its body root preserves acyclicity. Every non-root graph node has exactly one parent edge, so the undirected interaction graph has \(|V|-1\) edges and is a tree.

`ROOT` has exactly one relay-body child. Removing that one edge disconnects `ROOT` from every memory leaf. Thus

\[
\text{focal--exterior edge cut}=1
\]

for every \(m\).

A binary relay has degree at most three: one parent and at most two children. The selector augmentation and pulse update do not add graph edges. The relay, memory-leaf, pulse, selector, and focal alphabets are fixed finite alphabets independent of \(m\). In the executable construction the selector-augmented relay alphabet has at most 6 states, the selector-augmented leaf alphabet at most 12 states, and the pulse/message alphabet 3 symbols. Therefore maximum degree and local state/message sizes remain uniformly bounded.

### Step 7 — exact canonical access length

Let

\[
H(m)
\]

be the maximum body-root-to-leaf selector depth of the midpoint-balanced tree. The recurrence is

\[
H(1)=0,
\]

and for \(m>1\),

\[
H(m)=1+\max\{H(\lfloor m/2\rfloor),H(\lceil m/2\rceil)\}.
\]

Induction gives

\[
H(m)=\lceil\log_2m\rceil.
\]

A probe for a leaf at depth \(d_j\) uses \(d_j\) address symbols, one `fire`, and \(d_j+1\) propagation ticks, for total length

\[
2d_j+2.
\]

Taking the deepest leaf gives

\[
L_{\rm query}^{\rm worst}
=2H(m)+2
=2\lceil\log_2m\rceil+2.
\]

All six theorem clauses now follow. \(\square\)

---

## Corollary 1 — narrow physical boundary is not an exact causal-compression bound

Within this explicit family, the focal/exterior graph cut stays equal to one and the interaction graph stays a tree, while the exterior response information forced by the open grammar grows as

\[
\log_2 |B_m|\ge m
\]

for any exact comparison-domain exterior summary used together with the focal bit.

Therefore bounded physical cut width, bounded degree, acyclicity, and treewidth one do not by themselves upper-bound exact open-system response memory.

This is a derived mathematical corollary of the relay, not a claim that a real ecological corridor or sparse interaction network realizes the witness.

## Corollary 2 — no static-resource-only bound on exact interface inflation

Consider the class of finite deterministic synchronous controlled networks satisfying all of the following uniform resource bounds:

- primitive action alphabet size at most 4;
- closed and open legal grammars represented by one-state partial DFAs;
- closed/open grammar edit distance at most one transition;
- maximum graph degree at most 3;
- focal/exterior edge cut at most 1;
- local node-state alphabet size at most 12 and local pulse/message alphabet size at most 3;
- radius-one local updates.

There is **no finite universal constant** depending only on those resource bounds that upper-bounds

\[
K_O-K_C
\]

throughout the class.

### Proof

Every \(N_m\) constructed above belongs to this class with the same resource constants, but

\[
K_O(N_m)-K_C(N_m)=m.
\]

If a finite resource-only upper bound \(C\) existed, choosing \(m>C\) would contradict the equality above. Hence no such bound exists. \(\square\)

Equivalently, exact response-interface complexity is not uniformly controlled by physical cut width, bounded degree, local alphabet size, action alphabet size, and the number of edited grammar transitions alone. A one-transition change in legal future behavior can expose an arbitrarily large amount of dormant exact response information while every listed local/static resource stays fixed.

This corollary is a no-go consequence of the explicit family, not a historical firstness claim.

## Corollary 3 — logarithmic access is order-optimal under the broader bounded-local contract

The general causal-cone theorem in `docs/local_causal_cone_bound.md` says that, for maximum degree \(\Delta\), uniform local-state bound \(q\), radius-one updates, and horizon \(T\), the number \(N_T\) of exact focal response classes available from all legal words of length at most \(T\) obeys

\[
\log_2N_T
\le
|B_T(o)|\log_2q.
\]

For fixed \(\Delta\ge3\) and fixed \(q\), the radius-\(T\) ball grows at most exponentially in \(T\). Therefore exposing

\[
N_T=2^{\Theta(m)}
\]

classes requires

\[
T=\Omega(\log m).
\]

The fixed-regular relay has \(\Delta\le3\), a uniform local-state bound, and reaches its full

\[
2^{m+1}
\]

open quotient by horizon

\[
2\lceil\log_2m\rceil+2.
\]

Hence its access latency is order-optimal in the broader bounded-degree, bounded-local-state, radius-one class. The exact coefficient and additive constant remain architecture-specific; only the \(\Theta(\log m)\) order is general. \(\square\)

---

## What has actually been strengthened

Relative to the earlier relay package, the theorem now removes two hidden presentation dependencies simultaneously:

- the primitive action alphabet no longer grows with \(m\);
- the legal future grammar is no longer an enumerated \(m\)-dependent word family.

It also removes the power-of-two restriction on the explicit selector construction. The strongest witness therefore works for every positive \(m\) under one fixed regular grammar schema.

The remaining historical novelty gate is unchanged: issue #122 asks whether classical uniform sequential-machine compilation already provides a comparable simultaneous bounded-local realization package. If it does, the construction remains an explicit extremal equality witness, but its realization **existence** should not be described as historically first.

## Executable aggregation

The finite replay surface for this theorem is

```python
from causal_model.extremal_open_composition import (
    certify_fixed_regular_extremal_theorem,
)

cert = certify_fixed_regular_extremal_theorem(m)
assert cert.verify()
assert cert.innovation_slack_bits == 0
assert cert.focal_exterior_cut_width == 1
```

The executable certificate checks one supplied finite \(m\). It is not the proof of the quantified all-\(m\) theorem above.
