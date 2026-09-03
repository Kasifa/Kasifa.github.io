#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075f_modal_phase_integration_identity_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075f_modal_phase_integration_identity_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075f_modal_phase_integration_identity_qa.sh"
FIXTURES="$ROOT/scripts/r075f_modal_phase_integration_identity_fixtures.json"
EXPECTED="$ROOT/scripts/r075f_modal_phase_integration_identity_expected.json"
MAIN="$ROOT/research/r075f_modal_phase_integration_identity.md"
PRIMARY_AUDIT="$ROOT/research/r075f_modal_phase_integration_identity_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075f_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
CERT="$ROOT/research/r075f_modal_phase_integration_identity_certificate.json"
REPORT="$ROOT/research/r075f_modal_phase_integration_identity_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075f_modal_phase_integration_identity_independent_audit.md"
QA_REPORT="$ROOT/research/r075f_modal_phase_integration_identity_qa_report.md"

EXPECTED_MAIN_HASH=f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440
EXPECTED_PRIMARY_AUDIT_HASH=4320ac5544b51888eb8088db98e500a9877ecfe9a984f156783cac096a27c99a
EXPECTED_REPORT_SOURCE_HASH=3838603ea143b2efe1e96995fac34d7e8565211dc91dd244ab01cf6d526f3481
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_FIXTURES_HASH=0ce9b3bf060f4b38fe497be7bcdad3d1bdbd51ea27ff9aab146c8b10f5a0aced
EXPECTED_EXPECTED_HASH=3946cb2cc992f4d1e55b88a7be9b7ecd8529e76a437093af6583f8fdacf2ddc9

TMP_ROOT=$(mktemp -d /tmp/r075f-certificate-qa.XXXXXX)
trap 'rm -rf "$TMP_ROOT"' EXIT

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

command -v "$PYTHON_BIN" >/dev/null
command -v ruby >/dev/null
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"
"$PYTHON_BIN" -m json.tool "$FIXTURES" >"$TMP_ROOT/fixtures.pretty"
"$PYTHON_BIN" -m json.tool "$EXPECTED" >"$TMP_ROOT/expected.pretty"

test "$(digest "$MAIN")" = "$EXPECTED_MAIN_HASH"
test "$(digest "$PRIMARY_AUDIT")" = "$EXPECTED_PRIMARY_AUDIT_HASH"
test "$(digest "$REPORT_SOURCE")" = "$EXPECTED_REPORT_SOURCE_HASH"
test "$(digest "$B_SOURCE")" = "$EXPECTED_B_HASH"
test "$(digest "$E_SOURCE")" = "$EXPECTED_E_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.' "$PRIMARY_AUDIT"
grep -q 'Equation tags F.1--F.23 are unique and consecutive.' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075F_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075F_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 16' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075F_JSON="$CERT" R075F_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":20' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 20/20' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift dependency_table_missing fixture_drift expected_drift tag reference display control mode_n_shear_sign mode_m_shear_sign ell_sign product_cross_two phase_lhs_sign no_division period_factor endpoint_half dissipation_factor gradient_nm_sign cutoff_ell_sign eta_initial eta_terminal time_ibp_sign vertical_ibp_sign square_decomposition transport_reconstruction cancellation_residual diagonal_identity fejer_even_allowed fejer_count fejer_fourth fejer_weight_bound fejer_mean fejer_ratio_n3 fejer_ratio_n5 fejer_ratio_n7 fejer_divergence counterexample_claim e24_closed full_clock clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 \
    R075F_MUTATION="$mutation" \
    R075F_JSON="$TMP_ROOT/python-$mutation.json" \
    R075F_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" \
    2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075F_JSON="$CERT" \
    R075F_RUBY_MUTATION="$mutation" \
    R075F_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" \
    2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq 43
test "$ruby_mutations" -eq 43

if env R075F_MUTATION=unknown_mutation \
  R075F_JSON="$TMP_ROOT/unknown-python.json" \
  R075F_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" \
  2>"$TMP_ROOT/unknown-python.stderr"; then
  echo "Python accepted an unknown mutation" >&2
  exit 1
fi
grep -q 'unknown R075F_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075F_JSON="$CERT" \
  R075F_RUBY_MUTATION=unknown_mutation \
  R075F_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" \
  2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo "Ruby accepted an unknown mutation" >&2
  exit 1
fi
grep -q 'unknown R075F_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-regenerate.stdout"
env R075F_JSON="$CERT" R075F_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
report_source_hash=$(digest "$REPORT_SOURCE")
b_source_hash=$(digest "$B_SOURCE")
e_source_hash=$(digest "$E_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75F certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Python assertions: 16/16'
  printf '%s\n' '- Ruby assertions: 20/20'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075f_modal_phase_integration_identity.md | $main_hash |"
  printf '%s\n' "| research/r075f_modal_phase_integration_identity_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075f_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075f_modal_phase_integration_identity_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075f_modal_phase_integration_identity_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075f_modal_phase_integration_identity_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075f_modal_phase_integration_identity_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075f_modal_phase_integration_identity_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075f_modal_phase_integration_identity_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075f_modal_phase_integration_identity_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075f_modal_phase_integration_identity_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit was checked for the frozen main hash, PASS with zero'
  printf '%s\n' 'mathematical and release blockers, and F.1--F.23 coverage.'
  printf '%s\n' 'The report-source file is byte-bound only; literature content and'
  printf '%s\n' 'recorded HTTP access checks are outside this finite certificate.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075b_bulk_clock_outer_padding_gate.md | $b_source_hash |"
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_source_hash |"
  printf '%s\n' ''
  printf '%s\n' 'Both hashes match the F main note source table and both implementations.'
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- F.1--F.18 modal equations, product rule, ell=m-n, nm, and pi/2pi normalization: PASS.'
  printf '%s\n' '- Genuine two-mode closed solution, endpoint rows, F.14/F.15 IBP, and F.12/F.17/F.18: PASS.'
  printf '%s\n' '- Direct transport and all closed-solution rows agree in Q[p], p=pi^-2: PASS.'
  printf '%s\n' '- F.19--F.23 ordered Fejer counts, N=3/5/7 moments, ratios, and divergence: PASS.'
  printf '%s\n' '- Tags F.1--F.23, references, and 23/23 displays: PASS.'
  printf '%s\n' '- Main/audit/source/dependencies/fixtures/expected byte bindings: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The finite checks certify the exact route-pruning identities only.'
  printf '%s\n' 'The Fejer family is not the frozen geometric collar and is not an E.24'
  printf '%s\n' 'counterexample. E.24, complete-clock extraction, fixed deletion,'
  printf '%s\n' 'suitable-weak transfer, regularity, and singularity remain OPEN.'
  printf '%s\n' '**NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075f-modal-phase-integration-identity","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
