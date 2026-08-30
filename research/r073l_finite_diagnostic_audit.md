# R0.73L finite diagnostic audit

**Status:** PASS; sealed diagnostic package and independent reconstruction

**Package:** `experiments/r073l/`

## 1. Direct decision

The finite Fourier diagnostic is internally consistent and agrees with an
independent time integrator.  It supports the predicted bounded
action-normalized gain and the onset of \(O(\varepsilon)\) instantaneous
complement leakage.  It has no proof weight for the infinite-dimensional
theorem.

## 2. Frozen configuration

The primary run used:

- kinetic cutoffs \(N=32,48,64\), with dimensions \(65,97,129\);
- viscosities/slowness parameters
  \(10^{-3},5\cdot10^{-4},2.5\cdot10^{-4},1.25\cdot10^{-4},
  6.25\cdot10^{-5}\);
- the complete slow interval \([0,1/450]\), corresponding to terminal fast
  times from \(2.2222\) to \(35.5556\);
- 65 reporting nodes and a DOP853 solve with
  `rtol=1e-10`, `atol=1e-12`;
- the same four-term kinetic recurrence and fixed Riesz circle used in
  R0.73K.

Fifteen primary trajectories completed, each with 3,269 right-hand-side
evaluations.  Progress and resource samples were written as NDJSON during the
run.

## 3. Main numerical observations

At the largest cutoff, the terminal action-normalized gains were

| \(\varepsilon\) | terminal action | \(G_Ne^{-\Phi_N}\) | \(\|Q_Nu\|/\|P_Nu\|\) |
|---:|---:|---:|---:|
| \(1.0\times10^{-3}\) | 0.374611 | 0.99982849 | 0.00223605 |
| \(5.0\times10^{-4}\) | 0.752465 | 0.99970105 | 0.00184208 |
| \(2.5\times10^{-4}\) | 1.508182 | 0.99952276 | 0.00130284 |
| \(1.25\times10^{-4}\) | 3.019622 | 0.99937793 | 0.000683043 |
| \(6.25\times10^{-5}\) | 6.042504 | 0.99932905 | 0.000313255 |

Across all cases, the terminal normalized gain stayed in
\([0.99932905,0.99982849]\).  The maximum absolute forward-orbit
backward-action residual was \(6.712\times10^{-4}\).

The log--log slope of terminal leakage over all five viscosities was about
0.710, reflecting a pre-asymptotic shoulder at the two largest viscosities.
Over the three smallest viscosities, the slope was

\[
 1.02813,
\]

consistent with the continuum proof's \(O(\varepsilon)\) upper law.  The
largest observed leakage-to-\(\varepsilon\) ratio over the full trajectories
was 5.6013.  These are observations, not fitted theorem constants.

## 4. Cutoff and independent-solver checks

For the two largest cutoffs, the maximum terminal differences were

\[
 |(G_Ne^{-\Phi_N})_{48}-(G_Ne^{-\Phi_N})_{64}|
 \le6.995\times10^{-15},
\]

\[
 |(\|Q_Nu\|/\|P_Nu\|)_{48}
  -(\|Q_Nu\|/\|P_Nu\|)_{64}|
 \le3.144\times10^{-15}.
\]

The independent reconstruction used piecewise midpoint matrix exponentials
at \(N=32\), with 256 and 512 time blocks, and recomputed the selected action
from midpoint eigenvalues.  It did not import the primary solver.  At 512
blocks its maximum differences from the primary output were

\[
 1.852\times10^{-9}
 \quad\text{for terminal normalized gain},
\]

and

\[
 1.706\times10^{-9}
 \quad\text{for terminal leakage}.
\]

The last-two-mesh refinement differences were below
\(5.554\times10^{-9}\).  All configured checks passed.

## 5. Package integrity

The sealed manifest contains 15 required source, configuration, result,
environment, and monitoring files; `SHA256SUMS` additionally binds the
manifest.  The fail-closed package validator passed schema, source-binding,
configuration-binding, checksum, monitoring-endpoint, and claim-boundary
checks.

## 6. Exact boundary

The diagnostic establishes only:

```text
finiteSelectedDynamicsReproduced=PASS
finiteActionNormalizedGainStable=PASS
finiteLeakageTailSlopeApproximatelyOne=OBSERVED
finiteCutoffAgreement=PASS
independentFiniteReconstruction=PASS
continuumAdiabaticTheoremFromNumerics=FALSE
nonlinearNavierStokesFromNumerics=FALSE
ClayFromNumerics=FALSE
```
