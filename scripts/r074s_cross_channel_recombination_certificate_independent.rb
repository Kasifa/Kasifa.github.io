#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent Ruby Rational audit of R0.74S Step 6.
#
# All stopped-row, event, D_post, Abel, genealogy, witness, and mutation
# arithmetic is reconstructed below before the Python-produced JSON certificate
# is opened.  The JSON cross-check validates its schema, note hash, required
# identifiers, row-level outcomes, failure arrays, and summary consistency.  No
# value read from that JSON is an arithmetic input to the reconstruction.

require "digest"
require "json"
require "set"

REPO = File.expand_path("..", __dir__)
NOTE_PATH = File.join(
  REPO,
  "research",
  "r074s_cross_channel_recombination_no_gain.md"
)
DEFAULT_CERTIFICATE_PATH = File.join(
  REPO,
  "research",
  "r074s_cross_channel_recombination_certificate.json"
)
EXPECTED_NOTE_FIELD = "research/r074s_cross_channel_recombination_no_gain.md"
EXPECTED_CATEGORY_IDS = {
  "exact" => %w[
    weight_drop_coefficient_recombination
    singleton_genealogy_row_count
    one_block_internal_edge_count
    witness_matched_square_scaling
  ],
  "finite" => %w[
    exact_rational_stopped_row_recombination_with_ties
    exact_rational_omega_pair_and_insertion_monotonicity_grid
    exact_rational_three_channel_event_jump_identity_with_ties
    exact_rational_dissipation_corrected_S137_with_ties
    exact_rational_blockwise_residual_abel_all_blocks_through_12
    exhaustive_eight_shell_genealogy_count_with_ties
    exact_one_block_scalar_witness_N_1_through_64
    exact_epsilon_N_super_gaussian_exponent_gap_N_2_through_64
  ],
  "structural" => %w[
    tags_consecutive
    tags_unique
    required_text_7e95a02a89ca
    required_text_a3a080fe53f2
    required_text_016e0bfabac3
    required_text_83d09a767ccd
    required_text_986f8acee87c
    required_text_b3bdf558d29c
    required_text_62e326eb23e2
    required_text_f0280c796fec
    required_text_e4d4b6d29a47
    required_text_8fc334b38a53
    required_text_ede4d28b10e0
    required_text_30a7bc62866a
    required_text_1516be8976b6
    required_text_f03c10a60963
    required_text_3f21a114cd43
    required_text_bc661ee11412
    required_text_614e69480092
    required_text_14066eb6fd90
    required_text_23ffb81f6184
    required_text_875b58a94275
    required_text_80f5371794fc
    required_formula_f89cd322383e
    required_formula_a7575a43d5c7
    required_formula_1fd9302e5770
    required_formula_5c885cff81b6
    required_formula_a8bbecceff61
    required_formula_838834cf127d
    required_formula_c7a198893183
    required_formula_4289dfc0bef7
    required_formula_5a514d6c32a6
    required_formula_e886f000f3a9
    required_formula_d40da7e6d1ba
    required_formula_b45d5901f8b0
    required_formula_003cc75c79a3
    required_formula_b2ad59f86bf9
    required_formula_53376a859143
    required_formula_92b450499f74
    required_formula_37b7d6e92926
    required_formula_8f77d640a27a
    required_formula_481dfd19339d
    required_formula_54744c93df33
    required_formula_7cc14ff6a528
    required_formula_a5cb4d17fb20
    required_formula_54c6c850061d
    required_formula_81a891526791
    required_formula_a3862c34ea5b
    forbidden_b004710258d9
    forbidden_6d9bfc2401b3
    forbidden_0265ef52ab2f
    forbidden_1fcb3fdff421
    forbidden_cf3a13bfbafb
    forbidden_e8afa30adf8a
    display_math_balanced
    inline_math_balanced
    no_disallowed_control_characters
    no_malformed_mathscr_command
  ],
  "negative" => %w[
    outer_k_plus_one_shift_removed
    weight_drop_coefficient_sign_reversed
    root_completed_clock_sign_reversed
    internal_overlap_max_replaced_by_min
    d_post_post_increment_sign_reversed_exact_fixture
    event_jump_terminal_minus_sign_mutation_rejected
    residual_sign_mutation_rejected
    d_post_upper_bound_reversal_rejected
    scalar_work_pde_boundary_mutation_rejected
    epsilon_exponent_gap_mutation_rejected
  ]
}.freeze
EXPECTED_CLAIM_BOUNDARY = {
  "four_channel_recombination" => "PROVED_FINITE_ALGEBRA",
  "three_channel_genealogy_identity" => "PROVED_FINITE_ALGEBRA",
  "d_post_one_sided_decomposition" => "PROVED_ANALYTICALLY_AND_CHECKED_ON_FINITE_RATIONAL_DENSITIES",
  "omega_cutoff_nonnegativity" => "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
  "quadratic_Q_ledger" => "INHERITED_AND_PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
  "blockwise_residual_abel" => "PROVED_FINITE_ALGEBRA",
  "scalar_one_block_no_go" => "PROVED_ABSTRACT_NOT_PDE",
  "W_N_sc_is_pde_work" => false,
  "epsilon_N_exponent_gap" => "PROVED_EXACT_FINITE_EXPONENT_ALGEBRA",
  "pde_weighted_genealogy_theorem" => "OPEN",
  "cross_channel_dynamical_sign_theorem" => "OPEN",
  "dissipation_dominated_branch" => "OPEN",
  "r074r_persistence_hypotheses" => "OPEN",
  "fixed_scale_Q1_unconditional" => "OPEN",
  "scale_contraction" => "OPEN",
  "regularity" => "OPEN",
  "singularity_formation" => "OPEN",
  "clay_millennium_problem_solved" => false
}.freeze

def q(value)
  "#{value.numerator}/#{value.denominator}"
end

def gamma_family(shell_max)
  (1..(shell_max + 2)).to_h do |shell|
    [shell, Rational(1, shell * shell + 3 * shell + 7)]
  end
end

def ball_plus(seed, shell, time)
  numerator =
    (seed + 2) * shell * shell +
    (3 * seed + 5) * shell * time +
    7 * time * time + 11 * shell - 3 * time + seed + 1
  Rational(numerator, 17 + seed)
end

def ball_minus(seed, shell, time)
  numerator =
    (seed + 5) * shell * shell -
    (seed + 2) * shell * time +
    5 * time * time - 7 * shell + 13 * time - seed + 3
  Rational(numerator, 23 + 2 * seed)
end

def shell_row(seed, gamma, shell, time)
  gamma.fetch(shell) * (
    ball_plus(seed, shell + 1, time) - ball_minus(seed, shell, time)
  )
end

def boundary_row(seed, gamma, boundary, time)
  gamma.fetch(boundary) * (
    ball_plus(seed, boundary, time) - ball_minus(seed, boundary, time)
  )
end

def internal_edges(shell_set, shell_max)
  (2..shell_max).select do |boundary|
    shell_set.include?(boundary - 1) && shell_set.include?(boundary)
  end
end

