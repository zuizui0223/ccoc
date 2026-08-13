# Universal-compilation source acquisition and evidence audit

> **Status:** novelty-control evidence memo. This file records what has actually been verified for the corrected compiler reduction in `universal_compilation_reduction_risk.md`. It is not a priority claim. Primary text, authoritative bibliography, contemporaneous summaries, and later secondary summaries are kept distinct.

## 1. Corrected historical question

The bounded-local CCOC witness would be largely generic if a classical sequential-machine compiler produces one fixed full-language network with all four resources below.

- **H1 — bounded locality:** constant local component state and fan-in/fan-out or graph degree bounded independently of source-machine size.
- **H2 — fixed context-independent controls:** source inputs are direct, or use one fixed finite-alphabet encoding/distribution mechanism with quantified cost independent of the later closed/open sublanguage.
- **H3 — two-way response-trace faithfulness:** on the embedded source states, source response equality holds iff the declared compiled observable responses are equal. One-way source-trace decoding is insufficient because richer compiled observables could split a source-equivalence class.
- **H4 — bounded timing/output latency:** source steps/words are realized with explicit bounded network-round, settling, and output-decoding overhead.

Under one fixed full-language network with H2 + H3, same-hardware restriction is **derived**: for a source sublanguage `L`, use the same network only on encoded words `c(L)`. The old C6 is therefore not an independent hurdle for a genuine full-language compiler.

Incomplete-specification methods still raise a separate **resynthesis** question when they synthesize a different network from each partial specification.

## 2. Evidence table

Status vocabulary:

- **PRIMARY PARTIAL:** a primary text directly supports part of the required resource but not the complete CCOC contract;
- **PARTIAL:** authoritative/secondary evidence supports a nearby property;
- **UNKNOWN:** the inspected material does not establish the resource;
- **NOT TARGETED:** the source addresses another resource.

| Source | Material actually inspected | H1 locality | H2 controls | H3 trace faithfulness | H4 timing | Current verdict |
|---|---|---:|---:|---:|---:|---|
| **Hsieh, Tan & Newborn (1968)**, *Uniform modular realization of sequential machines* | DBLP DOI/bibliographic record + contemporaneous IEEE literature digest; ACM body not recovered | PARTIAL | PARTIAL | UNKNOWN | PARTIAL | Major fixed-input/unit-delay risk. Correct DOI is `10.1145/800186.810626`. Fixed input is directly relevant because CCOC's primitive control dimension is fixed as `m` grows. |
| **Weiner & Hopcroft (1968)**, *Bounded Fan-in, Bounded Fan-out Uniform Decompositions of Synchronous Sequential Machines* | Princeton/CiNii archival records + abstract-style description; report body not recovered | PARTIAL | UNKNOWN | UNKNOWN | UNKNOWN | Strongest H1 lead. Available evidence points to identical two-state modules with source-state-count-independent fan-in/fan-out, but H2–H4 await report no. 61. |
| **Ullman & Weiner (1969)**, *Uniform Synthesis of Sequential Circuits* | **primary BSTJ OCR: abstract + introduction**, exact 14-page article PDF route; construction pages not yet readable | UNKNOWN/PARTIAL | **PRIMARY PARTIAL** | **PRIMARY PARTIAL** | **PRIMARY PARTIAL** | Major compiler risk. Primary text explicitly covers binary input, a fixed module with delay, “isomorphic realization”, and input spacing independent of network size. Remaining gaps are fan-out, input distribution, formal realization/output definition, and exact clock semantics. |
| **Arnold, Tan & Newborn (1970)**, *Iteratively Realized Sequential Circuits* | IBM Research primary abstract | UNKNOWN | UNKNOWN | PARTIAL | UNKNOWN | Primary abstract verifies realization of arbitrary synchronous flow tables as a regular array of identical modules, but not the H1–H4 constants. |
| **Newborn & Arnold (1972)**, *Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits* | authoritative bibliographic/DOI records only | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | High-priority H1/H2 source. Correct DOI `10.1109/T-C.1972.223432`; title/author validation is mandatory because an automated unpaywall route has misdirected to Kim–Newborn `223521`. |
| **Huang, Cain & Kinney (1972)**, *Output Sufficient Modules for Uniform Decomposition of Synchronous Sequential Circuits* | bibliographic record + accessible summary | NOT TARGETED/PARTIAL | PARTIAL | UNKNOWN | UNKNOWN | Module-input lower bound scales with **source input count**. Because CCOC fixes source input dimension as `m` grows, this does not create an `m`-dependent H2 obstruction. |
| **Williams (1975)**, *Uniform Decomposition of Incompletely Specified Sequential Machines* | authoritative bibliography + secondary acquisition leads | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Decisive question is per-specification resynthesis versus one full-machine hardware realization later restricted by admissible behavior. |
| **Jóźwiak & Ślusarczyk (2004)**, *General decomposition of incompletely specified sequential machines with multi-state behavior realization* | primary publisher article/abstract material | PARTIAL | UNKNOWN | PARTIAL/UNKNOWN | PARTIAL | Establishes mature ancestry for incomplete specification + constrained network decomposition, not one verified H1–H4 full-language compiler. |

