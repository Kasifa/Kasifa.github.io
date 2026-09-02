#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent standard-library verifier for R0.74S Step 11.
#
# The exact Rational and finite exhaustive checks below are independent of any
# future primary certificate.  They verify only the discrete/algebraic content
# of the shared-budget, terminal-trace, scalar-excess, rational-clock, flat-
# tower, and exact-family falsification reductions.  They do not machine-prove
# the inherited PDE estimates, either open packing hypothesis, Q.12, Q.1,
# regularity, or the Navier--Stokes Millennium problem.

require "digest"
require "json"

REPO = File.expand_path("..", __dir__)

def input_path(environment_key, relative)
  File.expand_path(ENV.fetch(environment_key, File.join(REPO, relative)))
end

NOTE_PATH = input_path(
  "R074S_SHARED_BUDGET_NOTE",
  "research/r074s_shared_budget_terminal_trace_obstruction.md"
)

ARTIFACT_SPECS = {
  "main_note" => {
    "environment" => "R074S_SHARED_BUDGET_NOTE",
    "path" => "research/r074s_shared_budget_terminal_trace_obstruction.md",
    "sha256" => "fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693"
  },
  "primary_generator" => {
    "environment" => "R074S_SHARED_BUDGET_PRIMARY_GENERATOR",
    "path" => "scripts/r074s_shared_budget_terminal_trace_certificate.py",
    "sha256" => "a397d27943fca4d4a487038b5c14956667c7d36b3be5eb069262d2593f8ad2de"
  },
  "primary_json" => {
    "environment" => "R074S_SHARED_BUDGET_PRIMARY_JSON",
    "path" => "research/r074s_shared_budget_terminal_trace_certificate.json",
    "sha256" => "ea5c9f13ba412703995b2875a26c84fa20779457399ffa9117871b65fafaf8d0"
  },
  "primary_report" => {
    "environment" => "R074S_SHARED_BUDGET_PRIMARY_REPORT",
    "path" => "research/r074s_shared_budget_terminal_trace_certificate_report.md",
    "sha256" => "6e86813ab2b001a8f357af42d952a9104ba70859b32441148ad5cd3ab283ffc4"
  },
  "primary_audit" => {
    "environment" => "R074S_SHARED_BUDGET_PRIMARY_AUDIT",
    "path" => "research/r074s_shared_budget_terminal_trace_primary_audit.md",
    "sha256" => "d8bf38f4337af366cd450a50622f7105b8925db37cd87c09ce839fe129a058d5"
  },
  "independent_audit" => {
    "environment" => "R074S_SHARED_BUDGET_INDEPENDENT_AUDIT",
    "path" => "research/r074s_shared_budget_terminal_trace_independent_audit.md",
    "sha256" => "cfabe4b389c31b7ddeab755f51db8cf7daa88875add33621b0722b4487520f65"
  }
}.freeze

DEPENDENCY_SPECS = {
  "R0.74P" => {
    "environment" => "R074S_SHARED_BUDGET_DEP_R074P",
    "path" => "research/r074p_temporal_observable_triage.md",
    "sha256" => "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867"
  },
  "R0.74Q_problem_freeze" => {
    "environment" => "R074S_SHARED_BUDGET_DEP_R074Q_FREEZE",
    "path" => "research/r074q_problem_freeze.md",
    "sha256" => "42efa94f5310d8f7ce3cea1896ee1e0a8ddd9bddf5d588f9bb853c8696a1a962"
  },
  "R0.74Q_relaxed_multipacket" => {
    "environment" => "R074S_SHARED_BUDGET_DEP_R074Q_MULTIPACKET",
    "path" => "research/r074q_relaxed_multipacket_cubic_obstruction.md",
    "sha256" => "ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d"
  },
  "R0.74R_clock_gate" => {
    "environment" => "R074S_SHARED_BUDGET_DEP_R074R_CLOCK",
    "path" => "research/r074r_arbitrary_clock_extraction_gate.md",
    "sha256" => "ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7"
  },
  "R0.74R_persistent_lobe" => {
    "environment" => "R074S_SHARED_BUDGET_DEP_R074R_LOBE",
    "path" => "research/r074r_persistent_lobe_cubic_packing.md",
    "sha256" => "e7f151048e85d95133f8c6414849c0fe9dc40cc48b7a12666b7e21496ddb99b5"
  },
  "R0.74S_Step8" => {
    "environment" => "R074S_SHARED_BUDGET_DEP_STEP8",
    "path" => "research/r074s_defect_relaxed_total_rayleigh_excess.md",
    "sha256" => "0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab"
  },
  "R0.74S_Step10" => {
    "environment" => "R074S_SHARED_BUDGET_DEP_STEP10",
    "path" => "research/r074s_paid_branch_last_exit_residual.md",
    "sha256" => "9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c"
  }
}.freeze

