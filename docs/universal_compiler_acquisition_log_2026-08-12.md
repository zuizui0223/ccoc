# Universal-compiler source acquisition log — 2026-08-12

> **Purpose.** Record the source-retrieval work behind issue #122 without
> upgrading theorem claims from titles, search snippets, or secondary summaries.
> This log distinguishes bibliographic/holding verification from full-text theorem
> extraction.

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

- The IEEE Transactions on Computers volume/issue bibliographic record is
  independently indexed in DBLP and library databases.
- The current search exposed publisher-link metadata but did not yield a readable
  primary full text through the available web path.

### Evidence status

No C1–C6 clause is upgraded from the title alone. In particular, “bounded signal
fan-out” is **not** silently interpreted as a complete bounded-degree compiler
contract, and “universal module” is **not** taken to imply fixed external input
semantics or bounded simulation slowdown.

### Next retrieval action

Acquire the IEEE full text through institutional access or document delivery and
extract:

- universal-module state count;
- input count and signal fan-out constants;
- source-input presentation/encoding;
- number of copies required versus source-machine size;
- clocking/simulation delay;
- output readout delay;
- whether one realized network can be evaluated under restricted input languages
  without recompilation.

## 3. Williams (1975)

Target:

> George H. Williams, *Uniform Decomposition of Incompletely Specified Sequential
> Machines*, IEEE Transactions on Computers, C-24(8):840–843, August 1975.

### Verified acquisition facts

- The title, author, issue, and page range are present in IEEE Transactions on
  Computers volume indexes and DBLP.
- The available search did not recover a readable primary full text in this pass.

### Why this source is decisive

This paper is the most dangerous historical intersection because it explicitly
combines **uniform decomposition** with **incomplete specification**. But no claim
is upgraded until the original four-page paper is read.

### Next retrieval action

Acquire the IEEE full text and determine whether incomplete specification is used
only to choose a smaller decomposition, or whether the same already-compiled
hardware supports both restricted and less-restricted input semantics. The latter
would bear directly on C6.

Also extract component state size, connectivity/fan-out, external input semantics,
copy-count growth, and clock/output delay.

## 4. Arnold, Tan & Newborn (1970)

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

## 5. Current novelty-control conclusion

The acquisition pass supports a narrower and cleaner status than a broad
literature-search statement:

1. **Known historical ancestry:** exact/contextual machine simplification,
   incomplete-specification decomposition, and repeated identical-module
   realization are all old ideas.
2. **Verified bounded-local risk:** Weiner–Hopcroft is a real, directly relevant
   historical construction and must be read before claiming bounded-local
   originality.
3. **Unresolved decisive clauses:** the current accessible evidence does not yet
   establish C3 + C5 + C6 simultaneously for a classical compiler.
4. **Therefore:** CCOC may describe its relay as an explicit extremal realization,
   but must not make a priority/firstness claim for bounded-local existence or
   logarithmic access until the three original texts above are extracted.

This is an acquisition result, not evidence that the missing clauses fail.

## 6. Reproducible source pointers

- Princeton archival finding aid:
  <https://findingaids.library.upenn.edu/records/PRIN_MUDD_ENG027>
- CiNii Books record for Weiner–Hopcroft report no. 61:
  <https://ci.nii.ac.jp/ncid/BA8670779X>
- IBM Research primary abstract for Arnold–Tan–Newborn (1970):
  <https://research.ibm.com/publications/iteratively-realized-sequential-circuits>
- DBLP IEEE Transactions on Computers volume 21 index:
  <https://dblp.org/db/journals/tc/tc21.html>
- DBLP IEEE Transactions on Computers volume 24 index:
  <https://dblp.org/db/journals/tc/tc24>

The DBLP/index links above are used only to locate bibliographic records and
publisher routes; they are not treated as substitutes for the original theorem
text.
