# RACH promotion calculus

## One question behind the repository

RACH asks:

> **When may a rule discovered inside a finite observation window be promoted to a
> portable causal law, and which certificate is required for that promotion?**

A rule can be exactly correct at one level and still fail at the next. The
repository therefore treats promotion as a sequence of explicit proof
obligations, not as an informal jump from good local fit to general law.

Read [the theorem spine](theorem_spine.md) for the compact status of every
proved result and its boundary.

## Four failure modes, one joint condition, and one epistemic gate

| Axis | Invalid automatic promotion | What can go wrong | Exact RACH response |
|---|---|---|---|
| **Time** | specified local update \(\Rightarrow\) one long-run endpoint | cycles or multiple attractors | ranking, recurrent-cycle, or multistability certificate |
| **Outside memory** | small closed-context rule \(\Rightarrow\) small open rule | independently addressable exterior completions | separating-word product lower bound or dynamic blanket certificate |
| **Outside delay** | no difference within the present horizon \(\Rightarrow\) no future difference | a boundary event becomes legal only later | prefix-grammar delayed separator and horizon certificate |
| **Mechanism plurality** | small law per retained candidate \(\Rightarrow\) one universal deterministic law | candidates induce different macro transitions | universal-law agreement, candidate-safe law, or set-valued law |
| **Joint separation** | outside-memory bound + type bound \(\Rightarrow\) additive bound | the full completion/type product is unrealizable or not jointly addressable | concrete pairwise structural separator for each joint state pair |
| **Evidence gate** | convenient selected model \(\Rightarrow\) justified retained family | data or solver pruning discarded a live mechanism | simultaneous retained-family coverage; otherwise `UNRESOLVED` |

The first five rows are mathematical structure once a finite theorem domain is
declared. The evidence gate is epistemic: it controls which candidate families
may honestly enter the structural theorems.

## The central objects

Let \(W\) be an observation window. Its outside is not merely the geographic
exterior of a plot. It is a declared boundary contract:

\[
(W,\Gamma,C),
\]

where

- \(\Gamma\) is a grammar of admissible exterior completions, attachments,
  events, and future actions; and
- \(C\) is a retained candidate family of mechanisms or completion models.

For candidate \(	heta\), completion \(e\), and legal boundary word
\(w\in\Gamma^*\), write the window trace as

\[
R_W^	heta(x,e,w).
\]

A portable deterministic law must say which summary replaces the hidden outside,
how that summary updates under future legal actions, and whether this induced
macro transition is common across the intended candidate family.

Closure therefore means neither “the outside does not exist” nor “nothing
entered while we watched.” It means that, under a declared grammar, the outside
has a dynamically sufficient summary and the desired macro transition is
well-defined at the intended candidate level.

## The theorem spine in one diagram

```text
finite observation window W
        |
        +-- passive traces
        |       |
        |       +-- completion no-go:
        |               same passive trace, different future boundary response
        |
        +-- declared exterior grammar Gamma
        |       |
        |       +-- addressable-completion lower bounds
        |       +-- dynamic-blanket upper bounds
        |       +-- grammar-aware finite horizons for fixed systems
        |       +-- delayed no-uniform-horizon families
        |
retained candidate family C
        |
        +-- candidate-specific dynamic interfaces q_theta
        |       |
        |       +-- common induced maps -> universal deterministic open law
        |       +-- distinct maps + type retained -> candidate-safe open law
        |       +-- distinct maps + type forgotten -> set-valued law / UNRESOLVED
        |
        +-- joint realizable product I x E_1 x ... x E_q x R
                |
                +-- concrete joint separators -> additive joint lower bound

local transition rules
        |
        +-- time promotion -> closure / recurrence / multistability certificates
```

The coordinate extension/compression witness and relay-tree compilation are one
concrete exterior grammar inside this picture. They do not claim that all open
ecosystems have a binary tree structure.

## What is now proved

### 1. Exterior memory cannot be ignored by closed-context compression

For operationally addressable coordinates

\[
I	imes E_1	imes\cdots	imes E_q,
\]

concrete future separating words imply

\[
K_{\mathrm{open}}
\ge
\log_2|I|+
\sum_j\log_2|E_j|.
\]

If every fixed closed context reads only one coordinate, the open versus closed
interface gap is bounded below by the omitted coordinate information. The binary
relay family realizes the sharp values

\[
K_{\mathrm{open}}=q+1,
\qquad
\max_iK_{\mathrm{closed},i}=2.
\]

### 2. Finite dynamic blankets are the positive criterion

A summary is an exact open macro-interface only when it is output preserving and
update closed under every permitted action. If

\[
q=(\alpha,eta)
\]

is such a dynamic inside-plus-boundary summary, then

\[
K_{\mathrm{open}}
\le
\log_2|\operatorname{im}q|
\le
\log_2|I|+\log_2|B|.
\]

