# R0.71P -- Simultaneous positive entries admit a spatial square-sum payment, while their temporal packing remains uncontrolled

**Date:** 2026-08-26

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, localized Littlewood--Paley frames, normalized
Hilbert directions, temporal BV, analytic zero sets, and source measures

**Status:** release source.  The report proves a finite-order positive-entry
measure theorem, a sharp simultaneous frame--cell batching estimate, a
counting-measure reduction, an abstract sequential-entry separation, and a
sharp one-sided smooth Navier--Stokes initial jet.  It proves no uniform NSE
zero count, infinite-frame estimate, Leray-level continuation criterion,
singularity, global regularity, novelty, or Millennium-problem result.

## 0. Direct decision

R0.71O identified, at every isolated finite-order zero of

\[
 C_{j,Q}(t)=\operatorname{curl}(\chi_QT_j\omega(t)),
 \qquad d_{j,Q}(t)=\|C_{j,Q}(t)\|_2^2,
\]

the right positive-entry atom

\[
 A_{j,Q,+}(t_0)
 =\frac{(\langle F_j(t_0),c_{j,Q}(t_0)\rangle^+)^2}
 {Y(t_0)\|c_{j,Q}(t_0)\|_2^2},
 \qquad F_j=T_j\mathbb P(u\times\omega),
 \qquad Y=\|\omega\|_2^2.
 \tag{0.1}
\]

The R0.71P target is

\[
 \boxed{
 \mathsf S_{\Lambda,+}(K)
 =\sum_{(j,Q)\in\Lambda}\kappa_j^{-2}
 \sum_{t_0\in\mathcal Z^+_{j,Q}(K)}
 A_{j,Q,+}(t_0),}
 \tag{0.2}
\]

first for a finite truncation \(\Lambda\), and then uniformly as the
truncation and observation interval grow.  The set
\(\mathcal Z^+_{j,Q}(K)\) contains finite-order denominator zeros with a
positive-denominator component immediately to their right.  A nonzero trace
at the left observation boundary is a separate initial term, unless that
boundary itself is a zero with a one-sided finite-order expansion.

Throughout the entry ledger, the observation window is half open,
\(K=[a,b)\).  Thus a finite-order zero at \(a\) may be an entry, whereas the
right observation endpoint is excluded.  This convention prevents an
artificial double count when adjacent windows are concatenated.

The finite decision is:

1. \(\mathsf S_{\Lambda,+}\) is the atomic mass of a **positive,
   componentwise relaxed entry measure**.  It is obtained by taking the
   positive soft face part in each shell--cell component and only then
   summing.  It is not, in general, the positive Jordan part of the signed
   aggregate.
2. It is not the positive variation of the ordinary hard representative.
   At an even-order touch the hard BV jump is zero while the segmented/soft
   entry remains positive.
3. All entries that occur at one common time are paid by bounded spatial
   overlap and the homogeneous \(\dot H^{-1}\) Littlewood--Paley square sum.
4. The complete target is bounded by that time-slice square sum integrated
   against the **distinct entry-time counting measure**, not against
   Lebesgue time.
5. A fixed finite frame--cell truncation has finite entry mass on every
   half-open window whose closure lies in a classical time-analytic interval.
6. Time analyticity supplies no uniform entry count across truncations,
   solutions, shells, cells, or intervals approaching a possible singular
   endpoint.
7. The R0.71O oscillatory Hilbert path saturates the counting-measure
   reduction while its ordinary first-time budgets remain bounded.
8. The genuine R0.71O smooth NSE initial jet has
   \(A_+=\|F\|_2^2/Y=1/4\), so the one-cell projection constant is sharp.

Thus fixed-partition **spatial batching closes**, but temporal packing does
not.  The next useful input must control entry times, positive source mass, or
a quantitative analytic nondegeneracy ratio.  It cannot be another signed
rearrangement of the already positive atoms.

## 1. Setup and declared frame assumptions

Work on the normalized periodic torus.  On a classical interval let \(u\) be
a nontrivial, zero-mean incompressible solution, let
\(\omega=\operatorname{curl}u\), and write

\[
 L=\mathbb P(u\times\omega),\qquad F_j=T_jL,
 \qquad W_j=T_j\omega.
 \tag{1.1}
\]

