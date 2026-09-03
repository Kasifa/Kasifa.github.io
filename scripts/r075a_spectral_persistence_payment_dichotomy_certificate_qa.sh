#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=${PYTHON_BIN:-python3}
PY_SCRIPT="$ROOT/scripts/r075a_spectral_persistence_payment_dichotomy_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075a_spectral_persistence_payment_dichotomy_certificate_independent.rb"
CERT="$ROOT/research/r075a_spectral_persistence_payment_dichotomy_certificate.json"
REPORT="$ROOT/research/r075a_spectral_persistence_payment_dichotomy_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075a_spectral_persistence_payment_dichotomy_certificate_independent_audit.md"
QA_REPORT="$ROOT/research/r075a_spectral_persistence_payment_dichotomy_certificate_qa_report.md"
TMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/r075a-certificate-qa.XXXXXX")
trap 'rm -rf "$TMP_ROOT"' EXIT

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

command -v "$PYTHON_BIN" >/dev/null
command -v ruby >/dev/null

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075A_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075A_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075A_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"

mutations=(
  wrong_sign
  cutoff_r_minus_2
  cutoff_r_minus_4
  wrong_weight_omega
  p_reciprocal
  critical_only_omission
  full_clock_promotion
  source_drift
)

for mutation in "${mutations[@]}"; do
  if env PYTHONHASHSEED=0 \
    R075A_MUTATION="$mutation" \
    R075A_JSON="$TMP_ROOT/python-$mutation.json" \
    R075A_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"

  if env R075A_RUBY_MUTATION="$mutation" \
    R075A_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
done

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075A_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$ROOT/research/r075a_spectral_persistence_payment_dichotomy.md")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$0")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75A certificate QA report' '' '- Verdict: **PASS**'
  printf '%s\n' "- Main SHA-256: \`$main_hash\`"
  printf '%s\n' "- Python producer SHA-256: \`$python_hash\`"
  printf '%s\n' "- Ruby verifier SHA-256: \`$ruby_hash\`"
  printf '%s\n' "- QA driver SHA-256: \`$qa_hash\`"
  printf '%s\n' "- Certificate JSON SHA-256: \`$cert_hash\`"
  printf '%s\n' "- Python report SHA-256: \`$report_hash\`"
  printf '%s\n' "- Ruby report SHA-256: \`$ruby_report_hash\`"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- Frozen main and all five source-table SHA-256 bindings: PASS.'
  printf '%s\n' '- Exact fractions, `p=32/63`, nested-core inequalities, and B interval: PASS.'
  printf '%s\n' '- Moving-cutoff sign and exact `R^-3` scale: PASS.'
  printf '%s\n' '- Every R/L/omega exponent in (A.26)--(A.34): PASS.'
  printf '%s\n' '- Horizontal modal equations, energy signs, and forward/backward exponents: PASS.'
  printf '%s\n' '- Required tags, resolved references, balanced displays, and status boundaries: PASS.'
  printf '%s\n' '- Python hash seeds 0, 1, and 42 produced byte-identical JSON and Markdown: PASS.'
  printf '%s\n' '- Canonical regeneration was byte-stable for JSON and both reports: PASS.'
  printf '%s\n' '- Independent Ruby exact recomputation and Python-ledger cross-check: PASS.'
  printf '%s\n' '- Eight targeted mutations were rejected by both Python and Ruby: PASS.'
  printf '%s\n' '' 'Rejected mutations: wrong transport sign; `R^-2` cutoff; `R^-4` cutoff;'
  printf '%s\n' 'wrong omega weight; reciprocal p; omission of critical/shorter focusing;'
  printf '%s\n' 'promotion to full clock; and frozen-source drift.' ''
  printf '%s\n' 'The certificate is fail-closed at the W-remote endpoint/payment dichotomy.'
  printf '%s\n' 'Complete K, fixed deletion, arbitrary suitable weak solutions, regularity,'
  printf '%s\n' 'singularity, and Clay remain open. **NOT CLAY.**'
} >"$QA_REPORT"

echo '{"suite":"r075a-spectral-persistence-payment-dichotomy","status":"PASS","mutations":8,"pythonHashSeeds":3}'
