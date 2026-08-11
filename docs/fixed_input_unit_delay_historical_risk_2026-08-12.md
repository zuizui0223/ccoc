# Fixed-input / unit-delay historical risk — 2026-08-12

> **Status:** novelty-control memo. This file records a newly sharpened historical
> risk to the residual CCOC realization claim. It deliberately separates
> contemporaneous abstracts/digests from original-paper verification. No C1–C6
> clause is upgraded beyond what the cited evidence supports.

## 1. Why this changes the novelty gate

The post-reopening CCOC relay was strengthened to use a fixed global primitive
control alphabet

\[
\{0,1,\mathsf{fire},\mathsf{tick}\}
\]

while the number of dormant memories `m` grows. One possible residual novelty
argument was therefore that old universal-module constructions might require an
input/control interface that grows with the compiled machine.

Two older lines make that argument unsafe unless stated much more narrowly:

1. **Hsieh–Tan–Newborn (1968)** explicitly studies uniform modular realization
   after fixing the source-machine input dimension, and a contemporaneous IEEE
   literature digest reports a unit-delay result/limitation in that setting.
2. **Ullman–Weiner (1969)** studies binary-input sequential machines realized by
   networks of one fixed module with delay; an abstract-style record gives a
   quantitative fixed-module realization bound.

Because the CCOC primitive control alphabet is fixed as `m` grows, it belongs to a
**fixed finite input-interface regime**. Thus a historical theorem whose module is
allowed to depend on a fixed input dimension can still threaten the CCOC
asymptotic novelty: dependence on that fixed dimension is a constant with respect
to `m`.

The correct residual question is no longer simply

> did old work have a fixed module and bounded delay?

It is closer to

> did old work simultaneously retain bounded fanout/local degree, a fixed-small
> external control encoding, faithful low-latency simulation, and one fixed
> realized hardware network on which restricted and opened input grammars can be
> compared?

That last same-hardware grammar condition is C6.

## 2. Hsieh, Tan & Newborn (1968)

Target:

> Edward P. Hsieh, Chung-Jen Tan, and Monroe M. Newborn,
> *Uniform modular realization of sequential machines*,
> ACM National Conference 1968, pp. 613–621,
> DOI `10.1145/800186.810625`.

### Evidence obtained

DBLP verifies the paper identity, pages, and DOI route.

A contemporaneous IEEE *Abstracts of Current Computer Literature* digest, already
identified in the historical watchlist, summarizes the paper's logical-
completeness question. The digest reports, in substance:

- no finite set of modules is logically complete for realization of **all**
  synchronous sequential machines with **unit delay** when input dimension is
  unrestricted;
- for each fixed positive input count `n`, however, a finite uniform modular basis
  can realize every `n`-input synchronous machine; the summary describes the
  result using copies of one module.

This is substantially stronger historical evidence than a title-only watchlist,
but it is still a **contemporaneous secondary digest**, not the original ACM
proof. Exact module state size, input convention, interconnection/fanout bounds,
and the formal meaning of unit delay must still be extracted from the paper.

### Relevance to CCOC

The first bullet does **not** rescue CCOC by itself. CCOC does not let its global
primitive alphabet grow with `m`; it has four symbols. A four-symbol alphabet can
in principle be encoded by a fixed number of binary control lines. Therefore the
historically positive **fixed-input-dimension** regime is the relevant one, not
only the impossibility result across unbounded input dimensions.

This is an inference from the source comparison, not a historical theorem claim.
It means only that CCOC should not argue novelty from “our input alphabet is
constant” until the original Hsieh construction is read.

### Primary extraction questions

1. What exactly is an `n`-input synchronous machine: `n` binary input terminals,
   `n` input symbols, or another convention?
2. Does the universal module type depend on `n`? If so, which resources grow with
   `n`?
3. What does **unit delay** mean formally: one source-machine transition per
   network clock, one delay element per path, or another circuit notion?
4. Is the realization behaviorally isomorphic at every source clock?
5. What are module fan-in and fan-out, and do they depend on source state count?
6. Are external input terminals connected directly to modules or routed/encoded
   through an auxiliary network?
7. Can the same realized network be evaluated under a restricted subset/language
   of source inputs without resynthesis?

Until these are answered from the original paper, C3/C5/C6 remain unresolved.

## 3. Ullman & Weiner (1969)

Target:

> J. D. Ullman and Peter Weiner,
> *Uniform Synthesis of Sequential Circuits*,
> Bell System Technical Journal 48(5):1115–1127, May–June 1969.

### Primary acquisition route verified

The Bell System Technical Journal archival index provides an article-level primary
PDF route. A second independent VTDA archive index lists the exact file
`bstj48-5-1115.pdf` (5.2 MB), and the original Bell Labs bibliography records the
same article PDF path.

The automated screenshot backend in the current environment returned a cache miss
when asked to render that 14-page PDF, so the body text was **not** silently
reconstructed from the PDF. The acquisition route is nevertheless now exact and
reproducible.

Primary PDF route:

`https://vtda.org/pubs/BSTJ/vol48-1969/articles/bstj48-5-1115.pdf`

### Abstract-style evidence obtained

A publication record on Peter Weiner's ResearchGate profile summarizes the paper
as studying synthesis by networks of a **fixed module with delay**. It further
states that every binary-input `n`-state sequential machine has an isomorphic
realization using a bounded number of copies of a module with `2r+1` inputs, with
an explicit quantitative bound on the copy count.

