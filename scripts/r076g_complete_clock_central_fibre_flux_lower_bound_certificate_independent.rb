#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"
require "json"

root = File.expand_path("..", __dir__)
stem = "r076g_complete_clock_central_fibre_flux_lower_bound"
fixture_path = File.join(root, "scripts", "#{stem}_fixtures.json")
expected_path = File.join(root, "scripts", "#{stem}_expected.json")
main_path = File.join(root, "research", "#{stem}.md")
primary_path = File.join(root, "research", "#{stem}_primary_audit.md")
source_path = File.join(root, "research", "r076g_report-source.md")
python_json_path = ENV.fetch("R076G_JSON", File.join(root, "research", "#{stem}_certificate.json"))
report_path = ENV.fetch("R076G_RUBY_REPORT", File.join(root, "research", "#{stem}_independent_audit.md"))
mutation = ENV.fetch("R076G_RUBY_MUTATION", "")

frozen = {
  "research/#{stem}.md" => "20f32790b53f2b0f5cb39b7071bd2cda96ddb4e15f75211e1682f4ba37dd0bb2",
  "research/#{stem}_primary_audit.md" => "af47153c4e1f4c5749f68c3f89d7533c5d95f3c0c6f15b0c775a9e35317c807e",
  "research/r076g_report-source.md" => "3aea1d04dce4987c3883c1b93bec04e714ee17b540fb6a99546d084efa326f74",
  "research/r075b_bulk_clock_outer_padding_gate.md" => "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
  "research/r075r_outer_cap_spectral_concentration_obstruction.md" => "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
  "research/r076e_linear_modal_entropy_window.md" => "1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4",
  "research/r076f_exponential_spatial_observation_lower_bound.md" => "48204fcbf8fe9af3f0fdc7720844c3dd8362d8767caf73de016eda7250b70973",
  "scripts/#{stem}_fixtures.json" => "32e1dcf71a77ba0d28e3924fcb7e7aeb4d2840aa08ba2b2e352bb4d20d0464af",
  "scripts/#{stem}_expected.json" => "0a2d3d086381029941310ae502b4cf9462e025d0c75e62dd87c07334728a6ba8",
}.freeze

raws = {
  "main" => File.binread(main_path),
  "primary" => File.binread(primary_path),
  "source" => File.binread(source_path),
  "fixtures" => File.binread(fixture_path),
  "expected" => File.binread(expected_path),
}
fixture = JSON.parse(raws.fetch("fixtures"))
expected = JSON.parse(raws.fetch("expected"))
main_text = raws.fetch("main").dup.force_encoding(Encoding::UTF_8)
primary_text = raws.fetch("primary").dup.force_encoding(Encoding::UTF_8)
source_text = raws.fetch("source").dup.force_encoding(Encoding::UTF_8)
python_json = JSON.parse(File.read(python_json_path, encoding: "UTF-8"))

