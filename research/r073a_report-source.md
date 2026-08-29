# R0.73A report source: the hidden physical mean mode and a finite-transient long-wave OS bound

**Date:** 2026-08-29

**Status:** analytic pass; the independent physical-theorem and projection
audits have passed with all required scope edits applied.  The deterministic
formal certificate, formal figure, and publication gates remain pending at
this source-freeze stage.

**Keywords:** Orr--Sommerfeld, physical long-wave limit, zero-mode
cancellation, transient growth, moving tangent projection, nonnormality,
heat-decaying shear

---

## 0. Direct decision and claim boundary

Retain the heat path

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x
 \tag{0.1}
\]

and the physical two-dimensional long-wave family

\[
 \beta=\xi=0,\qquad \gamma\ne0,\qquad
 \mu=\gamma^2\in(0,1],\qquad c=\gamma\Lambda\in\mathbb R.
 \tag{0.2}
\]

The central structural decision is that the raw mean of Orr--Sommerfeld
vorticity is the wrong low-gap coordinate.  The regular physical coordinate
is

\[
 h=\mu^{-1}\Pi_0q=\Pi_0(\mathcal L_\mu^{-1}q),
 \qquad r=Q_0q,
 \qquad q=\mu h+r,
 \tag{0.3}
\]

where \(h\) is the mean wall-normal velocity.  In this coordinate, an exact
zero-mode cancellation removes every \(1/\mu\) coefficient and yields an
all-start evolution estimate with a finite transient prefactor.

Within the stated row, norm, rate, domain, and parameter scope, the audited
positive conclusions are

\[
\boxed{
\begin{aligned}
\texttt{exactPhysicalMeanOSCancellation}&=\texttt{CLOSED},\\
\texttt{exactMeanVelocityZeroMeanVorticitySystem}&=\texttt{CLOSED},\\
\texttt{renormalizedPhysicalLongWaveOSTransientPropagator}&=\texttt{CLOSED},\\
\texttt{renormalizedPhysicalLongWaveOSForcedDuhamel}&=\texttt{CLOSED},\\
\texttt{exactPhysicalTangentLiftedLineNoninvariance}&=\texttt{CLOSED},\\
\texttt{exactMovingTangentQuotientAlgebra}&=\texttt{CLOSED},\\
\texttt{orthogonalTangentProjectionSpeed}&=\texttt{CLOSED},\\
\texttt{explicitOrthogonalTangentBlocks}&=\texttt{CLOSED}.
\end{aligned}}
\tag{0.4}
\]

The following proposed simplifications have audited exact counterarguments.
In the first key, "closes" means that the
lifted line \(h=0\),
\(r\in\operatorname{span}\{W_{xx}(d)\}\) is an invariant and sufficient
one-dimensional physical state; it does not refer to the general moving
quotient identity in Sec. 7.  The fixed-two-harmonic claim below concerns the
coupled row \(c\ne0\); at \(c=0\), the heat generator preserves that fixed
space:

\[
\boxed{
\begin{aligned}
\texttt{rankOneAbstractTangentClosesPhysicalLongWaveLimit}
 &=\texttt{FALSE},\\
\texttt{fixedTwoHarmonicOSInvariance}
 &=\texttt{FALSE},\\
\texttt{twoSidedInvariantOrthogonalTangentSplit}
 &=\texttt{FALSE},\\
\texttt{uniformlyBoundedPositiveGapTangentDualPressureBlock}
 &=\texttt{FALSE}.
\end{aligned}}
\tag{0.5}
\]

The following remain open:

\[
\boxed{
\begin{aligned}
\texttt{lowGapOSTransientA2Propagator}&=\texttt{OPEN},\\
\texttt{lowGapPhysicalKineticPropagator}&=\texttt{OPEN},\\
\texttt{generalBlochLowGapOSPropagator}&=\texttt{OPEN},\\
\texttt{lowGapOSSquirePropagator}&=\texttt{OPEN},\\
\texttt{BlochUniformPhysicalVelocityDirectSum}&=\texttt{OPEN},\\
\texttt{nonlinearNavierStokes}&=\texttt{OPEN},\\
\texttt{Clay}&=\texttt{OPEN}.
\end{aligned}}
\tag{0.6}
\]

The new positive theorem is a viscous-rate estimate in a hybrid
mean-velocity/mean-zero-vorticity norm.  It is not an enhanced-dissipation
theorem and is not uniformly equivalent to the physical kinetic norm.

