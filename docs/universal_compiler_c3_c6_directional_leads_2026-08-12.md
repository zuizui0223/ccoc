# Universal-compiler C3/C6 directional leads — 2026-08-12

> **Status:** source-acquisition aid only. Nothing in this memo upgrades a
> compiler-contract status in `universal_compilation_source_audit.md` unless the
> relevant statement has been verified in a primary theorem text. In particular,
> C3 and C6 remain `UNKNOWN` for the decisive historical compilers.

## Why separate a directional-lead memo

The broad prior-art question is already settled: context-dependent machine
simplification, incomplete-specification decomposition, and uniform modular
realization are historical substrate. The remaining CCOC novelty risk is narrower:

- **C3:** where does a classical universal decomposition pay for source-machine
  input complexity? Does it preserve a fixed external control alphabet, or move
  machine-size/input-size complexity into module inputs, input distribution, or an
  encoding network?
- **C6:** when a source machine is incompletely specified or input-restricted, is
  the *same already-compiled network* evaluated under a restricted language, or is
  a new decomposition synthesized from the restricted specification?

Search results can point toward one interpretation without proving it. This memo
records those directions so the primary-source extraction is targeted rather than
repeating broad literature searches.

## 1. C3 lead: Huang, Kain & Kinney (1972)

Target:

> C. C. Huang, Richard Y. Kain, and Larry L. Kinney, *Output Sufficient Modules
> for Uniform Decomposition of Synchronous Sequential Circuits*, 13th Annual
> Symposium on Switching and Automata Theory (SWAT), 1972, pp. 192–199,
> DOI `10.1109/SWAT.1972.17`.

### Bibliographic status

DBLP independently indexes the paper and its DOI route. The paper is directly
adjacent to the Newborn–Arnold universal-module line.

### Secondary directional lead — **not theorem evidence**

An abstract-style secondary record reports that the paper's primary concern is the
number of inputs required by a universal/output-sufficient module and states that
this required input count grows exponentially with the number of inputs of the
sequential machines to be realized.

If the primary paper confirms that statement with the relevant notion of “input,”
it would be important for CCOC because it would show that classical modular
universality may carry a nonconstant **input-interface resource cost** even while
component state/fanout constraints are bounded. That would weaken any inference

> bounded local modules ⇒ fixed-small external/control interface.

It would **not automatically prove** that CCOC's four-symbol global control
alphabet is historically new, because the counted module inputs may represent
intermodule signals rather than external controls, and a separate fixed-alphabet
encoder may still exist.

### Primary extraction questions

When the IEEE/SWAT paper is obtained, extract literally:

1. the formal definitions of `universal module` and `output sufficient module`;
2. the lower/upper bound on module input count and exactly which source-machine
   parameter controls the bound;
3. whether counted inputs are external source controls, intermodule signals, or
   both;
4. whether arbitrary source input symbols are presented directly or encoded;
5. whether a fixed-size external alphabet can drive the construction with bounded
   time overhead;
6. the paper's explicit relationship to Newborn–Arnold (1972), including which
   assumptions are inherited and which are strengthened.

### C3 decision impact

- If the primary result requires module/input-interface size growing with source
  input complexity and no fixed-alphabet bounded-overhead encoding is supplied,
  this supports a quantitative distinction for the explicit CCOC relay.
- If the primary result also supplies a fixed external alphabet with constant or
  logarithmic encoding overhead, the CCOC distinction narrows substantially.
- Until the primary text is read: **C3 remains `UNKNOWN`.**

## 2. C6 lead: Williams (1975)

Target:

> George H. Williams, *Uniform Decomposition of Incompletely Specified Sequential
> Machines*, IEEE Transactions on Computers, C-24(8):840–843, 1975.

DBLP and IEEE-volume indexes verify the bibliographic identity and page range.

### Secondary directional lead — **not theorem evidence**

