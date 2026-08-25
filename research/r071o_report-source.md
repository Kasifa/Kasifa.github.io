# R0.71O -- Soft regularization exposes denominator faces, but does not pay them from the available energy and denominator-mass budgets

**Date:** 2026-08-26

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, localized Littlewood--Paley observables, normalized
Hilbert directions, temporal BV, and source measures

**Status:** release source.  The report proves exact soft--hard identities, a
finite-order face-measure theorem, an abstract smooth-path separation, and a
one-sided smooth Navier--Stokes initial-jet example.  It proves no uniform
NSE face sum, continuation criterion, singularity, global regularity, novelty,
or Millennium-problem result.

## 0. Direct decision

R0.71N left one fixed-cell boundary question.  Let

\[
 C_Q=\operatorname{curl}(\chi_QW_j),\qquad
 d_Q=\|C_Q\|_2^2,\qquad
 B_Q=\langle F_j,C_Q\rangle,
\]

and, on \(Y=\|\omega\|_2^2>0\), regularize the hard denominator by

\[
 R_{Q,\varepsilon}=\sqrt{d_Q+\varepsilon},\qquad
 z_{Q,\varepsilon}
 =\frac{B_Q}{\sqrt YR_{Q,\varepsilon}},\qquad
 a_{Q,\varepsilon}=(z_{Q,\varepsilon}^+)^2.
 \tag{0.1}
\]

Does \(\varepsilon\downarrow0\) remove the denominator faces, or does it
produce a measure that still needs an independent payment?

The finite answer is:

1. the soft quotient is globally smooth for each \(\varepsilon>0\);
2. on \(d_Q>0\), it factors exactly through the hard scalar;
3. at every isolated finite-order zero, the soft transition creates explicit
   positive and negative one-sided face atoms;
4. the additional soft radial damping has no atom at such a zero;
5. the two unsymmetrized raw source terms each have logarithmically divergent
   mass near an active face, although their sum has the finite face limit;
6. a smooth Hilbert-path family has uniformly bounded ordinary
   \(W^{1,p}\)-in-time data but face cost growing like its zero count;
7. a genuine smooth NSE initial trace can start at \(d_Q=0\) and have a
   strictly positive right entry trace.

Thus soft regularization **exposes** the hard faces.  It does not pay them from
the Leray energy or the R0.71L denominator-mass budget.  An NSE-specific
cancellation after the full frame--cell sum remains possible and is not
excluded here.

## 1. Claim boundary and conventions

The exact fixed-cell identities hold for a classical, zero-mean,
incompressible periodic solution, one fixed real-even scalar annular
multiplier \(T_j\), and one fixed time-independent nonnegative smooth cutoff
\(\chi_Q\).  No moving cutoff or refresh jump is inserted.

The hard formulas require

\[
 Y(t)>0,\qquad d_Q(t)>0.
 \tag{1.1}
\]

The soft formulas require only \(Y>0\).  At \(d_Q=0\), one has \(C_Q=0\)
and hence \(B_Q=0\), so the soft scalar is exactly zero.

There are two source conventions.  Put

\[
 \lambda_j=\nu\kappa_j^2.
\]

The R0.71N-style soft source is

\[
 \mathcal J_{Q,\varepsilon}^{N}
 =(z_{Q,\varepsilon})_t+\lambda_jz_{Q,\varepsilon}.
 \tag{1.2}
\]

The R0.71I soft-direction source is

\[
 \mathcal J_{Q,\varepsilon}^{I}
 =(z_{Q,\varepsilon})_t
 +\lambda_j(1+\theta_{Q,\varepsilon})z_{Q,\varepsilon},
 \qquad
 \theta_{Q,\varepsilon}
 =\frac{\varepsilon}{d_Q+\varepsilon}.
 \tag{1.3}
\]

They differ by

\[
 \mathcal J_{Q,\varepsilon}^{I}
 =\mathcal J_{Q,\varepsilon}^{N}
 +\lambda_j\theta_{Q,\varepsilon}z_{Q,\varepsilon}.
 \tag{1.4}
\]

Both are used below, with the superscript retained.  Confusing them changes
where the extra soft radial term appears, but not the face measure.

The endpoint convention is also explicit.  Distributional BV on an open
observation interval does not charge its endpoints.  The component ledger
used in R0.71I charges one-sided entry and exit traces.  Whenever a count
includes observation-boundary faces, that fact is stated.

