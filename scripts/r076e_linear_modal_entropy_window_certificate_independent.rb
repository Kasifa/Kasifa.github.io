#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed exact-arithmetic audit for frozen R0.76E.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
STEM = 'r076e_linear_modal_entropy_window'
MAIN = ROOT.join("research/#{STEM}.md")
PRIMARY = ROOT.join("research/#{STEM}_primary_audit.md")
SOURCE = ROOT.join('research/r076e_report-source.md')
FIXTURES = ROOT.join("scripts/#{STEM}_fixtures.json")
EXPECTED = ROOT.join("scripts/#{STEM}_expected.json")
CERTIFICATE = Pathname.new(ENV.fetch('R076E_JSON', ROOT.join("research/#{STEM}_certificate.json").to_s))
OUT = Pathname.new(ENV.fetch('R076E_RUBY_REPORT', ROOT.join("research/#{STEM}_independent_audit.md").to_s))
MUTATION = ENV.fetch('R076E_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => '1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4',
  "research/#{STEM}_primary_audit.md" => '5ce8fb3f2f2f487002b0e391db49855edb3cff72574058e26150813d69615d27',
  'research/r076e_report-source.md' => '10e506fa9d250b14d9f42f6eac7c2c83cfca934a85a2da6e223cd473f21e0c12',
  'research/r076d_quantitative_growing_mode_entropy_window.md' => 'cd94e3384f01963cb7b8a14fdb8376c6197c361473447f15500db0acac5e958e',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075b_bulk_clock_outer_padding_gate.md' => '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a'
}.freeze
FIXTURES_SHA256 = '9b5b0a7d88fe31d4156a7fbc8f73b52a9b5a8271437ee1be867970cec244cf47'
EXPECTED_SHA256 = 'af6c1fd49d57945306f5f97a99f160a8fcbaec21bce887b78fe74e0bbe4d4f80'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash d_hash r_hash clock_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema expected_schema],
  'integrity' => %w[utf8 controls no_cr no_trailing tags display_opens display_closes unnumbered references tex_qquad tex_quad tex_frac tex_linebreak],
  'geometry' => %w[delta_order support_radius support_bound plateau_length plateau_bound],
  'scaled' => %w[positive_q integer_modes ordered_modes dyadic_band ell kappas alpha n1r lambda clock_t clock_mass velocity real_band],
  'space' => %w[term_count turan_power chebyshev length_ratio spatial_formula gap_free],
  'split' => %w[terms m m_plus_one d0_power two_power start start_conditions start_power decay_power binary_exponent binary_negative early_power late_threshold late_monotone endpoint_power endpoint_threshold],
  'endpoint' => %w[unit_length unit_chebyshev unit_ratio finite_insertion finite_absorption large_monotone stronger_power endpoint_formula full_mass no_factorial],
  'energy' => %w[gradient_lambda q_squared gradient_coefficient weighted_power endpoint_lambda_power heat_clock_mass cutoff_definition cutoff_rows energy_identity gradient_inequality q_absorption speed_zero],
  'scale' => %w[flux_prefactor mass_prefactor target normalized r_cancel frozen_rate new_window witness_new witness_old],
  'proof' => %w[main_bound normalized_bound stable_family split_choice early_bound late_bound weighted_bound endpoint_bound bounded_branch heat_branch onset_bound physical_row exact_pde complete_square no_projection],
  'source' => %w[nazarov friedland_yomdin erdelyi theorem_number complex_scope adjacent_real adjacent_shift local_split source_table no_new_theorem no_novelty finite_not_proof primary_pass blocker_zero],
  'boundary' => %w[exact_shear one_band growing_constant r075r_compatible arbitrary_packets_open version_m_conditional regularity_open singularity_open no_figure no_simulation not_clay sole_publisher]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

def flat(value)
  value.gsub(/\s+/, ' ')
end

def q(value)
  Rational(value.to_s)
end

def qstr(value)
  value.denominator == 1 ? value.numerator.to_s : "#{value.numerator}/#{value.denominator}"
end

def encoded(values)
  values.transform_values { |value| value.denominator == 1 ? value.numerator : qstr(value) }
