# Quantitative prior-art matrix for the residual CCOC claim

> **Purpose.** The broad historical novelty gate has already established that
> input-restricted minimization, interacting-FSM don't-cares, environment
> abstraction, state-identification test families, and modular sequential-machine
> realization are all prior art. This matrix asks the remaining quantitative
> question:
>
> **Does prior work already combine the same extremal state-count separation and
> bounded-local realization constraints as the current CCOC witness?**
>
> `YES` means directly supported by a source reviewed in the audit. `NO` means the
> reviewed source clearly works outside that condition. `UNKNOWN` means the
> available source did not establish the point; it must not be silently inferred.

## 1. Residual CCOC benchmark

The benchmark to be matched is the post-reopening power-of-two family
`m=2^d` on comparison domain

\[
D_m=\{0,1\}^{m+1}.
\]

It simultaneously has:

1. `m` explicit fixed closed contexts;
2. every fixed closed exact response quotient has two classes;
3. the union of all closed grammars still has two classes;
4. the shared-view/join capacity is also two classes;
5. real local routing dynamics are already legal in the closed contexts;
6. exactly one primitive action type, `fire`, is newly legal when the system is opened;
7. the open quotient becomes discrete on `2^(m+1)` states;
8. therefore open-only innovation is exactly `m` bits and saturates the absolute
   finite-domain upper bound;
9. open global primitive alphabet size is four;
10. the realization uses pairwise radius-one updates, maximum degree three, and
    local state/message alphabets bounded independently of `m`;
11. exact query length is `2 log2(m)+2` in the selector-plus-return architecture;
12. the same family is `O(log m)` and order-optimal under the broader
    bounded-degree/bounded-local-state causal-cone model.

A historical source does **not** subsume this benchmark merely because it proves
input-restricted minimization or uniform modular realization separately.

---

## 2. Matrix

