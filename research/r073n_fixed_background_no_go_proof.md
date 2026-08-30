# R0.73N proof: finite-strain stability and nonuniform family sensitivity

**Status:** continuum proof; independent analytic and adversarial audits,
direct symmetry audit, and bounded literature audit PASS; finite and
publication gates remain separate

**Depends on:** the sealed R0.73M prescribed-action departure theorem only
for the lower bound in Section 5; Sections 2--4 are direct estimates for the
exact physical Navier--Stokes equation

## 1. Statement

On the normalized standard three-torus, in the mean-zero divergence-free
phase space, let

\[
 \overline U_\Lambda(t,y)
 =\left(0,0,-\Lambda e^{-4t}\sin2y
 +\frac\Lambda2e^{-16t}\sin4y\right),
 \qquad \Lambda>0.
 \tag{1.1}
\]

For every fixed \(\Lambda\), this exact unforced trajectory is forward
synchronized \((H^3,H^3)\)-stable from \(t_0=0\) in the full
three-dimensional strong phase space.  It is also synchronized
\((H^3_{\rm pl},L^2_{\rm pl})\)-stable in the invariant planar subsystem,
with genuine \(L^2\) initial smallness.  These are the natural
trajectory-at-\(t_0=0\) extensions of the FPS equilibrium norm
quantifiers, not orbital or all-starting-time uniform stability.
More precisely:

1. any coexisting strong solution \(V\) satisfies

   \[
   \|V(T)-\overline U_\Lambda(T)\|_2
   \le e^{\Lambda j(T)}
   \|V(0)-\overline U_\Lambda(0)\|_2,
   \tag{1.2}
   \]

   where

   \[
   j(T)=\frac{1-e^{-4T}}4+\frac{1-e^{-16T}}{16}
   \le\frac5{16};
   \tag{1.3}
   \]

2. there is a positive, \(\Lambda\)-dependent \(H^3\) radius on which every
   three-dimensional perturbation is global and remains uniformly small;

3. at \(T_*=1/1800\), for every sufficiently large \(\Lambda\), the local
   \(L^2\)-to-\(L^2\) chordal modulus obeys

   \[
   c_*e^{\Lambda\mathcal A_*}
   \le\mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T_*)
   \le e^{\Lambda j_*},
   \tag{1.4}
   \]

   with \(\mathcal A_*<j_*\).

Thus R0.73M gives exponentially growing pointed amplification, hence
failure of uniform continuity on an explicit unbounded data set, not
instability of any fixed member in the synchronized senses proved here.

## 2. Exact relative-energy inequality

Let \(V\) be a strong solution of the same unforced equation and put

\[
 w=V-\overline U_\Lambda.
 \tag{2.1}
\]

Since both fields are divergence free, \(w\) satisfies

\[
 \partial_tw-\Delta w
 +\overline U_\Lambda\cdot\nabla w
 +w\cdot\nabla\overline U_\Lambda
 +w\cdot\nabla w+\nabla q=0,
 \qquad \nabla\cdot w=0.
 \tag{2.2}
\]

The pressure, background transport, and self-transport terms vanish in the
\(L^2\) pairing.  If \(F_\Lambda\) is the third component of the background,
then

\[
 \frac12\frac{\mathrm d}{\mathrm dt}\|w\|_2^2
 +\|\nabla w\|_2^2
 =-\int_{\mathbb T^3}
 (\partial_yF_\Lambda)w_2w_3\,\mathrm dx.
 \tag{2.3}
\]

Using \(2|w_2w_3|\le |w_2|^2+|w_3|^2\le|w|^2\),

\[
 \frac12\frac{\mathrm d}{\mathrm dt}\|w\|_2^2
 \le\frac12\|\partial_yF_\Lambda(t)\|_\infty
 \|w\|_2^2.
 \tag{2.4}
\]

Equation (1.1) gives

\[
 \partial_yF_\Lambda
 =-2\Lambda e^{-4t}\cos2y
 +2\Lambda e^{-16t}\cos4y,
 \tag{2.5}
\]

and hence

\[
 \frac12\|\partial_yF_\Lambda(t)\|_\infty
 \le\Lambda(e^{-4t}+e^{-16t}).
 \tag{2.6}
\]

Gronwall now yields

\[
 \|w(T)\|_2
 \le\exp\left\{
 \Lambda\int_0^T(e^{-4t}+e^{-16t})\,\mathrm dt
 \right\}\|w(0)\|_2,
 \tag{2.7}
\]

