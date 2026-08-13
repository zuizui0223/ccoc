# Primary-source request handoff — 2026-08-13

> **Purpose.** Reduce issue #122's remaining historical gate to the smallest set of human acquisition actions. All broad web/mirror searching is finished. This file contains only request metadata and the H1–H4 extraction order once copies arrive.

## Why these requests matter

The residual CCOC realization claim is conditional on whether one classical compiler jointly provides:

- **H1:** bounded local state/connectivity independent of source state count;
- **H2:** fixed context-independent source controls/input distribution;
- **H3:** two-way response-trace faithfulness at the designated external output;
- **H4:** bounded source-step/network/output latency.

Titles, abstracts, holdings, and automatic non-retrieval do not decide these clauses. The construction pages do.

## Request A — Osaka Prefectural Central Library: Newborn–Arnold 1972

### Exact article

- journal: `IEEE Transactions on Computers`
- volume/issue: `C-21(1)` / volume 21, number 1
- date: January 1972
- authors: Monroe M. Newborn; Thomas F. Arnold
- title: `Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits`
- pages: `63–79`
- DOI: `10.1109/T-C.1972.223433`
- CiNii holding: `AA00667773`
- holding coverage: 大阪府立中央図書館, 1969–1973

### Route

Use the Osaka Prefectural Library Web-copy service. The current route permits remote requests, including a one-time/no-registration path, with postal delivery. Final copying is subject to the library's copyright/source-condition decision.

Current ordinary-library postal-copy pricing recorded in the audit:

- black-and-white: 30 yen per copied sheet;
- color: 100 yen per copied sheet;
- actual postage;
- 100-yen dispatch charge for up to 50 sheets, with additional handling by 50-sheet blocks;
- final sheet count and charge are quoted by the library and prepaid before copying.

Do not estimate the final total from the journal page count; physical copied-sheet count and postage are determined by the library.

### First extraction on receipt

Read in this order:

1. exact universal-module state count and input/output arity;
2. signal fan-out and fan-in/interconnection constants;
3. dependence of those constants on source **state count** versus source **input count**;
4. external source-input wiring/distribution;
5. formal definition of realization/equivalence and designated outputs;
6. clock/delay/settling semantics;
7. module-count and depth/diameter bounds.

This is the highest-value direct test of H1/H2.

## Request B — Osaka Prefectural Central Library: Drilman–Weiner 1972

### Exact article

- journal: `IEEE Transactions on Computers`
- volume/issue: `C-21(10)` / volume 21, number 10
- date: October 1972
- authors: J. Drilman; Peter Weiner
- title: `Modular Networks and Nondeterministic Sequential Machines`
- pages: `1124–1129`
- IEEE Xplore article number: `1672054`
- DBLP key: `journals/tc/DrilmanW72`
- CiNii holding: `AA00667773`

**Do not add a DOI unless independently verified.** The audit intentionally leaves it unset; a nearby DOI was previously easy to misassign.

### Route

Use the same Osaka Web-copy service. Do not assume that separate applications will share one postage charge; the library may dispatch them separately.

### First extraction on receipt

1. exact definition of the `r`-bounded nondeterministic sequential machine;
2. relation between the nondeterministic specification and deterministic realizations/refinements;
3. whether multiple refinements share one fixed modular network or require resynthesis;
4. formal definition and resources of `M_{r,p}`;
5. source input presentation/distribution;
6. designated output/equivalence semantics;
7. timing/latency;
8. module-count/depth dependence.

This is the most direct early test of whether fixed-module synthesis and incomplete/nondeterministic behavior already coexist under one fixed-hardware semantics.

## Request C — University of Tokyo / Princeton: Weiner–Hopcroft report no. 61

### Exact item

- authors: Peter Weiner; John E. Hopcroft
- title: `Bounded fan-in, bounded fan-out uniform decompositions of synchronous sequential machines`
- institution: Princeton University, Digital Systems Laboratory
- report: Technical Report no. 61
- date: April 1968
- extent: 7 pages + 3 leaves of plates
- University of Tokyo General Library call no.: `U600:769`
- item: `0004766739`
- NCID: `BA8670779X`

### Route

For remote use, the University of Tokyo General Library directs external users to place photocopy requests **through a library**. An academic/university library can use NACSIS-ILL; a public library can also request photocopy through interlibrary procedures. The audit records General Library participant ID `FA001787`.

Alternative route: Princeton archival/library digitization inquiry.

Request the **complete item including all three plates**, subject to copyright/library policy.

### First extraction on receipt

1. module state cardinality and I/O arity;
2. exact fan-in/fan-out constants;
3. external input terminal wiring/distribution;
4. formal realization/equivalence definition;
5. designated output terminals;
6. source clock/module clock/delay convention;
7. source-step to output-valid latency;
8. module-count bound;
9. network depth/diameter if stated;
10. dependence on source state count versus source input count.

This is the strongest historical H1 source.

## Request/visit D — Tokyo University of Technology: IEEE TC C-24(8), August 1975

### Two articles in one issue

1. George H. Williams, `Uniform Decomposition of Incompletely Specified Sequential Machines`, pp. `840–843`.
2. Tiu Le Van; Noël van Houtte, `Delayed Universal Logic Modules and Sequential Machine Synthesis`, pp. `853–855`.

CiNii records Tokyo University of Technology Media Center Library holding `IEEE Transactions on Computers` for 1968–2017.

### Route

Current external-user guidance permits on-site viewing/copying of physical books and journals. Affiliates of a non-partner university are instructed to bring an introduction letter from their home-university library. Current copy-machine charge recorded by the audit is 10 yen per sheet; old-periodical individual articles may be copied in full for research use subject to the library's copyright rules.

### First extraction on receipt

For **Williams**:

1. exact incomplete-machine semantics;
2. what is recomputed when the incomplete specification changes;
3. whether component count/wiring/control network is resynthesized per specification;
4. whether one full network can instead be held fixed while only admissible behavior changes;
5. universal component resources and interconnection restrictions.

For **Le Van–van Houtte**:

1. formal definition of `delay`;
2. source/module clock relation;
3. output-validity/settling interval;
4. number of stages/delays per simulated source step;
5. dependence on source state count/input count/network depth;
6. designated external output semantics.

## Follow-up only after the 1975 issue is read

The same Tokyo holding covers:

- Sureshchander (1978) comment, C-27(2):191;
- Almaini (1978), C-27(10):951–960;
- Chen & Hurst (1982), C-31(2):140–147.

Use these to interpret/correct/resource-compare the 1975 construction. Do not substitute later papers for the original construction pages.

## Ullman–Weiner 1969 special case

The exact 14-page BSTJ article and exact Internet Archive item identifier `bstj48-5-1115` are already resolved. Primary abstract/introduction text is already admitted. The only remaining need is a renderable/searchable copy of the **construction pages** covering fan-out, input distribution, formal isomorphism/output, clocking, and delay.

If a verified scan of those pages becomes available, no new literature search is needed; go directly to H1–H4 extraction.

## Admission rule for all recovered files

Before using a recovered copy as evidence:

1. verify title, authors, volume/report, year, and page range;
2. retain provenance/source route;
3. do not infer missing clauses from title or abstract;
4. extract H1–H4 literally/structurally from the primary construction;
5. update issue #122 and the canonical source audit only after the relevant passage is actually read.

## Definition of done

The historical gate can be decided when at least one full-language compiler is mapped convincingly to all H1–H4, or when the closest primary constructions are read and each fails a required clause for a documented reason. Automatic non-retrieval is never such a failure.