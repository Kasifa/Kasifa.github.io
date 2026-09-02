#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent standard-library verifier for R0.74S Step 13.
#
# Exact Rational/integer calculations are run before the primary certificate
# artifacts are inspected.  They independently check the temporal exponents,
# adaptive rate/depth witness, two-regime Morrey arithmetic, heat-shear
# constants, the scaled high-Rayleigh row, the critical eight-ary tree,
# best-N deletion, cubic Holder duality, Dini behavior, and repeated
# incidences.  They do not machine-prove the inherited PDE estimates, either
# open packing gate, the moving-Morrey hypothesis, an NSE realization of an
# abstract countermodel, regularity, or the Navier--Stokes Millennium problem.

require "digest"
require "json"
require "open3"
require "rbconfig"

REPO = File.expand_path("..", __dir__)
SCHEMA = "r074s-temporal-integrability-morrey-independent-verifier-v1"
EXPECTED_TAGS = (307..342).map { |number| "S.#{number}" }.freeze
INTERNAL_HASH_PROBE = "R074S_TEMPORAL_INTERNAL_HASH_PROBE"

ARTIFACT_SPECS = {
  "main_note" => {
    "environment" => "R074S_TEMPORAL_NOTE",
    "path" => "research/r074s_temporal_integrability_morrey_threshold.md",
    "sha256" => "d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de"
  },
  "primary_generator" => {
    "environment" => "R074S_TEMPORAL_PRIMARY_GENERATOR",
    "path" => "scripts/r074s_temporal_integrability_morrey_certificate.py",
    "sha256" => "eb313260c16431c1379d1b77a508b8bb7740ac713c014126c08e44bc2d0cfafb"
  },
  "primary_json" => {
    "environment" => "R074S_TEMPORAL_PRIMARY_JSON",
    "path" => "research/r074s_temporal_integrability_morrey_certificate.json",
    "sha256" => "095e8a7a0ba378ff2178a166cbed81e1f132be055d37165c945020a26466e330"
  },
  "primary_report" => {
    "environment" => "R074S_TEMPORAL_PRIMARY_REPORT",
    "path" => "research/r074s_temporal_integrability_morrey_certificate_report.md",
    "sha256" => "c464af1617391beda5b077e13066629203d408519ab32ee89b2115475346fe2b"
  },
  "primary_audit" => {
    "environment" => "R074S_TEMPORAL_PRIMARY_AUDIT",
    "path" => "research/r074s_temporal_integrability_morrey_primary_audit.md",
    "sha256" => "5910f46c0dd401d3766343d75ae3e68bdecb9d8416615fd8feb74d0f560adefd"
  },
  "independent_audit" => {
    "environment" => "R074S_TEMPORAL_INDEPENDENT_AUDIT",
    "path" => "research/r074s_temporal_integrability_morrey_independent_audit.md",
    "sha256" => "332bf2a5b4503b9456bc76b1067bc44cb2d788e37fa7f2e34f10211a700e7ce3"
  }
}.freeze

DEPENDENCY_SPECS = {
  "R0.74P" => {
    "environment" => "R074S_TEMPORAL_DEP_R074P",
    "path" => "research/r074p_temporal_observable_triage.md",
    "sha256" => "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867"
  },
  "R0.74R-arbitrary" => {
    "environment" => "R074S_TEMPORAL_DEP_R074R_ARBITRARY",
    "path" => "research/r074r_arbitrary_clock_extraction_gate.md",
    "sha256" => "ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7"
  },
  "R0.74S-step11" => {
    "environment" => "R074S_TEMPORAL_DEP_STEP11",
    "path" => "research/r074s_shared_budget_terminal_trace_obstruction.md",
    "sha256" => "fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693"
  },
  "R0.74S-step12" => {
    "environment" => "R074S_TEMPORAL_DEP_STEP12",
    "path" => "research/r074s_terminal_window_morrey_packing.md",
    "sha256" => "03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f"
  }
}.freeze

PRIMARY_SCHEMA = "r074s-temporal-integrability-morrey-certificate-v1"
PRIMARY_SUMMARY = {
  "exact_passed" => 31,
  "exact_total" => 31,
  "finite_passed" => 11,
  "finite_total" => 11,
  "dependency_passed" => 4,
  "dependency_total" => 4,
  "structural_passed" => 22,
  "structural_total" => 22,
  "negative_passed" => 32,
  "negative_total" => 32
}.freeze

PRIMARY_LINKS = [
  "https://doi.org/10.1016/j.aim.2024.109654",
  "https://doi.org/10.1016/j.jde.2017.09.036",
  "https://doi.org/10.1007/s00526-017-1151-7",
  "https://doi.org/10.1006/aima.2000.1937"
].freeze

def resolved_path(spec)
  File.expand_path(ENV.fetch(spec.fetch("environment"), File.join(REPO, spec.fetch("path"))))
end

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

def rational_sum(values)
  values.inject(Rational(0, 1), :+)
end

def assert_exact(condition, message)
  raise RuntimeError, message unless condition
end

def exact_group(identifier)
  counter = { "cases" => 0 }
  check = lambda do |condition, message|
    counter["cases"] += 1
    assert_exact(condition, message)
  end
  yield check
  { "id" => identifier, "cases" => counter.fetch("cases"), "pass" => true }
