# R0.73B report source: Bloch near-carrier cancellation and a complete physical-kinetic finite-transient theorem

**Date:** 2026-08-29

**Status:** analytic pass after independent audit.  The deterministic
certificate, formal-figure contract, and publication gate remain required
before any claim key is released as closed.

**Keywords:** linearized Navier--Stokes, time-dependent shear, physical
kinetic energy, Orr--Sommerfeld--Squire, Bloch fiber, low wave number,
lift-up, finite transient

---

## 0. Direct decision

There are two different low-gap statements, and R0.73B must not merge them.

First, the homogeneous Orr--Sommerfeld equation has an exact zero-lattice
Bloch carrier coordinate.  Its apparent coupling-side \(g^{-1}\) term reduces
to the physical orientation factor

\[
 \omega_{\beta,\gamma,\xi}
 =\frac{2\gamma\beta}{\beta^2+\xi^2+\gamma^2},
 \qquad |\omega_{\beta,\gamma,\xi}|\le1.
 \tag{0.1}
\]

This gives a finite-transient theorem in a hybrid
carrier/vorticity norm \(X_g\).  It extends the exact cancellation of R0.73A
from \(\beta=0\) to the full low-gap Bloch cell.

Second, the complete divergence-free velocity equation has a simpler and
stronger conclusion at the viscous row rate.  The shear production is paid
directly in physical kinetic energy, and the exact heat path satisfies
\(\|W_x\|_{L^1_dL^\infty_x}<\infty\).  Consequently every Fourier--Bloch
row, including its Squire component and exceptional component-coordinate
rows, has a finite all-time transient.  The row estimates sum without a
row-count loss.

The analytically closed claim keys, still awaiting deterministic and release
gates, are

\[
\boxed{
\begin{aligned}
\texttt{exactBlochNearCarrierCancellation}&=\texttt{ANALYTIC\_PASS},\\
\texttt{exactBlochCarrierSystem}&=\texttt{ANALYTIC\_PASS},\\
\texttt{blochNearCarrierFiniteTransient}&=\texttt{ANALYTIC\_PASS},\\
\texttt{exactHeatShearGradientPrimitive}&=\texttt{ANALYTIC\_PASS},\\
\texttt{completePhysicalKineticFiniteTransient}&=\texttt{ANALYTIC\_PASS},\\
\texttt{completeOSSquireKineticFiniteTransient}&=\texttt{ANALYTIC\_PASS},\\
\texttt{blochUniformPhysicalVelocityDirectSumAtViscousRates}
 &=\texttt{ANALYTIC\_PASS},\\
\texttt{physicalKineticForcedDuhamel}&=\texttt{ANALYTIC\_PASS},\\
\texttt{sharpKineticShearFormCoefficientAndLowGapLimit}
 &=\texttt{ANALYTIC\_PASS},\\
\texttt{nearCarrierInstantaneousKineticGrowth}&=\texttt{ANALYTIC\_PASS}.
\end{aligned}}
\tag{0.2}
\]

The independently proved negative statements are

\[
\boxed{
\begin{aligned}
\texttt{lambdaIndependentKineticPrefactor}&=\texttt{FALSE},\\
\texttt{fixedCUniformLowGapKineticPropagator}&=\texttt{FALSE},\\
\texttt{allRowPrefactorOneKineticContraction}&=\texttt{FALSE}.
\end{aligned}}
\tag{0.3}
\]

The following remain open:

\[
\boxed{
\begin{aligned}
\texttt{polynomiallySharpLambdaKineticPrefactor}&=\texttt{OPEN},\\
\texttt{completeOSSquireA2DirectSum}&=\texttt{OPEN},\\
\texttt{transportedAdjointPressureA2Modulation}&=\texttt{OPEN},\\
\texttt{nonlinearNavierStokes}&=\texttt{OPEN},\\
\texttt{Clay}&=\texttt{OPEN}.
\end{aligned}}
\tag{0.4}
\]

The word "complete" in (0.2) refers only to the complete *linearized row*.
It does not mean the nonlinear equation or the Millennium problem.

---

## 1. Exact inherited system

All one-dimensional norms and inner products use normalized periodic
measure,

