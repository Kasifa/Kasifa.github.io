#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent Rational reconstruction of every finite R0.74J certificate
# field.  The frozen JSON is opened only after all arithmetic and boundary
# strings have been reconstructed.

require "json"

CERTIFICATE_PATH = File.expand_path(
  "../research/r074j_matching_payment_certificate.json",
  __dir__
)

def q(value)
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
    "left" => q(left),
    "relation" => relation,
    "right" => q(right),
    "margin" => q(margin),
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
half = Rational(1, 2)
two_thirds = Rational(2, 3)

shell_index = Rational(5, 1)
rho_over_r = Rational(2, 1)
shell_inner = Rational(2, 1)**shell_index.to_i * rho_over_r
shell_outer = Rational(2, 1)**(shell_index.to_i + 1) * rho_over_r
box_x1_length = Rational(2, 1)
box_x2_length = Rational(2, 1)
box_x3_lower = Rational(80, 1)
box_x3_upper = Rational(96, 1)
box_x3_length = box_x3_upper - box_x3_lower
box_volume = box_x1_length * box_x2_length * box_x3_length
box_outer_square = box_x3_upper**2 + one + one
shell_outer_square = shell_outer**2

gamma_numerator = Rational(4, 1)**(shell_index.to_i - 1)
gamma_exponent = gamma_numerator / Rational(32, 1)

r_cap = Rational(1, 200)
arcsin_input_cap = Rational(16, 1) * r_cap
delta_over_r = Rational(2, 1) * Rational(16, 1)
left_distance = box_x3_lower - delta_over_r
right_distance_absolute_lower = Rational(3, 1) -
                                (delta_over_r + box_x3_upper) * r_cap
required_distance_at_cap = Rational(48, 1) * r_cap

time_upper = Rational(65, 1)
brownian_variance_coefficient = Rational(2, 1) * time_upper
exit_denominator = left_distance**2
exit_probability = brownian_variance_coefficient / exit_denominator
one_minus_theta = Rational(2, 1) * exit_probability
theta_lower = one - one_minus_theta

time_lower = Rational(61, 1)
time_length = time_upper - time_lower
normalization_coefficient = Rational(1, 4)
box_volume_coefficient = box_volume
theta_cube_floor = half**3
gu_coefficient = normalization_coefficient *
                 time_length *
                 box_volume_coefficient *
                 theta_cube_floor
gu_r_power = Rational(-2, 1) + Rational(2, 1) + Rational(3, 1)

rho = Rational(1, 320)
log_payment_coefficient = Rational(3, 1) * rho
l_square_ratio = Rational(2, 1)**2
lacunarity_coefficient = log_payment_coefficient * (l_square_ratio - one)

payment_b_power = Rational(3, 1)
payment_r_power = Rational(3, 1)
payment_l_power = Rational(0, 1)
payment_23_b_power = payment_b_power * two_thirds
payment_23_r_power = payment_r_power * two_thirds
payment_23_l_power = payment_l_power * two_thirds
sqrt_log_l_power = Rational(2, 1) * half
frontier_l_power = payment_23_l_power + sqrt_log_l_power

ratio_b_power = payment_b_power - Rational(2, 1)
ratio_r_power = payment_r_power - Rational(2, 1)
ratio_l_power = payment_l_power - Rational(1, 1)

