# Universal-compilation source acquisition and evidence audit

> **Status:** novelty-control evidence memo. This file records what has actually
> been verified from accessible sources for the corrected compiler reduction in
> `universal_compilation_reduction_risk.md`. It is not a priority claim and it does
> not infer theorem properties from titles, snippets, or secondary summaries.

## 1. Corrected historical question

The bounded-local CCOC witness would be largely generic if classical sequential-
machine compilation provides one fixed full-language network with all of the
following resources on the declared comparison domain.

- **H1 — bounded locality:** constant local component state plus fan-in/fan-out or
  degree bounded independently of compiled-machine size.
- **H2 — fixed context-independent controls:** source input words are presented
  directly or by one fixed finite-alphabet encoding whose cost is quantified and
  does not depend on which closed/open sublanguage is later being studied.
- **H3 — two-way response-trace faithfulness:** source trace equality holds iff the
  declared compiled observable traces are equal. One-way source-trace decodability
  is insufficient because the compiled observable may introduce spurious closed-
  context distinctions.
- **H4 — bounded timing overhead:** source steps/words are simulated with explicit
  bounded network-round and output-decoding latency.

Under H2 + H3, ordinary same-hardware restriction to a source sublanguage is
**derived**: keep the one compiled network fixed and quantify only over encoded
words from that sublanguage. The old C6 condition is therefore not treated as an
independent hurdle for a true full-language compiler.

A separate restriction/resynthesis question remains for methods, such as some
incomplete-specification decompositions, that synthesize a different network from
each partial specification rather than compile one full machine once.

## 2. Evidence table

Status vocabulary:

- **VERIFIED:** directly supported by primary/authoritative material inspected;
- **PARTIAL:** a nearby/broader property is supported, but the required contract is
  not completely established;
- **UNKNOWN:** inspected material does not establish the property;
- **NOT TARGETED:** source addresses another decomposition resource.

| Source | Material directly inspected | H1 locality | H2 controls | H3 two-way trace faithfulness | H4 timing | Resynthesis note | Current verdict |
|---|---|---:|---:|---:|---:|---|---|
| **Hsieh, Tan & Newborn (1968)**, *Uniform modular realization of sequential machines* | authoritative bibliographic/DOI record plus contemporaneous IEEE literature digest; original ACM paper not yet inspected | PARTIAL | PARTIAL | UNKNOWN | PARTIAL | not established | Major fixed-input/unit-delay risk. The fixed-input positive regime is relevant because CCOC's primitive alphabet is fixed as `m` grows, but primary module/interconnect/trace details remain missing. |
| **Weiner & Hopcroft (1968)**, *Bounded Fan-in, Bounded Fan-out Uniform Decompositions of Synchronous Sequential Machines* | Princeton/CiNii archival records plus abstract-style description; report body not yet inspected | PARTIAL | UNKNOWN | UNKNOWN | UNKNOWN | not established | Most direct bounded-local compiler risk. Accessible evidence supports identical two-state modules with state-count-independent fan-in/fan-out in broad terms, but not H2–H4. |
| **Ullman & Weiner (1969)**, *Uniform Synthesis of Sequential Circuits* | primary Bell System journal/VTDA article route verified; 14-page PDF resolves but renderer cache failure prevented page inspection; an abstract-style publication record reproduces the phrase “isomorphic realization” | UNKNOWN/PARTIAL | PARTIAL | **PARTIAL** | PARTIAL | not established | H3 is now a stronger historical risk than before: “isomorphic realization” is exactly the kind of semantic preservation that could satisfy the response-faithfulness requirement at the designated external output. The construction body is still required before marking H3 verified or inferring locality/timing constants. |
| **Arnold, Tan & Newborn (1970)**, *Iteratively Realized Sequential Circuits* | IBM Research primary abstract | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | not established | Primary abstract verifies arbitrary synchronous flow-table realization as a regular array of identical modules. It does not settle the corrected reduction contract. |
| **Newborn & Arnold (1972)**, *Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits* | authoritative bibliographic/DOI records; full text not recovered | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | not established | High-priority full-text source. Correct DOI is `10.1109/T-C.1972.223432`. A DBLP “unpaywalled version” link currently resolves to the adjacent Kim–Newborn input-restriction DOI `10.1109/T-C.1972.223521`; this is an acquisition metadata hazard, not evidence about the theorem. |
| **Huang, Cain & Kinney (1972)**, *Output Sufficient Modules for Uniform Decomposition of Synchronous Sequential Circuits* | bibliographic record plus abstract/summary material | NOT TARGETED/PARTIAL | **PARTIAL** | UNKNOWN | UNKNOWN | not established | The accessible summary says the number of inputs required by an output-sufficient module grows exponentially with the input count of the source sequential machines. Because CCOC holds the primitive input alphabet fixed as `m` grows, that historical lower-bound direction does **not** by itself force an `m`-dependent module-input cost. It therefore weakens H2 as an easy escape hatch, while still not proving fixed external-control distribution. |
| **Williams (1975)**, *Uniform Decomposition of Incompletely Specified Sequential Machines* | authoritative bibliographic record; secondary abstract-style descriptions retained only as acquisition leads | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | **DECISIVE** | The central question is whether each incomplete specification is resynthesized into a new component set/wiring or whether one full-machine realization is merely restricted. |
| **Jóźwiak & Ślusarczyk (2004)**, *General decomposition of incompletely specified sequential machines with multi-state behavior realization* | primary ScienceDirect article/abstract material | PARTIAL | UNKNOWN | PARTIAL/UNKNOWN | PARTIAL | specification-dependent decomposition is in scope | Confirms that incomplete-specification plus constrained network decomposition is mature prior art. It does not establish one exact full-language compiler with H1–H4. |

