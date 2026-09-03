#!/usr/bin/env ruby
# Independent exact verifier for frozen R0.75J.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075j_mean_zero_adjoint_flux_obstruction.md'
PRIMARY_AUDIT = ROOT + 'research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md'
REPORT_SOURCE = ROOT + 'research/r075j_report-source.md'
FIXTURES = ROOT + 'scripts/r075j_mean_zero_adjoint_flux_obstruction_fixtures.json'
EXPECTED = ROOT + 'scripts/r075j_mean_zero_adjoint_flux_obstruction_expected.json'
JSON_PATH = Pathname.new(
  ENV.fetch(
    'R075J_JSON',
    (ROOT + 'research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json').to_s
  )
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075J_RUBY_REPORT',
    (ROOT + 'research/r075j_mean_zero_adjoint_flux_obstruction_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075J_RUBY_MUTATION', '')
SCHEMA = 'r075j-mean-zero-adjoint-flux-obstruction-certificate-v1'

FROZEN_SOURCES = {
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075f_modal_phase_integration_identity.md' =>
    'f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440',
  'research/r075h_single_pass_transport_flux_closure.md' =>
    '849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9',
  'research/r075i_diffusion_safe_block_participation.md' =>
    'c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7',
  'research/r075j_mean_zero_adjoint_flux_obstruction.md' =>
    '960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d',
  'research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md' =>
    'f2de2d439d428ccd2885f7d3fc333496cb9753896c772a54df04622e4c52c76e',
  'research/r075j_report-source.md' =>
    '1d195b0bc6760a4458fd3b4f7d11c5c892ca259c88aa5de3b014b4986ad166ca'
}.freeze
FIXTURES_SHA256 = '754d585bab0b194adaa3f945dc8b14950e3c078564f38dc63919cf733fcfea2c'
EXPECTED_SHA256 = '6c32cd1ff38895c5e3b0a580ad9a5e789fc3d9d8e672ba6644dceeb29befe5b8'

NEGATIVE_MUTATIONS = %w[
  source_drift audit_drift report_source_drift dependency_drift
  dependency_table_missing fixture_drift expected_drift tag reference display
  control forward_time_sign forward_drift_sign forward_diffusion_sign
  adjoint_time_sign adjoint_drift_sign adjoint_diffusion_sign drift_divergence
  square_diss_sign square_diss_factor derivative_source_abs
  derivative_source_positive source_b_x2 source_mean_quantifier
  positive_source_equal tau_direction A_sign B_sign b_sign terminal_nonzero
  adjoint_source_cos adjoint_source_sin eta_denominator eta_positive slice_sign
  sign_change_false j12_initial_sign j12_terminal_sign j12_bulk_sign
  j12_endpoint_swap j12_source_pairing j5_half j5_diss_sign j13_initial_sign
  j13_diss_sign j13_drop_negative_initial signed_decomposition
  energy_endpoint_sign energy_factor shift_initial_sign shift_terminal_sign
  shift_diss_sign constant_homogeneous exact_shift_nonzero surcharge_half
  surcharge_not_cd majorant_direction phi_nonnegative terminal_nonnegative
  majorant_half majorant_terminal_sign majorant_diss_sign
  majorant_source_direction favorable_terminal favorable_dissipation
  pde_backward exact_adjoint_nonnegative aplus_signed majorant_paid
  uncontrolled_dissipation_paid free_shift blanket_no_go feynman_kac_closed
  transition_closed periodic_closed e24_closed complete_clock fixed_deletion
  suitable_weak regularity singularity simulation_used novelty clay
].freeze

abort("unknown R075J_RUBY_MUTATION: #{MUTATION}") unless
  MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)

def rat(value)
  Rational(value.to_s)
end