---

## 1. Scope and provenance

R0.72Y derived the exact Fourier-row Orr--Sommerfeld--Squire system.  R0.72Z
closed a signed high-gap \(L^2_q\) class and found the exact abstract
gapless tangent solution \(q_*=W_{xx}\).  The low-gap physical row, its
transient prefactor, and the relation between the abstract tangent and the
physical singular limit remained open.

This section restricts the first positive theorem to (0.2).  It does not
cover a nonzero Bloch residue, a nonzero Squire orientation, or the direct
sum over three-dimensional Fourier rows.  The supplied thesis gives the
standard linearized equations and normal-mode setting, but it does not give
the heat path (0.1), the zero-mode cancellation below, or the resulting
all-start transient estimate.

The literature audit found stationary long-wave Kato reductions, active
periodic Orr--Sommerfeld estimates in fixed geometry, and all-start
nonautonomous propagators under strong monotonicity and spectral-stability
hypotheses.  It did not find a theorem combining the present heat collision,
physical zero-mode singularity, explicit transient prefactor, Squire
transfer, and Bloch-uniform physical direct sum.

---

## 2. Exact physical zero-mode cancellation

Let

\[
 \mathcal L_\mu=-\partial_x^2+\mu,
 \qquad
 B_\mu(d)q=Wq+W_{xx}\mathcal L_\mu^{-1}q,
 \tag{2.1}
\]

and consider

\[
 q_d=-\mathcal L_\mu q-icB_\mu(d)q+F_q.
 \tag{2.2}
\]

Write \(\Pi_0\) for the normalized periodic mean and \(Q_0=I-\Pi_0\).
For mean-zero \(r\), put \(s_r=\mathcal L_\mu^{-1}r\).  Then \(s_r\) is
mean-zero and

\[
 r=-s_{r,xx}+\mu s_r.
 \tag{2.3}
\]

Periodic integration by parts twice gives

\[
 \begin{aligned}
 \Pi_0(Wr)
 &=\Pi_0(-Ws_{r,xx}+\mu Ws_r)\\
 &=-\Pi_0(W_{xx}s_r)+\mu\Pi_0(Ws_r).
 \end{aligned}
 \tag{2.4}
\]

Therefore

\[
 \boxed{
 \Pi_0\!\left(Wr+W_{xx}\mathcal L_\mu^{-1}r\right)
 =\mu\Pi_0\!\left(W\mathcal L_\mu^{-1}r\right).}
 \tag{2.5}
\]

This is the decisive cancellation.  It is an exact identity for every
mean-zero \(r\); it is not a small-parameter expansion or a finite Fourier
observation.

For the mean part \(\mu h\),

\[
 B_\mu(\mu h)=h(W_{xx}+\mu W),
 \qquad \Pi_0(W_{xx}+\mu W)=0.
 \tag{2.6}
\]

Projecting (2.2), using \(q=\mu h+r\), and dividing only the already
cancelled mean equation by \(\mu\), yields the exact forced system

\[
 \boxed{
 \begin{aligned}
 h_d&=-\mu h-ic\Pi_0(W\mathcal L_\mu^{-1}r)
       +\mu^{-1}\Pi_0F_q,\\
 r_d&=-\mathcal L_\mu r
 -icQ_0\!\left(Wr+W_{xx}\mathcal L_\mu^{-1}r\right)\\
 &\qquad-ic\,h(W_{xx}+\mu W)+Q_0F_q.
 \end{aligned}}
 \tag{2.7}
\]

Every homogeneous coefficient in (2.7) is regular as \(\mu\downarrow0\).
The forcing coordinate retains the honest \(\mu^{-1}\Pi_0F_q\) payment.

---

## 3. A regular physical state space

Use the normalized periodic \(L^2\) norm and define

\[
 \|(h,r)\|_{X_\mu}^2=|h|^2+\|r\|_2^2.
 \tag{3.1}
\]

This norm treats the physical mean wall-normal velocity and the mean-zero
OS vorticity as independent coordinates.  On \(Q_0L^2\),

\[
 \|\mathcal L_\mu^{-1}r\|_2
 \le\frac1{1+\mu}\|r\|_2,
 \qquad
 \langle\mathcal L_\mu r,r\rangle
 \ge(1+\mu)\|r\|_2^2.
 \tag{3.2}
\]

