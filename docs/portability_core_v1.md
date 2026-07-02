# Portability core v1: the canonical RACH theorem family

## One question

When does a causal macro-law remain exact after the permitted outside of a focal
window expands through new modules, new legal connections, or newly available
interventions?

RACH v1 does **not** answer every question about evidence, model uncertainty, or
field design. It establishes the structural conditions under which an exact
finite macro-law can be portable, and the operational conditions that obstruct
that portability.

## Canonical claim

\[
\boxed{
\text{A finite portable macro-law is possible only when every newly permitted
future distinction is absorbed by one finite, update-consistent macro schema.}
}
\]

The positive and negative statements below are conditional criteria. They are
not an unconditional classification of all ecological systems.

## The portability family

### Layer P0 — finite-model prerequisite

The finite closure calculus distinguishes a unique global endpoint, recurrence,
and multistability for a declared finite deterministic update system.

\[
\text{local transition specification}
\not\Rightarrow
\text{one global endpoint}.
\]

This is a prerequisite for finite-model claims, not a special theorem about open
composition.

### Layer P1 — exact dynamic factorization

For a declared grammar, a summary is exact only when it preserves current output,
enabled legal actions, and successor summary after every legal action. The
canonical grammar-aware quotient is the coarsest exact interface.

\[
\boxed{
\text{finite update-closed boundary summary}
\Rightarrow
\text{exact finite macro-interface.}
}
\]

This is the positive base result. It says a law can exist; it does not yet say
the same law survives composition changes.

### Layer P2 — addressability obstruction

For a reachable product subsystem

\[
S^*\cong I\times E_1\times\cdots\times E_q,
\]

if the declared future grammar has concrete decoder words for the inside state
and for every exterior factor, then

\[
\boxed{
K_{\mathrm{open}}
\ge
\log_2|I|+\sum_j\log_2|E_j|.
}
\]

The decoder premise is operational: any two product states that differ in one
coordinate have distinct legal future behaviour under a word that decodes that
coordinate. The resulting lower bound is an injection statement about exact
open interfaces.

For each fixed closed context \(j\), suppose a supplied exact summary factors
through \((I,E_j)\). That premise provides the closed-context **upper bound**

\[
K_{\mathrm{closed},j}
\le
\log_2|I|+\log_2|E_j|.
\]

Combining this upper bound with the open lower bound yields

\[
\boxed{
K_{\mathrm{open}}-
\max_jK_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-
\max_j\log_2|E_j|.
}
\]

This is the Extension–Compression Noncommutation Inequality. It is the central
negative structural result: a small law in every fixed closed context need not
produce one small extension-stable law. A factorization through \((I,E_j)\)
alone does not say that the closed minimal interface has exactly
\(|I||E_j|\) states; equality is a property of the explicit witness below.

The relay tree is a **sharpness witness**, not a separate headline theorem. It
attains the binary bound with a constant-size local node/message grammar,
pairwise messages, and maximum degree three. The family still has a growing set
of selectable ports, so this is not a claim of a constant-size global action
alphabet.

### Layer P3 — composition portability ladder

The three earlier modules are one theorem family, not three parallel headline
claims.

| Level | Extra premise | Conclusion |
|---|---|---|
| Boundedness | Every stage factors through a common finite summary alphabet \(Q\) | \(\sup_m K_m\le\log_2|Q|\) |
| Coherent portability | Every stage induces the same macro output, legal-action, and transition system; embeddings preserve labels | one exact macro-law is shared across the nested stages |
| Conservative extension | Legal rows may grow inside one fixed finite action alphabet, but old meanings are unchanged and a newly legal action is label-deterministic | one finite conservative macro schema remains exact on the union grammar |

The last level contains the fixed-legality case as the special case in which no
legal row grows.

The positive conclusion is therefore not merely “the quotient stays small.” It
is:

\[
\boxed{
\text{old macro meaning is preserved under every declared conservative extension.}
}
\]

### Layer P4 — concrete portability obstructions

Two obstruction forms are retained.

1. **Cumulative addressability.** If each newly attached nontrivial factor is
   jointly realizable with earlier factors and independently decoded by a future
   word, interface memory grows cumulatively.

2. **New-action fiber split.** If a newly legal action separates two states
   previously merged by a proposed macrostate, no exact conservative schema can
   retain that merge.

The second obstruction is local and concrete: it returns the old pair, the new
action or word, and the conflicting traces or successor labels.

## What portability core v1 does not claim

- It does not prove that all systems have either a bounded blanket or cumulative
  addressability. Families satisfying neither supplied premise remain
  `UNRESOLVED`.
- It does not prove that empirical ecosystems are finite deterministic systems.
- It does not turn a grammar state into a biological state by definition.
- It does not establish an evidence procedure for discovering the correct
  boundary grammar from data.
- It does not automatically combine exterior-memory and candidate-mechanism
  memory without a joint realizability and separation premise.

## Companion programs

### Identifiability companion

Delayed addressability and adaptive finite-experiment no-go answer a different
question:

\[
\text{Can finite evidence establish exterior closure?}
\]

They show that without an independently justified horizon and grammar contract,
the correct finite-evidence conclusion can be `UNRESOLVED`. This is not a premise
of the portability theorem family.

Candidate-safe and joint exterior–mechanism laws are also companion work. They
study whether retained mechanism families share one macro transition, not
whether open composition alone preserves one.

### Experimental-design shelf

Reset panels, completion coverage, cell-loss robustness, and common-mode failure
are conditional design results after a quotient, reset contract, or failure model
has already been fixed. They remain executable regressions but are not active
structural theorem targets.

## v1 stop criteria

Portability core v1 is considered complete enough to stop adding local theorem
variants when all are true:

1. The positive family is presented as one ladder rather than independent
   theorems.
2. The Extension–Compression inequality is the sole headline lower bound.
3. Relay constructions are explicitly witnesses of sharpness.
4. Delayed evidence and candidate uncertainty are documented as companion
   programs.
5. Every remaining open issue states which canonical claim it changes; a new
   special case alone is not sufficient reason to add a theorem.

See [research priorities](research_priorities.md) for the freeze policy and
repository partition plan.