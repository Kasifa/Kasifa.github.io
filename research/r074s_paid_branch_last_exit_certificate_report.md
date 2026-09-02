# R0.74S paid-branch last-exit certificate report

## Result

**PASS** — 12/12 exact rows,
10/10 finite groups,
79/79 source/claim checks,
and 47/47
negative mutations passed.

## Exact rational checks

| Check | Left | Right | Margin |
|---|---:|---:|---:|
| two_thirds_last_exit_clock_increment | 1/3 | 1/3 | 0/1 |
| positive_q_residual_lower_margin | 1/60 | 1/60 | 0/1 |
| negative_q_residual_upper_margin | 1/60 | 1/60 | 0/1 |
| lambda_four_exact_long_boundary | 1/1 | 1/1 | 0/1 |
| long_payment_lambda_recovery | 1/1 | 1/1 | 0/1 |
| C_LE_is_strictly_below_C4_by_cubes | 32/1 | 32/1 | 0/1 |
| one_Q_ledger_sharp_pair | 24/1 | 24/1 | 0/1 |
| one_cubic_ledger_Holder_equality | 8/1 | 8/1 | 0/1 |
| plateau_Q_coefficient | 7/1 | 7/1 | 0/1 |
| small_payment_fallback | 1/8 | 1/8 | 0/1 |
| D_persistence_fixture_terminal_excess | 2/5 | 2/5 | 0/1 |
| D_persistence_fixture_early_excess | 7/100 | 7/100 | 0/1 |

## Finite groups

| Group | Primary count | Result |
|---|---:|---:|
| D_first_full_truth_table_and_boundary_fixtures | 32 | PASS |
| two_thirds_last_exit_not_first_exit_fixtures | 3 | PASS |
| signed_delta_Q_sharp_residual_limits | 4 | PASS |
| disjoint_Q_paid_rows_use_one_global_ledger | 2 | PASS |
| combined_Psigma_PLE_one_cubic_Holder_ledger | 7380 | PASS |
| paid_deletion_same_set_and_best_N_enumeration | 22620 | PASS |
| shared_N_and_sup_inf_quantifier_witnesses | 1 | PASS |
| fixed_N_finite_to_infinite_and_growing_budget_fixtures | 16 | PASS |
| full_history_beta_sigma_not_last_exit_fixtures | 1 | PASS |
| terminal_D_dominance_does_not_persist_on_last_exit_interval | 1 | PASS |

The D-first Boolean truth table covers
32 predicate configurations and
9 exact endpoint fixtures, with every one of
the six branches reached and exactly one branch selected for every positive
terminal row.  The paid-deletion enumeration checks
22620 same-set inequalities,
9018 forward best-N inequalities, and
9018 reverse half-tail inequalities.  The combined
cubic ledger passes 7380 radical-free cubed
Holder checks, including a mixed P_sigma/P_LE equality row.

The remaining groups certify last-versus-first exit, both signed sharp
residual limits, one combined Q ledger, a shared exception budget, the
sup-inf order, finite-prefix fixtures illustrating fixed-N versus
growing-budget behavior, full-history versus last-exit classification, and
the rational terminal-D counterexample.

## Source and claim boundary

The producer locks the exact source bytes and consecutive unique tags
(S.223)--(S.247).  It checks the full-history Step 8 classes, D-first
priority, all strict/equality conventions, a.e. non-D persistence, the
single 6 B_Q and C5 ledgers, one shared N, good-terminal residual domain,
K-only terminal closure, plateau/full separation, and distinct PROVED,
INHERITED, REFUTED OR RULED OUT, OPEN, and NOT CLAIMED ledgers.

## Negative mutations

