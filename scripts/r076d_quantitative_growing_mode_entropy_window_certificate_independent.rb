#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed exact-arithmetic audit for frozen R0.76D.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
STEM = 'r076d_quantitative_growing_mode_entropy_window'
MAIN = ROOT.join("research/#{STEM}.md")
PRIMARY = ROOT.join("research/#{STEM}_primary_audit.md")
SOURCE = ROOT.join('research/r076d_report-source.md')
FIXTURES = ROOT.join("scripts/#{STEM}_fixtures.json")
EXPECTED = ROOT.join("scripts/#{STEM}_expected.json")
CERTIFICATE = Pathname.new(ENV.fetch('R076D_JSON', ROOT.join("research/#{STEM}_certificate.json").to_s))
OUT = Pathname.new(ENV.fetch('R076D_RUBY_REPORT', ROOT.join("research/#{STEM}_independent_audit.md").to_s))
MUTATION = ENV.fetch('R076D_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => 'cd94e3384f01963cb7b8a14fdb8376c6197c361473447f15500db0acac5e958e',
  "research/#{STEM}_primary_audit.md" => '9b99247ceb34cadc12c7f4f0858be642316ca80d1ff83d05dfd745a9906356d8',
  'research/r076d_report-source.md' => 'f2358780d382dcace69b7ebef855bf3c8e63d15b581dc86b62b7e3c751fbd310',
  'research/r076c_full_frequency_fixed_mode_flux_payment.md' => '2b2f4a2b353645e72ca54bfc06495a9f52329498b9c16a9e451ca7b3456f6bbf',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075b_bulk_clock_outer_padding_gate.md' => '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a'
}.freeze
FIXTURES_SHA256 = 'ffe5c2b9a1a6b0c20b710dc45fcac9543069ea6af38dce34804665012984b374'
EXPECTED_SHA256 = 'eb5dd9ebaa6a74cbc7f999fdbd55ee54a50588342c3dfba9412ac53c935ba2dd'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash c_hash r_hash clock_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema expected_schema],
  'integrity' => %w[utf8 controls no_cr no_trailing tags display_opens display_closes references tex_qquad tex_frac],
  'geometry' => %w[delta_order support_radius support_bound plateau_length plateau_bound],
  'scaled' => %w[positive_q integer_modes ordered_modes dyadic_band ell kappas alpha n1r lambda clock_t clock_mass velocity real_band],
  'space' => %w[term_count turan_power chebyshev length_ratio map_scale original_frequency rescaled_frequency bernstein_rational bernstein_e returned_rational returned_e interval_containment gap_free],
  'heat' => %w[heat_terms m factorial_argument factorial factorial_over_four center_shift shifted_lower shifted_upper net_decay heat_endpoint_power endpoint_comparison tail_formula endpoint_formula family_hypothesis imaginary_free],
  'energy' => %w[gradient_lambda q_squared gradient_coefficient gradient_inequality onset weighted_power energy_endpoint_power bounded_branch high_branch endpoint_cancel q_absorption speed_zero],
  'scale' => %w[flux_prefactor mass_prefactor target normalized r_cancel frozen_rate entropy_window limsup_rate],
  'proof' => %w[main_bound normalized_bound spatial_lemma heat_lemma bounded_trace heat_clock energy_identity physical_row exact_pde complete_square no_sign_route no_projection],
  'source' => %w[nazarov friedland_yomdin erdelyi theorem_number complex_coefficients source_space source_heat source_flux source_rate local_deductions no_novelty finite_not_proof primary_pass math_zero release_zero],
  'boundary' => %w[exact_shear one_band growing_constant r075r_compatible arbitrary_packets_open version_m_conditional regularity_open singularity_open no_figure not_clay]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

def digest(path)
  Digest::SHA256.file(path).hexdigest
end

