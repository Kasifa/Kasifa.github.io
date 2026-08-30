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
| `unitRealDuhamelCoefficientSweep` | FINITE_ARCHIVED | 319 endpoint/snapshot rows and 29 raw NPZ members in `research/certificates/r073h/` | not a continuum coefficient theorem |
| `genericFourierLerayCrossCheck` | FINITE_ARCHIVED | primary harmonic formulas checked against a generic Fourier--Leray convolution kernel | validates finite algebra/code only |
| `aliasFreeFFTIndependentSentinels` | FINITE_ARCHIVED | four preregistered formal physical-grid sentinels plus one independently recomputed holdout; maximum coefficient relative error \(2.0164\times10^{-9}\) | not a tail enclosure |
| `quadraticCubicCompensatedScaling` | FINITE_ARCHIVED | at \(d=0.01\), frozen-grid natural-log slopes \(0.9876043\) and \(1.9532335\); blind holdout compensated ratios \(0.9250135\) and \(0.8849248\) | not a \(\Lambda\to\infty\) limit proof and not the theorem endpoint \(d=D\le1/450\) |
| `signedCubicFeedback` | FINITE_ARCHIVED | blind holdout total signed compensated projection \(-0.6597415\), inside the preregistered interval \([-0.72,-0.58]\) | the finite cubic sign is profile/cutoff-specific and does not determine full nonlinear feedback after higher orders |

The sealed package contains 21 cutoff comparisons and six step comparisons.
Every finite response ratio quoted in this matrix uses
\(d=0.01>1/450\), outside the
continuum-theorem interval.  These values diagnose the frozen harmonic code
path and cannot be identified with the theorem endpoint \(d=D\).
The independent validator recomputes all NPZ endpoint observables and reports
a maximum relative discrepancy of \(1.043\times10^{-15}\).  The six step
rows do not have raw step endpoints in the NPZ archive; for that subset the
independent check is limited to the locked producer, the CSV internal maximum
and threshold, and the package hashes.  This limitation is recorded in both
`validation.json` and the certificate README.

## 4. Open statements

| Key | Status | What is still required |
|---|---|---|
| `sharpSelectedGainAction` | OPEN | matching upper/lower asymptotics for \(G_\Lambda\) on the selected bundle |
| `prescribedLowerLawSeedDeparture` | OPEN | harmonic-resolved estimates tied to the chosen lower-law seed rather than the actual gain |
| `uniformTaylorRadiusAtNaturalEndpoint` | OPEN | all-order Taylor control for the prescribed lower-law seed, uniform in large \(\Lambda\) |
| `fullContinuumHarmonicResolvedSemigroupEstimate` | OPEN | a general operator/tail theorem beyond the selected-orbit cumulative-energy argument used here |
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
