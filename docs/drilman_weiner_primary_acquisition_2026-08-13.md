# Drilman–Weiner 1972 primary acquisition route — 2026-08-13

> **Purpose.** Turn the newly identified intersection between fixed-module synthesis
> and nondeterministic sequential machines into a concrete primary-text acquisition
> gate. No H1–H4 compiler resource is promoted until the article body is read.

## 1. Exact article identity

Target:

> J. Drilman and Peter Weiner, *Modular Networks and Nondeterministic Sequential
> Machines*, IEEE Transactions on Computers, volume C-21, number 10, October 1972,
> pp. 1124–1129.

DBLP independently verifies the title, authors, journal, volume/issue, year, and
page range (`journals/tc/DrilmanW72`). A complete IEEE Transactions on Computers
bibliography records IEEE Xplore article number:

`1672054`

No DOI is entered in this acquisition memo because the current search has not
produced a sufficiently authoritative DOI mapping. Do not infer one from nearby
IEEE records.

## 2. The same Osaka holding covers this article

CiNii Books record `AA00667773` records Osaka Prefectural Central Library holding
the relevant IEEE Transactions on Computers run for **1969–1973**. The October
1972 C-21(10) issue therefore falls within the same explicitly recorded run used
for the Newborn–Arnold January article.

This makes Drilman–Weiner a second **actionable direct-copy target** at the same
holding library.

## 3. Direct Web-copy route and cost contract

Osaka Prefectural Library's current Web copy service is available remotely and the
library states that anyone may use it, including a one-time/no-registration path.
Copies are mailed rather than delivered electronically.

For ordinary library books/journals/newspapers, current postal-copy charges are:

- black-and-white: **30 yen per copied sheet**;
- color: **100 yen per copied sheet**;
- plus actual postage;
- plus a **100-yen dispatch/handling charge for up to 50 sheets**, with another
  100 yen for each additional 50-sheet block.

The library determines the actual copied-sheet count and total charge, then sends
that amount by email. Payment is prepaid; online banking is accepted. Copying and
postal dispatch begin after payment is confirmed.

Because this is a 1972 periodical back issue, the library's declared copyright
scope permits an individual article to be copied in full for research use, subject
to final copyright/source-condition review.

The article is only six journal pages (`1124–1129`), but do not precompute an
exact total price from six pages because copied-sheet count and postage are set by
the library. The service also warns that multiple applications may be dispatched
separately, so do not assume one combined postage charge with the Newborn–Arnold
request.

## 4. Exact request metadata

Use:

- journal: `IEEE Transactions on Computers`;
- volume/issue: `C-21(10)` / volume 21, number 10;
- date: October 1972;
- authors: J. Drilman; Peter Weiner;
- article: `Modular Networks and Nondeterministic Sequential Machines`;
- pages: `1124–1129`;
- IEEE Xplore article number: `1672054`;
- CiNii holding record: `AA00667773`;
- holding: 大阪府立中央図書館, 1969–1973.

Title, authors, issue, and pages are the primary admission keys. Do not add an
unverified DOI to the library request.

## 5. Why this source is unusually important

Secondary indexed abstract text says the paper begins from synthesis by
interconnections of copies of a **fixed module**, defines a module family
`M_{r,p}`, and introduces an `r`-bounded **nondeterministic sequential machine**
(NSM) class. It also says `M_{r,p}` can synthesize machines with `2^p` input
symbols.

That combination is historically dangerous for CCOC because it may connect two
lines that cannot safely be treated as separate:

1. uniform/fixed-module sequential-machine realization; and
2. incomplete/nondeterministic behavior classes.

The secondary abstract is an acquisition lead only. The primary paper must decide
whether nondeterminism is a specification device, an implementation device, or a
family-of-refinements device, and whether the same modular hardware represents
multiple deterministic refinements.

## 6. Primary extraction contract

### A. Nondeterministic specification semantics

Extract literally:

1. the definition of an `r`-bounded NSM;
2. the role of the initial state and allowed successor sets;
3. the relation between an NSM and deterministic sequential machines;
4. whether deterministic refinements/realizations are chosen inside one fixed NSM
   specification;
5. whether changing the permitted behavior causes network resynthesis.

### B. Fixed-module realization

Extract:

1. formal definition of `M_{r,p}`;
2. module state cardinality;
3. module input/output arity;
4. fan-in/fan-out/interconnection restrictions;
5. number of module copies needed versus source state count and input count;
6. whether one hardware network is fixed for a full behavior class.

### C. H2 controls

Extract:

1. how the `2^p` source input symbols are presented/distributed;
2. whether distribution cost depends on source state count;
3. whether restricting admissible input/behavior leaves the same external control
   interface and wiring in place.

CCOC keeps source input dimension fixed as `m` grows, so a resource that depends
only on fixed `p` is constant with respect to the CCOC scaling variable.

### D. H3 response faithfulness

Extract:

1. formal realization/equivalence relation;
2. designated network outputs;
3. whether module-internal outputs are hidden;
4. whether source and compiled response equality agree in both directions on the
   embedded source states.

### E. H4 timing

Extract:

1. synchronous clock/delay convention;
2. source input timing;
3. output-validity/settling time;
4. dependence on source state count;
5. network depth/diameter if stated.

## 7. Decision consequences

### Fixed network represents multiple deterministic refinements + H1–H4

This would be a serious direct threat to the residual CCOC realization novelty,
because incomplete/nondeterministic specification and bounded modular compilation
would already coexist in one classical construction.

### Network is resynthesized for each deterministic refinement

Then the paper remains strong ancestry for nondeterministic/incomplete modular
synthesis but does not directly reproduce CCOC's same-hardware restricted/open
future-grammar comparison.

### H1/H2 are strong but H3/H4 are weak

Record the exact partial compiler resources. Do not infer two-way quotient
preservation or logarithmic access from synthesis alone.

## 8. Stop rule

Do not repeat generic title/DOI mirror searches. The next information-producing
step is one of:

1. submit the Osaka Web copy request for pp. 1124–1129;
2. retrieve the preserved C-21(10) issue through Internet Archive/Portico/another
   lawful library route;
3. obtain a verified primary scan.

Until the body is read, the paper remains a **high-risk acquisition lead**, not an
H1–H4 theorem source.
