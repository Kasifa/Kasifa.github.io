# R0.71G exact-certificate bundle

This directory archives the exact producer and the independent checker for
the R0.71G signed projected-Lamb residence gate.

## Decision recorded by the bundle

1. The projected Lamb vector
   \(L=\mathbb P(u\times\omega)=u_t-\nu\Delta u\) satisfies the two exact
   smooth-solution evolution formulas stated in the report.  The shell
   expansion retains every interacting shell pair.
2. For a fixed heat height and cutoff, differentiating the signed work and
   denominator gives an exact normalized-amplitude identity.  The radial
   part cancels, so the positive square visible in the unnormalized work
   derivative cannot by itself control the normalized quotient.
3. The exact initial physical-time derivatives of \(B,d,q,Y\), and \(q/Y\)
   are recovered from the full Navier--Stokes datum.  The calculation does
   not freeze the later solution to its six initial modes.
4. The global-smooth 2D3C family reduces to an infinite sideband chain.  The
   report's analytic Duhamel estimate gives arbitrarily long sign-positive
   residence in viscous units at fixed initial energy.  The JSON field
   `analyticDuhamelBoundRecorded` records that report dependency; it does
   not claim that a finite program proves the arbitrary-duration theorem.
5. Finite adaptive integrations show that fixed positive relative levels
   in the checked family exit on the critical viscous scale.  These samples
   support the displayed figure but do not prove a general residence law.
6. A disjoint-event construction shows that critical residence together
   with a \(K^{-2}\)-weighted heat bulk does not imply an unweighted bottom
   trace.  The report supplies a separate conditional BV layer-cake lemma.

These statements prove no unconditional regularity theorem, singularity,
priority, originality, or Millennium-problem claim.

## Files

- `result.json` — canonical sorted JSON emitted by the exact producer;
- `independent-result.json` — independent FFT and adaptive-chain checker;
- `command.txt` — exact reproduction commands;
- `environment.txt` — runtime, hardware, and compute-boundary record;
- `SHA256SUMS` — hashes for the archived payloads and source dependencies;
- `../../r071g_exact_audit.py` — exact symbolic producer;
- `../../r071g_independent_audit.py` — independent numerical checker;
- `../../r071g_report-source.md` — analytic report;
- `../../r071g_gap_matrix.md` — claim and obstruction matrix;
- `../../r071g_literature_audit.md` — bounded primary-source audit;
- `../../r071g_independent_audit.md` — independent mathematical audit.

## Reproduction boundary

The exact producer certifies finite Fourier algebra, exact initial
derivatives, scaling exponents, the normalized radial cancellation, and the
abstract residence-only counterexample.  The independent checker begins
from the full trigonometric velocity, reconstructs the true NSE initial
derivative by FFT and Leray projection, and integrates the reduced sideband
chain with two truncation radii.

This is not DNS and contains no 3D PDE time stepping.  The Mac workstation
alone was used, with one process.  No DGX or GPU resource was used.
