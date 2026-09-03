#!/usr/bin/env ruby
# Independent exact verifier for frozen R0.75H.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075h_single_pass_transport_flux_closure.md'
PRIMARY_AUDIT = ROOT + 'research/r075h_single_pass_transport_flux_closure_primary_audit.md'
REPORT_SOURCE = ROOT + 'research/r075h_report-source.md'
FIXTURES = ROOT + 'scripts/r075h_single_pass_transport_flux_closure_fixtures.json'
EXPECTED = ROOT + 'scripts/r075h_single_pass_transport_flux_closure_expected.json'
JSON_PATH = Pathname.new(
  ENV.fetch(
    'R075H_JSON',
    (ROOT + 'research/r075h_single_pass_transport_flux_closure_certificate.json').to_s
  )
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075H_RUBY_REPORT',
    (ROOT + 'research/r075h_single_pass_transport_flux_closure_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075H_RUBY_MUTATION', '')
SCHEMA = 'r075h-single-pass-transport-flux-closure-certificate-v1'

FROZEN_SOURCES = {
  'research/r075b_bulk_clock_outer_padding_gate.md' =>
    '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075f_modal_phase_integration_identity.md' =>
    'f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440',
  'research/r075g_signed_flux_gain_threshold.md' =>
    'f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41',
  'research/r075h_report-source.md' =>
    '5b0b05b2ce903986ef8439a766766e8bdb97e2fe4d9eb6035f73102583b1b779',
  'research/r075h_single_pass_transport_flux_closure.md' =>
    '849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9',
  'research/r075h_single_pass_transport_flux_closure_primary_audit.md' =>
    '3c85368e051102997e66ae36fa43290b6200e688db886380215fb40ec0bb757e'
}.freeze
FIXTURES_SHA256 = '7e4b5691d6929c97f72146c293a55e3b6fcf5875bc51f78bd1a58e9f84a0b217'
EXPECTED_SHA256 = '099d017cb7ff61d5a9dff54449c9a91a12e8657343bb11579ad135e9cd350573'

NEGATIVE_MUTATIONS = %w[
  source_drift audit_drift report_source_drift dependency_drift
  dependency_table_missing fixture_drift expected_drift tag reference display
  control transport_pde_sign transport_energy_sign eta_initial eta_terminal
  eta_monotone eta_plateau eta_ibp_sign transport_half characteristic_direction
  set_translation_direction q_shift terminal_containment seam_crossing
  terminal_l2 persistence_direction persistence_time holder_measure
  holder_delta_power holder_volume_power holder_l3_power holder_division
  h23_flux_r h23_flux_omega h23_delta_r h23_volume_l h23_volume_r
  h23_cubic_r h23_cubic_omega h23_cubic_p rate_rho_sign rate_cgamma_sign
  rate_fraction matching_lower_direction matching_r_power matching_cube_root
  diff_terminal_sign diff_dissipation_sign diff_cutoff_sign diff_circularity
  atom_r_sign atom_omega_sign flux_normalization measurement_weight
  benchmark_nse conditional_weight payment_region transport_absolute_flux
  block_count diffusive_characteristic e24_closed complete_clock fixed_deletion
  suitable_weak regularity clay
].freeze

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  abort("unknown R075H_RUBY_MUTATION: #{MUTATION}")
end

def rational(value)
  Rational(value.to_s)
end

def rational_text(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

def vector_add(vectors)
  keys = vectors.flat_map(&:keys).uniq.sort
  keys.to_h do |key|
    [key, vectors.sum { |vector| vector.fetch(key, Rational(0)) }]
  end
end

def vector_text(vector)
  vector.to_h { |key, value| [key, rational_text(value)] }
end

def contained?(inner, outer)
  outer[0] <= inner[0] && inner[0] <= inner[1] && inner[1] <= outer[1]
end

# Exact bivariate polynomials in (x,t), kept separate from the Python
# implementation and evaluated only with Ruby Rational arithmetic.
def polynomial_clean(polynomial)
  polynomial.reject { |_power, coefficient| coefficient.zero? }
end

def polynomial_add(*polynomials)
  result = Hash.new(Rational(0))
  polynomials.each do |polynomial|
    polynomial.each { |power, coefficient| result[power] += coefficient }
  end
  polynomial_clean(result)
end

def polynomial_scale(polynomial, scale)
  polynomial_clean(polynomial.to_h do |power, coefficient|
    [power, coefficient * scale]
  end)
end

def polynomial_multiply(left, right)
  result = Hash.new(Rational(0))
  left.each do |(left_x, left_t), left_coefficient|
    right.each do |(right_x, right_t), right_coefficient|
      result[[left_x + right_x, left_t + right_t]] +=
        left_coefficient * right_coefficient
    end
  end
  polynomial_clean(result)
end

def polynomial_power(polynomial, exponent)
  (1..exponent).reduce({[0, 0] => Rational(1)}) do |product, _index|
    polynomial_multiply(product, polynomial)
  end
end

def polynomial_derivative(polynomial, variable)
  result = Hash.new(Rational(0))
  polynomial.each do |power, coefficient|
    next if power[variable].zero?

    reduced = power.dup
    multiplier = reduced[variable]
    reduced[variable] -= 1
    result[reduced] += coefficient * multiplier
  end
  polynomial_clean(result)
end

def polynomial_integrate_x(polynomial, lower, upper)
  result = Hash.new(Rational(0))
  polynomial.each do |(x_power, t_power), coefficient|
    next_power = x_power + 1
    result[[0, t_power]] += coefficient *
      (upper**next_power - lower**next_power) / next_power
  end
  polynomial_clean(result)
end

def polynomial_integrate_t(polynomial, lower, upper)
  polynomial.sum do |(x_power, t_power), coefficient|
    raise 'x was not integrated' unless x_power.zero?

    next_power = t_power + 1
    coefficient * (upper**next_power - lower**next_power) / next_power
  end
end

def polynomial_evaluate_t(polynomial, value)
  polynomial.sum do |(x_power, t_power), coefficient|
    raise 'x was not integrated' unless x_power.zero?

    coefficient * value**t_power
  end
end

def polynomial_coefficients(polynomial, degree)
  (0..degree).map do |power|
    rational_text(polynomial.fetch([0, power], Rational(0)))
  end
end

text = MAIN.read
flat_text = text.gsub(/\s+/, ' ')
scan_text = text + (MUTATION == 'control' ? "\u0001" : '')
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_payload = JSON.parse(JSON_PATH.read)

source_expectations = FROZEN_SOURCES.dup
source_expectations['research/r075h_single_pass_transport_flux_closure.md'] =
  '0' * 64 if MUTATION == 'source_drift'
source_expectations[
  'research/r075h_single_pass_transport_flux_closure_primary_audit.md'
] = '0' * 64 if MUTATION == 'audit_drift'
source_expectations['research/r075h_report-source.md'] =
  '0' * 64 if MUTATION == 'report_source_drift'
source_expectations['research/r075b_bulk_clock_outer_padding_gate.md'] =
  '0' * 64 if MUTATION == 'dependency_drift'
source_rows = source_expectations.keys.sort.to_h do |path|
  [path, [
    source_expectations.fetch(path),
    Digest::SHA256.file(ROOT + path).hexdigest
  ]]
end
fixture_expected_hash = MUTATION == 'fixture_drift' ? '0' * 64 : FIXTURES_SHA256
expected_expected_hash = MUTATION == 'expected_drift' ? '0' * 64 : EXPECTED_SHA256
fixture_hash = Digest::SHA256.file(FIXTURES).hexdigest
expected_hash = Digest::SHA256.file(EXPECTED).hexdigest

# H.10--H.14 through Fourier constant coefficients.
transport = fixtures.fetch('weightedTransportCase')
cutoff_mean = rational(transport.fetch('cutoffMean'))
cutoff_amplitude = rational(transport.fetch('cutoffSineAmplitude'))
eta_initial = rational(transport.fetch('etaInitial'))
eta_terminal = rational(transport.fetch('etaTerminal'))
eta_nondecreasing = transport.fetch('etaNondecreasing')
eta_initial = 1 if MUTATION == 'eta_initial'
eta_terminal = 0 if MUTATION == 'eta_terminal'
eta_nondecreasing = false if MUTATION == 'eta_monotone'

# H^2 has zero coefficient 1/2. At terminal theta=pi/2 its +/-2
# coefficients are -i/4 and +i/4. xi has +/-2 coefficients -ic/2,+ic/2.
xi_plus = Complex(0, -cutoff_amplitude / 2)
xi_minus = xi_plus.conjugate
h2_initial = {0 => Rational(1, 2), 2 => Rational(1, 4), -2 => Rational(1, 4)}
h2_terminal = {
  0 => Rational(1, 2),
  2 => Complex(0, Rational(-1, 4)),
  -2 => Complex(0, Rational(1, 4))
}
weighted_energy = lambda do |h2|
  (
    cutoff_mean * h2.fetch(0) +
    xi_plus * h2.fetch(-2) +
    xi_minus * h2.fetch(2)
  ).real
end
initial_energy = weighted_energy.call(h2_initial)
terminal_energy = weighted_energy.call(h2_terminal)
half_factor = MUTATION == 'transport_half' ? Rational(1) : Rational(1, 2)
# With theta=pi*t/2: integral cos(theta)dtheta=1 and
# integral sin(theta)cos(theta)dtheta=1/2.
eta_prime_penalty =
  half_factor * (cutoff_mean / 2 + cutoff_amplitude / 8)
direct_sign = MUTATION == 'transport_pde_sign' ? -1 : 1
energy_sign = MUTATION == 'transport_energy_sign' ? -1 : 1
direct_flux =
  direct_sign * energy_sign * half_factor * cutoff_amplitude / 8
ibp_sign = MUTATION == 'eta_ibp_sign' ? 1 : -1
endpoint_minus_penalty =
  half_factor * eta_terminal * terminal_energy -
  half_factor * eta_initial * initial_energy +
  ibp_sign * eta_prime_penalty
transport_observed = {
  'initialEnergy' => rational_text(initial_energy),
  'terminalEnergy' => rational_text(terminal_energy),
  'terminalHalfEnergy' => rational_text(terminal_energy / 2),
  'etaPrimePenalty' => rational_text(eta_prime_penalty),
  'directWeightedFlux' => rational_text(direct_flux),
  'endpointMinusPenalty' => rational_text(endpoint_minus_penalty),
  'identityResidual' => rational_text(direct_flux - endpoint_minus_penalty),
  'positivePart' => rational_text([direct_flux, Rational(0)].max),
  'terminalHalfEnergyMinusPositivePart' =>
    rational_text(terminal_energy / 2 - [direct_flux, Rational(0)].max),
  'cutoffMinimum' => rational_text(cutoff_mean - cutoff_amplitude),
  'cutoffMaximum' => rational_text(cutoff_mean + cutoff_amplitude)
}

# H.7 and H.15--H.17 through exact lifted interval arithmetic.
tube = fixtures.fetch('terminalTubeCase')
t2 = rational(tube.fetch('terminalTime'))
j0, j1 = tube.fetch('terminalInterval').map { |value| rational(value) }
omega0 = tube.fetch('omega0Lift').map { |value| rational(value) }
omega_plus = tube.fetch('omegaPlusLift').map { |value| rational(value) }
q_terminal = t2 / 8
q_initial = j0 / 8
shift = q_terminal - q_initial
shift *= -1 if MUTATION == 'q_shift'
characteristic_sign = MUTATION == 'characteristic_direction' ? 1 : -1
characteristic_preimage = omega0.map do |endpoint|
  endpoint + characteristic_sign * shift
end
set_sign = MUTATION == 'set_translation_direction' ? 1 : -1
stated_preimage = omega0.map { |endpoint| endpoint + set_sign * shift }
wrong_image = omega0.map { |endpoint| endpoint + shift }
correct_contained = contained?(stated_preimage, omega_plus)
correct_contained = false if MUTATION == 'terminal_containment'
wrong_contained = contained?(wrong_image, omega_plus)
no_seam = MUTATION != 'seam_crossing'
terminal_l2 = rational(tube.fetch('terminalL2OnOmega0'))
terminal_l2 += Rational(1, 8) if MUTATION == 'terminal_l2'
# Integral of cos^2 over an interval of one full cos^2 period 1/2.
earlier_l2 = Rational(1, 2) * Rational(1, 2)
terminal_weighted = rational(tube.fetch('terminalWeightedEnergy'))
persistence_sign = MUTATION == 'persistence_direction' ? -1 : 1
persistence_slack = persistence_sign * (earlier_l2 - terminal_weighted)
interval_length = j1 - j0
persistence_time =
  MUTATION == 'persistence_time' ? interval_length**2 : interval_length
tube_observed = {
  'terminalIntervalLength' => rational_text(interval_length),
  'qTerminalOverTwoPi' => rational_text(q_terminal),
  'qInitialOverTwoPi' => rational_text(q_initial),
  'backwardShiftAtInitial' => rational_text(shift),
  'correctPreimage' => characteristic_preimage.map { |value| rational_text(value) },
  'wrongDirectionImage' => wrong_image.map { |value| rational_text(value) },
  'correctPreimageContained' => correct_contained,
  'wrongDirectionContained' => wrong_contained,
  'terminalL2OnOmega0' => rational_text(terminal_l2),
  'earlierL2OnPreimage' => rational_text(earlier_l2),
  'terminalWeightedEnergy' => rational_text(terminal_weighted),
  'persistenceSlack' => rational_text(persistence_slack),
  'integratedPersistenceLowerBound' =>
    rational_text(persistence_time * terminal_weighted)
}

# H.18--H.19 using direct finite-measure norms for a constant field.
holder = fixtures.fetch('holderEqualityCase')
delta = rational(holder.fetch('delta'))
volume = rational(holder.fetch('spatialVolume'))
magnitude = rational(holder.fetch('constantFieldMagnitude'))
cylinder_measure =
  MUTATION == 'holder_measure' ? delta + volume : delta * volume
l2_integral = delta * volume * magnitude**2
l3_integral = delta * volume * magnitude**3
measure_one_third = MUTATION == 'holder_measure' ? Rational(1, 2) : Rational(1, 4)
l3_two_thirds = MUTATION == 'holder_l3_power' ? Rational(1, 2) : Rational(1, 4)
holder_right = measure_one_third * l3_two_thirds
endpoint_energy = l2_integral / delta
delta_minus_two_thirds =
  %w[holder_delta_power holder_division].include?(MUTATION) ?
  Rational(2) :
  Rational(4)
volume_one_third =
  MUTATION == 'holder_volume_power' ? Rational(1, 4) : Rational(1, 2)
endpoint_bound_right =
  delta_minus_two_thirds * volume_one_third * l3_two_thirds
holder_observed = {
  'cylinderMeasure' => rational_text(cylinder_measure),
  'l2Integral' => rational_text(l2_integral),
  'l3Integral' => rational_text(l3_integral),
  'measureOneThird' => rational_text(measure_one_third),
  'l3TwoThirds' => rational_text(l3_two_thirds),
  'holderRight' => rational_text(holder_right),
  'endpointEnergy' => rational_text(endpoint_energy),
  'deltaMinusTwoThirds' => rational_text(delta_minus_two_thirds),
  'volumeOneThird' => rational_text(volume_one_third),
  'endpointBoundRight' => rational_text(endpoint_bound_right)
}

# H.23--H.24: independent Laurent exponent sum.
factor_rows = fixtures.fetch('h23Factors').to_h do |item|
  [
    item.fetch('name'),
    %w[L R omega p].to_h { |key| [key, rational(item.fetch(key))] }
  ]
end
factor_mutations = {
  'h23_flux_r' => ['fluxNormalization', 'R', Rational(1)],
  'h23_flux_omega' => ['fluxNormalization', 'omega', Rational(0)],
  'h23_delta_r' => ['deltaMinusTwoThirds', 'R', Rational(-1)],
  'h23_volume_l' => ['volumeOneThird', 'L', Rational(1, 3)],
  'h23_volume_r' => ['volumeOneThird', 'R', Rational(2)],
  'h23_cubic_r' => ['cubicTwoThirds', 'R', Rational(2, 3)],
  'h23_cubic_omega' => ['cubicTwoThirds', 'omega', Rational(2, 3)],
  'h23_cubic_p' => ['cubicTwoThirds', 'p', Rational(1, 3)]
}
if factor_mutations.key?(MUTATION)
  name, key, value = factor_mutations.fetch(MUTATION)
  factor_rows.fetch(name)[key] = value
end
h23_product = vector_add(factor_rows.values)
constants = fixtures.fetch('constants')
rho = rational(constants.fetch('rho'))
c_gamma = rational(constants.fetch('cGamma'))
rho_sign = MUTATION == 'rate_rho_sign' ? -1 : 1
gamma_sign = MUTATION == 'rate_cgamma_sign' ? 1 : -1
rate = rho_sign * rho / 6 + gamma_sign * c_gamma / 12
rate += Rational(1, 238_140_000) if MUTATION == 'rate_fraction'
h23_observed = {'product' => vector_text(h23_product), 'rate' => rational_text(rate)}

# H.26 finite matching-scale example.
matching = fixtures.fetch('matchingBackgroundCase')
mr = rational(matching.fetch('R'))
ml = rational(matching.fetch('L'))
momega = rational(matching.fetch('omega'))
mpb = rational(matching.fetch('pB'))
lower_scale = ml**2 * momega * mr**-3
coefficient_left = Rational(2)
matching_r_factor = MUTATION == 'matching_r_power' ? Rational(1) : Rational(1, 2)
pb_cube_root = MUTATION == 'matching_cube_root' ? Rational(8) : Rational(4)
matching_right = matching_r_factor * pb_cube_root
matching_observed = {
  'assumedLowerScale' => rational_text(lower_scale),
  'coefficientLeft' => rational_text(coefficient_left),
  'rOneThirdPBCubeRoot' => rational_text(matching_right),
  'inequalityDirection' =>
    MUTATION == 'matching_lower_direction' ? 'left>=right' : 'left<=right'
}

# One coherent nondegenerate rational fixture for H.11--H.23. The cutoff is
# piecewise affine, hence this block checks the a.e. transport/IBP arithmetic
# but is deliberately not reused for the smooth Delta-xi identity in H.28.
coherent = fixtures.fetch('coherentRationalClosureCase')
c_qprime = rational(coherent.fetch('qPrime'))
c_qprime *= -1 if MUTATION == 'transport_pde_sign'
c_eta_break = rational(coherent.fetch('etaBreak'))
c_eta_slope = rational(coherent.fetch('etaEarlySlope'))
c_eta_plateau = MUTATION == 'eta_plateau' ? Rational(0) :
  rational(coherent.fetch('etaPlateau'))
c_j0, c_j1 = coherent.fetch('terminalInterval').map { |value| rational(value) }
c_omega0 = coherent.fetch('omega0').map { |value| rational(value) }
c_omega_plus = coherent.fetch('omegaPlus').map { |value| rational(value) }
c_r = rational(coherent.fetch('R'))
c_l = rational(coherent.fetch('L'))
c_omega = rational(coherent.fetch('omega'))
c_weight = rational(coherent.fetch('exteriorWeight'))
c_pb = rational(coherent.fetch('matchingPB'))

linear_polynomial = lambda do |spec|
  polynomial_clean({
    [0, 0] => rational(spec.fetch('constant')),
    [1, 0] => rational(spec.fetch('x')),
    [0, 1] => rational(spec.fetch('t'))
  })
end
c_h = linear_polynomial.call(coherent.fetch('positiveField'))
c_g = linear_polynomial.call(coherent.fetch('negativeControlField'))
c_xi_pieces = coherent.fetch('xiPieces').map do |piece|
  lower, upper = piece.fetch('interval').map { |value| rational(value) }
  xi = polynomial_clean({
    [0, 0] => rational(piece.fetch('constant')),
    [1, 0] => rational(piece.fetch('x'))
  })
  [lower, upper, xi]
end

weighted_x_integral = lambda do |field, power|
  field_power = polynomial_power(field, power)
  polynomial_add(*c_xi_pieces.map do |lower, upper, xi|
    polynomial_integrate_x(polynomial_multiply(xi, field_power), lower, upper)
  end)
end
xi_prime_x_integral = lambda do |field|
  field_square = polynomial_power(field, 2)
  polynomial_add(*c_xi_pieces.map do |lower, upper, xi|
    polynomial_integrate_x(
      polynomial_multiply(polynomial_derivative(xi, 0), field_square),
      lower,
      upper
    )
  end)
end
eta_weighted_time_integral = lambda do |polynomial|
  early_eta = {[0, 1] => c_eta_slope}
  polynomial_integrate_t(
    polynomial_multiply(early_eta, polynomial),
    Rational(0),
    c_eta_break
  ) + c_eta_plateau * polynomial_integrate_t(
    polynomial,
    c_eta_break,
    Rational(1)
  )
end

c_energy = weighted_x_integral.call(c_h, 2)
c_negative_energy = weighted_x_integral.call(c_g, 2)
c_energy_derivative = polynomial_derivative(c_energy, 1)
c_flux_density = polynomial_scale(
  xi_prime_x_integral.call(c_h),
  c_qprime
)
c_negative_flux_density = polynomial_scale(
  xi_prime_x_integral.call(c_g),
  c_qprime
)
if MUTATION == 'transport_energy_sign'
  c_flux_density = polynomial_scale(c_flux_density, -1)
  c_negative_flux_density = polynomial_scale(c_negative_flux_density, -1)
end
c_transport_residual = polynomial_add(
  polynomial_derivative(c_h, 1),
  polynomial_scale(polynomial_derivative(c_h, 0), c_qprime)
)
c_half = MUTATION == 'transport_half' ? Rational(1) : Rational(1, 2)
c_direct_flux = c_half * eta_weighted_time_integral.call(c_flux_density)
c_negative_direct_flux =
  c_half * eta_weighted_time_integral.call(c_negative_flux_density)
c_initial_energy = polynomial_evaluate_t(c_energy, Rational(0))
c_terminal_energy = polynomial_evaluate_t(c_energy, Rational(1))
c_negative_terminal_energy =
  polynomial_evaluate_t(c_negative_energy, Rational(1))
c_eta_penalty = c_half * c_eta_slope * polynomial_integrate_t(
  c_energy,
  Rational(0),
  c_eta_break
)
c_endpoint_rhs =
  c_half * c_eta_plateau * c_terminal_energy -
  c_half * eta_initial * c_initial_energy +
  (MUTATION == 'eta_ibp_sign' ? c_eta_penalty : -c_eta_penalty)
c_positive_part = [c_direct_flux, Rational(0)].max
c_negative_positive_part = if MUTATION == 'transport_absolute_flux'
                             c_negative_direct_flux.abs
                           else
                             [c_negative_direct_flux, Rational(0)].max
                           end

c_delta = c_j1 - c_j0
c_shift = c_qprime * (Rational(1) - c_j0)
c_preimage_sign = MUTATION == 'characteristic_direction' ? 1 : -1
c_preimage = c_omega0.map { |endpoint| endpoint + c_preimage_sign * c_shift }
c_wrong_image = c_omega0.map { |endpoint| endpoint + c_shift }
c_preimage_contained = contained?(c_preimage, c_omega_plus)
c_wrong_contained = contained?(c_wrong_image, c_omega_plus)
c_tube_l2 = polynomial_integrate_t(
  polynomial_integrate_x(polynomial_power(c_h, 2), *c_omega_plus),
  c_j0,
  c_j1
)
c_tube_l3 = polynomial_integrate_t(
  polynomial_integrate_x(polynomial_power(c_h, 3), *c_omega_plus),
  c_j0,
  c_j1
)
c_terminal_unweighted_l2 = polynomial_evaluate_t(
  polynomial_integrate_x(polynomial_power(c_h, 2), *c_omega0),
  Rational(1)
)
c_volume = c_omega_plus[1] - c_omega_plus[0]
c_measure = c_delta * c_volume
c_h17_slack = c_tube_l2 - c_delta * c_terminal_energy
c_h18_left_cubed = c_tube_l2**3
c_h18_right_cubed = c_measure * c_tube_l3**2
c_h19_left_cubed = c_delta**2 * c_terminal_energy**3
c_h19_right_cubed = c_volume * c_tube_l3**2

c_atom_r_power = MUTATION == 'atom_r_sign' ? 2 : -2
c_atom_omega_power = MUTATION == 'atom_omega_sign' ? -1 : 1
c_atom = c_r**c_atom_r_power * c_omega**c_atom_omega_power * c_tube_l3
c_measurement = c_r**-2 *
  (MUTATION == 'measurement_weight' ? c_weight**-1 : c_weight) * c_tube_l3
c_flux_r_power = MUTATION == 'flux_normalization' ? 1 : -1
c_flux_x = c_omega * c_r**c_flux_r_power * c_positive_part
c_h23_left_cubed = c_flux_x**3
c_h23_right_cubed = c_l**2 * c_omega * c_r**-2 * c_atom**2
c_matching_lower = c_l**2 * c_omega * c_r**-3
c_matching_left_cube = c_l**2 * c_omega * c_r**-2
c_matching_right_cube = c_r * c_pb
c_weight_ok = MUTATION != 'conditional_weight' && c_weight >= c_omega
c_payment_region_ok = MUTATION != 'payment_region'

coherent_observed = {
  'transportResidualCoefficients' => [
    rational_text(c_transport_residual.fetch([0, 0], Rational(0))),
    rational_text(c_transport_residual.fetch([1, 0], Rational(0))),
    rational_text(c_transport_residual.fetch([0, 1], Rational(0)))
  ],
  'energyPolynomial' => polynomial_coefficients(c_energy, 2),
  'energyDerivativePolynomial' => polynomial_coefficients(c_energy_derivative, 1),
  'fluxDensityPolynomial' => polynomial_coefficients(c_flux_density, 1),
  'initialEnergy' => rational_text(c_initial_energy),
  'terminalEnergy' => rational_text(c_terminal_energy),
  'etaPrimePenalty' => rational_text(c_eta_penalty),
  'directWeightedFlux' => rational_text(c_direct_flux),
  'endpointMinusPenalty' => rational_text(c_endpoint_rhs),
  'positivePart' => rational_text(c_positive_part),
  'h14Slack' => rational_text(c_terminal_energy / 2 - c_positive_part),
  'delta' => rational_text(c_delta),
  'omegaPlusVolume' => rational_text(c_volume),
  'maxBackwardShift' => rational_text(c_shift),
  'correctPreimageAtJStart' => c_preimage.map { |value| rational_text(value) },
  'wrongImageAtJStart' => c_wrong_image.map { |value| rational_text(value) },
  'correctPreimageContained' => c_preimage_contained,
  'wrongImageContained' => c_wrong_contained,
  'terminalUnweightedL2' => rational_text(c_terminal_unweighted_l2),
  'terminalWeightedSlack' =>
    rational_text(c_terminal_unweighted_l2 - c_terminal_energy),
  'tubeL2' => rational_text(c_tube_l2),
  'tubeL3' => rational_text(c_tube_l3),
  'h17Slack' => rational_text(c_h17_slack),
  'cylinderMeasure' => rational_text(c_measure),
  'h18LeftCubed' => rational_text(c_h18_left_cubed),
  'h18RightCubed' => rational_text(c_h18_right_cubed),
  'h18StrictGap' => rational_text(c_h18_right_cubed - c_h18_left_cubed),
  'h19LeftCubed' => rational_text(c_h19_left_cubed),
  'h19RightCubed' => rational_text(c_h19_right_cubed),
  'h19StrictGap' => rational_text(c_h19_right_cubed - c_h19_left_cubed),
  'terminalAtomP' => rational_text(c_atom),
  'benchmarkMeasurementP' => rational_text(c_measurement),
  'normalizedPositiveFluxX' => rational_text(c_flux_x),
  'h23LeftCubed' => rational_text(c_h23_left_cubed),
  'h23RightCubed' => rational_text(c_h23_right_cubed),
  'h23StrictGap' => rational_text(c_h23_right_cubed - c_h23_left_cubed),
  'matchingLowerScale' => rational_text(c_matching_lower),
  'matchingPBCubeComparisonLeft' => rational_text(c_matching_left_cube),
  'matchingPBCubeComparisonRight' => rational_text(c_matching_right_cube),
  'negativeEnergyPolynomial' => polynomial_coefficients(c_negative_energy, 2),
  'negativeTerminalEnergy' => rational_text(c_negative_terminal_energy),
  'negativeDirectFlux' => rational_text(c_negative_direct_flux),
  'negativePositivePart' => rational_text(c_negative_positive_part),
  'negativeAbsoluteFlux' => rational_text(c_negative_direct_flux.abs),
  'negativeAbsMinusTerminalHalfEnergy' =>
    rational_text(c_negative_direct_flux.abs - c_negative_terminal_energy / 2)
}

# H.28 coefficient ledger.
diff = fixtures.fetch('diffusiveIdentityCase')
terminal_coefficient = MUTATION == 'diff_terminal_sign' ? -1 : 1
dissipation_coefficient = MUTATION == 'diff_dissipation_sign' ? -1 : 1
cutoff_coefficient = MUTATION == 'diff_cutoff_sign' ? 1 : -1
diff_transport =
  terminal_coefficient * rational(diff.fetch('terminalHalfEnergy')) +
  dissipation_coefficient * rational(diff.fetch('dissipation')) +
  cutoff_coefficient * rational(diff.fetch('cutoffHalfIntegral'))
target_on_right = MUTATION != 'diff_circularity'
diff_observed = {
  'transport' => rational_text(diff_transport),
  'terminalCoefficient' => terminal_coefficient.to_s,
  'dissipationCoefficient' => dissipation_coefficient.to_s,
  'cutoffCoefficient' => cutoff_coefficient.to_s,
  'targetDissipationAppearsOnRight' => target_on_right
}

tags = text.scan(/\\tag\{(H\.[^}]+)\}/).flatten
tags << 'H.1' if MUTATION == 'tag'
references = text.scan(/\(H\.([0-9]+[a-z]?)\)/).flatten.map do |value|
  "H.#{value}"
end
references << 'H.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\[' }
display_close = text.lines.count { |line| line.strip == '\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..29).map { |index| "H.#{index}" }

dependency_paths = %w[
  research/r075b_bulk_clock_outer_padding_gate.md
  research/r075e_horizontal_cross_mode_flux_reduction.md
  research/r075f_modal_phase_integration_identity.md
  research/r075g_signed_flux_gain_threshold.md
]
dependency_table_present = dependency_paths.all? do |path|
  text.lines.any? do |line|
    line.include?(path) && line.include?(FROZEN_SOURCES.fetch(path))
  end
end
dependency_table_present = false if MUTATION == 'dependency_table_missing'

required_tokens = [
  "\\eta_R'\\ge0",
  '\\Omega_0-\\bigl(q(t_2)-q(t)\\bigr)e_2',
  'H(t,x)=H\\bigl(t_2,x+(q(t_2)-q(t))e_2\\bigr)',
  '\\delta_R^{-2/3}|\\Omega_+|^{1/3}',
  'L^{2/3}\\omega^{1/3}R^{-2/3}',
  '-\\frac{4279}{238140000}',
  'p_b >= c L^2 omega R^(-3)',
  '\\le C R^{1/3}p_b^{1/3}',
  '+\\int_s^{t_2}\\!\\int\\eta_R\\xi|\\nabla_{23}F|^2',
  'does not assert that the benchmark pair is a Navier--Stokes solution',
  'The characteristic identity (H.15) also fails after diffusion.',
  '\\mathbf{NOT\\ CLAY}'
]

audit_text = PRIMARY_AUDIT.read
boundary = {
  'signedNotAbsoluteFlux' => MUTATION != 'transport_absolute_flux',
  'noBlockCount' => MUTATION != 'block_count',
  'fixedLiftNoSeam' => no_seam,
  'terminalTubeInsidePaymentRegion' => MUTATION != 'payment_region',
  'weightLowerBoundConditional' => MUTATION != 'conditional_weight',
  'benchmarkNotNSE' => MUTATION != 'benchmark_nse',
  'diffusiveCharacteristicUnavailable' => MUTATION != 'diffusive_characteristic',
  'E24Open' => MUTATION != 'e24_closed',
  'completeClockOpen' => MUTATION != 'complete_clock',
  'fixedDeletionOpen' => MUTATION != 'fixed_deletion',
  'suitableWeakTransferOpen' => MUTATION != 'suitable_weak',
  'regularityAndSingularityOpen' => MUTATION != 'regularity',
  'notClay' => MUTATION != 'clay'
}

checks = {
  'all seven frozen source hashes' =>
    source_rows.values.all? { |pair| pair[0] == pair[1] },
  'fixture and expected byte bindings' =>
    fixture_hash == fixture_expected_hash &&
    expected_hash == expected_expected_hash &&
    fixtures.fetch('schema') ==
      'r075h-single-pass-transport-flux-closure-fixtures-v1' &&
    expected.fetch('schema') ==
      'r075h-single-pass-transport-flux-closure-expected-v1' &&
    fixtures.fetch('frozenSources') == FROZEN_SOURCES,
  'primary audit main binding and PASS/0 status' =>
    audit_text.include?(FROZEN_SOURCES.fetch(
      'research/r075h_single_pass_transport_flux_closure.md'
    )) &&
    audit_text.include?(
      'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.'
    ) &&
    audit_text.include?('Equation tags H.1--H.29 are unique and consecutive.'),
  'B/E/F/G table entries in main' => dependency_table_present,
  'weighted transport Fourier endpoint energies' =>
    transport_observed.fetch('initialEnergy') == '1/4' &&
    transport_observed.fetch('terminalEnergy') == '5/16' &&
    transport_observed.fetch('cutoffMinimum') == '1/4' &&
    transport_observed.fetch('cutoffMaximum') == '3/4',
  'eta endpoint and monotonicity hypotheses' =>
    eta_initial == 0 && eta_terminal == 1 && eta_nondecreasing,
  'weighted transport direct flux and IBP identity' =>
    transport_observed == expected.fetch('weightedTransport') &&
    direct_flux > 0 && direct_flux == endpoint_minus_penalty,
  'characteristic translation direction' =>
    characteristic_preimage == stated_preimage &&
    characteristic_preimage.map { |value| rational_text(value) } ==
      expected.dig('terminalTube', 'correctPreimage'),
  'lifted set containment and no seam' =>
    correct_contained && !wrong_contained && no_seam,
  'terminal L2 persistence and time integration' =>
    tube_observed == expected.fetch('terminalTube') &&
    earlier_l2 >= terminal_l2 && terminal_l2 >= terminal_weighted &&
    persistence_slack >= 0,
  'spacetime Holder equality' =>
    holder_observed.fetch('cylinderMeasure') == '1/64' &&
    l2_integral == holder_right,
  'delta minus two-thirds and volume one-third endpoint bound' =>
    holder_observed == expected.fetch('holder') &&
    endpoint_energy == endpoint_bound_right,
  'H.23 full L/R/omega/p exponent product' =>
    h23_observed.fetch('product') == expected.dig('h23', 'product'),
  'H.24 exact negative rate' =>
    rational_text(rate) == expected.dig('h23', 'rate') && rate < 0,
  'H.26 matching lower-bound direction' =>
    matching_observed == expected.fetch('matchingBackground') &&
    mpb >= lower_scale && coefficient_left <= matching_right,
  'coherent rational H.11--H.23 chain and signed control' =>
    coherent_observed == expected.fetch('coherentRationalClosure') &&
    c_transport_residual.empty? &&
    c_energy_derivative == c_flux_density &&
    c_eta_plateau == 1 && c_j0 >= c_eta_break &&
    c_direct_flux == c_endpoint_rhs && c_direct_flux.positive? &&
    c_preimage_contained && !c_wrong_contained &&
    c_terminal_unweighted_l2 >= c_terminal_energy &&
    c_h17_slack.positive? &&
    c_h18_right_cubed > c_h18_left_cubed &&
    c_h19_right_cubed > c_h19_left_cubed &&
    c_weight_ok && c_payment_region_ok &&
    c_atom <= c_measurement &&
    c_h23_right_cubed > c_h23_left_cubed &&
    c_pb >= c_matching_lower &&
    c_matching_left_cube <= c_matching_right_cube &&
    c_negative_direct_flux.negative? &&
    c_negative_positive_part.zero? &&
    c_negative_direct_flux.abs > c_negative_terminal_energy / 2,
  'H.28 signs and target dissipation circularity' =>
    diff_observed == expected.fetch('diffusiveIdentity') &&
    target_on_right && dissipation_coefficient == 1,
  '29 tags, references, and displays' =>
    tags == expected_tags && tags.uniq.length == 29 &&
    (references - tags).empty? &&
    display_open == 29 && display_close == 29,
  'formula and status sentinels' =>
    required_tokens.all? do |token|
      flat_text.include?(token.gsub(/\s+/, ' '))
    end,
  'claim boundary' => boundary.values.all?,
  'Python schema and all exact-ledger cross-checks' =>
    python_payload.fetch('schema') == SCHEMA &&
    python_payload.fetch('verdict') == 'PASS' &&
    python_payload.fetch('weightedTransport') == transport_observed &&
    python_payload.fetch('terminalTube') == tube_observed &&
    python_payload.fetch('holder') == holder_observed &&
    python_payload.fetch('h23') == h23_observed &&
    python_payload.fetch('matchingBackground') == matching_observed &&
    python_payload.fetch('coherentRationalClosure') == coherent_observed &&
    python_payload.fetch('diffusiveIdentity') == diff_observed,
  'UTF-8 and control safety' =>
    scan_text.valid_encoding? &&
    !scan_text.each_codepoint.any? do |code|
      code < 32 && ![9, 10].include?(code)
    end
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed = checks.reject { |_name, passed| passed }.keys
REPORT.write(
  "# R0.75H independent finite audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}\n" \
  "- Fixture SHA-256: #{fixture_hash}\n" \
  "- Expected SHA-256: #{expected_hash}\n" \
  "- Failed checks: #{failed.empty? ? 'none' : failed.join('; ')}\n\n" \
  "Ruby uses Fourier constant coefficients for the smooth weighted " \
  "transport example and obtains direct positive flux 1/64, equal to the " \
  "endpoint-minus-eta-prime row. A second nondegenerate all-rational field " \
  "is propagated coherently through H.11--H.23, including the endpoint " \
  "identity, lifted-set direction, terminal persistence, both Holder rows, " \
  "p/P normalization, and matching scale. Its tent cutoff is an a.e. " \
  "arithmetic fixture, not the smooth H.28 cutoff. The mirrored negative-flux " \
  "control has zero positive part and nonzero absolute flux, rejecting an " \
  "absolute-value substitution.\n\n" \
  "The exact exponent, rate, matching-lower-bound, and diffusive-sign ledgers " \
  "agree with Python. The target dissipation remains on the right of H.28, " \
  "so the diffusive route is circular. P_R^(M,tr) is not an NSE assertion. " \
  "E.24 and all larger claims remain OPEN. **NOT CLAY.**\n"
)

puts JSON.generate(
  suite: 'r075h-single-pass-transport-flux-closure-independent',
  verdict: verdict,
  assertions: checks.length
)
exit(verdict == 'PASS' ? 0 : 1)
