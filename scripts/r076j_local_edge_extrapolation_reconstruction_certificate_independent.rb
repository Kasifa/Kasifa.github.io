#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed finite verifier for R0.76J.
#
# This implementation uses only Ruby's standard library.  It recomputes the
# Laguerre samples, tail margin, endpoint/plateau constants, and asymptotic
# rational rate without invoking the Python certificate.  The Python JSON is
# read only after those calculations, as a cross-implementation consistency
# check.  Finite checks do not prove Plancherel, the Volterra induction, any
# imported theorem, or a continuum Navier--Stokes implication.

require "digest"
require "json"

ROOT = File.expand_path("..", __dir__)
STEM = "r076j_local_edge_extrapolation_reconstruction"
MAIN = File.join(ROOT, "research", "#{STEM}.md")
SOURCE = File.join(ROOT, "research", "r076j_report-source.md")
PRIMARY = File.join(ROOT, "research", "#{STEM}_primary_audit.md")
R076I_MAIN = File.join(ROOT, "research", "r076i_chebyshev_scale_full_plateau_window.md")
R076I_PRIMARY = File.join(ROOT, "research", "r076i_chebyshev_scale_full_plateau_window_primary_audit.md")
PYTHON_JSON = ENV.fetch("R076J_JSON", File.join(ROOT, "research", "#{STEM}_certificate.json"))
REPORT = ENV.fetch("R076J_RUBY_REPORT", File.join(ROOT, "research", "#{STEM}_independent_audit.md"))
RUBY_JSON = ENV.fetch("R076J_RUBY_JSON", "")
MUTATION = ENV.fetch("R076J_RUBY_MUTATION", "")

SHA256 = /\A[0-9a-f]{64}\z/
CORE_COMMIT = "0b73f68e072e573d9aaaa824e137e29a49d3cd67"

# Generated certificate/report/audit files are intentionally absent: binding
# them would create a self-referential hash cycle.
FROZEN = {
  "research/#{STEM}.md" => "a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f",
  "research/r076j_report-source.md" => "371eac6e3f053d4ba51ded16f35024ba805d10c5a81c1f01879704ce583763c7",
  "research/#{STEM}_primary_audit.md" => "1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5",
  "research/r076i_chebyshev_scale_full_plateau_window.md" => "6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce",
  "research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md" => "65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe",
  "scripts/#{STEM}_fixtures.json" => "f0957b65e763339d1ff8cc029a13e13231b22b44dff8796b3b21883ffb352c31",
  "scripts/#{STEM}_expected.json" => "9e5ad2f9bed318cd1232319240d2e574f070eda0364f97957df9c013f35878e8"
}.freeze

GROUPS = {
  "bindings" => %w[
    main_hash source_hash primary_audit_hash r076i_main_hash
    r076i_primary_hash fixture_hash expected_hash hash_specs_well_formed generated_outputs_unbound
    upstream_hashes_stated upstream_commit_stated primary_bound_objects
  ],
  "integrity" => %w[
    main_utf8 source_utf8 primary_utf8 no_controls no_cr no_trailing
    tag_sequence tag_count display_balance display_count reference_closure
  ],
  "laguerre" => %w[
    sample_table series_recurrence_agree y_zero_identity positivity
    order_zero_identity finite_series_bound finite_exponential_bound
    basis_index_range negative_majorant positive_majorant
  ],
  "tail" => %w[
    cutoff_multiplier alpha_choice cutoff_two exponent_split
    threshold_identity threshold_inequality exponential_partial_sum
    exponential_over_100 strict_tail_margin finite_range_factor
    tail_text_chain zero_function_guard
  ],
  "edge" => %w[
    alpha_n_product squared_prefactor amplitude_prefactor
    laguerre_squared_exponent amplitude_exponent bilateral_exponent
    reflection range_all_nonnegative complex_coefficients real_frequencies
    collisions_merged no_spacing_assumption
  ],
  "plateau" => %w[
    sample_e_a sample_delta_a branch_count exterior_prefactor
    interior_prefactor holder_prefactor squared_exponent q_exponent
    phi_definition full_observation physical_bound normalized_bound
  ],
  "asymptotic" => %w[
    mode_window omega_input omega_third_rate normalized_rate
    exponent_scale polynomial_scale exact_rate_text j46_text
  ],
  "sources" => %w[
    zhang_versioned_abs zhang_versioned_pdf erdelyi_journal
    garcia_ross kos_doi architecture_attribution no_black_box
    bounded_search no_priority_search_claim
  ],
  "boundary" => %w[
    literature_label proved_locally finite_computation open_label
    exact_shear_scope arbitrary_field_open regularity_open singularity_open
    no_simulation no_figure no_novelty no_priority not_clay
  ],
  "python_cross" => %w[
    json_object required_fields verdict freeze_ready assertions_positive
    exact_object bindings_object frozen_binding_subset
  ]
}.freeze

NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze
abort("duplicate mutation name in R0.76J Ruby suite") unless
  NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

if ENV.fetch("R076J_RUBY_LIST_MUTATIONS", "") == "1"
  puts NEGATIVE_MUTATIONS
  exit 0
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

def fraction_string(value)
  value.denominator == 1 ? value.numerator.to_s : "#{value.numerator}/#{value.denominator}"
end

def digest(relative)
  path = File.join(ROOT, relative)
  File.file?(path) ? Digest::SHA256.file(path).hexdigest : nil
end

def binding_row(relative, expected)
  observed = digest(relative)
  {
    "expectedSha256" => expected,
    "observedSha256" => observed || "MISSING",
    "exists" => File.file?(File.join(ROOT, relative)),
    "locked" => SHA256.match?(expected),
    "pass" => SHA256.match?(expected) && observed == expected
  }
end

def binomial(n, k)
  return 0 if k.negative? || k > n

  k = [k, n - k].min
  (1..k).reduce(1) { |value, j| value * (n - k + j) / j }
end

# Direct finite defining series for L_m(-y).
def laguerre_series(m, y)
  (0..m).reduce(Rational(0)) do |sum, ell|
    sum + Rational(binomial(m, ell), 1) * y**ell / (1..ell).reduce(1, :*)
  end
end

# Independent three-term recurrence for the same polynomial.
def laguerre_recurrence(m, y)
  return Rational(1) if m.zero?
  return Rational(1) + y if m == 1

  previous = Rational(1)
  current = Rational(1) + y
  (1...m).each do |index|
    following = ((2 * index + 1) * current + y * current - index * previous) / (index + 1)
    previous = current
    current = following
  end
  current
end

main_raw = File.binread(MAIN)
source_raw = File.binread(SOURCE)
primary_raw = File.binread(PRIMARY)
r076i_main_raw = File.binread(R076I_MAIN)
r076i_primary_raw = File.binread(R076I_PRIMARY)
main_text = main_raw.dup.force_encoding("UTF-8")
source_text = source_raw.dup.force_encoding("UTF-8")
primary_text = primary_raw.dup.force_encoding("UTF-8")
cm = compact(main_text)
cs = compact(source_text)
cp = compact(primary_text)

begin
  python_json = JSON.parse(File.read(PYTHON_JSON, encoding: "UTF-8"))
rescue Errno::ENOENT, JSON::ParserError => error
  warn "R0.76J Python certificate unavailable or invalid: #{error.message}"
  exit 2
end

bindings = FROZEN.keys.sort.to_h do |relative|
  [relative, binding_row(relative, FROZEN.fetch(relative))]
end
freeze_ready = bindings.values.all? { |row| row.fetch("locked") && row.fetch("pass") }

tags = main_text.scan(/\\tag\{J\.(\d+)\}/).flatten.map(&:to_i)
refs = main_text.scan(/(?<![A-Za-z0-9_.])J\.(\d+)/).flatten.map(&:to_i)
display_opens = main_text.scan(/^\\\[$/).length
display_closes = main_text.scan(/^\\\]$/).length

