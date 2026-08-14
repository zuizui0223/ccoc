# Short compiler-source acquisition addendum — 2026-08-14

> **Purpose:** reduce the remaining H1–H4 acquisition risk by adding short or predecessor primary sources that may settle one compiler clause sooner than the longer report/paper targets. This document adds acquisition targets only. No H1–H4 cell is upgraded until the primary body is actually read.

## 1. Weiner & Hopcroft (1968) — two-page Proceedings of the IEEE version

A same-title journal short version is bibliographically indexed as:

- Peter Weiner; J. E. Hopcroft
- *Bounded fan-in, bounded fan-out uniform decompositions of synchronous sequential machines*
- *Proceedings of the IEEE* 56(7), 1968, pp. 1219–1220

Secondary indexing reproduces an abstract-style description of a general decomposition into identical two-state modules with fan-in/fan-out bounds independent of the number of states in the source machine. That description is a **lead only** and is not admitted as H1 evidence until the two original IEEE pages are read.

### Domestic acquisition route

CiNii Journals records *Proceedings of the IEEE* under NCID `AA00783901` with extensive Japanese holdings. Several holdings explicitly cover volume 56 issue 7 or all of volume 56, so the two-page H1 source can be requested domestically rather than waiting for a publisher download. Examples visible in the current catalogue include:

- Tohoku University Engineering Library: `51-89`;
- Tohoku University Research Institute of Electrical Communication Library: `51-103`;
- Tohoku University Institute of Multidisciplinary Research for Advanced Materials Library: `51-58` (therefore volume 56 is included);
- Kobe University Library for Maritime Sciences: `56(7-12)`;
- Saga University Library: `56(7-12)`;
- Tokyo Gakugei University Library: `56-82`;
- Institute of Industrial Science Library, the University of Tokyo: `51-85`;
- Saitama University Library: volumes including `53-58`;
- National Astronomical Observatory of Japan, Mizusawa VLBI Observatory: `56-100`.

Tohoku University's current Engineering Library portal also lists **IEEE Xplore Digital Library** and explicitly includes *Proceedings of the IEEE* among its IEEE resources. A library notice identifies the physical *Proceedings of the IEEE* holding with the Research Institute of Electrical Communication library. This does not guarantee that the 1968 article is electronically licensed, but it makes the fastest check:

1. search the exact title in institutional IEEE Xplore access;
2. if unavailable electronically, check/request the RIEC physical backfile for Vol. 56, No. 7;
3. only then use domestic ILL.

The exact article pages **1219–1220**, not the secondary abstract, are the evidence target.

### Acquisition use

Acquire this two-page item before or in parallel with Technical Report no. 61. The short paper may settle H1 quickly; report no. 61 remains the preferred construction source for H2–H4, input distribution, designated outputs, timing, module count, and diagrams.

### Admission rule

- verify title/authors/volume/issue/pages from the recovered primary copy;
- do **not** guess or add a DOI unless independently verified from an authoritative record;
- extract the exact module-state, fan-in, and fan-out statement with page number;
- do not infer H2–H4 from the short abstract.

## 2. Weiner & Hopcroft (1967) — predecessor construction semantics

Bibliographic target:

- Peter Weiner; John E. Hopcroft
- *Modular Decomposition of Synchronous Sequential Machines*
- 1967 IEEE Symposium on Switching and Automata Theory, pp. 233–239
- authoritative bibliographic DOI route: `10.1109/FOCS.1967.19`

This predecessor is not a substitute for the 1968 bounded-fan-in/fan-out result. Its value is narrower: it may expose the authors' explicit meaning of module interconnection, external input terminals, realization/equivalence, and designated outputs.

### Domestic conference-record route

CiNii Books records the complete 1967 IEEE conference record (335 pages; NCID `BA16385655`) at multiple Japanese libraries. Current listed holdings include:

- Osaka University Science and Engineering Library;
- Kansai University Library;
- Kyushu University Science and Technology Library;
- Kyoto University Research Institute for Mathematical Sciences Library;
- Institute of Industrial Science Library, the University of Tokyo;
- University of Tokyo Graduate School of Information Science and Technology / CS library;
- Hiroshima University East Library.

A separate in-house reproduction record (NCID `BA87672533`) is listed at Ibaraki University Library, Hitachi Branch.

For ILL, request the conference record pages **233–239** by exact title/authors. This domestic route is now preferred over waiting for the IEEE electronic edition when only H2/H3 construction semantics are needed.

### Extraction priority

1. exact rule for what a component input terminal may connect to;
2. treatment of external source inputs versus internal component outputs/constants;
3. formal definition of decomposition/realization;
4. designated external outputs and whether internal signals are observationally hidden;
5. timing or delay semantics if present.

Use it primarily to illuminate H2/H3 terminology. Do not transfer resource bounds from the 1967 construction into the 1968 theorem without an explicit statement.

## 3. Hsieh, Tan & Newborn (1968) — fixed-input / unit-delay source

Bibliographic target:

- Edward P. Hsieh; Chung-Jen Tan; Monroe M. Newborn
- *Uniform modular realization of sequential machines*
- ACM National Conference 1968, pp. 613–621
- DOI `10.1145/800186.810626`

This source is high-value because CCOC keeps the primitive source-input dimension fixed as the hidden-state parameter grows. Existing contemporaneous/secondary evidence indicates that the fixed-input regime is historically the dangerous positive regime for uniform modular realization, but the original ACM body has not yet been recovered.

### Extraction priority

1. exact fixed source-input-count assumption;
2. universal-module state/input/output resources as a function of that fixed input count;
3. interconnection/fan-out restrictions;
4. external input distribution;
5. unit-delay / source-step timing semantics;
6. formal output realization/equivalence.

Do not upgrade H2 or H4 until these clauses are read in the primary paper.

## 4. Updated acquisition ordering

The primary gate should now be attacked in two lanes.

### Lane A — fastest H1 settlement

1. Weiner–Hopcroft 1968 Proceedings short version, pp. 1219–1220 — **Tohoku institutional IEEE Xplore -> RIEC physical backfile -> domestic ILL**;
2. Weiner–Hopcroft report no. 61, including all three plates;
3. Newborn–Arnold 1972, pp. 63–79.

### Lane B — H2/H3/H4 semantics

1. Weiner–Hopcroft 1967 predecessor, pp. 233–239 — **domestic conference-record ILL first**;
2. Ullman–Weiner 1969 construction pages;
3. Hsieh–Tan–Newborn 1968, pp. 613–621;
4. Le Van–van Houtte 1975 timing paper;
5. Williams 1975 / Drilman–Weiner 1972 for fixed-hardware versus resynthesis questions.

## 5. Decision discipline

These extra targets shorten the route to a decision; they do not broaden the historical survey. Stop after the joint H1–H4 compiler contract is either verified or one required clause fails for a documented primary-text reason. Non-retrieval is never a clause failure.

Tracking: issue #122 (historical gate), issue #185 (execution checklist), `primary_compiler_request_packet_2026-08-14.md` (main request packet).