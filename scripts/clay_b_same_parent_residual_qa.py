#!/usr/bin/env python3
"""Finite coefficient/exponent and source-byte checks, not a PDE proof."""
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
    ("research/clay_b_same_parent_residual_20260906.md", "6620dfbf00c9a35a5b76b6315765ea38993b844d7354e25202b61a600cc018f3", "BU", 20),
    ("research/clay_b_same_parent_residual_reading_20260906.md", "a9c55437bb40ccabfe84dabcc465392e05ad72ba6b01b62d7f0405d7f052aa3e", None, 0),
    ("research/clay_b_same_parent_residual_report_20260906.md", "498723405361e572396e5748ce33fe9cc943a5848cc8551a3771c592aff6701f", None, 0),
]
PREVIOUS = "research/clay_b_convex_pressure_trace_release_20260906.json"
PREVIOUS_SHA = "881c25b4df6ea3d256479b4c2f88ddefe15141f8867afb068b9364b904a36937"
PREVIOUS_COMMIT = "1cd4679f91661ece2b3d55ae16d45ba980094344"
HELPER = "scripts/clay_b_ancient_sequence_qa.py"
HELPER_SHA = "b9e3451bbb1774ebcf9ab4a5fb40a2722368bff3d04caee0b3cedcce2a5254d7"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def opposite_sign_literals(text):
    return (r"b_\rho+(b\cdot\nabla)b+\nabla p_b&=-\nu\Delta b" in text
            and r"w_\rho+(b\cdot\nabla)w+\nabla\pi&=\nu\Delta w" in text)


def previous_check(expected):
    raw = (ROOT/PREVIOUS).read_bytes()
    obj = json.loads(raw)
    if digest(raw) != expected or obj["source_commit"] != PREVIOUS_COMMIT:
        return {"pass": False, "rows_checked": 0, "failures": ["manifest identity"]}
    rows = obj["files"]+obj["dependencies"]
    failures = []
    if len(rows) != 142 or len({row["path"] for row in rows}) != 142:
        failures.append("count or duplicate")
    for row in rows:
        work = (ROOT/row["path"]).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{PREVIOUS_COMMIT}:{row['path']}"], cwd=ROOT)
        if not (work == frozen and digest(work) == row["sha256"] and len(work) == row["bytes"]):
            failures.append(row["path"])
    return {"pass": not failures, "rows_checked": len(rows), "failures": failures}


def arithmetic():
    rows = []

    def check(name, value, expected):
        value, expected = F(value), F(expected)
        rows.append({"name": name, "actual": str(value), "expected": str(expected), "pass": value == expected})

    check("BU3-4 residual atom coefficient", 1+2*(-1), -1)
    check("BU5 positive forced Laplacian b coefficient", 1-2, -1)
    check("BU5 alternative Laplacian cw coefficient", -1+2, 1)
    # Pressure coordinates: Pi(z,z), c Pi(z,w), c^2 Pi(w,w).
    check("BU6 q mixed coefficient from pb plus cpi", -2+1, -1)
    check("BU6 q self coefficient from pb plus cpi", 1-1, 0)
    # Expand |grad b|^2-c^2|grad w|^2 with b=z-cw.
    check("BU7 differential energy mixed coefficient", 2*(-1), -2)
    check("BU7 differential energy self coefficient", (-1)**2-1, 0)
    check("BU8 Young retained dissipation coefficient", 1-F(1, 2), F(1, 2))
    check("BU9 finite pressure space reciprocal", F(1, 6)+F(1, 2), F(2, 3))
    check("BU9 gradient pressure time reciprocal", F(1, 2)+F(1, 2), 1)
    check("BU9 pressure-cutoff time reciprocal", F(1, 2)+F(1, 4), F(3, 4))
    check("BU12 L12over5 interpolation reciprocal", F(3, 4)*F(1, 2)+F(1, 4)*F(1, 6), F(5, 12))
    check("BU12 L3 interpolation reciprocal", F(1, 2)*F(1, 2)+F(1, 2)*F(1, 6), F(1, 3))
    check("BU12 transport spatial reciprocal", F(1, 6)+2*F(5, 12), 1)
    check("BU12 time length power", 1-F(1, 2)-F(1, 4), F(1, 4))
    check("BU12 boundary source time length power", 1-F(1, 2), F(1, 2))
    check("BU15 Fourier s2 summability margin only", 2*F(2)-3, 1)
    check("BU16 mixed pressure finite space reciprocal", F(1, 2)+F(1, 6), F(2, 3))
    check("BU19 entropy spatial reciprocal shortfall", F(2, 3)+F(1, 2), F(7, 6))
    check("BU19 fixed amplitude power remains", 1+0, 1)
    return rows


def main():
    sources = [source_check(*row) for row in SOURCES]
    for row in sources:
        row["checks"]["no_bare_qquad"] = re.search(r"(?<!\\)\bqquad\b", (ROOT/row["path"]).read_text()) is None
    actual = (ROOT/SOURCES[0][0]).read_text()
    sources[0]["checks"]["specific_opposite_viscosity_literals"] = opposite_sign_literals(actual)
    previous = previous_check(PREVIOUS_SHA)
    old_live = subprocess.check_output([sys.executable, "-B", "scripts/clay_b_convex_pressure_qa.py"], cwd=ROOT)
    old_saved = (ROOT/"research/clay_b_convex_pressure_qa_20260906.json").read_bytes()
    old_qa = old_live == old_saved and json.loads(old_live)["status"] == "PASS"
    paper = json.loads((ROOT/"research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT/"AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "parsed_private_paper_unchanged": digest(json.dumps(paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
        "helper_identity": digest((ROOT/HELPER).read_bytes()) == HELPER_SHA,
    }
    altered = actual.replace(r"&=-\nu\Delta b", r"&=\nu\Delta b", 1)
    controls = {
        "wrong_BU_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BU", 20)["checks"]["reviewed_hash"],
        "wrong_BU_tag_count_rejected": not source_check(SOURCES[0][0], SOURCES[0][1], "BU", 19)["checks"]["continuous_unique_tags"],
        "wrong_predecessor_manifest_rejected": not previous_check("0"*64)["pass"],
        "actual_text_reversed_b_diffusion_rejected": altered != actual and not opposite_sign_literals(altered),
    }
    exact = arithmetic()
    passed = (all(all(row["checks"].values()) for row in sources) and previous["pass"] and old_qa
              and all(protected.values()) and all(controls.values()) and all(row["pass"] for row in exact))
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "20 named rational coefficients and exponents plus source bytes; not PDE, limit, or novelty certification",
        "sources": sources, "formula_tags_checked": 20, "arithmetic_checks": exact,
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
