#!/usr/bin/env ruby
# Independent exact verifier for frozen R0.75K.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075k_positive_majorant_high_frequency_trace_loss.md'
PRIMARY_AUDIT = ROOT + 'research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md'
REPORT_SOURCE = ROOT + 'research/r075k_report-source.md'
FIXTURES = ROOT + 'scripts/r075k_positive_majorant_high_frequency_trace_loss_fixtures.json'
EXPECTED = ROOT + 'scripts/r075k_positive_majorant_high_frequency_trace_loss_expected.json'
JSON_PATH = Pathname.new(
  ENV.fetch(
    'R075K_JSON',
    (ROOT + 'research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json').to_s
  )
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075K_RUBY_REPORT',
    (ROOT + 'research/r075k_positive_majorant_high_frequency_trace_loss_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075K_RUBY_MUTATION', '')
SCHEMA = 'r075k-positive-majorant-high-frequency-trace-loss-certificate-v1'

FROZEN_SOURCES = {
  'research/r075e_horizontal_cross_mode_flux_reduction.md' =>
    '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049',
  'research/r075i_diffusion_safe_block_participation.md' =>
    'c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7',
  'research/r075j_mean_zero_adjoint_flux_obstruction.md' =>
    '960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d',
  'research/r075k_positive_majorant_high_frequency_trace_loss.md' =>
    '9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf',
  'research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md' =>
    '401f12d9a5f35646638ae08446a1177a0b0485b9bbb54206702dee9fc7e7a4a2',
  'research/r075k_report-source.md' =>
    '5a45521ecb5e85b69b077af9d4db3cbb1c52dc1b61cccf8fb3bbb9daabac7001'
}.freeze
FIXTURES_SHA256 = 'f15df9bf59d6a96151f84ae2fa11a12b3965820450fbad526d4f71f11a6f7328'
EXPECTED_SHA256 = '5ad1107080ccf033e842521e8f985196357d6cb858f945b007a5df50c2a12d77'

NEGATIVE_MUTATIONS = %w[
  source_drift audit_drift report_source_drift dependency_drift
  dependency_table_missing fixture_drift expected_drift tag reference display
  control forward_time_sign forward_drift_sign forward_diffusion_sign
  adjoint_time_sign adjoint_drift_sign adjoint_diffusion_sign constant_shear
  q_constant q_cosine a_cosine q_majorant_direction q_nonnegative q_modes
  a_modes time_reversal semigroup_drift_sign semigroup_diffusion_sign
  semigroup_source_sign phi_terminal phi_nonnegative phi_modes phi_mass_sign
  phi_mass_factor phi_mass_endpoint decay_sign phase_direction time_decay
  time_phase drift_phase laplacian_sign passive_residual k_integer k_lower
  square_frequency square_zero_coefficient square_side_coefficient
  entrance_half orthogonality boundary_k_dependence cos_quarter cos_symmetry
  cos_integral mass_decay_three mass_k_square mass_amplitude
  mass_upper_direction exponential_range mass_exact_factor boundary_A mass_A
  mass_k two_thirds ratio_A ratio_k amplitude_cancel ratio_growth
  ratio_constant signed_source_frequency signed_field_frequency
  signed_mode_match signed_flux_nonzero signed_integer_quantifier
  physical_flux_absolute W_limit_order W_continuous W_nonnegative W_integral
  W_depends_k W_frequency riemann_lebesgue W_boundary_limit
  local_atom_not_alone e24_counterexample all_majorants_ruled
  fdependent_ruled signed_kernel_ruled full_versionm_ruled trace_atom_ruled
  nse_solution transition_closed periodic_closed complete_clock fixed_deletion
  suitable_weak regularity singularity novelty simulation_used clay
].freeze

abort("unknown R075K_RUBY_MUTATION: #{MUTATION}") unless
  MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)

def rat(value)
  Rational(value.to_s)
end