## 2. Global soft quotient identities

For brevity suppress \((j,Q)\).  Let

\[
 R_\varepsilon=\sqrt{d+\varepsilon},\qquad
 z_\varepsilon=\frac B{\sqrt YR_\varepsilon},
 \qquad
 a_\varepsilon=(z_\varepsilon^+)^2.
 \tag{2.1}
\]

Direct differentiation gives

\[
 \boxed{
 (z_\varepsilon)_t
 =\frac{B_t}{\sqrt YR_\varepsilon}
 -\frac{z_\varepsilon}{2}
 \left(\frac{Y_t}{Y}+\frac{d_t}{d+\varepsilon}\right).}
 \tag{2.2}
\]

Therefore

\[
 \boxed{
 \mathcal J_\varepsilon^N
 =\frac{B_t+\lambda B}{\sqrt YR_\varepsilon}
 -\frac{z_\varepsilon}{2}
 \left(\frac{Y_t}{Y}+\frac{d_t}{d+\varepsilon}\right).}
 \tag{2.3}
\]

On the positive branch,

\[
 \boxed{
 (a_\varepsilon)_t+2\lambda a_\varepsilon
 =2z_\varepsilon^+\mathcal J_\varepsilon^N,}
 \tag{2.4}
\]

and equivalently

\[
 \boxed{
 (a_\varepsilon)_t
 +2\lambda(1+\theta_\varepsilon)a_\varepsilon
 =2z_\varepsilon^+\mathcal J_\varepsilon^I.}
 \tag{2.5}
\]

For each fixed \(\varepsilon>0\), these equations are global across the zero
set of \(d\).  This removes the coordinate singularity.  It does not yet give
a bound uniform in \(\varepsilon\).

## 3. Exact hard--soft factorization

On one connected component of \(\{d>0\}\), define the hard objects

\[
 z=\frac B{\sqrt{Yd}},\qquad
 a=(z^+)^2,\qquad
 \mathcal J=z_t+\lambda z,
 \tag{3.1}
\]

and

\[
 \sigma_\varepsilon=\frac d{d+\varepsilon}
 =1-\theta_\varepsilon.
 \tag{3.2}
\]

### Theorem 3.1 -- exact face-source identity

On \(d>0\),

\[
 \boxed{z_\varepsilon=\sqrt{\sigma_\varepsilon}\,z,}
 \qquad
 \boxed{a_\varepsilon=\sigma_\varepsilon a,}
 \tag{3.3}
\]

and

\[
 (\sigma_\varepsilon)_t
 =\frac{\varepsilon d_t}{(d+\varepsilon)^2}.
 \tag{3.4}
\]

The N-style source satisfies

\[
 \boxed{
 2z_\varepsilon^+\mathcal J_\varepsilon^N
 =2\sigma_\varepsilon z^+\mathcal J
 +(\sigma_\varepsilon)_ta.}
 \tag{3.5}
\]

The I-style source satisfies

\[
 \boxed{
 2z_\varepsilon^+\mathcal J_\varepsilon^I
 =2\sigma_\varepsilon z^+\mathcal J
 +(\sigma_\varepsilon)_ta
 +2\lambda\theta_\varepsilon a_\varepsilon.}
 \tag{3.6}
\]

#### Proof

Equations (3.3)--(3.4) follow from the definitions.  Differentiate
\(a_\varepsilon=\sigma_\varepsilon a\), use

\[
 a_t+2\lambda a=2z^+\mathcal J,
\]

and compare with (2.4).  This gives (3.5).  Equation (3.6) follows from
(1.4).  No projection estimate or NSE energy inequality is used. \(\square\)

The term \((\sigma_\varepsilon)_ta\) is the exact face layer.  The extra
radial term in (3.6) is nonnegative, but Section 4 shows that it has vanishing
mass at every finite-order zero.

## 4. Finite-order face theorem

Let \(H\) be the real Hilbert space containing \(C(t)\).  Suppose \(t_0\) is
an isolated classical finite-order zero and the one-sided Taylor remainders
are differentiable:

\[
 C(t_0+\tau)=c\tau^m+O(|\tau|^{m+1})_H,
 \qquad
 C_t(t_0+\tau)=mc\tau^{m-1}+O(|\tau|^m)_H,
 \qquad c\ne0,
 \qquad m\in\mathbb N.
 \tag{4.1}
\]

