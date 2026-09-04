#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
STEM=r076d_quantitative_growing_mode_entropy_window
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/${STEM}_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/${STEM}_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/${STEM}_qa.sh"
FIXTURES="$ROOT/scripts/${STEM}_fixtures.json"
EXPECTED="$ROOT/scripts/${STEM}_expected.json"
MAIN="$ROOT/research/${STEM}.md"
PRIMARY="$ROOT/research/${STEM}_primary_audit.md"
SOURCE="$ROOT/research/r076d_report-source.md"
C_SOURCE="$ROOT/research/r076c_full_frequency_fixed_mode_flux_payment.md"
R_SOURCE="$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md"
CLOCK_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
CERT="$ROOT/research/${STEM}_certificate.json"
REPORT="$ROOT/research/${STEM}_certificate_report.md"
RUBY_REPORT="$ROOT/research/${STEM}_independent_audit.md"
QA_REPORT="$ROOT/research/${STEM}_qa_report.md"

EXPECTED_MAIN_HASH=cd94e3384f01963cb7b8a14fdb8376c6197c361473447f15500db0acac5e958e
EXPECTED_PRIMARY_HASH=9b99247ceb34cadc12c7f4f0858be642316ca80d1ff83d05dfd745a9906356d8
EXPECTED_SOURCE_HASH=f2358780d382dcace69b7ebef855bf3c8e63d15b581dc86b62b7e3c751fbd310
EXPECTED_C_HASH=2b2f4a2b353645e72ca54bfc06495a9f52329498b9c16a9e451ca7b3456f6bbf
EXPECTED_R_HASH=e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
EXPECTED_CLOCK_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_FIXTURES_HASH=ffe5c2b9a1a6b0c20b710dc45fcac9543069ea6af38dce34804665012984b374
EXPECTED_EXPECTED_HASH=eb5dd9ebaa6a74cbc7f999fdbd55ee54a50588342c3dfba9412ac53c935ba2dd
EXPECTED_PY_HASH=ed96f55b1326f1e7c1330670c132c523c7861f53edcb046b662159d83e60ce54
EXPECTED_RUBY_HASH=9f12fa2aadc35dfb228e8f0ab60eec420c5c6bdfa306f1b66ca4828cdde4d391
EXPECTED_CERT_HASH=e57d160e8b3b37ed714e884750f50abbaaaac25a1e3ec3ba395a0193e0b6757d
EXPECTED_REPORT_HASH=460917d50cd9aeeb4af5898322915d67fa8ec3e1971f2e5945becf858ccd9c94
EXPECTED_RUBY_REPORT_HASH=0d6e3b7f363fdb9e031a228038ae7af4152d51d101e6050f39c4de7dc21fa69a

TMP_ROOT=$(mktemp -d /tmp/r076d-certificate-qa.XXXXXX)
trap 'rm -rf "$TMP_ROOT"' EXIT

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

command -v "$PYTHON_BIN" >/dev/null
command -v ruby >/dev/null
"$PYTHON_BIN" -B -c 'import pathlib,sys; compile(pathlib.Path(sys.argv[1]).read_text(), sys.argv[1], "exec")' "$PY_SCRIPT"
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"
"$PYTHON_BIN" -m json.tool "$FIXTURES" >"$TMP_ROOT/fixtures.pretty"
"$PYTHON_BIN" -m json.tool "$EXPECTED" >"$TMP_ROOT/expected.pretty"

test "$(digest "$MAIN")" = "$EXPECTED_MAIN_HASH"
test "$(digest "$PRIMARY")" = "$EXPECTED_PRIMARY_HASH"
test "$(digest "$SOURCE")" = "$EXPECTED_SOURCE_HASH"
test "$(digest "$C_SOURCE")" = "$EXPECTED_C_HASH"
test "$(digest "$R_SOURCE")" = "$EXPECTED_R_HASH"
test "$(digest "$CLOCK_SOURCE")" = "$EXPECTED_CLOCK_HASH"
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
grep -q 'finite arithmetic is not proof' "$REPORT"
grep -q 'not proof of Turan--Nazarov' "$RUBY_REPORT"

"$PYTHON_BIN" - "$MAIN" "$PRIMARY" "$SOURCE" <<'PY'
import pathlib
import re
import sys

paths = [pathlib.Path(value) for value in sys.argv[1:]]
for path in paths:
    raw = path.read_bytes()
    raw.decode("utf-8")
    bad = [(i, b) for i, b in enumerate(raw)
           if (b < 32 and b not in (9, 10, 13)) or b == 127]
    if bad:
        raise SystemExit(f"control bytes in {path}: {bad[:8]}")
    if b"\r" in raw:
        raise SystemExit(f"CR byte in {path}")

text = paths[0].read_text(encoding="utf-8")
tags = [int(value) for value in re.findall(r"\\tag\{D\.(\d+)\}", text)]
if tags != list(range(1, 42)):
    raise SystemExit(f"bad D tag sequence: {tags}")
