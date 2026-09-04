#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075o_vertical_diffusion_packet_gain_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075o_vertical_diffusion_packet_gain_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075o_vertical_diffusion_packet_gain_qa.sh"
FIXTURES="$ROOT/scripts/r075o_vertical_diffusion_packet_gain_fixtures.json"
EXPECTED="$ROOT/scripts/r075o_vertical_diffusion_packet_gain_expected.json"
MAIN="$ROOT/research/r075o_vertical_diffusion_packet_gain.md"
PRIMARY_AUDIT="$ROOT/research/r075o_vertical_diffusion_packet_gain_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075o_report-source.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
G_SOURCE="$ROOT/research/r075g_signed_flux_gain_threshold.md"
M_SOURCE="$ROOT/research/r075m_dyadic_packet_diffusive_flux_gain.md"
N_SOURCE="$ROOT/research/r075n_radial_collar_averaged_wiener_row.md"
CERT="$ROOT/research/r075o_vertical_diffusion_packet_gain_certificate.json"
REPORT="$ROOT/research/r075o_vertical_diffusion_packet_gain_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075o_vertical_diffusion_packet_gain_independent_audit.md"
QA_REPORT="$ROOT/research/r075o_vertical_diffusion_packet_gain_qa_report.md"

EXPECTED_MAIN_HASH=3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9
EXPECTED_PRIMARY_AUDIT_HASH=27f9341f93bd2b031dbd3fd0e8d745788d5ff36a085ddb8be4ef8e1c5553e69b
EXPECTED_REPORT_SOURCE_HASH=9d2c234b0ba2a33b0f573a7933c26bcc751db6fe85919f2e146a0e6a18128c2b
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_G_HASH=f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41
EXPECTED_M_HASH=13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7
EXPECTED_N_HASH=ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318
EXPECTED_FIXTURES_HASH=46dff6097c3a052dc968f1c712c3421105ea5be51d3c905c492cc463cc04f0ad
EXPECTED_EXPECTED_HASH=228ac56e500a32b1f7c64c04d4110c78c4105c4d2a997fa8b108bd7449d59833

TMP_ROOT=$(mktemp -d /tmp/r075o-certificate-qa.XXXXXX)
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
test "$(digest "$M_SOURCE")" = "$EXPECTED_M_HASH"
test "$(digest "$N_SOURCE")" = "$EXPECTED_N_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q 'Verdict: \*\*PASS\*\*' "$PRIMARY_AUDIT"
grep -q 'Mathematical blocker count: \*\*0\*\*' "$PRIMARY_AUDIT"
grep -q 'Release blocker count: \*\*0\*\*' "$PRIMARY_AUDIT"
grep -q 'main-note SHA-256 is to be frozen by the finite certificate' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075O_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075O_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 19' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"fluxOverPiPerUnitX3": "-15"' "$CERT"
grep -q '"finalEnergyBoundOverPi": "105/2"' "$CERT"
grep -q '"massRationalWithoutEPi": "1/144"' "$CERT"
grep -q '"combinedConstant": "e\*(2\*pi)\^(2/3)"' "$CERT"
grep -q '"kappaStar": "98605/71442"' "$CERT"
grep -q '"displayedExponent": "-4279/238140000"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075O_JSON="$CERT" R075O_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":20' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 20/20' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift dependency_table_missing fixture_drift expected_drift tag reference display control operator_time operator_drift operator_vertical_diffusion evolution_horizontal_decay evolution_shear_phase evolution_vertical_semigroup constant_shear flux_outer_half flux_spatial_2pi flux_difference_index reconstruction_sign flux_real_part flux_B_sign d0 diagonal_before_absolute eta_lower eta_upper eta_measurable xi_real_periodic w_infty_finite vertical_heat_growth vertical_square_missing vertical_l2_norm vertical_contraction_direction arbitrary_vertical_energy vertical_cap_energy time_kernel_denominator time_kernel_infinity denominator_lower row_sum column_sum schur_direction schur_sqrt quadratic_form_direction mode_count_loss parseval_factor energy_quarter horizontal_K_lower total_frequency_cap horizontal_only_cap finite_packet real_symmetry K_integer K2T_condition short_interval short_interval_inside heat_square cap_four l2_floor_direction holder_volume holder_direction holder_power torus_dimension time_length mass_16 mass_pi mass_e inversion_direction inversion_e inversion_16pi inversion_K inversion_M combine_div4 combine_constant vertical_cardinality_loss payment_R payment_omega flux_R flux_omega mass_power frequency_power positive_part normalized_R normalized_omega normalized_K normalized_p amplitude_degree wiener_row wiener_L canonical_only universal_cutoff shear_R B_constant plateau_shear coefficient_R kappa_direction kappa_numerator kappa_denominator kappa_half kappa_reduce kappa_decimal strict_direction equality_allowed frozen_kappa rate_rho rate_cgamma rate_sign rate_fraction L_prefactor R_domain omega_positive own_full_torus_atom versionm_claim collar_localized arbitrary_vertical_cubic remove_total_cap nonconstant_closed interpacket_closed lowdifference_closed e24_claim complete_clock fixed_deletion suitable_weak regularity singularity novelty priority literature_complete simulation dns clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R075O_MUTATION="$mutation" \
    R075O_JSON="$TMP_ROOT/python-$mutation.json" \
    R075O_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075O_JSON="$CERT" R075O_RUBY_MUTATION="$mutation" \
    R075O_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq 132