def clean?(raw)
  raw.dup.force_encoding(Encoding::UTF_8).valid_encoding? &&
    raw.bytes.none? { |byte| (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127 }
end

def flat(value)
  value.gsub(/\s+/, ' ')
end

def qstr(value)
  value.denominator == 1 ? value.numerator.to_s : "#{value.numerator}/#{value.denominator}"
end

def encoded(values)
  values.transform_values { |value| value.denominator == 1 ? value.numerator : qstr(value) }
end

def fragments?(text, fragments)
  fragments.all? { |fragment| text.include?(fragment) }
end

abort "unknown R076D_RUBY_MUTATION: #{MUTATION}" if !MUTATION.empty? && !NEGATIVE_MUTATIONS.include?(MUTATION)
abort 'duplicate mutation name in R0.76D Ruby suite' unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

main_raw = MAIN.binread
primary_raw = PRIMARY.binread
source_raw = SOURCE.binread
main_text = main_raw.force_encoding(Encoding::UTF_8)
primary_text = primary_raw.force_encoding(Encoding::UTF_8)
source_text = source_raw.force_encoding(Encoding::UTF_8)
compact = flat(main_text)
compact_primary = flat(primary_text)
compact_source = flat(source_text)
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_certificate = JSON.parse(CERTIFICATE.read)
bindings = FROZEN.sort.to_h do |path, expected_hash|
  [path, { 'expectedSha256' => expected_hash, 'observedSha256' => digest(ROOT.join(path)) }]
end

delta0 = Rational(fixtures.dig('profile', 'delta0'))
delta = Rational(fixtures.dig('profile', 'delta'))
q_count = fixtures.dig('scaledCase', 'q').to_i
a_value = Rational(fixtures.dig('scaledCase', 'a'))
radius = Rational(fixtures.dig('scaledCase', 'R'))
b_shear = Rational(fixtures.dig('scaledCase', 'B'))
modes = fixtures.dig('scaledCase', 'frequencies').map { |value| Rational(value) }
ell = a_value * radius
kappas = modes.map { |mode| mode * ell }
alpha = kappas.first
n1r = modes.first * radius
lambda_value = (alpha / a_value)**2
clock_end = Rational(fixtures.dig('clock', 'scaledClockEnd'))
temporal_end = clock_end * lambda_value
velocity = b_shear * radius / a_value
real_magnitudes = kappas.map { |kappa| (kappa / alpha)**2 }
geometry = {
  'supportRadius' => qstr(1 + delta / a_value),
  'supportWithinThreeHalves' => 1 + delta / a_value <= Rational(3, 2),
  'centralPlateauLength' => qstr(2 - 2 * delta / a_value),
  'centralPlateauAtLeastOne' => 2 - 2 * delta / a_value >= 1
}
scaled = {
  'ell' => qstr(ell), 'kappas' => kappas.map { |value| qstr(value) }, 'alpha' => qstr(alpha),
  'n1R' => qstr(n1r), 'lambda' => qstr(lambda_value), 'T' => qstr(temporal_end),
  'KOverH' => qstr(lambda_value), 'dyadicBand' => modes.last <= 2 * modes.first,
  'v' => qstr(velocity),
  'realPartsWithinMinusFourMinusOne' => real_magnitudes.min >= 1 && real_magnitudes.max <= 4
}

maximum_terms = 2 * q_count
local_scale = Rational(fixtures.dig('spatialObservation', 'localMapScale'))
maximum_original_frequency = 2 * alpha
maximum_rescaled_frequency = local_scale * maximum_original_frequency
space = {
  'maximumTerms' => maximum_terms,
  'turanExponent' => maximum_terms - 1,
  'lengthRatio' => qstr(Rational(fixtures.dig('spatialObservation', 'jPlusLength')) /
                         Rational(fixtures.dig('spatialObservation', 'chebyshevMeasureLower'))),
  'maximumOriginalFrequency' => qstr(maximum_original_frequency),
  'maximumRescaledFrequency' => qstr(maximum_rescaled_frequency),
  'bernsteinConstantRationalPart' => qstr(alpha),
  'bernsteinConstantEMultiplier' => qstr(2 * (maximum_terms + 1)),
  'returnedDerivativeRationalPart' => qstr(2 * alpha),
  'returnedDerivativeEMultiplier' => qstr(4 * (maximum_terms + 1))
}

n_terms = fixtures.dig('heatTail', 'maximumTerms').to_i
m_value = 2 * (n_terms - 1)
factorial_arg = m_value + 1
factorial = (1..factorial_arg).reduce(1, :*)
shift = Rational(fixtures.dig('heatTail', 'centerShift'))
shifted_lower = -4 + shift
shifted_upper = -1 + shift
endpoint_r = Rational(m_value) + Rational(2, 3)
heat = {
  'maximumTerms' => n_terms, 'm' => m_value, 'factorialArgument' => factorial_arg,
  'factorial' => factorial, 'factorialOverFour' => factorial / 4,
  'endpointPower' => qstr(endpoint_r), 'endpointComparisonPower' => m_value,
  'shiftedRealLower' => qstr(shifted_lower), 'shiftedRealUpper' => qstr(shifted_upper),
  'netDecay' => qstr(-shift + [shifted_lower.abs, shifted_upper.abs].max)
}

ledger = fixtures['lambdaLedger']
weighted_power = Rational(ledger.dig('gradientPrefactor', 'lambda')) +
                 Rational(ledger.dig('changeOfClock', 'sPerTau', 'lambda')) +
                 Rational(ledger.dig('changeOfClock', 'dsPerDtau', 'lambda')) +
                 Rational(ledger.dig('weightedTail', 'K')) * Rational(ledger.dig('clockMass', 'KPerH', 'lambda'))
endpoint_lambda_power = Rational(ledger.dig('endpointTail', 'T')) +
                        Rational(ledger.dig('endpointTail', 'K')) * Rational(ledger.dig('clockMass', 'KPerH', 'lambda'))
q_squared = Rational(q_count * q_count, a_value.to_i * a_value.to_i)
energy = {
  'lambda' => qstr(lambda_value), 'qSquaredOverASquared' => qstr(q_squared),
  'gradientCoefficient' => qstr(lambda_value + q_squared),
  'weightedLambdaPower' => qstr(weighted_power), 'endpointLambdaPower' => qstr(endpoint_lambda_power)
}
scale = {
  'fluxPrefactor' => encoded('a' => Rational(2), 'R' => Rational(3), 'v' => Rational(1)),
  'massPrefactor' => encoded('a' => Rational(2), 'R' => Rational(5), 'H' => Rational(1)),
  'afterMass' => encoded('a' => Rational(2, 3), 'R' => Rational(-1, 3), 'M' => Rational(2, 3)),
  'normalized' => encoded('a' => Rational(2, 3), 'R' => Rational(0), 'omega' => Rational(1, 3), 'p' => Rational(2, 3)),
  'frozenRate' => qstr(-Rational(fixtures.dig('frozenScales', 'cGamma')) / 12)
}

tags = main_text.scan(/\\tag\{D\.(\d+)\}/).flatten.map(&:to_i)
refs = main_text.scan(/(?<![A-Za-z0-9_.])D\.(\d+)/).flatten.map(&:to_i)
checks = {
  'bindings' => {
    'main_hash' => bindings.fetch("research/#{STEM}.md").values.uniq.length == 1,
    'primary_hash' => bindings.fetch("research/#{STEM}_primary_audit.md").values.uniq.length == 1,
    'source_hash' => bindings.fetch('research/r076d_report-source.md').values.uniq.length == 1,
    'c_hash' => bindings.fetch('research/r076c_full_frequency_fixed_mode_flux_payment.md').values.uniq.length == 1,
    'r_hash' => bindings.fetch('research/r075r_outer_cap_spectral_concentration_obstruction.md').values.uniq.length == 1,
    'clock_hash' => bindings.fetch('research/r075b_bulk_clock_outer_padding_gate.md').values.uniq.length == 1
  },
  'inputs' => {
    'fixture_hash' => digest(FIXTURES) == FIXTURES_SHA256, 'expected_hash' => digest(EXPECTED) == EXPECTED_SHA256,
    'fixture_schema' => fixtures['schema'] == 'r076d-quantitative-growing-mode-entropy-window-fixtures-v1',
    'expected_schema' => expected['schema'] == 'r076d-quantitative-growing-mode-entropy-window-expected-v1'
  },
  'integrity' => {
    'utf8' => [main_raw, primary_raw, source_raw].all? { |raw| clean?(raw) }, 'controls' => clean?(main_raw),
    'no_cr' => !main_raw.include?("\r"),
    'no_trailing' => main_text.lines.all? { |line| line.chomp !~ /[ \t]$/ },
    'tags' => tags == (1..41).to_a, 'display_opens' => main_text.scan(/^\\\[$/).length == 41,
    'display_closes' => main_text.scan(/^\\\]$/).length == 41, 'references' => (refs.uniq - tags.uniq).empty?,
    'tex_qquad' => main_text !~ /(?<!\\)\bqquad\b/, 'tex_frac' => main_text !~ /(?<!\\)\bfrac\{/
  },
  'geometry' => {
    'delta_order' => 0 < delta0 && delta0 < delta,
    'support_radius' => geometry['supportRadius'] == expected.dig('geometry', 'supportRadius'),
    'support_bound' => geometry['supportWithinThreeHalves'] == expected.dig('geometry', 'supportWithinThreeHalves'),
    'plateau_length' => geometry['centralPlateauLength'] == expected.dig('geometry', 'centralPlateauLength'),
    'plateau_bound' => geometry['centralPlateauAtLeastOne'] == expected.dig('geometry', 'centralPlateauAtLeastOne')
  },
  'scaled' => {
    'positive_q' => q_count >= 1, 'integer_modes' => modes.all? { |value| value.denominator == 1 && value >= 1 },
    'ordered_modes' => modes == modes.uniq.sort, 'dyadic_band' => scaled['dyadicBand'] == expected.dig('scaledCase', 'dyadicBand'),
    'ell' => scaled['ell'] == expected.dig('scaledCase', 'ell'), 'kappas' => scaled['kappas'] == expected.dig('scaledCase', 'kappas'),
    'alpha' => scaled['alpha'] == expected.dig('scaledCase', 'alpha'), 'n1r' => scaled['n1R'] == expected.dig('scaledCase', 'n1R'),
    'lambda' => scaled['lambda'] == expected.dig('scaledCase', 'lambda') && lambda_value == n1r**2,
    'clock_t' => scaled['T'] == expected.dig('scaledCase', 'T'), 'clock_mass' => scaled['KOverH'] == expected.dig('scaledCase', 'KOverH'),
    'velocity' => scaled['v'] == expected.dig('scaledCase', 'v'),
    'real_band' => scaled['realPartsWithinMinusFourMinusOne'] == expected.dig('scaledCase', 'realPartsWithinMinusFourMinusOne')
  },
  'space' => {
    'term_count' => space['maximumTerms'] == expected.dig('spatialObservation', 'maximumTerms'),
    'turan_power' => space['turanExponent'] == expected.dig('spatialObservation', 'turanExponent'),
    'chebyshev' => Rational(fixtures.dig('spatialObservation', 'chebyshevMeasureLower')) == Rational(1, 2),
    'length_ratio' => space['lengthRatio'] == expected.dig('spatialObservation', 'lengthRatio'), 'map_scale' => local_scale == Rational(1, 2),
    'original_frequency' => space['maximumOriginalFrequency'] == expected.dig('spatialObservation', 'maximumOriginalFrequency'),
    'rescaled_frequency' => space['maximumRescaledFrequency'] == expected.dig('spatialObservation', 'maximumRescaledFrequency'),
    'bernstein_rational' => space['bernsteinConstantRationalPart'] == expected.dig('spatialObservation', 'bernsteinConstantRationalPart'),
    'bernstein_e' => space['bernsteinConstantEMultiplier'] == expected.dig('spatialObservation', 'bernsteinConstantEMultiplier'),
    'returned_rational' => space['returnedDerivativeRationalPart'] == expected.dig('spatialObservation', 'returnedDerivativeRationalPart'),
    'returned_e' => space['returnedDerivativeEMultiplier'] == expected.dig('spatialObservation', 'returnedDerivativeEMultiplier'),
    'interval_containment' => fragments?(compact, ['For `z_0 in J`', 'observation interval is contained in `J^+`']),
    'gap_free' => fragments?(compact, ['There is no dependence on the size or separation', 'Imaginary parts and exponent gaps never enter'])
  },
  'heat' => {
    'heat_terms' => heat['maximumTerms'] == expected.dig('heatTail', 'maximumTerms'), 'm' => heat['m'] == expected.dig('heatTail', 'm'),
    'factorial_argument' => heat['factorialArgument'] == expected.dig('heatTail', 'factorialArgument'),
    'factorial' => heat['factorial'] == expected.dig('heatTail', 'factorial'),
    'factorial_over_four' => heat['factorialOverFour'] == expected.dig('heatTail', 'factorialOverFour'),
    'center_shift' => shift == Rational(5, 2), 'shifted_lower' => heat['shiftedRealLower'] == expected.dig('heatTail', 'shiftedRealLower'),
    'shifted_upper' => heat['shiftedRealUpper'] == expected.dig('heatTail', 'shiftedRealUpper'),
    'net_decay' => heat['netDecay'] == expected.dig('heatTail', 'netDecay'),
    'heat_endpoint_power' => heat['endpointPower'] == expected.dig('heatTail', 'endpointPower'),
    'endpoint_comparison' => Rational(fixtures.dig('heatTail', 'endpointComparison')) == Rational(5, 4) && heat['endpointComparisonPower'] == expected.dig('heatTail', 'endpointComparisonPower'),
    'tail_formula' => fragments?(compact, ['m=2(N-1)', '\\frac{(m+1)!}{4}']),
    'endpoint_formula' => fragments?(compact, ['\\left(\\frac54\\right)^m', 'T^{2/3}(1+T)^me^{-2T}']),
    'family_hypothesis' => compact.scan('every `Q(.;z)` satisfying D.20').length == 1,
    'imaginary_free' => compact.scan('Imaginary parts and exponent gaps never enter').length == 1
  },
  'energy' => {
    'gradient_lambda' => energy['lambda'] == expected.dig('energy', 'lambda'),
    'q_squared' => energy['qSquaredOverASquared'] == expected.dig('energy', 'qSquaredOverASquared'),
    'gradient_coefficient' => energy['gradientCoefficient'] == expected.dig('energy', 'gradientCoefficient'),
    'gradient_inequality' => compact_primary.scan('a^(-2)(alpha+q)^2 <= C(lambda+q^2/a^2)').length == 1,
    'onset' => compact.scan('0\\le\\zeta(s)\\le C_\\eta s').length == 1,
    'weighted_power' => energy['weightedLambdaPower'] == expected.dig('energy', 'weightedLambdaPower'),
    'energy_endpoint_power' => energy['endpointLambdaPower'] == expected.dig('energy', 'endpointLambdaPower'),
    'bounded_branch' => compact.scan('When `lambda<=1`').length == 1, 'high_branch' => compact.scan('When `lambda>1`').length == 1,
    'endpoint_cancel' => fragments?(compact_primary, ['T^(-2/3)K_T^(2/3)', 'cancel exactly']),
    'q_absorption' => compact.scan('polynomial factor is absorbed').length == 1,
    'speed_zero' => compact_primary.scan('`B=0` is covered').length == 1
  },
  'scale' => {
    'flux_prefactor' => scale['fluxPrefactor'] == expected.dig('scaleLedger', 'fluxPrefactor'),
    'mass_prefactor' => scale['massPrefactor'] == expected.dig('scaleLedger', 'massPrefactor'),
    'target' => scale['afterMass'] == expected.dig('scaleLedger', 'afterMass'),
    'normalized' => scale['normalized'] == expected.dig('scaleLedger', 'normalized'), 'r_cancel' => scale.dig('normalized', 'R') == 0,
    'frozen_rate' => scale['frozenRate'] == expected.dig('scaleLedger', 'frozenRate'),
    'entropy_window' => compact.scan('q(L)\\log(q(L)+1)=o(L^2)').length >= 1,
    'limsup_rate' => compact.scan('-\\frac2{11907}').length >= 2
  },
  'proof' => {
    'main_bound' => fragments?(compact, ['|\\mathcal T_{\\boldsymbol n,R}|', '\\exp\\!\\bigl(C_*q\\log(q+1)\\bigr)', 'a^{2/3}R^{-1/3}']),
    'normalized_bound' => fragments?(compact, ['\\mathfrak X_{\\boldsymbol n,R}', 'a^{2/3}\\omega^{1/3}']),
    'spatial_lemma' => fragments?(compact, ['**Lemma D.1.**', "(\\alpha+q)^{-1}\\|g'\\|_{L^\\infty(J)}"]),
    'heat_lemma' => fragments?(compact, ['**Lemma D.2.**', '\\int_0^T\\tau k(\\tau)^{2/3}d\\tau']),
    'bounded_trace' => fragments?(compact, ['h(4)\\le D^{6q}H', 'h(4)^{2/3}\\le D^{4q}H^{2/3}']),
    'heat_clock' => fragments?(compact, ['\\tau=\\lambda s', 'K_T=lambda H']),
    'energy_identity' => fragments?(compact, ['exact real-square identity', '2a^{-2}\\int_0^4\\zeta\\int\\Xi_a|G_z|^2']),
    'physical_row' => fragments?(compact, ['\\frac{a^2R^3}{2}v', '4\\pi\\delta_0a^2R^5H']),
    'exact_pde' => compact.scan('\\partial_tF+B\\partial_2F-\\partial_2^2F=0').length == 1,
    'complete_square' => compact.scan('complete real square before absolute values').length == 1,
    'no_sign_route' => fragments?(compact, ['No analytic-density split', 'localized-current sign', 'standalone carrier integration by parts']),
    'no_projection' => compact.scan('cannot be applied merely to a Fourier projection').length == 1
  },
  'source' => {
    'nazarov' => source_text.include?('https://www.mathnet.ru/eng/aa397'),
    'friedland_yomdin' => source_text.include?('https://arxiv.org/abs/1107.0039'),
    'erdelyi' => source_text.include?('https://people.tamu.edu/~terdelyi/papers-online/sbornik150R.pdf'),
    'theorem_number' => compact_source.scan('Theorem 2.7.1').length >= 1, 'complex_coefficients' => source_text.include?('a_j in C'),
    'source_space' => source_text.include?('D.17, D.21, and D.27'), 'source_heat' => source_text.include?('D.21--D.26'),
    'source_flux' => source_text.include?('D.32--D.39 together with D.5'), 'source_rate' => source_text.include?('D.40 and frozen value'),
    'local_deductions' => compact_source.scan('Everything after those two inputs').length == 1,
    'no_novelty' => fragments?(compact_source, ['not evidence of novelty or priority', 'no completeness, novelty, priority, or sharpness claim']),
    'finite_not_proof' => compact_source.scan('Finite arithmetic may audit').length == 1,
    'primary_pass' => primary_text.include?('Current verdict: **PASS**'),
    'math_zero' => primary_text.include?('Mathematical blocker count: **0**'),
    'release_zero' => primary_text.include?('Release blocker count: **0**')
  },
  'boundary' => {
    'exact_shear' => compact.scan('exact constant-shear family').length >= 1, 'one_band' => compact.scan('one dyadic band').length >= 1,
    'growing_constant' => compact.scan('constant grows with `q`').length == 1,
    'r075r_compatible' => compact.scan('R0.75R already rules out').length == 1,
    'arbitrary_packets_open' => compact.scan('arbitrary packets').length >= 1,
    'version_m_conditional' => compact.scan('Version-M').length >= 2,
    'regularity_open' => compact.scan('regularity').length >= 1, 'singularity_open' => compact.scan('singularity').length >= 1,
    'no_figure' => compact.scan('No formal scientific figure or simulation is claimed').length == 1,
    'not_clay' => main_text.include?('**NOT CLAY.**') && source_text.include?('**NOT CLAY.**') && primary_text.include?('**NOT CLAY.**')
  }
}

GROUPS.each do |group, names|
  abort "check inventory mismatch in #{group}" unless checks.fetch(group).keys == names
end
checks.each_value { |group| group[MUTATION] = false if group.key?(MUTATION) } unless MUTATION.empty?
assertions = checks.values.sum(&:length)
passed = checks.values.sum { |group| group.values.count(true) }
verdict = passed == assertions ? 'PASS' : 'FAIL'
exact = {
  'geometry' => geometry, 'scaledCase' => scaled, 'spatialObservation' => space,
  'heatTail' => heat, 'energy' => energy, 'scaleLedger' => scale
}
same_sections = exact.keys.count { |key| exact.fetch(key) == python_certificate.fetch('exact').fetch(key) }

lines = [
  '# R0.76D independent exact audit', '', "- Verdict: **#{verdict}**.",
  "- Ruby assertions: #{passed}/#{assertions}.",
  "- Python/Ruby exact sections identical: #{same_sections == exact.length ? 'PASS' : 'FAIL'} (#{same_sections}/#{exact.length}).",
  "- Named negative mutations: #{NEGATIVE_MUTATIONS.length}.",
  '- Independent arithmetic: geometry, carrier scaling, derivative constants, factorial tail, lambda powers, and physical exponents.',
  '- Continuum boundary: this computation is not proof of Turan--Nazarov, Erdelyi, or the analytic flux estimate.',
  '', 'The fixture independently returns 11!/4=9,979,200, gradient coefficient',
  '257/64, weighted exponent -1/3, endpoint exponent 0, and rate -2/11907.',
  'The mathematical and source audits report zero blockers. **NOT CLAY.**', ''
]
OUT.write(lines.join("\n"))
puts JSON.generate('suite' => 'r076d-independent', 'status' => verdict, 'assertions' => assertions,
                   'exactSections' => same_sections)
exit(verdict == 'PASS' && same_sections == exact.length ? 0 : 1)
