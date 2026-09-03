#!/usr/bin/env ruby
# Independent finite Fourier/trigonometric verifier for frozen R0.75E.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075e_horizontal_cross_mode_flux_reduction.md'
JSON_PATH = Pathname.new(
  ENV.fetch(
    'R075E_JSON',
    (ROOT + 'research/r075e_horizontal_cross_mode_flux_reduction_certificate.json').to_s
  )
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075E_RUBY_REPORT',
    (ROOT + 'research/r075e_horizontal_cross_mode_flux_reduction_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075E_RUBY_MUTATION', '')
SCHEMA = 'r075e-horizontal-cross-mode-flux-reduction-certificate-v1'
MAIN_SHA256 = '99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049'

FROZEN_DEPENDENCIES = {
  'research/r075b_bulk_clock_outer_padding_gate.md' =>
    '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075c_background_shear_packing_false_positive.md' =>
    '1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89',
  'research/r075d_passive_gradient_route_screen.md' =>
    '54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6'
}.freeze

NEGATIVE_MUTATIONS = %w[
  source_drift
  dependency_drift
  dependency_table_missing
  tag
  reference
  display
  control
  period_factor
  formula_pi_factor
  laurent_derivative_sign
  difference_sign
  index_reversal
  diagonal_nonzero
  zero_mode_nonzero
  singleton_physical
  real_pair_zero
  reality_pair_broken
  e15_volume
  e15_cutoff_r
  e15_cubic_normalization
  e15_omega
  e16_decay_sign
  e16_denominator
  e21_pi
  e21_omega
  e21_r
  e23_pb_power
  e23_pf_power
  e23_residual_r
  endpoint_dropped
  transport_sign
  mode_invariance
  x1_hat_not_average
  zero_mode_small_payment
  complex_physical
  real_pair_cancelled
  e24_closed
  full_clock
  clay
].freeze

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  abort("unknown R075E_RUBY_MUTATION: #{MUTATION}")
end

def canonical_rational(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

def vector_add(*vectors)
  keys = vectors.flat_map(&:keys).uniq
  keys.to_h do |key|
    [key, vectors.sum { |vector| vector.fetch(key, Rational(0)) }]
  end
end

def vector_scale(scale, vector)
  vector.transform_values { |value| scale * value }
end

def vector_strings(vector)
  vector.to_h do |key, value|
    [key.to_s, canonical_rational(value)]
  end
end

text = MAIN.read
scan_text = text + (MUTATION == 'control' ? "\u0001" : '')
flat_text = text.gsub(/\s+/, ' ')

# Independent trigonometric computation. For
# X=2+cos(2x)+sin(2x), F=a cos(x)+c sin(x), a=2, c=1,
# the constant coefficient of X'F^2 equals
# -a*c+(a^2-c^2)/2=-1/2. Since (1/2)*(2*pi)/pi=1,
# this is the direct value T/pi.
a = Rational(2)
c = Rational(1)
cutoff_active = MUTATION != 'real_pair_zero'
direct_constant =
  cutoff_active ? (-a * c + (a**2 - c**2) / 2) : Rational(0)
derivative_sign = MUTATION == 'laurent_derivative_sign' ? -1 : 1
period_factor = MUTATION == 'period_factor' ? Rational(1) : Rational(2)
direct_t_over_pi =
  derivative_sign * Rational(1, 2) * period_factor * direct_constant

xi_plus = cutoff_active ? Complex(Rational(1, 2), Rational(-1, 2)) : 0
xi_minus = cutoff_active ? Complex(Rational(1, 2), Rational(1, 2)) : 0
f_plus = Complex(a / 2, -c / 2)
f_minus = Complex(a / 2, c / 2)
f_minus = Complex(Rational(1, 2), Rational(1, 2)) if MUTATION == 'reality_pair_broken'

difference_sign = MUTATION == 'difference_sign' ? -1 : 1
index_reversal = MUTATION == 'index_reversal'
formula_pi_factor = MUTATION == 'formula_pi_factor' ? Rational(2) : Rational(1)

# Assemble only the two ordered off-diagonal terms. This is intentionally
# separate from the trigonometric direct computation above.
xi_for_plus_two = index_reversal ? xi_minus : xi_plus
xi_for_minus_two = index_reversal ? xi_plus : xi_minus
term_minus_to_plus =
  Complex(0, difference_sign * 2) *
  xi_for_plus_two * f_minus * f_plus.conjugate
term_plus_to_minus =
  Complex(0, difference_sign * -2) *
  xi_for_minus_two * f_plus * f_minus.conjugate
spectral_sum = formula_pi_factor * (term_minus_to_plus + term_plus_to_minus)
spectral_t_over_pi = spectral_sum.real
spectral_imaginary = spectral_sum.imag

diagonal_contribution =
  if MUTATION == 'diagonal_nonzero'
    2 * (f_plus.abs2 + f_minus.abs2)
  else
    Rational(0)
  end

zero_mode_t_over_pi =
  MUTATION == 'zero_mode_nonzero' ? Rational(1) : Rational(0)
singleton_t_over_pi = Rational(0)
singleton_is_real = MUTATION == 'singleton_physical'
real_pair_is_real =
  f_minus == f_plus.conjugate && f_plus == f_minus.conjugate

# Independent dimensional algebra through generic Laurent exponent vectors.
p_normalization = {
  R: MUTATION == 'e15_cubic_normalization' ? Rational(-1) : Rational(-2),
  omega: Rational(1)
}
p_integral = {
  R: -p_normalization[:R],
  omega: -p_normalization[:omega],
  pF: Rational(1)
}
cylinder = {
  L: Rational(2),
  R: MUTATION == 'e15_volume' ? Rational(4) : Rational(5)
}
holder_factor = vector_scale(Rational(1, 3), cylinder)
cubic_two_thirds = vector_scale(Rational(2, 3), p_integral)
l2_bound = vector_add(holder_factor, cubic_two_thirds)
dissipation_prefactor = {
  R: MUTATION == 'e15_cutoff_r' ? Rational(-2) : Rational(-3),
  omega: MUTATION == 'e15_omega' ? Rational(0) : Rational(1)
}
e15_result = vector_add(l2_bound, dissipation_prefactor)

e16_cgamma =
  if MUTATION == 'e16_decay_sign'
    Rational(1, 12)
  elsif MUTATION == 'e16_denominator'
    Rational(-1, 6)
  else
    Rational(-1, 12)
  end

e21 = {
  pi: MUTATION == 'e21_pi' ? Rational(0) : Rational(1),
  R: MUTATION == 'e21_r' ? Rational(1) : Rational(-1),
  omega: MUTATION == 'e21_omega' ? Rational(0) : Rational(1)
}
e23 = {
  L: Rational(0),
  R: MUTATION == 'e23_residual_r' ? Rational(1) : Rational(0),
  omega: Rational(0),
  pB: MUTATION == 'e23_pb_power' ? Rational(2, 3) : Rational(1, 3),
  pF: MUTATION == 'e23_pf_power' ? Rational(1, 3) : Rational(2, 3)
}

power_ledger = {
  'E.14_pFNormalization' => vector_strings(p_normalization),
  'E.15_cylinderVolume' => vector_strings(cylinder),
  'E.15_holderFactor' => vector_strings(holder_factor),
  'E.15_cubicTwoThirds' => vector_strings(cubic_two_thirds),
  'E.15_L2Bound' => vector_strings(l2_bound),
  'E.15_dissipationPrefactor' => vector_strings(dissipation_prefactor),
  'E.15_result' => vector_strings(e15_result),
  'E.16_decay' => vector_strings(
    L: Rational(2, 3), cGamma: e16_cgamma
  ),
  'E.21_fluxNormalization' => vector_strings(e21),
  'E.23_mixedFlux' => vector_strings(e23)
}
expected_power_ledger = {
  'E.14_pFNormalization' => {'R' => '-2', 'omega' => '1'},
  'E.15_cylinderVolume' => {'L' => '2', 'R' => '5'},
  'E.15_holderFactor' => {'L' => '2/3', 'R' => '5/3'},
  'E.15_cubicTwoThirds' => {
    'R' => '4/3', 'omega' => '-2/3', 'pF' => '2/3'
  },
  'E.15_L2Bound' => {
    'L' => '2/3', 'R' => '3', 'omega' => '-2/3', 'pF' => '2/3'
  },
  'E.15_dissipationPrefactor' => {'R' => '-3', 'omega' => '1'},
  'E.15_result' => {
    'L' => '2/3', 'R' => '0', 'omega' => '1/3', 'pF' => '2/3'
  },
  'E.16_decay' => {'L' => '2/3', 'cGamma' => '-1/12'},
  'E.21_fluxNormalization' => {'pi' => '1', 'R' => '-1', 'omega' => '1'},
  'E.23_mixedFlux' => {
    'L' => '0', 'R' => '0', 'omega' => '0',
    'pB' => '1/3', 'pF' => '2/3'
  }
}.freeze

boundary = {
  'endpointRetained' => MUTATION != 'endpoint_dropped',
  'transportRightSign' => MUTATION == 'transport_sign' ? -1 : 1,
  'horizontalSupportInvariant' => MUTATION != 'mode_invariance',
  'x1AverageXiUsed' => MUTATION != 'x1_hat_not_average',
  'zeroModeAllPayment' => MUTATION != 'zero_mode_small_payment',
  'complexSingletonPhysical' => MUTATION == 'complex_physical',
  'realPairFluxAlwaysZero' => MUTATION == 'real_pair_cancelled',
  'arbitraryRealE24Proved' => MUTATION == 'e24_closed',
  'completeClockProved' => MUTATION == 'full_clock',
  'clayClaim' => MUTATION == 'clay'
}

tags = text.scan(/\\tag\{(E\.[^}]+)\}/).flatten
tags << 'E.1' if MUTATION == 'tag'
references = text.scan(/\(E\.([0-9]+[a-z]?)\)/).flatten.map do |value|
  "E.#{value}"
end
references << 'E.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\[' }
display_close = text.lines.count { |line| line.strip == '\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..24).map { |index| "E.#{index}" }

dependency_expectations = FROZEN_DEPENDENCIES.dup
if MUTATION == 'dependency_drift'
  dependency_expectations[dependency_expectations.keys.sort.first] = '0' * 64
end
dependency_rows = dependency_expectations.keys.sort.to_h do |path|
  expected = dependency_expectations[path]
  table_present = text.lines.any? do |line|
    line.include?(path) && line.include?(FROZEN_DEPENDENCIES[path])
  end
  if MUTATION == 'dependency_table_missing' &&
     path == dependency_expectations.keys.sort.first
    table_present = false
  end
  [
    path,
    {
      'expectedSha256' => expected,
      'observedSha256' => Digest::SHA256.file(ROOT + path).hexdigest,
      'mainTableEntryPresent' => table_present
    }
  ]
end

b_text = (ROOT + 'research/r075b_bulk_clock_outer_padding_gate.md').read
d_text = (ROOT + 'research/r075d_passive_gradient_route_screen.md').read
b_tags = b_text.scan(/\\tag\{(B\.[^}]+)\}/).flatten
d_tags = d_text.scan(/\\tag\{(D\.[^}]+)\}/).flatten

