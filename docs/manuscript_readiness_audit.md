# Manuscript readiness audit: open-composition causal compression

> **Current status: 2026-08-19.** The theorem package is ready for manuscript completion under a narrow claim boundary. Manuscript prose now lives inside CCOC under `manuscript/`.

## Decision

The first paper should center one statement:

\[
\boxed{
\text{exact compression in each fixed closed future grammar}
\not\Rightarrow
\text{one comparably small exact interface for the opened grammar}.
}
\]

The manuscript is not a paper about generic contextual minimization. Its quantitative center is the same-system closed/open separation and its explicit extremal realization.

## Current first-paper package

| Role | Current asset | Use | Non-claim |
|---|---|---|---|
| Formal substrate | `CORE-1`, grammar-aware interface modules | Exact interface for one supplied grammar. | Fixed-grammar minimization is not claimed new. |
| Headline theorem | `CORE-2`, `extension_compression_noncommutation.py`, `operational_addressability.py` | Small closed factorizations can coexist with a much larger open exact interface. | Pair separation/cardinality is not itself a novelty claim. |
| Premise robustness | `addressable_codebooks.py`, `codebook_families.py` | Large inflation survives constrained jointly realizable codebooks. | Do not promote this to a separate headline theorem. |
| Extremal sharpness | `fixed_regular_grammar_relay.py`, `extremal_open_composition.py`, relay modules | One-action maximal open-only response distinction with fixed controls and bounded-local realization. | No historical firstness claim for the relay/compiler architecture. |
| Locality support | `local_causal_cone.py` | Architecture-specific access and broader causal-cone lower-bound context. | Generic locality is classical substrate. |
| Positive boundary | `CORE-4` | Sufficient conservative portability criterion. | Not a necessity theorem. |
| Local obstruction | `CORE-5` | A newly legal future word/action can invalidate one proposed merge. | One split does not rule out every alternative macro-law. |
| Ecology/scope | `docs/nonempirical_scope.md` | Interpret grammar opening as declared colonization/reconnection/rewiring possibilities. | No claim that a real ecosystem satisfies the formal contract. |

Approximate addressability is secondary stronger-model material. Evidence, mechanism-uncertainty, inherited-law repair, field-protocol, stochastic special-case, and other historical branches are not first-paper dependencies.

## Precise theorem spine

### A. Exact grammar-aware response interface

For a supplied finite deterministic controlled system and finite legal-future grammar, the stable response quotient is the coarsest exact deterministic interface preserving current output, legal-action availability, and successor macro labels. This is foundational machinery.

### B. Cross-grammar lower bound

For a jointly realizable comparison codebook \(C\), if the open grammar contains future words that separate all distinct codewords, then the exact open quotient on that domain is discrete:

\[
K_{\mathrm{open}}(D_C)=\log_2|C|.
\]

If each fixed closed context factors through a small retained projection, then the closed/open comparison gives the response-interface gap used in the manuscript.

### C. Extremal one-action family

The explicit family keeps the closed response interface minimal while one newly legal primitive action activates the full finite-domain distinction. In the canonical binary family:

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m.
\]

The bounded-local realization uses fixed primitive controls, bounded local alphabets, pairwise radius-one dynamics, maximum degree three, and logarithmic causal access. These properties establish sharpness under a simple local implementation; they are not presented as historically first.

### D. Conservative portability boundary

A finite macro schema remains exact under legal-action expansion when old meanings are preserved and every newly legal action is uniform in availability and macro successor inside each macro fiber. This supplies the constructive counterpart to the negative theorem.

## Novelty status

### GO

The manuscript may make the same-system cross-grammar quantitative separation its contribution target.

### Surrendered claims

Do not claim discovery of:

- context-dependent or input-restricted minimization;
- environment-relative state abstraction;
- generic state-reduction/composition noncommutation;
- generic exponential descriptional gaps under restricted domains;
- generic quotient/common-refinement facts;
- bounded-local sequential-machine realization in isolation.

### Historical compiler audit

H1–H4 remains an informative Related Work audit. It is non-blocking because the manuscript no longer depends on historical firstness of the relay realization.

## Remaining manuscript blockers

1. **Self-contained analytic exposition.** All definitions and theorem proofs must be written independently in manuscript/supplement prose.
2. **Related Work control.** Every novelty comparison must match the conservative claim boundary and be source-checked.
3. **Ecological framing.** The Introduction and Discussion must explain why future grammar expansion is an ecological state-representation problem rather than merely an automata problem.
4. **Figures.** Build the four agreed figures below.
5. **Immutable submission provenance.** Freeze a final CCOC SHA and rerun theorem registry, paper-core replay, and full pytest.
6. **Final human review.** Review historical wording, ecological interpretation, authorship, acknowledgements, funding, competing interests, and AI-use disclosure as applicable to the target journal.

No separate repository, new theorem family, or additional primary-source acquisition is required merely to begin or complete the manuscript.

## Figure contract

1. **Closed versus open grammar:** same system, restricted closed future grammars, expanded open grammar.
2. **Operational lower bound:** two comparison states and the future word that separates them.
3. **Extremal relay:** selector/pulse architecture, fixed controls, degree-three locality.
4. **Positive boundary:** uniform newly legal action preserving a macro fiber versus a fiber forced to split.

Any ecological illustration is synthetic interpretation, not empirical validation.

## Repository policy

- `ccoc`: theorem code, proof/source provenance, manuscript prose, figures, and submission controls.
- Git history: archive for historicalized CCOC branches.
- `mltr`, `mrm`, `ced`, `crest`: separate companion ownership domains.

## Current verdict

**The mathematical package is manuscript-ready. The remaining work is writing, traceability, figure construction, source-controlled Related Work, and submission QA—not more theorem accumulation.**
