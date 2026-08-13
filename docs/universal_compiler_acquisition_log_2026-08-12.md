# Universal-compiler source acquisition log — through 2026-08-13

> **Purpose.** Record source-retrieval work behind issue #122 so the historical audit is reproducible and does not loop over already exhausted routes. This ledger uses the corrected H1–H4 compiler contract. Bibliographic location, primary-text extraction, and secondary directional evidence are kept separate.

## Live compiler resources

- **H1:** bounded local component state + state-count-independent fan-in/fan-out or degree.
- **H2:** fixed context-independent source controls / input distribution with quantified cost.
- **H3:** two-way response-trace faithfulness at the declared compiled output interface.
- **H4:** bounded source-step / settling / output latency.

For one fixed full-language network, same-hardware sublanguage restriction is derived from H2 + H3 and is not a separate C6 target. Incomplete-specification papers still require a resynthesis check.

## 1. Ullman & Weiner (1969) — primary text partially recovered

Target:

> J. D. Ullman and Peter Weiner, *Uniform Synthesis of Sequential Circuits*, Bell System Technical Journal 48(5):1115–1127, May–June 1969.

### Acquisition routes verified

- article-level VTDA PDF `bstj48-5-1115.pdf`; web opener resolves 14 pages;
- TCI BSTJ index identifies Internet Archive item `bstj48-5-1115`;
- complete-issue scans exist in historical BSTJ archives;
- a WorldRadioHistory complete-issue scan is OCR-indexed and exposes article text.

### Primary text recovered on 2026-08-13

The OCR-indexed **primary BSTJ article** exposes its abstract and opening paragraphs. These passages directly establish:

- binary-input sequential machines are in the target class;
- synthesis uses networks of a fixed module with delay;
- the paper states an **isomorphic realization** result;
- the introduction states that the required interval between source inputs need not grow with network size: it is bounded by the response time of one module after an input change;
- diagrams omit initialization and clock-control provision.

### H1–H4 status

- **H1:** UNKNOWN/PARTIAL — fixed module is explicit, bounded fan-out/degree is not yet extracted.
- **H2:** PRIMARY PARTIAL — fixed binary source input is explicit; physical input distribution cost remains unread.
- **H3:** PRIMARY PARTIAL, strong risk — “isomorphic realization” is primary wording; formal realization/output definition remains unread.
- **H4:** PRIMARY PARTIAL, materially strengthened — network-size-dependent per-input settling time is not an easy residual boundary; exact synchronous-round semantics remain unread.

### Remaining blocker

The article PDF still fails in the screenshot backend and later construction OCR has not surfaced. Do **not** search more generic mirrors. Resume only with a route exposing construction pages or searchable later OCR.

Canonical detail: `ullman_weiner_primary_ocr_2026-08-13.md`; issue #137.

## 2. Hsieh, Tan & Newborn (1968) — DOI corrected; primary body still missing

Target:

> Edward P. Hsieh, Chung-Jen Tan, Monroe M. Newborn, *Uniform modular realization of sequential machines*, ACM National Conference 1968, 613–621.

### Bibliographic correction on 2026-08-13

The DBLP record's DOI link and unpaywall route both point to:

`10.1145/800186.810626`

The previously recorded `10.1145/800186.810625` was a repository error and has been corrected in the canonical audit.

### Retrieval status

The correct DOI route still cache-misses in the available web environment. Targeted title/DOI searches did not surface a readable ACM primary copy. Stop mirror searching unless a genuinely new archive route appears.

A contemporaneous IEEE *Abstracts of Current Computer Literature* digest remains the strongest accessible evidence. It reports the unit-delay logical-completeness distinction between unbounded input dimension and a positive fixed-input regime.

### Claim consequence

Because CCOC fixes the source control dimension as `m` grows, the positive fixed-input historical regime is directly relevant. This secondary digest is sufficient for claim control but not for H1–H4 theorem extraction.

## 3. Weiner & Hopcroft (1968) — strongest H1 source, physical holdings verified

Target:

> Peter Weiner and John E. Hopcroft, *Bounded Fan-in, Bounded Fan-out Uniform Decompositions of Synchronous Sequential Machines*, Digital Systems Laboratory Technical Report no. 61, Princeton University, April 1968.

### Verified holdings

- Princeton archival finding aid confirms the report;
- CiNii Books identifies Digital Systems Laboratory Technical Report no. 61 and a University of Tokyo General Library holding: `U600:769`, record `0004766739`.

