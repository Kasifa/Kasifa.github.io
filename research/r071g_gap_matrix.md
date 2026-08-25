# R0.71G gap matrix — signed projected-Lamb residence time

**Date:** 2026-08-25

**Scope.** Original unforced three-dimensional incompressible Navier--Stokes
equations, first on the periodic torus and then under the scale-covariant
whole-space check used in R0.71F.  The target is either a theorem that derives
a quantitative time--frequency occupation bound from independent NSE budgets,
or a precise obstruction showing which new budget is missing.  A restatement
of `integral A_loc,+ < infinity` is not an advance.

| Claim slot | Final evidence | Status | Boundary retained |
|---|---|---:|---|
| Exact evolution of `L=P(u x omega)` | Equations (3.2) and (1.1) are derived in physical space; the symbolic producer reconstructs both coefficient-by-coefficient from the full six-mode datum | closed | Used only for classical solutions; no Leray-limit derivative identity is claimed |
| Heat--time diagonal ledger | Equations (3.10)--(3.11) retain the source, positive curl square, moving cutoff, bottom face, and positive-height face | closed | The unnormalized positive square does not survive quotient normalization |
| Physical-time moving-cutoff ledger | Equations (4.3)--(4.8) retain viscosity, nonlinear source, movement, cutoff collar, and denominator derivative | closed | A flow-transported cutoff still has a nonzero Eulerian time derivative |
| Definition of a "large" trace | The 2D3C theorem proves sign-only residence can last arbitrarily many viscous times; fixed positive relative levels retain critical `K^-2` scaling | closed distinction | A later-time reset of a relative threshold needs a nondegenerate reference value |
| Normalized quotient derivative | Equation (5.3) proves exact radial cancellation; only `A partial_t L` and angular rotation remain | closed | No sign and no energy-level estimate for these terms |
| Zero denominator | An exact Hilbert-space example makes the zero convention discontinuous; `q_epsilon` or all internal time faces are necessary | closed | Passing `epsilon -> 0` may create a defect measure |
| Leray-level occupation bound | Source counting shows the required time derivative, angular, movement, collar, and normalization budgets are absent from standard energy | rejected at current budget | This is a failure of the present closure, not a proof that no stronger NSE mechanism exists |
| Dissipation-wavenumber overlap | Version-pinned audit confirms unconditional `Lambda in L^1` gives only a `K^-1` Chebyshev tail, whereas stronger conditions imply regularity | closed comparison | `Lambda` is not the signed Lamb observable |
| Bad-interval/intermittency overlap | Gibbon--Doering give genuine high-derivative bad-interval widths; Cheskidov--Dai give the closest time-frequency occupation condition | closed comparison | The first uses global derivative ratios; the second is a regularity hypothesis rather than an energy consequence |
| True NSE witness | Exact infinite sideband chain, analytic Duhamel bound, localized sign formula, exact initial derivatives, independent FFT, and two-radius ODE checks | closed | Finite ODE values are checks; the arbitrary-duration theorem rests on the analytic bound |
| Universal sign-only `O((nu K^2)^-1)` duration | Fixed-energy 2D3C family rejects every finite universal sign-duration constant | rejected | The trace becomes exponentially small; no quantitative high-level theorem is rejected |
| Critical relative-superlevel duration | Exact weak-nonlinearity profiles and all-amplitude matched-aggregate envelopes give `O((nu K^2)^-1)` on the witness family | supported only on witness | No theorem for arbitrary NSE solutions follows |
| Residence alone closes continuation | Disjoint critical episodes have finite weighted bulk but divergent unweighted bottom integral | rejected | Amplitude, crossings, or frequency-envelope summability is still required |
| Residence plus weighted BV | Layer cake and one-dimensional coarea prove the conditional criterion (9.2)--(9.3) | conditional theorem | The required BV sum is not derived from Leray energy |
| Novelty boundary | Two bounded search waves found adjacent dynamic-wavenumber, time-frequency, bad-interval, positive-strain, and filtered-stretching results but no exact standard-budget theorem for the target object | bounded negative finding | Not a nonexistence, originality, or priority statement |

## Version-pinned primary sources

- Alexey Cheskidov and Roman Shvydkoy, *A unified approach to
  regularity problems for the 3D Navier--Stokes and Euler equations: the use
  of Kolmogorov's dissipation range*, arXiv:1102.1944.  Relevant items:
  Theorem 1.1 / Corollary 3.3, the dissipation-wavenumber definition, and
  Lemma 4.1 (`Lambda in L^1` for Leray--Hopf solutions).
- J. D. Gibbon and Charles R. Doering, *Intermittency and regularity issues
  in 3D Navier--Stokes turbulence*, arXiv:math/0406146.  Relevant only as a
  distinct good/bad-interval framework; its interval variables and hypotheses
  must not be identified with signed Lamb occupation.
- Alexey Cheskidov and Mimi Dai, *Regularity criteria for the 3D
  Navier--Stokes and MHD equations*, arXiv:1507.06611v6.  Its indicator-weighted
  shell-vorticity integral is the nearest time--frequency occupation formula,
  but it is an assumption in a regularity criterion.
- Evan Miller, *A regularity criterion for the Navier--Stokes equation
  involving only the middle eigenvalue of the strain tensor*,
  arXiv:1710.05569v4.  It supplies a true sign-sensitive comparison, not a
  signed-shell residence mechanism.
- Nicolas Lerner and Francois Vigneron, *On some properties of the curl
  operator and their consequences for the Navier--Stokes system*,
  arXiv:2203.07950v1.  It establishes projected-Lamb algebra as prior
  structure.
- Runlong Yu, *Filtered vortex stretching and subgrid defects for the
  three-dimensional Navier--Stokes equations*, arXiv:2606.27560v1.  It is a
  recent conditional preprint and is not treated as an energy-driven
  occupation theorem.
- R0.71C, R0.71E, and R0.71F local reports and locked certificates.  These
  are prior internal results, not external novelty evidence.

## Final route decision

The sign-only branch is closed negatively.  The critical normalized
superlevel branch remains open, but its exact derivative requires an angular
source-curvature budget not supplied by the current energy ledger.  R0.71H
will test that term directly and stop the temporal-residence route if the only
available closure is a known regularity norm or an assumed weighted-BV sum.

## Excluded discovery result

The first-pass search returned an article claiming that pressure can always
be chosen to enforce Navier--Stokes regularity.  That claim conflicts with the
fixed-pressure structure of the original problem and is not used as evidence.
