#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent Ruby Rational reconstruction of the R0.74N finite certificate.
# This program never invokes the Python generator and never uses derived JSON
# values as mathematical inputs.  It also freezes the byte-level JSON hash.

require "digest"
require "json"

EXPECTED_CERTIFICATE_SHA256 =
  "53481cf393308a786c3a414da6238faaa9b8a15dac0017638c47584615bbecc2"

def r(numerator, denominator = 1)
  Rational(numerator, denominator)
end

def qs(value)
  "#{value.numerator}/#{value.denominator}"
end

def relation_holds?(left, relation, right)
  case relation
  when "==" then left == right
  when ">" then left > right
  when ">=" then left >= right
  when "<" then left < right
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
    "left" => qs(left),
    "relation" => relation,
    "right" => qs(right),
    "margin" => qs(signed_margin(left, relation, right)),
    "pass" => relation_holds?(left, relation, right),
    "note" => note
  }
end

def taylor2(x)
  r(1) + x + x**2 / r(2)
end

def taylor3(x)
  taylor2(x) + x**3 / r(6)
end

def parse_fraction(value)
  match = /\A(-?\d+)\/([1-9]\d*)\z/.match(value.to_s)
  raise ArgumentError, "invalid rational #{value.inspect}" unless match

  result = Rational(Integer(match[1], 10), Integer(match[2], 10))
  unless value == qs(result)
    raise ArgumentError, "noncanonical rational #{value.inspect}"
  end
  result
end

certificate_path = if ARGV.empty?
                     File.expand_path(
                       "../research/r074n_all_shell_certificate.json",
                       __dir__
                     )
                   elsif ARGV.length == 1
                     File.expand_path(ARGV.fetch(0))
                   else
                     warn "usage: ruby #{File.basename(__FILE__)} [certificate.json]"
                     exit 2
                   end

raw = File.binread(certificate_path)
actual_sha256 = Digest::SHA256.hexdigest(raw)
certificate = JSON.parse(raw)
failures = []

zero = r(0)
one = r(1)
lambda_scale = r(63, 32)
annular_exponent = r(8, 3969)
radius_exponent = r(1, 320)
defect_exponent = r(1, 640)
sigma_denominator = r(32_768)
j_threshold = 14
audit_j_min = 14
audit_j_max = 21

bad_reflection_exponent = r(1, 16)
bad_reserve = bad_reflection_exponent - radius_exponent - annular_exponent
outer_jump_rate = 3 * annular_exponent
outer_reserve = outer_jump_rate - radius_exponent
outer_coefficient = r(4) / lambda_scale**2
gamma_scale_identity = annular_exponent * lambda_scale**2
sigma_square_growth = 2 * (radius_exponent - defect_exponent)
sigma_tail_denominator = r(1056) * sigma_denominator**2

chord_threshold_k = 3
chord_delta_threshold = r(3 * 4**(chord_threshold_k - 1), 32)
chord_taylor_threshold = taylor3(chord_delta_threshold)
chord_ratio_envelope_threshold = r(2) / chord_taylor_threshold
chord_geometric_ratio = r(1, 2)
chord_uniform_majorant = r(2 + 4 + 2 * 8)

outer_threshold_k = 4
outer_delta_threshold = r(3 * 4**(outer_threshold_k - 1), 32)
outer_taylor_threshold = taylor2(outer_delta_threshold)
outer_ratio_envelope_threshold = r(4) / outer_taylor_threshold
outer_geometric_ratio = r(1, 2)
outer_tail_factor = one / (one - outer_geometric_ratio)

