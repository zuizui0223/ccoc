# Feedback-network candidate triage — 2026-08-14

> **Purpose:** decide what would count as genuinely new ecological mechanism theory after the existing saturation, depletion, stochastic-coupling, and spatial-reachability packages. This is a research-control document, not a theorem claim.

## 1. Why another nearby model is not enough

CCOC already has exact or sharp results for:

- monotone abundance saturation;
- bounded/unbounded downward reach;
- stochastic mortality/depletion;
- hidden cross-guild modulation of a downstream transition hazard;
- monotone spread on a fixed directed graph;
- finite future-horizon reachability.

A proposed “network ecology” extension is not new merely because it combines two of those ingredients in one state vector.

The following are **not** sufficient new targets:

1. static directed spread + independent mortality at each patch;
2. a fixed graph plus one cross-guild recruitment probability `p(A)`;
3. static shortest-path reachability multiplied by a depletion budget;
4. a product macro containing both capped abundance and current directed distance;
5. replacing a Bernoulli hazard by another one-parameter family while the dependency structure is unchanged.

Those are compositions or parameter changes of established results.

## 2. Minimum mechanism required for a new theorem

The next serious mechanism must contain **endogenous feedback between ecological state and future accessibility**.

A useful candidate class has three coupled layers:

### Occupancy / abundance state

Patch/guild state `X_t` records the ecological entities whose presence, abundance, or local mode matters.

### Interaction state

`M_t` records a finite interaction mode: facilitators, inhibitors, mutualists, antagonists, or other local interaction states that alter transitions.

### Effective movement/transition structure

The directed colonization graph or transition kernel is

\[
G(X_t,M_t)
\quad\text{or}\quad
K(\cdot\mid X_t,M_t,a_t),
\]

rather than one fixed graph/kernel.

The feedback requirement is that legal dynamics include both directions:

\[
(X_t,M_t)
\longrightarrow
\text{future movement/extinction kernel}
\longrightarrow
(X_{t+1},M_{t+1}),
\]

and the ecological transition can in turn change the interaction mode that controls later movement or extinction.

A one-way covariate effect is not enough; there must be a cycle.

## 3. Canonical ecological interpretation

One minimal biological reading is:

1. occupancy of a facilitator/mutualist opens or strengthens a dispersal/colonization pathway;
2. colonization of another guild changes competitive/predatory pressure;
3. that interaction changes extinction or persistence of the facilitator;
4. facilitator loss then closes or weakens future reachability.

The focal response can be target occupancy, persistence, or another declared state/output. The exact choice must be fixed before quotient statements are made.

This captures a phenomenon absent from the current spatial theorem: **the graph on which future reachability is evaluated is itself an ecological state variable altered by the dynamics.**

## 4. Non-reducibility test

Before implementation, construct the smallest finite witness in which two microstates agree on every existing summary listed below but have different future responses:

- current focal output;
- current static shortest distance to the target;
- current capped guild abundances;
- remaining scalar depletion budget;
- current one-step downstream hazard diameter bound treated independently of movement.

Yet the pair must be separated by a legal future word because their hidden interaction state changes a future edge/kernel and that altered edge/kernel feeds back into later persistence or movement.

If no such witness exists, the candidate probably reduces to a product/composition of existing theorems and should not become a new package.

## 5. Stronger non-reducibility target

The best witness would show that **no summary formed only from current reachability plus independent local hazard summaries is exact**.

One route is a feedback cycle where:

- hidden mode `m` changes which corridor is available after a colonization event;
- taking that corridor changes the state that controls later extinction;
- extinction then changes which corridor is available on a subsequent spread.

The distinguishing word therefore needs alternating movement and turnover events. A one-step transition-row comparison or one static shortest-path query would not expose the distinction.

This would separate the new mechanism from both:

- `spatial_dispersal_reachability.py`, whose graph is fixed; and
- `cross_guild_stochastic_coupling.py`, whose hidden-tail effect changes a transition probability but does not endogenously rewrite future spatial accessibility.

## 6. Positive theorem target

A useful positive result should identify an **interaction-closed macrostate** rather than defaulting to the full microstate.

Candidate structure:

- a finite macro interaction mode `Q`;
- a macro occupancy/reachability summary `R`;
- every legal ecological action sends `(Q,R)` to a distribution or successor depending only on `(Q,R)`;
- effective movement edges relevant to the focal response are determined by `Q`;
- feedback updates of `Q` depend only on `(Q,R)`.

Then `(Q,R)` is an exact controlled macro interface even though the physical graph changes through time.

The theorem would be worthwhile only if `|Q|` and the size of `R` can stay bounded while the underlying patch/species system grows under a clear structural condition (for example bounded interaction types/modules rather than bounded total graph size).

## 7. Negative theorem target

A complementary lower bound should show how portability fails when hidden interaction modes remain addressable through feedback.

A candidate parameter is an **independent feedback-mode rank** `r`: the number of interaction distinctions that can be separately converted, through legal alternating movement/turnover words, into different focal response traces.

If a finite family realizes all `2^r` feedback profiles while keeping the currently visible reachability/capped-abundance summary fixed, then every exact interface must retain at least `r` feedback bits.

However, do not promote this as new merely by renaming the existing addressability theorem. A worthwhile construction must derive the `r` addressable modes from the ecological feedback rules themselves and exhibit a structural constraint or sharpness property not already supplied by the relay family.

## 8. Resource question worth testing

The potentially new resource phenomenon is **adaptation caused by endogenous graph rewiring**, not generic message passing.

Ask whether one can bound the information/time needed to update a macro when ecological feedback changes which movement edges are causally relevant.

A meaningful result would couple:

- number of newly relevant interaction/movement modes;
- boundary communication/update capacity;
- response horizon;
- approximation error.

Do not restate the existing retention/update bound unless state-dependent accessibility creates a new structural upper/lower term.

## 9. Falsification against existing packages

Before opening theorem code, the candidate must pass all four checks:

### Check A — not static reachability

Freezing the interaction state should collapse the model to the existing spatial theorem. The new result must use transitions that change that interaction state.

### Check B — not independent cross-guild hazard

Removing the movement/reachability dependence should collapse the model to the existing `delta` theorem. The new result must require the hazard/interaction effect to alter future accessibility or be altered by movement.

### Check C — not a scalar depletion budget

Replacing feedback with a bounded count of removals should reduce to `L+D`. The new distinction must depend on **which interaction state changes**, not only how many downward events remain.

### Check D — not generic causal cone

A proof based only on bounded degree, locality, and finite propagation speed is substrate. The theorem must exploit the ecological feedback structure to obtain its macrostate, lower bound, or sharp tradeoff.

## 10. Minimal executable benchmark before theorem code

Use a tiny finite benchmark only after specifying the mechanism:

- 3–6 patches/nodes;
- binary or very small local ecological states;
- at least one facilitator/inhibitor interaction mode;
- spread and extinction/turnover actions;
- one focal output;
- a feedback cycle causing a later movement edge/kernel to depend on an earlier ecological transition.

Enumerate the canonical response quotient and compare it against:

1. static-distance summary;
2. capped-abundance summary;
3. their direct product;
4. the proposed feedback-aware summary.

Proceed to a theorem family only if the feedback-aware summary captures a repeatable structural pattern and the direct-product baseline provably fails.

## 11. Stop rule

Do not create a new `feedback_*` theorem module until the non-reducibility witness exists and survives the four checks above.

If the smallest examples always collapse to an existing product summary, record that negative triage result and stop. The repository already contains enough theorem variants; failed novelty triage is a useful result.
