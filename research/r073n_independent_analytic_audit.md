# R0.73N independent analytic audit

**Audit date:** 2026-08-31

**Files audited:** r073n_problem_freeze.md,
r073n_fixed_background_no_go_proof.md, and
r073n_scaling_obstruction.md

**Method:** independent rederivation of the exact background equation,
relative energy, all-time strain envelope, planar and three-dimensional
stability quantifiers, \(H^3\) bootstrap, pointed moduli, rational exponent
comparison, scaling ledger, and compactness obstruction

**Verdict:** **MATHEMATICAL FINAL PASS**

The continuum theorem and route obstruction pass.  Finite diagnostics and
publication remain separate evidence classes.

## 1. The background is an exact unforced trajectory

Write

\[
 \overline U_\Lambda(t,y)=e_zF_\Lambda(t,y),\qquad
 F_\Lambda=-\Lambda e^{-4t}\sin2y
 +{\Lambda\over2}e^{-16t}\sin4y.
\]

Because \(F_\Lambda\) is independent of \(z\),
\((\overline U_\Lambda\cdot\nabla)\overline U_\Lambda=0\).
Each Fourier mode satisfies the heat equation with rates \(4\) and \(16\).
Thus

\[
 \partial_t\overline U_\Lambda-\Delta\overline U_\Lambda=0
\]

and the field is an exact zero-forcing Navier--Stokes solution on the
standard torus for every finite \(\Lambda>0\).

## 2. Relative \(L^2\) bound

For \(w=V-\overline U_\Lambda\), divergence-free integration by parts
removes pressure, \(\overline U_\Lambda\)-transport, and self-transport.
The only energy-producing term is

\[
 -\int(\partial_yF_\Lambda)w_2w_3.
\]

The pointwise inequality \(2|w_2w_3|\le |w|^2\) gives

\[
 {1\over2}{d\over dt}\|w\|_2^2
 \le {1\over2}\|\partial_yF_\Lambda\|_\infty\|w\|_2^2.
\]

Since

\[
 {1\over2}\|\partial_yF_\Lambda(t)\|_\infty
 \le\Lambda(e^{-4t}+e^{-16t}),
\]

Gronwall yields

\[
 \|w(T)\|_2
 \le e^{\Lambda j(T)}\|w(0)\|_2,\qquad
 j(T)={1-e^{-4T}\over4}+{1-e^{-16T}\over16}.
\]

The factor of two is correct for the norm rather than its square.
Furthermore \(j(T)\uparrow5/16\), so the same finite upper factor applies
on every common strong lifespan.

## 3. Planar synchronized stability

The subspace

\[
 \mathcal S_{2D}
 =\{(0,v_2(y,z),v_3(y,z)):
 \partial_yv_2+\partial_zv_3=0\}
\]

is invariant.  Its scalar vorticity has the standard two-dimensional
enstrophy identity, so every \(H^3_{\rm pl}\) datum produces a global strong
solution.  Therefore

\[
 \|w(0)\|_2<\epsilon e^{-5\Lambda/16}
 \quad\Longrightarrow\quad
 \sup_{t\ge0}\|w(t)\|_2<\epsilon.
\]

This is synchronized \((H^3_{\rm pl},L^2_{\rm pl})\) stability with
genuine \(L^2\) initial smallness.  No planar \(H^3\)-small assumption is
inserted.

## 4. Full three-dimensional \(H^3\) energy

In the mean-zero divergence-free phase space, put

\[
 X=\|w\|_{H^3}^2,\qquad
 Y=\|\nabla w\|_{H^3}^2.
\]

Normalized periodic Fourier weights give \(X\le Y\).  A direct
Kato--Ponce/Moser derivation, or the equivalent integer-derivative
derivation with norm constants absorbed, gives

\[
 {1\over2}X'+Y
 \le C_3\|\overline U_\Lambda\|_{H^4}X
 +C_3X^{1/2}Y.
\]

The background transport uses a commutator after its leading
divergence-free cancellation.  The \(w\cdot\nabla\overline U_\Lambda\)
term uses the \(H^3\) product estimate and one extra derivative of the
background.  The self-transport term is bounded by
\(C\|\nabla w\|_\infty X\le CX^{3/2}\le CX^{1/2}Y\).
Thus the displayed inequality has no untracked derivative loss.

## 5. Integrated \(H^4\) background and bootstrap

Under normalized periodic measure,

\[
 \|\sin(ky)\|_{H^4}={(1+k^2)^2\over\sqrt2}.
\]

The triangle inequality and exact heat integrals give

\[
 \begin{aligned}
 A_{4,\Lambda}
 &:=\int_0^\infty\|\overline U_\Lambda(t)\|_{H^4}\,dt\\
 &\le\Lambda\left[
 {1\over4}{25\over\sqrt2}
 +{1\over2}{1\over16}{289\over\sqrt2}\right]
 ={489\over32\sqrt2}\Lambda.
 \end{aligned}
\]

On the bootstrap interval \(X^{1/2}\le(2C_3)^{-1}\),

\[
 X'+Y\le2C_3\|\overline U_\Lambda\|_{H^4}X.
\]

Taking

\[
 r_3={1\over4C_3},\qquad
 R_\Lambda=r_3e^{-C_3A_{4,\Lambda}},
\]

and \(\|w(0)\|_{H^3}<R_\Lambda\), Gronwall gives the strict improvement

\[
 X(t)^{1/2}
 \le e^{C_3A_{4,\Lambda}}X(0)^{1/2}
 <r_3<{1\over2C_3}.
\]

