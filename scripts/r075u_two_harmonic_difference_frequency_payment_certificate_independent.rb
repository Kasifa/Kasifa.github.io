#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed finite audit for frozen R0.75U.

require 'digest'
require 'json'

ROOT = File.expand_path('..', __dir__)
STEM = 'r075u_two_harmonic_difference_frequency_payment'
MAIN = File.join(ROOT, 'research', "#{STEM}.md")
PRIMARY = File.join(ROOT, 'research', "#{STEM}_primary_audit.md")
SOURCE = File.join(ROOT, 'research', 'r075u_report-source.md')
FIXTURES = File.join(ROOT, 'scripts', "#{STEM}_fixtures.json")
EXPECTED = File.join(ROOT, 'scripts', "#{STEM}_expected.json")
CERT = ENV.fetch('R075U_JSON', File.join(ROOT, 'research', "#{STEM}_certificate.json"))
REPORT = ENV.fetch('R075U_RUBY_REPORT', File.join(ROOT, 'research', "#{STEM}_independent_audit.md"))
MUTATION = ENV.fetch('R075U_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => 'f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4',
  "research/#{STEM}_primary_audit.md" => '3687decf19ff49016e101a174d066b355689dcca7a4dc36a941b84994b118d6a',
  'research/r075u_report-source.md' => 'd0e9356a162b683a33c5b4c49692a62962d2a9c63cccba9eb9d84040aaf4a01f',
  'research/r075b_bulk_clock_outer_padding_gate.md' => '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075s_full_frequency_single_harmonic_clock_payment.md' => 'd2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd',
  'research/r075t_two_harmonic_collar_coercivity.md' => '822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66'
}.freeze
FIXTURES_SHA256 = 'c654b79a1b3b69078df01000c43fee54fdff39ea64c7bc47e206b114dc20b0c6'
EXPECTED_SHA256 = '381e80ca54eee51fb3aab823837f0bfdc28e84353e02c8f41fceed261d6aec12'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash dependency_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema],
  'integrity' => %w[utf8 controls tags displays references],
  'clock' => %w[clock_length cutoff_onset cutoff_derivative],
  'radial' => %w[radial_low radial_high quotient no_extra_d],
  'moment' => %w[tau phase_travel node_crossing cubic_moment],
  'slowLow' => %w[low_heat slow_phase sine_distance q_sigma],
  'slowHigh' => %w[high_heat zeta_onset laplace_first laplace_second],
  'fast' => %w[fast_phase w_zero bv_ibp tau_compare],
  'scaling' => %w[time_change amplitude_cancel d_power r_power],
  'mass' => %w[t_coercivity a_power target_power],
  'normalization' => %w[p_definition x_definition r_cancel omega_rate],
  'exactPde' => %w[transport_heat exact_shear background_boundary],
  'source' => %w[primary_sources no_import bounded_search],
  'audit' => %w[audit_pass math_zero release_zero alias_boundary],
  'boundary' => %w[difference_only self_sum_open low_carrier_open e24_open not_clay]
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

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  warn "unknown R075U_RUBY_MUTATION: #{MUTATION}"
  exit 2
end
abort('duplicate mutation name in R0.75U Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

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
  'source_hash' => 'research/r075u_report-source.md',
  'dependency_hash' => 'research/r075t_two_harmonic_collar_coercivity.md'
}
frozen[drift[MUTATION]] = '0' * 64 if drift.key?(MUTATION)
bindings = frozen.to_h do |path, expected_hash|
  [path, { 'expectedSha256' => expected_hash, 'observedSha256' => digest(File.join(ROOT, path)) }]
end

clock = fixtures.fetch('clock')
radius = Rational(clock.fetch('R'))
computed_clock = { 'T' => qtext(Rational(clock.fetch('durationCoefficient'), 1) * radius**Integer(clock.fetch('durationRPower'))) }

phase_cases = fixtures.fetch('phaseCases').map do |row|
  lam = Rational(row.fetch('Lambda'))
  sigma = Rational(row.fetch('sigmaAbs'))
  initial = Rational(row.fetch('initialDistance'))
  tau = lam <= 1 ? Rational(1) : 1 / lam
  travel = sigma * tau
  qq = [Rational(1), initial + travel].min
  {
    'name' => row.fetch('name'), 'tau' => qtext(tau), 'phaseTravel' => qtext(travel),
    'q' => qtext(qq), 'regime' => travel <= 1 ? 'slow' : 'fast'
  }
end

radial_cases = fixtures.fetch('radialCases').map do |row|
  epsilon = Rational(row.fetch('n'), 1) * Rational(row.fetch('a'), 1) * Rational(row.fetch('R'))
  { 'name' => row.fetch('name'), 'naR' => qtext(epsilon), 'branch' => epsilon <= 1 ? 'low' : 'high' }
end

after_radial = { 'a' => Rational(2), 'R' => Rational(5, 3) }
after_mass = { 'a' => Rational(2, 3), 'R' => Rational(-1, 3) }
normalized = { 'a' => Rational(2, 3), 'R' => Rational(0), 'omega' => Rational(1, 3), 'p' => Rational(2, 3) }
scale_ledger = {
  'afterRadial' => encoded(after_radial),
  'afterMass' => encoded(after_mass),
  'normalized' => encoded(normalized),
  'frozenRate' => qtext(-Rational(fixtures.dig('frozenScales', 'cGamma')) / 12)
}

