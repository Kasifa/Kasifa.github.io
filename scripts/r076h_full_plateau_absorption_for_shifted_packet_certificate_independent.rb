#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent fail-closed finite audit for R0.76H.

require "digest"
require "json"

root = File.expand_path("..", __dir__)
stem = "r076h_full_plateau_absorption_for_shifted_packet"
main_path = File.join(root, "research", "#{stem}.md")
primary_path = File.join(root, "research", "#{stem}_primary_audit.md")
source_path = File.join(root, "research", "r076h_report-source.md")
fixture_path = File.join(root, "scripts", "#{stem}_fixtures.json")
expected_path = File.join(root, "scripts", "#{stem}_expected.json")
python_json_path = ENV.fetch("R076H_JSON", File.join(root, "research", "#{stem}_certificate.json"))
report_path = ENV.fetch("R076H_RUBY_REPORT", File.join(root, "research", "#{stem}_independent_audit.md"))
mutation = ENV.fetch("R076H_RUBY_MUTATION", "")

frozen_hashes = {
  "research/#{stem}.md" => "11490112a1893400a1099dd9f45b906ce78d7dab1ebcf549eaa7870241dc0ef4",
  "research/#{stem}_primary_audit.md" => "91e1f31f3adf19a9f352a8cd6defc8988971e51f0905e4a634f949223992c58d",
  "research/r076h_report-source.md" => "3e706ae12caace1118f941f92c85bc0a1a11ed4a6e158acf7258918a67616d87",
  "research/r076g_complete_clock_central_fibre_flux_lower_bound.md" => "20f32790b53f2b0f5cb39b7071bd2cda96ddb4e15f75211e1682f4ba37dd0bb2",
  "research/r075p_buffered_collar_entrance_concentration.md" => "8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6",
  "research/r075r_outer_cap_spectral_concentration_obstruction.md" => "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
  "research/r076e_linear_modal_entropy_window.md" => "1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4",
  "scripts/#{stem}_fixtures.json" => "035ff9b04f61c11744668c51e6fd8ef1e35da93de85fab2bd9b971acca79747d",
  "scripts/#{stem}_expected.json" => "f80cc1d8b6673a6f18069d6756f605de821ac661561d11295a40c468532e083b",
}

groups = {
  "bindings" => %w[
    main_hash primary_hash source_hash packet_dependency_hash
    plateau_dependency_hash subcap_dependency_hash uniform_dependency_hash
    fixture_hash expected_hash
  ],
  "inputs" => %w[
    fixture_schema expected_schema fixture_keys expected_keys fixture_utf8
    expected_utf8 p_value rho_value gamma_value m_denominator beta_value
    rate_inputs
  ],
  "integrity" => %w[
    main_utf8 primary_utf8 source_utf8 no_controls no_cr no_trailing
    tag_sequence display_balance reference_closure no_discouraged_prose
    no_bare_left holder_spelling
  ],
  "clock_packet" => %w[
    absolute_start absolute_terminal_start absolute_end clock_length
    reset_start reset_terminal_start reset_end sample_a sample_m mode_count
    mode_list strict_modes dyadic_equality packet_rules exact_shear
  ],
  "geometry" => %w[
    sample_geometry subcap_order distance_rule distance_value strip_endpoints
    strip_width terminal_endpoints terminal_widths area_rule area_interior
    area_samples area_upper mass_jacobian strip_mass_coefficient
    terminal_mass_coefficient
  ],
  "moment" => %w[
    variance_rule coefficient_rule degree coefficient_count coefficients
    coefficients_nonnegative sample_value sample_derivative global_upper
    relative_comparison tail_bases tail_rate_negative derivative_bound
    log_comparison moment_not_finite_proof
  ],
  "adjacent" => %w[
    compact_w_range comparison_exponent cubed_exponent two_thirds_exponent
    sup_inf_direction strip_factor cap_l1 favourable_sign adverse_reduces
    time_holder physical_upper
  ],
  "terminal" => %w[
    s0 w_star w0 k0_definition box_order mass_box_scale flux_box_scale
    negative_ratio signed_positive mass_two_sided flux_two_sided
  ],
  "rates" => %w[
    a_square_density m_density q_density raw_rate r_third_rate
    omega_third_rate normalization_cancel normalized_rate
  ],
  "source" => %w[
    local_dependencies heat_sources small_time_sources remez_sources
    no_external_import no_priority_claim
  ],
  "boundary" => %w[
    explicit_only full_plateau complete_signed_flux exact_raw exact_normalized
    arbitrary_open uniform_open version_m_open regularity_open no_figure
    no_simulation not_clay
  ],
}
negative_mutations = groups.values.flatten
abort("duplicate mutation name in R0.76H Ruby suite") unless negative_mutations.uniq.length == negative_mutations.length

