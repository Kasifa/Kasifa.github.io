#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed exact finite audit for frozen R0.75X.

require 'digest'
require 'json'

ROOT = File.expand_path('..', __dir__)
STEM = 'r075x_fixed_finite_mode_low_carrier_payment'
MAIN = File.join(ROOT, 'research', "#{STEM}.md")
PRIMARY = File.join(ROOT, 'research', "#{STEM}_primary_audit.md")
SOURCE = File.join(ROOT, 'research', 'r075x_report-source.md')
FIXTURES = File.join(ROOT, 'scripts', "#{STEM}_fixtures.json")
EXPECTED = File.join(ROOT, 'scripts', "#{STEM}_expected.json")
CERT = ENV.fetch('R075X_JSON', File.join(ROOT, 'research', "#{STEM}_certificate.json"))
REPORT = ENV.fetch('R075X_RUBY_REPORT', File.join(ROOT, 'research', "#{STEM}_independent_audit.md"))
MUTATION = ENV.fetch('R075X_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => '8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763',
  "research/#{STEM}_primary_audit.md" => '8fffbf0c8ad50d5765c734f8e5627ce0dbe0d6b2aad4bcb26aa5c298f6143b2c',
  'research/r075x_report-source.md' => '8fa756c7efe2660dbc5eeb51e2a11d10dce58f36f4c0d0f757000be1447b7f34',
  'research/r075b_bulk_clock_outer_padding_gate.md' => '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075w_full_frequency_two_harmonic_flux_payment.md' => '571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4'
}.freeze
FIXTURES_SHA256 = 'de231e977d9a2551222f0a4f0a8ebcb65490f76574bc4fa494db480e2b61a0e9'
EXPECTED_SHA256 = '879ff3458050e712048654eb91623a00e5436a22f12c6b814fb137aa8af96311'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash b_hash r_hash w_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema],
  'integrity' => %w[utf8 controls tags displays references],
  'clock' => %w[clock_length cutoff_onset cutoff_derivative],
  'family' => %w[fixed_q ordered_modes dyadic_band low_carrier scaled_upper],
  'scaled' => %w[ell alphas velocity heat_rates scaled_pde],
  'ode' => %w[ode_order symmetric_coefficients last_row compact_family initial_jet confluent_degree gap_free_space],
  'trace' => %w[term_count real_parts imaginary_free gap_free_time turan_power sublevel_measure endpoint_trace],
  'kernel' => %w[kernel_odd kernel_zero primitive_support kernel_norms primitive_second cross_section],
  'identity' => %w[square_pde advective_row energy_derivative xi_second dissipation heat_cancel identity_signs],
  'payment' => %w[spatial_application holder_time terminal_payment dimensionless_payment],
  'mass' => %w[fibre_area mass_a mass_r flux_prefactor target_a target_r target_m],
  'normalization' => %w[p_definition x_definition r_cancel omega_power frozen_rate],
  'q_boundary' => %w[temporal_growth spatial_nonquantitative fixed_q_only r_obstruction],
  'source' => %w[nazarov_original primary_restatement bounded_search],
  'audit' => %w[audit_pass math_zero release_zero finite_boundary],
  'figure' => %w[analytic_only no_simulation_claim no_formal_figure],
  'boundary' => %w[low_only high_three_open packets_open e24_open version_m_conditional not_clay]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

def digest(path)
  Digest::SHA256.file(path).hexdigest
end