SCHEMA = "r074s-shared-budget-terminal-trace-independent-verifier-v1"
PLACEHOLDER = /\ASTEP11_[A-Z0-9_]+_SHA_PLACEHOLDER\z/
EXPECTED_TAGS = (248..272).map { |number| "S.#{number}" }.freeze

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

def tuples(entries, length, prefix = [], &block)
  if prefix.length == length
    yield prefix
    return
  end

  entries.each { |entry| tuples(entries, length, prefix + [entry], &block) }
end

def subsets_of_size_at_most(length, budget)
  indices = (0...length).to_a
  maximum = [budget, length].min
  (0..maximum).flat_map { |size| indices.combination(size).to_a }
end

def exhaustive_best_tail(values, budget)
  subsets_of_size_at_most(values.length, budget).map do |deleted|
    deleted_lookup = deleted.to_h { |index| [index, true] }
    kept = []
    values.each_with_index do |value, index|
      kept << value unless deleted_lookup[index]
    end
    rational_sum(kept)
  end.min || Rational(0, 1)
end

def sorted_best_tail(values, budget)
  kept = values.sort.reverse.drop([budget, values.length].min)
  rational_sum(kept)
end

def shared_budget_checks
  exact_group("shared_budget_infimal_convolution") do |check|
    coordinate_pairs = [
      [0, 0], [1, 0], [2, 0], [0, 1], [0, 2]
    ].map { |left, right| [Rational(left, 1), Rational(right, 1)] }

    tuples(coordinate_pairs, 4) do |rows|
      left = rows.map(&:first)
      right = rows.map(&:last)
      total = left.zip(right).map { |a, b| a + b }
      (0..4).each do |budget|
        direct = exhaustive_best_tail(total, budget)
        convolution = (0..budget).map do |left_budget|
          exhaustive_best_tail(left, left_budget) +
            exhaustive_best_tail(right, budget - left_budget)
        end.min
        check.call(direct == convolution, "infimal convolution failed")
        check.call(direct == sorted_best_tail(total, budget), "top-N formula failed")
      end
    end

    magnitude = Rational(11, 1)
    left = [magnitude, 0]
    right = [0, magnitude]
    check.call(exhaustive_best_tail(left, 1).zero?, "left one-budget witness failed")
    check.call(exhaustive_best_tail(right, 1).zero?, "right one-budget witness failed")
    check.call(exhaustive_best_tail(left.zip(right).map { |a, b| a + b }, 1) == magnitude,
               "duplicated budget witness failed")
    check.call(exhaustive_best_tail(left.zip(right).map { |a, b| a + b }, 2).zero?,
               "summed budget witness failed")
  end
end

