#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075k_positive_majorant_high_frequency_trace_loss_qa.sh"
FIXTURES="$ROOT/scripts/r075k_positive_majorant_high_frequency_trace_loss_fixtures.json"
EXPECTED="$ROOT/scripts/r075k_positive_majorant_high_frequency_trace_loss_expected.json"
MAIN="$ROOT/research/r075k_positive_majorant_high_frequency_trace_loss.md"
PRIMARY_AUDIT="$ROOT/research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md"
REPORT_SOURCE="$ROOT/research/r075k_report-source.md"
E_SOURCE="$ROOT/research/r075e_horizontal_cross_mode_flux_reduction.md"
I_SOURCE="$ROOT/research/r075i_diffusion_safe_block_participation.md"
J_SOURCE="$ROOT/research/r075j_mean_zero_adjoint_flux_obstruction.md"
CERT="$ROOT/research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json"
REPORT="$ROOT/research/r075k_positive_majorant_high_frequency_trace_loss_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075k_positive_majorant_high_frequency_trace_loss_independent_audit.md"
QA_REPORT="$ROOT/research/r075k_positive_majorant_high_frequency_trace_loss_qa_report.md"

EXPECTED_MAIN_HASH=9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf
EXPECTED_PRIMARY_AUDIT_HASH=401f12d9a5f35646638ae08446a1177a0b0485b9bbb54206702dee9fc7e7a4a2
EXPECTED_REPORT_SOURCE_HASH=5a45521ecb5e85b69b077af9d4db3cbb1c52dc1b61cccf8fb3bbb9daabac7001
EXPECTED_E_HASH=99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049
EXPECTED_I_HASH=c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7
EXPECTED_J_HASH=960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d
EXPECTED_FIXTURES_HASH=f15df9bf59d6a96151f84ae2fa11a12b3965820450fbad526d4f71f11a6f7328
EXPECTED_EXPECTED_HASH=5ad1107080ccf033e842521e8f985196357d6cb858f945b007a5df50c2a12d77

TMP_ROOT=$(mktemp -d /tmp/r075k-certificate-qa.XXXXXX)
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
test "$(digest "$I_SOURCE")" = "$EXPECTED_I_HASH"
test "$(digest "$J_SOURCE")" = "$EXPECTED_J_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q "$EXPECTED_MAIN_HASH" "$PRIMARY_AUDIT"
grep -q 'Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.' "$PRIMARY_AUDIT"
grep -q 'Equation tags K.1--K.18 are unique and consecutive.' "$PRIMARY_AUDIT"
grep -q 'All 18 display-math environments are paired.' "$PRIMARY_AUDIT"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075K_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075K_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 19' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"spatialMassSymbol": "2\*pi\*T"' "$CERT"
grep -q '"ratioCubeNormalized": "50625/64"' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075K_JSON="$CERT" R075K_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":21' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 21/21' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift dependency_table_missing fixture_drift expected_drift tag reference display control forward_time_sign forward_drift_sign forward_diffusion_sign adjoint_time_sign adjoint_drift_sign adjoint_diffusion_sign constant_shear q_constant q_cosine a_cosine q_majorant_direction q_nonnegative q_modes a_modes time_reversal semigroup_drift_sign semigroup_diffusion_sign semigroup_source_sign phi_terminal phi_nonnegative phi_modes phi_mass_sign phi_mass_factor phi_mass_endpoint decay_sign phase_direction time_decay time_phase drift_phase laplacian_sign passive_residual k_integer k_lower square_frequency square_zero_coefficient square_side_coefficient entrance_half orthogonality boundary_k_dependence cos_quarter cos_symmetry cos_integral mass_decay_three mass_k_square mass_amplitude mass_upper_direction exponential_range mass_exact_factor boundary_A mass_A mass_k two_thirds ratio_A ratio_k amplitude_cancel ratio_growth ratio_constant signed_source_frequency signed_field_frequency signed_mode_match signed_flux_nonzero signed_integer_quantifier physical_flux_absolute W_limit_order W_continuous W_nonnegative W_integral W_depends_k W_frequency riemann_lebesgue W_boundary_limit local_atom_not_alone e24_counterexample all_majorants_ruled fdependent_ruled signed_kernel_ruled full_versionm_ruled trace_atom_ruled nse_solution transition_closed periodic_closed complete_clock fixed_deletion suitable_weak regularity singularity novelty simulation_used clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 \
    R075K_MUTATION="$mutation" \
    R075K_JSON="$TMP_ROOT/python-$mutation.json" \
    R075K_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" \
    2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075K_JSON="$CERT" \
    R075K_RUBY_MUTATION="$mutation" \
    R075K_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" \
    2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations=$((ruby_mutations + 1))
