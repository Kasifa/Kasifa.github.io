#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent exact audit for R0.74T Step 19.
#
# This program does not import or invoke the Python producer.  It rebuilds
# the exponent ledger, finite Holder/time-floor proxies, fixed-deletion
# clocks, logarithmic threshold, and asynchronous-window algebra with Ruby
# Rational arithmetic.  Only after those checks does it inspect the primary
# JSON contract.  It does not machine-prove any continuous PDE input.

require "digest"
require "json"
require "set"

REPO = File.expand_path("..", __dir__)
NOTE = ENV.fetch(
  "R074T_DWELL_INDEPENDENT_NOTE",
  File.join(REPO, "research/r074t_schedule_invariant_dwell_coercivity.md")
)
LITERATURE = ENV.fetch(
  "R074T_DWELL_INDEPENDENT_LITERATURE",
  File.join(REPO, "research/r074t_schedule_invariant_literature_audit.md")
)
PRIMARY_JSON = ENV.fetch(
  "R074T_DWELL_INDEPENDENT_PRIMARY_JSON",
  File.join(REPO, "research/r074t_schedule_invariant_dwell_certificate.json")
)
REPORT = ENV.fetch(
  "R074T_DWELL_INDEPENDENT_REPORT",
  File.join(REPO, "research/r074t_schedule_invariant_dwell_independent_audit.md")
)

SCHEMA = "r074t-schedule-invariant-dwell-independent-v1"
MUTATION = ENV.fetch("R074T_DWELL_INDEPENDENT_MUTATION", "").strip
NOTE_SHA256 = ENV.fetch(
  "R074T_DWELL_EXPECTED_NOTE_SHA256",
  "8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd"
)
LITERATURE_SHA256 = ENV.fetch(
  "R074T_DWELL_EXPECTED_LITERATURE_SHA256",
  "60b49f6279c696a370af5f8050a6162753372eba81f8215e02e15259f084e88b"
)
EXPECTED_TAGS = (1..43).map { |number| "T.#{number}" }.freeze

DEPENDENCIES = {
  "r074e_version_m_payment" => [
    "research/r074e_local_mollified_frame_gate.md",
    "3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7"
  ],
  "r074f_packet_survival" => [
    "research/r074f_two_packet_survival.md",
    "0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb"
  ],
  "r074p_completed_clock" => [
    "research/r074p_temporal_observable_triage.md",
    "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867"
  ],
  "r074q_common_shear" => [
    "research/r074q_common_shear_multipacket_gate.md",
    "60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695"
  ],
  "r074q_relaxed_multipacket" => [
    "research/r074q_relaxed_multipacket_cubic_obstruction.md",
    "ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d"
  ],
  "r074s_fixed_deletion" => [
    "research/r074s_fixed_deletion_simultaneous_height.md",
    "305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1"
  ]
}.freeze

NEGATIVE_MUTATIONS = %w[
  gamma_weight_quarter_to_half
  gamma_exponent_sign
  two_thirds_to_half
  L_power_sign
  theta_power_sign
  holder_direction
  time_inf_to_sup
  survival_forall_to_exists
  min_to_max
  fixed_to_moving_deletion
  same_shell_allowed
  allow_signed_clocks
  K_floor_to_Hfix
  hstar_to_full_clock
  volume_upper_to_lower
  theta_bound_direction
  survival_defect_sign
  margin_sign
  async_qpre_sign
  async_interval_direction
  sum_overlapping_lobes
  tag_inventory
  claim_boundary
  source_hash
  literature_hash
  dependency_hash
  primary_schema
].freeze


def mutation?(name)
  MUTATION == name
end


def sha256(path)
  Digest::SHA256.file(path).hexdigest
end


def display_path(path)
  prefix = REPO + "/"
  path.start_with?(prefix) ? path.delete_prefix(prefix) : path
end


def exact_group(identifier)
  counter = { "cases" => 0 }
  verify = lambda do |condition, message|
    counter["cases"] += 1
    raise RuntimeError, message unless condition
  end
  details = yield verify
  {
    "id" => identifier,
    "cases" => counter.fetch("cases"),
    "details" => details,
    "pass" => true
  }
