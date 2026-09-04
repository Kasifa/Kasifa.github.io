#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=python3
PY_SCRIPT="$ROOT/scripts/r075p_buffered_collar_entrance_concentration_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/r075p_buffered_collar_entrance_concentration_certificate_independent.rb"
QA_SCRIPT="$ROOT/scripts/r075p_buffered_collar_entrance_concentration_qa.sh"
FIXTURES="$ROOT/scripts/r075p_buffered_collar_entrance_concentration_fixtures.json"
EXPECTED="$ROOT/scripts/r075p_buffered_collar_entrance_concentration_expected.json"
MAIN="$ROOT/research/r075p_buffered_collar_entrance_concentration.md"
PRIMARY="$ROOT/research/r075p_buffered_collar_entrance_concentration_primary_audit.md"
SOURCE="$ROOT/research/r075p_report-source.md"
B_SOURCE="$ROOT/research/r075b_bulk_clock_outer_padding_gate.md"
I_SOURCE="$ROOT/research/r075i_diffusion_safe_block_participation.md"
N_SOURCE="$ROOT/research/r075n_radial_collar_averaged_wiener_row.md"
O_SOURCE="$ROOT/research/r075o_vertical_diffusion_packet_gain.md"
CERT="$ROOT/research/r075p_buffered_collar_entrance_concentration_certificate.json"
REPORT="$ROOT/research/r075p_buffered_collar_entrance_concentration_certificate_report.md"
RUBY_REPORT="$ROOT/research/r075p_buffered_collar_entrance_concentration_independent_audit.md"
QA_REPORT="$ROOT/research/r075p_buffered_collar_entrance_concentration_qa_report.md"

EXPECTED_MAIN_HASH=8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6
EXPECTED_PRIMARY_HASH=e065759a1df3c118f71dd47ac9b5ded9df40536217f557b3c1155e8bf64d3390
EXPECTED_SOURCE_HASH=fcde6bed847b0628aff7de90a49e8150e4a279fca8e46d7053943fdadf0478ca
EXPECTED_B_HASH=430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a
EXPECTED_I_HASH=c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7
EXPECTED_N_HASH=ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318
EXPECTED_O_HASH=3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9
EXPECTED_FIXTURES_HASH=9d9bf2a00fbdf58eb85a01a3f7fe931f289a5bc1166430dac1f704e4406ec6d7
EXPECTED_EXPECTED_HASH=cc472fb797c98d61e004c09fb84ba4a29029d72665f60507628c166134b39d31

TMP_ROOT=$(mktemp -d /tmp/r075p-certificate-qa.XXXXXX)
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
test "$(digest "$I_SOURCE")" = "$EXPECTED_I_HASH"
test "$(digest "$N_SOURCE")" = "$EXPECTED_N_HASH"
test "$(digest "$O_SOURCE")" = "$EXPECTED_O_HASH"
test "$(digest "$FIXTURES")" = "$EXPECTED_FIXTURES_HASH"
test "$(digest "$EXPECTED")" = "$EXPECTED_EXPECTED_HASH"

grep -q 'Verdict: \*\*PASS\*\*' "$PRIMARY"
grep -q 'Mathematical blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'Release blocker count: \*\*0\*\*' "$PRIMARY"
grep -q 'does not authorize publication' "$PRIMARY"

for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" \
    R075P_JSON="$TMP_ROOT/certificate-$seed.json" \
    R075P_REPORT="$TMP_ROOT/report-$seed.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-$seed.stdout"
done
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-1.md"
cmp "$TMP_ROOT/report-0.md" "$TMP_ROOT/report-42.md"

env PYTHONHASHSEED=0 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-canonical.stdout"
grep -q '"assertions": 21' "$TMP_ROOT/python-canonical.stdout"
grep -q '"verdict": "PASS"' "$CERT"
grep -q '"fibreLength": "1/2"' "$CERT"
grep -q '"tau": "1/196608"' "$CERT"
grep -q '"massLowerTimesSqrtPi": "1/86016"' "$CERT"
grep -q '"sigmaStar": "8558/178605"' "$CERT"
grep -q '"rateAtHalfThreshold": "-4279/476280000"' "$CERT"
grep -q '"packetToRowRatio": "18/125"' "$CERT"
grep -q '"projectionDominationValid": false' "$CERT"
cmp "$TMP_ROOT/certificate-0.json" "$CERT"
cmp "$TMP_ROOT/report-0.md" "$REPORT"

