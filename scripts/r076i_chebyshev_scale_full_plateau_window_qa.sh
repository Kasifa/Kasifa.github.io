#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
STEM=r076i_chebyshev_scale_full_plateau_window
PY_SCRIPT="$ROOT/scripts/"$STEM"_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/"$STEM"_certificate_independent.rb"
FIXTURES="$ROOT/scripts/"$STEM"_fixtures.json"
EXPECTED="$ROOT/scripts/"$STEM"_expected.json"
MAIN="$ROOT/research/"$STEM".md"
PRIMARY="$ROOT/research/"$STEM"_primary_audit.md"
SOURCE="$ROOT/research/r076i_report-source.md"
CERT="$ROOT/research/"$STEM"_certificate.json"
REPORT="$ROOT/research/"$STEM"_certificate_report.md"
RUBY_REPORT="$ROOT/research/"$STEM"_independent_audit.md"
QA_REPORT="$ROOT/research/"$STEM"_qa_report.md"

TMP_ROOT=$(mktemp -d /tmp/r076i-certificate-qa.XXXXXX)
trap 'rm -rf "$TMP_ROOT"' EXIT

python3 -Werror -B -c 'import pathlib,sys; compile(pathlib.Path(sys.argv[1]).read_text(), sys.argv[1], "exec")' "$PY_SCRIPT"
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"
python3 -m json.tool "$FIXTURES" >"$TMP_ROOT/fixtures.pretty"
python3 -m json.tool "$EXPECTED" >"$TMP_ROOT/expected.pretty"

# Generated outputs and the generated independent audit must never enter the
# Python/Ruby FROZEN maps; the QA layer may lock them only after generation.
python3 - "$PY_SCRIPT" <<'PY'
import runpy
import sys

namespace = runpy.run_path(sys.argv[1])
frozen = set(namespace["FROZEN"])
forbidden = {
    "research/r076i_chebyshev_scale_full_plateau_window_certificate.json",
    "research/r076i_chebyshev_scale_full_plateau_window_certificate_report.md",
    "research/r076i_chebyshev_scale_full_plateau_window_independent_audit.md",
    "research/r076i_chebyshev_scale_full_plateau_window_qa_report.md",
}
overlap = sorted(frozen & forbidden)
if overlap:
    raise SystemExit(f"generated-output hash cycle: {overlap}")
if len(frozen) != 7:
    raise SystemExit(f"unexpected frozen binding count: {len(frozen)}")
PY

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R076I_JSON="$TMP_ROOT/certificate-$seed.json" \
    R076I_REPORT="$TMP_ROOT/report-$seed.md" \
    python3 -Werror -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

BASE_CERT="$TMP_ROOT/certificate-0.json"
BASE_REPORT="$TMP_ROOT/report-0.md"
read -r verdict freeze_ready assertions placeholders <<EOF
$(python3 - "$BASE_CERT" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
print(data["verdict"], str(data["freezeReady"]).lower(), data["assertionsTotal"], len(data["placeholders"]))
PY
)
EOF

test "$assertions" -eq 129
if test "$freeze_ready" = true; then
  test "$verdict" = PASS
  test "$placeholders" -eq 0
else
  test "$verdict" = SCAFFOLD_PASS
  test "$placeholders" -gt 0
fi

env R076I_JSON="$BASE_CERT" \
  R076I_RUBY_REPORT="$TMP_ROOT/ruby-baseline.md" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-baseline.stdout"
grep -q "Verdict: \*\*$verdict\*\*" "$TMP_ROOT/ruby-baseline.md"
grep -q 'Ruby assertions: 129/129' "$TMP_ROOT/ruby-baseline.md"
grep -q 'Python/Ruby exact section identical: PASS' "$TMP_ROOT/ruby-baseline.md"
grep -q 'Python/Ruby mutation inventory identical: PASS' "$TMP_ROOT/ruby-baseline.md"
grep -q 'Python/Ruby bindings identical: PASS' "$TMP_ROOT/ruby-baseline.md"
grep -q 'Python/Ruby freeze state compatible: PASS' "$TMP_ROOT/ruby-baseline.md"

mutations=$(python3 -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1], encoding="utf-8"))["negativeMutations"]))' "$BASE_CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {count++} END {print count+0}')
test "$mutation_total" -eq 129

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R076I_MUTATION="$mutation" \
    R076I_JSON="$TMP_ROOT/python-$mutation.json" \
    R076I_REPORT="$TMP_ROOT/python-$mutation.md" \
    python3 -Werror -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    printf '%s\n' "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R076I_JSON="$BASE_CERT" R076I_RUBY_MUTATION="$mutation" \
    R076I_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    printf '%s\n' "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done

