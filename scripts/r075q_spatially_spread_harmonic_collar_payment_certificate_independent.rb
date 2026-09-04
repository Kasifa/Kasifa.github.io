#!/usr/bin/env ruby
# Independent fail-closed verifier for frozen R0.75Q.

require "digest"
require "json"

ROOT = File.expand_path("..", __dir__)
STEM = "r075q_spatially_spread_harmonic_collar_payment"
MAIN = File.join(ROOT, "research", "#{STEM}.md")
PRIMARY = File.join(ROOT, "research", "#{STEM}_primary_audit.md")
SOURCE = File.join(ROOT, "research", "r075q_report-source.md")
FIXTURES = File.join(ROOT, "scripts", "#{STEM}_fixtures.json")
EXPECTED = File.join(ROOT, "scripts", "#{STEM}_expected.json")
CERTIFICATE = ENV.fetch("R075Q_JSON", File.join(ROOT, "research", "#{STEM}_certificate.json"))
OUT_REPORT = ENV.fetch("R075Q_RUBY_REPORT", File.join(ROOT, "research", "#{STEM}_independent_audit.md"))
MUTATION = ENV.fetch("R075Q_RUBY_MUTATION", "")

FROZEN = {
  "research/r075b_bulk_clock_outer_padding_gate.md" =>
    "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
  "research/r075l_single_harmonic_diffusive_signed_flux_gain.md" =>
    "52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5",
  "research/r075n_radial_collar_averaged_wiener_row.md" =>
    "ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318",
  "research/r075p_buffered_collar_entrance_concentration.md" =>
    "8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6",
  "research/r075q_spatially_spread_harmonic_collar_payment.md" =>
    "9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c",
  "research/r075q_spatially_spread_harmonic_collar_payment_primary_audit.md" =>
    "92255869e165efdbe72557187dd1fe6e7e4449264dcf8033b285286d50f725be",
  "research/r075q_report-source.md" =>
    "b1fcfece0396b04ae9f59e42ef09957a422c36fa0843730a9fb22919bc24c600"
}.freeze
FIXTURES_SHA256 = "a0954f102de2fbc5ac5fb57fd68ba2ae084cc27743240fac6e3297b81d4410f5"
EXPECTED_SHA256 = "8f3e45bb4a62e2a5bd506fd3cc522610d59115f34411fd85b04c7b72081cb444"

