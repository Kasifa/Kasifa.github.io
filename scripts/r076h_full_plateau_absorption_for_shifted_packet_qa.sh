#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
STEM=r076h_full_plateau_absorption_for_shifted_packet
PY_SCRIPT="$ROOT/scripts/"$STEM"_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/"$STEM"_certificate_independent.rb"
FIXTURES="$ROOT/scripts/"$STEM"_fixtures.json"
EXPECTED="$ROOT/scripts/"$STEM"_expected.json"
MAIN="$ROOT/research/"$STEM".md"
PRIMARY="$ROOT/research/"$STEM"_primary_audit.md"
SOURCE="$ROOT/research/r076h_report-source.md"
CERT="$ROOT/research/"$STEM"_certificate.json"
REPORT="$ROOT/research/"$STEM"_certificate_report.md"
RUBY_REPORT="$ROOT/research/"$STEM"_independent_audit.md"
QA_REPORT="$ROOT/research/"$STEM"_qa_report.md"

EXPECTED_MAIN_HASH=11490112a1893400a1099dd9f45b906ce78d7dab1ebcf549eaa7870241dc0ef4
EXPECTED_PRIMARY_HASH=91e1f31f3adf19a9f352a8cd6defc8988971e51f0905e4a634f949223992c58d
EXPECTED_SOURCE_HASH=3e706ae12caace1118f941f92c85bc0a1a11ed4a6e158acf7258918a67616d87
EXPECTED_FIXTURES_HASH=035ff9b04f61c11744668c51e6fd8ef1e35da93de85fab2bd9b971acca79747d
EXPECTED_EXPECTED_HASH=f80cc1d8b6673a6f18069d6756f605de821ac661561d11295a40c468532e083b
EXPECTED_PY_HASH=65cd03fa1420eaffbf1a0e795d178b13b46829f79811963a724f2c25a9c72b2f
EXPECTED_RUBY_HASH=4b1d72ad23b82eb48eef6df96d98bb904aa8f72e4932724ac72557c881c46cb3
EXPECTED_CERT_HASH=452e46b75a10d7fcb637d85234e1d3f76c471cd4ea1cec6b69b568260a8ff55e
EXPECTED_REPORT_HASH=d9c80bc4af24f7f55046e2b5d13484841d3c430232c586913c10b23cbd425267
EXPECTED_RUBY_REPORT_HASH=f3d301f7b29cd1d5ceb89604d4b14d306e3f1fb47c35a5cce1cd689fc8b16fbd

TMP_ROOT=$(mktemp -d /tmp/r076h-certificate-qa.XXXXXX)
trap 'rm -rf "$TMP_ROOT"' EXIT

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

python3 -Werror -B -c 'import pathlib,sys; compile(pathlib.Path(sys.argv[1]).read_text(), sys.argv[1], "exec")' "$PY_SCRIPT"
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"
python3 -m json.tool "$FIXTURES" >"$TMP_ROOT/fixtures.pretty"
python3 -m json.tool "$EXPECTED" >"$TMP_ROOT/expected.pretty"

test "$(digest "$MAIN")" = "$EXPECTED_MAIN_HASH"
test "$(digest "$PRIMARY")" = "$EXPECTED_PRIMARY_HASH"
test "$(digest "$SOURCE")" = "$EXPECTED_SOURCE_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"
test "$(digest "$PY_SCRIPT")" = "$EXPECTED_PY_HASH"
test "$(digest "$RUBY_SCRIPT")" = "$EXPECTED_RUBY_HASH"
test "$(digest "$CERT")" = "$EXPECTED_CERT_HASH"
test "$(digest "$REPORT")" = "$EXPECTED_REPORT_HASH"
test "$(digest "$RUBY_REPORT")" = "$EXPECTED_RUBY_REPORT_HASH"
test "$(digest "$ROOT/research/r076g_complete_clock_central_fibre_flux_lower_bound.md")" = 20f32790b53f2b0f5cb39b7071bd2cda96ddb4e15f75211e1682f4ba37dd0bb2
test "$(digest "$ROOT/research/r075p_buffered_collar_entrance_concentration.md")" = 8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6
test "$(digest "$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md")" = e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
test "$(digest "$ROOT/research/r076e_linear_modal_entropy_window.md")" = 1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" R076H_JSON="$TMP_ROOT/certificate-$seed.json" \
    R076H_REPORT="$TMP_ROOT/report-$seed.md" python3 -Werror -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
python3 - "$CERT" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
if data.get("verdict") != "PASS":
    raise SystemExit(f"canonical certificate verdict is {data.get('verdict')!r}")
if data.get("assertionsTotal") != 126:
    raise SystemExit(f"unexpected assertion total: {data.get('assertionsTotal')!r}")
PY
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R076H_JSON="$CERT" ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Verdict: \*\*PASS\*\*' "$RUBY_REPORT"
grep -q 'Ruby assertions: 126/126' "$RUBY_REPORT"
grep -q 'Python/Ruby exact section identical: PASS' "$RUBY_REPORT"
grep -q 'Python/Ruby mutation inventory identical: PASS' "$RUBY_REPORT"