test "$ruby_mutations" -eq 132

if env R075O_MUTATION=unknown_mutation \
  R075O_JSON="$TMP_ROOT/unknown-python.json" R075O_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075O_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075O_JSON="$CERT" R075O_RUBY_MUTATION=unknown_mutation \
  R075O_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075O_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075O_JSON="$CERT" R075O_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
report_source_hash=$(digest "$REPORT_SOURCE")
e_source_hash=$(digest "$E_SOURCE")
g_source_hash=$(digest "$G_SOURCE")
m_source_hash=$(digest "$M_SOURCE")
n_source_hash=$(digest "$N_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75O certificate QA report' ''
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
  printf '%s\n' "| research/r075o_vertical_diffusion_packet_gain.md | $main_hash |"
  printf '%s\n' "| research/r075o_vertical_diffusion_packet_gain_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075o_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075o_vertical_diffusion_packet_gain_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075o_vertical_diffusion_packet_gain_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075o_vertical_diffusion_packet_gain_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075o_vertical_diffusion_packet_gain_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075o_vertical_diffusion_packet_gain_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075o_vertical_diffusion_packet_gain_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075o_vertical_diffusion_packet_gain_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075o_vertical_diffusion_packet_gain_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit is byte-bound and checked for PASS/0. By its explicit'
  printf '%s\n' 'design it delegates the final main SHA binding to this certificate.'
  printf '%s\n' 'The report-source is byte-bound; literature completeness is outside this finite suite.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_source_hash |"
  printf '%s\n' "| research/r075g_signed_flux_gain_threshold.md | $g_source_hash |"
  printf '%s\n' "| research/r075m_dyadic_packet_diffusive_flux_gain.md | $m_source_hash |"
  printf '%s\n' "| research/r075n_radial_collar_averaged_wiener_row.md | $n_source_hash |"
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- O.9 difference index, sign, 2*pi pairing, outer pi*B, and d_0 cancellation: PASS.'
  printf '%s\n' '- Arbitrary vertical-frequency heat contraction and Schur row/column bounds: PASS.'
  printf '%s\n' '- Horizontal Parseval and exact energy coefficient 1/4: PASS.'
  printf '%s\n' '- Total-frequency cap, K^2*T>=1, T^2 Holder, and O.17 constants: PASS.'
  printf '%s\n' '- (16*pi)^(2/3)/4=(2*pi)^(2/3) and no vertical cardinality loss: PASS.'
  printf '%s\n' '- Normalization R^(1/3)omega^(1/3)K^(-2/3)p^(2/3): PASS.'
  printf '%s\n' '- Strict kappa*=98605/71442 and frozen exponent -4279/238140000: PASS.'
  printf '%s\n' '- O.1--O.24, references, 24/24 displays, four dependencies, and control bytes: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'O.1 allows arbitrary vertical frequencies only for the quadratic-energy row.'
  printf '%s\n' 'The cubic conversion retains a total-frequency cap and K^2*T>=1.'
  printf '%s\n' 'O.24 controls one packet against its own full-T^2 atom, not Version-M.'
  printf '%s\n' 'Collar localization, nonconstant shear, inter-packet and low-difference control,'
  printf '%s\n' 'cap removal, E.24, complete clock, fixed deletion, suitable-weak transfer,'
  printf '%s\n' 'regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075o-vertical-diffusion-packet-gain","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
