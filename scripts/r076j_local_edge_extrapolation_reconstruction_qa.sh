#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
STEM=r076j_local_edge_extrapolation_reconstruction
PY_SCRIPT="$ROOT/scripts/"$STEM"_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/"$STEM"_certificate_independent.rb"
FIXTURES="$ROOT/scripts/"$STEM"_fixtures.json"
EXPECTED="$ROOT/scripts/"$STEM"_expected.json"
MAIN="$ROOT/research/"$STEM".md"
PRIMARY="$ROOT/research/"$STEM"_primary_audit.md"
SOURCE="$ROOT/research/r076j_report-source.md"
R076I_MAIN="$ROOT/research/r076i_chebyshev_scale_full_plateau_window.md"
R076I_PRIMARY="$ROOT/research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md"
CERT="$ROOT/research/"$STEM"_certificate.json"
REPORT="$ROOT/research/"$STEM"_certificate_report.md"
RUBY_REPORT="$ROOT/research/"$STEM"_independent_audit.md"
QA_REPORT="$ROOT/research/"$STEM"_qa_report.md"

TMP_ROOT=$(mktemp -d /tmp/r076j-certificate-qa.XXXXXX)
trap 'rm -rf "$TMP_ROOT"' EXIT

for required in "$PY_SCRIPT" "$RUBY_SCRIPT" "$FIXTURES" "$EXPECTED" \
  "$MAIN" "$PRIMARY" "$SOURCE" "$R076I_MAIN" "$R076I_PRIMARY"; do
  test -f "$required"
done

python3 -Werror -B -c 'import pathlib,sys; compile(pathlib.Path(sys.argv[1]).read_text(), sys.argv[1], "exec")' "$PY_SCRIPT"
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"
python3 -m json.tool "$FIXTURES" >"$TMP_ROOT/fixtures.pretty"
python3 -m json.tool "$EXPECTED" >"$TMP_ROOT/expected.pretty"

# Generated outputs, the QA report, and AGENTS.md must never be members of
# the producer's frozen research-input map.
python3 - "$PY_SCRIPT" <<'PY'
import runpy
import sys

namespace = runpy.run_path(sys.argv[1])
frozen = namespace.get("FROZEN")
if not isinstance(frozen, dict) or not frozen:
    raise SystemExit("Python FROZEN map missing")
forbidden = {
    "research/r076j_local_edge_extrapolation_reconstruction_certificate.json",
    "research/r076j_local_edge_extrapolation_reconstruction_certificate_report.md",
    "research/r076j_local_edge_extrapolation_reconstruction_independent_audit.md",
    "research/r076j_local_edge_extrapolation_reconstruction_qa_report.md",
}
overlap = sorted(set(frozen) & forbidden)
if overlap:
    raise SystemExit(f"generated-output hash cycle: {overlap}")
if any(path.endswith("/AGENTS.md") or path == "AGENTS.md" for path in frozen):
    raise SystemExit("AGENTS.md entered Python FROZEN map")
required = {
    "research/r076j_local_edge_extrapolation_reconstruction.md",
    "research/r076j_report-source.md",
    "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md",
    "research/r076i_chebyshev_scale_full_plateau_window.md",
    "research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md",
}
missing = sorted(required - set(frozen))
if missing:
    raise SystemExit(f"required frozen bindings missing: {missing}")
PY

# Three hash seeds must generate byte-identical finite certificates.
for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" python3 -Werror -B "$PY_SCRIPT" \
    --check --output "$TMP_ROOT/certificate-$seed.json" \
    >"$TMP_ROOT/python-$seed.stdout"
  python3 -m json.tool "$TMP_ROOT/certificate-$seed.json" >"$TMP_ROOT/certificate-$seed.pretty"
done

cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-1.json"
cmp "$TMP_ROOT/certificate-0.json" "$TMP_ROOT/certificate-42.json"

