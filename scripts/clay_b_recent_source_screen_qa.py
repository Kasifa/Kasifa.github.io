#!/usr/bin/env python3
"""Read-only integrity and rational bookkeeping; not a PDE proof checker."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("research/clay_b_recent_source_energy_benchmark_20260906.md", "828ddd67f693591540c6c246b460b6708811eb67a4ef596eb9b4f190a8019f69", "BC", 18),
    ("research/clay_b_dyadic_recent_source_screen_20260906.md", "e1bbdc21cc3327383d61782245ec698035c75b1e0c506458bde6d3d63dc83fa3", "BD", 22),
    ("research/clay_b_static_background_comparison_20260906.md", "1881a50f1628cc249ec5d8bd9c228abf43962e633419bec37c12623ab5ea198b", "BE", 17),
    ("research/clay_b_recent_source_screen_report_20260906.md", "cbf97012e2c54b9bd19fa3e60d3e11a360f08e0d0b6b64e3e6631d245c3b636d", None, 0),
    ("research/clay_b_recent_source_screen_literature_20260906.md", "4e0f9f113b47cd301ceb5684d4bc8c626293a5a0d5cf5ec37fdf9d471c12364a", None, 0),
    ("research/clay_b_pressure_mechanism_review_plan_20260906.md", "ec6999f936f94554a757fd8d880c82388208fd1251a3bbaa0e8db6f01878ea60", None, 0),
    ("research/clay_b_recent_source_screen_internal_audit_20260906.md", "cf22fb4134eff744479a387601e34a5e0e25714de07bbacf0ce405f02a68e214", None, 0),
]
PREVIOUS = "research/clay_b_lagged_pressure_release_20260906.json"
PREVIOUS_SHA = "14ee88415128d1ca4dd65648efb8a1168815d1264f16e24f8d264aa07d5d6dfd"
PREVIOUS_COMMIT = "891e6b85f53ae19272973c191726f1278e47918b"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    source_rows = []
    for path, expected, prefix, count in SOURCES:
        data = (ROOT / path).read_bytes()
        text = data.decode("utf-8")
        tags = re.findall(r"\\tag\{([A-Z]+)\.(\d+)\}", text)
        wanted = [(prefix, str(n)) for n in range(1, count + 1)] if prefix else []
        checks = {
            "reviewed_hash": digest(data) == expected,
            "continuous_unique_tags": tags == wanted,
            "inline_delimiters": text.count(r"\(") == text.count(r"\)"),
            "display_delimiters": text.count(r"\[") == text.count(r"\]"),
            "no_control_characters": not any(ord(c) < 32 and c not in "\n\t" for c in text),
            "no_trailing_whitespace": all(line == line.rstrip() for line in text.splitlines()),
            "final_newline": data.endswith(b"\n"),
            "explicit_clay_boundary": "NOT CLAY" in text,
        }
        source_rows.append({"path": path, "sha256": digest(data), "bytes": len(data),
                            "lines": len(text.splitlines()), "formula_tags": count, "checks": checks})

    arithmetic = []

    def check(name, value, expected):
        value, expected = F(value), F(expected)
        arithmetic.append({"name": name, "actual": str(value), "expected": str(expected),
                           "pass": value == expected})

    check("BC delta/tau", -4 + F(8, 3), F(-4, 3))
    check("BC pure heat with A_J", F(16, 3) - 6, F(-2, 3))
    check("BC pure heat constant", F(16, 3) - 7, F(-5, 3))
    check("remaining dissipation", F(3, 4) - F(1, 8), F(5, 8))
    check("BD tensor L3/2 to H1 kernel", 2 + 3 * (F(2, 3) - F(1, 2)), F(5, 2))
    check("BD pointwise L2 time kernel", F(5, 2) - 2 / F(2), F(3, 2))
    check("BD pointwise L4 time kernel", 2 - 2 / F(4), F(3, 2))
    check("BD L2 result first kernel", F(5, 2) - 2, F(1, 2))
    check("BD L2 result second kernel", 2 - 2 / F(4, 3), F(1, 2))
    check("BD Young first relation", 1 + F(3, 16) - F(1, 2) - F(11, 16), 0)
    check("BD Young second relation", 1 + F(3, 16) - F(3, 4) - F(7, 16), 0)
    check("BD L16/3 first kernel", F(5, 2) - 2 / F(16, 11), F(9, 8))
    check("BD L16/3 second kernel", 2 - 2 / F(16, 7), F(9, 8))
    check("BD square sum weight", 2 * F(9, 8), F(9, 4))
    check("BD first M power", F(1, 2) + 4, F(9, 2))
    check("BD first E power", F(1, 4) + 4 * F(1, 2), F(9, 4))
    check("BD second M power", F(1, 2) + 4 * F(1, 2), F(5, 2))
    check("BD second E power", F(1, 4) + 4 * F(3, 4), F(13, 4))
    check("BD lowest band Lambda loss", F(3, 4) * F(9, 2) - 3, F(3, 8))
    check("BD scalar L1 exponent", 2 - 3, -1)
    check("BD scalar normalized square exponent", -1 + 4 - 3, 0)
    alpha = F(4, 3)
    check("BE N/K exponent", alpha - F(3, 4), F(7, 12))
    for name, actual, expected in [
        ("BE first remainder", 3 * alpha - 4, 0),
        ("BE second remainder", 3 * alpha - 7, -3),
        ("BE third remainder", F(3, 2) * alpha - 4, -2),
        ("BE fourth remainder", F(3, 2) * alpha - 7, -5),
        ("BE fifth remainder", 4 * alpha - 7, F(-5, 3)),
        ("BE heat L infinity comparison", 2 * F(3, 4), F(3, 2)),
        ("BE heat pressure gradient comparison", 2 * 2, 4),
    ]:
        check(name, actual, expected)

    previous_data = (ROOT / PREVIOUS).read_bytes()
    previous = json.loads(previous_data)
    rows = previous["files"] + previous["dependencies"]
    previous_failures = []
    if digest(previous_data) != PREVIOUS_SHA or previous["source_commit"] != PREVIOUS_COMMIT:
        previous_failures.append("previous manifest identity")
    if len(rows) != 51 or len({row["path"] for row in rows}) != 51:
        previous_failures.append("previous manifest count or duplicates")
    for row in rows:
        work = (ROOT / row["path"]).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{PREVIOUS_COMMIT}:{row['path']}"], cwd=ROOT)
        if not (work == frozen and digest(work) == row["sha256"] and len(work) == row["bytes"]):
            previous_failures.append(row["path"])

    passed = (all(all(row["checks"].values()) for row in source_rows)
              and all(row["pass"] for row in arithmetic) and not previous_failures)
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "Source integrity and exact rational bookkeeping; not a PDE proof certificate",
        "sources": source_rows,
        "formula_tags_checked": sum(row["formula_tags"] for row in source_rows),
        "fraction_checks": arithmetic,
        "previous_freeze": {"path": PREVIOUS, "sha256": digest(previous_data),
                            "source_commit": previous["source_commit"], "rows_checked": len(rows),
                            "worktree_and_source_commit_bytes_hash_size": not previous_failures,
                            "failures": previous_failures},
        "validator": {"path": str(Path(__file__).relative_to(ROOT)),
                      "sha256": digest(Path(__file__).read_bytes())},
        "publication_state_inspected": False,
        "simulation": False,
        "G": "OPEN",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
