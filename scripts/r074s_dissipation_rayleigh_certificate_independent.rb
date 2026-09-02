#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent finite/algebraic audit for R0.74S Step 7.
#
# The arithmetic below is reconstructed with Ruby Rational before the primary
# Python JSON is inspected.  The producer artifact is then checked for schema,
# row, claim-boundary, and SHA-256 integrity.  No number read from the producer
# JSON is used to establish the independent inequalities.

require "digest"
require "json"
require "set"

REPO = File.expand_path("..", __dir__)
NOTE_PATH = File.expand_path(
  ENV.fetch(
    "R074S_DISSIPATION_NOTE",
    File.join(REPO, "research/r074s_dissipation_rayleigh_gate.md")
  )
)
CERTIFICATE_PATH = File.expand_path(
  ENV.fetch(
    "R074S_DISSIPATION_JSON",
    File.join(REPO, "research/r074s_dissipation_rayleigh_certificate.json")
  )
)
GENERATOR_PATH = File.expand_path(
  ENV.fetch(
    "R074S_DISSIPATION_GENERATOR",
    File.join(REPO, "scripts/r074s_dissipation_rayleigh_certificate.py")
  )
)
REPORT_PATH = File.expand_path(
  ENV.fetch(
    "R074S_DISSIPATION_REPORT",
    File.join(REPO, "research/r074s_dissipation_rayleigh_certificate_report.md")
  )
)

EXPECTED_NOTE_FIELD = "research/r074s_dissipation_rayleigh_gate.md"
EXPECTED_GENERATOR_FIELD = "scripts/r074s_dissipation_rayleigh_certificate.py"
EXPECTED_SCHEMA = "r074s-dissipation-rayleigh-certificate-v1"

EXPECTED_IDS = {
  "exact_checks" => %w[
    trichotomy_half_minus_two_eighths
    g_over_e_normalization_factor_two
    jensen_four_R_squared_constant_squared
    per_shell_power_of_two_exponent
    per_shell_gamma_exponent
    per_shell_lambda_exponent
    per_shell_payment_exponent
    per_shell_C1_exponent
    per_shell_scalar_two_exponent
    cross_shell_holder_reciprocal_exponents
    cross_shell_coefficient_cube_gamma_exponent
    residual_threshold_reciprocal
    canonical_profile_geometric_sum
    constant_profile_tail_base_exponent
    constant_profile_tail_exponent_growth
    constant_profile_exp_series_lower_bound
  ],
  "finite_checks" => %w[
    exact_rational_priority_trichotomy
    exact_rational_low_rayleigh_mass_implication
    direct_low_set_eta_zero_and_zero_denominator_boundaries
    exact_rational_step_function_jensen_delta_at_most_four
    exact_rational_cross_shell_holder
    constant_lambda_super_gaussian_geometric_tail
    canonical_one_seventh_and_critical_boundary
    near_critical_profile_exact_geometric_sums
  ],
  "negative_mutations" => %w[
    mutation_threshold_eighth_to_quarter
    mutation_drop_g_over_e_factor_two
    mutation_extend_rho_equivalence_to_eta_zero
    mutation_reverse_jensen_direction
    mutation_replace_jensen_half_by_one
    mutation_gamma_exponent_one_third_to_two_thirds
    mutation_declare_critical_lambda_summable
    mutation_residual_factor_eight_to_four
    mutation_promote_finite_checks_to_analytic_PDE_Clay_claims
  ]
}.freeze

EXPECTED_SCOPE = {
  "finite_algebraic_only" => true,
  "machine_proves_Navier_Stokes_PDE" => false,
  "machine_proves_R211" => false,
  "machine_proves_R214" => false,
  "machine_proves_regularity_or_Clay" => false,
  "machine_proves_zero_denominator_weak_gradient_fact" => false
}.freeze

def fraction_string(value)
  "#{value.numerator}/#{value.denominator}"
end

def parse_fraction(value)
  match = /\A(-?\d+)\/(\d+)\z/.match(value.to_s)
  raise ArgumentError, "not a normalized rational string: #{value.inspect}" unless match

  Rational(match[1].to_i, match[2].to_i)
end

def deep_copy(value)
  Marshal.load(Marshal.dump(value))
end

def compact_source(body)
  body.gsub(/\s+/, "").delete("&").gsub(/\\[,!;:]/, "")
end

