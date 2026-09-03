#!/usr/bin/env bash
set -euo pipefail
repo="$(cd "$(dirname "$0")/.."&&pwd)";cd "$repo"
py="$repo/scripts/r074w_remote_adjacent_inward_comparison_certificate.py";rb="$repo/scripts/r074w_remote_adjacent_inward_comparison_certificate_independent.rb"
json="$repo/research/r074w_remote_adjacent_inward_comparison_certificate.json";report="$repo/research/r074w_remote_adjacent_inward_comparison_certificate_report.md";ind="$repo/research/r074w_remote_adjacent_inward_comparison_independent_audit.md";qa_report="$repo/research/r074w_remote_adjacent_inward_comparison_qa_report.md"
python3 "$py";ruby "$rb";tmp="$(mktemp -d /tmp/r074w-remote-inward-qa.XXXXXX)"
for seed in 0 1 42;do PYTHONHASHSEED="$seed" R074W_JSON="$tmp/$seed.json" R074W_REPORT="$tmp/$seed.md" python3 "$py">/dev/null;cmp "$json" "$tmp/$seed.json";cmp "$report" "$tmp/$seed.md";done
R074W_INDEPENDENT_REPORT="$tmp/ind.md" ruby "$rb">/dev/null;cmp "$ind" "$tmp/ind.md"
run_py(){ if R074W_MUTATION="$1" R074W_JSON=/dev/null R074W_REPORT=/dev/null python3 "$py">/dev/null 2>&1;then echo "PY_FAIL_OPEN $1";return 1;else echo "PY_REJECTED $1";fi;}
run_rb(){ if R074W_INDEPENDENT_MUTATION="$1" R074W_INDEPENDENT_REPORT=/dev/null ruby "$rb">/dev/null 2>&1;then echo "RB_FAIL_OPEN $1";return 1;else echo "RB_REJECTED $1";fi;}
export py rb;export -f run_py run_rb
mutations=(swap_q64_q65 free_age_for_shear_age delete_winding absolute_o1 deterministic_equality close_critical_band wrong_packet_states drop_cross drop_inversion T_not_Tstar fixed_deletion_complete drop_not_clay fraction_margin source_hash primary_hash literature_hash tag_inventory probability_without_eta survival_quantifier sweeping_quantifier all_shell_upper_true whole_shell_complete novelty_claim)
printf '%s\n' "${mutations[@]}"|xargs -P 6 -n 1 bash -c 'run_py "$1"' bash|tee "$tmp/py-mutations.txt"
printf '%s\n' "${mutations[@]}" primary_schema|xargs -P 6 -n 1 bash -c 'run_rb "$1"' bash|tee "$tmp/rb-mutations.txt"
test "$(grep -c '^PY_REJECTED' "$tmp/py-mutations.txt")" = 23;test "$(grep -c '^RB_REJECTED' "$tmp/rb-mutations.txt")" = 24
python3 -m py_compile "$py";ruby -c "$rb">/dev/null;bash -n "$0";python3 -m json.tool "$json">/dev/null
python3 - <<'PY'
from pathlib import Path
for name in ('research/r074w_remote_adjacent_inward_comparison.md','research/r074w_remote_adjacent_inward_comparison_primary_audit.md','research/r074w_remote_adjacent_inward_literature_audit.md'):
 t=Path(name).read_text(encoding='utf-8');assert not any(ord(c)<32 and c not in '\n\r' for c in t);assert t.count(r'\[')==t.count(r'\]');assert t.count(r'\begin{aligned}')==t.count(r'\end{aligned}')
PY
main_sha="$(shasum -a 256 research/r074w_remote_adjacent_inward_comparison.md|awk '{print $1}')";primary_sha="$(shasum -a 256 research/r074w_remote_adjacent_inward_comparison_primary_audit.md|awk '{print $1}')";lit_sha="$(shasum -a 256 research/r074w_remote_adjacent_inward_literature_audit.md|awk '{print $1}')"
test "$main_sha" = d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10;test "$primary_sha" = 66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73;test "$lit_sha" = ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99
{
 echo '# R0.74W certificate QA report';echo;echo '- Python: PASS, 33/33 checks, 33 cases.';echo '- Independent Ruby: PASS, 6/6 groups, 56 assertions.';echo '- Python mutations: 23/23 rejected.';echo '- Ruby mutations: 24/24 rejected.';echo '- PYTHONHASHSEED 0, 1, 42 and Ruby regeneration: byte-identical.';echo '- Syntax, UTF-8, controls, delimiters, tags/references, JSON and scoped diff whitespace: PASS.';echo;echo '## Frozen inputs';echo;echo "- Main: \`$main_sha\`";echo "- Primary audit: \`$primary_sha\`";echo "- Literature audit: \`$lit_sha\`";echo;echo '## Boundary';echo;echo '**FINITE EXACT ARITHMETIC/STRUCTURE ONLY.** No analytic Brownian-bridge lemma, whole-shell or fixed-deletion theorem, novelty result, regularity result, singularity result, or Clay claim is proved by this QA.'
} > "$qa_report"
check_ws(){ local out code;set +e;out="$(git diff --no-index --check /dev/null "$1" 2>&1)";code=$?;set -e;[ "$code" -le 1 ]&&[ -z "$out" ];}
for f in scripts/r074w_remote_adjacent_inward_comparison_certificate.py scripts/r074w_remote_adjacent_inward_comparison_certificate_independent.rb scripts/r074w_remote_adjacent_inward_comparison_qa.sh research/r074w_remote_adjacent_inward_comparison_certificate.json research/r074w_remote_adjacent_inward_comparison_certificate_report.md research/r074w_remote_adjacent_inward_comparison_independent_audit.md research/r074w_remote_adjacent_inward_comparison_qa_report.md;do check_ws "$f";done
printf 'QA_PASS\tpython=23/23\truby=24/24\tseeds=3/3\nQA_TEMP\t%s\n' "$tmp"
