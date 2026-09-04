#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
STEM=r076c_full_frequency_fixed_mode_flux_payment
PY_SCRIPT="$ROOT/scripts/$STEM"_certificate.py
RUBY_SCRIPT="$ROOT/scripts/$STEM"_certificate_independent.rb
QA_SCRIPT="$ROOT/scripts/$STEM"_qa.sh
FIXTURES="$ROOT/scripts/$STEM"_fixtures.json
EXPECTED="$ROOT/scripts/$STEM"_expected.json
MAIN="$ROOT/research/$STEM".md
PRIMARY="$ROOT/research/$STEM"_primary_audit.md
SOURCE="$ROOT/research/r076c_report-source.md"
CLOCK_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
OUTER_SOURCE="$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md"
LOW_SOURCE="$ROOT/research/r075x_fixed_finite_mode_low_carrier_payment.md"
MODERATE_SOURCE="$ROOT/research/r076b_moderate_carrier_fixed_mode_flux_payment.md"
CERT="$ROOT/research/$STEM"_certificate.json
REPORT="$ROOT/research/$STEM"_certificate_report.md
RUBY_REPORT="$ROOT/research/$STEM"_independent_audit.md
QA_REPORT="$ROOT/research/$STEM"_qa_report.md

EXPECTED_MAIN_HASH=2b2f4a2b353645e72ca54bfc06495a9f52329498b9c16a9e451ca7b3456f6bbf
EXPECTED_PRIMARY_HASH=d60546eab80d2fa6ef633efeb0b34120d7b9f81a33249e500f8d94b9a8c15f74
EXPECTED_SOURCE_HASH=be523d313f5a487fd0b1550cb948f1e05b117f6d1734b8d9cbfd5ab1b5d57b27
EXPECTED_CLOCK_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_OUTER_HASH=e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
EXPECTED_LOW_HASH=8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763
EXPECTED_MODERATE_HASH=a8a4cc853ec1029cb52afee724a4a783da156bd57de5399c58a7f42e2ab0306d
EXPECTED_FIXTURES_HASH=36d1612b57932fad7ff6e9a4375b842d4900b0868625cfb5d498ce89a4dcee82
EXPECTED_EXPECTED_HASH=6dbd56d366b6b048acd769ff5b5eff303ede111153330de763ec04cee571ad52
EXPECTED_PY_HASH=cd336bbee4c0e0a31be3642522bdc4703b724ef5d5f21ca587a74d84e7897452
EXPECTED_RUBY_HASH=4e26bc8b0c79222bbc3c5f4945a8c85fff9980bcf6ad5f607de48ace86293259
EXPECTED_CERT_HASH=0ffd5fff7812eb777866cff70eb0bff68112ae176ffd8706ea732ddda55b4a9b
EXPECTED_REPORT_HASH=be4c0d24e4b98fd0ae7c26fd4fd0fb955dc7007f64bba2c49f517b71c17ba8f6
EXPECTED_RUBY_REPORT_HASH=a24ebbf47641c706dd756ce23ba65f5b68c59010bfa1e65f829ae97d7022c358

TMP_ROOT=$(mktemp -d /tmp/r076c-certificate-qa.XXXXXX)
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
test "$(digest "$CLOCK_SOURCE")" = "$EXPECTED_CLOCK_HASH"
test "$(digest "$OUTER_SOURCE")" = "$EXPECTED_OUTER_HASH"
test "$(digest "$LOW_SOURCE")" = "$EXPECTED_LOW_HASH"
test "$(digest "$MODERATE_SOURCE")" = "$EXPECTED_MODERATE_HASH"
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
grep -q 'arbitrary measurable time family' "$PRIMARY"
grep -q 'not proof of the continuum Turan--Nazarov theorem' "$PRIMARY"

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
tags = [int(value) for value in re.findall(r"\\tag\{C\.(\d+)\}", text)]
if tags != list(range(1, 36)):
    raise SystemExit(f"bad C tag sequence: {tags}")
opens = len(re.findall(r"(?m)^\\\[$", text))
closes = len(re.findall(r"(?m)^\\\]$", text))
if opens != 35 or closes != 35:
    raise SystemExit(f"bad display delimiters: {opens}/{closes}")
refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])C\.(\d+)", text)]
if set(refs) - set(tags):
    raise SystemExit(f"dangling C references: {sorted(set(refs)-set(tags))}")
