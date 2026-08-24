# R0.70G exact adjacent-jet audit

This archive checks the finite algebra used in the R0.70G adjacent-source
affine-jet gate.

The producer verifies, with exact SymPy arithmetic:

- the critical transport factors for degree-(n) strain jets;
- the constant covariant-increment recurrence and its ordinary-difference
  dilation defect;
- finite Abel summation by parts;
- two inequivalent constant and linear harmonic profiles with identical
  positive (e_1)-lobe pairings;
- the radial constant-core zero-strain lemma;
- the source-side square-function exponents;
- the inherited R0.70F positive initial-face work factors.

The archive does **not** computer-prove the smooth partition construction,
the heat-kernel (BMO^{-1}) estimate, the primary-source search, a core-moment
Carleson estimate, or persistence on backward cylinders with one common
interior terminal time. It does not identify the fixed-source observable with
Yu's moving-shell positive quantity. No regularity, singularity, or
Millennium claim is made.

The analytic and source-boundary checks are recorded in
`research/r070g_independent_audit.md`.

## Reproduction

From the repository root, run the command recorded in `command.txt`. The
expected producer environment is recorded in `environment.txt`.

## Payloads

- `result.json`: deterministic exact symbolic output and claim boundary;
- `command.txt`: reproduction command;
- `environment.txt`: baseline and interpreter versions;
- `SHA256SUMS`: hashes of the producer, report, result, command, environment,
  and this README.