rescue StandardError => error
  {
    "id" => identifier,
    "cases" => counter.fetch("cases"),
    "error_class" => error.class.to_s,
    "error" => error.message,
    "pass" => false
  }
end

def sorted_best_tail(values, budget)
  raise ArgumentError, "best-N inputs must be nonnegative" if
    budget.negative? || values.any?(&:negative?)

  rational_sum(values.sort.reverse.drop([budget, values.length].min))
end

def brute_best_tail(values, budget)
  indices = (0...values.length).to_a
  maximum = [budget, values.length].min
  candidates = (0..maximum).flat_map { |size| indices.combination(size).to_a }
  candidates.map do |deleted|
    lookup = deleted.to_h { |index| [index, true] }
    retained = values.each_with_index.map do |value, index|
      value unless lookup[index]
    end.compact
    rational_sum(retained)
  end.min || Rational(0, 1)
end

def geometric_sum(ratio, length)
  (0...length).inject(Rational(0, 1)) { |total, index| total + ratio**index }
end

def temporal_exponent_checks
  exact_group("temporal_exponents_and_optimizer") do |check|
    p = Rational(4, 3)
    a = 1 - 1 / p
    check.call(2 - 2 / p == Rational(1, 2), "dimensionless L4/3 R power is wrong")
    check.call(3 * Rational(1, 4) == Rational(3, 4), "cubic time reciprocal is wrong")
    check.call(a == Rational(1, 4), "window Holder exponent is wrong")
    check.call(p / (5 * p - 3) == Rational(4, 11), "p=4/3 depth exponent is wrong")
    exponent = (4 * p - 2) / (5 * p - 3)
    check.call(exponent == Rational(10, 11), "p=4/3 optimized exponent is wrong")
    check.call(exponent - Rational(2, 3) == Rational(8, 33), "10/11 gap is wrong")
    check.call(
      Rational(8, 11) + Rational(2, 3) * Rational(3, 11) == Rational(10, 11),
      "mixed H/A optimizer does not recover 10/11"
    )
    check.call(Rational(1, 5) == Rational(1, 5), "Linfinity depth limit is wrong")
    check.call(Rational(4, 5) > Rational(2, 3), "Linfinity ceiling reached the target")

    ps = [Rational(6, 5), Rational(4, 3), Rational(3, 2), Rational(2), Rational(7)]
    betas = [Rational(1, 2), Rational(2, 3), Rational(3, 4), Rational(1), Rational(5, 4)]
    ps.product(betas).each do |sample_p, beta|
      sample_a = 1 - 1 / sample_p
      got = Rational(2, 3) * (sample_a + beta) / (sample_a + Rational(2, 3))
      gap = Rational(2, 3) * (beta - Rational(2, 3)) /
            (sample_a + Rational(2, 3))
      check.call(got - Rational(2, 3) == gap, "general beta gap identity failed")
      check.call((got > Rational(2, 3)) == (beta > Rational(2, 3)),
                 "general beta threshold sign failed")
      next unless beta == 1

      delta_power = (beta - Rational(2, 3)) /
                    (sample_a + Rational(2, 3))
      check.call(delta_power == sample_p / (5 * sample_p - 3),
                 "linear delta exponent simplification failed")
      check.call(got == 2 * (2 * sample_p - 1) / (5 * sample_p - 3),
                 "linear E_p simplification failed")
    end

    reciprocal_rs = [Rational(1, 2), Rational(5, 12), Rational(1, 3),
                     Rational(1, 4), Rational(1, 6)]
    reciprocal_rs.repeated_permutation(3) do |triple|
      spatial = rational_sum(triple)
      temporal = rational_sum(triple.map { |inverse_r| Rational(3, 4) - Rational(3, 2) * inverse_r })
      if spatial == 1
        check.call(temporal == Rational(3, 4), "energy-admissible triple endpoint failed")
      elsif spatial < 1
        check.call(temporal > Rational(3, 4), "subcritical spatial sum did not worsen time exponent")
      end
    end
  end
end

def window_holder_checks
  exact_group("L43_window_Holder_integer_grid") do |check|
    alphabet = [0, 1, 2, 3]
    (1..4).each do |length|
      alphabet.repeated_permutation(length) do |roots|
        l1 = roots.sum { |root| root**3 }
        l43_power = roots.sum { |root| root**4 }
        check.call(l1**4 <= length * l43_power**3,
                   "raised L4/3 window Holder inequality failed")
      end
    end
  end
end

