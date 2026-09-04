#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075n_radial_collar_averaged_wiener_row_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075n_radial_collar_averaged_wiener_row_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075n_radial_collar_averaged_wiener_row_qa.sh"
FIXTURES="$ROOT/scripts/r075n_radial_collar_averaged_wiener_row_fixtures.json"
EXPECTED="$ROOT/scripts/r075n_radial_collar_averaged_wiener_row_expected.json"
MAIN="$ROOT/research/r075n_radial_collar_averaged_wiener_row.md"
PRIMARY_AUDIT="$ROOT/research/r075n_radial_collar_averaged_wiener_row_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075n_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
C_SOURCE="$ROOT/research/r075c_background_shear_packing_false_positive.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
M_SOURCE="$ROOT/research/r075m_dyadic_packet_diffusive_flux_gain.md"
CERT="$ROOT/research/r075n_radial_collar_averaged_wiener_row_certificate.json"
REPORT="$ROOT/research/r075n_radial_collar_averaged_wiener_row_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075n_radial_collar_averaged_wiener_row_independent_audit.md"
QA_REPORT="$ROOT/research/r075n_radial_collar_averaged_wiener_row_qa_report.md"

EXPECTED_MAIN_HASH=ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318
EXPECTED_PRIMARY_AUDIT_HASH=c43c063b1c003be22782e7d8e1ce0b3f42cdd3ef4d01912c9de34c876d8c9aba
EXPECTED_REPORT_SOURCE_HASH=ae9d5d630ee0549193c016fcbc07c599b0c678fbaf9c15c5d3c7f24bdf18e27c
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_C_HASH=1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_M_HASH=13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7
EXPECTED_FIXTURES_HASH=2dee2146f94f3fa6d0d0c5828d8d6f354f0856f620e1261a133c9a2c81f8a0cb
EXPECTED_EXPECTED_HASH=31614fc11bc4355723fff7773bec8ab13bc44808ffffa0958c78ec1cfe2bba48

TMP_ROOT=$(mktemp -d /tmp/r075n-certificate-qa.XXXXXX)
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
test "$(digest "$B_SOURCE")" = "$EXPECTED_B_HASH"
test "$(digest "$C_SOURCE")" = "$EXPECTED_C_HASH"
test "$(digest "$E_SOURCE")" = "$EXPECTED_E_HASH"
test "$(digest "$M_SOURCE")" = "$EXPECTED_M_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.' "$PRIMARY_AUDIT"
grep -q 'Equation tags N.1--N.17 are unique and consecutive.' "$PRIMARY_AUDIT"
grep -q 'All 17 display-math environments are paired.' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075N_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075N_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 16' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"normalization": "1/(2\*pi)"' "$CERT"
grep -q '"derivativeRule": "d_ell=i\*ell\*Xi_ell"' "$CERT"
grep -q '"dZero": "0+0i"' "$CERT"
grep -q '"highReciprocalTailBound": "1/2"' "$CERT"
grep -q '"uniformCapOverPi": "32"' "$CERT"
grep -q '"volumeOverPi": "1544/3"' "$CERT"
grep -q '"KLowerRPower": "-3/2"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075N_JSON="$CERT" R075N_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":17' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 17/17' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift dependency_table_missing fixture_drift expected_drift tag reference display control p_reciprocal a_definition r_definition R_range a_condition central_chart periodic_overlap profile_fixed profile_smooth profile_nonnegative profile_support profile_plateau B_choice_freedom canonical_universal derivative_cost fourier_normalization fourier_sign derivative_i derivative_ell d0 integration_by_parts reconstruction_phase sampling_compact sampling_W21 sampling_uniform_A sampling_nu sampling_R sup_sum_order low_cutoff low_count low_L1 low_R_power high_one_ibp high_denominator high_tail_direction high_tail_R high_raw high_R_power discrete_riemann slice_scaling_x1 slice_derivative_R slice_fourier_R slice_2pi slice_empty_range slice_interior_difference slice_area_factor tangency_missing tangency_cap outer_disk radial_lower radial_first_derivative radial_third_derivative radial_uniform fubini_direction slice_L1_a sum_all_modes coefficientwise_sup row_R_loss row_a_power full_average_jacobian full_derivative_R full_fourier_R full_shell_formula full_shell_volume_power full_fubini_a full_row_R full_row_a wiener_h1_substitution frequency_K frequency_gain frequency_direction frequency_R frequency_first_L frequency_first_R frequency_full_L frequency_full_R frequency_threshold physical_coefficient_only dynamical_flux_claim canonical_required all_cutoffs_claim vertical_diffusion_closed nonconstant_shear_closed local_cubic_closed interpacket_closed low_difference_closed e24_claim complete_clock fixed_deletion suitable_weak regularity singularity novelty priority simulation clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R075N_MUTATION="$mutation" \
    R075N_JSON="$TMP_ROOT/python-$mutation.json" \
    R075N_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075N_JSON="$CERT" R075N_RUBY_MUTATION="$mutation" \
    R075N_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq 107