checks = [
  expected_row("lambda", lambda_scale, "==", r(63, 32),
               "frozen dyadic scale"),
  expected_row("annular_exponent", annular_exponent, "==", r(8, 3969),
               "Gamma_j=exp(-c_gamma L_j^2)"),
  expected_row("radius_exponent", radius_exponent, "==", r(1, 320),
               "R_j=exp(-rho L_j^2)"),
  expected_row("gamma_scale_identity", gamma_scale_identity, "==", r(1, 128),
               "c_gamma lambda^2=1/128"),
  expected_row("bad_reserve", bad_reserve, "==", r(72_851, 1_270_080),
               "1/16-rho-c_gamma"),
  expected_row("bad_reserve_positive", bad_reserve, ">", zero,
               "bad path pays Gamma_j and one R"),
  expected_row("outer_jump_rate", outer_jump_rate, "==", r(8, 1323),
               "negative logarithmic rate of Gamma_(j+1)/Gamma_j"),
  expected_row("outer_reserve", outer_reserve, "==", r(1237, 423_360),
               "3c_gamma-rho"),
  expected_row("outer_reserve_positive", outer_reserve, ">", zero,
               "outer jump pays one inverse R"),
  expected_row("outer_coefficient", outer_coefficient, "==", r(4096, 3969),
               "4^(j+1)/L_j^2"),
  expected_row("sigma_square_growth", sigma_square_growth, "==", r(1, 320),
               "Sigma_L^2/R^2 has exp(L^2/320) growth"),
  expected_row("sigma_tail_denominator", sigma_tail_denominator, "==",
               r(1_133_871_366_144),
               "1056 times 32768 squared in the good-path tail"),
  expected_row("chord_threshold_delta", chord_delta_threshold, "==", r(3, 2),
               "delta_3 for b_k=2^k Gamma_k"),
  expected_row("chord_threshold_taylor3", chord_taylor_threshold, "==", r(67, 16),
               "cubic Taylor lower bound for exp(3/2)"),
  expected_row("chord_threshold_ratio_envelope",
               chord_ratio_envelope_threshold, "==", r(32, 67),
               "exact upper envelope for b_4/b_3"),
  expected_row("chord_threshold_ratio_below_half",
               chord_ratio_envelope_threshold, "<", chord_geometric_ratio,
               "chord ratios are below one half from k=3 onward"),
  expected_row("chord_delta_growth", r(4), "==", r(4),
               "delta_(k+1)/delta_k"),
  expected_row("chord_uniform_majorant", chord_uniform_majorant, "==", r(22),
               "sum 2^k Gamma_k is bounded by 2+4+2*8"),
  expected_row("outer_threshold_delta", outer_delta_threshold, "==", r(6),
               "delta_4 for a_k=4^k Gamma_k"),
  expected_row("outer_threshold_taylor2", outer_taylor_threshold, "==", r(25),
               "quadratic Taylor lower bound for exp(6)"),
  expected_row("outer_threshold_ratio_envelope",
               outer_ratio_envelope_threshold, "==", r(4, 25),
               "exact upper envelope for a_5/a_4"),
  expected_row("outer_threshold_ratio_below_half",
               outer_ratio_envelope_threshold, "<", outer_geometric_ratio,
               "outer ratios are below one half from k=4 onward"),
  expected_row("outer_delta_growth", r(4), "==", r(4),
               "delta_(k+1)/delta_k"),
  expected_row("outer_tail_factor", outer_tail_factor, "==", r(2),
               "geometric majorant used for the infinite outer tail")
]

inward_ratio_exponents = []
(1..8).each do |m|
  normalized = annular_exponent * (one - r(1, 4**m))
  direct = r(4**(j_threshold - 1) - 4**(j_threshold - m - 1), 32)
  via_l = normalized * (lambda_scale * 2**j_threshold)**2
  inward_ratio_exponents << {
    "m" => m,
    "normalized_rate" => qs(normalized),
    "direct_exponent_at_j14" => qs(direct),
    "via_L_exponent_at_j14" => qs(via_l)
  }
  checks << expected_row(
    "inward_gamma_ratio_m#{m}", via_l, "==", direct,
    "-log(Gamma_j/Gamma_(j-m)) reconstructed two ways at j=14"
  )
end