\[
 \langle f,g\rangle_0=\frac1{2\pi}
 \int_0^{2\pi}\overline f(x)g(x)\,dx,
 \qquad \|1\|_2=1.
 \tag{1.0}
\]

Let

\[
 A_\beta=\partial_x+i\beta,
 \qquad D_\beta=-iA_\beta,
 \qquad \mathcal L=D_\beta^2+\mu,
 \tag{1.1}
\]

\[
 \mu=\xi^2+\gamma^2,
 \qquad g=\beta^2+\mu,
 \qquad c=\gamma\Lambda,
 \qquad \beta\in[-1/2,1/2).
 \tag{1.2}
\]

The half-open Bloch cell avoids double-counting the boundary fiber.  At its
included endpoint \(\beta=-1/2\) (equivalently at the excluded representative
\(\beta=1/2\)), the two lowest lattice eigenvalues are tied.  The identity
below still holds, but the zero-lattice carrier must not be called the unique
slow mode there.

The exact heat-decaying shear is

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad W_d=W_{xx}.
 \tag{1.3}
\]

Throughout, evolution times satisfy \(0\le s\le d<\infty\).

For \(\mu>0\), define

\[
 q=\mathcal Lv,
 \qquad \eta=i\gamma u_1-i\xi u_3.
 \tag{1.4}
\]

R0.72Y proved the exact triangular system

\[
 q_d=-\mathcal Lq-ic\left(Wq+W_{xx}\mathcal L^{-1}q\right)+F_q,
 \tag{1.5}
\]

\[
 \eta_d=(-\mathcal L-icW)\eta
 +i\xi\Lambda W_x\mathcal L^{-1}q+F_\eta.
 \tag{1.6}
\]

The primitive velocity row, valid also at the exceptional values where
(1.4) degenerates, is

\[
 u_d=-\mathcal Lu
 -\mathbb P_j\!\left(icWu+\Lambda W_xve_3\right)+F.
 \tag{1.7}
\]

---

## 2. Exact Bloch near-carrier cancellation

Let \(\Pi_0\) denote the periodic Fourier-zero coefficient and
\(Q_0=I-\Pi_0\).  For the physical hybrid theorem take \(\mu>0\) and set

\[
 h=\Pi_0(\mathcal L^{-1}q)=\Pi_0v,
 \qquad r=Q_0q,
 \qquad q=gh+r.
 \tag{2.1}
\]

When \(\mu=0\) and \(\beta\ne0\), the algebraic identity below still makes
sense because \(g>0\), but the component divergence constraint forces
\(v=0\) on that exceptional physical row.  R0.73B therefore states the
nontrivial hybrid theorem only for \(\mu>0\); all exceptional rows are
covered later in primitive velocity components.

When \(\beta\ne0\), \(h\) is the coefficient of the zero lattice mode in
the Bloch envelope.  It is not the literal spatial mean of the full
quasiperiodic physical field.

Put \(s_r=\mathcal L^{-1}r\).  Since \(\Pi_0r=0\) and \(\mathcal L\) is
diagonal on periodic Fourier modes, \(\Pi_0s_r=0\).  Moreover

\[
 r=-s_{r,xx}-2i\beta s_{r,x}+gs_r.
 \tag{2.2}
\]

Two periodic integrations by parts give

\[
 \Pi_0(-Ws_{r,xx})=-\Pi_0(W_{xx}s_r),
 \tag{2.3}
\]

and one integration by parts gives

\[
 \Pi_0(-2i\beta Ws_{r,x})
 =2i\beta\Pi_0(W_xs_r).
 \tag{2.4}
\]

Therefore

\[
 \boxed{
 \Pi_0\!\left(Wr+W_{xx}\mathcal L^{-1}r\right)
 =g\Pi_0(W\mathcal L^{-1}r)
 +2i\beta\Pi_0(W_x\mathcal L^{-1}r).}
 \tag{2.5}
\]

This is an infinite-dimensional identity for every mean-zero \(r\in L^2\).
Indeed \(s_r\in H^2\), so the integrations by parts are legitimate; the
identity can equivalently be checked first on trigonometric polynomials and
extended by density.

Since

\[
 \mathcal L^{-1}(gh)=h,
 \qquad
 W(gh)+W_{xx}\mathcal L^{-1}(gh)=h(gW+W_{xx}),
 \tag{2.6}
\]

