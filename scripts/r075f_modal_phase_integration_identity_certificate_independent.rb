#!/usr/bin/env ruby
# Independent ordered-pair and Fejer verifier for frozen R0.75F.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075f_modal_phase_integration_identity.md'
PRIMARY_AUDIT = ROOT + 'research/r075f_modal_phase_integration_identity_primary_audit.md'
REPORT_SOURCE = ROOT + 'research/r075f_report-source.md'
FIXTURES = ROOT + 'scripts/r075f_modal_phase_integration_identity_fixtures.json'
EXPECTED = ROOT + 'scripts/r075f_modal_phase_integration_identity_expected.json'
JSON_PATH = Pathname.new(
  ENV.fetch(
    'R075F_JSON',
    (ROOT + 'research/r075f_modal_phase_integration_identity_certificate.json').to_s
  )
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075F_RUBY_REPORT',
    (ROOT + 'research/r075f_modal_phase_integration_identity_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075F_RUBY_MUTATION', '')
SCHEMA = 'r075f-modal-phase-integration-identity-certificate-v1'

FROZEN_SOURCES = {
  'research/r075b_bulk_clock_outer_padding_gate.md' =>
    '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075f_modal_phase_integration_identity.md' =>
    'f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440',
  'research/r075f_modal_phase_integration_identity_primary_audit.md' =>
    '4320ac5544b51888eb8088db98e500a9877ecfe9a984f156783cac096a27c99a',
  'research/r075f_report-source.md' =>
    '3838603ea143b2efe1e96995fac34d7e8565211dc91dd244ab01cf6d526f3481'
}.freeze
FIXTURES_SHA256 = '0ce9b3bf060f4b38fe497be7bcdad3d1bdbd51ea27ff9aab146c8b10f5a0aced'
EXPECTED_SHA256 = '3946cb2cc992f4d1e55b88a7be9b7ecd8529e76a437093af6583f8fdacf2ddc9'

NEGATIVE_MUTATIONS = %w[
  source_drift audit_drift report_source_drift dependency_drift
  dependency_table_missing fixture_drift expected_drift tag reference display
  control mode_n_shear_sign mode_m_shear_sign ell_sign product_cross_two
  phase_lhs_sign no_division period_factor endpoint_half dissipation_factor
  gradient_nm_sign cutoff_ell_sign eta_initial eta_terminal time_ibp_sign
  vertical_ibp_sign square_decomposition transport_reconstruction
  cancellation_residual diagonal_identity fejer_even_allowed fejer_count
  fejer_fourth fejer_weight_bound fejer_mean fejer_ratio_n3 fejer_ratio_n5
  fejer_ratio_n7 fejer_divergence counterexample_claim e24_closed full_clock
  clay
].freeze

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  abort("unknown R075F_RUBY_MUTATION: #{MUTATION}")
end

def rational(value)
  Rational(value.to_s)
end

def complex_value(pair)
  Complex(rational(pair[0]), rational(pair[1]))
end

def rational_text(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

def complex_array(value)
  [rational_text(value.real), rational_text(value.imag)]
end

def poly_add(*values)
  [
    values.sum { |value| value[0] },
    values.sum { |value| value[1] }
  ]
end

def poly_scale(scale, value)
  [scale * value[0], scale * value[1]]
end

def poly_array(value)
  value.map { |coefficient| rational_text(coefficient) }
end

text = MAIN.read
flat_text = text.gsub(/\s+/, ' ')
scan_text = text + (MUTATION == 'control' ? "\u0001" : '')
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_payload = JSON.parse(JSON_PATH.read)

source_expectations = FROZEN_SOURCES.dup
source_expectations['research/r075f_modal_phase_integration_identity.md'] =
  '0' * 64 if MUTATION == 'source_drift'
source_expectations[
  'research/r075f_modal_phase_integration_identity_primary_audit.md'
] = '0' * 64 if MUTATION == 'audit_drift'
source_expectations['research/r075f_report-source.md'] =
  '0' * 64 if MUTATION == 'report_source_drift'
source_expectations['research/r075b_bulk_clock_outer_padding_gate.md'] =
  '0' * 64 if MUTATION == 'dependency_drift'
source_rows = source_expectations.keys.sort.to_h do |path|
  [path, [
    source_expectations[path],
    Digest::SHA256.file(ROOT + path).hexdigest
  ]]
end

fixture_expected_hash = MUTATION == 'fixture_drift' ? '0' * 64 : FIXTURES_SHA256
expected_expected_hash = MUTATION == 'expected_drift' ? '0' * 64 : EXPECTED_SHA256
fixture_hash = Digest::SHA256.file(FIXTURES).hexdigest
expected_hash = Digest::SHA256.file(EXPECTED).hexdigest

# Compute F.5 first and then F.6--F.8 via Ruby Complex arithmetic.
product = fixtures.fetch('productCase')
n = product.fetch('n')
m = product.fetch('m')
b = rational(product.fetch('b'))
fn = complex_value(product.fetch('fN'))
fnp = complex_value(product.fetch('fNPrime'))
fnpp = complex_value(product.fetch('fNSecond'))
fm = complex_value(product.fetch('fM'))
fmp = complex_value(product.fetch('fMPrime'))
fmpp = complex_value(product.fetch('fMSecond'))
cfm = fm.conjugate
cfmp = fmp.conjugate
cfmpp = fmpp.conjugate

n_shear_sign = MUTATION == 'mode_n_shear_sign' ? 1 : -1
m_shear_sign = MUTATION == 'mode_m_shear_sign' ? -1 : 1
dtfn = fnpp - n * n * fn + Complex(0, n_shear_sign * n * b) * fn
dtcfm = cfmpp - m * m * cfm + Complex(0, m_shear_sign * m * b) * cfm
g = fn * cfm
dtg = dtfn * cfm + fn * dtcfm
cross = fnp * cfmp
cross_factor = MUTATION == 'product_cross_two' ? 1 : 2
gsecond = fnpp * cfm + cross_factor * cross + fn * cfmpp
ell = MUTATION == 'ell_sign' ? n - m : m - n
lhs_sign = MUTATION == 'phase_lhs_sign' ? -1 : 1
phase_lhs = Complex(0, lhs_sign * ell * b) * g
phase_rhs = dtg - gsecond + 2 * cross + (n * n + m * m) * g

product_observed = {
  'ell' => ell,
  'nm' => n * m,
  'dtFN' => complex_array(dtfn),
  'dtConjugateFM' => complex_array(dtcfm),
  'g' => complex_array(g),
  'dtG' => complex_array(dtg),
  'gSecond' => complex_array(gsecond),
  'phaseLhs' => complex_array(phase_lhs),
  'phaseRhs' => complex_array(phase_rhs)
}
no_division =
  MUTATION != 'no_division' &&
  text.include?('No division by \\(b\\) or \\(\\ell\\) occurs.')

# Independently assemble the normalized forms from their definitions.
moment = fixtures.fetch('phaseMomentCase')
primary = moment.fetch('primaryOrderedPair')
endpoint = complex_value(primary.fetch('endpoint'))
eta_prime = complex_value(primary.fetch('etaPrime'))
xi_second = complex_value(primary.fetch('xiSecond'))
mass = complex_value(primary.fetch('mass'))
vertical_gradient = complex_value(primary.fetch('verticalGradient'))
mn = moment.fetch('n') * moment.fetch('m')
mell = MUTATION == 'ell_sign' ?
  moment.fetch('n') - moment.fetch('m') :
  moment.fetch('m') - moment.fetch('n')
eta_initial = rational(moment.fetch('etaAtInitial'))
eta_terminal = rational(moment.fetch('etaAtTerminal'))
eta_initial = Rational(1) if MUTATION == 'eta_initial'
eta_terminal = Rational(0) if MUTATION == 'eta_terminal'

period_over_pi = MUTATION == 'period_factor' ? Rational(1) : Rational(2)
half_energy = MUTATION == 'endpoint_half' ? Rational(1) : Rational(1, 2)
endpoint_factor = half_energy * period_over_pi
cutoff_factor = half_energy * period_over_pi
dissipation_factor =
  MUTATION == 'dissipation_factor' ? Rational(1) : period_over_pi
gradient_nm = MUTATION == 'gradient_nm_sign' ? -mn : mn
cutoff_square_sign = MUTATION == 'cutoff_ell_sign' ? 1 : -1
time_sign = MUTATION == 'time_ibp_sign' ? 1 : -1
vertical_sign = MUTATION == 'vertical_ibp_sign' ? 1 : -1
mass_coefficient =
  if MUTATION == 'square_decomposition'
    mell * mell - 2 * mn
  else
    mell * mell + 2 * mn
  end

single_transport =
  eta_terminal * endpoint +
  time_sign * eta_prime +
  vertical_sign * xi_second +
  mass_coefficient * mass +
  2 * vertical_gradient
endpoint_off = endpoint_factor * 2 * endpoint.real
cutoff_off = cutoff_factor * 2 * (
  eta_prime.real + xi_second.real +
  cutoff_square_sign * mell * mell * mass.real
)
dissipation_off = dissipation_factor * 2 * (
  vertical_gradient.real + gradient_nm * mass.real
)
transport_multiplier = MUTATION == 'transport_reconstruction' ? 2 : 1
transport = transport_multiplier * 2 * single_transport.real
reconstructed = endpoint_off - cutoff_off + dissipation_off
cancellation_remainder =
  transport - reconstructed +
  (MUTATION == 'cancellation_residual' ? Rational(1) : Rational(0))
diagonal_direct = MUTATION != 'diagonal_identity'

normalization_observed = {
  'horizontalPeriodOverPi' => rational_text(period_over_pi),
  'endpointHalfEnergyFactorOverPi' => rational_text(endpoint_factor),
  'cutoffHalfEnergyFactorOverPi' => rational_text(cutoff_factor),
  'dissipationPeriodFactorOverPi' => rational_text(dissipation_factor),
  'horizontalGradientMultiplier' => rational_text(gradient_nm)
}
phase_observed = {
  'ell' => mell,
  'ellSquared' => mell * mell,
  'nm' => mn,
  'nSquaredPlusMSquared' => mass_coefficient,
  'singlePairTOverPiBeforeRealSum' => complex_array(single_transport),
  'endpointOffOverPi' => rational_text(endpoint_off),
  'cutoffOffOverPi' => rational_text(cutoff_off),
  'dissipationOffOverPi' => rational_text(dissipation_off),
  'transportOverPi' => rational_text(transport),
  'endpointMinusCutoffPlusDissipationOverPi' => rational_text(reconstructed),
  'postSubstitutionOffDiagonalRemainderOverPi' =>
    rational_text(cancellation_remainder)
}

# Directly integrate a genuine two-mode solution in the formal ring Q[p],
# p=pi^-2. This calculation does not use the arbitrary moment fixture.
closed = fixtures.fetch('closedSolutionCase')
cn = closed.fetch('n')
cm = closed.fetch('m')
cell = MUTATION == 'ell_sign' ? cn - cm : cm - cn
cb_over_pi = rational(closed.fetch('bOverPi'))
decay = rational(closed.fetch('decayRate'))
eta_rate = rational(closed.fetch('etaExponentialRate'))
wave_n = closed.fetch('x3WaveN')
wave_m = closed.fetch('x3WaveM')
elementary = closed.fetch('elementaryIntegrals')
int_cos = elementary.fetch('integralCosPiT').map { |value| rational(value) }
int_t_cos = elementary.fetch('integralTCosPiT').map { |value| rational(value) }
pi_int_t_sin =
  elementary.fetch('piTimesIntegralTSinPiT').map { |value| rational(value) }

closed_endpoint_diag = [Rational(1), Rational(0)]
closed_endpoint_off = [Rational(-1, 2), Rational(0)]
closed_cutoff_diag = [Rational(3), Rational(0)]
cutoff_time_coefficient =
  eta_rate - cell * cell +
  (MUTATION == 'cutoff_ell_sign' ? cell * cell : -cell * cell)
closed_cutoff_off = poly_scale(
  Rational(1, 2),
  poly_add(int_cos, poly_scale(cutoff_time_coefficient, int_t_cos))
)
closed_dissipation_diag = [Rational(2), Rational(0)]
vertical_multiplier = wave_n * wave_m
horizontal_multiplier =
  MUTATION == 'gradient_nm_sign' ? -cn * cm : cn * cm
closed_dissipation_off = poly_scale(
  vertical_multiplier + horizontal_multiplier,
  int_t_cos
)
direct_sign = MUTATION == 'phase_lhs_sign' ? -1 : 1
direct_factor = MUTATION == 'transport_reconstruction' ? 2 : 1
closed_transport_direct = poly_scale(
  direct_factor * direct_sign * Rational(cell) * cb_over_pi / 2,
  pi_int_t_sin
)
closed_left = poly_add(
  closed_endpoint_diag,
  closed_endpoint_off,
  closed_dissipation_diag,
  closed_dissipation_off
)
closed_right = poly_add(
  closed_cutoff_diag,
  closed_cutoff_off,
  closed_transport_direct
)

closed_time_endpoint = poly_scale(eta_terminal, closed_endpoint_off)
closed_time_eta_prime = poly_scale(
  Rational(1, 2),
  poly_add(int_cos, poly_scale(eta_rate, int_t_cos))
)
closed_time_direct = poly_scale(
  Rational(1, 2),
  poly_add(
    poly_scale(-2 * decay, int_t_cos),
    poly_scale(direct_sign * Rational(cell) * cb_over_pi, pi_int_t_sin)
  )
)
closed_time_by_parts = poly_add(
  closed_time_endpoint,
  poly_scale(time_sign, closed_time_eta_prime)
)
g_wave = wave_n - wave_m
closed_vertical_left = poly_scale(
  Rational(-vertical_sign * g_wave * g_wave, 2),
  int_t_cos
)
closed_vertical_right = poly_scale(
  Rational(-vertical_sign * cell * cell, 2),
  int_t_cos
)
closed_twice_gradient = poly_scale(vertical_multiplier, int_t_cos)
closed_mass_multiplier =
  MUTATION == 'square_decomposition' ?
  cn * cn - cm * cm :
  cn * cn + cm * cm
closed_mass = poly_scale(Rational(closed_mass_multiplier, 2), int_t_cos)
closed_phase_sum = poly_add(
  closed_time_direct,
  closed_vertical_left,
  closed_twice_gradient,
  closed_mass
)
closed_f17_right = poly_add(
  closed_endpoint_off,
  poly_scale(-1, closed_cutoff_off),
  closed_dissipation_off
)
closed_f17_residual = poly_add(
  closed_transport_direct,
  poly_scale(-1, closed_f17_right),
  MUTATION == 'cancellation_residual' ?
    [Rational(1), Rational(0)] :
    [Rational(0), Rational(0)]
)
closed_f18_left = poly_add(closed_endpoint_diag, closed_dissipation_diag)
closed_f18_right =
  MUTATION == 'diagonal_identity' ?
  [Rational(0), Rational(0)] :
  closed_cutoff_diag

closed_observed = {
  'endpointDiag' => poly_array(closed_endpoint_diag),
  'endpointOff' => poly_array(closed_endpoint_off),
  'cutoffDiag' => poly_array(closed_cutoff_diag),
  'cutoffOff' => poly_array(closed_cutoff_off),
  'dissipationDiag' => poly_array(closed_dissipation_diag),
  'dissipationOff' => poly_array(closed_dissipation_off),
  'transportDirect' => poly_array(closed_transport_direct),
  'localEnergyLeft' => poly_array(closed_left),
  'localEnergyRight' => poly_array(closed_right),
  'timeDerivativeDirect' => poly_array(closed_time_direct),
  'timeEndpoint' => poly_array(closed_time_endpoint),
  'timeEtaPrime' => poly_array(closed_time_eta_prime),
  'timeEndpointMinusEtaPrime' => poly_array(closed_time_by_parts),
  'verticalIbpLeft' => poly_array(closed_vertical_left),
  'verticalIbpRight' => poly_array(closed_vertical_right),
  'phaseTimeRow' => poly_array(closed_time_direct),
  'phaseMinusGSecondRow' => poly_array(closed_vertical_left),
  'phaseTwiceGradientRow' => poly_array(closed_twice_gradient),
  'phaseMassRow' => poly_array(closed_mass),
  'phaseRowsSum' => poly_array(closed_phase_sum),
  'f17Right' => poly_array(closed_f17_right),
  'f17Residual' => poly_array(closed_f17_residual),
  'f18Left' => poly_array(closed_f18_left),
  'f18Right' => poly_array(closed_f18_right)
}

# Count ordered differences with explicit nested loops, not the Python formula.
ns = fixtures.fetch('fejerOddN').dup
ns << 4 if MUTATION == 'fejer_even_allowed'
fejer_rows = {}
ns.each do |current_n|
  half = (current_n - 1) / 2
  modes = (-half..half).to_a
  counts = Hash.new(0)
  modes.each do |left|
    modes.each do |right|
      counts[left - right] += 1
    end
  end
  counts[0] += 1 if MUTATION == 'fejer_count' && current_n == 3
  count_values = (-(current_n - 1)..(current_n - 1)).map do |difference|
    counts[difference]
  end
  fourth = count_values.sum { |value| value * value }
  fourth += 1 if MUTATION == 'fejer_fourth' && current_n == 5
  x_mean = Rational(modes.length, current_n * current_n)
  a_squared_mean = Rational(modes.length, current_n)
  x_mean += Rational(1, 7) if MUTATION == 'fejer_mean' && current_n == 7
  localized = Rational(fourth, current_n**3)
  ratio = localized / (x_mean * a_squared_mean)
  ratio += 1 if MUTATION == "fejer_ratio_n#{current_n}"
  weight_bound =
    if MUTATION == 'fejer_weight_bound' && current_n == 3
      false
    else
      modes.length == current_n
    end
  fejer_rows[current_n.to_s] = {
    'differenceCounts' => count_values,
    'fourthMoment' => rational_text(Rational(fourth)),
    'xMean' => rational_text(x_mean),
    'aSquaredMean' => rational_text(a_squared_mean),
    'localizedMean' => rational_text(localized),
    'ratio' => rational_text(ratio),
    'odd' => current_n.odd?,
    'realSymmetric' => modes == modes.reverse.map { |value| -value },
    'weightBoundByTriangle' => weight_bound
  }
end
divergence_leading =
  MUTATION == 'fejer_divergence' ? Rational(-2, 3) : Rational(2, 3)

tags = text.scan(/\\tag\{(F\.[^}]+)\}/).flatten
tags << 'F.1' if MUTATION == 'tag'
references = text.scan(/\(F\.([0-9]+[a-z]?)\)/).flatten.map do |value|
  "F.#{value}"
end
references << 'F.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\[' }
display_close = text.lines.count { |line| line.strip == '\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..23).map { |index| "F.#{index}" }

dependency_table_present = [
  'research/r075b_bulk_clock_outer_padding_gate.md',
  'research/r075e_horizontal_cross_mode_flux_reduction.md'
].all? do |path|
  text.lines.any? do |line|
    line.include?(path) && line.include?(FROZEN_SOURCES.fetch(path))
  end
end
dependency_table_present = false if MUTATION == 'dependency_table_missing'

required_tokens = [
  '\\ell=m-n',
  'i\\ell b g_{nm}',
  "+2f_n'\\overline{f_m}'",
  'n^2+m^2=(m-n)^2+2nm=\\ell^2+2nm',
  '\\mathcal T_\\xi =\\mathcal E_{\\rm off} -\\mathcal A_{\\rm off} +\\mathcal D_{\\rm off}',
  '\\mathcal E_{\\rm diag}+\\mathcal D_{\\rm diag} =\\mathcal A_{\\rm diag}',
  '\\langle h\\rangle:=\\frac1{2\\pi}',
  '0\\le X_N\\le1',
  '\\frac{2N^3+N}{3}',
  '\\frac{2N+N^{-1}}3\\longrightarrow\\infty',
  'not a counterexample to the R0.75E target',
  'None of these is proved here.',
  '\\mathbf{NOT\\ CLAY}'
]

audit_text = PRIMARY_AUDIT.read
boundary = {
  'positivityOnlyComparisonRuledOut' => true,
  'frozenCollarCounterexample' => MUTATION == 'counterexample_claim',
  'arbitraryRealE24Proved' => MUTATION == 'e24_closed',
  'completeClockProved' => MUTATION == 'full_clock',
  'clayClaim' => MUTATION == 'clay'
}

source_binding_ok = source_rows.values.all? { |pair| pair[0] == pair[1] }
fixture_binding_ok =
  fixture_hash == fixture_expected_hash &&
  expected_hash == expected_expected_hash &&
  fixtures.fetch('schema') ==
    'r075f-modal-phase-integration-identity-fixtures-v1' &&
  expected.fetch('schema') ==
    'r075f-modal-phase-integration-identity-expected-v1' &&
  fixtures.fetch('frozenSources') == FROZEN_SOURCES
fejer_exact_ok =
  fejer_rows.keys.sort == expected.fetch('fejer').keys.sort &&
  fejer_rows.all? do |key, row|
    expected_row = expected.fetch('fejer').fetch(key)
    row.fetch('differenceCounts') == expected_row.fetch('differenceCounts') &&
      row.fetch('fourthMoment') == expected_row.fetch('fourthMoment') &&
      row.fetch('xMean') == expected_row.fetch('xMean') &&
      row.fetch('aSquaredMean') == expected_row.fetch('aSquaredMean') &&
      row.fetch('localizedMean') == expected_row.fetch('localizedMean') &&
      row.fetch('odd') &&
      row.fetch('realSymmetric') &&
      row.fetch('weightBoundByTriangle')
  end
fejer_ratio_ok =
  expected.fetch('fejer').all? do |key, expected_row|
    fejer_rows.fetch(key).fetch('ratio') == expected_row.fetch('ratio')
  end && divergence_leading == Rational(2, 3)

checks = {
  'all five frozen source hashes' => source_binding_ok,
  'fixture and expected byte bindings' => fixture_binding_ok,
  'primary audit main binding and PASS/0 status' =>
    audit_text.include?(FROZEN_SOURCES.fetch(
      'research/r075f_modal_phase_integration_identity.md'
    )) &&
    audit_text.include?(
      'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.'
    ) &&
    audit_text.include?('Equation tags F.1--F.23 are unique and consecutive.'),
  'B/E table entries in main' => dependency_table_present,
  'two F.5 modal equations' =>
    complex_array(dtfn) == expected.dig('productCase', 'dtFN') &&
    complex_array(dtcfm) == expected.dig('productCase', 'dtConjugateFM'),
  'F.6 product derivative' =>
    complex_array(dtg) == expected.dig('productCase', 'dtG'),
  'F.7 vertical product rule' =>
    complex_array(gsecond) == expected.dig('productCase', 'gSecond'),
  'F.8 ell phase identity without division' =>
    product_observed == expected.fetch('productCase') &&
    phase_lhs == phase_rhs && no_division,
  'F.9--F.13 pi/2pi and nm normalization' =>
    normalization_observed == expected.fetch('normalization'),
  'F.14--F.15 endpoint and IBP signs' =>
    eta_initial == 0 && eta_terminal == 1 &&
    time_sign == -1 && vertical_sign == -1,
  'F.16--F.17 exact reconstruction' =>
    phase_observed == expected.fetch('phaseMomentCase') &&
    transport == reconstructed,
  'closed-solution direct F.5--F.18 integration' =>
    closed_observed == expected.fetch('closedSolutionNormalizedByKq') &&
    closed_time_direct == closed_time_by_parts &&
    closed_vertical_left == closed_vertical_right &&
    closed_phase_sum == closed_transport_direct &&
    closed_left == closed_right &&
    closed_f17_residual == [Rational(0), Rational(0)] &&
    closed_f18_left == closed_f18_right,
  'F.18 complete off-diagonal cancellation' =>
    cancellation_remainder == 0 && diagonal_direct,
  'F.19--F.22 explicit Fejer ordered counts' => fejer_exact_ok,
  'F.23 ratios N=3/5/7 and divergence' => fejer_ratio_ok,
  '23 tags, references, and displays' =>
    tags == expected_tags && tags.uniq.length == 23 &&
    (references - tags).empty? &&
    display_open == 23 && display_close == 23,
  'formula and status sentinels' =>
    required_tokens.all? do |token|
      flat_text.include?(token.gsub(/\s+/, ' '))
    end,
  'claim boundary' =>
    boundary.fetch('positivityOnlyComparisonRuledOut') &&
    !boundary.fetch('frozenCollarCounterexample') &&
    !boundary.fetch('arbitraryRealE24Proved') &&
    !boundary.fetch('completeClockProved') &&
    !boundary.fetch('clayClaim'),
  'Python schema, verdict, and exact rows' =>
    python_payload.fetch('schema') == SCHEMA &&
    python_payload.fetch('verdict') == 'PASS' &&
    python_payload.fetch('exactProductCase') == expected.fetch('productCase') &&
    python_payload.fetch('exactPhaseFormsOverPi') ==
      expected.fetch('phaseMomentCase') &&
    python_payload.fetch('closedSolutionNormalizedByKq') ==
      expected.fetch('closedSolutionNormalizedByKq') &&
    python_payload.fetch('fejerRows').all? do |key, row|
      expected.fetch('fejer').fetch(key).fetch('ratio') == row.fetch('ratio')
    end,
  'UTF-8 and control safety' =>
    scan_text.valid_encoding? &&
    !scan_text.each_codepoint.any? do |code|
      code < 32 && ![9, 10].include?(code)
    end
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed = checks.reject { |_name, passed| passed }.keys
REPORT.write(
  "# R0.75F independent finite audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}\n" \
  "- Fixture SHA-256: #{fixture_hash}\n" \
  "- Expected SHA-256: #{expected_hash}\n" \
  "- Failed checks: #{failed.empty? ? 'none' : failed.join('; ')}\n\n" \
  "Ruby independently evaluates the two modal equations with exact Complex " \
  "Rational arithmetic, then checks the product rule and F.8. A genuine " \
  "two-mode solution is integrated in Q[p], p=pi^-2: transport is obtained " \
  "directly from i*ell*b*g, both integration-by-parts identities agree, and " \
  "F.12, F.17, and F.18 have exactly zero residual.\n\n" \
  "For N=3,5,7, nested ordered-pair loops give fourth moments 19, 85, 231 " \
  "and ratios 19/9, 17/5, 33/7. The finite family rules out only a " \
  "positivity-only uniform diagonal comparison; it is not a frozen-collar " \
  "counterexample. E.24 and all larger claims remain OPEN. **NOT CLAY.**\n"
)

puts JSON.generate(
  suite: 'r075f-modal-phase-integration-identity-independent',
  verdict: verdict,
  assertions: checks.length
)
exit(verdict == 'PASS' ? 0 : 1)
