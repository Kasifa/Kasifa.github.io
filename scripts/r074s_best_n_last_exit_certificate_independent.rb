#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent finite/algebraic verifier for R0.74S Step 9.
#
# The mathematics is rebuilt below with Ruby Rational before the primary
# Python producer is inspected.  Environment overrides make the verifier
# relocatable: two directories containing byte-identical inputs must produce
# byte-identical JSON.  This certificate does not machine-prove the inherited
# Navier--Stokes, local-energy, density-of-good-times, or regularity results.

require "digest"
require "json"
require "set"

REPO = File.expand_path("..", __dir__)

NOTE_PATH = File.expand_path(
  ENV.fetch(
    "R074S_LAST_EXIT_NOTE",
    File.join(REPO, "research/r074s_best_n_last_exit_equivalence.md")
  )
)
PRIMARY_JSON_PATH = File.expand_path(
  ENV.fetch(
    "R074S_LAST_EXIT_JSON",
    File.join(REPO, "research/r074s_best_n_last_exit_certificate.json")
  )
)
PRIMARY_GENERATOR_PATH = File.expand_path(
  ENV.fetch(
    "R074S_LAST_EXIT_GENERATOR",
    File.join(REPO, "scripts/r074s_best_n_last_exit_certificate.py")
  )
)
PRIMARY_REPORT_PATH = File.expand_path(
  ENV.fetch(
    "R074S_LAST_EXIT_REPORT",
    File.join(REPO, "research/r074s_best_n_last_exit_certificate_report.md")
  )
)

EXPECTED_NOTE_FIELD = "research/r074s_best_n_last_exit_equivalence.md"
EXPECTED_JSON_FIELD = "research/r074s_best_n_last_exit_certificate.json"
EXPECTED_GENERATOR_FIELD = "scripts/r074s_best_n_last_exit_certificate.py"
EXPECTED_REPORT_FIELD = "research/r074s_best_n_last_exit_certificate_report.md"
EXPECTED_NOTE_SHA256 = "85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd"
EXPECTED_PRIMARY_GENERATOR_SHA256 = "0f04b79049ecd92c4a366ad9916fc8b6da9220b2f5baee34726aef2d4feaee65"
EXPECTED_PRIMARY_JSON_SHA256 = "26ee76d969d3aec5eec55d9fa981bce195538cc3e2464fc0ece2c46b7c4accf0"
EXPECTED_PRIMARY_REPORT_SHA256 = "1108b72113d84b90ebc5570c2c7b4bfaa1ccdc299525c557979b564109ab6481"
EXPECTED_PRIMARY_SCHEMA = "r074s-best-n-last-exit-certificate-v1"

# Filled from the independently reviewed producer contract.  Exact identifier
# sets, rather than summary counts alone, make a row deletion detectable even
# when a stale producer also edits its summary.
EXPECTED_PRIMARY_IDS = {
  "exact_checks" => %w[
    half_exit_two_halves_recover_terminal_flux
    two_thirds_last_exit_increment
    strict_quarter_upcrossing_margin
    one_sixth_signed_increment_margin
    clock_reduction_BQ_coefficient_at_two_thirds
    last_exit_work_coefficient_at_two_thirds
    sharp_Q_error_coefficient
    signed_tail_positive_negative_split
    plateau_is_not_forced_to_equal_full_domain
  ],
  "finite_checks" => %w[
    best_N_signed_tail_rearrangement_enumeration
    best_N_l1_Lipschitz_enumeration
    signed_half_exit_piecewise_linear_fixtures
    K_last_exit_one_BQ_enumeration
    signed_F_nonnegative_K_best_N_comparison
    plateau_terminal_reduction_squared_Cauchy_enumeration
    quantifier_cancellation_and_domain_fixtures
    simultaneous_plateau_no_compression_enumeration
  ],
  "structural_checks" => %w[
    locked_note_sha256
    S200_S222_tags_consecutive
    S200_S222_tags_unique
    display_math_balanced
    inline_math_balanced
    no_disallowed_control_characters
    required_section_50a178dbd6b9
    required_section_10e509d582ad
    required_section_2640c5af5654
    required_section_ca8a878092e9
    required_section_14686a66fbd1
    required_section_c094a0ff861a
    required_section_2ac79847958a
    required_section_f12c3f9639c6
    required_section_065ced81d5d0
    required_text_08fb3a7005b8
    required_text_d84842950c2e
    required_text_2d43ea1858bd
    required_text_2702bd57c5a6
    required_text_1ecbd389ee11
    required_text_f173f5b3c5e4
    required_text_365da6caf9ee
    required_text_ac2676912847
    required_text_8ca243a31ad1
    required_text_4f0b13963538
    required_text_b101459fde56
    required_text_1e78f062db02
    required_text_a89d7e4da1f4
    required_text_df507ff27f5c
    required_text_88bda8ce5c81
    required_text_dfdcc60d2643
    required_text_2a751a0e41a0
    required_text_83521546d61a
    required_text_171e292ebbe1
    required_text_80f5371794fc
    required_formula_a5c64ed77b11
    required_formula_0f7df94d6eec
    required_formula_4e2d8117f057
    required_formula_d7fee0a16585
    required_formula_2c3e22c8fec9
    required_formula_0f299108227e
    required_formula_194e4d118d2c
    required_formula_85bcaa11c5c8
    required_formula_9a1a172e6ec8
    required_formula_84c1ac94cea9
    required_formula_d23bc21e28ba
    required_formula_3895c5bb57ef
    required_formula_beaae77f7936
    proved_contains_only_reductions_and_equivalences
    inherited_binds_P_Q_and_Step8
    refuted_contains_no_exception_but_preserves_S38
    open_contains_best_N_PDE_and_Q1
    not_claimed_contains_selector_domain_and_Clay_boundaries
    source_ledger_4602129d7f24
    source_ledger_42f05018e4c1
    source_ledger_fc80df0f6adb
    source_ledger_0bcfa95c7c0f
  ],
  "negative_mutations" => %w[
    mutation_half_exit_factor_one_rejected
    mutation_replace_one_minus_theta_by_theta_rejected
    mutation_drop_delta_Q_rejected
    mutation_replace_one_BQ_by_half_BQ_rejected
    mutation_allow_theta_three_quarters_strict_rejected
    mutation_swap_sup_inf_quantifiers_rejected
    mutation_replace_signed_tail_by_subset_sup_rejected
    mutation_identify_plateau_with_full_domain_rejected
    mutation_drop_positive_part_rejected
    mutation_half_exit_one_half_to_one_rejected
    mutation_full_Q12_domain_to_plateau_rejected
    mutation_good_terminal_to_arbitrary_terminal_rejected
    mutation_claim_half_exit_S37_admissible_rejected
    mutation_claim_last_exit_selector_continuous_rejected
    mutation_open_heading_to_proved_rejected
    mutation_remove_refuted_heading_rejected
    mutation_remove_final_tag_rejected
    mutation_assert_plateau_full_equality_rejected
  ]
}.freeze
EXPECTED_PRIMARY_STRUCTURAL_COUNT = 57
REQUIRED_PRIMARY_STRUCTURAL_IDS = %w[
  locked_note_sha256
  S200_S222_tags_consecutive
  S200_S222_tags_unique
  refuted_contains_no_exception_but_preserves_S38
  open_contains_best_N_PDE_and_Q1
  not_claimed_contains_selector_domain_and_Clay_boundaries
].freeze
EXPECTED_PRIMARY_SCOPE = {
  "finite_algebraic_and_statement_integrity_only" => true,
  "machine_proves_Navier_Stokes_PDE" => false,
  "machine_proves_R0_74Q_PDE_tail_bound" => false,
  "machine_proves_good_time_theory" => false,
  "machine_proves_inherited_variation_bounds" => false,
  "machine_proves_regularity_or_Clay" => false
}.freeze
EXPECTED_PRIMARY_EXACT_VALUES = {
  "half_exit_two_halves_recover_terminal_flux" => ["1/1", "1/1", "0/1"],
  "two_thirds_last_exit_increment" => ["1/3", "1/3", "0/1"],
  "strict_quarter_upcrossing_margin" => ["1/12", "1/12", "0/1"],
  "one_sixth_signed_increment_margin" => ["1/6", "1/6", "0/1"],
  "clock_reduction_BQ_coefficient_at_two_thirds" => ["4/1", "4/1", "0/1"],
  "last_exit_work_coefficient_at_two_thirds" => ["3/1", "3/1", "0/1"],
  "sharp_Q_error_coefficient" => ["1/1", "1/1", "0/1"],
  "signed_tail_positive_negative_split" => ["3/1", "3/1", "0/1"],
  "plateau_is_not_forced_to_equal_full_domain" => ["2/1", "2/1", "0/1"]
}.freeze
EXPECTED_PRIMARY_FINITE_COUNTS = {
  "best_N_signed_tail_rearrangement_enumeration" => ["configurations_checked", 4490],
  "best_N_l1_Lipschitz_enumeration" => ["configurations_checked", 2916],
  "signed_half_exit_piecewise_linear_fixtures" => ["configurations_checked", 6],
  "K_last_exit_one_BQ_enumeration" => ["best_N_tail_checks", 2744],
  "signed_F_nonnegative_K_best_N_comparison" => ["configurations_checked", 2916],
  "plateau_terminal_reduction_squared_Cauchy_enumeration" => ["configurations_checked", 2916],
  "simultaneous_plateau_no_compression_enumeration" => ["configurations_checked", 390]
}.freeze