test "$ruby_mutations" -eq 107

if env R075N_MUTATION=unknown_mutation \
  R075N_JSON="$TMP_ROOT/unknown-python.json" R075N_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075N_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075N_JSON="$CERT" R075N_RUBY_MUTATION=unknown_mutation \
  R075N_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075N_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075N_JSON="$CERT" R075N_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
report_source_hash=$(digest "$REPORT_SOURCE")
b_source_hash=$(digest "$B_SOURCE")
c_source_hash=$(digest "$C_SOURCE")
e_source_hash=$(digest "$E_SOURCE")
m_source_hash=$(digest "$M_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75N certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 16/16'
  printf '%s\n' '- Ruby assertions: 17/17'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075n_radial_collar_averaged_wiener_row.md | $main_hash |"
  printf '%s\n' "| research/r075n_radial_collar_averaged_wiener_row_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075n_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075n_radial_collar_averaged_wiener_row_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075n_radial_collar_averaged_wiener_row_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075n_radial_collar_averaged_wiener_row_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075n_radial_collar_averaged_wiener_row_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075n_radial_collar_averaged_wiener_row_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075n_radial_collar_averaged_wiener_row_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075n_radial_collar_averaged_wiener_row_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075n_radial_collar_averaged_wiener_row_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit is checked against the frozen main SHA, PASS/0,'
  printf '%s\n' 'N.1--N.17, and 17/17 displays. The report-source is byte-bound only;'
  printf '%s\n' 'its literature search and access record are outside this finite certificate.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075b_bulk_clock_outer_padding_gate.md | $b_source_hash |"
  printf '%s\n' "| research/r075c_background_shear_packing_false_positive.md | $c_source_hash |"
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_source_hash |"
  printf '%s\n' "| research/r075m_dyadic_packet_diffusive_flux_gain.md | $m_source_hash |"
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- B leaves cutoff choice freedom; the radial collar is a selectable canonical cover, not universal necessity: PASS.'
  printf '%s\n' '- Fourier normalization 1/(2*pi), d_ell=+i*ell*Xi_ell, and d_0=0: PASS.'
  printf '%s\n' '- Low/high sampling split, two integrations by parts, tail O(R), and sum_l sup_z order: PASS.'
  printf '%s\n' '- Exact disk slices, including tangencies, satisfy the uniform 4*pi*a*delta cap: PASS.'
  printf '%s\n' '- Radial first/third derivatives and Fubini L1 bounds O(a) and O(a^2): PASS.'
  printf '%s\n' '- x1/full averaging scales R/R^2; Wiener rows are O(a) and O(Ra^2): PASS.'
  printf '%s\n' '- K>=R^(-3/2) yields K^(-2/3)<=R and outputs LR and L^2R^2: PASS.'
  printf '%s\n' '- Tags N.1--N.17, references, 17/17 displays, dependencies, and control bytes: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'This certifies only the selected canonical geometric coefficient rows.'
  printf '%s\n' 'It proves neither a universal cutoff statement nor a dynamical flux theorem.'
  printf '%s\n' 'Vertical diffusion, nonconstant shear, local cubic payment, inter-packet'
  printf '%s\n' 'summation, low differences, E.24, complete clock, fixed deletion,'
  printf '%s\n' 'suitable-weak transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075n-radial-collar-averaged-wiener-row","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