and both \(W\) and \(W_{xx}\) have zero mean, (1.5) becomes exactly

\[
 \boxed{
 \begin{aligned}
 h_d={}&-gh-ic\Pi_0(W\mathcal L^{-1}r)
 +\frac{2c\beta}{g}\Pi_0(W_x\mathcal L^{-1}r)
 +g^{-1}\Pi_0F_q,\\
 r_d={}&-\mathcal Lr
 -icQ_0\!\left(Wr+W_{xx}\mathcal L^{-1}r\right)\\
 &-ic\,h(W_{xx}+gW)+Q_0F_q.
 \end{aligned}}
 \tag{2.7}
\]

The apparently singular coefficient in (2.7) is

\[
 \frac{2c\beta}{g}
 =\Lambda\frac{2\gamma\beta}
 {\beta^2+\xi^2+\gamma^2}.
 \tag{2.8}
\]

The elementary inequality \(2|\gamma\beta|\le\gamma^2+\beta^2\le g\)
proves

\[
 \boxed{\left|\frac{2c\beta}{g}\right|\le|\Lambda|.}
 \tag{2.9}
\]

Thus the physical orientation removes the raw \(g^{-1}\) divergence from
the **homogeneous coupling**.  It does not remove the amplitude payment
\(|\Lambda|\), and arbitrary OS forcing still pays the explicit carrier
factor \(g^{-1}\Pi_0F_q\) in (2.7).

---

## 3. Homogeneous hybrid low-gap Bloch estimate

Assume throughout this section that \(\mu>0\), \(0<g\le1\), and
\(F_q=0\).

Let

\[
 \ell=(1-|\beta|)^2+\mu
 =\min_{n\ne0}\big((n+\beta)^2+\mu\big).
 \tag{3.1}
\]

On the half-open Bloch cell, \(\ell\ge g\).  For
\(\beta\in[-1/2,1/2)\), one also has \(\ell\ge1/4\).  Define

\[
 \|(h,r)\|_{X_g}^2=|h|^2+\|r\|_2^2.
 \tag{3.2}
\]

The exact coefficient ledger is

\[
 B=\|W\|_\infty+\ell^{-1}\|W_{xx}\|_\infty,
 \tag{3.3}
\]

\[
 A_1=|c|\ell^{-1}\|W\|_2,
 \qquad
 A_2=\frac{2|c\beta|}{g}\ell^{-1}\|W_x\|_2,
 \qquad
 A_3=|c|\|W_{xx}+gW\|_2.
 \tag{3.4}
\]

Taking real parts in (2.7) gives

\[
 \frac12\frac d{dd}\|(h,r)\|_{X_g}^2
 \le-g|h|^2-\ell\|r\|_2^2
 +|c|B\|r\|_2^2+(A_1+A_2+A_3)|h|\|r\|_2.
 \tag{3.5}
\]

Hence

\[
 \frac12\frac d{dd}\|(h,r)\|_{X_g}^2
 \le\left[-g+C_{\beta,\mu,c,\Lambda}(d)\right]
 \|(h,r)\|_{X_g}^2,
 \tag{3.6}
\]

where

\[
 C_{\beta,\mu,c,\Lambda}
 =|c|B+\frac12(A_1+A_2+A_3).
 \tag{3.7}
\]

The exact normalized \(L^2\) profile quantities are

\[
 \|W\|_2^2=\frac18e^{-2d}+\frac1{32}e^{-8d},
 \qquad
 \|W_x\|_2^2=\frac18(e^{-2d}+e^{-8d}),
 \tag{3.8}
\]

\[
 \|W_{xx}+gW\|_2^2
 =\frac{(1-g)^2}{8}e^{-2d}
 +\frac{(4-g)^2}{32}e^{-8d}.
 \tag{3.9}
\]

For a simple uniform theorem, restrict to \(0<g\le1\).  Using
\(\ell^{-1}\le4\), (2.9), normalized \(L^2\le L^\infty\), and

\[
 \begin{aligned}
 \|W\|_\infty&\le\frac12e^{-d}+\frac14e^{-4d},\\
 \|W_{xx}\|_\infty&\le\frac12e^{-d}+e^{-4d},\\
 \|W_x\|_\infty&=\frac12e^{-d}+\frac12e^{-4d},
 \end{aligned}
 \tag{3.10}
\]

