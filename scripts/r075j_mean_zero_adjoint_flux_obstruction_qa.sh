#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075j_mean_zero_adjoint_flux_obstruction_qa.sh"
FIXTURES="$ROOT/scripts/r075j_mean_zero_adjoint_flux_obstruction_fixtures.json"
EXPECTED="$ROOT/scripts/r075j_mean_zero_adjoint_flux_obstruction_expected.json"
MAIN="$ROOT/research/r075j_mean_zero_adjoint_flux_obstruction.md"
PRIMARY_AUDIT="$ROOT/research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075j_report-source.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
F_SOURCE="$ROOT/research/r075f_modal_phase_integration_identity.md"
H_SOURCE="$ROOT/research/r075h_single_pass_transport_flux_closure.md"
I_SOURCE="$ROOT/research/r075i_diffusion_safe_block_participation.md"
CERT="$ROOT/research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json"
REPORT="$ROOT/research/r075j_mean_zero_adjoint_flux_obstruction_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075j_mean_zero_adjoint_flux_obstruction_independent_audit.md"
QA_REPORT="$ROOT/research/r075j_mean_zero_adjoint_flux_obstruction_qa_report.md"

EXPECTED_MAIN_HASH=960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d
EXPECTED_PRIMARY_AUDIT_HASH=f2de2d439d428ccd2885f7d3fc333496cb9753896c772a54df04622e4c52c76e
EXPECTED_REPORT_SOURCE_HASH=1d195b0bc6760a4458fd3b4f7d11c5c892ca259c88aa5de3b014b4986ad166ca
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_F_HASH=f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440
EXPECTED_H_HASH=849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9
EXPECTED_I_HASH=c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7
EXPECTED_FIXTURES_HASH=754d585bab0b194adaa3f945dc8b14950e3c078564f38dc63919cf733fcfea2c
EXPECTED_EXPECTED_HASH=6c32cd1ff38895c5e3b0a580ad9a5e789fc3d9d8e672ba6644dceeb29befe5b8

TMP_ROOT=$(mktemp -d /tmp/r075j-certificate-qa.XXXXXX)
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
test "$(digest "$F_SOURCE")" = "$EXPECTED_F_HASH"
test "$(digest "$H_SOURCE")" = "$EXPECTED_H_HASH"
test "$(digest "$I_SOURCE")" = "$EXPECTED_I_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.' "$PRIMARY_AUDIT"
grep -q 'Equation tags J.1--J.20 are unique and consecutive.' "$PRIMARY_AUDIT"
grep -q 'All 20 display-math environments are paired.' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075J_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075J_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 19' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"etaSamples"' "$CERT"
grep -q '"exactConstantSum": "0"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075J_JSON="$CERT" R075J_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":24' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 24/24' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift dependency_table_missing fixture_drift expected_drift tag reference display control forward_time_sign forward_drift_sign forward_diffusion_sign adjoint_time_sign adjoint_drift_sign adjoint_diffusion_sign drift_divergence square_diss_sign square_diss_factor derivative_source_abs derivative_source_positive source_b_x2 source_mean_quantifier positive_source_equal tau_direction A_sign B_sign b_sign terminal_nonzero adjoint_source_cos adjoint_source_sin eta_denominator eta_positive slice_sign sign_change_false j12_initial_sign j12_terminal_sign j12_bulk_sign j12_endpoint_swap j12_source_pairing j5_half j5_diss_sign j13_initial_sign j13_diss_sign j13_drop_negative_initial signed_decomposition energy_endpoint_sign energy_factor shift_initial_sign shift_terminal_sign shift_diss_sign constant_homogeneous exact_shift_nonzero surcharge_half surcharge_not_cd majorant_direction phi_nonnegative terminal_nonnegative majorant_half majorant_terminal_sign majorant_diss_sign majorant_source_direction favorable_terminal favorable_dissipation pde_backward exact_adjoint_nonnegative aplus_signed majorant_paid uncontrolled_dissipation_paid free_shift blanket_no_go feynman_kac_closed transition_closed periodic_closed e24_closed complete_clock fixed_deletion suitable_weak regularity singularity simulation_used novelty clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 \
    R075J_MUTATION="$mutation" \
    R075J_JSON="$TMP_ROOT/python-$mutation.json" \
    R075J_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" \
    2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075J_JSON="$CERT" \
    R075J_RUBY_MUTATION="$mutation" \
    R075J_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" \
    2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq 84
test "$ruby_mutations" -eq 84

if env R075J_MUTATION=unknown_mutation \
  R075J_JSON="$TMP_ROOT/unknown-python.json" \
  R075J_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" \
  2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075J_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075J_JSON="$CERT" \
  R075J_RUBY_MUTATION=unknown_mutation \
  R075J_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" \
  2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075J_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/python-regenerate.stdout"
env R075J_JSON="$CERT" R075J_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
report_source_hash=$(digest "$REPORT_SOURCE")
e_source_hash=$(digest "$E_SOURCE")
f_source_hash=$(digest "$F_SOURCE")
h_source_hash=$(digest "$H_SOURCE")
i_source_hash=$(digest "$I_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75J certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Python assertions: 19/19'
  printf '%s\n' '- Ruby assertions: 24/24'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075j_mean_zero_adjoint_flux_obstruction.md | $main_hash |"
  printf '%s\n' "| research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075j_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075j_mean_zero_adjoint_flux_obstruction_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075j_mean_zero_adjoint_flux_obstruction_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075j_mean_zero_adjoint_flux_obstruction_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075j_mean_zero_adjoint_flux_obstruction_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075j_mean_zero_adjoint_flux_obstruction_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit is checked against the frozen main SHA, PASS/0,'
  printf '%s\n' 'J.1--J.20, and 20/20 displays. The report-source is byte-bound only;'
  printf '%s\n' 'its literature search and access record are outside this finite certificate.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_source_hash |"
  printf '%s\n' "| research/r075f_modal_phase_integration_identity.md | $f_source_hash |"
  printf '%s\n' "| research/r075h_single_pass_transport_flux_closure.md | $h_source_hash |"
  printf '%s\n' "| research/r075i_diffusion_safe_block_participation.md | $i_source_hash |"
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- L/L* time, drift, diffusion, divergence, and passive-square signs: PASS.'
  printf '%s\n' '- Physical derivative source has zero mean for every fixed parameter slice: PASS.'
  printf '%s\n' '- Rational adjoint fixture gives (1+tau+2tau^2+tau^3)cos(x), zero terminal data, eta>0, and both slice signs: PASS.'
  printf '%s\n' '- J.12 endpoint/bulk signs and J.5/J.13 dissipation signs: PASS.'
  printf '%s\n' '- Constant shift cancels exactly; dropping dissipation costs CD: PASS.'
  printf '%s\n' '- Nonnegative majorant direction and both favorable rows: PASS.'
  printf '%s\n' '- a_+ and |a| are not the original signed mean-zero source: PASS.'
  printf '%s\n' '- Tags J.1--J.20, references, 20/20 displays, and control bytes: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The exact signed adjoint is sign-changing. A positive majorant remains a'
  printf '%s\n' 'viable architecture, but its initial row is unpaid. This is not a blanket'
  printf '%s\n' 'no-go for resolvent or Feynman--Kac methods. Transition geometry, periodic'
  printf '%s\n' 'recrossing, E.24, complete clock, fixed deletion, suitable-weak transfer,'
  printf '%s\n' 'regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075j-mean-zero-adjoint-flux-obstruction","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
