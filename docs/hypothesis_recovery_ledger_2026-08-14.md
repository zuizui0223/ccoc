# CCOC hypothesis recovery ledger — 2026-08-14

> **Ordering rule:** hypothesis recovery comes before novelty adjudication. This ledger records what was asked, proved, refuted, corrected, archived, or left open. It intentionally does **not** decide historical novelty. Existing novelty audits are provisional inputs until this ledger is accepted as complete.

## Status vocabulary

- **PROVED** — analytic theorem exists on the declared domain; finite certificates may replay it.
- **SHARPNESS / CONSTRUCTION** — an explicit family attains a bound; not a classification of all systems.
- **NO-GO PROVED** — a quantified impossibility holds in the declared evidence/model class.
- **REFUTED** — the proposed statement is false; a concrete counterexample is retained.
- **CORRECTED** — the original broad statement was false/too broad and has a valid replacement.
- **CONDITIONAL / SUFFICIENT** — valid only under stated extra assumptions; converse not claimed.
- **UNRESOLVED** — neither a positive certificate nor a lower-bound obstruction currently classifies the case.
- **OPEN CANDIDATE** — finite benchmark or research question exists, but no public theorem yet.
- **LEGACY / ARCHIVED** — scientifically retained for provenance but outside the current first-paper proof spine.
- **UNMERGED EXPERIMENTAL** — posed and partly implemented on an unmerged branch; never promoted to the canonical theory.
- **HISTORICAL GATE** — hypothesis about prior literature, not a CCOC mathematical theorem.

## Recovery boundary

This ledger covers scientific/evidential hypothesis families posed in the repository through PR #200, including the July registry (`CORE-0`--`CORE-5`, `EXT-1`--`EXT-4`, `ID-1`--`ID-3`, `LEGACY-1`), August reopen theorems, false intermediate conjectures, and the current feedback/application candidates. Pure serialization, signing, packaging, and CI engineering changes are not separate scientific hypotheses unless they changed an evidence-validity assumption.

---

## A. Pre-CCOC causal-replaceability and evidence hypotheses

| ID | Recovered hypothesis / question | Current status | Decisive source / replacement | Scope guard |
|---|---|---|---|---|
| `HYP-A01` | In the finite sign-consistent disjunctive structural model, null observations eliminate mechanisms exactly and a last-driver-standing criterion can certify causal replaceability. | **PROVED / LEGACY** | early theorem core; `replaceability.py` and associated tests | Conditional on the declared candidate set, sign/grammar assumptions, and observation fidelity. |
| `HYP-A02` | A generalized finite qualitative program (`AllOf`/`AnyOf`/`Not`) can enumerate admissible mechanism states and classify forced mechanisms under hard/noisy observations. | **PROVED / LEGACY** | `ecological_program.py` | Does not identify the true biological program without a supplied candidate universe. |
| `HYP-A03` | Joint confidence-set coverage at level `1-alpha` lifts to a bound `<=alpha` on false decisive mechanism claims. | **PROVED / LEGACY** | `confidence_lifting.py` | Coverage is an input contract, not inferred from the lifting theorem. |
| `HYP-A04` | The same soundness guarantee survives arbitrary stopping/look selection if an all-look/anytime coverage certificate is supplied. | **PROVED / LEGACY** | `anytime_confidence_lifting.py` | Optional stopping is safe only under the declared anytime certificate. |
| `HYP-A05` | Symbolic candidate-set reasoning adds solver-validity error `beta`, giving false-decisive risk `<=alpha+beta`; proof-carrying exact rational certificates can set `beta=0`. | **PROVED / LEGACY** | symbolic candidate / feasibility certificate modules | Solver validity must itself be certified. |
| `HYP-A06` | Outer-envelope/model-universe uncertainty contributes an additional `gamma`, yielding `alpha+beta+gamma`; exact inclusion certificates can make `gamma=0` for admitted looks. | **PROVED / LEGACY** | outer-envelope / polyhedral inclusion modules | Only for the declared nesting/admission contract. |
| `HYP-A07` | Under nested candidate universes, outer-invariant/excluded classifications persist inward, while inner unresolved cases remain unresolved outward in the stated directions. | **PROVED / LEGACY** | nested-universe stability modules | Not a claim that every candidate universe is correctly nested. |
| `HYP-A08` | Decisive result manifests remain sound only when every required proof/evidence binding is complete and replayable. | **PROVED AS EVIDENCE CONTRACT / LEGACY** | manifest/admission-transcript/checkpoint work | Cryptographic integrity does not prove scientific completeness. |
| `HYP-A09` | Finite-alphabet e-processes with running-max retention could provide all-look candidate retention with error allocated across required cells rather than competitors. | **UNMERGED EXPERIMENTAL** | PR #31 branch | Never merged; do not cite as canonical theorem. |

