#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent exact-arithmetic reconstruction of the R0.74M nearest-inward
# finite certificate.  This program uses Ruby Rational arithmetic and the
# constants/formulas in the analytic note.  It does not invoke or import the
# Python certificate generator, and it never accepts values from the JSON
# derived/check sections as inputs to its reconstruction.

require "digest"
require "json"

EXPECTED_CERTIFICATE_SHA256 =
  "5aed76e6c2aac58c1507784dd014a132560967a1bb89e69080fa0e170f65462f"

EXPECTED_TOP_LEVEL_KEYS = %w[
  analytic_boundary checks derived inputs result schema scope status_flags
  summary
].sort.freeze

EXPECTED_INPUT_KEYS = %w[
  G1 L_analytic_threshold c_def c_h j_threshold lambda plateau_a rho
].sort.freeze

EXPECTED_BOUNDARY = [
  "does not prove the normalized bridge or common-forward-law identity",
  "does not prove the Brownian reflection estimate",
  "does not prove heat-kernel positivity or the periodic Gaussian tail",
  "does not prove the support-conditioned displacement lemma",
  "does not synthesize every shell row or prove the full R0.74K condition",
  "does not prove a universal endpoint estimate, regularity, singularity, or Clay"
].freeze

EXPECTED_STATUS = {
  "clay_problem" => "NOT_CLAIMED",
  "finite_arithmetic" => "PASS",
  "full_signed_collar_condition" => "OPEN",
  "nearest_inward_analytic_proof" => "REQUIRES_INDEPENDENT_AUDIT"
}.freeze

def parse_fraction(value)
  match = /\A(-?\d+)\/([1-9]\d*)\z/.match(value.to_s)
  raise ArgumentError, "invalid reduced fraction #{value.inspect}" unless match

  numerator = Integer(match[1], 10)
  denominator = Integer(match[2], 10)
  rational = Rational(numerator, denominator)
  unless value == "#{rational.numerator}/#{rational.denominator}"
    raise ArgumentError, "noncanonical fraction #{value.inspect}"
  end
  rational
end

def fraction_string(value)
  "#{value.numerator}/#{value.denominator}"
end

def relation_holds?(left, relation, right)
  case relation
  when "==" then left == right
  when ">"  then left > right
  when ">=" then left >= right
  when "<"  then left < right
  when "<=" then left <= right
  else
    raise ArgumentError, "unsupported relation #{relation.inspect}"
  end
end

def signed_margin(left, relation, right)
  case relation
  when "==", ">", ">=" then left - right
  when "<", "<=" then right - left
  else
    raise ArgumentError, "unsupported relation #{relation.inspect}"
  end
end

def expected_row(id, left, relation, right, note)
  {
    "id" => id,
    "left" => left,
    "relation" => relation,
    "right" => right,
    "margin" => signed_margin(left, relation, right),
    "pass" => relation_holds?(left, relation, right),
    "note" => note
  }
end

certificate_path = if ARGV.empty?
                     File.expand_path(
                       "../research/r074m_nearest_inward_certificate.json",
                       __dir__
                     )
                   elsif ARGV.length == 1
                     File.expand_path(ARGV.fetch(0))
                   else
                     warn "usage: ruby #{File.basename(__FILE__)} [certificate.json]"
                     exit 2
                   end

raw = File.binread(certificate_path)
certificate_sha256 = Digest::SHA256.hexdigest(raw)
certificate = JSON.parse(raw)
failures = []

record = lambda do |condition, message|
  failures << message unless condition
end

record.call(certificate.keys.sort == EXPECTED_TOP_LEVEL_KEYS,
            "top-level field inventory differs from the v1 schema")

# Freeze primitive mathematical inputs before any derived quantity is formed.
# Every rational below is reconstructed natively by Ruby.
lambda_scale = Rational(63, 32)
center_height = Rational(15, 16)
radius_exponent = Rational(1, 320)
weight_gap = Rational(2, 1323)
defect_exponent = Rational(1, 640)
plateau_exponent = Rational(49, 14_625)
index_threshold = 13
analytic_threshold = Rational(9216, 1)