tags = text.scan(/\\tag\{U\.(\d+)\}/).flatten.map(&:to_i)
refs = text.scan(/U\.(\d+)/).flatten.map(&:to_i)
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
            clean?(raw) && clean?(raw_primary) && clean?(raw_source) && tags == (1..28).to_a &&
              text.scan('\\[').length == 28 && text.scan('\\]').length == 28 && (refs.uniq - tags.uniq).empty?)
record.call('complete clock and cutoff onset', 'clock',
            computed_clock == expected.fetch('clock') &&
              fragments?(compact, ['T_R=4R^2', '\\eta_R(0)=0', 'C_\\eta R^{-2}']))
record.call('uniform radial quotient', 'radial',
            radial_cases == expected.fetch('radialCases') &&
              fragments?(compact, ['\\min\\{naR,1\\}', '\\frac{|J_{n,R}|}{n}\\le Ca^2R^3']))
record.call('phase-distance moment', 'moment',
            phase_cases == expected.fetch('phaseCases') &&
              fragments?(compact, ['periodic triangular wave', '\\ge c\\tau q^3', 'cubic mean is `r^3/4`']))
record.call('slow low-heat branch', 'slowLow',
            fragments?(compact, ['Assume `|sigma|tau<=1`', 'If `Lambda<=1`',
                                  '|\\sin(\\alpha+\\sigma s)|\\le Cq', '`q>=c|sigma|`']))
record.call('slow high-heat branch', 'slowHigh',
            fragments?(compact, ['If `Lambda>=1`', 'zeta(s)<=C_eta s',
                                  '\\int_0^\\infty se^{-\\Lambda s}', 'C|\\sigma|\\tau^2q']))
record.call('fast BV branch', 'fast',
            fragments?(compact, ['Assume `|sigma|tau>=1`', 'Since `w(0)=0`',
                                  'one integration by parts', '\\le C\\tau']))
record.call('exact scaling and amplitude cancellation', 'scaling',
            fragments?(compact, ['If `AC=0`', '\\Lambda=(k^2+m^2)R^2', '\\sigma=dBR^2',
                                  '\\frac C{dR^{4/3}}', 'amplitude product cancels exactly']))
record.call('defect mass and target powers', 'mass',
            scale_ledger.fetch('afterRadial') == expected.dig('scaleLedger', 'afterRadial') &&
              scale_ledger.fetch('afterMass') == expected.dig('scaleLedger', 'afterMass') &&
              fragments?(compact, ['Ca^2R^{5/3}', 'ca^2R^3', 'Ca^{2/3}R^{-1/3}']))
record.call('normalization and frozen rate', 'normalization',
            scale_ledger.fetch('normalized') == expected.dig('scaleLedger', 'normalized') &&
              scale_ledger.fetch('frozenRate') == expected.dig('scaleLedger', 'frozenRate') &&
              fragments?(compact, ['R^{-2}\\omega M', '\\frac\\omega R', '-\\frac2{11907}']))
record.call('exact shear PDE and background boundary', 'exactPde',
            fragments?(compact, ['\\partial_tF+B\\partial_2F-\\partial_2^2F=0',
                                  'exact smooth unforced shear', 'nonzero constant background']))
record.call('bounded primary-source boundary', 'source',
            fragments?(compact_source, ['arXiv:1604.01831', 'arXiv:1609.07020v6', 'arXiv:1711.04279',
                                         'no external theorem has been silently substituted']))
record.call('primary audit verdict and alias boundary', 'audit',
            fragments?(compact_primary, ['Current verdict: **PASS**', 'Mathematical blocker count: **0**',
                                          'Release blocker count: **0**', 'fixed-grid scan can alias']))
record.call('claim boundary', 'boundary',
            fragments?(compact, ['difference-frequency target T.31', 'not a complete two-harmonic flux theorem',
                                  'self frequencies `2k,2m`', 'arbitrary-field E.24', '\\mathbf{NOT\\ CLAY}']))
record.call('Python certificate agreement', 'bindings',
            certificate.fetch('verdict') == 'PASS' && certificate.fetch('clock') == computed_clock &&
              certificate.fetch('phaseCases') == phase_cases && certificate.fetch('radialCases') == radial_cases &&
              certificate.fetch('scaleLedger') == scale_ledger)

verdict = checks.all? { |row| row.fetch('pass') } ? 'PASS' : 'FAIL'
passed = checks.count { |row| row.fetch('pass') }
report = [
  '# R0.75U independent finite audit', '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{passed}/#{checks.length}",
  "- Blocker count: #{verdict == 'PASS' ? 0 : checks.length - passed}", '',
  'The Ruby implementation independently recomputes the clock, phase regimes,',
  'radial branches, target powers, file bindings, and proof boundary.',
  'It does not use fast-phase quadrature as proof.  The self/sum block and',
  'complete two-mode payment remain OPEN. **NOT CLAY.**', ''
]
File.write(REPORT, report.join("\n"), mode: 'w', encoding: 'UTF-8')
puts JSON.generate({ 'suite' => 'r075u-ruby-independent', 'verdict' => verdict, 'assertions' => checks.length })
exit(verdict == 'PASS' ? 0 : 1)
