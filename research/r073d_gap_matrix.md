# R0.73D gap matrix

**Date:** 2026-08-30  
**Purpose:** bind every static viscous-persistence claim to its evidence and
prevent a fixed frozen spectral theorem from being extended to the
nonautonomous or nonlinear problem.

| ID | statement | state | evidence | exact boundary or next gate |
|---|---|---|---|---|
| D1 | the R0.73C eigenvector belongs to \(X_{1/4}\) and the eigenvalue is isolated with finite algebraic multiplicity | CLOSED | \(c=i\eta_*\) avoids critical levels; compact perturbation of skew multiplication | does not prove simplicity or uniqueness in the bracket |
| D2 | \(UAU^{-1}=M+K\) on \(L^2\), with the correct kinetic-space and elliptic domains | CLOSED | exact Fourier/unitary calculation plus independent domain audit | preserve \(D(H_0)=L^2\), \(D(H_\varepsilon)=H^2\) |
| D3 | the Rayleigh correction \(K\) is compact | CLOSED | bounded Fourier commutator followed by compact \(L^{-1/2}\) | special to the fixed row; not a full three-dimensional compactness claim |
| D4 | dissipative base resolvents are uniformly bounded and converge strongly, together with adjoints | CLOSED | coercivity, dense-core identity, resolvent equicontinuity | no operator-norm convergence of the base resolvents |
| D5 | the full resolvents exist and are uniformly bounded on a fixed inviscid contour | CLOSED | norm convergence of compact Fredholm factors | existential contour; no certified numerical radius |
| D6 | fixed-cluster Riesz projections converge in operator norm | CLOSED | subtract analytic base resolvent, compact sandwich, adjoint strong convergence; independent audit PASS | only the fixed cluster; not all right-half-plane spectrum |
| D7 | total algebraic multiplicity of the fixed viscous cluster equals the inviscid multiplicity | CLOSED | projection norm below one and compact viscous resolvent | does not identify the unknown integer \(m_*\) |
| D8 | every eigenvalue in the fixed viscous cluster converges to \(\sigma_*\) | CLOSED | repeat on nested fixed circles | no convergence rate |
| D9 | a general zero-viscosity unstable-spectrum theorem already exists | literature pass | Shvydkoy--Friedlander 2008 | project contribution must be stated as explicit realization/special strengthening |
| D10 | moving-profile Riesz continuation is uniform in \(\varepsilon\) | OPEN | none | control \(d\)-dependence on a common contour |
| D11 | complementary frozen or moving semigroup has a uniform exponential dichotomy | OPEN | none | resolvent/Gearhart or direct semigroup theorem on the complement |
| D12 | logarithmic fast-time instability transfers to the heat-decaying profile | OPEN | R0.73C conditional lemma only | fixed-projection Volterra or Kato/dichotomy proof |
| D13 | complete OS--Squire \(A_2\) direct sum | OPEN | one two-dimensional Fourier row only | pressure/Squire and collision-scale closure |
| D14 | nonlinear Navier--Stokes or Clay implication | OPEN | no nonlinear frequency closure | separate nonlinear theorem required |

## Release decision variables

```text
staticVanishingViscosityPersistence=CLOSED
fixedClusterRieszProjectionNormConvergence=CLOSED
fixedClusterAlgebraicMultiplicityPreservation=CLOSED
generalPersistencePrecedent=KNOWN
movingProfileUniformContour=OPEN
uniformComplementaryDichotomy=OPEN
logFastTimeTransfer=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

The first three status values were closed only after the independent analytic
audit passed.  No finite diagnostic was used to change their status.