def exact_row(identifier, left, right, meaning)
  {
    "id" => identifier,
    "left" => fraction_string(left),
    "right" => fraction_string(right),
    "margin" => fraction_string(left - right),
    "meaning" => meaning,
    "pass" => left == right
  }
end

def independent_exact_bookkeeping
  rows = [
    exact_row(
      "residual_low_share",
      Rational(1, 2) - Rational(1, 8) - Rational(1, 8),
      Rational(1, 4),
      "D/T>=1/2 and two failed 1/8 tests leave a strict low share above 1/4"
    ),
    exact_row(
      "rayleigh_density_factor",
      Rational(1, 1) / Rational(1, 2),
      Rational(2),
      "g has coefficient 1/R while e has coefficient 1/(2R)"
    ),
    exact_row(
      "kinetic_mass_denominator",
      Rational(1, 4) / Rational(2),
      Rational(1, 8),
      "g> T/4 and g<=2 lambda R^-2 e give R^-2 integral e>T/(8 lambda)"
    ),
    exact_row(
      "four_parabolic_units_yield_half",
      Rational(4) * Rational(1, 2)**2,
      Rational(1),
      "delta<=4 implies delta^-1/2>=1/2"
    ),
    exact_row(
      "holder_power_of_two",
      Rational(3, 2) * Rational(2, 3),
      Rational(1),
      "(2^(3k/2))^(2/3)=2^k"
    ),
    exact_row(
      "holder_gamma_power",
      Rational(1, 2) * Rational(2, 3),
      Rational(1, 3),
      "(gamma^(1/2))^(2/3)=gamma^(1/3)"
    ),
    exact_row(
      "cross_shell_duality",
      Rational(1, 3) + Rational(2, 3),
      Rational(1),
      "the shell coefficient and payment use Holder exponents 3 and 3/2"
    ),
    exact_row(
      "cubed_shell_coefficient",
      3 * Rational(1, 3),
      Rational(1),
      "cubing gamma^(1/3) leaves one gamma in the ledger"
    ),
    exact_row(
      "residual_factor",
      Rational(8) * Rational(1, 8),
      Rational(1),
      "a 1/8 residual threshold requires coefficient 8"
    ),
    exact_row(
      "canonical_sum",
      Rational(1, 8) / (1 - Rational(1, 8)),
      Rational(1, 7),
      "the epsilon=1 ledger is sum from k=1 of 2^(-3k)"
    ),
    exact_row(
      "critical_shell_weight",
      3 - 3,
      Rational(0),
      "2^(3k) times (2^-k)^3 has zero net dyadic exponent"
    ),
    exact_row(
      "subcritical_gamma_exponent_at_alpha_quarter",
      Rational(1) - 3 * Rational(1, 4),
      Rational(1, 4),
      "the gamma exponent remains positive at alpha=1/4"
    )
  ]

  {
    "id" => "independent_exact_bookkeeping",
    "rows" => rows,
    "pass" => rows.all? { |row| row.fetch("pass") }
  }
end

def independent_priority_trichotomy
  denominator = 24
  terminals = [Rational(1, 2), Rational(1), Rational(3, 2), Rational(2)]
  failures = []
  eligible = 0
  configurations = 0
  counts = Hash.new(0)

  terminals.each do |terminal|
    grid = (0..12).map { |index| terminal * Rational(index, denominator) }
    grid.repeated_permutation(3) do |defect, high, low|
      configurations += 1
      dissipation = defect + high + low
      next if dissipation < terminal / 2

      eligible += 1
      branch = if defect >= terminal / 8
                 "defect"
               elsif high >= terminal / 8
                 "high"
               else
                 "low"
               end
      counts[branch] += 1
      conditions = [
        branch != "defect" || terminal <= 8 * defect,
        branch != "high" || (defect < terminal / 8 && terminal <= 8 * high),
        branch != "low" || (
          defect < terminal / 8 && high < terminal / 8 && low > terminal / 4
        )
      ]
      next if conditions.all?

      failures << {
        "T" => fraction_string(terminal),
        "defect" => fraction_string(defect),
        "high" => fraction_string(high),
        "low" => fraction_string(low),
        "branch" => branch
      } if failures.length < 12
    end
  end

  {
    "id" => "independent_priority_trichotomy_grid",
    "grid_denominator" => denominator,
    "configurations_checked" => configurations,
    "eligible_checked" => eligible,
    "class_counts" => counts.sort.to_h,
    "failures" => failures,
    "pass" => failures.empty? && counts.values.sum == eligible && counts.keys.sort == %w[defect high low]
  }