laguerre_expected = {
  "0@1/2" => Rational(1),
  "1@1/2" => Rational(3, 2),
  "2@1/2" => Rational(17, 8),
  "3@1/2" => Rational(139, 48),
  "4@1/2" => Rational(1473, 384),
  "5@1/2" => Rational(19_091, 3840),
  "0@2" => Rational(1),
  "1@2" => Rational(3),
  "2@2" => Rational(7),
  "3@2" => Rational(43, 3),
  "4@2" => Rational(27),
  "5@2" => Rational(719, 15)
}.freeze
laguerre_observed = laguerre_expected.keys.to_h do |key|
  m_text, y_text = key.split("@", 2)
  [key, laguerre_series(Integer(m_text), Rational(y_text))]
end

laguerre_grid = (0..12).flat_map do |m|
  [Rational(0), Rational(1, 8), Rational(1, 2), Rational(2), Rational(5), Rational(25)].map do |y|
    [m, y]
  end
end
laguerre_bound_margins = laguerre_grid.map do |m, y|
  value = laguerre_series(m, y).to_f
  bound = Math.exp(2.0 * Math.sqrt(m * y.to_f))
  bound - value
end

# The first seven nonnegative exponential-series terms mean k=0,...,6.
exp5_partial = (0..6).reduce(Rational(0)) do |sum, k|
  sum + Rational(5**k, (1..k).reduce(1, :*))
end
partial_tail_upper = Rational(5, 1) / exp5_partial
strict_tail_margin = Rational(1, 20) - partial_tail_upper

sample_n = 3
sample_alpha = Rational(25 * sample_n, 2)
tail_cutoff = Rational(25 * sample_n, 1) / sample_alpha
alpha_n_product = Rational(20, 19) * sample_alpha * sample_n
edge_squared_prefactor = Rational(250, 19)
edge_amplitude_prefactor_squared = Rational(250, 19)

sample_a = 64
sample_delta0 = Rational(1, 10)
sample_delta = Rational(1, 2)
sample_q = 3
sample_e_a = Rational(1) - sample_delta0 / sample_a
sample_delta_a = (sample_delta + sample_delta0) / (sample_a - sample_delta0)
branches = 2 * sample_q
exterior_numerator = Rational(250, 19) * branches**2 / sample_q**2
interior_numerator = Rational(250, 19) * branches**2 / sample_q**2
holder_at_half = Rational(1000, 19) * 2 # (2e)^(1/3)e^(-1) at e=1/2

mode_window = Rational(5, 2)
c_gamma = Rational(8, 3969)
omega_third_rate = -c_gamma / 12

checks = GROUPS.to_h do |group, names|
  [group, names.to_h { |name| [name, false] }]
end

checks["bindings"]["main_hash"] = bindings.fetch("research/#{STEM}.md").fetch("pass")
checks["bindings"]["source_hash"] = bindings.fetch("research/r076j_report-source.md").fetch("pass")
checks["bindings"]["primary_audit_hash"] = bindings.fetch("research/#{STEM}_primary_audit.md").fetch("pass")
checks["bindings"]["r076i_main_hash"] = bindings.fetch("research/r076i_chebyshev_scale_full_plateau_window.md").fetch("pass")
checks["bindings"]["r076i_primary_hash"] = bindings.fetch("research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md").fetch("pass")
checks["bindings"]["fixture_hash"] = bindings.fetch("scripts/#{STEM}_fixtures.json").fetch("pass")
checks["bindings"]["expected_hash"] = bindings.fetch("scripts/#{STEM}_expected.json").fetch("pass")
checks["bindings"]["hash_specs_well_formed"] = FROZEN.values.all? { |value| SHA256.match?(value) }
checks["bindings"]["generated_outputs_unbound"] = FROZEN.keys.none? do |path|
  path.end_with?("_certificate.json", "_certificate_report.md", "_independent_audit.md", "_qa_report.md") ||
    File.basename(path) == "AGENTS.md"
end
checks["bindings"]["upstream_hashes_stated"] = [
  FROZEN.fetch("research/r076i_chebyshev_scale_full_plateau_window.md"),
  FROZEN.fetch("research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md")
].all? { |value| main_text.include?(value) && primary_text.include?(value) }
checks["bindings"]["upstream_commit_stated"] = main_text.include?(CORE_COMMIT) && primary_text.include?(CORE_COMMIT)
checks["bindings"]["primary_bound_objects"] = [
  FROZEN.fetch("research/#{STEM}.md"),
  FROZEN.fetch("research/r076j_report-source.md")
].all? { |value| primary_text.include?(value) }

