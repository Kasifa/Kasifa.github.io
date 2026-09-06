#!/usr/bin/env python3
"""Finite coefficient/exponent and source checks, not PDE or limit semantics."""
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
    ("research/clay_b_signed_mixed_pressure_20260907.md", "2d793018ad1de5d9c4bdb56edda46f591dbce8df9a0ec2a3fd9dcf66942c4199", "BV", 23),
    ("research/clay_b_signed_mixed_pressure_reading_20260907.md", "f10ee68c876175a2b34ced557702248713dc5135766ad746ea92813b3deb208a", None, 0),
    ("research/clay_b_signed_mixed_pressure_report_20260907.md", "fabb3577a11e06e08b4c83bd5ea991d6d900f903cb1a9bdc532e100176e69440", None, 0),
]
PREVIOUS = "research/clay_b_same_parent_residual_release_20260906.json"
PREVIOUS_SHA = "511286836b23b8f3507f09d300709777c264d1be009f44f8475aa208bc91c227"
PREVIOUS_COMMIT = "9708a86053d507a51b0c3843211774ede954efea"
HELPER = "scripts/clay_b_ancient_sequence_qa.py"
HELPER_SHA = "b9e3451bbb1774ebcf9ab4a5fb40a2722368bff3d04caee0b3cedcce2a5254d7"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def joint_source_sign_literals(text):
    return (r"&-2\nu c\sum_k\int Z_R[\partial_kz,\partial_kw]" in text
            and r"-2\nu c\sum_k\int C_R[\partial_kw,\partial_kw]" in text)


def previous_check(expected):
    raw = (ROOT/PREVIOUS).read_bytes()
    obj = json.loads(raw)
    if digest(raw) != expected or obj["source_commit"] != PREVIOUS_COMMIT:
        return {"pass": False, "rows_checked": 0, "failures": ["manifest identity"]}
    rows = obj["files"]+obj["dependencies"]
    failures = []
    if len(rows) != 149 or len({row["path"] for row in rows}) != 149:
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

    check("BV2 pressure-gradient sign multiplication", (-1)*(-1), 1)
    check("BV3 projected transport coefficient", 0-1, -1)
    check("BV5 spatial Holder reciprocal", F(1, 6)+F(1, 3)+F(1, 2), 1)
    check("BV fixed amplitude pressure time reciprocal", F(1, 2)+F(1, 2), 1)
    check("BV6 unpaid weighted time reciprocal", F(1, 4)+1, F(5, 4))
    check("BV8 f fourth power exponent", F(1, 8)*4, F(1, 2))
    check("BV8 d time exponent", F(15, 16), F(15, 16))
    check("BV8 product time exponent", F(1, 8)+F(15, 16), F(17, 16))
    check("BV10 bilinear derivative bound coefficient", 3+3, 6)
    check("BV12 same-amplitude Hessian scale power", -1+1, 0)
    check("BV14 opposite diffusion cross cancellation", 1-1, 0)
    check("BV14 source Z coefficient divided by nu c", 2*(-1), -2)
    check("BV14 source C coefficient divided by nu c", 2*(-1), -2)
    check("BV16 z-square constant coefficient", 6, 6)
    check("BV16 z-square c coefficient", 12/F(2), 6)
    check("BV16 w-square constant coefficient", 6, 6)
    check("BV16 w-square c coefficient", 12/F(2)+2, 8)
    check("BV16 limiting w-gradient coefficient", -2*1, -2)
    check("BV17 pressure primitive coefficient cancellation", -2-(-2), 0)
    check("BV18 mixed pressure coefficient divided by c", (-1)*(-1)*(-1), -1)
    check("BV20 moved combined-pressure coefficient", -1, -1)
    check("BV21 pressure-square time reciprocal", F(1, 2)+F(1, 2), 1)
    check("BV22 interpolated space reciprocal", (F(2, 3)+F(1, 3))/2, F(1, 2))
    check("BV22 interpolated time reciprocal", (F(1, 2)+1)/2, F(3, 4))
    check("BV22 required dual time exponent", 1/(1-F(3, 4)), 4)
    return rows


def main():
    sources = [source_check(*row) for row in SOURCES]
    for row in sources:
        row["checks"]["no_bare_qquad"] = re.search(r"(?<!\\)\bqquad\b", (ROOT/row["path"]).read_text()) is None
    actual = (ROOT/SOURCES[0][0]).read_text()
    sources[0]["checks"]["specific_joint_source_signs"] = joint_source_sign_literals(actual)
    previous = previous_check(PREVIOUS_SHA)
    old_live = subprocess.check_output([sys.executable, "-B", "scripts/clay_b_same_parent_residual_qa.py"], cwd=ROOT)
    old_saved = (ROOT/"research/clay_b_same_parent_residual_qa_20260906.json").read_bytes()
    old_qa = old_live == old_saved and json.loads(old_live)["status"] == "PASS"
    paper = json.loads((ROOT/"research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT/"AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "parsed_private_paper_unchanged": digest(json.dumps(paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
        "helper_identity": digest((ROOT/HELPER).read_bytes()) == HELPER_SHA,
    }
    altered = actual.replace(r"-2\nu c\sum_k\int C_R", r"+2\nu c\sum_k\int C_R", 1)
    controls = {
        "wrong_BV_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BV", 23)["checks"]["reviewed_hash"],
        "wrong_BV_tag_count_rejected": not source_check(SOURCES[0][0], SOURCES[0][1], "BV", 22)["checks"]["continuous_unique_tags"],
        "wrong_predecessor_manifest_rejected": not previous_check("0"*64)["pass"],
        "actual_text_reversed_joint_source_rejected": altered != actual and not joint_source_sign_literals(altered),
    }
    exact = arithmetic()
    passed = (all(all(row["checks"].values()) for row in sources) and previous["pass"] and old_qa
              and all(protected.values()) and all(controls.values()) and all(row["pass"] for row in exact))
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "25 named finite rational coefficients/exponents plus source bytes; not PDE, limit, or novelty certification",
        "sources": sources, "formula_tags_checked": 23, "arithmetic_checks": exact,
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
