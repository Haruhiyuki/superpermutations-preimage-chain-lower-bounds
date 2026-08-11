# A uniform score-`2(n-2)` non-standard kernel

## Statement

For every target order `n ≥ 8`, put `m=n-1` and consider the palindromic kernel word

\[
K_n=m^{m-2}(m-2)m^4(m-2)m^{m-2}.
\]

In Houston's notation this is

\[
(n-1)^{n-3}(n-3)(n-1)^4(n-3)(n-1)^{n-3}.
\]

Examples are

```text
n=8:  7777757777577777
n=9:  888888688886888888
n=10: 99999997999979999999
```

The kernel is self-avoiding and has score exactly `2(n-2)`.

This supplies a uniform kernel with precisely the score required for a gain-two upper bound. It
does **not** by itself prove such an upper bound: one must still complete the kernel by a rooted
exact cover of the remaining cyclic classes.

## Residual dynamics

As in Egan's `KernelFinder`, work on permutations of `m=n-1` symbols. Let `R=T₁` be left rotation.
A positive kernel digit `d` visits

\[
p,Rp,\ldots,R^{d-1}p
\]

and leaves the block at `T₂R^{d-1}p`.

For a full digit `m`, the macro-map is

\[
A=T_2R^{-1},
\qquad
A(x_1,\ldots,x_m)=(x_2,\ldots,x_{m-1},x_1,x_m).
\]

For the short digit `m-2`, the macro-map is

\[
B=T_2R^{m-3},
\]

\[
B(x_1,\ldots,x_m)
=(x_m,x_1,\ldots,x_{m-3},x_{m-1},x_{m-2}).
\]

It is enough to prove that the cyclic classes at the starts of all blocks are distinct, because the
states visited inside one block are rotations of its start state.

## Explicit cyclic classes

Rotate each block start so that symbol `1` comes first.

### First phase

There are `m-1` block starts `P_j`, `0≤j≤m-2`:

\[
\widehat P_0=(1,2,\ldots,m),
\]

and, for `1≤j≤m-2`,

\[
\widehat P_j=(1,2,\ldots,j,m,j+1,\ldots,m-1).
\]

They are pairwise distinct because the position of `m` is distinct.

### Middle phase

After the first short block, the four full blocks and the second short block start in the five
classes

\[
\begin{aligned}
\widehat Q_0&=(1,2,\ldots,m-4,m-2,m-3,m,m-1),\\
\widehat Q_1&=(1,2,\ldots,m-4,m-2,m,m-3,m-1),\\
\widehat Q_2&=(1,2,\ldots,m-4,m-2,m,m-1,m-3),\\
\widehat Q_3&=(1,m-3,2,3,\ldots,m-4,m-2,m,m-1),\\
\widehat Q_4&=(1,2,m-3,3,4,\ldots,m-4,m-2,m,m-1).
\end{aligned}
\]

These are visibly distinct for `m≥7`.

### Final phase

Let

\[
D=(m-3,3,4,\ldots,m-4,m-2,m,m-1,2),
\]

and let `ρ` be left rotation of this `(m-1)`-tuple. The final `m-2` full blocks have cyclic classes

\[
\widehat R_j=(1,\rho^j D),
\qquad 0≤j≤m-3.
\]

They are pairwise distinct because `D` contains distinct symbols and the corresponding cuts of its
cyclic order are distinct.

## Pairwise separation of the three phases

For a cyclic class written with `1` first, record the ordered pair

\[
(\operatorname{pred}(1),\operatorname{succ}(1)).
\]

The final-phase classes have exactly the following pairs:

\[
(2,m-3),(m-3,3),(3,4),\ldots,(m-4,m-2),(m-2,m),(m,m-1).
\]

The first and middle phases use only

\[
(m,2),\ (m-1,m),\ (m-1,2),\ (m-3,2),\ (m-1,m-3),
\]

so no final-phase class occurs earlier.

The only first/middle ambiguity left by this neighbour invariant is between `P_j` for `j≥2` and
`Q_0,Q_1,Q_4`, all of which have pair `(m-1,2)`. Their positions of `m` force respectively
`j=m-2`, `j=m-3`, or `j=m-2`; direct comparison then distinguishes them:

* `Q_0` swaps `m-3` and `m-2` relative to `P_{m-2}`;
* `Q_1` delays `m-3` past `m` relative to `P_{m-3}`;
* `Q_4` has third entry `m-3`, whereas `P_{m-2}` has third entry `3`.

Since `m≥7`, all these symbols are distinct. Therefore every block cyclic class is distinct, and
`K_n` is self-avoiding for every `n≥8`.

## Score

The kernel has

* `2m` full digits;
* two digits of length `m-2`;
* `2m+2=2n` parts;
* `2m^2+2m-4` visited residual permutations.

The Houston score is therefore

\[
\begin{aligned}
\operatorname{score}(K_n)
&=(2m^2+2m-4)-(m-1)(2m+2)\\
&=2m-2\\
&=2(n-2).
\end{aligned}
\]

## Conditional gain-two consequence

The complete-2-cycle completion formula subtracts

\[
\frac{\operatorname{score}(K_n)}{n-2}=2
\]

from the Williams/Egan value. Hence, if `K_n` admits a rooted exact-cover completion for every
`n≥8`, then

\[
S(n)\le n!+(n-1)!+(n-2)!+(n-3)!+n-5.
\]

The remaining theorem is thus cleanly isolated:

> **Uniform completion problem.** Prove that the cyclic classes outside `K_n` can be partitioned by
> oriented complete 2-cycle rows whose parent graph is rooted in `K_n`.

The accompanying checker validates the dynamics and score without factorial search. It has been
run for every `8≤n≤100`; this computation supports but is not needed by the symbolic proof above.