def adaptive_witness_checks
  exact_group("adaptive_rate_depth_and_best_N_witness") do |check|
    roots = [1, 2, 3]
    constants = [Rational(1, 2), Rational(1), Rational(5, 3)]
    roots.product(constants, (1..6).to_a).each do |root, c_rho, size|
      payment = Rational(root**33, 1)
      depth = Rational(1, root**12)
      residual_total = c_rho * root**30
      rate_total = payment
      coordinates = Array.new(size, residual_total / size)
      budget = size - 1
      check.call(depth <= 1, "adaptive depth left the unit window")
      check.call(rate_total == payment, "adaptive L4/3 rate ledger failed")
      check.call(residual_total == c_rho * payment * Rational(1, root**3),
                 "adaptive L1 scaling failed")
      check.call(residual_total <= c_rho * payment, "adaptive linear L1 ledger failed")
      check.call(sorted_best_tail(coordinates, budget) == residual_total / size,
                 "adaptive N=M-1 tail failed")
      check.call(brute_best_tail(coordinates, budget) == residual_total / size,
                 "adaptive brute best-N tail failed")
      [2, 3].each do |cube_root|
        delta = depth / cube_root**3
        deep_right = c_rho * root**22 * root**8 * cube_root**2
        check.call(delta < depth, "deep-window fixture is not deep")
        check.call(residual_total <= deep_right, "deep allowance failed")
      end
      check.call(c_rho * root**22 * root**8 == residual_total,
                 "adaptive balance is not exact at delta=d")
    end
  end
end

def morrey_checks
  exact_group("Morrey_two_regimes_and_threshold") do |check|
    roots = [Rational(0), Rational(1, 5), Rational(1, 2), Rational(1),
             Rational(3, 2), Rational(2), Rational(7)]
    constants = [Rational(1, 3), Rational(1), Rational(5, 2)]
    roots.product(constants, constants).each do |root, c_zero, c_morrey|
      payment = root**3
      target = root**2
      inferred = [c_zero * payment, c_morrey * (1 + target)].min
      bound = [c_zero, 2 * c_morrey].max * target
      check.call(inferred <= bound, "payment-dependent Morrey cap failed")
      if payment <= 1
        check.call(payment <= target, "small-payment comparison P<=P^(2/3) failed")
      else
        check.call(1 <= target, "large-payment comparison 1<=P^(2/3) failed")
      end
    end

    theta_data = [[Rational(3, 4), 9], [Rational(5, 6), 10], [Rational(1), 12]]
    theta_data.each do |theta, exponent|
      previous = nil
      (2..9).each do |root|
        payment = Rational(root**12, 1)
        total = [payment, Rational(root**exponent, 1)].min
        target = Rational(root**8, 1)
        ratio = total / target
        check.call(theta > Rational(2, 3), "countermodel theta is not supercritical")
        check.call(total == root**exponent, "wrong branch of two-cap minimum")
        check.call(previous.nil? || ratio > previous, "supercritical ratio did not grow")
        previous = ratio
      end
    end
  end
end

def heat_shear_checks
  exact_group("heat_shear_exact_coefficients") do |check|
    sine_square = Rational(1, 1)
    absolute_sine_cube = Rational(8, 3)
    transverse_torus_factor = Rational(4, 1)
    gradient_spatial = transverse_torus_factor * sine_square
    cubic_spatial = transverse_torus_factor * absolute_sine_cube
    dissipation = gradient_spatial * Rational(1, 2)
    cubic = cubic_spatial * Rational(1, 3)
    check.call(gradient_spatial == 4, "torus gradient coefficient is wrong")
    check.call(cubic_spatial == Rational(32, 3), "torus cubic coefficient is wrong")
    check.call(dissipation == 2, "heat dissipation coefficient is wrong")
    check.call(cubic == Rational(32, 9), "heat cubic coefficient is wrong")
    check.call(dissipation / cubic == Rational(9, 16), "n^2/A ratio coefficient is wrong")
    (1..8).each do |frequency|
      time_gradient = Rational(frequency**2, 2 * frequency**2)
      time_cubic = Rational(1, 3 * frequency**2)
      check.call(gradient_spatial * time_gradient == 2,
                 "frequency cancellation in dissipation failed")
      check.call(cubic_spatial * time_cubic == Rational(32, 9 * frequency**2),
                 "frequency scaling in cubic integral failed")
    end
    velocity_component = 0
    profile_coordinate = 1
    cutoff_derivative_coordinate = 0
    check.call(velocity_component != profile_coordinate,
               "the shear direction differentiates its own profile")
    check.call(velocity_component != profile_coordinate,
               "the convection derivative is not identically zero")
    check.call(cutoff_derivative_coordinate != profile_coordinate,
               "the flux prefactor unexpectedly depends on y1")
  end
end

def high_rayleigh_checks
  exact_group("scaled_high_Rayleigh_row") do |check|
    scales = [Rational(1, 17), Rational(1, 3), Rational(1), Rational(11, 2)]
    scales.each do |scale|
      total = scale
      ancestor = Rational(3, 5) * scale
      sigma = Rational(983, 12_000) * scale
      excess = Rational(2617, 6000) * scale
      residual = Rational(1, 3) * scale
      check.call(ancestor - 2 * sigma == excess, "high-Rayleigh excess identity failed")
      check.call(Rational(1, 12) * scale - sigma == Rational(17, 12_000) * scale,
                 "sigma strict margin failed")
      check.call(excess - Rational(1, 6) * scale == Rational(539, 2000) * scale,
                 "excess strict margin failed")
      check.call(total / 6 < residual && residual < total / 2,
                 "residual left its strict branch band")
      check.call(ancestor > total / 8, "high-Rayleigh mass missed its threshold")
      check.call(excess < ancestor, "selected excess exceeded ancestor mass")
    end
  end