For each fixed \(\mu>0\), the nonlocal terms in (2.7) are bounded
perturbations of \((-\mu)\oplus(-\mathcal L_\mu)\).  Their coefficients are
continuous in \(d\), so the homogeneous system defines a two-parameter
evolution family on \(\mathbb C\oplus Q_0L^2\).

---

## 4. The all-start finite-transient theorem

Define

\[
 \begin{aligned}
 b_\mu(d)&=\|W\|_\infty
 +\frac{\|W_{xx}\|_\infty}{1+\mu},\\
 p_\mu(d)&=\frac{\|W\|_2}{1+\mu},\\
 k_\mu(d)&=\|W_{xx}+\mu W\|_2.
 \end{aligned}
 \tag{4.1}
\]

The diagonal OS perturbation and the two off-diagonal couplings satisfy

\[
 \left|\left\langle
 Q_0(Wr+W_{xx}\mathcal L_\mu^{-1}r),r
 \right\rangle\right|
 \le b_\mu\|r\|_2^2,
 \tag{4.2}
\]

\[
 \left|\Pi_0(W\mathcal L_\mu^{-1}r)\right||h|
 \le p_\mu|h|\|r\|_2,
 \tag{4.3}
\]

\[
 \left|\langle h(W_{xx}+\mu W),r\rangle\right|
 \le k_\mu|h|\|r\|_2.
 \tag{4.4}
\]

For

\[
 X(d)=|h(d)|^2+\|r(d)\|_2^2,
 \tag{4.5}
\]

the real part of the homogeneous system, together with
\(2|h|\|r\|_2\le X\), gives

\[
 \frac12X'
 \le-\mu X
 +|c|\left[b_\mu+\frac12(p_\mu+k_\mu)\right]X.
 \tag{4.6}
\]

For \(0<\mu\le1\), normalized \(L^2\) is bounded by \(L^\infty\), and

\[
 b_\mu+\frac12(p_\mu+k_\mu)
 \le2\|W\|_\infty+\frac32\|W_{xx}\|_\infty.
 \tag{4.7}
\]

The profile (0.1) therefore gives the explicit integrable majorant

\[
 C_W(d)=\frac74e^{-d}+2e^{-4d},
 \tag{4.8}
\]

\[
 J(s,d)=\int_s^dC_W(\tau)\,d\tau
 =\frac74(e^{-s}-e^{-d})
 +\frac12(e^{-4s}-e^{-4d})
 \le\frac94e^{-s}.
 \tag{4.9}
\]

Gronwall applied to \(X\), followed by a square root, proves

\[
 \boxed{
 \|(h(d),r(d))\|_{X_\mu}
 \le e^{-\mu(d-s)+|c|J(s,d)}
 \|(h(s),r(s))\|_{X_\mu}}
 \tag{4.10}
\]

for every \(d\ge s\ge0\).  In particular, when \(|c|\le4\),

\[
 \boxed{
 \|U_\mu(d,s)\|_{X_\mu\to X_\mu}
 \le e^9e^{-\mu(d-s)}.}
 \tag{4.11}
\]

The exponent \(9\) is a transparent uniform upper bound, not an optimized
transient constant.  The important result is the absence of a
\(\mu\)-dependent prefactor in \(X_\mu\), while the long-time rate remains
the viscous rate \(\mu\).

---

## 5. Forced Duhamel estimate

Define the transformed forcing

\[
 \mathfrak F_\mu(d)
 =\left(\mu^{-1}\Pi_0F_q(d),Q_0F_q(d)\right).
 \tag{5.1}
\]

Assume
\(\mathfrak F_\mu\in L^1_{\mathrm{loc}}
([s,d];\mathbb C\oplus Q_0L^2)\).  Variation of constants and (4.10) give

\[
 \boxed{
 \begin{aligned}
 \|(h(d),r(d))\|_{X_\mu}
 &\le e^{-\mu(d-s)+|c|J(s,d)}
 \|(h(s),r(s))\|_{X_\mu}\\
 &\quad+\int_s^d
 e^{-\mu(d-\tau)+|c|J(\tau,d)}
 \|\mathfrak F_\mu(\tau)\|_{X_\mu}\,d\tau.
 \end{aligned}}
 \tag{5.2}
\]

The mean forcing payment is part of the theorem.  Deleting it would change
the norm or the physical variable.

---

## 6. The lifted tangent line is not invariant at positive gap

