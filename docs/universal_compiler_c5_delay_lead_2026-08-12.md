# Universal-compiler C5 delay lead — 2026-08-12

> **Status:** source-acquisition aid only. This memo does **not** upgrade C5 in
> `universal_compilation_source_audit.md`. The word “delayed” in a historical title
> is not enough to identify CCOC's simulation-time overhead. Primary construction
> details are required.

## 1. Why C5 needs its own historical check

CCOC's compiler clause C5 asks a specific operational question:

> If one source-machine control word has length `L`, how many synchronous local
> network rounds are required before the compiled focal output faithfully recovers
> the source response?

This is not the same as asking whether a logic module contains a delay element or
whether propagation delay is useful inside a circuit. A historical paper can be
about “delayed universal logic modules” while still leaving CCOC's source-step to
network-step slowdown unresolved.

The acquisition task must therefore separate:

1. **module/circuit delay as a primitive resource**;
2. **depth/propagation delay inside one compiled source step**;
3. **multi-round simulation slowdown** between source and compiled machines;
4. **output decoding/readout delay** after the relevant source response;
5. **network diameter/depth**, which may constrain but does not by itself equal
   semantic simulation latency.

## 2. Primary C5 target: Le Van & van Houtte (1975)

Target:

> Tiu Le Van and Noël van Houtte, *Delayed Universal Logic Modules and Sequential
> Machine Synthesis*, IEEE Transactions on Computers, C-24(8):853–855, August
> 1975.

### Verified bibliographic facts

- DBLP indexes the article under key `journals/tc/VanH75` and provides DOI,
  IEEE-Computer-Society, and Unpaywall routes.
- Independent IEEE Transactions on Computers tables of contents confirm the
  authors, title, August 1975 issue, and pages 853–855.
- The paper appears in the same issue immediately after George H. Williams's
  *Uniform Decomposition of Incompletely Specified Sequential Machines*
  (pp. 840–843).
- A readable primary full text was not recovered through the current web path in
  this pass. The exact DOI was not safely resolved from the accessible metadata,
  so it is deliberately not guessed here.

### Current evidence status

The title alone establishes only that delayed universal logic modules are the
paper's declared topic. It does **not** establish:

- one source-machine step per module-network step;
- constant, logarithmic, or any quantified source-to-network slowdown;
- output decoding latency;
- network depth or diameter;
- whether “delay” refers to physical/logic delay, stored state, or semantic
  simulation rounds.

Therefore **C5 remains `UNKNOWN`.**

### Primary extraction questions

When the original three-page IEEE correspondence is obtained, extract literally:

1. the formal definition of a delayed universal logic module;
2. whether delay is an internal module primitive, interconnection delay, or a
   sequence of synchronous machine clocks;
3. how a source sequential-machine transition is represented by the constructed
   network;
4. the number of module/network clock steps per source transition, if stated;
5. the longest input-to-output or state-to-output delay relevant to faithful
   response recovery;
6. construction depth/diameter and whether it scales with source state count or
   source input count;
7. any area/module-count versus delay tradeoff;
8. whether external controls are held fixed during a multi-step compiled
   transition or re-encoded across several network clocks.

Only items 3–5 can directly settle the semantic C5 contract.

## 3. Correction/critique target: Sureshchander (1978)

Target:

> Sureshchander, *Comments on “Delayed Universal Logic Modules and Sequential
> Machine Synthesis”*, IEEE Transactions on Computers, C-27(2):191, February
> 1978.

### Verified bibliographic facts

DBLP and the IEEE Transactions on Computers volume-27 table of contents both
confirm the one-page comment and its target paper.

### Why it matters

A formal comment published three years later may identify a flaw, missing
condition, bound, or interpretation in the 1975 construction. But without the
one-page primary text we cannot infer what the comment concerns.

### Extraction questions

Obtain the original page and record:

- which proposition/construction in Le Van–van Houtte is being corrected or
  challenged;