def sup_min_checks
  exact_group("terminal_supremum_and_budget_minimum") do |check|
    coordinate_pairs = [
      [0, 0], [1, 0], [2, 0], [0, 1], [0, 2]
    ].map { |left, right| [Rational(left, 1), Rational(right, 1)] }
    states = []
    tuples(coordinate_pairs, 3) do |rows|
      states << [rows.map(&:first), rows.map(&:last)]
    end

    states.each do |first|
      states.each do |second|
        terminals = [first, second]
        (0..2).each do |budget|
          pointwise_sup = terminals.map do |left, right|
            exhaustive_best_tail(left.zip(right).map { |a, b| a + b }, budget)
          end.max
          separated_sup = (0..budget).map do |left_budget|
            terminals.map { |left, _right| exhaustive_best_tail(left, left_budget) }.max +
              terminals.map { |_left, right| exhaustive_best_tail(right, budget - left_budget) }.max
          end.min
          check.call(pointwise_sup <= separated_sup, "sup-min inequality reversed")
        end
      end
    end

    magnitude = Rational(13, 1)
    terminals = [
      [[magnitude, 0], [0, 1]],
      [[1, 0], [0, magnitude]]
    ]
    adaptive = terminals.map do |left, right|
      exhaustive_best_tail(left.zip(right).map { |a, b| a + b }, 1)
    end.max
    frozen = (0..1).map do |left_budget|
      terminals.map { |left, _right| exhaustive_best_tail(left, left_budget) }.max +
        terminals.map { |_left, right| exhaustive_best_tail(right, 1 - left_budget) }.max
    end.min
    check.call(adaptive == 1, "adaptive terminal split witness failed")
    check.call(frozen == magnitude, "frozen terminal split witness failed")
    check.call(adaptive < frozen, "supremum unexpectedly commuted with minimum")
  end
end

def dyadic_bin(depth)
  raise ArgumentError, "depth must lie in (0,1)" unless depth.positive? && depth < 1

  index = 0
  loop do
    lower = Rational(1, 2**(index + 1))
    upper = Rational(1, 2**index)
    return index if lower <= depth && depth < upper

    index += 1
  end
end

def layer_cake_rhs(atoms)
  grouped = Hash.new(Rational(0, 1))
  atoms.each { |depth, weight| grouped[depth] += weight }
  depths = grouped.keys.sort
  cumulative = Rational(0, 1)
  twice_integral = Rational(0, 1)
  depths.each_with_index do |depth, index|
    cumulative += grouped.fetch(depth)
    next_depth = depths[index + 1] || Rational(1, 1)
    twice_integral += cumulative * (depth**-2 - next_depth**-2)
  end
  rational_sum(grouped.values) + twice_integral
end

def dyadic_and_layer_cake_checks
  exact_group("normalized_depth_dyadic_and_layer_cake") do |check|
    square_roots = [Rational(1, 2), Rational(1, 1), Rational(3, 2), Rational(2, 1)]
    durations = [Rational(1, 64), Rational(1, 20), Rational(1, 8), Rational(1, 3)]
    amplitudes = [Rational(1, 5), Rational(1, 1), Rational(7, 3)]
    square_roots.product(durations, amplitudes).each do |root, duration, amplitude|
      lambda_value = root**2
      depth = duration * root**3
      next unless depth.positive? && depth < 1

      weight = amplitude * lambda_value**3
      check.call(weight * depth**-2 == amplitude * duration**-2,
                 "normalized inverse-duration identity failed")
    end

    depths = [
      Rational(1, 2), Rational(3, 8), Rational(1, 4), Rational(1, 5),
      Rational(1, 8), Rational(1, 10), Rational(1, 16), Rational(3, 64)
    ]
    weight_choices = [Rational(1, 3), Rational(2, 1)]
    tuples(weight_choices, depths.length) do |weights|
      atoms = depths.zip(weights)
      exact_moment = atoms.inject(Rational(0, 1)) do |sum, (depth, weight)|
        sum + weight * depth**-2
      end
      dyadic_moment = atoms.inject(Rational(0, 1)) do |sum, (depth, weight)|
        sum + weight * 4**dyadic_bin(depth)
      end
      check.call(dyadic_moment <= exact_moment, "dyadic lower bound failed")
      check.call(exact_moment <= 4 * dyadic_moment, "dyadic upper bound failed")
      check.call(layer_cake_rhs(atoms) == exact_moment, "finite layer-cake identity failed")
    end

    (1..30).each do |atom_count|
      atoms = (1..atom_count).map do |index|
        depth = Rational(1, 2**index)
        [depth, depth**2]
      end
      moment = atoms.inject(Rational(0, 1)) do |sum, (depth, weight)|
        sum + weight * depth**-2
      end
      check.call(moment == atom_count, "critical endpoint moment is not the atom count")
      atoms.each do |depth, _weight|
        cumulative = atoms.select { |candidate, _| candidate <= depth }.sum do |_candidate, weight|
          weight
        end
        check.call(cumulative <= 2 * depth**2, "critical quadratic Carleson bound failed")
      end
    end
  end
