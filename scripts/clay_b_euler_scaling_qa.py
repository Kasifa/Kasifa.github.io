#!/usr/bin/env python3
"""Read-only finite exponent and source checks, not a PDE proof certificate."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess

from clay_b_ancient_sequence_qa import source_check

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("research/clay_b_euler_scaling_energy_preflight_20260906.md", "183ddfa8166dcce32143bd5aba9511a59e2b5bbbf07d62884a1b7dcbd00266e3", "BK", 12),
    ("research/clay_b_stage_strategy_review_20260906.md", "addf4d96077852d5ac9733fd04b33488978e99cc71fd9ee5c8c188aa6f338dfd", None, 0),
    ("research/clay_b_stage_strategy_primary_reading_20260906.md", "b7c76e78b8a07eb4d58807f802b937dd68356df513d58024f5fb512ace3bf083", None, 0),
]
PREVIOUS = "research/clay_b_fixed_history_screen_release_20260906.json"
PREVIOUS_SHA = "73ac9094f3786b82a2d4ea6597717bf2f43733f0caf0b089359c30330abb5407"
PREVIOUS_COMMIT = "67476e7a2e236af9c3ce50ca95f8925f032d5704"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def arithmetic_checks():
    # Coefficients of 1, beta, beta^2; all polynomial identities are exact.
    def poly(a=0, b=0, c=0):
        return (F(a), F(b), F(c))

    def add(a, b):
        return tuple(x+y for x, y in zip(a, b))

    def scale(k, a):
        return tuple(F(k)*x for x in a)

    def sub(a, b):
        return add(a, scale(-1, b))

    def at(a, beta):
        return sum(x*F(beta)**j for j, x in enumerate(a))

    rows = []

    def check(name, actual, expected):
        if not isinstance(actual, tuple):
            actual, expected = poly(actual), poly(expected)
        rows.append({"name": name, "actual_coefficients": list(map(str, actual)),
                     "expected_coefficients": list(map(str, expected)),
                     "pass": actual == expected})

    amplitude, time, pressure = poly(1, 1), poly(2, 1), poly(2, 2)
    time_term = add(amplitude, time)
    check("transport minus time exponent", sub(add(scale(2, amplitude), poly(1)), time_term), poly())
    check("pressure gradient minus time exponent", sub(add(pressure, poly(1)), time_term), poly())
    check("resulting viscosity exponent", sub(time_term, add(amplitude, poly(2))), poly(0, 1))
    energy = sub(scale(2, amplitude), poly(3))
    check("cell L2 exponent", energy, poly(-1, 2))
    check("gradient spacetime exponent", sub(sub(scale(2, add(amplitude, poly(1))), poly(3)), time), poly(-1, 1))
    check("pressure L3over2 spacetime exponent", sub(sub(scale(F(3, 2), pressure), poly(3)), time), poly(-2, 2))
    cubic = sub(sub(scale(3, amplitude), poly(3)), time)
    check("short-window cubic exponent", cubic, poly(-2, 2))
    holder = scale(F(1, 4), time)
    check("time Holder factor exponent", holder, poly(F(1, 2), F(1, 4)))
    gn = add(cubic, holder)
    check("energy-only GN exponent", gn, poly(F(-3, 2), F(9, 4)))
    check("nonhomogeneous GN lower term exponent", add(cubic, time), poly(0, 3))
    check("energy-only GN threshold beta2over3", at(gn, F(2, 3)), 0)
    conditional = scale(F(3, 4), energy)
    check("conditional local GN small factor exponent", conditional, poly(F(-3, 4), F(3, 2)))
    check("conditional threshold beta1over2", at(conditional, F(1, 2)), 0)
    check("mixed norm kappa", 3*(F(3, 3)+F(2, 3)-1), 2)
    p = 1/F(3, 10)
    check("eta0 p and q", p, F(10, 3))
    numerator = F(3, 2)*(1+3/p)
    check("compatibility numerator exponent", numerator, F(57, 20))
    denominator = poly(0, 2, 1)
    check("compatibility denominator polynomial", scale(2, poly(0, 1, F(1, 2))), denominator)
    ratio = sub(poly(0, numerator), denominator)
    check("compatibility ratio polynomial", ratio, poly(0, F(17, 20), -1))
    check("compatibility at beta1", at(ratio, 1), F(-3, 20))
    check("compatibility at beta1over2", at(ratio, F(1, 2)), F(7, 40))
    return rows


def previous_check(expected):
    raw = (ROOT/PREVIOUS).read_bytes()
    obj = json.loads(raw)
    if digest(raw) != expected or obj["source_commit"] != PREVIOUS_COMMIT:
        return {"pass": False, "rows_checked": 0, "failures": ["manifest identity"]}
    rows = obj["files"]+obj["dependencies"]
    failures = []
    if len(rows) != 89 or len({r["path"] for r in rows}) != 89:
        failures.append("count or duplicate")
    for row in rows:
        work = (ROOT/row["path"]).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{PREVIOUS_COMMIT}:{row['path']}"], cwd=ROOT)
        if not (work == frozen and digest(work) == row["sha256"] and len(work) == row["bytes"]):
            failures.append(row["path"])
    return {"pass": not failures, "rows_checked": len(rows), "failures": failures}


def main():
    sources = [source_check(*row) for row in SOURCES]
    arithmetic = arithmetic_checks()
    previous = previous_check(PREVIOUS_SHA)
    paper = json.loads((ROOT/"research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT/"AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "parsed_private_paper_unchanged": digest(json.dumps(paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
    }
    controls = {
        "wrong_BK_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BK", 12)["checks"]["reviewed_hash"],
        "wrong_BK_tag_count_rejected": not source_check(SOURCES[0][0], SOURCES[0][1], "BK", 11)["checks"]["continuous_unique_tags"],
        "wrong_previous_manifest_rejected": not previous_check("0"*64)["pass"],
    }
    passed = (all(all(s["checks"].values()) for s in sources)
              and all(r["pass"] for r in arithmetic) and previous["pass"]
              and all(protected.values()) and all(controls.values()))
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "Internal source integrity and explicitly written finite polynomial algebra; not a PDE proof certificate",
        "sources": sources, "formula_tags_checked": 12, "arithmetic_checks": arithmetic,
        "previous_freeze": {"path": PREVIOUS, "sha256": PREVIOUS_SHA, "source_commit": PREVIOUS_COMMIT, **previous},
        "protected_state": protected, "limited_negative_controls": controls,
        "validator": {"path": str(Path(__file__).relative_to(ROOT)), "sha256": digest(Path(__file__).read_bytes()),
                      "frozen_helper": "scripts/clay_b_ancient_sequence_qa.py", "helper_sha256": digest((ROOT/"scripts/clay_b_ancient_sequence_qa.py").read_bytes())},
        "new_research_release": False, "publication_state_inspected": False,
        "simulation": False, "G": "OPEN",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