which is exactly (1.2)--(1.3).  Since \(j(T)\le5/16\) for every
\(T<T_{\max}\), it follows that

\[
 \sup_{0\le t<T_{\max}}\|w(t)\|_2
 \le e^{5\Lambda/16}\|w(0)\|_2
 \tag{2.8}
\]

on the common strong lifespan.  This estimate is nonlinear and permits
fully three-dimensional \(w\); no selected row, spectral approximation, or
Fourier truncation is used.

## 3. Planar fixed-member synchronized stability

If \(w(0)\) lies in the invariant planar subspace

\[
 \mathcal S_{2D}
 =\{(0,v_2(y,z),v_3(y,z)):
 \partial_yv_2+\partial_zv_3=0\},
 \tag{3.1}
\]

then both \(V\) and \(\overline U_\Lambda\) remain in that subspace.  The
scalar-vorticity enstrophy identity gives global smoothness.  Given
\(\epsilon>0\), choose

\[
 \delta=\epsilon e^{-5\Lambda/16}.
 \tag{3.2}
\]

For any planar \(V(0)\in H^3_{\rm pl}\) satisfying
\(\|w(0)\|_2<\delta\), global two-dimensional regularity and (2.8) give

\[
 \sup_{t\ge0}\|w(t)\|_2<\epsilon.
 \tag{3.3}
\]

Thus every fixed member is synchronized
\((H^3_{\rm pl},L^2_{\rm pl})\)-stable in the exact planar subsystem with
the FPS choice of regularity and distance norms.  In particular, the
R0.73M planar construction cannot be
diagonalized into fixed-member \(H^3\)-small,
\(L^2\)-fixed-distance escape.

## 4. A positive full three-dimensional \(H^3\) tube

The preceding \(L^2\) estimate alone does not prove global strong existence
for arbitrary three-dimensional perturbations.  We now close that gap for a
sufficiently small, fixed-\(\Lambda\) \(H^3\) tube.

Work in the mean-zero divergence-free phase space.  Use the normalized
Bessel-potential norm, put \(J^3=(I-\Delta)^{3/2}\), and write

\[
 X(t)=\|w(t)\|_{H^3}^2,
 \qquad
 Y(t)=\|\nabla w(t)\|_{H^3}^2.
 \tag{4.1}
\]

The perturbation is mean zero, so \(X\le Y\).  Standard periodic
Kato--Ponce/Moser commutator estimates, together with the cancellations of
the top-order transport terms, give a universal \(C_3\ge1\) such that

\[
 \frac12X'(t)+Y(t)
 \le C_3\|\overline U_\Lambda(t)\|_{H^4}X(t)
 +C_3X(t)^{1/2}Y(t).
 \tag{4.2}
\]

Equivalently, after expanding integer derivatives through order three, the
three contributions have the schematic bounds

\[
 \begin{aligned}
 |\langle[D^\alpha,\overline U_\Lambda\cdot\nabla]w,
 D^\alpha w\rangle|
 &\le C_3\|\overline U_\Lambda\|_{H^4}X,\\
 |\langle D^\alpha(w\cdot\nabla\overline U_\Lambda),
 D^\alpha w\rangle|
 &\le C_3\|\overline U_\Lambda\|_{H^4}X,\\
 |\langle[D^\alpha,w\cdot\nabla]w,D^\alpha w\rangle|
 &\le C_3X^{1/2}Y,
 \end{aligned}
 \tag{4.3}
\]

summed over \(|\alpha|\le3\).  The Sobolev product and commutator bounds use
\(H^3(\mathbb T^3)\hookrightarrow W^{1,\infty}\).  The mean-zero Poincare
inequality is used only to pass from \(X\) to \(Y\).

Set

\[
 A_{4,\Lambda}
 :=\int_0^\infty\|\overline U_\Lambda(t)\|_{H^4}\,\mathrm dt.
 \tag{4.4}
\]

The two Fourier modes are orthogonal.  The triangle inequality and

\[
 \|\sin(ky)\|_{H^4}
 ={(1+k^2)^2\over\sqrt2}
 \tag{4.5}
\]

give

