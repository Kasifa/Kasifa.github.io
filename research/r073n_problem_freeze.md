# R0.73N problem freeze: fixed-background stability and the Lyapunov transfer obstruction

**Status:** frozen source contract; continuum proof plus independent
analytic, adversarial, symmetry, compactness, and bounded primary-source
audits PASS; finite and publication gates remain separate

**Parent result:** R0.73M prescribed-action planar nonlinear departure

**Equation:** unforced incompressible Navier--Stokes on the standard
three-torus, viscosity one, in the mean-zero divergence-free phase space

**Topologies:** the full three-dimensional theorem is forward synchronized
\((H^3,H^3)\) stability from \(t_0=0\), using the FPS norm quantifiers but
extending them from an equilibrium to one fixed trajectory.  Its
\(H^3\)-small-input, \(L^2\)-observed consequence is recorded separately
and is not renamed FPS \((H^3,L^2)\) stability.  Synchronized
\((H^3_{\rm pl},L^2_{\rm pl})\) stability with genuine \(L^2\) initial
smallness is proved only in the invariant planar subsystem.

## 0. Direct decision to be proved

R0.73M does **not** produce Lyapunov instability of one fixed background.
The parameter that makes the initial perturbation vanish also changes the
background:

\[
 \overline U_\Lambda(t,y)
 =(0,0,2\Lambda W(4t,2y)),
 \qquad
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x.
 \tag{0.1}
\]

R0.73N asks a sharper question than logical non-implication.  For each fixed
\(0<\Lambda<\infty\), can the trajectory \(\overline U_\Lambda\) exhibit
the \(H^3\)-small-input, \(L^2\)-fixed-distance escape suggested by R0.73M,
or does the unforced heat decay give it a positive \(H^3\) stability radius?

The target answer is a no-go theorem for the present route:

1. every coexisting strong solution has a lifetime-independent relative
   \(L^2\) gain bound, which becomes all-time in the planar subsystem and
   inside the three-dimensional \(H^3\) tube;
2. every fixed member has a positive three-dimensional \(H^3\) strong-solution
   stability tube;
3. R0.73M instead proves exponentially growing pointed amplification and
   failure of uniform continuity across an unbounded family of marked
   backgrounds;
4. no exact symmetry, time shift, or compactness argument identifies that
   family with one trajectory in the same equation, domain, and topology.

This is a structural closure of the proposed fixed-background upgrade, not a
statement about arbitrary backgrounds or about finite-time singularity.

## 1. Exact physical background and strain envelope

Expanding (0.1) in physical time gives

\[
 \overline U_\Lambda(t,y)
 =\left(0,0,
 -\Lambda e^{-4t}\sin2y
 +\frac\Lambda2e^{-16t}\sin4y\right).
 \tag{1.1}
\]

If \(F_\Lambda(t,y)\) denotes the third component, then

\[
 \|\partial_yF_\Lambda(t)\|_\infty
 \le 2\Lambda(e^{-4t}+e^{-16t}).
 \tag{1.2}
\]

Define the normalized accumulated symmetric-strain envelope

\[
 j(T):=\frac{1-e^{-4T}}4+\frac{1-e^{-16T}}{16},
 \qquad
 j(\infty)=\frac5{16}.
 \tag{1.3}
\]

At the R0.73M endpoint

\[
 D_*:=\frac1{450},
 \qquad
 T_*:=\frac{D_*}{4}=\frac1{1800},
 \tag{1.4}
\]

write

\[
 j_*:=j(T_*)
 =\frac{1-e^{-D_*}}4+\frac{1-e^{-4D_*}}{16}.
 \tag{1.5}
\]

The inherited selected action is

\[
 \mathcal A_*:=\int_0^{D_*}\lambda_0(d)\,\mathrm d d,
 \qquad
 \frac{167}{450000}<\mathcal A_*<\frac{173}{450000}.
 \tag{1.6}
\]

