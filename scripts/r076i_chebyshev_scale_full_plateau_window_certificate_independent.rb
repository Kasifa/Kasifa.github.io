#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed finite verifier for R0.76I.
#
# Every research/input binding is sealed to a 64-character SHA-256 digest.
# Placeholder mode remains supported for future unsealed rebuilds and can
# produce SCAFFOLD_PASS only. Generated certificate/report/audit outputs are
# deliberately excluded from this binding set to avoid a hash cycle.

require "digest"
require "json"

ROOT = File.expand_path("..", __dir__)
STEM = "r076i_chebyshev_scale_full_plateau_window"
MAIN = File.join(ROOT, "research", "#{STEM}.md")
SOURCE = File.join(ROOT, "research", "r076i_report-source.md")
FIXTURES = File.join(ROOT, "scripts", "#{STEM}_fixtures.json")
EXPECTED = File.join(ROOT, "scripts", "#{STEM}_expected.json")
PYTHON_JSON = ENV.fetch("R076I_JSON", File.join(ROOT, "research", "#{STEM}_certificate.json"))
REPORT = ENV.fetch("R076I_RUBY_REPORT", File.join(ROOT, "research", "#{STEM}_independent_audit.md"))
MUTATION = ENV.fetch("R076I_RUBY_MUTATION", "")

PLACEHOLDER = /\APENDING_R076I_[A-Z0-9_]+_SHA256\z/
SHA256 = /\A[0-9a-f]{64}\z/

FROZEN = {
  "research/#{STEM}.md" => "6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce",
  "research/r076i_report-source.md" => "0ee0fbd75f9691e2ac898a57921f8a0574ba9af9ea652f85d0199856d7e3d423",
  "research/#{STEM}_primary_audit.md" => "65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe",
  "research/r076e_linear_modal_entropy_window.md" => "1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4",
  "research/r076h_full_plateau_absorption_for_shifted_packet.md" => "11490112a1893400a1099dd9f45b906ce78d7dab1ebcf549eaa7870241dc0ef4",
  "scripts/#{STEM}_fixtures.json" => "f1475b2549490c3639c15a4fc103e704d0de98a518f50249b732a8e0a135d776",
  "scripts/#{STEM}_expected.json" => "26485db072bf886fae88f0737546d7090f77b9b23e55c356bf8affe6aeba1da5"
}.freeze

GROUPS = {
  "bindings" => %w[
    main_hash source_hash primary_audit_hash r076e_dependency_hash
    r076h_dependency_hash fixture_hash expected_hash hash_specs_well_formed
    freeze_state_consistent
  ],
  "inputs" => %w[
    fixture_schema expected_schema fixture_keys expected_keys fixture_utf8
    expected_utf8 p_value rho_value gamma_value sample_values source_inventory
    dependency_inventory
  ],
  "integrity" => %w[
    main_utf8 source_utf8 no_controls no_cr no_trailing tag_sequence tag_count
    display_balance display_count reference_closure
  ],
  "geometry" => %w[
    delta_order e_rule e_value e_length right_endpoint delta_rule delta_value
    rescaled_endpoint endpoint_identity physical_gap endpoint_regime
    main_geometry_fragments
  ],
  "zhang" => %w[
    afr_value complex_coefficients real_frequencies duplicates_merged
    unnormalized_norm branch_count amplitude_exponent squared_exponent
    q_squared_exponent phi_square scaled_prefactor i17_constant i17_range
    i18_bilateral i19_full_interval
  ],
  "derivative" => %w[
    markov_coefficient two_to_fifth leading_coefficient sample_markov_leading
    frequency_square_coefficient sample_frequency_square observation_power
    q_seven q_three_alpha_two ledger_sum high_carrier_power i20_fragment
    i21_fragment i33_fragment
  ],
  "terminal" => %w[
    branch_upper endpoint_factor cube_rule two_thirds_rule sample_cube
    sample_two_thirds i23_fragment i24_fragment
  ],
  "energy" => %w[
    row_count row_names row_signs row_coefficients row_a_powers terminal_row
    cutoff_row curvature_row gradient_row four_line_identity
    complete_real_boundary
  ],
  "physical" => %w[
    a_power r_power q_power physical_bound normalized_bound mode_window
    growing_example window_margin gamma_rate normalized_rate delta_asymptotic
    phi_asymptotic physical_conversion
  ],
  "source" => %w[
    zhang_abs zhang_pdf erdelyi_abs erdelyi_journal erdelyi_pdf kos_journal
    zhang_metadata erdelyi_metadata kos_metadata lower_witness_boundary
    local_dependencies_named no_priority_claim
  ],
  "boundary" => %w[
    conditional_literature preprint_boundary full_class_sharpness
    real_dyadic_sharpness_open arbitrary_packets_open version_m_open
    regularity_open singularity_open no_figure no_simulation not_clay
    no_clay_claim exact_shear_scope
  ]
}.freeze
NEGATIVE_MUTATIONS = GROUPS.values.flatten.freeze

