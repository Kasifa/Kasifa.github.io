# R0.73M finite-diagnostic protocol

**Status:** source-frozen protocol; formal outputs must be generated only after
the source commit exists

**Date:** 2026-08-31 (Asia/Shanghai)

## 1. Question and evidence class

The finite computation asks whether the already proved prescribed-action
recoding has the expected finite-Galerkin anatomy at the exact endpoint

\[
 D_*={1\over450},\qquad T_*={1\over1800},\qquad d=4t.
\]

It computes a binary64 Galerkin diagnostic.  It is not used to prove the
continuum theorem.  In particular, the finite quantity

\[
 A_{N,0}:=\int_0^{D_*}\lambda_{N,0}(d)\,\mathrm d d
\]

is always called the **finite inviscid action proxy**.  It must never be
identified with the continuum action \(\mathcal A_*\).

The central finite recoding is

\[
 g^{(0)}_{N,\varepsilon}
 :=G_{N,\varepsilon}\exp(-A_{N,0}/\varepsilon).
\tag{1.1}
\]

This differs from the R0.73L viscous normalization

\[
 G_{N,\varepsilon}\exp(-A_{N,\varepsilon}/\varepsilon),
 \qquad
 A_{N,\varepsilon}:=\int_0^{D_*}
 \lambda_{N,\varepsilon}(d)\,\mathrm d d.
\tag{1.2}
\]

Both must be computed, stored under different field names, and compared.
Renaming the quantity in (1.2) as (1.1) is a release-stopping error.

## 2. Frozen grid

The primary grid is the Cartesian product

\[
 N\in\{32,48,64\},\qquad
 \varepsilon\in
 \{10^{-3},5\!\times\!10^{-4},2.5\!\times\!10^{-4},
 1.25\!\times\!10^{-4},6.25\!\times\!10^{-5}\}.
\]

The fixed-contour branch uses center \(0.17\), radius \(0.003\), and 65
uniform profile-time samples on \([0,D_*]\).  The primary linear solve uses
DOP853 with `rtol=1e-10`, `atol=1e-12`, and
`max_step=D_*/256`.  The primary harmonic hierarchy uses fast-time step
`0.05`.

Step convergence is rerun at \(N=64\),
\(\varepsilon\in\{10^{-3},6.25\times10^{-5}\}\), and fast-time steps
`0.1`, `0.05`, and `0.025`.

Independent linear/action recomputation covers five preregistered sentinels:

| cutoff | \(\varepsilon\) |
|---:|---:|
| 32 | \(10^{-3}\) |
| 32 | \(6.25\times10^{-5}\) |
| 48 | \(2.5\times10^{-4}\) |
| 64 | \(5\times10^{-4}\) |
| 64 | \(6.25\times10^{-5}\) |

Independent harmonic recomputation covers
\((32,10^{-3})\), \((48,2.5\times10^{-4})\), and
\((64,6.25\times10^{-5})\).

## 3. Primary coefficients

Let the finite Taylor hierarchy be

\[
 v_N(\eta)=\eta V_1+\eta^2V_2+\eta^3V_3+O(\eta^4),
\]

and define the actual finite linear gain

\[
 G_{N,\varepsilon}:=\|V_1(D_*)\|_2.
\]

All endpoint coefficients are normalized by this measured gain:

\[
 a_N={V_1\over G_{N,\varepsilon}},\qquad
 b_N={V_2\over G_{N,\varepsilon}^2},\qquad
 c_N={V_3\over G_{N,\varepsilon}^3}.
\tag{3.1}
\]

The implementation must not normalize (3.1) directly by
\(e^{A_{N,0}/\varepsilon}\).  It stores separately:

- \(\|a_N(D_*)\|_2\), which must equal one up to roundoff;
- \(\|b_N(D_*)\|_2\), supported only on \(K_z=0,\pm2\);
- \(\|\Pi_{\pm1}c_N(D_*)\|_2\);
- \(\operatorname{Re}\langle a_N,\Pi_{\pm1}c_N\rangle\), with the
  zero-row and doubled-row paths stored separately;
- divergence, reality, forbidden-parity, and outer-shell diagnostics.

For display values \(\rho\in\{0.02,0.05\}\), define only the finite
third-order target-row diagnostic

\[
 \delta_{N,\varepsilon}
 =\rho g^{(0)}_{N,\varepsilon},\qquad
 \delta_{N,\varepsilon}a_N(D_*)
 +\delta_{N,\varepsilon}^3\Pi_{\pm1}c_N(D_*).
\tag{3.2}
\]

These \(\rho\) values are visualization choices, not certified continuum
Taylor radii.

## 4. Independent paths

The independent linear validator must not import the primary program.  It
uses midpoint matrix-exponential propagation and midpoint quadrature to
recompute \(G_{N,\varepsilon}\), \(A_{N,0}\),
\(A_{N,\varepsilon}\), and (1.1).

The independent hierarchy validator must not import the primary program.  It
uses scalar vorticity, Biot--Savart inversion, alias-free FFT convolution,
and an independently written time integrator.  It compares the five raw
paths

