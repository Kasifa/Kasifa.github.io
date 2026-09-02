#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent standard-library verifier for R0.74S Step 10.
#
# Exact Rational fixtures are evaluated before the primary Python producer
# contract is parsed.  This verifier checks finite algebra, quantifiers,
# source/audit/report byte locks, and the exact primary schema/identifier
# contract.  It does not machine-prove inherited suitable-weak analysis, a
# uniform residual packing theorem, Q.12, Q.1, regularity, or the Millennium
# problem.

require "digest"
require "json"
require "set"

REPO = File.expand_path("..", __dir__)

def input_path(environment_key, relative)
  File.expand_path(ENV.fetch(environment_key, File.join(REPO, relative)))
end

NOTE_PATH = input_path(
  "R074S_PAID_BRANCH_NOTE",
  "research/r074s_paid_branch_last_exit_residual.md"
)
PRIMARY_AUDIT_PATH = input_path(
  "R074S_PAID_BRANCH_PRIMARY_AUDIT",
  "research/r074s_paid_branch_last_exit_primary_audit.md"
)
INDEPENDENT_AUDIT_PATH = input_path(
  "R074S_PAID_BRANCH_INDEPENDENT_AUDIT",
  "research/r074s_paid_branch_last_exit_independent_audit.md"
)
GENERATOR_PATH = input_path(
  "R074S_PAID_BRANCH_GENERATOR",
  "scripts/r074s_paid_branch_last_exit_certificate.py"
)
PRIMARY_JSON_PATH = input_path(
  "R074S_PAID_BRANCH_JSON",
  "research/r074s_paid_branch_last_exit_certificate.json"
)
PRIMARY_REPORT_PATH = input_path(
  "R074S_PAID_BRANCH_REPORT",
  "research/r074s_paid_branch_last_exit_certificate_report.md"
)

DEPENDENCY_SPECS = {
  "R0.74P" => {
    "environment" => "R074S_PAID_BRANCH_DEP_R074P",
    "path" => "research/r074p_temporal_observable_triage.md",
    "sha256" => "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867"
  },
  "R0.74Q" => {
    "environment" => "R074S_PAID_BRANCH_DEP_R074Q",
    "path" => "research/r074q_problem_freeze.md",
    "sha256" => "42efa94f5310d8f7ce3cea1896ee1e0a8ddd9bddf5d588f9bb853c8696a1a962"
  },
  "R0.74R_Step2" => {
    "environment" => "R074S_PAID_BRANCH_DEP_R074R_STEP2",
    "path" => "research/r074r_arbitrary_clock_extraction_gate.md",
    "sha256" => "ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7"
  },
  "R0.74S_Step2" => {
    "environment" => "R074S_PAID_BRANCH_DEP_STEP2",
    "path" => "research/r074s_terminal_upcrossing_stopped_work.md",
    "sha256" => "3ec5f9b894f89e9febb95e5a100836b5b18e455f8366bf99e93b746ac6353da4"
  },
  "R0.74S_Step7" => {
    "environment" => "R074S_PAID_BRANCH_DEP_STEP7",
    "path" => "research/r074s_dissipation_rayleigh_gate.md",
    "sha256" => "e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3"
  },
  "R0.74S_Step8" => {
    "environment" => "R074S_PAID_BRANCH_DEP_STEP8",
    "path" => "research/r074s_defect_relaxed_total_rayleigh_excess.md",
    "sha256" => "0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab"
  },
  "R0.74S_Step9" => {
    "environment" => "R074S_PAID_BRANCH_DEP_STEP9",
    "path" => "research/r074s_best_n_last_exit_equivalence.md",
    "sha256" => "85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd"
  }
}.freeze

DEPENDENCY_PATHS = DEPENDENCY_SPECS.to_h do |label, spec|
  [label, input_path(spec.fetch("environment"), spec.fetch("path"))]
end.freeze

CANONICAL_PATHS = {
  "main_note" => "research/r074s_paid_branch_last_exit_residual.md",
  "primary_audit" => "research/r074s_paid_branch_last_exit_primary_audit.md",
  "independent_audit" => "research/r074s_paid_branch_last_exit_independent_audit.md",
  "primary_generator" => "scripts/r074s_paid_branch_last_exit_certificate.py",
  "primary_json" => "research/r074s_paid_branch_last_exit_certificate.json",
  "primary_report" => "research/r074s_paid_branch_last_exit_certificate_report.md"
}.freeze

EXPECTED_HASHES = {
  "main_note" => "9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c",
  "primary_audit" => "cf7bbfcb01a5389878a2a9f65ffa0e083863f8f6478986bc10110cfd24e6446c",
  "independent_audit" => "cb33dd2a1fed8a58f285bdb3e7a053480c40b06a899d1a1bd3a18549b6b8125a",
  "primary_generator" => "2763b3fa575ce723a400b6c7e5654d0a64c8a9db470d79097dc5a77769a365a9",
  "primary_json" => "8f37a8ce4d6513406297e6ce1e676ceaafa39776723bba839074120f206314de",
  "primary_report" => "6e25a07a417f96907e5e17da6b561830b75aa1a44d0b4b13fa56107dc31e4a5f"
}.freeze

ARTIFACT_PATHS = {
  "main_note" => NOTE_PATH,
  "primary_audit" => PRIMARY_AUDIT_PATH,
  "independent_audit" => INDEPENDENT_AUDIT_PATH,
  "primary_generator" => GENERATOR_PATH,
  "primary_json" => PRIMARY_JSON_PATH,
  "primary_report" => PRIMARY_REPORT_PATH
}.freeze

EXPECTED_PRIMARY_SCHEMA = "r074s-paid-branch-last-exit-certificate-v1"
INDEPENDENT_SCHEMA = "r074s-paid-branch-last-exit-independent-verifier-v1"

# This digest covers the sorted key set of every JSON object at every array
# position.  It therefore rejects an unknown or missing key anywhere in the
# producer contract without treating the locked producer artifact as a schema
# oracle.  The strict parser below separately rejects duplicate raw keys.
EXPECTED_PRIMARY_OBJECT_SCHEMA_SHA256 = "14f251e3479b63b95ef531b1e59cbb2975136ab88ee2831334d4f64d83c01dae"

EXPECTED_PRIMARY_SCOPE = {
  "finite_exact_fraction_and_statement_integrity_only" => true,
  "machine_proves_Q12_or_Q1" => false,
  "machine_proves_R211_R214" => false,
  "machine_proves_fixed_N_PDE_packing" => false,
  "machine_proves_inherited_good_time_theory" => false,
  "machine_proves_regularity_or_Clay" => false
}.freeze