abort("duplicate mutation name in R0.76I Ruby suite") unless
  NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

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

def digest_or_nil(relative)
  path = File.join(ROOT, relative)
  File.file?(path) ? Digest::SHA256.file(path).hexdigest : nil
end

def binding_row(relative, expected)
  observed = digest_or_nil(relative)
  locked = SHA256.match?(expected)
  placeholder = PLACEHOLDER.match?(expected)
  valid_spec = locked || placeholder
  passed = valid_spec && (!locked || observed == expected)
  status = if locked
             passed ? "locked_match" : "locked_mismatch"
           else
             placeholder ? "placeholder_unlocked" : "invalid_hash_spec"
           end
  {
    "expectedSha256" => expected,
    "observedSha256" => observed || "MISSING",
    "exists" => File.file?(File.join(ROOT, relative)),
    "locked" => locked,
    "placeholder" => placeholder,
    "status" => status,
    "pass" => passed
  }
end

main_raw = File.binread(MAIN)
source_raw = File.binread(SOURCE)
fixture_raw = File.binread(FIXTURES)
expected_raw = File.binread(EXPECTED)
main_text = main_raw.dup.force_encoding("UTF-8")
source_text = source_raw.dup.force_encoding("UTF-8")
cm = compact(main_text)
fixture = JSON.parse(fixture_raw)
expected = JSON.parse(expected_raw)
python_json = JSON.parse(File.read(PYTHON_JSON, encoding: "UTF-8"))

bindings = FROZEN.keys.sort.to_h do |relative|
  [relative, binding_row(relative, FROZEN.fetch(relative))]
end
placeholders = bindings.select { |_relative, row| row.fetch("placeholder") }.keys
freeze_ready = bindings.values.all? { |row| row.fetch("locked") && row.fetch("pass") }
bound = ->(relative) { bindings.fetch(relative).fetch("pass") }

frozen = fixture.fetch("frozen")
sample = fixture.fetch("sample")
zhang = fixture.fetch("zhang")
geometry = fixture.fetch("geometry")
derivative = fixture.fetch("derivative")
terminal = fixture.fetch("terminal")
energy = fixture.fetch("energyIdentity")
physical = fixture.fetch("physical")
sources = fixture.fetch("sources")
dependencies = fixture.fetch("dependencies")
boundary = fixture.fetch("boundary")

a = sample.fetch("a")
delta0 = Rational(sample.fetch("delta0"))
delta = Rational(sample.fetch("delta"))
q_modes = sample.fetch("q")
alpha = Rational(sample.fetch("alpha"))
branches = 2 * q_modes
e_a = Rational(1) - delta0 / a
e_length = 2 * e_a
right_endpoint = Rational(1) + delta / a
delta_a = (delta + delta0) / (a - delta0)
rescaled_endpoint = right_endpoint / e_a
physical_gap = right_endpoint - e_a

afr = zhang.fetch("AFr")
amplitude_sqrt2_coefficient = 3 * branches
squared_sqrt2_coefficient = 6 * branches
q_squared_sqrt2_coefficient = 12 * q_modes
phi_squared = Rational(q_squared_sqrt2_coefficient**2 * 2) * delta_a
scaled_squared_prefactor = Rational(18 * afr * q_modes * q_modes) / e_a

two_to_fifth = 2**5
markov_leading_coefficient = derivative.fetch("markovCoefficient") * two_to_fifth
sample_markov_leading = derivative.fetch("markovCoefficient") * branches**5
sample_frequency_square = Rational(derivative.fetch("frequencySquareCoefficient")) * q_modes * alpha**2
q_seven = q_modes**7
q_three_alpha_two = Rational(q_modes**3) * alpha**2
ledger_sum = Rational(q_seven) + q_three_alpha_two
high_carrier_intermediate = Rational(3) + Rational(8, 3)

