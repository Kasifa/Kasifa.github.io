# R0.73A analytic proof draft: a regular physical long-wave OS system

**Date:** 2026-08-29

**Audit state:** complete analytic draft; source-stage until independently
re-derived and certificate-bound.

## 1. Theorem statement

Let

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad \mathcal L_\mu=-\partial_x^2+\mu,
 \tag{1.1}
\]

and consider the physical two-dimensional long-wave Orr--Sommerfeld row

\[
 q_d=-\mathcal L_\mu q
 -ic\left(Wq+W_{xx}\mathcal L_\mu^{-1}q\right),
 \tag{1.2}
\]

where

\[
 \beta=\xi=0,\qquad \mu=\gamma^2\in(0,1],
 \qquad c=\gamma\Lambda\in\mathbb R.
 \tag{1.3}
\]

Write

\[
 h=\mu^{-1}\Pi_0q,qquad r=Q_0q,qquad
 \|(h,r)\|_{X_\mu}^2=|h|^2+\|r\|_2^2.
 \tag{1.4}
\]

Then the evolution family \(U_\mu(d,s)\) of (1.2) satisfies, for every
\(d\ge s\ge0\),

\[
 \boxed{
 \|U_\mu(d,s)q_s\|_{X_\mu}
 \le e^{-\mu(d-s)+|c|J(s,d)}\|q_s\|_{X_\mu},}
 \tag{1.5}
\]

where the notation on each side means the transformed pair in (1.4), and

\[
 J(s,d)=\frac74(e^{-s}-e^{-d})
 +\frac12(e^{-4s}-e^{-4d}).
 \tag{1.6}
\]

In particular,

\[
 J(s,d)\le\frac94e^{-s}\le\frac94,
 \tag{1.7}
\]

so that \(|c|\le4\) gives the estimate, uniform for
\(0<\mu\le1\), \(d\ge s\ge0\), in \(X_\mu\),

\[
 \boxed{
 \|U_\mu(d,s)\|_{X_\mu\to X_\mu}
 \le e^9e^{-\mu(d-s)}.}
 \tag{1.8}
\]

This is a viscous-rate estimate with a finite transient prefactor.  It is
not an enhanced-dissipation or scalar-\(A_2\)-rate estimate.

## 2. Exact physical mean cancellation

Let \(s_r=\mathcal L_\mu^{-1}r\).  Since \(r\) has zero mean, so does
\(s_r\), and

\[
 r=-\partial_x^2s_r+\mu s_r.
 \tag{2.1}
\]

Twice integrating by parts on the periodic cell gives

\[
 \begin{aligned}
 \Pi_0(Wr)
 &=\Pi_0(-Ws_{r,xx}+\mu Ws_r)\\
 &=-\Pi_0(W_{xx}s_r)+\mu\Pi_0(Ws_r).
 \end{aligned}
 \tag{2.2}
\]

Therefore

\[
 \boxed{
 \Pi_0\left(Wr+W_{xx}\mathcal L_\mu^{-1}r\right)
 =\mu\Pi_0\left(W\mathcal L_\mu^{-1}r\right).}
 \tag{2.3}
\]

For the mean component, \(\mathcal L_\mu^{-1}(\mu h)=h\), so

\[
 W(\mu h)+W_{xx}\mathcal L_\mu^{-1}(\mu h)
 =h(W_{xx}+\mu W),
 \tag{2.4}
\]

which is mean-zero.  Projecting (1.2), using \(q=\mu h+r\), and dividing
the mean equation by \(\mu\) yields the exact regular system

\[
 \boxed{
 \begin{aligned}
 h_d&=-\mu h-ic\,\Pi_0(W\mathcal L_\mu^{-1}r),\\
 r_d&=-\mathcal L_\mu r
 -icQ_0\left(Wr+W_{xx}\mathcal L_\mu^{-1}r\right)
 -ic\,h(W_{xx}+\mu W).
 \end{aligned}}
 \tag{2.5}
\]

The cancellation (2.3) removes every \(1/\mu\) coefficient.  For fixed
\(\mu>0\), existence of the evolution family follows by treating the
continuous-in-\(d\) multiplication/inverse-Laplacian part as a bounded
perturbation of \((-\mu)\oplus(-\mathcal L_\mu)\) on
\(\mathbb C\oplus Q_0L^2\).

## 3. Energy estimate and explicit prefactor

Set

\[
 X(d)=|h(d)|^2+\|r(d)\|_2^2.
 \tag{3.1}
\]

On the mean-zero subspace,

\[
 \|\mathcal L_\mu^{-1}r\|_2
 \le\frac1{1+\mu}\|r\|_2,
 \qquad
 \langle\mathcal L_\mu r,r\rangle
 \ge(1+\mu)\|r\|_2^2.
 \tag{3.2}
\]

Define

\[
 \begin{aligned}
 b_\mu(d)&=\|W\|_\infty
 +\frac{\|W_{xx}\|_\infty}{1+\mu},\\
 p_\mu(d)&=\frac{\|W\|_2}{1+\mu},\\
 k_\mu(d)&=\|W_{xx}+\mu W\|_2.
 \end{aligned}
 \tag{3.3}
\]

The diagonal nonlocal term is bounded by

\[
 \left|\left\langle
 Q_0(Wr+W_{xx}\mathcal L_\mu^{-1}r),r
 \right\rangle\right|
 \le b_\mu(d)\|r\|_2^2,
 \tag{3.4}
\]

and the two off-diagonal terms are bounded by

