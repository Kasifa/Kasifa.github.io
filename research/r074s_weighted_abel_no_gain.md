# R0.74S Step 1 — weighted Abel summation has no standalone shell-compression gain

## 0. Result and boundary

This note tests the most favorable algebraic version of the signed
adjacent-shell route proposed in R0.74Q and sharpened after R0.74R.  It
proves four facts.

1. Shell-dependent stopping times admit an exact finite stopped-Abel
   identity.
2. For the frozen super-Gaussian weights, the discrete spatial variation of
   every binary active-shell set is uniformly comparable to its entire
   active weighted mass.
3. Even under an ideal complementary collar partition, every shared
   internal face retains a fixed fraction of the larger adjacent weight.
4. The absolute-value bound after Abel summation is algebraically sharp.

Therefore discrete Abel summation followed by absolute values supplies no
\(M^{-1/2}\), no vanishing high-shell factor, and no route from a linear
\(P_R^M\) ledger to the desired \((P_R^M)^{2/3}\) ledger in the
large-payment regime.  A successful stopping-time proof must retain genuine
Navier--Stokes sign information, or separately control boundary supply,
negative work/backscatter, leakage, and the mismatch between the actual
padded cutoffs and an exact partition.

The theorem below is finite-dimensional algebra.  The sharpness witnesses
are not Navier--Stokes solutions, and the ideal adjacent-boundary
representation is not asserted for the frozen R0.74P flux.
**PROVED ALGEBRAIC NO-GAIN. NOT CLAY.**

## 1. Frozen weight gap

Let

\[
 \gamma_k=\exp\!\left(-\frac{4^{k-1}}{32}\right),\qquad k\ge1.
\tag{S.1}
\]

Then

\[
 \frac{\gamma_{k+1}}{\gamma_k}
 =\exp\!\left(-\frac{3\cdot4^{k-1}}{32}\right)
 \le \exp\!\left(-\frac3{32}\right)
 \le\frac{32}{35}.
\tag{S.2}
\]

The last inequality follows from \(e^x\ge1+x\).  Consequently,

\[
 \boxed{
 \gamma_k-\gamma_{k+1}\ge\frac3{35}\gamma_k.}
\tag{S.3}
\]

The optimal uniform relative gap is \(1-e^{-3/32}\); the rational constant
\(3/35\) is retained for exact certification.

## 2. Exact stopped-Abel identity

Fix \(M\ge1\), \(s<\tau\), stopping times
\(\sigma_k\in[s,\tau)\), and integrable real boundary densities
\(b_1,\ldots,b_{M+1}\).  Put

\[
 f_k=b_{k+1}-b_k,\qquad
 c_k(t)=\gamma_k1_{(\sigma_k,\tau)}(t).
\tag{S.4}
\]

### Proposition 2.1 — stopped adjacent-boundary summation

One has

\[
\begin{aligned}
 \sum_{k=1}^{M}\gamma_k\int_{\sigma_k}^{\tau}f_k(t)\,dt
 =\int_s^\tau\Big[
 &-c_1b_1+c_Mb_{M+1}\\
 &+\sum_{m=2}^{M}(c_{m-1}-c_m)b_m
 \Big](t)\,dt.
\end{aligned}
\tag{S.5}
\]

**Proof.**  Finiteness permits interchange of the sum and time integral.
At each time,

\[
\begin{aligned}
 \sum_{k=1}^{M}c_k(b_{k+1}-b_k)
 &=-c_1b_1+c_Mb_{M+1}
   +\sum_{m=2}^{M}(c_{m-1}-c_m)b_m.
\end{aligned}
\tag{S.6}
\]

Integrate (S.6).  \(\square\)

For \(A\subset\{1,\ldots,M\}\), extend
\(c_k=\gamma_k1_A(k)\) by \(c_0=c_{M+1}=0\), and define

\[
 V_\gamma(A):=\sum_{m=1}^{M+1}|c_m-c_{m-1}|.
\tag{S.7}
\]

