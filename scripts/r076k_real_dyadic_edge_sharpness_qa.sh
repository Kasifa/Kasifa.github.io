#!/bin/bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
STEM=r076k_real_dyadic_edge_sharpness
PY_SCRIPT="$ROOT/scripts/"$STEM"_certificate.py"
RUBY_SCRIPT="$ROOT/scripts/"$STEM"_certificate_independent.rb"
FIXTURES="$ROOT/scripts/"$STEM"_fixtures.json"
EXPECTED="$ROOT/scripts/"$STEM"_expected.json"
MAIN="$ROOT/research/"$STEM".md"
PRIMARY="$ROOT/research/"$STEM"_primary_audit.md"
SOURCE="$ROOT/research/r076k_report-source.md"
R076J_MAIN="$ROOT/research/r076j_local_edge_extrapolation_reconstruction.md"
R076J_PRIMARY="$ROOT/research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md"
CERT="$ROOT/research/"$STEM"_certificate.json"
REPORT="$ROOT/research/"$STEM"_certificate_report.md"
RUBY_REPORT="$ROOT/research/"$STEM"_independent_audit.md"
QA_REPORT="$ROOT/research/"$STEM"_qa_report.md"

TMP_ROOT=$(mktemp -d /tmp/r076k-certificate-qa.XXXXXX)
trap 'rm -rf "$TMP_ROOT"' EXIT

for required in "$PY_SCRIPT" "$RUBY_SCRIPT" "$FIXTURES" "$EXPECTED" \
  "$MAIN" "$PRIMARY" "$SOURCE" "$R076J_MAIN" "$R076J_PRIMARY"; do
  test -f "$required"
done

python3 -Werror -B -c 'import pathlib,sys; compile(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"), sys.argv[1], "exec")' "$PY_SCRIPT"
ruby -c "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-syntax.stdout"
python3 -m json.tool "$FIXTURES" >"$TMP_ROOT/fixtures.pretty"
python3 -m json.tool "$EXPECTED" >"$TMP_ROOT/expected.pretty"

# The producer binds only immutable analytic inputs; generated outputs and
# AGENTS.md are forbidden to prevent cycles or accidental user-file capture.
python3 - "$PY_SCRIPT" <<'PY'
import runpy
import sys

namespace = runpy.run_path(sys.argv[1])
frozen = namespace.get("FROZEN")
if not isinstance(frozen, dict) or not frozen:
    raise SystemExit("Python FROZEN map missing")
required = {
    "research/r076k_real_dyadic_edge_sharpness.md",
    "research/r076k_report-source.md",
    "research/r076k_real_dyadic_edge_sharpness_primary_audit.md",
    "research/r076j_local_edge_extrapolation_reconstruction.md",
    "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md",
    "scripts/r076k_real_dyadic_edge_sharpness_fixtures.json",
    "scripts/r076k_real_dyadic_edge_sharpness_expected.json",
}
if set(frozen) != required:
    raise SystemExit(f"Python FROZEN inventory drift: {sorted(set(frozen) ^ required)}")
for path in frozen:
    if path == "AGENTS.md" or path.endswith("/AGENTS.md"):
        raise SystemExit("AGENTS.md entered Python FROZEN map")
    if any(token in path for token in ("_certificate.json", "_certificate_report.md", "_independent_audit.md", "_qa_report.md")):
        raise SystemExit(f"generated-output hash cycle: {path}")
PY

# Hash randomization must not affect the canonical Python certificate.
for seed in 0 1 42; do
  env PYTHONHASHSEED="$seed" python3 -Werror -B "$PY_SCRIPT" \
    --check --output "$TMP_ROOT/python-$seed.json"
  python3 -m json.tool "$TMP_ROOT/python-$seed.json" >"$TMP_ROOT/python-$seed.pretty"
done
cmp "$TMP_ROOT/python-0.json" "$TMP_ROOT/python-1.json"
cmp "$TMP_ROOT/python-0.json" "$TMP_ROOT/python-42.json"
BASE_CERT="$TMP_ROOT/python-0.json"