At exactly \(\mu=0\), on the abstract mean-zero space,

\[
 q_*=W_{xx},\qquad
 (-\partial_x^2)^{-1}q_*=-W
 \tag{6.1}
\]

is an exact solution of the gapless OS equation.  This remains true and is
not retracted.

For the physical family \(\mu>0\), initialize instead

\[
 h(s)=0,\qquad r(s)=W_{xx}(s),
 \qquad c=c_\mu=\gamma\Lambda_\mu.
 \tag{6.2}
\]

The first equation in (2.7) gives the exact derivative

\[
 \boxed{
 h_d(s)=ic_\mu\left[
 \frac{e^{-2s}}{8(1+\mu)}
 +\frac{e^{-8s}}{8(4+\mu)}
 \right].}
 \tag{6.3}
\]

Hence, along a specified parameter path on which
\(c_\mu\to c_0\),

\[
 h_d(s)\longrightarrow
 ic_0\left(\frac18e^{-2s}+\frac1{32}e^{-8s}\right)
 =ic_0\Pi_0(W(s)^2)
 \tag{6.4}
\]

as \(\mu\downarrow0\).  This limit is nonzero when \(c_0\ne0\).  Since
\(c_\mu=\gamma\Lambda_\mu\) and \(\mu=\gamma^2\), such a path requires
\(|\Lambda_\mu|\) to grow like \(|\gamma|^{-1}\).  If \(\Lambda\) is held
fixed, then \(c_\mu\to0\) and this instantaneous derivative tends to zero;
the present calculation does not decide that singular limit.

For every fixed \(\mu>0\) with \(c_\mu\ne0\), the lifted line
\(h=0\), \(r\in\operatorname{span}\{W_{xx}(d)\}\) is not invariant.
Consequently a \(W_{xx}\)-amplitude alone is not a sufficient state variable
for the physical positive-gap evolution.  This is a mismatch in the lifted
\(X_\mu\)-type phase space.  Because the raw mean is \(\mu h\), the
instantaneous calculation by itself does not disprove convergence in every
topology applied only to raw \(q\).

---

## 7. Exact moving-tangent quotient algebra

The previous mismatch does not make the abstract tangent useless.  It
instead requires a precise distinction between a trajectory bundle, an
invariant splitting, and the physical singular limit.

Let \(H\) be a Hilbert space, let \(\mathscr A(d)\) have a common dense
domain \(D\), and let
\(\phi\in C^1(I;H)\cap C(I;D)\) be a strong solution satisfying

\[
 \phi_d=\mathscr A(d)\phi.
 \tag{7.1}
\]

Let \(\psi\in C^1(I;H)\) be a normalized dual with
\(\psi(d)\in D(\mathscr A(d)^*)\) for every \(d\), and assume
\(d\mapsto\mathscr A(d)^*\psi(d)\) is continuous:

\[
 \langle\psi,\phi\rangle=1,
 \qquad P=\phi\otimes\psi,
 \qquad Q=I-P,
 \tag{7.2}
\]

Then one has

\[
 P_d=\phi_d\otimes\psi+\phi\otimes\psi_d,
 \qquad
 Q\mathscr AP=P_dP.
 \tag{7.3}
\]

For a strong solution
\(q\in C^1(I;H)\cap C(I;D)\) of \(q_d=\mathscr Aq\), put

\[
 a=\langle\psi,q\rangle,
 \qquad z=Qq.
 \tag{7.4}
\]

Then the exact triangular equations are

\[
 \boxed{
 a_d=\langle\psi_d+\mathscr A^*\psi,z\rangle,}
 \tag{7.5}
\]

\[
 \boxed{
 z_d=\mathscr Az
 -\phi\langle\psi_d+\mathscr A^*\psi,z\rangle
 =(Q\mathscr AQ-P_dQ)z.}
 \tag{7.6}
\]

The tangent amplitude does not force the complement.  The complement can
still force the amplitude.  Both moving blocks are invariant if and only if

\[
 \boxed{\psi_d=-\mathscr A^*\psi.}
 \tag{7.7}
\]

For the gapless OS generator, (7.7) is forward anti-parabolic.  When
\(c\ne0\), its pressure adjoint also generates new Fourier modes, so a
uniformly bounded transported dual is a new analytic problem rather than a
finite-dimensional projection choice.  At \(c=0\), finite Fourier support is
preserved, although the forward anti-heat growth still prevents a generic
\(L^2\) all-start construction.

