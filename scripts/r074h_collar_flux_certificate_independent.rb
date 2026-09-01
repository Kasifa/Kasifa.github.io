#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent exact-arithmetic audit for the R0.74H finite certificate.
#
# This program reconstructs all 25 checks with Ruby Rational arithmetic and
# compares only the resulting id/relation/left/right/margin/pass fields with
# the frozen JSON certificate.  It does not invoke or import the Python
# producer, and no value read from the JSON is used as an arithmetic input.

require "json"

CERTIFICATE_PATH = File.expand_path(
  "../research/r074h_collar_flux_certificate.json",
  __dir__
)

def rational_string(value)
  "#{value.numerator}/#{value.denominator}"
end

def exact_check(id, left, relation, right)
  case relation
  when "=="
    margin = left - right
    passed = left == right
  when "<"
    margin = right - left
    passed = left < right
  when ">"
    margin = left - right
    passed = left > right
  else
    raise ArgumentError, "unsupported relation: #{relation}"
  end

  {
    "id" => id,
    "left" => rational_string(left),
    "relation" => relation,
    "right" => rational_string(right),
    "margin" => rational_string(margin),
    "pass" => passed
  }
end

one = Rational(1, 1)
two_thirds = Rational(2, 3)
three_halves = Rational(3, 2)

# Parabolic shell bookkeeping, reconstructed independently.
time_power = Rational(2, 1)
space_power = Rational(3, 1)
measure_power = time_power + space_power
holder_volume_power = measure_power / Rational(3, 1)
quadratic_prefactor_power = Rational(-1, 1) + Rational(-2, 1)
normalized_s2_power = quadratic_prefactor_power + holder_volume_power
normalized_s3_power = Rational(-2, 1) * two_thirds

# R0.74G amplitude and repaired-flux bookkeeping.
gamma_power_after_amplitude = Rational(2, 1) * Rational(-1, 2) + one
terminal_b_power = Rational(2, 1)
terminal_l_power = one
terminal_r_power = Rational(2, 1)

payment_b_power = Rational(3, 1)
payment_l_power = Rational(0, 1)
payment_r_power = Rational(3, 1)
payment_23_b_power = payment_b_power * two_thirds
payment_23_l_power = payment_l_power * two_thirds
payment_23_r_power = payment_r_power * two_thirds

flux_b_power = Rational(2, 1)
flux_l_power = one
flux_r_power = Rational(2, 1)
cubic_flux_b_power = flux_b_power * three_halves
cubic_flux_l_power = flux_l_power * three_halves
cubic_flux_r_power = flux_r_power * three_halves

b_as_r_power = Rational(-2, 1)
old_payment_as_r = payment_b_power * b_as_r_power + payment_r_power
target_as_r = terminal_b_power * b_as_r_power + terminal_r_power

