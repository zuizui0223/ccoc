# Manuscript readiness audit: open-composition causal compression

> **Current status: 2026-08-13.** CCOC/RACH is an active theorem archive with a
> preserved July 2026 reproducibility checkpoint. Manuscript prose still belongs
> in a separate `rach-open-composition-paper` workspace, but post-reopening theorem
> strengthening is allowed here through branch/PR review.

## Decision

The theorem package is ready for a theorem-first manuscript **under a narrow claim
boundary**. The main scientific statement is

\[
\boxed{
\text{exact compression in each fixed closed composition grammar}
\not\Rightarrow
\text{one small exact interface for the declared open grammar}.
}
\]

The strongest current quantitative realization goes beyond the historical v1
product witness: arbitrary addressable codebooks are allowed, static closed-view
capacity is separated from open-only future innovation, and one newly legal
primitive action can attain the absolute finite-domain maximum `m` bits of new
response memory on a degree-three, pairwise, constant-local-state relay.

Passing finite certificates support reproducibility. They do not replace the
analytic proofs and do not infer a biological grammar from observations.

## Current manuscript package

| Manuscript role | CCOC asset | What can be used | What must not be claimed |
|---|---|---|---|
| Formal substrate | `CORE-1`, grammar-aware interface modules | Exact interface preserves output, legal-action rows, and successor labels for one supplied finite grammar. | Do not claim fixed-grammar quotient/minimization as novel. |
| Main negative theorem | strengthened `CORE-2`, `addressable_codebooks.py`, `extension_compression_noncommutation.py` | A jointly realizable, operationally future-separable codebook forces a large exact open quotient while supplied closed factorizations remain small. | Do not infer codebook structure/addressability from data; do not claim ordinary distinguishability as novel. |
| Quantitative decomposition | union/refinement and `interface_inflation.py` assets | Separate closed-view capacity, join-realizability loss, and genuinely new open-only future innovation. | Common refinement and the algebraic identity are substrate, not novelty claims. |
| Extremal witness | `single_action_innovation.py`, relay modules | One newly legal primitive action gives `iota_new=m`, saturating the finite-domain maximum; fixed global alphabet `{0,1,fire,tick}`, degree three, pairwise radius-one dynamics, constant local grammar. | Do not claim historical firstness for uniform modular realization; issue #122 remains the gate. |
| Locality scope | `innovation_capacity_latency.py`, local causal-cone assets | Exact `2 log2(m)+2` access in the declared selector/return architecture and `Omega(log m)` order lower bound in the broader bounded-local causal-cone class. | Do not claim bounded degree alone implies latency or present the generic causal-cone principle as new. |
| Positive boundary | `CORE-4`, conservative portability modules | A finite update-consistent conservative schema is a sufficient exact portability condition. | Do not present it as a necessary characterization of all abstractions. |
| Local negative boundary | `CORE-5` | A newly legal future word that splits one proposed macro fiber refutes that merge. | One split does not rule out every alternative macro-law. |
| Scope / ecology | `docs/nonempirical_scope.md` | Focal-window/exterior-module language can motivate the mathematics synthetically. | No empirical ecosystem validation, fitted parameters, or claim that a real community satisfies the model contract. |

Companion results such as adaptive finite-evidence nonidentifiability and the Fano
approximate-addressability bound may be cited as robustness/limitations, but they
should not enlarge the first-paper theorem spine unless the manuscript scope is
explicitly changed.

## Precise theorem spine

### A. Exact grammar-aware response interface

For a supplied finite deterministic controlled system and finite grammar, two
states may be merged only when current output, legal-action availability, and
successor macro labels agree throughout the legal future response semantics. The
resulting quotient is the coarsest exact interface for that fixed contract.

This is mathematical substrate.

### B. Cross-grammar addressability lower bound

Let a finite comparison codebook

\[
C\subseteq A_0\times\cdots\times A_q
\]

be jointly realizable. If declared open-grammar future words recover enough
coordinates to separate every distinct codeword, then the exact open quotient on
that comparison domain is discrete:

\[
\boxed{K_{\mathrm{open}}(D_C)=\log_2|C|.}
\]

If each fixed closed context factors on the same comparison domain through a
small retained projection `pi_j`, then

\[
\boxed{
K_{\mathrm{open}}(D_C)-\max_jK_{\mathrm{closed},j}(D_C)
\ge
\log_2|C|-\max_j\log_2|\pi_j(C)|.
}
\]

The historical full product is only one special case. Parity and fixed-richness
families show that nearly linear inflation can survive strong global composition
constraints.

### C. Closed-view capacity versus open-only future innovation

When the open grammar is exactly the union of the closed grammars, the exact
quotient is their common refinement. For the more general case where the actual
open grammar adds new future words, the total gap can be organized as

\[
\boxed{
\Delta_{\mathrm{total}}
=
\Delta_{\mathrm{capacity}}
-
\delta_{\mathrm{join}}
+
\iota_{\mathrm{new}}.
}
\]

The static common-refinement/join terms have classical ancestry. The useful
interpretive separation is that `iota_new` records distinctions unavailable under
the entire closed-union response grammar and created only by newly legal future
experiments/actions.

### D. One-action maximal-innovation witness

On

