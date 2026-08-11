# Universal-compilation source acquisition and evidence audit

> **Status:** novelty-control evidence memo. This file records what has actually
> been verified from accessible sources for the compiler clauses in
> `universal_compilation_reduction_risk.md`. It is not a priority claim and it does
> not infer theorem properties from titles, snippets, or secondary summaries.

## 1. Question being audited

The residual CCOC bounded-local claim is at risk if a classical compiler maps an
arbitrary synchronous controlled finite-state machine to one fixed modular network
while satisfying all of the following:

- **C1 — constant local state:** component state size is bounded independently of
  the compiled machine size;
- **C2 — bounded local connectivity:** fan-in/fan-out or degree is bounded
  independently of machine size;
- **C3 — fixed external control semantics:** the external alphabet is preserved,
  or encoded over a fixed alphabet with explicit bounded overhead;
- **C4 — faithful behavioral simulation:** the compiled observable recovers the
  original controlled response on the comparison domain;
- **C5 — bounded time overhead:** original control words are simulated with an
  explicit constant/polylogarithmic or otherwise quantified slowdown;
- **C6 — restriction compatibility:** closed and open grammars are restrictions of
  the external language on the **same compiled hardware**, rather than requiring
  a newly compiled network for each context.

A source subsumes the current bounded-local existence claim only if enough of this
joint contract is actually established. Evidence for C1 or C2 alone is not enough.

## 2. Evidence table

Status vocabulary:

- **VERIFIED:** directly supported by the primary/authoritative material inspected;
- **PARTIAL:** a broader statement is supported, but not the quantitative clause
  needed by CCOC;
- **UNKNOWN:** the inspected material does not establish the clause;
- **NOT TARGETED:** the source addresses a different decomposition question.

| Source | Material directly inspected | C1 | C2 | C3 | C4 | C5 | C6 | Current verdict |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **Hsieh, Tan & Newborn (1968)**, *Uniform modular realization of sequential machines* | DBLP/DOI plus a contemporaneous IEEE literature digest; original ACM paper not yet inspected | PARTIAL | UNKNOWN | PARTIAL | PARTIAL | PARTIAL | UNKNOWN | **Major fixed-input/unit-delay risk.** Contemporary secondary evidence says unrestricted-input logical completeness at unit delay is impossible for a finite module set, but each fixed input dimension admits uniform modular realization. Since CCOC keeps its primitive control alphabet fixed as `m` grows, the positive fixed-input regime is directly relevant. Primary extraction is mandatory before upgrading C3/C5. |
| **Weiner & Hopcroft (1968)**, *Bounded Fan-in, Bounded Fan-out Uniform Decompositions of Synchronous Sequential Machines* | authoritative archival/catalog records; discoverable abstract reproduction, but no primary full text | PARTIAL | PARTIAL | UNKNOWN | PARTIAL | UNKNOWN | UNKNOWN | High-priority blocker. The available evidence supports a bounded-fan-in/out identical-small-module realization in broad terms, but does not settle input encoding, timing, output delay, or same-hardware grammar restriction. |
| **Ullman & Weiner (1969)**, *Uniform Synthesis of Sequential Circuits* | primary bibliographic/archive PDF route verified; article body could not be rendered by current screenshot backend; abstract-style publication record inspected | PARTIAL | UNKNOWN | PARTIAL | PARTIAL | PARTIAL | UNKNOWN | **Major fixed-input/fixed-module risk.** Abstract-style evidence explicitly places binary-input sequential machines in networks of a fixed module with delay and reports isomorphic realization with quantitative copy bounds. This makes fixed input + fixed module + delay unsafe as novelty language; bounded fanout/degree, exact semantic latency, and C6 remain unresolved. |
| **Arnold, Tan & Newborn (1970)**, *Iteratively Realized Sequential Circuits* | IBM Research primary abstract | UNKNOWN | UNKNOWN | UNKNOWN | PARTIAL | UNKNOWN | UNKNOWN | Primary abstract verifies realization of an arbitrary synchronous flow table as a regular array of identical modules. It does not provide the CCOC compiler constants or timing/restriction semantics. |
| **Newborn & Arnold (1972)**, *Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits* | authoritative bibliographic record/title only | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Title-level evidence is insufficient. Full theorem text is required before any C1–C6 upgrade. |
| **Williams (1975)**, *Uniform Decomposition of Incompletely Specified Sequential Machines* | authoritative bibliographic record; secondary abstract-style descriptions not treated as theorem evidence | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Particularly dangerous because incomplete specification and uniform decomposition meet in one paper, but the decisive compiler properties remain unverified. |
| **Jóźwiak & Ślusarczyk (2004)**, *General decomposition of incompletely specified sequential machines with multi-state behavior realization* | primary ScienceDirect article/abstract material | NOT TARGETED | PARTIAL | UNKNOWN | PARTIAL | PARTIAL | UNKNOWN | Confirms that incomplete-specification plus constrained network decomposition is mature prior art. It does not, in the inspected passages, establish the fixed identical-module compiler contract C1–C6. |

