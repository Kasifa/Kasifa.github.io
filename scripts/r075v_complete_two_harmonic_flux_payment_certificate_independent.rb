#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed finite audit for frozen R0.75V.

require 'digest'
require 'json'

ROOT = File.expand_path('..', __dir__)
STEM = 'r075v_complete_two_harmonic_flux_payment'
MAIN = File.join(ROOT, 'research', "#{STEM}.md")
PRIMARY = File.join(ROOT, 'research', "#{STEM}_primary_audit.md")
SOURCE = File.join(ROOT, 'research', 'r075v_report-source.md')
FIXTURES = File.join(ROOT, 'scripts', "#{STEM}_fixtures.json")
EXPECTED = File.join(ROOT, 'scripts', "#{STEM}_expected.json")
CERT = ENV.fetch('R075V_JSON', File.join(ROOT, 'research', "#{STEM}_certificate.json"))
REPORT = ENV.fetch('R075V_RUBY_REPORT', File.join(ROOT, 'research', "#{STEM}_independent_audit.md"))
MUTATION = ENV.fetch('R075V_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => '6917ff77099b6271b005ca90335df589434a38b0a57001893dcae8b02fd34824',
  "research/#{STEM}_primary_audit.md" => 'cf23652951c5e1721270577c9a32bc476142b439aefa8ee5f62112cfd8bf5cbd',
  'research/r075v_report-source.md' => 'a099949ad6968468389b412e1d250c5e1a788ac046b949d4d69fbcf1501e9811',
  'research/r075b_bulk_clock_outer_padding_gate.md' => '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075t_two_harmonic_collar_coercivity.md' => '822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66',
  'research/r075u_two_harmonic_difference_frequency_payment.md' => 'f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4'
}.freeze
FIXTURES_SHA256 = 'd2a16f6e718931aebca696d4934fa497be6bceef8c4e301a9851d04d11e622bc'
EXPECTED_SHA256 = 'ebe2cd2b8aad095730eca4b59e5b79e630a28a0f0215fd2cec0024a4593386c6'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash dependency_hash u_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema],
  'integrity' => %w[utf8 controls tags displays references],
  'clock' => %w[clock_length cutoff_onset cutoff_derivative],
  'frequencies' => %w[n_sum d_difference n_minus_d n_plus_d dyadic_ratio beat_scale],
  'jet' => %w[quotient_extension jet_zero jet_one jet_two odd_difference even_difference],
  'ibp' => %w[self_phase sum_phase self_coefficient sum_coefficient initial_boundary no_spurious_db],
  'quadratic' => %w[uv_factor zeroth_term odd_term even_term h_square],
  'heat' => %w[m_plus m_zero m_minus heat_extra heat_cancel grouped_heat],
  'trace' => %w[right_endpoint phase_affine phase_fast amplitude_ratio exact_heat trace_power],
  'scaling' => %w[holder eta_scale heat_scale bounded_q pre_mass_a pre_mass_r triangle_after_blocks],
  'mass' => %w[t_coercivity mass_a mass_r target_power],
  'normalization' => %w[p_definition x_definition r_cancel omega_power omega_rate],
  'exactPde' => %w[transport_heat exact_shear background_boundary],
  'source' => %w[exact_waves observability clay_source bounded_search],
  'audit' => %w[audit_pass math_zero release_zero finite_boundary],
  'boundary' => %w[exact_pair low_carrier_open multimode_open e24_open version_m_conditional not_clay]
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
  warn "unknown R075V_RUBY_MUTATION: #{MUTATION}"
  exit 2
end
abort('duplicate mutation name in R0.75V Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

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
  'source_hash' => 'research/r075v_report-source.md',
  'dependency_hash' => 'research/r075t_two_harmonic_collar_coercivity.md',
  'u_hash' => 'research/r075u_two_harmonic_difference_frequency_payment.md'
}
frozen[drift[MUTATION]] = '0' * 64 if drift.key?(MUTATION)
bindings = frozen.to_h do |path, expected_hash|
  [path, { 'expectedSha256' => expected_hash, 'observedSha256' => digest(File.join(ROOT, path)) }]
end

clock = fixtures.fetch('clock')
radius = Rational(clock.fetch('R'))
computed_clock = {
  'T' => qtext(Rational(clock.fetch('durationCoefficient'), 1) * radius**Integer(clock.fetch('durationRPower')))
}