def positive_part(value)
  [value, Rational(0)].max
end

def rational_string(value)
  "#{value.numerator}/#{value.denominator}"
end

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

def deep_copy(value)
  Marshal.load(Marshal.dump(value))
end

def compact_source(body)
  body.gsub(/\s+/, "").delete("&").gsub(/\\[,!;:]/, "")
end

def subsets_up_to(length, nmax)
  (0..[length, nmax].min).flat_map do |size|
    (0...length).to_a.combination(size).to_a
  end
end

def vectors(values, length)
  return [[]] if length.zero?

  vectors(values, length - 1).flat_map do |prefix|
    values.map { |value| prefix + [value] }
  end
end

def s_n_bruteforce(vector, nmax)
  subsets_up_to(vector.length, nmax).map do |removed|
    removed_set = removed.to_set
    positive_part(
      vector.each_with_index.sum(Rational(0)) do |value, index|
        removed_set.include?(index) ? Rational(0) : value
      end
    )
  end.min
end

def s_n_raw_inf_then_positive(vector, nmax)
  raw_inf = subsets_up_to(vector.length, nmax).map do |removed|
    removed_set = removed.to_set
    vector.each_with_index.sum(Rational(0)) do |value, index|
      removed_set.include?(index) ? Rational(0) : value
    end
  end.min
  positive_part(raw_inf)
end

def s_n_rearranged(vector, nmax)
  largest_positive = vector.select(&:positive?).sort.reverse.first(nmax)
  positive_part(vector.sum(Rational(0)) - largest_positive.sum(Rational(0)))
end

def l1_distance(left, right)
  left.zip(right).sum(Rational(0)) { |a, b| (a - b).abs }
end

def value_at(samples, time)
  last = samples.length - 1
  return samples.fetch(last) if time == last

  left = time.floor
  fraction = time - left
  samples.fetch(left) + fraction * (samples.fetch(left + 1) - samples.fetch(left))
end

# Last time at which the piecewise-linear sample path is <= threshold.
# The final sample is assumed to be strictly above threshold.
def last_leq_exit(samples, threshold)
  candidate = nil
  (0...(samples.length - 1)).each do |index|
    left = samples.fetch(index)
    right = samples.fetch(index + 1)
    if right <= threshold
      candidate = Rational(index + 1)
    elsif left <= threshold && right > threshold
      candidate = Rational(index) + (threshold - left) / (right - left)
    end
  end
  candidate
end

def finite_group(identifier, cases, failures, extra = {})
  {
    "id" => identifier,
    "cases" => cases,
    "failures" => failures.first(8),
    "failure_count" => failures.length,
    "pass" => failures.empty?
  }.merge(extra)
end

def check_s_n_reconstruction
  values = [-1, Rational(-1, 2), 0, Rational(1, 2), 1].map { |x| Rational(x) }
  failures = []
  cases = 0
  cancellation_cases = 0
  vectors(values, 4).each do |vector|
    (0..4).each do |nmax|
      direct = s_n_bruteforce(vector, nmax)
      rearranged = s_n_rearranged(vector, nmax)
      commuted = s_n_raw_inf_then_positive(vector, nmax)
      cases += 1
      cancellation_cases += 1 if vector.any?(&:positive?) && vector.any?(&:negative?) && direct.zero?
      next if direct == rearranged && direct == commuted

      failures << {
        "vector" => vector.map { |x| rational_string(x) },
        "N" => nmax,
        "direct" => rational_string(direct),
        "rearranged" => rational_string(rearranged),
        "commuted" => rational_string(commuted)
      }
    end
  end
  finite_group(
    "signed_S_N_rearrangement_and_positive_infimum_commutation",
    cases,
    failures,
    "cancellation_cases" => cancellation_cases
  )
end

def check_s_n_lipschitz
  values = [-1, Rational(-1, 2), 0, Rational(1, 2), 1].map { |x| Rational(x) }
  fixtures = vectors(values, 3)
  failures = []
  equality_cases = 0
  cases = 0
  fixtures.each do |left|
    fixtures.each do |right|
      (0..3).each do |nmax|
        lhs = (s_n_bruteforce(left, nmax) - s_n_bruteforce(right, nmax)).abs
        rhs = l1_distance(left, right)
        cases += 1
        equality_cases += 1 if lhs == rhs && rhs.positive?
        next if lhs <= rhs

        failures << {
          "left" => left.map { |x| rational_string(x) },
          "right" => right.map { |x| rational_string(x) },
          "N" => nmax,
          "lhs" => rational_string(lhs),
          "rhs" => rational_string(rhs)
        }
      end
    end
  end
  finite_group(
    "S_N_l1_Lipschitz_constant_one",
    cases,
    failures,
    "positive_equality_cases" => equality_cases
  )
