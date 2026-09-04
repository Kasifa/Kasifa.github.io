#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed exact-arithmetic audit for frozen R0.76B.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
STEM = 'r076b_moderate_carrier_fixed_mode_flux_payment'
MAIN = ROOT.join("research/#{STEM}.md")
PRIMARY = ROOT.join("research/#{STEM}_primary_audit.md")
SOURCE = ROOT.join('research/r076b_report-source.md')
FIXTURES = ROOT.join("scripts/#{STEM}_fixtures.json")
EXPECTED = ROOT.join("scripts/#{STEM}_expected.json")
CERTIFICATE = Pathname.new(ENV.fetch('R076B_JSON', ROOT.join("research/#{STEM}_certificate.json").to_s))
OUT = Pathname.new(ENV.fetch('R076B_RUBY_REPORT', ROOT.join("research/#{STEM}_independent_audit.md").to_s))
MUTATION = ENV.fetch('R076B_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => 'a8a4cc853ec1029cb52afee724a4a783da156bd57de5399c58a7f42e2ab0306d',
  "research/#{STEM}_primary_audit.md" => '0a6314c454021da284bbf157de36d6c2bd1683d600a21c8394f723acc26aa447',
  'research/r076b_report-source.md' => '362fcf898a533efaf4072c876dba09f4231c131ad1c48d48efc92c52215428fc',
  'research/r075b_bulk_clock_outer_padding_gate.md' => '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075w_full_frequency_two_harmonic_flux_payment.md' => '571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4',
  'research/r075x_fixed_finite_mode_low_carrier_payment.md' => '8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763',
  'research/r075z_unresolved_cluster_carrier_current_gate.md' => '30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97',
  'research/r076a_complete_clock_localized_current_sign_obstruction.md' => 'd23532f84702be1630daa0b8d56d02242571dd8a1f8024c59a7f71bec30f26eb'
}.freeze
FIXTURES_SHA256 = '1f9b3df9cb8ff3f9d22250ce425b837d40268829bf18cb3e12b3f7d2dca64bf2'
EXPECTED_SHA256 = '4533edf290e07f1fddc5df1b9ef1655a5623f4a3714e840b1c402cdf3b8db3f1'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash b_hash r_hash w_hash x_hash z_hash a_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema expected_schema],
  'integrity' => %w[utf8 controls tags display_opens display_closes references tex_left tex_fraction],
  'geometry' => %w[delta_order support_radius support_bound plateau_length plateau_bound xi_mass xi_second_scale],
  'family' => %w[fixed_q integer_modes ordered_modes real_phases dyadic_band alpha threshold high_branch inverse_radius scaled_gaps],
  'scaled' => %w[ell kappas ratios velocity heat_rates real_parts scaled_pde clock],
  'space_value' => %w[term_count turan_power scaled_i chebyshev_measure scaled_jplus length_ratio imaginary_roots gap_free_value],
  'space_derivative' => %w[compact_roots companion_family unit_window double_window margin jet_uniqueness alpha_factor point_derivative],
  'time_trace' => %w[temporal_terms temporal_power sublevel_measure real_bound imaginary_free gap_free_time terminal_trace],
  'identity' => %w[square_pde advective_row energy_derivative xi_second dissipation heat_cancel identity_signs onset],
  'point' => %w[point_g point_gz point_gzz point_gs point_residual endpoint_family],
  'payment' => %w[value_row xi_second_row gradient_ratio holder_time endpoint_payment dimensionless_payment full_real_square],
  'scale' => %w[fibre_area mass_a mass_r flux_prefactor target_a target_r target_m r_cancel omega_power frozen_rate],
  'source_audit' => %w[nazarov primary_restatement erdelyi brudnyi jaming_saba local_ode_proof no_novelty audit_pass math_zero release_zero finite_not_proof no_figure],
  'boundary' => %w[x_split n1r_closed ultrahigh_open growing_q_open packets_open analytic_subblock_unused carrier_ibp_rejected version_m_conditional regularity_open singularity_open not_clay]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

def digest(path)
  Digest::SHA256.file(path).hexdigest
end