\[
 p_\mu(d)|h|\|r\|_2,
 \qquad
 k_\mu(d)|h|\|r\|_2.
 \tag{3.5}
\]

Taking the real part of (2.5) against \((h,r)\), and using
\(2|h|\|r\|_2\le X\), gives

\[
 \frac12X'
 \le-\mu X
 +|c|\left[b_\mu+\frac12(p_\mu+k_\mu)\right]X.
 \tag{3.6}
\]

For \(0<\mu\le1\),

\[
 \begin{aligned}
 b_\mu+\frac12(p_\mu+k_\mu)
 &\le2\|W\|_\infty+\frac32\|W_{xx}\|_\infty\\
 &\le\frac74e^{-d}+2e^{-4d}
 =C_W(d).
 \end{aligned}
 \tag{3.7}
\]

Gronwall applied to (3.6), followed by a square root, proves (1.5).
Integrating (3.7) gives (1.6)--(1.8).

## 4. Forced corollary and its exact payment

For

\[
 q_d=-\mathcal L_\mu q-icB_\mu(d)q+F_q,
 \tag{4.1}
\]

define the transformed forcing

\[
 \mathfrak F_\mu(d)
 =\left(\mu^{-1}\Pi_0F_q(d),Q_0F_q(d)\right).
 \tag{4.2}
\]

Assume
\(\mathfrak F_\mu\in L^1_{\mathrm{loc}}
([s,d];\mathbb C\oplus Q_0L^2)\).  Variation of constants and (1.5) give

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
 \tag{4.3}
\]

The \(\mu^{-1}\) payment on the mean forcing is explicit and cannot be
deleted from this norm.

## 5. The lifted abstract tangent line is not invariant at positive gap

At \(\mu=0\), the abstract mean-zero OS equation admits

\[
 q_*=W_{xx},\qquad(-\partial_x^2)^{-1}q_*=-W.
 \tag{5.1}
\]

For the physical \(\mu>0\) family, initialize instead
\(h(s)=0\), \(r(s)=W_{xx}(s)\), and allow
\(c=c_\mu=\gamma\Lambda_\mu\).  The first equation in (2.5) gives the exact
instantaneous hidden-mean derivative

\[
 \boxed{
 h_d(s)=ic_\mu\left[
 \frac{e^{-2s}}{8(1+\mu)}
 +\frac{e^{-8s}}{8(4+\mu)}
 \right].}
 \tag{5.2}
\]

Hence, along a specified parameter sequence for which
\(c_\mu\to c_0\),

\[
 h_d(s)\longrightarrow
 ic_0\left(\frac18e^{-2s}+\frac1{32}e^{-8s}\right)
 =ic_0\,\Pi_0(W(s)^2)
 \tag{5.3}
\]

as \(\mu\downarrow0\).  This limit is nonzero when \(c_0\ne0\); because
\(c_\mu=\gamma\Lambda_\mu\), that parameter path requires
\(|\Lambda_\mu|\) to grow like \(|\gamma|^{-1}\).  If \(\Lambda\) is held
fixed instead, then \(c_\mu\to0\) and this instantaneous derivative tends
to zero.

For every fixed positive gap with \(c_\mu\ne0\), the lifted line
\(h=0\), \(r\in\operatorname{span}\{W_{xx}(d)\}\) is not invariant.
Consequently a \(W_{xx}\)-amplitude alone is not a sufficient state variable
for the physical positive-gap evolution.  The calculation establishes a
mismatch in the lifted \(X_\mu\)-type phase space; by itself it does not
disprove convergence in every topology applied only to raw
\(q=\mu h+r\).

## 6. Norm boundary

The three relevant norms are exactly

\[
 \|q\|_2^2=\mu^2|h|^2+\|r\|_2^2,
 \tag{6.1}
\]

\[
 \|(h,r)\|_{X_\mu}^2=|h|^2+\|r\|_2^2,
 \tag{6.2}
\]

and the OS part of the physical kinetic norm,

\[
 Q_{\rm kin}^2
 =\mu^{-1}\|\mathcal L_\mu^{-1/2}q\|_2^2
 =|h|^2+\mu^{-1}
 \|\mathcal L_\mu^{-1/2}r\|_2^2.
 \tag{6.3}
\]

The map between raw \(L^2_q\) and \(X_\mu\) loses \(\mu^{-1}\) in one
direction.  The multiplier in the second term of (6.3) ranges over
\(1/[\mu(k^2+\mu)]\), \(k\ne0\), so \(X_\mu\) and physical kinetic energy
are not uniformly equivalent either.  Estimate (1.5) must not be exported
to those norms without a separate argument and the necessary
\(\Lambda\)/orientation payments.

## 7. Exact claim decision if audits pass

- `exactPhysicalMeanOSCancellation=CLOSED`.
- `exactMeanVelocityZeroMeanVorticitySystem=CLOSED`.
- `renormalizedPhysicalLongWaveOSTransientPropagator=CLOSED`.
- `renormalizedPhysicalLongWaveOSForcedDuhamel=CLOSED`.
- `rankOneAbstractTangentClosesPhysicalLongWaveLimit=FALSE`, where
  "closes" means an invariant lifted one-dimensional physical state.
- `lowGapOSTransientA2Propagator=OPEN`.
- `lowGapPhysicalKineticPropagator=OPEN`.
- `lowGapOSSquirePropagator=OPEN`.
- `BlochUniformPhysicalVelocityDirectSum=OPEN`.
- `nonlinearNavierStokes=OPEN`.
- `Clay=OPEN`.