end

def check_half_exit_paths
  middle_values = [-2, -1, 0, 1, 2].map { |x| Rational(x) }
  terminal_values = [-2, -1, 0, 1, 2].map { |x| Rational(x) }
  failures = []
  cases = 0
  positive_terminals = 0
  negative_terminals = 0
  zero_terminals = 0
  vectors(middle_values, 3).each do |middle|
    terminal_values.each do |terminal|
      samples = [Rational(0)] + middle + [terminal]
      if terminal.zero?
        ell = Rational(samples.length - 1)
        delta = terminal - value_at(samples, ell)
        zero_terminals += 1
        valid = delta.zero?
      else
        sign = terminal.positive? ? Rational(1) : Rational(-1)
        transformed = samples.map { |value| sign * value }
        ell = last_leq_exit(transformed, terminal.abs / 2)
        at_exit = ell.nil? ? nil : value_at(samples, ell)
        delta = ell.nil? ? nil : terminal - at_exit
        positive_terminals += 1 if terminal.positive?
        negative_terminals += 1 if terminal.negative?
        valid = !ell.nil? && at_exit == terminal / 2 && delta == terminal / 2
      end
      cases += 1
      next if valid

      failures << {
        "samples" => samples.map { |x| rational_string(x) },
        "ell" => ell&.then { |x| rational_string(x) },
        "delta" => delta&.then { |x| rational_string(x) }
      }
    end
  end
  finite_group(
    "signed_half_exit_piecewise_linear_reconstruction",
    cases,
    failures,
    "positive_terminals" => positive_terminals,
    "negative_terminals" => negative_terminals,
    "zero_terminals" => zero_terminals
  )
end

def check_half_exit_best_n_identity
  values = [-2, -1, 0, 1, 2].map { |x| Rational(x) }
  failures = []
  cases = 0
  vectors(values, 4).each do |terminal_vector|
    increments = terminal_vector.map { |value| value / 2 }
    (0..4).each do |nmax|
      left = s_n_bruteforce(increments, nmax)
      right = s_n_bruteforce(terminal_vector, nmax) / 2
      cases += 1
      next if left == right

      failures << {
        "terminal" => terminal_vector.map { |x| rational_string(x) },
        "N" => nmax,
        "left" => rational_string(left),
        "right" => rational_string(right)
      }
    end
  end
  finite_group("half_exit_equals_one_half_signed_best_N_tail", cases, failures)
end

def check_k_last_exit_paths
  ratios = [0, Rational(1, 2), 1, Rational(3, 2), 2].map { |x| Rational(x) }
  terminals = [Rational(1, 2), 1, Rational(3, 2), 2].map { |x| Rational(x) }
  thetas = [Rational(1, 4), Rational(1, 3), Rational(1, 2), Rational(2, 3), Rational(3, 4), Rational(4, 5)]
  failures = []
  cases = 0
  strict_cases = 0
  endpoint_cases = 0
  vectors(ratios, 3).each do |middle_ratios|
    terminals.each do |terminal|
      samples = [Rational(0)] + middle_ratios.map { |ratio| ratio * terminal } + [terminal]
      thetas.each do |theta|
        ell = last_leq_exit(samples, theta * terminal)
        at_exit = ell.nil? ? nil : value_at(samples, ell)
        delta = ell.nil? ? nil : terminal - at_exit
        strict_expected = theta < Rational(3, 4)
        strict_actual = !delta.nil? && delta > terminal / 4
        strict_cases += 1 if strict_actual
        endpoint_cases += 1 if theta == Rational(3, 4)
        cases += 1
        next if !ell.nil? && at_exit == theta * terminal && delta == (1 - theta) * terminal && strict_actual == strict_expected

        failures << {
          "samples" => samples.map { |x| rational_string(x) },
          "theta" => rational_string(theta),
          "ell" => ell&.then { |x| rational_string(x) },
          "at_exit" => at_exit&.then { |x| rational_string(x) },
          "strict_actual" => strict_actual,
          "strict_expected" => strict_expected
        }
      end
    end
  end
  finite_group(
    "K_theta_last_exit_and_strict_upcrossing_boundary",
    cases,
    failures,
    "strict_cases" => strict_cases,
    "theta_three_quarters_cases" => endpoint_cases,
    "zero_terminal_strict_upcrossing" => false
  )
end

def check_one_bq_perturbation
  terminal_vectors = vectors([0, 1, 2].map { |x| Rational(x) }, 3)
  delta_q_vectors = vectors([-1, 0, 1].map { |x| Rational(x) }, 3)
  thetas = [Rational(1, 3), Rational(1, 2), Rational(2, 3), Rational(4, 5)]
  failures = []
  cases = 0
  sharp_cases = 0
  terminal_vectors.each do |terminal_vector|
    delta_q_vectors.each do |delta_q|
      bq = delta_q.sum(Rational(0)) { |value| value.abs }
      thetas.each do |theta|
        coefficient = 1 - theta
        stopped = terminal_vector.zip(delta_q).map { |t, q| coefficient * t - q }
        (0..3).each do |nmax|
          work = s_n_bruteforce(stopped, nmax)
          baseline = coefficient * s_n_bruteforce(terminal_vector, nmax)
          error = (work - baseline).abs
          cases += 1
          sharp_cases += 1 if bq.positive? && error == bq
          next if error <= bq

          failures << {
            "T" => terminal_vector.map { |x| rational_string(x) },
            "delta_Q" => delta_q.map { |x| rational_string(x) },
            "theta" => rational_string(theta),
            "N" => nmax,
            "error" => rational_string(error),
            "B_Q" => rational_string(bq)
          }
        end
      end
    end
  end
  finite_group(
    "theta_last_exit_best_N_comparison_with_one_BQ",
    cases,
    failures,
    "sharp_cases" => sharp_cases
  )
end

def check_signed_clock_tail_comparison
  clock_vectors = vectors([0, 1, 2].map { |x| Rational(x) }, 3)
  q_vectors = vectors([-1, 0, 1].map { |x| Rational(x) }, 3)
  failures = []
  cases = 0
  sharp_cases = 0
  clock_vectors.each do |clock|
    q_vectors.each do |q_vector|
      flux = clock.zip(q_vector).map { |k, q| k - q }
      bq = q_vector.sum(Rational(0)) { |value| value.abs }
      (0..3).each do |nmax|
        error = (s_n_bruteforce(flux, nmax) - s_n_bruteforce(clock, nmax)).abs
        cases += 1
        sharp_cases += 1 if bq.positive? && error == bq
        next if error <= bq

        failures << {
          "K" => clock.map { |x| rational_string(x) },
          "Q" => q_vector.map { |x| rational_string(x) },
          "N" => nmax,
          "error" => rational_string(error),
          "B_Q" => rational_string(bq)
        }
      end
    end
  end
  finite_group(
    "signed_F_and_nonnegative_K_tails_differ_by_one_BQ",
    cases,
    failures,
    "sharp_cases" => sharp_cases
  )
end

