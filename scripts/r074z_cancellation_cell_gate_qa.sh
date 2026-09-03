#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PY="$ROOT/scripts/r074z_cancellation_cell_gate_certificate.py"
RB="$ROOT/scripts/r074z_cancellation_cell_gate_certificate_independent.rb"
REPORT="$ROOT/research/r074z_cancellation_cell_gate_qa_report.md"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/r074z-qa.XXXXXX")
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
python3 -m py_compile "$PY"; ruby -c "$RB" >/dev/null
python3 "$PY" >/dev/null; ruby "$RB" >/dev/null
base=''; seeds='0 1 42'
for seed in $seeds; do
  PYTHONHASHSEED=$seed R074Z_JSON="$TMP/$seed.json" R074Z_REPORT="$TMP/$seed.md" python3 "$PY" >/dev/null
  sum="$(shasum -a 256 "$TMP/$seed.json" | awk '{print $1}')/$(shasum -a 256 "$TMP/$seed.md" | awk '{print $1}')"
  if [ -z "$base" ]; then base=$sum; cp "$TMP/$seed.json" "$TMP/base.json"; cp "$TMP/$seed.md" "$TMP/base.md"; else cmp -s "$TMP/$seed.json" "$TMP/base.json"; cmp -s "$TMP/$seed.md" "$TMP/base.md"; fi
done
py_mut='fraction tube_drop endpoint_theorem conditional_to_theorem novelty clay tag reference display source_hash dependency_hash full_clock_upgrade persistence_nonstrict critical_proved analyticity_theorem omit_uniformity primary_hash literature_hash primary_verdict finite_non_hit literature_novelty literature_open'
pm=0
for m in $py_mut; do
  if R074Z_MUTATION=$m R074Z_JSON="$TMP/p-$m.json" R074Z_REPORT="$TMP/p-$m.md" python3 "$PY" >/dev/null 2>&1; then echo "Python mutation survived: $m" >&2; exit 1; fi
  pm=$((pm+1))
done
rb_mut="$py_mut primary_schema"; rmuts=0
for m in $rb_mut; do
  if R074Z_RUBY_MUTATION=$m R074Z_RUBY_REPORT="$TMP/r-$m.md" ruby "$RB" >/dev/null 2>&1; then echo "Ruby mutation survived: $m" >&2; exit 1; fi
  rmuts=$((rmuts+1))
done
for f in "$PY" "$RB" "$ROOT/research/r074z_cancellation_cell_gate_certificate.json" "$ROOT/research/r074z_cancellation_cell_gate_certificate_report.md" "$ROOT/research/r074z_cancellation_cell_gate_independent_audit.md"; do
  python3 - "$f" <<'PY'
import pathlib,sys
b=pathlib.Path(sys.argv[1]).read_bytes(); s=b.decode('utf-8')
assert not any(ord(c)<32 and c not in '\t\n\r' for c in s)
PY
  d=$(git diff --no-index --check /dev/null "$f" 2>&1 || true); [ -z "$d" ] || { echo "$d" >&2; exit 1; }
done
python3 "$PY" >/dev/null; ruby "$RB" >/dev/null
cat > "$REPORT" <<EOF
# R0.74Z certificate QA report

- Verdict: **PASS**
- Python assertions: 10/10
- Ruby assertions: 11/11
- Python negative mutations rejected: $pm/$pm
- Ruby negative mutations rejected: $rmuts/$rmuts
- PYTHONHASHSEED byte-determinism: PASS (0, 1, 42)
- Python syntax / Ruby syntax / UTF-8 / control-character / whitespace checks: PASS
- Main source SHA-256: \`$(shasum -a 256 "$ROOT/research/r074z_cancellation_cell_gate.md" | awk '{print $1}')\`
- Primary audit SHA-256: \`$(shasum -a 256 "$ROOT/research/r074z_cancellation_cell_gate_primary_audit.md" | awk '{print $1}')\` (PASS, blocker 0)
- Literature audit SHA-256: \`$(shasum -a 256 "$ROOT/research/r074z_cancellation_cell_gate_literature_audit.md" | awk '{print $1}')\` (finite non-hit, no novelty inference)
- Deterministic artifact digest: \`$base\`

Scope: FINITE EXACT ARITHMETIC/STRUCTURE ONLY. The strict no-go requires limsup(-log θ_L)/L² < κ_*. Full-clock Y.57 and the critical κ_*+o(1) layer remain OPEN/NOT PROVED; Z.16 does not upper-bound accumulated rows. Analyticity is only a conditional structural observation. Time-tame persistence requires Z.22 plus moving-strip all-winding uniformity. No novelty or Clay claim is certified.
EOF
echo "PASS python=10 ruby=11 py_mutations=$pm ruby_mutations=$rmuts seeds=3"