The canonical all-word quotient is the coarsest exact deterministic interface.
For each fixed finite controlled system it stabilizes after a finite horizon.

### 3. A finite horizon is not uniform across delayed outside families

For every memory scale \(m\) and delay \(H\), the delayed-addressability family
has

\[
\max_iK_{\mathrm{closed},i}=2,
\qquad
K_{\mathrm{open}}=m+1,
\qquad
H_\star=H+1.
\]

No legal trace before \(\mathrm{wait}^H\mathrm{fire}\) can expose the relevant
exterior bit. Hence no fixed finite-horizon trace procedure certifies closure
uniformly over the union of such delayed families.

### 4. Candidate-specific laws do not automatically form a universal law

For a retained candidate family on shared macrostate space \(Q\), a universal
deterministic law exists exactly when

\[
G_a^	heta=G_a^{	heta'}
\quad
orall	heta,	heta',a.
\]

When the induced maps disagree, candidate identity cannot be silently discarded.
Under uniform response separation,

\[
K_{\mathrm{candidate	ext{-}safe}}
\ge
\log_2|Q|+\log_2R.
\]

Forgetting response type yields the set-valued law

\[
F_a(q)=\{G_a^	heta(q):	heta\in C\}.
\]

It is deterministic if and only if all retained response types agree.

### 5. Joint open laws require two kinds of agreement

For candidate-specific dynamic interfaces

\[
q_	heta:S_	heta	o Q,
\]

a universal deterministic open law exists exactly when every \(q_	heta\) is
output preserving and update closed, all candidates share the same macro output
map, and

\[
G_a^	heta=G_a^{	heta'}
\quad
orall	heta,	heta',a.
\]

Thus boundary sufficiency and mechanism invariance remain separate proof
obligations.

For jointly realizable states

\[
I	imes E_1	imes\cdots	imes E_q	imes R,
\]

an additive lower bound is valid only when every unequal pair has a concrete
legal joint separator. Under that condition,

\[
oxed{
K_{\mathrm{joint	ext{-}safe}}
\ge
\log_2|I|+
\sum_j\log_2|E_j|+
\log_2|R|.
}
\]

The canonical witness attains equality with a constant local alphabet
\(\{\mathrm{observe},\mathrm{read},\mathrm{intervene}\}\). Port choice is
structural and response type changes the `intervene` transition; neither enters
as a growing action label.

## The law-reporting rule

RACH's output is determined by the strongest certificate actually present.

| What has been certified | Reportable output |
|---|---|
| fixed candidate, fixed grammar, exact dynamic summary | candidate-specific deterministic open law |
| common dynamic interfaces and common induced maps across candidates | universal deterministic open law |
| common dynamic interfaces but multiple retained response types | candidate-safe deterministic open law on an augmented state |
| response type omitted while candidate transitions disagree | set-valued law or `UNRESOLVED` |
| exterior separator or delayed separator violates the proposed summary/horizon | no closure certificate at that scale; report the counterexample or lower bound |
| no joint separator for a proposed product | do not claim additive exterior-plus-mechanism memory |

This avoids two opposite mistakes: declaring a universal law from one convenient
candidate, and declaring the entire problem hopeless when a rigorous set-valued
or candidate-safe statement remains available.

## Observation-regime comparison is a special case

`observation_regime_closure.py` compares two declared action regimes on the same
state space. In the promotion calculus it is one operational way to alter the
boundary grammar; it is not a generic statement that observing an ecosystem
necessarily changes it.

## What remains outside the current theorem core

The current results are conditional on finite labelled deterministic systems,
explicit state spaces, action alphabets, grammars, and retained candidate
families. They do not prove corresponding results for arbitrary continuous,
stochastic, hidden-state, simultaneous, or empirical systems.

The general bridge

\[
	ext{data or solver output}
\longrightarrow
	ext{retained completion/mechanism family}
\longrightarrow
	ext{candidate-safe open-law verdict}
\]

is not implemented yet. Existing evidence modules remain staging for that
bridge; they must not be presented as if they already infer an exterior grammar.

## Next theorem targets

1. **Grammar-aware blanket factorization.** Extend dynamic blanket factorization
   to summaries over the finite product of system state and prefix-grammar state,
   rather than using grammar state only for finite-horizon stabilization.
2. **Joint micro-compilation.** Compile the multi-valued joint witness to a
   degree-three pairwise local protocol, or state the sharp restricted compiler
   theorem that is actually proved.
3. **Evidence bridge.** Connect data or solver output to retained completion and
   response-type families behind explicit coverage assumptions.

A larger coordinate table, a new provenance wrapper, or a generic statistical
backend unconnected to these objects is not a new core theorem.

## Boundary

RACH does not claim that every ecosystem has a finite-state representation, that
passive data are useless, or that arbitrary outside conditions can be exhausted.
Every result remains conditional on its declared observation window, action
grammar, completion family, candidate family, and certificate assumptions.