Assume also
\[
 F(t_0+\tau)=F_0+O(|\tau|)_H,\quad F_t=O_H(1),
 \qquad
 Y(t_0+\tau)=Y_0+O(|\tau|),\quad Y_t=O(1),
\]
with \(Y_0>0\), and put

\[
 b=\langle F(t_0),c\rangle_H,
 \qquad q=\|c\|_H^2.
 \tag{4.2}
\]

### Theorem 4.1 -- one-sided traces and relaxed face measures

The squared hard positive scalar has the one-sided traces

\[
 \boxed{
 A_+=\frac{(b^+)^2}{Y_0q},
 \qquad
 A_-=\frac{(((-1)^mb)^+)^2}{Y_0q}.}
 \tag{4.3}
\]

On the right and left inner scales

\[
 \delta_\varepsilon
 =\left(\frac\varepsilon q\right)^{1/(2m)},
 \qquad s=\frac{|\tau|}{\delta_\varepsilon},
 \tag{4.4}
\]

the leading soft profiles are

\[
 a_\varepsilon(t_0+\tau)
 =A_\pm\frac{s^{2m}}{1+s^{2m}}+o(1).
 \tag{4.5}
\]

Choose any \(r_\varepsilon\downarrow0\) such that
\(\delta_\varepsilon/r_\varepsilon\to0\), and let
\(\mu_\varepsilon\) denote the restriction of \(Da_\varepsilon\) to
\((t_0-r_\varepsilon,t_0+r_\varepsilon)\).

Then the shrinking face-layer measures satisfy

\[
 \boxed{
 \mu_\varepsilon
 \stackrel{*}{\rightharpoonup}
 (A_+-A_-)\delta_{t_0},}
 \tag{4.6}
\]

\[
 \boxed{
 \mu_\varepsilon^+
 \stackrel{*}{\rightharpoonup}A_+\delta_{t_0},
 \qquad
 \mu_\varepsilon^-
 \stackrel{*}{\rightharpoonup}A_-\delta_{t_0},}
 \tag{4.7}
\]

and

\[
 \boxed{
 |\mu_\varepsilon|
 \stackrel{*}{\rightharpoonup}
 (A_++A_-)\delta_{t_0}.}
 \tag{4.8}
\]

The regular hard derivative away from \(t_0\) is retained separately.

The extra soft radial term has no face atom:

\[
 \int_{|t-t_0|<r}
 2\lambda\theta_\varepsilon a_\varepsilon\,dt
 =O\!\left(\varepsilon^{1/(2m)}\right)
 \longrightarrow0.
 \tag{4.9}
\]

Therefore the source measures in (3.5)--(3.6) have the same atomic Jordan
parts:

\[
 (\text{source})^+_{\rm atom}=A_+\delta_{t_0},
 \qquad
 (\text{source})^-_{\rm atom}=A_-\delta_{t_0}.
 \tag{4.10}
\]

#### Proof

From (4.1) and the derivative remainder,

\[
 d(t_0+\tau)=q\tau^{2m}+O(|\tau|^{2m+1}),
 \qquad
 B(t_0+\tau)=b\tau^m+O(|\tau|^{m+1}),
 \tag{4.11}
\]

This gives (4.3) and (4.5).  The profile

\[
 \Phi_m(s)=\frac{s^{2m}}{1+s^{2m}}
\]

increases from zero to one, with

\[
 \Phi_m'(s)
 =\frac{2ms^{2m-1}}{(1+s^{2m})^2},
 \qquad
 \int_0^\infty\Phi_m'(s)\,ds=1.
 \tag{4.12}
\]

Approaching \(t_0\) from the left gives a negative layer of mass \(A_-\);
leaving to the right gives a positive layer of mass \(A_+\).  This proves
(4.6)--(4.8): the rescaled functions converge in \(C^1\) on every bounded
\(s\)-interval, while the Taylor derivative bounds make the variation in
\(\delta_\varepsilon\ll|\tau|<r_\varepsilon\) equal to the profile tail plus
\(O(r_\varepsilon)\).  After (4.4), the radial integral is a constant multiple of

\[
 \varepsilon^{1/(2m)}
 \int_0^\infty\frac{s^{2m}}{(1+s^{2m})^2}\,ds,
\]

and the integral is finite.  This proves (4.9)--(4.10). \(\square\)

### 4.1 Three distinct zero types