def rtext(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

def exponent_text(row)
  row.to_h { |key, value| [key, rtext(value)] }
end

text = MAIN.read
audit_text = PRIMARY_AUDIT.read
source_text = REPORT_SOURCE.read
flat_text = text.gsub(/\s+/, ' ')
flat_source_text = source_text.gsub(/\s+/, ' ')
scan_text = text + audit_text + source_text + (MUTATION == 'control' ? "\u0001" : '')
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_payload = JSON.parse(JSON_PATH.read)

# Frozen byte bindings are recomputed locally.
source_expectations = FROZEN_SOURCES.dup
source_expectations['research/r075k_positive_majorant_high_frequency_trace_loss.md'] =
  '0' * 64 if MUTATION == 'source_drift'
source_expectations[
  'research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md'
] = '0' * 64 if MUTATION == 'audit_drift'
source_expectations['research/r075k_report-source.md'] =
  '0' * 64 if MUTATION == 'report_source_drift'
source_expectations['research/r075j_mean_zero_adjoint_flux_obstruction.md'] =
  '0' * 64 if MUTATION == 'dependency_drift'
source_rows = source_expectations.keys.sort.to_h do |path|
  [path, [source_expectations.fetch(path), Digest::SHA256.file(ROOT + path).hexdigest]]
end
fixture_expected_hash = MUTATION == 'fixture_drift' ? '0' * 64 : FIXTURES_SHA256
expected_expected_hash = MUTATION == 'expected_drift' ? '0' * 64 : EXPECTED_SHA256
fixture_hash = Digest::SHA256.file(FIXTURES).hexdigest
expected_hash = Digest::SHA256.file(EXPECTED).hexdigest

# Independent L/L* coefficient ledger.
operator_fixture = fixtures.fetch('operatorCase')
forward = operator_fixture.fetch('forward').to_h { |key, value| [key, rat(value)] }
adjoint = operator_fixture.fetch('adjoint').to_h { |key, value| [key, rat(value)] }
forward['time'] *= -1 if MUTATION == 'forward_time_sign'
forward['drift'] *= -1 if MUTATION == 'forward_drift_sign'
forward['secondDerivative'] *= -1 if MUTATION == 'forward_diffusion_sign'
adjoint['time'] *= -1 if MUTATION == 'adjoint_time_sign'
adjoint['drift'] *= -1 if MUTATION == 'adjoint_drift_sign'
adjoint['secondDerivative'] *= -1 if MUTATION == 'adjoint_diffusion_sign'
shear = rat(operator_fixture.fetch('constantShear'))
shear *= -1 if MUTATION == 'constant_shear'
operator_observed = {
  'forward' => exponent_text(forward),
  'adjoint' => exponent_text(adjoint)
}

# q-a is constant and q attains its minimum at cos(x)=-1.
source_fixture = fixtures.fetch('majorantSourceCase')
q0 = rat(source_fixture.fetch('qConstant'))
q1 = rat(source_fixture.fetch('qCosineCoefficient'))
a1 = rat(source_fixture.fetch('aCosineCoefficient'))
q0 = 0 if MUTATION == 'q_constant'
q1 = 2 if MUTATION == 'q_cosine'
a1 = 2 if MUTATION == 'a_cosine'
majorant_rows = source_fixture.fetch('cosineSamples').map do |cosine_value|
  cosine = rat(cosine_value)
  q_value = q0 + q1 * cosine
  a_value = a1 * cosine
  {
    'cosine' => rtext(cosine), 'q' => rtext(q_value), 'a' => rtext(a_value),
    'qMinusA' => rtext(q_value - a_value)
  }
end
q_modes = source_fixture.fetch('sourceModes').dup
q_modes << 2 if MUTATION == 'q_modes'
a_modes = [-1, 1]
a_modes << 0 if MUTATION == 'a_modes'
majorant_observed = {
  'rows' => majorant_rows,
  'qNonnegativeOnCosineRange' => MUTATION == 'q_nonnegative' ? false : q0 - q1.abs >= 0,
  'qMajorizesAOnCosineRange' =>
    MUTATION == 'q_majorant_direction' ? false : q0 - (q1 - a1).abs >= 0,
  'qModes' => q_modes,
  'aModes' => a_modes
}

# Time reversal turns the zero-terminal problem into a positive forward one.
semigroup_fixture = fixtures.fetch('semigroupCase')
total_time = rat(semigroup_fixture.fetch('T'))
reverse_drift = rat(semigroup_fixture.fetch('reversedGeneratorDrift'))
reverse_diffusion = rat(semigroup_fixture.fetch('reversedGeneratorDiffusion'))
source_sign = rat(semigroup_fixture.fetch('sourceSign'))
reverse_drift *= -1 if MUTATION == 'semigroup_drift_sign'
reverse_diffusion *= -1 if MUTATION == 'semigroup_diffusion_sign'
source_sign *= -1 if MUTATION == 'semigroup_source_sign'
terminal = rat(semigroup_fixture.fetch('terminalValue'))
terminal = 1 if MUTATION == 'phi_terminal'
phi_modes = q_modes.dup
phi_modes << 2 if MUTATION == 'phi_modes'
mass_over_pi = 2 * total_time
mass_over_pi *= -1 if MUTATION == 'phi_mass_sign'
mass_over_pi /= 2 if MUTATION == 'phi_mass_factor'
mass_over_pi += 1 if MUTATION == 'phi_mass_endpoint'
semigroup_observed = {
  'timeDirection' => MUTATION == 'time_reversal' ? 'backward-in-tau' : 'forward-in-tau',
  'duhamelOrientation' => MUTATION == 'time_reversal' ? 'integral-T-to-0' : 'integral-0-to-T',
  'reversedGeneratorDrift' => rtext(reverse_drift),
  'reversedGeneratorDiffusion' => rtext(reverse_diffusion),
  'sourceSign' => rtext(source_sign),
  'terminalValue' => rtext(terminal),
  'PhiNonnegative' => MUTATION != 'phi_nonnegative',
  'PhiEntranceModes' => phi_modes,
  'spatialMassSymbol' => MUTATION == 'phi_mass_sign' ? '-2*pi*T' : '2*pi*T',
  'spatialMassOverPi' => rtext(mass_over_pi)
}

# Exact integral of |cos|^3 from four quarter periods.
moment_fixture = fixtures.fetch('absoluteCosineMoment')
quarter = rat(moment_fixture.fetch('quarterIntegral'))
symmetry = rat(moment_fixture.fetch('symmetryFactor'))
quarter += Rational(1, 3) if MUTATION == 'cos_quarter'
symmetry = 2 if MUTATION == 'cos_symmetry'
full_moment = quarter * symmetry
full_moment += 1 if MUTATION == 'cos_integral'
moment_observed = {
  'quarterIntegral' => rtext(quarter),
  'symmetryFactor' => rtext(symmetry),
  'fullIntegral' => rtext(full_moment)
}

# Direct differentiation and finite Fourier support at k=1,2,5.
family_fixture = fixtures.fetch('passiveFamilyCase')
amplitude = rat(family_fixture.fetch('A'))
amplitude += 1 if MUTATION == 'mass_amplitude'
family_time = rat(family_fixture.fetch('T'))
integer_quantifier = MUTATION != 'k_integer'
lower_quantifier = MUTATION != 'k_lower'
signed_source_frequency = MUTATION == 'signed_source_frequency' ? 2 : 1
family_observed = family_fixture.fetch('integerK').map do |k|
  time_cos = MUTATION == 'decay_sign' || MUTATION == 'time_decay' ? k * k : -k * k
  time_sin = MUTATION == 'phase_direction' || MUTATION == 'time_phase' ? -k : k
  drift_sin = MUTATION == 'drift_phase' ? k : -k
  diffusion_cos = MUTATION == 'laplacian_sign' ? -k * k : k * k
  residual_cos = time_cos + diffusion_cos
  residual_sin = time_sin + drift_sin
  residual_cos += 1 if MUTATION == 'passive_residual'
  square_frequency = MUTATION == 'square_frequency' ? k : 2 * k
  square_zero = amplitude**2 * (MUTATION == 'square_zero_coefficient' ? 1 : Rational(1, 2))
  square_side = amplitude**2 * (MUTATION == 'square_side_coefficient' ? Rational(1, 2) : Rational(1, 4))
  entrance_factor = MUTATION == 'entrance_half' ? 1 : Rational(1, 2)
  boundary_over_pi = entrance_factor * square_zero * mass_over_pi
  boundary_over_pi += 1 if MUTATION == 'orthogonality'
  boundary_over_pi += k if MUTATION == 'boundary_k_dependence'
  decay_factor = MUTATION == 'mass_decay_three' ? 1 : 3
  frequency_denominator = MUTATION == 'mass_k_square' ? k : k * k
  mass_coefficient = full_moment * amplitude**3 / (decay_factor * frequency_denominator)
  mass_coefficient += 1 if MUTATION == 'mass_exact_factor'
  mass_upper = MUTATION == 'mass_upper_direction' ? -mass_coefficient : mass_coefficient
  signed_match = [square_frequency, -square_frequency].include?(signed_source_frequency)
  signed_match = (k == 1) if MUTATION == 'signed_field_frequency'
  signed_match = true if MUTATION == 'signed_mode_match'
  signed_flux = signed_match ? Rational(1) : Rational(0)
  signed_flux += 1 if MUTATION == 'signed_flux_nonzero'
  ratio_cube = boundary_over_pi**3 / mass_upper**2 / (family_time / 2)**3
  ratio_cube += 1 if MUTATION == 'ratio_constant'
  {
    'k' => k,
    'timeCos' => rtext(Rational(time_cos)),
    'timeSin' => rtext(Rational(time_sin)),
    'driftSin' => rtext(Rational(drift_sin)),
    'diffusionCos' => rtext(Rational(diffusion_cos)),
    'residualCos' => rtext(Rational(residual_cos)),
    'residualSin' => rtext(Rational(residual_sin)),
    'squareModes' => [-square_frequency, 0, square_frequency],
    'squareModeCoefficients' => [rtext(square_side), rtext(square_zero), rtext(square_side)],
    'BOverPi' => rtext(boundary_over_pi),
    'massCoefficientTimesOneMinusQ' => rtext(mass_coefficient),
    'massUpperCoefficient' => rtext(mass_upper),
    'ratioCubeNormalized' => rtext(ratio_cube),
    'signedFlux' => rtext(signed_flux)
  }
end

# Symbolic homogeneity, computed separately from the finite frequency rows.
factor_fixture = fixtures.fetch('exponentFactors')
boundary_exponents = factor_fixture.fetch('boundary').to_h { |key, value| [key, rat(value)] }
mass_exponents = factor_fixture.fetch('massUpper').to_h { |key, value| [key, rat(value)] }
boundary_exponents['A'] = 1 if MUTATION == 'boundary_A'
mass_exponents['A'] = 2 if MUTATION == 'mass_A'
mass_exponents['k'] = -1 if MUTATION == 'mass_k'
two_thirds = rat(factor_fixture.fetch('twoThirds'))
two_thirds = Rational(1, 3) if MUTATION == 'two_thirds'
mass_two_thirds = mass_exponents.to_h { |key, value| [key, value * two_thirds] }
ratio_exponents = boundary_exponents.to_h do |key, value|
  [key, value - mass_two_thirds.fetch(key)]
end
ratio_exponents['A'] += 1 if MUTATION == 'ratio_A'
ratio_exponents['k'] -= Rational(1, 3) if MUTATION == 'ratio_k'
exponent_observed = {
  'boundary' => exponent_text(boundary_exponents),
  'massUpper' => exponent_text(mass_exponents),
  'massTwoThirds' => exponent_text(mass_two_thirds),
  'ratio' => exponent_text(ratio_exponents),
  'amplitudeCancels' => MUTATION != 'amplitude_cancel',
  'ratioDiverges' => MUTATION != 'ratio_growth'
}

# The fixed W is chosen before the k-limit; only its oscillatory row vanishes.
weight_fixture = fixtures.fetch('fixedWeightCase')
fixed_weight_observed = {
  'quantifier' => MUTATION == 'W_limit_order' ? 'choose-W-after-k' : 'for-each-fixed-W-then-k-to-infinity',
  'continuous' => MUTATION == 'W_continuous' ? false : weight_fixture.fetch('continuous'),
  'nonnegative' => MUTATION == 'W_nonnegative' ? false : weight_fixture.fetch('nonnegative'),
  'integralPositive' => MUTATION == 'W_integral' ? false : weight_fixture.fetch('integralPositive'),
  'dependsOnK' => MUTATION == 'W_depends_k' ? true : weight_fixture.fetch('dependsOnK'),
  'oscillatoryTerm' => MUTATION == 'W_frequency' ? 'integral-W-cos(kx)' : 'integral-W-cos(2kx)',
  'oscillatoryLimit' => MUTATION == 'riemann_lebesgue' ? 'nonzero' : '0',
  'boundaryLimit' => MUTATION == 'W_boundary_limit' ? '0' : 'A^2/4*integral(W)>0'
}

tags = text.scan(/\\tag\{(K\.[^}]+)\}/).flatten
tags << 'K.1' if MUTATION == 'tag'
references = text.scan(/\(K\.([0-9]+[a-z]?)\)/).flatten.map { |value| "K.#{value}" }
references << 'K.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\\[' }
display_close = text.lines.count { |line| line.strip == '\\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..18).map { |index| "K.#{index}" }

dependency_paths = %w[
  research/r075e_horizontal_cross_mode_flux_reduction.md
  research/r075i_diffusion_safe_block_participation.md
  research/r075j_mean_zero_adjoint_flux_obstruction.md
]
dependency_table_present = dependency_paths.all? do |path|
  text.lines.any? { |line| line.include?(path) && line.include?(FROZEN_SOURCES.fetch(path)) }
end
dependency_table_present = false if MUTATION == 'dependency_table_missing'

required_tokens = [
  '\\mathcal L=\\partial_t+\\partial_2-\\partial_2^2',
  '\\mathcal L^*=-\\partial_t-\\partial_2-\\partial_2^2',
  'q(x_2):=1+\\cos x_2\\ge a(x_2)',
  '\\int_0^{2\\pi}\\Phi(0,x_2)\\,dx_2=2\\pi T',
  'F_k(t,x_2):=A e^{-k^2t}\\cos\\bigl(k(x_2-t)\\bigr)',
  '\\mathcal L F_k=0',
  '\\frac{A^2\\pi T}{2}',
  '\\frac{8A^3}{9k^2}\\bigl(1-e^{-3k^2T}\\bigr)',
  '\\left(\\frac98\\right)^{2/3}k^{4/3}',
  '\\mathcal T_k=0',
  'Let `W` be any fixed continuous',
  'The Riemann--Lebesgue lemma makes the second row tend to zero.',
  'not a counterexample to E.24',
  '\\mathbf{NOT\\ CLAY}'
]

boundary = {
  'integerFrequenciesAtLeastOne' => integer_quantifier && lower_quantifier,
  'exponentialFactorStrictlyBetweenZeroAndOne' => MUTATION != 'exponential_range',
  'massUpperBoundDirectionCorrect' => MUTATION != 'mass_upper_direction',
  'signedFluxZeroForEveryIntegerK' => MUTATION != 'signed_integer_quantifier',
  'physicalFluxNotAbsoluteValue' => MUTATION != 'physical_flux_absolute',
  'fixedWeightIndependentOfK' => !%w[W_depends_k W_limit_order].include?(MUTATION),
  'onlyLocalSpacetimeCubicAtomAloneRuledOut' => MUTATION != 'local_atom_not_alone',
  'notE24Counterexample' => MUTATION != 'e24_counterexample',
  'notAllMajorantsRuledOut' => MUTATION != 'all_majorants_ruled',
  'FDependentTestsRemainOpen' => MUTATION != 'fdependent_ruled',
  'signedKernelsRemainOpen' => MUTATION != 'signed_kernel_ruled',
  'fullVersionMPaymentNotRuledOut' => MUTATION != 'full_versionm_ruled',
  'traceFrequencyAtomRemainsOpen' => MUTATION != 'trace_atom_ruled',
  'passiveFamilyNotNSEAssertion' => MUTATION != 'nse_solution',
  'transitionGeometryOpen' => MUTATION != 'transition_closed',
  'periodicCopiesOpen' => MUTATION != 'periodic_closed',
  'completeClockOpen' => MUTATION != 'complete_clock',
  'fixedDeletionOpen' => MUTATION != 'fixed_deletion',
  'suitableWeakTransferOpen' => MUTATION != 'suitable_weak',
  'regularityOpen' => MUTATION != 'regularity',
  'singularityOpen' => MUTATION != 'singularity',
  'noNoveltyOrPriorityClaim' => MUTATION != 'novelty',
  'noSimulationUsed' => MUTATION != 'simulation_used',
  'notClay' => MUTATION != 'clay'
}

checks = {
  'frozen source bindings' => source_rows.values.all? { |expected_hash, actual_hash| expected_hash == actual_hash },
  'fixture and expected bindings' =>
    fixture_hash == fixture_expected_hash && expected_hash == expected_expected_hash &&
    fixtures.fetch('frozenSources') == FROZEN_SOURCES,
  'primary audit status and main binding' =>
    audit_text.include?(FROZEN_SOURCES.fetch('research/r075k_positive_majorant_high_frequency_trace_loss.md')) &&
    audit_text.include?('Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.') &&
    audit_text.include?('Equation tags K.1--K.18 are unique and consecutive.') &&
    audit_text.include?('All 18 display-math environments are paired.'),
  'three dependency bindings' => dependency_table_present,
  'forward and adjoint signs' => operator_observed == expected.fetch('operators') && shear == 1,
  'nonnegative source majorant' => majorant_observed == expected.fetch('majorantSource'),
  'positive zero-terminal semigroup' =>
    semigroup_observed == expected.fetch('semigroup') && reverse_diffusion.positive? && source_sign.positive? && terminal.zero?,
  'entrance mass and modes' =>
    semigroup_observed.fetch('spatialMassSymbol') == '2*pi*T' && mass_over_pi == 2 * total_time && phi_modes == [-1, 0, 1],
  'passive equation and square support' =>
    family_observed == expected.fetch('passiveFamily') &&
    family_observed.all? { |row| row.fetch('residualCos') == '0' && row.fetch('residualSin') == '0' },
  'boundary orthogonality' => family_observed.all? { |row| row.fetch('BOverPi') == '9' },
  'absolute cosine moment' => moment_observed == expected.fetch('absoluteCosineMoment'),
  'mass formula and upper direction' =>
    MUTATION != 'exponential_range' && MUTATION != 'mass_upper_direction' &&
    family_observed.all? { |row| rat(row.fetch('massCoefficientTimesOneMinusQ')).positive? },
  'amplitude cancellation and growth' =>
    exponent_observed == expected.fetch('exponents') && ratio_exponents == {'A' => 0, 'k' => Rational(4, 3)} &&
    family_observed.each_cons(2).all? { |left, right| rat(right.fetch('ratioCubeNormalized')) > rat(left.fetch('ratioCubeNormalized')) },
  'signed physical flux' =>
    family_observed.all? { |row| row.fetch('signedFlux') == '0' } &&
    integer_quantifier && lower_quantifier && MUTATION != 'signed_integer_quantifier',
  'fixed W and Riemann Lebesgue' => fixed_weight_observed == expected.fetch('fixedWeight'),
  'tags references displays' =>
    tags == expected_tags && tags.uniq.length == 18 && (references.uniq - tags).empty? &&
    display_open == 18 && display_close == 18,
  'formula and status sentinels' => required_tokens.all? { |token| flat_text.include?(token.gsub(/\s+/, ' ')) },
  'source report boundary' =>
    flat_source_text.include?('no complete-clock, regularity, novelty, or priority claim') &&
    flat_source_text.include?('fixed nontrivial positive weight') &&
    source_text.include?('Does the construction disprove E.24?'),
  'claim boundary' => boundary.values.all?,
  'utf8 and control safety' =>
    !scan_text.include?("\uFFFD") && scan_text.each_codepoint.none? { |code| code < 32 && ![9, 10].include?(code) },
  'python canonical ledger agreement' =>
    python_payload.fetch('schema') == SCHEMA && python_payload.fetch('verdict') == 'PASS' &&
    python_payload.dig('assertions', 'passed') == 19 &&
    python_payload.fetch('operators') == operator_observed &&
    python_payload.fetch('majorantSource') == majorant_observed &&
    python_payload.fetch('semigroup') == semigroup_observed &&
    python_payload.fetch('absoluteCosineMoment') == moment_observed &&
    python_payload.fetch('passiveFamily') == family_observed &&
    python_payload.fetch('exponents') == exponent_observed &&
    python_payload.fetch('fixedWeight') == fixed_weight_observed &&
    python_payload.fetch('claimBoundary') == boundary
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed = checks.select { |_name, passed| !passed }.keys
REPORT.write(
  "# R0.75K independent finite audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Mathematical blockers: #{verdict == 'PASS' ? 0 : failed.length}\n" \
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}\n" \
  "- Failed checks: #{failed.empty? ? 'none' : failed.join('; ')}\n\n" \
  "An independent Rational ledger verifies the L/L* signs, q=1+cos(x)>=cos(x), " \
  "the positive reversed semigroup, entrance modes 0,+/-1 and mass 2*pi*T. " \
  "Direct differentiation verifies LF_k=0 and Fourier support 0,+/-2k. " \
  "For k=1,2,5 it recomputes B_k/pi=A^2*T/2, integral |cos(kx)|^3=8/3, " \
  "the 8A^3/(9k^2) mass coefficient, amplitude cancellation, and k^(4/3) growth.\n\n" \
  "The signed physical flux is zero for every integer k>=1. The W quantifier " \
  "is fixed-W first and the Riemann--Lebesgue limit applies only to the " \
  "oscillatory row. The result rules out only a fixed nonnegative entrance " \
  "weight with the local spacetime cubic atom alone; it does not close E.24, " \
  "all majorants, or full Version-M. **NOT CLAY.**\n"
)
puts JSON.generate(
  'suite' => 'r075k-positive-majorant-high-frequency-trace-loss-independent',
  'verdict' => verdict,
  'assertions' => checks.length
)
exit(verdict == 'PASS' ? 0 : 1)
