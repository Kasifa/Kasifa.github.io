# R0.71Y independent audit record

**Date:** 2026-08-26  
**Decision:** PASS for the selected-root operator-sampling theorem after the
corrections and scope reductions listed below.

## 1. Audited statement

The audited claim belongs to the real-shear, fixed-target, triangular
Fourier-lattice architecture of R0.71W. Let \(M=2N+1\) launched carrier
phases have unit modulus and distinct positive integer multipliers. Let the
persistent background be matched to the full growing-dimensional cost

\[
 E_N=S^2K_{s,N}+P^2K_{v,N}.
\]

For any selected \(N\) exact target roots in a layer \(x\ge A_0>0\), define

\[
 \delta_{\mathrm{obs},N}
 =\frac P{q^2}\sup_{x\ge A_0}
 \|V_{z_N}(x)\|_{\ell^2\to\ell^2}.
\]

Then

\[
 \frac{\mathcal J_N^{\rm sel}}
 {D_N^{1/3}\Lambda_1(I;u_N)}
 \le C\nu^{-2}
 \frac{\delta_{\mathrm{obs},N}^{4/3}}N.
\]

The result is exact at finite \(q\). It is not a first-Dyson approximation.
It controls the selected roots, not an unproved complete growing-dimensional
root set.

## 2. Analytic proof audit

The proof chain received independent line-by-line review.

1. \(D_q\) is self-adjoint nonpositive and, for real shear coefficients,
   \(V_z\) is skew-adjoint. Hence the active scalar is exactly
   \(\ell^2\)-contractive.
2. At an exact target root, the diagonal heat coordinate is zero, so the
   physical target slope is exactly \(SP\,P_0V_zF\).
3. The exact sampled-slope mass is at most
   \(NM\Omega_N^2\), with no ECT or inverse-Jacobian constant.
4. The scalar/shear amplitude optimization is attained at
   \(S^2K_s/(P^2K_v)=3\) and contributes \(3/4^{4/3}\).
5. Fourier multiplier and weighted Cauchy estimates give
   \(\Omega_N^2/K_{v,N}\le2\pi^2K_z^2/3\).
6. The integer lattice gives
   \(K_{s,N}\ge\sum_{j=1}^{2N+1}j^2\) and
   \(NM/K_{s,N}\le3/(4N)\).
7. The complete factor satisfies \(\Lambda_1\ge\nu^2\); the full-frequency
   rotational charge is retained and can only increase the denominator.

No fatal algebraic or normalization error was found.

## 3. Required corrections to the inherited route matrix

Two R0.71X statements required correction.

First, because the operator supremum starts at \(A_0>0\), its Fourier lower
bound is heat weighted:

\[
 \Omega_N\ge c
 \left(\sum_l|z_l|^2e^{-2\nu d^2r_l^2A_0}\right)^{1/2}.
\]

There is no dimension-independent lower bound by the unweighted
\(\|z\|_2\). The single mode \(r=R,z_R=1\) disproves it.

Second, observation-layer coupling is not the complete IFT parameter. A
launch-to-root Dyson certificate also sees

\[
 \eta_{\mathrm{Dyson},N}
 =\frac P{q^2}\int_0^{\tau_N}\|V_z(x)\|\,dx
\]

and a quantitative IFT additionally pays inverse-Jacobian and derivative-
Lipschitz constants. For fixed \(A_0>0\), the audited one-way estimate

\[
 \delta_{\mathrm{obs},N}
 \le C_{A_0,\nu,d}\eta_{\mathrm{Dyson},N}
\]

is valid. The reverse comparison fails. These repairs affect the open-route
diagnostic, not the R0.71X fixed-dimensional endpoint theorem.

## 4. Exact separated-root enhancement

For minimum scaled root gap \(h_N>0\), \(b=2\nu d^2\), and

\[
 W_N^2=\sum_l|z_l|^2e^{-br_l^2A_0},
\]

the independently audited finite-\(q\) estimate is

\[
 G_N^{\rm ex}
 \le\frac{2|K_z|^2M}{bh_N}W_N^2.
\]