def check_exception_cauchy
  vectors_nonnegative = vectors([0, 1, 2].map { |x| Rational(x) }, 4)
  failures = []
  cases = 0
  equality_cases = 0
  vectors_nonnegative.each do |vector|
    (0..4).each do |nmax|
      subsets_up_to(4, nmax).each do |indices|
        lhs = indices.sum(Rational(0)) { |index| vector.fetch(index) }
        rhs_squared = Rational(nmax) * vector.sum(Rational(0)) { |value| value**2 }
        cases += 1
        equality_cases += 1 if lhs.positive? && lhs**2 == rhs_squared
        next if lhs**2 <= rhs_squared

        failures << {
          "vector" => vector.map { |x| rational_string(x) },
          "N" => nmax,
          "S" => indices,
          "lhs_squared" => rational_string(lhs**2),
          "rhs_squared" => rational_string(rhs_squared)
        }
      end
    end
  end
  finite_group(
    "exceptional_set_Cauchy_sqrt_N_coefficient",
    cases,
    failures,
    "positive_equality_cases" => equality_cases
  )
end

def check_quantifier_order
  failures = []
  cases = 0
  rows = []
  (1..5).each do |nmax|
    dimension = nmax + 1
    states = (0...dimension).map do |active|
      Array.new(dimension, Rational(0)).tap { |row| row[active] = Rational(1) }
    end
    sup_inf = states.map { |state| s_n_bruteforce(state, nmax) }.max
    inf_sup = subsets_up_to(dimension, nmax).select { |set| set.length == nmax }.map do |removed|
      removed_set = removed.to_set
      states.map do |state|
        state.each_with_index.sum(Rational(0)) do |value, index|
          removed_set.include?(index) ? Rational(0) : value
        end
      end.max
    end.min
    cases += 1
    valid = sup_inf.zero? && inf_sup == 1
    failures << { "N" => nmax, "sup_inf" => rational_string(sup_inf), "inf_sup" => rational_string(inf_sup) } unless valid
    rows << { "N" => nmax, "sup_inf" => rational_string(sup_inf), "inf_sup" => rational_string(inf_sup) }
  end
  finite_group("terminal_dependent_exception_quantifier_order", cases, failures, "rows" => rows)
end

def check_cancellation_and_exhaustion
  failures = []
  cases = 0
  rows = []
  (1..8).each do |pairs|
    vector = Array.new(pairs) { [Rational(1), Rational(-1)] }.flatten
    half = vector.map { |value| value / 2 }
    full = s_n_bruteforce(half, 0)
    finite_subset_sup = subsets_up_to(half.length, half.length).map do |indices|
      positive_part(indices.sum(Rational(0)) { |index| half.fetch(index) })
    end.max
    expected = Rational(pairs, 2)
    cases += 1
    failures << { "pairs" => pairs, "full" => rational_string(full), "subset_sup" => rational_string(finite_subset_sup) } unless full.zero? && finite_subset_sup == expected
    rows << { "pairs" => pairs, "full" => rational_string(full), "subset_sup" => rational_string(finite_subset_sup) }
  end
  signed = [Rational(-1), Rational(1, 2)]
  full = s_n_bruteforce(signed, 0)
  arbitrary_subset_sup = subsets_up_to(2, 2).map do |indices|
    positive_part(indices.sum(Rational(0)) { |index| signed.fetch(index) })
  end.max
  cases += 1
  failures << { "signed_full" => rational_string(full), "arbitrary_subset_sup" => rational_string(arbitrary_subset_sup) } unless full.zero? && arbitrary_subset_sup == Rational(1, 2)
  finite_group(
    "forced_full_signed_tail_versus_arbitrary_subset_supremum",
    cases,
    failures,
    "rows" => rows,
    "negative_half_counterexample" => {
      "full" => rational_string(full),
      "arbitrary_subset_sup" => rational_string(arbitrary_subset_sup)
    }
  )
end

def check_plateau_and_boundary_stresses
  failures = []
  cases = 0
  plateau_rows = 0
  thetas = [Rational(1, 4), Rational(1, 2), Rational(2, 3)]
  (2..10).each do |shells|
    (0...shells).each do |nmax|
      [Rational(1, 2), Rational(1), Rational(3, 2)].each do |height|
        terminal = Array.new(shells, height)
        thetas.each do |theta|
          tail = s_n_bruteforce(terminal, nmax)
          half = s_n_bruteforce(terminal.map { |value| value / 2 }, nmax)
          theta_work = s_n_bruteforce(terminal.map { |value| (1 - theta) * value }, nmax)
          expected = Rational(shells - nmax) * height
          cases += 1
          plateau_rows += 1
          next if tail == expected && half == expected / 2 && theta_work == (1 - theta) * expected

          failures << { "M" => shells, "N" => nmax, "H" => rational_string(height), "theta" => rational_string(theta) }
        end
      end
    end
  end

  # K=0, Q=-F: sharp S_N(F)-S_N(K)=B_Q and no strict upcrossing.
  b = Rational(3, 2)
  k_zero = [Rational(0)]
  f_positive = [b]
  q_negative = [-b]
  k_zero_valid = s_n_bruteforce(k_zero, 0).zero? &&
                 s_n_bruteforce(f_positive, 0) == b &&
                 s_n_bruteforce(f_positive.map { |x| x / 2 }, 0) == b / 2 &&
                 (s_n_bruteforce(f_positive, 0) - s_n_bruteforce(k_zero, 0)).abs == q_negative.sum(Rational(0)) { |value| value.abs } &&
                 !(Rational(0) > Rational(0))
  cases += 1
  failures << { "stress" => "K_zero" } unless k_zero_valid

  # F=0, K=Q: every stopped F increment is zero while the K tail is positive.
  k_path = [Rational(0), Rational(1, 2), Rational(1), Rational(1)]
  f_path = Array.new(k_path.length, Rational(0))
  theta = Rational(1, 2)
  ell = last_leq_exit(k_path, theta * k_path.last)
  f_increment = f_path.last - value_at(f_path, ell)
  f_zero_valid = s_n_bruteforce([k_path.last], 0) == 1 && f_increment.zero?
  cases += 1
  failures << { "stress" => "F_zero" } unless f_zero_valid

  # The half-F stop need not be a K-upcrossing (the scalar model (S.209)).
  f_path = [Rational(0), Rational(1, 2), Rational(1)]
  k_path = [Rational(0), Rational(1), Rational(1)]
  ell_f = last_leq_exit(f_path, Rational(1, 2))
  half_not_upcross = k_path.last - value_at(k_path, ell_f)
  cases += 1
  failures << { "stress" => "half_exit_not_upcross", "delta_K" => rational_string(half_not_upcross) } unless half_not_upcross.zero?

  # Full-history theta exit exists, but a late plateau window contains none.
  plateau_path = [Rational(0), Rational(1), Rational(1), Rational(1)]
  threshold = Rational(2, 3)
  full_ell = last_leq_exit(plateau_path, threshold)
  recent_samples = plateau_path[2..3]
  recent_ell = recent_samples.last <= threshold ? Rational(1) : last_leq_exit(recent_samples, threshold)
  recent_valid = !full_ell.nil? && recent_ell.nil?
  cases += 1
  failures << { "stress" => "recent_window", "full_ell" => full_ell&.then { |x| rational_string(x) }, "recent_ell" => recent_ell } unless recent_valid

  # Early transition bump separates the full terminal domain from I_R.
  full_values = [Rational(0), Rational(1), Rational(0), Rational(0)]
  full_sup = full_values.map { |value| positive_part(value) }.max
  plateau_sup = full_values[2..3].map { |value| positive_part(value) }.max
  cases += 1
  failures << { "stress" => "full_vs_plateau" } unless full_sup == 1 && plateau_sup.zero?

  finite_group(
    "plateau_zero_clock_zero_flux_recent_window_and_domain_stresses",
    cases,
    failures,
    "plateau_rows" => plateau_rows,
    "K_zero_sharp" => k_zero_valid,
    "F_zero_Q_paid" => f_zero_valid,
    "half_exit_not_upcross" => half_not_upcross.zero?,
    "recent_window_has_no_level_exit" => recent_valid,
    "full_domain_exceeds_plateau_domain" => full_sup > plateau_sup
  )
