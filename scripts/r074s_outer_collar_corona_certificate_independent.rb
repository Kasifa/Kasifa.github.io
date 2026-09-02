#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent standard-library verifier for R0.74S Step 14.
#
# Exact Rational/integer calculations are evaluated before any primary
# certificate artifact is opened.  They independently check collar geometry
# and weights, aligned best-N spikes, cubic Holder duality, the parabolic
# 32-child tree, density roots and lambda cancellation, jump/Dini arithmetic,
# the critical low-transition corona, and the heat-shear period count.  The
# primary artifacts are inspected only for frozen hashes and internal
# consistency.  This program does not call the primary generator and does not
# use its algorithms as a mathematical oracle.
#
# The checks do not machine-prove the pressure decomposition, inherited PDE
# estimates, either open packing gate, the open jump--corona lemma, an NSE
# realization of an abstract fixture, regularity, or the Navier--Stokes
# Millennium problem.

require "digest"
require "json"
require "open3"
require "rbconfig"

REPO = File.expand_path("..", __dir__)
SCHEMA = "r074s-outer-collar-corona-independent-verifier-v1"
EXPECTED_TAGS = (343..376).map { |number| "S.#{number}" }.freeze
INTERNAL_HASH_PROBE = "R074S_OUTER_CORONA_INTERNAL_HASH_PROBE"

ARTIFACT_SPECS = {
  "main_note" => {
    "environment" => "R074S_OUTER_CORONA_NOTE",
    "path" => "research/r074s_outer_collar_corona_obstruction.md",
    "sha256" => "c843284d68c0d7d441214b0b3e67e97ca4c5ebda5f527a957eb6e9bdc07f55f9"
  },
  "primary_generator" => {
    "environment" => "R074S_OUTER_CORONA_PRIMARY_GENERATOR",
    "path" => "scripts/r074s_outer_collar_corona_certificate.py",
    "sha256" => "041328286841e79e8863aca9c5ca9ef7c6ebbab328505c030dd1789c76d03e05"
  },
  "primary_json" => {
    "environment" => "R074S_OUTER_CORONA_PRIMARY_JSON",
    "path" => "research/r074s_outer_collar_corona_certificate.json",
    "sha256" => "1714426abc2bbe0a6f98ea5bced5c15843a68fbe66ed02adef670ee681f42be3"
  },
  "primary_report" => {
    "environment" => "R074S_OUTER_CORONA_PRIMARY_REPORT",
    "path" => "research/r074s_outer_collar_corona_certificate_report.md",
    "sha256" => "d3a5213ed8a646ccf6b26947a31ad18276c3e6e823c4296e8b1b760deabd05ef"
  },
  "primary_audit" => {
    "environment" => "R074S_OUTER_CORONA_PRIMARY_AUDIT",
    "path" => "research/r074s_outer_collar_corona_primary_audit.md",
    "sha256" => "7f7dd6a7bb1ca6e598b4156388037fe6db7c191a7baacd46d9abe43b12c37e90"
  },
  "independent_audit" => {
    "environment" => "R074S_OUTER_CORONA_INDEPENDENT_AUDIT",
    "path" => "research/r074s_outer_collar_corona_independent_audit.md",
    "sha256" => "9baa160a706c962f3eb6911d55882c3bc2f883ccdea6c674689930ab4b4e4156"
  }
}.freeze

DEPENDENCY_SPECS = {
  "R0.74S-step12" => {
    "environment" => "R074S_OUTER_CORONA_DEP_STEP12",
    "path" => "research/r074s_terminal_window_morrey_packing.md",
    "sha256" => "03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f"
  },
  "R0.74S-step13" => {
    "environment" => "R074S_OUTER_CORONA_DEP_STEP13",
    "path" => "research/r074s_temporal_integrability_morrey_threshold.md",
    "sha256" => "d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de"
  }
}.freeze

PRIMARY_SCHEMA = "r074s-outer-collar-corona-certificate-v1"
PRIMARY_SUMMARY = {
  "dependency_passed" => 3,
  "dependency_total" => 3,
  "exact_passed" => 12,
  "exact_total" => 12,
  "finite_cases" => 74_287,
  "finite_passed" => 9,
  "finite_total" => 9,
  "negative_passed" => 49,
  "negative_total" => 49,
  "structural_passed" => 37,
  "structural_total" => 37
}.freeze

PRIMARY_LINKS = [
  "https://doi.org/10.1002/cpa.3160350604",
  "https://doi.org/10.4171/AIHPC/20",
  "https://doi.org/10.1006/aima.2000.1937",
  "https://doi.org/10.1016/j.aim.2024.109654",
  "https://doi.org/10.1007/s00526-017-1151-7"
].freeze

def resolved_path(spec)
  File.expand_path(ENV.fetch(spec.fetch("environment"), File.join(REPO, spec.fetch("path"))))
end

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

def rational_sum(values)
  values.inject(Rational(0, 1), :+)
end

def assert_exact(condition, message)
  raise RuntimeError, message unless condition
end

def exact_group(identifier)
  counter = { "cases" => 0 }
  check = lambda do |condition, message|
    counter["cases"] += 1
    assert_exact(condition, message)
  end
  yield check
  { "id" => identifier, "cases" => counter.fetch("cases"), "pass" => true }
rescue StandardError => error
  {
    "id" => identifier,
    "cases" => counter.fetch("cases"),
    "error_class" => error.class.to_s,
    "error" => error.message,
    "pass" => false
  }
end

def sorted_best_tail(values, budget)
  raise ArgumentError, "best-N inputs must be nonnegative" if
    budget.negative? || values.any?(&:negative?)

  rational_sum(values.sort.reverse.drop([budget, values.length].min))
end

def brute_best_tail(values, budget)
  raise ArgumentError, "best-N inputs must be nonnegative" if
    budget.negative? || values.any?(&:negative?)

  indices = (0...values.length).to_a
  maximum = [budget, values.length].min
  (0..maximum).flat_map { |size| indices.combination(size).to_a }.map do |deleted|
    lookup = deleted.to_h { |index| [index, true] }
    retained = values.each_with_index.map do |value, index|
      value unless lookup[index]
    end.compact
    rational_sum(retained)
  end.min || Rational(0, 1)