done
test "$python_mutations" -eq 100
test "$ruby_mutations" -eq 100

if env R075K_MUTATION=unknown_mutation \
  R075K_JSON="$TMP_ROOT/unknown-python.json" \
  R075K_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" \
  >"$TMP_ROOT/unknown-python.stdout" \
  2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075K_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075K_JSON="$CERT" \
  R075K_RUBY_MUTATION=unknown_mutation \
  R075K_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" \
  2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075K_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075K_JSON="$CERT" R075K_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_audit_hash=$(digest "$PRIMARY_AUDIT")
report_source_hash=$(digest "$REPORT_SOURCE")
e_source_hash=$(digest "$E_SOURCE")
i_source_hash=$(digest "$I_SOURCE")
j_source_hash=$(digest "$J_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75K certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 19/19'
  printf '%s\n' '- Ruby assertions: 21/21'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075k_positive_majorant_high_frequency_trace_loss.md | $main_hash |"
  printf '%s\n' "| research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md | $primary_audit_hash |"
  printf '%s\n' "| research/r075k_report-source.md | $report_source_hash |"
  printf '%s\n' "| scripts/r075k_positive_majorant_high_frequency_trace_loss_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075k_positive_majorant_high_frequency_trace_loss_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075k_positive_majorant_high_frequency_trace_loss_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075k_positive_majorant_high_frequency_trace_loss_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075k_positive_majorant_high_frequency_trace_loss_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit is checked against the frozen main SHA, PASS/0,'
  printf '%s\n' 'K.1--K.18, and 18/18 displays. The report-source is byte-bound only;'
  printf '%s\n' 'its literature search and access record are outside this finite certificate.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075e_horizontal_cross_mode_flux_reduction.md | $e_source_hash |"
  printf '%s\n' "| research/r075i_diffusion_safe_block_participation.md | $i_source_hash |"
  printf '%s\n' "| research/r075j_mean_zero_adjoint_flux_obstruction.md | $j_source_hash |"
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- L/L* time, drift, and diffusion signs: PASS.'
  printf '%s\n' '- q=1+cos(x)>=cos(x), q>=0, positive reversed semigroup, and zero terminal data: PASS.'
  printf '%s\n' '- Phi(0) has only modes 0,+/-1 and spatial mass 2*pi*T: PASS.'
  printf '%s\n' '- LF_k=0 and F_k(0)^2 has only modes 0,+/-2k: PASS.'
  printf '%s\n' '- B_k/pi=A^2*T/2 for k=1,2,5 and every integer-k signed flux is zero: PASS.'
  printf '%s\n' '- Integral |cos(kx)|^3=8/3 and M_k=8A^3(1-exp(-3k^2T))/(9k^2): PASS.'
  printf '%s\n' '- A cancels and the boundary/payment ratio grows as k^(4/3): PASS.'
  printf '%s\n' '- Fixed-W-first quantifier and Riemann--Lebesgue boundary: PASS.'
  printf '%s\n' '- Tags K.1--K.18, references, 18/18 displays, and control bytes: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'The no-go is limited to a fixed nonnegative entrance weight combined with'
  printf '%s\n' 'the local spacetime cubic atom alone. It does not refute E.24, adaptive or'
  printf '%s\n' 'signed majorants, or the full Version-M ledger. Transition/periodic geometry,'
  printf '%s\n' 'complete clock, fixed deletion, suitable-weak transfer, regularity, and'
  printf '%s\n' 'singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075k-positive-majorant-high-frequency-trace-loss","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