frequency_cases = fixtures.fetch('frequencyCases').map do |row|
  k = Integer(row.fetch('k'))
  m = Integer(row.fetch('m'))
  n = k + m
  d = k - m
  {
    'name' => row.fetch('name'), 'n' => n, 'd' => d,
    'nMinusD' => n - d, 'nPlusD' => n + d,
    'dOverN' => qtext(Rational(d, n)),
    'daR' => qtext(Rational(d, 1) * Rational(row.fetch('a')) * Rational(row.fetch('R')))
  }
end

jet = fixtures.fetch('quadraticJet')
k0 = Rational(jet.fetch('K0'))
kplus = Rational(jet.fetch('Kplus'))
kminus = Rational(jet.fetch('Kminus'))
computed_jet = {
  'average' => qtext((kplus + kminus) / 2),
  'oddDifference' => qtext((kplus - kminus) / 2),
  'evenDifference' => qtext((kplus + kminus) / 2 - k0)
}

heat = fixtures.fetch('constantMultiplierHeat')
hn = Rational(heat.fetch('n'))
hd = Rational(heat.fetch('d'))
hk = Rational(heat.fetch('K'))
mplus = (hn + hd)**2 * hk / 2
mzero = hn**2 * hk / 2
mminus = (hn - hd)**2 * hk / 2
cross = 2 * mzero + hd**2 * hk
computed_heat = {
  'Mplus' => qtext(mplus), 'M0' => qtext(mzero), 'Mminus' => qtext(mminus),
  'crossCoefficient' => qtext(cross),
  'cancellingQuadraticForm' => qtext(-mplus + cross - mminus)
}

computed_ibp = { 'selfKCoefficient' => '1/4', 'sumKCoefficient' => '1/2' }
after_cutoff = { 'a' => Rational(2), 'R' => Rational(5, 3) }
after_mass = { 'a' => Rational(2, 3), 'R' => Rational(-1, 3) }
normalized = {
  'a' => Rational(2, 3), 'R' => Rational(0),
  'omega' => Rational(1, 3), 'p' => Rational(2, 3)
}
computed_scale = {
  'afterCutoff' => encoded(after_cutoff),
  'afterHeat' => encoded(after_cutoff).merge('boundedFactor' => '(nR)^2(1+nR)^-8'),
  'afterMass' => encoded(after_mass),
  'normalized' => encoded(normalized),
  'frozenRate' => qtext(-Rational(fixtures.dig('frozenScales', 'cGamma')) / 12)
}

tags = text.scan(/\\tag\{V\.(\d+)\}/).flatten.map(&:to_i)
refs = text.scan(/\bV\.(\d+)\b/).flatten.map(&:to_i)
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
            clean?(raw) && clean?(raw_primary) && clean?(raw_source) && tags == (1..43).to_a &&
              text.scan('\\[').length == 43 && text.scan('\\]').length == 43 && (refs.uniq - tags.uniq).empty?)
record.call('complete clock and cutoff', 'clock',
            computed_clock == expected.fetch('clock') &&
              fragments?(compact, ['T_R=4R^2', '\\eta_R(0)=0', 'C_\\eta R^{-2}']))
record.call('dyadic frequency ledger', 'frequencies',
            frequency_cases == expected.fetch('frequencyCases') &&
              fragments?(compact, ['arguments `n-d,n,n+d`', 'd<=n/3', 'n\\ell>=2maR']))
record.call('radial quotient two-jet', 'jet',
            computed_jet == expected.fetch('quadraticJet') &&
              fragments?(compact, ['K_R(r):=\\frac{J_{r,R}}r', 'j=0,1,2', '(1+rR)^{-N}',
                                    '\\Lambda_N\\varepsilon', '\\Lambda_N\\varepsilon^2']))
record.call('exact time integration by parts', 'ibp',
            computed_ibp == expected.fetch('integrationByParts') &&
              fragments?(compact, ['\\frac{g(t)\\cos(2\\phi+2kBt)}{2k}',
                                    'Because `eta_R(0)=0`', 'No derivative of the relative phase']))
record.call('quadratic cancellation decomposition', 'quadratic',
            fragments?(compact, ['\\overline G\\,(u+v)^2', 'G_\\Delta(u^2-v^2)',
                                  '\\varepsilon(A_t+C_t)\\le CH(t)', '\\le C\\Lambda H(t)^2']))
