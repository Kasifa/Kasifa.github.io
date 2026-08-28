# R0.72Y independent audit: complete Fourier--Leray rows and the lift-up boundary

**Date:** 2026-08-28

**Audit scope:** independent algebraic and analytic audit of the complete
three-dimensional linearization about the exact heat-shear background used in
R0.72T--X.  The audit checks the pressure Poisson factor, carrier-cell and
Bloch normalization, row Leray projection, Orr--Sommerfeld--Squire reduction,
velocity reconstruction, kinetic-energy identity, and the exact
zero-coupling lift-up solution.  It does not audit or assert a complete
full-row enhanced-dissipation theorem.

**Outcome:** the full Fourier-row equations and the scalar invariant embedding
are correct under the explicit normalization below.  A zero-coupling row has
an exact lift-up solution, including a mean-zero version, which rules out a
uniform strict contraction based only on the scalar coupling
\(\varepsilon_j\).  Strong full-row enhanced dissipation, scale-sharp pressure
absorption, and orientation-uniform Squire transfer remain open.

---

## 0. Evidence and model boundary

The exact nonlinear triangular class is

\[
 u=(f(y,z,t),0,v(y,t)),\qquad
 v_t=\nu v_{yy},\qquad
 f_t+vf_z=\nu(f_{yy}+f_{zz}).
 \tag{0.1}
\]

It is recorded in `research/r071w_report-source.md`, lines 160--193.  The
projected-Lamb identity for that class is recorded there at lines 195--216.
The commensurate affine row and its exact cell reduction are recorded in
`research/r072p_report-source.md`, lines 136--220, and in
`research/r072q_report-source.md`, lines 102--176.

R0.72X records only the scalar residue-row equation, Bloch gauge, scalar
damping, and strong scalar-row direct sum in
`research/r072x_report-source.md`, lines 554--657.  Its gap matrix explicitly
leaves negative-Sobolev forcing and the complete linearized shear subsystem
open at `research/r072x_gap_matrix.md`, lines 24--35.  The literature audit
also states that the scalar estimate contains no lift-up or pressure structure
at `research/r072x_literature_audit.md`, lines 17--31 and 164--167.

The thesis-derived stability equations supply the standard incompressible
linearization about a parallel shear, but not the heat history, commensurate
lattice, Bloch residues, or the complete three-dimensional row derived below.
Those structures must therefore be derived from Navier--Stokes and the exact
project background, rather than attributed directly to the thesis.

---

## 1. Assumptions and normalization

Work on a three-torus with coordinates \((x_1,y,x_3)\).  The background is

\[
 U^b(t,y)=(0,0,V(t,y)),\qquad V_t=\nu V_{yy},\qquad \nu>0.
 \tag{1.1}
\]

For the collision family, write

\[
 V(t,y)=A_bW(d,x),\qquad A_b=2\delta a,
 \tag{1.2}
\]

\[
 d=\nu R^2(t-t_*),\qquad x=Ry-\phi_*,\qquad R\in\mathbb N,
 \tag{1.3}
\]

where

\[
 W(d,x)=\frac12e^{-d}
 \left[-\sin x+\frac12e^{-3d}\sin2x\right],
 \qquad W_d=W_{xx}.
 \tag{1.4}
\]

The amplitude \(A_b\) is allowed to have either sign.  The physical project
normalization used in R0.72X sets \(\nu=1\); retaining \(\nu\) here makes the
dimensionless factors auditable before that specialization.

Fix horizontal Fourier frequencies \((K_x,K_z)\in\mathbb Z^2\).  Because
\(W\) has only the shear-direction harmonics \(\pm R,\pm2R\), write the
remaining shear frequency as

\[
 m=r+nR,\qquad n\in\mathbb Z,qquad [r]\in\mathbb Z/R\mathbb Z,
 \tag{1.5}
\]

and choose a representative

\[
 \beta=\frac rR.
 \tag{1.6}
\]

The complete row index is

\[
 \boxed{j=(K_x,K_z,[r]_R).}
 \tag{1.7}
\]

Define

\[
 \xi=\frac{K_x}{R},\qquad
 \gamma=\frac{K_z}{R},\qquad
 \mu=\xi^2+\gamma^2,
 \tag{1.8}
\]

