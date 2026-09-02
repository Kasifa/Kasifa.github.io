#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent finite/algebraic audit for R0.74S Step 8.
#
# All mathematical fixtures below are reconstructed with Ruby Rational before
# the Python producer artifact is inspected.  The script checks scalar and
# finite-measure models only.  It does not machine-prove the inherited PDE,
# compactness, spatial Holder, or shell-ledger results.

require "digest"
require "json"
require "set"

REPO = File.expand_path("..", __dir__)
NOTE_PATH = File.expand_path(
  ENV.fetch(
    "R074S_DEFECT_NOTE",
    File.join(REPO, "research/r074s_defect_relaxed_total_rayleigh_excess.md")
  )
)
CERTIFICATE_PATH = File.expand_path(
  ENV.fetch(
    "R074S_DEFECT_JSON",
    File.join(REPO, "research/r074s_defect_relaxed_total_rayleigh_certificate.json")
  )
)
GENERATOR_PATH = File.expand_path(
  ENV.fetch(
    "R074S_DEFECT_GENERATOR",
    File.join(REPO, "scripts/r074s_defect_relaxed_total_rayleigh_certificate.py")
  )
)
REPORT_PATH = File.expand_path(
  ENV.fetch(
    "R074S_DEFECT_REPORT",
    File.join(REPO, "research/r074s_defect_relaxed_total_rayleigh_certificate_report.md")
  )
)

EXPECTED_NOTE_FIELD = "research/r074s_defect_relaxed_total_rayleigh_excess.md"
EXPECTED_GENERATOR_FIELD = "scripts/r074s_defect_relaxed_total_rayleigh_certificate.py"
EXPECTED_SCHEMA = "r074s-defect-relaxed-total-rayleigh-certificate-v1"

EXPECTED_PRIMARY_IDS = {
  "exact_checks" => %w[
    priority_half_minus_beta_minus_sigma
    sigma_threshold_contributes_one_sixth
    beta_threshold_reciprocal
    excess_threshold_reciprocal
    jensen_four_R_squared_constant_squared
    per_shell_power_of_two_exponent
    per_shell_gamma_exponent
    per_shell_lambda_exponent
    per_shell_payment_exponent
    C4_cubed_scalar
    cross_shell_holder_reciprocal_exponents
    cross_shell_coefficient_cube_gamma
    cross_shell_coefficient_cube_dyadic
    selected_flux_sharp_coefficient
    direct_clock_to_full_flux_one_BQ
    exact_family_ratio_identity_at_K_4096
  ],
  "finite_checks" => %w[
    finite_signed_measure_scalar_x_below_Jordan_X
    finite_nonnegative_measure_decomposition
    exact_one_sixth_beta_sigma_x_priority_trichotomy
    exact_rational_Jensen_on_normalized_length_below_four
    C4_equals_12_times_2C1_to_two_thirds_cube_identity
    exact_rational_cross_shell_Holder
    finite_selected_and_global_excess_ledgers
    exact_shear_terminal_scalar_excess_absorbed_by_beta
    finite_Portmanteau_positive_part_lsc_direction_proxy
    finite_compact_test_supremum_lsc_proxy_for_Jordan_X
    finite_absolute_continuous_density_x_versus_X_cancellation
    open_terminal_endpoint_escape_direction
    finite_terminal_Q_variation_to_signed_flux_reduction
    finite_global_scalar_excess_to_flux_variation_ledger
    exact_selected_flux_six_fifths_coefficient
    finite_selected_excess_to_common_terminal_stopped_work_proxy
    finite_no_exception_clock_and_flux_comparison
    finite_inherited_exact_family_universal_quadratic_refutation_proxy
    finite_S38_conditional_implication_arithmetic
  ],
  "negative_mutations" => %w[
    mutation_reorder_priority_sigma_before_beta
    mutation_stale_or_undefined_I_X_selected_index
    mutation_beta_threshold_one_sixth_to_one_fifth
    mutation_sigma_threshold_denominator_twelve_to_ten
    mutation_Jensen_half_constant_to_one
    mutation_drop_factor_two_inside_C4
    mutation_conflate_scalar_x_with_Jordan_X
    mutation_close_hard_terminal_endpoint
    mutation_promote_fixed_scale_X_finiteness_to_quadratic_bound
    mutation_promote_linear_scalar_flux_bound_to_quadratic
    mutation_change_universal_gate_REFUTED_back_to_OPEN
    mutation_delete_common_zero_start_from_lower_comparison
    mutation_weaken_sharp_BQ_flux_comparison_to_2BQ
    mutation_delete_BQ_error_from_flux_comparison
    mutation_promote_liminf_to_hard_mass_convergence
    mutation_assert_smooth_density_existence
    mutation_assert_selected_sum_lsc
    mutation_assert_X_zero_for_shear
    mutation_promote_finite_certificate_to_measure_PDE_Clay
    mutation_drop_selected_six_fifths_coefficient_to_one
  ]
}.freeze

EXPECTED_PRIMARY_SCOPE = {
  "finite_algebraic_only" => true,
  "machine_proves_Jordan_or_Radon_regularity" => false,
  "machine_proves_Navier_Stokes_PDE" => false,
  "machine_proves_Portmanteau_or_measure_topology" => false,
  "machine_proves_good_stop_selection_or_primitive_continuity" => false,
  "machine_proves_inherited_R074O_R074P_exact_PDE_family" => false,
  "machine_proves_inherited_R074P_R074R_analysis" => false,
  "machine_proves_regularity_or_Clay" => false,
  "machine_proves_smooth_approximation_existence" => false
}.freeze

REQUIRED_PRIMARY_STRUCTURAL_IDS = %w[
  tags_consecutive_S163_through_S199
  tags_unique
  priority_order_beta_sigma_x
  selected_index_is_I_x
  literal_thresholds
  scalar_and_Jordan_definitions_distinct
  open_terminal_endpoint
  sharp_five_sixths_six_fifths
  fixed_scale_Jordan_finiteness
  global_scalar_linear_flux_ledger
  no_exception_clock_comparison
  no_exception_common_zero_start
  universal_gate_refuted_not_open
].freeze

EXPECTED_PRIMARY_EXACT_VALUES = {
  "direct_clock_to_full_flux_one_BQ" => {
    "left" => "1/1", "right" => "1/1", "margin" => "0/1"
  },
  "exact_family_ratio_identity_at_K_4096" => {
    "left" => "4096/1", "right" => "4096/1", "margin" => "0/1"
  }
}.freeze

def fraction_string(value)
  "#{value.numerator}/#{value.denominator}"
end

def deep_copy(value)
  Marshal.load(Marshal.dump(value))
end

def positive_part(value)
  [value, Rational(0)].max
end

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

def compact_source(body)
  body.gsub(/\s+/, "").delete("&").gsub(/\\[,!;:]/, "")
end

def exact_row(identifier, left, right, meaning)
  {
    "id" => identifier,
    "left" => fraction_string(left),
    "right" => fraction_string(right),
    "margin" => fraction_string(left - right),
    "meaning" => meaning,
    "pass" => left == right
  }
end