EXPECTED_PRIMARY_IDS = {
  "exact_checks" => %w[
    two_thirds_last_exit_clock_increment
    positive_q_residual_lower_margin
    negative_q_residual_upper_margin
    lambda_four_exact_long_boundary
    long_payment_lambda_recovery
    C_LE_is_strictly_below_C4_by_cubes
    one_Q_ledger_sharp_pair
    one_cubic_ledger_Holder_equality
    plateau_Q_coefficient
    small_payment_fallback
    D_persistence_fixture_terminal_excess
    D_persistence_fixture_early_excess
  ],
  "finite_checks" => %w[
    D_first_full_truth_table_and_boundary_fixtures
    two_thirds_last_exit_not_first_exit_fixtures
    signed_delta_Q_sharp_residual_limits
    disjoint_Q_paid_rows_use_one_global_ledger
    combined_Psigma_PLE_one_cubic_Holder_ledger
    paid_deletion_same_set_and_best_N_enumeration
    shared_N_and_sup_inf_quantifier_witnesses
    fixed_N_finite_to_infinite_and_growing_budget_fixtures
    full_history_beta_sigma_not_last_exit_fixtures
    terminal_D_dominance_does_not_persist_on_last_exit_interval
  ],
  "structural_checks" => %w[
    locked_note_sha256
    S223_S247_tags_consecutive
    S223_S247_tags_unique
    display_math_line_delimiters_balanced
    inline_math_delimiters_balanced
    no_disallowed_control_or_zero_width_characters
    no_tabs_or_trailing_whitespace
    required_heading_00
    required_heading_01
    required_heading_02
    required_heading_03
    required_heading_04
    required_heading_05
    required_heading_06
    required_heading_07
    required_heading_08
    required_heading_09
    required_heading_10
    scope_not_clay
    fixed_profile_quantifiers
    canonical_last_exit_is_max
    last_exit_strict_after_stop
    delta_F_has_minus_delta_Q
    positive_terminal_restriction
    long_boundary_formula
    short_boundary_formula
    Q_large_boundary_formula
    Q_small_boundary_formula
    D_boundary_formula
    nonD_boundary_formula
    boundary_assignment_sentence
    full_history_not_last_exit
    beta_boundary_formula
    sigma_strict_boundary_formula
    D_first_priority
    absolute_Q_meaning
    low_Rayleigh_no_double_charge
    one_6BQ_statement
    a.e_nonD_persistence
    stop_value_not_used
    shell_dependent_sets
    one_C5_statement
    residual_union
    Ix_beta_nesting
    residual_strict_two_sided
    finite_Holder_before_monotone_limit
    monotone_convergence_for_infinite_shells
    best_N_nonnegative_domain
    best_N_infimum_formula
    same_set_before_infimum
    one_shared_N
    good_terminal_residual_gate
    K_only_domain_closure
    reverse_half_tail
    fixed_N_equivalence
    plateau_not_full
    full_gate_explicitly_open
    plateau_does_not_give_Q12
    sharp_Q_equality_paid
    fixed_N_not_truncation_budget
    D_persistence_invalid
    double_charge_truth_boundary
    open_claim_heading
    not_claimed_heading
    selector_regularities_not_claimed
    full_history_redefinition_not_claimed
    plateau_full_not_identified
    final_not_clay
    proved_ledger_keeps_S243_conditional
    inherited_ledger_names_all_four_steps
    refuted_ledger_preserves_nonsharp_truth
    open_ledger_contains_residual_Q12_and_Q1
    not_claimed_ledger_preserves_domain_and_Clay_boundaries
    source_R074P
    source_R074Q
    source_R074R
    source_Step7
    source_Step8
    source_Step9
  ],
  "negative_mutations" => %w[
    mutation_last_exit_to_first_exit_rejected
    mutation_D_equality_to_nonD_rejected
    mutation_beta_equality_to_failure_rejected
    mutation_sigma_equality_to_success_rejected
    mutation_long_equality_to_short_rejected
    mutation_Q_equality_to_small_rejected
    mutation_drop_absolute_Q_rejected
    mutation_Q_split_before_long_rejected
    mutation_Q_split_before_D_rejected
    mutation_DeltaF_minus_to_plus_DeltaQ_rejected
    mutation_residual_factor_six_to_five_rejected
    mutation_residual_half_to_two_fifths_rejected
    mutation_shared_N_to_two_branch_budgets_rejected
    mutation_sup_inf_to_inf_sup_rejected
    mutation_fixed_N_to_truncation_N_rejected
    mutation_full_beta_to_last_exit_beta_rejected
    mutation_full_sigma_to_last_exit_sigma_rejected
    mutation_terminal_D_to_last_exit_E_persistence_rejected
    mutation_source_last_exit_max_to_min_rejected
    mutation_source_DeltaF_sign_rejected
    mutation_source_D_boundary_ge_to_gt_rejected
    mutation_source_beta_boundary_ge_to_gt_rejected
    mutation_source_sigma_boundary_gt_to_ge_rejected
    mutation_source_long_boundary_ge_to_gt_rejected
    mutation_source_short_boundary_lt_to_le_rejected
    mutation_source_Q_boundary_ge_to_gt_rejected
    mutation_source_Qsmall_boundary_lt_to_le_rejected
    mutation_source_full_history_to_LE_rejected
    mutation_source_D_first_to_Q_first_rejected
    mutation_source_absolute_Q_to_signed_positive_rejected
    mutation_source_a.e_to_every_time_rejected
    mutation_source_same_set_to_separate_sets_rejected
    mutation_source_nonnegative_bestN_to_signed_without_positive_part_rejected
    mutation_source_finite_Holder_limit_removed_rejected
    mutation_source_one_shared_N_to_two_N_rejected
    mutation_source_good_gate_to_all_terminals_rejected
    mutation_source_K_continuity_to_residual_continuity_rejected
    mutation_source_fixed_profile_to_solution_dependent_rejected
    mutation_source_plateau_to_full_Q12_rejected
    mutation_source_OPEN_to_PROVED_rejected
    mutation_source_selector_continuity_claim_rejected
    mutation_source_remove_final_tag_rejected
    mutation_source_6BQ_to_12BQ_statement_drift_rejected
    mutation_source_C5_to_2C5_statement_drift_rejected
    mutation_source_nonsharp_double_charge_called_false_rejected
    mutation_source_D_persistence_warning_removed_rejected
    mutation_source_fixed_N_to_truncation_budget_rejected
  ]
}.freeze

EXPECTED_EXACT_PAYLOADS = {
  "two_thirds_last_exit_clock_increment" => %w[1/3 1/3 0/1],
  "positive_q_residual_lower_margin" => %w[1/60 1/60 0/1],
  "negative_q_residual_upper_margin" => %w[1/60 1/60 0/1],
  "lambda_four_exact_long_boundary" => %w[1/1 1/1 0/1],
  "long_payment_lambda_recovery" => %w[1/1 1/1 0/1],
  "C_LE_is_strictly_below_C4_by_cubes" => %w[32/1 32/1 0/1],
  "one_Q_ledger_sharp_pair" => %w[24/1 24/1 0/1],
  "one_cubic_ledger_Holder_equality" => %w[8/1 8/1 0/1],
  "plateau_Q_coefficient" => %w[7/1 7/1 0/1],
  "small_payment_fallback" => %w[1/8 1/8 0/1],
  "D_persistence_fixture_terminal_excess" => %w[2/5 2/5 0/1],
  "D_persistence_fixture_early_excess" => %w[7/100 7/100 0/1]
}.freeze

EXPECTED_FINITE_FIELDS = {
  "D_first_full_truth_table_and_boundary_fixtures" => {
    "predicate_configurations_checked" => 32,
    "boundary_fixture_count" => 9,
    "branch_counts" => {
      "P_LE" => 8, "P_Q" => 4, "P_beta" => 8,
      "P_sigma" => 4, "R_sh" => 4, "R_x" => 4
    }
  },
  "two_thirds_last_exit_not_first_exit_fixtures" => {
    "configurations_checked" => 3
  },
  "signed_delta_Q_sharp_residual_limits" => {
    "configurations_checked" => 4
  },
  "disjoint_Q_paid_rows_use_one_global_ledger" => {
    "Q_paid_shell_count" => 2,
    "terminal_sum" => "24/1",
    "used_variation" => "4/1",
    "full_B_Q" => "7/1"
  },
  "combined_Psigma_PLE_one_cubic_Holder_ledger" => {
    "configurations_checked" => 7380,
    "equality_cases" => 404
  },
  "paid_deletion_same_set_and_best_N_enumeration" => {
    "pointwise_same_set_checks" => 22_620,
    "best_N_forward_checks" => 9_018,
    "best_N_reverse_checks" => 9_018,
    "rearrangement_checks" => 18_036
  },
  "shared_N_and_sup_inf_quantifier_witnesses" => {
    "shared_combined_tail" => "1/1",
    "forbidden_branchwise_tail_sum" => "0/1",
    "sup_tau_inf_S" => "0/1",
    "inf_S_sup_tau" => "1/1"
  },
  "fixed_N_finite_to_infinite_and_growing_budget_fixtures" => {
    "configurations_checked" => 16,
    "infinite_S1_limit" => "1/2"
  },
  "full_history_beta_sigma_not_last_exit_fixtures" => {
    "beta_full_branch" => ["P_beta"],
    "beta_last_exit_mutation_branch" => ["R_x"],
    "sigma_full_branch" => ["P_sigma"],
    "sigma_last_exit_mutation_branch" => ["R_x"]
  },
  "terminal_D_dominance_does_not_persist_on_last_exit_interval" => {
    "last_exit" => "1/4",
    "normalized_duration" => "7/4",
    "terminal_D" => "3/5",
    "delta_D_after_last_exit" => "0/1",
    "D_nondecreasing" => true
  }
}.freeze

