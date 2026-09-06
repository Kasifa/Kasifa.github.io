#!/usr/bin/env python3
"""Read-only finite bookkeeping and provenance; not a PDE proof certificate."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
from clay_b_ancient_sequence_qa import source_check
from clay_b_euler_scaling_qa import previous_check, PREVIOUS, PREVIOUS_SHA, PREVIOUS_COMMIT

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("research/clay_b_critical_euler_compactness_20260906.md", "69f34722f1158324610b18e94e611ace714424dc506254afcacd4bd37a057954", "BL", 20),
    ("research/clay_b_euler_rigidity_energy_atom_20260906.md", "e023ac8a8140dcf523a1a6bee70a810b6f58041529e34f79c94df89f1355b907", "BM", 8),
    ("research/clay_b_periodic_no_atom_endpoint_20260906.md", "11d2133b8c4cd0de6242bff03d1c2c8e4d5d6e12237e3da2cc4c35bb1e6d5b5c", "BN", 8),
    ("research/clay_b_euler_compactness_primary_reading_20260906.md", "3c12f717fd8e4a2102c79b274a849ddb9b5736d296026b19f8b4e53e1abfb456", None, 0),
    ("research/clay_b_euler_compactness_report_20260906.md", "526a362083423d2fe2be657ccb4efc75fa79b818e385c80000d16ce5bf972d4d", None, 0),
]
STAGE_COMMIT = "b85838c7139c7e6e248d3c1dfebd0866a92a166a"
STAGE_FILES = [
    "research/clay_b_euler_scaling_energy_preflight_20260906.md",
    "research/clay_b_stage_strategy_review_20260906.md",
    "research/clay_b_stage_strategy_primary_reading_20260906.md",
    "research/clay_b_stage_strategy_internal_audit_20260906.md",
    "research/clay_b_euler_scaling_qa_20260906.json",
    "scripts/clay_b_euler_scaling_qa.py",
]
HELPERS = {
    "scripts/clay_b_euler_scaling_qa.py": "f5c987b9f064a02af3e164be0ee197b8aab2f82ab24fbbf7564d5a00e393d09c",
    "scripts/clay_b_ancient_sequence_qa.py": "b9e3451bbb1774ebcf9ab4a5fb40a2722368bff3d04caee0b3cedcce2a5254d7",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def arithmetic():
    out = []

    def check(name, value, expected):
        value, expected = F(value), F(expected)
        out.append({"name": name, "actual": str(value), "expected": str(expected), "pass": value == expected})

    p, q = F(10, 3), F(11, 3)
    theta = (F(1, 3)-1/p)/(F(1, 2)-1/p)
    check("BL GN energy power", (p-2)/2, F(2, 3))
    check("BL far pressure radial power", 3-3*F(5, 3), -2)
    check("BL pressure integral interpolation", F(3, 2)/F(5, 3), F(9, 10))
    check("BL pressure volume power", 1-F(3, 2)/F(5, 3), F(1, 10))
    check("BL mollified time Holder", 1-1/F(5, 3), F(2, 5))
    check("BL strong L3 interpolation theta", theta, F(1, 6))
    check("BL terminal layer power", 1-3/p, F(1, 10))
    check("BM cubic lower bound power", 2/(3*theta), 4)
    check("BM high norm denominator power", -2*(1-theta)/(p*theta), -3)
    dim = 3+F(5, 2)
    check("BN cylinder volume power", dim, F(11, 2))
    check("BN pressure velocity reciprocal sum", 1/(q/2)+1/q, F(9, 11))
    check("BN time cutoff power", -F(5, 2)+dim*(1-2/q), 0)
    check("BN nonlinear flux power", -1+dim*(1-3/q), 0)
    check("BN viscous cutoff power", -2+dim*(1-2/q), F(1, 2))
    check("BN energy-only time loss", -F(5, 2)+dim*(1-2/p), -F(3, 10))
    check("BN energy-only flux loss", -1+dim*(1-3/p), -F(9, 20))
    check("LS strong diagonal critical line", 6/q+5/q, 3)
    check("LS diagonal concentration threshold", 3-(2/q)/(1-3/q), 0)
    # Coefficients in x=1/p after substituting 1/q=3/4-3x/2.
    check("BN energy line constant coefficient", 5*F(3, 4), F(15, 4))
    check("BN energy line x coefficient", 6-5*F(3, 2), -F(3, 2))
    return out


def main():
    sources = [source_check(*row) for row in SOURCES]
    previous = previous_check(PREVIOUS_SHA)
    stage = []
    for path in STAGE_FILES:
        raw = (ROOT/path).read_bytes()
        old = subprocess.check_output(["git", "show", f"{STAGE_COMMIT}:{path}"], cwd=ROOT)
        stage.append({"path": path, "sha256": digest(raw), "bytes": len(raw), "unchanged": raw == old})
    helper_checks = {p: digest((ROOT/p).read_bytes()) == h for p, h in HELPERS.items()}
    old_qa = subprocess.check_output(["python3", "-B", "scripts/clay_b_euler_scaling_qa.py"], cwd=ROOT)
    old_saved = (ROOT/"research/clay_b_euler_scaling_qa_20260906.json").read_bytes()
    old_qa_check = old_qa == old_saved and json.loads(old_qa)["status"] == "PASS"
    paper = json.loads((ROOT/"research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT/"AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "parsed_private_paper_unchanged": digest(json.dumps(paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
    }
    controls = {
        "wrong_BL_expected_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BL", 20)["checks"]["reviewed_hash"],
        "wrong_BN_tag_count_rejected": not source_check(SOURCES[2][0], SOURCES[2][1], "BN", 7)["checks"]["continuous_unique_tags"],
        "wrong_predecessor_manifest_rejected": not previous_check("0"*64)["pass"],
    }
    exact = arithmetic()
    passed = (all(all(s["checks"].values()) for s in sources) and previous["pass"]
              and all(s["unchanged"] for s in stage) and all(helper_checks.values())
              and old_qa_check and all(protected.values()) and all(controls.values())
              and all(r["pass"] for r in exact))
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "Actual-source integrity and finite written arithmetic; not a PDE certificate or automatic proof semantics",
        "sources": sources, "new_formula_tags_checked": 36, "combined_BK_BN_tags": 48,
        "arithmetic_checks": exact,
        "previous_freeze": {"path": PREVIOUS, "sha256": PREVIOUS_SHA, "source_commit": PREVIOUS_COMMIT, **previous},
        "previous_internal_stage": {"commit": STAGE_COMMIT, "files": stage, "saved_QA_live_identical": old_qa_check},
        "helper_hashes": helper_checks,
        "protected_state": protected, "limited_negative_controls": controls,
        "validator": {"path": str(Path(__file__).relative_to(ROOT)), "sha256": digest(Path(__file__).read_bytes())},
        "publication_state_inspected": False, "simulation": False, "G": "OPEN", "clay_result": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
