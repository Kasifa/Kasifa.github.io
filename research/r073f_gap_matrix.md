# R0.73F gap matrix

**Date:** 2026-08-30  
**Purpose:** bind the moving-profile spectral and evolution claims to their
exact evidence, while keeping one-row linear amplification separate from the
nonlinear Navier--Stokes problem

| ID | statement | state | evidence | exact boundary or next gate |
|---|---|---|---|---|
| F1 | a uniform frozen exponential dichotomy survives a sufficiently small bounded nonautonomous perturbation even when the stable semigroup is not invertible | CLOSED | self-contained stable and unstable Lyapunov--Perron graph equations; contraction radius \(\rho<\nu/(16K^2)\) | the radius is conservative and depends on non-explicit R0.73E constants |
| F2 | the instantaneous generators \(\widetilde B_\varepsilon(d)\), \(0\le d\le d_0\), have a uniform spectral strip separating an \(m\)-dimensional unstable part | CLOSED | apply F1 to each constant profile perturbation; stable positive-time and unstable negative-time Laplace formulas give the strip and identify the graph projection with the Riesz split | only a sufficiently small existential \(d_0\) is obtained |
| F3 | one fixed contour defines all instantaneous unstable Riesz projections, and \(P_\varepsilon^{\rm inst}(d)\) is uniformly bounded and norm-\(C^1\) | CLOSED | strip on the left, dissipative/Neumann bounds on the other rectangle sides, fixed contour differentiation | no uniform map into unscaled \(H^2\) is claimed |
| F4 | the exact moving profile has a uniform dynamical evolution dichotomy on \(0\le d\le d_0\) | CLOSED | clamp extension, exact \((49/4)d\) bounded drift, and F1 with constants independent of \(\varepsilon\) and interval length \(d_0/\varepsilon\) | the dynamic projection need not equal the instantaneous Riesz projection |
| F5 | the moving unstable fiber starts exactly at the frozen top space | CLOSED | the perturbation extension is zero for all negative fast times, so the unstable graph integral at time zero vanishes | the initial top vector may depend on \(\varepsilon\) |
| F6 | at every physical endpoint \(0<d\le d_0\), the exact row gain is at least \(K_1^{-1}e^{(\alpha+\eta)d/\varepsilon}\) | CLOSED | inverse estimate on the moving unstable fiber and undoing the shift \(\alpha\) | endpoint growth at a prescribed \(d>d_0\) remains open |
| F7 | for every fixed observation window \(D>0\), \(G_{1/2}(\Lambda;D)\ge K_1^{-1}e^{(\alpha+\eta)\min(D,d_0)|\Lambda|}\) for both signs | CLOSED | take the admissible time \(\min(D,d_0)\), exact kinetic isometry, invariant \(\xi=0\) OS--Squire embedding, and conjugation | when \(D>d_0\), the lower bound is attained inside the window, not asserted at its endpoint |
| F8 | \(\log G_{1/2}(\Lambda;D)=\Theta(|\Lambda|)\) for every fixed \(D>0\) | CLOSED | F7 plus the R0.73B complete-row upper bound \(e^{5|\Lambda|/16}\) | the sharp exponent and existence of a normalized limit remain open |
| F9 | a frozen spectral gap, bounded \(C^1\) drift, and a common domain imply a uniform moving dichotomy | FALSE IN GENERAL | exact \(3\times3\) nonnormal block with gap growing like \(\varepsilon^{-1}\) but transient prefactor growing like \(\varepsilon^{-1}\) | R0.73E supplies the stronger uniform reduced-resolvent/semigroup input for the exact row |
| F10 | positive instantaneous spectral abscissa at every time implies fixed-window growth | FALSE IN GENERAL | exact normal \(4\times4\) crossing example with positive pointwise maximum but endpoint decay \(e^{-D/(4\varepsilon)}\) | a uniform backward estimate on the complete top bundle is sufficient |
| F11 | the complete OS--Squire \(A_2\) direct-sum estimate | OPEN | one invariant \(\gamma=1/2\) row has a lower and upper exponential order | pressure/Squire coupling and all collision rows remain |
| F12 | nonlinear Navier--Stokes regularity or blow-up | OPEN | no nonlinear mode-convolution or remainder closure | a separate nonlinear theorem is required |

## Release decision variables

```text
boundedPerturbationRoughnessWithNoninvertibleStableSemigroup=CLOSED
movingProfileUniformSpectralStrip=CLOSED
movingProfileUniformContour=CLOSED
movingInstantaneousProjectionNormC1=CLOSED
movingProfileEvolutionDichotomy=CLOSED
movingUnstableFiberStartsAtFrozenTopSpace=CLOSED
fixedSmallEndpointExponentialLowerLaw=CLOSED
fixedWindowExponentialLowerLaw=CLOSED
fixedWindowLogGainThetaLambda=CLOSED

frozenSpectralGapImpliesUniformDichotomy=FALSE
spectralGapPlusBoundedC1PlusCommonDomainImpliesMovingDichotomy=FALSE
instantaneousPositiveSpectralAbscissaImpliesFixedWindowGrowth=FALSE

explicitWindowSize=OPEN
sharpExponentialRate=OPEN
normalizedLogGainLimitExists=OPEN
arbitraryEndpointBeyondSmallWindow=OPEN
dynamicProjectionEqualsInstantaneousRieszProjection=OPEN
graphDomainKatoTransport=OPEN_NOT_USED
singleEpsilonIndependentInitialOrbit=OPEN
certifiedSigmaStarIsRightmost=OPEN
inviscidEigenvalueSimple=OPEN
completeOSSquireA2DirectSum=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

The `CLOSED` states depend on the R0.73E uniform frozen dichotomy.  The finite
diagnostics and counterexamples cannot change any continuum state.
