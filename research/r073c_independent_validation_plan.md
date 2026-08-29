# R0.73C independent validation and certificate packaging plan

**Date:** 2026-08-30  
**Scope:** C3 neutral mode, C4 frozen Rayleigh instability, and the boundary
between finite diagnostics and an infinite-dimensional certificate  
**Hard rule:** this plan does not modify or import
`research/r073c_interval_monodromy.py`, and no finite Fourier output may set
`frozenCollisionRayleighInstability=CLOSED`.

## 1. Current evidence audit

### 1.1 Primary Fourier screen

The current primary diagnostic is
[`r073c_spectral_screen_agent.py`](r073c_spectral_screen_agent.py).  It has
two deliberately different matrix families.

1. `P_N A_gamma P_N` is the ordinary Fourier--Galerkin compression of

   \[
   (A_\gamma)_{mn}=-i\gamma\left(\widehat W_{m-n}
   +\frac{\widehat{W''}_{m-n}}{n^2+\gamma^2}\right).
   \]

   It supplies eigenvalue, left/right condition, and exact embedded-output
   residual diagnostics.
2. `A_gamma^(N)=B+CP_N`, with `B=-i gamma M_W` and
   `C=-i gamma M_W'' L_gamma^-1`, is an infinite-dimensional finite-rank
   perturbation of the normal multiplier `B`.  Its true approximation error
   obeys

   \[
   \|A_\gamma-A_\gamma^{(N)}\|
   \le\frac{\gamma\|W''\|_\infty}{(N+1)^2+\gamma^2}.
   \]

   The script currently evaluates the associated finite Fredholm matrix on
   a contour, but only with floating-point quadrature and sampled nodes.

The following parts are correctly labelled and usable:

- the matrix has only shifts `+-1,+-2` and agrees entrywise with an
  independently derived real recurrence;
- at `gamma=1/2`, the real candidate is
  `sigma=0.170407976920434...`;
- the `N=48` ordinary Galerkin eigenvector has complete band-output residual
  `6.5522e-9`, falling below `4e-11` at `N=64`;
- its simple-eigenvalue projector condition approaches `3.90820585883`;
- the second finite candidate is
  `0.040539390616 +- 0.176137671494 i`;
- the finite-rank/Fredholm contour
  `|z-0.1704|=0.06` has sampled minimum singular value `0.05691363`,
  sampled inverse norm `17.57049`, and sampled winding one;
- the conditional `N=48` tail/Neumann product is `0.401104236`, assuming
  the still-uncertified contour ceilings stated in the spectral note.

The following are not proof evidence:

- agreement of `N=96` and `N=128` digits;
- a small residual for a nonnormal operator without a complement inverse;
- the right edge of `P_N A P_N` at `gamma=sqrt(7)/2` or `gamma=3/2`;
- a winding number obtained only from finitely many floating-point contour
  samples;
- the large-outer-cutoff matrix used to visualize `B+CP_N`;
- the conditional Neumann product before its hypotheses are interval
  certified.

At the neutral threshold, the ordinary finite-section right edge decreases
toward the imaginary essential spectrum and is not the exact neutral mode.
The validation must retain this as a spectral-pollution sentinel, not turn it
into an unstable eigenvalue claim.

### 1.2 Independent finite validator now available

The independent source is
[`independent_fourier_spectral_validator.py`](../experiments/r073c/independent_fourier_spectral_validator.py).
It does not import the primary producer.  Instead it reconstructs each
column from

\[
\begin{aligned}
 A_{n+1,n}&=\frac\gamma4\left(1-\lambda_n^{-1}\right),
 &A_{n-1,n}&=-A_{n+1,n},\\
 A_{n+2,n}&=\gamma\left(-\frac18+\frac1{2\lambda_n}\right),
 &A_{n-2,n}&=-A_{n+2,n},
\end{aligned}
\qquad \lambda_n=n^2+\gamma^2.
\]

On the current primary JSON it independently passed thirteen checks:

- fail-closed claim boundary;
- 20 banded eigenvalue sentinels for
  `gamma in {1/4,1/2,3/4,1}`;
- complete embedded-output residuals;
- left/right projector conditions;
- `gamma=1/2` cutoff agreement and the secondary pair;
- neutral-threshold pollution behavior;
- three `B+CP_N` outer-compression spots built by a second recurrence;
- five Fredholm contour singular-value spots;
- an independent 512-node sampled winding screen;
- exact tail/resolvent constant arithmetic;
- Fredholm singularity at the finite-rank candidate;
- no NaN or infinite recorded number.

