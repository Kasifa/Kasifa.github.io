# R0.72Y report source: complete Fourier--Leray rows, forced scalar transfer, and the exact lift-up boundary

**Date:** 2026-08-28

**Status:** this section reconstructs the complete three-dimensional
linearization about the exact heat-shear background, including the pressure
Poisson equation, Bloch--Leray rows, Orr--Sommerfeld--Squire variables,
velocity recovery, and the exceptional zero-horizontal-frequency rows.  The
strong scalar invariant rows inherit the R0.72X all-start semigroup.  For
those rows, the forced spacetime map is \(O(\alpha^2)\) for \(L_x^2\)
forcing, \(O(\alpha)\) for standard covariant \(H^{-1}\) forcing, and
\(O(\alpha^2)\) for the semiclassical negative norm.  Both latter powers are
sharp.  Standard \(H^{-1}\) forcing has no vanishing
\(L_d^\infty L_x^2\) endpoint gain.  An exact \(K_z=0\) lift-up solution,
including a spatially mean-zero version, rules out any full-row strict
contraction theorem depending only on the scalar coupling
\(\varepsilon_j\).  A scale-sharp estimate for the complete
Orr--Sommerfeld--Squire row remains open.

**Keywords:** time-dependent shear, Fourier--Leray decomposition,
Orr--Sommerfeld equation, Squire equation, Bloch residue, enhanced
dissipation, negative Sobolev forcing, lift-up

---

## 0. Exact decision and claim boundary

The exact background is

\[
 U^b(t,y)=(0,0,V(t,y)),\qquad V_t=\nu V_{yy},
 \tag{0.1}
\]

with the collision path

\[
 V(t,y)=A_bW(d,x),\qquad A_b=2\delta a,
 \tag{0.2}
\]

\[
 d=\nu R^2(t-t_*),\qquad x=Ry-\phi_*,
 \tag{0.3}
\]

\[
 W(d,x)=\frac12e^{-d}
 \left[-\sin x+\frac12e^{-3d}\sin2x\right],
 \qquad W_d=W_{xx}.
 \tag{0.4}
\]

The main positive conclusions are:

\[
\boxed{
\begin{aligned}
\texttt{exactThreeDimensionalLinearization}&=\texttt{CLOSED},\\
\texttt{exactPressurePoissonFactorTwo}&=\texttt{CLOSED},\\
\texttt{exactBlochLerayNormalization}&=\texttt{CLOSED},\\
\texttt{exactFourierRowDirectSum}&=\texttt{CLOSED},\\
\texttt{exactOSSquireTriangularization}&=\texttt{CLOSED},\\
\texttt{exactVelocityReconstruction}&=\texttt{CLOSED},\\
\texttt{fullRowEnergyIdentity}&=\texttt{CLOSED},\\
\texttt{dampingDominatedFullRows}&=\texttt{CLOSED},\\
\texttt{muZeroRowsSeparated}&=\texttt{CLOSED},\\
\texttt{exactZeroCouplingLiftUpFormula}&=\texttt{CLOSED},\\
\texttt{meanZeroLiftUpCounterexample}&=\texttt{CLOSED},\\
\texttt{scalarA2InvariantEmbedding}&=\texttt{CLOSED},\\
\texttt{strongRowL2ForcingDuhamelAlpha2}&=\texttt{CLOSED},\\
\texttt{strongRowStandardHMinusOneTransferAlpha}&=\texttt{CLOSED},\\
\texttt{strongRowSemiclassicalHMinusOneTransferAlpha2}&=\texttt{CLOSED},\\
\texttt{strongRowForcedEndpointStandardScaleOne}&=\texttt{CLOSED},\\
\texttt{strongForcedDirectSumNoCountLoss}&=\texttt{CLOSED},\\
\texttt{weakZeroFiniteHistoryEnergyLedger}&=\texttt{CLOSED}.
\end{aligned}}
\tag{0.5}
\]

The following proposed extensions are false:

\[
\boxed{
\begin{aligned}
\texttt{scalarA2EqualsCompleteRow}&=\texttt{FALSE},\\
\texttt{epsilonOnlyFullRowClosure}&=\texttt{FALSE},\\
\texttt{allPhysicalRowsUniformStrictContraction}&=\texttt{FALSE},\\
\texttt{standardHMinusOneTransferAlpha2}&=\texttt{FALSE},\\
\texttt{HMinusOneEndpointAlphaGain}&=\texttt{FALSE},\\
\texttt{allRowsStrongScaleForcedGain}&=\texttt{FALSE}.
\end{aligned}}
\tag{0.6}
\]

The remaining system-level statements are open:

\[
\boxed{
\begin{aligned}
\texttt{strongFullRowA2Estimate}&=\texttt{OPEN},\\
\texttt{scaleSharpOSPressureAbsorption}&=\texttt{OPEN},\\
\texttt{orientationUniformSquireTransfer}&=\texttt{OPEN},\\
\texttt{lowGapWeakFullRows}&=\texttt{OPEN},\\
\texttt{completeLinearizedShearSubsystem}&=\texttt{OPEN},\\
\texttt{nonlinearNavierStokes}&=\texttt{OPEN},\\
\texttt{Clay}&=\texttt{OPEN}.
\end{aligned}}
\tag{0.7}
\]

