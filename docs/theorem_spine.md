# RACH theorem spine: established results, exact limits, and frontier

## The promotion problem

RACH asks when a rule found in a finite observation window may be promoted to a
portable causal law. Promotion is not one yes/no jump:

\[
\boxed{
\text{local rule}
\to
\text{long-run rule}
\to
\text{open-boundary rule}
\to
\text{candidate-independent open rule}.
}
\]

Each arrow has a distinct proof obligation. A certificate at one level does not
silently certify the next.

## Promotion ladder

| Promotion to be justified | Failure mode | Exact RACH response | Primary module |
|---|---|---|---|
| Local update \(\to\) one long-run endpoint | cycles or multiple attractors | ranking, cycle, or multistability certificate | `causal_closure_calculus.py` |
| Passive window rule \(\to\) open-boundary rule | unseen exterior completion has a future separator | completion counterexample and open trace quotient | `observation_window_completion.py` |
| Small closed-context interface \(\to\) small open interface | independently addressable exterior coordinates | separating-word product lower bound | `addressable_completion_bounds.py` |
| Finite boundary summary \(\to\) exact open macro-law | summary fits now but fails to update | dynamic-interface / blanket certificate | `dynamic_boundary_blankets.py` |
| Fixed horizon \(\to\) family-wide closure certificate | a legal exterior event is delayed | prefix grammar and delayed separator | `delayed_addressability.py` |
| Candidate-specific law \(\to\) universal deterministic law | retained mechanisms induce different macro maps | response-type agreement or obstruction | `candidate_safe_laws.py` |
| Separate outside and candidate results \(\to\) additive joint law | joint states are unrealizable or not jointly separable | common-interface criterion plus structural joint separators | `joint_open_candidate_laws.py` |

The relay-tree compilation is a robustness result for selected-port witnesses:
it eliminates a high-degree or growing-local-lookup explanation. It is not a
claim that every ecological boundary has a tree topology.

## Established theorem package

### A. Time: local specification is not global closure

For a finite total deterministic update map \(F:S\to S\), the closure calculus
certifies global closure, recurrent nonclosure, or multistable nonclosure.

\[
\text{specified local transitions}
\not\Rightarrow
\text{one globally closing endpoint}.
\]

This is a finite deterministic-map theorem, not a claim that an empirical
ecosystem has one fully specified deterministic update map.

### B. Outside memory: passive agreement does not imply open equivalence

For the window-completion family with focal bit \(y\) and \(m\) exterior bits,

\[
K_{\mathrm{passive}}=1,
\qquad
K_{\mathrm{open}}=m+1.
\]

Passive traces can agree forever while a declared future boundary action
separates completions. The addressable product theorem extends this: for
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

For binary coordinates, the relay-tree family attains

\[
K_{\mathrm{open}}=q+1,
\qquad
\max_iK_{\mathrm{closed},i}=2.
\]

### C. Positive criterion: finite dynamic blankets

A static covariate list is not an exact open law. A summary \(q:S\to Q\) must
preserve output and update through every allowed action:

\[
h=\bar h\circ q,
\qquad
q(T(s,a))=\bar T_a(q(s)).
\]

The all-word trace quotient is the coarsest exact extension-stable deterministic
interface. If \(q=(\alpha,\beta)\) combines inside and boundary summaries,

\[
K_{\mathrm{open}}
\le
\log_2|\operatorname{im}q|
\le
\log_2|I|+\log_2|B|.
\]

For a fixed finite controlled system, its exact quotient stabilizes after a
finite counterfactual horizon. The binary addressable family shows that no
boundary blanket of uniformly bounded size works across every growing exterior
family.

### D. Outside delay: no uniform finite closure horizon

For every memory scale \(m\) and delay \(H\), delayed addressability gives

\[
\boxed{
\max_iK_{\mathrm{closed},i}=2,
\qquad
K_{\mathrm{open}}=m+1,
\qquad
H_\star=H+1.
}
\]

Before \(\mathrm{wait}^H\mathrm{fire}\), every allowed trace is exterior-blind.
The next legal word separates a completion. Thus

\[
\boxed{
\text{finite certificate for every fixed member}
\not\Rightarrow
\text{one finite horizon for the expanding delayed family}.
}
\]