The observed maximum discrepancies were:

| quantity | maximum discrepancy |
|---|---:|
| leading eigenvalue | `1.33e-15` |
| embedded residual, absolute | `2.00e-16` |
| projector condition | `2.14e-14` |
| finite-rank outer eigenvalue | `0` at recorded precision |
| conditional constants | `0` at recorded precision |

The validator's output still says
`infiniteDimensionalSpectrumProved=false` and
`continuousContourEnclosed=false`.  This is intentional.

### 1.3 Interval monodromy prototype

The separate source `research/r073c_interval_monodromy.py` works on the
periodic Rayleigh ODE

\[
 \phi''=\left(\gamma^2+\frac{W''}{W-i\eta}\right)\phi,
 \qquad \gamma=\frac12,\qquad \eta>0,
\]

without Fourier truncation.  Its current JSON records `eta`, step interval,
step count, Taylor order, real/imaginary trace intervals,
`traceMinusTwo`, and a sign decision.  It is a primary proof prototype, not
its own independent validator.

Before it can close C4, a separate implementation must verify:

1. the sign convention `c_ph=i eta` and `sigma=gamma eta>0`;
2. exact Wronskian conservation, hence determinant-one monodromy;
3. that `trace(M_eta)-2` has certified opposite signs at two positive eta
   endpoints;
4. continuity on that eta interval, whose denominator never vanishes;
5. every Picard box and Taylor remainder enclosure;
6. the same sign bracket at different step/order/precision settings;
7. byte-bound output, environment, and an independent arithmetic backend.

No part of the independent validator should import functions from the
monodromy producer.

## 2. Reproducible finite-output workflow

The finite diagnostic should eventually live under `experiments/r073c/`
with these files:

| path | role |
|---|---|
| `fourier_screen.json` | primary finite Fourier/Fredholm output |
| `independent_fourier_validation.json` | independent recurrence check |
| `command.txt` | exact one-thread commands |
| `environment.json` | Python, NumPy/SciPy, BLAS, CPU, thread policy |
| `progress.ndjson` | start, phase, completion, and failure events |
| `manifest.json` | immutable file inventory and claim boundary |
| `README.md` | human-readable scope and limitations |

Proposed commands, with the dependency path created outside the repository,
are:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 research/r073c_spectral_screen_agent.py \
  --deps "$R073C_DEPS_DIR" \
  --active-N 48 --outer-N 192 \
  --contour-samples 2048 --quadrature 32768 \
  --output experiments/r073c/fourier_screen.json

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 experiments/r073c/independent_fourier_spectral_validator.py \
  --deps "$R073C_DEPS_DIR" \
  --primary experiments/r073c/fourier_screen.json \
  --winding-nodes 512 --quadrature 8192 \
  --output experiments/r073c/independent_fourier_validation.json
