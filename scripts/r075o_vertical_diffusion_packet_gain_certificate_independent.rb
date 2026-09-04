#!/usr/bin/env ruby
# Independent exact verifier for frozen R0.75O.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075o_vertical_diffusion_packet_gain.md'
PRIMARY_AUDIT = ROOT + 'research/r075o_vertical_diffusion_packet_gain_primary_audit.md'
REPORT_SOURCE = ROOT + 'research/r075o_report-source.md'
FIXTURES = ROOT + 'scripts/r075o_vertical_diffusion_packet_gain_fixtures.json'
EXPECTED = ROOT + 'scripts/r075o_vertical_diffusion_packet_gain_expected.json'
JSON_PATH = Pathname.new(
  ENV.fetch('R075O_JSON', (ROOT + 'research/r075o_vertical_diffusion_packet_gain_certificate.json').to_s)
)
REPORT = Pathname.new(
  ENV.fetch('R075O_RUBY_REPORT', (ROOT + 'research/r075o_vertical_diffusion_packet_gain_independent_audit.md').to_s)
)
MUTATION = ENV.fetch('R075O_RUBY_MUTATION', '')
SCHEMA = 'r075o-vertical-diffusion-packet-gain-certificate-v1'

FROZEN_SOURCES = {
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075g_signed_flux_gain_threshold.md' =>
    'f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41',
  'research/r075m_dyadic_packet_diffusive_flux_gain.md' =>
    '13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7',
  'research/r075n_radial_collar_averaged_wiener_row.md' =>
    'ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318',
  'research/r075o_vertical_diffusion_packet_gain.md' =>
    '3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9',
  'research/r075o_vertical_diffusion_packet_gain_primary_audit.md' =>
    '27f9341f93bd2b031dbd3fd0e8d745788d5ff36a085ddb8be4ef8e1c5553e69b',
  'research/r075o_report-source.md' =>
    '9d2c234b0ba2a33b0f573a7933c26bcc751db6fe85919f2e146a0e6a18128c2b'
}.freeze
FIXTURES_SHA256 = '46dff6097c3a052dc968f1c712c3421105ea5be51d3c905c492cc463cc04f0ad'
EXPECTED_SHA256 = '228ac56e500a32b1f7c64c04d4110c78c4105c4d2a997fa8b108bd7449d59833'

NEGATIVE_MUTATIONS = %w[
  source_drift audit_drift report_source_drift dependency_drift
  dependency_table_missing fixture_drift expected_drift tag reference display
  control operator_time operator_drift operator_vertical_diffusion
  evolution_horizontal_decay evolution_shear_phase evolution_vertical_semigroup
  constant_shear flux_outer_half flux_spatial_2pi flux_difference_index
  reconstruction_sign flux_real_part flux_B_sign d0 diagonal_before_absolute
  eta_lower eta_upper eta_measurable xi_real_periodic w_infty_finite
  vertical_heat_growth vertical_square_missing vertical_l2_norm
  vertical_contraction_direction arbitrary_vertical_energy vertical_cap_energy
  time_kernel_denominator time_kernel_infinity denominator_lower row_sum
  column_sum schur_direction schur_sqrt quadratic_form_direction mode_count_loss
  parseval_factor energy_quarter horizontal_K_lower total_frequency_cap
  horizontal_only_cap finite_packet real_symmetry K_integer K2T_condition
  short_interval short_interval_inside heat_square cap_four l2_floor_direction
  holder_volume holder_direction holder_power torus_dimension time_length mass_16
  mass_pi mass_e inversion_direction inversion_e inversion_16pi inversion_K
  inversion_M combine_div4 combine_constant vertical_cardinality_loss payment_R
  payment_omega flux_R flux_omega mass_power frequency_power positive_part
  normalized_R normalized_omega normalized_K normalized_p amplitude_degree
  wiener_row wiener_L canonical_only universal_cutoff shear_R B_constant
  plateau_shear coefficient_R kappa_direction kappa_numerator
  kappa_denominator kappa_half kappa_reduce kappa_decimal strict_direction
  equality_allowed frozen_kappa rate_rho rate_cgamma rate_sign rate_fraction
  L_prefactor R_domain omega_positive own_full_torus_atom versionm_claim
  collar_localized arbitrary_vertical_cubic remove_total_cap nonconstant_closed
  interpacket_closed lowdifference_closed e24_claim complete_clock fixed_deletion
  suitable_weak regularity singularity novelty priority literature_complete
  simulation dns clay
].freeze

