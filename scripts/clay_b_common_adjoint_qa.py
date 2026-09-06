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
    ("research/clay_b_common_adjoint_full_tail_20260906.md", "c924ec592db62dfc5975e4848230fddb14849119f7c914a0056ce9d50ad9ec64", "BP", 32),
    ("research/clay_b_full_tail_second_order_20260906.md", "92c694794634105f1d6244863b03a8aacf4e80e21061abef6c96b61c8dcc7606", "BQ", 13),
    ("research/clay_b_operator_budget_strength_20260906.md", "35d7b914b633cfbd821cdfbcff5a7ce7127e50e2cb1e20f00c4913a2e23e3c61", "BR", 12),
    ("research/clay_b_common_adjoint_primary_reading_20260906.md", "e10b6664956f6c3e1e3b583c1fcf143b52c0618f01fcf7938fcb8baac58890b0", None, 0),
    ("research/clay_b_common_adjoint_report_20260906.md", "602ce0de7321076e821dc2edfc85c444e3ad4c43359d426f12202867ad150d6a", None, 0),
]
PREVIOUS = "research/clay_b_energy_atom_cost_screen_release_20260906.json"
PREVIOUS_SHA = "d63a17b488c5098874b1fc3e42735f10d39c71b5c25ea0e13da9766b63d8f6b7"
PREVIOUS_COMMIT = "7567e791fa3170bc71551c817cecc50b663d4d65"
BASE_COMMIT = "7ea29a64cc1ba081e703afec4b59b3adeb9758da"
HISTORY = {
    "research/clay_b_report-source_20260905.md": "5bbe9e994c2e5344ff139e9a632ad3908d31341e555ca1ff9e255ed1fc9b8250",
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
    if len(rows) != 115 or len({r["path"] for r in rows}) != 115:
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

    check("BP harmonic L2 volume exponent", F(3, 2), F(3, 2))
    # N^3 M^2 + N^-2 Z: balancing yields y <= C M^(4/5) Z^(3/5).
    z_power = F(3, 5)
    check("BP Nash Z power in squared norm", z_power, F(3, 5))
    check("BP Nash squared-norm ODE exponent", 1/z_power, F(5, 3))
    check("BP Nash mass denominator exponent", -F(4, 5)/z_power, -F(4, 3))
    decay = 1/(1/z_power-1)
    check("BP Nash squared-norm time decay", decay, F(3, 2))
    check("BP scalar L1-L2 norm time decay", decay/2, F(3, 4))
    theta_125 = (F(5, 12)-F(1, 6))/(F(1, 2)-F(1, 6))
    theta_3 = (F(1, 3)-F(1, 6))/(F(1, 2)-F(1, 6))
    check("BP L12/5 low-norm interpolation weight", theta_125, F(3, 4))
    check("BP L12/5 squared low-norm power", 2*theta_125, F(3, 2))
    check("BP L12/5 squared gradient power", 2*(1-theta_125), F(1, 2))
    check("BP L3 low-norm interpolation weight", theta_3, F(1, 2))
    check("BP pressure product reciprocal exponent", F(1, 6)+F(1, 2), F(2, 3))
    check("BP time Holder reciprocal total", F(1, 2)+F(1, 4)+F(1, 4), 1)
    check("BP duration Holder remainder", 1-F(1, 2)-F(1, 4), F(1, 4))
    check("BP dissipative viscosity power", -F(1, 2)/2, -F(1, 4))
    check("BP escape initial-norm power", F(3, 2)+F(1, 2), 2)
    check("BP H1 Fourier squared tail power", -2*F(1), -2)
    # c <= C d^(1/2) a^(1/4) K^(1/4) + nu l^(1/2) K^(1/2).
    check("BQ convective K inverse power", 1/F(1, 4), 4)
    check("BQ first alternative d power", -F(1, 2)/F(1, 4), -2)
    check("BQ first alternative a power", -F(1, 4)/F(1, 4), -1)
    check("BQ second alternative viscosity power", -1/F(1, 2), -2)
    check("BQ second alternative interval power", -F(1, 2)/F(1, 2), -1)
    for label, theta, p_expected, alpha_expected in [
        ("q4", F(3, 4), 8, 7), ("q6", F(1, 2), 4, 3), ("qInfinity", F(0), 2, 1)
    ]:
        check(f"BQ {label} critical time exponent", 2/(1-theta), p_expected)
        check(f"BQ {label} viscosity loss exponent", (1+theta)/(1-theta), alpha_expected)
    # Exact coefficient identities in theta, not sampling additional q's.
    check("BQ Young reciprocal constant coefficient", F(1, 2)+F(1, 2), 1)
    check("BQ Young reciprocal theta coefficient", F(1, 2)-F(1, 2), 0)
    check("BR squared-difference alpha coefficient", 1-2, -1)
    check("BR squared-difference terminal-norm coefficient", F(1), 1)
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
    old_live = subprocess.check_output([sys.executable, "-B", "scripts/clay_b_energy_atom_qa.py"], cwd=ROOT)
    old_saved = (ROOT/"research/clay_b_energy_atom_qa_20260906.json").read_bytes()
    old_qa = old_live == old_saved and json.loads(old_live)["status"] == "PASS"
    paper = json.loads((ROOT/"research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT/"AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "parsed_private_paper_unchanged": digest(json.dumps(paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
        "helper_identity": digest((ROOT/HELPER).read_bytes()) == HELPER_SHA,
    }
    controls = {
        "wrong_BP_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BP", 32)["checks"]["reviewed_hash"],
        "wrong_BR_tag_count_rejected": not source_check(SOURCES[2][0], SOURCES[2][1], "BR", 11)["checks"]["continuous_unique_tags"],
        "wrong_predecessor_manifest_rejected": not previous_check("0"*64)["pass"],
    }
    exact = arithmetic()
    passed = (all(all(s["checks"].values()) for s in sources) and previous["pass"]
              and all(r["pass"] for r in history) and old_qa
              and all(protected.values()) and all(controls.values()) and all(r["pass"] for r in exact))
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "Explicit finite algebra and actual-source provenance, not a PDE proof or automatic semantics",
        "sources": sources, "formula_tags_checked": 57, "arithmetic_checks": exact,
        "previous_freeze": {"path": PREVIOUS, "sha256": PREVIOUS_SHA, "source_commit": PREVIOUS_COMMIT, **previous},
        "historical_sources": {"base_commit": BASE_COMMIT, "rows": history},
        "previous_saved_QA_live_identical": old_qa,
        "previous_saved_QA_bytes": len(old_saved),
        "protected_state": protected, "limited_negative_controls": controls,
        "validator": {"path": str(Path(__file__).relative_to(ROOT)), "sha256": digest(Path(__file__).read_bytes()),
                      "helper": HELPER, "helper_sha256": HELPER_SHA},
        "publication_state_inspected": False, "simulation": False, "G": "OPEN", "clay_result": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