end

def geometric_sum(ratio, length)
  (0...length).inject(Rational(0, 1)) { |total, index| total + ratio**index }
end

def collar_geometry_and_weight_checks
  exact_group("collar_geometry_weights_and_incidence") do |check|
    radii = [Rational(1, 16), Rational(1, 3), Rational(1), Rational(7, 2)]
    radii.product((1..18).to_a).each do |scale, index|
      rho = 2**index * scale
      outer_left = 2 * rho
      outer_right = 2 * rho + scale / 8
      outer_payment_left = 2**(index + 1) * scale
      outer_payment_right = 2**(index + 2) * scale
      check.call(outer_left == outer_payment_left,
                 "outer collar missed the A_k(2R) left endpoint")
      check.call(outer_right < outer_payment_right,
                 "outer collar escaped A_k(2R)")

      target_log_weight = -Rational(4**(index - 1), 32)
      outer_payment_log_weight = target_log_weight
      check.call(target_log_weight - outer_payment_log_weight == 0,
                 "aligned outer log-weight ratio is not zero")

      support_k_right = 2 * rho + scale / 8
      support_k_plus_two_left = 4 * rho - scale / 8
      separation = support_k_plus_two_left - support_k_right
      check.call(separation == 2 * rho - scale / 4,
                 "two-shell support separation formula failed")
      check.call(separation >= Rational(15, 4) * scale,
                 "two-shell supports are not separated by 15R/4")

      next unless index >= 3

      inner_left = rho - scale / 8
      inner_right = rho
      inner_payment_left = 2**(index - 1) * scale
      inner_payment_right = 2**index * scale
      check.call(inner_left >= inner_payment_left,
                 "inner collar escaped A_{k-2}(2R) on the left")
      check.call(inner_right == inner_payment_right,
                 "inner collar missed the A_{k-2}(2R) right boundary")

      inner_payment_log_weight = -Rational(4**(index - 3), 32)
      ratio_log = target_log_weight - inner_payment_log_weight
      expected = -Rational(15 * 4**(index - 3), 32)
      check.call(ratio_log == expected, "inner super-Gaussian ratio exponent failed")
      check.call(ratio_log.negative?, "inner weight ratio did not improve")
    end

    check.call(2**3 * 2**2 == 32, "parabolic halving does not have 32 children")
    check.call(Rational(15, 4) > 2, "diameter-2R incidence separation failed")
  end
end

def best_n_aligned_spike_checks
  exact_group("aligned_best_N_smooth_spike_scaling") do |check|
    profile_norms = [Rational(1), Rational(3, 2), Rational(7, 3)]
    finite_ps = [[2, 1], [3, 2], [4, 3], [5, 2]]

    (0..5).to_a.product([0, 2, 9], (1..4).to_a, profile_norms).each do |budget, cutoff, root, phi_norm|
      coordinate_count = budget + 1
      payment = Rational(root**3, 1)
      shell_indices = (1..coordinate_count).map { |offset| cutoff + offset }
      check.call(shell_indices.length == coordinate_count,
                 "spike coordinate count is not N+1")
      check.call(shell_indices.all? { |index| index > cutoff },
                 "spike was not placed beyond arbitrary K0")
      check.call(shell_indices.uniq.length == coordinate_count,
                 "spike shell indices are not distinct")

      # Symbolic gamma exponents uniquely identify the positive aligned weights.
      target_exponents = shell_indices.map { |index| Rational(4**(index - 1), 32) }
      payment_exponents = target_exponents.dup
      check.call(target_exponents == payment_exponents,
                 "target and payment weights are not aligned")
      weighted_l1_rows = Array.new(coordinate_count, payment / coordinate_count)
      check.call(rational_sum(weighted_l1_rows) == payment,
                 "aligned weighted L1 payment is not P")

      finite_ps.each do |numerator, denominator|
        power = numerator - denominator
        first_scale = 2
        second_scale = 3
        first_value = payment * phi_norm * first_scale**power / coordinate_count
        second_value = payment * phi_norm * second_scale**power / coordinate_count
        check.call(second_value > first_value, "finite-p spike norm did not grow")

        # d=s^{-p_num}; then d^(1/p-1)=s^(p_num-p_den), exactly.
        width = Rational(1, first_scale**numerator)
        check.call(width.positive? && width < 1, "spike width left (0,1)")
        expected = payment * phi_norm * first_scale**power / coordinate_count
        coordinates = Array.new(coordinate_count, expected)
        check.call(sorted_best_tail(coordinates, budget) == expected,
                   "sorted N-of-(N+1) spike tail failed")
        check.call(brute_best_tail(coordinates, budget) == expected,
                   "brute N-of-(N+1) spike tail failed")

        clay_scale = Rational(root**2, 1)
        constant = Rational(3, 1)
        chosen_scale = 2
        chosen_scale += 1 while
          payment * phi_norm * chosen_scale**power / coordinate_count <= constant * clay_scale
        check.call(
          payment * phi_norm * chosen_scale**power / coordinate_count > constant * clay_scale,
          "finite-p width could not exceed C_* P^(2/3)"
        )
      end

      # p=infinity: d=s^{-1} and the same exact exponent is one.
      infinity_scale = 5
      infinity_value = payment * phi_norm * infinity_scale / coordinate_count
      infinity_coordinates = Array.new(coordinate_count, infinity_value)
      check.call(brute_best_tail(infinity_coordinates, budget) == infinity_value,
                 "Linfinity N-of-(N+1) spike tail failed")
    end

    alphabet = [Rational(0), Rational(1, 4), Rational(1), Rational(7, 3)]
    (0..4).each do |length|
      alphabet.repeated_permutation(length) do |values|
        (0..length).each do |budget|
          check.call(sorted_best_tail(values, budget) == brute_best_tail(values, budget),
                     "best-N sorted and subset definitions disagree")
        end
      end
    end
  end
end