\[
 \begin{aligned}
 A_{4,\Lambda}
 &\le\Lambda\left[
 {1\over4}{25\over\sqrt2}
 +{1\over2}{1\over16}{289\over\sqrt2}
 \right]\\
 &=\frac{489}{32\sqrt2}\Lambda.
 \end{aligned}
 \tag{4.6}
\]

Let

\[
 r_3:=\frac1{4C_3},
 \qquad
 R_\Lambda:=r_3e^{-C_3A_{4,\Lambda}}.
 \tag{4.7}
\]

Assume \(\|w(0)\|_{H^3}<R_\Lambda\).  On the maximal interval where
\(X^{1/2}\le(2C_3)^{-1}\), equation (4.2) implies

\[
 X'(t)+Y(t)
 \le2C_3\|\overline U_\Lambda(t)\|_{H^4}X(t),
 \tag{4.8}
\]

and therefore

\[
 X(t)^{1/2}
 \le e^{C_3A_{4,\Lambda}}X(0)^{1/2}
 <r_3<\frac1{2C_3}.
 \tag{4.9}
\]

The strict improvement closes the bootstrap.  Moreover,
\(\|\overline U_\Lambda(t)\|_{H^3}\) is bounded for all \(t\ge0\), so
\(\|V(t)\|_{H^3}\le
\|\overline U_\Lambda(t)\|_{H^3}+\|w(t)\|_{H^3}\) remains bounded on every
finite interval.  The standard \(H^3\) continuation criterion therefore
makes the solution global and proves

\[
 \sup_{t\ge0}\|w(t)\|_{H^3}
 \le e^{C_3A_{4,\Lambda}}\|w(0)\|_{H^3}.
 \tag{4.10}
\]

For every \(\epsilon>0\), choosing

\[
 \delta_\Lambda(\epsilon)
 =\min\{R_\Lambda,
 \epsilon e^{-C_3A_{4,\Lambda}}}
 \tag{4.11}
\]

proves full three-dimensional forward synchronized \((H^3,H^3)\)
stability of the fixed trajectory from \(t_0=0\), with the FPS choice of
regularity and distance norms.  It also implies the custom
\(H^3\)-small-input/\(L^2\)-observed estimate, since
\(\|w\|_2\le\|w\|_{H^3}\).  It does not prove FPS \((H^3,L^2)\) stability,
whose hypothesis would require only \(L^2\) smallness.  The \(H^3\) radius
may be exponentially small in \(\Lambda\), but it is positive for every
fixed \(\Lambda\).

## 5. The exact meaning of R0.73M: pointed sensitivity

Let \(\mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T)\) be the local chordal
modulus in the problem freeze, equation (5.1).  The upper bound (1.2) gives

\[
 \mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T_*)
 \le e^{\Lambda j_*}.
 \tag{5.1}
\]

R0.73M supplies, for every sufficiently large \(\Lambda\) and every
\(0<\rho\le\rho_0\), the perturbation

\[
 h_{\Lambda,\rho}
 =\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda,
 \qquad
 \|\phi_\Lambda\|_2=1,
 \tag{5.2}
\]

and the endpoint estimate

\[
 \|\Pi_{\{K_z=\pm1\}}
 (V_{\Lambda,\rho}(T_*)-
 \overline U_\Lambda(T_*))\|_2
 \ge c_*\rho.
 \tag{5.3}
\]

Since projection cannot increase the norm, division by
\(\|h_{\Lambda,\rho}\|_2=\rho e^{-\Lambda\mathcal A_*}\) yields

\[
 \mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T_*)
 \ge c_*e^{\Lambda\mathcal A_*}.
 \tag{5.4}
\]

Combining (5.1) and (5.4) proves the bracket

\[
 c_*e^{\Lambda\mathcal A_*}
 \le\mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T_*)
 \le e^{\Lambda j_*}.
 \tag{5.5}
\]

It remains to verify that the upper exponent does not contradict the lower
one.  Since \(D_*=1/450\), the strict inequality
\(1-e^{-x}>x-x^2/2\) gives

\[
 \begin{aligned}
 j_*
 &=\frac{1-e^{-D_*}}4
 +\frac{1-e^{-4D_*}}{16}\\
 &>\frac{D_*}2-\frac58D_*^2
 =\frac{359}{324000}.
 \end{aligned}
 \tag{5.6}
\]

The inherited action bound and exact rational comparison give

\[
 \mathcal A_*<\frac{173}{450000}
 <\frac{359}{324000}<j_*.
 \tag{5.7}
\]