end

def check_theta_two_thirds
  failures = []
  cases = 0
  strict_cases = 0
  values = [0, Rational(1, 12), Rational(1, 7), Rational(1, 6), Rational(1, 3), 1].map { |x| Rational(x) }
  terminals = [Rational(1, 2), 1, Rational(3, 2), 2].map { |x| Rational(x) }
  terminals.each do |terminal|
    values.each do |ratio|
      [-1, 1].each do |sign|
        delta_q = Rational(sign) * ratio * terminal
        delta_f = terminal / 3 - delta_q
        hypothesis = delta_q.abs < terminal / 6
        conclusion = delta_f > terminal / 6
        cases += 1
        strict_cases += 1 if hypothesis
        next unless hypothesis != (ratio < Rational(1, 6)) || (hypothesis && !conclusion)

        failures << {
          "T" => rational_string(terminal),
          "delta_Q" => rational_string(delta_q),
          "delta_F" => rational_string(delta_f),
          "hypothesis" => hypothesis,
          "conclusion" => conclusion
        }
      end
    end
  end
  failures << { "stress" => "no eligible strict case" } if strict_cases.zero?
  finite_group(
    "theta_two_thirds_one_sixth_implication",
    cases,
    failures,
    "eligible_strict_cases" => strict_cases
  )
end

