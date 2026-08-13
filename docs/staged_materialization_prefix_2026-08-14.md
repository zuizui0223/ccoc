# Staged materialization: prefix resource criterion

Let \(E=(E_1,\ldots,E_m)\) be independent uniform binary exterior coordinates. A closed representation \(C\) has at most \(2^k\) states. At stages \(t=1,\ldots,r\), nested coordinate sets \(S_t\) must be available after that stage. If stage \(q\) contributes at most \(c_qT_q\) boundary symbols from an alphabet of size \(s_q\), then every prefix obeys

\[
\boxed{
k+\sum_{q=1}^{t}c_qT_q\log_2s_q
\ge
|S_t|-\sum_{j\in S_t}h_2(\varepsilon_{j,t}).}
\]

Here \(\varepsilon_{j,t}\le1/2\) is the decoding error for coordinate \(j\in S_t\) after stage \(t\). Thus staged portability imposes all prefix constraints, not only the terminal total budget.

## Proof

Let \(U_q\) be the stage-\(q\) boundary history and \(W_t=(C,U_1,\ldots,U_t)\). Since the coordinates in \(S_t\) are independent uniform bits,

\[
H(E_{S_t})=|S_t|.
\]

Coordinate-wise Fano and conditional-entropy subadditivity give

\[
H(E_{S_t}\mid W_t)
\le
\sum_{j\in S_t}h_2(\varepsilon_{j,t}),
\]

so

\[
I(E_{S_t};W_t)
\ge
|S_t|-\sum_{j\in S_t}h_2(\varepsilon_{j,t}).
\]

On the resource side, \(H(C)\le k\). The stage-\(q\) boundary history has at most \(s_q^{c_qT_q}\) possible values. By the entropy chain rule,

\[
H(U_1,\ldots,U_t\mid C)
\le
\sum_{q=1}^{t}c_qT_q\log_2s_q.
\]

Hence

\[
I(E_{S_t};W_t)
\le H(W_t)
\le
k+\sum_{q=1}^{t}c_qT_q\log_2s_q.
\]

Combining the two bounds proves the theorem. \(\square\)

For a common stage-\(t\) error ceiling \(\varepsilon_t\),

\[
\boxed{
k+\sum_{q=1}^{t}c_qT_q\log_2s_q
\ge |S_t|\bigl(1-h_2(\varepsilon_t)\bigr).}
\]

## Exact power-of-two subclass: necessity and sufficiency

Take

\[
S_t=\{1,\ldots,m_t\},
\qquad
m_1\le\cdots\le m_r=m,
\]

zero error, and \(s_t=2^{b_t}\). Write

\[
L_t=c_tT_tb_t
\]

for the number of binary symbol positions available at stage \(t\). Then an exact staged materialization exists **if and only if**

\[
\boxed{k+\sum_{q=1}^{t}L_q\ge m_t\qquad\forall t.}
\]

Necessity is the zero-error prefix theorem.

For sufficiency, retain the first \(k\) coordinates. Each remaining bit \(E_j\), \(j>k\), has deadline

\[
d(j)=\min\{t:m_t\ge j\}.
\]

By stage \(t\), exactly

\[
\max\{0,m_t-k\}
\]

unretained bits have deadlines at or before \(t\). The prefix condition is equivalent to

\[
\sum_{q=1}^{t}L_q\ge\max\{0,m_t-k\}
\qquad\forall t.
\]

Allocate available binary positions in earliest-deadline order. If some deadline \(t\) were missed, more than \(\sum_{q\le t}L_q\) unretained bits would have deadlines at or before \(t\), contradicting the prefix condition. Thus every coordinate required at stage \(t\) is available by that stage. Grouping each stage's assigned bits into \(b_t\)-bit symbols realizes the declared power-of-two boundary resources.

Therefore the prefix inequalities completely characterize exact feasibility in this subclass. \(\square\)

## Path-independent memory versus prefix-sensitive installation

The terminal-grammar theorem says the minimum size of one exact interface valid across a globally-new-symbol grammar chain depends only on the terminal canonical quotient. The present result asks a different question: whether enough information can be installed by each intermediate deadline.

Take four exterior bits, no pre-retention \(k=0\), and two stages whose cumulative binary capacities are

\[
(1,4).
\]

Two exposure profiles have the same final four-bit requirement:

- \((m_1,m_2)=(1,4)\) is feasible;
- \((m_1,m_2)=(3,4)\) is infeasible because the first prefix requires three bits but only one position is available.

Both have the same terminal memory requirement and the same total four positions. The difference is only **when** the distinctions become operationally required.

Thus

\[
\boxed{\text{terminal shared-memory capacity can be path-independent}}
\]

while

\[
\boxed{\text{online installation feasibility is prefix-sensitive}.}
\]

The exact iff was independently exhaustively checked for small cases with up to three stages and final \(m\le5\); no mismatch was found between the prefix criterion and direct assignment feasibility. This computation is supporting falsification, not the proof.

## Relation to CCOC

This result joins three existing components:

1. terminal canonical memory for a grammar chain;
2. retention/update information debt;
3. finite boundary installation time.

A macro-interface can therefore be large enough in principle yet fail as an **online portable interface** because its required distinctions are exposed faster than the boundary can install them.

## Claim discipline

Fano, finite-alphabet entropy counting, and the unit-job deadline argument are classical substrate. The CCOC-specific content is the coupled open-composition interpretation: grammar exposure creates staged causal-information deadlines, and finite boundary throughput turns those deadlines into a complete exact feasibility criterion in the binary power-of-two subclass.