Then \(Y(t)=\|\omega(t)\|_2^2>0\) throughout that classical interval: if
\(Y(t)=0\), zero mean and incompressibility give \(u(t)=0\).  Forward
uniqueness makes the solution zero on the remaining forward interval, and
time analyticity then makes it zero on the connected classical interval.  The
trivial solution has no positive entries and is assigned zero mass.

The real-even, time-independent annular multipliers \(T_j\) have nominal
frequencies \(\kappa_j\).  The fixed cutoffs \(\chi_Q\) may depend on the
shell but do not move or refresh in this release.  Put

\[
 C_{j,Q}=\operatorname{curl}(\chi_QW_j),
 \qquad d_{j,Q}=\|C_{j,Q}\|_2^2,
 \qquad B_{j,Q}=\langle F_j,C_{j,Q}\rangle.
 \tag{1.2}
\]

The support family has bounded overlap

\[
 M_\chi
 =\sup_j\sup_x\sum_Q
 \mathbf 1_{\operatorname{supp}\chi_Q}(x)<\infty,
 \tag{1.3}
\]

and the declared annular family satisfies the standard upper square-function
bound

\[
 \sum_j\kappa_j^{-2}\|T_jf\|_2^2
 \le C_T\|f\|_{\dot H^{-1}}^2
 \tag{1.4}
\]

for the relevant zero-mean fields.  These are geometric properties of the
fixed frame, not regularity assumptions on the solution.

At a finite-order zero \(t_0\), write \(\tau=t-t_0\) and assume

\[
 C_{j,Q}(t_0+\tau)
 =c_{j,Q}(t_0)\tau^m+O_{L^2}(|\tau|^{m+1}),
 \qquad c_{j,Q}(t_0)\ne0,
 \tag{1.5}
\]

with the differentiated remainder used in R0.71O.  Then (0.1) is the right
trace of

\[
 a_{j,Q}
 =\left(\frac{B_{j,Q}^+}{\sqrt{Yd_{j,Q}}}\right)^2
 \tag{1.6}
\]

on the component to the right.  The left trace is

\[
 A_{j,Q,-}(t_0)
 =\frac{(((-1)^m\langle F_j(t_0),c_{j,Q}(t_0)\rangle)^+)^2}
 {Y(t_0)\|c_{j,Q}(t_0)\|_2^2}.
 \tag{1.7}
\]

The target (0.2) intentionally uses only \(A_+\).  The stronger total-Jordan
sum \(A_++A_-\), moving cutoffs, and refresh atoms remain outside this
release.

## 2. Segmented positive variation is not ordinary hard BV

Fix \(K=[a,b)\).  For every connected component of
\(\{d_{j,Q}>0\}\cap K\), extend the restricted branch by zero at its two
observation-side endpoints, and call the sum of their positive variations
\(V^+_{\rm seg}(a_{j,Q};K)\).  If \(d_{j,Q}(a)>0\), this convention creates
the declared initial trace

\[
 I^+_{j,Q}(K)=a_{j,Q}(a+).
 \tag{2.0}
\]

Otherwise put \(I^+_{j,Q}(K)=0\).  In particular, if \(a\) itself is a
finite-order zero with a positive-denominator component to its right, its
mass is an entry atom in \(\mathcal Z^+_{j,Q}(K)\), not an initial trace.

### Theorem 2.1 -- exact positive-entry decomposition

Under the R0.71O finite-order hypotheses,

\[
 \boxed{
 V^+_{\rm seg}(a_{j,Q};K)
 =\sum_{J\in\operatorname{Comp}(\{d_{j,Q}>0\}\cap K)}
 V^+(a_{j,Q};J)
 +I^+_{j,Q}(K)
 +\sum_{t_0\in\mathcal Z^+_{j,Q}(K)}A_{j,Q,+}(t_0),}
 \tag{2.1}
\]

Therefore

\[
 \boxed{
 \mathsf S_{\Lambda,+}(K)
 =\sum_{(j,Q)\in\Lambda}\kappa_j^{-2}
 \left[V^+_{\rm seg}(a_{j,Q};K)
 -\sum_{J\in\operatorname{Comp}(\{d_{j,Q}>0\}\cap K)}
 V^+(a_{j,Q};J)-I^+_{j,Q}(K)\right].}
 \tag{2.2}
\]

