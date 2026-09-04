#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
STEM=r076b_moderate_carrier_fixed_mode_flux_payment
PY_SCRIPT="$ROOT/scripts/$STEM"_certificate.py
RUBY_SCRIPT="$ROOT/scripts/$STEM"_certificate_independent.rb
QA_SCRIPT="$ROOT/scripts/$STEM"_qa.sh
FIXTURES="$ROOT/scripts/$STEM"_fixtures.json
EXPECTED="$ROOT/scripts/$STEM"_expected.json
MAIN="$ROOT/research/$STEM".md
PRIMARY="$ROOT/research/$STEM"_primary_audit.md
SOURCE="$ROOT/research/r076b_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
R_SOURCE="$ROOT/research/r075r_outer_cap_spectral_concentration_obstruction.md"
W_SOURCE="$ROOT/research/r075w_full_frequency_two_harmonic_flux_payment.md"
X_SOURCE="$ROOT/research/r075x_fixed_finite_mode_low_carrier_payment.md"
Z_SOURCE="$ROOT/research/r075z_unresolved_cluster_carrier_current_gate.md"
A_SOURCE="$ROOT/research/r076a_complete_clock_localized_current_sign_obstruction.md"
CERT="$ROOT/research/$STEM"_certificate.json
REPORT="$ROOT/research/$STEM"_certificate_report.md
RUBY_REPORT="$ROOT/research/$STEM"_independent_audit.md
QA_REPORT="$ROOT/research/$STEM"_qa_report.md

EXPECTED_MAIN_HASH=a8a4cc853ec1029cb52afee724a4a783da156bd57de5399c58a7f42e2ab0306d
EXPECTED_PRIMARY_HASH=0a6314c454021da284bbf157de36d6c2bd1683d600a21c8394f723acc26aa447
EXPECTED_SOURCE_HASH=362fcf898a533efaf4072c876dba09f4231c131ad1c48d48efc92c52215428fc
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_R_HASH=e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3
EXPECTED_W_HASH=571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4
EXPECTED_X_HASH=8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763
EXPECTED_Z_HASH=30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97
EXPECTED_A_HASH=d23532f84702be1630daa0b8d56d02242571dd8a1f8024c59a7f71bec30f26eb
EXPECTED_FIXTURES_HASH=1f9b3df9cb8ff3f9d22250ce425b837d40268829bf18cb3e12b3f7d2dca64bf2
EXPECTED_EXPECTED_HASH=4533edf290e07f1fddc5df1b9ef1655a5623f4a3714e840b1c402cdf3b8db3f1
EXPECTED_PY_HASH=b4ec0ba8fbbe9033dcec3254a1acc3a4f7e662fe320c4697f253f575aa98863a
EXPECTED_RUBY_HASH=0b53934fc132eda0c51a5885d8b50089b74897aeaff1373e1033bc825c43e849
EXPECTED_CERT_HASH=d825624473f176c054134a75a47cb63fee65f7fe3bfe946ae505522a9c3c053e
EXPECTED_REPORT_HASH=5ae840453141f3059b94459996f7aaf808766fe3367ea433251343de128f938e
EXPECTED_RUBY_REPORT_HASH=1962313e8898dd6cdbafa9f1b543712d3660c25521c039e5311b21629bb1f6bf

TMP_ROOT=$(mktemp -d /tmp/r076b-certificate-qa.XXXXXX)
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
test "$(digest "$R_SOURCE")" = "$EXPECTED_R_HASH"
test "$(digest "$W_SOURCE")" = "$EXPECTED_W_HASH"
test "$(digest "$X_SOURCE")" = "$EXPECTED_X_HASH"
test "$(digest "$Z_SOURCE")" = "$EXPECTED_Z_HASH"
test "$(digest "$A_SOURCE")" = "$EXPECTED_A_HASH"
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
grep -q 'standalone carrier-block method' "$PRIMARY"

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
tags = [int(value) for value in re.findall(r"\\tag\{B\.(\d+)\}", text)]
if tags != list(range(1, 42)):
    raise SystemExit(f"bad B tag sequence: {tags}")
