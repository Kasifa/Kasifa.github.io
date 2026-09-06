#!/usr/bin/env python3
"""Read-only byte and scaling checks. Not a PDE proof certificate."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("research/clay_b_ancient_constant_sequence_preflight_20260906.md", "b945d23de1829d220e2fee7d4c18a8732622d16b428a8f85dda1216a4ec7e1a0", "BH", 18),
    ("research/clay_b_dynamic_strategy_review_20260906.md", "acfb4d8587a7942784df344b060a72fd20faf18ac013c3f0ed4a20f48f293255", None, 0),
    ("research/clay_b_dynamic_strategy_primary_reading_20260906.md", "2b8f0ae5f98bea63516261d78a1982060aef98757d827bc41363f4408e8e83c1", None, 0),
]
PREVIOUS = "research/clay_b_pressure_mechanism_screen_release_20260906.json"
PREVIOUS_SHA = "378bd958ca9f003f7ef44792de567c98080370bbffa95d261d79c1da9c83c6ea"
PREVIOUS_COMMIT = "1df0d394d3da2c6ae01b843a86b4830d266148a7"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_check(path, expected, prefix, count):
    data = (ROOT / path).read_bytes()
    text = data.decode("utf-8")
    wanted = [(prefix, str(i)) for i in range(1, count + 1)] if prefix else []
    checks = {
        "reviewed_hash": digest(data) == expected,
        "continuous_unique_tags": re.findall(r"\\tag\{([A-Z]+)\.(\d+)\}", text) == wanted,
        "inline_delimiters": text.count(r"\(") == text.count(r"\)"),
        "display_delimiters": text.count(r"\[") == text.count(r"\]"),
        "no_control_characters": not any(ord(c) < 32 and c not in "\n\t" for c in text),
        "no_trailing_whitespace": all(line == line.rstrip() for line in text.splitlines()),
        "final_newline": data.endswith(b"\n"),
        "clay_boundary": "NOT CLAY" in text,
        "personal_prose": not any(s in text for s in ["我们", "攻关", "主攻", "三重审计", "杀死错误想法"]),
    }
    return {"path": path, "sha256": digest(data), "bytes": len(data),
            "lines": len(text.splitlines()), "formula_tags": count, "checks": checks}


def scaling_checks():
    rows = []

    def check(name, value, expected):
        value, expected = F(value), F(expected)
        rows.append({"name": name, "actual": str(value), "expected": str(expected),
                     "pass": value == expected})

    # In U(x,t), x=y/n, t=(s+sqrt(n))/n, original viscosity=n^-1.
    dim, x, t, nu, short_time = 3, F(-1), F(-1), F(-1), F(-1, 2)
    check("BH9 time exponent", t, -1)
    check("BH9 transport exponent", x, -1)
    check("BH9 pressure gradient exponent", x, -1)
    check("BH10 resulting viscosity exponent", t + nu - 2*x, 0)
    check("BH9 new period exponent", 2 - x, 3)
    check("BH9 past length exponent", short_time - t, F(1, 2))
    check("BH11 spatial energy Jacobian", -dim*x, 3)
    gradient_factor = 2*x - dim*x
    check("BH12 gradient spatial Jacobian", gradient_factor, 1)
    check("BH12 gradient spacetime Jacobian", gradient_factor - t, 2)
    dissipation = gradient_factor - t + short_time
    check("BH12 total dissipation bound exponent", dissipation, F(3, 2))
    check("BH1 dissipation divided by period exponent", dissipation - (2-x), F(-3, 2))
    check("BH18 history over period squared exponent", short_time-t-2*(2-x), F(-11, 2))

    # Exact q rescaling in BH13: amplitude=q^-1, x=y/q, t=s/q^2.
    a, xq, tq, pq = F(-1), F(-1), F(-2), F(-2)
    check("BH13 time term q exponent", a+tq, -3)
    check("BH13 transport q exponent", 2*a+xq, -3)
    check("BH13 pressure term q exponent", pq+xq, -3)
    check("BH13 viscous term q exponent", a+2*xq, -3)
    check("BH13 energy q factor", 2*a-dim*xq, 1)
    check("BH13 spacetime dissipation q factor", 2*a+2*xq-dim*xq-tq, 1)
    check("BH14 period q factor", -xq, 1)
    check("BH14 history q factor", -tq, 2)
    check("BH17 fixed initial amplitude M exponent", a, -1)
    check("BH17 full past over period squared M exponent", -tq-2*(-xq), 0)
    return rows


def main():
    sources = [source_check(*row) for row in SOURCES]
    scaling = scaling_checks()
    previous_bytes = (ROOT / PREVIOUS).read_bytes()
    previous = json.loads(previous_bytes)
    rows = previous["files"] + previous["dependencies"]
    failures = []
    if digest(previous_bytes) != PREVIOUS_SHA or previous["source_commit"] != PREVIOUS_COMMIT:
        failures.append("previous manifest identity")
    if len(rows) != 74 or len({row["path"] for row in rows}) != 74:
        failures.append("previous row count or duplicate")
    for row in rows:
        work = (ROOT / row["path"]).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{PREVIOUS_COMMIT}:{row['path']}"], cwd=ROOT)
        if not (work == frozen and digest(work) == row["sha256"] and len(work) == row["bytes"]):
            failures.append(row["path"])
    private_paper = json.loads((ROOT / "research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT / "AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "private_paper_unchanged": digest(json.dumps(private_paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
    }
    # Pure in-memory controls. They do not modify proof files or PDE input data.
    mutation_controls = {
        "wrong_reviewed_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BH", 18)["checks"]["reviewed_hash"],
        "wrong_formula_count_rejected": not source_check(SOURCES[0][0], SOURCES[0][1], "BH", 17)["checks"]["continuous_unique_tags"],
        "wrong_original_viscosity_rejected": F(-1) + F(0) - 2*F(-1) != 0,
        "wrong_q_pressure_amplitude_rejected": F(-1)+F(-1) != F(-1)+F(-2),
    }
    passed = (all(all(row["checks"].values()) for row in sources)
              and all(row["pass"] for row in scaling) and not failures
              and all(protected.values()) and all(mutation_controls.values()))
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "Reviewed-source provenance and exact scaling algebra; not a PDE proof certificate",
        "sources": sources, "formula_tags_checked": 18, "scaling_checks": scaling,
        "previous_freeze": {"path": PREVIOUS, "sha256": digest(previous_bytes),
                            "source_commit": previous["source_commit"], "rows_checked": len(rows),
                            "worktree_and_source_commit_bytes_hash_size": not failures,
                            "failures": failures},
        "protected_state": protected, "mutation_controls": mutation_controls,
        "validator": {"path": str(Path(__file__).relative_to(ROOT)),
                      "sha256": digest(Path(__file__).read_bytes())},
        "publication_state_inspected": False, "simulation": False, "G": "OPEN",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
