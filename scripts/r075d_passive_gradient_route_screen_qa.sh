#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075d_passive_gradient_route_screen_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075d_passive_gradient_route_screen_certificate_independent.rb"
CERT="$ROOT/research/r075d_passive_gradient_route_screen_certificate.json"
REPORT="$ROOT/research/r075d_passive_gradient_route_screen_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075d_passive_gradient_route_screen_independent_audit.md"
QA_REPORT="$ROOT/research/r075d_passive_gradient_route_screen_qa_report.md"
MAIN="$ROOT/research/r075d_passive_gradient_route_screen.md"
REPORT_SOURCE="$ROOT/research/r075d_report-source.md"
PRIMARY_AUDIT="$ROOT/research/r075d_passive_gradient_route_screen_primary_audit.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
C_SOURCE="$ROOT/research/r075c_background_shear_packing_false_positive.md"
EXPECTED_MAIN_HASH=54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6
EXPECTED_REPORT_SOURCE_HASH=5c415c3e280fea1569a42d64d99400fe4dfaf440d2808d637ca57cfc1d386c1f
EXPECTED_PRIMARY_AUDIT_HASH=f06e29971ea3f0b05c7a1c39983a2ae21aa241a8e46f02e2450632e07c5eaef7
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_C_HASH=1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89
TMP_ROOT=$(mktemp -d /tmp/r075d-certificate-qa.XXXXXX)
trap 'rm -rf "$TMP_ROOT"' EXIT

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

command -v "$PYTHON_BIN" >/dev/null
command -v ruby >/dev/null
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"

test "$(digest "$MAIN")" = "$EXPECTED_MAIN_HASH"
test "$(digest "$REPORT_SOURCE")" = "$EXPECTED_REPORT_SOURCE_HASH"
test "$(digest "$PRIMARY_AUDIT")" = "$EXPECTED_PRIMARY_AUDIT_HASH"
grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS' "$PRIMARY_AUDIT"
grep -q 'blocker count: 0' "$PRIMARY_AUDIT"
grep -q 'tags D.1--D.23 are unique and consecutive' "$PRIMARY_AUDIT"
test "$(digest "$B_SOURCE")" = "$EXPECTED_B_HASH"
test "$(digest "$C_SOURCE")" = "$EXPECTED_C_HASH"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075D_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075D_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 20' "$TMP_ROOT/python-canonical.stdout"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075D_JSON="$CERT" R075D_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":23' "$TMP_ROOT/ruby-canonical.stdout"

mutations='holder_volume cubic_payment_r target_weight klow_threshold klow_rate modal_energy_sign modal_decay zero_mode_omission gradient_forcing_sign gradient_dissipation transition_volume block_count critical_threshold gap_fraction transport_sign transport_dropped pf_normalization fallback_cutoff_r fallback_volume mixed_holder mixed_weight cubic_sum pb_scale pb_rate small_payment_direction linear_absorbed interaction_power component_promotion high_frequency_proved intermediate_band_closed commutator_closed periodic_dropped counterexample_promotion full_clock_promotion source_drift dependency_drift dependency_table_assumed tag reference display clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 \
    R075D_MUTATION="$mutation" \
    R075D_JSON="$TMP_ROOT/python-$mutation.json" \
    R075D_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" \
    2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R075D_JSON="$CERT" \
    R075D_RUBY_MUTATION="$mutation" \
    R075D_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" \
    2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done

if env R075D_MUTATION=unknown_mutation \
  R075D_JSON="$TMP_ROOT/unknown-python.json" \
  R075D_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" \
  2>"$TMP_ROOT/unknown-python.stderr"; then
  echo "Python accepted an unknown mutation" >&2
  exit 1
fi
grep -q 'unknown R075D_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075D_JSON="$CERT" \
  R075D_RUBY_MUTATION=unknown_mutation \
  R075D_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" \
  2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo "Ruby accepted an unknown mutation" >&2
  exit 1
fi
grep -q 'unknown R075D_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-regenerate.stdout"
env R075D_JSON="$CERT" R075D_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
report_source_hash=$(digest "$REPORT_SOURCE")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
b_source_hash=$(digest "$B_SOURCE")
c_source_hash=$(digest "$C_SOURCE")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$0")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75D certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' "- Python assertions: 20/20"
  printf '%s\n' "- Ruby assertions: 23/23"
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075d_passive_gradient_route_screen.md | $main_hash |"
  printf '%s\n' "| research/r075d_report-source.md | $report_source_hash |"
  printf '%s\n' "| research/r075d_passive_gradient_route_screen_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| scripts/r075d_passive_gradient_route_screen_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075d_passive_gradient_route_screen_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075d_passive_gradient_route_screen_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075d_passive_gradient_route_screen_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075d_passive_gradient_route_screen_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075d_passive_gradient_route_screen_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The report-source file is hash-bound in this QA release manifest only.'
  printf '%s\n' 'Its literature content and the recorded HTTP status are outside the'
  printf '%s\n' 'finite arithmetic producer and independent Ruby verifier.'
  printf '%s\n' 'The primary audit is also release-bound and was checked for the frozen'
  printf '%s\n' 'main hash, PASS with zero blockers, and D.1--D.23 coverage.'
  printf '%s\n' ''
  printf '%s\n' '## Certificate-side dependency boundary' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075b_bulk_clock_outer_padding_gate.md | $b_source_hash |"
  printf '%s\n' "| research/r075c_background_shear_packing_false_positive.md | $c_source_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The main note has no embedded frozen-source table. These two hashes are'
  printf '%s\n' 'certificate-side bindings and are not represented as main-file rows.'
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- Tags D.1--D.23, local references, B/C references, and 23/23 displays: PASS.'
  printf '%s\n' '- D.4--D.7 Holder/R/L/omega/K powers and K-low exact rate: PASS.'
  printf '%s\n' '- Modal equation, norm versus squared-norm damping, and zero-mode obstruction: PASS.'
  printf '%s\n' '- D.10--D.11 forcing sign and exact Laplacian dissipation: PASS.'
  printf '%s\n' '- Transition-band volume, short-block threshold, and intermediate gap: PASS.'
  printf '%s\n' '- D.16--D.23 transport, pF/pB normalizations, mixed homogeneity, and exact rate: PASS.'
  printf '%s\n' '- Small-payment direction and non-absorption on the frozen large-payment branch: PASS.'
  printf '%s\n' '- Commutator, periodic-weight, interaction, and counterexample boundaries remain OPEN: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The exact fallback is P^(2/3)+P and closes only the small-payment regime.'
  printf '%s\n' 'The frozen branch has P tending to infinity; the linear term is not'
  printf '%s\n' 'absorbed. No exact counterexample or complete-clock result is'
  printf '%s\n' 'certified. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075d-passive-gradient-route-screen","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