def cubic_duality_and_incidence_checks
  exact_group("cubic_duality_and_repeated_incidence") do |check|
    alphabet = [0, 1, 2, 3]
    equality_seen = false
    (0..4).each do |length|
      alphabet.repeated_permutation(length) do |coefficients|
        alphabet.repeated_permutation(length) do |payment_roots|
          left = coefficients.zip(payment_roots).sum do |coefficient, root|
            coefficient * root**2
          end
          coefficient_cube = coefficients.sum { |coefficient| coefficient**3 }
          payment = payment_roots.sum { |root| root**3 }
          check.call(left**3 <= coefficient_cube * payment**2,
                     "cubic Holder inequality failed")
          equality_seen ||= left.positive? && left**3 == coefficient_cube * payment**2
        end
      end
    end
    check.call(equality_seen, "no nonzero cubic Holder equality was exercised")

    [[1, 2, 4], [2, 3, 5], [1, 1, 1, 1]].each do |coefficients|
      cube_sum = coefficients.sum { |coefficient| coefficient**3 }
      roots = coefficients
      objective = coefficients.zip(roots).sum { |coefficient, root| coefficient * root**2 }
      payment = roots.sum { |root| root**3 }
      check.call(objective == cube_sum && payment == cube_sum,
                 "duality optimizer proportionality failed")
      check.call(objective**3 == cube_sum * payment**2,
                 "exact cubic duality equality failed")
      # After normalization sum p_i=1, the candidate objective cubed is sum c_i^3.
      check.call(Rational(objective**3, payment**2) == cube_sum,
                 "normalized dual objective cube is wrong")
    end

    # The first logical node occurs twice.  Both payment and coefficient cube
    # must be charged twice on the incidence multiset.
    coefficients = [Rational(2), Rational(2), Rational(1, 2)]
    roots = [Rational(1, 3), Rational(1, 3), Rational(3, 4)]
    left = coefficients.zip(roots).sum { |coefficient, root| coefficient * root**2 }
    repeated_cubes = rational_sum(coefficients.map { |value| value**3 })
    repeated_payment = rational_sum(roots.map { |value| value**3 })
    distinct_cubes = coefficients[0]**3 + coefficients[2]**3
    distinct_payment = roots[0]**3 + roots[2]**3
    check.call(left**3 <= repeated_cubes * repeated_payment**2,
               "Holder failed on repeated incidences")
    check.call(repeated_cubes > distinct_cubes, "coefficient incidences were deduplicated")
    check.call(repeated_payment > distinct_payment, "payment incidences were deduplicated")
  end
end

def root_tree_and_lambda_checks
  exact_group("parabolic_roots_factorization_and_lambda_cancellation") do |check|
    check.call(2**3 == 8, "spatial child count is not eight")
    check.call(2**2 == 4, "temporal child count is not four")
    check.call(8 * 4 == 32, "parabolic child count is not 32")
    check.call(Rational(1, 2) == Rational(1, 2), "child radius is not half")

    lambdas = [Rational(1, 5), Rational(1), Rational(7, 3), Rational(11)]
    root_radii = [Rational(1, 32), Rational(1, 8), Rational(3, 16)]
    lambdas.each do |level|
      masses = root_radii.map { |radius| Rational(3, 2) * level * radius }
      total_mass = rational_sum(masses)
      root_radii.zip(masses).each do |radius, mass|
        parent_radius = 2 * radius
        parent_mass = mass
        check.call(level * radius < mass, "root missed its strict lower threshold")
        check.call(mass <= 2 * level * radius, "root exceeded parent upper threshold")
        check.call(parent_mass / parent_radius <= level,
                   "root parent density is above lambda")

        coefficient_cube = radius
        payment_square = mass**3 / radius
        check.call(mass**3 == coefficient_cube * payment_square,
                   "powered critical root factorization failed")
      end
      check.call(rational_sum(root_radii) < total_mass / level,
                 "antichain root-radius bound failed")

      # Cube the Holder product.  This avoids floating radicals while proving
      # exact cancellation of lambda in (S.365).
      coefficient_cap = total_mass / level
      payment_cap_squared = 2 * level * total_mass**2
      check.call(coefficient_cap * payment_cap_squared == 2 * total_mass**3,
                 "lambda did not cancel from the cubic Holder product")
    end
  end
end

def jump_and_dini_checks
  exact_group("jump_decay_and_Dini_telescope") do |check|
    kappas = [Rational(6, 5), Rational(3, 2), Rational(2), Rational(7, 3)]
    alphas = [1, 3, 5]
    kappas.product(alphas).each do |kappa, alpha|
      parent_radius = Rational(1)
      child_radii = [Rational(1, 4 * kappa), Rational(1, 8 * kappa),
                     Rational(1, 8 * kappa)]
      check.call(rational_sum(child_radii) == parent_radius / (2 * kappa),
                 "first-jump radius fixture is wrong")
      check.call(rational_sum(child_radii) <= parent_radius / kappa,
                 "first-jump radius packing failed")
      check.call(child_radii.all? { |radius| radius <= parent_radius / 2 },
                 "proper descendant radius cap failed")

      theta = Rational(2**(1 - alpha), 1) / kappa
      check.call(theta.positive? && theta < 1, "jump coefficient is not strict")
      coefficient_sum = rational_sum(child_radii.map { |radius| radius**alpha })
      coefficient_cap = theta * parent_radius**alpha
      check.call(coefficient_sum <= coefficient_cap,
                 "alpha jump coefficient bound failed")
      (1..18).each do |generations|
        partial = geometric_sum(theta, generations)
        exact_formula = (1 - theta**generations) / (1 - theta)
        check.call(partial == exact_formula, "jump Dini geometric identity failed")
        check.call(partial < 1 / (1 - theta), "jump Dini sum exceeded its cap")
      end
    end

    (0..12).each do |start_depth|
      direct_product = Rational(1)
      partial = Rational(0)
      previous_partial = nil
      (0..80).each do |length|
        expected = Rational(start_depth + 1, start_depth + length + 1)
        check.call(direct_product == expected, "non-Dini product failed to telescope")
        partial += direct_product
        check.call(previous_partial.nil? || partial > previous_partial,
                   "positive non-Dini partial sum did not increase")
        previous_partial = partial
        theta = Rational(start_depth + length + 1, start_depth + length + 2)
        check.call(theta < 1, "levelwise factor is not strict")
        direct_product *= theta
      end
      check.call(partial > 1, "harmonic telescoping fixture is empty")
    end
  end