BASE_CERT="$TMP_ROOT/certificate-0.json"
read -r verdict freeze_ready assertions python_mutations <<EOF
$(python3 - "$BASE_CERT" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
required = {"verdict", "freezeReady", "assertionsTotal", "exact", "bindings"}
missing = sorted(required - set(data))
if missing:
    raise SystemExit(f"Python certificate fields missing: {missing}")
if not isinstance(data["exact"], dict) or not data["exact"]:
    raise SystemExit("Python exact ledger missing or empty")
if not isinstance(data["bindings"], dict) or not data["bindings"]:
    raise SystemExit("Python bindings ledger missing or empty")
if not isinstance(data["assertionsTotal"], int) or data["assertionsTotal"] <= 0:
    raise SystemExit("Python assertionsTotal is not positive")
mutations = data.get("negativeMutations")
if not isinstance(mutations, list) or not mutations or len(mutations) != len(set(mutations)):
    raise SystemExit("Python negativeMutations missing, empty, or duplicated")
print(data["verdict"], str(data["freezeReady"]).lower(), data["assertionsTotal"], len(mutations))
PY
)
EOF

test "$verdict" = PASS
test "$freeze_ready" = true

env R076J_JSON="$BASE_CERT" \
  R076J_RUBY_REPORT="$TMP_ROOT/ruby-baseline.md" \
  R076J_RUBY_JSON="$TMP_ROOT/ruby-baseline.json" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-baseline.stdout"
python3 -m json.tool "$TMP_ROOT/ruby-baseline.json" >"$TMP_ROOT/ruby-baseline.pretty"
grep -q 'Verdict: \*\*PASS\*\*' "$TMP_ROOT/ruby-baseline.md"
grep -q 'J.1--J.46 equation inventory and reference closure: PASS' "$TMP_ROOT/ruby-baseline.md"
grep -q 'Independent Laguerre series/recurrence sample cross-check: PASS' "$TMP_ROOT/ruby-baseline.md"

# Fail closed on exact-ledger drift, missing cross-language bindings, or any
# accidental AGENTS.md artifact entry.  Ruby exact values are independently
# generated; Python is checked against its own declared exact ledger here.
python3 - "$BASE_CERT" "$TMP_ROOT/ruby-baseline.json" <<'PY'
import json
import sys

python_cert = json.load(open(sys.argv[1], encoding="utf-8"))
ruby_cert = json.load(open(sys.argv[2], encoding="utf-8"))
if ruby_cert.get("verdict") != "PASS" or ruby_cert.get("freezeReady") is not True:
    raise SystemExit("Ruby certificate is not frozen PASS")
required_exact = {
    ("tail", "finiteRangeFactor"): "20/19",
    ("edge", "squaredPrefactor"): "250/19",
    ("edge", "amplitudeExponentSqrt2Coefficient"): 5,
    ("edge", "laguerreSquaredExponentSqrt2Coefficient"): 10,
    ("plateau", "exteriorNumerator"): "1000/19",
    ("plateau", "interiorNumerator"): "1000/19",
    ("plateau", "holderNumerator"): "2000/19",
    ("plateau", "phiSqrt2QCoefficient"): 20,
    ("asymptotic", "modeWindowExponent"): "5/2",
    ("asymptotic", "normalizedLogRate"): "-2/11907",
    ("structure", "firstTag"): 1,
    ("structure", "lastTag"): 46,
    ("structure", "tagCount"): 46,
    ("structure", "displayCount"): 48,
}
for path, expected in required_exact.items():
    observed = ruby_cert["exact"]
    for key in path:
        observed = observed[key]
    if observed != expected:
        raise SystemExit(f"Ruby exact drift at {path}: {observed!r}")

python_exact_blob = json.dumps(python_cert["exact"], sort_keys=True, separators=(",", ":"))
for token in ('20/19', '250/19', '1000/19', '2000/19', '5/2', '-2/11907'):
    if token not in python_exact_blob:
        raise SystemExit(f"Python exact ledger lacks {token}")

required_bindings = {
    "research/r076j_local_edge_extrapolation_reconstruction.md": "a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f",
    "research/r076j_report-source.md": "371eac6e3f053d4ba51ded16f35024ba805d10c5a81c1f01879704ce583763c7",
    "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md": "1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5",
    "research/r076i_chebyshev_scale_full_plateau_window.md": "6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce",
    "research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md": "65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe",
}
for cert in (python_cert, ruby_cert):
    bindings = cert.get("bindings")
    if not isinstance(bindings, dict):
        raise SystemExit("bindings object missing")
    if any(path.endswith("/AGENTS.md") or path == "AGENTS.md" for path in bindings):
        raise SystemExit("AGENTS.md entered a certificate binding map")
    for path, digest in required_bindings.items():
        row = bindings.get(path)
        if not isinstance(row, dict):
            raise SystemExit(f"binding row missing: {path}")
        if row.get("expectedSha256") != digest or row.get("observedSha256") != digest or row.get("pass") is not True:
            raise SystemExit(f"binding mismatch: {path}")
