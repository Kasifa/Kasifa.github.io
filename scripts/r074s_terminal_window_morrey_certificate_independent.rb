#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent standard-library verifier for R0.74S Step 12.
#
# The exact Rational and integer checks below are evaluated before any primary
# certificate artifact is inspected.  They verify finite best-N/layer-cake
# algebra, the common-window shallow/deep split, synchronized-spike and budget
# arithmetic, moving-cover and monotone-occupation fixtures, mixed-norm scale
# cancellation, and the abstract super-Gaussian tail filter.  They do not
# machine-prove absolute continuity for NSE flux primitives, the inherited PDE
# estimates, either universal open packing gate, the conditional Morrey
# hypothesis for the bare suitable-weak class, Q.12, Q.1, regularity, or the
# Navier--Stokes Millennium problem.

require "digest"
require "json"
require "open3"
require "rbconfig"

REPO = File.expand_path("..", __dir__)

def input_path(environment_key, relative)
  File.expand_path(ENV.fetch(environment_key, File.join(REPO, relative)))
end

NOTE_PATH = input_path(
  "R074S_WINDOW_NOTE",
  "research/r074s_terminal_window_morrey_packing.md"
)

ARTIFACT_SPECS = {
  "main_note" => {
    "environment" => "R074S_WINDOW_NOTE",
    "path" => "research/r074s_terminal_window_morrey_packing.md",
    "sha256" => "03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f"
  },
  "primary_generator" => {
    "environment" => "R074S_WINDOW_PRIMARY_GENERATOR",
    "path" => "scripts/r074s_terminal_window_morrey_certificate.py",
    "sha256" => "90529ecfd080d3554fc45b63f5734a86f8736834cd6a65365c03fc82fb927a5a"
  },
  "primary_json" => {
    "environment" => "R074S_WINDOW_PRIMARY_JSON",
    "path" => "research/r074s_terminal_window_morrey_certificate.json",
    "sha256" => "741cb443b35a447df112d8078b79150eb21d5de308c4835219e0aa54f5e5b9d6"
  },
  "primary_report" => {
    "environment" => "R074S_WINDOW_PRIMARY_REPORT",
    "path" => "research/r074s_terminal_window_morrey_certificate_report.md",
    "sha256" => "e9d5ebee782751b2cad17a4b7a78829ee7c4da6b6d7b828a9d5bb8faadba36ad"
  },
  "primary_audit" => {
    "environment" => "R074S_WINDOW_PRIMARY_AUDIT",
    "path" => "research/r074s_terminal_window_morrey_primary_audit.md",
    "sha256" => "77397f923a20cb51382031bc4a8da82944190d4273aca8c316864e053e4c9396"
  },
  "independent_audit" => {
    "environment" => "R074S_WINDOW_INDEPENDENT_AUDIT",
    "path" => "research/r074s_terminal_window_morrey_independent_audit.md",
    "sha256" => "148a75ca1ed9fdba3d8e0df3d1681f0e3fa4997df76960498faf64ffab9b9c95"
  }
}.freeze

DEPENDENCY_SPECS = {
  "R0.74P" => {
    "environment" => "R074S_WINDOW_DEP_R074P",
    "path" => "research/r074p_temporal_observable_triage.md",
    "sha256" => "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867"
  },
  "R0.74R-arbitrary" => {
    "environment" => "R074S_WINDOW_DEP_R074R_ARBITRARY",
    "path" => "research/r074r_arbitrary_clock_extraction_gate.md",
    "sha256" => "ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7"
  },
  "R0.74R-persistent" => {
    "environment" => "R074S_WINDOW_DEP_R074R_PERSISTENT",
    "path" => "research/r074r_persistent_lobe_cubic_packing.md",
    "sha256" => "e7f151048e85d95133f8c6414849c0fe9dc40cc48b7a12666b7e21496ddb99b5"
  },
  "R0.74S-step8" => {
    "environment" => "R074S_WINDOW_DEP_STEP8",
    "path" => "research/r074s_defect_relaxed_total_rayleigh_excess.md",
    "sha256" => "0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab"
  },
  "R0.74S-step11" => {
    "environment" => "R074S_WINDOW_DEP_STEP11",
    "path" => "research/r074s_shared_budget_terminal_trace_obstruction.md",
    "sha256" => "fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693"
  },
  "R0.74F-packet" => {
    "environment" => "R074S_WINDOW_DEP_R074F",
    "path" => "research/r074f_two_packet_survival.md",
    "sha256" => "0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb"
  }
}.freeze

