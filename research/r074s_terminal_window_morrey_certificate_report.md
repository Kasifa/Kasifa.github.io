# R0.74S Step 12 — deterministic certificate report

- Schema: r074s-terminal-window-morrey-certificate-v1
- Source: research/r074s_terminal_window_morrey_packing.md
- Source SHA-256: 03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f
- Exact checks: 16/16
- Finite checks: 12/12
- Structural checks: 51/51
- Negative mutations rejected: 11/11
- Overall: PASS

## Scope

This certificate checks exact finite algebra, rational scaling
bookkeeping, integer cover counts, an elementary super-Gaussian tail
criterion, frozen hashes, primary links, and claim-boundary wording.
It does not machine-prove the inherited PDE estimates, either universal
packing gate, the conditional Morrey hypothesis for the bare class, Q.12,
Q.1, regularity, or the Navier--Stokes Millennium problem.  **NOT CLAY.**

## Check groups

### Exact Checks

- **PASS** — terminal_interval_inclusion_1: For d<=delta, the last-exit interval lies in the common terminal window.
- **PASS** — terminal_interval_inclusion_2: For d<=delta, the last-exit interval lies in the common terminal window.
- **PASS** — terminal_interval_inclusion_3: For d<=delta, the last-exit interval lies in the common terminal window.
- **PASS** — terminal_interval_inclusion_4: For d<=delta, the last-exit interval lies in the common terminal window.
- **PASS** — delta_inverse_two_thirds_1_2: For a rational cube delta=a^3, delta^(-2/3)=a^(-2) exactly.
- **PASS** — delta_inverse_two_thirds_1_4: For a rational cube delta=a^3, delta^(-2/3)=a^(-2) exactly.
- **PASS** — delta_inverse_two_thirds_3_2: For a rational cube delta=a^3, delta^(-2/3)=a^(-2) exactly.
- **PASS** — frozen_packet_full_variation: S.304: B times 65 R^2 is at most 65/32 after the R^2 factors cancel.
- **PASS** — frozen_packet_no_winding_rational_margin: The exact stronger comparison 65/32<3, together with the standard pi>3, implies 65/32<2 pi without floating point.
- **PASS** — frozen_packet_terminal_window_variation: S.304: the four-R^2 terminal window has variation at most 1/8.
- **PASS** — frozen_packet_terminal_window_one_eighth: The terminal-window variation reduces exactly to 1/8.
- **PASS** — averaged_balance_delta_power: Balancing delta P/eta with delta^(-2/3) A gives delta proportional to (eta A/P)^(3/5).
- **PASS** — averaged_balance_eta_exponent: The optimized exceptional-terminal factor is eta^(-2/5).
- **PASS** — averaged_balance_A_exponent: The optimized A exponent is 3/5.
- **PASS** — averaged_balance_P_exponent_before_substitution: The remaining explicit payment exponent is 2/5.
- **PASS** — averaged_balance_four_fifths_after_A_substitution: Substitution A=P^(2/3) gives the S.284 exponent 4/5.

### Finite Checks