end

def independent_low_mass_implication
  terminals = [Rational(1, 2), Rational(1), Rational(3, 2)]
  lambdas = [Rational(1, 4), Rational(1, 2), Rational(1), Rational(2), Rational(3)]
  excesses = [Rational(1, 96), Rational(1, 32), Rational(1, 8), Rational(1, 3)]
  slacks = [Rational(0), Rational(1, 40), Rational(1, 7)]
  checked = 0
  failures = []
  minimum_margin = nil

  terminals.product(lambdas, excesses, slacks).each do |terminal, lambda, excess, slack|
    low_g = terminal / 4 + excess
    normalized_e = low_g / (2 * lambda) + slack
    checked += 1
    margin = normalized_e - terminal / (8 * lambda)
    minimum_margin = margin if minimum_margin.nil? || margin < minimum_margin
    correct = low_g <= 2 * lambda * normalized_e && margin.positive?
    next if correct

    failures << {
      "T" => fraction_string(terminal),
      "lambda" => fraction_string(lambda),
      "low_g" => fraction_string(low_g),
      "normalized_e" => fraction_string(normalized_e)
    } if failures.length < 12
  end

  {
    "id" => "independent_low_rayleigh_mass_grid",
    "configurations_checked" => checked,
    "minimum_strict_margin" => fraction_string(minimum_margin),
    "failures" => failures,
    "pass" => failures.empty? && minimum_margin.positive?
  }
end

def independent_jensen_step_functions
  weights = [Rational(1, 4), Rational(1, 2), Rational(1), Rational(3, 2)]
  roots = [Rational(0), Rational(1, 2), Rational(1), Rational(2), Rational(3)]
  checked = 0
  equality_cases = 0
  failures = []

  weights.repeated_permutation(3) do |cell_weights|
    delta = cell_weights.sum
    next if delta > 4

    roots.repeated_permutation(3) do |energy_roots|
      energy_mass = cell_weights.zip(energy_roots).sum do |weight, root|
        weight * root**2
      end
      three_half_mass = cell_weights.zip(energy_roots).sum do |weight, root|
        weight * root**3
      end
      checked += 1
      jensen_margin = delta * three_half_mass**2 - energy_mass**3
      half_margin = 4 * three_half_mass**2 - energy_mass**3
      equality_cases += 1 if jensen_margin.zero?
      next if jensen_margin >= 0 && half_margin >= 0

      failures << {
        "delta" => fraction_string(delta),
        "energy_mass" => fraction_string(energy_mass),
        "three_half_mass" => fraction_string(three_half_mass),
        "jensen_margin" => fraction_string(jensen_margin),
        "half_margin" => fraction_string(half_margin)
      } if failures.length < 12
    end
  end

  {
    "id" => "independent_exact_step_jensen",
    "configurations_checked" => checked,
    "equality_cases" => equality_cases,
    "radicals_used" => false,
    "failures" => failures,
    "pass" => failures.empty? && checked.positive?
  }
end

def independent_cross_shell_holder
  coefficients = [Rational(1, 3), Rational(1), Rational(2)]
  payment_roots = [Rational(0), Rational(1, 2), Rational(1), Rational(2)]
  checked = 0
  equality_cases = 0
  failures = []

  coefficients.repeated_permutation(3) do |a_values|
    payment_roots.repeated_permutation(3) do |b_values|
      # Put p_i=b_i^3.  Then p_i^(2/3)=b_i^2, so the cubed Holder
      # comparison is a purely rational polynomial identity/inequality.
      lhs = a_values.zip(b_values).sum { |a_value, b_value| a_value * b_value**2 }**3
      rhs = a_values.sum { |a_value| a_value**3 } * b_values.sum { |b_value| b_value**3 }**2
      checked += 1
      equality_cases += 1 if lhs == rhs
      next if lhs <= rhs

      failures << {
        "a" => a_values.map { |value| fraction_string(value) },
        "b" => b_values.map { |value| fraction_string(value) },
        "lhs" => fraction_string(lhs),
        "rhs" => fraction_string(rhs)
      } if failures.length < 12
    end
  end

  {
    "id" => "independent_exact_cross_shell_holder",
    "configurations_checked" => checked,
    "equality_cases" => equality_cases,
    "radicals_used" => false,
    "failures" => failures,
    "pass" => failures.empty? && checked.positive?
  }
end

