#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075g_signed_flux_gain_threshold_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075g_signed_flux_gain_threshold_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075g_signed_flux_gain_threshold_qa.sh"
FIXTURES="$ROOT/scripts/r075g_signed_flux_gain_threshold_fixtures.json"
EXPECTED="$ROOT/scripts/r075g_signed_flux_gain_threshold_expected.json"
MAIN="$ROOT/research/r075g_signed_flux_gain_threshold.md"
PRIMARY_AUDIT="$ROOT/research/r075g_signed_flux_gain_threshold_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075g_report-source.md"
C_SOURCE="$ROOT/research/r075c_background_shear_packing_false_positive.md"
D_SOURCE="$ROOT/research/r075d_passive_gradient_route_screen.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
F_SOURCE="$ROOT/research/r075f_modal_phase_integration_identity.md"
CERT="$ROOT/research/r075g_signed_flux_gain_threshold_certificate.json"
REPORT="$ROOT/research/r075g_signed_flux_gain_threshold_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075g_signed_flux_gain_threshold_independent_audit.md"
QA_REPORT="$ROOT/research/r075g_signed_flux_gain_threshold_qa_report.md"

EXPECTED_MAIN_HASH=f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41
EXPECTED_PRIMARY_AUDIT_HASH=4717b365e5a4dc1bff169db51708a8a74fe51e6dd414a9a68a448813d95541aa
EXPECTED_REPORT_SOURCE_HASH=2722d2801945a2ee074b0a9c4a973f592849ae012ddd4c264b7fea5ad76e9896
EXPECTED_C_HASH=1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89
EXPECTED_D_HASH=54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_F_HASH=f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440
EXPECTED_FIXTURES_HASH=6bcf72a52763b04f98c21109fabbd570aa552cfe472280cff7ff4a0738eb0c9a
EXPECTED_EXPECTED_HASH=03b3475a3f8e82cb986e63ef52af6fdb899ac200b70024661c379542356b6ab0

TMP_ROOT=$(mktemp -d /tmp/r075g-certificate-qa.XXXXXX)
trap 'rm -rf "$TMP_ROOT"' EXIT

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

command -v "$PYTHON_BIN" >/dev/null
command -v ruby >/dev/null
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"
"$PYTHON_BIN" -m json.tool "$FIXTURES" >"$TMP_ROOT/fixtures.pretty"
"$PYTHON_BIN" -m json.tool "$EXPECTED" >"$TMP_ROOT/expected.pretty"

test "$(digest "$MAIN")" = "$EXPECTED_MAIN_HASH"
test "$(digest "$PRIMARY_AUDIT")" = "$EXPECTED_PRIMARY_AUDIT_HASH"
test "$(digest "$REPORT_SOURCE")" = "$EXPECTED_REPORT_SOURCE_HASH"
test "$(digest "$C_SOURCE")" = "$EXPECTED_C_HASH"
test "$(digest "$D_SOURCE")" = "$EXPECTED_D_HASH"
test "$(digest "$E_SOURCE")" = "$EXPECTED_E_HASH"
test "$(digest "$F_SOURCE")" = "$EXPECTED_F_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.' "$PRIMARY_AUDIT"
grep -q 'Equation tags G.1--G.24 are unique and consecutive.' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075G_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075G_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 16' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075G_JSON="$CERT" R075G_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":18' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 18/18' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift dependency_table_missing fixture_drift expected_drift tag reference display control g9_normalization_r g9_time_r g9_volume_l g9_volume_r g9_b_cubic_r g9_cube_root rho_value c_gamma_value alpha_formula alpha_fraction equality_non_strict equality_polynomial alpha_third_sign alpha_third_denominator alpha_quarter_sign alpha_quarter_denominator beta_factor beta_fraction amplitude_flux_degree amplitude_atom_degree amplitude_two_thirds amplitude_ratio zero_convention transport_pde_sign transport_energy_sign transport_endpoint_sign transport_flux_factor transport_cutoff_frequency passage_width_exponent passage_speed_exponent passage_occupation_product passage_window_exponent passage_winding conditional_proved threshold_necessary equality_closes quarter_counterexample amplitude_gain interaction_proved diffusion_benchmark_proved e24_closed full_clock fixed_deletion suitable_weak regularity clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 \
    R075G_MUTATION="$mutation" \
    R075G_JSON="$TMP_ROOT/python-$mutation.json" \
    R075G_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" \
    2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075G_JSON="$CERT" \
    R075G_RUBY_MUTATION="$mutation" \
    R075G_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" \
    2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq 57