| Prior work | Restricted / incomplete input semantics | Exact or minimum context-dependent implementation | Quantitative restricted→less-restricted state gap | One newly enabled primitive symbol/action | Interacting/environment-generated restrictions | Identical / uniform modules | Bounded fan-in/out / bounded local degree independent of machine size | Explicit local propagation / latency bound | Current assessment |
|---|---|---|---|---|---|---|---|---|---|
| **Kim & Newborn 1972**, *The Simplification of Sequential Machines with Input Restrictions* | **YES** | **YES**, as attributed by Larrauri–Bloem 2021: first exact Tail Minimization solution via an induced incompletely specified Mealy machine | **UNKNOWN** | **UNKNOWN** | Cascade context via the input language produced by the head: **YES** in the later formulation | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Direct prior art for the broad closed-context compression problem; quantitative/local extremal status unresolved |
| **Devadas 1991**, sequential don't-cares in interacting FSMs | **YES** | Optimization/minimization: **YES** | **UNKNOWN** | **UNKNOWN** | **YES** | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Direct ancestry for exploiting contextual sequential irrelevance in networks |
| **Wang & Brayton 1993**, input don't-care sequences in FSM networks | **YES** | Exact cascade don't-care computation attributed to Kim–Newborn; network methods: **YES/partial** | **UNKNOWN** | **UNKNOWN** | **YES**, arbitrary network topology considered | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Broad context/input-restriction mechanism is prior art |
| **Watanabe & Brayton 1993**, maximum permissible behaviors | **YES**, via component/network compatibility | Complete permissible replacement behavior: **YES** | **UNKNOWN** | **UNKNOWN** | **YES** | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Prior art for contextual replacement flexibility, not yet a quantitative match |
| **Aziz–Singhal–Swamy–Brayton 1993**, minimizing interacting FSMs | **YES**, through total-system equivalences/don't-cares | **YES** | **UNKNOWN** | **UNKNOWN** | **YES** | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Strong interacting-FSM minimization ancestry |
| **Raimi–Hojati–Namjoshi 2000**, environment modeling and language universality | **YES** | Safe abstraction/state reduction: **YES** | **UNKNOWN** | **UNKNOWN** | **YES**, explicitly abstracts component FSMs around a focal FSM | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Broad environment-dependent abstraction is prior art |
| **Larrauri & Bloem 2021**, Tail Minimization | **YES** | **YES**, minimum-state replacement under context-generated `Out(H)` | **UNKNOWN**; paper focuses algorithmic complexity/algorithms, not the CCOC extremal ratio in the reviewed passages | **UNKNOWN** | **YES**, sequential composition | **NO/NOT THE TARGET**; replacement is a Mealy machine, not a local-module compilation theorem | **NO/NOT THE TARGET** in the reviewed formulation | **NO/NOT THE TARGET** | Closest modern exact formulation of context-restricted minimization; does not yet establish the CCOC local extremal package |
| **Larrauri & Bloem 2022**, conformance testing under input restrictions | **YES** | Testing rather than minimum implementation: **NO** | **UNKNOWN** | **UNKNOWN** | **YES**, component inputs controlled by other components | **NO/NOT THE TARGET** | **NO/NOT THE TARGET** | Test-length/testing conditions, but not the CCOC local propagation theorem: **NO/DIFFERENT** | Strong semantic neighbor, not a direct extremal implementation result |
| **Weiner & Hopcroft 1968**, bounded fan-in/out uniform decomposition | Input restriction/incomplete specification: **NO in the reviewed abstract** | Realizes a given synchronous sequential machine: **YES** | Restricted→open gap: **NO in the reviewed abstract** | **NO in the reviewed abstract** | **NO in the reviewed abstract** | **YES**, identical two-state modules | **YES**, fan-in/fan-out bound independent of original machine state count | **UNKNOWN** | Direct prior art for bounded-local identical-module realization of arbitrary synchronous machines |
| **Arnold–Tan–Newborn 1970**, iteratively realized sequential circuits | Input restriction/incomplete specification: **NO in the reviewed abstract** | Arbitrary synchronous flow table realization: **YES** | **NO in the reviewed abstract** | **NO in the reviewed abstract** | **NO in the reviewed abstract** | **YES**, identical modules in regular arrays | **UNKNOWN** from the reviewed IBM abstract | **UNKNOWN** | Kills novelty of constant/repeated local-module realization alone |
| **Newborn & Arnold 1972**, bounded signal fan-out universal modules | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Title/bibliography strongly suggests universal modules, but theorem details: **UNKNOWN** | Bounded signal fan-out is explicit in title; quantitative theorem details: **UNKNOWN** | **UNKNOWN** | High-priority full-text watchlist; do not infer subsumption from title |
| **Williams 1975**, uniform decomposition of incompletely specified sequential machines | **YES**, incomplete specification | Available abstract-style secondary text says a minimal-cover search reduces copies of a universal two-state component machine: **YES**, subject to original-source verification | **UNKNOWN**; reduction is stated, extremal asymptotics not established in the current source | **UNKNOWN** | Environment-generated restriction specifically: **UNKNOWN** | **YES** in the available summary: universal two-state component copies | Fan-in/out bound: **UNKNOWN** | **UNKNOWN** | Very dangerous intersection of incomplete specification and uniform two-state decomposition; quantitative/local details require original verification |
| **Jóźwiak & Ślusarczyk 2004**, general decomposition of incompletely specified sequential machines | **YES** | General constructive decomposition: **YES** | **UNKNOWN** relative to the CCOC restricted→open benchmark | New-symbol condition: **UNKNOWN** | Networks of collaborating partial machines: **YES** | Uniform identical modules specifically: **NO/NOT REQUIRED** | Structural/interconnection constraints are part of the theory, but a CCOC-like constant-degree theorem: **UNKNOWN** | Speed is an implementation objective; exact response-query latency theorem: **UNKNOWN** | Shows incomplete-specification + constrained network decomposition is a mature general theory |
| **Centralized unlock-and-scan baseline** (CCOC audit counterexample, not prior literature) | **YES** | Trivial construction | **YES**, one-bit closed → `2^(m+1)` discrete open domain | **YES**, one `fire` | No compositional locality requirement | **NO** | **NO** | **NO** | Proves maximal one-action innovation alone is elementary and cannot carry novelty |
| **CCOC current relay** | **YES** | exact finite response quotient / explicit witness | **YES**, `1 bit → m+1 bits`, absolute maximum on `D_m` | **YES**, exactly `fire` | `m` explicit closed contexts with pre-existing routing | **YES**, constant local grammar | **YES**, max degree 3 / radius-one pairwise update | **YES**, exact narrow latency and general `Omega(log m)` causal-cone order bound | Residual novelty candidate is the **simultaneous combination**, not any individual column |

---

## 3. Sources that materially changed the verdict

### Weiner & Hopcroft 1968

The bibliographic record is independently confirmed by the Princeton Digital
Systems Laboratory report catalog and the Proceedings of the IEEE citation.
An accessible abstract reproduction states that a **general decomposition scheme**
realizes a given synchronous sequential machine as an interconnection of
**identical two-state modules**, with module fan-in and fan-out bounded
independently of the number of states in the given machine.

This means the bounded-local / identical-small-module part of CCOC cannot be sold
as new in isolation.

### Williams 1975

DBLP confirms:

> George H. Williams, *Uniform Decomposition of Incompletely Specified Sequential
> Machines*, IEEE Transactions on Computers 24(8):840–843, 1975.

A discoverable abstract-style secondary copy says that uniform decomposition is
extended to incompletely specified sequential machines; arbitrary Moore machines
are realized using copies of a universal two-state component machine; and
incomplete specification can reduce the number of copies via a uniform-cost
minimal-cover search.

Because the detailed text was not obtained from the original IEEE source in this
audit, those detailed statements remain marked **source-verification pending**.
Nevertheless, the title + bibliographic record alone makes this a mandatory
source before claiming that CCOC uniquely combines incomplete/restricted behavior
with uniform modular realization.

### Jóźwiak & Ślusarczyk 2004

The ScienceDirect abstract and accessible article text explicitly frame
sequential-machine decomposition as representing a machine by a network of
collaborating partial machines, discuss incompletely specified machines,
implementation/interconnection constraints, information flows, speed/resource
objectives, and claim a general decomposition theory covering earlier structural
models as special cases.

This is strong evidence that the **broad** combination “incomplete specification
+ constrained network decomposition” is well-established.

---

## 4. What is still not matched by the reviewed sources

The current audit has **not** found a source that explicitly proves all of the
following in one family:

\[
|P_j|=2\ \forall j,
\qquad
|P_U|=C=2,
\qquad
|P_O|=2^{m+1},
\]

with:

- `m` separately declared fixed input-restricted contexts;
- one newly legal primitive action type;
- an absolute-maximal `m`-bit response-quotient increase;
- bounded-degree / bounded-fan-in-out independent of `m`;
- constant local state alphabet;
- pairwise radius-one dynamics;
- a fixed small global control alphabet;
- logarithmic causal access latency under the local realization.

But this is a **negative search result**, not proof of novelty.  The Williams 1975
and Weiner–Hopcroft 1968 lines make it quite plausible that a sufficiently general
classical construction can reproduce many of these features after translation.

---

## 5. Decisive next comparison

The next literature pass should no longer search broad keywords such as
“input-restricted minimization” or “uniform decomposition”; those are settled.
It should ask quantitative questions of the old constructions:

1. **Williams 1975**: how many two-state component copies are needed in the worst
   case as incompleteness is removed? Can defining one previously unspecified
   input transition force an exponential increase in required copies?
2. **Weiner–Hopcroft 1968 / Newborn–Arnold 1972**: what is the module count,
   network diameter/depth, and control/input overhead when compiling an `n`-state
   machine? Does the construction preserve a constant external alphabet and
   logarithmic information-access depth?
3. **Kim–Newborn descendants**: is there a published worst-case family with an
   `O(1)` context-minimal machine but an unrestricted minimum of `2^m` states, and
   can the restriction change by only one primitive input symbol or transition
   family?
4. **General decomposition / don’t-care synthesis**: do any constructions make
   the above state gap while keeping component state count and fan-in/out bounded
   uniformly?

If the answer is yes, CCOC should be repositioned as a particularly clean causal-
interface/ecological synthesis of classical results. If the quantitative package
remains absent, that **extremal package**, not the underlying compression idea,
may support a theorem novelty claim.

---

## 6. Manuscript wording now allowed

Safe wording:

> Classical sequential-machine theory already establishes state minimization
> under input restrictions and uniform bounded-fan-in/out modular realization.
> Our remaining theoretical question is quantitative: whether an extremal
> closed-to-open response-complexity jump can be achieved while those constraints
> hold simultaneously. We give an explicit family attaining the finite-domain
> maximum under a degree-three local realization; we have not yet established a
> priority claim for that combined extremal construction.

Unsafe wording:

> “No prior theory shows that open composition destroys finite-state compression.”

> “This is the first bounded-local realization of a large finite-state machine.”

> “One newly legal action causing maximal interface inflation is itself new.”

---

## 7. Evidence status

### Strong / primary-or-authoritative support

- DBLP / Princeton catalog for Weiner–Hopcroft 1968 bibliographic record.
- IBM Research abstract for Arnold–Tan–Newborn 1970.
- DBLP for Williams 1975 bibliographic record.
- ScienceDirect full abstract/article snippets for Jóźwiak–Ślusarczyk 2004.
- Larrauri–Bloem 2021 full text for the Kim–Newborn historical attribution.

### Secondary / must verify before quoting as a theorem

- the detailed Williams 1975 abstract-style text currently surfaced through an
  Academia mirror;
- the Weiner–Hopcroft abstract reproduction currently surfaced through a research
  profile/search index.

The matrix intentionally keeps `UNKNOWN` wherever the reviewed evidence does not
support a condition. This is a novelty-control document, not an argument from
silence.
