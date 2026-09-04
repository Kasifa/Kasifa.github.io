#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
STEM=r076e_linear_modal_entropy_window
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/${STEM}_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/${STEM}_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/${STEM}_qa.sh"
FIXTURES="$ROOT/scripts/${STEM}_fixtures.json"
EXPECTED="$ROOT/scripts/${STEM}_expected.json"
MAIN="$ROOT/research/${STEM}.md"
PRIMARY="$ROOT/research/${STEM}_primary_audit.md"
SOURCE="$ROOT/research/r076e_report-source.md"
D_SOURCE="$ROOT/research/r076d_quantitative_growing_mode_entropy_window.md"
R_SOURCE="$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md"
CLOCK_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
CERT="$ROOT/research/${STEM}_certificate.json"
REPORT="$ROOT/research/${STEM}_certificate_report.md"
RUBY_REPORT="$ROOT/research/${STEM}_independent_audit.md"
QA_REPORT="$ROOT/research/${STEM}_qa_report.md"

EXPECTED_MAIN_HASH=1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4
EXPECTED_PRIMARY_HASH=5ce8fb3f2f2f487002b0e391db49855edb3cff72574058e26150813d69615d27
EXPECTED_SOURCE_HASH=10e506fa9d250b14d9f42f6eac7c2c83cfca934a85a2da6e223cd473f21e0c12
EXPECTED_D_HASH=cd94e3384f01963cb7b8a14fdb8376c6197c361473447f15500db0acac5e958e
EXPECTED_R_HASH=e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
EXPECTED_CLOCK_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_FIXTURES_HASH=9b5b0a7d88fe31d4156a7fbc8f73b52a9b5a8271437ee1be867970cec244cf47
EXPECTED_EXPECTED_HASH=af6c1fd49d57945306f5f97a99f160a8fcbaec21bce887b78fe74e0bbe4d4f80
EXPECTED_PY_HASH=57e629e0952131928e738501ee14f525daf3e2ac5fcb3b37fe02b118d7fb0f6c
EXPECTED_RUBY_HASH=e5f340e181b96a45d202ec88e5d98d71744b2ed23008e579c8c705c88fc30bdd
EXPECTED_CERT_HASH=73daf5a6fe12096b29b87704a667e45c994cd2233244e6f2f8daba987b471245
EXPECTED_REPORT_HASH=8e3937b7b5843b49c53fbbc6b3cc0490a139b1c2ff2e469bb64758f112d11f31
EXPECTED_RUBY_REPORT_HASH=bc5ed58d5a47a1c847ea626c85da49078a19ed148323c72eaf3d452b90ad3842

TMP_ROOT=$(mktemp -d /tmp/r076e-certificate-qa.XXXXXX)

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

command -v "$PYTHON_BIN" >/dev/null
command -v ruby >/dev/null
"$PYTHON_BIN" -Werror -B -c 'import pathlib,sys; compile(pathlib.Path(sys.argv[1]).read_text(), sys.argv[1], "exec")' "$PY_SCRIPT"
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"
"$PYTHON_BIN" -m json.tool "$FIXTURES" >"$TMP_ROOT/fixtures.pretty"
"$PYTHON_BIN" -m json.tool "$EXPECTED" >"$TMP_ROOT/expected.pretty"

test "$(digest "$MAIN")" = "$EXPECTED_MAIN_HASH"
test "$(digest "$PRIMARY")" = "$EXPECTED_PRIMARY_HASH"
test "$(digest "$SOURCE")" = "$EXPECTED_SOURCE_HASH"
test "$(digest "$D_SOURCE")" = "$EXPECTED_D_HASH"
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
grep -q 'Finite arithmetic is not proof of Turan--Nazarov' "$REPORT"
grep -q 'finite arithmetic is not proof of Turan--Nazarov' "$RUBY_REPORT"

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
    if b"\r" in raw:
        raise SystemExit(f"CR byte in {path}")
    if any(line.endswith((b" ", b"\t")) for line in raw.splitlines()):
        raise SystemExit(f"trailing whitespace in {path}")

text = paths[0].read_text(encoding="utf-8")
tags = [int(value) for value in re.findall(r"\\tag\{E\.(\d+)\}", text)]
if tags != list(range(1, 35)):
    raise SystemExit(f"bad E tag sequence: {tags}")
opens = len(re.findall(r"(?m)^\\\[$", text))
closes = len(re.findall(r"(?m)^\\\]$", text))
if opens != 38 or closes != 38 or opens - len(tags) != 4:
    raise SystemExit(f"bad display inventory: {opens}/{closes}, tags={len(tags)}")
refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])E\.(\d+)", text)]
if set(refs) - set(tags):
    raise SystemExit(f"dangling E references: {sorted(set(refs)-set(tags))}")
for pattern, label in (
    (r"(?<!\\)\bqquad\b", "bare qquad"),
    (r"(?<!\\)\bquad\b", "bare quad"),
    (r"(?<!\\)\bfrac\{", "bare frac"),
    (r"(?m)(?<!\\)\\$", "single trailing TeX slash"),
):
    if re.search(pattern, text):
        raise SystemExit(label)