The generic phrase “forced \(H^{-1}\) transfer” is therefore too coarse.
The spatial norm and target topology must be stated.  This section closes
three different scalar estimates and explicitly does not close the complete
vector row.

---

## 1. Provenance and scope

The supplied thesis derives the standard constant-density incompressible
linearized perturbation equations in Chapter 3, equations (3.9a)--(3.9b),
then introduces normal modes in (3.10) and a steady unidirectional base flow
in (3.11).  After a rotation of coordinate labels, that is the conventional
starting point for Section 2 below.

The thesis does not contain the time-dependent heat identity (0.1), the
two-harmonic collision path (0.4), the commensurate \(R\)-cell, Bloch
residues, the all-start \(A_2\) theorem, or the complete row theorem below.
Those statements are derived here from Navier--Stokes and the already frozen
R0.72T--X scalar analysis.  The thesis is therefore background provenance,
not evidence for the new claims.

The exact nonlinear triangular class used earlier is

\[
 u=(f(y,z,t),0,v(y,t)),\qquad
 v_t=\nu v_{yy},\qquad
 f_t+vf_z=\nu(f_{yy}+f_{zz}).
 \tag{1.1}
\]

That invariant class is narrower than the complete perturbation system.
R0.72X proved an all-start scalar propagator bound for the exact collision
path.  The first task here is to identify exactly where that scalar operator
sits inside the full linearization.

---

## 2. Physical linearization and the pressure factor

Let \(u=(u_1,u_2,u_3)\) be a perturbation and put \(v=u_2\).  Direct
linearization of incompressible Navier--Stokes about (0.1) gives

\[
\boxed{
 \partial_tu+V\partial_{x_3}u+vV_y e_3+\nabla p
 =\nu\Delta u,\qquad \nabla\cdot u=0.}
\tag{2.1}
\]

At horizontal Fourier frequency \((K_x,K_z)\), define

\[
 \Delta_K=\partial_y^2-K_x^2-K_z^2,\qquad
 \mathscr D=\partial_t+iK_zV-\nu\Delta_K.
 \tag{2.2}
\]

The component equations are

\[
 \mathscr D u_1=-iK_xp,\qquad
 \mathscr D v=-p_y,\qquad
 \mathscr D u_3+V_yv=-iK_zp,
 \tag{2.3}
\]

\[
 iK_xu_1+v_y+iK_zu_3=0.
 \tag{2.4}
\]

The pressure factor is best checked before rescaling.  In fact,

\[
 \nabla\cdot(V\partial_{x_3}u)
 =V_y\partial_{x_3}v=iK_zV_yv,
 \tag{2.5}
\]

and

\[
 \nabla\cdot(vV_ye_3)
 =\partial_{x_3}(vV_y)=iK_zV_yv.
 \tag{2.6}
\]

Taking the divergence of (2.1) gives

\[
\boxed{\Delta_Kp=-2iK_zV_yv.}
\tag{2.7}
\]

The factor two is structural: one copy comes from differentiating the
background transport, and one comes from the explicit shear-gradient term.

---

## 3. Bloch normalization, Leray projection, and the exact row sum

The shear harmonics in \(W\) shift a physical shear frequency only by
\(\pm R\) and \(\pm2R\).  Write

\[
 m=r+nR,\qquad n\in\mathbb Z,\qquad [r]_R\in\mathbb Z/R\mathbb Z,
 \tag{3.1}
\]

and choose a representative

\[
 \beta=\frac rR.
 \tag{3.2}
\]

The complete invariant row label is

\[
 \boxed{j=(K_x,K_z,[r]_R).}
 \tag{3.3}
\]

Set

\[
 \xi=\frac{K_x}{R},\qquad
 \gamma=\frac{K_z}{R},\qquad
 \mu=\xi^2+\gamma^2,
 \tag{3.4}
\]

\[
 \Lambda=\frac{A_b}{\nu R},\qquad
 c=\gamma\Lambda=\frac{K_zA_b}{\nu R^2},\qquad
 \varepsilon_j=|c|.
 \tag{3.5}
\]

For the convention \(A_b=2\delta a\) and \(\nu=1\), this recovers

\[
 \varepsilon_j=\frac{2|\delta K_z|a}{R^2}.
 \tag{3.6}
\]

The difference between \(c\) and \(\Lambda\) is essential.  Scalar mixing
is weighted by \(K_z\); lift-up is not.

On the \(2\pi\)-cell define

\[
 A_\beta=\partial_x+i\beta,\qquad
 \mathcal L=-A_\beta^2+\mu,
 \tag{3.7}
\]

\[
 \nabla_j=(i\xi,A_\beta,i\gamma),\qquad
 \operatorname{div}_j=i\xi u_1+A_\beta u_2+i\gamma u_3.
 \tag{3.8}
\]

Then

\[
 \operatorname{div}_j\nabla_j=-\mathcal L.
 \tag{3.9}
\]

After division by \(\nu R^2\), with \(\pi=p/(\nu R)\), the exact row is

\[
\boxed{
 u_d+icWu+\Lambda W_xve_3+\nabla_j\pi
 =-\mathcal Lu,\qquad \operatorname{div}_ju=0.}
\tag{3.10}
\]

Taking the row divergence and using

