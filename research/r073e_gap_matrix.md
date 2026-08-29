# R0.73E gap matrix

**Date:** 2026-08-30
**Purpose:** bind the fixed-positive-half-plane, relative-dichotomy, and
logarithmic-transfer claims to their exact evidence while preventing a
one-row linear theorem from being extended to the full nonlinear problem.

| ID | statement | state | evidence | exact boundary or next gate |
|---|---|---|---|---|
| E1 | every admissible fixed half-plane \(\operatorname{Re}z\ge b>0\) contains only the viscous continuations of the finitely many inviscid clusters | CLOSED | compact Fredholm convergence on the bounded core plus uniform high-imaginary and high-real-part resolvent estimates | \(\forall b>0\,\exists\varepsilon_b\); no uniformity as \(b\downarrow0\) |
| E2 | the total right-of-\(b\) Riesz projection converges in operator norm and preserves algebraic multiplicity | CLOSED | analytic base integral vanishes; compact sandwich converges in norm using strong and adjoint-strong base resolvents | does not identify individual eigenvalues as simple or rightmost |
| E3 | the extended reduced resolvent is uniformly bounded on the whole fixed half-plane | CLOSED | invariant Riesz decomposition, analytic reduced part, maximum principle on cluster disks, and noncompact resolvent splice | the object at a projected eigenvalue is the complement-part resolvent, not the full resolvent |
| E4 | the finite spectral block \(B_\varepsilon\Pi_{\varepsilon,b}\) converges in operator norm | CLOSED | contour functional calculus after subtracting the analytic base term | no quantitative rate or explicit viscosity threshold |
| E5 | the complete inviscid top cluster exists, is finite, and has a strict complementary spectral gap | CLOSED | compact spectrum, positive certified eigenvalue, discreteness in the open right half-plane, and isolation of the finite top set | the certified \(\sigma_*\) is not proved rightmost |
| E6 | the viscous top cluster has a uniform relative exponential dichotomy | CLOSED | whole-line reduced resolvent, analytic-semigroup Bromwich shift, integration by parts, common short-time bound, and finite-block inverse group | the unshifted complement may grow; absolute decay is not claimed |
| E7 | the frozen full semigroup obeys \(\|e^{tB_\varepsilon}\|\le C_\delta e^{(a+\delta)t}\) | CLOSED | top-block contour bound plus the smaller complement exponent | \(C_\delta\) may diverge as \(\delta\downarrow0\) |
| E8 | the exact heat-profile drift transfers a top viscous eigenmode through \(T_\varepsilon=M\log(1/\varepsilon)\) for every fixed \(M>0\) | CLOSED | explicit \(49/4\) bounded-drift estimate and fixed-generator Duhamel--Gronwall argument | no moving Riesz projection, adiabatic transport, or fixed-window exponential law is proved |
| E9 | the exact \(\gamma=1/2\) row gain dominates every fixed power of \(|\Lambda|\) on every fixed observation window | CLOSED | logarithmic lower rate, observation-window supremum, both-sign conjugation, and exact \(\beta=\xi=0\) OS--Squire embedding | this excludes polynomial upper bounds that must cover the row; it does not prove the full \(A_2\) direct sum |
| E10 | removing only the selected finite leading cluster leaves another finite unstable pair | FINITE DIAGNOSTIC | \(N=24,48,96\), five viscosities, independent contour/resolvent/semigroup recomputation | no continuum eigenpair or continuum spectral ordering follows |
| E11 | a fixed inviscid complement can suffer large long-time leakage into the moving leading cluster | FINITE DIAGNOSTIC | \(\|P_\varepsilon-P_0\|\approx3.09\times10^{-4}\) but the fixed-complement endpoint is about \(1.95\times10^{11}\) at the sampled row | sampled binary64 behavior only; no continuous-time or continuum bound |
| E12 | the complete OS--Squire \(A_2\) direct-sum estimate | OPEN | one invariant two-dimensional row is covered | pressure/Squire coupling and all collision rows remain |
| E13 | nonlinear Navier--Stokes regularity or blow-up | OPEN | no nonlinear mode-convolution closure | a separate nonlinear theorem is required |

## Release decision variables

```text
fixedPositiveHalfPlaneNoPollution=CLOSED
allModesRightOfBProjectionNormPersistence=CLOSED
topInviscidClusterExists=CLOSED
topViscousClusterPersistence=CLOSED
topReducedHalfPlaneResolventUniform=CLOSED
frozenTopClusterRelativeDichotomy=CLOSED
fixedFrozenGeneratorVolterraTransfer=CLOSED
logFastTimeTransfer=CLOSED
superPolynomialCompleteRowNoGo=CLOSED

certifiedSigmaStarIsRightmost=OPEN
selectedSigmaStarComplementDichotomy=OPEN
uniformHalfPlaneBoundAtBEqualsZero=OPEN
globalRightHalfPlaneNoPollution=OPEN
absoluteUniformComplementDecay=OPEN
explicitHalfPlaneGap=OPEN
explicitViscosityThreshold=OPEN
quantitativeEigenvalueRate=OPEN
movingProfileUniformContour=OPEN
graphDomainKatoTransport=OPEN
movingProfileEvolutionDichotomy=OPEN
inviscidRootUnique=OPEN
inviscidEigenvalueSimple=OPEN
completeOSSquireA2DirectSum=OPEN
fixedWindowExponentialLowerLaw=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

The analytic states above depend on the corrected proof and independent
analytic audit.  The finite experiment is deliberately unable to change any
continuum `OPEN` state.
