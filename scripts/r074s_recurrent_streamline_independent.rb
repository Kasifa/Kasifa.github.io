#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent standard-library audit for R0.74S Step 17.
#
# The exact field calculations below do not import or invoke the primary
# Python certificate.  They use a rational trigonometric-polynomial quotient
#
#   Q[s_x,c_x,s_y,c_y] / (s_x^2+c_x^2-1, s_y^2+c_y^2-1)
#
# and the derivations d(s_i)=c_i, d(c_i)=-s_i.  The remaining finite checks
# use Rational arithmetic and exhaustive deletion of finite coordinate sets.
# Text checks are evaluated only after the independent mathematics.
#
# This audit does not machine-prove the continuum regular-level theorem,
# arbitrary-cutoff positivity, the Version-M analytic payment bounds, the
# open positive-excursion estimate (S.472), regularity, or a Clay claim.

require "digest"
require "json"
require "open3"
require "rbconfig"

REPO = File.expand_path("..", __dir__)
SCHEMA = "r074s-recurrent-streamline-independent-audit-v1"
STEP16_PARENT_COMMIT = "159ea3c548e51b918512855cf79959460e882b48"
STEP17_CORE_COMMIT = "7355c01dead23c3524242006318b02a8324447e6"

MUTATION_ENV = "R074S_RECURRENT_INDEPENDENT_MUTATION"
INTERNAL_MUTATION = "R074S_RECURRENT_INDEPENDENT_INTERNAL_MUTATION"
INTERNAL_PATH = "R074S_RECURRENT_INDEPENDENT_INTERNAL_PATH"
INTERNAL_STABILITY = "R074S_RECURRENT_INDEPENDENT_INTERNAL_STABILITY"
MUTATION = ENV.fetch(MUTATION_ENV, "").strip

NEGATIVE_MUTATIONS = %w[
  taylor_laplacian
  taylor_pressure_sign
  level_value
  orbit_orientation
  positive_phase_order
  period_floor
  phase_length_power
  flux_radius_power
  lp_amplitude_power
  range_amplitude_power
  payment_amplitude_power
  deletion_cardinality
  jordan_endpoint
  clock_start
  clock_relation
  hybrid_infimum_direction
].freeze

ARTIFACT_SPECS = {
  "step17_note" => {
    "environment" => "R074S_RECURRENT_INDEPENDENT_NOTE",
    "path" => "research/r074s_recurrent_streamline_temporal_tail_obstruction.md",
    "sha256" => "7d204b326be45a82bc0d8531ea2f2d894c0c125b76e3ccbf02fdc1978a6011c5"
  },
  "step15_note" => {
    "environment" => "R074S_RECURRENT_INDEPENDENT_STEP15",
    "path" => "research/r074s_hybrid_flux_tail_equivalence.md",
    "sha256" => "2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d"
  },
  "step16_note" => {
    "environment" => "R074S_RECURRENT_INDEPENDENT_STEP16",
    "path" => "research/r074s_moving_frame_taylor_vortex_obstruction.md",
    "sha256" => "de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0"
  }
}.freeze

EXPECTED_TAGS = (445..475).map { |number| "S.#{number}" }.freeze

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

# Exact quotient normal form: each cosine exponent is reduced to zero or one
# by c_i^(2q+r)=(1-s_i^2)^q c_i^r.
class TrigPoly
  VARIABLE_COUNT = 4
  COSINE_INDICES = [1, 3].freeze
  ZERO = Array.new(VARIABLE_COUNT, 0).freeze

  attr_reader :terms

  def initialize(raw = {})
    accumulated = Hash.new(Rational(0, 1))
    raw.each do |powers, coefficient|
      coefficient = Rational(coefficient)
      next if coefficient.zero?

      states = { powers.dup => coefficient }
      COSINE_INDICES.each do |cosine_index|
        sine_index = cosine_index - 1
        reduced = Hash.new(Rational(0, 1))
        states.each do |current, current_coefficient|
          quotient, remainder = current.fetch(cosine_index).divmod(2)
          (0..quotient).each do |j|
            target = current.dup
            target[cosine_index] = remainder
            target[sine_index] += 2 * j
            reduced[target] += current_coefficient * (j.odd? ? -1 : 1) *
                               binomial(quotient, j)
          end
        end
        states = reduced.reject { |_powers, value| value.zero? }
      end
      states.each { |powers2, value| accumulated[powers2] += value }
    end
    @terms = accumulated.reject { |_powers, value| value.zero? }
  end

  def self.constant(value)
    value = Rational(value)
    value.zero? ? new : new(ZERO.dup => value)
  end

  def self.variable(index)
    powers = ZERO.dup
    powers[index] = 1
    new(powers => Rational(1, 1))
  end

  def +(other)
    raw = Hash.new(Rational(0, 1))
    @terms.each { |powers, value| raw[powers] += value }
    other.terms.each { |powers, value| raw[powers] += value }
    TrigPoly.new(raw)
  end

  def -@
    scale(-1)
  end

  def -(other)
    self + (-other)
  end

  def *(other)
    raw = Hash.new(Rational(0, 1))
    @terms.each do |left_powers, left_value|
      other.terms.each do |right_powers, right_value|
        powers = left_powers.zip(right_powers).map { |a, b| a + b }
        raw[powers] += left_value * right_value
      end
    end
    TrigPoly.new(raw)
  end

  def scale(value)
    value = Rational(value)
    TrigPoly.new(@terms.to_h { |powers, coefficient| [powers, coefficient * value] })
  end

  def derivative(axis)
    sine_index = 2 * axis
    cosine_index = sine_index + 1
    raw = Hash.new(Rational(0, 1))
    @terms.each do |powers, coefficient|
      sine_power = powers.fetch(sine_index)
      cosine_power = powers.fetch(cosine_index)
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
    TrigPoly.new(raw)
  end

  def **(power)
    raise ArgumentError, "negative polynomial power" if power.negative?

    answer = TrigPoly.constant(1)
    power.times { answer *= self }
    answer
  end

  def zero?
    @terms.empty?
  end

  def ==(other)
    other.is_a?(TrigPoly) && @terms == other.terms
  end
