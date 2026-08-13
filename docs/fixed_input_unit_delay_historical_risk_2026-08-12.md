# Fixed-input / unit-delay historical risk — corrected audit

> **Status:** novelty-control memo. This file isolates the historical risk created by classical fixed-input uniform modular synthesis. It uses the corrected H1–H4 compiler contract and separates primary evidence from contemporaneous secondary summaries.

## 1. Why fixed input is dangerous for CCOC novelty

The CCOC relay keeps the global primitive control alphabet fixed,

\[
\{0,1,\mathsf{fire},\mathsf{tick}\},
\]

while the number `m` of dormant memories grows. Therefore a classical universal module whose resources depend only on a **fixed source input dimension** can still be constant with respect to `m`.

The relevant historical question is not merely whether old work used a fixed module. It is whether one classical full-language construction simultaneously provides:

- **H1:** bounded local component state and bounded fan-in/fan-out or degree;
- **H2:** fixed context-independent external input semantics/distribution;
- **H3:** two-way response-trace faithfulness at the declared output interface;
- **H4:** bounded source-step / network-settling / output latency.

Under one fixed full-language realization with H2 + H3, same-hardware restriction to closed/open sublanguages is derived. The old separate C6 clause should not be treated as an independent historical hurdle.

## 2. Hsieh, Tan & Newborn (1968)

Target:

> Edward P. Hsieh, Chung-Jen Tan, and Monroe M. Newborn,  
> *Uniform modular realization of sequential machines*,  
> ACM National Conference 1968, pp. 613–621.

### DOI correction

The canonical DBLP record's **electronic edition via DOI** and its unpaywall route both point to:

`10.1145/800186.810626`

The repository previously recorded `10.1145/800186.810625`. That value is therefore treated as a bibliographic error and is replaced by `...810626` in the live audit.

### Evidence currently available

The original ACM paper has still not been recovered in readable full text. A contemporaneous IEEE *Abstracts of Current Computer Literature* digest summarizes the paper's logical-completeness result in substance as follows:

- no finite module set realizes **all input dimensions** at unit delay;
- for each fixed positive input count, a finite uniform modular realization exists.

Because this is a contemporaneous secondary digest rather than the ACM proof, exact module state count, fan-out, input distribution, trace semantics, and the formal meaning of unit delay remain unresolved.

### Consequence for CCOC

The unbounded-input impossibility does not rescue CCOC: CCOC's source control dimension is fixed as `m` grows. The historically positive fixed-input regime is the relevant comparison.

Primary extraction still needs to answer:

1. what `n` inputs means formally;
2. what module resources depend on `n`;
3. exact unit-delay semantics;
4. whether realization is behaviorally isomorphic/two-way trace faithful;
5. fan-in/fan-out versus source state count;
6. how external inputs are wired/distributed;
7. whether the construction is one fixed full-language hardware realization.

## 3. Ullman & Weiner (1969): primary evidence now recovered

Target:

> J. D. Ullman and Peter Weiner,  
> *Uniform Synthesis of Sequential Circuits*,  
> Bell System Technical Journal 48(5):1115–1127, May–June 1969.

The primary article is located through an exact 14-page article PDF and complete-issue archive scans. Although the PDF screenshot backend still fails, an OCR-indexed scan of the primary BSTJ issue exposes the article abstract and introduction.

The **primary paper itself** states that it studies networks of a fixed module with delay, gives an **isomorphic realization** for every binary-input `n`-state sequential machine, and says the required time between source inputs need not increase with the number of modules: it need not exceed the response time of a single module after an input change.

This materially changes the historical gate:

- **H2: PARTIAL.** Binary/fixed source input is explicit; physical input-distribution cost is not yet extracted.
- **H3: strong PARTIAL.** “Isomorphic realization” is primary text, but the paper's formal realization/output definition is not yet recovered.
- **H4: primary-text PARTIAL.** Network-size-dependent per-input settling time is no longer an easy residual novelty boundary.
- **H1: unresolved.** A fixed module does not by itself establish bounded fan-out or graph degree.

See `ullman_weiner_primary_ocr_2026-08-13.md` and issue #137.

## 4. Related fixed-input evidence

### Huang, Cain & Kinney (1972)

Accessible summary material reports that the input count of an output-sufficient universal module grows exponentially with the input count of the **source sequential machine**. That does not imply growth with CCOC's `m`, because the source input dimension is held fixed. It therefore cannot by itself rescue H2.

### Weiner–Hopcroft lineage

Weiner & Hopcroft's 1968 bounded-fan-in/bounded-fan-out report remains the strongest H1 lead. Archival records and abstract-style evidence identify identical two-state modules and state-count-independent fan-in/fan-out bounds, but the primary report body is still required for H2–H4.

### Newborn & Arnold (1972)

*Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits* remains a high-priority H1/H2 source. Direct inspection of the DBLP January-1972 TOC electronic-edition links gives the DOI:

`10.1109/T-C.1972.223433`

The previously recorded `...223432` is the immediately preceding Koontz–Fukunaga article (pp. 56–63), not Newborn–Arnold. The separate Kim–Newborn input-restriction paper is `...223521`.

Automated retrieval must therefore validate title, authors, issue, and pages rather than trusting a DOI-only route. A direct Osaka Prefectural Central Library copy route is now recorded in `newborn_arnold_primary_acquisition_2026-08-13.md`.

## 5. Residual realization claim after the audit

The historically safe position is narrow:

> CCOC supplies an explicit degree-three, radius-one, fixed-control relay that attains the extremal closed/open response separation with `Theta(log m)` addressed access. Its existence should be treated as a constrained sharpness witness while classical compiler H1–H4 remain unresolved.

Do **not** claim novelty merely from:

- fixed source alphabet;
- repeated fixed modules;
- modular synthesis with delay;
- bounded fan-in/fan-out as a broad idea;
- unit-delay/fixed-input synthesis;
- same-hardware grammar restriction as an independent extra condition when a full-language H2/H3 compiler already exists.

## 6. Decision rule

If a classical full-language construction satisfies H1–H4 with constant or comparable polylogarithmic overhead, demote bounded-local/logarithmic-access **existence** completely and retain the CCOC relay only as a clean explicit sharp construction.

If H1 is classical but H2 or H4 necessarily grows with source state count, then the simultaneous fixed-control/degree-three/radius-one/`Theta(log m)` package may retain a quantitative distinction.

## 7. Canonical pointers

- live compiler gate: issue #122
- Ullman–Weiner construction-page blocker: issue #137
- `universal_compilation_reduction_risk.md`
- `universal_compilation_source_audit.md`
- `ullman_weiner_primary_ocr_2026-08-13.md`
- `newborn_arnold_primary_acquisition_2026-08-13.md`

Primary article route for Ullman–Weiner:

`https://vtda.org/pubs/BSTJ/vol48-1969/articles/bstj48-5-1115.pdf`

Hsieh–Tan–Newborn canonical bibliographic route:

`https://dblp.org/rec/conf/acm/HsiehTN68`
