# R0.70H exact core-moment variation audit

This archive checks the finite algebra used in the R0.70H fixed-center
core-moment variation gate.

The producer performs exact finite symbolic regressions for:

- the work-critical normalization of zeroth and first core moments;
- constant- and variable-coefficient finite pairing-covariant Abel identities;
- weighted source-shift invertibility on representative geometric grids;
- a scalar-contraction proxy for the adjacent
  filter/cutoff/normalization scale ledger;
- the conditional nested parabolic time-window ledger and the actual
  `r_k^(-2)` spacetime overlap factors;
- the nonconstant-radius `rho`-to-`lambda` index map and the exact
  `r_k*(r_k^(-2))^2=r_k^(-3)` dual-weight identity;
- one polynomial pointwise-divergence regression for the filtered
  local-enstrophy identity, with `Omega=curl(U)` and subfilter flux;
- the corrected R0.70F constant-core recurrence;
- finite samples of the formulas whose analytic proofs give bounded ordinary
  variation and linear pairing-covariant mass;
- component scale-weight geometric series, with profile norms and full-field
  cross terms deliberately excluded.

The finite `Lambda=2,4,8` calculations are exact algebraic regression cases.
They do not certify the geometric separation required by the compact field
construction, which retains the R0.70F assumption that `Lambda` is fixed and
sufficiently large.

The archive does **not** computer-prove the filter multiplier hypothesis, the
compact support geometry inherited from R0.70F, the primary-source search, a
Leray-class parabolic Carleson estimate, nonlinear time persistence, or a
common-positive-terminal-time pressure test. No regularity, singularity, or
Millennium claim is made.

The report supplies the general index-shift proofs. The producer checks
finite generic and rational instances; it does not turn finite regression
loops into a proof for arbitrary sequence length. Its polynomial weights are
not compactly supported, so the local-enstrophy check is explicitly a
pointwise divergence identity rather than a boundary-free integral theorem.

The analytic and source-boundary checks are recorded in
`research/r070h_independent_audit.md`.

## Reproduction

From the repository root, run the command recorded in `command.txt`. The
expected producer environment is recorded in `environment.txt`.

## Payloads

- `result.json`: deterministic exact symbolic output and claim boundary;
- `command.txt`: reproduction command;
- `environment.txt`: baseline and interpreter versions;
- `SHA256SUMS`: hashes of the producer, report, result, command, environment,
  and this README.
