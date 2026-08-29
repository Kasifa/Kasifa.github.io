# R0.73B problem freeze: Bloch near-carrier cancellation and physical kinetic finite transients

**Frozen:** 2026-08-29

**Status:** source-stage.  Every candidate below is `TO_PROVE` or
`TO_DISPROVE`.  Nothing in this file is public, formally certified, or a
claim about nonlinear Navier--Stokes.

## 1. Inherited complete row

Use the R0.72Y--R0.73A notation

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

The heat shear is

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad W_d=W_{xx}.
 \tag{1.3}
\]

All evolution intervals satisfy \(0\le s\le d<\infty\).

For \(\mu>0\), the exact Orr--Sommerfeld--Squire variables are

\[
 q=\mathcal Lv,
 \qquad \eta=i\gamma u_1-i\xi u_3,
 \tag{1.4}
\]

\[
 q_d=-\mathcal Lq-ic\left(Wq+W_{xx}\mathcal L^{-1}q\right)+F_q,
 \tag{1.5}
\]

\[
 \eta_d=(-\mathcal L-icW)\eta
 +i\xi\Lambda W_x\mathcal L^{-1}q+F_\eta.
 \tag{1.6}
\]

The component formulation remains valid when \(\mu=0\), where (1.4)--(1.6)
may be singular.

The half-open Bloch cell avoids double-counting its endpoint fiber.  At the
included representative \(\beta=-1/2\), the lowest eigenvalue is double;
the zero-lattice coefficient used below remains an exact coordinate but is
not the unique slow mode.

## 2. Near-constant Bloch coordinate

Let \(\Pi_0\) be the periodic Fourier-zero projection, \(Q_0=I-\Pi_0\),
and assume \(g>0\).  Define

\[
 h=\Pi_0(\mathcal L^{-1}q)=\Pi_0v,
 \qquad r=Q_0q,
 \qquad q=gh+r.
 \tag{2.1}
\]

For \(s_r=\mathcal L^{-1}r\), one has

\[
 r=-s_{r,xx}-2i\beta s_{r,x}+gs_r.
 \tag{2.2}
\]

The candidate exact cancellation is

\[
 \boxed{
 \Pi_0\!\left(Wr+W_{xx}\mathcal L^{-1}r\right)
 =g\Pi_0(W\mathcal L^{-1}r)
 +2i\beta\Pi_0(W_x\mathcal L^{-1}r).}
 \tag{2.3}
\]

Consequently the candidate regular system is

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
 \tag{2.4}
\]

The only new low-gap coefficient in the homogeneous coupling is physical:

\[
 \boxed{
 \frac{2|c\beta|}{g}
 =|\Lambda|\frac{2|\gamma\beta|}{\beta^2+\xi^2+\gamma^2}
 \le |\Lambda|.}
 \tag{2.5}
\]

`exactBlochNearCarrierCancellation=TO_PROVE`.

The transformed forcing is not regularized by this identity: it retains
\(g^{-1}\Pi_0F_q\).  The hybrid theorem below is therefore frozen for
\(F_q=0\), \(\mu>0\).  When \(\mu=0\), \(\beta\ne0\), the algebraic
identity remains true but the physical component constraint forces \(v=0\).

## 3. Candidate hybrid Bloch transient

Put

\[
 \lambda_\perp=(1-|\beta|)^2+\mu\ge\frac14,
 \qquad
 \|(h,r)\|_{X_g}^2=|h|^2+\|r\|_2^2.
 \tag{3.1}
\]

For \(\mu>0\), \(0<g\le1\), and \(F_q=0\), the candidate uniform
majorants are

\[
 C_c(d)=4e^{-d}+\frac{43}{8}e^{-4d},
 \qquad
 C_\Lambda(d)=e^{-d}+e^{-4d},
 \tag{3.2}
\]

\[
 J_c(s,d)=4(e^{-s}-e^{-d})
 +\frac{43}{32}(e^{-4s}-e^{-4d}),
 \tag{3.3}
\]

\[
 J_\Lambda(s,d)=(e^{-s}-e^{-d})
 +\frac14(e^{-4s}-e^{-4d}).
 \tag{3.4}
\]

The candidate theorem is

\[
 \boxed{
 \|(h(d),r(d))\|_{X_g}
 \le
 e^{-g(d-s)+|c|J_c(s,d)+|\Lambda|J_\Lambda(s,d)}
 \|(h(s),r(s))\|_{X_g}.}
 \tag{3.5}
\]

