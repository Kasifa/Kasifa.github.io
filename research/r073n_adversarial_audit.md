# R0.73N adversarial audit

**Audit date:** 2026-08-31

**Objects:** r073n_fixed_background_no_go_proof.md and
r073n_scaling_obstruction.md

**Verdict:** **PASS**

The independent second-pass analytic audit closed the continuum estimates,
quantifiers, topology labels, and transformation ledger.  Finite and
publication gates remain separate.

## 1. Could the relative-energy exponent be off by a factor of two?

No.  The exact identity is

\[
 {1\over2}{d\over dt}\|w\|_2^2+\|\nabla w\|_2^2
 =-\int(\partial_yF_\Lambda)w_2w_3.
\]

Since \(2|w_2w_3|\le |w|^2\),

\[
 {d\over dt}\|w\|_2^2
 \le\|\partial_yF_\Lambda\|_\infty\|w\|_2^2.
\]

Passing from the squared norm to the norm contributes the required factor
\(1/2\).  Because

\[
 \|\partial_yF_\Lambda(t)\|_\infty
 \le2\Lambda(e^{-4t}+e^{-16t}),
\]

the norm exponent is exactly bounded by \(\Lambda j(T)\), not
\(2\Lambda j(T)\).

## 2. Is the all-time \(L^2\) statement using a nonexistent 3D solution?

No after correction.  For arbitrary three-dimensional data, the estimate is
stated only on the common strong lifespan:

\[
 \sup_{0\le t<T_{\max}}\|w(t)\|_2
 \le e^{5\Lambda/16}\|w(0)\|_2.
\]

It becomes an all-time statement either in the invariant planar subsystem,
where two-dimensional regularity is global, or inside the separately proved
three-dimensional \(H^3\) tube.  Weak-solution existence is not used.

## 3. Does the planar theorem secretly assume \(H^3\) smallness?

No after correction.  The planar comparison datum must belong to
\(H^3_{\rm pl}\) so that it is a strong datum, but the smallness hypothesis
is only

\[
 \|w(0)\|_2<\epsilon e^{-5\Lambda/16}.
\]

Global two-dimensional continuation then makes this a synchronized
\((H^3_{\rm pl},L^2_{\rm pl})\) statement with genuine \(L^2\) initial
smallness.

## 4. Is the full-3D conclusion mislabeled FPS \((H^3,L^2)\)?

No after correction.  The full-3D theorem assumes \(H^3\) smallness and
observes \(H^3\) distance, so its norm pair is \((H^3,H^3)\).  The resulting
\(L^2\) observation is only an \(H^3\)-input/\(L^2\)-output corollary.
Full-3D FPS \((H^3,L^2)\), which would allow large-\(H^3\) but
small-\(L^2\) data, remains OPEN.

FPS state their definition for equilibria.  The present statement is
explicitly a forward synchronized trajectory statement from \(t_0=0\), not
orbital stability and not a bound uniform over every starting time.

## 5. Can the \(H^3\) bootstrap cross its threshold?

No.  With

\[
 X=\|w\|_{H^3}^2,\qquad
 Y=\|\nabla w\|_{H^3}^2,\qquad X\le Y,
\]

the periodic product and commutator bounds give

\[
 {1\over2}X'+Y
 \le C_3\|\overline U_\Lambda\|_{H^4}X
 + C_3X^{1/2}Y.
\]

On \(X^{1/2}\le(2C_3)^{-1}\),

\[
 X'+Y\le2C_3\|\overline U_\Lambda\|_{H^4}X.
\]

The choices

\[
 r_3=(4C_3)^{-1},\qquad
 R_\Lambda=r_3e^{-C_3A_{4,\Lambda}}
\]

give the strict improvement \(X^{1/2}<r_3<(2C_3)^{-1}\).  The background
and perturbation \(H^3\) norms then remain bounded on every finite interval,
so the standard strong-solution continuation alternative closes globally.

## 6. Is the \(H^4\)-integral constant normalized correctly?

Yes.  Under normalized periodic measure,