one obtains

\[
 C_{\beta,\mu,c,\Lambda}(d)
 \le |c|\left(4e^{-d}+\frac{43}{8}e^{-4d}\right)
 +|\Lambda|(e^{-d}+e^{-4d}).
 \tag{3.11}
\]

Define

\[
 J_c(s,d)=4(e^{-s}-e^{-d})
 +\frac{43}{32}(e^{-4s}-e^{-4d}),
 \tag{3.12}
\]

\[
 J_\Lambda(s,d)=(e^{-s}-e^{-d})
 +\frac14(e^{-4s}-e^{-4d}).
 \tag{3.13}
\]

Gronwall then yields the audited homogeneous all-start bound

\[
 \boxed{
 \|(h(d),r(d))\|_{X_g}
 \le e^{-g(d-s)+|c|J_c(s,d)+|\Lambda|J_\Lambda(s,d)}
 \|(h(s),r(s))\|_{X_g}.}
 \tag{3.14}
\]

At \(\beta=0\), \(A_2=0\), \(g=\mu\), and the sharper R0.73A
majorant applies.  The purpose of (3.14) is uniform Bloch regularity, not
constant optimization.

---

## 4. Exact physical kinetic identity

For every complete divergence-free velocity row, take the real \(L^2\)
inner product of (1.7) with \(u\).  The scalar potential is skew and the
Leray projection is orthogonal.  Thus

\[
 \boxed{
 \frac12\frac d{dd}\|u\|_2^2
 +\|A_\beta u\|_2^2+\mu\|u\|_2^2
 =-\Lambda\operatorname{Re}\langle W_xv,u_3\rangle
 +\operatorname{Re}\langle F,u\rangle.}
 \tag{4.1}
\]

The identity is first justified for smooth divergence-free row data (or a
finite Galerkin approximation) and physical projected forcing.  The
estimate below is stable under approximation, so density extends the
evolution bound to divergence-free \(L^2\) mild solutions.  Gradient parts
of an unprojected force vanish after the row Leray projection.

The Fourier gap gives

\[
 \|A_\beta u\|_2^2+\mu\|u\|_2^2
 \ge g\|u\|_2^2.
 \tag{4.2}
\]

The production term has no sign, but it is exactly bounded in physical
components:

\[
 |\Lambda\operatorname{Re}\langle W_xv,u_3\rangle|
 \le\frac{|\Lambda|}{2}\|W_x\|_\infty\|u\|_2^2.
 \tag{4.3}
\]

The orientation singularity visible in raw Squire coordinates is absent in
(4.3): the wall-normal and streamwise components are already normalized in
the same physical kinetic norm.  This does not make \(|\Lambda|\) disappear.

For the exact profile, equality in the \(L^\infty\) norm is attained at
\(x=\pi\):

\[
 \boxed{
 \|W_x(d)\|_\infty=\frac12(e^{-d}+e^{-4d}).}
 \tag{4.4}
\]

Therefore

\[
 \boxed{
 K(s,d)=\int_s^d\|W_x(\tau)\|_\infty\,d\tau
 =\frac12(e^{-s}-e^{-d})
 +\frac18(e^{-4s}-e^{-4d}).}
 \tag{4.5}
\]

In particular,

\[
 \frac12K(s,\infty)
 =\frac14e^{-s}+\frac1{16}e^{-4s}
 \le\frac5{16}e^{-s}.
 \tag{4.6}
\]

---

## 5. Complete row and forced estimates

For the homogeneous equation, (4.1)--(4.3) imply

\[
 \frac d{dd}\|u\|_2
 \le\left[-g+\frac{|\Lambda|}{2}\|W_x\|_\infty\right]\|u\|_2
 \tag{5.1}
\]

in the standard regularized sense at a zero of the norm.  Consequently,

\[
 \boxed{
 \|U_j(d,s)\|_{L^2_u\to L^2_u}
 \le
 \exp\!\left[-g_j(d-s)+\frac{|\Lambda|}{2}K(s,d)\right].}
 \tag{5.2}
\]

The global all-time version is