checks["integrity"]["main_utf8"] = clean_bytes(main_raw)
checks["integrity"]["source_utf8"] = clean_bytes(source_raw)
checks["integrity"]["primary_utf8"] = clean_bytes(primary_raw)
checks["integrity"]["no_controls"] = [main_raw, source_raw, primary_raw, r076i_main_raw, r076i_primary_raw].all? { |raw| clean_bytes(raw) }
checks["integrity"]["no_cr"] = [main_raw, source_raw, primary_raw].none? { |raw| raw.include?("\r") }
checks["integrity"]["no_trailing"] = [main_text, source_text, primary_text].all? do |text|
  text.lines.none? { |line| line.chomp.end_with?(" ", "\t") }
end
checks["integrity"]["tag_sequence"] = tags == (1..46).to_a
checks["integrity"]["tag_count"] = tags.length == 46
checks["integrity"]["display_balance"] = display_opens == display_closes
checks["integrity"]["display_count"] = display_opens == 48
checks["integrity"]["reference_closure"] = (refs.uniq - tags.uniq).empty?

checks["laguerre"]["sample_table"] = laguerre_observed == laguerre_expected
checks["laguerre"]["series_recurrence_agree"] = laguerre_grid.all? do |m, y|
  laguerre_series(m, y) == laguerre_recurrence(m, y)
end
checks["laguerre"]["y_zero_identity"] = (0..20).all? { |m| laguerre_series(m, 0) == 1 }
checks["laguerre"]["positivity"] = laguerre_grid.all? { |m, y| laguerre_series(m, y).positive? }
checks["laguerre"]["order_zero_identity"] = [0, Rational(1, 7), Rational(3), Rational(25)].all? do |y|
  laguerre_series(0, y) == 1
end
checks["laguerre"]["finite_series_bound"] = laguerre_grid.all? do |m, y|
  laguerre_series(m, y) <= (0..m).reduce(Rational(0)) do |sum, ell|
    sum + Rational((m * y)**ell, (1..ell).reduce(1, :*)**2)
  end
end
checks["laguerre"]["finite_exponential_bound"] = laguerre_bound_margins.min >= -1.0e-11
checks["laguerre"]["basis_index_range"] = cm.include?("\\sum_{m=0}^{N-1}L_m(-\\alphat)^2")
checks["laguerre"]["negative_majorant"] = cm.include?("|\\varphi_m(-x)|\\le\\sqrt\\alphae^{\\alphax/2}L_m(-\\alphax)")
checks["laguerre"]["positive_majorant"] = cm.include?("|\\varphi_m(t)|\\le\\sqrt\\alphae^{-\\alphat/2}L_m(-\\alphat)")

checks["tail"]["cutoff_multiplier"] = 25 * sample_n == 75
checks["tail"]["alpha_choice"] = sample_alpha == Rational(75, 2)
checks["tail"]["cutoff_two"] = tail_cutoff == 2
checks["tail"]["exponent_split"] = Rational(4, 5) + Rational(1, 5) == 1
checks["tail"]["threshold_identity"] = 4 * Math.sqrt(sample_n * 25 * sample_n) == Rational(4, 5) * 25 * sample_n
checks["tail"]["threshold_inequality"] = [1, 2, 3, 8].all? do |n|
  [25 * n, 36 * n, 100 * n].all? { |y| 4 * Math.sqrt(n * y) <= 4.0 * y / 5.0 + 1.0e-12 }
end
checks["tail"]["exponential_partial_sum"] = exp5_partial == Rational(81_445, 720)
checks["tail"]["exponential_over_100"] = exp5_partial > 100
checks["tail"]["strict_tail_margin"] = strict_tail_margin == Rational(1889, 325_780) && strict_tail_margin.positive?
checks["tail"]["finite_range_factor"] = Rational(1) / (1 - Rational(1, 20)) == Rational(20, 19)
checks["tail"]["tail_text_chain"] = [
  "25N/\\alpha", "5Ne^{-5N}<\\frac1{20}", "\\frac{19}{20}I_\\alpha(F)", "\\frac{20}{19}"
].all? { |fragment| cm.include?(fragment) }
checks["tail"]["zero_function_guard"] = main_text.include?("If `F=0`, J.11 is immediate") && main_text.include?("I_alpha(F)>0")