rescue StandardError => error
  {
    "id" => identifier,
    "cases" => counter.fetch("cases"),
    "error_class" => error.class.to_s,
    "error" => error.message,
    "pass" => false
  }
end


def add_vectors(*vectors)
  keys = vectors.flat_map(&:keys).uniq
  keys.to_h do |key|
    [key, vectors.sum(Rational(0, 1)) { |vector| vector.fetch(key, Rational(0, 1)) }]
  end.reject { |_key, value| value.zero? }
end


def scale_vector(vector, factor)
  vector.transform_values { |value| value * factor }.reject { |_key, value| value.zero? }
end


def deletion_sets(size, budget)
  indices = (0...size).to_a
  (0..[size, budget].min).flat_map do |count|
    indices.combination(count).map(&:to_set)
  end
end


def tail(row, deleted)
  row.each_with_index.sum(Rational(0, 1)) do |value, index|
    deleted.include?(index) ? Rational(0, 1) : value
  end
end


def fixed_height(matrix, budget)
  deletion_sets(matrix.first.length, budget).map do |deleted|
    matrix.map { |row| tail(row, deleted) }.max
  end.min
end


def moving_height(matrix, budget)
  sets = deletion_sets(matrix.first.length, budget)
  matrix.map { |row| sets.map { |deleted| tail(row, deleted) }.min }.max
end


GROUPS = []

GROUPS << exact_group("independent_atomic_exponent_ledger") do |verify|
  gamma_weight = mutation?("gamma_weight_quarter_to_half") ? Rational(1, 2) : Rational(1, 4)
  l_power = mutation?("L_power_sign") ? Rational(1, 2) : Rational(-1, 2)
  theta_power = mutation?("theta_power_sign") ? Rational(-1, 1) : Rational(1, 1)
  factors = [
    { "R" => Rational(-2, 1), "two" => Rational(-2, 1) },
    { "theta" => theta_power, "R" => Rational(3, 1) },
    { "Gamma" => gamma_weight },
    { "C_Omega" => Rational(-1, 2), "L" => l_power, "R" => Rational(-3, 2) },
    { "two" => Rational(3, 2), "R" => Rational(3, 2),
      "Gamma" => Rational(-3, 2), "h" => Rational(3, 2) },
    { "c_W" => Rational(1, 1) }
  ]
  raw = add_vectors(*factors)
  expected_raw = {
    "R" => Rational(1, 1), "two" => Rational(-1, 2),
    "theta" => Rational(1, 1), "Gamma" => Rational(-5, 4),
    "C_Omega" => Rational(-1, 2), "L" => Rational(-1, 2),
    "h" => Rational(3, 2), "c_W" => Rational(1, 1)
  }
  verify.call(raw == expected_raw, "raw monomial mismatch")

  power = mutation?("two_thirds_to_half") ? Rational(1, 2) : Rational(2, 3)
  powered = scale_vector(raw, power)
  powered["Gamma"] *= -1 if mutation?("gamma_exponent_sign")
  expected_powered = {
    "R" => Rational(2, 3), "two" => Rational(-1, 3),
    "theta" => Rational(2, 3), "Gamma" => Rational(-5, 6),
    "C_Omega" => Rational(-1, 3), "L" => Rational(-1, 3),
    "h" => Rational(1, 1), "c_W" => Rational(2, 3)
  }
  verify.call(powered == expected_powered, "powered Lambda monomial mismatch")

  h_power = raw.fetch("h")
  recovered = raw.dup
  recovered.delete("h")
  recovered = add_vectors(
    recovered,
    scale_vector(
      { "Gamma" => Rational(1, 1), "amplitude" => Rational(2, 1),
        "L" => Rational(1, 1), "R" => Rational(2, 1) },
      h_power
    )
  )
  verify.call(
    recovered.slice("theta", "amplitude", "Gamma", "L", "R") == {
      "theta" => Rational(1, 1), "amplitude" => Rational(3, 1),
      "Gamma" => Rational(1, 4), "L" => Rational(1, 1), "R" => Rational(4, 1)
    },
    "packet-amplitude recovery mismatch"
  )
  verify.call(Rational(1, 2) / Rational(1, 16) == 8, "robust constant square mismatch")
  verify.call(Rational(2, 1)**3 == 8, "powered exact constant mismatch")
  { "raw" => raw.transform_values(&:to_s), "powered" => powered.transform_values(&:to_s) }
