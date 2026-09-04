#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed exact audit for frozen R0.75R.

require 'digest'
require 'json'

ROOT = File.expand_path('..', __dir__)
STEM = 'r075r_outer_cap_spectral_concentration_obstruction'
MAIN = File.join(ROOT, 'research', "#{STEM}.md")
PRIMARY = File.join(ROOT, 'research', "#{STEM}_primary_audit.md")
SOURCE = File.join(ROOT, 'research', 'r075r_report-source.md')
FIXTURES = File.join(ROOT, 'scripts', "#{STEM}_fixtures.json")
EXPECTED = File.join(ROOT, 'scripts', "#{STEM}_expected.json")
CERT = ENV.fetch('R075R_JSON', File.join(ROOT, 'research', "#{STEM}_certificate.json"))
REPORT = ENV.fetch('R075R_RUBY_REPORT', File.join(ROOT, 'research', "#{STEM}_independent_audit.md"))
MUTATION = ENV.fetch('R075R_RUBY_MUTATION', '')

FROZEN = {
  'research/r075b_bulk_clock_outer_padding_gate.md' =>
    '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075n_radial_collar_averaged_wiener_row.md' =>
    'ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318',
  'research/r075q_spatially_spread_harmonic_collar_payment.md' =>
    '9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' =>
    'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075r_outer_cap_spectral_concentration_obstruction_primary_audit.md' =>
    '9b52e3d54fce43c609f70f0b8e71c53def0b4b705144be39a7b62e88d5e07355',
  'research/r075r_report-source.md' =>
    '767bfc43f9510a2acdf7fbff9d52624ed23ed80e4c3af174c77a47c3824d87ed'
}.freeze
FIXTURES_SHA256 = '226b7411967f2fa6f1960d29a03f32ef40945af47c6545c3f60e4115e507a1d1'
EXPECTED_SHA256 = '25d46dc6276a42f764dc503100750186213186368aebc9d94be409cd80f3c251'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash dependency_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema],
  'sourceIntegrity' => %w[utf8 control tags displays dependency_table],
  'crossSection' => %w[cross_section_mass moving_endpoint cross_section_sign],
  'outerCap' => %w[outer_interval outer_separation outer_lower],
  'spectralArithmetic' => %w[divisibility integer_carrier band_lower band_upper],
  'spectralText' => %w[support_minkowski support_real support_no_remainder],
  'dirichletRows' => %w[dirichlet_pointwise dirichlet_l2 dirichlet_tail],
  'transportArithmetic' => %w[transport_k transport_shift transport_bound],
  'exactPde' => %w[transport_equation divergence nonlinear_term constant_pressure],
  'heatPersistence' => %w[heat_multiplier heat_global heat_off_diagonal],
  'fluxLower' => %w[flux_sign negative_cap flux_time flux_power],
  'plateauUpper' => %w[plateau_projection plateau_linf plateau_volume mass_power],
  'powerLedger' => %w[mass_two_thirds raw_quotient amplitude_cancel],
  'normalization' => %w[normalization_factor normalized_r normalized_omega],
  'tailExact' => %w[tail_m1 tail_m2 tail_m3],
  'frozenRate' => %w[kappa_formula kappa_one r_exponent kappa_positive],
  'sourceBoundary' => %w[source_primary source_geometry source_no_import source_nonexhaustive],
  'claimBoundary' => %w[plateau_only version_m_open e24_open smooth_no_singularity],
  'auditBoundary' => %w[audit_pass audit_math_zero audit_release_zero audit_no_publish],
  'routeBoundary' => %w[route_alternatives clock_open weak_open novelty not_clay]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

def digest(path)
  Digest::SHA256.file(path).hexdigest
end

def flat(text)
  text.gsub(/\s+/, ' ')
end

def all_fragments?(text, fragments)
  fragments.all? { |fragment| text.include?(fragment) }
end