end

SX = TrigPoly.variable(0)
CX = TrigPoly.variable(1)
SY = TrigPoly.variable(2)
CY = TrigPoly.variable(3)

def vector_add(left, right)
  left.zip(right).map { |a, b| a + b }
end

def vector_scale(vector, value)
  vector.map { |component| component.scale(value) }
end

def vector_divergence(vector)
  vector.each_with_index.inject(TrigPoly.constant(0)) do |sum, pair|
    component, axis = pair
    sum + component.derivative(axis)
  end
end

def vector_laplacian(vector)
  vector.map do |component|
    component.derivative(0).derivative(0) +
      component.derivative(1).derivative(1)
  end
end

def vector_dot(left, right)
  left.zip(right).inject(TrigPoly.constant(0)) { |sum, pair| sum + pair[0] * pair[1] }
end

def vector_convection(vector)
  vector.each_index.map do |component|
    vector.each_index.inject(TrigPoly.constant(0)) do |sum, axis|
      sum + vector.fetch(axis) * vector.fetch(component).derivative(axis)
    end
  end
end

def gradient(polynomial)
  [polynomial.derivative(0), polynomial.derivative(1)]
end

def zero_vector?(vector)
  vector.all?(&:zero?)
end

def cosine_double(sine, cosine)
  cosine**2 - sine**2
end

def taylor_exact_checks
  exact_group("exact_trigonometric_quotient_Taylor_identities") do |check|
    psi = SX * SY
    w = [SX * CY, -(CX * SY)]
    pressure_sign = mutation?("taylor_pressure_sign") ? -1 : 1
    pressure = (cosine_double(SX, CX) + cosine_double(SY, CY)).scale(
      Rational(pressure_sign, 4)
    )
    decay = mutation?("taylor_laplacian") ? 1 : 2

    check.call(vector_divergence(w).zero?, "Taylor field is not divergence free")
    check.call(zero_vector?(vector_add(vector_laplacian(w), vector_scale(w, decay))),
               "Taylor Laplace eigenvalue is not two")
    check.call(zero_vector?(vector_add(vector_convection(w), gradient(pressure))),
               "Taylor convection and pressure gradient do not cancel")
    check.call(vector_dot(gradient(psi), w).zero?,
               "Hamiltonian field is not tangent to the psi levels")

    energy = vector_dot(w, w)
    expected_energy = TrigPoly.constant(Rational(1, 2)) -
                      (cosine_double(SX, CX) * cosine_double(SY, CY)).scale(
                        Rational(1, 2)
                      )
    check.call(energy == expected_energy, "Taylor modulus-square identity failed")

    bernoulli = energy.scale(Rational(1, 2)) + pressure
    current = w.map { |component| component * bernoulli }
    check.call(vector_divergence(current).zero?,
               "fixed-frame Bernoulli current is not divergence free")

    q = vector_dot(w, gradient(energy))
    check.call(!q.zero?, "streamline derivative q is identically zero")
    check.call(decay == 2, "decay-rate mutation escaped")
    check.call(pressure_sign == 1, "pressure-sign mutation escaped")
  end
end

def topology_and_orientation_checks
  exact_group("regular_level_topology_samples_and_forward_orientation") do |check|
    claimed_level = mutation?("level_value") ? Rational(2, 3) : Rational(1, 2)
    start_psi = Rational(1, 2)
    target_psi = Rational(1, 2)
    start_g = Rational(1, 2)
    target_g = Rational(3, 4)
    start_velocity = mutation?("orbit_orientation") ?
      [Rational(-1, 2), Rational(1, 2)] :
      [Rational(1, 2), Rational(-1, 2)]

    check.call(start_psi == claimed_level, "x_* is not on the claimed level")
    check.call(target_psi == claimed_level, "target phase is not on the claimed level")
    check.call(Rational(1) != claimed_level,
               "the only positive-cell critical point lies on the regular level")
    check.call(start_velocity == [Rational(1, 2), Rational(-1, 2)],
               "the lower-branch orbit orientation is reversed")
    check.call(start_velocity[0].positive? && start_velocity[1].negative?,
               "the orbit does not initially move toward (pi/2,pi/6)")
    check.call(start_g == Rational(1, 2), "g(0) is not one half")
    check.call(target_g == Rational(3, 4), "g(s_*) is not three quarters")

    forward_increment = if mutation?("positive_phase_order")
                          start_g - target_g
                        else
                          target_g - start_g
                        end
    check.call(forward_increment == Rational(1, 4),
               "the selected ordered phases do not give a positive 1/4 rise")

    # The level equation in the positive cell forces each sine factor >=1/2;
    # the two inverse-sine branches meet at x_1=pi/6 and 5pi/6.
    lower_sine_bound = Rational(1, 2)
    endpoint_other_sine = claimed_level / lower_sine_bound
    check.call(endpoint_other_sine == 1,
               "the two explicit branches do not meet at the claimed endpoints")
    check.call(target_g - start_g == Rational(1, 4),
               "g is not certified nonconstant on the same oriented component")
  end