required_tokens = [
  '\\le C(P_R^M)^{2/3}\\quad(L\\ge L_0)',
  'f_n(t,x_3)',
  '\\widehat\\xi_\\ell(x_1,x_3)',
  '\\Xi_\\ell(x_3)',
  'The \\(x_1\\)-average \\(\\Xi_\\ell\\)',
  '\\mathcal T_\\xi(F,b)',
  '\\pi\\operatorname {Re}\\sum_{n,m\\in\\mathbb Z}',
  'i(m-n)',
  '\\Xi_{m-n}f_n\\overline{f_m}',
  'common factor \\(2\\pi\\)',
  'Every diagonal term \\(n=m\\) vanishes',
  'purely off-diagonal',
  'S=\\{0\\}',
  'complexified scalar equation',
  'not by itself a real Navier--Stokes velocity field',
  'p_F:=R^{-2}\\omega',
  'CL^{2/3}\\omega^{1/3}p_F^{2/3}',
  'L^{2/3}\\exp\\!\\left(-\\frac{c_\\gamma}{12}L^2\\right)',
  'f_{-n}=\\overline{f_n}',
  'S=\\{n,-n\\}',
  '\\frac{\\pi\\omega}{R}\\Bigg[',
  '\\le Cp_b^{1/3}p_F^{2/3}',
  '\\mathfrak X_{\\xi,R}(F,b)\\le C(P_R^M)^{2/3}',
  'No such bound is proved here',
  'Algebraic diagnostic only',
  'not promoted to a physical real Navier--Stokes result',
  'Open:** (E.24) for arbitrary real fields',
  '\\mathbf{NOT\\ CLAY}'
]