def components(shell_set)
  ordered = shell_set.to_a.sort
  return [] if ordered.empty?

  result = []
  first = ordered.first
  last = ordered.first
  ordered.drop(1).each do |shell|
    if shell == last + 1
      last = shell
    else
      result << [first, last]
      first = shell
      last = shell
    end
  end
  result << [first, last]
  result
end

def stopped_channel(
  seed,
  shell_set,
  stops,
  shell_max,
  tau,
  include_mismatch:,
  outer_shift: 1,
  root_coefficient: -1,
  gap_coefficient: 1,
  overlap_rule: :max
)
  gamma = gamma_family(shell_max)
  value = Rational(0)

  shell_set.to_a.sort.each do |shell|
    rho = if shell == 1 || !shell_set.include?(shell - 1)
            tau
          else
            stops.fetch(shell - 1)
          end
    lambda_time = if !shell_set.include?(shell + 1)
                    tau
                  else
                    stops.fetch(shell + 1)
                  end

    if stops.fetch(shell) < rho
      value += root_coefficient * gamma.fetch(shell) * (
        ball_minus(seed, shell, rho) -
        ball_minus(seed, shell, stops.fetch(shell))
      )
    end

    if stops.fetch(shell) < lambda_time
      ball_index = shell + outer_shift
      value += gamma.fetch(shell) * (
        ball_plus(seed, ball_index, lambda_time) -
        ball_plus(seed, ball_index, stops.fetch(shell))
      )
    end
  end

  internal_edges(shell_set, shell_max).each do |boundary|
    left_stop = stops.fetch(boundary - 1)
    right_stop = stops.fetch(boundary)
    start_time = overlap_rule == :max ? [left_stop, right_stop].max : [left_stop, right_stop].min
    d_m = gamma.fetch(boundary - 1) - gamma.fetch(boundary)
    value += gap_coefficient * d_m * (
      ball_plus(seed, boundary, tau) -
      ball_plus(seed, boundary, start_time)
    )
    next unless include_mismatch

    value += boundary_row(seed, gamma, boundary, tau) -
             boundary_row(seed, gamma, boundary, start_time)
  end

  value
end

def stopped_shell_sum(seed, shell_set, stops, shell_max, tau)
  gamma = gamma_family(shell_max)
  shell_set.sum(Rational(0)) do |shell|
    shell_row(seed, gamma, shell, tau) -
      shell_row(seed, gamma, shell, stops.fetch(shell))
  end
end

def phi_value(seed, shell_set, time, shell_max)
  gamma = gamma_family(shell_max)
  shell_part = shell_set.sum(Rational(0)) do |shell|
    shell_row(seed, gamma, shell, time)
  end
  boundary_part = internal_edges(shell_set, shell_max).sum(Rational(0)) do |boundary|
    boundary_row(seed, gamma, boundary, time)
  end
  shell_part - boundary_part
end

def each_stopped_family(shell_max, stop_levels)
  (0...(1 << shell_max)).each do |mask|
    shell_set = (1..shell_max).select { |shell| (mask & (1 << (shell - 1))).positive? }.to_set
    ordered = shell_set.to_a.sort
    stop_levels.repeated_permutation(ordered.length) do |assignment|
      yield shell_set, ordered.zip(assignment).to_h
    end
  end
end

def reconstruct_stopped_rows
  shell_max = 6
  stop_levels = [1, 2, 3]
  tau = 4
  row_seeds = [0, 1, 2, 3, 4]
  failures = []
  configurations = 0

  row_seeds.each do |seed|
    each_stopped_family(shell_max, stop_levels) do |shell_set, stops|
      configurations += 1
      left = stopped_channel(
        seed,
        shell_set,
        stops,
        shell_max,
        tau,
        include_mismatch: true
      )
      right = stopped_shell_sum(seed, shell_set, stops, shell_max, tau)
      next if left == right

      failures << {
        "seed" => seed,
        "shells" => shell_set.to_a.sort,
        "stops" => stops,
        "channels" => q(left),
        "stopped_shells" => q(right)
      } if failures.length < 12
    end
  end

  {
    "id" => "independent_S115_five_rows_with_ties",
    "row_fixtures" => row_seeds.length,
    "configurations_checked" => configurations,
    "failures" => failures,
    "pass" => failures.empty?
  }
end

def reconstruct_event_identity
  shell_max = 6
  stop_levels = [1, 2, 3]
  tau = 4
  row_seeds = [5, 6]
  failures = []
  configurations = 0
  epochs = 0

  row_seeds.each do |seed|
    each_stopped_family(shell_max, stop_levels) do |shell_set, stops|
      configurations += 1
      direct = stopped_channel(
        seed,
        shell_set,
        stops,
        shell_max,
        tau,
        include_mismatch: false
      )
      event_value = phi_value(seed, shell_set, tau, shell_max)
      stops.values.uniq.sort.each do |event_time|
        before = shell_set.select { |shell| stops.fetch(shell) < event_time }.to_set
        after = shell_set.select { |shell| stops.fetch(shell) <= event_time }.to_set
        event_value -= phi_value(seed, after, event_time, shell_max) -
                       phi_value(seed, before, event_time, shell_max)
        epochs += 1
      end

      expanded = stopped_shell_sum(seed, shell_set, stops, shell_max, tau)
      gamma = gamma_family(shell_max)
      expanded -= internal_edges(shell_set, shell_max).sum(Rational(0)) do |boundary|
        start_time = [stops.fetch(boundary - 1), stops.fetch(boundary)].max
        boundary_row(seed, gamma, boundary, tau) -
          boundary_row(seed, gamma, boundary, start_time)
      end

      next if direct == event_value && direct == expanded

      failures << {
        "seed" => seed,
        "shells" => shell_set.to_a.sort,
        "stops" => stops,
        "three_channel" => q(direct),
        "event_value" => q(event_value),
        "shell_minus_boundary" => q(expanded)
      } if failures.length < 12
    end
  end

  {
    "id" => "independent_S136_grouped_event_identity_with_ties",
    "row_fixtures" => row_seeds.length,
    "configurations_checked" => configurations,
    "activation_epochs_checked" => epochs,
    "failures" => failures,
    "pass" => failures.empty?
  }
end