def rtext(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

def poly_trim(poly)
  result = poly.dup
  result.pop while result.length > 1 && result[-1].zero?
  result
end

def poly_add(*polys)
  size = polys.map(&:length).max
  poly_trim((0...size).map do |index|
    polys.sum { |poly| index < poly.length ? poly[index] : Rational(0) }
  end)
end

def poly_scale(poly, scalar)
  poly_trim(poly.map { |coefficient| scalar * coefficient })
end

def poly_multiply(left, right)
  result = Array.new(left.length + right.length - 1, Rational(0))
  left.each_with_index do |left_value, left_index|
    right.each_with_index do |right_value, right_index|
      result[left_index + right_index] += left_value * right_value
    end
  end
  poly_trim(result)
end

def poly_derivative(poly)
  return [Rational(0)] if poly.length == 1

  poly_trim(poly.each_with_index.drop(1).map { |coefficient, index| coefficient * index })
end

def poly_evaluate(poly, value)
  poly.reverse.reduce(Rational(0)) { |accumulator, coefficient| accumulator * value + coefficient }
end

def poly_text(poly, degree)
  (0..degree).map { |index| rtext(index < poly.length ? poly[index] : Rational(0)) }
end

text = MAIN.read
audit_text = PRIMARY_AUDIT.read
source_text = REPORT_SOURCE.read
flat_text = text.gsub(/\s+/, ' ')
scan_text = text + audit_text + source_text + (MUTATION == 'control' ? "\u0001" : '')
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_payload = JSON.parse(JSON_PATH.read)

source_expectations = FROZEN_SOURCES.dup
source_expectations['research/r075j_mean_zero_adjoint_flux_obstruction.md'] =
  '0' * 64 if MUTATION == 'source_drift'
source_expectations[
  'research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md'
] = '0' * 64 if MUTATION == 'audit_drift'
source_expectations['research/r075j_report-source.md'] =
  '0' * 64 if MUTATION == 'report_source_drift'
source_expectations['research/r075f_modal_phase_integration_identity.md'] =
  '0' * 64 if MUTATION == 'dependency_drift'
source_rows = source_expectations.keys.sort.to_h do |path|
  [path, [source_expectations.fetch(path), Digest::SHA256.file(ROOT + path).hexdigest]]
end
fixture_expected_hash = MUTATION == 'fixture_drift' ? '0' * 64 : FIXTURES_SHA256
expected_expected_hash = MUTATION == 'expected_drift' ? '0' * 64 : EXPECTED_SHA256
fixture_hash = Digest::SHA256.file(FIXTURES).hexdigest
expected_hash = Digest::SHA256.file(EXPECTED).hexdigest

# Operator coefficients and the passive-square row.
operator = fixtures.fetch('operatorCase')
forward = operator.fetch('forward').to_h { |key, value| [key, rat(value)] }
adjoint = operator.fetch('adjoint').to_h { |key, value| [key, rat(value)] }
forward['time'] *= -1 if MUTATION == 'forward_time_sign'
forward['drift'] *= -1 if MUTATION == 'forward_drift_sign'
forward['laplacian'] *= -1 if MUTATION == 'forward_diffusion_sign'
adjoint['time'] *= -1 if MUTATION == 'adjoint_time_sign'
adjoint['drift'] *= -1 if MUTATION == 'adjoint_drift_sign'
adjoint['laplacian'] *= -1 if MUTATION == 'adjoint_diffusion_sign'
divergence_term = MUTATION == 'drift_divergence' ? Rational(1) : Rational(0)
square_dissipation = rat(operator.fetch('squareDissipationCoefficient'))
square_dissipation *= -1 if MUTATION == 'square_diss_sign'
square_dissipation /= 2 if MUTATION == 'square_diss_factor'
operator_observed = {
  'forward' => forward.to_h { |key, value| [key, rtext(value)] },
  'adjoint' => adjoint.to_h { |key, value| [key, rtext(value)] },
  'driftDivergenceTerm' => rtext(divergence_term),
  'squareDissipationCoefficient' => rtext(square_dissipation)
}

# Product quadrature for the physical derivative source.
physical = fixtures.fetch('physicalDerivativeSourceCase')
eta = rat(physical.fetch('eta'))
x2_measures = physical.fetch('x2CellMeasures').map { |value| rat(value) }
derivatives = physical.fetch('cutoffDerivativeValues').map { |value| rat(value) }
derivatives.map!(&:abs) if MUTATION == 'derivative_source_abs'
derivatives.map! { |value| [value, Rational(0)].max } if MUTATION == 'derivative_source_positive'
x3_measures = physical.fetch('x3CellMeasures').map { |value| rat(value) }
drifts = physical.fetch('driftValues').map { |value| rat(value) }
derivative_means = []
source_means = []
drifts.each do |drift|
  derivative_mean = x2_measures.zip(derivatives).sum { |measure, value| measure * value }
  derivative_means << derivative_mean
  source_mean = if MUTATION == 'source_b_x2'
                  local_drifts = [drift, drift + 1]
                  eta * x2_measures.zip(local_drifts, derivatives).sum do |measure, local_drift, derivative|
                    measure * local_drift * derivative
                  end
                else
                  eta * drift * derivative_mean
                end
  source_means << source_mean
end
total_signed_mean = x3_measures.zip(source_means).sum { |measure, value| measure * value }
drift_average = x3_measures.zip(drifts).sum { |measure, value| measure * value }
original_derivatives = physical.fetch('cutoffDerivativeValues').map { |value| rat(value) }
positive_derivative_mean = x2_measures.zip(original_derivatives).sum do |measure, value|
  measure * [value, Rational(0)].max
end
absolute_derivative_mean = x2_measures.zip(original_derivatives).sum do |measure, value|
  measure * value.abs
end
physical_observed = {
  'derivativeMeanByX3Cell' => derivative_means.map { |value| rtext(value) },
  'sourceMeanByX3Cell' => source_means.map { |value| rtext(value) },
  'totalSignedMean' => rtext(total_signed_mean),
  'positivePartMean' => rtext(eta * drift_average * positive_derivative_mean),
  'absoluteMean' => rtext(eta * drift_average * absolute_derivative_mean),
  'positivePartEqualsSignedSource' => MUTATION == 'positive_source_equal',
  'quantifier' => MUTATION == 'source_mean_quantifier' ? 'integrated-only' : 'every-(t,x1)'
}

# Requested rational tau-polynomial Fourier fixture.
explicit = fixtures.fetch('explicitAdjointCase')
a_poly = explicit.fetch('AInTau').map { |value| rat(value) }
b_field_poly = explicit.fetch('BInTau').map { |value| rat(value) }
drift_poly = explicit.fetch('bInTau').map { |value| rat(value) }
a_poly = poly_scale(a_poly, -1) if MUTATION == 'A_sign'
b_field_poly = poly_scale(b_field_poly, -1) if MUTATION == 'B_sign'
drift_poly[1] *= -1 if MUTATION == 'b_sign'
a_poly[0] += 1 if MUTATION == 'terminal_nonzero'
tau_time_factor = MUTATION == 'tau_direction' ? Rational(-1) : Rational(1)
cos_poly = poly_add(
  poly_scale(poly_derivative(a_poly), -adjoint.fetch('time') * tau_time_factor),
  poly_scale(poly_multiply(drift_poly, b_field_poly), adjoint.fetch('drift')),
  poly_scale(a_poly, -adjoint.fetch('laplacian'))
)
sin_poly = poly_add(
  poly_scale(poly_derivative(b_field_poly), -adjoint.fetch('time') * tau_time_factor),
  poly_scale(poly_multiply(drift_poly, a_poly), -adjoint.fetch('drift')),
  poly_scale(b_field_poly, -adjoint.fetch('laplacian'))
)
source_cos = [Rational(1), Rational(1), Rational(2), Rational(1)]
source_sin = [Rational(0)]
source_cos[2] += 1 if MUTATION == 'adjoint_source_cos'
source_sin[0] = 1 if MUTATION == 'adjoint_source_sin'
sample_taus = explicit.fetch('sampleTau').map { |value| rat(value) }
eta_denominator = MUTATION == 'eta_denominator' ?
  [Rational(2), Rational(-1)] : drift_poly
eta_samples = sample_taus.map do |tau|
  poly_evaluate(source_cos, tau) / poly_evaluate(eta_denominator, tau)
end
eta_numerator_minimum = [poly_evaluate(source_cos, 0), poly_evaluate(source_cos, 1)].min
eta_denominator_minimum = [
  poly_evaluate(eta_denominator, 0), poly_evaluate(eta_denominator, 1)
].min
eta_positive_on_interval = eta_numerator_minimum.positive? &&
  eta_denominator_minimum.positive? && source_cos.all? { |coefficient| coefficient >= 0 } &&
  eta_denominator.length <= 2
eta_positive_on_interval = false if MUTATION == 'eta_positive'
slice_samples = sample_taus.drop(1).map do |tau|
  at_zero = poly_evaluate(a_poly, tau)
  at_pi = -at_zero
  at_pi *= -1 if MUTATION == 'slice_sign'
  {'tau' => rtext(tau), 'atX0' => rtext(at_zero), 'atXPi' => rtext(at_pi)}
end
explicit_observed = {
  'cosineCoefficientsInTau' => poly_text(cos_poly, 3),
  'sineCoefficientsInTau' => poly_text(sin_poly, 3),
  'sourceCosineCoefficientsInTau' => poly_text(source_cos, 3),
  'terminalA' => rtext(poly_evaluate(a_poly, Rational(0))),
  'terminalB' => rtext(poly_evaluate(b_field_poly, Rational(0))),
  'etaSamples' => eta_samples.map { |value| rtext(value) },
  'etaNumeratorMinimumOnUnitInterval' => rtext(eta_numerator_minimum),
  'etaDenominatorMinimumOnUnitInterval' => rtext(eta_denominator_minimum),
  'etaPositiveOnUnitInterval' => eta_positive_on_interval,
  'sliceSamples' => slice_samples,
  'nonzeroSlicesChangeSign' => MUTATION != 'sign_change_false'
}
eta_positive = eta_positive_on_interval && eta_samples.all?(&:positive?)

# J.12 signs.
duality = fixtures.fetch('dualityCase')
initial = rat(duality.fetch('initialBoundary'))
terminal = rat(duality.fetch('terminalBoundary'))
bulk = rat(duality.fetch('bulkLg'))
initial_coefficient = MUTATION == 'j12_initial_sign' ? Rational(-1) : Rational(1)
terminal_coefficient = MUTATION == 'j12_terminal_sign' ? Rational(1) : Rational(-1)
bulk_coefficient = MUTATION == 'j12_bulk_sign' ? Rational(-1) : Rational(1)
initial, terminal = terminal, initial if MUTATION == 'j12_endpoint_swap'
duality_rhs = initial_coefficient * initial + terminal_coefficient * terminal + bulk_coefficient * bulk
source_pairing = rat(duality.fetch('sourcePairing'))
source_pairing += 1 if MUTATION == 'j12_source_pairing'
duality_observed = {
  'initialCoefficient' => rtext(initial_coefficient),
  'terminalCoefficient' => rtext(terminal_coefficient),
  'bulkCoefficient' => rtext(bulk_coefficient),
  'rhs' => rtext(duality_rhs),
  'sourcePairing' => rtext(source_pairing),
  'residual' => rtext(duality_rhs - source_pairing)
}

# J.5/J.13 signs and finite inequality.
signed = fixtures.fetch('signedDissipationCase')
initial_plus = rat(signed.fetch('initialPsiPlus'))
initial_minus = rat(signed.fetch('initialPsiMinus'))
diss_plus = rat(signed.fetch('dissipationPsiPlus'))
diss_minus = rat(signed.fetch('dissipationPsiMinus'))
initial_minus *= -1 if MUTATION == 'signed_decomposition'
j5_initial_coefficient = MUTATION == 'j5_half' ? Rational(1) : Rational(1, 2)
j5_diss_coefficient = MUTATION == 'j5_diss_sign' ? Rational(1) : Rational(-1)
exact_flux = j5_initial_coefficient * (initial_plus - initial_minus) +
  j5_diss_coefficient * (diss_plus - diss_minus)
j13_initial_coefficient = MUTATION == 'j13_initial_sign' ? Rational(-1, 2) : Rational(1, 2)
j13_diss_coefficient = MUTATION == 'j13_diss_sign' ? Rational(-1) : Rational(1)
upper_bound = j13_initial_coefficient * initial_plus + j13_diss_coefficient * diss_minus
upper_bound += Rational(1, 2) * initial_minus if MUTATION == 'j13_drop_negative_initial'
signed_observed = {
  'squareDissipationCoefficient' => rtext(square_dissipation),
  'J5InitialCoefficient' => rtext(j5_initial_coefficient),
  'J5DissipationCoefficient' => rtext(j5_diss_coefficient),
  'exactFlux' => rtext(exact_flux),
  'J13InitialPositiveCoefficient' => rtext(j13_initial_coefficient),
  'J13NegativeDissipationCoefficient' => rtext(j13_diss_coefficient),
  'upperBound' => rtext(upper_bound),
  'upperSlack' => rtext(upper_bound - exact_flux)
}

# Constant shift and energy identity.
shift = fixtures.fetch('constantShiftCase')
constant = rat(shift.fetch('C'))
energy_initial = rat(shift.fetch('energyInitial'))
energy_terminal = rat(shift.fetch('energyTerminal'))
dissipation = rat(shift.fetch('dissipation'))
endpoint_sign = MUTATION == 'energy_endpoint_sign' ? Rational(1) : Rational(-1)
dissipation_factor = MUTATION == 'energy_factor' ? Rational(1) : Rational(2)
energy_residual = energy_initial + endpoint_sign * energy_terminal - dissipation_factor * dissipation
homogeneous_source = MUTATION == 'constant_homogeneous' ? Rational(1) : Rational(0)
initial_constant = (MUTATION == 'shift_initial_sign' ? Rational(-1, 2) : Rational(1, 2)) *
  constant * energy_initial
terminal_constant = (MUTATION == 'shift_terminal_sign' ? Rational(1, 2) : Rational(-1, 2)) *
  constant * energy_terminal
dissipation_constant = (MUTATION == 'shift_diss_sign' ? Rational(1) : Rational(-1)) *
  constant * dissipation
exact_constant_sum = initial_constant + terminal_constant + dissipation_constant
exact_constant_sum += 1 if MUTATION == 'exact_shift_nonzero'
surcharge = (MUTATION == 'surcharge_half' ? Rational(1, 4) : Rational(1, 2)) *
  constant * (energy_initial - energy_terminal)
c_times_d = constant * dissipation
c_times_d += 1 if MUTATION == 'surcharge_not_cd'
shift_observed = {
  'energyIdentityResidual' => rtext(energy_residual),
  'homogeneousAdjointSource' => rtext(homogeneous_source),
  'initialConstantContribution' => rtext(initial_constant),
  'terminalConstantContribution' => rtext(terminal_constant),
  'dissipationConstantContribution' => rtext(dissipation_constant),
  'exactConstantSum' => rtext(exact_constant_sum),
  'droppedDissipationSurcharge' => rtext(surcharge),
  'CtimesD' => rtext(c_times_d)
}

# Positive majorant ledger.
majorant = fixtures.fetch('majorantCase')
half_source = rat(majorant.fetch('halfSourcePairing'))
half_source += 1 if MUTATION == 'majorant_source_direction'
majorant_half = MUTATION == 'majorant_half' ? Rational(1) : Rational(1, 2)
half_initial = majorant_half * rat(majorant.fetch('initialPairing'))
terminal_row = (MUTATION == 'majorant_terminal_sign' ? majorant_half : -majorant_half) *
  rat(majorant.fetch('terminalPairing'))
dissipation_row = (MUTATION == 'majorant_diss_sign' ? Rational(1) : Rational(-1)) *
  rat(majorant.fetch('weightedDissipation'))
exact_majorant_rhs = half_initial + terminal_row + dissipation_row
majorant_observed = {
  'direction' => MUTATION == 'majorant_direction' ? 'a>=LstarPhi' : 'a<=LstarPhi',
  'PhiNonnegative' => MUTATION == 'phi_nonnegative' ? false : majorant.fetch('PhiNonnegative'),
  'terminalNonnegative' => MUTATION == 'terminal_nonnegative' ? false : majorant.fetch('terminalNonnegative'),
  'halfSourcePairing' => rtext(half_source),
  'halfInitialRow' => rtext(half_initial),
  'negativeHalfTerminalRow' => rtext(terminal_row),
  'negativeDissipationRow' => rtext(dissipation_row),
  'exactMajorantRhs' => rtext(exact_majorant_rhs),
  'boundaryOnlyUpper' => rtext(half_initial),
  'terminalTermFavorable' => MUTATION != 'favorable_terminal',
  'dissipationTermFavorable' => MUTATION != 'favorable_dissipation'
}

tags = text.scan(/\\tag\{(J\.[^}]+)\}/).flatten
tags << 'J.1' if MUTATION == 'tag'
references = text.scan(/\(J\.([0-9]+[a-z]?)\)/).flatten.map { |value| "J.#{value}" }
references << 'J.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\[' }
display_close = text.lines.count { |line| line.strip == '\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..20).map { |index| "J.#{index}" }

dependency_paths = %w[
  research/r075e_horizontal_cross_mode_flux_reduction.md
  research/r075f_modal_phase_integration_identity.md
  research/r075h_single_pass_transport_flux_closure.md
  research/r075i_diffusion_safe_block_participation.md
]
dependency_table_present = dependency_paths.all? do |path|
  text.lines.any? { |line| line.include?(path) && line.include?(FROZEN_SOURCES.fetch(path)) }
end
dependency_table_present = false if MUTATION == 'dependency_table_missing'

required_tokens = [
  '\\mathcal L:=\\partial_t+b(t,x_3)\\partial_2-\\Delta_{23}',
  '\\mathcal L^*:=-\\partial_t-b(t,x_3)\\partial_2-\\Delta_{23}',
  '\\int_{\\mathbb T^2_{23}}a(t,x_1,x_2,x_3)\\,dx_2dx_3',
  '-\\frac d{dt}\\int_{\\mathbb T^2_{23}}\\psi',
  '\\mathcal Lg=-2|\\nabla_{23}F|^2',
  '\\int_{\\mathbb T^3}\\phi(s)g(s)',
  '-\\int_{\\mathbb T^3}\\phi(t_2)g(t_2)',
  '+\\int_s^{t_2}\\!\\int\\phi\\,\\mathcal Lg',
  'E(s)-E(t_2)=2D',
  '\\frac C2\\bigl(E(s)-E(t_2)\\bigr)-CD=0',
  'a\\le\\mathcal L^*\\Phi',
  'Replacing `a` by `|a|` or `a_+` changes the equation',
  'does not construct the paid majorant or close E.24',
  'It is not a no-go theorem for all resolvent or Feynman--Kac methods',
  '\\mathbf{NOT\\ CLAY}'
]

boundary = {
  'backwardProblemIsAdjointNotPassiveIllPosedness' => MUTATION != 'pde_backward',
  'exactAdjointForcedSignChanging' => MUTATION != 'exact_adjoint_nonnegative',
  'positivePartIsNotPhysicalSignedSource' =>
    !%w[aplus_signed positive_source_equal].include?(MUTATION),
  'majorantInitialRowUnpaid' => MUTATION != 'majorant_paid',
  'negativeAdjointDissipationUnpaid' => MUTATION != 'uncontrolled_dissipation_paid',
  'constantShiftNotFree' => MUTATION != 'free_shift',
  'notBlanketNoGoForAdjointMethods' => MUTATION != 'blanket_no_go',
  'FeynmanKacMajorantPaymentOpen' => MUTATION != 'feynman_kac_closed',
  'transitionGeometryOpen' => MUTATION != 'transition_closed',
  'periodicRecrossingOpen' => MUTATION != 'periodic_closed',
  'E24Open' => MUTATION != 'e24_closed',
  'completeClockOpen' => MUTATION != 'complete_clock',
  'fixedDeletionOpen' => MUTATION != 'fixed_deletion',
  'suitableWeakTransferOpen' => MUTATION != 'suitable_weak',
  'regularityOpen' => MUTATION != 'regularity',
  'singularityOpen' => MUTATION != 'singularity',
  'noSimulationUsed' => MUTATION != 'simulation_used',
  'noNoveltyOrPriorityClaim' => MUTATION != 'novelty',
  'notClay' => MUTATION != 'clay'
}

flat_audit = audit_text.gsub(/\s+/, ' ')
checks = {
  'all seven frozen hashes' => source_rows.values.all? { |pair| pair[0] == pair[1] },
  'fixture and expected byte bindings' =>
    fixture_hash == fixture_expected_hash && expected_hash == expected_expected_hash &&
    fixtures.fetch('schema') == 'r075j-mean-zero-adjoint-flux-obstruction-fixtures-v1' &&
    expected.fetch('schema') == 'r075j-mean-zero-adjoint-flux-obstruction-expected-v1' &&
    fixtures.fetch('frozenSources') == FROZEN_SOURCES,
  'primary audit frozen PASS and 20 displays' =>
    audit_text.include?(FROZEN_SOURCES.fetch('research/r075j_mean_zero_adjoint_flux_obstruction.md')) &&
    audit_text.include?('Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.') &&
    audit_text.include?('Equation tags J.1--J.20 are unique and consecutive.') &&
    audit_text.include?('All 20 display-math environments are paired.'),
  'four dependency rows in main' => dependency_table_present,
  'forward and adjoint drift-diffusion signs' =>
    operator_observed.fetch('forward') == expected.dig('operators', 'forward') &&
    operator_observed.fetch('adjoint') == expected.dig('operators', 'adjoint') &&
    divergence_term.zero?,
  'passive-square dissipation coefficient' =>
    operator_observed == expected.fetch('operators') && square_dissipation == -2,
  'physical derivative source zero for each fixed slice' =>
    physical_observed == expected.fetch('physicalSource') &&
    derivative_means.all?(&:zero?) && source_means.all?(&:zero?) && total_signed_mean.zero?,
  'positive part and absolute source differ from signed source' =>
    physical_observed.fetch('positivePartMean') == '6' &&
    physical_observed.fetch('absoluteMean') == '12' &&
    !physical_observed.fetch('positivePartEqualsSignedSource'),
  'explicit adjoint cosine and zero sine identity' =>
    explicit_observed == expected.fetch('explicitAdjoint') &&
    cos_poly == source_cos && sin_poly == source_sin,
  'explicit terminal zero and eta positivity' =>
    poly_evaluate(a_poly, 0).zero? && poly_evaluate(b_field_poly, 0).zero? && eta_positive,
  'nonzero slice has both signs' =>
    slice_samples.all? { |row| rat(row.fetch('atX0')) > 0 && rat(row.fetch('atXPi')) < 0 } &&
    explicit_observed.fetch('nonzeroSlicesChangeSign'),
  'J.12 two endpoint and bulk signs' =>
    duality_observed == expected.fetch('duality') && duality_rhs == source_pairing,
  'J.5 negative dissipation sign' =>
    signed_observed.fetch('J5InitialCoefficient') == '1/2' &&
    signed_observed.fetch('J5DissipationCoefficient') == '-1' &&
    signed_observed.fetch('exactFlux') == '2',
  'J.13 positive negative-part dissipation upper row' =>
    signed_observed == expected.fetch('signedDissipation') && exact_flux <= upper_bound,
  'global energy identity and homogeneous constant' =>
    energy_residual.zero? && homogeneous_source.zero?,
  'constant shift cancels exactly' =>
    shift_observed == expected.fetch('constantShift') && exact_constant_sum.zero?,
  'dropped row costs exact CD surcharge' => surcharge == c_times_d && surcharge.positive?,
  'majorant direction and nonnegativity' =>
    majorant_observed.fetch('direction') == 'a<=LstarPhi' &&
    majorant_observed.fetch('PhiNonnegative') && majorant_observed.fetch('terminalNonnegative'),
  'majorant terminal and dissipation terms favorable' =>
    majorant_observed == expected.fetch('majorant') &&
    half_source <= exact_majorant_rhs && exact_majorant_rhs <= half_initial &&
    terminal_row <= 0 && dissipation_row <= 0,
  '20 tags references and displays' =>
    tags == expected_tags && tags.uniq.length == 20 && (references - tags).empty? &&
    display_open == 20 && display_close == 20,
  'formula and source status sentinels' =>
    required_tokens.all? { |token| flat_text.include?(token.gsub(/\s+/, ' ')) } &&
    source_text.include?('does not establish novelty') &&
    source_text.include?('Viable but open'),
  'claim boundary' => boundary.values.all?,
  'Python schema and all exact ledgers agree' =>
    python_payload.fetch('schema') == SCHEMA && python_payload.fetch('verdict') == 'PASS' &&
    python_payload.fetch('operators') == operator_observed &&
    python_payload.fetch('physicalSource') == physical_observed &&
    python_payload.fetch('explicitAdjoint') == explicit_observed &&
    python_payload.fetch('duality') == duality_observed &&
    python_payload.fetch('signedDissipation') == signed_observed &&
    python_payload.fetch('constantShift') == shift_observed &&
    python_payload.fetch('majorant') == majorant_observed &&
    python_payload.fetch('claimBoundary') == boundary,
  'UTF-8 and control safety' =>
    scan_text.valid_encoding? &&
    !scan_text.each_codepoint.any? { |code| code < 32 && ![9, 10].include?(code) }
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed = checks.reject { |_name, passed| passed }.keys
REPORT.write(
  "# R0.75J independent finite audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}\n" \
  "- Fixture SHA-256: #{fixture_hash}\n" \
  "- Expected SHA-256: #{expected_hash}\n" \
  "- Failed checks: #{failed.empty? ? 'none' : failed.join('; ')}\n\n" \
  "Ruby independently computes the Fourier action of L* on the rational " \
  "tau-polynomial fixture. It obtains (1+tau+2tau^2+tau^3) cos(x), zero " \
  "sine mode, terminal zero, positive eta samples, and opposite slice signs. " \
  "Finite product quadrature verifies physical-source mean zero for each " \
  "parameter slice and separates the signed source from a_+ and |a|.\n\n" \
  "The endpoint, passive-square, dissipation, shift-cancellation, CD-surcharge, " \
  "and positive-majorant ledgers agree exactly with the independent Python " \
  "producer. The majorant initial row remains unpaid, and this obstruction is " \
  "not a blanket no-go for adjoint or Feynman--Kac methods. E.24 and all " \
  "larger claims remain OPEN. **NOT CLAY.**\n"
)

puts JSON.generate(
  suite: 'r075j-mean-zero-adjoint-flux-obstruction-independent',
  verdict: verdict,
  assertions: checks.length
)
exit(verdict == 'PASS' ? 0 : 1)
