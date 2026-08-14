# Mechanism-to-data bridge — 2026-08-14

> **Purpose:** translate established CCOC ecological theorem assumptions into observable quantities, falsification checks, and minimal empirical contracts without turning the theorem repository into an empirical fitting package. This document does not claim that any real system satisfies the assumptions. It states what data would be needed to test that claim.

## 1. Governing principle

The ecological theorems are useful only if their structural assumptions can be confronted with observations or experiments.

The bridge therefore separates four layers:

1. **semantic state** — what ecological microstate the theorem means by abundance, occupancy, or guild state;
2. **future grammar** — which colonization, depletion, mortality, or spread events are treated as legal futures;
3. **response** — what outcome defines causal equivalence;
4. **mechanism parameter** — the threshold/rate/hazard/reachability quantity appearing in the theorem.

A dataset can support an application only if all four are operationally declared. Fitting a convenient statistical model to one response variable does not identify the CCOC grammar or causal interface by itself.

## 2. Saturation threshold `L_g`

### Theorem role

For guild abundance `N_g`, the deterministic saturation theorem uses

\[
Z_g=\min(L_g,N_g).
\]

Exact compression requires states above `L_g` to be future-equivalent under the declared legal dynamics.

### Observable contract

Data need:

- repeated or manipulated measurements of guild abundance `N_g`;
- the declared focal response used by the theorem;
- repeated next-state observations under comparable legal actions/environmental conditions;
- enough observations above a candidate threshold to test the saturated tail rather than extrapolate it.

### Falsification condition

A proposed threshold `L_g` fails if there exist two states with

\[
N_g,N'_g\ge L_g
\]

and the same other declared macro variables/actions, but either:

1. the focal response differs; or
2. their next-macro-state transition laws differ materially.

Thus visual flattening of a mean response curve is insufficient. Exact saturation is a **response-plus-transition** claim.

### Practical estimand

The empirical target is the smallest defensible `L_g` after which both the response and the relevant transition kernel cease to depend on hidden abundance. For exact application, residual tail dependence must be treated as a failure, not as noise that can be ignored by definition.

For approximate application, tail dependence should be quantified and propagated as an error budget rather than forcing a binary saturated/unsaturated classification.

## 3. Downward-reach budget `D`

### Theorem role

If at most `D` future one-unit depletion events remain legal, the exact initial abundance cap is

\[
L+D.
\]

### Observable/experimental contract

`D` is primarily a **future-grammar quantity**, not a free fitted parameter. It must be tied to a declared observation/intervention horizon and event definition.

Possible empirical inputs:

- maximum number of discrete depletion/disturbance events that can occur within the declared horizon;
- a conservative bound on cumulative downward abundance change, converted into the theorem's event units;
- experimental protocols specifying how many removals/interventions are allowed;
- management/disturbance regimes that explicitly bound future removals.

### Falsification condition

A claimed budget `D` fails as an exact grammar restriction if an admissible future can reduce abundance by more than `D` theorem units before the response horizon closes.

Do not estimate `D` from the realized number of disturbances in one short time series while declaring larger disturbances illegal. The grammar concerns **possible legal futures**, not only observed frequency.

## 4. Mortality/depletion rate `mu`

### Theorem role

The stochastic results distinguish exact causal relevance from finite-horizon detectability. Positive downward rate can restore full exact abundance distinguishability even when a small finite-horizon macro remains accurate.

### Constant-total-rate model

For a state-independent depletion clock, the empirical target is a total event rate `mu`.

Data need:

- event times or repeated intervals with known exposure duration;
- a defensible definition of one depletion event;
- evidence that the event intensity is approximately constant over the state range to which the theorem is applied.

The finite-horizon bound depends on the dimensionless product `mu*T`, so reporting `mu` without the corresponding response horizon `T` is incomplete.

### Per-capita mortality model

For independent per-capita mortality, data need individual or cohort survival information sufficient to evaluate the assumption that survival probability over time `t` is approximately

\[
q=e^{-\mu t}.
\]

The theorem should not be applied merely because a survival curve is monotone. Dependence among individuals, density-dependent mortality, or shared shocks change the transition kernel and must be checked separately.

### Falsification condition

The chosen mortality mechanism fails if transition probabilities depend on hidden state variables in ways not represented by the declared model. A poor rate model is not rescued by the abstract CCOC theorem.

## 5. Hidden cross-guild coupling diameter `delta`

### Theorem role

For response-capped guild A with threshold `L_A`, let hidden A abundance modulate guild-B recruitment hazard `p(A)`. The saturated-tail diameter is

\[
\delta
=
\sup_{A\ge L_A}p(A)-\inf_{A\ge L_A}p(A).
\]

Exact capped portability requires `delta=0`; the sharp one-step minimax common-macro TV error is `delta/2`.

### Observable contract

Data need:

- A abundance measured **above** the candidate saturation threshold, not only capped A state;
- B recruitment/colonization outcomes over a fixed interval or action;
- B's current declared macrostate;
- the environmental/action variables that define the transition row;
- replication across the saturated A tail.

### Estimand

The target is not a generic regression coefficient for A. It is the **range of the response-relevant B transition hazard over A states that the proposed macro would merge**.