MUTATION_GROUPS = {
  "allFrozenBindings" => %w[main_hash audit_hash source_hash dependency_hash],
  "fixtureExpectedBindings" => %w[fixture_hash expected_hash],
  "primaryAuditStatus" => %w[audit_pass audit_math_blocker audit_release_blocker audit_publish],
  "dependencyTableBindings" => %w[dep_b dep_l dep_n dep_p dep_role],
  "tagsReferencesDisplays" => %w[tag_missing tag_duplicate tag_gap reference display_open display_close aligned_pair],
  "utf8ControlAndTex" => %w[utf8 control bare_qquad qquad_count time_integral_line],
  "radialDerivativeRow" => %w[radial_outer radial_inner radial_volume radial_derivative radial_l1 radial_scale radial_chart radial_periodic_lift],
  "harmonicEquation" => %w[harmonic_real harmonic_integer harmonic_time harmonic_drift harmonic_transport harmonic_diffusion harmonic_sum harmonic_x1x3],
  "signedFluxCancellation" => %w[eta_range flux_outer_half square_half constant_row cancel_before_abs pre_time_quarter time_integral_upper flux_eighth ordinary_heat flux_fixture],
  "rectangleFibreGeometry" => %w[rectangle_side transverse_radius safe_radius a_condition chart_condition fibre_formula fibre_two_sided fibre_lower],
  "phaseUniformPeriodFloor" => %w[cos_period cos_integral phase_uniform period_count floor_direction floor_half kar_condition x2_lower],
  "spatialCollarMass" => %w[x3_length spatial_product spatial_delta spatial_a spatial_R all_times],
  "timeIntegralAndCBox" => %w[k2T time_three time_direction exp_three cbox_two cbox_nine cbox_pi mass_delta mass_a mass_R mass_k mass_A],
  "cubicInversionCombination" => %w[inverse_direction inverse_delta inverse_a inverse_R inverse_k inverse_M combine_delta combine_B combine_a combine_R_cancel combine_k combine_M],
  "normalizationScaleAndRate" => %w[payment_R payment_omega flux_R flux_omega norm_B norm_a norm_R norm_omega norm_k norm_p shear_scale frequency_scale after_L after_R after_omega rho cgamma rate_fraction rate_sign large_L],
  "conditionalVersionMLedger" => %w[ledger_full_window ledger_same_interval ledger_exterior ledger_weight ledger_coordinate_translation actual_component same_velocity pointwise_domination ledger_nonnegative ledger_direction projection_excluded arbitrary_realization realized_subclass sufficiently_large],
  "lowEntranceDiagnostic" => %w[entrance_E0 entrance_area entrance_ratio sigma_fixed sigma_lower sigma_upper sigma_strict entrance_limit not_hidden_P not_counterexample],
  "formulaSentinels" => %w[formula_q1 formula_q10 formula_q14 formula_q18 formula_q21 formula_q22 formula_q24 formula_q25 formula_q26 formula_q27 formula_q28],
  "sourceReportBoundary" => %w[source_primary_links source_titles source_adjacency source_no_import source_nonexhaustive source_no_novelty],
  "claimBoundary" => %w[one_harmonic constant_shear independent_x1x3 total_field projection_open multimode_open vertical_open low_packet_open nonconstant_open interpacket_open frequency_cap_open e24_open clock_open fixed_deletion_open weak_open regularity_open singularity_open novelty priority not_clay]
}.freeze
NEGATIVE_MUTATIONS = MUTATION_GROUPS.values.flatten.freeze

abort("unknown R075Q_RUBY_MUTATION: #{MUTATION}") unless MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
abort("duplicate mutation name in R0.75Q Ruby suite") unless NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

def digest(path)
  Digest::SHA256.file(path).hexdigest
end

def rat(value)
  Rational(value.to_s)
end

def rtext(value)
  value.denominator == 1 ? value.numerator.to_s : "#{value.numerator}/#{value.denominator}"
end

def flat(text)
  text.gsub(/\s+/, " ")
end

def all_fragments?(text, fragments)
  fragments.all? { |fragment| text.include?(fragment) }
end

def clean_bytes?(bytes)
  bytes.dup.force_encoding(Encoding::UTF_8).valid_encoding? &&
    bytes.bytes.none? { |b| (b < 32 && ![9, 10, 13].include?(b)) || b == 127 }
end

def guarded(name, result)
  result && !MUTATION_GROUPS.fetch(name).include?(MUTATION)
end

raw = File.binread(MAIN)
raw_primary = File.binread(PRIMARY)
raw_source = File.binread(SOURCE)
text = raw.force_encoding(Encoding::UTF_8)
primary = raw_primary.force_encoding(Encoding::UTF_8)
source = raw_source.force_encoding(Encoding::UTF_8)
flat_main = flat(text)
flat_primary = flat(primary)
flat_source = flat(source)
fixtures = JSON.parse(File.read(FIXTURES, encoding: "UTF-8"))
expected = JSON.parse(File.read(EXPECTED, encoding: "UTF-8"))
certificate = JSON.parse(File.read(CERTIFICATE, encoding: "UTF-8"))

frozen = FROZEN.dup
drift = {
  "main_hash" => "research/#{STEM}.md",
  "audit_hash" => "research/#{STEM}_primary_audit.md",
  "source_hash" => "research/r075q_report-source.md",
  "dependency_hash" => "research/r075l_single_harmonic_diffusive_signed_flux_gain.md"
}
frozen[drift[MUTATION]] = "0" * 64 if drift.key?(MUTATION)
bindings_ok = frozen.all? { |path, value| digest(File.join(ROOT, path)) == value }
fixture_hash = MUTATION == "fixture_hash" ? "0" * 64 : FIXTURES_SHA256
expected_hash = MUTATION == "expected_hash" ? "0" * 64 : EXPECTED_SHA256

