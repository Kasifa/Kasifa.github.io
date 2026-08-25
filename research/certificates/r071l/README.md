# R0.71L certificate bundle

This bundle certifies the fixed-cell viscous-fusion ledger and archives a
standalone deterministic diagnostic of the explicit aligned witness.

The exact producer proves finite algebra:

- fixed-cutoff Laplacian/collar fusion;
- normalization and projective recombination;
- a nontrivial single-eigenspace cancellation;
- aligned cutoff--curl numerator cancellation;
- the witness-specific two-sided denominator comparison; and
- the precise boundary between Leray-paid denominator mass and the remaining
  tangent product.

The independent checker reconstructs the Fourier witness and tensor cutoff
without importing the exact producer or an earlier audit. Its floating-point
signs are diagnostic only and are not continuous interval certificates.
It computes the pure-heat leading coefficients only; the finite-(K)
(O_\nu(K^{-3})) transfer is an analytic input from R0.71J and is not
certified by this quadrature.

Claim boundary: the bundle does not prove a Leray-level impossibility theorem,
an unconditional BV estimate, continuation, singularity, global regularity,
originality, or a Millennium-problem result.

## Files

- `result.json` — exact symbolic result;
- `independent-result.json` — standalone 360 by 80 deterministic diagnostic;
- `command.txt` — reproduction commands;
- `environment.txt` — execution environment;
- `build_hashes.py` and `SHA256SUMS` — archive integrity;
- `../../r071l_exact_audit.py` and `../../r071l_independent_audit.py` — producers;
- `../../r071l_report-source.md`, `../../r071l_gap_matrix.md`,
  `../../r071l_literature_audit.md`, and `../../r071l_independent_audit.md` —
  analytic evidence;
- `../../../figures/r071l-viscous-fusion/fig-r071l-viscous-fusion-gap` —
  journal figure package.
