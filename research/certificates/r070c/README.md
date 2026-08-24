# R0.70C exact parity and transversality audit

This archive checks the finite-dimensional symbolic identities used in the
R0.70C generic dynamical sign-defect obstruction.

The producer verifies, with exact SymPy arithmetic:

- divergence, curl, parity, heat eigenvalue, and vortex stretching for the
  inversion-even trigonometric seed;
- the exact torus \(L^1\) and squared \(L^2\) values of that stretching;
- the Beltrami, heat, anti-half-translation, and nonzero total-stretching
  identities for the periodic ABC comparator;
- the simple root and derivative of the normalized two-copy leading
  polynomial \(1-\lambda^3\).

The archive does **not** computer-prove Kato theory, high-Sobolev smooth
dependence, the pointwise annular reconstruction, the no-cross-support
construction, or the Banach-space implicit-function step.  Those are analytic
arguments in `research/r070c_report-source.md`.  Exact nonlinear tuning is
restricted to a specially chosen large even two-plateau cutoff; neither it nor
the perturbative theorem is asserted for every prescribed Yu single-core
geometry.  The ABC check concerns total periodic vortex stretching, not a
periodized annular decomposition.  No Navier--Stokes regularity or singularity
claim is made.

## Reproduction

From the repository root, run the command recorded in `command.txt`.  The
expected producer environment is recorded in `environment.txt`.

## Payloads

- `result.json`: deterministic exact symbolic output and claim boundary;
- `command.txt`: reproduction command;
- `environment.txt`: baseline and interpreter versions;
- `SHA256SUMS`: hashes of the producer, result, command, environment, and this
  README.