abort("unknown R075O_RUBY_MUTATION: #{MUTATION}") unless
  MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)

def rat(value)
  Rational(value.to_s)
end

def rtext(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

def cadd(left, right)
  [left[0] + right[0], left[1] + right[1]]
end

def cmul(left, right)
  [left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]]
end

def cconj(value)
  [value[0], -value[1]]
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
source_expectations['research/r075o_vertical_diffusion_packet_gain.md'] = '0' * 64 if MUTATION == 'source_drift'
source_expectations['research/r075o_vertical_diffusion_packet_gain_primary_audit.md'] = '0' * 64 if MUTATION == 'audit_drift'
source_expectations['research/r075o_report-source.md'] = '0' * 64 if MUTATION == 'report_source_drift'
source_expectations['research/r075e_horizontal_cross_mode_flux_reduction.md'] = '0' * 64 if MUTATION == 'dependency_drift'
source_rows = source_expectations.keys.sort.to_h do |path|
  [path, [source_expectations.fetch(path), Digest::SHA256.file(ROOT + path).hexdigest]]
end
fixture_expected_hash = MUTATION == 'fixture_drift' ? '0' * 64 : FIXTURES_SHA256
expected_expected_hash = MUTATION == 'expected_drift' ? '0' * 64 : EXPECTED_SHA256
fixture_hash = Digest::SHA256.file(FIXTURES).hexdigest
expected_hash = Digest::SHA256.file(EXPECTED).hexdigest

# Exact horizontal Laurent pairing, deliberately evaluated independently.
flux_fixture = fixtures.fetch('horizontalFluxCase')
b_value = rat(flux_fixture.fetch('B'))
c_amp = rat(flux_fixture.fetch('cosAmplitude'))
s_amp = rat(flux_fixture.fetch('sinAmplitude'))
field = {1 => [c_amp / 2, -s_amp / 2], -1 => [c_amp / 2, s_amp / 2]}
d_modes = flux_fixture.fetch('dModes').to_h do |row|
  [row.fetch('ell'), [rat(row.fetch('real')), rat(row.fetch('imag'))]]
end
modal = [Rational(0), Rational(0)]
field.each do |n, cn|
  field.each do |m, cm|
    index = MUTATION == 'flux_difference_index' ? n - m : m - n
    modal = cadd(modal, cmul(d_modes.fetch(index, [Rational(0), Rational(0)]), cmul(cn, cconj(cm))))
  end
end
signed_b = MUTATION == 'flux_B_sign' ? -b_value : b_value
horizontal_observed = {
  'dZero' => MUTATION == 'd0' ? '1+0i' : '0+0i',
  'directX2IntegralOverPi' => rtext(c_amp * s_amp),
  'differenceIndex' => MUTATION == 'flux_difference_index' ? 'n-m' : 'm-n',
  'fluxOverPiPerUnitX3' => rtext(signed_b * modal[0]),
  'modalRealSum' => rtext(modal[0]),
  'outerFactor' => MUTATION == 'flux_outer_half' ? '2*pi*B' : 'pi*B',
  'reconstructionPhase' => MUTATION == 'reconstruction_sign' ? '-i*ell*x2' : '+i*ell*x2',
  'x2PairingFactor' => MUTATION == 'flux_spatial_2pi' ? 'pi' : '2*pi'
}

# Treat q=e^{-t} as an exact rational symbol and compute squared heat weights.
vertical_fixture = fixtures.fetch('verticalContractionCase')
heat_q = rat(vertical_fixture.fetch('q'))
heat_q = 1 / heat_q if MUTATION == 'vertical_heat_growth'
initial_energy = vertical_fixture.fetch('modeEnergies').sum { |row| rat(row.fetch('energy')) }
initial_energy += 1 if MUTATION == 'vertical_l2_norm'
square_factor = MUTATION == 'vertical_square_missing' ? 1 : 2
evolved_energy = vertical_fixture.fetch('modeEnergies').sum do |row|
  rat(row.fetch('energy')) * heat_q**(square_factor * row.fetch('j')**2)
