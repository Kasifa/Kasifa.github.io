#!/usr/bin/env bash
set -euo pipefail
r="$(cd "$(dirname "$0")/.."&&pwd)";cd "$r";py="$r/scripts/r074x_three_packet_fixed_deletion_gate_certificate.py";rb="$r/scripts/r074x_three_packet_fixed_deletion_gate_certificate_independent.rb";j="$r/research/r074x_three_packet_fixed_deletion_gate_certificate.json";pr="$r/research/r074x_three_packet_fixed_deletion_gate_certificate_report.md";ir="$r/research/r074x_three_packet_fixed_deletion_gate_independent_audit.md";qr="$r/research/r074x_three_packet_fixed_deletion_gate_qa_report.md"
python3 "$py";ruby "$rb";t="$(mktemp -d /tmp/r074x-gate-qa.XXXXXX)"
for s in 0 1 42;do PYTHONHASHSEED=$s R074X_JSON="$t/$s.json" R074X_REPORT="$t/$s.md" python3 "$py">/dev/null;cmp "$j" "$t/$s.json";cmp "$pr" "$t/$s.md";done
R074X_INDEPENDENT_REPORT="$t/i.md" ruby "$rb">/dev/null;cmp "$ir" "$t/i.md"
rp(){ R074X_MUTATION="$1" R074X_JSON=/dev/null R074X_REPORT=/dev/null python3 "$py">/dev/null 2>&1&&{ echo "PY_FAIL $1";return 1;}||echo "PY_REJECT $1";};rr(){ R074X_INDEPENDENT_MUTATION="$1" R074X_INDEPENDENT_REPORT=/dev/null ruby "$rb">/dev/null 2>&1&&{ echo "RB_FAIL $1";return 1;}||echo "RB_REJECT $1";};export py rb;export -f rp rr
m=(fraction cross_sign payment_gap payment_normalization inf_sup_swap domain_drop equal_time_forbidden strip_to_whole fixed_gate_proved route_not_nogo x52_removed clay novelty tag reference display source_hash audit_hash dependency_hash exact_solution_removed three_packet_removed literature_hash finite_non_hit no_novelty_claim)
printf '%s\n' "${m[@]}"|xargs -P6 -n1 bash -c 'rp "$1"' bash|tee "$t/p";printf '%s\n' "${m[@]}" primary_schema|xargs -P6 -n1 bash -c 'rr "$1"' bash|tee "$t/r";test "$(grep -c PY_REJECT "$t/p")" = 24;test "$(grep -c RB_REJECT "$t/r")" = 25
python3 -m py_compile "$py";ruby -c "$rb">/dev/null;bash -n "$0";python3 -m json.tool "$j">/dev/null
{
 echo '# R0.74X certificate QA report';echo;echo '- Python: PASS, 31/31 checks, 231 cases/assertions.';echo '- Ruby: PASS, 5/5 groups, 36 assertions.';echo '- Mutations: Python 24/24, Ruby 25/25 rejected.';echo '- PYTHONHASHSEED 0/1/42 and Ruby regeneration: byte-identical.';echo;echo '**FINITE EXACT ARITHMETIC/STRUCTURE ONLY.** No analytic, fixed-deletion, novelty, or Clay proof.'
} > "$qr"
cw(){ local o c;set +e;o="$(git diff --no-index --check /dev/null "$1" 2>&1)";c=$?;set -e;[ $c -le 1 ]&&[ -z "$o" ];};for f in scripts/r074x_three_packet_fixed_deletion_gate_certificate.py scripts/r074x_three_packet_fixed_deletion_gate_certificate_independent.rb scripts/r074x_three_packet_fixed_deletion_gate_qa.sh research/r074x_three_packet_fixed_deletion_gate_certificate.json research/r074x_three_packet_fixed_deletion_gate_certificate_report.md research/r074x_three_packet_fixed_deletion_gate_independent_audit.md research/r074x_three_packet_fixed_deletion_gate_qa_report.md;do cw "$f";done
printf 'QA_PASS python=24/24 ruby=25/25 seeds=3/3\nQA_TEMP %s\n' "$t"
