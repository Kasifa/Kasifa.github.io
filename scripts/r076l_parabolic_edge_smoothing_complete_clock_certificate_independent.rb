#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent, fail-closed finite verifier for R0.76L.
#
# This Ruby 2.6-compatible implementation uses only the standard library. It
# independently recomputes the rational and Q(alpha), alpha^3=2, ledgers, the
# heat-polynomial and integer-shear samples, the collar/plateau geometry, the
# physical normalization, the backward-heat sample, and the archived figure
# diagnostics.  Only after those checks are complete does it read the Python
# JSON for an exact cross-implementation comparison.  The finite certificate
# does not prove the continuum Laplace principle, the uniform Duhamel limit,
# or any Navier--Stokes regularity/singularity statement.  NOT CLAY.

require "csv"
require "digest"
require "json"
require "zlib"
require "open3"

ROOT = File.expand_path("..", __dir__)
STEM = "r076l_parabolic_edge_smoothing_complete_clock"
FIXTURE_PATH = File.join(ROOT, "scripts", "#{STEM}_fixtures.json")
EXPECTED_PATH = File.join(ROOT, "scripts", "#{STEM}_expected.json")
PYTHON_JSON_PATH = ENV.fetch("R076L_JSON", File.join(ROOT, "research", "#{STEM}_certificate.json"))
REPORT_PATH = ENV.fetch("R076L_RUBY_REPORT", File.join(ROOT, "research", "#{STEM}_independent_audit.md"))
RUBY_JSON_PATH = ENV.fetch("R076L_RUBY_JSON", "")
MUTATION = ENV.fetch("R076L_RUBY_MUTATION", "")
DEVELOPMENT = ENV.fetch("R076L_DEVELOPMENT", "") == "1"

FIXTURE_SCHEMA = "r076l-parabolic-edge-smoothing-complete-clock-fixtures-v1"
EXPECTED_SCHEMA = "r076l-parabolic-edge-smoothing-complete-clock-expected-v1"
INDEPENDENT_SCHEMA = "r076l-parabolic-edge-smoothing-complete-clock-independent-v1"
UPSTREAM_CORE_COMMIT = "8a89aee4fe0839de44e21a90ba827a9cc77b3062"
FIXTURE_SHA256 = "cf442a934bd713ef046f1aa5b6f41ea5a1cfe118e6cef91a30d20a26d16bd1a9"
EXPECTED_SHA256 = "48dc286d198512034aaee9ce65ef696fe367942c9ea9a6e840ac0e7c31c2f8ed"
SHA256_PATTERN = /\A[0-9a-f]{64}\z/
COMMIT_PATTERN = /\A[0-9a-f]{40}\z/

GROUPS = {
  "bindings" => %w[
    hash_inventory hash_specs_well_formed fixture_self_hash expected_self_hash
    all_frozen_hashes source_commit_ready
    upstream_commit_exact upstream_commit_stated upstream_hashes_stated
    core_objects_bound figure_objects_bound generated_outputs_unbound
  ],
  "inputs" => %w[
    fixture_schema expected_schema fixture_object expected_object fixture_keys
    expected_keys file_inventory structure_inventory scale_inventory
    saddle_inventory tilt_inventory heat_series_inventory integer_shear_inventory
    operator_inventory geometry_inventory normalization_inventory backward_inventory
    diagnostic_inventory claims_inventory
  ],
  "integrity" => %w[
    main_utf8 source_utf8 primary_utf8 fixture_utf8 expected_utf8 no_controls
    no_cr no_trailing tag_sequence tag_unique tag_count display_balance
    display_count reference_closure
  ],
  "scale" => %w[
    scale_sample_domain m_squared_over_a mu_cube mu_value sqrt_a gamma_value gamma_square
    terminal_layer clock_residual fixed_slice common_heat strict_order
    power_rows power_gamma power_mu power_mu_squared power_backward
  ],
  "cubic_saddle" => %w[
    generator_cube isolating_interval basis_order z4 sqrt_two_z4 f4 g4 two_g4
    z4_cube f4_cube f3_cube f4_minus_f3 g4_cube z4_over_eight
    sqrt_square two_z4 rate_function terminal_dominance gap_value ratio_slope
    ratio_slope_cube
  ],
  "tilt" => %w[
    tilt_sample_domain delta_c centered_y linear_tilt constant_penalty kernel_ratio_tilt
    kernel_ratio_squares identities_agree positive_sign
  ],
  "heat_series" => %w[
    chebyshev_recurrence coefficients endpoint_direct endpoint_formula
    derivative_ratios derivatives_positive forward_coefficients backward_coefficients
    evaluation_point forward_value backward_value positive_weights weight_sum
    mean_j mean_ell mean_ell_pair pde_identity j_ratios increasing_forward_backward
  ],
  "integer_shear" => %w[
    shear_sample_domain w_coefficients substitution_coefficients derivative_coefficients
    coefficient_formulas_agree coefficients_nonzero carrier modes amplitudes phases
    strict_modes dyadic_band pde_mode pde_time_cosine pde_time_sine
    pde_transport_sine pde_laplacian_cosine pde_cosine_residual pde_sine_residual
    exact_shear_text
  ],
  "operator" => %w[
    operator_sample_domain l_eta second_derivative difference first_order_sign
    degree_preserved operator_text weighted_norm_text duhamel_text confluence_rate_text
  ],
  "geometry_clock" => %w[
    geometry_sample_domain a_value e_a scaled_velocity background_shear gamma
    subcap_left subcap_right strict_subcap positive_coordinate negative_coordinate
    paired_gap subcap_coordinate plateau_coordinate cap_plateau_gap
    terminal_cap terminal_plateau terminal_gap strip_z strip_width
    area_endpoints integrated_area velocity_sign weight_sign square_difference_sign
    flux_sign complete_clock_absorption_text
  ],
  "normalization" => %w[
    flux_monomial mass_monomial unweighted_quotient r_weighted_quotient
    lower_a_power lower_h_power upper_a_power upper_h_power normalized_plateau
    normalized_flux normalized_quotient omega_third_rate a_square_density
    penalty_coefficient penalty_log_rate formal_status formal_saddle
    formal_displacement formal_tilt formal_squared_ratio formal_critical_kappa
    formal_threshold open_boundary_text
  ],
  "backward_heat" => %w[
    backward_sample_domain chebyshev_degree terms backward_polynomial forward_polynomial
    backward_absolute forward_absolute imaginary_coefficients imaginary_terms
    imaginary_value forward_backward_distinct
  ],
  "diagnostic" => %w[
    config_schema config_parameters csv_shape csv_columns grid_cartesian degree_policy
    mu_identity limit_decimals saddle_residual coarse_amplitude coarse_tilt
    phase_amplitude phase_tilt finite_values progress_count progress_stages
    resource_count png_signature png_crc png_pixels png_dpi pdf_pages pdf_unencrypted
    pdf_no_javascript svg_dimensions panel_count away_sequence monotonicity_boundary
    finite_only
  ],
  "sources" => %w[
    dlmf_185 dlmf_189 dlmf_1814 hall_ho kabluchko dominici
    batahan_shehata khan rosenbloom_widder ditzian bounded_search
    operational_prior_art no_novelty_priority search_stop deep_research_boundary
  ],
  "boundary" => %w[
    explicit_family forward_heat complete_clock_positive full_plateau normalized_rate
    scale_reduction candidate_killed formal_figure finite_diagnostic
    no_terminal_prepaid arbitrary_open a2_boundary_open bulk_a4_open version_m_open
    regularity_open singularity_open no_simulation finite_not_proof no_novelty
    no_priority not_clay primary_pass
  ],
  "python_cross" => %w[
    json_available json_object required_fields python_pass python_freeze_ready assertion_count
    exact_object exact_agrees bindings_object binding_subset structure_agrees
  ]
}.freeze

NEGATIVE_MUTATIONS = %w[
  source_commit_missing source_hash_drift fixture_schema expected_schema
  heat_time_changed heat_edge_changed shear_eta_changed shear_mode_changed
  shear_drift_changed operator_sign_changed geometry_drift_changed
  geometry_radius_changed physical_R_power physical_A_power plateau_R_power
  omega_rate_changed high_degree_parameter arbitrary_packet_upgrade
  diagnostic_to_proof diagnostic_row_count equation_tag_changed
  source_boundary_removed progress_missing_complete figure_limit_changed
  generated_output_bound agents_file_bound
].freeze
abort("duplicate mutation name in R0.76L Ruby suite") unless
  NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

if ENV.fetch("R076L_RUBY_LIST_MUTATIONS", "") == "1"
  puts NEGATIVE_MUTATIONS
  exit 0
end
unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
  warn "unknown R076L_RUBY_MUTATION: #{MUTATION}"
  exit 2
end

def read_json(path, label)
  JSON.parse(File.read(path, encoding: "UTF-8"))
rescue Errno::ENOENT, JSON::ParserError => error
  warn "R0.76L #{label} unavailable or invalid: #{error.message}"
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
  rational = value.is_a?(Rational) ? value : Rational(value)
  rational.denominator == 1 ? rational.numerator.to_s : "#{rational.numerator}/#{rational.denominator}"
end

def exact_root(value, degree)
  rational = Rational(value)
  raise ArgumentError, "positive root required" if rational.negative?
  root = lambda do |integer|
    lo, hi = 0, integer + 1
    while lo + 1 < hi
      mid = (lo + hi) / 2
      mid**degree <= integer ? lo = mid : hi = mid
    end
    raise ArgumentError, "non-rational sample root" unless lo**degree == integer
    lo
  end
  Rational(root.call(rational.numerator), root.call(rational.denominator))
end

def factorial(n)
  (1..n).reduce(1, :*)
end

def sha256(relative)
  path = File.join(ROOT, relative)
  File.file?(path) ? Digest::SHA256.file(path).hexdigest : nil
end

def poly_trim(coefficients)
  output = coefficients.dup
  output.pop while output.length > 1 && output.last == 0
  output
end

def poly_pad(coefficients, length)
  coefficients + Array.new([length - coefficients.length, 0].max, 0)
end

def poly_add(left, right)
  length = [left.length, right.length].max
  poly_trim((0...length).map { |index| (left[index] || 0) + (right[index] || 0) })
end

def poly_scale(coefficients, scalar)
  poly_trim(coefficients.map { |value| value * scalar })
end

def poly_shift(coefficients)
  [0] + coefficients
end

def poly_multiply(left, right)
  output = Array.new(left.length + right.length - 1, 0)
  left.each_with_index do |left_value, left_index|
    right.each_with_index do |right_value, right_index|
      output[left_index + right_index] += left_value * right_value
    end
  end
  poly_trim(output)
end

def poly_derivative(coefficients, order = 1)
  output = coefficients.dup
  order.times do
    return [0] if output.length <= 1

    output = (1...output.length).map { |index| output[index] * index }
  end
  poly_trim(output)
end

def poly_evaluate(coefficients, value)
  coefficients.reverse.reduce(0) { |total, coefficient| total * value + coefficient }
end

def poly_compose(outer, inner)
  outer.reverse.reduce([0]) do |output, coefficient|
    poly_add(poly_multiply(output, inner), [coefficient])
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

def heat_polynomial(coefficients, time, sign)
  output = [Rational(0)]
  (0..((coefficients.length - 1) / 2)).each do |j|
    derivative = poly_derivative(coefficients, 2 * j)
    factor = ((sign**j) * (time**j)) / factorial(j)
    output = poly_add(output, poly_scale(derivative, factor))
  end
  poly_pad(output, coefficients.length)
end

def complex_pair(value)
  [fraction_string(value.real), fraction_string(value.imag)]
end

def png_metadata(path)
  raw = File.binread(path)
  return {"signature" => false, "crc" => false} unless raw.start_with?("\x89PNG\r\n\x1A\n".b)

  offset = 8
  width = nil
  height = nil
  x_pixels_per_metre = nil
  y_pixels_per_metre = nil
  unit = nil
  crc_ok = true
  while offset + 12 <= raw.bytesize
    length = raw.byteslice(offset, 4).unpack("N").first
    type = raw.byteslice(offset + 4, 4)
    data = raw.byteslice(offset + 8, length)
    stored_crc = raw.byteslice(offset + 8 + length, 4).unpack("N").first
    crc_ok &&= Zlib.crc32(type + data) == stored_crc
    if type == "IHDR"
      width, height = data.unpack("NN")
    elsif type == "pHYs"
      x_pixels_per_metre, y_pixels_per_metre, unit = data.unpack("NNC")
    end
    offset += 12 + length
    break if type == "IEND"
  end
  dpi = if unit == 1 && x_pixels_per_metre == y_pixels_per_metre
          (x_pixels_per_metre * 0.0254).round
        end
  {"signature" => true, "crc" => crc_ok, "width" => width, "height" => height, "dpi" => dpi}
