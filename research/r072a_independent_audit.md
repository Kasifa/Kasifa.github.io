# R0.72A independent audit record

**Date:** 2026-08-27  
**Audited objects:** `r072a_report-source.md`, `r072a_gap_matrix.md`,
`r072a_exact_audit.py`, and the independent finite-lattice calculation.  
**Decision:** pass after the quantifier corrections recorded below.

## 1. Audit separation

Three analytic checks were performed independently:

1. a full re-derivation of the local-exposure BV estimate and its exponent
   ledger;
2. a domain/regularity check at exact launch \(A_0=0\);
3. a separate derivation of the frozen Bessel chain, growing-window error,
   root persistence, and logarithmic coefficient.

The numerical auditor imports neither the producer nor its result. The
producer uses complex DOP853 and Bessel-centered brackets. The independent
auditor uses the invariant real phase, fixed-step RK4, unseeded sign-change
discovery, and cubic Hermite interpolation.

## 2. Local-exposure theorem

Define

\[
 \ell_2(I)=\Omega^{-2}\int_I\|V(x)\|^2\,dx,
 \qquad
 q_I=(\Omega\sqrt M)^{-1}\int_I|QF|\,dx.
 \tag{2.1}
\]

The heat multiplier and the R0.71Z dissipation pairing give

\[
 0\le\ell_2(I)\le\min\{L,C_\kappa\},
 \qquad
 0\le q_I\le3.
 \tag{2.2}
\]

For \(g=e^{\lambda_0(x-A)}F_0\), direct differentiation gives

\[
 \|g'\|_\infty\le e^{\lambda_0L}\eta\sqrt M,
 \tag{2.3}
\]

and

\[
 \int_I|g''|
 \le e^{\lambda_0L}\eta\sqrt M
 \bigl(q_I+\eta\ell_2(I)\bigr).
 \tag{2.4}
\]

The complex BV zero lemma therefore yields

\[
 G_{\rm all}^{\rm ex}(I)
 \le e^{2\lambda_0L}M\Omega^2
 \bigl(1+q_I+\eta\ell_2(I)\bigr).
 \tag{2.5}
\]

No root-count, root-separation, largest-carrier, or inverse-\(A_0\) factor
appears.

After the existing amplitude optimization and lattice bounds, the normalized
power is

\[
 M^{-2}\eta^{4/3}(1+\eta L).
 \tag{2.6}
\]

For \(\eta=M^\alpha,L=M^{-\beta}\), its two exponent constraints are

\[
 \frac43\alpha-2<0,
 \qquad
 \frac73\alpha-\beta-2<0.
 \tag{2.7}
\]

They are exactly

\[
 \alpha<\min\left\{\frac32,\frac{6+3\beta}{7}\right\}.
 \tag{2.8}
\]

The equality lines are not converse statements.

## 3. Launch endpoint

For each fixed finite carrier set, every shift is bounded in the graph norm
of \(D_q\), while the finite-support launch belongs to every polynomially
weighted lattice space. Hence

\[
 F\in C([0,T];D(D_q))\cap C^1([0,T];\ell^2).
 \tag{3.1}
\]

More importantly, the uniform integrals remain valid from zero:

\[
 \int_0^\infty\mathcal E(x)\,dx\le M/2,
 \tag{3.2}
\]

\[
 \int_0^\infty A(x)^2\,dx
 \le\frac{\Omega_0^2}{4\kappa K_z^2},
 \qquad
 \int_0^\infty|QF|\,dx\le3\Omega_0\sqrt M,
 \tag{3.3}
\]

and

\[
 \int_0^\infty\|V(x)\|^2\,dx
 \le C_\kappa\Omega_0^2.
 \tag{3.4}
\]