def reconstruct_block_abel
  shell_max = 16
  failures = []
  blocks_checked = 0

  [0, 2, 5].each do |seed|
    gamma = gamma_family(shell_max)
    plus = (1..(shell_max + 1)).to_h do |shell|
      [shell, Rational(shell * shell + (seed + 3) * shell + 5, 11 + seed)]
    end
    minus = (1..(shell_max + 1)).to_h do |shell|
      [shell, plus.fetch(shell) - Rational(shell + seed + 1, 29 + seed)]
    end
    boundary = (1..shell_max).to_h do |shell|
      [shell, gamma.fetch(shell) * (plus.fetch(shell) - minus.fetch(shell))]
    end
    residual = (1..shell_max).to_h do |shell|
      [shell, gamma.fetch(shell) * (plus.fetch(shell + 1) - plus.fetch(shell))]
    end
    shell_row_values = (1..shell_max).to_h do |shell|
      [shell, gamma.fetch(shell) * (plus.fetch(shell + 1) - minus.fetch(shell))]
    end

    (1..shell_max).each do |first|
      (first..shell_max).each do |last|
        blocks_checked += 1
        terminal_outer_and_gap = gamma.fetch(last) * plus.fetch(last + 1)
        terminal_outer_and_gap += ((first + 1)..last).sum(Rational(0)) do |boundary_index|
          (gamma.fetch(boundary_index - 1) - gamma.fetch(boundary_index)) *
            plus.fetch(boundary_index)
        end
        s138_right = gamma.fetch(first) * plus.fetch(first)
        s138_right += (first..last).sum(Rational(0)) { |shell| residual.fetch(shell) }

        signed_ball_form = terminal_outer_and_gap - gamma.fetch(first) * minus.fetch(first)
        s139_first = boundary.fetch(first) +
                     (first..last).sum(Rational(0)) { |shell| residual.fetch(shell) }
        s139_second = shell_row_values.fetch(first) +
                      ((first + 1)..last).sum(Rational(0)) { |shell| residual.fetch(shell) }
        direct_phi = (first..last).sum(Rational(0)) { |shell| shell_row_values.fetch(shell) }
        direct_phi -= ((first + 1)..last).sum(Rational(0)) { |shell| boundary.fetch(shell) }

        next if terminal_outer_and_gap == s138_right &&
                signed_ball_form == s139_first &&
                signed_ball_form == s139_second &&
                signed_ball_form == direct_phi

        failures << {
          "seed" => seed,
          "block" => [first, last],
          "S138_left" => q(terminal_outer_and_gap),
          "S138_right" => q(s138_right),
          "signed_ball" => q(signed_ball_form),
          "S139_first" => q(s139_first),
          "S139_second" => q(s139_second),
          "direct_phi" => q(direct_phi)
        } if failures.length < 12
      end
    end
  end

  {
    "id" => "independent_S138_S139_all_blocks_through_16",
    "block_fixtures_checked" => blocks_checked,
    "failures" => failures,
    "pass" => failures.empty?
  }
end

def reconstruct_genealogy_counts
  shell_max = 8
  stop_levels = [1, 2, 3]
  tau = 4
  failures = []
  configurations = 0

  each_stopped_family(shell_max, stop_levels) do |shell_set, stops|
    configurations += 1
    edges = internal_edges(shell_set, shell_max)
    component_count = components(shell_set).length
    tie_count = edges.count { |boundary| stops.fetch(boundary - 1) == stops.fetch(boundary) }
    root_count = 0
    outer_count = 0

    shell_set.each do |shell|
      rho = if shell == 1 || !shell_set.include?(shell - 1)
              tau
            else
              stops.fetch(shell - 1)
            end
      lambda_time = if !shell_set.include?(shell + 1)
                      tau
                    else
                      stops.fetch(shell + 1)
                    end
      root_count += 1 if stops.fetch(shell) < rho
      outer_count += 1 if stops.fetch(shell) < lambda_time
    end

    n_value = shell_set.length
    passed =
      edges.length == n_value - component_count &&
      root_count + outer_count == n_value + component_count - tie_count &&
      root_count + outer_count + edges.length == 2 * n_value - tie_count
    next if passed

    failures << {
      "shells" => shell_set.to_a.sort,
      "stops" => stops,
      "n" => n_value,
      "components" => component_count,
      "ties" => tie_count,
      "roots" => root_count,
      "outers" => outer_count,
      "internal" => edges.length
    } if failures.length < 12
  end

  {
    "id" => "independent_S140_S141_counts_with_ties",
    "configurations_checked" => configurations,
    "failures" => failures,
    "pass" => failures.empty?
  }
end

def dpost_beta(shell, point)
  Rational(((5 * shell + 7 * point + shell * point) % 13) + 1, 41)
end

def dpost_psi(shell, point)
  dpost_beta(shell, point) +
    dpost_beta(shell + 1, point) +
    Rational(((3 * shell + 2 * point) % 11) + 1, 31)
end

def dpost_omega(shell_set, gamma, shell_max, point_count)
  (0...point_count).map do |point|
    shell_part = shell_set.sum(Rational(0)) do |shell|
      gamma.fetch(shell) * dpost_psi(shell, point)
    end
    boundary_part = internal_edges(shell_set, shell_max).sum(Rational(0)) do |boundary|
      gamma.fetch(boundary) * dpost_beta(boundary, point)
    end
    shell_part - boundary_part
  end
end

def dpost_pair(cutoff, density)
  cutoff.zip(density).sum(Rational(0)) { |left, right| left * right }
end

def reconstruct_omega_monotonicity
  shell_max = 7
  point_count = 17
  gamma = gamma_family(shell_max)
  failures = []
  pair_comparisons = 0
  insertion_configurations = 0
  insertion_comparisons = 0

  (1..shell_max).each do |shell|
    (0...point_count).each do |point|
      weighted_boundary =
        gamma.fetch(shell) * dpost_beta(shell, point) +
        gamma.fetch(shell + 1) * dpost_beta(shell + 1, point)
      weighted_shell = gamma.fetch(shell) * dpost_psi(shell, point)
      pair_comparisons += 1
      next if weighted_boundary >= 0 && weighted_boundary <= weighted_shell

      failures << {
        "kind" => "weighted_pair",
        "shell" => shell,
        "point" => point,
        "boundary" => q(weighted_boundary),
        "shell_cutoff" => q(weighted_shell)
      } if failures.length < 12
    end
  end

  (0...(1 << shell_max)).each do |mask|
    shell_set = (1..shell_max).select do |shell|
      (mask & (1 << (shell - 1))).positive?
    end.to_set
    (1..shell_max).each do |inserted_shell|
      next if shell_set.include?(inserted_shell)

      insertion_configurations += 1
      enlarged = shell_set | [inserted_shell].to_set
      before = dpost_omega(shell_set, gamma, shell_max, point_count)
      after = dpost_omega(enlarged, gamma, shell_max, point_count)
      before.zip(after).each_with_index do |(left, right), point|
        insertion_comparisons += 1
        next if left >= 0 && right >= left

        failures << {
          "kind" => "insertion",
          "shells" => shell_set.to_a.sort,
          "inserted_shell" => inserted_shell,
          "point" => point,
          "before" => q(left),
          "after" => q(right)
        } if failures.length < 12
      end
    end
  end

  {
    "id" => "independent_Omega_insertion_monotonicity",
    "shell_max" => shell_max,
    "point_count" => point_count,
    "weighted_pair_comparisons" => pair_comparisons,
    "insertion_configurations_checked" => insertion_configurations,
    "insertion_point_comparisons" => insertion_comparisons,
    "failures" => failures,
    "pass" => failures.empty?
  }
end