\[
 \operatorname{div}_j(icWu)=icW_xv,\qquad
 \operatorname{div}_j(\Lambda W_xve_3)=icW_xv,
 \tag{3.11}
\]

gives

\[
\boxed{\mathcal L\pi=2icW_xv.}
\tag{3.12}
\]

Whenever

\[
 g_j=\mu+\operatorname{dist}(\beta,\mathbb Z)^2>0,
 \tag{3.13}
\]

\(\mathcal L\) is invertible and the row Leray projection is

\[
\boxed{
 \mathbb P_j=I+\nabla_j\mathcal L^{-1}\operatorname{div}_j.}
\tag{3.14}
\]

The plus sign follows from

\[
 \operatorname{div}_j\mathbb P_j=0,\qquad
 \mathbb P_j\nabla_j=0.
 \tag{3.15}
\]

Thus

\[
\boxed{
 u_d=-\mathcal Lu
 -\mathbb P_j\!\left(icWu+\Lambda W_xve_3\right).}
\tag{3.16}
\]

Multiplication by \(W\) preserves the residue class, while the Fourier
Leray multiplier is diagonal at the complete physical frequency.  Hence

\[
\boxed{
 L^2_\sigma(\mathbb T^3)
 =\bigoplus_{K_x,K_z}\ \bigoplus_{[r]_R}
 \mathcal H_{K_x,K_z,r}.}
\tag{3.17}
\]

Parseval introduces no row-count factor once a uniform row bound is known.
Orthogonality does not itself produce that bound.

---

## 4. Orr--Sommerfeld--Squire reduction

Assume \(\mu>0\) and put

\[
 q=\mathcal Lv,\qquad
 \eta=i\gamma u_1-i\xi u_3.
 \tag{4.1}
\]

The second component of (3.10) is

\[
 v_d=-\mathcal Lv-icWv-A_\beta\pi.
 \tag{4.2}
\]

The product identities

\[
 \mathcal L(Wv)
 =Wq-W_{xx}v-2W_xA_\beta v,
 \tag{4.3}
\]

\[
 \mathcal LA_\beta\pi
 =2ic\left(W_{xx}v+W_xA_\beta v\right)
 \tag{4.4}
\]

cancel the first-derivative commutators and give

\[
\boxed{
 q_d=(-\mathcal L-icW)q
 -icW_{xx}\mathcal L^{-1}q.}
\tag{4.5}
\]

The nonlocal term has a minus sign.  It is the pressure feedback absent
from the scalar R0.72X generator.

The first and third components give, after the pressure terms cancel,

\[
\boxed{
 \eta_d=(-\mathcal L-icW)\eta
 +i\xi\Lambda W_x\mathcal L^{-1}q.}
\tag{4.6}
\]

The system is triangular in the direction \(q\to\eta\).  Its two unresolved
scale issues are visible in (4.5)--(4.6):

1. the Orr--Sommerfeld feedback
   \(-icW_{xx}\mathcal L^{-1}q\) must be absorbed at the collision scale;
2. the Squire coefficient is \(\xi\Lambda\), while the scalar coupling is
   \(c=\gamma\Lambda\).  A lower bound on \(|c|\) does not control nearly
   transverse rows with \(|\xi/\gamma|\gg1\).

These equations are exact.  No full-row enhanced-dissipation conclusion is
drawn from their triangular form.

---

## 5. Velocity recovery and kinetic energy

The divergence constraint and the definition of \(\eta\) give

\[
 \xi u_1+\gamma u_3=iA_\beta v,\qquad
 \gamma u_1-\xi u_3=-i\eta.
 \tag{5.1}
\]

The coefficient matrix squares to \(\mu I\).  Therefore

\[
\boxed{
 u_1=\frac{i}{\mu}
 \left(\xi A_\beta v-\gamma\eta\right),\qquad
 u_3=\frac{i}{\mu}
 \left(\gamma A_\beta v+\xi\eta\right).}
\tag{5.2}
\]

The two coefficient rows are orthogonal, so

\[
\boxed{
 \|u\|_2^2
 =\|v\|_2^2
 +\frac1\mu
 \left(\|A_\beta v\|_2^2+\|\eta\|_2^2\right).}
\tag{5.3}
\]

Equivalently,

\[
 \|u\|_2^2
 =\frac1\mu
 \left(\|\mathcal L^{-1/2}q\|_2^2+\|\eta\|_2^2\right).
 \tag{5.4}
\]

These formulas are invalid at \(\mu=0\).  The degenerate rows are treated
directly in Section 8.

---

## 6. The exact scalar \(A_2\) embedding

For \(\mu>0\), impose

\[
 v=0,\qquad
 u=g\,\frac{(\gamma,0,-\xi)}{\sqrt\mu}.
 \tag{6.1}
\]

This polarization is divergence free.  The pressure source and lift term
vanish, and (3.10) becomes

\[
\boxed{
 g_d=\left[A_\beta^2-\mu\right]g-icWg.}
\tag{6.2}
\]

This is exactly the scalar Bloch row controlled in R0.72X.  Hence the exact
\(A_2\) estimate embeds into the full three-dimensional linearization
without approximation.

The embedding is proper.  General data have nonzero \(v\), activate the
pressure feedback (4.5), and then force \(\eta\) through (4.6).  Therefore