A secondary abstract-style copy describes the method in terms of realizing a
Moore machine by copies of a universal two-state component, representing each
component's processed information by a partial mapping, and exploiting incomplete
specification to **reduce the number of component copies through a minimal-cover
search over partial mappings**.

Taken only as a search lead, this wording points more naturally toward
**specification-dependent synthesis/optimization** than toward CCOC's C6 contract,
which requires one already-compiled network whose admissible external language can
simply be restricted or opened without recompiling the hardware.

That directional interpretation is not a verdict. The abstract-style copy is not
being treated as the original IEEE theorem text, and it does not establish whether
one universal wiring can be retained while only a subset of inputs/transitions is
made admissible.

### Primary extraction questions

When the four-page IEEE paper is obtained, determine literally:

1. what is held fixed when incomplete specification changes: universal component
   type only, or component count/wiring/control interface as well;
2. whether the minimal-cover search produces a new decomposition for a particular
   incomplete machine;
3. whether a decomposition synthesized for a less-restricted completion also
   realizes a restricted version merely by forbidding inputs/transitions;
4. conversely, whether a decomposition synthesized from the restricted machine can
   be opened without changing hardware;
5. whether the component count can grow asymptotically when unspecified behavior
   is filled in;
6. external-input presentation and timing semantics.

### C6 decision impact

- If each incomplete specification is re-synthesized into a different component
  set or wiring, Williams is strong prior art for **context-dependent uniform
  decomposition** but does not by itself satisfy C6.
- If one fixed compiled network supports both restricted and opened admissible
  languages without structural change, Williams is much more dangerous and may
  subsume the structural restricted→open aspect of CCOC.
- Until the primary text is read: **C6 remains `UNKNOWN`.**

## 3. Why these two leads change the acquisition priority

The remaining historical comparison should now be read as a resource-accounting
problem rather than a keyword-priority search.

| Source | Decisive resource/question | Current status |
|---|---|---|
| Weiner–Hopcroft (1968) | C3 input distribution, C5 clock/latency, C6 same-hardware language restriction | primary full text needed |
| Newborn–Arnold (1972) | universal-module input/fanout contract and timing | primary full text needed |
| Huang–Kain–Kinney (1972) | whether universal/output-sufficient module input count is intrinsically nonconstant and what those inputs mean | primary full text needed; strong C3 lead |
| Williams (1975) | specification-dependent resynthesis versus same-hardware restricted/open semantics | primary full text needed; directional C6 lead |
| Arnold–Tan–Newborn (1970) | regular-array input presentation and iteration/clock semantics | full text needed |

This is a better discriminator than asking whether an old paper uses the words
“uniform,” “universal,” “bounded,” or “incompletely specified.”

## 4. Current claim-control rule

No manuscript wording should say that historical decomposition **fails** C3 or C6.
The strongest source-grounded statement remains:

> Classical work establishes contextual/incomplete-specification simplification
> and uniform modular realization in broad terms, but the present audit has not
> yet verified a historical compiler that simultaneously preserves the CCOC
> external-control semantics, comparable access latency, and same-hardware
> restricted/open grammar contract.

The directional leads above merely make the next primary-text extraction more
focused.

## 5. Source pointers

Bibliographic/primary-routing sources:

- DBLP, Huang–Kain–Kinney SWAT 1972 record:
  <https://dblp.org/rec/conf/focs/HuangKK72>
- DOI route for Huang–Kain–Kinney:
  <https://doi.org/10.1109/SWAT.1972.17>
- DBLP, Williams 1975 record:
  <https://dblp.org/rec/journals/tc/Williams75>
- DBLP, Newborn–Arnold 1972 record:
  <https://dblp.org/rec/journals/tc/NewbornA72>

Secondary search leads, retained only to target primary-source acquisition:

- Huang–Kain–Kinney abstract-style summary:
  <https://eurekamag.com/research/103/689/103689625.php>
- Williams abstract-style search copy surfaced through Academia; do not quote it
  as the original IEEE source.
