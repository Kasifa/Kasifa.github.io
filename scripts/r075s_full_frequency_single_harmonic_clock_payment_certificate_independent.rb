#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed exact audit for frozen R0.75S.

require 'digest'
require 'json'

ROOT = File.expand_path('..', __dir__)
STEM = 'r075s_full_frequency_single_harmonic_clock_payment'
MAIN = File.join(ROOT, 'research', "#{STEM}.md")
PRIMARY = File.join(ROOT, 'research', "#{STEM}_primary_audit.md")
SOURCE = File.join(ROOT, 'research', 'r075s_report-source.md')
FIXTURES = File.join(ROOT, 'scripts', "#{STEM}_fixtures.json")
EXPECTED = File.join(ROOT, 'scripts', "#{STEM}_expected.json")
CERT = ENV.fetch('R075S_JSON', File.join(ROOT, 'research', "#{STEM}_certificate.json"))
REPORT = ENV.fetch('R075S_RUBY_REPORT', File.join(ROOT, 'research', "#{STEM}_independent_audit.md"))
MUTATION = ENV.fetch('R075S_RUBY_MUTATION', '')

FROZEN = {
  'research/r075s_full_frequency_single_harmonic_clock_payment.md' =>
    'd2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd',
  'research/r075s_full_frequency_single_harmonic_clock_payment_primary_audit.md' =>
    '38e2bc95b5785b97df5d85474f3ed6105458a117249710b2c052cebbd769b5eb',
  'research/r075s_report-source.md' =>
    'ab9771e732204f28d3493ae9db73e7aa62aa980cc15b69dfefb39f226520b2a7',
  'research/r075b_bulk_clock_outer_padding_gate.md' =>
    '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075q_spatially_spread_harmonic_collar_payment.md' =>
    '9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' =>
    'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3'
}.freeze
FIXTURES_SHA256 = '82874592703552c1639c69066ddbf1ab531c135cd92eeae775c20be66cd8260f'
EXPECTED_SHA256 = 'e806089d4649b73649edeed5c0204b81a42dbef79c758283b128ec49a57abd8b'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash dependency_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema],
  'integrity' => %w[utf8 controls tags displays references],
  'clock' => %w[clock_length clock_scaling cutoff_variation],
  'fluxIdentity' => %w[odd_cross_section constant_cancel cosine_cancel phase_factor],
  'radialRows' => %w[radial_low radial_l1 radial_tail radial_r_scale],
  'nodeGeometry' => %w[fiber node_lower plateau_mass],
  'smallPhase' => %w[small_sigma_moment small_sigma_holder node_distance],
  'largePhase' => %w[large_sigma_moment bv_total phase_ibp],
  'lowSplit' => %w[epsilon_split lambda_bound low_flux low_mass],
  'lowLedger' => %w[low_two_thirds low_target low_amplitude],
  'highMass' => %w[phase_uniform heat_time high_mass_power],
  'highPhase' => %w[zero_shear high_bv one_over_k],
  'highQBelow' => %w[q_lower radial_below target_below],
  'highQAbove' => %w[radial_above time_above power_compare],
  'coverage' => %w[epsilon_overlap q_overlap all_integer_k],
  'normalization' => %w[p_definition x_definition r_cancel omega_rate],
  'exactPde' => %w[divergence transport nonlinear laplacian pressure],
  'sourceBoundary' => %w[source_primary source_observation source_no_import source_search_limit],
  'auditBoundary' => %w[audit_pass audit_math_zero audit_release_zero audit_alias_warning],
  'claimBoundary' => %w[single_harmonic multimode_open version_m_conditional e24_open not_clay]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

def digest(path)
  Digest::SHA256.file(path).hexdigest
end

def flat(text)
  text.gsub(/\s+/, ' ')
end

def clean?(bytes)
  value = bytes.dup.force_encoding(Encoding::UTF_8)
  value.valid_encoding? && bytes.bytes.none? { |b| (b < 32 && ![9, 10, 13].include?(b)) || b == 127 }
end

def all_fragments?(text, fragments)
  fragments.all? { |fragment| text.include?(fragment) }
end