SCHEMA = "r074s-terminal-window-morrey-independent-verifier-v1"
PLACEHOLDER = /\ASTEP12_[A-Z0-9_]+_SHA_PLACEHOLDER\z/
EXPECTED_TAGS = (273..306).map { |number| "S.#{number}" }.freeze
INTERNAL_NEGATIVE_PROBE = "R074S_WINDOW_INTERNAL_NEGATIVE_PROBE"

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
  yield lambda { |condition, message|
    counter["cases"] += 1
    assert_exact(condition, message)
  }
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

def subsets_of_size_at_most(length, budget)
  indices = (0...length).to_a
  maximum = [budget, length].min
  (0..maximum).flat_map { |size| indices.combination(size).to_a }
end

def exhaustive_best_tail(values, budget)
  raise ArgumentError, "best-N data and budget must be nonnegative" if
    budget.negative? || values.any?(&:negative?)

  subsets_of_size_at_most(values.length, budget).map do |deleted|
    lookup = deleted.to_h { |index| [index, true] }
    rational_sum(values.each_with_index.map do |value, index|
      lookup[index] ? nil : value
    end.compact)
  end.min || Rational(0, 1)
end

def sorted_best_tail(values, budget)
  rational_sum(values.sort.reverse.drop([budget, values.length].min))
end

def layer_cake_integral(values, budget)
  levels = values.select(&:positive?).uniq.sort
  previous = Rational(0, 1)
  levels.inject(Rational(0, 1)) do |total, level|
    multiplicity = values.count { |value| value >= level }
    contribution = (level - previous) * [multiplicity - budget, 0].max
    previous = level
    total + contribution
  end
end

def best_n_layer_cake_checks
  exact_group("best_N_and_layer_cake_finite_exhaustive") do |check|
    alphabet = [
      Rational(0, 1), Rational(1, 3), Rational(2, 3),
      Rational(1, 1), Rational(2, 1)
    ]
    (0..4).each do |length|
      alphabet.repeated_permutation(length) do |values|
        (0..(length + 1)).each do |budget|
          brute = exhaustive_best_tail(values, budget)
          sorted = sorted_best_tail(values, budget)
          layer_cake = layer_cake_integral(values, budget)
          check.call(brute == sorted, "top-N deletion formula failed")
          check.call(brute == layer_cake, "finite layer-cake identity failed")
        end
      end
    end
  end
end

def best_n_l1_lipschitz_checks
  exact_group("best_N_l1_Lipschitz_finite_exhaustive") do |check|
    alphabet = [Rational(0, 1), Rational(1, 2), Rational(1, 1), Rational(2, 1)]
    vectors = alphabet.repeated_permutation(3).to_a
    vectors.each do |left|
      vectors.each do |right|
        distance = rational_sum(left.zip(right).map { |a, b| (a - b).abs })
        (0..4).each do |budget|
          gap = (sorted_best_tail(left, budget) -
                 sorted_best_tail(right, budget)).abs
          check.call(gap <= distance, "best-N map exceeded its l1 distance")
        end
      end
    end
  end
end

def common_window_split_checks
  exact_group("common_window_shallow_deep_split") do |check|
    # A row is [residual, common-window majorant, shallow?].
    states = [
      [Rational(0, 1), Rational(0, 1), true],
      [Rational(1, 3), Rational(1, 3), true],
      [Rational(1, 3), Rational(2, 3), true],
      [Rational(1, 1), Rational(2, 1), true],
      [Rational(1, 4), Rational(0, 1), false],
      [Rational(2, 1), Rational(0, 1), false]
    ]
    states.repeated_permutation(4) do |rows|
      residual = rows.map(&:first)
      window = rows.map { |row| row[1] }
      deep_debt = rational_sum(rows.map { |row| row[2] ? nil : row[0] }.compact)
      (0..5).each do |budget|
        check.call(
          sorted_best_tail(residual, budget) <=
            sorted_best_tail(window, budget) + deep_debt,
          "best-N shallow/deep split failed"
        )
        subsets_of_size_at_most(rows.length, budget).each do |deleted|
          lookup = deleted.to_h { |index| [index, true] }
          kept_residual = rational_sum(residual.each_with_index.map do |value, index|
            lookup[index] ? nil : value
          end.compact)
          kept_window = rational_sum(window.each_with_index.map do |value, index|
            lookup[index] ? nil : value
          end.compact)
          check.call(
            kept_residual <= kept_window + deep_debt,
            "same-deletion-set shallow/deep domination failed"
          )
        end
      end
    end

    # Literal interval arithmetic for d<=delta and rational-cube checks for
    # delta^(-2/3).
    interval_rows = [
      [Rational(1), Rational(0), Rational(3, 4), Rational(1, 4)],
      [Rational(2), Rational(-1), Rational(1), Rational(1)],
      [Rational(7, 3), Rational(1, 3), Rational(8, 5), Rational(3, 2)]
    ]
    interval_rows.each do |tau, start, delta, duration|
      last_exit = tau - duration
      window_left = [start, tau - delta].max
      check.call(duration <= delta, "fixture does not satisfy d<=delta")
      check.call(last_exit >= window_left, "last-exit interval leaves common window")
    end
    [Rational(1, 2), Rational(1, 1), Rational(3, 2)].each do |root|
      delta = root**3
      next unless delta.positive? && delta < 4

      inverse_two_thirds = root**-2
      check.call(inverse_two_thirds**3 * delta**2 == 1,
                 "exact rational-cube inverse-two-thirds identity failed")
    end
  end
