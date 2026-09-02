#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent standard-library verifier for R0.74S Step 16.
#
# The primary producer represents trigonometric fields by complex Fourier
# Laurent polynomials.  This verifier deliberately uses a different exact
# model: the rational polynomial quotient
#
#   Q[s_x,c_x,s_y,c_y,s_z,c_z] / (s_i^2+c_i^2-1),
#
# with differentiation defined by d s_i = c_i and d c_i = -s_i.  It first
# reconstructs the Taylor and ABC identities, physical-shell deletion,
# support, path, temporal exponent, and payment bookkeeping.  Only after all
# independent groups have been evaluated does it open the primary JSON and
# compare its verdict and claim labels.
#
# Negative mutations can be selected with
#
#   R074S_TAYLOR_INDEPENDENT_MUTATION=<name> ruby <this-file>
#
# where <name> is one of the values in NEGATIVE_MUTATIONS below.  Artifact
# paths can be overridden with R074S_TAYLOR_INDEPENDENT_NOTE and
# R074S_TAYLOR_INDEPENDENT_PRIMARY_JSON; byte-lock mismatches fail closed.
#
# This finite verifier does not machine-prove arbitrary-mollifier continuity,
# the continuum C_R payment bounds, the open critical L1 estimate (S.444),
# regularity, or the Navier--Stokes Millennium problem.

require "digest"
require "json"
require "open3"
require "rbconfig"

REPO = File.expand_path("..", __dir__)
SCHEMA = "r074s-moving-frame-taylor-vortex-independent-verifier-v1"
PRIMARY_SCHEMA = "r074s-moving-frame-taylor-vortex-certificate-v1"

MUTATION_ENV = "R074S_TAYLOR_INDEPENDENT_MUTATION"
INTERNAL_MUTATION_PROBE = "R074S_TAYLOR_INDEPENDENT_INTERNAL_MUTATION_PROBE"
INTERNAL_PATH_PROBE = "R074S_TAYLOR_INDEPENDENT_INTERNAL_PATH_PROBE"
MUTATION = ENV.fetch(MUTATION_ENV, "").strip

NEGATIVE_MUTATIONS = %w[
  taylor_eigenvalue
  abc_directional_derivative
  deletion_cardinality
  support_scale
  path_window
  temporal_height
  payment_power
  note_claim_label
  primary_claim_label
].freeze

ARTIFACT_SPECS = {
  "main_note" => {
    "environment" => "R074S_TAYLOR_INDEPENDENT_NOTE",
    "path" => "research/r074s_moving_frame_taylor_vortex_obstruction.md",
    "sha256" => "de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0"
  },
  "primary_json" => {
    "environment" => "R074S_TAYLOR_INDEPENDENT_PRIMARY_JSON",
    "path" => "research/r074s_moving_frame_taylor_vortex_certificate.json",
    "sha256" => "27f93a7e23268be2c337eef6ae0488a8fb60508c51f6dbf12080807e5f636271"
  }
}.freeze

EXPECTED_TAGS = (
  (417..438).map { |number| "S.#{number}" } +
  %w[S.438a S.438b] +
  (439..444).map { |number| "S.#{number}" }
).freeze

EXPECTED_PRIMARY_CLAIMS = {
  "S342_quadratic_tail_for_p_gt_1" => "FALSE_BY_SMOOTH_EXACT_NSE",
  "S444_critical_L1_tail" => "OPEN",
  "hybrid_terminal_flux_gate" => "OPEN_NOT_REFUTED",
  "Q12" => "OPEN",
  "Q1" => "OPEN",
  "regularity" => "OPEN",
  "millennium_problem_solved" => false
}.freeze

PRIMARY_FINITE_IDS = %w[
  taylor_exact_fourier_identities
  abc_independent_exact_screen
  N_plus_one_deletion_pigeonhole
  finite_small_R_support_screen
  temporal_and_payment_exponents
  terminal_characteristic_screen
  complete_payment_and_L1_amplitude_bookkeeping
].freeze

SOURCE_LINKS = %w[
  https://doi.org/10.1080/14786442308634295
  https://doi.org/10.1098/rspa.1937.0036
  https://doi.org/10.1016/j.physleta.2020.126857
  https://doi.org/10.1017/jfm.2020.126
  https://doi.org/10.1017/S0022112086002859
].freeze

VARIABLE_COUNT = 6
SINE_INDICES = [0, 2, 4].freeze
COSINE_INDICES = [1, 3, 5].freeze
ZERO_MONOMIAL = Array.new(VARIABLE_COUNT, 0).freeze

def mutation?(name)
  MUTATION == name
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

def binomial(n, k)
  return 0 if k.negative? || k > n
  return 1 if k.zero? || k == n

  k = [k, n - k].min
  (1..k).inject(1) { |value, j| value * (n - k + j) / j }
end

def without_zero_coefficients(polynomial)
  clean = {}
  polynomial.each do |powers, value|
    clean[powers] = value unless value.zero?
  end
  clean
end

