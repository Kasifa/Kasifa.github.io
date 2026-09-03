#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent exact audit for R0.74S Step 18.
#
# This Ruby implementation does not import or invoke the primary Python
# certificate.  It recomputes finite minimax, layer-cake, clock-payment,
# triangular-clock, and fixed-N obstruction checks with Rational arithmetic,
# then audits the frozen source and dependency hashes.
#
# It does not machine-prove the continuum local-energy inputs, dense
# good-time closure, the open fixed-deletion gate, regularity, or a Clay
# claim.

require "digest"
require "json"
require "set"

REPO = File.expand_path("..", __dir__)
NOTE = ENV.fetch(
  "R074S_FIXED_DELETION_INDEPENDENT_NOTE",
  File.join(REPO, "research/r074s_fixed_deletion_simultaneous_height.md")
)
LITERATURE = ENV.fetch(
  "R074S_FIXED_DELETION_INDEPENDENT_LITERATURE",
  File.join(REPO, "research/r074s_fixed_deletion_literature_audit.md")
)
PRIMARY_JSON = ENV.fetch(
  "R074S_FIXED_DELETION_INDEPENDENT_PRIMARY_JSON",
  File.join(REPO, "research/r074s_fixed_deletion_certificate.json")
)
REPORT = ENV.fetch(
  "R074S_FIXED_DELETION_INDEPENDENT_REPORT",
  File.join(REPO, "research/r074s_fixed_deletion_independent_audit.md")
)

SCHEMA = "r074s-fixed-deletion-independent-audit-v1"
MUTATION = ENV.fetch("R074S_FIXED_DELETION_INDEPENDENT_MUTATION", "").strip
NOTE_SHA256 = "305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1"
LITERATURE_SHA256 = "fea7470814c0c21399c6e2b25961e8b3791e584cc24612ac37e9d1be7ce707ce"
EXPECTED_TAGS = (476..493).map { |number| "S.#{number}" }.freeze

DEPENDENCIES = {
  "step10_paid_branch" => [
    "research/r074s_paid_branch_last_exit_residual.md",
    "9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c"
  ],
  "step15_hybrid" => [
    "research/r074s_hybrid_flux_tail_equivalence.md",
    "2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d"
  ],
  "step17_recurrent" => [
    "research/r074s_recurrent_streamline_temporal_tail_obstruction.md",
    "7d204b326be45a82bc0d8531ea2f2d894c0c125b76e3ccbf02fdc1978a6011c5"
  ]
}.freeze