def reconstruct_dpost_fixture_and_mutation
  shell_max = 5
  stop_levels = [0, 1, 2]
  tau = 3
  point_count = 9
  gamma = gamma_family(shell_max)

  energy = (0..tau).to_h do |time|
    values = (0...point_count).map do |point|
      Rational(((11 * time + 7 * point * point + 3 * point) % 23) + 1, 19)
    end
    [time, values]
  end
  dissipation = (0..tau).to_h do |time|
    values = (0...point_count).map do |point|
      value = Rational(((5 * point + 2) % 11) + 1, 23)
      (0...time).each do |step|
        value += Rational(((7 * step + 3 * point * point + point) % 13) + 1, 29)
      end
      value
    end
    [time, values]
  end

  failures = []
  stopped_configurations = 0
  density_configurations = 0
  tied_configurations = 0
  empty_configurations = 0
  positive_dpost_configurations = 0
  event_insertions = 0
  sign_reversal_counterexamples = 0
  first_sign_reversal = nil

  each_stopped_family(shell_max, stop_levels) do |shell_set, stops|
    stopped_configurations += 1
    ordered = shell_set.to_a.sort
    events = stops.values.uniq.sort
    has_tie = events.length < ordered.length
    omega_terminal = dpost_omega(shell_set, gamma, shell_max, point_count)
    delta_rows = []
    delta_sum = Array.new(point_count, Rational(0))
    delta_nonnegative = true

    events.each do |event_time|
      before = shell_set.select { |shell| stops.fetch(shell) < event_time }.to_set
      after = shell_set.select { |shell| stops.fetch(shell) <= event_time }.to_set
      before_omega = dpost_omega(before, gamma, shell_max, point_count)
      after_omega = dpost_omega(after, gamma, shell_max, point_count)
      delta = after_omega.zip(before_omega).map { |right, left| right - left }
      delta_nonnegative &&= delta.all? { |value| value >= 0 }
      delta.each_with_index { |value, index| delta_sum[index] += value }
      delta_rows << [event_time, delta]
      event_insertions += 1
    end

    partition = delta_sum == omega_terminal
    (0...3).each do |variant|
      density_configurations += 1
      tied_configurations += 1 if has_tie
      empty_configurations += 1 if shell_set.empty?
      quadratic = (0..tau).to_h do |time|
        values = (0...point_count).map do |point|
          Rational(
            ((13 * time + 5 * point * point + 7 * point + 11 * variant) % 31) - 15,
            17 + 2 * variant
          )
        end
        [time, values]
      end
      flux = (0..tau).to_h do |time|
        values = (0...point_count).map do |point|
          energy.fetch(time).fetch(point) +
            dissipation.fetch(time).fetch(point) -
            quadratic.fetch(time).fetch(point)
        end
        [time, values]
      end

      event_value = lambda do |density|
        terminal = dpost_pair(omega_terminal, density.fetch(tau))
        insertions = delta_rows.sum(Rational(0)) do |event_time, delta|
          dpost_pair(delta, density.fetch(event_time))
        end
        terminal - insertions
      end
      insertion_energy = delta_rows.sum(Rational(0)) do |event_time, delta|
        dpost_pair(delta, energy.fetch(event_time))
      end
      d_post = delta_rows.sum(Rational(0)) do |event_time, delta|
        dpost_pair(delta, dissipation.fetch(tau)) -
          dpost_pair(delta, dissipation.fetch(event_time))
      end
      reversed_d_post = -d_post
      event_e = event_value.call(energy)
      event_d = event_value.call(dissipation)
      event_q = event_value.call(quadratic)
      event_f = event_value.call(flux)
      phi_e = dpost_pair(omega_terminal, energy.fetch(tau))
      phi_d = dpost_pair(omega_terminal, dissipation.fetch(tau))
      identity_rhs = phi_e - insertion_energy + d_post - event_q
      first_bound = phi_e + d_post + event_q.abs
      terminal_bound = phi_e + phi_d + event_q.abs
      positive_dpost_configurations += 1 if d_post > 0

      if reversed_d_post != event_d
        sign_reversal_counterexamples += 1
        first_sign_reversal ||= {
          "shells" => ordered,
          "stops" => stops,
          "mutated" => q(reversed_d_post),
          "target" => q(event_d)
        }
      end

      conditions = {
        "delta_partition" => partition,
        "delta_nonnegative" => delta_nonnegative,
        "insertion_energy_nonnegative" => insertion_energy >= 0,
        "D_post_exact_event_decomposition" => d_post == event_d,
        "D_post_nonnegative" => d_post >= 0,
        "D_post_nonvacuous_off_empty_set" => shell_set.empty? || d_post > 0,
        "D_post_bounded_by_terminal_D" => d_post <= phi_d,
        "E_plus_D_minus_Q_event_identity" => event_f == event_e + event_d - event_q,
        "D_post_expansion_identity" => event_f == identity_rhs,
        "strengthened_one_sided_bound" => [event_f, Rational(0)].max <= first_bound,
        "terminal_clock_corollary" => first_bound <= terminal_bound
      }
      next if conditions.values.all?

      failures << {
        "shells" => ordered,
        "stops" => stops,
        "Q_variant" => variant,
        "W_three" => q(event_f),
        "D_post" => q(d_post),
        "Phi_D" => q(phi_d),
        "conditions" => conditions
      } if failures.length < 12
    end
  end

  check = {
    "id" => "independent_S137_D_post_exact_fixture_with_ties",
    "shell_max" => shell_max,
    "point_count" => point_count,
    "stopped_configurations_checked" => stopped_configurations,
    "density_configurations_checked" => density_configurations,
    "tied_configurations_checked" => tied_configurations,
    "empty_configurations_checked" => empty_configurations,
    "positive_D_post_configurations" => positive_dpost_configurations,
    "event_insertions_checked" => event_insertions,
    "failures" => failures,
    "pass" => failures.empty?
  }
  mutation = {
    "id" => "D_post_time_increment_sign_reversed",
    "counterexamples_found" => sign_reversal_counterexamples,
    "first_example" => first_sign_reversal,
    "pass" => sign_reversal_counterexamples.positive?
  }
  [check, mutation]
end