The exact elementary comparison to be audited is

\[
 j_*>\frac{359}{324000}>\frac{173}{450000}>\mathcal A_*.
 \tag{1.7}
\]

The first inequality follows from \(1-e^{-x}>x-x^2/2\), not from a
floating-point evaluation.

## 2. Fixed-trajectory stability quantifiers

Friedlander--Pavlović--Shvydkoy state their definition for an equilibrium:
\(X\) is the solution-regularity class and \(Z\) is used for both initial
smallness and observed distance.  We use the same norm quantifiers for
**forward synchronized stability of the fixed trajectory from
\(t_0=0\)**; this is neither orbital stability nor a claim uniform over all
starting times.  Thus full three-dimensional \((H^3,H^3)\) stability here
means

\[
 \forall\epsilon>0\ \exists\delta>0:\quad
 V(0)\in H^3_\sigma,\quad
 \|V(0)-\overline U(0)\|_{H^3}<\delta
 \tag{2.1}
\]

implies a global strong solution and

\[
 \sup_{t\ge0}\|V(t)-\overline U(t)\|_{H^3}<\epsilon.
 \tag{2.2}
\]

This theorem implies the weaker, custom \(H^3\)-input/\(L^2\)-observation
statement obtained by replacing the norm in (2.2) by \(L^2\).  It does
**not** imply FPS \((H^3,L^2)\) stability, because that definition would
assume only \(L^2\) initial smallness for otherwise arbitrary \(H^3\) data.

In the invariant planar subsystem, global two-dimensional regularity does
permit the corresponding synchronized choice
\(X=H^3_{\rm pl}\), \(Z=L^2_{\rm pl}\) with genuine \(L^2\) initial
smallness.

The fixed-distance escape relevant to R0.73M is the negation of the custom
\(H^3\)-input/\(L^2\)-observation statement.  It would require

\[
 \exists\epsilon_0>0\quad\forall\delta>0\quad
 \exists h_\delta,\ t_\delta\ge0:
 \|h_\delta\|_{H^3}<\delta,
 \quad
 \|V_\delta(t_\delta)-\overline U(t_\delta)\|_2
 \ge\epsilon_0.
 \tag{2.3}
\]

The background, viscosity, domain, forcing, and both norms in (2.3) cannot
depend on \(\delta\).  FPS instability has one additional branch: failure
of the required global solution.  R0.73M supplies neither branch for one
fixed background.

R0.73M has a different quantifier order:

\[
 \exists\rho_0,c_*,\Lambda_0\quad
 \forall\Lambda\ge\Lambda_0\quad
 \forall\rho\in(0,\rho_0],
 \tag{2.4}
\]

with the background equal to \(\overline U_\Lambda\).  Fixing \(\Lambda\)
and sending \(\rho\downarrow0\) makes both the input and the licensed endpoint
lower bound tend to zero.  Sending \(\Lambda\to\infty\) keeps the endpoint
at fixed order only by changing the background.

## 3. Targets N1--N3: relative energy, finite strain, and the planar consequence

Let \(V\) be any strong solution of the same unforced equation on
\([0,T]\), and put \(w=V-\overline U_\Lambda\).  The first obligation is

\[
 \boxed{
 \|w(T)\|_2
 \le e^{\Lambda j(T)}\|w(0)\|_2.}
 \tag{3.1}
\]

Consequently, on every common strong lifespan,

\[
 \boxed{
 \sup_{0\le t<T_{\max}}\|w(t)\|_2
 \le e^{5\Lambda/16}\|w(0)\|_2.}
 \tag{3.2}
\]

For planar perturbations the common lifespan is global by the two-dimensional
vorticity estimate.  For arbitrary three-dimensional perturbations, N4 below
must provide the global strong tube before (3.2) is advertised as a full
Lyapunov-stability theorem.

## 4. Target N4: a positive three-dimensional \(H^3\) tube

