# Manuscript theorem traceability record

> **Claim-control version: 2026-08-13.** This file maps manuscript mathematics to
> CCOC provenance. It deliberately separates **what is proved** from **what may be
> historically novel**. The theorem package remains valid under its assumptions;
> novelty has been narrowed substantially by the August historical audit.

## 1. Core mathematical map

| Manuscript role | Provenance | Valid mathematical use | Novelty status |
|---|---|---|---|
| Exact grammar-aware response interface | `CORE-1`; `dynamic_boundary_blankets.py`, `grammar_aware_blankets.py` | Coarsest exact finite interface preserving current output, legal rows, and successors for a declared grammar | **Substrate.** Fixed-grammar quotient/minimality is not claimed new. |
| Addressable codebook/product lower bound | `CORE-2`; `extension_compression_noncommutation.py`, `addressable_codebooks.py` | Pair-separating legal future responses force injectivity on a declared codebook; closed factorizations give comparison upper bounds | **Substrate/formalism.** Pair separation and cardinality lower bound are Myhill–Nerode/separating-family style mathematics. |
| Closed/open interface gap | `CORE-2` | Combine open lower bound with closed **upper bounds**; equality only under additional closed decoder conditions | **Formal problem statement, not firstness-bearing by itself.** Context-dependent minimization and broad reduction/composition noncommutation have classical ancestry. |
| Fixed-regular maximal one-action theorem | `fixed_regular_grammar_relay.py`, `extremal_open_composition.py`, `docs/fixed_regular_extremal_theorem_2026-08-13.md` | For every positive `m`, one fixed four-symbol grammar schema gives `|P_C|=2`, `|P_O|=2^(m+1)`, `iota_new=m`, cut width one, degree at most three, bounded local alphabets, and exact worst canonical access `2 ceil(log2 m)+2` | **Residual conditional candidate only as a simultaneous constrained package.** The quotient/kernel and regular-language ingredients are substrate. Historical realization firstness remains gated by #122. |
| Conservative finite portability | `CORE-4`; `compositional_boundedness.py`, `coherent_portable_macrolaw.py`, `conservative_macro_schema.py` | Sufficient finite factorization criterion for preserving one macro schema under declared action/composition growth | Useful positive boundary; no complete converse claim. |
| Future-word/fiber split | `CORE-5` | Local certificate that one proposed macro merge fails when a newly legal response separates states inside the fiber | Supporting logic only. |

## 2. Mathematical statement that should appear in the paper

For a finite comparison domain `D`, let each legal future word `w` induce a
response map `R_w`. Then

\[
s\sim_L t
\iff
R_w(s)=R_w(t)\quad\forall w\in L,
\]

so

\[
\sim_L=\bigcap_{w\in L}\ker R_w.
\]

This explains grammar monotonicity and why a pair-separating future family makes a
codebook discrete. The codebook theorem is still worth stating because its
operational assumptions are the model contract used by CCOC; the kernel/cardinality
step is not assigned novelty.

## 3. Quantitative construction to emphasize

The strongest explicit construction is now the **arbitrary-`m` fixed-regular relay**.
For every integer `m>=1`, use the same primitive alphabet and grammar schemas

\[
A=\{0,1,\mathsf{fire},\mathsf{tick}\},
\]

\[
L_C=\{0,1,\mathsf{tick}\}^{*},
\qquad
L_O=A^{*}.
\]

Both grammars have one partial-DFA state independent of `m`; opening adds exactly
the missing `fire` transition. On

\[
D_m=\{0,1\}^{m+1},
\]

the construction has

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
\iota_{\rm new}=m.
\]

The same family simultaneously has:

- absolute zero-slack saturation of the finite-domain innovation bound;
- one newly legal primitive action (`fire`);
- no `m`-dependent legal-word list in the theorem statement;
- pairwise radius-one updates;
- maximum degree three;
- bounded local state/message alphabets;
- tree interaction topology and focal/exterior edge cut one;
- exact worst canonical response access `2 ceil(log2(m)) + 2`.

The analytic proof is
`docs/fixed_regular_extremal_theorem_2026-08-13.md`. The executable aggregate
certificate is `causal_model/extremal_open_composition.py`. These aggregate
existing results; they are not an additional independent theorem branch.

**Claim rule:** write this as an explicit extremal constrained construction. Do not
use “first” or equivalent wording while #122 is unresolved.

## 4. Why the novelty boundary moved

The current related-work audit establishes or strongly documents ancestry for:

- Kim--Newborn and interacting-FSM input/context-restricted minimization;
- incomplete-machine state reduction;
- promise/restricted-domain descriptional advantages;
- Hartmanis--Stearns reduction/realization noncommutation;
- repeated identical modules, fixed-input modular synthesis, bounded fanout, and
  fixed modules with delay;
- common-refinement/state-complexity and natural-join style accounting.

The Larrauri--Bloem tail-minimization “exponential improvement” is algorithmic
relative to the classical determinization route, not an exponential minimum-state
closed/open ratio; their exponential solution-size result concerns the distinct
tail-synthesis problem.

## 5. Live compiler gate attached to the relay

Issue #122 asks whether one classical full-language compiler supplies all four
resources with comparable overhead:

- **H1:** bounded local state/connectivity;
- **H2:** fixed context-independent source controls/input distribution;
- **H3:** two-way response-trace faithfulness with no spurious closed distinctions;
- **H4:** bounded source-step/network/output latency.

If H1–H4 all hold, the bounded-local **existence** part of the relay is demoted. The
relay remains useful for explicit constants, architecture, equality/sharpness, and
ecological explanation.

### Primary sources now actionable

- Weiner--Hopcroft report no. 61 — University of Tokyo / Princeton physical-copy
  route;
- Newborn--Arnold 1972 C-21(1):63–79 — Osaka Prefectural Central Library direct
  copy route; correct DOI `10.1109/T-C.1972.223433`;
- Drilman--Weiner 1972 C-21(10):1124–1129 — same Osaka holding; fixed-module plus
  nondeterministic-machine lead;
- Williams + Le Van--van Houtte 1975 C-24(8) — Tokyo University of Technology
  physical route;
- Sureshchander 1978, Almaini 1978, Chen--Hurst 1982 — same Tokyo holding as
  follow-up/correction/comparison sources.

No H1–H4 resource is promoted merely because a source is obtainable.

## 6. Required independent analytic proofs

The manuscript/supplement must independently prove:

1. exact response-equivalence/interface definition;
2. codebook pair-separation injection and closed/open comparison;
3. the fixed-regular extremal theorem: all-word closed invariant, legal coordinate
   readout, discrete open quotient, capacity equality, locality/cut properties, and
   arbitrary-`m` latency;
4. conservative finite portability factorization.

The current integrated proof of item 3 is
`docs/fixed_regular_extremal_theorem_2026-08-13.md`. It should be transferred into
LaTeX independently of the Python implementation.

Passing Python tests or finite replay are not the analytic proof.

## 7. Reproducibility provenance

Canonical surfaces remain:

- `docs/theorem_registry.json` / `docs/theorem_registry.md`;
- `docs/paper_core_audit.md`;
- `scripts/verify_paper_core.py`;
- `tests/test_paper_core_reproducibility.py`;
- `.github/workflows/paper-core-reproducibility.yml`.

The post-reopening aggregate replay additionally uses
`tests/test_extremal_open_composition.py`.

At manuscript transfer time record an exact CCOC SHA, theorem registry version,
replay SHA/run/artifact, and #122 status. Never cite “latest” without a SHA.

## 8. Ecological interpretation boundary

The paper may interpret the formal state coordinates as dormant exterior ecological
modules and the legal future grammar as possible colonization/connection/action
histories. This is synthetic interpretation only.

A useful derived ecological corollary is recorded in
`docs/narrow_physical_boundary_not_causal_closure_2026-08-13.md`: in the explicit
relay, the focal node is separated from all exterior memories by a single graph
edge for every `m`, while the exact dynamic boundary summary required by the open
grammar still needs at least `m` exterior bits. The manuscript may use this to
explain that **small physical boundary width is not a causal-closure certificate**.
This is a consequence of the existing relay plus blanket lower bound, not a new
firstness-bearing theorem.

The archive does not establish that any observed ecosystem realizes the declared
codebook, grammar, decoder words, relay topology, or finite blanket. Empirical
applications must justify those contracts independently. In particular, a narrow
corridor, inlet, island connection, or present interaction cut cannot by itself be
interpreted as evidence for a small causal boundary state.

## 9. Fallback research decision

If the historical compiler gate subsumes the constrained relay existence claim,
the next mathematics should not defend the old slogan. The active targets become:

- a genuine necessity/converse theorem in a delimited cross-grammar class;
- a nonclassical coupled memory/control/latency tradeoff;
- approximate/stochastic **portability**, not only approximate addressability;
- an ecological structural theorem that derives addressability or finite-blanket
  conditions from explicit colonization/dispersal/network constraints.

This traceability record should be copied logically—not verbatim code—into the
future manuscript repository once issue #141's repository-creation blocker is
removed.