At one internal zero, the positive atom of the ordinary hard BV
representative is

\[
 (Da_{j,Q})^+\{t_0\}=(A_+-A_-)^+,
 \tag{2.3}
\]

whereas the segmented/soft entry atom is \(A_+\).  Their difference is

\[
 \boxed{A_+-(A_+-A_-)^+=\min(A_+,A_-).}
 \tag{2.4}
\]

For an even-order touch with \(A_-=A_+=A>0\), ordinary hard BV has no atom,
while the segmented positive entry is \(A\).  Consequently standard BV of
the hard limit cannot replace the target.

#### Proof

At an internal zero, the zero-padded branch to its right starts with the
transition \(0\to A_+\), which contributes \(A_+\) to positive variation;
the branch to its left ends with \(A_-\to0\), which contributes only negative
variation.  If the window starts inside a positive component, zero padding
instead creates \(0\to a(a+)\), exactly the term \(I^+(K)\).  The right
observation endpoint is excluded.  Adding the ordinary positive variation
inside all disjoint branches proves (2.1), and subtracting both the interior
variation and the initial trace proves (2.2).  The hard representative jumps
directly from \(A_-\) to \(A_+\), giving (2.3); (2.4) is the scalar identity.
\(\square\)

### 2.1 Exact level-crossing representation

Tonelli's theorem gives the nonnegative layer-cake identity

\[
 \boxed{
 \mathsf S_{\Lambda,+}(K)
 =\int_0^\infty
 \sum_{(j,Q)\in\Lambda}\kappa_j^{-2}
 \#\{t_0\in\mathcal Z^+_{j,Q}(K):A_{j,Q,+}(t_0)>s\}\,ds.}
 \tag{2.5}
\]

This counts face entries of the zero-padded or soft amplitude through the
positive level \(s\).  It is not a sign crossing of \(d_{j,Q}\): the
denominator is nonnegative and touches zero.  Formula (2.5) represents an
already defined variation; it does not produce an NSE bound for it.

## 3. The componentwise relaxed positive-entry measure has no internal sign

The shell--cell index family is countable.  For a finite truncation define

\[
 \eta^+_\Lambda
 =\sum_{(j,Q)\in\Lambda}\kappa_j^{-2}
 \sum_{t_0\in\mathcal Z^+_{j,Q}}
 A_{j,Q,+}(t_0)\delta_{t_0}.
 \tag{3.1}
\]

For one shell--cell component, the positive and negative soft face parts have
the separate weak limits

\[
 \mu^+_{\varepsilon,j,Q}\rightharpoonup A_+\delta_{t_0},
 \qquad
 \mu^-_{\varepsilon,j,Q}\rightharpoonup A_-\delta_{t_0}.
 \tag{3.2}
\]

Their signed difference may instead converge to
\((A_+-A_-)\delta_{t_0}\); at an even touch it vanishes.  Thus (3.1) is the
sum of the **componentwise relaxed positive parts**.  It is not generally
\((\sum_{j,Q}\mu_{j,Q})^+\), and it is not the positive Jordan part of the
signed weak limit.

### Theorem 3.1 -- monotone positive-face sum

Every coefficient in (3.1) is nonnegative.  Hence:

1. two shell--cell atoms at the same time add rather than cancel;
2. finite truncations are monotone under inclusion;
3. for a countable frame, the infinite sum defines an extended positive
   Borel measure as the monotone limit of finite truncations; local finiteness
   is not asserted;
4. cancellation in a signed aggregate concerns a different observable and
   cannot bound (3.1) without an additional domination inequality.

In particular, the phrase “an NSE-specific cancellation of the positive-entry
sum” is too strong.  What remains possible is an NSE-specific **estimate**, a
packing law, or cancellation in a signed precursor followed by a new
inequality that dominates the componentwise relaxed positive measure.

## 4. Simultaneous entries admit a spatial square-sum payment

For one time \(t\), let

\[
 \mathcal E_\Lambda(t)
 =\{(j,Q)\in\Lambda:t\in\mathcal Z^+_{j,Q}\}
 \tag{4.1}
\]

and define the batch mass

\[
 \mathsf e_\Lambda(t)
 =\sum_{(j,Q)\in\mathcal E_\Lambda(t)}
 \kappa_j^{-2}A_{j,Q,+}(t).
 \tag{4.2}
\]

### Theorem 4.1 -- time-slice entry batching

Under (1.3)--(1.5),

\[
 \boxed{
 \mathsf e_\Lambda(t)
 \le\frac{M_\chi}{Y(t)}
 \sum_j\kappa_j^{-2}\|F_j(t)\|_2^2
 \le M_\chi C_T
 \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}.}
 \tag{4.3}
\]