def reconstruct_witness
  failures = []
  rows = []

  (1..64).each do |n_value|
    gamma = (1..n_value).to_h do |shell|
      [shell, Rational(1, (shell + 1) * (shell + 1))]
    end
    balls = { 1 => Rational(0) }
    (1..n_value).each do |shell|
      balls[shell + 1] = balls.fetch(shell) + 1 / gamma.fetch(shell)
    end

    outer = gamma.fetch(n_value) * balls.fetch(n_value + 1)
    gap = (2..n_value).sum(Rational(0)) do |boundary|
      (gamma.fetch(boundary - 1) - gamma.fetch(boundary)) * balls.fetch(boundary)
    end
    epsilon = (1...n_value).sum(Rational(0)) do |shell|
      gamma.fetch(n_value) / gamma.fetch(shell)
    end
    total = outer + gap
    unit_variations = Array.new(n_value, Rational(1))
    y2_squared = unit_variations.sum(Rational(0)) { |variation| variation * variation }

    shell_set = (1..n_value).to_set
    stops = shell_set.to_h { |shell| [shell, 1] }
    tau = 2
    edges = internal_edges(shell_set, n_value)
    component_count = components(shell_set).length
    tie_count = edges.count { |boundary| stops.fetch(boundary - 1) == stops.fetch(boundary) }
    root_count = 0
    outer_count = 0
    shell_set.each do |shell|
      rho = shell == 1 ? tau : stops.fetch(shell - 1)
      lambda_time = shell == n_value ? tau : stops.fetch(shell + 1)
      root_count += 1 if stops.fetch(shell) < rho
      outer_count += 1 if stops.fetch(shell) < lambda_time
    end
    internal_count = edges.length
    events = stops.values.uniq.sort
    merger_count = events.sum do |event_time|
      before = shell_set.select { |shell| stops.fetch(shell) < event_time }.to_set
      after = shell_set.select { |shell| stops.fetch(shell) <= event_time }.to_set
      before_blocks = components(before)
      components(after).sum do |first, last|
        inherited = before_blocks.count do |old_first, old_last|
          old_first <= last && first <= old_last
        end
        [inherited - 1, 0].max
      end
    end
    passed =
      outer >= 0 && gap >= 0 &&
      outer == 1 + epsilon &&
      gap == n_value - 1 - epsilon &&
      total == n_value &&
      y2_squared == n_value &&
      component_count == 1 &&
      events.length == 1 &&
      merger_count.zero? &&
      internal_count == n_value - component_count &&
      root_count + outer_count == n_value + component_count - tie_count &&
      root_count + outer_count + internal_count == n_value + 1

    row = {
      "N" => n_value,
      "outer" => q(outer),
      "gap" => q(gap),
      "epsilon" => q(epsilon),
      "total" => q(total),
      "Y2_squared" => q(y2_squared),
      "terminal_components" => component_count,
      "activation_epochs" => events.length,
      "mergers" => merger_count,
      "roots" => root_count,
      "outers" => outer_count,
      "internal" => internal_count,
      "ties" => tie_count,
      "three_family_rows" => root_count + outer_count + internal_count,
      "pass" => passed
    }
    rows << row if [1, 2, 8, 16, 32, 64].include?(n_value)
    failures << row unless passed
  end

  {
    "id" => "independent_one_epoch_one_block_witness_N_1_through_64",
    "weight_proxy" => "gamma_m=1/(m+1)^2",
    "sample_rows" => rows,
    "failures" => failures,
    "pass" => failures.empty?
  }
end

def reconstruct_epsilon_exponent_gap
  failures = []
  rows = []
  comparisons = 0
  (2..64).each do |n_value|
    gaps = (1...n_value).map do |shell|
      comparisons += 1
      Rational(4**(n_value - 1) - 4**(shell - 1), 32)
    end
    expected = Rational(3 * 4**(n_value - 2), 32)
    conditions = {
      "minimum_at_adjacent_shell" => gaps.min == gaps.last,
      "adjacent_gap_exact" => gaps.last == expected,
      "all_ratios_have_claimed_exponent_gap" => gaps.all? { |gap| gap >= expected },
      "epsilon_has_N_minus_one_terms" => gaps.length == n_value - 1
    }
    row = {
      "N" => n_value,
      "terms_in_epsilon" => gaps.length,
      "minimum_exponent_gap" => q(gaps.min),
      "claimed_exponent_gap" => q(expected),
      "conditions" => conditions,
      "pass" => conditions.values.all?
    }
    rows << row if [2, 3, 8, 16, 32, 64].include?(n_value)
    failures << row unless row.fetch("pass")
  end
  {
    "id" => "independent_epsilon_N_super_gaussian_exponent_gap",
    "N_min" => 2,
    "N_max" => 64,
    "comparisons_checked" => comparisons,
    "sample_rows" => rows,
    "failures" => failures,
    "pass" => failures.empty?
  }
end

def mutation_audit(dpost_mutation)
  shell_max = 6
  stop_levels = [1, 2, 3]
  tau = 4
  seed = 7
  mutation_counts = {
    "outer_ball_index_k_instead_of_k_plus_1" => 0,
    "root_sign_reversed" => 0,
    "gap_sign_reversed" => 0,
    "overlap_min_instead_of_max" => 0,
    "event_jump_subtraction_replaced_by_addition" => 0
  }
  first_examples = {}

  each_stopped_family(shell_max, stop_levels) do |shell_set, stops|
    target = stopped_shell_sum(seed, shell_set, stops, shell_max, tau)
    variants = {
      "outer_ball_index_k_instead_of_k_plus_1" => stopped_channel(
        seed, shell_set, stops, shell_max, tau,
        include_mismatch: true, outer_shift: 0
      ),
      "root_sign_reversed" => stopped_channel(
        seed, shell_set, stops, shell_max, tau,
        include_mismatch: true, root_coefficient: 1
      ),
      "gap_sign_reversed" => stopped_channel(
        seed, shell_set, stops, shell_max, tau,
        include_mismatch: true, gap_coefficient: -1
      ),
      "overlap_min_instead_of_max" => stopped_channel(
        seed, shell_set, stops, shell_max, tau,
        include_mismatch: true, overlap_rule: :min
      )
    }

    event_mutation = phi_value(seed, shell_set, tau, shell_max)
    stops.values.uniq.sort.each do |event_time|
      before = shell_set.select { |shell| stops.fetch(shell) < event_time }.to_set
      after = shell_set.select { |shell| stops.fetch(shell) <= event_time }.to_set
      event_mutation += phi_value(seed, after, event_time, shell_max) -
                        phi_value(seed, before, event_time, shell_max)
    end
    three_channel_target = stopped_channel(
      seed, shell_set, stops, shell_max, tau, include_mismatch: false
    )
    variants["event_jump_subtraction_replaced_by_addition"] = event_mutation

    variants.each do |identifier, mutated_value|
      comparison_target = if identifier == "event_jump_subtraction_replaced_by_addition"
                            three_channel_target
                          else
                            target
                          end
      next if mutated_value == comparison_target

      mutation_counts[identifier] += 1
      first_examples[identifier] ||= {
        "shells" => shell_set.to_a.sort,
        "stops" => stops,
        "mutated" => q(mutated_value),
        "target" => q(comparison_target)
      }
    end
  end

  # Two further independent mutations of the block/witness arithmetic.
  gamma = gamma_family(8)
  plus = (1..9).to_h { |shell| [shell, Rational(shell * shell + 2 * shell + 3, 13)] }
  block_mutation_failures = 0
  omitted_outer_failures = 0
  (1..8).each do |first|
    (first..8).each do |last|
      right = gamma.fetch(first) * plus.fetch(first)
      right += (first..last).sum(Rational(0)) do |shell|
        gamma.fetch(shell) * (plus.fetch(shell + 1) - plus.fetch(shell))
      end
      wrong_gap_sign = gamma.fetch(last) * plus.fetch(last + 1)
      wrong_gap_sign -= ((first + 1)..last).sum(Rational(0)) do |boundary|
        (gamma.fetch(boundary - 1) - gamma.fetch(boundary)) * plus.fetch(boundary)
      end
      block_mutation_failures += 1 unless wrong_gap_sign == right
    end
  end

  (1..64).each do |n_value|
    witness_gamma = (1..n_value).to_h do |shell|
      [shell, Rational(1, (shell + 1) * (shell + 1))]
    end
    balls = { 1 => Rational(0) }
    (1..n_value).each do |shell|
      balls[shell + 1] = balls.fetch(shell) + 1 / witness_gamma.fetch(shell)
    end
    gap_only = (2..n_value).sum(Rational(0)) do |boundary|
      (witness_gamma.fetch(boundary - 1) - witness_gamma.fetch(boundary)) *
        balls.fetch(boundary)
    end
    omitted_outer_failures += 1 unless gap_only == n_value
  end

  mutation_counts["S138_gap_sign_reversed"] = block_mutation_failures
  mutation_counts["witness_terminal_outer_omitted"] = omitted_outer_failures
  rows = mutation_counts.map do |identifier, count|
    {
      "id" => identifier,
      "counterexamples_found" => count,
      "first_example" => first_examples[identifier],
      "pass" => count.positive?
    }
  end
  rows << dpost_mutation
  {
    "id" => "independent_numerical_mutation_rejection",
    "mutations" => rows,
    "passed" => rows.count { |row| row.fetch("pass") },
    "total" => rows.length,
    "pass" => rows.all? { |row| row.fetch("pass") }
  }