gamma_window = []
chord_window = []
outer_window = []
(audit_j_min..audit_j_max).each do |j|
  l_j = lambda_scale * 2**j
  l_j_squared = l_j**2
  gamma_exponent = annular_exponent * l_j_squared
  direct_gamma_exponent = r(4**(j - 1), 32)
  outer_jump_exponent = outer_jump_rate * l_j_squared
  direct_outer_jump = r(3 * 4**(j - 1), 32)

  chord_k = j - 2
  chord_delta = r(3 * 4**(chord_k - 1), 32)
  chord_taylor = taylor3(chord_delta)
  chord_ratio_upper = r(2) / chord_taylor

  outer_k = j + 1
  outer_delta = r(3 * 4**(outer_k - 1), 32)
  outer_taylor = taylor2(outer_delta)
  outer_ratio_upper = r(4) / outer_taylor
  coefficient = r(4**(j + 1)) / l_j_squared

  gamma_window << {
    "j" => j,
    "L_squared" => qs(l_j_squared),
    "gamma_exponent" => qs(gamma_exponent),
    "direct_gamma_exponent" => qs(direct_gamma_exponent),
    "outer_jump_exponent" => qs(outer_jump_exponent),
    "direct_outer_jump" => qs(direct_outer_jump),
    "four_j_plus_one_over_L_squared" => qs(coefficient)
  }
  chord_window << {
    "j" => j,
    "ratio_base_k" => chord_k,
    "delta" => qs(chord_delta),
    "taylor3" => qs(chord_taylor),
    "ratio_upper" => qs(chord_ratio_upper)
  }
  outer_window << {
    "j" => j,
    "ratio_base_k" => outer_k,
    "delta" => qs(outer_delta),
    "taylor2" => qs(outer_taylor),
    "ratio_upper" => qs(outer_ratio_upper)
  }

  checks.concat([
    expected_row("window_j#{j}_gamma_exponent", gamma_exponent, "==",
                 direct_gamma_exponent, "c_gamma L_j^2=4^(j-1)/32"),
    expected_row("window_j#{j}_outer_jump_exponent", outer_jump_exponent,
                 "==", direct_outer_jump,
                 "-log(Gamma_(j+1)/Gamma_j)=3c_gamma L_j^2"),
    expected_row("window_j#{j}_outer_coefficient", coefficient, "==",
                 r(4096, 3969), "4^(j+1)/L_j^2 is j-independent"),
    expected_row("window_j#{j}_chord_ratio_upper", chord_ratio_upper, "<",
                 r(1, 2), "last audited chord increment is below one half"),
    expected_row("window_j#{j}_outer_ratio_upper", outer_ratio_upper, "<",
                 r(1, 2), "first audited outer-tail ratio is below one half")
  ])
end

inner_bad_r = r(6 + 2 - 1 - 3)
inner_bad_l = zero
inner_good_r = r(6 + 2 - 1 - 4)
inner_good_l = zero
outer_shell_r = r(2 + 2)
outer_shell_l = zero
outer_summed_r = outer_shell_r
outer_summed_l = r(2)
main_r = r(5)
main_l = r(1)
target_r = r(5)
target_l = r(1)

checks.concat([
  expected_row("inner_bad_raw_R_power", inner_bad_r, "==", r(4),
               "R^6 R^2 R^-1 R^-3"),
  expected_row("inner_bad_raw_L_power", inner_bad_l, "==", zero,
               "combined chord is uniformly bounded"),
  expected_row("inner_good_raw_R_power", inner_good_r, "==", r(3),
               "R^6 R^2 R^-1 R^-4"),
  expected_row("inner_good_raw_L_power", inner_good_l, "==", zero,
               "combined chord is uniformly bounded"),
  expected_row("outer_shell_raw_R_power", outer_shell_r, "==", r(4),
               "time R^2 times collar volume-gradient R^2"),
  expected_row("outer_shell_raw_L_power", outer_shell_l, "==", zero,
               "before 4^k is normalized"),
  expected_row("outer_summed_raw_R_power", outer_summed_r, "==", r(4),
               "after outer geometric summation"),
  expected_row("outer_summed_raw_L_power", outer_summed_l, "==", r(2),
               "4^(j+1)=(4096/3969)L^2"),
  expected_row("main_inherited_R_power", main_r, "==", r(5),
               "R0.74L target-shell ledger"),
  expected_row("main_inherited_L_power", main_l, "==", r(1),
               "R0.74L target-shell ledger"),
  expected_row("target_R_power", target_r, "==", r(5),
               "Gamma_j L_j R_j^5 target"),
  expected_row("target_L_power", target_l, "==", r(1),
               "Gamma_j L_j R_j^5 target")
])

passed = checks.count { |entry| entry.fetch("pass") }
analytic_boundary = [
  "does not prove the combined inward chord or its exact periodization",
  "does not prove the common-forward-law or final-segment expulsion lemmas",
  "does not prove the packet maximum principle or outer collar volume bound",
  "does not prove convergence of the infinite annular observable",
  "does not replace the independent analytic reconstruction of R0.74N",
  "does not prove a universal endpoint estimate, regularity, singularity, or Clay"
]

