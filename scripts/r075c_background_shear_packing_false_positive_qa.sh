#!/bin/sh
set -eu
R=$(CDPATH= cd -- "$(dirname -- "$0")/.."&&pwd);P="$R/scripts/r075c_background_shear_packing_false_positive_certificate.py";B="$R/scripts/r075c_background_shear_packing_false_positive_certificate_independent.rb";Q="$R/research/r075c_background_shear_packing_false_positive_qa_report.md";T=$(mktemp -d "${TMPDIR:-/tmp}/r075c.XXXXXX");trap 'rm -rf "$T"' EXIT
python3 -m py_compile "$P";ruby -c "$B">/dev/null;python3 "$P">/dev/null;ruby "$B">/dev/null
for z in 0 1 42;do PYTHONHASHSEED=$z R075C_JSON="$T/$z.json" R075C_REPORT="$T/$z.md" python3 "$P">/dev/null;done
cmp "$T/0.json" "$T/1.json";cmp "$T/0.json" "$T/42.json";cmp "$T/0.md" "$T/1.md";cmp "$T/0.md" "$T/42.md"
ms='cap_volume slice_area time_volume pm_rpower fraction neff heat_power heat_integral ratio b45_disproved f_proved nonzero_path source dependency tag reference display clay';n=0
for m in $ms;do if R075C_MUTATION=$m R075C_JSON="$T/p.json" R075C_REPORT="$T/p.md" python3 "$P">/dev/null 2>&1;then exit 1;fi;n=$((n+1));done
nr=0;for m in $ms independent;do if R075C_RUBY_MUTATION=$m R075C_RUBY_REPORT="$T/r.md" ruby "$B">/dev/null 2>&1;then exit 1;fi;nr=$((nr+1));done
python3 "$P">/dev/null;ruby "$B">/dev/null
cat >"$Q" <<EOF
# R0.75C QA report

- Verdict: **PASS**
- Python assertions: 8/8
- Ruby assertions: 9/9
- Mutations rejected: $n/$n and $nr/$nr
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Source SHA-256: $(shasum -a 256 "$R/research/r075c_background_shear_packing_false_positive.md"|awk '{print $1}')

Finite exact arithmetic/structure only. Universal B.44 rejected; B.45 not disproved; passive dissipation OPEN; NOT CLAY.
EOF
echo "PASS python=8 ruby=9 mutations=$n+$nr seeds=3"
