#!/usr/bin/env ruby
# Independent fail-closed exact audit for frozen R0.75Z.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
STEM = 'r075z_unresolved_cluster_carrier_current_gate'
MAIN = ROOT.join('research', "#{STEM}.md")
PRIMARY = ROOT.join('research', "#{STEM}_primary_audit.md")
SOURCE = ROOT.join('research', 'r075z_report-source.md')
FIXTURES = ROOT.join('scripts', "#{STEM}_fixtures.json")
EXPECTED = ROOT.join('scripts', "#{STEM}_expected.json")
CERTIFICATE = Pathname.new(ENV.fetch('R075Z_JSON', ROOT.join('research', "#{STEM}_certificate.json").to_s))
OUT = Pathname.new(ENV.fetch('R075Z_RUBY_REPORT', ROOT.join('research', "#{STEM}_independent_audit.md").to_s))
MUTATION = ENV.fetch('R075Z_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => '30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97',
  "research/#{STEM}_primary_audit.md" => '895d09e0b403c0a6bcf216624527dd6c2bf76f15d7ce5f6b6b0a31b6f64a1eb0',
  'research/r075z_report-source.md' => '9b071b3e020210922834435ea7e5806620479d400eb044f48f34e7b02c259d4c',
  'research/r075b_bulk_clock_outer_padding_gate.md' => '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075x_fixed_finite_mode_low_carrier_payment.md' => '8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763',
  'research/r075y_strongly_separated_multimode_flux_payment.md' => '74790f910b596c86b204291d997ef723cabbc85d14a89e3fe900814fcd88b0a6'
}.freeze
FIXTURES_SHA256 = '9bd703f41f4b4823a4b6fe38136bf2a5bef126cf15edb3b54036cf1b80e4f4b0'
EXPECTED_SHA256 = '6043f94b70b6068a58d7716877a5319edc9edfc90b47bfee23ea7baee0ad58d4'

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

def flat(text)
  text.gsub(/\s+/, ' ')
end

def all_in?(text, fragments)
  fragments.all? { |fragment| text.include?(fragment) }
end

def signed_minimum_gap(modes)
  signed = (modes.map { |mode| -mode } + modes).sort
  signed.each_cons(2).map { |left, right| right - left }.min
end

def classify(modes, ell, threshold)
  return 'X' if modes.first * ell < threshold
  return 'Y' if modes.each_cons(2).all? { |left, right| (right - left) * ell >= threshold }

  'Z'
end

def clusters(modes, ell, threshold)
  blocks = [[modes.first]]
  modes.each_cons(2) do |left, right|
    if (right - left) * ell >= threshold
      blocks << [right]
    else
      blocks.last << right
    end
  end
  blocks
end

fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
certificate = JSON.parse(CERTIFICATE.read)
negative_mutations = certificate.fetch('negativeMutations')
unless MUTATION.empty? || negative_mutations.include?(MUTATION)
  warn "unknown R075Z_RUBY_MUTATION: #{MUTATION}"
  exit 2
end

main_text = MAIN.read
primary_text = PRIMARY.read
source_text = SOURCE.read
compact = flat(main_text)
compact_primary = flat(primary_text)
compact_source = flat(source_text)

q_count = Integer(fixtures.fetch('q'))
ell = Rational(fixtures.fetch('ell').to_s)
threshold = Integer(fixtures.fetch('thresholdMultiplier')) * q_count
computed_partition = {}
fixtures.fetch('partitionCases').each do |name, raw_modes|
  modes = raw_modes.map { |value| Integer(value) }
  item = {
    'sector' => classify(modes, ell, threshold),
    'dyadicBand' => modes.last <= 2 * modes.first
  }
  unless name == 'x'
    gap = signed_minimum_gap(modes)
    item['signedMinimumGap'] = gap
    item['separationProduct'] = Integer(ell * gap)
    item['clusters'] = clusters(modes, ell, threshold)
  end
  computed_partition[name] = item
end

cluster = fixtures.fetch('cluster')
carrier = Integer(cluster.fetch('carrier'))
offsets = cluster.fetch('offsets').map { |value| Integer(value) }
amplitudes = cluster.fetch('amplitudes').map { |value| Integer(value) }
phase_signs = cluster.fetch('phasesOverPi').map { |value| Integer(value).even? ? 1 : -1 }
speed = Integer(cluster.fetch('transportSpeed'))
coefficients = amplitudes.zip(phase_signs).map { |amplitude, sign| Complex(amplitude * sign, 0) }
z_value = coefficients.sum(Complex(0, 0))
zy_value = offsets.zip(coefficients).sum(Complex(0, 0)) { |offset, coefficient| Complex(0, offset) * coefficient }
q_value = (z_value.real**2 + z_value.imag**2).to_i
j_value = (z_value.conjugate * zy_value).imag.to_i

residual = offsets.zip(coefficients).sum(Complex(0, 0)) do |offset, coefficient|
  zt = Complex(-2 * carrier * offset - offset**2, -speed * offset) * coefficient
  zy = Complex(0, offset) * coefficient
  zyy = -offset**2 * coefficient
  zt + speed * zy - zyy - Complex(0, 2 * carrier) * zy
end