\[
 \boxed{
 \|U_j(d,s)\|_{L^2_u\to L^2_u}
 \le e^{5|\Lambda|e^{-s}/16}e^{-g_j(d-s)}.}
 \tag{5.3}
\]

For physical projected component forcing
\(F_j=\mathbb P_jf_j\in L^1_{\rm loc}(L^2)\), variation of constants gives

\[
 \boxed{
 \begin{aligned}
 \|u(d)\|_2
 &\le G_j(d,s)\|u(s)\|_2\\
 &\quad+\int_s^dG_j(d,\tau)\|F(\tau)\|_2\,d\tau,
 \end{aligned}}
 \tag{5.4}
\]

where

\[
 G_j(d,s)=
 \exp\!\left[-g_j(d-s)+\frac{|\Lambda|}{2}K(s,d)\right].
 \tag{5.5}
\]

The forcing in (5.4) is the physical projected component forcing.  It is
not interchangeable with arbitrary independently prescribed \(F_q,F_\eta\)
without the velocity-recovery weights.

---

## 6. Exact OS--Squire kinetic interpretation

When \(\mu>0\), R0.72Y proved

\[
 u_1=\frac{i}{\mu}(\xi A_\beta v-\gamma\eta),
 \qquad
 u_3=\frac{i}{\mu}(\gamma A_\beta v+\xi\eta),
 \tag{6.1}
\]

and

\[
 \boxed{
 \|u\|_2^2
 =\frac1\mu\left(
 \|\mathcal L^{-1/2}q\|_2^2+\|\eta\|_2^2\right).}
 \tag{6.2}
\]

Thus (5.2) is a complete Orr--Sommerfeld--Squire propagator theorem in the
exact physical kinetic norm.  It does not estimate \(q\) and \(\eta\) in
unweighted \(L^2\).

For the carrier decomposition (2.1), the OS contribution to (6.2) is

\[
 \frac1\mu\|\mathcal L^{-1/2}q\|_2^2
 =\frac g\mu|h|^2
 +\frac1\mu\|\mathcal L^{-1/2}r\|_2^2.
 \tag{6.3}
\]

Equation (6.3) explains why \(X_g\) and kinetic energy are complementary,
not equivalent, low-gap ledgers.  At \(\beta=0\), the carrier weight is
exactly one; the mean-zero vorticity weight still carries \(\mu^{-1}\).

At \(\mu=0\), (6.1)--(6.3) are invalid.  The component estimate
(5.2) remains valid and therefore covers the exceptional rows without a
pseudoinverse convention.

---

## 7. Bloch/Fourier direct sum

The complete physical space in the frozen periodic geometry is the discrete
orthogonal sum of the invariant rows derived in R0.72Y.  Apply (5.2) first
to any finite set of rows, square and sum, and then let the finite sets
increase to all rows.  Monotone convergence and Parseval give the
heat-weighted direct-sum estimate

\[
 \boxed{
 \left(\sum_j e^{2g_j(d-s)}\|u_j(d)\|_2^2\right)^{1/2}
 \le e^{|\Lambda|K(s,d)/2}
 \left(\sum_j\|u_j(s)\|_2^2\right)^{1/2}.}
 \tag{7.1}
\]

Dropping the row weights gives

\[
 \boxed{
 \|U(d,s)\|_{L^2_\sigma\to L^2_\sigma}
 \le e^{|\Lambda|K(s,d)/2}
 \le e^{5|\Lambda|e^{-s}/16}.}
 \tag{7.2}
\]

Minkowski's integral inequality gives the corresponding unweighted forced
direct sum for \(F\in L^1_{\rm loc}(L^2_\sigma)\):

\[
 \boxed{
 \|u(d)\|_{L^2_\sigma}
 \le e^{|\Lambda|K(s,d)/2}\|u(s)\|_{L^2_\sigma}
 +\int_s^d e^{|\Lambda|K(\tau,d)/2}
 \|F(\tau)\|_{L^2_\sigma}\,d\tau.}
 \tag{7.3}
\]

A heat-weighted forced output would require the corresponding row-weighted
forcing norm inside the time integral; (7.3) does not claim that stronger
statement.  In a genuinely continuous Bloch model the same proof uses the
orthogonal direct integral and Tonelli in place of the discrete sum.