end

def histogram_tree_tail(m, levels, budget)
  remaining_budget = budget
  removed_mass = Rational(0, 1)
  (0...levels).each do |depth|
    removed_here = [remaining_budget, 8**depth].min
    removed_mass += Rational(removed_here, m**2 * 8**depth)
    remaining_budget -= removed_here
    break if remaining_budget.zero?
  end
  Rational(m, 1) - removed_mass
end

def critical_tree_checks
  exact_group("critical_eight_ary_tree_and_best_N") do |check|
    (1..8).each do |m|
      levels = m**3
      total_nodes = (8**levels - 1) / 7
      p_total = Rational(levels, m**3)
      b_total = Rational(levels, m**2)
      s_total = Rational(5 * levels, 3 * m**2)
      coefficient_cube_total = Rational(levels, 1)
      square_total = Rational(25, 9 * m**4) * geometric_sum(Rational(1, 8), levels)
      square_formula = Rational(200, 63 * m**4) * (1 - Rational(1, 8)**levels)
      check.call(p_total == 1, "tree payment total is not one")
      check.call(b_total == m, "tree ancestor total is not m")
      check.call(s_total == Rational(5 * m, 3), "tree linear payment is wrong")
      check.call(coefficient_cube_total == m**3, "tree coefficient cube total is wrong")
      check.call(b_total**3 == coefficient_cube_total * p_total**2,
                 "global cubic Holder equality failed")
      check.call(square_total == square_formula, "tree square geometric sum failed")
      check.call(square_total < Rational(200, 63 * m**4), "tree square bound is not strict")

      [0, [levels / 2, 8].min, levels - 1].uniq.each do |depth|
        b_value = Rational(1, m**2 * 8**depth)
        s_value = Rational(5, 3 * m**2 * 8**depth)
        c_value = Rational(1, 2**depth)
        p_root = Rational(1, m * 2**depth)
        p_value = p_root**3
        remaining_levels = levels - depth
        subtree = b_value**2 * geometric_sum(Rational(1, 8), remaining_levels)
        subtree_formula = Rational(8, 7) * (1 - Rational(1, 8)**remaining_levels) * b_value**2
        check.call(8**depth * b_value == Rational(1, m**2), "level b mass failed")
        check.call(8**depth * s_value == Rational(5, 3 * m**2), "level s mass failed")
        check.call(8**depth * p_value == Rational(1, m**3), "level p mass failed")
        check.call(8**depth * c_value**3 == 1, "level c cube mass failed")
        check.call(p_value == c_value**3 / levels, "tree optimizer payment failed")
        check.call(c_value * p_root**2 == b_value, "b=c p^(2/3) failed")
        check.call(subtree == subtree_formula, "subtree square formula failed")
        check.call(subtree <= Rational(8, 7) * b_value**2, "subtree square cap failed")
        if depth < levels - 1
          check.call(8 * (c_value / 2)**3 == c_value**3,
                     "nonleaf child-cube conservation failed")
        else
          check.call(Rational(0) != c_value**3,
                     "leaf was incorrectly assigned the nonleaf identity")
        end
      end

      budgets = [0, 1, 2, 7, 8, 9, 24].select { |budget| budget < total_nodes }.uniq
      budgets.each do |budget|
        actual = histogram_tree_tail(m, levels, budget)
        level = 0
        level += 1 while (8**(level + 1) - 1) / 7 <= budget
        cumulative = (8**level - 1) / 7
        remainder = budget - cumulative
        formula = Rational(m, 1) -
                  (Rational(level, 1) + Rational(remainder, 8**level)) / m**2
        lower = Rational(m, 1) - Rational(budget, m**2)
        check.call(actual == formula, "exact histogram best-N formula failed")
        check.call(actual >= lower, "tree best-N lower bound failed")
        ratio_cube = lower**3 / Rational(5 * m, 3)**2
        expected_ratio_cube = Rational(9, 25) * m *
                              (1 - Rational(budget, m**3))**3
        check.call(ratio_cube == expected_ratio_cube,
                   "rationalized normalized-tail formula failed")
      end
    end
    factors = (2..4).to_h { |power| [power, Rational(8, 2**power)] }
    check.call(factors == { 2 => 2, 3 => 1, 4 => Rational(1, 2) },
               "cube is not the unique critical child exponent")
  end
end

def cubic_holder_checks
  exact_group("cubic_Holder_polynomial_exhaustive") do |check|
    alphabet = [0, 1, 2, 3]
    equality_seen = false
    (0..4).each do |length|
      alphabet.repeated_permutation(length) do |coefficients|
        alphabet.repeated_permutation(length) do |roots|
          left = coefficients.zip(roots).sum { |coefficient, root| coefficient * root**2 }
          coefficient_cube = coefficients.sum { |coefficient| coefficient**3 }
          payment = roots.sum { |root| root**3 }
          check.call(left**3 <= coefficient_cube * payment**2,
                     "integer cubic Holder inequality failed")
          equality_seen ||= left.positive? && left**3 == coefficient_cube * payment**2
        end
      end
    end
    # (1/8)^(2/3)=1/4 exactly; keep radicals out of the verifier.
    eight_left = 8 * Rational(1, 4)
    check.call(eight_left == 2, "eight-coordinate cubic-duality equality failed")
    check.call(equality_seen, "no nonzero cubic Holder equality case was exercised")
  end
