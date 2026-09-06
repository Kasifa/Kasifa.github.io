#!/usr/bin/env python3
"""Finite expressions, one rational rank, and source bytes; not PDE semantics."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from clay_b_ancient_sequence_qa import source_check

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("research/clay_b_convex_pressure_trace_20260906.md", "5fdcfff02462775d0fd7bef22be16c75436da07a54299afc2cdbb8d36e06ffa6", "BT", 22),
    ("research/clay_b_convex_pressure_primary_reading_20260906.md", "d1089a732877a2bcbccce08f470cc114c3fdad6580c8b9e88d878ad20ef16232", None, 0),
    ("research/clay_b_convex_pressure_report_20260906.md", "8fe9a1a7ccef13c7f702d23080b21015478be1132066a65b7f30d1f7632bc9cb", None, 0),
]
PREVIOUS = "research/clay_b_adjoint_weak_trace_screen_release_20260906.json"
PREVIOUS_SHA = "a76d488aad8f484fc2f99820cb1489b9df65ad1e93b073b2bc35fd2952ba66da"
PREVIOUS_COMMIT = "65de3e3b22be98d65fc32a47b56394e22a050f75"
HELPER = "scripts/clay_b_ancient_sequence_qa.py"
HELPER_SHA = "b9e3451bbb1774ebcf9ab4a5fb40a2722368bff3d04caee0b3cedcce2a5254d7"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def spacing_ok(text):
    return re.search(r"(?<!\\)\bqquad\b", text) is None


def previous_check(expected):
    raw = (ROOT/PREVIOUS).read_bytes()
    obj = json.loads(raw)
    if digest(raw) != expected or obj["source_commit"] != PREVIOUS_COMMIT:
        return {"pass": False, "rows_checked": 0, "failures": ["manifest identity"]}
    rows = obj["files"]+obj["dependencies"]
    failures = []
    if len(rows) != 135 or len({r["path"] for r in rows}) != 135:
        failures.append("count or duplicate")
    for row in rows:
        work = (ROOT/row["path"]).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{PREVIOUS_COMMIT}:{row['path']}"], cwd=ROOT)
        if not (work == frozen and digest(work) == row["sha256"] and len(work) == row["bytes"]):
            failures.append(row["path"])
    return {"pass": not failures, "rows_checked": len(rows), "failures": failures}


def rational_rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [x/scale for x in a[row]]
        for i in range(len(a)):
            if i != row:
                factor = a[i][col]
                a[i] = [x-factor*y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def arithmetic():
    rows = []

    def check(name, value, expected):
        value, expected = F(value), F(expected)
        rows.append({"name": name, "actual": str(value), "expected": str(expected), "pass": value == expected})

    check("BT pressure time reciprocal sum", F(1, 2)+F(1, 2), 1)
    check("BT pressure space reciprocal sum", F(1, 6)+F(1, 2), F(2, 3))
    check("BT zero-mean pressure Sobolev exponent", 1/(F(2, 3)-F(1, 3)), 3)
    # s^3 times radial Hessian eigenvalue = s^2-(s^2-1).
    check("BT radial Hessian s-squared coefficient", 1-1, 0)
    check("BT radial Hessian constant coefficient", -(-1), 1)
    check("BT normalized quadratic energy constant", F(1, 2)*1, F(1, 2))
    check("BT dissipative coefficient cancellation", F(1, 2)*(-2)+1, 0)
    check("BT q1 L1 interpolation weight", 2/F(1)-1, 1)
    check("BT q3over2 L1 interpolation weight", 2/F(3, 2)-1, F(1, 3))
    check("BT formal q2 limiting weight not a trace claim", 2/F(2)-1, 0)
    # x=1/q, theta=2x-1; theta+(1-theta)/2=x.
    check("BT interpolation x coefficient", 2-1, 1)
    check("BT interpolation constant coefficient", -1+F(2, 2), 0)
    check("BT small-R gradient-bound normalization exponent", 1-1, 0)
    check("BT kappa-half amplitude residual exponent", -F(1, 2)+1, F(1, 2))
    check("BT constant-field curl-potential multiplier", -F(1, 2)*(-2), 1)
    check("BT linear-field curl-potential multiplier", -F(1, 3)*(-3), 1)
    # Symmetric H coordinates: H11,H22,H33,H12,H13,H23.
    constraints = [
        [1, -1, 0, 0, 0, 0], [0, 1, -1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1],
    ]
    check("BT symmetric Hessian trace-free constraint rank", rational_rank(constraints), 5)
    return rows


def main():
    sources = [source_check(*r) for r in SOURCES]
    for row in sources:
        row["checks"]["no_bare_qquad"] = spacing_ok((ROOT/row["path"]).read_text())
    previous = previous_check(PREVIOUS_SHA)
    old_live = subprocess.check_output([sys.executable, "-B", "scripts/clay_b_adjoint_trace_qa.py"], cwd=ROOT)
    old_saved = (ROOT/"research/clay_b_adjoint_trace_qa_20260906.json").read_bytes()
    old_qa = old_live == old_saved and json.loads(old_live)["status"] == "PASS"
    paper = json.loads((ROOT/"research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT/"AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "parsed_private_paper_unchanged": digest(json.dumps(paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
        "helper_identity": digest((ROOT/HELPER).read_bytes()) == HELPER_SHA,
    }
    actual_text = (ROOT/SOURCES[0][0]).read_text()
    altered_text = actual_text.replace(r"\qquad", "qquad", 1)
    controls = {
        "wrong_BT_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BT", 22)["checks"]["reviewed_hash"],
        "wrong_BT_tag_count_rejected": not source_check(SOURCES[0][0], SOURCES[0][1], "BT", 21)["checks"]["continuous_unique_tags"],
        "wrong_predecessor_manifest_rejected": not previous_check("0"*64)["pass"],
        "actual_text_lost_qquad_slash_rejected": actual_text != altered_text and not spacing_ok(altered_text),
    }
    exact = arithmetic()
    passed = (all(all(s["checks"].values()) for s in sources) and previous["pass"]
              and old_qa and all(protected.values()) and all(controls.values())
              and all(r["pass"] for r in exact))
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "16 named rational expressions plus one exact matrix rank and source bytes, not PDE semantics",
        "sources": sources, "formula_tags_checked": 22, "arithmetic_checks": exact,
        "previous_freeze": {"path": PREVIOUS, "sha256": PREVIOUS_SHA, "source_commit": PREVIOUS_COMMIT, **previous},
        "previous_saved_QA_live_identical": old_qa, "previous_saved_QA_bytes": len(old_saved),
        "protected_state": protected, "limited_negative_controls": controls,
        "validator": {"path": str(Path(__file__).relative_to(ROOT)), "sha256": digest(Path(__file__).read_bytes()),
                      "helper": HELPER, "helper_sha256": HELPER_SHA},
        "publication_state_inspected": False, "simulation": False, "G": "OPEN", "clay_result": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
