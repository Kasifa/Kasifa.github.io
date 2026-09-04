#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed finite audit for frozen R0.75W.

require 'digest'
require 'json'

ROOT = File.expand_path('..', __dir__)
STEM = 'r075w_full_frequency_two_harmonic_flux_payment'
MAIN = File.join(ROOT, 'research', "#{STEM}.md")
PRIMARY = File.join(ROOT, 'research', "#{STEM}_primary_audit.md")
SOURCE = File.join(ROOT, 'research', 'r075w_report-source.md')
FIXTURES = File.join(ROOT, 'scripts', "#{STEM}_fixtures.json")
EXPECTED = File.join(ROOT, 'scripts', "#{STEM}_expected.json")
CERT = ENV.fetch('R075W_JSON', File.join(ROOT, 'research', "#{STEM}_certificate.json"))
REPORT = ENV.fetch('R075W_RUBY_REPORT', File.join(ROOT, 'research', "#{STEM}_independent_audit.md"))
MUTATION = ENV.fetch('R075W_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => '571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4',
  "research/#{STEM}_primary_audit.md" => '78255a0d84020d1d1c9dc6509ed1cc8eb9a9fdaced21d93e4f586383e4fc9ea0',
  'research/r075w_report-source.md' => '461ab29f02072eb039c9b57c497a87d04ff95255af68d561c68f4d3224726d7a',
  'research/r075b_bulk_clock_outer_padding_gate.md' => '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075t_two_harmonic_collar_coercivity.md' => '822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66',
  'research/r075v_complete_two_harmonic_flux_payment.md' => '6917ff77099b6271b005ca90335df589434a38b0a57001893dcae8b02fd34824'
}.freeze
FIXTURES_SHA256 = '2b59973a6901b0a70068a2952e1324fd1780f853508c250821daaab659aa8b1f'
EXPECTED_SHA256 = '44afc8aebea8e15a4d54adf28fd48f8da28dd61c74e6f87a9ded21667d61867f'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash b_hash r_hash t_hash v_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema],
  'integrity' => %w[utf8 controls tags displays references],
  'clock' => %w[clock_length cutoff_onset cutoff_derivative],
  'split' => %w[dyadic_pair low_sector high_sector exhaustive_split scaled_upper_bound],
  'scaled' => %w[ell alpha beta v alpha_heat beta_heat scaled_pde],
  'ode' => %w[ode_coefficients state_matrix compact_family initial_jet confluent_degree gap_free_space],
  'trace' => %w[four_terms real_parts imaginary_free gap_free_time turan_power sublevel_set endpoint_trace],
  'kernel' => %w[kernel_odd kernel_zero primitive_support kernel_norms primitive_second cross_section],
  'identity' => %w[square_pde advective_row energy_derivative xi_second dissipation heat_cancel identity_signs],
  'payment' => %w[spatial_application holder_time terminal_payment dimensionless_payment],
  'mass' => %w[fibre_area mass_a mass_r flux_prefactor target_a target_r target_m],
  'normalization' => %w[p_definition x_definition r_cancel omega_power frozen_rate],
  'source' => %w[nazarov_original primary_restatement clay_source bounded_search],
  'audit' => %w[audit_pass math_zero release_zero finite_boundary],
  'figure' => %w[analytic_only no_simulation_claim no_formal_figure],
  'boundary' => %w[exact_pair three_modes_open packets_open e24_open version_m_conditional not_clay]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

def digest(path)
  Digest::SHA256.file(path).hexdigest
end

def clean?(bytes)
  value = bytes.dup.force_encoding(Encoding::UTF_8)
  value.valid_encoding? && bytes.bytes.none? { |b| (b < 32 && ![9, 10, 13].include?(b)) || b == 127 }
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
  out = Array.new(left.length + right.length - 1, Rational(0))
  left.each_with_index do |x, i|
    right.each_with_index { |y, j| out[i + j] += x * y }
  end
  out
end

def poly_deriv(poly, order = 1)
  out = poly.dup
  order.times { out = (1...out.length).map { |j| j * out[j] } }
  out
end

def poly_integral_symmetric(poly)
  poly.each_with_index.sum(Rational(0)) do |value, j|
    j.even? ? Rational(2) * value / (j + 1) : Rational(0)
  end
end

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  warn "unknown R075W_RUBY_MUTATION: #{MUTATION}"
  exit 2
