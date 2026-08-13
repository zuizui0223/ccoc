# Williams / Le Van–van Houtte 1975 primary acquisition route — 2026-08-13

> **Purpose.** Turn the decisive 1975 C-24(8) resynthesis/timing gate into an
> actionable Japanese primary-reading route. Two high-value historical sources
> occur in the same issue, so one issue-level visit can test both the fixed-hardware
> question and the delayed-module timing line.

## 1. Two targets in one issue

Target issue:

> IEEE Transactions on Computers, volume C-24, number 8, August 1975.

DBLP/independent issue indexes identify both targets:

1. George H. Williams, *Uniform Decomposition of Incompletely Specified
   Sequential Machines*, pp. **840–843**;
2. Tiu Le Van and Noël van Houtte, *Delayed Universal Logic Modules and Sequential
   Machine Synthesis*, pp. **853–855**.

No DOI is required for the acquisition contract. Title, authors, issue, and page
range are sufficient and avoid repeating the DOI-neighbor errors encountered in
the 1972 audit.

## 2. Japanese holding covers 1975

CiNii Books record `AA11952057` for `Computers, IEEE transactions on` records the
Tokyo University of Technology Media Center Library holding as **1968–2017**.
Therefore the August 1975 C-24(8) issue lies inside the declared run.

The same issue is independently known to be preserved in the IEEE Transactions on
Computers archival run (C-24(1–12) for 1975), so a future renderable archive item
remains a second lawful route.

## 3. External on-site use is explicitly allowed

Tokyo University of Technology's current library guidance states that external
users may use the library for **viewing and copying books and journals**.
Electronic resources are restricted to internal users, so this route should be
understood as access to the library's physical journal holding.

Current entry conditions distinguish external-user categories. In particular,
students/staff from a non-partner university are instructed to bring an
introduction letter issued by their home university library. Other external users
follow the identity-document route described by the library. The holding should be
confirmed in OPAC before visiting.

This is an **on-site primary-reading/copying route**, not a verified direct postal
copy service for unaffiliated external requesters.

## 4. Copy cost and copyright scope

Tokyo University of Technology's current copy-machine guidance states:

- copies cost **10 yen per sheet**, independent of size;
- the copy machine may be used only for material held by the library;
- copying is limited by Copyright Act Article 31;
- for a journal article after the relevant publication interval has elapsed, the
  **entire individual article may be copied**;
- one copy per person, for research use, with no redistribution.

Thus both 1975 articles are within the library's declared old-periodical article
copy category, subject to the actual item's condition and library staff rules.

## 5. Williams extraction contract — fixed hardware or resynthesis?

The Williams paper is decisive because secondary historical summaries describe
uniform decomposition of **incompletely specified** sequential machines using
copies of a universal two-state component and a minimization/cover procedure. The
primary body must settle what physically changes when the specification changes.

Extract literally:

1. the formal incomplete-machine model;
2. what entries/behaviors are unspecified;
3. the definition of a valid uniform decomposition;
4. whether each incomplete specification is synthesized into a **new network**;
5. whether component count, component identities, wiring, or input connections
   change when the specification is refined/completed;
6. whether one full deterministic machine can be realized once and later studied
   under restricted admissible inputs without resynthesis;
7. the state cardinality and input/output arity of the universal component;
8. any fan-in/fan-out or interconnection constraints;
9. any component-count bound or minimization objective;
10. whether the paper quantifies how component count changes as incompleteness is
    removed.

### Interpretation

- **Per-specification resynthesis:** strong ancestry for contextual/incomplete
  decomposition, but not CCOC's same-hardware grammar-opening construction.
- **One fixed network with only admissibility changing:** much more dangerous; it
  would directly weaken the remaining fixed-hardware distinction.

Do not infer either reading from the title or secondary abstract.

## 6. Le Van–van Houtte extraction contract — what does “delay” buy?

The second article in the same issue is valuable for H4 and for interpreting the
classical universal-module timing vocabulary.

Extract:

1. formal definition of a delayed universal logic module;
2. whether delay is internal state, a clock step, propagation time, or another
   resource;
3. how source-machine inputs are timed;
4. when the simulated/realized output becomes valid;
5. number of module delays/network stages per source step;
6. dependence of latency on source state count, source input count, or network
   depth;
7. module input/output arity and fanout assumptions;
8. whether realization preserves one designated source output interface or exposes
   additional module outputs.

The later 1978 published comment should be read after this paper if the construction
contains a point that was corrected or challenged; the existence of the comment
alone is not negative evidence.

## 7. Efficient acquisition plan

One visit/request for **C-24(8), August 1975** should prioritize copying both page
ranges:

- Williams: `840–843`;
- Le Van & van Houtte: `853–855`.

That is seven journal pages in total before any cover/issue metadata pages needed
for provenance. Exact physical copy count is determined on site.

If a renderable preserved archive issue becomes available first, use it instead,
but validate the issue, title, authors, and page ranges before promoting evidence.

## 8. Decision consequence for CCOC

This issue can resolve two remaining ambiguities efficiently:

- **resynthesis question:** whether incomplete specification historically meant a
  new modular network or merely a restriction on one fixed realization;
- **timing question:** whether delayed universal-module synthesis already has a
  source-step/network-latency contract comparable to the CCOC relay.

No H1–H4 resource is promoted in this memo. The source bodies must be read first.

## 9. Stop rule

Do not resume broad searches for `uniform decomposition`, `delay`, or `incomplete
machines`. The next information-producing actions are:

1. inspect/copy C-24(8) through the Tokyo University of Technology physical
   holding under its external-user rules; or
2. recover the exact preserved C-24(8) archive item and inspect the two articles.

Until then, Williams remains a **resynthesis gate** and Le Van–van Houtte remains a
**timing acquisition target**, not verified compiler evidence.