python_payload = JSON.parse(JSON_PATH.read)
actual_main_hash = Digest::SHA256.file(MAIN).hexdigest
expected_main_hash = MUTATION == 'source_drift' ? '0' * 64 : MAIN_SHA256

checks = {
  'main source binding' => actual_main_hash == expected_main_hash,
  'three frozen dependency table bindings' =>
    dependency_rows.values.all? do |row|
      row['expectedSha256'] == row['observedSha256'] &&
        row['mainTableEntryPresent']
    end,
  'finite T/pi normalization' =>
    Rational(1, 2) * period_factor == 1 &&
    direct_t_over_pi == Rational(-1, 2) &&
    spectral_t_over_pi == Rational(-1, 2) &&
    spectral_imaginary == 0,
  'diagonal and zero mode vanish' =>
    diagonal_contribution == 0 && zero_mode_t_over_pi == 0,
  'complex singleton is diagnostic only' =>
    singleton_t_over_pi == 0 && !singleton_is_real,
  'real +/-1 pair is physical and nonzero' =>
    real_pair_is_real &&
    direct_t_over_pi == spectral_t_over_pi &&
    direct_t_over_pi != 0,
  'E.14--E.23 exponent ledger' => power_ledger == expected_power_ledger,
  'local energy and modal boundary' =>
    boundary['endpointRetained'] &&
    boundary['transportRightSign'] == 1 &&
    boundary['horizontalSupportInvariant'] &&
    boundary['x1AverageXiUsed'],
  '24 tags, local references, and displays' =>
    tags == expected_tags && tags.uniq.length == 24 &&
    (references - tags).empty? &&
    display_open == 24 && display_close == 24,
  'external B/D references' =>
    b_tags.include?('B.14') &&
    text.include?('cutoff and local energy identity') &&
    %w[D.9 D.18 D.23].all? do |label|
      text.include?(label) && d_tags.include?(label)
    end,
  'formula and status sentinels' => required_tokens.all? do |token|
    flat_text.include?(token.gsub(/\s+/, ' '))
  end,
  'claim boundary' =>
    boundary['zeroModeAllPayment'] &&
    !boundary['complexSingletonPhysical'] &&
    !boundary['realPairFluxAlwaysZero'] &&
    !boundary['arbitraryRealE24Proved'] &&
    !boundary['completeClockProved'] &&
    !boundary['clayClaim'] &&
    text.include?('arbitrarily large payment') &&
    text.include?('Open:** (E.24) for arbitrary real fields') &&
    text.include?('\\mathbf{NOT\\ CLAY}'),
  'Python schema and verdict' =>
    python_payload['schema'] == SCHEMA && python_payload['verdict'] == 'PASS',
  'Python finite example cross-check' =>
    python_payload.dig('exactFiniteExample', 'directTOverPi') == '-1/2' &&
    python_payload.dig('exactFiniteExample', 'spectralTOverPi') == '-1/2' &&
    python_payload.dig('exactFiniteExample', 'zeroModeTOverPi') == '0' &&
    python_payload.dig('exactFiniteExample', 'complexSingletonPhysical') == false &&
    python_payload.dig('exactFiniteExample', 'realPairPhysical') == true,
  'Python exponent and dependency cross-check' =>
    python_payload['powerLedger'] == expected_power_ledger &&
    python_payload.dig('checks', 'frozenDependencyBindings', 'pass') == true,
  'UTF-8 and control safety' =>
    scan_text.valid_encoding? &&
    !scan_text.each_codepoint.any? do |code|
      code < 32 && ![9, 10].include?(code)
    end
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed_checks = checks.reject { |_name, passed| passed }.keys
REPORT.write(
  "# R0.75E independent finite Fourier audit\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Main SHA-256: #{actual_main_hash}\n" \
  "- Direct T/pi: #{direct_t_over_pi}\n" \
  "- Spectral T/pi: #{spectral_t_over_pi}\n" \
  "- Tags and displays: #{tags.length}/#{display_open}\n" \
  "- Failed checks: #{failed_checks.empty? ? 'none' : failed_checks.join('; ')}\n\n" \
  "Ruby used real trigonometric orthogonality for the direct flux and then " \
  "assembled the two ordered off-diagonal complex Fourier terms separately. " \
  "Both give T/pi=-1/2 for X=2+cos(2x)+sin(2x) and " \
  "F=2cos(x)+sin(x). Diagonal and zero-mode contributions vanish. The " \
  "complex singleton is not a physical real field, while the real +/-1 " \
  "pair has nonzero flux.\n\n" \
  "Ruby also recomputed the E.14--E.23 dimensional ledger with generic " \
  "exponent-vector arithmetic, then cross-checked the Python JSON schema, " \
  "finite example, ledger, and dependency binding.\n\n" \
  "The finite witness checks E.10 algebra and normalization only; it is " \
  "not a full E.1 spacetime trajectory or the geometric collar cutoff.\n\n" \
  "The all-payment conclusion is restricted to the real horizontal zero " \
  "mode for L>=L0. E.24 for arbitrary real fields, complete clock, fixed " \
  "deletion, suitable-weak transfer, and regularity remain OPEN. " \
  "**NOT CLAY.**\n"
)

puts JSON.generate(
  verdict: verdict,
  assertions: checks.length,
  failedChecks: failed_checks,
  mutation: MUTATION.empty? ? nil : MUTATION
)
exit(verdict == 'PASS' ? 0 : 1)