---

## 8. The orthogonal tangent line is regular but not decoupled

On the abstract mean-zero row, set

\[
 a=e^{-d},\qquad b=e^{-4d},
 \qquad
 \phi=W_{xx}=\frac a2\sin x-b\sin2x.
 \tag{8.1}
\]

Let

\[
 N=\|\phi\|_2^2=\frac{a^2}{8}+\frac{b^2}{2},
 \qquad \psi_\perp=\frac\phi N,
 \qquad P_\perp=\phi\otimes\psi_\perp.
 \tag{8.2}
\]

With

\[
 \theta=b\sin x+\frac a2\sin2x,
 \qquad
 \zeta=Q_\perp\phi_d=\omega\theta,
 \tag{8.3}
\]

one obtains

\[
 \omega=\frac{3r_*}{1+r_*^2},
 \qquad r_*=2e^{-3d}.
 \tag{8.4}
\]

Consequently

\[
 \boxed{
 \|(P_\perp)_d\|=|\omega|\le\frac32,}
 \tag{8.5}
\]

with equality at \(d=(\log2)/3\).  The moving line has no singular
kinematic rotation.

The adjoint pressure vector is nevertheless nonzero:

\[
 \boxed{
 \begin{aligned}
 G:=\mathscr B_0^*\phi
 &=-\frac{3ab}{16}\cos x
 +\frac{3a^2}{32}\cos2x\\
 &\quad-\frac{37ab}{144}\cos3x
 +\frac{3b^2}{32}\cos4x.
 \end{aligned}}
 \tag{8.6}
\]

The orthogonal defect is

\[
 \psi_{\perp,d}+\mathscr A_0^*\psi_\perp
 =\frac{2\zeta+icG}{N}.
 \tag{8.7}
\]

Thus the orthogonal quotient is exact but contains a nonzero
complement-to-tangent block proportional to \(|c|G\).  Bounded projection
speed does not imply a small projected OS generator.

---

## 9. The two-harmonic carrier is not invariant when \(c\ne0\)

The fixed space

\[
 \mathcal S=\operatorname{span}\{\sin x,\sin2x\}
 \tag{9.1}
\]

contains \(\phi\) and \(\phi_d\), so it is the minimal fixed heat/tangent
carrier.  For

\[
 q=x_1\sin x+x_2\sin2x,
 \tag{9.2}
\]

direct Fourier multiplication gives

\[
 \boxed{
 \mathscr B_0q
 =-\frac3{16}(a x_2+2b x_1)(\cos x-\cos3x).}
 \tag{9.3}
\]

Only the tangent line \(a x_2+2b x_1=0\) lies in this pressure-coupling
kernel.  Because \(-\mathcal L_0\mathcal S\subset\mathcal S\), (9.3)
proves that the full instantaneous OS generator does not preserve
\(\mathcal S\) whenever \(c\ne0\).  At \(c=0\), the full generator is just
\(-\mathcal L_0\), so \(\mathcal S\) is invariant.  For \(c\ne0\), return
coupling is also nonzero; for example,

\[
 \Pi_{\mathcal S}\mathscr A_0(I-\Pi_{\mathcal S})\cos x
 =\frac{3icb}{8}\sin x.
 \tag{9.4}
\]

Applying the pressure operator to \(\cos3x\) creates \(\sin4x\) and
\(\sin5x\).  No finite two-mode invariant closure follows for the coupled
row \(c\ne0\).

---

## 10. A positive-gap dual obstruction

For \(|\beta|\le1/2\), put

\[
 \mathcal L_{\beta,\mu}=(-i\partial_x+\beta)^2+\mu,
 \qquad g=\beta^2+\mu>0,
 \tag{10.1}
\]

and

\[
 \mathscr B_{\beta,\mu}^*
 =M_W+\mathcal L_{\beta,\mu}^{-1}M_\phi.
 \tag{10.2}
\]

For every dual normalized by \(\langle\psi_{\beta,\mu},\phi\rangle=1\),
the constant Fourier coefficient satisfies

\[
 \widehat{\phi\psi_{\beta,\mu}}(0)=1,
 \qquad
 \widehat{\mathcal L_{\beta,\mu}^{-1}
 (\phi\psi_{\beta,\mu})}(0)=\frac1g.
 \tag{10.3}
\]

Therefore

