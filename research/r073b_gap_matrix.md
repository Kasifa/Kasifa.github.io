# R0.73B claim--evidence--gap matrix

**Frozen:** 2026-08-29

**Release state:** independent analytic audit passed after all required scope
edits.  Deterministic certificate, formal figure, bilingual/PDF build, and
live-deployment gates remain required.

| Claim key | Source-stage status | Analytic evidence | Deterministic evidence | Publication boundary |
|---|---|---|---|---|
| `exactBlochNearCarrierCancellation` | ANALYTIC PASS; CERT PENDING | report Sec. 2 and independent audit Sec. 1 | exact Fourier-matrix identity planned | \(\mu>0\); chosen zero-lattice carrier is not unique at the Bloch endpoint |
| `exactBlochCarrierSystem` | ANALYTIC PASS; CERT PENDING | report Eq. (2.7), independent sign audit | raw versus transformed generator similarity planned | homogeneous coupling regular; forcing mean pays \(g^{-1}\) |
| `boundedBlochOrientationCoefficient` | ANALYTIC PASS; CERT PENDING | \(2|\gamma\beta|\le g\) | parameter-grid check planned | pays \(|\Lambda|\), not a zero cost |
| `blochNearCarrierFiniteTransient` | ANALYTIC PASS; CERT PENDING | report Sec. 3, independent constant ledger | finite rows below envelope planned | \(\mu>0\), \(0<g\le1\), \(F_q=0\); hybrid norm and viscous rate only |
| `exactHeatShearGradientPrimitive` | ANALYTIC PASS; CERT PENDING | \(L^\infty\) maximum attained at \(x=\pi\) | symbolic/point check planned | exact only for the frozen two-harmonic heat path |
| `completePhysicalKineticFiniteTransient` | ANALYTIC PASS; CERT PENDING | report Secs. 4--5, independent energy audit | finite propagator rows below envelope planned | linearized component equation; exponential \(|\Lambda|\) prefactor |
| `completeOSSquireKineticFiniteTransient` | ANALYTIC PASS; CERT PENDING | exact R0.72Y recovery plus independent component audit | OS--Squire/velocity similarity check planned | \(\mu>0\) in OS--Squire coordinates; exceptional rows use components |
| `blochUniformPhysicalVelocityDirectSumAtViscousRates` | ANALYTIC PASS; CERT PENDING | finite partial sums, monotone convergence, Parseval | row grid only, not proof | discrete periodic direct sum; no enhanced rate |
| `physicalKineticForcedDuhamel` | ANALYTIC PASS; CERT PENDING | variation of constants with projected physical forcing | kernel checks planned | arbitrary unweighted \((F_q,F_\eta)\) excluded |
| `sharpKineticShearFormCoefficientAndLowGapLimit` | ANALYTIC PASS; CERT PENDING | kinetic-form note and independent tail-block proof | banded operator checks planned | two-dimensional physical OS row; logarithmic coefficient, not exact gain |
| `nearCarrierInstantaneousKineticGrowth` | ANALYTIC PASS; CERT PENDING | exact carrier--tangent plane and sign criterion | symbolic condition check planned | fixed nonzero \(\Lambda\), sufficiently small \(\mu\) |
| `lambdaIndependentKineticPrefactor` | ANALYTICALLY FALSE; CERT PENDING | exact zero-row lift-up solution | finite gain scaling planned | rules out only \(\Lambda\)-independent all-row prefactors |
| `allRowPrefactorOneKineticContraction` | ANALYTICALLY FALSE; CERT PENDING | lift-up and positive carrier--tangent logarithmic growth | fixed-\(\Lambda\) triangular limit planned | finite transient remains bounded; it is not a contraction |
| `fixedCUniformLowGapKineticPropagator` | ANALYTICALLY FALSE; CERT PENDING | continuity lemma gives \(\mu^{-1/2}\) output | fitted divergence exponent planned | fixed \(c\ne0\) means \(|\Lambda|=|c|/\sqrt\mu\to\infty\) |
| `polynomiallySharpLambdaKineticPrefactor` | OPEN | linear lower bound versus exponential upper bound | finite values cannot close asymptotic sharpness | no matching upper/lower dependence |
| `completeOSSquireA2DirectSum` | OPEN | viscous-rate energy only | excluded | no collision-uniform enhanced-dissipation rate |
| `transportedAdjointPressureA2Modulation` | OPEN | R0.73A dual obstruction remains relevant | excluded | not needed for the present viscous-rate theorem |
| `nonlinearNavierStokes` | OPEN | no nonlinear convolution or bootstrap | excluded | vortex stretching and scale interactions remain |
| `Clay` | OPEN | no global regularity or singularity theorem | excluded | Millennium problem untouched |

## Publication rule

Every positive claim must retain its norm, parameter path, row scope, decay
rate, and transient prefactor.  Every negative claim must retain its explicit
witness.  Finite Fourier computations screen and reproduce the theorem but
do not replace the infinite-dimensional energy proof.  Section counters
measure archived research notes, not percentage progress toward the Clay
problem.