\[
 \texttt{scalarA2InvariantEmbedding}=\texttt{CLOSED},
 \qquad
 \texttt{scalarA2EqualsCompleteRow}=\texttt{FALSE}.
 \tag{6.3}
\]

---

## 7. Full-row energy and a closed damping-dominated class

Taking the real \(L^2\) inner product of (3.10) with \(u\) gives

\[
\boxed{
 \frac12\frac d{dd}\|u\|_2^2
 +\|A_\beta u\|_2^2+\mu\|u\|_2^2
 =-\Lambda\operatorname{Re}\langle W_xv,u_3\rangle.}
\tag{7.1}
\]

The scalar potential is skew and pressure is orthogonal to
divergence-free data.  The right side is the shear-production term and has
no fixed sign.

On a compact time interval \(K\), put

\[
 M_K=\sup_{d\in K}\|W_x(d)\|_\infty.
 \tag{7.2}
\]

Poincare and \(2ab\le a^2+b^2\) give

\[
 \frac12\frac d{dd}\|u\|_2^2
 +\left(g_j-\frac{|\Lambda|M_K}{2}\right)\|u\|_2^2
 \le0.
 \tag{7.3}
\]

Every row satisfying

\[
\boxed{g_j>\frac{|\Lambda|M_K}{2}}
\tag{7.4}
\]

therefore obeys

\[
\boxed{
 \|u(d_2)\|_2
 \le e^{-[g_j-|\Lambda|M_K/2](d_2-d_1)}
 \|u(d_1)\|_2.}
\tag{7.5}
\]

This closes the high-gap, damping-dominated full rows.  It is an ordinary
energy estimate, not a collision-scale enhanced-dissipation theorem for the
remaining low-gap rows.

---

## 8. Exceptional rows and the exact lift-up obstruction

When \(\mu=0\), one has

\[
 K_x=K_z=0,\qquad \xi=\gamma=c=0.
 \tag{8.1}
\]

If \(\operatorname{dist}(\beta,\mathbb Z)>0\), divergence gives
\(A_\beta v=0\), hence \(v=0\), and the tangential components solve
covariant heat equations.  If \(\beta=0\), a cell-constant \(v\) is allowed
and the third component still contains lift-up.  This row must be handled
in component variables; inserting a pseudoinverse into (4.5)--(5.4) would
be invalid.

The stronger obstruction also occurs at \(\mu>0\).  Take

\[
 \gamma=0,\qquad \beta=0,\qquad \xi\ge0,
 \tag{8.2}
\]

so

\[
 c=\varepsilon_j=0,\qquad \mu=\xi^2.
 \tag{8.3}
\]

At time \(d_1\), choose

\[
 u_1(d_1)=u_3(d_1)=0,\qquad v(d_1)=v_0,
 \tag{8.4}
\]

where \(v_0\) is constant in the cell.  With
\(\tau=d_2-d_1>0\),

\[
 v(d_2)=e^{-\xi^2\tau}v_0.
 \tag{8.5}
\]

Because

\[
 (W_x)_d=(W_x)_{xx},
 \tag{8.6}
\]

Duhamel's formula is exact:

\[
\boxed{
 u_3(d_2,x)
 =-\Lambda\tau e^{-\xi^2\tau}W_x(d_2,x)v_0.}
\tag{8.7}
\]

Direct differentiation verifies the residual:

\[
 \partial_du_3-(\partial_x^2-\xi^2)u_3+\Lambda W_xv
 =-\Lambda\tau e^{-\xi^2\tau}
 \left[(W_x)_d-(W_x)_{xx}\right]v_0=0.
 \tag{8.8}
\]

For the exact path,

\[
 W_x(d,x)=\frac12e^{-d}
 \left[-\cos x+e^{-3d}\cos2x\right],
 \tag{8.9}
\]

and Fourier orthogonality gives

\[
\boxed{
 \frac1{2\pi}\int_0^{2\pi}|W_x(d,x)|^2\,dx
 =\frac18\left(e^{-2d}+e^{-8d}\right).}
\tag{8.10}
\]

Thus

\[
\boxed{
 \frac{\|u(d_2)\|_2^2}{\|u(d_1)\|_2^2}
 =e^{-2\xi^2\tau}
 \left[
 1+\frac{\Lambda^2\tau^2}{8}
 \left(e^{-2d_2}+e^{-8d_2}\right)
 \right].}
\tag{8.11}
\]

For \(\xi=0\), every \(\Lambda\ne0\) and \(\tau>0\) gives strict growth.
For \(\xi>0\), the physical perturbation carries the horizontal factor
\(e^{iK_xx_1}\) and is spatially mean zero.  For fixed \(d_1<d_2\), (8.11)
still exceeds one when \(|\Lambda|\) is sufficiently large.

Deleting only the global constant velocity mode therefore does not restore
a background-uniform contraction theorem.  The example does not refute a
full-row bound with an explicit transient prefactor, an orientation payment,
or a larger projection.

---

## 9. Strong scalar forcing: the exact causal kernel

Consider a strong scalar invariant row on \(K=[d_-,d_+]\):

\[
 G_d=(A_\beta^2-\mu)G-i\sigma\varepsilon WG+F,
 \qquad \varepsilon\ge4,
 \tag{9.1}
\]

where \(\sigma\in\{-1,1\}\) and