end

# Exact arithmetic in Q(alpha), alpha^3=2, represented in the basis
# (1, alpha, alpha^2).
class CubicTwo
  attr_reader :coefficients

  def initialize(c0 = 0, c1 = 0, c2 = 0)
    @coefficients = [Rational(c0), Rational(c1), Rational(c2)].freeze
  end

  def +(other)
    right = self.class.convert(other)
    CubicTwo.new(*@coefficients.each_index.map { |index| @coefficients[index] + right.coefficients[index] })
  end

  def -@
    CubicTwo.new(*@coefficients.map { |value| -value })
  end

  def -(other)
    self + (-self.class.convert(other))
  end

  def *(other)
    right = self.class.convert(other)
    a0, a1, a2 = @coefficients
    b0, b1, b2 = right.coefficients
    CubicTwo.new(
      a0 * b0 + 2 * (a1 * b2 + a2 * b1),
      a0 * b1 + a1 * b0 + 2 * a2 * b2,
      a0 * b2 + a1 * b1 + a2 * b0
    )
  end

  def /(scalar)
    rational = Rational(scalar)
    CubicTwo.new(*@coefficients.map { |value| value / rational })
  end

  def **(power)
    raise ArgumentError, "negative CubicTwo exponent" if power.negative?

    result = CubicTwo.new(1)
    base = self
    exponent = power
    while exponent.positive?
      result *= base if exponent.odd?
      base *= base
      exponent /= 2
    end
    result
  end

  def ==(other)
    @coefficients == self.class.convert(other).coefficients
  rescue TypeError
    false
  end

  def coerce(other)
    [self.class.convert(other), self]
  end

  def to_a
    @coefficients.map { |value| fraction_string(value) }
  end

  def self.convert(value)
    return value if value.is_a?(CubicTwo)
    return CubicTwo.new(value) if value.is_a?(Integer) || value.is_a?(Rational)

    raise TypeError, "cannot convert #{value.class} to CubicTwo"
  end
end

fixtures = read_json(FIXTURE_PATH, "fixtures")
expected = read_json(EXPECTED_PATH, "expected values")

# Controls alter parsed inputs before independent computation. No assertion
# or verdict is forcibly changed; the ordinary checks must find the fault.
input_mutations = {
  "source_commit_missing" => [["frozen", "sourceCommit"], "0" * 40],
  "fixture_schema" => [["schema"], "corrupted"],
  "heat_time_changed" => [["heatSeriesSample", "time"], "2"],
  "heat_edge_changed" => [["heatSeriesSample", "edgeCoordinate"], "3"],
  "shear_eta_changed" => [["integerShearSample", "eta"], "2"],
  "shear_mode_changed" => [["integerShearSample", "firstMode"], 5],
  "shear_drift_changed" => [["integerShearSample", "backgroundShear"], "3"],
  "operator_sign_changed" => [["operatorSample", "eta"], "-1/4"],
  "geometry_drift_changed" => [["geometryClockSample", "beta"], "-9/40"],
  "geometry_radius_changed" => [["geometryClockSample", "pairedRadius"], "3"],
  "physical_R_power" => [["normalizationSample", "physicalFluxRExponent"], "4"],
  "physical_A_power" => [["normalizationSample", "physicalFluxAExponent"], "3"],
  "plateau_R_power" => [["normalizationSample", "plateauMassRExponent"], "6"],
  "omega_rate_changed" => [["normalizationSample", "omegaLogRate"], "-4/3969"],
  "high_degree_parameter" => [["normalizationSample", "formalKappa"], "8"],
  "arbitrary_packet_upgrade" => [["claims", "uniformArbitraryPacketTheorem"], true],
  "diagnostic_to_proof" => [["claims", "finiteDiagnosticProvesLimit"], true],
  "diagnostic_row_count" => [["diagnostic", "rowCount"], 15]
}
if input_mutations.key?(MUTATION)
  path, value = input_mutations.fetch(MUTATION)
  target = path[0...-1].reduce(fixtures) { |object, key| object.fetch(key) }
  target[path.last] = value
end
expected["schema"] = "corrupted" if MUTATION == "expected_schema"
if MUTATION == "source_hash_drift"
  fixtures["frozen"]["sha256"][fixtures["files"]["main"]] = "0" * 64
elsif MUTATION == "generated_output_bound"
  fixtures["frozen"]["sha256"]["research/#{STEM}_certificate.json"] = "0" * 64
elsif MUTATION == "agents_file_bound"
  fixtures["frozen"]["sha256"]["AGENTS.md"] = sha256("AGENTS.md")
end

files = fixtures.is_a?(Hash) && fixtures["files"].is_a?(Hash) ? fixtures["files"] : {}
frozen = fixtures.is_a?(Hash) && fixtures["frozen"].is_a?(Hash) ? fixtures["frozen"] : {}
frozen_hashes = frozen["sha256"].is_a?(Hash) ? frozen["sha256"] : {}
self_binding_specs = {
  "scripts/#{STEM}_fixtures.json" => FIXTURE_SHA256,
  "scripts/#{STEM}_expected.json" => EXPECTED_SHA256
}.freeze
binding_specs = frozen_hashes.merge(self_binding_specs).freeze

raw_by_name = files.each_with_object({}) do |(name, relative), output|
  begin
    output[name] = File.binread(File.join(ROOT, relative))
  rescue Errno::ENOENT
    output[name] = "".b
  end
end
raw_by_name["main"] = raw_by_name["main"].sub("\\tag{L.1}", "\\tag{L.999}") if MUTATION == "equation_tag_changed"
raw_by_name["source"] = raw_by_name["source"].gsub("NOT CLAY.", "REMOVED") if MUTATION == "source_boundary_removed"
if MUTATION == "progress_missing_complete"
  raw_by_name["figureProgress"] = raw_by_name["figureProgress"].lines.reject { |line| line.include?('"stage": "complete"') }.join
elsif MUTATION == "figure_limit_changed"
  raw_by_name["figureData"] = raw_by_name["figureData"].gsub("0.396850262992", "0.500000000000")
end
text_by_name = raw_by_name.transform_values { |raw| raw.dup.force_encoding("UTF-8") }
main_text = text_by_name.fetch("main", "")
source_text = text_by_name.fetch("source", "")
primary_text = text_by_name.fetch("primaryAudit", "")
compact_main = compact(main_text)
compact_source = compact(source_text)
compact_primary = compact(primary_text)

bindings = binding_specs.keys.sort.each_with_object({}) do |relative, output|
  expected_hash = binding_specs[relative]
  observed_hash = sha256(relative)
  output[relative] = {
    "expectedSha256" => expected_hash,
    "observedSha256" => observed_hash || "MISSING",
    "exists" => !observed_hash.nil?,
    "locked" => expected_hash.is_a?(String) && SHA256_PATTERN.match?(expected_hash),
    "pass" => expected_hash.is_a?(String) && SHA256_PATTERN.match?(expected_hash) && observed_hash == expected_hash
  }
end
source_commit_ready = COMMIT_PATTERN.match?(frozen["sourceCommit"].to_s)
source_tree_ready = source_commit_ready && frozen_hashes.keys.all? do |relative|
  bytes, _error, status = Open3.capture3("git", "-C", ROOT, "show", "#{frozen['sourceCommit']}:#{relative}")
  status.success? && File.file?(File.join(ROOT, relative)) && bytes.b == File.binread(File.join(ROOT, relative))
end
freeze_ready = source_tree_ready && bindings.values.all? { |row| row["pass"] } && !DEVELOPMENT

tags = main_text.scan(/\\tag\{L\.(\d+)\}/).flatten.map(&:to_i)
references = main_text.scan(/(?<![A-Za-z0-9_.])L\.(\d+)/).flatten.map(&:to_i)
display_opens = main_text.scan(/^\\\[$/).length
display_closes = main_text.scan(/^\\\]$/).length

# Scale ledger.
scale_fixture = fixtures.fetch("scaleSample")
scale_a = Integer(scale_fixture.fetch("A"))
scale_m = Integer(scale_fixture.fetch("m"))
scale_m2_over_a = Rational(scale_m**2, scale_a)
scale_mu_cube = scale_m2_over_a
scale_mu = exact_root(scale_m2_over_a, 3)
scale_sqrt_a = exact_root(scale_a, 2)
scale_gamma = Rational(scale_m, scale_sqrt_a)
scale_h = Rational(1, 1 + scale_mu**2)
power_rows = scale_fixture.fetch("alphaValues").map do |value|
  alpha_value = fraction(value)
  {
    "alpha" => fraction_string(alpha_value),
    "gammaExponent" => fraction_string(alpha_value - Rational(1, 2)),
    "muExponent" => fraction_string((2 * alpha_value - 1) / 3),
    "muSquaredExponent" => fraction_string((4 * alpha_value - 2) / 3),
    "backwardExponent" => fraction_string(2 * alpha_value - 2)
  }
end

# Exact cubic-field saddle ledger.
saddle_fixture = fixtures.fetch("saddleSample")
alpha = CubicTwo.new(0, 1, 0)
z4 = alpha**5
sqrt_two_z4 = 2 * alpha
f4 = sqrt_two_z4 - (z4 * z4) / 16
g4 = z4 / 8
two_g4 = 2 * g4
saddle_gap = fraction(saddle_fixture.fetch("capPlateauGap"))
squared_ratio_slope = two_g4 * saddle_gap
generator_left = fraction(saddle_fixture.fetch("generatorIsolatingInterval").fetch(0))
generator_right = fraction(saddle_fixture.fetch("generatorIsolatingInterval").fetch(1))

# Exact Gaussian tilt identity sample.
tilt_fixture = fixtures.fetch("tiltSample")
tilt_s = fraction(tilt_fixture.fetch("heatTime"))
tilt_y = fraction(tilt_fixture.fetch("y"))
tilt_c1 = fraction(tilt_fixture.fetch("c1"))
tilt_c2 = fraction(tilt_fixture.fetch("c2"))
tilt_delta_c = tilt_c2 - tilt_c1
tilt_centered_y = tilt_y - tilt_c1
tilt_linear = tilt_delta_c * tilt_centered_y / (2 * tilt_s)
tilt_penalty = tilt_delta_c**2 / (4 * tilt_s)
tilt_ratio = tilt_linear - tilt_penalty
tilt_ratio_square = ((tilt_y - tilt_c1)**2 - (tilt_y - tilt_c2)**2) / (4 * tilt_s)

# Exact T_4 heat-series ledger.
heat_fixture = fixtures.fetch("heatSeriesSample")
heat_degree = Integer(heat_fixture.fetch("degree"))
heat_a = fraction(heat_fixture.fetch("A"))
heat_s = fraction(heat_fixture.fetch("time"))
heat_c = fraction(heat_fixture.fetch("edgeCoordinate"))
heat_t = heat_s / heat_a**2
heat_chebyshev = chebyshev_coefficients(heat_degree)
endpoint_direct = (0..heat_degree).map do |order|
  poly_evaluate(poly_derivative(heat_chebyshev, order), Rational(1))
end
endpoint_formula = (0..heat_degree).map do |order|
  if order.zero?
    Rational(1)
  else
    numerator = (1...order).reduce(Rational(heat_degree**2)) do |value, r|
      value * (heat_degree**2 - r**2)
    end
    denominator = (1..order).reduce(1) { |value, r| value * (2 * r - 1) }
    numerator / denominator
  end
end
derivative_ratios = (0...heat_degree).map do |order|
  endpoint_formula.fetch(order + 1) / endpoint_formula.fetch(order)
end
forward_heat = heat_polynomial(heat_chebyshev, heat_t, 1)
backward_heat = heat_polynomial(heat_chebyshev, heat_t, -1)
heat_x = Rational(1) + heat_c / heat_a
forward_heat_value = poly_evaluate(forward_heat, heat_x)
backward_heat_value = poly_evaluate(backward_heat, heat_x)
positive_weights = []
(0..(heat_degree / 2)).each do |j|
  (0..(heat_degree - 2 * j)).each do |ell|
    k = ell + 2 * j
    weight = endpoint_formula.fetch(k) * (heat_c**ell) * (heat_s**j) /
      ((heat_a**k) * factorial(ell) * factorial(j))
    positive_weights << {"ell" => ell, "j" => j, "k" => k, "value" => fraction_string(weight)}
  end
