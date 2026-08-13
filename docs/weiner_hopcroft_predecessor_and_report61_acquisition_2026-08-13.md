# Weiner–Hopcroft predecessor and report-61 acquisition update — 2026-08-13

> **Purpose.** Refine issue #122's H1–H4 acquisition plan without promoting any
> compiler resource from unread primary text. This memo distinguishes a verified
> primary-document location, an authoritative bibliographic record, and a
> secondary/indexed construction lead.

## 1. Report no. 61 now has a concrete physical acquisition route

Target:

> Peter Weiner and John E. Hopcroft, *Bounded Fan-in, Bounded Fan-out Uniform
> Decompositions of Synchronous Sequential Machines*, Digital Systems Laboratory
> Technical Report no. 61, Princeton University, April 1968.

CiNii Books records the report as `7 p., [3] leaves of plates` and identifies a
physical holding at the **University of Tokyo General Library**:

- call number: `U600:769`;
- item/record: `0004766739`;
- NCID: `BA8670779X`.

The Princeton Computer Sciences Laboratory technical-report finding aid
independently lists the same April-1968 report as a physical archival item.

### Evidence consequence

This resolves **where the primary report can lawfully be obtained**. It does not
resolve H1–H4 by itself. The report body has not been read in the current audit.

The next legitimate acquisition action is therefore a library/archive scan or a
newly renderable digital copy, not another generic mirror search.

### Actionable remote-copy route

The University of Tokyo General Library's current external-user guidance states
that remote photocopy requests from outside users must be placed **through a
library** rather than directly by the individual requester. Its interlibrary
service guidance gives a NACSIS-ILL route for academic libraries and also permits
photocopy requests through public-library channels.

For a complete-copy request, use the exact metadata above and request the full
item, including the three leaves of plates, subject to copyright and library
policy. This means report no. 61 is no longer merely `located`: it is an
**actionable ILL/photocopy acquisition target**.

## 2. The 1967 predecessor is formally identified

The immediate predecessor is:

> Peter Weiner and John E. Hopcroft, *Modular Decomposition of Synchronous
> Sequential Machines*, 8th Annual Symposium on Switching and Automata Theory
> (SWAT/FOCS 1967), pp. 233–239.

DBLP identifies the electronic edition by DOI:

`10.1109/FOCS.1967.19`

The DOI, IEEE Computer Society, and Unpaywall routes all failed to return readable
primary text in the present web environment. This failure is an acquisition
limitation, not evidence that the source is unavailable elsewhere.

## 3. Secondary/indexed text makes H2 more dangerous, but does not verify it

An indexed secondary publication page for the 1967 paper exposes the beginning of
its description. It says that the paper treats interconnection **literally** and
that a component input terminal must be directly connected to one of:

1. a logical constant;
2. an output terminal of another component machine; or
3. an external input terminal.

If this wording is confirmed in the primary construction, it would weaken a
possible H2 escape based on an expensive hidden input-encoding layer: the source
inputs appear to enter the modular network as actual external terminals rather
than through an `m`-dependent symbolic decoder.

However, this is currently **SECONDARY/INDEXED LEAD ONLY**. It must not be used to
promote H2. The primary 1967 paper or report no. 61 must be read before recording a
compiler theorem property.

## 4. Updated H1–H4 interpretation

### H1 — bounded locality

The 1968 report title and long-standing abstract-style descriptions make this the
strongest historical H1 lead: identical two-state modules with fan-in/fan-out
bounded independently of source state count. The primary report body is still
needed for the exact constants and graph/interconnection contract.

### H2 — fixed context-independent controls

Status remains **UNKNOWN / DANGEROUS LEAD** for the Weiner–Hopcroft compiler.

The 1967 indexed description suggests literal external-input wiring. The CCOC
source control alphabet is already fixed as `m` grows, so an input mechanism whose
cost depends only on the fixed source input dimension would not rescue the relay's
realization novelty.

Primary extraction must determine:

- how source input terminals are distributed to module inputs;
- whether source-state count affects that distribution cost;
- whether the same distribution is retained when only the admissible source
  sublanguage changes.

### H3 — two-way response-trace faithfulness