inputs = certificate.fetch("inputs")
record.call(inputs.keys.sort == EXPECTED_INPUT_KEYS,
            "input-field inventory differs from the v1 schema")
record.call(parse_fraction(inputs.fetch("lambda")) == lambda_scale,
            "inputs.lambda does not equal 63/32")
record.call(parse_fraction(inputs.fetch("c_h")) == center_height,
            "inputs.c_h does not equal 15/16")
record.call(parse_fraction(inputs.fetch("rho")) == radius_exponent,
            "inputs.rho does not equal 1/320")
record.call(parse_fraction(inputs.fetch("G1")) == weight_gap,
            "inputs.G1 does not equal 2/1323")
record.call(parse_fraction(inputs.fetch("c_def")) == defect_exponent,
            "inputs.c_def does not equal 1/640")
record.call(parse_fraction(inputs.fetch("plateau_a")) == plateau_exponent,
            "inputs.plateau_a does not equal 49/14625")
record.call(inputs.fetch("j_threshold") == index_threshold,
            "inputs.j_threshold does not equal 13")
record.call(parse_fraction(inputs.fetch("L_analytic_threshold")) ==
            analytic_threshold,
            "inputs.L_analytic_threshold does not equal 9216")

zero = Rational(0, 1)

# Discrete scale and final-segment geometry.
l13 = lambda_scale * (2**index_threshold)
outer_coefficient = Rational(1, 1) / lambda_scale
modulus_coefficient = Rational(1, 16)
defect_window_coefficient = Rational(3, 5)
geometry_gap =
  defect_window_coefficient - outer_coefficient - modulus_coefficient

final_segment_length = Rational(1, 64)
reflection_exponent =
  modulus_coefficient**2 / (4 * final_segment_length)

# The retained central heat-kernel copy is evaluated at times at least
# (61-1/64)R^2 and at distance at most (3L/5+64)R.
heat_time_lower = Rational(61, 1) - final_segment_length
heat_exponent_multiplier = Rational(1, 1) / (4 * heat_time_lower)
heat_linear = defect_window_coefficient
heat_offset = Rational(64, 1)
heat_margin_quadratic =
  defect_exponent - heat_exponent_multiplier * heat_linear**2
heat_margin_linear =
  2 * heat_exponent_multiplier * heat_linear * heat_offset
heat_margin_constant = heat_exponent_multiplier * heat_offset**2
heat_margin_at_l0 =
  heat_margin_quadratic * analytic_threshold**2 -
  heat_margin_linear * analytic_threshold - heat_margin_constant
heat_margin_derivative_at_l0 =
  2 * heat_margin_quadratic * analytic_threshold - heat_margin_linear

# Positive-displacement payments.
plateau_gap = plateau_exponent - defect_exponent
expulsion_gap = radius_exponent - defect_exponent

b_r2_lower = Rational(1, 128)
b_r2_upper = Rational(1, 64)
time_upper = Rational(65, 1)
plateau_negative_coefficient = 4 * time_upper * b_r2_upper

# The final positive contribution is
# (1/2)*(BR^2 lower)*(final segment length) = 1/16384.
# Reserving half of it after absorbing the plateau error gives 1/32768.
sigma_denominator = Rational(2, 1) /
                    (Rational(1, 2) * b_r2_lower * final_segment_length)
negative_absorption_required =
  plateau_negative_coefficient * sigma_denominator
plateau_gap_at_l0 = plateau_gap * analytic_threshold**2
plateau_exp_lower = plateau_gap_at_l0**2 / 2

# For L>=63/8, the R/8 padding contributes at most (1/63)LR.
radius_coefficient_upper =
  outer_coefficient + Rational(1, 63)
four_radius_coefficient = 4 * radius_coefficient_upper
expulsion_at_l0 = defect_exponent * analytic_threshold**2
expulsion_exp_lower = expulsion_at_l0**2 / 2
expulsion_radius_required =
  sigma_denominator * four_radius_coefficient * analytic_threshold