# Reduce c_i^(2q+r) to (1-s_i^2)^q c_i^r.  The resulting normal form has
# cosine exponent zero or one in every coordinate and is unique for the
# chosen quotient ordering.
def canonical_monomials(powers, coefficient)
  states = { powers.dup => coefficient }
  COSINE_INDICES.each do |cosine_index|
    sine_index = cosine_index - 1
    reduced = Hash.new(Rational(0, 1))
    states.each do |current, current_coefficient|
      quotient, remainder = current[cosine_index].divmod(2)
      (0..quotient).each do |j|
        target = current.dup
        target[cosine_index] = remainder
        target[sine_index] += 2 * j
        sign = j.odd? ? -1 : 1
        reduced[target] += current_coefficient * sign * binomial(quotient, j)
      end
    end
    states = without_zero_coefficients(reduced)
  end
  states
end

def normalize_polynomial(raw)
  answer = Hash.new(Rational(0, 1))
  raw.each do |powers, coefficient|
    next if coefficient.zero?

    canonical_monomials(powers, coefficient).each do |canonical, value|
      answer[canonical] += value
    end
  end
  without_zero_coefficients(answer)
end

def polynomial_constant(value)
  value = Rational(value)
  return {} if value.zero?

  { ZERO_MONOMIAL.dup => value }
end

def polynomial_variable(index)
  powers = ZERO_MONOMIAL.dup
  powers[index] = 1
  { powers => Rational(1, 1) }
end

def polynomial_add(*polynomials)
  raw = Hash.new(Rational(0, 1))
  polynomials.each do |polynomial|
    polynomial.each { |powers, value| raw[powers] += value }
  end
  normalize_polynomial(raw)
end

def polynomial_scale(polynomial, scalar)
  scalar = Rational(scalar)
  normalize_polynomial(polynomial.to_h { |powers, value| [powers, value * scalar] })
end

def polynomial_multiply(left, right)
  raw = Hash.new(Rational(0, 1))
  left.each do |left_powers, left_value|
    right.each do |right_powers, right_value|
      powers = left_powers.zip(right_powers).map { |a, b| a + b }
      raw[powers] += left_value * right_value
    end
  end
  normalize_polynomial(raw)
end

def polynomial_power(polynomial, exponent)
  raise ArgumentError, "negative polynomial power" if exponent.negative?

  answer = polynomial_constant(1)
  exponent.times { answer = polynomial_multiply(answer, polynomial) }
  answer
end

def polynomial_derivative(polynomial, axis)
  sine_index = 2 * axis
  cosine_index = sine_index + 1
  raw = Hash.new(Rational(0, 1))
  polynomial.each do |powers, coefficient|
    sine_power = powers[sine_index]
    cosine_power = powers[cosine_index]
    if sine_power.positive?
      target = powers.dup
      target[sine_index] -= 1
      target[cosine_index] += 1
      raw[target] += coefficient * sine_power
    end
    if cosine_power.positive?
      target = powers.dup
      target[cosine_index] -= 1
      target[sine_index] += 1
      raw[target] -= coefficient * cosine_power
    end
  end
  normalize_polynomial(raw)
end

def polynomial_substitute(polynomial, assignments)
  raw = Hash.new(Rational(0, 1))
  polynomial.each do |powers, coefficient|
    target = powers.dup
    value = coefficient
    assignments.each do |index, assigned|
      value *= Rational(assigned)**target[index]
      target[index] = 0
    end
    raw[target] += value
  end
  normalize_polynomial(raw)
end

def vector_add(left, right)
  (0...3).map { |index| polynomial_add(left[index], right[index]) }
end

def vector_scale(vector, scalar)
  vector.map { |component| polynomial_scale(component, scalar) }
end

def vector_derivative(vector, axis)
  vector.map { |component| polynomial_derivative(component, axis) }
end

def vector_divergence(vector)
  polynomial_add(*(0...3).map { |axis| polynomial_derivative(vector[axis], axis) })
end

def vector_laplacian(vector)
  vector.map do |component|
    polynomial_add(*(0...3).map do |axis|
      polynomial_derivative(polynomial_derivative(component, axis), axis)
    end)
  end
end

def vector_curl(vector)
  [
    polynomial_add(polynomial_derivative(vector[2], 1),
                   polynomial_scale(polynomial_derivative(vector[1], 2), -1)),
    polynomial_add(polynomial_derivative(vector[0], 2),
                   polynomial_scale(polynomial_derivative(vector[2], 0), -1)),
    polynomial_add(polynomial_derivative(vector[1], 0),
                   polynomial_scale(polynomial_derivative(vector[0], 1), -1))
  ]
end

def vector_dot(left, right)
  polynomial_add(*(0...3).map do |index|
    polynomial_multiply(left[index], right[index])
  end)
end

def vector_energy(vector)
  vector_dot(vector, vector)
end

def vector_convection(vector)
  (0...3).map do |component|
    polynomial_add(*(0...3).map do |axis|
      polynomial_multiply(vector[axis], polynomial_derivative(vector[component], axis))
    end)
  end
end

def zero_vector?(vector)
  vector.all?(&:empty?)
end

def evaluate_at_origin(polynomial)
  assignments = {
    0 => Rational(0), 1 => Rational(1),
    2 => Rational(0), 3 => Rational(1),
    4 => Rational(0), 5 => Rational(1)
  }
  reduced = polynomial_substitute(polynomial, assignments)
  reduced.fetch(ZERO_MONOMIAL, Rational(0, 1))
end

SX = polynomial_variable(0).freeze
CX = polynomial_variable(1).freeze
SY = polynomial_variable(2).freeze
CY = polynomial_variable(3).freeze
SZ = polynomial_variable(4).freeze
CZ = polynomial_variable(5).freeze

