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
| Weiner & Hopcroft (1968), *Bounded Fan-in, Bounded Fan-out Uniform Decompositions of Synchronous Sequential Machines* | authoritative archival/catalog records; discoverable abstract reproduction, but no primary full text | PARTIAL | PARTIAL | UNKNOWN | PARTIAL | UNKNOWN | UNKNOWN | High-priority blocker. The available evidence supports a bounded-fan-in/out identical-small-module realization in broad terms, but does not settle input encoding, timing, output delay, or same-hardware grammar restriction. |
| Arnold, Tan & Newborn (1970), *Iteratively Realized Sequential Circuits* | IBM Research primary abstract | UNKNOWN | UNKNOWN | UNKNOWN | PARTIAL | UNKNOWN | UNKNOWN | Primary abstract verifies realization of an arbitrary synchronous flow table as a regular array of identical modules. It does not provide the CCOC compiler constants or timing/restriction semantics. |
| Newborn & Arnold (1972), *Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits* | authoritative bibliographic record/title only | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Title-level evidence is insufficient. Full theorem text is required before any C1–C6 upgrade. |
| Williams (1975), *Uniform Decomposition of Incompletely Specified Sequential Machines* | authoritative bibliographic record; secondary abstract-style descriptions not treated as theorem evidence | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Particularly dangerous because incomplete specification and uniform decomposition meet in one paper, but the decisive compiler properties remain unverified. |
| Jóźwiak & Ślusarczyk (2004), *General decomposition of incompletely specified sequential machines with multi-state behavior realization* | primary ScienceDirect article/abstract material | NOT TARGETED | PARTIAL | UNKNOWN | PARTIAL | PARTIAL | UNKNOWN | Confirms that incomplete-specification plus constrained network decomposition is mature prior art. It does not, in the inspected passages, establish the fixed identical-module compiler contract C1–C6. |

## 3. What the accessible sources establish

### 3.1 Weiner–Hopcroft report exists, but the decisive full text was not obtained

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

### 3.2 Arnold–Tan–Newborn gives genuine primary evidence for uniform modular realization

The IBM Research abstract states that synthesis techniques realize an arbitrary
synchronous flow table as an array of identical modules interconnected in a
regular pattern. This is enough to rule out novelty claims based merely on
“arbitrary synchronous behavior can be realized by repeated identical modules.”

It is not enough to infer constant component state, bounded degree, fixed input
encoding, one-clock simulation, output latency, or restricted-language
compatibility. Those remain UNKNOWN until the full construction is inspected.

### 3.3 The 2004 general decomposition theory blocks broad novelty claims

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

Therefore the current manuscript-safe status remains:

> CCOC gives an explicit extremal bounded-local realization. Whether the existence
> and logarithmic-access properties follow from classical universal sequential-
> machine compilation with comparable input, timing, and restriction semantics is
> still an open historical-comparison question.

No priority or firstness claim should be made while C3/C5/C6 remain unresolved.

## 5. Decisive acquisition order

### Priority 1 — Weiner & Hopcroft (1968)

Acquisition routes already verified:

- Princeton Lewis Science and Engineering Library collection; the finding aid says
  digitization can be requested via `englib@princeton.edu`;
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

### Priority 2 — Newborn & Arnold (1972)

Request the exact paper:

> Monroe M. Newborn and Thomas F. Arnold, *Universal Modules for Bounded Signal
> Fan-Out Synchronous Sequential Circuits*, IEEE Transactions on Computers,
> 21(1):63–79, 1972.

Determine whether it strengthens the 1968 construction on input distribution,
module universality, fan-out constants, or simulation timing. Do not infer these
properties from the title.

### Priority 3 — Williams (1975)

Request:

> George H. Williams, *Uniform Decomposition of Incompletely Specified Sequential
> Machines*, IEEE Transactions on Computers, 24(8):840–843, 1975.

Because the paper explicitly concerns incompletely specified sequential machines,
extract:

- whether one universal compiled architecture is used across completions/input
  restrictions, or the decomposition itself changes with the specification;
- whether incomplete specification changes only the number of components or also
  their wiring/control interface;
- component-state and fan-in/out bounds;
- worst-case component count as unspecified behavior is made specified;
- external-input and timing semantics.

### Priority 4 — Arnold, Tan & Newborn (1970)

Use the full text to resolve the regular-array module state size, interconnectivity,
external input presentation, and iteration/clock semantics.

## 6. Decision rule after full-text extraction

1. **C1–C6 with constant or comparable logarithmic overhead:** stop presenting
   bounded-local existence/logarithmic access as residual mathematical novelty.
   Keep the relay as an explicit sharp construction and shift the manuscript claim
   to the exact causal-interface accounting/ecological synthesis or to a genuinely
   stronger theorem target.
2. **C1–C2 hold but C3, C5, or C6 require machine-size-dependent overhead or
   recompilation:** the explicit CCOC relay retains a quantitative distinction:
   fixed four-symbol control alphabet, one newly legal primitive action,
   radius-one pairwise degree-three dynamics, and `Theta(log m)` access on one
   fixed hardware family.
3. **Williams already combines incomplete specification with one fixed
   input-preserving bounded-local compiler:** narrow the claim further; the
   extremal response-quotient package may remain useful, but not the broad
   restricted-to-open modular phenomenon.

## 7. Source pointers

- IBM Research, Arnold–Tan–Newborn (1970):
  <https://research.ibm.com/publications/iteratively-realized-sequential-circuits>
- Princeton archival finding-aid record containing the Weiner–Hopcroft report:
  <https://findingaids.library.upenn.edu/records/PRIN_MUDD_ENG027>
- CiNii bibliographic record for the Weiner–Hopcroft technical report:
  <https://ci.nii.ac.jp/ncid/BA8670779X>
- DBLP volume record for Newborn–Arnold (1972):
  <https://dblp.org/db/journals/tc/tc21.html>
- DBLP volume record for Williams (1975):
  <https://dblp.org/db/journals/tc/tc24>
- ScienceDirect, Jóźwiak–Ślusarczyk (2004):
  <https://www.sciencedirect.com/science/article/abs/pii/S1383762103001929>

The bibliography entries for Newborn–Arnold (1972) and Williams (1975) are
confirmed, but their full theorem text was not recovered in this pass. Their rows
therefore remain UNKNOWN rather than being completed from secondary descriptions.