env R075P_JSON="$CERT" R075P_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-canonical.stdout"
grep -q '"verdict":"PASS"' "$TMP_ROOT/ruby-canonical.stdout"
grep -q '"assertions":22' "$TMP_ROOT/ruby-canonical.stdout"
grep -q 'Assertions: 22/22' "$RUBY_REPORT"

mutations='source_drift audit_drift report_source_drift dependency_drift fixture_drift expected_drift audit_status audit_blocker audit_authorization dependency_table_missing tag reference display control utf8 fibre_outer fibre_inner fibre_factor fibre_monotonicity fibre_safe_radius fibre_lower_only fibre_tangency central_chart cutoff_translation cutoff_transport_sign operator_drift operator_diffusion constant_shear local_identity_laplacian local_identity_gradient_sign gradient_cap gradient_four energy_eight r2_vs_k2 cap_preserved c0_energy tau_mu tau_k window_condition displacement_B displacement_R c0_displacement support_margin tau_inside persistence_direction persistence_half entrance_assumed holder_direction holder_volume holder_power fibre_to_cubic cubic_R_cancel time_mu cstar_sqrt2 cstar_pi cubic_a cubic_mu cubic_K cubic_E inverse_direction inverse_a inverse_mu inverse_K inverse_M no_backward flux_quarter wiener_a combine_a combine_mu combine_K combine_M positive_part payment_R payment_omega flux_R flux_omega normalized_R normalized_omega normalized_p B_scale K_scale coefficient_R coefficient_L rho cgamma rate_sign rate_sigma threshold_numerator threshold_denominator threshold_strict equality_allowed ledger_time ledger_space ledger_weight ledger_nonnegative ledger_direction actual_component same_velocity pointwise_domination projection_excluded arbitrary_zero_path realized_subclass p3p30_independent low_fraction low_not_counterexample localized_kernel_open formula_packet formula_cutoff formula_energy formula_holder formula_threshold formula_payment literature_identity literature_complete literature_import single_packet total_cap e24_open nonconstant_open interpacket_open lowdiff_open cap_open complete_clock_open fixed_deletion_open suitable_weak_open regularity_open singularity_open novelty priority simulation dns clay'

python_mutations=0
ruby_mutations=0
for mutation in $mutations; do
  if env PYTHONHASHSEED=0 R075P_MUTATION="$mutation" \
    R075P_JSON="$TMP_ROOT/python-$mutation.json" \
    R075P_REPORT="$TMP_ROOT/python-$mutation.md" \
    "$PYTHON_BIN" -B "$PY_SCRIPT" \
    >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q '"verdict": "FAIL"' "$TMP_ROOT/python-$mutation.json"
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/python-$mutation.md"
  python_mutations=$((python_mutations + 1))

  if env R075P_JSON="$CERT" R075P_RUBY_MUTATION="$mutation" \
    R075P_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
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

if env R075P_MUTATION=unknown_mutation \
  R075P_JSON="$TMP_ROOT/unknown-python.json" R075P_REPORT="$TMP_ROOT/unknown-python.md" \
  "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075P_MUTATION' "$TMP_ROOT/unknown-python.stderr"

if env R075P_JSON="$CERT" R075P_RUBY_MUTATION=unknown_mutation \
  R075P_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R075P_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=42 "$PYTHON_BIN" -B "$PY_SCRIPT" >"$TMP_ROOT/python-regenerate.stdout"
env R075P_JSON="$CERT" R075P_RUBY_REPORT="$RUBY_REPORT" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-regenerate.stdout"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"

main_hash=$(digest "$MAIN")
primary_hash=$(digest "$PRIMARY")
source_hash=$(digest "$SOURCE")
b_hash=$(digest "$B_SOURCE")
i_hash=$(digest "$I_SOURCE")
n_hash=$(digest "$N_SOURCE")
o_hash=$(digest "$O_SOURCE")
fixtures_hash=$(digest "$FIXTURES")
expected_hash=$(digest "$EXPECTED")
python_hash=$(digest "$PY_SCRIPT")
ruby_hash=$(digest "$RUBY_SCRIPT")
qa_hash=$(digest "$QA_SCRIPT")
cert_hash=$(digest "$CERT")
report_hash=$(digest "$REPORT")
ruby_report_hash=$(digest "$RUBY_REPORT")

