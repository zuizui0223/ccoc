# Newborn–Arnold 1972 primary acquisition route — 2026-08-13

> **Purpose.** Convert the highest-priority H1/H2 source in issue #122 from an
> unreliable DOI/full-text target into an actionable Japanese primary-copy route.
> This is acquisition/claim control only. No compiler resource is promoted until
> the article body is actually read.

## 1. Exact article identity

Target:

> Monroe M. Newborn and Thomas F. Arnold, *Universal Modules for Bounded Signal
> Fan-Out Synchronous Sequential Circuits*, IEEE Transactions on Computers,
> volume 21, number 1, January 1972, pp. 63–79.

DBLP independently records the article in volume 21(1), pages 63–79. The canonical
DOI already validated in the repository is:

`10.1109/T-C.1972.223432`

Do not accept `10.1109/T-C.1972.223521` for this article. That DOI belongs to
Kim & Newborn, *The Simplification of Sequential Machines with Input
Restrictions*. An automated route has previously cross-wired the two adjacent
records, so every recovered copy must be title/author-validated before admission.

## 2. Japanese physical holding covers the target year

CiNii Books record `AA00667773`, titled

`IEEE transactions on computers trans & computer group news`,

lists one Japanese holding:

> **大阪府立中央図書館 — 1969–1973**.

The target January 1972 issue falls inside that recorded run.

A broader CiNii author/title index also records the ordinary print title
`IEEE transactions on computers` as held by hundreds of Japanese libraries. This
provides fallback ILL routes if the Osaka holding proves incomplete at issue level.

The Osaka run is the preferred first route because its year coverage is explicit.

## 3. Osaka provides a direct remote-copy service

The current official Osaka Prefectural Library usage guide says that copies of its
holdings may be requested without visiting the library. For written requests it
accepts article-level bibliographic information including journal title/volume,
author, article title, and pages.

More importantly, the library's **Web複写サービス** is available to anyone:

- the OPAC record can be used to start a copy request;
- a user may apply with ordinary registration, Web-only registration, or a
  **one-time/no-registration path**;
- the library contacts the requester if the requested section needs clarification;
- non-visit copy orders are delivered by **post**, not by email;
- copying remains subject to copyright law, source condition, and the library's
  preservation rules.

Thus this paper is no longer an `unrecovered web PDF` blocker. It is an
**actionable primary-copy request**.

## 4. Exact request metadata

Use the following request fields so the library does not need to infer the target:

- journal: `IEEE Transactions on Computers`;
- volume/issue: `C-21(1)` / volume 21, number 1;
- date: January 1972;
- authors: Monroe M. Newborn; Thomas F. Arnold;
- article: `Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits`;
- pages: `63–79`;
- DOI: `10.1109/T-C.1972.223432`;
- CiNii holding record: `AA00667773`;
- holding: 大阪府立中央図書館, 1969–1973.

Request pp. 63–79, subject to the library's copyright determination. Do not ask the
library to resolve the DOI from title alone because of the documented adjacent-
record misrouting hazard.

## 5. Why this source is decisive for CCOC

The title directly targets **bounded signal fan-out** universal modules for
synchronous sequential circuits. That makes it potentially decisive for the
residual relay-realization claim, but the title is not theorem evidence.

The primary body must answer the corrected H1–H4 compiler contract.

### H1 — bounded locality

Extract literally:

1. universal module state cardinality;
2. module input and output arity;
3. exact signal fan-out bound;
4. whether the bound is independent of the number of source-machine states;
5. whether fan-in or graph degree is also uniformly bounded, or whether only
   fan-out is controlled.

### H2 — fixed context-independent controls

Extract:

1. how source input terminals enter the module network;
2. whether a source input is replicated/distributed by additional circuitry;
3. dependence of that distribution on source state count versus source input
   count;
4. whether the construction uses one fixed external alphabet/encoding for the
   full realized machine;
5. whether restricting the legal source input language can be done on the same
   compiled network without changing the encoding/wiring.

Because CCOC keeps the primitive source-control dimension fixed while `m` grows, a
resource depending only on fixed source input count does not yield an `m`-dependent
escape.

### H3 — two-way response-trace faithfulness

Extract:

1. the formal definition of realization/equivalence;
2. which network outputs are designated as source-machine outputs;
3. whether internal/module outputs are observationally hidden;
4. whether equality of source response traces is equivalent to equality of the
   declared compiled response traces on embedded states.

One-way source decoding is insufficient for CCOC: extra designated observables
could create spurious closed-context distinctions.

### H4 — source-step / network-round / output latency

Extract:

1. source clock and module clock conventions;
2. propagation/delay assumptions;
3. when source output is valid after an input change;
4. whether the bound depends on source state count;
5. network depth/diameter or any settling-time bound;
6. module-count asymptotics if stated.

## 6. Decision rule after the copy is recovered

### If H1–H4 hold with comparable overhead

The existence of a bounded-local realization of the elementary CCOC unlock seed
should be demoted as residual novelty. Retain the explicit relay for transparency,
sharp constants, and ecology-facing interpretation, but do not defend a firstness
claim.

### If only bounded fan-out is established

Do not silently convert fan-out into maximum-degree locality. Record exactly which
side of H1 is proved and which remains open.

### If input distribution or latency scales with source state count

The current fixed-control, degree-three, radius-one, logarithmic-access relay may
retain a quantitative realization distinction.

### If realization is only one-way

A classical network may preserve source behavior while adding observable
internal distinctions. It then does not automatically reproduce the small closed
response quotient required by CCOC.

## 7. Stop rule

Do not repeat generic DOI/title mirror searches for this article. The next
information-producing step is one of:

1. submit the Osaka Web copy request for the identified pages;
2. obtain the issue through another CiNii/ILL holding;
3. recover a new verified primary scan from a preserved archive.

Until the primary body is read, **H1, H2, H3, and H4 remain unpromoted**.