EXPECTED_SUMMARY = {
  "exact_passed" => 12,
  "exact_total" => 12,
  "finite_passed" => 10,
  "finite_total" => 10,
  "negative_mutations_passed" => 47,
  "negative_mutations_total" => 47,
  "structural_passed" => 79,
  "structural_total" => 79
}.freeze

EXPECTED_SOURCE_MUTATION_FAILURES = {
  "mutation_source_last_exit_max_to_min_rejected" => ["canonical_last_exit_is_max"],
  "mutation_source_DeltaF_sign_rejected" => ["delta_F_has_minus_delta_Q"],
  "mutation_source_D_boundary_ge_to_gt_rejected" => ["D_boundary_formula"],
  "mutation_source_beta_boundary_ge_to_gt_rejected" => ["beta_boundary_formula"],
  "mutation_source_sigma_boundary_gt_to_ge_rejected" => ["sigma_strict_boundary_formula"],
  "mutation_source_long_boundary_ge_to_gt_rejected" => ["long_boundary_formula"],
  "mutation_source_short_boundary_lt_to_le_rejected" => ["short_boundary_formula"],
  "mutation_source_Q_boundary_ge_to_gt_rejected" => ["Q_large_boundary_formula"],
  "mutation_source_Qsmall_boundary_lt_to_le_rejected" => ["Q_small_boundary_formula"],
  "mutation_source_full_history_to_LE_rejected" => ["full_history_not_last_exit"],
  "mutation_source_D_first_to_Q_first_rejected" => ["D_first_priority"],
  "mutation_source_absolute_Q_to_signed_positive_rejected" => ["absolute_Q_meaning"],
  "mutation_source_a.e_to_every_time_rejected" => ["a.e_nonD_persistence"],
  "mutation_source_same_set_to_separate_sets_rejected" => ["same_set_before_infimum"],
  "mutation_source_nonnegative_bestN_to_signed_without_positive_part_rejected" => ["best_N_nonnegative_domain"],
  "mutation_source_finite_Holder_limit_removed_rejected" => ["finite_Holder_before_monotone_limit"],
  "mutation_source_one_shared_N_to_two_N_rejected" => ["one_shared_N"],
  "mutation_source_good_gate_to_all_terminals_rejected" => ["good_terminal_residual_gate"],
  "mutation_source_K_continuity_to_residual_continuity_rejected" => ["K_only_domain_closure"],
  "mutation_source_fixed_profile_to_solution_dependent_rejected" => ["fixed_profile_quantifiers"],
  "mutation_source_plateau_to_full_Q12_rejected" => ["plateau_does_not_give_Q12"],
  "mutation_source_OPEN_to_PROVED_rejected" => ["full_gate_explicitly_open"],
  "mutation_source_selector_continuity_claim_rejected" => ["selector_regularities_not_claimed"],
  "mutation_source_remove_final_tag_rejected" => ["S223_S247_tags_consecutive"],
  "mutation_source_6BQ_to_12BQ_statement_drift_rejected" => ["one_6BQ_statement"],
  "mutation_source_C5_to_2C5_statement_drift_rejected" => ["one_C5_statement"],
  "mutation_source_nonsharp_double_charge_called_false_rejected" => [
    "double_charge_truth_boundary",
    "refuted_ledger_preserves_nonsharp_truth"
  ],
  "mutation_source_D_persistence_warning_removed_rejected" => ["D_persistence_invalid"],
  "mutation_source_fixed_N_to_truncation_budget_rejected" => ["fixed_N_not_truncation_budget"]
}.freeze

SOURCE_MUTATIONS_ALLOWING_TRUE_INEQUALITY = Set.new(%w[
  mutation_source_6BQ_to_12BQ_statement_drift_rejected
  mutation_source_C5_to_2C5_statement_drift_rejected
]).freeze

BRANCHES = %w[P_beta P_sigma P_LE P_Q R_sh R_x].freeze

def fraction_string(value)
  "#{value.numerator}/#{value.denominator}"
end

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

class RejectDuplicateKeysHash < Hash
  def []=(key, value)
    raise JSON::ParserError, "duplicate JSON key #{key.inspect}" if key?(key)

    super
  end
end

def strict_json_parse(bytes)
  source = bytes.dup.force_encoding(Encoding::UTF_8)
  raise JSON::ParserError, "primary JSON is not valid UTF-8" unless source.valid_encoding?

  parsed = JSON.parse(
    source,
    object_class: RejectDuplicateKeysHash,
    array_class: Array,
    create_additions: false
  )
  plain_json_value(parsed)
end

def plain_json_value(value)
  case value
  when Hash
    value.each_with_object({}) do |(key, entry), result|
      result[key] = plain_json_value(entry)
    end
  when Array
    value.map { |entry| plain_json_value(entry) }
  else
    value
  end
end

def object_schema_entries(value, path = [], entries = [])
  case value
  when Hash
    keys = value.keys.sort
    entries << [path, keys]
    keys.each do |key|
      object_schema_entries(value.fetch(key), path + [key], entries)
    end
  when Array
    value.each_with_index do |entry, index|
      object_schema_entries(entry, path + [index], entries)
    end
  end
  entries
end

def object_schema_sha256(value)
  Digest::SHA256.hexdigest(JSON.generate(object_schema_entries(value)))
end

def deep_copy(value)
  Marshal.load(Marshal.dump(value))
end

def subsets_up_to(length, maximum)
  (0..[length, maximum].min).flat_map do |size|
    (0...length).to_a.combination(size).to_a
  end
end

def best_n(values, maximum)
  subsets_up_to(values.length, maximum).map do |removed|
    removed_set = removed.to_set
    values.each_with_index.sum(Rational(0)) do |value, index|
      removed_set.include?(index) ? Rational(0) : value
    end
  end.min
end

def best_n_formula(values, maximum)
  values.sort.reverse.drop([maximum, values.length].min).sum(Rational(0))
end

def finite_group(identifier, cases, failures, details = {})
  {
    "id" => identifier,
    "cases" => cases,
    "failures" => failures.first(8),
    "details" => details,
    "pass" => failures.empty?
  }
end

def branch_memberships(d_side, beta_side, sigma_side, long_side, q_large_side)
  {
    "P_beta" => d_side && beta_side,
    "P_sigma" => d_side && !beta_side && sigma_side,
    "P_LE" => !d_side && long_side,
    "P_Q" => !d_side && !long_side && q_large_side,
    "R_sh" => !d_side && !long_side && !q_large_side,
    "R_x" => d_side && !beta_side && !sigma_side
  }
end

def numeric_branch(terminal:, dissipation:, beta:, sigma:, duration:, delta_q:)
  return [] unless terminal.positive?

  flags = branch_memberships(
    dissipation >= terminal / 2,
    beta >= terminal / 6,
    sigma > terminal / 12,
    duration >= 1,
    delta_q.abs >= terminal / 6
  )
  BRANCHES.select { |branch| flags.fetch(branch) }
