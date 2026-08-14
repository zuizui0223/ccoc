# RACH claim-status audit

This is the canonical scope audit. Its purpose is to prevent a valid finite certificate from being narrated as a classification of arbitrary ecosystems.

## Status vocabulary

| Status | Meaning |
|---|---|
| **Exact finite theorem** | Exact statement on the declared finite domain and grammar. |
| **Sufficient criterion** | Gives the conclusion when its additional premises are supplied; no converse. |
| **Lower-bound obstruction** | Operational separation forces memory or refutes a specified merge. |
| **Sharpness witness** | One family attains a bound; it does not classify all families. |
| **No-go theorem** | Quantified impossibility in a stated model/evidence class. |
| **`UNRESOLVED`** | The theory deliberately does not classify the case. |
| **Open candidate** | Finite benchmark/question exists but has not been promoted to a public theorem. |

## A. Portability core v1

### A0. Finite closure classification

- **Status:** Exact finite theorem.
- **Module:** `causal_closure_calculus.py`.
- **Claim:** A finite total deterministic update map is certified as globally closing, recurrent, or multistable.
- **Domain:** Declared finite deterministic state map.
- **Do not claim:** Local rules of real ecosystems imply one endpoint or decide boundary portability.

### A1. Exact grammar-aware dynamic interface

- **Status:** Exact finite theorem.
- **Modules:** `dynamic_boundary_blankets.py`, `grammar_aware_blankets.py`.
- **Claim:** The legal-word quotient on system state × grammar state is the coarsest exact interface preserving output, enabled actions, and legal successors.
- **Domain:** Finite deterministic controlled system with a fixed finite grammar.
- **Do not claim:** The supplied grammar is automatically biologically correct.

### A2. Addressable-completion product bound

- **Status:** Lower-bound obstruction.
- **Modules:** `addressable_completion_bounds.py`, `extension_compression_noncommutation.py`.
- **Claim:** A jointly realizable product subsystem

  \[
  I\times E_1\times\cdots\times E_q
  \]

  with legal decoders for every coordinate forces

  \[
  K_{\mathrm{open}}\ge \log_2|I|+\sum_j\log_2|E_j|.
  \]

- **Domain:** Supplied product realization and concrete decoder words.
- **Do not claim:** Exterior memory adds in every growing composition without the joint-realizability and separation premise.

### A3. Extension--compression noncommutation

- **Status:** Lower-bound corollary under closed-context factorization.
- **Module:** `extension_compression_noncommutation.py`.
- **Claim:** If fixed context \(j\) factors through \((I,E_j)\), then

  \[
  K_{\mathrm{open}}-\max_jK_{\mathrm{closed},j}
  \ge
  \sum_j\log_2|E_j|-\max_j\log_2|E_j|.
  \]

- **Do not claim:** Every closed-context compression fails to commute with every open composition.

### A4. Binary relay realization

- **Status:** Sharpness witness.
- **Modules:** `extension_compression.py`, `relay_tree_compilation.py`.
- **Claim:** The binary equality case is attained with constant local grammar, pairwise messages, and maximum degree three.
- **Do not claim:** Bounded degree alone implies a memory gap.

### A5. Nested composition portability ladder

- **Status:** Nested sufficient criteria.
- **Modules:** `compositional_boundedness.py`, `coherent_portable_macrolaw.py`, `conservative_macro_schema.py`.

| Level | Valid conclusion |
|---|---|
| Boundedness | A common finite summary alphabet gives a uniform interface-size upper bound. |
| Coherent portability | Common macro output/action/transition dynamics plus label-coherent embeddings give one law across nested stages. |
| Conservative extension | Monotone legal rows, fixed old meanings, and label-deterministic new actions give one finite schema on the union grammar. |

- **Do not claim:** These are necessary conditions for every portable law.

### A6. Future-word and new-action obstructions

- **Status:** Local lower-bound obstruction.
- **Modules:** `coherent_portable_macrolaw.py`, `conservative_macro_schema.py`.
- **Claim:** A later legal word or new action separating two states in one proposed macro fiber invalidates that proposed merge.
- **Do not claim:** One split rules out every possible alternative macro-law.

## B. Selected post-v1 structural extension

### B1. Non-nested edge preservation with supplied projections

- **Status:** Sufficient finite-domain transport-coherence criterion.
- **Module:** `non_nested_portability.py`.
- **Claim:** A connected declared replacement graph shares one exact macro law when every stage already has the same exact macro dynamics and every edge supplies a total, output/legal-action/label-preserving, successor-closed transport relation. The transport may be many-to-one or one-to-many.
- **Witness:** A three-to-two many-to-one replacement.
- **Do not claim:** Edge preservation proves that a target interface can always be constructed without target-fiber label consistency.