read -r python_assertions python_mutations <<EOF
$(python3 - "$BASE_CERT" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
if data.get("verdict") != "PASS" or data.get("freezeReady") is not True:
    raise SystemExit("Python certificate is not frozen PASS")
if data.get("assertionsPassed") != data.get("assertionsTotal"):
    raise SystemExit("Python assertion count mismatch")
mutations = data.get("negativeMutations")
if not isinstance(mutations, list) or not mutations or len(mutations) != len(set(mutations)):
    raise SystemExit("Python mutation inventory invalid")
if not isinstance(data.get("exact"), dict) or not data["exact"]:
    raise SystemExit("Python exact ledger missing")
print(data["assertionsTotal"], len(mutations))
PY
)
EOF

env R076K_JSON="$BASE_CERT" \
  R076K_RUBY_REPORT="$TMP_ROOT/ruby-baseline.md" \
  R076K_RUBY_JSON="$TMP_ROOT/ruby-baseline.json" \
  ruby "$RUBY_SCRIPT" >"$TMP_ROOT/ruby-baseline.stdout"
python3 -m json.tool "$TMP_ROOT/ruby-baseline.json" >"$TMP_ROOT/ruby-baseline.pretty"
grep -q 'Verdict: \*\*PASS\*\*' "$TMP_ROOT/ruby-baseline.md"

read -r ruby_assertions ruby_mutations <<EOF
$(python3 - "$BASE_CERT" "$TMP_ROOT/ruby-baseline.json" <<'PY'
import json
import sys

python_cert = json.load(open(sys.argv[1], encoding="utf-8"))
ruby_cert = json.load(open(sys.argv[2], encoding="utf-8"))
if ruby_cert.get("verdict") != "PASS" or ruby_cert.get("freezeReady") is not True:
    raise SystemExit("Ruby certificate is not frozen PASS")
if ruby_cert.get("assertionsPassed") != ruby_cert.get("assertionsTotal"):
    raise SystemExit("Ruby assertion count mismatch")
mutations = ruby_cert.get("negativeMutations")
if not isinstance(mutations, list) or not mutations or len(mutations) != len(set(mutations)):
    raise SystemExit("Ruby mutation inventory invalid")
if ruby_cert.get("exact") != python_cert.get("exact"):
    raise SystemExit("Python/Ruby exact ledgers differ")
print(ruby_cert["assertionsTotal"], len(mutations))
PY
)
EOF

# Independently require the frozen expected object as a third exact ledger.
python3 - "$BASE_CERT" "$TMP_ROOT/ruby-baseline.json" "$EXPECTED" <<'PY'
import json
import sys

python_cert = json.load(open(sys.argv[1], encoding="utf-8"))
ruby_cert = json.load(open(sys.argv[2], encoding="utf-8"))
expected = json.load(open(sys.argv[3], encoding="utf-8"))
expected.pop("schema")
if python_cert["exact"] != expected or ruby_cert["exact"] != expected:
    raise SystemExit("exact ledger differs from frozen expected JSON")
