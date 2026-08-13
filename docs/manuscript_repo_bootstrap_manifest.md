# `rach-open-composition-paper` bootstrap manifest

> **Claim-control version: 2026-08-13.** This is a transfer contract, not manuscript
> prose. It supersedes the earlier framing in which the bare cross-grammar
> noncommutation/codebook bound could be read as the firstness-bearing novelty.

## 1. Current research decision

The finite theorem package remains mathematically useful and should be transferred
to the manuscript, but **formal theorem role and novelty role are now separate**.

### Formal substrate carried into the paper

- finite deterministic controlled system;
- declared legal future-word grammar;
- exact response quotient / grammar-aware interface;
- grammar enlargement refines the response equivalence;
- pair-separating/addressable codebooks give open-interface cardinality lower
  bounds;
- supplied closed factorizations give closed-interface upper bounds;
- conservative finite macro schemas give a sufficient positive portability
  condition.

These objects make the ecological/compositional question precise. They are **not
assigned historical firstness**.

### Explicitly demoted as novelty

Do not claim novelty for:

1. fixed-grammar Myhill--Nerode/bisimulation-style quotient machinery;
2. environment/input/context-dependent state minimization;
3. generic large or exponential descriptional advantage under restricted domains;
4. common refinement / natural-join / product-capacity accounting;
5. the broad slogan that state reduction/compression and realization/composition
   need not commute (Hartmanis--Stearns 1962 is direct ancestry);
6. the bare pair-separating/codebook cardinality argument;
7. a centralized construction in which one newly legal action exposes many
   previously irrelevant distinctions;
8. repeated fixed modules, fixed-input modular synthesis, bounded fan-in/fan-out,
   or delayed universal modules as ideas in isolation;
9. generic finite-speed/local causal-cone bounds.

### Residual firstness candidate only

The only remaining candidate is the **simultaneous extremal/local package** of the
explicit relay family:

\[
|P_j|=2\quad\forall j,
\qquad |P_U|=2,
\qquad |P_O|=2^{m+1},
\qquad \iota_{\rm new}=m,
\]

with `iota_new=m` saturating the finite-domain maximum, while the same family has:

- only one newly legal primitive action (`fire`);
- fixed global control alphabet `{0,1,fire,tick}`;
- real routing already legal in the closed regime;
- bounded local state/message alphabets;
- pairwise radius-one dynamics;
- maximum degree three;
- `O(log m)` causal access and exact `2 log2(m)+2` length in the declared
  selector-plus-return architecture.

Even this is **conditional**. Issue #122 asks whether a classical universal
sequential-machine compiler already supplies comparable H1--H4 resources. If it
does, the relay remains a transparent extremal construction but loses a
firstness-bearing existence claim.

## 2. Target repository and manual blocker

Target:

`zuizui0223/rach-open-composition-paper`

Recommended initial state:

- private while drafting;
- default branch `main`;
- initialize with README;
- do not copy `causal_model/` into the manuscript repository.

Issue #141 remains a genuine manual blocker. The connected GitHub tool surface has
no repository-creation action, and the current execution environment also lacks an
authenticated `gh` CLI.

## 3. Initial directory contract

```text
rach-open-composition-paper/
  README.md
  manuscript/
    main.tex
    sections/
      01_ecological_question.tex
      02_response_interface_formalism.tex
      03_cross_grammar_lower_bound.tex
      04_extremal_one_action_family.tex
      05_bounded_local_realization.tex
      06_positive_portability.tex
      07_ecological_interpretation.tex
      08_discussion.tex
    references.bib
  supplement/
    theorem_proofs.tex
    reproducibility.tex
    related_work_audit.tex
  figures/
    README.md
  traceability/
    CCOC_PIN.md
    THEOREM_MAP.md
    CLAIM_BOUNDARY.md
    REPLAY_PIN.md
  submission/
    cover_letter.tex
    reviewer_candidates.md
```

The section names intentionally avoid making “noncommutation” a novelty label.

## 4. Manuscript theorem roles

### Definition / substrate

Define the exact grammar-aware response interface on a declared finite controlled
system. State the response-kernel viewpoint if useful:

\[
\sim_L=\bigcap_{w\in L}\ker R_w.
\]

Use this as formal machinery, not a novelty claim.

### Theorem 1 — operational cross-grammar lower bound

State the addressable codebook/product result and the closed/open comparison. The
proof is a direct pair-separation/injection argument. It belongs in the paper
because it makes the model contract auditable, **not because pair separation itself
is claimed new**.

### Quantitative family

Present constrained codebooks only as robustness/context. The main quantitative
construction should be the one-action family with one-bit fixed closed quotients,
one-bit closed union, and maximal `m`-bit open-only innovation.

### Local realization