end

def rx_comparison_checks
  exact_group("selected_excess_one_fifth_to_three") do |check|
    denominator = 60
    terminal = Rational(1, 1)
    (0..9).each do |beta_numerator|
      beta = Rational(beta_numerator, denominator)
      (0..10).each do |sigma_numerator|
        twice_lambda_sigma = Rational(sigma_numerator, denominator)
        (30..60).each do |dissipation_numerator|
          dissipation = Rational(dissipation_numerator, denominator)
          (-beta_numerator..beta_numerator).each do |q_numerator|
            q = Rational(q_numerator, denominator)
            excess = dissipation - beta - twice_lambda_sigma
            residual = Rational(1, 3) - q
            check.call(excess > terminal / 6, "selected excess lost the strict one-sixth margin")
            check.call(residual > terminal / 6 && residual < terminal / 2,
                       "residual lost the strict Step 10 interval")
            check.call(excess / 5 < residual, "one-fifth comparison failed")
            check.call(residual < 3 * excess, "factor-three comparison failed")
          end
        end
      end
    end

    # The two exact errors from the limiting constants are both 4 epsilon.
    (7..80).each do |integer|
      epsilon = Rational(1, integer)
      beta = Rational(1, 6) - epsilon
      next if beta.negative?

      lower_residual = Rational(1, 6) + epsilon
      lower_excess = Rational(5, 6) + epsilon
      check.call(5 * lower_residual - lower_excess == 4 * epsilon,
                 "one-fifth sharpness identity failed")

      upper_residual = Rational(1, 2) - epsilon
      upper_excess = Rational(1, 6) + epsilon
      check.call(3 * upper_excess - upper_residual == 4 * epsilon,
                 "factor-three sharpness identity failed")
    end

    sample_pairs = [
      [Rational(1, 3), Rational(1, 8)],
      [Rational(2, 5), Rational(1, 5)],
      [Rational(7, 10), Rational(1, 4)],
      [Rational(5, 6), Rational(1, 6) + Rational(1, 100)],
      [Rational(1, 6) + Rational(1, 100), Rational(1, 2) - Rational(1, 100)],
      [Rational(0, 1), Rational(0, 1)]
    ]
    tuples(sample_pairs, 4) do |pairs|
      excess_vector = pairs.map(&:first)
      residual_vector = pairs.map(&:last)
      next unless pairs.all? do |excess, residual|
        excess.zero? ? residual.zero? : excess / 5 <= residual && residual <= 3 * excess
      end

      (0..4).each do |budget|
        excess_tail = exhaustive_best_tail(excess_vector, budget)
        residual_tail = exhaustive_best_tail(residual_vector, budget)
        check.call(excess_tail / 5 <= residual_tail, "best-N one-fifth comparison failed")
        check.call(residual_tail <= 3 * excess_tail, "best-N factor-three comparison failed")
      end
    end
  end
end

def affine_integral(value_at_left, slope, length)
  value_at_left * length + slope * length**2 / 2
end

