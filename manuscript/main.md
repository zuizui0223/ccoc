# Causal Compression under Open Composition

> Working manuscript. Primary target lane: *Theoretical Ecology*.

## Abstract

Ecological models routinely compress many micro-configurations into the same coarse state under a fixed set of future possibilities. We ask when such compression remains valid after the set of legally possible future interactions is enlarged. For finite deterministic controlled systems, we define exact response equivalence relative to a declared grammar of legal future actions. This makes state compression explicitly contract-relative: two configurations may be equivalent under one future grammar and distinguishable under another. We prove a cross-grammar lower bound showing that independently future-addressable exterior coordinates force retained interface information, even when every fixed closed context factors through a small summary. We then give an explicit family in which the exact closed response quotient has only two classes while opening one previously illegal primitive action makes the open quotient discrete on \(2^{m+1}\) states, increasing exact response memory by \(m\) bits and saturating the finite-domain maximum. The same separation is realized with a fixed four-symbol action alphabet, bounded local state and message alphabets, pairwise radius-one dynamics, maximum degree three, and logarithmic causal access. A complementary sufficient theorem identifies when a finite macro-law remains portable under grammar expansion. Ecologically, the results formalize a distinction between present functional equivalence and open-future causal equivalence: latent differences that are irrelevant under all currently allowed interactions can become state-defining once colonization, reconnection, dispersal access, or rewiring makes them addressable. The results are theorem-first and conditional on a declared finite model contract; they do not infer that contract from empirical data.

## 1. Ecological question

Ecology depends on state reduction. Communities that differ in species identities, interaction histories, demographic details, or local configuration are routinely treated as instances of the same functional state when those differences are judged irrelevant to the process under study. This compression is scientifically useful only if the distinctions that are discarded remain irrelevant to the future questions for which the coarse state is used.

The difficulty is that ecological futures are not fixed once and for all. A patch that is effectively isolated today may later receive a colonist. A habitat connection may reopen. A mutualist, pathogen, predator, or dispersal source that is currently absent may become reachable. Interaction structure can be rewired without changing every local state variable at the moment of reconnection. These changes do not merely alter parameter values inside an already declared future; they can enlarge the set of future operations through which previously dormant differences can affect a focal ecological response.

This paper isolates that structural issue. We hold the underlying controlled system fixed and change only the declared grammar of legal future actions. We ask whether an exact state compression that is valid in each restricted or closed future remains comparably small after those futures are opened.

The central distinction is

\[
\boxed{
\text{present or closed-context functional equivalence}
\;\not\Rightarrow\;
\text{open-future causal equivalence}.
}
\]

The statement does not mean that every open system is irreducibly complex. Nor does it claim that context-dependent state minimization is itself new. The narrower quantitative question is how large the exact response-interface penalty can become when the physical system is held fixed and only the legal future grammar is enlarged.

### 1.1 State identity depends on the future contract

Suppose two global configurations currently produce the same focal output. Under a restricted future in which only one interaction pathway can ever be activated, the configurations may remain indistinguishable for every legal future word. An exact model for that restricted task may therefore merge them. If a larger future grammar later allows another pathway to be selectively exposed, the same pair may cease to be mergeable.

The point is not that the earlier compression was wrong. It was exact for its declared contract. What changes is the set of counterfactual futures the coarse state must preserve. In this sense, opening the future can turn previously ignorable ecological differences into required state information.

We represent this explicitly by separating three objects:

1. a finite controlled system describing the available state transitions and focal output;
2. a grammar specifying which future action words are legally admissible;
3. the exact response interface induced by that pair.

This lets us distinguish complexity of the local transition rules from complexity forced by future addressability. The main construction keeps the local rule, action alphabet, graph degree, and local alphabets uniformly bounded while the exact open response memory grows without bound.

### 1.2 What “open composition” means here

“Open” is used in a deliberately formal sense. It does not mean that the model contains every imaginable ecological event. It means that a declared open grammar permits future actions or connections that are not legal in the closed comparison grammar. The theorem is therefore always relative to an explicit future contract.

Possible ecological readings of such an expansion include making a previously inaccessible source population reachable, reconnecting a habitat, admitting a new interaction partner, allowing a delayed reservoir to affect the focal system, or enabling a rewired pathway. These readings motivate the mathematics; they are not empirical claims that a particular field system satisfies the construction.

### 1.3 Scope

All headline results concern declared finite deterministic controlled systems. The executable certificates verify finite witnesses and regression properties. They do not establish the quantified analytic theorems by themselves and do not validate an observed ecosystem. In particular, the paper does not infer the correct state space, future grammar, completion family, or interpretation map from data. Those are parts of the model contract to which the theorems are applied.

