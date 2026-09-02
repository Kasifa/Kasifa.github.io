#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent Ruby Rational reconstruction of the R0.74P finite certificate.
# It does not invoke the Python producer and does not use JSON values as
# mathematical inputs.

require "digest"
require "json"

EXPECTED_CERTIFICATE_SHA256 =
  "c65b38def48b5439f112ab145360c1abb211de5bf6f004eca103271d8d9a204b"

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

def check_row(id, left, relation, right, note)
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

def parse_fraction(value)
  match = /\A(-?\d+)\/([1-9]\d*)\z/.match(value.to_s)
  raise ArgumentError, "invalid rational #{value.inspect}" unless match

  result = Rational(Integer(match[1], 10), Integer(match[2], 10))
  raise ArgumentError, "noncanonical rational #{value.inspect}" unless value == qs(result)

  result
end

def first_difference(expected, actual, path = "$")
  return nil if expected == actual

  if expected.is_a?(Hash) && actual.is_a?(Hash)
    keys = (expected.keys | actual.keys).sort
    keys.each do |key|
      return "#{path}.#{key}: missing from expected" unless expected.key?(key)
      return "#{path}.#{key}: missing from actual" unless actual.key?(key)

      difference = first_difference(expected[key], actual[key], "#{path}.#{key}")
      return difference if difference
    end
  elsif expected.is_a?(Array) && actual.is_a?(Array)
    return "#{path}: length #{actual.length}, expected #{expected.length}" unless expected.length == actual.length

    expected.each_index do |index|
      difference = first_difference(expected[index], actual[index], "#{path}[#{index}]")
      return difference if difference
    end
  end

  "#{path}: actual #{actual.inspect}, expected #{expected.inspect}"
end