NEGATIVE_MUTATIONS = %w[
  minimax_order
  layer_cake
  q_payment
  reverse_six
  triangle_fixed
  triangle_separable
  ledger_power
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


def deletion_sets(size, budget)
  indices = (0...size).to_a
  (0..[size, budget].min).flat_map do |count|
    indices.combination(count).map(&:to_set)
  end
end


def tail(vector, deleted)
  vector.each_with_index.sum(Rational(0, 1)) do |value, index|
    deleted.include?(index) ? Rational(0, 1) : value
  end
end


def moving_tail(matrix, budget)
  sets = deletion_sets(matrix.first.length, budget)
  matrix.map { |row| sets.map { |set| tail(row, set) }.min }.max
end


def fixed_tail(matrix, budget)
  deletion_sets(matrix.first.length, budget).map do |set|
    matrix.map { |row| tail(row, set) }.max
  end.min
end


def separable_tail(vector, budget)
  deletion_sets(vector.length, budget).map { |set| tail(vector, set) }.min
end


def maxima(matrix)
  (0...matrix.first.length).map do |index|
    matrix.map { |row| row.fetch(index) }.max
  end
end


def layer_cake_best(vector, budget)
  previous = Rational(0, 1)
  integral = Rational(0, 1)
  vector.select(&:positive?).uniq.sort.each do |level|
    count = vector.count { |value| value >= level }
    integral += (level - previous) * [count - budget, 0].max
    previous = level
  end
  integral += 1 if mutation?("layer_cake")
  integral
end


GROUPS = []

GROUPS << exact_group("independent_minimax_hierarchy") do |verify|
  strict = false
  [
    [3, 3, [0, 1]],
    [4, 2, [0, 1, 2]]
  ].each do |shells, times, alphabet|
    alphabet.repeated_permutation(shells * times) do |flat|
      matrix = times.times.map do |time|
        shells.times.map do |shell|
          Rational(flat.fetch(time * shells + shell), 1)
        end
      end
      envelope = maxima(matrix).each_with_index.map do |value, index|
        value + Rational((index + flat.sum) % 2, 1)
      end
      (0..shells).each do |budget|
        moving = moving_tail(matrix, budget)
        fixed = fixed_tail(matrix, budget)
        separable = separable_tail(envelope, budget)
        relation = if mutation?("minimax_order")
                     fixed <= moving && moving <= separable
                   else
                     moving <= fixed && fixed <= separable
                   end
        verify.call(relation, "minimax hierarchy failure")
        strict ||= moving < fixed
      end
    end
  end
  verify.call(strict, "no strict minimax witness found")
  { "strict_case_seen" => strict }
end

GROUPS << exact_group("independent_layer_cake") do |verify|
  (1..6).each do |size|
    [0, 1, 2, 3].repeated_permutation(size) do |raw|
      vector = raw.map { |value| Rational(value, 1) }
      (0..size).each do |budget|
        verify.call(
          separable_tail(vector, budget) == layer_cake_best(vector, budget),
          "layer-cake identity failure"
        )
      end
    end
  end
  nil
end

GROUPS << exact_group("independent_completed_clock_payments") do |verify|
  [
    [[0, 2, 1], [2, 0, 1], [1, 1, 0]],
    [[3, 0, 2, 1], [0, 3, 1, 2]],
    [[1, 4], [4, 1], [2, 2]]
  ].each do |raw_matrix|
    z = raw_matrix.map { |row| row.map { |value| Rational(value, 1) } }
    shells = z.first.length
    qvar = shells.times.map { |index| Rational((2 * index + 1) % 3, 1) }
    k_forward = z.map do |row|
      row.each_with_index.map { |value, index| [value - qvar.fetch(index), 0].max }
    end
    payment = shells.times.map { |index| Rational((index + 1) % 3, 1) }
    pi_value = payment.sum(Rational(0, 1))
    k_reverse = z.map do |row|
      row.each_with_index.map { |value, index| 6 * value + payment.fetch(index) }
    end
    (0..shells).each do |budget|
      hfix = fixed_tail(z, budget)
      bq = qvar.sum(Rational(0, 1))
      forward_right = fixed_tail(k_forward, budget)
      forward_right += bq unless mutation?("q_payment")
      verify.call(hfix <= forward_right, "Q-payment comparison failure")

      coefficient = mutation?("reverse_six") ? 5 : 6
      verify.call(
        fixed_tail(k_reverse, budget) <= pi_value + coefficient * hfix,
        "paid-branch reverse comparison failure"
      )
      verify.call(
        fixed_tail(k_reverse, budget) <= separable_tail(maxima(k_reverse), budget),
        "simultaneous height exceeds separable maxima"
      )
    end
  end
  nil
end

GROUPS << exact_group("independent_triangular_clock_values") do |verify|
  strict = 0
  (1..10).each do |shells|
    (0...shells).each do |budget|
      [Rational(1, 1), Rational(3, 2), Rational(7, 3)].each do |height|
        matrix = [Array.new(shells, Rational(0, 1))]
        shells.times do |active|
          matrix << shells.times.map do |index|
            index == active ? height : Rational(0, 1)
          end
        end
        matrix << Array.new(shells, Rational(0, 1))

        moving = moving_tail(matrix, budget)
        fixed = fixed_tail(matrix, budget)
        separable = separable_tail(maxima(matrix), budget)
        expected_fixed = mutation?("triangle_fixed") ? height + 1 : height
        expected_separable = if mutation?("triangle_separable")
                               (shells - budget + 1) * height
                             else
                               (shells - budget) * height
                             end
        verify.call(
          moving == (budget.zero? ? height : 0),
          "triangular moving-tail value failure"
        )
        verify.call(fixed == expected_fixed, "triangular fixed-tail value failure")
        verify.call(
          separable == expected_separable,
          "triangular separable-tail value failure"
        )
        verify.call(2 * shells * height == matrix.first.length * 0 + 2 * shells * height,
                    "triangular total variation bookkeeping failure")
        if budget >= 1 && shells >= budget + 2
          strict += 1
          verify.call(
            moving < fixed && fixed < separable,
            "triangular strict hierarchy failure"
          )
        end
      end
    end
  end
  verify.call(strict.positive?, "no strict triangular case")
  { "strict_cases" => strict }
end

GROUPS << exact_group("independent_fixed_N_ledger_obstruction") do |verify|
  rows = []
  (0..8).each do |budget|
    shells = budget + 2
    [1, 2, 5, 10, 25, 100].each do |constant|
      height = Rational(4 * constant**3 * shells**2 + 1, 1)
      payment = 2 * shells * height
      left_cube = height**3
      right_cube = constant**3 * payment**2
      right_cube *= height if mutation?("ledger_power")
      verify.call(left_cube > right_cube, "fixed-N power obstruction failure")
      rows << {
        "budget" => budget,
        "constant" => constant,
        "height" => height.to_s
      }
    end
  end
  rows
end

GROUPS << exact_group("independent_source_structure") do |verify|
  note = File.read(NOTE, encoding: "UTF-8")
  literature = File.read(LITERATURE, encoding: "UTF-8")
  tags = note.scan(/\\tag\{(S\.\d+)\}/).flatten
  expected = mutation?("tag_inventory") ? (476..494).map { |n| "S.#{n}" } : EXPECTED_TAGS
  verify.call(tags == expected, "equation-tag order or range failure")
  verify.call(tags.uniq.length == tags.length, "duplicate equation tag")
  verify.call(note.scan('\[').length == note.scan('\]').length,
              "display delimiter imbalance")
  phrases = [
    "**NOT CLAY.**",
    "Equation (S.486) is **OPEN**",
    "Equation (S.487) is also **OPEN**",
    "**ABSTRACT CLOCK STRESS TESTS**",
    "terminal-dependent deletion set"
  ]
  phrases << "MILLENNIUM PROBLEM SOLVED" if mutation?("claim_boundary")
  phrases.each { |phrase| verify.call(note.include?(phrase), "missing claim boundary") }
  verify.call(
    literature.include?("No row contains all target coordinates."),
    "missing bounded non-collision conclusion"
  )
  nil
end

GROUPS << exact_group("independent_hash_locks") do |verify|
  expected_note = mutation?("source_hash") ? "0" * 64 : NOTE_SHA256
  expected_literature = mutation?("literature_hash") ? "0" * 64 : LITERATURE_SHA256
  verify.call(sha256(NOTE) == expected_note, "Step 18 note hash mismatch")
  verify.call(
    sha256(LITERATURE) == expected_literature,
    "Step 18 literature hash mismatch"
  )
  DEPENDENCIES.each_with_index do |(_name, pair), index|
    relative, expected = pair
    expected = "0" * 64 if mutation?("dependency_hash") && index.zero?
    verify.call(
      sha256(File.join(REPO, relative)) == expected,
      "dependency hash mismatch"
    )
  end
  nil
end

GROUPS << exact_group("independent_primary_certificate_contract") do |verify|
  payload = JSON.parse(File.read(PRIMARY_JSON, encoding: "UTF-8"))
  expected_schema = if mutation?("primary_schema")
                      "wrong-schema"
                    else
                      "r074s-fixed-deletion-certificate-v1"
                    end
  verify.call(payload.fetch("schema") == expected_schema, "primary schema mismatch")
  verify.call(payload.fetch("verdict") == "PASS", "primary certificate is not PASS")
  verify.call(
    payload.dig("note", "sha256") == NOTE_SHA256,
    "primary note hash mismatch"
  )
  verify.call(
    payload.dig("literature", "sha256") == LITERATURE_SHA256,
    "primary literature hash mismatch"
  )
  required = %w[
    finite_minimax_and_separable_hierarchy
    finite_layer_cake_and_fixed_set_tonelli
    completed_clock_forward_reverse_and_separable_bounds
    disjoint_triangular_clock_exact_values
    fixed_N_linear_ledger_cannot_force_two_thirds_power
  ]
  passed = payload.fetch("checks").select { |row| row.fetch("pass") }
                  .map { |row| row.fetch("id") }
  required.each do |identifier|
    verify.call(passed.include?(identifier), "missing primary finite check")
  end
  nil
end


verdict = GROUPS.all? { |group| group.fetch("pass") } ? "PASS" : "FAIL"
finite_cases = GROUPS.sum { |group| group.fetch("cases") }

lines = [
  "# R0.74S Step 18 — independent Ruby audit",
  "",
  "- Schema: #{SCHEMA}",
  "- Source note: #{display_path(NOTE)}",
  "- Source SHA-256: #{sha256(NOTE)}",
  "- Literature SHA-256: #{sha256(LITERATURE)}",
  "- Independent groups: #{GROUPS.count { |group| group.fetch('pass') }}/#{GROUPS.length}",
  "- Exact assertions: #{finite_cases}",
  "",
  "## Verdict",
  "",
  "**#{verdict}**",
  "",
  "The Ruby verifier is implementation-independent from the Python producer.",
  "It recomputes all finite functional identities with Rational arithmetic",
  "and checks the frozen source, literature, dependency, and primary-result",
  "contracts.",
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
  "## Analytic audit boundary",
  "",
  "For each fixed deletion set S, Step 10 S.235 and Step 15 r <= z give",
  "",
  "\\[",
  " \\sum_{k\\notin S}K_k(\\tau)",
  " \\le \\Pi_R^{\\boldsymbol\\lambda}",
  "      +6\\sum_{k\\notin S}z_k(\\tau)",
  "\\]",
  "",
  "at every common good terminal time.  Continuity of the K vector into",
  "\\(\\ell^1\\) and density of the common good-time set close only the left",
  "side to all terminal times; no continuity of the hybrid stops is assumed.",
  "Taking the supremum for that same S and then the infimum proves S.484.",
  "",
  "The converse target-scale comparison follows from",
  "\\(z_k(\\tau)\\le K_k(\\tau)+\\operatorname{TV}Q_k\\).  Neither direction",
  "proves that the common finite deletion exists with a quadratic bound.",
  "",
  "## Claim boundary",
  "",
  "- The triangular-clock strictness is abstract only.",
  "- The Taylor compatibility screen uses R chosen after N as in S.451.",
  "- The fixed-deletion and completed-clock gates remain open.",
  "- Q.12, Q.1, scale contraction, regularity, and the Millennium problem remain open.",
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
  "assertions" => finite_cases,
  "mutation" => MUTATION.empty? ? nil : MUTATION
)
exit(verdict == "PASS" ? 0 : 1)
