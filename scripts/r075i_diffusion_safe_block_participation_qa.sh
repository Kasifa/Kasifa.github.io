#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075i_diffusion_safe_block_participation_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075i_diffusion_safe_block_participation_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075i_diffusion_safe_block_participation_qa.sh"
FIXTURES="$ROOT/scripts/r075i_diffusion_safe_block_participation_fixtures.json"
EXPECTED="$ROOT/scripts/r075i_diffusion_safe_block_participation_expected.json"
MAIN="$ROOT/research/r075i_diffusion_safe_block_participation.md"
PRIMARY_AUDIT="$ROOT/research/r075i_diffusion_safe_block_participation_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075i_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
C_SOURCE="$ROOT/research/r075c_background_shear_packing_false_positive.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
G_SOURCE="$ROOT/research/r075g_signed_flux_gain_threshold.md"
H_SOURCE="$ROOT/research/r075h_single_pass_transport_flux_closure.md"
CERT="$ROOT/research/r075i_diffusion_safe_block_participation_certificate.json"
REPORT="$ROOT/research/r075i_diffusion_safe_block_participation_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075i_diffusion_safe_block_participation_independent_audit.md"
QA_REPORT="$ROOT/research/r075i_diffusion_safe_block_participation_qa_report.md"

EXPECTED_MAIN_HASH=c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7
EXPECTED_PRIMARY_AUDIT_HASH=a8e481bfa28ba244a6022b782880ce9a86c40de29e3b0064474841eca99cecbd
EXPECTED_REPORT_SOURCE_HASH=8459adb6735caa2ee6c6e9c27202125cda34ad9072e2d78167f3f961e34f5de3
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_C_HASH=1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_G_HASH=f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41
EXPECTED_H_HASH=849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9
EXPECTED_FIXTURES_HASH=afda306afcf26640be72978b654a1a7dd1b23c0df5e92137f450520a6c7d515b
EXPECTED_EXPECTED_HASH=27514a38beec5c5e949a2a639faa5db539a4fbdeefec175e9e6e90a0507afd2a

TMP_ROOT=$(mktemp -d /tmp/r075i-certificate-qa.XXXXXX)
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
test "$(digest "$G_SOURCE")" = "$EXPECTED_G_HASH"
test "$(digest "$H_SOURCE")" = "$EXPECTED_H_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.' "$PRIMARY_AUDIT"
grep -q 'Equation tags I.1--I.27 are unique and consecutive.' "$PRIMARY_AUDIT"
grep -q 'All 27 display-math environments are paired.' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075I_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075I_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 18' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"nEff": "125/81"' "$CERT"
grep -q '"fluxPerBlock": "0"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075I_JSON="$CERT" R075I_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":24' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 24/24' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift dependency_table_missing fixture_drift expected_drift tag reference display control block_time_r support_l support_r cylinder_measure b_r cutoff_r pointwise_coefficient measure_third_l measure_third_r cubic_r cubic_omega cubic_p normalization_r normalization_omega final_l holder_cell_measure holder_l2_power holder_l3_power holder_direction cubic_atom_r cubic_atom_omega transport_half one_block_direction participation_power neff_numerator neff_denominator neff_zero neff_lower_direction neff_upper_direction aggregation_identity unequal_as_count equal_mass_count aggregate_positive_part aggregate_absolute_sum aggregate_direction payment_pa_direction payment_pf_direction payment_power payment_upper_use rho_sign cgamma_sign theta_ratio theta_offset theta_strict beta_complement beta_strict one_rate_fraction uniform_theta uniform_rate_fraction endpoint_polynomial zero_mode_mean zero_mode_flux zero_mode_payment zero_mode_neff pde_required diffusion_unsafe participation_proved participation_necessary high_neff_counterexample uniform_counterexample signed_alternative_closed transition_closed recrossing_closed e24_closed complete_clock fixed_deletion suitable_weak regularity singularity novelty simulation_used clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 \
    R075I_MUTATION="$mutation" \
    R075I_JSON="$TMP_ROOT/python-$mutation.json" \
    R075I_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" \
    2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075I_JSON="$CERT" \
    R075I_RUBY_MUTATION="$mutation" \
    R075I_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" \
    2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq 83
test "$ruby_mutations" -eq 83

if env R075I_MUTATION=unknown_mutation \
  R075I_JSON="$TMP_ROOT/unknown-python.json" \
  R075I_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" \
  2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075I_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075I_JSON="$CERT" \
  R075I_RUBY_MUTATION=unknown_mutation \
  R075I_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" \
  2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075I_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-regenerate.stdout"
env R075I_JSON="$CERT" R075I_RUBY_REPORT="$RUBY_REPORT" \
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
g_source_hash=$(digest "$G_SOURCE")
h_source_hash=$(digest "$H_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75I certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Python assertions: 18/18'
  printf '%s\n' '- Ruby assertions: 24/24'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075i_diffusion_safe_block_participation.md | $main_hash |"
  printf '%s\n' "| research/r075i_diffusion_safe_block_participation_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075i_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075i_diffusion_safe_block_participation_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075i_diffusion_safe_block_participation_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075i_diffusion_safe_block_participation_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075i_diffusion_safe_block_participation_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075i_diffusion_safe_block_participation_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075i_diffusion_safe_block_participation_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075i_diffusion_safe_block_participation_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075i_diffusion_safe_block_participation_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit is bound to the final main SHA and checked for PASS/0,'
  printf '%s\n' 'I.1--I.27, and the corrected 27/27 display count. The report-source is'
  printf '%s\n' 'byte-bound only; its literature search is outside this finite certificate.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075b_bulk_clock_outer_padding_gate.md | $b_source_hash |"
  printf '%s\n' "| research/r075c_background_shear_packing_false_positive.md | $c_source_hash |"
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_source_hash |"
  printf '%s\n' "| research/r075g_signed_flux_gain_threshold.md | $g_source_hash |"
  printf '%s\n' "| research/r075h_single_pass_transport_flux_closure.md | $h_source_hash |"
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- I.5--I.13 intermediate and final R/L/omega/p powers: PASS.'
  printf '%s\n' '- Nonconstant rational one-block Holder and strict payment margins: PASS.'
  printf '%s\n' '- Perfect-cube participation cases, exact identity, and 1 <= N_eff <= N: PASS.'
  printf '%s\n' '- Unequal atoms [1,8] give N_eff=125/81 exactly: PASS.'
  printf '%s\n' '- Signed positive-part triangle inequality and Version-M upper-payment direction: PASS.'
  printf '%s\n' '- theta*=8558/35721, beta*=27163/35721, both endpoint strictness checks: PASS.'
  printf '%s\n' '- Rates -4279/238140000 and 27163/476280000, with below/above signs: PASS.'
  printf '%s\n' '- I.27 zero mode: equal positive p_j, N_eff=N=4, and every block flux zero: PASS.'
  printf '%s\n' '- Tags I.1--I.27, references, 27/27 displays, and control bytes: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The one-block estimate uses no PDE and is diffusion-safe, but it does not'
  printf '%s\n' 'prove a participation bound. I.19 is sufficient only; high N_eff is not'
  printf '%s\n' 'a necessary obstruction or an E.24 counterexample. Signed cancellation,'
  printf '%s\n' 'transition bands, recrossing, E.24, complete clock, fixed deletion,'
  printf '%s\n' 'suitable-weak transfer, regularity, and singularity remain OPEN.'
  printf '%s\n' '**NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075i-diffusion-safe-block-participation","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
