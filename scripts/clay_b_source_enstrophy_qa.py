#!/usr/bin/env python3
"""Finite named bookkeeping and byte checks, never a PDE or novelty certificate."""
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
    ("research/clay_b_source_enstrophy_20260907.md", "0008aef30fe1bf6364e924b17d2830e0ed42b47da4cb5d2445feac980c8de3a4", "BW", 18),
    ("research/clay_b_source_enstrophy_reading_20260907.md", "b3486a49e85723d2c8967bffe52cbfd1ae232518b66cb5c249fa539d5a421c7a", None, 0),
    ("research/clay_b_source_enstrophy_report-source_20260907.md", "b6f6b07247253102699ca9c32fb515fe0fed2497da223a7530552134ca46f5ed", None, 0),
]
PREVIOUS = "research/clay_b_signed_mixed_pressure_release_20260907.json"
PREVIOUS_SHA = "b4d5090a3e365a0f298f2b8f9bd46db7f00a90d3c23e2507e79d3b72b9bceaa5"
PREVIOUS_COMMIT = "cb5acbb4416ca2d6502e9b7d48d19f91a150f2a0"
HELPER = "scripts/clay_b_ancient_sequence_qa.py"
HELPER_SHA = "b9e3451bbb1774ebcf9ab4a5fb40a2722368bff3d04caee0b3cedcce2a5254d7"
LEDGER = "research/clay_b_source_enstrophy_literature_ledger_20260907.json"
LEDGER_SHA = "fa346bb0cf05a0c6a0576c2b209bc9e0987dcfd3e84adcd63b26e67354c2d885"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def specific_literals(text):
    return (r"H(z,w)'=-2\nu cK_w-2B_b(z,w)" in text
            and r"\int_0^\delta\|\Delta w(\rho)\|_2^{4/3}\,d\rho=+\infty" in text)


def previous_check(expected):
    raw = (ROOT/PREVIOUS).read_bytes()
    obj = json.loads(raw)
    if digest(raw) != expected or obj["source_commit"] != PREVIOUS_COMMIT:
        return {"pass": False, "rows_checked": 0, "failures": ["manifest identity"]}
    rows = obj["files"]+obj["dependencies"]
    failures = []
    if len(rows) != 156 or len({r["path"] for r in rows}) != 156:
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

    check("BW2 polarization factor", 1/F(2), F(1, 2))
    check("BW3 b diffusion RHS coefficient", (-1)*(-1), 1)
    check("BW3 w diffusion RHS coefficient", (-1)*1, -1)
    check("BW3 z source coefficient divided by nu c", (-1)*2, -2)
    check("BW4 opposite cross diffusion cancellation", -((-1)+1), 0)
    check("BW4 source coefficient divided by nu c", -2*1, -2)
    check("BW7 symmetric off diagonal c a coefficient", (2+1-1)/F(2), 1)
    check("BW7 determinant a e coefficient", (-1)*1, -1)
    check("BW7 determinant a c d coefficient", (-1)*2, -2)
    check("BW7 determinant a squared c squared coefficient", -(1*1), -1)
    check("BW10 gradient L4 interpolation reciprocal", F(1, 4)/2+F(3, 4)/6, F(1, 4))
    check("BW10 gradient-square Gamma power", 2*F(1, 4)/2, F(1, 4))
    check("BW10 Young K exponent", 1/F(3, 4), F(4, 3))
    check("BW10 Young remaining exponent", 1/(1-F(3, 4)), 4)
    check("BW10 viscosity negative power", -F(3, 4)/(1-F(3, 4)), -3)
    check("BW10 Gamma_b power", 4/F(2), 2)
    check("BW9 source-square Young coefficient", 2**2/(4*F(1, 2)), 2)
    check("BW13 self Gamma power after Young", F(3, 4)*4, 3)
    check("BW13 c power after Young", 1*4, 4)
    check("BW17 convective spatial reciprocal", F(1, 3)+F(1, 6), F(1, 2))
    check("BW17 convective temporal reciprocal", F(1, 4)+F(3, 4), 1)
    check("BW17 heat interval power", 1-F(3, 4), F(1, 4))
    check("BW18 weighted-work temporal reciprocal", F(1, 4)+F(3, 4), 1)
    check("BW16 finite L2 to L4over3 interval power", F(3, 4)-F(1, 2), F(1, 4))
    check("Literature energy p3 q4 condition LHS", F(6, 3)+F(5, 4), F(13, 4))
    return rows