There is no row-count factor.  There is also no global strict decay in
(7.2), because the exact zero row contains undamped constant velocity and
lift-up-compatible component variables.  The theorem is a finite-transient
direct sum, not an enhanced-dissipation direct sum.

---

## 8. The \(\Lambda\) payment is unavoidable

Take the exact zero-horizontal-frequency lift-up solution from R0.72Y,
with constant wall-normal velocity at time \(s\) and zero tangential
velocity.  Then

\[
 u_3(d,x)=-\Lambda(d-s)W_x(d,x)v_0
 \tag{8.1}
\]

and, in normalized \(L^2\),

\[
 \boxed{
 \frac{\|u(d)\|_2^2}{\|u(s)\|_2^2}
 =1+\frac{\Lambda^2(d-s)^2}{8}
 \left(e^{-2d}+e^{-8d}\right).}
 \tag{8.2}
\]

For example, at \(s=0,d=1\),

\[
 \|U(1,0)\|
 \ge\left[1+\frac{\Lambda^2}{8}
 (e^{-2}+e^{-8})\right]^{1/2}.
 \tag{8.3}
\]

Hence any all-row physical kinetic bound must grow at least linearly in
\(|\Lambda|\) along this family.  In particular, a \(\Lambda\)-independent
prefactor and an all-row prefactor-one contraction are false.

The upper bound (7.2) is exponential in \(|\Lambda|\), while (8.3) is only
linear.  R0.73B does not claim that the upper dependence is sharp.

---

## 9. Fixed \(\Lambda\) and fixed \(c\) are different limits

On the physical two-dimensional row

\[
 \beta=\xi=0,
 \qquad \mu=\gamma^2,
 \qquad c=\gamma\Lambda,
 \tag{9.1}
\]

bounded \(\Lambda\) implies \(c\to0\) as \(\mu\downarrow0\).  Equation
(5.3) is then uniform in \(\mu\) in physical kinetic energy.

By contrast, fixed \(c\ne0\) implies

\[
 |\Lambda|=\frac{|c|}{\sqrt\mu}\longrightarrow\infty.
 \tag{9.2}
\]

Start the regular R0.73A system from \(h(s)=1,r(s)=0\).  Its exact initial
derivative is

\[
 r_d(s)=-ic(W_{xx}(s)+\mu W(s)).
 \tag{9.3}
\]

For fixed \(c\), work on
\(X=\mathbb C\oplus Q_0L^2\).  On every compact time interval the regular
\((h,r)\) generator is the heat generator plus a uniformly bounded
perturbation.  Moreover

\[
 \|\mathcal L_\mu^{-1}Q_0-
 \mathcal L_0^{-1}Q_0\|_{2\to2}\longrightarrow0,
 \qquad
 e^{-t\mathcal L_\mu}Q_0=e^{-\mu t}e^{t\partial_x^2}Q_0.
 \tag{9.4}
\]

The Duhamel formula and a standard perturbation estimate therefore give
operator-norm convergence of the evolution families on compact intervals.
For the \(\mu=0\) limiting solution,

\[
 P_{1,2}r_0(s+\tau)
 =-ic\tau W_{xx}(s)+O(\tau^2),
 \tag{9.5}
\]

where \(P_{1,2}\) projects onto modes \(\{\pm1,\pm2\}\).  Choose one
sufficiently small fixed \(\tau_0>0\).  Continuity in \(\mu\) gives a
constant \(a_0>0\), independent of sufficiently small \(\mu\), such that

\[
 \|P_{1,2}r_\mu(s+\tau_0)\|_2\ge a_0.
 \tag{9.6}
\]

For \(0<\mu\le1\), the four projected eigenvalues are at most five, so

\[
 \|\mathcal L_\mu^{-1/2}r_\mu(s+\tau_0)\|_2
 \ge5^{-1/2}a_0.
 \tag{9.7}
\]

The exact OS kinetic identity now yields

\[
 \|u(s+\tau_0)\|_2
 \ge \frac{a_0}{\sqrt{5\mu}},
 \qquad \|u(s)\|_2=1.
 \tag{9.8}
\]

Thus a fixed-\(c\), \(\mu\)-uniform physical kinetic propagator is false.
The same evolution remains uniformly bounded in the R0.73A hybrid
\(X_\mu\) norm.  This is a norm-and-parameter-path separation, not a
contradiction.