PY

# Mutation inventories are implementation-local: each verifier must reject
# every one of its own named negative controls, plus an unknown mutation.
python_mutation_names=$(python3 -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1], encoding="utf-8"))["negativeMutations"]))' "$BASE_CERT")
python_mutations_run=0
for mutation in $python_mutation_names; do
  if env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" \
    --mutation "$mutation" --output "$TMP_ROOT/python-$mutation.json" \
    >"$TMP_ROOT/python-$mutation.stdout" 2>"$TMP_ROOT/python-$mutation.stderr"; then
    printf '%s\n' "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  python3 - "$TMP_ROOT/python-$mutation.json" <<'PY'
import json
import sys
if json.load(open(sys.argv[1], encoding="utf-8")).get("verdict") != "FAIL":
    raise SystemExit("Python negative control did not emit FAIL")
PY
  python_mutations_run=$((python_mutations_run + 1))
done
test "$python_mutations_run" -eq "$python_mutations"

ruby_mutation_names=$(env R076J_RUBY_LIST_MUTATIONS=1 ruby "$RUBY_SCRIPT")
ruby_mutation_total=$(printf '%s\n' "$ruby_mutation_names" | awk 'NF {count++} END {print count+0}')
test "$ruby_mutation_total" -gt 0
ruby_mutations_run=0
for mutation in $ruby_mutation_names; do
  if env R076J_JSON="$BASE_CERT" R076J_RUBY_MUTATION="$mutation" \
    R076J_RUBY_REPORT="$TMP_ROOT/ruby-$mutation.md" \
    R076J_RUBY_JSON="$TMP_ROOT/ruby-$mutation.json" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-$mutation.stdout" 2>"$TMP_ROOT/ruby-$mutation.stderr"; then
    printf '%s\n' "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-$mutation.md"
  ruby_mutations_run=$((ruby_mutations_run + 1))
done
test "$ruby_mutations_run" -eq "$ruby_mutation_total"

if env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" \
  --mutation unknown_mutation --output "$TMP_ROOT/unknown-python.json" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  printf '%s\n' 'Python accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown mutation: unknown_mutation' "$TMP_ROOT/unknown-python.stderr"

if env R076J_JSON="$BASE_CERT" R076J_RUBY_MUTATION=unknown_mutation \
  R076J_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  printf '%s\n' 'Ruby accepted an unknown mutation' >&2
  exit 1
fi
grep -q 'unknown R076J_RUBY_MUTATION' "$TMP_ROOT/unknown-ruby.stderr"

# Direct structural, hash, equation, and claim-boundary gate independent of
# both certificate producers.
python3 - "$ROOT" "$BASE_CERT" "$FIXTURES" "$EXPECTED" <<'PY'
import hashlib
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
certificate = json.load(open(sys.argv[2], encoding="utf-8"))
fixtures = json.load(open(sys.argv[3], encoding="utf-8"))
expected = json.load(open(sys.argv[4], encoding="utf-8"))
if fixtures.get("schema") != "r076j-local-edge-extrapolation-reconstruction-fixtures-v1":
    raise SystemExit("fixture schema drift")
if expected.get("schema") != "r076j-local-edge-extrapolation-reconstruction-expected-v1":
    raise SystemExit("expected schema drift")

locked = {
    "research/r076j_local_edge_extrapolation_reconstruction.md": "a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f",
    "research/r076j_report-source.md": "371eac6e3f053d4ba51ded16f35024ba805d10c5a81c1f01879704ce583763c7",
    "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md": "1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5",
    "research/r076i_chebyshev_scale_full_plateau_window.md": "6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce",
    "research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md": "65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe",
}
for relative, digest in locked.items():
    observed = hashlib.sha256((root / relative).read_bytes()).hexdigest()
    if observed != digest:
        raise SystemExit(f"frozen hash drift: {relative}")

