#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075e_horizontal_cross_mode_flux_reduction_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075e_horizontal_cross_mode_flux_reduction_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075e_horizontal_cross_mode_flux_reduction_qa.sh"
MAIN="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
CERT="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction_certificate.json"
REPORT="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction_independent_audit.md"
QA_REPORT="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction_qa_report.md"
PRIMARY_AUDIT="$ROOT/research/r075e_horizontal_cross_mode_flux_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075e_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
C_SOURCE="$ROOT/research/r075c_background_shear_packing_false_positive.md"
D_SOURCE="$ROOT/research/r075d_passive_gradient_route_screen.md"

EXPECTED_MAIN_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_PRIMARY_AUDIT_HASH=da2778c1f0d5538981c517fccf75c96a635abbe7fae8833359c727dd2b301860
EXPECTED_REPORT_SOURCE_HASH=96577484d25745b419c30723c0af2d2873fbfff1f3340b79e1d7c9af71327199
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_C_HASH=1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89
EXPECTED_D_HASH=54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6

TMP_ROOT=$(mktemp -d /tmp/r075e-certificate-qa.XXXXXX)
trap 'rm -rf "$TMP_ROOT"' EXIT

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

command -v "$PYTHON_BIN" >/dev/null
command -v ruby >/dev/null
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"

test "$(digest "$MAIN")" = "$EXPECTED_MAIN_HASH"
test "$(digest "$PRIMARY_AUDIT")" = "$EXPECTED_PRIMARY_AUDIT_HASH"
test "$(digest "$REPORT_SOURCE")" = "$EXPECTED_REPORT_SOURCE_HASH"
test "$(digest "$B_SOURCE")" = "$EXPECTED_B_HASH"
test "$(digest "$C_SOURCE")" = "$EXPECTED_C_HASH"
test "$(digest "$D_SOURCE")" = "$EXPECTED_D_HASH"

grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.' "$PRIMARY_AUDIT"
grep -q 'Equation tags E.1--E.24 are unique and consecutive.' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075E_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075E_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 13' "$TMP_ROOT/python-canonical.stdout"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075E_JSON="$CERT" R075E_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":16' "$TMP_ROOT/ruby-canonical.stdout"

mutations='source_drift dependency_drift dependency_table_missing tag reference display control period_factor formula_pi_factor laurent_derivative_sign difference_sign index_reversal diagonal_nonzero zero_mode_nonzero singleton_physical real_pair_zero reality_pair_broken e15_volume e15_cutoff_r e15_cubic_normalization e15_omega e16_decay_sign e16_denominator e21_pi e21_omega e21_r e23_pb_power e23_pf_power e23_residual_r endpoint_dropped transport_sign mode_invariance x1_hat_not_average zero_mode_small_payment complex_physical real_pair_cancelled e24_closed full_clock clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 \
    R075E_MUTATION="$mutation" \
    R075E_JSON="$TMP_ROOT/python-$mutation.json" \
    R075E_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" \
    2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R075E_JSON="$CERT" \
    R075E_RUBY_MUTATION="$mutation" \
    R075E_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" \
    2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done

if env R075E_MUTATION=unknown_mutation \
  R075E_JSON="$TMP_ROOT/unknown-python.json" \
  R075E_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" \
  2>"$TMP_ROOT/unknown-python.stderr"; then
  echo "Python accepted an unknown mutation" >&2
  exit 1
fi
grep -q 'unknown R075E_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075E_JSON="$CERT" \
  R075E_RUBY_MUTATION=unknown_mutation \
  R075E_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" \
  2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo "Ruby accepted an unknown mutation" >&2
  exit 1
fi
grep -q 'unknown R075E_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-regenerate.stdout"
env R075E_JSON="$CERT" R075E_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
report_source_hash=$(digest "$REPORT_SOURCE")
b_source_hash=$(digest "$B_SOURCE")
c_source_hash=$(digest "$C_SOURCE")
d_source_hash=$(digest "$D_SOURCE")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75E certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Python assertions: 13/13'
  printf '%s\n' '- Ruby assertions: 16/16'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $main_hash |"
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075e_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075e_horizontal_cross_mode_flux_reduction_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075e_horizontal_cross_mode_flux_reduction_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075e_horizontal_cross_mode_flux_reduction_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit was checked for the frozen main hash, PASS with zero'
  printf '%s\n' 'mathematical and release blockers, and E.1--E.24 coverage.'
  printf '%s\n' 'The report-source file is byte-bound here only; its literature content'
  printf '%s\n' 'and recorded HTTP checks are outside the finite arithmetic suite.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075b_bulk_clock_outer_padding_gate.md | $b_source_hash |"
  printf '%s\n' "| research/r075c_background_shear_packing_false_positive.md | $c_source_hash |"
  printf '%s\n' "| research/r075d_passive_gradient_route_screen.md | $d_source_hash |"
  printf '%s\n' ''
  printf '%s\n' 'All three observed hashes match both the certificate constants and the'
  printf '%s\n' 'frozen-source table embedded in the E main note.'
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- Tags E.1--E.24, references, and 24/24 displays: PASS.'
  printf '%s\n' '- Direct Laurent and independent ordered-mode T/pi normalization: PASS (-1/2).'
  printf '%s\n' '- Diagonal cancellation, zero mode, and complex-singleton zero flux: PASS.'
  printf '%s\n' '- Complex singleton is not physical; a real +/-1 pair has nonzero flux: PASS.'
  printf '%s\n' '- E.15 L/R/omega/pF powers and E.16 exponential sign: PASS.'
  printf '%s\n' '- E.21 pi*omega/R normalization and E.23 mixed powers: PASS.'
  printf '%s\n' '- Endpoint, transport sign, support invariance, and x1-average boundary: PASS.'
  printf '%s\n' '- E.24 arbitrary-real estimate and all larger conclusions remain OPEN: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The finite witness verifies E.10 algebra and normalization only; it is'
  printf '%s\n' 'not a full E.1 spacetime trajectory or the geometric collar cutoff.'
  printf '%s\n' 'The all-payment estimate is restricted to the real horizontal zero mode'
  printf '%s\n' 'for L>=L0. A complex singleton is diagnostic only, while a real +/-n'
  printf '%s\n' 'pair is not forced to cancel. E.24, complete clock, fixed deletion,'
  printf '%s\n' 'suitable-weak transfer, and regularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075e-horizontal-cross-mode-flux-reduction","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