\[
 \|\sin(2y)\|_{H^4}={25\over\sqrt2},\qquad
 \|\sin(4y)\|_{H^4}={289\over\sqrt2}.
\]

Integrating the two heat amplitudes gives

\[
 A_{4,\Lambda}
 \le\Lambda\left({25\over4\sqrt2}
 +{289\over32\sqrt2}\right)
 ={489\over32\sqrt2}\Lambda.
\]

This is an upper bound obtained by the triangle inequality; it is not
advertised as the optimal integral.

## 7. Does the R0.73M lower bound apply to the local modulus?

Yes, only for sufficiently large fixed \(\Lambda\).  For such a fixed
\(\Lambda\), the R0.73M family

\[
 h_{\Lambda,\rho}
 =\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda
\]

satisfies \(\|h_{\Lambda,\rho}\|_{H^3}\to0\) as
\(\rho\downarrow0\).  It therefore enters the limsup defining the local
pointed modulus.  The upper bound applies to every chord whose comparison
solution remains strong to \(T_*\).

## 8. Is the \(H^3\)-to-\(L^2\) lower bracket missing the launch cost?

No.  The \(L^2\)-normalized launch obeys
\(\|\phi_\Lambda\|_{H^3}\le C_H\Lambda^2\), so division by the actual
\(H^3\) input yields only

\[
 \mathfrak L_{\Lambda,\mathrm{loc}}^{3\to2}(T_*)
 \ge {c_*\over C_H}\Lambda^{-2}
 e^{\Lambda\mathcal A_*}.
\]

The polynomial loss is retained.  It still diverges exponentially.

## 9. Are there multiple Navier--Stokes flow maps hidden in the wording?

No after correction.  With viscosity, torus, and forcing fixed, there is
one time-\(T_*\) map \(S_{T_*}\) on its strong-solution domain.  The
parameter \(\Lambda\) marks different basepoints.  For fixed
\(0<\rho\le\rho_0\), R0.73M supplies pairs whose \(H^3\) separation tends
to zero while their \(L^2\) output separation stays at least \(c_*\rho\).
This proves failure of uniform continuity on that explicit unbounded data
set.  It does not prove discontinuity at any one basepoint.

## 10. Could the energy upper exponent contradict the selected lower one?

No.  The strict elementary chain is

\[
 j_*>{359\over324000}>{173\over450000}>\mathcal A_*.
\]

The first inequality follows from \(1-e^{-x}>x-x^2/2\), and the last is the
sealed R0.73M action bound.  The bracket establishes compatibility only:
neither exponent is claimed sharp, and no prefactor limit follows.

## 11. Can the varying backgrounds be diagonalized into one member?

No within the audited transformations.  Pure amplitude multiplication is
an accidental symmetry of the shear background, not of its nonlinear
neighborhood.  A time shift would require simultaneously

\[
 \Lambda=\Lambda_0e^{-4\tau}
 =\Lambda_0e^{-16\tau},
\]

forcing \(\tau=0\).  Fixed-viscosity parabolic scaling changes the torus,
Fourier rows, observation time, and \(H^3\) norm unless its scale is one.
Original-time compactness fails because the background norm grows like
\(\Lambda\), and bounded time shifts lose the second harmonic.

## 12. Does fixed-member stability advance the Clay alternative?

No.  The theorem constructs a positive stability neighborhood for one
explicit class of globally smooth, decaying shears.  It neither controls
large three-dimensional perturbations nor produces vortex-stretching
growth, a singularity, or global regularity for arbitrary smooth data.

## Exact boundary

~~~text
fixedTimeRelativeL2LipschitzBound=CLOSED
fixedMemberPlanarL2SynchronizedStability=CLOSED
fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED
fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY
familyFlowMapNonuniformMarkedBasepointSensitivity=CLOSED
singleR073mMemberH3SmallL2FixedDistanceEscape=FALSE
fullThreeDimensionalFPSH3L2Stability=OPEN
optimalFixedMemberStabilityRadius=OPEN
sharpFamilyLipschitzExponent=OPEN
arbitraryFixedBackgroundInstability=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
~~~
