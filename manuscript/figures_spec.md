# Figure contract for the first CCOC paper

The paper uses four figures. Each figure has one job and must map directly to the theorem spine; no figure is allowed to become an extra theorem or empirical case study.

## Figure 1 — Same system, different future grammar

**Question answered:** Why can two states be equivalent in a closed context but not under an opened future?

**Panels**

A. One fixed controlled system with focal state/output and several dormant exterior modules.

B. Closed grammar: only the currently admissible pathway can affect the focal response. Multiple microstates collapse to the same exact response class.

C. Open grammar: one additional class of legal future actions makes previously dormant modules addressable, splitting the old response class.

D. Summary statement:

\[
\text{closed functional equivalence}\not\Rightarrow\text{open-future causal equivalence}.
\]

**Must show visually:** the physical plant is unchanged; only legal future actions change.

**Must not imply:** that all ecological openness destroys compression or that a real ecosystem is represented by the cartoon.

**Main-text location:** Sections 1–2.

---

## Figure 2 — Operational lower-bound mechanism

**Question answered:** What exactly forces the open response quotient to be large?

**Panels**

A. Comparison state written as

\[
(i,e_1,\ldots,e_q).
\]

B. A base decoder word \(r_0\) exposes \(i\); module-specific legal words \(r_j\) expose \(e_j\).

C. Two states differing in coordinate \(e_j\) are separated by \(r_j\).

D. Consequence:

\[
K_{\rm open}\ge \log_2|I|+\sum_j\log_2|E_j|,
\]

while a closed context that factors through \((I,E_j)\) remains small.

**Must show visually:** the lower bound is an operational distinguishability/injection argument, not an assumed additive decomposition.

**Main-text location:** Section 3.

---

## Figure 3 — One-action extremal bounded-local witness

**Question answered:** Can maximal interface inflation occur without growing local grammar, graph degree, or action alphabet?

**Panels**

A. Balanced binary relay tree with focal ROOT, selector, and dormant binary memory leaves \(b_1,\ldots,b_m\).

B. Closed grammar

\[
L_C=\{0,1,\mathsf{tick}\}^*
\]

with `fire` illegal. Closed quotient: \(|P_C|=2\).

C. Open grammar

\[
L_O=\{0,1,\mathsf{fire},\mathsf{tick}\}^*
\]

adds only `fire`. Query word

\[
a_j\,\mathsf{fire}\,\mathsf{tick}^{d_j+1}
\]

reads leaf \(j\).

D. Extremal result:

\[
|P_O|=2^{m+1},\qquad K_O-K_C=m,
\]

with degree \(\le3\), bounded local alphabets, one-edge focal/exterior cut, and worst query length

\[
2\lceil\log_2m\rceil+2.
\]

**Must show visually:** `fire` is the only newly legal primitive action; the underlying network and transition rules are unchanged.

**Must not claim:** historical firstness of bounded-local compilation.

**Main-text location:** Sections 4–5.

---

## Figure 4 — Portability versus forced split

**Question answered:** When can the old macro-law survive future expansion, and what is the local obstruction when it cannot?

**Panels**

A. Positive case: two microstates inside the same macro fiber receive a newly legal action with identical macro successor and output behavior. The fiber remains valid.

B. Nested-stage interpretation: embeddings preserve the same macro label and common macro dynamics.

C. Negative case: a newly legal word/action produces different traces or macro successors from two formerly merged states.

D. Decision rule:

\[
\text{new behavior uniform within old fibers}\Rightarrow\text{portability may hold},
\]

whereas

\[
\text{new behavior splits an old fiber}\Rightarrow\text{that merge is not portable}.
\]

**Main-text location:** Section 6 and Discussion.

---

## Production rules

- Figures are conceptual/mathematical, not empirical.
- Use the same symbols as the manuscript and supplement.
- No decorative panels without a theorem or interpretation role.
- Figure captions must state the claim boundary and avoid historical-priority wording.
- Figure 3 is the only detailed construction figure; Figures 1, 2, and 4 should stay visually simple.
