#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent exact-arithmetic implementation for the R0.76F finite ledger.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
STEM = 'r076f_exponential_spatial_observation_lower_bound'
MAIN = ROOT.join("research/#{STEM}.md")
PRIMARY = ROOT.join("research/#{STEM}_primary_audit.md")
SOURCE = ROOT.join('research/r076f_report-source.md')
FIXTURES = ROOT.join("scripts/#{STEM}_fixtures.json")
EXPECTED = ROOT.join("scripts/#{STEM}_expected.json")
PYTHON_CERTIFICATE = Pathname.new(ENV.fetch('R076F_JSON', ROOT.join("research/#{STEM}_certificate.json").to_s))
OUT = Pathname.new(ENV.fetch('R076F_RUBY_REPORT', ROOT.join("research/#{STEM}_independent_audit.md").to_s))
MUTATION = ENV.fetch('R076F_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => '48204fcbf8fe9af3f0fdc7720844c3dd8362d8767caf73de016eda7250b70973',
  "research/#{STEM}_primary_audit.md" => 'abcaa220c56d1f90c4b34061191e7cd009b8d911be3f83d705e95aa51b4d84cc',
  'research/r076f_report-source.md' => '5e3939710dcfefcbc08b93761d8cdda1e655656a1bcd404b63fcea251ffd5e1e',
  'research/r076e_linear_modal_entropy_window.md' => '1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4',
  "scripts/#{STEM}_fixtures.json" => '1b11049ab482eb9b6d6b99cfdabfb4cd0a34ac4f483e3e69c5ec178dce752b5a',
  "scripts/#{STEM}_expected.json" => '9703be8236b77e556085f9b358f4128ace4e32920a5391ebc1e2a900b232d37a'
}.freeze

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash predecessor_hash fixture_hash expected_hash],
  'inputs' => %w[fixture_schema expected_schema fixture_utf8 expected_utf8],
  'integrity' => %w[main_utf8 primary_utf8 source_utf8 no_controls no_cr no_trailing tag_sequence display_balance reference_closure no_discouraged_prose],
  'geometry' => %w[i_order j_order i_length j_length endpoint_in_j endpoint_outside_i delta_positive delta_cap x_definition sine_monotonic_range],
  'dyadic' => %w[q_at_least_two frequency_count integer_frequencies frequency_rule strict_order first_frequency last_frequency dyadic_band no_zero_mode amplitude_count amplitudes_nonnegative binomial_coefficients amplitude_sum],
  'ratio' => %w[sample_sine_square triple_angle_identity triple_angle_ratio lower_exponent lower_bound l3_measure_factor phase_alignment derivative_nonnegative],
  'scale' => %w[spacing_rule alpha_rule sample_alpha scaled_fibre exact_heat_shear navier_stokes_embedding],
  'asymptotic' => %w[log_bound positive_slope polynomial_rejected quadratic_changes_coefficient small_quadratic_not_excluded],
  'source' => %w[nazarov_source friedland_source remez_source journal_doi preprint_boundary no_novelty_claim primary_pass math_blocker_zero release_blocker_zero fixture_correction],
  'boundary' => %w[spatial_only no_complete_flux_lower alternative_proof_open exact_base_open arbitrary_packets_open version_m_open regularity_open singularity_open no_figure no_simulation not_clay]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

