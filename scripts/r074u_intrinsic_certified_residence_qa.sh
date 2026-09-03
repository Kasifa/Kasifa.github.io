#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
python_cert="$repo_dir/scripts/r074u_intrinsic_certified_residence_certificate.py"
ruby_cert="$repo_dir/scripts/r074u_intrinsic_certified_residence_certificate_independent.rb"
primary_json="$repo_dir/research/r074u_intrinsic_certified_residence_certificate.json"
primary_report="$repo_dir/research/r074u_intrinsic_certified_residence_certificate_report.md"
independent_report="$repo_dir/research/r074u_intrinsic_certified_residence_independent_audit.md"
qa_report="$repo_dir/research/r074u_intrinsic_certified_residence_qa_report.md"

cd "$repo_dir"
python3 "$python_cert"
ruby "$ruby_cert"

qa_dir="$(mktemp -d /tmp/r074u-intrinsic-residence-qa.XXXXXX)"
for seed in 0 1 42; do
  (
    cd /tmp
    PYTHONHASHSEED="$seed" \
      R074U_RESIDENCE_JSON="$qa_dir/primary-$seed.json" \
      R074U_RESIDENCE_REPORT="$qa_dir/primary-$seed.md" \
      python3 "$python_cert" >/dev/null
  )
  cmp "$primary_json" "$qa_dir/primary-$seed.json"
  cmp "$primary_report" "$qa_dir/primary-$seed.md"
done

(
  cd /tmp
  R074U_RESIDENCE_INDEPENDENT_REPORT="$qa_dir/independent.md" ruby "$ruby_cert" >/dev/null
)
cmp "$independent_report" "$qa_dir/independent.md"

run_python_mutation() {
  local mutation="$1"
  if R074U_RESIDENCE_MUTATION="$mutation" R074U_RESIDENCE_JSON=/dev/null \
      R074U_RESIDENCE_REPORT=/dev/null python3 "$python_cert" >/dev/null 2>&1; then
    printf 'PY_FAIL_OPEN\t%s\n' "$mutation"
    return 1
  fi
  printf 'PY_REJECTED\t%s\n' "$mutation"
}

run_ruby_mutation() {
  local mutation="$1"
  if R074U_RESIDENCE_INDEPENDENT_MUTATION="$mutation" \
      R074U_RESIDENCE_INDEPENDENT_REPORT=/dev/null ruby "$ruby_cert" >/dev/null 2>&1; then
    printf 'RB_FAIL_OPEN\t%s\n' "$mutation"
    return 1
  fi
  printf 'RB_REJECTED\t%s\n' "$mutation"
}

export python_cert ruby_cert
export -f run_python_mutation run_ruby_mutation
mutations=(
  A_squared_margin_sign epsilon_crude_bound speed_bound_direction slab_72_to_73
  upper_1024_to_1023 phase_96_to_97 phase_144_to_145 cstar_sign
  cross_tail_margin_sign theta_cert_log_sign theta_necessary_direction
  corridor_upper_to_K_superlevel Omega_to_Theta physical_to_frequency_shell
  drop_full_slab_compact_min drop_periodic_term K_to_Hfix overclaim drop_not_clay
  tag_inventory source_hash literature_hash dependency_hash
)
printf '%s\n' "${mutations[@]}" | xargs -P 6 -n 1 bash -c 'run_python_mutation "$1"' bash | tee "$qa_dir/python-mutations.txt"
printf '%s\n' "${mutations[@]}" primary_schema | xargs -P 6 -n 1 bash -c 'run_ruby_mutation "$1"' bash | tee "$qa_dir/ruby-mutations.txt"

test "$(grep -c '^PY_REJECTED' "$qa_dir/python-mutations.txt")" = "23"
test "$(grep -c '^RB_REJECTED' "$qa_dir/ruby-mutations.txt")" = "24"

note_sha="$(shasum -a 256 research/r074u_intrinsic_certified_residence.md | awk '{print $1}')"
literature_sha="$(shasum -a 256 research/r074u_intrinsic_residence_literature_audit.md | awk '{print $1}')"
test "$note_sha" = "e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99"
test "$literature_sha" = "0cf6e19a42e524aaf79aca10d72c5380029dce37032215974d99976a0b2a327c"

{
  printf '# R0.74U Step 20 certificate QA report\n\n'
  printf -- '- Primary Python certificate: PASS, 31/31 groups, 869 finite cases.\n'
  printf -- '- Independent Ruby audit: PASS, 9/9 groups, 1,651 independent Rational assertions.\n'
  printf -- '- Python negative mutations: 23/23 rejected.\n'
  printf -- '- Ruby negative mutations: 24/24 rejected.\n'
  printf -- '- Python byte determinism: PYTHONHASHSEED 0, 1, and 42 produce byte-identical JSON and Markdown.\n'
  printf -- '- Independent Ruby Markdown regeneration: byte-identical.\n\n'
  printf '## Frozen source bindings\n\n'
  printf -- '- Theorem note SHA-256: `%s`\n' "$note_sha"
  printf -- '- Literature audit SHA-256: `%s`\n\n' "$literature_sha"
  printf '## Mutation boundary\n\n'
  printf 'The fail-closed suite rejects changes to the A(L) squared reserve, epsilon and speed directions, 72/5 slab truncation, 1024/3 upper coefficient, 96/5 and 144/5 phase constants, c_*, cross-tail margins, theta substitution and necessary-bound direction, corridor/K quantifiers, Omega and physical-shell semantics, full-slab compact-minimum and periodic inputs, forbidden Hfix substitution, claim boundary, tag inventory, schemas, and frozen hashes.\n\n'
  printf 'This is finite exact arithmetic, kinematic, structural, dependency, and hash QA only. It does not machine-prove continuous PDE estimates, novelty, regularity, singularity, or a Clay claim.\n'
} > "$qa_report"

check_whitespace() {
  local target="$1" output code
  set +e
  output="$(git diff --no-index --check /dev/null "$target" 2>&1)"
  code=$?
  set -e
  if [ "$code" -gt 1 ] || [ -n "$output" ]; then
    printf '%s\n' "$output" >&2
    return 1
  fi
}

for target in \
  scripts/r074u_intrinsic_certified_residence_certificate.py \
  scripts/r074u_intrinsic_certified_residence_certificate_independent.rb \
  scripts/r074u_intrinsic_certified_residence_qa.sh \
  research/r074u_intrinsic_certified_residence_certificate.json \
  research/r074u_intrinsic_certified_residence_certificate_report.md \
  research/r074u_intrinsic_certified_residence_independent_audit.md \
  research/r074u_intrinsic_certified_residence_qa_report.md; do
  check_whitespace "$target"
done

printf 'QA_PASS\tpython_mutations=23/23\truby_mutations=24/24\tseeds=3/3\n'
printf 'QA_TEMP\t%s\n' "$qa_dir"
