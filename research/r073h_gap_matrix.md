# R0.73H gap matrix

**Date:** 2026-08-30  
**Rule:** continuum theorem, exact finite subcertificate, and floating-point
diagnostic are recorded in separate columns

## 1. Closed analytic statements

| Key | Status | Evidence | Boundary |
|---|---|---|---|
| `exactHarmonicTaylorHierarchy` | CLOSED | `r073h_harmonic_derivation.md`, Sections 2--5 | support algebra only; it does not bound coefficient size |
| `targetHasNoQuadraticOrQuarticTerm` | CLOSED | parity induction in equation (5.3) | the next possible target correction is quintic, not necessarily nonzero |
| `continuumDoubledRowNumericalAbscissa` | CLOSED | gauge reduction, exact rational low block, analytic tail and time perturbation in `r073h_harmonic_energy_proof.md`, Section 3 | valid only on \(0\le d\le\min(d_0,1/450)\) |
| `localizedLinearCumulativeEnergy` | CLOSED | backward conorm plus physical kinetic identity | no pointwise \(H^1\) or uniform high-Sobolev claim |
| `localizedQuadraticCubicEnergy` | CLOSED | Ladyzhenskaya and Stieltjes localization, Sections 7.1--7.2 | constants are existential and profile-family specific |
| `fourthOrderExactRemainder` | CLOSED | Section 8 energy cancellation and product measures | only inside the exact planar subsystem |
| `gainNormalizedFixedDistanceDeparture` | CLOSED | target projection in Section 9 | seed is \(\delta/G_\Lambda\), not a prescribed sharp exponential law |
| `selectedOrbitGlobalSmoothness` | CLOSED | exact planar invariance plus 2D Navier--Stokes theory | global smoothness does not imply stability |

## 2. Exact false inferences

| Key | Status | Reason |
|---|---|---|
| `gainLowerBoundDeterminesActualGain` | FALSE_AS_INFERENCE | a lower bound on \(G_\Lambda\) supplies no matching upper action |
| `gainNormalizedDepartureImpliesPrescribedSeedDeparture` | FALSE_AS_INFERENCE | \(\delta/G_\Lambda\) may be exponentially smaller than \(\delta e^{-r\Lambda D}\) |
| `finiteCubicCoefficientProvesContinuumSaturation` | FALSE_AS_INFERENCE | a finite sign and magnitude do not control Fourier tails or higher Taylor orders |
| `familyDepartureIsSingleBackgroundLyapunovInstability` | FALSE_AS_INFERENCE | the background changes with \(\Lambda\) |
| `planarDepartureCreatesThreeDimensionalVortexStretching` | FALSE | the selected orbit stays in an exact two-dimensional invariant subspace |
| `planarDepartureImpliesFiniteTimeSingularity` | FALSE | every selected orbit is globally smooth |
| `planarDepartureResolvesClay` | FALSE | no transverse three-dimensional regularity or singularity alternative is addressed |

## 3. Finite diagnostics

| Key | Status | Planned/archived evidence | Prohibited interpretation |
|---|---|---|---|
| `unitRealDuhamelCoefficientSweep` | FINITE | `research/certificates/r073h/` primary arrays and endpoint tables | not a continuum coefficient theorem |
| `genericFourierLerayCrossCheck` | FINITE | direct convolution comparison | validates finite algebra/code only |
| `aliasFreeFFTIndependentSentinels` | FINITE | independent physical-grid implementation | not a tail enclosure |
| `quadraticCubicCompensatedScaling` | FINITE | log slopes and compensated plateaus over the frozen grid | not a \(\Lambda\to\infty\) limit proof |
| `signedCubicFeedback` | FINITE | mean, double, and total target projections | sign may depend on the profile and higher-order terms |

## 4. Open statements

| Key | Status | What is still required |
|---|---|---|
| `sharpSelectedGainAction` | OPEN | matching upper/lower asymptotics for \(G_\Lambda\) on the selected bundle |
| `prescribedLowerLawSeedDeparture` | OPEN | harmonic-resolved estimates tied to the chosen lower-law seed rather than the actual gain |
| `uniformTaylorRadiusAtNaturalEndpoint` | OPEN | control of all orders, or a direct nonlinear argument, uniform in large \(\Lambda\) |
| `singleBackgroundLyapunovSequence` | OPEN | a fixed smooth background and a sequence of perturbations for that same background |
| `transverseOSSquireEvolution` | OPEN | complete nonautonomous estimates with \(K_x\ne0\) or nonzero first velocity component |
| `transverseTriadClosure` | OPEN | three-dimensional harmonic and derivative-loss control after the OS/Squire step |
| `finiteTimeSingularity` | OPEN | no evidence in this release supports a singular orbit |
| `Clay` | OPEN | the global regularity versus singularity problem for arbitrary smooth 3D data remains untouched |

## 5. Next gate

The next mathematical fork should not return to the already closed planar
energy bookkeeping.  It should first determine which of the following is
feasible:

1. prove a matching action for \(G_\Lambda\), which would convert the
   gain-normalized seed into an explicit scale; or
2. introduce one transverse row and derive the exact nonautonomous
   Orr--Sommerfeld/Squire energy and triad system.

The two tasks may be screened in parallel, but neither may use the finite
cubic sign as a continuum hypothesis.