checks["edge"]["alpha_n_product"] = alpha_n_product == Rational(2250, 19)
checks["edge"]["squared_prefactor"] = edge_squared_prefactor == Rational(250, 19)
checks["edge"]["amplitude_prefactor"] = edge_amplitude_prefactor_squared == Rational(250, 19)
checks["edge"]["laguerre_squared_exponent"] = 4 * Math.sqrt(sample_n * sample_alpha) / (Math.sqrt(2) * sample_n) == 10.0
checks["edge"]["amplitude_exponent"] = Rational(10, 2) == 5
checks["edge"]["bilateral_exponent"] = 2 * 5 == 10
checks["edge"]["reflection"] = main_text.include?("Applying it to `t -> g(-t)` proves the left half")
checks["edge"]["range_all_nonnegative"] = main_text.include?("every `d>=0`")
checks["edge"]["complex_coefficients"] = cm.include?("c_j\\in\\mathbbC")
checks["edge"]["real_frequencies"] = cm.include?("\\mu_j\\in\\mathbbR")
checks["edge"]["collisions_merged"] = main_text.include?("repeated frequencies are merged")
checks["edge"]["no_spacing_assumption"] = main_text.include?("No frequency spacing or upper-frequency cutoff")

checks["plateau"]["sample_e_a"] = sample_e_a == Rational(639, 640)
checks["plateau"]["sample_delta_a"] = sample_delta_a == Rational(2, 213)
checks["plateau"]["branch_count"] = branches == 6 && main_text.include?("N<=2q")
checks["plateau"]["exterior_prefactor"] = exterior_numerator == Rational(1000, 19)
checks["plateau"]["interior_prefactor"] = interior_numerator == Rational(1000, 19)
checks["plateau"]["holder_prefactor"] = holder_at_half == Rational(2000, 19)
checks["plateau"]["squared_exponent"] = 2 * 5 == 10
checks["plateau"]["q_exponent"] = 10 * 2 == 20
checks["plateau"]["phi_definition"] = cm.include?("\\Phi_a^{\\rmloc}:=20\\sqrt2q\\sqrt{\\Delta_a}")
checks["plateau"]["full_observation"] = cm.include?("\\frac{1000}{19e_a}q^2e^{\\Phi_a^{\\rmloc}}") && cm.include?("\\frac{2000}{19}q^2e^{\\Phi_a^{\\rmloc}}h(s)^{2/3}")
checks["plateau"]["physical_bound"] = cm.include?("a^{2/3}R^{-1/3}q^7e^{\\Phi_a^{\\rmloc}}")
checks["plateau"]["normalized_bound"] = cm.include?("a^{2/3}q^7\\omega^{1/3}e^{\\Phi_a^{\\rmloc}}")

checks["asymptotic"]["mode_window"] = mode_window == Rational(5, 2)
checks["asymptotic"]["omega_input"] = c_gamma == Rational(8, 3969)
checks["asymptotic"]["omega_third_rate"] = omega_third_rate == Rational(-2, 11_907)
checks["asymptotic"]["normalized_rate"] = fraction_string(omega_third_rate) == "-2/11907"
checks["asymptotic"]["exponent_scale"] = Rational(1, 2) + 2 == Rational(5, 2)
checks["asymptotic"]["polynomial_scale"] = 7 * Rational(12, 5) < 2 * 12 # log q is subquadratic even for polynomial q
checks["asymptotic"]["exact_rate_text"] = cm.include?("=-\\frac2{11907}") && main_text.include?("=-2/11907")
checks["asymptotic"]["j46_text"] = cm.include?("O\\!\\left(\\frac{q(L)}{L^{5/2}}\\right)") && cm.include?("q=o(L^{5/2})")

