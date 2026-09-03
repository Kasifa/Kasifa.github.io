#!/usr/bin/env ruby
# Independent exact verifier for frozen R0.75I.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075i_diffusion_safe_block_participation.md'
PRIMARY_AUDIT = ROOT + 'research/r075i_diffusion_safe_block_participation_primary_audit.md'
REPORT_SOURCE = ROOT + 'research/r075i_report-source.md'
FIXTURES = ROOT + 'scripts/r075i_diffusion_safe_block_participation_fixtures.json'
EXPECTED = ROOT + 'scripts/r075i_diffusion_safe_block_participation_expected.json'
JSON_PATH = Pathname.new(
  ENV.fetch(
    'R075I_JSON',
    (ROOT + 'research/r075i_diffusion_safe_block_participation_certificate.json').to_s
  )
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075I_RUBY_REPORT',
    (ROOT + 'research/r075i_diffusion_safe_block_participation_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075I_RUBY_MUTATION', '')
SCHEMA = 'r075i-diffusion-safe-block-participation-certificate-v1'

FROZEN_SOURCES = {
  'research/r075b_bulk_clock_outer_padding_gate.md' =>
    '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075c_background_shear_packing_false_positive.md' =>
    '1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89',
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075g_signed_flux_gain_threshold.md' =>
    'f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41',
  'research/r075h_single_pass_transport_flux_closure.md' =>
    '849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9',
  'research/r075i_diffusion_safe_block_participation.md' =>
    'c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7',
  'research/r075i_diffusion_safe_block_participation_primary_audit.md' =>
    'a8e481bfa28ba244a6022b782880ce9a86c40de29e3b0064474841eca99cecbd',
  'research/r075i_report-source.md' =>
    '8459adb6735caa2ee6c6e9c27202125cda34ad9072e2d78167f3f961e34f5de3'
}.freeze
FIXTURES_SHA256 = 'afda306afcf26640be72978b654a1a7dd1b23c0df5e92137f450520a6c7d515b'
EXPECTED_SHA256 = '27514a38beec5c5e949a2a639faa5db539a4fbdeefec175e9e6e90a0507afd2a'

NEGATIVE_MUTATIONS = %w[
  source_drift audit_drift report_source_drift dependency_drift
  dependency_table_missing fixture_drift expected_drift tag reference display
  control block_time_r support_l support_r cylinder_measure b_r cutoff_r
  pointwise_coefficient measure_third_l measure_third_r cubic_r cubic_omega
  cubic_p normalization_r normalization_omega final_l holder_cell_measure
  holder_l2_power holder_l3_power holder_direction cubic_atom_r
  cubic_atom_omega transport_half one_block_direction participation_power
  neff_numerator neff_denominator neff_zero neff_lower_direction
  neff_upper_direction aggregation_identity unequal_as_count equal_mass_count
  aggregate_positive_part aggregate_absolute_sum aggregate_direction
  payment_pa_direction payment_pf_direction payment_power payment_upper_use
  rho_sign cgamma_sign theta_ratio theta_offset theta_strict beta_complement
  beta_strict one_rate_fraction uniform_theta uniform_rate_fraction
  endpoint_polynomial zero_mode_mean zero_mode_flux zero_mode_payment
  zero_mode_neff pde_required diffusion_unsafe participation_proved
  participation_necessary high_neff_counterexample uniform_counterexample
  signed_alternative_closed transition_closed recrossing_closed e24_closed
  complete_clock fixed_deletion suitable_weak regularity singularity novelty
  simulation_used clay
].freeze

abort("unknown R075I_RUBY_MUTATION: #{MUTATION}") unless
  MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)

def rat(value)
  Rational(value.to_s)
end

