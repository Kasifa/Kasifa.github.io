#!/usr/bin/env ruby
# Independent exact-arithmetic verifier for the frozen R0.75D certificate.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075d_passive_gradient_route_screen.md'
JSON_PATH = Pathname.new(
  ENV.fetch(
    'R075D_JSON',
    (ROOT + 'research/r075d_passive_gradient_route_screen_certificate.json').to_s
  )
)
REPORT = Pathname.new(
  ENV.fetch(
    'R075D_RUBY_REPORT',
    (ROOT + 'research/r075d_passive_gradient_route_screen_independent_audit.md').to_s
  )
)
MUTATION = ENV.fetch('R075D_RUBY_MUTATION', '')
SCHEMA = 'r075d-passive-gradient-route-screen-certificate-v1'
MAIN_SHA256 = '54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6'

CERTIFICATE_DEPENDENCIES = {
  'research/r075b_bulk_clock_outer_padding_gate.md' =>
    '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075c_background_shear_packing_false_positive.md' =>
    '1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89'
}.freeze

NEGATIVE_MUTATIONS = %w[
  holder_volume
  cubic_payment_r
  target_weight
  klow_threshold
  klow_rate
  modal_energy_sign
  modal_decay
  zero_mode_omission
  gradient_forcing_sign
  gradient_dissipation
  transition_volume
  block_count
  critical_threshold
  gap_fraction
  transport_sign
  transport_dropped
  pf_normalization
  fallback_cutoff_r
  fallback_volume
  mixed_holder
  mixed_weight
  cubic_sum
  pb_scale
  pb_rate
  small_payment_direction
  linear_absorbed
  interaction_power
  component_promotion
  high_frequency_proved
  intermediate_band_closed
  commutator_closed
  periodic_dropped
  counterexample_promotion
  full_clock_promotion
  source_drift
  dependency_drift
  dependency_table_assumed
  tag
  reference
  display
  clay
].freeze

unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  abort("unknown R075D_RUBY_MUTATION: #{MUTATION}")
end

def exponent_row(values)
  values.transform_values do |value|
    value.denominator == 1 ? value.numerator.to_s : value.to_s
  end
end

text = MAIN.read
flat_text = text.gsub(/\s+/, ' ')
rho = Rational(9, 10_000)
c_gamma = Rational(8, 3969)

volume_l = Rational(2)
volume_r = MUTATION == 'holder_volume' ? Rational(4) : Rational(5)
holder_l = volume_l / 3
holder_r = volume_r / 3

cubic_r = MUTATION == 'cubic_payment_r' ? Rational(1) : Rational(2)
cubic_omega = Rational(-1)
cubic_payment = Rational(1)
cubic_two_thirds_r = Rational(2, 3) * cubic_r
cubic_two_thirds_omega = Rational(2, 3) * cubic_omega
cubic_two_thirds_payment = Rational(2, 3) * cubic_payment

l2_l = holder_l
l2_r = holder_r + cubic_two_thirds_r
l2_omega = cubic_two_thirds_omega
l2_payment = cubic_two_thirds_payment

prefactor_r = Rational(-1)
prefactor_omega = MUTATION == 'target_weight' ? Rational(0) : Rational(1)
target_k = Rational(2)
target_l = l2_l
target_r = l2_r + prefactor_r
target_omega = l2_omega + prefactor_omega
target_payment = l2_payment

klow_r = -target_r / 2
klow_l = -target_l / 2
klow_omega = -target_omega / 2
klow_omega = Rational(1, 6) if MUTATION == 'klow_threshold'