end

def rational_text(value)
  return nil unless value.is_a?(String)

  Rational(value)
rescue ArgumentError, ZeroDivisionError
  nil
end

def require_fields(row, fields, issues)
  missing = fields.reject { |field| row.key?(field) }
  issues << "missing fields: #{missing.join(',')}" unless missing.empty?
end

def require_empty_array(row, field, issues)
  value = row[field]
  issues << "#{field} must be a present empty array" unless value.is_a?(Array) && value.empty?
end

def finite_row_integrity(row)
  issues = []
  identifier = row["id"]
  case identifier
  when "exact_rational_stopped_row_recombination_with_ties"
    require_fields(row, %w[shell_max configurations_checked failures], issues)
    issues << "shell_max must equal 5" unless row["shell_max"] == 5
    issues << "configurations_checked must equal 1024" unless row["configurations_checked"] == 4**5
    require_empty_array(row, "failures", issues)
  when "exact_rational_omega_pair_and_insertion_monotonicity_grid"
    require_fields(
      row,
      %w[shell_max radii_checked pair_comparisons insertion_comparisons pair_failures insertion_failures],
      issues
    )
    shell_max = row["shell_max"]
    radii = row["radii_checked"]
    issues << "shell_max must equal 6" unless shell_max == 6
    issues << "radii_checked must equal 182" unless radii == 182
    issues << "pair_comparisons relation failed" unless
      row["pair_comparisons"] == 3 * 6 * 182
    issues << "insertion_comparisons relation failed" unless
      row["insertion_comparisons"] == 6 * 2**5 * 182
    require_empty_array(row, "pair_failures", issues)
    require_empty_array(row, "insertion_failures", issues)
  when "exact_rational_three_channel_event_jump_identity_with_ties"
    require_fields(row, %w[shell_max configurations_checked events_checked failures], issues)
    issues << "shell_max must equal 5" unless row["shell_max"] == 5
    issues << "configurations_checked must equal 1024" unless row["configurations_checked"] == 4**5
    issues << "events_checked must equal 2343" unless row["events_checked"] == 2343
    require_empty_array(row, "failures", issues)
  when "exact_rational_dissipation_corrected_S137_with_ties"
    require_fields(
      row,
      %w[shell_max radii_checked stopped_configurations_checked Q_density_variants configurations_checked tied_configurations_checked event_insertions_checked density_pairings_checked failures],
      issues
    )
    expected = {
      "shell_max" => 4,
      "radii_checked" => 30,
      "stopped_configurations_checked" => 256,
      "Q_density_variants" => 3,
      "configurations_checked" => 768,
      "tied_configurations_checked" => 549,
      "event_insertions_checked" => 525,
      "density_pairings_checked" => 45_930
    }
    expected.each do |field, value|
      issues << "#{field} must equal #{value}" unless row[field] == value
    end
    require_empty_array(row, "failures", issues)
  when "exact_rational_blockwise_residual_abel_all_blocks_through_12"
    require_fields(row, %w[blocks_checked rows failures], issues)
    rows = row["rows"]
    expected_blocks = (1..12).flat_map { |first| (first..12).map { |last| [first, last] } }
    issues << "blocks_checked must equal 78" unless row["blocks_checked"] == expected_blocks.length
    unless rows.is_a?(Array) && rows.length == expected_blocks.length
      issues << "rows must contain all 78 blocks"
    else
      actual_blocks = rows.map { |entry| entry.is_a?(Hash) ? entry["block"] : nil }
      issues << "block list mismatch" unless actual_blocks == expected_blocks
      rows.each do |entry|
        ball_form = entry.is_a?(Hash) ? rational_text(entry["ball_form"]) : nil
        boundary_form = entry.is_a?(Hash) ? rational_text(entry["boundary_plus_residual"]) : nil
        root_form = entry.is_a?(Hash) ? rational_text(entry["root_shell_plus_residual"]) : nil
        valid = entry.is_a?(Hash) && entry["pass"] == true &&
          !ball_form.nil? && !boundary_form.nil? && !root_form.nil? &&
          ball_form == boundary_form && ball_form == root_form
        issues << "invalid Abel row" unless valid
      end
    end
    require_empty_array(row, "failures", issues)
  when "exhaustive_eight_shell_genealogy_count_with_ties"
    require_fields(row, %w[configurations_checked failures], issues)
    issues << "configurations_checked must equal 65536" unless row["configurations_checked"] == 4**8
    require_empty_array(row, "failures", issues)
  when "exact_one_block_scalar_witness_N_1_through_64"
    require_fields(
      row,
      %w[rows failures pde_realization_asserted stopped_work_symbol weight_ratio_proxy],
      issues
    )
    rows = row["rows"]
    issues << "pde_realization_asserted must be false" unless row["pde_realization_asserted"] == false
    issues << "stopped_work_symbol mismatch" unless row["stopped_work_symbol"] == "W_N^sc"
    issues << "weight_ratio_proxy mismatch" unless row["weight_ratio_proxy"] == "1/2"
    unless rows.is_a?(Array) && rows.all? { |entry| entry.is_a?(Hash) } &&
           rows.length == 64 && rows.map { |entry| entry["N"] } == (1..64).to_a
      issues << "witness rows must cover N=1..64"
    else
      rows.each do |entry|
        n_value = entry["N"]
        conditions = entry["conditions"]
        expected_condition_keys = %w[
          finite_telescoping
          gap_split
          matched_square_for_unit_positive_variations
          one_block
          one_epoch
          outer_split
          same_nonnegative_sign
          strict_upcrossing
          unit_positive_variations
          zero_mergers
        ]
        conditions_valid = conditions.is_a?(Hash) &&
          conditions.keys.sort == expected_condition_keys.sort &&
          expected_condition_keys.all? { |key| conditions[key] == true }
        expected_outer = Rational(2**n_value - 1, 2**(n_value - 1))
        expected_gap = n_value - expected_outer
        valid = entry["pass"] == true && conditions_valid &&
          rational_text(entry["Y2_squared"]) == n_value &&
          rational_text(entry["total_stopped_work"]) == n_value &&
          rational_text(entry["root"]) == 0 && rational_text(entry["mismatch"]) == 0 &&
          rational_text(entry["outer"]) == expected_outer &&
          rational_text(entry["weight_drop"]) == expected_gap &&
          entry["positive_variations_checked"] == n_value &&
          entry["active_time_cells_checked"] == 3 &&
          entry["activation_epochs"] == 1 && entry["block_mergers"] == 0 &&
          entry["maximum_active_components"] == 1
        issues << "invalid witness row N=#{n_value}" unless valid
      end
    end
    require_empty_array(row, "failures", issues)
  when "exact_epsilon_N_super_gaussian_exponent_gap_N_2_through_64"
    require_fields(row, %w[comparisons_checked rows failures], issues)
    rows = row["rows"]
    issues << "comparisons_checked must equal 2016" unless row["comparisons_checked"] == 2016
    unless rows.is_a?(Array) && rows.all? { |entry| entry.is_a?(Hash) } &&
           rows.length == 63 && rows.map { |entry| entry["N"] } == (2..64).to_a
      issues << "epsilon rows must cover N=2..64"
    else
      rows.each do |entry|
        n_value = entry["N"]
        expected = Rational(3 * 4**(n_value - 2), 32)
        conditions = entry["conditions"]
        expected_condition_keys = %w[
          adjacent_gap_exact
          all_ratios_have_claimed_exponent_gap
          epsilon_has_N_minus_one_terms
          minimum_at_adjacent_shell
        ]
        conditions_valid = conditions.is_a?(Hash) &&
          conditions.keys.sort == expected_condition_keys.sort &&
          expected_condition_keys.all? { |key| conditions[key] == true }
        valid = entry["pass"] == true && conditions_valid &&
          entry["terms_in_epsilon"] == n_value - 1 &&
          rational_text(entry["minimum_exponent_gap"]) == expected &&
          rational_text(entry["claimed_exponent_gap"]) == expected
        issues << "invalid epsilon row N=#{n_value}" unless valid
      end
    end
    require_empty_array(row, "failures", issues)
  else
    issues << "unexpected finite identifier"
  end
  {
    "id" => identifier,
    "issues" => issues,
    "pass" => issues.empty?
  }