bad_event_gap =
  reflection_exponent - radius_exponent - weight_gap
super_rate = 2 * expulsion_gap
sigma_square_prefactor_denominator = sigma_denominator**2

# Raw scale ledgers, before the bad event supplies one extra R and the good
# Gaussian tail supplies R^2.  Pairs are [L power, R power].
bad_scale = [
  [0, 6],  # outer R^6
  [0, 2],  # time interval
  [0, -1], # endpoint heat kernel
  [1, 0],  # collar slice
  [0, -3]  # derivative-kernel L2 integral
].transpose.map(&:sum)

good_scale = [
  [0, 6],  # outer R^6
  [0, 2],  # time interval
  [0, -1], # endpoint heat kernel
  [1, 0],  # collar slice
  [0, -4]  # derivative-kernel tail
].transpose.map(&:sum)

expected_checks = [
  expected_row("lambda", lambda_scale, "==", Rational(63, 32),
               "frozen dyadic scale"),
  expected_row("center_height", center_height, "==", Rational(15, 16),
               "frozen packet height"),
  expected_row("radius_exponent", radius_exponent, "==", Rational(1, 320),
               "R=exp(-rho L^2)"),
  expected_row("weight_gap_G1", weight_gap, "==", Rational(2, 1323),
               "Gamma_(j-1)/Gamma_j exponent"),
  expected_row("L13", l13, "==", Rational(16_128, 1),
               "first inherited discrete index"),
  expected_row("L13_beats_heat_threshold", l13, ">=", analytic_threshold,
               "actual family index exceeds L>=9216"),
  expected_row("outer_coefficient", outer_coefficient, "==", Rational(32, 63),
               "j-1 padded outer radius before R/8"),
  expected_row("geometry_gap", geometry_gap, "==", Rational(149, 5040),
               "room below the 3L/5 defect window"),
  expected_row("geometry_gap_positive", geometry_gap, ">", zero,
               "final segment remains in the defect window"),
  expected_row("final_segment_length", final_segment_length, "==", Rational(1, 64),
               "physical final segment length in R^2 units"),
  expected_row("reflection_exponent", reflection_exponent, "==", Rational(1, 16),
               "LR/16 Brownian modulus exponent"),
  expected_row("heat_time_lower", heat_time_lower, "==", Rational(3903, 64),
               "61-1/64"),
  expected_row("heat_exponent_multiplier", heat_exponent_multiplier, "==",
               Rational(16, 3903),
               "reciprocal of four times the lower heat time"),
  expected_row("heat_margin_quadratic", heat_margin_quadratic, "==",
               Rational(361, 4_163_200),
               "positive L^2 coefficient in the defect comparison"),
  expected_row("heat_margin_linear", heat_margin_linear, "==",
               Rational(2048, 6505),
               "linear cost in the defect comparison"),
  expected_row("heat_margin_constant", heat_margin_constant, "==",
               Rational(65_536, 3903),
               "constant cost in the defect comparison"),
  expected_row("heat_margin_at_L0", heat_margin_at_l0, "==",
               Rational(433_872_896, 97_575),
               "defect exponent margin at L=9216"),
  expected_row("heat_margin_at_L0_positive", heat_margin_at_l0, ">", zero,
               "defect exponent holds at the base threshold"),
  expected_row("heat_margin_derivative_at_L0", heat_margin_derivative_at_l0,
               "==", Rational(41_744, 32_525),
               "margin is increasing after L=9216"),
  expected_row("heat_margin_derivative_positive", heat_margin_derivative_at_l0,
               ">", zero, "monotone threshold propagation"),
  expected_row("plateau_gap", plateau_gap, "==",
               Rational(3347, 1_872_000),
               "plateau defect decays faster than the inward defect"),
  expected_row("plateau_gap_positive", plateau_gap, ">", zero,
               "positive displacement survives subtraction"),
  expected_row("expulsion_gap", expulsion_gap, "==", Rational(1, 640),
               "expulsion scale is larger than LR"),
  expected_row("expulsion_gap_positive", expulsion_gap, ">", zero,
               "Sigma/(LR) diverges"),
  expected_row("negative_absorption_required", negative_absorption_required,
               "==", Rational(133_120, 1),
               "exponential factor needed to absorb the global negative term"),
  expected_row("plateau_exp_lower", plateau_exp_lower, ">",
               negative_absorption_required,
               "e^z >= z^2/2 pays the negative term at L=9216"),
  expected_row("radius_coefficient_upper", radius_coefficient_upper, "==",
               Rational(11, 21), "padded inward radius divided by LR"),
  expected_row("four_radius_coefficient", four_radius_coefficient, "==",
               Rational(44, 21), "coefficient required for Sigma>=4r_-"),
  expected_row("expulsion_exp_lower", expulsion_exp_lower, ">",
               expulsion_radius_required,
               "e^x >= x^2/2 makes Sigma>=4r_- at L=9216"),
  expected_row("bad_event_gap", bad_event_gap, "==",
               Rational(24_497, 423_360),
               "fast-return rarity pays R and the weight gap"),
  expected_row("bad_event_gap_positive", bad_event_gap, ">", zero,
               "bad path exponent has strict reserve"),
  expected_row("super_rate", super_rate, "==", Rational(1, 320),
               "Sigma^2/R^2 has exp(L^2/320) growth"),
  expected_row("super_rate_positive", super_rate, ">", zero,
               "good-path heat tail is super-Gaussian in L"),
  expected_row("sigma_square_denominator", sigma_square_prefactor_denominator,
               "==", Rational(1_073_741_824, 1),
               "32768^2 exact prefactor denominator"),
  expected_row("bad_R_power", Rational(bad_scale.fetch(1), 1), "==",
               Rational(4, 1),
               "raw bad-path ledger before its extra R payment"),
  expected_row("bad_L_power", Rational(bad_scale.fetch(0), 1), "==",
               Rational(1, 1), "bad-path L power"),
  expected_row("good_R_power", Rational(good_scale.fetch(1), 1), "==",
               Rational(3, 1),
               "raw good-path ledger before its R^2 tail payment"),
  expected_row("good_L_power", Rational(good_scale.fetch(0), 1), "==",
               Rational(1, 1), "good-path L power")
].freeze