endpoint_factor = 4 * q_modes
cubed_coefficient = endpoint_factor**3
two_thirds_coefficient = 16 * q_modes**2

rows = energy.fetch("rows")
row_names = rows.map { |row| row.fetch("name") }
row_signs = rows.map { |row| row.fetch("sign") }
row_coefficients = rows.map { |row| row.fetch("coefficient") }
row_a_powers = rows.map { |row| row.fetch("aPower") }

mode_window = Rational(physical.fetch("modeWindowExponent"))
example_window = Rational(physical.fetch("growingExampleExponent"))
window_margin = mode_window - example_window
omega_third_rate = -Rational(frozen.fetch("cGamma")) / 12

tags = main_text.scan(/\\tag\{I\.(\d+)\}/).flatten.map(&:to_i)
refs = main_text.scan(/(?<![A-Za-z0-9_.])I\.(\d+)/).flatten.map(&:to_i)
display_opens = main_text.scan(/^\\\[$/).length
display_closes = main_text.scan(/^\\\]$/).length

fixture_keys = %w[
  schema freeze frozen sample zhang geometry derivative terminal energyIdentity
  physical sources dependencies boundary
]
expected_keys = %w[
  schema sample geometry zhang derivative terminal energyIdentity physical
  structure claims
]

checks = GROUPS.to_h { |group, names| [group, names.to_h { |name| [name, false] }] }

checks["bindings"]["main_hash"] = bound.call("research/#{STEM}.md")
checks["bindings"]["source_hash"] = bound.call("research/r076i_report-source.md")
checks["bindings"]["primary_audit_hash"] = bound.call("research/#{STEM}_primary_audit.md")
checks["bindings"]["r076e_dependency_hash"] = bound.call("research/r076e_linear_modal_entropy_window.md")
checks["bindings"]["r076h_dependency_hash"] = bound.call("research/r076h_full_plateau_absorption_for_shifted_packet.md")
checks["bindings"]["fixture_hash"] = bound.call("scripts/#{STEM}_fixtures.json")
checks["bindings"]["expected_hash"] = bound.call("scripts/#{STEM}_expected.json")
checks["bindings"]["hash_specs_well_formed"] = bindings.values.all? { |row| row.fetch("locked") || row.fetch("placeholder") }
checks["bindings"]["freeze_state_consistent"] =
  (!placeholders.empty? && fixture.dig("freeze", "state") == "PENDING_PRIMARY_AUDIT_HASH_SEAL") ||
  (placeholders.empty? && fixture.dig("freeze", "state") == "HASH_SEALED")

checks["inputs"]["fixture_schema"] = fixture.fetch("schema") == "r076i-chebyshev-scale-full-plateau-window-fixtures-v1"
checks["inputs"]["expected_schema"] = expected.fetch("schema") == "r076i-chebyshev-scale-full-plateau-window-expected-v1"
checks["inputs"]["fixture_keys"] = fixture.keys.sort == fixture_keys.sort
checks["inputs"]["expected_keys"] = expected.keys.sort == expected_keys.sort
checks["inputs"]["fixture_utf8"] = clean_bytes(fixture_raw)
checks["inputs"]["expected_utf8"] = clean_bytes(expected_raw)
checks["inputs"]["p_value"] = Rational(frozen.fetch("p")) == Rational(32, 63)
checks["inputs"]["rho_value"] = Rational(frozen.fetch("rho")) == Rational(9, 10_000)
checks["inputs"]["gamma_value"] = Rational(frozen.fetch("cGamma")) == Rational(8, 3969)
checks["inputs"]["sample_values"] = [a, delta0, delta, q_modes, alpha] == [64, Rational(1, 10), Rational(1, 2), 3, Rational(5, 2)]
checks["inputs"]["source_inventory"] = sources.keys.sort == %w[erdelyiAbs erdelyiJournal erdelyiPdf kosJournal zhangAbs zhangPdf].sort
checks["inputs"]["dependency_inventory"] = dependencies == {
  "research/r076e_linear_modal_entropy_window.md" => FROZEN.fetch("research/r076e_linear_modal_entropy_window.md"),
  "research/r076h_full_plateau_absorption_for_shifted_packet.md" => FROZEN.fetch("research/r076h_full_plateau_absorption_for_shifted_packet.md")
}