def h_value(time)
  case time
  when Rational(0, 1)..Rational(9, 10)
    Rational(0, 1)
  when Rational(9, 10)..Rational(1, 1)
    Rational(2, 3) * (time - Rational(9, 10))
  when Rational(1, 1)..Rational(39, 20)
    Rational(1, 15) + (time - 1) / 300
  when Rational(39, 20)..Rational(2, 1)
    Rational(419, 6000) + Rational(1981, 300) * (time - Rational(39, 20))
  else
    raise ArgumentError, "h fixture evaluated outside [0,2]"
  end
end

def defect_dissipation(time)
  return Rational(0, 1) if time <= Rational(1, 10)
  return Rational(6, 5) * (time - Rational(1, 10)) if time <= Rational(3, 5)

  Rational(3, 5)
end

def early_energy(time)
  return Rational(0, 1) unless time.between?(Rational(1, 10), Rational(3, 5))

  Rational(12, 125) * (time - Rational(1, 10)) * (Rational(3, 5) - time)
end

def high_rayleigh_dissipation(time)
  return Rational(0, 1) if time <= Rational(1, 10)
  return Rational(3, 5) if time >= Rational(3, 5)

  length = Rational(1, 2)
  position = time - Rational(1, 10)
  coefficient = Rational(12, 125)
  300 * coefficient * (length * position**2 / 2 - position**3 / 3)
end

def rational_clock_checks
  exact_group("two_rational_last_exit_localization_clocks") do |check|
    first_length = Rational(1, 10)
    second_length = Rational(19, 20)
    third_length = Rational(1, 20)
    sigma_h =
      affine_integral(0, Rational(2, 3), first_length) +
      affine_integral(Rational(1, 15), Rational(1, 300), second_length) +
      affine_integral(Rational(419, 6000), Rational(1981, 300), third_length)
    check.call(sigma_h == Rational(959, 12_000), "late kinetic integral is wrong")
    check.call(h_value(Rational(1, 1)) == Rational(1, 15), "h(1) is wrong")
    check.call(h_value(Rational(39, 20)) == Rational(419, 6000), "h(39/20) is wrong")
    check.call(h_value(Rational(2, 1)) == Rational(2, 5), "h(2) is wrong")

    defect_terminal = defect_dissipation(Rational(2, 1))
    defect_excess = defect_terminal - 2 * sigma_h
    check.call(defect_terminal == Rational(3, 5), "defect terminal mass is wrong")
    check.call(defect_terminal >= Rational(1, 2), "defect row is not D-dominated")
    check.call(sigma_h < Rational(1, 12), "defect row entered the kinetic paid branch")
    check.call(defect_excess == Rational(2641, 6000), "defect scalar excess is wrong")
    check.call(defect_excess > Rational(1, 6), "defect scalar excess lacks margin")
    check.call(defect_terminal >= Rational(1, 8), "defect ancestry threshold failed")
    check.call(defect_dissipation(2) - defect_dissipation(1) == 0,
               "defect was incorrectly localized after the last exit")

    support_length = Rational(1, 2)
    early_integral = Rational(12, 125) * support_length**3 / 6
    high_mass = 300 * early_integral
    sigma_high = sigma_h + early_integral
    high_excess = high_mass - 2 * sigma_high
    check.call(early_integral == Rational(1, 500), "early kinetic integral is wrong")
    check.call(high_mass == Rational(3, 5), "high-Rayleigh mass is wrong")
    check.call(high_mass >= Rational(1, 8), "high-Rayleigh ancestry threshold failed")
    check.call(sigma_high == Rational(983, 12_000), "high-Rayleigh kinetic mass is wrong")
    check.call(sigma_high < Rational(1, 12), "high-Rayleigh row entered kinetic payment")
    check.call(high_excess == Rational(2617, 6000), "high-Rayleigh scalar excess is wrong")
    check.call(high_excess > Rational(1, 6), "high-Rayleigh scalar excess lacks margin")

    # Exact rational sampling supplements the analytic monotonicity and support
    # bounds: before t=1 both clocks are at most 2/3, after t=1 both exceed it.
    (0..1200).each do |numerator|
      time = Rational(numerator, 600)
      defect_clock = defect_dissipation(time) + h_value(time)
      high_clock = high_rayleigh_dissipation(time) + early_energy(time) + h_value(time)
      if time < 1
        check.call(defect_clock < Rational(2, 3), "defect clock crossed before t=1")
        check.call(high_clock < Rational(2, 3), "high-Rayleigh clock crossed before t=1")
      elsif time == 1
        check.call(defect_clock == Rational(2, 3), "defect clock misses its last exit")
        check.call(high_clock == Rational(2, 3), "high-Rayleigh clock misses its last exit")
      else
        check.call(defect_clock > Rational(2, 3), "defect clock recrossed after t=1")
        check.call(high_clock > Rational(2, 3), "high-Rayleigh clock recrossed after t=1")
      end
    end

    defect_residual = (defect_dissipation(2) + h_value(2)) -
                      (defect_dissipation(1) + h_value(1))
    high_residual = (high_rayleigh_dissipation(2) + h_value(2)) -
                    (high_rayleigh_dissipation(1) + early_energy(1) + h_value(1))
    check.call(defect_residual == Rational(1, 3), "defect last-exit residual is wrong")
    check.call(high_residual == Rational(1, 3), "high-Rayleigh last-exit residual is wrong")
    check.call(high_rayleigh_dissipation(2) - high_rayleigh_dissipation(1) == 0,
               "high-Rayleigh mass was incorrectly localized after the last exit")
  end