end

def category_content_issues(category, rows)
  issues = []
  if category == "exact"
    rows.each do |row|
      left = row.is_a?(Hash) ? rational_text(row["left"]) : nil
      right = row.is_a?(Hash) ? rational_text(row["right"]) : nil
      margin = row.is_a?(Hash) ? rational_text(row["margin"]) : nil
      valid = row.is_a?(Hash) && !left.nil? && !right.nil? && !margin.nil? &&
        left == right && margin == 0
      label = row.is_a?(Hash) ? row["id"] : "non-object"
      issues << "invalid exact row #{label}" unless valid
    end
  elsif category == "negative"
    numerical_ids = EXPECTED_CATEGORY_IDS.fetch("negative").first(5)
    rows.each do |row|
      next unless row.is_a?(Hash)

      if numerical_ids.include?(row["id"])
        valid = row["counterexamples_found"].is_a?(Integer) && row["counterexamples_found"].positive?
        if row["id"] == "d_post_post_increment_sign_reversed_exact_fixture"
          valid &&= row["target_inequality_used_as_input"] == false
          valid &&= row["correct_reconstruction"] == row["W_three_from_channels"]
          valid &&= row["mutated_reconstruction"] != row["W_three_from_channels"]
        end
        issues << "invalid numerical mutation #{row['id']}" unless valid
      else
        valid = row["correct_sentinel_present"] == true &&
          row["wrong_sentinel_inserted"] == true && row["mutated_structural_result"] == "FAIL"
        issues << "invalid structural mutation #{row['id']}" unless valid
      end
    end
  end
  issues
end