Let \(C_3\) be a universal constant in the periodic \(H^3\) commutator
estimate, and put

\[
 A_{4,\Lambda}:=\int_0^\infty
 \|\overline U_\Lambda(t)\|_{H^4}\,\mathrm dt.
 \tag{4.1}
\]

With the normalized Bessel-potential Sobolev norm, the explicit two-mode
background satisfies

\[
 A_{4,\Lambda}
 \le\frac{489}{32\sqrt2}\Lambda.
 \tag{4.2}
\]

The target is to prove constants \(r_3,C_3>0\), independent of \(\Lambda\),
such that

\[
 \|w(0)\|_{H^3}
 \le r_3e^{-C_3A_{4,\Lambda}}
 \tag{4.3}
\]

implies a unique global three-dimensional strong solution and

\[
 \boxed{
 \sup_{t\ge0}\|w(t)\|_{H^3}
 \le e^{C_3A_{4,\Lambda}}\|w(0)\|_{H^3}.}
 \tag{4.4}
\]

The constants need not be numerically sharp.  Positivity for each fixed
\(\Lambda\), and explicit nonuniform dependence on \(\Lambda\), are the
logical points.

## 5. Targets N5--N6: nonuniform family sensitivity

For fixed \(T\), define the strong-solution domain

\[
 \mathcal D_T:=\{u_0\in H^3_{\sigma,0}:
 \text{the unique strong solution from }u_0
 \text{ exists on }[0,T]\},
 \tag{5.0}
\]

and let \(S_T:\mathcal D_T\to H^3_{\sigma,0}\) be its time-\(T\) state map.
Define the local \(L^2\)-to-\(L^2\) chordal modulus at the marked background
by

\[
 \mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T)
 :=\limsup_{r\downarrow0}
 \sup_{\substack{h\in C^\infty_{\sigma,0},\
 0<\|h\|_{H^3}<r\\
 \overline U_\Lambda(0)+h\in\mathcal D_T}}
 \frac{\|S_T(\overline U_\Lambda(0)+h)
 -S_T(\overline U_\Lambda(0))\|_2}{\|h\|_2},
 \tag{5.1}
\]

where \(C^\infty_{\sigma,0}\) denotes smooth mean-zero divergence-free
fields.  The superscript \(2\to2\) records the two norms in the quotient;
the neighborhood is still localized in \(H^3\).  For every sufficiently
large \(\Lambda\), R0.73M and N1 should give

\[
 \boxed{
 c_*e^{\Lambda\mathcal A_*}
 \le\mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T_*)
 \le e^{\Lambda j_*}.}
 \tag{5.2}
\]

Define \(\mathfrak L_{\Lambda,\mathrm{loc}}^{3\to2}(T)\) by the same
formula (5.1), with \(\|h\|_{H^3}\) in the denominator.  Using the R0.73M
launch estimate \(\|\phi_\Lambda\|_{H^3}\le C_H\Lambda^2\), it obeys

\[
 \frac{c_*}{C_H}\Lambda^{-2}e^{\Lambda\mathcal A_*}
 \le\mathfrak L_{\Lambda,\mathrm{loc}}^{3\to2}(T_*)
 \le e^{\Lambda j_*}.
 \tag{5.3}
\]

Indeed, at any fixed \(0<\rho\le\rho_0\), define

\[
 \mathcal E_\rho:=
 \{\overline U_\Lambda(0),
 \overline U_\Lambda(0)+h_{\Lambda,\rho}:
 \Lambda\ge\Lambda_0\}\subset\mathcal D_{T_*}.
 \tag{5.4}
\]