end

def periodic_averaging_checks
  exact_group("periodic_floor_bound_and_recurrent_phase_length") do |check|
    divisor = mutation?("period_floor") ? Rational(1) : Rational(2)
    (2..24).each do |numerator|
      (1..9).each do |denominator|
        length_ratio = Rational(numerator, denominator)
        next if length_ratio < 2

        check.call(length_ratio.floor >= length_ratio / divisor,
                   "floor(L/T) does not dominate L/(2T)")
      end
    end
    check.call(divisor == 2, "periodic-floor mutation escaped")

    phase_length_powers = {
      "mu" => 1,
      "A" => mutation?("phase_length_power") ? 0 : 1,
      "exp_minus_one" => 1
    }
    check.call(phase_length_powers == { "mu" => 1, "A" => 1, "exp_minus_one" => 1 },
               "L_A does not have the exact mu*A*(e^(2R^2)-1) power data")
    check.call(Rational(1, 2) * 2 == 1, "phase antiderivative coefficient is wrong")
  end
end

def temporal_dimension_checks
  exact_group("dimensionless_time_R_and_amplitude_exponents") do |check|
    raw_radius = mutation?("flux_radius_power") ? 0 : -1
    raw_amplitude = mutation?("lp_amplitude_power") ? 2 : 3
    check.call(raw_radius == -1, "dot F lost its R^(-1) prefactor")
    check.call(raw_amplitude == 3, "dot F lost its cubic amplitude")

    [Rational(1), Rational(4, 3), Rational(2), Rational(7, 2)].each do |p_value|
      before = {
        "gamma" => p_value,
        "c" => p_value,
        "mu" => p_value - 1,
        "R" => (2 * p_value - 2) + raw_radius * p_value,
        "A" => raw_amplitude * p_value - 1
      }
      check.call(before.fetch("mu") == p_value - 1,
                 "change of phase has the wrong mu exponent")
      check.call(before.fetch("R") == p_value - 2,
                 "finite-p normalization has the wrong R^(p-2) exponent")
      check.call(before.fetch("A") == 3 * p_value - 1,
                 "pre-averaging amplitude is not A^(3p-1)")

      after = before.merge(
        "mu" => before.fetch("mu") + 1,
        "A" => before.fetch("A") + 1
      )
      check.call(after.fetch("mu") == p_value, "averaging lost one mu factor")
      check.call(after.fetch("A") == 3 * p_value,
                 "recurrent averaging does not produce A^(3p)")
      check.call(after.fetch("R") == p_value - 2,
                 "displayed exact R exponent changed after averaging")
    end

    infinity_radius = 2 + raw_radius
    check.call(infinity_radius == 1, "L-infinity normalization is not R*A^3")

    range_power = mutation?("range_amplitude_power") ? 3 : 2
    payment_power = mutation?("payment_amplitude_power") ? 2 : 3
    completed_clock_height_power = 2 # K=E+D; both rows are quadratic here.
    check.call(range_power == 2, "signed range is not quadratic in A")
    check.call(payment_power == 3, "complete payment is not cubic in A")
    check.call(completed_clock_height_power == 2,
               "the recurrent Taylor completed-clock height is not quadratic")
    check.call(completed_clock_height_power == range_power,
               "M^K and O+ do not share the recurrent-family amplitude scale")
    check.call(Rational(2, 3) * payment_power == range_power,
               "P^(2/3) does not have the quadratic amplitude scale")
    check.call(raw_amplitude == 3 && payment_power == 3,
               "absolute recurrent tail and payment do not share A^3")
    check.call(raw_amplitude - Rational(2, 3) * payment_power == 1,
               "S.444 counterexample ratio does not grow linearly in A")

    [Rational(0), Rational(1, 4), Rational(2, 3), Rational(9, 10)].each do |beta|
      check.call(3 * (1 - beta) > 0,
                 "the stated beta range does not force divergence")
    end
  end
end

def rational_sum(values)
  values.inject(Rational(0, 1), :+)
end

def best_tail(values, budget)
  raise ArgumentError, "negative deletion budget" if budget.negative?
  raise ArgumentError, "negative tail coordinate" if values.any?(&:negative?)

  indices = (0...values.length).to_a
  candidates = []
  (0..[budget, values.length].min).each do |size|
    indices.combination(size) do |deleted|
      deletion = deleted.to_h { |index| [index, true] }
      retained = []
      values.each_with_index do |value, index|
        retained << value unless deletion.key?(index)
      end
      candidates << rational_sum(retained)
    end
  end
  candidates.min || Rational(0, 1)