## B. Closure, observation, and identifiability hypotheses

| ID | Recovered hypothesis / question | Current status | Decisive source / replacement | Scope guard |
|---|---|---|---|---|
| `HYP-B01` | A finite deterministic update map can be exactly certified as globally closing, recurrent nonclosure, or multistable nonclosure. | **PROVED / `CORE-0` LEGACY** | `causal_closure_calculus.py` | Finite total deterministic maps only. |
| `HYP-B02` | Observer/candidate-specific closure verdicts can be promoted to one conclusion even when retained candidates disagree. | **REFUTED AS A UNIVERSAL INFERENCE** | observer-coupled closure work | Candidate disagreement is deliberately `UNRESOLVED`. |
| `HYP-B03` | Passive/current observations alone are sufficient to certify future closure. | **REFUTED** | observation-regime / completion counterexamples | Future legal probes can separate passively identical states. |
| `HYP-B04` | Any fixed finite observation horizon is enough to certify closure uniformly over delayed families. | **NO-GO PROVED** | `observation_window_completion.py`, `delayed_addressability.py` | A supplied independent horizon bound changes the problem. |
| `HYP-B05` | A jointly realizable addressable product `I x E_1 x ... x E_q` forces additive exact open-interface memory. | **PROVED LOWER-BOUND OBSTRUCTION** | `addressable_completion_bounds.py`, `extension_compression_noncommutation.py` | Requires joint realizability and legal coordinate decoders. |
| `HYP-B06` | Exact dynamic compression is equivalent to output preservation plus update closure under every legal action; the all-word quotient is the unique coarsest exact interface and stabilizes finitely. | **PROVED** | `dynamic_boundary_blankets.py` | Declared finite deterministic controlled system. |
| `HYP-B07` | Required memory and first distinguishing delay are the same resource. | **REFUTED** | `delayed_addressability.py` | Families independently tune memory gap and delay. |
| `HYP-B08` | A finite transcript, even with many samples, gives an upper bound on the complete canonical boundary complexity without a completion/coverage contract. | **REFUTED / NO-GO PROVED** | witnessed-boundary / free-completion no-go | Finite evidence gives witnessed lower bounds unless grammar/completion coverage is supplied. |
| `HYP-B09` | Some finite-depth adaptive experiment can uniformly certify closure over the unbounded delayed family. | **NO-GO PROVED / `ID-1`** | `adaptive_closure_no_go.py` | Does not prohibit certification under an externally bounded model/horizon class. |
| `HYP-B10` | Grammar state can be omitted whenever physical state/output match. | **REFUTED** | `grammar_aware_blankets.py` | Enabled-action/future-language differences can require grammar state in the exact interface. |
| `HYP-B11` | Candidate-specific exact small macro laws automatically imply one candidate-universal deterministic macro law. | **REFUTED; exact replacement PROVED** | `candidate_safe_laws.py` / `ID-2` | Universal law exists iff all induced candidate maps agree on every declared action. |
| `HYP-B12` | Exterior-state and candidate-mechanism lower bounds add automatically. | **REFUTED AS AN AUTOMATIC RULE; CONDITIONAL JOINT BOUND PROVED** | `joint_open_candidate_laws.py` / `ID-3` | Additivity requires explicit joint separation/realizability. |
| `HYP-B13` | With resettable fresh copies, delayed joint memory/depth/action budgets have exact finite panel frontiers. | **PROVED / LEGACY DESIGN** | delayed joint reset/budgeted quotient modules | Requires the declared reset/fresh-copy protocol. |
| `HYP-B14` | Replication count alone guarantees robustness to common-mode failure. | **REFUTED; corrected panel theorem PROVED** | robust/common-mode canonical panel modules | Robustness depends on the declared failure-mode cover, not raw replicate count. |