end

def check_partition
  failures = []
  branch_counts = BRANCHES.to_h { |branch| [branch, 0] }
  cases = 0
  [false, true].repeated_permutation(5) do |predicates|
    cases += 1
    selected = BRANCHES.select do |branch|
      branch_memberships(*predicates).fetch(branch)
    end
    if selected.length == 1
      branch_counts[selected.first] += 1
    else
      failures << { "predicates" => predicates, "selected" => selected }
    end
  end

  f = ->(n, d = 1) { Rational(n, d) }
  fixtures = [
    ["zero", [f.call(0), f.call(0), f.call(0), f.call(0), f.call(0), f.call(0)], []],
    ["D_equal_beta_equal", [f.call(12), f.call(6), f.call(2), f.call(2), f.call(1), f.call(2)], ["P_beta"]],
    ["D_sigma_strict", [f.call(12), f.call(6), f.call(1), f.call(3, 2), f.call(1, 2), f.call(1)], ["P_sigma"]],
    ["D_sigma_equal", [f.call(12), f.call(6), f.call(3, 2), f.call(1), f.call(1, 2), f.call(3, 2)], ["R_x"]],
    ["nonD_long_equal", [f.call(12), f.call(5), f.call(0), f.call(0), f.call(1), f.call(2)], ["P_LE"]],
    ["short_Q_positive_equal", [f.call(12), f.call(5), f.call(0), f.call(0), f.call(1, 2), f.call(2)], ["P_Q"]],
    ["short_Q_negative_equal", [f.call(12), f.call(5), f.call(0), f.call(0), f.call(1, 2), f.call(-2)], ["P_Q"]],
    ["short_Q_positive_small", [f.call(12), f.call(5), f.call(0), f.call(0), f.call(1, 2), f.call(3, 2)], ["R_sh"]],
    ["short_Q_negative_small", [f.call(12), f.call(5), f.call(0), f.call(0), f.call(1, 2), f.call(-3, 2)], ["R_sh"]]
  ]
  fixtures.each do |identifier, args, expected|
    cases += 1
    actual = numeric_branch(
      terminal: args[0], dissipation: args[1], beta: args[2],
      sigma: args[3], duration: args[4], delta_q: args[5]
    )
    failures << { "fixture" => identifier, "actual" => actual, "expected" => expected } unless actual == expected
  end

  low_rayleigh_mass = Rational(1, 8) + Rational(1, 200)
  failures << { "fixture" => "low_Rayleigh_not_excluded" } unless low_rayleigh_mass > Rational(1, 12)
  finite_group(
    "independent_D_first_partition",
    cases,
    failures,
    "branch_counts" => branch_counts,
    "boundary_fixtures" => fixtures.length,
    "low_Rayleigh_mass" => fraction_string(low_rayleigh_mass)
  )
end

def level_hits(path, level)
  hits = []
  path.each { |time, value| hits << time if value == level }
  path.each_cons(2) do |left, right|
    left_time, left_value = left
    right_time, right_value = right
    if left_value == right_value
      hits.concat([left_time, right_time]) if left_value == level
      next
    end
    ratio = (level - left_value) / (right_value - left_value)
    hits << left_time + ratio * (right_time - left_time) if ratio.between?(0, 1)
  end
  hits.uniq.sort
end

def interpolate(path, time)
  path.each_cons(2) do |left, right|
    left_time, left_value = left
    right_time, right_value = right
    next unless left_time <= time && time <= right_time

    return right_value if right_time == left_time

    ratio = (time - left_time) / (right_time - left_time)
    return left_value + ratio * (right_value - left_value)
  end
  raise ArgumentError, "time outside path"
end

def check_last_exit
  f = ->(n, d = 1) { Rational(n, d) }
  fixtures = [
    [
      "oscillatory",
      [[f.call(0), f.call(0)], [f.call(1), f.call(9)], [f.call(2), f.call(6)], [f.call(3), f.call(8)], [f.call(4), f.call(12)]],
      f.call(8, 9), f.call(3)
    ],
    [
      "level_plateau",
      [[f.call(0), f.call(0)], [f.call(1), f.call(8)], [f.call(5, 2), f.call(8)], [f.call(4), f.call(12)]],
      f.call(1), f.call(5, 2)
    ],
    [
      "monotone",
      [[f.call(0), f.call(0)], [f.call(2), f.call(6)], [f.call(4), f.call(12)]],
      f.call(8, 3), f.call(8, 3)
    ]
  ]
  failures = []
  rows = []
  fixtures.each do |identifier, path, expected_first, expected_last|
    terminal = path.last[1]
    level = Rational(2, 3) * terminal
    hits = level_hits(path, level)
    first = hits.min
    last = hits.max
    passed = first == expected_first && last == expected_last && terminal - level == terminal / 3
    failures << { "fixture" => identifier } unless passed
    rows << {
      "id" => identifier,
      "first" => fraction_string(first),
      "last" => fraction_string(last)
    }
  end
  finite_group("independent_two_thirds_last_exit", fixtures.length, failures, "rows" => rows)
end

def check_residual_bounds
  failures = []
  cases = 0
  gaps = []
  [12, 30, 120, 1_200, 12_000].each do |denominator|
    epsilon = Rational(1, denominator)
    [Rational(1, 6) - epsilon, -Rational(1, 6) + epsilon].each do |delta_q|
      cases += 1
      residual = Rational(1, 3) - delta_q
      passed = delta_q.abs < Rational(1, 6) &&
               Rational(1, 6) < residual && residual < Rational(1, 2) &&
               Rational(2) * residual < 1 && 1 < Rational(6) * residual
      failures << { "epsilon" => fraction_string(epsilon), "delta_Q" => fraction_string(delta_q) } unless passed
      gaps << [residual - Rational(1, 6), Rational(1, 2) - residual]
    end
  end
  cases += 1
  failures << { "fixture" => "Q_equality_not_paid" } unless Rational(1, 6).abs >= Rational(1, 6)
  cases += 1
  nested = Rational(1) <= Rational(5, 4) && Rational(5, 4) <= Rational(3, 2) && Rational(3, 2) < Rational(2)
  failures << { "fixture" => "Ix_beta_nesting" } unless nested
  finite_group(
    "independent_residual_sign_and_sharp_limits",
    cases,
    failures,
    "smallest_boundary_gap" => fraction_string(gaps.flatten.min),
    "nested_beta_chain" => nested
  )
end

def check_one_q_ledger
  options = [
    ["P_beta", Rational(1, 3)],
    ["P_Q", Rational(1, 2)],
    ["other", Rational(2, 3)],
    ["none", Rational(0)]
  ]
  failures = []
  cases = 0
  equality_cases = 0
  (1..4).each do |length|
    options.repeated_permutation(length) do |coordinates|
      cases += 1
      used = coordinates.select { |label, _| %w[P_beta P_Q].include?(label) }
      terminal_sum = used.sum(Rational(0)) { |_, variation| 6 * variation }
      used_variation = used.sum(Rational(0)) { |_, variation| variation }
      full_ledger = coordinates.sum(Rational(0)) { |_, variation| variation }
      equality_cases += 1 if terminal_sum == 6 * full_ledger
      unless terminal_sum == 6 * used_variation && terminal_sum <= 6 * full_ledger
        failures << { "coordinates" => coordinates.map(&:first) }
      end
    end
  end
  finite_group(
    "independent_single_Q_ledger",
    cases,
    failures,
    "equality_cases" => equality_cases
  )
end