The R0.73M input pairs have
\(H^3\) separation at most
\(C_H\rho\Lambda^2e^{-\Lambda\mathcal A_*}\to0\), while their output
\(L^2\) separation is at least \(c_*\rho\).  Thus the single
time-\(T_*\) Navier--Stokes flow map
\[
 S_{T_*}:(\mathcal E_\rho,\|\cdot\|_{H^3})
 \longrightarrow(H^3_{\sigma,0},\|\cdot\|_2)
\]
is not uniformly continuous.  Its local modulus at every individual
basepoint remains finite.  Equation (1.7) confirms that the energy upper
exponent is compatible with the selected-action lower exponent; no
sharpness or exponent equality is claimed.

## 6. Targets N7--N8: exact symmetry and compactness audit

The following candidate identifications must be checked algebraically:

1. amplitude-only multiplication;
2. time translation along one heat trajectory;
3. spatial translation, rotation, and Galilean transformation;
4. parabolic Navier--Stokes scaling;
5. a \(\Lambda\to\infty\) compactness limit;
6. embedding infinitely many active blocks into one smooth periodic shear.

An admissible transfer must preserve one viscosity, one periodic domain, one
forcing, one base trajectory, the initial \(H^3\) topology, and the observed
\(L^2\) distance.  A map that changes any of these is not a proof of (2.3).

## 7. Proof obligations

| ID | Obligation | Required evidence |
|---|---|---|
| N1 | exact perturbation relative-energy identity | continuum integration by parts; no linearization or truncation |
| N2 | explicit finite all-time strain | exact two-mode formula and analytic integration |
| N3 | fixed member has a positive planar stability radius | N1 plus exact planar global regularity |
| N4 | fixed member has a positive full 3D \(H^3\) tube | periodic commutator estimate, bootstrap, and continuation |
| N5 | family sensitivity has a two-sided exponential bracket | R0.73M lower theorem plus N1 upper bound; no equality of exponents |
| N6 | \(j_*>\mathcal A_*\) | strict exponential Taylor bound and rational comparison |
| N7 | no exact symmetry turns the family into one member | direct transformation formulas including domain and norm bookkeeping |
| N8 | no compactness or infinite-block shortcut | explicit norm divergence and Sobolev/Fourier obstruction |
| N9 | literature boundary | bounded primary-source audit of Lyapunov, transient, forced, and family-level notions |

## 8. Mandatory stop conditions and forbidden shortcuts

- Do not exchange \(\forall\Lambda\) with a fixed-background quantifier.
- Do not call a finite but large amplification factor Lyapunov instability.
- Do not require the escape time in (2.3) to equal \(T_*\); N1 must control
  all times before closing the no-go.
- Do not claim full three-dimensional Lyapunov stability from the \(L^2\)
  estimate alone; N2 must first close global strong continuation.
- Do not rename the full-3D \(H^3\)-input/\(L^2\)-observation corollary as
  FPS \((H^3,L^2)\) stability.
- Do not use weak-solution existence to claim \(H^3\) stability.
- Do not call amplitude multiplication a symmetry of the nonlinear
  perturbation equation merely because the shear background has zero
  self-advection.
- Do not use parabolic scaling without tracking the torus, frequencies,
  observation time, and \(H^3\) norm.
- Do not infer an optimal stability radius or a sharp upper exponent.
- Do not infer stability of arbitrary unforced backgrounds.
- Do not infer absence of high-Sobolev growth, vortex stretching,
  finite-time singularity, or a Clay conclusion.

## 9. Exact claim boundary if N1--N9 pass

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
amplitudeOnlyIdentificationIsNSSymmetry=FALSE
timeTranslationIdentifiesLambdaFamily=FALSE
parabolicScalingIdentifiesLambdaFamilyOnFixedTorus=FALSE
optimalFixedMemberStabilityRadius=OPEN
sharpFamilyLipschitzExponent=OPEN
arbitraryFixedBackgroundInstability=OPEN
transverseCriticalNormGrowth=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
```

The intended result is a rigorous route correction: R0.73M measures
nonuniform sensitivity across an unbounded family of globally smooth
backgrounds.  It cannot be converted into one-background Lyapunov
instability within the same unforced periodic topology.
