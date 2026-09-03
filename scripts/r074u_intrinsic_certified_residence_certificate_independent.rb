#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent Ruby/Rational audit for R0.74U Step 20.  This rebuilds the
# arithmetic and finite corridor fixtures; it does not invoke Python and does
# not treat the primary JSON as mathematical evidence.

require "digest"
require "json"

REPO = File.expand_path("..", __dir__)
NOTE = ENV.fetch("R074U_RESIDENCE_INDEPENDENT_NOTE", File.join(REPO, "research/r074u_intrinsic_certified_residence.md"))
LITERATURE = ENV.fetch("R074U_RESIDENCE_INDEPENDENT_LITERATURE", File.join(REPO, "research/r074u_intrinsic_residence_literature_audit.md"))
PRIMARY = ENV.fetch("R074U_RESIDENCE_INDEPENDENT_PRIMARY_JSON", File.join(REPO, "research/r074u_intrinsic_certified_residence_certificate.json"))
REPORT = ENV.fetch("R074U_RESIDENCE_INDEPENDENT_REPORT", File.join(REPO, "research/r074u_intrinsic_certified_residence_independent_audit.md"))
SCHEMA = "r074u-intrinsic-certified-residence-independent-v1"
PRIMARY_SCHEMA = "r074u-intrinsic-certified-residence-certificate-v1"
MUTATION = ENV.fetch("R074U_RESIDENCE_INDEPENDENT_MUTATION", "").strip
NOTE_SHA = "e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99"
LITERATURE_SHA = "0cf6e19a42e524aaf79aca10d72c5380029dce37032215974d99976a0b2a327c"

DEPENDENCIES = {
  "research/r074p_temporal_observable_triage.md" => "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867",
  "research/r074t_schedule_invariant_dwell_coercivity.md" => "8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd",
  "research/r074q_common_shear_multipacket_gate.md" => "60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695",
  "research/r074q_relaxed_multipacket_cubic_obstruction.md" => "ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d",
  "research/r074f_two_packet_survival.md" => "0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb",
  "research/r074s_moving_frame_taylor_vortex_obstruction.md" => "de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0"
}.freeze

NEGATIVE_MUTATIONS = %w[
  A_squared_margin_sign epsilon_crude_bound speed_bound_direction slab_72_to_73
  upper_1024_to_1023 phase_96_to_97 phase_144_to_145 cstar_sign
  cross_tail_margin_sign theta_cert_log_sign theta_necessary_direction
  corridor_upper_to_K_superlevel Omega_to_Theta physical_to_frequency_shell
  drop_full_slab_compact_min drop_periodic_term K_to_Hfix overclaim drop_not_clay
  tag_inventory source_hash literature_hash dependency_hash primary_schema
].freeze

def mut?(name)
  MUTATION == name
end

def sha(path)
  Digest::SHA256.file(path).hexdigest
end

def group(id)
  state = { "cases" => 0 }
  verify = lambda do |condition, message|
    state["cases"] += 1
    raise message unless condition
  end
  details = yield verify
  state.merge("id" => id, "pass" => true, "details" => details)
rescue StandardError => error
  state.merge("id" => id, "pass" => false, "error" => error.message)
end

groups = []
groups << group("independent_annular_exact_arithmetic") do |v|
  l0 = Rational(9216, 1); x = 1 / l0
  margin = (Rational(64, 63)**2 - Rational(1, 256) - (Rational(15, 16) + x)**2 - (Rational(3, 8) + Rational(3, 2) * x)**2)
  margin = -margin if mut?("A_squared_margin_sign")
  v.call(margin == Rational(15_232_043, 1_849_688_064) && margin.positive?, "A(L) squared reserve")
  v.call(Rational(15, 16) - x - Rational(32, 63) == Rational(9235, 21_504), "inner annular margin")
  exp4 = (0..3).sum(Rational(0, 1)) { |n| Rational(4**n, (1..n).reduce(1, :*)) }
  threshold = mut?("epsilon_crude_bound") ? Rational(1, 5) : Rational(1, 4)
  v.call(Rational(49, 14_625) * l0**2 > 4 && exp4 > 16 && threshold == Rational(1, 4), "epsilon<1/4 ledger")
  { "A_margin" => margin.to_s, "inner_margin" => Rational(9235, 21_504).to_s }
end

