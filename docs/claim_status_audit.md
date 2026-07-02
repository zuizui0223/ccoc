# RACH claim-status audit

This is the canonical scope audit. Its purpose is to prevent a valid finite
certificate from being narrated as a classification of arbitrary ecosystems.

## Status vocabulary

| Status | Meaning |
|---|---|
| **Exact finite theorem** | Exact statement on the declared finite domain and grammar. |
| **Sufficient criterion** | Gives the conclusion when its additional premises are supplied; no converse. |
| **Lower-bound obstruction** | Operational separation forces memory or refutes a specified merge. |
| **Sharpness witness** | One family attains a bound; it does not classify all families. |
| **No-go theorem** | Quantified impossibility in a stated model/evidence class. |
| **`UNRESOLVED`** | The theory deliberately does not classify the case. |

## A. Portability core v1

### A0. Finite closure classification

- **Status:** Exact finite theorem.
- **Module:** `causal_closure_calculus.py`.
- **Claim:** A finite total deterministic update map is certified as globally
  closing, recurrent, or multistable.
- **Domain:** Declared finite deterministic state map.
- **Do not claim:** Local rules of real ecosystems imply one endpoint or decide
  boundary portability.

### A1. Exact grammar-aware dynamic interface

- **Status:** Exact finite theorem.
- **Modules:** `dynamic_boundary_blankets.py`, `grammar_aware_blankets.py`.
- **Claim:** The legal-word quotient on system state × grammar state is the
  coarsest exact interface preserving output, enabled actions, and legal
  successors.
- **Domain:** Finite deterministic controlled system with a fixed finite grammar.
- **Do not claim:** The supplied grammar is automatically biologically correct.

### A2. Addressable-completion product bound

- **Status:** Lower-bound obstruction.
- **Modules:** `addressable_completion_bounds.py`,
  `extension_compression_noncommutation.py`.
- **Claim:** A jointly realizable product subsystem

  \[
  I\times E_1\times\cdots\times E_q
  \]

  with legal decoders for the inside coordinate and every exterior coordinate
  forces at least

  \[
  K_{\mathrm{open}}\ge \log_2|I|+\sum_j\log_2|E_j|.
  \]

- **Domain:** Supplied product realization and concrete decoder words.
- **Do not claim:** Exterior memory adds in every growing composition without the
  joint-realizability and separation premise.

### A3. Extension--compression noncommutation

- **Status:** Lower-bound corollary under closed-context factorization.
- **Module:** `extension_compression_noncommutation.py`.
- **Claim:** If fixed context \(j\) factors through \((I,E_j)\), then

  \[
  K_{\mathrm{open}}-\max_jK_{\mathrm{closed},j}
  \ge
  \sum_j\log_2|E_j|-\max_j\log_2|E_j|.
  \]

- **Do not claim:** Every closed-context compression fails to commute with every
  open composition.

### A4. Binary relay realization

- **Status:** Sharpness witness.
- **Modules:** `extension_compression.py`, `relay_tree_compilation.py`.
- **Claim:** The binary equality case is attained with constant local grammar,
  pairwise messages, and maximum degree three.
- **Do not claim:** Bounded degree alone implies a memory gap.

### A5. Nested composition portability ladder

- **Status:** Nested sufficient criteria.
- **Modules:** `compositional_boundedness.py`,
  `coherent_portable_macrolaw.py`, `conservative_macro_schema.py`.

| Level | Valid conclusion |
|---|---|
| Boundedness | A common finite summary alphabet gives a uniform interface-size upper bound. |
| Coherent portability | Common macro output/action/transition dynamics plus label-coherent embeddings give one law across nested stages. |
| Conservative extension | Monotone legal rows, fixed old meanings, and label-deterministic new actions give one finite schema on the union grammar. |

- **Do not claim:** These are necessary conditions for every portable law.

### A6. Future-word and new-action obstructions

- **Status:** Local lower-bound obstruction.
- **Modules:** `coherent_portable_macrolaw.py`, `conservative_macro_schema.py`.
- **Claim:** A later legal word or new action separating two states in one proposed
  macro fiber invalidates that proposed merge.
- **Do not claim:** One split rules out every possible alternative macro-law.

## B. Selected post-v1 structural extension

### B1. Non-nested replacement transport

- **Status:** Sufficient finite-domain transport-coherence criterion.
- **Module:** `non_nested_portability.py`.
- **Claim:** A connected declared replacement graph shares one exact macro law
  when every stage already has the same exact macro dynamics and every edge
  supplies a total, output/legal-action/label-preserving, successor-closed
  transport relation. The transport may be many-to-one or one-to-many.
- **Witnesses:** A three-to-two many-to-one replacement and a four-to-three
  newly-legal-word rewiring obstruction.
- **Domain:** Declared finite grammar-aware controlled systems, a common finite
  macro dynamics, and explicit replacement transports.
- **Do not claim:** Transport failure proves cumulative addressability, unbounded
  memory, or the absence of every alternative macro-law.
- **Proof-strength note:** The current positive criterion assumes exact stage
  projections into the common macro law. Constructing a target projection from
  one source projection and a transport relation is an open strengthening, not
  part of the current theorem.

### B2. Non-nested newly-legal-word split

- **Status:** Local obstruction to one carried merge.
- **Module:** `non_nested_portability.py`.
- **Claim:** A word illegal before replacement and legal afterward, which separates
  two carried states in one proposed target fiber, refutes that fiber.
- **Do not claim:** The obstruction supplies a global memory-growth lower bound.

## C. Identifiability companion

### C1. Delayed exposure and adaptive finite-evidence no-go

- **Status:** No-go theorem.
- **Modules:** `delayed_addressability.py`, `adaptive_closure_no_go.py`.
- **Claim:** For every finite-depth adaptive policy, a delay-gated closed/open pair
  can agree on the transcript and separate later. Without an independent horizon
  and grammar contract, finite transcript-only evidence cannot uniformly certify
  closure over that family.
- **Do not claim:** No finite experiment can ever certify closure under a supplied
  finite horizon and completion contract.

### C2. Candidate universal-law criterion

- **Status:** Exact finite theorem for a retained candidate family.
- **Module:** `candidate_safe_laws.py`.
- **Claim:** A deterministic candidate-universal macro law exists exactly when all
  induced candidate maps agree on every declared action.
- **Do not claim:** Candidate uncertainty and composition growth are the same axis.

### C3. Joint exterior--mechanism bound

- **Status:** Lower-bound obstruction under explicit joint separation.
- **Module:** `joint_open_candidate_laws.py`.
- **Do not claim:** Separate exterior and candidate lower bounds add automatically.

## D. Experimental-design legacy

- **Status:** Conditional derived design theorems, frozen for new feature work.
- **Use:** Optimize or protect a protocol only after quotient, reset, coverage, and
  failure contracts are fixed.
- **Do not claim:** These modules establish closure or portability by themselves.

## E. Explicit unresolved region

A family remains `UNRESOLVED` when neither a finite update-consistent
factorization nor an independently decoded, jointly realizable addressability
product has been supplied. In particular, **unconstrained** non-nested
replacement/rewiring, stochasticity, approximate portability, and
composition-dependent candidate families are not implied by current results.

## Review rule

Every new public theorem statement must name one status above and state:

1. finite domain and legal grammar;
2. additional premise;
3. valid conclusion; and
4. a sentence beginning **“Do not claim:”**.