def check_cubic_holder
  values = [Rational(0), Rational(1, 2), Rational(1), Rational(3, 2)]
  failures = []
  cases = 0
  equality_cases = 0
  mixed_equality = false
  (1..3).each do |length|
    values.repeated_permutation(length) do |coefficients|
      values.repeated_permutation(length) do |payments|
        cases += 1
        left = coefficients.zip(payments).sum(Rational(0)) { |a, b| a * b * b }
        right_cube = coefficients.sum(Rational(0)) { |a| a**3 } *
                     payments.sum(Rational(0)) { |b| b**3 }**2
        left_cube = left**3
        equality_cases += 1 if left_cube == right_cube
        mixed_equality = true if length == 2 && coefficients == [1, 1] && payments == [1, 1]
        failures << { "length" => length } if left_cube > right_cube
      end
    end
  end
  failures << { "fixture" => "missing_mixed_equality" } unless mixed_equality
  finite_group(
    "independent_combined_cubic_Holder",
    cases,
    failures,
    "equality_cases" => equality_cases,
    "mixed_Psigma_PLE_equality" => mixed_equality
  )
end

def check_paid_deletion_best_n
  options = [
    [Rational(0), Rational(0), Rational(0)],
    [Rational(2), Rational(0), Rational(2)],
    [Rational(7), Rational(0), Rational(7)],
    [Rational(4), Rational(1), Rational(0)],
    [Rational(7), Rational(4, 3), Rational(0)],
    [Rational(2), Rational(3, 8), Rational(0)]
  ]
  failures = []
  pointwise = 0
  forward = 0
  reverse = 0
  rearrangements = 0
  (1..4).each do |length|
    options.repeated_permutation(length) do |coordinates|
      terminal = coordinates.map { |row| row[0] }
      residual = coordinates.map { |row| row[1] }
      paid = coordinates.sum(Rational(0)) { |row| row[2] }
      subsets_up_to(length, length).each do |removed|
        pointwise += 1
        removed_set = removed.to_set
        lhs = terminal.each_with_index.sum(Rational(0)) { |value, index| removed_set.include?(index) ? 0 : value }
        rhs = paid + 6 * residual.each_with_index.sum(Rational(0)) { |value, index| removed_set.include?(index) ? 0 : value }
        failures << { "kind" => "pointwise", "length" => length } if lhs > rhs
      end
      (0..(length + 1)).each do |maximum|
        forward += 1
        terminal_tail = best_n(terminal, maximum)
        residual_tail = best_n(residual, maximum)
        failures << { "kind" => "forward", "length" => length, "N" => maximum } if terminal_tail > paid + 6 * residual_tail
        reverse += 1
        failures << { "kind" => "reverse", "length" => length, "N" => maximum } if residual_tail > terminal_tail / 2
        rearrangements += 2
        unless terminal_tail == best_n_formula(terminal, maximum) && residual_tail == best_n_formula(residual, maximum)
          failures << { "kind" => "rearrangement", "length" => length, "N" => maximum }
        end
      end
    end
  end
  finite_group(
    "independent_paid_deletion_best_N",
    pointwise + forward + reverse + rearrangements,
    failures,
    "pointwise_same_set" => pointwise,
    "forward_best_N" => forward,
    "reverse_best_N" => reverse,
    "rearrangements" => rearrangements
  )
end

def check_quantifiers_and_domains
  failures = []
  cases = 0

  branch_x = [Rational(1), Rational(0)]
  branch_short = [Rational(0), Rational(1)]
  combined = branch_x.zip(branch_short).map(&:sum)
  shared = best_n(combined, 1)
  duplicated = best_n(branch_x, 1) + best_n(branch_short, 1)
  cases += 1
  failures << { "fixture" => "shared_exception_budget" } unless shared == 1 && duplicated.zero?

  states = [
    [Rational(1), Rational(0), Rational(0)],
    [Rational(0), Rational(1), Rational(0)],
    [Rational(0), Rational(0), Rational(1)]
  ]
  sup_inf = states.map { |state| best_n(state, 1) }.max
  fixed_costs = subsets_up_to(3, 1).map do |removed|
    removed_set = removed.to_set
    states.map do |state|
      state.each_with_index.sum(Rational(0)) { |value, index| removed_set.include?(index) ? 0 : value }
    end.max
  end
  inf_sup = fixed_costs.min
  cases += 1
  failures << { "fixture" => "sup_inf_order" } unless sup_inf.zero? && inf_sup == 1

  plateau_states = [[Rational(0), Rational(0)], [Rational(1, 2), Rational(0)]]
  full_states = plateau_states + [[Rational(2), Rational(1)]]
  plateau_sup = plateau_states.map { |state| best_n(state, 0) }.max
  full_sup = full_states.map { |state| best_n(state, 0) }.max
  cases += 1
  failures << { "fixture" => "plateau_full_domain" } unless plateau_sup == Rational(1, 2) && full_sup == 3

  approximants = (2..21).map do |denominator|
    time = Rational(denominator - 1, denominator)
    best_n([time, 2 * time], 1)
  end
  cases += approximants.length
  increasing = approximants.each_cons(2).all? { |left, right| left < right }
  endpoint_tail = best_n([Rational(1), Rational(2)], 1)
  failures << { "fixture" => "dense_good_terminal_approximation" } unless increasing && endpoint_tail == 1 && approximants.last == Rational(20, 21)

  vectors = [Rational(0), Rational(1, 2), Rational(1)].repeated_permutation(3).to_a
  vectors.product(vectors).each do |left, right|
    (0..2).each do |maximum|
      cases += 1
      difference = (best_n(left, maximum) - best_n(right, maximum)).abs
      l1 = left.zip(right).sum(Rational(0)) { |a, b| (a - b).abs }
      failures << { "fixture" => "l1_Lipschitz", "N" => maximum } if difference > l1
    end
  end

  finite_group(
    "independent_quantifier_and_domain_fixtures",
    cases,
    failures,
    "shared_tail" => fraction_string(shared),
    "duplicated_branch_tail" => fraction_string(duplicated),
    "sup_inf" => fraction_string(sup_inf),
    "inf_sup" => fraction_string(inf_sup),
    "plateau_sup" => fraction_string(plateau_sup),
    "full_sup" => fraction_string(full_sup),
    "last_good_approximant" => fraction_string(approximants.last)
  )
end

def check_fixed_n_truncation
  failures = []
  rows = []
  (1..12).each do |length|
    prefix = (1..length).map { |index| Rational(1, 2**index) }
    fixed = best_n(prefix, 1)
    expected = Rational(1, 2) - Rational(1, 2**length)
    growing = best_n(prefix, length)
    passed = fixed == expected && growing.zero?
    failures << { "M" => length } unless passed
    rows << [length, fraction_string(fixed), fraction_string(growing)]
  end
  finite_group(
    "independent_fixed_N_truncation",
    rows.length,
    failures,
    "rows" => rows,
    "infinite_fixed_N_limit" => "1/2"
  )
end