def independent_exact_bookkeeping
  rows = [
    exact_row(
      "three_equal_shares_of_half",
      Rational(1, 2) / 3,
      Rational(1, 6),
      "beta, normalized kinetic mass, and scalar excess split the guaranteed half"
    ),
    exact_row(
      "sigma_threshold_from_normalized_share",
      Rational(1, 6) / 2,
      Rational(1, 12),
      "2 lambda sigma has threshold T/6 exactly when sigma has threshold T/(12 lambda)"
    ),
    exact_row(
      "strict_residual_share",
      Rational(1, 2) - Rational(1, 6) - Rational(1, 6),
      Rational(1, 6),
      "failure of the first two priority tests leaves strict scalar excess above T/6"
    ),
    exact_row(
      "equal_share_maximin_budget",
      3 * Rational(1, 6),
      Rational(1, 2),
      "three guaranteed nonnegative contributions cannot all have threshold above one sixth"
    ),
    exact_row(
      "beta_reciprocal_constant",
      6 * Rational(1, 6),
      Rational(1),
      "the beta branch has terminal coefficient six"
    ),
    exact_row(
      "scalar_excess_reciprocal_constant",
      6 * Rational(1, 6),
      Rational(1),
      "the selected scalar-excess branch has terminal coefficient six"
    ),
    exact_row(
      "jensen_four_parabolic_units",
      4 * Rational(1, 2)**2,
      Rational(1),
      "delta at most four gives delta to minus one half at least one half"
    ),
    exact_row(
      "per_shell_power_of_two",
      Rational(3, 2) * Rational(2, 3),
      Rational(1),
      "raising 2^(3k/2) to power 2/3 gives 2^k"
    ),
    exact_row(
      "per_shell_gamma_power",
      Rational(1, 2) * Rational(2, 3),
      Rational(1, 3),
      "raising gamma^(1/2) to power 2/3 gives gamma^(1/3)"
    ),
    exact_row(
      "per_shell_lambda_power",
      Rational(3, 2) * Rational(2, 3),
      Rational(1),
      "the kinetic threshold leaves one power of lambda"
    ),
    exact_row(
      "per_shell_payment_power",
      Rational(1) * Rational(2, 3),
      Rational(2, 3),
      "the cubic payment is raised to power 2/3"
    ),
    exact_row(
      "C4_integer_factor",
      Rational(12),
      Rational(12),
      "the threshold T/(12 lambda) produces the literal factor twelve"
    ),
    exact_row(
      "C4_factor_two_exponent",
      Rational(1) * Rational(2, 3),
      Rational(2, 3),
      "the Jensen one half becomes 2^(2/3) after inversion"
    ),
    exact_row(
      "cross_shell_holder_exponents",
      Rational(1, 3) + Rational(2, 3),
      Rational(1),
      "Holder uses conjugate exponents 3 and 3/2"
    ),
    exact_row(
      "cross_shell_gamma_cube",
      3 * Rational(1, 3),
      Rational(1),
      "cubing the shell coefficient leaves gamma to power one"
    ),
    exact_row(
      "critical_profile_dyadic_power",
      Rational(3) - 3 * Rational(1),
      Rational(0),
      "the critical profile leaves one in every coefficient-ledger row"
    ),
    exact_row(
      "canonical_profile_sum",
      Rational(1, 8) / (1 - Rational(1, 8)),
      Rational(1, 7),
      "epsilon one gives the geometric sum one seventh"
    ),
    exact_row(
      "terminal_flux_nonbeta_share",
      Rational(1) - Rational(1, 6),
      Rational(5, 6),
      "failure of the beta test and K=Q+F leave more than five sixths in F"
    ),
    exact_row(
      "terminal_flux_reciprocal",
      Rational(6, 5) * Rational(5, 6),
      Rational(1),
      "the direct selected terminal-flux coefficient is six fifths"
    ),
    exact_row(
      "full_flux_equivalence_coefficient",
      Rational(1),
      Rational(1),
      "the shell partition spends each Q-variation row once, not twice"
    ),
    exact_row(
      "zero_clock_negative_Q_sharp_margin",
      (Rational(0) - Rational(1)).abs,
      Rational(1),
      "K=0, Q=-1, F=1 makes |W-C_full|=B_Q"
    ),
    exact_row(
      "exact_family_ratio_lower_bound",
      (Rational(8) - Rational(1)) / Rational(1),
      Rational(7),
      "C_full/A=K_star and B_Q/A<=1 give W_up/A>=K_star-1"
    )
  ]

  {
    "id" => "independent_exact_bookkeeping",
    "rows" => rows,
    "pass" => rows.all? { |row| row.fetch("pass") }
  }
end

def independent_priority_trichotomy
  terminals = [Rational(1, 2), Rational(1), Rational(3, 2), Rational(2)]
  denominator = 24
  configurations = 0
  eligible = 0
  counts = Hash.new(0)
  failures = []

  terminals.each do |terminal|
    grid = (0..16).map { |index| terminal * Rational(index, denominator) }
    grid.repeated_permutation(3) do |nu, beta, kinetic|
      configurations += 1
      next if nu < terminal / 2

      eligible += 1
      scalar_excess = positive_part(nu - beta - kinetic)
      branch = if beta >= terminal / 6
                 "beta"
               elsif kinetic > terminal / 6
                 "sigma"
               else
                 "x"
               end
      counts[branch] += 1
      conditions = [
        branch != "beta" || terminal <= 6 * beta,
        branch != "sigma" || (beta < terminal / 6 && kinetic > terminal / 6),
        branch != "x" || (
          beta < terminal / 6 && kinetic <= terminal / 6 &&
          scalar_excess > terminal / 6 && terminal < 6 * scalar_excess
        )
      ]
      next if conditions.all?

      failures << {
        "T" => fraction_string(terminal),
        "nu" => fraction_string(nu),
        "beta" => fraction_string(beta),
        "two_lambda_sigma" => fraction_string(kinetic),
        "x" => fraction_string(scalar_excess),
        "branch" => branch
      } if failures.length < 12
    end
  end

  {
    "id" => "independent_priority_trichotomy_grid",
    "grid_denominator" => denominator,
    "configurations_checked" => configurations,
    "eligible_checked" => eligible,
    "class_counts" => counts.sort.to_h,
    "failures" => failures,
    "pass" => failures.empty? && counts.values.sum == eligible && counts.keys.sort == %w[beta sigma x]
  }
end

def independent_maximin_check
  denominator = 48
  candidates = []
  best = Rational(-1)

  (0..24).each do |a_num|
    (0..24 - a_num).each do |b_num|
      c_num = 24 - a_num - b_num
      shares = [a_num, b_num, c_num].map { |value| Rational(value, denominator) }
      floor = shares.min
      best = floor if floor > best
      candidates << shares if floor == Rational(1, 6)
    end
  end

  {
    "id" => "independent_equal_share_maximin",
    "allocations_checked" => 325,
    "best_guaranteed_share" => fraction_string(best),
    "maximizers" => candidates.map { |row| row.map { |value| fraction_string(value) } },
    "pass" => best == Rational(1, 6) && candidates == [[Rational(1, 6)] * 3]
  }