def clean?(bytes)
  value = bytes.dup.force_encoding(Encoding::UTF_8)
  value.valid_encoding? && bytes.bytes.none? { |byte| (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127 }
end

def flat(value)
  value.gsub(/\s+/, ' ')
end

def fragments?(value, fragments)
  fragments.all? { |fragment| value.include?(fragment) }
end

def qstr(value)
  value.denominator == 1 ? value.numerator.to_s : "#{value.numerator}/#{value.denominator}"
end

def encoded(hash)
  hash.to_h { |key, value| [key, value.denominator == 1 ? value.numerator : qstr(value)] }
end

def poly_mul(left, right)
  result = Array.new(left.length + right.length - 1, Rational(0))
  left.each_with_index do |x_value, i|
    right.each_with_index { |y_value, j| result[i + j] += x_value * y_value }
  end
  result
end

def poly_derivative(poly, order = 1)
  result = poly.dup
  order.times { result = (1...result.length).map { |index| index * result[index] } }
  result
end

def symmetric_integral(poly)
  poly.each_with_index.sum(Rational(0)) do |value, index|
    index.even? ? Rational(2) * value / (index + 1) : Rational(0)
  end
end

def phase_cos_sin(value)
  {
    Rational(0) => [Rational(1), Rational(0)],
    Rational(1, 2) => [Rational(0), Rational(1)],
    Rational(1) => [Rational(-1), Rational(0)]
  }.fetch(value)
end

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  warn "unknown R076B_RUBY_MUTATION: #{MUTATION}"
  exit 2
end
abort('duplicate mutation name in R0.76B Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

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

frozen = FROZEN.dup
mutation_path = {
  'main_hash' => "research/#{STEM}.md",
  'primary_hash' => "research/#{STEM}_primary_audit.md",
  'source_hash' => 'research/r076b_report-source.md',
  'b_hash' => 'research/r075b_bulk_clock_outer_padding_gate.md',
  'r_hash' => 'research/r075r_outer_cap_spectral_concentration_obstruction.md',
  'w_hash' => 'research/r075w_full_frequency_two_harmonic_flux_payment.md',
  'x_hash' => 'research/r075x_fixed_finite_mode_low_carrier_payment.md',
  'z_hash' => 'research/r075z_unresolved_cluster_carrier_current_gate.md',
  'a_hash' => 'research/r076a_complete_clock_localized_current_sign_obstruction.md'
}[MUTATION]
frozen[mutation_path] = '0' * 64 if mutation_path
bindings = frozen.sort.to_h do |path, expected_hash|
  [path, {'expectedSha256' => expected_hash, 'observedSha256' => digest(ROOT.join(path))}]
end

delta0 = Rational(fixtures.dig('profile', 'delta0'))
delta = Rational(fixtures.dig('profile', 'delta'))
row = fixtures.fetch('scaledCase')
q_count = Integer(row.fetch('q'))
a_value = Rational(row.fetch('a'))
radius = Rational(row.fetch('R'))
b_shear = Rational(row.fetch('B'))
modes = row.fetch('frequencies').map { |value| Rational(value) }
amplitudes = row.fetch('amplitudes').map { |value| Rational(value) }
phases = row.fetch('phasesOverPi').map { |value| Rational(value) }
ell = a_value * radius
kappas = modes.map { |mode| mode * ell }
alpha = kappas.first
ratios = kappas.map { |value| value / alpha }
gaps = kappas.each_cons(2).map { |left, right| right - left }
velocity = b_shear * radius / a_value
heat_rates = kappas.map { |value| value**2 / a_value**2 }
threshold = 8 * q_count
clock_end = Rational(fixtures.dig('clock', 'clockEnd'))
computed_case = {
  'ell' => qstr(ell),
  'alphas' => kappas.map { |value| qstr(value) },
  'ratios' => ratios.map { |value| qstr(value) },
  'gaps' => gaps.map { |value| qstr(value) },
  'threshold' => threshold,
  'highBranch' => alpha >= threshold,
  'inverseRadiusEndpoint' => modes.first * radius == 1 && alpha == a_value,
  'dyadicBand' => modes.last <= 2 * modes.first,
  'v' => qstr(velocity),
  'physicalEnd' => qstr(clock_end * radius**2),
  'heatRates' => heat_rates.map { |value| qstr(value) },
  'realPartsWithinFour' => heat_rates.max <= 4
}

support_radius = 1 + delta / a_value
plateau_length = 2 - 2 * delta / a_value
computed_geometry = {
  'supportRadius' => qstr(support_radius),
  'supportWithinThreeHalves' => support_radius <= Rational(3, 2),
  'centralPlateauLength' => qstr(plateau_length),
  'centralPlateauAtLeastOne' => plateau_length >= 1,
  'xiMassLowerOverPi' => qstr(2 * delta0),
  'xiSecondCoefficientScale' => qstr(1 / a_value)
}

windows = fixtures.fetch('spatialWindows')
i_length = Rational(windows.dig('I', 1)) - Rational(windows.dig('I', 0))
jp_length = Rational(windows.dig('Jplus', 1)) - Rational(windows.dig('Jplus', 0))
scaled_i = alpha * i_length
cheb_lower = scaled_i / Rational(windows.fetch('chebyshevThreshold'))
scaled_jp = alpha * jp_length
margin = alpha * (Rational(windows.dig('Jplus', 1)) - Rational(windows.dig('J', 1)))
computed_space = {
  'maximumTerms' => 2 * q_count,
  'turanExponent' => 2 * q_count - 1,
  'scaledIMeasure' => qstr(scaled_i),
  'chebyshevMeasureLower' => qstr(cheb_lower),
  'scaledJplusMeasure' => qstr(scaled_jp),
  'lengthRatio' => qstr(scaled_jp / cheb_lower),
  'margin' => qstr(margin),
  'normalizedPointDerivative' => qstr(2 * kappas[1] / alpha)
}
computed_time = {
  'maximumTerms' => 2 * q_count,
  'turanExponent' => 2 * q_count - 1,
  'sublevelMeasureLower' => '2',
  'realPartBound' => '4',
  'gapFactor' => '0'
}

cos_sin = phases.map { |value| phase_cos_sin(value) }
point_g = amplitudes.zip(cos_sin).sum(Rational(0)) { |amp, cs| amp * cs[0] }
point_gz = amplitudes.zip(kappas, cos_sin).sum(Rational(0)) { |amp, kappa, cs| amp * kappa * cs[1] }
point_gzz = -amplitudes.zip(kappas, cos_sin).sum(Rational(0)) { |amp, kappa, cs| amp * kappa**2 * cs[0] }
point_gs = amplitudes.zip(kappas, heat_rates, cos_sin).sum(Rational(0)) do |amp, kappa, rate, cs|
  amp * (-rate * cs[0] - kappa * velocity * cs[1])
end
residual = point_gs + velocity * point_gz - point_gzz / a_value**2
computed_point = {
  'G' => qstr(point_g),
  'Gz' => qstr(point_gz),
  'Gzz' => qstr(point_gzz),
  'Gs' => qstr(point_gs),
  'scaledPdeResidual' => qstr(residual)
}

identity = fixtures.fetch('transportIdentity')
i_velocity = Rational(identity.fetch('v'))
i_time = Rational(identity.fetch('s'))
i_a = Rational(identity.fetch('a'))
xi = [1, 0, -2, 0, 1].map { |value| Rational(value) }
w_kernel = poly_derivative(xi)
g_poly = [-i_velocity * i_time, Rational(1)]
g_squared = poly_mul(g_poly, g_poly)
advective = i_velocity * symmetric_integral(poly_mul(w_kernel, g_squared))
energy_derivative = -2 * i_velocity * symmetric_integral(poly_mul(xi, g_poly))
xi_second = symmetric_integral(poly_mul(poly_derivative(xi, 2), g_squared))
dissipation = symmetric_integral(xi)
heat_cancellation = -xi_second / i_a**2 + 2 * dissipation / i_a**2
computed_identity = {
  'advectiveRow' => qstr(advective),
  'energyDerivative' => qstr(energy_derivative),
  'xiSecondRow' => qstr(xi_second),
  'dissipationRow' => qstr(dissipation),
  'heatCancellation' => qstr(heat_cancellation)
}

computed_scale = {
  'fluxPrefactor' => encoded('a' => Rational(2), 'R' => Rational(3), 'v' => Rational(1)),
  'massPrefactor' => encoded('a' => Rational(2), 'R' => Rational(5), 'H' => Rational(1)),
  'afterMass' => encoded('a' => Rational(2, 3), 'R' => Rational(-1, 3), 'M' => Rational(2, 3)),
  'normalized' => encoded('a' => Rational(2, 3), 'R' => Rational(0),
                          'omega' => Rational(1, 3), 'p' => Rational(2, 3)),
  'frozenRate' => qstr(-Rational(fixtures.dig('frozenScales', 'cGamma')) / 12)
}

tags = main_text.scan(/\\tag\{B\.(\d+)\}/).flatten.map(&:to_i)
references = main_text.scan(/\bB\.(\d+)\b/).flatten.map(&:to_i)
display_opens = main_text.scan(/^\\\[$/).length
display_closes = main_text.scan(/^\\\]$/).length
assertions = []
record = lambda do |name, group, condition, details = nil|
  assertions << {'name' => name, 'group' => group,
                 'pass' => condition && !GROUPS.fetch(group).include?(MUTATION), 'details' => details}
end

record.call('frozen source bindings', 'bindings',
            bindings.values.all? { |entry| entry['expectedSha256'] == entry['observedSha256'] }, bindings)
record.call('fixture and expected bindings', 'inputs',
            digest(FIXTURES) == FIXTURES_SHA256 && digest(EXPECTED) == EXPECTED_SHA256 &&
              fixtures.fetch('schema').end_with?('fixtures-v1') && expected.fetch('schema').end_with?('expected-v1'))
record.call('UTF-8, controls, equation tags, displays, references, and TeX escapes', 'integrity',
            clean?(main_raw) && clean?(primary_raw) && clean?(source_raw) && tags == (1..41).to_a &&
              display_opens == 41 && display_closes == 41 && (references.uniq - tags.uniq).empty? &&
              main_text.include?('\\begin{aligned}') && main_text.include?('-\\frac2{11907}'),
            {'tags' => tags.length, 'opens' => display_opens, 'closes' => display_closes})
record.call('frozen primitive geometry', 'geometry',
            0 < delta0 && delta0 < delta && computed_geometry == expected.fetch('geometry') &&
              fragments?(compact, ['\\Xi_a(z)=\\int_{-\\infty}^zW_a(r)', "\\|\\Xi_a''\\|_1\\le Ca",
                                   'supported in `J`', '4\\pi\\delta_0a^2R^5H']), computed_geometry)
record.call('fixed-q dyadic high branch and inverse-radius endpoint', 'family',
            computed_case == expected.fetch('scaledCase') &&
              fragments?(compact, ['Fix an integer `q>=1`', 'n_1,\\ldots,n_q\\in\\mathbb N',
                                   '\\phi_j\\in\\mathbb R', 'n_q\\le2n_1', 'n_1R\\le1',
                                   '8q\\le\\alpha\\le a', '\\kappa_q\\le2\\alpha']), computed_case)
record.call('scaled variables, clock, heat rates, and PDE', 'scaled',
            residual.zero? && velocity == 1 && heat_rates.max <= 4 &&
              fragments?(compact, ['s=\\frac t{R^2}', 'v=\\frac{BR}{a}',
                                   '\\partial_sG+v\\partial_zG-a^{-2}\\partial_z^2G=0',
                                   '0\\le\\kappa_j^2/a^2\\le4']))
record.call('carrier-scaled Turan--Nazarov value observation', 'space_value',
            computed_space == expected.fetch('spatialObservation') &&
              fragments?(compact, ['r_j=\\kappa_j/\\alpha\\in[1,2]', '|E|\\ge\\frac\\alpha2',
                                   '|alpha J^+|/|E|<=8', '(8C)^{2q-1}',
                                   'No frequency separation enters the constant']), computed_space)
record.call('compact unit-window derivative observation', 'space_derivative',
            margin >= Rational(windows.fetch('localHalfWidth')) &&
              Rational(computed_space.fetch('normalizedPointDerivative')) == Rational(289, 144) &&
              fragments?(compact, ['\\prod_{j=1}^m(\\partial_x^2+r_j^2)f=0', 'complete initial jet',
                                   'contradicting ODE uniqueness', 'concentric double window',
                                   "g'=alpha f'(alpha z)", '\\alpha^{-1}\\|G_z(s)\\|']), {'margin' => qstr(margin)})
record.call('gap-free complete-clock terminal trace', 'time_trace',
            computed_time == expected.fetch('temporalTrace') &&
              fragments?(compact, ['N_z\\le2q', '-\\kappa_j^2/a^2\\pm i\\kappa_jv',
                                   'independent of `v` and of all gaps', 'h(4)\\le C_qH']), computed_time)
record.call('exact square transport identity and polynomial fixture', 'identity',
            computed_identity == expected.fetch('transportIdentity') && advective == energy_derivative &&
              heat_cancellation.zero? && fragments?(compact, ['=-2a^{-2}|G_z|^2',
                                                               "=E'(s)-a^{-2}\\int\\Xi_a''G^2",
                                                               '+2a^{-2}\\int\\Xi_a|G_z|^2',
                                                               'Since `zeta(0)=0`']), computed_identity)
record.call('exact endpoint-family point and PDE residual', 'point',
            computed_point == expected.fetch('point') && residual.zero? && alpha == a_value && modes.first * radius == 1,
            computed_point)
record.call('complete real-field payment', 'payment',
            fragments?(compact, ['\\left(\\frac\\alpha a\\right)^2h(s)^{2/3}', '\\le C_qH^{2/3}',
                                 'complete square `G^2`', 'all cross-cluster products', 'no localized-current sign']) &&
              fragments?(compact_primary, ['terminal row is positive', 'localized gradient row positive',
                                           'No row is dropped by sign', 'standalone carrier-block method']))
record.call('physical scale and normalization ledger', 'scale',
            computed_scale == expected.fetch('scaleLedger') &&
              fragments?(compact, ['\\frac{a^2R^3}{2}v', 'C_qa^{2/3}R^{-1/3}',
                                   'R^{-2}\\omega M', '\\frac\\omega R', '-\\frac2{11907}']), computed_scale)
record.call('primary-source, mathematical-audit, and no-figure boundary', 'source_audit',
            fragments?(compact_source, ['https://www.mathnet.ru/eng/aa397', 'https://arxiv.org/abs/1107.0039',
                                        'https://arxiv.org/abs/1602.02315',
                                        'https://doi.org/10.1006/jath.2001.3576',
                                        'https://arxiv.org/abs/2311.17714', 'proves that statement directly',
                                        'not evidence of novelty or priority']) &&
              fragments?(compact_primary, ['Current verdict: **PASS**', 'Mathematical blocker count: **0**',
                                           'Release blocker count: **0**', 'not represented as proof',
                                           'No formal figure is required']))
record.call('exact theorem and open-claim boundary', 'boundary',
            fragments?(compact, ['R0.75X with `C_0=8q`', 'under the full condition B.4',
                                 'entire exact-shear carrier range', 'ultra-high sector `n_1R>1`',
                                 'constant uniform in growing `q`', 'arbitrary growing packets',
                                 'The proof above restores the full real field', 'R0.76A',
                                 'Version-M measurement row', 'regularity', 'singularity', '**NOT CLAY.**']) &&
              certificate.dig('boundary', 'fixedQInverseRadiusPayment') == 'PROVED' &&
              certificate.dig('boundary', 'analyticDensitySubblock') == 'NOT_USED' &&
              certificate.dig('boundary', 'standaloneCarrierSpatialIntegrationByParts') == 'REJECTED' &&
              certificate.dig('boundary', 'clayProblemSolved') == false)

verdict = assertions.all? { |item| item.fetch('pass') } ? 'PASS' : 'FAIL'
report = [
  '# R0.76B independent Ruby audit',
  '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{assertions.count { |item| item.fetch('pass') }}/#{assertions.length}",
  "- Mutation challenge: #{MUTATION.empty? ? 'none' : MUTATION}",
  "- Blocker count: #{verdict == 'PASS' ? 0 : 1}",
  '',
  'The audit independently recomputes the q=3 inverse-radius endpoint,',
  'carrier-scaled window ratios, temporal exponent bounds, exact PDE point,',
  'polynomial energy identity, and scale ledger.  Finite arithmetic is not',
  'proof of the continuum Turan--Nazarov or compact-ODE arguments.',
  '',
  'The theorem concerns the complete real square for fixed q and n_1 R <= 1.',
  'Ultra-high carriers, growing packets, Version-M transfer, regularity, and',
  'singularity remain OPEN. **NOT CLAY.**',
  ''
]
OUT.write(report.join("\n"))
puts JSON.generate({suite: 'r076b-independent-ruby-audit-v1', verdict: verdict,
                    assertions: assertions.length, mutation: MUTATION})
exit(verdict == 'PASS' ? 0 : 1)