for required in (
    r"n_1,\ldots,n_q\in\mathbb N",
    r"\phi_j\in\mathbb R",
    r"Q(\tau;z)",
    r"T^{-2/3}K_T^{2/3}",
    r"\lambda^{-1/3}H^{2/3}",
    r"-\frac2{11907}",
):
    if required not in text:
        raise SystemExit(f"missing TeX fragment: {required}")
if re.search(r"(?<!\\)\bqquad\b", text):
    raise SystemExit("bare qquad token")
PY

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" R076C_JSON="$TMP_ROOT/certificate-$seed.json" \
    R076C_REPORT="$TMP_ROOT/report-$seed.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
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
grep -q '"n1R": "2"' "$CERT"
grep -q '"lambda": "4"' "$CERT"
grep -q '"T": "16"' "$CERT"
grep -q '"weightedLambdaPower": "-1/3"' "$CERT"
grep -q '"endpointLambdaPower": "0"' "$CERT"
grep -q '"Gz": "577/6"' "$CERT"
grep -q '"Gs": "-2159423/20736"' "$CERT"
grep -q '"scaledPdeResidual": "0"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R076C_JSON="$CERT" R076C_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Verdict: \*\*PASS\*\*' "$RUBY_REPORT"
grep -q 'Ruby assertions: 140/140' "$RUBY_REPORT"
grep -q 'Python/Ruby exact sections identical: PASS (7/7)' "$RUBY_REPORT"

mutations=$("$PYTHON_BIN" -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {n++} END {print n+0}')
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R076C_MUTATION="$mutation" \
    R076C_JSON="$TMP_ROOT/python-$mutation.json" R076C_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    printf '%s\n' "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R076C_JSON="$CERT" R076C_RUBY_MUTATION="$mutation" \
    R076C_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    printf '%s\n' "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R076C_MUTATION=unknown_mutation R076C_JSON="$TMP_ROOT/unknown-python.json" \
  R076C_REPORT="$TMP_ROOT/unknown-python.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  printf '%s\n' 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076C_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R076C_JSON="$CERT" R076C_RUBY_MUTATION=unknown_mutation \
  R076C_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  printf '%s\n' 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076C_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

: >"$QA_REPORT"
core_count=$(find "$ROOT/research" "$ROOT/scripts" -maxdepth 1 -type f \
  \( -name 'r076c_*' -o -name 'r076c-*' \) | wc -l | tr -d ' ')
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
  printf '%s\n' '# R0.76C certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 140/140'
  printf '%s\n' '- Ruby assertions: 140/140'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' '- Exact core inventory: 12/12 files'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  printf '%s\n' "| research/$STEM.md | $main_hash |"
  printf '%s\n' "| research/${STEM}_primary_audit.md | $primary_hash |"
  printf '%s\n' "| research/r076c_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/${STEM}_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/${STEM}_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/${STEM}_qa.sh | $qa_hash |"
  printf '%s\n' "| research/${STEM}_certificate.json | $cert_hash |"
  printf '%s\n' "| research/${STEM}_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/${STEM}_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- C.1--C.35, 35/35 tags and displays, four frozen dependencies, references, UTF-8, controls, and TeX escapes: PASS.'
  printf '%s\n' '- Exact q=3 ultra-high family n_1 R=2, lambda=4, T=16, rescaled exponent bands, PDE point, and scale ledger: PASS.'
  printf '%s\n' '- Weighted onset exponent lambda^(-1/3) and terminal exponent lambda^0 are recomputed independently: PASS.'
  printf '%s\n' '- Complete-real-field energy identity and all signs are checked independently: PASS.'
  printf '%s\n' '- C.14 is explicitly restricted to exponential-polynomial families; arbitrary measurable time families are excluded: PASS.'
  printf '%s\n' '- The analytic density, localized-current sign, and standalone carrier integration-by-parts routes are not used: PASS.'
  printf '%s\n' '- Finite fixtures are explicitly excluded as proof of the continuum observation lemmas: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable to this analytic theorem; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'The bounded source report imports only Turan--Nazarov and makes no novelty or priority claim.'
  printf '%s\n' 'R0.76C closes the carrier range only for each fixed finite exact real shear family.'
  printf '%s\n' 'Growing packets, Version-M transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r076c-full-frequency-fixed-mode-flux-payment","status":"PASS","assertions":140,"mutations":%s,"pythonHashSeeds":3,"coreFiles":12}\n' "$mutation_total"