end

def independent_jensen_check
  deltas = [Rational(1, 2), Rational(1), Rational(2), Rational(3), Rational(4)]
  values = [Rational(0), Rational(1, 2), Rational(1), Rational(2), Rational(3)]
  configurations = 0
  equality_cases = 0
  failures = []

  deltas.each do |delta|
    values.repeated_permutation(3) do |q_values|
      configurations += 1
      cell = delta / 3
      sigma = cell * q_values.sum { |q| q**2 }
      cubic = cell * q_values.sum { |q| q**3 }
      jensen_margin = delta * cubic**2 - sigma**3
      equality_cases += 1 if jensen_margin.zero?

      # If sigma is strictly larger than this rational proxy threshold, the
      # source's weaker one-half consequence must also be strict.
      threshold = sigma * Rational(3, 4)
      consequence = sigma.zero? || 4 * cubic**2 > threshold**3
      next if jensen_margin >= 0 && consequence

      failures << {
        "delta" => fraction_string(delta),
        "q" => q_values.map { |q| fraction_string(q) },
        "sigma" => fraction_string(sigma),
        "cubic" => fraction_string(cubic),
        "jensen_margin" => fraction_string(jensen_margin)
      } if failures.length < 12
    end
  end

  {
    "id" => "independent_step_function_jensen",
    "configurations_checked" => configurations,
    "equality_cases" => equality_cases,
    "failures" => failures,
    "pass" => failures.empty? && equality_cases.positive?
  }
end

def independent_cross_shell_holder
  coefficients = [Rational(1, 3), Rational(1), Rational(2)]
  roots = [Rational(0), Rational(1, 2), Rational(1), Rational(2)]
  configurations = 0
  equality_cases = 0
  failures = []

  coefficients.repeated_permutation(3) do |a|
    roots.repeated_permutation(3) do |q|
      configurations += 1
      left = a.zip(q).sum { |coefficient, root| coefficient * root**2 }
      coefficient_cube = a.sum { |coefficient| coefficient**3 }
      payment = q.sum { |root| root**3 }
      margin = coefficient_cube * payment**2 - left**3
      equality_cases += 1 if margin.zero?
      next if margin >= 0

      failures << {
        "a" => a.map { |value| fraction_string(value) },
        "cube_roots_of_p" => q.map { |value| fraction_string(value) },
        "margin" => fraction_string(margin)
      } if failures.length < 12
    end
  end

  {
    "id" => "independent_cross_shell_holder",
    "configurations_checked" => configurations,
    "equality_cases" => equality_cases,
    "failures" => failures,
    "pass" => failures.empty? && equality_cases.positive?
  }
end

def independent_scalar_jordan_order
  values = [Rational(-2), Rational(-1), Rational(0), Rational(1), Rational(2)]
  configurations = 0
  strict_cases = 0
  failures = []

  values.repeated_permutation(4) do |atoms|
    configurations += 1
    scalar = positive_part(atoms.sum)
    jordan = atoms.sum { |value| positive_part(value) }
    strict_cases += 1 if scalar < jordan
    next if scalar >= 0 && scalar <= jordan

    failures << {
      "atoms" => atoms.map { |value| fraction_string(value) },
      "x" => fraction_string(scalar),
      "X" => fraction_string(jordan)
    } if failures.length < 12
  end

  {
    "id" => "independent_scalar_and_jordan_order",
    "configurations_checked" => configurations,
    "strict_cancellation_cases" => strict_cases,
    "failures" => failures,
    "pass" => failures.empty? && strict_cases.positive?
  }
end

def independent_total_mass_bound
  values = [Rational(0), Rational(1, 6), Rational(1, 2), Rational(1), Rational(2)]
  configurations = 0
  failures = []

  values.repeated_permutation(3) do |nu, beta, kinetic|
    configurations += 1
    scalar = positive_part(nu - beta - kinetic)
    jordan = scalar # one-atom measure
    conditions = [
      nu <= beta + kinetic + scalar,
      scalar <= jordan
    ]
    next if conditions.all?

    failures << {
      "nu" => fraction_string(nu),
      "beta" => fraction_string(beta),
      "two_lambda_sigma" => fraction_string(kinetic)
    } if failures.length < 12
  end

  {
    "id" => "independent_total_mass_positive_part_bound",
    "configurations_checked" => configurations,
    "failures" => failures,
    "pass" => failures.empty?
  }
end

def independent_step7_domination
  values = [Rational(0), Rational(1, 4), Rational(1), Rational(2)]
  lambdas = [Rational(1, 4), Rational(1), Rational(2)]
  configurations = 0
  strict_cases = 0
  failures = []

  lambdas.each do |lambda|
    values.repeated_permutation(4) do |g1, g2, defect, beta|
      e1 = Rational(1, 2)
      e2 = Rational(1)
      configurations += 1
      cells = [[g1, e1], [g2, e2]]
      alpha_atoms = cells.each_with_index.map do |(g, energy), index|
        local_defect = index.zero? ? defect : Rational(0)
        local_beta = index == 1 ? beta : Rational(0)
        local_defect + g - local_beta - 2 * lambda * energy
      end
      jordan = alpha_atoms.sum { |value| positive_part(value) }
      scalar = positive_part(alpha_atoms.sum)
      high_viscous = cells.sum do |g, energy|
        g > 2 * lambda * energy ? g : Rational(0)
      end
      raw = defect + high_viscous
      strict_cases += 1 if jordan < raw
      next if scalar <= jordan && jordan <= raw

      failures << {
        "lambda" => fraction_string(lambda),
        "g" => [g1, g2].map { |value| fraction_string(value) },
        "defect" => fraction_string(defect),
        "beta" => fraction_string(beta),
        "x" => fraction_string(scalar),
        "X" => fraction_string(jordan),
        "raw" => fraction_string(raw)
      } if failures.length < 12
    end
  end

  {
    "id" => "independent_step7_raw_residual_domination",
    "configurations_checked" => configurations,
    "strict_cases" => strict_cases,
    "failures" => failures,
    "pass" => failures.empty? && strict_cases.positive?
  }
end

def independent_smooth_density_formula
  values = [Rational(0), Rational(1, 4), Rational(1), Rational(2)]
  lambdas = [Rational(1, 2), Rational(1), Rational(2)]
  configurations = 0
  cancellation_cases = 0
  failures = []

  lambdas.each do |lambda|
    values.repeated_permutation(3) do |g_values|
      q_values = [g_values[1], g_values[2], g_values[0] - Rational(1, 4)]
      e_values = [g_values[2], g_values[0], g_values[1]]
      weights = [Rational(1, 4), Rational(1, 3), Rational(5, 12)]
      atoms = 3.times.map do |index|
        weights[index] * (
          g_values[index] - q_values[index].abs - 2 * lambda * e_values[index]
        )
      end
      scalar_from_measure = positive_part(atoms.sum)
      jordan_from_measure = atoms.sum { |value| positive_part(value) }
      scalar_from_formula = positive_part(
        3.times.sum do |index|
          weights[index] * (
            g_values[index] - q_values[index].abs - 2 * lambda * e_values[index]
          )
        end
      )
      jordan_from_formula = 3.times.sum do |index|
        weights[index] * positive_part(
          g_values[index] - q_values[index].abs - 2 * lambda * e_values[index]
        )
      end
      configurations += 1
      cancellation_cases += 1 if scalar_from_measure < jordan_from_measure
      next if scalar_from_measure == scalar_from_formula && jordan_from_measure == jordan_from_formula

      failures << {
        "lambda" => fraction_string(lambda),
        "g" => g_values.map { |value| fraction_string(value) },
        "qdot" => q_values.map { |value| fraction_string(value) },
        "e" => e_values.map { |value| fraction_string(value) }
      } if failures.length < 12
    end
  end

  {
    "id" => "independent_smooth_density_formula",
    "configurations_checked" => configurations,
    "strict_cancellation_cases" => cancellation_cases,
    "failures" => failures,
    "pass" => failures.empty? && cancellation_cases.positive?
  }
