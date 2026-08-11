# Quantitative prior-art addendum: fixed-input and delay lineage — 2026-08-12

> **Purpose.** Add the Hsieh–Tan–Newborn / Ullman–Weiner fixed-input and delay
> lineage to the residual quantitative novelty gate without prematurely converting
> secondary abstracts/digests into `YES` entries in the main matrix. The canonical
> matrix remains `quantitative_prior_art_matrix.md`; this addendum should be folded
> into it after primary-text extraction.

## 1. Newly relevant comparison rows

| Prior work | Fixed input regime | Uniform / fixed module | Bounded fanout / degree | Timing / delay | Restricted→open same-hardware semantics | Quantitative relevance to CCOC | Evidence level |
|---|---|---|---|---|---|---|---|
| **Hsieh–Tan–Newborn 1968**, *Uniform modular realization of sequential machines* | **PARTIAL:** contemporaneous IEEE digest explicitly distinguishes arbitrary input dimension from fixed `n`-input machines | **PARTIAL:** digest reports uniform modular realization for fixed input dimension | **UNKNOWN** | **PARTIAL:** digest explicitly formulates a `unit delay` logical-completeness result/limitation; exact delay semantics await original paper | **UNKNOWN** | Major risk because CCOC's global primitive alphabet stays fixed as `m` grows; dependence of the historical module on fixed input dimension would still be `O(1)` in `m` | contemporaneous secondary digest + DBLP/DOI |
| **Ullman–Weiner 1969**, *Uniform Synthesis of Sequential Circuits* | **PARTIAL:** abstract-style record explicitly says binary-input machines | **PARTIAL:** network of a fixed module with delay; isomorphic realization and quantitative copy bound reported | **UNKNOWN** | **PARTIAL:** delay is explicit, but semantic source-step/network-round meaning unverified | **UNKNOWN** | Directly kills any broad claim that fixed-input + fixed-module + delay is a new CCOC combination | primary PDF route verified; body not rendered; abstract-style publication record inspected |
| **Drilman–Weiner 1972**, *Modular Networks and Nondeterministic Sequential Machines* | **PARTIAL:** abstract says module family `M_{r,p}` synthesizes machines with `2^p` input symbols | **PARTIAL** | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Shows input capacity was an explicit parameter of classical modular-network design; relevant to C3 resource accounting | abstract-style publication record + bibliographic record |

No row above is evidence for the CCOC restricted→open quotient gap itself. These
sources threaten the **realization novelty**, not the extension–compression
response-complexity accounting by themselves.

## 2. Why fixed input dimension matters for the current relay

The strengthened CCOC open action alphabet is

\[
A_O=\{0,1,\mathsf{fire},\mathsf{tick}\},
\]

independent of `m`. Thus the family lies in a fixed finite control-interface
regime. Even if an older universal module depends on the number of source input
terminals, that dependence may be a constant across the CCOC asymptotic family.

Therefore the following inference is **not safe**:

> historical universal modules fail for arbitrary input dimension, therefore a
> fixed four-symbol CCOC interface is novel.

The primary Hsieh paper must first be checked for its input convention and the
resources that depend on fixed `n`.

## 3. Residual quantitative package after this addendum

The main matrix previously treated the residual package as a simultaneous
combination of maximal response inflation and bounded-local realization. The new
historical evidence narrows the realization side further.

The currently unmatched package is now best written as:

\[
|P_U|=2,
\qquad
|P_O|=2^{m+1},
\qquad
\iota_{new}=m,
\]

on one fixed hardware family, together with:

- fixed four-symbol primitive global control alphabet;
- exactly one newly legal primitive action type;
- closed routing already active before that action is legalized;
- pairwise radius-one local dynamics;
- maximum degree three;
- local state/message alphabets bounded independently of `m`;
- logarithmic addressed access;
- **same-hardware** comparison of closed and open grammars.

The first three historical rows above make “fixed input,” “fixed module,” and
“delay” too weak to list as standalone novelty features.

## 4. What could still collapse the residual package

### Historical fixed-input + bounded-fanout compiler

If Hsieh/Ullman–Weiner fixed-input synthesis can be combined directly with the
Weiner–Hopcroft bounded-fan-in/fan-out construction at constant semantic delay,
the local realization of the centralized CCOC witness may follow generically.

### Same-hardware language restriction

Even a universal compiler does not automatically settle the CCOC experiment if a
new hardware network must be synthesized for each restricted/incomplete source
specification. A direct C6 theorem—one compiled network, different admissible input
languages—would be much more dangerous.

### Input encoding hidden in the network

A fixed source alphabet alone is not enough. The primary papers must show whether
source control symbols are broadcast/directly wired, or whether decoding/distribution
requires an `m`- or machine-size-dependent interface whose complexity was not
counted as part of the module.

## 5. Decision for manuscript wording

### Still allowed

> We give an explicit extremal response-separation family under a fixed four-symbol
> control interface, degree-three radius-one dynamics, constant local state grammar,
> and logarithmic addressed access. Classical modular-synthesis work already covers
> closely related fixed-input, fixed-module, delayed, and bounded-fanout
> realizations separately; whether one classical compiler subsumes this entire
> restricted/open package remains under primary-source audit.

### Now explicitly disallowed

- “Fixed-input uniform modular synthesis is new.”
- “Using one fixed module with delay is new.”
- “A constant global action alphabet separates CCOC from classical modular
  synthesis.”
- “Unit-delay universal modular realization was impossible before CCOC.”

## 6. Primary-text merge gate

Fold these rows into `quantitative_prior_art_matrix.md` only after the following
are extracted from primary sources:

1. Hsieh–Tan–Newborn 1968: definition of `n` inputs, exact unit-delay theorem,
   module dependence on `n`, fanout/interconnection;
2. Ullman–Weiner 1969: exact `r,p` definitions, module-copy bound, delay semantics,
   fanout/depth;
3. Weiner–Hopcroft 1968: compatibility of bounded fan-in/out with fixed-input
   semantics and clocking;
4. Williams 1975: same-hardware restriction versus re-synthesis.

Until then, the addendum is a novelty-control warning, not a priority verdict.