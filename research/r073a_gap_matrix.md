# R0.73A claim--evidence--gap matrix

**Frozen:** 2026-08-29

**Release state:** analytic derivations and both independent audits complete;
all required scope edits applied.  Formal certificate, figure, bilingual,
PDF, publication, and live-deployment gates remain pending.

| Claim key | Source-stage status | Analytic evidence | Deterministic evidence | Publication boundary |
|---|---|---|---|---|
| `exactPhysicalMeanOSCancellation` | CLOSED | Report Sec. 2, exact periodic integration by parts | exact Fourier coefficient identity for every active shift | beta=xi=0; mu=gamma^2 in (0,1] |
| `exactMeanVelocityZeroMeanVorticitySystem` | CLOSED | Report Secs. 2--3, q=mu h+r projection | entrywise raw-q versus transformed-matrix similarity | no Squire variable |
| `renormalizedPhysicalLongWaveOSTransientPropagator` | CLOSED | Report Sec. 4, logarithmic norm and Gronwall | direct deterministic propagator grid lies below the analytic envelope | X_mu norm and viscous rate only |
| `renormalizedPhysicalLongWaveOSForcedDuhamel` | CLOSED | Report Sec. 5, variation of constants | kernel and forcing-coordinate ledger | mean forcing pays mu^-1 |
| `exactPhysicalTangentLiftedLineNoninvariance` | CLOSED | Report Sec. 6, positive-gap hidden-mean derivative | exact finite-mu coefficients; path-qualified mu-to-zero limit | noninvariance holds for each c_mu nonzero; fixed Lambda raw-q limit remains undecided |
| `exactMovingTangentQuotientAlgebra` | CLOSED | Report Sec. 7, general Hilbert-space identities | finite Fourier algebra is illustrative only | abstract gapless OS row; strong/domain-compatible statement |
| `orthogonalTangentProjectionSpeed` | CLOSED | Report Sec. 8, exact omega=3r/(1+r^2) | exact coefficient spot checks | kinematic statement only |
| `explicitOrthogonalTangentBlocks` | CLOSED | Report Sec. 8, explicit zeta and G | four Fourier coefficients independently checked | nonzero cG block remains |
| `rankOneAbstractTangentClosesPhysicalLongWaveLimit` | FALSE, lifted-line meaning | Report Sec. 6, positive-gap noninvariance | exact hidden-mean derivative; path-qualified limit sequence | not failure of q*=Wxx or of general moving quotient algebra |
| `fixedTwoHarmonicOSInvariance` | FALSE for c != 0 | Report Sec. 9, exact leakage and return formulas | finite matrix compressions consistent | at c=0 the heat generator preserves the carrier |
| `twoSidedInvariantOrthogonalTangentSplit` | FALSE | Report Secs. 7--8, nonzero dual defect | explicit nonzero zeta/G coefficients | transported dual remains possible but anti-parabolic |
| `uniformlyBoundedPositiveGapTangentDualPressureBlock` | FALSE, unweighted | Report Sec. 10, forced constant coefficient 1/g | finite small-gap dual spot checks | fixed d or compact d interval with inf norm(phi)>0; this is the unscaled pressure block, while the OS block carries abs(c); weighted theorem not excluded |
| `frozenLowWaveRowsAutomaticallyStable` | CONTRADICTED AS A GENERAL ASSUMPTION | stationary long-wave specialization, Report Sec. 11 | 419/448 unprojected broad cases have positive finite edge | finite sweep is not an operator theorem |
| `fixedLowModeCompressionUniformlyStabilizesFrozenScreen` | NEGATIVE IN DECLARED FINITE SWEEP | exact noninvariance explains the failure | Wxx deletion worsens 141/448; two-mode deletion worsens 111/448 | compression Q*AQ is not an invariant quotient |
| `stableFrozenCompressionNeedsNoTransientPrefactor` | NEGATIVE IN DECLARED FINITE SWEEP | nonnormality literature boundary | stable target T05 has sampled gain 2.054 and Kreiss lower bound 1.550 | sampled finite diagnostic only |
| `rawL2qUniformLowGapTransientPrefactor` | OPEN | no rigorous singular-family theorem | excluded from certificate conclusion | generator blow-up alone is insufficient |
| `lowGapOSTransientA2Propagator` | OPEN | no A2-rate proof | excluded | new theorem has only rate mu |
| `lowGapPhysicalKineticPropagator` | OPEN | exact norm mismatch in Report Sec. 13 | weighted singular values not certified | X_mu is not uniformly equivalent |
| `generalBlochLowGapOSPropagator` | OPEN | beta-dependent physical modulation absent | excluded | positive-gap g^-1 obstruction must be weighted |
| `lowGapOSSquirePropagator` | OPEN | R0.72Z history not coupled to X_mu | excluded | lift-up and orientation remain |
| `BlochUniformPhysicalVelocityDirectSum` | OPEN | no beta, xi, gamma summation | excluded | no complete kinetic row sum |
| `nonlinearNavierStokes` | OPEN | no nonlinear convolution or bootstrap | excluded | vortex stretching remains |
| `Clay` | OPEN | no global regularity or breakdown theorem | excluded | Millennium problem untouched |

## Publication rule

Every positive statement must retain its norm, physical row, parameter
range, and decay rate.  Every false statement must retain the precise
witness and scope.  The finite spectral sweep must remain labelled as a
Galerkin diagnostic without a tail theorem.  OPEN entries must not be
described as nearly proved, and release counters measure archived sections,
not progress toward the Clay problem.