def independent_profile_ledger
  failures = []
  rows = []

  (1..9).each do |numerator|
    epsilon = Rational(numerator, 3)
    ratio = Rational(1, 2)**numerator
    infinite_sum = ratio / (1 - ratio)
    partial = (1..20).sum { |shell| ratio**shell }
    expected_partial = ratio * (1 - ratio**20) / (1 - ratio)
    net_gamma_exponent = Rational(1) - 3 * Rational(1, 3)
    net_dyadic_exponent_per_shell = Rational(3) - 3 * (1 + epsilon)
    conditions = [
      net_gamma_exponent.zero?,
      net_dyadic_exponent_per_shell == -3 * epsilon,
      partial == expected_partial,
      partial < infinite_sum
    ]
    failures << { "epsilon" => fraction_string(epsilon) } unless conditions.all?
    rows << {
      "epsilon" => fraction_string(epsilon),
      "ratio" => fraction_string(ratio),
      "sum" => fraction_string(infinite_sum),
      "partial_20" => fraction_string(partial)
    }
  end

  critical_partial = (1..128).sum { Rational(1) }
  canonical = rows.find { |row| row.fetch("epsilon") == "1/1" }

  # An elementary tail comparison independent of floating point: at k=4,
  # x=3*4^(k-1)/32=6 and exp(6)>1+6+6^2/2+6^3/6=61>16.
  # Hence 8*exp(-6)<1/2; later exponents grow by four.
  tail_exponent = Rational(3 * 4**3, 32)
  exponential_lower_bound = Rational(1) + tail_exponent + tail_exponent**2 / 2 + tail_exponent**3 / 6
  tail_valid = tail_exponent == 6 && exponential_lower_bound > 16

  # For alpha<1/3 the remaining gamma exponent beta=1-3 alpha is positive,
  # so the same super-geometric ratio argument applies after a finite index.
  alpha_rows = [Rational(0), Rational(1, 12), Rational(1, 6), Rational(1, 4), Rational(11, 36)].map do |alpha|
    beta = 1 - 3 * alpha
    { "alpha" => fraction_string(alpha), "beta" => fraction_string(beta), "positive" => beta.positive? }
  end
  failures << { "constant_profile_tail" => "failed" } unless tail_valid
  failures << { "subcritical_alpha" => "failed" } unless alpha_rows.all? { |row| row.fetch("positive") }
  failures << { "canonical_sum" => canonical } unless canonical && canonical.fetch("sum") == "1/7"
  failures << { "critical_partial" => fraction_string(critical_partial) } unless critical_partial == 128

  {
    "id" => "independent_profile_and_boundary_ledger",
    "near_critical_rows" => rows,
    "canonical_sum" => canonical&.fetch("sum"),
    "critical_partial_sum_128" => fraction_string(critical_partial),
    "constant_profile_tail" => {
      "starts_at_shell" => 4,
      "exponent" => fraction_string(tail_exponent),
      "exp_lower_bound" => fraction_string(exponential_lower_bound),
      "ratio_strictly_below_one_half" => tail_valid
    },
    "subcritical_alpha_rows" => alpha_rows,
    "failures" => failures,
    "pass" => failures.empty?
  }
end

