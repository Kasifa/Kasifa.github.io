#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
STEM=r076f_exponential_spatial_observation_lower_bound
PY_SCRIPT="$ROOT/scripts/${STEM}_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/${STEM}_certificate_independent.rb"
FIXTURES="$ROOT/scripts/${STEM}_fixtures.json"
EXPECTED="$ROOT/scripts/${STEM}_expected.json"
MAIN="$ROOT/research/${STEM}.md"
PRIMARY="$ROOT/research/${STEM}_primary_audit.md"
SOURCE="$ROOT/research/r076f_report-source.md"
CERT="$ROOT/research/${STEM}_certificate.json"
REPORT="$ROOT/research/${STEM}_certificate_report.md"
RUBY_REPORT="$ROOT/research/${STEM}_independent_audit.md"
QA_REPORT="$ROOT/research/${STEM}_qa_report.md"

EXPECTED_MAIN_HASH=48204fcbf8fe9af3f0fdc7720844c3dd8362d8767caf73de016eda7250b70973
EXPECTED_PRIMARY_HASH=abcaa220c56d1f90c4b34061191e7cd009b8d911be3f83d705e95aa51b4d84cc
EXPECTED_SOURCE_HASH=5e3939710dcfefcbc08b93761d8cdda1e655656a1bcd404b63fcea251ffd5e1e
EXPECTED_PREDECESSOR_HASH=1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4
EXPECTED_FIXTURES_HASH=1b11049ab482eb9b6d6b99cfdabfb4cd0a34ac4f483e3e69c5ec178dce752b5a
EXPECTED_EXPECTED_HASH=9703be8236b77e556085f9b358f4128ace4e32920a5391ebc1e2a900b232d37a
EXPECTED_PY_HASH=2882146fba7376d1f2d83d324c816b763729c59443fa4cb1f5fbcc47778c6994
EXPECTED_RUBY_HASH=191b7ee7c0e7ed9157a33606c0ed00e3d0bd1db374260b26d8d5d5b64807bf32
EXPECTED_CERT_HASH=0558eab8a7ce5ae36e1614fe0c2184debfa8550c655a86baab590fbb9ee6f259
EXPECTED_REPORT_HASH=7de8bb9ce8b59704c4097616a14e09366c8cc9031acf2e2692b51bce9a785ea0
EXPECTED_RUBY_REPORT_HASH=8b90a9ab9b60a17f6e5cfc097f658c80ce4cb410142d72123b72bef6895ab7de

TMP_ROOT=$(mktemp -d /tmp/r076f-certificate-qa.XXXXXX)
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
test "$(digest "$ROOT/research/r076e_linear_modal_entropy_window.md")" = "$EXPECTED_PREDECESSOR_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"
test "$(digest "$PY_SCRIPT")" = "$EXPECTED_PY_HASH"
test "$(digest "$RUBY_SCRIPT")" = "$EXPECTED_RUBY_HASH"
test "$(digest "$CERT")" = "$EXPECTED_CERT_HASH"
test "$(digest "$REPORT")" = "$EXPECTED_REPORT_HASH"
test "$(digest "$RUBY_REPORT")" = "$EXPECTED_RUBY_REPORT_HASH"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" R076F_JSON="$TMP_ROOT/certificate-$seed.json" \
    R076F_REPORT="$TMP_ROOT/report-$seed.md" python3 -Werror -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"assertionsTotal": 83' "$CERT"
grep -q '"lowerBound": 8' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R076F_JSON="$CERT" ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Verdict: \*\*PASS\*\*' "$RUBY_REPORT"
grep -q 'Ruby assertions: 83/83' "$RUBY_REPORT"
grep -q 'Python/Ruby exact section identical: PASS' "$RUBY_REPORT"

