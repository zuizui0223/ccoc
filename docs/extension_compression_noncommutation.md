# Extension–Compression Noncommutation Theorem

## Headline

A simple causal macro-law for every *fixed* closed ecological connection does
not imply a simple macro-law that remains correct under all future permitted
connections.

\[
\boxed{
\text{simple law in every closed context}
\not\Rightarrow
\text{simple extension-stable law for the open system.}
}
\]

The gap can occur with a constant local grammar, pairwise messages only, and
bounded degree. It is driven by separately addressable dormant modules, not by
higher interaction order or an increasingly complicated local rule.

## Exact interface memory

For a finite deterministic controlled system \(\mathcal M=(S,A,T,h)\) and a
declared legal-word grammar \(\mathcal L\), define

\[
s\equiv_{\mathcal L}s'
\iff
\forall w\in\mathcal L,
\operatorname{Tr}(s,w)=\operatorname{Tr}(s',w).
\]

The quotient \(S/\!\equiv_{\mathcal L}\) is the coarsest exact causal interface,
and

\[
K_{\mathcal L}=\log_2|S/\!\equiv_{\mathcal L}|.
\]

Grammar enlargement only refines the quotient:

\[
\mathcal L_1\subseteq\mathcal L_2
\Longrightarrow
K_{\mathcal L_1}\le K_{\mathcal L_2}.
\]

## Addressable-completion product lower bound

Suppose a reachable product subsystem is

\[
S^*\cong I\times E_1\times\cdots\times E_q.
\]

Assume a legal base word \(r_0\) decodes \(i\in I\), and for every module
\(j\), a legal future boundary word \(r_j\) decodes \(e_j\in E_j\),
independently of all other product coordinates.

For two distinct product states, either the inside coordinates differ and
\(r_0\) separates them, or some exterior coordinate differs and its \(r_j\)
separates them. Thus the open trace quotient is discrete on \(S^*\):

\[
\boxed{
K_{\mathrm{open}}
\ge
\log_2|I|+\sum_{j=1}^q\log_2|E_j|.
}
\]

This is an injection proof from concrete future read words and decoders—not a
partition-counting convention.

## Closed-context factorization and the main inequality

Fix a context \(j\). If every trace allowed in that closed context factors
through

\[
(i,e_1,\ldots,e_q)\mapsto(i,e_j),
\]

and the base word plus the module-\(j\) word distinguish those two coordinates,
then

\[
K_{\mathrm{closed},j}
=
\log_2|I|+\log_2|E_j|.
\]

Therefore

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

This is the **Extension–Compression Noncommutation Inequality**.

## Sharp bounded-degree binary family

For \(|I|=2\), \(|E_j|=2\), and \(q=m\),

\[
K_{\mathrm{closed},j}=2,
\qquad
K_{\mathrm{open}}\ge m+1,
\qquad
\Delta\ge m-1.
\]

The existing relay-tree family attains equality:

\[
\boxed{
K_{\mathrm{open}}=m+1,
\qquad
K_{\mathrm{closed},j}=2,
\qquad
\Delta=m-1.
}
\]

It compiles the binary witness into a balanced tree with one repeated finite
local grammar, directed pairwise child-to-parent messages, a sequential reader
attachment, and maximum degree three. Its macro probe is exactly conjugate to
reading one dormant module into the focal output.

Hence the linear gap remains even though the local grammar does not grow with
\(m\).

## Relation to the adaptive closure no-go

The adaptive finite-experiment theorem is epistemic: without a uniform delay and
finite boundary contract, no finite adaptive transcript proves exterior closure.
The present theorem is structural: once distinct dormant modules are legal future
boundary reads, each independently addressable module forces interface memory.

## Ecological projection

A module \(E_j\) can represent a future-connectable source population, delayed
mutualist, pathogen reservoir, dispersal route, neighboring community, or habitat
connection. A fixed community may expose only one module and therefore admit a
small macro-law. A law meant to survive future additions/removals/reconnections
must preserve every module that can later be independently exposed.

\[
\boxed{
\text{Open ecological composition can destroy macro-law portability}
\text{ even when local interaction grammar remains simple.}
}
\]

The relay tree is a sharp finite witness, not a literal claim that real
ecosystems are binary relay trees.