- **PASS** — best_N_layer_cake_exhaustive: S.278 is checked exactly on every length-at-most-four vector over five rational levels.
- **PASS** — best_N_l1_Lipschitz_exhaustive: The S.276 one-Lipschitz estimate is checked exactly on all ordered pairs in a rational grid.
- **PASS** — common_window_shallow_deep_split_exhaustive: A common deletion set pays every shallow coordinate by its window majorant and every deep coordinate by one positive-depth debt.
- **PASS** — synchronized_spike_exact_ratios: S.281 is checked with cube-valued M and H, so every normalized P^(2/3) ratio remains rational and grows with H at fixed M.
- **PASS** — conditional_min_cap_P_small_P_large: S.294 is checked separately for P<=1 (P<=P^(2/3)) and P>=1 (1<=P^(2/3)).
- **PASS** — exception_budget_union_exhaustive: S.286 is checked exactly, including overlapping supports: defect and high-Rayleigh deletion budgets add.
- **PASS** — conditional_charging_Holder_exhaustive: The shellwise Holder row behind S.287 is checked after cubing, with p_k chosen as exact rational cubes.
- **PASS** — moving_tube_cover_count_arithmetic: The normalized greedy count has the S.291 shape 2^(3k)+L 2^(2k), with one explicit harmless cover constant.
- **PASS** — monotone_periodic_occupation_exact_fixtures: S.305 is checked exactly for constant-speed paths after circumference normalization, with both endpoint inequalities attained.
- **PASS** — mixed_norm_R_exponents_cancel_exactly: S.297--S.299 scale exponents are checked as Fractions, including the allowed q=infinity endpoint and finite r.
- **PASS** — super_Gaussian_eventual_geometric_tail: For polynomial weights 2^(mk), m=0,...,5, an exact elementary exp lower bound yields an eventual ratio below 1/2 and hence a two-term geometric tail cap.
- **PASS** — abstract_super_Gaussian_best_N_filter: S.306 is checked on exact rational Gamma,H,p fixtures: deletion of the first N terms, adjacent ratios, and the geometric cap all agree.

### Structural Checks