\[
 \alpha=(\varepsilon/4)^{-1/5}\in(0,1].
 \tag{9.2}
\]

R0.72X gives one \(q=q_{K,T}\in(0,1)\) such that

\[
 \|U_\alpha(d,s)\|_{2\to2}
 \le e^{-\mu(d-s)}
 q^{\lfloor(d-s)/(2T\alpha^2)\rfloor}.
 \tag{9.3}
\]

Put

\[
 h=2T\alpha^2,\qquad
 k_\mu(r)=\mathbf1_{r\ge0}e^{-\mu r}q^{\lfloor r/h\rfloor}.
 \tag{9.4}
\]

For every \(p\in[1,\infty)\) and \(\mu>0\),

\[
\boxed{
 \|k_\mu\|_{L^p(0,\infty)}^p
 =\frac{1-e^{-p\mu h}}
 {p\mu(1-q^pe^{-p\mu h})}.}
\tag{9.5}
\]

At \(\mu=0\), the limit is

\[
 \|k_0\|_{L^p}^p=\frac h{1-q^p}.
 \tag{9.6}
\]

Define

\[
 A_q=\frac{2T}{1-q},\qquad
 B_q=\frac{2T}{1-q^2}.
 \tag{9.7}
\]

For

\[
 (\mathcal DF)(d)=\int_{d_-}^{d}U_\alpha(d,s)F(s)\,ds,
 \tag{9.8}
\]

Young's inequality and (9.5) give

\[
 \|\mathcal DF\|_{L_d^2L_x^2}
 \le\sqrt{B_q}\,\alpha\|F\|_{L_d^1L_x^2},
 \tag{9.9}
\]

\[
 \|\mathcal DF\|_{L_d^\infty L_x^2}
 \le\|F\|_{L_d^1L_x^2},
 \tag{9.10}
\]

\[
\boxed{
 \|\mathcal DF\|_{L_d^2L_x^2}
 \le A_q\alpha^2\|F\|_{L_d^2L_x^2},}
\tag{9.11}
\]

\[
 \|\mathcal DF\|_{L_d^\infty L_x^2}
 \le\sqrt{B_q}\,\alpha\|F\|_{L_d^2L_x^2}.
 \tag{9.12}
\]

The \(O(\alpha^2)\) coefficient belongs to the spacetime
\(L_d^2L_x^2\to L_d^2L_x^2\) map.  It is not an endpoint estimate and does
not automatically survive replacement of the spatial input norm by
standard \(H^{-1}\).

---

## 10. Standard and semiclassical negative norms

Define

\[
 \|F\|_{H^{-1}_\beta}^2
 =\sum_{n\in\mathbb Z}
 \frac{|F_n|^2}{1+(n+\beta)^2},
 \tag{10.1}
\]

\[
 \|F\|_{\mathcal H^{-1}_{\alpha,\beta}}^2
 =\sum_{n\in\mathbb Z}
 \frac{|F_n|^2}{1+\alpha^2(n+\beta)^2}.
 \tag{10.2}
\]

Let \(g\in L^2(K;L_x^2)\) and define the backward adjoint response

\[
 z(s)=\int_s^{d_+}U_\alpha(d,s)^*g(d)\,dd.
 \tag{10.3}
\]

The same causal kernel and the backward energy identity give

\[
 \|z\|_{L_d^2L_x^2}
 \le A_q\alpha^2\|g\|_{L_d^2L_x^2},
 \tag{10.4}
\]

\[
 \|A_\beta z\|_{L_d^2L_x^2}
 \le\sqrt{A_q}\,\alpha\|g\|_{L_d^2L_x^2}.
 \tag{10.5}
\]

With

\[
 C_q=\sqrt{A_q^2+A_q},
 \tag{10.6}
\]

one has

\[
 \|z\|_{L_d^2H^1_\beta}
 \le C_q\alpha\|g\|_{L_d^2L_x^2},
 \tag{10.7}
\]

\[
 \|z\|_{L_d^2\mathcal H^1_{\alpha,\beta}}
 \le C_q\alpha^2\|g\|_{L_d^2L_x^2}.
 \tag{10.8}
\]

For the zero-initial forward variational solution, the transposition
identity

\[
 \int_K(G,g)\,dd=\int_K\langle F,z\rangle\,dd
 \tag{10.9}
\]

therefore proves

\[
\boxed{
 \|G\|_{L_d^2L_x^2}
 \le C_q\alpha
 \|F\|_{L_d^2H^{-1}_\beta},}
\tag{10.10}
\]

\[
\boxed{
 \|G\|_{L_d^2L_x^2}
 \le C_q\alpha^2
 \|F\|_{L_d^2\mathcal H^{-1}_{\alpha,\beta}}.}
\tag{10.11}
\]

For nonzero initial data, linear superposition and the homogeneous kernel
give

\[
 \|G\|_{L_d^2L_x^2}
 \le\sqrt{B_q}\,\alpha\|G(d_-)\|_2
 + C_q\alpha\|F\|_{L_d^2H^{-1}_\beta},
 \tag{10.12}
\]

or the same homogeneous term plus
\(C_q\alpha^2\|F\|_{L_d^2\mathcal H^{-1}_{\alpha,\beta}}\).