\[
 \boxed{
 \frac1g
 \le\|\mathscr B_{\beta,\mu}^*\psi_{\beta,\mu}\|_2
 +\|W\|_\infty\|\psi_{\beta,\mu}\|_2.}
 \tag{10.4}
\]

For fixed \(d\), or uniformly on any compact \(d\)-interval where
\(\inf_d\|\phi(d)\|_2>0\), a normalized dual family cannot keep both its
projection norm and its raw adjoint pressure vector uniformly bounded as
\(g\downarrow0\).
Moreover, if \(\|\psi\|_2\le M\), then

\[
 \boxed{
 \|Q^*\mathscr B_{\beta,\mu}^*\psi\|_2
 \ge\frac1g-\|W\|_\infty M
 -C_d(|\beta|+g)M^2.}
 \tag{10.5}
\]

Thus a uniformly bounded unweighted projection leaves a \(g^{-1}\)
divergence in the unscaled pressure off-block
\(Q^*\mathscr B_{\beta,\mu}^*\psi\).  In the full OS generator this pressure
block is multiplied by \(|c|\); the displayed estimate forces a divergent
OS contribution only along paths for which \(|c|/g\to\infty\), up to the
displayed lower-order terms.  At exactly \(g=0\), the abstract operator acts
on a different space, \(L^2_0\), and its explicit mean projection deletes
the constant coefficient.  Without first specifying a common embedding or
coordinate identification, the present calculation makes no operator-norm
continuity claim between the \(g>0\) and \(g=0\) families.

This result does not prohibit a weighted modulation theorem.  It specifies
the weight such a theorem must pay.

---

## 11. Frozen long-wave literature specialization

The stationary two-dimensional theorem of
Colombo--Dolce--Montalto--Ventura applies to each frozen profile after the
identification

\[
 \nu_{\rm lit}=|\Lambda|^{-1},\qquad
 \varepsilon_{\rm lit}=|\gamma|,
 \qquad U_{\rm lit}=\operatorname{sgn}(\Lambda)W.
 \tag{11.1}
\]

In the normalized periodic convention,

\[
 H(d)=\|\partial_x^{-1}W(d)\|_2^2
 =\frac18e^{-2d}+\frac1{128}e^{-8d}.
 \tag{11.2}
\]

After multiplying their generator by \(|\Lambda|\), their small-long-wave
expansion specializes to

\[
 \operatorname{Re}\lambda_0(d)
 =c^2H(d)-\gamma^2
 +O_W(|c|^3+|c|\mu),
 \tag{11.3}
\]

under the source theorem's smallness condition
\(|c|\le\delta_0(\|W\|_{C^2})\).  When \(|\Lambda|\ge1\), the remainder
is \(O_W(|c|^3)\).  The leading frozen instability criterion is

\[
 |\Lambda|^2H(d)>1.
 \tag{11.4}
\]

Equation (11.3) is a specialization of an existing theorem, not a new
R0.73A theorem.  Frozen instability also does not contradict (4.10): the
latter permits a finite transient factor and only asserts eventual decay at
the viscous rate for the time-dependent heat path.

---

## 12. Finite frozen spectral diagnostic

A deterministic Fourier--Galerkin audit screened 448 parameter cases at
\(N=18\), each under three compressions, and 10 target cases at
\(N=12,18,24,32,40\).  In total it recorded 1,494 matrix rows.

At the broad-screen resolution, the unprojected matrix had positive spectral
edge in 419 of 448 cases.  Removing the instantaneous \(W_{xx}\) direction
produced a nonpositive edge in only 91 cases and worsened the edge in 141.
Removing \(\operatorname{span}\{\sin x,\sin2x\}\) produced a nonpositive
edge in 180 cases and worsened it in 111.

All ten target unprojected matrices retained positive spectral edge at
\(N=40\).  A representative spectrally stable two-mode compression still
had numerical abscissa \(336.082\), sampled semigroup gain \(2.054\), and a
sampled Kreiss lower bound \(1.550\).  This supports the need for a transient
prefactor and argues against concatenating frozen eigenvalues.

The \(N=32\) to \(N=40\) maximum relative spectral-edge difference was
below \(1.60\times10^{-3}\), and the maximum difference in sampled
base-ten log gain was below \(5.67\times10^{-6}\).  The independent finite
checker passed all 13 declared checks.