end
weight_values = positive_weights.map { |row| fraction(row.fetch("value")) }
weight_sum = weight_values.sum
mean_j = positive_weights.each_with_index.reduce(Rational(0)) do |sum, (row, index)|
  sum + row.fetch("j") * weight_values.fetch(index)
end / weight_sum
mean_ell = positive_weights.each_with_index.reduce(Rational(0)) do |sum, (row, index)|
  sum + row.fetch("ell") * weight_values.fetch(index)
end / weight_sum
mean_ell_pair = positive_weights.each_with_index.reduce(Rational(0)) do |sum, (row, index)|
  ell = row.fetch("ell")
  sum + ell * (ell - 1) * weight_values.fetch(index)
end / weight_sum
ell_zero_weights = positive_weights.select { |row| row["ell"].zero? }.map { |row| fraction(row["value"]) }
ell_zero_ratios = ell_zero_weights.each_cons(2).map { |left, right| right / left }

# Exact integer shear and coefficient construction.
shear_fixture = fixtures.fetch("integerShearSample")
shear_degree = Integer(shear_fixture.fetch("degree"))
shear_eta = fraction(shear_fixture.fetch("eta"))
shear_first_mode = Integer(shear_fixture.fetch("firstMode"))
shear_b = fraction(shear_fixture.fetch("backgroundShear"))
shear_polynomial = chebyshev_coefficients(shear_degree)
i_eta = Complex(Rational(0), shear_eta)
w_coefficients = [Complex(Rational(0), Rational(1, 1) / shear_eta), 1 / i_eta]
substitution_coefficients = poly_pad(poly_compose(shear_polynomial, w_coefficients), shear_degree + 1)
derivative_coefficients = (0..shear_degree).map do |j|
  poly_evaluate(poly_derivative(shear_polynomial, j), Complex(Rational(0), Rational(1, 1) / shear_eta)) /
    (factorial(j) * (i_eta**j))
end
real_transformed = substitution_coefficients.map(&:real)
shear_modes = (shear_first_mode..(shear_first_mode + shear_degree)).to_a
shear_amplitudes = real_transformed.map { |value| 2 * value.abs }
shear_phases = real_transformed.map { |value| value.positive? ? Rational(0) : Rational(1) }
pde_mode = Integer(shear_fixture.fetch("pdeCheckMode"))
pde_time_cosine = -(pde_mode**2)
pde_time_sine = pde_mode * shear_b
pde_transport_sine = -shear_b * pde_mode
pde_laplacian_cosine = pde_mode**2

# Exact conjugated operator sample.
operator_fixture = fixtures.fetch("operatorSample")
operator_eta = fraction(operator_fixture.fetch("eta"))
operator_polynomial = operator_fixture.fetch("polynomialCoefficientsAscending").map { |value| fraction(value) }
operator_i_eta = Complex(Rational(0), operator_eta)
one_plus_i_eta_w = [Complex(1, 0), operator_i_eta]
operator_second = poly_derivative(operator_polynomial, 2)
operator_first = poly_derivative(operator_polynomial, 1)
operator_l_eta = poly_add(
  poly_multiply(poly_multiply(one_plus_i_eta_w, one_plus_i_eta_w), operator_second),
  poly_scale(poly_multiply(one_plus_i_eta_w, operator_first), operator_i_eta)
)
operator_l_eta = poly_pad(operator_l_eta, operator_polynomial.length)
operator_second_padded = poly_pad(operator_second, operator_polynomial.length)
operator_difference = poly_pad(poly_add(operator_l_eta, poly_scale(operator_second_padded, -1)), operator_polynomial.length)

# Collar, clock, and plateau geometry.
geometry_fixture = fixtures.fetch("geometryClockSample")
geometry_a = fraction(geometry_fixture.fetch("a"))
geometry_delta0 = fraction(geometry_fixture.fetch("delta0"))
geometry_delta = fraction(geometry_fixture.fetch("outerDelta"))
geometry_r = fraction(geometry_fixture.fetch("rCenter"))
geometry_h = fraction(geometry_fixture.fetch("halfWidth"))
geometry_r_pair = fraction(geometry_fixture.fetch("pairedRadius"))
geometry_r_scale = fraction(geometry_fixture.fetch("R"))
geometry_beta = fraction(geometry_fixture.fetch("beta"))
geometry_terminal_s = fraction(geometry_fixture.fetch("terminalTime"))
geometry_a_edge = geometry_a - geometry_delta0
geometry_e_a = geometry_a_edge / geometry_a
geometry_v = -geometry_beta / geometry_a_edge
geometry_b = -geometry_beta * geometry_a / (geometry_a_edge * geometry_r_scale)
geometry_gamma = geometry_beta * geometry_a / geometry_a_edge
geometry_c_plus = geometry_r_pair + geometry_delta0 + geometry_gamma * geometry_terminal_s
geometry_c_minus = geometry_r_pair + geometry_delta0 - geometry_gamma * geometry_terminal_s
geometry_c_subcap = geometry_r - geometry_h + geometry_delta0
geometry_c_plateau = 2 * geometry_delta0
geometry_c_terminal_cap = geometry_c_subcap + geometry_gamma * geometry_terminal_s
geometry_c_terminal_plateau = geometry_c_plateau + geometry_gamma * geometry_terminal_s
strip_c = geometry_fixture.fetch("plateauStripC").map { |value| fraction(value) }
strip_z = strip_c.map { |c| Rational(1) + (c - geometry_delta0) / geometry_a }
area_over_pi = lambda do |z|
  outer = [(geometry_a + geometry_delta0)**2 - geometry_a**2 * z**2, Rational(0)].max
  inner = [(geometry_a - geometry_delta0)**2 - geometry_a**2 * z**2, Rational(0)].max
  outer - inner
end
strip_area_endpoints = strip_z.map { |z| area_over_pi.call(z) }
# On this outer strip the inner disk has vanished and z=1+(c-delta0)/a.
# Integrate [ (a+delta0)^2-(a+c-delta0)^2 ] dc/a exactly.
c_left, c_right = strip_c
strip_integral_antiderivative = lambda do |c|
  constant = (geometry_a + geometry_delta0)**2 - (geometry_a - geometry_delta0)**2
  (constant * c - (geometry_a - geometry_delta0) * c**2 - c**3 / 3) / geometry_a
end
integrated_strip_area = strip_integral_antiderivative.call(c_right) - strip_integral_antiderivative.call(c_left)
velocity_sign = geometry_v <=> 0
positive_weight_sign = -1
paired_square_difference_sign = geometry_c_plus > geometry_c_minus ? 1 : -1
paired_flux_sign = velocity_sign * positive_weight_sign * paired_square_difference_sign

# Physical and normalized monomial ledger.
normalization_fixture = fixtures.fetch("normalizationSample")
flux_coefficient = fraction(normalization_fixture.fetch("physicalFluxCoefficient"))
flux_a_exponent = fraction(normalization_fixture.fetch("physicalFluxAExponent"))
flux_r_exponent = fraction(normalization_fixture.fetch("physicalFluxRExponent"))
mass_a_exponent = fraction(normalization_fixture.fetch("plateauMassAExponent"))
mass_r_exponent = fraction(normalization_fixture.fetch("plateauMassRExponent"))
quotient_a_exponent = flux_a_exponent - Rational(2, 3) * mass_a_exponent
quotient_r_exponent = flux_r_exponent - Rational(2, 3) * mass_r_exponent
r_weighted_exponent = quotient_r_exponent + Rational(1, 3)
normalized_p_r = Rational(-2)
normalized_p_omega = Rational(1)
normalized_x_r = Rational(-1)
normalized_x_omega = Rational(1)
normalized_q_r = normalized_x_r - Rational(2, 3) * normalized_p_r
normalized_q_omega = normalized_x_omega - Rational(2, 3) * normalized_p_omega
omega_log_rate = fraction(normalization_fixture.fetch("omegaLogRate"))
r_log_rate = fraction(normalization_fixture.fetch("rLogRate"))
omega_third_rate = (quotient_r_exponent + normalized_q_r) * r_log_rate + normalized_q_omega * omega_log_rate
a_over_l = fraction(normalization_fixture.fetch("aOverL"))
a_squared_density = a_over_l**2
penalty_coefficient = -normalized_q_omega * omega_log_rate / a_squared_density
penalty_log_rate = -a_squared_density * penalty_coefficient
formal_kappa = fraction(normalization_fixture.fetch("formalKappa"))
formal_s = fraction(saddle_fixture.fetch("heatTime"))
formal_gap = saddle_gap
formal_integration_saddle = exact_root(2 * formal_s * formal_kappa, 2)
formal_displacement = formal_integration_saddle
formal_tilt = exact_root(formal_kappa / (2 * formal_s), 2)
formal_squared_ratio = 2 * formal_gap * formal_tilt
formal_critical_kappa = formal_s * penalty_coefficient**2 / (2 * formal_gap**2)

# Backward-heat sign sample.
backward_fixture = fixtures.fetch("backwardHeatSample")
backward_n = Integer(backward_fixture.fetch("n"))
backward_degree = Integer(backward_fixture.fetch("m"))
backward_a = fraction(backward_fixture.fetch("A"))
backward_time = fraction(backward_fixture.fetch("time"))
backward_t = backward_time / backward_a**2
backward_chebyshev = chebyshev_coefficients(backward_degree)
backward_polynomial = heat_polynomial(backward_chebyshev, backward_t, -1)
wrong_forward_polynomial = heat_polynomial(backward_chebyshev, backward_t, 1)
backward_terms = (0..backward_n).map do |j|
  Rational(backward_n * factorial(backward_n + j - 1), factorial(backward_n - j)) *
    ((4 * backward_t)**j) / factorial(j)
end
backward_absolute = poly_evaluate(backward_polynomial, Rational(0)).abs
forward_absolute = poly_evaluate(wrong_forward_polynomial, Rational(0)).abs
imaginary_y = fraction(backward_fixture.fetch("imaginaryAxisY"))
imaginary_even_coefficients = backward_polynomial.each_slice(2).map(&:first).map(&:abs)
imaginary_terms = imaginary_even_coefficients.each_with_index.map do |coefficient, j|
  coefficient * imaginary_y**(2 * j)
end
imaginary_value = imaginary_terms.sum

# Archived diagnostic and figure ledger.
diagnostic_fixture = fixtures.fetch("diagnostic")
config = JSON.parse(raw_by_name.fetch("figureConfig", "{}"))
data_rows = CSV.parse(raw_by_name.fetch("figureData", ""), headers: true)
data_columns = data_rows.headers || []
progress_rows = raw_by_name.fetch("figureProgress", "").lines.reject { |line| line.strip.empty? }.map do |line|
  JSON.parse(line)
end
resource_rows = CSV.parse(raw_by_name.fetch("figureResources", ""), headers: true)
png = png_metadata(File.join(ROOT, files.fetch("figurePng")))
pdf_raw = raw_by_name.fetch("figurePdf", "")
svg_text = text_by_name.fetch("figureSvg", "")
diagnostic_a_values = data_rows.map { |row| Integer(row.fetch("A")) }.uniq
diagnostic_power_values = data_rows.map { |row| fraction_string(fraction(row.fetch("degreePower"))) }.uniq
diagnostic_max = lambda do |column|
  data_rows.map { |row| row.fetch(column).to_f.abs }.max || Float::NAN
end
saddle_limit_decimal = format("%.12f", 2.0**(5.0 / 3.0))
amplitude_limit_decimal = format("%.12f", 3.0 * 2.0**(-2.0 / 3.0))
tilt_limit_decimal = format("%.12f", 2.0**(-4.0 / 3.0))
away_rows = data_rows.select { |row| fraction(row.fetch("degreePower")) == Rational(3, 4) }
  .sort_by { |row| Integer(row.fetch("A")) }
away_errors = away_rows.map { |row| (row.fetch("unitTiltOverMu").to_f - tilt_limit_decimal.to_f).abs }

scale_exact = {
  "mSquaredOverA" => fraction_string(scale_m2_over_a),
  "muCubed" => fraction_string(scale_mu_cube),
  "mu" => fraction_string(scale_mu),
  "sqrtA" => fraction_string(scale_sqrt_a),
  "gamma" => fraction_string(scale_gamma),
  "gammaSquared" => fraction_string(scale_gamma**2),
  "terminalLayerWidth" => fraction_string(scale_h),
  "clockResidualScale" => fraction_string(scale_mu),
  "fixedSliceScale" => fraction_string(scale_gamma),
  "commonHeatScale" => fraction_string(scale_mu**2),
  "strictScaleOrdering" => scale_mu < scale_gamma && scale_gamma < scale_mu**2,
  "powerLawRows" => power_rows
}