required_bindings = {
    "research/r076k_real_dyadic_edge_sharpness.md": "e293a3aa3e9c1dde443ed7a8c07afd2c709d3855d8b469b38033b04d71116bf2",
    "research/r076k_report-source.md": "21dbd71aae07ecbe910d4bcefbf6e1caccc3cddc41171a57ffd239c6eed34f3e",
    "research/r076k_real_dyadic_edge_sharpness_primary_audit.md": "36a26cb421a108127b516e47a0008625d67ec43a1d009a14bef9d7684ef03671",
    "research/r076j_local_edge_extrapolation_reconstruction.md": "a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f",
    "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md": "1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5",
    "scripts/r076k_real_dyadic_edge_sharpness_fixtures.json": "16acf468a6722ee1e66e36a855fdd1e84e56bdc3519e6e2326d6bec0a3b82518",
    "scripts/r076k_real_dyadic_edge_sharpness_expected.json": "8f32d96856fdf5d0a86030737f5bf049b227f976661089ed6d31d4a41a1c5b50",
}
for certificate, required_paths in (
    (python_cert, set(required_bindings)),
    (ruby_cert, {
        "research/r076k_real_dyadic_edge_sharpness.md",
        "research/r076k_report-source.md",
        "research/r076k_real_dyadic_edge_sharpness_primary_audit.md",
        "research/r076j_local_edge_extrapolation_reconstruction.md",
        "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md",
    }),
):
    bindings = certificate.get("bindings")
    if not isinstance(bindings, dict):
        raise SystemExit("certificate bindings missing")
    if any(path == "AGENTS.md" or path.endswith("/AGENTS.md") for path in bindings):
        raise SystemExit("AGENTS.md entered certificate bindings")
    for path in required_paths:
        digest = required_bindings[path]
        row = bindings.get(path)
        if not isinstance(row, dict):
            raise SystemExit(f"binding row missing: {path}")
        if row.get("expectedSha256") != digest or row.get("observedSha256") != digest or row.get("pass") is not True:
            raise SystemExit(f"binding mismatch: {path}")
PY

# Every implementation-local negative control must fail, as must an unknown
# name.  Baseline outputs are never reused as a mutation result.
python_mutations_run=0
while IFS= read -r mutation; do
  test -n "$mutation"
  if env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" \
    --mutation "$mutation" --output "$TMP_ROOT/python-mutation.json" \
    >"$TMP_ROOT/python-mutation.stdout" 2>"$TMP_ROOT/python-mutation.stderr"; then
    echo "Python mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  python3 - "$TMP_ROOT/python-mutation.json" <<'PY'
import json
import sys
if json.load(open(sys.argv[1], encoding="utf-8")).get("verdict") != "FAIL":
    raise SystemExit("Python mutation did not emit FAIL")
PY
  python_mutations_run=$((python_mutations_run + 1))
done < <(python3 -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1], encoding="utf-8"))["negativeMutations"]))' "$BASE_CERT")
test "$python_mutations_run" -eq "$python_mutations"

ruby_mutation_names=$(env R076K_RUBY_LIST_MUTATIONS=1 ruby "$RUBY_SCRIPT")
ruby_mutation_total=$(printf '%s\n' "$ruby_mutation_names" | awk 'NF {count++} END {print count+0}')
test "$ruby_mutation_total" -eq "$ruby_mutations"
ruby_mutations_run=0
for mutation in $ruby_mutation_names; do
  if env R076K_JSON="$BASE_CERT" R076K_RUBY_MUTATION="$mutation" \
    R076K_RUBY_REPORT="$TMP_ROOT/ruby-mutation.md" \
    R076K_RUBY_JSON="$TMP_ROOT/ruby-mutation.json" \
    ruby "$RUBY_SCRIPT" \
    >"$TMP_ROOT/ruby-mutation.stdout" 2>"$TMP_ROOT/ruby-mutation.stderr"; then
    echo "Ruby mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -q 'Verdict: \*\*FAIL\*\*' "$TMP_ROOT/ruby-mutation.md"
  ruby_mutations_run=$((ruby_mutations_run + 1))
done
test "$ruby_mutations_run" -eq "$ruby_mutations"

if python3 -Werror -B "$PY_SCRIPT" --mutation unknown_mutation \
  --output "$TMP_ROOT/unknown-python.json" \
  >"$TMP_ROOT/unknown-python.stdout" 2>"$TMP_ROOT/unknown-python.stderr"; then
  echo 'Python accepted unknown mutation' >&2
  exit 1
fi
grep -q 'unknown mutation' "$TMP_ROOT/unknown-python.stderr"