\[
 \Lambda=\frac{A_b}{\nu R},\qquad
 c=\gamma\Lambda
 =\frac{2\delta aK_z}{\nu R^2},\qquad
 \varepsilon_j=|c|.
 \tag{1.9}
\]

Thus, after setting \(\nu=1\),

\[
 \varepsilon_j=\frac{2|\delta K_z|a}{R^2},
 \tag{1.10}
\]

exactly as in R0.72X.  The distinction between \(c=\gamma\Lambda\) and
\(\Lambda\) is essential: advection/mixing is weighted by \(K_z\), while
lift-up is not.

On the periodic cell define

\[
 A_\beta=\partial_x+i\beta,
 \qquad
 \mathcal L=-A_\beta^2+\mu,
 \tag{1.11}
\]

\[
 \nabla_j=(i\xi,A_\beta,i\gamma),
 \qquad
 \operatorname{div}_j=i\xi u_1+A_\beta u_2+i\gamma u_3.
 \tag{1.12}
\]

Then

\[
 \operatorname{div}_j\nabla_j=A_\beta^2-\mu=-\mathcal L.
 \tag{1.13}
\]

For \(\mu>0\), \(\mathcal L\) is strictly positive and invertible for every
Bloch residue.  The cases \(\mu=0\) are separated in Section 8.

---

## 2. Independent physical linearization and pressure factor two

Let the perturbation be \(u=(u_1,u_2,u_3)\) and write \(v=u_2\).  Direct
linearization of incompressible Navier--Stokes about (1.1) gives

\[
 \boxed{
 \partial_tu+V\partial_{x_3}u+vV_y e_3+\nabla p
 =\nu\Delta u,
 \qquad \nabla\cdot u=0.}
 \tag{2.1}
\]

On the horizontal Fourier mode \((K_x,K_z)\), put

\[
 \Delta_K=\partial_y^2-K_x^2-K_z^2,
 \qquad
 \mathscr D=\partial_t+iK_zV-\nu\Delta_K.
 \tag{2.2}
\]

The component equations are

\[
 \mathscr D u_1=-iK_xp,
 \qquad
 \mathscr D v=-p_y,
 \qquad
 \mathscr D u_3+V_yv=-iK_zp,
 \tag{2.3}
\]

\[
 iK_xu_1+v_y+iK_zu_3=0.
 \tag{2.4}
\]

The pressure factor is checked before any rescaling.  First,

\[
 \nabla\cdot(V\partial_{x_3}u)
 =V_y\partial_{x_3}v
 =iK_zV_yv,
 \tag{2.5}
\]

because \(\nabla\cdot u=0\).  Second,

\[
 \nabla\cdot(vV_ye_3)
 =\partial_{x_3}(vV_y)
 =iK_zV_yv.
 \tag{2.6}
\]

Taking the divergence of (2.1) therefore gives

\[
 \boxed{\Delta_Kp=-2iK_zV_yv.}
 \tag{2.7}
\]

The factor two is not a convention: the transport term and the shear-gradient
term contribute one copy each.  The sign in (2.7) follows from keeping
\(+\nabla p\) on the left of (2.1).

**Verdict:** `exactThreeDimensionalLinearization=CLOSED` and
`exactPressurePoissonFactorTwo=CLOSED`.

---

## 3. Bloch normalization and row Leray projection

Divide (2.1) by \(\nu R^2\), use (1.2)--(1.9), and set

\[
 \pi=\frac{p}{\nu R}.
 \tag{3.1}
\]

The exact normalized row is

\[
 \boxed{
 u_d+icWu+\Lambda W_xv e_3+\nabla_j\pi=-\mathcal Lu,
 \qquad \operatorname{div}_ju=0.}
 \tag{3.2}
\]

There is no missing power of \(R\):

\[
 \frac{K_zA_b}{\nu R^2}=c,
 \qquad
 \frac{A_bR}{\nu R^2}=\Lambda.
 \tag{3.3}
\]

Taking the row divergence of (3.2) gives

\[
 \operatorname{div}_j(icWu)=icW_xv,
 \tag{3.4}
\]

\[
 \operatorname{div}_j(\Lambda W_xve_3)
 =i\gamma\Lambda W_xv=icW_xv,
 \tag{3.5}
\]

and, by (1.13),

\[
 \operatorname{div}_j\nabla_j\pi=-\mathcal L\pi.
 \tag{3.6}
\]

Hence