end
vertical_observed = {
  'initialEnergy' => rtext(initial_energy),
  'evolvedEnergy' => rtext(evolved_energy),
  'ratio' => rtext(evolved_energy / initial_energy),
  'contractive' => evolved_energy <= initial_energy
}

# Assemble the finite Schur matrix directly by columns rather than reusing Python rows.
schur_fixture = fixtures.fetch('schurCase')
k_value = schur_fixture.fetch('K')
modes = schur_fixture.fetch('modes')
a_values = schur_fixture.fetch('a').map { |value| rat(value) }
weights = schur_fixture.fetch('dNormByAbsDifference').to_h { |key, value| [key.to_i, rat(value)] }
w_value = rat(schur_fixture.fetch('WInfinity'))
denominator_shift = MUTATION == 'time_kernel_denominator' ? 1 : 0
matrix = modes.map do |n|
  modes.map do |m|
    weights.fetch((m - n).abs, Rational(0)) / (n * n + m * m + denominator_shift)
  end
end
row_sums = matrix.map(&:sum)
column_sums = (0...modes.length).map { |column| matrix.sum { |row| row[column] } }
max_row = row_sums.max + (MUTATION == 'row_sum' ? 1 : 0)
max_column = column_sums.max + (MUTATION == 'column_sum' ? 1 : 0)
schur_bound = w_value / ((MUTATION == 'denominator_lower' ? 1 : 2) * k_value * k_value)
quadratic = (0...modes.length).sum do |i|
  (0...modes.length).sum { |j| matrix[i][j] * a_values[i] * a_values[j] }
end
quadratic += 1 if %w[schur_sqrt quadratic_form_direction].include?(MUTATION)
sum_a_squared = a_values.sum { |value| value * value }
schur_bound *= modes.length if MUTATION == 'mode_count_loss'
abs_b = rat(schur_fixture.fetch('absB'))
pre_parseval = abs_b * w_value * sum_a_squared / (2 * k_value * k_value)
e0_over_pi = 2 * sum_a_squared
final_energy = abs_b * w_value * e0_over_pi / (4 * k_value * k_value)
final_energy += 1 if MUTATION == 'energy_quarter'
schur_observed = {
  'E0OverPi' => rtext(e0_over_pi),
  'finalEnergyBoundOverPi' => rtext(final_energy),
  'kernelQuadraticForm' => rtext(quadratic),
  'maxColumnSum' => rtext(max_column),
  'maxRowSum' => rtext(max_row),
  'parsevalFactor' => MUTATION == 'parseval_factor' ? '4*pi' : '2*pi',
  'preParsevalBoundOverPi' => rtext(pre_parseval),
  'schurBound' => rtext(schur_bound),
  'sumASquared' => rtext(sum_a_squared)
}

# Derive the short-block coefficients from cap, time length, and torus dimension.
cubic_fixture = fixtures.fetch('cubicCase')
cubic_k = cubic_fixture.fetch('K')
cubic_t = rat(cubic_fixture.fetch('T'))
cap = rat(cubic_fixture.fetch('totalFrequencyCapCoefficient'))
cap += 1 if MUTATION == 'cap_four'
short_denominator = cubic_fixture.fetch('shortTimeDenominator').to_i
short_denominator /= 2 if MUTATION == 'short_interval'
short_interval = Rational(1, short_denominator * cubic_k * cubic_k)
heat_square = MUTATION == 'heat_square' ? 1 : 2
endpoint_exponent = heat_square * cap * cubic_k * cubic_k * short_interval
torus_dimension = cubic_fixture.fetch('torusDimension')
torus_dimension = 1 if MUTATION == 'torus_dimension'
holder_factor = %w[holder_volume holder_power].include?(MUTATION) ? '1/sqrt(2*pi)' : '1/(2*pi)'
mass_rational = Rational(1, 2 * short_denominator * cubic_k * cubic_k)
mass_rational *= 2 if %w[time_length mass_16].include?(MUTATION)
inverse_constant = MUTATION == 'inversion_16pi' ? 'e*(8*pi)^(2/3)' : 'e*(16*pi)^(2/3)'
combined_two_power = Rational(8, 3) - (MUTATION == 'combine_div4' ? 1 : 2)
cubic_observed = {
  'combinedConstant' => MUTATION == 'combine_constant' ? 'e*(4*pi)^(2/3)' : 'e*(2*pi)^(2/3)',
  'combinedEPower' => MUTATION == 'mass_e' ? '2' : '1',
  'combinedKPower' => MUTATION == 'inversion_K' ? '-1/3' : '-2/3',
  'combinedMPower' => MUTATION == 'inversion_M' ? '1/3' : '2/3',
  'combinedPiPower' => MUTATION == 'mass_pi' ? '1/3' : '2/3',
  'combinedTwoPower' => rtext(combined_two_power),
  'conditionKSquaredT' => rtext(cubic_k * cubic_k * cubic_t),
  'holderFactor' => holder_factor,
  'inverseConstant' => MUTATION == 'inversion_e' ? 'e^2*(16*pi)^(2/3)' : inverse_constant,
  'massRationalWithoutEPi' => rtext(mass_rational),
  'shortInterval' => rtext(short_interval),
  'squaredDecayExponentAtEndpoint' => rtext(endpoint_exponent)
}