opens = len(re.findall(r"(?m)^\\\[$", text))
closes = len(re.findall(r"(?m)^\\\]$", text))
if opens != 41 or closes != 41:
    raise SystemExit(f"bad display delimiters: {opens}/{closes}")
refs = [int(value) for value in re.findall(r"\bB\.(\d+)\b", text)]
if set(refs) - set(tags):
    raise SystemExit(f"dangling B references: {sorted(set(refs)-set(tags))}")
for required in (
    r"n_1,\ldots,n_q\in\mathbb N",
    r"\phi_j\in\mathbb R",
    r"\mathcal Q_z(s)",
    r"\left(\frac\alpha a\right)^2h(s)^{2/3}",
    r"-\frac2{11907}",
):
    if required not in text:
        raise SystemExit(f"missing TeX fragment: {required}")
PY

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" R076B_JSON="$TMP_ROOT/certificate-$seed.json" \
    R076B_REPORT="$TMP_ROOT/report-$seed.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 15' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"fixedQInverseRadiusPayment": "PROVED"' "$CERT"
grep -q '"analyticDensitySubblock": "NOT_USED"' "$CERT"
grep -q '"standaloneCarrierSpatialIntegrationByParts": "REJECTED"' "$CERT"
grep -q '"ultraHighCarrier": "OPEN"' "$CERT"
grep -q '"alphas": \[' "$CERT"
grep -q '"normalizedPointDerivative": "289/144"' "$CERT"
grep -q '"Gs": "-1039967/20736"' "$CERT"
grep -q '"scaledPdeResidual": "0"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R076B_JSON="$CERT" R076B_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
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
  if env PYTHONHASHSEED=0 R076B_MUTATION="$mutation" \
    R076B_JSON="$TMP_ROOT/python-$mutation.json" R076B_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    printf '%s\n' "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  python_mutations=$((python_mutations + 1))

  if env R076B_JSON="$CERT" R076B_RUBY_MUTATION="$mutation" \
    R076B_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    printf '%s\n' "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq "$mutation_total"
test "$ruby_mutations" -eq "$mutation_total"

if env R076B_MUTATION=unknown_mutation R076B_JSON="$TMP_ROOT/unknown-python.json" \
  R076B_REPORT="$TMP_ROOT/unknown-python.md" "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  printf '%s\n' 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076B_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R076B_JSON="$CERT" R076B_RUBY_MUTATION=unknown_mutation \
  R076B_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  printf '%s\n' 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076B_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R076B_JSON="$CERT" R076B_RUBY_REPORT="$RUBY_REPORT" ruby "$RUBY_SCRIPT" \
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
  printf '%s\n' '# R0.76B certificate QA report' ''
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
  printf '%s\n' "| research/r076b_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/"$STEM"_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/"$STEM"_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/"$STEM"_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/"$STEM"_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/"$STEM"_qa.sh | $qa_hash |"
  printf '%s\n' "| research/"$STEM"_certificate.json | $cert_hash |"
  printf '%s\n' "| research/"$STEM"_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/"$STEM"_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' '' '## Checks' ''
  printf '%s\n' '- B.1--B.41, 41/41 tags and displays, six frozen dependencies, references, UTF-8, controls, and TeX escapes: PASS.'
  printf '%s\n' '- Exact q=3 inverse-radius endpoint, window ratios, temporal rates, PDE point, and scale ledger: PASS.'
  printf '%s\n' '- Complete-real-field energy identity and the (alpha/a)^2 gradient absorption are checked independently: PASS.'
  printf '%s\n' '- The analytic density subblock and failed standalone carrier integration-by-parts route are not used: PASS.'
  printf '%s\n' '- Finite fixtures are explicitly excluded as proof of the continuum observation lemmas: PASS.'
  printf '%s\n' '- Formal scientific figure: not applicable to this analytic theorem; no simulation claim is made.'
  printf '%s\n' ''
  printf '%s\n' 'The bounded source report imports only Turan--Nazarov and makes no novelty or priority claim.'
  printf '%s\n' 'R0.76B proves the fixed-q exact-shear estimate only for n_1 R <= 1.'
  printf '%s\n' 'Ultra-high carriers, growing packets, Version-M transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r076b-moderate-carrier-fixed-mode-flux-payment","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$mutation_total"