end

def independent_endpoint_lsc
  # On J=(0,1), delta_(1-1/n) converges ambiently to delta_1.  The limit
  # open-set mass is zero and every approximating open-set mass is one.
  portmanteau_limit = Rational(0)
  portmanteau_liminf = Rational(1)

  # Positive and negative atoms may collide.  Jordan positive mass can drop,
  # but cannot jump above the liminf in this model.
  jordan_limit = Rational(0)
  jordan_liminf = Rational(1)

  {
    "id" => "independent_open_endpoint_and_jordan_lsc",
    "portmanteau_limit" => fraction_string(portmanteau_limit),
    "portmanteau_liminf" => fraction_string(portmanteau_liminf),
    "jordan_limit" => fraction_string(jordan_limit),
    "jordan_liminf" => fraction_string(jordan_liminf),
    "pass" => (
      portmanteau_limit <= portmanteau_liminf &&
      jordan_limit <= jordan_liminf
    )
  }
end

def independent_flux_bridge
  terminals = [Rational(1, 2), Rational(1), Rational(2)]
  q_values = [Rational(-1, 6), Rational(-1, 12), Rational(0), Rational(1, 12)]
  e_fractions = [Rational(0), Rational(1, 4), Rational(1, 2)]
  sigma_terms = [Rational(0), Rational(1, 24), Rational(1, 12), Rational(1, 6)]
  beta_slacks = [Rational(0), Rational(1, 48), Rational(1, 12)]
  configurations = 0
  residual_cases = 0
  failures = []

  terminals.product(q_values, e_fractions, sigma_terms, beta_slacks).each do |
    terminal, q_fraction, e_fraction, kinetic_fraction, beta_slack
  |
    q = terminal * q_fraction
    endpoint_energy = terminal * e_fraction
    next if endpoint_energy > terminal / 2

    dissipation = terminal - endpoint_energy
    kinetic = terminal * kinetic_fraction
    beta = q.abs + terminal * beta_slack
    flux = terminal - q
    alpha = dissipation - beta - kinetic
    scalar = positive_part(alpha)
    configurations += 1

    base_conditions = [
      beta >= q.abs,
      scalar <= positive_part(flux - endpoint_energy - kinetic),
      scalar <= positive_part(flux)
    ]

    in_x = beta < terminal / 6 && kinetic <= terminal / 6 && scalar > terminal / 6
    if in_x
      residual_cases += 1
      base_conditions.concat([
        flux > 5 * terminal / 6,
        terminal < Rational(6, 5) * flux,
        flux.positive?
      ])
    end
    next if base_conditions.all?

    failures << {
      "T" => fraction_string(terminal),
      "Q" => fraction_string(q),
      "beta" => fraction_string(beta),
      "E" => fraction_string(endpoint_energy),
      "two_lambda_sigma" => fraction_string(kinetic),
      "F" => fraction_string(flux),
      "x" => fraction_string(scalar),
      "in_Ix" => in_x
    } if failures.length < 12
  end

  {
    "id" => "independent_terminal_flux_bridge",
    "configurations_checked" => configurations,
    "selected_residual_cases" => residual_cases,
    "failures" => failures,
    "pass" => failures.empty? && residual_cases.positive?
  }
end

def independent_shear_boundary
  terminals = [Rational(1, 4), Rational(1), Rational(3)]
  sigmas = [Rational(0), Rational(1, 5), Rational(2)]
  configurations = 0
  failures = []

  terminals.product(sigmas).each do |terminal, sigma|
    nu = terminal * Rational(3, 4)
    beta = terminal
    scalar = positive_part(nu - beta - sigma)
    configurations += 1
    failures << {
      "T" => fraction_string(terminal),
      "nu" => fraction_string(nu),
      "beta" => fraction_string(beta),
      "sigma_term" => fraction_string(sigma)
    } unless scalar.zero?
  end

  # This two-cell signed measure has total nu <= total beta and x=0, but
  # positive Jordan mass.  It proves only that terminal totals cannot imply
  # X=0; it is not asserted to be the exact shear's local density.
  alpha_atoms = [Rational(2), Rational(-3)]
  scalar_witness = positive_part(alpha_atoms.sum)
  jordan_witness = alpha_atoms.sum { |value| positive_part(value) }

  {
    "id" => "independent_shear_x_zero_X_unknown",
    "configurations_checked" => configurations,
    "terminal_total_x" => fraction_string(scalar_witness),
    "possible_local_X" => fraction_string(jordan_witness),
    "failures" => failures,
    "pass" => failures.empty? && scalar_witness.zero? && jordan_witness.positive?
  }
end

def discrete_terminal_observables(k_rows, q_rows)
  shell_count = k_rows.length
  time_count = k_rows.fetch(0).length
  raise ArgumentError, "shape mismatch" unless q_rows.length == shell_count
  raise ArgumentError, "empty time grid" unless time_count >= 2
  raise ArgumentError, "shape mismatch" unless (k_rows + q_rows).all? { |row| row.length == time_count }
  raise ArgumentError, "nonzero initial clock" unless (k_rows + q_rows).all? { |row| row.fetch(0).zero? }
  raise ArgumentError, "negative completed clock" unless k_rows.flatten.all? { |value| value >= 0 }

  flux_rows = shell_count.times.map do |shell|
    time_count.times.map { |time| k_rows[shell][time] - q_rows[shell][time] }
  end
  b_q = q_rows.sum do |row|
    (1...time_count).sum { |time| (row[time] - row[time - 1]).abs }
  end
  k_sup = (1...time_count).map do |time|
    k_rows.sum { |row| row[time] }
  end.max
  c_full = (1...time_count).map do |time|
    positive_part(flux_rows.sum { |row| row[time] })
  end.max

  w_up = (1...time_count).map do |terminal|
    shell_contributions = shell_count.times.map do |shell|
      valid = (0...terminal).select do |stop|
        k_rows[shell][terminal] - k_rows[shell][stop] > k_rows[shell][terminal] / 4
      end
      next Rational(0) if valid.empty?

      best = valid.map do |stop|
        flux_rows[shell][terminal] - flux_rows[shell][stop]
      end.max
      positive_part(best)
    end
    shell_contributions.sum
  end.max

  {
    "B_Q" => b_q,
    "K_sup" => k_sup,
    "C_full" => c_full,
    "W_up" => w_up
  }