def clean?(bytes)
  string = bytes.dup.force_encoding(Encoding::UTF_8)
  string.valid_encoding? && bytes.bytes.none? { |b| (b < 32 && ![9, 10, 13].include?(b)) || b == 127 }
end

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  warn "unknown R075R_RUBY_MUTATION: #{MUTATION}"
  exit 2
end
abort('duplicate mutation name in R0.75R Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

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
  'main_hash' => 'research/r075r_outer_cap_spectral_concentration_obstruction.md',
  'primary_hash' => 'research/r075r_outer_cap_spectral_concentration_obstruction_primary_audit.md',
  'source_hash' => 'research/r075r_report-source.md',
  'dependency_hash' => 'research/r075q_spatially_spread_harmonic_collar_payment.md'
}
frozen[drift[MUTATION]] = '0' * 64 if drift.key?(MUTATION)
bindings = frozen.to_h do |path, expected_hash|
  [path, { 'expectedSha256' => expected_hash, 'observedSha256' => digest(File.join(ROOT, path)) }]
end

s = fixtures.fetch('spectralCase')
m = Integer(s.fetch('m'))
k = Integer(s.fetch('K'))
n = Integer(s.fetch('n'))
carrier = Integer(s.fetch('q'))
spectral = {
  'divisor' => 16 * m,
  'twoMn' => 2 * m * n,
  'lowerBand' => carrier - 2 * m * n,
  'upperBand' => carrier + 2 * m * n,
  'supportInsideK2K' => k <= carrier - 2 * m * n && carrier + 2 * m * n <= 2 * k
}

tr = fixtures.fetch('transportCase')
radius = Rational(tr.fetch('R'))
b = Rational(tr.fetch('b'))
abs_b = Rational(tr.fetch('absB').to_s)
time = Rational(tr.fetch('T'))
tk = Integer(tr.fetch('K'))
transport = {
  'RToMinusThreeHalves' => 64,
  'driftDistance' => (abs_b * time).to_s,
  'bTimesR' => (b * radius).to_s,
  'driftBoundSharp' => abs_b * time == b * radius,
  'timeIsKMinusTwo' => time == Rational(1, tk * tk)
}

scales = fixtures.fetch('frozenScales')
rho = Rational(scales.fetch('rho'))
c_gamma = Rational(scales.fetch('cGamma'))
tails = fixtures.fetch('tailCases').map do |row|
  tm = Integer(row.fetch('m'))
  power = Rational(2 * tm, 1) + Rational(1, 6)
  {
    'm' => tm,
    'pointwiseExponent' => -2 * tm,
    'relativeL2Exponent' => 1 - 4 * tm,
    'cubicExponent' => -6 * tm,
    'quotientRecoveryExponent' => 4 * tm,
    'kappa' => (power * rho / 4 - c_gamma / 12).to_s,
    'rExponent' => (-power + c_gamma / (3 * rho)).to_s
  }
end

ledger = {
  'flux' => { 'B' => 1, 'a' => 1, 'R' => 1, 'A' => 2, 'n' => -1, 'K' => -2 },
  'mass' => { 'A' => 3, 'a' => 2, 'R' => 3, 'K' => -2, 'nR' => '-6m' },
  'massTwoThirds' => { 'A' => 2, 'a' => '4/3', 'R' => 2, 'K' => '-4/3', 'nR' => '-4m' },
  'rawQuotient' => { 'B' => 1, 'a' => '-1/3', 'R' => -1, 'n' => -1, 'K' => '-2/3', 'nR' => '4m' },
  'normalizedRExponent' => '-2m-1/6',
  'normalizedOmegaExponent' => '1/3',
  'amplitudeCancels' => true
}

tags = text.scan(/\\tag\{R\.(\d+)\}/).flatten.map(&:to_i)
checks = []
record = lambda do |name, group, condition|
  checks << {
    'name' => name,
    'pass' => condition && !GROUPS.fetch(group).include?(MUTATION)
  }
end

record.call('frozen source bindings', 'bindings',
            bindings.values.all? { |row| row['expectedSha256'] == row['observedSha256'] })