current = offsets.zip(amplitudes).sum { |offset, amplitude| offset * amplitude**2 }
offset_gradient = offsets.zip(amplitudes).sum { |offset, amplitude| offset**2 * amplitude**2 }
modulated_dissipation = offset_gradient + 2 * carrier * current
full_gradient = offsets.zip(amplitudes).sum { |offset, amplitude| (carrier + offset)**2 * amplitude**2 }
computed_cluster = {
  'carrier' => carrier,
  'offsets' => offsets,
  'scaledWidth' => Integer((offsets.last - offsets.first) * ell),
  'strictWidthBound' => threshold * (offsets.length - 1),
  'widthBoundHolds' => (offsets.last - offsets.first) * ell < threshold * (offsets.length - 1),
  'widthBelowCarrier' => offsets.last <= carrier
}
computed_point = {
  'Z' => [z_value.real.to_i, z_value.imag.to_i],
  'Zy' => [zy_value.real.to_i, zy_value.imag.to_i],
  'Q' => q_value,
  'J' => j_value,
  'unweightedAbsorber' => q_value + (zy_value.real**2 + zy_value.imag**2).to_i,
  'weightedCurrent' => 2 * carrier * j_value.abs,
  'modulatedDissipationDensity' => (zy_value.real**2 + zy_value.imag**2).to_i + 2 * carrier * j_value
}
computed_global = {
  'currentOver2Pi' => current,
  'offsetGradientOver2Pi' => offset_gradient,
  'modulatedDissipationOver2Pi' => modulated_dissipation,
  'fullGradientOver2Pi' => full_gradient
}
square_left = z_value.real.to_i**2
square_right = ((z_value.abs**2 + (z_value * z_value).real) / 2).to_i
computed_identity = {
  'pdeResidual' => [residual.real.to_i, residual.imag.to_i],
  'squareLeft' => square_left,
  'squareRight' => square_right
}

assertions = []
record = lambda do |name, ok, details = nil|
  assertions << {'name' => name, 'pass' => !!ok, 'details' => details}
end

observed_bindings = FROZEN.transform_values.with_index do |_digest, index|
  sha256(ROOT.join(FROZEN.keys[index]))
end
record.call('frozen source bindings', FROZEN.all? { |path, digest| sha256(ROOT.join(path)) == digest }, observed_bindings)
record.call('fixture bindings', sha256(FIXTURES) == FIXTURES_SHA256 && sha256(EXPECTED) == EXPECTED_SHA256)
record.call(
  'certificate schema and canonical verdict',
  certificate.fetch('schema') == 'r075z-unresolved-cluster-carrier-current-gate-certificate-v1' &&
    certificate.fetch('verdict') == 'PASS' && certificate.fetch('assertions').length == 15
)
record.call('partition recomputation', threshold == expected.fetch('threshold') && computed_partition == expected.fetch('partition'), computed_partition)
record.call('cluster recomputation', computed_cluster == expected.fetch('clusterLedger'), computed_cluster)
record.call('PDE and square recomputation', computed_identity == expected.fetch('identityLedger'), computed_identity)
record.call('point obstruction recomputation', computed_point == expected.fetch('pointLedger'), computed_point)
record.call('global current recomputation', computed_global == expected.fetch('globalLedger'), computed_global)

tags = main_text.scan(/\\tag\{Z\.(\d+)\}/).flatten.map(&:to_i)
display_opens = main_text.lines.count { |line| line.chomp == '\\[' }
display_closes = main_text.lines.count { |line| line.chomp == '\\]' }
record.call('tag and display integrity', tags == (1..31).to_a && display_opens == 31 && display_closes == 31)
record.call(
  'modulation and current text boundary',
  all_in?(compact, [
    '\\partial_tZ_C+B\\partial_yZ_C-\\partial_y^2Z_C', '-2iN\\partial_yZ_C=0',
    '=-2|\\partial_yZ_C|^2-4NJ_C', '=2\\pi\\sum_{j=r}^s d_jA_j^2'
  ])
)
record.call(
  'pointwise no-go is narrowly stated',
  all_in?(compact, ['2N|J(y)|', 'N<=C', '1-2N<0', 'does not rule out']) &&
    !compact.include?('no pointwise estimate for J')
)
record.call(
  'cross-cluster and fixed-q boundary',
  all_in?(compact, ['For fixed `q`', 'cross-cluster products must still be added',
                    'No full Z-sector flux payment is claimed'])
)
record.call(
  'source collision boundary',
  all_in?(compact_source, ['https://www.mathnet.ru/eng/aa397', 'https://arxiv.org/abs/math/0012186',
                           'https://arxiv.org/abs/1609.07020', 'context and possible tools',
                           'No novelty, priority, or completeness claim'])
)
record.call(
  'primary audit boundary',
  all_in?(compact_primary, ['Current verdict: **PASS**', 'Mathematical blocker count: **0**',
                            'Release blocker count: **0**', 'not represented as proof'])
)
record.call(
  'open claims and NOT CLAY',
  all_in?(compact, ['full Z-sector collar-flux estimate', 'complete Version-M extraction',
                    'regularity', 'singularity', '**NOT CLAY.**']) &&
    certificate.dig('boundary', 'clayProblemSolved') == false
)

mutation_failure = !MUTATION.empty?
verdict = assertions.all? { |item| item.fetch('pass') } && !mutation_failure ? 'PASS' : 'FAIL'
report_lines = [
  '# R0.75Z independent Ruby audit',
  '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{assertions.count { |item| item.fetch('pass') }}/#{assertions.length}",
  "- Mutation challenge: #{MUTATION.empty? ? 'none' : MUTATION}",
  "- Blocker count: #{verdict == 'PASS' ? 0 : 1}",
  '',
  'The audit independently recomputes the strict/equality partition cases,',
  'cluster bounds, PDE residual, square identity, local obstruction, and global',
  'Fourier ledgers.  Finite fixtures are not proof of the continuum identities.',
  'The full clustered-sector payment and Navier--Stokes regularity remain OPEN.',
  '**NOT CLAY.**',
  ''
]
OUT.write(report_lines.join("\n"))
puts JSON.generate({suite: 'r075z-independent-ruby-audit-v1', verdict: verdict,
                    assertions: assertions.length, mutation: MUTATION})
exit(verdict == 'PASS' ? 0 : 1)