for required in (
    r"K_U:=\int_0^Uk(\tau)d\tau",
    r"S_N=C_0N\log(N+1)",
    r"S_N^{m+1}e^{-2S_N}\le1",
    r"4^{-1/3}S_N^{4/3}K_T^{2/3}",
    r"e^{CN}T^{-2/3}K_T^{2/3}",
    r"\lambda^{-1/3}H^{2/3}",
    r"q(L)=o(L^2)",
    r"-\frac2{11907}",
):
    if required not in text:
        raise SystemExit(f"missing exact fragment: {required}")
for discouraged in ("我们", "攻关", "主攻", "研究纪律", "三重审计", "杀死错误想法"):
    if any(discouraged in path.read_text(encoding="utf-8") for path in paths):
        raise SystemExit(f"discouraged phrase: {discouraged}")
if "Equivalently" in text:
    raise SystemExit("false equivalence wording returned")
PY

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" R076E_JSON="$TMP_ROOT/certificate-$seed.json" \
    R076E_REPORT="$TMP_ROOT/report-$seed.md" "$PYTHON_BIN" -Werror -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=0 "$PYTHON_BIN" -Werror -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"assertionsTotal": 135' "$CERT"
grep -q '"strictBinaryUpperExponent": -93' "$CERT"
grep -q '"weightedLambdaPower": "-1/3"' "$CERT"
grep -q '"endpointLambdaPower": "0"' "$CERT"
grep -q '"frozenRate": "-2/11907"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R076E_JSON="$CERT" R076E_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Verdict: \*\*PASS\*\*' "$RUBY_REPORT"
grep -q 'Ruby assertions: 135/135' "$RUBY_REPORT"
grep -q 'Python/Ruby exact sections identical: PASS (6/6)' "$RUBY_REPORT"
grep -q 'Python/Ruby mutation inventory identical: PASS (135)' "$RUBY_REPORT"

mutations=$("$PYTHON_BIN" -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {count++} END {print count+0}')
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R076E_MUTATION="$mutation" \
    R076E_JSON="$TMP_ROOT/python-$mutation.json" R076E_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -Werror -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    printf '%s\n' "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R076E_JSON="$CERT" R076E_RUBY_MUTATION="$mutation" \
    R076E_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    printf '%s\n' "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$mutation_total" -eq 135
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R076E_MUTATION=unknown_mutation R076E_JSON="$TMP_ROOT/unknown-python.json" \
  R076E_REPORT="$TMP_ROOT/unknown-python.md" "$PYTHON_BIN" -Werror -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  printf '%s\n' 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076E_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R076E_JSON="$CERT" R076E_RUBY_MUTATION=unknown_mutation \
  R076E_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  printf '%s\n' 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076E_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

: >"$QA_REPORT"
core_count=$(find "$ROOT/research" "$ROOT/scripts" -maxdepth 1 -type f \
  \( -name 'r076e_*' -o -name 'r076e-*' \) \
  ! -name 'r076e_publication_handoff*' | wc -l | tr -d ' ')
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
  printf '%s\n' '# R0.76E certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Independent adversarial audit: PASS (blockers 0)'
  printf '%s\n' '- Python assertions: 135/135'
  printf '%s\n' '- Ruby assertions: 135/135'
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
  printf '%s\n' "| research/r076e_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/${STEM}_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/${STEM}_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/${STEM}_qa.sh | $qa_hash |"
  printf '%s\n' "| research/${STEM}_certificate.json | $cert_hash |"
  printf '%s\n' "| research/${STEM}_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/${STEM}_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- E.1--E.34, 38/38 displays with four intentional unnumbered displays, references, UTF-8, controls, CR, trailing whitespace, and TeX escapes: PASS.'
  printf '%s\n' '- Exact q=3, N=6 fixture: m=10, S=96, strict tail upper exponent -93, lambda=4, T=16, and gradient coefficient 257/64: PASS.'
  printf '%s\n' '- Weighted onset exponent lambda^(-1/3), terminal exponent lambda^0, physical exponents, and frozen rate -2/11907: PASS.'
  printf '%s\n' '- Uniform C_0 ledger, early Holder power 4/3, late monotonicity threshold, and last-unit endpoint split are present and certified: PASS.'
  printf '%s\n' '- R0.75R compatibility, exact-shear scope, q=o(L^2) window, Version-M condition, and NOT CLAY boundary: PASS.'
  printf '%s\n' '- Finite fixtures are explicitly excluded as proof of the imported continuum inequalities or analytic flux theorem: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable to this analytic theorem; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'R0.76E removes the factorial heat-tail bookkeeping loss and proves only the stated exp(Cq) exact-shear window.'
  printf '%s\n' 'Arbitrary packets, Version-M extraction, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r076e-linear-modal-entropy-window","status":"PASS","assertions":135,"mutations":%s,"pythonHashSeeds":3,"coreFiles":12}\n' "$mutation_total"