The exact displayed formula is truncated by the accessible page rendering, so it
is not reproduced here. The important source-grounded point is narrower: fixed
binary input, one fixed delayed module, isomorphic realization, and quantitative
module-count analysis were already being studied explicitly in 1969.

### Consequence for the novelty gate

This makes the following language unsafe as a residual CCOC novelty claim:

- “old modular synthesis only handled a growing external alphabet”;
- “fixed-input uniform synthesis with delay is new”;
- “a fixed module with bounded response delay is itself the new ingredient.”

The original paper still needs to resolve whether its delay notion equals CCOC's
semantic C5, and whether its module/interconnection fanout is uniformly bounded.
It also does not, from the evidence inspected here, establish C6.

## 4. Related direct-input evidence from Weiner–Hopcroft lineage

A separate abstract-style record for **Weiner & Hopcroft (1967), _Modular
Decomposition of Synchronous Sequential Machines_** defines interconnection
literally: component inputs are connected to logical constants, component outputs,
or external inputs. This makes external-input wiring a first-class part of the
classical decomposition model rather than an incidental detail.

The 1968 Weiner–Hopcroft bounded-fan-in/bounded-fan-out result remains the most
important generic-compiler source because its abstract-style record explicitly
states identical two-state modules and state-count-independent fan-in/fan-out
bounds.

The missing step is to establish from primary text how those external inputs are
distributed and how timing is preserved.

## 5. Drilman & Weiner (1972) strengthens the fixed-input warning

A publication abstract for:

> J. Drilman and Peter Weiner,
> *Modular Networks and Nondeterministic Sequential Machines*,
> IEEE Transactions on Computers 21(10):1124–1129, 1972,

states that the paper defines a family of modules `M_{r,p}` and that `M_{r,p}` can
synthesize sequential machines with `2^p` input symbols.

Again this is abstract-style evidence, not a C3 verdict. But it reinforces the
interpretation that classical modular-synthesis theory parameterized its universal
modules explicitly by input capacity rather than ignoring the input interface.

## 6. Updated residual novelty candidate

After this pass, the historically safest residual CCOC realization claim is not

> fixed alphabet + fixed module + logarithmic/delayed access.

Those ingredients are too close to the 1968–1972 modular-synthesis lineage.

The narrower candidate is the **simultaneous constrained package**:

1. one fixed hardware family;
2. fixed four-symbol global primitive control alphabet;
3. real routing already legal in the closed regime;
4. exactly one newly legal primitive action type opens the response grammar;
5. closed-union quotient remains one bit while open-only innovation is the
   finite-domain maximum `m` bits;
6. pairwise radius-one dynamics;
7. maximum degree three;
8. constant local node/message state grammar;
9. `Theta(log m)` addressed access in the explicit relay;
10. the closed/open comparison is performed on the **same hardware**, by changing
    admissible control grammar rather than recompiling the network.

Even this package must not be called historically first until the primary old
compiler papers are checked. In particular, Hsieh–Tan–Newborn 1968 weakens C3/C5
as standalone discriminators, while Weiner–Hopcroft 1968 threatens bounded
fanout/locality. C6 may become the most structurally distinctive remaining clause.

## 7. Decision rule

### If Hsieh/Ullman–Weiner + Weiner–Hopcroft compose cleanly

If primary texts establish that, for a fixed input dimension, one can uniformly
compile arbitrary synchronous machines with:

- bounded local state;
- bounded fanout/degree;
- direct/fixed input semantics;
- constant or comparable semantic delay;
- and the same compiled hardware remains valid when only admissible input
  languages are restricted,

then the bounded-local/logarithmic-access existence side of CCOC is mostly
classical. The relay should be presented as an unusually clean extremal witness,
not a new realization phenomenon.

### If C6 or one bounded-resource clause fails

If the classical module/interconnection must be redesigned when the input
specification changes, or if bounded fanout and fixed control require a materially
larger semantic delay/resource, the explicit CCOC construction retains a
quantitative/structural distinction.

## 8. Source pointers

Primary/authoritative bibliographic and archive routes:

- Hsieh–Tan–Newborn DBLP record:
  `https://dblp.org/rec/conf/acm/HsiehTN68`
- Hsieh–Tan–Newborn DOI:
  `https://doi.org/10.1145/800186.810625`
- Bell System Technical Journal issue record:
  `https://onlinelibrary.wiley.com/toc/15387305c/1969/48/5`
- VTDA primary-PDF archive index:
  `https://vtda.org/pubs/BSTJ/vol48-1969/articles/`
- Ullman–Weiner primary PDF:
  `https://vtda.org/pubs/BSTJ/vol48-1969/articles/bstj48-5-1115.pdf`
- Bell System bibliography entry with historical PDF paths:
  `https://ftp.math.utah.edu/pub/tex/bib/bstj1960.html`

Abstract/digest evidence used only for direction and claim control:

- Peter Weiner ResearchGate publication profile (Ullman–Weiner,
  Weiner–Hopcroft, Drilman–Weiner summaries);
- contemporaneous IEEE *Abstracts of Current Computer Literature* digest for
  Hsieh–Tan–Newborn, as already recorded in `newborn_locality_memory_watchlist.md`.

None of the secondary summaries substitutes for primary theorem extraction.