end

def synchronized_spike_checks
  exact_group("synchronized_spike_exact_scaling") do |check|
    (1..3).each do |cube_root_m|
      shell_count = cube_root_m**3
      budget = shell_count - 1
      previous_ratio = nil
      [1, 2, 5, 11].each do |cube_root_h|
        height = Rational(cube_root_h**3, 1)
        epsilon = Rational(1, 97)
        r_squared = Rational(9, 4)
        amplitude = height / (epsilon * r_squared)
        one_integral = amplitude * epsilon * r_squared
        vector = Array.new(shell_count, height)
        total = rational_sum(vector)
        # The exhaustive length-at-most-four group has already certified the
        # sorted formula independently; avoid a pointless 2^M enumeration for
        # the M=27 flat vector here.
        tail = sorted_best_tail(vector, budget)
        normalized_ratio = Rational(cube_root_h, cube_root_m**2)
        check.call(one_integral == height, "single spike integral is wrong")
        check.call(total == shell_count * height, "total spike variation is wrong")
        check.call(tail == height, "N=M-1 spike tail is wrong")
        check.call(
          tail**3 == normalized_ratio**3 * total**2,
          "rationalized H/(MH)^(2/3) identity failed"
        )
        check.call(
          previous_ratio.nil? || normalized_ratio > previous_ratio,
          "normalized ratio did not grow with spike height"
        )
        previous_ratio = normalized_ratio
      end
    end
  end
end

def minimum_cap_checks
  exact_group("conditional_minimum_cap_two_regimes") do |check|
    roots = [
      Rational(1, 5), Rational(1, 2), Rational(1),
      Rational(3, 2), Rational(2), Rational(5)
    ]
    constants = [Rational(1, 3), Rational(1), Rational(7, 2), Rational(9)]
    saw_small = false
    saw_large = false
    roots.product(constants, constants).each do |root, c_zero, finite_cap|
      payment = root**3
      quadratic_scale = root**2
      left = [c_zero * payment, finite_cap].min
      right = [c_zero, finite_cap].max * quadratic_scale
      saw_small ||= payment <= 1
      saw_large ||= payment >= 1
      check.call(left <= right, "min(C0 P,B) cap failed")
      if payment <= 1
        check.call(payment <= quadratic_scale, "small-payment power comparison failed")
      else
        check.call(Rational(1) <= quadratic_scale, "large-payment power comparison failed")
      end
    end
    check.call(saw_small && saw_large, "both payment regimes were not exercised")
  end
end

def exception_budget_checks
  exact_group("exception_budget_union_finite_exhaustive") do |check|
    alphabet = [Rational(0), Rational(1), Rational(2)]
    vectors = alphabet.repeated_permutation(3).to_a
    vectors.each do |defect|
      vectors.each do |high_rayleigh|
        combined = defect.zip(high_rayleigh).map { |a, b| a + b }
        (0..3).each do |defect_budget|
          (0..3).each do |high_budget|
            left = sorted_best_tail(combined, defect_budget + high_budget)
            right = sorted_best_tail(defect, defect_budget) +
                    sorted_best_tail(high_rayleigh, high_budget)
            check.call(left <= right, "unioned exception budgets failed")
          end
        end
      end
    end
  end
end

