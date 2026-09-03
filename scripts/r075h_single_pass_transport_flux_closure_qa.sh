#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075h_single_pass_transport_flux_closure_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075h_single_pass_transport_flux_closure_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075h_single_pass_transport_flux_closure_qa.sh"
FIXTURES="$ROOT/scripts/r075h_single_pass_transport_flux_closure_fixtures.json"
EXPECTED="$ROOT/scripts/r075h_single_pass_transport_flux_closure_expected.json"
MAIN="$ROOT/research/r075h_single_pass_transport_flux_closure.md"
PRIMARY_AUDIT="$ROOT/research/r075h_single_pass_transport_flux_closure_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075h_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
F_SOURCE="$ROOT/research/r075f_modal_phase_integration_identity.md"
G_SOURCE="$ROOT/research/r075g_signed_flux_gain_threshold.md"
CERT="$ROOT/research/r075h_single_pass_transport_flux_closure_certificate.json"
REPORT="$ROOT/research/r075h_single_pass_transport_flux_closure_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075h_single_pass_transport_flux_closure_independent_audit.md"
QA_REPORT="$ROOT/research/r075h_single_pass_transport_flux_closure_qa_report.md"

EXPECTED_MAIN_HASH=849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9
EXPECTED_PRIMARY_AUDIT_HASH=3c85368e051102997e66ae36fa43290b6200e688db886380215fb40ec0bb757e
EXPECTED_REPORT_SOURCE_HASH=5b0b05b2ce903986ef8439a766766e8bdb97e2fe4d9eb6035f73102583b1b779
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_F_HASH=f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440
EXPECTED_G_HASH=f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41
EXPECTED_FIXTURES_HASH=7e4b5691d6929c97f72146c293a55e3b6fcf5875bc51f78bd1a58e9f84a0b217
EXPECTED_EXPECTED_HASH=099d017cb7ff61d5a9dff54449c9a91a12e8657343bb11579ad135e9cd350573

TMP_ROOT=$(mktemp -d /tmp/r075h-certificate-qa.XXXXXX)
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
test "$(digest "$F_SOURCE")" = "$EXPECTED_F_HASH"
test "$(digest "$G_SOURCE")" = "$EXPECTED_G_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.' "$PRIMARY_AUDIT"
grep -q 'Equation tags H.1--H.29 are unique and consecutive.' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075H_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075H_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 19' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075H_JSON="$CERT" R075H_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":22' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 22/22' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift dependency_table_missing fixture_drift expected_drift tag reference display control transport_pde_sign transport_energy_sign eta_initial eta_terminal eta_monotone eta_plateau eta_ibp_sign transport_half characteristic_direction set_translation_direction q_shift terminal_containment seam_crossing terminal_l2 persistence_direction persistence_time holder_measure holder_delta_power holder_volume_power holder_l3_power holder_division h23_flux_r h23_flux_omega h23_delta_r h23_volume_l h23_volume_r h23_cubic_r h23_cubic_omega h23_cubic_p rate_rho_sign rate_cgamma_sign rate_fraction matching_lower_direction matching_r_power matching_cube_root diff_terminal_sign diff_dissipation_sign diff_cutoff_sign diff_circularity atom_r_sign atom_omega_sign flux_normalization measurement_weight benchmark_nse conditional_weight payment_region transport_absolute_flux block_count diffusive_characteristic e24_closed complete_clock fixed_deletion suitable_weak regularity clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 \
    R075H_MUTATION="$mutation" \
    R075H_JSON="$TMP_ROOT/python-$mutation.json" \
    R075H_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" \
    2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075H_JSON="$CERT" \
    R075H_RUBY_MUTATION="$mutation" \
    R075H_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" \
    2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq 66
test "$ruby_mutations" -eq 66

if env R075H_MUTATION=unknown_mutation \
  R075H_JSON="$TMP_ROOT/unknown-python.json" \
  R075H_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" \
  2>"$TMP_ROOT/unknown-python.stderr"; then
  echo "Python accepted an unknown mutation" >&2
  exit 1
fi
grep -q 'unknown R075H_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075H_JSON="$CERT" \
  R075H_RUBY_MUTATION=unknown_mutation \
  R075H_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" \
  2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo "Ruby accepted an unknown mutation" >&2
  exit 1
fi
grep -q 'unknown R075H_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-regenerate.stdout"
env R075H_JSON="$CERT" R075H_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
report_source_hash=$(digest "$REPORT_SOURCE")
b_source_hash=$(digest "$B_SOURCE")
e_source_hash=$(digest "$E_SOURCE")
f_source_hash=$(digest "$F_SOURCE")
g_source_hash=$(digest "$G_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75H certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Python assertions: 19/19'
  printf '%s\n' '- Ruby assertions: 22/22'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075h_single_pass_transport_flux_closure.md | $main_hash |"
  printf '%s\n' "| research/r075h_single_pass_transport_flux_closure_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075h_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075h_single_pass_transport_flux_closure_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075h_single_pass_transport_flux_closure_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075h_single_pass_transport_flux_closure_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075h_single_pass_transport_flux_closure_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075h_single_pass_transport_flux_closure_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075h_single_pass_transport_flux_closure_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075h_single_pass_transport_flux_closure_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075h_single_pass_transport_flux_closure_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit was checked for the frozen main hash, PASS with zero'
  printf '%s\n' 'mathematical and release blockers, and H.1--H.29 coverage.'
  printf '%s\n' 'The report-source file is byte-bound only; literature content and'
  printf '%s\n' 'recorded HTTP access checks are outside this finite certificate.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075b_bulk_clock_outer_padding_gate.md | $b_source_hash |"
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_source_hash |"
  printf '%s\n' "| research/r075f_modal_phase_integration_identity.md | $f_source_hash |"
  printf '%s\n' "| research/r075g_signed_flux_gain_threshold.md | $g_source_hash |"
  printf '%s\n' ''
  printf '%s\n' 'All hashes match the H main note source table and both implementations.'
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- Smooth pure transport with nondecreasing eta: direct positive flux and endpoint identity PASS (1/64).'
  printf '%s\n' '- One nondegenerate all-rational fixture coherently recomputes H.11--H.23, including H.20--H.22: PASS.'
  printf '%s\n' '- Mirrored negative-flux control rejects replacing the signed positive part by absolute value: PASS.'
  printf '%s\n' '- Characteristic and lifted-set translation direction, no seam, and terminal L2 persistence: PASS.'
  printf '%s\n' '- Holder delta^(-2/3) and volume^(1/3) powers via a nonzero equality case: PASS.'
  printf '%s\n' '- Full H.23 R/L/omega/p normalization and rate -4279/238140000: PASS.'
  printf '%s\n' '- Matching p_b lower bound gives H.26 in the displayed direction: PASS.'
  printf '%s\n' '- H.28 terminal/dissipation/cutoff signs and diffusive circularity: PASS.'
  printf '%s\n' '- Tags H.1--H.29, references, 29/29 displays, and control bytes: PASS.'
  printf '%s\n' '- Main/audit/source/dependencies/fixtures/expected byte bindings: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'Only the signed pure-transport terminal-tube benchmark is certified.'
  printf '%s\n' 'The benchmark P_R^(M,tr) is not an NSE solution functional. The result'
  printf '%s\n' 'does not cover absolute flux, multiple windings, or the diffusive'
  printf '%s\n' 'characteristic. E.24, complete clock, fixed deletion, suitable-weak'
  printf '%s\n' 'transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075h-single-pass-transport-flux-closure","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