end

def independent_no_exception_equivalence
  k_values = [Rational(0), Rational(1), Rational(2)]
  q_values = [Rational(-1), Rational(0), Rational(1)]
  configurations = 0
  equality_c_minus_w = 0
  equality_w_minus_c = 0
  failures = []

  # Two shells and two post-initial times.  Piecewise-linear interpolation
  # realizes every row with nonnegative K and absolutely continuous Q.
  k_values.repeated_permutation(4) do |k_flat|
    q_values.repeated_permutation(4) do |q_flat|
      k_rows = [[Rational(0), k_flat[0], k_flat[1]],
                [Rational(0), k_flat[2], k_flat[3]]]
      q_rows = [[Rational(0), q_flat[0], q_flat[1]],
                [Rational(0), q_flat[2], q_flat[3]]]
      observed = discrete_terminal_observables(k_rows, q_rows)
      b_q = observed.fetch("B_Q")
      k_sup = observed.fetch("K_sup")
      c_full = observed.fetch("C_full")
      w_up = observed.fetch("W_up")
      configurations += 1
      equality_c_minus_w += 1 if c_full - w_up == b_q && b_q.positive?
      equality_w_minus_c += 1 if w_up - c_full == b_q && b_q.positive?
      conditions = [
        k_sup - b_q <= w_up,
        w_up <= k_sup + b_q,
        (w_up - c_full).abs <= b_q
      ]
      next if conditions.all?

      failures << {
        "K" => k_rows.map { |row| row.map { |value| fraction_string(value) } },
        "Q" => q_rows.map { |row| row.map { |value| fraction_string(value) } },
        "observed" => observed.transform_values { |value| fraction_string(value) }
      } if failures.length < 12
    end
  end

  sharp = discrete_terminal_observables(
    [[Rational(0), Rational(0)]],
    [[Rational(0), Rational(-1)]]
  )
  sharp_conditions = [
    sharp.fetch("B_Q") == 1,
    sharp.fetch("K_sup") == 0,
    sharp.fetch("C_full") == 1,
    sharp.fetch("W_up") == 0,
    (sharp.fetch("W_up") - sharp.fetch("C_full")).abs == sharp.fetch("B_Q")
  ]

  {
    "id" => "independent_no_exception_gate_equivalence",
    "configurations_checked" => configurations,
    "C_minus_W_sharp_cases" => equality_c_minus_w,
    "W_minus_C_sharp_cases" => equality_w_minus_c,
    "zero_clock_negative_Q_stress" => sharp.transform_values { |value| fraction_string(value) },
    "failures" => failures,
    "pass" => failures.empty? && sharp_conditions.all? && equality_c_minus_w.positive?
  }
end

def independent_exact_family_refutation
  k_stars = [2, 4, 8, 16, 32].map { |value| Rational(value) }
  rows = k_stars.map do |k_star|
    terminal_scale = k_star
    quadratic_scale = terminal_scale / k_star
    q_error = quadratic_scale
    stopped_lower = terminal_scale - q_error
    ratio_lower = stopped_lower / quadratic_scale
    {
      "K_star" => fraction_string(k_star),
      "terminal_scale" => fraction_string(terminal_scale),
      "quadratic_scale" => fraction_string(quadratic_scale),
      "stopped_ratio_lower" => fraction_string(ratio_lower),
      "expected_ratio_lower" => fraction_string(k_star - 1),
      "pass" => ratio_lower == k_star - 1
    }
  end

  {
    "id" => "independent_exact_family_universal_gate_refutation",
    "rows" => rows,
    "ratios_strictly_increase" => rows.each_cons(2).all? do |left, right|
      Rational(*left.fetch("stopped_ratio_lower").split("/").map(&:to_i)) <
        Rational(*right.fetch("stopped_ratio_lower").split("/").map(&:to_i))
    end,
    "pass" => rows.all? { |row| row.fetch("pass") } &&
      rows.each_cons(2).all? do |left, right|
        Rational(*left.fetch("stopped_ratio_lower").split("/").map(&:to_i)) <
          Rational(*right.fetch("stopped_ratio_lower").split("/").map(&:to_i))
      end
  }
end

