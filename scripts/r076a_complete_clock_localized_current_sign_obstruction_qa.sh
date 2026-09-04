#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
STEM=r076a_complete_clock_localized_current_sign_obstruction
PY_SCRIPT="$ROOT/scripts/$STEM"_certificate.py
RUBY_SCRIPT="$ROOT/scripts/$STEM"_certificate_independent.rb
QA_SCRIPT="$ROOT/scripts/$STEM"_qa.sh
FIXTURES="$ROOT/scripts/$STEM"_fixtures.json
EXPECTED="$ROOT/scripts/$STEM"_expected.json
MAIN="$ROOT/research/$STEM".md
PRIMARY="$ROOT/research/$STEM"_primary_audit.md
SOURCE="$ROOT/research/r076a_report-source.md"
R_SOURCE="$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md"
W_SOURCE="$ROOT/research/r075w_full_frequency_two_harmonic_flux_payment.md"
Z_SOURCE="$ROOT/research/r075z_unresolved_cluster_carrier_current_gate.md"
CERT="$ROOT/research/$STEM"_certificate.json
REPORT="$ROOT/research/$STEM"_certificate_report.md
RUBY_REPORT="$ROOT/research/$STEM"_independent_audit.md
QA_REPORT="$ROOT/research/$STEM"_qa_report.md

EXPECTED_MAIN_HASH=d23532f84702be1630daa0b8d56d02242571dd8a1f8024c59a7f71bec30f26eb
EXPECTED_PRIMARY_HASH=0f7f56d32025f4cd86218f54dfcf5155675f316d2afecdd0007b13ad70240a8d
EXPECTED_SOURCE_HASH=0bbf94774c7d76e623c025a731e0238eca39080c4720a039f080afb038ecad8b
EXPECTED_R_HASH=e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
EXPECTED_W_HASH=571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4
EXPECTED_Z_HASH=30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97
EXPECTED_FIXTURES_HASH=f3644b2a7a641bc92c6c1936f1c05cbed88a6a3e94e25d650c7258ce07b30a31
EXPECTED_EXPECTED_HASH=32d0f99d07d842bf6c9161698249c186c4d23d2f1f33e7f8bd7fc18804887697
EXPECTED_PY_HASH=7dfff7dfb26ccfb9399c0a9cc32a914d5e1d94f3a81ed172f4ec245343d43ab5
EXPECTED_RUBY_HASH=5633861e614cba477f59e8ca4d6f52bc9c29e561178ae07117af53d83cc13366
EXPECTED_CERT_HASH=cd09488885f0e31d95f94c7f46bf0c80b1ad476a438a3fa081d3ec83d4c2949c
EXPECTED_REPORT_HASH=665e69226763e2df99615714829387309a3f66a1ec1e35b19f4af35d005c0d12
EXPECTED_RUBY_REPORT_HASH=cd5608262b4f9c35f30afec9af2a108621f4f89cf8f4a69d973e1e07b6ee670d

TMP_ROOT=$(mktemp -d /tmp/r076a-certificate-qa.XXXXXX)
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
test "$(digest "$R_SOURCE")" = "$EXPECTED_R_HASH"
test "$(digest "$W_SOURCE")" = "$EXPECTED_W_HASH"
test "$(digest "$Z_SOURCE")" = "$EXPECTED_Z_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"
test "$(digest "$PY_SCRIPT")" = "$EXPECTED_PY_HASH"
test "$(digest "$RUBY_SCRIPT")" = "$EXPECTED_RUBY_HASH"
test "$(digest "$CERT")" = "$EXPECTED_CERT_HASH"
test "$(digest "$REPORT")" = "$EXPECTED_REPORT_HASH"
test "$(digest "$RUBY_REPORT")" = "$EXPECTED_RUBY_REPORT_HASH"

grep -q 'Current verdict: \*\*PASS\*\*' "$PRIMARY"
grep -q 'Mathematical blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'Release blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'not represented as proof' "$PRIMARY"

"$PYTHON_BIN" - "$MAIN" "$PRIMARY" "$SOURCE" <<'PY'
import pathlib
import re
import sys

