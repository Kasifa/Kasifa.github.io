#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
STEM=r075t_two_harmonic_collar_coercivity
PY_SCRIPT="$ROOT/scripts/${STEM}_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/${STEM}_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/${STEM}_qa.sh"
FIXTURES="$ROOT/scripts/${STEM}_fixtures.json"
EXPECTED="$ROOT/scripts/${STEM}_expected.json"
MAIN="$ROOT/research/${STEM}.md"
PRIMARY="$ROOT/research/${STEM}_primary_audit.md"
SOURCE="$ROOT/research/r075t_report-source.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
M_SOURCE="$ROOT/research/r075m_dyadic_packet_diffusive_flux_gain.md"
R_SOURCE="$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md"
S_SOURCE="$ROOT/research/r075s_full_frequency_single_harmonic_clock_payment.md"
CERT="$ROOT/research/${STEM}_certificate.json"
REPORT="$ROOT/research/${STEM}_certificate_report.md"
RUBY_REPORT="$ROOT/research/${STEM}_independent_audit.md"
QA_REPORT="$ROOT/research/${STEM}_qa_report.md"

EXPECTED_MAIN_HASH=822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66
EXPECTED_PRIMARY_HASH=97d804444737284d7ec40b3ce45389272b1a9f61d1901f7bcebf9ed0eab935e5
EXPECTED_SOURCE_HASH=c2255cdd07f2e490921d93ba7e62a809c0348a9e6136b7fd5537cf3799e4e8d8
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_M_HASH=13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7
EXPECTED_R_HASH=e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
EXPECTED_S_HASH=d2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd
EXPECTED_FIXTURES_HASH=939b04eeccb9c96b6d5cb21d49ebc48e7a8387dfccdc08afd2dfd6db77fd4393
EXPECTED_EXPECTED_HASH=cd58217667129d5a2f01dd2b315b86a934de1258be2eefab401f5b66efc127c5

TMP_ROOT=$(mktemp -d /tmp/r075t-certificate-qa.XXXXXX)
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
test "$(digest "$E_SOURCE")" = "$EXPECTED_E_HASH"
test "$(digest "$M_SOURCE")" = "$EXPECTED_M_HASH"
test "$(digest "$R_SOURCE")" = "$EXPECTED_R_HASH"
test "$(digest "$S_SOURCE")" = "$EXPECTED_S_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q 'Current verdict: \*\*PASS\*\*' "$PRIMARY"
grep -q 'Mathematical blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'Release blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'falsification aid only' "$PRIMARY"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075T_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075T_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 14' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"ell": "1/2"' "$CERT"
grep -q '"radialSquaredDifference": "1/8"' "$CERT"
grep -q '"hSquared": "9/16"' "$CERT"
grep -q '"hSquared": "79/16"' "$CERT"
grep -q '"hSquared": "19"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075T_JSON="$CERT" R075T_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":15' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 15/15' "$RUBY_REPORT"
grep -q 'Blocker count: 0' "$RUBY_REPORT"

mutations=$("$PYTHON_BIN" -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["negativeMutations"]))' "$CERT")
mutation_total=$(printf '%s\n' "$mutations" | awk 'NF {n++} END {print n+0}')
python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R075T_MUTATION="$mutation" \
    R075T_JSON="$TMP_ROOT/python-$mutation.json" \
    R075T_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R075T_JSON="$CERT" R075T_RUBY_MUTATION="$mutation" \
    R075T_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
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

if env R075T_MUTATION=unknown_mutation \
  R075T_JSON="$TMP_ROOT/unknown-python.json" R075T_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075T_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075T_JSON="$CERT" R075T_RUBY_MUTATION=unknown_mutation \
  R075T_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075T_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075T_JSON="$CERT" R075T_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
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
  printf '%s\n' '# R0.75T certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 14/14'
  printf '%s\n' '- Ruby assertions: 15/15'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$mutation_total Python; $ruby_mutations/$mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  printf '%s\n' "| research/${STEM}.md | $main_hash |"
  printf '%s\n' "| research/${STEM}_primary_audit.md | $primary_hash |"
  printf '%s\n' "| research/r075t_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/${STEM}_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/${STEM}_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/${STEM}_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/${STEM}_qa.sh | $qa_hash |"
  printf '%s\n' "| research/${STEM}_certificate.json | $cert_hash |"
  printf '%s\n' "| research/${STEM}_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/${STEM}_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- T.1--T.31, 31/31 tags, 32/32 displays, four dependencies, references, UTF-8, and control bytes: PASS.'
  printf '%s\n' '- Exact central plateau fibre and a^2 R^3 geometry: PASS.'
  printf '%s\n' '- Uniform beta-to-zero envelope basis and resolved/unresolved beat split: PASS.'
  printf '%s\n' '- Holder cubic conversion, unequal heat rates, and four-term flux identity: PASS.'
  printf '%s\n' '- Finite probes are explicitly excluded as proof of continuum constants: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The source report is byte-bound; its primary-source screen is bounded and establishes no novelty.'
  printf '%s\n' 'T proves spatial collar coercivity only for one dyadic pair with m a R >= C_0.'
  printf '%s\n' 'T.31, complete two-mode payment, low carriers, three or more modes, arbitrary-field E.24,'
  printf '%s\n' 'Version-M extraction, suitable-weak transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075t-two-harmonic-collar-coercivity","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$mutation_total"