end
abort('duplicate mutation name in R0.75W Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

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
drift = {
  'main_hash' => "research/#{STEM}.md",
  'primary_hash' => "research/#{STEM}_primary_audit.md",
  'source_hash' => 'research/r075w_report-source.md',
  'b_hash' => 'research/r075b_bulk_clock_outer_padding_gate.md',
  'r_hash' => 'research/r075r_outer_cap_spectral_concentration_obstruction.md',
  't_hash' => 'research/r075t_two_harmonic_collar_coercivity.md',
  'v_hash' => 'research/r075v_complete_two_harmonic_flux_payment.md'
}
frozen[drift[MUTATION]] = '0' * 64 if drift.key?(MUTATION)
bindings = frozen.to_h do |path, expected_hash|
  [path, { 'expectedSha256' => expected_hash, 'observedSha256' => digest(File.join(ROOT, path)) }]
end

clock = fixtures.fetch('clock')
radius = Rational(clock.fetch('R'))
computed_clock = {
  'T' => qtext(Rational(clock.fetch('durationCoefficient')) * radius**Integer(clock.fetch('durationRPower')))
}

row = fixtures.fetch('scaledCase')
k = Rational(row.fetch('k'))
m = Rational(row.fetch('m'))
a = Rational(row.fetch('a'))
radius = Rational(row.fetch('R'))
b_shear = Rational(row.fetch('B'))
ell = a * radius
alpha = k * ell
beta = m * ell
velocity = b_shear * radius / a
computed_scaled = {
  'ell' => qtext(ell), 'alpha' => qtext(alpha), 'beta' => qtext(beta), 'v' => qtext(velocity),
  'alphaHeat' => qtext(alpha**2 / a**2), 'betaHeat' => qtext(beta**2 / a**2)
}
computed_ode = {
  'secondDerivativeCoefficient' => qtext(alpha**2 + beta**2),
  'zerothCoefficient' => qtext(alpha**2 * beta**2), 'confluentDegree' => 3
}
computed_trace = { 'maximumTerms' => 4, 'turanExponent' => 3, 'gapFactor' => 0 }

identity = fixtures.fetch('transportIdentity')
iv = Rational(identity.fetch('v'))
is_value = Rational(identity.fetch('s'))
ia = Rational(identity.fetch('a'))
xi = [1, 0, -2, 0, 1].map { |x| Rational(x) }
w = poly_deriv(xi)
g = [-iv * is_value, Rational(1)]
g2 = poly_mul(g, g)
advective = iv * poly_integral_symmetric(poly_mul(w, g2))
energy_derivative = -2 * iv * poly_integral_symmetric(poly_mul(xi, g))
xi_second = poly_integral_symmetric(poly_mul(poly_deriv(xi, 2), g2))
dissipation = poly_integral_symmetric(xi)
heat_cancellation = -xi_second / ia**2 + 2 * dissipation / ia**2
computed_identity = {
  'advectiveRow' => qtext(advective), 'energyDerivative' => qtext(energy_derivative),
  'xiSecondRow' => qtext(xi_second), 'dissipationRow' => qtext(dissipation),
  'heatCancellation' => qtext(heat_cancellation)
}

computed_scale = {
  'fluxPrefactor' => encoded('a' => Rational(2), 'R' => Rational(3), 'v' => Rational(1)),
  'massPrefactor' => encoded('a' => Rational(2), 'R' => Rational(5), 'H' => Rational(1)),
  'afterMass' => encoded('a' => Rational(2, 3), 'R' => Rational(-1, 3), 'M' => Rational(2, 3)),
  'normalized' => encoded('a' => Rational(2, 3), 'R' => Rational(0), 'omega' => Rational(1, 3), 'p' => Rational(2, 3)),
  'frozenRate' => qtext(-Rational(fixtures.dig('frozenScales', 'cGamma')) / 12)
}

tags = text.scan(/\\tag\{W\.(\d+)\}/).flatten.map(&:to_i)
refs = text.scan(/\bW\.(\d+)\b/).flatten.map(&:to_i)
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
            clean?(raw) && clean?(raw_primary) && clean?(raw_source) && tags == (1..33).to_a &&
              text.scan('\\[').length == 34 && text.scan('\\]').length == 34 && (refs.uniq - tags.uniq).empty?)
record.call('complete clock and cutoff', 'clock',
            computed_clock == expected.fetch('clock') &&
              fragments?(compact, ['T_R=4R^2', '\\eta_R(0)=0', 'C_\\eta R^{-2}']))
record.call('exhaustive carrier split', 'split',
            fragments?(compact, ['1<=m<k<=2m', 'maR\\ge C_0', '`maR<C_0`', '`0<beta<alpha<=2C_0`',
                                  'partition all possibilities']))
record.call('low-carrier scaled variables and heat', 'scaled',
            computed_scaled == expected.fetch('scaledCase') &&
              fragments?(compact, ['v=\\frac{BR}{a}', '\\partial_sG+v\\partial_zG-a^{-2}\\partial_z^2G=0']))
record.call('confluent fourth-order spatial ODE', 'ode',
            computed_ode == expected.fetch('spatialOde') &&
              fragments?(compact, ['(\\partial_z^2+\\alpha^2)(\\partial_z^2+\\beta^2)g=0',
                                    'cubic-polynomial space', 'initial jet', 'a nonzero limiting solution']))
record.call('gap-free four-term temporal trace', 'trace',
            computed_trace == expected.fetch('temporalTrace') &&
              fragments?(compact, ['N\\le4', 'independent of the imaginary parts', 'half-measure sublevel set',
                                    'h(4)\\le C H', '-\\alpha^2/a^2\\pm i\\alpha v']))