g = fixtures.fetch("geometryCase")
a, d0, delta, radius, k, time, amp = %w[a delta0 delta R k T A].map { |key| rat(g.fetch(key)) }
outer = (a + delta) * radius
inner = (a - delta) * radius
shell_over_pi = Rational(4, 3) * (outer**3 - inner**3)
radial = {
  "outerRadius" => rtext(outer), "innerRadius" => rtext(inner),
  "shellVolumeOverPi" => rtext(shell_over_pi),
  "derivativeL1BoundOverPi" => rtext(shell_over_pi / radius),
  "benchmarkA2R2" => rtext(a * a * radius * radius),
  "centralChartCertified" => outer < Rational(3, 2)
}

harmonic = {
  "timeCoefficient" => "-k^2", "driftCoefficient" => "+k*B*sin",
  "transportCoefficient" => "-k*B*sin", "diffusionCoefficient" => "+k^2",
  "operatorSum" => "0"
}

f = fixtures.fetch("fluxCase")
f_a, f_b, f_k, vxi = %w[A absB k derivativeL1].map { |key| rat(f.fetch(key)) }
flux = {
  "outerHalf" => "1/2", "squareHalf" => "1/2", "constantRow" => "0",
  "preTimeFactor" => "1/4",
  "timeIntegralUpper" => rtext(Rational(1, 2) / (f_k * f_k)),
  "finalFactor" => "1/(8*k^2)",
  "fixtureBound" => rtext(f_a * f_a * f_b * vxi / (8 * f_k * f_k))
}

length = a * radius / 2
max_sq = a * a * radius * radius / 8
safe_sq = (a - 2 * d0)**2 * radius * radius
rectangle = {
  "maxTransverseRadiusSquared" => rtext(max_sq),
  "safeRadiusSquared" => rtext(safe_sq),
  "insideFibreSafeDisk" => max_sq <= safe_sq,
  "fibreLower" => rtext(4 * d0 * radius),
  "x2Length" => rtext(length), "x3Length" => rtext(length),
  "kTimesX2Length" => rtext(k * length), "completePeriods" => "1",
  "onePeriodIntegral" => rtext(Rational(4, 3) / k),
  "claimedX2LowerTimesPi" => rtext(a * radius / 3),
  "phaseUniform" => true,
  "spatialLowerTimesPi" => rtext(2 * d0 * a * a * radius**3 / 3)
}

mass_coeff = Rational(2, 9) * d0 * a * a * radius**3 * amp**3 / (k * k)
cubic = {
  "timeLower" => "(1-exp(-3))/(3*k^2)",
  "cBox" => "2*(1-exp(-3))/(9*pi)",
  "massLowerCoefficientWithoutExpOverPi" => rtext(mass_coeff),
  "massPowers" => {"delta0"=>"1", "a"=>"2", "R"=>"3", "k"=>"-2", "A"=>"3"},
  "inversePowers" => {"delta0"=>"-2/3", "a"=>"-4/3", "R"=>"-2", "k"=>"4/3", "M"=>"2/3"},
  "combinedPowers" => {"delta0"=>"-2/3", "absB"=>"1", "a"=>"2/3", "R"=>"0", "k"=>"-2/3", "M"=>"2/3"}
}

n = fixtures.fetch("normalizationCase")
rate = rat(n.fetch("rho")) / 6 - rat(n.fetch("cGamma")) / 12
normalization = {
  "beforeScaleBounds" => {"absB"=>"1", "a"=>"2/3", "R"=>"1/3", "omega"=>"1/3", "k"=>"-2/3", "p"=>"2/3"},
  "afterScaleBounds" => {"L"=>"2/3", "R"=>"-2/3", "omega"=>"1/3", "p"=>"2/3"},
  "exponentialRate" => rtext(rate), "strictlyNegative" => rate < 0
}