## C. First-paper closed/open composition hypotheses

| ID | Recovered hypothesis / question | Current status | Decisive source / replacement | Scope guard |
|---|---|---|---|---|
| `HYP-C01` | A system may admit a very small exact interface in a closed composition while the corresponding open grammar requires a much larger exact interface. | **PROVED** | initial extension-compression witnesses; now `CORE-2` | Exact statement is relative to declared legal futures. |
| `HYP-C02` | The closed/open separation can be realized by bounded local interactions on a degree-three relay tree. | **SHARPNESS / CONSTRUCTION PROVED** | `relay_tree_compilation.py` / `CORE-3` | Does not classify arbitrary bounded-degree networks. |
| `HYP-C03` | Operational addressability plus closed-context factorizations yields an extension--compression noncommutation lower bound. | **PROVED / `CORE-2`** | `extension_compression_noncommutation.py` | Closed factorization supplies an upper bound, not automatically the exact closed minimum. |
| `HYP-C04` | Every family must either have one finite common interface or exhibit the addressable-product lower bound. | **REFUTED AS A DICHOTOMY** | `compositional_boundedness.py` | Systems satisfying neither certificate remain `UNRESOLVED`. |
| `HYP-C05` | Small exact interfaces at each stage are sufficient for one portable macro-law across stages. | **REFUTED AS SUFFICIENT; corrected criterion PROVED** | `coherent_portable_macrolaw.py` | Common output/action/transition meanings and label coherence are additionally required. |
| `HYP-C06` | Conservative legal-action growth preserves one finite macro schema if old meanings persist and newly legal actions descend uniformly on macro fibers. | **PROVED SUFFICIENT / `CORE-4`** | `conservative_macro_schema.py` | Not necessary for every possible portable law. |
| `HYP-C07` | A future word/new action splitting one proposed fiber proves that no alternative macro-law exists. | **REFUTED AS GLOBAL CLAIM; local obstruction PROVED / `CORE-5`** | `coherent_portable_macrolaw.py`, `conservative_macro_schema.py` | It refutes that merge only. |
| `HYP-C08` | Product independence is necessary for the open-memory lower bound. | **REFUTED; codebook generalization PROVED** | `addressable_codebooks.py` / PR #107 | Sufficiently large jointly realizable codebooks with legal decoders are enough. |
| `HYP-C09` | For a common plant and union of closed legal-word families, the exact union-language equivalence is the intersection/common refinement of the closed equivalences. | **PROVED** | union-grammar refinement work / PR #111 | Same plant/response semantics and declared language union. |
| `HYP-C10` | Total inflation decomposes into nominal closed-family capacity, join loss, and open-only innovation. | **PROVED IDENTITY** | interface-inflation decomposition / PR #113 | Bookkeeping identity; not by itself a mechanism theorem. |
| `HYP-C11` | One newly legal primitive action can create linear pure open-only innovation while every fixed closed quotient and their union remain tiny. | **PROVED** | single-action innovation / PR #115, generalized by PR #160 | Initially powers of two, later all `m>=1`. |
| `HYP-C12` | Open-only innovation cannot exceed finite semantic-domain capacity, and equality occurs when the open quotient is discrete. | **PROVED; relay saturates** | innovation-capacity work / PR #117 | Finite domain. |
| `HYP-C13` | Bounded graph degree alone forces a logarithmic latency lower bound for resolving exponentially many states. | **REFUTED / TOO WEAK; corrected causal-cone theorem PROVED** | PR #117 scope correction; `local_causal_cone.py` / PR #120 | Need local update radius and bounded local information/state capacity, not degree alone. |
| `HYP-C14` | Small physical cut width/treewidth alone implies a uniformly small exact causal interface. | **REFUTED BY CONSTRUCTION** | fixed relay/extremal family | Cut one still permits `m` bits of exact open inflation. |