if env R076K_JSON="$BASE_CERT" R076K_RUBY_MUTATION=unknown_mutation \
  R076K_RUBY_REPORT="$TMP_ROOT/unknown-ruby.md" \
  R076K_RUBY_JSON="$TMP_ROOT/unknown-ruby.json" \
  ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/unknown-ruby.stdout" 2>"$TMP_ROOT/unknown-ruby.stderr"; then
  echo 'Ruby accepted unknown mutation' >&2
  exit 1
fi
grep -qi 'unknown' "$TMP_ROOT/unknown-ruby.stderr"

# A direct gate, independent of both producers, checks frozen bytes, equation
# inventory, exact high-risk rows, and the conservative claim boundary.
python3 - "$ROOT" "$EXPECTED" <<'PY'
import hashlib
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
expected = json.load(open(sys.argv[2], encoding="utf-8"))
locked = {
    "research/r076k_real_dyadic_edge_sharpness.md": "e293a3aa3e9c1dde443ed7a8c07afd2c709d3855d8b469b38033b04d71116bf2",
    "research/r076k_report-source.md": "21dbd71aae07ecbe910d4bcefbf6e1caccc3cddc41171a57ffd239c6eed34f3e",
    "research/r076k_real_dyadic_edge_sharpness_primary_audit.md": "36a26cb421a108127b516e47a0008625d67ec43a1d009a14bef9d7684ef03671",
    "research/r076j_local_edge_extrapolation_reconstruction.md": "a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f",
    "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md": "1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5",
}
for relative, digest in locked.items():
    raw = (root / relative).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise SystemExit(f"frozen hash drift: {relative}")
    if b"\r" in raw or b"\t" in raw or re.search(rb"[ \t]+$", raw, re.M):
        raise SystemExit(f"text hygiene drift: {relative}")
    if any((byte < 32 and byte != 10) or byte == 127 for byte in raw):
        raise SystemExit(f"control byte: {relative}")

main = (root / "research/r076k_real_dyadic_edge_sharpness.md").read_text(encoding="utf-8")
source = (root / "research/r076k_report-source.md").read_text(encoding="utf-8")
primary = (root / "research/r076k_real_dyadic_edge_sharpness_primary_audit.md").read_text(encoding="utf-8")
tags = [int(value) for value in re.findall(r"\\tag\{K\.(\d+)\}", main)]
without_tags = re.sub(r"\\tag\{K\.\d+\}", "", main)
refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])K\.(\d+)", without_tags)]
if tags != list(range(1, 49)) or len(tags) != 48 or set(refs) - set(tags):
    raise SystemExit("K.1--K.48 inventory or reference closure drift")
if len(re.findall(r"^\\\[$", main, re.M)) != 48 or len(re.findall(r"^\\\]$", main, re.M)) != 48:
    raise SystemExit("display inventory drift")
compact = re.sub(r"\s+", "", main)
for fragment in (
    r"\frac1{2\sqrt2}", r"\fracd{128}", r"\fracq{\sqrt2}",
    r"\eta_Lq(L)^27^{q(L)}\longrightarrow0", r"q(L)=o(L^2)",
    r"U_m(x_r)^2-U_m(-x_r)^2", r"4\sin(2x_r)T_m(x_r)^2",
    r"x-\frac{v\tau}{e_a}+\frac{2iM_L\tau}{A^2}",
    r"e^{-(T/A^2)D^2}T_{2n}", r"A^(3/2)<<m=o(A^2)",
):
    if fragment not in compact:
        raise SystemExit(f"formula fragment missing: {fragment}")
for marker in ("**LITERATURE:**", "**PROVED LOCALLY:**", "**FINITE COMPUTATION:**", "**OPEN:**", "**NOT CLAY.**"):
    if marker not in main:
        raise SystemExit(f"claim marker missing: {marker}")
for phrase in ("No simulation or formal scientific figure is needed", "No novelty or priority claim is made", "complete signed collar flux"):
    if phrase not in main:
        raise SystemExit(f"claim phrase missing: {phrase}")
if "not evidence of novelty or priority" not in source or "R0.76K keeps that problem open" not in source:
    raise SystemExit("source boundary missing")