## 3. What the accessible sources establish

### 3.1 Hsieh–Tan–Newborn makes fixed input dimension a first-class historical parameter

DBLP verifies the 1968 ACM paper and DOI `10.1145/800186.810625`. A
contemporaneous IEEE *Abstracts of Current Computer Literature* digest reports the
paper's logical-completeness result in terms of **unit delay** and input dimension:
there is no finite universal module set covering arbitrary synchronous machines
at unit delay when the input dimension is unrestricted, while for each fixed input
count a finite uniform modular realization exists.

This is not yet primary-proof evidence, so exact module state count, interconnect,
fanout, and the formal definition of unit delay remain unresolved. But the result
already changes the novelty-control logic: CCOC's primitive alphabet is fixed at
four symbols as `m` grows, so one cannot appeal to the historical impossibility for
**unbounded** input dimension without first showing that it applies to the CCOC
fixed-input regime.

The detailed extraction questions and inference boundary are recorded in
`fixed_input_unit_delay_historical_risk_2026-08-12.md`.

### 3.2 Weiner–Hopcroft report exists, but the decisive full text was not obtained

The Princeton Digital Systems Laboratory archival record confirms the April 1968
report. The archival finding-aid route exposes catalog metadata rather than a
web-readable report, but it explicitly states that the Lewis Science and
Engineering Library accepts questions or digitization requests for the collection.
A CiNii bibliographic record independently identifies Digital Systems Laboratory
Technical Report no. 61 and lists a University of Tokyo General Library physical
holding, call number `U600:769`, record `0004766739`.

A discoverable abstract reproduction describes a general decomposition of a given
synchronous sequential machine into identical two-state modules with fan-in and
fan-out bounded independently of the original state count. Because that wording
was not recovered from the primary report itself in this pass, it is retained as
**supporting abstract evidence**, not as a completed theorem extraction.

Consequently the following remain unresolved from primary text:

1. whether an original external input symbol is supplied directly to the network
   or requires a machine-size-dependent code/distribution mechanism;
2. whether one source-machine clock step corresponds to one network step;
3. output decoding location and delay;
4. number of modules and network diameter/depth as functions of source size;
5. whether restricting the admissible external input language leaves the compiled
   hardware unchanged.

These are precisely C3, the quantitative part of C4, C5, and C6.

### 3.3 Ullman–Weiner confirms that fixed-module-with-delay synthesis is not a new axis

The Bell System Technical Journal bibliographic record places *Uniform Synthesis
of Sequential Circuits* at 48(5):1115–1127. The TCI/VTDA archives expose the exact
primary PDF path `bstj48-5-1115.pdf`; the current screenshot backend returned a
cache miss, so the paper body was not reconstructed from an unread PDF.

An abstract-style publication record states that the paper considers synthesis by
networks of a **fixed module with delay** and that every binary-input `n`-state
sequential machine has an isomorphic realization with an explicit finite bound on
copies of a module with `2r+1` inputs. The displayed copy-count formula is truncated
in the accessible rendering and is not quoted here.

This is enough for claim control: neither “binary/fixed input,” “one fixed module,”
nor “delay” can carry CCOC novelty in isolation. The primary paper is still needed
to determine fanout/local degree, semantic slowdown/output latency, and C6.

### 3.4 Arnold–Tan–Newborn gives genuine primary evidence for uniform modular realization

The IBM Research abstract states that synthesis techniques realize an arbitrary
synchronous flow table as an array of identical modules interconnected in a
regular pattern. This is enough to rule out novelty claims based merely on
“arbitrary synchronous behavior can be realized by repeated identical modules.”

It is not enough to infer constant component state, bounded degree, fixed input
encoding, one-clock simulation, output latency, or restricted-language
compatibility. Those remain UNKNOWN until the full construction is inspected.

### 3.5 The 2004 general decomposition theory blocks broad novelty claims

The primary 2004 article frames sequential-machine decomposition as replacement by
a network of collaborating partial machines, explicitly includes incompletely
specified machines, and treats structural/interconnection and implementation
quality constraints. This establishes mature ancestry for the broad combination

> incomplete or context-restricted behavior + constrained network decomposition.

It does **not** by itself settle whether a fixed two-state/bounded-degree universal
compiler preserves CCOC's restricted-versus-open external grammar with comparable
latency.

## 4. What has *not* been established

This audit has not found primary-text evidence that a classical construction
simultaneously satisfies C1–C6 with constant or polylogarithmic overhead.

Equally importantly, it has not established that no such theorem exists.

The Hsieh–Tan–Newborn and Ullman–Weiner lines make two earlier candidate
boundaries weaker than before: **fixed input dimension** and **fixed module with
delay** are themselves historical modular-synthesis themes. The residual question
therefore concentrates more strongly on the simultaneous bounded-resource and
same-hardware grammar contract.

Current manuscript-safe status:

> Classical sequential-machine theory already treats fixed-input uniform modular
> realization, fixed modules with delay, and bounded-fan-in/fan-out decomposition
> in closely related constructions. CCOC provides one explicit extremal
> restricted-to-open response separation under a degree-three, fixed-control
> realization. Whether that combined realization package follows from classical
> compilers with comparable external-input, timing, and same-hardware restriction
> semantics remains an open historical-comparison question.

