# RACH theorem spine: what is proved, what it means, and what comes next

## The central question

RACH asks when a rule obtained inside a finite observation window can be
promoted to a portable causal macro-law under declared future ecological
connections.

\[
\boxed{
\text{internal rule}
\not\Rightarrow
\text{portable open-system rule}.
}
\]

A promotion must separately survive time, future exterior completion, delayed
exposure, update closure, and retained mechanism variation. A certificate at one
level does not certify the others.

## The active theorem chain

### 1. Time: local updates need not give global closure

For a finite deterministic update map, the closure calculus gives an exact
certificate of one global endpoint, recurrence, or multistability.

\[
\text{local transition specification}
\not\Rightarrow
\text{one global endpoint}.
\]

This is the time prerequisite; it does not assume empirical ecosystems are fully
specified deterministic maps.

### 2. Open composition: compression and extension do not commute

For a reachable addressable product subsystem

\[
S^*\cong I\times E_1\times\cdots\times E_q,
\]

suppose the declared future grammar contains a concrete word that decodes the
inside coordinate and one concrete future word that decodes each exterior
coordinate. Then every unequal product pair has a future separator, so

\[
\boxed{
K_{\mathrm{open}}
\ge
\log_2|I|+\sum_{j=1}^{q}\log_2|E_j|.
}
\]

If each fixed closed context \(j\) factors through \((I,E_j)\), then

\[
K_{\mathrm{closed},j}
=
\log_2|I|+\log_2|E_j|,
\]

and therefore

\[
\boxed{
K_{\mathrm{open}}-
\max_j K_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-
\max_j\log_2|E_j|.
}
\]

This is the core **Extension–Compression Noncommutation Inequality**. It shows
that a small law for every fixed community does not yield one small interface
that remains correct after future species addition, removal, or reconnection.

The binary relay-tree family is sharp:

\[
K_{\mathrm{closed},j}=2,
\qquad K_{\mathrm{open}}=m+1,
\qquad \Delta=m-1.
\]

It uses one constant local grammar, pairwise messages, and maximum degree three.
Thus the gap does not require high-order interactions or growing local rule
complexity.

### 3. Positive side: an open law exists exactly through an update-closed blanket

A boundary summary \(q\) is exact only when it preserves output, enabled legal
actions, and successor summary under every legal action. In the ordinary
controlled form,

\[
h=\bar h\circ q,
\qquad
q(T(s,a))=\bar T_a(q(s)).
\]

For a finite grammar-aware contract, the summary is defined on physical state
and grammar state. Equal summaries must preserve current output, enabled action
sets, and successor summaries. The canonical legal-word quotient is coarsest.

\[
\boxed{
\text{outside can be ignored only when its future effect factors through a
finite update-closed boundary state.}
}
\]

This is the positive counterpart to the lower bound: the theory does not say
open laws never exist.

### 4. Delay and adaptive evidence: finite experiments do not certify closure

For each finite adaptive policy \(\Pi\) of depth \(D\), a delayed closed/open
pair can be chosen with gate delay \(H>D\) such that

\[
\operatorname{Transcript}_{\Pi}(M_{\mathrm{closed}})
=
\operatorname{Transcript}_{\Pi}(M_{\mathrm{open}}),
\]

but a later legal word separates them.

\[
|B_\Gamma(M_{\mathrm{closed}})|=1,
\qquad
|B_\Gamma(M_{\mathrm{open}})|=2^{2^\ell}.
\]

Hence no finite transcript-only adaptive procedure is both sound and complete
for exterior closure over an unbounded delayed-addressability family.

\[
\boxed{
\text{finite adaptive evidence without an independent horizon contract}
\Rightarrow \mathrm{UNRESOLVED},
\text{ not closure.}
}
\]

A uniform delay bound, finite grammar/address bound, and completion coverage
contract restore finite exhaustive certification.

### 5. Retained mechanisms: instance laws need not be universal laws

Candidate-specific dynamic interfaces can each be exact while their induced
macro maps disagree. A candidate-independent deterministic law exists exactly
when

\[
G_a^\theta=G_a^{\theta'}
\quad
\forall\theta,\theta',a.
\]

Otherwise the honest outputs are a candidate-safe interface retaining response
type, a set-valued law, or `UNRESOLVED`.

### 6. Joint exterior–mechanism claims require joint separation

Exterior memory and mechanism response type may be added only when jointly
realizable product states have concrete joint future separators. Under that
premise,

\[
K_{\mathrm{joint-safe}}
\ge
\log_2|I|+
\sum_j\log_2|E_j|+
\log_2|R|.
\]

Standalone exterior and candidate lower bounds do not automatically add.

## What has become clear

The theory now separates three logically different reasons that a portable law
can fail:

| Question | Exact result | Honest conclusion when it fails |
|---|---|---|
| Does the specified local system close over time? | closure / cycle / multistability certificates | nonclosure |
| Does closed-context compression survive future composition? | extension–compression lower bound | required interface grows with addressable exterior memory |
| Can finite adaptive evidence prove exterior closure? | delayed adaptive no-go | `UNRESOLVED` without independent bounds |
| Can outside be compressed at all? | dynamic grammar-aware blanket criterion | no exact deterministic macro-law at that summary |
| Do retained mechanisms share one macro transition? | universal-law criterion | candidate-safe, set-valued, or `UNRESOLVED` |

The ecological reversal is therefore precise:

\[
\boxed{
\text{macro-law failure need not mean local ecology is complicated.}
}
\]

\[
\boxed{
\text{It can mean that future-connectable modules are separately addressable.}
}
\]

## Scope boundaries

Nothing here proves that arbitrary ecosystems are finite deterministic systems,
that a plot supplies the correct exterior grammar, or that a finite replay proves
claims beyond its declared state and grammar domain. The finite witnesses show
logical obstructions and sharp possible lower bounds; empirical application
needs a separately justified ecological completion contract.

## Legacy design shelf

Budgeted reset panels, witnessed evidence bounds, independent cell-loss panels,
and common-mode panel robustness remain executable but are no longer active
research targets. They are listed in [the legacy shelf](legacy/README.md).

## Next theorem target

The next core task is a **compositional boundedness dichotomy** for a nested
family of future connection grammars \(\Gamma_1\subseteq\Gamma_2\subseteq\cdots\):

- a positive condition under which newly attachable modules factor through one
  fixed finite dynamic boundary summary, so \(\sup_m K_{\Gamma_m}<\infty\); and
- a negative condition under which each new module is independently addressable
  relative to the existing quotient, forcing cumulative growth.

This would turn the present sharp witness into a family-level criterion for when
open ecological composition preserves, versus destroys, finite macro-law
portability.

## Navigation

- [Current architecture](current_architecture.md)
- [Asset map](repository_asset_map.md)
- [Legacy shelf](legacy/README.md)
- [Dynamic boundary blankets](dynamic_boundary_blankets.md)
- [Grammar-aware dynamic blankets](grammar_aware_dynamic_blankets.md)
- [Delayed addressability](delayed_addressability.md)
- [Adaptive closure no-go](adaptive_closure_no_go.md)
- [Extension–compression noncommutation](extension_compression_noncommutation.md)
- [Joint open-candidate laws](joint_open_candidate_laws.md)