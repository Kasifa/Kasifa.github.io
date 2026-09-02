# R0.74S low-Rayleigh dissipation certificate report

## Result

**PASS** — 16/16 exact algebra rows,
8/8 finite checks,
52/52 structural checks,
and 9/9 negative
mutations passed.

## Exact algebra

| Check | Left | Right | Margin |
|---|---:|---:|---:|
| trichotomy_half_minus_two_eighths | 1/4 | 1/4 | 0/1 |
| g_over_e_normalization_factor_two | 1/1 | 1/1 | 0/1 |
| jensen_four_R_squared_constant_squared | 1/1 | 1/1 | 0/1 |
| per_shell_power_of_two_exponent | 1/1 | 1/1 | 0/1 |
| per_shell_gamma_exponent | 1/3 | 1/3 | 0/1 |
| per_shell_lambda_exponent | 1/1 | 1/1 | 0/1 |
| per_shell_payment_exponent | 2/3 | 2/3 | 0/1 |
| per_shell_C1_exponent | 2/3 | 2/3 | 0/1 |
| per_shell_scalar_two_exponent | 11/3 | 11/3 | 0/1 |
| cross_shell_holder_reciprocal_exponents | 1/1 | 1/1 | 0/1 |
| cross_shell_coefficient_cube_gamma_exponent | 1/1 | 1/1 | 0/1 |
| residual_threshold_reciprocal | 1/1 | 1/1 | 0/1 |
| canonical_profile_geometric_sum | 1/7 | 1/7 | 0/1 |
| constant_profile_tail_base_exponent | 6/1 | 6/1 | 0/1 |
| constant_profile_tail_exponent_growth | 4/1 | 4/1 | 0/1 |
| constant_profile_exp_series_lower_bound | 25/1 | 25/1 | 0/1 |

## Finite rational checks

- The priority trichotomy passes 2436
  eligible exact rational splits out of 2916
  grid configurations.  Its class counts are
  defect=2044,
  high=360, and
  low=32.
- The low-Rayleigh mass implication passes
  800 exact rational fixtures, including the
  normalization factor two and the strict `T/(8 lambda)` conclusion.
- The direct definition of `L` passes 704
  eta-zero and zero-row boundary fixtures.  The analytic weak-gradient fact
  used to reach the zero row from a zero weighted denominator is explicitly
  outside this machine check.
- Jensen passes 69564 rational step functions on
  normalized lengths at most four, with 1020
  equality cases retained.  The square-valued energy levels make every
  comparison exact and radical-free.
- Cross-shell Hölder passes 69228 exact rational
  coefficient/payment fixtures, with 492
  equality cases.
- For `lambda_k=1`, the exact base `x_4=6` and recurrence
  `x_(k+1)=4x_k` give a strict geometric ratio below `1/2` from shell four;
  29 exact rational rows check the ledger.
  This uses `exp(x) >= 1+x+x^2/2` only as the displayed elementary comparison.
- For `lambda_k=2^(-2k) gamma_k^(-1/3)`, the coefficient ledger is
  `2^(-3k)` and its exact infinite geometric sum is
  `1/7`.  The critical profile
  has unit coefficients and partial sum
  `64/1` at shell 64.
- The general near-critical geometric formula passes
  9 exact epsilon values on the grid
  `epsilon=n/3`, including the canonical `epsilon=1` sum `1/7`.

## Negative mutations

- `mutation_threshold_eighth_to_quarter`: rejected.
- `mutation_drop_g_over_e_factor_two`: rejected.
- `mutation_extend_rho_equivalence_to_eta_zero`: rejected.
- `mutation_reverse_jensen_direction`: rejected.
- `mutation_replace_jensen_half_by_one`: rejected.
- `mutation_gamma_exponent_one_third_to_two_thirds`: rejected.
- `mutation_declare_critical_lambda_summable`: rejected.
- `mutation_residual_factor_eight_to_four`: rejected.
- `mutation_promote_finite_checks_to_analytic_PDE_Clay_claims`: rejected.

## Reproducibility

- Source note SHA-256: `e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3`
- Generator SHA-256: `61bb1322151b66fc0cf780d2dfc15e0e06dde9a6cc59cc192be1b8c9e8d5e76a`
- JSON payload SHA-256: `4f26fefe25ec92cdae86c2a45f384d0ed87ab3afe83a7d9ef7829ff829be6be1`
- The output contains no timestamp, random seed, floating-point calculation,
  network input, or non-standard Python dependency.
- Set `R074S_DISSIPATION_NOTE`, `R074S_DISSIPATION_JSON`, and
  `R074S_DISSIPATION_REPORT` to rebuild against explicit paths.

## Boundary

This is a finite/algebraic certificate.  It checks rational threshold
arithmetic, finite rational step functions, exponent bookkeeping, elementary
sequence comparisons, and statement integrity.  It does **not** machine-prove
the inherited padded-shell Hölder estimate (R.214), the shell-dependent
payment theorem (R.211), their analytic hypotheses, any Navier--Stokes PDE
claim, regularity, or the Millennium problem.

**FINITE/ALGEBRAIC ONLY.  INHERITED ANALYSIS NOT MACHINE-PROVED.  NOT CLAY.**