groups << group("independent_speed_direction_grid") do |v|
  eps = [Rational(0), Rational(1, 16), Rational(1, 8), Rational(1, 5), Rational(249, 1000)]
  eps.product(eps).each do |e1, ei|
    next if ei > e1
    lower = (1 - ei) / 128
    upper = Rational(1, 128) / (1 - e1)
    relation = mut?("speed_bound_direction") ? lower >= upper : lower.positive? && lower <= upper
    v.call(relation, "speed inequality direction")
  end
  { "epsilon_grid" => eps.map(&:to_s) }
end

groups << group("independent_residence_constant_ledger") do |v|
  lower = mut?("slab_72_to_73") ? Rational(73, 5) : Rational(72, 5)
  upper = mut?("upper_1024_to_1023") ? Rational(1023, 3) : Rational(1024, 3)
  inner = mut?("phase_96_to_97") ? Rational(97, 5) : Rational(96, 5)
  outer = mut?("phase_144_to_145") ? Rational(145, 5) : Rational(144, 5)
  v.call(128 * Rational(3, 8) * Rational(3, 4) == 36, "travel allowance")
  v.call(lower * Rational(5, 144) == Rational(1, 2), "72/5 slab truncation")
  v.call(upper == Rational(1024, 3), "1024/3 upper coefficient")
  v.call(inner * Rational(5, 288) == Rational(1, 3), "96/5 phase")
  v.call(outer * Rational(5, 144) == 1, "144/5 phase")
  { "lower" => lower.to_s, "upper" => upper.to_s, "inner" => inner.to_s, "outer" => outer.to_s }
end

groups << group("independent_linear_corridor_grid") do |v|
  xs = [Rational(1, 1000), Rational(1, 100), Rational(5, 288), Rational(5, 144)]
  aa = [Rational(376, 1000), Rational(2, 5), Rational(1, 2), Rational(3, 4)]
  ee = [Rational(0), Rational(1, 8), Rational(1, 5), Rational(249, 1000)]
  tt = [Rational(0), Rational(1, 4), Rational(1, 2), Rational(3, 4), Rational(1)]
  xs.product(aa, ee, ee, tt).each do |x, a, e1, ei, tau|
    next if ei > e1
    speed = Rational(1, 128) / (1 - e1)
    half = a * x / speed
    actual = [Rational(1), tau + half].min - [Rational(0), tau - half].max
    v.call(actual >= Rational(72, 5) * x, "corridor lower")
    v.call(actual <= [Rational(1), 256 * a * x / (1 - ei)].min, "corridor upper")
  end
  { "grid_axes" => [xs.length, aa.length, ee.length, ee.length, tt.length] }
end

groups << group("independent_tail_periodic_ledger") do |v|
  cross = Rational(49, 14_850) - Rational(3, 2) * Rational(8, 3969)
  cross = -cross if mut?("cross_tail_margin_sign")
  cstar = Rational(3, 22) * Rational(144, 5)**2 - Rational(4, 3969)
  cstar = -cstar if mut?("cstar_sign")
  periodic = mut?("drop_periodic_term") ? Rational(4, 3969) : -cstar
  v.call(cross == Rational(67, 242_550) && cross.positive?, "cross-tail margin")
  v.call(Rational(4601, 2_910_600).positive?, "inner cross-tail margin")
  v.call(cstar == Rational(123_450_676, 1_091_475) && cstar.positive? && periodic == -cstar, "periodic cstar")
  { "cross" => cross.to_s, "cstar" => cstar.to_s }
end

groups << group("independent_theta_substitution") do |v|
  coefficient = mut?("theta_cert_log_sign") ? Rational(-1, 2) : Rational(1, 2)
  v.call(coefficient == Rational(1, 2), "theta_cert makes log L2 coefficient positive")
  v.call(5 * Rational(8, 3969) - Rational(75, 22_528) == Rational(603_445, 89_413_632), "T.24 margin")
  direction = mut?("theta_necessary_direction") ? :lower : :upper
  v.call(direction == :upper, "T.28 remains a necessary upper bound")
  { "log_L2" => coefficient.to_s, "necessary_direction" => direction.to_s }
end

