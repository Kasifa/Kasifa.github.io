# R0.70F exact affine-jet audit

This archive checks the finite algebra used in the R0.70F fixed-annulus
affine-jet gate.

The producer verifies, with exact SymPy arithmetic:

- the homotopy vector potentials for the constant-strain, linear-strain, and
  solid-rotation core fields;
- divergence, curl, strain, harmonicity, and the positive core contractions;
- the exact interlaced-scale factors for the constant and linear initial-face
  work;
- the closed triangular dyadic sum and the four asymptotic Taylor slopes.

The archive does **not** computer-prove smooth cutoff gluing, partition and
filter support buffers, the heat-kernel \(BMO^{-1}\) estimate, Koch--Tataru
well-posedness, or persistence on nested backward cylinders with one common
interior terminal time. It does not identify the project fixed-source work
with Yu's moving-shell positive quantity. No regularity, singularity, or
Millennium claim is made.

The analytic and primary-source checks, including the corrected
coarser-carrier cross-source argument, are recorded in
`research/r070f_independent_audit.md`.

## Reproduction

From the repository root, run the command recorded in command.txt. The
expected producer environment is recorded in environment.txt.

## Payloads

- result.json: deterministic exact symbolic output and claim boundary;
- command.txt: reproduction command;
- environment.txt: baseline and interpreter versions;
- SHA256SUMS: hashes of the producer, report, result, command, environment,
  and this README.
