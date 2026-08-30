# R0.73N literature audit: fixed trajectories, parameter families, and transient growth

**Status:** bounded two-wave primary-source audit and internal
claim-boundary reconciliation PASS

**Search date:** 2026-08-31 (Asia/Shanghai)

**Scope:** definitions and theorems that could affect the attempted transfer
from the R0.73M varying-background family to Lyapunov instability of one
fixed unforced Navier--Stokes trajectory

## 1. Direct literature decision

No checked source turns a parameter-dependent family with unbounded finite
gain into Lyapunov instability of one fixed member.  The closest sources
separate into five classes:

1. autonomous spectral instability of one fixed, generally forced steady
   solution;
2. high-order instability constructions for singularly parameterized
   approximate-solution families, sometimes with small forcing;
3. transient or threshold growth whose gain becomes large only in a
   singular parameter limit;
4. non-autonomous shear results that either assume spectral stability along
   the full path or stop at a frozen Rayleigh spectral transition;
5. stable-side results for fixed Couette or decaying periodic shear
   geometries with hypotheses different from the R0.73M family.

The R0.73N fixed-member \(H^3\) stability tube is not imported from any of
these papers.  It is an internal continuum theorem obtained by a direct
relative-energy, periodic commutator, bootstrap, and continuation argument
for the explicit unforced heat shear.  External literature fixes the
definitions, supplies neighboring precedents, and prevents mislabeling.

This is a bounded source audit.  It is neither an exhaustive literature
classification nor a novelty, first-result, or priority claim.

## 2. The Friedlander--Pavlović--Shvydkoy convention

Friedlander, Pavlović, and Shvydkoy define \((X,Z)\) nonlinear stability of
one fixed equilibrium \(U_0\) by the following order:

\[
 \forall\rho>0\quad\exists\delta>0:
 \quad v_0\in X,\quad \|v_0\|_Z<\delta
 \Longrightarrow
 \left\{
 \begin{array}{l}
 v\in C([0,\infty);X)\text{ is a global solution},\\
 \|v(t)\|_Z<\rho\text{ for almost every }t\ge0.
 \end{array}\right.
 \tag{2.1}
\]

- S. Friedlander, N. Pavlović, and R. Shvydkoy,
  [*Nonlinear instability for the Navier--Stokes equations*](https://arxiv.org/html/math/0508173v1),
  Communications in Mathematical Physics 264 (2006), 335--347;
  [journal DOI](https://doi.org/10.1007/s00220-006-1526-7).

The roles of \(X\) and \(Z\) are consequential.  The condition
\((H^3,L^2)\) in this convention means that the perturbation is \(H^3\)
regular but is required to be small only in \(L^2\); the solution must remain
global in \(H^3\), and the observed distance is \(L^2\).  It does **not**
mean that the initial perturbation is small in \(H^3\) and only the output is
measured in \(L^2\).

Accordingly, the R0.73N conclusions must be separated as follows.

1. In the full three-dimensional phase space, the internal proof gives
   FPS-style \((H^3,H^3)\) stability for every fixed \(\Lambda\).
2. The same theorem implies the custom mixed-topology corollary
   \(H^3\)-small input \(\Rightarrow L^2\)-small synchronized output.  This
   is denoted \(H^3\)-in/\(L^2\)-out below and is not written as an FPS pair.
3. In the invariant planar subsystem, two-dimensional global regularity and
   the relative \(L^2\) estimate give genuine FPS-style
   \((H^3_{\mathrm{pl}},L^2_{\mathrm{pl}})\) stability.
4. Full-three-dimensional FPS \((H^3,L^2)\) stability is **OPEN**.  The
   present proof does not control arbitrary \(H^3\)-regular perturbations
   that are small only in \(L^2\) but may be large in \(H^3\).

The distinction between “almost every \(t\)” in the source and a strict
supremum bound is immaterial after the usual margin adjustment
\(\rho=\epsilon/2\) and continuity in the observation norm.  The distinction
between the \(X\)- and \(Z\)-smallness quantifiers is not immaterial.

FPS also note that failure of the required global \(X\)-solution is itself a
branch of Lyapunov instability.  A fixed-distance escape statement is
therefore only the global-solution branch of the logical negation, not the
entire negation.

## 3. From an equilibrium to a fixed trajectory

FPS Definition 2.1 is stated for a smooth steady equilibrium and an
autonomous linearized generator.  The R0.73N background
\(\overline U_\Lambda(t)\) is a nonstationary solution of the autonomous
Navier--Stokes equation.  The exact adaptation used here is:

> forward synchronized stability of the trajectory through
> \(\overline U_\Lambda(0)\), with the initial time fixed at \(t_0=0\).

The perturbed and reference solutions are compared at the same physical
time.  No phase shift or distance to the orbit as a set is allowed.  This is
not orbital stability, and the definition does not assert uniformity over
all possible starting times along the trajectory.

The FPS quantifier pattern is adopted, but FPS do not prove a theorem for
this time-dependent trajectory.  Any stability or instability conclusion
for \(\overline U_\Lambda(t)\) must therefore come from the internal
non-autonomous estimates.

## 4. Autonomous spectral transfer does not apply

FPS Theorem 2.2 assumes one smooth steady solution \(U_0\), one fixed
forcing, and one autonomous linearized operator whose spectrum enters the
open right half-plane.  It then transfers spectral instability to nonlinear
\((L^q,L^p)\) instability for \(q>\max\{p,n\}\).

Their escape time is chosen through a relation of the form
\(\epsilon e^{\lambda t_\epsilon}=\mathrm{constant}\), and hence grows as
the initial size vanishes.  This confirms two separate points:

- continuity of a fixed-time solution map does not rule out Lyapunov
  instability;
- an instantaneous or frozen unstable spectrum is not enough for a
  non-autonomous trajectory whose unstable window and total action are
  finite.

The R0.73N finite-total-strain estimate controls all future times on the
common strong lifespan.  That internal estimate, not FPS spectral theory,
is what closes the route-specific fixed-member statement.

## 5. Family-level Grenier constructions use different quantifiers

Desjardins and Grenier formulate instability relative to a family of
approximate solutions \(u_\varepsilon^{\mathrm{app}}\).  Exact solutions
start within an arbitrarily high algebraic order of that family and
separate at a parameter-dependent time under additional growth and
resolvent hypotheses.

- B. Desjardins and E. Grenier,
  [*Linear instability implies nonlinear instability for various types of
  viscous boundary layers*](https://numdam.org/item/AIHPC_2003__20_1_87_0/),
  Annales de l'Institut Henri Poincaré C 20 (2003), 87--106;
  [journal DOI](https://doi.org/10.1016/S0294-1449%2802%2900009-4).

Grenier's earlier high-order constructions concern Euler and Prandtl
instability:

- E. Grenier,
  [*On the nonlinear instability of Euler and Prandtl equations*](https://doi.org/10.1002/1097-0312%28200009%2953%3A9%3C1067%3A%3AAID-CPA1%3E3.0.CO%3B2-Q),
  Communications on Pure and Applied Mathematics 53 (2000), 1067--1091.

Grenier and Nguyen give a boundary-layer instability theorem in a singular
viscosity regime:

- E. Grenier and T. T. Nguyen,
  [*\(L^\infty\) instability of Prandtl layers*](https://arxiv.org/abs/1803.11024),
  Annals of PDE 5 (2019), article 18;
  [journal DOI](https://doi.org/10.1007/s40818-019-0074-3).

These are legitimate family-level or boundary-layer instability
precedents.  Their parameter, boundary, approximate-solution, and in some
nearby formulations small-forcing hypotheses do not identify their
background family with one fixed member of the exact unforced periodic
R0.73M equation.

## 6. Transient and threshold growth are not Lyapunov instability

Li, Masmoudi, and Zhao prove a sharp small-viscosity threshold and transient
exponential growth near Couette flow:

- H. Li, N. Masmoudi, and W. Zhao,
  [*A dynamical approach to the study of instability near Couette flow*](https://arxiv.org/abs/2203.10894),
  Communications on Pure and Applied Mathematics 77 (2024), 2863--2946;
  [journal DOI](https://doi.org/10.1002/cpa.22183).

The perturbation scale and gain are organized through \(\nu\to0\).  For one
fixed positive viscosity, that certificate does not by itself give the
\(\forall\delta\) fixed-distance quantifier for one background.  This is
the same logical distinction as finite gain at each fixed \(\Lambda\)
versus unbounded pointed gain as \(\Lambda\to\infty\).

Trefethen, Trefethen, Reddy, and Driscoll give the classical non-normal
linear distinction: spectrally stable dynamics can have very large but
finite transient amplification and later decay.

- L. N. Trefethen, A. E. Trefethen, S. C. Reddy, and T. A. Driscoll,
  [*Hydrodynamic stability without eigenvalues*](https://doi.org/10.1126/science.261.5121.578),
  Science 261 (1993), 578--584.

This source licenses the terminology distinction only.  Its linear and
model-based discussion is not evidence for the nonlinear R0.73N theorem.
Large finite amplification at a fixed parameter is compatible with
Lyapunov stability because the admissible initial radius can shrink by the
same finite factor.

## 7. Exact evolving and periodic shears do not conflict

Li and Zhao prove nonlinear asymptotic stability for heat-evolving monotone
shears under hypotheses including spectral stability along the relevant
full path:

- H. Li and W. Zhao,
  [*Asymptotic stability in the critical space of 2D monotone shear flow in
  the viscous fluid*](https://arxiv.org/abs/2306.03555), 2023.

Their monotonicity and full-path Rayleigh hypotheses do not cover the
periodic two-harmonic R0.73M background.  The paper nevertheless confirms
that a frozen operator cannot replace an evolution-family estimate.

Li and Zhao also construct a boundary-free heat-evolving shear whose frozen
inviscid Rayleigh operator passes from no point spectrum to an unstable
eigenvalue:

- H. Li and W. Zhao,
  [*Viscosity driven instability of shear flows without boundaries*](https://arxiv.org/abs/2410.23798),
  2024.

Their result is a frozen Rayleigh spectral transition.  The corresponding
exact-unforced nonlinear growth is explicitly left as a further challenge,
so it neither proves nor contradicts the R0.73N fixed-trajectory theorem.

Lin and Xu prove metastability and rapid decay of the non-shear part of
perturbations near periodic Kolmogorov flows, including a nonlinear result
at a viscosity-dependent vorticity scale:

- Z. Lin and M. Xu,
  [*Metastability of Kolmogorov flows and inviscid damping of shear flows*](https://arxiv.org/abs/1707.00278),
  Archive for Rational Mechanics and Analysis 231 (2019), 1811--1852;
  [journal DOI](https://doi.org/10.1007/s00205-018-1311-8).

This is a stable-side periodic decaying-shear comparison.  Its geometry,
norms, spectral structure, and threshold do not prove the explicit
R0.73N \(H^3\) tube.  It is consistent with, but not provenance for, that
internal theorem.

## 8. Forced steady benchmarks are a different equation

Classical Kolmogorov instability concerns a stationary solution maintained
in a fixed-equilibrium setting:

- L. D. Meshalkin and Ya. G. Sinai,
  [*Investigation of the stability of a stationary solution of a system of
  equations for the plane movement of an incompressible viscous liquid*](https://doi.org/10.1016/0021-8928%2862%2990149-1),
  Journal of Applied Mathematics and Mechanics 25 (1961), 1700--1705.

Plane Couette flow provides a classical fixed steady benchmark:

- V. A. Romanov,
  [*Stability of plane-parallel Couette flow*](https://doi.org/10.1007/BF01078886),
  Functional Analysis and Its Applications 7 (1973), 137--146.

Forcing, a pressure gradient, or moving walls can maintain a nondecaying
steady background for which autonomous spectral theory is appropriate.
Those changes alter the equation or boundary-value problem and cannot be
silently imported into the unforced periodic R0.73N trajectory.

## 9. Internal theorem provenance and local strong theory

For every fixed \(\Lambda\), the positive three-dimensional \(H^3\) tube is
supported by the R0.73N energy and bootstrap calculation itself.  Its
support class is:

~~~text
internal continuum theorem
~~~

and not:

~~~text
external literature inference
~~~

Classical local strong well-posedness and continuation theory may be cited
as background for the final continuation step:

- H. Fujita and T. Kato,
  [*On the Navier--Stokes initial value problem. I*](https://doi.org/10.1007/BF00276188),
  Archive for Rational Mechanics and Analysis 16 (1964), 269--315.

This citation does not supply the finite-strain radius, the relative
estimate, or stability of the present orbit.  Those claims remain internal.
The periodic \(H^3\) commutator estimate must also be presented consistently
with the selected Sobolev norm; a standard estimate may justify the tool,
but not the theorem-specific conclusion.

## 10. Quantifier and flow-map boundary

R0.73M proves

\[
 \exists\rho_0,c_*,\Lambda_0\quad
 \forall\Lambda\ge\Lambda_0\quad
 \forall\rho\in(0,\rho_0]
 \tag{10.1}
\]

with a different base \(\overline U_\Lambda\) for each \(\Lambda\).  For
fixed \(\rho\), the selected \(H^3\) input vanishes as
\(\Lambda\to\infty\), while the endpoint remains at least \(c_*\rho\).
For fixed \(\Lambda\), sending \(\rho\to0\) sends both the input and the
licensed lower-bound scale \(c_*\rho\) to zero.  No quantifier exchange
produces a fixed member.

The autonomous Navier--Stokes equation has one time-\(T_*\) solution map
\(S(T_*)\), not a different solution map for each \(\Lambda\).  The precise
family is the collection of pointed perturbation maps

\[
 F_\Lambda(h)
 :=S(T_*)(\overline U_\Lambda(0)+h)
   -S(T_*)\overline U_\Lambda(0).
 \tag{10.2}
\]

R0.73M gives exponentially growing lower bounds for their pointed
amplification and consequently failure of equicontinuity at \(h=0\) across
the unbounded family.  Alternatively, it shows failure of uniform
continuity of the single flow map on a planar data set containing the
selected pairs.  The binary failure of equicontinuity itself is not assigned
an exponential rate.

## 11. Search boundary and stop rule

The first search wave covered the FPS definition, autonomous
spectral-to-nonlinear transfer, transient growth, Couette thresholds, and
evolving shears.  The second wave targeted Grenier family quantifiers,
boundary-layer theorems, periodic decaying Kolmogorov flow, forced steady
benchmarks, and classical strong-solution provenance.

The search stopped because:

- the topology and quantifier conventions are fixed by a primary source;
- every consequential neighboring theorem has an explicit mismatch;
- no checked source replaces the internal finite-strain proof;
- further generic searches were unlikely to alter the claim boundary.

The absence statement is strictly limited to the recorded sources and
searches.  It must not be used to claim absolute novelty or priority.

## 12. Evidence-supported wording

Subject to the remaining internal analytic and publication gates, the
strongest admissible wording is:

> The R0.73M construction gives exponentially growing pointed amplification
> and consequent non-equicontinuity across an unbounded family of exact
> unforced planar backgrounds.  A direct R0.73N energy and bootstrap theorem
> gives every fixed member a positive full-three-dimensional FPS-style
> \((H^3,H^3)\) stability tube, together with an
> \(H^3\)-in/\(L^2\)-out corollary.  In the invariant planar subsystem the
> relative \(L^2\) estimate and two-dimensional global regularity give
> FPS-style \((H^3_{\mathrm{pl}},L^2_{\mathrm{pl}})\) stability.  This blocks
> the proposed fixed-member inference without asserting full-three-
> dimensional FPS \((H^3,L^2)\) stability.

The following wording is not supported:

- “R0.73M already proves Lyapunov instability of one fixed background”;
- “full-three-dimensional FPS \((H^3,L^2)\) stability is closed”;
- “\((H^3,H^3)\) hence \((H^3,L^2)\)” when FPS pair notation is intended;
- “large transient gain is equivalent to Lyapunov instability”;
- “a frozen unstable eigenvalue proves instability of the evolving orbit”;
- “the fixed-member theorem follows from FPS, Lin--Xu, or Couette theory”;
- “the bounded audit proves a first or priority result”;
- “the no-go applies to every Navier--Stokes background”;
- “fixed-member stability rules out high-norm growth or singularity”;
- “R0.73N resolves any part of the Clay alternative.”
