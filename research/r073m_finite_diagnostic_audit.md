# R0.73M finite prescribed-action diagnostic audit

**Status:** PASS; sealed finite package, independent linear/action
reconstruction, and independent cubic-hierarchy reconstruction

**Package:** `research/certificates/r073m/`

**Source commit:** `7a4d7706d7a50525611b6267061aea0a79f9fd04`

## 1. Direct decision

The finite Fourier computation is internally consistent and reproduces the
prescribed-action recoding on the registered grid.  In particular, the
finite quantity

\[
 g^{(0)}_{N,\varepsilon}
 :=G_{N,\varepsilon}\exp(-A_{N,0}/\varepsilon)
\]

stays in the narrow interval

\[
 0.9960745296895327
 \le g^{(0)}_{N,\varepsilon}
 \le 0.9965850277770183
\]

while the unnormalized physical gain ranges from (1.4541761769) to
(420.6631904678).  The normalized quadratic and selected cubic
coefficients have the registered finite (\varepsilon)-scaling, and a
separately written vorticity/FFT implementation reproduces the stored
coefficients.

This is finite binary64 evidence.  It does not prove a continuum prefactor
limit, a two-term WKB expansion, a uniform Taylor radius, a full nonlinear
trajectory, transverse three-dimensional control, singularity, or the Clay
problem.

## 2. Frozen configuration and fail-closed resolution amendment

The formal grid is

\[
 N\in\{40,48,64\},\qquad
 \varepsilon\in\{10^{-3},5\times10^{-4},2.5\times10^{-4},
 1.25\times10^{-4},6.25\times10^{-5}\}.
\]

It uses 65 action nodes on (0\le d\le1/450), DOP853 for the selected
linear evolution, and fixed-step RK4 in fast time for the physical harmonic
hierarchy through cubic order.  The archive contains fifteen primary cases
and 1,170 action rows.

The first formal preflight at source commit
`7f8a06b0989f53bd79d71bb470058559d001904a` used (N=32,48,64).  It
completed all cases but failed exactly one gate: at
((N,\varepsilon)=(32,6.25\times10^{-5})), the outer-three-shell mass
fraction of (V_3) was (1.5202609437\times10^{-7}), above the frozen
(10^{-8}) threshold.  Three time steps reproduced the failure, whereas
raising the cutoff to (N=40) reduced it to
(3.7440487359\times10^{-10}).  The threshold was not relaxed.  The failed
result hash and resolution table are retained in
`r073m_numerical_protocol.md`.

## 3. Separate finite actions and prescribed-action recoding

The computation stores two different objects under different names:

\[
 A_{N,0}=\int_0^{D_*}\lambda_{N,0}(d)\,\mathrm d d,
 \qquad
 A_{N,\varepsilon}=\int_0^{D_*}
 \lambda_{N,\varepsilon}(d)\,\mathrm d d.
\]

Across the formal grid,

\[
 A_{N,0}\in
 [0.00037786035537770317,0.00037786035537770330],
\]

whereas

\[
 A_{N,\varepsilon}\in
 [0.00037461106351576096,0.00037765647898429130].
\]

Thus the finite prescribed-action prefactor uses (A_{N,0}), not the
viscous action.  For comparison, normalization by the separately computed
viscous action gives values in
([0.9993290522892043,0.9998284900215669]).  Neither normalization is
renamed as the continuum action (\mathcal A_*).

For the two display amplitudes, the selected third-order target diagnostic
has endpoint ranges

\[
 \rho=0.02:\quad[0.01992149059,0.01993170055],
\]

\[
 \rho=0.05:\quad[0.04980372648,0.04982925137].
\]

These are visualization diagnostics for the truncated Taylor expression;
they are not certified continuum Taylor radii and are not full nonlinear
Navier--Stokes trajectories.

## 4. Finite quadratic and cubic hierarchy

At (N=64), the normalized coefficients are:

| (\varepsilon) | (\|b\|_2/\varepsilon) | (\|\Pi_{\pm1}c\|_2/\varepsilon^2) | (\operatorname{Re}\langle a,\Pi_{\pm1}c\rangle/\varepsilon^2) |
|---:|---:|---:|---:|
| (1.0\times10^{-3}) | 0.534989 | 0.226363 | -0.165073 |
| (5.0\times10^{-4}) | 0.755238 | 0.499796 | -0.358398 |
| (2.5\times10^{-4}) | 0.877032 | 0.755997 | -0.533738 |
| (1.25\times10^{-4}) | 0.907135 | 0.842574 | -0.622203 |
| (6.25\times10^{-5}) | 0.912201 | 0.855484 | -0.640395 |

At the smallest viscosity, the signed cubic quantity splits as

\[
 -0.531810\quad\text{through the mean row},\qquad
 -0.108585\quad\text{through the doubled row},
\]

after division by (\varepsilon^2).  The common negative sign is the finite
signature of the registered cubic return.  The table is consistent with the
analytic rate bookkeeping, but five finite viscosities do not establish a
coefficient limit or an asymptotic expansion.

## 5. Cutoff, time-step, conjugacy, and tail checks

All stored primary checks passed.  Selected maximums include:

| check | observed maximum | threshold |
|---|---:|---:|
| physical/kinetic gain discrepancy | (2.607\times10^{-10}) | (2\times10^{-7}) |
| (N=48\leftrightarrow64) action discrepancy | (1.084\times10^{-19}) | (2\times10^{-12}) |
| (N=48\leftrightarrow64) prefactor discrepancy | (1.998\times10^{-15}) | (2\times10^{-6}) |
| finest-pair selected hierarchy discrepancy | (4.276\times10^{-15}) | (10^{-6}) |
| step-convergence discrepancy | (1.158\times10^{-8}) | (10^{-7}) |
| outer-three-shell mass fraction | (3.744\times10^{-10}) | (10^{-8}) |
| generator conjugacy defect | (8.544\times10^{-17}) | (5\times10^{-12}) |

The selected eigenvalue imaginary part, eigen-residual, divergence,
reality, phase-anchor, parity, and endpoint-normalization checks also passed.
Finite cutoff agreement is not promoted to an analytic Fourier-tail proof.

## 6. Independent reconstructions

The independent linear program uses midpoint matrix-exponential products
with 256 and 512 blocks and independently recomputes both action branches.
It does not import the primary producer.  Across five preregistered
sentinels, its maximum discrepancies were:

\[
 2.083\times10^{-9}\quad\text{for gain},
\]

\[
 4.976\times10^{-12}\quad\text{for inviscid action},
 \qquad
 5.020\times10^{-12}\quad\text{for viscous action},
\]

and (2.105\times10^{-9}) for the prescribed-action prefactor.  The
last-two-mesh refinement discrepancy was (5.557\times10^{-9}).  All five
sentinels passed their (2\times10^{-6}) gates.

The independent hierarchy program uses scalar vorticity, an independently
written Biot--Savart map, alias-free physical-grid FFT products, and fixed
RK4.  It does not import the primary producer.  Three preregistered
sentinels passed; the maximum coefficient relative difference was
(8.320\times10^{-10}), against a (2\times10^{-8}) gate, and the maximum
forbidden-parity leakage was (1.097\times10^{-17}).

## 7. Package integrity

The fail-closed validator recomputed the raw-archive observables and every
tolerance decision, verified the source and upstream hashes, checked the
exact output schema, and passed 28 of 28 checks.  The sealed manifest binds
30 package files;
`SHA256SUMS` has 31 entries including the manifest.  Post-seal verification
passed.  The complete R0.73M Node gate passed three of three test groups.

## 8. Exact boundary

```text
finiteInviscidActionProxyComputed=PASS
finiteViscousActionStoredSeparately=PASS
finitePrescribedActionRecodingComputed=PASS
finiteABCoefficientsComputed=PASS
independentLinearActionReconstruction=PASS
independentCubicHierarchyReconstruction=PASS
continuumActionFromFiniteComputation=FALSE
continuumPrefactorLimit=OPEN
twoTermWKB=OPEN
uniformTaylorRadius=OPEN
fullNonlinearTrajectoryComputed=FALSE
fixedBackgroundLyapunovInstability=OPEN
transverseThreeDimensionalClosure=OPEN
finiteTimeSingularity=OPEN
ClayProblemSolved=FALSE
```
