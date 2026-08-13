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

## 6. Claim-control consequence

The historical risk to the bounded-local relay has increased, not decreased.
Report no. 61 has a concrete primary acquisition route, and the predecessor line
suggests that direct source-input wiring may already be part of the classical
model. Therefore CCOC must continue to describe the relay as an **explicit
constrained extremal construction**, not as a historically first bounded-local
compiler witness.

No H1–H4 resource is upgraded in this memo from unread or secondary text.