record.call('scaled radial primitive', 'kernel',
            fragments?(compact, ['W_a(z)=-2\\pi a z', 'Oddness gives `int W_a=0`',
                                  '\\Xi_a(z)=\\int_{-\\infty}^{z}', '\\|\\Xi_a\'\'\\|_{L^1}=\\|W_a\'\\|_{L^1}\\le Ca',
                                  '=aR^2\\int_{\\mathbb R}W_a(z)G(s,z)^2']))
record.call('transport identity exact finite fixture', 'identity',
            computed_identity == expected.fetch('transportIdentity') && advective == energy_derivative &&
              heat_cancellation.zero? && fragments?(compact, ['=-2a^{-2}|\\partial_zG|^2',
                                                               "E'(s)-a^{-2}\\int\\Xi_a''G^2",
                                                               "+2a^{-2}\\int\\Xi_a|\\partial_zG|^2"]))
record.call('identity sign audit', 'identity',
            fragments?(compact_primary, ['terminal energy: plus', 'cutoff derivative: minus',
                                          'heat row: minus', 'localized dissipation: plus']))
record.call('dimensionless complete-clock payment', 'payment',
            fragments?(compact, ['|E(4)|\\le Ch(4)^{2/3}\\le CH^{2/3}',
                                  '\\left|v\\int_0^4\\zeta\\int W_aG^2\\right|', 'No division by `v`']))
record.call('physical mass substitution and target powers', 'mass',
            computed_scale.fetch('fluxPrefactor') == expected.dig('scaleLedger', 'fluxPrefactor') &&
              computed_scale.fetch('massPrefactor') == expected.dig('scaleLedger', 'massPrefactor') &&
              computed_scale.fetch('afterMass') == expected.dig('scaleLedger', 'afterMass') &&
              fragments?(compact, ['4\\pi\\delta_0a^2R^5H', 'Ca^{2/3}R^{-1/3}']))
record.call('normalization and frozen rate', 'normalization',
            computed_scale.fetch('normalized') == expected.dig('scaleLedger', 'normalized') &&
              computed_scale.fetch('frozenRate') == expected.dig('scaleLedger', 'frozenRate') &&
              fragments?(compact, ['R^{-2}\\omega M', '\\frac\\omega R', '-\\frac2{11907}']))
record.call('bounded primary-source boundary', 'source',
            fragments?(compact_source, ['Nazarov', 'https://www.mathnet.ru/eng/aa397', 'arxiv.org/abs/1107.0039',
                                         'official Clay Mathematics Institute', 'not a novelty search']))
record.call('primary audit verdict and finite boundary', 'audit',
            fragments?(compact_primary, ['Current verdict: **PASS**', 'Mathematical blocker count: **0**',
                                          'Release blocker count: **0**', 'not represented as proof']))
record.call('analytic no-figure gate', 'figure',
            fragments?(compact, ['proof is analytic', 'no formal scientific figure or simulation is claimed']) &&
              fragments?(compact_primary, ['No formal figure is required', 'would not verify compact ODE observability']))
record.call('exact-subfamily claim boundary', 'boundary',
            fragments?(compact, ['exact pair W.1', 'three or more harmonics', 'arbitrary dyadic packets',
                                  'arbitrary-field E.24', 'conditional on the realized-subclass', '**NOT CLAY.**']))
record.call('Python certificate agreement', 'bindings',
            certificate.fetch('verdict') == 'PASS' && certificate.fetch('clock') == computed_clock &&
              certificate.fetch('scaledCase') == computed_scaled && certificate.fetch('spatialOde') == computed_ode &&
              certificate.fetch('temporalTrace') == computed_trace &&
              certificate.fetch('transportIdentity') == computed_identity &&
              certificate.fetch('scaleLedger') == computed_scale &&
              certificate.fetch('negativeMutations') == NEGATIVE_MUTATIONS)

verdict = checks.all? { |row_check| row_check.fetch('pass') } ? 'PASS' : 'FAIL'
passed = checks.count { |row_check| row_check.fetch('pass') }
report = [
  '# R0.75W independent finite audit', '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{passed}/#{checks.length}",
  "- Blocker count: #{verdict == 'PASS' ? 0 : checks.length - passed}", '',
  'The Ruby implementation independently recomputes the scaled frequencies,',
  'confluent ODE coefficients, polynomial transport-identity fixture, target',
  'powers, source bindings, and proof boundary. It does not replace the',
  'continuum ODE compactness lemma or Turan--Nazarov theorem with sampling.',
  'The theorem is limited to one exact dyadic two-harmonic shear. **NOT CLAY.**', ''
]
File.write(REPORT, report.join("\n"), mode: 'w', encoding: 'UTF-8')
puts JSON.generate({ 'suite' => 'r075w-ruby-independent', 'verdict' => verdict, 'assertions' => checks.length })
exit(verdict == 'PASS' ? 0 : 1)
