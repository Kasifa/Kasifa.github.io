# R0.72C independent analytic audit

**Date:** 2026-08-27
**Scope:** line-by-line algebraic audit independent of the producer program.
No sampled or floating-point output is used as proof.

## 1. Assumptions and quantifiers

- \(\nu>0\), \(d\ge1\), \(K_z\ne0\), and
  \(q\ge\max(1,2|K_y|/d)\).
- The \(r_l\) are finitely many pairwise distinct positive integers.
- The physical coefficients \(w_l\) are complex and the two opposite shifts
  carry \(w_l\) and \(\overline{w_l}\).
- The coupling \(\delta\) is real.
- The launch vector has finite support and squared norm \(M\).
- \(I=[A,A+L]\subset[A_0,\infty)\).

The slope theorem is valid for every real \(\delta\). The target-row root-mass
theorem is stated only for \(\delta\ne0\), exactly where division by
\(\delta^2\) is legitimate.

## 2. The naive complex extension is invalid

For a one-carrier coefficient \(z=i\), the expression

\[
-iK_z z(T_1+T_{-1})=K_z(T_1+T_{-1})
\]

is self-adjoint, not skew-adjoint. On
\((e_0+e_1)/\sqrt2\), its quadratic form is \(K_z\). The energy derivative
can therefore be positive for sufficiently large \(\delta K_z\). Any argument
that merely replaces the real coefficients of R0.72B by complex coefficients
in the same shift sum is rejected.

## 3. Conjugate pairing restores the energy identity

The physical operator is

\[
(V_wF)_r=-iK_z\sum_l e^{-\kappa r_l^2x}
\left(w_lF_{r-r_l}+\overline{w_l}F_{r+r_l}\right).
\]

Under the discrete Fourier transform it is multiplication by

\[
-iK_z\sum_l e^{-\kappa r_l^2x}
\left(w_le^{ir_l\theta}+\overline{w_l}e^{-ir_l\theta}\right).
\]

The parenthesis is real, so the multiplier is purely imaginary and \(V_w\)
is skew-adjoint. Thus the dissipative energy identity used by the root ledger
survives arbitrary physical phases.

## 4. Target-row norm and heat contraction

The row \(P_0V_w(x)\) has the two coefficients
\(-iK_zw_le^{-\kappa r_l^2x}\) and
\(-iK_z\overline{w_l}e^{-\kappa r_l^2x}\). Hence

\[
\rho(x)^2
=2K_z^2\sum_l|w_l|^2e^{-2\kappa r_l^2x}.
\]

Every row norm is bounded by the operator norm, so
\(\rho_A\le\Omega_A\). The multiplier at time \(x\ge A_0\) is the torus heat
evolution of the multiplier at \(A_0\); \(L^\infty\) heat contraction gives

\[
\Omega_A=\sup_{x\ge A_0}\|V_w(x)\|=\|V_w(A_0)\|.
\]

No sign or phase condition enters either statement.

## 5. Mixed exposure and differentiated-row payment

Direct integration yields

\[
\int_{A_0}^{\infty}\rho(x)^2\,dx
\le \frac{\rho_A^2}{2\kappa}.
\]

Combining this with the inherited multiplier-square estimate gives

\[
\ell_\times(I)
=\frac{\int_I\rho\|V_w\|}
{\rho_A\Omega_A}
\le\min\{L,C_\times\},
\qquad
C_\times=\frac{\pi}{\sqrt2\,45^{1/4}\kappa}.
\]

