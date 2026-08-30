# R0.73H adversarial audit

**Date:** 2026-08-30  
**Object:** `r073h_harmonic_energy_proof.md` and
`r073h_harmonic_derivation.md`  
**Method:** test the strongest conclusion against the most likely hidden
failures before publication

## 1. Could the backward estimate have been used in the wrong direction?

No.  The proof does not invert an operator-norm lower bound.  The selected
initial vector lies in the moving unstable fiber, its image stays in that
fiber, and R0.73F bounds the inverse evolution from the endpoint back to
every intermediate time.  Dividing that orbit by its actual endpoint norm
gives

\[
 \|a(s)\|_2\le K_{\rm F}e^{-r\Lambda(D-s)}.
\]

This is the exact localization used later.

## 2. Could the nonlinear coefficient be off by a factor of \(\Lambda\)?

No.  R0.73H keeps physical velocity amplitude and changes only time from
\(t\) to \(d=4t\).  Therefore

\[
 \mathcal B(f,g)=-\frac14\mathbb P[(f\cdot\nabla)g].
\]

In fast time \(\theta=\Lambda d\), the coefficient becomes
\(\varepsilon_\nu/4\).  The launch amplitude is separately named \(\rho\)
in the finite expansion.  No step uses the rescaled-amplitude equation from
R0.73G as though it were the physical equation.

## 3. Is the \(K_z=\pm2\) energy bound only a finite-matrix observation?

No.  The \(|m|\le4\) exact rational block is combined with an analytic
\(|m|\ge5\) diagonal bound and a cross-block operator-norm bound.  The
resulting two-block quadratic form proves

\[
 -\partial_x^2+1-\frac94W_x(0,x)^2\ge\frac1{20}I
\]

on the full periodic space.  The explicit time perturbation leaves
\(1/40\) at \(d\le1/450\).  The finite block is a subcertificate, not a
Galerkin limit argument.

## 4. Could a hidden constant mode invalidate the homogeneous
Ladyzhenskaya inequality?

No.  The carrier has nonzero \(K_z\).  Bilinear terms are divergences of
periodic tensors.  Both linearized background terms also have zero spatial
average.  The mean row generated at second order is a zero-mean tangential
shear.  Thus \(a,b,c\), the exact perturbation, the approximate solution,
and the error all retain zero total mean.

## 5. Does the proof secretly require a uniform \(H^s\) semigroup?

No.  It uses pointwise \(L^2\) localization only for the selected linear
orbit.  Gradient information appears solely as cumulative dissipation.
Ladyzhenskaya and Stieltjes product measures propagate this pair of
quantities through the quadratic, cubic, and remainder equations.  No
pointwise \(H^1\), uniform \(H^3\), or high-frequency semigroup estimate is
inserted.

## 6. Can the generated doubled row grow too quickly?

The universal numerical-abscissa \(1/2\) would be too large for the
quadratic rate budget.  R0.73H does not use it there.  The continuum
doubled-row estimate \(1/3<2r\) is exactly the additional strict margin.
The cubic and fourth-order steps use \(1/2<3r\) and \(1/2<4r\).

## 7. Is the fourth-order error estimate missing a transport term?

No.  The terms

\[
 \langle\mathcal B(u_{\rm app},e),e\rangle,
 \qquad
 \langle\mathcal B(e,e),e\rangle
\]

cancel.  The remaining term is controlled by
\(\|\nabla u_{\rm app}\|_2^2\|e\|_2^2\), whose time integral is
\(O(\delta^2)\).  The proof explicitly includes this extra integrating
factor and separately controls the cumulative error dissipation.  The
residual sign is fixed by defining

\[
 R_{\rm app}=\mathcal L u_{\rm app}
 +\mathcal B(u_{\rm app},u_{\rm app})-\partial_du_{\rm app}.
\]

## 8. Could the quadratic term contaminate the target lower bound?

No.  Exact Fourier parity places \(b\) in \(K_z=0,\pm2\).  Therefore
\(\Pi_{\pm1}b=0\).  The target estimate contains the unit linear endpoint,
the uniformly bounded cubic coefficient, and the fourth-order error only.

## 9. Does the theorem identify the sharp initial scale?

No.  The seed is \(\delta/G_\Lambda\).  R0.73F gives a lower bound on
\(G_\Lambda\), but R0.73H does not prove
\(G_\Lambda\asymp e^{r\Lambda D}\).  It would be invalid to replace the
actual-gain normalization with the prescribed seed
\(\delta e^{-r\Lambda D}\) without a new matching estimate.

## 10. Is this Lyapunov instability of one background?

No.  The background amplitude and launch both vary with \(\Lambda\).  The
result is a family-level fixed-distance departure.  A fixed-background
Lyapunov sequence remains open.

## 11. Does the result enter the three-dimensional singularity mechanism?

No.  The selected real launch stays in an exact planar invariant subspace.
Each orbit is globally smooth by two-dimensional Navier--Stokes theory.
There is no transverse \(K_x\ne0\) row, no nonzero first velocity component,
and no three-dimensional vortex stretching.  The result does not resolve
the Clay problem.

## 12. Can the finite cubic sign be promoted to a theorem?

No.  The finite diagnostic records Duhamel coefficients, path phases,
cutoff agreement, and an independent FFT comparison.  Its endpoint
\(d=0.01\) is not identified with the existential analytic \(D\); it has
no Fourier-tail enclosure and no fourth-or-higher coefficient control.
Any observed negative signed cubic feedback is a finite profile diagnostic,
not a continuum saturation theorem.

## Verdict

No adversarial test above invalidates the gain-normalized planar departure
theorem.  Publication remains conditional on the exact certificate,
independent analytic audit, finite-package gates, figure QA, and release
transaction all passing.  The strongest permitted statement is the one in
the proof: varying-background, planar, gain-normalized, fixed-distance
nonlinear departure with globally smooth selected orbits.