def structural_results(note_body, enforce_hash: true)
  compact = compact_source(note_body)
  tags = note_body.scan(/\\tag\{S\.(\d+)\}/).flatten.map(&:to_i)
  tag_counts = tags.each_with_object(Hash.new(0)) { |tag, counts| counts[tag] += 1 }
  checks = {
    "locked_note_sha256" => !enforce_hash || Digest::SHA256.hexdigest(note_body) == EXPECTED_NOTE_SHA256,
    "title" => note_body.include?("R0.74S Step 9"),
    "tags_consecutive_S200_through_S222" => tags == (200..222).to_a,
    "tags_unique" => tag_counts.values.all? { |count| count == 1 },
    "terminal_domains_are_plateau_and_full" => compact.include?("\\mathcalD\\in\\{I_R,\\mathcalT_R\\}") && compact.include?("\\mathfrakC_R^M(\\mathcalT_R)=\\mathfrakC_{{\\rmfull},R}^M"),
    "only_plateau_below_full" => compact.include?("\\mathfrakC_R^M\\le\\mathfrakC_{{\\rmfull},R}^M") && compact.include?("equalityisneitherusednorasserted"),
    "S_N_definition_sup_inf_order" => compact.include?("\\mathcalS_N(x):=\\inf_{S\\subset\\mathbbN,") && compact.include?("\\sum_{k\\notinS}x_k\\right]_+") && note_body.include?("\\sup_{\\tau}\\inf_{S_\\tau}") && note_body.include?("not\n\\(\\inf_S\\sup_\\tau\\)"),
    "signed_rearrangement_formula" => compact.include?("\\mathcalS_N(x)=\\left[\\sum_kx_k-\\sum_{m=1}^{N}x_m^{+*}\\right]_+=\\left[\\sum_{m>N}x_m^{+*}-\\|x_-\\|_{\\ell^1}\\right]_+"),
    "S_N_l1_Lipschitz" => compact.include?("|\\mathcalS_N(x)-\\mathcalS_N(y)|\\le\\|x-y\\|_{\\ell^1}"),
    "signed_finite_subset_warning" => note_body.include?("an arbitrary finite-subset supremum cannot reconstruct the signed tail"),
    "l1_good_time_closure" => note_body.include?("continuous\ninto \\(\\ell^1\\)") && note_body.include?("common dense good-time set"),
    "half_exit_uses_terminal_sign" => compact.include?("\\operatorname{sgn}(f_k)F_{k,R}(t)\\le{|f_k|\\over2}"),
    "half_exit_zero_terminal_convention" => compact.include?("\\ell_k^F(\\tau):=\\tau\\quad\\hbox{if}f_k=0"),
    "half_exit_exact_one_half" => compact.include?("F_{k,R}(\\tau)-F_{k,R}(\\ell_k^F(\\tau))={1\\over2}F_{k,R}(\\tau)"),
    "half_exit_best_N_identity" => compact.include?("\\mathfrakW_{1/2,N,R}^{F}(\\mathcalD)={1\\over2}\\mathcalS_{N,R}^{F}(\\mathcalD)"),
    "half_exit_plateau_reduction" => compact.include?("\\mathfrakC_R^M\\leB_{Q,R}^M+\\sqrtNZ_R+2\\mathfrakW_{1/2,N,R}^{F}(I_R)"),
    "half_exit_not_upcrossing" => compact.include?("K(1)-K(1/2)=0") && note_body.include?("strict upcrossing condition (S.25) fails") && note_body.include?("need\nnot be admissible"),
    "K_zero_terminal_convention" => compact.include?("\\ell_{k,\\theta}^{K}(\\tau):=\\tau\\quad\\hbox{if}T_k=0"),
    "K_last_exit_identity" => compact.include?("L_{k,\\theta}(\\tau):=F_{k,R}(\\tau)-F_{k,R}(\\ell_{k,\\theta}^{K}(\\tau))=(1-\\theta)T_k-\\DeltaQ_{k,\\theta}(\\tau)"),
    "K_last_exit_absolute_tail" => compact.include?("\\sum_k|L_{k,\\theta}(\\tau)|\\le(1-\\theta)\\sum_kT_k+B_{Q,R}^M<\\infty"),
    "sharp_one_BQ_comparison" => compact.include?("(1-\\theta)\\mathcalS_{N,R}^{K}(\\mathcalD)-B_{Q,R}^M\\le\\mathfrakW_{\\theta,N,R}^{K}(\\mathcalD)\\le(1-\\theta)\\mathcalS_{N,R}^{K}(\\mathcalD)+B_{Q,R}^M"),
    "strict_theta_and_positive_terminal" => compact.include?("0<\\theta<{3\\over4}:\\qquadT_k>0") && compact.include?("(1-\\theta)T_k>{1\\over4}T_k"),
    "zero_clock_omitted" => note_body.include?("Shells with \\(T_k=0\\) have") && note_body.include?("and are omitted"),
    "good_terminal_only_closure" => note_body.include?("Fix a good terminal") && note_body.include?("good-stop closure statement only at good\nterminals"),
    "last_exit_selector_not_continuous" => note_body.include?("not continuity of the last-exit map") && note_body.include?("canonical last-exit selector is continuous") && note_body.include?("NOT CLAIMED"),
    "no_infinite_local_energy_test" => note_body.include?("or the right to insert one\ninfinite") && note_body.include?("one infinite stopped cutoff is an admissible local-energy test") && note_body.include?("NOT CLAIMED"),
    "K_plateau_reduction_constant" => compact.include?("{\\mathfrakW_{\\theta,N,R}^{K}(I_R)\\over1-\\theta}+\\left(1+{1\\over1-\\theta}\\right)B_{Q,R}^M"),
    "F_K_tail_one_BQ" => compact.include?("\\left|\\mathcalS_{N,R}^{F}(\\mathcalD)-\\mathcalS_{N,R}^{K}(\\mathcalD)\\right|\\leB_{Q,R}^M"),
    "full_domain_is_Q12" => note_body.include?("Taking \\(\\mathcal D=\\mathcal T_R\\) recovers exactly the full-terminal\nR0.74Q gate (Q.12)"),
    "plateau_domain_is_weaker" => note_body.include?("Taking \\(\\mathcal D=I_R\\) gives its weaker plateau"),
    "terminal_exception_counterexample" => compact.include?("x(\\tau_1)=(1,0)") && note_body.include?("fixed\nexceptional set is strictly stronger"),
    "cancellation_counterexample" => compact.include?("F(\\tau)=(1,-1)") && note_body.include?("not asserted to be an (S.25)-admissible Step 2 family"),
    "plateau_zero_start" => compact.include?("h(s_R)=0") && compact.include?("K_k(t)=F_k(t)=h(t)") && compact.include?("(M-N)H"),
    "K_zero_stress" => compact.include?("K\\equiv0") && compact.include?("\\mathcalS_0^K=0") && compact.include?("\\mathcalS_0^F=B") && note_body.include?("no strict (S.25) stop exists"),
    "F_zero_stress" => compact.include?("K=Q=h") && compact.include?("F=0") && note_body.include?("every last-exit flux increment vanishes"),
    "recent_window_stress" => note_body.include?("recent window contains\nno \\(\\theta\\)-level exit at all") && note_body.include?("must retain the full history") && compact.include?("[s_R,\\tau]"),
    "theta_two_thirds_one_sixth" => compact.include?("\\DeltaK_{k,2/3}={1\\over3}T_k") && compact.include?("|\\DeltaQ_{k,2/3}|<{1\\over6}T_k") && compact.include?("\\DeltaF_{k,2/3}>{1\\over6}T_k"),
    "residual_not_yet_defined" => note_body.include?("will be\ndefined and audited in the next step"),
    "paid_branches_exact" => note_body.include?("Step 7 low-Rayleigh branch") && note_body.include?("\\(Q\\)-visible \\(\\mathcal I_\\beta\\)") && note_body.include?("kinetic-mass\n\\(\\mathcal I_\\sigma\\)"),
    "residual_may_contain_defect_or_high_Rayleigh" => note_body.include?("still contain anomalous-defect or high-Rayleigh dissipation"),
    "universal_no_exception_gate_refuted" => note_body.include?("The following are **REFUTED**") && note_body.include?("universal no-exception antecedent"),
    "conditional_S38_preserved" => note_body.include?("The conditional implication (S.38) remains valid"),
    "best_N_PDE_bound_open" => note_body.include?("fixed \\(N_0\\), solution- and scale-independent PDE estimate") && note_body.include?("remain **OPEN**"),
    "single_packet_not_N1" => note_body.include?("single dominant packet proves \\(N_0=1\\) is sufficient") && note_body.include?("NOT CLAIMED"),
    "stress_tests_not_PDE" => note_body.include?("scalar stress tests are PDE solutions") && note_body.include?("NOT CLAIMED"),
    "not_clay" => note_body.scan("NOT CLAY").length >= 2,
    "no_tabs" => !note_body.include?("\t"),
    "no_control_characters" => !note_body.match?(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/),
    "no_trailing_whitespace" => note_body.lines.none? { |line| line.match?(/[ \t]+$/) }
  }
  checks.map { |identifier, passed| { "id" => identifier, "pass" => !!passed } }
end

def note_valid?(note_body)
  structural_results(note_body, enforce_hash: false).all? { |row| row.fetch("pass") }
end

def source_mutation_results(note_body)
  mutations = {
    "swap_sup_inf_order" => note_body.sub("\\sup_{\\tau}\\inf_{S_\\tau}", "\\inf_{S}\\sup_{\\tau}"),
    "delete_terminal_sign_from_half_exit" => note_body.sub("\\operatorname {sgn}(f_k)F_{k,R}(t)", "F_{k,R}(t)"),
    "change_half_to_third" => note_body.gsub("{1\\over2}F_{k,R}(\\tau)", "{1\\over3}F_{k,R}(\\tau)"),
    "delete_half_zero_terminal_convention" => note_body.sub("\\ell_k^F(\\tau):=\\tau\\quad\\hbox{if }f_k=0", "\\ell_k^F(\\tau):=s_R\\quad\\hbox{if }f_k=0"),
    "change_sharp_one_BQ_to_two" => note_body.sub("+B_{Q,R}^M.}\n\\tag{S.214}", "+2B_{Q,R}^M.}\n\\tag{S.214}"),
    "delete_lower_BQ_error" => note_body.sub("-B_{Q,R}^M\n \\le\\mathfrak W_{\\theta,N,R}^{K}", "\n \\le\\mathfrak W_{\\theta,N,R}^{K}"),
    "allow_theta_three_quarters" => note_body.sub("0<\\theta<{3\\over4}:", "0<\\theta\\le{3\\over4}:") ,
    "delete_positive_terminal_condition" => note_body.sub(" \\qquad\n T_k>0,", ""),
    "promote_half_exit_to_upcrossing" => note_body.sub("need\nnot be admissible", "are always admissible"),
    "conflate_plateau_and_full" => note_body.sub("Only the inequality\n\\(\\mathfrak C_R^M\\le\\mathfrak C_{{\\rm full},R}^M\\) is inherited", "The equality\n\\(\\mathfrak C_R^M=\\mathfrak C_{{\\rm full},R}^M\\) is inherited"),
    "bind_Q12_to_plateau" => note_body.sub("\\mathcal D=\\mathcal T_R", "\\mathcal D=I_R"),
    "erase_cancellation_disclaimer" => note_body.sub("not asserted to be an (S.25)-admissible Step 2 family", "asserted to be an (S.25)-admissible Step 2 family"),
    "erase_K_zero_no_upcrossing" => note_body.sub("no strict (S.25) stop exists", "a strict (S.25) stop exists"),
    "truncate_last_exit_to_recent_window" => note_body.sub("must retain the full history", "may be truncated to the recent window"),
    "promote_infinite_cutoff" => note_body.sub("or the right to insert one\ninfinite", "and the right to insert one\ninfinite"),
    "promote_last_exit_continuity" => note_body.sub("not continuity of the last-exit map", "continuity of the last-exit map"),
    "promote_universal_gate" => note_body.sub("The following are **REFUTED**:", "The following are **PROVED**:"),
    "refute_conditional_S38" => note_body.sub("The conditional implication (S.38) remains valid", "The conditional implication (S.38) is refuted"),
    "promote_N1_sufficiency" => note_body.sub("single dominant packet proves \\(N_0=1\\) is sufficient", "single dominant packet does not prove \\(N_0=1\\) is sufficient"),
    "promote_scalar_stress_to_PDE" => note_body.sub("scalar stress tests are PDE solutions", "scalar stress tests are not PDE solutions"),
    "remove_not_clay" => note_body.gsub("NOT CLAY", "CLAY")
  }
  rows = mutations.map do |identifier, mutated|
    changed = mutated != note_body
    rejected = changed && !note_valid?(mutated)
    { "id" => identifier, "changed" => changed, "rejected" => rejected, "pass" => changed && rejected }
  end
  { "id" => "source_claim_mutations", "rows" => rows, "pass" => rows.all? { |row| row.fetch("pass") } }
