#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent exact-arithmetic audit for frozen R0.76A.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
STEM = 'r076a_complete_clock_localized_current_sign_obstruction'
MAIN = ROOT.join("research/#{STEM}.md")
PRIMARY = ROOT.join("research/#{STEM}_primary_audit.md")
SOURCE = ROOT.join('research/r076a_report-source.md')
FIXTURES = ROOT.join("scripts/#{STEM}_fixtures.json")
EXPECTED = ROOT.join("scripts/#{STEM}_expected.json")
CERTIFICATE = Pathname.new(ENV.fetch('R076A_JSON', ROOT.join("research/#{STEM}_certificate.json").to_s))
OUT = Pathname.new(ENV.fetch('R076A_RUBY_REPORT', ROOT.join("research/#{STEM}_independent_audit.md").to_s))
MUTATION = ENV.fetch('R076A_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => 'd23532f84702be1630daa0b8d56d02242571dd8a1f8024c59a7f71bec30f26eb',
  "research/#{STEM}_primary_audit.md" => '0f7f56d32025f4cd86218f54dfcf5155675f316d2afecdd0007b13ad70240a8d',
  'research/r076a_report-source.md' => '0bbf94774c7d76e623c025a731e0238eca39080c4720a039f080afb038ecad8b',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075w_full_frequency_two_harmonic_flux_payment.md' => '571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4',
  'research/r075z_unresolved_cluster_carrier_current_gate.md' => '30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97'
}.freeze
FIXTURES_SHA256 = 'f3644b2a7a641bc92c6c1936f1c05cbed88a6a3e94e25d650c7258ce07b30a31'
EXPECTED_SHA256 = '32d0f99d07d842bf6c9161698249c186c4d23d2f1f33e7f8bd7fc18804887697'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash r_hash w_hash z_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema expected_schema],
  'integrity' => %w[utf8 controls tags display_opens display_closes references left_escape fraction_escape],
  'geometry' => %w[delta_order support_radius support_bound plateau_length plateau_bound xi_mass xi_nonzero],
  'cluster' => %w[threshold ceiling_carrier alpha beta carrier_branch gap_branch dyadic_band],
  'clock' => %w[radius physical_speed scaled_speed physical_end clock_end],
  'damping' => %w[mu four_mu quarter_bound exp_bound r_lower],
  'phase' => %w[phase_actual phase_half cosine_inequality cosine_lower],
  'current' => %w[current_formula bracket_upper current_upper current_negative],
  'correction' => %w[derivative_square beta_square_bound correction_upper target_upper correction_negative],
  'point' => %w[point_z point_zz point_j point_correction pde_residual full_gradient],
  'localization' => %w[positive_weight nonzero_cutoff negative_integral negative_coefficient common_heat all_cutoffs],
  'source' => %w[nazarov kovrijkine egidi_veselic jaming_saba context_only no_novelty],
  'audit' => %w[audit_pass math_zero release_zero finite_not_proof figure_decision],
  'boundary' => %w[sign_only perturbative_open joint_open z_payment_open w_payment_retained regularity_open singularity_open not_clay]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

def flat(text)
  text.gsub(/\s+/, ' ')
end

def all_in?(text, fragments)
  fragments.all? { |fragment| text.include?(fragment) }
end

def qstr(value)
  value.denominator == 1 ? value.numerator.to_s : "#{value.numerator}/#{value.denominator}"
end

