# Supplement — proof and reproducibility spine

This supplement is the manuscript-facing proof surface for *Causal Compression under Open Composition*. It is deliberately narrower than the theorem archive. Every result below maps to one current CORE item and one analytic source. Executable certificates are reproducibility support, not substitutes for proofs.

## S1. Definitions and exact response interface

Let a finite deterministic controlled system be

\[
\mathcal M=(S,A,T,h)
\]

with finite state set \(S\), primitive action alphabet \(A\), transition map \(T\), and focal output \(h\). A declared legal future grammar \(\mathcal L\subseteq A^*\) determines the admissible future words.

For \(s\in S\) and \(w\in\mathcal L\), write \(\operatorname{Tr}(s,w)\) for the focal output trace under \(w\). Define

\[
s\equiv_{\mathcal L}t
\iff
\forall w\in\mathcal L,
\operatorname{Tr}(s,w)=\operatorname{Tr}(t,w).
\]

The quotient \(Q_{\mathcal L}=S/\!\equiv_{\mathcal L}\) is the canonical exact response interface, with memory

\[
K_{\mathcal L}=\log_2|Q_{\mathcal L}|.
\]

**CORE mapping:** CORE-1.

**Analytic source:** `docs/dynamic_boundary_blankets.md`.

**Executable support:** `causal_model/dynamic_boundary_blankets.py`, `causal_model/grammar_aware_blankets.py`, `causal_model/shared_grammar.py`.

**Non-claim:** fixed-grammar minimization is mathematical substrate, not the paper's novelty claim.

---

## S2. Cross-grammar addressability lower bound

### Theorem S1 — operational addressability lower bound

Suppose a reachable comparison subsystem is

\[
S^*\cong I\times E_1\times\cdots\times E_q.
\]

Assume one legal open future word decodes \(I\), and for every \(j\) another legal open word decodes \(E_j\), independently of the other coordinates. Then every distinct pair of comparison states is separated by a legal open future trace. Therefore

\[
K_{\mathrm{open}}
\ge
\log_2|I|+
\sum_{j=1}^q\log_2|E_j|.
\]

If closed context \(j\) factors exactly through \((I,E_j)\), then

\[
K_{\mathrm{closed},j}
\le
\log_2|I|+\log_2|E_j|,
\]

so

\[
K_{\mathrm{open}}-
\max_jK_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-
\max_j\log_2|E_j|.
\]

### Proof

Take two distinct states in \(S^*\). If their inside coordinates differ, the inside decoder separates them. Otherwise some exterior coordinate differs, and the corresponding exterior decoder separates them. Thus every pair lies in different exact open response classes, so the open quotient is discrete on the comparison subsystem. The closed upper bound follows from the assumed factorization. Subtracting the largest closed bound gives the stated inequality. \(\square\)

**CORE mapping:** CORE-2.

**Analytic sources:** `docs/extension_compression_noncommutation.md`, `docs/portability_core_v1.md`.

**Executable support:** `causal_model/extension_compression_noncommutation.py`.

**Non-claim:** the distinguishability/cardinality step is Myhill–Nerode-style substrate.

---

## S3. Constrained codebooks

The Cartesian product premise is stronger than required. Let \(C\) be any finite jointly realizable codebook inside the comparison domain. If the declared legal open future family separates every distinct pair of codewords, the exact open quotient is discrete on \(C\), hence

\[
|Q_{\mathrm{open}}|\ge |C|.
\]

If each closed context factors through a smaller projection \(\pi_j(C)\), then

\[
K_{\mathrm{open}}-
\max_jK_{\mathrm{closed},j}
\ge
\log_2|C|-
\max_j\log_2|\pi_j(C)|.
\]

This is retained as robustness of the premise, not a separate headline theorem.

**Analytic source:** `docs/addressable_codebook_bound.md`.

**Executable support:** `causal_model/addressable_codebooks.py` and retained codebook-family tests.

---

## S4. Fixed-regular extremal family

### Theorem S2 — maximal one-action open-response inflation

For every integer \(m\ge1\), there exists a finite deterministic synchronous controlled network with comparison domain

\[
D_m=\{0,1\}^{m+1}
\]

and fixed primitive action alphabet

\[
A=\{0,1,\mathsf{fire},\mathsf{tick}\}
\]

such that:

1. the closed grammar is \(L_C=\{0,1,\mathsf{tick}\}^*\);
2. the open grammar is \(L_O=A^*\), so opening adds only `fire`;
3. \(|P_C|=2\) and \(K_C=1\);
4. \(|P_O|=2^{m+1}\) and \(K_O=m+1\);
5. therefore \(K_O-K_C=m\), the absolute finite-domain maximum;
6. the interaction graph is a tree of maximum degree at most three with a one-edge focal/exterior cut and local alphabets bounded independently of \(m\);
7. the worst canonical query length is