end

def flat_tower_checks
  exact_group("pure_defect_flat_tower") do |check|
    (0..14).each do |shell_count|
      vector = Array.new(shell_count, Rational(1, 3))
      (0..16).each do |budget|
        expected = Rational([shell_count - budget, 0].max, 3)
        check.call(exhaustive_best_tail(vector, budget) == expected,
                   "finite flat-tower best-N tail failed")
      end
    end

    (2..12).each do |scale_integer|
      shell_count = scale_integer**6
      payment = Rational(shell_count, 1)
      quadratic_scale = Rational(scale_integer**4, 1)
      square_function = Rational(scale_integer**3, 1)
      check.call(quadratic_scale**3 == payment**2, "A=P^(2/3) identity failed")
      check.call(square_function**2 == shell_count, "Z=sqrt(M) identity failed")
      check.call(square_function / quadratic_scale == Rational(1, scale_integer),
                 "Z/A decay identity failed")
      (0..5).each do |budget|
        tail = Rational(shell_count - budget, 3)
        ratio = Rational(scale_integer**2, 3) -
                Rational(budget, 3 * scale_integer**4)
        check.call(tail / quadratic_scale == ratio, "flat-tower divergent ratio failed")
      end
    end
  end
end

def exact_family_checks
  exact_group("N_plus_one_target_falsification_and_payment_obstruction") do |check|
    positive_offsets = [Rational(1, 5), Rational(1, 1), Rational(7, 3)]
    [Rational(1, 3), Rational(1, 1), Rational(5, 2)].each do |quadratic_scale|
      [Rational(1, 1), Rational(2, 1), Rational(7, 3)].each do |paid_constant|
        (0..5).each do |budget|
          targets = (0..budget).map do |index|
            paid_constant * quadratic_scale + positive_offsets[index % positive_offsets.length]
          end
          (0...(1 << targets.length)).each do |mask|
            paid_sum = targets.each_with_index.sum(Rational(0, 1)) do |target, index|
              (mask & (1 << index)).zero? ? 0 : target
            end
            next unless paid_sum <= paid_constant * quadratic_scale

            check.call(mask.zero?, "a super-paid target was assigned to a paid class")
          end

          residuals = targets.map.with_index do |target, index|
            target * (Rational(1, 6) + Rational(index + 1, 1000))
          end
          tail = exhaustive_best_tail(residuals, budget)
          check.call(tail > targets.min / 6, "N+1 residual lower bound failed")
        end
      end
    end

    (1..30).each do |ratio|
      budget = ratio % 6
      target_count = budget + 1
      quadratic_scale = Rational(1, 1)
      targets = Array.new(target_count, Rational(ratio + 1, 1))
      residuals = targets.map { |target| target * Rational(1001, 6000) }
      check.call(exhaustive_best_tail(residuals, budget) > Rational(ratio + 1, 6),
                 "finite S.270 divergence surrogate failed")
      check.call(targets.min / quadratic_scale == ratio + 1,
                 "target-to-payment ratio failed")
    end

    c_gamma = Rational(8, 3969)
    rho = Rational(1, 320)
    leading = Rational(5, 6) * c_gamma * Rational(16, 63)**2
    kappa_two = Rational(10, 3) * c_gamma - Rational(2, 3) * rho
    check.call(leading == Rational(5120, 47_258_883), "S.271 leading exponent is wrong")
    check.call(leading.positive?, "S.271 leading exponent is not positive")
    check.call(kappa_two == Rational(8831, 1_905_120), "persistent-lobe exponent is wrong")
    check.call(kappa_two.positive?, "persistent-lobe exponent is not positive")
  end