Consequently, on the normalized torus,

\[
 \boxed{
 \mathsf e_\Lambda(t)
 \lesssim M_\chi C_T
 \|u(t)\|_2Y(t)^{1/2}.}
 \tag{4.4}
\]

The constants are independent of the number of simultaneous cells and of a
finite truncation \(\Lambda\).

#### Proof

The Taylor coefficient \(c_{j,Q}(t)\) in (1.5) is supported in
\(\operatorname{supp}\chi_Q\).  Therefore

\[
 \langle F_j,c_{j,Q}\rangle
 =\langle\mathbf1_{\operatorname{supp}\chi_Q}F_j,c_{j,Q}\rangle,
\]

and Cauchy--Schwarz gives the sharp cellwise bound

\[
 A_{j,Q,+}(t)
 \le\frac{\|\mathbf1_{\operatorname{supp}\chi_Q}F_j(t)\|_2^2}{Y(t)}.
 \tag{4.5}
\]

Sum first over all entering cells, enlarge to all cells, and use (1.3):

\[
 \sum_Q\|\mathbf1_{\operatorname{supp}\chi_Q}F_j\|_2^2
 \le M_\chi\|F_j\|_2^2.
 \tag{4.6}
\]

Then (1.4) proves (4.3).  Finally, Leray projection is bounded on
\(\dot H^{-1}\), and Sobolev duality, Hölder, and interpolation give

\[
 \begin{aligned}
 \|L\|_{\dot H^{-1}}
 &\lesssim\|u\times\omega\|_{6/5}
 \le\|u\|_3\|\omega\|_2\\
 &\lesssim\|u\|_2^{1/2}
 \|\nabla u\|_2^{1/2}Y^{1/2}
 \lesssim\|u\|_2^{1/2}Y^{3/4}.
 \end{aligned}
 \tag{4.7}
\]

Squaring and dividing by \(Y\) yields (4.4). \(\square\)

### 4.1 What (4.3) improves

Bounding every face by the global \(\|F_j\|_2^2/Y\) and then summing cells
would multiply by the cell count.  The support of the leading direction and
bounded overlap remove that spatial multiplicity.  This is the positive
result of R0.71P.

It is a same-time statement.  It does not permit summing (4.3) over unrelated
entry times using a Lebesgue-time energy inequality.

## 5. The complete target is a temporal counting-measure integral

Let \(\mathcal T_\Lambda(K)\) be the set of **distinct** times in the
half-open window \(K=[a,b)\) at which at least one member of \(\Lambda\) has
\(A_{j,Q,+}(t)>0\), and put

\[
 \mathfrak n_\Lambda
 =\sum_{t\in\mathcal T_\Lambda(K)}\delta_t.
 \tag{5.1}
\]

Simultaneous entries across any number of shells and cells are grouped into
one batch \(\mathsf e_\Lambda(t)\).

### Theorem 5.1 -- space--time batching reduction

Define

\[
 \mathcal H(t)
 =M_\chi C_T\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}.
 \tag{5.2}
\]

Then

\[
 \boxed{
 \mathsf S_{\Lambda,+}(K)
 =\int_K\mathsf e_\Lambda(t)\,d\mathfrak n_\Lambda(t)
 \le\int_K\mathcal H(t)\,d\mathfrak n_\Lambda(t).}
 \tag{5.3}
\]

For the countable family, set

\[
 \mathsf e(t)=\sum_{j,Q}\kappa_j^{-2}A_{j,Q,+}(t),
 \qquad
 \mathcal T(K)=\{t\in K:\mathsf e(t)>0\},
 \qquad
 \mathfrak n=\sum_{t\in\mathcal T(K)}\delta_t.
 \tag{5.4}
\]