checks["integrity"]["main_utf8"] = clean_bytes(main_raw)
checks["integrity"]["source_utf8"] = clean_bytes(source_raw)
checks["integrity"]["no_controls"] = [main_raw, source_raw, fixture_raw, expected_raw].all? { |raw| clean_bytes(raw) }
checks["integrity"]["no_cr"] = [main_raw, source_raw, fixture_raw, expected_raw].none? { |raw| raw.include?("\r") }
checks["integrity"]["no_trailing"] = [main_text, source_text].all? do |text|
  text.lines.none? { |line| line.chomp.end_with?(" ", "\t") }
end
checks["integrity"]["tag_sequence"] = tags == (1..38).to_a
checks["integrity"]["tag_count"] = tags.length == expected.dig("structure", "tagCount") && tags.length == 38
checks["integrity"]["display_balance"] = display_opens == display_closes
checks["integrity"]["display_count"] = display_opens == expected.dig("structure", "displayCount") && display_opens == 42
checks["integrity"]["reference_closure"] = (refs.uniq - tags.uniq).empty?

checks["geometry"]["delta_order"] = Rational(0) < delta0 && delta0 < delta
checks["geometry"]["e_rule"] = geometry.fetch("eRule") == "1-delta0/a"
checks["geometry"]["e_value"] = e_a == Rational(expected.dig("geometry", "eA"))
checks["geometry"]["e_length"] = e_length == Rational(expected.dig("geometry", "eALength"))
checks["geometry"]["right_endpoint"] = right_endpoint == Rational(expected.dig("geometry", "rightEndpoint"))
checks["geometry"]["delta_rule"] = geometry.fetch("deltaRule") == "(delta+delta0)/(a-delta0)"
checks["geometry"]["delta_value"] = delta_a == Rational(expected.dig("geometry", "deltaA"))
checks["geometry"]["rescaled_endpoint"] = rescaled_endpoint == Rational(expected.dig("geometry", "rescaledRightEndpoint"))
checks["geometry"]["endpoint_identity"] = rescaled_endpoint == 1 + delta_a
checks["geometry"]["physical_gap"] = physical_gap == Rational(expected.dig("geometry", "physicalExteriorWidthOneSide")) && physical_gap == e_a * delta_a
checks["geometry"]["endpoint_regime"] = a >= delta + 2 * delta0 && delta_a <= 1 && expected.dig("geometry", "endpointRegime")
checks["geometry"]["main_geometry_fragments"] = [
  "e_a:=1-\\frac{\\delta_0}{a}", "E_a=[-e_a,e_a]",
  "I_a=\\left[-1-\\frac\\deltaa,1+\\frac\\deltaa\\right]",
  "\\Delta_a:=\\frac{\\delta+\\delta_0}{a-\\delta_0}"
].all? { |fragment| cm.include?(fragment) }

checks["zhang"]["afr_value"] = afr == expected.dig("zhang", "AFr") && afr == 8191
checks["zhang"]["complex_coefficients"] = zhang.fetch("coefficientField") == "complex" && cm.include?("c_r\\in\\mathbbC")
checks["zhang"]["real_frequencies"] = zhang.fetch("frequencyField") == "real" && cm.include?("\\mu_r\\in\\mathbbR")
checks["zhang"]["duplicates_merged"] = zhang.fetch("duplicateFrequencyRule") == "merge-before-counting" && cm.include?("duplicatebranchesareremoved")
checks["zhang"]["unnormalized_norm"] = zhang.fetch("normRule") == "unnormalized-L2-minus1-plus1" && cm.include?("\\|g\\|_{L^2[-1,1]}")
checks["zhang"]["branch_count"] = branches == expected.dig("sample", "complexBranches") && branches == 6 && cm.include?("N=2q")
checks["zhang"]["amplitude_exponent"] = amplitude_sqrt2_coefficient == expected.dig("zhang", "amplitudeExponentSqrt2Coefficient") && amplitude_sqrt2_coefficient == 18
checks["zhang"]["squared_exponent"] = squared_sqrt2_coefficient == expected.dig("zhang", "squaredExponentSqrt2Coefficient") && squared_sqrt2_coefficient == 36
checks["zhang"]["q_squared_exponent"] = q_squared_sqrt2_coefficient == expected.dig("zhang", "qSquaredExponentSqrt2Coefficient") && q_squared_sqrt2_coefficient == 36
checks["zhang"]["phi_square"] = phi_squared == Rational(expected.dig("zhang", "phiSquared"))
checks["zhang"]["scaled_prefactor"] = scaled_squared_prefactor == Rational(expected.dig("zhang", "scaledSquaredPrefactor"))
checks["zhang"]["i17_constant"] = cm.include?("\\sqrt{\\frac{9A_{\\rmfr}}2}\\,N") && cm.include?("A_{\\rmfr}\\le8191")
checks["zhang"]["i17_range"] = main_text.include?("0<=d<=1") && cm.include?("e^{3\\sqrt2N\\sqrtd}")
checks["zhang"]["i18_bilateral"] = cm.include?("\\frac{18A_{\\rmfr}}{e_a}q^2") && cm.include?("e^{12\\sqrt2q\\sqrt{\\Delta_a}}") && cm.include?("reflectionontheleftexterior")
checks["zhang"]["i19_full_interval"] = cm.include?("\\|G(s)\\|_{L^\\infty(I_a)}^2") && cm.include?("\\Phi_a:=12\\sqrt2q\\sqrt{\\Delta_a}")

