#!/usr/bin/env ruby
# Independent exact verifier for the frozen R0.75G gain threshold.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075g_signed_flux_gain_threshold.md'
PRIMARY_AUDIT = ROOT + 'research/r075g_signed_flux_gain_threshold_primary_audit.md'
REPORT_SOURCE = ROOT + 'research/r075g_report-source.md'
FIXTURES = ROOT + 'scripts/r075g_signed_flux_gain_threshold_fixtures.json'
EXPECTED = ROOT + 'scripts/r075g_signed_flux_gain_threshold_expected.json'
JSON_PATH = Pathname.new(
  ENV.fetch(
    'R075G_JSON',
    (ROOT + 'research/r075g_signed_flux_gain_threshold_certificate.json').to_s
  )
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075G_RUBY_REPORT',
    (ROOT + 'research/r075g_signed_flux_gain_threshold_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075G_RUBY_MUTATION', '')
SCHEMA = 'r075g-signed-flux-gain-threshold-certificate-v1'

FROZEN_SOURCES = {
  'research/r075c_background_shear_packing_false_positive.md' =>
    '1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89',
  'research/r075d_passive_gradient_route_screen.md' =>
    '54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6',
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075f_modal_phase_integration_identity.md' =>
    'f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440',
  'research/r075g_report-source.md' =>
    '2722d2801945a2ee074b0a9c4a973f592849ae012ddd4c264b7fea5ad76e9896',
  'research/r075g_signed_flux_gain_threshold.md' =>
    'f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41',
  'research/r075g_signed_flux_gain_threshold_primary_audit.md' =>
    '4717b365e5a4dc1bff169db51708a8a74fe51e6dd414a9a68a448813d95541aa'
}.freeze
FIXTURES_SHA256 = '6bcf72a52763b04f98c21109fabbd570aa552cfe472280cff7ff4a0738eb0c9a'
EXPECTED_SHA256 = '03b3475a3f8e82cb986e63ef52af6fdb899ac200b70024661c379542356b6ab0'

NEGATIVE_MUTATIONS = %w[
  source_drift audit_drift report_source_drift dependency_drift
  dependency_table_missing fixture_drift expected_drift tag reference display
  control g9_normalization_r g9_time_r g9_volume_l g9_volume_r g9_b_cubic_r
  g9_cube_root rho_value c_gamma_value alpha_formula alpha_fraction
  equality_non_strict equality_polynomial alpha_third_sign
  alpha_third_denominator alpha_quarter_sign alpha_quarter_denominator
  beta_factor beta_fraction amplitude_flux_degree amplitude_atom_degree
  amplitude_two_thirds amplitude_ratio zero_convention transport_pde_sign
  transport_energy_sign transport_endpoint_sign transport_flux_factor
  transport_cutoff_frequency passage_width_exponent passage_speed_exponent
  passage_occupation_product passage_window_exponent passage_winding
  conditional_proved threshold_necessary equality_closes quarter_counterexample
  amplitude_gain interaction_proved diffusion_benchmark_proved e24_closed
  full_clock fixed_deletion suitable_weak regularity clay
].freeze

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  abort("unknown R075G_RUBY_MUTATION: #{MUTATION}")
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

text = MAIN.read
flat_text = text.gsub(/\s+/, ' ')
scan_text = text + (MUTATION == 'control' ? "\u0001" : '')
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_payload = JSON.parse(JSON_PATH.read)

source_expectations = FROZEN_SOURCES.dup
source_expectations['research/r075g_signed_flux_gain_threshold.md'] =
  '0' * 64 if MUTATION == 'source_drift'
source_expectations[
  'research/r075g_signed_flux_gain_threshold_primary_audit.md'
] = '0' * 64 if MUTATION == 'audit_drift'
source_expectations['research/r075g_report-source.md'] =
  '0' * 64 if MUTATION == 'report_source_drift'
source_expectations[
  'research/r075c_background_shear_packing_false_positive.md'
] = '0' * 64 if MUTATION == 'dependency_drift'
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

# G.9: multiply independent monomials by adding Laurent exponents.
factor_rows = fixtures.fetch('g9Factors').to_h do |item|
  [
    item.fetch('name'),
    %w[L R omega].to_h { |key| [key, rational(item.fetch(key))] }
  ]
end
factor_mutations = {
  'g9_normalization_r' => ['paymentNormalization', 'R', Rational(-1)],
  'g9_time_r' => ['timeLength', 'R', Rational(3)],
  'g9_volume_l' => ['collarVolume', 'L', Rational(1)],
  'g9_volume_r' => ['collarVolume', 'R', Rational(2)],
  'g9_b_cubic_r' => ['bCubed', 'R', Rational(-5)]
}
if factor_mutations.key?(MUTATION)
  name, key, value = factor_mutations.fetch(MUTATION)
  factor_rows.fetch(name)[key] = value
end
g9_product = vector_add(factor_rows.values)
root_denominator = MUTATION == 'g9_cube_root' ? 2 : 3
g9_root = g9_product.transform_values do |value|
  value / root_denominator
end
g9_observed = {
  'product' => vector_text(g9_product),
  'cubeRoot' => vector_text(g9_root)
}

# Threshold arithmetic is recomputed directly from rho and c_gamma.
constants = fixtures.fetch('constants')
rho = rational(constants.fetch('rho'))
c_gamma = rational(constants.fetch('cGamma'))
rho += Rational(1, 10_000) if MUTATION == 'rho_value'
c_gamma += Rational(1, 3969) if MUTATION == 'c_gamma_value'
alpha_denominator = MUTATION == 'alpha_formula' ? 2 * rho : 3 * rho
alpha_star = 1 - c_gamma / alpha_denominator
alpha_star += Rational(1, 107_163) if MUTATION == 'alpha_fraction'
rate = lambda do |alpha, sign, denominator|
  (1 - alpha) * rho / 4 + sign * c_gamma / denominator
end
equality_rate = rate.call(alpha_star, -1, 12)
equality_strict = MUTATION != 'equality_non_strict'
equality_polynomial =
  MUTATION == 'equality_polynomial' ? Rational(0) : Rational(2, 3)
alpha_third = rational(constants.fetch('testAlphas')[0])
alpha_quarter = rational(constants.fetch('testAlphas')[1])
third_rate = rate.call(
  alpha_third,
  MUTATION == 'alpha_third_sign' ? 1 : -1,
  MUTATION == 'alpha_third_denominator' ? 6 : 12
)
quarter_rate = rate.call(
  alpha_quarter,
  MUTATION == 'alpha_quarter_sign' ? 1 : -1,
  MUTATION == 'alpha_quarter_denominator' ? 6 : 12
)
beta_factor = MUTATION == 'beta_factor' ? Rational(2) : Rational(3)
beta_star = beta_factor * alpha_star
beta_star += Rational(1, 35_721) if MUTATION == 'beta_fraction'
threshold_observed = {
  'alphaStar' => rational_text(alpha_star),
  'alphaEqualityRate' => rational_text(equality_rate),
  'alphaEqualityPolynomialPower' => rational_text(equality_polynomial),
  'alphaOneThirdRate' => rational_text(third_rate),
  'alphaOneQuarterRate' => rational_text(quarter_rate),
  'betaStar' => rational_text(beta_star),
  'betaOverAlpha' => rational_text(beta_factor)
}

# Exact amplitude rows; base atoms are literal perfect cubes 3^3 and 2^3.
amplitude = fixtures.fetch('amplitudeCase')
base_flux = rational(amplitude.fetch('baseFlux'))
base_pb = rational(amplitude.fetch('basePB'))
base_pf = rational(amplitude.fetch('basePF'))
amplitude_rows = amplitude.fetch('positiveAmplitudes').to_h do |raw_a|
  a = rational(raw_a)
  flux_degree = MUTATION == 'amplitude_flux_degree' ? 1 : 2
  atom_degree = MUTATION == 'amplitude_atom_degree' ? 2 : 3
  two_thirds_degree = MUTATION == 'amplitude_two_thirds' ? 3 : 2
  flux = base_flux * a**flux_degree
  p_af = base_pf * a**atom_degree
  p_af_two_thirds = 4 * a**two_thirds_degree
  ratio = flux / (3 * p_af_two_thirds)
  ratio += 1 if MUTATION == 'amplitude_ratio' && raw_a == '3'
  [
    raw_a,
    {
      'flux' => rational_text(flux),
      'pAF' => rational_text(p_af),
      'pAFTwoThirds' => rational_text(p_af_two_thirds),
      'correlationRatio' => rational_text(ratio)
    }
  ]
end
zero_convention =
  MUTATION == 'zero_convention' ?
  '1' :
  amplitude.fetch('zeroSignedNumeratorConvention')

# Pure transport, independently through Fourier constant coefficients.
# H^2 has coefficients 1/2 at zero and exp(+/-2it)/4 at +/-2.
transport = fixtures.fetch('pureTransportCase')
drift = rational(transport.fetch('drift'))
cutoff_mean = rational(transport.fetch('cutoffMean'))
cutoff_amplitude = rational(transport.fetch('cutoffSineAmplitude'))
xi_plus = Complex(0, -cutoff_amplitude / 2)
xi_minus = xi_plus.conjugate
h2_initial = {0 => Rational(1, 2), 2 => Rational(1, 4), -2 => Rational(1, 4)}
h2_terminal = {
  0 => Rational(1, 2),
  2 => Complex(0, Rational(-1, 4)),
  -2 => Complex(0, Rational(1, 4))
}
weighted_mean = lambda do |h2|
  cutoff_mean * h2.fetch(0) +
    xi_plus * h2.fetch(-2) +
    xi_minus * h2.fetch(2)
end
initial_energy = weighted_mean.call(h2_initial).real / 2
terminal_energy = weighted_mean.call(h2_terminal).real / 2
endpoint_difference = terminal_energy - initial_energy
endpoint_difference *= -1 if MUTATION == 'transport_endpoint_sign'
pde_sign = MUTATION == 'transport_pde_sign' ? -1 : 1
energy_sign = MUTATION == 'transport_energy_sign' ? -1 : 1
flux_multiplier =
  MUTATION == 'transport_flux_factor' ? Rational(1, 2) : Rational(1, 4)
# Integral_0^(pi/4) cos(2t) dt = 1/2.
integrated_flux =
  if MUTATION == 'transport_cutoff_frequency'
    Rational(0)
  else
    pde_sign * energy_sign * drift * cutoff_amplitude *
      flux_multiplier * Rational(1, 2)
  end
transport_observed = {
  'initialHalfEnergy' => rational_text(initial_energy),
  'terminalHalfEnergy' => rational_text(terminal_energy),
  'endpointDifference' => rational_text(endpoint_difference),
  'integratedPositiveFlux' => rational_text(integrated_flux),
  'identityResidual' => rational_text(integrated_flux - endpoint_difference),
  'cutoffMinimum' => rational_text(cutoff_mean - cutoff_amplitude),
  'cutoffMaximum' => rational_text(cutoff_mean + cutoff_amplitude)
}

# One exact monotone unwrapped crossing q(t)=v*t.
passage = fixtures.fetch('singlePassageCase')
r_value = rational(passage.fetch('R'))
width_factor = rational(passage.fetch('intervalWidthFactor'))
speed_factor = rational(passage.fetch('speedLowerFactor'))
window_factor = rational(passage.fetch('fullWindowFactor'))
width_power = MUTATION == 'passage_width_exponent' ? 2 : 1
speed_power = MUTATION == 'passage_speed_exponent' ? -1 : -2
width = width_factor * r_value**width_power
speed = speed_factor * r_value**speed_power
occupation =
  MUTATION == 'passage_occupation_product' ? width * speed : width / speed
window_power = MUTATION == 'passage_window_exponent' ? 3 : 2
window = window_factor * r_value**window_power
fraction = occupation / window
passage_observed = {
  'intervalWidth' => rational_text(width),
  'speedLowerBound' => rational_text(speed),
  'occupationUpperBound' => rational_text(occupation),
  'rCubed' => rational_text(r_value**3),
  'occupationOverRCubed' => rational_text(occupation / r_value**3),
  'fullWindowLength' => rational_text(window),
  'occupationFraction' => rational_text(fraction),
  'occupationFractionOverR' => rational_text(fraction / r_value),
  'occupationRExponent' => (width_power - speed_power).to_s,
  'relativeFractionRExponent' => (width_power - speed_power - window_power).to_s
}

tags = text.scan(/\\tag\{(G\.[^}]+)\}/).flatten
tags << 'G.1' if MUTATION == 'tag'
references = text.scan(/\(G\.([0-9]+[a-z]?)\)/).flatten.map do |value|
  "G.#{value}"
