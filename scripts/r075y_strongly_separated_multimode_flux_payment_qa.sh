#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
STEM=r075y_strongly_separated_multimode_flux_payment
PY_SCRIPT="$ROOT/scripts/$STEM"_certificate.py
RUBY_SCRIPT="$ROOT/scripts/$STEM"_certificate_independent.rb
QA_SCRIPT="$ROOT/scripts/$STEM"_qa.sh
FIXTURES="$ROOT/scripts/$STEM"_fixtures.json
EXPECTED="$ROOT/scripts/$STEM"_expected.json
MAIN="$ROOT/research/$STEM".md
PRIMARY="$ROOT/research/$STEM"_primary_audit.md
SOURCE="$ROOT/research/r075y_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
R_SOURCE="$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md"
U_SOURCE="$ROOT/research/r075u_two_harmonic_difference_frequency_payment.md"
X_SOURCE="$ROOT/research/r075x_fixed_finite_mode_low_carrier_payment.md"
CERT="$ROOT/research/$STEM"_certificate.json
REPORT="$ROOT/research/$STEM"_certificate_report.md
RUBY_REPORT="$ROOT/research/$STEM"_independent_audit.md
QA_REPORT="$ROOT/research/$STEM"_qa_report.md

EXPECTED_MAIN_HASH=74790f910b596c86b204291d997ef723cabbc85d14a89e3fe900814fcd88b0a6
EXPECTED_PRIMARY_HASH=f7e1feedd1fa359877554eff4fa20c470f727ae7743c990136525ad22d6cdf3b
EXPECTED_SOURCE_HASH=e6d6b1ed2830b46fc901a9ab09ef368f258f13dfc8c0961076baedd5b46e1589
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_R_HASH=e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
EXPECTED_U_HASH=f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4
EXPECTED_X_HASH=8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763
EXPECTED_FIXTURES_HASH=45448bf75c867b3f9654db79c77ae52b9bd35d7e781b240f564a9d871faab32b
EXPECTED_EXPECTED_HASH=324e92dd32d6e1ca76b22c47a201206e1c924e1100b92de1c8429ffd17ac25d3

TMP_ROOT=$(mktemp -d /tmp/r075y-certificate-qa.XXXXXX)
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
test "$(digest "$U_SOURCE")" = "$EXPECTED_U_HASH"
test "$(digest "$X_SOURCE")" = "$EXPECTED_X_HASH"
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
tags = [int(value) for value in re.findall(r"\\tag\{Y\.(\d+)\}", text)]
if tags != list(range(1, 40)):
    raise SystemExit(f"bad Y tag sequence: {tags}")
if text.count("\\[") != 39 or text.count("\\]") != 39:
    raise SystemExit("display delimiter count is not 39/39")
PY

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" R075Y_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075Y_REPORT="$TMP_ROOT/report-$seed.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 17' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"T": "1/100"' "$CERT"
grep -q '"minimumSignedGap": 96' "$CERT"
grep -q '"separationProduct": 24' "$CERT"
grep -q '"offDiagonalCoefficient": "5/48"' "$CERT"
grep -q '"retainedDiagonalCoefficient": "7/48"' "$CERT"
grep -q '"totalRows": 9' "$CERT"
grep -q '"R": 0' "$CERT"
grep -q '"frozenRate": "-2/11907"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075Y_JSON="$CERT" R075Y_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":18' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 18/18' "$RUBY_REPORT"
grep -q 'Blocker count: 0' "$RUBY_REPORT"

mutations=$("$PYTHON_BIN" -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {n++} END {print n+0}')
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R075Y_MUTATION="$mutation" \
    R075Y_JSON="$TMP_ROOT/python-$mutation.json" R075Y_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R075Y_JSON="$CERT" R075Y_RUBY_MUTATION="$mutation" \
    R075Y_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R075Y_MUTATION=unknown_mutation R075Y_JSON="$TMP_ROOT/unknown-python.json" \
  R075Y_REPORT="$TMP_ROOT/unknown-python.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075Y_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075Y_JSON="$CERT" R075Y_RUBY_MUTATION=unknown_mutation \
  R075Y_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075Y_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075Y_JSON="$CERT" R075Y_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
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
  printf '%s\n' '# R0.75Y certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 17/17'
  printf '%s\n' '- Ruby assertions: 18/18'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  printf '%s\n' "| research/$STEM.md | $main_hash |"
  printf '%s\n' "| research/"$STEM"_primary_audit.md | $primary_hash |"
  printf '%s\n' "| research/r075y_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/"$STEM"_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/"$STEM"_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/"$STEM"_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/"$STEM"_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/"$STEM"_qa.sh | $qa_hash |"
  printf '%s\n' "| research/"$STEM"_certificate.json | $cert_hash |"
  printf '%s\n' "| research/"$STEM"_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/"$STEM"_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- Y.1--Y.39, 39/39 tags and displays, four dependencies, references, UTF-8, controls, and TeX spacing: PASS.'
  printf '%s\n' '- Exact q=3 fixture, six signed modes, separation product 24, and strict Gram margin: PASS.'
  printf '%s\n' '- Complete-clock slow/fast regimes, cutoff onset, and physical R^(-4/3) row scale: PASS.'
  printf '%s\n' '- Exactly q^2 Fourier rows, radial quotient, plateau mass, normalization, and rate -2/11907: PASS.'
  printf '%s\n' '- Finite fixtures are explicitly excluded as proof of the continuum Gram and complete-clock lemmas: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable to this analytic theorem; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'The source report treats separated-frequency observability as classical context and makes no novelty claim.'
  printf '%s\n' 'Y proves only the strongly separated exact-shear class, with explicit q^2 cost.'
  printf '%s\n' 'Unresolved clusters, arbitrary packets, E.24, Version-M extraction, suitable-weak transfer,'
  printf '%s\n' 'regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075y-strongly-separated-multimode-flux-payment","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$mutation_total"