Thus the coefficient \(\ell^1\) norm on the right side of (S.5) is exactly
\(V_\gamma(A(t))\), where
\(A(t)=\{k:\sigma_k<t<\tau\}\).

## 3. Active coefficient variation is not small

Every nonempty finite \(A\subset\{1,\ldots,M\}\) has a unique decomposition
into maximal integer blocks

\[
 A=\bigcup_{\nu=1}^{J}[p_\nu,q_\nu]_{\mathbb Z},
 \qquad q_\nu+1<p_{\nu+1}.
\tag{S.8}
\]

### Theorem 3.1 — exact component formula and two-sided mass bound

For every such \(A\),

\[
 \boxed{
 V_\gamma(A)=2\sum_{\nu=1}^{J}\gamma_{p_\nu}.}
\tag{S.9}
\]

Moreover,

\[
 \boxed{
 \frac6{35}\sum_{k\in A}\gamma_k
 \le V_\gamma(A)
 \le2\sum_{k\in A}\gamma_k.}
\tag{S.10}
\]

**Proof.**  On one block \([p,q]_{\mathbb Z}\), strict decrease of
\(\gamma_k\) gives

\[
 \gamma_p+\sum_{k=p+1}^{q}(\gamma_{k-1}-\gamma_k)+\gamma_q
 =2\gamma_p.
\tag{S.11}
\]

The zero gaps separate the block contributions, proving (S.9).  The upper
bound in (S.10) follows from
\(\gamma_{p_\nu}\le\sum_{k=p_\nu}^{q_\nu}\gamma_k\).  By (S.2),

\[
 \sum_{k=p_\nu}^{q_\nu}\gamma_k
 \le\gamma_{p_\nu}\sum_{j=0}^{\infty}\left(\frac{32}{35}\right)^j
 =\frac{35}{3}\gamma_{p_\nu}.
\tag{S.12}
\]

Sum (S.12) over the blocks and use (S.9) to obtain the lower bound.
\(\square\)

In particular, neither one connected active block nor arbitrarily many
components produces a coefficient-compression factor.  The comparison is
uniform in \(M\), in the positions of the blocks, and in the stopping times.

## 4. Even an ideal complementary collar retains the weight gap

The actual R0.74E padded cutoffs are not assumed to form an exact partition.
To give cancellation its best possible chance, suppose instead that a
shared collar at radius \(2^{k+1}R\) uses one smooth transition
\(\vartheta\) satisfying

\[
 \vartheta(z)+\vartheta(-z)=1,\qquad \vartheta'\ge0.
\tag{S.13}
\]

With \(z=(|y|-2^{k+1}R)/(R/8)\), the outer transition of shell \(k\) is
\(\vartheta(-z)\) and the inner transition of shell \(k+1\) is
\(\vartheta(z)\).  Since (S.13) implies
\(\vartheta'(-z)=\vartheta'(z)\),

\[
\begin{aligned}
 \nabla\!\left[
  \gamma_k\vartheta(-z)+\gamma_{k+1}\vartheta(z)
 \right]
 =\frac8R(\gamma_{k+1}-\gamma_k)
   \vartheta'(z)\frac{y}{|y|}.
\end{aligned}
\tag{S.14}
\]

Equations (S.3) and (S.14) give the pointwise coefficient bound