saddle_exact = {
  "basisOrder" => ["1", "alpha", "alpha^2"],
  "generatorCube" => "2",
  "z4" => z4.to_a,
  "squareRootTwoZ4" => sqrt_two_z4.to_a,
  "F4" => f4.to_a,
  "G4" => g4.to_a,
  "twoG4" => two_g4.to_a,
  "z4Cube" => fraction_string((z4**3).coefficients.fetch(0)),
  "F4Cube" => fraction_string((f4**3).coefficients.fetch(0)),
  "F3Cube" => fraction_string(Rational(81, 16)),
  "F4CubeMinusF3Cube" => fraction_string((f4**3).coefficients.fetch(0) - Rational(81, 16)),
  "G4Cube" => fraction_string((g4**3).coefficients.fetch(0)),
  "z4OverEight" => (z4 / 8).to_a,
  "squareRootTwoZ4Squared" => (sqrt_two_z4**2).to_a,
  "twoZ4" => (2 * z4).to_a,
  "F4FromRateFunction" => (sqrt_two_z4 - (z4 * z4) / 16).to_a,
  "terminalDominatesTimeThree" => (f4**3).coefficients.fetch(0) > Rational(81, 16),
  "capPlateauGap" => fraction_string(saddle_gap),
  "squaredRatioSlopeForGap" => squared_ratio_slope.to_a,
  "squaredRatioSlopeForGapCube" => fraction_string((squared_ratio_slope**3).coefficients.fetch(0))
}

tilt_exact = {
  "deltaC" => fraction_string(tilt_delta_c),
  "baseCenteredY" => fraction_string(tilt_centered_y),
  "linearTilt" => fraction_string(tilt_linear),
  "constantPenalty" => fraction_string(tilt_penalty),
  "logKernelRatioByTilt" => fraction_string(tilt_ratio),
  "logKernelRatioBySquareDifference" => fraction_string(tilt_ratio_square),
  "tiltSignPositive" => tilt_ratio.positive?
}

heat_exact = {
  "chebyshevCoefficientsAscending" => heat_chebyshev.map { |value| fraction_string(value) },
  "endpointDerivativesDirect" => endpoint_direct.map { |value| fraction_string(value) },
  "endpointDerivativesFormula" => endpoint_formula.map { |value| fraction_string(value) },
  "successiveDerivativeRatios" => derivative_ratios.map { |value| fraction_string(value) },
  "allEndpointDerivativesPositive" => endpoint_formula.all?(&:positive?),
  "forwardHeatCoefficientsAscending" => forward_heat.map { |value| fraction_string(value) },
  "backwardHeatCoefficientsAscending" => backward_heat.map { |value| fraction_string(value) },
  "evaluationPoint" => fraction_string(heat_x),
  "forwardHeatValue" => fraction_string(forward_heat_value),
  "backwardHeatValue" => fraction_string(backward_heat_value),
  "positiveWeights" => positive_weights,
  "weightSum" => fraction_string(weight_sum),
  "meanJ" => fraction_string(mean_j),
  "meanEll" => fraction_string(mean_ell),
  "meanEllEllMinusOne" => fraction_string(mean_ell_pair),
  "cSquaredMeanJOverTime" => fraction_string(heat_c**2 * mean_j / heat_s),
  "ellZeroSuccessiveJRatios" => ell_zero_ratios.map { |value| fraction_string(value) },
  "positiveSeriesIncreasingInTimeAndPositiveC" => positive_weights.all? { |row| fraction(row["value"]).positive? },
  "forwardBackwardDistinct" => forward_heat != backward_heat
}

integer_shear_exact = {
  "wEtaCoefficientsAscending" => w_coefficients.map { |value| complex_pair(value) },
  "transformedCoefficientsBySubstitution" => real_transformed.map { |value| fraction_string(value) },
  "transformedCoefficientsByDerivativeFormula" => derivative_coefficients.map { |value| fraction_string(value.real) },
  "allTransformedCoefficientsNonzero" => substitution_coefficients.none?(&:zero?),
  "carrier" => fraction_string(shear_first_mode * shear_eta),
  "modes" => shear_modes,
  "amplitudes" => shear_amplitudes.map { |value| fraction_string(value) },
  "phasesOverPi" => shear_phases.map { |value| fraction_string(value) },
  "strictlyIncreasingModes" => shear_modes.each_cons(2).all? { |left, right| right == left + 1 },
  "closedDyadicBand" => shear_modes.first == shear_first_mode && shear_modes.last == 2 * shear_first_mode,
  "pdeMode" => pde_mode,
  "pdeTimeDerivativeCosineCoefficient" => fraction_string(pde_time_cosine),
  "pdeTimeDerivativeSineCoefficient" => fraction_string(pde_time_sine),
  "pdeTransportSineCoefficient" => fraction_string(pde_transport_sine),
  "pdeNegativeLaplacianCosineCoefficient" => fraction_string(pde_laplacian_cosine),
  "pdeCosineResidual" => fraction_string(pde_time_cosine + pde_laplacian_cosine),
  "pdeSineResidual" => fraction_string(pde_time_sine + pde_transport_sine)
}

operator_exact = {
  "lEtaCoefficientsAscending" => operator_l_eta.map { |value| complex_pair(value) },
  "secondDerivativeCoefficientsAscending" => operator_second_padded.map { |value| complex_pair(Complex(value, 0)) },
  "differenceCoefficientsAscending" => operator_difference.map { |value| complex_pair(value) },
  "firstOrderImaginarySignPositive" => operator_difference.fetch(1).imag.positive?,
  "degreePreserved" => operator_l_eta.length <= operator_polynomial.length
}

geometry_exact = {
  "A" => fraction_string(geometry_a_edge),
  "eA" => fraction_string(geometry_e_a),
  "scaledVelocity" => fraction_string(geometry_v),
  "backgroundShear" => fraction_string(geometry_b),
  "gamma" => fraction_string(geometry_gamma),
  "rCenterMinusThreeHalfWidths" => fraction_string(geometry_r - 3 * geometry_h),
  "rCenterPlusThreeHalfWidths" => fraction_string(geometry_r + 3 * geometry_h),
  "strictSubcapGeometry" => geometry_delta0 < geometry_r - 3 * geometry_h &&
    geometry_r + 3 * geometry_h < geometry_delta,
  "positiveEdgeCoordinate" => fraction_string(geometry_c_plus),
  "negativeEdgeCoordinate" => fraction_string(geometry_c_minus),
  "pairedCoordinateGap" => fraction_string(geometry_c_plus - geometry_c_minus),
  "subcapCoordinate" => fraction_string(geometry_c_subcap),
  "plateauCoordinate" => fraction_string(geometry_c_plateau),
  "capPlateauGap" => fraction_string(geometry_c_subcap - geometry_c_plateau),
  "terminalCapCoordinate" => fraction_string(geometry_c_terminal_cap),
  "terminalPlateauCoordinate" => fraction_string(geometry_c_terminal_plateau),
  "terminalCoordinateGap" => fraction_string(geometry_c_terminal_cap - geometry_c_terminal_plateau),
  "plateauStripZ" => strip_z.map { |value| fraction_string(value) },
  "plateauStripZWidth" => fraction_string(strip_z.fetch(1) - strip_z.fetch(0)),
  "areaOverPiAtStripEndpoints" => strip_area_endpoints.map { |value| fraction_string(value) },
  "integratedStripAreaOverPi" => fraction_string(integrated_strip_area),
  "velocitySign" => velocity_sign,
  "positiveWeightSign" => positive_weight_sign,
  "pairedSquareDifferenceSign" => paired_square_difference_sign,
  "pairedFluxSign" => paired_flux_sign
}

normalization_exact = {
  "physicalFlux" => {
    "coefficient" => fraction_string(flux_coefficient),
    "aExponent" => fraction_string(flux_a_exponent),
    "rExponent" => fraction_string(flux_r_exponent)
  },
  "plateauMass" => {
    "coefficient" => "1",
    "aExponent" => fraction_string(mass_a_exponent),
    "rExponent" => fraction_string(mass_r_exponent)
  },
  "unweightedQuotient" => {
    "coefficient" => fraction_string(flux_coefficient),
    "aExponent" => fraction_string(quotient_a_exponent),
    "rExponent" => fraction_string(quotient_r_exponent)
  },
  "rWeightedQuotient" => {
    "coefficient" => fraction_string(flux_coefficient),
    "aExponent" => fraction_string(quotient_a_exponent),
    "rExponent" => fraction_string(r_weighted_exponent)
  },
  "lowerBoundAExponent" => fraction_string(quotient_a_exponent - Rational(2, 3)),
  "lowerBoundTerminalLayerExponent" => "1",
  "upperBoundAExponent" => fraction_string(quotient_a_exponent),
  "upperBoundTerminalLayerExponent" => fraction_string(Rational(-2, 3)),
  "normalizedPlateau" => {"rExponent" => fraction_string(normalized_p_r), "omegaExponent" => "1"},
  "normalizedFlux" => {"rExponent" => fraction_string(normalized_x_r), "omegaExponent" => "1"},
  "normalizedQuotientFactor" => {
    "rExponent" => fraction_string(normalized_q_r),
    "omegaExponent" => fraction_string(normalized_q_omega)
  },
  "omegaThirdLogRate" => fraction_string(omega_third_rate),
  "aSquaredLeadingDensity" => fraction_string(a_squared_density),
  "aSquaredPenaltyCoefficient" => fraction_string(penalty_coefficient),
  "aSquaredPenaltyLogRate" => fraction_string(penalty_log_rate),
  "formalHighDegree" => {
    "status" => "OPEN_DIRECTION",
    "kappa" => fraction_string(formal_kappa),
    "heatTime" => fraction_string(formal_s),
    "capPlateauGap" => fraction_string(formal_gap),
    "integrationSaddleCoefficient" => fraction_string(formal_integration_saddle),
    "physicalDisplacementCoefficient" => fraction_string(formal_displacement),
    "tiltCoefficient" => fraction_string(formal_tilt),
    "squaredRatioExponentCoefficient" => fraction_string(formal_squared_ratio),
    "criticalKappa" => fraction_string(formal_critical_kappa),
    "sampleExceedsFormalThreshold" => formal_kappa > formal_critical_kappa
  }
}

backward_exact = {
  "terms" => backward_terms.map { |value| fraction_string(value) },
  "exactAbsoluteValue" => fraction_string(backward_absolute),
  "wrongForwardSignAbsoluteValue" => fraction_string(forward_absolute),
  "backwardPolynomialCoefficientsAscending" => backward_polynomial.map { |value| fraction_string(value) },
  "wrongForwardPolynomialCoefficientsAscending" => wrong_forward_polynomial.map { |value| fraction_string(value) },
  "imaginaryAxisPositiveEvenCoefficients" => imaginary_even_coefficients.map { |value| fraction_string(value) },
  "imaginaryAxisTerms" => imaginary_terms.map { |value| fraction_string(value) },
  "imaginaryAxisValue" => fraction_string(imaginary_value),
  "forwardBackwardDistinct" => backward_polynomial != wrong_forward_polynomial
}

diagnostic_exact = {
  "rowCount" => data_rows.length,
  "columnCount" => data_columns.length,
  "columns" => data_columns,
  "AValues" => diagnostic_a_values,
  "degreePowers" => diagnostic_power_values,
  "theoreticalLimitDecimals" => {
    "saddle" => saddle_limit_decimal,
    "amplitude" => amplitude_limit_decimal,
    "tilt" => tilt_limit_decimal
  },
  "maximumSaddleDerivativeResidual" => format("%.12e", diagnostic_max.call("saddleDerivativeResidual")),
  "maximumCoarseFineAmplitudeDelta" => format("%.12e", diagnostic_max.call("coarseFineAmplitudeDelta")),
  "maximumCoarseFineTiltDelta" => format("%.12e", diagnostic_max.call("coarseFineTiltDelta")),
  "maximumPhaseDropAmplitudeDelta" => format("%.12e", diagnostic_max.call("phaseDropAmplitudeDelta")),
  "maximumPhaseDropTiltDelta" => format("%.12e", diagnostic_max.call("phaseDropTiltDelta")),
  "progressEventCount" => progress_rows.length,
  "resourceSampleCount" => resource_rows.length,
  "progressStages" => progress_rows.map { |row| row["stage"] }.uniq,
  "pngPixels" => [png["width"], png["height"]],
  "pngDpi" => png["dpi"],
  "pdfPages" => pdf_raw.scan(/\/Type\s*\/Page\b/).length,
  "pdfEncrypted" => pdf_raw.include?("/Encrypt"),
  "pdfHasJavaScript" => pdf_raw.match?(/\/JavaScript|\/JS\b/),
  "svgWidth" => svg_text[/\bwidth="([^"]+)"/, 1],
  "svgHeight" => svg_text[/\bheight="([^"]+)"/, 1],
  "panelCount" => %w[(a) (b) (c)].count { |label| svg_text.include?(">#{label}<") },
  "monotonicityRequired" => diagnostic_fixture.fetch("monotonicityRequired"),
  "knownPreasymptoticAwaySequence" => diagnostic_fixture.fetch("knownPreasymptoticAwaySequence"),
  "finiteDiagnosticOnly" => true
}

