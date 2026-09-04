#!/usr/bin/env ruby
# Independent exact verifier for frozen R0.75L.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075l_single_harmonic_diffusive_signed_flux_gain.md'
PRIMARY_AUDIT = ROOT + 'research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md'
REPORT_SOURCE = ROOT + 'research/r075l_report-source.md'
FIXTURES = ROOT + 'scripts/r075l_single_harmonic_diffusive_signed_flux_gain_fixtures.json'
EXPECTED = ROOT + 'scripts/r075l_single_harmonic_diffusive_signed_flux_gain_expected.json'
JSON_PATH = Pathname.new(
  ENV.fetch(
    'R075L_JSON',
    (ROOT + 'research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json').to_s
  )
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075L_RUBY_REPORT',
    (ROOT + 'research/r075l_single_harmonic_diffusive_signed_flux_gain_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075L_RUBY_MUTATION', '')
SCHEMA = 'r075l-single-harmonic-diffusive-signed-flux-gain-certificate-v1'

FROZEN_SOURCES = {
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075g_signed_flux_gain_threshold.md' =>
    'f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41',
  'research/r075k_positive_majorant_high_frequency_trace_loss.md' =>
    '9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf',
  'research/r075l_single_harmonic_diffusive_signed_flux_gain.md' =>
    '52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5',
  'research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md' =>
    'a7578e5370d182decc39f0da2f2fb581e5ef842ae7b914a120b5784bc32bd302',
  'research/r075l_report-source.md' =>
    'a300de54b9fe06e94455a055bbb42bdce8ec7bb004080389a95412966a5b941a'
}.freeze
FIXTURES_SHA256 = '0b9ba1f018b6e52414f20dee6687f5ff55c5ea0ef247ddbd905bc8c204245ad9'
EXPECTED_SHA256 = '9178489eaf9f44c5b182b6080cce7212591b1a3dd86459ecbd82c1382b38db9a'

NEGATIVE_MUTATIONS = %w[
  source_drift audit_drift report_source_drift dependency_drift
  dependency_table_missing fixture_drift expected_drift tag reference display
  control operator_time operator_drift_symbol operator_diffusion time_decay
  time_phase drift_phase diffusion_sign passive_residual k_integer k_lower
  A_positive B_real real_field constant_shear single_harmonic square_frequency
  square_zero_coefficient square_side_coefficient diagonal_not_zero
  diagonal_after_absolute periodic_mean absolute_before_cancel eta_lower
  eta_upper eta_sample eta_measurable xi_periodic xi_smooth xi_real
  vxi_absolute vxi_bound time_decay_multiplier time_integral_sign
  time_integral_denominator q2_symbol q2_interval drop_q2_direction flux_half
  flux_square_half flux_coefficient flux_B_absolute flux_Vxi cos_quarter
  cos_symmetry cos_integral mass_decay_multiplier mass_denominator
  mass_amplitude mass_k_square mass_symbol q3_symbol condition_direction
  condition_one q3_comparison q3_float_equality c3_positive c3_symbol
  a2_prefactor a2_power_k a2_power_mass a2_inequality cstar_outer cstar_inner
  flux_A flux_k mass_A mass_k two_thirds ratio_k amplitude_cancel target_omega
  target_R payment_R payment_omega payment_M normalized_R normalized_omega
  normalized_k normalized_p positive_part alpha_numerator alpha_denominator
  kappa_multiplier kappa_reduce endpoint_equality decimal_display decimal_exact
  strict_direction R_interval frequency_direction physical_signed full_torus
  unpaid_BVxi g1_claim e24_claim full_versionm_claim multimode_closed
  collar_closed nonconstant_closed low_frequency_closed complete_clock
  fixed_deletion suitable_weak regularity singularity novelty priority
  simulation clay
].freeze

abort("unknown R075L_RUBY_MUTATION: #{MUTATION}") unless
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

def rounded_decimal(value, digits)
  scale = 10**digits
  scaled = value * scale
  rounded = (2 * scaled.numerator + scaled.denominator) / (2 * scaled.denominator)
  whole, fraction = rounded.divmod(scale)
  format("%d.%0#{digits}d", whole, fraction)
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
source_expectations['research/r075l_single_harmonic_diffusive_signed_flux_gain.md'] =
  '0' * 64 if MUTATION == 'source_drift'
source_expectations[
  'research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md'
] = '0' * 64 if MUTATION == 'audit_drift'
source_expectations['research/r075l_report-source.md'] =
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

# Reconstruct L_B and the exact Fourier-mode identities from fixture primitives.
operator_observed = fixtures.fetch('operatorCase').dup
operator_observed['timeCoefficient'] = '-1' if MUTATION == 'operator_time'
operator_observed['driftCoefficientSymbol'] = '-B' if MUTATION == 'operator_drift_symbol'
operator_observed['secondDerivativeCoefficient'] = '1' if MUTATION == 'operator_diffusion'

family_fixture = fixtures.fetch('passiveFamilyCase')
amplitude = rat(family_fixture.fetch('A'))
amplitude += 1 if MUTATION == 'mass_amplitude'
shear = rat(family_fixture.fetch('B'))
variation = rat(family_fixture.fetch('Vxi'))

eta_fixture = fixtures.fetch('etaCase')
eta_lower = rat(eta_fixture.fetch('lowerBound'))
eta_upper = rat(eta_fixture.fetch('upperBound'))
eta_lower = Rational(1, 2) if MUTATION == 'eta_lower'
eta_upper = 2 if MUTATION == 'eta_upper'
eta_samples = eta_fixture.fetch('allowedSamples').map { |value| rat(value) }
eta_samples[1] = Rational(4, 3) if MUTATION == 'eta_sample'
eta_observed = {
  'rows' => eta_samples.map do |value|
    {'eta' => rtext(value), 'admissible' => eta_lower <= value && value <= eta_upper}
  end,
  'absoluteValueMayUseEtaUpperBound' => MUTATION != 'eta_upper'
}

time_fixture = fixtures.fetch('timeIntegralCase')
decay_two = rat(time_fixture.fetch('decayMultiplier'))
decay_two = 1 if MUTATION == 'time_decay_multiplier'
time_observed = {
  'exactSymbol' => if MUTATION == 'time_integral_sign'
                     '(q2-1)/(2*k^2)'
                   elsif MUTATION == 'time_integral_denominator'
                     '(1-q2)/(k^2)'
                   else
                     '(1-q2)/(2*k^2)'
                   end,
  'q2Symbol' => MUTATION == 'q2_symbol' ? 'exp(-k^2*T)' : time_fixture.fetch('q2Symbol'),
  'q2Interval' => MUTATION == 'q2_interval' ? 'q2>1' : '0<q2<1',
  'dropFactorDirection' => MUTATION == 'drop_q2_direction' ? '1-q2>=1' : '1-q2<=1'
}

moment_fixture = fixtures.fetch('absoluteCosineMoment')
quarter = rat(moment_fixture.fetch('quarterIntegral'))
symmetry = rat(moment_fixture.fetch('symmetryFactor'))
quarter += Rational(1, 3) if MUTATION == 'cos_quarter'
symmetry = 2 if MUTATION == 'cos_symmetry'
full_moment = quarter * symmetry
full_moment += 1 if MUTATION == 'cos_integral'
moment_observed = {
  'quarterIntegral' => rtext(quarter),
  'symmetryFactor' => rtext(symmetry),
  'fullIntegral' => rtext(full_moment)
}

mass_fixture = fixtures.fetch('massConversionCase')
decay_three = rat(mass_fixture.fetch('decayMultiplier'))
decay_three = 2 if MUTATION == 'mass_decay_multiplier'

family_observed = family_fixture.fetch('integerK').map do |k|
  time_cos = MUTATION == 'time_decay' ? k * k : -k * k
  time_sin = shear * k * (MUTATION == 'time_phase' ? -1 : 1)
  drift_sin = shear * k * (MUTATION == 'drift_phase' ? 1 : -1)
  diffusion_cos = MUTATION == 'diffusion_sign' ? -k * k : k * k
  residual_cos = time_cos + diffusion_cos
  residual_sin = time_sin + drift_sin
  residual_cos += 1 if MUTATION == 'passive_residual'
  square_frequency = MUTATION == 'square_frequency' ? k : 2 * k
  square_zero = amplitude**2 * (MUTATION == 'square_zero_coefficient' ? 1 : Rational(1, 2))
  square_side = amplitude**2 * (MUTATION == 'square_side_coefficient' ? Rational(1, 2) : Rational(1, 4))
  diagonal = %w[diagonal_not_zero periodic_mean].include?(MUTATION) ? 1 : 0
  primitive_denominator = decay_two * k * k
  primitive_denominator = k * k if MUTATION == 'time_integral_denominator'
  definition_half = MUTATION == 'flux_half' ? 1 : Rational(1, 2)
  square_half = MUTATION == 'flux_square_half' ? 1 : Rational(1, 2)
  coefficient_shear = MUTATION == 'flux_B_absolute' ? -shear.abs : shear.abs
  coefficient_variation = MUTATION == 'flux_Vxi' ? variation + 1 : variation
  flux_coefficient = definition_half * square_half * amplitude**2 *
    coefficient_shear * coefficient_variation / primitive_denominator
  flux_coefficient += 1 if MUTATION == 'flux_coefficient'
  mass_denominator = decay_three * k * k
  mass_denominator = decay_three * k if %w[mass_denominator mass_k_square].include?(MUTATION)
  mass_coefficient = full_moment * amplitude**3 / mass_denominator
  {
    'k' => k,
    'timeCos' => rtext(Rational(time_cos)),
    'timeSin' => rtext(time_sin),
    'driftSin' => rtext(drift_sin),
    'diffusionCos' => rtext(Rational(diffusion_cos)),
    'residualCos' => rtext(Rational(residual_cos)),
    'residualSin' => rtext(residual_sin),
    'squareModes' => [-square_frequency, 0, square_frequency],
    'squareModeCoefficients' => [rtext(square_side), rtext(square_zero), rtext(square_side)],
    'diagonalPairing' => rtext(Rational(diagonal)),
    'timeIntegralDenominator' => rtext(primitive_denominator),
    'fluxCoefficientTimesOneMinusQ2' => rtext(flux_coefficient),
    'fluxUpperCoefficient' => rtext(flux_coefficient),
    'massCoefficientTimesOneMinusQ3' => rtext(mass_coefficient)
  }
end

q3_symbol = MUTATION == 'q3_symbol' ? 'exp(-k^2*T)' : mass_fixture.fetch('q3Symbol')
condition = if MUTATION == 'condition_direction'
              'k^2*T<=1'
            elsif MUTATION == 'condition_one'
              'k^2*T>=0'
            else
              'k^2*T>=1'
            end
q3_comparison = MUTATION == 'q3_comparison' ? '0<exp(-3)<=q3<1' : '0<q3<=exp(-3)<1'
c3_symbol = MUTATION == 'c3_symbol' ? '1+exp(-3)' : mass_fixture.fetch('c3Symbol')
a2_conversion = 'A^2<=(9/(8*c3))^(2/3)*k^(4/3)*M^(2/3)'
a2_conversion = 'A^2<=(8/(9*c3))^(2/3)*k^(4/3)*M^(2/3)' if MUTATION == 'a2_prefactor'
a2_conversion = 'A^2<=(9/(8*c3))^(2/3)*k^(2/3)*M^(2/3)' if MUTATION == 'a2_power_k'
a2_conversion = 'A^2<=(9/(8*c3))^(2/3)*k^(4/3)*M^(1/3)' if MUTATION == 'a2_power_mass'
a2_conversion = 'A^2>=(9/(8*c3))^(2/3)*k^(4/3)*M^(2/3)' if MUTATION == 'a2_inequality'
cstar = '1/8*(9/(8*c3))^(2/3)'
cstar = '1/4*(9/(8*c3))^(2/3)' if MUTATION == 'cstar_outer'
cstar = '1/8*(8/(9*c3))^(2/3)' if MUTATION == 'cstar_inner'
mass_symbol = MUTATION == 'mass_symbol' ?
  '8*A^3*(1-q3)/(3*k^2)' : '8*A^3*(1-q3)/(9*k^2)'
conversion_observed = {
  'exactSymbol' => mass_symbol,
  'q3Symbol' => q3_symbol,
  'condition' => condition,
  'q3Comparison' => q3_comparison,
  'c3Symbol' => c3_symbol,
  'c3Interval' => MUTATION == 'c3_positive' ? 'c3>1' : '0<c3<1',
  'A2Conversion' => a2_conversion,
  'CStar' => cstar
}

# Independently solve the exponent equations, including p=R^-2 omega M.
exponent_fixture = fixtures.fetch('exponentCase')
flux_exp = exponent_fixture.fetch('fluxUpper').to_h { |key, value| [key, rat(value)] }
mass_exp = exponent_fixture.fetch('mass').to_h { |key, value| [key, rat(value)] }
flux_exp['A'] = 1 if MUTATION == 'flux_A'
flux_exp['k'] = -1 if MUTATION == 'flux_k'
mass_exp['A'] = 2 if MUTATION == 'mass_A'
mass_exp['k'] = -1 if MUTATION == 'mass_k'
two_thirds = rat(exponent_fixture.fetch('twoThirds'))
two_thirds = Rational(1, 3) if MUTATION == 'two_thirds'
mass_two_thirds = mass_exp.to_h { |key, value| [key, value * two_thirds] }
ratio_exp = {
  'A' => flux_exp.fetch('A') - mass_two_thirds.fetch('A'),
  'B' => flux_exp.fetch('B'),
  'Vxi' => flux_exp.fetch('Vxi'),
  'k' => flux_exp.fetch('k') - mass_two_thirds.fetch('k')
}
ratio_exp['k'] += Rational(1, 3) if MUTATION == 'ratio_k'
target_prefactor = exponent_fixture.fetch('targetPrefactor').to_h { |key, value| [key, rat(value)] }
payment = exponent_fixture.fetch('paymentDefinition').to_h { |key, value| [key, rat(value)] }
target_prefactor['omega'] = 0 if MUTATION == 'target_omega'
target_prefactor['R'] = 0 if MUTATION == 'target_R'
payment['R'] = -1 if MUTATION == 'payment_R'
payment['omega'] = -1 if MUTATION == 'payment_omega'
payment['M'] = 2 if MUTATION == 'payment_M'
m_power = payment.fetch('M')
target_normalized = {
  'R' => target_prefactor.fetch('R') - two_thirds * payment.fetch('R') / m_power,
  'omega' => target_prefactor.fetch('omega') - two_thirds * payment.fetch('omega') / m_power,
  'k' => ratio_exp.fetch('k'),
  'p' => two_thirds / m_power
}
target_normalized['R'] += Rational(1, 3) if MUTATION == 'normalized_R'
target_normalized['omega'] += Rational(1, 3) if MUTATION == 'normalized_omega'
target_normalized['k'] += Rational(1, 3) if MUTATION == 'normalized_k'
target_normalized['p'] = Rational(1, 3) if MUTATION == 'normalized_p'
exponent_observed = {
  'fluxUpper' => exponent_text(flux_exp),
  'mass' => exponent_text(mass_exp),
  'massTwoThirds' => exponent_text(mass_two_thirds),
  'fluxOverMassTwoThirds' => exponent_text(ratio_exp),
  'targetNormalized' => exponent_text(target_normalized),
  'amplitudeCancels' => MUTATION != 'amplitude_cancel'
}

# Exact threshold arithmetic; the decimal is derived, never an equality premise.
threshold_fixture = fixtures.fetch('thresholdCase')
alpha = rat(threshold_fixture.fetch('alphaStar'))
alpha += Rational(1, 107_163) if MUTATION == 'alpha_numerator'
alpha = Rational(27_163, 107_162) if MUTATION == 'alpha_denominator'
multiplier = rat(threshold_fixture.fetch('multiplier'))
multiplier = 2 if MUTATION == 'kappa_multiplier'
kappa_star = alpha * multiplier
kappa_star += Rational(1, 71_442) if MUTATION == 'kappa_reduce'
strict_kappa = rat(threshold_fixture.fetch('strictTestKappa'))
strict_margin = strict_kappa - kappa_star
strict_exponent_margin = Rational(2, 3) * strict_kappa - alpha
display = rounded_decimal(kappa_star, threshold_fixture.fetch('displayDigits'))
display = '0.3802105205' if MUTATION == 'decimal_display'
threshold_observed = {
  'alphaStar' => rtext(alpha),
  'kappaStar' => rtext(kappa_star),
  'endpointEquality' => MUTATION == 'endpoint_equality' ?
    '2*kappaStar/3>alphaStar' : '2*kappaStar/3=alphaStar',
  'displayRounded10' => display,
  'strictTestKappa' => rtext(strict_kappa),
  'strictKappaMargin' => rtext(strict_margin),
  'strictExponentMargin' => rtext(strict_exponent_margin),
  'RInterval' => MUTATION == 'R_interval' ? 'R>1' : threshold_fixture.fetch('RInterval')
}

tags = text.scan(/\\tag\{(L\.[^}]+)\}/).flatten
tags << 'L.1' if MUTATION == 'tag'
references = text.scan(/\(L\.([0-9]+[a-z]?)\)/).flatten.map { |value| "L.#{value}" }
references << 'L.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\\[' }
display_close = text.lines.count { |line| line.strip == '\\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..17).map { |index| "L.#{index}" }

dependency_paths = %w[
  research/r075e_horizontal_cross_mode_flux_reduction.md
  research/r075g_signed_flux_gain_threshold.md
  research/r075k_positive_majorant_high_frequency_trace_loss.md
]
dependency_table_present = dependency_paths.all? do |path|
  text.lines.any? { |line| line.include?(path) && line.include?(FROZEN_SOURCES.fetch(path)) }
end
dependency_table_present = false if MUTATION == 'dependency_table_missing'

required_tokens = [
  '\\mathcal L_B:=\\partial_t+B\\partial_2-\\partial_2^2',
  'F_k(t,x_2) :=A e^{-k^2t}\\cos\\bigl(k(x_2-Bt)\\bigr)',
  '\\boxed{\\mathcal L_BF_k=0.}',
  '\\int_0^T e^{-2k^2t}\\,dt',
  '\\bigl(1-e^{-2k^2T}\\bigr)',
  '\\frac{A^2|B|V_\\xi}{8k^2}',
  '\\frac{8A^3}{9k^2}\\bigl(1-e^{-3k^2T}\\bigr)',
  'k^2T\\ge1',
  'C_*:=\\frac18 \\left(\\frac9{8(1-e^{-3})}\\right)^{2/3}',
  'R^{1/3}\\omega^{1/3}k^{-2/3}',
  '\\frac{27163}{71442}',
  'not a proof of G.1',
  'or prove E.24',
  '\\mathbf{NOT\\ CLAY}'
]

boundary = {
  'integerKAtLeastOne' => !%w[k_integer k_lower].include?(MUTATION),
  'amplitudePositive' => MUTATION != 'A_positive',
  'realConstantShear' => !%w[B_real constant_shear].include?(MUTATION),
  'oneRealHarmonic' => !%w[real_field single_harmonic].include?(MUTATION),
  'diagonalRemovedBeforeAbsoluteValue' => !%w[diagonal_after_absolute absolute_before_cancel].include?(MUTATION),
  'periodicDerivativeMeanZero' => MUTATION != 'periodic_mean',
  'etaMeasurableAndInUnitInterval' => MUTATION != 'eta_measurable',
  'xiSmoothPeriodicReal' => !%w[xi_periodic xi_smooth xi_real].include?(MUTATION),
  'VxiUsesAbsoluteDerivative' => MUTATION != 'vxi_absolute',
  'innerIntegralBoundedByVxi' => MUTATION != 'vxi_bound',
  'q2DropDirectionCorrect' => MUTATION != 'drop_q2_direction',
  'q3OnlySymbolicInterval' => MUTATION != 'q3_float_equality',
  'conditionAndComparisonDirectionCorrect' => !%w[condition_direction condition_one q3_comparison].include?(MUTATION),
  'c3StrictlyBetweenZeroAndOne' => MUTATION != 'c3_positive',
  'positivePartNormalization' => MUTATION != 'positive_part',
  'strictThresholdDirection' => MUTATION != 'strict_direction',
  'decimalIsDisplayOnly' => MUTATION != 'decimal_exact',
  'frequencyImplicationDirection' => MUTATION != 'frequency_direction',
  'physicalSignedFlux' => MUTATION != 'physical_signed',
  'fullTorusCubicOnly' => MUTATION != 'full_torus',
  'BVxiCoefficientUnpaid' => MUTATION != 'unpaid_BVxi',
  'notG1' => MUTATION != 'g1_claim',
  'notE24' => MUTATION != 'e24_claim',
  'notFullVersionM' => MUTATION != 'full_versionm_claim',
  'multimodeOpen' => MUTATION != 'multimode_closed',
  'collarLocalizationOpen' => MUTATION != 'collar_closed',
  'nonconstantShearOpen' => MUTATION != 'nonconstant_closed',
  'lowFrequencySectorOpen' => MUTATION != 'low_frequency_closed',
  'completeClockOpen' => MUTATION != 'complete_clock',
  'fixedDeletionOpen' => MUTATION != 'fixed_deletion',
  'suitableWeakTransferOpen' => MUTATION != 'suitable_weak',
  'regularityOpen' => MUTATION != 'regularity',
  'singularityOpen' => MUTATION != 'singularity',
  'noNoveltyClaim' => MUTATION != 'novelty',
  'noPriorityClaim' => MUTATION != 'priority',
  'noSimulationUsed' => MUTATION != 'simulation',
  'notClay' => MUTATION != 'clay'
}

checks = {
  'frozen source bindings' => source_rows.values.all? { |wanted, seen| wanted == seen },
  'fixture and expected bindings' =>
    fixture_hash == fixture_expected_hash && expected_hash == expected_expected_hash &&
    fixtures.fetch('frozenSources') == FROZEN_SOURCES,
  'primary audit binding and status' =>
    audit_text.include?(FROZEN_SOURCES.fetch('research/r075l_single_harmonic_diffusive_signed_flux_gain.md')) &&
    audit_text.include?('Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.') &&
    audit_text.include?('Equation tags L.1--L.17 are unique and consecutive.') &&
    audit_text.include?('All 17 display-math environments are paired.'),
  'three dependency bindings' => dependency_table_present,
  'operator signs' => operator_observed == expected.fetch('operator'),
  'eta bounds' => eta_observed == expected.fetch('eta'),
  'passive differentiation and square modes' =>
    family_observed == expected.fetch('passiveFamily') &&
    family_observed.all? { |row| row.fetch('residualCos') == '0' && row.fetch('residualSin') == '0' },
  'diagonal cancellation first' =>
    family_observed.all? { |row| row.fetch('diagonalPairing') == '0' } &&
    boundary.fetch('diagonalRemovedBeforeAbsoluteValue') && boundary.fetch('periodicDerivativeMeanZero'),
  'time primitive and flux factor' =>
    time_observed == expected.fetch('timeIntegral') && decay_two == 2 &&
    boundary.fetch('q2DropDirectionCorrect'),
  'cosine moment and cubic mass' =>
    moment_observed == expected.fetch('absoluteCosineMoment') && decay_three == 3 &&
    family_observed.all? { |row| rat(row.fetch('massCoefficientTimesOneMinusQ3')).positive? },
  'symbolic exponential guard' =>
    conversion_observed == expected.fetch('massConversion') &&
    boundary.fetch('q3OnlySymbolicInterval') &&
    boundary.fetch('conditionAndComparisonDirectionCorrect') &&
    boundary.fetch('c3StrictlyBetweenZeroAndOne'),
  'homogeneity and normalization' =>
    exponent_observed == expected.fetch('exponents') &&
    target_normalized == {'R' => Rational(1, 3), 'omega' => Rational(1, 3), 'k' => Rational(-2, 3), 'p' => Rational(2, 3)},
  'exact threshold' =>
    threshold_observed == expected.fetch('threshold') && Rational(2, 3) * kappa_star == alpha &&
    strict_margin.positive? && strict_exponent_margin.positive?,
  'R less than one direction' =>
    threshold_observed.fetch('RInterval') == '0<R<1' &&
    Rational(2, 3) * strict_kappa > alpha && MUTATION != 'frequency_direction',
  'tags references displays' =>
    tags == expected_tags && tags.uniq.length == 17 && (references.uniq - tags).empty? &&
    display_open == 17 && display_close == 17,
  'formula and status sentinels' => required_tokens.all? { |token| flat_text.include?(token.gsub(/\s+/, ' ')) },
  'source report boundary' =>
    flat_source.include?('no E.24, complete-clock, regularity, novelty, or priority claim') &&
    flat_source.include?('one-real-harmonic physical signed flux') &&
    flat_source.include?('full-torus spacetime cubic mass'),
  'claim boundary' => boundary.values.all?,
  'utf8 and control safety' =>
    !scan_text.include?("\uFFFD") && scan_text.each_codepoint.none? { |code| code < 32 && ![9, 10].include?(code) },
  'python canonical ledger agreement' =>
    python_payload.fetch('schema') == SCHEMA && python_payload.fetch('verdict') == 'PASS' &&
    python_payload.dig('assertions', 'passed') == 19 &&
    python_payload.fetch('operator') == operator_observed &&
    python_payload.fetch('eta') == eta_observed &&
    python_payload.fetch('passiveFamily') == family_observed &&
    python_payload.fetch('timeIntegral') == time_observed &&
    python_payload.fetch('absoluteCosineMoment') == moment_observed &&
    python_payload.fetch('massConversion') == conversion_observed &&
    python_payload.fetch('exponents') == exponent_observed &&
    python_payload.fetch('threshold') == threshold_observed &&
    python_payload.fetch('claimBoundary') == boundary
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed = checks.select { |_name, passed| !passed }.keys
REPORT.write(
  "# R0.75L independent finite audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Mathematical blockers: #{verdict == 'PASS' ? 0 : failed.length}\n" \
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}\n" \
  "- Failed checks: #{failed.empty? ? 'none' : failed.join('; ')}\n\n" \
  "An independent Rational/Fourier ledger verifies L_BF_k=0, square modes " \
  "0,+/-2k, diagonal cancellation before absolute values, the eta/V_xi bound, " \
  "the exact time primitive, and flux coefficient A^2|B|V_xi/(8k^2). " \
  "It also recomputes integral |cos(kx)|^3=8/3 and " \
  "M_k=8A^3(1-q3)/(9k^2).\n\n" \
  "The exp(-3) term is retained symbolically with 0<q3<=exp(-3)<1. " \
  "Homogeneity gives A cancellation, C_*, k^(-2/3), and target powers " \
  "R^(1/3)omega^(1/3)p^(2/3). The strict frequency endpoint is " \
  "27163/71442; equality is excluded.\n\n" \
  "This is only a one-real-harmonic, constant-shear, full-torus benchmark; " \
  "|B|V_xi is unpaid. It is not G.1, E.24, or full Version-M. **NOT CLAY.**\n"
)
puts JSON.generate(
  'suite' => 'r075l-single-harmonic-diffusive-signed-flux-gain-independent',
  'verdict' => verdict,
  'assertions' => checks.length
)
exit(verdict == 'PASS' ? 0 : 1)
