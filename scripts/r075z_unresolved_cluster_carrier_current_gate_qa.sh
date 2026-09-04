#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
STEM=r075z_unresolved_cluster_carrier_current_gate
PY_SCRIPT="$ROOT/scripts/$STEM"_certificate.py
RUBY_SCRIPT="$ROOT/scripts/$STEM"_certificate_independent.rb
QA_SCRIPT="$ROOT/scripts/$STEM"_qa.sh
FIXTURES="$ROOT/scripts/$STEM"_fixtures.json
EXPECTED="$ROOT/scripts/$STEM"_expected.json
MAIN="$ROOT/research/$STEM".md
PRIMARY="$ROOT/research/$STEM"_primary_audit.md
SOURCE="$ROOT/research/r075z_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
R_SOURCE="$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md"
X_SOURCE="$ROOT/research/r075x_fixed_finite_mode_low_carrier_payment.md"
Y_SOURCE="$ROOT/research/r075y_strongly_separated_multimode_flux_payment.md"
CERT="$ROOT/research/$STEM"_certificate.json
REPORT="$ROOT/research/$STEM"_certificate_report.md
RUBY_REPORT="$ROOT/research/$STEM"_independent_audit.md
QA_REPORT="$ROOT/research/$STEM"_qa_report.md

EXPECTED_MAIN_HASH=30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97
EXPECTED_PRIMARY_HASH=895d09e0b403c0a6bcf216624527dd6c2bf76f15d7ce5f6b6b0a31b6f64a1eb0
EXPECTED_SOURCE_HASH=9b071b3e020210922834435ea7e5806620479d400eb044f48f34e7b02c259d4c
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_R_HASH=e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
EXPECTED_X_HASH=8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763
EXPECTED_Y_HASH=74790f910b596c86b204291d997ef723cabbc85d14a89e3fe900814fcd88b0a6
EXPECTED_FIXTURES_HASH=9bd703f41f4b4823a4b6fe38136bf2a5bef126cf15edb3b54036cf1b80e4f4b0
EXPECTED_EXPECTED_HASH=6043f94b70b6068a58d7716877a5319edc9edfc90b47bfee23ea7baee0ad58d4

TMP_ROOT=$(mktemp -d /tmp/r075z-certificate-qa.XXXXXX)
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
test "$(digest "$X_SOURCE")" = "$EXPECTED_X_HASH"
test "$(digest "$Y_SOURCE")" = "$EXPECTED_Y_HASH"
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
bad_spacing = re.findall(r"(?<![\\A-Za-z])(?:quad|qquad|mathcal)\b", text)
if bad_spacing:
    raise SystemExit(f"unescaped TeX command fragments: {bad_spacing}")
tags = [int(value) for value in re.findall(r"\\tag\{Z\.(\d+)\}", text)]
if tags != list(range(1, 32)):
    raise SystemExit(f"bad Z tag sequence: {tags}")
opens = len(re.findall(r"(?m)^\\\[$", text))
closes = len(re.findall(r"(?m)^\\\]$", text))
if opens != 31 or closes != 31:
    raise SystemExit(f"bad display delimiters: {opens}/{closes}")
PY

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" R075Z_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075Z_REPORT="$TMP_ROOT/report-$seed.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 15' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"threshold": 16' "$CERT"
grep -q '"sector": "X"' "$CERT"
grep -q '"sector": "Y"' "$CERT"
grep -q '"sector": "Z"' "$CERT"
grep -q '"weightedCurrent": 32' "$CERT"
grep -q '"modulatedDissipationDensity": -31' "$CERT"
grep -q '"fullGradientOver2Pi": 1313' "$CERT"
grep -q '"pdeResidual"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075Z_JSON="$CERT" R075Z_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":15' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 15/15' "$RUBY_REPORT"
grep -q 'Blocker count: 0' "$RUBY_REPORT"

mutations=$("$PYTHON_BIN" -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {n++} END {print n+0}')
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R075Z_MUTATION="$mutation" \
    R075Z_JSON="$TMP_ROOT/python-$mutation.json" R075Z_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    printf '%s\n' "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R075Z_JSON="$CERT" R075Z_RUBY_MUTATION="$mutation" \
    R075Z_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    printf '%s\n' "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R075Z_MUTATION=unknown_mutation R075Z_JSON="$TMP_ROOT/unknown-python.json" \
  R075Z_REPORT="$TMP_ROOT/unknown-python.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  printf '%s\n' 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075Z_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075Z_JSON="$CERT" R075Z_RUBY_MUTATION=unknown_mutation \
  R075Z_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  printf '%s\n' 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075Z_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075Z_JSON="$CERT" R075Z_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
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
  printf '%s\n' '# R0.75Z certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 15/15'
  printf '%s\n' '- Ruby assertions: 15/15'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  printf '%s\n' "| research/$STEM.md | $main_hash |"
  printf '%s\n' "| research/"$STEM"_primary_audit.md | $primary_hash |"
  printf '%s\n' "| research/r075z_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/"$STEM"_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/"$STEM"_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/"$STEM"_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/"$STEM"_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/"$STEM"_qa.sh | $qa_hash |"
  printf '%s\n' "| research/"$STEM"_certificate.json | $cert_hash |"
  printf '%s\n' "| research/"$STEM"_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/"$STEM"_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- Z.1--Z.31, 31/31 tags and displays, four dependencies, references, UTF-8, controls, and TeX spacing: PASS.'
  printf '%s\n' '- Exact fixed-q X/Y/Z partition, including strict low branch and equality separator: PASS.'
  printf '%s\n' '- Exact carrier-envelope PDE, square split, local current, and full-period Fourier ledgers: PASS.'
  printf '%s\n' '- The point fixture rejects only carrier-uniform absorption of the N-weighted absolute current: PASS.'
  printf '%s\n' '- Finite fixtures are explicitly excluded as proof of the continuum identities: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable to this analytic gate; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'The bounded source report classifies local-observation literature as context, not proof or novelty evidence.'
  printf '%s\n' 'Z closes the parameter partition and one naive recursion route only.'
  printf '%s\n' 'The full clustered-sector payment, cross-cluster aggregation, Version-M transfer,'
  printf '%s\n' 'regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075z-unresolved-cluster-carrier-current-gate","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$mutation_total"