end

GROUPS << exact_group("independent_perfect_power_grid") do |verify|
  roots = [Rational(1, 3), Rational(3, 5), Rational(4, 5), Rational(1, 1)]
  power = mutation?("two_thirds_to_half") ? Rational(1, 2) : Rational(2, 3)
  exponents = {
    "theta" => mutation?("theta_power_sign") ? Rational(-2, 3) : Rational(2, 3),
    "R" => power,
    "Gamma" => mutation?("gamma_exponent_sign") ? Rational(5, 6) : Rational(-5, 6),
    "L" => mutation?("L_power_sign") ? Rational(1, 3) : Rational(-1, 3),
    "h" => Rational(3, 2) * power
  }
  roots.repeated_permutation(5) do |q, r, g, ell, s|
    observed = Rational(2, 1)
    [[q, exponents["theta"]], [r, exponents["R"]],
     [g, exponents["Gamma"]], [ell, exponents["L"]],
     [s, exponents["h"]]].each do |root, exponent|
      integer = 24 * exponent
      verify.call(integer.denominator == 1, "nonintegral perfect-power exponent")
      observed *= root**integer.numerator
    end
    expected = 2 * q**16 * r**16 * g**-20 * ell**-8 * s**24
    verify.call(observed == expected, "perfect-power Lambda row mismatch")
  end
  nil
end

GROUPS << exact_group("independent_finite_holder_and_time_floor") do |verify|
  strict_holder = false
  strict_floor = false
  (1..5).each do |length|
    [0, 1, 2, 4].repeated_permutation(length) do |values|
      weights = length.times.map { |index| Rational(2 * index + 1, 1) }
      volume = weights.sum(Rational(0, 1))
      l2 = values.each_with_index.sum(Rational(0, 1)) { |value, i| weights[i] * value**2 }
      l3 = values.each_with_index.sum(Rational(0, 1)) { |value, i| weights[i] * value**3 }
      left = l3**2 * volume
      right = l2**3
      holder_relation = mutation?("holder_direction") ? left <= right : left >= right
      verify.call(holder_relation, "finite Holder direction failure")
      strict_holder ||= left > right

      floor = if mutation?("time_inf_to_sup") || mutation?("survival_forall_to_exists")
                values.max
              else
                values.min
              end
      predicted = volume * floor**3
      integral = l3
      verify.call(integral >= predicted, "time infimum-floor failure")
      strict_floor ||= integral > predicted
    end
  end
  verify.call(strict_holder, "no strict Holder row")
  verify.call(strict_floor, "no strict time-floor row")
  nil
end

GROUPS << exact_group("independent_two_clock_quantifiers") do |verify|
  equality = false
  [
    [[1, 0], [0, 2]],
    [[0, 3], [2, 0], [1, 1]],
    [[1, 0, 4], [0, 2, 1], [3, 0, 0]],
    [[2, 1, 0], [0, 0, 3]]
  ].each do |raw|
    matrix = raw.map { |row| row.map { |value| Rational(value, 1) } }
    shells = matrix.first.length
    shells.times.to_a.combination(2) do |k1, k2|
      matrix.each_index do |t1|
        matrix.each_index do |t2|
          h1 = matrix[t1][k1]
          h2 = matrix[t2][k2]
          next unless h1.positive? && h2.positive?

          target = mutation?("min_to_max") ? [h1, h2].max : [h1, h2].min
          observed = if mutation?("fixed_to_moving_deletion")
                       moving_height(matrix, 1)
                     else
                       fixed_height(matrix, 1)
                     end
          verify.call(observed >= target, "two-clock fixed-deletion failure")
          equality ||= observed == target
        end
      end
    end
  end
  if mutation?("same_shell_allowed")
    matrix = [[Rational(1, 1), Rational(0, 1)], [Rational(2, 1), Rational(0, 1)]]
    verify.call(fixed_height(matrix, 1) >= 1, "same-shell mutation exposed")
  end
  if mutation?("allow_signed_clocks")
    matrix = [[Rational(1, 1), Rational(-100, 1)],
              [Rational(-100, 1), Rational(1, 1)]]
    verify.call(fixed_height(matrix, 1) >= 1, "signed-clock mutation exposed")
  end
  verify.call(equality, "no equality witness")
  nil
