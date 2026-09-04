#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075l_single_harmonic_diffusive_signed_flux_gain_qa.sh"
FIXTURES="$ROOT/scripts/r075l_single_harmonic_diffusive_signed_flux_gain_fixtures.json"
EXPECTED="$ROOT/scripts/r075l_single_harmonic_diffusive_signed_flux_gain_expected.json"
MAIN="$ROOT/research/r075l_single_harmonic_diffusive_signed_flux_gain.md"
PRIMARY_AUDIT="$ROOT/research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075l_report-source.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
G_SOURCE="$ROOT/research/r075g_signed_flux_gain_threshold.md"
K_SOURCE="$ROOT/research/r075k_positive_majorant_high_frequency_trace_loss.md"
CERT="$ROOT/research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json"
REPORT="$ROOT/research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075l_single_harmonic_diffusive_signed_flux_gain_independent_audit.md"
QA_REPORT="$ROOT/research/r075l_single_harmonic_diffusive_signed_flux_gain_qa_report.md"

EXPECTED_MAIN_HASH=52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5
EXPECTED_PRIMARY_AUDIT_HASH=a7578e5370d182decc39f0da2f2fb581e5ef842ae7b914a120b5784bc32bd302
EXPECTED_REPORT_SOURCE_HASH=a300de54b9fe06e94455a055bbb42bdce8ec7bb004080389a95412966a5b941a
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_G_HASH=f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41
EXPECTED_K_HASH=9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf
EXPECTED_FIXTURES_HASH=0b9ba1f018b6e52414f20dee6687f5ff55c5ea0ef247ddbd905bc8c204245ad9
EXPECTED_EXPECTED_HASH=9178489eaf9f44c5b182b6080cce7212591b1a3dd86459ecbd82c1382b38db9a

TMP_ROOT=$(mktemp -d /tmp/r075l-certificate-qa.XXXXXX)
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
test "$(digest "$PRIMARY_AUDIT")" = "$EXPECTED_PRIMARY_AUDIT_HASH"
test "$(digest "$REPORT_SOURCE")" = "$EXPECTED_REPORT_SOURCE_HASH"
test "$(digest "$E_SOURCE")" = "$EXPECTED_E_HASH"
test "$(digest "$G_SOURCE")" = "$EXPECTED_G_HASH"
test "$(digest "$K_SOURCE")" = "$EXPECTED_K_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.' "$PRIMARY_AUDIT"
grep -q 'Equation tags L.1--L.17 are unique and consecutive.' "$PRIMARY_AUDIT"
grep -q 'All 17 display-math environments are paired.' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075L_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075L_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 19' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"kappaStar": "27163/71442"' "$CERT"
grep -q '"CStar": "1/8\*(9/(8\*c3))\^(2/3)"' "$CERT"
grep -q '"massCoefficientTimesOneMinusQ3": "24/25"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075L_JSON="$CERT" R075L_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":20' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 20/20' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift dependency_table_missing fixture_drift expected_drift tag reference display control operator_time operator_drift_symbol operator_diffusion time_decay time_phase drift_phase diffusion_sign passive_residual k_integer k_lower A_positive B_real real_field constant_shear single_harmonic square_frequency square_zero_coefficient square_side_coefficient diagonal_not_zero diagonal_after_absolute periodic_mean absolute_before_cancel eta_lower eta_upper eta_sample eta_measurable xi_periodic xi_smooth xi_real vxi_absolute vxi_bound time_decay_multiplier time_integral_sign time_integral_denominator q2_symbol q2_interval drop_q2_direction flux_half flux_square_half flux_coefficient flux_B_absolute flux_Vxi cos_quarter cos_symmetry cos_integral mass_decay_multiplier mass_denominator mass_amplitude mass_k_square mass_symbol q3_symbol condition_direction condition_one q3_comparison q3_float_equality c3_positive c3_symbol a2_prefactor a2_power_k a2_power_mass a2_inequality cstar_outer cstar_inner flux_A flux_k mass_A mass_k two_thirds ratio_k amplitude_cancel target_omega target_R payment_R payment_omega payment_M normalized_R normalized_omega normalized_k normalized_p positive_part alpha_numerator alpha_denominator kappa_multiplier kappa_reduce endpoint_equality decimal_display decimal_exact strict_direction R_interval frequency_direction physical_signed full_torus unpaid_BVxi g1_claim e24_claim full_versionm_claim multimode_closed collar_closed nonconstant_closed low_frequency_closed complete_clock fixed_deletion suitable_weak regularity singularity novelty priority simulation clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 \
    R075L_MUTATION="$mutation" \
    R075L_JSON="$TMP_ROOT/python-$mutation.json" \
    R075L_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" \
    2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075L_JSON="$CERT" \
    R075L_RUBY_MUTATION="$mutation" \
    R075L_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" \
    2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq 120