| Mutation | Classification | Result |
|---|---|---:|
| mutation_last_exit_to_first_exit_rejected | false_formula | rejected |
| mutation_D_equality_to_nonD_rejected | false_formula | rejected |
| mutation_beta_equality_to_failure_rejected | false_formula | rejected |
| mutation_sigma_equality_to_success_rejected | false_formula | rejected |
| mutation_long_equality_to_short_rejected | false_formula | rejected |
| mutation_Q_equality_to_small_rejected | false_formula | rejected |
| mutation_drop_absolute_Q_rejected | false_formula | rejected |
| mutation_Q_split_before_long_rejected | false_formula | rejected |
| mutation_Q_split_before_D_rejected | false_formula | rejected |
| mutation_DeltaF_minus_to_plus_DeltaQ_rejected | false_formula | rejected |
| mutation_residual_factor_six_to_five_rejected | false_inequality | rejected |
| mutation_residual_half_to_two_fifths_rejected | false_inequality | rejected |
| mutation_shared_N_to_two_branch_budgets_rejected | wrong_quantifier | rejected |
| mutation_sup_inf_to_inf_sup_rejected | wrong_quantifier | rejected |
| mutation_fixed_N_to_truncation_N_rejected | wrong_quantifier | rejected |
| mutation_full_beta_to_last_exit_beta_rejected | wrong_interval | rejected |
| mutation_full_sigma_to_last_exit_sigma_rejected | wrong_interval | rejected |
| mutation_terminal_D_to_last_exit_E_persistence_rejected | false_persistence | rejected |
| mutation_source_last_exit_max_to_min_rejected | false_definition | rejected |
| mutation_source_DeltaF_sign_rejected | false_formula | rejected |
| mutation_source_D_boundary_ge_to_gt_rejected | strict_boundary_drift | rejected |
| mutation_source_beta_boundary_ge_to_gt_rejected | strict_boundary_drift | rejected |
| mutation_source_sigma_boundary_gt_to_ge_rejected | strict_boundary_drift | rejected |
| mutation_source_long_boundary_ge_to_gt_rejected | strict_boundary_drift | rejected |
| mutation_source_short_boundary_lt_to_le_rejected | overlapping_boundary_drift | rejected |
| mutation_source_Q_boundary_ge_to_gt_rejected | strict_boundary_drift | rejected |
| mutation_source_Qsmall_boundary_lt_to_le_rejected | overlapping_boundary_drift | rejected |
| mutation_source_full_history_to_LE_rejected | wrong_interval | rejected |
| mutation_source_D_first_to_Q_first_rejected | overlapping_priority | rejected |
| mutation_source_absolute_Q_to_signed_positive_rejected | false_sign_rule | rejected |
| mutation_source_a.e_to_every_time_rejected | false_good_time_extension | rejected |
| mutation_source_same_set_to_separate_sets_rejected | wrong_quantifier | rejected |
| mutation_source_nonnegative_bestN_to_signed_without_positive_part_rejected | wrong_positive_part_domain | rejected |
| mutation_source_finite_Holder_limit_removed_rejected | invalid_infinite_step | rejected |
| mutation_source_one_shared_N_to_two_N_rejected | wrong_quantifier | rejected |
| mutation_source_good_gate_to_all_terminals_rejected | unsupported_closure | rejected |
| mutation_source_K_continuity_to_residual_continuity_rejected | unsupported_regularity | rejected |
| mutation_source_fixed_profile_to_solution_dependent_rejected | wrong_quantifier | rejected |
| mutation_source_plateau_to_full_Q12_rejected | wrong_domain | rejected |
| mutation_source_OPEN_to_PROVED_rejected | claim_inflation | rejected |
| mutation_source_selector_continuity_claim_rejected | claim_inflation | rejected |
| mutation_source_remove_final_tag_rejected | source_integrity | rejected |
| mutation_source_6BQ_to_12BQ_statement_drift_rejected | statement_integrity_nonsharp_drift | rejected |
| mutation_source_C5_to_2C5_statement_drift_rejected | statement_integrity_nonsharp_drift | rejected |
| mutation_source_nonsharp_double_charge_called_false_rejected | claim_boundary_drift | rejected |
| mutation_source_D_persistence_warning_removed_rejected | false_persistence | rejected |
| mutation_source_fixed_N_to_truncation_budget_rejected | wrong_quantifier | rejected |

The `6B_Q -> 12B_Q` and `C5 -> 2C5` mutations are rejected as
statement-integrity drift.  Their looser inequalities may remain true; this
certificate does not mislabel them as algebraically false.

## Reproducibility

- Expected locked note SHA-256: `9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c`
- Actual note SHA-256: `9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c`
- Generator SHA-256: `2763b3fa575ce723a400b6c7e5654d0a64c8a9db470d79097dc5a77769a365a9`
- JSON payload SHA-256: `8f37a8ce4d6513406297e6ce1e676ceaafa39776723bba839074120f206314de`
- Schema: `r074s-paid-branch-last-exit-certificate-v1`
- No timestamp, random input, floating-point arithmetic, network input, or
  non-standard Python dependency is used.
- `R074S_PAID_BRANCH_NOTE`, `R074S_PAID_BRANCH_JSON`, and
  `R074S_PAID_BRANCH_REPORT` provide explicit deterministic path overrides.

## Boundary

This is a finite rational-algebra and statement-integrity certificate.  It
does not machine-prove the inherited local-energy theory, R.211/R.214, a
fixed solution- and scale-independent residual packing theorem, Q.12, Q.1,
regularity, or the Millennium problem.

**FINITE/ALGEBRAIC ONLY. INHERITED ANALYSIS NOT MACHINE-PROVED. NOT CLAY.**