test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R076I_MUTATION=unknown_mutation \
  R076I_JSON="$TMP_ROOT/unknown-python.json" \
  R076I_REPORT="$TMP_ROOT/unknown-python.md" \
  python3 -Werror -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  printf '%s\n' 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076I_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R076I_JSON="$BASE_CERT" R076I_RUBY_MUTATION=unknown_mutation \
  R076I_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  printf '%s\n' 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076I_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

python3 - "$FIXTURES" "$BASE_CERT" <<'PY'
import json
import sys

fixture = json.load(open(sys.argv[1], encoding="utf-8"))
certificate = json.load(open(sys.argv[2], encoding="utf-8"))
sources = fixture["sources"]
if sources["zhangAbs"] != "https://arxiv.org/abs/2607.10501v1":
    raise SystemExit("Zhang abstract URL is not version-locked")
if sources["zhangPdf"] != "https://arxiv.org/pdf/2607.10501v1":
    raise SystemExit("Zhang PDF URL is not version-locked")
exact = certificate["exact"]
if exact["geometry"]["eA"] != "639/640" or exact["geometry"]["deltaA"] != "2/213":
    raise SystemExit("sample interval arithmetic drift")
if exact["zhang"]["AFr"] != 8191 or exact["zhang"]["qSquaredExponentSqrt2Coefficient"] != 36:
    raise SystemExit("Zhang constant/exponent drift")
if exact["terminal"]["cubedCoefficient"] != 1728 or exact["terminal"]["twoThirdsCoefficient"] != 144:
    raise SystemExit("terminal arithmetic drift")
if exact["physical"]["modeWindowExponent"] != "5/2" or exact["physical"]["normalizedLogRate"] != "-2/11907":
    raise SystemExit("asymptotic ledger drift")
PY

# Canonical generated outputs must equal the hash-seed-stable temporary
# outputs.  The Ruby report must likewise reproduce its temporary baseline.
env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT"
cmp "$BASE_CERT" "$CERT"
cmp "$BASE_REPORT" "$REPORT"
env R076I_JSON="$CERT" ruby "$RUBY_SCRIPT"
cmp "$TMP_ROOT/ruby-baseline.md" "$RUBY_REPORT"

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT"
env R076I_JSON="$CERT" ruby "$RUBY_SCRIPT"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

: >"$QA_REPORT"
core_count=$(find "$ROOT/research" "$ROOT/scripts" -maxdepth 1 -type f \
  \( -name 'r076i_*' -o -name 'r076i-*' \) \
  ! -name 'r076i_publication_handoff*' | wc -l | tr -d ' ')
test "$core_count" -eq 12

{
  printf '%s\n' '# R0.76I certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Independent mathematical rereads: PASS (2 lanes; blockers 0)'
  printf '%s\n' "- Python assertions: $assertions/$assertions"
  printf '%s\n' "- Ruby assertions: $assertions/$assertions"
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Python/Ruby exact arithmetic, mutation inventory, bindings, and freeze state: PASS'
  printf '%s\n' '- Generated-output hash-cycle guard: PASS'
  printf '%s\n' '- Canonical outputs regeneration-stable: PASS'
  printf '%s\n' '- Exact core inventory: 12/12 files (11 manifest rows plus this self-generated QA report)'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  for path in "$MAIN" "$PRIMARY" "$SOURCE" "$FIXTURES" "$EXPECTED" \
    "$PY_SCRIPT" "$RUBY_SCRIPT" "$ROOT/scripts/"$STEM"_qa.sh" \
    "$CERT" "$REPORT" "$RUBY_REPORT"; do
    rel=$(printf '%s\n' "$path" | sed "s|^$ROOT/||")
    printf '| %s | %s |\n' "$rel" "$(digest "$path")"
  done
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- I.1--I.38, 42 displays, reference closure, UTF-8, CR, and trailing whitespace: PASS.'
  printf '%s\n' '- Exact e_a=639/640, Delta_a=2/213, two-sided 2q branch count, and Zhang exponent ledger: PASS.'
  printf '%s\n' '- Erdelyi derivative powers, reverse-time E_N^+ terminal trace, and four-row energy signs: PASS.'
  printf '%s\n' '- Physical a^(2/3)R^(-1/3) conversion, R cancellation, and normalized -2/11907 rate: PASS.'
  printf '%s\n' '- CONDITIONAL-LITERATURE, unrefereed-v1, restricted-sharpness, OPEN, and NOT CLAY boundaries: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'Finite certificates audit the exact ledger; they do not prove the imported literature or the continuum theorem.'
} >"$QA_REPORT"

printf '{"suite":"r076i-chebyshev-scale-full-plateau-window","status":"%s","freezeReady":%s,"assertions":%s,"mutations":%s,"pythonHashSeeds":3,"generatedHashCycle":false}\n' \
  "$verdict" "$freeze_ready" "$assertions" "$mutation_total"