end

def primary_validation(payload, note_hash, generator_hash)
  errors = []
  unless payload.is_a?(Hash)
    return ["root is not an object"]
  end

  errors << "schema mismatch" unless payload["schema"] == EXPECTED_PRIMARY_SCHEMA
  errors << "producer pass is not true" unless payload["pass"] == true
  source = payload["source"]
  unless source.is_a?(Hash)
    errors << "source is not an object"
  else
    errors << "note path mismatch" unless source["note"] == EXPECTED_NOTE_FIELD
    errors << "generator path mismatch" unless source["generator"] == EXPECTED_GENERATOR_FIELD
    errors << "note hash mismatch" unless source["note_sha256"] == note_hash
    errors << "locked note hash mismatch" unless source["locked_note_sha256"] == EXPECTED_NOTE_SHA256
    errors << "generator hash mismatch" unless source["generator_sha256"] == generator_hash
  end

  if EXPECTED_PRIMARY_SCOPE
    errors << "scope mismatch" unless payload["scope"] == EXPECTED_PRIMARY_SCOPE
  elsif !payload["scope"].is_a?(Hash)
    errors << "scope is not an object"
  end

  summary = payload["summary"]
  errors << "summary is not an object" unless summary.is_a?(Hash)
  group_to_stem = {
    "exact_checks" => "exact",
    "finite_checks" => "finite",
    "structural_checks" => "structural",
    "negative_mutations" => "negative_mutations"
  }
  group_to_stem.each do |group, stem|
    rows = payload[group]
    unless rows.is_a?(Array) && !rows.empty?
      errors << "#{group} missing or empty"
      next
    end
    errors << "#{group} has failed row" unless rows.all? { |row| row.is_a?(Hash) && row["pass"] == true }
    ids = rows.each_with_object([]) do |row, values|
      values << row["id"] if row.is_a?(Hash) && row.key?("id")
    end
    errors << "#{group} has missing or duplicate ids" unless ids.length == rows.length && ids.uniq.length == ids.length

    expected_ids = EXPECTED_PRIMARY_IDS[group]
    errors << "#{group} id set mismatch" if expected_ids && !expected_ids.empty? && ids.to_set != expected_ids.to_set
    if group == "exact_checks"
      EXPECTED_PRIMARY_EXACT_VALUES.each do |identifier, expected|
        row = rows.find { |candidate| candidate["id"] == identifier }
        actual = row && [row["left"], row["right"], row["margin"]]
        errors << "#{identifier} exact payload mismatch" unless actual == expected
      end
    elsif group == "finite_checks"
      EXPECTED_PRIMARY_FINITE_COUNTS.each do |identifier, (field, expected)|
        row = rows.find { |candidate| candidate["id"] == identifier }
        errors << "#{identifier} finite count mismatch" unless row && row[field] == expected
      end
    end
    if group == "structural_checks"
      errors << "structural count mismatch" if EXPECTED_PRIMARY_STRUCTURAL_COUNT && rows.length != EXPECTED_PRIMARY_STRUCTURAL_COUNT
      errors << "required structural ids missing" unless REQUIRED_PRIMARY_STRUCTURAL_IDS.to_set.subset?(ids.to_set)
    end

    next unless summary.is_a?(Hash)

    total_keys = ["#{stem}_total", "#{group}_total"]
    passed_keys = ["#{stem}_passed", "#{group}_passed", "#{stem}_rejected", "#{group}_rejected"]
    total_key = total_keys.find { |key| summary.key?(key) }
    passed_key = passed_keys.find { |key| summary.key?(key) }
    errors << "#{group} summary total absent" if total_key.nil?
    errors << "#{group} summary passed absent" if passed_key.nil?
    errors << "#{group} summary total mismatch" if total_key && summary[total_key] != rows.length
    errors << "#{group} summary passed mismatch" if passed_key && summary[passed_key] != rows.count { |row| row["pass"] == true }
  end
  errors
end

