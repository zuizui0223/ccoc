# RACH claim-status audit

This document is the canonical scope audit for public RACH claims. It does not
add mathematics. Its job is to stop a valid finite result from being narrated as
a broader classification than its hypotheses support.

## Status vocabulary

| Status | Meaning |
|---|---|
| **Exact finite theorem** | Necessary-and-sufficient or exact statement on the explicitly declared finite domain and grammar. |
| **Sufficient criterion** | Gives portability, boundedness, or factorization when its premises are supplied; no converse is claimed. |
| **Lower-bound obstruction** | A supplied operational separation premise forces a minimum interface size or refutes a proposed merge. |
| **Sharpness witness** | One family attaining a bound; it does not classify all families. |
| **No-go theorem** | A quantified impossibility within a stated model/evidence class. |
| **UNRESOLVED boundary** | The current theory intentionally makes no classification. |

## A. Portability core v1

### A0. Finite closure classification

- **Status:** Exact finite theorem.
- **Module:** `causal_closure_calculus.py`.
- **Claim:** A declared finite deterministic update map is classified by exact
  certificates into global closure, recurrence, or multistability.
- **Domain:** Finite total deterministic state map.
- **Do not claim:** Local update rules of real ecosystems imply one global
  endpoint, or that this decides boundary portability.

### A1. Exact grammar-aware dynamic interface

- **Status:** Exact finite theorem for the declared controlled system and legal
  grammar.
- **Modules:** `dynamic_boundary_blankets.py`, `grammar_aware_blankets.py`.
- **Claim:** The legal-word quotient on system state × declared grammar state is
  the coarsest exact interface preserving output, enabled actions, and legal
  successor summaries.
- **Domain:** Finite deterministic controlled system with a fixed finite grammar.
- **Do not claim:** The declared grammar is automatically the biologically
  correct intervention grammar, or that grammar state is itself a biological
  variable.

### A2. Addressable-completion product bound

- **Status:** Lower-bound obstruction.
- **Modules:** `addressable_completion_bounds.py`,
  `extension_compression_noncommutation.py`.
- **Claim:** If a jointly realizable product subsystem

  \[
  I\times E_1\times\cdots\times E_q
  \]

  has a concrete legal decoder for the inside coordinate and each exterior
  coordinate, every open-safe exact interface has at least

  \[
  \log_2|I|+\sum_j\log_2|E_j|
  \]

  bits on that subsystem.
- **Domain:** Supplied product realization and operational decoder words.
- **Do not claim:** Every growing ecosystem contains such an independent product,
  or that exterior memory adds without the stated joint-separation premise.

### A3. Extension--compression noncommutation inequality

- **Status:** Lower-bound corollary under closed-context factorization.
- **Module:** `extension_compression_noncommutation.py`.
- **Claim:** If each fixed closed context factors through \((I,E_j)\), then

  \[
  K_{\mathrm{open}}-\max_jK_{\mathrm{closed},j}
  \ge
  \sum_j\log_2|E_j|-\max_j\log_2|E_j|.
  \]
- **Domain:** A2 plus the stated closed-context factorization.
- **Do not claim:** Every closed-context compression and every open composition
  fail to commute. The theorem gives a certified obstruction family, not a
  universal dichotomy.

### A4. Binary relay realization

- **Status:** Sharpness witness.
- **Modules:** `extension_compression.py`, `relay_tree_compilation.py`,
  `extension_compression_noncommutation.py`.
- **Claim:** For binary modules, equality is attained with constant local grammar,
  pairwise messages, and degree at most three.
- **Domain:** The declared relay-tree family.
- **Do not claim:** Every ecological network has relay-tree dynamics, or that
  bounded degree alone implies a memory gap.

### A5. Composition portability ladder

- **Status:** Three nested sufficient criteria.
- **Modules:** `compositional_boundedness.py`,
  `coherent_portable_macrolaw.py`, `conservative_macro_schema.py`.