end

GROUPS << exact_group("independent_illegal_replacement_witnesses") do |verify|
  rows = [
    { h: Rational(1, 1), l: Rational(1, 1), pi: Rational(1, 1), hf: Rational(0, 1) },
    { h: Rational(1, 1), l: Rational(1, 1), pi: Rational(0, 1), hf: Rational(1, 6) },
    { h: Rational(2, 1), l: Rational(20, 1), pi: Rational(20, 1), hf: Rational(0, 1) }
  ]
  rows.each do |row|
    verify.call(row[:l] >= row[:h], "missing lobe-floor witness")
    verify.call(row[:l] <= row[:pi] + 6 * row[:hf], "Step 18 bridge fixture invalid")
    if mutation?("K_floor_to_Hfix")
      verify.call(row[:hf] >= row[:h], "illegal Hfix replacement exposed")
    elsif mutation?("hstar_to_full_clock")
      verify.call(2 * row[:h] >= 2 * row[:l], "illegal full-clock replacement exposed")
    else
      verify.call(row[:hf] >= [Rational(0, 1), (row[:h] - row[:pi]) / 6].max,
                  "safe paid factor-six consequence failed")
    end
  end
  nil
end

GROUPS << exact_group("independent_volume_and_overlap_witnesses") do |verify|
  energy = Rational(4, 1)
  volume_cap = Rational(2, 1)
  actual_volume = mutation?("volume_upper_to_lower") ? Rational(8, 1) : Rational(1, 1)
  verify.call(actual_volume <= volume_cap, "volume cap direction exposed")
  verify.call(energy**3 / actual_volume >= energy**3 / volume_cap,
              "volume-controlled L3 lower bound failed")
  one_lobe = Rational(11, 1)
  claimed = mutation?("sum_overlapping_lobes") ? 2 * one_lobe : one_lobe
  verify.call(one_lobe >= claimed, "overlapping lobe double count exposed")
  nil
end

GROUPS << exact_group("independent_logarithmic_threshold") do |verify|
  c_gamma = Rational(8, 3969)
  a_s = Rational(75, 22528)
  rho = Rational(1, 320)
  margin = mutation?("margin_sign") ? a_s - 5 * c_gamma : 5 * c_gamma - a_s
  verify.call(margin == Rational(603_445, 89_413_632), "T.25 margin mismatch")
  verify.call(margin.positive?, "T.25 margin is not positive")
  d_sign = mutation?("survival_defect_sign") ? -1 : 1
  verify.call(d_sign == 1, "d_L sign mutation exposed")
  verify.call(a_s - rho == Rational(23, 112_640), "survival reserve mismatch")
  verify.call(5 * c_gamma - rho == Rational(8831, 1_270_080), "total reserve mismatch")

  [Rational(1, 1), Rational(4, 1), Rational(16, 1)].each do |l1sq|
    [Rational(1, 2), Rational(3, 1)].each do |d_l|
      [Rational(0, 1), Rational(2, 1)].each do |log_l2|
        [Rational(-1, 1), Rational(0, 1), Rational(2, 1)].each do |log_c|
          [Rational(0, 1), Rational(1, 3), Rational(5, 1)].each do |slack|
            ceiling = -margin * l1sq - d_l + log_l2 / 2 + Rational(3, 2) * log_c
            log_theta = ceiling - slack
            log_lambda = Rational(2, 3) * (log_theta + margin * l1sq + d_l - log_l2 / 2)
            direction = mutation?("theta_bound_direction") ? log_theta >= ceiling : log_theta <= ceiling
            verify.call(direction, "theta necessary-bound direction failure")
            verify.call(log_lambda <= log_c, "bounded-Lambda rearrangement failure")
          end
        end
      end
    end
  end
  nil