def main():
    sources = [source_check(*row) for row in SOURCES]
    for row in sources:
        row["checks"]["no_bare_qquad"] = re.search(r"(?<!\\)\bqquad\b", (ROOT/row["path"]).read_text()) is None
    actual = (ROOT/SOURCES[0][0]).read_text()
    sources[0]["checks"]["two_specific_formula_literals"] = specific_literals(actual)
    previous = previous_check(PREVIOUS_SHA)
    old_live = subprocess.check_output([sys.executable, "-B", "scripts/clay_b_signed_mixed_pressure_qa.py"], cwd=ROOT)
    old_saved = (ROOT/"research/clay_b_signed_mixed_pressure_qa_20260907.json").read_bytes()
    old_qa = old_live == old_saved and json.loads(old_live)["status"] == "PASS"
    paper = json.loads((ROOT/"research/clay_b_active_checkpoint_20260906.json").read_text())["paper"]
    protected = {
        "user_agents_unchanged": digest((ROOT/"AGENTS.md").read_bytes()) == "80959a5c6d2db01543f8f1ae1ddc2e1ba7430c1b14d1b4ef658dcc965efecfab",
        "parsed_private_paper_unchanged": digest(json.dumps(paper, sort_keys=True).encode()) == "c9755ea86f93575cc96c28ac5b3caa1a059bddec2b58a448d09d9cc54d6431c5",
        "helper_identity": digest((ROOT/HELPER).read_bytes()) == HELPER_SHA,
    }
    wrong_sign = actual.replace(r"H(z,w)'=-2\nu cK_w", r"H(z,w)'=+2\nu cK_w", 1)
    wrong_power = actual.replace(r"\|\Delta w(\rho)\|_2^{4/3}", r"\|\Delta w(\rho)\|_2^{5/4}", 1)
    controls = {
        "wrong_BW_hash_rejected": not source_check(SOURCES[0][0], "0"*64, "BW", 18)["checks"]["reviewed_hash"],
        "wrong_BW_tag_count_rejected": not source_check(SOURCES[0][0], SOURCES[0][1], "BW", 17)["checks"]["continuous_unique_tags"],
        "wrong_predecessor_manifest_rejected": not previous_check("0"*64)["pass"],
        "actual_text_cross_source_sign_rejected": wrong_sign != actual and not specific_literals(wrong_sign),
        "actual_text_trace_power_rejected": wrong_power != actual and not specific_literals(wrong_power),
    }
    ledger_raw = (ROOT/LEDGER).read_bytes()
    ledger = {"path": LEDGER, "sha256": digest(ledger_raw), "bytes": len(ledger_raw),
              "identity_pass": digest(ledger_raw) == LEDGER_SHA,
              "parse_pass": isinstance(json.loads(ledger_raw), dict)}
    exact = arithmetic()
    passed = (all(all(r["checks"].values()) for r in sources) and previous["pass"] and old_qa
              and all(protected.values()) and all(controls.values()) and all(r["pass"] for r in exact)
              and ledger["identity_pass"] and ledger["parse_pass"])
    result = {
        "status": "PASS" if passed else "FAIL",
        "classification": "25 named finite coefficients/exponents plus source bytes; not a PDE, limit, matrix-positivity or novelty certificate",
        "sources": sources, "formula_tags_checked": 18, "arithmetic_checks": exact,
        "previous_freeze": {"path": PREVIOUS, "sha256": PREVIOUS_SHA, "source_commit": PREVIOUS_COMMIT, **previous},
        "previous_saved_QA_live_identical": old_qa, "previous_saved_QA_bytes": len(old_saved),
        "literature_ledger": ledger, "protected_state": protected, "limited_negative_controls": controls,
        "validator": {"path": str(Path(__file__).relative_to(ROOT)), "sha256": digest(Path(__file__).read_bytes()),
                      "helper": HELPER, "helper_sha256": HELPER_SHA},
        "publication_state_inspected": False, "simulation": False, "G": "OPEN", "clay_result": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
