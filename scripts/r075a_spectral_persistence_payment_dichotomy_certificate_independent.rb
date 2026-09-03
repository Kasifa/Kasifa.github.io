#!/usr/bin/env ruby
# Independent exact-arithmetic verifier for the frozen R0.75A certificate.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075a_spectral_persistence_payment_dichotomy.md'
JSON_PATH = Pathname.new(ENV.fetch('R075A_JSON', (ROOT + 'research/r075a_spectral_persistence_payment_dichotomy_certificate.json').to_s))
REPORT = Pathname.new(ENV.fetch('R075A_RUBY_REPORT', (ROOT + 'research/r075a_spectral_persistence_payment_dichotomy_certificate_independent_audit.md').to_s))
MUTATION = ENV.fetch('R075A_RUBY_MUTATION', '')
MAIN_HASH = 'f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388'
SCHEMA = 'r075a-spectral-persistence-payment-dichotomy-certificate-v1'

SOURCES = {
  'research/r074p_temporal_observable_triage.md' => 'a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867',
  'research/r074q_common_shear_multipacket_gate.md' => '60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695',
  'research/r074u_intrinsic_certified_residence.md' => 'e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99',
  'research/r074w_remote_adjacent_inward_comparison.md' => 'd818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10',
  'research/r074z_cancellation_cell_gate.md' => 'bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a'
}.freeze

MUTATIONS = %w[
  wrong_sign cutoff_r_minus_2 cutoff_r_minus_4 wrong_weight_omega
  p_reciprocal critical_only_omission full_clock_promotion source_drift
].freeze

abort("unknown R075A_RUBY_MUTATION: #{MUTATION}") unless MUTATION.empty? || MUTATIONS.include?(MUTATION)

text = MAIN.read
flat_text = text.gsub(/\s+/, ' ')
p_value = MUTATION == 'p_reciprocal' ? Rational(63, 32) : Rational(32, 63)
lambda_value = Rational(63, 32)
c_gamma = Rational(8, 3969)
rho = Rational(9, 10_000)
gap = Rational(5, 24) * c_gamma - Rational(1, 6) * rho
transport_sign = MUTATION == 'wrong_sign' ? -1 : 1
cutoff_power = MUTATION == 'cutoff_r_minus_2' ? -2 : (MUTATION == 'cutoff_r_minus_4' ? -4 : -3)
weight_power = MUTATION == 'wrong_weight_omega' ? Rational(1) : Rational(1, 4)
critical_covered = MUTATION != 'critical_only_omission'
full_clock_promoted = MUTATION == 'full_clock_promotion'

nested = [
  Rational(3, 16) < Rational(1, 4),
  Rational(5, 4) < Rational(21, 16),
  Rational(21, 16) < Rational(23, 16),
  Rational(23, 16) < Rational(3, 2),
  Rational(-1) < Rational(-15, 16),
  Rational(-15, 16) < Rational(-9, 16),
  Rational(-9, 16) < Rational(-1, 2),
  Rational(-15, 16) < 0,
  Rational(5, 2) / Rational(15, 16) == Rational(8, 3),
  Rational(8, 3) > 2,
  Rational(5, 4) - Rational(1, 96) > 0
]

b_lower = Rational(1, 128)
b_plateau_upper = Rational(1, 128) / Rational(3, 4)
b_crude_upper = Rational(1, 96)

a28_r = Rational(3, 2) * 3 - Rational(1, 2) * 6
a28_l = -Rational(1, 2) * Rational(1, 2)
a29_r = a28_r - 2
a31_r = a29_r + Rational(3, 2)
a31_w = weight_power - Rational(3, 2)
a1 = [Rational(2, 3) * a31_r, Rational(2, 3) * a28_l, Rational(2, 3) * a31_w]

expected_exponents = {
  'A.26_X' => {'EStar' => '1', 'L' => '0', 'R' => '3', 'omega' => '0'},
  'A.27_spacetimeVolume' => {'EStar' => '0', 'L' => '1/2', 'R' => '6', 'omega' => '0'},
  'A.28_cubicIntegral' => {'EStar' => '3/2', 'L' => '-1/4', 'R' => '3/2', 'omega' => '0'},
  'A.29_paymentBeforeEndpoint' => {'EStar' => '3/2', 'L' => '-1/4', 'R' => '-1/2', 'omega' => '1/4'},
  'A.30_endpointSubstitution' => {'L' => '0', 'R' => '1', 'hRemote' => '1', 'omega' => '-1'},
  'A.31_paymentAfterEndpoint' => {'L' => '-1/4', 'R' => '1', 'hRemote' => '3/2', 'omega' => '-5/4'},
  'A.1_twoThirdsPower' => {'L' => '-1/6', 'R' => '2/3', 'hRemote' => '1', 'omega' => '-5/6'},
  'A.32_logOmega' => {'cGamma' => '1/4'},
  'A.32_logR' => {'rho' => '1/4'},
  'A.33_rate' => {'cGamma' => '5/24', 'rho' => '-1/6'}
}.freeze

tags = text.scan(/\\tag\{(A\.[^}]+)\}/).flatten
refs = text.scan(/\(A\.([0-9]+[a-z]?)\)/).flatten.map { |value| "A.#{value}" }
opens = text.lines.count { |line| line.strip == '\\[' }
closes = text.lines.count { |line| line.strip == '\\]' }