The two entries of
\(Q=P_0[V_w'+V_w(D_q+\lambda_0)]\) have the same moduli as in the real
coefficient calculation. The dissipation-paired estimate therefore remains

\[
\int_{A_0}^{\infty}|QF|\,dx\le3\rho_A\sqrt M,
\qquad q_\rho(I)\le3.
\]

## 6. Complete root sum and the \(\delta=0\) branch

For \(g=e^{\lambda_0(x-A)}F_0\),

\[
\|g'\|_\infty
\le e^{\lambda_0L}|\delta|\rho_A\sqrt M,
\]

\[
\int_I|g''|
\le e^{\lambda_0L}|\delta|\rho_A\sqrt M
\left(q_\rho+\eta\ell_\times\right).
\]

The bounded-variation zero-sampling lemma gives

\[
\sum_{F_0(\tau)=0}|F_0'(\tau)|^2
\le e^{2\lambda_0L}\delta^2M\rho_A^2
\left(1+q_\rho+\eta\ell_\times\right)
\]

for every finite root subset and then for the complete extended nonnegative
sum. At a root \(F_0'=\delta P_0V_wF\). Only when \(\delta\ne0\) may this
identity be divided by \(\delta^2\), producing

\[
G_{\rm all}^{\rm ex}
=\sum_{F_0(\tau)=0}|P_0V_w(\tau)F(\tau)|^2.
\]

If \(\delta=0\), the slope bound still holds but no target-row estimate is
inferred by division.

## 7. Degenerate carrier branch

If \(\rho_A=0\), every positive heat weight forces \(w_l=0\). Hence
\(V_w=Q=0\), \(\Omega_A=\eta=0\), and both complete sums vanish. Setting
\(q_\rho=\ell_\times=\chi_A=0\) on this branch makes the statement
self-contained without a zero quotient. All normalized estimates assume a
nonzero carrier profile.

## 8. Joint phase inequality

For the nondegenerate branch,

\[
\chi_A\left(\frac{\Omega_A^2}{K_v}\right)^{1/3}
=\frac{\rho_A^2}{\Omega_A^{4/3}K_v^{1/3}}
\le\left(\frac{\rho_A^2}{K_v}\right)^{1/3},
\]

because \(\Omega_A\ge\rho_A\). Estimating \(\chi_A\) and
\(\Omega_A^2/K_v\) separately would discard this compensation and is not a
valid route to the sharp phase-uniform exponent.

## 9. Uniform heat-participation power

Assume
\(c_-a_M\le|w_l|\le c_+a_M\). After sorting the distinct positive
carriers, \(r_{(j)}\ge j\), so

\[
K_s\ge S_M\ge M^3/3,\qquad
K_v\ge c_-^2a_M^2K_s,
\]

\[
\rho_A^2\le2K_z^2c_+^2a_M^2
H_M(A_0),\qquad
H_M(A_0)=\sum_{j=1}^Me^{-2\kappa A_0j^2}.
\]

Substitution into the joint inequality gives

\[
\Phi_{A,M}
\le C(K_z,c_+/c_-)M^{-3}H_M(A_0)^{1/3}.
\]

At \(A_0=0\), \(H_M=M\), yielding \(M^{-8/3}\). If
\(A_0=A=A_*>0\) is fixed, the heat sum is uniformly bounded and the power is
\(M^{-3}\).

## 10. Burn-in transition

With \(t_M=\kappa A_{0,M}\):

- \(t_MM^2\to0\) gives \(H_M=M(1+o(1))\);
- \(t_MM^2\to c\in(0,\infty)\) gives a Riemann-sum multiple of \(M\);
- \(t_MM^2\to\infty\) and \(t_M\to0\) gives
  \(H_M\sim\sqrt\pi/(2\sqrt{2t_M})\);
- \(t_M\to t_*>0\) gives a finite positive theta sum;
- \(t_M\to\infty\) gives
  \(H_M=e^{-2t_M}[1+O(e^{-6t_M})]\).

Consequently, for \(A_{0,M}\asymp M^{-\sigma}\),
\[
p_\sigma=3-\sigma/6\quad(0<\sigma<2),\qquad
p_\sigma=8/3\quad(\sigma\ge2).
\]

## 11. Phase-region algebra

If \(\eta=M^\alpha\), \(L=M^{-\beta}\), and
\(\Phi=O(M^{-p})\), the two ledger terms vanish under

\[
\alpha<\min\left\{\frac{3p}{4},
\frac{3p+3\beta}{7}\right\}.
\]

Substitution gives

\[
\alpha<\min\left\{2,\frac{8+3\beta}{7}\right\}
\]

at exact launch with arbitrary phases, and

\[
\alpha<\min\left\{\frac94,\frac{9+3\beta}{7}\right\}
\]

after a fixed positive restart. These are sufficient regions; equality and
the exterior are not converses.

## 12. Rudin--Shapiro sharpness

For \(M=2^n\) with odd \(n\), the Rudin--Shapiro recursion has

\[
|P_n(z)|^2+|Q_n(z)|^2=2M\quad(|z|=1),
\qquad P_n(1)=\sqrt{2M}.
\]

For the corresponding sign carriers, the real shear multiplier attains the
upper bound at \(\theta=0\). Therefore

\[
\Omega_0=2|K_z|a_M\sqrt{2M},\qquad
\rho_0^2=2K_z^2a_M^2M,\qquad
\chi_0=\frac14,
\]

and

\[
\Phi_{0,M}
=\frac{|K_z|^{2/3}}2
\left(\frac{M}{S_M}\right)^{4/3}
\asymp M^{-8/3}.
\]

Thus a phase-uniform \(M^{-10/3}\) bound is false, and the
\(-8/3\) upper-prefactor exponent is sharp along this subsequence.

## 13. Fixed-positive sharpness

Take \(A_0=A=A_*>0\), \(r_l=l\), and \(w_l=a_M>0\). The heat sums
\[
H_{t,M}=\sum_{l=1}^Me^{-tl^2},\qquad
J_{t,M}=\sum_{l=1}^Me^{-2tl^2},
\quad t=\kappa A_*
\]
converge to finite positive limits. Direct substitution gives
\[
\Phi_{A,M}
=2^{-1/3}|K_z|^{2/3}
\frac{M J_{t,M}}{S_M^{4/3}H_{t,M}^{4/3}}
\asymp M^{-3}.
\]

## 14. Fixed effective coupling versus fixed raw coupling

The phase diagram compares families at fixed
\(\eta=|\delta|\Omega_A\). At fixed raw \(\delta\),

\[
\eta^{4/3}\Phi_{A,M}
=|\delta|^{4/3}\frac{M}{K_s}
\frac{\rho_A^2}{K_v^{1/3}}.
\]

For fixed moduli, the leading displayed factor is phase-independent.
The exposure bracket can still depend on phase through \(q_\rho\) and
\(\eta\ell_\times\); this distinction is retained in the report.

## 15. Burn-in and scope boundary

A theorem after \(A_*>0\) estimates only the restarted tail. The full
nonnegative ledger decomposes as

\[
G_{\rm all}^{\rm ex}([0,A_*+L])
=G_{\rm pre}^{\rm ex}([0,A_*])
+G_{\rm tail}^{\rm ex}((A_*,A_*+L]).
\]

No terminal decay can subtract the pre-ledger. The Rudin--Shapiro and
same-sign families establish sharpness only for the algebraic coefficient in
an upper bound. They do not establish a lower bound for actual root mass,
normalized ledger saturation, a finite-time singularity, or a continuation
criterion for general three-dimensional Navier--Stokes solutions.

## Audit conclusion

The conjugate-paired phase extension, complete-root slope estimate, target-row
ledger for \(\delta\ne0\), joint phase inequality, heat-transition powers,
phase regions, and the two sharp algebraic families are mutually consistent
under the stated hypotheses. No algebraic basis was found for extending the
coherent \(M^{-10/3}\) exponent uniformly over phases or for using positive
burn-in to erase launch-time exposure.