### B2. Transported target exact factorization

- **Status:** Sufficient finite-domain theorem.
- **Module:** `non_nested_portability.py`.
- **Claim:** Given one exact source projection and a relation covering both finite product spaces, if related states preserve output and equal legal-action rows, the relation is successor-closed, and every target fiber receives one source label, then

  \[
  q_T(t)=q_S(s)\quad ((s,t)\in R)
  \]

  is well-defined, exact, and induces the same finite macro dynamics as \(q_S\).
- **Witness:** The target labels \((0,1)\) of a three-to-two many-to-one replacement are constructed without being supplied.
- **Do not claim:** This is a necessary characterization of all replacement portability, or a theorem for target-only legal actions, stochasticity, approximation, or data-inferred transports.

### B3. Conservative non-nested transport

- **Status:** Sufficient finite-domain theorem.
- **Module:** `non_nested_conservative_transport.py`.
- **Claim:** Given one exact source projection and a total target-fiber-label-consistent relation, if related states preserve output, all source-legal actions remain legal and successor-closed at the target, and every target-only action has uniform availability and uniform target macro successor within each derived target fiber, then the certificate constructs one conservative macro schema. The source realizes a restriction and the target realizes its expanded rows.
- **Witness:** A three-to-two many-to-one replacement with target-only `reveal`, deriving labels \((0,1)\) and schema rows \(((1,1),(0,1))\).
- **Do not claim:** This covers arbitrary new actions, actions whose availability differs within a target fiber, actions with different target successors within a target fiber, or data-inferred transports.

### B4. Non-nested newly-legal-word split

- **Status:** Local obstruction to one carried merge.
- **Module:** `non_nested_portability.py`.
- **Claim:** A word illegal before replacement and legal afterward, which separates two carried states in one proposed target fiber, refutes that fiber.
- **Do not claim:** The obstruction supplies a global memory-growth lower bound.

## C. Identifiability companion

### C1. Delayed exposure and adaptive finite-evidence no-go

- **Status:** No-go theorem.
- **Modules:** `delayed_addressability.py`, `adaptive_closure_no_go.py`.
- **Claim:** For every finite-depth adaptive policy, a delay-gated closed/open pair can agree on the transcript and separate later. Without an independent horizon and grammar contract, finite transcript-only evidence cannot uniformly certify closure over that family.
- **Do not claim:** No finite experiment can ever certify closure under a supplied finite horizon and completion contract.

### C2. Candidate universal-law criterion

- **Status:** Exact finite theorem for a retained candidate family.
- **Module:** `candidate_safe_laws.py`.
- **Claim:** A deterministic candidate-universal macro law exists exactly when all induced candidate maps agree on every declared action.
- **Do not claim:** Candidate uncertainty and composition growth are the same axis.

### C3. Joint exterior--mechanism bound

- **Status:** Lower-bound obstruction under explicit joint separation.
- **Module:** `joint_open_candidate_laws.py`.
- **Do not claim:** Separate exterior and candidate lower bounds add automatically.

## D. Experimental-design legacy

- **Status:** Conditional derived design theorems, frozen for new feature work.
- **Use:** Optimize or protect a protocol only after quotient, reset, coverage, and failure contracts are fixed.
- **Do not claim:** These modules establish closure or portability by themselves.

## E. Post-reopening exact converse and resource results

The July registry IDs remain frozen provenance anchors; the following August results are explicit theorem surfaces rather than retroactive registry rewrites.

### E1. Grammar expansion versus arbitrary grammar mutation

- **One-state action expansion:** exact stable-refinement converse (`action_grammar_closure.py`).
- **Globally-new-symbol multi-state expansion:** exact refinement/converse with frozen old action columns (`grammar_expansion_closure.py`).
- **Arbitrary same-domain grammar mutation:** quotient relation may be equal, finer, coarser, or incomparable; reuse of the closed labeling has its own exact row-descent criterion (`grammar_interface_reuse.py`).
- **Permanent correction:** the broad PR #162 monotonicity claim is false.

### E2. Fixed-regular extremal family