def cosine_double(sine, cosine)
  polynomial_add(polynomial_power(cosine, 2), polynomial_scale(polynomial_power(sine, 2), -1))
end

def taylor_exact_checks
  exact_group("taylor_exact_trigonometric_quotient") do |check|
    w = [
      polynomial_multiply(SX, CY),
      polynomial_scale(polynomial_multiply(CX, SY), -1),
      {}
    ]
    pressure = polynomial_scale(
      polynomial_add(cosine_double(SX, CX), cosine_double(SY, CY)),
      Rational(1, 4)
    )
    gradient_pressure = (0...3).map { |axis| polynomial_derivative(pressure, axis) }
    eigenvalue = mutation?("taylor_eigenvalue") ? 1 : 2

    check.call(vector_divergence(w).empty?, "Taylor divergence is nonzero")
    check.call(
      zero_vector?(vector_add(vector_laplacian(w), vector_scale(w, eigenvalue))),
      "Taylor Laplace eigenvalue is not the expected value"
    )
    check.call(
      zero_vector?(vector_add(vector_convection(w), gradient_pressure)),
      "Taylor convection does not equal minus pressure gradient"
    )

    energy = vector_energy(w)
    expected_energy = polynomial_add(
      polynomial_constant(Rational(1, 2)),
      polynomial_scale(
        polynomial_multiply(cosine_double(SX, CX), cosine_double(SY, CY)),
        Rational(-1, 2)
      )
    )
    check.call(energy == expected_energy, "Taylor modulus-square identity failed")

    bernoulli = polynomial_add(polynomial_scale(energy, Rational(1, 2)), pressure)
    bernoulli_current = w.map { |component| polynomial_multiply(bernoulli, component) }
    check.call(vector_divergence(bernoulli_current).empty?,
               "Taylor fixed-frame Bernoulli current is not divergence free")

    directional = vector_dot(w, (0...3).map { |axis| polynomial_derivative(energy, axis) })
    line_value = polynomial_substitute(
      directional,
      2 => Rational(0), 3 => Rational(1), 4 => Rational(0), 5 => Rational(1)
    )
    expected_line = polynomial_scale(
      polynomial_multiply(polynomial_power(SX, 2), CX),
      2
    )
    check.call(line_value == expected_line,
               "Taylor invariant-line drift is not sin(x) sin(2x)")

    # With b'=-2b and Delta W=-2W, the time and viscous rows cancel;
    # the remaining nonlinear row is the pressure gradient checked above.
    check.call(eigenvalue == 2, "Taylor exponential decay rate must be two")
  end
end

def abc_exact_checks
  exact_group("abc_exact_trigonometric_quotient") do |check|
    u = [
      polynomial_add(SZ, CY),
      polynomial_add(SX, CZ),
      polynomial_add(SY, CX)
    ]
    check.call(vector_divergence(u).empty?, "ABC divergence is nonzero")
    check.call(zero_vector?(vector_add(vector_curl(u), vector_scale(u, -1))),
               "ABC curl is not U")
    check.call(zero_vector?(vector_add(vector_laplacian(u), u)),
               "ABC Laplacian is not -U")

    energy = vector_energy(u)
    expected_energy = polynomial_add(
      polynomial_constant(3),
      polynomial_scale(polynomial_add(
        polynomial_multiply(SZ, CY),
        polynomial_multiply(SX, CZ),
        polynomial_multiply(SY, CX)
      ), 2)
    )
    check.call(energy == expected_energy,
               "ABC nonconstant modulus-square modes are wrong")

    mean_zero_pressure = polynomial_scale(
      polynomial_add(energy, polynomial_constant(-3)),
      Rational(-1, 2)
    )
    gradient_pressure = (0...3).map do |axis|
      polynomial_derivative(mean_zero_pressure, axis)
    end
    check.call(zero_vector?(vector_add(vector_convection(u), gradient_pressure)),
               "ABC convection and mean-zero pressure do not cancel")

    phase_u = u.map { |component| evaluate_at_origin(component) }
    phase_gradient = (0...3).map do |axis|
      evaluate_at_origin(polynomial_derivative(energy, axis))
    end
    directional = phase_u.zip(phase_gradient).inject(Rational(0, 1)) do |total, pair|
      total + pair[0] * pair[1]
    end
    expected_directional = mutation?("abc_directional_derivative") ? 5 : 6
    check.call(phase_u == [1, 1, 1], "ABC value at the origin is not (1,1,1)")
    check.call(phase_gradient == [2, 2, 2],
               "ABC modulus-square gradient at the origin is not (2,2,2)")
    check.call(directional == expected_directional,
               "ABC directional derivative has the wrong value")
    check.call(expected_directional == 6,
               "ABC directional-derivative mutation was not rejected")
  end
end

def squared_length(mode)
  mode.inject(0) { |total, coordinate| total + coordinate**2 }
end