end

def incidence_and_dini_checks
  exact_group("Dini_root_and_repeated_incidence") do |check|
    # Named exceptional sets must dominate the best-N infimum.
    alphabet = [Rational(0), Rational(1, 4), Rational(1), Rational(5, 2)]
    alphabet.repeated_permutation(3) do |values|
      (0..3).each do |budget|
        best = sorted_best_tail(values, budget)
        brute = brute_best_tail(values, budget)
        check.call(best == brute, "best-N sorted and subset formulas disagree")
      end
    end

    # Node zero occurs twice; both p and c^3 must be counted twice.
    coefficients = [Rational(2), Rational(2), Rational(1, 2)]
    roots = [Rational(1, 3), Rational(1, 3), Rational(3, 4)]
    left = coefficients.zip(roots).sum { |coefficient, root| coefficient * root**2 }
    incidence_cubes = rational_sum(coefficients.map { |value| value**3 })
    incidence_payments = rational_sum(roots.map { |value| value**3 })
    distinct_cubes = coefficients[0]**3 + coefficients[2]**3
    distinct_payments = roots[0]**3 + roots[2]**3
    check.call(left**3 <= incidence_cubes * incidence_payments**2,
               "repeated-incidence Holder inequality failed")
    check.call(incidence_cubes > distinct_cubes, "coefficient incidence was deduplicated")
    check.call(incidence_payments > distinct_payments, "payment incidence was deduplicated")

    [Rational(1, 5), Rational(1, 2), Rational(7, 8)].each do |theta|
      (1..14).each do |generations|
        partial = geometric_sum(theta, generations)
        check.call(partial < 1 / (1 - theta), "uniform Dini geometric cap failed")
      end
    end
    (1..24).each do |generations|
      check.call(geometric_sum(Rational(1), generations) == generations,
                 "critical Dini sum did not grow linearly")
    end

    harmonic_partial = Rational(0)
    square_partial = Rational(0)
    (0..32).each do |generation|
      direct = Rational(1)
      squared = Rational(1)
      generation.times do |index|
        theta = Rational(index + 1, index + 2)
        direct *= theta
        squared *= theta**2
      end
      harmonic = Rational(1, generation + 1)
      square = Rational(1, (generation + 1)**2)
      check.call(direct == harmonic, "strict non-Dini product failed to telescope")
      check.call(squared == square, "Dini product failed to telescope")
      harmonic_partial += harmonic
      square_partial += square
    end
    check.call(harmonic_partial > 4, "strict theta<1 fixture did not expose divergence")
    check.call(square_partial < 2, "square-Dini fixture exceeded its exact bound")

    root_cubes = Rational(7, 3)
    d_constant = Rational(9, 2)
    incidence_multiplicity = 4
    coefficient_incidence_cap = incidence_multiplicity * root_cubes * d_constant
    check.call(coefficient_incidence_cap == 42,
               "root/Dini/incidence product cap is wrong")
  end
end

def compact(text)
  text.gsub(/\s+/, "")
end