l = fixtures.fetch("ledgerCase")
l_r, omega, weight, field, other, measure, projected, cancelled =
  %w[R omega outerWeight F otherComponent tubeMeasure projectedPiece largerComponentAfterCancellation].map { |key| rat(l.fetch(key)) }
magnitude = 5.to_r
packet = l_r**-2 * omega * field**3 * measure
row = l_r**-2 * weight * magnitude**3 * measure
ledger = {
  "velocityMagnitude" => rtext(magnitude), "packetCubicIntegral" => rtext(packet),
  "versionMRowContribution" => rtext(row), "packetToRowRatio" => rtext(packet / row),
  "pointwiseDominated" => field <= magnitude,
  "projectionDominationValid" => projected <= cancelled.abs
}

e = fixtures.fetch("entranceCase")
e_a, e_r, e_amp, sigma = %w[a R A sigmaSample].map { |key| rat(e.fetch(key)) }
entrance = {
  "E0OverPiSquared" => rtext(2 * e_amp**2),
  "entranceUpperOverPi" => rtext(e_a**2 * e_r**2 * e_amp**2),
  "fractionUpperTimesPi" => rtext(e_a**2 * e_r**2 / 2),
  "sigmaSample" => rtext(sigma), "powerGap" => rtext(2 - sigma),
  "validForEveryFixedSigmaBelowTwo" => sigma >= 0 && sigma < 2
}

tags = text.scan(/\\tag\{Q\.(\d+)\}/).flatten.map(&:to_i)
mentions = text.scan(/Q\.(\d+)/).flatten.map(&:to_i)
structure_ok = tags == (1..28).to_a && tags.uniq.length == 28 &&
  mentions.all? { |x| tags.include?(x) } && text.scan(/\\\[/).length == 28 &&
  text.scan(/\\\]/).length == 28 && text.scan(/\\begin\{aligned\}/).length == 2 &&
  text.scan(/\\end\{aligned\}/).length == 2
controls_ok = clean_bytes?(File.binread(MAIN)) && clean_bytes?(File.binread(PRIMARY)) &&
  clean_bytes?(File.binread(SOURCE)) && !text.match?(/(?<!\\)qquad/) &&
  text.scan(/\\qquad/).length == 17 &&
  text.lines.any? { |line| line.include?("A^3\\int_0^T e^{-3k^2t}\\,dt\\\\") }