## D. Non-nested replacement / transport hypotheses (`EXT` archive)

| ID | Recovered hypothesis / question | Current status | Decisive source / replacement | Scope guard |
|---|---|---|---|---|
| `HYP-D01` | A connected replacement graph can share one exact macro law under supplied output/action/label-preserving successor-closed transport relations, even many-to-one or one-to-many. | **PROVED SUFFICIENT / `EXT-1`** | `non_nested_portability.py` | Supplied projections/relations; not necessary. |
| `HYP-D02` | A target exact factorization can be constructed from a source projection and a fiber-consistent total transport relation. | **PROVED SUFFICIENT / `EXT-2`** | `non_nested_portability.py` | Requires target-fiber label consistency and action-row preservation. |
| `HYP-D03` | Target-only actions can be admitted under a non-nested conservative transport when availability and macro successors are uniform within target fibers. | **PROVED SUFFICIENT / `EXT-3`** | `non_nested_conservative_transport.py` | Does not cover arbitrary new actions. |
| `HYP-D04` | A newly legal target word splitting one carried fiber refutes that carried merge. | **PROVED LOCAL OBSTRUCTION / `EXT-4`** | `non_nested_portability.py` | No global memory-growth conclusion. |
| `HYP-D05` | Failure of one supplied transport/reuse certificate implies no alternative portable macro-law exists. | **NOT PROVED / EXPLICIT NON-CLAIM** | claim-status audit | Keep outside the theorem set. |

## E. Fixed-regular extremal and exact converse hypotheses

| ID | Recovered hypothesis / question | Current status | Decisive source / replacement | Scope guard |
|---|---|---|---|---|
| `HYP-E01` | The one-action extremal family can be made fully uniform for every `m>=1` with a fixed four-symbol alphabet, fixed one-state closed/open grammar schemas, degree `<=3`, cut one, bounded local alphabets, and open quotient `2^(m+1)`. | **PROVED / SHARPNESS** | `fixed_regular_grammar_relay.py`, `extremal_open_composition.py`, PR #160 | Explicit family, not all networks. |
| `HYP-E02` | In a one-state action-language expansion, iterating refinement of the closed canonical quotient by the newly available open actions reaches exactly the open canonical quotient. | **PROVED** | `action_grammar_closure.py`, PR #161 | One-state action grammar. |
| `HYP-E03` | Arbitrary multi-state finite grammar transition completion can only refine the canonical grammar-aware quotient. | **REFUTED** | PR #162; explicit coarsening counterexample | This false claim must never be restored. |
| `HYP-E04` | The refinement/converse theorem is valid for multi-state **globally-new-symbol** expansion when every old action column is frozen. | **CORRECTED + PROVED** | `grammar_expansion_closure.py`, PR #163 | No filling of a missing transition for a symbol already legal somewhere closed. |
| `HYP-E05` | Under arbitrary same-domain grammar change, canonical closed/open quotients must be nested. | **REFUTED** | `grammar_interface_reuse.py`, PR #164 | They may be equal, finer, coarser, or incomparable. |
| `HYP-E06` | Under arbitrary same-domain grammar change, the old closed labeling is reusable exactly iff open enabled-action rows and successor fibers descend uniformly on each closed fiber. | **PROVED** | `grammar_interface_reuse.py`, PR #164 | Reuse theorem, not quotient-monotonicity theorem. |
| `HYP-E07` | Along a valid globally-new-symbol expansion chain, the terminal quotient is the minimum single exact labeling valid for every stage. | **PROVED** | `terminal_grammar_portability.py`, PR #166 | Corrected expansion class only. |