def spectral_multiplier_checks
  exact_group("independent_spectral_and_radial_multiplier_data") do |check|
    taylor_velocity_modes = [
      [1, 1, 0], [1, -1, 0], [-1, 1, 0], [-1, -1, 0]
    ]
    taylor_energy_modes = [
      [2, 2, 0], [2, -2, 0], [-2, 2, 0], [-2, -2, 0]
    ]
    abc_velocity_modes = [
      [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]
    ]
    abc_energy_modes = []
    [[0, 1, 1], [1, 0, 1], [1, 1, 0]].each do |seed|
      [-1, 1].repeated_permutation(2) do |signs|
        nonzero = 0
        abc_energy_modes << seed.map do |entry|
          next 0 if entry.zero?

          value = signs[nonzero]
          nonzero += 1
          value
        end
      end
    end

    check.call(taylor_velocity_modes.all? { |mode| squared_length(mode) == 2 },
               "Taylor velocity modes do not share length sqrt(2)")
    check.call(taylor_energy_modes.all? { |mode| squared_length(mode) == 8 },
               "Taylor modulus-square modes do not share length 2sqrt(2)")
    check.call(abc_velocity_modes.all? { |mode| squared_length(mode) == 1 },
               "ABC velocity modes do not share unit length")
    check.call(abc_energy_modes.length == 12 &&
               abc_energy_modes.all? { |mode| squared_length(mode) == 2 },
               "ABC modulus-square modes do not share length sqrt(2)")
    check.call(taylor_velocity_modes.map { |mode| squared_length(mode) }.uniq == [2],
               "a radial mollifier would not give one Taylor velocity multiplier")
    check.call(taylor_energy_modes.map { |mode| squared_length(mode) }.uniq == [8],
               "a radial cutoff would not give one Taylor energy multiplier")
  end
end

def rational_sum(values)
  values.inject(Rational(0, 1), :+)
end

def brute_best_tail(values, budget)
  raise ArgumentError, "negative deletion budget" if budget.negative?
  raise ArgumentError, "negative coordinate" if values.any?(&:negative?)

  indices = (0...values.length).to_a
  maximum = [budget, values.length].min
  candidates = []
  (0..maximum).each do |size|
    indices.combination(size) do |deleted|
      lookup = deleted.to_h { |index| [index, true] }
      candidates << rational_sum(values.each_with_index.map do |value, index|
        value unless lookup[index]
      end.compact)
    end
  end
  candidates.min || Rational(0, 1)
end

def deletion_checks
  exact_group("N_plus_one_common_deletion") do |check|
    (0..10).each do |budget|
      coordinate_count = mutation?("deletion_cardinality") ? budget : budget + 1
      values = (1..coordinate_count).map { |index| Rational(1, index) }
      check.call(coordinate_count == budget + 1,
                 "the witness does not contain N+1 coordinates")
      tail = brute_best_tail(values, budget)
      check.call(tail == Rational(1, budget + 1),
                 "best-N deletion did not leave the smallest positive coordinate")
      check.call(tail.positive?, "N deletions removed all N+1 positive coordinates")
    end
    (0..256).each do |budget|
      check.call((budget + 1) - budget == 1,
                 "generic complement-cardinality identity failed")
    end
  end
end

def support_denominator
  mutation?("support_scale") ? 2 : 32
end

def witness_radius(budget, denominator = support_denominator)
  shell_count = budget + 1
  support_factor = Rational(2**(shell_count + 1) * 8 + 1, 8)
  [Rational(1, denominator) / support_factor, support_factor]
end

def support_checks
  exact_group("physical_shell_support_and_cosine_positivity") do |check|
    (0..64).each do |budget|
      radius, largest_factor = witness_radius(budget)
      largest_support_radius = largest_factor * radius
      q_dot_y_squared_bound = 8 * largest_support_radius**2

      check.call(radius.positive?, "chosen physical scale is not positive")
      # pi>3: R<3/16 is a stronger rational check than R<pi/16.
      check.call(radius < Rational(3, 16), "R<pi/16 was not certified")
      # Squaring the other S.429 constraint and again using pi^2>9.
      check.call(72 * (largest_factor * radius)**2 < 9,
                 "R<pi/(6sqrt(2) support_factor) was not certified")
      # |q.y|^2 <= |q|^2 |y|^2, |q|^2=8.  Since pi/3>1,
      # a bound below one puts the support strictly in cos(q.y)>1/2.
      check.call(q_dot_y_squared_bound < 1,
                 "Taylor energy phase left the cosine-positive region")
      (1..(budget + 1)).each do |shell_index|
        factor = Rational(2**(shell_index + 1) * 8 + 1, 8)
        check.call(factor * radius <= largest_support_radius,
                   "an earlier physical shell exceeded the largest support")
      end
    end
    check.call(support_denominator == 32,
               "support-scale negative mutation was not rejected")
  end
end

def path_delta
  mutation?("path_window") ? Rational(1, 2) : Rational(1, 100)
end

