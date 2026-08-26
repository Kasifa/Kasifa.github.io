# R0.71T independent audit

**Audit boundary:** finite Fourier algebra, the resonant precompensation
normal form, simple-entry and outgoing-coarea identities, the complete
variable-denominator trace ledger, and the two-parameter scaling exponents.

The exact producer `research/r071t_exact_audit.py` uses SymPy rational and
symbolic algebra.  The checker `research/r071t_independent_audit.py` imports
neither that producer nor its output.  It reconstructs the seed with a
standalone NumPy FFT, evaluates the coarea integrals with SciPy adaptive
quadrature, checks the trace identity by direct numerical integration,
checks the resonant slope by centered finite differences, and reconstructs
the scaling table in floating point.

The fixed-time nonlinear NSE implicit-function theorem is an analytic part of
the report.  Neither finite script is presented as a numerical proof of that
theorem.

## 1. Exact producer

The exact certificate contains eight passing checks.

1. **Fourier seed.**  It reconstructs the four \(|k|^2=2\) target modes of
   \(F_*\) and proves

   \[
   Y_*=1,
   \quad \|F_*\|_2^2=\frac14,
   \quad \|\operatorname{curl}F_*\|_2^2=\frac12,
   \quad \|C_t\|_2^2=1,
   \quad \langle F_*,C_t\rangle=\frac12,
   \quad A_+=\frac14.
   \]

2. **Resonant precompensation.**  The leading target-shell equation

   \[
   x_t=-2\nu x+a^2e^{-2\nu t}F_0,
   \qquad x(0)=-a^2\tau F_0
   \]

   has

   \[
   x(t)=a^2F_0(t-\tau)e^{-2\nu t},
   \quad x(\tau)=0,
   \quad x_t(\tau)=a^2e^{-2\nu\tau}F_0.
   \]

3. **Simple face and slope charge.**  On the single target radius
   \(\rho^2=2\), the producer proves \(A_+=1/4\), \(A_-=0\), and exact
   equality between the weighted atom and the normalized slope square.

4. **Outgoing coarea.**  With
   \(\rho(s)=6s(1-s)\mathbf1_{(0,1)}\), every model radius
   \(r(t)=t^m\), \(1\le m\le8\), has unit outgoing mass.  Even orders have
   zero signed face but still have unit outgoing face.

5. **Symmetric trace kernel.**  The triangular-kernel identity has zero
   symbolic residual on every monomial of degree zero through eight.

6. **Variable denominator.**  For \(g=e^{bt}\) and \(Y=e^{2bt}\), the
   normalized scalar \(f=g/\sqrt Y\) is exactly constant.  The producer
   verifies that the \(g_t\) and \(Y_t/(2Y)\) terms cancel exactly.

7. **Double scaling.**  With \(a_\lambda=\lambda^{-2}\), the leading atom,
   bare budget, and ratio are exactly

   \[
   \frac{e^{-2\nu\tau}}{4\lambda^4},
   \qquad
   \frac{1-e^{-4\nu\tau}}{16\nu\lambda^6},
   \qquad
   \frac{2\nu}{\sinh(2\nu\tau)}\lambda^2.
   \]

8. **Scale table.**  The entry atom has scale exponent zero, the bare time
   integral exponent \(-2\), and each proposed scale-matched strong or
   occupation density exponent \(+2\) before time integration.

## 2. Independent numerical reconstruction

The independent certificate contains six passing groups.

- A \(32^3\) FFT reconstructs the four target modes.  The divergence,
  target-vorticity, norm, pairing, and face residuals are all exactly zero in
  the recorded floating-point run.
- Twelve resonant-normal-form tests cover
  \(\nu\in\{0.3,1,2.1\}\), \(a\in\{0.07,0.2\}\), and
  \(\tau\in\{0.01,0.08\}\).  The largest centered-difference residual is
  \(1.173\times10^{-13}\).
- Adaptive quadrature checks orders \(1\) through \(8\) at
  \(\delta\in\{0.2,0.03,0.004\}\).  The largest unit-mass residual is
  \(6.661\times10^{-16}\).
- One nontrivial degree-five polynomial is reconstructed at four window
  heights.  The largest trace residual is \(1.110\times10^{-16}\).
- Twelve exponential denominator tests cover four growth rates and three
  times.  The largest cancellation residual, including the normalized value,
  is \(2.220\times10^{-16}\).
- The double-scaling ledger is reconstructed for
  \(\lambda=1,2,\ldots,128\) at \(\nu=1\), \(\tau=0.05\).  The ratio divided
  by \(\lambda^2\) is
  \(19.9667055145922\) throughout; the largest relative residual is
  \(3.559\times10^{-16}\).

## 3. Independence boundary

The two scripts use different arithmetic and reconstruction paths:

| Object | Exact producer | Independent checker |
|---|---|---|
| Fourier seed | sparse rational Fourier convolution | physical-grid FFT and spectral projection |
| precompensation | symbolic ODE solution | direct formula and finite-difference slope |
| coarea | exact polynomial integration | adaptive floating-point quadrature |
| trace identity | symbolic monomial basis | numerical nontrivial polynomial |
| denominator | symbolic simplification | direct exponential evaluation |
| scaling | symbolic exponents and coefficients | explicit frequency sweep |

Agreement therefore checks the finite algebra against implementation mistakes
in either one path.  It does not certify the standard local flow-map theorem,
the IFT remainder estimate, an infinite family of entries, or a Leray-level
occupation bound.

## 4. Result boundary

The audited finite statements support the R0.71T proof, but the hierarchy of
evidence remains explicit.

1. The Fourier, coarea, trace, denominator, and scaling statements are exact
   finite identities.
2. The resonant equation is the quadratic normal form of the NSE target
   shell; the exact nonlinear zero comes from the analytic IFT proof.
3. The independent finite-Galerkin figure, when present, is corroborative
   time stepping and root shooting, not direct numerical simulation of the
   continuum theorem.
4. No certificate proves recurrence packing, a continuation criterion,
   singularity, or global regularity.
