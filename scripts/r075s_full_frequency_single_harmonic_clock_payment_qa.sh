#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
STEM=r075s_full_frequency_single_harmonic_clock_payment
PY_SCRIPT="$ROOT/scripts/${STEM}_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/${STEM}_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/${STEM}_qa.sh"
FIXTURES="$ROOT/scripts/${STEM}_fixtures.json"
EXPECTED="$ROOT/scripts/${STEM}_expected.json"
MAIN="$ROOT/research/${STEM}.md"
PRIMARY="$ROOT/research/${STEM}_primary_audit.md"
SOURCE="$ROOT/research/r075s_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
Q_SOURCE="$ROOT/research/r075q_spatially_spread_harmonic_collar_payment.md"
R_SOURCE="$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md"
CERT="$ROOT/research/${STEM}_certificate.json"
REPORT="$ROOT/research/${STEM}_certificate_report.md"
RUBY_REPORT="$ROOT/research/${STEM}_independent_audit.md"
QA_REPORT="$ROOT/research/${STEM}_qa_report.md"

EXPECTED_MAIN_HASH=d2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd
EXPECTED_PRIMARY_HASH=38e2bc95b5785b97df5d85474f3ed6105458a117249710b2c052cebbd769b5eb
EXPECTED_SOURCE_HASH=ab9771e732204f28d3493ae9db73e7aa62aa980cc15b69dfefb39f226520b2a7
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_Q_HASH=9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c
EXPECTED_R_HASH=e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
EXPECTED_FIXTURES_HASH=82874592703552c1639c69066ddbf1ab531c135cd92eeae775c20be66cd8260f
EXPECTED_EXPECTED_HASH=e806089d4649b73649edeed5c0204b81a42dbef79c758283b128ec49a57abd8b

TMP_ROOT=$(mktemp -d /tmp/r075s-certificate-qa.XXXXXX)
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
test "$(digest "$E_SOURCE")" = "$EXPECTED_E_HASH"
test "$(digest "$Q_SOURCE")" = "$EXPECTED_Q_HASH"
test "$(digest "$R_SOURCE")" = "$EXPECTED_R_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q 'Current verdict: \*\*PASS\*\*' "$PRIMARY"
grep -q 'Mathematical blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'Release blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'does not authorize publication' "$PRIMARY"
grep -q 'can alias the oscillation' "$PRIMARY"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075S_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075S_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 21' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"T": "1/64"' "$CERT"
grep -q '"epsilon": "1"' "$CERT"
grep -q '"epsilon": "8"' "$CERT"
grep -q '"epsilon": "32"' "$CERT"
grep -q '"frozenRate": "-2/11907"' "$CERT"
grep -q '"normalizedRExponent": 0' "$CERT"
grep -q '"normalizedOmegaExponent": "1/3"' "$CERT"
grep -q '"amplitudeCancels": true' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075S_JSON="$CERT" R075S_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":23' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 23/23' "$RUBY_REPORT"
grep -q 'Blocker count: 0' "$RUBY_REPORT"

mutations=$("$PYTHON_BIN" -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {n++} END {print n+0}')
test "$mutation_total" -eq 76
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R075S_MUTATION="$mutation" \
    R075S_JSON="$TMP_ROOT/python-$mutation.json" \
    R075S_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075S_JSON="$CERT" R075S_RUBY_MUTATION="$mutation" \
    R075S_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
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

if env R075S_MUTATION=unknown_mutation \
  R075S_JSON="$TMP_ROOT/unknown-python.json" R075S_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075S_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075S_JSON="$CERT" R075S_RUBY_MUTATION=unknown_mutation \
  R075S_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075S_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075S_JSON="$CERT" R075S_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_hash=$(digest "$PRIMARY")
source_hash=$(digest "$SOURCE")
b_hash=$(digest "$B_SOURCE")
e_hash=$(digest "$E_SOURCE")
q_hash=$(digest "$Q_SOURCE")
r_hash=$(digest "$R_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75S certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 21/21'
  printf '%s\n' '- Ruby assertions: 23/23'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  printf '%s\n' "| research/${STEM}.md | $main_hash |"
  printf '%s\n' "| research/${STEM}_primary_audit.md | $primary_hash |"
  printf '%s\n' "| research/r075s_report-source.md | $source_hash |"
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
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_hash |"
  printf '%s\n' "| research/r075q_spatially_spread_harmonic_collar_payment.md | $q_hash |"
  printf '%s\n' "| research/r075r_outer_cap_spectral_concentration_obstruction.md | $r_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- S.1--S.41, 41/41 tags, 42/42 displays, dependencies, references, UTF-8, and control bytes: PASS.'
  printf '%s\n' '- Exact radial reduction and all three sine-coefficient scales: PASS.'
  printf '%s\n' '- Low-frequency node geometry and moving-phase BV lemma: PASS.'
  printf '%s\n' '- High-frequency phase-uniform mass, BV cancellation, and radial Fourier tail: PASS.'
  printf '%s\n' '- All-frequency coverage, amplitude cancellation, and normalized rate -2/11907: PASS.'
  printf '%s\n' '- Fast-phase quadrature aliasing is explicitly excluded as proof evidence: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The source report is byte-bound; its literature screen is bounded and does not establish novelty.'
  printf '%s\n' 'S proves the complete-clock physical-collar payment only for one real constant-drift harmonic.'
  printf '%s\n' 'Multimode interference, nonconstant shear, E.24, complete Version-M extraction, fixed deletion,'
  printf '%s\n' 'suitable-weak transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075s-full-frequency-single-harmonic-clock-payment","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$mutation_total"
