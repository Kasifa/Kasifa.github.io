#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
STEM=r075q_spatially_spread_harmonic_collar_payment
PY_SCRIPT="$ROOT/scripts/${STEM}_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/${STEM}_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/${STEM}_qa.sh"
FIXTURES="$ROOT/scripts/${STEM}_fixtures.json"
EXPECTED="$ROOT/scripts/${STEM}_expected.json"
MAIN="$ROOT/research/${STEM}.md"
PRIMARY="$ROOT/research/${STEM}_primary_audit.md"
SOURCE="$ROOT/research/r075q_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
L_SOURCE="$ROOT/research/r075l_single_harmonic_diffusive_signed_flux_gain.md"
N_SOURCE="$ROOT/research/r075n_radial_collar_averaged_wiener_row.md"
P_SOURCE="$ROOT/research/r075p_buffered_collar_entrance_concentration.md"
CERT="$ROOT/research/${STEM}_certificate.json"
REPORT="$ROOT/research/${STEM}_certificate_report.md"
RUBY_REPORT="$ROOT/research/${STEM}_independent_audit.md"
QA_REPORT="$ROOT/research/${STEM}_qa_report.md"

EXPECTED_MAIN_HASH=9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c
EXPECTED_PRIMARY_HASH=92255869e165efdbe72557187dd1fe6e7e4449264dcf8033b285286d50f725be
EXPECTED_SOURCE_HASH=b1fcfece0396b04ae9f59e42ef09957a422c36fa0843730a9fb22919bc24c600
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_L_HASH=52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5
EXPECTED_N_HASH=ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318
EXPECTED_P_HASH=8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6
EXPECTED_FIXTURES_HASH=a0954f102de2fbc5ac5fb57fd68ba2ae084cc27743240fac6e3297b81d4410f5
EXPECTED_EXPECTED_HASH=8f3e45bb4a62e2a5bd506fd3cc522610d59115f34411fd85b04c7b72081cb444

TMP_ROOT=$(mktemp -d /tmp/r075q-certificate-qa.XXXXXX)
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
test "$(digest "$L_SOURCE")" = "$EXPECTED_L_HASH"
test "$(digest "$N_SOURCE")" = "$EXPECTED_N_HASH"
test "$(digest "$P_SOURCE")" = "$EXPECTED_P_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q 'Verdict: \*\*PASS\*\*' "$PRIMARY"
grep -q 'Mathematical blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'Release blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'does not authorize publication' "$PRIMARY"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075Q_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075Q_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 20' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"exponentialRate": "-4279/238140000"' "$CERT"
grep -q '"fixtureBound": "315/16384"' "$CERT"
grep -q '"spatialLowerTimesPi": "1/384"' "$CERT"
grep -q '"massLowerCoefficientWithoutExpOverPi": "3/131072"' "$CERT"
grep -q '"packetToRowRatio": "18/125"' "$CERT"
grep -q '"projectionDominationValid": false' "$CERT"
grep -q '"fractionUpperTimesPi": "1/32"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075Q_JSON="$CERT" R075Q_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":21' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 21/21' "$RUBY_REPORT"
grep -q 'Blocker count: 0' "$RUBY_REPORT"
grep -q 'time integral on one physical source line' "$RUBY_REPORT"

mutations=$("$PYTHON_BIN" -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {n++} END {print n+0}')
test "$mutation_total" -eq 180
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R075Q_MUTATION="$mutation" \
    R075Q_JSON="$TMP_ROOT/python-$mutation.json" \
    R075Q_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075Q_JSON="$CERT" R075Q_RUBY_MUTATION="$mutation" \
    R075Q_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R075Q_MUTATION=unknown_mutation \
  R075Q_JSON="$TMP_ROOT/unknown-python.json" R075Q_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075Q_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075Q_JSON="$CERT" R075Q_RUBY_MUTATION=unknown_mutation \
  R075Q_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075Q_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075Q_JSON="$CERT" R075Q_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_hash=$(digest "$PRIMARY")
source_hash=$(digest "$SOURCE")
b_hash=$(digest "$B_SOURCE")
l_hash=$(digest "$L_SOURCE")
n_hash=$(digest "$N_SOURCE")
p_hash=$(digest "$P_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75Q certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 20/20'
  printf '%s\n' '- Ruby assertions: 21/21'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  printf '%s\n' "| research/${STEM}.md | $main_hash |"
  printf '%s\n' "| research/${STEM}_primary_audit.md | $primary_hash |"
  printf '%s\n' "| research/r075q_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/${STEM}_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/${STEM}_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/${STEM}_qa.sh | $qa_hash |"
  printf '%s\n' "| research/${STEM}_certificate.json | $cert_hash |"
  printf '%s\n' "| research/${STEM}_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/${STEM}_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' '' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  printf '%s\n' "| research/r075b_bulk_clock_outer_padding_gate.md | $b_hash |"
  printf '%s\n' "| research/r075l_single_harmonic_diffusive_signed_flux_gain.md | $l_hash |"
  printf '%s\n' "| research/r075n_radial_collar_averaged_wiener_row.md | $n_hash |"
  printf '%s\n' "| research/r075p_buffered_collar_entrance_concentration.md | $p_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- Q.1--Q.28, references, 28/28 displays, dependencies, TeX, UTF-8, and control bytes: PASS.'
  printf '%s\n' '- Radial L1 scale, 1/8 flux row, exact fibre, phase-uniform period floor, and c_box: PASS.'
  printf '%s\n' '- Q.21 full time integral appears explicitly on the same physical source line: PASS.'
  printf '%s\n' '- Cubic inversion, normalization, and exact rate -4279/238140000: PASS.'
  printf '%s\n' '- Full-window same-v_R actual-component Version-M ledger and low-entrance diagnostic: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The report-source is byte-bound; its bounded literature screen is adjacent context,'
  printf '%s\n' 'not a completeness, novelty, or priority conclusion. Q is one real horizontal harmonic.'
  printf '%s\n' 'Projection, multimode, vertical, nonconstant-shear, E.24, complete-clock, fixed-deletion,'
  printf '%s\n' 'suitable-weak, regularity, and singularity conclusions remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075q-spatially-spread-harmonic-collar-payment","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$mutation_total"
