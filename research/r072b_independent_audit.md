# R0.72B independent analytic audit

**Date:** 2026-08-27
**Scope:** line-by-line algebraic audit independent of the producer certificate.
No numerical output is used as proof.

## 1. Assumption audit

- \(r_l\) are finitely many distinct positive integers.
- \(z_l\in\mathbb R\), so \(V_z(x)\) is skew-adjoint.
- \(K_z\ne0\), \(\kappa=\nu d^2>0\).
- \(q\ge\max(1,2|K_y|/d)\), exactly the hypothesis used in the
  explicit \(Q\)-row bound.
- The launch vector has finite support and squared norm \(M\).
- The counted interval \(I=[A,A+L]\) lies in \([A_0,\infty)\).

No same-sign or amplitude-comparability assumption enters the main theorem.
Those assumptions first enter the coherent corollary.

## 2. Row norm

The row \(P_0V_z(x)\) has coefficients
\(-iK_zz_le^{-\kappa r_l^2x}\) at each of the two distinct inputs
\(r_l\) and \(-r_l\). Therefore its squared Euclidean row norm is

\[
2K_z^2\sum_l|z_l|^2e^{-2\kappa r_l^2x}=\rho(x)^2.
\]

The multiplier norm dominates every row norm, so \(\rho_A\le\Omega\).
The squared row norm is nonincreasing in \(x\).

## 3. Mixed exposure constant

Direct integration gives

\[
\int_{A_0}^\infty\rho^2
=\frac{K_z^2}{\kappa}
\sum_l\frac{|z_l|^2e^{-2\kappa r_l^2A_0}}{r_l^2}
\le\frac{\rho_A^2}{2\kappa}.
\]

The inherited multiplier estimate is

\[
\int_{A_0}^\infty\|V_z(x)\|^2dx
\le C_\kappa\Omega^2.
\]

Cauchy--Schwarz gives

\[
\int\rho\|V_z\|
\le\rho_A\Omega\sqrt{C_\kappa/(2\kappa)}.
\]

The local pointwise estimate is at most \(L\rho_A\Omega\). Thus
\(C_\times=\sqrt{C_\kappa/(2\kappa)}\) is valid. Dimensional audit:
\(C_\kappa\) and \(1/\kappa\) both have time dimension, so \(C_\times\)
also has time dimension.

## 4. \(Q\)-payment constant

The inherited pointwise estimate is

\[
|QF|\le6\sqrt{2\nu}d|K_z|A\mathcal E^{1/2}.
\]

The two integrals are

\[
\int A^2=\rho_A^2/(4\kappa K_z^2),
\qquad
\int\mathcal E\le M/2.
\]

Their product gives

\[
6\sqrt{2\nu}d|K_z|
\frac{\rho_A}{2\sqrt\kappa|K_z|}
\sqrt{\frac M2}=3\rho_A\sqrt M,
\]

because \(\sqrt\kappa=\sqrt\nu d\). The constant 3 is exact at the
level of this estimate.

## 5. BV root sum

For \(g=e^{\lambda_0(x-A)}F_0\),

\[
\|g'\|_\infty\le e^{\lambda_0L}|\delta|\rho_A\sqrt M,
\]

\[
\int_I|g''|
\le e^{\lambda_0L}|\delta|\rho_A\sqrt M
\bigl[q_\rho+\eta\ell_\times\bigr].
\]

The first zero contributes one copy of the squared sup norm. The remaining
zeros contribute the product of the sup norm and the \(L^1\) derivative
variation. This yields exactly

\[
e^{2\lambda_0L}\delta^2M\rho_A^2
[1+q_\rho+\eta\ell_\times].
\]

The bound is uniform over every finite root subset. The monotone supremum over
finite subsets is therefore legitimate even if the full zero set is not first
shown to be finite or countable.

## 6. Degenerate branch

\(\rho_A=0\) implies every \(z_l=0\), because \(K_z\ne0\) and every heat
weight is strictly positive. Hence \(V_z=0\), \(\Omega=0\), and the root
slope measure is zero. No division by \(\rho_A\Omega\) is made on this
branch.

## 7. Normalized optimizer

The only change to the R0.72A pre-optimization estimate is
\(M\Omega^2\mapsto M\rho_A^2\). Factoring
\(\rho_A^2=\chi_A\Omega^2\) shows that the scalar amplitude function is
unchanged. Its maximum remains at

\[
u=S^2K_s/(P^2K_v)=3.
\]

Thus the normalized theorem acquires exactly one factor \(\chi_A\), with no
change to the \(\eta^{4/3}\) power.

## 8. Coherent asymptotics

At exact launch with same-sign amplitudes,

\[
\Omega=2|K_z|\sum_l|z_l|,
\qquad
\chi_0=\frac12\frac{\sum_l|z_l|^2}{(\sum_l|z_l|)^2}.
\]

Comparable amplitudes give \(\chi_0=O(M^{-1})\). Distinct positive integer
carriers and comparable amplitudes give

\[
M/K_s=O(M^{-2}),\qquad
\Omega^2/K_v=O(M^{-1}).
\]

The product is \(M^{-2}M^{-1}M^{-1/3}=M^{-10/3}\). Power counting gives

\[
-10/3+4\alpha/3<0\iff\alpha<5/2,
\]

\[
-10/3+7\alpha/3-\beta<0
\iff\alpha<(10+3\beta)/7.
\]

The equality lines are not converses.

## 9. Enhanced-dissipation logic

The Duhamel difference between changing and frozen propagators is bounded by
the coupling-weighted profile change \(\Xi_A\), not only by
\(L\kappa r_{\max}^2\). Any decay estimate obtained after a burn-in time
can multiply the restarted tail bound through \(E_a\). Since the full root
ledger is nonnegative and additive over disjoint time intervals, it cannot
remove the pre-burn-in contribution.

The one-carrier Bessel family confirms the distinction: its root mass grows
like \(\log R\) on a window with
\(L_R\Gamma_R^{\rm fr}\to0\), \(\Xi_R\to0\), and vanishing energy loss.

## 10. Documentation correction

The R0.72A independent finite evolution is fixed-step classical RK4. The
phrase “exponential midpoint” in the earlier report is a documentation error;
the code and archived configuration agree on RK4.

## Audit conclusion

The target-row mixed-exposure theorem, coherent \(M^{-10/3}\) corollary,
phase boundary, and burn-in/tail distinction are algebraically consistent
under the stated assumptions. The audit found no basis for extending the
coherent \(M^{-1}\) participation factor to arbitrary fixed \(A_0>0\), or
for claiming a nonautonomous enhanced-dissipation theorem for the changing
many-frequency profile.