- **Status:** Sharpness / extremal construction.
- **Modules:** `fixed_regular_grammar_relay.py`, `extremal_open_composition.py`.
- **Claim:** For every `m>=1`, one fixed four-symbol setup and one newly legal primitive action have `|P_C|=2`, `|P_O|=2^(m+1)`, exact innovation `m`, degree at most three, cut one, and bounded local alphabets.
- **Do not claim:** All bounded-local networks exhibit this inflation.

### E3. Chain/resource portability

- **Status:** Exact/quantitative theorems under declared resource models.
- **Modules/docs:** `terminal_grammar_portability.py`, `portability_adaptation_tradeoff.py`, retention-boundary-time and staged-prefix results.
- **Claim:** terminal memory, retained/update information, full-interface installation time, selected-query latency, and stage deadlines are distinct resources with proved inequalities/iff criteria in the stated subclasses.
- **Do not claim:** The information-theoretic/scheduling substrate itself is new or that a single-trajectory cut bound applies automatically to counterfactual query families.

## F. Post-reopening ecological/stochastic/spatial results

### F1. Deterministic saturation and capacity portability

- **Status:** Exact finite/changing-domain theorems in the declared guild model.
- **Modules:** `ecological_saturation_blanket.py`, `ecological_capacity_portability.py`, `budgeted_depletion_blanket.py`.
- **Claim:** non-negative colonization makes `Z_g=min(L_g,N_g)` exact; changing capacity domains can share one macro law; a remaining one-unit downward-reach budget `D` raises the exact cap to `L+D`.
- **Do not claim:** Thresholding alone is exact when legal future dynamics can return hidden oversaturation to the response-sensitive region beyond the declared budget.

### F2. Stochastic exact and finite-horizon approximate saturation

- **Status:** Exact controlled-Markov theorem plus model-specific approximate portability theorems.
- **Modules:** `stochastic_ecological_portability.py`, `continuous_time_depletion_reach.py`, `per_capita_mortality_reach.py`, `finite_horizon_stochastic_saturation.py`.
- **Claim:** `Q_a(D|Z)` gives exact stochastic saturation portability; positive downward probability/rate can restore all exact abundance classes; nevertheless a fixed `L+1`-state macro has capacity-independent finite-horizon TV bounds in the declared depletion/mortality models.
- **Do not claim:** Stochasticity or approximation remains globally `UNRESOLVED`; those July gaps are now partly solved in these explicit model classes.

### F3. Hidden cross-guild coupling

- **Status:** Exact criterion + sharp one-step approximate bound in the declared Bernoulli recruitment model.
- **Module:** `cross_guild_stochastic_coupling.py`.
- **Claim:** capped two-guild state is exact iff saturated-tail downstream hazard diameter `delta=0`; best single common row has worst TV error `delta/2`.
- **Do not claim:** The elementary Bernoulli/TV calculation classifies arbitrary interaction networks.

### F4. Spatial reachability

- **Status:** Exact finite theorem.
- **Module:** `spatial_dispersal_reachability.py`.
- **Claim:** monotone directed spread reduces to distance-to-target plus unreachable; with at most `H` future spreads, the initial quotient has `min(D,H)+2` classes.
- **Do not claim:** Arbitrary dispersal, extinction, state-dependent edges, or feedback networks reduce to the same distance summary.

### F5. Feedback-network candidate

- **Status:** Open candidate with finite nonreducibility benchmark, **not a public theorem**.
- **Sources:** `experiments/feedback_network_nonreducibility.py`, `docs/feedback_network_candidate_triage_2026-08-14.md`.
- **Claim currently allowed:** a five-state benchmark defeats a static distance/occupancy summary only after `spread -> turnover -> spread`.
- **Do not claim:** a scalable feedback-memory theorem has been proved.

## G. Current unresolved regions after hypothesis recovery

The old July statement that “stochasticity and approximate portability are unresolved” is superseded by Section F in specific declared model classes.

The genuinely open scientific questions currently retained by `docs/hypothesis_recovery_ledger_2026-08-14.md` are:

1. scalable feedback-aware closure/portability beyond the finite PR #198 benchmark;
2. an empirical application with sufficient transition/recruitment/movement information to identify a declared CCOC mechanism rather than merely fit associations.

Arbitrary models outside the proved deterministic/stochastic/ecological/spatial subclasses remain `UNRESOLVED` unless another certificate applies.

## Review rule

Every new public theorem statement must name one status above and state:

1. finite/declared semantic domain and legal grammar;
2. additional premise/resource/error contract;
3. valid conclusion; and
4. a sentence beginning **“Do not claim:”**.

Novelty is a separate later adjudication. A correct theorem status does not by itself establish historical novelty.
