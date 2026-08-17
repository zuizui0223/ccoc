# CCOC current theorem and proof spine — 2026-08-17

CCOC has one current publication spine. This document lists only the present CORE-1–CORE-5 proof dependencies. Historical non-nested replacement, mechanism-uncertainty, evidence-design, feedback, ecological special-case, and other removed branches are not part of the current CCOC theorem chain.

## 1. CORE-1 — canonical exact dynamic interface

For a declared finite deterministic controlled system and legal grammar, define two states as equivalent when every legal finite word gives the same output trace.

The canonical response quotient is the coarsest exact deterministic interface.

### Proof source

`docs/dynamic_boundary_blankets.md` proves:

1. finite counterfactual-horizon stabilization;
2. right-congruence / dynamic-interface completeness;
3. finite dynamic-blanket upper bounds; and
4. the uniform blanket obstruction when combined with addressability.

The executable implementations are `dynamic_boundary_blankets.py`, `grammar_aware_blankets.py`, and `shared_grammar.py`.

This is foundational substrate. The current novelty claim does not rest on generic fixed-grammar minimization.

---

## 2. CORE-2 — cross-grammar extension–compression lower bound

Let a declared comparison family contain a jointly realizable product

\[
I\times E_1\times\cdots\times E_q.
\]

If legal future words decode the inside coordinate and every exterior coordinate, then every two distinct product states are separated by a legal future trace. Therefore

\[
K_{\mathrm{open}}
\ge
\log_2|I|+\sum_j\log_2|E_j|.
\]

If closed context `j` admits a supplied exact factorization through `(I,E_j)`, then

\[
K_{\mathrm{closed},j}
\le
\log_2|I|+\log_2|E_j|,
\]

and hence

\[
\boxed{
K_{\mathrm{open}}-\max_jK_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-\max_j\log_2|E_j|.
}
\]

### Proof source

- `docs/extension_compression_noncommutation.md`
- `docs/portability_core_v1.md`
- executable injection certificate in `causal_model/extension_compression_noncommutation.py`.

The proof is an operational injection using declared decoder words, not an arithmetic assumption that independent memory contributions always add.

---

## 3. CORE-3 — bounded-local extremal sharpness

For every `m>=1`, the fixed-regular relay family has

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

under one fixed four-symbol primitive alphabet, with opening adding one primitive action, while the interaction graph remains a degree-at-most-three tree with one-edge focal/exterior cut and bounded local alphabets.

### Proof source

`docs/fixed_regular_extremal_theorem_2026-08-13.md` gives the all-`m` proof:

1. fixed grammar and total local dynamics;
2. closed all-word invariant;
3. legal addressability of every exterior coordinate;
4. discreteness of the open quotient;
5. exact capacity sharpness;
6. bounded locality and one-edge cut; and
7. exact logarithmic query length.

Executable `certify_fixed_regular_extremal_theorem(m)` checks one finite supplied `m`; it is not the quantified proof itself.

CORE-3 is sharpness support for CORE-2, not a second independent headline lower bound.

---

## 4. CORE-4 — positive conservative portability boundary

CCOC retains a positive boundary showing when a finite macro-law can remain exact across declared nested extension.

### Coherent portability

If every stage factors through one common finite macro dynamics and embeddings preserve macro labels, the stage laws are compatible restrictions of one portable law.

Proof: `docs/coherent_portable_macrolaw.md`.

### Conservative legal-action expansion

If legal action rows grow monotonically, old action meanings never change, and each newly legal action has one label-deterministic successor inside a macro fiber, the union grammar carries one finite conservative macro schema.

Proof: `docs/conservative_macro_schema.md`.

These are sufficient positive criteria. They are not the unique source-relative repair problem of MLTR.

---

## 5. CORE-5 — local future-word/new-action obstruction

If two states in one proposed macro fiber are separated by a later legal word or newly legal action, the proposed merge cannot be exact.

The proof is immediate from deterministic factorization: one quotient state cannot carry two distinct future traces or two different quotient successors under the same legal action.

Proof/witness sources are the CORE-4 documents and modules.

CORE-5 is a local warning. It does not by itself yield the global memory lower bound of CORE-2 or the unique coarsest inherited-law repair of MLTR.

---

## 6. Dependency graph

```text
CORE-1  canonical exact interface
   |
   +--> CORE-2  operational cross-grammar lower bound  [headline]
   |        |
   |        +--> CORE-3  bounded-local equality/sharpness witness
   |
   +--> CORE-4  positive sufficient portability boundary
            |
            +--> CORE-5  concrete local obstruction when a proposed fiber is split
```

The first-paper story is therefore not a catalogue of quotient theorems. It is one structural contrast:

\[
\boxed{
\text{small exact interfaces in closed futures}
\not\Rightarrow
\text{one comparably small exact interface for an open future grammar},
}
\]

with a sharp bounded-local witness and a separate positive boundary showing when portability can hold.

---

## 7. Proof/replay rule

A quantified analytic theorem must have a written proof source. Finite certificates, tests, and replay artifacts are implementation guards and witnesses; they do not replace the quantified proof.

The executable registry `docs/theorem_registry.json` remains the current machine-readable inventory. `docs/claim_status_audit.md` records the current proof status and non-claims. Historical theorem truth remains available through Git history and the historical archive, not through this current proof spine.