# Rebuild the R/omega normalization and exact rational threshold.
norm = fixtures.fetch('normalizationCase')
payment_r = rat(norm.fetch('paymentRPower'))
payment_omega = rat(norm.fetch('paymentOmegaPower'))
flux_r = rat(norm.fetch('fluxRPower'))
flux_omega = rat(norm.fetch('fluxOmegaPower'))
mass_power = rat(norm.fetch('massPower'))
frequency_power = rat(norm.fetch('frequencyPower'))
payment_r += 1 if MUTATION == 'payment_R'
payment_omega += 1 if MUTATION == 'payment_omega'
flux_r += 1 if MUTATION == 'flux_R'
flux_omega += 1 if MUTATION == 'flux_omega'
mass_power = Rational(1, 3) if MUTATION == 'mass_power'
frequency_power = Rational(-1, 3) if MUTATION == 'frequency_power'
normalized_r = flux_r - payment_r * mass_power
normalized_omega = flux_omega - payment_omega * mass_power
normalized_k = frequency_power
normalized_p = mass_power
normalized_r += 1 if MUTATION == 'normalized_R'
normalized_omega += 1 if MUTATION == 'normalized_omega'
normalized_k += 1 if MUTATION == 'normalized_K'
normalized_p += 1 if MUTATION == 'normalized_p'
shear_r = rat(norm.fetch('shearRPower'))
shear_r = -1 if MUTATION == 'shear_R'
rho = rat(norm.fetch('rho'))
c_gamma = rat(norm.fetch('cGamma'))
rho += Rational(1, 10_000) if MUTATION == 'rate_rho'
c_gamma += Rational(1, 3969) if MUTATION == 'rate_cgamma'
kappa_star = (5 - c_gamma / rho) / 2
kappa_star += Rational(1, 71_442) if MUTATION == 'kappa_numerator'
kappa_star = Rational(98_605, 71_441) if MUTATION == 'kappa_denominator'
kappa_star *= 2 if MUTATION == 'kappa_half'
kappa_star = Rational(197_210, 71_442) if MUTATION == 'kappa_reduce'
frozen_kappa = rat(norm.fetch('frozenKappa'))
frozen_kappa = Rational(4, 3) if MUTATION == 'frozen_kappa'
displayed_rate = rho / 6 - c_gamma / 12
displayed_rate = -displayed_rate if MUTATION == 'rate_sign'
displayed_rate += Rational(1, 238_140_000) if MUTATION == 'rate_fraction'
normalization_observed = {
  'coefficientRPower' => MUTATION == 'coefficient_R' ? '(2*kappa-2)/3' : '(2*kappa-5)/3',
  'displayedExponent' => rtext(displayed_rate),
  'frozenKappa' => rtext(frozen_kappa),
  'kappaStar' => rtext(kappa_star),
  'normalizedKPower' => rtext(normalized_k),
  'normalizedOmegaPower' => rtext(normalized_omega),
  'normalizedPPower' => rtext(normalized_p),
  'normalizedRPower' => rtext(normalized_r),
  'positiveDecayRate' => rtext(-displayed_rate),
  'strictThreshold' => !%w[strict_direction equality_allowed].include?(MUTATION)
}