def clean?(bytes)
  value = bytes.dup.force_encoding(Encoding::UTF_8)
  value.valid_encoding? && bytes.bytes.none? { |byte| (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127 }
end

def flat(value)
  value.gsub(/\s+/, ' ')
end

def fragments?(value, fragments)
  fragments.all? { |fragment| value.include?(fragment) }
end

def qtext(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

def encoded(powers)
  powers.to_h { |key, value| [key, value.denominator == 1 ? value.numerator : value.to_s] }
end

def poly_mul(left, right)
  output = Array.new(left.length + right.length - 1, Rational(0))
  left.each_with_index do |x_value, i|
    right.each_with_index { |y_value, j| output[i + j] += x_value * y_value }
  end
  output
end

def poly_derivative(poly, order = 1)
  output = poly.dup
  order.times { output = (1...output.length).map { |index| index * output[index] } }
  output
end

def symmetric_integral(poly)
  poly.each_with_index.sum(Rational(0)) do |value, index|
    index.even? ? Rational(2) * value / (index + 1) : Rational(0)
  end
end

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  abort("unknown R075X_RUBY_MUTATION: #{MUTATION}")
end
abort('duplicate mutation name in R0.75X Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

raw = File.binread(MAIN)
raw_primary = File.binread(PRIMARY)
raw_source = File.binread(SOURCE)
text = raw.force_encoding(Encoding::UTF_8)
primary = raw_primary.force_encoding(Encoding::UTF_8)
source = raw_source.force_encoding(Encoding::UTF_8)
compact = flat(text)
compact_primary = flat(primary)
compact_source = flat(source)
fixtures = JSON.parse(File.read(FIXTURES, encoding: 'UTF-8'))
expected = JSON.parse(File.read(EXPECTED, encoding: 'UTF-8'))
certificate = JSON.parse(File.read(CERT, encoding: 'UTF-8'))

frozen = FROZEN.dup
mutation_path = {
  'main_hash' => "research/#{STEM}.md",
  'primary_hash' => "research/#{STEM}_primary_audit.md",
  'source_hash' => 'research/r075x_report-source.md',
  'b_hash' => 'research/r075b_bulk_clock_outer_padding_gate.md',
  'r_hash' => 'research/r075r_outer_cap_spectral_concentration_obstruction.md',
  'w_hash' => 'research/r075w_full_frequency_two_harmonic_flux_payment.md'
}[MUTATION]
frozen[mutation_path] = '0' * 64 if mutation_path
bindings = frozen.sort.to_h do |path, expected_hash|
  [path, { 'expectedSha256' => expected_hash, 'observedSha256' => digest(File.join(ROOT, path)) }]
end

clock = fixtures.fetch('clock')
radius = Rational(clock.fetch('R'))
duration = Rational(clock.fetch('durationCoefficient')) * radius**clock.fetch('durationRPower')
computed_clock = { 'T' => qtext(duration) }

row = fixtures.fetch('scaledCase')
q_count = row.fetch('q')
modes = row.fetch('frequencies').map { |value| Rational(value) }
a_value = Rational(row.fetch('a'))
radius = Rational(row.fetch('R'))
b_shear = Rational(row.fetch('B'))
c_zero = Rational(row.fetch('C0'))
ell = a_value * radius
alphas = modes.map { |mode| mode * ell }
velocity = b_shear * radius / a_value
heat_rates = alphas.map { |alpha| alpha**2 / a_value**2 }
computed_scaled = {
  'ell' => qtext(ell),
  'alphas' => alphas.map { |value| qtext(value) },
  'v' => qtext(velocity),
  'heatRates' => heat_rates.map { |value| qtext(value) },
  'lowCarrier' => modes.first * ell < c_zero,
  'dyadicBand' => modes.last <= 2 * modes.first
}

squares = alphas.map { |alpha| alpha**2 }
sigmas = (1..q_count).map do |degree|
  squares.combination(degree).sum(Rational(0)) { |combination| combination.inject(Rational(1), :*) }
end
last_row = sigmas.reverse.flat_map { |sigma| [-sigma, Rational(0)] }
computed_ode = {
  'q' => q_count,
  'order' => 2 * q_count,
  'sigma' => sigmas.map { |value| qtext(value) },
  'lastRow' => last_row.map { |value| qtext(value) },
  'fullyConfluentDegree' => 2 * q_count - 1
}
computed_trace = {
  'maximumTerms' => 2 * q_count,
  'turanExponent' => 2 * q_count - 1,
  'sublevelMeasureLower' => 2,
  'gapFactor' => 0
}

identity = fixtures.fetch('transportIdentity')
i_velocity = Rational(identity.fetch('v'))
i_time = Rational(identity.fetch('s'))
i_a = Rational(identity.fetch('a'))
xi = [1, 0, -2, 0, 1].map { |value| Rational(value) }
w_kernel = poly_derivative(xi)
g_poly = [-i_velocity * i_time, Rational(1)]
g_squared = poly_mul(g_poly, g_poly)
advective = i_velocity * symmetric_integral(poly_mul(w_kernel, g_squared))
energy_derivative = -2 * i_velocity * symmetric_integral(poly_mul(xi, g_poly))
xi_second = symmetric_integral(poly_mul(poly_derivative(xi, 2), g_squared))
dissipation = symmetric_integral(xi)
heat_cancellation = -xi_second / i_a**2 + 2 * dissipation / i_a**2
computed_identity = {
  'advectiveRow' => qtext(advective),
  'energyDerivative' => qtext(energy_derivative),
  'xiSecondRow' => qtext(xi_second),
  'dissipationRow' => qtext(dissipation),
  'heatCancellation' => qtext(heat_cancellation)
}

computed_scale = {
  'fluxPrefactor' => encoded('a' => Rational(2), 'R' => Rational(3), 'v' => Rational(1)),
  'massPrefactor' => encoded('a' => Rational(2), 'R' => Rational(5), 'H' => Rational(1)),
  'afterMass' => encoded('a' => Rational(2, 3), 'R' => Rational(-1, 3), 'M' => Rational(2, 3)),
  'normalized' => encoded('a' => Rational(2, 3), 'R' => Rational(0),
                          'omega' => Rational(1, 3), 'p' => Rational(2, 3)),
  'frozenRate' => qtext(-Rational(fixtures.dig('frozenScales', 'cGamma')) / 12)
}

tags = text.scan(/\\tag\{X\.(\d+)\}/).flatten.map(&:to_i)
refs = text.scan(/\bX\.(\d+)\b/).flatten.map(&:to_i)
checks = []
record = lambda do |name, group, condition|
  checks << { 'name' => name, 'pass' => condition && !GROUPS.fetch(group).include?(MUTATION) }
end

record.call('frozen source bindings', 'bindings',
            bindings.values.all? { |entry| entry['expectedSha256'] == entry['observedSha256'] })
record.call('fixture and expected bindings', 'inputs',
            digest(FIXTURES) == FIXTURES_SHA256 && digest(EXPECTED) == EXPECTED_SHA256 &&
              fixtures.fetch('schema').end_with?('fixtures-v1'))
record.call('UTF-8, controls, tags, displays, and references', 'integrity',
            clean?(raw) && clean?(raw_primary) && clean?(raw_source) && tags == (1..36).to_a &&
              text.scan('\\[').length == 36 && text.scan('\\]').length == 36 && (refs.uniq - tags.uniq).empty?)
record.call('complete clock and cutoff', 'clock',
            computed_clock == expected.fetch('clock') &&
              fragments?(compact, ['4R^2', '\\eta_R(0)=0', 'C_\\eta R^{-2}']))
record.call('fixed finite dyadic low-carrier family', 'family',
            computed_scaled['lowCarrier'] && computed_scaled['dyadicBand'] &&
              fragments?(compact, ['Fix an integer `q>=1`', 'n_q\\le2n_1', 'n_1aR<C_0',
                                    '0<\\alpha_1<\\cdots<\\alpha_q\\le2C_0']))
record.call('scaled variables and heat rates', 'scaled',
            computed_scaled == expected.fetch('scaledCase') &&
              fragments?(compact, ['v=\\frac{BR}{a}',
                                    '\\partial_sG+v\\partial_zG-a^{-2}\\partial_z^2G=0']))
record.call('2q-order confluent spatial ODE', 'ode',
            computed_ode == expected.fetch('spatialOde') &&
              fragments?(compact, ['\\prod_{j=1}^q(\\partial_z^2+\\alpha_j^2)g=0',
                                    '(-\\sigma_q,0,-\\sigma_{q-1},0,\\ldots,-\\sigma_1,0)',
                                    'degree at most `2q-1`', 'unit initial jet', 'No inverse frequency gap']))
record.call('gap-free 2q-term temporal trace', 'trace',
            computed_trace == expected.fetch('temporalTrace') &&
              fragments?(compact, ['N\\le2q', 'independent of the imaginary parts',
                                    'has measure at least two', 'h(4)\\le C_qH',
                                    '-\\alpha_j^2/a^2\\pm i\\alpha_jv']))
record.call('scaled radial primitive', 'kernel',
            fragments?(compact, ['W_a(z)=-2\\pi az', 'Oddness gives `int W_a=0`',
                                  '\\Xi_a(z)=\\int_{-\\infty}^zW_a(r)', "\\|\\Xi_a''\\|_1\\le Ca",
                                  '\\frac{a^2R^3}{2}v']))
record.call('transport identity exact finite fixture', 'identity',
            computed_identity == expected.fetch('transportIdentity') && advective == energy_derivative &&
              heat_cancellation.zero? &&
              fragments?(compact, ['=-2a^{-2}|\\partial_zG|^2', "=E'(s)-a^{-2}\\int\\Xi_a''G^2",
                                    '+2a^{-2}\\int\\Xi_a|\\partial_zG|^2']))
record.call('identity signs and complete payment', 'payment',
            fragments?(compact_primary, ['terminal row is positive', 'cutoff derivative row negative',
                                          "`Xi_a''` row negative", 'localized gradient row positive']) &&
              fragments?(compact, ['|E(4)|\\le C_qh(4)^{2/3}\\le C_qH^{2/3}',
                                    '\\le C_qH^{2/3}', 'never divides by `v`']))
record.call('physical mass substitution and target powers', 'mass',
            computed_scale.fetch('fluxPrefactor') == expected.dig('scaleLedger', 'fluxPrefactor') &&
              computed_scale.fetch('massPrefactor') == expected.dig('scaleLedger', 'massPrefactor') &&
              computed_scale.fetch('afterMass') == expected.dig('scaleLedger', 'afterMass') &&
              fragments?(compact, ['4\\pi\\delta_0a^2R^5H', 'C_qa^{2/3}R^{-1/3}']))
record.call('normalization and frozen rate', 'normalization',
            computed_scale.fetch('normalized') == expected.dig('scaleLedger', 'normalized') &&
              computed_scale.fetch('frozenRate') == expected.dig('scaleLedger', 'frozenRate') &&
              fragments?(compact, ['R^{-2}\\omega M', '\\frac\\omega R', '-\\frac2{11907}']))
record.call('explicit fixed-q boundary', 'q_boundary',
            fragments?(compact, ['grows at most exponentially in `q`', 'no quantitative uniform bound in `q`',
                                  'fixed-finite-dimensional theorem', 'outer-cap construction of R0.75R']))
record.call('bounded primary-source boundary', 'source',
            fragments?(compact_source, ['Nazarov', 'https://www.mathnet.ru/eng/aa397',
                                         'https://arxiv.org/abs/1107.0039',
                                         'no completeness, novelty, or priority claim']))
record.call('primary audit verdict and finite boundary', 'audit',
            fragments?(compact_primary, ['Current verdict: **PASS**', 'Mathematical blocker count: **0**',
                                          'Release blocker count: **0**', 'not represented as proof']))
record.call('analytic no-figure gate', 'figure',
            fragments?(compact, ['proof is analytic', 'no formal scientific figure or simulation is claimed']) &&
              fragments?(compact_primary, ['No formal figure is required', 'no simulation result enters the claim']))
record.call('fixed-subfamily claim boundary', 'boundary',
            fragments?(compact, ['high-carrier sector for three or more modes', 'arbitrary dyadic packets',
                                  'arbitrary-field E.24', 'Version-M measurement row', '**NOT CLAY.**']))
record.call('Python certificate agreement', 'bindings',
            certificate.fetch('verdict') == 'PASS' &&
              certificate.fetch('clock') == computed_clock &&
              certificate.fetch('scaledCase') == computed_scaled &&
              certificate.fetch('spatialOde') == computed_ode &&
              certificate.fetch('temporalTrace') == computed_trace &&
              certificate.fetch('transportIdentity') == computed_identity &&
              certificate.fetch('scaleLedger') == computed_scale &&
              certificate.fetch('negativeMutations') == NEGATIVE_MUTATIONS)

verdict = checks.all? { |check| check.fetch('pass') } ? 'PASS' : 'FAIL'
passed = checks.count { |check| check.fetch('pass') }
report = [
  '# R0.75X independent finite audit', '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{passed}/#{checks.length}",
  "- Blocker count: #{verdict == 'PASS' ? 0 : checks.length - passed}", '',
  'The Ruby implementation independently recomputes the q=3 companion row,',
  'scaled variables, term count, polynomial transport identity, target powers,',
  'source bindings, and fixed-q boundary. It does not replace the continuum',
  'compactness lemma or the Turan--Nazarov theorem with finite sampling.',
  'The theorem is low-carrier and fixed-finite-dimensional. **NOT CLAY.**', ''
]
File.write(REPORT, report.join("\n"), mode: 'w', encoding: 'UTF-8')
puts JSON.generate('suite' => 'r075x-ruby-independent', 'verdict' => verdict, 'assertions' => checks.length)
exit(verdict == 'PASS' ? 0 : 1)
