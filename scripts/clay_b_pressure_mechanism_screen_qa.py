#!/usr/bin/env python3
"""Read-only provenance and rational checks, not a PDE proof certificate."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("research/clay_b_periodic_radial_pressure_identity_20260906.md", "20ff518eddb94f9a4b120ce2b7caaf6e9318d3c3d7bbb6310d8fde764c17664b", "BF", 15),
    ("research/clay_b_pressure_potential_energy_screen_20260906.md", "05546f98e5afffa9093c78c95c771428d783cfc36281c82f4d0b87d62c508efb", "BG", 22),
    ("research/clay_b_pressure_mechanism_primary_reading_20260906.md", "888d834803b8c018630892cf136ee1247803933c629bf9b75655c5b9e1b4e1a3", None, 0),
    ("research/clay_b_pressure_mechanism_screen_report_20260906.md", "2eb627e33ffebfeb49b0ddb7d40f1d6cf23ab7c15f720974a6299e291a7f2de4", None, 0),
]
PREVIOUS = "research/clay_b_recent_source_screen_release_20260906.json"
PREVIOUS_SHA = "d15d3bb15e8481c5f389c562665b374c2f7a16139eb1f32029b8ed6b0381102b"
PREVIOUS_COMMIT = "5314045dcedcc7e781d9fed0f167cae5c0451d62"
AH = "research/clay_b_pressure_residual_obstruction_20260906.md"
AH_SHA = "12d1c6b1c658084ce9243e5ab985347acb49f1bb6bd06757fe82e2ff93da416a"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_check(path, expected, prefix, count):
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
        "clay_boundary": "NOT CLAY" in text,
    }
    return {"path": path, "sha256": digest(data), "bytes": len(data),
            "lines": len(text.splitlines()), "formula_tags": count, "checks": checks}


def rational_checks():
    rows = []

    def check(name, actual, expected):
        actual, expected = F(actual), F(expected)
        rows.append({"name": name, "actual": str(actual), "expected": str(expected),
                     "pass": actual == expected})

    check("BF w1 mass divided by pi R2", 4 / F(2), 2)
    check("BF w0 mass divided by pi R3", 4 / F(3), F(4, 3))
    check("BF unit w1 boundary value", 1 - F(1, 2), F(1, 2))
    check("BF unit w1 boundary derivative", -F(1, 2), -F(1, 2))
    check("BF unit w0 boundary value", F(1, 2) - F(1, 6), F(1, 3))
    check("BF unit w0 boundary derivative", -2 / F(6), -F(1, 3))
    check("BF w1 interior radial Poisson coefficient", -2 * (-F(1, 2)), 1)
    check("BF w0 interior Poisson coefficient", -6 * (-F(1, 6)), 1)
    check("BF first correction coefficient", 2 * 2, 4)
    check("BF second correction coefficient", 3 * F(4, 3), 4)
    check("BF constant field tangential integral divided by pi", F(8, 3) / 2, F(4, 3))
    check("BG kernel L3/2 R power", 3 / F(3, 2) - 1, 1)
    check("BG kernel L2 R power", 3 / F(2) - 1, F(1, 2))
    check("BG L4 interpolation theta", (F(1, 2) - F(1, 4)) / (F(1, 2) - F(1, 6)), F(3, 4))
    check("BG pressure L2 M power", 2 * (1 - F(3, 4)), F(1, 2))
    check("BG pressure L2 gradient power", 2 * F(3, 4), F(3, 2))
    check("BG time integrability gradient power", F(3, 2) * F(4, 3), 2)
    check("BG time integrability M power", F(1, 2) * F(4, 3), F(2, 3))
    check("BG fixed energy amplitude squared volume", -3 + 3, 0)
    check("BG gradient energy epsilon power", -3 - 2 + 3, -2)
    check("BG singular pressure epsilon power", -3 - 3 + 3, -3)
    check("BG smooth pressure correction epsilon power", -3 + 3, 0)
    check("BG negative potential epsilon power", -3 + 3 - 1, -1)
    check("BG core rotation amplitude epsilon power", -F(3, 2) - 1, -F(5, 2))
    check("BG E prime contribution to A log derivative", F(1, 2) * (-2), -1)
    return rows


def main():
    sources = [source_check(*row) for row in SOURCES]
    arithmetic = rational_checks()
    previous_bytes = (ROOT / PREVIOUS).read_bytes()
    previous = json.loads(previous_bytes)
    rows = previous["files"] + previous["dependencies"]
    failures = []
    if digest(previous_bytes) != PREVIOUS_SHA or previous["source_commit"] != PREVIOUS_COMMIT:
        failures.append("previous identity")
    if len(rows) != 65 or len({row["path"] for row in rows}) != 65:
        failures.append("previous row count or duplicate")
    for row in rows:
        work = (ROOT / row["path"]).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{PREVIOUS_COMMIT}:{row['path']}"], cwd=ROOT)
        if not (work == frozen and digest(work) == row["sha256"] and len(work) == row["bytes"]):
            failures.append(row["path"])
    ah_bytes = (ROOT / AH).read_bytes()
    ah_frozen = subprocess.check_output(["git", "show", f"{PREVIOUS_COMMIT}:{AH}"], cwd=ROOT)
    ah_ok = digest(ah_bytes) == AH_SHA and ah_bytes == ah_frozen
    passed = (all(all(row["checks"].values()) for row in sources)
              and all(row["pass"] for row in arithmetic) and not failures and ah_ok)
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "Source integrity and exact rational bookkeeping, not a PDE proof certificate",
        "sources": sources,
        "formula_tags_checked": sum(row["formula_tags"] for row in sources),
        "fraction_checks": arithmetic,
        "previous_freeze": {"path": PREVIOUS, "sha256": digest(previous_bytes),
                            "source_commit": previous["source_commit"], "rows_checked": len(rows),
                            "worktree_and_source_commit_bytes_hash_size": not failures,
                            "failures": failures},
        "AH_reused_source": {"path": AH, "sha256": digest(ah_bytes), "bytes": len(ah_bytes),
                             "worktree_source_commit_hash": ah_ok},
        "validator": {"path": str(Path(__file__).relative_to(ROOT)),
                      "sha256": digest(Path(__file__).read_bytes())},
        "publication_state_inspected": False, "simulation": False, "G": "OPEN",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
