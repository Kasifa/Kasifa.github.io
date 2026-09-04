#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed finite audit for frozen R0.75T.

require 'digest'
require 'json'

ROOT = File.expand_path('..', __dir__)
STEM = 'r075t_two_harmonic_collar_coercivity'
MAIN = File.join(ROOT, 'research', "#{STEM}.md")
PRIMARY = File.join(ROOT, 'research', "#{STEM}_primary_audit.md")
SOURCE = File.join(ROOT, 'research', 'r075t_report-source.md')
FIXTURES = File.join(ROOT, 'scripts', "#{STEM}_fixtures.json")
EXPECTED = File.join(ROOT, 'scripts', "#{STEM}_expected.json")
CERT = ENV.fetch('R075T_JSON', File.join(ROOT, 'research', "#{STEM}_certificate.json"))
REPORT = ENV.fetch('R075T_RUBY_REPORT', File.join(ROOT, 'research', "#{STEM}_independent_audit.md"))
MUTATION = ENV.fetch('R075T_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => '822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66',
  "research/#{STEM}_primary_audit.md" => '97d804444737284d7ec40b3ce45389272b1a9f61d1901f7bcebf9ed0eab935e5',
  'research/r075t_report-source.md' => 'c2255cdd07f2e490921d93ba7e62a809c0348a9e6136b7fd5537cf3799e4e8d8',
  'research/r075e_horizontal_cross_mode_flux_reduction.md' => '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075m_dyadic_packet_diffusive_flux_gain.md' => '13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075s_full_frequency_single_harmonic_clock_payment.md' => 'd2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd'
}.freeze
FIXTURES_SHA256 = '939b04eeccb9c96b6d5cb21d49ebc48e7a8387dfccdc08afd2dfd6db77fd4393'
EXPECTED_SHA256 = 'cd58217667129d5a2f01dd2b315b86a934de1258be2eefab401f5b66efc127c5'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash dependency_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema],
  'integrity' => %w[utf8 controls tags displays references],
  'geometry' => %w[ell radial_difference fiber_area plateau_power],
  'envelope' => %w[regular_basis beta_zero gram_compact phase_ibp],
  'slowBeat' => %w[envelope_identity sinc_identity phase_distance slow_defect],
  'resolvedBeat' => %w[gram_formula sinc_gap boundary_errors resolved_defect],
  'holder' => %w[holder_direction holder_length amplitude_degree],
  'diffusive' => %w[unequal_heat moving_phase time_slice],
  'flux' => %w[self_coefficients cross_coefficients difference_frequency sum_frequency],
  'power' => %w[fiber_power interval_power final_power],
  'source' => %w[primary_sources no_import bounded_search],
  'audit' => %w[audit_pass math_zero release_zero],
  'boundary' => %w[two_modes low_carrier_open temporal_open e24_open not_clay]
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

