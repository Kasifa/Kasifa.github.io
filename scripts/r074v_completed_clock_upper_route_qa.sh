#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
py="$repo_dir/scripts/r074v_completed_clock_upper_route_certificate.py"
rb="$repo_dir/scripts/r074v_completed_clock_upper_route_certificate_independent.rb"
json="$repo_dir/research/r074v_completed_clock_upper_route_certificate.json"
report="$repo_dir/research/r074v_completed_clock_upper_route_certificate_report.md"
independent="$repo_dir/research/r074v_completed_clock_upper_route_independent_audit.md"
qa_report="$repo_dir/research/r074v_completed_clock_upper_route_qa_report.md"
cd "$repo_dir"
python3 "$py"; ruby "$rb"
qa_dir="$(mktemp -d /tmp/r074v-completed-clock-qa.XXXXXX)"
for seed in 0 1 42; do
  PYTHONHASHSEED="$seed" R074V_JSON="$qa_dir/$seed.json" R074V_REPORT="$qa_dir/$seed.md" python3 "$py" >/dev/null
  cmp "$json" "$qa_dir/$seed.json"; cmp "$report" "$qa_dir/$seed.md"
done
R074V_INDEPENDENT_REPORT="$qa_dir/independent.md" ruby "$rb" >/dev/null
cmp "$independent" "$qa_dir/independent.md"
run_py(){ if R074V_MUTATION="$1" R074V_JSON=/dev/null R074V_REPORT=/dev/null python3 "$py" >/dev/null 2>&1; then echo "PY_FAIL_OPEN $1"; return 1; else echo "PY_REJECTED $1"; fi; }
run_rb(){ if R074V_INDEPENDENT_MUTATION="$1" R074V_INDEPENDENT_REPORT=/dev/null ruby "$rb" >/dev/null 2>&1; then echo "RB_FAIL_OPEN $1"; return 1; else echo "RB_REJECTED $1"; fi; }
export py rb; export -f run_py run_rb
mutations=(d0_sign chi65_sign chi66_sign rho_margin_sign gamma_ratio_sign H_ratio_sign union_threshold remainder_threshold box_inner_failure box_outer_failure box_volume_failure v_R_minus_a K_upper_proved V64_common_shear_theorem drop_accumulated_dissipation AI_to_Aclk uniform_arbitrary_Astar drop_not_clay tag_inventory claim_sentinel source_hash primary_audit_hash dependency_hash torus_chord_cap volume_cap central_pairs_to_all_k wrong_versionM_shift raw_endpoint_all_times hard_time_raw_formula)
printf '%s\n' "${mutations[@]}" | xargs -P 6 -n 1 bash -c 'run_py "$1"' bash | tee "$qa_dir/python-mutations.txt"
printf '%s\n' "${mutations[@]}" primary_schema | xargs -P 6 -n 1 bash -c 'run_rb "$1"' bash | tee "$qa_dir/ruby-mutations.txt"
test "$(grep -c '^PY_REJECTED' "$qa_dir/python-mutations.txt")" = 29
test "$(grep -c '^RB_REJECTED' "$qa_dir/ruby-mutations.txt")" = 30
note_sha="$(shasum -a 256 research/r074v_completed_clock_upper_route.md|awk '{print $1}')"
audit_sha="$(shasum -a 256 research/r074v_completed_clock_upper_route_primary_audit.md|awk '{print $1}')"
test "$note_sha" = 031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c
test "$audit_sha" = 148b41ef2755d6ca42927595362fd59c81db8880713293a8e82c1c288fdea77d
{
 echo '# R0.74V Step 21 certificate QA report'; echo
  echo '- Python certificate: PASS, 33/33 groups, 77 finite cases.'
  echo '- Independent Ruby: PASS, 7/7 groups, 106 independent assertions.'
  echo '- Python mutations: 29/29 rejected.'; echo '- Ruby mutations: 30/30 rejected.'
 echo '- PYTHONHASHSEED 0, 1, 42 and independent Ruby regeneration are byte-identical.'; echo
 echo '## Frozen hashes'; echo; echo "- Route memo: \`$note_sha\`"; echo "- Primary audit: \`$audit_sha\`"; echo
 echo '## Boundary'; echo
 echo 'This is finite exact arithmetic, union/box, semantic, dependency, and hash QA. It does not prove the proposed occupation estimates, the remote common-shear comparison, a completed-clock upper, regularity, singularity, or a Clay claim.'
} > "$qa_report"
check_ws(){ local out code; set +e; out="$(git diff --no-index --check /dev/null "$1" 2>&1)"; code=$?; set -e; [ "$code" -le 1 ] && [ -z "$out" ]; }
for f in scripts/r074v_completed_clock_upper_route_certificate.py scripts/r074v_completed_clock_upper_route_certificate_independent.rb scripts/r074v_completed_clock_upper_route_qa.sh research/r074v_completed_clock_upper_route_certificate.json research/r074v_completed_clock_upper_route_certificate_report.md research/r074v_completed_clock_upper_route_independent_audit.md research/r074v_completed_clock_upper_route_qa_report.md; do check_ws "$f"; done
printf 'QA_PASS\tpython=29/29\truby=30/30\tseeds=3/3\nQA_TEMP\t%s\n' "$qa_dir"