def structural_results(note_body)
  compact = compact_source(note_body)
  tags = note_body.scan(/\\tag\{S\.(\d+)\}/).flatten.map(&:to_i)
  tag_counts = tags.each_with_object(Hash.new(0)) do |tag, counts|
    counts[tag] += 1
  end
  expected_tags = (163..tags.max).to_a
  checks = {
    "title" => note_body.include?("R0.74S Step 8"),
    "starts_at_S163" => tags.min == 163,
    "tags_contiguous" => tags == expected_tags,
    "tags_unique" => tag_counts.values.all? { |count| count == 1 },
    "contains_S199" => tags.max == 199,
    "open_terminal_interval" => compact.include?("J_\\tau:=(s_R,\\tau)"),
    "sigma_definition" => compact.include?("\\sigma_{k,R}(A):={1\\overR^2}\\int_Ae_{k,R}(t)dt"),
    "nu_definition" => compact.include?("\\nu_{k,R}(A):={\\gamma_k\\overR}"),
    "beta_absolute_density" => compact.include?("\\beta_{k,R}(A):=\\int_A|\\dotQ_{k,R}(t)|dt"),
    "measure_identity" => compact.include?("d\\nu_{k,R}(t)=g_{k,R}(t)dt+d\\boldsymbol\\delta_{k,R}(t)"),
    "scalar_before_jordan" => compact.include?("x_{k,R}^{\\boldsymbol\\lambda}(\\tau):=\\left[\\alpha_{k,R}^{\\boldsymbol\\lambda}(J_\\tau)\\right]_+"),
    "jordan_definition" => compact.include?("X_{k,R}^{\\boldsymbol\\lambda}(\\tau):=(\\alpha_{k,R}^{\\boldsymbol\\lambda})^+(J_\\tau)"),
    "x_le_X" => compact.include?("0\\le[\\alpha(J_\\tau)]_+\\le\\alpha^+(J_\\tau)"),
    "compact_test_variation" => compact.include?("\\sup_{\\substack{\\phi\\inC_c(J_\\tau)\\\\0\\le\\phi\\le1}}\\int_{J_\\tau}\\phid\\alpha"),
    "beta_threshold_sixth" => compact.include?("\\beta_{k,R}(J_\\tau)\\ge\\frac16T_k"),
    "sigma_threshold_twelve" => compact.include?("\\sigma_{k,R}(J_\\tau)>\\frac{T_k}{12\\lambda_k}"),
    "x_threshold_sixth" => compact.include?("x_{k,R}^{\\boldsymbol\\lambda}(\\tau)>\\frac16T_k"),
    "jensen_delta" => compact.include?("\\delta_\\tau^{-1/2}\\sigma_{k,R}(J_\\tau)^{3/2}"),
    "jensen_half" => compact.include?(">{1\\over2}\\left({T_k\\over12\\lambda_k}\\right)^{3/2}"),
    "C4_constant" => compact.include?("C_4=12(2C_1)^{2/3}"),
    "coefficient_ledger" => compact.include?("\\sum_{k\\ge1}2^{3k}\\gamma_k\\lambda_k^3"),
    "selected_residual" => compact.include?("6\\sum_{k\\in\\mathcalI_x(\\tau)}x_{k,R}^{\\boldsymbol\\lambda}(\\tau)"),
    "global_scalar_le_jordan" => compact.include?("\\mathfrakx_{1,R}^{\\boldsymbol\\lambda}(\\tau)\\le\\mathcalX_{1,R}^{\\boldsymbol\\lambda}(\\tau)"),
    "step7_domination" => compact.include?("x_{k,R}^{\\boldsymbol\\lambda}(\\tau)\\leX_{k,R}^{\\boldsymbol\\lambda}(\\tau)\\lem_{k,R}(\\tau)+\\int_{H_{k,R}}g_{k,R}(t)dt"),
    "shear_x_zero" => compact.include?("x_{k,R}^{\\boldsymbol\\lambda}(\\tau)=0"),
    "shear_X_not_claimed" => note_body.match?(/not asserted that\s+the Jordan-envelope value/i) || note_body.match?(/not claimed that\s+\\\(X_k\\\) vanishes/i),
    "portmanteau_open_direction" => compact.include?("\\nu_{k,R}(J_\\tau)\\le\\liminf_{n\\to\\infty}\\nu_{k,R}^{(n)}(J_\\tau)"),
    "scalar_lsc_direction" => compact.include?("x_{k,R}^{\\boldsymbol\\lambda}[u,p](\\tau)\\le\\liminf_{n\\to\\infty}x_{k,R}^{\\boldsymbol\\lambda}[u_n,p_n](\\tau)"),
    "jordan_lsc_direction" => compact.include?("X_{k,R}^{\\boldsymbol\\lambda}[u,p](\\tau)\\le\\liminf_{n\\to\\infty}X_{k,R}^{\\boldsymbol\\lambda}[u_n,p_n](\\tau)"),
    "smooth_scalar_formula" => compact.include?("\\left[\\int_{s_R}^{\\tau}\\left(g_{k,R}(t)-|\\dotQ_{k,R}(t)|-{2\\lambda_k\\overR^2}e_{k,R}(t)\\right)dt\\right]_+"),
    "smooth_jordan_formula" => compact.include?("\\int_{s_R}^{\\tau}\\left[g_{k,R}(t)-|\\dotQ_{k,R}(t)|-{2\\lambda_k\\overR^2}e_{k,R}(t)\\right]_+dt"),
    "conditional_smooth_approximation" => note_body.include?("conditionally") && note_body.include?("does not prove that every suitable weak solution admits smooth"),
    "functional_not_PDE" => note_body.match?(/not asserted to\s+solve Navier--Stokes/i),
    "endpoint_escape_test" => note_body.include?("Endpoint escape permits only lower semicontinuity"),
    "uniform_primitive_warning" => note_body.include?("Uniform primitive convergence is insufficient"),
    "scalar_linear_flux_bound" => compact.include?("\\mathfrakx_{1,R}^{\\boldsymbol\\lambda}(\\tau)\\le\\mathfrakW_{{\\rmup},R}^M"),
    "selected_flux_five_sixths" => compact.include?("F_{k,R}(\\tau)=T_k-Q_{k,R}(\\tau)\\geT_k-|Q_{k,R}(\\tau)|>{5T_k\\over6}"),
    "selected_flux_six_fifths" => compact.include?("\\sum_{k\\in\\mathcalI_x(\\tau)}K_{k,R}(\\tau)\\le{6\\over5}\\mathfrakW_{{\\rmup},R}^M"),
    "X_finiteness_bound" => compact.include?("\\mathcalX_{1,R}^{\\boldsymbol\\lambda}(\\tau)\\le\\sum_{k\\ge1}\\nu_{k,R}(J_\\tau)"),
    "scalar_flux_pointwise" => compact.include?("x_{k,R}^{\\boldsymbol\\lambda}(\\tau)\\le[F_{k,R}(\\tau)]_+"),
    "scalar_linear_payment" => compact.include?("\\le\\mathfrakL_{{\\rmabs},R}^M\\leCP_R^M"),
    "quadratic_Q_definition" => compact.include?("B_{Q,R}^M:=\\sum_{k\\ge1}\\operatorname{TV}_{[s_R,t_0)}Q_{k,R}\\leC_Q(P_R^M)^{2/3}"),
    "full_terminal_clock_definition" => compact.include?("\\mathcalK_R^M:=\\sup_{\\tau\\in\\mathcalG_R}\\sum_{k\\ge1}K_{k,R}(\\tau)"),
    "full_flux_definition" => compact.include?("\\mathfrakC_{{\\rmfull},R}^M:=\\sup_{s_R<\\tau<t_0}\\left[\\sum_{k\\ge1}F_{k,R}(\\tau)\\right]_+"),
    "terminal_clock_two_sided" => compact.include?("\\mathcalK_R^M-B_{Q,R}^M\\le\\mathfrakW_{{\\rmup},R}^M\\le\\mathcalK_R^M+B_{Q,R}^M"),
    "sharp_full_flux_equivalence" => compact.include?("\\bigl|\\mathfrakW_{{\\rmup},R}^M-\\mathfrakC_{{\\rmfull},R}^M\\bigr|\\leB_{Q,R}^M"),
    "zero_clock_negative_Q_stress" => compact.include?("K=0\\),\\(Q=-B\\),\\(F=B") && compact.include?("\\mathfrakC_{\\rmfull}=B") && compact.include?("\\mathfrakW_{\\rmup}=0"),
    "plateau_only_below_full" => compact.include?("\\mathfrakC_R^M\\le\\mathfrakC_{{\\rmfull},R}^M") && note_body.include?("equality is neither") && note_body.include?("needed nor claimed"),
    "exact_family_scale_separation" => compact.include?("(P_{R_j}^{M,*})^{2/3}\\asymp{T_*\\overK_*}") && compact.include?("K_*\\longrightarrow\\infty"),
    "stopped_ratio_diverges" => compact.include?("{\\mathfrakW_{{\\rmup},R_j}^{M,*}\\over(P_{R_j}^{M,*})^{2/3}}\\longrightarrow\\infty"),
    "universal_gate_refuted" => note_body.include?("The following are **REFUTED**") && note_body.include?("universal all-solution estimate"),
    "conditional_S38_preserved" => note_body.include?("The conditional implication (S.38) itself") && note_body.include?("remains correct"),
    "best_N_route_preserved" => note_body.include?("fixed best-\\(N_0\\)") || note_body.include?("fixed best-\\(N\\)"),
    "forbid_false_C_below_W" => !compact.include?("\\mathfrakC_{{\\rmfull},R}^M\\le\\mathfrakW_{{\\rmup},R}^M"),
    "forbid_old_two_B_coefficient" => !compact.include?("\\le2B_{Q,R}^M"),
    "no_false_infinite_global_claim" => !note_body.include?("global excess sums can be infinite"),
    "no_selected_lsc_claim" => note_body.include?("selected excess sum is lower semicontinuous") && note_body.include?("NOT CLAIMED"),
    "not_clay" => note_body.scan("NOT CLAY").length >= 2,
    "no_tab" => !note_body.include?("\t"),
    "no_control_characters" => !note_body.match?(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/),
    "no_trailing_whitespace" => note_body.lines.none? { |line| line.match?(/[ \t]+$/) }
  }

  checks.map do |identifier, passed|
    { "id" => identifier, "pass" => passed }
  end
