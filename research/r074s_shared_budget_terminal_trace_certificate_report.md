# R0.74S Step 11 — deterministic certificate report

- Schema: r074s-shared-budget-terminal-trace-certificate-v1
- Source: research/r074s_shared_budget_terminal_trace_obstruction.md
- Source SHA-256: fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693
- Exact checks: 14/14
- Finite checks: 7/7
- Structural checks: 34/34
- Negative mutations rejected: 7/7
- Overall: PASS

## Scope

This certificate checks finite exact algebra, rational fixtures, source
integrity, and claim boundaries.  It does not machine-prove the inherited
PDE estimates, either open branch-packing theorem, Q.12, Q.1, regularity,
or the Navier--Stokes Millennium problem.  **NOT CLAY.**

## Check groups

### Exact Checks

- **PASS** — duplicate_budget_joint_tail: S.252: one shared exception leaves one large coordinate.
- **PASS** — duplicate_budget_two_exceptions: Two exceptions, not one, delete both branches.
- **PASS** — adaptive_terminal_split_value: The pointwise adaptive branch split has worst value one.
- **PASS** — fixed_terminal_split_value: A split frozen across terminals has worst value M.
- **PASS** — common_h_integral: Exact trapezoidal integral in S.266.
- **PASS** — pure_defect_excess: Pure-defect selected excess.
- **PASS** — high_rayleigh_bump_integral: Quadratic bump integral.
- **PASS** — high_rayleigh_g_integral: High-Rayleigh viscous ancestor mass.
- **PASS** — high_rayleigh_sigma: Common h plus the early kinetic bump.
- **PASS** — high_rayleigh_excess: High-Rayleigh selected excess.
- **PASS** — both_clock_thresholds: Both rational rows lie in the intended selected-excess threshold class.
- **PASS** — flat_tower_best_N_formula: S.268 checked for four tower sizes and every admissible budget.
- **PASS** — N_plus_one_falsification_finite_fixture: Four targets above the total paid bound leave one residual after three deletions.
- **PASS** — persistent_lobe_positive_exponent: Inherited R0.74R second-shell payment exponent.

### Finite Checks

- **PASS** — shared_budget_infimal_convolution_exhaustive: S.249 checked on every five-coordinate disjoint state over values 0,1,2.
- **PASS** — selected_excess_ratio_grid_and_sharpness: S.262 checked on a finite feasible grid; scaled boundary fixtures leave margin four.
- **PASS** — dyadic_inverse_square_bounds: S.255 checked on three exact dyadic atoms.
- **PASS** — layer_cake_atomwise_identity: S.256 evaluated exactly atom by atom.
- **PASS** — critical_carleson_finite_log_growth: A critical quadratic tail coexists with an inverse moment equal to shell count.
- **PASS** — frozen_weight_eventual_ratio_elementary_bound: For k>=6 the exponent is at least 96; exp(96)>1+96>16 implies 8 exp(-96)<1/2.
- **PASS** — weighted_holder_cube_form: Finite weighted Hölder row underlying S.258, checked without floating point.

### Structural Checks

- **PASS** — locked_note_sha256: The analyzed note is byte-identical to the audited source.
- **PASS** — shared_budget_exact: Required source marker: \mathcal S_N(a+b)
 =\min_{0\le n\le N}
- **PASS** — domain_sup_min_warning: Required source marker: need not be an
equality because a supremum
- **PASS** — honest_two_N: Required source marker: best-\(2N\) combined estimate
- **PASS** — short_branch_domain: Required source marker: k\in\mathcal H_\tau:
- **PASS** — inverse_duration: Required source marker: a_kd_k^{-2}
- **PASS** — critical_carleson: Required source marker: critical exponent two
- **PASS** — nested_tent: Required source marker: nested-tent estimate
- **PASS** — terminal_trace: Required source marker: has no terminal
trace
- **PASS** — anti_concentration_open: Required source marker: \tag{S.261}
- **PASS** — rx_constants: Required source marker: {1\over5}x_k^{\rm sel}<r_k^x<3x_k^{\rm sel}
- **PASS** — fixed_solution_nonuniform: Required source marker: N=N(u,R,\varepsilon)
- **PASS** — pure_defect_tower: Required source marker: Repeating the pure-defect scalar row
- **PASS** — rx_gate_open: Required source marker: \tag{S.269}
- **PASS** — positive_denominator: Required source marker: \(A_R>0\)
- **PASS** — falsification_target: Required source marker: \tag{S.270}
- **PASS** — multipacket_cost: Required source marker: A_R^{(N)}:=(P_R^{M,(N)})^{2/3}
- **PASS** — bounded_search: Required source marker: The search is evidence against an immediate literature shortcut
- **PASS** — combined_open: Required source marker: \tag{S.272}
- **PASS** — stress_not_nse: Required source marker: ABSTRACT STRESS TESTS, NOT NSE COUNTEREXAMPLES
- **PASS** — not_clay: Required source marker: **NOT CLAY.**
- **PASS** — S248_S272_tags_consecutive: The twenty-five equation tags are consecutive and ordered.
- **PASS** — S248_S272_tags_unique: Every Step 11 tag occurs exactly once.
- **PASS** — display_math_balanced: Display-math delimiters balance.
- **PASS** — no_tabs_or_trailing_whitespace: Source has no tabs or trailing whitespace.
- **PASS** — no_forbidden_control_characters: Source has no hidden control characters.
- **PASS** — three_open_gates_not_promoted: S.261, S.269, and S.272 remain visibly open.
- **PASS** — literature_search_nonexhaustive: The bounded search is not presented as exhaustive.
- **PASS** — dependency_R0.74P: Frozen dependency hash.
- **PASS** — dependency_R0.74Q: Frozen dependency hash.
- **PASS** — dependency_R0.74R-step2: Frozen dependency hash.
- **PASS** — dependency_R0.74R-persistent: Frozen dependency hash.
- **PASS** — dependency_R0.74S-step8: Frozen dependency hash.
- **PASS** — dependency_R0.74S-step10: Frozen dependency hash.

### Negative Mutation Checks

- **PASS** — reject_min_to_max: Mutation must be rejected by shared_budget_exact.
- **PASS** — reject_rx_upper_constant_four: Mutation must be rejected by rx_constants.
- **PASS** — reject_missing_short_domain: Mutation must be rejected by short_branch_domain.
- **PASS** — reject_either_row_tower: Mutation must be rejected by pure_defect_tower.
- **PASS** — reject_zero_denominator_omission: Mutation must be rejected by positive_denominator.
- **PASS** — reject_open_to_proved: Mutation must be rejected by three_open_gates_not_promoted.
- **PASS** — reject_not_clay_removal: Mutation must be rejected by not_clay.
