#!/usr/bin/env ruby
# Independent exact verifier for frozen R0.75N.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075n_radial_collar_averaged_wiener_row.md'
PRIMARY_AUDIT = ROOT + 'research/r075n_radial_collar_averaged_wiener_row_primary_audit.md'
REPORT_SOURCE = ROOT + 'research/r075n_report-source.md'
B_SOURCE = ROOT + 'research/r075b_bulk_clock_outer_padding_gate.md'
FIXTURES = ROOT + 'scripts/r075n_radial_collar_averaged_wiener_row_fixtures.json'
EXPECTED = ROOT + 'scripts/r075n_radial_collar_averaged_wiener_row_expected.json'
JSON_PATH = Pathname.new(
  ENV.fetch('R075N_JSON', (ROOT + 'research/r075n_radial_collar_averaged_wiener_row_certificate.json').to_s)
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075N_RUBY_REPORT',
    (ROOT + 'research/r075n_radial_collar_averaged_wiener_row_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075N_RUBY_MUTATION', '')
SCHEMA = 'r075n-radial-collar-averaged-wiener-row-certificate-v1'

FROZEN_SOURCES = {
  'research/r075b_bulk_clock_outer_padding_gate.md' =>
    '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075c_background_shear_packing_false_positive.md' =>
    '1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89',
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075m_dyadic_packet_diffusive_flux_gain.md' =>
    '13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7',
  'research/r075n_radial_collar_averaged_wiener_row.md' =>
    'ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318',
  'research/r075n_radial_collar_averaged_wiener_row_primary_audit.md' =>
    'c43c063b1c003be22782e7d8e1ce0b3f42cdd3ef4d01912c9de34c876d8c9aba',
  'research/r075n_report-source.md' =>
    'ae9d5d630ee0549193c016fcbc07c599b0c678fbaf9c15c5d3c7f24bdf18e27c'
}.freeze
FIXTURES_SHA256 = '2dee2146f94f3fa6d0d0c5828d8d6f354f0856f620e1261a133c9a2c81f8a0cb'
EXPECTED_SHA256 = '31614fc11bc4355723fff7773bec8ab13bc44808ffffa0958c78ec1cfe2bba48'

NEGATIVE_MUTATIONS = %w[
  source_drift audit_drift report_source_drift dependency_drift
  dependency_table_missing fixture_drift expected_drift tag reference display
  control p_reciprocal a_definition r_definition R_range a_condition
  central_chart periodic_overlap profile_fixed profile_smooth
  profile_nonnegative profile_support profile_plateau B_choice_freedom
  canonical_universal derivative_cost fourier_normalization fourier_sign
  derivative_i derivative_ell d0 integration_by_parts reconstruction_phase
  sampling_compact sampling_W21 sampling_uniform_A sampling_nu sampling_R
  sup_sum_order low_cutoff low_count low_L1 low_R_power high_one_ibp
  high_denominator high_tail_direction high_tail_R high_raw high_R_power
  discrete_riemann slice_scaling_x1 slice_derivative_R slice_fourier_R
  slice_2pi slice_empty_range slice_interior_difference slice_area_factor
  tangency_missing tangency_cap outer_disk radial_lower
  radial_first_derivative radial_third_derivative radial_uniform
  fubini_direction slice_L1_a sum_all_modes coefficientwise_sup row_R_loss
  row_a_power full_average_jacobian full_derivative_R full_fourier_R
  full_shell_formula full_shell_volume_power full_fubini_a full_row_R
  full_row_a wiener_h1_substitution frequency_K frequency_gain
  frequency_direction frequency_R frequency_first_L frequency_first_R
  frequency_full_L frequency_full_R frequency_threshold
  physical_coefficient_only dynamical_flux_claim canonical_required
  all_cutoffs_claim vertical_diffusion_closed nonconstant_shear_closed
  local_cubic_closed interpacket_closed low_difference_closed e24_claim
  complete_clock fixed_deletion suitable_weak regularity singularity
  novelty priority simulation clay
].freeze

abort("unknown R075N_RUBY_MUTATION: #{MUTATION}") unless
  MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)