checks = certificate.fetch("checks")
record.call(checks.length == expected_checks.length,
            "certificate has #{checks.length} checks; expected " \
            "#{expected_checks.length}")

actual_ids = checks.map { |entry| entry.fetch("id") }
expected_ids = expected_checks.map { |entry| entry.fetch("id") }
record.call(actual_ids.uniq.length == actual_ids.length,
            "certificate contains duplicate check ids")
record.call(actual_ids == expected_ids,
            "check ids or ordering differ from the independent inventory")

rows = []
expected_checks.each_with_index do |expected, index|
  entry = checks[index]
  if entry.nil?
    failures << "#{expected.fetch('id')}: missing check"
    next
  end

  begin
    actual_left = parse_fraction(entry.fetch("left"))
    actual_right = parse_fraction(entry.fetch("right"))
    actual_margin = parse_fraction(entry.fetch("margin"))
    actual_relation = entry.fetch("relation")
    actual_pass = entry.fetch("pass")
    evaluated_pass = relation_holds?(actual_left, actual_relation, actual_right)

    row_failures = []
    row_failures << "field inventory" unless entry.keys.sort ==
                                                   expected.keys.sort
    row_failures << "id" unless entry.fetch("id") == expected.fetch("id")
    row_failures << "left" unless actual_left == expected.fetch("left")
    row_failures << "relation" unless actual_relation ==
                                            expected.fetch("relation")
    row_failures << "right" unless actual_right == expected.fetch("right")
    row_failures << "margin" unless actual_margin == expected.fetch("margin")
    row_failures << "pass" unless actual_pass == evaluated_pass &&
                                       actual_pass == expected.fetch("pass") &&
                                       actual_pass == true
    row_failures << "note" unless entry.fetch("note") == expected.fetch("note")

    unless row_failures.empty?
      failures << "#{expected.fetch('id')}: mismatched " \
                  "#{row_failures.join(', ')}"
    end
    rows << [expected.fetch("id"), expected.fetch("left"),
             expected.fetch("relation"), expected.fetch("right"),
             expected.fetch("margin"), row_failures.empty?]
  rescue KeyError, ArgumentError => e
    failures << "#{expected.fetch('id')}: #{e.message}"
  end