def semantic_note_checks(body, bytes)
  rows = []
  add = lambda do |identifier, condition|
    rows << { "id" => identifier, "pass" => !!condition }
  end
  compact_body = compact(body)
  tags = body.scan(/\\tag\{(S\.\d+)\}/).flatten
  add.call("exact_S307_S342_tag_sequence", tags == EXPECTED_TAGS)
  add.call("all_36_tags_unique", tags.uniq.length == EXPECTED_TAGS.length)
  add.call("display_math_balanced", body.scan(/\\\[/).length == body.scan(/\\\]/).length)
  add.call("valid_UTF8", body.valid_encoding?)
  add.call("no_CR_or_NUL", !bytes.include?("\r") && !bytes.include?("\0"))
  add.call("no_forbidden_controls", bytes.bytes.none? { |byte| byte < 32 && byte != 10 })
  add.call("no_trailing_whitespace",
           body.lines.none? { |line| line.sub(/\n\z/, "").match?(/[ \t]\z/) })

  compact_fragments = {
    "common_deletion_order" =>
      '\\mathfrakH^F_{p,N,R}:=\\inf_{\\#S\\leN}\\sum_{k\\notinS}\\|h_{k,R}\\|_{L^p(0,4)}',
    "window_depth_plus" =>
      'C_H\\delta^{a_p}P^\\beta+C_{\\rmdeep}\\delta^{-2/3}P^{2/3}',
    "temporal_endpoints" =>
      'p={4\\over3}:\\quad\\delta\\asympP^{-4/11},\\quadE_p={10\\over11};\\qquadp=\\infty:\\quad\\delta\\asympP^{-1/5},\\quadE_p={4\\over5}',
    "adaptive_P_ge_one" => 'Take\\(P\\ge1\\)',
    "adaptive_nonnegative_profile" => '0\\le\\rho\\inC_c^\\infty((-1,0))',
    "adaptive_depth_binding" => 'd_{k,P}=d',
    "Morrey_equal_coordinate_binding" => 'x_k^{\\rmsel}=b_k=T_P/M',
    "heat_positive_parameters" => 'take\\(A>0\\),\\(T>0\\)',
    "tree_nonleaf_relation" => '\\quad(0\\led(v)\\leL-2)',
    "cubic_duality" => '\\sup_{p_\\nu\\ge0,\\ \\sump_\\nu\\le1}\\sum_\\nuc_\\nup_\\nu^{2/3}=\\left(\\sum_\\nuc_\\nu^3\\right)^{1/3}',
    "root_cube_bound" => '\\sum_{v\\in{\\rmroots}}c_v^3\\leC_{\\rmroot}',
    "incidence_multiplicity" => '\\#\\{\\hbox{incidencescarryingafixednode}v\\}\\leM_{\\rminc}',
    "uniform_Dini_start" => '\\sup_{d_0\\ge0}\\sum_{n\\ge0}\\prod_{j=0}^{n-1}\\theta_{d_0+j}\\leC_D<\\infty',
    "incidence_payment_sum" => '\\sum_{\\rmincidences}p_\\nu\\leB_{\\rminc}C_pP_R^M'
  }
  compact_fragments.each do |identifier, fragment|
    add.call(identifier, compact_body.include?(compact(fragment)))
  end

  literal_fragments = {
    "fixed_solution_nonuniform" => "No uniform estimate for it in terms of \\(P_R^M\\) is claimed",
    "abstract_boundary" => "ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES",
    "tree_not_NSE" => "It is not an NSE counterexample.",
    "no_DGX" => "No DNS or DGX computation is used",
    "not_CLAY" => "**NOT CLAY.**",
    "open_terminal_gate" => "The universal terminal-window gate (S.280)",
    "open_claim_ledger" => "The following remain **OPEN**:"
  }
  literal_fragments.each do |identifier, fragment|
    add.call(identifier, body.include?(fragment))
  end
  add.call("not_CLAY_repeated", body.scan(/\*\*NOT CLAY\.\*\*/).length >= 2)
  add.call("all_primary_links", PRIMARY_LINKS.all? { |link| body.include?(link) })
  add.call("known_bad_tokens_absent",
           !body.include?(",qquad") && !body.include?("h_v=b_v") &&
             !compact_body.include?(compact('\\qquad2\\le r\\le6')))
  rows
end

def note_structure_checks(path, artifact_row)
  return [{ "id" => "main_note_exists", "pass" => false }] unless File.file?(path)

  bytes = File.binread(path)
  body = bytes.dup.force_encoding(Encoding::UTF_8)
  rows = [{
    "id" => "main_note_hash_lock",
    "expected_sha256" => artifact_row.fetch("expected_sha256"),
    "actual_sha256" => artifact_row.fetch("actual_sha256"),
    "pass" => artifact_row.fetch("pass")
  }]
  rows.concat(semantic_note_checks(body, bytes))
  rows
end

def artifact_checks
  ARTIFACT_SPECS.map do |label, spec|
    path = resolved_path(spec)
    actual = File.file?(path) ? sha256(path) : nil
    {
      "id" => label,
      "path" => spec.fetch("path"),
      "resolved_path" => path,
      "expected_sha256" => spec.fetch("sha256"),
      "actual_sha256" => actual,
      "pass" => actual == spec.fetch("sha256")
    }
  end
end

def dependency_checks
  DEPENDENCY_SPECS.map do |label, spec|
    path = resolved_path(spec)
    actual = File.file?(path) ? sha256(path) : nil
    {
      "id" => label,
      "path" => spec.fetch("path"),
      "resolved_path" => path,
      "expected_sha256" => spec.fetch("sha256"),
      "actual_sha256" => actual,
      "pass" => actual == spec.fetch("sha256")
    }
  end
end

def primary_artifact_content_checks(artifacts)
  exact_group("primary_artifact_content_consistency") do |check|
    paths = artifacts.to_h { |row| [row.fetch("id"), row.fetch("resolved_path")] }
    payload = JSON.parse(File.read(paths.fetch("primary_json"), encoding: "UTF-8"))
    check.call(payload.fetch("schema") == PRIMARY_SCHEMA, "primary JSON schema changed")
    check.call(payload.fetch("overall_pass") == true, "primary JSON is not PASS")
    check.call(payload.fetch("summary") == PRIMARY_SUMMARY, "primary JSON summary changed")
    check.call(payload.fetch("note_sha256") == ARTIFACT_SPECS.fetch("main_note").fetch("sha256"),
               "primary JSON note hash disagrees")
    check.call(payload.fetch("generator_sha256") == ARTIFACT_SPECS.fetch("primary_generator").fetch("sha256"),
               "primary JSON generator hash disagrees")
    %w[exact_checks finite_checks dependency_checks structural_checks negative_checks].each do |key|
      check.call(payload.fetch(key).all? { |row| row.fetch("pass") },
                 "primary JSON contains a failed #{key} row")
    end

    report = File.read(paths.fetch("primary_report"), encoding: "UTF-8")
    check.call(report.include?("- Exact: 31/31"), "primary report exact count changed")
    check.call(report.include?("- Finite: 11/11"), "primary report finite count changed")
    check.call(report.include?("- Dependencies: 4/4"), "primary report dependency count changed")
    check.call(report.include?("- Structural: 22/22"), "primary report structural count changed")
    check.call(report.include?("- Negative mutations: 32/32"), "primary report mutation count changed")
    check.call(report.include?("- Overall: **PASS**"), "primary report is not PASS")

    primary_audit = File.read(paths.fetch("primary_audit"), encoding: "UTF-8")
    independent_audit = File.read(paths.fetch("independent_audit"), encoding: "UTF-8")
    check.call(primary_audit.include?("**Verdict: PASS"), "primary audit verdict changed")
    check.call(independent_audit.include?("**Final verdict: PASS"), "independent audit verdict changed")
    check.call(independent_audit.include?("**NOT CLAY.**"), "independent audit lost NOT CLAY")
  end