mutations=$(python3 -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {count++} END {print count+0}')
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R076H_MUTATION="$mutation" \
    R076H_JSON="$TMP_ROOT/python-$mutation.json" R076H_REPORT="$TMP_ROOT/python-$mutation.md" \
    python3 -Werror -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    printf '%s\n' "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R076H_JSON="$CERT" R076H_RUBY_MUTATION="$mutation" \
    R076H_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    printf '%s\n' "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R076H_MUTATION=unknown_mutation R076H_JSON="$TMP_ROOT/unknown-python.json" \
  R076H_REPORT="$TMP_ROOT/unknown-python.md" python3 -Werror -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  printf '%s\n' 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076H_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R076H_JSON="$CERT" R076H_RUBY_MUTATION=unknown_mutation \
  R076H_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  printf '%s\n' 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076H_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

python3 - "$MAIN" "$PRIMARY" "$SOURCE" <<'PY'
import pathlib
import re
import sys

paths = [pathlib.Path(value) for value in sys.argv[1:]]
for path in paths:
    raw = path.read_bytes()
    raw.decode("utf-8")
    if b"\r" in raw:
        raise SystemExit(f"CR byte in {path}")
    if any(line.endswith((b" ", b"\t")) for line in raw.splitlines()):
        raise SystemExit(f"trailing whitespace in {path}")

text = paths[0].read_text(encoding="utf-8")
flat = re.sub(r"\s+", " ", text)
tags = [int(value) for value in re.findall(r"\\tag\{H\.(\d+)\}", text)]
if tags != list(range(1, 40)):
    raise SystemExit(f"bad H tag sequence: {tags}")
if len(re.findall(r"(?m)^\\\[$", text)) != 39 or len(re.findall(r"(?m)^\\\]$", text)) != 39:
    raise SystemExit("bad display inventory")
for required in (
    r"M_L^{\rm plat}=aR^5",
    r"\mathcal A_a(z)=4\pi a\delta_0",
    r"\frac{\delta_0}{8a}",
    r"\left(\frac{2}{3w_0}\right)^{4m}=o(1)",
    r"\frac3{40000}",
    r"-\frac2{11907}",
    "arbitrary packets",
    "**NOT CLAY.**",
):
    if required not in text and required not in flat:
        raise SystemExit(f"missing exact fragment: {required}")
if re.search(r"(?<!\\)left[\[(]", text):
    raise SystemExit("bare left delimiter")
if "Holder" in text or "Hölder" not in text:
    raise SystemExit("Hölder spelling regression")
for discouraged in ("我们", "攻关", "主攻", "研究纪律", "三重审计", "杀死错误想法"):
    if any(discouraged in path.read_text(encoding="utf-8") for path in paths):
        raise SystemExit(f"discouraged phrase: {discouraged}")
PY

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R076H_JSON="$CERT" ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

: >"$QA_REPORT"
core_count=$(find "$ROOT/research" "$ROOT/scripts" -maxdepth 1 -type f \
  \( -name 'r076h_*' -o -name 'r076h-*' \) \
  ! -name 'r076h_publication_handoff*' | wc -l | tr -d ' ')
test "$core_count" -eq 12
assertions=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["assertionsTotal"])' "$CERT")

{
  printf '%s\n' '# R0.76H certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Independent mathematical rereads: PASS (2 audits; blockers 0)'
  printf '%s\n' "- Python assertions: $assertions/$assertions"
  printf '%s\n' "- Ruby assertions: $assertions/$assertions"
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Python/Ruby exact section and mutation inventory: PASS'
  printf '%s\n' '- Canonical outputs regeneration-stable: PASS'
  printf '%s\n' '- Exact core inventory: 12/12 files (11 hash-bound manifest rows plus this self-generated QA report)'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  for path in "$MAIN" "$PRIMARY" "$SOURCE" "$FIXTURES" "$EXPECTED" "$PY_SCRIPT" "$RUBY_SCRIPT" "$ROOT/scripts/"$STEM"_qa.sh" "$CERT" "$REPORT" "$RUBY_REPORT"; do
    rel=$(printf '%s\n' "$path" | sed "s|^$ROOT/||")
    printf '| %s | %s |\n' "$rel" "$(digest "$path")"
  done
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- H.1--H.39, displays, references, UTF-8, CR, trailing whitespace, and prose screen: PASS.'
  printf '%s\n' '- Exact shell cross-section, aR^5 Jacobian, adjacent strip, and terminal-box powers: PASS.'
  printf '%s\n' '- Exact m=4 moment coefficients, derivative, cap comparison exponents, and dyadic sample modes: PASS.'
  printf '%s\n' '- Complete signed-flux positivity and two-sided full-plateau bounds: PASS.'
  printf '%s\n' '- Raw 3/40000 and normalized -2/11907 logarithmic rates: PASS.'
  printf '%s\n' '- Explicit-packet-only, arbitrary-packets-open, source, and NOT CLAY boundaries: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'Finite certificates audit the exact ledger; they are not the continuum proof.'
} >"$QA_REPORT"

printf '{"suite":"r076h-full-plateau-absorption-for-shifted-packet","status":"PASS","assertions":%s,"mutations":%s,"pythonHashSeeds":3,"coreFiles":12}\n' "$assertions" "$mutation_total"
