#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent exact-arithmetic audit for the R0.74I finite certificate.
#
# All arithmetic is reconstructed with Ruby Rational values before the frozen
# JSON is opened.  The JSON is used only as a comparison target.  No frozen
# field is used as an arithmetic input.

require "json"

CERTIFICATE_PATH = File.expand_path(
  "../research/r074i_tube_log_certificate.json",
  __dir__
)

def rational_string(value)
  "#{value.numerator}/#{value.denominator}"
end

def exact_check(id, left, relation, right, note)
  case relation
  when "=="
    margin = left - right
    passed = left == right
  when "<"
    margin = right - left
    passed = left < right
  else
    raise ArgumentError, "unsupported relation: #{relation}"
  end

  {
    "id" => id,
    "left" => rational_string(left),
    "relation" => relation,
    "right" => rational_string(right),
    "margin" => rational_string(margin),
    "pass" => passed,
    "note" => note
  }
end

def flatten_leaves(value, path = "$", output = {})
  case value
  when Hash
    value.keys.sort.each do |key|
      flatten_leaves(value.fetch(key), "#{path}.#{key}", output)
    end
  when Array
    value.each_with_index do |item, index|
      flatten_leaves(item, "#{path}[#{index}]", output)
    end
  else
    output[path] = value
  end
  output
end

one = Rational(1, 1)
two = Rational(2, 1)
half = Rational(1, 2)
two_thirds = Rational(2, 3)
three_halves = Rational(3, 2)

# Navier--Stokes scaling, reconstructed from primitive definitions.
rescaled_velocity_power = one
velocity_cubic_power = Rational(3, 1) * rescaled_velocity_power
inverse_space_jacobian_power = Rational(-3, 1)
inverse_time_jacobian_power = Rational(-2, 1)
scaled_l3_power = velocity_cubic_power +
                  inverse_space_jacobian_power +
                  inverse_time_jacobian_power
physical_velocity_cubic_power = Rational(-3, 1)
physical_space_jacobian_power = Rational(3, 1)
physical_time_jacobian_power = Rational(2, 1)
physical_l3_integral_power = physical_velocity_cubic_power +
                             physical_space_jacobian_power +
                             physical_time_jacobian_power
normalized_physical_l3_power = Rational(-2, 1) + physical_l3_integral_power

half_radius_time_factor = half**2
half_radius_normalization_factor = half**-2

energy_recovery_power = three_halves * two_thirds
tube_threshold_recovery_power = three_halves * two_thirds
combined_l3_to_payment_power = two_thirds * three_halves

rho = Rational(1, 320)
two_rho = Rational(2, 1) * rho
three_rho = Rational(3, 1) * rho
window_width = three_rho - two_rho
l_prefactor = Rational(63, 32)
next_l_prefactor = Rational(2, 1) * l_prefactor
l_square_ratio = two**2
next_lower_log_exponent = Rational(2, 1) * rho * l_square_ratio
lacunarity_log_exponent = next_lower_log_exponent - Rational(3, 1) * rho

payment_b_power = Rational(3, 1)
payment_r_power = Rational(3, 1)
payment_l_power = Rational(0, 1)
payment_23_b_power = payment_b_power * two_thirds
payment_23_r_power = payment_r_power * two_thirds
payment_23_l_power = payment_l_power * two_thirds
sqrt_log_l_power = Rational(2, 1) * half
frontier_l_power = payment_23_l_power + sqrt_log_l_power

gap_constant_coefficient = half - half
gap_delta_coefficient = Rational(0, 1) - Rational(-1, 1)

endpoint_l_after_cancellation = one - one
endpoint_inverse_outer_power = one / two_thirds
endpoint_payment_power = two_thirds * endpoint_inverse_outer_power
endpoint_b_power = Rational(2, 1) * endpoint_inverse_outer_power
endpoint_r_power = Rational(2, 1) * endpoint_inverse_outer_power
endpoint_k_power = Rational(-1, 1) * endpoint_inverse_outer_power

b_lower = Rational(1, 256)
b_limit = Rational(1, 128)
b_upper = Rational(1, 64)