exact = {
  "structure" => {
    "firstTag" => tags.first,
    "lastTag" => tags.last,
    "tagCount" => tags.length,
    "displayCount" => display_opens,
    "tagSequenceComplete" => tags == (1..72).to_a,
    "referencesClosed" => (references.uniq - tags.uniq).empty?
  },
  "scaleSample" => scale_exact,
  "saddleSample" => saddle_exact,
  "tiltSample" => tilt_exact,
  "heatSeriesSample" => heat_exact,
  "integerShearSample" => integer_shear_exact,
  "operatorSample" => operator_exact,
  "geometryClockSample" => geometry_exact,
  "normalizationSample" => normalization_exact,
  "backwardHeatSample" => backward_exact,
  "diagnostic" => diagnostic_exact,
  "claims" => fixtures.fetch("claims")
}

checks = GROUPS.each_with_object({}) do |(group, names), output|
  output[group] = names.each_with_object({}) { |name, rows| rows[name] = false }
end

file_values = files.values
checks["bindings"]["hash_inventory"] = frozen_hashes.keys.sort == file_values.sort
checks["bindings"]["hash_specs_well_formed"] = frozen_hashes.values.all? do |value|
  value.is_a?(String) && SHA256_PATTERN.match?(value)
end
checks["bindings"]["fixture_self_hash"] = sha256("scripts/#{STEM}_fixtures.json") == FIXTURE_SHA256
checks["bindings"]["expected_self_hash"] = sha256("scripts/#{STEM}_expected.json") == EXPECTED_SHA256
checks["bindings"]["all_frozen_hashes"] = bindings.values.all? { |row| row["pass"] }
checks["bindings"]["source_commit_ready"] = source_tree_ready
checks["bindings"]["upstream_commit_exact"] = frozen["upstreamCoreCommit"] == UPSTREAM_CORE_COMMIT
checks["bindings"]["upstream_commit_stated"] = primary_text.include?(UPSTREAM_CORE_COMMIT)
upstream_names = %w[r076kMain r076kSource r076kPrimaryAudit r076kCertificate r076kQaReport]
checks["bindings"]["upstream_hashes_stated"] = upstream_names.all? do |name|
  primary_text.include?(frozen_hashes.fetch(files.fetch(name), "MISSING"))
end
checks["bindings"]["core_objects_bound"] = %w[main source primaryAudit].all? do |name|
  row = bindings[files[name]]
  row.is_a?(Hash) && row["pass"]
end
figure_names = files.keys.select { |name| name.start_with?("figure") }
checks["bindings"]["figure_objects_bound"] = figure_names.include?("figureQaReport") && figure_names.all? do |name|
  row = bindings[files[name]]
  row.is_a?(Hash) && row["pass"]
end
checks["bindings"]["generated_outputs_unbound"] = frozen_hashes.keys.none? do |path|
  path.end_with?("_certificate.json", "_certificate_report.md", "_independent_audit.md", "_qa_report.md") &&
    !path.include?("r076k_") || File.basename(path) == "AGENTS.md"
end

checks["inputs"]["fixture_schema"] = fixtures["schema"] == FIXTURE_SCHEMA
checks["inputs"]["expected_schema"] = expected["schema"] == EXPECTED_SCHEMA
checks["inputs"]["fixture_object"] = fixtures.is_a?(Hash)
checks["inputs"]["expected_object"] = expected.is_a?(Hash)
checks["inputs"]["fixture_keys"] = fixtures.keys.sort == %w[
  backwardHeatSample claims diagnostic files frozen geometryClockSample heatSeriesSample
  integerShearSample normalizationSample operatorSample saddleSample scaleSample schema
  structure tiltSample
].sort
checks["inputs"]["expected_keys"] = expected.keys.sort == %w[
  backwardHeatSample claims diagnostic geometryClockSample heatSeriesSample
  integerShearSample normalizationSample operatorSample saddleSample scaleSample schema
  structure tiltSample
].sort
checks["inputs"]["file_inventory"] = files.length == frozen_hashes.length &&
  files.values.uniq.length == files.length && files.values.sort == frozen_hashes.keys.sort
checks["inputs"]["structure_inventory"] = fixtures["structure"].keys.sort == %w[
  displayCount equationPrefix firstTag lastTag tagCount
].sort
checks["inputs"]["scale_inventory"] = scale_fixture.keys.sort == %w[A alphaValues m].sort
checks["inputs"]["saddle_inventory"] = saddle_fixture.keys.sort == %w[
  capPlateauGap cubicGenerator generatorCube generatorIsolatingInterval heatTime
].sort
checks["inputs"]["tilt_inventory"] = tilt_fixture.keys.sort == %w[c1 c2 heatTime y].sort
checks["inputs"]["heat_series_inventory"] = heat_fixture.keys.sort == %w[A degree edgeCoordinate time].sort
checks["inputs"]["integer_shear_inventory"] = shear_fixture.keys.sort == %w[
  backgroundShear degree eta firstMode pdeCheckMode
].sort
checks["inputs"]["operator_inventory"] = operator_fixture.keys.sort == %w[
  eta polynomialCoefficientsAscending
].sort
checks["inputs"]["geometry_inventory"] = geometry_fixture.keys.sort == %w[
  R a beta delta0 halfWidth outerDelta pairedRadius plateauStripC rCenter terminalTime
].sort
checks["inputs"]["normalization_inventory"] = normalization_fixture.keys.sort == %w[
  aOverL formalKappa omegaLogRate physicalFluxAExponent physicalFluxCoefficient
  physicalFluxRExponent plateauMassAExponent plateauMassRExponent rLogRate
].sort
checks["inputs"]["backward_inventory"] = backward_fixture.keys.sort == %w[A imaginaryAxisY m n time].sort
checks["inputs"]["diagnostic_inventory"] = diagnostic_fixture.keys.sort == %w[
  AValues coarseFineTolerance coarseGridPoints columnCount degreePolicy degreePowers
  edgeCoordinates figureHeightMillimetres figureWidthMillimetres fineGridPoints heatTime
  knownPreasymptoticAwaySequence limitDecimalTolerance monotonicityRequired muIdentityRelativeTolerance
  pdfPages phaseDrop phaseDropTolerance pngDpi pngPixels progressEventCount resourceSampleCount
  rowCount saddleResidualTolerance schema
].sort
checks["inputs"]["claims_inventory"] = fixtures.fetch("claims").keys.sort == expected.fetch("claims").keys.sort

checks["integrity"]["main_utf8"] = clean_bytes(raw_by_name.fetch("main"))
checks["integrity"]["source_utf8"] = clean_bytes(raw_by_name.fetch("source"))
checks["integrity"]["primary_utf8"] = clean_bytes(raw_by_name.fetch("primaryAudit"))
checks["integrity"]["fixture_utf8"] = clean_bytes(File.binread(FIXTURE_PATH))
checks["integrity"]["expected_utf8"] = clean_bytes(File.binread(EXPECTED_PATH))
text_inputs = raw_by_name.reject { |name, _raw| %w[figurePng figurePdf].include?(name) }.values
checks["integrity"]["no_controls"] = text_inputs.all? { |raw| clean_bytes(raw) }
checks["integrity"]["no_cr"] = text_inputs.none? { |raw| raw.include?("\r") }
checks["integrity"]["no_trailing"] = [main_text, source_text, primary_text].all? do |body|
  body.lines.none? { |line| line.chomp.end_with?(" ", "\t") }
end
checks["integrity"]["tag_sequence"] = tags == (1..fixtures.dig("structure", "lastTag")).to_a
checks["integrity"]["tag_unique"] = tags.uniq.length == tags.length
checks["integrity"]["tag_count"] = tags.length == fixtures.dig("structure", "tagCount")
checks["integrity"]["display_balance"] = display_opens == display_closes
checks["integrity"]["display_count"] = display_opens == fixtures.dig("structure", "displayCount")
checks["integrity"]["reference_closure"] = (references.uniq - tags.uniq).empty?

scale_expected = expected.fetch("scaleSample")
checks["scale"]["scale_sample_domain"] = scale_a.positive? && scale_m.even? && scale_m > Math.sqrt(scale_a)
checks["scale"]["m_squared_over_a"] = scale_m2_over_a == 64 && scale_exact["mSquaredOverA"] == scale_expected["mSquaredOverA"]
checks["scale"]["mu_cube"] = scale_mu**3 == scale_mu_cube && scale_exact["muCubed"] == scale_expected["muCubed"]
checks["scale"]["mu_value"] = scale_exact["mu"] == scale_expected["mu"]
checks["scale"]["sqrt_a"] = scale_sqrt_a**2 == scale_a && scale_exact["sqrtA"] == scale_expected["sqrtA"]
checks["scale"]["gamma_value"] = scale_gamma == scale_m / scale_sqrt_a && scale_exact["gamma"] == scale_expected["gamma"]
checks["scale"]["gamma_square"] = scale_gamma**2 == 64 && scale_exact["gammaSquared"] == scale_expected["gammaSquared"]
checks["scale"]["terminal_layer"] = scale_h == Rational(1, 17) && scale_exact["terminalLayerWidth"] == scale_expected["terminalLayerWidth"]
checks["scale"]["clock_residual"] = scale_exact["clockResidualScale"] == scale_expected["clockResidualScale"]
checks["scale"]["fixed_slice"] = scale_exact["fixedSliceScale"] == scale_expected["fixedSliceScale"]
checks["scale"]["common_heat"] = scale_exact["commonHeatScale"] == scale_expected["commonHeatScale"]
checks["scale"]["strict_order"] = scale_exact["strictScaleOrdering"] && scale_expected["strictScaleOrdering"]
checks["scale"]["power_rows"] = power_rows == scale_expected["powerLawRows"]
checks["scale"]["power_gamma"] = power_rows.all? { |row| fraction(row["gammaExponent"]) == fraction(row["alpha"]) - Rational(1, 2) }
checks["scale"]["power_mu"] = power_rows.all? { |row| fraction(row["muExponent"]) == (2 * fraction(row["alpha"]) - 1) / 3 }
checks["scale"]["power_mu_squared"] = power_rows.all? { |row| fraction(row["muSquaredExponent"]) == 2 * fraction(row["muExponent"]) }
checks["scale"]["power_backward"] = power_rows.all? { |row| fraction(row["backwardExponent"]) == 2 * fraction(row["alpha"]) - 2 }

saddle_expected = expected.fetch("saddleSample")
checks["cubic_saddle"]["generator_cube"] = alpha**3 == 2 && saddle_fixture["generatorCube"] == "2" &&
  saddle_fixture["cubicGenerator"] == "alpha" && fraction(saddle_fixture["heatTime"]) == 4
