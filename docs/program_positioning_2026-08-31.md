# CCOC program positioning and naming boundary — 2026-08-31

## Status

This document is the normative current-facing statement of what CCOC is, what it is not, and how historical RACH ancestry should be represented.

## 1. One-sentence identity

**CCOC is a representation theory for exact response interfaces under changing legal future grammars.**

Its primary question is:

> For a fully declared finite controlled system, which state distinctions must an exact interface retain, and how can that requirement increase when previously illegal future actions become legal?

The central mathematical object is the grammar-relative response quotient

\[
Q_{\mathcal L}=S/\!\equiv_{\mathcal L},
\qquad
K_{\mathcal L}=\log_2|Q_{\mathcal L}|.
\]

The first-paper claim is a cross-grammar representation lower bound, together with a bounded-local extremal realization and a positive portability boundary.

## 2. What CCOC is not

CCOC is not an epistemic uncertainty measure and not an observation-selection method. It does not ask which causal mechanism is true, assign uncertainty to competing mechanisms, or choose the next measurement.

CCOC is also not a latent-channel identification paper. It does not infer a decomposition such as `W=FE` from net observations, estimate proxy transport, or return an identified set or calibration-breakdown factor.

Those tasks may use related words such as quotient, boundary, exactness, contract, or information, but their estimands differ.

## 3. Separation from RACH (microdonta)

RACH owns the inferential pipeline

```text
declared candidate family + evidence
-> admissible region A_epsilon
-> residual mechanism uncertainty
-> NOV / RACH-SEQ
-> next observation
```

Its information quantity

\[
D_{\mathrm{RACH}}=H(S\mid A_\epsilon)
\]

is epistemic: it describes uncertainty about mechanism identity after conditioning on evidence. A verified candidate observation can reduce this uncertainty in expectation through

\[
NOV(Q)=I(S;Q\mid A_\epsilon)/K.
\]

CCOC instead takes the controlled system and future grammar as declared. Its lower bound concerns how much exact response state must be represented. Adding data is not an operation in the theorem that reduces `K_L`; changing the declared future grammar is.

Therefore the clean contrast is:

> **RACH asks what we still do not know. CCOC asks what an exact interface must still remember even when the system is fully specified.**

## 4. Separation from the N1–N4 channel-identification boundary

The N1–N4 programme is an identification theory for multiplicative latent channels. N1 uses the reciprocal action

```text
(F,E) -> (cF,E/c)
```

under which `W=FE` and every net-only observable `Phi(W)` remain invariant. Finite proxy-transport bounds then yield partial identification and breakdown factors; direct calibration can restore point identification.

This is closer to CCOC than RACH in structural style because both expose an obstruction that richer-looking surface information does not automatically remove. The obstruction is nevertheless different:

- **CCOC:** legal future words separate concrete states and force a large exact response quotient;
- **N1:** a group action preserves all net-only observations and prevents latent channel identification.

Accordingly, it is safe to describe them as related structural-obstruction arguments, but not as the same theorem or the same proof technique.

## 5. Portfolio relation

| Programme | Unknown or fixed object | Operation | Output | Type |
|---|---|---|---|---|
| CCOC | controlled system treated as declared | enlarge/restrict legal future grammar | exact-interface size / lower bound | representation |
| RACH | mechanism identity uncertain | acquire and condition on observations | residual entropy / next-observation value | inference and design |
| N1–N4 boundary | latent channel allocation uncertain | change observation/calibration assumptions | identified set / breakdown factor | identification |

The three papers should remain separate. No theorem should be counted as a primary contribution in more than one programme.

## 6. Citation policy

The CCOC first paper is self-contained and does not require the RACH or N1–N4 papers as theorem dependencies.

A future boundary paper may cite CCOC as a related representation-side structural obstruction, provided it states the distinction explicitly. The recommended relation is one-way and conceptual:

```text
CCOC: opening legal futures can reveal distinctions an exact representation must retain.
N1: enriching observations within a net-only invariant class still cannot reveal latent channel allocation.
```

CCOC itself need not cite the boundary paper merely to establish this portfolio relation.

## 7. Naming rule

Current-facing repository surfaces must use **CCOC** for this repository and theorem programme.

Use CCOC in:

- README and manuscript workspace documentation;
- package/distribution metadata;
- current API examples and aliases;
- nonempirical-scope and contribution-boundary documentation;
- submission and release materials.

Historical recovery documents may retain `RACH`, `RACH/CCOC`, or similar wording only when describing the actual ancestry of the repository. Such occurrences are provenance, not current identity, and must not be blindly replaced.

The current Python import package remains `causal_model` for compatibility. Examples should use a CCOC-facing alias such as

```python
import causal_model.portability_core as ccoc
```

rather than `as rach`.

## 8. Manuscript-facing claim firewall

The CCOC manuscript may claim:

1. exact response equivalence is contract-relative to a legal future grammar;
2. grammar enlargement refines the exact response relation;
3. independently future-addressable coordinates force retained interface information;
4. one newly legal primitive action can produce maximal finite-domain response-memory inflation in the explicit family;
5. the separation survives bounded local alphabets, bounded degree, narrow physical cut, and logarithmic access;
6. a coherent common macro-law gives a positive portability condition.

It should not claim:

- that observations identify the correct ecological mechanism;
- that CCOC reduces causal uncertainty;
- that `K_L` is posterior entropy or residual epistemic uncertainty;
- that N1–N4 channel non-identification is a CCOC theorem;
- that generic quotient minimization, Myhill–Nerode distinguishability, or bounded-local compilation is historically new in isolation.

## 9. Development rule

When a proposed addition is mainly about acquiring evidence, reducing uncertainty, proxy calibration, latent-channel identification, or empirical mechanism claims, route it out of CCOC. CCOC development should remain centered on exact representation under a declared future contract and on mathematically distinct strengthenings of that problem.