end

GROUPS << exact_group("independent_asynchronous_interval_algebra") do |verify|
  radii = [Rational(1, 50), Rational(1, 10), Rational(1, 5), Rational(3, 10)]
  radii << Rational(2, 5) if mutation?("async_interval_direction")
  radii.each do |r|
    left = 64 * r**2
    right = 65 * r**2
    j1 = [left + r**3, left + 2 * r**3]
    j2 = [right - r**3, right]
    verify.call(j1[1] - j1[0] == r**3, "J1 length mismatch")
    verify.call(j2[1] - j2[0] == r**3, "J2 length mismatch")
    verify.call(j1[0] > left && j1[1] < right, "J1 leaves terminal slab")
    verify.call(j2[0] > left && j2[1] <= right, "J2 leaves terminal slab")
    verify.call(j1[1] < j2[0], "unit-dwell intervals overlap")
    verify.call(j2[0] - j1[1] == r**2 * (1 - 3 * r), "interval gap mismatch")
  end
  [Rational(1, 128), Rational(3, 7), Rational(5, 1)].each do |b|
    [Rational(-4, 1), Rational(0, 1), Rational(7, 3)].each do |integral|
      q_pre = mutation?("async_qpre_sign") ? b * integral : -b * integral
      verify.call(q_pre + b * integral == 0, "terminal recentering sign failure")
    end
  end
  nil
end

GROUPS << exact_group("independent_source_and_literature_structure") do |verify|
  note = File.read(NOTE, encoding: "UTF-8")
  literature = File.read(LITERATURE, encoding: "UTF-8")
  tags = note.scan(/\\tag\{(T\.\d+)\}/).flatten
  expected = mutation?("tag_inventory") ? (1..44).map { |number| "T.#{number}" } : EXPECTED_TAGS
  verify.call(tags == expected, "equation tag order/range failure")
  verify.call(tags.uniq.length == tags.length, "duplicate equation tag")
  verify.call(note.scan('\\[').length == note.scan('\\]').length, "display imbalance")
  required = [
    "**NOT CLAY.**",
    "R074T_STEP19_STATUS_LOCAL_COERCIVITY_PROVED",
    "R074T_STEP19_STATUS_FULL_CLOCK_GATE_OPEN",
    "Nor may (T.17) be rewritten with",
    "arbitrary relative scheduling **inside the stated slab**",
    "**ABSTRACT SHARPNESS TESTS**"
  ]
  required << "MILLENNIUM PROBLEM SOLVED" if mutation?("claim_boundary")
  required.each { |phrase| verify.call(note.include?(phrase), "missing source boundary") }
  verify.call(!note.include?(",quad"), "malformed qquad token")
  verify.call(!note.include?("|le "), "malformed inequality token")
  urls = %w[
    https://arxiv.org/pdf/1101.5507
    https://arxiv.org/pdf/1706.02371
    https://arxiv.org/pdf/2101.05406
    https://arxiv.org/pdf/2207.06301
    https://arxiv.org/pdf/2212.08413
    https://arxiv.org/pdf/1101.2193
  ]
  urls.each { |url| verify.call(literature.include?(url), "missing primary-source URL") }
  verify.call(literature.include?("finite primary-source non-hit"), "missing bounded-search boundary")
  verify.call(literature.include?("does not prove novelty"), "missing novelty boundary")
  nil
end

GROUPS << exact_group("independent_hash_locks") do |verify|
  expected_note = mutation?("source_hash") ? "0" * 64 : NOTE_SHA256
  expected_literature = mutation?("literature_hash") ? "0" * 64 : LITERATURE_SHA256
  verify.call(sha256(NOTE) == expected_note, "Step 19 note hash mismatch")
  verify.call(sha256(LITERATURE) == expected_literature, "literature hash mismatch")
  DEPENDENCIES.each_with_index do |(_name, pair), index|
    relative, expected = pair
    expected = "0" * 64 if mutation?("dependency_hash") && index.zero?
    verify.call(sha256(File.join(REPO, relative)) == expected, "dependency hash mismatch")
  end
  nil
