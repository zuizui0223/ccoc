# RACH theorem map: core, companions, and frozen shelves

## Repository decision

RACH no longer treats every valid result as one long theorem chain. The active
structural program is **portability core v1**. Delayed evidence, retained
mechanisms, and experiment design are companion or legacy programs with their
own questions.

Read [portability core v1](portability_core_v1.md) for the canonical statement
and [research priorities](research_priorities.md) for the freeze policy.

## A. Portability core v1

### A0. Finite-model prerequisite

For a declared finite deterministic update system, local transition rules need
not imply one global endpoint. The closure calculus distinguishes global closure,
recurrence, and multistability.

\[
\text{local transition specification}
\not\Rightarrow
\text{one global endpoint}.
\]

This is a prerequisite, not the main open-composition theorem.

### A1. Exact finite factorization

A grammar-aware boundary summary is exact only when it preserves current output,
enabled legal actions, and successor summary after every legal action. Its
canonical legal-word quotient is the coarsest exact interface.

\[
\boxed{
\text{finite update-closed boundary summary}
\Rightarrow
\text{exact finite macro-interface.}
}
\]

### A2. Extension–compression obstruction

For an addressable product subsystem

\[
S^*\cong I\times E_1\times\cdots\times E_q,
\]

with concrete legal decoder words for the inside coordinate and every exterior
factor,

\[
\boxed{
K_{\mathrm{open}}
\ge
\log_2|I|+\sum_j\log_2|E_j|.
}
\]

If fixed closed context \(j\) factors through \((I,E_j)\),

\[
\boxed{
K_{\mathrm{open}}-
\max_jK_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-
\max_j\log_2|E_j|.
}
\]

This is the Extension–Compression Noncommutation Inequality. It is the core
lower-bound obstruction, not merely an example.

The binary relay tree is a sharpness witness:

\[
K_{\mathrm{closed},j}=2,
\qquad K_{\mathrm{open}}=m+1,
\qquad \Delta=m-1.
\]

Its bounded degree and constant local grammar show that the gap is not an
artifact of growing local interaction complexity.

### A3. Portability ladder under composition

These results are one family.

| Level | Theorem status | Premise | Conclusion |
|---|---|---|---|
| Uniform boundedness | sufficient criterion | every stage factors through one finite summary alphabet \(Q\) | \(\sup_mK_m\le\log_2|Q|\) |
| Coherent portability | sufficient criterion | same macro output/action/transition system at every stage; label-coherent embeddings | one exact macro-law across nested stages |
| Conservative extension | sufficient criterion | legal rows may expand in a fixed finite action alphabet; old meanings fixed; new actions label-deterministic | one exact finite macro schema on the union grammar |

The fixed-legality theorem is contained in conservative extension as the case
where no legal row expands.

### A4. Concrete obstruction within a proposed macrostate

A newly legal action can invalidate a proposed portable merge without any global
state-count argument. If two states in one proposed summary fiber have different
one-step traces or successor labels under that action, no exact conservative
schema can retain the merge.

\[
q(x)=q(y),
\quad
\operatorname{Tr}(x,a)\ne\operatorname{Tr}(y,a)
\ \text{or}\ q(T(x,a))\ne q(T(y,a)).
\]

The certificate identifies the pair and action.

## B. Identifiability companion

### B1. Delayed exterior exposure

For any finite adaptive policy, a delayed closed/open pair can agree on the
complete policy transcript while separating after the policy horizon.

\[
\boxed{
\text{finite adaptive evidence without an independent horizon contract}
\Rightarrow \mathrm{UNRESOLVED},
\text{ not closure.}
}
\]

This is an epistemic result about what finite evidence can certify. It is not a
premise of the structural portability core.

### B2. Retained mechanism families

Candidate-specific laws form one universal deterministic law exactly when all
induced candidate maps agree:

\[
G_a^\theta=G_a^{\theta'}
\quad\forall\theta,\theta',a.
\]

Otherwise the honest outputs are a candidate-safe law, a set-valued law, or
`UNRESOLVED`.

Joint exterior–mechanism lower bounds require their own joint realizability and
concrete joint-separation premises. They are not automatic additions of separate
lower bounds.

## C. Experimental-design legacy shelf

The following remain executable and tested but are not active theorem targets:

- budgeted reset and delayed joint panels;
- witnessed boundary evidence;
- independent cell-loss panel robustness;
- common-mode failure robustness; and
- narrow observation-regime closure utilities.

They are conditional design results after a quotient, reset, coverage, or failure
contract has already been fixed. See [legacy/README.md](legacy/README.md).

## D. Honest unresolved region

No theorem currently classifies every growing composition family. In particular,
a family may lack both:

- a supplied common finite dynamic factorization; and
- a jointly realizable independent-decoder product certificate.

Such a family is

\[
\boxed{\mathrm{UNRESOLVED}.}
\]

This is a deliberate boundary against false dichotomies.

## E. Priority order

1. Consolidate and audit portability core v1; do not add local variants.
2. Separate public entry points and logical packages.
3. Choose exactly one subsequent direction only after the v1 stop criteria are
   met: non-nested rewiring, composition-dependent mechanisms, or approximate
   noisy portability.

See [research priorities](research_priorities.md).