#!/usr/bin/env python3
"""Read-only source and algebra checks, not a PDE proof certificate."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess

from clay_b_ancient_sequence_qa import source_check

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("research/clay_b_fixed_history_mild_preflight_20260906.md", "6889ac3d6297c651b37a0292867b9706fd028bd03f65564857054b75ec5c2fb4", "BI", 20),
    ("research/clay_b_record_time_history_preflight_20260906.md", "a5a066edbbdaec0c7b046f0741414ef68c3915faba55f8a7470da66ac96119b3", "BJ", 32),
    ("research/clay_b_fixed_history_report_20260906.md", "fa576ce97d2bb7080ea9eaee6b0342cfc6c34180c7c2da5155c2169911a818b2", None, 0),
    ("research/clay_b_fixed_history_primary_reading_20260906.md", "ace36d02d7b3fbbe650756d5536dbb93136fda5d3b30189aebe57c3627811693", None, 0),
]
PREVIOUS = "research/clay_b_ancient_constant_screen_release_20260906.json"
PREVIOUS_SHA = "9712e6cfc929cdf397428eca3c141df8720f4a0e3a7fae68fd4bc83d0db0fa33"
PREVIOUS_COMMIT = "4dfd49be08e9f8bb253432851669c9d632936b5c"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def arithmetic_checks():
    rows = []

    def scalar(name, actual, expected):
        actual, expected = F(actual), F(expected)
        rows.append({"name": name, "kind": "rational", "actual": str(actual),
                     "expected": str(expected), "pass": actual == expected})

    def affine(name, actual, expected):
        # Pair (constant, coefficient of eta); no finite sampling of eta.
        actual, expected = tuple(map(F, actual)), tuple(map(F, expected))
        rows.append({"name": name, "kind": "affine_in_eta", "actual": list(map(str, actual)),
                     "expected": list(map(str, expected)), "pass": actual == expected})

    scalar("BI kernel L1 time exponent", F(3, 2)-2, F(-1, 2))
    scalar("BI kernel spatial tail exponent", 3-4, -1)
    scalar("BI periodic image contribution M exponent", 1+2-4, -1)
    scalar("BI cell L2 energy M exponent", -2+3, 1)
    scalar("BI spacetime dissipation M exponent", -4+3+2, 1)
    scalar("Initial cell L3 cubed M exponent", -3+3, 0)
    scalar("BI initial velocity M exponent", -1, -1)
    scalar("BI full history over period squared exponent", 2-2, 0)
    scalar("BI old time kernel integral exponent", -2+1, -1)
    affine("BI growing-window over full-history exponent", (1-2, 1), (-1, 1))
    affine("BI growing-window old-tail exponent", (1-1, -1), (0, -1))
    affine("BI growing-window physical-time exponent", (1-2, 1), (-1, 1))

    q = F(1, 4)
    s0, s1, s2 = q/(1-q), q/(1-q)**2, q*(1+q)/(1-q)**3
    scalar("BJ geometric sum", s0, F(1, 3))
    scalar("BJ first geometric moment", s1, F(4, 9))
    scalar("BJ second geometric moment", s2, F(20, 27))
    scalar("BJ scalar A linear j coefficient", 2*s1, F(8, 9))
    a2, a1, a0 = s0, 2*s1, s2
    scalar("BJ recurrence quadratic j coefficient", 4*a2-a2, 1)
    scalar("BJ recurrence linear j coefficient", -8*a2+3*a1, 0)
    scalar("BJ recurrence constant independent of d", 4*a2-4*a1+3*a0, 0)
    scalar("BJ recurrence d coefficient", 4*s0-s0, 1)
    scalar("BJ scalar slope over minimum H cubed coefficient", F(1, 2)/F(1, 8), 4)
    scalar("BJ previous-level lifetime factor", 2**2, 4)
    scalar("BJ Type I upper-bound factor", 2**2, 4)
    return rows


def previous_check(expected_sha):
    raw = (ROOT / PREVIOUS).read_bytes()
    previous = json.loads(raw)
    if digest(raw) != expected_sha or previous["source_commit"] != PREVIOUS_COMMIT:
        return {"pass": False, "rows_checked": 0, "failures": ["previous manifest identity"]}
    rows = previous["files"] + previous["dependencies"]
    failures = []
    if len(rows) != 81 or len({row["path"] for row in rows}) != 81:
        failures.append("previous count or duplicate")
    for row in rows:
        work = (ROOT / row["path"]).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{PREVIOUS_COMMIT}:{row['path']}"], cwd=ROOT)
        if not (work == frozen and digest(work) == row["sha256"] and len(work) == row["bytes"]):
            failures.append(row["path"])
    return {"pass": not failures, "rows_checked": len(rows), "failures": failures}


def main():
    sources = [source_check(*row) for row in SOURCES]
    arithmetic = arithmetic_checks()
    previous = previous_check(PREVIOUS_SHA)
    paper = json.loads((ROOT / "research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT / "AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "private_paper_object_unchanged": digest(json.dumps(paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
    }
    controls = {
        "wrong_reviewed_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BI", 20)["checks"]["reviewed_hash"],
        "wrong_tag_count_rejected": not source_check(SOURCES[1][0], SOURCES[1][1], "BJ", 31)["checks"]["continuous_unique_tags"],
        "wrong_predecessor_manifest_hash_rejected": not previous_check("0"*64)["pass"],
    }
    passed = (all(all(row["checks"].values()) for row in sources)
              and all(row["pass"] for row in arithmetic) and previous["pass"]
              and all(protected.values()) and all(controls.values()))
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "Source integrity, exact rational and affine bookkeeping; not a PDE proof certificate",
        "sources": sources, "formula_tags_checked": 52,
        "arithmetic_checks": arithmetic,
        "previous_freeze": {"path": PREVIOUS, "sha256": PREVIOUS_SHA,
                            "source_commit": PREVIOUS_COMMIT, **previous},
        "protected_state": protected, "negative_controls": controls,
        "validator": {"path": str(Path(__file__).relative_to(ROOT)),
                      "sha256": digest(Path(__file__).read_bytes()),
                      "frozen_helper": "scripts/clay_b_ancient_sequence_qa.py",
                      "helper_sha256": digest((ROOT / "scripts/clay_b_ancient_sequence_qa.py").read_bytes())},
        "publication_state_inspected": False, "simulation": False, "G": "OPEN",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