end

def note_structure_checks(body, actual_hash)
  return [{ "id" => "valid_UTF8", "pass" => false }] unless body.valid_encoding?

  checks = []
  add = lambda do |identifier, condition|
    checks << { "id" => identifier, "pass" => !!condition }
  end

  add.call("valid_UTF8", true)
  add.call("locked_main_note_sha256",
           actual_hash == ARTIFACT_SPECS.fetch("main_note").fetch("sha256"))
  tags = body.scan(/\\tag\{(S\.\d+)\}/).flatten
  add.call("exact_25_tag_sequence", tags == EXPECTED_TAGS)
  add.call("all_25_tags_unique", tags.uniq.length == 25)
  EXPECTED_TAGS.each do |tag|
    add.call("tag_#{tag.delete('.').downcase}_present_once", tags.count(tag) == 1)
  end

  required_fragments = {
    "fixed_profile_quantifiers" => "independently of the solution,",
    "shared_budget_adds_counts" => "N_0=N_{\\rm sh}+N_x",
    "sup_min_noncommutation" => "a supremum and a finite minimum do not generally commute",
    "short_terminal_hypothesis_open" => "\\quad\\textbf{OPEN}",
    "selected_excess_target_open" => "\\textbf{OPEN:}\\quad",
    "combined_target_open" => "\\textbf{OPEN: find fixed }N_{\\rm sh},N_x",
    "rx_literal_constants" => "{1\\over5}x_k^{\\rm sel}<r_k^x<3x_k^{\\rm sel}",
    "rx_global_non_strict_ancestor" => "r_k^x\\le3x_k^{\\rm sel}\\le3b_k",
    "fixed_solution_nonuniform_N" => "N=N(u,R,\\varepsilon)",
    "fixed_solution_N_independent_tau" => "independent of \\(\\tau\\)",
    "pure_defect_flat_tower_only" => "Repeating the pure-defect scalar row",
    "flat_tower_not_NSE" => "It is not an NSE counterexample",
    "S270_positive_payment" => "\\(A_R>0\\) and \\(N+1\\) distinct target shells",
    "single_packet_scope_caveat" => "This does not exclude unproved off-target behavior",
    "S271_payment_definition" => "A_R^{(N)}:=(P_R^{M,(N)})^{2/3}",
    "multipacket_not_universal_no_go" => "not a theorem ruling out every multi-packet architecture",
    "bounded_search_not_exhaustive" => "The search is evidence against an immediate literature shortcut",
    "ancestry_not_last_exit" => "localize either ancestor to the last-exit interval",
    "proved_conditional_implications_only" => "the conditional implications from (S.261), (S.269), (S.270), and",
    "open_ledger_keeps_Q1_open" => "(S.243), Q.12, Q.1, scale contraction",
    "not_claimed_heading" => "The following are **NOT CLAIMED**:",
    "no_selector_regularities_claimed" => "continuity or measurability of the moving branch masks",
    "not_clay_scope_sentence" => "No claim of novelty, singularity formation, regularity, or a",
    "final_not_clay" => "**NOT CLAY.**"
  }
  required_fragments.each do |identifier, fragment|
    add.call(identifier, body.include?(fragment))
  end
  add.call("three_open_boxes_present", body.scan(/\\textbf\{OPEN(?::|\})/).length >= 3)
  add.call("not_clay_repeated", body.scan(/NOT CLAY/).length >= 2)
  add.call("does_not_claim_S243_refutation", body.include?("does not disprove (S.243)"))
  add.call("display_math_balanced", body.scan(/\\\[/).length == body.scan(/\\\]/).length)
  add.call("no_tabs", !body.include?("\t"))
  add.call("no_trailing_whitespace", body.lines.none? { |line| line.match?(/[ \t]+\n\z/) })
  checks
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
      "expected_sha256" => expected,
      "actual_sha256" => actual,
      "locked" => locked,
      "status" => locked ? (actual == expected ? "locked_match" : "locked_mismatch") : "placeholder_unlocked",
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
      "expected_sha256" => spec.fetch("sha256"),
      "actual_sha256" => actual,
      "pass" => actual == spec.fetch("sha256")
    }
  end