Present the degree-three relay as the strongest remaining contribution candidate.
Its historical status must be written conditional on #122.

### Positive boundary

Present conservative macro-schema portability as a sufficient constructive
counterpart. Do not imply necessity.

## 5. Current source-acquisition gate

The compiler gate is no longer a broad web-search task. The relevant primary
sources now have concrete acquisition routes:

- **Weiner--Hopcroft 1968 report no. 61:** University of Tokyo / Princeton
  physical-copy route;
- **Newborn--Arnold 1972:** Osaka Prefectural Central Library direct Web-copy
  route, C-21(1):63--79, correct DOI `10.1109/T-C.1972.223433`;
- **Drilman--Weiner 1972:** same Osaka holding, C-21(10):1124--1129, fixed-module
  synthesis plus nondeterministic-machine lead;
- **Williams + Le Van--van Houtte 1975:** Tokyo University of Technology physical
  C-24(8) route;
- the same Tokyo holding covers the 1978 correction/resource papers and the 1982
  comparative follow-up.

Primary bodies must be read before H1--H4 status is promoted. Until then the
manuscript wording remains conditional.

## 6. `traceability/CLAIM_BOUNDARY.md` required contents

Start with four bins.

### Formalism used, no firstness claim

- response quotient / exact interface;
- grammar monotonicity;
- codebook lower bound;
- closed/open inequality.

### Classical ancestry explicitly acknowledged

- contextual/input-restricted minimization;
- incomplete-machine reduction;
- state-reduction/realization noncommutation;
- fixed/uniform modular synthesis;
- common-refinement/state-complexity substrate.

### Conditional contribution candidate

> An explicit family simultaneously attains the maximum one-action open-response
> innovation while retaining fixed controls, bounded local state/connectivity,
> pairwise radius-one dynamics, and logarithmic access.

### Fallback if #122 subsumes the relay

> The relay is retained as a clean extremal realization and ecological explanatory
> model; historical novelty is not claimed. Future mathematics moves to a genuine
> converse/necessity result, coupled resource tradeoff, stochastic/approximate
> portability, or ecological structural theorem.

## 7. Related-work neighborhoods

The manuscript must distinguish at least:

1. Myhill--Nerode/transducer/bisimulation/state abstraction;
2. Kim--Newborn and interacting-FSM input-don't-care/context minimization;
3. promise/incomplete-domain descriptional complexity;
4. Hartmanis--Stearns style reduction/realization noncommutation;
5. uniform modular sequential-machine synthesis and bounded-fanout/fixed-module
   lines;
6. incomplete/nondeterministic modular decomposition, including Drilman--Weiner and
   Williams;
7. modern compositional/causal abstraction.

The Larrauri--Bloem “exponential improvement” must not be misdescribed: in tail
minimization it is an algorithmic/representation improvement over the classical
route; their exponential minimum solution-size result belongs to the distinct tail
synthesis problem.

## 8. Proof and replay contract

The manuscript must independently prove:

1. exact response-equivalence definition;
2. pair-separation injection for the codebook theorem;
3. closed/open gap using closed **upper bounds**;
4. maximal one-action innovation in the explicit family;
5. relay locality/control/latency properties;
6. conservative portability factorization.

Python replay is provenance and finite-witness verification only. It is not the
analytic proof and does not validate an observed ecosystem.

At transfer time pin:

- exact CCOC `main` SHA;
- theorem-registry version;
- exact successful paper-core replay SHA/run/artifact;
- issue #122 status;
- the precise allowed novelty wording at that date.

Never write “latest” without a SHA.

## 9. Figure contract

Use at most four primary figures:

1. same plant, restricted versus open legal future grammars;
2. maximal one-action response innovation;
3. degree-three bounded-local relay and access path;
4. conservative portability versus a fiber split.

The ecology panel should be an interpretation of the formal contract, not empirical
validation.

## 10. Migration sequence

1. create `rach-open-composition-paper` manually;
2. re-read CCOC `main` and pin its SHA;
3. re-check #122 and all recovered primary compiler texts;
4. populate traceability files before Introduction/Discussion;
5. create a compile-minimal LaTeX skeleton;
6. draft theorem statements and analytic proofs;
7. write Related Work with page-level primary-source checks;
8. only then write ecological framing, abstract, figures, cover letter, and reviewer
   candidates.

## 11. Definition of done for bootstrap

The manuscript workspace is ready for substantive drafting when:

- the repository exists and is writable;
- exact CCOC theorem/replay pins are recorded;
- `CLAIM_BOUNDARY.md` reflects the conditional extremal/local novelty decision;
- a minimal LaTeX skeleton compiles;
- no theorem code has been copied into the paper repository;
- #122 status is visible in traceability;
- theorem-first section order is fixed.
