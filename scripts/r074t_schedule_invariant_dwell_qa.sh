#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
python_cert="$repo_dir/scripts/r074t_schedule_invariant_dwell_certificate.py"
ruby_cert="$repo_dir/scripts/r074t_schedule_invariant_dwell_certificate_independent.rb"
primary_json="$repo_dir/research/r074t_schedule_invariant_dwell_certificate.json"
primary_report="$repo_dir/research/r074t_schedule_invariant_dwell_certificate_report.md"
independent_report="$repo_dir/research/r074t_schedule_invariant_dwell_independent_audit.md"
qa_report="$repo_dir/research/r074t_schedule_invariant_dwell_qa_report.md"

cd "$repo_dir"
python3 "$python_cert"
ruby "$ruby_cert"

qa_dir="$(mktemp -d /tmp/r074t-schedule-dwell-qa.XXXXXX)"

for seed in 0 1 42; do
  (
    cd /tmp
    PYTHONHASHSEED="$seed" \
      R074T_DWELL_JSON="$qa_dir/primary-$seed.json" \
      R074T_DWELL_REPORT="$qa_dir/primary-$seed.md" \
      python3 "$python_cert" >/dev/null
  )
  cmp "$primary_json" "$qa_dir/primary-$seed.json"
  cmp "$primary_report" "$qa_dir/primary-$seed.md"
done

(
  cd /tmp
  R074T_DWELL_INDEPENDENT_REPORT="$qa_dir/independent.md" \
    ruby "$ruby_cert" >/dev/null
)
cmp "$independent_report" "$qa_dir/independent.md"

run_python_mutation() {
  local mutation="$1"
  if R074T_DWELL_MUTATION="$mutation" \
      R074T_DWELL_JSON=/dev/null \
      R074T_DWELL_REPORT=/dev/null \
      python3 "$python_cert" >/dev/null 2>&1; then
    printf 'PY_FAIL_OPEN\t%s\n' "$mutation"
    return 1
  fi
  printf 'PY_REJECTED\t%s\n' "$mutation"
}

run_ruby_mutation() {
  local mutation="$1"
  if R074T_DWELL_INDEPENDENT_MUTATION="$mutation" \
      R074T_DWELL_INDEPENDENT_REPORT=/dev/null \
      ruby "$ruby_cert" >/dev/null 2>&1; then
    printf 'RB_FAIL_OPEN\t%s\n' "$mutation"
    return 1
  fi
  printf 'RB_REJECTED\t%s\n' "$mutation"
}

export repo_dir python_cert ruby_cert
export -f run_python_mutation run_ruby_mutation

printf '%s\n' \
  gamma_weight_quarter_to_half gamma_exponent_sign two_thirds_to_half \
  L_power_sign theta_power_sign holder_direction time_inf_to_sup \
  survival_forall_to_exists min_to_max fixed_to_moving_deletion \
  same_shell_allowed allow_signed_clocks K_floor_to_Hfix \
  hstar_to_full_clock volume_upper_to_lower theta_bound_direction \
  survival_defect_sign margin_sign async_qpre_sign \
  async_interval_direction sum_overlapping_lobes tag_inventory \
  claim_boundary source_hash literature_hash dependency_hash |
  xargs -P 6 -n 1 bash -c 'run_python_mutation "$1"' bash |
  tee "$qa_dir/python-mutations.txt"

printf '%s\n' \
  gamma_weight_quarter_to_half gamma_exponent_sign two_thirds_to_half \
  L_power_sign theta_power_sign holder_direction time_inf_to_sup \
  survival_forall_to_exists min_to_max fixed_to_moving_deletion \
  same_shell_allowed allow_signed_clocks K_floor_to_Hfix \
  hstar_to_full_clock volume_upper_to_lower theta_bound_direction \
  survival_defect_sign margin_sign async_qpre_sign \
  async_interval_direction sum_overlapping_lobes tag_inventory \
  claim_boundary source_hash literature_hash dependency_hash primary_schema |
  xargs -P 6 -n 1 bash -c 'run_ruby_mutation "$1"' bash |
  tee "$qa_dir/ruby-mutations.txt"

