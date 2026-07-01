# RACH theorem spine: established results, exact limits, and frontier

## The one promotion problem

RACH asks when a rule found in a finite observation window may be promoted to a
portable causal law. The answer is not a single yes/no test. A promotion can
fail along distinct axes:

\[
\boxed{
\text{local rule}
\to
\text{long-run rule}
\to
\text{open-boundary rule}
\to
\text{candidate-independent rule}.
}
\]

Each arrow needs its own certificate. A certificate on one arrow does not
silently certify the others.

This document is the current research entrance. It records **what has actually
been proved in the repository's finite deterministic domains**, what those
results do not say, and the next mathematical frontier.

## The promotion ladder

| Promotion to be justified | What can fail | Exact RACH response | Primary module |
|---|---|---|---|
| Local update \(\to\) one long-run endpoint | cycles or multiple attractors | ranking, cycle, or multistability certificate | `causal_closure_calculus.py` |
| Passive window rule \(\to\) open-boundary rule | an unseen exterior completion has a future separator | completion counterexample and open trace quotient | `observation_window_completion.py` |
| Small closed-context interface \(\to\) small open interface | independently addressable exterior coordinates | separating-word product lower bound | `addressable_completion_bounds.py` |
| Finite boundary summary \(\to\) exact open macro-law | summary predicts now but fails to update under a future action | dynamic-interface / blanket factorization certificate | `dynamic_boundary_blankets.py` |
| Fixed finite horizon \(\to\) family-wide closure certificate | a legal exterior event is delayed | delayed grammar and delayed separator | `delayed_addressability.py` |
| Candidate-specific law \(\to\) universal deterministic law | retained mechanisms induce different macro transitions | response-type agreement or obstruction certificate | `candidate_safe_laws.py` |

The relay-tree compilation is not another arrow. It protects the
extension/completion witnesses from an implementation objection: their lower
bounds persist under one constant local grammar, pairwise messages, and maximum
degree three.

## Established theorem package

### A. Time: local specification is not global closure

For a finite total deterministic update map \(F:S\to S\), the closure calculus
classifies the system as exactly one of global closure, recurrent nonclosure, or
multistable nonclosure. The certificates are respectively a strict descending
ranking, a directed cycle, or distinct fixed points.

\[
\text{specified local transitions}
\not\Rightarrow
\text{one globally closing endpoint}.
\]

This is a theorem about finite deterministic maps. It is not an assertion that
an empirical ecosystem has one deterministic update map.

### B. Outside memory: passive agreement does not imply open equivalence

For the observation-window family with focal bit \(y\) and \(m\) exterior bits,

\[
K_{\mathrm{passive}}=1,
\qquad
K_{\mathrm{open}}=m+1.
\]

Passive traces can agree forever while a declared future boundary action
separates completions. This is an existence no-go: no passive-trace-only rule can
certify closure for every member of a model class containing that family.

The addressable product theorem generalizes the memory lower bound. For
operationally readable coordinates

\[
I\times E_1\times\cdots\times E_q,
\]

concrete separating words imply

\[
\boxed{
K_{\mathrm{open}}
\ge
\log_2|I|+
\sum_{j=1}^{q}\log_2|E_j|.
}
\]

If a fixed closed context reads only \(E_c\), then

\[
\boxed{
K_{\mathrm{open}}-
\max_cK_{\mathrm{closed},c}
\ge
\sum_j\log_2|E_j|-
\max_c\log_2|E_c|.
}
\]

For binary coordinates, the coordinate and relay-tree families attain equality:

\[
K_{\mathrm{open}}=q+1,
\qquad
\max_cK_{\mathrm{closed},c}=2.
\]

### C. Positive criterion: finite dynamic blankets

A static external covariate list is not an exact open law. A summary \(q:S\to Q\)
must preserve current output and update through every permitted action:

\[
h=\bar h\circ q,
\qquad
q(T(s,a))=\bar T_a(q(s)).
\]

The all-word trace quotient is the coarsest exact extension-stable deterministic
interface. If \(q=(\alpha,\beta)\) combines inside and boundary summaries, then

\[
\boxed{
K_{\mathrm{open}}
\le
\log_2|\operatorname{im}q|
\le
\log_2|I|+\log_2|B|.
}
\]

For a fixed finite controlled system, its exact quotient stabilizes after a
finite counterfactual horizon:

\[
H_\star\le |\operatorname{im}q|-1.
\]

The lower and upper bounds meet in the addressable binary family. Any exact
blanket there requires

\[
\boxed{
\log_2|B_m|\ge m.
}
\]

Thus a finite blanket may exist for each fixed system while no blanket of size
bounded independently of the exterior-family scale exists.

### D. Outside delay: no uniform finite closure horizon

The delayed-addressability family has independent memory and delay parameters.
For every \(m\ge1\) and \(H\ge0\), a prefix grammar with local symbols
`wait` and `fire` yields