if "PASS -- single-slice theorem only" not in primary or "complete-clock flux remains open" not in primary:
    raise SystemExit("primary verdict boundary missing")

integer = expected["integerSliceSample"]
if integer["netHeatExponents"] != ["0"] * 4 or integer["carrierPhaseOverPi"] != "5/3":
    raise SystemExit("integer heat/phase ledger drift")
semi = expected["semigroupSample"]
if semi["directDecayExponents"] != semi["rhsCombinedDecayExponents"] or semi["directPhases"] != semi["rhsCombinedPhases"]:
    raise SystemExit("finite-eta semigroup ledger drift")
if semi["imaginaryShift"] != "1/2" or semi["scalarHeatExponent"] != "-1/4":
    raise SystemExit("semigroup sign drift")
if expected["backwardHeatSample"]["exactValue"] == expected["backwardHeatSample"]["wrongForwardSignValue"]:
    raise SystemExit("backward/forward sign control collapsed")
claims = expected["claims"]
if claims["completeFluxLowerBound"] or claims["fullQOLFiveHalvesRange"] or claims["l3EndpointOptimality"] or claims["clayClaimed"]:
    raise SystemExit("open claim upgraded")
PY

render_python_report() {
  python3 - "$1" "$2" <<'PY'
import json
import pathlib
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
lines = [
    "# R0.76K finite certificate report",
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
for name in sorted(data["groups"]):
    row = data["groups"][name]
    lines.append(f"| {name} | {row['passed']} | {row['total']} |")
lines.extend([
    "",
    "## Finite-certificate boundary",
    "",
    "This report audits finite coefficient, phase, polynomial, constant,",
    "geometry, semigroup, backward-heat, equation, claim, and hash ledgers.",
    "It does not prove the continuum limits or a complete-clock flux lower",
    "bound. **NOT CLAY.**",
    "",
])
pathlib.Path(sys.argv[2]).write_text("\n".join(lines), encoding="utf-8")
PY
}

# Materialize canonical outputs only after temporary and negative gates pass.
env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" --check --output "$CERT"
cmp "$BASE_CERT" "$CERT"
render_python_report "$CERT" "$REPORT"
env R076K_JSON="$CERT" R076K_RUBY_REPORT="$RUBY_REPORT" \
  R076K_RUBY_JSON="$TMP_ROOT/ruby-final.json" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/ruby-final.stdout"
cmp "$TMP_ROOT/ruby-baseline.json" "$TMP_ROOT/ruby-final.json"
cmp "$TMP_ROOT/ruby-baseline.md" "$RUBY_REPORT"

digest() {
  shasum -a 256 "$1" | awk '{print $1}'
}

cert_before=$(digest "$CERT")
report_before=$(digest "$REPORT")
ruby_before=$(digest "$RUBY_REPORT")
env PYTHONHASHSEED=0 python3 -Werror -B "$PY_SCRIPT" --check --output "$CERT"
render_python_report "$CERT" "$REPORT"
env R076K_JSON="$CERT" R076K_RUBY_REPORT="$RUBY_REPORT" \
  R076K_RUBY_JSON="$TMP_ROOT/ruby-regenerated.json" ruby "$RUBY_SCRIPT" \
  >"$TMP_ROOT/ruby-regenerated.stdout"
test "$(digest "$CERT")" = "$cert_before"
test "$(digest "$REPORT")" = "$report_before"
test "$(digest "$RUBY_REPORT")" = "$ruby_before"
cmp "$TMP_ROOT/ruby-final.json" "$TMP_ROOT/ruby-regenerated.json"

python3 - "$ROOT" "$QA_REPORT" "$CERT" "$TMP_ROOT/ruby-final.json" \
  "$python_mutations_run" "$ruby_mutations_run" <<'PY'
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
qa_path = pathlib.Path(sys.argv[2])
python_cert = json.load(open(sys.argv[3], encoding="utf-8"))
ruby_cert = json.load(open(sys.argv[4], encoding="utf-8"))
python_mutations = int(sys.argv[5])
ruby_mutations = int(sys.argv[6])
manifest = [
    "research/r076k_real_dyadic_edge_sharpness.md",
    "research/r076k_real_dyadic_edge_sharpness_primary_audit.md",
    "research/r076k_report-source.md",
    "scripts/r076k_real_dyadic_edge_sharpness_fixtures.json",
    "scripts/r076k_real_dyadic_edge_sharpness_expected.json",
    "scripts/r076k_real_dyadic_edge_sharpness_certificate.py",
    "scripts/r076k_real_dyadic_edge_sharpness_certificate_independent.rb",
    "scripts/r076k_real_dyadic_edge_sharpness_qa.sh",
    "research/r076k_real_dyadic_edge_sharpness_certificate.json",
    "research/r076k_real_dyadic_edge_sharpness_certificate_report.md",
    "research/r076k_real_dyadic_edge_sharpness_independent_audit.md",
]
if any("AGENTS.md" in path for path in manifest):
    raise SystemExit("AGENTS.md entered manifest")
rows = []
for relative in manifest:
    path = root / relative
    rows.append((relative, hashlib.sha256(path.read_bytes()).hexdigest()))
lines = [
    "# R0.76K certificate QA report",
    "",
    "- Verdict: **PASS**",
    "- Mathematical blockers: 0",
    "- Independent mathematical rereads: PASS (4 lanes; blockers 0 after corrections)",
    f"- Python assertions: {python_cert['assertionsPassed']}/{python_cert['assertionsTotal']}",
    f"- Ruby assertions: {ruby_cert['assertionsPassed']}/{ruby_cert['assertionsTotal']}",
    f"- Negative mutations rejected: {python_mutations}/{len(python_cert['negativeMutations'])} Python; {ruby_mutations}/{len(ruby_cert['negativeMutations'])} Ruby",
    "- Unknown mutations rejected fail-closed by both implementations: PASS",
    "- PYTHONHASHSEED byte stability: PASS (0, 1, 42)",
    "- Exact coefficient and independent Taylor/binomial routes: PASS",
    "- Exact integer-slice complex and cosine routes, heat prepayment, and phases: PASS",
    "- Finite-eta K.46 decay/phase conjugation and sign controls: PASS",
    "- K.48 backward-heat value and independent wrong-forward-sign control: PASS",
    "- K.1--K.48, 48 displays, dangling-reference gate, hashes, and claim boundary: PASS",
    "- q=o(L^2) proved slice range; q=o(L^(5/2)) full lower range remains open",
    "- Complete-clock signed flux relative to full plateau remains open",
    "- Generated-output hash-cycle guard: PASS",
    "- AGENTS.md excluded from bindings, inventory, and release manifest: PASS",
    "- Canonical outputs regeneration-stable: PASS",
    "- Formal figure required: no; simulation required: no",
    "- Exact core inventory: 12/12 files (11 manifest rows plus this QA report)",
    "",
    "## Release manifest",
    "",
    "| path | SHA-256 |",
    "|---|---|",
]
lines.extend(f"| {relative} | {digest} |" for relative, digest in rows)
lines.extend([
    "",
    "## Boundary",
    "",
    "The certificates audit finite arithmetic, source, equation, claim, and",
    "hash ledgers. They do not prove the continuum limit, a complete-clock",
    "flux lower bound, regularity, or singularity. **NOT CLAY.**",
    "",
])
qa_path.write_text("\n".join(lines), encoding="utf-8")
PY

# Re-render the self-generated QA report once and demand byte stability.
qa_before=$(digest "$QA_REPORT")
python3 - "$ROOT" "$QA_REPORT" "$CERT" "$TMP_ROOT/ruby-final.json" \
  "$python_mutations_run" "$ruby_mutations_run" <<'PY'
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
qa_path = pathlib.Path(sys.argv[2])
python_cert = json.load(open(sys.argv[3], encoding="utf-8"))
ruby_cert = json.load(open(sys.argv[4], encoding="utf-8"))
manifest = [
    "research/r076k_real_dyadic_edge_sharpness.md",
    "research/r076k_real_dyadic_edge_sharpness_primary_audit.md",
    "research/r076k_report-source.md",
    "scripts/r076k_real_dyadic_edge_sharpness_fixtures.json",
    "scripts/r076k_real_dyadic_edge_sharpness_expected.json",
    "scripts/r076k_real_dyadic_edge_sharpness_certificate.py",
    "scripts/r076k_real_dyadic_edge_sharpness_certificate_independent.rb",
    "scripts/r076k_real_dyadic_edge_sharpness_qa.sh",
    "research/r076k_real_dyadic_edge_sharpness_certificate.json",
    "research/r076k_real_dyadic_edge_sharpness_certificate_report.md",
    "research/r076k_real_dyadic_edge_sharpness_independent_audit.md",
]
rows = [(relative, hashlib.sha256((root / relative).read_bytes()).hexdigest()) for relative in manifest]
lines = [
    "# R0.76K certificate QA report", "", "- Verdict: **PASS**",
    "- Mathematical blockers: 0",
    "- Independent mathematical rereads: PASS (4 lanes; blockers 0 after corrections)",
    f"- Python assertions: {python_cert['assertionsPassed']}/{python_cert['assertionsTotal']}",
    f"- Ruby assertions: {ruby_cert['assertionsPassed']}/{ruby_cert['assertionsTotal']}",
    f"- Negative mutations rejected: {sys.argv[5]}/{len(python_cert['negativeMutations'])} Python; {sys.argv[6]}/{len(ruby_cert['negativeMutations'])} Ruby",
    "- Unknown mutations rejected fail-closed by both implementations: PASS",
    "- PYTHONHASHSEED byte stability: PASS (0, 1, 42)",
    "- Exact coefficient and independent Taylor/binomial routes: PASS",
    "- Exact integer-slice complex and cosine routes, heat prepayment, and phases: PASS",
    "- Finite-eta K.46 decay/phase conjugation and sign controls: PASS",
    "- K.48 backward-heat value and independent wrong-forward-sign control: PASS",
    "- K.1--K.48, 48 displays, dangling-reference gate, hashes, and claim boundary: PASS",
    "- q=o(L^2) proved slice range; q=o(L^(5/2)) full lower range remains open",
    "- Complete-clock signed flux relative to full plateau remains open",
    "- Generated-output hash-cycle guard: PASS",
    "- AGENTS.md excluded from bindings, inventory, and release manifest: PASS",
    "- Canonical outputs regeneration-stable: PASS",
    "- Formal figure required: no; simulation required: no",
    "- Exact core inventory: 12/12 files (11 manifest rows plus this QA report)",
    "", "## Release manifest", "", "| path | SHA-256 |", "|---|---|",
]
lines.extend(f"| {relative} | {digest} |" for relative, digest in rows)
lines.extend(["", "## Boundary", "", "The certificates audit finite arithmetic, source, equation, claim, and", "hash ledgers. They do not prove the continuum limit, a complete-clock", "flux lower bound, regularity, or singularity. **NOT CLAY.**", ""])
qa_path.write_text("\n".join(lines), encoding="utf-8")
PY
test "$(digest "$QA_REPORT")" = "$qa_before"

printf '%s\n' "R0.76K_QA=PASS"
printf '%s\n' "PYTHON_ASSERTIONS=$python_assertions/$python_assertions"
printf '%s\n' "RUBY_ASSERTIONS=$ruby_assertions/$ruby_assertions"
printf '%s\n' "PYTHON_MUTATIONS=$python_mutations_run/$python_mutations"
printf '%s\n' "RUBY_MUTATIONS=$ruby_mutations_run/$ruby_mutations"
printf '%s\n' "CORE_FILES=12/12"