```

The final run should be executed twice from clean output paths.  The two
JSON files must be byte-identical.  This determinism check still does not
upgrade their mathematical status beyond finite diagnostic.

## 3. Finite manifest schema

The finite experiment `manifest.json` should contain at least:

```json
{
  "schemaVersion": "r073c-finite-fourier-manifest-v1",
  "release": "r073c",
  "stage": "finite-diagnostic",
  "createdAt": "UTC ISO-8601",
  "gitHead": "commit or explicit dirty-source hashes",
  "scope": "frozen collision Rayleigh finite Fourier/Fredholm screen",
  "parameters": {
    "d": "0",
    "gammaRows": ["1/4", "1/2", "3/4", "1", "sqrt(7)/2", "3/2"],
    "galerkinCutoffs": [8, 12, 16, 24, 32, 48, 64, 96, 128],
    "fredholmActiveN": 48,
    "outerDiagnosticN": 192,
    "contourCenter": "0.1704",
    "contourRadius": "0.06",
    "contourSamples": 2048,
    "quadraturePoints": 32768
  },
  "normalization": {
    "fourierBasis": "exp(i n x)",
    "l2": "(2 pi)^-1 integral",
    "laplacianEigenvalue": "n^2+gamma^2",
    "phaseSpeedRelation": "sigma=-i gamma c_ph"
  },
  "sources": {
    "producer": "research/r073c_spectral_screen_agent.py",
    "independentValidator": "experiments/r073c/independent_fourier_spectral_validator.py",
    "problemFreeze": "research/r073c_problem_freeze.md",
    "spectralNote": "research/r073c_spectral_enclosure_agent.md"
  },
  "commands": ["exact command strings"],
  "environment": {
    "path": "experiments/r073c/environment.json",
    "sha256": "..."
  },
  "outputs": [
    {"path": "...", "bytes": 0, "sha256": "..."}
  ],
  "numericPolicy": {
    "randomness": "none",
    "threads": 1,
    "eigenvalueOrdering": "largest real part for declared rows",
    "residual": "full band output through N+2",
    "winding": "sampled phase only",
    "nanOrInfinityAllowed": false
  },
  "claimBoundary": {
    "finiteDimensionalOnly": true,
    "ordinaryCutoffConvergenceIsProof": false,
    "continuousContourEnclosed": false,
    "infiniteDimensionalSpectrumProved": false,
    "intervalMonodromyValidated": false,
    "nonautonomousTransferProved": false,
    "nonlinearNavierStokesProved": false,
    "clayProblemSolved": false
  },
  "limitations": [
    "ordinary Galerkin is not norm-convergent because B is a multiplier",
    "outer compression of B+CP_N is finite diagnostic only",
    "floating contour samples do not enclose arcs",
    "no interval winding or complement resolvent is supplied",
    "no fast-time transfer is supplied"
  ]
}
```

Every source and output referenced above needs `bytes` and `sha256`; source
hashes should be stored even when the working tree is not yet committed.

## 4. Independent finite validation schema

`independent_fourier_validation.json` should be fail-closed and contain:

```json
{
  "schemaVersion": "r073c-independent-fourier-validation-v1",
  "status": "passed or failed",
  "primary": {"path": "...", "bytes": 0, "sha256": "..."},
  "validator": {"path": "...", "bytes": 0, "sha256": "..."},
  "checks": {
    "primaryBoundaryIsFailClosed": true,
    "independentBandedEigenvalues": true,
    "independentEmbeddedResiduals": true,
    "independentProjectorConditions": true,
    "gammaHalfCandidateCutoffAgreement": true,
    "secondaryPairRecomputed": true,
    "neutralThresholdRightEdgeFlaggedAsPollution": true,
    "independentFiniteRankOuterSpots": true,
    "fredholmContourSpotMargin": true,
    "independentSampledWinding": true,
    "independentConditionalTailArithmetic": true,
    "finiteRankRootConsistency": true,
    "allRecordedNumbersFinite": true
  },
  "tolerances": {
    "leadingEigenvalueAbsolute": 2e-12,
    "embeddedResidualAbsolute": 2e-12,
    "projectorConditionAbsolute": 2e-8,
    "finiteRankOuterEigenvalueAbsolute": 3e-12,
    "fredholmSpotSingularLower": 0.056,
    "sampledPhaseIncrementUpper": 0.03
  },
  "maximumErrors": {},
  "recomputedSentinels": [],
  "neutralThresholdRows": [],
  "independentWindingScreen": {},
  "claimBoundary": {
    "independentFiniteMatrixAgreement": true,
    "sampledFredholmWindingAgreement": true,
    "ordinaryCutoffConvergenceIsProof": false,
    "continuousContourEnclosed": false,
    "infiniteDimensionalSpectrumProved": false,
    "intervalMonodromyValidated": false,
    "fourierTailRieszCertificateValidated": false,
    "nonautonomousTransferProved": false
  }
}
```

If any required check is absent, false, NaN, nonfinite, outside tolerance,
or bound to the wrong primary SHA-256, `status` must be `failed`.

## 5. Formal C4 certificate schemas

Finite output and a formal certificate should never share the same status
field.  The eventual certificate directory should be
`research/certificates/r073c/` and contain separate primary and independent
records.

### 5.1 Interval-monodromy certificate

Required fields:

```json
{
  "schemaVersion": "r073c-rayleigh-monodromy-certificate-v1",
  "arithmetic": {
    "library": "...",
    "version": "...",
    "precisionBits": 0,
    "outwardRoundingVerified": true
  },
  "operator": {
    "gamma": "1/2",
    "W": "-sin(x)/2+sin(2x)/4",
    "ode": "phi''=(gamma^2+W''/(W-i eta))phi",
    "phaseSpeed": "c_ph=i eta",
    "growthEigenvalue": "sigma=gamma eta"
  },
  "etaBracket": {"lower": "...", "upper": "..."},
  "endpointRuns": [
    {
      "eta": "...",
      "steps": 0,
      "order": 0,
      "stepInterval": ["...", "..."],
      "traceReal": ["...", "..."],
      "traceImag": ["...", "..."],
      "traceMinusTwo": ["...", "..."],
      "sign": "negative or positive",
      "allPicardBoxesClosed": true,
      "maximumStateWidth": "...",
      "maximumRemainderWidth": "..."
    }
  ],
  "analyticChecks": {
    "denominatorNonzeroForPositiveEta": true,
    "monodromyDeterminantExactlyOne": true,
    "traceContinuousOnEtaBracket": true,
    "endpointSignsOpposite": true,
    "periodicEigenvalueExists": true,
    "sigmaLowerBoundPositive": "..."
  },
  "claimBoundary": {
    "frozenCollisionRayleighInstability": "certified",
    "logarithmicFastTimeTransfer": "open",
    "nonlinearNavierStokes": "open",
    "clay": "open"
  }
}
```

The independent monodromy validator must use a different implementation or
arithmetic backend, recompute both endpoint signs, verify all hashes, and
record its own precision/step refinement.  Merely rerunning the same source
with different flags is a refinement check, not independent validation.

### 5.2 Fourier-tail/Riesz certificate

If the Fourier route is retained as an independent proof, its certificate
needs:

```json
{
  "schemaVersion": "r073c-fourier-riesz-certificate-v1",
  "gamma": "1/2",
  "approximation": "A^(N)=B+CP_N",
  "activeN": 0,
  "contour": {"center": "...", "radius": "...", "minimumReal": "..."},
  "analyticFourierStrip": {
    "width": "...",
    "denominatorLower": "...",
    "coefficientAliasUpper": "..."
  },
  "fredholm": {
    "dimension": 0,
    "nodeCount": 0,
    "nodeSingularLower": "...",
    "derivativeUpper": "...",
    "arcSingularLower": "...",
    "inverseUpper": "...",
    "winding": 1
  },
  "operatorTail": {
    "WxxInfinityUpper": "...",
    "deltaNUpper": "...",
    "resolventUpper": "...",
    "neumannProductUpper": "...",
    "strictlyBelowOne": true
  },
  "rieszConclusion": {
    "algebraicMultiplicityInDisk": 1,
    "realPartLower": "...",
    "infiniteDimensionalEigenvalueEnclosed": true
  }
}
```

This route must use ball/interval Fourier coefficients, cover complete
contour arcs, and certify winding.  A floating `min singular` table cannot
populate these fields.

## 6. Cross-route validation decision

The strongest audit is to keep the two routes mathematically independent:

| evidence | finite Fourier route | interval ODE route |
|---|---|---|
| candidate location | `sigma~0.1704079769` | `eta~sigma/gamma~0.3408159538` |
| discretization | Fourier modes | physical-space Taylor steps |
| formal passage | compact-tail Riesz homotopy | determinant-one monodromy and trace sign |
| main failure mode | spectral pollution / unclosed contour | interval dependency / unclosed remainder |
| required independent check | recurrence plus interval Fredholm validator | second ODE implementation/backend |

For a formal C4 close, at least one route must be fully certified and
independently validated.  The other route should numerically overlap its
enclosed `sigma` or `eta` range.  Agreement increases confidence but does not
replace either route's proof obligations.

## 7. Fail-closed release gates

The future R0.73C gate should reject publication as a completed section if
any of the following holds:

1. only ordinary cutoff convergence is present;
2. the primary and independent outputs are not SHA-bound;
3. the monodromy endpoint intervals do not have strict opposite signs;
4. Wronskian/determinant-one or eta-continuity is missing;
5. a Fredholm contour is sampled but not interval-covered;
6. the complement/operator tail is absent;
7. any validator imports the primary producer rather than reconstructing it;
8. any JSON says finite-dimensional rows prove infinite-dimensional
   spectrum;
9. C4 is used to assert C5, nonlinear closure, or a Clay conclusion.

The publication ledger can advance C4 only after the formal certificate,
independent validation, manifest hashes, and boundary checks all pass.  C5
must remain a separate gate even after C4 closes.