checks["cubic_saddle"]["isolating_interval"] = generator_left**3 < 2 && 2 < generator_right**3
checks["cubic_saddle"]["basis_order"] = saddle_exact["basisOrder"] == saddle_expected["basisOrder"]
checks["cubic_saddle"]["z4"] = z4 == alpha**5 && saddle_exact["z4"] == saddle_expected["z4"]
checks["cubic_saddle"]["sqrt_two_z4"] = sqrt_two_z4**2 == 2 * z4 && saddle_exact["squareRootTwoZ4"] == saddle_expected["squareRootTwoZ4"]
checks["cubic_saddle"]["f4"] = f4 == sqrt_two_z4 - z4**2 / 16 && saddle_exact["F4"] == saddle_expected["F4"]
checks["cubic_saddle"]["g4"] = g4 == z4 / 8 && saddle_exact["G4"] == saddle_expected["G4"]
checks["cubic_saddle"]["two_g4"] = two_g4 == 2 * g4 && saddle_exact["twoG4"] == saddle_expected["twoG4"]
checks["cubic_saddle"]["z4_cube"] = saddle_exact["z4Cube"] == saddle_expected["z4Cube"]
checks["cubic_saddle"]["f4_cube"] = saddle_exact["F4Cube"] == saddle_expected["F4Cube"]
checks["cubic_saddle"]["f3_cube"] = saddle_exact["F3Cube"] == saddle_expected["F3Cube"]
checks["cubic_saddle"]["f4_minus_f3"] = saddle_exact["F4CubeMinusF3Cube"] == saddle_expected["F4CubeMinusF3Cube"]
checks["cubic_saddle"]["g4_cube"] = saddle_exact["G4Cube"] == saddle_expected["G4Cube"]
checks["cubic_saddle"]["z4_over_eight"] = saddle_exact["z4OverEight"] == saddle_expected["z4OverEight"]
checks["cubic_saddle"]["sqrt_square"] = saddle_exact["squareRootTwoZ4Squared"] == saddle_expected["squareRootTwoZ4Squared"]
checks["cubic_saddle"]["two_z4"] = saddle_exact["twoZ4"] == saddle_expected["twoZ4"]
checks["cubic_saddle"]["rate_function"] = saddle_exact["F4FromRateFunction"] == saddle_expected["F4FromRateFunction"]
checks["cubic_saddle"]["terminal_dominance"] = saddle_exact["terminalDominatesTimeThree"] && saddle_expected["terminalDominatesTimeThree"]
checks["cubic_saddle"]["gap_value"] = saddle_exact["capPlateauGap"] == saddle_expected["capPlateauGap"]
checks["cubic_saddle"]["ratio_slope"] = saddle_exact["squaredRatioSlopeForGap"] == saddle_expected["squaredRatioSlopeForGap"]
checks["cubic_saddle"]["ratio_slope_cube"] = saddle_exact["squaredRatioSlopeForGapCube"] == saddle_expected["squaredRatioSlopeForGapCube"]

tilt_expected = expected.fetch("tiltSample")
checks["tilt"]["tilt_sample_domain"] = tilt_s.positive? && tilt_y > tilt_c2 && tilt_c2 > tilt_c1
checks["tilt"]["delta_c"] = tilt_exact["deltaC"] == tilt_expected["deltaC"]
checks["tilt"]["centered_y"] = tilt_exact["baseCenteredY"] == tilt_expected["baseCenteredY"]
checks["tilt"]["linear_tilt"] = tilt_exact["linearTilt"] == tilt_expected["linearTilt"]
checks["tilt"]["constant_penalty"] = tilt_exact["constantPenalty"] == tilt_expected["constantPenalty"]
checks["tilt"]["kernel_ratio_tilt"] = tilt_exact["logKernelRatioByTilt"] == tilt_expected["logKernelRatioByTilt"]
checks["tilt"]["kernel_ratio_squares"] = tilt_exact["logKernelRatioBySquareDifference"] == tilt_expected["logKernelRatioBySquareDifference"]
checks["tilt"]["identities_agree"] = tilt_ratio == tilt_ratio_square
checks["tilt"]["positive_sign"] = tilt_exact["tiltSignPositive"] && tilt_expected["tiltSignPositive"]

heat_expected = expected.fetch("heatSeriesSample")
checks["heat_series"]["chebyshev_recurrence"] = heat_chebyshev == [1, 0, -8, 0, 8]
checks["heat_series"]["coefficients"] = heat_exact["chebyshevCoefficientsAscending"] == heat_expected["chebyshevCoefficientsAscending"]
checks["heat_series"]["endpoint_direct"] = heat_exact["endpointDerivativesDirect"] == heat_expected["endpointDerivativesDirect"]
checks["heat_series"]["endpoint_formula"] = endpoint_direct == endpoint_formula && heat_exact["endpointDerivativesFormula"] == heat_expected["endpointDerivativesFormula"]
checks["heat_series"]["derivative_ratios"] = heat_exact["successiveDerivativeRatios"] == heat_expected["successiveDerivativeRatios"]
checks["heat_series"]["derivatives_positive"] = endpoint_formula.all?(&:positive?) && heat_expected["allEndpointDerivativesPositive"]
checks["heat_series"]["forward_coefficients"] = heat_exact["forwardHeatCoefficientsAscending"] == heat_expected["forwardHeatCoefficientsAscending"]
checks["heat_series"]["backward_coefficients"] = heat_exact["backwardHeatCoefficientsAscending"] == heat_expected["backwardHeatCoefficientsAscending"]
checks["heat_series"]["evaluation_point"] = heat_exact["evaluationPoint"] == heat_expected["evaluationPoint"]
checks["heat_series"]["forward_value"] = heat_exact["forwardHeatValue"] == heat_expected["forwardHeatValue"]
checks["heat_series"]["backward_value"] = heat_exact["backwardHeatValue"] == heat_expected["backwardHeatValue"]
checks["heat_series"]["positive_weights"] = positive_weights == heat_expected["positiveWeights"]
checks["heat_series"]["weight_sum"] = heat_exact["weightSum"] == heat_expected["weightSum"] && weight_sum == forward_heat_value
checks["heat_series"]["mean_j"] = heat_exact["meanJ"] == heat_expected["meanJ"]
checks["heat_series"]["mean_ell"] = heat_exact["meanEll"] == heat_expected["meanEll"]
checks["heat_series"]["mean_ell_pair"] = heat_exact["meanEllEllMinusOne"] == heat_expected["meanEllEllMinusOne"]
checks["heat_series"]["pde_identity"] = mean_ell_pair == heat_c**2 * mean_j / heat_s && heat_exact["cSquaredMeanJOverTime"] == heat_expected["cSquaredMeanJOverTime"]
checks["heat_series"]["j_ratios"] = heat_exact["ellZeroSuccessiveJRatios"] == heat_expected["ellZeroSuccessiveJRatios"]
checks["heat_series"]["increasing_forward_backward"] = heat_exact["positiveSeriesIncreasingInTimeAndPositiveC"] && heat_exact["forwardBackwardDistinct"] && heat_expected["forwardBackwardDistinct"]

shear_expected = expected.fetch("integerShearSample")
checks["integer_shear"]["shear_sample_domain"] = shear_degree.even? && shear_eta.positive? && shear_first_mode == shear_degree
checks["integer_shear"]["w_coefficients"] = integer_shear_exact["wEtaCoefficientsAscending"] == shear_expected["wEtaCoefficientsAscending"]
checks["integer_shear"]["substitution_coefficients"] = integer_shear_exact["transformedCoefficientsBySubstitution"] == shear_expected["transformedCoefficientsBySubstitution"]
checks["integer_shear"]["derivative_coefficients"] = integer_shear_exact["transformedCoefficientsByDerivativeFormula"] == shear_expected["transformedCoefficientsByDerivativeFormula"]
checks["integer_shear"]["coefficient_formulas_agree"] = substitution_coefficients == derivative_coefficients &&
  substitution_coefficients.all? { |coefficient| coefficient.imaginary.zero? }
checks["integer_shear"]["coefficients_nonzero"] = substitution_coefficients.none?(&:zero?) && shear_expected["allTransformedCoefficientsNonzero"]
checks["integer_shear"]["carrier"] = integer_shear_exact["carrier"] == shear_expected["carrier"]
checks["integer_shear"]["modes"] = shear_modes == shear_expected["modes"]
checks["integer_shear"]["amplitudes"] = integer_shear_exact["amplitudes"] == shear_expected["amplitudes"]
checks["integer_shear"]["phases"] = integer_shear_exact["phasesOverPi"] == shear_expected["phasesOverPi"]
checks["integer_shear"]["strict_modes"] = integer_shear_exact["strictlyIncreasingModes"] && shear_expected["strictlyIncreasingModes"]
checks["integer_shear"]["dyadic_band"] = integer_shear_exact["closedDyadicBand"] && shear_expected["closedDyadicBand"]
checks["integer_shear"]["pde_mode"] = pde_mode == shear_expected["pdeMode"]
checks["integer_shear"]["pde_time_cosine"] = integer_shear_exact["pdeTimeDerivativeCosineCoefficient"] == shear_expected["pdeTimeDerivativeCosineCoefficient"]
checks["integer_shear"]["pde_time_sine"] = integer_shear_exact["pdeTimeDerivativeSineCoefficient"] == shear_expected["pdeTimeDerivativeSineCoefficient"]
checks["integer_shear"]["pde_transport_sine"] = integer_shear_exact["pdeTransportSineCoefficient"] == shear_expected["pdeTransportSineCoefficient"]
checks["integer_shear"]["pde_laplacian_cosine"] = integer_shear_exact["pdeNegativeLaplacianCosineCoefficient"] == shear_expected["pdeNegativeLaplacianCosineCoefficient"]
checks["integer_shear"]["pde_cosine_residual"] = integer_shear_exact["pdeCosineResidual"] == "0" && shear_expected["pdeCosineResidual"] == "0"
checks["integer_shear"]["pde_sine_residual"] = integer_shear_exact["pdeSineResidual"] == "0" && shear_expected["pdeSineResidual"] == "0"
checks["integer_shear"]["exact_shear_text"] = compact_main.include?("unforcedthree-dimensionalNavier--Stokesequation") && compact_main.include?("(\\partial_t+B_L\\partial_2-\\partial_2^2)F_L=0")

operator_expected = expected.fetch("operatorSample")
checks["operator"]["operator_sample_domain"] = operator_eta.positive? && operator_polynomial.length == 3
checks["operator"]["l_eta"] = operator_exact["lEtaCoefficientsAscending"] == operator_expected["lEtaCoefficientsAscending"]
checks["operator"]["second_derivative"] = operator_exact["secondDerivativeCoefficientsAscending"] == operator_expected["secondDerivativeCoefficientsAscending"]
checks["operator"]["difference"] = operator_exact["differenceCoefficientsAscending"] == operator_expected["differenceCoefficientsAscending"]
checks["operator"]["first_order_sign"] = operator_exact["firstOrderImaginarySignPositive"] && operator_expected["firstOrderImaginarySignPositive"]
checks["operator"]["degree_preserved"] = operator_exact["degreePreserved"] && operator_expected["degreePreserved"]
checks["operator"]["operator_text"] = compact_main.include?("(1+i\\etaw)^2D_w^2+i\\eta(1+i\\etaw)D_w")
checks["operator"]["weighted_norm_text"] = main_text.include?("||p||_rho=sum |p_k|rho^k") && compact_main.include?("\\|\\mathcalL_\\eta-D_w^2\\|\\leC\\etam^2")
checks["operator"]["duhamel_text"] = compact_main.include?("\\|e^{t\\mathcalL_\\eta}T_m-e^{tD_w^2}T_m\\|_\\rho")
checks["operator"]["confluence_rate_text"] = compact_main.include?("-\\frac9{40000}L^2+o(L^2)")

geometry_expected = expected.fetch("geometryClockSample")
checks["geometry_clock"]["geometry_sample_domain"] = geometry_a > geometry_delta0 && geometry_delta > geometry_delta0 && geometry_r_scale.positive?
checks["geometry_clock"]["a_value"] = geometry_exact["A"] == geometry_expected["A"]
checks["geometry_clock"]["e_a"] = geometry_exact["eA"] == geometry_expected["eA"]
checks["geometry_clock"]["scaled_velocity"] = geometry_exact["scaledVelocity"] == geometry_expected["scaledVelocity"]
checks["geometry_clock"]["background_shear"] = geometry_exact["backgroundShear"] == geometry_expected["backgroundShear"]
checks["geometry_clock"]["gamma"] = geometry_exact["gamma"] == geometry_expected["gamma"]
checks["geometry_clock"]["subcap_left"] = geometry_exact["rCenterMinusThreeHalfWidths"] == geometry_expected["rCenterMinusThreeHalfWidths"]
checks["geometry_clock"]["subcap_right"] = geometry_exact["rCenterPlusThreeHalfWidths"] == geometry_expected["rCenterPlusThreeHalfWidths"]
checks["geometry_clock"]["strict_subcap"] = geometry_exact["strictSubcapGeometry"] && geometry_expected["strictSubcapGeometry"]
checks["geometry_clock"]["positive_coordinate"] = geometry_exact["positiveEdgeCoordinate"] == geometry_expected["positiveEdgeCoordinate"]
checks["geometry_clock"]["negative_coordinate"] = geometry_exact["negativeEdgeCoordinate"] == geometry_expected["negativeEdgeCoordinate"]
checks["geometry_clock"]["paired_gap"] = geometry_exact["pairedCoordinateGap"] == geometry_expected["pairedCoordinateGap"]
checks["geometry_clock"]["subcap_coordinate"] = geometry_exact["subcapCoordinate"] == geometry_expected["subcapCoordinate"]
checks["geometry_clock"]["plateau_coordinate"] = geometry_exact["plateauCoordinate"] == geometry_expected["plateauCoordinate"]
checks["geometry_clock"]["cap_plateau_gap"] = geometry_exact["capPlateauGap"] == geometry_expected["capPlateauGap"]
checks["geometry_clock"]["terminal_cap"] = geometry_exact["terminalCapCoordinate"] == geometry_expected["terminalCapCoordinate"]
checks["geometry_clock"]["terminal_plateau"] = geometry_exact["terminalPlateauCoordinate"] == geometry_expected["terminalPlateauCoordinate"]
checks["geometry_clock"]["terminal_gap"] = geometry_exact["terminalCoordinateGap"] == geometry_expected["terminalCoordinateGap"]
checks["geometry_clock"]["strip_z"] = geometry_exact["plateauStripZ"] == geometry_expected["plateauStripZ"]
checks["geometry_clock"]["strip_width"] = geometry_exact["plateauStripZWidth"] == geometry_expected["plateauStripZWidth"]
checks["geometry_clock"]["area_endpoints"] = geometry_exact["areaOverPiAtStripEndpoints"] == geometry_expected["areaOverPiAtStripEndpoints"]
checks["geometry_clock"]["integrated_area"] = geometry_exact["integratedStripAreaOverPi"] == geometry_expected["integratedStripAreaOverPi"]
checks["geometry_clock"]["velocity_sign"] = geometry_exact["velocitySign"] == geometry_expected["velocitySign"]
checks["geometry_clock"]["weight_sign"] = geometry_exact["positiveWeightSign"] == geometry_expected["positiveWeightSign"]
checks["geometry_clock"]["square_difference_sign"] = geometry_exact["pairedSquareDifferenceSign"] == geometry_expected["pairedSquareDifferenceSign"]
checks["geometry_clock"]["flux_sign"] = geometry_exact["pairedFluxSign"] == geometry_expected["pairedFluxSign"]
checks["geometry_clock"]["complete_clock_absorption_text"] = compact_main.include?("-2(F_4-F_3)\\mu^2+o(\\mu^2)") && compact_main.include?("\\mathcalS_L>0")

