#!/bin/bash
set -euo pipefail

TASK_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TASK_PYTHON=/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
exec "$TASK_PYTHON" -B - "$TASK_ROOT" <<'PY'
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(sys.argv[1])
stem = "r076l_parabolic_edge_smoothing_complete_clock"
report_path = Path(os.environ.get("QA_REPORT", root / f"research/{stem}_qa_report.md"))
py_script = root / f"scripts/{stem}_certificate.py"
rb_script = root / f"scripts/{stem}_certificate_independent.rb"
fixture_path = root / f"scripts/{stem}_fixtures.json"
expected_path = root / f"scripts/{stem}_expected.json"
figure = root / "figures/r076l-parabolic-edge/fig-r076l-parabolic-edge"

def run(args, env=None, code=0):
    result = subprocess.run(
        [str(arg) for arg in args], cwd=root, env=env,
        capture_output=True, text=True,
    )
    if result.returncode != code:
        raise AssertionError(f"command exit {result.returncode}, expected {code}: {args}\n{result.stdout}\n{result.stderr}")
    return result

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

compile(py_script.read_text(), str(py_script), "exec")
run(["ruby", "-c", rb_script])
fixture = json.loads(fixture_path.read_text())
expected = json.loads(expected_path.read_text())
expected.pop("schema")
assert set(fixture["files"].values()) == set(fixture["frozen"]["sha256"])
assert len(fixture["files"]) == 19
for path in fixture["frozen"]["sha256"]:
    assert "AGENTS.md" not in path and "__pycache__" not in path and ".pyc" not in path
    assert not path.startswith("public/") and "publication" not in path
    assert not path.startswith(f"research/{stem}_certificate")
    assert not path.startswith(f"research/{stem}_independent")
    assert not path.startswith(f"research/{stem}_qa")