def rational_text(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  warn "unknown R075S_RUBY_MUTATION: #{MUTATION}"
  exit 2
end
abort('duplicate mutation name in R0.75S Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

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
  'source_hash' => 'research/r075s_report-source.md',
  'dependency_hash' => 'research/r075q_spatially_spread_harmonic_collar_payment.md'
}
frozen[drift[MUTATION]] = '0' * 64 if drift.key?(MUTATION)
bindings = {}
frozen.each do |path, expected_hash|
  bindings[path] = {
    'expectedSha256' => expected_hash,
    'observedSha256' => digest(File.join(ROOT, path))
  }
end

clock = fixtures.fetch('clock')
radius = Rational(clock.fetch('R'))
time = Rational(clock.fetch('durationCoefficient'), 1) * radius**Integer(clock.fetch('durationRPower'))
computed_clock = { 'T' => time.to_s }

regimes = fixtures.fetch('regimeCases').map do |row|
  a = Rational(row.fetch('a'), 1)
  r = Rational(row.fetch('R'))
  k = Integer(row.fetch('k'))
  q = k * r
  epsilon = a * q
  lambda = k * k * 4 * r * r
  regime = if epsilon.to_f <= 2 * Math::PI
             'low'
           elsif q <= 1
             'high-q-below-one'
           else
             'high-q-above-one'
           end
  {
    'name' => row.fetch('name'),
    'q' => rational_text(q),
    'epsilon' => rational_text(epsilon),
    'lambda' => rational_text(lambda),
    'regime' => regime
  }
end

variation_total = fixtures.fetch('variationLedger').values.map(&:to_i).sum
frozen_rate = -Rational(fixtures.dig('frozenScales', 'cGamma')) / 12
computed_ledger = {
  'lowTarget' => { 'A' => 2, 'a' => 2, 'R' => 3, 'J' => '2/3' },
  'amplitudeCancels' => true,
  'normalizedRExponent' => 0,
  'normalizedOmegaExponent' => '1/3'
}

tags = text.scan(/\\tag\{S\.(\d+)\}/).flatten.map(&:to_i)
refs = text.scan(/S\.(\d+)/).flatten.map(&:to_i)
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
            clean?(raw) && clean?(raw_primary) && clean?(raw_source) && tags == (1..41).to_a &&
              text.scan('\\[').length == text.scan('\\]').length && (refs.uniq - tags.uniq).empty?)
record.call('complete clock arithmetic and cutoff variation', 'clock',
            computed_clock == expected.fetch('clock') &&
              all_fragments?(compact, ['T_R:=t_2-s_R=4R^2', 'nondecreasing', 'total variation is at most one']))
record.call('exact odd radial flux identity', 'fluxIdentity',
            all_fragments?(compact, ['D_R(y):=', '=-2\\pi y\\vartheta(|y|/R-a)', 'It is odd',
                                     'constant and cosine rows vanish', '\\frac{A^2B S_{k,R}}4',
                                     '\\sin(2\\phi+2kBt)']))
record.call('three radial coefficient bounds', 'radialRows',
            all_fragments?(compact, ['q:=kR', '\\varepsilon:=kaR=aq', '-2\\pi R^2',
                                     '\\min\\{\\varepsilon,1,q^{-N}\\}', 'integrations by parts']))
record.call('rectangular subcollar node lower bound', 'nodeGeometry',
            all_fragments?(compact, ['|x_2|\\le aR/4', '\\ge4\\delta_0R',
                                     '|\\cos(\\varepsilon z-\\psi)|^3', 'Q_\\varepsilon(\\psi)^3',
                                     '\\ge c\\,a^2R^3Q_\\varepsilon(\\psi)^3']))
record.call('small phase-speed branch', 'smallPhase',
            all_fragments?(compact, ['For `|sigma|<=1`', 'J^{1/3}\\ge c\\min',
                                     '|sin(2psi)|<=2Q_epsilon(psi)', 'C|\\sigma|J^{1/3}\\le CJ^{2/3}']))
record.call('large phase-speed BV branch', 'largePhase',
            variation_total == expected.fetch('variationTotal') &&
              all_fragments?(compact, ['For `|sigma|>=1`', 'J>=c', 'for every `lambda>=0`',
                                       '\\operatorname {Var}_{[0,1]}w', '\\le2', 'integration by parts']))
record.call('low-frequency split and bounds', 'lowSplit',
            regimes == expected.fetch('regimeCases') &&
              all_fragments?(compact, ['\\varepsilon=kaR\\le2\\pi', '\\lambda:=k^2T_R=4q^2',
                                       '\\le\\frac{16\\pi^2}{a^2}\\le1', 'CA^2a^2R^3']))
record.call('low-frequency power ledger', 'lowLedger',
            computed_ledger == expected.fetch('powerLedger') &&
              all_fragments?(compact_primary, ['a^{2/3}R^{-1/3}M^{2/3}',
                                               'A^2a^2R^3J^{2/3}', 'T_R=4R^2']))
record.call('high-frequency phase-uniform mass', 'highMass',
            all_fragments?(compact, ['\\varepsilon=kaR\\ge2\\pi', 'for every }\\psi',
                                     '\\min\\{T_R,k^{-2}\\}', 'phase-uniform plateau estimate Q.19']))