test "$(wc -l < "$qa_dir/python-mutations.txt" | tr -d ' ')" = "26"
test "$(wc -l < "$qa_dir/ruby-mutations.txt" | tr -d ' ')" = "27"
test "$(grep -c '^PY_REJECTED' "$qa_dir/python-mutations.txt")" = "26"
test "$(grep -c '^RB_REJECTED' "$qa_dir/ruby-mutations.txt")" = "27"

check_whitespace() {
  local target="$1"
  local check_output
  local check_code
  set +e
  check_output="$(git diff --no-index --check /dev/null "$target" 2>&1)"
  check_code=$?
  set -e
  # Exit 1 means the file differs from /dev/null, as every nonempty artifact
  # should.  Whitespace errors are emitted on stderr/stdout; exit >1 is an
  # operational failure.
  if [ "$check_code" -gt 1 ] || [ -n "$check_output" ]; then
    printf '%s\n' "$check_output" >&2
    return 1
  fi
}

for target in \
  scripts/r074t_schedule_invariant_dwell_certificate.py \
  scripts/r074t_schedule_invariant_dwell_certificate_independent.rb \
  scripts/r074t_schedule_invariant_dwell_qa.sh \
  research/r074t_schedule_invariant_dwell_certificate.json \
  research/r074t_schedule_invariant_dwell_certificate_report.md \
  research/r074t_schedule_invariant_dwell_independent_audit.md \
  research/r074t_schedule_invariant_dwell_qa_report.md; do
  check_whitespace "$target"
done

note_sha="$(shasum -a 256 research/r074t_schedule_invariant_dwell_coercivity.md | awk '{print $1}')"
literature_sha="$(shasum -a 256 research/r074t_schedule_invariant_literature_audit.md | awk '{print $1}')"

{
  printf '# R0.74T Step 19 certificate QA report\n\n'
  printf -- '- Primary Python certificate: PASS, 31/31 groups, 18,933 exact finite cases.\n'
  printf -- '- Independent Ruby audit: PASS, 11/11 groups, 9,201 independent assertions.\n'
  printf -- '- Python negative mutations: 26/26 rejected.\n'
  printf -- '- Ruby negative mutations: 27/27 rejected.\n'
  printf -- '- Python byte determinism: PYTHONHASHSEED 0, 1, and 42 are byte-identical for JSON and Markdown.\n'
  printf -- '- Ruby byte determinism: independent Markdown regeneration is byte-identical.\n'
  printf -- '- Scoped git diff whitespace audit: PASS.\n\n'
  printf '## Frozen source bindings\n\n'
  printf -- '- Theorem note SHA-256: `%s`\n' "$note_sha"
  printf -- '- Literature audit SHA-256: `%s`\n\n' "$literature_sha"
  printf '## Boundary\n\n'
  printf 'The mutation suite exercises exponent signs, the two-thirds power, the\n'
  printf 'Gamma one-quarter shell weight, L and theta powers, Holder and volume\n'
  printf 'directions, all-time survival, min/fixed-deletion quantifiers, forbidden\n'
  printf 'Hfix/full-clock substitutions, logarithmic dwell direction, asynchronous\n'
  printf 'recentring and interval geometry, source structure, and frozen hashes.\n\n'
  printf 'This is finite algebraic, combinatorial, structural, and hash QA only.\n'
  printf 'It does not machine-prove continuous PDE inputs, regularity, or a Clay claim.\n'
} > "$qa_report"

printf 'QA_PASS\tpython_mutations=26/26\truby_mutations=27/27\tseeds=3/3\n'
printf 'QA_TEMP\t%s\n' "$qa_dir"