checks = [
  exact_check(
    "ns_rescaled_velocity_cubic_power",
    velocity_cubic_power,
    "==",
    Rational(3, 1),
    "U=r*u contributes r^3 to |U|^3"
  ),
  exact_check(
    "ns_inverse_space_jacobian_power",
    inverse_space_jacobian_power,
    "==",
    Rational(-3, 1),
    "xi=(x-x0)/r gives dxi=r^-3 dx"
  ),
  exact_check(
    "ns_inverse_time_jacobian_power",
    inverse_time_jacobian_power,
    "==",
    Rational(-2, 1),
    "s=(t-t0)/r^2 gives ds=r^-2 dt"
  ),
  exact_check(
    "ns_scaled_l3_total_power",
    scaled_l3_power,
    "==",
    Rational(-2, 1),
    "the transformed unit-cylinder integral equals r^-2 times the physical integral"
  ),
  exact_check(
    "ns_physical_l3_integral_power",
    physical_l3_integral_power,
    "==",
    Rational(2, 1),
    "u=r^-1 U, dx=r^3 dxi, and dt=r^2 ds give physical L3 power r^2"
  ),
  exact_check(
    "ns_normalized_l3_scale_invariance",
    normalized_physical_l3_power,
    "==",
    Rational(0, 1),
    "r^-2 times the physical L3 integral is scale invariant"
  ),
  exact_check(
    "half_radius_time_length_factor",
    half_radius_time_factor,
    "==",
    Rational(1, 4),
    "the interval I_(R/2) has length R^2/4"
  ),
  exact_check(
    "half_radius_normalization_factor",
    half_radius_normalization_factor,
    "==",
    Rational(4, 1),
    "(R/2)^-2 equals 4 R^-2"
  ),
  exact_check(
    "half_radius_fixed_factor_product",
    half_radius_time_factor * half_radius_normalization_factor,
    "==",
    one,
    "the exact time-length and normalization factors multiply to one"
  ),
  exact_check(
    "energy_from_payment_inverse_power",
    energy_recovery_power,
    "==",
    one,
    "raising E^(3/2)<=P to the power 2/3 recovers E<=P^(2/3)"
  ),
  exact_check(
    "tube_to_payment_threshold_power",
    tube_threshold_recovery_power,
    "==",
    one,
    "P<=epsilon_tube^(3/2) implies P^(2/3)<=epsilon_tube at the exponent level"
  ),
  exact_check(
    "l3_to_payment_threshold_chain",
    combined_l3_to_payment_power,
    "==",
    one,
    "an L3 threshold exponent 2/3 followed by the payment exponent 3/2 is linear"
  ),
  exact_check(
    "rho_exact_value",
    rho,
    "==",
    Rational(1, 320),
    "the frozen packet family uses rho=1/320"
  ),
  exact_check(
    "two_rho",
    two_rho,
    "==",
    Rational(1, 160),
    "the lower logarithmic-window coefficient is 2 rho"
  ),
  exact_check(
    "three_rho",
    three_rho,
    "==",
    Rational(3, 320),
    "the upper logarithmic-window coefficient is 3 rho"
  ),
  exact_check(
    "log_window_width",
    window_width,
    "==",
    Rational(1, 320),
    "3 rho minus 2 rho equals rho"
  ),
  exact_check(
    "next_L_prefactor",
    next_l_prefactor,
    "==",
    Rational(63, 16),
    "L_(j+1)=2 L_j doubles the exact prefactor 63/32"
  ),
  exact_check(
    "L_square_ratio",
    l_square_ratio,
    "==",
    Rational(4, 1),
    "L_(j+1)^2=4 L_j^2"
  ),
  exact_check(
    "next_lower_log_exponent",
    next_lower_log_exponent,
    "==",
    Rational(1, 40),
    "2 rho L_(j+1)^2 contributes 8 rho L_j^2"
  ),
  exact_check(
    "lacunarity_log_exponent",
    lacunarity_log_exponent,
    "==",
    Rational(1, 64),
    "8 rho minus 3 rho equals 5 rho=1/64"
  ),
  exact_check(
    "payment_upper_23_B_power",
    payment_23_b_power,
    "==",
    Rational(2, 1),
    "(B^3 R^3)^(2/3) recovers B^2"
  ),
  exact_check(
    "payment_upper_23_R_power",
    payment_23_r_power,
    "==",
    Rational(2, 1),
    "(B^3 R^3)^(2/3) recovers R^2"
  ),
  exact_check(
    "payment_upper_23_L_power",
    payment_23_l_power,
    "==",
    Rational(0, 1),
    "the frozen payment upper scale has no L power before the logarithmic factor"
  ),
  exact_check(
    "sqrt_log_recovers_L_power",
    sqrt_log_l_power,
    "==",
    one,
    "sqrt of a logarithmic window proportional to L^2 contributes L^1"
  ),
  exact_check(
    "frontier_total_L_power",
    frontier_l_power,
    "==",
    one,
    "P^(2/3) sqrt(log P) has the target L power"
  ),
  exact_check(
    "subcritical_gap_constant_coefficient",
    gap_constant_coefficient,
    "==",
    Rational(0, 1),
    "in 1/2-(1/2-delta), the constant coefficient cancels"
  ),
  exact_check(
    "subcritical_gap_delta_coefficient",
    gap_delta_coefficient,
    "==",
    one,
    "in 1/2-(1/2-delta), the delta coefficient is one"
  ),
  exact_check(
    "endpoint_gamma_gap",
    half - half,
    "==",
    Rational(0, 1),
    "at gamma=1/2 the logarithmic exponent gap is zero"
  ),
  exact_check(
    "endpoint_L_cancellation",
    endpoint_l_after_cancellation,
    "==",
    Rational(0, 1),
    "the target L and sqrt-log L factors cancel in a hypothetical endpoint estimate"
  ),
  exact_check(
    "endpoint_inverse_outer_power",
    endpoint_inverse_outer_power,
    "==",
    three_halves,
    "inverting the outer power 2/3 requires raising to 3/2"
  ),
  exact_check(
    "endpoint_payment_power",
    endpoint_payment_power,
    "==",
    one,
    "raising P^(2/3) to 3/2 recovers P"
  ),
  exact_check(
    "endpoint_forced_B_power",
    endpoint_b_power,
    "==",
    Rational(3, 1),
    "raising B^2 to 3/2 forces B^3"
  ),
  exact_check(
    "endpoint_forced_R_power",
    endpoint_r_power,
    "==",
    Rational(3, 1),
    "raising R^2 to 3/2 forces R^3"
  ),
  exact_check(
    "endpoint_forced_K_power",
    endpoint_k_power,
    "==",
    Rational(-3, 2),
    "the hypothetical endpoint constant forces the factor K^-3/2"
  ),
  exact_check(
    "eventual_b_lower_is_below_limit",
    b_lower,
    "<",
    b_limit,
    "1/256 is strictly below the limit 1/128"
  ),
  exact_check(
    "eventual_b_upper_is_above_limit",
    b_limit,
    "<",
    b_upper,
    "1/128 is strictly below the convenient upper bound 1/64"
  )
]