def primary_artifact_mutations(payload, note_hash, generator_hash)
  mutations = {
    "stale_note_hash" => ->(copy) { copy.fetch("source")["note_sha256"] = "0" * 64 },
    "stale_locked_note_hash" => ->(copy) { copy.fetch("source")["locked_note_sha256"] = "1" * 64 },
    "stale_generator_hash" => ->(copy) { copy.fetch("source")["generator_sha256"] = "f" * 64 },
    "wrong_schema" => ->(copy) { copy["schema"] = "r074s-best-n-last-exit-certificate-v0" },
    "producer_pass_false" => ->(copy) { copy["pass"] = false },
    "drop_exact_row_and_adjust_summary" => lambda do |copy|
      copy.fetch("exact_checks").pop
      summary = copy.fetch("summary")
      key = %w[exact_total exact_checks_total].find { |candidate| summary.key?(candidate) }
      summary[key] -= 1 if key
      key = %w[exact_passed exact_checks_passed].find { |candidate| summary.key?(candidate) }
      summary[key] -= 1 if key
    end,
    "duplicate_finite_id" => lambda do |copy|
      rows = copy.fetch("finite_checks")
      rows[1]["id"] = rows[0]["id"]
    end,
    "flip_structural_pass" => ->(copy) { copy.fetch("structural_checks")[0]["pass"] = false },
    "flip_negative_mutation_pass" => ->(copy) { copy.fetch("negative_mutations")[0]["pass"] = false },
    "stale_summary_count" => lambda do |copy|
      key = copy.fetch("summary").keys.find { |candidate| candidate.end_with?("_total") }
      copy.fetch("summary")[key] += 1
    end,
    "drop_required_structural_row" => lambda do |copy|
      required = REQUIRED_PRIMARY_STRUCTURAL_IDS.first
      rows = copy.fetch("structural_checks")
      index = required ? rows.index { |row| row["id"] == required } : 0
      rows.delete_at(index || 0)
    end,
    "mutate_refuted_claim_row" => lambda do |copy|
      row = copy.fetch("structural_checks").find do |candidate|
        candidate["id"] == "refuted_contains_no_exception_but_preserves_S38"
      end
      row["id"] = "proved_universal_no_exception_gate"
    end,
    "mutate_open_claim_row" => lambda do |copy|
      row = copy.fetch("structural_checks").find do |candidate|
        candidate["id"] == "open_contains_best_N_PDE_and_Q1"
      end
      row["id"] = "proved_best_N_PDE_and_Q1"
    end,
    "tamper_half_exit_exact_payload" => lambda do |copy|
      row = copy.fetch("exact_checks").find do |candidate|
        candidate["id"] == "half_exit_two_halves_recover_terminal_flux"
      end
      row["left"] = "2/1"
      row["right"] = "2/1"
    end,
    "promote_machine_scope" => lambda do |copy|
      scope = copy.fetch("scope")
      key = scope.keys.find { |candidate| candidate.match?(/PDE|Navier|regularity|Clay|infinite|good/i) && scope[candidate] == false }
      scope[key] = true
    end
  }
  rows = mutations.map do |identifier, mutate|
    copy = deep_copy(payload)
    begin
      mutate.call(copy)
      errors = primary_validation(copy, note_hash, generator_hash)
      { "id" => identifier, "errors" => errors, "pass" => !errors.empty? }
    rescue KeyError, NoMethodError, TypeError => error
      { "id" => identifier, "errors" => ["mutation setup failed: #{error.class}: #{error.message}"], "pass" => false }
    end
  end
  { "id" => "primary_artifact_mutations", "rows" => rows, "pass" => rows.all? { |row| row.fetch("pass") } }
end

def report_results(body, json_hash, note_hash, generator_hash)
  checks = {
    "reports_PASS" => body.include?("**PASS**"),
    "binds_primary_json_hash" => body.include?(json_hash),
    "binds_note_hash" => body.include?(note_hash),
    "binds_generator_hash" => body.include?(generator_hash),
    "finite_algebraic_scope" => body.match?(/finite|algebraic/i),
    "denies_Clay" => body.include?("NOT CLAY")
  }
  checks.map { |identifier, passed| { "id" => identifier, "pass" => !!passed } }
end

required_paths = [NOTE_PATH, PRIMARY_JSON_PATH, PRIMARY_GENERATOR_PATH, PRIMARY_REPORT_PATH]
missing = required_paths.reject { |path| File.file?(path) }
unless missing.empty?
  warn "missing required input(s): #{missing.join(', ')}"
  exit 2
end

note_body = File.binread(NOTE_PATH).force_encoding(Encoding::UTF_8)
note_hash = sha256(NOTE_PATH)
independent_checks = [
  check_s_n_reconstruction,
  check_s_n_lipschitz,
  check_half_exit_paths,
  check_half_exit_best_n_identity,
  check_k_last_exit_paths,
  check_one_bq_perturbation,
  check_signed_clock_tail_comparison,
  check_exception_cauchy,
  check_quantifier_order,
  check_cancellation_and_exhaustion,
  check_plateau_and_boundary_stresses,
  check_theta_two_thirds
]
structure = structural_results(note_body)
source_mutations = source_mutation_results(note_body)

# The producer artifact is inspected only after all independent mathematics,
# source structure, and source mutation checks have been evaluated.
generator_hash = sha256(PRIMARY_GENERATOR_PATH)
json_hash = sha256(PRIMARY_JSON_PATH)
report_hash = sha256(PRIMARY_REPORT_PATH)
payload = JSON.parse(File.binread(PRIMARY_JSON_PATH))
primary_errors = primary_validation(payload, note_hash, generator_hash)
primary_errors << "generator artifact hash mismatch" unless generator_hash == EXPECTED_PRIMARY_GENERATOR_SHA256
primary_errors << "primary JSON artifact hash mismatch" unless json_hash == EXPECTED_PRIMARY_JSON_SHA256
primary_errors << "primary report artifact hash mismatch" unless report_hash == EXPECTED_PRIMARY_REPORT_SHA256
artifact_mutations = primary_artifact_mutations(payload, note_hash, generator_hash)
report_checks = report_results(
  File.binread(PRIMARY_REPORT_PATH).force_encoding(Encoding::UTF_8),
  json_hash,
  note_hash,
  generator_hash
)

pass = note_hash == EXPECTED_NOTE_SHA256 &&
       independent_checks.all? { |row| row.fetch("pass") } &&
       structure.all? { |row| row.fetch("pass") } &&
       source_mutations.fetch("pass") &&
       primary_errors.empty? &&
       artifact_mutations.fetch("pass") &&
       report_checks.all? { |row| row.fetch("pass") }

output = {
  "schema" => "r074s-best-n-last-exit-independent-audit-v1",
  "source" => {
    "note" => EXPECTED_NOTE_FIELD,
    "note_sha256" => note_hash,
    "primary_generator" => EXPECTED_GENERATOR_FIELD,
    "primary_generator_sha256" => generator_hash,
    "primary_certificate" => EXPECTED_JSON_FIELD,
    "primary_certificate_sha256" => json_hash,
    "primary_report" => EXPECTED_REPORT_FIELD,
    "primary_report_sha256" => report_hash
  },
  "independent_checks" => independent_checks,
  "structural_checks" => structure,
  "source_mutations" => source_mutations,
  "primary_producer_errors" => primary_errors,
  "artifact_mutations" => artifact_mutations,
  "report_checks" => report_checks,
  "scope" => {
    "finite_and_algebraic_only" => true,
    "machine_proves_inherited_Navier_Stokes_PDE" => false,
    "machine_proves_good_time_density_or_l1_topology" => false,
    "machine_proves_infinite_local_energy_test_admissibility" => false,
    "machine_proves_best_N_PDE_packing" => false,
    "machine_proves_regularity_or_Clay" => false
  },
  "summary" => {
    "independent_groups_passed" => independent_checks.count { |row| row.fetch("pass") },
    "independent_groups_total" => independent_checks.length,
    "independent_finite_cases" => independent_checks.sum { |row| row.fetch("cases", 0) },
    "structural_passed" => structure.count { |row| row.fetch("pass") },
    "structural_total" => structure.length,
    "source_mutations_rejected" => source_mutations.fetch("rows").count { |row| row.fetch("pass") },
    "source_mutations_total" => source_mutations.fetch("rows").length,
    "artifact_mutations_rejected" => artifact_mutations.fetch("rows").count { |row| row.fetch("pass") },
    "artifact_mutations_total" => artifact_mutations.fetch("rows").length,
    "report_checks_passed" => report_checks.count { |row| row.fetch("pass") },
    "report_checks_total" => report_checks.length
  },
  "pass" => pass
}

puts JSON.pretty_generate(output)
exit(pass ? 0 : 1)