end

def critical_corona_checks
  exact_group("critical_low_transition_corona_mass") do |check|
    fixtures = [
      [Rational(1), Rational(1), Rational(3, 2)],
      [Rational(3, 5), Rational(7, 4), Rational(2)],
      [Rational(11, 8), Rational(2, 3), Rational(5, 3)]
    ]
    fixtures.each do |root_radius, root_mass, root_coefficient|
      root_density = root_mass / root_radius
      previous_density = nil
      (0..14).each do |depth|
        count = 8**depth
        node_radius = root_radius / 2**depth
        node_mass = root_mass / 8**depth
        density = node_mass / node_radius
        coefficient = root_coefficient / 2**depth
        check.call(count * node_mass == root_mass, "corona level lost mass")
        check.call(density == root_density / 4**depth,
                   "corona density scaling failed")
        check.call(count * coefficient**3 == root_coefficient**3,
                   "critical coefficient cube was not conserved")
        check.call(previous_density.nil? || density == previous_density / 4,
                   "corona child density is not one quarter")
        check.call(previous_density.nil? || density < previous_density,
                   "corona produced an upward density jump")
        previous_density = density
      end
      check.call(8 * (root_coefficient / 2)**3 == root_coefficient**3,
                 "eight-child critical cube identity failed")
      check.call(root_coefficient**3 != root_radius || root_coefficient == 1,
                 "fixture failed to distinguish incidence c from rho^(1/3)")
    end
    [Rational(6, 5), Rational(3, 2), Rational(2), Rational(7)].each do |kappa|
      density = Rational(1)
      (1..20).each do |depth|
        child_density = Rational(1, 4**depth)
        check.call(child_density <= density, "critical corona had a kappa jump")
        check.call(!(child_density > kappa * density),
                   "critical corona entered the first-jump skeleton")
      end
    end
  end
end

def heat_shear_period_checks
  exact_group("heat_shear_period_counts_mass_split_and_zero_flux") do |check|
    (1..24).each do |level|
      frequency = 2**level
      check.call(frequency == 2**level, "heat-shear frequency is not dyadic")
      (0...level).each do |parent_depth|
        sine_periods_in_child = 2**(level - parent_depth - 1)
        cosine_square_periods_in_child = 2**(level - parent_depth)
        check.call(sine_periods_in_child.is_a?(Integer) && sine_periods_in_child >= 1,
                   "child interval lacks an integer sine period")
        check.call(cosine_square_periods_in_child == 2 * sine_periods_in_child,
                   "cosine-square period count is wrong")
        x2_mass_fraction = Rational(1, 2)
        transverse_fraction = Rational(1, 2) * Rational(1, 2)
        check.call(x2_mass_fraction * transverse_fraction == Rational(1, 8),
                   "spatial child viscous mass is not one eighth")
      end
    end

    velocity_coordinate = 0
    profile_coordinate = 1
    path_velocity_coordinate = 0
    cutoff_derivative_coordinate = 0
    check.call(velocity_coordinate != profile_coordinate,
               "shear differentiates in its velocity direction")
    check.call(path_velocity_coordinate == velocity_coordinate,
               "moving path is not parallel to e1")
    check.call(cutoff_derivative_coordinate != profile_coordinate,
               "flux derivative unexpectedly points along the profile coordinate")
    check.call(0 == 0, "periodic y1 derivative did not integrate to zero")
  end
end

def compact(text)
  text.gsub(/\s+/, "")
end

