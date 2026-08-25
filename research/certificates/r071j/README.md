# R0.71J exact-certificate bundle

This directory archives the exact and independent audits for the R0.71J
all-frame positive-defect release.

## Decision recorded by the bundle

1. For every finite fixed family between refreshes, shellwise positive joint
   creation equals the weighted amplitude derivative plus a nonnegative
   viscous mass and a nonnegative negative-source defect.  The fixed-epsilon
   soft ledger adds another nonnegative radial damping row.
2. Tight-frame Parseval identities telescope the raw signed numerator, not
   the normalized source after shellwise positive parts.
3. The parent-only broad frame declared in R0.71E contains a fixed-energy
   global-smooth 2D3C family with exact initial constants `2041/200`,
   `178*K^2`, `500*K^2`, `3942*K^4`, and `B=0`.
4. Independent direct heat evolution of every initial Fourier coefficient
   reconstructs the four limiting profiles.  At `theta=log(2)/18`, the
   limiting parent amplitude is a fixed positive number.
5. For all sufficiently large dyadic `K`, full-frame positive creation is at
   least order `K^-2`, whereas the complete parent-frame physical-time heat
   endpoint is at most order `K^-4`.  Their ratio is bounded below by a fixed
   positive multiple of `nu*K^2`.
6. The result covers the R0.71E parent-only frame, one global cell, heat
   height zero, and fixed positive viscosity.  It does not cover the later
   child refinement, matched spatial cells, denominator or refresh faces, a
   different NSE budget, the full face-paid weighted-BV target, regularity,
   singularity, originality, priority, or the Millennium problem.

## Files

- `result.json` — canonical sorted JSON from the exact SymPy producer;
- `independent-result.json` — independent standard-library Fourier,
  direct-heat, and scaling checks;
- `command.txt` — reproduction commands;
- `environment.txt` — runtime, commit fields, and compute boundary;
- `SHA256SUMS` — release dependency hashes;
- `build_hashes.py` — deterministic hash-ledger generator;
- `../../r071j_exact_audit.py` — exact producer;
- `../../r071j_independent_audit.py` — independent checker;
- `../../r071g_exact_audit.py` — exact finite-Fourier primitive imported by
  the producer;
- `../../r071j_report-source.md` — formal analytic report;
- `../../r071j_gap_matrix.md` — claim and obstruction matrix;
- `../../r071j_literature_audit.md` — bounded primary-source audit;
- `../../r071j_independent_audit.md` — independent mathematical audit;
- `../../../figures/r071j-full-frame/fig-r071j-full-frame-gap` — journal
  figure package.

## Commit binding

`environment.txt` binds the clean source snapshot and the byte-exact verified
GitHub Pages deployment to
`6ab52563da0447ecd67dfdfb03b053f023c284a4`.  The figure manifest and both
SHA-256 ledgers were rebuilt only after that source release was online.

## Reproduction boundary

The producer uses exact SymPy contraction and the repository's exact finite
Fourier primitives.  The independent checker implements its own binary64
Fourier algebra with only the Python standard library and rebuilds the heat
profiles from decayed initial coefficients.  The finite-window result uses
an analytic Duhamel estimate.  No GPU, DGX, DNS, fitted model, or finite-`K`
three-dimensional PDE time stepping is used.