with tempfile.TemporaryDirectory(prefix="r076l-qa-") as temp:
    tmp = Path(temp)
    baseline = None
    for seed in (0, 1, 42):
        output = tmp / f"python-{seed}.json"
        run([sys.executable, "-B", py_script, "--check", "--output", output],
            env={**os.environ, "PYTHONHASHSEED": str(seed)})
        if baseline is None:
            baseline = output.read_bytes()
        else:
            assert output.read_bytes() == baseline
    py_cert = json.loads(baseline)
    assert py_cert["verdict"] == "PASS" and py_cert["freezeReady"]
    assert py_cert["assertionsPassed"] == py_cert["assertionsTotal"]
    assert py_cert["exact"] == expected and not py_cert["failures"]

    ruby_env = {
        **os.environ, "R076L_JSON": str(tmp / "python-0.json"),
        "R076L_RUBY_REPORT": str(tmp / "ruby.md"),
        "R076L_RUBY_JSON": str(tmp / "ruby.json"),
        "R076L_RUBY_MUTATION": "", "R076L_DEVELOPMENT": "",
    }
    run(["ruby", rb_script], env=ruby_env)
    rb_bytes, rb_report = (tmp / "ruby.json").read_bytes(), (tmp / "ruby.md").read_bytes()
    rb_cert = json.loads(rb_bytes)
    assert rb_cert["verdict"] == "PASS" and rb_cert["freezeReady"]
    assert rb_cert["assertionsPassed"] == rb_cert["assertionsTotal"]
    assert rb_cert["exact"] == expected and not rb_cert["failures"]
    run(["ruby", rb_script], env=ruby_env)
    assert (tmp / "ruby.json").read_bytes() == rb_bytes
    assert (tmp / "ruby.md").read_bytes() == rb_report

    mutation_counts = {}
    for language, cert in (("Python", py_cert), ("Ruby", rb_cert)):
        mutations = cert["negativeMutations"]
        assert mutations and len(mutations) == len(set(mutations))
        for mutation in mutations:
            if language == "Python":
                output = tmp / "python-mutation.json"
                run([sys.executable, "-B", py_script, "--mutation", mutation, "--output", output], code=1)
            else:
                output = tmp / "ruby.json"
                run(["ruby", rb_script], env={**ruby_env, "R076L_RUBY_MUTATION": mutation}, code=1)
            result = json.loads(output.read_text())
            assert result["verdict"] == "FAIL" and not result["freezeReady"], mutation
            assert result["failures"] and result["assertionsPassed"] < result["assertionsTotal"], mutation
        mutation_counts[language] = len(mutations)
    run([sys.executable, "-B", py_script, "--mutation", "unknown-control"], code=2)
    run(["ruby", rb_script], env={**ruby_env, "R076L_RUBY_MUTATION": "unknown-control"}, code=2)

    spec = importlib.util.spec_from_file_location("r076l_certificate", py_script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sensitivity = [
        ("heatSeriesSample", "time", "2", "heatSeriesSample"),
        ("integerShearSample", "eta", "2", "integerShearSample"),
        ("integerShearSample", "backgroundShear", "3", "integerShearSample"),
        ("operatorSample", "eta", "-1/4", "operatorSample"),
        ("geometryClockSample", "beta", "-9/40", "geometryClockSample"),
        ("normalizationSample", "physicalFluxCoefficient", "3/2", "normalizationSample"),
        ("normalizationSample", "physicalFluxAExponent", "3", "normalizationSample"),
        ("normalizationSample", "physicalFluxRExponent", "4", "normalizationSample"),
        ("normalizationSample", "plateauMassRExponent", "6", "normalizationSample"),
        ("normalizationSample", "omegaLogRate", "-4/3969", "normalizationSample"),
        ("normalizationSample", "formalKappa", "8", "normalizationSample"),
    ]
    for section, key, value, observed in sensitivity:
        altered = copy.deepcopy(fixture)
        altered[section][key] = value
        exact, checks = module.build_exact(altered)
        assert exact[observed] != expected[observed], (section, key)
    # R cancels exactly. Changing its log rate alone must have no effect;
    # changing the R exponent first makes the rate observable.
    altered = copy.deepcopy(fixture)
    altered["normalizationSample"]["rLogRate"] = "99"
    exact, _ = module.build_exact(altered)
    assert exact["normalizationSample"] == expected["normalizationSample"]
    altered["normalizationSample"]["physicalFluxRExponent"] = "4"
    exact, _ = module.build_exact(altered)
    assert exact["normalizationSample"]["omegaThirdLogRate"] != expected["normalizationSample"]["omegaThirdLogRate"]

    # Verify byte corruption against each binding on isolated temporary copies.
    # Originals and the source commit remain untouched.
    tamper_count = 0
    original_root = module.ROOT
    module.ROOT = tmp
    try:
        for index, (relative, row) in enumerate(py_cert["bindings"].items()):
            copy_path = tmp / f"binding-{index}"
            raw = (root / relative).read_bytes()
            copy_path.write_bytes(raw)
            assert module.binding(copy_path.name, row["expectedSha256"])["pass"]
            copy_path.write_bytes(bytes([raw[0] ^ 1]) + raw[1:])
            assert not module.binding(copy_path.name, row["expectedSha256"])["pass"]
            tamper_count += 1
    finally:
        module.ROOT = original_root

    before = {name: digest(figure / name) for name in ("data.csv", "figure.svg", "progress.ndjson", "resources.csv")}
    run([sys.executable, "-B", figure / "plot.py", "--check"])
    assert before == {name: digest(figure / name) for name in before}
    if (figure / "manifest.json").is_file():
        run([sys.executable, "-B", root / "research/validate_figure_package.py", figure])
    for relative, expected_hash in fixture["frozen"]["sha256"].items():
        assert digest(root / relative) == expected_hash

report = f"""# R0.76L research certificate QA

Verdict: **PASS**

- Python finite certificate: {py_cert['assertionsPassed']}/{py_cert['assertionsTotal']}.
- Independent Ruby finite certificate: {rb_cert['assertionsPassed']}/{rb_cert['assertionsTotal']}.
- Python, Ruby, and frozen expected exact ledgers: identical.
- Python hash seeds 0, 1, 42: byte-identical certificates.
- Repeated Ruby certificate and report: byte-identical.
- Python observed-ledger corruption controls: {mutation_counts['Python']}/{mutation_counts['Python']} caught by ordinary assertions.
- Ruby parsed-input corruption controls: {mutation_counts['Ruby']}/{mutation_counts['Ruby']} caught by ordinary assertions.
- Unknown control names: rejected by both implementations.
- Arithmetic input sensitivity: {len(sensitivity)}/{len(sensitivity)} changes observed.
- Exact R-log-rate cancellation and coupled exponent perturbation: PASS.
- Isolated single-byte binding corruptions: {tamper_count}/{tamper_count} rejected.
- Archived data/SVG regeneration: byte-identical; progress and resource logs unchanged.
- Source tree and frozen bytes: bound to {fixture['frozen']['sourceCommit']}.
- Figure manifest is additionally validated when present; its final validation belongs to the research freeze inventory.

The negative controls exercise finite arithmetic, validation, provenance,
and claim-boundary checks. They do not prove the continuum asymptotics or
the exact-shear transfer theorem. The analytic primary audit is a separate
source artifact. **NOT CLAY.**
"""
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(report, encoding="utf-8")
print(json.dumps({"verdict": "PASS", "pythonAssertions": py_cert["assertionsTotal"],
                  "rubyAssertions": rb_cert["assertionsTotal"], "negativeControls": mutation_counts,
                  "singleByteTamperChecks": tamper_count}))
PY