checks["derivative"]["markov_coefficient"] = derivative.fetch("markovCoefficient") == 108
checks["derivative"]["two_to_fifth"] = two_to_fifth == expected.dig("derivative", "twoToFifth") && two_to_fifth == 32
checks["derivative"]["leading_coefficient"] = markov_leading_coefficient == expected.dig("derivative", "markovLeadingCoefficient") && markov_leading_coefficient == 3456
checks["derivative"]["sample_markov_leading"] = sample_markov_leading == expected.dig("derivative", "sampleMarkovLeading") && sample_markov_leading == 839_808
checks["derivative"]["frequency_square_coefficient"] = derivative.fetch("frequencySquareCoefficient") == 8
checks["derivative"]["sample_frequency_square"] = sample_frequency_square == Rational(expected.dig("derivative", "sampleFrequencySquareUpper")) && sample_frequency_square == 150
checks["derivative"]["observation_power"] = derivative.fetch("observationQPower") == 2
checks["derivative"]["q_seven"] = q_seven == expected.dig("derivative", "qSeven") && q_seven == 2187
checks["derivative"]["q_three_alpha_two"] = q_three_alpha_two == Rational(expected.dig("derivative", "qThreeAlphaTwo"))
checks["derivative"]["ledger_sum"] = ledger_sum == Rational(expected.dig("derivative", "ledgerSum"))
checks["derivative"]["high_carrier_power"] = high_carrier_intermediate == Rational(expected.dig("derivative", "highCarrierIntermediatePower")) && high_carrier_intermediate < Rational(expected.dig("derivative", "highCarrierDominatingPower"))
checks["derivative"]["i20_fragment"] = cm.include?("108N^5+\\sum_{r=1}^N\\mu_r^2")
checks["derivative"]["i21_fragment"] = cm.include?("q^7+q^3\\alpha^2") && cm.include?("\\sum_{j=1}^q\\bigl(\\kappa_j^2+(-\\kappa_j)^2\\bigr)\\le8q\\alpha^2")
checks["derivative"]["i33_fragment"] = cm.include?("q^3[q\\log(q+1)]^{4/3}") && cm.include?("\\leCq^7H^{2/3}")

checks["terminal"]["branch_upper"] = terminal.fetch("branchUpperRule") == "2q" && cm.include?("N_z\\le2q")
checks["terminal"]["endpoint_factor"] = endpoint_factor == expected.dig("terminal", "endpointFactor") && endpoint_factor == 12
checks["terminal"]["cube_rule"] = terminal.fetch("cubedRule") == "64q3" && 4**3 == 64
checks["terminal"]["two_thirds_rule"] = terminal.fetch("twoThirdsRule") == "16q2" && 16**3 == 64**2
checks["terminal"]["sample_cube"] = cubed_coefficient == expected.dig("terminal", "cubedCoefficient") && cubed_coefficient == 1728
checks["terminal"]["sample_two_thirds"] = two_thirds_coefficient == expected.dig("terminal", "twoThirdsCoefficient") && two_thirds_coefficient == 144
checks["terminal"]["i23_fragment"] = cm.include?("|G(4,z)|\\le2N_z\\left(\\int_3^4|G(s,z)|^2ds\\right)^{1/2}")
checks["terminal"]["i24_fragment"] = cm.include?("h(4)\\le64q^3\\int_3^4h(s)ds\\le64q^3H") && cm.include?("h(4)^{2/3}\\le16q^2H^{2/3}")