checks["sources"]["zhang_versioned_abs"] = source_text.include?("https://arxiv.org/abs/2607.10501v1")
checks["sources"]["zhang_versioned_pdf"] = source_text.include?("https://arxiv.org/pdf/2607.10501v1")
checks["sources"]["erdelyi_journal"] = source_text.include?("https://www.mathnet.ru/eng/sm8670")
checks["sources"]["garcia_ross"] = source_text.include?("https://arxiv.org/abs/1312.5018")
checks["sources"]["kos_doi"] = source_text.include?("https://doi.org/10.1007/s10474-007-6176-5")
checks["sources"]["architecture_attribution"] = source_text.include?("Attribution for the Sections 2--4 architecture")
checks["sources"]["no_black_box"] = source_text.include?("No theorem from the preprint is assumed") && main_text.include?("not an unproved theorem used by J.2")
checks["sources"]["bounded_search"] = source_text.include?("The search was bounded") && source_text.include?("Search stopped")
checks["sources"]["no_priority_search_claim"] = source_text.include?("not evidence of novelty or priority") && source_text.include?("not an exhaustive historical or priority search")

checks["boundary"]["literature_label"] = main_text.include?("**LITERATURE:**")
checks["boundary"]["proved_locally"] = main_text.include?("**PROVED LOCALLY:**") && main_text.include?("**PROVED LOCALLY FROM ESTABLISHED LITERATURE**")
checks["boundary"]["finite_computation"] = main_text.include?("**FINITE COMPUTATION:**")
checks["boundary"]["open_label"] = main_text.include?("**OPEN:**")
checks["boundary"]["exact_shear_scope"] = main_text.include?("exact one-band constant shear") && cm.include?("u=(0,B,F(t,x_2))")
checks["boundary"]["arbitrary_field_open"] = main_text.include?("arbitrary-field") && main_text.include?("arbitrary nonlinear packets")
checks["boundary"]["regularity_open"] = main_text.include?("regularity")
checks["boundary"]["singularity_open"] = main_text.include?("singularity")
checks["boundary"]["no_simulation"] = main_text.include?("No simulation")
checks["boundary"]["no_figure"] = main_text.include?("No simulation or formal figure is needed")
checks["boundary"]["no_novelty"] = main_text.include?("No novelty")
checks["boundary"]["no_priority"] = main_text.include?("priority") && cs.include?("Nocitationcount")
checks["boundary"]["not_clay"] = main_text.include?("**NOT CLAY.**") && source_text.include?("**NOT CLAY.**") && primary_text.include?("**NOT CLAY.**")

python_required = %w[verdict freezeReady assertionsTotal exact bindings]
python_bindings = python_json.is_a?(Hash) && python_json["bindings"].is_a?(Hash) ? python_json["bindings"] : {}
python_binding_subset = FROZEN.all? do |relative, expected|
  row = python_bindings[relative]
  row.is_a?(Hash) && row["expectedSha256"] == expected &&
    row["observedSha256"] == bindings.fetch(relative).fetch("observedSha256") && row["pass"] == true
end
checks["python_cross"]["json_object"] = python_json.is_a?(Hash)
checks["python_cross"]["required_fields"] = python_required.all? { |key| python_json.key?(key) }
checks["python_cross"]["verdict"] = python_json["verdict"] == "PASS"
checks["python_cross"]["freeze_ready"] = python_json["freezeReady"] == true
checks["python_cross"]["assertions_positive"] = python_json["assertionsTotal"].is_a?(Integer) && python_json["assertionsTotal"].positive?
checks["python_cross"]["exact_object"] = python_json["exact"].is_a?(Hash) && !python_json["exact"].empty?
checks["python_cross"]["bindings_object"] = python_json["bindings"].is_a?(Hash)
checks["python_cross"]["frozen_binding_subset"] = python_binding_subset

unless checks.keys == GROUPS.keys && GROUPS.all? { |group, names| checks.fetch(group).keys == names }
  abort("R0.76J Ruby assertion inventory mismatch")
end

unless MUTATION.empty?
  unless NEGATIVE_MUTATIONS.include?(MUTATION)
    warn "unknown R076J_RUBY_MUTATION: #{MUTATION}"
    exit 2
  end
  GROUPS.each do |group, names|
    checks.fetch(group)[MUTATION] = false if names.include?(MUTATION)
  end