def structural_audit(body)
  compact = compact_source(body)
  tags = body.scan(/\\tag\{S\.(\d+)\}/).flatten.map(&:to_i)
  expected_tags = (142..162).to_a

  required_text = [
    "No zero-over-zero convention is needed.",
    "The third class has a parabolically normalized kinetic time mass.",
    "The remaining high-Rayleigh and anomalous-defect classes are **OPEN**.",
    "It does not say that \\(L_{k,R}\\) itself has a fixed positive measure.",
    "No uniform bound on \\(\\#\\mathcal B_\\tau\\) is obtained here.",
    "positive measure where \\(\\eta_R>0\\)",
    "coefficient term in (R.217) is unambiguously zero",
    "This is a **PROVED CONDITIONAL IMPLICATION**, not a finite-exception",
    "No novelty or priority claim is made.",
    "**NOT CLAY.**"
  ]
  required_compact = [
    "\\eta_R(t)>0,\\quad\\int_{\\mathbbT^3}\\Psi_k^R|v_R|^2>0:",
    "g_{k,R}(t)\\le{2\\lambda_k\\overR^2}e_{k,R}(t)",
    "m_{k,R}(\\tau)\\ge\\frac18T_k",
    "\\int_{H_{k,R}}g_{k,R}(t)\\,dt\\ge\\frac18T_k",
    "{T_k\\over8\\lambda_k}",
    "C_2=8(2C_1)^{2/3}",
    "\\mathscrL(\\boldsymbol\\lambda):=\\sum_{k\\ge1}2^{3k}\\gamma_k\\lambda_k^3",
    "\\lambda_k^{(\\varepsilon)}:=2^{-(1+\\varepsilon)k}\\gamma_k^{-1/3}",
    "{2^{-3\\varepsilon}\\over1-2^{-3\\varepsilon}}",
    "\\lambda_k^{\\rmcrit}:=2^{-k}\\gamma_k^{-1/3}",
    "+8\\sum_{k\\in\\mathcalI_{\\rmdef}(\\tau)}m_{k,R}(\\tau)",
    "+8\\sum_{k\\in\\mathcalI_{\\rmhi}(\\tau)}",
    "\\Lambda_{k,R,\\tau}=0"
  ]
  forbidden_text = [
    "The high-Rayleigh branch is proved.",
    "The anomalous-defect branch is proved.",
    "The fixed-scale inequality (Q.1) follows unconditionally.",
    "The Navier--Stokes Millennium problem is solved.",
    "The certificate machine-proves (R.214)."
  ]

  checks = [
    {
      "id" => "tags_consecutive_and_unique",
      "actual" => tags,
      "expected" => expected_tags,
      "pass" => tags == expected_tags && tags.uniq.length == tags.length
    }
  ]
  required_text.each_with_index do |sentinel, index|
    checks << {
      "id" => format("required_text_%02d", index + 1),
      "sentinel" => sentinel,
      "pass" => body.include?(sentinel)
    }
  end
  required_compact.each_with_index do |sentinel, index|
    checks << {
      "id" => format("required_formula_%02d", index + 1),
      "sentinel" => sentinel,
      "pass" => compact.include?(compact_source(sentinel))
    }
  end
  forbidden_text.each_with_index do |sentinel, index|
    checks << {
      "id" => format("forbidden_claim_%02d", index + 1),
      "sentinel" => sentinel,
      "pass" => !body.include?(sentinel)
    }
  end
  checks << {
    "id" => "display_math_balanced",
    "count" => body.scan(/\$\$/).length,
    "pass" => body.scan(/\$\$/).length.even?
  }
  checks << {
    "id" => "no_disallowed_controls",
    "pass" => body.each_byte.none? { |byte| byte < 32 && ![9, 10, 13].include?(byte) }
  }

  {
    "checks" => checks,
    "failed_ids" => checks.reject { |row| row.fetch("pass") }.map { |row| row.fetch("id") },
    "pass" => checks.all? { |row| row.fetch("pass") }
  }
end

def validate_exact_producer_rows(rows, issues)
  rows.each do |row|
    begin
      left = parse_fraction(row.fetch("left"))
      right = parse_fraction(row.fetch("right"))
      margin = parse_fraction(row.fetch("margin"))
      issues << "exact row #{row['id']} arithmetic mismatch" unless left == right && margin == left - right
    rescue KeyError, ArgumentError => error
      issues << "exact row #{row['id'].inspect}: #{error.message}"
    end
  end
end

def validate_structural_producer_rows(rows, note_body, issues)
  compact = compact_source(note_body)
  prose = note_body.gsub(/\s+/, " ")
  rows.each do |row|
    identifier = row["id"].to_s
    case identifier
    when "tags_consecutive_S142_through_S162"
      expected = (142..162).map(&:to_s)
      issues << "producer tag ledger stale" unless row["expected"] == expected && row["actual"] == expected
    when "tags_unique"
      issues << "producer tag uniqueness stale" unless row["actual_count"] == 21 && row["unique_count"] == 21
    when /\Arequired_text_/
      sentinel = row["sentinel"]
      issues << "producer required text sentinel absent: #{identifier}" unless sentinel.is_a?(String) && prose.include?(sentinel)
    when /\Arequired_formula_/
      sentinel = row["sentinel"]
      issues << "producer formula sentinel absent: #{identifier}" unless sentinel.is_a?(String) && compact.include?(compact_source(sentinel))
    when /\Aforbidden_/
      sentinel = row["sentinel"]
      issues << "producer forbidden sentinel present: #{identifier}" unless sentinel.is_a?(String) && !note_body.include?(sentinel)
    else
      issues << "unknown producer structural row: #{identifier}"
    end
  end
end