def check_full_history_and_D_counterexample
  failures = []
  cases = 0
  f = ->(n, d = 1) { Rational(n, d) }

  beta_full = numeric_branch(
    terminal: f.call(12), dissipation: f.call(6), beta: f.call(2),
    sigma: f.call(0), duration: f.call(1, 2), delta_q: f.call(0)
  )
  beta_last = numeric_branch(
    terminal: f.call(12), dissipation: f.call(6), beta: f.call(0),
    sigma: f.call(0), duration: f.call(1, 2), delta_q: f.call(0)
  )
  sigma_full = numeric_branch(
    terminal: f.call(12), dissipation: f.call(6), beta: f.call(1),
    sigma: f.call(3, 2), duration: f.call(1, 2), delta_q: f.call(0)
  )
  sigma_last = numeric_branch(
    terminal: f.call(12), dissipation: f.call(6), beta: f.call(1),
    sigma: f.call(0), duration: f.call(1, 2), delta_q: f.call(0)
  )
  cases += 2
  failures << { "fixture" => "full_history_beta" } unless beta_full == ["P_beta"] && beta_last == ["R_x"]
  failures << { "fixture" => "full_history_sigma" } unless sigma_full == ["P_sigma"] && sigma_last == ["R_x"]

  times = [f.call(0), f.call(1, 2), f.call(1), f.call(2), f.call(3)]
  k_values = [f.call(0), f.call(2, 3), f.call(2, 3), f.call(7, 10), f.call(1)]
  d_values = [f.call(0), f.call(2, 3), f.call(2, 3), f.call(2, 3), f.call(2, 3)]
  k_path = times.zip(k_values)
  d_path = times.zip(d_values)
  last_exit = level_hits(k_path, f.call(2, 3)).max
  early_times = [f.call(1), f.call(3, 2), f.call(2)]
  early_excess = early_times.map { |time| interpolate(k_path, time) - interpolate(d_path, time) }
  nonnegative = k_values.zip(d_values).all? { |k, d| k >= d }
  monotone_d = d_values.each_cons(2).all? { |left, right| left <= right }
  cases += 1
  counterexample_ok = last_exit == 1 &&
                      times.last - last_exit == 2 &&
                      d_values.last >= Rational(1, 2) &&
                      d_values[2] == d_values.last &&
                      early_excess.max < Rational(1, 6) &&
                      nonnegative && monotone_d
  failures << { "fixture" => "terminal_D_not_LE_persistence" } unless counterexample_ok

  finite_group(
    "independent_full_history_and_D_boundary",
    cases,
    failures,
    "beta_full" => beta_full,
    "beta_last_exit_mutation" => beta_last,
    "sigma_full" => sigma_full,
    "sigma_last_exit_mutation" => sigma_last,
    "D_counterexample_last_exit" => fraction_string(last_exit),
    "D_counterexample_duration" => fraction_string(times.last - last_exit),
    "D_counterexample_max_early_E" => fraction_string(early_excess.max)
  )
end

def independent_fixture_groups
  [
    check_partition,
    check_last_exit,
    check_residual_bounds,
    check_one_q_ledger,
    check_cubic_holder,
    check_paid_deletion_best_n,
    check_quantifiers_and_domains,
    check_fixed_n_truncation,
    check_full_history_and_D_counterexample
  ]
end

def note_structure_checks(body)
  return [{ "id" => "valid_UTF8", "pass" => false }] unless body.valid_encoding?

  tags = body.scan(/\\tag\{S\.(\d+)\}/).flatten.map(&:to_i)
  checks = {
    "valid_UTF8" => true,
    "S223_S247_consecutive" => tags == (223..247).to_a,
    "S223_S247_unique" => tags.uniq.length == 25,
    "title_is_Step10" => body.include?("R0.74S Step 10"),
    "D_first_partition_named" => body.include?("*D-first* priority rule"),
    "full_history_warning" => body.include?("not the last-exit interval"),
    "single_Q_ledger" => body.include?("one copy of \\(6B_Q\\)"),
    "single_cubic_ledger" => body.include?("unnecessary second copy"),
    "good_terminal_gate" => body.include?("good-terminal residual"),
    "K_only_closure" => body.include?("Only the inherited \\(\\ell^1\\)-continuity"),
    "S243_open" => body.include?("OPEN: there exist fixed"),
    "not_claimed_section" => body.include?("The following are **NOT CLAIMED**"),
    "final_not_clay" => body.rstrip.end_with?("**NOT CLAY.**"),
    "no_tabs" => !body.include?("\t"),
    "no_trailing_whitespace" => body.lines.none? { |line| line.match?(/[ \t]+$/) },
    "no_control_characters" => !body.match?(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/)
  }
  checks.map { |identifier, passed| { "id" => identifier, "pass" => !!passed } }
end

def nested_field_matches?(row, expected)
  row.is_a?(Hash) && expected.all? { |key, value| row[key] == value }
end

def validate_primary(payload, actual_hashes)
  errors = []
  return ["primary root is not an object"] unless payload.is_a?(Hash)

  schema_digest = object_schema_sha256(payload)
  unless schema_digest == EXPECTED_PRIMARY_OBJECT_SCHEMA_SHA256
    errors << "recursive object key schema mismatch"
  end

  expected_top_keys = %w[
    exact_checks finite_checks negative_mutations pass schema scope source
    structural_checks summary
  ].sort
  errors << "top-level key set mismatch" unless payload.keys.sort == expected_top_keys
  errors << "schema mismatch" unless payload["schema"] == EXPECTED_PRIMARY_SCHEMA
  errors << "producer pass is not true" unless payload["pass"] == true
  errors << "scope mismatch" unless payload["scope"] == EXPECTED_PRIMARY_SCOPE
  errors << "summary mismatch" unless payload["summary"] == EXPECTED_SUMMARY

  source = payload["source"]
  if source.is_a?(Hash)
    errors << "source note path mismatch" unless source["note"] == CANONICAL_PATHS["main_note"]
    errors << "source generator path mismatch" unless source["generator"] == CANONICAL_PATHS["primary_generator"]
    errors << "source note hash mismatch" unless source["note_sha256"] == actual_hashes["main_note"]
    errors << "locked note hash mismatch" unless source["locked_note_sha256"] == EXPECTED_HASHES["main_note"]
    errors << "source generator hash mismatch" unless source["generator_sha256"] == actual_hashes["primary_generator"]
  else
    errors << "source is not an object"
  end

  EXPECTED_PRIMARY_IDS.each do |group, expected_ids|
    rows = payload[group]
    unless rows.is_a?(Array)
      errors << "#{group} is not an array"
      next
    end
    ids = rows.map { |row| row.is_a?(Hash) ? row["id"] : nil }
    errors << "#{group} id order/set mismatch" unless ids == expected_ids
    errors << "#{group} has failed row" unless rows.all? { |row| row.is_a?(Hash) && row["pass"] == true }
    if group == "finite_checks"
      errors << "finite_checks contains nonempty failures" unless rows.all? do |row|
        !row.is_a?(Hash) || !row.key?("failures") || row["failures"] == []
      end
    end
  end


  all_ids = EXPECTED_PRIMARY_IDS.keys.flat_map do |group|
    rows = payload[group]
    rows.is_a?(Array) ? rows.map { |row| row.is_a?(Hash) ? row["id"] : nil } : []
  end
  expected_global_count = EXPECTED_PRIMARY_IDS.values.sum(&:length)
  unless all_ids.length == expected_global_count &&
         all_ids.none?(&:nil?) &&
         all_ids.uniq.length == expected_global_count
    errors << "check identifiers are not globally unique and complete"
  end

  exact_rows = payload["exact_checks"]
  if exact_rows.is_a?(Array)
    EXPECTED_EXACT_PAYLOADS.each do |identifier, expected|
      row = exact_rows.find do |candidate|
        candidate.is_a?(Hash) && candidate["id"] == identifier
      end
      actual = row.is_a?(Hash) ? [row["left"], row["right"], row["margin"]] : nil
      errors << "#{identifier} exact payload mismatch" unless actual == expected
    end
  end

  finite_rows = payload["finite_checks"]
  if finite_rows.is_a?(Array)
    EXPECTED_FINITE_FIELDS.each do |identifier, expected_fields|
      row = finite_rows.find do |candidate|
        candidate.is_a?(Hash) && candidate["id"] == identifier
      end
      errors << "#{identifier} finite payload mismatch" unless row && nested_field_matches?(row, expected_fields)
    end
  end


  mutation_rows = payload["negative_mutations"]
  if mutation_rows.is_a?(Array)
    EXPECTED_SOURCE_MUTATION_FAILURES.each do |identifier, expected_failures|
      row = mutation_rows.find { |candidate| candidate.is_a?(Hash) && candidate["id"] == identifier }
      next errors << "#{identifier} source mutation row missing" unless row

      expected_truth_value = SOURCE_MUTATIONS_ALLOWING_TRUE_INEQUALITY.include?(identifier)
      precise = row["kind"] == "source_mutation" &&
                row["changed"] == true &&
                row["baseline_structural_pass"] == true &&
                row["source_occurrences"] == 1 &&
                row["expected_failed_check"] == expected_failures.first &&
                row["mutated_structural_failures"] == expected_failures &&
                row["mutated_inequality_can_remain_true"] == expected_truth_value
      errors << "#{identifier} source mutation failure contract mismatch" unless precise
    end
  end
  errors
