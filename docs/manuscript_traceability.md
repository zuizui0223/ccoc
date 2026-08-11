# Manuscript theorem traceability record

> **Purpose.** This file is the permanent bridge between the frozen CCOC/RACH
> theorem archive and the planned submission workspace. It is provenance metadata,
> not manuscript prose. The manuscript must restate definitions and proofs
> independently and pin a permanent repository commit/release before submission.
>
> **Claim-control status (2026-08-12).** The mathematical theorem package below is
> usable under its written assumptions. Priority/firstness for the bounded-local
> realization remains conditional while issue #122 audits classical universal
> sequential-machine compilation, especially compiler clauses C3, C5, and C6.

## 1. Canonical manuscript spine

| Manuscript role | Registry source | Formal statement carried to manuscript | Canonical implementation | Finite replay route | Mandatory non-claim / scope guard |
|---|---|---|---|---|---|
| **Definition / substrate: exact grammar-aware interface** | `CORE-1` | For a declared finite deterministic controlled system and fixed finite legal-action grammar, the legal-word quotient is the coarsest exact interface preserving current output, enabled legal-action rows, and enabled-action successors. | `causal_model/dynamic_boundary_blankets.py`; `causal_model/grammar_aware_blankets.py`; `causal_model/shared_grammar.py` | `python -m pytest tests/test_dynamic_boundary_blankets.py tests/test_grammar_aware_blankets.py tests/test_shared_grammar.py -q` | The quotient/minimality object is fixed-grammar substrate, not the novelty claim. The supplied grammar is not inferred from ecological data. |
| **Main negative theorem: addressable-completion lower bound** | `CORE-2` | On a declared jointly realizable product-indexed comparison set, uniformly legal decoder words for the inside and each exterior coordinate force every exact open interface to be injective on that set; hence open memory is at least the log of the addressable product size. | `causal_model/extension_compression_noncommutation.py`; `causal_model/operational_addressability.py` | `python -m pytest tests/test_extension_compression.py tests/test_operational_addressability.py -q` | No lower bound follows from system size, exterior-module count, or composition alone. Joint realizability and operational separation are assumptions. |
| **Main corollary: extension–compression noncommutation** | `CORE-2` | Combine the open injection lower bound with supplied closed-context exact factorizations through `(I,E_j)` to obtain a closed-vs-open interface-memory gap. Closed factorization gives an **upper bound**; equality requires additional closed decoder conditions. | same as `CORE-2` | same as `CORE-2`; finite equality cases are replayed in the binary witness | Do not replace closed upper bounds by equality in the general theorem. Do not claim that every open ecological system has growing memory. |
| **Sharpness / realization theorem: bounded-local binary relay** | `CORE-3` plus post-reopening relay strengthening | The explicit binary family attains the declared closed/open separation using pairwise radius-one updates, maximum degree three, bounded local node/message state, and a fixed four-symbol global control alphabet in the strengthened addressed relay. | `causal_model/extension_compression.py`; `causal_model/relay_tree_compilation.py` | `python -m pytest tests/test_extension_compression.py tests/test_relay_tree_compilation.py -q`; paper-core replay below | This is an explicit sharpness realization, not a classification of arbitrary bounded-degree networks. Historical universal-compilation novelty risk remains open in #122. |
| **Positive boundary: conservative finite portability** | `CORE-4` | A declared finite summary schema remains exact through a finite composition/action-growth chain when old macro meanings are preserved and newly available actions have fiber-uniform availability and one macro successor. | `causal_model/compositional_boundedness.py`; `causal_model/coherent_portable_macrolaw.py`; `causal_model/conservative_macro_schema.py` | `python -m pytest tests/test_compositional_boundedness.py tests/test_coherent_portable_macrolaw.py tests/test_conservative_macro_schema.py -q` | Sufficient, not necessary; finite deterministic scope only. No theorem about arbitrary infinite, stochastic, continuous, or learned ecological systems. |
| **Local diagnostic: future-word / newly legal-action split** | `CORE-5` | A later legal word or newly legal action refutes one proposed macro merge if it separates two states within that fiber. | `causal_model/coherent_portable_macrolaw.py`; `causal_model/conservative_macro_schema.py` | `python -m pytest tests/test_coherent_portable_macrolaw.py tests/test_conservative_macro_schema.py -q` | One fiber split does not prove a global lower bound and does not rule out every alternative macro-law. In the manuscript this is supporting logic, not a separate headline theorem. |

## 2. Post-reopening quantitative strengthening and how to cite it

The canonical registry IDs remain `CORE-1`–`CORE-5`; the August 2026 work sharpens
how the manuscript may formulate the same spine rather than creating a new
publication-core theorem family.

### 2.1 Codebook / constrained-domain strengthening of `CORE-2`

The full Cartesian product is not the only useful comparison domain. For a finite
jointly realizable codebook `C`, operational pair separation gives an exact open
restricted-domain quotient of size `|C|`; closed factorizations give comparison
upper bounds through the corresponding coordinate projections. Parity and
fixed-richness families show that near-linear interface inflation can persist
under strong composition constraints.

**Manuscript use:** present this as a strengthening/robustness paragraph or
supplementary corollary to the addressability theorem, not as a second conceptual
spine. Generic distinguishability of a finite set is Myhill–Nerode/fooling-set-like
substrate and is not itself a priority claim.

### 2.2 Union-grammar refinement and causal-interface inflation accounting

When the open grammar is exactly the union of closed grammars on one common
comparison domain, the open response equivalence is the common refinement of the
closed response equivalences. The resulting product-capacity / realizability-defect
identity is an exact accounting tool. When genuinely open-only words are added,
`iota_new` records additional dynamic distinctions; `CORE-5` supplies the local
split witness for positive open-only innovation.