def rtext(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

def vector_zero
  {'L' => Rational(0), 'R' => Rational(0), 'omega' => Rational(0), 'p' => Rational(0)}
end

def vector_add(*vectors)
  vector_zero.keys.to_h do |key|
    [key, vectors.sum { |vector| vector.fetch(key, Rational(0)) }]
  end
end

def vector_scale(vector, scalar)
  vector.to_h { |key, value| [key, value * scalar] }
end

def vector_text(vector)
  vector.to_h { |key, value| [key, rtext(value)] }
end

def integer_cuberoot(value)
  return -integer_cuberoot(-value) if value.negative?

  root = 0
  root += 1 while (root + 1)**3 <= value
  raise "not a perfect cube: #{value}" unless root**3 == value

  root
end

def exact_cuberoot(value)
  raise 'negative participation payment' if value.negative?

  Rational(integer_cuberoot(value.numerator), integer_cuberoot(value.denominator))
end

text = MAIN.read
audit_text = PRIMARY_AUDIT.read
source_text = REPORT_SOURCE.read
flat_text = text.gsub(/\s+/, ' ')
scan_text = text + audit_text + source_text + (MUTATION == 'control' ? "\u0001" : '')
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_payload = JSON.parse(JSON_PATH.read)

source_expectations = FROZEN_SOURCES.dup
source_expectations['research/r075i_diffusion_safe_block_participation.md'] =
  '0' * 64 if MUTATION == 'source_drift'
source_expectations[
  'research/r075i_diffusion_safe_block_participation_primary_audit.md'
] = '0' * 64 if MUTATION == 'audit_drift'
source_expectations['research/r075i_report-source.md'] =
  '0' * 64 if MUTATION == 'report_source_drift'
source_expectations['research/r075c_background_shear_packing_false_positive.md'] =
  '0' * 64 if MUTATION == 'dependency_drift'
source_rows = source_expectations.keys.sort.to_h do |path|
  [path, [source_expectations.fetch(path), Digest::SHA256.file(ROOT + path).hexdigest]]
end
fixture_expected_hash = MUTATION == 'fixture_drift' ? '0' * 64 : FIXTURES_SHA256
expected_expected_hash = MUTATION == 'expected_drift' ? '0' * 64 : EXPECTED_SHA256
fixture_hash = Digest::SHA256.file(FIXTURES).hexdigest
expected_hash = Digest::SHA256.file(EXPECTED).hexdigest

# I.5--I.13: independent Laurent ledger.
block_time = vector_zero
block_time['R'] = MUTATION == 'block_time_r' ? Rational(2) : Rational(3)
support = vector_zero
support['L'] = MUTATION == 'support_l' ? Rational(1) : Rational(2)
support['R'] = MUTATION == 'support_r' ? Rational(2) : Rational(3)
cylinder = vector_add(block_time, support)
cylinder['R'] += 1 if MUTATION == 'cylinder_measure'
b_bound = vector_zero
b_bound['R'] = MUTATION == 'b_r' ? Rational(-1) : Rational(-2)
cutoff_bound = vector_zero
cutoff_bound['R'] = MUTATION == 'cutoff_r' ? Rational(1) : Rational(-1)
pointwise = vector_add(b_bound, cutoff_bound)
pointwise['R'] += 1 if MUTATION == 'pointwise_coefficient'
measure_third = vector_scale(cylinder, Rational(1, 3))
measure_third['L'] = Rational(1, 3) if MUTATION == 'measure_third_l'
measure_third['R'] = Rational(1) if MUTATION == 'measure_third_r'
cubic_base = {'L' => Rational(0), 'R' => Rational(2),
              'omega' => Rational(-1), 'p' => Rational(1)}
cubic_two_thirds = vector_scale(cubic_base, Rational(2, 3))
cubic_two_thirds['R'] = Rational(2, 3) if MUTATION == 'cubic_r'
cubic_two_thirds['omega'] = Rational(2, 3) if MUTATION == 'cubic_omega'
cubic_two_thirds['p'] = Rational(1, 3) if MUTATION == 'cubic_p'
normalization = vector_zero
normalization['R'] = MUTATION == 'normalization_r' ? Rational(1) : Rational(-1)
normalization['omega'] = MUTATION == 'normalization_omega' ? Rational(0) : Rational(1)
final_product = vector_add(normalization, pointwise, measure_third, cubic_two_thirds)
final_product['L'] += Rational(1, 3) if MUTATION == 'final_l'
exponent_observed = {
  'blockTime' => vector_text(block_time),
  'supportVolume' => vector_text(support),
  'cylinderMeasure' => vector_text(cylinder),
  'pointwiseCoefficient' => vector_text(pointwise),
  'measureOneThird' => vector_text(measure_third),
  'cubicTwoThirds' => vector_text(cubic_two_thirds),
  'fluxNormalization' => vector_text(normalization),
  'finalProduct' => vector_text(final_product)
}

# Direct two-cell sums give a nonconstant strict Holder diagnostic.
holder = fixtures.fetch('oneBlockHolderCase')
hr = rat(holder.fetch('R'))
hl = rat(holder.fetch('L'))
homega = rat(holder.fetch('omega'))
htime = rat(holder.fetch('timeLength'))
hsupport = rat(holder.fetch('supportVolume'))
measures = holder.fetch('cellMeasures').map { |value| rat(value) }
measures[0] += Rational(1, 64) if MUTATION == 'holder_cell_measure'
values = holder.fetch('fieldValues').map { |value| rat(value) }
l2_power = MUTATION == 'holder_l2_power' ? 1 : 2
l3_power = MUTATION == 'holder_l3_power' ? 2 : 3
l2_integral = measures.zip(values).sum { |measure, value| measure * value**l2_power }
l3_integral = measures.zip(values).sum { |measure, value| measure * value**l3_power }
cylinder_measure = measures.sum
holder_left_cubed = l2_integral**3
holder_right_cubed = cylinder_measure * l3_integral**2
cubic_r_power = MUTATION == 'cubic_atom_r' ? 2 : -2
cubic_omega_power = MUTATION == 'cubic_atom_omega' ? -1 : 1
cubic_atom = hr**cubic_r_power * homega**cubic_omega_power * l3_integral
reconstructed_cubic = hr**2 * homega**-1 * cubic_atom
half = MUTATION == 'transport_half' ? Rational(1) : Rational(1, 2)
transport_upper = half * rat(holder.fetch('eta')) *
  rat(holder.fetch('bMagnitude')) *
  rat(holder.fetch('cutoffDerivativeMagnitude')) * l2_integral
normalized_flux = homega / hr * transport_upper
one_block_left_cubed = normalized_flux**3
one_block_right_cubed = hl**2 * homega * hr**-2 * cubic_atom**2
holder_observed = {
  'timeFromR' => rtext(hr**3),
  'supportFromLR' => rtext(hl**2 * hr**3),
  'cylinderMeasure' => rtext(cylinder_measure),
  'l2Integral' => rtext(l2_integral),
  'l3Integral' => rtext(l3_integral),
  'holderLeftCubed' => rtext(holder_left_cubed),
  'holderRightCubed' => rtext(holder_right_cubed),
  'holderStrictGap' => rtext(holder_right_cubed - holder_left_cubed),
  'cubicAtom' => rtext(cubic_atom),
  'cubicIntegralFromAtom' => rtext(reconstructed_cubic),
  'transportAbsoluteUpper' => rtext(transport_upper),
  'normalizedFlux' => rtext(normalized_flux),
  'oneBlockRightCubed' => rtext(one_block_right_cubed),
  'oneBlockLeftCubed' => rtext(one_block_left_cubed),
  'oneBlockStrictGap' => rtext(one_block_right_cubed - one_block_left_cubed)
}
holder_direction = MUTATION == 'holder_direction' ? 'left>=right' : 'left<=right'
one_block_direction = MUTATION == 'one_block_direction' ? 'left>=right' : 'left<=right'

# Exact participation arithmetic for perfect cubes, including zero atoms.
participation_observed = fixtures.fetch('participationCases').map do |item|
  payments = item.fetch('payments').map { |value| rat(value) }
  roots = payments.map { |value| exact_cuberoot(value) }
  terms = MUTATION == 'participation_power' ? roots : roots.map { |root| root**2 }
  total = payments.sum
  sum_two_thirds = terms.sum
  cardinality = payments.length
  cardinality = 3 if MUTATION == 'equal_mass_count' &&
    item.fetch('name') == 'equalMassFourBlocks'
  n_eff = if total.zero?
            MUTATION == 'neff_zero' ? Rational(1) : Rational(0)
          else
            numerator_power = MUTATION == 'neff_numerator' ? 2 : 3
            denominator_power = MUTATION == 'neff_denominator' ? 1 : 2
            sum_two_thirds**numerator_power / total**denominator_power
          end
  n_eff = Rational(cardinality) if MUTATION == 'unequal_as_count' &&
    item.fetch('name') == 'unequalPerfectCubes'
  identity_residual = sum_two_thirds**3 - n_eff * total**2
  identity_residual += 1 if MUTATION == 'aggregation_identity'
  positive = total.positive?
  {
    'name' => item.fetch('name'),
    'cardinality' => cardinality,
    'totalPayment' => rtext(total),
    'sumTwoThirds' => rtext(sum_two_thirds),
    'nEff' => rtext(n_eff),
    'lowerSlack' => positive ? rtext(n_eff - 1) : 'not-applicable',
    'upperSlack' => positive ? rtext(cardinality - n_eff) : 'not-applicable',
    'identityResidual' => rtext(identity_residual)
  }
end
neff_lower_direction = MUTATION == 'neff_lower_direction' ? 'N_eff<=1' : '1<=N_eff'
neff_upper_direction = MUTATION == 'neff_upper_direction' ? 'N<=N_eff' : 'N_eff<=N'

# Exact signed finite sums.
signed_observed = fixtures.fetch('signedAggregationCases').map do |item|
  fluxes = item.fetch('fluxes').map { |value| rat(value) }
  signed_sum = fluxes.sum
  positive_part = MUTATION == 'aggregate_positive_part' ?
    signed_sum.abs : [signed_sum, Rational(0)].max
  absolute_sum = MUTATION == 'aggregate_absolute_sum' ?
    signed_sum : fluxes.sum(&:abs)
  {
    'name' => item.fetch('name'),
    'signedSum' => rtext(signed_sum),
    'positivePart' => rtext(positive_part),
    'sumAbsolute' => rtext(absolute_sum),
    'triangleSlack' => rtext(absolute_sum - positive_part),
    'inequalityDirection' =>
      MUTATION == 'aggregate_direction' ? 'left>=right' : 'left<=right'
  }
end

payment = fixtures.fetch('paymentDirectionCase')
pa = rat(payment.fetch('pA'))
pf = rat(payment.fetch('pF'))
constant_times_p = rat(payment.fetch('constant')) * rat(payment.fetch('P'))
payment_observed = {
  'pA' => rtext(pa),
  'pF' => rtext(pf),
  'constantTimesP' => rtext(constant_times_p),
  'pAToPFDirection' => MUTATION == 'payment_pa_direction' ? 'pA>=pF' : 'pA<=pF',
  'pFToPDirection' => MUTATION == 'payment_pf_direction' ? 'pF>=CP' : 'pF<=CP',
  'targetPower' => MUTATION == 'payment_power' ? '1/3' : '2/3',
  'usesUpperDomination' => MUTATION != 'payment_upper_use',
  'firstSlack' => rtext(pf - pa),
  'secondSlack' => rtext(constant_times_p - pf)
}

# Exact threshold and endpoint calculations.
constants = fixtures.fetch('thresholdConstants')
rho = rat(constants.fetch('rho'))
c_gamma = rat(constants.fetch('cGamma'))
rho *= -1 if MUTATION == 'rho_sign'
c_gamma *= -1 if MUTATION == 'cgamma_sign'
theta_star = if MUTATION == 'theta_ratio'
               rho / c_gamma - 2
             else
               c_gamma / rho - (MUTATION == 'theta_offset' ? 1 : 2)
             end
beta_star = MUTATION == 'beta_complement' ? 1 + theta_star : 1 - theta_star
one_rate = rho / 6 - c_gamma / 12
one_rate += Rational(1, 238_140_000) if MUTATION == 'one_rate_fraction'
below_rate = (rho * (2 + rat(constants.fetch('thetaBelow'))) - c_gamma) / 12
endpoint_rate = (rho * (2 + theta_star) - c_gamma) / 12
above_rate = (rho * (2 + rat(constants.fetch('thetaAbove'))) - c_gamma) / 12
full_theta = MUTATION == 'uniform_theta' ? Rational(0) : Rational(1)
full_uniform_rate = (rho * (2 + full_theta) - c_gamma) / 12
full_uniform_rate += Rational(1, 476_280_000) if MUTATION == 'uniform_rate_fraction'
threshold_observed = {
  'thetaStar' => rtext(theta_star),
  'betaStar' => rtext(beta_star),
  'oneBlockRate' => rtext(one_rate),
  'belowRate' => rtext(below_rate),
  'endpointRate' => rtext(endpoint_rate),
  'aboveRate' => rtext(above_rate),
  'fullUniformRate' => rtext(full_uniform_rate),
  'thetaEndpointAccepted' => MUTATION == 'theta_strict',
  'betaEndpointAccepted' => MUTATION == 'beta_strict',
  'remainingEndpointFactor' => MUTATION == 'endpoint_polynomial' ? '1' : 'L^(2/3)'
}

# I.27 zero horizontal mode.
zero_mode = fixtures.fetch('zeroModeCase')
z_measures = zero_mode.fetch('x2CellMeasures').map { |value| rat(value) }
z_derivatives = zero_mode.fetch('cutoffDerivativeValues').map { |value| rat(value) }
derivative_mean = z_measures.zip(z_derivatives).sum do |measure, value|
  measure * (MUTATION == 'zero_mode_mean' ? value.abs : value)
end
z_flux = Rational(1, 2) * rat(zero_mode.fetch('timeLength')) *
  rat(zero_mode.fetch('eta')) * rat(zero_mode.fetch('bValue')) *
  rat(zero_mode.fetch('fieldValue'))**2 * derivative_mean
z_flux += 1 if MUTATION == 'zero_mode_flux'
z_cubic_integral = rat(zero_mode.fetch('timeLength')) *
  rat(zero_mode.fetch('domainVolume')) * rat(zero_mode.fetch('fieldValue')).abs**3
z_payment = rat(zero_mode.fetch('R'))**-2 *
  rat(zero_mode.fetch('omega')) * z_cubic_integral
z_payment *= 8 if MUTATION == 'zero_mode_payment'
z_count = zero_mode.fetch('blockCount')
z_total = z_count * z_payment
z_term = exact_cuberoot(z_payment)**2
z_sum = z_count * z_term
z_neff = z_sum**3 / z_total**2
z_neff -= 1 if MUTATION == 'zero_mode_neff'
zero_mode_observed = {
  'cutoffDerivativeMean' => rtext(derivative_mean),
  'fluxPerBlock' => rtext(z_flux),
  'cubicIntegralPerBlock' => rtext(z_cubic_integral),
  'paymentPerBlock' => rtext(z_payment),
  'totalPayment' => rtext(z_total),
  'sumTwoThirds' => rtext(z_sum),
  'nEff' => rtext(z_neff),
  'blockCount' => z_count,
  'highParticipationIsCounterexample' => MUTATION == 'high_neff_counterexample',
  'participationBoundIsNecessary' => MUTATION == 'participation_necessary'
}

tags = text.scan(/\\tag\{(I\.[^}]+)\}/).flatten
tags << 'I.1' if MUTATION == 'tag'
references = text.scan(/\(I\.([0-9]+[a-z]?)\)/).flatten.map { |value| "I.#{value}" }
references << 'I.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\[' }
display_close = text.lines.count { |line| line.strip == '\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..27).map { |index| "I.#{index}" }

dependency_paths = %w[
  research/r075b_bulk_clock_outer_padding_gate.md
  research/r075c_background_shear_packing_false_positive.md
  research/r075e_horizontal_cross_mode_flux_reduction.md
  research/r075g_signed_flux_gain_threshold.md
  research/r075h_single_pass_transport_flux_closure.md
]
dependency_table_present = dependency_paths.all? do |path|
  text.lines.any? { |line| line.include?(path) && line.include?(FROZEN_SOURCES.fetch(path)) }
end
dependency_table_present = false if MUTATION == 'dependency_table_missing'

required_tokens = [
  'No equation for the passive field is used in this estimate.',
  'For an arbitrary real measurable field',
  'physical diffusion cannot invalidate this conclusion.',
  '\\left[\\sum_{j\\in A}\\mathcal T_j\\right]_+',
  'N_{\\rm eff}(A)^{1/3}p_A^{2/3}',
  '\\theta<\\frac{c_\\gamma}{\\rho}-2',
  '\\frac{8558}{35721}=\\theta_*',
  '\\frac{27163}{35721}',
  '\\frac{27163}{476280000}>0',
  '\\int_{\\mathbb T_{x_2}}\\partial_2\\xi\\,dx_2',
  'is only a sufficient route.',
  'Failure of (I.19) neither disproves',
  '\\mathbf{NOT\\ CLAY}'
]

boundary = {
  'arbitraryFieldNoPDEUsed' => MUTATION != 'pde_required',
  'oneBlockEstimateDiffusionSafe' => MUTATION != 'diffusion_unsafe',
  'participationEstimateRemainsConditional' => MUTATION != 'participation_proved',
  'participationIsSufficientNotNecessary' => MUTATION != 'participation_necessary',
  'highParticipationIsNotCounterexample' => MUTATION != 'high_neff_counterexample',
  'uniformAbsoluteLossIsNotCounterexample' => MUTATION != 'uniform_counterexample',
  'signedCancellationAlternativeOpen' => MUTATION != 'signed_alternative_closed',
  'shearTransitionBandsOpen' => MUTATION != 'transition_closed',
  'periodicRecrossingOpen' => MUTATION != 'recrossing_closed',
  'E24Open' => MUTATION != 'e24_closed',
  'completeClockOpen' => MUTATION != 'complete_clock',
  'fixedDeletionOpen' => MUTATION != 'fixed_deletion',
  'suitableWeakTransferOpen' => MUTATION != 'suitable_weak',
  'regularityOpen' => MUTATION != 'regularity',
  'singularityOpen' => MUTATION != 'singularity',
  'noNoveltyOrPriorityClaim' => MUTATION != 'novelty',
  'noSimulationUsed' => MUTATION != 'simulation_used',
  'notClay' => MUTATION != 'clay'
}

positive_part_bounds = participation_observed.reject do |row|
  row.fetch('lowerSlack') == 'not-applicable'
end
flat_audit = audit_text.gsub(/\s+/, ' ')
checks = {
  'all eight frozen hashes' => source_rows.values.all? { |pair| pair[0] == pair[1] },
  'fixture and expected byte bindings' =>
    fixture_hash == fixture_expected_hash && expected_hash == expected_expected_hash &&
    fixtures.fetch('schema') == 'r075i-diffusion-safe-block-participation-fixtures-v1' &&
    expected.fetch('schema') == 'r075i-diffusion-safe-block-participation-expected-v1' &&
    fixtures.fetch('frozenSources') == FROZEN_SOURCES,
  'primary audit frozen PASS and 27-display correction' =>
    audit_text.include?(FROZEN_SOURCES.fetch('research/r075i_diffusion_safe_block_participation.md')) &&
    audit_text.include?('Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.') &&
    audit_text.include?('Equation tags I.1--I.27 are unique and consecutive.') &&
    audit_text.include?('All 27 display-math environments are paired.') &&
    flat_audit.include?('High participation is neither an E.24 counterexample'),
  'five dependency rows in main' => dependency_table_present,
  'I.5--I.12 intermediate exponent ledger' =>
    exponent_observed.reject { |key, _value| key == 'finalProduct' } ==
      expected.fetch('exponentLedger').reject { |key, _value| key == 'finalProduct' },
  'I.13 final L/R/omega/p product' =>
    exponent_observed.fetch('finalProduct') == expected.dig('exponentLedger', 'finalProduct'),
  'nonconstant rational Holder fixture' =>
    holder_observed.fetch('cylinderMeasure') == '1/16' &&
    holder_observed.fetch('l2Integral') == '5/16' &&
    holder_observed.fetch('l3Integral') == '7/8' &&
    holder_direction == 'left<=right' && holder_left_cubed < holder_right_cubed,
  'one-block atom reconstruction and strict flux payment' =>
    holder_observed == expected.fetch('oneBlockHolder') &&
    htime == hr**3 && hsupport == hl**2 * hr**3 &&
    reconstructed_cubic == l3_integral && one_block_direction == 'left<=right' &&
    one_block_left_cubed < one_block_right_cubed,
  'single equal unequal sparse and zero participation cases' =>
    participation_observed == expected.fetch('participation'),
  '[1,8] gives exact 125/81 not block count' =>
    participation_observed[2].fetch('nEff') == '125/81' &&
    participation_observed[2].fetch('cardinality') == 2,
  'exact aggregation identity' =>
    participation_observed.all? { |row| row.fetch('identityResidual') == '0' },
  'one <= N_eff <= collection cardinality' =>
    neff_lower_direction == '1<=N_eff' && neff_upper_direction == 'N_eff<=N' &&
    positive_part_bounds.all? do |row|
      rat(row.fetch('lowerSlack')) >= 0 && rat(row.fetch('upperSlack')) >= 0
    end,
  'signed positive-part triangle inequality' =>
    signed_observed == expected.fetch('signedAggregation') &&
    signed_observed.all? { |row| rat(row.fetch('triangleSlack')) >= 0 },
  'Version-M upper-payment direction and two-thirds power' =>
    payment_observed == expected.fetch('paymentDirection') &&
    pa <= pf && pf <= constant_times_p,
  'theta and beta exact thresholds' =>
    threshold_observed.fetch('thetaStar') == '8558/35721' &&
    threshold_observed.fetch('betaStar') == '27163/35721',
  'strict endpoint and L two-thirds residue' =>
    threshold_observed.fetch('endpointRate') == '0' &&
    !threshold_observed.fetch('thetaEndpointAccepted') &&
    !threshold_observed.fetch('betaEndpointAccepted') &&
    threshold_observed.fetch('remainingEndpointFactor') == 'L^(2/3)',
  'one-block below above and full-uniform exact rates' =>
    threshold_observed == expected.fetch('thresholds') &&
    one_rate.negative? && below_rate.negative? && above_rate.positive? &&
    full_uniform_rate.positive?,
  'I.27 zero-mode derivative and flux cancellation' =>
    derivative_mean.zero? && z_flux.zero? && z_payment.positive?,
  'I.27 maximal participation is not necessary or counterexample' =>
    zero_mode_observed == expected.fetch('zeroMode') && z_neff == z_count &&
    !zero_mode_observed.fetch('highParticipationIsCounterexample') &&
    !zero_mode_observed.fetch('participationBoundIsNecessary'),
  '27 tags references and displays' =>
    tags == expected_tags && tags.uniq.length == 27 && (references - tags).empty? &&
    display_open == 27 && display_close == 27,
  'formula source and status sentinels' =>
    required_tokens.all? { |token| flat_text.include?(token.gsub(/\s+/, ' ')) } &&
    source_text.include?('This is a bounded non-hit, not evidence of novelty or priority.') &&
    source_text.include?('high participation is not a counterexample or a') &&
    source_text.include?('necessary obstruction'),
  'claim boundary' => boundary.values.all?,
  'Python schema and exact ledgers agree' =>
    python_payload.fetch('schema') == SCHEMA && python_payload.fetch('verdict') == 'PASS' &&
    python_payload.fetch('exponentLedger') == exponent_observed &&
    python_payload.fetch('oneBlockHolder') == holder_observed &&
    python_payload.fetch('participation') == participation_observed &&
    python_payload.fetch('signedAggregation') == signed_observed &&
    python_payload.fetch('paymentDirection') == payment_observed &&
    python_payload.fetch('thresholds') == threshold_observed &&
    python_payload.fetch('zeroMode') == zero_mode_observed &&
    python_payload.fetch('claimBoundary') == boundary,
  'UTF-8 and control safety' =>
    scan_text.valid_encoding? &&
    !scan_text.each_codepoint.any? { |code| code < 32 && ![9, 10].include?(code) }
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed = checks.reject { |_name, passed| passed }.keys
REPORT.write(
  "# R0.75I independent finite audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}\n" \
  "- Fixture SHA-256: #{fixture_hash}\n" \
  "- Expected SHA-256: #{expected_hash}\n" \
  "- Failed checks: #{failed.empty? ? 'none' : failed.join('; ')}\n\n" \
  "Ruby independently reconstructs I.5--I.13, including every intermediate " \
  "R/L/omega/p exponent. A nonconstant rational two-cell field gives strict " \
  "Holder and one-block margins. Perfect-cube atoms verify the exact " \
  "participation identity, 1 <= N_eff <= N, and [1,8] -> 125/81; mixed " \
  "signed blocks verify the positive-part triangle inequality.\n\n" \
  "All exact threshold fractions and endpoint signs agree with the frozen " \
  "note. The I.27 zero mode has N_eff=N=4 and zero flux on every block, so " \
  "large participation is neither a necessary obstruction nor an E.24 " \
  "counterexample. I.19 remains only a sufficient absolute-summation route. " \
  "The one-block estimate uses no PDE and is diffusion-safe, but it does not " \
  "prove participation. E.24 and all larger claims remain OPEN. **NOT CLAY.**\n"
)

puts JSON.generate(
  suite: 'r075i-diffusion-safe-block-participation-independent',
  verdict: verdict,
  assertions: checks.length
)
exit(verdict == 'PASS' ? 0 : 1)