- **PASS** — locked_note_sha256: The analyzed Step 12 note is byte-identical to the frozen source.
- **PASS** — common_terminal_window_definition: Required compact source marker: J_{\tau,\delta}&:=(\max\{s_R,\tau-\deltaR^2\},\tau)
- **PASS** — short_deep_reduction: Required compact source marker: \mathcalS_N(r^{\rmsh}(\tau))\le\mathcalV^F_{N,R}(\tau,\delta)+C_{\rmdeep}\delta^{-2/3}A_R
- **PASS** — best_N_Lipschitz: Required compact source marker: |\mathcalS_N(a)-\mathcalS_N(b)|&\le\|a-b\|_{\ell^1}
- **PASS** — layer_cake_identity: Required compact source marker: \mathcalS_N(z)=\int_0^\infty\bigl(n_z(t)-N\bigr)_+\,dt
- **PASS** — window_gate_open: Required compact source marker: \tag{S.280}
- **PASS** — synchronized_spike: Required compact source marker: \tag{S.281}
- **PASS** — four_fifths_boundary: Required compact source marker: (P_R^M)^{4/5}
- **PASS** — optimizer_inside_admissible_delta_range: Required compact source marker: \delta\asymp(\etaA_R/P_R^M)^{3/5}\)liesin\((0,4)\)
- **PASS** — exception_budgets_add: Required compact source marker: \mathcalS_{N_D+N_H}(d^{\rmdef}+h)\le\mathcalS_{N_D}(d^{\rmdef})+\mathcalS_{N_H}(h)
- **PASS** — ancestor_gate_open: Required compact source marker: \tag{S.288}
- **PASS** — moving_tube_cover: Required compact source marker: C_\psi\bigl(2^{3k}+L2^{2k}\bigr)
- **PASS** — conditional_min_cap: Required compact source marker: \mathcalS_0(x^{\rmsel}(\tau))\le\max\{C_0,B(M,L)\}A_R
- **PASS** — mixed_norm_definition: Required compact source marker: \mathcalU_{q,r}(R):=R^{1-\theta}\|u\|_{L_t^q(I_{8R};L_x^r(\mathbbT^3))}\leM_*
- **PASS** — path_exponent_zero: Required compact source marker: R^{-1-3/r+2-2/q+\theta-1}=CM_*
- **PASS** — combined_open_gate: Required compact source marker: \tag{S.303}
- **PASS** — no_winding_full_interval: Required compact source marker: \operatorname{Var}_{[0,65R^2]}Q\le{65\over32}<2\pi
- **PASS** — no_winding_terminal_window: Required compact source marker: \operatorname{Var}_{I_{2R}}Q\le{1\over8}
- **PASS** — occupation_lower_bound: Required compact source marker: {m|J|\overB}\le\tau_J
- **PASS** — occupation_upper_bound: Required compact source marker: \tau_J\le{(m+1)|J|\over\betaB}
- **PASS** — super_Gaussian_filter_hypothesis: Required compact source marker: q_N:=2^p\Gamma^{3\cdot4^N}<1
- **PASS** — super_Gaussian_filter_conclusion: Required compact source marker: \mathcalS_N(z)\le\sum_{\ell\geN}z_\ell\le{H2^{pN}\Gamma^{4^N}\over1-q_N}
- **PASS** — not_clay: Required literal source marker: **NOT CLAY.**
- **PASS** — common_window_continuity: Required literal source marker: continuous common-window gate
- **PASS** — uniform_modulus_not_claimed: Required literal source marker: The modulus in
(S.277) depends on the solution and scale.
- **PASS** — conditional_benchmark: Required literal source marker: conditional benchmark, not a theorem for the bare suitable-weak class
- **PASS** — abstract_not_NSE: Required literal source marker: ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES
- **PASS** — super_Gaussian_boundary: Required literal source marker: super-Gaussian
- **PASS** — kinematic_screen: Required literal source marker: kinematic screen
- **PASS** — speed_not_missing_ingredient: Required literal source marker: rule out speed alone as the missing
ingredient
- **PASS** — bounded_search_boundary: Required literal source marker: The search is evidence against an immediate literature shortcut
- **PASS** — primary_link_1: Required primary-source link.
- **PASS** — primary_link_2: Required primary-source link.
- **PASS** — primary_link_3: Required primary-source link.
- **PASS** — primary_link_4: Required primary-source link.
- **PASS** — primary_link_5: Required primary-source link.
- **PASS** — primary_link_6: Required primary-source link.
- **PASS** — S273_final_tags_consecutive: Step 12 equation tags are consecutive, ordered, and reach the frozen final tag.
- **PASS** — S273_final_tags_unique: Every frozen Step 12 equation tag occurs exactly once.
- **PASS** — three_universal_gates_remain_open: S.280, S.288, and S.303 remain visibly open.
- **PASS** — conditional_not_bare_class: Morrey and mixed-norm conclusions remain conditional.
- **PASS** — display_math_balanced: Display-math delimiters balance.
- **PASS** — no_tabs_or_trailing_whitespace: Source has no tabs or trailing whitespace.
- **PASS** — no_forbidden_control_characters: Source has LF newlines and no embedded control characters.
- **PASS** — no_DNS_claim: The analytic certificate is not presented as DNS.
- **PASS** — dependency_R0.74P: Frozen dependency hash.
- **PASS** — dependency_R0.74R-arbitrary: Frozen dependency hash.
- **PASS** — dependency_R0.74R-persistent: Frozen dependency hash.
- **PASS** — dependency_R0.74S-step8: Frozen dependency hash.
- **PASS** — dependency_R0.74S-step11: Frozen dependency hash.
- **PASS** — dependency_R0.74F-packet: Frozen dependency hash.

### Negative Mutation Checks

- **PASS** — reject_layer_cake_missing_positive_part: Mutation must be rejected by layer_cake_identity.
- **PASS** — reject_wrong_four_fifths_endpoint: Mutation must be rejected by four_fifths_boundary.
- **PASS** — reject_max_to_min_cap: Mutation must be rejected by conditional_min_cap.
- **PASS** — reject_budget_sum_to_max: Mutation must be rejected by exception_budgets_add.
- **PASS** — reject_open_to_proved: Mutation must be rejected by three_universal_gates_remain_open.
- **PASS** — reject_conditional_boundary_removal: Mutation must be rejected by conditional_benchmark.
- **PASS** — reject_not_clay_removal: Mutation must be rejected by not_clay.
- **PASS** — reject_CKN_primary_link_removal: Mutation must be rejected by primary_link_1.
- **PASS** — reject_super_Gaussian_boundary_removal: Mutation must be rejected by super_Gaussian_boundary.
- **PASS** — reject_occupation_beta_denominator: Mutation must be rejected by occupation_upper_bound.
- **PASS** — reject_super_Gaussian_ratio_exponent: Mutation must be rejected by super_Gaussian_filter_hypothesis.