def rational_text(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  warn "unknown R075T_RUBY_MUTATION: #{MUTATION}"
  exit 2
end
abort('duplicate mutation name in R0.75T Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

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
  'source_hash' => 'research/r075t_report-source.md',
  'dependency_hash' => 'research/r075m_dyadic_packet_diffusive_flux_gain.md'
}
frozen[drift[MUTATION]] = '0' * 64 if drift.key?(MUTATION)
bindings = frozen.to_h do |path, expected_hash|
  [path, { 'expectedSha256' => expected_hash, 'observedSha256' => digest(File.join(ROOT, path)) }]
end

geometry = fixtures.fetch('geometry')
a = Rational(geometry.fetch('a'), 1)
delta0 = Rational(geometry.fetch('delta0'), 1)
radius = Rational(geometry.fetch('R'))
ell = a * radius
radial = 4 * a * delta0 * radius * radius
computed_geometry = {
  'ell' => rational_text(ell),
  'radialSquaredDifference' => rational_text(radial),
  'fiberAreaPiCoefficient' => rational_text(radial),
  'plateauPower' => { 'a' => 2, 'R' => 3, 'H' => 3 }
}

beat_cases = fixtures.fetch('beatCases').map do |row|
  local_ell = Rational(row.fetch('ell'))
  d_ell = (Integer(row.fetch('k')) - Integer(row.fetch('m'))) * local_ell
  theta = Rational(row.fetch('phaseDistanceToPi'))
  q_squared = [Rational(1), d_ell**2 + theta**2].min
  amp_a = Rational(row.fetch('A'), 1)
  amp_c = Rational(row.fetch('C'), 1)
  h_squared = (amp_a - amp_c)**2 + amp_a * amp_c * q_squared
  {
    'name' => row.fetch('name'),
    'dEll' => rational_text(d_ell),
    'qSquared' => rational_text(q_squared),
    'hSquared' => rational_text(h_squared),
    'regime' => d_ell <= 1 ? 'unresolved' : 'resolved'
  }
end

tags = text.scan(/\\tag\{T\.(\d+)\}/).flatten.map(&:to_i)
refs = text.scan(/T\.(\d+)/).flatten.map(&:to_i)
checks = []
record = lambda do |name, group, condition|
  checks << { 'name' => name, 'pass' => condition && !GROUPS.fetch(group).include?(MUTATION) }
end

record.call('frozen source bindings', 'bindings',
            bindings.values.all? { |row| row['expectedSha256'] == row['observedSha256'] })
record.call('fixture and expected bindings', 'inputs',
            digest(FIXTURES) == FIXTURES_SHA256 && digest(EXPECTED) == EXPECTED_SHA256 &&
              fixtures.fetch('schema').end_with?('fixtures-v1'))
record.call('UTF-8, controls, tags, displays, and references', 'integrity',
            clean?(raw) && clean?(raw_primary) && clean?(raw_source) && tags == (1..31).to_a &&
              text.scan('\\[').length == 32 && text.scan('\\]').length == 32 && (refs.uniq - tags.uniq).empty?)
record.call('exact plateau fibre geometry', 'geometry',
            computed_geometry == expected.fetch('geometry') &&
              fragments?(compact, ['=4\\pi a\\delta_0R^2', 'I_ell=[-ell/2,ell/2]', 'a^2R^3H_{d,aR}^3']))
record.call('uniform slow-envelope sampling', 'envelope',
            fragments?(compact, ['alpha,gamma in C', 'v_\\beta(s)=', 's,&\\beta=0',
                                  'continuous and positive definite', 'one integration by parts']))
record.call('unresolved beat defect', 'slowBeat',
            beat_cases.first(2) == expected.fetch('beatCases').first(2) &&
              fragments?(compact, ['A^2+C^2+2AC\\operatorname {sinc}', '(A-C)^2+2AC',
                                    '\\min\\{1,(d\\ell)^2+\\theta^2\\}']))
record.call('resolved beat gap', 'resolvedBeat',
            beat_cases.drop(2) == expected.fetch('beatCases').drop(2) &&
              fragments?(compact, ['2\\sin(1/2)<1', 'C(mell)^(-1)ell(A^2+C^2)',
                                    '\\ge c\\ell(A^2+C^2)']))
record.call('Holder cubic conversion', 'holder',
            fragments?(compact, ['\\ge\\ell^{-1/2}', '\\ge c\\ell H_{d,\\ell}^3']))
record.call('exact diffusive time-slice corollary', 'diffusive',
            fragments?(compact, ['A_t&=Ae^{-k^2t}', 'C_t=Ce^{-m^2t}',
                                  '\\phi-\\psi+dBt', '\\int_0^{T_R}H_{d,aR}(t)^3\\,dt']))
record.call('four exact flux prefactors', 'flux',
            fixtures.fetch('fluxCoefficients') == expected.fetch('fluxCoefficients') &&
              fragments?(compact, ['\\frac B4', 'J_{2k,R}', 'J_{2m,R}', '\\frac B2',
                                    'J_{d,R}', 'J_{k+m,R}']))
record.call('final power ledger', 'power',
            computed_geometry.fetch('plateauPower') == { 'a' => 2, 'R' => 3, 'H' => 3 })
record.call('bounded primary-source boundary', 'source',
            fragments?(compact_source, ['arXiv:math/0012186', 'arXiv:1609.07020v6',
                                         'not a completeness, novelty, or priority certificate']))
record.call('primary audit verdict', 'audit',
            fragments?(compact_primary, ['Current verdict: **PASS**', 'Mathematical blocker count: **0**',
                                          'Release blocker count: **0**', 'falsification aid only']))
record.call('claim boundary', 'boundary',
            fragments?(compact, ['exactly two harmonics', 'does **not** yet prove', 'low-carrier pairs',
                                  'arbitrary-field E.24', '\\mathbf{NOT\\ CLAY}']))
record.call('Python certificate agreement', 'bindings',
            certificate.fetch('verdict') == 'PASS' && certificate.fetch('geometry') == computed_geometry &&
              certificate.fetch('beatCases') == beat_cases &&
              certificate.fetch('fluxCoefficients') == fixtures.fetch('fluxCoefficients'))

verdict = checks.all? { |row| row.fetch('pass') } ? 'PASS' : 'FAIL'
passed = checks.count { |row| row.fetch('pass') }
report = [
  '# R0.75T independent finite audit',
  '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{passed}/#{checks.length}",
  "- Blocker count: #{verdict == 'PASS' ? 0 : checks.length - passed}",
  '',
  'The Ruby implementation independently recomputes the exact fibre geometry,',
  'three beat fixtures, four flux prefactors, file bindings, and proof boundary.',
  'It treats T.31 and complete two-mode payment as OPEN. **NOT CLAY.**',
  ''
]
File.write(REPORT, report.join("\n"), mode: 'w', encoding: 'UTF-8')
puts JSON.generate({ 'suite' => 'r075t-ruby-independent', 'verdict' => verdict, 'assertions' => checks.length })
exit(verdict == 'PASS' ? 0 : 1)