power_ledger = {
  'D.4_spacetimeVolume' => exponent_row('L' => volume_l, 'R' => volume_r),
  'D.4_holderMeasureFactor' => exponent_row('L' => holder_l, 'R' => holder_r),
  'D.4_cubicPayment' => exponent_row(
    'R' => cubic_r, 'omega' => cubic_omega, 'payment' => cubic_payment
  ),
  'D.4_cubicTwoThirds' => exponent_row(
    'R' => cubic_two_thirds_r,
    'omega' => cubic_two_thirds_omega,
    'payment' => cubic_two_thirds_payment
  ),
  'D.4_L2Bound' => exponent_row(
    'L' => l2_l, 'R' => l2_r, 'omega' => l2_omega,
    'payment' => l2_payment
  ),
  'D.5_targetCoefficient' => exponent_row(
    'K' => target_k, 'L' => target_l, 'R' => target_r,
    'omega' => target_omega, 'payment' => target_payment
  ),
  'D.6_Klow' => exponent_row(
    'L' => klow_l, 'R' => klow_r, 'omega' => klow_omega
  )
}

expected_power_ledger = {
  'D.4_spacetimeVolume' => {'L' => '2', 'R' => '5'},
  'D.4_holderMeasureFactor' => {'L' => '2/3', 'R' => '5/3'},
  'D.4_cubicPayment' => {'R' => '2', 'omega' => '-1', 'payment' => '1'},
  'D.4_cubicTwoThirds' => {
    'R' => '4/3', 'omega' => '-2/3', 'payment' => '2/3'
  },
  'D.4_L2Bound' => {
    'L' => '2/3', 'R' => '3', 'omega' => '-2/3', 'payment' => '2/3'
  },
  'D.5_targetCoefficient' => {
    'K' => '2', 'L' => '2/3', 'R' => '2',
    'omega' => '1/3', 'payment' => '2/3'
  },
  'D.6_Klow' => {'L' => '-1/3', 'R' => '-1', 'omega' => '-1/6'}
}.freeze

klow_rate = (-klow_r) * rho / 4 + (-klow_omega) * c_gamma / 4
klow_rate += Rational(1, 10**9) if MUTATION == 'klow_rate'
expected_klow_rate = Rational(147_163, 476_280_000)

block_count_r = MUTATION == 'block_count' ? Rational(-2) : Rational(-1)
critical_k_r = MUTATION == 'critical_threshold' ? Rational(-1) : Rational(-3, 2)
critical_rate = (-critical_k_r) * rho / 4
gap = critical_rate - expected_klow_rate
gap += Rational(1, 10**9) if MUTATION == 'gap_fraction'
expected_gap = Rational(27_163, 952_560_000)

mass_normalization_r =
  MUTATION == 'pf_normalization' ? Rational(-1) : Rational(-2)
mass_normalization_omega = Rational(1)
cubic_integral_r = -mass_normalization_r
cubic_integral_omega = -mass_normalization_omega

fallback_volume_l = Rational(2)
fallback_volume_r =
  MUTATION == 'fallback_volume' ? Rational(4) : Rational(5)
cutoff_prefactor_r =
  MUTATION == 'fallback_cutoff_r' ? Rational(-2) : Rational(-3)
cutoff_prefactor_omega = Rational(1)
fallback_result_l = fallback_volume_l / 3
fallback_result_r =
  cutoff_prefactor_r + fallback_volume_r / 3 +
  Rational(2, 3) * cubic_integral_r
fallback_result_omega =
  cutoff_prefactor_omega + Rational(2, 3) * cubic_integral_omega

transport_sign = MUTATION == 'transport_sign' ? -1 : 1
transport_retained = MUTATION != 'transport_dropped'
transport_prefactor_r = Rational(-2)
transport_prefactor_omega =
  MUTATION == 'mixed_weight' ? Rational(0) : Rational(1)
mixed_b_power =
  MUTATION == 'mixed_holder' ? Rational(2, 3) : Rational(1, 3)
mixed_f_power = Rational(1) - mixed_b_power
mixed_result_r =
  transport_prefactor_r +
  (mixed_b_power + mixed_f_power) * cubic_integral_r
mixed_result_omega =
  transport_prefactor_omega +
  (mixed_b_power + mixed_f_power) * cubic_integral_omega
cubic_sum_controlled = MUTATION != 'cubic_sum'

pb_l = Rational(2)
pb_r = MUTATION == 'pb_scale' ? Rational(-2) : Rational(-3)
pb_omega = Rational(1)
pb_rate = (-pb_r) * rho / 4 - pb_omega * c_gamma / 4
pb_rate += Rational(1, 10**9) if MUTATION == 'pb_rate'
expected_pb_rate = Rational(27_163, 158_760_000)