tags = text.scan(/\\tag\{(O\.[^}]+)\}/).flatten
tags << 'O.1' if MUTATION == 'tag'
references = text.scan(/\(O\.([0-9]+[a-z]?)\)/).flatten.map { |value| "O.#{value}" }
references << 'O.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\\[' }
display_close = text.lines.count { |line| line.strip == '\\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..24).map { |index| "O.#{index}" }

dependencies = %w[
  research/r075e_horizontal_cross_mode_flux_reduction.md
  research/r075g_signed_flux_gain_threshold.md
  research/r075m_dyadic_packet_diffusive_flux_gain.md
  research/r075n_radial_collar_averaged_wiener_row.md
]
dependency_table_present = dependencies.all? do |path|
  text.lines.any? { |line| line.include?(path) && line.include?(FROZEN_SOURCES.fetch(path)) }
end
dependency_table_present = false if MUTATION == 'dependency_table_missing'

required_tokens = [
  '\\mathcal L_B^{(2)} :=\\partial_t+B\\partial_2-\\Delta_{23}',
  'f_n(t)=e^{-n^2t}e^{-inBt}e^{t\\partial_3^2}f_n^0',
  '=\\pi B\\operatorname {Re}\\sum_{n,m}',
  '\\frac{\\|d_{m-n}\\|_\\infty}{n^2+m^2}a_na_m',
  '=\\frac{|B|\\mathcal W_\\infty}{4K^2}E_0',
  'n^2+j^2\\le4K^2',
  '\\frac{e^{-3/2}}{16\\pi}K^{-2}E_0^{3/2}',
  '(16pi)^(2/3)/4=(2pi)^(2/3)',
  'R^{1/3}\\omega^{1/3}K^{-2/3}',
  '\\frac{98605}{71442}',
  '-\\frac{4279}{238140000}',
  '\\mathbf{NOT\\ CLAY}'
]

boundary = {
  'operatorTimeSign' => MUTATION != 'operator_time',
  'operatorDriftSign' => MUTATION != 'operator_drift',
  'operatorVerticalDiffusionSign' => MUTATION != 'operator_vertical_diffusion',
  'horizontalHeatDecay' => MUTATION != 'evolution_horizontal_decay',
  'shearPhaseSign' => MUTATION != 'evolution_shear_phase',
  'verticalHeatSemigroupForward' => MUTATION != 'evolution_vertical_semigroup',
  'constantShearOnly' => !%w[constant_shear B_constant].include?(MUTATION),
  'realPartRetained' => MUTATION != 'flux_real_part',
  'diagonalRemovedBeforeAbsoluteValues' => MUTATION != 'diagonal_before_absolute',
  'etaBetweenZeroAndOne' => !%w[eta_lower eta_upper].include?(MUTATION),
  'etaMeasurable' => MUTATION != 'eta_measurable',
  'cutoffRealPeriodic' => MUTATION != 'xi_real_periodic',
  'WInfinityFinite' => MUTATION != 'w_infty_finite',
  'verticalContractionDirection' => MUTATION != 'vertical_contraction_direction',
  'energyEstimateAllowsArbitraryVerticalFrequencies' => MUTATION != 'arbitrary_vertical_energy',
  'noVerticalCapUsedInEnergyRow' => MUTATION != 'vertical_cap_energy',
  'infiniteTimeKernelUpperBound' => MUTATION != 'time_kernel_infinity',
  'horizontalModesAtLeastK' => MUTATION != 'horizontal_K_lower',
  'schurUpperDirection' => MUTATION != 'schur_direction',
  'quadraticFormUpperDirection' => MUTATION != 'quadratic_form_direction',
  'totalFrequencyCapForCubic' => !%w[total_frequency_cap horizontal_only_cap].include?(MUTATION),
  'finitePacketForCubic' => MUTATION != 'finite_packet',
  'realAdmissibilityForCubic' => MUTATION != 'real_symmetry',
  'KPositiveInteger' => MUTATION != 'K_integer',
  'KSquaredTAtLeastOne' => MUTATION != 'K2T_condition',
  'shortIntervalInsideTimeDomain' => MUTATION != 'short_interval_inside',
  'L2FloorLowerDirection' => MUTATION != 'l2_floor_direction',
  'HolderLowerDirection' => MUTATION != 'holder_direction',
  'torusMeasureIsTwoDimensional' => MUTATION != 'torus_dimension',
  'inverseEnergyUpperDirection' => MUTATION != 'inversion_direction',
  'noVerticalCardinalityLoss' => MUTATION != 'vertical_cardinality_loss',
  'positivePartBoundedByAbsoluteFlux' => MUTATION != 'positive_part',
  'amplitudeHomogeneityTwo' => MUTATION != 'amplitude_degree',
  'canonicalWienerRowInserted' => !%w[wiener_row wiener_L].include?(MUTATION),
  'canonicalChoiceNotUniversal' => !%w[canonical_only universal_cutoff].include?(MUTATION),
  'constantPlateauShearBound' => MUTATION != 'plateau_shear',
  'shearScaleRMinusTwo' => MUTATION != 'shear_R',
  'kappaPowerDirection' => MUTATION != 'kappa_direction',
  'kappaDecimalDisplayOnly' => MUTATION != 'kappa_decimal',
  'strictEndpoint' => !%w[strict_direction equality_allowed].include?(MUTATION),
  'linearLPrefactorRetained' => MUTATION != 'L_prefactor',
  'RInUnitInterval' => MUTATION != 'R_domain',
  'omegaPositive' => MUTATION != 'omega_positive',
  'ownFullTorusAtomOnly' => MUTATION != 'own_full_torus_atom',
  'notVersionMPayment' => MUTATION != 'versionm_claim',
  'physicalCollarLocalizationOpen' => MUTATION != 'collar_localized',
  'arbitraryVerticalCubicNotClaimed' => MUTATION != 'arbitrary_vertical_cubic',
  'totalFrequencyCapRemovalOpen' => MUTATION != 'remove_total_cap',
  'nonconstantShearOpen' => MUTATION != 'nonconstant_closed',
  'interpacketSummationOpen' => MUTATION != 'interpacket_closed',
  'lowDifferencesOpen' => MUTATION != 'lowdifference_closed',
  'E24Open' => MUTATION != 'e24_claim',
  'completeClockOpen' => MUTATION != 'complete_clock',
  'fixedDeletionOpen' => MUTATION != 'fixed_deletion',
  'suitableWeakTransferOpen' => MUTATION != 'suitable_weak',
  'regularityOpen' => MUTATION != 'regularity',
  'singularityOpen' => MUTATION != 'singularity',
  'noNovelty' => MUTATION != 'novelty',
  'noPriority' => MUTATION != 'priority',
  'literatureSearchNotComplete' => MUTATION != 'literature_complete',
  'noSimulation' => MUTATION != 'simulation',
  'noDNS' => MUTATION != 'dns',
  'notClay' => MUTATION != 'clay'
}

checks = {
  'frozen source bindings' => source_rows.values.all? { |wanted, seen| wanted == seen },
  'fixture expected bindings' =>
    fixture_hash == fixture_expected_hash && expected_hash == expected_expected_hash &&
    fixtures.fetch('frozenSources') == FROZEN_SOURCES,
  'primary audit status' =>
    audit_text.include?('Verdict: **PASS**') &&
    audit_text.include?('Mathematical blocker count: **0**') &&
    audit_text.include?('Release blocker count: **0**') &&
    audit_text.include?('main-note SHA-256 is to be frozen by the finite certificate'),
  'four dependencies' => dependency_table_present,
  'operator exact evolution' => %w[
    operatorTimeSign operatorDriftSign operatorVerticalDiffusionSign
    horizontalHeatDecay shearPhaseSign verticalHeatSemigroupForward constantShearOnly
  ].all? { |key| boundary.fetch(key) },
  'horizontal pairing pi sign zero mode' =>
    horizontal_observed == expected.fetch('horizontalFlux') && boundary.fetch('realPartRetained') &&
    boundary.fetch('diagonalRemovedBeforeAbsoluteValues'),
  'vertical heat contraction' =>
    vertical_observed == expected.fetch('verticalContraction') && boundary.fetch('verticalContractionDirection'),
  'schur parseval quarter' =>
    schur_observed == expected.fetch('schur') && max_row <= schur_bound && max_column <= schur_bound &&
    quadratic <= schur_bound * sum_a_squared && boundary.fetch('schurUpperDirection'),
  'arbitrary vertical energy quantifier' => %w[
    energyEstimateAllowsArbitraryVerticalFrequencies noVerticalCapUsedInEnergyRow
    infiniteTimeKernelUpperBound horizontalModesAtLeastK
  ].all? { |key| boundary.fetch(key) },
  'short cubic constants' =>
    cubic_observed == expected.fetch('cubic') && boundary.fetch('L2FloorLowerDirection') &&
    boundary.fetch('HolderLowerDirection') && boundary.fetch('torusMeasureIsTwoDimensional') &&
    boundary.fetch('inverseEnergyUpperDirection') && boundary.fetch('noVerticalCardinalityLoss'),
  'total cap time quantifiers' => %w[
    totalFrequencyCapForCubic finitePacketForCubic realAdmissibilityForCubic
    KPositiveInteger KSquaredTAtLeastOne shortIntervalInsideTimeDomain
  ].all? { |key| boundary.fetch(key) },
  'normalization powers' =>
    normalization_observed == expected.fetch('normalization') &&
    boundary.fetch('positivePartBoundedByAbsoluteFlux') && boundary.fetch('amplitudeHomogeneityTwo'),
  'threshold frozen rate' =>
    kappa_star == Rational(98_605, 71_442) &&
    displayed_rate == Rational(-4279, 238_140_000) && frozen_kappa > kappa_star &&
    boundary.fetch('kappaPowerDirection') && boundary.fetch('strictEndpoint') &&
    boundary.fetch('linearLPrefactorRetained'),
  'canonical collar shear scope' =>
    boundary.fetch('canonicalWienerRowInserted') && boundary.fetch('canonicalChoiceNotUniversal') &&
    boundary.fetch('constantPlateauShearBound'),
  'tags references displays' =>
    tags == expected_tags && tags.uniq.length == 24 && (references.uniq - tags).empty? &&
    display_open == 24 && display_close == 24,
  'formula status sentinels' => required_tokens.all? { |token| flat_text.include?(token.gsub(/\s+/, ' ')) },
  'source report boundary' =>
    flat_source.include?('This negative search result is only a routing fact. It is not evidence of novelty or priority.') &&
    flat_source.include?('requires an upper-frequency cap') &&
    flat_source.include?('not a standalone resolution of E.24'),
  'claim boundary' => boundary.values.all?,
  'utf8 control safety' =>
    !scan_text.include?("\uFFFD") && scan_text.each_codepoint.none? { |code| code < 32 && ![9, 10].include?(code) },
  'python canonical ledger agreement' =>
    python_payload.fetch('schema') == SCHEMA && python_payload.fetch('verdict') == 'PASS' &&
    python_payload.dig('assertions', 'passed') == 19 &&
    python_payload.fetch('horizontalFlux') == horizontal_observed &&
    python_payload.fetch('verticalContraction') == vertical_observed &&
    python_payload.fetch('schur') == schur_observed &&
    python_payload.fetch('cubic') == cubic_observed &&
    python_payload.fetch('normalization') == normalization_observed &&
    python_payload.fetch('claimBoundary') == boundary
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed = checks.select { |_name, passed| !passed }.keys
REPORT.write(
  "# R0.75O independent finite audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Mathematical blockers: #{verdict == 'PASS' ? 0 : failed.length}\n" \
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}\n" \
  "- Failed checks: #{failed.empty? ? 'none' : failed.join('; ')}\n\n" \
  "Independent Rational arithmetic verifies the O.9 pi/sign convention, d_0 " \
  "cancellation, vertical heat contraction, both Schur sums, Parseval, and 1/4.\n\n" \
  "The total-cap fixture verifies the short L2 floor, T^2 Holder factor, O.17, " \
  "e*(16*pi)^(2/3), and reduction to e*(2*pi)^(2/3). Normalization gives " \
  "R^(1/3)omega^(1/3)K^(-2/3)p^(2/3), kappa*=98605/71442, and rate " \
  "-4279/238140000.\n\n" \
  "Arbitrary vertical frequencies are allowed only in the energy row. The cubic " \
  "conversion retains the total-frequency cap and K^2*T>=1. O.24 concerns one " \
  "packet's own full-T^2 atom, not Version-M. **NOT CLAY.**\n"
)
puts JSON.generate(
  'suite' => 'r075o-vertical-diffusion-packet-gain-independent',
  'verdict' => verdict,
  'assertions' => checks.length
)
exit(verdict == 'PASS' ? 0 : 1)