def validate_finite_producer_rows(rows, issues)
  by_id = rows.to_h { |row| [row["id"], row] }
  trichotomy = by_id["exact_rational_priority_trichotomy"] || {}
  class_counts = trichotomy["class_counts"]
  if class_counts.is_a?(Hash)
    issues << "producer trichotomy count mismatch" unless class_counts.values.sum == trichotomy["dissipation_branch_configurations"]
  else
    issues << "producer trichotomy class counts absent"
  end

  boundary = by_id["canonical_one_seventh_and_critical_boundary"] || {}
  issues << "producer canonical profile stale" unless boundary["canonical_profile"] == "lambda_k=2^(-2k)*gamma_k^(-1/3)"
  issues << "producer canonical sum stale" unless boundary["canonical_infinite_coefficient_sum"] == "1/7"
  issues << "producer critical profile stale" unless boundary["critical_profile"] == "lambda_k=2^(-k)*gamma_k^(-1/3)"
  issues << "producer critical partial sum stale" unless boundary["critical_partial_sum_at_64"] == "64/1"

  direct = by_id["direct_low_set_eta_zero_and_zero_denominator_boundaries"] || {}
  issues << "producer improperly claims zero-gradient machine proof" unless direct["analytic_zero_denominator_gradient_implication_machine_proved"] == false

  near = by_id["near_critical_profile_exact_geometric_sums"] || {}
  epsilon_grid = near["epsilon_grid"]
  rows = near["rows"]
  issues << "producer near-critical epsilon grid absent" unless epsilon_grid == "n/3 for n=1,...,9" && rows.is_a?(Array) && rows.any? { |row| row["epsilon"] == "1/1" && row["infinite_sum"] == "1/7" }
end

def validate_negative_producer_rows(rows, issues)
  by_id = rows.to_h { |row| [row["id"], row] }
  threshold = by_id["mutation_threshold_eighth_to_quarter"] || {}
  issues << "producer threshold mutation lacks counterexample" unless threshold["counterexample"] == true
  r217_scope = by_id["mutation_promote_finite_checks_to_analytic_PDE_Clay_claims"] || {}
  forbidden = r217_scope["forbidden_claims_detected"]
  issues << "producer claim-promotion mutation stale" unless forbidden.is_a?(Array) && forbidden.any? { |claim| claim.include?("R.214") } && forbidden.any? { |claim| claim.include?("Millennium") }
end

def producer_payload_audit(payload, note_body, certificate_sha256: nil)
  issues = []
  issues << "schema mismatch" unless payload["schema"] == EXPECTED_SCHEMA
  issues << "top-level pass is not true" unless payload["pass"] == true
  issues << "scope mismatch" unless payload["scope"] == EXPECTED_SCOPE

  source = payload["source"]
  if source.is_a?(Hash)
    issues << "note path mismatch" unless source["note"] == EXPECTED_NOTE_FIELD
    issues << "generator path mismatch" unless source["generator"] == EXPECTED_GENERATOR_FIELD
    issues << "note hash mismatch" unless source["note_sha256"] == Digest::SHA256.hexdigest(note_body)
    issues << "generator hash mismatch" unless source["generator_sha256"] == Digest::SHA256.file(GENERATOR_PATH).hexdigest
  else
    issues << "source object absent"
  end

  summary = payload["summary"]
  issues << "summary object absent" unless summary.is_a?(Hash)
  EXPECTED_IDS.each do |category, expected_ids|
    rows = payload[category]
    unless rows.is_a?(Array) && rows.all? { |row| row.is_a?(Hash) }
      issues << "#{category} is not an object array"
      next
    end
    identifiers = rows.map { |row| row["id"] }
    issues << "#{category} identifiers mismatch" unless identifiers.sort == expected_ids.sort && identifiers.uniq.length == identifiers.length
    issues << "#{category} contains failed row" unless rows.all? { |row| row["pass"] == true }
    rows.each do |row|
      row.each do |field, value|
        next unless field == "failures" || field.end_with?("_failures")

        issues << "#{category}/#{row['id']}/#{field} is nonempty" unless value.is_a?(Array) && value.empty?
      end
    end

    if summary.is_a?(Hash)
      prefix = category == "negative_mutations" ? "negative_mutations" : category.sub(/_checks\z/, "")
      issues << "#{category} summary total mismatch" unless summary["#{prefix}_total"] == rows.length
      issues << "#{category} summary pass mismatch" unless summary["#{prefix}_passed"] == rows.length
    end

    validate_exact_producer_rows(rows, issues) if category == "exact_checks"
    validate_finite_producer_rows(rows, issues) if category == "finite_checks"
    validate_negative_producer_rows(rows, issues) if category == "negative_mutations"
  end

  structural_rows = payload["structural_checks"]
  if structural_rows.is_a?(Array) && structural_rows.all? { |row| row.is_a?(Hash) }
    identifiers = structural_rows.map { |row| row["id"] }
    issues << "structural ids are not unique" unless identifiers.uniq.length == identifiers.length
    issues << "structural row failed" unless structural_rows.all? { |row| row["pass"] == true }
    validate_structural_producer_rows(structural_rows, note_body, issues)
    if summary.is_a?(Hash)
      issues << "structural summary total mismatch" unless summary["structural_total"] == structural_rows.length
      issues << "structural summary pass mismatch" unless summary["structural_passed"] == structural_rows.length
    end
  else
    issues << "structural_checks is not an object array"
  end

  if certificate_sha256
    report = File.binread(REPORT_PATH)
    source ||= {}
    expected_report_fragments = [
      "**PASS**",
      "Source note SHA-256: `#{source['note_sha256']}`",
      "Generator SHA-256: `#{source['generator_sha256']}`",
      "JSON payload SHA-256: `#{certificate_sha256}`",
      "FINITE/ALGEBRAIC ONLY",
      "NOT CLAY"
    ]
    expected_report_fragments.each do |fragment|
      issues << "report cross-check missing #{fragment.inspect}" unless report.include?(fragment)
    end
  end

  {
    "issues" => issues,
    "pass" => issues.empty?
  }
