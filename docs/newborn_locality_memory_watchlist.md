# Newborn locality / memory watchlist

> **Status:** mixed evidence. One important modular-realization claim is supported
> by an authoritative IBM abstract; several other items remain bibliographic
> watchlist entries because their full texts were not obtained. Do not infer
> unverified theorem details from titles alone.

The historical novelty search around Kim–Newborn input restrictions surfaced a
cluster of earlier/lateral work by Monroe M. Newborn that is directly relevant to
the **remaining bounded-local extremal CCOC candidate**.

## 1. Arnold, Tan & Newborn (1970): identical-module realization is established

Thomas F. Arnold, Chung-Jen Tan, and Monroe M. Newborn,
**“Iteratively Realized Sequential Circuits,”**
*IEEE Transactions on Computers* 19(1):54–66, 1970.

An authoritative IBM Research publication record provides the abstract. It
states that synthesis techniques are given for realizing **an arbitrary
synchronous flow table as an array of identical modules interconnected in a
regular pattern**, with several structures and corresponding modules considered.

### CCOC consequence

The following cannot be used as novelty claims by themselves:

- realizing an arbitrary / large sequential behavior with repeated identical
  finite modules;
- a constant local module type while system size grows;
- regular modular architecture for sequential-machine realization.

This substantially narrows the role of CCOC's “constant local grammar” claim. Its
possible value is only in the **simultaneous combination** with input-restriction
separation, one-action maximal innovation, pairwise degree-three realization, and
exact query-latency saturation.

## 2. Newborn (1968): maximal-memory watchlist

Monroe M. Newborn,
**“Maximal Memory Binary Input-Binary Output Finite-Memory Sequential Machines.”**
*IEEE Transactions on Computers* 17(1):67–71, 1968.

OhioLINK also indexes Newborn's 1967 Ohio State PhD dissertation,
**“Maximal memory binary input-binary output sequential machines.”**

These titles are especially important for the CCOC memory-sharpness audit because
the current relay realizes a binary controlled system whose open interface
retains the maximum possible dormant-memory distinctions on the declared domain.
The current audit did **not** obtain the paper or dissertation text, so no claim
about what “maximal memory” means in those works is made here.

## 3. Hsieh, Tan & Newborn (1968): uniform modular realization

Edward P. Hsieh, Chung-Jen Tan, and Monroe M. Newborn,
**“Uniform modular realization of sequential machines.”**
ACM National Conference 1968:613–621.

A contemporary IEEE literature digest available through CiteSeer summarizes the
problem as realizing synchronous Moore machines with a finite set of sequential
modules and discusses logical completeness limitations. The full original paper
was not obtained in the current audit, so this remains a high-priority source for
full review.

## 4. Earlier iterative sequential-circuit lineage

### Arnold, Tan & Newborn (1968)

**“Iteratively Realized Sequential Circuits.”**
SWAT 1968:431–448.

### Arnold & Newborn (1969)

**“Iteratively Realized Sequential Circuits: Further Considerations.”**
SWAT 1969:194–212.

These are direct predecessors of the 1970 IEEE paper whose abstract explicitly
supports arbitrary synchronous-flow-table realization by arrays of identical
modules.

## 5. Newborn & Arnold (1972): bounded-fanout watchlist

Monroe M. Newborn and Thomas F. Arnold,
**“Universal Modules for Bounded Signal Fan-Out Synchronous Sequential
Circuits.”**
*IEEE Transactions on Computers* 21(1):63–79, 1972.

The bibliographic record is verified, but the full text was not obtained in this
audit. The paper is a top-priority locality source because the current CCOC
residual candidate relies on bounded degree/fan-out-like constraints and a fixed
local grammar.

A later paper, **“Output sufficient modules for uniform decomposition of
synchronous sequential circuits,”** cites Newborn–Arnold (1972) in the context of
universal modules and explicitly discusses the number of inputs a universal
module must have. This confirms that the paper belongs to a genuine modular
sequential-circuit theory lineage, but does not by itself establish that it
contains the specific CCOC construction.

## 6. Revised locality novelty boundary

After the IBM abstract, even **constant-local modular realization of arbitrary
sequential behavior** is prior art. Combined with the nonlocal unlock-and-scan
baseline documented elsewhere, CCOC should not claim novelty for:

- one new action causing maximal interface innovation in a centralized machine;
- pre-existing routing plus one revealing action without locality;
- repeated identical local modules / constant module type alone;
- bounded-fanout modular sequential realization as a broad idea.

The unresolved candidate is now stricter:

> the *same* family couples `m` fixed one-bit input-restricted contexts and a
> one-bit closed union/join capacity to **absolute-maximal one-action open
> innovation**, while realizing the effect with four global action symbols,
> pairwise adjacent updates, maximum degree three, constant local state/message
> grammar, and zero latency slack under its explicit selector-plus-pulse local
> architecture.

No direct historical match for this entire package has been established.

## 7. Verified provenance and missing evidence

Supported beyond bibliographic title:

- Arnold–Tan–Newborn 1970: IBM Research abstract explicitly states arbitrary
  synchronous flow-table realization using arrays of identical modules in a
  regular pattern.
- Hsieh–Tan–Newborn 1968: a contemporary IEEE literature digest summarizes its
  finite-module / logical-completeness problem.

Bibliographic/watchlist only in the present audit:

- Newborn 1968 maximal-memory paper;
- Newborn 1967 maximal-memory dissertation (OhioLINK metadata confirms it);
- Newborn–Arnold 1972 bounded-fanout universal-module paper;
- the full 1968/1969 iterative papers.

This file is deliberately a **do-not-overclaim checkpoint**. Missing full texts
are a reason to weaken priority language, not a license to fill in theorem details
from memory or titles.