end

failures = checks.each_with_object([]) do |(group, rows), output|
  rows.each { |name, passed| output << "#{group}.#{name}" unless passed }
end
assertions = GROUPS.values.sum(&:length)

exact = {
  "laguerre" => {
    "samples" => laguerre_observed.transform_values { |value| fraction_string(value) },
    "sampleCount" => laguerre_grid.length,
    "minimumSampleBoundMargin" => format("%.12g", laguerre_bound_margins.min)
  },
  "tail" => {
    "cutoffMultiplier" => 25,
    "sampleN" => sample_n,
    "sampleAlpha" => fraction_string(sample_alpha),
    "sampleCutoff" => fraction_string(tail_cutoff),
    "exp5PartialK0Through6" => fraction_string(exp5_partial),
    "tailUpperFromPartial" => fraction_string(partial_tail_upper),
    "strictTailMarginLowerBound" => fraction_string(strict_tail_margin),
    "finiteRangeFactor" => "20/19"
  },
  "edge" => {
    "squaredPrefactor" => "250/19",
    "amplitudePrefactorSquared" => "250/19",
    "laguerreSquaredExponentSqrt2Coefficient" => 10,
    "amplitudeExponentSqrt2Coefficient" => 5
  },
  "plateau" => {
    "sampleEA" => fraction_string(sample_e_a),
    "sampleDeltaA" => fraction_string(sample_delta_a),
    "complexBranches" => branches,
    "exteriorNumerator" => "1000/19",
    "interiorNumerator" => "1000/19",
    "holderNumerator" => "2000/19",
    "phiSqrt2QCoefficient" => 20
  },
  "asymptotic" => {
    "modeWindowExponent" => fraction_string(mode_window),
    "cGamma" => fraction_string(c_gamma),
    "normalizedLogRate" => fraction_string(omega_third_rate)
  },
  "structure" => {
    "firstTag" => tags.first,
    "lastTag" => tags.last,
    "tagCount" => tags.length,
    "displayCount" => display_opens
  }
}

verdict = failures.empty? && freeze_ready ? "PASS" : "FAIL"
payload = {
  "schema" => "r076j-local-edge-extrapolation-independent-v1",
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
  "# R0.76J independent finite audit",
  "",
  "- Verdict: **#{verdict}**",
  "- Freeze-ready hash seal: **#{freeze_ready ? 'yes' : 'no'}**",
  "- Ruby assertions: #{assertions - failures.length}/#{assertions}",
  "- Python certificate fields and seven-file binding subset: #{checks.fetch('python_cross').values.all? ? 'PASS' : 'FAIL'}",
  "- J.1--J.46 equation inventory and reference closure: #{checks.fetch('integrity').values_at('tag_sequence', 'tag_count', 'reference_closure').all? ? 'PASS' : 'FAIL'}",
  "- Independent Laguerre series/recurrence sample cross-check: #{checks.fetch('laguerre').values_at('sample_table', 'series_recurrence_agree').all? ? 'PASS' : 'FAIL'}",
  "- Exact tail-margin lower bound: #{fraction_string(strict_tail_margin)}",
  "- Exact normalized logarithmic rate: #{fraction_string(omega_third_rate)}",
  "- Failures: #{failures.empty? ? 'none' : failures.join(', ')}",
  "",
  "## Finite-audit boundary",
  "",
  "This Ruby verifier independently recomputes the finite Laguerre samples,",
  "20/19 tail ledger, 250/19--2000/19 constants, 5sqrt(2)--20sqrt(2)",
  "exponents, and q=o(L^(5/2)) rate.  It does not prove Plancherel, the",
  "continuum Volterra argument, the imported R0.76I literature inputs, or a",
  "Navier--Stokes regularity/singularity claim. **NOT CLAY.**",
  ""
]
File.write(REPORT, report.join("\n"), encoding: "UTF-8")

puts JSON.generate(
  "suite" => "r076j-local-edge-extrapolation-independent",
  "status" => verdict,
  "assertions" => assertions,
  "failures" => failures.length
)
exit(verdict == "PASS" ? 0 : 1)