def path_checks
  exact_group("terminal_characteristic_and_positive_drift_block") do |check|
    # If y=tan(xi/2) and y'=mu*b*y, then xi'=mu*b*sin(xi).
    [Rational(1, 5), Rational(2, 3), Rational(5, 4)].each do |half_angle|
      [Rational(1, 2), Rational(3, 4), Rational(1)].each do |multiplier|
        [Rational(2, 3), Rational(5), Rational(17, 4)].each do |amplitude|
          check.call(multiplier.positive? && multiplier <= 1,
                     "mollifier multiplier left the normalized positive range")
          sine_xi = 2 * half_angle / (1 + half_angle**2)
          xi_derivative = 2 * multiplier * amplitude * half_angle /
                          (1 + half_angle**2)
          check.call(xi_derivative == multiplier * amplitude * sine_xi,
                     "half-angle characteristic formula failed")
        end
      end
    end

    delta = path_delta
    check.call(2 * delta < 1, "path window is too long for the exponential bound")
    exponential_integral_bound = delta / (1 - 2 * delta)
    # e^x <= 1/(1-x) for 0<=x<1, and pi>3.  Thus the backward
    # displacement is below pi/8 and xi remains in [pi/8,pi/4].
    check.call(exponential_integral_bound < Rational(3, 8),
               "terminal path may leave the positive phase sector")

    [0, 3, 8, 16, 32].each do |budget|
      radius, = witness_radius(budget, 32)
      threshold = delta / radius**2
      amplitude = threshold.floor + 1
      physical_width = delta / amplitude
      dimensionless_width = physical_width / radius**2
      check.call(physical_width < radius**2,
                 "terminal physical block did not fit inside I_R")
      check.call(dimensionless_width == delta / (amplitude * radius**2),
                 "physical-to-dimensionless time conversion failed")
      check.call(dimensionless_width.positive?, "terminal block has zero width")
    end

    check.call(path_delta == Rational(1, 100),
               "path-window negative mutation was not rejected")
  end
end

def exponent_checks
  exact_group("temporal_tail_R_A_and_payment_exponents") do |check|
    height_exponent = mutation?("temporal_height") ? Rational(2) : Rational(3)
    p_values = [
      Rational(1), Rational(12, 11), Rational(4, 3), Rational(2), Rational(4), nil
    ]
    p_values.each do |p_value|
      inverse_p = p_value.nil? ? Rational(0) : 1 / p_value
      amplitude_exponent = height_exponent - inverse_p
      radius_exponent = 1 - 2 * inverse_p
      ratio_exponent = amplitude_exponent - 2
      minimum_payment_power = amplitude_exponent / 3

      check.call(amplitude_exponent == 3 - inverse_p,
                 "A exponent is not 3-1/p")
      check.call(radius_exponent == 1 - 2 * inverse_p,
                 "R exponent is not 1-2/p")
      check.call(ratio_exponent == 1 - inverse_p,
                 "quadratic-payment ratio exponent is wrong")
      check.call(minimum_payment_power == 1 - inverse_p / 3,
                 "minimum beta is not 1-1/(3p)")
      if p_value == 1
        check.call(ratio_exponent.zero? && minimum_payment_power == Rational(2, 3),
                   "critical p=1 amplitude saturation failed")
      else
        check.call(ratio_exponent.positive? &&
                   minimum_payment_power > Rational(2, 3),
                   "supercritical p>1 obstruction exponent failed")
      end
    end

    [Rational(0), Rational(1, 4), Rational(1), Rational(7, 3)].each do |alpha|
      beta = (2 + alpha) / 3
      check.call(3 * beta - alpha == 2,
                 "positive-window boundary 3beta-alpha=2 failed")
    end
    check.call(3 * Rational(2, 3) - Rational(1, 4) < 2,
               "quadratic payment incorrectly allowed positive time gain")
    check.call(height_exponent == 3,
               "temporal-height negative mutation was not rejected")
  end
end

def payment_checks
  exact_group("complete_payment_and_critical_L1_bookkeeping") do |check|
    payment_cap = mutation?("payment_power") ? Rational(2) : Rational(3)
    rows = {
      "buffered_energy_then_three_halves" => Rational(2) * Rational(3, 2),
      "velocity_cubic" => Rational(1) * Rational(3),
      "pressure_then_three_halves" => Rational(2) * Rational(3, 2),
      "harmonic_Lambda_then_three_halves" => Rational(2) * Rational(3, 2)
    }
    rows.each do |name, exponent|
      check.call(exponent <= payment_cap,
                 "#{name} exceeds the claimed A^#{payment_cap} payment cap")
      check.call(exponent == 3, "#{name} does not have cubic amplitude scale")
    end
    endpoint_lower = Rational(2) * Rational(3, 2)
    critical_l1 = Rational(3) - Rational(1)
    check.call(endpoint_lower == 3, "endpoint payment lower exponent is not three")
    check.call(critical_l1 == 2, "critical L1 tail exponent is not two")
    check.call(critical_l1 == Rational(2, 3) * endpoint_lower,
               "p=1 tail does not match P^(2/3) in amplitude")
    check.call(payment_cap == 3, "payment-power negative mutation was not rejected")
  end
end

def configuration_checks
  exact_group("mutation_configuration") do |check|
    check.call(MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION),
               "unknown #{MUTATION_ENV}=#{MUTATION.inspect}")
  end
end

def independent_checks
  [
    configuration_checks,
    taylor_exact_checks,
    abc_exact_checks,
    spectral_multiplier_checks,
    deletion_checks,
    support_checks,
    path_checks,
    exponent_checks,
    payment_checks
  ]
end

def resolved_path(spec)
  default_path = File.join(REPO, spec.fetch("path"))
  File.expand_path(ENV.fetch(spec.fetch("environment"), default_path))
end

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

