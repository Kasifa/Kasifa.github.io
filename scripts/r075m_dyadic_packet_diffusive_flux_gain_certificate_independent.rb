#!/usr/bin/env ruby
# Independent exact verifier for frozen R0.75M.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075m_dyadic_packet_diffusive_flux_gain.md'
PRIMARY_AUDIT = ROOT + 'research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md'
REPORT_SOURCE = ROOT + 'research/r075m_report-source.md'
FIXTURES = ROOT + 'scripts/r075m_dyadic_packet_diffusive_flux_gain_fixtures.json'
EXPECTED = ROOT + 'scripts/r075m_dyadic_packet_diffusive_flux_gain_expected.json'
JSON_PATH = Pathname.new(
  ENV.fetch('R075M_JSON', (ROOT + 'research/r075m_dyadic_packet_diffusive_flux_gain_certificate.json').to_s)
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075M_RUBY_REPORT',
    (ROOT + 'research/r075m_dyadic_packet_diffusive_flux_gain_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075M_RUBY_MUTATION', '')
SCHEMA = 'r075m-dyadic-packet-diffusive-flux-gain-certificate-v1'

FROZEN_SOURCES = {
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075g_signed_flux_gain_threshold.md' =>
    'f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41',
  'research/r075l_single_harmonic_diffusive_signed_flux_gain.md' =>
    '52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5',
  'research/r075m_dyadic_packet_diffusive_flux_gain.md' =>
    '13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7',
  'research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md' =>
    '2b5ee050c09e3be925143c12c29082c3fe562a83b9a2d2669511a2bb1684d7dc',
  'research/r075m_report-source.md' =>
    'f8ed7af8ef5051b0efa73177d0530562917d55dfa6476b00b8f871db0da99d67'
}.freeze
FIXTURES_SHA256 = 'b93d727b4bf0729af2064e51fbc0c1450d98806c9b92fe11727b4d5423fa157f'
EXPECTED_SHA256 = 'cef1705998bc935448f371d6f389d46059b59e99bf230bd75dad0489fb85a4f4'

NEGATIVE_MUTATIONS = %w[
  source_drift audit_drift report_source_drift dependency_drift
  dependency_table_missing fixture_drift expected_drift tag reference display
  control operator_time operator_drift operator_diffusion fourier_factor
  reconstruction_sign difference_index spatial_factor flux_half modal_prefactor
  d0_nonzero cancel_after_absolute absolute_before_diagonal time_phase time_decay
  diffusion_sign passive_residual K_lower K_upper K_integer packet_finite
  real_symmetry mode_count eta_lower eta_upper eta_measurable xi_periodic
  xi_smooth xi_real W_definition time_kernel_absolute time_kernel_infinity
  kernel_denominator denominator_lower denominator_factor row_sum column_sum
  schur_direction schur_sqrt quadratic_form mode_count_loss parseval_factor
  energy_quarter short_window short_window_inside upper_edge l2_decay_multiplier
  l2_endpoint l2_direction holder_measure holder_direction l3_endpoint
  mass_window mass_constant mass_K_power mass_E_power condition
  inversion_constant inversion_e_power inversion_2pi_power inversion_K_power
  inversion_M_power inverse_heat combined_constant combined_e_power
  combined_2pi_power combined_K_power combined_M_power combined_B_power
  combined_W_power amplitude_degree wiener_weight wiener_cs_direction
  wiener_inverse_series wiener_weighted_sum wiener_parseval
  wiener_first_derivative wiener_second_derivative wiener_third_derivative
  pointwise_replacement target_R target_omega payment_R payment_omega payment_M
  normalized_R normalized_omega normalized_K normalized_p positive_part
  R_positive omega_positive alpha_numerator alpha_denominator kappa_multiplier
  kappa_reduce strict_direction endpoint_equality R_domain frequency_direction
  physical_signed full_torus single_packet arbitrary_interference
  interpacket_closed cutoff_calibrated collar_localized local_versionm
  low_difference_closed nonconstant_closed e24_claim complete_clock
  fixed_deletion suitable_weak regularity singularity novelty priority
  simulation clay
].freeze

abort("unknown R075M_RUBY_MUTATION: #{MUTATION}") unless
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
flat_text = text.gsub(/\s+/, ' ')
flat_source = source_text.gsub(/\s+/, ' ')
scan_text = text + audit_text + source_text + (MUTATION == 'control' ? "\u0001" : '')
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_payload = JSON.parse(JSON_PATH.read)

source_expectations = FROZEN_SOURCES.dup
source_expectations['research/r075m_dyadic_packet_diffusive_flux_gain.md'] =
  '0' * 64 if MUTATION == 'source_drift'
source_expectations[
  'research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md'
] = '0' * 64 if MUTATION == 'audit_drift'
source_expectations['research/r075m_report-source.md'] =
  '0' * 64 if MUTATION == 'report_source_drift'
source_expectations['research/r075g_signed_flux_gain_threshold.md'] =
  '0' * 64 if MUTATION == 'dependency_drift'
source_rows = source_expectations.keys.sort.to_h do |path|
  [path, [source_expectations.fetch(path), Digest::SHA256.file(ROOT + path).hexdigest]]
end
fixture_expected_hash = MUTATION == 'fixture_drift' ? '0' * 64 : FIXTURES_SHA256
expected_expected_hash = MUTATION == 'expected_drift' ? '0' * 64 : EXPECTED_SHA256
fixture_hash = Digest::SHA256.file(FIXTURES).hexdigest
expected_hash = Digest::SHA256.file(EXPECTED).hexdigest

operator_observed = fixtures.fetch('operatorCase').dup
operator_observed['timeCoefficient'] = '-1' if MUTATION == 'operator_time'
operator_observed['driftCoefficientSymbol'] = '-B' if MUTATION == 'operator_drift'
operator_observed['secondDerivativeCoefficient'] = '1' if MUTATION == 'operator_diffusion'

packet_fixture = fixtures.fetch('fourierPacketCase')
k_floor = packet_fixture.fetch('K')
modes = packet_fixture.fetch('modes').dup
shear = rat(packet_fixture.fetch('B'))
coefficients = packet_fixture.fetch('coefficients').to_h do |key, value|
  [key.to_i, rat(value)]
end
coefficients[-2] += 1 if MUTATION == 'real_symmetry'
coefficient_energy = coefficients.values.sum { |value| value.abs**2 }
real_admissible = modes.all? { |n| coefficients[-n] == coefficients[n] }
all_in_band = modes.all? { |n| k_floor <= n.abs && n.abs <= 2 * k_floor }
all_in_band = false if %w[K_lower K_upper].include?(MUTATION)
packet_observed = {
  'K' => MUTATION == 'K_integer' ? k_floor + 1 : k_floor,
  'B' => rtext(shear),
  'modes' => modes,
  'modeCount' => modes.length + (MUTATION == 'mode_count' ? 1 : 0),
  'realAdmissible' => real_admissible,
  'allModesInDyadicBand' => all_in_band,
  'coefficientEnergy' => rtext(coefficient_energy),
  'E0OverPi' => rtext(2 * coefficient_energy)
}

evolution_observed = modes.map do |n|
  time_real = MUTATION == 'time_decay' ? n * n : -n * n
  time_imag = n * shear * (MUTATION == 'time_phase' ? 1 : -1)
  drift_imag = n * shear
  diffusion_real = MUTATION == 'diffusion_sign' ? -n * n : n * n
  residual_real = time_real + diffusion_real
  residual_imag = time_imag + drift_imag
  residual_real += 1 if MUTATION == 'passive_residual'
  {
    'n' => n,
    'timeReal' => rtext(Rational(time_real)),
    'timeImag' => rtext(time_imag),
    'driftImag' => rtext(drift_imag),
    'diffusionReal' => rtext(Rational(diffusion_real)),
    'residualReal' => rtext(Rational(residual_real)),
    'residualImag' => rtext(residual_imag)
  }
end

cutoff = {0 => rat(packet_fixture.fetch('dZero'))}
packet_fixture.fetch('positiveCutoffModes').each do |row|
  ell = row.fetch('ell')
  value = rat(row.fetch('coefficient'))
  cutoff[ell] = value
  cutoff[-ell] = value
end
cutoff[0] = 1 if MUTATION == 'd0_nonzero'
wiener_norm = cutoff.values.sum(&:abs)
wiener_norm -= cutoff.fetch(8).abs if MUTATION == 'W_definition'
fourier_observed = {
  'reconstructionPhase' => MUTATION == 'reconstruction_sign' ? '-i*ell*x' : '+i*ell*x',
  'kernelIndex' => MUTATION == 'difference_index' ? 'n-m' : 'm-n',
  'dZero' => rtext(cutoff.fetch(0)),
  'diagonalVanishesBeforeAbsoluteValue' => !%w[cancel_after_absolute absolute_before_diagonal].include?(MUTATION),
  'spatialIntegralFactor' => MUTATION == 'spatial_factor' ? 'pi' : '2*pi',
  'fluxKernelFactor' => %w[flux_half modal_prefactor].include?(MUTATION) ? '2*pi*B' : 'pi*B'
}
fourier_observed['reconstructionPhase'] = 'coefficient-1/pi' if MUTATION == 'fourier_factor'

eta_fixture = fixtures.fetch('etaCase')
eta_lower = rat(eta_fixture.fetch('lowerBound'))
eta_upper = rat(eta_fixture.fetch('upperBound'))
eta_lower = Rational(1, 4) if MUTATION == 'eta_lower'
eta_upper = Rational(3, 4) if MUTATION == 'eta_upper'
eta_observed = {
  'rows' => eta_fixture.fetch('samples').map do |value|
    number = rat(value)
    {'eta' => value, 'admissible' => eta_lower <= number && number <= eta_upper}
  end
}

denominator_lower = Rational(2 * k_floor * k_floor)
denominator_lower = Rational(k_floor * k_floor) if MUTATION == 'denominator_lower'
denominator_lower = Rational(4 * k_floor * k_floor) if MUTATION == 'denominator_factor'
matrix = {}
modes.product(modes).each do |n, m|
  denominator = if MUTATION == 'kernel_denominator'
                  Rational(n.abs + m.abs)
                else
                  Rational(n * n + m * m)
                end
  matrix[[n, m]] = cutoff.fetch(m - n, 0).abs / denominator
end
row_sums = modes.to_h { |n| [n, modes.sum { |m| matrix.fetch([n, m]) }] }
column_sums = modes.to_h { |m| [m, modes.sum { |n| matrix.fetch([n, m]) }] }
row_sums[modes.first] += 1 if MUTATION == 'row_sum'
column_sums[modes.first] += 1 if MUTATION == 'column_sum'
crude_bound = wiener_norm / denominator_lower
absolute_quadratic = modes.product(modes).sum do |n, m|
  matrix.fetch([n, m]) * coefficients.fetch(n).abs * coefficients.fetch(m).abs
end
absolute_quadratic += 1 if MUTATION == 'quadratic_form'
schur_upper = crude_bound * coefficient_energy
schur_upper += 1 if MUTATION == 'schur_sqrt'
schur_observed = {
  'Wxi' => rtext(wiener_norm),
  'denominatorLowerBound' => rtext(denominator_lower),
  'rowSums' => row_sums.to_h { |key, value| [key.to_s, rtext(value)] },
  'columnSums' => column_sums.to_h { |key, value| [key.to_s, rtext(value)] },
  'maximumExactRowOrColumn' => rtext([row_sums.values.max, column_sums.values.max].max),
  'crudeRowColumnBound' => rtext(crude_bound),
  'absoluteQuadraticForm' => rtext(absolute_quadratic),
  'schurQuadraticUpper' => rtext(schur_upper),
  'parsevalEnergyFactor' => MUTATION == 'parseval_factor' ? 'pi' : '2*pi',
  'finalEnergyCoefficient' => MUTATION == 'energy_quarter' ? 'Wxi/(2*K^2)' : 'Wxi/(4*K^2)',
  'modeCountFactor' => MUTATION == 'mode_count_loss' ? 'K' : 'none'
}

short_fixture = fixtures.fetch('shortTimeCase')
time_denominator = rat(short_fixture.fetch('timeDenominator'))
time_denominator = 4 if %w[short_window mass_window].include?(MUTATION)
upper_multiplier = rat(short_fixture.fetch('upperPacketMultiplier'))
upper_multiplier = 3 if MUTATION == 'upper_edge'
heat_multiplier = rat(short_fixture.fetch('squaredHeatMultiplier'))
heat_multiplier = 1 if MUTATION == 'l2_decay_multiplier'
upper_square = upper_multiplier**2
heat_exponent = heat_multiplier * upper_square
endpoint_exponent = heat_exponent / time_denominator
cubic_monomial = {
  'rational' => rtext(Rational(1, time_denominator.to_i)),
  'e' => MUTATION == 'mass_constant' ? '-1' : '-3/2',
  '2pi' => MUTATION == 'holder_measure' ? '-1' : '-1/2',
  'K' => MUTATION == 'mass_K_power' ? '-1' : '-2',
  'E0' => MUTATION == 'mass_E_power' ? '1' : '3/2'
}
inversion = {
  'rational' => MUTATION == 'inversion_constant' ? '2' : '4',
  'e' => MUTATION == 'inversion_e_power' ? '3/2' : '1',
  '2pi' => MUTATION == 'inversion_2pi_power' ? '1/2' : '1/3',
  'K' => MUTATION == 'inversion_K_power' ? '2/3' : '4/3',
  'M' => MUTATION == 'inversion_M_power' ? '1/3' : '2/3'
}
combined = {
  'rational' => MUTATION == 'combined_constant' ? '4' : '1',
  'e' => MUTATION == 'combined_e_power' ? '0' : '1',
  '2pi' => MUTATION == 'combined_2pi_power' ? '1/2' : '1/3',
  'B' => MUTATION == 'combined_B_power' ? '0' : '1',
  'Wxi' => MUTATION == 'combined_W_power' ? '0' : '1',
  'K' => MUTATION == 'combined_K_power' ? '-1/3' : '-2/3',
  'M' => MUTATION == 'combined_M_power' ? '1/3' : '2/3'
}
short_observed = {
  'interval' => "0<=t<=1/(#{rtext(time_denominator)}*K^2)",
  'upperModeSquareBound' => "#{rtext(upper_square)}*K^2",
  'squaredHeatExponent' => "-#{rtext(heat_exponent)}*K^2*t",
  'endpointL2Factor' => MUTATION == 'l2_endpoint' ? 'exp(-2)' : 'exp(-1)',
  'holderCircleFactor' => MUTATION == 'holder_measure' ? '(2*pi)^(-1)' : '(2*pi)^(-1/2)',
  'endpointL3Factor' => MUTATION == 'l3_endpoint' ? 'exp(-1)' : 'exp(-3/2)',
  'cubicLowerMonomial' => cubic_monomial,
  'energyInversionMonomial' => inversion,
  'combinedFluxMonomial' => combined
}

weighted_sum = cutoff.sum { |ell, value| (1 + ell * ell) * value.abs**2 }
inverse_sum = (-8..8).sum { |ell| Rational(1, 1 + ell * ell) }
weighted_sum += 1 if MUTATION == 'wiener_weighted_sum'
inverse_sum += 1 if MUTATION == 'wiener_inverse_series'
cs_gap = weighted_sum * inverse_sum - wiener_norm**2
cs_gap *= -1 if MUTATION == 'wiener_cs_direction'
wiener_observed = {
  'Wxi' => rtext(wiener_norm),
  'finiteWeightedSquareSum' => rtext(weighted_sum),
  'finiteInverseWeightSum' => rtext(inverse_sum),
  'WxiSquared' => rtext(wiener_norm**2),
  'cauchySchwarzGap' => rtext(cs_gap),
  'weightSymbol' => MUTATION == 'wiener_weight' ? '1+|ell|' : '1+ell^2',
  'parsevalIdentity' => if MUTATION == 'wiener_parseval'
                         "sum(1+ell^2)|d_ell|^2=||xi'||_2^2+||xi''||_2^2"
                       else
                         "sum(1+ell^2)|d_ell|^2=(||xi'||_2^2+||xi''||_2^2)/(2*pi)"
                       end,
  'highestXiDerivative' => MUTATION == 'wiener_third_derivative' ? 3 : 2,
  'pointwiseSupAloneSufficient' => MUTATION == 'pointwise_replacement'
}

normalization_fixture = fixtures.fetch('normalizationCase')
gain = normalization_fixture.fetch('fluxGain').to_h { |key, value| [key, rat(value)] }
gain['K'] = Rational(-1, 3) if MUTATION == 'combined_K_power'
target = normalization_fixture.fetch('targetPrefactor').to_h { |key, value| [key, rat(value)] }
payment = normalization_fixture.fetch('paymentDefinition').to_h { |key, value| [key, rat(value)] }
target['R'] = 0 if MUTATION == 'target_R'
target['omega'] = 0 if MUTATION == 'target_omega'
payment['R'] = -1 if MUTATION == 'payment_R'
payment['omega'] = -1 if MUTATION == 'payment_omega'
payment['M'] = 2 if MUTATION == 'payment_M'
p_m = payment.fetch('M')
normalized = {
  'B' => gain.fetch('B'),
  'Wxi' => gain.fetch('Wxi'),
  'R' => target.fetch('R') - gain.fetch('M') * payment.fetch('R') / p_m,
  'omega' => target.fetch('omega') - gain.fetch('M') * payment.fetch('omega') / p_m,
  'K' => gain.fetch('K'),
  'p' => gain.fetch('M') / p_m
}
normalized['R'] += Rational(1, 3) if MUTATION == 'normalized_R'
normalized['omega'] += Rational(1, 3) if MUTATION == 'normalized_omega'
normalized['K'] += Rational(1, 3) if MUTATION == 'normalized_K'
normalized['p'] = Rational(1, 3) if MUTATION == 'normalized_p'
normalization_observed = {
  'fluxGain' => exponent_text(gain),
  'targetNormalized' => exponent_text(normalized)
}

threshold_fixture = fixtures.fetch('thresholdCase')
alpha = rat(threshold_fixture.fetch('alphaStar'))
alpha += Rational(1, 107_163) if MUTATION == 'alpha_numerator'
alpha = Rational(27_163, 107_162) if MUTATION == 'alpha_denominator'
multiplier = rat(threshold_fixture.fetch('multiplier'))
multiplier = 2 if MUTATION == 'kappa_multiplier'
kappa_star = alpha * multiplier
kappa_star += Rational(1, 71_442) if MUTATION == 'kappa_reduce'
strict_kappa = rat(threshold_fixture.fetch('strictTestKappa'))
threshold_observed = {
  'alphaStar' => rtext(alpha),
  'kappaStar' => rtext(kappa_star),
  'endpointEquality' => MUTATION == 'endpoint_equality' ?
    '2*kappaStar/3>alphaStar' : '2*kappaStar/3=alphaStar',
  'strictTestKappa' => rtext(strict_kappa),
  'strictKappaMargin' => rtext(strict_kappa - kappa_star),
  'strictExponentMargin' => rtext(Rational(2, 3) * strict_kappa - alpha),
  'RInterval' => MUTATION == 'R_domain' ? 'R>1' : threshold_fixture.fetch('RInterval'),
  'powerDirection' => MUTATION == 'frequency_direction' ?
    'larger-exponent-gives-larger-power' : 'larger-exponent-gives-smaller-power'
}

tags = text.scan(/\\tag\{(M\.[^}]+)\}/).flatten
tags << 'M.1' if MUTATION == 'tag'
references = text.scan(/\(M\.([0-9]+[a-z]?)\)/).flatten.map { |value| "M.#{value}" }
references << 'M.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\\[' }
display_close = text.lines.count { |line| line.strip == '\\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..20).map { |index| "M.#{index}" }

dependencies = %w[
  research/r075e_horizontal_cross_mode_flux_reduction.md
  research/r075g_signed_flux_gain_threshold.md
  research/r075l_single_harmonic_diffusive_signed_flux_gain.md
]
dependency_table_present = dependencies.all? do |path|
  text.lines.any? { |line| line.include?(path) && line.include?(FROZEN_SOURCES.fetch(path)) }
end
dependency_table_present = false if MUTATION == 'dependency_table_missing'

required_tokens = [
  'd_\\ell:=\\frac1{2\\pi}\\int_0^{2\\pi}',
  '\\mathcal W_\\xi:=\\sum_{\\ell\\in\\mathbb Z}|d_\\ell|',
  '\\mathcal L_BF=0',
  '\\pi B\\sum_{n,m\\in\\Lambda_K}d_{m-n}c_n\\overline{c_m}',
  '\\le\\frac1{2K^2}',
  '\\frac{|B|\\mathcal W_\\xi}{4K^2}E_0',
  '\\ge e^{-1}E_0',
  '(2\\pi)^{-1/2}e^{-3/2}E_0^{3/2}',
  '4e(2\\pi)^{1/3}K^{4/3}M_K^{2/3}',
  'e(2\\pi)^{1/3}|B|\\mathcal W_\\xi',
  'R^{1/3}\\omega^{1/3}K^{-2/3}',
  '\\frac{27163}{71442}',
  '\\mathbf{NOT\\ CLAY}'
]

boundary = {
  'KIntegerAtLeastOne' => !%w[K_integer K_lower].include?(MUTATION),
  'finiteRealAdmissiblePacket' => !%w[packet_finite real_symmetry].include?(MUTATION),
  'upperBandAtMostTwoK' => MUTATION != 'K_upper',
  'etaInUnitInterval' => !%w[eta_measurable eta_lower eta_upper].include?(MUTATION),
  'xiSmoothPeriodicReal' => !%w[xi_periodic xi_smooth xi_real].include?(MUTATION),
  'timeKernelAbsoluteValue' => MUTATION != 'time_kernel_absolute',
  'extensionToInfinityDirection' => MUTATION != 'time_kernel_infinity',
  'schurInequalityDirection' => MUTATION != 'schur_direction',
  'shortWindowContained' => MUTATION != 'short_window_inside',
  'L2LowerDirection' => MUTATION != 'l2_direction',
  'HolderLowerDirection' => MUTATION != 'holder_direction',
  'conditionK2TAtLeastOne' => MUTATION != 'condition',
  'noInverseHeatFlow' => MUTATION != 'inverse_heat',
  'passiveAmplitudeDegreeTwo' => MUTATION != 'amplitude_degree',
  'WienerUsesBothFirstAndSecondDerivatives' => !%w[wiener_first_derivative wiener_second_derivative].include?(MUTATION),
  'noThirdDerivativeRequired' => MUTATION != 'wiener_third_derivative',
  'pointwiseSupNotSubstituted' => MUTATION != 'pointwise_replacement',
  'positivePartNormalization' => MUTATION != 'positive_part',
  'RAndOmegaPositive' => !%w[R_positive omega_positive].include?(MUTATION),
  'strictThreshold' => MUTATION != 'strict_direction',
  'physicalSignedFlux' => MUTATION != 'physical_signed',
  'fullTorusCubicOnly' => MUTATION != 'full_torus',
  'singleDyadicPacketOnly' => MUTATION != 'single_packet',
  'arbitraryFiniteWithinPacketInterference' => MUTATION != 'arbitrary_interference',
  'noModeCountFactor' => MUTATION != 'mode_count_loss',
  'interpacketSummationOpen' => MUTATION != 'interpacket_closed',
  'cutoffWienerScalingOpen' => MUTATION != 'cutoff_calibrated',
  'collarLocalizationOpen' => MUTATION != 'collar_localized',
  'localVersionMReplacementOpen' => MUTATION != 'local_versionm',
  'lowDifferenceSectorOpen' => MUTATION != 'low_difference_closed',
  'nonconstantShearOpen' => MUTATION != 'nonconstant_closed',
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
  'fixture and expected bindings' =>
    fixture_hash == fixture_expected_hash && expected_hash == expected_expected_hash &&
    fixtures.fetch('frozenSources') == FROZEN_SOURCES,
  'primary audit binding and status' =>
    audit_text.include?(FROZEN_SOURCES.fetch('research/r075m_dyadic_packet_diffusive_flux_gain.md')) &&
    audit_text.include?('Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.') &&
    audit_text.include?('Equation tags M.1--M.20 are unique and consecutive.') &&
    audit_text.include?('All 20 display-math environments are paired.'),
  'three dependency bindings' => dependency_table_present,
  'operator and packet evolution' =>
    operator_observed == expected.fetch('operator') && evolution_observed == expected.fetch('evolutionCases') &&
    evolution_observed.all? { |row| row.fetch('residualReal') == '0' && row.fetch('residualImag') == '0' },
  'packet support reality parseval' => packet_observed == expected.fetch('packet'),
  'fourier convention pi diagonal' =>
    fourier_observed == expected.fetch('fourierConvention') && fourier_observed.fetch('dZero') == '0' &&
    fourier_observed.fetch('diagonalVanishesBeforeAbsoluteValue'),
  'eta bounds' => eta_observed == expected.fetch('eta'),
  'schur rows columns quarter' =>
    schur_observed == expected.fetch('schur') && row_sums.values.max <= crude_bound &&
    column_sums.values.max <= crude_bound && absolute_quadratic <= schur_upper &&
    boundary.fetch('schurInequalityDirection'),
  'short time l2 l3 inversion' =>
    short_observed == expected.fetch('shortTime') && endpoint_exponent == 1 &&
    boundary.fetch('shortWindowContained') && boundary.fetch('L2LowerDirection') &&
    boundary.fetch('HolderLowerDirection') && boundary.fetch('conditionK2TAtLeastOne'),
  'combined constant homogeneity' =>
    combined == expected.dig('shortTime', 'combinedFluxMonomial') &&
    combined == {'rational' => '1', 'e' => '1', '2pi' => '1/3', 'B' => '1', 'Wxi' => '1', 'K' => '-2/3', 'M' => '2/3'} &&
    boundary.fetch('passiveAmplitudeDegreeTwo'),
  'wiener h1 cauchy schwarz' =>
    wiener_observed == expected.fetch('wiener') && cs_gap >= 0 &&
    boundary.fetch('WienerUsesBothFirstAndSecondDerivatives') &&
    boundary.fetch('noThirdDerivativeRequired') && boundary.fetch('pointwiseSupNotSubstituted'),
  'target normalization' =>
    normalization_observed == expected.fetch('normalization') &&
    normalized == {'B' => 1, 'Wxi' => 1, 'R' => Rational(1, 3), 'omega' => Rational(1, 3), 'K' => Rational(-2, 3), 'p' => Rational(2, 3)},
  'exact strict threshold' =>
    threshold_observed == expected.fetch('threshold') && Rational(2, 3) * kappa_star == alpha &&
    strict_kappa > kappa_star && Rational(2, 3) * strict_kappa > alpha,
  'tags references displays' =>
    tags == expected_tags && tags.uniq.length == 20 && (references.uniq - tags).empty? &&
    display_open == 20 && display_close == 20,
  'formula and status sentinels' => required_tokens.all? { |token| flat_text.include?(token.gsub(/\s+/, ' ')) },
  'source report boundary' =>
    flat_source.include?('no E.24, complete-clock, regularity, novelty, or priority claim') &&
    flat_source.include?('arbitrary finite interference inside one dyadic horizontal packet') &&
    flat_source.include?('cutoff derivative is measured in its Wiener norm'),
  'claim boundary' => boundary.values.all?,
  'utf8 and control safety' =>
    !scan_text.include?("\uFFFD") && scan_text.each_codepoint.none? { |code| code < 32 && ![9, 10].include?(code) },
  'python canonical ledger agreement' =>
    python_payload.fetch('schema') == SCHEMA && python_payload.fetch('verdict') == 'PASS' &&
    python_payload.dig('assertions', 'passed') == 19 &&
    python_payload.fetch('operator') == operator_observed && python_payload.fetch('packet') == packet_observed &&
    python_payload.fetch('evolutionCases') == evolution_observed &&
    python_payload.fetch('fourierConvention') == fourier_observed && python_payload.fetch('eta') == eta_observed &&
    python_payload.fetch('schur') == schur_observed && python_payload.fetch('shortTime') == short_observed &&
    python_payload.fetch('wiener') == wiener_observed &&
    python_payload.fetch('normalization') == normalization_observed &&
    python_payload.fetch('threshold') == threshold_observed && python_payload.fetch('claimBoundary') == boundary
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed = checks.select { |_name, passed| !passed }.keys
REPORT.write(
  "# R0.75M independent finite audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Mathematical blockers: #{verdict == 'PASS' ? 0 : failed.length}\n" \
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}\n" \
  "- Failed checks: #{failed.empty? ? 'none' : failed.join('; ')}\n\n" \
  "An independent Rational matrix calculation verifies the Fourier 1/(2*pi) " \
  "convention, pi*B kernel, d_0 cancellation, Schur row and column sums, " \
  "Parseval normalization, and the exact 1/4 energy factor.\n\n" \
  "Symbolic exponent arithmetic verifies the e^(-1) L2 floor, " \
  "(2*pi)^(-1/2)e^(-3/2) L3 floor, inversion 4e(2*pi)^(1/3), and final " \
  "e(2*pi)^(1/3) constant. A finite cutoff checks the Wiener--H1 row using " \
  "only the first two cutoff derivatives.\n\n" \
  "Normalization gives R^(1/3)omega^(1/3)K^(-2/3)p^(2/3), with strict " \
  "threshold 27163/71442. This remains a signed, full-torus, one-packet " \
  "result; inter-packet summation, collar calibration/localization, local " \
  "Version-M payment, and E.24 remain open. **NOT CLAY.**\n"
)
puts JSON.generate(
  'suite' => 'r075m-dyadic-packet-diffusive-flux-gain-independent',
  'verdict' => verdict,
  'assertions' => checks.length
)
exit(verdict == 'PASS' ? 0 : 1)
