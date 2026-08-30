# R0.73G gap matrix

**Date:** 2026-08-30  
**Purpose:** identify exactly what the R0.73F one-row linear amplification
does and does not imply after restoring the quadratic Navier--Stokes term

| ID | statement | state | evidence | boundary or next gate |
|---|---|---|---|---|
| G1 | The \(R=2\), \(K_x=0\), \(K_z=\pm1\) realization is an exact perturbation problem around a smooth decaying Navier--Stokes shear. | CLOSED | Direct physical scaling and subtraction of the exact heat shear. | Only the selected conjugate row pair supplies the lower signal. |
| G2 | The real R0.73F seed and its full nonlinear evolution preserve \(u_1=0\) and \(\partial_{x_1}=0\). | CLOSED | Exact invariance of \(\mathcal S_{2D}\). | The single row is not invariant; the larger planar class is. |
| G3 | Every smooth orbit in the selected nonlinear class is global. | CLOSED | The restriction is exactly periodic 2D Navier--Stokes, with the scalar-vorticity enstrophy identity. | This is a barrier to singularity, not a theorem for general 3D data. |
| G4 | A frozen top eigenvector has physical \(H^3\) cost at most \(C\Lambda^2\) after kinetic \(L^2\) normalization. | CLOSED | Fixed-contour eigenvalue bound, order-zero kinetic operator, two elliptic iterations, and exact physical lift. | The power two is deliberately non-sharp; no whole-projection \(L^2\to H^3\) bound is used. |
| G5 | A perturbation with \(Y(0)\le(a\Lambda/4b)e^{-a\Lambda T_D}\) obeys \(Y(t)\le2e^{a\Lambda t}Y(0)\) on the fixed window. | CLOSED | The commutator inequality \(Y'\le a\Lambda Y+bY^2\) and scalar comparison. | This is a sufficient envelope, not a sharp transition threshold. |
| G6 | The exact all-mode remainder is at most \(C_De^{M_D\Lambda}\|w_0\|_{H^3}^2\). | CLOSED | \(L^2\) energy for \(r=w-z\) and the full quadratic forcing, together with G5. | The coarse exponent \(M_D\) is not matched to the unstable exponent. |
| G7 | Seeds below the explicit ceiling inherit at least half of the R0.73F relative gain. | CLOSED | G4--G6 and the R0.73F lower law. | The final perturbation may still tend to zero as \(\Lambda\to\infty\). |
| G8 | The selected complex Fourier row is a nonlinear invariant subsystem. | FALSE | Exact self-interaction has a nonzero physical \(K_z=2\) Leray component; the real pair has channels \(K_z=0,\pm2\). | Feedback to \(K_z=\pm1\) begins no earlier than cubic order. |
| G9 | One-row gain alone yields order-one departure from a natural seed \(\delta\asymp e^{-\kappa_D\Lambda}\). | NOT PROVED / FALSE AS AN INFERENCE | The sufficient ceiling also pays the crude \(H^3\) envelope and can be much smaller. | A harmonic-resolved bilinear or targeted cubic estimate is required. |
| G10 | The selected row can create three-dimensional vortex stretching. | FALSE | The identities \(u_1=0\) and \(\partial_{x_1}=0\) are preserved exactly. | Add a transverse mode with \(K_x\ne0\) or nonzero first component. |
| G11 | A transverse three-dimensional seed can be propagated through the unstable planar bundle with a closed triad remainder. | OPEN | No sharp transverse Squire, pressure, or mode-convolution theorem is available here. | This is the next analytic gate. |
| G12 | The selected mechanism proves finite-time singularity or resolves the Clay problem. | OPEN | Every nonlinear orbit proved in this section is globally smooth. | No conclusion for arbitrary three-dimensional data. |

## Release decision variables

```text
exactDecayingShearPerturbationEquation=CLOSED
selectedSeedPlanarInvariantClass=CLOSED
selectedNonlinearOrbitGlobalSmoothness=CLOSED
topEigenvectorPolynomialH3Cost=CLOSED
fixedWindowH3Bootstrap=CLOSED
allModeQuadraticRemainderBound=CLOSED
nonlinearRelativeAmplification=CLOSED
topEigenvectorDoubleRowLeakage=CLOSED

singleLinearRowNonlinearInvariant=FALSE
selectedRowCanCreateThreeDimensionalVortexStretching=FALSE
oneRowGainAloneImpliesOrderOneDeparture=FALSE_AS_INFERENCE
oneRowGainAloneImpliesFiniteTimeSingularity=FALSE

naturalSeedOrderOneDeparture=OPEN
sharpBilinearEvolutionAtUnstableRate=OPEN
transverseThreeDimensionalTriadClosure=OPEN
singleBackgroundSingleOrbitInstability=OPEN
completeOSSquireA2DirectSum=OPEN
Clay=OPEN
```

The CLOSED amplification statement and the CLOSED global-smoothness
statement apply to the same selected family.  Large relative growth is
therefore compatible with regularity and is not evidence of a
Navier--Stokes singularity.