\[
D_m=\{0,1\}^{m+1},
\]

the strengthened relay keeps the closed union at

\[
|P_U|=2
\]

while adding only the primitive action `fire` makes the open quotient discrete:

\[
|P_O|=2^{m+1}.
\]

Therefore

\[
\boxed{\iota_{\mathrm{new}}=m.}
\]

Since

\[
\iota_{\mathrm{new}}
\le
\log_2|D_m|-\log_2|P_U|=m,
\]

the witness is absolutely memory-sharp on the declared finite comparison domain.

The same family has a fixed four-symbol control alphabet, maximum degree three,
pairwise radius-one selector/pulse dynamics, constant local state/message grammar,
and logarithmic causal access.

### E. Conservative portability boundary

If the same finite macro labels preserve old outputs/actions/successors and every
newly legal action is uniform in availability and macro successor inside each
fiber, one conservative finite macro schema remains exact as the grammar expands.
This is the constructive sufficient counterpart to the negative theorem.

## Novelty status

### GO: Tier A

The manuscript may center the **same-system cross-grammar response-interface
separation**: one deterministic plant/system is held fixed while the declared
legal future grammar changes from closed contexts to an open grammar.

The paper must not claim that contextual minimization, incomplete-machine state
reduction, ordinary state complexity, common refinement, or exact quotienting are
new.

### CONDITIONAL GO: constrained relay

The relay remains valuable as a particularly clean extremal witness. Its
**historical realization firstness is unresolved** because classical uniform
sequential-machine synthesis already includes fixed-input regimes, repeated
identical modules, delay, bounded fan-out constructions, and incomplete
specification.

The corrected comparison gate is H1--H4:

1. bounded local state/connectivity;
2. fixed context-independent external input encoding/distribution;
3. two-way response-trace faithfulness without spurious compiled distinctions;
4. bounded source-step/network-round/output latency.

Primary OCR from Ullman--Weiner (1969) has materially strengthened the historical
risk. Until the construction pages or equivalent primary text resolve the
remaining clauses, use the relay as a **constrained sharpness witness**, not a
firstness claim.

## Robustness already established

- The codebook theorem removes the unnecessary full-product premise.
- Fixed-richness codebooks retain almost-linear inflation.
- The one-action family shows the dynamic open-only term can equal its absolute
  finite-domain maximum.
- The fixed primitive control alphabet removes the old growing-port caveat.
- The local causal-cone theorem separates architecture-specific exact latency from
  the broader `Omega(log m)` order lower bound.
- The adaptive closure no-go shows finite intelligent experimentation alone does
  not certify closure without a horizon/grammar contract.
- The Fano companion shows fixed decoding error below one half does not collapse
  the open-memory requirement to `O(1)` in the binary full-product family.

## Hard blockers before submission

1. **Tier-A quantitative prior-art falsification.** Search specifically for a
   same-system promise/input-restricted machine theorem in which expanding the
   allowed future-word/input language produces the same small-closed/large-open
   exact quotient gap. Broad contextual-minimization searches are no longer
   enough.
2. **Universal-compiler primary-source gate.** Continue issue #122 through the
   H1--H4 contract and issue #137's construction-page acquisition route. Do not
   repeat generic mirror searches.
3. **Manuscript repository creation.** Create `zuizui0223/rach-open-composition-paper`
   as tracked in issue #141, then pin the exact CCOC source/replay SHA at transfer
   time.
4. **Independent proof exposition.** Restate all analytic definitions and proofs
   in LaTeX rather than referring to Python certificate output as proof.
5. **Related Work claim control.** Convert the novelty audits into page-checked
   comparisons and keep the abstract/introduction within the Tier-A/Tier-B
   boundary.

## What is not a submission blocker

The following are valid future research directions but should not delay the first
paper:

- a necessity/converse theorem for a delimited cross-grammar class;
- approximate/stochastic **portability** beyond the existing Fano lower-bound
  robustness result;
- a new joint tradeoff linking response memory to a nonclassical structural
  resource;
- an ecological composition theorem that derives addressability or a finite
  blanket from explicit ecological network/dispersal constraints.

Replacement/rewiring transport remains centered in `zuizui0223/mltr`.

## Figure contract

1. **Closed versus open grammar.** Same plant/system, small closed response
   grammars, expanded open future grammar.
2. **Operational lower-bound proof.** Two codewords differing in a future-readable
   coordinate and the decoder word that separates them.
3. **One-action relay.** Binary selector tree, `fire` as the only newly legal
   primitive action, local pulse return, fixed four-symbol controls, degree three.
4. **Positive boundary.** A macro fiber preserved by a uniform new action versus a
   fiber forced to split by nonuniform future response.

An ecological focal-patch illustration may be added only as a synthetic reading,
not as data evidence.

## Repository policy

- `ccoc`: theorem archive, active theorem strengthening under branch/PR discipline,
  historical replay, claim control, source audits.
- `rach-open-composition-paper`: manuscript prose, bibliography, figures,
  submission files, and pinned theorem provenance once manually created.
- `zuizui0223/mltr`: non-nested replacement/rewiring transport program.

The next CCOC work should be driven by the remaining gates above, not by theorem
count. See [`research_priorities.md`](research_priorities.md) for the canonical
agenda.
