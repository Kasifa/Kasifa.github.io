#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent exact-arithmetic reconstruction for the R0.74L main-collar
# certificate.  This implementation uses only Ruby's Rational arithmetic and
# the formulas stated in the analytic note; it does not call the primary
# certificate generator.

require "digest"
require "json"

EXPECTED_CERTIFICATE_SHA256 =
  "252808d60f90343e3a9d614f0ae11003984498d2362e05f9441d53175bcafd7e"

EXPECTED_BOUNDARY = [
  "does not prove the normalized-bridge reversal identity",
  "does not prove reflection-principle or stopping-time claims",
  "does not prove the thickened-slice BV geometry",
  "does not prove the short-clock occupation lemma",
  "does not treat the nearest inward collar or the full signed packet condition",
  "does not prove a universal endpoint estimate, regularity, singularity, or Clay"
].freeze

EXPECTED_STATUS = {
  "clay_problem" => "NOT_CLAIMED",
  "finite_arithmetic" => "PASS",
  "main_collar_analytic_proof" => "REQUIRES_INDEPENDENT_AUDIT",
  "nearest_inward_collar" => "OUTSIDE_R074L_FREEZE"
}.freeze

def parse_fraction(value)
  match = /\A(-?\d+)\/([1-9]\d*)\z/.match(value.to_s)
  raise ArgumentError, "invalid fraction #{value.inspect}" unless match

  Rational(Integer(match[1], 10), Integer(match[2], 10))
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
  when "==" then left - right
  when ">", ">=" then left - right
  when "<", "<=" then right - left
  else
    raise ArgumentError, "unsupported relation #{relation.inspect}"
  end
end

