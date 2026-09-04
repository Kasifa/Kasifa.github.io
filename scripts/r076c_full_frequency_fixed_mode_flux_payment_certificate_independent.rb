#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed exact-arithmetic audit for frozen R0.76C.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
STEM = 'r076c_full_frequency_fixed_mode_flux_payment'
MAIN = ROOT.join("research/#{STEM}.md")
PRIMARY = ROOT.join("research/#{STEM}_primary_audit.md")
SOURCE = ROOT.join('research/r076c_report-source.md')
FIXTURES = ROOT.join("scripts/#{STEM}_fixtures.json")
EXPECTED = ROOT.join("scripts/#{STEM}_expected.json")
CERTIFICATE = Pathname.new(ENV.fetch('R076C_JSON', ROOT.join("research/#{STEM}_certificate.json").to_s))
OUT = Pathname.new(ENV.fetch('R076C_RUBY_REPORT', ROOT.join("research/#{STEM}_independent_audit.md").to_s))
MUTATION = ENV.fetch('R076C_RUBY_MUTATION', '')

FROZEN = {
  "research/#{STEM}.md" => '2b2f4a2b353645e72ca54bfc06495a9f52329498b9c16a9e451ca7b3456f6bbf',
  "research/#{STEM}_primary_audit.md" => 'd60546eab80d2fa6ef633efeb0b34120d7b9f81a33249e500f8d94b9a8c15f74',
  'research/r076c_report-source.md' => 'be523d313f5a487fd0b1550cb948f1e05b117f6d1734b8d9cbfd5ab1b5d57b27',
  'research/r075b_bulk_clock_outer_padding_gate.md' => '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075r_outer_cap_spectral_concentration_obstruction.md' => 'e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3',
  'research/r075x_fixed_finite_mode_low_carrier_payment.md' => '8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763',
  'research/r076b_moderate_carrier_fixed_mode_flux_payment.md' => 'a8a4cc853ec1029cb52afee724a4a783da156bd57de5399c58a7f42e2ab0306d'
}.freeze
FIXTURES_SHA256 = '36d1612b57932fad7ff6e9a4375b842d4900b0868625cfb5d498ce89a4dcee82'
EXPECTED_SHA256 = '6dbd56d366b6b048acd769ff5b5eff303ede111153330de763ec04cee571ad52'