1. `V1`,
2. `V2_Kz0`,
3. `V2_KzPlusMinus2`,
4. `V3_via_Kz0`,
5. `V3_via_KzPlusMinus2`.

The old R0.73H endpoint \(d=0.01\) may not be interpolated.  Every hierarchy
case must be rerun at \(D_*=1/450\).

## 5. Frozen validation gates

The source package must validate, fail closed, at least the following:

- `profileTimeEnd == 1/450`, `physicalTimeEnd == 1/1800`, and `d=4t`;
- all 15 primary grid cases exist exactly once and contain only finite values;
- the finite inviscid and viscous actions are stored separately;
- fixed-contour branch count and phase anchor remain valid at every action
  node;
- generator and selected-eigenpair relative residuals are at most
  \(5\times10^{-12}\);
- divergence, reality, and forbidden-parity relative residuals are at most
  \(5\times10^{-10}\);
- \(|\|a_N(D_*)\|_2-1|\le5\times10^{-10}\);
- primary fast-step relative discrepancy is at most \(10^{-7}\);
- finest adjacent-cutoff relative discrepancy is at most \(10^{-6}\);
- outer-three-shell mass fraction is at most \(10^{-8}\);
- independent linear gain and both action discrepancies are at most
  \(2\times10^{-6}\) relative;
- independent \(g^{(0)}\) discrepancy is at most \(2\times10^{-6}\)
  absolute;
- independent raw hierarchy paths agree to \(2\times10^{-8}\) relative;
- the exact rational identities
  \(D_*=1/450\), \(T_*=D_*/4=1/1800\),
  \(2\mu_*-1/3=1/1500\),
  \(3\mu_*-1/2=1/1000\), and
  \(4\mu_*-1/2=21/125\) are checked without floating-point arithmetic.

The additional configuration gates have the following fixed operands:

- `numericalReality` is the maximum absolute imaginary part of every
  selected viscous and inviscid eigenvalue;
- `physicalKineticGainRelative` is
  \(|G_{\rm phys}-G_{\rm kin}|/\max(G_{\rm phys},G_{\rm kin})\), maximized
  over the 15 primary cases;
- `largestCutoffActionProxyAbsolute` and
  `largestCutoffPrefactorAbsolute` are the maximum absolute \(N=48\) versus
  \(N=64\) differences over the five epsilon values;
- `independentLinearRefinement` is the maximum relative 256-step versus
  512-step change among the independently recomputed gain, the two actions,
  and \(g^{(0)}\);
- `independentHierarchyForbiddenParityRelative` is the maximum independent
  forbidden-row norm divided by its corresponding full coefficient norm.

The exact output names, scalar/array shapes, dtypes, and normalizations are
machine-frozen by `config.json` under `outputSchema`.  The exact fractions
are also frozen there under `exactRationals`; the exact-identity program must
compare its independently constructed `fractions.Fraction` values with that
configuration rather than silently relying on an unrelated hard-coded set.

If an independently implemented method has a documented normalization
difference, the validator must compare after an explicit exact conversion;
loosening a gate after seeing a formal result is not permitted without a new
source commit and a written protocol amendment.

## 6. Source-before-run and process monitoring

Formal outputs may be created only after the complete source package and
this protocol are committed.  A smoke test must write outside the formal
package.  The formal run records:

- source commit and bound upstream source hashes;
- exact command, Python/dependency environment, host and resource metadata;
- timestamped `progress.ndjson` and independent progress streams;
- deterministic scientific CSV/JSON/NPZ payloads;
- validation report, flat manifest, and `SHA256SUMS`.

Scientific result JSON must not contain wall-clock timestamps or measured
runtime.  Timestamped progress/resource streams and environment/manifest
metadata are intentionally operational and need not be byte-identical across
runs; they must remain outside the deterministic scientific payload fields.

The run is monitored while active.  Expected local-CPU cost is 90--120
seconds and less than 1 GB RAM; DGX is not selected unless a measured local
bottleneck invalidates that estimate.

## 7. Mandatory claim boundary

Every certificate summary, figure caption, and public note must encode the
following truth values:

```text
finiteInviscidActionProxyComputed=true
finiteViscousActionComputedSeparately=true
finitePrescribedActionRecodingComputed=true
finiteABCoefficientsComputed=true
continuumActionCertifiedByFiniteComputation=false
continuumGainPrefactorCertifiedByFiniteComputation=false
prefactorLimitCertified=false
twoTermWKBCertified=false
uniformTaylorRadiusCertified=false
fourthOrderRemainderCertified=false
fullNonlinearNavierStokesTrajectoryComputed=false
finiteCutoffAgreementIsTailProof=false
singleFixedBackgroundLyapunovInstabilityCertified=false
transverseThreeDimensionalClosureCertified=false
finiteTimeSingularityCertified=false
clayProblemSolved=false
```

This key set and spelling must be byte-for-byte identical to the
`claimBoundary` object in the canonical configuration.

The finite package diagnoses action recoding and the first three Taylor
coefficients.  It does not compute a full nonlinear trajectory, control the
fourth-order remainder, produce a continuum prefactor limit, or add any
three-dimensional vortex-stretching conclusion.