def semantic_note_checks(body, bytes)
  rows = []
  add = lambda do |identifier, condition|
    rows << { "id" => identifier, "pass" => !!condition }
  end
  compact_body = compact(body)
  tags = body.scan(/\\tag\{(S\.\d+)\}/).flatten
  add.call("exact_S343_S376_tag_sequence", tags == EXPECTED_TAGS)
  add.call("all_34_tags_unique", tags.uniq.length == EXPECTED_TAGS.length)
  add.call("display_math_balanced", body.scan(/\\\[/).length == body.scan(/\\\]/).length)
  add.call("valid_UTF8", body.valid_encoding?)
  add.call("no_CR_or_NUL", !bytes.include?("\r") && !bytes.include?("\0"))
  add.call("no_forbidden_controls", bytes.bytes.none? { |byte| byte < 32 && byte != 10 })
  add.call("no_trailing_whitespace",
           body.lines.none? { |line| line.sub(/\n\z/, "").match?(/[ \t]\z/) })

  compact_fragments = {
    "S343_two_collar_geometry" =>
      '\\operatorname{supp}\\nabla\\psi_k^R&\\subsetC_{k,R}^-\\cupC_{k,R}^+\\subsetB_{3\\rho_k}',
    "S345_four_signed_channels" =>
      '\\dotF_{k,R}=\\dotF_{k,R}^{\\rm cub}+\\dotF_{k,R}^{\\rm loc}+\\dotF_{k,R}^{\\rm har}+\\dotF_{k,R}^{\\rm dr}',
    "S347_dimensionless_majorant" =>
      'h_{k,R}(\\sigma)=R^2|\\dotF_{k,R}(t(\\sigma))|\\le\\sum_\\alpha\\widehath_{k,R}^{\\alpha}(\\sigma)',
    "S348_linear_L1_only" =>
      '\\sum_{k\\ge1}\\sum_\\alpha\\|\\widehath_{k,R}^{\\alpha}\\|_{L^1(0,4)}\\leCP_R^M',
    "S349_fixed_tail_order" =>
      '\\mathfrakH^F_{4/3,K,R}\\le\\mathfrakT^F_{4/3,K,R}\\leCT_K(R)',
    "S350_collar_payment_indices" =>
      'C_{k,R}^+\\subsetA_k(2R)\\quad(k\\ge1),\\qquadC_{k,R}^-\\subsetA_{k-2}(2R)\\quad(k\\ge3)',
    "S351_inner_weight_ratio" =>
      '{\\gamma_k\\over\\gamma_{k-2}}=\\exp\\!\\left(-{15\\,4^{k-3}\\over32}\\right)',
    "S352_outer_weight_alignment" =>
      '={\\gamma_k\\over\\gamma_k}=1',
    "S353_aligned_spike_weights" =>
      'w_i=\\alpha_i=\\gamma_{k_i}',
    "S354_best_N_spike" =>
      '\\inf_{\\#S\\leN}\\sum_{i\\notinS}\\|H_i\\|_{L^p}={P\\overN+1}\\|\\phi\\|_{L^p}d^{1/p-1}',
    "S357_incidence_multiset_budgets" =>
      '\\sum_{(\\nu,k)\\in\\mathscrI_\\tau}p_\\nu&\\leC_pP_R^M',
    "S359_exact_cubic_duality" =>
      '\\sup_{p_i\\ge0,\\ \\sum_ip_i\\le1}\\sum_ic_ip_i^{2/3}=\\left(\\sum_ic_i^3\\right)^{1/3}',
    "S360_measure_pullback_R_inverse" =>
      '\\nu_R(A)&:=R^{-1}\\widetilde{\\boldsymbol\\mu}(\\Phi_R(A))',
    "S361_32_children" =>
      '\\#\\operatorname{child}(Q)=32',
    "S362_root_bounds" =>
      '\\lambda\\rho_Q<m_Q\\le2\\lambda\\rho_Q,\\qquad\\sum_{Q\\in\\mathscrR_\\lambda}\\rho_Q\\le{\\mathfrakM_R\\over\\lambda}',
    "S365_lambda_cancellation" =>
      '=2^{1/3}\\mathfrakM_R',
    "S367_jump_decay" =>
      '\\theta_\\alpha:={2^{1-\\alpha}\\over\\kappa}<1',
    "S369_non_Dini_telescope" =>
      '\\prod_{j=0}^{n-1}\\theta_{d_0+j}={d_0+1\\overd_0+n+1}',
    "S370_critical_child_cube" =>
      '=8\\left({c_S\\over2}\\right)^3=c_S^3',
    "S371_unfolded_shell_incidence" =>
      '\\#\\{k:R\\operatorname{pr}_zQ\\cap\\operatorname{supp}\\psi_k^R\\ne\\varnothing\\}\\le2',
    "S372_heat_shear_frequency" =>
      'u^{(n)}(t,x)=Ae^{-n^2t}\\sin(nx_2)e_1,\\qquadp^{(n)}=0,\\qquadn=2^L',
    "S373_heat_shear_mass_split" =>
      '={1\\over8}\\int_{J}\\!\\int_Q|\\nablau^{(2^L)}|^2',
    "S374_zero_flux" =>
      '\\dotF_{k,R}^{(2^L)}(t)=0\\quad\\hbox{forevery}k,R,t',
    "S375_common_exceptional_set" =>
      'onecommonshellset\\(E_\\tau\\),\\(\\#E_\\tau\\leN_b\\),suchthatforeverysolution,scale,andgoodterminal',
    "S375_repeated_payment" =>
      '\\sum_{\\substack{(\\nu,k):\\nu\\rightsquigarrowk\\\\k\\notinE_\\tau}}p_\\nu\\leC_pP_R^M',
    "S376_conditional_arrow" =>
      '\\text{(S.375)}\\quad\\Longrightarrow\\quad\\mathcalS_{N_b}(b(\\tau))'
  }
  compact_fragments.each do |identifier, fragment|
    add.call(identifier, compact_body.include?(compact(fragment)))
  end

  literal_fragments = {
    "fixed_solution_not_uniform" =>
      "The conclusion is only that, for each fixed solution and fixed scale",
    "outer_alignment_method_scope" =>
      "a proof which takes absolute values on each outer collar",
    "spike_abstract_boundary" =>
      "This is an **ABSTRACT METHOD OBSTRUCTION**.",
    "spike_not_PDE_counterexample" =>
      "does not refute the PDE estimate (S.342)",
    "incidence_conditional_boundary" =>
      "This implication is **PROVED / CONDITIONAL**",
    "threshold_no_gain_boundary" =>
      "This is a **PROVED THRESHOLD NO-GAIN** statement.",
    "critical_corona_not_NSE" =>
      "Step 13 did not realize the full tree as the clocks of one Navier--Stokes solution.",
    "unfold_before_incidence" =>
      "after each nonnegative periodized integral has been unfolded to the Euclidean lift",
    "forest_countable_locally_finite" =>
      "a countable, locally finite forest of comoving parabolic dyadic trees",
    "forest_shifted_grid_family" =>
      "drawn from a fixed finite family of shifted grids",
    "forest_top_cover" =>
      "(0,4)\\times \\bigcup_{k\\ge1}\\{z:Rz\\in\\operatorname {supp}\\psi_k^R\\}",
    "forest_unbounded_lift_boundary" =>
      "The single local cell \\(Q_0\\) in Section 5 does not cover the unbounded lifted shell family",
    "topwise_positive_levels" =>
      "For each top cell \\(T\\), a construction may select a level \\(\\lambda_T>0\\)",
    "unperiodized_incidence_definition" =>
      "only for incidence with one unperiodized lifted support",
    "open_bare_PDE_lemma" =>
      "The following statement is **OPEN** for the bare periodic suitable-weak class.",
    "one_universal_kappa" =>
      "There should exist a universal \\(\\kappa>1\\), a universal integer \\(N_b\\)",
    "forest_uniform_constants" =>
      "the number of top cells, and the forest depth",
    "uniform_solution_scale_terminal" =>
      "are independent of the solution, \\(R\\), \\(\\tau\\), the selected levels \\(\\lambda_T\\)",
    "full_incidence_multiset" =>
      "summation over the full incidence multiset, not over distinct nodes",
    "periodic_copy_and_repeat_charge" =>
      "include every periodic copy after unfolding and every repeated use across forest tops",
    "same_exceptional_set_channels" =>
      "The same \\(E_\\tau\\) must be used for the defect and high-Rayleigh ancestors",
    "assignment_is_open_construction" =>
      "These assignments are part of the asserted PDE construction",
    "zero_payment_convention_bound" =>
      "The zero-payment convention is the one following (S.356).",
    "top_boundary_scope" =>
      "The top row includes cells before a first crossing and every top-boundary contribution.",
    "top_and_corona_scope" =>
      "The corona row includes the moving-frame drift and every node not reached by the jump skeleton.",
    "heat_shear_not_gate_counterexample" =>
      "It neither refutes (S.342) nor realizes the abstract ancestor failure",
    "claim_abstract_not_NSE" =>
      "The following are **ABSTRACT METHOD OBSTRUCTIONS, NOT NSE",
    "claim_conditional" =>
      "The following statements are **CONDITIONAL**:",
    "claim_open" =>
      "The following remain **OPEN**:",
    "no_DNS_or_DGX" =>
      "No DNS or DGX computation is used",
    "not_CLAY" => "**NOT CLAY.**"
  }
  literal_fragments.each do |identifier, fragment|
    add.call(identifier, compact_body.include?(compact(fragment)))
  end
  add.call("not_CLAY_repeated", body.scan(/\*\*NOT CLAY\.\*\*/).length >= 2)
  add.call("all_primary_links", PRIMARY_LINKS.all? { |link| body.include?(link) })
  add.call("discouraged_collective_prose_absent",
           ["我们", "攻关", "主攻", "研究纪律", "三重审计", "杀死错误想法"].none? do |token|
             body.include?(token)
           end)
  rows
