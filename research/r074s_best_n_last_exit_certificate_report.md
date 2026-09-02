# R0.74S best-\(N\) last-exit certificate report

## Result

**PASS** — 9/9 exact algebra rows,
8/8 finite checks,
57/57 structural/source checks,
and 18/18 negative
mutations passed.

## Exact algebra

| Check | Left | Right | Margin |
|---|---:|---:|---:|
| half_exit_two_halves_recover_terminal_flux | 1/1 | 1/1 | 0/1 |
| two_thirds_last_exit_increment | 1/3 | 1/3 | 0/1 |
| strict_quarter_upcrossing_margin | 1/12 | 1/12 | 0/1 |
| one_sixth_signed_increment_margin | 1/6 | 1/6 | 0/1 |
| clock_reduction_BQ_coefficient_at_two_thirds | 4/1 | 4/1 | 0/1 |
| last_exit_work_coefficient_at_two_thirds | 3/1 | 3/1 | 0/1 |
| sharp_Q_error_coefficient | 1/1 | 1/1 | 0/1 |
| signed_tail_positive_negative_split | 3/1 | 3/1 | 0/1 |
| plateau_is_not_forced_to_equal_full_domain | 2/1 | 2/1 | 0/1 |

## Finite enumeration

- The signed best-\(N\) rearrangement identity passes
  4490 exact integer-vector configurations.
- The \(\ell^1\)-Lipschitz estimate passes
  2916 vector-pair/\(N\) configurations,
  including 260 equality cases.
- The signed half-exit identity passes all
  6 rational piecewise-linear paths, including
  positive, negative, oscillatory, and zero terminals.
- The pointwise and best-\(N\) last-exit comparisons pass
  5488 and 2744
  exact checks, with 2135 sharp one-\(B_Q\) rows.
- The signed-\(F\)/nonnegative-\(K\) comparison passes
  2916 configurations, including
  509 equality cases.
- The plateau terminal reduction passes
  2916 radical-free squared-Cauchy fixtures.
- The simultaneous-plateau no-compression formulas pass
  390 exact configurations.
- The quantifier, cancellation, and strict plateau/full-domain witnesses all
  pass in `quantifier_cancellation_and_domain_fixtures`.

## Structural and source boundary

The certificate locks tags (S.200)--(S.222), both terminal domains, the
full-terminal interpretation of R0.74Q (Q.12), the good-terminal and
positive-terminal restrictions in the finite S.37 closure, and the separate
PROVED / INHERITED / REFUTED / OPEN / NOT CLAIMED ledgers.  It also requires
the explicit statement that terminal-tail continuity does not imply
continuity of the canonical last-exit selector.

## Negative mutations

- `mutation_half_exit_factor_one_rejected`: rejected.
- `mutation_replace_one_minus_theta_by_theta_rejected`: rejected.
- `mutation_drop_delta_Q_rejected`: rejected.
- `mutation_replace_one_BQ_by_half_BQ_rejected`: rejected.
- `mutation_allow_theta_three_quarters_strict_rejected`: rejected.
- `mutation_swap_sup_inf_quantifiers_rejected`: rejected.
- `mutation_replace_signed_tail_by_subset_sup_rejected`: rejected.
- `mutation_identify_plateau_with_full_domain_rejected`: rejected.
- `mutation_drop_positive_part_rejected`: rejected.
- `mutation_half_exit_one_half_to_one_rejected`: rejected.
- `mutation_full_Q12_domain_to_plateau_rejected`: rejected.
- `mutation_good_terminal_to_arbitrary_terminal_rejected`: rejected.
- `mutation_claim_half_exit_S37_admissible_rejected`: rejected.
- `mutation_claim_last_exit_selector_continuous_rejected`: rejected.
- `mutation_open_heading_to_proved_rejected`: rejected.
- `mutation_remove_refuted_heading_rejected`: rejected.
- `mutation_remove_final_tag_rejected`: rejected.
- `mutation_assert_plateau_full_equality_rejected`: rejected.

## Reproducibility

- Source note SHA-256: `85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd`
- Generator SHA-256: `0f04b79049ecd92c4a366ad9916fc8b6da9220b2f5baee34726aef2d4feaee65`
- JSON payload SHA-256: `26ee76d969d3aec5eec55d9fa981bce195538cc3e2464fc0ece2c46b7c4accf0`
- The output contains no timestamp, random input, floating-point calculation,
  network input, or non-standard Python dependency.
- Set `R074S_BEST_N_NOTE`, `R074S_BEST_N_JSON`, and
  `R074S_BEST_N_REPORT` to rebuild against explicit input/output paths.

## Boundary

This is a finite/algebraic and statement-integrity certificate.  It does not
machine-prove the inherited local-energy good-time theory, R0.74P variation
bounds, the R0.74Q terminal reduction, the R0.74O/P exact Navier--Stokes
family, any fixed-\(N_0\) PDE tail estimate, the future paid-branch residual,
regularity, or the Millennium problem.

**FINITE/ALGEBRAIC ONLY. INHERITED ANALYSIS NOT MACHINE-PROVED. NOT CLAY.**