end

def note_valid?(note_body)
  structural_results(note_body).all? { |row| row.fetch("pass") }
end

def independent_source_mutations(note_body)
  mutations = {
    "swap_scalar_jordan_order" => note_body.sub(
      "0\\le[\\alpha(J_\\tau)]_+\n &\\le\\alpha^+(J_\\tau)",
      "0\\le\\alpha^+(J_\\tau)\n &\\le[\\alpha(J_\\tau)]_+"
    ),
    "change_beta_threshold_to_fifth" => note_body.gsub("\\ge\\frac16T_k", "\\ge\\frac15T_k"),
    "change_sigma_denominator_twelve_to_ten" => note_body.gsub("\\frac{T_k}{12\\lambda_k}", "\\frac{T_k}{10\\lambda_k}"),
    "change_C4_twelve_to_ten" => note_body.sub("C_4=12(2C_1)^{2/3}", "C_4=10(2C_1)^{2/3}"),
    "reverse_portmanteau" => note_body.sub(
      "\\nu_{k,R}(J_\\tau)\n \\le\\liminf",
      "\\nu_{k,R}(J_\\tau)\n \\ge\\liminf"
    ),
    "delete_shear_boundary" => note_body.sub(/not asserted that\s+the Jordan-envelope value/i, "asserted that the Jordan-envelope value"),
    "delete_terminal_flux_bridge" => note_body.sub("\\mathfrak W_{{\\rm up},R}^M", "\\mathfrak W_{{\\rm missing},R}^M"),
    "promote_functional_family_to_PDE" => note_body.sub(/not asserted to\s+solve Navier--Stokes/i, "asserted to solve Navier--Stokes"),
    "remove_not_clay" => note_body.gsub("NOT CLAY", "CLAY")
  }

  mutations["weaken_sharp_B_to_two_B"] = note_body.gsub(
    "\\le B_{Q,R}^M.}\n\\tag{S.198}",
    "\\le 2B_{Q,R}^M.}\n\\tag{S.198}"
  )
  mutations["promote_false_C_below_W"] = note_body.sub(
    "\\bigl|\\mathfrak W_{{\\rm up},R}^M-",
    "\\mathfrak C_{{\\rm full},R}^M\\le\\mathfrak W_{{\\rm up},R}^M,\\qquad\\bigl|\\mathfrak W_{{\\rm up},R}^M-"
  )
  mutations["erase_zero_clock_stress"] = note_body.sub(
    "\\(K=0\\), \\(Q=-B\\), \\(F=B\\)",
    "\\(K=B\\), \\(Q=0\\), \\(F=B\\)"
  )
  mutations["promote_refuted_universal_gate"] = note_body.sub(
    "The following are **REFUTED**:",
    "The following are **PROVED**:"
  )
  mutations["refute_conditional_S38"] = note_body.sub(
    "The conditional implication (S.38) itself\n  remains correct.",
    "The conditional implication (S.38) itself\n  is refuted."
  )

  rows = mutations.map do |identifier, mutated|
    changed = mutated != note_body
    {
      "id" => identifier,
      "changed" => changed,
      "rejected" => changed && !note_valid?(mutated),
      "pass" => changed && !note_valid?(mutated)
    }
  end
  {
    "id" => "independent_source_mutations",
    "rows" => rows,
    "pass" => rows.all? { |row| row.fetch("pass") }
  }
end

def producer_validation(certificate, note_hash, generator_hash)
  errors = []
  errors << "root is not an object" unless certificate.is_a?(Hash)
  return errors unless certificate.is_a?(Hash)

  errors << "schema mismatch" unless certificate["schema"] == EXPECTED_SCHEMA
  errors << "producer pass is not true" unless certificate["pass"] == true

  source = certificate["source"]
  unless source.is_a?(Hash)
    errors << "source is not an object"
  else
    errors << "note path mismatch" unless source["note"] == EXPECTED_NOTE_FIELD
    errors << "generator path mismatch" unless source["generator"] == EXPECTED_GENERATOR_FIELD
    errors << "note hash mismatch" unless source["note_sha256"] == note_hash
    errors << "generator hash mismatch" unless source["generator_sha256"] == generator_hash
  end

  scope = certificate["scope"]
  unless scope.is_a?(Hash)
    errors << "scope is not an object"
  else
    errors << "scope mismatch" unless scope == EXPECTED_PRIMARY_SCOPE
  end

  groups = %w[exact_checks finite_checks structural_checks negative_mutations]
  summary_prefix = {
    "exact_checks" => "exact",
    "finite_checks" => "finite",
    "structural_checks" => "structural",
    "negative_mutations" => "negative_mutations"
  }
  groups.each do |group|
    rows = certificate[group]
    unless rows.is_a?(Array) && !rows.empty?
      errors << "#{group} missing or empty"
      next
    end
    errors << "#{group} has a failed row" unless rows.all? { |row| row.is_a?(Hash) && row["pass"] == true }
    identifiers = rows.each_with_object([]) do |row, values|
      values << row["id"] if row.is_a?(Hash) && row.key?("id")
    end
    errors << "#{group} has missing or duplicate ids" unless identifiers.length == rows.length && identifiers.uniq.length == identifiers.length
    if EXPECTED_PRIMARY_IDS.key?(group)
      errors << "#{group} id set mismatch" unless identifiers.to_set == EXPECTED_PRIMARY_IDS.fetch(group).to_set
      if group == "exact_checks"
        EXPECTED_PRIMARY_EXACT_VALUES.each do |identifier, expected|
          row = rows.find { |candidate| candidate["id"] == identifier }
          errors << "#{identifier} exact payload mismatch" unless row && expected.all? { |key, value| row[key] == value }
        end
      end
    elsif group == "structural_checks"
      errors << "structural check count mismatch" unless rows.length == 75
      errors << "required structural ids absent" unless REQUIRED_PRIMARY_STRUCTURAL_IDS.to_set.subset?(identifiers.to_set)
    end
  end

  summary = certificate["summary"]
  unless summary.is_a?(Hash)
    errors << "summary is not an object"
    return errors
  end

  groups.each do |group|
    rows = certificate[group]
    next unless rows.is_a?(Array)

    stem = summary_prefix.fetch(group)
    total_candidates = ["#{stem}_total", "#{group}_total"]
    passed_candidates = ["#{stem}_passed", "#{group}_passed"]
    total_key = total_candidates.find { |key| summary.key?(key) }
    passed_key = passed_candidates.find { |key| summary.key?(key) }
    errors << "#{group} summary total absent" if total_key.nil?
    errors << "#{group} summary passed absent" if passed_key.nil?
    errors << "#{group} summary total mismatch" if total_key && summary[total_key] != rows.length
    errors << "#{group} summary passed mismatch" if passed_key && summary[passed_key] != rows.count { |row| row["pass"] == true }
  end

  errors