def artifact_checks
  ARTIFACT_SPECS.map do |identifier, spec|
    path = resolved_path(spec)
    actual = File.file?(path) ? sha256(path) : nil
    {
      "id" => identifier,
      "path" => spec.fetch("path"),
      "resolved_path" => path,
      "expected_sha256" => spec.fetch("sha256"),
      "actual_sha256" => actual,
      "pass" => actual == spec.fetch("sha256")
    }
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
  tags = body.scan(/\\tag\{(S\.\d+(?:a|b)?)\}/).flatten

  add.call("exact_S417_S444_tag_sequence", tags == EXPECTED_TAGS)
  add.call("all_30_tags_unique", tags.uniq.length == EXPECTED_TAGS.length)
  add.call("display_math_balanced", body.scan(/\\\[/).length == body.scan(/\\\]/).length)
  add.call("valid_UTF8", body.valid_encoding?)
  add.call("no_CR_or_NUL", !bytes.include?("\r") && !bytes.include?("\0"))
  add.call("no_forbidden_controls", bytes.bytes.none? { |byte| byte < 32 && byte != 10 })

  add.call("taylor_1923_nomenclature",
           body.include?("Taylor's 1923 bi-periodic decaying vortex"))
  add.call("taylor_green_3D_boundary",
           body.include?("not the fully three-dimensional datum studied by Taylor and"))
  add.call("exact_NSE_anchor", compact_body.include?(compact(
    '\\partial_tu_A-\\Delta u_A+(u_A\\!\\cdot\\!\\nabla)u_A+\\nabla p_A=0'
  )))
  add.call("physical_not_Fourier_shells",
           body.include?("distinct physical annuli") &&
           body.include?("No Fourier-shell index"))
  add.call("moving_drift_anchor",
           body.include?("fixed-frame physical energy flux is zero") &&
           body.include?("moving-cutoff drift"))
  add.call("complete_payment_convergence_boundary",
           body.include?("exterior \\(\\mathcal G\\) all-copy sums converge by the frozen") &&
           body.include?("super-Gaussian shell weights, while the harmonic \\(\\mathcal H\\) row uses") &&
           body.include?("frozen algebraic order-\\(-4\\) kernel") &&
           compact_body.include?(compact('P_R^M\\le C_RA^3')))
  add.call("S342_false_narrow_claim",
           !mutation?("note_claim_label") &&
           body.include?("**(S.342 is false)**") &&
           body.include?("The counterexample is only to the supercritical temporal-tail statement"))
  add.call("S342_quantifier_negation",
           body.include?('\\text{For every }p\\in(1,\\infty],\\ N\\in\\mathbb N_0,\\ C>0') &&
           body.include?('\\mathfrak H^F_{p,N,R}>C(P_R^M)^{2/3}'))
  add.call("S444_universal_and_open",
           body.include?('\\forall\\text{ admissible Version-M solutions, }R,z_0') &&
           body.include?("Equation (S.444) is **OPEN**"))
  add.call("p1_extension_not_literal_S388",
           body.include?("Step 15 (S.386)--(S.387) already includes") &&
           body.include?("Repeating the implication (S.389)--(S.391)"))
  add.call("ABC_mean_zero_pressure_and_sketch",
           body.include?("mean-zero pressure") &&
           compact_body.include?(compact('-b_A^2(|U|^2-3)/2')) &&
           body.include?("corroborating verification sketch"))
  add.call("source_links_complete", SOURCE_LINKS.all? { |link| body.include?(link) })
  add.call("source_search_not_priority",
           body.include?("bounded collision search") &&
           body.include?("not a priority claim"))
  add.call("downstream_open_claims",
           body.include?("The following remain **OPEN AND UNCHANGED**:") &&
           body.include?("Q.1, scale contraction, and regularity"))
  add.call("not_CLAY", body.include?("**NOT CLAY.**"))
  add.call("no_route_minimal_overclaim", !body.include?("route-minimal"))
  rows
end

def note_structure_checks(artifacts)
  artifact = artifacts.find { |row| row.fetch("id") == "main_note" }
  return [{ "id" => "main_note_exists", "pass" => false }] unless artifact &&
                                                                       File.file?(artifact.fetch("resolved_path"))

  bytes = File.binread(artifact.fetch("resolved_path"))
  body = bytes.dup.force_encoding(Encoding::UTF_8)
  rows = [{
    "id" => "main_note_hash_lock",
    "expected_sha256" => artifact.fetch("expected_sha256"),
    "actual_sha256" => artifact.fetch("actual_sha256"),
    "pass" => artifact.fetch("pass")
  }]
  return rows + [{ "id" => "valid_UTF8", "pass" => false }] unless body.valid_encoding?

  rows + semantic_note_checks(body, bytes)
end