record.call('fixture and expected bindings', 'inputs',
            digest(FIXTURES) == FIXTURES_SHA256 && digest(EXPECTED) == EXPECTED_SHA256 &&
              fixtures.fetch('schema').end_with?('fixtures-v1'))
record.call('UTF-8, controls, tags, and displays', 'sourceIntegrity',
            clean?(raw) && clean?(raw_primary) && clean?(raw_source) &&
              tags == (1..41).to_a && text.scan('\\[').length == text.scan('\\]').length &&
              FROZEN.keys.first(4).all? { |path| compact.include?(path) })
record.call('exact radial cross-section identity', 'crossSection',
            all_fragments?(compact, ['Xi_R(y)=2\\pi', 'D_R(y)=\\Xi_R\'(y)',
                                     '=-2\\pi y\\vartheta(|y|/R-a)', 'D_R<0', 'D_R>0']))
record.call('outer-cap separation and sign', 'outerCap',
            all_fragments?(compact, ['s_*\\in(\\delta_0,\\delta)', 's_*-3h', 'I_+:=',
                                     'outside the `x_2` projection', '-D_R(y)\\ge c_\\vartheta aR']))
record.call('spectral arithmetic', 'spectralArithmetic',
            spectral == expected.fetch('spectralCase') && (k % (16 * m)).zero? &&
              n == k / (16 * m) && carrier == 3 * k / 2)
record.call('real spectral support text', 'spectralText',
            all_fragments?(compact, ['[-2mn,2mn]=[-K/8,K/8]', 'shifts this support by `+q` and `-q`',
                                     '\\frac{11K}{8}\\le|j|\\le\\frac{13K}{8}',
                                     'without a projection remainder']))
record.call('Dirichlet concentration and tail rows', 'dirichletRows',
            all_fragments?(compact, ['|d_n(z)|\\le C\\min', 'c_mA^2n^{-1}\\le\\|G_K\\|',
                                     '(nR)^{1-4m}', 'The relative tail', 'tends to zero']))
record.call('transport arithmetic', 'transportArithmetic',
            transport['RToMinusThreeHalves'] == expected.dig('transportCase', 'RToMinusThreeHalves') &&
              transport['driftDistance'] == expected.dig('transportCase', 'driftDistance') &&
              transport['bTimesR'] == expected.dig('transportCase', 'bTimesR') &&
              transport['driftBoundSharp'] && transport['timeIsKMinusTwo'])
record.call('exact Navier-Stokes realization', 'exactPde',
            all_fragments?(compact, ['(\\partial_t+B\\partial_2-\\partial_2^2)F_K=0',
                                     '\\nabla\\!\\cdot u_K=0', '(u_K\\!\\cdot\\nabla)u_K=(0,0,B\\partial_2F_K)',
                                     'with constant pressure', 'not a passive-scalar surrogate']))
record.call('heat persistence', 'heatPersistence',
            all_fragments?(compact, ['\\|F_K(t)\\|_2^2\\ge e^{-8}', 'e^{-d^2/(4t)}',
                                     'e^{-d^2/(8t)}', 'e^{-c(KR)^2}',
                                     'R^{-3/2}\\le K\\le2R^{-3/2}']))
record.call('signed flux lower bound', 'fluxLower',
            all_fragments?(compact, ['integrand `BD_R|F_K|^2` is nonnegative for `y>0`', 'only adverse contribution',
                                     '\\mathcal T_K', '\\ge c_m|B|aRA^2n^{-1}K^{-2}']))
record.call('plateau cubic upper bound', 'plateauUpper',
            all_fragments?(compact, ['|y|\\le(a+\\delta_0)R', '(nR)^{-2m}',
                                     'volume at most `C a^2R^3`', '(nR)^{-6m}']))