passed = checks.count { |item| item.fetch("pass") }
expected_payload = {
  "analytic_boundary" => [
    "does not prove or justify the local energy inequality or the moving-test limit",
    "does not prove existence, uniqueness, confinement, or any estimate for the mollified path",
    "does not prove the fixed-cylinder interpolation inequality",
    "does not prove or invoke the velocity-only epsilon-regularity criterion",
    "does not prove the R0.74F-H packet construction or any packet upper or lower bound",
    "does not verify the literature boundary, novelty, or priority",
    "does not prove regularity, singularity exclusion, continuation, or global smoothness",
    "does not solve the Clay Millennium problem"
  ],
  "checks" => checks,
  "exact_implications" => [
    "The Navier-Stokes rescaling gives integral_(Q1)|U|^3 = r^-2 integral_(Qr)|u|^3 at the exponent level.",
    "From E^(3/2)<=P, the inverse exponent is 2/3; choosing P<=epsilon_tube^(3/2) is exponent-compatible with E<=epsilon_tube.",
    "For rho=1/320, the logarithmic window is [2 rho,3 rho] and the consecutive-index lower-minus-upper exponent is 5 rho=1/64.",
    "The payment upper scale to the 2/3 power supplies B^2 R^2, while sqrt(log P) supplies the missing L power.",
    "Writing gamma=1/2-delta makes the subcritical exponent gap exactly delta; the endpoint gap is zero.",
    "A hypothetical endpoint upper bound forces P to have powers B^3 R^3 and K^-3/2 after L cancellation."
  ],
  "result" => passed == checks.length ? "PASS" : "FAIL",
  "summary" => { "passed" => passed, "total" => checks.length }
}

# The frozen artifact is opened only after all independent arithmetic and all
# expected text fields have been constructed.
frozen_payload = JSON.parse(File.read(CERTIFICATE_PATH))
expected_leaves = flatten_leaves(expected_payload)
frozen_leaves = flatten_leaves(frozen_payload)
paths = (expected_leaves.keys | frozen_leaves.keys).sort
mismatches = []
paths.each do |path|
  expected = expected_leaves[path]
  actual = frozen_leaves[path]
  next if expected == actual &&
          expected_leaves.key?(path) == frozen_leaves.key?(path)

  mismatches << {
    "path" => path,
    "expected" => expected,
    "actual" => actual,
    "expected_present" => expected_leaves.key?(path),
    "actual_present" => frozen_leaves.key?(path)
  }
end

audit_pass = mismatches.empty? && passed == checks.length
output = {
  "certificate" => CERTIFICATE_PATH,
  "engine" => "Ruby Rational independent reconstruction",
  "frozen_json_used_as_arithmetic_input" => false,
  "independent_summary" => { "passed" => passed, "total" => checks.length },
  "leaf_field_comparisons" => paths.length,
  "mismatch_count" => mismatches.length,
  "mismatches" => mismatches,
  "result" => audit_pass ? "PASS" : "FAIL"
}

puts JSON.pretty_generate(output)
exit(audit_pass ? 0 : 1)
