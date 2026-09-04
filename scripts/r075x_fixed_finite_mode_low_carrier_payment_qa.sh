#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
STEM=r075x_fixed_finite_mode_low_carrier_payment
PY_SCRIPT="$ROOT/scripts/${STEM}_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/${STEM}_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/${STEM}_qa.sh"
FIXTURES="$ROOT/scripts/${STEM}_fixtures.json"
EXPECTED="$ROOT/scripts/${STEM}_expected.json"
MAIN="$ROOT/research/${STEM}.md"
PRIMARY="$ROOT/research/${STEM}_primary_audit.md"
SOURCE="$ROOT/research/r075x_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
R_SOURCE="$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md"
W_SOURCE="$ROOT/research/r075w_full_frequency_two_harmonic_flux_payment.md"
CERT="$ROOT/research/${STEM}_certificate.json"
REPORT="$ROOT/research/${STEM}_certificate_report.md"
RUBY_REPORT="$ROOT/research/${STEM}_independent_audit.md"
QA_REPORT="$ROOT/research/${STEM}_qa_report.md"

EXPECTED_MAIN_HASH=8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763
EXPECTED_PRIMARY_HASH=8fffbf0c8ad50d5765c734f8e5627ce0dbe0d6b2aad4bcb26aa5c298f6143b2c
EXPECTED_SOURCE_HASH=8fa756c7efe2660dbc5eeb51e2a11d10dce58f36f4c0d0f757000be1447b7f34
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_R_HASH=e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
EXPECTED_W_HASH=571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4
EXPECTED_FIXTURES_HASH=de231e977d9a2551222f0a4f0a8ebcb65490f76574bc4fa494db480e2b61a0e9
EXPECTED_EXPECTED_HASH=879ff3458050e712048654eb91623a00e5436a22f12c6b814fb137aa8af96311

TMP_ROOT=$(mktemp -d /tmp/r075x-certificate-qa.XXXXXX)
trap 'rm -rf "$TMP_ROOT"' EXIT

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

command -v "$PYTHON_BIN" >/dev/null
command -v ruby >/dev/null
"$PYTHON_BIN" -B -c 'import pathlib, sys; compile(pathlib.Path(sys.argv[1]).read_text(), sys.argv[1], "exec")' "$PY_SCRIPT"
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"
"$PYTHON_BIN" -m json.tool "$FIXTURES" >"$TMP_ROOT/fixtures.pretty"
"$PYTHON_BIN" -m json.tool "$EXPECTED" >"$TMP_ROOT/expected.pretty"

test "$(digest "$MAIN")" = "$EXPECTED_MAIN_HASH"
test "$(digest "$PRIMARY")" = "$EXPECTED_PRIMARY_HASH"
test "$(digest "$SOURCE")" = "$EXPECTED_SOURCE_HASH"
test "$(digest "$B_SOURCE")" = "$EXPECTED_B_HASH"
test "$(digest "$R_SOURCE")" = "$EXPECTED_R_HASH"
test "$(digest "$W_SOURCE")" = "$EXPECTED_W_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q 'Current verdict: \*\*PASS\*\*' "$PRIMARY"
grep -q 'Mathematical blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'Release blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'not represented as proof' "$PRIMARY"

"$PYTHON_BIN" - "$MAIN" <<'PY'
import pathlib
import re
import sys

text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
bad_spacing = re.findall(r"(?<![\\A-Za-z])(?:quad|qquad)\b", text)
if bad_spacing:
    raise SystemExit(f"unescaped TeX spacing commands: {bad_spacing}")
if "+|\\partial_zG" in text:
    raise SystemExit("damaged derivative norm delimiter")
PY

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" R075X_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075X_REPORT="$TMP_ROOT/report-$seed.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 18' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"T": "1/16"' "$CERT"
grep -q '"order": 6' "$CERT"
grep -q '"fullyConfluentDegree": 5' "$CERT"
grep -q '"maximumTerms": 6' "$CERT"
grep -q '"turanExponent": 5' "$CERT"
grep -q '"heatCancellation": "0"' "$CERT"
grep -q '"frozenRate": "-2/11907"' "$CERT"
grep -q '"R": 0' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075X_JSON="$CERT" R075X_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":19' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 19/19' "$RUBY_REPORT"
grep -q 'Blocker count: 0' "$RUBY_REPORT"

mutations=$("$PYTHON_BIN" -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {n++} END {print n+0}')
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R075X_MUTATION="$mutation" \
    R075X_JSON="$TMP_ROOT/python-$mutation.json" R075X_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R075X_JSON="$CERT" R075X_RUBY_MUTATION="$mutation" \
    R075X_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R075X_MUTATION=unknown_mutation R075X_JSON="$TMP_ROOT/unknown-python.json" \
  R075X_REPORT="$TMP_ROOT/unknown-python.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075X_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075X_JSON="$CERT" R075X_RUBY_MUTATION=unknown_mutation \
  R075X_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075X_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075X_JSON="$CERT" R075X_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_hash=$(digest "$PRIMARY")
source_hash=$(digest "$SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75X certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 18/18'
  printf '%s\n' '- Ruby assertions: 19/19'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  printf '%s\n' "| research/${STEM}.md | $main_hash |"
  printf '%s\n' "| research/${STEM}_primary_audit.md | $primary_hash |"
  printf '%s\n' "| research/r075x_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/${STEM}_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/${STEM}_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/${STEM}_qa.sh | $qa_hash |"
  printf '%s\n' "| research/${STEM}_certificate.json | $cert_hash |"
  printf '%s\n' "| research/${STEM}_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/${STEM}_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- X.1--X.36, 36/36 tags and displays, three dependencies, references, UTF-8, controls, and TeX-spacing commands: PASS.'
  printf '%s\n' '- Fixed q=3 exact fixture, low-carrier scaling, six-dimensional companion row, and six-term trace ledger: PASS.'
  printf '%s\n' '- Fully confluent degree-five boundary, radial primitive, and exact local-energy signs: PASS.'
  printf '%s\n' '- Flux, mass, Holder, normalization, and exact rate -2/11907 ledgers: PASS.'
  printf '%s\n' '- Finite fixtures are explicitly excluded as proof of the continuum compactness and Turan--Nazarov lemmas: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable to this analytic theorem; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'The source report is byte-bound and limits the imported result to the Turan--Nazarov inequality.'
  printf '%s\n' 'X proves the low-carrier estimate for each fixed finite harmonic family.'
  printf '%s\n' 'Uniform q-growth, high carriers for three or more modes, arbitrary packets, E.24,'
  printf '%s\n' 'Version-M extraction, suitable-weak transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075x-fixed-finite-mode-low-carrier-payment","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$mutation_total"