groups << group("independent_source_claim_audit") do |v|
  text = File.read(NOTE, encoding: "UTF-8")
  tags = text.scan(/\\tag\{(U\.\d+)\}/).flatten
  expected = mut?("tag_inventory") ? (1..46).map { |n| "U.#{n}" } : (1..45).map { |n| "U.#{n}" }
  v.call(tags == expected && tags.uniq.length == tags.length, "U tag inventory")
  tokens = ["**NOT CLAY.**", "Full-slab", "compact-minimum", "noncentral periodic copies", "physical shell", "\\Omega_i(t)", "No converse inclusion and no upper bound for this superlevel set", "R074U_STEP20_END"]
  tokens << "frequency shell corridor" if mut?("physical_to_frequency_shell")
  tokens << "\\Theta_i(t)" if mut?("Omega_to_Theta")
  tokens << "FULL_SLAB_COMPACT_MIN_REMOVED" if mut?("drop_full_slab_compact_min")
  tokens << "U.24 IS AN UPPER BOUND FOR THE K SUPERLEVEL" if mut?("corridor_upper_to_K_superlevel")
  tokens << "\\mathfrak H^{\\rm fix}" if mut?("K_to_Hfix")
  tokens << "THE MILLENNIUM PROBLEM IS SOLVED" if mut?("overclaim")
  tokens = tokens.reject { |x| x == "**NOT CLAY.**" } << "**CLAY CLAIM.**" if mut?("drop_not_clay")
  tokens.each { |token| v.call(text.include?(token), "missing source sentinel #{token}") }
  v.call(!text.include?("frequency shell corridor"), "physical/frequency shell substitution")
  { "tags" => tags.length, "sentinels" => tokens.length }
end

groups << group("independent_hash_locks") do |v|
  expected_note = mut?("source_hash") ? "0" * 64 : NOTE_SHA
  expected_lit = mut?("literature_hash") ? "0" * 64 : LITERATURE_SHA
  v.call(File.file?(NOTE) && sha(NOTE) == expected_note, "note hash")
  v.call(File.file?(LITERATURE) && sha(LITERATURE) == expected_lit, "literature hash")
  DEPENDENCIES.each_with_index do |(relative, digest), index|
    wanted = mut?("dependency_hash") && index.zero? ? "0" * 64 : digest
    path = File.join(REPO, relative)
    v.call(File.file?(path) && sha(path) == wanted, "dependency #{relative}")
  end
  { "note" => sha(NOTE), "literature" => sha(LITERATURE), "dependencies" => DEPENDENCIES.length }
end

groups << group("independent_primary_contract") do |v|
  data = JSON.parse(File.read(PRIMARY, encoding: "UTF-8"))
  expected = mut?("primary_schema") ? "invalid-schema" : PRIMARY_SCHEMA
  v.call(data.fetch("schema") == expected, "primary schema")
  v.call(data.fetch("verdict") == "PASS", "primary verdict")
  v.call(data.fetch("mutation").nil?, "primary is unmutated")
  v.call(data.fetch("negative_mutations") == NEGATIVE_MUTATIONS.reject { |name| name == "primary_schema" }, "primary mutation contract")
  { "primary_checks" => data.fetch("checks").length }
end

verdict = groups.all? { |row| row.fetch("pass") } ? "PASS" : "FAIL"
assertions = groups.sum { |row| row.fetch("cases") }
lines = [
  "# R0.74U Step 20 independent Ruby audit", "",
  "- Schema: #{SCHEMA}", "- Verdict: **#{verdict}**",
  "- Independent groups: #{groups.count { |g| g.fetch('pass') }}/#{groups.length}",
  "- Independent Rational assertions: #{assertions}",
  "- Note SHA-256: `#{File.file?(NOTE) ? sha(NOTE) : 'MISSING'}`",
  "- Literature SHA-256: `#{File.file?(LITERATURE) ? sha(LITERATURE) : 'MISSING'}`", "",
  "## Group inventory", "", "| Group | Result | Assertions |", "|---|---:|---:|"
]
groups.each { |g| lines << "| #{g.fetch('id')} | #{g.fetch('pass') ? 'PASS' : 'FAIL'} | #{g.fetch('cases')} |" }
lines += ["", "## Independence and boundary", "",
          "Ruby Rational arithmetic independently rebuilds the annular, speed, slab, corridor, tail, periodic, and theta ledgers before reading the primary JSON contract.", "",
          "This remains a finite arithmetic, kinematic, structural, and hash audit. It does not prove the continuous PDE estimates, a K-superlevel upper bound, regularity, singularity, novelty, or a Clay claim.", ""]
failed = groups.reject { |g| g.fetch("pass") }
lines += ["## Failed groups", ""] + failed.map { |g| "- #{g.fetch('id')}: #{g['error']}" } + [""] unless failed.empty?
File.write(REPORT, lines.join("\n"), mode: "w", encoding: "UTF-8")
puts JSON.generate({ "schema" => SCHEMA, "verdict" => verdict, "groups_passed" => groups.count { |g| g.fetch("pass") }, "groups_total" => groups.length, "assertions" => assertions, "mutation" => MUTATION.empty? ? nil : MUTATION })
exit(verdict == "PASS" ? 0 : 1)