Indeed, the middle comparison is

\[
 173\cdot324000=56{,}052{,}000
 <161{,}550{,}000=359\cdot450000.
 \tag{5.8}
\]

Using the R0.73M launch bound
\(\|\phi_\Lambda\|_{H^3}\le C_H\Lambda^2\), the
\(H^3\)-input/\(L^2\)-output local modulus also satisfies

\[
 \frac{c_*}{C_H}\Lambda^{-2}e^{\Lambda\mathcal A_*}
 \le\mathfrak L_{\Lambda,\mathrm{loc}}^{3\to2}(T_*)
 \le e^{\Lambda j_*}.
 \tag{5.9}
\]

At any fixed \(0<\rho\le\rho_0\), these same input pairs have

\[
 \|h_{\Lambda,\rho}\|_{H^3}
 \le C_H\rho\Lambda^2e^{-\Lambda\mathcal A_*}\longrightarrow0,
 \qquad
 \|S_{T_*}(\overline U_\Lambda(0)+h_{\Lambda,\rho})
 -S_{T_*}(\overline U_\Lambda(0))\|_2\ge c_*\rho.
 \tag{5.10}
\]

Therefore \(S_{T_*}\) is not uniformly continuous from \(H^3\) to \(L^2\)
on the explicit unbounded set containing these marked pairs.  The gap
\(j_*-\mathcal A_*\) only shows compatibility.  Neither endpoint of (5.5)
or (5.9) is asserted to be the sharp nonlinear Lipschitz exponent.  These
are local moduli of the same time-\(T_*\) Navier--Stokes flow map at
different marked basepoints, not different solution maps.

## 6. Quantifier obstruction

R0.73M proves

\[
 \exists\rho_0,c_*,\Lambda_0\quad
 \forall\Lambda\ge\Lambda_0\quad
 \forall\rho\in(0,\rho_0]
 \tag{6.1}
\]

with a different base \(\overline U_\Lambda\) for every \(\Lambda\).  For
fixed \(\rho>0\), the initial \(H^3\) perturbation tends to zero as
\(\Lambda\to\infty\), while the endpoint remains at least \(c_*\rho\).

Fix instead one admissible
\(\Lambda^\sharp\ge\Lambda_0\).  Sending \(\rho\downarrow0\) in the
R0.73M construction makes both the input and, by (1.2), the actual endpoint
distance tend to zero:

\[
 \|h_{\Lambda^\sharp,\rho}\|_{H^3}\to0,
 \qquad
 \|V_{\Lambda^\sharp,\rho}(T_*)-
 \overline U_{\Lambda^\sharp}(T_*)\|_2\to0.
 \tag{6.2}
\]

More decisively, Sections 2--4 give a positive stability radius for every
fixed \(\Lambda>0\), including members below the R0.73M threshold.
Therefore the exchange

\[
 \left(\forall\Lambda\ \exists h_\Lambda\right)
 \quad\Longrightarrow\quad
 \left(\exists\Lambda_0\ \forall\delta\ \exists h_\delta\right)
 \tag{6.3}
\]

is not merely unproved: the \(H^3\)-small-input,
\(L^2\)-fixed-distance conclusion is false for every member of the family.
This statement does not assert FPS \((H^3,L^2)\) stability.

## 7. Result ledger and boundary

The proof establishes, subject to independent audit,

```text
fixedTimeRelativeL2LipschitzBound=CLOSED
finiteAllTimeStrainEnvelope=CLOSED
fixedMemberPlanarL2SynchronizedStability=CLOSED
fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED
fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY
familyFlowMapNonuniformMarkedBasepointSensitivity=CLOSED
familyDepartureImpliesFixedMemberInstability=FALSE_AS_INFERENCE
singleR073mMemberH3SmallL2FixedDistanceEscape=FALSE
fullThreeDimensionalFPSH3L2Stability=OPEN
optimalFixedMemberStabilityRadius=OPEN
sharpFamilyLipschitzExponent=OPEN
arbitraryFixedBackgroundInstability=OPEN
transverseCriticalNormGrowth=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
```

The no-go is topology- and family-specific.  It does not exclude transient
growth at fixed \(\Lambda\), growth in a stronger or critical norm, loss of
regularity outside the proved \(H^3\) tube, forced steady-flow instability,
or a different fixed non-autonomous trajectory with infinite accumulated
strain.
