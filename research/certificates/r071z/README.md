# R0.71Z certificates

This directory archives two independent finite audits for the all-root
bounded-variation and launch-inclusive floor-cancellation release.

- `result.json` is produced by `research/r071z_exact_audit.py` with
  110-digit standard-library `Decimal` arithmetic. It recomputes the
  bounded-variation constant (C_\kappa), the optimizer at (u=3), the
  (M/K_s=O(M^{-2})) lattice factor, bounded-coupling envelopes, the
  strong-coupling diagnostic (eta=M^{6/7}), the
  (Omega^2/K_v\le 2\pi^2K_z^2/3) constant, the exact contrast identity,
  and the loss of fixed-window heat retention.
- `independent-result.json` is produced by
  `research/r071z_independent_audit.py`. It imports neither the producer nor
  its output. Starting from repeated raw parameters, it constructs finite
  shift matrices and checks skew-adjointness, dissipation, contraction, the
  exact target row, multiplier integrals, dissipative payment, and a separate
  complex bounded-variation sampling example.

The analytic proof is in `research/r071z_report-source.md`. These calculations
do not prove the infinite-lattice theorem, enumerate the complete nonlinear
root set, construct a strong-coupling root family, perform DNS, time-step
three-dimensional turbulence, or prove Navier--Stokes regularity.