test "$ruby_mutations" -eq 57

if env R075G_MUTATION=unknown_mutation \
  R075G_JSON="$TMP_ROOT/unknown-python.json" \
  R075G_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" \
  2>"$TMP_ROOT/unknown-python.stderr"; then
  echo "Python accepted an unknown mutation" >&2
  exit 1
fi
grep -q 'unknown R075G_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075G_JSON="$CERT" \
  R075G_RUBY_MUTATION=unknown_mutation \
  R075G_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" \
  2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo "Ruby accepted an unknown mutation" >&2
  exit 1
fi
grep -q 'unknown R075G_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-regenerate.stdout"
env R075G_JSON="$CERT" R075G_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
report_source_hash=$(digest "$REPORT_SOURCE")
c_source_hash=$(digest "$C_SOURCE")
d_source_hash=$(digest "$D_SOURCE")
e_source_hash=$(digest "$E_SOURCE")
f_source_hash=$(digest "$F_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75G certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Python assertions: 16/16'
  printf '%s\n' '- Ruby assertions: 18/18'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075g_signed_flux_gain_threshold.md | $main_hash |"
  printf '%s\n' "| research/r075g_signed_flux_gain_threshold_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075g_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075g_signed_flux_gain_threshold_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075g_signed_flux_gain_threshold_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075g_signed_flux_gain_threshold_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075g_signed_flux_gain_threshold_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075g_signed_flux_gain_threshold_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075g_signed_flux_gain_threshold_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075g_signed_flux_gain_threshold_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075g_signed_flux_gain_threshold_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit was checked for the frozen main hash, PASS with zero'
  printf '%s\n' 'mathematical and release blockers, and G.1--G.24 coverage.'
  printf '%s\n' 'The report-source file is byte-bound only; literature content and'
  printf '%s\n' 'recorded HTTP access checks are outside this finite certificate.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075c_background_shear_packing_false_positive.md | $c_source_hash |"
  printf '%s\n' "| research/r075d_passive_gradient_route_screen.md | $d_source_hash |"
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_source_hash |"
  printf '%s\n' "| research/r075f_modal_phase_integration_identity.md | $f_source_hash |"
  printf '%s\n' ''
  printf '%s\n' 'All hashes match the G main note source table and both implementations.'
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- G.9 product and G.10 L/R/omega cube-root exponents: PASS.'
  printf '%s\n' '- alpha*=27163/107163, strict equality boundary, and alpha=1/3,1/4 margins: PASS.'
  printf '%s\n' '- beta*=27163/35721 and beta=3alpha conversion: PASS.'
  printf '%s\n' '- Exact positive-amplitude quadratic/cubic homogeneity family: PASS.'
  printf '%s\n' '- Smooth pure-transport positive flux and endpoint difference, both 1/32: PASS.'
  printf '%s\n' '- Single unwrapped rational crossing with O(R^3) occupation and O(R) fraction: PASS.'
  printf '%s\n' '- Tags G.1--G.24, references, and 24/24 displays: PASS.'
  printf '%s\n' '- Main/audit/source/dependencies/fixtures/expected byte bindings: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The threshold is sufficient only for the hypothesized G.1 route.'
  printf '%s\n' 'The equality case retains the growing L^(2/3) factor; the 1/4 result is'
  printf '%s\n' 'not a counterexample. The transport and one-passage examples do not'
  printf '%s\n' 'prove the arbitrary diffusive interaction estimate. G.1, G.18, G.24,'
  printf '%s\n' 'E.24, complete clock, fixed deletion, suitable-weak transfer,'
  printf '%s\n' 'regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075g-signed-flux-gain-threshold","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