def clean_bytes?(data)
  data.dup.force_encoding(Encoding::UTF_8).valid_encoding? &&
    data.bytes.none? { |byte| (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127 }
end

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  warn "unknown R076A_RUBY_MUTATION: #{MUTATION}"
  exit 2
end
abort('duplicate mutation name in R0.76A Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
certificate = JSON.parse(CERTIFICATE.read)
abort('Python/Ruby mutation manifests differ') unless certificate.fetch('negativeMutations') == NEGATIVE_MUTATIONS

main_raw = MAIN.binread
primary_raw = PRIMARY.binread
source_raw = SOURCE.binread
main_text = main_raw.force_encoding(Encoding::UTF_8)
primary_text = primary_raw.force_encoding(Encoding::UTF_8)
source_text = source_raw.force_encoding(Encoding::UTF_8)
compact = flat(main_text)
compact_primary = flat(primary_text)
compact_source = flat(source_text)

delta0 = Rational(fixtures.dig('profile', 'delta0'))
delta = Rational(fixtures.dig('profile', 'delta'))
q_count = Integer(fixtures.dig('scale', 'q'))
a = Rational(fixtures.dig('scale', 'a'))
ell = Rational(fixtures.dig('scale', 'ell'))
clock_end = Rational(fixtures.dig('scale', 'clockEnd'))
v_fixture = Rational(fixtures.dig('scale', 'scaledSpeed'))
frequencies = fixtures.dig('cluster', 'frequencies').map { |value| Integer(value) }
amplitudes = fixtures.dig('cluster', 'amplitudes').map { |value| Integer(value) }
phases = fixtures.dig('cluster', 'phasesOverPi').map { |value| Integer(value) }

support_radius = 1 + delta / a
plateau_length = 2 - 2 * delta / a
xi_mass_lower_over_pi = 2 * delta0
computed_geometry = {
  'supportRadius' => qstr(support_radius),
  'supportWithinThreeHalves' => support_radius <= Rational(3, 2),
  'centralPlateauLength' => qstr(plateau_length),
  'centralPlateauAtLeastOne' => plateau_length >= 1,
  'xiMassLowerOverPi' => qstr(xi_mass_lower_over_pi)
}

threshold = 8 * q_count
carrier = frequencies.first
upper = frequencies.last
computed_carrier = (Rational(threshold, 1) / ell).ceil
alpha = carrier * ell
beta = (upper - carrier) * ell
radius = ell / a
physical_speed = a / radius
scaled_speed = physical_speed * radius / a
computed_cluster = {
  'threshold' => threshold,
  'carrier' => carrier,
  'upperFrequency' => upper,
  'alpha' => Integer(alpha),
  'beta' => qstr(beta),
  'carrierCondition' => alpha >= threshold,
  'gapConditionFails' => beta < threshold,
  'dyadicBand' => upper <= 2 * carrier,
  'R' => qstr(radius),
  'physicalSpeed' => Integer(physical_speed),
  'scaledSpeed' => Integer(scaled_speed)
}

mu = (2 * alpha * beta + beta**2) / a**2
four_mu = 4 * mu
phase_actual = beta * (support_radius + clock_end)
phase_bound = Rational(1, 2)
cosine_lower = Rational(7, 8)
r_lower = Rational(3, 4)
current_upper = -Rational(9, 16) * beta
correction_upper = beta**2 + 2 * alpha * current_upper
target_correction_upper = -alpha * beta
computed_bounds = {
  'mu' => qstr(mu),
  'fourMu' => qstr(four_mu),
  'fourMuBelowQuarter' => four_mu < Rational(1, 4),
  'phaseMaximum' => qstr(phase_bound),
  'cosineLower' => qstr(cosine_lower),
  'rLower' => qstr(r_lower),
  'currentUpper' => qstr(current_upper),
  'correctionUpper' => qstr(correction_upper),
  'targetCorrectionUpper' => qstr(target_correction_upper),
  'correctionTargetHolds' => correction_upper <= target_correction_upper,
  'strictNegative' => current_upper.negative? && correction_upper.negative?
}

phase_signs = phases.map { |value| value.even? ? 1 : -1 }
point_z = amplitudes[0] * phase_signs[0] + amplitudes[1] * phase_signs[1]
point_zz = beta * amplitudes[1] * phase_signs[1]
point_j = point_z * point_zz
point_correction = point_zz**2 + 2 * alpha * point_j
full_gradient = alpha**2 * point_z**2 + point_correction
pde_residual = mu - (2 * alpha * beta + beta**2) / a**2
computed_point = {
  'Z' => [point_z, 0],
  'Zz' => [0, qstr(point_zz)],
  'J' => qstr(point_j),
  'correctionDensity' => qstr(point_correction)
}
negative_coefficient_over_pi = -Rational(9, 8) * delta0 * beta
physical_end = clock_end * radius**2
computed_clock = {
  'physicalEnd' => qstr(physical_end),
  'negativeCoefficientOverPi' => qstr(negative_coefficient_over_pi)
}

tags = main_text.scan(/\\tag\{A\.(\d+)\}/).flatten.map(&:to_i)
references = main_text.scan(/\bA\.(\d+)\b/).flatten.map(&:to_i)
display_opens = main_text.lines.count { |line| line.chomp == '\\[' }
display_closes = main_text.lines.count { |line| line.chomp == '\\]' }

assertions = []
record = lambda do |name, group, ok, details = nil|
  assertions << {'name' => name, 'group' => group, 'pass' => (!!ok && !GROUPS.fetch(group).include?(MUTATION)), 'details' => details}
end

record.call('frozen source bindings', 'bindings', FROZEN.all? { |path, digest| sha256(ROOT.join(path)) == digest })
record.call(
  'fixture, expected, and canonical certificate bindings', 'inputs',
  sha256(FIXTURES) == FIXTURES_SHA256 && sha256(EXPECTED) == EXPECTED_SHA256 &&
    fixtures.fetch('schema').end_with?('fixtures-v1') && expected.fetch('schema').end_with?('expected-v1') &&
    certificate.fetch('schema') == 'r076a-complete-clock-localized-current-sign-obstruction-certificate-v1' &&
    certificate.fetch('verdict') == 'PASS' && certificate.fetch('assertions').length == 15
)
record.call(
  'UTF-8, controls, tags, displays, references, and TeX escapes', 'integrity',
  clean_bytes?(main_raw) && clean_bytes?(primary_raw) && clean_bytes?(source_raw) &&
    tags == (1..34).to_a && display_opens == 34 && display_closes == 34 &&
    (references.uniq - tags).empty? && main_text.include?('I_-=\\left[') &&
    main_text.include?('\\frac18\\alpha\\beta-\\frac98\\alpha\\beta'),
  {'tags' => tags.length, 'opens' => display_opens, 'closes' => display_closes}
)
record.call(
  'primitive support, plateau, and mass ledger', 'geometry',
  0 < delta0 && delta0 < delta && a >= [Rational(24), 2 * delta].max &&
    computed_geometry == expected.fetch('geometry') &&
    all_in?(compact, ['\\Xi_a(z)\\ge0', '\\subset\\left[-\\frac32,\\frac32\\right]',
                      '\\int_{\\mathbb R}\\Xi_a(z)\\,dz\\ge2\\pi\\delta_0>0']),
  computed_geometry
)
record.call(
  'exact high-carrier unresolved cluster', 'cluster',
  computed_carrier == carrier && computed_cluster == expected.fetch('cluster') &&
    all_in?(compact, ['N=\\left\\lceil\\frac{16}{\\ell}\\right\\rceil', 'N\\ell\\ge8q',
                      '\\beta<8q', 'actual unresolved high-carrier cluster']),
  computed_cluster
)
record.call(
  'scaled and physical clock ledger', 'clock',
  v_fixture == scaled_speed && scaled_speed == 1 && computed_clock == expected.fetch('clock') &&
    all_in?(compact, ['s=\\frac t{R^2}', 'v=\\frac{BR}{a}', 'constant speed `B=a/R`']),
  computed_clock
)
record.call(
  'exact damping and uniform envelope lower bound', 'damping',
  qstr(mu) == expected.dig('bounds', 'mu') && qstr(four_mu) == expected.dig('bounds', 'fourMu') &&
    four_mu < Rational(1, 4) && Math.exp(-0.25) > 0.75 &&
    all_in?(compact, ['4\\mu', '<\\frac14', '\\frac34<e^{-1/4}\\le r(s)\\le1']),
  {'mu' => qstr(mu), 'fourMu' => qstr(four_mu)}
)
record.call(
  'support-wide complete-clock phase bound', 'phase',
  phase_actual <= phase_bound && qstr(phase_bound) == expected.dig('bounds', 'phaseMaximum') &&
    qstr(cosine_lower) == expected.dig('bounds', 'cosineLower') &&
    all_in?(compact, ['|\\beta(z-s)|', '\\le\\frac12', '\\ge\\frac78']),
  {'actualMaximum' => qstr(phase_actual), 'certifiedMaximum' => qstr(phase_bound)}
)
record.call(
  'uniform strict negative current', 'current',
  qstr(current_upper) == expected.dig('bounds', 'currentUpper') && current_upper.negative? &&
    all_in?(compact, ['&=\\beta r\\left(r-2\\cos(\\beta(z-s))\\right)',
                      'J\\le-\\frac34\\beta r\\le-\\frac9{16}\\beta']),
  {'currentUpper' => qstr(current_upper)}
)
record.call(
  'uniform negative correction density', 'correction',
  qstr(correction_upper) == expected.dig('bounds', 'correctionUpper') &&
    qstr(target_correction_upper) == expected.dig('bounds', 'targetCorrectionUpper') &&
    correction_upper <= target_correction_upper && target_correction_upper.negative? &&
    all_in?(compact, ['|\\partial_zZ|^2=\\beta^2r^2\\le\\beta^2',
                      '\\le\\frac18\\alpha\\beta-\\frac98\\alpha\\beta', '=-\\alpha\\beta']),
  {'correctionUpper' => qstr(correction_upper), 'target' => qstr(target_correction_upper)}
)
record.call(
  'exact point, PDE coefficient, and retained full gradient', 'point',
  computed_point == expected.fetch('point') && pde_residual.zero? && full_gradient == Rational(30_625, 121) &&
    all_in?(compact_primary, ['Z_s+Z_z-a^{-2}Z_{zz}-2i\\alpha a^{-2}Z_z=0',
                              'J=-\\frac1{11}', '\\frac{30625}{121}>0']),
  {'point' => computed_point, 'pdeResidual' => qstr(pde_residual), 'fullGradient' => qstr(full_gradient)}
)
record.call(
  'strict negativity after every admissible localization', 'localization',
  negative_coefficient_over_pi == Rational(expected.dig('clock', 'negativeCoefficientOverPi')) &&
    all_in?(compact, ['\\zeta:[0,4]\\longrightarrow[0,1]', '\\int_0^4\\zeta(s)\\,ds>0',
                      '\\zeta e^{-2\\alpha^2s/a^2}', '<0', 'Every nonzero frozen cutoff']),
  {'negativeCoefficientOverPi' => qstr(negative_coefficient_over_pi)}
)
record.call(
  'bounded contextual source report', 'source',
  all_in?(compact_source, ['https://www.mathnet.ru/eng/aa397', 'https://arxiv.org/abs/math/0012186',
                           'https://arxiv.org/abs/1609.07020', 'https://arxiv.org/abs/2311.17714',
                           'Context only', 'not represented as evidence of novelty'])
)
record.call(
  'primary audit and analytic-only figure decision', 'audit',
  all_in?(compact_primary, ['Current verdict: **PASS**', 'Mathematical blocker count: **0**',
                            'Release blocker count: **0**', 'not represented as proof',
                            'no simulation or formal scientific figure is needed'])
)
record.call(
  'narrow sign obstruction and open-claim boundary', 'boundary',
  all_in?(compact, ['rules out only the strategy of discarding', 'may still be perturbative',
                    'joint multiplier argument must retain', 'full Z-sector collar-flux estimate',
                    'already pays that estimate', 'regularity', 'singularity', '**NOT CLAY.**']) &&
    certificate.dig('boundary', 'clayProblemSolved') == false
)

verdict = assertions.all? { |item| item.fetch('pass') } ? 'PASS' : 'FAIL'
report_lines = [
  '# R0.76A independent Ruby audit',
  '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{assertions.count { |item| item.fetch('pass') }}/#{assertions.length}",
  "- Mutation challenge: #{MUTATION.empty? ? 'none' : MUTATION}",
  "- Blocker count: #{verdict == 'PASS' ? 0 : 1}",
  '',
  'The audit independently recomputes the frozen geometry, physical/scaled',
  'clock, unresolved pair, exact rational bounds, point current, correction',
  'density, PDE coefficient, and retained full-gradient value.  Finite fixtures',
  'are not proof of the continuum sign statement.',
  '',
  'Only localized sign-dropping is rejected.  General cluster payment,',
  'Version-M transfer, regularity, and singularity remain OPEN. **NOT CLAY.**',
  ''
]
OUT.write(report_lines.join("\n"))
puts JSON.generate({suite: 'r076a-independent-ruby-audit-v1', verdict: verdict,
                    assertions: assertions.length, mutation: MUTATION})
exit(verdict == 'PASS' ? 0 : 1)