test "$ruby_mutations" -eq 120

if env R075L_MUTATION=unknown_mutation \
  R075L_JSON="$TMP_ROOT/unknown-python.json" \
  R075L_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" \
  2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075L_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075L_JSON="$CERT" \
  R075L_RUBY_MUTATION=unknown_mutation \
  R075L_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" \
  2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075L_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075L_JSON="$CERT" R075L_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
report_source_hash=$(digest "$REPORT_SOURCE")
e_source_hash=$(digest "$E_SOURCE")
g_source_hash=$(digest "$G_SOURCE")
k_source_hash=$(digest "$K_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75L certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 19/19'
  printf '%s\n' '- Ruby assertions: 20/20'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075l_single_harmonic_diffusive_signed_flux_gain.md | $main_hash |"
  printf '%s\n' "| research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075l_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075l_single_harmonic_diffusive_signed_flux_gain_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075l_single_harmonic_diffusive_signed_flux_gain_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075l_single_harmonic_diffusive_signed_flux_gain_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075l_single_harmonic_diffusive_signed_flux_gain_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit is checked against the frozen main SHA, PASS/0,'
  printf '%s\n' 'L.1--L.17, and 17/17 displays. The report-source is byte-bound only;'
  printf '%s\n' 'its literature search and access record are outside this finite certificate.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_source_hash |"
  printf '%s\n' "| research/r075g_signed_flux_gain_threshold.md | $g_source_hash |"
  printf '%s\n' "| research/r075k_positive_majorant_high_frequency_trace_loss.md | $k_source_hash |"
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- L_B signs and all three derivative rows of F_k cancel exactly: PASS.'
  printf '%s\n' '- F_k^2 has only 0,+/-2k modes; the diagonal is removed before absolute values: PASS.'
  printf '%s\n' '- 0<=eta<=1, V_xi, (1-q2)/(2k^2), and A^2|B|V_xi/(8k^2): PASS.'
  printf '%s\n' '- Integral |cos(kx)|^3=8/3 and M_k=8A^3(1-q3)/(9k^2): PASS.'
  printf '%s\n' '- q3<=exp(-3) is symbolic/ordered only; no floating equality is used: PASS.'
  printf '%s\n' '- A^2 conversion, C_*, k^(-2/3), and R^(1/3)omega^(1/3): PASS.'
  printf '%s\n' '- Strict kappa endpoint 27163/71442 and display-only decimal: PASS.'
  printf '%s\n' '- Tags L.1--L.17, references, 17/17 displays, and control bytes: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'This is limited to one real harmonic, constant shear, and a full-torus cubic'
  printf '%s\n' 'mass; |B|V_xi remains unpaid. It does not prove G.1, E.24, or the full Version-M'
  printf '%s\n' 'estimate. Multimode/collar/nonconstant-shear bounds, complete clock, fixed deletion,'
  printf '%s\n' 'suitable-weak transfer, regularity, and singularity remain open. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075l-single-harmonic-diffusive-signed-flux-gain","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