- whether the issue concerns delay, universality, state-machine synthesis,
  connectivity, or something else;
- any corrected quantitative delay/resource bound;
- whether the original authors replied elsewhere.

Until that page is read, the existence of a comment is only a reason for extra
caution, not negative evidence about the 1975 result.

## 4. Comparison targets after the 1975/1978 pair

Two later IEEE Transactions on Computers papers provide useful context for how
universal-logic-module sequential implementations were evaluated:

1. **A. E. A. Almaini (1978)**,
   *Sequential Machine Implementations Using Universal Logic Modules*,
   C-27(10):951–960.
2. **X. Chen & Stanley L. Hurst (1982)**,
   *A Comparison of Universal-Logic-Module Realizations and Their Application in
   the Synthesis of Combinatorial and Sequential Logic Networks*,
   C-31(2):140–147.

At present only authoritative bibliographic/index evidence has been inspected for
these papers. They are comparison targets, not theorem evidence for C5.

If primary texts are acquired, extract whether their comparison metrics include:

- number of module levels / critical path;
- number of clocks per sequential transition;
- state/output latency;
- module count versus depth tradeoffs;
- input/interface count;
- whether sequential state is stored inside modules or propagated through delayed
  interconnections.

This can help translate the older “delay” vocabulary into the semantic resource
needed by the CCOC compiler contract.

## 5. C5 decision rule

### Case C5-A — constant source-step simulation

If the classical construction proves that each source-machine input/transition is
faithfully simulated with a constant number of local synchronous rounds and
constant output-decoding delay, then CCOC cannot use `Theta(log m)` access alone as
an historical novelty argument; the explicit relay may simply instantiate a
classical compiler with weaker or comparable timing.

### Case C5-B — size-dependent semantic slowdown

If faithful simulation requires delay growing materially with compiled-machine
size, source state count, source input count, or network depth, then the explicit
CCOC relay may retain a quantitative realization distinction when combined with
its fixed external alphabet, degree-three radius-one updates, and logarithmic
addressed access.

### Case C5-C — only physical/module delay is analyzed

If the classical “delayed module” literature discusses local circuit delay without
providing a source-transition-to-network-round simulation contract, it does not by
itself settle C5 either way.

Until the primary 1975/1978 texts are read: **C5 remains `UNKNOWN`.**

## 6. Current combined novelty-gate picture

The remaining universal-compilation comparison is now naturally split into three
resource questions:

| Clause | Historical question | Highest-priority sources |
|---|---|---|
| **C3** | Where is source-input/control complexity paid? | Newborn–Arnold (1972); Huang–Kain–Kinney (1972) |
| **C5** | What is the semantic source-step → local-network-round/output delay? | Le Van–van Houtte (1975); Sureshchander (1978); then Almaini (1978), Chen–Hurst (1982) |
| **C6** | Same compiled hardware under restricted/open languages, or specification-dependent re-synthesis? | Williams (1975); Weiner–Hopcroft (1968) |

Weiner–Hopcroft (1968) remains relevant to all three because its universal
bounded-fan-in/out compiler is the most direct route by which the explicit CCOC
local witness could become generic.

## 7. Source pointers

Authoritative bibliographic/index routes used in this pass:

- DBLP volume 24 / `VanH75`:
  <https://dblp.org/rec/journals/tc/VanH75>
- IEEE Transactions on Computers volume-24 table of contents:
  <https://ftp.math.utah.edu/pub/tex/bib/toc/ieeetranscomput1970.html>
- DBLP volume 27 / Sureshchander comment:
  <https://dblp.org/db/journals/tc/tc27.html>
- DBLP Almaini record:
  <https://dblp.org/rec/journals/tc/Almaini78>
- DBLP Chen–Hurst record:
  <https://dblp.org/rec/journals/tc/ChenH82>

These routes establish bibliographic identity and acquisition targets. They do not
replace the primary theorem/construction text.