end

expected_derived = {
  "L13" => fraction_string(l13),
  "bad_event_gap" => fraction_string(bad_event_gap),
  "bad_scale" => "L^#{fraction_string(Rational(bad_scale.fetch(0), 1))} " \
                 "R^#{fraction_string(Rational(bad_scale.fetch(1), 1))}",
  "expulsion_gap" => fraction_string(expulsion_gap),
  "geometry_gap" => fraction_string(geometry_gap),
  "good_scale" => "L^#{fraction_string(Rational(good_scale.fetch(0), 1))} " \
                  "R^#{fraction_string(Rational(good_scale.fetch(1), 1))}",
  "heat_margin_at_L0" => fraction_string(heat_margin_at_l0),
  "heat_margin_derivative_at_L0" =>
    fraction_string(heat_margin_derivative_at_l0),
  "plateau_gap" => fraction_string(plateau_gap),
  "reflection_exponent" => fraction_string(reflection_exponent),
  "super_rate" => fraction_string(super_rate)
}.freeze

derived = certificate.fetch("derived")
record.call(derived.keys.sort == expected_derived.keys.sort,
            "derived-field inventory differs from the independent inventory")
expected_derived.each do |key, expected_value|
  record.call(derived.fetch(key) == expected_value,
              "derived.#{key}=#{derived.fetch(key).inspect}; " \
              "expected #{expected_value.inspect}")
end

record.call(certificate.fetch("schema") ==
            "r074m-nearest-inward-certificate-v1",
            "unexpected certificate schema")
record.call(certificate.fetch("scope") ==
            "finite exact rational constants, monotone thresholds, and scale ledger only",
            "certificate scope is not the frozen finite-arithmetic scope")
record.call(certificate.fetch("analytic_boundary") == EXPECTED_BOUNDARY,
            "analytic boundary differs from the strict six-item boundary")
record.call(certificate.fetch("status_flags") == EXPECTED_STATUS,
            "status flags differ from the frozen non-analytic boundary")

summary = certificate.fetch("summary")
record.call(summary.keys.sort == %w[passed total],
            "summary field inventory differs from the v1 schema")
record.call(summary.fetch("total") == expected_checks.length,
            "summary.total does not equal #{expected_checks.length}")
record.call(summary.fetch("passed") == expected_checks.length,
            "summary.passed does not equal #{expected_checks.length}")
record.call(certificate.fetch("result") == "PASS",
            "certificate.result is not PASS")
record.call(certificate_sha256 == EXPECTED_CERTIFICATE_SHA256,
            "certificate SHA-256 #{certificate_sha256} does not match " \
            "#{EXPECTED_CERTIFICATE_SHA256}")

puts "R0.74M independent exact-arithmetic reconstruction"
puts "certificate: #{certificate_path}"
puts "certificate_sha256: #{certificate_sha256}"
puts ""
rows.each do |id, left, relation, right, margin, passed|
  label = passed ? "PASS" : "FAIL"
  puts format(
    "%-4s %-38s %s %s %s  margin=%s",
    label,
    id,
    fraction_string(left),
    relation,
    fraction_string(right),
    fraction_string(margin)
  )
end

puts ""
if failures.empty?
  puts "RESULT: PASS (#{rows.length}/#{expected_checks.length} checks)"
  puts "PASS #{rows.length}/#{expected_checks.length}"
  puts "ANALYTIC BOUNDARY: finite arithmetic only; no analytic lemma is certified."
  exit 0
end

puts "RESULT: FAIL (#{failures.length} discrepancy/discrepancies)"
failures.each { |failure| puts "- #{failure}" }
exit 1