paths = [pathlib.Path(value) for value in sys.argv[1:]]
for path in paths:
    raw = path.read_bytes()
    raw.decode("utf-8")
    bad = [(index, byte) for index, byte in enumerate(raw)
           if (byte < 32 and byte not in (9, 10, 13)) or byte == 127]
    if bad:
        raise SystemExit(f"control bytes in {path}: {bad[:8]}")

text = paths[0].read_text(encoding="utf-8")
tags = [int(value) for value in re.findall(r"\\tag\{A\.(\d+)\}", text)]
if tags != list(range(1, 35)):
    raise SystemExit(f"bad A tag sequence: {tags}")
opens = len(re.findall(r"(?m)^\\\[$", text))
closes = len(re.findall(r"(?m)^\\\]$", text))
if opens != 34 or closes != 34:
    raise SystemExit(f"bad display delimiters: {opens}/{closes}")
refs = [int(value) for value in re.findall(r"\bA\.(\d+)\b", text)]
if set(refs) - set(tags):
    raise SystemExit(f"dangling A references: {sorted(set(refs)-set(tags))}")
if "I_-=\\left[" not in text:
    raise SystemExit("missing escaped left delimiter in A.15")
if "\\frac18\\alpha\\beta-\\frac98\\alpha\\beta" not in text:
    raise SystemExit("missing two escaped fractions in A.28")
PY

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" R076A_JSON="$TMP_ROOT/certificate-$seed.json" \
    R076A_REPORT="$TMP_ROOT/report-$seed.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 15' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"localizedSignDropping": "REJECTED"' "$CERT"
grep -q '"generalClusterCurrentEstimate": "OPEN"' "$CERT"
grep -q '"fullZSectorPayment": "OPEN"' "$CERT"
grep -q '"carrier": 176' "$CERT"
grep -q '"currentUpper": "-9/176"' "$CERT"
grep -q '"correctionDensity": "-351/121"' "$CERT"
grep -q '"fullGradient": "30625/121"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R076A_JSON="$CERT" R076A_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
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
  if env PYTHONHASHSEED=0 R076A_MUTATION="$mutation" \
    R076A_JSON="$TMP_ROOT/python-$mutation.json" R076A_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    printf '%s\n' "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R076A_JSON="$CERT" R076A_RUBY_MUTATION="$mutation" \
    R076A_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    printf '%s\n' "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R076A_MUTATION=unknown_mutation R076A_JSON="$TMP_ROOT/unknown-python.json" \
  R076A_REPORT="$TMP_ROOT/unknown-python.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  printf '%s\n' 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076A_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R076A_JSON="$CERT" R076A_RUBY_MUTATION=unknown_mutation \
  R076A_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  printf '%s\n' 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076A_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R076A_JSON="$CERT" R076A_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
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
  printf '%s\n' '# R0.76A certificate QA report' ''
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
  printf '%s\n' "| research/r076a_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/"$STEM"_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/"$STEM"_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/"$STEM"_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/"$STEM"_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/"$STEM"_qa.sh | $qa_hash |"
  printf '%s\n' "| research/"$STEM"_certificate.json | $cert_hash |"
  printf '%s\n' "| research/"$STEM"_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/"$STEM"_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- A.1--A.34, 34/34 tags and displays, three frozen dependencies, references, UTF-8, controls, and TeX escapes: PASS.'
  printf '%s\n' '- Exact primitive support/mass, integer-frequency cluster, clock scaling, damping, phase, and point ledgers: PASS.'
  printf '%s\n' '- Uniform localized-current and correction-density signs are audited independently: PASS.'
  printf '%s\n' '- Finite fixtures are explicitly excluded as proof of the continuum identities: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable to this analytic gate; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'The bounded source report is contextual and makes no novelty or priority claim.'
  printf '%s\n' 'R0.76A rejects only localized sign-dropping.  General cluster payment,'
  printf '%s\n' 'Version-M transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r076a-complete-clock-localized-current-sign-obstruction","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$mutation_total"