These are finite diagnostics only.  There is no Galerkin tail enclosure,
spectral-pollution theorem, continuous-time gain optimizer, certified
pseudospectrum, or infinite-dimensional frozen spectral conclusion.  The
projected matrices are compressions \(Q^*AQ\), not invariant quotients.

---

## 13. Exact norm boundary

The three relevant norms satisfy

\[
 \|q\|_2^2=\mu^2|h|^2+\|r\|_2^2,
 \tag{13.1}
\]

\[
 \|(h,r)\|_{X_\mu}^2=|h|^2+\|r\|_2^2,
 \tag{13.2}
\]

and, for the OS component of physical kinetic energy,

\[
 Q_{\rm kin}^2
 =\mu^{-1}\|\mathcal L_\mu^{-1/2}q\|_2^2
 =|h|^2+\mu^{-1}
 \|\mathcal L_\mu^{-1/2}r\|_2^2.
 \tag{13.3}
\]

The map from raw \(L^2_q\) to \(X_\mu\) loses \(\mu^{-1}\) in one
direction.  On a nonzero Fourier mode \(k\), the second kinetic multiplier
is \([\mu(k^2+\mu)]^{-1}\).  Therefore neither raw \(L^2_q\) nor kinetic
energy is uniformly equivalent to \(X_\mu\) as \(\mu\downarrow0\).

No conclusion in Secs. 4--5 may be exported to either norm without a new
weighted argument.

---

## 14. What is new and what is not

The audited analytic increment of this section consists of:

1. the exact physical zero-mode cancellation (2.5);
2. the regular mean-velocity/mean-zero-vorticity system (2.7);
3. the all-start finite-transient bound (4.10) and forced estimate (5.2);
4. the exact positive-gap noninvariance and the path-qualified lifted
   tangent mismatch (6.3)--(6.4);
5. the moving-tangent quotient identities (7.3)--(7.7);
6. the explicit orthogonal projection speed and pressure block
   (8.5)--(8.7);
7. the exact two-mode pressure leakage and, for \(c\ne0\), noninvariance
   witness (9.3)--(9.4); and
8. the positive-gap unweighted pressure-dual obstruction (10.4)--(10.5),
   with the full OS coefficient retaining its explicit \(|c|\) factor.

The stationary long-wave eigenvalue expansion in Sec. 11 belongs to the
cited literature.  The sweep in Sec. 12 is a reproducible finite diagnostic,
not an operator theorem.

---

## 15. Mathematical value and remaining distance

This section makes a real but scoped advance.  It replaces a singular raw
coordinate by the physical mean velocity, proves that the resulting
nonautonomous OS family has a finite all-start transient factor, and rules
out two tempting but insufficient projection strategies.  It also explains
why R0.72Z's exact tangent orbit and a physical \(\mu\downarrow0\) theorem
can both be correct without being the same statement.

Its direct value for the Millennium problem remains limited.  The estimate
has only viscous-rate decay, uses a hybrid norm, and excludes the general
Bloch row, Squire lift-up, physical kinetic direct sum, nonlinear frequency
convolution, and vortex stretching.  It is best understood as a clean
linear low-gap coordinate theorem and a theorem-design constraint.

The next viable target is a weighted modulation estimate that simultaneously
tracks the physical mean coordinate, the tangent carrier, the near-constant
mode, and the adjoint pressure cost.  The target must retain explicit
\(g\)-, \(|c|\)-, \(|\Lambda|\)-, and orientation payments and must seek an
\(A_2\)-scale improvement only after the physical kinetic norm is controlled.

---

## 16. Reproducibility and release requirements

The release must bind:

- this canonical report, the problem freeze, gap matrix, literature audit,
  and independent analytic audit;
- two independent deterministic constructions of the transformed Fourier
  generator and its zero-mode cancellation;
- a direct finite propagator comparison against (4.10);
- the exact hidden-mean derivative (6.3);
- the frozen spectral diagnostic and its independent validator;
- a journal figure in PDF, SVG, and 600 dpi PNG;
- source hashes, environment records, and a fail-closed release manifest;
- Chinese and English HTML notes, synchronized PDFs, the cumulative recap,
  literature page, home route, publication counters, and live byte checks.

The scoped analytic statuses in (0.4)--(0.5) are now CLOSED/FALSE after two
independent audits.  This section is not counted as published or formally
sealed until the remaining certificate, figure, bilingual, PDF, release, and
live-deployment gates pass.