Still **UNKNOWN** for report no. 61. `realization` must be read formally. The
compiler must not expose additional designated observables that split source states
which are response-equivalent under a closed grammar.

### H4 — source-step / network-round / output latency

Still **UNKNOWN** for report no. 61. The primary construction must state its
clocking/settling convention and when the realized machine output is valid after a
source input change.

## 5. Exact extraction checklist for report no. 61

When the seven-page report and plates are obtained, extract literally:

1. module state cardinality and input/output arity;
2. fan-in and fan-out constants;
3. external input terminal wiring and any replication/distribution network;
4. definition of realization/equivalence/isomorphism;
5. which network outputs are designated as source outputs;
6. source clock, module clock, delay, or settling semantics;
7. source-step to valid-output latency;
8. module-count bound;
9. network depth/diameter bound if stated;
10. whether any of those resources depend on source state count versus source
    input count.

These ten fields are sufficient to map the construction onto the corrected CCOC
H1–H4 contract.

## 6. Related 1968 Ullman–Weiner bridge source

A second dangerous source in the same historical line is:

> Jeffrey D. Ullman and Peter Weiner, *Universal Two State Machines:
> Characterization Theorems and Decomposition Schemes*, SWAT 1968, pp. 413–426.

DBLP verifies the bibliographic identity. A secondary indexed abstract says that
its first part characterizes when a two-state machine is **universal**, including
necessary-and-sufficient conditions and a testing algorithm, while its second part
turns to economical realization of sequential machines using such modules.

The primary paper body has not been recovered in the current environment, so no
H1–H4 clause is promoted from that abstract. Nevertheless, the source is a high-
priority bridge between the 1967/1968 Weiner–Hopcroft decomposition line and the
1969 Ullman–Weiner fixed-module/delay synthesis theorem.

## 7. Drilman–Weiner 1972 joins nondeterminism and fixed-module synthesis

A further source materially increases the historical risk:

> J. Drilman and Peter Weiner, *Modular Networks and Nondeterministic Sequential
> Machines*, IEEE Transactions on Computers 21(10):1124–1129, October 1972.

DBLP verifies the journal identity. A complete IEEE bibliography gives IEEE Xplore
article number `1672054`. A secondary indexed abstract states that the paper
considers synthesis of sequential machines by interconnections of copies of a
**fixed module**, defines a family of modules `M_{r,p}`, and then introduces an
`r`-bounded **nondeterministic sequential machine** class.

This is important because it joins two lines that must not be treated as if they
were historically separate:

- incompletely specified / nondeterministic sequential behavior; and
- uniform synthesis by copies of a fixed module.

It predates Williams (1975), which had previously been treated as the most obvious
intersection of incomplete specification and uniform two-state decomposition.

### Evidence discipline

The indexed abstract is not enough to determine whether Drilman–Weiner supplies a
CCOC-like fixed-hardware restriction theorem, whether its nondeterminism is a
specification device or an implementation device, or whether its module family
satisfies H1–H4 with the needed uniform constants. The primary IEEE article must be
read before promoting any compiler resource.

### Primary extraction questions

If the 1972 article becomes readable, extract:

1. the formal definition of `r`-bounded NSM;
2. what relation between an NSM and deterministic machines is being represented;
3. whether one modular network represents all deterministic refinements or a new
   network is synthesized for each machine;
4. module state count, input/output arity, and fan-out assumptions;
5. external input presentation;
6. designated output semantics and simulation/realization equivalence;
7. clock/delay semantics and latency;
8. module-count/depth dependence on the size of the realized machine.

A positive fixed-hardware answer would be much more dangerous to the residual CCOC
realization claim than generic incomplete-machine minimization alone.

## 8. Claim-control consequence

The historical risk to the bounded-local relay has increased, not decreased.
Report no. 61 has a concrete primary acquisition route, the predecessor line
suggests that direct source-input wiring may already be part of the classical
model, the 1968 Ullman–Weiner source explicitly studies universal two-state
modules, and the 1972 Drilman–Weiner source joins nondeterministic machines with
fixed-module synthesis.

Therefore CCOC must continue to describe the relay as an **explicit constrained
extremal construction**, not as a historically first bounded-local compiler
witness.

No H1–H4 resource is upgraded in this memo from unread or secondary text.