**Manuscript use:** use this to clarify mechanism/accounting, not as the novelty
headline. Common refinement, natural-join/product-capacity algebra, and the fact
that adding response words can refine a partition are classical substrate.

### 2.3 One-new-action maximal-innovation relay

The strengthened relay keeps routing dynamics legal on the closed side and opens
only one primitive action, `fire`. On its declared finite comparison domain the
closed-union quotient remains two classes while the open quotient is discrete,
so the open-only innovation saturates the finite-domain capacity bound. The fixed
global action alphabet is `{0,1,fire,tick}` and addressed access is logarithmic in
`m` in the explicit relay family.

**Manuscript use:** this is the cleanest quantitative sharpness statement currently
available. However, issue #122 makes the novelty rule explicit: do not claim that
bounded-local existence or logarithmic access is historically first until the
Weiner–Hopcroft / Newborn–Arnold / Williams compiler details are resolved.

## 3. Proof obligations that must appear independently in LaTeX

The paper repository may cite this codebase for provenance and finite replay, but
must independently contain at least the following analytic arguments.

1. **Exact-interface definition and fixed-grammar quotient substrate.** State the
   finite controlled-system and grammar objects precisely and prove the required
   exactness/minimality fact only to the extent needed by the paper.
2. **Addressability injection proof.** For two distinct product/codebook states,
   select a coordinate on which they differ and invoke the corresponding declared
   legal decoder word to separate their future traces. Conclude injectivity of any
   exact open interface on the comparison set.
3. **Closed/open gap derivation.** Combine the open lower bound with closed
   **upper bounds** from supplied exact factorizations. State separately the extra
   conditions that make the explicit witness attain equality.
4. **Relay realization proof.** Define the finite local state/message grammar,
   topology, selector dynamics, firing, return/pulse dynamics, and focal readout;
   prove the claimed degree/locality/alphabet bounds and behavioral correspondence
   to the coordinate witness. Do not rely on exhaustive Python replay as the
   general proof.
5. **Positive portability proof.** Show that output, legal-action rows, and macro
   successors factor through the proposed finite schema at every declared stage.

## 4. Canonical finite reproducibility surface

The submission should point readers to one consolidated replay route rather than
asking them to infer validity from scattered tests.

- provenance registry: `docs/theorem_registry.json` and `docs/theorem_registry.md`;
- mathematical audit: `docs/paper_core_audit.md`;
- manuscript-readiness/scope audit: `docs/manuscript_readiness_audit.md`;
- replay script: `scripts/verify_paper_core.py`;
- replay regression: `tests/test_paper_core_reproducibility.py`;
- workflow: `.github/workflows/paper-core-reproducibility.yml`.

The workflow/replay is a certificate for declared finite instances and provenance.
It is **not** an automated proof checker and does not validate an observed
ecosystem.

## 5. Related-work / novelty gates attached to theorem claims

| Claim component | Known ancestry / comparison class | Current manuscript rule |
|---|---|---|
| Fixed-grammar exact quotient/minimization | Myhill–Nerode / deterministic transducer minimization, bisimulation/state abstraction, predictive-state approaches | Cite as substrate; no priority claim. |
| Context/input-restricted minimization | Kim–Newborn lineage, interacting-FSM don't-cares, Tail Minimization and related sequential-machine work | Broad contextual compression is prior art; novelty cannot be phrased as “closed context allows smaller machine.” |
| Common refinement / product capacity | regular-language state/quotient complexity, database/natural-join style product accounting | Use as exact accounting substrate, not headline novelty. |
| Repeated identical/local module realization | Weiner–Hopcroft, Arnold–Tan–Newborn, Newborn–Arnold, later decomposition theory | Historical ancestry is established in broad terms. Residual quantitative novelty is conditional on unresolved compiler semantics/overhead. |
| Incomplete specification + uniform/constrained decomposition | Williams (1975) and later general decomposition work | Broad combination is prior art; original full-text compiler clauses remain part of issue #122. |
| CCOC residual candidate | simultaneous extremal restricted→open response separation plus fixed small global controls, bounded local state/connectivity, radius-one pairwise realization, and logarithmic access | Allowed only as an **explicit combined construction**; no firstness wording until #122 is resolved. |

The live evidence/control files are:

- `docs/quantitative_prior_art_matrix.md`;
- `docs/universal_compilation_reduction_risk.md`;
- `docs/universal_compilation_source_audit.md`;
- `docs/universal_compiler_acquisition_log_2026-08-12.md`;
- GitHub issue #122.

## 6. Ecological interpretation boundary

The manuscript may give a synthetic ecological reading in which a focal community
or patch is coupled to dormant exterior modules and future composition makes
additional responses addressable. This is a model interpretation only.

The archive does **not** support claims that:

- any observed ecosystem realizes the product/codebook assumptions;
- a real ecological boundary grammar has been identified from data;
- the relay architecture is a literal ecological interaction network;
- field observations establish closure, open-interface memory, or transportability.

Any empirical application must independently justify the state variables,
admissible exterior actions, decoder/response contract, and comparison domain.

## 7. Transfer contract for `rach-open-composition-paper`

When the manuscript repository exists, copy the logical content of this record
into its `traceability/` area and pin a permanent CCOC/RACH commit or release. The
paper workspace should contain manuscript LaTeX, bibliography, figures, supplement,
and cover letter; those artifacts should not be developed inside this theorem
archive.

At transfer time record:

- exact CCOC commit/release SHA;
- theorem registry version;
- exact paper-core replay artifact/workflow run;
- status of issue #122 and the allowed novelty wording at that date;
- any theorem statement differences introduced by manuscript notation only.

Until that transfer is possible, this file is the canonical publication bridge.