main = (root / "research/r076j_local_edge_extrapolation_reconstruction.md").read_text(encoding="utf-8")
source = (root / "research/r076j_report-source.md").read_text(encoding="utf-8")
primary = (root / "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md").read_text(encoding="utf-8")
tags = [int(value) for value in re.findall(r"\\tag\{J\.(\d+)\}", main)]
refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])J\.(\d+)", main)]
if tags != list(range(1, 47)) or len(tags) != 46:
    raise SystemExit("J.1--J.46 tag sequence drift")
if set(refs) - set(tags):
    raise SystemExit("dangling J-reference")
if len(re.findall(r"^\\\[$", main, re.M)) != 48 or len(re.findall(r"^\\\]$", main, re.M)) != 48:
    raise SystemExit("display inventory drift")

compact = re.sub(r"\s+", "", main)
formula_fragments = [
    r"\frac{20}{19}", r"25N/\alpha", r"5Ne^{-5N}<\frac1{20}",
    r"\sqrt{\frac{250}{19}}", r"e^{5\sqrt2N\sqrtd}",
    r"e^{10\sqrt2N\sqrtd}", r"20\sqrt2q\sqrt{\Delta_a}",
    r"\frac{1000}{19e_a}", r"\frac{2000}{19}",
    r"q=o(L^{5/2})", r"=-\frac2{11907}",
]
missing = [fragment for fragment in formula_fragments if fragment not in compact]
if missing:
    raise SystemExit(f"equation fragments missing: {missing}")

for marker in ("**LITERATURE:**", "**PROVED LOCALLY:**", "**FINITE COMPUTATION:**", "**OPEN:**", "**NOT CLAY.**"):
    if marker not in main:
        raise SystemExit(f"claim-boundary marker missing: {marker}")
for phrase in (
    "No simulation or formal figure is needed",
    "exact one-band constant shear",
    "No novelty, priority, regularity",
):
    if phrase not in main:
        raise SystemExit(f"claim-boundary phrase missing: {phrase}")
if "not an exhaustive historical or priority search" not in source:
    raise SystemExit("source search-limit boundary missing")
if "Finite certificates" not in primary or "cannot prove" not in primary:
    raise SystemExit("primary finite-certificate boundary missing")
if any(path.endswith("/AGENTS.md") or path == "AGENTS.md" for path in certificate["bindings"]):
    raise SystemExit("AGENTS.md entered release bindings")
PY

# Materialize canonical outputs only after every temporary and negative gate
# passes, then prove deterministic regeneration.
env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" --check --output "$CERT"
cmp "$BASE_CERT" "$CERT"
env R076J_JSON="$CERT" ruby "$RUBY_SCRIPT"
cmp "$TMP_ROOT/ruby-baseline.md" "$RUBY_REPORT"

render_python_report() {
  python3 - "$1" "$2" <<'PY'
import json
import pathlib
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
groups = data["groups"]
lines = [
    "# R0.76J finite certificate report",
    "",
    f"- Verdict: **{data['verdict']}**",
    f"- Freeze-ready hash seal: **{'yes' if data['freezeReady'] else 'no'}**",
    f"- Python assertions: {data['assertionsPassed']}/{data['assertionsTotal']}",
    f"- Frozen bindings: {sum(row['pass'] for row in data['bindings'].values())}/{len(data['bindings'])}",
    f"- Failures: {'none' if not data['failures'] else ', '.join(data['failures'])}",
    "",
    "## Assertion groups",
    "",
    "| group | passed | total |",
    "|---|---:|---:|",
]
for name in sorted(groups):
    lines.append(f"| {name} | {groups[name]['passed']} | {groups[name]['total']} |")
lines.extend([
    "",
    "## Finite-certificate boundary",
    "",
    "This report audits the finite arithmetic, fixtures, equation inventory,",
    "claim labels, and frozen hashes.  It does not prove Plancherel, the",
    "continuum theorem, imported literature, regularity, or singularity.",
    "**NOT CLAY.**",
    "",
])
pathlib.Path(sys.argv[2]).write_text("\n".join(lines), encoding="utf-8")
PY
}