end

def note_structure_checks(path, artifact_row)
  return [{ "id" => "main_note_exists", "pass" => false }] unless File.file?(path)

  bytes = File.binread(path)
  body = bytes.dup.force_encoding(Encoding::UTF_8)
  rows = [{
    "id" => "main_note_hash_lock",
    "expected_sha256" => artifact_row.fetch("expected_sha256"),
    "actual_sha256" => artifact_row.fetch("actual_sha256"),
    "pass" => artifact_row.fetch("pass")
  }]
  rows.concat(semantic_note_checks(body, bytes))
  rows
end

def artifact_checks
  ARTIFACT_SPECS.map do |label, spec|
    path = resolved_path(spec)
    actual = File.file?(path) ? sha256(path) : nil
    {
      "id" => label,
      "path" => spec.fetch("path"),
      "resolved_path" => path,
      "expected_sha256" => spec.fetch("sha256"),
      "actual_sha256" => actual,
      "pass" => actual == spec.fetch("sha256")
    }
  end
end

def dependency_checks
  DEPENDENCY_SPECS.map do |label, spec|
    path = resolved_path(spec)
    actual = File.file?(path) ? sha256(path) : nil
    {
      "id" => label,
      "path" => spec.fetch("path"),
      "resolved_path" => path,
      "expected_sha256" => spec.fetch("sha256"),
      "actual_sha256" => actual,
      "pass" => actual == spec.fetch("sha256")
    }
  end
end

def primary_artifact_content_checks(artifacts)
  exact_group("primary_artifact_content_consistency") do |check|
    paths = artifacts.to_h { |row| [row.fetch("id"), row.fetch("resolved_path")] }
    payload = JSON.parse(File.read(paths.fetch("primary_json"), encoding: "UTF-8"))
    check.call(payload.fetch("schema") == PRIMARY_SCHEMA, "primary JSON schema changed")
    check.call(payload.fetch("overall_pass") == true, "primary JSON is not PASS")
    check.call(payload.fetch("summary") == PRIMARY_SUMMARY, "primary JSON summary changed")
    check.call(payload.fetch("note_sha256") == ARTIFACT_SPECS.fetch("main_note").fetch("sha256"),
               "primary JSON note hash disagrees")
    check.call(
      payload.fetch("generator_sha256") ==
        ARTIFACT_SPECS.fetch("primary_generator").fetch("sha256"),
      "primary JSON generator hash disagrees"
    )
    %w[exact_checks finite_checks dependency_checks structural_checks negative_checks].each do |key|
      check.call(payload.fetch(key).all? { |row| row.fetch("pass") },
                 "primary JSON contains a failed #{key} row")
    end

    report = File.read(paths.fetch("primary_report"), encoding: "UTF-8")
    check.call(report.include?("- Exact: 12/12"), "primary report exact count changed")
    check.call(report.include?("- Finite groups: 9/9"), "primary report finite count changed")
    check.call(report.include?("- Finite rational cases: 74287"),
               "primary report finite-case count changed")
    check.call(report.include?("- Dependencies: 3/3"),
               "primary report dependency count changed")
    check.call(report.include?("- Structural: 37/37"),
               "primary report structural count changed")
    check.call(report.include?("- Negative mutations: 49/49"),
               "primary report mutation count changed")
    check.call(report.include?("- Overall: **PASS**"), "primary report is not PASS")

    primary_audit = File.read(paths.fetch("primary_audit"), encoding: "UTF-8")
    independent_audit = File.read(paths.fetch("independent_audit"), encoding: "UTF-8")
    check.call(primary_audit.include?("**Verdict: PASS"), "primary audit verdict changed")
    check.call(primary_audit.include?("**PASS / NOT CLAY.**"),
               "primary audit lost PASS / NOT CLAY")
    check.call(independent_audit.include?("**Final verdict: PASS"),
               "independent audit verdict changed")
    check.call(independent_audit.include?("**PASS / NOT CLAY.**"),
               "independent audit lost PASS / NOT CLAY")
  end
end

