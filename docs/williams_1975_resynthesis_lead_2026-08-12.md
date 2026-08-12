# Williams (1975) incomplete-machine decomposition: resynthesis lead

> **Status:** secondary-source acquisition/claim-control memo, 2026-08-12.
> This memo does **not** upgrade any H1–H4 compiler property and does not treat
> secondary text as a substitute for the primary IEEE correspondence.

## 1. Source identity

Authoritative bibliographic records identify:

> George H. Williams, *Uniform Decomposition of Incompletely Specified Sequential
> Machines*, IEEE Transactions on Computers, C-24(8), 840–843, August 1975.

DBLP key: `journals/tc/Williams75`.

The paper appears in the same issue as Le Van & van Houtte,
*Delayed Universal Logic Modules and Sequential Machine Synthesis*, pp. 853–855.

The current search index exposes DBLP links for a DOI/electronic edition, Computer
Society edition, and an unpaywalled route, but did not expose a stable DOI value in
retrievable text during this pass. Do not guess a DOI from neighboring IEEE papers.

## 2. Secondary resynthesis lead

A currently indexed Academia profile page is **metadata-misattributed**: the page
is headed as Frans Handoko / *A Discussion on Two Algorithms for Determining
Maximum Compatibles*, but the attached abstract-style text describes uniform
decomposition of incompletely specified sequential machines.

That text says, in substance, that:

- a Moore sequential machine is realized by interconnected copies of a universal
  two-state component machine;
- each component processes information represented by a partial mapping;
- incomplete specification can reduce the number of component copies;
- the reduction is obtained by a uniform-cost search for a minimal cover over the
  partial mappings.

Because the hosting metadata is visibly cross-wired, this is only a **directional
lead**. It must not be cited as Williams's primary abstract or theorem statement.

## 3. Why this matters for the corrected CCOC compiler gate

The corrected compiler reduction distinguishes two questions:

1. Does one full-language compiler produce a fixed network satisfying H1–H4?
2. Does an incomplete-specification method instead optimize/synthesize a network
   specifically for the partial specification supplied to it?

The secondary Williams wording is much more naturally consistent with (2): the
number of component copies is reduced by solving a minimal-cover problem on the
partial mappings induced by the incomplete specification.

If the primary paper confirms this reading, Williams is strong prior art for
**specification-dependent uniform decomposition**, but it does not by itself give
CCOC's dangerous full-machine reduction in which one hardware network is compiled
once and closed/open grammars are later imposed by restricting the admissible
control language.

This is an **inference from secondary wording**, not a verified historical fact.
The primary 840–843 pages control the final classification.

## 4. Decisive primary-text extraction

When the August 1975 issue or article becomes readable, extract only:

- what object is supplied to the synthesis procedure: a full machine plus a
  restriction, or an incompletely specified machine directly;
- whether the universal two-state component itself is fixed;
- whether the **number of copies**, wiring, or both are recomputed after the
  incomplete specification changes;
- the definition of the partial mappings and the minimal-cover objective;
- whether the uniform-cost search is part of network construction/optimization;
- whether two different incomplete specifications of the same completion would
  generally lead to different decomposed networks;
- any timing/input/output semantics relevant to H2–H4.

If copy count or wiring is recomputed from each partial specification, classify the
paper under **resynthesis ancestry**, not as evidence that one fixed full-language
compiled network automatically supports nested closed/open grammars.

## 5. Relation to broader decomposition prior art

The primary 2004 Jóźwiak–Ślusarczyk article independently confirms that general
decomposition of incompletely specified sequential machines is mature synthesis
prior art and explicitly treats the result as a network constructed to realize the
given machine while satisfying structural/implementation constraints.

Therefore even if Williams turns out to be specification-dependent resynthesis,
CCOC cannot claim novelty for "incomplete/context-restricted machine + constrained
decomposition". The only point protected by this distinction is the narrower
**same full hardware, later grammar restriction** compiler question.

## 6. Metadata caution from the same historical cluster

The 1972 SWAT paper *Output Sufficient Modules for Uniform Decomposition of
Synchronous Sequential Circuits* is authoritatively indexed by DBLP as C. C. Huang,
Richard Y. **Kain**, and Larry L. Kinney. A secondary Eureka record renders the
second author as "Cain" while attaching the correct DOI `10.1109/SWAT.1972.17`.

Together with the already recorded Newborn–Arnold/Kim–Newborn DOI cross-link, this
is a reminder that automated historical-source acquisition must validate title,
authors, venue, pages, and DOI jointly before promoting any text to primary
evidence.

## 7. Stop rule

Do not build a new theorem or a new compiler clause from this memo.

Next action is only one of:

1. read the primary Williams pages and classify resynthesis versus fixed-hardware
   restriction; or
2. leave the classification `SECONDARY LEAD / PRIMARY UNKNOWN`.

No amount of repeated secondary search should be converted into a priority claim.