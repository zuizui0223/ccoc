# Universal-compiler source acquisition log — 2026-08-12

> **Purpose.** Record the source-retrieval work behind issue #122 without
> upgrading theorem claims from titles, search snippets, or secondary summaries.
> This log distinguishes bibliographic/holding verification from full-text theorem
> extraction. Directional secondary leads are recorded separately from verified
> compiler-contract statuses.

## 1. Weiner & Hopcroft (1968)

Target:

> Peter Weiner and John E. Hopcroft, *Bounded Fan-in, Bounded Fan-out Uniform
> Decompositions of Synchronous Sequential Machines*, Digital Systems Laboratory
> Technical Report no. 61, Princeton University, April 1968; later summarized in
> *Proceedings of the IEEE* 56(7):1219–1220.

### Verified acquisition facts

- The Princeton Computer Sciences Laboratory archival finding aid contains the
  April 1968 report as one physical item.
- The CiNii Books record identifies the report as Digital Systems Laboratory
  Technical Report no. 61, 7 pages plus plates, and lists one physical holding:
  University of Tokyo General Library, call number `U600:769`, record
  `0004766739`.
- The Princeton finding aid exposes the archival collection, but the report itself
  was not recovered as a web-readable scan in this pass.

### Evidence status

The original report text has **not** yet been inspected. Therefore C3 (external
input encoding/distribution), C5 (clock/time overhead), C6 (same-hardware input
restriction compatibility), module count, network diameter, and output decoding
latency remain unresolved.

### Next retrieval action

Obtain the physical/digitized report through either:

1. University of Tokyo General Library (`U600:769`, `0004766739`); or
2. Princeton Lewis Science and Engineering Library / archival digitization route.

The extraction template in `universal_compilation_source_audit.md` should then be
filled literally from the report.

## 2. Newborn & Arnold (1972)

Target:

> Monroe M. Newborn and Thomas F. Arnold, *Universal Modules for Bounded Signal
> Fan-Out Synchronous Sequential Circuits*, IEEE Transactions on Computers,
> C-21(1):63–79, January 1972.

### Verified acquisition facts

- DBLP's actual electronic-edition link for this record resolves to the primary DOI
  **`10.1109/T-C.1972.223432`** and also exposes IEEE Computer Society,
  Unpaywall, and Internet Archive Scholar routes.
- A previous version of this log incorrectly assigned DOI
  `10.1109/T-C.1972.223521` to Newborn–Arnold. Expanding the adjacent DBLP records
  shows that **`10.1109/T-C.1972.223521` belongs to Joonki Kim and Monroe M.
  Newborn, *The Simplification of Sequential Machines with Input Restrictions*,
  IEEE Transactions on Computers 21(12):1440–1443 (1972)**. The mapping is
  corrected here rather than silently retained.
- The available web client did not recover the Newborn–Arnold primary article from
  the DOI, IEEE, Unpaywall, or Internet Archive Scholar routes in this pass. This is
  a retrieval failure only; it is **not** evidence that no open or institutionally
  accessible copy exists.
- The exact title, authors, issue, and page range are independently indexed in
  DBLP and library databases.

### Evidence status

No C1–C6 clause is upgraded from the title or DOI metadata alone. In particular,
“bounded signal fan-out” is **not** silently interpreted as a complete
bounded-degree compiler contract, and “universal module” is **not** taken to imply
fixed external input semantics or bounded simulation slowdown.

### Next retrieval action

Acquire DOI `10.1109/T-C.1972.223432` through institutional IEEE access, document
delivery, Internet Archive preservation, or a verified author/archive copy and
extract:

- universal-module state count;
- input count and signal fan-out constants;
- source-input presentation/encoding;
- number of copies required versus source-machine size;
- clocking/simulation delay;
- output readout delay;
- whether one realized network can be evaluated under restricted input languages
  without recompilation.

## 3. Huang, Kain & Kinney (1972) — focused C3 lead

Target:

> C. C. Huang, Richard Y. Kain, and Larry L. Kinney, *Output Sufficient Modules
> for Uniform Decomposition of Synchronous Sequential Circuits*, 13th Annual
> Symposium on Switching and Automata Theory (SWAT), 1972, pp. 192–199,
> DOI `10.1109/SWAT.1972.17`.

### Verified acquisition facts

- DBLP indexes the paper and the DOI route.
- The paper is directly adjacent to the Newborn–Arnold universal-module line.
- A readable primary full text was not recovered in this pass.

### Secondary directional lead — not theorem evidence

An abstract-style secondary record says that the paper studies how many inputs a
universal/output-sufficient module must have and reports input-count growth with
the number of inputs of the sequential machines to be realized.

This is potentially decisive for **C3** because classical bounded-module
realization may pay for universality through a growing module/input interface even
when local state or fanout is bounded. But the secondary wording does not identify
whether the counted inputs are external controls, intermodule signals, or both,
and it does not rule out a separate fixed-alphabet bounded-overhead encoder.

Therefore C3 remains `UNKNOWN`.

### Next retrieval action

Acquire DOI `10.1109/SWAT.1972.17` and extract literally:

- formal definitions of universal and output-sufficient modules;
- the exact input-count bound and scaling parameter;
- whether counted inputs are source controls, intermodule signals, or both;
- source-alphabet encoding/distribution;
- timing overhead of any encoding;
- the exact dependence on Newborn–Arnold (1972).

Detailed decision logic is recorded in
`universal_compiler_c3_c6_directional_leads_2026-08-12.md`.

## 4. Williams (1975) — focused C6 lead

Target:

> George H. Williams, *Uniform Decomposition of Incompletely Specified Sequential
> Machines*, IEEE Transactions on Computers, C-24(8):840–843, August 1975.

### Verified acquisition facts

- The title, author, issue, and page range are present in IEEE Transactions on
  Computers volume indexes and DBLP.
- DBLP exposes DOI/IEEE/unpaywall routing, but a readable primary full text was not
  recovered through the available web path in this pass.

### Why this source is decisive

This paper is the most dangerous historical intersection because it explicitly
combines **uniform decomposition** with **incomplete specification**. But no C6
claim is upgraded until the original four-page paper is read.

A secondary abstract-style copy describes a reduction in the number of universal
two-state component copies found by a minimal-cover search over partial mappings.
That wording points directionally toward **specification-dependent synthesis or
optimization**, rather than automatically establishing CCOC's C6 requirement of
one already-compiled network whose admissible external language is merely
restricted/opened. The wording remains a search lead only.

### Next retrieval action

Acquire the IEEE full text and determine whether incomplete specification is used
only to synthesize a smaller decomposition, or whether the same already-compiled
hardware supports both restricted and less-restricted input semantics.

Extract:

- what is held fixed when the incomplete specification changes;
- whether component count/wiring/control interface changes;
- whether a less-restricted realization can be restricted without recompilation;
- whether a restricted realization can be opened without structural change;
- component state size and connectivity/fanout;
- external input semantics, copy-count growth, clocking, and output delay.

Detailed decision logic is recorded in
`universal_compiler_c3_c6_directional_leads_2026-08-12.md`.

## 5. Arnold, Tan & Newborn (1970)

Target:

> Thomas F. Arnold, Chung-Jen Tan, and Monroe M. Newborn, *Iteratively Realized
> Sequential Circuits*, IEEE Transactions on Computers 19(1):54–66, 1970.

### Primary evidence obtained

IBM Research provides an authoritative primary abstract stating that synthesis
techniques realize an arbitrary synchronous flow table as an array of identical
modules interconnected in a regular pattern.

This is sufficient to reject novelty language based solely on arbitrary
synchronous behavior plus repeated identical modules.

It is **not** sufficient to establish constant module state size, bounded degree,
fixed external-input encoding, one-source-clock-per-network-step simulation,
output delay, or C6.

The DOI route previously identified for the journal article is
`10.1109/TC.1970.5008900`; the full construction still needs inspection.

## 6. Current novelty-control conclusion

The acquisition pass now supports a resource-specific rather than keyword-level
historical comparison:

1. **Known historical ancestry:** exact/contextual machine simplification,
   incomplete-specification decomposition, and repeated identical-module
   realization are old ideas.
2. **Verified bounded-local risk:** Weiner–Hopcroft is a real, directly relevant
   historical construction and must be read before claiming bounded-local
   originality.
3. **C3 focus:** Newborn–Arnold plus Huang–Kain–Kinney must be checked for where
   source-input complexity is paid and whether a fixed external alphabet with
   bounded overhead survives the universal-module construction.
4. **C6 focus:** Williams must be checked for same-hardware input-language
   restriction versus specification-dependent re-synthesis.
5. **C5 remains open:** clocking, slowdown, output latency, and network depth still
   require primary construction details.
6. **Therefore:** CCOC may describe its relay as an explicit extremal realization,
   but must not make a priority/firstness claim for bounded-local existence or
   logarithmic access while C3/C5/C6 remain unresolved.

This is an acquisition result, not evidence that the missing clauses fail.

## 7. Reproducible source pointers

- Princeton archival finding aid:
  <https://findingaids.library.upenn.edu/records/PRIN_MUDD_ENG027>
- CiNii Books record for Weiner–Hopcroft report no. 61:
  <https://ci.nii.ac.jp/ncid/BA8670779X>
- DBLP Newborn–Arnold record:
  <https://dblp.org/rec/journals/tc/NewbornA72>
- Newborn–Arnold DOI:
  <https://doi.org/10.1109/T-C.1972.223432>
- DBLP Kim–Newborn input-restriction record (for the corrected adjacent DOI
  mapping):
  <https://dblp.org/rec/journals/tc/KimN72>
- Huang–Kain–Kinney DOI:
  <https://doi.org/10.1109/SWAT.1972.17>
- DBLP Williams record:
  <https://dblp.org/rec/journals/tc/Williams75>
- IBM Research primary abstract for Arnold–Tan–Newborn (1970):
  <https://research.ibm.com/publications/iteratively-realized-sequential-circuits>
- ScienceDirect, Jóźwiak–Ślusarczyk (2004):
  <https://www.sciencedirect.com/science/article/abs/pii/S1383762103001929>

Bibliographic/DOI/index routes are used to locate the original works. Secondary
abstract-style pages are used only to sharpen extraction questions and are not
substitutes for primary theorem text.