end

def independent_artifact_mutations(certificate, note_hash, generator_hash)
  mutations = {}

  mutations["stale_note_hash"] = lambda do |copy|
    copy.fetch("source")["note_sha256"] = "0" * 64
  end
  mutations["stale_generator_hash"] = lambda do |copy|
    copy.fetch("source")["generator_sha256"] = "f" * 64
  end
  mutations["wrong_schema"] = lambda do |copy|
    copy["schema"] = "r074s-defect-relaxed-total-rayleigh-certificate-v0"
  end
  mutations["producer_pass_false"] = lambda do |copy|
    copy["pass"] = false
  end
  mutations["drop_exact_row"] = lambda do |copy|
    copy.fetch("exact_checks").pop
    copy.fetch("summary")["exact_total"] -= 1
    copy.fetch("summary")["exact_passed"] -= 1
  end
  mutations["duplicate_finite_id"] = lambda do |copy|
    rows = copy.fetch("finite_checks")
    rows[1]["id"] = rows[0]["id"]
  end
  mutations["flip_structural_pass"] = lambda do |copy|
    copy.fetch("structural_checks")[0]["pass"] = false
  end
  mutations["promote_analytic_scope"] = lambda do |copy|
    key = copy.fetch("scope").keys.find { |candidate| candidate.match?(/PDE|Navier|regularity|Clay|compactness|Jordan|Portmanteau|R211|R214/) }
    copy.fetch("scope")[key] = true
  end
  mutations["stale_summary"] = lambda do |copy|
    key = copy.fetch("summary").keys.find { |candidate| candidate.end_with?("_total") }
    copy.fetch("summary")[key] += 1
  end
  mutations["tamper_sharp_one_BQ_exact_row"] = lambda do |copy|
    row = copy.fetch("exact_checks").find do |candidate|
      candidate["id"] == "direct_clock_to_full_flux_one_BQ"
    end
    row["left"] = "2/1"
    row["margin"] = "1/1"
  end

  rows = mutations.map do |identifier, mutate|
    copy = deep_copy(certificate)
    begin
      mutate.call(copy)
      errors = producer_validation(copy, note_hash, generator_hash)
      {
        "id" => identifier,
        "errors" => errors,
        "pass" => !errors.empty?
      }
    rescue KeyError, NoMethodError, TypeError => error
      {
        "id" => identifier,
        "errors" => ["mutation setup failed: #{error.class}: #{error.message}"],
        "pass" => false
      }
    end
  end

  {
    "id" => "independent_artifact_mutations",
    "rows" => rows,
    "pass" => rows.all? { |row| row.fetch("pass") }
  }
end

def report_validation(report_body, certificate_hash, note_hash, generator_hash)
  checks = {
    "reports_PASS" => report_body.include?("**PASS**"),
    "binds_certificate_hash" => report_body.include?(certificate_hash),
    "binds_note_hash" => report_body.include?(note_hash),
    "binds_generator_hash" => report_body.include?(generator_hash),
    "finite_scope" => report_body.match?(/finite|algebraic/i),
    "denies_Clay" => report_body.include?("NOT CLAY")
  }
  checks.map { |identifier, passed| { "id" => identifier, "pass" => !!passed } }
end

unless File.file?(NOTE_PATH)
  warn "missing required note: #{NOTE_PATH}"
  exit 2
end

note_body = File.binread(NOTE_PATH).force_encoding(Encoding::UTF_8)
note_hash = sha256(NOTE_PATH)
independent_checks = [
  independent_exact_bookkeeping,
  independent_priority_trichotomy,
  independent_maximin_check,
  independent_jensen_check,
  independent_cross_shell_holder,
  independent_scalar_jordan_order,
  independent_total_mass_bound,
  independent_step7_domination,
  independent_smooth_density_formula,
  independent_endpoint_lsc,
  independent_flux_bridge,
  independent_shear_boundary,
  independent_no_exception_equivalence,
  independent_exact_family_refutation
]
structure = structural_results(note_body)
source_mutations = independent_source_mutations(note_body)

# Only after the independent rational, finite-measure, source, and mutation
# checks are complete do we inspect the Python producer and its artifacts.
producer_paths = [CERTIFICATE_PATH, GENERATOR_PATH, REPORT_PATH]
missing = producer_paths.reject { |path| File.file?(path) }
unless missing.empty?
  warn "missing required producer artifact(s): #{missing.join(', ')}"
  exit 2
end

certificate_body = File.binread(CERTIFICATE_PATH)
generator_hash = sha256(GENERATOR_PATH)
certificate_hash = sha256(CERTIFICATE_PATH)
report_hash = sha256(REPORT_PATH)
certificate = JSON.parse(certificate_body)
report_body = File.binread(REPORT_PATH).force_encoding(Encoding::UTF_8)
producer_errors = producer_validation(certificate, note_hash, generator_hash)
artifact_mutations = independent_artifact_mutations(certificate, note_hash, generator_hash)
report_checks = report_validation(report_body, certificate_hash, note_hash, generator_hash)

pass = (
  independent_checks.all? { |row| row.fetch("pass") } &&
  structure.all? { |row| row.fetch("pass") } &&
  source_mutations.fetch("pass") &&
  producer_errors.empty? &&
  artifact_mutations.fetch("pass") &&
  report_checks.all? { |row| row.fetch("pass") }
)

output = {
  "schema" => "r074s-defect-relaxed-total-rayleigh-independent-audit-v1",
  "source" => {
    "note" => EXPECTED_NOTE_FIELD,
    "note_sha256" => note_hash,
    "primary_generator" => EXPECTED_GENERATOR_FIELD,
    "primary_generator_sha256" => generator_hash,
    "primary_certificate" => "research/r074s_defect_relaxed_total_rayleigh_certificate.json",
    "primary_certificate_sha256" => certificate_hash,
    "primary_report" => "research/r074s_defect_relaxed_total_rayleigh_certificate_report.md",
    "primary_report_sha256" => report_hash
  },
  "independent_checks" => independent_checks,
  "structural_checks" => structure,
  "source_mutations" => source_mutations,
  "primary_producer_errors" => producer_errors,
  "artifact_mutations" => artifact_mutations,
  "report_checks" => report_checks,
  "scope" => {
    "finite_and_algebraic_only" => true,
    "machine_proves_inherited_PDE_results" => false,
    "machine_proves_Portmanteau_or_Jordan_theorems" => false,
    "machine_proves_R211_or_R214" => false,
    "machine_proves_regularity_or_Clay" => false
  },
  "summary" => {
    "independent_checks_passed" => independent_checks.count { |row| row.fetch("pass") },
    "independent_checks_total" => independent_checks.length,
    "exact_rows_passed" => independent_checks[0].fetch("rows").count { |row| row.fetch("pass") },
    "exact_rows_total" => independent_checks[0].fetch("rows").length,
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