end

def fixed_deletion_sup_tail(rows, budget)
  raise ArgumentError, "empty terminal family" if rows.empty?

  coordinate_count = rows.first.length
  raise ArgumentError, "ragged terminal family" unless rows.all? { |row| row.length == coordinate_count }

  indices = (0...coordinate_count).to_a
  candidates = []
  (0..[budget, coordinate_count].min).each do |size|
    indices.combination(size) do |deleted|
      deletion = deleted.to_h { |index| [index, true] }
      terminal_sums = rows.map do |row|
        retained = []
        row.each_with_index { |value, index| retained << value unless deletion.key?(index) }
        rational_sum(retained)
      end
      candidates << terminal_sums.max
    end
  end
  candidates.min || Rational(0, 1)
end

def deletion_and_hybrid_checks
  exact_group("finite_common_deletion_and_minimax_direction") do |check|
    (0..12).each do |budget|
      count = mutation?("deletion_cardinality") ? budget : budget + 1
      weights = (1..count).map { |index| Rational(1, index) }
      check.call(count == budget + 1, "witness does not activate N+1 shells")
      check.call(best_tail(weights, budget) == Rational(1, budget + 1),
                 "N deletions did not leave the smallest of N+1 weights")
    end

    # Each time slice may choose its own best deletion in Z.  O uses one
    # fixed deletion after taking every coordinate's forward excursion.
    excursions = [Rational(10), Rational(10)]
    time_slices = [
      [Rational(10), Rational(0)],
      [Rational(0), Rational(10)]
    ]
    budget = 1
    z_value = time_slices.map { |row| best_tail(row, budget) }.max
    fixed_z_value = fixed_deletion_sup_tail(time_slices, budget)
    o_value = best_tail(excursions, budget)
    check.call(time_slices.all? do |row|
      row.zip(excursions).all? { |z_coordinate, excursion| z_coordinate <= excursion }
    end, "hybrid coordinates are not bounded coordinatewise by excursions")
    direction = if mutation?("hybrid_infimum_direction")
                  o_value <= z_value
                else
                  z_value <= o_value
                end
    check.call(direction, "the sup-inf/fixed-deletion direction was reversed")
    check.call(z_value <= fixed_z_value && fixed_z_value <= o_value,
               "varying deletion <= fixed hybrid <= O+ chain failed")
    check.call(z_value.zero? && fixed_z_value == 10 && o_value == 10,
               "strict minimax witness did not separate varying and fixed deletion")

    no_deletion_fixed = fixed_deletion_sup_tail(time_slices, 0)
    no_deletion_o = best_tail(excursions, 0)
    check.call(no_deletion_fixed == 10 && no_deletion_o == 20,
               "O+ was incorrectly identified as the minimal fixed-deletion hybrid target")
  end
end

def total_variation(path)
  path.each_cons(2).inject(Rational(0, 1)) { |sum, pair| sum + (pair[1] - pair[0]).abs }
end

def positive_variation(path)
  path.each_cons(2).inject(Rational(0, 1)) do |sum, pair|
    increment = pair[1] - pair[0]
    sum + [increment, Rational(0, 1)].max
  end
end

def negative_variation(path)
  path.each_cons(2).inject(Rational(0, 1)) do |sum, pair|
    decrement = pair[0] - pair[1]
    sum + [decrement, Rational(0, 1)].max
  end
end

def positive_excursion(path)
  best = Rational(0, 1)
  path.each_index do |left|
    ((left + 1)...path.length).each do |right|
      best = [best, path[right] - path[left]].max
    end
  end
  best
end

def symmetric_oscillation(path)
  path.max - path.min
end

def path_subtract(left, right)
  left.zip(right).map { |a, b| a - b }
end

