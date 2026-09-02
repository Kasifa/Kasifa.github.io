#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent Ruby Rational reconstruction of the R0.74O finite certificate.
# It never invokes the Python producer and never treats JSON values as
# mathematical inputs.  The expected byte-level JSON hash is frozen below.

require "digest"
require "json"

EXPECTED_CERTIFICATE_SHA256 =
  "30fd77ae3b4c88628e2d84207fc9b1728b1ab2343bf187fcd1141b080d6c5a5b"

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

def scale(name, b_power, r_power, l_power, kappa_power, gamma_power,
          heat_decay, note)
  {
    "name" => name,
    "B_power" => qs(b_power),
    "R_power" => qs(r_power),
    "L_power" => qs(l_power),
    "kappa_power" => qs(kappa_power),
    "Gamma_power" => qs(gamma_power),
    "heat_decay_coefficient" => qs(heat_decay),
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
                       "../research/r074o_amplitude_endpoint_certificate.json",
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
three_halves = r(3, 2)

lambda_scale = r(63, 32)
rho = r(1, 320)
c_gamma = r(8, 3969)
d_energy = r(98, 29_475)
e_energy = d_energy - c_gamma
margin_m = rho - three_halves * c_gamma
energy_reserve = e_energy - two_thirds * margin_m
delta = 2 * margin_m / (9 * rho)
q_star = two_thirds + delta
kappa_exponential_rate = margin_m / 3
kappa_l_power = two_thirds

audit_j_min = 14
audit_j_max = 21

checks = [
  expected_row("lambda_exact", lambda_scale, "==", r(63, 32),
               "frozen dyadic prefactor"),
  expected_row("rho_exact", rho, "==", r(1, 320),
               "R=exp(-rho L^2)"),
  expected_row("c_gamma_exact", c_gamma, "==", r(8, 3969),
               "Gamma=exp(-c_gamma L^2)"),
  expected_row("d_energy_exact", d_energy, "==", r(98, 29_475),
               "buffered packet-energy decay coefficient"),
  expected_row("e_energy_definition", e_energy, "==",
               d_energy - c_gamma, "e_E=d_E-c_gamma"),
  expected_row("e_energy_exact", e_energy, "==",
               r(17_018, 12_998_475),
               "exact packet-energy reserve before kappa"),
  expected_row("m_definition", margin_m, "==",
               rho - three_halves * c_gamma, "m=rho-3c_gamma/2"),
  expected_row("m_exact", margin_m, "==", r(43, 423_360),
               "exact cubic occupation reserve"),
  expected_row("m_positive", margin_m, ">", zero,
               "the exponential amplitude rate is positive"),
  expected_row("energy_reserve_definition", energy_reserve, "==",
               e_energy - two_thirds * margin_m,
               "energy reserve after the squared kappa amplitude"),
  expected_row("energy_reserve_exact", energy_reserve, "==",
               r(1171, 943_200), "e_E-2m/3"),
  expected_row("energy_reserve_positive", energy_reserve, ">", zero,
               "packet energy retains strict exponential decay"),
  expected_row("delta_definition", delta, "==",
               2 * margin_m / (9 * rho), "delta=2m/(9rho)"),
  expected_row("delta_exact", delta, "==", r(86, 11_907),
               "exact payment-power increment"),
  expected_row("delta_positive", delta, ">", zero,
               "q_star lies above two thirds"),
  expected_row("q_star_definition", q_star, "==", two_thirds + delta,
               "q_star=2/3+delta"),
  expected_row("q_star_exact", q_star, "==", r(8024, 11_907),
               "exact amplitude endpoint power"),
  expected_row("q_star_above_two_thirds", q_star, ">", two_thirds,
               "strict power lift"),
  expected_row("q_star_below_one", q_star, "<", one,
               "the endpoint power stays sublinear"),
  expected_row("kappa_exponential_rate", kappa_exponential_rate, "==",
               r(43, 1_270_080), "exp((m/3)L^2) rate"),
  expected_row("kappa_polynomial_L_power", kappa_l_power, "==",
               two_thirds,
               "L^(2/3) factor in the exact exponential amplitude"),
  expected_row("G_exponential_cancellation",
               3 * kappa_exponential_rate - rho + three_halves * c_gamma,
               "==", zero,
               "kappa^3 R Gamma^(-3/2) has zero L^2 exponent"),
  expected_row("G_polynomial_cancellation",
               3 * kappa_l_power - 2, "==", zero,
               "kappa^3 L^-2 has zero L power"),
  expected_row("H_polynomial_power",
               3 * kappa_l_power - r(7, 2), "==", r(-3, 2),
               "the harmonic packet ratio retains L^-3/2"),
  expected_row("energy_polynomial_power", 2 * kappa_l_power, "==",
               r(4, 3),
               "the squared amplitude contributes L^(4/3)"),
  expected_row("observable_polynomial_power",
               2 * kappa_l_power + 1, "==", r(7, 3),
               "collar and X observables carry kappa^2 L"),
  expected_row("observable_log_power",
               (2 * kappa_l_power + 1) / 2, "==", r(7, 6),
               "log P is proportional to L^2"),
  expected_row("sqrt_log_L_power", 2 * half, "==", one,
               "sqrt(log P) contributes one L power"),
  expected_row("endpoint_ratio_L_power",
               2 * kappa_l_power + 1 - 1, "==", r(4, 3),
               "ratio to the square-root-log comparator"),
  expected_row("endpoint_ratio_log_power",
               (2 * kappa_l_power + 1 - 1) / 2, "==", r(2, 3),
               "L^(4/3) equals (log P)^(2/3)"),
  expected_row("payment_growth_coefficient", 3 * rho, "==", r(3, 320),
               "B R^2 asymptotically constant makes B^3R^3 grow like exp(3rho L^2)"),
  expected_row("observable_growth_coefficient",
               2 * rho + 2 * kappa_exponential_rate, "==",
               r(1003, 158_760),
               "kappa^2 B^2 L R^2 exponential coefficient"),
  expected_row("delta_payment_match", 3 * rho * delta, "==",
               two_thirds * margin_m,
               "P^delta supplies exactly exp((2m/3)L^2)"),
  expected_row("q_star_exponential_match", 3 * rho * q_star, "==",
               2 * rho + 2 * kappa_exponential_rate,
               "P^q_star matches the observable exponential rate"),
  expected_row("calibrated_payment_R_power", -2 * 3 + 3, "==", r(-3),
               "B~R^-2 sends B^3R^3 to R^-3"),
  expected_row("calibrated_observable_R_power", -2 * 2 + 2, "==", r(-2),
               "B~R^-2 sends B^2R^2 to R^-2 before kappa")
]

scale_ledgers = [
  scale("E_shear", r(2), r(2), zero, zero, zero, zero,
        "background buffered energy B^2 R^2"),
  scale("E_packet", r(2), r(2), zero, r(2), r(-1), -d_energy,
        "a^2 R^2 exp(-d_E L^2) after a=kappa B Gamma^-1/2"),
  scale("G_shear", r(3), r(3), zero, zero, zero, zero,
        "background cubic row B^3 R^3"),
  scale("G_packet", r(3), r(4), r(-2), r(3), r(-3, 2), zero,
        "packet cubic row kappa^3 B^3 Gamma^-3/2 R^4 L^-2"),
  scale("H_shear", r(3), r(3), zero, zero, zero, zero,
        "background harmonic row B^3 R^3"),
  scale("H_packet", r(3), r(4), r(-7, 2), r(3), r(-3, 2), zero,
        "packet harmonic row kappa^3 B^3 Gamma^-3/2 R^4 L^-7/2"),
  scale("P", r(3), r(3), zero, zero, zero, zero,
        "complete payment scale B^3 R^3 after analytic absorption"),
  scale("C", r(2), r(2), one, r(2), zero, zero,
        "collar observable a^2 Gamma L R^2 after amplitude substitution"),
  scale("X", r(2), r(2), one, r(2), zero, zero,
        "exterior observable a^2 Gamma L R^2 after amplitude substitution")
]

expected_scale_values = {
  "E_shear" => [2, 2, 0, 0, 0, 0],
  "E_packet" => [2, 2, 0, 2, -1, -d_energy],
  "G_shear" => [3, 3, 0, 0, 0, 0],
  "G_packet" => [3, 4, -2, 3, r(-3, 2), 0],
  "H_shear" => [3, 3, 0, 0, 0, 0],
  "H_packet" => [3, 4, r(-7, 2), 3, r(-3, 2), 0],
  "P" => [3, 3, 0, 0, 0, 0],
  "C" => [2, 2, 1, 2, 0, 0],
  "X" => [2, 2, 1, 2, 0, 0]
}
scale_labels = %w[
  B_power R_power L_power kappa_power Gamma_power
  heat_decay_coefficient
]

scale_ledgers.each do |entry|
  name = entry.fetch("name")
  scale_labels.zip(expected_scale_values.fetch(name)).each do |label, value|
    checks << expected_row(
      "scale_#{name}_#{label}",
      parse_fraction(entry.fetch(label)),
      "==",
      r(value),
      "raw #{name} #{label} ledger"
    )
  end
end

checks.concat([
  expected_row("E_packet_exponential_coefficient",
               2 * kappa_exponential_rate + c_gamma - d_energy,
               "==", -energy_reserve,
               "packet-to-shear energy ratio decays at the strict reserve"),
  expected_row("E_packet_L_power_after_kappa", 2 * kappa_l_power,
               "==", r(4, 3), "energy ratio polynomial factor"),
  expected_row("G_packet_R_power_relative_to_shear", 4 - 3,
               "==", one,
               "one R remains before exponential-amplitude cancellation"),
  expected_row("G_packet_L_power_after_kappa",
               -2 + 3 * kappa_l_power, "==", zero,
               "cubic packet matches the background polynomial scale"),
  expected_row("H_packet_R_power_relative_to_shear", 4 - 3,
               "==", one,
               "one R remains before exponential-amplitude cancellation"),
  expected_row("H_packet_L_power_after_kappa",
               r(-7, 2) + 3 * kappa_l_power, "==", r(-3, 2),
               "harmonic packet is lower by L^-3/2"),
  expected_row("C_Gamma_cancellation", -one + one, "==", zero,
               "a^2 contributes Gamma^-1 and the collar contributes Gamma"),
  expected_row("X_Gamma_cancellation", -one + one, "==", zero,
               "a^2 contributes Gamma^-1 and the exterior lower bound contributes Gamma")
])

window_ledgers = []
(audit_j_min..audit_j_max).each do |j|
  l_squared = (lambda_scale * 2**j)**2
  gamma_decay = c_gamma * l_squared
  radius_decay = rho * l_squared
  kappa_exp = kappa_exponential_rate * l_squared
  kappa_cubed_exp = 3 * kappa_exp
  reserve_decay = energy_reserve * l_squared
  payment_growth = 3 * radius_decay
  observable_growth =
    (2 * rho + 2 * kappa_exponential_rate) * l_squared
  endpoint_growth = 3 * rho * q_star * l_squared
  window_ledgers << {
    "j" => j,
    "L_squared" => qs(l_squared),
    "Gamma_decay_exponent" => qs(gamma_decay),
    "R_decay_exponent" => qs(radius_decay),
    "kappa_exponent" => qs(kappa_exp),
    "kappa_cubed_exponent" => qs(kappa_cubed_exp),
    "energy_reserve_exponent" => qs(reserve_decay),
    "payment_growth_exponent" => qs(payment_growth),
    "observable_growth_exponent" => qs(observable_growth),
    "endpoint_growth_exponent" => qs(endpoint_growth)
  }
  checks.concat([
    expected_row("window_j#{j}_L_squared", l_squared, "==",
                 r(3969, 1024) * 4**j, "exact dyadic L_j^2"),
    expected_row("window_j#{j}_Gamma_decay", gamma_decay, "==",
                 r(4**j, 128), "c_gamma L_j^2"),
    expected_row("window_j#{j}_R_decay", radius_decay, "==",
                 r(3969 * 4**j, 327_680), "rho L_j^2"),
    expected_row("window_j#{j}_kappa_cubed", kappa_cubed_exp, "==",
                 margin_m * l_squared,
                 "three kappa exponential rates equal m L_j^2"),
    expected_row("window_j#{j}_energy_reserve_positive", reserve_decay,
                 ">", zero,
                 "strict packet-energy decay at this audited index"),
    expected_row("window_j#{j}_G_exponential_cancel",
                 kappa_cubed_exp - radius_decay +
                   three_halves * gamma_decay,
                 "==", zero,
                 "kappa^3 R Gamma^-3/2 cancellation at this index"),
    expected_row("window_j#{j}_endpoint_growth_match", endpoint_growth,
                 "==", observable_growth,
                 "P^q_star and the observable have the same exponential rate")
  ])
end

propagation_fields = %w[
  L_squared Gamma_decay_exponent R_decay_exponent kappa_exponent
  kappa_cubed_exponent energy_reserve_exponent payment_growth_exponent
  observable_growth_exponent endpoint_growth_exponent
]
window_ledgers.zip(window_ledgers.drop(1)).each do |left, right|
  next if right.nil?

  j = left.fetch("j")
  propagation_fields.each do |field|
    left_value = parse_fraction(left.fetch(field))
    right_value = parse_fraction(right.fetch(field))
    checks << expected_row(
      "window_j#{j}_to_j#{j + 1}_#{field}_factor",
      right_value,
      "==",
      4 * left_value,
      "all L^2 exponent ledgers propagate monotonically by factor four"
    )
  end
end

polynomial_choices = [
  [r(-2), r(0)],
  [r(-1), r(0)],
  [r(0), r(0)],
  [r(1, 2), r(1)],
  [r(1), r(1)],
  [r(2), r(2)],
  [r(4), r(4)]
]
polynomial_kappa_grid = []
polynomial_choices.each do |gamma, capital_m|
  threshold = gamma - half
  observable_l = 2 * capital_m + 1
  comparator_l = 2 * gamma
  divergence_l = observable_l - comparator_l
  polynomial_kappa_grid << {
    "gamma" => qs(gamma),
    "M" => qs(capital_m),
    "threshold_gamma_minus_half" => qs(threshold),
    "energy_ratio_L_power" => qs(2 * capital_m),
    "G_ratio_L_power" => qs(3 * capital_m - 2),
    "H_ratio_L_power" => qs(3 * capital_m - r(7, 2)),
    "observable_L_power" => qs(observable_l),
    "comparator_L_power" => qs(comparator_l),
    "divergence_L_power" => qs(divergence_l)
  }
  slug = if gamma.denominator == 1
           gamma.numerator.to_s
         else
           "#{gamma.numerator}_#{gamma.denominator}"
         end
  slug = slug.gsub("-", "neg")
  checks.concat([
    expected_row("poly_gamma_#{slug}_M_threshold", capital_m, ">",
                 threshold,
                 "chosen polynomial amplitude M exceeds gamma-1/2"),
    expected_row("poly_gamma_#{slug}_observable_L_power", observable_l,
                 "==", 2 * capital_m + 1,
                 "kappa^2 L observable power"),
    expected_row("poly_gamma_#{slug}_comparator_L_power", comparator_l,
                 "==", 2 * gamma,
                 "(log P)^gamma contributes L^(2gamma)"),
    expected_row("poly_gamma_#{slug}_divergence_L_power", divergence_l,
                 ">", zero,
                 "observable/comparator ratio has a positive L power")
  ])
end

passed = checks.count { |entry| entry.fetch("pass") }
analytic_boundary = [
  "FINITE ONLY: exact rational exponent and raw scale bookkeeping",
  "does not prove the buffered-energy, cubic-occupation, harmonic, pressure, or calibration estimates",
  "does not prove the collar-flux or exterior-observable lower bounds",
  "does not prove that the displayed asymptotic scales hold for any Navier--Stokes family",
  "does not prove a universal endpoint inequality or its failure without the separate analytic argument",
  "does not verify literature, novelty, or priority",
  "does not prove regularity, singularity, blow-up, continuation, or global smoothness",
  "does not solve the Clay Millennium problem; NOT CLAY"
]

expected_certificate = {
  "schema" => "r074o-amplitude-endpoint-certificate-v1",
  "scope" => "FINITE ONLY: exact rational amplitude-endpoint arithmetic, raw scale ledgers, finite index window, and polynomial-kappa sample grid",
  "inputs" => {
    "lambda" => qs(lambda_scale),
    "rho" => qs(rho),
    "c_gamma" => qs(c_gamma),
    "d_E" => qs(d_energy),
    "audit_window" => [audit_j_min, audit_j_max],
    "polynomial_gamma_grid" => polynomial_choices.map { |item| qs(item[0]) }
  },
  "derived" => {
    "e_E" => qs(e_energy),
    "m" => qs(margin_m),
    "energy_reserve" => qs(energy_reserve),
    "delta" => qs(delta),
    "q_star" => qs(q_star),
    "kappa_exponential_rate" => qs(kappa_exponential_rate),
    "kappa_L_power" => qs(kappa_l_power),
    "G_post_cancellation_L_power" => qs(zero),
    "H_post_cancellation_L_power" => qs(r(-3, 2)),
    "energy_polynomial_L_power" => qs(r(4, 3)),
    "observable_L_power" => qs(r(7, 3)),
    "observable_log_power" => qs(r(7, 6)),
    "endpoint_ratio_log_power" => qs(r(2, 3))
  },
  "scale_ledgers" => scale_ledgers,
  "window_ledgers" => window_ledgers,
  "window_propagation" => {
    "factor" => qs(r(4)),
    "fields" => propagation_fields,
    "reason" => "L_(j+1)^2=4L_j^2 and every displayed exponent is a fixed positive multiple of L_j^2"
  },
  "polynomial_kappa_grid" => polynomial_kappa_grid,
  "checks" => checks,
  "exact_implications" => [
    "For kappa=exp((m/3)L^2)L^(2/3), kappa^3 R Gamma^(-3/2)L^(-2)=1 at the exponent-ledger level.",
    "The H packet ratio has L power -3/2, while the packet energy ratio has L power 4/3 and strict exponential reserve 1171/943200.",
    "Under B R^2 asymptotically constant, P has exponential rate 3rho and the collar/X observable has the same exponential rate as P^q_star.",
    "The observable has residual L power 7/3, hence log power 7/6; relative to a square-root-log comparator the ratio has log power 2/3.",
    "For polynomial kappa=L^M, every sampled M exceeds gamma-1/2, so the observable divided by P^(2/3)(log P)^gamma has positive L power."
  ],
  "analytic_boundary" => analytic_boundary,
  "result" => passed == checks.length ? "PASS" : "FAIL",
  "summary" => {
    "passed" => passed,
    "total" => checks.length,
    "unique_ids" => checks.map { |item| item.fetch("id") }.uniq.length,
    "scale_rows" => scale_ledgers.length,
    "window_rows" => window_ledgers.length,
    "polynomial_rows" => polynomial_kappa_grid.length
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
    unless relation_holds?(left, relation, right)
      failures << "#{entry.fetch('id')}: relation fails"
    end
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
puts "audit_window: j=#{audit_j_min}..#{audit_j_max}"
puts "scale_rows: #{scale_ledgers.length}"
puts "window_rows: #{window_ledgers.length}"
puts "polynomial_rows: #{polynomial_kappa_grid.length}"

if failures.empty?
  puts "RESULT: PASS (#{passed}/#{checks.length} checks)"
  puts "PASS #{passed}/#{checks.length}"
  exit 0
end

warn "RESULT: FAIL"
failures.each { |failure| warn "- #{failure}" }
exit 1