\[
 \boxed{\mathcal L\pi=2icW_xv.}
 \tag{3.7}
\]

For \(\mu>0\), define

\[
 \boxed{
 \mathbb P_j=I+\nabla_j\mathcal L^{-1}\operatorname{div}_j.}
 \tag{3.8}
\]

The plus sign in (3.8) is correct.  Indeed,

\[
 \operatorname{div}_j\mathbb P_j
 =\operatorname{div}_j
 -\mathcal L\mathcal L^{-1}\operatorname{div}_j=0,
 \tag{3.9}
\]

and

\[
 \mathbb P_j\nabla_j
 =\nabla_j-\nabla_j\mathcal L^{-1}\mathcal L=0.
 \tag{3.10}
\]

Thus (3.2) is equivalently

\[
 \boxed{
 u_d=-\mathcal Lu
 -\mathbb P_j\!\left(icWu+\Lambda W_xve_3\right).}
 \tag{3.11}
\]

Multiplication by \(W,W_x,W_{xx}\) shifts the shear Fourier label only by
\(\pm R,\pm2R\), while the Fourier Leray multiplier acts diagonally at each
complete frequency.  Therefore every index (1.7) is invariant, and

\[
 L^2_\sigma(\mathbb T^3)
 =\bigoplus_{K_x,K_z}\ \bigoplus_{[r]_R}\mathcal H_{K_x,K_z,r}
 \tag{3.12}
\]

is an exact orthogonal decomposition.  A uniform row estimate sums by
Parseval with no row-count loss.  Orthogonality alone does not supply the
required uniform row constant.

**Verdict:** `exactBlochLerayNormalization=CLOSED` and
`exactRowDirectSum=CLOSED`.  The assertion that row orthogonality by itself
closes a full-system estimate is **FALSE**.

---

## 4. Orr--Sommerfeld equation and sign audit

Assume \(\mu>0\) and put

\[
 q=\mathcal Lv.
 \tag{4.1}
\]

The second component of (3.2) is

\[
 v_d=-\mathcal Lv-icWv-A_\beta\pi.
 \tag{4.2}
\]

Applying \(\mathcal L\) gives

\[
 q_d=-\mathcal Lq-ic\mathcal L(Wv)
 -\mathcal LA_\beta\pi.
 \tag{4.3}
\]

The two required product identities are

\[
 \mathcal L(Wv)
 =Wq-W_{xx}v-2W_xA_\beta v,
 \tag{4.4}
\]

and, using (3.7),

\[
 \mathcal LA_\beta\pi
 =A_\beta\mathcal L\pi
 =2ic\left(W_{xx}v+W_xA_\beta v\right).
 \tag{4.5}
\]

Substitution into (4.3) cancels both first-derivative commutator terms and
leaves

\[
 \boxed{
 q_d=(-\mathcal L-icW)q
 -icW_{xx}\mathcal L^{-1}q.}
 \tag{4.6}
\]

The sign of the pressure feedback in (4.6) is negative.  It can also be
checked from the traditional form

\[
 \left(\partial_d+icW+\mathcal L\right)
 (-\mathcal Lv)-icW_{xx}v=0.
 \tag{4.7}
\]

Equation (4.6) is not the R0.72X scalar equation: it contains the nonlocal
pressure feedback \(-icW_{xx}\mathcal L^{-1}\).

**Verdict:** `exactOrrSommerfeldRow=CLOSED`.  Treating the R0.72X scalar
generator as the complete Orr--Sommerfeld generator is **FALSE**.

---

## 5. Squire equation and sign audit

Define the cell-scaled wall-normal vorticity

\[
 \eta=i\gamma u_1-i\xi u_3.
 \tag{5.1}
\]

The first and third component equations from (3.2) are

\[
 (u_1)_d=-\mathcal Lu_1-icWu_1-i\xi\pi,
 \tag{5.2}
\]

\[
 (u_3)_d=-\mathcal Lu_3-icWu_3
 -\Lambda W_xv-i\gamma\pi.
 \tag{5.3}
\]

Multiply (5.2) by \(i\gamma\), multiply (5.3) by \(-i\xi\), and add.  The
pressure terms are

\[
 i\gamma(-i\xi\pi)-i\xi(-i\gamma\pi)
 =\gamma\xi\pi-\xi\gamma\pi=0.
 \tag{5.4}
\]

The lift term is