end

def contract_mutation_checks(payload, actual_hashes)
  mutations = {
    "wrong_schema" => [
      ->(copy) { copy["schema"] = "r074s-paid-branch-last-exit-certificate-v0" },
      ["schema mismatch"]
    ],
    "promote_machine_scope" => [
      ->(copy) { copy.fetch("scope")["machine_proves_Q12_or_Q1"] = true },
      ["scope mismatch"]
    ],
    "drop_exact_row_and_adjust_summary" => [
      lambda do |copy|
        copy.fetch("exact_checks").pop
        copy.fetch("summary")["exact_total"] -= 1
        copy.fetch("summary")["exact_passed"] -= 1
      end,
      [
        "recursive object key schema mismatch",
        "summary mismatch",
        "exact_checks id order/set mismatch",
        "check identifiers are not globally unique and complete",
        "D_persistence_fixture_early_excess exact payload mismatch"
      ]
    ],
    "duplicate_finite_id" => [
      ->(copy) { copy.fetch("finite_checks")[1]["id"] = copy.fetch("finite_checks")[0]["id"] },
      [
        "finite_checks id order/set mismatch",
        "check identifiers are not globally unique and complete",
        "two_thirds_last_exit_not_first_exit_fixtures finite payload mismatch"
      ]
    ],
    "flip_structural_pass" => [
      ->(copy) { copy.fetch("structural_checks")[0]["pass"] = false },
      ["structural_checks has failed row"]
    ],
    "drop_negative_mutation" => [
      ->(copy) { copy.fetch("negative_mutations").pop },
      [
        "recursive object key schema mismatch",
        "negative_mutations id order/set mismatch",
        "check identifiers are not globally unique and complete",
        "mutation_source_fixed_N_to_truncation_budget_rejected source mutation row missing"
      ]
    ],
    "tamper_exact_payload" => [
      ->(copy) { copy.fetch("exact_checks")[0]["left"] = "2/3" },
      ["two_thirds_last_exit_clock_increment exact payload mismatch"]
    ],
    "tamper_finite_count" => [
      ->(copy) { copy.fetch("finite_checks")[4]["configurations_checked"] += 1 },
      ["combined_Psigma_PLE_one_cubic_Holder_ledger finite payload mismatch"]
    ],
    "stale_note_hash" => [
      ->(copy) { copy.fetch("source")["note_sha256"] = "0" * 64 },
      ["source note hash mismatch"]
    ],
    "producer_pass_false" => [
      ->(copy) { copy["pass"] = false },
      ["producer pass is not true"]
    ],
    "unknown_top_level_key" => [
      ->(copy) { copy["unexpected"] = false },
      ["recursive object key schema mismatch", "top-level key set mismatch"]
    ],
    "missing_top_level_key" => [
      ->(copy) { copy.delete("pass") },
      [
        "recursive object key schema mismatch",
        "top-level key set mismatch",
        "producer pass is not true"
      ]
    ],
    "unknown_scope_key" => [
      ->(copy) { copy.fetch("scope")["unexpected"] = false },
      ["recursive object key schema mismatch", "scope mismatch"]
    ],
    "missing_source_key" => [
      ->(copy) { copy.fetch("source").delete("generator") },
      ["recursive object key schema mismatch", "source generator path mismatch"]
    ],
    "unknown_exact_row_key" => [
      ->(copy) { copy.fetch("exact_checks")[0]["unexpected"] = "0/1" },
      ["recursive object key schema mismatch"]
    ],
    "missing_exact_row_key" => [
      ->(copy) { copy.fetch("exact_checks")[0].delete("note") },
      ["recursive object key schema mismatch"]
    ],
    "merged_key_name_schema_collision" => [
      lambda do |copy|
        row = copy.fetch("structural_checks")[0]
        row["actual,enforced"] = [row.delete("actual"), row.delete("enforced")]
      end,
      ["recursive object key schema mismatch"]
    ],
    "reorder_exact_identifiers" => [
      ->(copy) { copy.fetch("exact_checks").rotate! },
      ["exact_checks id order/set mismatch"]
    ],
    "cross_group_duplicate_identifier" => [
      ->(copy) { copy.fetch("finite_checks")[0]["id"] = copy.fetch("exact_checks")[0]["id"] },
      [
        "finite_checks id order/set mismatch",
        "check identifiers are not globally unique and complete",
        "D_first_full_truth_table_and_boundary_fixtures finite payload mismatch"
      ]
    ],
    "nonempty_finite_failures_with_pass_true" => [
      ->(copy) { copy.fetch("finite_checks")[0]["failures"] = ["hidden"] },
      ["finite_checks contains nonempty failures"]
    ],
    "source_mutation_extra_failure" => [
      lambda do |copy|
        copy.fetch("negative_mutations")[18]["mutated_structural_failures"] << "unexpected"
      end,
      ["mutation_source_last_exit_max_to_min_rejected source mutation failure contract mismatch"]
    ]
  }
  mutations.map do |identifier, contract|
    mutation, expected_errors = contract
    copy = deep_copy(payload)
    mutation.call(copy)
    errors = validate_primary(copy, actual_hashes)
    {
      "id" => identifier,
      "errors" => errors,
      "expected_errors" => expected_errors,
      "rejected" => !errors.empty?,
      "pass" => errors == expected_errors
    }
  rescue KeyError, NoMethodError, TypeError => error
    { "id" => identifier, "rejected" => false, "error" => error.class.to_s, "pass" => false }
  end
end

