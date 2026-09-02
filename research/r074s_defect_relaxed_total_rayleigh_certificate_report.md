# R0.74S defect-relaxed total Rayleigh-excess certificate report

## Result

**PASS** — 16/16 exact algebra rows,
19/19 finite checks,
75/75 structural checks,
and 20/20
negative mutations passed.

## Exact algebra

| Check | Left | Right | Margin |
|---|---:|---:|---:|
| priority_half_minus_beta_minus_sigma | 1/6 | 1/6 | 0/1 |
| sigma_threshold_contributes_one_sixth | 1/6 | 1/6 | 0/1 |
| beta_threshold_reciprocal | 1/1 | 1/1 | 0/1 |
| excess_threshold_reciprocal | 1/1 | 1/1 | 0/1 |
| jensen_four_R_squared_constant_squared | 1/1 | 1/1 | 0/1 |
| per_shell_power_of_two_exponent | 1/1 | 1/1 | 0/1 |
| per_shell_gamma_exponent | 1/3 | 1/3 | 0/1 |
| per_shell_lambda_exponent | 1/1 | 1/1 | 0/1 |
| per_shell_payment_exponent | 2/3 | 2/3 | 0/1 |
| C4_cubed_scalar | 6912/1 | 6912/1 | 0/1 |
| cross_shell_holder_reciprocal_exponents | 1/1 | 1/1 | 0/1 |
| cross_shell_coefficient_cube_gamma | 1/1 | 1/1 | 0/1 |
| cross_shell_coefficient_cube_dyadic | 3/1 | 3/1 | 0/1 |
| selected_flux_sharp_coefficient | 1/1 | 1/1 | 0/1 |
| direct_clock_to_full_flux_one_BQ | 1/1 | 1/1 | 0/1 |
| exact_family_ratio_identity_at_K_4096 | 4096/1 | 4096/1 | 0/1 |

## Finite rational checks

- Scalar positive mass versus Jordan positive mass passes
  780 signed atomic fixtures, including
  544 strict cancellation cases.  The
  nonnegative `nu-beta-2 lambda sigma` realization independently passes
  1536 fixtures.
- The literal `beta -> sigma -> x` partition passes
  1080 exact configurations.  Branch counts
  are beta=432,
  sigma=216, and
  x=432.
- Jensen passes 22500 rational step functions on
  normalized lengths at most four.  The radical-free cube of
  `C4=12(2 C1)^(2/3)` passes 405 fixtures.
- Cross-shell Holder passes 69228 exact fixtures.
  Selected, global scalar, and global Jordan ledgers pass
  340 shell bundles, with strict examples of
  both enlargements retained.
- Exact-shear terminal absorption passes 243
  `D<=K=T<=beta` fixtures and separately records why it does not prove `X=0`.
- The scalar Portmanteau/positive-part proxy passes
  150 exact rows, while the finite compact-test
  supremum proxy for Jordan `X` passes
  7230 rows.  The density-formula comparison
  passes 4 cancellation fixtures.
- Endpoint escape has open target mass `0/1` versus
  liminf approximating mass `1/1`;
  ordinary mass convergence is correctly rejected.
- The completed-clock reduction `beta>=|Q|` passes
  2976 exact terminal fixtures, including
  308 cases where residual excess forces
  positive signed terminal flux above one sixth.
- The global scalar-excess/flux-variation chain passes
  780 finite shell families.  The
  sharp selected-shell coefficient `6/5` passes
  27 terminal-clock fixtures, and the
  selected-family bridge to the common-zero-start stopped-work supremum passes
  120 exact proxies.  Existence of the common
  good zero-start and the inherited stopped-work framework remain explicitly
  analytic inputs.
- The no-exception clock/flux comparison passes
  5184 exact aggregate fixtures,
  including 7 sharp
  `C_full-W_up=B_Q` cases and
  224 sharp reverse cases.
  The inherited exact-family scaling proxy reaches ratio
  `4096/1` after 12 rows,
  while 48 fixtures independently
  preserve the conditional arithmetic of (S.38).

## Negative mutations

- `mutation_reorder_priority_sigma_before_beta`: rejected.
- `mutation_stale_or_undefined_I_X_selected_index`: rejected.
- `mutation_beta_threshold_one_sixth_to_one_fifth`: rejected.
- `mutation_sigma_threshold_denominator_twelve_to_ten`: rejected.
- `mutation_Jensen_half_constant_to_one`: rejected.
- `mutation_drop_factor_two_inside_C4`: rejected.
- `mutation_conflate_scalar_x_with_Jordan_X`: rejected.
- `mutation_close_hard_terminal_endpoint`: rejected.
- `mutation_promote_fixed_scale_X_finiteness_to_quadratic_bound`: rejected.
- `mutation_promote_linear_scalar_flux_bound_to_quadratic`: rejected.
- `mutation_change_universal_gate_REFUTED_back_to_OPEN`: rejected.
- `mutation_delete_common_zero_start_from_lower_comparison`: rejected.
- `mutation_weaken_sharp_BQ_flux_comparison_to_2BQ`: rejected.
- `mutation_delete_BQ_error_from_flux_comparison`: rejected.
- `mutation_promote_liminf_to_hard_mass_convergence`: rejected.
- `mutation_assert_smooth_density_existence`: rejected.
- `mutation_assert_selected_sum_lsc`: rejected.
- `mutation_assert_X_zero_for_shear`: rejected.
- `mutation_promote_finite_certificate_to_measure_PDE_Clay`: rejected.
- `mutation_drop_selected_six_fifths_coefficient_to_one`: rejected.

## Reproducibility

- Source note SHA-256: `0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab`
- Generator SHA-256: `18735df5a8eff96167ef6314dad04150636c800c276e2fcffc7cbd8177fce9cf`
- JSON payload SHA-256: `3639edbccfddd97781805ed121fc91407771b9bf051ffefae5a17ad80087c69c`
- There is no timestamp, random seed, floating-point calculation, network
  input, or non-standard Python dependency.
- Set `R074S_DEFECT_RELAXED_NOTE`, `R074S_DEFECT_RELAXED_JSON`, and
  `R074S_DEFECT_RELAXED_REPORT` to rebuild against explicit paths.

## Boundary

This is a finite/algebraic certificate.  It checks exact rational threshold
arithmetic, finite atomic or step-function proxies, exponent bookkeeping, and
statement integrity.  It does **not** machine-prove Jordan/Radon regularity,
Portmanteau or measure topology, the inherited R0.74P/R0.74R estimates, their
analytic hypotheses, the inherited R0.74O/P smooth exact PDE family, existence
of smooth approximants, any new Navier--Stokes PDE claim, regularity, or the
Millennium problem.  The finite scaling rows audit the arithmetic of the
stated refutation; the smooth family itself remains inherited analysis.

**FINITE/ALGEBRAIC ONLY.  MEASURE TOPOLOGY AND PDE NOT MACHINE-PROVED.  NOT CLAY.**