\[
 -i\xi(-\Lambda W_xv)=+i\xi\Lambda W_xv.
 \tag{5.5}
\]

Therefore

\[
 \boxed{
 \eta_d=(-\mathcal L-icW)\eta
 +i\xi\Lambda W_x\mathcal L^{-1}q.}
 \tag{5.6}
\]

The sign of the Squire forcing in (5.6) is positive.  The system is
triangular in the direction \(q\to\eta\), but the \(q\)-equation itself is
not the homogeneous scalar equation.

**Verdict:** `exactSquireRow=CLOSED` and
`exactOSSquireTriangularization=CLOSED`.

---

## 6. Velocity reconstruction and kinetic-energy norm

For \(\mu>0\), the divergence constraint and (5.1) give

\[
 \xi u_1+\gamma u_3=iA_\beta v,
 \qquad
 \gamma u_1-\xi u_3=-i\eta.
 \tag{6.1}
\]

The coefficient matrix in (6.1) squares to \(\mu I\).  Hence

\[
 \boxed{
 u_1=\frac{i}{\mu}
 \left(\xi A_\beta v-\gamma\eta\right),}
 \tag{6.2}
\]

\[
 \boxed{
 u_3=\frac{i}{\mu}
 \left(\gamma A_\beta v+\xi\eta\right).}
 \tag{6.3}
\]

Substitution into (5.1) returns \(\eta\), and substitution into the divergence
constraint returns zero.  Orthogonality of the two coefficient rows yields

\[
 |u_1|^2+|u_3|^2
 =\frac1\mu\left(|A_\beta v|^2+|\eta|^2\right).
 \tag{6.4}
\]

Thus the exact kinetic-energy identity is

\[
 \boxed{
 \|u\|_2^2
 =\|v\|_2^2
 +\frac1\mu
 \left(\|A_\beta v\|_2^2+\|\eta\|_2^2\right).}
 \tag{6.5}
\]

Equivalently, since \(q=\mathcal Lv\),

\[
 \|u\|_2^2
 =\frac1\mu
 \left(\|\mathcal L^{-1/2}q\|_2^2+\|\eta\|_2^2\right).
 \tag{6.6}
\]

Formula (6.6) is valid only for \(\mu>0\).  It must not be continued to
\(\mu=0\) by a limiting notation.

**Verdict:** `exactVelocityReconstruction=CLOSED` and
`exactOSSquireEnergyNorm=CLOSED`.

---

## 7. Full-row energy identity and the damping-dominated class

Take the real part of the \(L^2\) inner product of (3.2) with \(u\).  The
real multiplication \(W\) makes \(icW\) skew, the pressure term vanishes on
divergence-free data, and periodic/Bloch boundary terms cancel.  Therefore

\[
 \boxed{
 \frac12\frac d{dd}\|u\|_2^2
 +\|A_\beta u\|_2^2+\mu\|u\|_2^2
 =-\Lambda\operatorname{Re}\langle W_xv,u_3\rangle.}
 \tag{7.1}
\]

This is the row version of shear production.  It has no fixed sign.  Put

\[
 g_j=\mu+\operatorname{dist}(\beta,\mathbb Z)^2,
 \qquad
 M_K=\sup_{d\in K}\|W_x(d)\|_\infty
 \tag{7.2}
\]

on a compact physical-time interval \(K\).  Poincare and
\(2\|v\|_2\|u_3\|_2\le\|v\|_2^2+\|u_3\|_2^2\) give

\[
 \frac12\frac d{dd}\|u\|_2^2
 +\left(g_j-\frac{|\Lambda|M_K}{2}\right)\|u\|_2^2
 \le0.
 \tag{7.3}
\]

Consequently every row satisfying

\[
 \boxed{g_j>\frac{|\Lambda|M_K}{2}}
 \tag{7.4}
\]

obeys

\[
 \boxed{
 \|u(d_2)\|_2
 \le
 e^{-[g_j-|\Lambda|M_K/2](d_2-d_1)}
 \|u(d_1)\|_2.}
 \tag{7.5}
\]

Without (7.4), the same calculation still gives the finite-background bound

\[
 \|u(d_2)\|_2
 \le
 \exp\!\left(
 \frac{|\Lambda|}{2}
 \int_{d_1}^{d_2}\|W_x(s)\|_\infty\,ds
 \right)\|u(d_1)\|_2.
 \tag{7.6}
\]