normalization_expected = expected.fetch("normalizationSample")
checks["normalization"]["flux_monomial"] = normalization_exact["physicalFlux"] == normalization_expected["physicalFlux"]
checks["normalization"]["mass_monomial"] = normalization_exact["plateauMass"] == normalization_expected["plateauMass"]
checks["normalization"]["unweighted_quotient"] = normalization_exact["unweightedQuotient"] == normalization_expected["unweightedQuotient"]
checks["normalization"]["r_weighted_quotient"] = normalization_exact["rWeightedQuotient"] == normalization_expected["rWeightedQuotient"]
checks["normalization"]["lower_a_power"] = normalization_exact["lowerBoundAExponent"] == normalization_expected["lowerBoundAExponent"]
checks["normalization"]["lower_h_power"] = normalization_exact["lowerBoundTerminalLayerExponent"] == normalization_expected["lowerBoundTerminalLayerExponent"]
checks["normalization"]["upper_a_power"] = normalization_exact["upperBoundAExponent"] == normalization_expected["upperBoundAExponent"]
checks["normalization"]["upper_h_power"] = normalization_exact["upperBoundTerminalLayerExponent"] == normalization_expected["upperBoundTerminalLayerExponent"]
checks["normalization"]["normalized_plateau"] = normalization_exact["normalizedPlateau"] == normalization_expected["normalizedPlateau"]
checks["normalization"]["normalized_flux"] = normalization_exact["normalizedFlux"] == normalization_expected["normalizedFlux"]
checks["normalization"]["normalized_quotient"] = normalization_exact["normalizedQuotientFactor"] == normalization_expected["normalizedQuotientFactor"]
checks["normalization"]["omega_third_rate"] = omega_third_rate == -Rational(2, 11_907) && normalization_exact["omegaThirdLogRate"] == normalization_expected["omegaThirdLogRate"]
checks["normalization"]["a_square_density"] = normalization_exact["aSquaredLeadingDensity"] == normalization_expected["aSquaredLeadingDensity"]
checks["normalization"]["penalty_coefficient"] = normalization_exact["aSquaredPenaltyCoefficient"] == normalization_expected["aSquaredPenaltyCoefficient"]
checks["normalization"]["penalty_log_rate"] = penalty_log_rate == omega_third_rate && normalization_exact["aSquaredPenaltyLogRate"] == normalization_expected["aSquaredPenaltyLogRate"]
formal_exact = normalization_exact.fetch("formalHighDegree")
formal_expected = normalization_expected.fetch("formalHighDegree")
checks["normalization"]["formal_status"] = formal_exact["status"] == "OPEN_DIRECTION" && formal_expected["status"] == "OPEN_DIRECTION"
checks["normalization"]["formal_saddle"] = formal_exact["integrationSaddleCoefficient"] == formal_expected["integrationSaddleCoefficient"]
checks["normalization"]["formal_displacement"] = formal_exact["physicalDisplacementCoefficient"] == formal_expected["physicalDisplacementCoefficient"]
checks["normalization"]["formal_tilt"] = formal_exact["tiltCoefficient"] == formal_expected["tiltCoefficient"]
checks["normalization"]["formal_squared_ratio"] = formal_exact["squaredRatioExponentCoefficient"] == formal_expected["squaredRatioExponentCoefficient"]
checks["normalization"]["formal_critical_kappa"] = formal_exact["criticalKappa"] == formal_expected["criticalKappa"]
checks["normalization"]["formal_threshold"] = formal_exact["sampleExceedsFormalThreshold"] && formal_expected["sampleExceedsFormalThreshold"]
checks["normalization"]["open_boundary_text"] = main_text.include?("derived **OPEN DIRECTION**, not a theorem") && compact_primary.include?("L.70--L.72arecorrectlymarked**OPEN**")

backward_expected = expected.fetch("backwardHeatSample")
checks["backward_heat"]["backward_sample_domain"] = backward_degree == 2 * backward_n && backward_t.positive?
checks["backward_heat"]["chebyshev_degree"] = backward_chebyshev == [-1, 0, 18, 0, -48, 0, 32]
checks["backward_heat"]["terms"] = backward_exact["terms"] == backward_expected["terms"] && backward_terms.sum == backward_absolute
checks["backward_heat"]["backward_polynomial"] = backward_exact["backwardPolynomialCoefficientsAscending"] == backward_expected["backwardPolynomialCoefficientsAscending"]
checks["backward_heat"]["forward_polynomial"] = backward_exact["wrongForwardPolynomialCoefficientsAscending"] == backward_expected["wrongForwardPolynomialCoefficientsAscending"]
checks["backward_heat"]["backward_absolute"] = backward_exact["exactAbsoluteValue"] == backward_expected["exactAbsoluteValue"]
checks["backward_heat"]["forward_absolute"] = backward_exact["wrongForwardSignAbsoluteValue"] == backward_expected["wrongForwardSignAbsoluteValue"]
checks["backward_heat"]["imaginary_coefficients"] = backward_exact["imaginaryAxisPositiveEvenCoefficients"] == backward_expected["imaginaryAxisPositiveEvenCoefficients"]
checks["backward_heat"]["imaginary_terms"] = backward_exact["imaginaryAxisTerms"] == backward_expected["imaginaryAxisTerms"]
checks["backward_heat"]["imaginary_value"] = backward_exact["imaginaryAxisValue"] == backward_expected["imaginaryAxisValue"]
checks["backward_heat"]["forward_backward_distinct"] = backward_exact["forwardBackwardDistinct"] && backward_expected["forwardBackwardDistinct"]

diagnostic_expected = expected.fetch("diagnostic")
checks["diagnostic"]["config_schema"] = config["schema"] == diagnostic_fixture["schema"]
checks["diagnostic"]["config_parameters"] = config["heatTime"].to_f == fraction(diagnostic_fixture["heatTime"]).to_f &&
  config["AValues"] == diagnostic_fixture["AValues"] &&
  config["degreePowers"].map { |value| fraction_string(fraction(value)) } == diagnostic_fixture["degreePowers"] &&
  config["fineGridPoints"] == diagnostic_fixture["fineGridPoints"] &&
  config["coarseGridPoints"] == diagnostic_fixture["coarseGridPoints"] &&
  config["figureWidthMillimetres"] == diagnostic_fixture["figureWidthMillimetres"] &&
  config["figureHeightMillimetres"] == diagnostic_fixture["figureHeightMillimetres"]
checks["diagnostic"]["csv_shape"] = data_rows.length == diagnostic_fixture["rowCount"] && data_columns.length == diagnostic_fixture["columnCount"]
checks["diagnostic"]["csv_columns"] = data_columns == diagnostic_expected["columns"]
checks["diagnostic"]["grid_cartesian"] = diagnostic_a_values == diagnostic_fixture["AValues"] &&
  diagnostic_power_values == diagnostic_fixture["degreePowers"] &&
  data_rows.length == diagnostic_a_values.length * diagnostic_power_values.length
checks["diagnostic"]["degree_policy"] = data_rows.all? do |row|
  target = Integer(row["A"])**row["degreePower"].to_f
  nearest_even = [(target / 2.0).round * 2, 2].max
  Integer(row["m"]) == nearest_even
end
mu_tolerance = fraction(diagnostic_fixture["muIdentityRelativeTolerance"]).to_f
checks["diagnostic"]["mu_identity"] = data_rows.all? do |row|
  recomputed = (Integer(row["m"])**2.to_f / Integer(row["A"]))**(1.0 / 3.0)
  observed = row["mu"].to_f
  (observed - recomputed).abs <= mu_tolerance * [1.0, recomputed.abs].max
end
limit_tolerance = fraction(diagnostic_fixture["limitDecimalTolerance"]).to_f
checks["diagnostic"]["limit_decimals"] = diagnostic_exact["theoreticalLimitDecimals"] == diagnostic_expected["theoreticalLimitDecimals"] &&
  data_rows.all? do |row|
    (row["saddleLimit"].to_f - saddle_limit_decimal.to_f).abs <= limit_tolerance &&
      (row["amplitudeLimit"].to_f - amplitude_limit_decimal.to_f).abs <= limit_tolerance &&
      (row["tiltLimit"].to_f - tilt_limit_decimal.to_f).abs <= limit_tolerance
  end
checks["diagnostic"]["saddle_residual"] = diagnostic_max.call("saddleDerivativeResidual") <= fraction(diagnostic_fixture["saddleResidualTolerance"]).to_f &&
  diagnostic_exact["maximumSaddleDerivativeResidual"] == diagnostic_expected["maximumSaddleDerivativeResidual"]
checks["diagnostic"]["coarse_amplitude"] = diagnostic_max.call("coarseFineAmplitudeDelta") <= fraction(diagnostic_fixture["coarseFineTolerance"]).to_f &&
  diagnostic_exact["maximumCoarseFineAmplitudeDelta"] == diagnostic_expected["maximumCoarseFineAmplitudeDelta"]
checks["diagnostic"]["coarse_tilt"] = diagnostic_max.call("coarseFineTiltDelta") <= fraction(diagnostic_fixture["coarseFineTolerance"]).to_f &&
  diagnostic_exact["maximumCoarseFineTiltDelta"] == diagnostic_expected["maximumCoarseFineTiltDelta"]
checks["diagnostic"]["phase_amplitude"] = diagnostic_max.call("phaseDropAmplitudeDelta") <= fraction(diagnostic_fixture["phaseDropTolerance"]).to_f &&
  diagnostic_exact["maximumPhaseDropAmplitudeDelta"] == diagnostic_expected["maximumPhaseDropAmplitudeDelta"]
checks["diagnostic"]["phase_tilt"] = diagnostic_max.call("phaseDropTiltDelta") <= fraction(diagnostic_fixture["phaseDropTolerance"]).to_f &&
  diagnostic_exact["maximumPhaseDropTiltDelta"] == diagnostic_expected["maximumPhaseDropTiltDelta"]
checks["diagnostic"]["finite_values"] = data_rows.all? do |row|
  data_columns.all? { |column| row[column] && row[column].to_f.finite? }