end
references << 'G.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\[' }
display_close = text.lines.count { |line| line.strip == '\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..24).map { |index| "G.#{index}" }

dependency_paths = %w[
  research/r075c_background_shear_packing_false_positive.md
  research/r075d_passive_gradient_route_screen.md
  research/r075e_horizontal_cross_mode_flux_reduction.md
  research/r075f_modal_phase_integration_identity.md
]
dependency_table_present = dependency_paths.all? do |path|
  text.lines.any? do |line|
    line.include?(path) && line.include?(FROZEN_SOURCES.fetch(path))
  end
end
dependency_table_present = false if MUTATION == 'dependency_table_missing'

required_tokens = [
  '\\alpha>\\alpha_*:=1-\\frac{c_\\gamma}{3\\rho}',
  '\\frac{27163}{107163}',
  '-\\frac{4279}{238140000}<0',
  '\\frac{1489}{1905120000}>0',
  'R^{-2}\\omega (R^2)(L^2R^3)(R^{-6})',
  '\\beta>\\beta_*:=3\\alpha_*',
  '\\frac{27163}{35721}',
  '\\mathfrak X_{\\xi,R}(AF,b)=A^2\\mathfrak X_{\\xi,R}(F,b)',
  '\\le C R^3',
  '\\partial_tH+b(t)\\partial_2H=0',
  'not a proof for the passive advection-diffusion problem',
  'None of those three outcomes is established here.',
  '\\mathbf{NOT\\ CLAY}'
]

e_text = (ROOT + 'research/r075e_horizontal_cross_mode_flux_reduction.md').read
f_text = (ROOT + 'research/r075f_modal_phase_integration_identity.md').read
audit_text = PRIMARY_AUDIT.read
boundary = {
  'G1ConditionalUnproved' => MUTATION != 'conditional_proved',
  'thresholdOnlyForG1Route' => MUTATION != 'threshold_necessary',
  'equalityDoesNotCloseUnrefined' => MUTATION != 'equality_closes',
  'quarterIsNotCounterexample' => MUTATION != 'quarter_counterexample',
  'amplitudeCannotCreateGain' => MUTATION != 'amplitude_gain',
  'interactionAtomUnproved' => MUTATION != 'interaction_proved',
  'singleUnwrappedPassageOnly' => MUTATION != 'passage_winding',
  'pureTransportNotDiffusiveProof' => MUTATION != 'diffusion_benchmark_proved',
  'E24Open' => MUTATION != 'e24_closed',
  'completeClockOpen' => MUTATION != 'full_clock',
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
      'r075g-signed-flux-gain-threshold-fixtures-v1' &&
    expected.fetch('schema') ==
      'r075g-signed-flux-gain-threshold-expected-v1' &&
    fixtures.fetch('frozenSources') == FROZEN_SOURCES,
  'primary audit main binding and PASS/0 status' =>
    audit_text.include?(FROZEN_SOURCES.fetch(
      'research/r075g_signed_flux_gain_threshold.md'
    )) &&
    audit_text.include?(
      'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.'
    ) &&
    audit_text.include?('Equation tags G.1--G.24 are unique and consecutive.'),
  'C/D/E/F table entries in main' => dependency_table_present,
  'G.9 exponent product' =>
    g9_observed.fetch('product') == expected.dig('g9', 'product'),
  'G.10 cube-root exponents' =>
    g9_observed.fetch('cubeRoot') == expected.dig('g9', 'cubeRoot'),
  'alpha star and strict equality boundary' =>
    threshold_observed.fetch('alphaStar') ==
      expected.dig('threshold', 'alphaStar') &&
    equality_rate == 0 && equality_polynomial == Rational(2, 3) &&
    equality_strict,
  'alpha one-third and one-quarter exact margins' =>
    rational_text(third_rate) ==
      expected.dig('threshold', 'alphaOneThirdRate') &&
    third_rate < 0 &&
    rational_text(quarter_rate) ==
      expected.dig('threshold', 'alphaOneQuarterRate') &&
    quarter_rate > 0,
  'beta star equals three alpha star' =>
    rational_text(beta_star) == expected.dig('threshold', 'betaStar') &&
    beta_factor == 3,
  'amplitude homogeneity finite family' =>
    amplitude_rows == expected.fetch('amplitudeRows') &&
    base_pb == 3**3 && base_pf == 2**3 && zero_convention == '0',
  'pure transport Fourier endpoint energies' =>
    transport_observed.fetch('initialHalfEnergy') ==
      expected.dig('pureTransportNormalized', 'initialHalfEnergy') &&
    transport_observed.fetch('terminalHalfEnergy') ==
      expected.dig('pureTransportNormalized', 'terminalHalfEnergy') &&
    transport_observed.fetch('cutoffMinimum') == '1/4' &&
    transport_observed.fetch('cutoffMaximum') == '3/4',
  'pure transport positive flux and endpoint difference' =>
    transport_observed == expected.fetch('pureTransportNormalized') &&
    integrated_flux > 0 && integrated_flux == endpoint_difference,
  'single unwrapped G.20 occupation scale' =>
    passage_observed == expected.fetch('singlePassage'),
  '24 tags, references, and displays' =>
    tags == expected_tags && tags.uniq.length == 24 &&
    (references - tags).empty? &&
    display_open == 24 && display_close == 24,
  'external E/F references and formula sentinels' =>
    e_text.include?('\\tag{E.22}') &&
    f_text.include?('\\tag{F.17}') &&
    f_text.include?('\\tag{F.18}') &&
    required_tokens.all? do |token|
      flat_text.include?(token.gsub(/\s+/, ' '))
    end,
  'claim boundary' => boundary.values.all?,
  'Python schema and exact-ledger cross-check' =>
    python_payload.fetch('schema') == SCHEMA &&
    python_payload.fetch('verdict') == 'PASS' &&
    python_payload.fetch('g9ExponentLedger') == g9_observed &&
    python_payload.fetch('thresholdLedger') == threshold_observed &&
    python_payload.fetch('amplitudeRows') == amplitude_rows &&
    python_payload.fetch('pureTransportNormalized') == transport_observed &&
    python_payload.fetch('singlePassage') == passage_observed,
  'UTF-8 and control safety' =>
    scan_text.valid_encoding? &&
    !scan_text.each_codepoint.any? do |code|
      code < 32 && ![9, 10].include?(code)
    end
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed = checks.reject { |_name, passed| passed }.keys
REPORT.write(
  "# R0.75G independent finite audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}\n" \
  "- Fixture SHA-256: #{fixture_hash}\n" \
  "- Expected SHA-256: #{expected_hash}\n" \
  "- Failed checks: #{failed.empty? ? 'none' : failed.join('; ')}\n\n" \
  "Ruby independently adds Laurent exponents, recomputes every rational " \
  "threshold and margin, and checks the amplitude family. For pure transport " \
  "it extracts Fourier constant coefficients instead of using the Python " \
  "trigonometric formula; the positive flux and endpoint difference are both " \
  "1/32. The rational monotone lift gives occupation O(R^3) and relative " \
  "fraction O(R).\n\n" \
  "G.1, G.18, and G.24 remain unproved sufficient targets. The one-passage " \
  "and pure-transport examples are benchmarks, not arbitrary diffusive-field " \
  "estimates. E.24 and all larger claims remain OPEN. **NOT CLAY.**\n"
)

puts JSON.generate(
  suite: 'r075g-signed-flux-gain-threshold-independent',
  verdict: verdict,
  assertions: checks.length
)
exit(verdict == 'PASS' ? 0 : 1)