Thus the high-gap, damping-dominated full rows are closed.  Equation (7.5)
does not prove enhanced dissipation in the remaining low-gap rows.

**Verdict:** `fullRowEnergyIdentity=CLOSED` and
`dampingDominatedFullRows=CLOSED`.

---

## 8. Special rows with \(\mu=0\)

The condition \(\mu=0\) means

\[
 K_x=K_z=0,qquad \xi=\gamma=c=0.
 \tag{8.1}
\]

The definitions of \(\eta\), reconstruction (6.2)--(6.3), and the energy
norm (6.5)--(6.6) are then degenerate and must not be used.

### 8.1 Nonzero Bloch residue

If \(\operatorname{dist}(\beta,\mathbb Z)>0\), the divergence constraint is

\[
 A_\beta v=0.
 \tag{8.2}
\]

Since \(A_\beta\) has no periodic kernel, \(v=0\).  Pressure is zero after
fixing its mean.  The two tangential components solve independent covariant
heat equations.  This row is strictly damped by the Bloch gap and has no
lift-up.

### 8.2 Periodic zero residue

If \(\beta=0\), then \(v\) may be constant in the cell.  The pressure source
vanishes because \(K_z=0\), but the third component still contains

\[
 (u_3)_d=\partial_x^2u_3-\Lambda W_xv.
 \tag{8.3}
\]

This is the genuine zero-horizontal-frequency lift-up row.  It must be
handled in component variables, not by inserting a pseudoinverse into
(4.6)--(6.6).

**Verdict:** `muZeroRowsSeparated=CLOSED`.  Any theorem quantifying all rows
through \(\mathcal L^{-1}\) without this split is invalid.

---

## 9. Exact zero-coupling lift-up solution

The sharper obstruction does not require \(\mu=0\).  Take

\[
 \gamma=0,\qquad \beta=0,
 \qquad \xi\ge0,
 \tag{9.1}
\]

so that

\[
 c=\varepsilon_j=0,qquad \mu=\xi^2.
 \tag{9.2}
\]

At an initial time \(d_1\), choose

\[
 u_1(d_1)=u_3(d_1)=0,qquad
 v(d_1)=v_0,
 \tag{9.3}
\]

where \(v_0\) is a normalized cell constant.  When \(\xi>0\), the physical
perturbation carries the horizontal factor \(e^{iK_xx_1}\), so it has zero
spatial mean despite being constant in the cell variable.

Let \(\tau=d_2-d_1>0\).  The second component is

\[
 v(d_2)=e^{-\xi^2\tau}v_0.
 \tag{9.4}
\]

The third component solves

\[
 (u_3)_d=(\partial_x^2-\xi^2)u_3
 -\Lambda W_x(d,x)v.
 \tag{9.5}
\]

Since \((W_x)_d=(W_x)_{xx}\),

\[
 e^{(d_2-s)\partial_x^2}W_x(s,\cdot)=W_x(d_2,\cdot).
 \tag{9.6}
\]

Duhamel's formula therefore gives the exact solution

\[
 \boxed{
 u_3(d_2,x)
 =-\Lambda\tau e^{-\xi^2\tau}
 W_x(d_2,x)v_0.}
 \tag{9.7}
\]

The sign is negative because the lift term occurs on the left of (3.2), or
equivalently as \(-\Lambda W_xv\) on the right of (9.5).

There is also a direct residual check.  Differentiating (9.7) at a variable
terminal time \(d\), with \(\tau=d-d_1\), gives

\[
 \partial_du_3-(\partial_x^2-\xi^2)u_3
 +\Lambda W_xv
 =-\Lambda\tau e^{-\xi^2\tau}
 \left[(W_x)_d-(W_x)_{xx}\right]v_0=0,
 \tag{9.7a}
\]

and (9.7) vanishes at \(d=d_1\).  Thus the displayed solution is checked both
by Duhamel's formula and by direct substitution.

For the exact collision path,

\[
 W_x(d,x)=\frac12e^{-d}
 \left[-\cos x+e^{-3d}\cos2x\right].
 \tag{9.8}
\]

Orthogonality of \(\cos x\) and \(\cos2x\), together with their mean square
\(1/2\), gives

\[
 \boxed{
 \frac1{2\pi}\int_0^{2\pi}|W_x(d,x)|^2\,dx
 =\frac18\left(e^{-2d}+e^{-8d}\right).}
 \tag{9.9}
\]

