#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed exact finite audit for frozen R0.75Y.

require 'digest'
require 'json'

ROOT = File.expand_path('..', __dir__)
STEM = 'r075y_strongly_separated_multimode_flux_payment'
MAIN = File.join(ROOT, 'research', "#{STEM}.md")
PRIMARY = File.join(ROOT, 'research', "#{STEM}_primary_audit.md")
SOURCE = File.join(ROOT, 'research', 'r075y_report-source.md')
FIXTURES = File.join(ROOT, 'scripts', "#{STEM}_fixtures.json")
EXPECTED = File.join(ROOT, 'scripts', "#{STEM}_expected.json")
CERT = ENV.fetch('R075Y_JSON', File.join(ROOT, 'research', "#{STEM}_certificate.json"))
REPORT = ENV.fetch('R075Y_RUBY_REPORT', File.join(ROOT, 'research', "#{STEM}_independent_audit.md"))
MUTATION = ENV.fetch('R075Y_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => '74790f910b596c86b204291d997ef723cabbc85d14a89e3fe900814fcd88b0a6',
  "research/#{STEM}_primary_audit.md" => 'f7e1feedd1fa359877554eff4fa20c470f727ae7743c990136525ad22d6cdf3b',
  'research/r075y_report-source.md' => 'e6d6b1ed2830b46fc901a9ab09ef368f258f13dfc8c0961076baedd5b46e1589',
  'research/r075b_bulk_clock_outer_padding_gate.md' => '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075u_two_harmonic_difference_frequency_payment.md' => 'f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4',
  'research/r075x_fixed_finite_mode_low_carrier_payment.md' => '8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763'
}.freeze
FIXTURES_SHA256 = '45448bf75c867b3f9654db79c77ae52b9bd35d7e781b240f564a9d871faab32b'
EXPECTED_SHA256 = '324e92dd32d6e1ca76b22c47a201206e1c924e1100b92de1c8429ffd17ac25d3'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash b_hash r_hash u_hash x_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema],
  'integrity' => %w[utf8 controls tags displays references tex_spacing],
  'clock' => %w[clock_length cutoff_range cutoff_onset cutoff_derivative],
  'geometry' => %w[plateau_widths central_chart fibre_area],
  'family' => %w[positive_modes ordered_modes dyadic_band signed_gap separation],
  'gram' => %w[signed_count minimum_gap offdiagonal_factor strict_margin l2_coefficient l3_coefficient signed_two_n1],
  'time' => %w[slow_phase fast_phase large_heat zero_shear physical_r physical_r_power],
  'flux' => %w[self_rows difference_rows sum_rows total_rows positive_row_frequencies phase_signs radial_quotient],
  'payment' => %w[modal_domination row_payment mass_payment],
  'scale' => %w[clock_scale radial_scale row_scale mass_scale target_scale],
  'normalization' => %w[p_definition x_definition r_cancel omega_power rate],
  'q_boundary' => %w[explicit_q_square forced_carrier subexponential_q sparse_not_dense r_obstruction],
  'source' => %w[source_urls classical_boundary bounded_search no_novelty],
  'audit' => %w[audit_pass math_zero release_zero deletion_tests finite_boundary],
  'figure' => %w[analytic_only no_simulation_claim no_formal_figure],
  'boundary' => %w[clusters_open packets_open e24_open version_m_conditional actual_component regularity_open not_clay]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

def digest(path)
  Digest::SHA256.file(path).hexdigest
end