## 3. Source-specific extraction status

### 3.1 Hsieh–Tan–Newborn (1968)

DBLP/DOI identify the ACM paper `10.1145/800186.810625`. A contemporaneous IEEE
literature digest reports a unit-delay logical-completeness distinction between
unbounded input dimension and a positive fixed-input-dimension regime.

That evidence is sufficient only for claim control: **fixed input dimension** and
**unit-delay modular synthesis** are historical themes. The original paper is
still required to extract:

- exact meaning of number of inputs;
- module state/input size as a function of that number;
- fan-in/fan-out or wiring constraints;
- formal unit-delay semantics;
- external input presentation;
- whether the observable realization is two-way trace faithful.

### 3.2 Weiner–Hopcroft (1968)

The Princeton archive confirms Digital Systems Laboratory Technical Report no. 61.
CiNii identifies a University of Tokyo General Library holding, call number
`U600:769`, record `0004766739`.

Accessible abstract-style evidence describes identical two-state modules with
fan-in/fan-out bounded independently of original machine state count. Because the
report itself has not been read, keep H2–H4 `UNKNOWN`.

The primary report must answer:

1. how source inputs enter/distribute through the network;
2. whether input presentation is context-independent;
3. what output is declared and whether source-equivalent states can produce any
   extra observable compiled distinction;
4. one source clock versus network rounds;
5. output latency;
6. module count and graph depth/diameter.

### 3.3 Ullman–Weiner (1969)

The Bell System Technical Journal issue and VTDA archive expose the exact primary
article at 48(5):1115–1127 and the direct PDF route
`bstj48-5-1115.pdf`. The web PDF opener resolves it as a 14-page document, but the
page-render/screenshot backend currently returns cache-miss errors, and the local
container cannot retrieve the host because outbound DNS is unavailable.

A publicly indexed abstract-style record additionally states that every binary-
input `n`-state sequential machine has an **isomorphic realization** using copies
of a module with delay. This is stronger claim-control evidence than generic
“behavioral simulation”: if “isomorphic” has its standard sequential-machine
meaning at the declared external output, then the construction is a plausible H3
match rather than merely a one-way simulator.