dependency_paths = FROZEN.keys.reject { |x| x.include?("r075q_") }
deps_ok = dependency_paths.all? { |path| text.include?(path) && text.include?(FROZEN.fetch(path)) }
primary_ok = all_fragments?(flat_primary, [
  "Verdict: **PASS**", "Mathematical blocker count: **0**",
  "Release blocker count: **0**", "does not authorize publication"
])
radial_text_ok = all_fragments?(flat_main, ["V_{\\xi,3}:=", "C_\\vartheta a^2R^2", "periodic lift", "No Wiener summation is needed"])
harmonic_text_ok = all_fragments?(flat_main, ["(\\partial_t+B\\partial_2-\\partial_2^2)F_k=0", "k\\in\\mathbb N", "independent of `x_1,x_3`"])
flux_text_ok = all_fragments?(flat_main, ["0<=eta<=1", "\\frac12\\int_0^T", "constant row vanishes", "absolute values only after that cancellation", "{8k^2}", "ordinary heat decay"])
rectangle_text_ok = all_fragments?(flat_main, ["aR/(2sqrt(2))<=(a-2delta_0)R", "\\ge4\\delta_0R", "a\\ge4\\delta_0"])
phase_text_ok = all_fragments?(flat_main, ["period `pi`", "\\frac43", "floor(k ell/pi)", "uniformly in the phase", "\\frac{aR}{3\\pi}", "\\frac{2\\delta_0a^2}{3\\pi}R^3"])
time_text_ok = all_fragments?(flat_main, ["k^2T>=1", "\\frac{2(1-e^{-3})}{9\\pi}", "\\delta_0a^2R^3k^{-2}A^3"])
inverse_text_ok = all_fragments?(flat_main, ["c_{\\rm box}^{-2/3}\\delta_0^{-2/3}", "a^{-4/3}R^{-2}k^{4/3}", "cancels the full `R^2`"])
normalization_text_ok = all_fragments?(flat_main, ["p_{k,\\rm col}:=R^{-2}\\omega M_{k,\\rm col}", "|B|a^{2/3}R^{1/3}\\omega^{1/3}k^{-2/3}", "L^{2/3}R^{-2/3}\\omega^{1/3}", "4279}{238140000}", "\\longrightarrow0"])
ledger_text_ok = all_fragments?(flat_main, ["`[0,T]` to lie in the same scale-`2R` exterior measurement interval", "weight is at least `omega`", "actual coordinate component", "same smooth velocity `v_R`", "`|F_k|<=|v_R|` pointwise", "nonnegativity of the exterior cubic row", "not asserted for a harmonic projection", "does not assert arbitrary zero-trajectory realization"])
entrance_text_ok = all_fragments?(flat_main, ["E_0=2\\pi^2A^2", "\\frac{a^2R^2}{2\\pi}", "For every fixed `0<=sigma<2`", "R^{2-\\sigma}\\longrightarrow0", "not a hidden use of P's entrance hypothesis"])
source_ok = all_fragments?(flat_source, ["arXiv:2603.14657", "arXiv:2410.05657", "arXiv:2103.07906", "arXiv:2101.05406", "10.1016/j.matpur.2019.04.009", "does not estimate Q's signed spherical-collar flux", "no observability theorem imported", "not a novelty or priority claim", "No citation graph or subscription-only exhaustive priority review"])
boundary_ok = all_fragments?(flat_main, ["one real harmonic", "constant shear", "independent of `x_1,x_3`", "total-field rather than packet-projection based", "Fourier or Littlewood--Paley projection", "two or more horizontal harmonics", "arbitrary vertical structure", "general low-entrance packet", "nonconstant shear", "inter-packet or low-difference summation", "total upper- frequency cap", "arbitrary-field E.24", "complete-clock extraction", "fixed deletion", "suitable-weak transfer", "regularity or singularity conclusion", "No novelty or priority claim", "NOT\\ CLAY"])

formula_ok = [1, 10, 14, 18, 21, 22, 24, 25, 26, 27, 28].all? { |number| text.include?("\\tag{Q.#{number}}") }
python_ok = certificate["schema"] == "r075q-spatially-spread-harmonic-collar-payment-certificate-v1" &&
  certificate["verdict"] == "PASS" && certificate["assertions"] == 20 &&
  certificate["passed"] == 20 && certificate["negativeMutations"] == NEGATIVE_MUTATIONS &&
  certificate["fixtureSha256"] == FIXTURES_SHA256 && certificate["expectedSha256"] == EXPECTED_SHA256 &&
  certificate.dig("checks", "normalizationScaleAndRate", "values", "exponentialRate") == "-4279/238140000" &&
  certificate.dig("checks", "conditionalVersionMLedger", "values", "projectionDominationValid") == false