rescue Errno::ENOENT, TypeError, KeyError => error
  { "issues" => ["#{error.class}: #{error.message}"], "pass" => false }
end

def producer_cross_check(note_body)
  certificate_bytes = File.binread(CERTIFICATE_PATH)
  payload = JSON.parse(certificate_bytes)
  audit = producer_payload_audit(
    payload,
    note_body,
    certificate_sha256: Digest::SHA256.hexdigest(certificate_bytes)
  )
  audit.merge(
    "certificate" => CERTIFICATE_PATH,
    "certificate_sha256" => Digest::SHA256.hexdigest(certificate_bytes),
    "generator_sha256" => Digest::SHA256.file(GENERATOR_PATH).hexdigest,
    "report_sha256" => Digest::SHA256.file(REPORT_PATH).hexdigest
  )
rescue Errno::ENOENT, JSON::ParserError => error
  { "issues" => ["#{error.class}: #{error.message}"], "pass" => false }
end

def adversarial_mutations(note_body, payload)
  mutations = []
  baseline_valid = producer_payload_audit(payload, note_body).fetch("pass")

  stale_hash = deep_copy(payload)
  stale_hash.fetch("source")["note_sha256"] = "0" * 64
  mutations << {
    "id" => "stale_note_hash_rejected",
    "pass" => baseline_valid && !producer_payload_audit(stale_hash, note_body).fetch("pass")
  }

  tag_shift = note_body.sub("\\tag{S.162}", "\\tag{S.163}")
  mutations << {
    "id" => "shifted_terminal_tag_rejected",
    "mutation_applied" => tag_shift != note_body,
    "pass" => baseline_valid && tag_shift != note_body && !structural_audit(tag_shift).fetch("pass")
  }

  wrong_profile = note_body.sub(
    "2^{-(1+\\varepsilon)k}\\gamma_k^{-1/3}",
    "2^{-(2+\\varepsilon)k}\\gamma_k^{-1/3}"
  )
  mutations << {
    "id" => "near_critical_profile_shift_rejected",
    "mutation_applied" => wrong_profile != note_body,
    "pass" => baseline_valid && wrong_profile != note_body && !structural_audit(wrong_profile).fetch("pass")
  }

  wrong_threshold = note_body.sub("\\frac18T_k", "\\frac14T_k")
  mutations << {
    "id" => "one_eighth_threshold_shift_rejected",
    "mutation_applied" => wrong_threshold != note_body,
    "pass" => baseline_valid && wrong_threshold != note_body && !structural_audit(wrong_threshold).fetch("pass")
  }

  missing_r217_boundary = note_body.sub(
    "positive measure where \\(\\eta_R>0\\)",
    "positive measure"
  )
  mutations << {
    "id" => "R217_positive_eta_boundary_removed_rejected",
    "mutation_applied" => missing_r217_boundary != note_body,
    "pass" => baseline_valid && missing_r217_boundary != note_body && !structural_audit(missing_r217_boundary).fetch("pass")
  }

  stale_profile = deep_copy(payload)
  profile_row = stale_profile.fetch("finite_checks").find do |row|
    row["id"] == "canonical_one_seventh_and_critical_boundary"
  end
  profile_row["canonical_profile"] = "lambda_k=2^(-k) gamma_k^(-1/3)" if profile_row
  mutations << {
    "id" => "producer_profile_row_tamper_rejected",
    "mutation_applied" => !profile_row.nil?,
    "pass" => baseline_valid && !profile_row.nil? && !producer_payload_audit(stale_profile, note_body).fetch("pass")
  }

  stale_summary = deep_copy(payload)
  stale_summary.fetch("summary")["finite_total"] += 1
  mutations << {
    "id" => "producer_summary_tamper_rejected",
    "pass" => baseline_valid && !producer_payload_audit(stale_summary, note_body).fetch("pass")
  }

  promoted_scope = deep_copy(payload)
  promoted_scope.fetch("scope")["machine_proves_R214"] = true
  mutations << {
    "id" => "producer_PDE_scope_promotion_rejected",
    "pass" => baseline_valid && !producer_payload_audit(promoted_scope, note_body).fetch("pass")
  }

  stale_generator = deep_copy(payload)
  stale_generator.fetch("source")["generator_sha256"] = "f" * 64
  mutations << {
    "id" => "stale_generator_hash_rejected",
    "pass" => baseline_valid && !producer_payload_audit(stale_generator, note_body).fetch("pass")
  }

  {
    "rows" => mutations,
    "baseline_valid" => baseline_valid,
    "passed" => mutations.count { |row| row.fetch("pass") },
    "total" => mutations.length,
    "pass" => mutations.all? { |row| row.fetch("pass") }
  }