\[
 \boxed{
 \left|\nabla[
  \gamma_k\vartheta(-z)+\gamma_{k+1}\vartheta(z)]
 \right|
 \ge\frac{24}{35R}\gamma_k\vartheta'(z).}
\tag{S.15}
\]

Thus perfect equal-weight face cancellation would still leave a uniformly
non-negligible weighted face.  At high shells the ratio
\(\gamma_{k+1}/\gamma_k\) tends to zero, so the residual approaches the
entire inner-shell coefficient rather than vanishing.

## 5. The absolute Abel estimate is sharp

Let

\[
 B(t):=\max_{1\le m\le M+1}|b_m(t)|.
\tag{S.16}
\]

Equation (S.5) implies

\[
 \left|
 \sum_{k=1}^{M}\gamma_k\int_{\sigma_k}^{\tau}f_k
 \right|
 \le\int_s^\tau V_\gamma(A(t))B(t)\,dt.
\tag{S.17}
\]

This inequality has no universal algebraic improvement.  Indeed, denote
the \(M+1\) coefficients on the right side of (S.6) by
\(d_m(t)\).  For any nonnegative \(B\in L^1(s,\tau)\), choose

\[
 b_m(t)=B(t)\operatorname {sgn}d_m(t),
 \qquad \operatorname {sgn}0:=0.
\tag{S.18}
\]

Then \(f_k=b_{k+1}-b_k\) is integrable and the integrand in (S.5) equals

\[
 \sum_{m=1}^{M+1}d_mb_m
 =B(t)\sum_{m=1}^{M+1}|d_m|
 =B(t)V_\gamma(A(t))
\tag{S.19}
\]

for almost every \(t\).  Hence equality holds in (S.17).  The measurable
witnesses can be approximated away from the finitely many stopping times by
smooth functions, so discontinuity is not the obstruction.

This witness is chosen to saturate a finite algebraic inequality.  It is not
a velocity field, pressure, local-energy solution, or Navier--Stokes
counterexample.

## 6. Exact interface with the R0.74R upcrossing branch

Suppose an auxiliary PDE binding eventually supplies normalized adjacent
densities \(f_k\), stopping times \(\sigma_k\), nonnegative target
increments \(a_k\), and quadratic errors \(q_k\) such that

\[
 a_k\le q_k+\gamma_k\int_{\sigma_k}^{\tau}f_k(t)\,dt,
 \qquad
 \sum_kq_k\le C A_R.
\tag{S.20}
\]

Then (S.5) gives the sufficient stopped-boundary condition

\[
 \boxed{
 \int_{s}^{\tau}V_\gamma(A(t))B(t)\,dt\le C A_R
 \quad\Longrightarrow\quad
 \sum_ka_k\le C A_R.}
\tag{S.21}
\]

This is a genuine conditional interface, but Theorem 3.1 shows why it is
not obtained merely by saying that internal faces cancel.  Once absolute
values are taken, \(V_\gamma(A)\) retains a fixed fraction of the complete
active weighted mass.  The missing estimate must instead exploit at least
one of the following:

- sign correlation between \(d_m\) and the Navier--Stokes boundary work
  \(b_m\);
- a separately controlled exterior supply/leakage term;
- negative work or backscatter that is retained rather than discarded;
- a PDE restriction on which shell blocks can be active with large
  boundary work; or
- a new boundary-work observable already bounded at the quadratic scale.

## 7. Binding boundary and next gate

The R0.74P flux uses the frozen padded cutoffs \(\Psi_k^R\), the
velocity--pressure work, moving-frame drift, and a quadratic source ledger.
It has not been rewritten as (S.4).  The complementary profile in Section 4
is a best-case comparison, not a hidden property of those cutoffs.

Accordingly:

- (S.2)--(S.21) are **PROVED ALGEBRA**;
- the conclusion that Abel-plus-absolute-values has no coefficient gain is
  **PROVED IN THE IDEAL ADJACENT MODEL**;
- a signed PDE estimate improving (S.17) is **OPEN**;
- the binding of stopped R0.74P upcrossings to boundary work, including all
  jump, pressure, drift, leakage, and backscatter rows, is **OPEN**; and
- (Q.1), scale contraction, regularity, singularity formation, and the Clay
  Millennium problem remain **OPEN / NOT CLAIMED**.

The next calculation should derive the actual time-dependent stopped-test
identity for
\(\sum_k\gamma_k1_{(\sigma_k,\tau)}(t)\Psi_k^R\), without taking absolute
values, and list every temporal jump and spatial-collar term.  Only after
that identity is exact is it meaningful to test a PDE sign mechanism.