def parser_self_checks(primary_bytes)
  source = primary_bytes.dup.force_encoding(Encoding::UTF_8)
  valid_utf8 = source.valid_encoding?
  rows = [{ "id" => "primary_JSON_valid_UTF8", "pass" => valid_utf8 }]
  unless valid_utf8
    rows << { "id" => "canonical_strict_parse", "pass" => false }
    rows << { "id" => "duplicate_raw_key_rejected", "pass" => false }
    return rows
  end

  begin
    strict_json_parse(source)
    rows << { "id" => "canonical_strict_parse", "pass" => true }
  rescue JSON::ParserError
    rows << { "id" => "canonical_strict_parse", "pass" => false }
  end

  duplicate_bytes = source.sub(/\A\{/, '{"schema":"duplicate",')
  begin
    strict_json_parse(duplicate_bytes)
    rows << { "id" => "duplicate_raw_key_rejected", "pass" => false }
  rescue JSON::ParserError => error
    rows << {
      "id" => "duplicate_raw_key_rejected",
      "error_class" => error.class.to_s,
      "pass" => error.message.include?("duplicate JSON key")
    }
  end
  rows
end

def report_checks(body, actual_hashes)
  return [{ "id" => "valid_UTF8", "pass" => false }] unless body.valid_encoding?

  checks = {
    "valid_UTF8" => true,
    "reports_PASS" => body.include?("**PASS**"),
    "reports_exact_count" => body.include?("12/12 exact rows"),
    "reports_finite_count" => body.include?("10/10 finite groups"),
    "reports_structural_count" => body.include?("79/79 source/claim checks"),
    "reports_mutation_count" => body.include?("47/47"),
    "binds_note_hash" => body.include?(actual_hashes["main_note"]),
    "binds_generator_hash" => body.include?(actual_hashes["primary_generator"]),
    "binds_json_hash" => body.include?(actual_hashes["primary_json"]),
    "binds_schema" => body.include?(EXPECTED_PRIMARY_SCHEMA),
    "denies_machine_PDE_proof" => body.include?("does not machine-prove"),
    "finite_algebraic_boundary" => body.include?("FINITE/ALGEBRAIC ONLY"),
    "not_clay" => body.include?("NOT CLAY")
  }
  checks.map { |identifier, passed| { "id" => identifier, "pass" => !!passed } }
end

def audit_binding_checks(primary_body, independent_body)
  locked_hash = EXPECTED_HASHES["main_note"]
  primary_valid = primary_body.valid_encoding?
  independent_valid = independent_body.valid_encoding?
  checks = {
    "primary_audit_valid_UTF8" => primary_valid,
    "independent_audit_valid_UTF8" => independent_valid,
    "primary_audit_binds_main" => primary_valid && primary_body.include?(locked_hash),
    "primary_audit_passes_25_rows" => primary_valid && primary_body.include?("All twenty-five numbered statements"),
    "primary_audit_keeps_S243_open" => primary_valid && primary_body.include?("remains explicitly open"),
    "independent_audit_binds_main" => independent_valid && independent_body.include?(locked_hash),
    "independent_audit_PASS" => independent_valid && independent_body.include?("PASS, with no mathematical reservation"),
    "independent_audit_keeps_S243_open" => independent_valid && independent_body.include?("(S.243) remains")
  }
  DEPENDENCY_SPECS.each do |label, spec|
    checks["primary_audit_binds_#{label}"] =
      primary_valid && primary_body.include?(spec.fetch("sha256"))
  end
  checks.map { |identifier, passed| { "id" => identifier, "pass" => !!passed } }
end

# Independent Rational mathematics is intentionally completed before the
# primary producer JSON is opened or its contract is inspected.
independent_checks = independent_fixture_groups

artifact_checks = ARTIFACT_PATHS.map do |label, path|
  actual = File.file?(path) ? sha256(path) : nil
  expected = EXPECTED_HASHES.fetch(label)
  {
    "id" => label,
    "path" => CANONICAL_PATHS.fetch(label),
    "actual_sha256" => actual,
    "expected_sha256" => expected,
    "pass" => actual == expected
  }
end
actual_hashes = artifact_checks.to_h { |row| [row.fetch("id"), row["actual_sha256"]] }

dependency_checks = DEPENDENCY_SPECS.map do |label, spec|
  path = DEPENDENCY_PATHS.fetch(label)
  actual = File.file?(path) ? sha256(path) : nil
  {
    "id" => label,
    "path" => spec.fetch("path"),
    "actual_sha256" => actual,
    "expected_sha256" => spec.fetch("sha256"),
    "pass" => actual == spec.fetch("sha256")
  }
end

missing_labels = ARTIFACT_PATHS.keys.reject { |label| File.file?(ARTIFACT_PATHS.fetch(label)) }
if missing_labels.empty?
  note_body = File.binread(NOTE_PATH).force_encoding(Encoding::UTF_8)
  note_checks = note_structure_checks(note_body)

  # Producer inspection begins only here.
  primary_bytes = File.binread(PRIMARY_JSON_PATH)
  parser_rows = parser_self_checks(primary_bytes)
  begin
    primary_payload = strict_json_parse(primary_bytes)
    primary_schema_digest = object_schema_sha256(primary_payload)
    primary_errors = validate_primary(primary_payload, actual_hashes)
    mutation_checks = contract_mutation_checks(primary_payload, actual_hashes)
  rescue JSON::ParserError, EncodingError, ArgumentError
    primary_payload = nil
    primary_schema_digest = nil
    primary_errors = ["strict JSON parse failed"]
    mutation_checks = []
  end
  report_rows = report_checks(
    File.binread(PRIMARY_REPORT_PATH).force_encoding(Encoding::UTF_8),
    actual_hashes
  )
  audit_rows = audit_binding_checks(
    File.binread(PRIMARY_AUDIT_PATH).force_encoding(Encoding::UTF_8),
    File.binread(INDEPENDENT_AUDIT_PATH).force_encoding(Encoding::UTF_8)
  )
else
  note_checks = []
  parser_rows = []
  primary_schema_digest = nil
  primary_errors = ["missing artifacts: #{missing_labels.sort.join(',')}"]
  mutation_checks = []
  report_rows = []
  audit_rows = []
end

pass = independent_checks.all? { |row| row.fetch("pass") } &&
       artifact_checks.length == ARTIFACT_PATHS.length &&
       artifact_checks.all? { |row| row.fetch("pass") } &&
       dependency_checks.length == DEPENDENCY_SPECS.length &&
       dependency_checks.all? { |row| row.fetch("pass") } &&
       note_checks.all? { |row| row.fetch("pass") } &&
       parser_rows.all? { |row| row.fetch("pass") } &&
       primary_errors.empty? &&
       mutation_checks.all? { |row| row.fetch("pass") } &&
       report_rows.all? { |row| row.fetch("pass") } &&
       audit_rows.all? { |row| row.fetch("pass") }

output = {
  "schema" => INDEPENDENT_SCHEMA,
  "artifacts" => artifact_checks,
  "dependencies" => dependency_checks,
  "independent_checks" => independent_checks,
  "note_checks" => note_checks,
  "parser_checks" => parser_rows,
  "primary_contract" => {
    "schema" => EXPECTED_PRIMARY_SCHEMA,
    "object_schema_sha256" => primary_schema_digest,
    "expected_object_schema_sha256" => EXPECTED_PRIMARY_OBJECT_SCHEMA_SHA256,
    "expected_counts" => EXPECTED_SUMMARY,
    "errors" => primary_errors,
    "pass" => primary_errors.empty?
  },
  "contract_mutations" => mutation_checks,
  "report_checks" => report_rows,
  "audit_binding_checks" => audit_rows,
  "scope" => {
    "standard_library_Ruby_only" => true,
    "rational_fixtures_run_before_primary_contract" => true,
    "strict_duplicate_unknown_and_missing_key_rejection" => true,
    "locks_seven_upstream_dependencies" => true,
    "uses_timestamp_random_network_or_gems" => false,
    "machine_proves_inherited_good_time_analysis" => false,
    "machine_proves_R211_R214" => false,
    "machine_proves_fixed_N_PDE_packing" => false,
    "machine_proves_Q12_Q1_regularity_or_Clay" => false
  },
  "summary" => {
    "independent_groups_passed" => independent_checks.count { |row| row.fetch("pass") },
    "independent_groups_total" => independent_checks.length,
    "independent_cases" => independent_checks.sum { |row| row.fetch("cases") },
    "artifact_hashes_passed" => artifact_checks.count { |row| row.fetch("pass") },
    "artifact_hashes_total" => ARTIFACT_PATHS.length,
    "dependency_hashes_passed" => dependency_checks.count { |row| row.fetch("pass") },
    "dependency_hashes_total" => DEPENDENCY_SPECS.length,
    "note_checks_passed" => note_checks.count { |row| row.fetch("pass") },
    "note_checks_total" => note_checks.length,
    "parser_checks_passed" => parser_rows.count { |row| row.fetch("pass") },
    "parser_checks_total" => parser_rows.length,
    "contract_mutations_rejected" => mutation_checks.count { |row| row.fetch("pass") },
    "contract_mutations_total" => mutation_checks.length,
    "report_checks_passed" => report_rows.count { |row| row.fetch("pass") },
    "report_checks_total" => report_rows.length,
    "audit_bindings_passed" => audit_rows.count { |row| row.fetch("pass") },
    "audit_bindings_total" => audit_rows.length
  },
  "pass" => pass
}

puts JSON.pretty_generate(output)
exit(pass ? 0 : 1)