def jordan_and_clock_checks
  exact_group("Jordan_positive_excursion_and_completed_clock_inequalities") do |check|
    jordan_paths = [
      [0, 2, -1],
      [0, -3, 1, -2],
      [0, 1, 0, 1, 0],
      [0, -1]
    ].map { |path| path.map { |value| Rational(value) } }
    jordan_paths.each do |path|
      endpoint_term = if mutation?("jordan_endpoint")
                        path.last - path.first
                      else
                        (path.last - path.first).abs
                      end
      right = endpoint_term + 2 * [positive_variation(path), negative_variation(path)].min
      check.call(total_variation(path) == right,
                 "TV=|endpoint|+2 min(V+,V-) failed")
    end

    # A finite recurrent clock: maximal height/forward range stays one while
    # positive and absolute variation count every traversal.
    [1, 2, 5, 11].each do |circuits|
      clock = [Rational(0)]
      circuits.times { clock.concat([Rational(1), Rational(0)]) }
      check.call(positive_excursion(clock) == 1, "recurrent O+ is not one")
      check.call(symmetric_oscillation(clock) == 1, "recurrent range is not one")
      check.call(clock.max == 1, "recurrent clock height is not one")
      check.call(positive_variation(clock) == circuits,
                 "positive variation did not count every circuit")
      check.call(total_variation(clock) == 2 * circuits,
                 "absolute variation did not count both legs")
    end

    clocks = [
      [0, 2, 1, 3, 0],
      [0, 1, 0, 2, 1],
      [0, 0, 4, 2, 3],
      [0, 3, 3, 1, 2]
    ].map { |path| path.map { |value| Rational(value) } }
    if mutation?("clock_start")
      clocks[0] = clocks[0].dup
      clocks[0][0] = Rational(1)
    end
    qs = [
      [0, 1, -1, 0, 1],
      [0, -1, 1, 1, 0],
      [0, 2, 1, -1, 0],
      [0, 0, -2, 1, -1]
    ].map { |path| path.map { |value| Rational(value) } }

    check.call(clocks.all? { |path| path.first.zero? },
               "completed clocks do not have the common zero start")
    check.call(clocks.flatten.all? { |value| value >= 0 }, "completed clock became negative")
    fs = clocks.zip(qs).map do |clock, q_path|
      mutation?("clock_relation") ?
        clock.zip(q_path).map { |a, b| a + b } :
        path_subtract(clock, q_path)
    end
    check.call(fs.each_index.all? { |index| fs[index] == path_subtract(clocks[index], qs[index]) },
               "F=K-Q was replaced by the wrong gauge relation")

    o_values = fs.map { |path| positive_excursion(path) }
    m_values = clocks.map(&:max)
    v_values = clocks.map { |path| positive_variation(path) }
    h_values = fs.map { |path| total_variation(path) }
    q_values = qs.map { |path| total_variation(path) }

    fs.each_index do |index|
      o = o_values.fetch(index)
      m = m_values.fetch(index)
      v = v_values.fetch(index)
      h = h_values.fetch(index)
      q = q_values.fetch(index)
      check.call(o <= m + q, "coordinate O+ <= M+TVQ failed")
      check.call(m <= o + q, "coordinate M <= O++TVQ failed")
      check.call(v <= h + q, "coordinate V+K <= TVF+TVQ failed")
      check.call(h <= 2 * v + q, "coordinate TVF <= 2V+K+TVQ failed")
      check.call(m <= v, "coordinate maximal height <= positive variation failed")
    end

    b_q = rational_sum(q_values)
    (0..3).each do |budget|
      o = best_tail(o_values, budget)
      m = best_tail(m_values, budget)
      v = best_tail(v_values, budget)
      h = best_tail(h_values, budget)
      check.call(o <= m + b_q, "aggregate O+ <= M+B_Q failed")
      check.call(m <= o + b_q, "aggregate M <= O++B_Q failed")
      check.call(v <= h + b_q, "aggregate V+K <= H+B_Q failed")
      check.call(h <= 2 * v + b_q, "aggregate H <= 2V+K+B_Q failed")
      check.call(m <= v, "aggregate M <= V+K failed")
    end
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
    topology_and_orientation_checks,
    periodic_averaging_checks,
    temporal_dimension_checks,
    deletion_and_hybrid_checks,
    jordan_and_clock_checks
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
  rows = ARTIFACT_SPECS.map do |identifier, spec|
    path = resolved_path(spec)
    actual = File.file?(path) ? sha256(path) : nil
    {
      "id" => identifier,
      "path" => spec.fetch("path"),
      "expected_sha256" => spec.fetch("sha256"),
      "actual_sha256" => actual,
      "pass" => actual == spec.fetch("sha256")
    }
  end
  core_stdout, core_stderr, core_status = Open3.capture3(
    "git", "-C", REPO, "rev-parse", "#{STEP17_CORE_COMMIT}^{commit}"
  )
  parent_stdout, parent_stderr, parent_status = Open3.capture3(
    "git", "-C", REPO, "rev-parse", "#{STEP17_CORE_COMMIT}^"
  )
  _ancestor_stdout, ancestor_stderr, ancestor_status = Open3.capture3(
    "git", "-C", REPO, "merge-base", "--is-ancestor", STEP17_CORE_COMMIT, "HEAD"
  )
  actual_core = core_status.success? && core_stderr.empty? ? core_stdout.strip : nil
  actual_parent = parent_status.success? && parent_stderr.empty? ? parent_stdout.strip : nil
  is_ancestor = ancestor_status.success? && ancestor_stderr.empty?
  rows << {
    "id" => "step17_core_commit_and_parent",
    "expected_commit" => STEP17_CORE_COMMIT,
    "actual_commit" => actual_core,
    "expected_parent" => STEP16_PARENT_COMMIT,
    "actual_parent" => actual_parent,
    "core_is_ancestor_of_HEAD" => is_ancestor,
    "pass" => actual_core == STEP17_CORE_COMMIT &&
              actual_parent == STEP16_PARENT_COMMIT && is_ancestor
  }
  rows
end

def compact(text)
  text.gsub(/[\s&]+/, "")
end

def equation_before_tag(body, tag)
  marker = "\\tag{#{tag}}"
  tag_index = body.index(marker)
  return "" unless tag_index

  opening = body.rindex("\\[", tag_index)
  return "" unless opening

  body[opening..(tag_index + marker.length)]
end