def conditional_holder_checks
  exact_group("conditional_ancestor_charging_Holder") do |check|
    alphabet = [Rational(0), Rational(1), Rational(2)]
    equality_cases = 0
    alphabet.repeated_permutation(3) do |coefficients|
      alphabet.repeated_permutation(3) do |roots|
        left = rational_sum(coefficients.zip(roots).map { |c, root| c * root**2 })
        coefficient_cube = rational_sum(coefficients.map { |value| value**3 })
        payment = rational_sum(roots.map { |root| root**3 })
        equality_cases += 1 if left**3 == coefficient_cube * payment**2
        check.call(
          left**3 <= coefficient_cube * payment**2,
          "cubed shellwise Holder inequality failed"
        )
      end
    end
    check.call(equality_cases.positive?, "Holder equality cases were not exercised")
  end
end

def floor_fraction(value)
  value.numerator.div(value.denominator)
end

def moving_cover_checks
  exact_group("moving_tube_cover_integer_arithmetic") do |check|
    lengths = [
      Rational(0), Rational(1, 7), Rational(1), Rational(5, 2),
      Rational(8), Rational(65), Rational(511, 3)
    ]
    (1..9).each do |shell|
      radial_scale = 2**shell
      spatial_balls = 2**(3 * shell)
      lengths.each do |length|
        # Four normalized time triggers plus one initial piece, and at most
        # floor(L/2^k) path-variation triggers.
        pieces = 5 + floor_fraction(length / radial_scale)
        cylinder_count = pieces * spatial_balls
        sharp_row = 5 * 2**(3 * shell) + length * 2**(2 * shell)
        advertised_row = 5 * (2**(3 * shell) + length * 2**(2 * shell))
        check.call(pieces.positive?, "cover has no time piece")
        check.call(cylinder_count <= sharp_row, "greedy cover exceeds sharp row")
        check.call(sharp_row <= advertised_row, "sharp row exceeds advertised form")
      end
    end
  end
end

def mixed_norm_exponent_checks
  exact_group("mixed_norm_scale_exponents") do |check|
    exponent_pairs = [
      [3, 3], [4, 6], [6, 6], [nil, 3], [nil, 6], [12, 4]
    ]
    exponent_pairs.each do |q_value, r_value|
      inverse_q = q_value.nil? ? Rational(0) : Rational(1, q_value)
      inverse_r = Rational(1, r_value)
      theta = 3 * inverse_r + 2 * inverse_q
      energy = 3 - 2 * theta + 2 * (theta - 1)
      cubic = 4 - 3 * theta + 3 * (theta - 1)
      pressure = 4 - 3 * theta + (2 * theta - 2) + (theta - 1)
      path = -1 - 3 * inverse_r + 2 - 2 * inverse_q + theta - 1
      check.call(energy == 1, "energy R exponent does not reduce to one")
      check.call(cubic == 1, "cubic R exponent does not reduce to one")
      check.call(pressure == 1, "pressure R exponent does not reduce to one")
      check.call(path.zero?, "path-length R exponent does not cancel")
    end
  end
end

def no_winding_checks
  exact_group("S304_no_winding_exact_arithmetic") do |check|
    full_variation = Rational(65, 32)
    terminal_variation = Rational(4, 32)
    check.call(65 * Rational(1, 32) == full_variation,
               "full-interval variation arithmetic failed")
    check.call(full_variation < 3,
               "65/32 does not lie below the rational comparison 3")
    check.call(3 < 6,
               "rational comparison used with the standard pi>3 failed")
    check.call(4 * Rational(1, 32) == terminal_variation,
               "terminal-window variation arithmetic failed")
    check.call(terminal_variation == Rational(1, 8),
               "terminal-window variation is not one eighth")
  end
end