end

GROUPS << exact_group("independent_primary_certificate_contract") do |verify|
  payload = JSON.parse(File.read(PRIMARY_JSON, encoding: "UTF-8"))
  expected_schema = mutation?("primary_schema") ? "wrong-schema" : "r074t-schedule-invariant-dwell-certificate-v1"
  verify.call(payload.fetch("schema") == expected_schema, "primary schema mismatch")
  verify.call(payload.fetch("verdict") == "PASS", "primary certificate is not PASS")
  verify.call(payload.dig("note", "sha256") == NOTE_SHA256, "primary note hash mismatch")
  verify.call(payload.dig("literature", "sha256") == LITERATURE_SHA256,
              "primary literature hash mismatch")
  required = %w[
    atomic_raw_monomial_exponents
    two_thirds_monomial_exponents
    finite_weighted_Holder_proxy
    finite_time_infimum_floor_proxy
    two_clock_fixed_deletion_schedule_invariance
    functional_direction_and_no_illegal_replacement
    bounded_ratio_forces_theta_upper_bound
    asynchronous_window_and_recentering_algebra
  ]
  passed = payload.fetch("checks").select { |row| row.fetch("pass") }
                  .map { |row| row.fetch("id") }
  required.each { |identifier| verify.call(passed.include?(identifier), "missing primary check") }
  nil
end


verdict = GROUPS.all? { |group| group.fetch("pass") } ? "PASS" : "FAIL"
assertions = GROUPS.sum { |group| group.fetch("cases") }

lines = [
  "# R0.74T Step 19 independent Ruby audit",
  "",
  "- Schema: #{SCHEMA}",
  "- Source note: #{display_path(NOTE)}",
  "- Source SHA-256: #{sha256(NOTE)}",
  "- Literature SHA-256: #{sha256(LITERATURE)}",
  "- Independent groups: #{GROUPS.count { |group| group.fetch('pass') }}/#{GROUPS.length}",
  "- Exact assertions: #{assertions}",
  "",
  "## Verdict",
  "",
  "**#{verdict}**",
  "",
  "This Ruby audit independently reconstructs the finite exponent, Holder,",
  "time-floor, clock-quantifier, logarithmic, and asynchronous-window checks",
  "before reading the primary JSON contract.",
  "",
  "## Group inventory",
  "",
  "| Group | Result | Assertions |",
  "|---|---:|---:|"
]
GROUPS.each do |group|
  lines << "| #{group.fetch('id')} | #{group.fetch('pass') ? 'PASS' : 'FAIL'} | #{group.fetch('cases')} |"
end
lines += [
  "",
  "## Claim boundary",
  "",
  "- Finite cells do not machine-prove continuous Holder or the lobe theorem.",
  "- The K-clock floor yields only the explicit fixed-deletion witness h_*.",
  "- It cannot be replaced by the full completed clock or stopped-flux Hfix.",
  "- Exact common-shear evolution, survival, dominance, and shell placement remain analytic inputs.",
  "- The asynchronous construction is restricted to the inherited terminal slab.",
  "- No full clock estimate, regularity theorem, or Clay claim is certified.",
  "",
  "## Failures",
  ""
]
failed = GROUPS.reject { |group| group.fetch("pass") }
if failed.empty?
  lines << "None."
else
  failed.each do |group|
    lines << "- #{group.fetch('id')}: #{group.fetch('error', 'unknown failure')}"
  end
end
lines << ""

File.write(REPORT, lines.join("\n"), mode: "w", encoding: "UTF-8")
puts JSON.generate(
  "schema" => SCHEMA,
  "verdict" => verdict,
  "groups_passed" => GROUPS.count { |group| group.fetch("pass") },
  "groups_total" => GROUPS.length,
  "assertions" => assertions,
  "mutation" => MUTATION.empty? ? nil : MUTATION
)
exit(verdict == "PASS" ? 0 : 1)