end

begin
  note_body = File.binread(NOTE_PATH).force_encoding("UTF-8")
  payload = JSON.parse(File.binread(CERTIFICATE_PATH))

  independent_checks = [
    independent_exact_bookkeeping,
    independent_priority_trichotomy,
    independent_low_mass_implication,
    independent_jensen_step_functions,
    independent_cross_shell_holder,
    independent_profile_ledger
  ]
  note_structure = structural_audit(note_body)
  producer = producer_cross_check(note_body)
  mutations = adversarial_mutations(note_body, payload)
  passed = independent_checks.all? { |row| row.fetch("pass") } &&
    note_structure.fetch("pass") && producer.fetch("pass") && mutations.fetch("pass")

  output = {
    "schema" => "r074s-dissipation-rayleigh-independent-ruby-v1",
    "engine" => "Ruby standard-library Rational reconstruction",
    "scope" => [
      "FINITE/ALGEBRAIC ONLY",
      "independent threshold, Jensen, Holder, and profile checks",
      "structural and claim-boundary source audit",
      "primary Python JSON used only as an object to cross-check",
      "does not machine-prove R.211, R.214, suitable-weak PDE facts, regularity, or Clay",
      "NOT CLAY"
    ],
    "source" => {
      "note" => NOTE_PATH,
      "note_sha256" => Digest::SHA256.hexdigest(note_body),
      "primary_certificate" => CERTIFICATE_PATH,
      "primary_certificate_sha256" => Digest::SHA256.file(CERTIFICATE_PATH).hexdigest
    },
    "independent_checks" => independent_checks,
    "note_structural_audit" => note_structure,
    "producer_cross_check" => producer,
    "adversarial_mutations" => mutations,
    "summary" => {
      "result" => passed ? "PASS" : "FAIL",
      "independent_passed" => independent_checks.count { |row| row.fetch("pass") },
      "independent_total" => independent_checks.length,
      "structural_passed" => note_structure.fetch("checks").count { |row| row.fetch("pass") },
      "structural_total" => note_structure.fetch("checks").length,
      "mutations_passed" => mutations.fetch("passed"),
      "mutations_total" => mutations.fetch("total"),
      "producer_cross_check" => producer.fetch("pass") ? "PASS" : "FAIL"
    }
  }

  puts JSON.pretty_generate(output)
  exit(passed ? 0 : 1)
rescue Errno::ENOENT, JSON::ParserError, ArgumentError, KeyError, TypeError => error
  warn "independent certificate error: #{error.class}: #{error.message}"
  exit 2
end