small_payment_leq_one = MUTATION != 'small_payment_direction'
linear_term_absorbed = MUTATION == 'linear_absorbed'
interaction_pb_power = Rational(1)
interaction_pf_power =
  MUTATION == 'interaction_power' ? Rational(1) : Rational(2)
interaction_payment_power = Rational(-2)

fallback_ledger = {
  'D.16_massNormalization' => exponent_row(
    'R' => mass_normalization_r, 'omega' => mass_normalization_omega
  ),
  'D.18_spacetimeVolume' => exponent_row(
    'L' => fallback_volume_l, 'R' => fallback_volume_r
  ),
  'D.18_cutoffPrefactor' => exponent_row(
    'R' => cutoff_prefactor_r, 'omega' => cutoff_prefactor_omega
  ),
  'D.18_result' => exponent_row(
    'L' => fallback_result_l,
    'R' => fallback_result_r,
    'omega' => fallback_result_omega,
    'pF' => Rational(2, 3)
  ),
  'D.19_transportPrefactor' => exponent_row(
    'R' => transport_prefactor_r, 'omega' => transport_prefactor_omega
  ),
  'D.19_mixedResult' => exponent_row(
    'R' => mixed_result_r,
    'omega' => mixed_result_omega,
    'pB' => mixed_b_power,
    'pF' => mixed_f_power
  ),
  'D.22_pBScale' => exponent_row(
    'L' => pb_l, 'R' => pb_r, 'omega' => pb_omega
  ),
  'D.23_interactionCondition' => exponent_row(
    'pB' => interaction_pb_power,
    'pF' => interaction_pf_power,
    'payment' => interaction_payment_power
  )
}

expected_fallback_ledger = {
  'D.16_massNormalization' => {'R' => '-2', 'omega' => '1'},
  'D.18_spacetimeVolume' => {'L' => '2', 'R' => '5'},
  'D.18_cutoffPrefactor' => {'R' => '-3', 'omega' => '1'},
  'D.18_result' => {
    'L' => '2/3', 'R' => '0', 'omega' => '1/3', 'pF' => '2/3'
  },
  'D.19_transportPrefactor' => {'R' => '-2', 'omega' => '1'},
  'D.19_mixedResult' => {
    'R' => '0', 'omega' => '0', 'pB' => '1/3', 'pF' => '2/3'
  },
  'D.22_pBScale' => {'L' => '2', 'R' => '-3', 'omega' => '1'},
  'D.23_interactionCondition' => {
    'pB' => '1', 'pF' => '2', 'payment' => '-2'
  }
}.freeze

modal = {
  'diffusionCoefficient' => -1,
  'horizontalLaplacianCoefficient' => 1,
  'imaginaryShearCoefficient' => 1,
  'energyTimeDerivative' => '1/2',
  'verticalDissipationSign' => 1,
  'horizontalDissipationSign' =>
    (MUTATION == 'modal_energy_sign' ? -1 : 1),
  'shearRealPart' => 0,
  'normDecayCoefficient' => (MUTATION == 'modal_decay' ? 2 : 1)
}
expected_modal = {
  'diffusionCoefficient' => -1,
  'horizontalLaplacianCoefficient' => 1,
  'imaginaryShearCoefficient' => 1,
  'energyTimeDerivative' => '1/2',
  'verticalDissipationSign' => 1,
  'horizontalDissipationSign' => 1,
  'shearRealPart' => 0,
  'normDecayCoefficient' => 1
}.freeze

zero_mode_obstruction = MUTATION != 'zero_mode_omission'
gradient_forcing_sign = MUTATION == 'gradient_forcing_sign' ? 1 : -1
gradient_dissipation =
  MUTATION == 'gradient_dissipation' ? 'Hessian' : 'Laplacian'

transition_l = MUTATION == 'transition_volume' ? Rational(2) : Rational(1)
transition_r = Rational(3)
full_collar_l = Rational(2)
full_collar_r = Rational(3)