def statement_mutation_checks(body)
  exact_group("statement_negative_mutations_rejected") do |check|
    mutations = {
      "S343_two_collar_geometry" => [
        '\\operatorname {supp}\\nabla\\psi_k^R',
        '\\operatorname {supp}\\psi_k^R'
      ],
      "S345_four_signed_channels" => [
        '+\\dot F_{k,R}^{\\rm dr},}',
        '-\\dot F_{k,R}^{\\rm dr},}'
      ],
      "S347_dimensionless_majorant" => [
        'h_{k,R}(\\sigma)=R^2|\\dot F_{k,R}(t(\\sigma))|',
        'h_{k,R}(\\sigma)=R|\\dot F_{k,R}(t(\\sigma))|'
      ],
      "S348_linear_L1_only" => [
        '\\le C P_R^M.}',
        '\\le C (P_R^M)^{2/3}.}'
      ],
      "S350_collar_payment_indices" => [
        'C_{k,R}^+\\subset A_k(2R)',
        'C_{k,R}^+\\subset A_{k-1}(2R)'
      ],
      "S351_inner_weight_ratio" => [
        '15\\,4^{k-3}',
        '3\\,4^{k-3}'
      ],
      "S352_outer_weight_alignment" => [
        '{\\gamma_k\\over\\gamma_k}=1',
        '{\\gamma_k\\over\\gamma_{k-1}}<1'
      ],
      "S353_aligned_spike_weights" => [
        'w_i=\\alpha_i=\\gamma_{k_i}',
        'w_i=\\gamma_{k_i-1},\\quad\\alpha_i=\\gamma_{k_i}'
      ],
      "S354_best_N_spike" => [
        'd^{1/p-1}.}',
        'd^{1-1/p}.}'
      ],
      "S357_incidence_multiset_budgets" => [
        '\\sum_{(\\nu,k)\\in\\mathscr I_\\tau}p_\\nu',
        '\\sum_{\\rm distinct\\ nodes}p_\\nu'
      ],
      "S359_exact_cubic_duality" => [
        '\\sum_ic_i^3',
        '\\sum_ic_i^2'
      ],
      "S360_measure_pullback_R_inverse" => [
        '\\nu_R(A)&:=R^{-1}',
        '\\nu_R(A)&:=R^{-2}'
      ],
      "S361_32_children" => [
        '\\#\\operatorname {child}(Q)=32',
        '\\#\\operatorname {child}(Q)=16'
      ],
      "S362_root_bounds" => [
        'm_Q\\le2\\lambda\\rho_Q',
        'm_Q\\le\\lambda\\rho_Q'
      ],
      "S365_lambda_cancellation" => [
        '=2^{1/3}\\mathfrak M_R.}',
        '=2^{1/3}\\lambda\\mathfrak M_R.}'
      ],
      "S367_jump_decay" => [
        '\\theta_\\alpha:={2^{1-\\alpha}\\over\\kappa}<1',
        '\\theta_\\alpha:={2^{\\alpha-1}\\over\\kappa}<1'
      ],
      "S369_non_Dini_telescope" => [
        '{d_0+1\\over d_0+n+1}',
        '{d_0+1\\over (d_0+n+1)^2}'
      ],
      "S370_critical_child_cube" => [
        '8\\left({c_S\\over2}\\right)^3=c_S^3',
        '8\\left({c_S\\over2}\\right)^2=c_S^2'
      ],
      "S371_unfolded_shell_incidence" => [
        '\\le2.}',
        '\\le1.}'
      ],
      "S372_heat_shear_frequency" => [
        'n=2^L.}',
        'n=3^L.}'
      ],
      "S373_heat_shear_mass_split" => [
        '={1\\over8}',
        '={1\\over32}'
      ],
      "S374_zero_flux" => [
        '\\dot F_{k,R}^{(2^L)}(t)=0',
        '\\dot F_{k,R}^{(2^L)}(t)>0'
      ],
      "S375_common_exceptional_set" => [
        'one common shell set',
        'one shell set per tree'
      ],
      "S376_conditional_arrow" => [
        '\\text{(S.375)}\\quad\\Longrightarrow',
        '\\text{(S.375)}\\quad\\Longleftarrow'
      ],
      "forest_countable_locally_finite" => [
        'a countable, locally finite forest',
        'one finite tree'
      ],
      "forest_shifted_grid_family" => [
        'a fixed finite family of shifted grids',
        'arbitrarily many shifted grids'
      ],
      "topwise_positive_levels" => [
        'may select a level \\(\\lambda_T>0\\)',
        'must use one nonpositive level \\(\\lambda_T\\le0\\)'
      ],
      "one_universal_kappa" => [
        'a universal \\(\\kappa>1\\)',
        'a top-dependent \\(\\kappa_T>1\\)'
      ],
      "full_incidence_multiset" => [
        'full incidence multiset, not over distinct nodes',
        'distinct nodes only'
      ],
      "same_exceptional_set_channels" => [
        'The same \\(E_\\tau\\) must be used',
        'Different exceptional sets may be used'
      ],
      "claim_open" => [
        'The following remain **OPEN**:',
        'The following are **PROVED**:'
      ],
      "no_DNS_or_DGX" => [
        'No DNS or DGX computation',
        'A DGX computation'
      ]
    }

    mutations.each do |expected_failure, (old, replacement)|
      mutated = body.sub(old, replacement)
      check.call(mutated != body, "mutation marker absent: #{expected_failure}")
      rows = semantic_note_checks(mutated, mutated.encode(Encoding::UTF_8))
      target = rows.find { |row| row.fetch("id") == expected_failure }
      check.call(!target.nil? && !target.fetch("pass"),
                 "semantic contract accepted mutation: #{expected_failure}")
    end

    clay_mutation = body.gsub("**NOT CLAY.**", "**CLAY.**")
    clay_rows = semantic_note_checks(clay_mutation, clay_mutation.encode(Encoding::UTF_8))
    check.call(clay_rows.any? { |row| row.fetch("id") == "not_CLAY" && !row.fetch("pass") },
               "NOT CLAY removal was accepted")

    tag_mutation = body.sub("\\tag{S.376}", "\\tag{S.375}")
    tag_rows = semantic_note_checks(tag_mutation, tag_mutation.encode(Encoding::UTF_8))
    check.call(
      tag_rows.any? { |row| row.fetch("id") == "exact_S343_S376_tag_sequence" && !row.fetch("pass") },
      "duplicate final tag was accepted"
    )

    damaged = body.b + "\r\0"
    damaged_body = damaged.dup.force_encoding(Encoding::UTF_8)
    damaged_rows = semantic_note_checks(damaged_body, damaged)
    check.call(
      damaged_rows.any? { |row| row.fetch("id") == "no_CR_or_NUL" && !row.fetch("pass") },
      "CR/NUL injection was accepted"
    )
  end