checks["energy"]["row_count"] = rows.length == energy.fetch("rowCount") && rows.length == 4
checks["energy"]["row_names"] = row_names == expected.dig("energyIdentity", "rowNames")
checks["energy"]["row_signs"] = row_signs == expected.dig("energyIdentity", "signs")
checks["energy"]["row_coefficients"] = row_coefficients == expected.dig("energyIdentity", "coefficients")
checks["energy"]["row_a_powers"] = row_a_powers == expected.dig("energyIdentity", "aPowers")
checks["energy"]["terminal_row"] = cm.include?("=\\zeta(4)\\mathcalE(4)")
checks["energy"]["cutoff_row"] = cm.include?("-\\int_0^4\\zeta'\\mathcalE\\,ds")
checks["energy"]["curvature_row"] = cm.include?("-a^{-2}\\int_0^4\\zeta\\int\\Xi_a''G^2")
checks["energy"]["gradient_row"] = cm.include?("+2a^{-2}\\int_0^4\\zeta\\int\\Xi_a|G_z|^2")
checks["energy"]["four_line_identity"] = %w[terminal cutoff curvature gradient].all? { |name| row_names.include?(name) } && main_text.include?("I.28--I.34")
checks["energy"]["complete_real_boundary"] = cm.include?("completerealsquare") && cm.include?("densityprojection") && cm.include?("standalonecarrierintegrationbyparts")

checks["physical"]["a_power"] = Rational(physical.fetch("aPower")) == Rational(expected.dig("physical", "aPower")) && Rational(physical.fetch("aPower")) == Rational(2, 3)
checks["physical"]["r_power"] = Rational(physical.fetch("rPower")) == Rational(expected.dig("physical", "rPower")) && Rational(physical.fetch("rPower")) == -Rational(1, 3)
checks["physical"]["q_power"] = physical.fetch("polynomialQPower") == expected.dig("physical", "qPower") && physical.fetch("polynomialQPower") == 7
checks["physical"]["physical_bound"] = cm.include?("a^{2/3}R^{-1/3}q^7")
checks["physical"]["normalized_bound"] = cm.include?("a^{2/3}q^7\\omega^{1/3}")
checks["physical"]["mode_window"] = mode_window == Rational(expected.dig("physical", "modeWindowExponent")) && mode_window == Rational(5, 2) && cm.include?("q(L)=o(L^{5/2})")
checks["physical"]["growing_example"] = example_window == Rational(expected.dig("physical", "growingExampleExponent")) && example_window == Rational(12, 5)
checks["physical"]["window_margin"] = window_margin == Rational(expected.dig("physical", "windowMarginExponent")) && window_margin == Rational(1, 10)
checks["physical"]["gamma_rate"] = omega_third_rate == Rational(frozen.fetch("omegaThirdLogRate")) && omega_third_rate == -Rational(2, 11_907)
checks["physical"]["normalized_rate"] = Rational(physical.fetch("normalizedLogRate")) == Rational(expected.dig("physical", "normalizedLogRate")) && Rational(physical.fetch("normalizedLogRate")) == -Rational(2, 11_907) && cm.include?("=-\\frac2{11907}")
checks["physical"]["delta_asymptotic"] = cm.include?("\\Delta_a=\\frac{\\delta+\\delta_0}{pL-\\delta_0}=O(L^{-1})")
checks["physical"]["phi_asymptotic"] = cm.include?("\\frac{q(L)\\sqrt{\\Delta_a}}{L^2}=O\\!\\left(\\frac{q(L)}{L^{5/2}}\\right)")
checks["physical"]["physical_conversion"] = cm.include?("\\mathcalT_{\\boldsymboln,R}=\\frac{a^2R^3}{2}v\\int_0^4\\zeta\\intW_aG^2")