Thus \(g'\) is absolutely continuous and \(g''\in L^1\) at launch. The BV
lemma may include the launch root.

The physical-window statement requires a specialization that was missing in
the first draft: observation must begin at the reference layer,
\(I_x=[A_0,A_0+L]\). Only then does \(A_0=0\) imply \(K_t=I_t\). The report
was corrected accordingly. Arbitrary \(\ell^2\) launch data and delayed
observation are not included in this endpoint statement.

## 4. Bessel family

For

\[
 D_r=-(r^2+1),
 \quad V_0=-i(T_1+T_{-1}),
 \quad W(0)=ie_{-1},
 \tag{4.1}
\]

the lattice Fourier transform and Jacobi--Anger identity give

\[
 W_r(\tau)=(-i)^rJ_{r+1}(2\tau),
 \qquad P_0W(\tau)=J_1(2\tau).
 \tag{4.2}
\]

The anti-linear symmetry

\[
 (\mathfrak CF)_r=(-1)^r\overline{F_r}
 \tag{4.3}
\]

is preserved by the exact evolution and fixes the launch vector, so the
target coordinate is exactly real.

For \(U_R(\tau)=F(\tau/R^4)\), contractive Duhamel comparison gives

\[
 \|U_R-W\|_{L^\infty(0,T;\ell^2)}
 \le R^{-4}\int_0^T
 \left(\|DW(s)\|+2s\right)\,ds.
 \tag{4.4}
\]

The exact Bessel moment identity is

\[
 \|DW(s)\|^2=6s^4+18s^2+4.
 \tag{4.5}
\]

The target row avoids the unbounded generator and gives the combined bound

\[
 \|P_0U_R-J_1(2\cdot)\|_{C^1([0,T])}
 \le C\frac{1+T^3}{R^4}.
 \tag{4.6}
\]

Taking \(T_R=j_{1,R}/2+\rho=O(R)\) makes the error \(O(R^{-1})\), whereas the
smallest limiting slope among the first \(R\) roots is \(\asymp R^{-1/2}\).
Each Bessel neighborhood therefore contains one selected simple exact root.
The report does not need to exclude every possible additional root, because
the complete nonnegative mass is at least the selected mass.

At a selected exact root, the scaled derivative equals \(h=P_0VF\). Thus

\[
 G_R^{\rm sel}
 =4\sum_{k=1}^RJ_0(j_{1,k})^2+O(R^{-1/2})
 =\frac8{\pi^2}\log R+O(1).
 \tag{4.7}
\]

The derivative in (4.7) is the rescaled \(\tau\)-derivative. The original
\(x\)-derivative is \(R^4\) times larger. R0.72A uses the normalized row
\(h\), consistently with R0.71Z.

## 5. Corrections required by the audit

The first report draft was changed in four places.

1. Section 5 now specializes to \(I_x=[A_0,A_0+L]\) before defining the
   launch-inclusive physical window.
2. Exact same-window cancellation is claimed only when observation begins at
   launch, \(A=A_0=0\).
3. The \(\Omega=0\) branch is removed before division by \(\Omega\) or
   \(K_v\); its charge is trivially zero.
4. The Bessel family is said not to establish normalized-ledger divergence,
   rather than being asserted not to diverge.

## 6. Numerical cross-audit

Both calculations passed every internal check. Their selected-mass values
agree as follows:

| \(R\) | producer mass | independent mass | absolute difference |
|---:|---:|---:|---:|
| 8 | 1.9302268777 | 1.9302268778 | \(1.42\times10^{-10}\) |
| 16 | 2.4677756563 | 2.4677756565 | \(2.04\times10^{-10}\) |
| 32 | 3.0126251861 | 3.0126251864 | \(2.57\times10^{-10}\) |
| 64 | 3.5652919858 | 3.5652919861 | \(2.89\times10^{-10}\) |

At \(R=64\), both are within \(7.27\times10^{-6}\) relative of the frozen
Bessel mass. Doubling the producer's \(R=32\) truncation radius changed no
reported root or mass at binary64 resolution. The layer lengths decrease
from \(2.7390\times10^{-2}\) at \(R=4\) to
\(6.0363\times10^{-6}\) at \(R=64\).

## 7. Final boundary

The audit certifies the local-exposure theorem, the finite-support launch
endpoint, and the exact selected-root Bessel lower family. It does not certify
a sharp \(1+\eta L\) upper loss, a growing-carrier normalized lower bound,
the full nonlinear rotational charge, a three-dimensional DNS, or any
Navier--Stokes regularity conclusion.