1. If \(b=0\), both displayed traces vanish.  Higher jets decide the next
   order; a zero denominator does not automatically create positive mass.
2. If \(m\) is odd and \(b\ne0\), exactly one of \(A_\pm\) is nonzero.  The
   face is a genuine jump of the hard \(L^1\) limit.
3. If \(m\) is even and \(b>0\), then \(A_-=A_+=A>0\).  The signed atom in
   (4.6) cancels, while (4.8) retains the cost \(2A\).

The last case is important.  Standard distributional BV of the hard limit
sees the jump

\[
 |A_+-A_-|,
\]

whereas the segmented component ledger and the relaxed soft layer see

\[
 A_++A_-.
\]

Their difference is the nonnegative relaxation defect

\[
 A_++A_--|A_+-A_-|=2\min(A_+,A_-).
 \tag{4.13}
\]

Thus lower semicontinuity of BV alone cannot recover two opposite atoms that
collapse at the same point.

### 4.2 The raw split is not uniformly measure-bounded

There is a second, practically important cancellation.  On the active branch
\(B>0\), direct differentiation can be written

\[
 (a_\varepsilon)_t+2\lambda a_\varepsilon
 =\mathsf S_\varepsilon+\mathsf R_\varepsilon,
 \tag{4.14}
\]

where

\[
 \mathsf S_\varepsilon
 =\frac{2B(B_t+\lambda B)}{Y(d+\varepsilon)}
  -a_\varepsilon\frac{Y_t}{Y},
 \qquad
 \mathsf R_\varepsilon
 =-\frac{B^2d_t}{Y(d+\varepsilon)^2}.
 \tag{4.15}
\]

Assume now the classical Taylor version of (4.1), so that the expansion and
its first derivative have the corresponding finite-order remainders.  On an
active right half-face set

\[
 \gamma^2=\frac{b^2}{Y_0q},\qquad X=qr^{2m}.
\]

For fixed sufficiently small \(r>0\), the singular parts obey

\[
 \int_{t_0}^{t_0+r}\mathsf S_\varepsilon\,dt
 =\gamma^2\log\!\left(1+\frac X\varepsilon\right)+O(1),
 \tag{4.16}
\]

\[
 \int_{t_0}^{t_0+r}\mathsf R_\varepsilon\,dt
 =-\gamma^2\left[
 \log\!\left(1+\frac X\varepsilon\right)
 -\frac{X}{X+\varepsilon}\right]+O(1).
 \tag{4.17}
\]

The left active half-face has the analogous formulas with time orientation
reversed.  Thus the total variations of the two raw singular pieces grow at
least like \(\gamma^2\log(1/\varepsilon)-O(1)\).  They are not separately
uniformly bounded Radon-measure families.  Their leading logarithms cancel,
and the joint half-face increment tends to \(\gamma^2\):

\[
 \gamma^2\frac{X}{X+\varepsilon}\longrightarrow\gamma^2.
 \tag{4.18}
\]

Consequently one cannot estimate the two terms in (4.15) separately and then
pass to the soft limit.  The cancellation-preserving form (3.5), or the full
time derivative in (4.14), is essential.

### 4.3 What is not covered

Theorem 4.1 requires an isolated finite-order zero.  A smooth flat path such
as

\[
 C(t)=e^{-1/t^2}\sin(1/t)e\quad(t>0),\qquad C(0)=0,
\]

can have zeros accumulating at \(0\).  Smoothness by itself is not a zero-count
budget.  If \(C\) vanishes on an interval, the correct object is the set of
connected components of \(\{d>0\}\), not a pointwise zero count.

## 5. Time analyticity on a classical periodic interval

For periodic strong solutions, time analyticity supplies a useful but limited
structural corollary.  Temam's periodic theory states that a three-dimensional
strong solution is analytic in time only on its local \(H^1\)-regularity
interval; it does not continue through a possible singular time
([Temam, Chapter 7, Theorem 7.1 and Remarks 7.1--7.2](https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7)).

On a compact subinterval strictly inside such a classical interval, the fixed
linear observable \(C_Q(t)\) is Hilbert-valued analytic.  Hence either:

1. \(C_Q\) is identically zero on the connected interval; or
2. every interior zero is isolated and finite order, and there are only
   finitely many zeros on the compact subinterval.

This places individual classical zeros under Theorem 4.1.  It gives no
uniform bound on their number, order, separation, or transversality across
solutions, shells, cells, or intervals approaching a putative singular time.

