#!/bin/sh
set -eu
R=$(CDPATH= cd -- "$(dirname -- "$0")/.."&&pwd);P="$R/scripts/r075b_bulk_clock_outer_padding_gate_certificate.py";B="$R/scripts/r075b_bulk_clock_outer_padding_gate_certificate_independent.rb";Q="$R/research/r075b_bulk_clock_outer_padding_gate_qa_report.md";T=$(mktemp -d "${TMPDIR:-/tmp}/r075b.XXXXXX");trap 'rm -rf "$T"' EXIT
python3 -m py_compile "$P";ruby -c "$B">/dev/null;python3 "$P">/dev/null;ruby "$B">/dev/null
for z in 0 1 42;do PYTHONHASHSEED=$z R075B_JSON="$T/$z.json" R075B_REPORT="$T/$z.md" python3 "$P">/dev/null;done
cmp "$T/0.json" "$T/1.json";cmp "$T/0.json" "$T/42.json";cmp "$T/0.md" "$T/1.md";cmp "$T/0.md" "$T/42.md"
ms='transport_sign r_minus2 r_minus4 safe_weight_omega outer_weight_quarter rate_swap full_clock counterexample nonzero_path source_drift dependency_drift fraction tag reference display endpoint_open accumulated_proved collar_l3 neff_exponent neff_threshold';n=0
for m in $ms;do if R075B_MUTATION=$m R075B_JSON="$T/p.json" R075B_REPORT="$T/p.md" python3 "$P">/dev/null 2>&1;then exit 1;fi;n=$((n+1));done
nr=0;for m in $ms primary_schema;do if R075B_RUBY_MUTATION=$m R075B_RUBY_REPORT="$T/r.md" ruby "$B">/dev/null 2>&1;then exit 1;fi;nr=$((nr+1));done
python3 "$P">/dev/null;ruby "$B">/dev/null
cat >"$Q" <<EOF
# R0.75B QA report

- Verdict: **PASS**
- Python assertions: 8/8
- Ruby assertions: 9/9
- Mutations rejected: $n/$n and $nr/$nr
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Source SHA-256: $(shasum -a 256 "$R/research/r075b_bulk_clock_outer_padding_gate.md"|awk '{print $1}')

Finite exact arithmetic/structure only. Safe subclock and outer endpoint paid; outer accumulated dissipation and full clock remain OPEN; the adverse full-window rate is method failure, not counterexample. NOT CLAY.
EOF
echo "PASS python=8 ruby=9 mutations=$n+$nr seeds=3"