## F. Portability resource hypotheses

| ID | Recovered hypothesis / question | Current status | Decisive source / replacement | Scope guard |
|---|---|---|---|---|
| `HYP-F01` | If exterior coordinates must be recoverable after opening, retained pre-opening information and post-opening update information obey an additive information lower bound. | **PROVED** | `portability_adaptation_tradeoff.py`, PR #167/#172 | Fano/entropy substrate; semantic variables/decoder errors must be declared. |
| `HYP-F02` | A finite boundary of width `c` and alphabet size `s` converts update-information debt into an installation-time lower bound `I(E;C)+cT log2 s >= ...`. | **PROVED** | retention-boundary-time theorem, PR #168 | Full interface materialization, not one counterfactual query. |
| `HYP-F03` | Selected-query latency and full-interface installation time are the same asymptotic resource. | **REFUTED BY SEPARATION** | PR #168/#169 | Fixed relay has selected query `Theta(log m)` but full installation `Omega(m)`. |
| `HYP-F04` | For staged exact binary/power-of-two materialization, terminal capacity alone is sufficient to meet every intermediate deadline. | **REFUTED AS SUFFICIENT; exact prefix criterion PROVED** | PR #171 | Need `k + sum_{q<=t} L_q >= m_t` for every prefix. |
| `HYP-F05` | The update bound should be stated only with `H(U|C)`. | **CORRECTED / STRENGTHENED** | PR #172 | Strong form uses `I(E;U|C)`; entropy form is a corollary. |

## G. Deterministic ecological hypotheses

| ID | Recovered hypothesis / question | Current status | Decisive source / replacement | Scope guard |
|---|---|---|---|---|
| `HYP-G01` | Under guild exchangeability, response saturation thresholds `L_g`, and non-negative colonization, capped abundance `Z_g=min(L_g,N_g)` is an exact dynamic blanket independent of raw abundance capacities. | **PROVED** | `ecological_saturation_blanket.py`, PR #173 | Requires forward-invariant saturated fibers under the legal dynamics. |
| `HYP-G02` | Saturation of the present response alone is enough to forget hidden oversaturation even after downward/depletion actions open. | **REFUTED** | PR #173 depletion obstruction | Repeated depletion can reveal all hidden oversaturation and restore `M+1` classes. |
| `HYP-G03` | Different abundance-capacity state spaces can share one exact macro law when they factor to the same capped domain and capacity-free transition law. | **PROVED CHANGING-DOMAIN PORTABILITY** | `ecological_capacity_portability.py`, PR #174 | Same saturation thresholds and macro action law. |
| `HYP-G04` | If at most `D` future one-unit depletion events remain legal, the exact initial abundance memory needs cap `L+D`, giving `L+D+1` classes when capacity is large enough. | **PROVED / SHARP IN MODEL** | `budgeted_depletion_blanket.py`, PR #175 | Prefix grammar and one-unit depletion model. |

## H. Stochastic ecological hypotheses

