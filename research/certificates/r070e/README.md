# R0.70E exact Yu-parity transversality audit

This archive checks the finite algebra used in the R0.70E parity--
transversality construction.

The producer verifies, with exact SymPy arithmetic:

- the divergence, vector potentials, heat eigenvalues, and reflection
  eigenvalues of the explicit even--odd Fourier pair;
- all four stretching coefficients and their parity;
- all four coefficients of the reflection-parameter cubic, its exact root,
  and its derivative;
- the spherical fourth moment and the leading small-frequency coefficient of
  Yu's hard-annulus strain multiplier.

The archive does **not** computer-prove compact vector-potential localization,
Gaussian heat-tail convergence, Kato small-data theory, or the implicit-
function theorem.  It also does not identify the project-defined signed
moving-shell contraction with Yu's positive annular quantity
\(\mu_k^{\mathrm{far,ann}}\).  No regularity or singularity claim is made.

## Reproduction

From the repository root, run the command recorded in `command.txt`.  The
expected producer environment is recorded in `environment.txt`.

## Payloads

- `result.json`: deterministic exact symbolic output and claim boundary;
- `command.txt`: reproduction command;
- `environment.txt`: baseline and interpreter versions;
- `SHA256SUMS`: hashes of the producer, result, command, environment, and this
  README.