The attached reader selects its port structurally; it is not a growing action
symbol.

### E. Mechanism plurality: instance laws are not universal laws

Let candidate \(\theta\) induce maps \(G_a^\theta:Q\to Q\) on shared
macrostate space \(Q\). A candidate-independent deterministic macro-law exists
exactly when

\[
G_a^\theta=G_a^{\theta'}
\quad
\forall\theta,\theta',a.
\]

Under uniform response separation, an exact candidate-safe interface requires

\[
K_{\mathrm{candidate\text{-}safe}}
\ge
\log_2|Q|+\log_2R,
\]

where \(R\) is the number of distinct induced response types. If type is
forgotten, the exact prediction is set-valued:

\[
F_a(q)=\{G_a^\theta(q):\theta\in C\}.
\]

### F. Joint exterior–mechanism separation

The joint theorem first requires candidate-specific **dynamic** interfaces into
the same macrostate space. A universal deterministic open law exists if and only
if those interfaces have the same macro output map and their induced transition
maps agree across every retained candidate.

This separates two obligations:

\[
\underbrace{q_\theta\text{ is update-closed}}_{\text{outside compression}}
\qquad\text{and}\qquad
\underbrace{G_a^\theta=G_a^{\theta'}}_{\text{mechanism invariance}}.
\]

For a jointly realizable product family

\[
I\times E_1\times\cdots\times E_q\times R,
\]

an additive lower bound is obtained only under **joint operational separation**:
every unequal product pair has one concrete legal future query that separates
its window traces. Then

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

The canonical structural witness attains equality. It uses one fixed local
alphabet \(\{\mathrm{observe},\mathrm{read},\mathrm{intervene}\}\):
`read` acts through a structural port attachment, and response type changes the
`intervene` transition rather than appearing as an action label.

The theorem does **not** infer additivity merely because the standalone exterior
and candidate theorems hold.

## What the combined spine says

A portable deterministic ecological macro-law needs, at the claimed level:

1. time validity;
2. a declared action and completion grammar;
3. an update-closed boundary summary for every retained candidate;
4. enough horizon to test the relevant legal grammar; and
5. common induced macro maps, unless response type is retained explicitly.

| Failure | Honest output |
|---|---|
| recurrence / multistability | nonclosure certificate |
| exterior separator | open-interface lower bound or closure no-go |
| summary fails update closure | no exact open deterministic interface at that summary |
| delayed legal separator | finite-horizon nonidentifiability |
| candidate transition disagreement | candidate-safe law, set-valued law, or `UNRESOLVED` |
| joint separation missing | no additive exterior-plus-mechanism lower bound claimed |

## What is not proved

The current spine does not establish that:

- arbitrary empirical ecosystems are finite deterministic systems;
- a geographic plot alone supplies the correct outside grammar;
- passive data are useless;
- finite replay proves a result beyond its declared grammar and state domain;
- every finite regular grammar has a low-dimensional dynamic blanket;
- a data-analysis pipeline retained every plausible completion or mechanism;
- every structural port grammar has a complete degree-three micro-compilation; or
- exterior and mechanism information always add without joint separation.

These boundaries are part of the results, not caveats to quietly delete.

## Next mathematical frontier

The strongest next target is a **grammar-aware dynamic blanket theorem**. The
current delay result treats grammar state in finite-horizon refinement, but the
positive blanket theorem does not yet characterize when a summary augmented with
finite grammar state is the coarsest exact open interface.

Two companion directions are:

1. a degree-three micro-compilation for the multi-valued joint witness; and
2. an evidence bridge from data or solvers to retained completion/mechanism
   families behind explicit coverage assumptions.

## Navigation

- [Promotion calculus](promotion_calculus.md): conceptual axis map.
- [Current architecture](current_architecture.md): code and certificate layers.
- [Asset map](repository_asset_map.md): active core versus gold and frozen assets.
- [Dynamic boundary blankets](dynamic_boundary_blankets.md): positive factorization.
- [Delayed addressability](delayed_addressability.md): delayed-horizon no-go.
- [Candidate-safe universal laws](candidate_safe_universal_laws.md): mechanism plurality.
- [Joint open-candidate laws](joint_open_candidate_laws.md): joint criterion and product witness.