## 2. Exact grammar-aware response interfaces

### 2.1 Controlled system and legal future grammar

Let

\[
\mathcal M=(S,A,T,h)
\]

be a finite deterministic controlled system. Here \(S\) is the finite state space, \(A\) the primitive action alphabet, \(T\) the controlled transition rule, and \(h:S\to Y\) the focal output.

A legal future grammar \(\mathcal L\subseteq A^*\) specifies which finite action words count as admissible futures for the scientific task under consideration. In the implementation, grammars are represented by finite prefix-closed action automata so that legality may depend on the current grammar state, but the response-equivalence idea can be written directly in terms of legal words.

For a state \(s\in S\) and a legal word

\[
w=a_1a_2\cdots a_t,
\]

let

\[
\operatorname{Tr}(s,w)
\]

denote the focal output trace along that controlled trajectory, including the current output and the outputs after each action.

### 2.2 Exact response equivalence

Two states are exactly response-equivalent under grammar \(\mathcal L\) when every legal future word produces the same focal trace:

\[
\boxed{
s\equiv_{\mathcal L}s'
\iff
\forall w\in\mathcal L,
\operatorname{Tr}(s,w)=\operatorname{Tr}(s',w).
}
\]

The quotient

\[
Q_{\mathcal L}=S/\!\equiv_{\mathcal L}
\]

is the coarsest exact deterministic response interface for that contract. Its exact memory requirement is

\[
K_{\mathcal L}=\log_2|Q_{\mathcal L}|.
\]

This fixed-grammar quotient is foundational machinery rather than a historical novelty claim. Its role here is to make the closed/open comparison precise.

### 2.3 Grammar enlargement and response refinement

When every future legal under \(\mathcal L_1\) is also legal under \(\mathcal L_2\), any pair that remains indistinguishable under the larger grammar is necessarily indistinguishable under the smaller one. Hence

\[
\mathcal L_1\subseteq\mathcal L_2
\quad\Longrightarrow\quad
\equiv_{\mathcal L_2}\subseteq\equiv_{\mathcal L_1}
\]

and therefore

\[
\boxed{
K_{\mathcal L_1}\le K_{\mathcal L_2}.
}
\]

The monotonicity itself is elementary. The substantive question is whether the increase can be large when the smaller grammars each admit strong compression and the physical implementation remains locally simple.

## 3. Cross-grammar compression gap

### 3.1 Operationally addressable exterior coordinates

Consider a reachable comparison subsystem with product form

\[
S^*\cong I\times E_1\times\cdots\times E_q,
\]

where \(I\) is a focal or inside coordinate and \(E_j\) are exterior coordinates that may represent dormant future-connectable modules.

We call an exterior coordinate operationally addressable under the open grammar when a concrete legal future word can recover that coordinate from the focal response. Formally, suppose there is a base word \(r_0\) whose trace decodes \(i\in I\), and for each \(j\) there is a legal open word \(r_j\) and decoder \(d_j\) such that

\[
d_j\!\left(
\operatorname{Tr}((i,e_1,\ldots,e_q),r_j)
\right)=e_j
\]

for every jointly realizable comparison state. The decoder for one module must work independently of the values of the other coordinates.

The condition is operational rather than merely combinatorial: each distinction counted in the lower bound has an explicit legal future experiment that can expose it.

### 3.2 Addressability lower bound

Take two distinct states in \(S^*\). If their inside coordinates differ, \(r_0\) separates them. Otherwise they differ in at least one exterior coordinate \(E_j\), and \(r_j\) separates them. Thus every distinct pair is distinguishable under the open future grammar. The exact open response quotient is therefore discrete on the comparison subsystem, which gives

\[
\boxed{
K_{\mathrm{open}}
\ge
\log_2|I|
+
\sum_{j=1}^q\log_2|E_j|.
}
\]

The proof is an injection argument from concrete legal future reads. Each independently future-readable coordinate forces the interface to retain the distinction needed to answer that future probe.

### 3.3 Closed-context factorization

Now fix one closed context \(j\). Suppose every trace legal in that context factors through only the focal state and the single exposed module,

\[
(i,e_1,\ldots,e_q)
\mapsto
(i,e_j),
\]

and suppose the closed grammar can distinguish the two retained coordinates. Then

\[
K_{\mathrm{closed},j}
=
\log_2|I|+
\log_2|E_j|.
\]

Combining the closed factorization with the open addressability lower bound yields

\[
\boxed{
K_{\mathrm{open}}
-
\max_jK_{\mathrm{closed},j}
\ge
\sum_{j=1}^q\log_2|E_j|
-
\max_j\log_2|E_j|.
}
\]

For binary \(I\) and binary exterior modules \(E_j\), with \(q=m\), every fixed closed context needs only two bits while the open interface needs at least \(m+1\) bits. Thus

\[
K_{\mathrm{open}}
-
\max_j K_{\mathrm{closed},j}
\ge m-1.
\]

This is the structural closed/open separation: individually small exact closed descriptions do not imply a comparably small exact description that survives the declared open future.

### 3.4 Constrained codebooks

The full Cartesian product is not essential to the argument. The current strengthening replaces it by an arbitrary finite jointly realizable comparison codebook. If the legal open future words separate every pair of codewords, the exact open quotient on that codebook is discrete. Closed projections can still be much smaller than the codebook itself.

This matters for the ecological interpretation because independently stored exterior possibilities need not occur in every formal combination. Strong global constraints among configurations can reduce the realizable set without removing the basic mechanism: if the remaining configurations are still separated by future addressability, a large open-interface requirement persists.

The codebook result is used as a robustness of assumptions, not as an additional headline theorem.

## 4. An extremal one-action family

The general lower bound shows why addressable exterior differences force memory. We next show that the gap can be maximized while keeping the grammar edit and local implementation simple.

For every integer \(m\ge1\), consider comparison states

\[
D_m=\{0,1\}^{m+1}
=\{(y,b_1,\ldots,b_m)\}.
\]

The focal bit \(y\) is immediately observable. The \(m\) bits \(b_j\) are dormant exterior memories. The controlled system uses one fixed primitive action alphabet

\[
A=\{0,1,\mathsf{fire},\mathsf{tick}\}.
\]

The underlying transition system is the same in both comparisons. Only action legality changes.

### 4.1 Closed and open grammars

The closed grammar permits

\[
L_C=\{0,1,\mathsf{tick}\}^{*},
\]

whereas the open grammar permits

\[
L_O=A^*.
\]

Opening therefore adds exactly one primitive legal transition: `fire` becomes available. The address actions `0` and `1`, and the propagation action `tick`, are already legal in the closed regime.

Under closed actions, no pulse can be emitted from the dormant memory leaves. Addressing may move a selector, but it does not change the focal output or reveal any \(b_j\). Consequently every closed trace depends only on \(y\). The exact closed quotient therefore has

\[
\boxed{
|P_C|=2,
\qquad
K_C=1.
}
\]

### 4.2 Opening one primitive action exposes every dormant bit

After `fire` becomes legal, each exterior coordinate can be queried. Let \(a_j\in\{0,1\}^{d_j}\) be the address of leaf \(j\) in the relay tree. The canonical open word

\[
w_j
=a_j\,\mathsf{fire}\,\mathsf{tick}^{d_j+1}
\]

selects leaf \(j\), emits its stored bit as a pulse, and propagates that pulse back to the focal output. Thus

\[
\operatorname{finaloutput}(s,w_j)=b_j.
\]

If two comparison states have different \(y\), the current output separates them. If they have the same \(y\) but differ in any \(b_j\), the corresponding \(w_j\) separates them. Hence the open response quotient is discrete:

\[
\boxed{
|P_O|=2^{m+1},
\qquad
K_O=m+1.
}
\]

The grammar expansion therefore creates

\[
\boxed{
K_O-K_C=m
}
\]

bits of exact open-only response memory.

Because a two-class quotient on a domain of size \(2^{m+1}\) can gain at most \(m\) bits before becoming discrete, the construction saturates the absolute finite-domain upper bound. There is no remaining memory slack in the declared comparison.

### 4.3 Why this is not merely a large action alphabet construction

The primitive action alphabet is fixed at four symbols for all \(m\), and the closed/open grammar descriptions are constant size. The result therefore does not arise by giving every new exterior coordinate its own primitive action name. The same addressing grammar is reused as the system grows; what scales is the amount of dormant state that a legal future can navigate to and expose.

## 5. Bounded-local sharpness realization

A centralized decoder could trivially store all \(m\) exterior bits and reveal them on demand. That would leave open whether the separation is merely an artifact of global access or a large local rule. The relay construction removes that explanation.

### 5.1 Local architecture

The exterior memory sites are leaves of a balanced binary relay tree. A focal `ROOT` sits above the relay-body root. Address symbols move a selector locally down the tree. `fire` emits a pulse only at the selected memory leaf. Each global action advances pulse propagation by one radius-one synchronous round. Internal relays combine child pulses by one fixed local Boolean rule.

The interaction graph remains a tree. Maximum degree is at most three. The focal node is separated from the entire exterior relay body by a single edge. Local node-state alphabets and message alphabets are bounded independently of \(m\).

Thus the growing exact response memory cannot be attributed to increasing local interaction order, an expanding primitive control alphabet, increasing degree, or a widening focal/exterior graph cut.

### 5.2 Access length

In a midpoint-balanced tree, the deepest leaf has depth

\[
H(m)=\lceil\log_2m\rceil.
\]

A query to a leaf at depth \(d_j\) uses \(d_j\) address actions, one `fire`, and \(d_j+1\) propagation ticks. Therefore the worst canonical read has length

\[
\boxed{
L_{\mathrm{query}}^{\mathrm{worst}}
=2\lceil\log_2m\rceil+2.
}
\]

A separate local causal-cone bound shows that exposing exponentially many exact focal response classes in a bounded-degree, bounded-local-state, radius-one system requires at least logarithmic horizon order. The relay therefore has order-optimal \(\Theta(\log m)\) access under that broader local contract, although its exact coefficient and additive constant are architecture-specific.

### 5.3 A narrow physical boundary does not bound exact causal memory

Within the explicit family, focal/exterior edge cut width remains one and the network remains a tree while the exact open response memory grows as \(m+1\) bits. Consequently bounded degree, tree topology, bounded local alphabets, a one-edge physical cut, and a one-transition grammar edit do not by themselves provide a universal upper bound on exact open response-interface inflation.

This is a mathematical corollary of the constructed family. It is not a claim that a narrow ecological corridor or sparse real interaction network necessarily realizes the same memory structure.

### 5.4 Historical-claim boundary

The relay is used here as an explicit constrained extremal and sharpness realization. We do not claim historical firstness for bounded-local sequential-machine compilation, fixed modular synthesis, contextual minimization, or generic state-reduction noncommutation. The scientific burden of the construction is narrower: it shows directly, within the declared comparison contract, that the maximal closed/open response gap is compatible with uniformly simple local implementation.

## 6. When a macro-law does remain portable

The negative theorem does not imply that grammar expansion always destroys a coarse law. A complementary sufficient result identifies a constructive positive boundary.

Consider a nested sequence of finite grammar-aware controlled systems. Suppose every stage projects to the same finite macrostate set \(Q\), with the same macro output \(\bar h\), legal-action rule, and macro transition rule \(\bar T\). Suppose further that embeddings from an earlier stage into a later one preserve the macro label of every old state.

Then every stage realizes the same exact macro dynamics. Old trajectories retain their macro meaning after extension, and the compatible finite-stage laws define one portable macro-law across the nested chain.

Schematically,

\[
\boxed{
\text{common finite macro dynamics}
+
\text{trajectory-preserving embeddings}
+
\text{label coherence}
\Rightarrow
\text{one extension-portable macro-law}.
}
\]

This sufficient condition is stronger than merely bounding the number of coarse labels. Having, for example, three labels at every stage is not enough if those labels change output meaning or transition semantics after extension.

The corresponding local obstruction is immediate. If two old states are merged by a proposed macrostate, remain merged after embedding, but a newly legal future word produces different focal traces from their images, then that proposed merge cannot belong to an exact portable macro-law. The future word is an explicit certificate of why the old equivalence failed.

The positive and negative results therefore meet at the same conceptual boundary: future expansion is harmless exactly in examples where newly legal behavior continues to factor through the old macro semantics; it forces refinement when it exposes distinctions internal to an old macro fiber.

## 7. Ecological interpretation

### 7.1 Dormant differences can become state variables

The formal exterior coordinates \(E_j\) or \(b_j\) can be read as dormant differences among globally possible ecological configurations. Examples include the state of a future-connectable source population, a delayed mutualist, a pathogen reservoir, an inaccessible dispersal branch, or a neighboring community whose influence is currently blocked.

Under a fixed closed context, most of these coordinates may never affect the focal response. An exact closed model can legitimately ignore them. Once the declared future allows those pathways to be selectively activated, the same distinctions can become necessary to predict the focal response. The theorem therefore concerns when state variables must change with the future interaction contract, not when one static list of ecological variables is universally sufficient.

### 7.2 Colonization, reconnection, dispersal, and rewiring

A colonization event can be represented not only as a change of current state but also as the opening of future interactions that were previously unavailable. The same is true of corridor restoration, reconnection among patches, arrival of a new interaction partner, or network rewiring. From the present perspective, the important question is whether the newly reachable future can independently expose differences that the old model had merged.

If it cannot—because all new behavior remains uniform within old macrostates—the positive portability condition can hold. If it can, some old equivalence is invalid for the enlarged task. When many independently addressable dormant distinctions exist, the exact interface cost can accumulate rather than being captured by a single generic “open-system” flag.

### 7.3 Functional redundancy is contract-relative

Two configurations can be functionally redundant with respect to every currently allowed trajectory and still fail to be redundant with respect to an enlarged future. This gives a precise sense in which redundancy is conditional on the intervention or composition grammar used to define function.

The result should not be read as denying useful functional groups or coarse ecological variables. It identifies what must be checked before exporting them to a broader future contract: the proposed merge must remain invariant under the newly legal responses one intends the model to support.

### 7.4 What is not established empirically

The relay tree is a finite sharpness witness, not a literal ecosystem. The theory does not estimate the number of dormant ecological coordinates in a field system, infer which future interactions are truly legal, or show that a real community attains the extremal bound. To apply the result empirically, one would first need an independently justified model contract specifying states, outputs, admissible future interactions, and the interpretation of the response interface.

Accordingly, the ecological contribution of the theorem is diagnostic and conceptual: it separates a source of state complexity—future addressability—from local rule complexity and shows that the former can dominate exact compression even under simple local structure.

## 8. Discussion

### 8.1 The contribution is quantitative, not the slogan that context matters

State reduction under input restrictions, environment-dependent minimization, and related context-sensitive equivalence ideas have substantial classical ancestry. The paper therefore does not assign novelty to the observation that a richer set of inputs or futures can refine a state partition.

The narrower contribution is the controlled quantitative comparison used here: the same system can possess a tiny exact response interface under the closed grammar while a minimal opening of legal future behavior activates the maximum possible additional exact response distinction on the comparison domain. The explicit local construction shows that this separation survives fixed primitive controls, bounded local state, pairwise radius-one dynamics, bounded degree, and a one-edge focal/exterior cut.

A source-checked Related Work section will distinguish this claim from classical contextual minimization, incomplete-machine reduction, promise/domain restrictions, reduction/realization noncommutation, modular sequential-machine synthesis, and modern causal or compositional abstraction. Historical firstness of the relay realization is not needed for the main argument.

### 8.2 What the lower bound says about ecological state choice

The theorem suggests a practical conceptual rule for theory construction: a state summary should be judged against the futures it is expected to support. If management, restoration, invasion, reconnection, or other scientific questions enlarge those futures, the adequacy of an earlier coarse state must be re-audited rather than assumed to transfer automatically.

This does not require retaining every microscopic difference. Only distinctions that can alter some legal future response are forced into the exact interface. The positive portability theorem makes the complementary point: when newly available dynamics remain uniform within the old coarse states, the same macro-law can persist across extension.

### 8.3 Exactness and approximation

The headline theory is exact. Real ecological prediction is usually noisy and approximate, so exact distinguishability is a strong contract. The retained approximate-addressability extension addresses one limited robustness question: bounded error in coordinate-specific decoding does not automatically collapse the memory requirement to \(O(1)\). It does not constitute a complete theory of approximate ecological state abstraction, rate-distortion tradeoffs, or stochastic portability. Those remain separate questions.

### 8.4 Limitations

The current results assume finite state and action spaces, declared legal-future grammars, deterministic controlled dynamics in the headline theorem, and a chosen focal output. The framework does not decide which ecological futures should be admitted or how to learn the contract from observations. It also does not imply that every ecological extension increases interface complexity; the positive theorem gives an explicit countercase.

Finally, interface memory is only one notion of ecological complexity. The result separates response-state requirements from several local/static structural quantities in one explicit family, but it does not claim that those structural quantities are irrelevant for other questions such as stability, persistence, inference, energetic cost, or approximate prediction.

### 8.5 Next questions

The first-paper result leaves several mathematically distinct directions: approximate or stochastic portability rather than approximate addressability alone; necessity or converse conditions for delimited classes of grammar expansion; coupled tradeoffs among response memory, control, and latency; and ecological structural assumptions that would upper-bound addressability from dispersal or network constraints. These are follow-up problems rather than prerequisites for the present manuscript.

## Supplement plan

The supplement will contain:

- complete analytic proofs with theorem numbering matched to the main text;
- theorem-to-code and theorem-to-test traceability;
- finite replay specification and immutable Git provenance;
- constrained-codebook details and examples;
- bounded-local construction details and local causal-cone support;
- approximate-addressability extension as secondary material;
- source-checked Related Work audit supporting the conservative novelty boundary.