| ID | Recovered hypothesis / question | Current status | Decisive source / replacement | Scope guard |
|---|---|---|---|---|
| `HYP-H01` | Stochasticity by itself destroys exact saturation compression. | **REFUTED; positive exact theorem PROVED** | `stochastic_ecological_portability.py`, PR #177 | If non-negative increment law is `Q_a(D|Z)`, capped state is exact controlled-Markov lumping. |
| `HYP-H02` | A positive one-unit depletion probability `p` is harmless for exact saturated compression. | **REFUTED** | PR #177 | Threshold rows differ by TV `p`; repeated attempts recover all `M+1` exact classes. |
| `HYP-H03` | Rare downward events become causally irrelevant as their rate `mu -> 0`. | **REFUTED FOR EXACT COMPLEXITY** | continuous-time/per-capita results, PR #178/#179 | Exact complexity jumps for every `mu>0`; detectability shifts to a longer rate-adapted horizon. |
| `HYP-H04` | If exact state count grows to `M+1`, every useful finite-horizon macro must also grow with capacity. | **REFUTED; positive approximate portability PROVED** | `finite_horizon_stochastic_saturation.py`, PR #180 | Fixed `L+1` macro has capacity-independent finite-horizon TV bounds in the declared models. |
| `HYP-H05` | Saturation of guild A's own response is sufficient to forget A above `L_A` even if A changes guild B's recruitment. | **REFUTED; exact criterion PROVED** | `cross_guild_stochastic_coupling.py`, PR #182 | Exact capped macro iff downstream saturated-tail hazard diameter `delta=0`; one-step minimax error `delta/2`. |

## I. Spatial and feedback hypotheses

| ID | Recovered hypothesis / question | Current status | Decisive source / replacement | Scope guard |
|---|---|---|---|---|
| `HYP-I01` | The full occupied-patch subset is always needed to predict a monotone directed-spread focal response. | **REFUTED; compressed theorem PROVED** | `spatial_dispersal_reachability.py`, PR #183 | Unlimited exact quotient is directed distance-to-target plus unreachable class. |
| `HYP-I02` | Under at most `H` future spread steps, all finite distances must remain distinct. | **REFUTED; capped-distance theorem PROVED** | PR #183 | Initial quotient has `min(D,H)+2`; farther-than-horizon states can merge with unreachable states for that grammar. |
| `HYP-I03` | Static distance/occupancy summaries remain exact when colonization, turnover, and interaction state feed back on future accessibility. | **REFUTED BY FINITE BENCHMARK** | `experiments/feedback_network_nonreducibility.py`, PR #198 | Not yet a scalable theorem. |
| `HYP-I04` | There exists a scalable feedback-aware closure/portability theorem in which latent interaction state rewrites later reachability and cannot be reduced to independent distance, depletion, or one-step hazard summaries. | **OPEN CANDIDATE** | `docs/feedback_network_candidate_triage_2026-08-14.md`, PR #198 | Requires a family theorem and matching lower/positive boundary before promotion. |

## J. Application / empirical-identifiability hypotheses

| ID | Recovered hypothesis / question | Current status | Decisive source / replacement | Scope guard |
|---|---|---|---|---|
| `HYP-J01` | Existing user-side ecological datasets already identify at least one CCOC structural parameter (`L`, `D`, `mu`, `delta`, directed edges, `H`) strongly enough for a first exact application package. | **CURRENTLY UNIDENTIFIED** | issue #199; mechanism-to-data bridge | Current data lack the required transition/recruitment/movement layer for an exact CCOC mechanism claim. |
| `HYP-J02` | Association/suitability data can be silently substituted for directed transition, recruitment, or movement evidence. | **REJECTED BY APPLICATION CONTRACT** | `docs/mechanism_to_data_bridge_2026-08-14.md` | Such substitutions leave the structural mechanism `UNIDENTIFIED`, not supported. |

## K. Historical compiler comparison hypotheses — not mathematical CCOC claims