checks["source"]["zhang_abs"] = sources.fetch("zhangAbs") == "https://arxiv.org/abs/2607.10501v1" && source_text.include?("https://arxiv.org/abs/2607.10501") && source_text.include?("arXiv:2607.10501v1")
checks["source"]["zhang_pdf"] = sources.fetch("zhangPdf") == "https://arxiv.org/pdf/2607.10501v1" && source_text.include?("https://arxiv.org/pdf/2607.10501") && source_text.include?("arXiv:2607.10501v1")
checks["source"]["erdelyi_abs"] = source_text.include?(sources.fetch("erdelyiAbs"))
checks["source"]["erdelyi_journal"] = source_text.include?(sources.fetch("erdelyiJournal"))
checks["source"]["erdelyi_pdf"] = source_text.include?(sources.fetch("erdelyiPdf"))
checks["source"]["kos_journal"] = source_text.include?(sources.fetch("kosJournal"))
checks["source"]["zhang_metadata"] = ["Ruizhe Zhang", "arXiv:2607.10501v1", "2026-07-11", "34 pages"].all? { |fragment| source_text.include?(fragment) }
checks["source"]["erdelyi_metadata"] = ["Theorem 2.20", "108 n^5", "equation (1.2)"].all? { |fragment| source_text.include?(fragment) }
checks["source"]["kos_metadata"] = source_text.include?("Two Turán type inequalities") && source_text.include?("10.1007/s10474-007-6176-5")
checks["source"]["lower_witness_boundary"] = ["confluent sequence", "complex sums", "larger `T_k` class", "**OPEN**"].all? { |fragment| source_text.include?(fragment) }
checks["source"]["local_dependencies_named"] = main_text.include?("R0.76E") && main_text.include?("R0.76H")
checks["source"]["no_priority_claim"] = source_text.include?("not evidence of novelty or priority") && source_text.include?("no priority claim is made")

checks["boundary"]["conditional_literature"] = boundary.fetch("conditionalLiterature") && expected.dig("claims", "conditionalLiterature") && main_text.include?("**CONDITIONAL-LITERATURE**")
checks["boundary"]["preprint_boundary"] = !boundary.fetch("zhangPeerReviewed") && expected.dig("claims", "preprintBoundary") && source_text.include?("UNREFEREED PREPRINT")
checks["boundary"]["full_class_sharpness"] = boundary.fetch("fullClassSharpnessOnly") && main_text.include?("full class `T_N`")
checks["boundary"]["real_dyadic_sharpness_open"] = !boundary.fetch("realDyadicSharpness") && expected.dig("claims", "realDyadicSharpnessOpen") && main_text.include?("matching lower bound within I.2")
checks["boundary"]["arbitrary_packets_open"] = !boundary.fetch("arbitraryPacketGeneralization") && expected.dig("claims", "arbitraryPacketsOpen") && main_text.include?("arbitrary nonlinear packets")
checks["boundary"]["version_m_open"] = !boundary.fetch("versionMExtraction") && expected.dig("claims", "versionMOpen") && main_text.include?("complete Version-M extraction")
checks["boundary"]["regularity_open"] = !boundary.fetch("regularityClaimed") && expected.dig("claims", "regularityOpen") && main_text.include?("regularity")
checks["boundary"]["singularity_open"] = !boundary.fetch("singularityClaimed") && expected.dig("claims", "singularityOpen") && main_text.include?("singularity")
checks["boundary"]["no_figure"] = !boundary.fetch("formalFigureRequired") && main_text.include?("No simulation or formal scientific figure is claimed")
checks["boundary"]["no_simulation"] = !boundary.fetch("simulationClaimed")
checks["boundary"]["not_clay"] = !boundary.fetch("clayClaimed") && expected.dig("claims", "notClay") && main_text.include?("**NOT CLAY.**")
checks["boundary"]["no_clay_claim"] = cm.include?("Nonovelty,priority,orClayimplicationisclaimed")
checks["boundary"]["exact_shear_scope"] = main_text.include?("exact real constant shears in one dyadic band") && cm.include?("u=(0,B,F(t,x_2))")

unless checks.keys == GROUPS.keys && GROUPS.all? { |group, names| checks.fetch(group).keys == names }
  abort("R0.76I Ruby assertion inventory mismatch")
end

unless MUTATION.empty?
  unless NEGATIVE_MUTATIONS.include?(MUTATION)
    warn "unknown R076I_RUBY_MUTATION: #{MUTATION}"
    exit 2
  end
  GROUPS.each do |group, names|
    checks.fetch(group)[MUTATION] = false if names.include?(MUTATION)
  end
end

failures = checks.each_with_object([]) do |(group, rows_in_group), output|
  rows_in_group.each do |name, passed|
    output << "#{group}.#{name}" unless passed
  end
end
assertions = GROUPS.values.sum(&:length)

