# R0.71Z independent audit record

**Date:** 2026-08-27  
**Decision:** PASS for the all-root BV slope-mass theorem and the
launch-inclusive mixed-window floor cancellation, subject to the scope below.

## 1. Audited theorem

For the exact real-shear triangular evolution

\[
 F'=D_qF+\delta V_z(x)F,\qquad \|F(0)\|_2^2=M,
\]

let

\[
 \Omega=\sup_{x\ge A_0}\|V_z(x)\|,
 \quad \eta=|\delta|\Omega,
 \quad I_x=[A,A+L]\subset[A_0,\infty).
\]

For distinct positive integer carrier multipliers, real shear coefficients,
and \(q\ge\max(1,2|K_y|/d)\), the complete target-root slope mass obeys

\[
\sum_{F_0(\tau)=0}|F_0'(\tau)|^2
\le e^{2\lambda_0L}(4+C_\kappa\eta)\eta^2M,
\qquad
C_\kappa=\frac{\pi^2}{\sqrt{45}\nu d^2}.
\]

For \(\delta\ne0\),

\[
G_{\rm all}^{\rm ex}
\le e^{2\lambda_0L}(4+C_\kappa\eta)M\Omega^2.
\]

If roots are counted on \(I_t=[a,b]\), while
\(\Lambda_1\) is computed on \(K_t=[\sigma_q,b]\) including launch, then

\[
\frac{\mathcal J_{\rm all}(I_t)}
{D^{1/3}\Lambda_1(K_t)}
\le C\nu^{-2}
\frac{\eta^{4/3}(1+\eta)}{M^2}.
\]

## 2. Analytic proof audit

The proof received an independent line-by-line reconstruction.

1. Real shear makes \(V_z\) skew-adjoint, so
   \(\|F(x)\|_2\le\sqrt M\) and
   \(\int-\langle D_qF,F\rangle\le M/2\).
2. The Fourier multiplier lower bound is
   \(\Omega^2\ge2K_z^2\sum_l|z_l|^2e^{-2\nu d^2r_l^2A_0}\).
3. Weighted \(r_l^{-2}\) Cauchy gives
   \(\int\|V_z\|\le\pi^2\Omega/(\sqrt{45}\nu d^2)\), hence the same
   constant controls \(\int\|V_z\|^2/\Omega\).
4. For \(h=P_0V_zF\), the combined row is
   \(Q=P_0[V_z'+V_z(D_q+\lambda_0)]\). Its exact coefficients at
   \(\pm r_l\) contain
   \(-2\nu d^2r_l^2\mp2\nu dr_lK_y/q\).
5. One power of \(r_l\) is paid by shear heat decay and one by exact scalar
   dissipation, giving \(\int|QF|\le3\Omega\sqrt M\).
6. The integrating factor \(g=e^{\lambda_0(x-A)}F_0\) satisfies
   \(\|g'\|_\infty\le e^{\lambda_0L}\eta\sqrt M\) and
   \(\|g''\|_1\le e^{\lambda_0L}\eta\sqrt M(3+C_\kappa\eta)\).
7. Between two scalar zeros,
   \(g'(\tau_k)=\ell_k^{-1}\int(s-\tau_{k-1})g''(s)\,ds\). Summing the
   disjoint gaps and multiplying by \(\|g'\|_\infty\) proves the squared
   slope bound.
8. The proof applies to every finite root subset. The extended nonnegative
   sum follows without a root-count or separation hypothesis.

No hidden second spectral moment, ECT determinant, inverse Jacobian, or
root-count factor was found.

## 3. Floor-cancellation audit

For \(K\) containing every counted root,

\[
\frac1{\mathcal R_Y(K)}
\sum_m\frac{|h_m|^2}{Y(t_m)}
=\sum_m|h_m|^2
\frac{\inf_KY}{Y(t_m)\sup_KY}
\le\frac{\sum_m|h_m|^2}{\sup_KY}.
\]

This distributes the single common \(1/\mathcal R_Y\) linearly; it does not
reuse the factor multiple times. Launch Parseval supplies
\(\sup_{K_t}Y\ge Y(\sigma_q)\gtrsim q^2E\), and launch data supplies
\(D\gtrsim q^2E\). The old amplitude optimizer and lattice inequalities then
give the stated \(M^{-2}\) endpoint.

The roots remain counted only on \(I_t\). Enlarging the root set to the
pre-observation layer would require
\(\sup_{x\ge0}\|V_z(x)\|\), a separate launch boundary analysis, and a new
statement.

## 4. Fixed-window retention boundary

The exact global heat shear

\[
u_{q,R}(t)=
(0,0,Ae^{-\nu(dRq)^2(t-\sigma_q)}\sin(dRq\,y))
\]

has \(L=0\), launch data of order \(A^2q^2R^2\), and observation retention
of order \(e^{-2\nu d^2R^2A_0}\). It proves that launch data alone cannot
force \(\sup_IY\gtrsim q^2E\) when \(I\) excludes launch.

This field has no nonzero target-root atom. The audit therefore records only
failure of automatic retention, not falsity of every fixed-window floor-free
atom inequality.

## 5. Literature boundary

Primary sources on scattered-zero Sobolev bounds, analytic semigroups,
Acquistapace--Terreni maximal regularity, Dyson--Phillips expansions, ECT
spaces, and NSE time analyticity were checked separately. None contains the
R0.71Z combined \(Q\)-row estimate or the all-root \(M^{-2}\) ledger.

Finite ECT cannot count an infinite Dyson target without finite closure or a
complex-tail zero-stability theorem. Bounded time dependence does not
automatically yield \(H_t^2\). These boundaries support the direct BV proof
and do not establish novelty or priority.

## 6. Release boundary

- Real, conjugate-symmetric shear is required.
- Launched carrier phases have unit modulus and distinct positive integer
  multipliers.
- The target heat generator is diagonal and the target is fixed.
- \(A_0>0\), \(q\ge\max(1,2|K_y|/d)\), and the physical observation window is
  fixed so \(e^{\lambda_0L}\) is uniform.
- The launch-inclusive theorem uses a mixed window: roots on \(I_t\), payment
  on \(K_t\).
- Strong coupling, \(A_0\to0\), non-unit/sparse phases, complex shear, and
  different geometry remain open.
- No universal endpoint, continuation criterion, finite-time singularity,
  global regularity, originality, or priority is claimed.