{
  printf '%s\n' '# R0.75P certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Python assertions: 21/21'
  printf '%s\n' '- Ruby assertions: 22/22'
  printf '%s\n' "- Negative mutations rejected: $python_mutations/$python_mutations Python; $ruby_mutations/$ruby_mutations Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Canonical JSON and both generated reports are regeneration-stable: PASS'
  printf '%s\n' ''
  printf '%s\n' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075p_buffered_collar_entrance_concentration.md | $main_hash |"
  printf '%s\n' "| research/r075p_buffered_collar_entrance_concentration_primary_audit.md | $primary_hash |"
  printf '%s\n' "| research/r075p_report-source.md | $source_hash |"
  printf '%s\n' "| scripts/r075p_buffered_collar_entrance_concentration_fixtures.json | $fixtures_hash |"
  printf '%s\n' "| scripts/r075p_buffered_collar_entrance_concentration_expected.json | $expected_hash |"
  printf '%s\n' "| scripts/r075p_buffered_collar_entrance_concentration_certificate.py | $python_hash |"
  printf '%s\n' "| scripts/r075p_buffered_collar_entrance_concentration_certificate_independent.rb | $ruby_hash |"
  printf '%s\n' "| scripts/r075p_buffered_collar_entrance_concentration_qa.sh | $qa_hash |"
  printf '%s\n' "| research/r075p_buffered_collar_entrance_concentration_certificate.json | $cert_hash |"
  printf '%s\n' "| research/r075p_buffered_collar_entrance_concentration_certificate_report.md | $report_hash |"
  printf '%s\n' "| research/r075p_buffered_collar_entrance_concentration_independent_audit.md | $ruby_report_hash |"
  printf '%s\n' ''
  printf '%s\n' 'The primary audit and report-source are byte-bound. Literature completeness'
  printf '%s\n' 'is outside this finite suite; the bounded source screen is not novelty evidence.'
  printf '%s\n' ''
  printf '%s\n' '## Frozen dependency bindings' ''
  printf '%s\n' '| path | SHA-256 |'
  printf '%s\n' '|---|---|'
  printf '%s\n' "| research/r075b_bulk_clock_outer_padding_gate.md | $b_hash |"
  printf '%s\n' "| research/r075i_diffusion_safe_block_participation.md | $i_hash |"
  printf '%s\n' "| research/r075n_radial_collar_averaged_wiener_row.md | $n_hash |"
  printf '%s\n' "| research/r075o_vertical_diffusion_packet_gain.md | $o_hash |"
  printf '%s\n' ''
  printf '%s\n' '## Checks' ''
  printf '%s\n' '- P.10 exact fibre length, safe radius, and 4*delta0*R lower bound: PASS.'
  printf '%s\n' '- Moving-cutoff sign, local-energy identity, 4*K^2, 8+C_phi, tau, and displacement: PASS.'
  printf '%s\n' '- Holder volume, c*, mu^(5/2), inverse powers, and O+N combination: PASS.'
  printf '%s\n' '- R/omega normalization and strict sigma*=8558/178605: PASS.'
  printf '%s\n' '- P.1--P.31, references, 31/31 displays, four dependencies, and control bytes: PASS.'
  printf '%s\n' '- P.31 same-v_R actual-component realization and nonnegative ledger direction: PASS.'
  printf '%s\n' ''
  printf '%s\n' 'P.31 is only a conditional realized-subclass payment statement. Fourier/LP'
  printf '%s\n' 'projections and arbitrary zero-trajectory realization are excluded. P.3--P.30'
  printf '%s\n' 'do not use that realization hypothesis. Low concentration is not a counterexample;'
  printf '%s\n' 'the localized signed-kernel branch, E.24, complete clock, fixed deletion,'
  printf '%s\n' 'suitable-weak transfer, regularity, and singularity remain OPEN. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r075p-buffered-collar-entrance-concentration","status":"PASS","mutations":%s,"pythonHashSeeds":3}\n' "$python_mutations"