Here \(A_{j,Q,+}(t)\) is extended by zero away from positive entry times.
The set \(\mathcal T(K)\) is countable: the index set is countable and each
finite-order entry set is discrete.

This is an extended counting Borel measure and need not be locally finite.
For increasing finite truncations \(\Lambda_N\), extend
\(\mathsf e_{\Lambda_N}\) by zero on \(\mathcal T(K)\).  Then
\(\mathsf e_{\Lambda_N}\uparrow\mathsf e\), and Tonelli/monotone convergence
is applied against the **fixed** measure \(\mathfrak n\):

\[
 \lim_N\mathsf S_{\Lambda_N,+}(K)
 =\lim_N\int_K\mathsf e_{\Lambda_N}\,d\mathfrak n
 =\int_K\mathsf e\,d\mathfrak n
 \le\int_K\mathcal H\,d\mathfrak n,
 \tag{5.5}
\]

with either side allowed to be infinite.  In particular, infinitely many
simultaneous entries are allowed; (4.3) still bounds their summed weight at
that time.

Equation (5.3) is the strongest unconditional reduction obtained here.  The
remaining measure is \(d\mathfrak n_\Lambda\), not \(dt\).  Even though the
Leray energy inequality controls ordinary time integrals such as

\[
 \int_K\|u(t)\|_2Y(t)^{1/2}\,dt,
 \tag{5.6}
\]

on bounded intervals, it does not control repeated samples of the same
quantity on a zero-measure set of entry times.

### 5.1 Fixed finite classical truncations

If \(K=[a,b)\) and \(\overline K=[a,b]\Subset I_{\rm strong}\), periodic strong
solutions are analytic in time with values in a strong spatial space.  Every
fixed bounded linear observable \(C_{j,Q}(t)\) is therefore Hilbert-valued
analytic.  If it is not identically zero, its first nonzero Taylor coefficient
at a zero has finite order and the zero is isolated.  Compactness gives
finitely many zeros.  If it is identically zero, it has no positive component
and contributes no entry.

Hence a fixed finite \(\Lambda\) has finite \(\mathcal T_\Lambda(K)\), and
\(\mathsf S_{\Lambda,+}(K)<\infty\).

This qualitative finiteness has no uniform constant as:

1. \(\Lambda\) grows to all shells and cells;
2. the solution varies in an energy-bounded family;
3. \(K\) approaches a possible singular endpoint;
4. zero orders, separations, or projection anchors degenerate.

## 6. Two sharpness tests

### 6.1 A genuine NSE initial face saturates (4.5)

On the normalized torus take the R0.71O initial datum

\[
 u_0(x)=(0,\cos x_1,\cos x_2),
 \tag{6.1}
\]

one radial multiplier with value zero at radius \(1\) and one at radius
\(\sqrt2\), and \(\chi=1\).  Exact Fourier convolution gives

\[
 Y(0)=1,
 \qquad\|F(0)\|_2^2=\frac14,
 \qquad C(0)=0,
 \tag{6.2}
\]

and the leading right direction is

\[
 c=C_t(0)=2F(0),
 \qquad\|c\|_2^2=1,
 \qquad\langle F(0),c\rangle=\frac12.
 \tag{6.3}
\]

Therefore

\[
 \boxed{
 A_+=\frac{(1/2)^2}{1\cdot1}
 =\frac14
 =\frac{\|F(0)\|_2^2}{Y(0)}.}
 \tag{6.4}
\]

The Cauchy residual is zero.  Thus no universal coefficient smaller than one
can improve the one-cell estimate (4.5).  This is still only a one-sided
initial jet, not an internal or repeated NSE face construction.

### 6.2 Sequential abstract entries saturate the counting measure

Let \(\|e\|_H=1\) and on the half-open window \(K=[0,2\pi)\) set

\[
 Y_N=1,\qquad F_N=e,
 \qquad C_N(t)=N^{-1}\sin(Nt)e.
 \tag{6.5}
\]

The positive atoms occur at
\(t=2k\pi/N\), \(k=0,\ldots,N-1\).  Thus the left zero observation boundary
is included, the right endpoint \(2\pi\) is excluded, and there are exactly
\(N\) positive entries.  Each has \(A_+=1\), and only one batch occurs at
each entry time.  Consequently

