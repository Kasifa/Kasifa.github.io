#!/usr/bin/env python3
"""Read-only finite algebra and provenance, not a PDE semantic certificate."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from clay_b_ancient_sequence_qa import source_check

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("research/clay_b_energy_atom_dissipation_20260906.md", "efd0eca624055fd6e825aa1f85602f3815a1ea20e6f257263d64f0021c5a5bac", "BO", 18),
    ("research/clay_b_energy_atom_primary_reading_20260906.md", "52f5a6d164b71b86ed96fdc03f2ffef78c5f88d8e571240465413828a05d7aa5", None, 0),
    ("research/clay_b_energy_atom_report_20260906.md", "20f567d833578fecc643d522a94cd25b5025fcc813e08ebaabbb2de0f4046a63", None, 0),
]
PREVIOUS = "research/clay_b_euler_compactness_screen_release_20260906.json"
PREVIOUS_SHA = "d2ed70e3b74ba7de548afb718f3cf7fc282c28b5aa4ccc2521555a90d84c6526"
PREVIOUS_COMMIT = "14d5a44345c6835aff8dfd19123c979ae185b471"
BASE_COMMIT = "11f6e30c0f181d9b590303e47d41f902b3046009"
HISTORY = {
    "research/clay_b_concentration_path_limits_20260906.md": "18107e469330f34cf230660d7d8becb7030afca9ee38526237f5287b7c238fcf",
    "research/clay_b_local_persistence_obstruction_20260906.md": "3a5013bc18f4dd54435ec6af17c73f0c31f36893a29a34d78bf356863e3ab1d1",
    "research/clay_b_signed_upcrossing_time_integrability_20260906.md": "862a939f42b968bfc6c1dfbc01405153f11b25f042182827d7318094474a8372",
    "research/r074r_primary_literature_boundary.md": "09016b151a353559c710421503f5b51e7339cfa9a01f52949e01b53cb1b17b3b",
}
HELPER = "scripts/clay_b_ancient_sequence_qa.py"
HELPER_SHA = "b9e3451bbb1774ebcf9ab4a5fb40a2722368bff3d04caee0b3cedcce2a5254d7"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def previous_check(expected):
    raw = (ROOT/PREVIOUS).read_bytes()
    obj = json.loads(raw)
    if digest(raw) != expected or obj["source_commit"] != PREVIOUS_COMMIT:
        return {"pass": False, "rows_checked": 0, "failures": ["manifest identity"]}
    rows = obj["files"]+obj["dependencies"]
    failures = []
    if len(rows) != 104 or len({r["path"] for r in rows}) != 104:
        failures.append("count or duplicate")
    for row in rows:
        work = (ROOT/row["path"]).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{PREVIOUS_COMMIT}:{row['path']}"], cwd=ROOT)
        if not (work == frozen and digest(work) == row["sha256"] and len(work) == row["bytes"]):
            failures.append(row["path"])
    return {"pass": not failures, "rows_checked": len(rows), "failures": failures}


def arithmetic():
    rows = []

    def check(name, actual, expected):
        actual, expected = F(actual), F(expected)
        rows.append({"name": name, "actual": str(actual), "expected": str(expected), "pass": actual == expected})

    theta = (F(1, 3)-F(1, 6))/(F(1, 2)-F(1, 6))
    energy, grad = 3*theta/2, 3*(1-theta)/2
    time = 1-grad
    check("BO ball energy volume power", 3*(1-F(2, 6)), 2)
    check("BO L3 interpolation theta", theta, F(1, 2))
    check("BO GN energy power", energy, F(3, 4))
    check("BO GN gradient square power", grad, F(3, 4))
    check("BO Holder duration power", time, F(1, 4))
    check("BO retained signed gain", F(1, 2)-F(1, 4)-F(1, 8), F(1, 8))
    check("BO powered duration exponent", 4*time, 1)
    check("BO powered dissipation exponent", 4*grad, 3)
    check("BO powered energy denominator exponent", -4*energy, -3)
    check("BO powered radius exponent", -4*(-1), 4)
    d_power = 4*grad+1
    m_power, r_power = F(4)+1, F(4)-2
    check("BO eliminated duration D exponent", d_power, 4)
    check("BO eliminated duration mass exponent", m_power, 5)
    check("BO eliminated duration radius exponent", r_power, 2)
    check("BO final mass exponent", m_power/d_power, F(5, 4))
    check("BO final energy exponent", -4*energy/d_power, -F(3, 4))
    check("BO final radius exponent", r_power/d_power, F(1, 2))
    check("BO compatible duration over radius squared", F(5, 2)-2, F(1, 2))
    check("BO compatible product exponent", F(5, 2)+3*F(1, 2), 4)
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
    old_live = subprocess.check_output([sys.executable, "-B", "scripts/clay_b_euler_compactness_qa.py"], cwd=ROOT)
    old_saved = (ROOT/"research/clay_b_euler_compactness_qa_20260906.json").read_bytes()
    old_qa = old_live == old_saved and json.loads(old_live)["status"] == "PASS"
    paper = json.loads((ROOT/"research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT/"AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "parsed_private_paper_unchanged": digest(json.dumps(paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
        "helper_identity": digest((ROOT/HELPER).read_bytes()) == HELPER_SHA,
    }
    controls = {
        "wrong_BO_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BO", 18)["checks"]["reviewed_hash"],
        "wrong_BO_tag_count_rejected": not source_check(SOURCES[0][0], SOURCES[0][1], "BO", 17)["checks"]["continuous_unique_tags"],
        "wrong_predecessor_manifest_rejected": not previous_check("0"*64)["pass"],
    }
    exact = arithmetic()
    passed = (all(all(s["checks"].values()) for s in sources) and previous["pass"]
              and all(r["pass"] for r in history) and old_qa
              and all(protected.values()) and all(controls.values()) and all(r["pass"] for r in exact))
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "Explicit finite algebra and actual-source provenance, not a PDE proof or automatic semantics",
        "sources": sources, "formula_tags_checked": 18, "arithmetic_checks": exact,
        "previous_freeze": {"path": PREVIOUS, "sha256": PREVIOUS_SHA, "source_commit": PREVIOUS_COMMIT, **previous},
        "historical_sources": {"base_commit": BASE_COMMIT, "rows": history},
        "previous_saved_QA_live_identical": old_qa,
        "protected_state": protected, "limited_negative_controls": controls,
        "validator": {"path": str(Path(__file__).relative_to(ROOT)), "sha256": digest(Path(__file__).read_bytes()),
                      "helper": HELPER, "helper_sha256": HELPER_SHA},
        "publication_state_inspected": False, "simulation": False, "G": "OPEN", "clay_result": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