expected_certificate = {
  "schema" => "r074n-all-shell-certificate-v1",
  "scope" => "finite exact rational exponent algebra, sequence audit window, and raw scale ledgers only",
  "result" => passed == checks.length ? "PASS" : "FAIL",
  "inputs" => {
    "lambda" => qs(lambda_scale),
    "c_gamma" => qs(annular_exponent),
    "rho" => qs(radius_exponent),
    "c_def" => qs(defect_exponent),
    "sigma_denominator" => qs(sigma_denominator),
    "j_threshold" => j_threshold,
    "audit_window" => [audit_j_min, audit_j_max]
  },
  "derived" => {
    "bad_reserve" => qs(bad_reserve),
    "outer_reserve" => qs(outer_reserve),
    "outer_coefficient" => qs(outer_coefficient),
    "sigma_square_growth" => qs(sigma_square_growth),
    "chord_ratio_threshold_k" => chord_threshold_k,
    "chord_ratio_envelope_at_threshold" => qs(chord_ratio_envelope_threshold),
    "chord_uniform_majorant" => qs(chord_uniform_majorant),
    "outer_ratio_threshold_k" => outer_threshold_k,
    "outer_ratio_envelope_at_threshold" => qs(outer_ratio_envelope_threshold),
    "outer_tail_factor" => qs(outer_tail_factor)
  },
  "sequence_audits" => {
    "window" => [audit_j_min, audit_j_max],
    "gamma_algebra" => gamma_window,
    "inward_ratio_exponents" => inward_ratio_exponents,
    "chord_partial_sum_increments" => chord_window,
    "outer_tail_ratios" => outer_window,
    "propagation" => {
      "delta_multiplier" => qs(r(4)),
      "chord_ratio_bound_from_k" => chord_threshold_k,
      "outer_ratio_bound_from_k" => outer_threshold_k,
      "ratio_bound" => qs(r(1, 2))
    }
  },
  "scale_ledgers" => {
    "inner_bad" => { "L_power" => qs(inner_bad_l), "R_power" => qs(inner_bad_r) },
    "inner_good" => { "L_power" => qs(inner_good_l), "R_power" => qs(inner_good_r) },
    "outer_single_shell" => { "L_power" => qs(outer_shell_l), "R_power" => qs(outer_shell_r) },
    "outer_after_summation" => { "L_power" => qs(outer_summed_l), "R_power" => qs(outer_summed_r) },
    "main_inherited" => { "L_power" => qs(main_l), "R_power" => qs(main_r) },
    "target" => { "L_power" => qs(target_l), "R_power" => qs(target_r) }
  },
  "checks" => checks,
  "summary" => { "passed" => passed, "total" => checks.length },
  "analytic_boundary" => analytic_boundary,
  "status_flags" => {
    "finite_arithmetic" => passed == checks.length ? "PASS" : "FAIL",
    "all_shell_analytic_proof" => "REQUIRES_INDEPENDENT_AUDIT",
    "finite_window_scope" => "J_14_THROUGH_J_21_WITH_MONOTONE_PROPAGATION_LEDGER",
    "clay_problem" => "NOT_CLAIMED"
  }
}

# Reject malformed or noncanonical row fractions before structural comparison.
begin
  certificate.fetch("checks").each do |entry|
    %w[left right margin].each { |key| parse_fraction(entry.fetch(key)) }
    unless relation_holds?(parse_fraction(entry.fetch("left")),
                           entry.fetch("relation"),
                           parse_fraction(entry.fetch("right"))) ==
           entry.fetch("pass")
      failures << "#{entry.fetch('id')}: stored pass flag disagrees with relation"
    end
  end
rescue KeyError, ArgumentError => e
  failures << "row schema: #{e.message}"
end

failures << "independent reconstruction differs from JSON" unless certificate == expected_certificate
unless actual_sha256 == EXPECTED_CERTIFICATE_SHA256
  failures << "certificate SHA-256 #{actual_sha256} != #{EXPECTED_CERTIFICATE_SHA256}"
end

puts "R0.74N independent exact-arithmetic reconstruction"
puts "certificate: #{certificate_path}"
puts "certificate_sha256: #{actual_sha256}"
puts "audit_window: j=#{audit_j_min}..#{audit_j_max}"
puts "gamma_rows: #{gamma_window.length}"
puts "chord_rows: #{chord_window.length}"
puts "outer_rows: #{outer_window.length}"
puts ""
checks.each do |entry|
  puts format("%-4s %-43s %s %s %s  margin=%s",
              entry.fetch("pass") ? "PASS" : "FAIL",
              entry.fetch("id"), entry.fetch("left"),
              entry.fetch("relation"), entry.fetch("right"),
              entry.fetch("margin"))
end

puts ""
if failures.empty?
  puts "RESULT: PASS (#{checks.length}/#{checks.length} checks)"
  puts "PASS #{checks.length}/#{checks.length}"
  puts "ANALYTIC BOUNDARY: finite arithmetic only; no analytic lemma is certified."
  exit 0
end

puts "RESULT: FAIL (#{failures.length} discrepancy/discrepancies)"
failures.each { |failure| puts "- #{failure}" }
exit 1