opens = len(re.findall(r"(?m)^\\\[$", text))
closes = len(re.findall(r"(?m)^\\\]$", text))
if opens != 41 or closes != 41:
    raise SystemExit(f"bad display delimiters: {opens}/{closes}")
refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])D\.(\d+)", text)]
if set(refs) - set(tags):
    raise SystemExit(f"dangling D references: {sorted(set(refs)-set(tags))}")
for required in (
    r"q(L)\log(q(L)+1)=o(L^2)",
    r"\left(\frac54\right)^m",
    r"\frac{(m+1)!}{4}",
    r"\lambda^{-1/3}H^{2/3}",
    r"-\frac2{11907}",
):
    if required not in text:
        raise SystemExit(f"missing TeX fragment: {required}")
if re.search(r"(?<!\\)\bqquad\b", text):
    raise SystemExit("bare qquad token")
PY

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" R076D_JSON="$TMP_ROOT/certificate-$seed.json" \
    R076D_REPORT="$TMP_ROOT/report-$seed.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"assertionsTotal": 123' "$CERT"
grep -q '"factorialOverFour": 9979200' "$CERT"
grep -q '"gradientCoefficient": "257/64"' "$CERT"
grep -q '"weightedLambdaPower": "-1/3"' "$CERT"
grep -q '"endpointLambdaPower": "0"' "$CERT"
grep -q '"frozenRate": "-2/11907"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R076D_JSON="$CERT" R076D_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Verdict: \*\*PASS\*\*' "$RUBY_REPORT"
grep -q 'Ruby assertions: 123/123' "$RUBY_REPORT"
grep -q 'Python/Ruby exact sections identical: PASS (6/6)' "$RUBY_REPORT"

mutations=$("$PYTHON_BIN" -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {n++} END {print n+0}')
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R076D_MUTATION="$mutation" \
    R076D_JSON="$TMP_ROOT/python-$mutation.json" R076D_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    printf '%s\n' "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R076D_JSON="$CERT" R076D_RUBY_MUTATION="$mutation" \
    R076D_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    printf '%s\n' "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$mutation_total" -eq 123
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R076D_MUTATION=unknown_mutation R076D_JSON="$TMP_ROOT/unknown-python.json" \
  R076D_REPORT="$TMP_ROOT/unknown-python.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  printf '%s\n' 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076D_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R076D_JSON="$CERT" R076D_RUBY_MUTATION=unknown_mutation \
  R076D_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  printf '%s\n' 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076D_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

: >"$QA_REPORT"
core_count=$(find "$ROOT/research" "$ROOT/scripts" -maxdepth 1 -type f \
  \( -name 'r076d_*' -o -name 'r076d-*' \) \
  ! -name 'r076d_publication_handoff*' | wc -l | tr -d ' ')
test "$core_count" -eq 12

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
  printf '%s\n' '# R0.76D certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 123/123'
  printf '%s\n' '- Ruby assertions: 123/123'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' '- Python/Ruby exact sections identical: PASS (6/6)'
  printf '%s\n' '- Exact core inventory: 12/12 files'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  printf '%s\n' "| research/$STEM.md | $main_hash |"
  printf '%s\n' "| research/${STEM}_primary_audit.md | $primary_hash |"
  printf '%s\n' "| research/r076d_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/${STEM}_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/${STEM}_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/${STEM}_qa.sh | $qa_hash |"
  printf '%s\n' "| research/${STEM}_certificate.json | $cert_hash |"
  printf '%s\n' "| research/${STEM}_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/${STEM}_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- D.1--D.41, 41/41 display blocks, three frozen dependencies, references, UTF-8, controls, CR, and TeX escapes: PASS.'
  printf '%s\n' '- Exact q=3, N=6 fixture: m=10, 11!/4=9,979,200, lambda=4, T=16, and gradient coefficient 257/64: PASS.'
  printf '%s\n' '- Erdelyi half-scale coefficients alpha+14e and returned derivative 2alpha+28e are recomputed independently: PASS.'
  printf '%s\n' '- Weighted onset exponent lambda^(-1/3), terminal exponent lambda^0, physical exponents, and frozen rate -2/11907: PASS.'
  printf '%s\n' '- The (5/4)^m endpoint comparison inserted after adversarial audit is present and certified: PASS.'
  printf '%s\n' '- R0.75R compatibility, exact-shear scope, growing constant, Version-M condition, and NOT CLAY boundary: PASS.'
  printf '%s\n' '- Finite fixtures are explicitly excluded as proof of the imported continuum inequalities or analytic flux theorem: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable to this analytic theorem; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'R0.76D quantifies the fixed-mode constant by exp(C q log(q+1)) and proves only the stated exact-shear growing-mode window.'
  printf '%s\n' 'Arbitrary packets, Version-M extraction, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r076d-quantitative-growing-mode-entropy-window","status":"PASS","assertions":123,"mutations":%s,"pythonHashSeeds":3,"coreFiles":12}\n' "$mutation_total"
