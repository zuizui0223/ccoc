# CCOC–MLTR claim firewall — 2026-08-16

## Decision

CCOC and MLTR may share finite controlled-system notation and exact-interface substrate, but they answer different quantified questions and must not share a headline theorem.

## CCOC question: simultaneous open-future compressibility

CCOC asks whether systems that are individually easy to compress under each fixed closed future grammar can require a much larger exact interface when those futures are made jointly legal.

For closed grammars \(\Gamma_i\), let

\[
K_i^* = \min_{q\text{ exact under }\Gamma_i} \log_2 |q|,
\]

and for an open grammar \(\Gamma_O\), let

\[
K_O^* = \min_{q\text{ exact under }\Gamma_O} \log_2 |q|.
\]

The CCOC headline is a cross-grammar separation of the form

\[
\max_i K_i^* = O(1),\qquad K_O^* = \Omega(m),
\]

with explicit bounded-local witness families. The closed optima are allowed to be different partitions. No inherited source partition is fixed in the statement.

**CCOC headline:** individual closed-context compressibility does not imply one comparably small exact interface for an open future grammar.

## MLTR question: source-relative transport and repair

MLTR instead fixes an already accepted source macro-law \(q_S\), carries its labels through a declared source–target relation, tests whether those inherited labels remain exact in the target, and—if not—asks for the unique coarsest exact target refinement constrained to preserve inherited semantics.

Its optimization is therefore source-relative:

\[
\min_{q_T\text{ exact},\;q_T\succeq \operatorname{carry}(q_S)} |q_T|.
\]

MLTR may allow the target operational grammar to differ from the source grammar, but it does not optimize independently over a family of closed grammars and does not claim CCOC's universal-interface lower bound.

## Non-overlap rule

### CCOC owns

- the cross-grammar extension–compression gap;
- lower bounds on the minimum exact open interface;
- bounded-local sharpness witnesses showing that the gap survives simple local structure;
- positive/negative portability statements only as boundaries supporting the lower-bound theorem.

### CCOC does not own

- unique coarsest repair of a fixed inherited source partition;
- transport defect relative to an inherited source law;
- path-label coherence across replacement histories;
- minimum history completion.

Those belong to MLTR.

### MLTR owns

- unchanged portability of a fixed inherited macro-law under a declared source–target change;
- unique coarsest source-relative exact repair;
- transport defect defined from that repair;
- route coherence and minimum history context.

### MLTR does not own

- the claim that every closed grammar admits a small optimum while the jointly open grammar has a large minimum exact interface;
- the bounded-local cross-grammar sharpness theorem;
- a universal-open-interface complexity lower bound independent of a fixed inherited partition.

## Registry consequence

CCOC `CORE-2` is the headline theorem candidate. `CORE-1` is foundational exact-interface substrate and `CORE-3` is its sharpness witness. `CORE-4` and `CORE-5` remain executable supporting boundaries, but they must not be advertised as the CCOC novelty claim or expanded into a repair theorem family.

## Development stop rule

A proposed CCOC result is out of scope if its main output is a repaired refinement of one fixed inherited partition, a repair-defect statistic, or history-mode augmentation. Route that work to MLTR instead.

A proposed MLTR result is out of scope if its main quantifier is over independently optimized closed grammars versus one jointly open grammar and its conclusion is a lower bound on the minimum exact open interface. Route that work to CCOC instead.