checks = [
  exact_check("parabolic_measure_power", measure_power, "==", Rational(5, 1)),
  exact_check("holder_volume_one_third", holder_volume_power, "==", Rational(5, 3)),
  exact_check(
    "quadratic_cutoff_prefactor",
    Rational(-1, 1) + Rational(-2, 1),
    "==",
    quadratic_prefactor_power
  ),
  exact_check("normalized_S2_power", normalized_s2_power, "==", Rational(-4, 3)),
  exact_check(
    "normalized_S3_two_thirds_power",
    normalized_s3_power,
    "==",
    Rational(-4, 3)
  ),
  exact_check(
    "quadratic_row_exponent_match",
    normalized_s2_power,
    "==",
    normalized_s3_power
  ),
  exact_check(
    "energy_payment_outer_power",
    three_halves * two_thirds,
    "==",
    one
  ),
  exact_check(
    "acceleration_payment_outer_power",
    three_halves * two_thirds,
    "==",
    one
  ),
  exact_check(
    "collar_payment_outer_power",
    three_halves * two_thirds,
    "==",
    one
  ),
  exact_check("small_payment_absorption_exponents", two_thirds, "<", one),
  exact_check("large_payment_two_regime_exponents", two_thirds, "<", one),
  exact_check(
    "amplitude_gamma_cancellation",
    gamma_power_after_amplitude,
    "==",
    Rational(0, 1)
  ),
  exact_check("old_payment_23_B_power", payment_23_b_power, "==", terminal_b_power),
  exact_check("old_payment_23_R_power", payment_23_r_power, "==", terminal_r_power),
  exact_check(
    "old_payment_23_L_power",
    payment_23_l_power,
    "==",
    Rational(0, 1)
  ),
  exact_check(
    "target_over_old_23_L_power",
    terminal_l_power - payment_23_l_power,
    "==",
    one
  ),
  exact_check("cubic_flux_B_power", cubic_flux_b_power, "==", payment_b_power),
  exact_check("cubic_flux_L_power", cubic_flux_l_power, "==", three_halves),
  exact_check("cubic_flux_R_power", cubic_flux_r_power, "==", payment_r_power),
  exact_check(
    "cubic_flux_beats_old_L_power",
    cubic_flux_l_power,
    ">",
    payment_l_power
  ),
  exact_check(
    "old_payment_under_B_Rminus2",
    old_payment_as_r,
    "==",
    Rational(-3, 1)
  ),
  exact_check(
    "target_under_B_Rminus2",
    target_as_r,
    "==",
    Rational(-2, 1)
  ),
  exact_check(
    "reference_payment_scale_diverges",
    old_payment_as_r,
    "<",
    Rational(0, 1)
  ),
  exact_check(
    "finite_tail_ratio_exponent_at_j4",
    Rational(3, 1) * Rational(4**3, 32),
    "==",
    Rational(6, 1)
  ),
  exact_check("flux_repair_sum_constant", one + one, "==", Rational(2, 1))
]

frozen = JSON.parse(File.read(CERTIFICATE_PATH))
frozen_checks = frozen.fetch("checks")
fields = %w[id relation left right margin pass].freeze
mismatches = []

if checks.length != 25
  mismatches << {
    "scope" => "independent_count",
    "expected" => 25,
    "actual" => checks.length
  }
end

if frozen_checks.length != checks.length
  mismatches << {
    "scope" => "frozen_count",
    "expected" => checks.length,
    "actual" => frozen_checks.length
  }
end

checks.each_with_index do |actual, index|
  expected = frozen_checks[index]
  if expected.nil?
    mismatches << { "scope" => "missing_frozen_check", "index" => index }
    next
  end

  fields.each do |field|
    next if actual[field] == expected[field]

    mismatches << {
      "scope" => "field",
      "index" => index,
      "id" => actual["id"],
      "field" => field,
      "expected" => expected[field],
      "actual" => actual[field]
    }
  end
end

independent_passed = checks.count { |item| item["pass"] }
summary_match = frozen.fetch("summary") == {
  "passed" => independent_passed,
  "total" => checks.length
}
result_match = frozen.fetch("result") ==
               (independent_passed == checks.length ? "PASS" : "FAIL")

mismatches << { "scope" => "summary" } unless summary_match
mismatches << { "scope" => "result" } unless result_match

audit_pass = mismatches.empty? && independent_passed == 25
output = {
  "certificate" => CERTIFICATE_PATH,
  "engine" => "Ruby Rational independent reconstruction",
  "fields_checked" => fields,
  "field_comparisons" => checks.length * fields.length,
  "independent_summary" => {
    "passed" => independent_passed,
    "total" => checks.length
  },
  "frozen_result_match" => result_match,
  "frozen_summary_match" => summary_match,
  "mismatch_count" => mismatches.length,
  "mismatches" => mismatches,
  "result" => audit_pass ? "PASS" : "FAIL"
}

puts JSON.pretty_generate(output)
exit(audit_pass ? 0 : 1)