route_state = {
  'exactPassiveFallbackProved' => true,
  'smallPaymentFallbackProved' => true,
  'frozenLargePaymentBranchClosed' => linear_term_absorbed,
  'interactionConditionProved' => linear_term_absorbed,
  'transportRetained' => transport_retained,
  'unconditionalLowFrequencyLemma' => MUTATION == 'component_promotion',
  'highFrequencyLocalCaptureProved' => MUTATION == 'high_frequency_proved',
  'intermediateBandClosed' => MUTATION == 'intermediate_band_closed',
  'commutatorsClosed' => MUTATION == 'commutator_closed',
  'periodizationRetained' => MUTATION != 'periodic_dropped',
  'exactCounterexampleConstructed' => MUTATION == 'counterexample_promotion',
  'fullClockExtractionProved' => MUTATION == 'full_clock_promotion',
  'clayClaim' => MUTATION == 'clay'
}

tags = text.scan(/\\tag\{(D\.[^}]+)\}/).flatten
tags << 'D.1' if MUTATION == 'tag'
references = text.scan(/\(D\.([0-9]+[a-z]?)\)/).flatten.map do |value|
  "D.#{value}"
end
references << 'D.99' if MUTATION == 'reference'
display_open = text.lines.count { |line| line.strip == '\[' }
display_close = text.lines.count { |line| line.strip == '\]' }
display_open += 1 if MUTATION == 'display'
expected_tags = (1..23).map { |index| "D.#{index}" }

dependency_expectations = CERTIFICATE_DEPENDENCIES.dup
if MUTATION == 'dependency_drift'
  dependency_expectations[dependency_expectations.keys.sort.first] = '0' * 64
end
dependency_rows = dependency_expectations.keys.sort.to_h do |path|
  [
    path,
    {
      'expectedSha256' => dependency_expectations[path],
      'observedSha256' => Digest::SHA256.file(ROOT + path).hexdigest,
      'bindingMode' => 'certificate-side',
      'mainTableEntryRequired' => false
    }
  ]
end
dependency_table_assumed = MUTATION == 'dependency_table_assumed'
main_source_table_present =
  CERTIFICATE_DEPENDENCIES.values.any? { |digest| text.include?(digest) }

b_text = (ROOT + 'research/r075b_bulk_clock_outer_padding_gate.md').read
b_tags = b_text.scan(/\\tag\{(B\.[^}]+)\}/).flatten
c_text = (ROOT + 'research/r075c_background_shear_packing_false_positive.md').read
c_tags = c_text.scan(/\\tag\{(C\.[^}]+)\}/).flatten

required_tokens = [
  'D_{k,R}^{{\\rm out},F}',
  '\\frac{\\omega}{R}\\int_{I_{2R}}\\int',
  'O(L^2R^5)',
  'CL^{2/3}R^{5/3}',
  'CR^2\\omega^{-1}P_R^M',
  'CK^2L^{2/3}R^2\\omega^{1/3}(P_R^M)^{2/3}',
  'cR^{-1}L^{-1/3}\\omega^{-1/6}',
  '\\frac\\rho4+\\frac{c_\\gamma}{24}+o(1)',
  'not yet an unconditional low-frequency lemma',
  '\\partial_tf_n-\\partial_3^2f_n+(n^2+inb)f_n=0',
  'F_m(t,x_3)=e^{-m^2t}\\sin(mx_3)',
  '=-b_3\\partial_2F',
  '+\\|\\Delta_{23}F\\|_2^2',
  '=-\\int b_3\\,\\partial_2F\\,\\partial_3F',
  'O(LR^3)',
  'O(L^2R^3)',
  'K^2R^3\\gg1',
  'K\\gg R^{-3/2}',
  '\\frac\\rho8-\\frac{c_\\gamma}{24}>0',
  'K_{\\rm low}\\ll K\\lesssim R^{-3/2}',
  '[P_{\\le K},b]\\partial_2F',
  '[P_{\\le K},\\xi_k^R]F',
  'Periodization must be retained before using any kernel estimate',
  'p_F&:=R^{-2}\\omega',
  'p_b&:=R^{-2}\\omega',
  'p_F+p_b\\le CP_R^M',
  '\\omega R^{-3}\\int_{I_{2R}}\\int_{\\rm out}|F|^2',
  'CL^{2/3}\\omega^{1/3}p_F^{2/3}',
  '\\omega R^{-2}\\int_{I_{2R}}\\int_{\\rm out}|b||F|^2',
  '=p_b^{1/3}p_F^{2/3}',
  '+Cp_b^{1/3}p_F^{2/3}',
  '+CP_R^M.',
  'P_R^M\\le1',
  'P_R^M\\le(P_R^M)^{2/3}',
  'p_b\\asymp L^2\\omega R^{-3}',
  '\\frac{27163}{158760000}>0',
  'P_R^M\\ge c p_b\\to\\infty',
  'p_bp_F^2\\le C(P_R^M)^2',
  'No such uniform interaction bound is presently proved',
  'Reapplying absolute Hölder/Young inequalities cannot change',
  'every commutator and shell-weight tail remains OPEN',
  'NO EXACT COUNTEREXAMPLE CONSTRUCTED',
  'proves neither complete-clock extraction nor a',
  '\\mathbf{NOT\\ CLAY}'
]

