# RACH theorem map: core, selected extension, companions, and frozen shelves

RACH does not treat every valid result as one long theorem chain. The repository has a frozen **portability core v1**, one selected post-v1 structural extension, an identifiability companion, and a legacy experimental-design shelf.

Read [portability core v1](portability_core_v1.md) for the canonical v1 statement, [non-nested replacement portability](non_nested_replacement_portability.md) for the selected extension, and [research priorities](research_priorities.md) for the current stop rule.

## A. Portability core v1

### A0. Finite-model prerequisite

A declared finite deterministic update system can be globally closing, recurrent, or multistable. Local transition syntax does not itself imply one endpoint.

### A1. Exact finite factorization

For a declared finite grammar, an exact interface preserves current output, enabled legal actions, and successor summary after every legal action. The legal-word quotient is the coarsest such interface.

\[
\boxed{
\text{finite update-closed boundary summary}
\Rightarrow
\text{exact finite macro-interface.}
}
\]

### A2. Extension--compression obstruction

For an addressable product subsystem

\[
S^*\cong I\times E_1\times\cdots\times E_q,
\]

with legal decoder words for the inside coordinate and every exterior factor,

\[
\boxed{
K_{\mathrm{open}}
\ge
\log_2|I|+\sum_j\log_2|E_j|.
}
\]

If fixed closed context \(j\) factors through \((I,E_j)\), then

\[
\boxed{
K_{\mathrm{open}}-\max_jK_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-\max_j\log_2|E_j|.
}
\]

The binary relay tree is the sharpness witness, attaining \(K_{\mathrm{closed},j}=2\) and \(K_{\mathrm{open}}=m+1\) with constant local grammar, pairwise messages, and degree at most three.

### A3. Nested portability ladder

| Level | Status | Premise | Conclusion |
|---|---|---|---|
| Boundedness | sufficient | common finite summary alphabet | uniform interface-size upper bound |
| Coherent portability | sufficient | same macro output/action/transition system and label-coherent embeddings | one exact macro-law across nested stages |
| Conservative extension | sufficient | fixed old meanings and label-deterministic new actions under monotone legal rows | one finite schema on the union grammar |

### A4. Local fiber-split obstruction

A newly legal action or future word that separates two states in one proposed macro fiber invalidates that proposed merge. This is a local obstruction, not a theorem that every alternative macro-law must fail.

## B. Selected post-v1 extension: non-nested replacement and rewiring

Nested embeddings need not exist after replacement, extinction, or rewiring. The selected extension uses declared total relations instead.

### B1. Transport-coherent edge preservation

If every finite stage already induces the same exact macro dynamics and each edge in a connected replacement graph has a total, label/output/legal-action preserving, successor-closed transport, one macro law is shared across the declared family. The relation may be many-to-one or one-to-many.

### B2. Transported target exact factorization

One exact source projection can construct the target projection. When a relation covers both product spaces, preserves output and equal legal-action rows, is successor-closed, and is label-consistent on every target fiber, define

\[
q_T(t)=q_S(s)\qquad ((s,t)\in R).
\]

The target label is well-defined, grammar-aware exact, and induces the same macro dynamics as \(q_S\).

### B3. Conservative transport with target-only actions

Target-only actions can be added without an embedding. A source exact projection and a total relation construct one conservative macro schema when source-legal actions remain legal and successor-closed, and every target-only action has uniform availability and one macro successor inside each derived target fiber.

The source realizes a restriction of the schema; the target realizes the expanded action rows. Thus non-nested replacement can transport conservative action growth, provided the new action does not split a macro fiber.

### B4. Local replacement obstruction

A newly legal word can split a previously carried merge. The certificate identifies the source pair, relation, future word, and target traces. This is exactly the failure mode excluded by B3's uniformity condition.

### B5. Scope boundary

Failure to supply B2 or B3 transport does not imply unbounded memory or failure of every alternative macro-law. B3 does not cover new actions with nonuniform availability or successor labels, nor stochasticity or approximate portability. Those cases remain `UNRESOLVED`.

## C. Identifiability companion

### C1. Delayed exterior exposure

For every finite adaptive policy, a delay-gated closed/open pair can agree on the complete policy transcript and separate later. Without an independent horizon and grammar contract, finite adaptive evidence yields `UNRESOLVED`, not closure.

### C2. Retained mechanism families

A candidate-universal deterministic law exists exactly when all retained candidate-induced macro maps agree on all declared actions. Joint exterior--mechanism lower bounds require their own joint realization and separation premise.

## D. Experimental-design legacy shelf

Reset panels, evidence coverage, cell-loss robustness, common-mode failures, and narrow observation-regime utilities remain executable regressions. They are conditional design results after a quotient or contract has already been fixed.

## E. Honest unresolved region

No theorem classifies every composition family. `UNRESOLVED` covers families that supply neither a finite update-consistent factorization nor an independently decoded, jointly realizable addressability product. It also includes unconstrained non-nested rewiring, noisy/approximate portability, and composition-dependent candidate mechanisms.

## F. Priority order

1. Preserve the frozen v1 core and its public claim discipline.
2. Treat B2, B3, and the newly-legal-word obstruction as the current stop point of non-nested portability.
3. Do not add another relation variant unless it changes the transport contract itself.
4. Keep candidate-dependent and approximate directions paused until a separate research decision is made.