Using (9.4), (9.7), and the divergence constraint \(u_1=0\) for
\(\xi>0\), the exact amplification is

\[
 \boxed{
 \frac{\|u(d_2)\|_2^2}{\|u(d_1)\|_2^2}
 =e^{-2\xi^2\tau}
 \left[
 1+\frac{\Lambda^2\tau^2}{8}
 \left(e^{-2d_2}+e^{-8d_2}\right)
 \right].}
 \tag{9.10}
\]

Two distinct obstructions follow.

1. For \(\xi=0\), every \(\Lambda\ne0\) and \(\tau>0\) gives strict
   growth.  This row contains a constant cross-stream input and belongs to
   the \(\mu=0,\beta=0\) sector of Section 8.2.
2. For \(\xi>0\), the physical input is mean-zero.  For every fixed
   \(d_1<d_2\), the right side of (9.10) exceeds one when \(|\Lambda|\) is
   sufficiently large and grows linearly in \(|\Lambda|\) at the norm level.
   A real-valued example is obtained by adjoining the conjugate row, or
   equivalently by replacing the horizontal phase with a cosine.

Thus deleting only the global constant-velocity mode does not produce a
background-uniform contraction theorem.  This example does not assert growth
for every fixed small background amplitude, nor does it refute a theorem that
retains an explicit \(\Lambda\)-dependent lift-up payment.

**Verdict:** `exactZeroCouplingLiftUpFormula=CLOSED`,
`meanZeroLiftUpCounterexample=CLOSED`, and
`allPhysicalRowsUniformStrictContraction=FALSE`.

---

## 10. Exact scalar \(A_2\) embedding and its boundary

Assume \(\mu>0\) and impose

\[
 v=0,
 \qquad
 u=g\frac{(\gamma,0,-\xi)}{\sqrt\mu}.
 \tag{10.1}
\]

Then \(\operatorname{div}_ju=0\), the pressure source (3.7) vanishes, and
the lift term vanishes.  Equation (3.2) reduces exactly to

\[
 \boxed{
 g_d=\left[(\partial_x+i\beta)^2-\mu\right]g-icWg.}
 \tag{10.2}
\]

With \(c=\sigma\varepsilon_j\), this is precisely the scalar residue-row
equation audited in R0.72X.  In the original triangular scalar sector
\(K_x=0\), the polarization in (10.1) is the \(x_1\)-direction and \(g=f\).

Therefore the R0.72X exact \(A_2\) estimate embeds without approximation into
the full linearization, but only on the invariant subspace (10.1).  It does
not estimate (4.6), nor the forced Squire coordinate (5.6).

For scalar data, one always has

\[
 \frac12\frac d{dd}\|g\|_2^2
 =-\|A_\beta g\|_2^2-\mu\|g\|_2^2.
 \tag{10.3}
\]

Thus weak scalar rows retain their bare heat/Bloch damping even when the
R0.72X strong-coupling threshold is unavailable.  This scalar energy fact
does not control shear production in (7.1).

**Verdict:** `scalarA2InvariantEmbedding=CLOSED`, while
`scalarA2EqualsCompleteRow=FALSE`.

---

## 11. Strong, weak, damped, and zero-coupling ledger

The coupling classes must be intersected with polarization and damping
information.

| Class | Exact conclusion | Audit status |
|---|---|---|
| \(\varepsilon_j\ge4\), scalar invariant subspace (10.1) | R0.72X exact \(A_2\) block and common-floor direct sum apply | **CLOSED by R0.72X** |
| \(\varepsilon_j\ge4\), complete row | Equations (4.6) and (5.6) add pressure feedback and lift-up | **OPEN** |
| \(0<\varepsilon_j<4\), scalar invariant subspace | Bare heat/Bloch estimate (10.3) applies rowwise | **CLOSED rowwise**, no uniform \(A_2\) rate claimed |
| Any coupling with (7.4) | Full velocity decays by (7.5) | **CLOSED** |
| Low-gap weak complete rows | Neither R0.72X nor (7.5) closes them | **OPEN** |
| \(\varepsilon_j=0\), scalar tangential subspace | Covariant heat flow; gapless tangential constants do not decay | **CLOSED / nondecay** |
| \(\varepsilon_j=0\), complete row | Exact lift-up (9.7)--(9.10) may grow | **FALSE for uniform strict contraction** |
| \(\mu=0,\beta\ne0\) | Divergence forces \(v=0\); Bloch heat damping | **CLOSED** |
| \(\mu=0,\beta=0\) | Inverse-operator OS--Squire coordinates degenerate; component lift-up remains | **CLOSED structural split** |