def statement_mutation_checks(body)
  exact_group("statement_negative_mutations_rejected") do |check|
    mutations = {
      "S342_false_narrow_claim" => ["**(S.342 is false)**", "**(S.342 is open)**"],
      "S342_quantifier_negation" => [
        '\\ N\\in\\mathbb N_0,\\ C>0', '\\ N=0,\\ C>0'
      ],
      "physical_not_Fourier_shells" => [
        "distinct physical annuli", "distinct Fourier annuli"
      ],
      "S444_universal_and_open" => [
        "Equation (S.444) is **OPEN**", "Equation (S.444) is **PROVED**"
      ],
      "p1_extension_not_literal_S388" => [
        "Step 15 (S.386)--(S.387) already includes",
        "Step 15 (S.388) already includes"
      ],
      "taylor_green_3D_boundary" => [
        "not the fully three-dimensional datum studied by Taylor and",
        "is the fully three-dimensional datum studied by Taylor and"
      ],
      "ABC_mean_zero_pressure_and_sketch" => [
        "mean-zero pressure", "unnormalized pressure"
      ],
      "complete_payment_convergence_boundary" => [
        "frozen algebraic order-\\(-4\\) kernel",
        "another super-Gaussian shell weight"
      ],
      "source_search_not_priority" => [
        "not a priority claim", "a priority claim"
      ],
      "downstream_open_claims" => [
        "The following remain **OPEN AND UNCHANGED**:",
        "The following are **PROVED AND CLOSED**:"
      ],
      "not_CLAY" => ["**NOT CLAY.**", "**CLAY.**"]
    }
    mutations.each do |target_id, pair|
      mutated = body.sub(pair[0], pair[1])
      check.call(mutated != body, "mutation marker absent for #{target_id}")
      target = semantic_note_checks(mutated, mutated.encode(Encoding::UTF_8)).find do |row|
        row.fetch("id") == target_id
      end
      check.call(target && !target.fetch("pass"),
                 "semantic checks accepted mutation #{target_id}")
    end

    duplicate_tag = body.sub("\\tag{S.444}", "\\tag{S.443}")
    tag_target = semantic_note_checks(
      duplicate_tag, duplicate_tag.encode(Encoding::UTF_8)
    ).find { |row| row.fetch("id") == "exact_S417_S444_tag_sequence" }
    check.call(tag_target && !tag_target.fetch("pass"),
               "duplicate final equation tag was accepted")

    damaged_bytes = body.b + "\r\0"
    damaged_body = damaged_bytes.dup.force_encoding(Encoding::UTF_8)
    byte_target = semantic_note_checks(damaged_body, damaged_bytes).find do |row|
      row.fetch("id") == "no_CR_or_NUL"
    end
    check.call(byte_target && !byte_target.fetch("pass"),
               "CR/NUL injection was accepted")
  end
end

def primary_json_comparison(independent_groups, artifacts)
  exact_group("primary_JSON_verdict_and_claim_label_comparison") do |check|
    artifact = artifacts.find { |row| row.fetch("id") == "primary_json" }
    check.call(artifact && File.file?(artifact.fetch("resolved_path")),
               "primary JSON is missing")

    # This is the first JSON.parse/File.read of the primary payload in the
    # normal control flow, and independent_groups was fully evaluated before
    # artifact_checks or this method was invoked.
    payload = JSON.parse(File.read(artifact.fetch("resolved_path"), encoding: "UTF-8"))
    check.call(payload.fetch("schema") == PRIMARY_SCHEMA, "primary schema changed")
    check.call(payload.fetch("verdict") == "PASS", "primary verdict is not PASS")
    check.call(independent_groups.all? { |row| row.fetch("pass") },
               "independent mathematics did not support a PASS comparison")

    expected_claims = EXPECTED_PRIMARY_CLAIMS.dup
    if mutation?("primary_claim_label")
      expected_claims["S342_quadratic_tail_for_p_gt_1"] = "OPEN"
    end
    check.call(payload.fetch("claim_boundary") == expected_claims,
               "primary claim-boundary labels changed")
    check.call(
      payload.fetch("claim_boundary").fetch("S342_quadratic_tail_for_p_gt_1") ==
        "FALSE_BY_SMOOTH_EXACT_NSE",
      "primary S.342 verdict is not the independently reconstructed label"
    )
    check.call(payload.fetch("claim_boundary").fetch("S444_critical_L1_tail") == "OPEN",
               "primary JSON promoted the open critical endpoint")
    check.call(payload.fetch("claim_boundary").fetch("millennium_problem_solved") == false,
               "primary JSON claims the Millennium problem is solved")
    check.call(payload.fetch("note").fetch("sha256") ==
               ARTIFACT_SPECS.fetch("main_note").fetch("sha256"),
               "primary JSON is bound to a different note")

    primary_ids = payload.fetch("finite_checks").map { |row| row.fetch("id") }
    check.call(primary_ids == PRIMARY_FINITE_IDS, "primary finite-check inventory changed")
    %w[finite_checks structural_checks dependency_checks].each do |key|
      check.call(payload.fetch(key).all? { |row| row.fetch("pass") },
                 "primary JSON contains a failed #{key} row")
    end
  end
end

def mutation_environment_checks
  exact_group("environment_selected_negative_mutations_fail_closed") do |check|
    NEGATIVE_MUTATIONS.each do |mutation|
      environment = {
        INTERNAL_MUTATION_PROBE => "1",
        MUTATION_ENV => mutation
      }
      stdout, stderr, status = Open3.capture3(
        environment, RbConfig.ruby, File.expand_path(__FILE__)
      )
      payload = JSON.parse(stdout)
      check.call(!status.success?, "mutation #{mutation} exited successfully")
      check.call(stderr.empty?, "mutation #{mutation} wrote stderr")
      check.call(payload.fetch("mutation") == mutation,
                 "mutation probe did not report #{mutation}")
      check.call(payload.fetch("pass") == false,
                 "mutation #{mutation} was not rejected")
    end
  end
end