Do **not** upgrade H3 to VERIFIED from this abstract alone. The primary body must
still establish what object is called isomorphic, which outputs are exposed, and
whether any internal module signals are part of the observation contract.

When render/download succeeds, extract:

- the fixed module definition and its state/input count;
- parameters in the quantitative copy-count theorem;
- external input wiring/encoding;
- the exact definition of “isomorphic realization” and whether it gives two-way
  response-trace faithfulness on the embedded source states;
- formal meaning of “delay” and source-step timing;
- fanout/connectivity restrictions.

### 3.4 Arnold–Tan–Newborn (1970)

The IBM Research primary abstract states that an arbitrary synchronous flow table
can be realized as an array of identical modules interconnected in a regular
pattern. This kills broad novelty language based on repeated identical modules.

The abstract does not establish H1 constants, H2 controls, H3 equivalence
preservation, or H4 timing.

### 3.5 Newborn–Arnold (1972)

Correct source:

> Monroe M. Newborn and Thomas F. Arnold, *Universal Modules for Bounded Signal
> Fan-Out Synchronous Sequential Circuits*, IEEE Transactions on Computers
> 21(1):63–79, DOI `10.1109/T-C.1972.223432`.

A prior audit incorrectly mapped DOI `223521` to this paper; that DOI belongs to
Kim–Newborn's *The Simplification of Sequential Machines with Input Restrictions*.
A fresh acquisition pass found a related metadata trap: DBLP's “unpaywalled
version” link attached to the Newborn–Arnold entry currently routes to DOI
`10.1109/T-C.1972.223521`, i.e. the Kim–Newborn paper. Therefore automated DOI
following must validate title/authors before treating any retrieved PDF as the
Newborn–Arnold source.

No H1–H4 status is upgraded from the title alone.

### 3.6 Huang–Cain–Kinney (1972): why input-dimension lower bounds do not rescue H2

The accessible summary for *Output Sufficient Modules for Uniform Decomposition of
Synchronous Sequential Circuits* reports that the number of inputs needed by an
output-sufficient universal module grows exponentially with the number of inputs
to the source sequential machines.

This is historically important but does not provide a scaling obstruction for the
current CCOC family: the primitive source input alphabet/control dimension is held
fixed as the number `m` of dormant coordinates grows. An exponential function of a
fixed input count is still a constant with respect to `m`.

Therefore the manuscript must **not** argue that classical universal-module
compilers necessarily lose H2 merely because universal module input count can grow
with source input dimension. The remaining H2 question is concrete: for a fixed
source input alphabet, does one classical construction distribute/encode each
source input with cost bounded independently of the source state count and of the
later closed/open sublanguage restriction?

### 3.7 Williams (1975)

Williams remains important, but for a more precise reason after the compiler-
contract correction.

If Williams takes each incomplete specification and runs a new decomposition or
minimal-cover synthesis, it is strong prior art for **context-dependent uniform
decomposition** but does not provide the one-full-machine compiler used in the
restriction-compatibility lemma.

If instead the paper proves that one full realization is fixed and restrictions
only change admissible controls/behavior, it becomes much more dangerous.

Primary extraction therefore asks what changes when the specification changes:
component count, component identities, wiring, external controls, or only the set
of admissible source behaviors.

## 4. What is already blocked as novelty

The audit supports no priority claim for the following ingredients in isolation:

- repeated identical local modules;
- uniform modular realization of arbitrary sequential behavior;
- fixed-input modular synthesis;
- delayed/fixed-module synthesis;
- bounded fan-in/fan-out modular realization as a broad idea;
- incomplete-specification plus constrained decomposition.

These are substrate or historical ancestry.

## 5. What remains unresolved

The audit has **not** verified a classical primary theorem that simultaneously
provides:

1. H1 bounded local resources;
2. H2 fixed context-independent controls with comparable encoding cost;
3. H3 two-way response-trace faithfulness on the embedded source states;
4. H4 comparable timing/output latency.

Nor has it proved that no such classical theorem exists.

Two candidate escape hatches are now weaker than they previously appeared:

- **H2:** historical input-count lower bounds do not force growth with `m` when
  CCOC's source input dimension is fixed;
- **H3:** Ullman–Weiner's indexed “isomorphic realization” wording is consistent
  with exactly the sort of two-way semantic preservation the compiler reduction
  needs, pending primary-text verification.

The corrected manuscript-safe status is therefore:

> Classical sequential-machine synthesis already contains closely related
> fixed-input, fixed-module/delay, bounded-fanout, and incomplete-specification
> constructions. CCOC's explicit relay should be treated as a constrained
> sharpness witness while the audit asks whether one classical full-language
> compiler satisfies bounded locality, fixed controls, two-way response-trace
> faithfulness, and comparable timing. If it does, same-hardware closed/open
> restriction follows automatically.

## 6. Revised acquisition priority

1. **Weiner–Hopcroft (1968)** — strongest H1 source; obtain report no. 61 and
   extract H2–H4.
2. **Ullman–Weiner (1969)** — primary PDF location is exact; resolve renderer/tool
   access and verify what “isomorphic realization” means, plus H1/H2/H4.
3. **Hsieh–Tan–Newborn (1968)** — obtain original ACM paper; fixed-input/unit-delay
   source most relevant to H2/H4.
4. **Newborn–Arnold (1972)** — bounded-signal-fanout universal-module details and
   relation to input distribution; validate DOI/title because of the DBLP cross-link
   metadata hazard.
5. **Williams (1975)** — determine full-machine restriction versus per-
   specification resynthesis.
6. **Huang–Cain–Kinney (1972)** — inspect the primary theorem to separate module
   input-count growth in source input dimension from source-state-count growth.

## 7. Decision rule

### A. H1–H4 all hold with constant/comparable overhead

Demote bounded-local/logarithmic-access realization novelty. Keep the explicit
relay for clarity and sharp constants only.

### B. One-way simulation but H3 fails

The classical compiler may preserve all open source distinctions while adding
spurious closed distinctions. It does not directly reproduce the complete CCOC
closed/open quotient separation.

### C. H1 holds but H2 or H4 is expensive

The explicit four-symbol, degree-three, radius-one, logarithmic-access relay may
retain a quantitative realization distinction. This claim now requires actual
state-count-dependent H2/H4 evidence; fixed source-input-dimension lower bounds are
not enough.

### D. Incomplete-machine methods resynthesize hardware

Treat them as strong contextual-decomposition ancestry, not as a direct
same-hardware full-language compiler.

## 8. Source pointers and acquisition records

Canonical supporting records in this repository:

- `universal_compilation_reduction_risk.md` — corrected reduction contract;
- `universal_compiler_acquisition_log_2026-08-12.md` — retrieval log;
- `universal_compiler_archive_route_2026-08-12.md` — preserved IEEE issue routes;
- `fixed_input_unit_delay_historical_risk_2026-08-12.md` — fixed-input/delay
  historical warning;
- `universal_compiler_c3_c6_directional_leads_2026-08-12.md` — dated pre-
  correction directional memo; read with the corrected contract in this file;
- issue #122 — live novelty gate;
- issue #137 — Ullman–Weiner PDF rendering blocker.

External source routes already verified by the audit include the Princeton/CiNii
Weiner–Hopcroft report records, Bell System/VTDA Ullman–Weiner article route, IBM
Research Arnold–Tan–Newborn abstract, DBLP/DOI records for Hsieh–Tan–Newborn and
Newborn–Arnold, the Huang–Cain–Kinney bibliographic/abstract record, and the primary
2004 ScienceDirect decomposition article.

Secondary abstract/digest records are retained only as acquisition/claim-control
leads and never substitute for original theorem extraction.