### Evidence status

The report body has not been read. Abstract-style evidence points to identical two-state modules with fan-in/fan-out bounded independently of source state count, making it the strongest H1 threat. H2–H4 remain UNKNOWN.

### Next legitimate action

Obtain an actual scan through the University of Tokyo or Princeton library/digitization route. Do not infer compiler timing/input properties from the title/abstract.

## 4. Newborn & Arnold (1972) — DOI fixed, automated route hazard recorded

Target:

> Monroe M. Newborn and Thomas F. Arnold, *Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits*, IEEE Transactions on Computers 21(1):63–79.

Correct DOI:

`10.1109/T-C.1972.223432`

`10.1109/T-C.1972.223521` belongs to Joonki Kim and Monroe M. Newborn, *The Simplification of Sequential Machines with Input Restrictions*.

A DBLP unpaywall route associated with Newborn–Arnold has been observed to resolve to `223521`. Therefore all automated full-text retrieval must validate title/authors before admission.

No H1–H4 clause is promoted from the title alone. The primary article remains unrecovered.

## 5. Huang, Cain & Kinney (1972) — H2 lower-bound interpretation fixed

Target:

> C. C. Huang, Richard Y. Cain, Larry L. Kinney, *Output Sufficient Modules for Uniform Decomposition of Synchronous Sequential Circuits*, SWAT 1972, 192–199, DOI `10.1109/SWAT.1972.17`.

Accessible summary material reports exponential growth in output-sufficient module input count as a function of the **source machine input count**.

This does not imply growth with CCOC's `m`, because the source control dimension is fixed. It therefore cannot by itself rescue H2. The remaining H2 question is source-state-count dependence of input distribution for a fixed source alphabet.

Primary full text remains unrecovered.

## 6. Williams (1975) — resynthesis gate

Target:

> George H. Williams, *Uniform Decomposition of Incompletely Specified Sequential Machines*, IEEE Transactions on Computers 24(8):840–843.

Bibliographic identity is verified; readable primary text remains unrecovered.

The live question is no longer a separate “C6” clause. It is whether each incomplete specification is **resynthesized** into new component count/wiring/control hardware, or whether one full-machine realization is held fixed and only admissibility is restricted.

Secondary wording suggesting minimal-cover optimization is an acquisition lead only.

## 7. Arnold, Tan & Newborn (1970)

IBM Research provides a primary abstract stating that an arbitrary synchronous flow table can be realized as an array of identical modules interconnected in a regular pattern.

This blocks broad novelty language based on repeated identical modules realizing arbitrary synchronous behavior, but does not establish the joint H1–H4 contract.

## 8. Current novelty-control result

The historical boundary is now narrower than at the start of the audit.

Established ancestry/risk:

- uniform realization by repeated identical modules is old;
- fixed-input modular synthesis is old;
- fixed modules with delay are old;
- bounded fan-in/fan-out modular decomposition is a direct historical line;
- incomplete-specification decomposition is old;
- Ullman–Weiner primary text makes **isomorphic realization + network-size-independent input settling** a concrete H3/H4 threat.

Still unresolved jointly:

1. H1 state-count-independent bounded locality;
2. H2 quantitatively cheap distribution of a fixed source control alphabet;
3. H3 formal two-way response semantics at the designated output;
4. H4 exact clock/round semantics comparable to the explicit relay.

Therefore the safe claim remains:

> CCOC's relay is an explicit constrained sharpness witness. Bounded-local/logarithmic-access **existence** should not carry a priority claim while the classical H1–H4 compiler comparison remains open.

## 9. Stop rule

Do not continue generic web searching for the same historical papers. Resume only when one of the following occurs:

- a primary scan/full OCR of Weiner–Hopcroft report no. 61 is obtained;
- Ullman–Weiner construction pages become searchable/renderable;
- the Hsieh ACM paper appears through a new verified archive route;
- a verified Newborn–Arnold or Williams primary copy becomes available.

Until then, further mirror hunting has low expected information value. Work should return to manuscript/provenance preparation rather than theorem proliferation.

## 10. Reproducible pointers

- live gate: issue #122
- Ullman–Weiner construction blocker: issue #137
- `universal_compilation_source_audit.md`
- `fixed_input_unit_delay_historical_risk_2026-08-12.md`
- `ullman_weiner_primary_ocr_2026-08-13.md`
- Princeton/CiNii report holdings recorded in the canonical source audit

This ledger is an acquisition record, not evidence that unrecovered compiler properties fail.