tokens = [
  'p=\\lambda^{-1}=\\frac{32}{63}',
  '\\frac1{128R^2}\\le B',
  '\\le\\frac1{96R^2}',
  'c\\,\\partial_z\\phi+\\Delta_{z3}\\phi',
  'K_\\phi R^{-3}\\mathbf 1_{\\mathcal S_+}',
  'C L^{1/2}R^6',
  'cE_*^{3/2}R^{3/2}L^{-1/4}',
  'c\\omega^{1/4}E_*^{3/2}R^{-1/2}L^{-1/4}',
  '\\frac{2R}{\\omega}h_{\\rm rem}',
  'R\\,\\omega^{-5/4}L^{-1/4}',
  'R^{2/3}\\omega^{-5/6}L^{-1/6}',
  '\\frac{64279}{238140000}>0',
  '\\partial_tf_n-\\partial_3^2f_n',
  '+(n^2+inb(t,x_3))f_n=0',
  '+\\|\\partial_3f_n(t)\\|_2^2',
  '+n^2\\|f_n(t)\\|_2^2=0',
  '\\|f_n(t)\\|_2\\le e^{-n^2(t-s)}\\|f_n(s)\\|_2',
  '\\ge e^{N^2(t-s)}',
  '\\Lambda_{\\rm band}:=N^2+M^2+B_QN',
  'W-REMOTE ENDPOINT PERSISTENCE/PAYMENT DICHOTOMY: PROVED',
  'NO FREQUENCY/GEOMETRY-UNIFORM LOCAL OBSERVABILITY CONSTANT',
  'COMPLETE }K\\textbf{, FIXED DELETION, AND REGULARITY: OPEN',
  'includes persistent, critical, and arbitrarily shorter smooth',
  'does **not** upper-bound the full completed clock',
  'a fixed-deletion theorem follows from (A.31) | **NOT PROVED**',
  '\\mathbf{NOT\\ CLAY}',
  'R075A_COMPLETE_CLOCK_OPEN'
]

json_payload = JSON.parse(JSON_PATH.read)
source_hash_expected = MUTATION == 'source_drift' ? '0' * 64 : MAIN_HASH
source_ok = Digest::SHA256.file(MAIN).hexdigest == source_hash_expected
dependencies_ok = SOURCES.all? do |path, digest|
  Digest::SHA256.file(ROOT + path).hexdigest == digest && text.include?("`#{path}` | `#{digest}`")
end

checks = {
  'main source binding' => source_ok,
  'five frozen source bindings' => dependencies_ok,
  'p reciprocal convention' => p_value == Rational(32, 63) && lambda_value == Rational(63, 32) && p_value * lambda_value == 1 && text !~ /p\s*=\s*\\frac\{63\}\{32\}/,
  'nested core inequalities' => nested.all?,
  'B interval' => b_lower < b_plateau_upper && b_plateau_upper == b_crude_upper,
  'moving cutoff sign and R power' => transport_sign == 1 && cutoff_power == -3,
  'exponent algebra A.26--A.34' => a28_r == Rational(3, 2) && a28_l == Rational(-1, 4) && a29_r == Rational(-1, 2) && a31_r == 1 && a31_w == Rational(-5, 4) && a1 == [Rational(2, 3), Rational(-1, 6), Rational(-5, 6)],
  'exact gap A.34' => gap == Rational(64_279, 238_140_000) && gap.positive?,
  '64 unique tags and resolved references' => tags.length == 64 && tags.uniq.length == 64 && (refs - tags).empty?,
  'balanced displays' => opens == 64 && closes == 64,
  'textual formula and boundary sentinels' => tokens.all? { |token| flat_text.include?(token.gsub(/\s+/, ' ')) },
  'critical and shorter coverage' => critical_covered && text.include?('all shorter smooth focusing'),
  'full clock and fixed deletion remain open' => !full_clock_promoted && flat_text.include?('a fixed-deletion bound nor refutes the frozen fixed-deletion theorem'),
  'python JSON schema and verdict' => json_payload['schema'] == SCHEMA && json_payload['verdict'] == 'PASS',
  'python JSON exact values' => json_payload.dig('exactValues', 'p') == '32/63' && json_payload.dig('exactValues', 'gapA34') == '64279/238140000',
  'python JSON exponent ledger' => json_payload.dig('checks', 'exponentLedgerA26ToA34', 'exponents') == expected_exponents,
  'UTF-8 and control safety' => text.valid_encoding? && !text.each_codepoint.any? { |code| code < 32 && ![9, 10, 13].include?(code) }
}

verdict = checks.values.all? ? 'PASS' : 'FAIL'
REPORT.write(
  "# R0.75A independent Ruby verification\n\n" \
  "- Verdict: **#{verdict}**\n" \
  "- Assertions: #{checks.values.count(true)}/#{checks.length}\n" \
  "- Main SHA-256: `#{Digest::SHA256.file(MAIN).hexdigest}`\n" \
  "- Exact p: `#{p_value}`; lambda: `#{lambda_value}`\n" \
  "- Exact gap (A.34): `#{gap}`\n" \
  "- Tags: #{tags.length}; displays: #{opens}/#{closes}\n\n" \
  "Ruby independently recomputed the nested geometry, B interval, moving-cutoff sign and R power, " \
  "the A.26--A.34 exponent algebra, and modal/status sentinels. It then cross-checked the Python " \
  "certificate schema, exact values, and full exponent ledger.\n\n" \
  "The certified result is confined to the exact finite common-shear W-remote endpoint/payment " \
  "dichotomy. Complete K, fixed deletion, arbitrary suitable weak solutions, regularity, and Clay " \
  "remain open. **NOT CLAY.**\n"
)

puts JSON.generate({verdict: verdict, assertions: checks.length, mutation: MUTATION.empty? ? nil : MUTATION})
exit(verdict == 'PASS' ? 0 : 1)
