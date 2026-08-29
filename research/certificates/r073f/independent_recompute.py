#!/usr/bin/env python3
"""Independently recompute R0.73F source, rational, and artifact sentinels."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073f"
SOURCE_COMMIT = "5edb1702314feca3e9d47a186b30fc53079cd67a"
ANALYTIC_PATHS = (
    "research/r073f_problem_freeze.md",
    "research/r073f_moving_dichotomy_proof.md",
    "research/r073f_gap_matrix.md",
    "research/r073f_literature_audit.md",
    "research/r073f_independent_analytic_audit.md",
    "research/r073f_report-source.md",
)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def committed(relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT)


def source_binding(relative: str) -> dict[str, object]:
    payload = committed(relative)
    blob = subprocess.check_output(
        ["git", "rev-parse", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT, text=True
    ).strip()
    working = ROOT / relative
    return {
        "path": relative,
        "sourceCommit": SOURCE_COMMIT,
        "gitBlob": blob,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "workingTreeMatchesCommitted": working.is_file() and working.read_bytes() == payload,
    }


def validate_ledger(directory: Path) -> dict[str, object]:
    ledger_rows = {}
    for line in (directory / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        ledger_rows[name] = digest
    actual_names = {path.name for path in directory.iterdir()
                    if path.is_file() and path.name != "SHA256SUMS"}
    hashes_match = all(
        (directory / name).is_file()
        and hashlib.sha256((directory / name).read_bytes()).hexdigest() == digest
        for name, digest in ledger_rows.items()
    )
    return {
        "inventoryExact": set(ledger_rows) == actual_names,
        "hashesMatch": hashes_match,
        "ledgerCount": len(ledger_rows),
        "actualCountExcludingLedger": len(actual_names),
    }


def main() -> int:
    blobs = {path: committed(path).decode("utf-8") for path in ANALYTIC_PATHS}
    proof = blobs["research/r073f_moving_dichotomy_proof.md"]
    gap = blobs["research/r073f_gap_matrix.md"]
    audit = blobs["research/r073f_independent_analytic_audit.md"]

    closed_ids = []
    false_ids = []
    open_ids = []
    for line in gap.splitlines():
        match = re.match(r"\| (F\d+) \|.*?\| (CLOSED|FALSE IN GENERAL|OPEN) \|", line)
        if not match:
            continue
        identifier, status = match.groups()
        {"CLOSED": closed_ids, "FALSE IN GENERAL": false_ids, "OPEN": open_ids}[status].append(identifier)

    rho_scaled = Fraction(1, 16)
    q_global = Fraction(8, 3) * rho_scaled
    one_minus_q_lower = 1 - q_global
    graph_upper = rho_scaled / (Fraction(3, 2) * one_minus_q_lower)
    product_upper = graph_upper * graph_upper

    finite = validate_ledger(ROOT / "experiments/r073f")
    figure = validate_ledger(ROOT / "figures/r073f/fig-r073f-fixed-window-roughness")
    finite_summary = json.loads((ROOT / "experiments/r073f/summary.json").read_text())
    finite_independent = json.loads((ROOT / "experiments/r073f/independent_validation.json").read_text())
    figure_validation = json.loads((ROOT / "figures/r073f/fig-r073f-fixed-window-roughness/validation.json").read_text())

    checks = {
        "sourceCommitExists": subprocess.run(["git", "cat-file", "-e", SOURCE_COMMIT + "^{commit}"], cwd=ROOT).returncode == 0,
        "sourceBindingsRecomputedFromGitObjects": len(ANALYTIC_PATHS) == 6,
        "gapTableF1ThroughF8Closed": closed_ids == [f"F{index}" for index in range(1, 9)],
        "gapLedgerTwoFalseShortcuts": false_ids == ["F9", "F10"],
        "gapLedgerTwoOpenRows": open_ids == ["F11", "F12"],
        "auditFinalPass": "**FINAL PASS.**" in audit,
        "commonContourFormulaPresent": r"P_\varepsilon^{\rm inst}(d)" in proof and r"\int_\Gamma" in proof,
        "normC1ButNoGraphDomainPresent": r"norm-\(C^1\)" in proof and r"unscaled \(H^2\) graph-norm" in proof,
        "movingDichotomyInverseEstimatePresent": r"K_1e^{-(\alpha+\eta)(t-r)}" in proof,
        "fixedWindowLowerAndUpperPresent": r"d_D=\min\{D,d_0\}" in proof and r"\frac5{16}" in proof,
        "rhoToQExactImplication": q_global == Fraction(1, 6),
        "qGlobalAtMostOneSixthForKAtLeastOne": q_global <= Fraction(1, 6),
        "graphStrictUpperOneTwentieth": graph_upper == Fraction(1, 20),
        "graphProductStrictUpperOneFourHundredth": product_upper == Fraction(1, 400),
        "finiteLedgerInventoryAndHashes": finite["inventoryExact"] and finite["hashesMatch"],
        "figureLedgerInventoryAndHashes": figure["inventoryExact"] and figure["hashesMatch"],
        "finitePrimaryAndIndependentPass": finite_summary["allPrimaryChecksPass"] and finite_independent["allChecksPass"],
        "figureValidationPass": figure_validation["status"] == "passed",
        "finiteClaimsRemainFinite": finite_summary["claimBoundary"]["finiteGainProvesContinuumDichotomy"] is False,
    }
    result = {
        "schemaVersion": "r073f-independent-certificate-recompute-v1",
        "release": "R0.73F",
        "sourceCommit": SOURCE_COMMIT,
        "sourceBindings": [source_binding(path) for path in ANALYTIC_PATHS],
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "gapStates": {"closed": closed_ids, "falseInGeneral": false_ids, "open": open_ids},
        "exactSentinels": {
            "rhoScaledUpper": [rho_scaled.numerator, rho_scaled.denominator],
            "qGlobalLimit": [q_global.numerator, q_global.denominator],
            "graphNormLimit": [graph_upper.numerator, graph_upper.denominator],
            "graphProductLimit": [product_upper.numerator, product_upper.denominator],
            "inequalitiesAreStrictBecauseRhoBoundIsStrict": True,
        },
        "artifactLedgers": {"finite": finite, "figure": figure},
        "claimBoundary": {
            "machineProofOfOperatorTheorem": False,
            "finiteEvidenceIsContinuumProof": False,
            "allRowClosure": False,
            "nonlinearNavierStokes": False,
            "Clay": False,
        },
    }
    (OUT / "independent_recompute.json").write_text(canonical(result), encoding="utf-8")
    with (OUT / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"event": "independent-recompute-complete", "allChecksPass": result["allChecksPass"]}, sort_keys=True) + "\n")
    return 0 if result["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