Giga--Jo--Mahalov--Yoneda prove related time analyticity and a no-sudden-mode
creation statement in their function-space setting
([Physica D 237 (2008), Theorems 1.1, 1.2 and 1.4](https://doi.org/10.1016/j.physd.2008.03.007)).
That statement excludes a mode missing on a whole time interval and then
appearing suddenly.  It does not exclude an isolated zero followed by
nonzero values.

## 6. Smooth-path separation from ordinary budgets

The face measure is not bounded by denominator mass or ordinary first-time
derivative norms at the level of abstract Hilbert paths.

Let \(\|e\|_H=1\), \(\lambda\ge0\), and on \([0,2\pi]\) set

\[
 Y_N=1,\qquad F_N=e,\qquad
 C_N(t)=\frac1N\sin(Nt)e.
 \tag{6.1}
\]

Then

\[
 d_N=N^{-2}\sin^2(Nt),\qquad
 B_N=N^{-1}\sin(Nt).
 \tag{6.2}
\]

Choose \(\varepsilon_N=N^{-4}\) and write

\[
 \delta_N=N^2\varepsilon_N=N^{-2},
 \qquad s=\sin(Nt).
\]

The soft states are

\[
 z_{N,\varepsilon}=\frac{s}{\sqrt{s^2+\delta_N}},
 \qquad
 a_{N,\varepsilon}
 =\frac{s_+^2}{s^2+\delta_N}.
 \tag{6.3}
\]

There are \(N\) positive components.  Including the observation-boundary
entry at \(t=0\),

\[
 \boxed{
 V^+(a_{N,\varepsilon})
 =V^-(a_{N,\varepsilon})
 =\frac{N}{1+\delta_N},}
 \tag{6.4}
\]

\[
 \boxed{
 \operatorname{TV}(a_{N,\varepsilon})
 =\frac{2N}{1+\delta_N}.}
 \tag{6.5}
\]

The ordinary quadratic budgets are

\[
 \int_0^{2\pi}d_N\,dt=\frac\pi{N^2},
 \qquad
 \int_0^{2\pi}\|C_{N,t}\|_H^2dt=\pi,
 \tag{6.6}
\]

\[
 \int_0^{2\pi}\|F_N\|_H^2dt=2\pi,
 \qquad
 \int_0^{2\pi}\|C_{N,t}+\lambda C_N\|_H^2dt
 =\pi\left(1+\frac{\lambda^2}{N^2}\right).
 \tag{6.7}
\]

More generally, for every fixed \(1\le p\le\infty\), the family is uniformly
bounded in

\[
 C_N\in W^{1,p}(0,2\pi;H),qquad
 F_N,\ C_{N,t}+\lambda C_N\in L^p(0,2\pi;H).
 \tag{6.8}
\]

Yet (6.4)--(6.5) grow like \(N\).

The extra I-style radial mass is exact:

\[
 \boxed{
 \int_0^{2\pi}
 2\lambda\theta_{N,\varepsilon}a_{N,\varepsilon}\,dt
 =\frac{\lambda\pi\sqrt{\delta_N}}
 {(1+\delta_N)^{3/2}}\longrightarrow0.}
 \tag{6.9}
\]

For each fixed \(N\), as \(\varepsilon\downarrow0\),

\[
 2z_{N,\varepsilon}^+
 \mathcal J_{N,\varepsilon}^{I}\,dt
 \stackrel{*}{\rightharpoonup}
 D\mathbf1_{\{\sin Nt>0\}}
 +2\lambda\mathbf1_{\{\sin Nt>0\}}dt.
 \tag{6.10}
\]

Its limiting positive and negative masses are

\[
 \boxed{N+2\lambda\pi\quad\text{and}\quad N,}
 \tag{6.11}
\]

respectively.  Thus the soft source, not the radial damping, carries the face
atoms.

The limit order matters.  Equations (6.4)--(6.11) take
\(\varepsilon\downarrow0\) for fixed \(N\), or a diagonal sequence with
\(N^2\varepsilon_N\to0\).  At fixed \(\varepsilon>0\), letting \(N\to\infty\)
blurs the transitions and gives

\[
 \frac{2N}{1+N^2\varepsilon}\longrightarrow0.
 \tag{6.12}
\]

### Theorem 6.1 -- abstract budget separation

No universal functional inequality can bound the relaxed face cost or the
positive soft source using only a right side that remains bounded on the
ordinary norms in (6.6)--(6.8).

This statement does not apply to a right side containing a zero count,
inverse denominator, transversality constant, second time derivative,
directional BV, or the source itself.  Most importantly, (6.1) is a smooth
Hilbert path; it is not asserted to arise from the coupled NSE observables
\((F_j,C_Q,Y)\).

## 7. A genuine NSE one-sided zero face

The abstract separation does not show that NSE creates arbitrary face counts.
It is nevertheless important to check that a positive zero-denominator face
is compatible with a genuine smooth NSE initial trace.

Work on the normalized torus and set

\[
 u_0(x)=
 (0,\cos x_1,0)+(0,0,\cos x_2).
 \tag{7.1}
\]

This field is real, zero mean, smooth, and divergence free.  Choose a smooth
real-even radial multiplier whose symbol is zero at radius \(1\) and one at
radius \(\sqrt2\).  Take \(\chi_Q=1\).

All initial vorticity modes have radius \(1\), so

\[
 W_j(0)=T_j\omega_0=0,
 \qquad C_Q(0)=0,
 \qquad d_Q(0)=0.
 \tag{7.2}
\]

The quadratic Lamb field has four target modes at

\[
 (\pm1,\pm1,0).
\]

With \(F_j=T_j\mathbb P(u_0\times\omega_0)\) and
\(G_j=\operatorname{curl}F_j\), exact Fourier convolution gives

\[
 Y(0)=1,qquad
 \|F_j(0)\|_2^2=\frac14,qquad
 \|G_j(0)\|_2^2=\frac12.
 \tag{7.3}
\]

Because \(W_j(0)=0\), the vorticity equation gives

\[
 W_{j,t}(0)=G_j(0),
 \qquad
 C_{Q,t}(0)=\operatorname{curl}G_j(0)=2F_j(0).
 \tag{7.4}
\]

Hence

\[
 \|C_{Q,t}(0)\|_2^2=1,
 \qquad
 B_{Q,t}(0)
 =\langle F_j(0),C_{Q,t}(0)\rangle=\frac12.
 \tag{7.5}
\]

Local smooth NSE existence and Taylor expansion yield, for \(t\downarrow0\),

\[
 C_Q(t)=tC_{Q,t}(0)+O(t^2),
 \qquad
 B_Q(t)=\frac t2+O(t^2),
 \qquad
 d_Q(t)=t^2+O(t^3).
 \tag{7.6}
\]

Therefore

\[
 \boxed{
 \lim_{t\downarrow0}z_Q(t)=\frac12,
 \qquad
 \lim_{t\downarrow0}a_Q(t)=\frac14.}
 \tag{7.7}
\]

This is a genuine one-sided NSE entry face.  It is an initial-jet result, not
a time step.  It does not produce an internal face, an arbitrarily large NSE
face count, or a violation of the R0.71I bound for one chosen smooth initial
time.  In fact, that initial-time bound is expected to pay this single face.

## 8. Relation to the R0.71I and R0.71L budgets

R0.71L proves

\[
 \nu\int_I\sum_{j,Q}\kappa_j^{-2}d_{j,Q}\,dt
 \lesssim\|u(0)\|_2^2.
 \tag{8.1}
\]

The family in Section 6 has denominator mass tending to zero while its face
cost diverges.  Thus (8.1), by itself, cannot pay the soft-limit faces through
a universal functional inequality.

R0.71I proves the exact one-sided BV reduction on every hard component.  The
present result identifies what happens when those components are recovered
from the global soft equation:

1. each right entry is the positive atom \(A_+\);
2. each left exit is the negative atom \(A_-\);
3. signed atoms may cancel when they collapse at the same zero;
4. their Jordan mass remains \(A_++A_-\);
5. the soft radial damping has no finite-order face atom.

The soft equation therefore validates the earlier instruction to retain all
one-sided faces.  It does not supply their uniform sum.

## 9. Literature boundary

The closest primary tools have narrower conclusions.

1. [Reshetnyak's 1968 stability theorem](https://doi.org/10.1007/BF02196453)
   underlies lower semicontinuity and continuity results for total variation
   measures.  Lower semicontinuity keeps a lower bound on total variation; it
   does not identify the extra pair of cancelling atoms in (4.13) without
   stronger convergence information.
2. [Vol'pert's BV chain rule](https://www.mathnet.ru/eng/sm4127) and the
   modern formulation by
   [Ambrosio--De Lellis--Maly](https://www.math.ias.edu/delellis/sites/math.ias.edu.delellis/files/chain100.pdf)
   apply to each fixed smooth map
   \(C\mapsto C/\sqrt{|C|^2+\varepsilon}\).  The derivative constant grows
   like \(\varepsilon^{-1/2}\), so the fixed-\(\varepsilon\) chain rule does
   not provide the uniform face limit.
3. [Fleming--Rishel coarea](https://doi.org/10.1007/BF01236935) and
   [Lochowski's crossing formula](https://arxiv.org/abs/1503.01746v4)
   can translate an already controlled BV quantity into level or crossing
   information.  They do not create a zero-level bound from Leray energy.
4. Periodic strong-solution time analyticity controls the local structure of
   one fixed observable, as described in Section 5, but gives no uniform zero
   count near a possible singular endpoint.

A bounded primary-source search using normalized vector, soft denominator,
BV/coarea, defect measure, source measure, and zero crossing did not locate a
theorem for the exact object

\[
 \frac{(B_Q^+)^2}{Y(d_Q+\varepsilon)}
\]

that identifies both one-sided face atoms and pays their NSE frame--cell sum
from energy plus denominator mass.  This is a bounded negative finding, not a
claim of nonexistence, originality, priority, or publishability.

## 10. What is closed and what remains open

### 10.1 Closed in R0.71O

1. The two soft source conventions and their exact relation are fixed.
2. The soft scalar factors as \(z_\varepsilon=\sqrt\sigma z\) and
   \(a_\varepsilon=\sigma a\) on every hard component.
3. The exact face source is \(\sigma_ta\).
4. Finite-order one-sided traces and signed/Jordan face atoms are explicit.
5. The extra soft radial damping has no finite-order atom.
6. The two raw singular pieces have opposite logarithmic divergence and must
   remain combined before the soft limit.
7. Standard hard BV and the segmented relaxed face cost are distinguished.
8. Ordinary \(W^{1,p}\)-in-time, field, and denominator-mass budgets do not control
   abstract face count.
9. A smooth NSE initial datum realizes a nonzero one-sided entry trace.

### 10.2 Not closed

1. No uniform NSE bound for the full shell--cell face sum is proved.
2. No internal NSE family with unbounded face count is constructed.
3. No bound on zero number, order, separation, or transversality follows from
   Leray energy.
4. No passage to infinitely many shells/cells or to a putative singular time
   is justified.
5. Refresh atoms and moving cutoffs remain outside this release.
6. No continuation, regularity, or singularity conclusion follows.

## 11. Route verdict and next finite gate

The R0.71O verdict is

\[
 \boxed{
 \text{soft regularization records the hard faces as source measures;}
 \quad
 \text{it does not pay their total mass}.}
 \tag{11.1}
\]

R0.71P should remain with a fixed partition.  Its finite task is to test the
weighted all-cell/all-shell entry measure

\[
 \sum_{j,Q}\kappa_j^{-2}
 \sum_{t_0\in Z_{j,Q}}A_{j,Q,+}(t_0)
 \tag{11.2}
\]

for an exact tight-frame cancellation, a coarea/analytic-zero estimate, or a
genuine NSE separation.  A bound that assumes the zero count, inverse
denominator, directional BV, or a continuation norm must be labeled
conditional.  Refresh atoms and moving cells should not be introduced until
this fixed-partition sum has a finite verdict.

## 12. Reproduction map

`research/r071o_exact_audit.py` checks the soft quotient, hard--soft
factorization, finite-order profiles, raw logarithmic cancellation,
oscillatory separation, and exact NSE Fourier initial jet with symbolic
arithmetic.

`research/r071o_independent_audit.py` imports neither the producer nor earlier
release code.  It uses adaptive quadrature for eight zero orders and seven
oscillation frequencies, and a standalone \(32^3\) FFT reconstruction of the
NSE initial face.

`research/r071o_gap_matrix.md` separates exact theorems, diagnostics,
functional separations, conditional implications, and open NSE claims.

`research/r071o_literature_audit.md` records the bounded primary-source search
and terminology boundaries.

No DNS, stochastic simulation, fitted model, GPU job, or DGX run is used.  The
question is a one-dimensional measure limit and an exact finite Fourier
initial jet; higher computational throughput would not strengthen the proof.
