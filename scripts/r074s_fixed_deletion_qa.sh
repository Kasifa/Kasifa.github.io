#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
python_cert="$repo_dir/scripts/r074s_fixed_deletion_certificate.py"
ruby_cert="$repo_dir/scripts/r074s_fixed_deletion_certificate_independent.rb"
primary_json="$repo_dir/research/r074s_fixed_deletion_certificate.json"
primary_report="$repo_dir/research/r074s_fixed_deletion_certificate_report.md"
independent_report="$repo_dir/research/r074s_fixed_deletion_independent_audit.md"

cd "$repo_dir"
python3 "$python_cert"
ruby "$ruby_cert"

qa_dir="$(mktemp -d /tmp/r074s-fixed-deletion-qa.XXXXXX)"

for seed in 0 1 42; do
  (
    cd /tmp
    PYTHONHASHSEED="$seed" \
      R074S_FIXED_DELETION_JSON="$qa_dir/primary-$seed.json" \
      R074S_FIXED_DELETION_REPORT="$qa_dir/primary-$seed.md" \
      python3 "$python_cert" >/dev/null
  )
  cmp "$primary_json" "$qa_dir/primary-$seed.json"
  cmp "$primary_report" "$qa_dir/primary-$seed.md"
done

(
  cd /tmp
  R074S_FIXED_DELETION_INDEPENDENT_REPORT="$qa_dir/independent.md" \
    ruby "$ruby_cert" >/dev/null
)
cmp "$independent_report" "$qa_dir/independent.md"

run_python_mutation() {
  local mutation="$1"
  if R074S_FIXED_DELETION_MUTATION="$mutation" \
      R074S_FIXED_DELETION_JSON=/dev/null \
      R074S_FIXED_DELETION_REPORT=/dev/null \
      python3 "$python_cert" >/dev/null 2>&1; then
    printf 'PY_FAIL_OPEN\t%s\n' "$mutation"
    return 1
  fi
  printf 'PY_REJECTED\t%s\n' "$mutation"
}

run_ruby_mutation() {
  local mutation="$1"
  if R074S_FIXED_DELETION_INDEPENDENT_MUTATION="$mutation" \
      R074S_FIXED_DELETION_INDEPENDENT_REPORT=/dev/null \
      ruby "$ruby_cert" >/dev/null 2>&1; then
    printf 'RB_FAIL_OPEN\t%s\n' "$mutation"
    return 1
  fi
  printf 'RB_REJECTED\t%s\n' "$mutation"
}

export repo_dir python_cert ruby_cert
export -f run_python_mutation run_ruby_mutation

printf '%s\n' \
  minimax_order layer_cake q_payment reverse_six triangle_fixed \
  triangle_separable ledger_power tag_inventory claim_boundary \
  source_hash literature_hash dependency_hash |
  xargs -P 6 -n 1 bash -c 'run_python_mutation "$1"' bash

printf '%s\n' \
  minimax_order layer_cake q_payment reverse_six triangle_fixed \
  triangle_separable ledger_power tag_inventory claim_boundary \
  source_hash literature_hash dependency_hash primary_schema |
  xargs -P 6 -n 1 bash -c 'run_ruby_mutation "$1"' bash

git diff --check

printf 'QA_PASS\tpython_mutations=12/12\truby_mutations=13/13\tseeds=3/3\n'
printf 'QA_TEMP\t%s\n' "$qa_dir"