No priority or firstness claim should be made while C3/C5/C6 remain unresolved.

## 5. Decisive acquisition order

A dated, reproducible acquisition/search log is maintained in
`universal_compiler_acquisition_log_2026-08-12.md`. The focused fixed-input/unit-
delay risk is recorded in `fixed_input_unit_delay_historical_risk_2026-08-12.md`.

### Priority 1 — Hsieh, Tan & Newborn (1968)

Obtain DOI `10.1145/800186.810625` and extract the original definition of input
count, unit delay, universal module dependence on input dimension, fan-in/fan-out,
and external-input interconnection. This source now directly controls whether C3
and C5 remain meaningful standalone distinctions at fixed input dimension.

### Priority 2 — Weiner & Hopcroft (1968)

Acquisition routes already verified:

- Princeton Lewis Science and Engineering Library collection;
- University of Tokyo General Library, `U600:769`, record `0004766739`.

Extract literally from the report:

- component state count;
- exact fan-in/fan-out constants;
- component count as a function of source machine size and input alphabet;
- external input distribution/encoding;
- clocking and slowdown;
- output readout/decoding delay;
- network depth/diameter if specified;
- whether a single compiled network can be evaluated under a restricted subset or
  language of the original external inputs without recompilation.

### Priority 3 — Ullman & Weiner (1969)

The exact primary PDF route is known:

`https://vtda.org/pubs/BSTJ/vol48-1969/articles/bstj48-5-1115.pdf`

Extract the module definition, the parameters `r`, `p`, the exact module-copy
bound, the formal delay semantics, interconnection/fanout restrictions, and any
external-input encoding/distribution assumptions.

### Priority 4 — Newborn & Arnold (1972)

Request the exact paper:

> Monroe M. Newborn and Thomas F. Arnold, *Universal Modules for Bounded Signal
> Fan-Out Synchronous Sequential Circuits*, IEEE Transactions on Computers,
> 21(1):63–79, 1972, DOI `10.1109/T-C.1972.223432`.

Determine whether it strengthens the 1968 constructions on input distribution,
module universality, fan-out constants, or simulation timing.

### Priority 5 — Williams (1975)

Request:

> George H. Williams, *Uniform Decomposition of Incompletely Specified Sequential
> Machines*, IEEE Transactions on Computers, 24(8):840–843, 1975.

Because the paper explicitly concerns incompletely specified sequential machines,
extract whether one compiled architecture is reused across restrictions or whether
component count/wiring/control interface is resynthesized from the partial
specification. This is the decisive C6 question.

## 6. Decision rule after full-text extraction

1. **C1–C6 with constant or comparable logarithmic overhead:** stop presenting
   bounded-local existence/logarithmic access as residual mathematical novelty.
   Keep the relay as an explicit sharp construction and shift the manuscript claim
   to the exact causal-interface accounting/ecological synthesis or to a genuinely
   stronger theorem target.
2. **Fixed-input/fixed-module unit-delay synthesis is classical, but bounded fanout,
   fixed controls, and C6 do not coexist:** narrow the residual realization claim
   to that simultaneous constrained package; do not market C3 or C5 alone.
3. **Williams or another classical construction already gives one fixed
   input-preserving bounded-local hardware network supporting both restricted and
   opened grammars:** demote the structural restricted→open realization claim and
   retain only the extremal response-quotient accounting/construction as appropriate.

## 7. Source pointers

- Hsieh–Tan–Newborn DBLP record:
  <https://dblp.org/rec/conf/acm/HsiehTN68>
- Hsieh–Tan–Newborn DOI:
  <https://doi.org/10.1145/800186.810625>
- Ullman–Weiner Bell System Technical Journal issue:
  <https://onlinelibrary.wiley.com/toc/15387305c/1969/48/5>
- Ullman–Weiner primary PDF archive:
  <https://vtda.org/pubs/BSTJ/vol48-1969/articles/bstj48-5-1115.pdf>
- Bell System bibliography with historical article PDF paths:
  <https://ftp.math.utah.edu/pub/tex/bib/bstj1960.html>
- IBM Research, Arnold–Tan–Newborn (1970):
  <https://research.ibm.com/publications/iteratively-realized-sequential-circuits>
- Princeton archival finding-aid record containing the Weiner–Hopcroft report:
  <https://findingaids.library.upenn.edu/records/PRIN_MUDD_ENG027>
- CiNii bibliographic record for the Weiner–Hopcroft technical report:
  <https://ci.nii.ac.jp/ncid/BA8670779X>
- Newborn–Arnold DOI:
  <https://doi.org/10.1109/T-C.1972.223432>
- ScienceDirect, Jóźwiak–Ślusarczyk (2004):
  <https://www.sciencedirect.com/science/article/abs/pii/S1383762103001929>

Secondary abstract/digest records remain claim-control aids, not substitutes for
primary theorem text.