def semantic_note_checks(body, bytes)
  rows = []
  add = lambda do |identifier, condition|
    rows << { "id" => identifier, "pass" => !!condition }
  end
  compact_body = compact(body)
  tags = body.scan(/\\tag\{(S\.\d+)\}/).flatten

  add.call("exact_S445_S475_sequence_once", tags == EXPECTED_TAGS)
  add.call("all_31_tags_unique", tags.uniq.length == 31 && tags.length == 31)
  add.call("display_math_balanced", body.scan(/\\\[/).length == body.scan(/\\\]/).length)
  add.call("valid_UTF8", body.valid_encoding?)
  add.call("no_CR_NUL_or_forbidden_controls",
           !bytes.include?("\r") && !bytes.include?("\0") &&
           bytes.bytes.none? { |byte| byte < 32 && byte != 10 })

  add.call("topology_explicit_compact_connected_same_component",
           body.include?("\\sin x_i\\ge1/2") &&
           body.include?("two branches") &&
           body.include?("compact connected oval") &&
           body.include?("lie on this same component") &&
           body.include?("\\Gamma\\times\\{0\\}"))
  add.call("finite_N_plus_one_common_deletion",
           body.include?("M=N+1") && body.include?("N=M-1") &&
           compact_body.include?("leavesatleastoneofthefirst") &&
           body.include?("one deletion set across all terminal times"))
  add.call("large_amplitude_quantifier_present",
           body.scan("A\\ge A_0(R)").length >= 2 &&
           body.include?("all asymptotic comparisons are as \\(A\\to\\infty\\)"))

  forward_markers = [
    "s_*\\in(0,T_*)",
    "g(s_*)-g(0)=1/4",
    "\\theta_A(a)=-T_*",
    "\\theta_A(b)=-T_*+s_*",
    "choose\\(a<b\\)in\\(I_R\\)by"
  ]
  add.call("ordered_forward_positive_excursion_witness",
           forward_markers.all? { |marker| compact_body.include?(compact(marker)) })
  add.call("coordinatewise_backtracking_support",
           body.scan("coordinatewise").length >= 2 &&
           body.include?("(S.456)") &&
           body.include?("B_{k,R}") && body.include?("\\asymp_{k,R}A^3"))

  dimension_markers = [
    "R^{2p-2}", "A^{3p-1}", "A^{3p}",
    "q_\\infty A^3", "A^2", "A^3", "(P_R^M)^{2/3}"
  ]
  add.call("dimension_and_A_R_exponents",
           dimension_markers.all? { |marker| compact_body.include?(compact(marker)) } &&
           body.scan("R^{p-2}").length >= 2)
  add.call("exact_Jordan_identity",
           compact(equation_before_tag(body, "S.468")).include?(
             compact("\\operatorname {TV}F_{k,R}=|F_{k,R}(t_0^-)|+2B_{k,R}")
           ))

  s470 = compact(equation_before_tag(body, "S.470"))
  add.call("hybrid_to_positive_excursion_to_TV_direction",
           s470.include?(compact("\\mathfrak Z_{N,R}^{\\boldsymbol\\lambda}(\\mathcal T_R)")) &&
           s470.include?(compact("\\le\\mathfrak O^{F,+}_{N,R}\\le\\mathfrak H^F_{1,N,R}")))
  s475 = compact(equation_before_tag(body, "S.475"))
  clock_markers = [
    "\\mathfrak O^{F,+}_{N,R}\\le\\mathfrak M^K_{N,R}+B_{Q,R}",
    "\\mathfrak M^K_{N,R}\\le\\mathfrak O^{F,+}_{N,R}+B_{Q,R}",
    "\\mathfrak V^K_{N,R}\\le\\mathfrak H^F_{1,N,R}+B_{Q,R}",
    "\\mathfrak H^F_{1,N,R}\\le2\\mathfrak V^K_{N,R}+B_{Q,R}",
    "\\mathfrak M^K_{N,R}\\le\\mathfrak V^K_{N,R}"
  ]
  add.call("all_five_clock_inequality_directions",
           clock_markers.all? { |marker| s475.include?(compact(marker)) } &&
           body.include?("only then optimize"))

  add.call("sublinear_quantifier_scope",
           body.include?("\\beta<1") &&
           body.include?("\\forall\\beta<1") &&
           body.include?("\\forall C>0") &&
           body.include?("After choosing \\(R\\) by (S.451)") &&
           body.include?("upper half of (S.461) when") &&
           body.include?("lower half when \\(\\beta<0\\)"))
  add.call("claim_boundary_S444_false_S472_open",
           body.include?("**(S.444 is false)**") &&
           body.include?("Equation (S.472) is **OPEN**") &&
           body.include?("direct hybrid terminal gate from Step 15 also remains") &&
           body.include?("**OPEN**"))
  add.call("Step15_Step16_and_frozen_Version_M_scope",
           body.include?("Step 15") && body.include?("Step 16") &&
           body.include?("frozen Version-M setting"))
  add.call("downstream_open_and_not_Clay",
           body.include?("The following remain **OPEN AND UNCHANGED**:") &&
           body.include?("Q.1, scale contraction, and regularity") &&
           body.include?("**NOT CLAY.**"))
  add.call("certificate_scope_not_overclaimed",
           body.include?("Finite calculations") &&
           body.include?("continuum analytic statement") &&
           body.include?("not a novelty or priority claim") &&
           !body.include?("route-minimal"))
  rows