def path_override_checks
  exact_group("environment_artifact_path_overrides_fail_closed") do |check|
    probes = [
      ["R074S_TAYLOR_INDEPENDENT_NOTE", "main_note"],
      ["R074S_TAYLOR_INDEPENDENT_PRIMARY_JSON", "primary_json"]
    ]
    probes.each do |environment_key, target_id|
      environment = {
        INTERNAL_PATH_PROBE => "1",
        MUTATION_ENV => "",
        environment_key => File.expand_path(__FILE__)
      }
      stdout, stderr, status = Open3.capture3(
        environment, RbConfig.ruby, File.expand_path(__FILE__)
      )
      payload = JSON.parse(stdout)
      target = payload.fetch("artifacts").find { |row| row.fetch("id") == target_id }
      check.call(!status.success?, "#{environment_key} mismatch exited successfully")
      check.call(stderr.empty?, "#{environment_key} mismatch wrote stderr")
      check.call(target && !target.fetch("pass"),
                 "#{environment_key} mismatch passed its byte lock")
      check.call(target.fetch("actual_sha256") == sha256(__FILE__),
                 "#{environment_key} did not resolve to the injected file")
    end
  end
end

# Independent mathematics is deliberately complete before any artifact hash,
# note read, or primary JSON read occurs below.
independent_groups = independent_checks

if ENV[INTERNAL_PATH_PROBE] == "1"
  artifacts = artifact_checks
  passed = independent_groups.all? { |row| row.fetch("pass") } &&
           artifacts.all? { |row| row.fetch("pass") }
  puts JSON.generate({
    "mutation" => MUTATION,
    "independent_checks" => independent_groups,
    "artifacts" => artifacts,
    "pass" => passed
  })
  exit(passed ? 0 : 1)
end

if ENV[INTERNAL_MUTATION_PROBE] == "1"
  extra_groups = []
  if mutation?("note_claim_label")
    artifacts = artifact_checks
    note_artifact = artifacts.find { |row| row.fetch("id") == "main_note" }
    bytes = File.binread(note_artifact.fetch("resolved_path"))
    body = bytes.dup.force_encoding(Encoding::UTF_8)
    rows = semantic_note_checks(body, bytes)
    extra_groups << {
      "id" => "mutated_note_semantics",
      "cases" => rows.length,
      "pass" => rows.all? { |row| row.fetch("pass") }
    }
  elsif mutation?("primary_claim_label")
    artifacts = artifact_checks
    extra_groups << primary_json_comparison(independent_groups, artifacts)
  end
  all_groups = independent_groups + extra_groups
  passed = all_groups.all? { |row| row.fetch("pass") }
  puts JSON.generate({
    "mutation" => MUTATION,
    "checks" => all_groups,
    "pass" => passed
  })
  exit(passed ? 0 : 1)
end

# Artifact inspection starts only here, after the independent calculations.
artifacts = artifact_checks
note_checks = note_structure_checks(artifacts)
note_artifact = artifacts.find { |row| row.fetch("id") == "main_note" }
if note_artifact && File.file?(note_artifact.fetch("resolved_path"))
  note_body = File.read(note_artifact.fetch("resolved_path"), encoding: "UTF-8")
  statement_mutations = statement_mutation_checks(note_body)
else
  statement_mutations = {
    "id" => "statement_negative_mutations_rejected",
    "cases" => 0,
    "error" => "main note missing",
    "pass" => false
  }
end

# The primary JSON content is opened only after every independent group above
# has returned.  It is used solely for verdict/label comparison, never as a
# mathematical oracle.
primary_comparison = primary_json_comparison(independent_groups, artifacts)
environment_mutations = mutation_environment_checks
path_mutations = path_override_checks
negative_groups = [statement_mutations, environment_mutations, path_mutations]

passed = independent_groups.all? { |row| row.fetch("pass") } &&
         artifacts.all? { |row| row.fetch("pass") } &&
         note_checks.all? { |row| row.fetch("pass") } &&
         primary_comparison.fetch("pass") &&
         negative_groups.all? { |row| row.fetch("pass") }

output = {
  "schema" => SCHEMA,
  "mutation" => MUTATION.empty? ? nil : MUTATION,
  "independent_checks" => independent_groups,
  "artifacts" => artifacts,
  "note_checks" => note_checks,
  "primary_artifact_checks" => [primary_comparison],
  "negative_mutation_checks" => negative_groups,
  "scope" => {
    "standard_library_Ruby_with_exact_Rational_trigonometric_quotient" => true,
    "independent_math_precedes_all_primary_JSON_access" => true,
    "calls_or_imports_primary_generator" => false,
    "uses_floating_point_random_timestamp_network_or_gems" => false,
    "machine_proves_arbitrary_mollifier_continuity" => false,
    "machine_proves_continuum_payment_bounds" => false,
    "machine_proves_open_critical_tail_S444" => false,
    "machine_proves_regularity_or_Clay" => false
  },
  "summary" => {
    "independent_groups_passed" => independent_groups.count { |row| row.fetch("pass") },
    "independent_groups_total" => independent_groups.length,
    "independent_cases" => independent_groups.inject(0) { |sum, row| sum + row.fetch("cases") },
    "artifact_locks_passed" => artifacts.count { |row| row.fetch("pass") },
    "artifact_locks_total" => artifacts.length,
    "note_checks_passed" => note_checks.count { |row| row.fetch("pass") },
    "note_checks_total" => note_checks.length,
    "primary_comparison_cases" => primary_comparison.fetch("cases"),
    "negative_groups_passed" => negative_groups.count { |row| row.fetch("pass") },
    "negative_groups_total" => negative_groups.length,
    "negative_cases" => negative_groups.inject(0) { |sum, row| sum + row.fetch("cases") }
  },
  "pass" => passed
}

puts JSON.pretty_generate(output)
exit(passed ? 0 : 1)