## 3. Source-specific extraction status

### 3.1 Hsieh–Tan–Newborn (1968): DOI correction and fixed-input warning

Canonical paper:

> Edward P. Hsieh, Chung-Jen Tan, Monroe M. Newborn, *Uniform modular realization of sequential machines*, ACM National Conference 1968, 613–621.

The canonical DBLP record's DOI link and its unpaywall route both point to:

`10.1145/800186.810626`

The previously recorded `10.1145/800186.810625` is therefore treated as a repository bibliographic error and should not be reused.

The original ACM paper has not yet been recovered in readable full text. A contemporaneous IEEE literature digest reports a unit-delay logical-completeness distinction: unrestricted input dimension defeats a finite universal module set, while a positive fixed-input-dimension regime admits uniform modular realization.

That secondary evidence is sufficient for **claim control**, not theorem extraction. CCOC keeps its source input dimension fixed while `m` grows, so it sits in the historically dangerous positive regime.

Primary extraction targets:

1. exact definition of source input count;
2. universal-module resources as a function of that count;
3. fan-in/fan-out and wiring constraints;
4. unit-delay semantics;
5. external input presentation/distribution;
6. formal output equivalence/isomorphism.

### 3.2 Weiner–Hopcroft (1968)

Princeton archival records identify Digital Systems Laboratory Technical Report no. 61. CiNii also records a University of Tokyo General Library holding, call `U600:769`, record `0004766739`.

Abstract-style evidence describes a general decomposition into identical two-state modules with fan-in and fan-out bounded independently of original machine state count. Because the report itself has not been read, do not upgrade H2–H4.

The report must settle source-input distribution, declared output, two-way response fidelity, source-clock/network timing, output latency, module count, and graph depth/diameter.

### 3.3 Ullman–Weiner (1969): primary text recovered

The Bell System Technical Journal issue places the article at 48(5):1115–1127. The VTDA article-level PDF resolves as a 14-page PDF. The screenshot backend still cache-misses, but a separate WorldRadioHistory complete-issue scan is OCR-indexed and exposes the article's **primary abstract and opening paragraphs**.

Primary text directly establishes all of the following:

- the synthesis target includes **binary-input** sequential machines;
- the network is built from copies of a **fixed module with delay**;
- the paper states an **isomorphic realization** result for every binary-input `n`-state sequential machine;
- the introduction states that the required interval between source inputs need not grow with the number of modules; it is bounded by the response time of a single module after an input change;
- the diagrams omit initialization and clock-control provision, so exact clock semantics still require the construction pages.

Consequences:

- **H2 = PRIMARY PARTIAL:** fixed source input is direct primary evidence; physical distribution/encoding cost remains unknown.
- **H3 = PRIMARY PARTIAL, strong risk:** “isomorphic realization” is direct primary wording, but the formal isomorphism and declared external output contract remain unread.
- **H4 = PRIMARY PARTIAL:** network-size-dependent per-input settling time is no longer a plausible easy novelty boundary. The exact synchronous round interpretation is still unresolved.
- **H1 = UNKNOWN/PARTIAL:** a fixed module is not enough to infer bounded fan-out or graph degree.

Canonical memo: `ullman_weiner_primary_ocr_2026-08-13.md`. Live construction-page blocker: issue #137.

### 3.4 Arnold–Tan–Newborn (1970)

The IBM Research primary abstract says an arbitrary synchronous flow table can be realized as an array of identical modules interconnected in a regular pattern. This blocks novelty language based merely on repeated identical modules realizing arbitrary synchronous behavior.

It does not establish H1 constants, H2 input cost, H3 exact equivalence preservation, or H4 timing.

### 3.5 Newborn–Arnold (1972)

Canonical source:

> Monroe M. Newborn and Thomas F. Arnold, *Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits*, IEEE Transactions on Computers 21(1):63–79, DOI `10.1109/T-C.1972.223432`.

`10.1109/T-C.1972.223521` belongs to Kim & Newborn, *The Simplification of Sequential Machines with Input Restrictions*. A DBLP unpaywall route associated with the Newborn–Arnold record has been observed to resolve to `223521`. Treat that as an acquisition metadata hazard and validate title/authors before accepting a retrieved PDF.