def occupation_checks
  exact_group("S305_monotone_occupation_normalized_fixtures") do |check|
    betas = [Rational(1, 4), Rational(1, 2), Rational(3, 4), Rational(1)]
    speed_bounds = [Rational(1), Rational(5, 2), Rational(7)]
    arcs = [Rational(1, 7), Rational(1, 3), Rational(3, 4), Rational(1)]
    remainders = [Rational(0), Rational(1, 9), Rational(1, 2), Rational(8, 9)]
    lower_equalities = 0
    upper_equalities = 0
    betas.product(speed_bounds, arcs, remainders, (0..4).to_a).each do |
      beta, speed_bound, arc, remainder, windings
    |
      slow = beta * speed_bound
      middle = (beta + 1) * speed_bound / 2
      fast = speed_bound
      speed_patterns = [
        [slow, slow], [middle, fast], [fast, fast], [fast, slow]
      ]
      speed_patterns.each do |full_speed, remainder_speed|
        remainder_in_arc = [remainder, arc].min
        occupation = windings * arc / full_speed +
                     remainder_in_arc / remainder_speed
        lower = windings * arc / speed_bound
        upper = (windings + 1) * arc / (beta * speed_bound)
        displacement = Rational(windings) + remainder
        check.call(floor_fraction(displacement) == windings,
                   "normalized winding count is wrong")
        check.call(slow <= full_speed && full_speed <= fast,
                   "full-cycle speed leaves allowed interval")
        check.call(slow <= remainder_speed && remainder_speed <= fast,
                   "remainder speed leaves allowed interval")
        check.call(lower <= occupation, "occupation violates lower bound")
        check.call(occupation <= upper, "occupation violates upper bound")
        lower_equalities += 1 if occupation == lower
        upper_equalities += 1 if occupation == upper
      end
    end
    check.call(lower_equalities.positive?, "lower endpoint was not attained")
    check.call(upper_equalities.positive?, "upper endpoint was not attained")
  end
end

def super_gaussian_checks
  exact_group("S306_super_Gaussian_best_N_filter") do |check|
    gammas = [Rational(1, 2), Rational(2, 3), Rational(3, 4)]
    heights = [Rational(0), Rational(1, 3), Rational(2)]
    gammas.product((0..4).to_a, heights).each do |gamma, power, height|
      budget = (0..8).find do |candidate|
        2**power * gamma**(3 * 4**candidate) < 1
      end
      check.call(!budget.nil?, "no finite q_N<1 was found")
      next if budget.nil?

      ratio_cap = 2**power * gamma**(3 * 4**budget)
      majorants = (0..(budget + 5)).map do |shell|
        height * 2**(power * shell) * gamma**(4**shell)
      end
      (budget...(majorants.length - 1)).each do |shell|
        exact_ratio = 2**power * gamma**(3 * 4**shell)
        check.call(majorants[shell + 1] == majorants[shell] * exact_ratio,
                   "adjacent super-Gaussian majorants disagree")
        check.call(exact_ratio <= ratio_cap,
                   "post-deletion adjacent ratio increased")
      end
      geometric_cap = majorants[budget] / (1 - ratio_cap)
      majorant_tail = rational_sum(majorants.drop(budget))
      check.call(majorant_tail <= geometric_cap,
                 "finite majorant tail exceeds geometric cap")

      multiplier_patterns = [
        Array.new(majorants.length, Rational(1)),
        majorants.each_index.map { |index| index.even? ? Rational(1) : Rational(1, 2) },
        majorants.each_index.map { |index| index < budget ? Rational(1) : Rational(1, 3) }
      ]
      multiplier_patterns.each do |multipliers|
        sequence = majorants.zip(multipliers).map { |value, factor| value * factor }
        chosen_tail = rational_sum(sequence.drop(budget))
        check.call(sorted_best_tail(sequence, budget) <= chosen_tail,
                   "deleting the first N entries did not upper-bound best-N")
        check.call(chosen_tail <= majorant_tail,
                   "dominated sequence exceeded its majorant tail")
        check.call(chosen_tail <= geometric_cap,
                   "dominated sequence exceeded S.306 cap")
      end
    end

    # For the inherited exponential weights, exp(x)>1+x turns the desired
    # ratio <1/2 into a fully rational sufficient threshold.
    (0..7).each do |power|
      threshold = Rational(2**(power + 1) - 1)
      first_shell = (1..32).find do |shell|
        Rational(3 * 4**(shell - 1), 32) >= threshold
      end
      check.call(!first_shell.nil?, "eventual geometric threshold not found")
      next if first_shell.nil?

      increment = Rational(3 * 4**(first_shell - 1), 32)
      previous = first_shell == 1 ? nil : Rational(3 * 4**(first_shell - 2), 32)
      check.call(increment >= threshold, "certified exponent increment is too small")
      check.call(previous.nil? || previous < threshold,
                 "reported shell is not the first sufficient one")
      check.call(Rational(1, 1) / (1 - Rational(1, 2)) == 2,
                 "geometric half-ratio multiplier is not two")
    end
  end
end

def compact(text)
  text.gsub(/\s+/, "")
end

PRIMARY_LINKS = [
  "https://doi.org/10.1002/cpa.3160350604",
  "https://arxiv.org/abs/2301.09603",
  "https://arxiv.org/abs/math/0607534",
  "https://arxiv.org/abs/math/0607537",
  "https://arxiv.org/abs/2111.14776",
  "https://doi.org/10.3934/dcdss.2013.6.1391"
].freeze

