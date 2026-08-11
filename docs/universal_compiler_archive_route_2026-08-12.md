# Universal-compiler preserved archive route — 2026-08-12

> **Status:** primary-source acquisition record for issue #122. This file records
> verified preservation/access routes for the old IEEE Transactions on Computers
> material needed by the C3/C5/C6 novelty gate. Preservation does not by itself
> verify any compiler clause.

## 1. Verified preservation route

The ISSN International Centre record for the online IEEE Transactions on Computers
(ISSN `1557-9956`, ISSN-L `0018-9340`) links the journal to IEEE Xplore, Scholars
Portal, Internet Archive, and Portico.

Its Keepers archival-status table reports:

- **Scholars Portal:** preserved from 1968 through 2026;
- **Internet Archive:** preserved from 1952 through 2003;
- **Portico:** preserved from 1968 through 2021.

The same record explicitly lists the old volume/issue ranges needed for the CCOC
novelty audit, including:

- 1972: `C-21(1–12)`;
- 1975: `C-24(1–12)`;
- 1978: `C-27(1–12)`;
- 1982: `C-31(1–12)`.

The Internet Archive journal collection linked by the ISSN record is:

`https://archive.org/details/pub_ieee-transactions-on-computers`

The current automated web environment reaches the collection landing page but the
issue/item list requires JavaScript and could not be enumerated here. This is a
**tool/UI limitation**, not evidence that the preserved issue scans are absent.

## 2. Exact issue-level retrieval targets

The next manual/browser or archive-API retrieval pass should look for these issues
inside the preserved collection.

### `C-21(1)` — January 1972

Primary C3/C5 target:

> Monroe M. Newborn and Thomas F. Arnold, *Universal Modules for Bounded Signal
> Fan-Out Synchronous Sequential Circuits*, pp. 63–79,
> DOI `10.1109/T-C.1972.223432`.

**DOI correction.** A previous version of this acquisition record incorrectly used
`10.1109/T-C.1972.223521`. DBLP's actual electronic-edition links show that
`223432` is the Newborn–Arnold article, whereas `223521` belongs to Kim–Newborn,
*The Simplification of Sequential Machines with Input Restrictions*, 21(12):
1440–1443 (1972).

Extract C1/C2/C3/C5/C6 details, especially module input count, source-input
presentation, clocking, output latency, and whether input-language restriction can
be imposed on one fixed realization.

### `C-24(8)` — August 1975

Primary C6 target:

> George H. Williams, *Uniform Decomposition of Incompletely Specified Sequential
> Machines*, pp. 840–843.

Primary C5 target in the **same issue**:

> Tiu Le Van and Noël van Houtte, *Delayed Universal Logic Modules and Sequential
> Machine Synthesis*, pp. 853–855.

Retrieving one preserved issue scan can therefore resolve two major branches of
#122 at once: Williams for same-hardware restriction versus specification-dependent
re-synthesis, and Le Van–van Houtte for the meaning and quantitative role of delay.

### `C-27(2)` — February 1978

Correction/critique target:

> Sureshchander, *Comments on “Delayed Universal Logic Modules and Sequential
> Machine Synthesis”*, p. 191.

The purpose is to determine exactly what part of the 1975 construction was being
corrected or challenged. The existence of the comment is not itself negative
evidence.

### `C-27(10)` — October 1978

Comparison/implementation target:

> A. E. A. Almaini, *Sequential Machine Implementations Using Universal Logic
> Modules*, pp. 951–960.

Extract whether implementation cost is measured by module count, levels/depth,
clock steps, output delay, input count, or another resource relevant to C3/C5.

### `C-31(2)` — February 1982

Comparison target:

> X. Chen and Stanley L. Hurst, *A Comparison of Universal-Logic-Module
> Realizations and Their Application in the Synthesis of Combinatorial and
> Sequential Logic Networks*, pp. 140–147.

Use the primary paper to translate the old universal-module vocabulary into
explicit input/depth/delay/resource metrics without relying on later patents or
secondary summaries.

## 3. Separate non-journal target

The Weiner–Hopcroft 1968 report is not resolved by the journal preservation route:

> Peter Weiner and John E. Hopcroft, *Bounded Fan-in, Bounded Fan-out Uniform
> Decompositions of Synchronous Sequential Machines*, Princeton Digital Systems
> Laboratory Technical Report no. 61.

Its independent acquisition routes remain:

- University of Tokyo General Library: call number `U600:769`, record
  `0004766739`;
- Princeton Lewis Science and Engineering Library / archival digitization route.

This report remains the most direct generic-compiler risk and should still be read
alongside the preserved IEEE issue scans.

## 4. Acquisition status versus evidence status

The archive discovery changes **retrievability**, not theorem evidence.

Current compiler-clause statuses remain:

- C3 external-control/input semantics: `UNKNOWN` for the decisive classical
  compiler family;
- C5 semantic source-step → local-network-round/output delay: `UNKNOWN`;
- C6 same compiled hardware under restricted/open grammars: `UNKNOWN`.

No clause should be upgraded until the relevant primary construction is read and
quoted/paraphrased into the extraction table.

## 5. Recommended retrieval order

Because one preserved issue contains both Williams and Le Van–van Houtte, the most
efficient order is now:

1. **Internet Archive `C-24(8)` (Aug. 1975)** — resolve the strongest C6 and C5
   leads together;
2. **Internet Archive `C-21(1)` (Jan. 1972)** — Newborn–Arnold C3/input/fanout and
   timing contract;
3. **Weiner–Hopcroft report no. 61** — generic bounded-fan-in/out compiler
   semantics and overhead;
4. **Internet Archive `C-27(2)` (Feb. 1978)** — read the correction/comment;
5. **Internet Archive `C-27(10)` and `C-31(2)`** — later resource comparisons;
6. **Huang–Kain–Kinney SWAT 1972** — non-journal C3/input-count result via DOI or
   institutional proceedings access.

This order maximizes the chance of resolving C3/C5/C6 with the fewest primary
source retrievals.

## 6. Source pointers

- ISSN International Centre journal record / Keepers status:
  `https://portal.issn.org/resource/ISSN/1557-9956`
- Internet Archive preserved journal collection:
  `https://archive.org/details/pub_ieee-transactions-on-computers`
- Newborn–Arnold DOI:
  `https://doi.org/10.1109/T-C.1972.223432`
- Kim–Newborn input-restriction DOI (to prevent future remapping confusion):
  `https://doi.org/10.1109/T-C.1972.223521`
- Huang–Kain–Kinney DOI:
  `https://doi.org/10.1109/SWAT.1972.17`
- Weiner–Hopcroft CiNii Books record:
  `https://ci.nii.ac.jp/ncid/BA8670779X`

The preservation claim is based on the Keepers record. Individual issue scans
still need item-level retrieval and inspection.