| Level | Premise | Valid conclusion |
|---|---|---|
| Boundedness | every stage factors through one finite summary alphabet | a uniform finite interface-size upper bound |
| Coherent portability | common macro output/legal-action/transition system and label-coherent embeddings | one exact macro-law across the nested stages |
| Conservative extension | monotone legal rows in one fixed finite action alphabet; old macro meanings fixed; new actions label-deterministic | one exact finite macro schema on the union grammar |

- **Do not claim:** These are necessary conditions for all possible portable laws,
  or that a family lacking the supplied factorization must grow.

### A6. Future-word and new-action obstructions

- **Status:** Lower-bound/local obstruction.
- **Modules:** `coherent_portable_macrolaw.py`,
  `conservative_macro_schema.py`.
- **Claim:** A later legal word or newly legal action that separates two states in
  one proposed macro fiber invalidates that proposed merge.
- **Domain:** The named pair, declared embedding, target grammar, and supplied
  word/action.
- **Do not claim:** One obstruction proves the absence of every alternative
  coarser or differently structured macro-law.

## B. Identifiability companion

### B1. Delayed exposure and adaptive finite-evidence no-go

- **Status:** No-go theorem.
- **Modules:** `delayed_addressability.py`, `adaptive_closure_no_go.py`.
- **Claim:** For every finite-depth adaptive policy over the fixed declared action
  alphabet, a delay-gated closed/open pair can agree on its entire transcript and
  separate later. Therefore finite transcript-only evidence cannot uniformly
  certify exterior closure across the unbounded delayed family.
- **Domain:** The specified finite-policy class and delay-gated comparator family.
- **Do not claim:** No finite experiment can ever certify closure. Certification
  becomes possible when an independently justified finite horizon, grammar, and
  completion contract are supplied.

### B2. Candidate universal-law criterion

- **Status:** Exact finite theorem for a retained candidate family with supplied
  induced macro maps.
- **Module:** `candidate_safe_laws.py`.
- **Claim:** A universal deterministic macro law exists exactly when all retained
  candidate induced maps agree on every declared action.
- **Domain:** Fixed candidate family and validated candidate-level interfaces.
- **Do not claim:** Candidate uncertainty is identical to composition growth, or
  that candidate and exterior memory can be added without joint realization.

### B3. Joint exterior--mechanism bound

- **Status:** Lower-bound obstruction under explicit joint structural separation.
- **Module:** `joint_open_candidate_laws.py`.
- **Claim:** Joint exterior and response-type memory is forced only when the joint
  product is realizable and concrete legal words separate unequal joint states.
- **Do not claim:** Separate exterior and candidate lower bounds automatically
  add in arbitrary model families.

## C. Experimental-design legacy

- **Status:** Conditional derived design theorems, frozen for new feature work.
- **Modules:** reset panels, witnessed evidence, robustness panels,
  common-mode failures, observation-regime special cases.
- **Valid use:** Optimize or protect a measurement/design protocol after the
  relevant quotient, reset, coverage, and failure contracts have been fixed.
- **Do not claim:** These establish closure, portability, or an ecological
  ontology by themselves.

## D. Explicit unresolved region

The repository currently does **not** classify all composition families.

A family is `UNRESOLVED` when neither of the following has been supplied:

1. a finite update-consistent factorization establishing a portability upper
   criterion; or
2. a jointly realizable, independently decoded product establishing an
   addressability lower obstruction.

Likewise, action-alphabet expansion, non-nested rewiring/replacement, and noisy
approximate portability remain future choices, not currently implied corollaries.

## Review rule for future claims

A new public theorem statement must name exactly one status above and include:

1. finite domain and legal grammar;
2. its additional premise;
3. its valid conclusion; and
4. at least one sentence beginning **“Do not claim:”**.

A result without a changed canonical claim belongs in an example, limitation, or
legacy regression rather than a new theorem branch.