\[
\boxed{
\max_iK_{\mathrm{closed},i}=2,
\qquad
K_{\mathrm{open}}=m+1,
\qquad
H_\star=H+1.
}
\]

Before the legal word \(\mathrm{wait}^{H}\mathrm{fire}\), all exterior
completions are trace-indistinguishable. At that next legal word, the structural
reader attachment exposes the exterior bit.

Therefore

\[
\boxed{
\text{finite certificate for every fixed grammar member}
\not\Rightarrow
\text{one finite horizon for the whole delayed family}.
}
\]

The port is structural in the degree-three relay realization; it is not injected
as a growing action alphabet.

### E. Mechanism plurality: instance laws are not universal laws

Let a retained candidate family share an observable macrostate space \(Q\), and
let candidate \(\theta\) induce maps \(G_a^\theta:Q\to Q\).

A candidate-independent deterministic macro-law exists exactly when

\[
\boxed{
G_a^\theta=G_a^{\theta'}
\quad
\forall\theta,\theta',a.
}
\]

The identity/flip witness has a one-bit exact law in every candidate but no
universal deterministic intervention law.

Define response type by equality of all induced candidate maps. Under **uniform
response separation**—every pair of response types has a concrete future-word
separator from every shared macrostate—an exact candidate-safe deterministic
interface requires

\[
\boxed{
K_{\mathrm{candidate\text{-}safe}}
\ge
\log_2|Q|+
\log_2R,
}
\]

where \(R\) is the number of response types.

The candidate-forgetting prediction is instead the set-valued law

\[
F_a(q)=\{G_a^\theta(q):\theta\in C\}.
\]

It is deterministic exactly when all retained response types agree. Delayed
candidate discrimination shows that this disagreement can remain hidden until an
arbitrarily late legal boundary event.

## What the combined spine says

A portable deterministic ecological macro-law needs more than a good fit inside
a plot or window. In the finite deterministic theorem domain, it needs all of
the following at the intended claim level:

1. **time validity:** no unresolved recurrence or multistability obstruction;
2. **boundary validity:** a declared action/completion grammar;
3. **outside compression:** an exact dynamically update-closed blanket;
4. **horizon adequacy:** enough of the declared grammar has been queried to
   distinguish the relevant quotient; and
5. **mechanism invariance:** retained candidates induce the same macro maps, or
   the response type is retained explicitly.

Failure at any one stage has a different honest output:

| Failure | Honest mathematical output |
|---|---|
| recurrence / multistability | nonclosure certificate |
| exterior separator | open-interface lower bound or closure no-go |
| blanket does not update | no exact open deterministic interface at that summary |
| delayed legal separator | finite-horizon nonidentifiability |
| candidate transition disagreement | candidate-safe law, set-valued law, or `UNRESOLVED` |

## What is not proved

The current spine does **not** establish any of the following:

- that arbitrary empirical ecosystems are finite deterministic systems;
- that a geographic plot alone determines the right outside grammar;
- that passive data are useless;
- that a finite replay proves a claim beyond its declared grammar and state
  domain;
- that every finite regular grammar has a useful low-dimensional dynamic blanket;
- that a data-analysis pipeline has correctly retained every plausible ecological
  completion or mechanism; or
- that the separate exterior-memory and candidate-response lower bounds add
  without an explicit joint separation theorem.

These boundaries are part of the result, not caveats to be quietly removed.

## Next mathematical frontier

The next nontrivial theorem should not be another larger coordinate witness. The
best target is a **joint open-and-candidate law criterion**.

For a retained family of completion grammars and mechanisms, define a common
candidate-safe boundary interface and determine when one deterministic macro
transition survives after both exterior completion and candidate identity are
forgotten. A useful theorem must distinguish at least these cases:

\[
\begin{array}{rcl}
\text{one common dynamic blanket and one common map}
&\Rightarrow&
\text{universal open deterministic law},\\[4pt]
\text{common blanket but multiple response types}
&\Rightarrow&
\text{candidate-safe or set-valued open law},\\[4pt]
\text{no uniformly bounded blanket}
&\Rightarrow&
\text{open-memory obstruction}.\\
\end{array}
\]

The key difficulty is to state a non-circular **joint separation** assumption
under which exterior-memory and response-type information have an additive lower
bound. That is a theorem problem, not a documentation exercise.

The two other high-value routes are:

1. a grammar-aware dynamic-blanket factorization theorem for regular boundary
   languages; and
2. an evidence bridge from data or solvers to retained completion-grammar and
   response-type families.

## Navigation

- [Promotion calculus](promotion_calculus.md): conceptual axis map.
- [Current architecture](current_architecture.md): code and certificate layers.
- [Asset map](repository_asset_map.md): active core versus gold and frozen assets.
- [Dynamic boundary blankets](dynamic_boundary_blankets.md): positive
  factorization theorem.
- [Delayed addressability](delayed_addressability.md): delayed-horizon no-go.
- [Candidate-safe universal laws](candidate_safe_universal_laws.md):
  mechanism-plurality theorem.