\[
 \boxed{
 \mathsf S_{N,+}=N
 =\int_0^{2\pi}1\,d\mathfrak n_N,}
 \tag{6.6}
\]

whereas

\[
 \int_0^{2\pi}1\,dt=2\pi.
 \tag{6.7}
\]

The ordinary quadratic budgets remain bounded:

\[
 \int d_Ndt=\frac\pi{N^2},\qquad
 \int\|C_{N,t}\|_H^2dt=\pi,
 \qquad\int\|F_N\|_H^2dt=2\pi.
 \tag{6.8}
\]

For \(\varepsilon_N=N^{-4}\), the soft-to-hard positive-entry ratio is

\[
 \frac{N/(1+N^{-2})}{N}
 =\frac1{1+N^{-2}}\longrightarrow1.
 \tag{6.9}
\]

Thus (5.3) is sharp at the level of smooth Hilbert paths, and no universal
replacement \(d\mathfrak n\mapsto dt\) follows from the ordinary budgets in
(6.8).  This is not a coupled NSE multiple-face example.

## 7. What time analyticity can quantify only conditionally

There is a standard conditional zero-count mechanism.  Suppose a
Hilbert-valued observable \(C\), with values in the complexification
\(H_{\mathbb C}\), extends holomorphically to
\(D(t_*,R)\), with

\[
 \sup_{D(t_*,R)}\|C(z)\|_H\le M,
 \qquad C(t_*)\ne0.
 \tag{7.1}
\]

Choose a norm-one complex linear functional \(\ell\) satisfying
\(\ell(C(t_*))=\|C(t_*)\|\), and set \(f(z)=\ell(C(z))\).  Every zero of
\(C\) is a zero of \(f\), while \(|f(t_*)|=\|C(t_*)\|\).  Jensen's formula
gives, for \(0<r<R\),

\[
 \boxed{
 N_C(D(t_*,r))
 \le\frac{\log(M/\|C(t_*)\|_H)}{\log(R/r)}.}
 \tag{7.2}
\]

Here \(N_C(D(t_*,r))\) counts distinct vector zeros; the scalar Jensen count
uses multiplicity and can only be larger.  The number \(M\) is a uniform norm
bound on the full complex disk.

The right side requires:

1. a complex-time radius \(R\);
2. an upper analytic norm \(M\);
3. a nondegenerate anchor \(\|C(t_*)\|\);
4. a covering of the real observation interval by such disks.

Classical NSE time analyticity supplies a disk only inside the strong
interval.  Leray energy supplies neither a uniform complex-time radius nor a
lower anchor for every filtered cell observable.  Formula (7.2) is therefore
a useful next gate, not a closed energy-level estimate.

## 8. Relation to prior budgets

### 8.1 R0.71I initial-time payment

R0.71I proved at one chosen smooth time

\[
 \sum_{j,Q}\kappa_j^{-2}a_{j,Q}(T_-)
 \lesssim\frac{\|L(T_-)\|_{\dot H^{-1}}^2}{Y(T_-)}.
 \tag{8.1}
\]

Theorem 4.1 is the corresponding statement for every **simultaneous batch**
of finite-order entries.  Repeating the estimate at unrelated times produces
the counting measure in (5.3); it does not create a time-integrated energy
bound.

### 8.2 R0.71L denominator mass

The R0.71L estimate

\[
 \nu\int_I\sum_{j,Q}\kappa_j^{-2}d_{j,Q}(t)\,dt
 \lesssim\|u(0)\|_2^2
 \tag{8.2}
\]

does not count zeros.  The family (6.5) has denominator mass tending to zero
and entry mass tending to infinity.

### 8.3 R0.71N and R0.71O source measures

The positive-entry measure is the face-atomic part of the componentwise
positive soft source.  A uniform bound for the complete componentwise
positive source would pay it, but that is the missing source estimate itself.
Splitting the raw source and radial terms loses the R0.71O logarithmic
cancellation; summing the already positive face atoms cannot restore a sign.

## 9. Primary-source boundary

The closest primary tools have narrower conclusions.