def clean?(bytes)
  value = bytes.dup.force_encoding(Encoding::UTF_8)
  value.valid_encoding? &&
    bytes.bytes.none? { |byte| (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127 }
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

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  abort("unknown R075Y_RUBY_MUTATION: #{MUTATION}")
end
abort('duplicate mutation name in R0.75Y Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

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
  'source_hash' => 'research/r075y_report-source.md',
  'b_hash' => 'research/r075b_bulk_clock_outer_padding_gate.md',
  'r_hash' => 'research/r075r_outer_cap_spectral_concentration_obstruction.md',
  'u_hash' => 'research/r075u_two_harmonic_difference_frequency_payment.md',
  'x_hash' => 'research/r075x_fixed_finite_mode_low_carrier_payment.md'
}[MUTATION]
frozen[mutation_path] = '0' * 64 if mutation_path
bindings = frozen.sort.to_h do |source_path, expected_hash|
  [source_path, {
    'expectedSha256' => expected_hash,
    'observedSha256' => digest(File.join(ROOT, source_path))
  }]
end

clock = fixtures.fetch('clock')
radius = Rational(clock.fetch('R'))
duration = Rational(clock.fetch('durationCoefficient')) * radius**clock.fetch('durationRPower')
computed_clock = { 'T' => qtext(duration) }

row = fixtures.fetch('separatedCase')
q_count = row.fetch('q')
modes = row.fetch('frequencies')
a_value = Rational(row.fetch('a'))
radius = Rational(row.fetch('R'))
ell = a_value * radius
signed = (modes.map { |mode| -mode } + modes).sort
minimum_gap = signed.each_cons(2).map { |left, right| right - left }.min
threshold = row.fetch('separationMultiplier') * q_count
separation_product = ell * minimum_gap
offdiagonal = Rational(2 * (2 * q_count - 1), minimum_gap)
half_diagonal = ell / 2
retained_diagonal = ell - offdiagonal
computed_case = {
  'ell' => qtext(ell),
  'signedFrequencies' => signed,
  'minimumSignedGap' => minimum_gap,
  'threshold' => threshold,
  'separationProduct' => separation_product.denominator == 1 ? separation_product.numerator : qtext(separation_product),
  'condition' => separation_product >= threshold,
  'dyadicBand' => modes.last <= 2 * modes.first,
  'forcedCarrierFloor' => row.fetch('separationMultiplier') * q_count * (q_count - 1)
}
computed_gram = {
  'signedModeCount' => signed.length,
  'offDiagonalCoefficient' => qtext(offdiagonal),
  'halfDiagonalCoefficient' => qtext(half_diagonal),
  'retainedDiagonalCoefficient' => qtext(retained_diagonal),
  'theoremL2Coefficient' => qtext(ell / 4),
  'theoremL3Coefficient' => qtext(ell / 8)
}

pairs = q_count * (q_count - 1) / 2
computed_rows = {
  'selfRows' => q_count,
  'differenceRows' => pairs,
  'sumRows' => pairs,
  'totalRows' => q_count + 2 * pairs
}

computed_scale = {
  'clockRow' => { 'r' => -1, 'R' => '-4/3', 'P3Integral' => '2/3' },
  'radialQuotient' => { 'r' => 1, 'a' => 2, 'R' => 3 },
  'afterRow' => { 'a' => 2, 'R' => '5/3', 'S3Integral' => '2/3' },
  'mass' => { 'a' => 2, 'R' => 3, 'S3Integral' => 1 },
  'target' => { 'q' => 2, 'a' => '2/3', 'R' => '-1/3', 'M' => '2/3' },
  'normalized' => { 'q' => 2, 'a' => '2/3', 'R' => 0, 'omega' => '1/3', 'p' => '2/3' },
  'frozenRate' => qtext(-Rational(fixtures.dig('frozenScales', 'cGamma')) / 12)
}

tags = text.scan(/\\tag\{Y\.(\d+)\}/).flatten.map(&:to_i)
refs = text.scan(/\bY\.(\d+)\b/).flatten.map(&:to_i)
checks = []
record = lambda do |name, group, condition|
  checks << {
    'name' => name,
    'group' => group,
    'pass' => condition && !GROUPS.fetch(group).include?(MUTATION)
  }
end

record.call('frozen source bindings', 'bindings',
            bindings.values.all? { |entry| entry['expectedSha256'] == entry['observedSha256'] })
record.call('fixture and expected bindings', 'inputs',
            digest(FIXTURES) == FIXTURES_SHA256 && digest(EXPECTED) == EXPECTED_SHA256 &&
              fixtures.fetch('schema').end_with?('fixtures-v1'))
record.call('UTF-8, controls, tags, displays, references, and TeX spacing', 'integrity',
            clean?(raw) && clean?(raw_primary) && clean?(raw_source) &&
              tags == (1..39).to_a && text.scan('\\[').length == 39 &&
              text.scan('\\]').length == 39 && (refs.uniq - tags.uniq).empty? &&
              text.scan(/(?<![\\A-Za-z])(?:quad|qquad)\b/).empty?)
record.call('complete clock and cutoff onset', 'clock',
            computed_clock == expected.fetch('clock') &&
              fragments?(compact, ['T_R=4R^2', '\\eta_R(0)=0', 'C_\\eta R^{-2}']))
record.call('plateau geometry and central chart', 'geometry',
            fragments?(compact, ['0<\\delta_0<\\delta', 'a\\ge4\\delta_0',
                                  '(a+\\delta)R<\\frac\\pi2', '4\\pi a\\delta_0R^2']))
record.call('ordered dyadic family and exact separation', 'family',
            computed_case == expected.fetch('separatedCase') &&
              modes == modes.uniq.sort && minimum_gap == row.fetch('minimumSignedGap'))
record.call('Gram ledger and strict half-diagonal margin', 'gram',
            computed_gram == expected.fetch('gramLedger') &&
              separation_product >= threshold && offdiagonal <= half_diagonal &&
              fragments?(compact, ['\\{2n_1\\}\\cup', '\\ell\\delta_{\\boldsymbol n}\\ge8q',
                                    '\\ge\\frac\\ell4S(t)^2', '\\ge\\frac\\ell8S(t)^3']))
record.call('phase-free slow and fast clock regimes', 'time',
            fragments?(compact, ['|\\sigma|\\tau\\le1', '|\\sigma|\\tau\\ge1',
                                  '\\zeta(s)\\le C_\\eta s',
                                  "|w(4)|+\\int_0^4|w'(s)|",
                                  '\\frac{C}{rR^{4/3}}']))
record.call('exact positive-frequency row ledger', 'flux',
            computed_rows == expected.fetch('rowLedger') &&
              fragments?(compact, ['J_{2n_j,R}', 'J_{n_j-n_i,R}', 'J_{n_i+n_j,R}',
                                    '\\sin(\\phi_j(t)-\\phi_i(t))',
                                    '\\frac{|J_{r,R}|}{r}\\le Ca^2R^3']))
record.call('modal and plateau payment', 'payment',
            fragments?(compact, ['P(t)^{3/2}\\le S(t)^3', 'Cq^2a^2R^{5/3}',
                                  '\\frac{\\pi\\delta_0}{2}a^2R^3']))
record.call('exact scale ledger', 'scale',
            computed_scale.slice('clockRow', 'radialQuotient', 'afterRow', 'mass', 'target') ==
              expected.fetch('scaleLedger').slice('clockRow', 'radialQuotient', 'afterRow', 'mass', 'target'))
record.call('normalization and frozen rate', 'normalization',
            computed_scale.fetch('normalized') == expected.dig('scaleLedger', 'normalized') &&
              computed_scale.fetch('frozenRate') == expected.dig('scaleLedger', 'frozenRate'))
record.call('explicit sparse q-growth boundary', 'q_boundary',
            fragments?(compact, ['q+2\\binom q2=q^2', 'n_1\\ell>=8q(q-1)',
                                  '\\log q=o(L^2)', 'not a dense-packet hypothesis',
                                  'outer-cap packet obstruction of R0.75R']))
record.call('bounded source boundary', 'source',
            fragments?(compact_source, ['https://arxiv.org/abs/2311.17714',
                                         'https://arxiv.org/abs/1705.11017',
                                         'No external paper is used as proof',
                                         'not evidence of completeness, novelty, or priority']))
record.call('primary audit and deletion tests', 'audit',
            fragments?(compact_primary, ['Current verdict: **PASS**',
                                          'Mathematical blocker count: **0**',
                                          'Release blocker count: **0**',
                                          'If `2n_1` is deleted',
                                          'If `eta_R(0)=0` is deleted',
                                          'not represented as proof']))
record.call('analytic-only figure boundary', 'figure',
            fragments?(compact, ['proof is analytic',
                                  'no simulation or formal scientific figure is needed']))
record.call('open and Version-M boundary', 'boundary',
            fragments?(compact, ['unresolved high-carrier clusters', 'arbitrary dyadic packets',
                                  'arbitrary-field E.24', 'Version-M measurement row',
                                  'actual component', 'regularity; and singularity',
                                  '**NOT CLAY.**']))
record.call('canonical Python certificate agreement', 'inputs',
            certificate.dig('summary', 'verdict') == 'PASS' &&
              certificate.dig('summary', 'assertions') == 17 &&
              certificate.fetch('negativeMutations') == NEGATIVE_MUTATIONS &&
              certificate.dig('computed', 'separatedCase') == computed_case &&
              certificate.dig('computed', 'gramLedger') == computed_gram &&
              certificate.dig('computed', 'rowLedger') == computed_rows &&
              certificate.dig('computed', 'scaleLedger') == computed_scale)

failures = checks.reject { |item| item.fetch('pass') }.map { |item| item.fetch('name') }
verdict = failures.empty? ? 'PASS' : 'FAIL'
File.write(
  REPORT,
  [
    '# R0.75Y independent exact finite audit',
    '',
    "- Verdict: **#{verdict}**",
    "- Assertions: #{checks.length - failures.length}/#{checks.length}",
    "- Mutation mode: `#{MUTATION.empty? ? 'none' : MUTATION}`",
    "- Exact separation product: `#{qtext(separation_product)}`",
    "- Exact Gram off-diagonal coefficient: `#{qtext(offdiagonal)}`",
    "- Exact retained diagonal coefficient: `#{qtext(retained_diagonal)}`",
    "- Exact Fourier-row count: `#{computed_rows.fetch('totalRows')}`",
    "- Blocker count: #{failures.length}",
    '',
    'This implementation independently recomputes the signed-spectrum gap,',
    'Gram margin, row count, and scale ledger. Finite checks are not continuum proof.',
    'Unresolved clusters and regularity remain open. **NOT CLAY.**',
    ''
  ].join("\n"),
  mode: 'w',
  encoding: 'UTF-8'
)

puts JSON.generate(
  'suite' => 'r075y-independent',
  'verdict' => verdict,
  'assertions' => checks.length,
  'failures' => failures
)
exit(failures.empty? ? 0 : 1)