def semantic_note_checks(body)
  checks = []
  add = lambda do |identifier, condition|
    checks << { "id" => identifier, "pass" => !!condition }
  end

  tags = body.scan(/\\tag\{(S\.\d+)\}/).flatten
  add.call("exact_S273_S306_tag_sequence", tags == EXPECTED_TAGS)
  add.call("all_34_tags_unique", tags.uniq.length == EXPECTED_TAGS.length)

  compact_body = compact(body)
  compact_fragments = {
    "common_window_definition" =>
      'J_{\tau,\delta}&:=(\max\{s_R,\tau-\deltaR^2\},\tau)',
    "short_deep_reduction" =>
      '\mathcalS_N(r^{\rmsh}(\tau))\le\mathcalV^F_{N,R}(\tau,\delta)+C_{\rmdeep}\delta^{-2/3}A_R',
    "best_N_Lipschitz" =>
      '|\mathcalS_N(a)-\mathcalS_N(b)|&\le\|a-b\|_{\ell^1}',
    "layer_cake_identity" =>
      '\mathcalS_N(z)=\int_0^\infty\bigl(n_z(t)-N\bigr)_+\,dt',
    "exception_budget_sum" =>
      '\mathcalS_{N_D+N_H}(d^{\rmdef}+h)\le\mathcalS_{N_D}(d^{\rmdef})+\mathcalS_{N_H}(h)',
    "conditional_max_cap" =>
      '\mathcalS_0(x^{\rmsel}(\tau))\le\max\{C_0,B(M,L)\}A_R',
    "moving_tube_cover" =>
      'C_\psi\bigl(2^{3k}+L2^{2k}\bigr)',
    "path_exponent_zero" =>
      'R^{-1-3/r+2-2/q+\theta-1}=CM_*',
    "no_winding_full_interval" =>
      '\operatorname{Var}_{[0,65R^2]}Q\le{65\over32}<2\pi',
    "no_winding_terminal_window" =>
      '\operatorname{Var}_{I_{2R}}Q\le{1\over8}',
    "occupation_two_sided_bound" =>
      '{m|J|\overB}\le\tau_J\le{(m+1)|J|\over\betaB}',
    "super_Gaussian_ratio_condition" =>
      'q_N:=2^p\Gamma^{3\cdot4^N}<1',
    "super_Gaussian_tail_bound" =>
      '\mathcalS_N(z)\le\sum_{\ell\geN}z_\ell\le{H2^{pN}\Gamma^{4^N}\over1-q_N}'
  }
  compact_fragments.each do |identifier, fragment|
    add.call(identifier, compact_body.include?(compact(fragment)))
  end

  literal_fragments = {
    "fixed_solution_modulus_nonuniform" =>
      "The modulus in\n(S.277) depends on the solution and scale.",
    "window_gate_open" =>
      "\\textbf{OPEN: find fixed }N_F",
    "ancestor_gate_open" =>
      "\\textbf{OPEN:}\\quad",
    "combined_gate_open" =>
      "\\textbf{OPEN: find fixed }N_F,N_b",
    "abstract_tests_not_NSE" =>
      "ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES",
    "conditional_not_bare_class" =>
      "conditional benchmark, not a theorem for the bare suitable-weak class",
    "bounded_search_not_priority_proof" =>
      "The search is evidence against an immediate literature shortcut",
    "speed_screen_is_conditional" =>
      "This is deliberately a conditional mechanism screen.",
    "speed_alone_not_missing_ingredient" =>
      "rule out speed alone as the missing\ningredient",
    "no_DNS_used" =>
      "No DNS, floating-point asymptotics, or DGX computation is used."
  }
  literal_fragments.each do |identifier, fragment|
    add.call(identifier, body.include?(fragment))
  end

  PRIMARY_LINKS.each_with_index do |link, index|
    add.call("primary_link_#{index + 1}", body.include?(link))
  end
  add.call("three_open_boxes_present", body.scan(/\\textbf\{OPEN/).length >= 3)
  add.call("not_clay_repeated", body.scan(/\*\*NOT CLAY\.\*\*/).length >= 2)
  add.call("conditional_wording_repeated", body.scan(/conditional/i).length >= 5)
  add.call("display_math_balanced", body.scan(/\\\[/).length == body.scan(/\\\]/).length)
  checks
end

def note_structure_checks(body, bytes, artifact_row)
  return [{ "id" => "valid_UTF8", "pass" => false }] unless body.valid_encoding?

  checks = [{ "id" => "valid_UTF8", "pass" => true }]
  checks << {
    "id" => "main_note_hash_lock",
    "locked" => artifact_row.fetch("locked"),
    "pass" => artifact_row.fetch("pass")
  }
  checks.concat(semantic_note_checks(body))
  checks << {
    "id" => "no_tabs_or_trailing_whitespace",
    "pass" => !body.include?("\t") &&
      body.lines.none? { |line| line.sub(/\n\z/, "").match?(/[ \t]\z/) }
  }
  checks << {
    "id" => "LF_only_and_no_forbidden_controls",
    "pass" => !bytes.include?("\r") &&
      bytes.bytes.none? { |byte| byte < 32 && byte != 10 }
  }
  checks
end

def statement_negative_mutation_checks(body)
  exact_group("statement_negative_mutations_rejected") do |check|
    mutations = {
      "layer_cake_identity" => [
        '\\bigl(n_z(t)-N\\bigr)_+', '\\bigl(n_z(t)-N\\bigr)'
      ],
      "conditional_max_cap" => [
        '\\max\\{C_0,B(M,L)\\}', '\\min\\{C_0,B(M,L)\\}'
      ],
      "exception_budget_sum" => [
        'N_D+N_H', '\\max\\{N_D,N_H\\}'
      ],
      "three_open_boxes_present" => [
        '\\textbf{OPEN', '\\textbf{PROVED'
      ],
      "not_clay_repeated" => [
        '**NOT CLAY.**', '**CLAY.**'
      ],
      "primary_link_1" => [
        PRIMARY_LINKS.first, 'https://invalid.example/ckn'
      ],
      "no_winding_full_interval" => [
        '{65\\over32}', '{65\\over16}'
      ],
      "super_Gaussian_ratio_condition" => [
        'q_N:=2^p\\Gamma^{3\\cdot4^N}<1',
        'q_N:=2^p\\Gamma^{3\\cdot4^N}>1'
      ]
    }
    mutations.each do |expected_failure, (old, replacement)|
      mutated = body.gsub(old, replacement)
      results = semantic_note_checks(mutated).to_h { |row| [row.fetch("id"), row.fetch("pass")] }
      check.call(mutated != body, "mutation source marker was absent: #{expected_failure}")
      check.call(!results.fetch(expected_failure),
                 "semantic check accepted mutation: #{expected_failure}")
    end
  end
end

def artifact_checks
  ARTIFACT_SPECS.map do |label, spec|
    path = input_path(spec.fetch("environment"), spec.fetch("path"))
    expected = spec.fetch("sha256")
    locked = !PLACEHOLDER.match?(expected)
    actual = File.file?(path) ? sha256(path) : nil
    {
      "id" => label,
      "path" => spec.fetch("path"),
      "resolved_path" => path,
      "expected_sha256" => expected,
      "actual_sha256" => actual,
      "locked" => locked,
      "status" => locked ? (actual == expected ? "locked_match" : "locked_mismatch") :
        "placeholder_unlocked",
      "pass" => locked ? actual == expected : true
    }
  end
end

def dependency_checks
  DEPENDENCY_SPECS.map do |label, spec|
    path = input_path(spec.fetch("environment"), spec.fetch("path"))
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

def environment_override_negative_checks
  exact_group("environment_override_hash_mutation_rejected") do |check|
    target_label = "R0.74S-step11"
    target_spec = DEPENDENCY_SPECS.fetch(target_label)
    check.call(sha256(__FILE__) != target_spec.fetch("sha256"),
               "negative probe unexpectedly collides with dependency hash")

    overrides = { INTERNAL_NEGATIVE_PROBE => "1" }
    DEPENDENCY_SPECS.each_value do |spec|
      overrides[spec.fetch("environment")] = nil
    end
    overrides[target_spec.fetch("environment")] = File.expand_path(__FILE__)
    stdout, stderr, status = Open3.capture3(
      overrides,
      RbConfig.ruby,
      File.expand_path(__FILE__)
    )
    payload = JSON.parse(stdout)
    rows = payload.fetch("dependencies")
    target = rows.find { |row| row.fetch("id") == target_label }
    others = rows.reject { |row| row.fetch("id") == target_label }
    check.call(!status.success?, "mutated dependency override exited successfully")
    check.call(stderr.empty?, "negative override probe wrote unexpected stderr")
    check.call(!target.fetch("pass"), "mutated dependency hash was accepted")
    check.call(target.fetch("actual_sha256") == sha256(__FILE__),
               "environment override did not select the injected file")
    check.call(others.all? { |row| row.fetch("pass") },
               "negative probe disturbed an untargeted dependency")
  end
end

# A child process used by the environment-negative test stops here.  It checks
# only dependency paths and therefore cannot recursively invoke itself.
if ENV[INTERNAL_NEGATIVE_PROBE] == "1"
  probe_dependencies = dependency_checks
  puts JSON.generate({ "dependencies" => probe_dependencies })
  exit(probe_dependencies.all? { |row| row.fetch("pass") } ? 0 : 1)
end

# Independent mathematics runs before primary artifact hashes or contents are
# inspected, so the primary certificate cannot serve as an oracle.
independent_groups = [
  best_n_layer_cake_checks,
  best_n_l1_lipschitz_checks,
  common_window_split_checks,
  synchronized_spike_checks,
  minimum_cap_checks,
  exception_budget_checks,
  conditional_holder_checks,
  moving_cover_checks,
  mixed_norm_exponent_checks,
  no_winding_checks,
  occupation_checks,
  super_gaussian_checks
]

artifacts = artifact_checks
dependencies = dependency_checks
main_note_row = artifacts.find { |row| row.fetch("id") == "main_note" }
if File.file?(NOTE_PATH)
  note_bytes = File.binread(NOTE_PATH)
  note_body = note_bytes.dup.force_encoding(Encoding::UTF_8)
  note_checks = note_structure_checks(note_body, note_bytes, main_note_row)
  statement_mutations = statement_negative_mutation_checks(note_body)
else
  note_checks = [{ "id" => "main_note_exists", "pass" => false }]
  statement_mutations = {
    "id" => "statement_negative_mutations_rejected",
    "cases" => 0,
    "error" => "main note missing",
    "pass" => false
  }
end
environment_mutation = environment_override_negative_checks

pass = independent_groups.all? { |row| row.fetch("pass") } &&
       artifacts.all? { |row| row.fetch("pass") } &&
       dependencies.all? { |row| row.fetch("pass") } &&
       note_checks.all? { |row| row.fetch("pass") } &&
       statement_mutations.fetch("pass") &&
       environment_mutation.fetch("pass")

placeholders = artifacts.reject { |row| row.fetch("locked") }.map { |row| row.fetch("id") }

output = {
  "schema" => SCHEMA,
  "independent_checks" => independent_groups,
  "artifacts" => artifacts,
  "dependencies" => dependencies,
  "note_checks" => note_checks,
  "negative_mutation_checks" => [statement_mutations, environment_mutation],
  "scope" => {
    "standard_library_Ruby_only" => true,
    "exact_Rational_and_integer_checks_precede_primary_artifact_inspection" => true,
    "uses_floating_point_random_timestamp_network_or_gems" => false,
    "machine_proves_inherited_PDE_estimates" => false,
    "machine_proves_uniform_terminal_window_gate_S280" => false,
    "machine_proves_universal_ancestor_gate_S288" => false,
    "machine_proves_combined_gate_S303_Q12_or_Q1" => false,
    "machine_proves_Morrey_hypothesis_for_bare_suitable_weak_class" => false,
    "machine_proves_regularity_or_Clay" => false
  },
  "summary" => {
    "independent_groups_passed" => independent_groups.count { |row| row.fetch("pass") },
    "independent_groups_total" => independent_groups.length,
    "independent_cases" => independent_groups.sum { |row| row.fetch("cases") },
    "artifact_locks_passed" => artifacts.count { |row| row.fetch("locked") && row.fetch("pass") },
    "artifact_locks_total" => artifacts.count { |row| row.fetch("locked") },
    "dependency_locks_passed" => dependencies.count { |row| row.fetch("pass") },
    "dependency_locks_total" => dependencies.length,
    "note_checks_passed" => note_checks.count { |row| row.fetch("pass") },
    "note_checks_total" => note_checks.length,
    "negative_groups_passed" => [statement_mutations, environment_mutation].count do |row|
      row.fetch("pass")
    end,
    "negative_groups_total" => 2,
    "placeholder_artifacts" => placeholders
  },
  "release_ready" => placeholders.empty? && pass,
  "pass" => pass
}

puts JSON.pretty_generate(output)
exit(pass ? 0 : 1)