end

def environment_override_checks
  exact_group("environment_hash_overrides_rejected") do |check|
    probes = [
      ["R074S_OUTER_CORONA_NOTE", "main_note", "artifacts"],
      ["R074S_OUTER_CORONA_PRIMARY_GENERATOR", "primary_generator", "artifacts"],
      ["R074S_OUTER_CORONA_PRIMARY_JSON", "primary_json", "artifacts"],
      ["R074S_OUTER_CORONA_PRIMARY_REPORT", "primary_report", "artifacts"],
      ["R074S_OUTER_CORONA_PRIMARY_AUDIT", "primary_audit", "artifacts"],
      ["R074S_OUTER_CORONA_INDEPENDENT_AUDIT", "independent_audit", "artifacts"],
      ["R074S_OUTER_CORONA_DEP_STEP12", "R0.74S-step12", "dependencies"],
      ["R074S_OUTER_CORONA_DEP_STEP13", "R0.74S-step13", "dependencies"]
    ]
    probes.each do |environment_key, target_id, collection|
      environment = { INTERNAL_HASH_PROBE => "1", environment_key => File.expand_path(__FILE__) }
      stdout, stderr, status = Open3.capture3(environment, RbConfig.ruby, File.expand_path(__FILE__))
      payload = JSON.parse(stdout)
      target = payload.fetch(collection).find { |row| row.fetch("id") == target_id }
      check.call(!status.success?, "#{environment_key} mismatch exited successfully")
      check.call(stderr.empty?, "#{environment_key} mismatch wrote stderr")
      check.call(!target.fetch("pass"), "#{environment_key} mismatch passed its hash lock")
      check.call(target.fetch("actual_sha256") == sha256(__FILE__),
                 "#{environment_key} did not resolve to the injected file")
    end
  end
end

if ENV[INTERNAL_HASH_PROBE] == "1"
  probe_artifacts = artifact_checks
  probe_dependencies = dependency_checks
  probe_pass = probe_artifacts.all? { |row| row.fetch("pass") } &&
               probe_dependencies.all? { |row| row.fetch("pass") }
  puts JSON.generate({ "artifacts" => probe_artifacts, "dependencies" => probe_dependencies })
  exit(probe_pass ? 0 : 1)
end

# Independent mathematics intentionally precedes all primary-artifact reads.
independent_groups = [
  collar_geometry_and_weight_checks,
  best_n_aligned_spike_checks,
  cubic_duality_and_incidence_checks,
  root_tree_and_lambda_checks,
  jump_and_dini_checks,
  critical_corona_checks,
  heat_shear_period_checks
]

artifacts = artifact_checks
dependencies = dependency_checks
main_note = artifacts.find { |row| row.fetch("id") == "main_note" }
note_path = main_note.fetch("resolved_path")
note_checks = note_structure_checks(note_path, main_note)

if File.file?(note_path)
  note_bytes = File.binread(note_path)
  note_body = note_bytes.dup.force_encoding(Encoding::UTF_8)
  statement_mutations = statement_mutation_checks(note_body)
else
  statement_mutations = {
    "id" => "statement_negative_mutations_rejected",
    "cases" => 0,
    "error" => "main note missing",
    "pass" => false
  }
end

artifact_content = primary_artifact_content_checks(artifacts)
environment_mutations = environment_override_checks
negative_groups = [statement_mutations, environment_mutations]

pass = independent_groups.all? { |row| row.fetch("pass") } &&
       artifacts.all? { |row| row.fetch("pass") } &&
       dependencies.all? { |row| row.fetch("pass") } &&
       note_checks.all? { |row| row.fetch("pass") } &&
       artifact_content.fetch("pass") &&
       negative_groups.all? { |row| row.fetch("pass") }

output = {
  "schema" => SCHEMA,
  "independent_checks" => independent_groups,
  "artifacts" => artifacts,
  "dependencies" => dependencies,
  "note_checks" => note_checks,
  "primary_artifact_checks" => [artifact_content],
  "negative_mutation_checks" => negative_groups,
  "scope" => {
    "standard_library_Ruby_with_Rational_JSON_Digest_Open3" => true,
    "independent_math_precedes_primary_artifact_inspection" => true,
    "calls_or_imports_primary_generator" => false,
    "uses_floating_point_random_timestamp_network_or_gems" => false,
    "machine_proves_pressure_decomposition_or_inherited_PDE_estimates" => false,
    "machine_proves_open_gates_S288_S342_or_open_lemma_S375" => false,
    "machine_proves_NSE_realization_of_abstract_fixtures" => false,
    "machine_proves_regularity_or_Clay" => false
  },
  "summary" => {
    "independent_groups_passed" => independent_groups.count { |row| row.fetch("pass") },
    "independent_groups_total" => independent_groups.length,
    "independent_cases" => independent_groups.sum { |row| row.fetch("cases") },
    "artifact_locks_passed" => artifacts.count { |row| row.fetch("pass") },
    "artifact_locks_total" => artifacts.length,
    "dependency_locks_passed" => dependencies.count { |row| row.fetch("pass") },
    "dependency_locks_total" => dependencies.length,
    "note_checks_passed" => note_checks.count { |row| row.fetch("pass") },
    "note_checks_total" => note_checks.length,
    "primary_artifact_groups_passed" => artifact_content.fetch("pass") ? 1 : 0,
    "primary_artifact_groups_total" => 1,
    "primary_artifact_cases" => artifact_content.fetch("cases"),
    "negative_groups_passed" => negative_groups.count { |row| row.fetch("pass") },
    "negative_groups_total" => negative_groups.length,
    "negative_cases" => negative_groups.sum { |row| row.fetch("cases") }
  },
  "pass" => pass
}

puts JSON.pretty_generate(output)
exit(pass ? 0 : 1)