1. [Fleming--Rishel's coarea formula](https://link.springer.com/article/10.1007/BF01236935)
   writes an already controlled total variation as an integral of level-set
   perimeters.  It does not produce BV from the NSE energy inequality and does
   not separate two opposite atoms collapsed at one point.
2. [Łochowski's upward/downward crossing formulas](https://arxiv.org/abs/1503.01746v4)
   identify positive and negative variation through level crossings.  Applied
   to the ordinary hard representative they see \((A_+-A_-)^+\); recovering
   \(A_+\) requires the soft or segmented path.
3. [Vol'pert's BV chain rule](https://www.mathnet.ru/eng/sm4127) applies to
   every fixed smooth regularization.  Its constants do not supply a uniform
   \(\varepsilon\downarrow0\) face bound.
4. [Temam, Chapter 7](https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7)
   gives time analyticity only on a classical regularity interval.  It gives
   no uniform zero count, order, spacing, or transversality.
5. [Masuda's analyticity and unique-continuation theorem](https://doi.org/10.3792/pja/1195521421)
   concerns the complete velocity field vanishing on a spatial open set.  A
   filtered cutoff observable lying in an operator kernel is a different
   event.
6. [Foias--Temam Gevrey regularity](https://doi.org/10.1016/0022-1236(89)90015-3)
   gives spatial Fourier decay, not a time-zero count or lower projection
   anchor.
7. [Giga--Jo--Mahalov--Yoneda](https://doi.org/10.1016/j.physd.2008.03.007)
   prove time analyticity and no sudden creation of an almost-periodic Fourier
   mode.  Isolated repeated zeros and physical cutoff observables are not
   excluded.
8. [Leray's 1934 weak-solution paper](https://link.springer.com/article/10.1007/BF02547354)
   supplies the foundational energy framework.  A time-integrated energy
   budget does not control repeated sampling on an entry-time counting
   measure.

The bounded two-wave primary-source search stopped after these interfaces
were resolved.  It found no theorem deriving (0.2) from Leray energy, time
analyticity, unique continuation, or spatial frequency decay.  This is a
bounded negative finding, not a claim of nonexistence, originality, or
priority.

## 10. Exact and independent audits

The exact producer `research/r071p_exact_audit.py` checks:

1. the Gram determinant identity behind the sharp cellwise estimate;
2. a rational finite overlap ledger;
3. the positive atomic and layer-cake sums;
4. the exact \(N\)-entry oscillatory family;
5. the exact Fourier coefficients of the sharp NSE initial entry.

The independent checker `research/r071p_independent_audit.py` imports neither
the exact producer nor prior release code.  It performs:

1. 64 seeded random overlap tests;
2. sampled-sign and Brent-root entry detection for \(N=1,\ldots,64\);
3. independent quadrature of the soft rising layers;
4. a standalone \(32^3\) NumPy FFT reconstruction of the NSE initial jet.

The checks are algebraic and diagnostic.  There is no PDE time stepping,
DNS, fitted parameter, interval-certified multiple-face construction, GPU
run, or DGX run in this release.

## 11. Finite route decision

R0.71P proves the exact reduction

\[
 \boxed{
 \text{positive entry sum}
 \ \le\ \text{spatial }\dot H^{-1}\text{ batch budget}
 \text{ sampled by an entry-time counting measure}.}
 \tag{11.1}
\]

The spatial cell multiplicity is removed by support overlap.  The remaining
temporal multiplicity is not controlled by the current energy, denominator
mass, ordinary first-time norms, or qualitative analyticity.

The next finite gate is R0.71Q: test the quantitative complex-time
Jensen/parabolic-window route.  Every candidate bound must expose the analytic
radius, upper complex norm, lower projection anchor, and window covering.  If
these inputs reduce to a known continuation norm, inverse denominator, target
BV, or an unproved transversality condition, the zero-count branch remains
conditional and should stop.

The following statements are not proved:

- a uniform all-shell/all-cell positive-entry estimate;
- a uniform temporal packing or zero-count theorem for NSE observables;
- an infinite-frame or Leray-level passage;
- a bound at a possible singular endpoint;
- a continuation criterion below known critical hypotheses;
- an internal or arbitrarily repeated NSE face construction;
- finite-time singularity or global smoothness in three dimensions;
- originality, priority, or resolution of the Millennium problem.