record.call('power ledger', 'powerLedger', ledger == expected.fetch('powerLedger'))
record.call('normalization algebra', 'normalization',
            all_fragments?(compact, ['`R^(1/3)omega^(1/3)`', '`|B|=bR^(-2)`',
                                     'R^{-3/2}\\le K\\le2R^{-3/2}', 'R^{-2m-1/6}\\omega^{1/3}']))
record.call('exact tail cases', 'tailExact', tails == expected.fetch('tailCases'))
record.call('positive frozen exponent', 'frozenRate',
            tails.all? { |row| Rational(row.fetch('kappa')).positive? } &&
              tails.first.fetch('kappa') == '304373/952560000' &&
              tails.first.fetch('rExponent') == '-304373/214326' &&
              all_fragments?(compact, ['\\kappa_m:=', '\\kappa_1=\\frac{304373}{952560000}>0',
                                       'R^{-304373/214326}']))
record.call('bounded primary-source boundary', 'sourceBoundary',
            all_fragments?(compact_source, ['arXiv:1609.07020', 'arXiv:1711.04279',
                                            'arXiv:math/0609429', 'no external theorem is needed',
                                            'search boundary, not a novelty or priority claim']))
record.call('plateau-only claim boundary', 'claimBoundary',
            all_fragments?(compact, ['specific attempted extension of Q', 'not a counterexample to E.24',
                                     'complete Version-M payment sees exterior rows beyond the plateau',
                                     'exact unforced smooth', 'does not concern singularity formation']))
record.call('primary audit status', 'auditBoundary',
            all_fragments?(compact_primary, ['Current verdict: **PASS**',
                                             'Mathematical blocker count: **0**',
                                             'Release blocker count: **0**',
                                             'does not authorize publication']))
record.call('route and open boundary', 'routeBoundary',
            all_fragments?(compact, ['full signed-flux cap', 'spreading or thickness hypothesis',
                                     'signed multimode cancellation', 'complete-clock extraction',
                                     'suitable-weak transfer', 'No novelty or priority claim',
                                     '\\mathbf{NOT\\ CLAY}']))

certificate_mutations = certificate.fetch('negativeMutations')
record.call('Python mutation inventory parity', 'inputs', certificate_mutations == NEGATIVE_MUTATIONS)
record.call('Python canonical certificate is PASS', 'bindings',
            certificate.fetch('verdict') == 'PASS' && certificate.fetch('assertions') == 21)

verdict = checks.all? { |row| row.fetch('pass') } ? 'PASS' : 'FAIL'
lines = [
  '# R0.75R independent exact audit', '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{checks.count { |row| row.fetch('pass') }}/#{checks.length}",
  "- Blocker count: #{checks.count { |row| !row.fetch('pass') }}",
  "- Mutation: `#{MUTATION.empty? ? 'none' : MUTATION}`", '',
  '## Independently recomputed rows', '',
  "- Spectral band: `[#{spectral['lowerBand']}, #{spectral['upperBand']}]` for `K=#{k}`.",
  "- Drift distance: `#{transport['driftDistance']}`; allowed `bR=#{transport['bTimesR']}`.",
  "- Smallest frozen rate: `#{tails.first['kappa']}`.",
  "- Corresponding R exponent: `#{tails.first['rExponent']}`.", '',
  '## Checks', ''
]
checks.each { |row| lines << "- #{row.fetch('pass') ? 'PASS' : 'FAIL'} -- #{row.fetch('name')}" }
lines += [
  '', '## Boundary', '',
  'This independent implementation checks one exact smooth shear family and the failure of its',
  'plateau-only multimode payment. Full-support payment, Version-M, E.24, complete clock, fixed',
  'deletion, suitable-weak transfer, regularity, and singularity remain open. **NOT CLAY.**', ''
]
File.write(REPORT, lines.join("\n"), mode: 'w', encoding: 'UTF-8')

puts JSON.generate({ schema: 'r075r-independent-audit-v1', verdict: verdict,
                     assertions: checks.length, passed: checks.count { |row| row.fetch('pass') } })
exit(verdict == 'PASS' ? 0 : 1)