mutations=$(python3 -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {count++} END {print count+0}')
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R076F_MUTATION="$mutation" \
    R076F_JSON="$TMP_ROOT/python-$mutation.json" R076F_REPORT="$TMP_ROOT/python-$mutation.md" \
    python3 -Werror -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    printf '%s\n' "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R076F_JSON="$CERT" R076F_RUBY_MUTATION="$mutation" \
    R076F_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    printf '%s\n' "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$mutation_total" -eq 83
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R076F_MUTATION=unknown_mutation R076F_JSON="$TMP_ROOT/unknown-python.json" \
  R076F_REPORT="$TMP_ROOT/unknown-python.md" python3 -Werror -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  printf '%s\n' 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076F_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R076F_JSON="$CERT" R076F_RUBY_MUTATION=unknown_mutation \
  R076F_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  printf '%s\n' 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076F_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

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
tags = [int(value) for value in re.findall(r"\\tag\{F\.(\d+)\}", text)]
if tags != list(range(1, 19)):
    raise SystemExit(f"bad F tag sequence: {tags}")
if len(re.findall(r"(?m)^\\\[$", text)) != 18 or len(re.findall(r"(?m)^\\\]$", text)) != 18:
    raise SystemExit("bad display inventory")
for required in (
    r"n_j=q+j-1", r"n_q=2q-1\le2q=2n_1", r"2^{q-1}",
    r"\frac{\sin(3x)}{\sin x}", r"\log C_q\ge(q-1)\log2",
    "not a lower bound for the complete collar flux", "**NOT CLAY.**",
):
    if required not in text and required not in flat:
        raise SystemExit(f"missing exact fragment: {required}")
for discouraged in ("我们", "攻关", "主攻", "研究纪律", "三重审计", "杀死错误想法"):
    if any(discouraged in path.read_text(encoding="utf-8") for path in paths):
        raise SystemExit(f"discouraged phrase: {discouraged}")
PY

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R076F_JSON="$CERT" ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

: >"$QA_REPORT"
core_count=$(find "$ROOT/research" "$ROOT/scripts" -maxdepth 1 -type f \
  \( -name 'r076f_*' -o -name 'r076f-*' \) \
  ! -name 'r076f_publication_handoff*' | wc -l | tr -d ' ')
test "$core_count" -eq 12

{
  printf '%s\n' '# R0.76F certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Independent mathematical audit: PASS (blockers 0; alpha-rule fixture correction closed)'
  printf '%s\n' '- Python assertions: 83/83'
  printf '%s\n' '- Ruby assertions: 83/83'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Python/Ruby exact section and mutation inventory: PASS'
  printf '%s\n' '- Canonical outputs regeneration-stable: PASS'
  printf '%s\n' '- Exact core inventory: 12/12 files'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  for path in "$MAIN" "$PRIMARY" "$SOURCE" "$FIXTURES" "$EXPECTED" "$PY_SCRIPT" "$RUBY_SCRIPT" "$ROOT/scripts/${STEM}_qa.sh" "$CERT" "$REPORT" "$RUBY_REPORT"; do
    rel=${path#"$ROOT/"}
    printf '| %s | %s |\n' "$rel" "$(digest "$path")"
  done
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- F.1--F.18, display balance, references, UTF-8, CR, trailing whitespace, and prose screen: PASS.'
  printf '%s\n' '- Exact q=4 sample: modes 4--7, binomial amplitudes 1,3,3,1, dyadic endpoint 7<=8: PASS.'
  printf '%s\n' '- At delta=2pi/3, x=pi/6 and sin(3x)/sin(x)=2, giving the exact lower bound 2^3=8: PASS.'
  printf '%s\n' '- Spatial-only, no-full-flux-lower-bound, literature, open-problem, and NOT CLAY boundaries: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'Finite certificates audit the exact ledger; they are not the continuum proof.'
} >"$QA_REPORT"

printf '{"suite":"r076f-exponential-spatial-observation-lower-bound","status":"PASS","assertions":83,"mutations":%s,"pythonHashSeeds":3,"coreFiles":12}\n' "$mutation_total"