end

def fragments?(value, parts)
  parts.all? { |part| value.include?(part) }
end

def clean_bytes?(data)
  data.dup.force_encoding(Encoding::UTF_8).valid_encoding? &&
    data.bytes.none? { |byte| (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127 }
end

abort "unknown R076E_RUBY_MUTATION: #{MUTATION}" unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
abort 'duplicate mutation name in R0.76E Ruby suite' unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

main_bytes = MAIN.binread
primary_bytes = PRIMARY.binread
source_bytes = SOURCE.binread
main_text = main_bytes.force_encoding(Encoding::UTF_8)
primary_text = primary_bytes.force_encoding(Encoding::UTF_8)
source_text = source_bytes.force_encoding(Encoding::UTF_8)
compact = flat(main_text)
compact_primary = flat(primary_text)
compact_source = flat(source_text)
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_certificate = JSON.parse(CERTIFICATE.read)
bindings = FROZEN.keys.sort.to_h do |path|
  [path, {'expectedSha256' => FROZEN.fetch(path), 'observedSha256' => sha256(ROOT.join(path))}]
end

delta0 = q(fixtures.dig('profile', 'delta0'))
delta = q(fixtures.dig('profile', 'delta'))
scaled_fixture = fixtures.fetch('scaledCase')
q_count = scaled_fixture.fetch('q').to_i
a_value = q(scaled_fixture.fetch('a'))
radius = q(scaled_fixture.fetch('R'))
b_shear = q(scaled_fixture.fetch('B'))
modes = scaled_fixture.fetch('frequencies').map { |value| q(value) }
ell = a_value * radius
kappas = modes.map { |mode| mode * ell }
alpha = kappas.first
n1r = modes.first * radius
lambda_value = (alpha / a_value)**2
temporal_end = q(fixtures.dig('clock', 'scaledClockEnd')) * lambda_value
velocity = b_shear * radius / a_value
real_magnitudes = kappas.map { |kappa| (kappa / alpha)**2 }

geometry = {
  'supportRadius' => qstr(1 + delta / a_value),
  'supportWithinThreeHalves' => 1 + delta / a_value <= q('3/2'),
  'centralPlateauLength' => qstr(2 - 2 * delta / a_value),
  'centralPlateauAtLeastOne' => 2 - 2 * delta / a_value >= 1
}
scaled = {
  'ell' => qstr(ell), 'kappas' => kappas.map { |value| qstr(value) },
  'alpha' => qstr(alpha), 'n1R' => qstr(n1r), 'lambda' => qstr(lambda_value),
  'T' => qstr(temporal_end), 'KOverH' => qstr(lambda_value),
  'dyadicBand' => modes.last <= 2 * modes.first, 'v' => qstr(velocity),
  'realPartsWithinMinusFourMinusOne' => real_magnitudes.min >= 1 && real_magnitudes.max <= 4
}

max_terms = 2 * q_count
space = {
  'maximumTerms' => max_terms,
  'turanExponent' => max_terms - 1,
  'lengthRatio' => qstr(q(fixtures.dig('spatialObservation', 'jPlusLength')) /
                        q(fixtures.dig('spatialObservation', 'chebyshevMeasureLower')))
}

delayed = fixtures.fetch('delayedSplit')
n_terms = delayed.fetch('maximumTerms').to_i
m_value = 2 * (n_terms - 1)
m_plus_one = m_value + 1
sample_d0 = delayed.fetch('sampleD0').to_i
sample_start = delayed.fetch('sampleStart').to_i
strict_power = delayed.fetch('sampleStartStrictPowerOfTwoUpper').to_i
d0_power = 2 * n_terms
two_power = m_value
start_power = strict_power * m_plus_one
decay_power = -2 * sample_start
binary_exponent = d0_power + two_power + start_power + decay_power
early_power = q(delayed.fetch('earlyWeightPower') + 1) / q(delayed.fetch('earlyWeightPower'))
endpoint_power = q(m_value) + q(delayed.fetch('endpointTimePower'))
split = {
  'maximumTerms' => n_terms, 'm' => m_value, 'mPlusOne' => m_plus_one,
  'sampleD0Power' => d0_power, 'sampleTwoPower' => two_power,
  'sampleStart' => sample_start, 'sampleStartPowerContribution' => start_power,
  'decayPowerContribution' => decay_power, 'strictBinaryUpperExponent' => binary_exponent,
  'weightedEarlyPower' => qstr(early_power), 'lateMonotoneThreshold' => m_plus_one,
  'endpointPower' => qstr(endpoint_power), 'endpointMonotoneThreshold' => qstr(endpoint_power / 2)
}

ledger = fixtures.fetch('lambdaLedger')
weighted_power = q(ledger.dig('gradientPrefactor', 'lambda')) +
                 q(ledger.dig('changeOfClock', 'sPerTau', 'lambda')) +
                 q(ledger.dig('changeOfClock', 'dsPerDtau', 'lambda')) +
                 q(ledger.dig('weightedClock', 'K')) * q(ledger.dig('clockMass', 'KPerH', 'lambda'))
endpoint_lambda_power = q(ledger.dig('endpointClock', 'T')) +
                        q(ledger.dig('endpointClock', 'K')) * q(ledger.dig('clockMass', 'KPerH', 'lambda'))
q_squared = q(q_count * q_count) / q(a_value * a_value)
energy = {
  'lambda' => qstr(lambda_value), 'qSquaredOverASquared' => qstr(q_squared),
  'gradientCoefficient' => qstr(lambda_value + q_squared),
  'weightedLambdaPower' => qstr(weighted_power),
  'endpointLambdaPower' => qstr(endpoint_lambda_power)
}
scale = {
  'fluxPrefactor' => encoded({'a' => q(2), 'R' => q(3), 'v' => q(1)}),
  'massPrefactor' => encoded({'a' => q(2), 'R' => q(5), 'H' => q(1)}),
  'afterMass' => encoded({'a' => q('2/3'), 'R' => q('-1/3'), 'M' => q('2/3')}),
  'normalized' => encoded({'a' => q('2/3'), 'R' => q(0), 'omega' => q('1/3'), 'p' => q('2/3')}),
  'frozenRate' => qstr(-q(fixtures.dig('frozenScales', 'cGamma')) / 12)
}

tags = main_text.scan(/\\tag\{E\.(\d+)\}/).flatten.map(&:to_i)
refs = main_text.scan(/(?<![A-Za-z0-9_.])E\.(\d+)/).flatten.map(&:to_i)
opens = main_text.scan(/^\\\[$/).length
closes = main_text.scan(/^\\\]$/).length

checks = {
  'bindings' => {
    'main_hash' => bindings.fetch("research/#{STEM}.md").values.uniq.length == 1,
    'primary_hash' => bindings.fetch("research/#{STEM}_primary_audit.md").values.uniq.length == 1,
    'source_hash' => bindings.fetch('research/r076e_report-source.md').values.uniq.length == 1,
    'd_hash' => bindings.fetch('research/r076d_quantitative_growing_mode_entropy_window.md').values.uniq.length == 1,
    'r_hash' => bindings.fetch('research/r075r_outer_cap_spectral_concentration_obstruction.md').values.uniq.length == 1,
    'clock_hash' => bindings.fetch('research/r075b_bulk_clock_outer_padding_gate.md').values.uniq.length == 1
  },
  'inputs' => {
    'fixture_hash' => sha256(FIXTURES) == FIXTURES_SHA256,
    'expected_hash' => sha256(EXPECTED) == EXPECTED_SHA256,
    'fixture_schema' => fixtures.fetch('schema') == 'r076e-linear-modal-entropy-window-fixtures-v1',
    'expected_schema' => expected.fetch('schema') == 'r076e-linear-modal-entropy-window-expected-v1'
  },
  'integrity' => {
    'utf8' => [main_bytes, primary_bytes, source_bytes].all? { |value| clean_bytes?(value) },
    'controls' => clean_bytes?(main_bytes),
    'no_cr' => [main_bytes, primary_bytes, source_bytes].none? { |value| value.include?("\r") },
    'no_trailing' => [main_text, primary_text, source_text].all? { |value| value.lines.none? { |line| line.chomp.end_with?(' ', "\t") } },
    'tags' => tags == (1..34).to_a, 'display_opens' => opens == 38,
    'display_closes' => closes == 38, 'unnumbered' => opens - tags.length == 4,
    'references' => (refs.uniq - tags.uniq).empty?,
    'tex_qquad' => main_text !~ /(?<!\\)\bqquad\b/,
    'tex_quad' => main_text !~ /(?<!\\)\bquad\b/,
    'tex_frac' => main_text !~ /(?<!\\)\bfrac\{/,
    'tex_linebreak' => main_text.lines.none? { |line| line.chomp.end_with?('\\') && !line.chomp.end_with?('\\\\') }
  },
  'geometry' => {
    'delta_order' => 0 < delta0 && delta0 < delta,
    'support_radius' => geometry['supportRadius'] == expected.dig('geometry', 'supportRadius'),
    'support_bound' => geometry['supportWithinThreeHalves'] == expected.dig('geometry', 'supportWithinThreeHalves'),
    'plateau_length' => geometry['centralPlateauLength'] == expected.dig('geometry', 'centralPlateauLength'),
    'plateau_bound' => geometry['centralPlateauAtLeastOne'] == expected.dig('geometry', 'centralPlateauAtLeastOne')
  },
  'scaled' => {
    'positive_q' => q_count >= 1,
    'integer_modes' => modes.all? { |value| value.denominator == 1 && value >= 1 },
    'ordered_modes' => modes == modes.uniq.sort,
    'dyadic_band' => scaled['dyadicBand'] == expected.dig('scaledCase', 'dyadicBand'),
    'ell' => scaled['ell'] == expected.dig('scaledCase', 'ell'),
    'kappas' => scaled['kappas'] == expected.dig('scaledCase', 'kappas'),
    'alpha' => scaled['alpha'] == expected.dig('scaledCase', 'alpha'),
    'n1r' => scaled['n1R'] == expected.dig('scaledCase', 'n1R'),
    'lambda' => scaled['lambda'] == expected.dig('scaledCase', 'lambda') && lambda_value == n1r**2,
    'clock_t' => scaled['T'] == expected.dig('scaledCase', 'T'),
    'clock_mass' => scaled['KOverH'] == expected.dig('scaledCase', 'KOverH'),
    'velocity' => scaled['v'] == expected.dig('scaledCase', 'v'),
    'real_band' => scaled['realPartsWithinMinusFourMinusOne'] == expected.dig('scaledCase', 'realPartsWithinMinusFourMinusOne')
  },
  'space' => {
    'term_count' => space['maximumTerms'] == expected.dig('spatialObservation', 'maximumTerms'),
    'turan_power' => space['turanExponent'] == expected.dig('spatialObservation', 'turanExponent'),
    'chebyshev' => q(fixtures.dig('spatialObservation', 'chebyshevMeasureLower')) == q('1/2'),
    'length_ratio' => space['lengthRatio'] == expected.dig('spatialObservation', 'lengthRatio'),
    'spatial_formula' => fragments?(compact, ['D^{2q}h(s)^{1/3}', '(\alpha+q)^{-1}\|G_z(s)\|_{L^\infty(J)}']),
    'gap_free' => fragments?(compact_primary, ['No imaginary-frequency size', 'gap, or spectral-gap denominator'])
  },
  'split' => {
    'terms' => split['maximumTerms'] == expected.dig('delayedSplit', 'maximumTerms'),
    'm' => split['m'] == expected.dig('delayedSplit', 'm'),
    'm_plus_one' => split['mPlusOne'] == expected.dig('delayedSplit', 'mPlusOne'),
    'd0_power' => split['sampleD0Power'] == expected.dig('delayedSplit', 'sampleD0Power') && sample_d0 == 2,
    'two_power' => split['sampleTwoPower'] == expected.dig('delayedSplit', 'sampleTwoPower'),
    'start' => split['sampleStart'] == expected.dig('delayedSplit', 'sampleStart'),
    'start_conditions' => sample_start >= [4, m_plus_one].max && sample_start < 2**strict_power,
    'start_power' => split['sampleStartPowerContribution'] == expected.dig('delayedSplit', 'sampleStartPowerContribution'),
    'decay_power' => split['decayPowerContribution'] == expected.dig('delayedSplit', 'decayPowerContribution'),
    'binary_exponent' => split['strictBinaryUpperExponent'] == expected.dig('delayedSplit', 'strictBinaryUpperExponent'),
    'binary_negative' => binary_exponent.negative?,
    'early_power' => split['weightedEarlyPower'] == expected.dig('delayedSplit', 'weightedEarlyPower'),
    'late_threshold' => split['lateMonotoneThreshold'] == expected.dig('delayedSplit', 'lateMonotoneThreshold'),
    'late_monotone' => sample_start >= m_plus_one,
    'endpoint_power' => split['endpointPower'] == expected.dig('delayedSplit', 'endpointPower'),
    'endpoint_threshold' => split['endpointMonotoneThreshold'] == expected.dig('delayedSplit', 'endpointMonotoneThreshold') && sample_start >= endpoint_power / 2
  },
  'endpoint' => {
    'unit_length' => q(fixtures.dig('lastUnit', 'intervalLength')) == q(expected.dig('lastUnit', 'intervalLength')),
    'unit_chebyshev' => q(fixtures.dig('lastUnit', 'chebyshevMeasureLower')) == q('1/2'),
    'unit_ratio' => qstr(q(fixtures.dig('lastUnit', 'intervalLength')) / q(fixtures.dig('lastUnit', 'chebyshevMeasureLower'))) == expected.dig('lastUnit', 'lengthRatio'),
    'finite_insertion' => fragments?(compact, ['S_N^{2/3}T^{-2/3}', '4<=T<=S_N']),
    'finite_absorption' => compact.scan('D_1^{2N}S_N^{2/3}').length == 1 && compact.scan('\le e^{CN}T^{-2/3}').length >= 1,
    'large_monotone' => compact.scan('`T^(m+2/3)e^(-2T)` decreases').length == 1,
    'stronger_power' => fragments?(compact, ['stronger power `m+1` in E.15', 'S_N^{m+2/3}e^{-2S_N}']),
    'endpoint_formula' => compact.scan('k(T)^{2/3}\le e^{CN}T^{-2/3}K_T^{2/3}').length == 1,
    'full_mass' => compact.scan('full `K_T`').length == 1 && compact.scan('full mass').length >= 1,
    'no_factorial' => compact.scan('Endpoint estimate without a factorial').length == 1
  },
  'energy' => {
    'gradient_lambda' => energy['lambda'] == expected.dig('energy', 'lambda'),
    'q_squared' => energy['qSquaredOverASquared'] == expected.dig('energy', 'qSquaredOverASquared'),
    'gradient_coefficient' => energy['gradientCoefficient'] == expected.dig('energy', 'gradientCoefficient'),
    'weighted_power' => energy['weightedLambdaPower'] == expected.dig('energy', 'weightedLambdaPower'),
    'endpoint_lambda_power' => energy['endpointLambdaPower'] == expected.dig('energy', 'endpointLambdaPower'),
    'heat_clock_mass' => compact.scan('K_T=\lambda H').length == 1,
    'cutoff_definition' => compact.scan('Define `zeta(s):=eta_R(R^2s)`').length == 1,
    'cutoff_rows' => fragments?(compact, ['\zeta(0)=0', "|\\zeta'|\\le C_\\eta", '\zeta(s)\le C_\eta s']),
    'energy_identity' => fragments?(compact, ['exact identity for the complete real square', '2a^{-2}\int_0^4\zeta\int\Xi_a|G_z|^2']),
    'gradient_inequality' => compact_primary.scan('a^(-2)(alpha+q)^2 <= C(lambda+q^2/a^2)').length == 1,
    'q_absorption' => fragments?(compact, ['q^2/a^2` part costs at most `q^2`', 'absorbed by one `e^(C_*q)`']),
    'speed_zero' => compact_primary.scan('`B=0` remains covered').length == 1
  },
  'scale' => {
    'flux_prefactor' => scale['fluxPrefactor'] == expected.dig('scaleLedger', 'fluxPrefactor'),
    'mass_prefactor' => scale['massPrefactor'] == expected.dig('scaleLedger', 'massPrefactor'),
    'target' => scale['afterMass'] == expected.dig('scaleLedger', 'afterMass'),
    'normalized' => scale['normalized'] == expected.dig('scaleLedger', 'normalized'),
    'r_cancel' => scale.dig('normalized', 'R').zero?,
    'frozen_rate' => scale['frozenRate'] == expected.dig('scaleLedger', 'frozenRate'),
    'new_window' => compact.scan('q(L)=o(L^2)').length >= 2,
    'witness_new' => fixtures.dig('windowWitness', 'newRatio') == expected.dig('windowWitness', 'newRatio') && expected.dig('windowWitness', 'newLimit').zero?,
    'witness_old' => fixtures.dig('windowWitness', 'oldRatio') == expected.dig('windowWitness', 'oldRatio') && expected.dig('windowWitness', 'oldLimit') == 2
  },
  'proof' => {
    'main_bound' => fragments?(compact, ['|\mathcal T_{\boldsymbol n,R}|', '\le e^{C_*q}a^{2/3}R^{-1/3}']),
    'normalized_bound' => fragments?(compact, ['\mathfrak X_{\boldsymbol n,R}', '\le e^{C_*q}a^{2/3}\omega^{1/3}']),
    'stable_family' => fragments?(compact, ['-4\le\operatorname {Re}\mu_r\le-1', 'K_U:=\int_0^Uk(\tau)d\tau']),
    'split_choice' => fragments?(compact, ['S_N=C_0N\log(N+1)', 'D_0^{2N}2^mS_N^{m+1}e^{-2S_N}\le1']),
    'early_bound' => fragments?(compact, ['4^{-1/3}S_N^{4/3}K_T^{2/3}', 'full observed mass']),
    'late_bound' => fragments?(compact, ['\int_{S_N}^\infty', '\le1']),
    'weighted_bound' => compact.scan('[N\log(N+1)]^{4/3}K_T^{2/3}').length == 1,
    'endpoint_bound' => compact.scan('e^{CN}T^{-2/3}K_T^{2/3}').length >= 2,
    'bounded_branch' => compact.scan('If `lambda<=1`').length == 1,
    'heat_branch' => compact.scan('If `lambda>1`').length == 1,
    'onset_bound' => fragments?(compact, ['[q\log(q+1)]^{4/3}', '\lambda^{-1/3}H^{2/3}']),
    'physical_row' => fragments?(compact, ['\frac{a^2R^3}{2}v', '4\pi\delta_0a^2R^5H']),
    'exact_pde' => compact.scan('\partial_tF+B\partial_2F-\partial_2^2F=0').length == 1,
    'complete_square' => compact.scan('complete real square is').length == 1,
    'no_projection' => compact.scan('It does not apply to a Fourier projection of a larger field').length == 1
  },
  'source' => {
    'nazarov' => source_text.scan('https://www.mathnet.ru/eng/aa397').length == 1,
    'friedland_yomdin' => source_text.scan('https://arxiv.org/abs/1107.0039').length == 1,
    'erdelyi' => source_text.scan('https://people.tamu.edu/~terdelyi/papers-online/sbornik150R.pdf').length == 1,
    'theorem_number' => compact_source.scan('Theorem 2.7.1').length >= 1,
    'complex_scope' => compact_source.scan('complex temporal exponents').length >= 1,
    'adjacent_real' => source_text.scan('remez7.pdf').length == 1,
    'adjacent_shift' => source_text.scan('papers-online/SP.pdf').length == 1,
    'local_split' => compact_source.scan('local improvement from `exp(Cq log(q+1))` to `exp(Cq)`').length == 1,
    'source_table' => compact_source.scan('| centered stable tail E.13 |').length == 1,
    'no_new_theorem' => compact_source.scan('needs no new external theorem').length == 1,
    'no_novelty' => fragments?(compact_source, ['no literature completeness', 'novelty, priority, or sharpness']),
    'finite_not_proof' => compact_source.scan('Finite arithmetic may audit').length == 1,
    'primary_pass' => primary_text.scan('Current verdict: **PASS**').length == 1,
    'blocker_zero' => fragments?(primary_text, ['Mathematical blocker count: **0**', 'Release blocker count: **0**'])
  },
  'boundary' => {
    'exact_shear' => compact.scan('exact real constant-shear family').length >= 1,
    'one_band' => compact.scan('one dyadic band').length >= 1,
    'growing_constant' => compact.scan('not uniform in `q`').length == 1,
    'r075r_compatible' => fragments?(compact, ['R0.75R concerns an arbitrary growing packet', 'not contradicted']),
    'arbitrary_packets_open' => compact.scan('arbitrary packets').length >= 1,
    'version_m_conditional' => compact.scan('Version-M').length >= 2,
    'regularity_open' => compact.scan('regularity').length >= 1,
    'singularity_open' => compact.scan('singularity').length >= 1,
    'no_figure' => compact.scan('No simulation or formal scientific figure is claimed').length == 1,
    'no_simulation' => compact_primary.scan('No simulation or formal scientific figure is claimed').length == 1,
    'not_clay' => main_text.scan('**NOT CLAY.**').length == 1 && source_text.scan('**NOT CLAY.**').length == 1 && primary_text.scan('**NOT CLAY.**').length == 1,
    'sole_publisher' => compact_primary.scan('sole FIFO publisher').length == 1
  }
}

GROUPS.each { |group, names| abort "check inventory mismatch in #{group}" unless checks.fetch(group).keys == names }
checks.each_value { |group| group[MUTATION] = false if group.key?(MUTATION) } unless MUTATION.empty?
assertions = checks.values.sum(&:length)
passed = checks.values.sum { |group| group.values.count(true) }
verdict = passed == assertions ? 'PASS' : 'FAIL'
exact = {
  'geometry' => geometry, 'scaledCase' => scaled, 'spatialObservation' => space,
  'delayedSplit' => split, 'energy' => energy, 'scaleLedger' => scale
}
same_sections = exact.keys.count { |key| exact.fetch(key) == python_certificate.fetch('exact').fetch(key) }
python_inventory_same = NEGATIVE_MUTATIONS == python_certificate.fetch('negativeMutations')
python_total_same = assertions == python_certificate.fetch('assertionsTotal')

report = [
  '# R0.76E independent Ruby certificate audit', '',
  "- Verdict: **#{verdict}**",
  "- Ruby assertions: #{passed}/#{assertions}",
  "- Python/Ruby exact sections identical: #{same_sections == exact.length ? 'PASS' : 'FAIL'} (#{same_sections}/#{exact.length})",
  "- Python/Ruby mutation inventory identical: #{python_inventory_same ? 'PASS' : 'FAIL'} (#{NEGATIVE_MUTATIONS.length})",
  "- Python/Ruby assertion totals identical: #{python_total_same ? 'PASS' : 'FAIL'} (#{assertions})",
  '', '## Exact recomputation', '',
  "- Delayed split: `N=#{n_terms}`, `m=#{m_value}`, `S=#{sample_start}`, strict binary upper exponent `#{binary_exponent}`.",
  "- Carrier ledger: weighted `#{qstr(weighted_power)}`, endpoint `#{qstr(endpoint_lambda_power)}`.",
  "- Physical frozen rate: `#{scale['frozenRate']}`.",
  '', '## Boundary', '',
  'This independent implementation recomputes the six exact sections and every named assertion.',
  'Its finite arithmetic is not proof of Turan--Nazarov, Erdelyi, the analytic energy identity, or the continuum flux theorem.',
  'Arbitrary packets, Version-M extraction, regularity, and singularity remain open. **NOT CLAY.**', ''
].join("\n")
OUT.write(report)

all_pass = verdict == 'PASS' && same_sections == exact.length && python_inventory_same && python_total_same
puts JSON.generate({'suite' => 'r076e-linear-modal-entropy-window-ruby', 'verdict' => (all_pass ? 'PASS' : 'FAIL'), 'assertions' => assertions})
exit(all_pass ? 0 : 1)