GROUPS = {
  'bindings' => %w[main_hash primary_hash source_hash clock_hash outer_hash low_hash moderate_hash],
  'inputs' => %w[fixture_hash expected_hash fixture_schema expected_schema],
  'integrity' => %w[utf8 controls tags display_opens display_closes references tex_qquad tex_zeta_prime],
  'geometry' => %w[delta_order support_radius support_bound plateau_length plateau_bound xi_mass xi_second_scale],
  'family' => %w[fixed_q integer_modes ordered_modes real_phases nonnegative_amplitudes real_speed dyadic_band no_carrier_upper constant_dependencies],
  'scaled' => %w[ell kappas alpha ratios scaled_gaps threshold high_spatial_branch n1r lambda ultrahigh_branch velocity physical_end original_heat_rates rescaled_real rescaled_imaginary real_band scaled_pde],
  'space' => %w[maximum_terms turan_power scaled_i chebyshev_measure scaled_jplus length_ratio margin normalized_derivative gap_free_space],
  'time_lemma' => %w[lemma_terms lemma_real_band family_hypothesis center_shift shifted_lower shifted_upper sublevel_measure subset_y interval_factor net_decay pointwise_tail weighted_tail endpoint_tail clock_lower imaginary_free gap_free_time],
  'ultrahigh' => %w[clock_t clock_mass zeta_onset zeta_linear gradient_prefactor clock_change weighted_lambda_power endpoint_lambda_power uniform_endpoint],
  'identity' => %w[square_pde advective_row energy_derivative xi_second dissipation heat_cancel identity_signs onset_endpoint complete_real_square],
  'point' => %w[point_g point_gz point_gzz point_gs point_residual],
  'payment' => %w[value_rows gradient_row gradient_paid terminal_paid dimensionless_payment low_branch full_frequency_union no_sign_drop],
  'scale' => %w[fibre_area mass_a mass_r flux_prefactor target_a target_r target_m r_cancel omega_power frozen_rate],
  'source_audit' => %w[nazarov friedland_yomdin theorem_restatement imaginary_statement local_corollary no_novelty primary_pass math_zero release_zero finite_not_proof no_figure],
  'boundary' => %w[fixed_q_only growing_q_open packets_open larger_field_open analytic_subblock_unused sign_route_rejected carrier_ibp_rejected version_m_conditional regularity_open singularity_open not_clay]
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
  warn "unknown R076C_RUBY_MUTATION: #{MUTATION}"
  exit 2
end
abort('duplicate mutation name in R0.76C Ruby suite') unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

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

bindings = FROZEN.sort.to_h do |path, expected_hash|
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
clock_end = Rational(fixtures.dig('clock', 'scaledClockEnd'))
ell = a_value * radius
kappas = modes.map { |mode| mode * ell }
alpha = kappas.first
ratios = kappas.map { |value| value / alpha }
gaps = kappas.each_cons(2).map { |left, right| right - left }
velocity = b_shear * radius / a_value
n1r = modes.first * radius
lambda_value = alpha**2 / a_value**2
original_heat = kappas.map { |value| value**2 / a_value**2 }
rescaled_real = kappas.map { |value| value**2 / alpha**2 }
rescaled_imag = kappas.map { |value| value * velocity / lambda_value }
threshold = 8 * q_count
temporal_end = clock_end * lambda_value
computed_case = {
  'ell' => qstr(ell),
  'kappas' => kappas.map { |value| qstr(value) },
  'alpha' => qstr(alpha),
  'ratios' => ratios.map { |value| qstr(value) },
  'gaps' => gaps.map { |value| qstr(value) },
  'threshold' => threshold,
  'highSpatialBranch' => alpha >= threshold,
  'n1R' => qstr(n1r),
  'lambda' => qstr(lambda_value),
  'ultraHighBranch' => lambda_value > 1,
  'dyadicBand' => modes.last <= 2 * modes.first,
  'v' => qstr(velocity),
  'physicalEnd' => qstr(clock_end * radius**2),
  'originalHeatRates' => original_heat.map { |value| qstr(value) },
  'rescaledRealMagnitudes' => rescaled_real.map { |value| qstr(value) },
  'rescaledImaginaryMagnitudes' => rescaled_imag.map { |value| qstr(value) },
  'realPartsWithinMinusFourMinusOne' => rescaled_real.min >= 1 && rescaled_real.max <= 4
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

shift = Rational(5, 2)
shifted_lower = -4 + shift
shifted_upper = -1 + shift
net_decay = -shift + [shifted_lower.abs, shifted_upper.abs].max
ledger = fixtures.fetch('lambdaLedger')
weighted_power = Rational(ledger.dig('gradientPrefactor', 'lambda')) +
                 Rational(ledger.dig('changeOfClock', 'sPerTau', 'lambda')) +
                 Rational(ledger.dig('changeOfClock', 'dsPerDtau', 'lambda')) +
                 Rational(ledger.dig('weightedTail', 'K')) * Rational(ledger.dig('clockMass', 'KPerH', 'lambda'))
endpoint_power = Rational(ledger.dig('endpointTail', 'T')) +
                 Rational(ledger.dig('endpointTail', 'K')) * Rational(ledger.dig('clockMass', 'KPerH', 'lambda'))
computed_time = {
  'maximumTerms' => 2 * q_count,
  'turanExponent' => 2 * q_count - 1,
  'sublevelMeasureLower' => '1/2',
  'centerShift' => qstr(shift),
  'shiftedRealLower' => qstr(shifted_lower),
  'shiftedRealUpper' => qstr(shifted_upper),
  'netDecay' => qstr(net_decay),
  'T' => qstr(temporal_end),
  'KOverH' => qstr(lambda_value),
  'weightedLambdaPower' => qstr(weighted_power),
  'endpointLambdaPower' => qstr(endpoint_power),
  'gapFactor' => '0'
}

cos_sin = phases.map { |value| phase_cos_sin(value) }
point_g = amplitudes.zip(cos_sin).sum(Rational(0)) { |amp, cs| amp * cs[0] }
point_gz = amplitudes.zip(kappas, cos_sin).sum(Rational(0)) { |amp, kappa, cs| amp * kappa * cs[1] }
point_gzz = -amplitudes.zip(kappas, cos_sin).sum(Rational(0)) { |amp, kappa, cs| amp * kappa**2 * cs[0] }
point_gs = amplitudes.zip(kappas, original_heat, cos_sin).sum(Rational(0)) do |amp, kappa, rate, cs|
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

tags = main_text.scan(/\\tag\{C\.(\d+)\}/).flatten.map(&:to_i)
refs = main_text.scan(/(?<![A-Za-z0-9_.])C\.(\d+)/).flatten.map(&:to_i)
checks = {
  'bindings' => {
    'main_hash' => bindings.fetch("research/#{STEM}.md").values.uniq.length == 1,
    'primary_hash' => bindings.fetch("research/#{STEM}_primary_audit.md").values.uniq.length == 1,
    'source_hash' => bindings.fetch('research/r076c_report-source.md').values.uniq.length == 1,
    'clock_hash' => bindings.fetch('research/r075b_bulk_clock_outer_padding_gate.md').values.uniq.length == 1,
    'outer_hash' => bindings.fetch('research/r075r_outer_cap_spectral_concentration_obstruction.md').values.uniq.length == 1,
    'low_hash' => bindings.fetch('research/r075x_fixed_finite_mode_low_carrier_payment.md').values.uniq.length == 1,
    'moderate_hash' => bindings.fetch('research/r076b_moderate_carrier_fixed_mode_flux_payment.md').values.uniq.length == 1
  },
  'inputs' => {
    'fixture_hash' => digest(FIXTURES) == FIXTURES_SHA256,
    'expected_hash' => digest(EXPECTED) == EXPECTED_SHA256,
    'fixture_schema' => fixtures['schema'] == 'r076c-full-frequency-fixed-mode-flux-payment-fixtures-v1',
    'expected_schema' => expected['schema'] == 'r076c-full-frequency-fixed-mode-flux-payment-expected-v1'
  },
  'integrity' => {
    'utf8' => [main_raw, primary_raw, source_raw].all? { |value| clean?(value) },
    'controls' => clean?(main_raw),
    'tags' => tags == (1..35).to_a,
    'display_opens' => main_text.scan('\\[').length == 35,
    'display_closes' => main_text.scan('\\]').length == 35,
    'references' => (refs.uniq - tags.uniq).empty?,
    'tex_qquad' => main_text !~ /(?<!\\)\bqquad\b/,
    'tex_zeta_prime' => !main_text.include?("zeta'Eds") && main_text.include?("\\zeta'E\\,ds")
  },
  'geometry' => {
    'delta_order' => 0 < delta0 && delta0 < delta,
    'support_radius' => computed_geometry['supportRadius'] == expected.dig('geometry', 'supportRadius'),
    'support_bound' => computed_geometry['supportWithinThreeHalves'] == expected.dig('geometry', 'supportWithinThreeHalves'),
    'plateau_length' => computed_geometry['centralPlateauLength'] == expected.dig('geometry', 'centralPlateauLength'),
    'plateau_bound' => computed_geometry['centralPlateauAtLeastOne'] == expected.dig('geometry', 'centralPlateauAtLeastOne'),
    'xi_mass' => computed_geometry['xiMassLowerOverPi'] == expected.dig('geometry', 'xiMassLowerOverPi'),
    'xi_second_scale' => computed_geometry['xiSecondCoefficientScale'] == expected.dig('geometry', 'xiSecondCoefficientScale')
  },
  'family' => {
    'fixed_q' => compact.include?('Fix an integer `q>=1`'),
    'integer_modes' => compact.include?('n_1,\\ldots,n_q\\in\\mathbb N'),
    'ordered_modes' => compact.include?('1\\le n_1<n_2<\\cdots<n_q\\le2n_1'),
    'real_phases' => compact.include?('\\phi_j\\in\\mathbb R'),
    'nonnegative_amplitudes' => compact.include?('A_j\\ge0'),
    'real_speed' => compact.include?('B\\in\\mathbb R'),
    'dyadic_band' => computed_case['dyadicBand'] == expected.dig('scaledCase', 'dyadicBand'),
    'no_carrier_upper' => compact.include?('with no carrier upper bound'),
    'constant_dependencies' => fragments?(compact, ['depending on `q` and the frozen profiles', 'not on `R`, the frequencies', 'phases, or `B`'])
  },
  'scaled' => {
    'ell' => computed_case['ell'] == expected.dig('scaledCase', 'ell'),
    'kappas' => computed_case['kappas'] == expected.dig('scaledCase', 'kappas'),
    'alpha' => computed_case['alpha'] == expected.dig('scaledCase', 'alpha'),
    'ratios' => computed_case['ratios'] == expected.dig('scaledCase', 'ratios'),
    'scaled_gaps' => computed_case['gaps'] == expected.dig('scaledCase', 'gaps'),
    'threshold' => computed_case['threshold'] == expected.dig('scaledCase', 'threshold'),
    'high_spatial_branch' => computed_case['highSpatialBranch'] == expected.dig('scaledCase', 'highSpatialBranch'),
    'n1r' => computed_case['n1R'] == expected.dig('scaledCase', 'n1R'),
    'lambda' => computed_case['lambda'] == expected.dig('scaledCase', 'lambda') && lambda_value == n1r**2,
    'ultrahigh_branch' => computed_case['ultraHighBranch'] == expected.dig('scaledCase', 'ultraHighBranch'),
    'velocity' => computed_case['v'] == expected.dig('scaledCase', 'v'),
    'physical_end' => computed_case['physicalEnd'] == expected.dig('scaledCase', 'physicalEnd'),
    'original_heat_rates' => computed_case['originalHeatRates'] == expected.dig('scaledCase', 'originalHeatRates'),
    'rescaled_real' => computed_case['rescaledRealMagnitudes'] == expected.dig('scaledCase', 'rescaledRealMagnitudes'),
    'rescaled_imaginary' => computed_case['rescaledImaginaryMagnitudes'] == expected.dig('scaledCase', 'rescaledImaginaryMagnitudes'),
    'real_band' => computed_case['realPartsWithinMinusFourMinusOne'] == expected.dig('scaledCase', 'realPartsWithinMinusFourMinusOne'),
    'scaled_pde' => fragments?(compact, ['G_s+vG_z-a^{-2}G_{zz}=0', '\\lambda=\\frac{\\alpha^2}{a^2}=(n_1R)^2>1'])
  },
  'space' => {
    'maximum_terms' => computed_space['maximumTerms'] == expected.dig('spatialObservation', 'maximumTerms'),
    'turan_power' => computed_space['turanExponent'] == expected.dig('spatialObservation', 'turanExponent'),
    'scaled_i' => computed_space['scaledIMeasure'] == expected.dig('spatialObservation', 'scaledIMeasure'),
    'chebyshev_measure' => computed_space['chebyshevMeasureLower'] == expected.dig('spatialObservation', 'chebyshevMeasureLower'),
    'scaled_jplus' => computed_space['scaledJplusMeasure'] == expected.dig('spatialObservation', 'scaledJplusMeasure'),
    'length_ratio' => computed_space['lengthRatio'] == expected.dig('spatialObservation', 'lengthRatio'),
    'margin' => computed_space['margin'] == expected.dig('spatialObservation', 'margin'),
    'normalized_derivative' => computed_space['normalizedPointDerivative'] == expected.dig('spatialObservation', 'normalizedPointDerivative'),
    'gap_free_space' => fragments?(compact, ['spatial observation proved in R0.76B', 'arbitrary frequency gaps'])
  },
  'time_lemma' => {
    'lemma_terms' => fragments?(compact, ['Q(\\tau)=\\sum_{r=1}^{N}c_re^{\\mu_r\\tau}', 'N\\le2q']),
    'lemma_real_band' => compact.include?('-4\\le\\operatorname {Re}\\mu_r\\le-1'),
    'family_hypothesis' => compact.include?('with every `Q(.;z)` an exponential polynomial satisfying C.12'),
    'center_shift' => computed_time['centerShift'] == expected.dig('temporalClock', 'centerShift') && compact.include?('Y(r)=e^{5r/2}Q(r)'),
    'shifted_lower' => computed_time['shiftedRealLower'] == expected.dig('temporalClock', 'shiftedRealLower'),
    'shifted_upper' => computed_time['shiftedRealUpper'] == expected.dig('temporalClock', 'shiftedRealUpper'),
    'sublevel_measure' => computed_time['sublevelMeasureLower'] == expected.dig('temporalClock', 'sublevelMeasureLower') && compact.include?('|E|\\ge\\frac12'),
    'subset_y' => compact.include?('`sup_E|Y|<=e^(5/2)(2I_Q)^(1/3)`'),
    'interval_factor' => compact.include?('`(C tau/|E|)^(N-1)<=C_q(1+tau)^(2q-1)`'),
    'net_decay' => computed_time['netDecay'] == expected.dig('temporalClock', 'netDecay'),
    'pointwise_tail' => fragments?(compact, ['(1+\\tau)^{3(2q-1)}e^{-3\\tau}', '\\int_0^1|Q(r)|^3dr']),
    'weighted_tail' => compact.include?('\\int_0^T\\tau k(\\tau)^{2/3}d\\tau'),
    'endpoint_tail' => fragments?(compact, ['k(T)^{2/3}\\le C_qT^{-2/3}K_T^{2/3}', 'T^(2(2q-1)+2/3)e^(-2T)']),
    'clock_lower' => compact.include?('T\\ge4'),
    'imaginary_free' => compact.include?('independent of all imaginary parts'),
    'gap_free_time' => compact.include?('independent of all imaginary parts and exponent gaps')
  },
  'ultrahigh' => {
    'clock_t' => computed_time['T'] == expected.dig('temporalClock', 'T') && compact.include?('T=4\\lambda'),
    'clock_mass' => computed_time['KOverH'] == expected.dig('temporalClock', 'KOverH') && compact.include?('K_T=\\int_0^{4\\lambda}k(\\tau)d\\tau=\\lambda H'),
    'zeta_onset' => fragments?(compact, ['`zeta(s)=eta_R(R^2s)`', '\\eta_R(0)=0']),
    'zeta_linear' => compact.include?('0\\le\\zeta(s)\\le C_\\eta s'),
    'gradient_prefactor' => compact.include?('a^(-2)int Xi_a|G_z|^2<=C_q lambda h^(2/3)'),
    'clock_change' => compact.include?('\\tau=\\lambda s'),
    'weighted_lambda_power' => computed_time['weightedLambdaPower'] == expected.dig('temporalClock', 'weightedLambdaPower') && compact.include?('C_q\\lambda^{-1/3}H^{2/3}'),
    'endpoint_lambda_power' => computed_time['endpointLambdaPower'] == expected.dig('temporalClock', 'endpointLambdaPower'),
    'uniform_endpoint' => fragments?(compact, ['h(4)^{2/3}=k(4\\lambda)^{2/3}', '\\le C_qH^{2/3}'])
  },
  'identity' => {
    'square_pde' => compact_primary.include?('(G^2)_s+v(G^2)_z-a^(-2)(G^2)_zz=-2a^(-2)|G_z|^2'),
    'advective_row' => computed_identity['advectiveRow'] == expected.dig('transportIdentity', 'advectiveRow'),
    'energy_derivative' => computed_identity['energyDerivative'] == expected.dig('transportIdentity', 'energyDerivative'),
    'xi_second' => computed_identity['xiSecondRow'] == expected.dig('transportIdentity', 'xiSecondRow'),
    'dissipation' => computed_identity['dissipationRow'] == expected.dig('transportIdentity', 'dissipationRow'),
    'heat_cancel' => computed_identity['heatCancellation'] == expected.dig('transportIdentity', 'heatCancellation'),
    'identity_signs' => fragments?(compact, ["E'(s)-a^{-2}\\int\\Xi_a''G^2", '+2a^{-2}\\int\\Xi_a|G_z|^2']),
    'onset_endpoint' => fragments?(compact, ['Since `zeta(0)=0`', "\\zeta(4)E(4)-\\int_0^4\\zeta'E\\,ds"]),
    'complete_real_square' => compact.include?('exact real-square identity')
  },
  'point' => {
    'point_g' => computed_point['G'] == expected.dig('point', 'G'),
    'point_gz' => computed_point['Gz'] == expected.dig('point', 'Gz'),
    'point_gzz' => computed_point['Gzz'] == expected.dig('point', 'Gzz'),
    'point_gs' => computed_point['Gs'] == expected.dig('point', 'Gs'),
    'point_residual' => computed_point['scaledPdeResidual'] == expected.dig('point', 'scaledPdeResidual')
  },
  'payment' => {
    'value_rows' => fragments?(compact, ['value part of C.11', '\\le C_qH^{2/3}']),
    'gradient_row' => compact.include?('a^(-2)int Xi_a|G_z|^2<=C_q lambda h^(2/3)'),
    'gradient_paid' => compact.include?('C.26 pays its time integral'),
    'terminal_paid' => compact.include?('Equation C.27 pays the terminal row'),
    'dimensionless_payment' => compact.include?('\\left|v\\int_0^4\\zeta\\int W_aG^2\\right| \\le C_qH^{2/3}'),
    'low_branch' => compact.include?('R0.76B supplies the complementary branch `alpha<=a`'),
    'full_frequency_union' => compact.include?('so C.4 holds at every carrier'),
    'no_sign_drop' => compact.include?('before any absolute value')
  },
  'scale' => {
    'fibre_area' => compact.include?('4\\pi\\delta_0a^2R^5H'),
    'mass_a' => computed_scale.dig('massPrefactor', 'a') == expected.dig('scaleLedger', 'massPrefactor', 'a'),
    'mass_r' => computed_scale.dig('massPrefactor', 'R') == expected.dig('scaleLedger', 'massPrefactor', 'R'),
    'flux_prefactor' => computed_scale['fluxPrefactor'] == expected.dig('scaleLedger', 'fluxPrefactor'),
    'target_a' => computed_scale.dig('afterMass', 'a') == expected.dig('scaleLedger', 'afterMass', 'a'),
    'target_r' => computed_scale.dig('afterMass', 'R') == expected.dig('scaleLedger', 'afterMass', 'R'),
    'target_m' => computed_scale.dig('afterMass', 'M') == expected.dig('scaleLedger', 'afterMass', 'M'),
    'r_cancel' => computed_scale.dig('normalized', 'R') == expected.dig('scaleLedger', 'normalized', 'R'),
    'omega_power' => computed_scale.dig('normalized', 'omega') == expected.dig('scaleLedger', 'normalized', 'omega'),
    'frozen_rate' => computed_scale['frozenRate'] == expected.dig('scaleLedger', 'frozenRate') && compact.include?('-\\frac2{11907}')
  },
  'source_audit' => {
    'nazarov' => fragments?(compact_source, ['F. L. Nazarov', 'https://www.mathnet.ru/eng/aa397']),
    'friedland_yomdin' => fragments?(compact_source, ['Omer Friedland and Yosef Yomdin', 'https://arxiv.org/abs/1107.0039']),
    'theorem_restatement' => compact_source.include?('Theorem 1.1'),
    'imaginary_statement' => compact_source.include?('imaginary parts do not enter the original inequality'),
    'local_corollary' => fragments?(compact_source, ['local corollary, not quoted', 'local change of variables']),
    'no_novelty' => compact_source.include?('not evidence of novelty or priority'),
    'primary_pass' => primary_text.include?('Current verdict: **PASS**'),
    'math_zero' => primary_text.include?('Mathematical blocker count: **0**'),
    'release_zero' => primary_text.include?('Release blocker count: **0**'),
    'finite_not_proof' => fragments?(compact, ['Finite fixtures may audit', 'not proof of the continuum exponential-polynomial lemma']),
    'no_figure' => compact.include?('No formal scientific figure or simulation is claimed')
  },
  'boundary' => {
    'fixed_q_only' => compact.include?('only for each fixed finite `q`'),
    'growing_q_open' => compact.include?('a quantitative constant suitable for `q=q(L)`'),
    'packets_open' => compact.include?('arbitrary growing packets'),
    'larger_field_open' => compact.include?('projection from a larger velocity'),
    'analytic_subblock_unused' => compact.include?('No density/carrier splitting'),
    'sign_route_rejected' => compact.include?('localized-current sign'),
    'carrier_ibp_rejected' => compact.include?('standalone oscillatory integration by parts'),
    'version_m_conditional' => compact.include?('same conditional `C_q(P_R^M)^(2/3)` consequence'),
    'regularity_open' => compact.include?('regularity'),
    'singularity_open' => compact.include?('singularity'),
    'not_clay' => [main_text, source_text, primary_text].all? { |value| value.include?('**NOT CLAY.**') }
  }
}

abort('R0.76C Ruby group order drift') unless checks.keys == GROUPS.keys
GROUPS.each do |group, names|
  abort("R0.76C Ruby assertion manifest drift in #{group}") unless checks.fetch(group).keys == names
end
unless MUTATION.empty?
  group = checks.find { |_name, values| values.key?(MUTATION) }
  group[1][MUTATION] = false
end

group_pass = checks.transform_values { |values| values.values.all? }
passed = group_pass.values.all?
total = checks.values.sum(&:length)
passed_count = checks.values.sum { |values| values.values.count(true) }
failed = checks.flat_map { |group, values| values.reject { |_name, value| value }.keys.map { |name| "#{group}.#{name}" } }

python_computed = certificate.fetch('computed')
cross_language = {
  'geometry' => python_computed.fetch('geometry') == computed_geometry,
  'scaledCase' => python_computed.fetch('scaledCase') == computed_case,
  'spatialObservation' => python_computed.fetch('spatialObservation') == computed_space,
  'temporalClock' => python_computed.fetch('temporalClock') == computed_time,
  'point' => python_computed.fetch('point') == computed_point,
  'transportIdentity' => python_computed.fetch('transportIdentity') == computed_identity,
  'scaleLedger' => python_computed.fetch('scaleLedger') == computed_scale
}
passed &&= cross_language.values.all?

lines = [
  '# R0.76C independent certificate audit',
  '',
  "- Verdict: **#{passed ? 'PASS' : 'FAIL'}**",
  "- Ruby assertions: #{passed_count}/#{total}",
  "- Mutation: `#{MUTATION.empty? ? 'none' : MUTATION}`",
  "- Python/Ruby exact sections identical: #{cross_language.values.all? ? 'PASS' : 'FAIL'} (#{cross_language.values.count(true)}/#{cross_language.length}).",
  "- Ultra-high fixture: `n_1R=#{qstr(n1r)}`, `lambda=#{qstr(lambda_value)}`, `T=#{qstr(temporal_end)}`.",
  "- Lambda ledger: weighted `#{qstr(weighted_power)}`, endpoint `#{qstr(endpoint_power)}`.",
  '- Finite arithmetic does not prove the continuum exponential-polynomial lemma.',
  '- Formal scientific figure: not applicable.',
  '- Boundary: fixed `q` exact shears only; growing packets, Version-M transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
]
unless failed.empty? && cross_language.values.all?
  lines += ['', '## Failures', '']
  lines.concat(failed.map { |name| "- `#{name}`" })
  cross_language.reject { |_name, value| value }.each_key { |name| lines << "- `cross_language.#{name}`" }
end
OUT.write(lines.join("\n") + "\n")
exit(passed ? 0 : 1)
