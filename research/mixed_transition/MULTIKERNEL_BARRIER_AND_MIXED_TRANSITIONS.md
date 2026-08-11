# The complete-2-cycle barrier and the mixed-transition route

## 1. Setup

For a permutation `p=(x₁,…,xₙ)`, write

\[
T_k(p)=(x_{k+1},\ldots,x_n,x_k,\ldots,x_1).
\]

The edge has weight `k`. The all-`T₁` successor consists of the `(n-1)!` cyclic classes. Let

\[
V=(n-1)!.
\]

The verified Egan/Hunter construction changes selected `T₁` successors to `T₂`, grouped into
complete 2-cycles, and then opens the remaining components and joins them by higher-weight edges.

## 2. Balance forces complete 2-cycles

Let `D⊆S_n` and define

\[
F_D(p)=\begin{cases}
T_2(p),&p\in D,\\
T_1(p),&p\notin D.
\end{cases}
\]

Because `T₁` and `T₂` are permutations of `S_n`, `F_D` is bijective if and only if

\[
T_2(D)=T_1(D).
\]

Equivalently, `D` is invariant under

\[
\Phi=T_1^{-1}T_2.
\]

Direct calculation gives

\[
\Phi(a,b,u_1,\ldots,u_{n-2})=(a,u_1,\ldots,u_{n-2},b).
\]

Hence `Φ` fixes the first symbol and cyclically rotates the remaining `n-1` symbols. Every orbit
has length `n-1`, and the orbits are exactly the complete 2-cycle rows indexed by a pivot and a
cyclic ordering of the other symbols.

**Balance theorem.** Every bijective successor using only `T₁` and `T₂` selects a union of complete
2-cycle rows. Thus abandoning complete rows while retaining only weights one and two is
impossible; mixed transition weights are necessary.

## 3. Weight-three splice runs have period `n-2`

Suppose a component cut at `p_i` is joined to the next component cut at `p_{i+1}` by a weight-three
edge. The start of the next opened 2-cycle is `T₂(p_{i+1})`, so

\[
T_3(p_i)=T_2(p_{i+1}).
\]

Therefore

\[
p_{i+1}=\Psi(p_i),\qquad \Psi=T_2^{-1}T_3.
\]

For `p=(a,b,c,u_1,…,u_{n-3})`,

\[
\Psi(p)=(a,b,u_1,\ldots,u_{n-3},c).
\]

Thus `Ψ` fixes the first two symbols and cyclically rotates the last `n-2` symbols. Its period is
exactly `n-2` when those symbols are distinct.

**Splice-period theorem.** A run of distinct kernel components joined only by weight-three edges has
length at most `n-2`.

This explains why every attempted chain of two standard kernel packets fails: after `n-2` steps the
cut state returns to the same `Ψ`-orbit.

## 4. Gain one is optimal in the forest-plus-splice paradigm

Consider a rooted forest of complete 2-cycle rows with

* `h` deficient kernel rows, hence `h` opened components;
* `a` complete attachment rows;
* `T=a+h` total selected rows.

Rooted exact coverage gives

\[
h(n-1)+a(n-2)=V,
\]

and therefore

\[
T=\frac{V-h}{n-2}.
\]

For `n≥4`, `V` is divisible by `n-2`, so `h=q(n-2)` for an integer `q≥1`.

The internal path weight is

\[
n!+a(n-1)+h(n-3)
   =n!+(n-1)T-2h.
\]

Joining the `h` components requires `h-1` seams. If all seams had weight three, the splice-period
theorem would allow at most `n-2` components in one run. Consequently at least `q-1` seams have
weight at least four. If `E` denotes the total excess over weight three, then

\[
E\ge q-1.
\]

The resulting word length satisfies

\[
\begin{aligned}
L
&\ge n+n!+(n-1)T-2h+3(h-1)+(q-1)\\
&=n+n!+(n-1)\frac{V-h}{n-2}+h+q-4\\
&=n!+(n-1)!+(n-2)!+(n-3)!+n-4.
\end{aligned}
\]

The right-hand side is exactly the verified gain-one upper bound.

**Paradigm barrier.** No construction consisting solely of a rooted complete-2-cycle forest whose
opened components are joined by ordinary overlap seams can improve gain one. Adding another
packet saves one selected row but forces at least one additional unit of splice cost.

This barrier is structural and holds for general `n`; it is not inferred from the degree-eight
experiment.

## 5. The correct general object: mixed-transition circulations

A successor with transition choice

\[
\kappa:S_n\to\{1,2,3,\ldots\},\qquad F_\kappa(p)=T_{\kappa(p)}(p),
\]

is admissible when `F_κ` is a permutation of `S_n`. Its excess over the all-`T₁` cover is

\[
C(\kappa)=\sum_{p\in S_n}(\kappa(p)-1).
\]

If `F_κ` is a single cycle, deleting an edge of weight `r` gives a superpermutation word of length

\[
n+n!+C(\kappa)-r.
\]

The bijectivity constraint is a perfect-matching or circulation condition in the bipartite Cayley
graph with allowed edges `p→T_k(p)`. Complete 2-cycles are merely the monochromatic `k=2` cycles
of this exchange graph.

### Alternating exchange cycles

Given a current bijective successor `F`, choose sources `p₁,…,p_m` and transition weights
`k₁,…,k_m` satisfying

\[
T_{k_i}(p_i)=F(p_{i+1})
\]

with indices cyclically interpreted. Replacing the old outgoing edges of the `p_i` by these new
edges preserves bijectivity automatically. The exact cost change is

\[
\Delta=\sum_i k_i-\sum_i w_F(p_i).
\]

The cycle-joining effect is read from the components of `F` met by the exchange cycle. This gives a
certificate format suitable for SAT/ILP search and later Lean verification.

## 6. Target theorem for a genuine general improvement

A useful scalable gadget must do more than add another standard kernel. One sufficient target is a
family of alternating exchange cycles that, for every sufficiently large `n`, merges `r_n` current
components while paying strictly less than one unit per additional component beyond the first:

\[
\Delta_n\le r_n-2.
\]

Inserted recursively into the gain-one lift, such a gadget would produce an unbounded gain over the
current construction. A stronger family with `r_n` of factorial size would begin to reduce the
coefficient of the `(n-3)!` term.

The immediate research task is therefore:

1. formulate mixed-transition exchange certificates independently of any fixed `n`;
2. search for symbol-stable gadgets rather than isolated words;
3. require a lifting law from degree `n` to degree `n+1`;
4. verify the finite gadget algebra with a small checker and then in Lean;
5. derive the resulting recurrence and asymptotic upper bound.

## 7. Degree-eight diagnostic

The verified gain-one certificate at `n=8` contains three relabelled standard-kernel packets among
its attachment rows. One packet admits a balanced exact-cover promotion:

* promote 6 rows to a second kernel;
* delete 5 owner rows;
* insert 4 replacement rows;
* retain rooted exact coverage;
* obtain 12 kernel rows, 826 attachments, and 838 total rows.

The row ledger would correspond to length `46203` if the 12 components admitted the required cheap
splice. They do not: the two packets lie in distinct `Ψ`-orbits, and there is no direct cut-state
path joining all 12 components even when all overlap weights are allowed. Accordingly, no new
upper bound is claimed.

The value of the experiment is diagnostic: it isolates the sole remaining obstruction as the
mixed-transition circulation problem predicted by the general barrier theorem.
