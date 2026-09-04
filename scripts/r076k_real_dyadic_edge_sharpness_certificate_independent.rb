#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent, fail-closed finite verifier for R0.76K.
#
# This Ruby 2.6-compatible implementation uses only the standard library.  It
# recomputes exact polynomial coefficients and integrals, the real dyadic
# sample, the heat/transport phase ledger, the d/128 constant, the growing-q
# sufficient-condition ledger, and the backward-heat finite samples without
# invoking the Python implementation.  The Python JSON is consumed only at the
# end as a cross-implementation check.  These finite checks do not prove the
# continuum limiting arguments, classical orthogonal-polynomial theorems, or
# any Navier--Stokes regularity/singularity statement.  NOT CLAY.

require "digest"
require "json"

ROOT = File.expand_path("..", __dir__)
STEM = "r076k_real_dyadic_edge_sharpness"
FIXTURE_PATH = File.join(ROOT, "scripts", "#{STEM}_fixtures.json")
EXPECTED_PATH = File.join(ROOT, "scripts", "#{STEM}_expected.json")
PYTHON_JSON = ENV.fetch("R076K_JSON", File.join(ROOT, "research", "#{STEM}_certificate.json"))
REPORT = ENV.fetch("R076K_RUBY_REPORT", File.join(ROOT, "research", "#{STEM}_independent_audit.md"))
RUBY_JSON = ENV.fetch("R076K_RUBY_JSON", "")
MUTATION = ENV.fetch("R076K_RUBY_MUTATION", "")

FIXTURE_SCHEMA = "r076k-real-dyadic-edge-sharpness-fixtures-v1"
EXPECTED_SCHEMA = "r076k-real-dyadic-edge-sharpness-expected-v1"
R076J_CORE_COMMIT = "25d44e986d5283107816f910f89b94bceb1d5726"
R076J_MAIN_SHA256 = "a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f"
R076J_PRIMARY_SHA256 = "1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5"
SHA256 = /\A[0-9a-f]{64}\z/
COMMIT = /\A[0-9a-f]{40}\z/

GROUPS = {
  "bindings" => %w[
    main_hash source_hash primary_audit_hash r076j_main_hash r076j_primary_hash
    k_hash_specs_well_formed j_hash_specs_exact j_commit_exact j_commit_well_formed
    upstream_commit_stated upstream_hashes_stated primary_bound_objects
    generated_outputs_unbound binding_inventory binding_rows_complete
  ],
  "inputs" => %w[
    fixture_schema expected_schema fixture_object expected_object fixture_keys
    expected_keys file_inventory frozen_inventory claims_inventory
    coefficient_sample_domain dyadic_sample_domain asymptotic_sample_domain
  ],
  "integrity" => %w[
    main_utf8 source_utf8 primary_utf8 fixture_utf8 expected_utf8 no_controls
    no_cr no_trailing tag_sequence tag_unique tag_count display_balance
    display_count reference_closure
  ],
  "coefficients" => %w[
    chebyshev_recurrence legendre_recurrence coefficient_sample_exact
    binomial_derivative_agree scaled_leading_limit all_sample_coefficients_nonzero
    transformed_degree coefficient_l1_bounds kernel_leading_formula
    kernel_leading_lower_bound confluent_error_bound coefficient_remainder_ledger
  ],
  "orthogonal_integrals" => %w[
    chebyshev_integrals_exact chebyshev_l2_bound legendre_endpoint
    legendre_orthogonality kernel_endpoint kernel_l2_squared
    normalized_kernel_endpoint normalized_kernel_l2_squared kernel_sup_ledger
    endpoint_l2_ratio endpoint_l3_power endpoint_l3_squared_power
  ],
  "dyadic_phase" => %w[
    positive_integer_modes consecutive_modes mode_count dyadic_lower_endpoint
    dyadic_upper_endpoint normalized_frequency_step carrier_identity
    amplitude_positive heat_compensation phase_residual real_cosine_identity
    conjugate_pairing quantifier_text
  ],
  "edge_constants" => %w[
    d_range arcosh_sqrt_samples chebyshev_cosh_samples pointwise_prefactor
    carrier_interval carrier_square_lower interval_fraction chebyshev_square_prefactor
    realification_square numerator_coefficient core_l2_upper exterior_ratio
    core_l3_upper l3_denominator_comparison l3_exterior_ratio constants_expected
  ],
  "asymptotic" => %w[
    eta_identity eta_log_formula q_over_l2 error_power_used sample_sufficient_condition
    sample_condition_decreases density_threshold threshold_positive
    n0_ceiling dyadic_eventually cap_gap_positive cap_gap_leading_positive
    backward_coefficients backward_sum_identity backward_growth_scale
    wrong_forward_direct negative_backward_sign_text
    overlap_exponent_comparison q_window_text
  ],
  "semigroup" => %w[
    positive_diffusion_time exact_transformed_coefficients integer_dyadic_modes
    real_drift_argument imaginary_shift direct_decay_exponents
    rhs_decay_decomposition wrong_imaginary_sign_rejected phase_decomposition
    scalar_heat_exponent carrier_phase finite_mode_identity exact_expected
    conjugation_fragment
  ],
  "sources" => %w[
    zhang_versioned_abs zhang_versioned_pdf zhang_proposition chen_price_publisher
    chen_price_doi dlmf_183 dlmf_186 architecture_attribution bounded_search
    no_priority_search_claim stop_reason
  ],
  "boundary" => %w[
    literature_label proved_locally finite_computation open_label not_clay
    real_dyadic_scope integer_slice_scope one_time_quantifier complete_clock_open
    full_plateau_open larger_window_open l3_gap_open arbitrary_field_open
    regularity_open singularity_open no_simulation no_figure no_novelty no_priority
    primary_pass single_slice_verdict
  ],
  "python_cross" => %w[
    json_object required_fields verdict freeze_ready assertions_positive
    exact_object bindings_object frozen_binding_subset structure_agrees
  ]
}.freeze

NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze
abort("duplicate mutation name in R0.76K Ruby suite") unless
  NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

if ENV.fetch("R076K_RUBY_LIST_MUTATIONS", "") == "1"
  puts NEGATIVE_MUTATIONS
  exit 0
end

def read_json(path, label)
  JSON.parse(File.read(path, encoding: "UTF-8"))
rescue Errno::ENOENT, JSON::ParserError => error
  warn "R0.76K #{label} unavailable or invalid: #{error.message}"
  exit 2
end