Here \(\gamma=\sqrt\mu\downarrow0\) is a long-wave family across the row
parameter (equivalently across expanding physical periods).  It is not a
claim that a single fixed periodic box contains discrete nonzero frequencies
converging continuously to zero.

---

## 10. Sharp two-dimensional OS shear coefficient

The complete-row estimate uses the elementary pointwise bound (4.3).  On
the physical two-dimensional OS row

\[
 \beta=\xi=0,\qquad \mu=\gamma^2>0,
 \tag{10.1}
\]

one can identify the best instantaneous shear-form coefficient.  With
\(v=\mathcal L_\mu^{-1}q\), define

\[
 E_\mu(v)=\mu^{-1}\langle\mathcal L_\mu v,v\rangle
 =\|v\|_2^2+\mu^{-1}\|v_x\|_2^2.
 \tag{10.2}
\]

Periodic integration by parts gives the exact identity

\[
 \frac12E_\mu'
\mu^{-1}\|\mathcal L_\mu v\|_2^2
=\frac c\mu\operatorname{Im}\int W_xv_x\overline v\,dx.
 \tag{10.3}
\]

Put

\[
 \rho_\mu(d)=\frac1{\sqrt\mu}
 \sup_{v\ne0}
 \frac{\left|\operatorname{Im}\int W_xv_x\overline v\,dx\right|}
 {E_\mu(v)}.
 \tag{10.4}
\]

Then

\[
 \|U_{\rm OS}(d,s)\|_{\mathcal K_\mu\to\mathcal K_\mu}
 \le\exp\!\left[-\mu(d-s)+|\Lambda|
 \int_s^d\rho_\mu(\tau)\,d\tau\right],
 \tag{10.5}
\]

and

\[
 \rho_\mu
 =\sqrt\mu\left\|\mathcal L_\mu^{-1/2}
 \left[-i\left(W_x\partial_x+\frac12W_{xx}\right)\right]
 \mathcal L_\mu^{-1/2}\right\|.
 \tag{10.6}
\]

The operator is self-adjoint and banded.  Splitting the carrier from the
mean-zero block gives

\[
 \rho_\mu(d)\le\min\left\{
 \frac12\|W_x\|_\infty,
 \frac{\delta_\mu+
 \sqrt{\delta_\mu^2+\|W_x\|_2^2}}2\right\},
 \qquad
 \delta_\mu=\|W_x\|_\infty\sqrt{\frac\mu{1+\mu}}.
 \tag{10.7}
\]

The complete operator-norm argument in
`research/r073b_kinetic_form_proof.md` proves

\[
 \boxed{
 \lim_{\mu\downarrow0}\rho_\mu(d)
 =\frac12\|W_x(d)\|_2
 =\frac{\sqrt{e^{-2d}+e^{-8d}}}{4\sqrt2}.}
 \tag{10.8}
\]

Dominated convergence then yields the integrated low-gap coefficient

\[
 \boxed{
 \lim_{\mu\downarrow0}\int_0^\infty\rho_\mu(d)\,dd
 =\frac1{4\sqrt2}\int_0^1\sqrt{1+y^6}\,dy
 =0.188106027072\ldots.}
 \tag{10.9}
\]

This sharpens an instantaneous OS logarithmic coefficient.  It is not the
exact maximum transient gain, and it does not replace the complete-row
constant when Squire and exceptional rows are included.

---

## 11. Exact carrier--tangent instantaneous-growth witness

Fix a time \(d\), assume \(\Lambda\ne0\), and let

\[
 A=\|W_x\|_2^2,
 \qquad D=A+\mu\|W\|_2^2,
 \qquad B=\|\mathcal L_\mu W\|_2^2.
 \tag{11.1}
\]

For real \(h,\varepsilon\), set

\[
 u_1=0,
 \quad v=h+i\operatorname{sgn}(\gamma)
 \operatorname{sgn}(\Lambda)\sqrt\mu\,\varepsilon W,
 \quad u_3=-\operatorname{sgn}(\Lambda)\varepsilon W_x.
 \tag{11.2}
\]

This smooth complex Fourier-row field is exactly divergence-free.  Its
kinetic metric, viscous form, and shear cross term are