Operationally, estimate or bound

\[
\sup p(B\text{ recruits}\mid A, Z_B,a)-
\inf p(B\text{ recruits}\mid A, Z_B,a)
\]

over `A>=L_A` within a declared action/context stratum.

### Falsification and interpretation

- statistically/experimentally defensible tail invariance supports the exact-lumping assumption only to the resolution of the data;
- a nonzero tail effect falsifies exact capped portability for that mechanism;
- an upper confidence bound on `delta` can be propagated into the theorem's one-step/path-TV approximate error bound.

The key ecological question is therefore not whether hidden A abundance varies, but whether that variation changes a downstream response-relevant kernel.

## 6. Directed dispersal edges and reachability depth

### Theorem role

The spatial theorem treats an occupied-patch subset on a directed graph. Future response is determined by minimum directed distance to the focal patch under repeated `spread` actions.

### Graph contract

A directed edge `u -> v` means that one legal spread step can move occupancy/influence from `u` to `v` under the declared mechanism. An edge is therefore mechanistic, not merely geographic proximity.

Evidence for an edge could come from:

- time-ordered colonization consistent with one-step movement;
- direct movement/propagule tracking;
- experimental transfer/connectivity tests;
- a separately validated dispersal model defining one-step accessibility.

Occurrence co-presence alone does not identify edge direction.

### Falsification condition

A graph is falsified for the declared spread mechanism if observed legal transitions repeatedly use edges declared impossible, or if declared one-step edges systematically fail under the conditions that supposedly define the action.

### Reachability quantities

Once the directed graph is declared, compute:

- distance from occupied patches to the focal target;
- maximum finite reachability depth `D`;
- unreachable components/barriers.

These are graph-derived quantities, not fitted response coefficients.

## 7. Future horizon `H`

### Theorem role

With at most `H` legal spread steps,

\[
|P_H|=\min(D,H)+2.
\]

### Empirical meaning

`H` must correspond to a declared response horizon plus a definition of one spread step. Examples:

- `H` seasonal colonization opportunities;
- `H` discrete dispersal generations;
- `H` experimentally permitted transfer rounds.

A clock-time horizon cannot be substituted for `H` until a step-duration model is supplied.

### Falsification condition

If more than `H` spread transitions are legal before the declared response is evaluated, then the finite-horizon grammar has been misspecified.

## 8. Testing exchangeability within guilds

Several abundance theorems compress individual identity into guild counts. That requires a form of exchangeability relative to the declared response and transition kernel.

Minimal check:

- compare states with equal guild counts but different individual/species identities or configurations;
- hold declared macro covariates/actions fixed;
- test whether focal responses and next-macro-state laws differ.

Persistent identity/configuration effects mean that guild count is not a sufficient semantic state for that application. The correct response is to refine the state description, not to force the theorem onto the data.

## 9. Information-flow quantities

The resource theorem uses

\[
I(E;C)+I(E;U\mid C).
\]

This can in principle be estimated only when the exterior state `E`, pre-opening representation `C`, and update/transcript `U` are jointly observable or experimentally recorded. Empirical mutual-information estimation is itself a separate statistical problem and should not be treated as proof of the theorem assumptions.

For an ecological application, the more interpretable first targets are usually `L`, `D`, `mu`, `delta`, directed edges, and `H`. Information-flow estimation is a second-stage analysis after the semantic variables are well defined.

## 10. Three minimal application datasets

### A. Saturation/disturbance dataset

Required fields:

- time/site/replicate;
- guild abundance before transition;
- focal response;
- action/disturbance label;
- next guild abundance/state;
- exposure interval.

Can test: `L`, bounded `D`, deterministic/stochastic saturation, and `mu` assumptions.

### B. Cross-guild recruitment dataset

Required fields:

- A abundance including the saturated tail;
- B current state;
- B recruitment outcome;
- action/context/exposure interval;
- relevant environmental covariates or experimental block.

Can test: hidden-tail hazard diameter `delta` and approximate portability.

### C. Spatial reachability dataset

Required fields:

- patch identifiers and geometry/network context;
- time-ordered occupancy;
- direct movement/propagule evidence where available;
- declared spread-step interval/action;
- focal target response.

Can test: directed edge hypotheses, barriers, distance shells, `D`, and horizon `H`.

## 11. Decision table for an application

A theorem-to-data application should report one of four outcomes for each structural assumption:

- **SUPPORTED AT CURRENT RESOLUTION** — no detected violation within a predeclared tolerance/data resolution;
- **APPROXIMATE** — violation quantified and propagated through a theorem error bound where available;
- **FALSIFIED** — an observed/experimental transition contradicts the declared structural assumption;
- **UNIDENTIFIED** — available data do not distinguish the relevant microstates/actions.

`UNIDENTIFIED` is not evidence for exact compression.

## 12. Repository boundary

This bridge belongs in CCOC because it defines the empirical meaning and falsification contract of theorem parameters. Actual fitting, data cleaning, model selection, uncertainty computation, and ecological case-study claims should live in a dedicated application repository/package.

Do not add data-dependent fitted constants to the theorem registry.