end
checks["diagnostic"]["progress_count"] = progress_rows.length == diagnostic_fixture["progressEventCount"] && diagnostic_exact["progressEventCount"] == diagnostic_expected["progressEventCount"]
checks["diagnostic"]["progress_stages"] = diagnostic_exact["progressStages"] == diagnostic_expected["progressStages"] && progress_rows.last["status"] == "PASS"
checks["diagnostic"]["resource_count"] = resource_rows.length == diagnostic_fixture["resourceSampleCount"] && diagnostic_exact["resourceSampleCount"] == diagnostic_expected["resourceSampleCount"]
checks["diagnostic"]["png_signature"] = png["signature"]
checks["diagnostic"]["png_crc"] = png["crc"]
checks["diagnostic"]["png_pixels"] = diagnostic_exact["pngPixels"] == diagnostic_expected["pngPixels"] && diagnostic_exact["pngPixels"] == diagnostic_fixture["pngPixels"]
checks["diagnostic"]["png_dpi"] = diagnostic_exact["pngDpi"] == diagnostic_expected["pngDpi"] && diagnostic_exact["pngDpi"] == diagnostic_fixture["pngDpi"]
checks["diagnostic"]["pdf_pages"] = diagnostic_exact["pdfPages"] == diagnostic_expected["pdfPages"] && diagnostic_exact["pdfPages"] == diagnostic_fixture["pdfPages"]
checks["diagnostic"]["pdf_unencrypted"] = diagnostic_exact["pdfEncrypted"] == false && diagnostic_expected["pdfEncrypted"] == false
checks["diagnostic"]["pdf_no_javascript"] = diagnostic_exact["pdfHasJavaScript"] == false && diagnostic_expected["pdfHasJavaScript"] == false
checks["diagnostic"]["svg_dimensions"] = diagnostic_exact["svgWidth"] == diagnostic_expected["svgWidth"] && diagnostic_exact["svgHeight"] == diagnostic_expected["svgHeight"]
checks["diagnostic"]["panel_count"] = diagnostic_exact["panelCount"] == 3 && diagnostic_expected["panelCount"] == 3
checks["diagnostic"]["away_sequence"] = away_errors.each_cons(2).all? { |left, right| right > left } &&
  diagnostic_exact["knownPreasymptoticAwaySequence"] == diagnostic_expected["knownPreasymptoticAwaySequence"]
checks["diagnostic"]["monotonicity_boundary"] = diagnostic_exact["monotonicityRequired"] == false && diagnostic_expected["monotonicityRequired"] == false
checks["diagnostic"]["finite_only"] = diagnostic_exact["finiteDiagnosticOnly"] && diagnostic_expected["finiteDiagnosticOnly"] && compact_source.include?("ItdoesnotprovetheLaplaceprinciple")

checks["sources"]["dlmf_185"] = source_text.include?("https://dlmf.nist.gov/18.5")
checks["sources"]["dlmf_189"] = source_text.include?("https://dlmf.nist.gov/18.9")
checks["sources"]["dlmf_1814"] = source_text.include?("https://dlmf.nist.gov/18.14")
checks["sources"]["hall_ho"] = source_text.include?("10.1007/s11005-025-01946-9")
checks["sources"]["kabluchko"] = source_text.include?("10.5802/ahl.227.pdf")
checks["sources"]["dominici"] = source_text.include?("math/0601078")
checks["sources"]["batahan_shehata"] = source_text.include?("Hermite-Chebyshev Polynomials with Their Generalized Form")
checks["sources"]["khan"] = source_text.include?("Certain Results for the Hermite and Chebyshev Polynomials of 2-Variables")
checks["sources"]["rosenbloom_widder"] = source_text.include?("10.1090/S0002-9947-1959-0107118-2")
checks["sources"]["ditzian"] = source_text.include?("10.1017/S144678870000968X")
checks["sources"]["bounded_search"] = source_text.include?("bounded primary-source search")
checks["sources"]["operational_prior_art"] = source_text.include?("fixed-scale operational identities are prior art")
checks["sources"]["no_novelty_priority"] = source_text.include?("not evidence of novelty, priority, or nonexistence")
checks["sources"]["search_stop"] = source_text.include?("Search stopped")
checks["sources"]["deep_research_boundary"] = source_text.include?("Deep Research was used") && source_text.include?("planning helper was unavailable")

claims = fixtures.fetch("claims")
claims_expected = expected.fetch("claims")
checks["boundary"]["explicit_family"] = claims["explicitStartPrepaidFamily"] && main_text.include?("one exact start-prepaid family")
checks["boundary"]["forward_heat"] = claims["forwardHeatObject"] && main_text.include?("forward Chebyshev edge object")
checks["boundary"]["complete_clock_positive"] = claims["completeClockEventuallyPositiveForFamily"] && compact_main.include?("\\mathcalS_L>0")
checks["boundary"]["full_plateau"] = claims["fullPhysicalPlateauUsed"] && main_text.include?("Full-plateau payment")
checks["boundary"]["normalized_rate"] = claims["normalizedQuadraticRateEstablishedForFamily"] && compact_main.include?("=-\\frac2{11907}<0")
checks["boundary"]["scale_reduction"] = claims["fixedSliceMuThreeHalvesReducedToClockMu"] && main_text.include?("static exponent `mu^(3/2)` to the parabolic exponent")
checks["boundary"]["candidate_killed"] = claims["candidateKilledForThisFamily"] && source_text.include?("rules out this family as a counterexample")
checks["boundary"]["formal_figure"] = claims["formalScientificFigureIncluded"] && files.key?("figureSvg") && files.key?("figurePdf") && files.key?("figurePng")
checks["boundary"]["finite_diagnostic"] = claims["finiteDiagnosticIncluded"] && main_text.include?("Finite diagnostic and its boundary")
checks["boundary"]["no_terminal_prepaid"] = !claims["terminalPrepaidConstructionUsed"] && !main_text.include?("terminal-prepaid")
checks["boundary"]["arbitrary_open"] = !claims["uniformArbitraryPacketTheorem"] && main_text.include?("not a uniform theorem for arbitrary packets")
checks["boundary"]["a2_boundary_open"] = !claims["mComparableToA2Covered"] && main_text.include?("does not cover `m` comparable with or larger than `A^2`")
checks["boundary"]["bulk_a4_open"] = !claims["bulkA4SaddleTheorem"] && main_text.include?("OPEN DIRECTION")
checks["boundary"]["version_m_open"] = !claims["versionMTransfer"] && main_text.include?("Version-M")
checks["boundary"]["regularity_open"] = !claims["regularityClaimed"] && main_text.include?("regularity")
checks["boundary"]["singularity_open"] = !claims["singularityClaimed"] && main_text.include?("singularity")
checks["boundary"]["no_simulation"] = !claims["simulationClaimed"] && !source_text.include?("simulation establishes")
checks["boundary"]["finite_not_proof"] = !claims["finiteDiagnosticProvesLimit"] && compact_source.include?("ItdoesnotprovetheLaplaceprinciple")
checks["boundary"]["no_novelty"] = !claims["noveltyClaimed"] && source_text.include?("not evidence of novelty")
checks["boundary"]["no_priority"] = !claims["priorityClaimed"] && source_text.include?("priority")
checks["boundary"]["not_clay"] = !claims["clayClaimed"] && [main_text, source_text, primary_text].all? { |body| body.include?("**NOT CLAY.**") }
checks["boundary"]["primary_pass"] = primary_text.include?("**PASS -- for the explicit start-prepaid exact-shear family")
checks["boundary"].keys.each do |name|
  checks["boundary"][name] &&= claims == claims_expected
end

# The expected object is checked before the Python certificate is opened.
expected_without_schema = expected.reject { |key, _value| key == "schema" }
local_exact_agrees = exact == expected_without_schema

python_json = nil
python_error = nil
begin
  python_json = JSON.parse(File.read(PYTHON_JSON_PATH, encoding: "UTF-8"))
rescue Errno::ENOENT, JSON::ParserError => error
  python_error = error.message
end
python_bindings = python_json.is_a?(Hash) && python_json["bindings"].is_a?(Hash) ? python_json["bindings"] : {}
python_binding_subset = binding_specs.all? do |relative, expected_hash|
  row = python_bindings[relative]
  row.is_a?(Hash) && row["expectedSha256"] == expected_hash &&
    row["observedSha256"] == bindings.fetch(relative)["observedSha256"] && row["pass"] == true
end
checks["python_cross"]["json_available"] = python_error.nil?
checks["python_cross"]["json_object"] = python_json.is_a?(Hash)
checks["python_cross"]["required_fields"] = python_json.is_a?(Hash) && %w[
  verdict freezeReady assertionsTotal assertionsPassed exact bindings
].all? { |key| python_json.key?(key) }
checks["python_cross"]["python_pass"] = python_json.is_a?(Hash) && python_json["verdict"] == "PASS"
checks["python_cross"]["python_freeze_ready"] = python_json.is_a?(Hash) &&
  python_json["freezeReady"] == freeze_ready
checks["python_cross"]["assertion_count"] = python_json.is_a?(Hash) &&
  python_json["assertionsTotal"].is_a?(Integer) && python_json["assertionsTotal"].positive? &&
  python_json["assertionsPassed"] == python_json["assertionsTotal"]
checks["python_cross"]["exact_object"] = python_json.is_a?(Hash) && python_json["exact"].is_a?(Hash) && !python_json["exact"].empty?
checks["python_cross"]["exact_agrees"] = local_exact_agrees && python_json.is_a?(Hash) && python_json["exact"] == exact
checks["python_cross"]["bindings_object"] = python_json.is_a?(Hash) && python_json["bindings"].is_a?(Hash)
checks["python_cross"]["binding_subset"] = python_binding_subset
python_structure = python_json.is_a?(Hash) && python_json["exact"].is_a?(Hash) ? python_json.dig("exact", "structure") : nil
checks["python_cross"]["structure_agrees"] = python_structure == exact["structure"]

unless checks.keys == GROUPS.keys && GROUPS.all? { |group, names| checks.fetch(group).keys == names }
  abort("R0.76L Ruby assertion inventory mismatch")
end

failures = checks.each_with_object([]) do |(group, rows), output|
  rows.each { |name, passed| output << "#{group}.#{name}" unless passed }
end
assertions = GROUPS.values.map(&:length).sum
verdict = failures.empty? && (freeze_ready || DEVELOPMENT) && local_exact_agrees ? "PASS" : "FAIL"
freeze_ready = verdict == "PASS" && freeze_ready

payload = {
  "schema" => INDEPENDENT_SCHEMA,
  "verdict" => verdict,
  "freezeReady" => freeze_ready,
  "sourceCommitReady" => source_commit_ready,
  "development" => DEVELOPMENT,
  "assertionsTotal" => assertions,
  "assertionsPassed" => assertions - failures.length,
  "failures" => failures,
  "negativeMutations" => NEGATIVE_MUTATIONS,
  "bindings" => bindings,
  "exact" => exact
}

unless RUBY_JSON_PATH.empty?
  File.write(RUBY_JSON_PATH, JSON.pretty_generate(payload) + "\n", encoding: "UTF-8")
end

report = [
  "# R0.76L independent finite audit",
  "",
  "- Verdict: **#{verdict}**",
  "- Freeze-ready hash seal: **#{freeze_ready ? 'yes' : 'no'}**",
  "- Source commit ready: **#{source_commit_ready ? 'yes' : 'no'}**",
  "- Ruby assertions: #{assertions - failures.length}/#{assertions}",
  "- Ruby exact object matches frozen expected object: #{local_exact_agrees ? 'PASS' : 'FAIL'}",
  "- Python/Ruby exact cross-check: #{checks.dig('python_cross', 'exact_agrees') ? 'PASS' : 'FAIL'}",
  "- Exact cubic-field saddle: z4=#{z4.to_a.inspect}, F4=#{f4.to_a.inspect}, G4=#{g4.to_a.inspect}",
  "- Exact normalized logarithmic rate: #{fraction_string(omega_third_rate)}",
  "- Diagnostic rows: #{data_rows.length}; PNG: #{png['width']}x#{png['height']} at #{png['dpi']} dpi; PDF pages: #{diagnostic_exact['pdfPages']}",
  "- Failures: #{failures.empty? ? 'none' : failures.join(', ')}",
  "",
  "## Finite-audit boundary",
  "",
  "This Ruby verifier independently recomputes the exact rational and cubic-field",
  "ledgers, heat-polynomial samples, integer modes, conjugated operator, paired",
  "geometry, normalization, backward-heat sign, hashes, diagnostic data, and",
  "claim gates before consulting the Python JSON. It does not prove the continuum",
  "Laplace principle, the growing-degree semigroup estimate, the complete-clock",
  "limit, or a Navier--Stokes regularity/singularity claim. **NOT CLAY.**",
  ""
]
File.write(REPORT_PATH, report.join("\n"), encoding: "UTF-8")

puts JSON.generate(
  "suite" => "r076l-parabolic-edge-smoothing-complete-clock-independent",
  "status" => verdict,
  "assertions" => assertions,
  "failures" => failures.length,
  "sourceCommitReady" => source_commit_ready
)
exit(verdict == "PASS" ? 0 : 1)