checks = [
  exact_check("payment_shell_index", shell_index, "==", Rational(5, 1), "the selected payment shell has index k=5"),
  exact_check("payment_radius_over_R", rho_over_r, "==", Rational(2, 1), "the complete payment is evaluated at rho=2R"),
  exact_check("shell_inner_over_R", shell_inner, "==", Rational(64, 1), "2^5 times 2R gives the fifth-shell inner radius 64R"),
  exact_check("shell_outer_over_R", shell_outer, "==", Rational(128, 1), "2^6 times 2R gives the fifth-shell outer radius 128R"),
  exact_check("box_inner_is_outside_shell_inner", shell_inner, "<", box_x3_lower, "the box has |x|>80R>64R"),
  exact_check("box_outer_square_is_inside_shell_outer", box_outer_square, "<", shell_outer_square, "96^2+1^2+1^2 is strictly below 128^2"),
  exact_check("box_outer_squared_margin", shell_outer_square - box_outer_square, "==", Rational(7166, 1), "the exact squared outer-shell margin is 7166 R^2"),
  exact_check("box_volume_coefficient", box_volume, "==", Rational(64, 1), "the side lengths 2R,2R,16R give volume 64R^3"),
  exact_check("gamma5_power_numerator", gamma_numerator, "==", Rational(256, 1), "4^(5-1)=256"),
  exact_check("gamma5_exponent", gamma_exponent, "==", Rational(8, 1), "4^4/32=8, so gamma_5=e^-8"),
  exact_check("R_cap", r_cap, "==", Rational(1, 200), "the analytic proof imposes R<=1/200"),
  exact_check("arcsin_input_cap", arcsin_input_cap, "==", Rational(2, 25), "16R<=2/25 under the frozen R cap"),
  exact_check("arcsin_input_below_half", arcsin_input_cap, "<", half, "2/25<1/2 permits arcsin(s)<=2s"),
  exact_check("delta_over_R_upper", delta_over_r, "==", Rational(32, 1), "arcsin(16R)<=32R"),
  exact_check("left_plateau_distance_over_R", left_distance, "==", Rational(48, 1), "80R-32R=48R"),
  exact_check("right_plateau_distance_at_R_cap", required_distance_at_cap, "<", right_distance_absolute_lower, "pi>3 and R<=1/200 leave more than 48R on the right"),
  exact_check("brownian_variance_coefficient", brownian_variance_coefficient, "==", Rational(130, 1), "Var(Z_t)=2t<=130R^2"),
  exact_check("chebyshev_denominator_coefficient", exit_denominator, "==", Rational(2304, 1), "(48R)^2=2304R^2"),
  exact_check("exit_probability_upper", exit_probability, "==", Rational(65, 1152), "130/2304 reduces to 65/1152"),
  exact_check("one_minus_theta_upper", one_minus_theta, "==", Rational(65, 576), "the range bound 0<=1-g<=2 doubles the exit probability"),
  exact_check("theta_rational_lower", theta_lower, "==", Rational(511, 576), "1-65/576=511/576"),
  exact_check("half_is_below_theta_lower", half, "<", theta_lower, "511/576>1/2"),
  exact_check("I_2R_length_coefficient", time_length, "==", Rational(4, 1), "65-61=4"),
  exact_check("payment_normalization_coefficient", normalization_coefficient, "==", Rational(1, 4), "(2R)^-2=(1/4)R^-2"),
  exact_check("theta_cube_floor", theta_cube_floor, "==", Rational(1, 8), "(1/2)^3=1/8"),
  exact_check("Gu_lower_coefficient", gu_coefficient, "==", Rational(8, 1), "(1/4)*4*64*(1/8)=8"),
  exact_check("Gu_R_power", gu_r_power, "==", Rational(3, 1), "normalization,time,and volume give -2+2+3=3"),
  exact_check("rho_exact_value", rho, "==", Rational(1, 320), "the frozen family uses rho=1/320"),
  exact_check("log_payment_coefficient", log_payment_coefficient, "==", Rational(3, 320), "matching B^3R^3 payment gives logarithmic coefficient 3rho"),
  exact_check("L_square_ratio", l_square_ratio, "==", Rational(4, 1), "L_(j+1)^2=4L_j^2"),
  exact_check("lacunarity_coefficient", lacunarity_coefficient, "==", Rational(9, 320), "3rho*(4-1)=9rho=9/320"),
  exact_check("payment_23_B_power", payment_23_b_power, "==", Rational(2, 1), "(B^3R^3)^(2/3) has B power 2"),
  exact_check("payment_23_R_power", payment_23_r_power, "==", Rational(2, 1), "(B^3R^3)^(2/3) has R power 2"),
  exact_check("sqrt_log_L_power", sqrt_log_l_power, "==", one, "sqrt of a logarithm proportional to L^2 supplies L power 1"),
  exact_check("frontier_total_L_power", frontier_l_power, "==", one, "P^(2/3)sqrt(log P) has total L power 1"),
  exact_check("payment_to_target_ratio_B_power", ratio_b_power, "==", one, "(B^3R^3)/(B^2LR^2) has B power 1"),
  exact_check("payment_to_target_ratio_R_power", ratio_r_power, "==", one, "(B^3R^3)/(B^2LR^2) has R power 1"),
  exact_check("payment_to_target_ratio_L_power", ratio_l_power, "==", Rational(-1, 1), "(B^3R^3)/(B^2LR^2) has L power -1")
]