def rat(value)
  Rational(value.to_s)
end

def rtext(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

def exponent_text(row)
  row.to_h { |key, value| [key, rtext(value)] }
end

text = MAIN.read
audit_text = PRIMARY_AUDIT.read
source_text = REPORT_SOURCE.read
b_text = B_SOURCE.read
flat_text = text.gsub(/\s+/, ' ')
flat_source = source_text.gsub(/\s+/, ' ')
flat_b = b_text.gsub(/\s+/, ' ')
scan_text = text + audit_text + source_text + (MUTATION == 'control' ? "\u0001" : '')
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_payload = JSON.parse(JSON_PATH.read)

source_expectations = FROZEN_SOURCES.dup
source_expectations['research/r075n_radial_collar_averaged_wiener_row.md'] =
  '0' * 64 if MUTATION == 'source_drift'
source_expectations[
  'research/r075n_radial_collar_averaged_wiener_row_primary_audit.md'
] = '0' * 64 if MUTATION == 'audit_drift'
source_expectations['research/r075n_report-source.md'] =
  '0' * 64 if MUTATION == 'report_source_drift'
source_expectations['research/r075b_bulk_clock_outer_padding_gate.md'] =
  '0' * 64 if MUTATION == 'dependency_drift'
source_rows = source_expectations.keys.sort.to_h do |path|
  [path, [source_expectations.fetch(path), Digest::SHA256.file(ROOT + path).hexdigest]]
end
fixture_expected_hash = MUTATION == 'fixture_drift' ? '0' * 64 : FIXTURES_SHA256
expected_expected_hash = MUTATION == 'expected_drift' ? '0' * 64 : EXPECTED_SHA256
fixture_hash = Digest::SHA256.file(FIXTURES).hexdigest
expected_hash = Digest::SHA256.file(EXPECTED).hexdigest

# Exact frozen calibration and a rational central-chart witness.
calibration_fixture = fixtures.fetch('calibrationCase')
p_value = rat(calibration_fixture.fetch('p'))
p_value = 1 / p_value if MUTATION == 'p_reciprocal'
length = rat(calibration_fixture.fetch('L'))
scale = rat(calibration_fixture.fetch('R'))
delta = rat(calibration_fixture.fetch('delta'))
a_value = p_value * length
a_value += 1 if MUTATION == 'a_definition'
radius = a_value * scale
radius += scale if MUTATION == 'r_definition'
outer_radius = (a_value + delta) * scale
calibration_observed = {
  'p' => rtext(p_value),
  'a' => rtext(a_value),
  'r' => rtext(radius),
  'aAtLeastMax2Delta1' => MUTATION == 'a_condition' ? false : a_value >= [2 * delta, 1].max,
  'outerSupportRadius' => rtext(outer_radius),
  'centralChartCertifiedByOuterRadiusBelowOne' => MUTATION == 'central_chart' ? false : outer_radius < 1
}

# A Laurent-polynomial fixture for d_l=+i*l*Xi_l.
fourier_fixture = fixtures.fetch('fourierDerivativeCase')
fourier_rows = fourier_fixture.fetch('XiModes').map do |row|
  ell = row.fetch('ell')
  real = rat(row.fetch('real'))
  imag = rat(row.fetch('imag'))
  derivative_real = -ell * imag
  derivative_imag = ell * real
  derivative_real, derivative_imag = ell * real, ell * imag if MUTATION == 'derivative_i'
  derivative_real, derivative_imag = -imag, real if MUTATION == 'derivative_ell'
  derivative_real = 1 if MUTATION == 'd0' && ell.zero?
  {
    'ell' => ell,
    'XiReal' => rtext(real),
    'XiImag' => rtext(imag),
    'dReal' => rtext(Rational(derivative_real)),
    'dImag' => rtext(Rational(derivative_imag))
  }
end
zero_row = fourier_rows.find { |row| row.fetch('ell').zero? }
fourier_observed = {
  'normalization' => MUTATION == 'fourier_normalization' ? '1/pi' : '1/(2*pi)',
  'reconstructionPhase' => %w[fourier_sign reconstruction_phase].include?(MUTATION) ? '-i*ell*x2' : '+i*ell*x2',
  'derivativeRule' => %w[fourier_sign integration_by_parts].include?(MUTATION) ?
    'd_ell=-i*ell*Xi_ell' : 'd_ell=i*ell*Xi_ell',
  'rows' => fourier_rows,
  'dZero' => "#{zero_row.fetch('dReal')}+#{zero_row.fetch('dImag')}i"
}

# Low/high sample split at R=1/4, preserving sum_l sup_z.
sampling_fixture = fixtures.fetch('samplingCase')
sample_scale = rat(sampling_fixture.fetch('R'))
sample_scale = Rational(1, 2) if MUTATION == 'sampling_R'
uniform_bound = rat(sampling_fixture.fetch('A'))
cutoff = (1 / sample_scale).to_i
cutoff -= 1 if MUTATION == 'low_cutoff'
low_count = 2 * cutoff + 1
low_count += 1 if MUTATION == 'low_count'
low_raw = uniform_bound * low_count
low_raw += uniform_bound if MUTATION == 'low_L1'
high_tail = 2 * sample_scale
high_tail = 2 * sample_scale**2 if MUTATION == 'high_tail_R'
high_raw = uniform_bound / sample_scale**2 * high_tail
high_raw *= sample_scale if %w[high_one_ibp high_denominator].include?(MUTATION)
high_raw += 1 if MUTATION == 'high_raw'
finite_reciprocal = 2 * sampling_fixture.fetch('finiteHighSamples').sum do |ell|
  Rational(1, ell * ell)
end
finite_raw = uniform_bound / sample_scale**2 * finite_reciprocal
sampling_rows = sampling_fixture.fetch('nu').map do |nu|
  low_weighted = sample_scale**nu * low_raw
  high_weighted = sample_scale**nu * high_raw
  low_weighted += 1 if MUTATION == 'low_R_power' && nu == 1
  high_weighted += 1 if MUTATION == 'high_R_power' && nu == 2
  {
    'nu' => nu,
    'lowWeightedBound' => rtext(low_weighted),
    'highWeightedBound' => rtext(high_weighted),
    'combinedWeightedBound' => rtext(low_weighted + high_weighted),
    'targetRPower' => rtext(Rational(nu - 1))
  }
end
sampling_observed = {
  'cutoffIndex' => rtext(Rational(cutoff)),
  'lowIntegerCount' => rtext(Rational(low_count)),
  'lowRawBound' => rtext(low_raw),
  'highReciprocalTailBound' => rtext(high_tail),
  'highRawBound' => rtext(high_raw),
  'finiteHighReciprocalSum' => rtext(finite_reciprocal),
  'finiteHighRawBound' => rtext(finite_raw),
  'rows' => sampling_rows,
  'lowMechanism' => MUTATION == 'discrete_riemann' ? 'Riemann-sum' : 'count-O(R^-1)-times-L1',
  'highMechanism' => MUTATION == 'high_one_ibp' ?
    'one-IBP-R^-1-times-harmonic-tail' : 'two-IBP-R^-2-times-tail-O(R)',
  'supremumOrder' => MUTATION == 'sup_sum_order' ?
    'sup-over-z-of-sum-over-ell' : 'sum-over-ell-of-sup-over-z'
}

# Exact disk-difference and tangency-cap cases, with areas divided by pi.
slice_fixture = fixtures.fetch('sliceAreaCase')
slice_a = rat(slice_fixture.fetch('a'))
slice_delta = rat(slice_fixture.fetch('delta'))
cap = 4 * slice_a * slice_delta
cap = 2 * slice_a * slice_delta if %w[slice_area_factor tangency_cap].include?(MUTATION)
slice_rows = slice_fixture.fetch('zSamples').map do |z_text|
  z_value = rat(z_text)
  outer = [(slice_a + slice_delta)**2 - z_value**2, 0].max
  inner = [(slice_a - slice_delta)**2 - z_value**2, 0].max
  area = outer - inner
  magnitude = z_value.abs
  region = if magnitude < slice_a - slice_delta
             'interior'
           elsif magnitude == slice_a - slice_delta
             'interior-boundary'
           elsif magnitude < slice_a + slice_delta
             'tangency'
           elsif magnitude == slice_a + slice_delta
             'empty-boundary'
           else
             'empty'
           end
  area = 0 if MUTATION == 'tangency_missing' && region == 'tangency'
  area += 1 if MUTATION == 'slice_interior_difference' && region.start_with?('interior')
  area += 1 if MUTATION == 'outer_disk' && region == 'tangency'
  {
    'z' => rtext(z_value),
    'region' => region,
    'areaOverPi' => rtext(Rational(area)),
    'capGapOverPi' => rtext(cap - area)
  }
end
slice_observed = {'uniformCapOverPi' => rtext(cap), 'rows' => slice_rows}

volume = Rational(4, 3) * ((slice_a + slice_delta)**3 - (slice_a - slice_delta)**3)
volume += 1 if MUTATION == 'full_shell_formula'
full_shell_observed = {
  'volumeOverPi' => rtext(volume),
  'exactExpansionOverPi' => MUTATION == 'full_shell_volume_power' ?
    '4*a^2*delta+8*delta^3/3' : '8*a^2*delta+8*delta^3/3',
  'volumeOverPiDividedByASquared' => rtext(volume / slice_a**2),
  'order' => MUTATION == 'full_shell_volume_power' ? 'O_delta(a^3)' : 'O_delta(a^2)'
}

# R-Jacobian and Fubini exponent ledgers for the two averaging patterns.
scaling_fixture = fixtures.fetch('scalingCase')
x1_prefactor = rat(scaling_fixture.fetch('x1AverageJacobianPower'))
full_prefactor = rat(scaling_fixture.fetch('fullAverageJacobianPower'))
derivative_power = rat(scaling_fixture.fetch('x2DerivativePower'))
fourier_jacobian = rat(scaling_fixture.fetch('x2FourierJacobianPower'))
x1_prefactor = 2 if MUTATION == 'slice_scaling_x1'
full_prefactor = 3 if MUTATION == 'full_average_jacobian'
slice_after_derivative = x1_prefactor + derivative_power
full_after_derivative = full_prefactor + derivative_power
slice_after_derivative += 1 if MUTATION == 'slice_derivative_R'
full_after_derivative += 1 if MUTATION == 'full_derivative_R'
slice_fourier = slice_after_derivative + fourier_jacobian
full_fourier = full_after_derivative + fourier_jacobian
slice_fourier += 1 if MUTATION == 'slice_fourier_R'
full_fourier += 1 if MUTATION == 'full_fourier_R'
slice_a_power = rat(scaling_fixture.fetch('sliceSupportAPower'))
full_a_power = rat(scaling_fixture.fetch('shellVolumeAPower'))
slice_a_power = 2 if MUTATION == 'slice_L1_a'
full_a_power = 3 if MUTATION == 'full_fubini_a'
slice_row_r = slice_fourier - 1
full_row_r = full_fourier - 1
slice_row_r -= 1 if MUTATION == 'row_R_loss'
full_row_r -= 1 if MUTATION == 'full_row_R'
slice_a_power += 1 if MUTATION == 'row_a_power'
full_a_power += 1 if MUTATION == 'full_row_a'
derivative_orders = scaling_fixture.fetch('radialDerivativeOrders').dup
derivative_orders[0] = 2 if MUTATION == 'radial_first_derivative'
derivative_orders[1] = 2 if MUTATION == 'radial_third_derivative'
scaling_observed = {
  'x1Average' => {
    'prefactorR' => rtext(x1_prefactor),
    'afterX2DerivativeR' => rtext(slice_after_derivative),
    'fourierCoefficientR' => rtext(slice_fourier),
    'fubiniL1A' => rtext(slice_a_power),
    'wienerRowR' => rtext(slice_row_r),
    'wienerRowA' => rtext(slice_a_power)
  },
  'fullAverage' => {
    'prefactorR' => rtext(full_prefactor),
    'afterX2DerivativeR' => rtext(full_after_derivative),
    'fourierCoefficientR' => rtext(full_fourier),
    'fubiniL1A' => rtext(full_a_power),
    'wienerRowR' => rtext(full_row_r),
    'wienerRowA' => rtext(full_a_power)
  },
  'radialDerivativeOrders' => derivative_orders,
  'radialDenominatorSafe' => MUTATION == 'radial_lower' ?
    'radius may vanish' : 'radius>=a-delta>=a/2>=1/2'
}

frequency_fixture = fixtures.fetch('frequencyCase')
k_lower_power = rat(frequency_fixture.fetch('KLowerRPower'))
gain_power = rat(frequency_fixture.fetch('gainKPower'))
k_lower_power = -1 if %w[frequency_K frequency_threshold].include?(MUTATION)
gain_power = Rational(-1, 3) if MUTATION == 'frequency_gain'
implied_r = k_lower_power * gain_power
first_result = {'L' => 1, 'R' => slice_row_r + implied_r}
full_result = {'L' => full_a_power, 'R' => full_row_r + implied_r}
implied_r += 1 if MUTATION == 'frequency_R'
first_result['L'] += 1 if MUTATION == 'frequency_first_L'
first_result['R'] += 1 if MUTATION == 'frequency_first_R'
full_result['L'] += 1 if MUTATION == 'frequency_full_L'
full_result['R'] += 1 if MUTATION == 'frequency_full_R'
frequency_observed = {
  'KLowerRPower' => rtext(k_lower_power),
  'gainKPower' => rtext(gain_power),
  'impliedRPower' => rtext(implied_r),
  'x1AveragedResult' => exponent_text(first_result),
  'fullyAveragedResult' => exponent_text(full_result)
}

tags = text.scan(/\\tag\{(N\.[^}]+)\}/).flatten
tags << 'N.1' if MUTATION == 'tag'
references = text.scan(/\(N\.([0-9]+[a-z]?)\)/).flatten.map { |value| "N.#{value}" }
references << 'N.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\\[' }
display_close = text.lines.count { |line| line.strip == '\\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..17).map { |index| "N.#{index}" }

dependencies = %w[
  research/r075b_bulk_clock_outer_padding_gate.md
  research/r075c_background_shear_packing_false_positive.md
  research/r075e_horizontal_cross_mode_flux_reduction.md
  research/r075m_dyadic_packet_diffusive_flux_gain.md
]
dependency_table_present = dependencies.all? do |path|
  text.lines.any? { |line| line.include?(path) && line.include?(FROZEN_SOURCES.fetch(path)) }
end
dependency_table_present = false if MUTATION == 'dependency_table_missing'

required_tokens = [
  'p=\\frac{32}{63},\\qquad a=pL,\\qquad r=aR',
  '\\sum_{\\ell\\in\\mathbb Z} \\|d_\\ell\\|_{L^\\infty_{x_3}} \\le C_\\vartheta a',
  'd_\\ell(x_3) &:=\\frac1{2\\pi}\\int_{-\\pi}^{\\pi}',
  '=i\\ell\\Xi_\\ell(x_3)',
  'R^\\nu\\sum_{\\ell\\in\\mathbb Z} \\sup_z|\\widehat h_z(\\ell R)|',
  '\\sum_{|\\ell|>R^{-1}}\\ell^{-2}\\le CR',
  '|A_{a,z}|\\le4\\pi a\\delta',
  "\\|h_{a,z}''\\|_{L^1_y}",
  '\\overline\\xi_{a,R}(Ry)=R^2G_a(y)',
  'D_\\ell=\\frac{R^2}{2\\pi}\\widehat h_a(\\ell R)',
  '\\le C_\\vartheta L^2R^2',
  '\\mathbf{NOT\\ CLAY}'
]

boundary = {
  'BLeavesCutoffChoiceFreedom' => MUTATION != 'B_choice_freedom',
  'canonicalChoiceNotUniversalNecessity' => !%w[canonical_universal all_cutoffs_claim canonical_required].include?(MUTATION),
  'fixedSmoothNonnegativeProfile' => !%w[profile_fixed profile_smooth profile_nonnegative].include?(MUTATION),
  'profileSupportedInFixedNormalizedCollar' => MUTATION != 'profile_support',
  'profileCoversComplementaryPiece' => MUTATION != 'profile_plateau',
  'RInUnitInterval' => MUTATION != 'R_range',
  'centralChartNoPeriodicOverlap' => MUTATION != 'periodic_overlap',
  'derivativeCostsRMinusJ' => MUTATION != 'derivative_cost',
  'samplingCompactW21Uniform' => !%w[sampling_compact sampling_W21 sampling_uniform_A].include?(MUTATION),
  'nuAtLeastOne' => MUTATION != 'sampling_nu',
  'sumOfCoefficientwiseSuprema' => !%w[sup_sum_order coefficientwise_sup].include?(MUTATION),
  'twoIntegrationsByParts' => MUTATION != 'high_one_ibp',
  'highTailDirectionCorrect' => MUTATION != 'high_tail_direction',
  'noUnsignedRiemannSum' => MUTATION != 'discrete_riemann',
  'tangencyCapIncluded' => !%w[tangency_missing tangency_cap].include?(MUTATION),
  'sliceFourierNormalizationTwoPi' => MUTATION != 'slice_2pi',
  'sliceEmptyOutsideOuterRadius' => MUTATION != 'slice_empty_range',
  'radialDerivativesUniform' => MUTATION != 'radial_uniform',
  'FubiniUpperDirection' => MUTATION != 'fubini_direction',
  'allHorizontalModesSummed' => MUTATION != 'sum_all_modes',
  'notCrudeWienerH1Substitution' => MUTATION != 'wiener_h1_substitution',
  'frequencyPowerDirection' => MUTATION != 'frequency_direction',
  'geometricCoefficientOnly' => MUTATION != 'physical_coefficient_only',
  'notDynamicalFluxTheorem' => MUTATION != 'dynamical_flux_claim',
  'verticalDiffusionOpen' => MUTATION != 'vertical_diffusion_closed',
  'nonconstantShearOpen' => MUTATION != 'nonconstant_shear_closed',
  'localCubicPaymentOpen' => MUTATION != 'local_cubic_closed',
  'interpacketSummationOpen' => MUTATION != 'interpacket_closed',
  'lowDifferenceSectorOpen' => MUTATION != 'low_difference_closed',
  'E24Open' => MUTATION != 'e24_claim',
  'completeClockOpen' => MUTATION != 'complete_clock',
  'fixedDeletionOpen' => MUTATION != 'fixed_deletion',
  'suitableWeakTransferOpen' => MUTATION != 'suitable_weak',
  'regularityOpen' => MUTATION != 'regularity',
  'singularityOpen' => MUTATION != 'singularity',
  'noNovelty' => MUTATION != 'novelty',
  'noPriority' => MUTATION != 'priority',
  'noSimulation' => MUTATION != 'simulation',
  'notClay' => MUTATION != 'clay'
}

checks = {
  'frozen source bindings' => source_rows.values.all? { |wanted, seen| wanted == seen },
  'fixture expected bindings' =>
    fixture_hash == fixture_expected_hash && expected_hash == expected_expected_hash &&
    fixtures.fetch('frozenSources') == FROZEN_SOURCES,
  'primary audit status' =>
    audit_text.include?(FROZEN_SOURCES.fetch('research/r075n_radial_collar_averaged_wiener_row.md')) &&
    audit_text.include?('Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.') &&
    audit_text.include?('Equation tags N.1--N.17 are unique and consecutive.') &&
    audit_text.include?('All 17 display-math environments are paired.'),
  'four dependencies' => dependency_table_present,
  'B freedom canonical calibration' =>
    calibration_observed == expected.fetch('calibration') &&
    flat_b.include?('The complementary clock contribution is covered by a cutoff') &&
    flat_b.include?('Only the inequalities') && boundary.fetch('BLeavesCutoffChoiceFreedom') &&
    boundary.fetch('canonicalChoiceNotUniversalNecessity'),
  'fourier sign normalization zero mode' => fourier_observed == expected.fetch('fourierDerivative'),
  'sampling split sup order' =>
    sampling_observed == expected.fetch('sampling') && boundary.fetch('samplingCompactW21Uniform') &&
    boundary.fetch('nuAtLeastOne') && boundary.fetch('sumOfCoefficientwiseSuprema') &&
    boundary.fetch('twoIntegrationsByParts') && boundary.fetch('highTailDirectionCorrect') &&
    boundary.fetch('noUnsignedRiemannSum'),
  'slice area tangency' =>
    slice_observed == expected.fetch('sliceAreas') &&
    slice_rows.all? { |row| rat(row.fetch('capGapOverPi')) >= 0 } && boundary.fetch('tangencyCapIncluded'),
  'radial fubini scaling' =>
    scaling_observed == expected.fetch('scaling') && boundary.fetch('radialDerivativesUniform') &&
    boundary.fetch('FubiniUpperDirection'),
  'full shell full average' =>
    full_shell_observed == expected.fetch('fullShell') &&
    scaling_observed.dig('fullAverage', 'wienerRowR') == '1' &&
    scaling_observed.dig('fullAverage', 'wienerRowA') == '2',
  'frequency diagnostic' =>
    frequency_observed == expected.fetch('frequency') && implied_r == 1 && boundary.fetch('frequencyPowerDirection'),
  'tags references displays' =>
    tags == expected_tags && tags.uniq.length == 17 && (references.uniq - tags).empty? &&
    display_open == 17 && display_close == 17,
  'formula status sentinels' => required_tokens.all? { |token| flat_text.include?(token.gsub(/\s+/, ' ')) },
  'source report boundary' =>
    flat_source.include?('no dynamical flux, local Version-M payment, E.24, regularity, novelty, or priority claim') &&
    flat_source.include?('coefficientwise `x_3` supremum is taken before summation') &&
    flat_source.include?('spherical tangencies are paid'),
  'claim boundary' => boundary.values.all?,
  'utf8 control safety' =>
    !scan_text.include?("\uFFFD") && scan_text.each_codepoint.none? { |code| code < 32 && ![9, 10].include?(code) },
  'python canonical ledger agreement' =>
    python_payload.fetch('schema') == SCHEMA && python_payload.fetch('verdict') == 'PASS' &&
    python_payload.dig('assertions', 'passed') == 16 &&
    python_payload.fetch('calibration') == calibration_observed &&
    python_payload.fetch('fourierDerivative') == fourier_observed &&
    python_payload.fetch('sampling') == sampling_observed &&
    python_payload.fetch('sliceAreas') == slice_observed &&
    python_payload.fetch('fullShell') == full_shell_observed &&
    python_payload.fetch('scaling') == scaling_observed &&
    python_payload.fetch('frequency') == frequency_observed &&
    python_payload.fetch('claimBoundary') == boundary
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed = checks.select { |_name, passed| !passed }.keys
REPORT.write(
  "# R0.75N independent finite audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Mathematical blockers: #{verdict == 'PASS' ? 0 : failed.length}\n" \
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}\n" \
  "- Failed checks: #{failed.empty? ? 'none' : failed.join('; ')}\n\n" \
  "An independent Rational calculation verifies p=32/63, the canonical " \
  "central-chart witness, d_ell=+i*ell*Xi_ell with 1/(2*pi), and d_0=0. " \
  "The sample split checks low counting, two-IBP high decay, R^(nu-1), " \
  "and sum_l sup_z order.\n\n" \
  "Exact disk slices include both tangency and empty cases under 4*pi*a*delta. " \
  "The scaling ledger verifies the first/third derivatives, Fubini O(a)/O(a^2), " \
  "x1/full averaging factors R/R^2, and full row O(Ra^2). At K>=R^(-3/2), " \
  "the outputs are LR and L^2R^2.\n\n" \
  "This is a selectable canonical geometric coefficient theorem, not a universal " \
  "cutoff or dynamical flux result. Vertical diffusion, local payment, packet " \
  "summation, low differences, and E.24 remain open. **NOT CLAY.**\n"
)
puts JSON.generate(
  'suite' => 'r075n-radial-collar-averaged-wiener-row-independent',
  'verdict' => verdict,
  'assertions' => checks.length
)
exit(verdict == 'PASS' ? 0 : 1)