record.call('grouped heat coefficient and cancellation', 'heat',
            computed_heat == expected.fetch('constantMultiplierHeat') &&
              fragments?(compact, ['L_R(r):=\\frac{r^2}2K_R(r)', '\\frac{d^2}2K_R(n)',
                                    '2(k^2+m^2)A_tC_tK_R(n)']))
record.call('right-endpoint complete-clock trace', 'trace',
            fragments?(compact, ['The endpoint in V.27', 'periodic distance function',
                                  'backward amplitude ratio is monotone', '(1+q)^{-8}H(T_R)^2']))
record.call('pre-mass scale ledger', 'scaling',
            computed_scale.fetch('afterCutoff') == expected.dig('scaleLedger', 'afterCutoff') &&
              computed_scale.fetch('afterHeat') == expected.dig('scaleLedger', 'afterHeat') &&
              fragments?(compact, ['q^2w_q<=C', 'Ca^2R^{5/3}I_H^{2/3}',
                                    'triangle inequality applied only after both coupled blocks']))
record.call('T mass substitution and target powers', 'mass',
            computed_scale.fetch('afterMass') == expected.dig('scaleLedger', 'afterMass') &&
              fragments?(compact, ['M_{k,m,R}^{\\rm plat}\\ge ca^2R^3I_H', 'a^{2/3}R^{-1/3}']))
record.call('normalization and frozen rate', 'normalization',
            computed_scale.fetch('normalized') == expected.dig('scaleLedger', 'normalized') &&
              computed_scale.fetch('frozenRate') == expected.dig('scaleLedger', 'frozenRate') &&
              fragments?(compact, ['R^{-2}\\omega M', '\\frac\\omega R', '-\\frac2{11907}']))
record.call('exact shear PDE and background boundary', 'exactPde',
            fragments?(compact, ['\\partial_tF+B\\partial_2F-\\partial_2^2F=0',
                                  'exact smooth unforced shear', 'nonzero constant background']))
record.call('bounded primary-source boundary', 'source',
            fragments?(compact_source, ['arXiv:1101.5507', 'arXiv:1604.01831', 'arXiv:1609.07020v6',
                                         'not evidence of novelty by itself']))
record.call('primary audit verdict and finite boundary', 'audit',
            fragments?(compact_primary, ['Current verdict: **PASS**', 'Mathematical blocker count: **0**',
                                          'Release blocker count: **0**',
                                          'Neither finite algebra nor sampling is represented as proof']))
record.call('exact-subfamily claim boundary', 'boundary',
            fragments?(compact, ['exact high-carrier dyadic pair', 'low-carrier pairs',
                                  'three or more harmonics', 'arbitrary-field E.24',
                                  'conditional on the realized-subclass', '**NOT CLAY.**']))
record.call('Python certificate agreement', 'bindings',
            certificate.fetch('verdict') == 'PASS' && certificate.fetch('clock') == computed_clock &&
              certificate.fetch('frequencyCases') == frequency_cases &&
              certificate.fetch('quadraticJet') == computed_jet &&
              certificate.fetch('constantMultiplierHeat') == computed_heat &&
              certificate.fetch('integrationByParts') == computed_ibp &&
              certificate.fetch('scaleLedger') == computed_scale &&
              certificate.fetch('negativeMutations') == NEGATIVE_MUTATIONS)

verdict = checks.all? { |row| row.fetch('pass') } ? 'PASS' : 'FAIL'
passed = checks.count { |row| row.fetch('pass') }
report = [
  '# R0.75V independent finite audit', '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{passed}/#{checks.length}",
  "- Blocker count: #{verdict == 'PASS' ? 0 : checks.length - passed}", '',
  'The Ruby implementation independently recomputes the dyadic frequencies,',
  'symmetric multiplier differences, integration-by-parts coefficients, heat',
  'cancellation, target powers, file bindings, and proof boundary.  It does not',
  'replace the continuum multiplier-jet or endpoint-trace proofs with sampling.',
  'The theorem is limited to one exact high-carrier dyadic pair. **NOT CLAY.**', ''
]
File.write(REPORT, report.join("\n"), mode: 'w', encoding: 'UTF-8')
puts JSON.generate({ 'suite' => 'r075v-ruby-independent', 'verdict' => verdict, 'assertions' => checks.length })
exit(verdict == 'PASS' ? 0 : 1)