python_payload = JSON.parse(JSON_PATH.read)
actual_main_hash = Digest::SHA256.file(MAIN).hexdigest
expected_main_hash = MUTATION == 'source_drift' ? '0' * 64 : MAIN_SHA256

checks = {
  'main source binding' => actual_main_hash == expected_main_hash,
  'certificate-side B/C bindings' => dependency_rows.values.all? do |row|
    row['expectedSha256'] == row['observedSha256']
  end,
  'dependency boundary' =>
    !dependency_table_assumed && !main_source_table_present,
  'D.4--D.6 power ledger' => power_ledger == expected_power_ledger,
  'D.7 exact K-low rate' =>
    klow_rate == expected_klow_rate && klow_rate.positive?,
  'D.16--D.23 fallback power ledger' =>
    fallback_ledger == expected_fallback_ledger,
  'transport and cubic separation' =>
    transport_sign == 1 && transport_retained && cubic_sum_controlled,
  'D.22 exact shear-payment rate' =>
    pb_rate == expected_pb_rate && pb_rate.positive?,
  'small-payment and interaction boundary' =>
    small_payment_leq_one && !linear_term_absorbed &&
    [interaction_pb_power, interaction_pf_power,
     interaction_payment_power] == [Rational(1), Rational(2), Rational(-2)],
  'modal equation and energy' => modal == expected_modal,
  'vertical zero-mode obstruction' =>
    zero_mode_obstruction &&
    text.include?('F_m(t,x_3)=e^{-m^2t}\\sin(mx_3)') &&
    text.include?('arbitrarily large vertical gradient'),
  'gradient sign and Laplacian dissipation' =>
    gradient_forcing_sign == -1 && gradient_dissipation == 'Laplacian',
  'transition-band geometry' =>
    [transition_l, transition_r, full_collar_l, full_collar_r] ==
      [Rational(1), Rational(3), Rational(2), Rational(3)],
  'short blocks and exact intermediate gap' =>
    block_count_r == -1 &&
    critical_k_r == Rational(-3, 2) &&
    critical_rate == Rational(27, 80_000) &&
    gap == expected_gap && gap.positive?,
  '23 tags, local references, and displays' =>
    tags == expected_tags && tags.uniq.length == 23 &&
    (references - tags).empty? &&
    display_open == 23 && display_close == 23,
  'external B.38 and R0.75C boundary' =>
    %w[B.14 B.38].all? { |label| text.include?(label) && b_tags.include?(label) } &&
    text.include?('R0.75C') &&
    %w[C.13 C.14 C.15 C.35].all? { |label| c_tags.include?(label) } &&
    c_text.include?('R075C_BACKGROUND_SHEAR_DISSIPATION_PAID'),
  'formula and status sentinels' => required_tokens.all? do |token|
    flat_text.include?(token.gsub(/\s+/, ' '))
  end,
  'analytic blockers retained' =>
    route_state['exactPassiveFallbackProved'] &&
    route_state['smallPaymentFallbackProved'] &&
    !route_state['frozenLargePaymentBranchClosed'] &&
    !route_state['interactionConditionProved'] &&
    route_state['transportRetained'] &&
    !route_state['highFrequencyLocalCaptureProved'] &&
    !route_state['intermediateBandClosed'] &&
    !route_state['commutatorsClosed'] &&
    route_state['periodizationRetained'],
  'claim boundary' =>
    route_state['exactPassiveFallbackProved'] &&
    route_state['smallPaymentFallbackProved'] &&
    !route_state['frozenLargePaymentBranchClosed'] &&
    !route_state['interactionConditionProved'] &&
    !route_state['unconditionalLowFrequencyLemma'] &&
    !route_state['exactCounterexampleConstructed'] &&
    !route_state['fullClockExtractionProved'] &&
    !route_state['clayClaim'] &&
    text.include?('not yet an unconditional low-frequency lemma') &&
    text.include?('NO EXACT COUNTEREXAMPLE CONSTRUCTED') &&
    text.include?('No such uniform interaction bound is presently proved') &&
    text.include?('proves neither complete-clock extraction') &&
    text.include?('\\mathbf{NOT\\ CLAY}'),
  'Python schema and verdict' =>
    python_payload['schema'] == SCHEMA && python_payload['verdict'] == 'PASS',
  'Python exact values' =>
    python_payload.dig('exactValues', 'klowRate') ==
      '147163/476280000' &&
    python_payload.dig('exactValues', 'intermediateGap') ==
      '27163/952560000' &&
    python_payload.dig('exactValues', 'shearPaymentRate') ==
      '27163/158760000',
  'Python ledger and dependency boundary' =>
    python_payload['powerLedger'] == expected_power_ledger &&
    python_payload['fallbackLedger'] == expected_fallback_ledger &&
    python_payload['dependencyBoundary'].include?(
      'certificate-side only'
    ),
  'UTF-8 and control safety' =>
    text.valid_encoding? &&
    !text.each_codepoint.any? { |code| code < 32 && ![9, 10].include?(code) }
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
failed_checks = checks.reject { |_name, passed| passed }.keys
REPORT.write(
  "# R0.75D independent Ruby verification\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Main SHA-256: #{actual_main_hash}\n" \
  "- K-low exact rate: #{klow_rate}\n" \
  "- Intermediate-band exact gap: #{gap}\n" \
  "- Frozen shear-payment rate: #{pb_rate}\n" \
  "- Tags: #{tags.length}; displays: #{display_open}/#{display_close}\n\n" \
  "- Failed checks: #{failed_checks.empty? ? 'none' : failed_checks.join('; ')}\n\n" \
  "Ruby independently recomputed the D.4--D.7 exponent ledger, modal and " \
  "gradient signs, collar volumes, block threshold, and exact fractions. " \
  "It also recomputed the D.16--D.23 mass normalizations, cutoff and mixed " \
  "Holder powers, shear-payment rate, small-payment direction, and " \
  "interaction homogeneity. It then cross-checked the Python schema, exact " \
  "values, both exponent ledgers, and certificate-side dependency " \
  "boundary.\n\n" \
  "R0.75D has no embedded frozen-source table. The B/C hashes are bound by " \
  "this certificate suite only.\n\n" \
  "The exact fallback is P^(2/3)+P and pays only the small-payment regime. " \
  "The frozen branch has P tending to infinity, so its linear term is not " \
  "absorbed. Low-frequency payment remains conditional. The interaction " \
  "condition, intermediate-frequency capture, commutators, projection " \
  "leakage, periodic weights, and an exact counterexample remain open. No " \
  "complete-clock result is certified. **NOT CLAY.**\n"
)

puts JSON.generate(
  verdict: verdict,
  assertions: checks.length,
  failedChecks: failed_checks,
  mutation: MUTATION.empty? ? nil : MUTATION
)
exit(verdict == 'PASS' ? 0 : 1)