end

# All independent mathematics is evaluated before any future primary artifact
# is inspected.  This order prevents a primary certificate from serving as an
# oracle for the Rational fixtures.
groups = [
  shared_budget_checks,
  sup_min_checks,
  dyadic_and_layer_cake_checks,
  rx_comparison_checks,
  rational_clock_checks,
  flat_tower_checks,
  exact_family_checks
]

artifacts = artifact_checks
dependencies = dependency_checks
main_note_row = artifacts.find { |row| row.fetch("id") == "main_note" }
if File.file?(NOTE_PATH)
  note_bytes = File.binread(NOTE_PATH)
  note_body = note_bytes.dup.force_encoding(Encoding::UTF_8)
  note_checks = note_structure_checks(note_body, main_note_row["actual_sha256"])
else
  note_checks = [{ "id" => "main_note_exists", "pass" => false }]
end

pass = groups.all? { |row| row.fetch("pass") } &&
       artifacts.all? { |row| row.fetch("pass") } &&
       dependencies.all? { |row| row.fetch("pass") } &&
       note_checks.all? { |row| row.fetch("pass") }

placeholders = artifacts.reject { |row| row.fetch("locked") }.map { |row| row.fetch("id") }

output = {
  "schema" => SCHEMA,
  "independent_checks" => groups,
  "artifacts" => artifacts,
  "dependencies" => dependencies,
  "note_checks" => note_checks,
  "scope" => {
    "standard_library_Ruby_only" => true,
    "exact_Rational_checks_run_before_future_primary_artifacts" => true,
    "uses_timestamp_random_network_or_gems" => false,
    "machine_proves_inherited_PDE_estimates" => false,
    "machine_proves_S261_or_S269" => false,
    "machine_proves_Q12_Q1_regularity_or_Clay" => false
  },
  "summary" => {
    "independent_groups_passed" => groups.count { |row| row.fetch("pass") },
    "independent_groups_total" => groups.length,
    "independent_cases" => groups.sum { |row| row.fetch("cases") },
    "artifact_locks_passed" => artifacts.count { |row| row.fetch("locked") && row.fetch("pass") },
    "artifact_locks_total" => artifacts.count { |row| row.fetch("locked") },
    "dependency_locks_passed" => dependencies.count { |row| row.fetch("pass") },
    "dependency_locks_total" => dependencies.length,
    "note_checks_passed" => note_checks.count { |row| row.fetch("pass") },
    "note_checks_total" => note_checks.length,
    "placeholder_artifacts" => placeholders
  },
  "release_ready" => placeholders.empty? && pass,
  "pass" => pass
}

puts JSON.pretty_generate(output)
exit(pass ? 0 : 1)