In particular, the label \(\varepsilon_j=0\) does not mean that every
background coupling is zero: \(c=\gamma\Lambda\) vanishes, while the lift
coefficient \(\xi\Lambda\) can remain nonzero.

---

## 12. Final claim ledger

\[
\boxed{
\begin{aligned}
\texttt{exactThreeDimensionalLinearization}&=\texttt{CLOSED},\\
\texttt{exactPressurePoissonFactorTwo}&=\texttt{CLOSED},\\
\texttt{exactBlochLerayNormalization}&=\texttt{CLOSED},\\
\texttt{exactFourierRowDirectSum}&=\texttt{CLOSED},\\
\texttt{exactOrrSommerfeldRow}&=\texttt{CLOSED},\\
\texttt{exactSquireRow}&=\texttt{CLOSED},\\
\texttt{exactVelocityReconstruction}&=\texttt{CLOSED},\\
\texttt{fullRowEnergyIdentity}&=\texttt{CLOSED},\\
\texttt{dampingDominatedFullRows}&=\texttt{CLOSED},\\
\texttt{muZeroRowsSeparated}&=\texttt{CLOSED},\\
\texttt{exactZeroCouplingLiftUpFormula}&=\texttt{CLOSED},\\
\texttt{meanZeroLiftUpCounterexample}&=\texttt{CLOSED},\\
\texttt{scalarA2InvariantEmbedding}&=\texttt{CLOSED},\\
\texttt{scalarA2EqualsCompleteRow}&=\texttt{FALSE},\\
\texttt{epsilonOnlyFullRowClosure}&=\texttt{FALSE},\\
\texttt{allPhysicalRowsUniformStrictContraction}&=\texttt{FALSE},\\
\texttt{strongFullRowA2Estimate}&=\texttt{OPEN},\\
\texttt{scaleSharpOSPressureAbsorption}&=\texttt{OPEN},\\
\texttt{orientationUniformSquireTransfer}&=\texttt{OPEN},\\
\texttt{lowGapWeakFullRows}&=\texttt{OPEN},\\
\texttt{nonlinearNavierStokes}&=\texttt{OPEN},\\
\texttt{Clay}&=\texttt{OPEN}.
\end{aligned}}
\tag{12.1}
\]

The strongest defensible R0.72Y statement at this stage is therefore an exact
Fourier--Leray/Orr--Sommerfeld--Squire decomposition plus the explicit
zero-coupling lift-up obstruction.  It is not a complete full-row
enhanced-dissipation theorem.

---

## 13. Remaining uncertainties and required next estimates

1. The formulas above use the explicit amplitude convention
   \(A_b=2\delta a\) and time scaling \(d=\nu R^2(t-t_*)\).  Any release that
   suppresses \(\nu\) must state that \(\nu=1\); otherwise (1.9) loses a
   factor \(\nu^{-1}\).
2. The abstract scalar damping \(\mu\) in R0.72X becomes exactly
   \((K_x^2+K_z^2)/R^2\) in this full three-dimensional reconstruction.  If a
   different physical geometry adds orthogonal labels, their squares must be
   included explicitly.
3. R0.72X's \(L_d^2L_x^2\) Duhamel estimate does not by itself absorb
   \(-icW_{xx}\mathcal L^{-1}q\) at the required collision scale, uniformly
   in low-gap rows.
4. Even if the Orr--Sommerfeld coordinate is controlled, the factor
   \(\xi\Lambda\) in (5.6) requires an orientation-sensitive payment or a
   damping tradeoff.  A coupling floor for \(|c|=|\gamma\Lambda|\) does not
   control \(|\xi\Lambda|\).
5. The lift-up example rules out a background-uniform contraction based only
   on \(\varepsilon_j\).  It does not rule out a full-row theorem with an
   explicit transient-growth prefactor, a projection excluding a larger
   invariant family, or a combined damping/orientation weight.
6. No statement here controls nonlinear convolution between rows, vortex
   stretching, a continuation norm, or the Clay regularity problem.
