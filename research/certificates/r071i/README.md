# R0.71I exact-certificate bundle

This directory archives the exact and independent audits for the R0.71I
joint-creation release.

## Decision recorded by the bundle

1. On every positive-denominator component, the normalized projected-Lamb
   coefficient satisfies the exact joint damped equation
   `a_t + 2*nu*K^2*a = 2*z^+*J`.
2. Its amplitude vector has an exact radial/tangent Pythagorean identity, and
   the deterministic BV formula reduces both endpoint amplitudes to the
   initial amplitude plus one-sided joint creation.
3. The fixed-epsilon scalar ledger is global and contains the additional
   positive radial damping `nu*K^2*epsilon/(d+epsilon)`.
4. A common-heat two-mode path has zero outer amplitude faces but a weighted
   BV/physical-time-volume ratio exactly proportional to `K^2`.
5. The canonical global-smooth 2D3C datum uses eight symmetric target modes.
   Its exact initial constants are `263/90`, `36*K^2/5`, `8*K^2`, `8*K^4`,
   and `B=0`.  A fixed-window Duhamel estimate yields a positive limiting
   interior pulse for one fixed smooth radial two-ring multiplier.
6. That pulse rejects payment of its one-sided joint creation by its R0.71F
   heat volume alone.  It does not reject the full face-paid weighted-BV
   target, the preselected broad dyadic frame, or every possible NSE budget.
7. Uncontrolled complementary-cutoff refresh has exact fixed-energy cost
   `3*U^2/28`; fixed or quantitatively transported partitions remain open.

The bundle makes no Leray-level, continuation, regularity, singularity,
originality, priority, or Millennium-problem claim.

## Files

- `result.json` — canonical sorted JSON from the exact SymPy producer;
- `independent-result.json` — independent standard-library path, Fourier,
  quadrature, and scaling checks;
- `command.txt` — reproduction commands;
- `environment.txt` — runtime and compute boundary;
- `SHA256SUMS` — release dependency hashes;
- `build_hashes.py` — deterministic hash-ledger generator;
- `../../r071i_exact_audit.py` — exact producer;
- `../../r071i_independent_audit.py` — independent checker;
- `../../r071i_report-source.md` — formal analytic report;
- `../../r071i_gap_matrix.md` — claim and obstruction matrix;
- `../../r071i_literature_audit.md` — bounded primary-source audit;
- `../../r071i_independent_audit.md` — independent mathematical audit;
- `../../../figures/r071i-joint/fig-r071i-joint-volume-gap` — journal figure
  package.

## Reproduction boundary

The exact producer uses symbolic contraction and exact finite Fourier
convolution.  The independent checker implements its own binary64 Fourier
algebra with only the Python standard library.  The 2D3C finite-window result
uses an analytic Duhamel estimate; the plotted curves are its closed-form
limit, not finite-K time-stepped data.  The figure adds an independent
70-digit Decimal audit.  No GPU, DGX, DNS, fitted model, or three-dimensional
PDE time stepping is used.