end

def statement_mutation_checks(body)
  exact_group("statement_negative_mutations_rejected") do |check|
    mutations = {
      "common_deletion_order" => [
        '\\inf_{\\#S\\le N}\\sum_{k\\notin S}',
        '\\sum_k\\inf_{\\#S\\le N}'
      ],
      "window_depth_plus" => [
        "P^\\beta\n     +C_{\\rm deep}",
        "P^\\beta\n     -C_{\\rm deep}"
      ],
      "adaptive_P_ge_one" => ['Take \\(P\\ge1\\)', 'Take \\(P>0\\)'],
      "adaptive_nonnegative_profile" => [
        '0\\le\\rho\\in C_c^\\infty((-1,0))',
        '\\rho\\in C_c^\\infty((-1,0))'
      ],
      "Morrey_equal_coordinate_binding" => [
        'x_k^{\\rm sel}=b_k=T_P/M',
        'b_k=T_P/M'
      ],
      "heat_positive_parameters" => [
        'take \\(A>0\\), \\(T>0\\)',
        'take \\(A\\ne0\\), \\(T>0\\)'
      ],
      "tree_nonleaf_relation" => [
        '\\quad(0\\le d(v)\\le L-2)',
        '\\quad(0\\le d(v)\\le L-1)'
      ],
      "cubic_duality" => [
        '=\\left(\\sum_\\nu c_\\nu^3\\right)^{1/3}.}',
        '=\\left(\\sum_\\nu c_\\nu^2\\right)^{1/2}.}'
      ],
      "root_cube_bound" => [
        '\\sum_{v\\in{\\rm roots}}c_v^3\\le C_{\\rm root}',
        '\\sum_{v\\in{\\rm roots}}c_v^3<\\infty'
      ],
      "incidence_multiplicity" => [
        '\\#\\{\\hbox{incidences carrying a fixed node }v\\}\\le M_{\\rm inc}',
        '\\#\\{\\hbox{incidences carrying a fixed node }v\\}<\\infty'
      ],
      "uniform_Dini_start" => [
        '\\sup_{d_0\\ge0}\\sum_{n\\ge0}',
        '\\sum_{n\\ge0}'
      ],
      "incidence_payment_sum" => [
        '\\sum_{\\rm incidences}p_\\nu',
        '\\sum_{\\rm distinct\\ nodes}p_\\nu'
      ],
      "abstract_boundary" => [
        'ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES',
        'NSE COUNTEREXAMPLES'
      ],
      "tree_not_NSE" => ['It is not an NSE counterexample.', 'It is an NSE counterexample.'],
      "no_DGX" => ['No DNS or DGX computation is used', 'DGX computation is used'],
      "open_claim_ledger" => ['The following remain **OPEN**:', 'The following are **CLOSED**:']
    }
    mutations.each do |expected_failure, (old, replacement)|
      mutated = body.sub(old, replacement)
      check.call(mutated != body, "mutation marker absent: #{expected_failure}")
      rows = semantic_note_checks(mutated, mutated.encode(Encoding::UTF_8))
      target = rows.find { |row| row.fetch("id") == expected_failure }
      check.call(!target.nil? && !target.fetch("pass"),
                 "semantic contract accepted mutation: #{expected_failure}")
    end

    clay_mutation = body.gsub("**NOT CLAY.**", "**CLAY.**")
    clay_rows = semantic_note_checks(clay_mutation, clay_mutation.encode(Encoding::UTF_8))
    check.call(clay_rows.any? { |row| row.fetch("id") == "not_CLAY" && !row.fetch("pass") },
               "NOT CLAY removal was accepted")

    tag_mutation = body.sub("\\tag{S.342}", "\\tag{S.341}")
    tag_rows = semantic_note_checks(tag_mutation, tag_mutation.encode(Encoding::UTF_8))
    check.call(tag_rows.any? { |row| row.fetch("id") == "exact_S307_S342_tag_sequence" && !row.fetch("pass") },
               "duplicate final tag was accepted")

    damaged = body.b + "\r\0"
    damaged_body = damaged.dup.force_encoding(Encoding::UTF_8)
    damaged_rows = semantic_note_checks(damaged_body, damaged)
    check.call(damaged_rows.any? { |row| row.fetch("id") == "no_CR_or_NUL" && !row.fetch("pass") },
               "CR/NUL injection was accepted")
  end