def clean_bytes?(data)
  data.dup.force_encoding(Encoding::UTF_8).valid_encoding? &&
    data.bytes.none? { |byte| (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127 }
end

def flat(text)
  text.gsub(/\s+/, ' ')
end

def choose(n, k)
  return 0 if k.negative? || k > n
  (1..k).reduce(1) { |value, index| value * (n - k + index) / index }
end

abort "unknown R076F_RUBY_MUTATION: #{MUTATION}" unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
abort 'duplicate mutation name in R0.76F Ruby suite' unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

fixture_raw = FIXTURES.binread
expected_raw = EXPECTED.binread
main_raw = MAIN.binread
primary_raw = PRIMARY.binread
source_raw = SOURCE.binread
fixture = JSON.parse(fixture_raw)
expected = JSON.parse(expected_raw)
python_certificate = JSON.parse(PYTHON_CERTIFICATE.read)
main_text = main_raw.force_encoding(Encoding::UTF_8)
primary_text = primary_raw.force_encoding(Encoding::UTF_8)
source_text = source_raw.force_encoding(Encoding::UTF_8)
compact_main = flat(main_text)
compact_source = flat(source_text)
bindings = FROZEN.keys.sort.to_h do |path|
  [path, {'expectedSha256' => FROZEN.fetch(path), 'observedSha256' => Digest::SHA256.file(ROOT.join(path)).hexdigest}]
end

geom = fixture.fetch('geometry')
i_left = Rational(geom.fetch('iLeft'))
i_right = Rational(geom.fetch('iRight'))
j_left = Rational(geom.fetch('jLeft'))
j_right = Rational(geom.fetch('jRight'))
endpoint = Rational(geom.fetch('endpoint'))
sample = fixture.fetch('sample')
q_count = sample.fetch('q').to_i
delta_over_pi = Rational(sample.fetch('deltaOverPi'))
x_over_pi = delta_over_pi / 4
modes = sample.fetch('frequencies').map(&:to_i)
amplitudes = sample.fetch('binomialAmplitudes').map(&:to_i)
expected_amplitudes = (0...q_count).map { |k| choose(q_count - 1, k) }
sine_squared = Rational(sample.fetch('sineSquared'))
triple_ratio = 3 - 4 * sine_squared
lower_exponent = q_count - 1
lower_bound = triple_ratio.to_i**lower_exponent
alpha_over_pi = q_count * delta_over_pi

tags = main_text.scan(/\\tag\{F\.(\d+)\}/).flatten.map(&:to_i)
refs = main_text.scan(/(?<![A-Za-z0-9_.])F\.(\d+)/).flatten.map(&:to_i)
opens = main_text.scan(/^\\\[$/).length
closes = main_text.scan(/^\\\]$/).length
discouraged = %w[我们 攻关 主攻 研究纪律 三重审计 杀死错误想法]

checks = {
  'bindings' => {
    'main_hash' => bindings.fetch("research/#{STEM}.md").values.uniq.length == 1,
    'primary_hash' => bindings.fetch("research/#{STEM}_primary_audit.md").values.uniq.length == 1,
    'source_hash' => bindings.fetch('research/r076f_report-source.md').values.uniq.length == 1,
    'predecessor_hash' => bindings.fetch('research/r076e_linear_modal_entropy_window.md').values.uniq.length == 1,
    'fixture_hash' => bindings.fetch("scripts/#{STEM}_fixtures.json").values.uniq.length == 1,
    'expected_hash' => bindings.fetch("scripts/#{STEM}_expected.json").values.uniq.length == 1
  },
  'inputs' => {
    'fixture_schema' => fixture.fetch('schema') == 'r076f-exponential-spatial-observation-lower-bound-fixtures-v1',
    'expected_schema' => expected.fetch('schema') == 'r076f-exponential-spatial-observation-lower-bound-expected-v1',
    'fixture_utf8' => clean_bytes?(fixture_raw), 'expected_utf8' => clean_bytes?(expected_raw)
  },
  'integrity' => {
    'main_utf8' => clean_bytes?(main_raw), 'primary_utf8' => clean_bytes?(primary_raw),
    'source_utf8' => clean_bytes?(source_raw),
    'no_controls' => [main_raw, primary_raw, source_raw].all? { |value| clean_bytes?(value) },
    'no_cr' => [main_raw, primary_raw, source_raw].none? { |value| value.include?("\r") },
    'no_trailing' => [main_text, primary_text, source_text].all? { |text| text.lines.none? { |line| line.chomp.end_with?(' ', "\t") } },
    'tag_sequence' => tags == (1..18).to_a, 'display_balance' => opens == 18 && closes == 18,
    'reference_closure' => (refs.uniq - tags.uniq).empty?,
    'no_discouraged_prose' => discouraged.none? { |word| [main_text, primary_text, source_text].any? { |text| text.include?(word) } }
  },
  'geometry' => {
    'i_order' => i_left < i_right, 'j_order' => j_left < i_left && i_right < j_right,
    'i_length' => i_right - i_left == Rational(expected.dig('geometry', 'iLength').to_s),
    'j_length' => j_right - j_left == Rational(expected.dig('geometry', 'jLength').to_s),
    'endpoint_in_j' => j_left <= endpoint && endpoint <= j_right && expected.dig('geometry', 'endpointInJ'),
    'endpoint_outside_i' => !(i_left <= endpoint && endpoint <= i_right) && expected.dig('geometry', 'endpointOutsideI'),
    'delta_positive' => delta_over_pi.positive?, 'delta_cap' => delta_over_pi <= Rational(2, 3),
    'x_definition' => x_over_pi == Rational(sample.fetch('xOverPi')),
    'sine_monotonic_range' => x_over_pi.positive? && x_over_pi <= Rational(1, 6)
  },
  'dyadic' => {
    'q_at_least_two' => q_count >= 2, 'frequency_count' => modes.length == q_count,
    'integer_frequencies' => modes.all? { |value| value.is_a?(Integer) },
    'frequency_rule' => modes == (0...q_count).map { |k| q_count + k },
    'strict_order' => modes == modes.uniq.sort && expected.dig('sample', 'strictlyIncreasing'),
    'first_frequency' => modes.first == expected.dig('sample', 'firstFrequency'),
    'last_frequency' => modes.last == expected.dig('sample', 'lastFrequency'),
    'dyadic_band' => modes.last <= 2 * modes.first && expected.dig('sample', 'dyadicBand'),
    'no_zero_mode' => modes.first >= 1, 'amplitude_count' => amplitudes.length == q_count,
    'amplitudes_nonnegative' => amplitudes.all? { |value| value >= 0 },
    'binomial_coefficients' => amplitudes == expected_amplitudes,
    'amplitude_sum' => amplitudes.sum == expected.dig('sample', 'amplitudeSum') && amplitudes.sum == 2**(q_count - 1)
  },
  'ratio' => {
    'sample_sine_square' => sine_squared == Rational(1, 4),
    'triple_angle_identity' => triple_ratio == 3 - 4 * sine_squared,
    'triple_angle_ratio' => triple_ratio == expected.dig('sample', 'tripleAngleRatio') && triple_ratio == 2,
    'lower_exponent' => lower_exponent == expected.dig('sample', 'lowerBoundExponent'),
    'lower_bound' => lower_bound == expected.dig('sample', 'lowerBound') && lower_bound == 8,
    'l3_measure_factor' => i_right - i_left == 1,
    'phase_alignment' => ['e^{i\\theta}H_{q,\\delta}(z_*)', '=|H_{q,\\delta}(z_*)|', '\\phi_{k+1}=-\\theta-k\\pi'].all? { |part| compact_main.include?(part) },
    'derivative_nonnegative' => main_text.include?('The derivative term is nonnegative')
  },
  'scale' => {
    'spacing_rule' => main_text.include?('Let `a,R>0` satisfy `delta=aR`'),
    'alpha_rule' => fixture.dig('scale', 'alphaRule') == 'q*delta' && main_text.include?('\\alpha=n_1aR=q\\delta'),
    'sample_alpha' => alpha_over_pi == Rational(expected.dig('sample', 'alphaOverPi')),
    'scaled_fibre' => compact_main.include?('G(0,z)=F(0,aRz)=g_{q,\\delta}(z)'),
    'exact_heat_shear' => compact_main.include?('is a smooth unforced Navier--Stokes solution'),
    'navier_stokes_embedding' => main_text.include?('`u=(0,0,F(t,x_2))`')
  },
  'asymptotic' => {
    'log_bound' => main_text.include?('\\log C_q\\ge(q-1)\\log2'),
    'positive_slope' => expected.dig('asymptotic', 'limitingSlope') == 'log(2)',
    'polynomial_rejected' => expected.dig('asymptotic', 'polynomialReplacementRejected') && compact_main.include?('cannot replace `e^(Cq)` by a polynomial loss'),
    'quadratic_changes_coefficient' => expected.dig('asymptotic', 'quadraticDensityChangesFrozenCoefficient') && compact_main.include?('cannot then be retained'),
    'small_quadratic_not_excluded' => compact_main.include?('could still leave a negative total exponent')
  },
  'source' => {
    'nazarov_source' => source_text.include?('F. L. Nazarov') && source_text.include?('mathnet.ru'),
    'friedland_source' => source_text.include?('Omer Friedland') && source_text.include?('2606.24823'),
    'remez_source' => source_text.include?('S. Tikhonov and P. Yuditskii'),
    'journal_doi' => source_text.include?('10.1007/s00365-019-09473-2'),
    'preprint_boundary' => source_text.include?('recent preprint'),
    'no_novelty_claim' => compact_source.include?('not presented as a new approximation theorem'),
    'primary_pass' => primary_text.include?('Current verdict: **PASS**'),
    'math_blocker_zero' => primary_text.include?('Mathematical blocker count: **0**'),
    'release_blocker_zero' => primary_text.include?('Release blocker count: **0**'),
    'fixture_correction' => ['initially encoded the rule for `alpha` as `q-delta`', 'fixture now says `q*delta`', 'Python and Ruby implementations validate'].all? { |part| flat(primary_text).include?(part) }
  },
  'boundary' => {
    'spatial_only' => compact_main.include?('lower bound for the spatial observation step'),
    'no_complete_flux_lower' => compact_main.include?('not a lower bound for the complete collar flux'),
    'alternative_proof_open' => compact_main.include?('does not exclude a different proof'),
    'exact_base_open' => compact_main.include?('does not determine the optimal exponential base'),
    'arbitrary_packets_open' => compact_main.include?('arbitrary packets'),
    'version_m_open' => compact_main.include?('complete Version-M extraction'),
    'regularity_open' => compact_main.include?('regularity'), 'singularity_open' => compact_main.include?('singularity'),
    'no_figure' => compact_main.include?('No simulation or formal scientific figure is claimed'),
    'no_simulation' => !fixture.dig('claimBoundary', 'simulationClaimed'),
    'not_clay' => main_text.include?('**NOT CLAY.**')
  }
}

unless MUTATION.empty?
  group = GROUPS.find { |_name, names| names.include?(MUTATION) }&.first
  checks.fetch(group)[MUTATION] = false
end

failures = checks.flat_map { |group, rows| rows.reject { |_name, value| value }.keys.map { |name| "#{group}.#{name}" } }
assertions = checks.values.sum(&:length)
verdict = failures.empty? ? 'PASS' : 'FAIL'
exact = {
  'q' => q_count, 'frequencies' => modes, 'amplitudes' => amplitudes,
  'xOverPi' => x_over_pi.to_s, 'tripleAngleRatio' => triple_ratio.to_i,
  'lowerBoundExponent' => lower_exponent, 'lowerBound' => lower_bound,
  'alphaOverPi' => alpha_over_pi.to_s
}
python_exact_match = python_certificate.fetch('exact') == exact
python_mutations_match = python_certificate.fetch('negativeMutations') == NEGATIVE_MUTATIONS

lines = [
  '# R0.76F independent Ruby certificate audit', '',
  "- Verdict: **#{verdict}**", "- Ruby assertions: #{assertions - failures.length}/#{assertions}",
  "- Python/Ruby exact section identical: #{python_exact_match ? 'PASS' : 'FAIL'}",
  "- Python/Ruby mutation inventory identical: #{python_mutations_match ? 'PASS' : 'FAIL'} (#{NEGATIVE_MUTATIONS.length})",
  "- Exact sample lower bound: 2^(#{lower_exponent})=#{lower_bound}",
  "- Failures: #{failures.empty? ? 'none' : failures.inspect}", '',
  'The counterexample-first mathematical reread recorded in the primary audit',
  'reports PASS with zero blockers and closed the alpha-rule fixture typo.',
  'This implementation independently recomputes the rational geometry, binomial',
  'frequencies, triple-angle ratio, and claim boundary.  Finite arithmetic is',
  'not proof of the continuum norm inequality or the Navier--Stokes embedding.',
  '**NOT CLAY.**', ''
]
OUT.write(lines.join("\n"))

unless python_exact_match && python_mutations_match
  warn 'Python/Ruby comparison failed'
  exit 1
end
puts JSON.generate({'suite' => 'r076f-ruby', 'verdict' => verdict, 'assertions' => assertions, 'failures' => failures})
exit(failures.empty? ? 0 : 1)