| ID | Historical hypothesis | Current status | Evidence state / decisive need | Consequence only after recovery |
|---|---|---|---|---|
| `HIST-H1` | Classical uniform sequential-machine compilation already provides local state/connectivity bounds independent of source state count. | **HISTORICAL GATE — UNRESOLVED** | Need primary construction/resource pages, especially Weiner--Hopcroft / Newborn--Arnold. | Controls historical wording for bounded-local realization existence. |
| `HIST-H2` | The classical construction uses fixed, context-independent source controls/input distribution without source-size-dependent hidden control cost. | **HISTORICAL GATE — PARTIAL** | Ullman--Weiner gives partial fixed-input evidence; distribution/encoding details remain unread. | Controls whether CCOC's fixed-control package is historically distinct. |
| `HIST-H3` | The classical compiled network preserves source response equivalence in both directions, without adding spurious observable distinctions. | **HISTORICAL GATE — PARTIAL** | “Isomorphic realization” wording recovered, but exact output/isomorphism contract remains unread. | Controls whether a compiler transports the closed/open quotient separation faithfully. |
| `HIST-H4` | One source step/input can be realized with bounded/comparable network/output latency rather than source-size-dependent settling time. | **HISTORICAL GATE — PARTIAL** | Primary wording supports size-independent input spacing in Ullman--Weiner; exact timing/output semantics remain unread. | Controls latency/resource comparison only. |

## L. Permanent scope corrections recovered from the project history

These are not optional editorial notes; they are hypotheses that were once tempting or stated too broadly and must remain visible.

1. **Arbitrary finite grammar completion does not monotonically refine the canonical quotient.** PR #162 was false; PR #163/#164 are the corrected theory.
2. **A closed factorization is an upper bound, not automatically the closed minimum.** Equality requires separation/decoder evidence.
3. **A declared product-indexed comparison set need not be transition-closed or reachable from one initial state.** The lower-bound theorem needs the declared semantic product/decoder contract, not that stronger property.
4. **Bounded degree alone does not imply the causal-cone latency bound.** Local update radius and bounded local information are needed.
5. **Finite executable replay is not a proof of an all-parameter theorem.** Analytic proof and finite certificate remain separate evidence layers.
6. **Small stagewise interface size does not imply coherent portability.** Shared macro meanings/dynamics are additional structure.
7. **Failure of one merge or transport certificate does not prove absence of every alternative macro-law.** Local obstruction stays local.
8. **Small physical cut does not imply small exact causal interface.** The fixed relay is a counterexample.
9. **Current output equality does not imply dynamic equivalence.** Future update closure is part of exact compression.
10. **Candidate-specific success does not imply candidate-universal success.** Agreement across retained candidates is a separate hypothesis.

## M. Hypotheses that are complete versus still open

### Mathematically closed / decided

The current repository has a decided answer (proved, refuted, or corrected) for the structural families through exact interfaces, addressability/noncommutation, bounded-local sharpness, conservative portability, same-domain converse/reuse, chain/resource tradeoffs, deterministic saturation/capacity/depletion, stochastic exact/approximate saturation, hidden cross-guild coupling, and directed spatial reachability.

### Open scientific hypotheses

Only the following scientific questions remain genuinely open inside the present CCOC scope:

1. `HYP-I04` — scalable feedback-memory/feedback-portability theorem beyond the five-state benchmark.
2. `HYP-J01` — identify a real application with enough transition/recruitment/movement information to instantiate a CCOC mechanism without conflating `UNIDENTIFIED` with support.

### Open historical hypotheses

`HIST-H1`--`HIST-H4` remain literature-comparison gates and are not mathematical theorem gaps.

## N. Novelty freeze until recovery acceptance

No novelty conclusion is finalized by this ledger. In particular, `docs/maximally_confirmable_novelty_2026-08-14.md` and related prior-art notes are **provisional** until this recovery ledger is accepted as complete.

The next phase, and only the next phase, is to evaluate novelty **row by row** against this ledger:

1. decide whether the hypothesis/result is mathematical substrate, a CCOC-specific theorem, a model-specific extension, or an open candidate;
2. search/compare the closest prior for that exact row and scope;
3. assign a novelty status with explicit evidence and non-claim;
4. only then synthesize manuscript novelty claims.

Do not infer novelty merely because a row is `PROVED`, and do not infer lack of novelty merely because one component has classical ancestry.