No H1–H4 property is promoted from the title alone.

### 3.6 Huang–Cain–Kinney (1972): why source-input lower bounds do not rescue H2

Accessible summary material says the input count required by an output-sufficient module grows exponentially with the number of **inputs to the source sequential machine**.

For CCOC the source input/control dimension is fixed as `m` grows. An exponential function of a fixed source input count is still constant with respect to `m`. Therefore this result cannot by itself establish a state-count-dependent external-control cost.

The remaining H2 question is concrete: for fixed source input alphabet, does a classical construction distribute each input with cost bounded independently of source state count?

### 3.7 Williams (1975): resynthesis rather than a separate C6

After correcting the compiler contract, Williams matters for one precise reason.

If every incomplete specification is separately minimized/decomposed, then the paper is strong prior art for context-dependent decomposition but does **not** supply one fixed full-language network whose grammar is merely restricted.

If one full realization is fixed and only admissible source behavior changes, it is much more dangerous. Primary extraction must ask what changes when the specification changes: component count, identities, wiring, controls, or only admissibility.

## 4. What is already blocked as novelty

Do not claim firstness for any of these ingredients in isolation:

- uniform modular realization of arbitrary sequential behavior;
- repeated identical modules;
- fixed-input modular synthesis;
- fixed modules with delay;
- bounded fan-in/fan-out as a broad modular-synthesis idea;
- incomplete-specification plus constrained decomposition;
- contextual/input-restricted minimization;
- generic exponential state blow-up.

These are classical substrate/ancestry.

## 5. What remains unresolved

No primary theorem has yet been verified here to satisfy the **joint** H1–H4 contract with overhead comparable to the explicit CCOC relay. Nor has absence of such a theorem been established.

The remaining possible realization distinction is now narrow. Ullman–Weiner substantially weakens H3 and H4 as escape hatches, while fixed source input weakens H2 arguments based only on growing input dimension. The live comparison is therefore concentrated on:

1. state-count-independent fan-out/degree plus constant local state;
2. quantitatively cheap distribution of a fixed external input alphabet;
3. formal two-way output-trace faithfulness;
4. exact clock/round semantics compatible with the relay's `Theta(log m)` access statement.

Manuscript-safe wording:

> Classical sequential-machine synthesis already contains closely related fixed-input, fixed-module/delay, bounded-fanout, and incomplete-specification constructions. CCOC's relay is an explicit constrained sharpness witness. Whether its existence/logarithmic-access package is already implied by one classical full-language compiler remains a primary-source comparison question.

## 6. Acquisition priority and stop rule

1. **Weiner–Hopcroft 1968 report no. 61:** strongest H1 source; extract H2–H4.
2. **Ullman–Weiner 1969 construction pages:** abstract/introduction are now primary-read; extract fan-out, input distribution, formal isomorphism/output definition, and clock semantics. Do not search generic mirrors; use a route exposing later OCR/pages.
3. **Hsieh–Tan–Newborn 1968 ACM paper:** corrected DOI `10.1145/800186.810626`; recover original proof if a genuine full-text route appears.
4. **Newborn–Arnold 1972:** bounded-signal-fanout theorem; title/author validate all retrieved copies.
5. **Williams 1975:** settle resynthesis.

Do not broaden this into another general modular-synthesis survey. The objective is only to decide the H1–H4 compiler reduction.

## 7. Decision rule

### A — H1–H4 all hold with comparable overhead

Demote bounded-local/logarithmic-access **existence** as residual mathematical novelty. Keep the relay for explicit architecture, sharp constants, and interpretation.

### B — H3 is only one-way

A classical simulator may preserve open distinctions while introducing spurious closed distinctions; it does not automatically reproduce the CCOC closed/open quotient gap.

### C — H1 holds but H2 or H4 grows with source state count

The simultaneous fixed-control/degree-three/radius-one/`Theta(log m)` relay can retain a quantitative realization distinction.

### D — incomplete-machine methods resynthesize hardware

Treat them as strong contextual-decomposition ancestry, not as the same fixed-hardware grammar-opening construction.

## 8. Canonical repository records

- `universal_compilation_reduction_risk.md` — corrected reduction
- this file — source evidence table
- `fixed_input_unit_delay_historical_risk_2026-08-12.md` — focused fixed-input warning
- `ullman_weiner_primary_ocr_2026-08-13.md` — primary OCR extraction
- issue #122 — live historical compiler gate
- issue #137 — Ullman–Weiner construction-page blocker

Secondary digests and abstract-style summaries are retained only as acquisition/claim-control leads; they do not substitute for primary theorem text.