\[
2\lceil\log_2m\rceil+2.
\]

### Proof spine

**Closed invariant.** Under `0`, `1`, and `tick`, no memory leaf emits a pulse. The focal output therefore remains equal to \(y\), so closed traces depend only on the focal bit. This yields exactly two closed response classes.

**Open addressability.** Let leaf \(j\) have address \(a_j\) and depth \(d_j\). The legal word

\[
a_j\,\mathsf{fire}\,\mathsf{tick}^{d_j+1}
\]

returns the stored bit \(b_j\) to the focal output. Hence every exterior coordinate is individually future-readable.

**Discrete open quotient.** Distinct focal bits are separated immediately; states with equal focal bit but different exterior memory are separated by the query for a differing leaf. Therefore every state in \(D_m\) occupies its own open response class.

**Sharpness.** A two-class closed quotient on a domain of size \(2^{m+1}\) can gain at most \(m\) bits before becoming discrete, and the construction attains that value.

**Locality.** The relay is a balanced binary tree. Address and pulse propagation use fixed radius-one local rules, bounded local alphabets, and degree at most three. The deepest leaf has depth \(\lceil\log_2m\rceil\), giving the query-length formula.

**CORE mapping:** CORE-3.

**Analytic source:** `docs/fixed_regular_extremal_theorem_2026-08-13.md`.

**Executable support:** `certify_fixed_regular_extremal_theorem(m)` in the current extremal open-composition implementation.

**Non-claim:** the paper does not claim historical firstness for bounded-local compilation or modular sequential-machine synthesis.

---

## S5. Positive portability boundary

### Theorem S3 — coherent portable macro-law

Consider nested finite grammar-aware systems with embeddings between stages. Suppose every stage maps to one common finite macrostate set \(Q\), has the same macro output and macro transition semantics, and embeddings preserve the macro label of every old state. Then all finite stages are compatible restrictions of one exact portable macro-law.

### Proof

At each stage the projection is an exact dynamic interface to the same macro system. Embedding coherence preserves the macro label of every earlier state. By induction, every earlier legal trajectory has the same macro trace in all later stages. The compatible finite-stage laws therefore define one common portable law on the nested union. \(\square\)

**CORE mapping:** CORE-4.

**Analytic sources:** `docs/coherent_portable_macrolaw.md`, `docs/conservative_macro_schema.md`.

---

## S6. Forced-split obstruction

### Proposition S4 — newly legal future word invalidates a merge

If two states lie in one proposed macro fiber but, after extension, a newly legal word yields distinct required focal traces from their embedded images, then that proposed merge cannot be exact for the extended grammar.

### Proof

One deterministic quotient state cannot simultaneously produce two distinct required response traces under the same legal word. Therefore the two states must lie in different exact extended response classes. \(\square\)

**CORE mapping:** CORE-5.

**Analytic source:** CORE-4 portability documents and theorem-spine statement.

---

## S7. Theorem-to-source traceability

| Manuscript result | CORE | Analytic proof source | Executable/replay role |
|---|---|---|---|
| Exact grammar-aware interface | CORE-1 | `docs/dynamic_boundary_blankets.md` | quotient/certificate regression |
| Cross-grammar lower bound | CORE-2 | `docs/extension_compression_noncommutation.md`; `docs/portability_core_v1.md` | finite injection certificate |
| Constrained codebook robustness | supporting | `docs/addressable_codebook_bound.md` | finite codebook checks |
| Fixed-regular extremal family | CORE-3 | `docs/fixed_regular_extremal_theorem_2026-08-13.md` | finite supplied-\(m\) certificate |
| Positive portability | CORE-4 | `docs/coherent_portable_macrolaw.md`; `docs/conservative_macro_schema.md` | finite compatibility witnesses |
| Forced split | CORE-5 | CORE-4 docs + `docs/theorem_spine.md` | explicit local counter-witness |

The current theorem registry and claim-status audit remain the machine-readable and human claim-control inventories. Removed historical branches are not manuscript dependencies.

---

## S8. Reproducibility contract

The latest validated theorem-code surface is the theorem-code merge recorded in `manuscript/PROVENANCE.md` and `docs/paper_core_replay_pin.md`. The validated PR head passed theorem-registry integrity, grammar-interface replay, paper-core replay, and the Python 3.10/3.11/3.12 test matrix.

Before submission, run on the final immutable submission commit:

```bash
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
pytest -q
```

Then record the exact commit SHA and preserve the generated machine-readable reports with the submission/release materials.

A successful replay verifies finite certificates, regressions, and provenance. It does not replace the analytic proofs above, establish empirical ecological validity, or establish historical priority.
