#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075m_dyadic_packet_diffusive_flux_gain_qa.sh"
FIXTURES="$ROOT/scripts/r075m_dyadic_packet_diffusive_flux_gain_fixtures.json"
EXPECTED="$ROOT/scripts/r075m_dyadic_packet_diffusive_flux_gain_expected.json"
MAIN="$ROOT/research/r075m_dyadic_packet_diffusive_flux_gain.md"
PRIMARY_AUDIT="$ROOT/research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075m_report-source.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
G_SOURCE="$ROOT/research/r075g_signed_flux_gain_threshold.md"
L_SOURCE="$ROOT/research/r075l_single_harmonic_diffusive_signed_flux_gain.md"
CERT="$ROOT/research/r075m_dyadic_packet_diffusive_flux_gain_certificate.json"
REPORT="$ROOT/research/r075m_dyadic_packet_diffusive_flux_gain_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075m_dyadic_packet_diffusive_flux_gain_independent_audit.md"
QA_REPORT="$ROOT/research/r075m_dyadic_packet_diffusive_flux_gain_qa_report.md"

EXPECTED_MAIN_HASH=13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7
EXPECTED_PRIMARY_AUDIT_HASH=2b5ee050c09e3be925143c12c29082c3fe562a83b9a2d2669511a2bb1684d7dc
EXPECTED_REPORT_SOURCE_HASH=f8ed7af8ef5051b0efa73177d0530562917d55dfa6476b00b8f871db0da99d67
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_G_HASH=f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41
EXPECTED_L_HASH=52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5
EXPECTED_FIXTURES_HASH=b93d727b4bf0729af2064e51fbc0c1450d98806c9b92fe11727b4d5423fa157f
EXPECTED_EXPECTED_HASH=cef1705998bc935448f371d6f389d46059b59e99bf230bd75dad0489fb85a4f4

TMP_ROOT=$(mktemp -d /tmp/r075m-certificate-qa.XXXXXX)
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
test "$(digest "$L_SOURCE")" = "$EXPECTED_L_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.' "$PRIMARY_AUDIT"
grep -q 'Equation tags M.1--M.20 are unique and consecutive.' "$PRIMARY_AUDIT"
grep -q 'All 20 display-math environments are paired.' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075M_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075M_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 19' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"fluxKernelFactor": "pi\*B"' "$CERT"
grep -q '"finalEnergyCoefficient": "Wxi/(4\*K\^2)"' "$CERT"
grep -q '"rational": "4"' "$CERT"
grep -q '"kappaStar": "27163/71442"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075M_JSON="$CERT" R075M_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":20' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 20/20' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift dependency_table_missing fixture_drift expected_drift tag reference display control operator_time operator_drift operator_diffusion fourier_factor reconstruction_sign difference_index spatial_factor flux_half modal_prefactor d0_nonzero cancel_after_absolute absolute_before_diagonal time_phase time_decay diffusion_sign passive_residual K_lower K_upper K_integer packet_finite real_symmetry mode_count eta_lower eta_upper eta_measurable xi_periodic xi_smooth xi_real W_definition time_kernel_absolute time_kernel_infinity kernel_denominator denominator_lower denominator_factor row_sum column_sum schur_direction schur_sqrt quadratic_form mode_count_loss parseval_factor energy_quarter short_window short_window_inside upper_edge l2_decay_multiplier l2_endpoint l2_direction holder_measure holder_direction l3_endpoint mass_window mass_constant mass_K_power mass_E_power condition inversion_constant inversion_e_power inversion_2pi_power inversion_K_power inversion_M_power inverse_heat combined_constant combined_e_power combined_2pi_power combined_K_power combined_M_power combined_B_power combined_W_power amplitude_degree wiener_weight wiener_cs_direction wiener_inverse_series wiener_weighted_sum wiener_parseval wiener_first_derivative wiener_second_derivative wiener_third_derivative pointwise_replacement target_R target_omega payment_R payment_omega payment_M normalized_R normalized_omega normalized_K normalized_p positive_part R_positive omega_positive alpha_numerator alpha_denominator kappa_multiplier kappa_reduce strict_direction endpoint_equality R_domain frequency_direction physical_signed full_torus single_packet arbitrary_interference interpacket_closed cutoff_calibrated collar_localized local_versionm low_difference_closed nonconstant_closed e24_claim complete_clock fixed_deletion suitable_weak regularity singularity novelty priority simulation clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R075M_MUTATION="$mutation" \
    R075M_JSON="$TMP_ROOT/python-$mutation.json" \
    R075M_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075M_JSON="$CERT" R075M_RUBY_MUTATION="$mutation" \
    R075M_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq 130
test "$ruby_mutations" -eq 130

if env R075M_MUTATION=unknown_mutation \
  R075M_JSON="$TMP_ROOT/unknown-python.json" R075M_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075M_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075M_JSON="$CERT" R075M_RUBY_MUTATION=unknown_mutation \
  R075M_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075M_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075M_JSON="$CERT" R075M_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
report_source_hash=$(digest "$REPORT_SOURCE")
e_source_hash=$(digest "$E_SOURCE")
g_source_hash=$(digest "$G_SOURCE")
l_source_hash=$(digest "$L_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75M certificate QA report' ''
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
  printf '%s\n' "| research/r075m_dyadic_packet_diffusive_flux_gain.md | $main_hash |"
  printf '%s\n' "| research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075m_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075m_dyadic_packet_diffusive_flux_gain_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075m_dyadic_packet_diffusive_flux_gain_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075m_dyadic_packet_diffusive_flux_gain_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075m_dyadic_packet_diffusive_flux_gain_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075m_dyadic_packet_diffusive_flux_gain_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075m_dyadic_packet_diffusive_flux_gain_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit is checked against the frozen main SHA, PASS/0,'
  printf '%s\n' 'M.1--M.20, and 20/20 displays. The report-source is byte-bound only;'
  printf '%s\n' 'its literature search and access record are outside this finite certificate.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_source_hash |"
  printf '%s\n' "| research/r075g_signed_flux_gain_threshold.md | $g_source_hash |"
  printf '%s\n' "| research/r075l_single_harmonic_diffusive_signed_flux_gain.md | $l_source_hash |"
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- Fourier convention, 2*pi spatial pairing, pi*B kernel, and d_0 cancellation: PASS.'
  printf '%s\n' '- Schur row/column bounds, Parseval, no mode-count factor, and exact 1/4: PASS.'
  printf '%s\n' '- Short-time L2/L3 factors and cubic lower bound: PASS.'
  printf '%s\n' '- Inversion 4e(2*pi)^(1/3) and combined e(2*pi)^(1/3): PASS.'
  printf '%s\n' '- Wiener--H1 weighted Cauchy--Schwarz and first/second derivative row: PASS.'
  printf '%s\n' '- Normalization R^(1/3)omega^(1/3)K^(-2/3)p^(2/3): PASS.'
  printf '%s\n' '- Strict threshold 27163/71442 and small-R power direction: PASS.'
  printf '%s\n' '- Tags M.1--M.20, references, 20/20 displays, and control bytes: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The result covers arbitrary finite interference within one real dyadic packet'
  printf '%s\n' 'only. Inter-packet summation, cutoff Wiener calibration, collar/local Version-M'
  printf '%s\n' 'payment, nonconstant shear, low differences, E.24, complete clock, fixed'
  printf '%s\n' 'deletion, suitable-weak transfer, regularity, and singularity remain OPEN.'
  printf '%s\n' '**NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075m-dyadic-packet-diffusive-flux-gain","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