At \(\beta=0\), the orientation term vanishes and the sharper R0.73A
constant must be retained instead of (3.2).

`blochNearCarrierFiniteTransient=TO_PROVE`.

## 4. Candidate complete physical kinetic theorem

For every complete divergence-free component row, R0.72Y gives

\[
 \frac12\frac d{dd}\|u\|_2^2
 +\|A_\beta u\|_2^2+\mu\|u\|_2^2
 =-\Lambda\operatorname{Re}\langle W_xv,u_3\rangle
 +\operatorname{Re}\langle F,u\rangle.
 \tag{4.1}
\]

The exact profile norm and its primitive are

\[
 \|W_x(d)\|_\infty=\frac12(e^{-d}+e^{-4d}),
 \tag{4.2}
\]

\[
 K(s,d)=\int_s^d\|W_x(\tau)\|_\infty\,d\tau
 =\frac12(e^{-s}-e^{-d})
 +\frac18(e^{-4s}-e^{-4d}).
 \tag{4.3}
\]

The proposed row bound is

\[
 \boxed{
 \|U_j(d,s)\|_{L^2_u\to L^2_u}
 \le
 \exp\!\left[-g_j(d-s)+\frac{|\Lambda|}{2}K(s,d)\right].}
 \tag{4.4}
\]

In particular,

\[
 \|U_j(d,s)\|
 \le e^{5|\Lambda|e^{-s}/16}e^{-g_j(d-s)}.
 \tag{4.5}
\]

For \(\mu>0\), this is exactly the kinetic OS--Squire norm

\[
 \|u\|_2^2
 =\frac1\mu\left(
 \|\mathcal L^{-1/2}q\|_2^2+\|\eta\|_2^2\right).
 \tag{4.6}
\]

The direct-sum candidate is

\[
 \boxed{
 \left(\sum_j e^{2g_j(d-s)}\|u_j(d)\|_2^2\right)^{1/2}
 \le e^{|\Lambda|K(s,d)/2}
 \left(\sum_j\|u_j(s)\|_2^2\right)^{1/2}.}
 \tag{4.7}
\]

`completePhysicalKineticFiniteTransient=TO_PROVE` and
`blochUniformPhysicalVelocityDirectSumAtViscousRates=TO_PROVE`.

These are viscous-row-rate statements.  They do not claim an \(A_2\),
enhanced-dissipation, or prefactor-one theorem.

## 5. Candidate sharp path separation

The exact zero-horizontal-frequency lift-up row from R0.72Y gives

\[
 \frac{\|u(d)\|_2^2}{\|u(s)\|_2^2}
 =1+\frac{\Lambda^2(d-s)^2}{8}
 \left(e^{-2d}+e^{-8d}\right)
 \tag{5.1}
\]

when its diffusive horizontal factor is zero.  Thus no bound uniform in
\(\Lambda\) is possible.

On the physical two-dimensional path \(\beta=\xi=0\),
\(\mu=\gamma^2\), fixed \(c\ne0\) means
\(|\Lambda|=|c|/\sqrt\mu\).  Starting from \(h=1,r=0\), the regular
R0.73A system has

\[
 r_d(s)=-ic(W_{xx}(s)+\mu W(s)).
 \tag{5.2}
\]

The candidate lower-bound argument is that for one sufficiently small fixed
\(\tau_0>0\), the low Fourier part of \(r(s+\tau_0)\) stays bounded away
from zero as \(\mu\downarrow0\), while its kinetic weight is
\(\mu^{-1/2}\mathcal L_\mu^{-1/2}\).  Hence the physical kinetic
propagator cannot be uniform on fixed-\(c\) paths.

`lambdaIndependentKineticPrefactor=TO_DISPROVE` and
`fixedCUniformLowGapKineticPropagator=TO_DISPROVE`.

## 6. Explicit exclusions

The following remain outside R0.73B unless a separate proof is found:

- an \(A_2\)-rate complete OS--Squire direct sum;
- a polynomially sharp upper prefactor in \(|\Lambda|\);
- a uniformly bounded transported adjoint tangent projection;
- nonlinear mode convolution or a perturbative bootstrap;
- any continuation criterion for general three-dimensional solutions;
- the Clay Millennium problem.