No pointwise extension \(U(d,s):H^{-1}\to L^2\) is assumed.  The retarded
operator is first defined for smooth \(L^2\)-valued forcing and extended by
(10.10)--(10.11).

For completeness, multiplication by the real smooth potential is a bounded
skew perturbation for each fixed row.  Galerkin or Lions variational theory
gives

\[
 G\in L^2(K;H^1_\beta),\qquad
 \partial_dG\in L^2(K;H^{-1}_\beta),\qquad
 G\in C(K;L_x^2).
 \tag{10.13}
\]

The last inclusion is the Hilbert-triple trace theorem.  It is not inferred
from graph membership alone.  Galerkin limits or Steklov averaging justify
the energy and transposition identities.

---

## 11. Endpoint bounds and their sharp boundary

Apply (10.10) on every prefix of \(K\).  Put

\[
 r_q=\frac{1+\sqrt{1+4C_q}}2,
 \tag{11.1}
\]

\[
 C_q'=\max\left\{
 r_q,\sqrt{2(C_q+r_q)}
 \right\}.
 \tag{11.2}
\]

The forced energy identity gives

\[
\boxed{
 \max\left\{
 \|A_\beta G\|_{L_d^2L_x^2},
 \|G\|_{L_d^\infty L_x^2}
 \right\}
 \le C_q'\|F\|_{L_d^2H^{-1}_\beta}.}
\tag{11.3}
\]

The semiclassical version is

\[
\boxed{
 \max\left\{
 \|A_\beta G\|_{L_d^2L_x^2},
 \|G\|_{L_d^\infty L_x^2}
 \right\}
 \le C_q'\alpha
 \|F\|_{L_d^2\mathcal H^{-1}_{\alpha,\beta}}.}
\tag{11.4}
\]

The use of a maximum in (11.3)--(11.4) is deliberate.  The same constant
would not control the sum of the two norms.

There is no missing standard endpoint power.  At terminal time \(d_+\),
take

\[
 F_N(d,x)=N^2
 \mathbf1_{[d_+-N^{-2},d_+]}(d)
 (2\pi)^{-1/2}e^{iNx}.
 \tag{11.5}
\]

Then

\[
 \|F_N\|_{L_d^2H_x^{-1}}
 =\frac N{\sqrt{1+N^2}}\longrightarrow1.
 \tag{11.6}
\]

The heat response at \(d_+\) is exactly
\((1-e^{-1})e_N\).  If
\(M_\alpha=\varepsilon\sup_K\|W\|_\infty\), Duhamel comparison bounds the
potential error by \(M_\alpha/(2N^2)\).  Choosing
\(N^2\gg M_\alpha+\mu\) leaves a positive endpoint lower bound independent
of \(\alpha\).  Thus

\[
 \texttt{HMinusOneEndpointAlphaGain}=\texttt{FALSE}.
 \tag{11.7}
\]

---

## 12. Sharpness of the two spacetime powers

The distinction between standard and semiclassical \(H^{-1}\) is realized
inside the exact collision chart.  Choose a nonzero even
\(\eta\in C_c^\infty(\mathbb R)\), put
\(\psi=\eta''\), and choose
\(\chi\in C_c^\infty((-T,T))\) that vanishes near the initial endpoint.
On the expanding torus define

\[
 w_\alpha(S,X)=\chi(S)\psi(X).
 \tag{12.1}
\]

The exact scaled potential and equation are

\[
 V_\alpha(S,X)=\alpha^{-3}\left[
 2e^{-\alpha^2S}\sin(\alpha X)
 -e^{-4\alpha^2S}\sin(2\alpha X)\right],
 \tag{12.2}
\]

\[
 w_S=w_{XX}-i\sigma V_\alpha w+f.
 \tag{12.3}
\]

Define the forcing exactly by

\[
 f_\alpha
 =\partial_Sw_\alpha-\partial_X^2w_\alpha
 +i\sigma V_\alpha w_\alpha.
 \tag{12.4}
\]

Since the potential is odd in \(X\)
and \(\psi\) is even with zero integral, \(f_\alpha\) is mean zero.  On the
fixed support the exact potential converges smoothly to the cubic collision
chart.  The limiting forcing is nonzero by uniqueness for the zero-initial
parabolic problem.

Return to physical variables:

\[
 G_\alpha(d,x)=w_\alpha(d/\alpha^2,x/\alpha),
 \qquad
 F_\alpha(d,x)=\alpha^{-2}
 f_\alpha(d/\alpha^2,x/\alpha).
 \tag{12.5}
\]

The exact change of variables gives

\[
 \|G_\alpha\|_{L_d^2L_x^2}^2
 =\alpha^3\|w_\alpha\|_{L_S^2L_X^2}^2,
 \tag{12.6}
\]

\[
 \|F_\alpha\|_{L_d^2\mathcal H^{-1}_{\alpha,0}}^2
 =\alpha^{-1}
 \|f_\alpha\|_{L_S^2H^{-1}(\mathbb T_\alpha)}^2.
 \tag{12.7}
\]

Fourier Riemann-sum convergence for the mean-zero localized profile also
gives

\[
 \|F_\alpha\|_{L_d^2H^{-1}}^2
 \sim\alpha
 \|f_0\|_{L_S^2\dot H^{-1}(\mathbb R)}^2.
 \tag{12.8}
\]

Consequently

\[
\boxed{
 \frac{\|G_\alpha\|_{L_d^2L_x^2}}
 {\|F_\alpha\|_{L_d^2H^{-1}}}
 \sim c_{\rm std}\alpha,}
\tag{12.9}
\]

\[
\boxed{
 \frac{\|G_\alpha\|_{L_d^2L_x^2}}
 {\|F_\alpha\|_{L_d^2\mathcal H^{-1}_{\alpha,0}}}
 \sim c_{\rm sc}\alpha^2,}
\tag{12.10}
\]

with positive constants.  The witness is zero-initial and mean zero.
Therefore the standard power cannot be improved from \(\alpha\) to
\(\alpha^2\) by imposing only a mean-zero condition.

The limiting Riemann-sum argument is analytic.  A finite certificate may
check sample scalings but cannot certify (12.8) as a limiting theorem.

---

## 13. Strong-row direct sum

For decoupled invariant scalar rows, let

\[
 \varepsilon_j\ge4,\qquad
 \alpha_j=(\varepsilon_j/4)^{-1/5}.
 \tag{13.1}
\]

Squaring (10.10) and summing by Parseval gives

\[
\boxed{
 \sum_j\|G_j\|_{L_d^2L_x^2}^2
 \le C_q^2\sum_j\alpha_j^2
 \|F_j\|_{L_d^2H^{-1}_{\beta_j}}^2.}
\tag{13.2}
\]

Likewise,

\[
\boxed{
 \sum_j\|G_j\|_{L_d^2L_x^2}^2
 \le C_q^2\sum_j\alpha_j^4
 \|F_j\|_{L_d^2\mathcal H^{-1}_{\alpha_j,\beta_j}}^2.}
\tag{13.3}
\]

There is no row-count factor.  Infinite sums follow by finite truncation and
monotone convergence in the energy topology.

This conclusion is restricted to the decoupled scalar invariant rows.  If a
coupled system has \(F=\mathcal BG+H\), standard-norm absorption would
require an actual estimate such as

\[
 C_q
 \left\|\operatorname{diag}(\alpha_j)\mathcal B\right\|<1.
 \tag{13.4}
\]

Neither (13.4) nor an equivalent triangular iteration follows from scalar
orthogonality.

---

## 14. Weak and zero scalar rows

For \(0\le\varepsilon<4\), the strong \(A_2\) theorem is not invoked.
Skewness still yields a finite-history energy ledger.  For a zero-initial
solution on an interval of length \(L\),

\[
 \sup_{d\in K}\|G(d)\|_2^2
 \le e^L\|F\|_{L_d^2H^{-1}_\beta}^2,
 \tag{14.1}
\]

\[
 \|G\|_{L_d^2L_x^2}
 \le\sqrt{Le^L}\|F\|_{L_d^2H^{-1}_\beta},
 \tag{14.2}
\]

\[
 \|A_\beta G\|_{L_d^2L_x^2}^2
 \le(1+Le^L)\|F\|_{L_d^2H^{-1}_\beta}^2.
 \tag{14.3}
\]

These bounds contain no enhanced-dissipation power.

Let

\[
 \rho=\operatorname{dist}(\beta,\mathbb Z),\qquad
 \gamma_{\rho,\mu}
 =\min\left\{1,\frac{\rho^2+\mu}{1+\rho^2}\right\}.
 \tag{14.4}
\]

If \(\rho^2+\mu>0\), Poincare and the energy identity give the
time-global estimate

\[
 \|G\|_{L_d^2H^1_\beta}
 \le\gamma_{\rho,\mu}^{-1}
 \|F\|_{L_d^2H^{-1}_\beta}.
 \tag{14.5}
\]

At \(\varepsilon=\beta=\mu=0\), the spatial constant satisfies
\(a'=f\).  On \([0,L]\), taking \(f=L^{-1/2}\) gives unit input norm and

\[
 \|a\|_{L^2(0,L)}=\frac L{\sqrt3}.
 \tag{14.6}
\]

No time-uniform estimate is possible for that undamped row.

At \(\beta=0\), mean zero is not invariant under multiplication by
\(W\) unless the operator explicitly projects out the mean.  A mean-zero
Poincare estimate cannot be inserted silently into the weak-row system.

---

## 15. Complete class ledger

| Row class | Exact conclusion | Status |
|---|---|---|
| \(\varepsilon_j\ge4\), scalar polarization (6.1) | R0.72X homogeneous \(A_2\) and Sections 9--13 forced estimates | **CLOSED** |
| \(\varepsilon_j\ge4\), complete row | Pressure feedback (4.5) and Squire forcing (4.6) remain | **OPEN** |
| \(0<\varepsilon_j<4\), scalar row | Bare energy plus finite-history forcing | **CLOSED without strong gain** |
| Any complete row satisfying (7.4) | Full velocity decays by (7.5) | **CLOSED** |
| Low-gap weak complete row | No scale-sharp bound here | **OPEN** |
| \(\varepsilon_j=0\), scalar tangential row | Covariant heat; gapless constants do not decay | **CLOSED / nondecay** |
| \(\varepsilon_j=0\), complete row | Exact lift-up (8.7)--(8.11) may grow | **FALSE for uniform strict contraction** |
| \(\mu=0,\beta\ne0\) | Divergence forces \(v=0\); Bloch heat damping | **CLOSED** |
| \(\mu=0,\beta=0\) | OS--Squire inverse coordinates degenerate; component lift-up remains | **CLOSED structural split** |

The coupling label \(\varepsilon_j=0\) does not mean that all background
coupling vanishes: \(c=\gamma\Lambda\) can be zero while
\(\xi\Lambda\) remains nonzero.

---

## 16. Primary-literature boundary

The literature check was bounded and source-based.  It does not establish a
novelty or priority claim.

1. Daniel Coble and Siming He,
   [*A Note on Enhanced Dissipation and Taylor Dispersion of Time-dependent
   Shear Flows*](https://arxiv.org/html/2309.15738), prove homogeneous
   nonautonomous scalar decay under a fixed finite set of uniformly
   nondegenerate critical points.  Their theorem does not pass through a
   critical-point collision and contains no forcing, Bloch fiber, pressure,
   or lift-up.
2. Michele Coti Zelati, Matias Delgadino, and Tarek Elgindi,
   [*On the relation between enhanced dissipation time-scales and mixing
   rates*](https://arxiv.org/html/1806.03258), show why a nonautonomous
   argument needs estimates uniform in every starting time.  Their
   \(H^{-1}\) quantity is a mixing output, not the forcing space used here.
3. Dongyi Wei and Zhifei Zhang,
   [*Transition threshold for the 3D Couette flow in Sobolev
   space*](https://arxiv.org/html/1803.01359v1), already treat structured
   forcing, lift-up, linear pressure, and vector coupling near Couette flow.
   Their change of variables uses \(Y=V(t,y,z)\) and division by
   \(\partial_yV\).  It ceases to be a diffeomorphism at the collision
   \(\partial_yV=0\).
4. Michele Coti Zelati, Tarek Elgindi, and Klaus Widmayer,
   [*Enhanced dissipation in the Navier--Stokes equations near the Poiseuille
   flow*](https://arxiv.org/html/1901.01571), control an active nonlocal
   linearized term and sum uniform integer Fourier rows.  That autonomous
   two-dimensional result does not supply Bloch-uniform collision estimates.
5. Jacob Bedrossian and Michele Coti Zelati,
   [*Enhanced dissipation, hypoellipticity, and anomalous small noise
   inviscid limits in shear flows*](https://arxiv.org/html/1510.08098),
   provide fixed finite-type shear benchmarks.  Their \(H^{-1}\) mixing
   output and stochastic forcing must not be conflated with deterministic
   \(L_d^2H^{-1}\) input here.
6. Johannes Benthaus, Giuseppe Coclite, and Camilla Nobili,
   [*Mixing and enhanced dissipation in a time-translating shear
   flow*](https://arxiv.org/html/2603.14624), study moving but still simple,
   separated critical points.  Translation is not collision or change of
   critical-point count.

The safe boundary is narrow: the checked literature contains
nonautonomous forcing and vector Couette results, but I did not find in this
bounded search a single theorem combining collision, Bloch-uniform fibers,
structured negative-Sobolev forcing, weak/zero rows, and the complete
linearized vector direct sum.  “Not found in this search” is not “proved
globally new.”

---

## 17. Certificate boundary

Finite deterministic checks cover:

1. \(W_d=W_{xx}\) and the exact \(W_x\) norm;
2. the two pressure-divergence contributions and factor two;
3. the Bloch--Leray sign identities;
4. the Orr--Sommerfeld and Squire algebraic signs;
5. velocity reconstruction and the kinetic-energy identity;
6. the lift-up residual and amplification formula;
7. the exact causal geometric sum and its zero-damping limit;
8. the standard/semiclassical Fourier-weight comparison;
9. the damping-gap algebra and exact claim-key ledger.

The certificate does not prove:

1. the R0.72X compactness theorem from scratch;
2. nonautonomous Galerkin existence, endpoint traces, or duality passage;
3. the Fourier Riemann-sum limit in the sharpness construction;
4. infinite-dimensional operator absorption for (4.5)--(4.6);
5. any nonlinear Navier--Stokes estimate.

The formal figure is also explanatory evidence, not a proof.

---

## 18. Research value and next theorem

This section has two concrete values.

First, it prevents a serious category error.  The exact scalar collision
theorem is a genuine invariant block of the full linearization, but it is
not the full Orr--Sommerfeld operator.  The missing pressure and lift-up
terms are now written with their exact signs, scales, and degenerate rows.

Second, the strong scalar block now has a sharp forced-transfer ledger.
Standard \(H^{-1}\) loses one collision-scale power relative to
\(L_x^2\) or semiclassical \(H^{-1}\), and the endpoint loses another.
Those losses constrain any later nonlinear bootstrap.

The direct value for the Clay problem remains low.  No estimate here controls
the full low-gap vector rows, nonlinear convolution between rows, vortex
stretching, a critical continuation norm, or global smoothness.

The next minimal theorem is R0.72Z:

\[
 \boxed{\text{control the Orr--Sommerfeld pressure feedback and split the
 Squire transfer by orientation and damping.}}
 \tag{18.1}
\]

It should first seek a weighted full-row propagator with an explicit
transient prefactor, not an impossible uniform strict contraction.  Only
after that linear estimate closes should nonlinear row convolution be
introduced.
