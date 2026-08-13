# Ullman–Weiner (1969) primary-text OCR extraction

> **Status:** primary-text claim-control memo. The Bell System Technical Journal article itself is publicly available as a 14-page PDF, but the current PDF screenshot backend still returns a cache-miss. A separate scan of the complete May–June 1969 BSTJ issue hosted by WorldRadioHistory is indexed with OCR text, and the search index exposes verbatim passages from the article. This memo records only what those primary-text OCR passages directly support.

## Source

J. D. Ullman and Peter Weiner, *Uniform Synthesis of Sequential Circuits*, Bell System Technical Journal 48(5):1115–1127, May–June 1969.

Primary routes confirmed in this audit:

- VTDA/BSTJ article PDF: `bstj48-5-1115.pdf` (14 pages)
- Internet Archive item identifier exposed by the TCI BSTJ index: `bstj48-5-1115`
- WorldRadioHistory complete BSTJ May–June 1969 issue scan, whose indexed OCR exposes the article text

The screenshot renderer still fails on the VTDA PDF, so figures and later construction pages have not been visually inspected here.

## Directly recovered primary text

The indexed OCR exposes the article title, authors, manuscript date, abstract, and opening paragraphs. It directly states that the paper studies synthesis of sequential machines by networks of a **fixed module with delay** and that every **binary-input n-state sequential machine has an isomorphic realization** using a bounded number of copies of a module with `2r+1` inputs.

The introduction further states that the constructed machines are fast: the **time between source inputs need not exceed the time required for a single module to resolve its output after an input change, regardless of how many modules are in the network**. It also notes that clock-control and initialization wiring are omitted from the diagrams.

These are primary-text statements from the 1969 paper, not a secondary abstract.

## H1–H4 consequences

### H1 — bounded locality

**Still unresolved from the recovered passages.**

The paper uses copies of a fixed module, so component type/state complexity is fixed for a chosen construction. However, the recovered OCR does not establish the fan-out/network-degree bound needed by the CCOC compiler contract. Do not infer H1 from the phrase “fixed module” alone.

### H2 — fixed context-independent controls

**PARTIAL.**

The target class is explicitly binary-input source machines, so the source control alphabet is fixed. The recovered passages do not yet show how that source input is physically distributed to module inputs, nor whether a machine-size-dependent input-distribution tree or encoding is required. Thus H2 remains unresolved at the quantitative wiring/distribution level.

### H3 — two-way response-trace faithfulness

**Strong PARTIAL risk.**

The paper itself—not merely a secondary record—uses the phrase **isomorphic realization** for every binary-input n-state machine. In standard sequential-machine usage this is much stronger than one-way simulation and is exactly the kind of statement that can preserve both source distinctions and source equivalences at the designated machine interface.

However, the current audit has not recovered the paper’s formal definition of realization/isomorphism or the exact set of externally observed outputs. H3 therefore remains PARTIAL rather than VERIFIED until those definitions/construction pages are read.

### H4 — bounded timing overhead

**Primary-text PARTIAL, materially strengthened.**

The introduction explicitly says that the time between inputs need not grow with the number of modules: it is bounded by the response time of a single module after an input change. This removes “network-size-dependent per-input settling time” as a plausible easy novelty boundary for this paper.

What is still missing is the formal relation between that physical settling-time statement and the exact synchronous source-step / output-trace semantics used by CCOC. Until the construction is read, avoid translating it into a theorem-level equality such as “one source step = one compiled round.”

## Novelty consequence

The historical compiler risk is now stronger than the previous source audit recorded:

- fixed source input is explicitly in scope;
- fixed repeated module with delay is explicitly in scope;
- isomorphic realization is stated in the primary paper;
- per-input settling time is explicitly independent of network size.

Accordingly, the CCOC bounded-local relay should remain a **sharpness witness**, not a firstness-bearing existence theorem. The remaining potentially meaningful realization distinctions are concentrated on the simultaneous package of:

1. bounded fan-out / graph degree and constant local state;
2. fixed, quantitatively cheap external-input distribution;
3. formal two-way trace faithfulness at the designated output interface; and
4. the exact clock/round semantics needed to compare `Theta(log m)` access latency.

If later primary pages verify all four with comparable constants, bounded-local/logarithmic-access existence must be fully demoted to classical compilation plus an explicit CCOC construction.

## Acquisition status

The acquisition problem is no longer “no primary text available.” The article itself and a primary OCR route are identified, and the introduction/abstract have been recovered. The remaining blocker is **construction-page extraction** (module wiring, isomorphism definition, fan-out, external-input distribution, and clock semantics).

This should replace any wording that treats Ullman–Weiner (1969) as abstract-only evidence.