The bootstrap cannot terminate.  The background \(H^3\) norm is bounded,
so \(V=\overline U_\Lambda+w\) remains \(H^3\)-bounded on every finite
interval.  The standard strong continuation alternative makes \(V\)
global.

Consequently every fixed member is forward synchronized
\((H^3,H^3)\)-stable from \(t_0=0\).  It has the custom
\(H^3\)-input/\(L^2\)-output corollary.  Full-three-dimensional FPS
\((H^3,L^2)\), which would require only \(L^2\) initial smallness, is not
proved and remains OPEN.

## 6. Endpoint exponent compatibility

At \(D_*=1/450\) and \(T_*=D_*/4\),

\[
 j_*={1-e^{-D_*}\over4}+{1-e^{-4D_*}\over16}.
\]

Applying \(1-e^{-x}>x-x^2/2\) to both exponentials gives

\[
 j_*>{D_*\over2}-{5D_*^2\over8}
 ={359\over324000}.
\]

The sealed R0.73M action interval then gives the strict exact chain

\[
 j_*>{359\over324000}>{173\over450000}>\mathcal A_*.
\]

No floating-point value is needed for this theorem-level comparison.

## 7. Local pointed moduli and uniform continuity

For a fixed sufficiently large \(\Lambda\), the R0.73M perturbations enter
every \(H^3\) neighborhood as \(\rho\downarrow0\).  Dividing the endpoint
lower bound by the exact \(L^2\) launch size gives

\[
 c_*e^{\Lambda\mathcal A_*}
 \le\mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T_*).
\]

The relative energy inequality gives the upper bound

\[
 \mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T_*)
 \le e^{\Lambda j_*}.
\]

The launch estimate
\(\|\phi_\Lambda\|_{H^3}\le C_H\Lambda^2\) gives

\[
 {c_*\over C_H}\Lambda^{-2}e^{\Lambda\mathcal A_*}
 \le\mathfrak L_{\Lambda,\mathrm{loc}}^{3\to2}(T_*)
 \le e^{\Lambda j_*}.
\]

At fixed \(0<\rho\le\rho_0\), the corresponding input-pair \(H^3\)
distance tends to zero as \(\Lambda\to\infty\), whereas its output
\(L^2\) distance remains at least \(c_*\rho\).  Hence the single
time-\(T_*\) flow map fails to be uniformly continuous on the explicit
unbounded set of marked pairs.  This is not discontinuity or instability
at one basepoint.

## 8. Quantifier audit

R0.73M has the order

\[
 \exists\rho_0,c_*,\Lambda_0\quad
 \forall\Lambda\ge\Lambda_0\quad
 \forall\rho\in(0,\rho_0].
\]

The background depends on \(\Lambda\).  Fixing one admissible
\(\Lambda^\sharp\) and sending \(\rho\downarrow0\) sends the actual endpoint
distance to zero by the relative upper bound.  Independently, the
\(H^3\) tube gives every fixed \(\Lambda>0\) a positive synchronized
stability radius.  The varying-background quantifiers therefore cannot be
exchanged into one fixed member with arbitrarily small \(H^3\) input and a
fixed \(L^2\) escape distance.

## 9. Symmetry and compactness audit

For

\[
 v(t,x)=A\,u(ACt,Cx),
\]

direct substitution gives

\[
 \nu'={A\over C}\nu,\qquad
 L'={L\over C},\qquad
 T'={T\over AC}.
\]

Fixed viscosity requires \(A=C\).  Preserving the standard torus as an
invertible conjugacy, the selected Fourier rows, the observation time, and
the \(H^3\) topology then forces \(C=1\).  Integer \(C>1\) is a
noninvertible torus covering and changes the rows and norm.

Pure amplitude works only on the base shear because its self-advection is
zero; it does not conjugate the perturbed nonlinear equation.  Equality
under a time shift would require

\[
 \Lambda=\Lambda_0e^{-4\tau}
 =\Lambda_0e^{-16\tau},
\]

and hence \(\tau=0\).  At the original time,
\(\|\overline U_\Lambda(0)\|_2^2=5\Lambda^2/8\), so there is no bounded
Sobolev subsequence.  Under a bounded time-shift normalization, the two
coefficients satisfy

\[
 b_\Lambda={a_\Lambda^4\over\Lambda^3};
\]

every bounded limit loses the second harmonic.  None of these maps
identifies the R0.73M family with one fixed trajectory in the same equation,
domain, time, and topology.

## 10. Final boundary

~~~text
fixedTimeRelativeL2LipschitzBound=CLOSED
finiteAllTimeStrainEnvelope=CLOSED
fixedMemberPlanarL2SynchronizedStability=CLOSED
fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED
fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY
familyFlowMapNonuniformMarkedBasepointSensitivity=CLOSED
familyDepartureImpliesFixedMemberInstability=FALSE_AS_INFERENCE
singleR073mMemberH3SmallL2FixedDistanceEscape=FALSE
amplitudeOnlyIdentificationIsNSSymmetry=FALSE
timeTranslationIdentifiesLambdaFamily=FALSE
parabolicScalingIdentifiesLambdaFamilyOnFixedTorus=FALSE
fullThreeDimensionalFPSH3L2Stability=OPEN
optimalFixedMemberStabilityRadius=OPEN
sharpFamilyLipschitzExponent=OPEN
arbitraryFixedBackgroundInstability=OPEN
transverseCriticalNormGrowth=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
~~~

The PASS is route-specific.  It does not classify arbitrary
Navier--Stokes trajectories, prove an optimal radius or sharp exponent,
control large three-dimensional perturbations, or advance either side of
the Clay alternative.