main_raw = File.binread(main_path)
primary_raw = File.binread(primary_path)
source_raw = File.binread(source_path)
fixture_raw = File.binread(fixture_path)
expected_raw = File.binread(expected_path)
main_text = main_raw.dup.force_encoding("UTF-8")
primary_text = primary_raw.dup.force_encoding("UTF-8")
source_text = source_raw.dup.force_encoding("UTF-8")
fm = main_text.gsub(/\s+/, " ")
fp = primary_text.gsub(/\s+/, " ")
fs = source_text.gsub(/\s+/, " ")
fixture = JSON.parse(fixture_raw)
expected = JSON.parse(expected_raw)
python_json = JSON.parse(File.read(python_json_path, encoding: "UTF-8"))

clean_bytes = lambda do |raw|
  utf8 = raw.dup.force_encoding("UTF-8")
  utf8.valid_encoding? && raw.bytes.none? do |byte|
    (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127
  end
end

digest = lambda { |relative| Digest::SHA256.file(File.join(root, relative)).hexdigest }
bindings = {}
frozen_hashes.keys.sort.each do |relative|
  bindings[relative] = {
    "expectedSha256" => frozen_hashes.fetch(relative),
    "observedSha256" => digest.call(relative),
  }
end
bound = lambda do |relative|
  row = bindings.fetch(relative)
  row.fetch("expectedSha256") == row.fetch("observedSha256")
end

frozen = fixture.fetch("frozen")
sample = fixture.fetch("sample")
packet = fixture.fetch("packet")
clock = fixture.fetch("clock")
geometry_fixture = fixture.fetch("geometry")
moment_fixture = fixture.fetch("moment")
bounds = fixture.fetch("bounds")
boundary = fixture.fetch("boundary")

a = sample.fetch("a")
m = sample.fetch("m")
delta0 = Rational(sample.fetch("delta0"))
delta = Rational(sample.fetch("delta"))
beta = Rational(frozen.fetch("beta"))
s_star = Rational(sample.fetch("sStar"))
h = Rational(sample.fetch("h"))
q_modes = 2 * m + 1
modes = (2 * m..4 * m).to_a
d_value = delta + 3 * delta0
s0_value = Rational(4) - Rational(1, a)
w_star_value = Rational(3, 2) + 4 * beta
w0_value = w_star_value - (4 * delta0 + beta) / a
strip_left = Rational(1) - 3 * delta0 / a
strip_right = Rational(1) - 2 * delta0 / a
terminal_left = Rational(1) - 4 * delta0 / a
terminal_right = Rational(1) - 3 * delta0 / a
time_width = Rational(1, a)
cap_width = 2 * h / a

area_over_pi = lambda do |z|
  outer = [(a + delta0)**2 - a * a * z * z, Rational(0)].max
  inner = [(a - delta0)**2 - a * a * z * z, Rational(0)].max
  outer - inner
end
interior_area = 4 * a * delta0
inner_sample = Rational(1) - 2 * delta0 / a
outer_edge = Rational(1) + delta0 / a
strip_mass_coefficient = 4 * delta0 * a * a
terminal_mass_coefficient = a * interior_area * time_width * (delta0 / a)

factorial = lambda { |n| (1..n).inject(1, :*) }
coefficients = (0..m).map do |ell|
  Rational(factorial.call(2 * m), factorial.call(2 * m - 2 * ell) * factorial.call(ell))
end
moment_s = Rational(sample.fetch("momentS"))
moment_w = Rational(sample.fetch("momentW"))
t_value = moment_s / (a * a)
moment_value = (0..m).inject(Rational(0)) do |sum, ell|
  sum + coefficients.fetch(ell) * t_value**ell * moment_w**(2 * m - 2 * ell)
end
moment_derivative = (0...m).inject(Rational(0)) do |sum, ell|
  power = 2 * m - 2 * ell
  sum + coefficients.fetch(ell) * t_value**ell * power * moment_w**(power - 1)
end
comparison_exponent = Rational(10, 7) * d_value * m / a
cubed_exponent = Rational(30, 7) * d_value * m / a
two_thirds_exponent = Rational(20, 7) * d_value * m / a
tail_rate_upper = Rational(1, 512) * Rational(2, 7) - Rational(49, 800)

p_value = Rational(frozen.fetch("p"))
p_square = p_value * p_value
a_square_density = p_square
m_density = p_square / frozen.fetch("mDenominator")
q_density = 2 * m_density
r_rate = Rational(frozen.fetch("rLogRate"))
omega_rate = Rational(frozen.fetch("omegaLogRate"))
raw_rate = -r_rate / 3
r_third_rate = r_rate / 3
omega_third_rate = omega_rate / 3
normalized_rate = raw_rate + r_third_rate + omega_third_rate

tags = main_text.scan(/\\tag\{H\.(\d+)\}/).flatten.map(&:to_i)
refs = main_text.scan(/(?<![A-Za-z0-9_.])H\.(\d+)/).flatten.map(&:to_i)
display_opens = main_text.scan(/^\\\[$/).length
display_closes = main_text.scan(/^\\\]$/).length
discouraged = ["我们", "攻关", "主攻", "研究纪律", "三重审计", "杀死错误想法"]

checks = {}
groups.each { |group, names| checks[group] = names.to_h { |name| [name, nil] } }

checks["bindings"]["main_hash"] = bound.call("research/#{stem}.md")
checks["bindings"]["primary_hash"] = bound.call("research/#{stem}_primary_audit.md")
checks["bindings"]["source_hash"] = bound.call("research/r076h_report-source.md")
checks["bindings"]["packet_dependency_hash"] = bound.call("research/r076g_complete_clock_central_fibre_flux_lower_bound.md")
checks["bindings"]["plateau_dependency_hash"] = bound.call("research/r075p_buffered_collar_entrance_concentration.md")
checks["bindings"]["subcap_dependency_hash"] = bound.call("research/r075r_outer_cap_spectral_concentration_obstruction.md")
checks["bindings"]["uniform_dependency_hash"] = bound.call("research/r076e_linear_modal_entropy_window.md")
checks["bindings"]["fixture_hash"] = bound.call("scripts/#{stem}_fixtures.json")
checks["bindings"]["expected_hash"] = bound.call("scripts/#{stem}_expected.json")

checks["inputs"]["fixture_schema"] = fixture.fetch("schema") == "r076h-full-plateau-absorption-for-shifted-packet-fixtures-v1"
checks["inputs"]["expected_schema"] = expected.fetch("schema") == "r076h-full-plateau-absorption-for-shifted-packet-expected-v1"
checks["inputs"]["fixture_keys"] = fixture.keys.sort == %w[boundary bounds clock frozen geometry moment packet sample schema].sort &&
  frozen.keys.sort == %w[beta cGamma mDenominator omegaLogRate p rLogRate rho].sort &&
  sample.keys.sort == %w[a delta delta0 h m momentS momentW sStar].sort &&
  packet.keys.sort == %w[carrierRule firstModeRule lastModeRule modeCountRule samplePositiveModes spacingRule].sort &&
  clock.keys.sort == %w[absoluteEndOverR2 absoluteStartOverR2 absoluteTerminalStartOverR2 resetEnd resetStart resetTerminalStart].sort &&
  geometry_fixture.keys.sort == %w[areaInteriorRule distanceRule plateauStripWidthRule positiveCapWidthRule scaledMassJacobianRule].sort &&
  moment_fixture.keys.sort == %w[coefficientRule comparisonSlopeRule sampleDegree varianceRule].sort &&
  bounds.keys.sort == %w[negativeBase tailExponent tailMomentBase tailReferenceBase wLower wUpper].sort &&
  boundary.keys.sort == %w[arbitraryPacketGeneralization clayClaimed completeSignedFlux exactNormalizedRate exactRawRate explicitShiftedBinomialOnly formalFigureRequired fullPhysicalPlateauMass simulationClaimed uniformExpCqImproved versionMExtraction].sort
checks["inputs"]["expected_keys"] = expected.keys.sort == %w[claims geometry moment rates sample schema].sort &&
  expected.fetch("sample").keys.sort == %w[a dyadicBand firstMode lastMode m q strictlyIncreasing twiceFirstMode].sort &&
  expected.fetch("geometry").keys.sort == %w[D areaAtInnerSampleOverPi areaAtOneOverPi areaAtOuterEdgeOverPi areaAtZeroOverPi interiorAreaOverPi plateauStripLeft plateauStripRight plateauStripWidth positiveCapWidth s0 stripMassCoefficientOverPiR5 terminalMassCoefficientOverPiR5 terminalPlateauLeft terminalPlateauRight terminalTimeWidth w0 wStar].sort &&
  expected.fetch("moment").keys.sort == %w[coefficients comparisonExponent cubedExponent sampleDerivative sampleValue twoThirdsExponent].sort &&
  expected.fetch("rates").keys.sort == %w[aSquareDensity mDensity normalizedRate omegaThirdRate qDensity rThirdRate rawRate].sort &&
  expected.fetch("claims").keys.sort == %w[arbitraryPacketsOpen candidateKilled fullPlateauUsed notClay signedFluxEventuallyPositive uniformExpCqOpen versionMOpen].sort
checks["inputs"]["fixture_utf8"] = clean_bytes.call(fixture_raw)
checks["inputs"]["expected_utf8"] = clean_bytes.call(expected_raw)
checks["inputs"]["p_value"] = p_value == Rational(32, 63)
checks["inputs"]["rho_value"] = Rational(frozen.fetch("rho")) == Rational(9, 10_000)
checks["inputs"]["gamma_value"] = Rational(frozen.fetch("cGamma")) == Rational(8, 3969)
checks["inputs"]["m_denominator"] = frozen.fetch("mDenominator") == 1024
checks["inputs"]["beta_value"] = beta == Rational(1, 100) && fm.include?("\\beta=\\frac1{100}")
checks["inputs"]["rate_inputs"] = r_rate == -Rational(frozen.fetch("rho")) / 4 && omega_rate == -Rational(frozen.fetch("cGamma")) / 4

checks["integrity"]["main_utf8"] = main_text.valid_encoding?
checks["integrity"]["primary_utf8"] = primary_text.valid_encoding?
checks["integrity"]["source_utf8"] = source_text.valid_encoding?
checks["integrity"]["no_controls"] = [main_raw, primary_raw, source_raw, fixture_raw, expected_raw].all? { |raw| clean_bytes.call(raw) }
checks["integrity"]["no_cr"] = [main_raw, primary_raw, source_raw, fixture_raw, expected_raw].none? { |raw| raw.include?("\r") }
checks["integrity"]["no_trailing"] = [main_text, primary_text, source_text].all? do |text|
  text.lines.none? { |line| line.chomp.end_with?(" ", "\t") }
end
checks["integrity"]["tag_sequence"] = tags == (1..39).to_a
checks["integrity"]["display_balance"] = display_opens == 39 && display_closes == 39
checks["integrity"]["reference_closure"] = (refs.uniq - tags.uniq).empty?
checks["integrity"]["no_discouraged_prose"] = discouraged.none? do |word|
  [main_text, primary_text, source_text].any? { |text| text.include?(word) }
end
checks["integrity"]["no_bare_left"] = main_text.match?(/(?<!\\)left[\[(]/) == false
checks["integrity"]["holder_spelling"] = !main_text.include?("Holder") && main_text.include?("Hölder")

checks["clock_packet"]["absolute_start"] = clock.fetch("absoluteStartOverR2") == 61
checks["clock_packet"]["absolute_terminal_start"] = clock.fetch("absoluteTerminalStartOverR2") == 64
checks["clock_packet"]["absolute_end"] = clock.fetch("absoluteEndOverR2") == 65
checks["clock_packet"]["clock_length"] = clock.fetch("absoluteEndOverR2") - clock.fetch("absoluteStartOverR2") == 4
checks["clock_packet"]["reset_start"] = clock.fetch("resetStart") == 0
checks["clock_packet"]["reset_terminal_start"] = clock.fetch("resetTerminalStart") == 3
checks["clock_packet"]["reset_end"] = clock.fetch("resetEnd") == 4
checks["clock_packet"]["sample_a"] = a == expected.dig("sample", "a") && a == 64
checks["clock_packet"]["sample_m"] = m == expected.dig("sample", "m") && m == a * a / 1024 && m == 4
checks["clock_packet"]["mode_count"] = q_modes == expected.dig("sample", "q") && q_modes == 9
checks["clock_packet"]["mode_list"] = modes == packet.fetch("samplePositiveModes")
checks["clock_packet"]["strict_modes"] = modes == modes.uniq.sort && expected.dig("sample", "strictlyIncreasing")
checks["clock_packet"]["dyadic_equality"] = modes.first == expected.dig("sample", "firstMode") &&
  modes.last == expected.dig("sample", "lastMode") &&
  modes.last == 2 * modes.first &&
  modes.last == expected.dig("sample", "twiceFirstMode") &&
  expected.dig("sample", "dyadicBand")
checks["clock_packet"]["packet_rules"] = packet == {
  "modeCountRule" => "2m+1", "firstModeRule" => "2m",
  "lastModeRule" => "4m", "carrierRule" => "3m",
  "spacingRule" => "aR", "samplePositiveModes" => modes,
} && ["q=2m+1", "\\cos(3my)", "\\varepsilon=aR", "B=-\\frac{\\beta a}{R}"].all? { |fragment| fm.include?(fragment) }
checks["clock_packet"]["exact_shear"] = fm.include?("smooth unforced shear") && fm.include?("u=(0,B,F_L(t,x_2))")

checks["geometry"]["sample_geometry"] = [delta0, delta, s_star, h] == [Rational(1, 10), Rational(1, 2), Rational(1, 4), Rational(1, 40)]
checks["geometry"]["subcap_order"] = delta0 < s_star - 3 * h && s_star - 3 * h < s_star + 3 * h && s_star + 3 * h < delta
checks["geometry"]["distance_rule"] = geometry_fixture.fetch("distanceRule") == "delta+3delta0"
checks["geometry"]["distance_value"] = d_value == Rational(expected.dig("geometry", "D")) && d_value == Rational(4, 5)
checks["geometry"]["strip_endpoints"] = strip_left == Rational(expected.dig("geometry", "plateauStripLeft")) &&
  strip_right == Rational(expected.dig("geometry", "plateauStripRight"))
checks["geometry"]["strip_width"] = strip_right - strip_left == Rational(expected.dig("geometry", "plateauStripWidth")) &&
  strip_right - strip_left == delta0 / a && geometry_fixture.fetch("plateauStripWidthRule") == "delta0/a"
checks["geometry"]["terminal_endpoints"] = terminal_left == Rational(expected.dig("geometry", "terminalPlateauLeft")) &&
  terminal_right == Rational(expected.dig("geometry", "terminalPlateauRight"))
checks["geometry"]["terminal_widths"] = time_width == Rational(expected.dig("geometry", "terminalTimeWidth")) &&
  cap_width == Rational(expected.dig("geometry", "positiveCapWidth")) &&
  geometry_fixture.fetch("positiveCapWidthRule") == "2h/a"
checks["geometry"]["area_rule"] = geometry_fixture.fetch("areaInteriorRule") == "4a delta0" &&
  fm.include?("-[(a-\\delta_0)^2-a^2z^2]_+")
checks["geometry"]["area_interior"] = interior_area == Rational(expected.dig("geometry", "interiorAreaOverPi"))
checks["geometry"]["area_samples"] = area_over_pi.call(Rational(0)) == Rational(expected.dig("geometry", "areaAtZeroOverPi")) &&
  area_over_pi.call(inner_sample) == Rational(expected.dig("geometry", "areaAtInnerSampleOverPi")) &&
  area_over_pi.call(Rational(1)) == Rational(expected.dig("geometry", "areaAtOneOverPi")) &&
  area_over_pi.call(outer_edge) == Rational(expected.dig("geometry", "areaAtOuterEdgeOverPi"))
checks["geometry"]["area_upper"] = [Rational(0), inner_sample, Rational(1), outer_edge].all? { |z| area_over_pi.call(z) <= interior_area } &&
  fm.include?("\\le4\\pi a\\delta_0")
checks["geometry"]["mass_jacobian"] = geometry_fixture.fetch("scaledMassJacobianRule") == "aR5" &&
  fm.include?("dx_2=aR dz") && fm.include?("dt=R^2ds") && fm.include?("M_L^{\\rm plat}=aR^5")
checks["geometry"]["strip_mass_coefficient"] = strip_mass_coefficient == Rational(expected.dig("geometry", "stripMassCoefficientOverPiR5"))
checks["geometry"]["terminal_mass_coefficient"] = terminal_mass_coefficient == Rational(expected.dig("geometry", "terminalMassCoefficientOverPiR5"))

checks["moment"]["variance_rule"] = moment_fixture.fetch("varianceRule") == "2s/a2" && fm.include?("\\sigma_s:=\\frac{\\sqrt{2s}}a")
checks["moment"]["coefficient_rule"] = moment_fixture.fetch("coefficientRule") == "(2m)!/((2m-2l)!l!)" &&
  fm.include?("\\frac{(2m)!}{(2m-2\\ell)!\\,\\ell!}")
checks["moment"]["degree"] = moment_fixture.fetch("sampleDegree") == 2 * m && 2 * m == 8
checks["moment"]["coefficient_count"] = coefficients.length == m + 1
checks["moment"]["coefficients"] = coefficients.map(&:to_i) == expected.dig("moment", "coefficients")
checks["moment"]["coefficients_nonnegative"] = coefficients.all? { |value| value >= 0 }
checks["moment"]["sample_value"] = moment_value == Rational(expected.dig("moment", "sampleValue"))
checks["moment"]["sample_derivative"] = moment_derivative == Rational(expected.dig("moment", "sampleDerivative"))
checks["moment"]["global_upper"] = fm.include?("|G_L(s,z)|\\le A\\varepsilon^{2m}\\mathcal M_{m,s}")
checks["moment"]["relative_comparison"] = fm.include?("=o(1)\\mathcal M_{m,s}(w)") &&
  fm.include?("\\frac12A\\varepsilon^{2m}\\mathcal M_{m,s}(w)")
checks["moment"]["tail_bases"] = Rational(bounds.fetch("tailMomentBase")) == Rational(9, 5) &&
  Rational(bounds.fetch("tailReferenceBase")) == Rational(7, 5) &&
  Rational(bounds.fetch("tailExponent")) == -Rational(49, 800)
checks["moment"]["tail_rate_negative"] = tail_rate_upper.negative? && fm.include?("2m log(9/7)-49a^2/800+O(1)")
checks["moment"]["derivative_bound"] = moment_fixture.fetch("comparisonSlopeRule") == "10m/7" &&
  fm.include?("\\le\\frac{2m}{w}\\le\\frac{10m}{7}")
checks["moment"]["log_comparison"] = fm.include?("\\exp\\!\\left(\\frac{10m}{7}|w-w'|\\right)")
checks["moment"]["moment_not_finite_proof"] = fs.include?("cannot replace the limiting moment argument")

checks["adjacent"]["compact_w_range"] = Rational(bounds.fetch("wLower")) == Rational(7, 5) &&
  Rational(bounds.fetch("wUpper")) == Rational(8, 5) &&
  fm.include?("\\frac75\\le w(s,z_o),w(s,z_p)\\le\\frac85")
checks["adjacent"]["comparison_exponent"] = comparison_exponent == Rational(expected.dig("moment", "comparisonExponent"))
checks["adjacent"]["cubed_exponent"] = cubed_exponent == Rational(expected.dig("moment", "cubedExponent"))
checks["adjacent"]["two_thirds_exponent"] = two_thirds_exponent == Rational(expected.dig("moment", "twoThirdsExponent"))
checks["adjacent"]["sup_inf_direction"] = main_text.include?("U_L(s)") && fm.include?("\\inf_{z\\in J_{a,p}}G_L(s,z)")
checks["adjacent"]["strip_factor"] = fm.include?("\\frac{\\delta_0}{8a}") && fm.include?("-\\frac{30D}{7}\\frac ma")
checks["adjacent"]["cap_l1"] = fm.include?("\\int_{\\mathcal C_{a,+}}(-W_a(z))\\,dz")
checks["adjacent"]["favourable_sign"] = fm.include?("positive cap is the only favourable sign")
checks["adjacent"]["adverse_reduces"] = fm.include?("full negative cap may only reduce the signed integral")
checks["adjacent"]["time_holder"] = fm.include?("\\le4^{1/3}Q_L^{2/3}")
checks["adjacent"]["physical_upper"] = fm.include?("a^{4/3}R^{-1/3}") && fm.include?("\\exp\\!\\left(C_*\\frac ma\\right)")

checks["terminal"]["s0"] = s0_value == Rational(expected.dig("geometry", "s0")) && s0_value == Rational(255, 64)
checks["terminal"]["w_star"] = w_star_value == Rational(expected.dig("geometry", "wStar")) && w_star_value == Rational(77, 50)
checks["terminal"]["w0"] = w0_value == Rational(expected.dig("geometry", "w0")) && w0_value == Rational(1963, 1280)
checks["terminal"]["k0_definition"] = fm.include?("K_0:=\\mathcal M_{m,s_0}(w_0)")
checks["terminal"]["box_order"] = terminal_left < terminal_right && terminal_right < strip_right &&
  strip_right < 1 && s0_value < 4 && cap_width.positive?
checks["terminal"]["mass_box_scale"] = terminal_mass_coefficient == 4 * delta0 * delta0 &&
  fm.include?("cR^5A^3\\varepsilon^{6m}K_0^3")
checks["terminal"]["flux_box_scale"] = a * time_width * cap_width == 2 * h / a &&
  fm.include?("c\\beta a^{-1}A^2\\varepsilon^{4m}K_0^2")
checks["terminal"]["negative_ratio"] = Rational(bounds.fetch("negativeBase")) == Rational(2, 3) &&
  fm.include?("\\left(\\frac{2}{3w_0}\\right)^{4m}=o(1)")
checks["terminal"]["signed_positive"] = fp.include?("eventual strict positivity") &&
  expected.dig("claims", "signedFluxEventuallyPositive")
checks["terminal"]["mass_two_sided"] = fm.include?("\\le M_L^{\\rm plat}") &&
  fm.include?("\\le Ca^2e^{Ca}R^5A^3\\varepsilon^{6m}K_0^3")
checks["terminal"]["flux_two_sided"] = fm.include?("\\le\\mathcal S_L") &&
  fm.include?("\\le C\\beta e^{Ca}A^2\\varepsilon^{4m}K_0^2")

checks["rates"]["a_square_density"] = a_square_density == Rational(expected.dig("rates", "aSquareDensity"))
checks["rates"]["m_density"] = m_density == Rational(expected.dig("rates", "mDensity")) && m_density == Rational(1, 3969)
checks["rates"]["q_density"] = q_density == Rational(expected.dig("rates", "qDensity")) && q_density == Rational(2, 3969)
checks["rates"]["raw_rate"] = raw_rate == Rational(expected.dig("rates", "rawRate")) && raw_rate == Rational(3, 40_000)
checks["rates"]["r_third_rate"] = r_third_rate == Rational(expected.dig("rates", "rThirdRate")) && r_third_rate == -Rational(3, 40_000)
checks["rates"]["omega_third_rate"] = omega_third_rate == Rational(expected.dig("rates", "omegaThirdRate")) && omega_third_rate == -Rational(2, 11_907)
checks["rates"]["normalization_cancel"] = raw_rate + r_third_rate == 0 && fm.include?("R^{1/3}\\omega^{1/3}")
checks["rates"]["normalized_rate"] = normalized_rate == Rational(expected.dig("rates", "normalizedRate")) &&
  normalized_rate == -Rational(2, 11_907) && fm.include?("=-\\frac2{11907}")

checks["source"]["local_dependencies"] = [
  frozen_hashes.fetch("research/r076g_complete_clock_central_fibre_flux_lower_bound.md"),
  frozen_hashes.fetch("research/r075p_buffered_collar_entrance_concentration.md"),
  frozen_hashes.fetch("research/r075r_outer_cap_spectral_concentration_obstruction.md"),
  frozen_hashes.fetch("research/r076e_linear_modal_entropy_window.md"),
].all? { |value| source_text.include?(value) }
checks["source"]["heat_sources"] = source_text.include?("1711.04279") && source_text.include?("1711.06088")
checks["source"]["small_time_sources"] = source_text.include?("math/0307158") &&
  source_text.include?("10.1016/j.jde.2004.05.007") && source_text.include?("1806.00969")
checks["source"]["remez_sources"] = source_text.include?("F. L. Nazarov") && source_text.include?("1809.09726")
checks["source"]["no_external_import"] = fs.include?("imports no external observability, Remez, or control theorem")
checks["source"]["no_priority_claim"] = fs.include?("not evidence of novelty or priority")

checks["boundary"]["explicit_only"] = boundary.fetch("explicitShiftedBinomialOnly") &&
  expected.dig("claims", "candidateKilled") && fp.include?("kills only the explicit shifted-binomial candidate")
checks["boundary"]["full_plateau"] = boundary.fetch("fullPhysicalPlateauMass") &&
  expected.dig("claims", "fullPlateauUsed") && fp.include?("full physical plateau mass")
checks["boundary"]["complete_signed_flux"] = boundary.fetch("completeSignedFlux") && fp.include?("complete-clock signed flux")
checks["boundary"]["exact_raw"] = boundary.fetch("exactRawRate") &&
  expected.dig("claims", "fullPlateauUsed") && fm.include?("=\\frac3{40000}")
checks["boundary"]["exact_normalized"] = boundary.fetch("exactNormalizedRate") && fm.include?("=-\\frac2{11907}<0")
checks["boundary"]["arbitrary_open"] = !boundary.fetch("arbitraryPacketGeneralization") &&
  expected.dig("claims", "arbitraryPacketsOpen") && fm.include?("arbitrary packets")
checks["boundary"]["uniform_open"] = !boundary.fetch("uniformExpCqImproved") &&
  expected.dig("claims", "uniformExpCqOpen") && fm.include?("does not improve R0.76E")
checks["boundary"]["version_m_open"] = !boundary.fetch("versionMExtraction") &&
  expected.dig("claims", "versionMOpen") && fm.include?("complete Version-M extraction")
checks["boundary"]["regularity_open"] = fm.include?("regularity") && fm.include?("singularity")
checks["boundary"]["no_figure"] = !boundary.fetch("formalFigureRequired") &&
  fm.include?("No simulation or formal scientific figure is claimed")
checks["boundary"]["no_simulation"] = !boundary.fetch("simulationClaimed")
checks["boundary"]["not_clay"] = !boundary.fetch("clayClaimed") &&
  expected.dig("claims", "notClay") && main_text.include?("**NOT CLAY.**")

unless checks.keys == groups.keys && groups.all? { |group, names| checks.fetch(group).keys == names }
  abort("R0.76H Ruby assertion inventory mismatch")
end

unless mutation.empty?
  unless negative_mutations.include?(mutation)
    warn "unknown R076H_RUBY_MUTATION: #{mutation}"
    exit 2
  end
  groups.each do |group, names|
    checks.fetch(group)[mutation] = false if names.include?(mutation)
  end
end

failures = checks.flat_map do |group, rows|
  rows.reject { |_name, value| value }.keys.map { |name| "#{group}.#{name}" }
end
assertions = checks.values.map(&:length).inject(0, :+)
exact = {
  "sample" => {"a" => a, "m" => m, "q" => q_modes, "modes" => modes},
  "geometry" => {
    "D" => d_value.to_s, "s0" => s0_value.to_s,
    "wStar" => w_star_value.to_s, "w0" => w0_value.to_s,
    "plateauStrip" => [strip_left.to_s, strip_right.to_s],
    "terminalPlateau" => [terminal_left.to_s, terminal_right.to_s],
    "interiorAreaOverPi" => interior_area.to_s,
    "stripMassCoefficientOverPiR5" => strip_mass_coefficient.to_s,
    "terminalMassCoefficientOverPiR5" => terminal_mass_coefficient.to_s,
  },
  "moment" => {
    "coefficients" => coefficients.map(&:to_i),
    "sampleValue" => moment_value.to_s,
    "sampleDerivative" => moment_derivative.to_s,
    "comparisonExponent" => comparison_exponent.to_s,
    "cubedExponent" => cubed_exponent.to_s,
    "twoThirdsExponent" => two_thirds_exponent.to_s,
  },
  "rates" => {
    "mDensity" => m_density.to_s, "qDensity" => q_density.to_s,
    "rawRate" => raw_rate.to_s, "rThirdRate" => r_third_rate.to_s,
    "omegaThirdRate" => omega_third_rate.to_s,
    "normalizedRate" => normalized_rate.to_s,
  },
}
exact_match = exact == python_json.fetch("exact")
mutation_match = negative_mutations == python_json.fetch("negativeMutations")
verdict = failures.empty? && exact_match && mutation_match ? "PASS" : "FAIL"

lines = [
  "# R0.76H independent finite audit", "",
  "- Verdict: **#{verdict}**",
  "- Ruby assertions: #{assertions - failures.length}/#{assertions}",
  "- Python/Ruby exact section identical: #{exact_match ? 'PASS' : 'FAIL'}",
  "- Python/Ruby mutation inventory identical: #{mutation_match ? 'PASS' : 'FAIL'}",
  "- Exact sample: a=#{a}, m=#{m}, q=#{q_modes}, modes #{modes.first}--#{modes.last}",
  "- Exact raw logarithmic rate: #{raw_rate}",
  "- Exact normalized logarithmic rate: #{normalized_rate}",
  "- Failures: #{failures.empty? ? 'none' : failures.inspect}", "",
  "This implementation independently recomputes every finite binding,",
  "geometry, moment, scaling, exponent, source, and claim-boundary row.",
  "It does not certify the continuum Gaussian-moment lemma.  The result",
  "concerns one explicit shifted-binomial packet on the full physical",
  "plateau. **NOT CLAY.**", "",
]
File.write(report_path, lines.join("\n"), mode: "w", encoding: "UTF-8")
exit(verdict == "PASS" ? 0 : 1)
