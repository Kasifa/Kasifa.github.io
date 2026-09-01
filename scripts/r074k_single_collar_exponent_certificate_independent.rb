#!/usr/bin/env ruby
# Independent exact-rational reconstruction for the R0.74K certificate.
# This program does not read the frozen JSON or the Python producer.

lam = Rational(63, 32)
c_h = Rational(15, 16)
rho = Rational(1, 320)
c_gamma = Rational(8, 3969)
epsilon = Rational(1, 128)
zero = Rational(0, 1)
one = Rational(1, 1)

outer_edge = ->(m) { one / (lam * (2 ** (m - 1))) }
distance = ->(m) { c_h - outer_edge.call(m) }
gain = ->(m) { c_gamma * (one - Rational(1, 4 ** m)) }
sharp_cost = ->(m) { distance.call(m) ** 2 / 132 }
coarse_cost = ->(m) { distance.call(m) ** 2 / 262 }

d1 = distance.call(1)
d2 = distance.call(2)
d3 = distance.call(3)
g1 = gain.call(1)
g2 = gain.call(2)
g3 = gain.call(3)

d_epsilon = c_h - one / lam + epsilon
eta_epsilon = one / lam - epsilon
chord_square = one / lam ** 2 - (one / lam - epsilon) ** 2
nearest_boundary_wrong_margin = g1 - sharp_cost.call(1)
nearest_slab_wrong_margin = g1 - d_epsilon ** 2 / 132
sharp_m2_margin = sharp_cost.call(2) - g2
uniform_deep_margin = d2 ** 2 / 132 - c_gamma
coarse_m2_margin = coarse_cost.call(2) - g2
coarse_m3_margin = coarse_cost.call(3) - g3
padding_robust_m2_margin = (d2 - epsilon) ** 2 / 132 - g2
outer_one_shell_decay = 3 * c_gamma
outer_after_one_r_loss = outer_one_shell_decay - rho

prefactor_b = Rational(3, 1)
prefactor_gamma = Rational(-1, 1)
prefactor_r = Rational(-1, 1)
integral_gamma = Rational(1, 1)
integral_l = Rational(1, 1)
integral_r = Rational(5, 1)
combined_b = prefactor_b
combined_gamma = prefactor_gamma + integral_gamma
combined_l = integral_l
combined_r = prefactor_r + integral_r
target_b = Rational(2, 1)
target_l = Rational(1, 1)
target_r = Rational(2, 1)
beta_b = Rational(1, 1)
beta_r = Rational(2, 1)

checks = []
eq = ->(id, left, right) { checks << [id, left == right] }
gt = ->(id, left, right) { checks << [id, left > right] }
lt = ->(id, left, right) { checks << [id, left < right] }

eq.call("lambda", lam, Rational(63, 32))
eq.call("center_height", c_h, Rational(15, 16))
eq.call("radius_exponent", rho, Rational(1, 320))
eq.call("annular_exponent", c_gamma, Rational(8, 3969))
eq.call("annular_scale_identity", c_gamma * lam ** 2, Rational(1, 128))
eq.call("inverse_lambda", one / lam, Rational(32, 63))
eq.call("m1_distance", d1, Rational(433, 1008))
eq.call("m2_distance", d2, Rational(689, 1008))
eq.call("m3_distance", d3, Rational(817, 1008))
eq.call("m1_weight_gain", g1, Rational(2, 1323))
eq.call("m2_weight_gain", g2, Rational(5, 2646))
eq.call("m3_weight_gain", g3, Rational(1, 504))
eq.call("nearest_boundary_wrong_margin", nearest_boundary_wrong_margin, Rational(15263, 134120448))
gt.call("nearest_boundary_wrong_sign", nearest_boundary_wrong_margin, zero)
eq.call("epsilon", epsilon, Rational(1, 128))
eq.call("epsilon_slab_height", eta_epsilon, Rational(4033, 8064))
eq.call("epsilon_distance", d_epsilon, Rational(3527, 8064))
eq.call("chord_square", chord_square, Rational(8129, 1032192))
gt.call("chord_positive", chord_square, zero)
eq.call("nearest_slab_wrong_margin", nearest_slab_wrong_margin, Rational(536399, 8583708672))
gt.call("nearest_slab_wrong_sign", nearest_slab_wrong_margin, zero)
eq.call("sharp_m2_margin", sharp_m2_margin, Rational(221281, 134120448))
gt.call("sharp_m2_positive", sharp_m2_margin, zero)
eq.call("uniform_deep_margin", uniform_deep_margin, Rational(204385, 134120448))
gt.call("uniform_deep_positive", uniform_deep_margin, zero)
eq.call("padding_robust_m2_margin", padding_robust_m2_margin, Rational(13471441, 8583708672))
gt.call("padding_robust_m2_positive", padding_robust_m2_margin, zero)
eq.call("coarse_m2_margin", coarse_m2_margin, Rational(-28319, 266208768))
lt.call("coarse_m2_negative", coarse_m2_margin, zero)
eq.call("coarse_m3_margin", coarse_m3_margin, Rational(139297, 266208768))
gt.call("coarse_m3_positive", coarse_m3_margin, zero)
eq.call("outer_one_shell_decay", outer_one_shell_decay, Rational(8, 1323))
eq.call("outer_after_one_R_loss", outer_after_one_r_loss, Rational(1237, 423360))
gt.call("outer_after_one_R_loss_positive", outer_after_one_r_loss, zero)
eq.call("conditional_gamma_cancellation", combined_gamma, zero)
eq.call("conditional_B_power", combined_b, Rational(3, 1))
eq.call("conditional_L_power", combined_l, Rational(1, 1))
eq.call("conditional_R_power", combined_r, Rational(4, 1))
eq.call("beta_times_target_B_power", beta_b + target_b, combined_b)
eq.call("beta_times_target_L_power", target_l, combined_l)
eq.call("beta_times_target_R_power", beta_r + target_r, combined_r)

failed = checks.reject { |_, ok| ok }
puts "frozen_json_used_as_arithmetic_input=false"
puts "independentPassed=#{checks.length - failed.length}"
puts "independentTotal=#{checks.length}"
puts "mismatchCount=#{failed.length}"
puts "failedIds=#{failed.map(&:first).join(',')}"
puts "nearestPositiveVolumeWrongMargin=#{nearest_slab_wrong_margin.numerator}/#{nearest_slab_wrong_margin.denominator}"
puts "uniformDeepMargin=#{uniform_deep_margin.numerator}/#{uniform_deep_margin.denominator}"
puts "result=#{failed.empty? ? 'PASS' : 'FAIL'}"
exit(failed.empty? ? 0 : 1)