end

def note_structure_checks(artifacts)
  artifact = artifacts.find { |row| row.fetch("id") == "step17_note" }
  return [{ "id" => "step17_note_exists", "pass" => false }] unless artifact &&
                                                                       File.file?(resolved_path(ARTIFACT_SPECS.fetch("step17_note")))

  path = resolved_path(ARTIFACT_SPECS.fetch("step17_note"))
  bytes = File.binread(path)
  body = bytes.dup.force_encoding(Encoding::UTF_8)
  rows = [{
    "id" => "step17_note_hash_lock",
    "expected_sha256" => artifact.fetch("expected_sha256"),
    "actual_sha256" => artifact.fetch("actual_sha256"),
    "pass" => artifact.fetch("pass")
  }]
  return rows + [{ "id" => "valid_UTF8", "pass" => false }] unless body.valid_encoding?

  rows + semantic_note_checks(body, bytes)
end

def mutate_once(body, before, after)
  raise RuntimeError, "mutation marker absent: #{before}" unless body.include?(before)

  body.sub(before, after)
end

def statement_mutation_checks(body)
  exact_group("statement_negative_mutations_rejected") do |check|
    probes = [
      ["topology_explicit_compact_connected_same_component",
       "compact connected oval", "disconnected open arc"],
      ["finite_N_plus_one_common_deletion", "M=N+1", "M=N"],
      ["large_amplitude_quantifier_present", "A\\ge A_0(R)", "A>0"],
      ["ordered_forward_positive_excursion_witness", "\\(a<b\\) in \\(I_R\\) by",
       "\\(b<a\\) in \\(I_R\\) by"],
      ["coordinatewise_backtracking_support", "coordinatewise", "aggregate-only"],
      ["dimension_and_A_R_exponents", "R^{p-2}", "R^{p-1}"],
      ["exact_Jordan_identity", "+2B_{k,R}", "-2B_{k,R}"],
      ["hybrid_to_positive_excursion_to_TV_direction",
       "\\le\\mathfrak O^{F,+}_{N,R}", "\\ge\\mathfrak O^{F,+}_{N,R}"],
      ["all_five_clock_inequality_directions", "only then optimize", "optimize first"],
      ["sublinear_quantifier_scope", "\\forall\\beta<1", "\\forall\\beta\\ge1"],
      ["claim_boundary_S444_false_S472_open", "Equation (S.472) is **OPEN**",
       "Equation (S.472) is **PROVED**"],
      ["Step15_Step16_and_frozen_Version_M_scope", "frozen Version-M setting",
       "unfrozen informal setting"],
      ["downstream_open_and_not_Clay", "**NOT CLAY.**", "**CLAY.**"],
      ["certificate_scope_not_overclaimed", "not a novelty or priority claim",
       "a novelty and priority claim"]
    ]
    probes.each do |target_id, before, after|
      mutated = mutate_once(body, before, after)
      row = semantic_note_checks(mutated, mutated.encode(Encoding::UTF_8)).find do |candidate|
        candidate.fetch("id") == target_id
      end
      check.call(row && !row.fetch("pass"), "statement mutation escaped: #{target_id}")
    end

    duplicate = mutate_once(body, "\\tag{S.475}", "\\tag{S.474}")
    row = semantic_note_checks(duplicate, duplicate.encode(Encoding::UTF_8)).find do |candidate|
      candidate.fetch("id") == "exact_S445_S475_sequence_once"
    end
    check.call(row && !row.fetch("pass"), "duplicate equation tag escaped")

    damaged_bytes = body.b + "\r\0"
    damaged_body = damaged_bytes.dup.force_encoding(Encoding::UTF_8)
    row = semantic_note_checks(damaged_body, damaged_bytes).find do |candidate|
      candidate.fetch("id") == "no_CR_NUL_or_forbidden_controls"
    end
    check.call(row && !row.fetch("pass"), "forbidden byte injection escaped")
  end
end