def python_certificate_cross_check(certificate_path)
  raw = File.binread(certificate_path)
  payload = JSON.parse(raw)
  note_sha = Digest::SHA256.file(NOTE_PATH).hexdigest
  summary = payload["summary"].is_a?(Hash) ? payload.fetch("summary") : {}
  category_keys = {
    "exact" => "exact_checks",
    "finite" => "finite_checks",
    "structural" => "structural_checks",
    "negative" => "negative_mutation_checks"
  }
  category_rows = {}
  category_audits = category_keys.map do |category, key|
    raw_rows = payload[key]
    rows = raw_rows.is_a?(Array) ? raw_rows : []
    category_rows[category] = rows
    rows_are_objects = rows.all? { |row| row.is_a?(Hash) }
    ids = rows.map { |row| row["id"] if row.is_a?(Hash) }.compact
    ids_valid = ids.length == rows.length && ids.all? do |identifier|
      identifier.is_a?(String) && !identifier.empty?
    end
    unique_ids = ids.uniq.length == ids.length
    failed_ids = rows.map do |row|
      next if row.is_a?(Hash) && row["pass"] == true

      row.is_a?(Hash) ? row["id"] : "non-object row"
    end.compact
    failure_field_issues = rows.flat_map do |row|
      next ["non-object row"] unless row.is_a?(Hash)

      row.map do |field, value|
        next unless field == "failures" || field.end_with?("_failures")
        next if value.is_a?(Array) && value.empty?

        "#{row['id']}:#{field}"
      end.compact
    end
    actual_passed = rows.count { |row| row.is_a?(Hash) && row["pass"] == true }
    actual_total = rows.length
    summary_passed = summary["#{category}_passed"]
    summary_total = summary["#{category}_total"]
    summary_matches = summary_passed == actual_passed && summary_total == actual_total
    expected_ids = EXPECTED_CATEGORY_IDS.fetch(category)
    missing_ids = expected_ids - ids
    unexpected_ids = ids - expected_ids
    expected_ids_match =
      actual_total == expected_ids.length && missing_ids.empty? && unexpected_ids.empty?
    content_issues = category_content_issues(category, rows)
    okay =
      raw_rows.is_a?(Array) && rows_are_objects && expected_ids_match &&
      ids_valid && unique_ids && failed_ids.empty? && failure_field_issues.empty? &&
      content_issues.empty? && actual_passed == actual_total && summary_matches
    {
      "category" => category,
      "array_present" => raw_rows.is_a?(Array),
      "expected_total" => expected_ids.length,
      "actual_passed" => actual_passed,
      "actual_total" => actual_total,
      "summary_passed" => summary_passed,
      "summary_total" => summary_total,
      "summary_matches_actual" => summary_matches,
      "unique_ids" => unique_ids,
      "missing_ids" => missing_ids,
      "unexpected_ids" => unexpected_ids,
      "failed_ids" => failed_ids,
      "failure_field_issues" => failure_field_issues,
      "content_issues" => content_issues,
      "pass" => okay
    }
  end
  finite_checks = category_rows.fetch("finite")
  finite_ids = finite_checks.map { |row| row["id"] if row.is_a?(Hash) }.compact
  required_ids = EXPECTED_CATEGORY_IDS.fetch("finite")
  finite_id_counts = finite_ids.each_with_object(Hash.new(0)) do |identifier, counts|
    counts[identifier] += 1
  end
  missing_required_ids = required_ids.reject { |identifier| finite_id_counts.fetch(identifier, 0) == 1 }
  unexpected_finite_ids = finite_ids - required_ids
  duplicate_finite_ids = finite_id_counts.select { |_identifier, count| count > 1 }.keys
  finite_failed_ids = finite_checks.map do |row|
    next if row.is_a?(Hash) && row["pass"] == true

    row.is_a?(Hash) ? row["id"] : "non-object row"
  end.compact
  finite_failure_field_issues = finite_checks.flat_map do |row|
    next ["non-object row"] unless row.is_a?(Hash)

    row.map do |field, value|
      next unless field == "failures" || field.end_with?("_failures")
      next if value.is_a?(Array) && value.empty?

      "#{row['id']}:#{field}"
    end.compact
  end
  finite_row_audits = finite_checks.map do |row|
    if row.is_a?(Hash)
      finite_row_integrity(row)
    else
      { "id" => "non-object row", "issues" => ["finite row is not an object"], "pass" => false }
    end
  end
  dpost_audit = finite_row_audits.find do |row|
    row["id"] == "exact_rational_dissipation_corrected_S137_with_ties"
  end
  claim_boundary = payload["claim_boundary"]
  claim_mismatches = EXPECTED_CLAIM_BOUNDARY.map do |field, expected|
    next if claim_boundary.is_a?(Hash) && claim_boundary[field] == expected

    {
      "field" => field,
      "expected" => expected,
      "actual" => claim_boundary.is_a?(Hash) ? claim_boundary[field] : nil
    }
  end.compact
  checks = [
    {
      "id" => "schema",
      "actual" => payload["schema"],
      "pass" => payload["schema"] == "r074s-cross-channel-recombination-certificate-v2"
    },
    {
      "id" => "note_path",
      "actual" => payload["note"],
      "expected" => EXPECTED_NOTE_FIELD,
      "pass" => payload["note"] == EXPECTED_NOTE_FIELD
    },
    {
      "id" => "note_sha256",
      "json" => payload["note_sha256"],
      "actual" => note_sha,
      "pass" => payload["note_sha256"] == note_sha
    },
    {
      "id" => "producer_summary_result",
      "actual" => summary["result"],
      "pass" => summary["result"] == "PASS" && category_audits.all? { |row| row.fetch("pass") }
    },
    {
      "id" => "producer_categories_all_pass",
      "categories" => category_audits,
      "pass" => category_audits.all? { |row| row.fetch("pass") }
    },
    {
      "id" => "producer_required_finite_ids",
      "missing_or_nonunique" => missing_required_ids,
      "unexpected" => unexpected_finite_ids,
      "duplicate_finite_ids" => duplicate_finite_ids,
      "pass" => missing_required_ids.empty? && unexpected_finite_ids.empty? && duplicate_finite_ids.empty?
    },
    {
      "id" => "producer_finite_rows_pass",
      "failed_ids" => finite_failed_ids,
      "failure_field_issues" => finite_failure_field_issues,
      "pass" => finite_failed_ids.empty? && finite_failure_field_issues.empty?
    },
    {
      "id" => "producer_finite_row_integrity",
      "rows" => finite_row_audits,
      "pass" => finite_row_audits.length == required_ids.length &&
        finite_row_audits.all? { |row| row.fetch("pass") }
    },
    {
      "id" => "producer_D_post_fixture_integrity",
      "audit" => dpost_audit,
      "pass" => !dpost_audit.nil? && dpost_audit.fetch("pass")
    },
    {
      "id" => "claim_boundary",
      "mismatches" => claim_mismatches,
      "unexpected_fields" => claim_boundary.is_a?(Hash) ? claim_boundary.keys - EXPECTED_CLAIM_BOUNDARY.keys : [],
      "pass" => claim_boundary.is_a?(Hash) && claim_mismatches.empty? &&
        (claim_boundary.keys - EXPECTED_CLAIM_BOUNDARY.keys).empty?
    }
  ]

  {
    "certificate_path" => certificate_path,
    "certificate_sha256" => Digest::SHA256.hexdigest(raw),
    "producer_summary" => summary,
    "checks" => checks,
    "pass" => checks.all? { |row| row.fetch("pass") }
  }
rescue Errno::ENOENT, JSON::ParserError, KeyError, TypeError => error
  {
    "certificate_path" => certificate_path,
    "error" => "#{error.class}: #{error.message}",
    "pass" => false
  }
end

if ARGV.length > 1
  warn "usage: ruby #{File.basename(__FILE__)} [python-certificate.json]"
  exit 2
end

certificate_path = File.expand_path(ARGV.fetch(0, DEFAULT_CERTIFICATE_PATH))

# Complete every independent arithmetic reconstruction before opening JSON.
dpost_check, dpost_mutation = reconstruct_dpost_fixture_and_mutation
independent_checks = [
  reconstruct_stopped_rows,
  reconstruct_omega_monotonicity,
  reconstruct_event_identity,
  dpost_check,
  reconstruct_block_abel,
  reconstruct_genealogy_counts,
  reconstruct_witness,
  reconstruct_epsilon_exponent_gap,
  mutation_audit(dpost_mutation)
]
producer_cross_check = python_certificate_cross_check(certificate_path)
passed = independent_checks.all? { |row| row.fetch("pass") } && producer_cross_check.fetch("pass")

output = {
  "schema" => "r074s-cross-channel-recombination-independent-ruby-v1",
  "engine" => "Ruby Rational independent reconstruction",
  "scope" => [
    "FINITE ONLY",
    "independent stopped-row and grouped-event arithmetic with tied stops",
    "independent exact Omega insertion and epsilon exponent-gap fixtures",
    "independent nonnegative-cutoff D_post fixture with signed Q and tied stops",
    "independent finite block Abel and genealogy counts",
    "abstract scalar witness only; no PDE realization",
    "Python JSON used only for schema and row/summary integrity cross-checks",
    "NOT CLAY"
  ],
  "note" => NOTE_PATH,
  "note_sha256" => Digest::SHA256.file(NOTE_PATH).hexdigest,
  "independent_checks" => independent_checks,
  "producer_cross_check" => producer_cross_check,
  "summary" => {
    "result" => passed ? "PASS" : "FAIL",
    "independent_passed" => independent_checks.count { |row| row.fetch("pass") },
    "independent_total" => independent_checks.length,
    "mutations_passed" => independent_checks.last.fetch("passed"),
    "mutations_total" => independent_checks.last.fetch("total"),
    "producer_cross_check" => producer_cross_check.fetch("pass") ? "PASS" : "FAIL"
  }
}

puts JSON.pretty_generate(output)
exit(passed ? 0 : 1)