checks = {
  "allFrozenBindings" => guarded("allFrozenBindings", bindings_ok),
  "fixtureExpectedBindings" => guarded("fixtureExpectedBindings", digest(FIXTURES) == fixture_hash && digest(EXPECTED) == expected_hash),
  "primaryAuditStatus" => guarded("primaryAuditStatus", primary_ok),
  "dependencyTableBindings" => guarded("dependencyTableBindings", deps_ok),
  "tagsReferencesDisplays" => guarded("tagsReferencesDisplays", structure_ok),
  "utf8ControlAndTex" => guarded("utf8ControlAndTex", controls_ok),
  "radialDerivativeRow" => guarded("radialDerivativeRow", radial == expected.fetch("radial") && radial_text_ok),
  "harmonicEquation" => guarded("harmonicEquation", harmonic == expected.fetch("harmonic") && harmonic_text_ok),
  "signedFluxCancellation" => guarded("signedFluxCancellation", flux == expected.fetch("flux") && flux_text_ok),
  "rectangleFibreGeometry" => guarded("rectangleFibreGeometry", rectangle["insideFibreSafeDisk"] && rectangle["fibreLower"] == expected.dig("rectangle", "fibreLower") && rectangle_text_ok),
  "phaseUniformPeriodFloor" => guarded("phaseUniformPeriodFloor", %w[kTimesX2Length completePeriods onePeriodIntegral claimedX2LowerTimesPi phaseUniform].all? { |key| rectangle[key] == expected.dig("rectangle", key) } && phase_text_ok),
  "spatialCollarMass" => guarded("spatialCollarMass", rectangle["spatialLowerTimesPi"] == expected.dig("rectangle", "spatialLowerTimesPi") && phase_text_ok),
  "timeIntegralAndCBox" => guarded("timeIntegralAndCBox", cubic["timeLower"] == expected.dig("cubic", "timeLower") && cubic["cBox"] == expected.dig("cubic", "cBox") && cubic["massLowerCoefficientWithoutExpOverPi"] == expected.dig("cubic", "massLowerCoefficientWithoutExpOverPi") && cubic["massPowers"] == expected.dig("cubic", "massPowers") && time_text_ok),
  "cubicInversionCombination" => guarded("cubicInversionCombination", cubic["inversePowers"] == expected.dig("cubic", "inversePowers") && cubic["combinedPowers"] == expected.dig("cubic", "combinedPowers") && inverse_text_ok),
  "normalizationScaleAndRate" => guarded("normalizationScaleAndRate", normalization == expected.fetch("normalization") && normalization_text_ok),
  "conditionalVersionMLedger" => guarded("conditionalVersionMLedger", ledger == expected.fetch("ledger") && ledger["pointwiseDominated"] && !ledger["projectionDominationValid"] && ledger_text_ok),
  "lowEntranceDiagnostic" => guarded("lowEntranceDiagnostic", entrance == expected.fetch("entrance") && entrance_text_ok),
  "formulaSentinels" => guarded("formulaSentinels", formula_ok),
  "sourceReportBoundary" => guarded("sourceReportBoundary", source_ok),
  "claimBoundary" => guarded("claimBoundary", boundary_ok),
  "pythonCertificateAgreement" => python_ok
}

passed = checks.values.count(true)
verdict = passed == checks.length ? "PASS" : "FAIL"
failed = checks.select { |_name, value| !value }.keys
lines = [
  "# R0.75Q independent finite audit", "",
  "- Verdict: **#{verdict}**",
  "- Blocker count: #{failed.length}",
  "- Assertions: #{passed}/#{checks.length}",
  "- Frozen main SHA-256: `#{FROZEN.fetch("research/#{STEM}.md")}`", "",
  "## Independent recomputation", "",
  "Ruby independently recomputed the radial shell row, one-harmonic PDE coefficients,",
  "the two 1/2 factors and 1/8 flux coefficient, the safe rectangle and exact fibre",
  "floor, the phase-uniform period count, the cubic mass/inversion powers, the frozen",
  "normalization rate `-4279/238140000`, the actual-component ledger direction, and",
  "the low-entrance ratio. Q.21 was inspected linewise: its first inequality explicitly",
  "contains the full time integral on one physical source line.", "",
  "## Scope", "",
  "The result is conditional on the same-velocity actual-component ledger alignment.",
  "It excludes projected larger fields and arbitrary realizations. Multimode, vertical,",
  "nonconstant-shear, E.24, complete-clock, fixed-deletion, suitable-weak, regularity,",
  "and singularity claims remain open. The bounded source report is adjacent context and",
  "is not novelty or priority evidence. **NOT CLAY.**", ""
]
unless failed.empty?
  lines += ["## Failed checks", ""] + failed.map { |name| "- #{name}" } + [""]
end
File.write(OUT_REPORT, lines.join("\n"), mode: "w", encoding: "UTF-8")
puts JSON.generate({suite: "R0.75Q-independent", verdict: verdict, assertions: checks.length, passed: passed, mutations: NEGATIVE_MUTATIONS.length})
exit(verdict == "PASS" ? 0 : 1)