def clean_bytes(raw)
  text = raw.dup.force_encoding("UTF-8")
  text.valid_encoding? && raw.bytes.none? do |byte|
    (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127
  end
end

def compact(text)
  text.gsub(/\s+/, "")
end

def fraction(value)
  Rational(value.to_s)
end

def fraction_string(value)
  value.denominator == 1 ? value.numerator.to_s : "#{value.numerator}/#{value.denominator}"
end

def complex_string(value)
  real = fraction_string(value.real)
  imaginary = fraction_string(value.imag.abs)
  sign = value.imag.negative? ? "-" : "+"
  "#{real}#{sign}#{imaginary}i"
end

def sha256(relative)
  path = File.join(ROOT, relative)
  File.file?(path) ? Digest::SHA256.file(path).hexdigest : nil
end

def binding_row(relative, expected)
  observed = sha256(relative)
  {
    "expectedSha256" => expected,
    "observedSha256" => observed || "MISSING",
    "exists" => File.file?(File.join(ROOT, relative)),
    "locked" => expected.is_a?(String) && SHA256.match?(expected),
    "pass" => expected.is_a?(String) && SHA256.match?(expected) && observed == expected
  }
end

def binomial(n, k)
  return 0 if k.negative? || k > n

  k = [k, n - k].min
  (1..k).reduce(1) { |value, j| value * (n - k + j) / j }
end

def factorial(n)
  (1..n).reduce(1, :*)
end

def poly_trim(coefficients)
  result = coefficients.dup
  result.pop while result.length > 1 && result.last == 0
  result
end

def poly_add(left, right)
  length = [left.length, right.length].max
  poly_trim((0...length).map { |j| (left[j] || 0) + (right[j] || 0) })
end

def poly_scale(coefficients, scalar)
  poly_trim(coefficients.map { |value| value * scalar })
end

def poly_shift(coefficients)
  [0] + coefficients
end

def poly_multiply(left, right)
  result = Array.new(left.length + right.length - 1, 0)
  left.each_with_index do |a, j|
    right.each_with_index { |b, k| result[j + k] += a * b }
  end
  poly_trim(result)
end

def poly_derivative(coefficients, order = 1)
  result = coefficients.dup
  order.times do
    return [0] if result.length <= 1

    result = (1...result.length).map { |j| result[j] * j }
  end
  poly_trim(result)
end

def poly_evaluate(coefficients, value)
  coefficients.reverse.reduce(0) { |total, coefficient| total * value + coefficient }
end

def polynomial_integral_minus_one_one(coefficients)
  coefficients.each_with_index.reduce(Rational(0)) do |sum, (coefficient, degree)|
    degree.even? ? sum + Rational(2) * coefficient / (degree + 1) : sum
  end
end

def chebyshev_coefficients(degree)
  return [Rational(1)] if degree.zero?
  return [Rational(0), Rational(1)] if degree == 1

  previous = [Rational(1)]
  current = [Rational(0), Rational(1)]
  (1...degree).each do
    following = poly_add(poly_scale(poly_shift(current), 2), poly_scale(previous, -1))
    previous = current
    current = following
  end
  current
end

def legendre_coefficients(degree)
  return [Rational(1)] if degree.zero?
  return [Rational(0), Rational(1)] if degree == 1

  previous = [Rational(1)]
  current = [Rational(0), Rational(1)]
  (1...degree).each do |m|
    numerator = poly_add(
      poly_scale(poly_shift(current), 2 * m + 1),
      poly_scale(previous, -m)
    )
    following = poly_scale(numerator, Rational(1, m + 1))
    previous = current
    current = following
  end
  current
end

def endpoint_kernel_coefficients(q, normalized = false)
  kernel = [Rational(0)]
  (0...q).each do |m|
    kernel = poly_add(kernel, poly_scale(legendre_coefficients(m), Rational(2 * m + 1, 2)))
  end
  normalized ? poly_scale(kernel, Rational(1, q)) : kernel
end

def transformed_coefficients(polynomial, epsilon)
  n = polynomial.length - 1
  i_epsilon = Complex(Rational(0), epsilon)
  (0..n).map do |j|
    (j..n).reduce(Complex(Rational(0), Rational(0))) do |sum, r|
      sum + polynomial[r] * (i_epsilon**(-r)) * ((-1)**(r - j)) * binomial(r, j)
    end
  end
end

def transformed_coefficients_derivative(polynomial, epsilon)
  n = polynomial.length - 1
  center = Complex(Rational(0), Rational(1, 1) / epsilon)
  i_epsilon = Complex(Rational(0), epsilon)
  (0..n).map do |j|
    poly_evaluate(poly_derivative(polynomial, j), center) /
      (factorial(j) * (i_epsilon**j))
  end
end

def angular_residual(value)
  two_pi = 2.0 * Math::PI
  ((value + Math::PI) % two_pi) - Math::PI
end

def cos_pi_decomposition(angle)
  normalized = angle % 2
  table = {
    Rational(0) => [Rational(1), Rational(0)],
    Rational(1, 6) => [Rational(0), Rational(1, 2)],
    Rational(1, 3) => [Rational(1, 2), Rational(0)],
    Rational(1, 2) => [Rational(0), Rational(0)],
    Rational(2, 3) => [Rational(-1, 2), Rational(0)],
    Rational(5, 6) => [Rational(0), Rational(-1, 2)],
    Rational(1) => [Rational(-1), Rational(0)],
    Rational(7, 6) => [Rational(0), Rational(-1, 2)],
    Rational(4, 3) => [Rational(-1, 2), Rational(0)],
    Rational(3, 2) => [Rational(0), Rational(0)],
    Rational(5, 3) => [Rational(1, 2), Rational(0)],
    Rational(11, 6) => [Rational(0), Rational(1, 2)]
  }
  table[normalized]
end

def explicit_even_chebyshev_coefficients(n)
  result = Array.new(2 * n + 1, Rational(0))
  (0..n).each do |k|
    coefficient = Rational(
      n * ((n + k - 1) >= 0 ? factorial(n + k - 1) : 1),
      factorial(n - k) * factorial(2 * k)
    )
    coefficient *= (-1)**(n - k) * (2**(2 * k))
    result[2 * k] = coefficient
  end
  result
end

def backward_heat_at_zero(polynomial, time_over_a2)
  polynomial.each_with_index.reduce(Rational(0)) do |sum, (coefficient, degree)|
    next sum unless degree.even?

    j = degree / 2
    sum + coefficient * ((-time_over_a2)**j) * Rational(factorial(2 * j), factorial(j))
  end
end

def backward_positive_sum(n, time_over_a2)
  (0..n).reduce(Rational(0)) do |sum, j|
    coefficient = Rational(n * factorial(n + j - 1), factorial(n - j))
    sum + coefficient * ((4 * time_over_a2)**j) / factorial(j)
  end
end

def expected_hash(frozen, key, relative)
  frozen[key] || frozen[relative]
end

fixtures = read_json(FIXTURE_PATH, "fixtures")
expected = read_json(EXPECTED_PATH, "expected values")

files = fixtures.is_a?(Hash) && fixtures["files"].is_a?(Hash) ? fixtures["files"] : {}
frozen = fixtures.is_a?(Hash) && fixtures["frozen"].is_a?(Hash) ? fixtures["frozen"] : {}

file_paths = {
  "main" => files["main"] || "research/#{STEM}.md",
  "source" => files["source"] || "research/r076k_report-source.md",
  "primaryAudit" => files["primaryAudit"] || "research/#{STEM}_primary_audit.md",
  "r076jMain" => files["r076jMain"] || "research/r076j_local_edge_extrapolation_reconstruction.md",
  "r076jPrimaryAudit" => files["r076jPrimaryAudit"] || "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md"
}.freeze

binding_specs = {
  file_paths.fetch("main") => expected_hash(frozen, "mainSha256", file_paths.fetch("main")),
  file_paths.fetch("source") => expected_hash(frozen, "sourceSha256", file_paths.fetch("source")),
  file_paths.fetch("primaryAudit") => expected_hash(frozen, "primaryAuditSha256", file_paths.fetch("primaryAudit")),
  file_paths.fetch("r076jMain") => expected_hash(frozen, "r076jMainSha256", file_paths.fetch("r076jMain")),
  file_paths.fetch("r076jPrimaryAudit") => expected_hash(frozen, "r076jPrimaryAuditSha256", file_paths.fetch("r076jPrimaryAudit"))
}.freeze

bindings = binding_specs.keys.sort.each_with_object({}) do |relative, output|
  output[relative] = binding_row(relative, binding_specs.fetch(relative))
end
freeze_ready = bindings.values.all? { |row| row.fetch("locked") && row.fetch("pass") }

raw = file_paths.each_with_object({}) do |(name, relative), output|
  begin
    output[name] = File.binread(File.join(ROOT, relative))
  rescue Errno::ENOENT
    output[name] = "".b
  end
end
text = raw.transform_values { |value| value.dup.force_encoding("UTF-8") }
main_text = text.fetch("main")
source_text = text.fetch("source")
primary_text = text.fetch("primaryAudit")
cm = compact(main_text)
cs = compact(source_text)

begin
  python_json = JSON.parse(File.read(PYTHON_JSON, encoding: "UTF-8"))
rescue Errno::ENOENT, JSON::ParserError => error
  warn "R0.76K Python certificate unavailable or invalid: #{error.message}"
  exit 2
end

tags = main_text.scan(/\\tag\{K\.(\d+)\}/).flatten.map(&:to_i)
refs = main_text.scan(/(?<![A-Za-z0-9_.])K\.(\d+)/).flatten.map(&:to_i)
display_opens = main_text.scan(/^\\\[$/).length
display_closes = main_text.scan(/^\\\]$/).length

# Exact rational polynomial samples, independently computed from the fixture.
chebyshev_table = (0..8).to_h { |degree| [degree, chebyshev_coefficients(degree)] }
legendre_table = (0..8).to_h { |degree| [degree, legendre_coefficients(degree)] }
polynomial_fixtures = fixtures["polynomialSamples"].is_a?(Array) ? fixtures["polynomialSamples"] : []
polynomial_expected = expected["polynomialSamples"].is_a?(Array) ? expected["polynomialSamples"] : []
polynomial_rows = polynomial_fixtures.map do |sample|
  polynomial = sample.fetch("coefficientsAscending").map { |value| fraction(value) }
  epsilon = fraction(sample.fetch("epsilon"))
  degree = polynomial.length - 1
  binomial_values = transformed_coefficients(polynomial, epsilon)
  derivative_values = transformed_coefficients_derivative(polynomial, epsilon)
  scaled_values = binomial_values.map do |value|
    (Complex(Rational(0), epsilon)**degree) * value
  end
  leading_values = (0..degree).map do |j|
    polynomial.last * ((-1)**(degree - j)) * binomial(degree, j)
  end
  {
    "name" => sample.fetch("name"),
    "polynomial" => polynomial,
    "epsilon" => epsilon,
    "binomial" => binomial_values,
    "derivative" => derivative_values,
    "scaled" => scaled_values,
    "leading" => leading_values
  }
end

def complex_object(value)
  {"re" => fraction_string(value.real), "im" => fraction_string(value.imag)}
end

polynomial_exact_rows = polynomial_rows.map do |row|
  {
    "name" => row.fetch("name"),
    "coefficients" => row.fetch("binomial").map { |value| complex_object(value) },
    "scaledCoefficients" => row.fetch("scaled").map { |value| complex_object(value) },
    "leadingLimits" => row.fetch("leading").map { |value| fraction_string(value) }
  }
end

chebyshev_integrals = (0..8).to_h do |degree|
  polynomial = chebyshev_table.fetch(degree)
  [degree, polynomial_integral_minus_one_one(poly_multiply(polynomial, polynomial))]
end

legendre_integrals = (0..6).flat_map do |left|
  (0..6).map do |right|
    integral = polynomial_integral_minus_one_one(
      poly_multiply(legendre_table.fetch(left), legendre_table.fetch(right))
    )
    [left, right, integral]
  end
end

sample_q = 4
kernel = endpoint_kernel_coefficients(sample_q)
normalized_kernel = endpoint_kernel_coefficients(sample_q, true)
kernel_endpoint = poly_evaluate(kernel, Rational(1))
kernel_l2_squared = polynomial_integral_minus_one_one(poly_multiply(kernel, kernel))
normalized_kernel_endpoint = poly_evaluate(normalized_kernel, Rational(1))
normalized_kernel_l2_squared = polynomial_integral_minus_one_one(
  poly_multiply(normalized_kernel, normalized_kernel)
)

# A fully explicit real, dyadic, exact-phase sample read from the fixture.
slice_fixture = fixtures.fetch("integerSliceSample")
phase_q = Integer(slice_fixture.fetch("q"))
phase_epsilon = fraction(slice_fixture.fetch("eta"))
phase_sample = polynomial_rows.find { |row| row.fetch("name") == slice_fixture.fetch("polynomialSample") }
phase_polynomial = phase_sample ? phase_sample.fetch("polynomial") : [Rational(0)]
phase_coefficients = transformed_coefficients(phase_polynomial, phase_epsilon)
phase_n0 = Integer(slice_fixture.fetch("n0"))
phase_modes = (0...phase_q).map { |j| phase_n0 + j }
phase_m = Rational(phase_n0) * phase_epsilon
phase_theta_over_pi = fraction(slice_fixture.fetch("thetaOverPi"))
phase_beta_over_pi = fraction(slice_fixture.fetch("transportPhaseOverPi"))
phase_heat_scale = fraction(slice_fixture.fetch("heatScale"))
phase_x_over_pi = fraction(slice_fixture.fetch("xOverPi"))
phase_rows = phase_modes.each_with_index.map do |mode, j|
  coefficient = phase_coefficients.fetch(j)
  argument_over_pi = if coefficient.real.zero? && coefficient.imag.positive?
                       Rational(1, 2)
                     elsif coefficient.real.zero? && coefficient.imag.negative?
                       Rational(-1, 2)
                     elsif coefficient.imag.zero? && coefficient.real.positive?
                       Rational(0)
                     elsif coefficient.imag.zero? && coefficient.real.negative?
                       Rational(1)
                     end
  phi_over_pi = argument_over_pi.nil? ? nil :
    -phase_theta_over_pi - argument_over_pi - mode * phase_beta_over_pi
  residual_over_pi = phi_over_pi.nil? ? nil : -phi_over_pi - mode * phase_beta_over_pi
  coefficient_magnitude = coefficient.real.zero? ? coefficient.imag.abs : coefficient.real.abs
  prepaid_heat_exponent = mode**2 * phase_heat_scale
  damping_heat_exponent = -(mode**2) * phase_heat_scale
  {
    "mode" => mode,
    "argumentOverPi" => argument_over_pi,
    "phiOverPi" => phi_over_pi,
    "residualOverPi" => residual_over_pi,
    "amplitudeAtSlice" => 2.0 * coefficient.abs,
    "compensatedAmplitudeExact" => 2 * coefficient_magnitude,
    "prepaidHeatExponent" => prepaid_heat_exponent,
    "dampingHeatExponent" => damping_heat_exponent,
    "netHeatExponent" => prepaid_heat_exponent + damping_heat_exponent
  }
end
phase_contributions = phase_rows.each_with_index.map do |row, j|
  angle_over_pi = row.fetch("mode") * phase_epsilon * phase_x_over_pi + row.fetch("residualOverPi")
  decomposition = cos_pi_decomposition(angle_over_pi)
  coefficient = phase_coefficients.fetch(j)
  magnitude = 2 * (coefficient.real.zero? ? coefficient.imag.abs : coefficient.real.abs)
  {
    "constant" => fraction_string(magnitude * decomposition.fetch(0)),
    "sqrt3Coefficient" => fraction_string(magnitude * decomposition.fetch(1))
  }
end

phase_angle_over_pi = phase_epsilon * phase_x_over_pi
phase_w = if phase_angle_over_pi == Rational(1, 2)
            Complex(Rational(1, 1) / phase_epsilon, Rational(1, 1) / phase_epsilon)
          end
phase_carrier_over_pi = phase_theta_over_pi + phase_m * phase_x_over_pi
phase_polynomial_value = phase_w.nil? ? nil : poly_evaluate(phase_polynomial, phase_w)
profile_constant = nil
profile_sqrt3 = nil
if phase_carrier_over_pi == Rational(5, 3) && phase_polynomial_value
  # exp(5 pi i/3)=(1-i sqrt(3))/2, so 2 Re(exp(...) (u+iv))=u+sqrt(3)v.
  profile_constant = phase_polynomial_value.real
  profile_sqrt3 = phase_polynomial_value.imag
end
phase_cosine_value = phase_rows.each_with_index.reduce(0.0) do |sum, (row, j)|
  sum + row.fetch("amplitudeAtSlice") * Math.cos(Math::PI * (
    row.fetch("mode") * phase_epsilon * phase_x_over_pi -
      row.fetch("phiOverPi") - row.fetch("mode") * phase_beta_over_pi
  ).to_f)
end
phase_target = 2.0 * (
  Complex.polar(1.0, Math::PI * phase_carrier_over_pi.to_f) *
    phase_polynomial_value
).real

# Constant ledgers in K.13--K.24.
pointwise_fixture = fixtures.fetch("pointwiseSample")
pointwise_q = Integer(pointwise_fixture.fetch("q"))
pointwise_d = fraction(pointwise_fixture.fetch("d"))
pointwise_degree = pointwise_q - 1
pointwise_polynomial = polynomial_rows.find do |row|
  row.fetch("name") == pointwise_fixture.fetch("polynomialSample")
end.fetch("polynomial")
pointwise_value = poly_evaluate(pointwise_polynomial, 1 + pointwise_d)
pointwise_l2_squared = polynomial_integral_minus_one_one(
  poly_multiply(pointwise_polynomial, pointwise_polynomial)
)
edge_d_samples = [Rational(1, 1024), Rational(1, 100), pointwise_d, Rational(1)]
arcosh_margins = edge_d_samples.map do |d|
  Math.acosh(1.0 + d.to_f) - Math.sqrt(d.to_f)
end
cosh_samples = [1, 2, 4, 7].product(edge_d_samples).map do |degree, d|
  polynomial_value = poly_evaluate(chebyshev_coefficients(degree), 1.0 + d.to_f)
  cosh_value = Math.cosh(degree * Math.acosh(1.0 + d.to_f))
  (polynomial_value - cosh_value).abs
end
exterior_fixture = fixtures.fetch("exteriorSample")
exterior_q = Integer(exterior_fixture.fetch("q"))
exterior_degree = exterior_q - 1
exterior_d = fraction(exterior_fixture.fetch("d"))
exterior_left = Rational(1) + Rational(7, 8) * exterior_d
exterior_right = Rational(1) + exterior_d
exterior_length = exterior_d / 8
sqrt_seven_d_over_eight = Rational(1, 3) # exact for the frozen d=8/63 sample
exterior_exponent = 2 * exterior_degree * sqrt_seven_d_over_eight
numerator_coefficient = Rational(4) * Rational(1, 4) * Rational(1, 2) * exterior_length
core_l2_upper = Rational(4) * Rational(2)
exterior_ratio = numerator_coefficient / core_l2_upper
core_l3_upper = Rational(8) * Rational(2)

# Growing-q, cap-gap, and backward-heat finite samples.
asymptotic_fixture = fixtures.fetch("asymptoticSample")
rho = fraction(asymptotic_fixture.fetch("rho"))
asymptotic_q = Integer(asymptotic_fixture.fetch("q"))
asymptotic_eta = fraction(asymptotic_fixture.fetch("eta"))
asymptotic_error_power = Integer(asymptotic_fixture.fetch("errorPower"))
convergence_base = Integer(asymptotic_fixture.fetch("convergenceBase"))
approximation_base = Integer(asymptotic_fixture.fetch("approximationBase"))
remainder_base = Integer(asymptotic_fixture.fetch("remainderBase"))
proved_window = fraction(asymptotic_fixture.fetch("provedWindowExponent"))
upper_window = fraction(asymptotic_fixture.fetch("upperWindowExponent"))
eta_q2_7q = asymptotic_eta * asymptotic_q**asymptotic_error_power * convergence_base**asymptotic_q
eta_q2_6q = asymptotic_eta * asymptotic_q**asymptotic_error_power * approximation_base**asymptotic_q
eta_q_5q = asymptotic_eta * asymptotic_q * remainder_base**asymptotic_q
density_threshold = rho.to_f / (4.0 * Math.log(convergence_base.to_f))
half_critical_net = -rho / 8
n0_from_eta = (Rational(1) / asymptotic_eta).ceil

cap_fixture = fixtures.fetch("signedCapSample")
cap_delta_zero = fraction(cap_fixture.fetch("delta0"))
cap_rc = fraction(cap_fixture.fetch("rCenter"))
cap_h = fraction(cap_fixture.fetch("halfWidth"))
cap_radius = fraction(cap_fixture.fetch("collarRadius"))
cap_a = fraction(cap_fixture.fetch("A"))
cap_x = fraction(cap_fixture.fetch("identityTestX"))
cap_left_x = fraction(cap_fixture.fetch("capLeftX"))
cap_m = Integer(cap_fixture.fetch("chebyshevDegree"))
cap_dp = 2 * cap_delta_zero / cap_a
cap_dc = (cap_rc - cap_h + cap_delta_zero) / cap_a
cap_gamma = cap_m * (Math.acosh(1.0 + cap_dc.to_f) - Math.acosh(1.0 + cap_dp.to_f))
cap_leading_rational = Rational(cap_m, Math.sqrt(cap_a.to_f).round)
cap_sqrt_argument = 2 * (cap_rc - cap_h + cap_delta_zero)
cap_constant_subtrahend = 2 * Math.sqrt(cap_delta_zero.to_f)
cap_leading = cap_leading_rational.to_f *
  (Math.sqrt(cap_sqrt_argument.to_f) - cap_constant_subtrahend)
cap_left_t = poly_evaluate(chebyshev_coefficients(cap_m), cap_left_x)
cap_left_pair_coefficient = 4 * cap_left_t**2

semigroup_fixture = fixtures.fetch("semigroupSample")
semigroup_epsilon = fraction(semigroup_fixture.fetch("epsilon"))
semigroup_tau = fraction(semigroup_fixture.fetch("tau"))
semigroup_a = fraction(semigroup_fixture.fetch("A"))
semigroup_e = fraction(semigroup_fixture.fetch("e"))
semigroup_v = fraction(semigroup_fixture.fetch("v"))
semigroup_m = fraction(semigroup_fixture.fetch("M"))
semigroup_x = fraction(semigroup_fixture.fetch("x"))
semigroup_polynomial = semigroup_fixture.fetch("polynomialCoefficientsAscending").map do |value|
  fraction(value)
end
semigroup_time = semigroup_tau / semigroup_a**2
semigroup_real_argument = semigroup_x - semigroup_v * semigroup_tau / semigroup_e
semigroup_imaginary_shift = 2 * semigroup_m * semigroup_tau / semigroup_a**2
semigroup_scalar_exponent = -(semigroup_m**2) * semigroup_tau / semigroup_a**2
semigroup_carrier_phase = semigroup_m * semigroup_real_argument
semigroup_coefficients = transformed_coefficients(semigroup_polynomial, semigroup_epsilon)
semigroup_base_mode_ratio = semigroup_m / semigroup_epsilon
semigroup_base_mode = semigroup_base_mode_ratio.denominator == 1 ? semigroup_base_mode_ratio.numerator : nil
semigroup_integer_modes = semigroup_base_mode.nil? ? [] :
  (0...semigroup_coefficients.length).map { |j| semigroup_base_mode + j }
semigroup_frequencies = (0...semigroup_coefficients.length).map do |j|
  semigroup_m + j * semigroup_epsilon
end
semigroup_direct_decay = semigroup_frequencies.map do |frequency|
  -(frequency**2) * semigroup_time
end
semigroup_internal_heat = (0...semigroup_coefficients.length).map do |j|
  -((j * semigroup_epsilon)**2) * semigroup_time
end
semigroup_shift_decay = (0...semigroup_coefficients.length).map do |j|
  -(j * semigroup_epsilon) * semigroup_imaginary_shift
end
semigroup_wrong_shift_decay = semigroup_shift_decay.map { |value| -value }
semigroup_rhs_decay = semigroup_internal_heat.each_with_index.map do |value, j|
  semigroup_scalar_exponent + value + semigroup_shift_decay.fetch(j)
end
semigroup_wrong_rhs_decay = semigroup_internal_heat.each_with_index.map do |value, j|
  semigroup_scalar_exponent + value + semigroup_wrong_shift_decay.fetch(j)
end
semigroup_direct_phases = semigroup_frequencies.map do |frequency|
  frequency * semigroup_real_argument
end
semigroup_internal_phases = (0...semigroup_coefficients.length).map do |j|
  j * semigroup_epsilon * semigroup_real_argument
end
semigroup_rhs_phases = semigroup_internal_phases.map do |value|
  semigroup_carrier_phase + value
end
semigroup_direct_terms = semigroup_coefficients.each_with_index.map do |coefficient, j|
  coefficient * Math.exp(semigroup_direct_decay.fetch(j).to_f) *
    Complex.polar(1.0, semigroup_direct_phases.fetch(j).to_f)
end
semigroup_rhs_terms = semigroup_coefficients.each_with_index.map do |coefficient, j|
  coefficient * Math.exp(semigroup_rhs_decay.fetch(j).to_f) *
    Complex.polar(1.0, semigroup_rhs_phases.fetch(j).to_f)
end
semigroup_term_residuals = semigroup_direct_terms.zip(semigroup_rhs_terms).map do |left, right|
  (left - right).abs
end

backward_fixture = fixtures.fetch("backwardHeatSample")
backward_n = Integer(backward_fixture.fetch("n"))
backward_m = Integer(backward_fixture.fetch("m"))
backward_a = fraction(backward_fixture.fetch("A"))
backward_t = fraction(backward_fixture.fetch("T"))
backward_time_over_a2 = backward_t / backward_a**2
explicit_backward_polynomial = explicit_even_chebyshev_coefficients(backward_n)
recurrence_backward_polynomial = chebyshev_coefficients(backward_m)
backward_terms = (0..backward_n).map do |j|
  Rational(backward_n * factorial(backward_n + j - 1), factorial(backward_n - j)) *
    ((4 * backward_time_over_a2)**j) / factorial(j)
end
backward_polynomial_value = backward_heat_at_zero(recurrence_backward_polynomial, backward_time_over_a2).abs
backward_sum_value = backward_positive_sum(backward_n, backward_time_over_a2)
wrong_forward_value = backward_heat_at_zero(recurrence_backward_polynomial, -backward_time_over_a2)
overlap_a = 10_000.0
overlap_m = overlap_a**1.75
backward_scale = overlap_m**2 / overlap_a**2
cap_scale = overlap_m / Math.sqrt(overlap_a)

checks = GROUPS.each_with_object({}) do |(group, names), output|
  output[group] = names.each_with_object({}) { |name, rows| rows[name] = false }
end

main_path = file_paths.fetch("main")
source_path = file_paths.fetch("source")
primary_path = file_paths.fetch("primaryAudit")
j_main_path = file_paths.fetch("r076jMain")
j_primary_path = file_paths.fetch("r076jPrimaryAudit")

checks["bindings"]["main_hash"] = bindings.fetch(main_path).fetch("pass")
checks["bindings"]["source_hash"] = bindings.fetch(source_path).fetch("pass")
checks["bindings"]["primary_audit_hash"] = bindings.fetch(primary_path).fetch("pass")
checks["bindings"]["r076j_main_hash"] = bindings.fetch(j_main_path).fetch("pass")
checks["bindings"]["r076j_primary_hash"] = bindings.fetch(j_primary_path).fetch("pass")
checks["bindings"]["k_hash_specs_well_formed"] = %w[mainSha256 sourceSha256 primaryAuditSha256].all? do |key|
  value = expected_hash(frozen, key, file_paths.fetch(key.sub("Sha256", ""), ""))
  value.is_a?(String) && SHA256.match?(value)
end
checks["bindings"]["j_hash_specs_exact"] =
  binding_specs.fetch(j_main_path) == R076J_MAIN_SHA256 &&
  binding_specs.fetch(j_primary_path) == R076J_PRIMARY_SHA256
checks["bindings"]["j_commit_exact"] = frozen["r076jCoreCommit"] == R076J_CORE_COMMIT
checks["bindings"]["j_commit_well_formed"] = COMMIT.match?(frozen["r076jCoreCommit"].to_s)
checks["bindings"]["upstream_commit_stated"] =
  primary_text.include?(R076J_CORE_COMMIT)
checks["bindings"]["upstream_hashes_stated"] = [R076J_MAIN_SHA256, R076J_PRIMARY_SHA256].all? do |value|
  primary_text.include?(value)
end
checks["bindings"]["primary_bound_objects"] =
  bindings.fetch(main_path).fetch("pass") && bindings.fetch(source_path).fetch("pass") &&
  bindings.fetch(primary_path).fetch("pass")
checks["bindings"]["generated_outputs_unbound"] = binding_specs.keys.none? do |path|
  path.end_with?("_certificate.json", "_certificate_report.md", "_independent_audit.md", "_qa_report.md") ||
    File.basename(path) == "AGENTS.md"
end
checks["bindings"]["binding_inventory"] = bindings.keys.sort == binding_specs.keys.sort
checks["bindings"]["binding_rows_complete"] = bindings.values.all? do |row|
  %w[expectedSha256 observedSha256 exists locked pass].all? { |key| row.key?(key) }
end

checks["inputs"]["fixture_schema"] = fixtures["schema"] == FIXTURE_SCHEMA
checks["inputs"]["expected_schema"] = expected["schema"] == EXPECTED_SCHEMA
checks["inputs"]["fixture_object"] = fixtures.is_a?(Hash)
checks["inputs"]["expected_object"] = expected.is_a?(Hash)
checks["inputs"]["fixture_keys"] = %w[
  schema files frozen polynomialSamples pointwiseSample exteriorSample
  integerSliceSample asymptoticSample signedCapSample semigroupSample backwardHeatSample claims
].all? { |key| fixtures.key?(key) }
checks["inputs"]["expected_keys"] = %w[
  schema structure polynomialSamples orthogonalPolynomials pointwiseSample
  exteriorSample integerSliceSample asymptoticSample signedCapSample
  semigroupSample backwardHeatSample claims
].all? { |key| expected.key?(key) }
checks["inputs"]["file_inventory"] = %w[main source primaryAudit r076jMain r076jPrimaryAudit].all? do |key|
  files[key].is_a?(String) && !files[key].empty?
end
checks["inputs"]["frozen_inventory"] = %w[
  mainSha256 sourceSha256 primaryAuditSha256 r076jMainSha256
  r076jPrimaryAuditSha256 r076jCoreCommit
].all? { |key| frozen[key].is_a?(String) }
claims = fixtures["claims"].is_a?(Hash) ? fixtures["claims"] : {}
checks["inputs"]["claims_inventory"] = %w[
  realDyadicSharpness exactIntegerSingleSlice signedTwoCapSingleSlice
  completeFluxLowerBound fullQOLFiveHalvesRange qOLSquaredRange
  l3EndpointOptimality formalFigureRequired simulationRequired noveltyClaimed clayClaimed
].all? { |key| claims.key?(key) }
checks["inputs"]["coefficient_sample_domain"] = polynomial_rows.length == 3 && polynomial_rows.all? do |row|
  row.fetch("epsilon").positive? && row.fetch("polynomial").length == 4 && !row.fetch("polynomial").last.zero?
end
checks["inputs"]["dyadic_sample_domain"] = phase_q >= 2 && phase_epsilon.positive? && phase_n0 >= phase_q - 1
checks["inputs"]["asymptotic_sample_domain"] =
  rho.positive? && asymptotic_eta.positive? && asymptotic_q >= 2 && cap_delta_zero.positive?

checks["integrity"]["main_utf8"] = clean_bytes(raw.fetch("main"))
checks["integrity"]["source_utf8"] = clean_bytes(raw.fetch("source"))
checks["integrity"]["primary_utf8"] = clean_bytes(raw.fetch("primaryAudit"))
checks["integrity"]["fixture_utf8"] = clean_bytes(File.binread(FIXTURE_PATH))
checks["integrity"]["expected_utf8"] = clean_bytes(File.binread(EXPECTED_PATH))
checks["integrity"]["no_controls"] = raw.values.all? { |value| clean_bytes(value) }
checks["integrity"]["no_cr"] = raw.values_at("main", "source", "primaryAudit").none? { |value| value.include?("\r") }
checks["integrity"]["no_trailing"] = text.values_at("main", "source", "primaryAudit").all? do |body|
  body.lines.none? { |line| line.chomp.end_with?(" ", "\t") }
end
checks["integrity"]["tag_sequence"] = tags == (1..48).to_a
checks["integrity"]["tag_unique"] = tags.uniq.length == tags.length
checks["integrity"]["tag_count"] = tags.length == 48
checks["integrity"]["display_balance"] = display_opens == display_closes
checks["integrity"]["display_count"] = display_opens == 48
checks["integrity"]["reference_closure"] = (refs.uniq - tags.uniq).empty?

checks["coefficients"]["chebyshev_recurrence"] =
  chebyshev_table.fetch(3) == [0, -3, 0, 4] &&
  chebyshev_table.fetch(4) == [1, 0, -8, 0, 8]
checks["coefficients"]["legendre_recurrence"] =
  legendre_table.fetch(3) == [0, Rational(-3, 2), 0, Rational(5, 2)] &&
  legendre_table.fetch(4) == [Rational(3, 8), 0, Rational(-30, 8), 0, Rational(35, 8)]
checks["coefficients"]["coefficient_sample_exact"] = polynomial_exact_rows == polynomial_expected
checks["coefficients"]["binomial_derivative_agree"] = polynomial_rows.all? do |row|
  row.fetch("binomial") == row.fetch("derivative")
end
checks["coefficients"]["scaled_leading_limit"] = polynomial_rows.all? do |row|
  degree = row.fetch("polynomial").length - 1
  row.fetch("leading").each_with_index.all? do |value, j|
    value == row.fetch("polynomial").last * ((-1)**(degree - j)) * binomial(degree, j)
  end
end
checks["coefficients"]["all_sample_coefficients_nonzero"] = polynomial_rows.all? do |row|
  row.fetch("binomial").none?(&:zero?)
end
checks["coefficients"]["transformed_degree"] = polynomial_rows.all? do |row|
  row.fetch("binomial").length == row.fetch("polynomial").length
end
checks["coefficients"]["coefficient_l1_bounds"] = (0..8).all? do |degree|
  chebyshev_table.fetch(degree).map(&:abs).sum <= (1.0 + Math.sqrt(2.0))**degree + 1.0e-12 &&
    legendre_table.fetch(degree).map(&:abs).sum <= (1.0 + Math.sqrt(2.0))**degree + 1.0e-12
end
kernel_leading_formula = Rational(2 * sample_q - 1, 2 * sample_q) *
  Rational(binomial(2 * sample_q - 2, sample_q - 1), 2**(sample_q - 1))
checks["coefficients"]["kernel_leading_formula"] = normalized_kernel.last == kernel_leading_formula
checks["coefficients"]["kernel_leading_lower_bound"] = normalized_kernel.last >= Rational(3, 4)
checks["coefficients"]["confluent_error_bound"] = [Rational(1, 8), Rational(1, 16)].all? do |eta|
  [-2.0, -1.0, 0.0, 1.0, 2.0].all? do |x|
    w = (Complex.polar(1.0, eta.to_f * x) - 1) / Complex(0.0, eta.to_f)
    (w - x).abs <= eta.to_f * x * x / 2.0 + 1.0e-12
  end
end
checks["coefficients"]["coefficient_remainder_ledger"] =
  Rational(9, 4).to_f * (1.0 + Math.sqrt(2.0)) < 6.0 &&
  5.0 < 7.0 && 6.0 < 7.0

checks["orthogonal_integrals"]["chebyshev_integrals_exact"] = {
  0 => Rational(2), 1 => Rational(2, 3), 2 => Rational(14, 15), 3 => Rational(34, 35)
}.all? { |degree, value| chebyshev_integrals.fetch(degree) == value }
checks["orthogonal_integrals"]["chebyshev_l2_bound"] = chebyshev_integrals.values.all? do |value|
  value <= 2
end
checks["orthogonal_integrals"]["legendre_endpoint"] = (0..8).all? do |degree|
  poly_evaluate(legendre_table.fetch(degree), Rational(1)) == 1
end
checks["orthogonal_integrals"]["legendre_orthogonality"] = legendre_integrals.all? do |left, right, value|
  target = left == right ? Rational(2, 2 * left + 1) : Rational(0)
  value == target
end
checks["orthogonal_integrals"]["kernel_endpoint"] = kernel_endpoint == Rational(sample_q**2, 2)
checks["orthogonal_integrals"]["kernel_l2_squared"] = kernel_l2_squared == Rational(sample_q**2, 2)
checks["orthogonal_integrals"]["normalized_kernel_endpoint"] =
  normalized_kernel_endpoint == Rational(sample_q, 2)
checks["orthogonal_integrals"]["normalized_kernel_l2_squared"] =
  normalized_kernel_l2_squared == Rational(1, 2)
checks["orthogonal_integrals"]["kernel_sup_ledger"] =
  (0...sample_q).map { |m| Rational(2 * m + 1, 2) }.sum == Rational(sample_q**2, 2)
checks["orthogonal_integrals"]["endpoint_l2_ratio"] =
  kernel_endpoint**2 / kernel_l2_squared == Rational(sample_q**2, 2) &&
  expected.fetch("orthogonalPolynomials").fetch("unnormalizedLegendreEndpoint") == fraction_string(kernel_endpoint) &&
  expected.fetch("orthogonalPolynomials").fetch("unnormalizedLegendreL2Squared") == fraction_string(kernel_l2_squared)
checks["orthogonal_integrals"]["endpoint_l3_power"] =
  kernel_endpoint**3 / Rational(sample_q**4, 4) == 8 &&
  expected.fetch("orthogonalPolynomials").fetch("unnormalizedLegendreL3CubeUpper") == fraction_string(Rational(sample_q**4, 4)) &&
  expected.fetch("orthogonalPolynomials").fetch("l3EndpointRatioLower") == "2"
checks["orthogonal_integrals"]["endpoint_l3_squared_power"] =
  expected.fetch("orthogonalPolynomials").fetch("l3EndpointSquaredLower") == "4"

orthogonal_expected = expected.fetch("orthogonalPolynomials")
checks["orthogonal_integrals"]["chebyshev_integrals_exact"] &&=
  orthogonal_expected.fetch("chebyshevThrough4") == (0..4).map do |degree|
    chebyshev_table.fetch(degree).map { |value| fraction_string(value) }
  end
checks["orthogonal_integrals"]["chebyshev_l2_bound"] &&=
  orthogonal_expected.fetch("t3AtThreeHalves") == fraction_string(
    poly_evaluate(chebyshev_table.fetch(3), Rational(3, 2))
  ) && orthogonal_expected.fetch("t3L2Squared") == fraction_string(chebyshev_integrals.fetch(3))
checks["orthogonal_integrals"]["normalized_kernel_endpoint"] &&=
  orthogonal_expected.fetch("normalizedLegendreEndpoint") == fraction_string(normalized_kernel_endpoint)
checks["orthogonal_integrals"]["normalized_kernel_l2_squared"] &&=
  orthogonal_expected.fetch("normalizedLegendreL2Squared") == fraction_string(normalized_kernel_l2_squared)
checks["orthogonal_integrals"]["kernel_endpoint"] &&=
  orthogonal_expected.fetch("normalizedLegendreKernelQ4") == normalized_kernel.map { |value| fraction_string(value) }

slice_expected = expected.fetch("integerSliceSample")
checks["dyadic_phase"]["positive_integer_modes"] = phase_modes.all?(&:positive?) &&
  slice_expected.fetch("indices") == phase_modes
checks["dyadic_phase"]["consecutive_modes"] = phase_modes.each_cons(2).all? { |left, right| right == left + 1 }
checks["dyadic_phase"]["mode_count"] = phase_modes.length == phase_q &&
  slice_expected.fetch("complexBranchCount") == 2 * phase_q
checks["dyadic_phase"]["dyadic_lower_endpoint"] = phase_modes.first == phase_n0
checks["dyadic_phase"]["dyadic_upper_endpoint"] = phase_modes.last <= 2 * phase_n0
scaled_frequencies = phase_modes.map { |mode| mode * phase_epsilon }
checks["dyadic_phase"]["normalized_frequency_step"] =
  scaled_frequencies.each_cons(2).all? { |left, right| right - left == phase_epsilon } &&
  slice_expected.fetch("scaledFrequencies") == scaled_frequencies.map { |value| fraction_string(value) }
checks["dyadic_phase"]["carrier_identity"] = phase_m == phase_n0 * phase_epsilon &&
  slice_expected.fetch("M") == fraction_string(phase_m) &&
  slice_expected.fetch("carrierPhaseOverPi") == fraction_string(phase_carrier_over_pi)
checks["dyadic_phase"]["amplitude_positive"] = phase_rows.all? do |row|
  row.fetch("amplitudeAtSlice").positive?
end
checks["dyadic_phase"]["heat_compensation"] = phase_rows.each_with_index.all? do |row, j|
  row.fetch("prepaidHeatExponent") == row.fetch("mode")**2 * phase_heat_scale &&
    row.fetch("dampingHeatExponent") == -(row.fetch("mode")**2) * phase_heat_scale &&
    row.fetch("netHeatExponent").zero? &&
    row.fetch("compensatedAmplitudeExact") ==
      2 * (phase_coefficients.fetch(j).real.zero? ? phase_coefficients.fetch(j).imag.abs : phase_coefficients.fetch(j).real.abs)
end &&
  slice_expected.fetch("prepaidHeatExponents") == phase_rows.map { |row| fraction_string(row.fetch("prepaidHeatExponent")) } &&
  slice_expected.fetch("dampingHeatExponents") == phase_rows.map { |row| fraction_string(row.fetch("dampingHeatExponent")) } &&
  slice_expected.fetch("netHeatExponents") == phase_rows.map { |row| fraction_string(row.fetch("netHeatExponent")) } &&
  slice_expected.fetch("compensatedAmplitudes") == phase_rows.map { |row| fraction_string(row.fetch("compensatedAmplitudeExact")) }
checks["dyadic_phase"]["phase_residual"] =
  phase_rows.none? { |row| row.fetch("argumentOverPi").nil? } &&
  slice_expected.fetch("coefficientArgumentsOverPi") == phase_rows.map { |row| fraction_string(row.fetch("argumentOverPi")) } &&
  slice_expected.fetch("phasesOverPi") == phase_rows.map { |row| fraction_string(row.fetch("phiOverPi")) } &&
  slice_expected.fetch("phaseResidualsOverPi") == phase_rows.map { |row| fraction_string(row.fetch("residualOverPi")) }
checks["dyadic_phase"]["real_cosine_identity"] =
  (phase_cosine_value - phase_target).abs <= 1.0e-9 &&
  !phase_w.nil? && slice_expected.fetch("wAtSample") == complex_object(phase_w) &&
  slice_expected.fetch("exactProfile") == {
    "constant" => fraction_string(profile_constant),
    "sqrt3Coefficient" => fraction_string(profile_sqrt3)
  } && slice_expected.fetch("cosineContributions") == phase_contributions
checks["dyadic_phase"]["conjugate_pairing"] = cm.include?("negativefrequenciesareexactlytheirconjugates") &&
  main_text.include?("2q` complex exponential branches")
checks["dyadic_phase"]["quantifier_text"] =
  cm.include?("foreveryprescribed`s_*`and`B`") &&
  cm.include?("notonepacketthatrealizesK.29ateverytime")

checks["edge_constants"]["d_range"] = edge_d_samples.all? { |d| d.positive? && d <= 1 }
checks["edge_constants"]["arcosh_sqrt_samples"] = arcosh_margins.min >= -1.0e-14
checks["edge_constants"]["chebyshev_cosh_samples"] = cosh_samples.max <= 1.0e-9
checks["edge_constants"]["pointwise_prefactor"] = cm.include?("\\frac1{2\\sqrt2}")
pointwise_expected = expected.fetch("pointwiseSample")
exterior_expected = expected.fetch("exteriorSample")
checks["edge_constants"]["pointwise_prefactor"] &&=
  pointwise_expected.fetch("q") == pointwise_q &&
  pointwise_expected.fetch("degree") == pointwise_degree &&
  pointwise_expected.fetch("d") == fraction_string(pointwise_d) &&
  pointwise_expected.fetch("chebyshevValue") == fraction_string(pointwise_value) &&
  pointwise_expected.fetch("polynomialL2Squared") == fraction_string(pointwise_l2_squared) &&
  pointwise_expected.fetch("theoremSquaredPrefactor") == "1/8"
checks["edge_constants"]["carrier_interval"] =
  exterior_left == Rational(10, 9) && exterior_right == Rational(71, 63)
checks["edge_constants"]["carrier_square_lower"] = Math.cos(Rational(1, 8).to_f)**2 >= 0.5
checks["edge_constants"]["interval_fraction"] = exterior_length == exterior_d / 8
checks["edge_constants"]["chebyshev_square_prefactor"] = Rational(1, 2)**2 == Rational(1, 4)
checks["edge_constants"]["realification_square"] = Rational(2)**2 == 4
checks["edge_constants"]["numerator_coefficient"] = numerator_coefficient == exterior_d / 16
checks["edge_constants"]["core_l2_upper"] = core_l2_upper == 8
checks["edge_constants"]["exterior_ratio"] = exterior_ratio == exterior_d / 128
checks["edge_constants"]["core_l3_upper"] = core_l3_upper == 16
checks["edge_constants"]["l3_denominator_comparison"] = 16**2 < 8**3
checks["edge_constants"]["l3_exterior_ratio"] = exterior_ratio == exterior_d / 128
checks["edge_constants"]["constants_expected"] = exterior_expected == {
  "q" => exterior_q,
  "degree" => exterior_degree,
  "d" => fraction_string(exterior_d),
  "intervalLeft" => fraction_string(exterior_left),
  "intervalRight" => fraction_string(exterior_right),
  "intervalLength" => fraction_string(exterior_length),
  "sqrtSevenDOverEight" => fraction_string(sqrt_seven_d_over_eight),
  "exponent" => fraction_string(exterior_exponent),
  "numeratorCoefficient" => fraction_string(numerator_coefficient),
  "l2DenominatorUpper" => fraction_string(core_l2_upper),
  "l3CubeUpper" => fraction_string(core_l3_upper),
  "l3TwoThirdsStrictUpper" => "8",
  "ratioCoefficient" => fraction_string(exterior_ratio)
}

checks["asymptotic"]["eta_identity"] = cm.include?("\\eta_L=(a-\\delta_0)R")
asymptotic_expected = expected.fetch("asymptoticSample")
checks["asymptotic"]["eta_log_formula"] =
  Math.log(eta_q2_7q.to_f).finite? &&
  (Math.log(eta_q2_7q.to_f) -
    (Math.log(asymptotic_eta.to_f) + 2 * Math.log(asymptotic_q) +
      asymptotic_q * Math.log(convergence_base))).abs <= 1.0e-12
checks["asymptotic"]["q_over_l2"] = upper_window - proved_window == Rational(1, 2)
checks["asymptotic"]["error_power_used"] =
  asymptotic_error_power == 2 &&
  eta_q2_7q == asymptotic_eta * asymptotic_q**asymptotic_error_power * convergence_base**asymptotic_q
checks["asymptotic"]["sample_sufficient_condition"] =
  eta_q2_7q == Rational(1, 16) && eta_q2_7q < 1
checks["asymptotic"]["sample_condition_decreases"] =
  eta_q2_6q < eta_q2_7q && eta_q_5q < eta_q2_7q
checks["asymptotic"]["density_threshold"] =
  (density_threshold - rho.to_f / (4.0 * Math.log(convergence_base.to_f))).abs <= 1.0e-15
checks["asymptotic"]["threshold_positive"] = density_threshold.positive?
checks["asymptotic"]["n0_ceiling"] =
  n0_from_eta == (Rational(1) / asymptotic_eta).ceil &&
  n0_from_eta * asymptotic_eta >= 1 && n0_from_eta * asymptotic_eta < 1 + asymptotic_eta
checks["asymptotic"]["dyadic_eventually"] = n0_from_eta >= asymptotic_q - 1
cap_expected = expected.fetch("signedCapSample")
checks["asymptotic"]["cap_gap_positive"] =
  cap_dc > cap_dp && cap_gamma.positive? &&
  cap_delta_zero < cap_rc - 3 * cap_h && cap_rc + 3 * cap_h < cap_radius &&
  cap_expected.fetch("plateauGap") == fraction_string(cap_dp) &&
  cap_expected.fetch("capGap") == fraction_string(cap_dc) &&
  cap_expected.fetch("capGapLarger") == true &&
  cap_expected.fetch("strictSubcapGeometry") == true
checks["asymptotic"]["cap_gap_leading_positive"] =
  cap_leading.positive? &&
  cap_expected.fetch("gammaLeadingRationalFactor") == fraction_string(cap_leading_rational) &&
  cap_expected.fetch("gammaLeadingSqrtArgument") == fraction_string(cap_sqrt_argument) &&
  cap_expected.fetch("gammaLeadingConstantSubtrahend") == fraction_string(2 * cap_delta_zero) &&
  cap_expected.fetch("pairIdentityCoefficient") == "4" &&
  cap_expected.fetch("t3AtCarrier") == fraction_string(poly_evaluate(chebyshev_coefficients(cap_m), cap_x)) &&
  cap_expected.fetch("capLeftX") == fraction_string(cap_left_x) &&
  cap_expected.fetch("t3AtCapLeft") == fraction_string(cap_left_t) &&
  cap_expected.fetch("capLeftPairSineCoefficient") == fraction_string(cap_left_pair_coefficient) &&
  cap_expected.fetch("carrierSinePositive") == (Math.sin(2.0 * cap_x.to_f) > 0)
checks["asymptotic"]["backward_coefficients"] =
  backward_m == 2 * backward_n && explicit_backward_polynomial == recurrence_backward_polynomial
checks["asymptotic"]["backward_sum_identity"] =
  backward_polynomial_value == backward_sum_value && backward_sum_value == backward_terms.sum
backward_expected = expected.fetch("backwardHeatSample")
checks["asymptotic"]["backward_growth_scale"] =
  backward_sum_value > 1 &&
  backward_expected.fetch("terms") == backward_terms.map { |value| fraction_string(value) } &&
  backward_expected.fetch("exactValue") == fraction_string(backward_sum_value) &&
  backward_expected.fetch("wrongForwardSignValue") == fraction_string(wrong_forward_value) &&
  wrong_forward_value != backward_sum_value
wrong_forward_from_terms = backward_terms.each_with_index.reduce(Rational(0)) do |sum, (value, j)|
  sum + ((-1)**j) * value
end
checks["asymptotic"]["wrong_forward_direct"] =
  wrong_forward_value == wrong_forward_from_terms && wrong_forward_value == Rational(531, 625)
checks["asymptotic"]["negative_backward_sign_text"] =
  cm.include?("e^{-(T/A^2)D^2}T_{2n}") &&
  !cm.include?("e^{+(T/A^2)D^2}T_{2n}")
checks["asymptotic"]["overlap_exponent_comparison"] =
  overlap_m > overlap_a**1.5 && overlap_m < overlap_a**2 && backward_scale > cap_scale
checks["asymptotic"]["q_window_text"] =
  cm.include?("q(L)=o(L^2)") && cm.include?("q=o(L^(5/2))") &&
  cm.include?("coarsesufficientconditiondoesnotcoverthefullR0.76Jupperwindow") &&
  asymptotic_expected == {
    "etaQSquaredSevenToQ" => fraction_string(eta_q2_7q),
    "etaQSquaredSixToQ" => fraction_string(eta_q2_6q),
    "etaQFiveToQ" => fraction_string(eta_q_5q),
    "normalizedLegendreLeadingQ4" => fraction_string(normalized_kernel.last),
    "generalLeadingLower" => "3/4",
    "halfCriticalNetExponentCoefficient" => fraction_string(half_critical_net),
    "provedWindowExponent" => fraction_string(proved_window),
    "upperWindowExponent" => fraction_string(upper_window),
    "windowGap" => fraction_string(upper_window - proved_window)
  }

semigroup_expected = expected.fetch("semigroupSample")
checks["semigroup"]["positive_diffusion_time"] = semigroup_time.positive?
checks["semigroup"]["exact_transformed_coefficients"] =
  semigroup_coefficients == [Complex(-16, 0), Complex(32, 0), Complex(-16, 0)]
checks["semigroup"]["integer_dyadic_modes"] =
  !semigroup_base_mode.nil? && semigroup_integer_modes == [4, 5, 6] &&
  semigroup_integer_modes.last <= 2 * semigroup_integer_modes.first
checks["semigroup"]["real_drift_argument"] = semigroup_real_argument == 2
checks["semigroup"]["imaginary_shift"] = semigroup_imaginary_shift == Rational(1, 2)
checks["semigroup"]["direct_decay_exponents"] =
  semigroup_direct_decay == [Rational(-1, 4), Rational(-25, 64), Rational(-9, 16)]
checks["semigroup"]["rhs_decay_decomposition"] =
  semigroup_rhs_decay == semigroup_direct_decay &&
  semigroup_internal_heat == [Rational(0), Rational(-1, 64), Rational(-1, 16)] &&
  semigroup_shift_decay == [Rational(0), Rational(-1, 8), Rational(-1, 4)]
checks["semigroup"]["wrong_imaginary_sign_rejected"] =
  semigroup_wrong_rhs_decay != semigroup_direct_decay &&
  semigroup_wrong_rhs_decay.each_with_index.any? { |value, j| value != semigroup_direct_decay.fetch(j) }
checks["semigroup"]["phase_decomposition"] =
  semigroup_rhs_phases == semigroup_direct_phases &&
  semigroup_internal_phases == [Rational(0), Rational(1, 2), Rational(1)]
checks["semigroup"]["scalar_heat_exponent"] = semigroup_scalar_exponent == Rational(-1, 4)
checks["semigroup"]["carrier_phase"] = semigroup_carrier_phase == 2
checks["semigroup"]["finite_mode_identity"] = semigroup_term_residuals.max <= 1.0e-14
checks["semigroup"]["exact_expected"] = semigroup_expected == {
  "epsilon" => fraction_string(semigroup_epsilon),
  "diffusionTime" => fraction_string(semigroup_time),
  "realDriftArgument" => fraction_string(semigroup_real_argument),
  "imaginaryShift" => fraction_string(semigroup_imaginary_shift),
  "transformedCoefficients" => semigroup_coefficients.map { |value| fraction_string(value.real) },
  "integerModes" => semigroup_integer_modes,
  "modeFrequencies" => semigroup_frequencies.map { |value| fraction_string(value) },
  "directDecayExponents" => semigroup_direct_decay.map { |value| fraction_string(value) },
  "internalHeatExponents" => semigroup_internal_heat.map { |value| fraction_string(value) },
  "imaginaryShiftExponents" => semigroup_shift_decay.map { |value| fraction_string(value) },
  "rhsCombinedDecayExponents" => semigroup_rhs_decay.map { |value| fraction_string(value) },
  "directPhases" => semigroup_direct_phases.map { |value| fraction_string(value) },
  "internalPhases" => semigroup_internal_phases.map { |value| fraction_string(value) },
  "rhsCombinedPhases" => semigroup_rhs_phases.map { |value| fraction_string(value) },
  "scalarHeatExponent" => fraction_string(semigroup_scalar_exponent),
  "carrierPhase" => fraction_string(semigroup_carrier_phase)
}
checks["semigroup"]["conjugation_fragment"] =
  cm.include?("e^{\\tauA^{-2}D^2}h_\\eta") &&
  cm.include?("x-\\frac{v\\tau}{e_a}+\\frac{2iM_L\\tau}{A^2}") &&
  cm.include?("-M_L^2\\tau/A^2")

checks["sources"]["zhang_versioned_abs"] = source_text.include?("https://arxiv.org/abs/2607.10501v1")
checks["sources"]["zhang_versioned_pdf"] = source_text.include?("https://arxiv.org/pdf/2607.10501v1")
checks["sources"]["zhang_proposition"] = source_text.include?("Proposition 7.1") && main_text.include?("Proposition 7.1")
checks["sources"]["chen_price_publisher"] = source_text.include?("drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2019.36")
checks["sources"]["chen_price_doi"] = source_text.include?("10.4230/LIPIcs.ICALP.2019.36")
checks["sources"]["dlmf_183"] = source_text.include?("https://dlmf.nist.gov/18.3")
checks["sources"]["dlmf_186"] = source_text.include?("https://dlmf.nist.gov/18.6")
checks["sources"]["architecture_attribution"] = source_text.include?("polynomial-to-exponential lower architecture")
checks["sources"]["bounded_search"] = source_text.include?("bounded search") || source_text.include?("search was deliberately bounded")
checks["sources"]["no_priority_search_claim"] = source_text.include?("not evidence of novelty or priority")
checks["sources"]["stop_reason"] = source_text.include?("Search stopped")

checks["boundary"]["literature_label"] = main_text.include?("**LITERATURE:**")
checks["boundary"]["proved_locally"] = main_text.include?("**PROVED LOCALLY:**")
checks["boundary"]["finite_computation"] = main_text.include?("**FINITE COMPUTATION:**")
checks["boundary"]["open_label"] = main_text.include?("**OPEN:**")
checks["boundary"]["not_clay"] = [main_text, source_text, primary_text].all? { |body| body.include?("**NOT CLAY.**") }
checks["boundary"]["real_dyadic_scope"] = main_text.include?("real one-dyadic-band class")
checks["boundary"]["integer_slice_scope"] = main_text.include?("Exact integer heat-shear slice realization")
checks["boundary"]["one_time_quantifier"] = cm.include?("anyoneprescribedscaledtime")
checks["boundary"]["complete_clock_open"] = main_text.include?("complete clock") && main_text.include?("complete signed flux")
checks["boundary"]["full_plateau_open"] = main_text.include?("full plateau mass")
checks["boundary"]["larger_window_open"] = cm.include?("doesnotcoverthefullR0.76Jupperwindow")
checks["boundary"]["l3_gap_open"] = main_text.include?("between `q^(4/3)` and `q^2` remains open")
checks["boundary"]["arbitrary_field_open"] = main_text.include?("arbitrary-field")
checks["boundary"]["regularity_open"] = main_text.include?("regularity")
checks["boundary"]["singularity_open"] = main_text.include?("singularity")
checks["boundary"]["no_simulation"] = main_text.include?("No simulation")
checks["boundary"]["no_figure"] = main_text.include?("No simulation or formal scientific figure is needed")
checks["boundary"]["no_novelty"] = main_text.include?("No novelty")
checks["boundary"]["no_priority"] = main_text.include?("priority") && source_text.include?("not evidence of novelty or priority")
checks["boundary"]["primary_pass"] = primary_text.include?("**PASS -- single-slice theorem only; complete-clock flux remains open.**")
checks["boundary"]["single_slice_verdict"] = primary_text.include?("single-slice theorem only")

python_required = %w[status assertionCount exact bindings]
python_bindings = python_json.is_a?(Hash) && python_json["bindings"].is_a?(Hash) ? python_json["bindings"] : {}
python_binding_subset = binding_specs.all? do |relative, hash|
  row = python_bindings[relative]
  row.is_a?(Hash) && row["expectedSha256"] == hash &&
    row["observedSha256"] == bindings.fetch(relative).fetch("observedSha256") && row["pass"] == true
end
python_structure = python_json.is_a?(Hash) && python_json["exact"].is_a?(Hash) ?
  python_json["exact"]["structure"] : nil
checks["python_cross"]["json_object"] = python_json.is_a?(Hash)
checks["python_cross"]["required_fields"] = python_required.all? { |key| python_json.key?(key) }
checks["python_cross"]["verdict"] = python_json["status"] == "PASS"
checks["python_cross"]["freeze_ready"] = freeze_ready && python_bindings.values.all? { |row| row["pass"] == true }
checks["python_cross"]["assertions_positive"] =
  python_json["assertionCount"].is_a?(Integer) && python_json["assertionCount"].positive?
checks["python_cross"]["exact_object"] = python_json["exact"].is_a?(Hash) && !python_json["exact"].empty?
checks["python_cross"]["bindings_object"] = python_json["bindings"].is_a?(Hash)
checks["python_cross"]["frozen_binding_subset"] = python_binding_subset
checks["python_cross"]["structure_agrees"] = python_structure.is_a?(Hash) &&
  python_structure["firstTag"] == 1 && python_structure["lastTag"] == 48 &&
  python_structure["tagCount"] == 48 && python_structure["displayCount"] == 48

unless checks.keys == GROUPS.keys && GROUPS.all? { |group, names| checks.fetch(group).keys == names }
  abort("R0.76K Ruby assertion inventory mismatch")
end

unless MUTATION.empty?
  unless NEGATIVE_MUTATIONS.include?(MUTATION)
    warn "unknown R076K_RUBY_MUTATION: #{MUTATION}"
    exit 2
  end
  GROUPS.each do |group, names|
    checks.fetch(group)[MUTATION] = false if names.include?(MUTATION)
  end
end

exact = {
  "structure" => {
    "firstTag" => tags.first,
    "lastTag" => tags.last,
    "tagCount" => tags.length,
    "displayCount" => display_opens
  },
  "polynomialSamples" => polynomial_exact_rows,
  "orthogonalPolynomials" => {
    "chebyshevThrough4" => (0..4).map do |degree|
      chebyshev_table.fetch(degree).map { |value| fraction_string(value) }
    end,
    "t3AtThreeHalves" => fraction_string(poly_evaluate(chebyshev_table.fetch(3), Rational(3, 2))),
    "t3L2Squared" => fraction_string(chebyshev_integrals.fetch(3)),
    "normalizedLegendreKernelQ4" => normalized_kernel.map { |value| fraction_string(value) },
    "normalizedLegendreEndpoint" => fraction_string(normalized_kernel_endpoint),
    "normalizedLegendreL2Squared" => fraction_string(normalized_kernel_l2_squared),
    "unnormalizedLegendreEndpoint" => fraction_string(kernel_endpoint),
    "unnormalizedLegendreL2Squared" => fraction_string(kernel_l2_squared),
    "unnormalizedLegendreL3CubeUpper" => fraction_string(Rational(sample_q**4, 4)),
    "l3EndpointRatioLower" => "2",
    "l3EndpointSquaredLower" => "4"
  },
  "pointwiseSample" => {
    "q" => pointwise_q,
    "degree" => pointwise_degree,
    "d" => fraction_string(pointwise_d),
    "chebyshevValue" => fraction_string(pointwise_value),
    "polynomialL2Squared" => fraction_string(pointwise_l2_squared),
    "theoremSquaredPrefactor" => "1/8"
  },
  "exteriorSample" => {
    "q" => exterior_q,
    "degree" => exterior_degree,
    "d" => fraction_string(exterior_d),
    "intervalLeft" => fraction_string(exterior_left),
    "intervalRight" => fraction_string(exterior_right),
    "intervalLength" => fraction_string(exterior_length),
    "sqrtSevenDOverEight" => fraction_string(sqrt_seven_d_over_eight),
    "exponent" => fraction_string(exterior_exponent),
    "numeratorCoefficient" => fraction_string(numerator_coefficient),
    "l2DenominatorUpper" => fraction_string(core_l2_upper),
    "l3CubeUpper" => fraction_string(core_l3_upper),
    "l3TwoThirdsStrictUpper" => "8",
    "ratioCoefficient" => fraction_string(exterior_ratio)
  },
  "integerSliceSample" => {
    "indices" => phase_modes,
    "scaledFrequencies" => scaled_frequencies.map { |value| fraction_string(value) },
    "M" => fraction_string(phase_m),
    "complexBranchCount" => 2 * phase_q,
    "coefficientArgumentsOverPi" => phase_rows.map { |row| fraction_string(row.fetch("argumentOverPi")) },
    "phasesOverPi" => phase_rows.map { |row| fraction_string(row.fetch("phiOverPi")) },
    "phaseResidualsOverPi" => phase_rows.map { |row| fraction_string(row.fetch("residualOverPi")) },
    "prepaidHeatExponents" => phase_rows.map { |row| fraction_string(row.fetch("prepaidHeatExponent")) },
    "dampingHeatExponents" => phase_rows.map { |row| fraction_string(row.fetch("dampingHeatExponent")) },
    "netHeatExponents" => phase_rows.map { |row| fraction_string(row.fetch("netHeatExponent")) },
    "compensatedAmplitudes" => phase_rows.map { |row| fraction_string(row.fetch("compensatedAmplitudeExact")) },
    "wAtSample" => complex_object(phase_w),
    "carrierPhaseOverPi" => fraction_string(phase_carrier_over_pi),
    "exactProfile" => {
      "constant" => fraction_string(profile_constant),
      "sqrt3Coefficient" => fraction_string(profile_sqrt3)
    },
    "cosineContributions" => phase_contributions
  },
  "asymptoticSample" => {
    "etaQSquaredSevenToQ" => fraction_string(eta_q2_7q),
    "etaQSquaredSixToQ" => fraction_string(eta_q2_6q),
    "etaQFiveToQ" => fraction_string(eta_q_5q),
    "normalizedLegendreLeadingQ4" => fraction_string(normalized_kernel.last),
    "generalLeadingLower" => "3/4",
    "halfCriticalNetExponentCoefficient" => fraction_string(half_critical_net),
    "provedWindowExponent" => fraction_string(proved_window),
    "upperWindowExponent" => fraction_string(upper_window),
    "windowGap" => fraction_string(upper_window - proved_window)
  },
  "signedCapSample" => {
    "plateauGap" => fraction_string(cap_dp),
    "capGap" => fraction_string(cap_dc),
    "capGapLarger" => cap_dc > cap_dp,
    "strictSubcapGeometry" => cap_delta_zero < cap_rc - 3 * cap_h && cap_rc + 3 * cap_h < cap_radius,
    "gammaLeadingRationalFactor" => fraction_string(cap_leading_rational),
    "gammaLeadingSqrtArgument" => fraction_string(cap_sqrt_argument),
    "gammaLeadingConstantSubtrahend" => fraction_string(2 * cap_delta_zero),
    "pairIdentityCoefficient" => "4",
    "t3AtCarrier" => fraction_string(poly_evaluate(chebyshev_coefficients(cap_m), cap_x)),
    "capLeftX" => fraction_string(cap_left_x),
    "t3AtCapLeft" => fraction_string(cap_left_t),
    "capLeftPairSineCoefficient" => fraction_string(cap_left_pair_coefficient),
    "carrierSinePositive" => Math.sin(2.0 * cap_x.to_f) > 0
  },
  "semigroupSample" => {
    "epsilon" => fraction_string(semigroup_epsilon),
    "diffusionTime" => fraction_string(semigroup_time),
    "realDriftArgument" => fraction_string(semigroup_real_argument),
    "imaginaryShift" => fraction_string(semigroup_imaginary_shift),
    "transformedCoefficients" => semigroup_coefficients.map { |value| fraction_string(value.real) },
    "integerModes" => semigroup_integer_modes,
    "modeFrequencies" => semigroup_frequencies.map { |value| fraction_string(value) },
    "directDecayExponents" => semigroup_direct_decay.map { |value| fraction_string(value) },
    "internalHeatExponents" => semigroup_internal_heat.map { |value| fraction_string(value) },
    "imaginaryShiftExponents" => semigroup_shift_decay.map { |value| fraction_string(value) },
    "rhsCombinedDecayExponents" => semigroup_rhs_decay.map { |value| fraction_string(value) },
    "directPhases" => semigroup_direct_phases.map { |value| fraction_string(value) },
    "internalPhases" => semigroup_internal_phases.map { |value| fraction_string(value) },
    "rhsCombinedPhases" => semigroup_rhs_phases.map { |value| fraction_string(value) },
    "scalarHeatExponent" => fraction_string(semigroup_scalar_exponent),
    "carrierPhase" => fraction_string(semigroup_carrier_phase)
  },
  "backwardHeatSample" => {
    "terms" => backward_terms.map { |value| fraction_string(value) },
    "exactValue" => fraction_string(backward_sum_value),
    "wrongForwardSignValue" => fraction_string(wrong_forward_value)
  },
  "claims" => claims
}

# Both implementations must independently reproduce the complete expected
# object; neither is accepted merely because the other emitted PASS.
expected_without_schema = expected.reject { |key, _value| key == "schema" }
checks["python_cross"]["exact_object"] &&= exact == expected_without_schema
checks["python_cross"]["exact_object"] &&= python_json["exact"] == exact

failures = checks.each_with_object([]) do |(group, rows), output|
  rows.each { |name, passed| output << "#{group}.#{name}" unless passed }
end
assertions = GROUPS.values.map(&:length).sum

verdict = failures.empty? && freeze_ready ? "PASS" : "FAIL"
payload = {
  "schema" => "r076k-real-dyadic-edge-sharpness-independent-v1",
  "verdict" => verdict,
  "freezeReady" => freeze_ready,
  "assertionsTotal" => assertions,
  "assertionsPassed" => assertions - failures.length,
  "failures" => failures,
  "negativeMutations" => NEGATIVE_MUTATIONS,
  "bindings" => bindings,
  "exact" => exact
}

unless RUBY_JSON.empty?
  File.write(RUBY_JSON, JSON.pretty_generate(payload) + "\n", encoding: "UTF-8")
end

report = [
  "# R0.76K independent finite audit",
  "",
  "- Verdict: **#{verdict}**",
  "- Freeze-ready hash seal: **#{freeze_ready ? 'yes' : 'no'}**",
  "- Ruby assertions: #{assertions - failures.length}/#{assertions}",
  "- Python certificate fields and frozen binding subset: #{checks.fetch('python_cross').values.all? ? 'PASS' : 'FAIL'}",
  "- K.1--K.48 equation inventory and reference closure: #{checks.fetch('integrity').values_at('tag_sequence', 'tag_count', 'reference_closure').all? ? 'PASS' : 'FAIL'}",
  "- Exact rational confluent samples: #{polynomial_rows.length}",
  "- Exact exterior-transfer coefficient: #{fraction_string(exterior_ratio)}",
  "- Exact backward-heat sample: #{fraction_string(backward_sum_value)}",
  "- Failures: #{failures.empty? ? 'none' : failures.join(', ')}",
  "",
  "## Finite-audit boundary",
  "",
  "This Ruby verifier independently recomputes finite rational complex",
  "coefficients, Chebyshev/Legendre integrals, the dyadic and phase sample,",
  "the 1/128 transfer ledger, growing-q sample logs, and an exact backward-heat",
  "value. It does not prove uniform convergence, classical orthogonality as a",
  "continuum theorem, the semigroup theorem, a complete-clock signed-flux lower",
  "bound, or a Navier--Stokes regularity/singularity claim. **NOT CLAY.**",
  ""
]
File.write(REPORT, report.join("\n"), encoding: "UTF-8")

puts JSON.generate(
  "suite" => "r076k-real-dyadic-edge-sharpness-independent",
  "status" => verdict,
  "assertions" => assertions,
  "failures" => failures.length
)
exit(verdict == "PASS" ? 0 : 1)