It implies

\[
 \frac{\mathcal J_N^{\rm sel}}
 {D_N^{1/3}\Lambda_1}
 \le C\frac{\delta_{\mathrm{obs},N}^{4/3}}{h_NN^2}.
\]

The pre-gap weighted-kernel form remains valid when \(\tau_1=A_0\); only
the \(h_N^{-1}\) corollary degenerates.

## 5. Equal-grid conditioning audit

For \(\tau_m=mh\) and \(x_l=e^{-bhr_l^2}\), the response block factors
exactly as cumulative-sum times Vandermonde times diagonal. Its determinant
therefore yields

\[
 \|\mathsf M^{-1}\|_2
 \ge h^{-1}(bh\,r_{\max}^2)^{-(N-1)/2}.
\]

For canonical \(r_l=l\), any small-coupling nonvanishing attempt forced into
\(hN^2\to0\) has rapidly growing inverse lower bound. The audit preserves the
essential limitation: inverse growth is not, by itself, an upper bound on the
largest true nonlinear IFT branch.

## 6. High-precision producer

The standard-library Decimal producer passes 13 of 13 checks. Principal
diagnostics are:

- optimizer \(u_*=3\), value \(0.4724703937105774\);
- \(\Omega^2/K_v\) upper constant \(6.579736267392906\) for \(K_z=1\);
- lattice-factor fitted power \(-0.99998617\);
- fixed observation-coupling envelope power \(-0.99998617\);
- critical \(\delta_{\rm obs}=N^{3/4}\) power \(1.38\times10^{-5}\);
- subcritical \(\delta_{\rm obs}=N^{1/2}\) power \(-0.33331951\);
- fixed-gap separated power \(-1.99998617\);
- quasi-uniform-gap separated power \(-0.99998617\); and
- equal-grid inverse lower bound
  \(\log_{10}\ge49.03\) at \(N=64,h=N^{-3}\).

The single-mode correction reaches a heat-weighted/unweighted ratio
\(3.45\times10^{-29}\) at \(r=32\).

## 7. Independent finite-matrix reconstruction

The independent NumPy/SciPy program imports neither the producer nor its
JSON and passes 12 of 12 checks. It obtains:

- zero skew-adjointness defect in every audited finite shift matrix;
- maximum root-coordinate slope/bound ratio \(0.05073\);
- maximum finite semigroup norm ratio \(0.64195\);
- maximum multiplier/l1-bound ratio \(0.78252\);
- maximum optimized-envelope ratio \(0.91797\);
- maximum separated sampled-slope/bound ratio \(0.002563\);
- equal-grid determinant factorization agreement within the declared
  binary64 tolerance; and
- minimum inverse-norm/lower-bound ratio \(14.31\).

These are finite algebraic corroborations, not DNS and not an exact-root
construction.

## 8. Literature boundary

The bounded primary-source review confirms that ECT/total positivity supplies
qualitative finite-dimensional nondegeneracy, while positive-real
Vandermonde, exponential-sum, and biorthogonal-family estimates can deteriorate
with dimension, gap, and observation time. Quantitative IFT sources supply
sufficient certified radii, not maximal true radii. No checked source proves
the R0.71Y NSE theorem or an all-root count.

## 9. Release boundary

The following limitations are mandatory.

- Real, conjugate-symmetric shear is required for skew-adjointness.
- The \(N^{-1}\) corollary uses the existing unit-modulus launched phases.
- The background must match the full \(K_s,K_v\) cost.
- The theorem controls selected roots. For \(M\) carriers and \(R\) sampled
  roots, the general bound is \(O(R\delta_{\rm obs}^{4/3}/M^2)\); no
  growing-dimensional no-spurious-root theorem is proved.
- The fixed-\(A_0\) Dyson comparison degenerates if \(A_{0,N}\to0\).
- Floor-free, sparse/weighted-phase, strong-observation-coupling, quadratic
  extra-root proliferation, and different-geometry routes remain open.
- The result proves no universal endpoint estimate, singularity, continuation
  criterion, global regularity, novelty, or priority.