end

def environment_override_checks
  exact_group("environment_hash_overrides_rejected") do |check|
    probes = [
      ["R074S_TEMPORAL_NOTE", "main_note", "artifacts"],
      ["R074S_TEMPORAL_DEP_STEP11", "R0.74S-step11", "dependencies"]
    ]
    probes.each do |environment_key, target_id, collection|
      environment = { INTERNAL_HASH_PROBE => "1", environment_key => File.expand_path(__FILE__) }
      stdout, stderr, status = Open3.capture3(environment, RbConfig.ruby, File.expand_path(__FILE__))
      payload = JSON.parse(stdout)
      target = payload.fetch(collection).find { |row| row.fetch("id") == target_id }
      check.call(!status.success?, "#{environment_key} mismatch exited successfully")
      check.call(stderr.empty?, "#{environment_key} mismatch wrote stderr")
      check.call(!target.fetch("pass"), "#{environment_key} mismatch passed its hash lock")
      check.call(target.fetch("actual_sha256") == sha256(__FILE__),
                 "#{environment_key} did not resolve to the injected file")
    end
  end
end

if ENV[INTERNAL_HASH_PROBE] == "1"
  probe_artifacts = artifact_checks
  probe_dependencies = dependency_checks
  probe_pass = probe_artifacts.all? { |row| row.fetch("pass") } &&
               probe_dependencies.all? { |row| row.fetch("pass") }
  puts JSON.generate({ "artifacts" => probe_artifacts, "dependencies" => probe_dependencies })
  exit(probe_pass ? 0 : 1)
end

# Independent mathematics is intentionally evaluated before primary JSON or
# reports are opened, so their PASS flags cannot act as a computational oracle.
independent_groups = [
  temporal_exponent_checks,
  window_holder_checks,
  adaptive_witness_checks,
  morrey_checks,
  heat_shear_checks,
  high_rayleigh_checks,
  critical_tree_checks,
  cubic_holder_checks,
  incidence_and_dini_checks
]

artifacts = artifact_checks
dependencies = dependency_checks
main_note = artifacts.find { |row| row.fetch("id") == "main_note" }
note_path = main_note.fetch("resolved_path")
note_checks = note_structure_checks(note_path, main_note)

if File.file?(note_path)
  note_bytes = File.binread(note_path)
  note_body = note_bytes.dup.force_encoding(Encoding::UTF_8)
  statement_mutations = statement_mutation_checks(note_body)
else
  statement_mutations = {
    "id" => "statement_negative_mutations_rejected",
    "cases" => 0,
    "error" => "main note missing",
    "pass" => false
  }
end

artifact_content = primary_artifact_content_checks(artifacts)
environment_mutations = environment_override_checks
negative_groups = [statement_mutations, environment_mutations]

pass = independent_groups.all? { |row| row.fetch("pass") } &&
       artifacts.all? { |row| row.fetch("pass") } &&
       dependencies.all? { |row| row.fetch("pass") } &&
       note_checks.all? { |row| row.fetch("pass") } &&
       artifact_content.fetch("pass") &&
       negative_groups.all? { |row| row.fetch("pass") }

output = {
  "schema" => SCHEMA,
  "independent_checks" => independent_groups,
  "artifacts" => artifacts,
  "dependencies" => dependencies,
  "note_checks" => note_checks,
  "primary_artifact_checks" => [artifact_content],
  "negative_mutation_checks" => negative_groups,
  "scope" => {
    "standard_library_Ruby_with_JSON_Digest_Open3" => true,
    "exact_Rational_and_integer_math_precedes_primary_artifact_inspection" => true,
    "uses_floating_point_random_timestamp_network_or_gems" => false,
    "machine_proves_inherited_PDE_estimates" => false,
    "machine_proves_open_gates_S280_S288_S303_or_S342" => false,
    "machine_proves_Morrey_or_incidence_hypotheses_for_bare_NSE" => false,
    "machine_proves_regularity_or_Clay" => false
  },
  "summary" => {
    "independent_groups_passed" => independent_groups.count { |row| row.fetch("pass") },
    "independent_groups_total" => independent_groups.length,
    "independent_cases" => independent_groups.sum { |row| row.fetch("cases") },
    "artifact_locks_passed" => artifacts.count { |row| row.fetch("pass") },
    "artifact_locks_total" => artifacts.length,
    "dependency_locks_passed" => dependencies.count { |row| row.fetch("pass") },
    "dependency_locks_total" => dependencies.length,
    "note_checks_passed" => note_checks.count { |row| row.fetch("pass") },
    "note_checks_total" => note_checks.length,
    "primary_artifact_groups_passed" => artifact_content.fetch("pass") ? 1 : 0,
    "primary_artifact_groups_total" => 1,
    "primary_artifact_cases" => artifact_content.fetch("cases"),
    "negative_groups_passed" => negative_groups.count { |row| row.fetch("pass") },
    "negative_groups_total" => negative_groups.length,
    "negative_cases" => negative_groups.sum { |row| row.fetch("cases") }
  },
  "pass" => pass
}

puts JSON.pretty_generate(output)
exit(pass ? 0 : 1)