certificate_path = if ARGV.empty?
                     File.expand_path(
                       "../research/r074p_temporal_clock_certificate.json",
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
half = r(1, 2)
two_thirds = r(2, 3)

margin_m = r(43, 423_360)
c_gamma = r(8, 3_969)
kappa_exponential_rate = margin_m / 3
kappa_l_power = two_thirds
k_exponential_rate = 2 * kappa_exponential_rate
k_l_power = 2 * kappa_l_power + 1
strong_gamma_penalty = c_gamma / 2

checks = [
  check_row("m_exact", margin_m, "==", r(43, 423_360),
            "inherited R0.74O amplitude reserve"),
  check_row("m_positive", margin_m, ">", zero,
            "the missing-scale factor grows exponentially"),
  check_row("c_gamma_exact", c_gamma, "==", r(8, 3_969),
            "target-shell super-Gaussian decay coefficient"),
  check_row("kappa_exponential_rate", kappa_exponential_rate, "==",
            r(43, 1_270_080), "kappa=exp((m/3)L^2)L^(2/3)"),
  check_row("kappa_L_power", kappa_l_power, "==", two_thirds,
            "polynomial L power in kappa"),
  check_row("K_exponential_rate", k_exponential_rate, "==",
            r(43, 635_040), "K=kappa^2 L exponential rate"),
  check_row("K_exponential_rate_positive", k_exponential_rate, ">", zero,
            "K tends to infinity"),
  check_row("K_L_power", k_l_power, "==", r(7, 3),
            "K=kappa^2 L has L power 7/3"),
  check_row("target_gamma_cancellation", one - one, "==", zero,
            "gamma times a_*^2 cancels Gamma^(-1)"),
  check_row("target_kappa_power", 2 * one, "==", r(2),
            "weighted target energy is quadratic in kappa"),
  check_row("strong_gamma_power", -half, "==", r(-1, 2),
            "strong square function divides the target by sqrt(Gamma)"),
  check_row("strong_exponential_penalty", strong_gamma_penalty, "==",
            r(4, 3_969), "Gamma^(-1/2) exponential coefficient"),
  check_row("strong_exponential_penalty_positive", strong_gamma_penalty,
            ">", zero, "over-weighted target cost is exponential")
]

sigma_values = [r(1, 4), r(1, 2), r(3, 4), r(1), r(3, 2), r(2), r(4)]
carleson_rows = []
sigma_values.each do |sigma|
  beta = [sigma, one].min
  branch = if sigma < one
             "intersection"
           elsif sigma == one
             "constant"
           else
             "right-endpoint-supremum"
           end
  carleson_rows << {
    "sigma" => qs(sigma),
    "attenuation_beta" => qs(beta),
    "maximizer_branch" => branch,
    "bound" => "K^(-beta)"
  }
  slug = "#{sigma.numerator}_#{sigma.denominator}"
  checks.concat(
    [
      check_row("sigma_#{slug}_beta_positive", beta, ">", zero,
                "every fixed sampled positive order attenuates"),
      check_row("sigma_#{slug}_beta_at_most_one", beta, "<=", one,
                "beta=min(sigma,1)"),
      check_row("sigma_#{slug}_beta_exact", beta, "==",
                sigma < one ? sigma : one,
                "piecewise Carleson attenuation exponent")
    ]
  )
end

square_roots = [2, 4, 8, 16, 32, 64]
l1_l2_rows = []
square_roots.each do |root_integer|
  root = r(root_integer)
  count = root * root
  l1 = count
  l2 = root
  ratio = l1 / l2
  l1_l2_rows << {
    "N" => count.to_i,
    "l1" => qs(l1),
    "l2" => qs(l2),
    "ratio" => qs(ratio),
    "sequence" => "N equal entries of value one"
  }
  checks.concat(
    [
      check_row("equal_#{count.to_i}_l2", l2, "==", root,
                "sqrt(N) for a perfect-square test size"),
      check_row("equal_#{count.to_i}_ratio", ratio, "==", root,
                "l1/l2=sqrt(N)"),
      check_row("equal_#{count.to_i}_strict_gap", l1, ">", l2,
                "finite equal-entry sequence separates l1 and l2")
    ]
  )
end

scale_rows = [
  {
    "name" => "paid_average",
    "B_power" => qs(r(2)),
    "R_power" => qs(r(2)),
    "L_power" => qs(zero),
    "kappa_power" => qs(zero),
    "Gamma_power" => qs(zero),
    "description" => "(P_*)^(2/3) is comparable to B^2 R^2"
  },
  {
    "name" => "target_clock",
    "B_power" => qs(r(2)),
    "R_power" => qs(r(2)),
    "L_power" => qs(one),
    "kappa_power" => qs(r(2)),
    "Gamma_power" => qs(zero),
    "description" => "v_j and T_* have scale kappa^2 B^2 L R^2"
  },
  {
    "name" => "missing_factor_K",
    "B_power" => qs(zero),
    "R_power" => qs(zero),
    "L_power" => qs(one),
    "kappa_power" => qs(r(2)),
    "Gamma_power" => qs(zero),
    "description" => "target clock divided by the paid average"
  },
  {
    "name" => "strong_target_clock",
    "B_power" => qs(r(2)),
    "R_power" => qs(r(2)),
    "L_power" => qs(one),
    "kappa_power" => qs(r(2)),
    "Gamma_power" => qs(r(-1, 2)),
    "description" => "over-weighted square function target lower bound"
  }
]

passed = checks.count { |item| item.fetch("pass") }
analytic_boundary = [
  "FINITE ONLY: exact rational exponent and finite sequence bookkeeping",
  "does not prove the local energy measure identity or moving-test passage",
  "does not prove the shellwise total-variation ledgers or infinite-shell limits",
  "does not prove the continuum optimization for every real sigma>0",
  "does not prove the exact-family terminal-lobe or target-flux estimates",
  "does not prove path, pressure-primitive, clock, BV, or square-function compactness",
  "does not prove an l1-to-l2 Navier--Stokes inequality or a good-scale theorem",
  "does not verify literature, novelty, or priority",
  "does not prove regularity, singularity, blow-up, continuation, or global smoothness",
  "does not solve the Clay Millennium problem; NOT CLAY"
]

expected_certificate = {
  "schema" => "r074p-temporal-clock-certificate-v1",
  "scope" => "FINITE ONLY: exact missing-factor arithmetic, sampled Carleson exponents, target weights, and finite l1/l2 witnesses",
  "inputs" => {
    "m" => qs(margin_m),
    "c_gamma" => qs(c_gamma),
    "sigma_grid" => sigma_values.map { |value| qs(value) },
    "equal_sequence_square_roots" => square_roots
  },
  "derived" => {
    "kappa_exponential_rate" => qs(kappa_exponential_rate),
    "kappa_L_power" => qs(kappa_l_power),
    "K_exponential_rate" => qs(k_exponential_rate),
    "K_L_power" => qs(k_l_power),
    "strong_Gamma_inverse_sqrt_exponential_rate" => qs(strong_gamma_penalty)
  },
  "scale_rows" => scale_rows,
  "carleson_rows" => carleson_rows,
  "l1_l2_rows" => l1_l2_rows,
  "checks" => checks,
  "exact_implications" => [
    "K_*=kappa^2 L has exponential rate 43/635040 and polynomial L power 7/3, so K_* diverges.",
    "The target-shell factor Gamma cancels the Gamma^(-1) in a_*^2, leaving the T_* scale.",
    "For each sampled fixed sigma>0, the Carleson attenuation exponent is min(sigma,1)>0.",
    "For N equal unit entries with sampled perfect-square N, l1/l2=sqrt(N).",
    "Dividing the matched target clock by sqrt(Gamma) adds exponential rate 4/3969."
  ],
  "analytic_boundary" => analytic_boundary,
  "result" => passed == checks.length ? "PASS" : "FAIL",
  "summary" => {
    "passed" => passed,
    "total" => checks.length,
    "unique_ids" => checks.map { |item| item.fetch("id") }.uniq.length,
    "scale_rows" => scale_rows.length,
    "carleson_rows" => carleson_rows.length,
    "l1_l2_rows" => l1_l2_rows.length
  }
}

begin
  actual_checks = certificate.fetch("checks")
  ids = actual_checks.map { |entry| entry.fetch("id") }
  failures << "duplicate check ids" unless ids.uniq.length == ids.length
  actual_checks.each do |entry|
    left = parse_fraction(entry.fetch("left"))
    right = parse_fraction(entry.fetch("right"))
    margin = parse_fraction(entry.fetch("margin"))
    relation = entry.fetch("relation")
    failures << "#{entry.fetch('id')}: false pass flag" unless entry.fetch("pass")
    failures << "#{entry.fetch('id')}: relation fails" unless relation_holds?(left, relation, right)
    unless margin == signed_margin(left, relation, right)
      failures << "#{entry.fetch('id')}: margin mismatch"
    end
  end
rescue KeyError, ArgumentError => e
  failures << "row schema: #{e.message}"
end

difference = first_difference(expected_certificate, certificate)
failures << "independent reconstruction differs: #{difference}" if difference
if actual_sha256 != EXPECTED_CERTIFICATE_SHA256
  failures << "certificate SHA-256 #{actual_sha256} != #{EXPECTED_CERTIFICATE_SHA256}"
end

puts "certificate_sha256: #{actual_sha256}"
puts "scale_rows: #{scale_rows.length}"
puts "carleson_rows: #{carleson_rows.length}"
puts "l1_l2_rows: #{l1_l2_rows.length}"

if failures.empty?
  puts "RESULT: PASS (#{passed}/#{checks.length} checks)"
  puts "PASS #{passed}/#{checks.length}"
  exit 0
end

warn "RESULT: FAIL"
failures.each { |failure| warn "- #{failure}" }
exit 1