record.call('high-frequency BV phase cancellation', 'highPhase',
            all_fragments?(compact, ['If `B=0`, the flux vanishes', 'Its total variation is at most two',
                                     '\\le\\frac Ck', '\\le CA^2\\frac{|S_{k,R}|}{k}']))
record.call('high regime q below one', 'highQBelow',
            all_fragments?(compact, ['If `q<=1`', '`q>=2pi/a`', 'CaR^3q^{-1}\\le Ca^2R^3',
                                     'min{T_R,k^(-2)}>=cR^2']))
record.call('high regime q above one', 'highQAbove',
            all_fragments?(compact, ['If `q>=1`', 'CaR^3q^{-2}', 'R^2q^{-2}',
                                     'q^(-2)<=q^(-4/3)', 'a<=a^2']))
record.call('frequency coverage', 'coverage',
            all_fragments?(compact_primary, ['overlaps at `epsilon=2pi`', 'overlap at `q=1`',
                                             'every integer `k>=1` is covered']))
record.call('normalization and exact frozen rate', 'normalization',
            frozen_rate == Rational(expected.fetch('frozenRate')) &&
              all_fragments?(compact, ['p_{k,R}^{\\rm plat}:=R^{-2}\\omega',
                                       '\\frac\\omega R[\\mathcal T_{k,R}]_+',
                                       'a^{2/3}\\omega^{1/3}', '=-\\frac{c_\\gamma}{12}<0']))
record.call('exact smooth Navier-Stokes shear', 'exactPde',
            all_fragments?(compact, ['u_k(t,x)=(0,B,F_k(t,x_2))', 'div u_k=0',
                                     '(u_k\\!\\cdot\\nabla)u_k=(0,0,B\\partial_2F_k)',
                                     '\\Delta u_k=(0,0,\\partial_2^2F_k)', 'constant pressure']))
record.call('bounded primary-source boundary', 'sourceBoundary',
            all_fragments?(compact_source, ['arXiv:1604.01831', 'arXiv:2103.07906',
                                            'arXiv:1609.07020', 'arXiv:1711.04279',
                                            'No external theorem is imported',
                                            'search boundary, not a novelty or priority claim']))
record.call('primary audit status and alias warning', 'auditBoundary',
            all_fragments?(compact_primary, ['Current verdict: **PASS**',
                                             'Mathematical blocker count: **0**',
                                             'Release blocker count: **0**',
                                             'does not authorize publication', 'can alias the oscillation']))
record.call('claim and route boundary', 'claimBoundary',
            all_fragments?(compact, ['including all frequencies omitted by Q', 'not a multimode estimate',
                                     'not asserted for a Fourier projection', 'arbitrary-field E.24',
                                     'complete Version-M clock extraction', 'No novelty or priority claim',
                                     '\\mathbf{NOT\\ CLAY}']))
record.call('Python mutation inventory parity', 'inputs',
            certificate.fetch('negativeMutations') == NEGATIVE_MUTATIONS)
record.call('Python canonical certificate is PASS', 'bindings',
            certificate.fetch('verdict') == 'PASS' && certificate.fetch('assertions') == 21)

verdict = checks.all? { |row| row.fetch('pass') } ? 'PASS' : 'FAIL'
lines = [
  '# R0.75S independent exact audit', '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{checks.count { |row| row.fetch('pass') }}/#{checks.length}",
  "- Blocker count: #{checks.count { |row| !row.fetch('pass') }}",
  "- Mutation: `#{MUTATION.empty? ? 'none' : MUTATION}`", '',
  "- Failed rows: `#{checks.reject { |row| row.fetch('pass') }.map { |row| row.fetch('name') }.join(', ')}`", '',
  '## Independent rows', '',
  "- Complete clock: `#{computed_clock}`.",
  "- Regime fixtures: `#{regimes.to_json}`.",
  "- BV total: `#{variation_total}`.",
  "- Frozen rate: `#{frozen_rate}`.",
  "- Power ledger: `#{computed_ledger.to_json}`.", '',
  'The independent implementation checks exact rational scale arithmetic, source bindings,',
  'formula structure, analytic branch markers, and the explicit aliasing warning. It does',
  'not turn finite fixtures into a proof of the continuum phase lemma.', '',
  'The certified result remains one real constant-drift harmonic. Multimode interference,',
  'nonconstant shear, E.24, complete Version-M extraction, fixed deletion, suitable-weak',
  'transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
]
File.write(REPORT, lines.join("\n") + "\n")
puts JSON.generate({ 'verdict' => verdict, 'assertions' => checks.length,
                     'failed' => checks.reject { |row| row.fetch('pass') }.map { |row| row.fetch('name') },
                     'mutation' => MUTATION.empty? ? nil : MUTATION })
exit(verdict == 'PASS' ? 0 : 1)