exact = {
  "sample" => {
    "a" => a, "delta0" => fraction_string(delta0), "delta" => fraction_string(delta),
    "q" => q_modes, "alpha" => fraction_string(alpha), "complexBranches" => branches
  },
  "geometry" => {
    "eA" => fraction_string(e_a), "eALength" => fraction_string(e_length),
    "rightEndpoint" => fraction_string(right_endpoint),
    "rescaledRightEndpoint" => fraction_string(rescaled_endpoint),
    "deltaA" => fraction_string(delta_a),
    "physicalExteriorWidthOneSide" => fraction_string(physical_gap)
  },
  "zhang" => {
    "AFr" => afr,
    "amplitudeExponentSqrt2Coefficient" => amplitude_sqrt2_coefficient,
    "squaredExponentSqrt2Coefficient" => squared_sqrt2_coefficient,
    "qSquaredExponentSqrt2Coefficient" => q_squared_sqrt2_coefficient,
    "phiSquared" => fraction_string(phi_squared),
    "scaledSquaredPrefactor" => fraction_string(scaled_squared_prefactor)
  },
  "derivative" => {
    "markovLeadingCoefficient" => markov_leading_coefficient,
    "sampleMarkovLeading" => sample_markov_leading,
    "sampleFrequencySquareUpper" => fraction_string(sample_frequency_square),
    "qSeven" => q_seven, "qThreeAlphaTwo" => fraction_string(q_three_alpha_two),
    "ledgerSum" => fraction_string(ledger_sum),
    "highCarrierIntermediatePower" => fraction_string(high_carrier_intermediate)
  },
  "terminal" => {
    "endpointFactor" => endpoint_factor,
    "cubedCoefficient" => cubed_coefficient,
    "twoThirdsCoefficient" => two_thirds_coefficient
  },
  "energyIdentity" => {
    "rowNames" => row_names, "signs" => row_signs,
    "coefficients" => row_coefficients, "aPowers" => row_a_powers
  },
  "physical" => {
    "aPower" => fraction_string(Rational(physical.fetch("aPower"))),
    "rPower" => fraction_string(Rational(physical.fetch("rPower"))),
    "qPower" => physical.fetch("polynomialQPower"),
    "modeWindowExponent" => fraction_string(mode_window),
    "growingExampleExponent" => fraction_string(example_window),
    "windowMarginExponent" => fraction_string(window_margin),
    "normalizedLogRate" => fraction_string(omega_third_rate)
  },
  "structure" => {
    "firstTag" => tags.first, "lastTag" => tags.last,
    "tagCount" => tags.length, "displayCount" => display_opens
  }
}

exact_match = python_json.fetch("exact") == exact
mutation_match = python_json.fetch("negativeMutations") == NEGATIVE_MUTATIONS
bindings_match = python_json.fetch("bindings") == bindings
python_state_match = if freeze_ready
                       python_json.fetch("freezeReady") && python_json.fetch("verdict") == "PASS"
                     else
                       !python_json.fetch("freezeReady") && python_json.fetch("verdict") == "SCAFFOLD_PASS"
                     end

failures << "cross.python_exact" unless exact_match
failures << "cross.mutation_inventory" unless mutation_match
failures << "cross.bindings" unless bindings_match
failures << "cross.freeze_state" unless python_state_match
verdict = if failures.empty?
            freeze_ready ? "PASS" : "SCAFFOLD_PASS"
          else
            "FAIL"
          end

report = [
  "# R0.76I independent finite audit",
  "",
  "- Verdict: **#{verdict}**",
  "- Freeze-ready hash seal: **#{freeze_ready ? 'yes' : 'no'}**",
  "- Ruby assertions: #{assertions - failures.count { |value| !value.start_with?('cross.') }}/#{assertions}",
  "- Pending hash placeholders: #{placeholders.length}",
  "- Python/Ruby exact section identical: #{exact_match ? 'PASS' : 'FAIL'}",
  "- Python/Ruby mutation inventory identical: #{mutation_match ? 'PASS' : 'FAIL'}",
  "- Python/Ruby bindings identical: #{bindings_match ? 'PASS' : 'FAIL'}",
  "- Python/Ruby freeze state compatible: #{python_state_match ? 'PASS' : 'FAIL'}",
  "- Failures: #{failures.empty? ? 'none' : failures}",
  "",
  "This verifier independently recomputes the exact rational ledger.  A",
  "SCAFFOLD_PASS is not a frozen certificate.  Imported theorems and continuum",
  "arguments remain outside the finite audit. **NOT CLAY.**",
  ""
]
File.write(REPORT, report.join("\n"), encoding: "UTF-8")
exit(failures.empty? ? 0 : 1)