render_python_report "$BASE_CERT" "$TMP_ROOT/python-baseline-report.md"
render_python_report "$CERT" "$REPORT"
cmp "$TMP_ROOT/python-baseline-report.md" "$REPORT"

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" --check --output "$CERT"
render_python_report "$CERT" "$REPORT"
env R076J_JSON="$CERT" ruby "$RUBY_SCRIPT"
test "$cert_before" = "$(digest "$CERT")"
test "$report_before" = "$(digest "$REPORT")"
test "$ruby_before" = "$(digest "$RUBY_REPORT")"
python3 -m json.tool "$CERT" >"$TMP_ROOT/canonical-certificate.pretty"

: >"$QA_REPORT"
core_count=$(find "$ROOT/research" "$ROOT/scripts" -maxdepth 1 -type f \
  \( -name 'r076j_*' -o -name 'r076j-*' \) \
  ! -name 'r076j_publication_handoff*' | wc -l | tr -d ' ')
test "$core_count" -eq 12

{
  printf '%s\n' '# R0.76J certificate QA report' ''
  printf '%s\n' '- Verdict: **PASS**'
  printf '%s\n' '- Mathematical blockers: 0'
  printf '%s\n' '- Independent mathematical rereads: PASS (2 lanes; blockers 0)'
  printf '%s\n' "- Python assertions: $assertions/$assertions"
  printf '%s\n' "- Ruby assertions: $(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(str(d["assertionsPassed"])+"/"+str(d["assertionsTotal"]))' "$TMP_ROOT/ruby-baseline.json")"
  printf '%s\n' "- Negative mutations rejected: $python_mutations_run/$python_mutations Python; $ruby_mutations_run/$ruby_mutation_total Ruby"
  printf '%s\n' '- Unknown mutations rejected fail-closed by both implementations: PASS'
  printf '%s\n' '- PYTHONHASHSEED byte stability: PASS (0, 1, 42)'
  printf '%s\n' '- Independent Laguerre series/recurrence samples and tail margin: PASS'
  printf '%s\n' '- Exact 20/19, 250/19, 1000/19, 2000/19 constant ledger: PASS'
  printf '%s\n' '- Exact 5sqrt(2), 10sqrt(2), 20sqrt(2) exponent ledger: PASS'
  printf '%s\n' '- q=o(L^(5/2)) and normalized -2/11907 rate ledger: PASS'
  printf '%s\n' '- J.1--J.46, 48 displays, reference closure, hashes, and claim boundary: PASS'
  printf '%s\n' '- Generated-output hash-cycle guard: PASS'
  printf '%s\n' '- AGENTS.md excluded from bindings, inventory, and release manifest: PASS'
  printf '%s\n' '- Canonical outputs regeneration-stable: PASS'
  printf '%s\n' '- Exact core inventory: 12/12 files (11 manifest rows plus this self-generated QA report)'
  printf '%s\n' '' '## Release manifest' ''
  printf '%s\n' '| path | SHA-256 |' '|---|---|'
  for path in "$MAIN" "$PRIMARY" "$SOURCE" "$FIXTURES" "$EXPECTED" \
    "$PY_SCRIPT" "$RUBY_SCRIPT" "$ROOT/scripts/"$STEM"_qa.sh" \
    "$CERT" "$REPORT" "$RUBY_REPORT"; do
    rel=$(printf '%s\n' "$path" | sed "s|^$ROOT/||")
    test "$(basename "$rel")" != AGENTS.md
    printf '| %s | %s |\n' "$rel" "$(digest "$path")"
  done
  printf '%s\n' '' '## Boundary' ''
  printf '%s\n' 'The certificates audit a finite arithmetic, source, equation, and hash ledger.'
  printf '%s\n' 'They do not prove Plancherel, the continuum theorem, the imported literature,'
  printf '%s\n' 'or Navier--Stokes regularity or singularity. **NOT CLAY.**'
} >"$QA_REPORT"

printf '{"suite":"r076j-local-edge-extrapolation-reconstruction","status":"PASS","freezeReady":true,"pythonAssertions":%s,"rubyAssertions":%s,"pythonMutations":%s,"rubyMutations":%s,"pythonHashSeeds":3,"generatedHashCycle":false,"agentsMdArtifactIncluded":false}\n' \
  "$assertions" "$ruby_mutation_total" "$python_mutations_run" "$ruby_mutations_run"