\[
 \|u\|_2^2=h^2+D\varepsilon^2,
 \qquad
 \|u_x\|_2^2+\mu\|u\|_2^2=\mu h^2+B\varepsilon^2,
 \qquad
 \mathcal S=|\Lambda|Ah\varepsilon.
 \tag{11.3}
\]

The largest instantaneous logarithmic growth rate of the norm on this
two-direction carrier--tangent plane is therefore

\[
 \lambda_{\rm trial}
 =-\frac12\left(\mu+\frac BD\right)
 +\frac12\sqrt{\left(\mu-\frac BD\right)^2
 +\frac{\Lambda^2A^2}{D}},
 \tag{11.4}
\]

with the exact sign criterion

\[
 \boxed{\lambda_{\rm trial}>0
 \quad\Longleftrightarrow\quad
 \Lambda^2A^2>4\mu B.}
 \tag{11.5}
\]

For every fixed nonzero \(\Lambda\), (11.5) holds for all sufficiently
small \(\mu\).  A short interval of strict kinetic growth follows, so a
prefactor-one contraction is false even on the bounded-\(\Lambda\) path.
At finite \(\mu\) the vorticity tangent is
\(\sqrt\mu\mathcal L_\mu W\), becoming proportional to
\(-\sqrt\mu W_{xx}\) only in the low-gap limit.

---

## 12. Literature boundary

Several parts of the framework have strong precedents.

- Colombo--Dolce--Montalto--Ventura prove a closely related stationary
  long-wave zero-mode cancellation and long-wave instability for general
  periodic shear profiles in
  [*Long-wave instability of periodic shear flows for the 2D
  Navier--Stokes equations*](https://arxiv.org/html/2509.18070v2).
  Their result prevents any universal low-wave decay claim, but it does not
  supply the present nonautonomous complete-velocity estimate.
- Jerome--Chomaz give the exact OS--Squire physical kinetic energy and the
  singular lift-up scaling in
  [*Extended Squire's transformation and its consequences on transient
  growth*](https://arxiv.org/html/1601.07598).  Their transformation assumes
  nonzero streamwise frequency and a stationary confined shear.
- Li--Wei--Zhang use a direction-dependent good unknown for the stationary
  three-dimensional Kolmogorov flow in
  [*Pseudospectral bound and transition threshold for the 3D Kolmogorov
  flow*](https://arxiv.org/html/1801.05645).  Their nonzero discrete
  streamwise mode avoids the present continuous low-gap boundary.
- Wei--Zhang--Zhao treat an active heat-decaying single-harmonic
  nonautonomous operator in
  [*Linear inviscid damping and enhanced dissipation for the Kolmogorov
  flow*](https://arxiv.org/html/1711.01822).  Their projected theorem does
  not contain the double-harmonic collision, Squire history, or Bloch
  near-carrier coordinate.
- Li--Zhao construct an all-start active propagator for strictly monotone
  time-dependent shear in
  [*Asymptotic stability in the critical space of 2D monotone shear flow in
  the viscous fluid*](https://arxiv.org/html/2306.03555v1).  Their spectral
  and geometric hypotheses exclude the present periodic collision.

The bounded search did not find the exact combination of the two-harmonic
heat path, the Bloch near-carrier cancellation, exceptional component rows,
complete OS--Squire physical energy, and the heat-weighted direct sum.
That statement is a bounded non-collision result, not a proof of novelty or
priority.

---

## 13. Research value and strict boundary

If the independent audit and certificate pass, R0.73B will close the
previously open *finite-transient, viscous-row-rate* physical velocity direct
sum.  It also identifies the exact Bloch replacement for the R0.73A hidden
mean cancellation and proves that the only new low-gap quotient is a bounded
physical orientation factor.

This does not close the stronger mechanism needed for the Millennium
problem.  The estimate has an exponential \(|\Lambda|\) prefactor, no
\(A_2\) or enhanced-dissipation rate, no nonlinear convolution estimate,
and no scale-critical bootstrap.  The next legitimate gate would be to ask
whether the complete row admits a sharper \(\Lambda\)-weighted modulation
or an \(A_2\) estimate on a spectrally stable projected class.  Adjoint
pressure cost remains part of that sharper problem; it is not needed for the
viscous-rate physical energy theorem proved here.
