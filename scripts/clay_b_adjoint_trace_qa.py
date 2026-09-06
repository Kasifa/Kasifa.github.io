#!/usr/bin/env python3
"""Finite arithmetic and actual-source provenance only, not PDE semantics."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from clay_b_ancient_sequence_qa import source_check

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("research/clay_b_adjoint_weak_trace_20260906.md", "1487c0fa39a1ee63fc3c421ebfd23028164b27c35a7f5225bdeebd60b0c2c449", "BS", 18),
    ("research/clay_b_adjoint_trace_primary_reading_20260906.md", "e8614682c41cca666241cb4891fe9880b42a3433a89e820f3bf23d875d66841b", None, 0),
    ("research/clay_b_adjoint_trace_report_20260906.md", "cf5ebbe7f039a44eacb6ca1d45d590cfe936dec7180638b4f7a9bf37fb41e326", None, 0),
]
PREVIOUS = "research/clay_b_common_adjoint_screen_release_20260906.json"
PREVIOUS_SHA = "5b96d48464f0380803617bacae049eb80bd072758f5a6556eff60bf1d8c3905a"
PREVIOUS_COMMIT = "32b12bff99e7a88d6be3d1317fd125cf30a72792"
BASE_COMMIT = "82b5d1f5a11c13a87151b08d17d6dfe674a89641"
HISTORY = {
    "research/clay_b_physical_adjoint_budget_20260905.md": "71bea08e6eba0a042ead57f1ef985de9b9d9aaa09968a7ae03a8cc2fae9f2430",
    "research/r071r_literature_audit.md": "aefe72709b38af9332bffb90213822c6a1a4208b2e42595e4bad64f295fba744",
    "research/r071s_literature_audit.md": "e7d7999e9af4a3a6de0cd7f0388a5df0621b3920bd5524cc4fc12d80370b0216",
}
HELPER = "scripts/clay_b_ancient_sequence_qa.py"
HELPER_SHA = "b9e3451bbb1774ebcf9ab4a5fb40a2722368bff3d04caee0b3cedcce2a5254d7"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def previous_check(expected):
    raw = (ROOT/PREVIOUS).read_bytes()
    obj = json.loads(raw)
    if digest(raw) != expected or obj["source_commit"] != PREVIOUS_COMMIT:
        return {"pass": False, "rows_checked": 0, "failures": ["manifest identity"]}
    rows = obj["files"]+obj["dependencies"]
    failures = []
    if len(rows) != 125 or len({r["path"] for r in rows}) != 125:
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

    # A_t has viscosity -nu, and rho differentiation reverses it.
    check("BS reversed adjoint viscosity sign", F(-1)*F(-1), 1)
    # b=-u(T-rho), b_rho=u_t and Delta b=-Delta u.
    check("BS reversed parent viscosity sign", F(1)*F(-1), -1)
    theta = (F(1, 2)-F(1, 3))/(F(1, 2)-F(1, 6))
    check("BS L3 gradient interpolation weight", theta, F(1, 2))
    check("BS w L3 time reciprocal", theta/2, F(1, 4))
    check("BS tensor space reciprocal", F(1, 3)+F(1, 6), F(1, 2))
    check("BS tensor time exponent", 1/(F(1, 4)+F(1, 2)), F(4, 3))
    check("BS energy-pairing time reciprocal sum", F(1, 2)+F(3, 4), F(5, 4))
    # e + nu D = (1-2 nu D)/2 + nu D.
    check("BS boundary energy constant", F(1, 2)*1, F(1, 2))
    check("BS dissipation coefficient cancellation", F(1, 2)*(-2)+1, 0)
    check("BS fixed-frequency Bernstein exponent", 1+F(3, 2), F(5, 2))
    # Let theta=3/q; 1/p=(1-theta)/2 and 1/r_w=theta/2.
    check("BS critical tensor-time constant coefficient", F(1, 2), F(1, 2))
    check("BS critical tensor-time theta coefficient", -F(1, 2)+F(1, 2), 0)
    check("BS q6 required drift time exponent", 2/(1-F(3, 6)), 4)
    check("BS q6 available w time exponent", 2/F(3, 6), 4)
    check("BS qInfinity required drift time exponent", 2/(1-F(0)), 2)
    return rows


def main():
    sources = [source_check(*r) for r in SOURCES]
    previous = previous_check(PREVIOUS_SHA)
    history = []
    for path, expected in HISTORY.items():
        raw = (ROOT/path).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{BASE_COMMIT}:{path}"], cwd=ROOT)
        history.append({"path": path, "sha256": digest(raw), "bytes": len(raw),
                        "pass": raw == frozen and digest(raw) == expected})
    old_live = subprocess.check_output([sys.executable, "-B", "scripts/clay_b_common_adjoint_qa.py"], cwd=ROOT)
    old_saved = (ROOT/"research/clay_b_common_adjoint_qa_20260906.json").read_bytes()
    old_qa = old_live == old_saved and json.loads(old_live)["status"] == "PASS"
    paper = json.loads((ROOT/"research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT/"AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "parsed_private_paper_unchanged": digest(json.dumps(paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
        "helper_identity": digest((ROOT/HELPER).read_bytes()) == HELPER_SHA,
    }
    controls = {
        "wrong_BS_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BS", 18)["checks"]["reviewed_hash"],
        "wrong_BS_tag_count_rejected": not source_check(SOURCES[0][0], SOURCES[0][1], "BS", 17)["checks"]["continuous_unique_tags"],
        "wrong_predecessor_manifest_rejected": not previous_check("0"*64)["pass"],
    }
    exact = arithmetic()
    passed = (all(all(s["checks"].values()) for s in sources) and previous["pass"]
              and all(r["pass"] for r in history) and old_qa
              and all(protected.values()) and all(controls.values()) and all(r["pass"] for r in exact))
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "15 named rational expressions and source bytes, not a PDE proof or automatic semantics",
        "sources": sources, "formula_tags_checked": 18, "arithmetic_checks": exact,
        "previous_freeze": {"path": PREVIOUS, "sha256": PREVIOUS_SHA, "source_commit": PREVIOUS_COMMIT, **previous},
        "historical_sources": {"base_commit": BASE_COMMIT, "rows": history},
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