flat = ->(text) { text.gsub(/\s+/, " ") }
clean_bytes = lambda do |data|
  data.dup.force_encoding(Encoding::UTF_8).valid_encoding? &&
    data.bytes.none? { |byte| (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127 }
end
fm = flat.call(main_text)
fp = flat.call(primary_text)
fs = flat.call(source_text)
m = Integer(fixture.dig("packet", "sampleM"))
modes = (2 * m..4 * m).to_a
count = 2 * m + 1
central_drift = Rational(fixture.dig("bounds", "centralDriftBase"))
moment = Rational(fixture.dig("bounds", "momentAllowance"))
central_raw = central_drift + moment
central_base = Rational(fixture.dig("bounds", "centralBase"))
central_gap = central_base - central_raw
positive = Rational(fixture.dig("bounds", "positiveBase"))
negative_geometry = Rational(1, 2) + Rational(fixture.dig("bounds", "negativeGeometryAllowance"))
negative = negative_geometry + moment
ratio_base = positive / central_base
adverse_ratio = negative / positive
p = Rational(fixture.dig("frozen", "p"))
p_square = p * p
denom = Integer(fixture.dig("frozen", "mDenominator"))
mode_density = 2 * p_square / denom
four_m_density = 4 * p_square / denom
omega_rate = -Rational(fixture.dig("frozen", "cGamma")) / 12
log_lower = Rational(expected.dig("rational", "logLowerBound"))
net_rate = four_m_density * log_lower + omega_rate

groups = {
  "bindings" => %w[main_hash primary_hash source_hash clock_dependency_hash cap_dependency_hash upper_dependency_hash static_dependency_hash fixture_hash expected_hash],
  "inputs" => %w[fixture_schema expected_schema fixture_utf8 expected_utf8 rho_value beta_value mode_count_rule first_mode_rule last_mode_rule expected_dyadic_band expected_claim_complete expected_claim_rate expected_claim_plateau_open expected_claim_not_clay],
  "integrity" => %w[main_utf8 primary_utf8 source_utf8 no_controls no_cr no_trailing tag_sequence display_balance reference_closure no_discouraged_prose no_bare_left no_undefined_delta_c],
  "clock" => %w[absolute_start absolute_terminal_start absolute_end clock_length reset_start reset_terminal_start reset_end terminal_unit_length translated_cutoff terminal_cutoff_one],
  "packet" => %w[sample_m mode_count mode_list integer_modes strict_order first_mode last_mode dyadic_equality no_zero_mode carrier_rule spacing_rule drift_nonzero scaled_drift real_scalar exact_heat nse_embedding],
  "rational" => %w[central_drift moment_allowance central_raw central_gap central_strict positive_base negative_geometry negative_base ratio_base adverse_ratio p_square mode_density four_m_density omega_rate log_lower net_rate net_rate_positive central_drift_from_beta fixture_negative_base fixture_ratio_base],
  "analysis" => %w[gaussian_formula moment_upper coherent_lower tail_bound central_spacetime positive_cap negative_cap signed_combination complete_flux_ratio physical_conversion central_proxy negative_support_sign good_bad_bridge log_inequality normalized_rate static_near_cap],
  "source" => %w[wang_source egidi_source miller_source laurent_source nazarov_source remez_source local_proof_boundary no_novelty_claim primary_pass math_blocker_zero release_blocker_zero],
  "boundary" => %w[complete_signed_flux central_only no_full_plateau_lower no_version_m_counterexample optimal_base_open arbitrary_open version_m_open regularity_open singularity_open no_figure no_simulation not_clay],
}.freeze
negative_mutations = groups.values.flatten.freeze
abort "unknown R076G_RUBY_MUTATION: #{mutation}" unless mutation.empty? || negative_mutations.include?(mutation)
abort "duplicate mutation name in R0.76G Ruby suite" unless negative_mutations.uniq.length == negative_mutations.length

bindings = frozen.keys.sort.to_h do |path|
  observed = Digest::SHA256.file(File.join(root, path)).hexdigest
  [path, {"expectedSha256" => frozen.fetch(path), "observedSha256" => observed}]
end
bound = lambda do |path|
  row = bindings.fetch(path)
  row.fetch("expectedSha256") == row.fetch("observedSha256")
end

checks = {}
groups.each { |group, names| checks[group] = names.to_h { |name| [name, nil] } }

checks["bindings"]["main_hash"] = bound.call("research/#{stem}.md")
checks["bindings"]["primary_hash"] = bound.call("research/#{stem}_primary_audit.md")
checks["bindings"]["source_hash"] = bound.call("research/r076g_report-source.md")
checks["bindings"]["clock_dependency_hash"] = bound.call("research/r075b_bulk_clock_outer_padding_gate.md")
checks["bindings"]["cap_dependency_hash"] = bound.call("research/r075r_outer_cap_spectral_concentration_obstruction.md")
checks["bindings"]["upper_dependency_hash"] = bound.call("research/r076e_linear_modal_entropy_window.md")
checks["bindings"]["static_dependency_hash"] = bound.call("research/r076f_exponential_spatial_observation_lower_bound.md")
checks["bindings"]["fixture_hash"] = bound.call("scripts/#{stem}_fixtures.json")
checks["bindings"]["expected_hash"] = bound.call("scripts/#{stem}_expected.json")
checks["inputs"]["fixture_schema"] = fixture["schema"] == "r076g-complete-clock-central-fibre-flux-lower-bound-fixtures-v1"
checks["inputs"]["expected_schema"] = expected["schema"] == "r076g-complete-clock-central-fibre-flux-lower-bound-expected-v1"
checks["inputs"]["fixture_utf8"] = clean_bytes.call(raws.fetch("fixtures"))
checks["inputs"]["expected_utf8"] = clean_bytes.call(raws.fetch("expected"))
checks["inputs"]["rho_value"] = Rational(fixture.dig("frozen", "rho")) == Rational(9, 10_000) && main_text.include?("`rho=9/10000`")
checks["inputs"]["beta_value"] = Rational(fixture.dig("frozen", "beta")) == Rational(1, 100) && fm.include?("\\beta=\\frac1{100}")
checks["inputs"]["mode_count_rule"] = fixture.dig("packet", "modeCountRule") == "2m+1" && fm.include?("q=2m+1")
checks["inputs"]["first_mode_rule"] = fixture.dig("packet", "firstModeRule") == "2m" && modes.first == 2 * m
checks["inputs"]["last_mode_rule"] = fixture.dig("packet", "lastModeRule") == "4m" && modes.last == 4 * m
checks["inputs"]["expected_dyadic_band"] = expected.dig("sample", "dyadicBand") && modes.last <= 2 * modes.first
checks["inputs"]["expected_claim_complete"] = expected.dig("claims", "exponentialCompleteCentralRow")
checks["inputs"]["expected_claim_rate"] = expected.dig("claims", "positiveNormalizedCentralRate")
checks["inputs"]["expected_claim_plateau_open"] = expected.dig("claims", "physicalPlateauSharpnessOpen")
checks["inputs"]["expected_claim_not_clay"] = expected.dig("claims", "notClay")
checks["integrity"]["main_utf8"] = clean_bytes.call(raws.fetch("main"))
checks["integrity"]["primary_utf8"] = clean_bytes.call(raws.fetch("primary"))
checks["integrity"]["source_utf8"] = clean_bytes.call(raws.fetch("source"))
checks["integrity"]["no_controls"] = raws.values.all? { |value| clean_bytes.call(value) }
checks["integrity"]["tag_sequence"] = main_text.scan(/\\tag\{G\.(\d+)\}/).flatten.map(&:to_i) == (1..40).to_a
checks["integrity"]["display_balance"] = main_text.scan(/^\\\[$/).length == 40 && main_text.scan(/^\\\]$/).length == 40
checks["integrity"]["no_cr"] = raws.values.none? { |value| value.include?("\r") }
checks["integrity"]["no_trailing"] = [main_text, primary_text, source_text].all? { |text| text.lines.none? { |line| line.chomp.end_with?(" ", "\t") } }
tags = main_text.scan(/\\tag\{G\.(\d+)\}/).flatten.map(&:to_i)
refs = main_text.scan(/(?<![A-Za-z0-9_.])G\.(\d+)/).flatten.map(&:to_i)
checks["integrity"]["reference_closure"] = (refs.uniq - tags.uniq).empty?
checks["integrity"]["no_discouraged_prose"] = %w[我们 攻关 主攻 研究纪律 三重审计 杀死错误想法].none? do |word|
  [main_text, primary_text, source_text].any? { |text| text.include?(word) }
end
checks["integrity"]["no_bare_left"] = main_text.scan(/(?<!\\)left[\[(]/).empty?
checks["integrity"]["no_undefined_delta_c"] = !main_text.include?("\\delta_c") && !primary_text.include?("delta_c")
checks["clock"]["absolute_start"] = fixture.dig("clock", "absoluteStartOverR2") == 61
checks["clock"]["absolute_terminal_start"] = fixture.dig("clock", "absoluteTerminalStartOverR2") == 64
checks["clock"]["absolute_end"] = fixture.dig("clock", "absoluteEndOverR2") == 65
checks["clock"]["clock_length"] = fixture.dig("clock", "absoluteEndOverR2") - fixture.dig("clock", "absoluteStartOverR2") == 4
checks["clock"]["reset_start"] = fixture.dig("clock", "resetStart") == 0
checks["clock"]["reset_terminal_start"] = fixture.dig("clock", "resetTerminalStart") == 3
checks["clock"]["reset_end"] = fixture.dig("clock", "resetEnd") == 4
checks["clock"]["terminal_unit_length"] = fixture.dig("clock", "resetEnd") - fixture.dig("clock", "resetTerminalStart") == 1
checks["clock"]["translated_cutoff"] = fm.include?("\\widetilde\\eta_R(t):=\\eta_R(s_R+t)")
checks["clock"]["terminal_cutoff_one"] = fm.include?("\\zeta(s)=1\\quad(3<s<4)")
checks["packet"]["sample_m"] = m == expected.dig("sample", "m")
checks["packet"]["mode_count"] = count == expected.dig("sample", "modeCount")
checks["packet"]["mode_list"] = modes == fixture.dig("packet", "samplePositiveModes")
checks["packet"]["integer_modes"] = modes.all? { |value| value.is_a?(Integer) }
checks["packet"]["strict_order"] = modes == modes.uniq.sort && expected.dig("sample", "strictlyIncreasing")
checks["packet"]["first_mode"] = modes.first == expected.dig("sample", "firstMode") && modes.first == 6
checks["packet"]["last_mode"] = modes.last == expected.dig("sample", "lastMode") && modes.last == 12
checks["packet"]["dyadic_equality"] = modes.last == 2 * modes.first && modes.last == expected.dig("sample", "twiceFirstMode")
checks["packet"]["no_zero_mode"] = modes.first.positive?
checks["packet"]["carrier_rule"] = fixture.dig("packet", "carrierRule") == "3m" && fm.include?("\\cos(3my)")
checks["packet"]["spacing_rule"] = fixture.dig("packet", "spacingRule") == "aR" && fm.include?("\\varepsilon=aR")
checks["packet"]["drift_nonzero"] = Rational(fixture.dig("frozen", "beta")).positive? && fm.include?("B=-\\frac{\\beta a}{R}")
checks["packet"]["scaled_drift"] = fm.include?("v=\\frac{BR}{a}=-\\beta")
checks["packet"]["real_scalar"] = fm.include?("real trigonometric polynomial")
checks["packet"]["exact_heat"] = fm.include?("(\\partial_t+B\\partial_2-\\partial_2^2)F_L=0")
checks["packet"]["nse_embedding"] = fm.include?("u_L(t,x)=(0,B,F_L(t,x_2))")
checks["rational"]["central_drift"] = central_drift == Rational(26, 25)
checks["rational"]["moment_allowance"] = moment == Rational(1, 8)
checks["rational"]["central_raw"] = central_raw == Rational(233, 200)
checks["rational"]["central_gap"] = central_gap == Rational(1, 600)
checks["rational"]["central_strict"] = central_raw < central_base
checks["rational"]["positive_base"] = positive == Rational(3, 2)
checks["rational"]["negative_geometry"] = negative_geometry == Rational(13, 24)
checks["rational"]["negative_base"] = negative == Rational(2, 3)
checks["rational"]["ratio_base"] = ratio_base == Rational(9, 7)
checks["rational"]["adverse_ratio"] = adverse_ratio == Rational(4, 9)
checks["rational"]["p_square"] = p_square == Rational(1024, 3969)
checks["rational"]["mode_density"] = mode_density == Rational(2, 3969)
checks["rational"]["four_m_density"] = four_m_density == Rational(4, 3969)
checks["rational"]["omega_rate"] = omega_rate == -Rational(2, 11907)
checks["rational"]["log_lower"] = log_lower == Rational(2, 9)
checks["rational"]["net_rate"] = net_rate == Rational(2, 35721)
checks["rational"]["net_rate_positive"] = net_rate.positive?
checks["rational"]["central_drift_from_beta"] = central_drift == 1 + 4 * Rational(fixture.dig("frozen", "beta"))
checks["rational"]["fixture_negative_base"] = Rational(fixture.dig("bounds", "negativeBase")) == negative
checks["rational"]["fixture_ratio_base"] = Rational(fixture.dig("bounds", "ratioBase")) == ratio_base
checks["analysis"]["gaussian_formula"] = fm.include?("periodic heat-kernel representation") && main_text.include?("\\mathbb E")
checks["analysis"]["moment_upper"] = fm.include?("\\left(|w|+\\frac{4\\sqrt m}{a}\\right)^{2m}")
checks["analysis"]["coherent_lower"] = fm.include?("G_L(s,z)\\ge\\frac A2\\varepsilon^{2m}w^{2m}")
checks["analysis"]["tail_bound"] = main_text.include?("e^{-49a^2/800}")
checks["analysis"]["central_spacetime"] = fm.include?("H_L\\le4A^3\\varepsilon^{6m}\\left(\\frac76\\right)^{6m}")
checks["analysis"]["positive_cap"] = main_text.include?("\\left(\\frac32\\right)^{4m}")
checks["analysis"]["negative_cap"] = main_text.include?("\\left(\\frac23\\right)^{4m}")
checks["analysis"]["signed_combination"] = fm.include?("Only the negative cap can contribute with the adverse sign")
checks["analysis"]["complete_flux_ratio"] = main_text.include?("\\left(\\frac97\\right)^{4m}")
checks["analysis"]["physical_conversion"] = fm.include?("\\mathcal T_L=\\frac{a^2R^3}{2}\\mathcal S_L")
checks["analysis"]["central_proxy"] = fm.include?("This `M_L^I` is not the full physical plateau mass")
checks["analysis"]["negative_support_sign"] = fm.include?("\\delta/a+4\\beta<1/2") && main_text.include?("w<0")
checks["analysis"]["good_bad_bridge"] = fm.include?("(1-o(1))(\\mathbb E|X|^{2m}-E_{\\rm tail})-E_{\\rm tail}")
checks["analysis"]["log_inequality"] = fm.include?("\\log(1+x)>x/(1+x)") && main_text.include?("x=2/7")
checks["analysis"]["normalized_rate"] = fm.include?("\\frac{4\\log(9/7)}{3969}-\\frac2{11907}>0")
checks["analysis"]["static_near_cap"] = fm.include?("\\le C_{\\delta_0,s_*}\\frac ma")
checks["source"]["wang_source"] = source_text.include?("1711.04279")
checks["source"]["egidi_source"] = source_text.include?("1711.06088")
checks["source"]["miller_source"] = source_text.include?("math/0307158") && source_text.include?("10.1016/j.jde.2004.05.007")
checks["source"]["laurent_source"] = source_text.include?("1806.00969") && source_text.include?("10.2140/apde.2021.14.355")
checks["source"]["nazarov_source"] = source_text.include?("F. L. Nazarov") && source_text.include?("mathnet.ru")
checks["source"]["remez_source"] = source_text.include?("S. Tikhonov and P. Yuditskii")
checks["source"]["local_proof_boundary"] = fs.include?("does not import a control or observability theorem")
checks["source"]["no_novelty_claim"] = fs.include?("not evidence of novelty or priority")
checks["source"]["primary_pass"] = primary_text.include?("Current verdict: **PASS**")
checks["source"]["math_blocker_zero"] = primary_text.include?("Mathematical blocker count: **0**")
checks["source"]["release_blocker_zero"] = primary_text.include?("Release blocker count: **0**")
checks["boundary"]["complete_signed_flux"] = fixture.dig("boundary", "completeSignedFlux") && fm.include?("complete signed flux")
checks["boundary"]["central_only"] = fixture.dig("boundary", "centralFibreProxy") && fm.include?("central-fibre proxy")
checks["boundary"]["no_full_plateau_lower"] = !fixture.dig("boundary", "fullPhysicalPlateauLowerBound") && fm.include?("does **not** prove an exponential lower bound")
checks["boundary"]["no_version_m_counterexample"] = !fixture.dig("boundary", "versionMCounterexample") && fm.include?("No counterexample to R0.76E, E.24, or Version-M is claimed")
checks["boundary"]["optimal_base_open"] = fm.include?("optimal exponential base")
checks["boundary"]["arbitrary_open"] = fm.include?("arbitrary packets")
checks["boundary"]["version_m_open"] = fm.include?("complete Version-M extraction")
checks["boundary"]["regularity_open"] = fm.include?("regularity")
checks["boundary"]["singularity_open"] = fm.include?("singularity")
checks["boundary"]["no_figure"] = !fixture.dig("boundary", "formalFigureRequired") && fm.include?("No simulation or formal scientific figure is claimed")
checks["boundary"]["no_simulation"] = !fixture.dig("boundary", "simulationClaimed")
checks["boundary"]["not_clay"] = !fixture.dig("boundary", "clayClaimed") && main_text.include?("**NOT CLAY.**")

if !mutation.empty?
  unless groups.values.flatten.include?(mutation)
    warn "unknown R076G_RUBY_MUTATION: #{mutation}"
    exit 2
  end
  groups.each { |group, names| checks[group][mutation] = false if names.include?(mutation) }
end

failures = checks.flat_map do |group, rows|
  rows.reject { |_name, value| value }.keys.map { |name| "#{group}.#{name}" }
end
assertions = checks.values.sum(&:length)
exact = {
  "sample" => { "m" => m, "modeCount" => count, "modes" => modes },
  "rational" => {
    "centralRaw" => central_raw.to_s, "centralGap" => central_gap.to_s,
    "ratioBase" => ratio_base.to_s, "adverseRatio" => adverse_ratio.to_s,
    "modeDensity" => mode_density.to_s, "fourMDensity" => four_m_density.to_s,
    "omegaRate" => omega_rate.to_s, "netRateRationalLowerBound" => net_rate.to_s,
  },
}
exact_match = exact == python_json.fetch("exact")
mutation_match = groups.values.flatten == python_json.fetch("negativeMutations")
verdict = failures.empty? && exact_match && mutation_match ? "PASS" : "FAIL"

lines = [
  "# R0.76G independent finite audit", "",
  "- Verdict: **#{verdict}**",
  "- Ruby assertions: #{assertions - failures.length}/#{assertions}",
  "- Python/Ruby exact section identical: #{exact_match ? 'PASS' : 'FAIL'}",
  "- Python/Ruby mutation inventory identical: #{mutation_match ? 'PASS' : 'FAIL'}",
  "- Exact sample modes: #{modes.inspect}",
  "- Exact normalized rational rate lower bound: #{net_rate}",
  "- Failures: #{failures.empty? ? 'none' : failures.inspect}", "",
  "This implementation independently recomputes every finite binding, input,",
  "structure, clock, frequency, rational, source, and claim-boundary row.",
  "It does not certify the continuum Gaussian lemma.  The result concerns",
  "the complete signed flux only against the central fibre proxy; full",
  "physical plateau sharpness remains open. **NOT CLAY.**", "",
]
File.write(report_path, lines.join("\n"), mode: "w", encoding: "UTF-8")
exit(verdict == "PASS" ? 0 : 1)