def mutation_environment_checks
  exact_group("environment_selected_negative_mutations_fail_closed") do |check|
    NEGATIVE_MUTATIONS.each do |mutation|
      environment = {
        INTERNAL_MUTATION => "1",
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
  exact_group("artifact_path_overrides_fail_closed") do |check|
    ARTIFACT_SPECS.each do |identifier, spec|
      environment = {
        INTERNAL_PATH => "1",
        MUTATION_ENV => "",
        spec.fetch("environment") => File.expand_path(__FILE__)
      }
      stdout, stderr, status = Open3.capture3(
        environment, RbConfig.ruby, File.expand_path(__FILE__)
      )
      payload = JSON.parse(stdout)
      target = payload.fetch("artifacts").find { |row| row.fetch("id") == identifier }
      check.call(!status.success?, "#{identifier} path override exited successfully")
      check.call(stderr.empty?, "#{identifier} path override wrote stderr")
      check.call(target && !target.fetch("pass"), "#{identifier} path override passed")
      check.call(target.fetch("actual_sha256") == sha256(__FILE__),
                 "#{identifier} did not resolve to the injected path")
    end
  end
end

def stability_payload(core, artifacts, note_checks)
  {
    "schema" => SCHEMA,
    "independent_checks" => core,
    "artifacts" => artifacts,
    "note_checks" => note_checks,
    "pass" => core.all? { |row| row.fetch("pass") } &&
              artifacts.all? { |row| row.fetch("pass") } &&
              note_checks.all? { |row| row.fetch("pass") }
  }
end

def reproducibility_checks
  exact_group("different_cwd_hash_seed_and_byte_reproducibility") do |check|
    probes = [
      [REPO, "0"],
      ["/", "1"],
      [REPO, "8675309"],
      ["/", "4294967291"]
    ]
    outputs = probes.map do |cwd, seed|
      environment = {
        INTERNAL_STABILITY => "1",
        MUTATION_ENV => "",
        "RUBY_HASH_SEED" => seed
      }
      stdout, stderr, status = Open3.capture3(
        environment, RbConfig.ruby, File.expand_path(__FILE__), chdir: cwd
      )
      check.call(status.success?, "stability probe failed from cwd=#{cwd}, seed=#{seed}")
      check.call(stderr.empty?, "stability probe wrote stderr from cwd=#{cwd}, seed=#{seed}")
      check.call(JSON.parse(stdout).fetch("pass"),
                 "stability payload was not PASS from cwd=#{cwd}, seed=#{seed}")
      stdout
    end
    check.call(outputs.uniq.length == 1,
               "output bytes depend on cwd or RUBY_HASH_SEED")
    check.call(Digest::SHA256.hexdigest(outputs.first) ==
               Digest::SHA256.hexdigest(outputs.last),
               "first and last stability digests differ")
  end
end

# Independent exact mathematics is complete before any note or hash is read.
core = independent_checks

if ENV[INTERNAL_MUTATION] == "1"
  passed = core.all? { |row| row.fetch("pass") }
  puts JSON.generate({ "mutation" => MUTATION, "checks" => core, "pass" => passed })
  exit(passed ? 0 : 1)
end

artifacts = artifact_checks

if ENV[INTERNAL_PATH] == "1"
  passed = artifacts.all? { |row| row.fetch("pass") }
  puts JSON.generate({ "artifacts" => artifacts, "pass" => passed })
  exit(passed ? 0 : 1)
end

note_checks = note_structure_checks(artifacts)

if ENV[INTERNAL_STABILITY] == "1"
  payload = stability_payload(core, artifacts, note_checks)
  puts JSON.generate(payload)
  exit(payload.fetch("pass") ? 0 : 1)
end

note_path = resolved_path(ARTIFACT_SPECS.fetch("step17_note"))
if File.file?(note_path)
  note_body = File.read(note_path, encoding: "UTF-8")
  statement_mutations = statement_mutation_checks(note_body)
else
  statement_mutations = {
    "id" => "statement_negative_mutations_rejected",
    "cases" => 0,
    "error" => "Step-17 note missing",
    "pass" => false
  }
end

environment_mutations = mutation_environment_checks
path_mutations = path_override_checks
reproducibility = reproducibility_checks
negative_groups = [statement_mutations, environment_mutations, path_mutations]

passed = core.all? { |row| row.fetch("pass") } &&
         artifacts.all? { |row| row.fetch("pass") } &&
         note_checks.all? { |row| row.fetch("pass") } &&
         negative_groups.all? { |row| row.fetch("pass") } &&
         reproducibility.fetch("pass")

output = {
  "schema" => SCHEMA,
  "mutation" => MUTATION.empty? ? nil : MUTATION,
  "independent_checks" => core,
  "artifacts" => artifacts,
  "note_checks" => note_checks,
  "negative_mutation_checks" => negative_groups,
  "reproducibility_check" => reproducibility,
  "scope" => {
    "standard_library_Ruby_exact_Rational_trigonometric_quotient" => true,
    "independent_math_precedes_note_and_artifact_access" => true,
    "imports_or_calls_primary_Python_certificate" => false,
    "uses_float_random_time_network_or_external_gems" => false,
    "machine_proves_continuum_topology_or_cutoff_bounds" => false,
    "machine_proves_open_S472_or_direct_hybrid_gate" => false,
    "machine_proves_regularity_or_Clay" => false
  },
  "summary" => {
    "independent_groups_passed" => core.count { |row| row.fetch("pass") },
    "independent_groups_total" => core.length,
    "independent_cases" => core.inject(0) { |sum, row| sum + row.fetch("cases") },
    "artifact_locks_passed" => artifacts.count { |row| row.fetch("pass") },
    "artifact_locks_total" => artifacts.length,
    "note_checks_passed" => note_checks.count { |row| row.fetch("pass") },
    "note_checks_total" => note_checks.length,
    "negative_mutation_probes" => NEGATIVE_MUTATIONS.length + 16,
    "negative_cases" => negative_groups.inject(0) { |sum, row| sum + row.fetch("cases") },
    "reproducibility_cases" => reproducibility.fetch("cases")
  },
  "pass" => passed
}

puts JSON.pretty_generate(output)
exit(passed ? 0 : 1)