analytic_boundary = [
  "does not prove the periodic heat-semigroup or Brownian representation",
  "does not prove arcsin(s)<=2s, pi>3, Chebyshev, or the circle-distance implication",
  "does not prove the shear lower bound for the continuum heat equation",
  "does not prove the R0.74F family construction or zero-frame identities",
  "does not prove the inherited R0.74G complete-payment upper bound",
  "does not prove any upper bound for X_j or C_j",
  "does not verify literature novelty or publication priority",
  "does not prove regularity, singularity exclusion, global smoothness, or the Clay Millennium problem"
]

analytic_inputs = [
  "the selected periodic shear equals one on P_R and lies in [-1,1]",
  "the periodic heat semigroup is expectation under Z_t mod 2pi with Var(Z_t)=2t",
  "all complete-payment rows are nonnegative",
  "Version M and Version F coincide on the explicit family",
  "R0.74G supplies P_j<=C B_j^3 R_j^3 and B_j R_j^2 tends to 1/128"
]

exact_implications = [
  "The fifth-shell proof box has weight e^-8 and volume 64R^3.",
  "The rational Chebyshev ledger gives theta>=511/576>1/2.",
  "The cubic row coefficient based on theta>=1/2 is 8e^-8 B^3R^3.",
  "Matching payment gives log(P_j)/L_j^2 tending to 3rho and lacunarity coefficient 9rho.",
  "P_j^(2/3)sqrt(log P_j) has the monomial scale B_j^2 L_j R_j^2."
]

passed = checks.count { |item| item.fetch("pass") }
expected = {
  "analytic_boundary" => analytic_boundary,
  "analytic_inputs" => analytic_inputs,
  "checks" => checks,
  "exact_implications" => exact_implications,
  "result" => passed == checks.length ? "PASS" : "FAIL",
  "summary" => {"passed" => passed, "total" => checks.length}
}

frozen = JSON.parse(File.read(CERTIFICATE_PATH))
expected_leaves = flatten_leaves(expected)
frozen_leaves = flatten_leaves(frozen)
all_paths = (expected_leaves.keys | frozen_leaves.keys).sort
mismatches = all_paths.filter do |path|
  expected_leaves[path] != frozen_leaves[path]
end

puts "engine=Ruby Rational independent reconstruction"
puts "frozen_json_used_as_arithmetic_input=false"
puts "independentPassed=#{passed}"
puts "independentTotal=#{checks.length}"
puts "leafFieldComparisons=#{all_paths.length}"
puts "mismatchCount=#{mismatches.length}"
unless mismatches.empty?
  mismatches.first(20).each do |path|
    warn "#{path}: expected=#{expected_leaves[path].inspect} frozen=#{frozen_leaves[path].inspect}"
  end
end
puts "result=#{mismatches.empty? && passed == checks.length ? 'PASS' : 'FAIL'}"

exit(mismatches.empty? && passed == checks.length ? 0 : 1)