certificate_path = if ARGV.empty?
                     File.expand_path(
                       "../research/r074l_main_collar_certificate.json",
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

# Freeze the primitive data before deriving anything.  These are the five
# mathematical inputs named by the certificate, not values copied from its
# derived/check sections.
lambda_scale = Rational(63, 32)
center_height = Rational(15, 16)
radius_exponent = Rational(1, 320)
index_threshold = 14
b_r2_lower = Rational(1, 128)
b_r2_upper = Rational(1, 64)

inputs = certificate.fetch("inputs")
record.call(parse_fraction(inputs.fetch("lambda")) == lambda_scale,
            "inputs.lambda does not equal 63/32")
record.call(parse_fraction(inputs.fetch("c_h")) == center_height,
            "inputs.c_h does not equal 15/16")
record.call(parse_fraction(inputs.fetch("rho")) == radius_exponent,
            "inputs.rho does not equal 1/320")
record.call(inputs.fetch("j_threshold") == index_threshold,
            "inputs.j_threshold does not equal 14")
record.call(inputs.fetch("B_R2_interval").map { |x| parse_fraction(x) } ==
            [b_r2_lower, b_r2_upper],
            "inputs.B_R2_interval does not equal [1/128, 1/64]")

# Independent reconstruction from the displayed formulas.
l14 = lambda_scale * (2**index_threshold)
distance_threshold = Rational(64 * 256, 1) / center_height

distance_reserve = Rational(255, 256)
reflection_time_denominator = 4 * 66
bad_exponent =
  distance_reserve**2 * center_height**2 / reflection_time_denominator
bad_exponent_reserve = bad_exponent - radius_exponent

heat_tail_argument = Rational(32**2, 4 * 65)
taylor4 = (0..4).inject(Rational(0, 1)) do |sum, degree|
  factorial = (1..degree).inject(1) { |product, n| product * n }
  sum + heat_tail_argument**degree / factorial
end

clock_length_upper = 65 * b_r2_upper

# Outer radius 2^(j+1)R equals (2/lambda)LR.  The R/8 padding is at most
# LR/63 once L >= 63/8.
outer_radius_coefficient = Rational(2, 1) / lambda_scale
padding_coefficient = Rational(1, 63)
projection_radius_coefficient =
  outer_radius_coefficient + padding_coefficient
component_length_coefficient = 2 * projection_radius_coefficient

# dt <= (4/3)dq/B and B^(-1) <= 128R^2.
inverse_b_coefficient = Rational(1, 1) / b_r2_lower
physical_duration_coefficient =
  Rational(4, 3) * component_length_coefficient * inverse_b_coefficient

# For generator d^2/dx^2, the reflection/Gaussian exponent at displacement
# R/16 over the duration above is (R/16)^2/(4 Delta t).
modulus_exponent_coefficient =
  Rational(1, 16**2 * 4) / physical_duration_coefficient

# Scale ledgers.  Each pair is [power of L, power of R].
good_scale = [
  [0, 6],  # outer R^6
  [0, 2],  # B^(-1) <= 128 R^2
  [0, -1], # heat-kernel endpoint weight
  [0, -3], # integral of H_R
  [1, 1]   # clock occupation bound CLR
].transpose.map(&:sum)

bad_scale = [
  [0, 6],  # outer R^6
  [0, -1], # heat-kernel endpoint weight
  [1, 0],  # pointwise collar bound CL
  [0, -3], # derivative heat-kernel square
  [0, 2],  # physical time window
  [0, 1]   # bad-event probability <= 4R
].transpose.map(&:sum)

expected_checks = [
  ["lambda", lambda_scale, "==", lambda_scale],
  ["center_height", center_height, "==", center_height],
  ["radius_exponent", radius_exponent, "==", radius_exponent],
  ["L14", l14, "==", Rational(32_256, 1)],
  ["L14_beats_distance_threshold", l14, ">=", distance_threshold],
  ["bad_exponent_A", bad_exponent, "==", Rational(4_876_875, 1_476_395_008)],
  ["bad_exponent_reserve", bad_exponent_reserve, "==",
   Rational(1_315_703, 7_381_975_040)],
  ["bad_exponent_reserve_positive", bad_exponent_reserve, ">", Rational(0, 1)],
  ["heat_tail_argument", heat_tail_argument, "==", Rational(256, 65)],
  ["taylor4", taylor4, "==", Rational(587_309_569, 17_850_625)],
  ["taylor4_beats_32", taylor4, ">", Rational(32, 1)],
  ["B_R2_lower", b_r2_lower, "==", Rational(1, 128)],
  ["B_R2_upper", b_r2_upper, "==", Rational(1, 64)],
  ["clock_length_upper", clock_length_upper, "==", Rational(65, 64)],
  ["clock_length_below_two", clock_length_upper, "<", Rational(2, 1)],
  ["projection_radius", projection_radius_coefficient, "==", Rational(65, 63)],
  ["component_length_coefficient", component_length_coefficient, "==",
   Rational(130, 63)],
  ["physical_duration_coefficient", physical_duration_coefficient, "==",
   Rational(66_560, 189)],
  ["modulus_exponent_coefficient", modulus_exponent_coefficient, "==",
   Rational(189, 68_157_440)],
  ["modulus_exponent_positive", modulus_exponent_coefficient, ">", Rational(0, 1)],
  ["good_R_power", Rational(good_scale.fetch(1), 1), "==", Rational(5, 1)],
  ["good_L_power", Rational(good_scale.fetch(0), 1), "==", Rational(1, 1)],
  ["bad_R_power", Rational(bad_scale.fetch(1), 1), "==", Rational(5, 1)],
  ["bad_L_power", Rational(bad_scale.fetch(0), 1), "==", Rational(1, 1)]
].freeze

checks = certificate.fetch("checks")
record.call(checks.length == expected_checks.length,
            "certificate has #{checks.length} checks; expected #{expected_checks.length}")

ids = checks.map { |entry| entry.fetch("id") }
expected_ids = expected_checks.map(&:first)
record.call(ids.uniq.length == ids.length, "certificate contains duplicate check ids")
record.call(ids == expected_ids,
            "check ids or ordering differ from the independent inventory")

rows = []
expected_checks.each do |id, expected_left, expected_relation, expected_right|
  entry = checks.find { |candidate| candidate.fetch("id") == id }
  if entry.nil?
    failures << "#{id}: missing check"
    next
  end

  begin
    actual_left = parse_fraction(entry.fetch("left"))
    actual_right = parse_fraction(entry.fetch("right"))
    actual_margin = parse_fraction(entry.fetch("margin"))
    actual_relation = entry.fetch("relation")
    actual_pass = entry.fetch("pass")
    expected_margin = signed_margin(expected_left, expected_relation, expected_right)
    evaluated_pass = relation_holds?(actual_left, actual_relation, actual_right)

    row_failures = []
    row_failures << "left" unless actual_left == expected_left
    row_failures << "relation" unless actual_relation == expected_relation
    row_failures << "right" unless actual_right == expected_right
    row_failures << "margin" unless actual_margin == expected_margin
    row_failures << "pass" unless actual_pass == evaluated_pass && actual_pass == true
    row_failures << "note" unless entry.fetch("note").is_a?(String) &&
                                         !entry.fetch("note").strip.empty?

    failures << "#{id}: mismatched #{row_failures.join(', ')}" unless row_failures.empty?
    rows << [id, expected_left, expected_relation, expected_right,
             expected_margin, row_failures.empty?]
  rescue KeyError, ArgumentError => e
    failures << "#{id}: #{e.message}"
  end
end

expected_derived = {
  "L14" => l14,
  "bad_exponent_A" => bad_exponent,
  "bad_exponent_reserve" => bad_exponent_reserve,
  "clock_length_upper" => clock_length_upper,
  "distance_threshold" => distance_threshold,
  "modulus_exponent_coefficient" => modulus_exponent_coefficient,
  "physical_duration_coefficient" => physical_duration_coefficient,
  "projection_radius_coefficient" => projection_radius_coefficient,
  "taylor4_at_256_over_65" => taylor4
}.freeze

derived = certificate.fetch("derived")
record.call(derived.keys.sort == expected_derived.keys.sort,
            "derived-field inventory differs from the independent inventory")
expected_derived.each do |key, expected_value|
  actual_value = parse_fraction(derived.fetch(key))
  record.call(actual_value == expected_value,
              "derived.#{key}=#{fraction_string(actual_value)}; " \
              "expected #{fraction_string(expected_value)}")
end

record.call(certificate.fetch("schema") == "r074l-main-collar-certificate-v1",
            "unexpected certificate schema")
record.call(certificate.fetch("scope") ==
            "finite exact rational constants, thresholds, and scale ledger only",
            "certificate scope is not the frozen finite-arithmetic scope")
record.call(certificate.fetch("analytic_boundary") == EXPECTED_BOUNDARY,
            "analytic boundary differs from the strict six-item boundary")
record.call(certificate.fetch("status_flags") == EXPECTED_STATUS,
            "status flags differ from the frozen non-analytic boundary")

summary = certificate.fetch("summary")
record.call(summary.fetch("total") == expected_checks.length,
            "summary.total does not equal #{expected_checks.length}")
record.call(summary.fetch("passed") == expected_checks.length,
            "summary.passed does not equal #{expected_checks.length}")
record.call(certificate.fetch("result") == "PASS",
            "certificate.result is not PASS")
record.call(certificate_sha256 == EXPECTED_CERTIFICATE_SHA256,
            "certificate SHA-256 #{certificate_sha256} does not match " \
            "#{EXPECTED_CERTIFICATE_SHA256}")

puts "R0.74L independent exact-arithmetic reconstruction"
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
  puts "ANALYTIC BOUNDARY: finite arithmetic only; no analytic lemma is certified."
  exit 0
end

puts "RESULT: FAIL (#{failures.length} discrepancy/discrepancies)"
failures.each { |failure| puts "- #{failure}" }
exit 1
